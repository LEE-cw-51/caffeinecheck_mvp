import json
from datetime import date

def main():
    print("=== Caffeine Check: 섭취 기록 ===")

    caffeine_db = {
        "스타벅스 아메리카노": {"base_caffeine": 150, "base_shots": 2},
        "캔커피": {"base_caffeine": 100, "base_shots": None},
        "에너지 드링크": {"base_caffeine": 80, "base_shots": None}
    }

    records = []
    daily_caffeine = 0

    while True:
        drink = input("음료 이름 (또는 '종료'): ")
        if drink == '종료':
            break

        if drink in caffeine_db:
            base = caffeine_db[drink]
            caffeine = base["base_caffeine"]

            if base["base_shots"]:
                extra = int(input("추가 샷 수: "))
                caffeine += extra * 75
        else:
            caffeine = int(input("직접 카페인(mg) 입력: "))

        records.append({"drink": drink, "caffeine": caffeine})
        daily_caffeine += caffeine
        print(f"현재 총 카페인: {daily_caffeine}mg")

    today = date.today().isoformat()
    data = {
        "date": today,
        "daily_caffeine": daily_caffeine,
        "records": records
    }

    with open(f"data/records_{today}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
