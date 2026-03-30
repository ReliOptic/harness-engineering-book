# Ch.11 대화 프롬프트 — Self-Immune System: Harness에서 Agent로

## 프로젝트 컨텍스트

나는 "Harness Engineering and AgentOps"라는 기술서를 집필 중이다. 이 책은 2026년 상반기 agent runtime의 실패를 관찰하고 측정하는 실험서다. 11챕터, 4-Part 구조이며, Part IV(Ch.10~11)는 관찰에서 시스템으로의 진화를 다룬다.

Ch.11은 이 책의 마지막 챕터로, **agent가 외부 harness에 의존하지 않고 스스로 자기 실패를 감지하고 복구하는 self-immune system**의 초기 설계를 제시한다. 이것은 Agent-1(외부 의존) → Agent-2(자기 모니터링) 전환의 핵심이다. Part I의 투자가 여기서 회수된다: Constitutional AI(학습 단계 자기교정)와 Reflexion(task 간 학습)이 self-immune(task 내 실시간 감지)의 학술적 계보가 된다.

**이 대화의 목적**: self-immune system의 설계 가능성과 구조적 한계를 동시에 탐구한다. 특히 "자기 모니터링이 추론 자원을 소비하는 재귀적 구조"의 한계와, 이 한계를 정량화하는 방법이 핵심.

---

## 핵심 자료

1. **Bai et al., Constitutional AI** (Anthropic, 2022)
   - 학습 단계의 자기교정 루프: constitution → self-evaluate → revise
   - Ch.11의 학술적 선조. 그러나 학습이 끝나면 루프도 멈춘다.

2. **Shinn et al., Reflexion** (NeurIPS 2023)
   - Task 간 자기 반성: 실패 → 언어 피드백 → 재시도
   - Ch.11과의 핵심 차이: task 사이의 학습 vs. task 내부의 감지

3. **Delétang et al., Language Modeling Is Compression** (ICLR 2024)
   - Cross-entropy as bit cost
   - Self-monitoring의 추론 비용을 정보이론으로 정량화하는 렌즈

4. **이 책의 실험 결과 (Ch.8~9)**:
   - E18: harness 내 token 사용 자동 보고 → 정확도와 overhead
   - E19: harness 내 실패 감지 + 자동 재시도 → 자기 복구율
   - E20: E18+E19 결합 → "mini self-immune" 안정성
   - E08: 자기 평가 정확도 붕괴 관찰

5. **이 책의 프레임워크**:
   - 5변수 프레임워크 (Ch.5)
   - 4개 관찰 지표: 도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율 (Ch.6)
   - Failure Budget Reallocation (Ch.7)
   - Operational Compiler (Ch.10)

---

## 10가지 평가 질문

나의 이해도를 평가해 주세요. 이 챕터는 이 책에서 가장 추측적(speculative)인 부분입니다. 내 답변에서 "관찰된 사실"과 "추론"과 "추측"을 엄격히 구분해 주세요.

### 학술적 계보 (Part I 회수)

1. **Constitutional AI → Self-immune**: Constitutional AI의 자기교정 루프(constitution → evaluate → revise)가 런타임에서도 작동한다고 가정해 봅시다. 이때 학습 단계와 런타임 단계에서 각각 어떤 차이가 발생하나요? "constitution"에 해당하는 것이 런타임에서는 무엇인가요?

2. **Reflexion → Self-immune 시간 척도**: Reflexion은 "task A 실패 → 반성 → task A 재시도"입니다. Self-immune은 "task A 실행 중 step 15에서 문제 감지 → 즉시 대응"입니다. 이 시간 척도 차이가 설계에서 어떤 근본적 차이를 만드나요?

3. **Cross-entropy로 self-monitoring 비용 읽기**: Ch.2에서 cross-entropy가 "틀린 모델의 대가"라는 것을 배웠습니다. Self-monitoring을 추가하면 agent가 "자기 상태를 예측"해야 합니다. 이 자기 예측의 cross-entropy(bit cost)를 어떻게 측정할 수 있을까요?

### 재귀적 한계 (핵심 문제)

4. **자기 모니터링의 재귀적 구조**: agent가 자기 상태를 모니터링하려면 추론 자원을 소비합니다. 시스템이 과부하 상태일 때 — 즉, 자기 진단이 가장 필요한 바로 그 순간에 — 자기 진단 기능도 신뢰성을 잃습니다. 이 재귀적 구조를 어떻게 정식화할 수 있나요?

5. **Cliff-proximity 감지**: 4개 관찰 지표(도구 정확도, IFR, reasoning depth, context 효율) 각각에 대해 "cliff에 얼마나 가까운가"를 실시간으로 감지하려면 어떤 신호를 봐야 하나요? 각 지표별로 "cliff 접근 경고 신호"를 설계해 보세요.

6. **Self-monitoring의 overhead budget**: Self-monitoring이 전체 token budget의 몇 %를 소비하면 "비용 > 이득"이 되나요? Ch.7의 HOR(Harness Overhead Ratio) 개념을 self-monitoring에 적용하면 "Self-monitoring Overhead Ratio"를 정의할 수 있나요?

### 전환 조건과 설계

7. **Agent-1 → Agent-2 전환 조건**: 어떤 조건이 충족되면 외부 harness 의존(Agent-1)에서 자기 모니터링(Agent-2)으로 전환할 수 있나요? 이 전환이 "harness를 제거하는 것"이 아니라 "harness를 agent 내부로 이동시키는 것"이라면, 구체적으로 무엇이 이동하나요?

8. **Temporal stability**: Self-immune이 작동하기 시작한 후, 시간이 지나면 자기 모니터링의 정확도가 어떻게 변하나요? 안정적으로 유지되나요, 아니면 점진적으로 감소하나요? 감소한다면 그 메커니즘은 무엇인가요?

### 열린 질문들

9. **Self-immune의 구조적 불가능성 조건**: 어떤 조건에서 self-immune은 원천적으로 불가능한가요? "자기 모니터링으로는 감지할 수 없는 실패 유형"이 있다면 그것은 무엇인가요?

10. **이 책 이후의 질문**: Ch.11이 닫아야 하는 것은 "결론"이 아니라 "미해결 질문"입니다. Self-immune 설계를 시도한 뒤 남는 가장 중요한 3개의 열린 질문을 제안해 보세요. 이 질문들이 왜 이 책의 범위 안에서는 답할 수 없는지도 설명해 보세요.

---

## 대화 종료 시 요청사항

모든 질문이 끝나면 다음을 생성해 주세요:

1. **이해도 프로필**: 내가 강한 영역과 약한 영역의 요약. 특히 "관찰"과 "추측"을 내가 잘 구분했는지 평가.
2. **Part I 회수 지도**: Constitutional AI, Reflexion, cross-entropy가 각각 Ch.11의 어떤 논점에서 소환되었는지, 그리고 "같은 계보이지만 다른 메커니즘"이라는 구분이 명확했는지 정리
3. **재귀적 한계 정식화**: 질문 4~6에서 도출된 자기 모니터링의 재귀적 구조와 overhead budget을 Ch.11 §4 초안 재료로 정리
4. **전환 조건 정식화**: 질문 7~8의 답변을 Ch.11 §7 "Agent-1→Agent-2 전환 조건" 섹션에 직접 사용할 수 있는 형태로 정리
5. **열린 질문 목록**: 질문 9~10에서 도출된 미해결 질문을 Ch.11 §8 "이 책 이후"에 배치할 수 있는 형태로 정리. 각 질문에 "왜 이 책에서 답할 수 없는가"를 한 문장으로 첨부.

결과 파일을 `dialogue/ch11-self-immune/` 폴더에 저장해 주세요.
