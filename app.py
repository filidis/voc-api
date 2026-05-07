from flask import Flask, jsonify
import swisseph as swe
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# caminho das efemérides (Render usa local)
swe.set_ephe_path(".")

PLANETS = [
    swe.SUN,
    swe.MOON,
    swe.MERCURY,
    swe.VENUS,
    swe.MARS,
    swe.JUPITER,
    swe.SATURN
]

ASPECTS = [0, 60, 90, 120, 180]

def jd(dt):
    return swe.julday(dt.year, dt.month, dt.day,
                      dt.hour + dt.minute/60.0)

def lon(body, t):
    return swe.calc_ut(t, body)[0][0]

def aspect(a, b):
    diff = abs(a - b) % 360
    return any(abs(diff - x) < 1.5 for x in ASPECTS)

def is_voc(t):
    m = lon(swe.MOON, t)
    for p in PLANETS:
        if p != swe.MOON:
            if aspect(m, lon(p, t)):
                return False
    return True

@app.route("/voc")
def voc():

    now = datetime.now(timezone.utc)

    results = []

    step = timedelta(minutes=15)

    start = None
    prev = False

    for i in range(7 * 24 * 4):  # 15 min steps

        dt = now + i * step
        t = jd(dt)

        voc = is_voc(t)

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

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
