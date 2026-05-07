from flask import Flask, jsonify
import swisseph as swe
from datetime import datetime, timedelta, timezone
import os

app = Flask(__name__)

swe.set_ephe_path(".")

# Planetas usados (padrão Astro.com)
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


# -------------------------
# BASE ASTRONÔMICA
# -------------------------

def jd(dt):
    return swe.julday(dt.year, dt.month, dt.day,
                      dt.hour + dt.minute / 60.0)


def moon_lon(jd):
    return swe.calc_ut(jd, swe.MOON)[0][0]


def planet_lon(jd, p):
    return swe.calc_ut(jd, p)[0][0]


def aspect(a, b):
    diff = abs((a - b) % 360)
    return any(abs(diff - x) < 0.8 for x in ASPECTS)


# -------------------------
# SIGNO
# -------------------------

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


# -------------------------
# ÚLTIMO ASPECTO ANTES DO SIGNO
# -------------------------

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


# -------------------------
# VOC REAL
# -------------------------

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


# -------------------------
# API
# -------------------------

@app.route("/")
def home():
    return jsonify({"status": "ok"})


@app.route("/voc")
def voc():

    now = datetime.now(timezone.utc)

    results = []

    for i in range(7 * 24 * 6):  # 10 min step

        dt = now + timedelta(minutes=i * 10)

        window = get_voc(dt)

        if window:

            if not results or results[-1]["fim"] != window["fim"]:
                results.append(window)

    return jsonify({
        "timezone": "UTC",
        "voc": results
    })


# -------------------------
# RENDER ENTRY POINT
# -------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
