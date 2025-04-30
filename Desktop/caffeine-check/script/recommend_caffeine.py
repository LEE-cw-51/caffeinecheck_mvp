import json
import os
from datetime import date, timedelta

def main():
    print("=== 7일간 기록 분석 ===")

    today = date.today()
    total_caffeine = 0
    valid_days = 0

    for i in range(1, 8):
        day = today - timedelta(days=i)
        filename = f"data/records_{day.isoformat()}.json"

        if not os.path.exists(filename):
            continue

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("slept_well", True) and not data.get("symptoms"):
            total_caffeine += data["daily_caffeine"]
            valid_days += 1

    if valid_days == 0:
        print("부작용 없는 기록이 없습니다.")
        return

    avg_caffeine = total_caffeine / valid_days
    coffee_per_day = avg_caffeine / 150

    print(f"부작용 없는 날 수: {valid_days}")
    print(f"평균 섭취량: {avg_caffeine:.1f}mg")
    print(f"⇒ 적정 커피 잔 수: 하루 {coffee_per_day:.1f}잔")

    if coffee_per_day < 1:
        print("추천: 하루 1잔 이하 섭취")
    elif coffee_per_day < 2:
        print("추천: 하루 1~2잔 섭취")
    else:
        print("추천: 하루 2잔 이상 섭취 가능 (주의 요망)")

if __name__ == "__main__":
    main()
