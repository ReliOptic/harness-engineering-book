# 문헌 참조 리스트 — Harness Engineering & AgentOps + KAIST PMBA 시험 대비

> 작성일: 2026-03-29
> 용도: (1) 『Harness Engineering and AgentOps』 집필용 학술 참조 (2) KAIST PMBA 중간고사 대비 개념 심화

---

## A. 핵심 아키텍처 — Transformer & Attention

| # | 논문/자료 | 저자 | 연도 | 활용 포인트 |
|---|----------|------|------|------------|
| A-1 | Attention Is All You Need | Vaswani et al. (Google) | 2017 | K-Q-V 메커니즘 원논문. 시험 답안의 기초 참조. 책에서는 에이전트 아키텍처의 기반으로 인용 |
| A-2 | Language Modeling Is Compression | Delétang et al. (DeepMind) | 2023 | Compression Hypothesis — "정확한 예측을 위해서는 이해가 필요하다"는 이론적 근거. 강의에서 다룬 "AI가 정말 사고하는가" 논의의 학술적 뒷받침 |

**시험 서술 연결:** A-1의 K-Q-V 구조 → Attention 가중치 오배분 → Hallucination 악화 경로를 서술할 때 기초 프레임

---

## B. RLHF → RLAIF 전환 계보

| # | 논문/자료 | 저자 | 연도 | 활용 포인트 |
|---|----------|------|------|------------|
| B-1 | Training Language Models to Follow Instructions with Human Feedback (InstructGPT) | Ouyang et al. (OpenAI) | 2022 | RLHF의 원형. 인간 평가자 기반 학습의 비용 구조와 한계를 보여주는 baseline |
| B-2 | RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback | Lee et al. (Google) | 2023 | 인간 → AI 평가 전환의 실증. RLHF와 RLAIF 성능이 거의 동등하다는 핵심 발견 |
| B-3 | Constitutional AI: Harmlessness from AI Feedback | Bai et al. (Anthropic) | 2022 | AI 자기 교정 루프(Self-critique). 에이전트 자기 감시(self-monitoring) 패턴의 이론적 원형. ARIA 프레임워크의 Runtime Guardrails 설계 시 참조 |

**책 집필 연결:** B-1 → B-2 → B-3 순서로 "파운데이션 모델 제작 비용 하락의 기술적 계보"를 설명하는 내러티브 구성 가능

---

## C. 합성 데이터와 비용 혁명

| # | 논문/자료 | 저자 | 연도 | 활용 포인트 |
|---|----------|------|------|------------|
| C-1 | Textbooks Are All You Need | Gunasekar et al. (Microsoft) | 2023 | Phi 모델. 합성 교과서 데이터만으로 소형 모델이 대형 모델에 근접한 성능 달성. 비용 혁명의 기술적 증거 |
| C-2 | Self-Instruct: Aligning Language Models with Self-Generated Instructions | Wang et al. | 2023 | 모델이 스스로 학습 데이터를 생성하는 방법론. 합성 데이터 파이프라인의 초기 형태 |

**책 집필 연결:** DeepSeek의 비용 효율성을 설명할 때 C-1, C-2를 기술적 배경으로 인용. Kiwon님이 직접 DeepSeek를 서빙한 경험과 결합하면 실무 사례 + 학술 근거의 투트랙 서술 가능

---

## D. 컨텍스트 설계와 Lost in the Middle

| # | 논문/자료 | 저자 | 연도 | 활용 포인트 |
|---|----------|------|------|------------|
| D-1 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. (Stanford/UC Berkeley) | 2023 | 긴 컨텍스트에서 중간 정보가 무시되는 현상의 실증. "Right Context > Big Context" 원칙의 학술적 근거 |
| D-2 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG) | Lewis et al. (Meta) | 2020 | 필요한 정보만 검색하여 컨텍스트에 주입하는 방법론. AgentOps에서 컨텍스트 관리 전략의 기초 |

**시험 서술 연결:** D-1을 K-Q-V로 재해석 — "불필요한 Key가 많아지면 Query가 엉뚱한 곳에 Attend하여 Hallucination 연쇄 발생"

**책 집필 연결:** D-2의 RAG 패턴은 에이전트의 메모리 관리(ARIA Memory Management 레이어)와 직결

---

## E. 에이전트 운영 — Temperature & 자기 교정

| # | 논문/자료 | 저자 | 연도 | 활용 포인트 |
|---|----------|------|------|------------|
| E-1 | Toolformer: Language Models Can Teach Themselves to Use Tools | Schick et al. (Meta) | 2023 | 에이전트의 도구 사용 학습. Temperature가 도구 선택 정확도에 미치는 영향 |
| E-2 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. | 2023 | 에이전트 자기 교정(Self-reflection) 루프. ARIA 프레임워크의 이론적 참조점. Pre-mortem의 proactivity 개념과 구조적 유사성 |
| E-3 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. (Princeton/Google) | 2023 | Reasoning + Acting 통합 패턴. 멀티 에이전트 시스템에서 각 에이전트의 추론-실행 루프 설계 시 기초 |

**책 집필 연결:** E-1~E-3는 하네스 엔지니어링 챕터에서 "에이전트 역할별 Temperature 프로파일" 설계의 이론적 기반. TeamClaws/PicoClaw 아키텍처의 설계 근거로 인용 가능

---

## F. 시각 자료 (강의 추천 포함)

| # | 자료 | 형식 | 활용 포인트 |
|---|------|------|------------|
| F-1 | 3Blue1Brown — Neural Network 시리즈 | YouTube | 벡터, 임베딩, Attention의 시각적 이해. 강의에서 직접 추천 |
| F-2 | Andrej Karpathy — LLM 소개 영상 | YouTube (3시간) | 4번째 숙제 필수 시청. 1.6배속 권장 |
| F-3 | 공돌이의 수학정리노트 | 한국어 블로그 | 한국어 기반 수학/벡터 개념 정리 |

---

## 활용 가이드

### 시험 대비 우선 읽기
1. A-1 (Attention 원논문) — 최소 Abstract + Section 3 (Multi-Head Attention)
2. D-1 (Lost in the Middle) — Abstract + Figure 1만으로도 핵심 파악 가능
3. F-2 (Karpathy 영상) — 숙제 겸 시험 대비

### 책 집필 우선 인용
1. B-1 → B-2 → B-3 (RLHF 비용 하락 계보)
2. C-1 (합성 데이터 비용 혁명)
3. E-2 (Reflexion — ARIA 자기 교정 루프)
4. D-1 (컨텍스트 설계 실증)

### 검색 팁
- 대부분 arXiv에서 무료 접근 가능 (arxiv.org에서 제목 검색)
- Google Scholar에서 제목 검색 시 PDF 직접 링크 확인 가능
