from datetime import datetime
from functools import cache
from typing import Final

from pytz import timezone


THOUSAND_SEPARATOR_MAP: Final = {",": ".", ".": ","}
TZ: Final = timezone("America/Caracas")
MONTHS = {
    1: "Ene",
    2: "Feb",
    3: "Mar",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic",
}
WEEKDAYS = {1: "Lun", 2: "Mar", 3: "Mie", 4: "Juv", 5: "Vie", 6: "Sáb", 7: "Dom"}
HOURS = {
    0: "12 AM",
    1: "1 AM",
    2: "2 AM",
    3: "3 AM",
    4: "4 AM",
    5: "5 AM",
    6: "6 AM",
    7: "7 AM",
    8: "8 AM",
    9: "9 AM",
    10: "10 AM",
    11: "11 AM",
    12: "12 PM",
    13: "1 PM",
    14: "2 PM",
    15: "3 PM",
    16: "4 PM",
    17: "5 PM",
    18: "6 PM",
    19: "7 PM",
    20: "8 PM",
    21: "9 PM",
    22: "10 PM",
    23: "11 PM",
}


@cache
def daily(date: datetime) -> str:
    return WEEKDAYS[date.isoweekday()]


@cache
def daily_30(date: datetime) -> str:
    return f"{WEEKDAYS[date.isoweekday()]} {date.day}"


@cache
def monthly(date: datetime) -> str:
    return MONTHS[date.month]


@cache
def hourly(date: datetime) -> str:
    return HOURS[date.hour]


@cache
def full_date(date: datetime) -> str:
    return date.date().isoformat()


CALLS = {
    "daily": daily,
    "daily_30": daily_30,
    "monthly": monthly,
    "hourly": hourly,
    "full_date": full_date,
}
