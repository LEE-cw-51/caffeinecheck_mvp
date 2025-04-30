import json
import os
from datetime import date

def handle_remove_record(payload):
    today = date.today().isoformat()
    filename = f"records_{today}.json"

    data = load_json(filename)
    if not data:
        return {"error": "오늘의 기록이 없습니다."}, 404

    target_drink = payload.get("drink")
    if not target_drink:
        return {"error": "삭제할 음료 이름을 입력하세요."}, 400

    new_records = []
    removed_caffeine = 0
    found = False

    for record in data["records"]:
        if record["drink"] == target_drink and not found:
            removed_caffeine = record["caffeine"]
            found = True
            continue
        new_records.append(record)

    if not found:
        return {"error": f"{target_drink} 기록이 없습니다."}, 404

    data["records"] = new_records
    data["daily_caffeine"] -= removed_caffeine
    save_json(filename, data)

    return {
        "message": f"{target_drink} 삭제 완료",
        "updated_total": data["daily_caffeine"]
    }, 200

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
