# /status

프로젝트 전체 현황을 보고한다.

## 실행 단계

1. `chapters/` 폴더에서 각 챕터 파일을 읽고 상태를 파악한다.
2. `experiments/` 폴더에서 완료된 실험 로그를 확인한다.
3. `deep-research/README.md`에서 DR 현황을 확인한다.
4. `field-dispatches/index.md`에서 dispatch 수를 확인한다.
5. 종합 보고서를 출력한다.

## 출력 형식

```
## 📊 프로젝트 현황 — YYYY-MM-DD

### 챕터 상태
| 챕터 | 상태 | 섹션 |
|------|------|------|
| Ch.1 | skeleton only / outline done / drafting (N/M) / integrated / reviewed | — |
...

### 실험 현황
- 완료: N건 (E01, E05, ...)
- 진행중: N건
- 미시작: N건
- 교차검증 완료: N건

### Deep Research 현황
- 완료: N건 (DR-1.1, ...)
- 미시작: N건

### Field Dispatch
- 총 N건 (이번 달: N건)

### Beta 마감까지 (2026-04-30)
- 남은 기간: N일
- 완료율: N%

### 다음 우선 행동 3가지
1. ...
2. ...
3. ...
```

## 사용 예시

```
/status
```
