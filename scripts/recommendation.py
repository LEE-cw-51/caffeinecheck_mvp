import json
import os
from datetime import datetime, timedelta

def get_recommendation():
    base_path = "data"
    today = datetime.today().date()
    records = []

    for i in range(7):
        day = today - timedelta(days=i)
        filename = f"records_{day.isoformat()}.json"
        path = os.path.join(base_path, filename)

        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 조건: 잠을 잘 잤고, 부작용이 없어야 유효함
        if data.get("slept_well") and not data.get("symptoms"):
            records.append(data.get("daily_caffeine", 0))

    if not records:
        return {"message": "부작용 없는 기록이 없습니다."}, 404

    avg_caffeine = sum(records) / len(records)
    cups = round(avg_caffeine / 120, 1)  # 평균 커피잔 수 계산 (기준: 120mg)

    recommendation = f"하루 {cups}잔 정도가 적절해 보여요."

    return {
        "valid_days": len(records),
        "avg_caffeine": round(avg_caffeine, 1),
        "coffee_per_day": cups,
        "recommendation": recommendation
    }, 200
