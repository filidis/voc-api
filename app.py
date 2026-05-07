from flask import Flask, jsonify
import swisseph as swe
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# Swiss Ephemeris setup
swe.set_ephe_path(".")

PLANETS = [
    swe.SUN,
    swe.MERCURY,
    swe.VENUS,
    swe.MARS,
    swe.JUPITER,
    swe.SATURN
]

ASPECTS = [0, 60, 90, 120, 180]


def julian_day(dt):
    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0
    )


def planet_lon(jd, planet):
    return swe.calc_ut(jd, planet)[0][0]


def is_aspect(a, b):
    diff = abs(a - b) % 360
    return any(abs(diff - asp) < 1.5 for asp in ASPECTS)


def moon_lon(jd):
    return swe.calc_ut(jd, swe.MOON)[0][0]


def is_voc(jd):
    m = moon_lon(jd)

    for p in PLANETS:
        pl = planet_lon(jd, p)
        if is_aspect(m, pl):
            return False

    return True


@app.route("/voc")
def voc():

    now = datetime.now(timezone.utc)

    results = []

    step_minutes = 10  # resolução (quanto menor, mais preciso)

    step = timedelta(minutes=step_minutes)

    prev = None
    start = None

    for i in range(7 * 24 * (60 // step_minutes)):

        dt = now + i * step
        jd = julian_day(dt)

        voc = is_voc(jd)

        if voc and not prev:
            start = dt

        if not voc and prev and start:
            results.append({
                "inicio": start.isoformat(),
                "fim": dt.isoformat()
            })
            start = None

        prev = voc

    return jsonify({
        "timezone": "UTC",
        "voc": results
    })


@app.route("/")
def home():
    return jsonify({"status": "ok"})
    

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
