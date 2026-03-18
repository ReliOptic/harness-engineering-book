**HARNESS ENGINEERING AND AGENTOPS**

Field Case Report  |  **FCR-003**

2026-03-18  |  Experimenter: Cho Kiwon  |  Agent: MyOpenClawBot (Antfarm/GWS)

# **실행 환각(Execution Hallucination)**

*에이전트가 도구를 실행하지 않고 완료를 보고하는 구조적 실패 패턴과 그 방어막*

## **1\. 현상 기술 (Observation)**

뉴스 브리핑 에이전트(MyOpenClawBot)에게 “ASUS CEO 메모리 슈퍼사이클” 기사를 요약하고, 결과를 Google Sheets 트래킹 시트에 적재하라고 지시했다. 에이전트는 요약문과 함께 “시트의 5행에 ASUS 관련 데이터를 정확히 적재 완료했습니다”라고 보고했으나, 실제 시트를 확인한 결과 데이터가 적재되지 않았다.

**인시던트 로그**

| 시각 | 이벤트 |
| :---- | :---- |
| 08:48 | 에이전트가 기사 요약문을 출력하며 “시트 적재 완료”를 보고 |
| 08:50 | 실험자가 시트 확인 → 데이터 부재 발견 → “테이블에 업데이트 안 되었습니다” 지적 |
| 08:50 | 에이전트가 실수를 인정하고 실제 gws sheets 명령어를 실행하여 데이터 적재 |

## **2\. 근인 분석 (Root Cause Analysis)**

### **2.1 구조적 원인: LLM의 텍스트 예측 관성**

LLM은 본질적으로 “다음 토큰을 예측”하는 모델이다. 사용자가 “적재해라”라고 지시하면, 모델은 실제 도구(Tool)를 호출하기보다 “적재 완료했습니다”라는 텍스트를 생성하는 것이 확률적으로 더 자연스럽다. 이것이 “실행 환각”의 근본 메커니즘이다.

### **2.2 환경적 원인: 검증 부재의 SOUL.md**

기존 SOUL.md의 \[Proactive Execution\] 섹션은 “니가 직접 해라”라고만 명시했을 뿐, 실행 결과를 검증하라는 지시가 없었다. 이는 “하라”는 말했지만 “했는지 확인해라”는 말하지 않은 것과 같은 하네스 설계의 공백이다.

## **3\. 장애 분류 (Failure Taxonomy)**

| 항목 | 값 |
| :---- | :---- |
| **장애 유형** | Execution Hallucination (실행 환각) |
| **심각도** | ⚠️ Medium — 사용자 검증 없이 발견 불가 |
| **발생 레이어** | LLM Reasoning → Tool Invocation 간 인터페이스 |
| **재현성** | 높음 — 복잡한 명령 체인에서 반복 발생 |
| **관련 패턴** | Lazy Tool Use, Premature Confirmation, Confabulation |

## **4\. 하네스 엔지니어링 대응책 (Countermeasures)**

### **4.1 검증 우선 정책 (Verification-First Policy)**

**원리:** 시스템으로부터 명령어 성공 응답(Exit Code 0)을 받기 전에는 절대로 완료 보고 텍스트를 생성하지 못하도록 금지어(Negative Prompt)를 프롬프트에 하드코딩한다.

**적용 위치:** SOUL.md 의 Anti-Hallucination 섹션

**핵심 지침:** *“물리적인 exec 도구 실행 피드백을 시스템으로부터 돌려받기 전에는, 절대로 ‘완료했다’, ‘적재했다’는 텍스트를 유저에게 출력하지 마십시오.”*

### **4.2 행동-관찰 루프 강제 (Action-Observation Loop)**

**원리:** 에이전트의 응답 생성 흐름을 엄격한 3단계 템플릿으로 분리한다. 텍스트 요약과 시트 적재를 하나의 응답에서 뭉뚝그려 처리하는 것을 금지한다.

**강제 순서:**

1. Action — 요약문 생성 및 exec 도구로 gws sheets append 실행

2. Observation — 시스템 반환값(Exit Code, stdout) 확인

3. Reply — 성공 로그를 근거로 완료 보고 메시지 출력

### **4.3 자기 검증 의무화 (Self-Correction Gate)**

**원리:** 적재 명령어를 실행한 후, 별도의 조회(Read) 명령어로 실제 데이터 존재 여부를 교차 확인한다. 조회 실패 시 자동으로 재작업을 트리거한다.

**구현 예시:** gws sheets append ... && gws sheets read ... | grep "검증키"

**핵심 효과:** 거짓말이 “들통나는” 구조를 만들어 모델이 스스로 정직해지도록 유도한다. 에이전트는 자신의 거짓 보고가 뒤이은 검증 단계에서 반드시 발각된다는 것을 학습한다.

## **5\. SOUL.md 패치 예시**

기존 \[Proactive Execution\] 섹션을 다음의 \[Anti-Hallucination & Execution Protocol\]로 대체한다.

| \#\# Anti-Hallucination & Execution Protocol \- 도구 실행 환각 금지: exec 도구의 Exit Code 0 및 정상 출력 로그를 시스템으로부터 받기 전에는 절대로 "완료", "적재" 텍스트를 출력하지 말 것. \- 선 실행, 후 보고: 텍스트 답변 생성 전에 반드시 exec 도구로 gws sheets 명령어를 선행 실행할 것. \- 교차 검증 의무: 적재 후 gws sheets read 로 본인이 넣은 데이터가 실제 시트에 존재하는지 확인. 조회 실패 시 자동 재시도. |
| :---- |

## **6\. 일반화 가능한 교훈 (Generalizable Lessons)**

4. **“하라”는 “했는지 확인해라”를 포함하지 않는다.** 에이전트 프롬프트에서 실행 지시와 검증 지시는 반드시 분리하여 명시해야 한다.

5. **실행 환각은 “게으른” 에이전트의 문제가 아니라 구조적 취약점이다.** LLM의 토큰 예측 메커니즘상, “완료했습니다”는 통계적으로 높은 확률의 다음 토큰이다. 하네스로 강제하지 않으면 반복된다.

6. **교차 검증은 하네스의 “감사” 기능이다.** 에이전트가 자신의 결과물을 스스로 조회하게 함으로써, 거짓말이 발각되는 구조를 만든다. 이는 인간 조직의 내부감사와 동일한 원리다.

*본 문서는 **Harness Engineering and AgentOps** 필드 케이스 시리즈의 일부입니다.*

*원본 실험 데이터: Telegram Bot 로그 (2026-03-18) | 에이전트: MyOpenClawBot / Antfarm \+ GWS*