# Per-Section 집필 워크플로

> 섹션 하나를 완성하는 표준 절차. 모든 챕터에 동일하게 적용된다.

---

## 1단계: 세션 시작

```
/begin chNN [section_N]
```

- 해당 섹션의 outline 블록만 읽는다 (챕터 파일 전체 금지)
- 섹션 outline에 명시된 DR, 실험, 증거 파일만 확인한다
- Specialist(Vera/Felix) 호출 필요 여부를 `specialist-trigger.md`에서 확인한다

---

## 2단계: 초고 작성

```
/draft chNN N
```

**Drafter (Chapter Agent):**
1. 섹션 outline의 재료만 사용한다
2. 명시되지 않은 파일을 추측으로 읽지 않는다
3. Specialist가 필요한 지점에서 멈추고 consultation 요청한다
4. 작성 완료 후 AI 문체 8대 금지 self-check 실행
5. 완성 후 반드시 멈춘다: "섹션 N 완성. 피드백 주시면 N+1로 넘어갑니다."

---

## 3단계: Specialist Consultation (해당 섹션만, 필요 시)

`specialist-trigger.md` 기준 해당 항목 존재 시:

**Vera 호출 (정량 분석):**
- 통계 방법, 지표 설계, Figure 해석 질문을 구체적으로 전달
- Vera consultation 결과를 받아 섹션에 통합
- Vera 결과는 Drafter의 산문에 녹인다 (별도 섹션 추가 금지)

**Felix 호출 (실험 설계):**
- Pre-registration, ground truth, 반례 설계 질문을 구체적으로 전달
- Felix consultation 결과를 받아 섹션에 통합

---

## 4단계: Editor 검토

**Editor Agent:**
- Voice Check (AI 문체 8대 금지)
- 용어 일관성 (glossary.md 기준 21쌍)
- 내러티브 Arc (이전/다음 챕터 handoff 확인)
- 반례 의무 (주장이 있으면 성립하지 않는 조건 명시 여부)
- **판정**: PASS / REVISE / REJECT

---

## 5단계: Kiwon 확인 및 다음 섹션

- **PASS**: Kiwon 최종 확인 후 챕터 파일에 반영. 다음 섹션으로.
- **REVISE**: Drafter에게 수정 지시 → 2단계로 돌아감.
- **REJECT**: Kiwon 개입 필요. 챕터 agent와 Kiwon이 논제 재점검.

---

## 세션 관리

- 섹션 하나 완료마다 Kiwon 피드백 대기
- 10턴 이상 진행 시: `/compact "voice rules, chapter outline, current section progress 유지"`
- 챕터 완료 시: `/clear` 후 다음 챕터를 새 세션에서 시작
- Ch.4, Ch.5는 실험 데이터 완성 여부를 먼저 확인한다

---

## 집필 순서 권고 (2026년 3월 기준)

| 순서 | 챕터 | 이유 |
|------|------|------|
| 1 | **Ch.3** | 전체 용어 기준점. 먼저 확정해야 다른 챕터에서 일관된 용어 사용 가능 |
| 2 | **Ch.1** | Kiwon primary. 용어 확정 후 §6(5변수 소개) 작성 가능 |
| 3 | **Ch.2** | 실험(E01~E03) 완료 후. Vera consultation 포함 |
| 4 | **Ch.4** | 전체 실험 완료 후. §1~§2는 사전 작성 가능 |
| 5 | **Ch.5** | Ch.4 완료 후 |
| 6 | **Ch.6** | Ch.5 ablation 결과 후 |
| 7 | **Ch.7** | §1 v0.2 존재. Ch.5-6 완료 후 나머지 섹션 |
| 8 | **Preface** | 7개 챕터 완성 후 마지막 |
