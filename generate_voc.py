import swisseph as swe
import json
from datetime import datetime, timedelta, timezone

swe.set_ephe_path(".")

PLANETS = [
    swe.SUN,
    swe.MERCURY,
    swe.VENUS,
    swe.MARS,
    swe.JUPITER,
    swe.SATURN,
    swe.URANUS,
    swe.NEPTUNE,
    swe.PLUTO
]

ASPECTS = [0, 60, 90, 120, 180]


def jd(dt):
    return swe.julday(dt.year, dt.month, dt.day,
                      dt.hour + dt.minute / 60.0)


def moon_lon(jd_):
    return swe.calc_ut(jd_, swe.MOON)[0][0]


def planet_lon(jd_, p):
    return swe.calc_ut(jd_, p)[0][0]


def aspect(a, b):
    diff = abs((a - b) % 360)
    return any(abs(diff - x) < 0.8 for x in ASPECTS)


def moon_sign(lon):
    return int(lon // 30)


def next_sign_change(dt):
    current = moon_sign(moon_lon(jd(dt)))

    t = dt

    for _ in range(2000):
        t += timedelta(minutes=5)
        if moon_sign(moon_lon(jd(t))) != current:
            return t

    return None


def last_aspect(dt, end_dt):

    t = dt

    while t < end_dt:

        j = jd(t)
        m = moon_lon(j)

        for p in PLANETS:
            pl = planet_lon(j, p)

            if aspect(m, pl):
                return t

        t += timedelta(minutes=5)

    return None


def get_voc(dt):

    sign_end = next_sign_change(dt)

    if not sign_end:
        return None

    start = last_aspect(dt, sign_end)

    if not start:
        start = dt

    return {
        "inicio": start.isoformat(),
        "fim": sign_end.isoformat()
    }


# -----------------------------
# GERA 7 DIAS
# -----------------------------
now = datetime.now(timezone.utc)

results = []

for i in range(7 * 24 * 6):  # 10 min steps

    dt = now + timedelta(minutes=i * 10)

    window = get_voc(dt)

    if window:
        if not results or results[-1]["fim"] != window["fim"]:
            results.append(window)


# -----------------------------
# SALVA CACHE
# -----------------------------
with open("voc_cache.json", "w") as f:
    json.dump({
        "timezone": "UTC",
        "voc": results
    }, f, indent=2)
