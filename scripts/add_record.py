import json
import os
from datetime import date

# 카페인 음료 기본 DB
caffeine_db = {
    "스타벅스 아메리카노": {"base_caffeine": 150, "base_shots": 2},
    "캔커피": {"base_caffeine": 100, "base_shots": None},
    "에너지 드링크": {"base_caffeine": 80, "base_shots": None}
}

def handle_add_record(payload):
    today = date.today().isoformat()
    filename = f"records_{today}.json"

    data = load_json(filename) or {
        "date": today,
        "daily_caffeine": 0,
        "records": []
    }

    drink = payload.get("drink")
    extra_shots = payload.get("extra_shots", 0)
    custom_caffeine = payload.get("caffeine")

    if not drink:
        return {"error": "음료 이름을 입력하세요."}, 400

    # 사전 정의된 음료 처리
    if drink in caffeine_db:
        base = caffeine_db[drink]
        caffeine = base["base_caffeine"]
        if base["base_shots"]:
            caffeine += extra_shots * 75
    else:
        # 사용자 정의 음료 처리
        if custom_caffeine is None:
            return {"error": "직접 입력한 음료는 caffeine 값을 포함해야 합니다."}, 400
        caffeine = custom_caffeine

    data["records"].append({"drink": drink, "caffeine": caffeine})
    data["daily_caffeine"] += caffeine
    save_json(filename, data)

    return {"message": f"{drink} 기록 완료!", "today_total": data["daily_caffeine"]}, 200

def load_json(filename):
    path = os.path.join("data", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_json(filename, data):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
