# ☕ caffeinecheck_mvp – 개인 맞춤형 카페인 추적 및 권장량 추천 시스템

카페인과 당류의 섭취량을 기록하고,  
수면 상태 및 부작용 피드백을 바탕으로  
**개인에게 적절한 카페인 섭취량을 추천**하는 백엔드 MVP 프로젝트입니다.

---

## 🧩 주요 기능

| 기능 | 설명 |
|------|------|
| ✅ `/add_record` | 음료 섭취 기록 추가 (카페인 자동 계산 or 수동 입력) |
| ✅ `/feedback` | 수면 만족도 + 부작용 기록 입력 |
| ✅ `/get_recommendation` | 최근 7일 데이터를 분석해 적정 커피 잔 수 추천 |
| ✅ `/remove_record` | 기록된 음료 중 하나 삭제 |

---

## 🗂️ 프로젝트 구조
```
caffeinecheck_mvp/ 
├── main_server.py      # Flask 서버 메인 진입점 
├── scripts/            # 기능별 모듈 
│   ├── add_record.py 
│   ├── feedback.py 
│   ├── recommendation.py 
│   └── remove_record.py 
├── data/               # 사용자 기록 저장소 (Git 추적 제외됨) 
└── README.md
```

---

## 🛠️ 기술 스택

- Python 3.x
- Flask (RESTful API)
- JSON (로컬 저장 방식)
- Git & GitHub 버전 관리

---

## 🔍 API 사용 예시 (Postman 기준)

### ▶ `/add_record` [POST]
```json
{
  "drink": "스타벅스 아메리카노",
  "extra_shots": 1
}
```
### ▶ '/feedback' [POST]
```json
{
  "slept_well": false,
  "symptoms": ["불면", "두근거림"]
}
```
### ▶ '/get_recommendation' [GET]
→ 최근 7일 중 부작용 없는 날의 평균 카페인량을 기준으로 적정 섭취 잔 수 추천

### ▶ '/remove_record' [DELETE]
```json
{
  "drink": "캔커피"
}
```

# 🚀 향후 계획
 프론트엔드 앱 연동 (React Native 또는 Flutter)

 Render 또는 Vercel로 서버 배포

 사용자별 개인화 고도화 (기상 시간, 체중, 카페인 민감도 등 반영)
 ## 📎 목적
이 프로젝트는 단순한 기록을 넘어서,
수면과 부작용 데이터를 바탕으로 실제 컨디션을 반영한 카페인 루틴을 만들기 위해 시작되었습니다.

“무조건 400mg까지 괜찮다”는 고정 기준 대신,
사용자 맞춤 권장량을 스스로 학습하도록 돕는 건강한 헬스케어 루틴을 목표로 합니다.

---

# 🧾 다음 할 일

1. VSCode에서 `README.md` 파일 열기  
2. 위 내용 전체 복사해서 붙여넣기  
3. 저장 후 아래 명령 실행:

```bash
git add README.md
git commit -m "📝 README.md 템플릿 적용 및 설명 추가"
git push origin main

