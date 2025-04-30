import json
import os
from datetime import date

def main():
    today = date.today().isoformat()
    filename = f"data/records_{today}.json"

    if not os.path.exists(filename):
        print("오늘 기록 파일이 없습니다.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    slept = input("어제 잘 주무셨나요? (y/n): ").strip().lower()
    slept_well = (slept == 'y')

    symptoms_list = ["두근거림", "손떨림", "불안감", "소화불량", "없음"]
    for i, s in enumerate(symptoms_list, 1):
        print(f"{i}. {s}")
    selected = input("부작용 번호 입력 (콤마로 구분): ")
    selected_indices = [int(x) for x in selected.split(",")]

    symptoms = [symptoms_list[i - 1] for i in selected_indices if symptoms_list[i - 1] != "없음"]

    daily_limit = 400 if slept_well and not symptoms else 350

    data["slept_well"] = slept_well
    data["symptoms"] = symptoms
    data["daily_limit"] = daily_limit

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"피드백 저장 완료. 권장 섭취량: {daily_limit}mg")

if __name__ == "__main__":
    main()
