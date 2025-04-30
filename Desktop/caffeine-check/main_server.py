from flask import Flask, request, jsonify
import json
import os
from datetime import date, timedelta

app = Flask(__name__)
DATA_FOLDER = "data"  # 기록 파일 저장 위치

# ---------------------
# Helper 함수
# ---------------------
def save_data(filename, data):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ---------------------
# 1. 오늘 섭취 기록 추가
# ---------------------
@app.route('/add_record', methods=['POST'])
def add_record():
    today = date.today().isoformat()
    filename = f"records_{today}.json"
    data = load_data(filename) or {
        "date": today,
        "daily_caffeine": 0,
        "records": []
    }

    record = request.json
    drink = record.get("drink")
    caffeine = record.get("caffeine")

    if not drink or caffeine is None:
        return jsonify({"error": "음료 이름과 카페인량을 모두 입력하세요"}), 400

    data["records"].append({"drink": drink, "caffeine": caffeine})
    data["daily_caffeine"] += caffeine
    save_data(filename, data)

    return jsonify({"message": f"{drink} 기록 완료!", "today_total": data["daily_caffeine"]})

# ---------------------
# 2. 수면 + 부작용 피드백
# ---------------------
@app.route('/feedback', methods=['POST'])
def feedback():
    today = date.today().isoformat()
    filename = f"records_{today}.json"
    data = load_data(filename)

    if not data:
        return jsonify({"error": "오늘 섭취 기록이 없습니다."}), 404

    feedback = request.json
    slept_well = feedback.get("slept_well")
    symptoms = feedback.get("symptoms", [])

    if slept_well is None:
        return jsonify({"error": "수면 여부를 입력하세요"}), 400

    data["slept_well"] = slept_well
    data["symptoms"] = symptoms
    data["daily_limit"] = 400 if slept_well and not symptoms else 350

    save_data(filename, data)

    return jsonify({
        "message": "피드백 저장 완료",
        "slept_well": slept_well,
        "symptoms": symptoms,
        "new_limit": data["daily_limit"]
    })

# ---------------------
# 3. 7일 평균 분석 → 최적 커피 권장량
# ---------------------
@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    today = date.today()
    total_caffeine = 0
    valid_days = 0

    for i in range(1, 8):
        day = today - timedelta(days=i)
        filename = f"records_{day.isoformat()}.json"
        data = load_data(filename)

        if data:
            slept_well = data.get("slept_well", True)
            symptoms = data.get("symptoms", [])
            if slept_well and not symptoms:
                total_caffeine += data["daily_caffeine"]
                valid_days += 1

    if valid_days == 0:
        return jsonify({"message": "부작용 없는 기록이 없습니다."}), 404

    avg_caffeine = total_caffeine / valid_days
    coffee_per_day = avg_caffeine / 150  # 1잔 = 150mg 기준

    if coffee_per_day < 1:
        recommendation = "하루 1잔 이하 추천"
    elif coffee_per_day < 2:
        recommendation = "하루 1~2잔 추천"
    else:
        recommendation = "하루 2잔 이상도 가능 (주의 필요)"

    return jsonify({
        "valid_days": valid_days,
        "avg_caffeine": round(avg_caffeine, 1),
        "coffee_per_day": round(coffee_per_day, 1),
        "recommendation": recommendation
    })

# ---------------------
# 서버 실행
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)
