#!/usr/bin/env python3
"""Calculate a compact Bazi chart from Gregorian birth data.

The script is intentionally dependency-free. Solar-term dates use a common
1900-2100 approximation, so birthdays close to term boundaries are flagged for
external calendar verification.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from dataclasses import dataclass
from typing import Any


STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
POLARITY = {
    "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
    "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴",
}
HIDDEN_STEMS = {
    "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"], "卯": ["乙"],
    "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"], "午": ["丁", "己"],
    "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"], "酉": ["辛"],
    "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"],
}

JIE_TERMS = [
    ("小寒", 1), ("立春", 2), ("惊蛰", 3), ("清明", 4), ("立夏", 5), ("芒种", 6),
    ("小暑", 7), ("立秋", 8), ("白露", 9), ("寒露", 10), ("立冬", 11), ("大雪", 12),
]

# Approximate day constants for jie terms. Values are common compact-calendar
# constants and are sufficient away from boundary dates.
TERM_C_20 = {
    "小寒": 6.11, "立春": 4.6295, "惊蛰": 6.3826, "清明": 5.59,
    "立夏": 6.318, "芒种": 6.5, "小暑": 7.928, "立秋": 8.35,
    "白露": 8.44, "寒露": 9.098, "立冬": 8.218, "大雪": 7.9,
}
TERM_C_21 = {
    "小寒": 5.4055, "立春": 3.87, "惊蛰": 5.63, "清明": 4.81,
    "立夏": 5.52, "芒种": 5.678, "小暑": 7.108, "立秋": 7.5,
    "白露": 7.646, "寒露": 8.318, "立冬": 7.438, "大雪": 7.18,
}

MONTH_BRANCH_BY_TERM = {
    "立春": "寅", "惊蛰": "卯", "清明": "辰", "立夏": "巳", "芒种": "午", "小暑": "未",
    "立秋": "申", "白露": "酉", "寒露": "戌", "立冬": "亥", "大雪": "子", "小寒": "丑",
}
FIRST_MONTH_STEM_BY_YEAR_STEM = {
    "甲": "丙", "己": "丙",
    "乙": "戊", "庚": "戊",
    "丙": "庚", "辛": "庚",
    "丁": "壬", "壬": "壬",
    "戊": "甲", "癸": "甲",
}
FIRST_HOUR_STEM_BY_DAY_STEM = {
    "甲": "甲", "己": "甲",
    "乙": "丙", "庚": "丙",
    "丙": "戊", "辛": "戊",
    "丁": "庚", "壬": "庚",
    "戊": "壬", "癸": "壬",
}


@dataclass(frozen=True)
class Pillar:
    stem: str
    branch: str

    @property
    def text(self) -> str:
        return f"{self.stem}{self.branch}"


def ganzhi(index: int) -> Pillar:
    return Pillar(STEMS[index % 10], BRANCHES[index % 12])


def ganzhi_index(stem: str, branch: str) -> int:
    for i in range(60):
        if STEMS[i % 10] == stem and BRANCHES[i % 12] == branch:
            return i
    raise ValueError(f"invalid ganzhi pair: {stem}{branch}")


def sexagenary_day(date_value: dt.date) -> Pillar:
    reference = dt.date(2000, 1, 1)  # widely used reference: 戊午 day.
    index = (date_value - reference).days + ganzhi_index("戊", "午")
    return ganzhi(index)


def parse_birth_time(value: str) -> tuple[int, int] | None:
    if value.lower() in {"unknown", "unk", "none", "na", "不详", "未知"}:
        return None
    try:
        hour_text, minute_text = value.split(":", 1)
        hour = int(hour_text)
        minute = int(minute_text)
    except Exception as exc:
        raise argparse.ArgumentTypeError("time must be HH:MM or unknown") from exc
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise argparse.ArgumentTypeError("time must be within 00:00-23:59")
    return hour, minute


def term_day(year: int, term_name: str) -> int:
    if not (1900 <= year <= 2100):
        raise ValueError("solar-term approximation supports years 1900-2100")
    yy = year % 100
    constants = TERM_C_20 if year < 2000 else TERM_C_21
    day = math.floor(yy * 0.2422 + constants[term_name]) - math.floor((yy - 1) / 4)
    # Known compact-formula exceptions for common jie terms.
    exceptions = {
        (2084, "立春"): 3,
        (1911, "立春"): 5,
        (2008, "小寒"): 6,
        (2019, "小寒"): 5,
    }
    return exceptions.get((year, term_name), day)


def term_date(year: int, term_name: str) -> dt.date:
    month = dict(JIE_TERMS)[term_name]
    return dt.date(year, month, term_day(year, term_name))


def jie_dates_around(year: int) -> list[tuple[str, dt.date]]:
    dates: list[tuple[str, dt.date]] = []
    for y in (year - 1, year, year + 1):
        if 1900 <= y <= 2100:
            for name, _ in JIE_TERMS:
                dates.append((name, term_date(y, name)))
    return sorted(dates, key=lambda item: item[1])


def active_jie(date_value: dt.date) -> tuple[str, dt.date]:
    candidates = [item for item in jie_dates_around(date_value.year) if item[1] <= date_value]
    if not candidates:
        raise ValueError("no prior jie term in supported range")
    return candidates[-1]


def next_jie(date_value: dt.date) -> tuple[str, dt.date]:
    candidates = [item for item in jie_dates_around(date_value.year) if item[1] > date_value]
    if not candidates:
        raise ValueError("no next jie term in supported range")
    return candidates[0]


def previous_jie(date_value: dt.date) -> tuple[str, dt.date]:
    return active_jie(date_value)


def year_pillar(date_value: dt.date) -> Pillar:
    lichun = term_date(date_value.year, "立春")
    year = date_value.year if date_value >= lichun else date_value.year - 1
    return ganzhi(year - 1984)


def month_pillar(date_value: dt.date, year_stem: str) -> tuple[Pillar, str, dt.date]:
    term_name, term_at = active_jie(date_value)
    branch = MONTH_BRANCH_BY_TERM[term_name]
    first_stem = FIRST_MONTH_STEM_BY_YEAR_STEM[year_stem]
    offset = (BRANCHES.index(branch) - BRANCHES.index("寅")) % 12
    stem = STEMS[(STEMS.index(first_stem) + offset) % 10]
    return Pillar(stem, branch), term_name, term_at


def hour_branch(hour: int, minute: int) -> str:
    if hour == 23 or hour == 0:
        return "子"
    branch_index = ((hour + 1) // 2) % 12
    return BRANCHES[branch_index]


def hour_pillar(time_value: tuple[int, int] | None, day_stem: str) -> Pillar | None:
    if time_value is None:
        return None
    branch = hour_branch(*time_value)
    first_stem = FIRST_HOUR_STEM_BY_DAY_STEM[day_stem]
    offset = BRANCHES.index(branch)
    stem = STEMS[(STEMS.index(first_stem) + offset) % 10]
    return Pillar(stem, branch)


def ten_god(day_stem: str, other_stem: str) -> str:
    day_el = ELEMENT[day_stem]
    other_el = ELEMENT[other_stem]
    same_polarity = POLARITY[day_stem] == POLARITY[other_stem]
    generates = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    controls = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
    if other_el == day_el:
        return "比肩" if same_polarity else "劫财"
    if generates[other_el] == day_el:
        return "偏印" if same_polarity else "正印"
    if generates[day_el] == other_el:
        return "食神" if same_polarity else "伤官"
    if controls[other_el] == day_el:
        return "七杀" if same_polarity else "正官"
    if controls[day_el] == other_el:
        return "偏财" if same_polarity else "正财"
    raise ValueError("unreachable ten-god relation")


def dayun_direction(year_stem: str, sex: str) -> str:
    yang_year = POLARITY[year_stem] == "阳"
    male = sex.lower() in {"male", "m", "男"}
    female = sex.lower() in {"female", "f", "女"}
    if not (male or female):
        raise ValueError("sex must be male/female or 男/女")
    return "forward" if (yang_year and male) or ((not yang_year) and female) else "backward"


def dayun_start_age(date_value: dt.date, direction: str) -> dict[str, Any]:
    if direction == "forward":
        name, boundary = next_jie(date_value)
        days = (boundary - date_value).days
    else:
        name, boundary = previous_jie(date_value)
        days = (date_value - boundary).days
    years = days / 3.0
    whole_years = int(years)
    months = round((years - whole_years) * 12)
    if months == 12:
        whole_years += 1
        months = 0
    return {
        "boundary_term": name,
        "boundary_date": boundary.isoformat(),
        "days": days,
        "approx_years": round(years, 2),
        "years": whole_years,
        "months": months,
    }


def dayun_list(month: Pillar, direction: str, start_years: int, count: int = 8) -> list[dict[str, Any]]:
    start_index = ganzhi_index(month.stem, month.branch)
    step = 1 if direction == "forward" else -1
    rows = []
    for i in range(1, count + 1):
        pillar = ganzhi(start_index + step * i)
        age_start = start_years + (i - 1) * 10
        rows.append({
            "index": i,
            "age_range": f"{age_start}-{age_start + 9}",
            "pillar": pillar.text,
        })
    return rows


def pillar_payload(pillar: Pillar | None, day_stem: str | None = None, *, is_day: bool = False) -> dict[str, Any] | None:
    if pillar is None:
        return None
    hidden = HIDDEN_STEMS[pillar.branch]
    payload: dict[str, Any] = {
        "pillar": pillar.text,
        "stem": pillar.stem,
        "branch": pillar.branch,
        "hidden_stems": hidden,
    }
    if day_stem is not None:
        payload["ten_god"] = "日主" if is_day else ten_god(day_stem, pillar.stem)
        payload["hidden_stem_ten_gods"] = [
            {"stem": stem, "ten_god": ten_god(day_stem, stem)} for stem in hidden
        ]
    return payload


def calculate(date_text: str, time_text: str, sex: str) -> dict[str, Any]:
    birth_date = dt.date.fromisoformat(date_text)
    parsed_time = parse_birth_time(time_text)
    warnings: list[str] = []

    if not (1900 <= birth_date.year <= 2100):
        raise ValueError("supported Gregorian year range is 1900-2100")

    day_date = birth_date
    if parsed_time and parsed_time[0] == 23:
        day_date = birth_date + dt.timedelta(days=1)
        warnings.append("23:00-23:59 is treated as late Zi hour and uses the next day pillar.")

    yp = year_pillar(birth_date)
    mp, active_term, active_term_date = month_pillar(birth_date, yp.stem)
    dp = sexagenary_day(day_date)
    hp = hour_pillar(parsed_time, dp.stem)

    for term_name, term_at in jie_dates_around(birth_date.year):
        delta = abs((birth_date - term_at).days)
        if delta <= 1:
            warnings.append(
                f"Birth date is within {delta} day(s) of {term_name} ({term_at}); verify pillars with a high-precision calendar."
            )

    direction = dayun_direction(yp.stem, sex)
    start = dayun_start_age(birth_date, direction)
    dayun = dayun_list(mp, direction, start["years"])

    return {
        "input": {"date": birth_date.isoformat(), "time": time_text, "sex": sex},
        "convention": {
            "calendar": "Gregorian date with solar-term month/year boundaries",
            "late_zi": "23:00-23:59 uses next day pillar",
            "solar_terms": "compact 1900-2100 approximation; verify boundary dates",
        },
        "active_jie": {"name": active_term, "date": active_term_date.isoformat()},
        "pillars": {
            "year": pillar_payload(yp, dp.stem),
            "month": pillar_payload(mp, dp.stem),
            "day": pillar_payload(dp, dp.stem, is_day=True),
            "hour": pillar_payload(hp, dp.stem),
        },
        "day_master": {"stem": dp.stem, "element": ELEMENT[dp.stem], "polarity": POLARITY[dp.stem]},
        "dayun": {
            "direction": direction,
            "start_age": start,
            "cycles": dayun,
        },
        "warnings": warnings,
    }


def render_text(result: dict[str, Any]) -> str:
    pillars = result["pillars"]
    hour = pillars["hour"]["pillar"] if pillars["hour"] else "未知"
    lines = [
        "Bazi calculation",
        f"- Input: {result['input']['date']} {result['input']['time']} sex={result['input']['sex']}",
        f"- Active jie: {result['active_jie']['name']} ({result['active_jie']['date']})",
        f"- Four pillars: {pillars['year']['pillar']} / {pillars['month']['pillar']} / {pillars['day']['pillar']} / {hour}",
        f"- Day master: {result['day_master']['stem']} ({result['day_master']['polarity']}{result['day_master']['element']})",
        f"- Dayun direction: {result['dayun']['direction']}",
        (
            "- Dayun start: approx "
            f"{result['dayun']['start_age']['approx_years']} years "
            f"({result['dayun']['start_age']['years']}y {result['dayun']['start_age']['months']}m), "
            f"boundary={result['dayun']['start_age']['boundary_term']} "
            f"{result['dayun']['start_age']['boundary_date']}"
        ),
        "- Dayun cycles:",
    ]
    for row in result["dayun"]["cycles"]:
        lines.append(f"  {row['index']}. age {row['age_range']}: {row['pillar']}")
    if result["warnings"]:
        lines.append("- Warnings:")
        for warning in result["warnings"]:
            lines.append(f"  * {warning}")
    return "\n".join(lines)


def self_test() -> None:
    result = calculate("2000-01-01", "12:00", "male")
    assert result["pillars"]["day"]["pillar"] == "戊午"
    assert result["pillars"]["hour"]["pillar"] == "戊午"
    result2 = calculate("1984-02-05", "00:30", "male")
    assert result2["pillars"]["year"]["pillar"] == "甲子"
    result3 = calculate("1984-02-04", "12:00", "male")
    assert result3["pillars"]["year"]["pillar"] in {"癸亥", "甲子"}
    print("self-test passed")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate a compact Bazi chart.")
    parser.add_argument("--date", help="Gregorian birth date, YYYY-MM-DD")
    parser.add_argument("--time", default="unknown", help="Birth time HH:MM or unknown")
    parser.add_argument("--sex", default="male", help="male/female or 男/女")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--self-test", action="store_true", help="Run built-in smoke tests")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0
    if not args.date:
        parser.error("--date is required unless --self-test is used")

    result = calculate(args.date, args.time, args.sex)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
