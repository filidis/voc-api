import json
from datetime import datetime, timedelta, timezone
import swisseph as swe

swe.set_ephe_path(".")

def generate_mock_voc():
    now = datetime.now(timezone.utc)

    # aqui entra sua lógica real (Swiss Ephemeris)
    return {
        "timezone": "UTC",
        "voc": [
            {
                "inicio": (now + timedelta(hours=2)).isoformat(),
                "fim": (now + timedelta(hours=6)).isoformat()
            }
        ]
    }


data = generate_mock_voc()

with open("voc_cache.json", "w") as f:
    json.dump(data, f, indent=2)
