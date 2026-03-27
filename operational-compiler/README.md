# Operational Compiler

> 반복 실패와 intervention rule을 운영 규칙으로 컴파일하는 구조. Dog food 결과물.
> 한 번에 harness에 embedding하는 것이 아니다.
> Lesson learned를 통해 점진적으로 발전시킨다.

---

## 설계 원칙

1. **관찰 먼저**: 실험에서 반복적으로 나타나는 실패 패턴을 먼저 관찰한다.
2. **점진적 컴파일**: 한 번에 완성하지 않는다. 하나씩 추가한다.
3. **CLI 우선**: 현재는 CLI 유틸리티 레이어로 구체화한다.
4. **업데이트 가능**: CLI만 업데이트하면 self-immune 능력이 향상된다.

---

## 현재 상태

실험(E01~E22) 완료 후 반복 실패 패턴을 분석하여 컴파일 후보를 선정한다.

Phase 4(실험) → Phase 5(분석) → Phase 6(Operational Compiler 설계) 순서로 진행.

---

## 관련 파일

- `design-notes.md` — 설계 의사결정 기록
- `failure-to-tool-map.md` — 실패 패턴 → 규칙 후보 매핑
- `src/` — 구현 코드 (Phase 6 이후)
- `tests/` — 테스트
- `examples/` — 사용 예시
