# /dispatch [url] "[한 줄 설명]"

Field Dispatch를 작성하고 저장한다.

## 실행 단계

1. URL을 fetch하여 핵심 내용을 파악한다.
2. `field-dispatches/index.md`에서 최신 dispatch 번호를 확인하고 다음 번호를 부여한다.
3. Field Dispatch 초안을 작성한다.
4. `field-dispatches/YYYY-MM/` 폴더에 저장한다.
5. `field-dispatches/index.md`를 업데이트한다.

## Dispatch 형식

```markdown
# FD-YYYY-MM-DD-NNN: [한 줄 제목]

**Date:** YYYY-MM-DD
**Reporter:** [팀원 이름]
**Source:** [URL]
**Category:** [카테고리]

## 무슨 일이 일어났는가 (3문장 이내)

[사실만. 의견 없이.]

## 우리 책과 어떻게 연결되는가 (3문장 이내)

[5변수 중 어떤 것과 관련되는지, 어떤 챕터에 영향을 주는지]

## 즉시 행동이 필요한가

- [ ] Deep research 필요 → DR-ID 부여
- [ ] 실험 설계 변경 필요
- [ ] 챕터 내용 수정 필요
- [x] 기록만 해두면 됨

## Tags

`#태그1` `#태그2`
```

## 카테고리
- `NEW_PROJECT`: 새로운 agent 관련 프로젝트
- `MODEL_RELEASE`: 새 모델 출시/업데이트
- `FRAMEWORK_CHANGE`: Agent 프레임워크 주요 변경
- `RESEARCH_PAPER`: 관련 논문/벤치마크
- `INDUSTRY_MOVE`: 투자, 인수, 전략적 발표
- `TOOLING`: Agent 관련 도구 출시/업데이트
- `INCIDENT`: Agent 시스템 주요 실패/사건
- `CONCEPT`: 새로운 개념/용어 부상

## 작성 시간 제한
1건당 5분 이내. Dispatch는 분석이 아니라 기록이다.

## 사용 예시

```
/dispatch https://github.com/666ghj/MiroFish "군집 지능 예측 엔진, GitHub trending 1위"
```
