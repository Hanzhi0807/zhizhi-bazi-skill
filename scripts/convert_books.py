#!/usr/bin/env python3
"""Convert all reference books to UTF-8 markdown for the zhizhi-bazi-skill.

Reads from D:/workspace/八字知识/参考书籍/
Writes to D:/workspace/zhizhi-bazi-skill/references/source-texts/

Handles: TXT(GBK), EPUB(ZIP+HTML), MOBI(BOOKMOBI), PDF(text)
"""

import os, sys, re, zipfile, zlib, html
from pathlib import Path

# ── Configuration ──────────────────────────────────────────

SOURCE_DIR = Path("D:/workspace/八字知识/参考书籍")
TARGET_DIR = Path("D:/workspace/zhizhi-bazi-skill/references/source-texts")

# Book definitions: (target_filename, source_keyword, author, format_hint)
BOOKS = [
    ("穷通宝鉴.md",         "穷通宝鉴",   "余春台",     "txt"),
    ("滴天髓阐微.md",       "滴天髓阐微", "京图/刘基/任铁樵", "epub"),
    ("子平真诠.md",         "子平真诠",   "沈孝瞻",     "epub"),
    ("渊海子平.md",         "渊海子平",   "徐子平",     "epub"),
    ("千里命稿.md",         "千里命稿",   "韦千里",     "txt"),
    ("三命通会.md",         "三 命 通 会.txt",   "万民英",     "txt"),
    ("神峰通考.md",         "神峰通考",   "张楠",       "pdf"),
    ("兰台妙选.md",         "兰台妙选",   "西窗老人",   "txt"),
]


def find_source_file(keyword):
    """Find the source file containing the given keyword."""
    for f in SOURCE_DIR.iterdir():
        if f.is_file() and keyword in f.name:
            return f
    return None


def read_gbk_text(filepath):
    """Read a GBK-encoded text file, return UTF-8 string."""
    with open(filepath, "rb") as f:
        raw = f.read()
    for enc in ["gbk", "gb18030"]:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    # Last resort: replace errors
    return raw.decode("gbk", errors="replace")


def extract_epub(filepath):
    """Extract text from an EPUB file (ZIP of HTML files)."""
    all_text = []
    with zipfile.ZipFile(filepath) as zf:
        html_files = sorted(
            [n for n in zf.namelist() if n.endswith((".html", ".xhtml", ".htm"))]
        )
        for hf in html_files:
            with zf.open(hf) as f:
                content = f.read().decode("utf-8", errors="replace")
            # Strip HTML tags
            content = re.sub(r"<head[^>]*>.*?</head>", "", content, flags=re.DOTALL)
            content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL)
            content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
            content = re.sub(r"<[^>]+>", "\n", content)
            content = html.unescape(content)
            # Normalize whitespace
            content = re.sub(r"\n\s*\n", "\n\n", content)
            content = re.sub(r" {2,}", " ", content)
            lines = [l.strip() for l in content.split("\n")]
            lines = [l for l in lines if l]  # remove empty lines
            all_text.extend(lines)
    return "\n".join(all_text)


def extract_mobi(filepath):
    """Extract text from a MOBI file."""
    with open(filepath, "rb") as f:
        raw = f.read()

    # Method 1: try UTF-8 decode with errors replace
    text = raw.decode("utf-8", errors="replace")

    # Find the actual book content after MOBI/PalmDOC headers
    # MOBI files have a header then the text in HTML/Markdown-like format
    # Look for the start of actual Chinese text
    lines = text.split("\n")
    content_lines = []
    started = False
    for line in lines:
        stripped = line.strip()
        # Skip control characters and binary garbage
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", stripped)
        if not cleaned:
            continue
        # Check for Chinese chars to know we're in the book content
        chinese = sum(1 for c in cleaned if "一" <= c <= "鿿")
        if chinese > 5:
            started = True
        if started and len(cleaned) > 5:
            content_lines.append(cleaned)

    return "\n".join(content_lines)


def extract_pdf(filepath):
    """Extract text from a PDF file using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        print("  [!] pdfplumber not available, install with: pip install pdfplumber")
        return ""

    all_text = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                all_text.append(text)
    return "\n".join(all_text)


def make_frontmatter(title, author, source_keyword):
    """Generate YAML frontmatter for a source text file."""
    import datetime
    today = datetime.date.today().isoformat()
    return f"""---
title: 《{title}》
author: {author}
source: {source_keyword}
converted: {today}
encoding: UTF-8
confidence: L0-原文
notes: 自动转换自原始文件，部分格式/标点可能因OCR或编码转换产生偏差。引用前建议与可信版本核对。
---

"""


def convert_book(target_name, keyword, author, fmt):
    """Convert one book to UTF-8 markdown."""
    src = find_source_file(keyword)
    if not src:
        print(f"  [!!] Source not found for '{keyword}'")
        return None

    print(f"  Converting: {src.name} ({fmt}) -> {target_name}")

    # Extract text by format
    if fmt == "txt":
        text = read_gbk_text(src)
    elif fmt == "epub":
        text = extract_epub(src)
    elif fmt == "mobi":
        text = extract_mobi(src)
    elif fmt == "pdf":
        text = extract_pdf(src)
    else:
        text = ""

    if not text or len(text.strip()) < 500:
        print(f"  [!!] Extracted text too short ({len(text)} chars) for {keyword}")
        return None

    # Combine frontmatter + content
    frontmatter = make_frontmatter(keyword, author, src.name)
    full_content = frontmatter + text

    # Write output
    outpath = TARGET_DIR / target_name
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(full_content)

    # Stats
    total_chars = len(text)
    chinese_chars = sum(1 for c in text if "一" <= c <= "鿿")
    chinese_pct = chinese_chars / max(total_chars, 1) * 100

    print(f"    -> {outpath}")
    print(f"    -> {total_chars:,} chars, {chinese_pct:.1f}% Chinese")
    return outpath


def self_check():
    """Validate all output files are valid UTF-8 with sufficient Chinese content."""
    print("\n=== Self-check ===")
    all_ok = True
    for f in sorted(TARGET_DIR.glob("*.md")):
        with open(f, "r", encoding="utf-8") as fh:
            text = fh.read()
        chinese = sum(1 for c in text if "一" <= c <= "鿿")
        pct = chinese / max(len(text), 1) * 100
        status = "OK" if pct > 30 else "LOW_CHINESE"
        if status != "OK":
            all_ok = False
        print(f"  [{status}] {f.name}: {len(text):,} chars, {pct:.1f}% Chinese")
    return all_ok


def main():
    print("=== Converting Reference Books to UTF-8 ===")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print()

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for target_name, keyword, author, fmt in BOOKS:
        result = convert_book(target_name, keyword, author, fmt)
        results.append((target_name, result))

    print(f"\n=== Summary ===")
    success = 0
    fail = 0
    for name, path in results:
        if path:
            print(f"  [OK] {name}")
            success += 1
        else:
            print(f"  [FAIL] {name}")
            fail += 1

    print(f"\n{success} succeeded, {fail} failed")

    if success > 0:
        ok = self_check()
        if ok:
            print("\nAll checks passed.")
        else:
            print("\nSome files have low Chinese content - may need manual review.")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
