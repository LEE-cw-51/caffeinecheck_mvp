import json
import os
from datetime import date

def handle_feedback(payload):
    today = date.today().isoformat()
    filename = f"records_{today}.json"

    data = load_json(filename)
    if not data:
        return {"error": "오늘의 기록이 없습니다."}, 404

    slept_well = payload.get("slept_well")
    symptoms = payload.get("symptoms", [])

    if slept_well is None:
        return {"error": "수면 여부(slept_well)를 반드시 포함해야 합니다."}, 400

    data["slept_well"] = slept_well
    data["symptoms"] = symptoms

    # 부작용 있거나 잠을 잘 못 잤으면 권장 카페인 줄이기
    if not slept_well or symptoms:
        limit = max(0, data.get("daily_caffeine", 0) - 50)
    else:
        limit = data.get("daily_caffeine", 0)

    data["daily_limit"] = limit
    save_json(filename, data)

    return {
        "message": "피드백 저장 완료",
        "slept_well": slept_well,
        "symptoms": symptoms,
        "new_limit": limit
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
