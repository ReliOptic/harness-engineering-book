# /outline [chNN]

해당 챕터의 section outline을 생성한다.

## 실행 단계 (조건부 읽기)

1. `chapter-map.md`에서 해당 챕터 항목만 읽는다 (파일 전체 X).
2. `writing-plan.md`에서 해당 챕터의 "핵심 구성" 섹션만 읽는다.
3. `deep-research/README.md`에서 챕터 배정 DR 목록을 확인한다 (목록만 확인, 파일 내용은 읽지 않음).
4. `experiments/scenario-master.md`에서 해당 챕터 실험 ID만 확인한다.
5. Outline을 생성한다 — 각 섹션에 필요한 DR/실험 ID를 명시한다.
   (이 ID가 `/draft` 단계의 최소 읽기 지침이 된다)

**DR/실험 파일 내용은 outline 단계에서 읽지 않는다. `/draft` 단계에서 섹션별로 필요할 때만 읽는다.**

## 출력 형식

각 섹션에 대해:
- 섹션 번호와 제목
- 핵심 메시지 한 문장
- 어떤 재료(DR/실험/사례)를 쓸지
- 예상 분량 (자 단위)
- 5변수 프레임워크 중 어떤 변수를 다루는지

## 승인 후 행동

사용자가 outline을 승인하면 `chapters/chNN-xxx.md` 상단의 outline placeholder에 기록한다.

## 글쓰기 원칙 (항상 적용)

- Voice: builder-operator. 현장의 톤.
- hype 금지: "revolutionary", "game-changing" 사용 안 함.
- 관찰된 것만 서술한다.

## 사용 예시

```
/outline ch01
/outline ch04
```
