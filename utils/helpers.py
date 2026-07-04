# utils/helpers.py

from datetime import datetime


def percent_change(a, b):

    if a == 0:
        return 0

    return ((b - a) / a) * 100


def clamp(value, minimum, maximum):

    return max(minimum, min(maximum, value))


def round2(value):

    return round(float(value), 2)


def today():

    return datetime.now().strftime("%Y-%m-%d")


def safe_div(a, b):

    if b == 0:
        return 0

    return a / b


def ema_alignment(last):

    return (
        last["EMA20"] >
        last["EMA50"] >
        last["EMA200"]
    )


def bearish_alignment(last):

    return (
        last["EMA20"] <
        last["EMA50"] <
        last["EMA200"]
    )
