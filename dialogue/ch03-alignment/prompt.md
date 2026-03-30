# Ch.3 대화 프롬프트 — 정렬에서 자율로: 모델은 어떻게 행동을 배우는가

## 프로젝트 컨텍스트

나는 "Harness Engineering and AgentOps"라는 기술서를 집필 중이다. 이 책은 2026년 상반기 agent runtime의 실패를 관찰하고 측정하는 실험서다. 11챕터, 4-Part 구조이며, Part I(Ch.1~4)은 agent를 만든 역사적 논문들을 기반으로 agent runtime 실패의 기술적 기원을 추적한다.

Ch.3은 모델이 "좋은 행동"을 학습하는 과정(RLHF, RLAIF, Constitutional AI)을 추적한 뒤, **학습 단계의 정렬이 왜 런타임 문제를 풀 수 없는지**를 구조적으로 논증한다. 이 gap이 바로 harness가 필요한 이유이며, Part II(Ch.7)와 Part IV(Ch.11 self-immune)의 직접적 전제가 된다.

**이 대화의 목적**: 아래 논문들을 내가 이해하는 과정에서 "학습이 풀 수 있는 것"과 "학습이 풀 수 없는 것"의 경계를 명확히 구분하는 통찰을 얻는다. 이 경계 분석이 Ch.3 §4의 핵심 논증이 된다.

---

## 핵심 논문과 자료

1. **Ouyang et al., "Training Language Models to Follow Instructions with Human Feedback" (InstructGPT)** (NeurIPS 2022, ~18,000 citations)
   - SFT → Reward Model → PPO 3단계 파이프라인
   - 인간 피드백으로 모델 행동을 정렬하는 최초의 체계적 방법론
   - https://arxiv.org/abs/2203.02155

2. **Lee et al., "RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback"** (2023)
   - 인간 대신 AI가 선호도를 생성하여 RLHF를 스케일링
   - RLAIF ≈ RLHF 성능이라는 실험 결과
   - https://arxiv.org/abs/2309.00267

3. **Bai et al., "Constitutional AI: Harmlessness from AI Feedback"** (Anthropic 2022, ~3,000 citations)
   - 모델이 헌법(원칙 목록)에 따라 자기 출력을 평가하고 수정하는 자기교정 루프
   - 학습 단계에서의 self-critique
   - https://arxiv.org/abs/2212.08073

4. **참고 자료**:
   - DPO (Direct Preference Optimization) — Rafailov et al., 2023
   - KTO (Kahneman-Tversky Optimization) — Ethayarajh et al., 2024

---

## 10가지 평가 질문

나의 이해도를 평가해 주세요. 각 질문에 대해 내가 답하면, 정확한 부분과 빈틈을 짚어주고, 빈틈이 있으면 보충 설명 후 다음 질문으로 넘어가 주세요. 모든 질문이 끝나면, 내 답변 과정에서 드러난 이해 패턴을 종합하여 Ch.3 집필에 활용할 수 있는 insight summary를 만들어 주세요.

### 기초 이해 (논문 내용)

1. **SFT의 역할과 한계**: Supervised Fine-Tuning이 모델 행동을 어떻게 바꾸는지, 그리고 SFT만으로 충분하지 않은 이유를 설명해 보세요. "평균적으로 좋은 답"과 "특정 상황에서 정확히 맞는 답"의 차이가 여기서 왜 중요한가요?

2. **Reward Model**: 인간 선호도 데이터로 reward model을 학습시키는 과정을 설명해 보세요. reward model이 "좋음"을 점수화할 때, 어떤 종류의 "좋음"은 잘 포착하고 어떤 종류는 놓치나요?

3. **PPO와 정렬**: PPO가 reward model의 점수를 최대화하도록 정책을 업데이트하는 과정에서, reward hacking이 발생하는 메커니즘을 설명해 보세요. KL penalty는 이것을 어떻게 완화하나요?

4. **RLAIF의 핵심 발견**: 인간 대신 AI가 선호도를 매기는 것이 왜 비슷한 성능을 낼 수 있는지 설명해 보세요. 이것이 정렬의 비용 구조를 어떻게 바꾸나요?

5. **Constitutional AI의 자기교정 루프**: 헌법(constitution)이란 무엇이며, 모델이 자기 출력을 헌법에 비추어 평가하고 수정하는 과정을 단계별로 설명해 보세요.

### 심화 이해 (경계 분석)

6. **학습이 풀 수 있는 것 vs. 없는 것**: RLHF/RLAIF로 개선할 수 있는 모델 행동의 범위와, 아무리 학습해도 개선할 수 없는 런타임 행동의 범위를 구분해 보세요. 예를 들어, "평균 응답 품질 향상"은 학습이 풀 수 있지만, "40-step task에서 step 37의 instruction following rate 유지"는 왜 학습으로 풀 수 없나요?

7. **Constitutional AI와 Self-immune의 차이**: Constitutional AI의 자기교정은 학습이 끝나면 멈춥니다. 만약 이 자기교정이 런타임에도 계속 작동한다면 어떤 일이 벌어질까요? 어떤 새로운 문제가 생기나요? (힌트: 자기 모니터링 자체가 추론 자원을 소비합니다)

8. **DPO의 등장이 의미하는 것**: DPO가 reward model 없이 직접 선호도를 최적화하는 것이, 정렬 연구의 방향에 대해 무엇을 시사하나요? reward model이라는 중간 단계를 제거하는 것의 장단점은?

### 운영 번역 (Agent Runtime 연결)

9. **Instruction Following Rate Decay**: aligned model이 짧은 대화에서는 지시를 잘 따르지만, 장기 실행에서 점진적으로 지시를 무시하게 되는 현상을 관찰합니다. RLHF의 학습 구조(짧은 비교 쌍 기반)가 이 decay를 왜 방지하지 못하는지 설명해 보세요.

10. **학습-런타임 경계가 Harness를 요구하는 이유**: 지금까지 논의한 모든 정렬 방법(SFT, RLHF, RLAIF, Constitutional AI)이 공통적으로 풀지 못하는 런타임 문제들을 종합해 보세요. 그리고 이 gap을 메우기 위해 "학습 바깥에서 작동하는 무언가"가 필요하다면, 그것은 어떤 속성을 가져야 하는지 추론해 보세요.

---

## 대화 종료 시 요청사항

모든 질문이 끝나면 다음을 생성해 주세요:

1. **이해도 프로필**: 내가 강한 영역과 약한 영역의 요약
2. **학습-런타임 경계 지도**: 대화에서 도출된 "학습이 풀 수 있는 것 / 풀 수 없는 것 / 경계가 모호한 것"의 3분류 표
3. **운영 번역 원료**: 질문 9~10의 답변을 정제하여 Ch.3 §4 "학습 정렬이 Runtime 문제를 풀지 못하는 구조적 이유" 섹션의 초안 재료
4. **Ch.7/Ch.11 연결 씨앗**: 대화에서 나온 "harness가 가져야 할 속성"과 "self-immune과 Constitutional AI의 차이"를 정리하여 이후 챕터 집필의 연결고리로 사용할 수 있는 핵심 논점

결과 파일을 `dialogue/ch03-alignment/` 폴더에 저장해 주세요.
