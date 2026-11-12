import json
import os
from pathlib import Path

import pymysql

connection = pymysql.connect(
    host=os.environ["DB_HOST"],
    port=int(os.environ.get("DB_PORT", "3306")),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    ssl_verify_cert=True,
    ssl_verify_identity=True,
)

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                name,
                steam,
                score,
                kills,
                deaths,
                headshots
            FROM rankme
            ORDER BY score DESC, kills DESC
        """)
        players = cursor.fetchall()
finally:
    connection.close()

for player in players:
    for key in ("score", "kills", "deaths", "headshots"):
        player[key] = int(player[key] or 0)

output = Path("data/rankings.json")
output.parent.mkdir(parents=True, exist_ok=True)

output.write_text(
    json.dumps(players, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Exported {len(players)} players.")

