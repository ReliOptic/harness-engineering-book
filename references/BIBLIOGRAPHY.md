# Bibliography — 공신력 문헌 데이터베이스

> DR 딥리서치에서 인용된 원문 중 직접 인용 가능한 공신력 있는 출처만 추출·정리.
> DR 자체는 인용하지 않는다. 이 목록의 출처를 확인하고 인용한다.
>
> **신뢰도 기준**
> - **A등급**: arXiv 논문, ACL/NeurIPS/ICLR/ICML 게재, 동료심사 저널, Stanford HAI, DeepMind/MSR 공식 연구
> - **B등급**: 주요 기술기업 공식 블로그(AWS/Google/NVIDIA/Microsoft/Netflix/OpenAI/Anthropic), 공식 GitHub 저장소, McKinsey/Gartner 보고서

---

## Ch.1 — 에이전트 생태계 현황

### 기반 서적

- **AI Engineering: Building Applications with Foundation Models**
  Chip Huyen, O'Reilly, 2025
  DR출처: DR-1.3 | 신뢰도: B (단행본)
  URL: https://huyenchip.com/
  요약: Foundation model 기반 AI 시스템 설계의 핵심 프레임워크. evaluation, agent planning, RAG 등 체계화.

- **Common pitfalls when building generative AI applications**
  Chip Huyen, huyenchip.com, 2025-01-16
  DR출처: DR-1.3 | 신뢰도: B (저자 공식 블로그)
  URL: https://huyenchip.com/2025/01/16/ai-engineering-pitfalls.html
  요약: AI 시스템 구축 시 반복되는 실패 패턴. 저자가 직접 정리한 실무 관찰.

- **How to Evaluate AI that's Smarter than Us**
  ACM Queue, 2025
  DR출처: DR-1.3 | 신뢰도: A
  URL: https://queue.acm.org/detail.cfm?id=3722043
  요약: AI 평가의 한계와 LLM-as-judge의 구조적 편향.

### 오픈소스 에이전트 생태계

- **HKUDS/Nanobot — Build MCP Agents** (GitHub 공식 저장소)
  DR출처: DR-1.1 | 신뢰도: B (1차 소스)
  URL: https://github.com/HKUDS/nanobot
  요약: OpenClaw 대비 99% 코드 축소(~4,000 LoC). MCP Native Host, LiteLLM 라우팅. 33K+ stars.

- **Nanobot Roadmap: From Lightweight Agent to Agent Kernel**
  GitHub Discussion #431, HKUDS/nanobot
  DR출처: DR-1.1 | 신뢰도: B (공식 1차 소스)
  URL: https://github.com/HKUDS/nanobot/discussions/431
  요약: Nanobot의 장기 로드맵. Linux Kernel 방식의 에이전트 커널 지향.

- **Security Audit (2026-02-16) · Issue #258 · sipeed/picoclaw** (GitHub 공식 이슈)
  DR출처: DR-1.1 | 신뢰도: B (1차 소스)
  URL: https://github.com/sipeed/picoclaw/issues/258
  요약: PicoClaw 공식 보안 감사 결과. 블랙리스트 기반 RCE 방어의 구조적 한계, SSRF 취약점.

- **HKUDS/CLI-Anything: Making ALL Software Agent-Native** (GitHub 공식 저장소)
  DR출처: DR-3.2 | 신뢰도: B (1차 소스)
  URL: https://github.com/HKUDS/CLI-Anything
  요약: 모든 CLI 소프트웨어에 HARNESS.md를 부여하는 7단계 파이프라인. 1,298개 E2E 테스트.

- **Harness engineering: leveraging Codex in an agent-first world**
  OpenAI 공식 블로그
  DR출처: DR-3.2 | 신뢰도: B
  URL: https://openai.com/index/harness-engineering/
  요약: OpenAI의 harness engineering 개념 정의 및 Codex 활용 방향.

### A2A 경제 & 에이전트 정체성

- **Internet 3.0: Architecture for a Web-of-Agents with its Algorithm for Ranking Agents**
  arXiv:2509.04979
  DR출처: DR-1.4 | 신뢰도: A
  URL: https://arxiv.org/abs/2509.04979
  요약: 에이전트 간 신뢰·평판 알고리즘(AgentRank-UC) 설계. Web-of-Agents 아키텍처.

- **The EigenTrust Algorithm for Reputation Management in P2P Networks**
  Kamvar et al., Stanford NLP Group (WWW 2003)
  DR출처: DR-1.4 | 신뢰도: A
  URL: https://nlp.stanford.edu/pubs/eigentrust.pdf
  요약: P2P 신뢰 알고리즘 원본. 에이전트 평판 시스템의 이론적 기반.

- **Seizing the agentic AI advantage**
  McKinsey, 2025
  DR출처: DR-1.4 | 신뢰도: B
  URL: https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage
  요약: 기업 환경에서 agentic AI 도입의 ROI와 전략적 접근.

- **Global AI Adoption in 2025 — AI Economy Institute**
  Microsoft, 2025
  DR출처: DR-1.4 | 신뢰도: B
  URL: https://www.microsoft.com/en-us/corporate-responsibility/topics/ai-economy-institute/reports/global-ai-adoption-2025/
  요약: 기업의 AI 에이전트 도입 현황 및 투자 규모 통계.

- **Secure agentic AI for your Frontier Transformation**
  Microsoft Security Blog, 2026-03-09
  DR출처: DR-1.4 | 신뢰도: B
  URL: https://www.microsoft.com/en-us/security/blog/2026/03/09/secure-agentic-ai-for-your-frontier-transformation/
  요약: 에이전트 신원 인증, 권한 거버넌스, 공급망 보안 아키텍처.

- **Authorization and Identity Governance Inside AI Agents**
  Microsoft Community Hub, 2026
  DR출처: DR-1.4 | 신뢰도: B
  URL: https://techcommunity.microsoft.com/blog/microsoft-security-blog/authorization-and-identity-governance-inside-ai-agents/4496977
  요약: 에이전트 내부 인증·권한 설계 패턴.

- **Xcode 26.3 unlocks the power of agentic coding**
  Apple Newsroom, 2026-02
  DR출처: DR-1.4 | 신뢰도: B
  URL: https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/
  요약: Apple의 agentic coding 공식 지원 선언 및 기능 명세.

---

## Ch.2 — 모델 상속: 벤치마크 & 최적화

### 에이전트 벤치마크

- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?**
  Jimenez et al., Princeton, arXiv:2310.06770
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://arxiv.org/abs/2310.06770
  요약: 실제 GitHub 이슈를 Docker 환경에서 자율 해결하는 코딩 에이전트 벤치마크 원본.

- **The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models**
  ICML 2026 (poster)
  DR출처: DR-2.4 | 신뢰도: A
  URL: https://icml.cc/virtual/2025/poster/46593
  요약: LLM 함수 호출 능력의 종합 평가 체계. v4까지 진화한 BFCL의 에이전트 평가 확장.

- **Technical Performance | The 2025 AI Index Report**
  Stanford HAI, 2025
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://hai.stanford.edu/ai-index/2025-ai-index-report/technical-performance
  요약: 2025년 LLM 성능 벤치마크 통계. 독점 vs 오픈소스 모델 격차 추이.

- **Why Do Multi-Agent LLM Systems Fail?**
  arXiv:2503.13657
  DR출처: DR-2.1, DR-5.1 | 신뢰도: A
  URL: https://arxiv.org/pdf/2503.13657
  요약: 다중 에이전트 시스템의 실패 원인 분류. 정렬 오류, 환각, 도구 오용 패턴 분석.

- **How Do LLMs Fail In Agentic Scenarios? A Qualitative Analysis**
  arXiv:2512.07497
  DR출처: DR-2.1, DR-5.1 | 신뢰도: A
  URL: https://arxiv.org/html/2512.07497v1
  요약: 에이전트 시뮬레이션 환경에서 LLM 실패의 질적 분석. 성공/실패 조건 분류.

- **Agents of Chaos** (baulab.info 공식 연구 사이트)
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://agentsofchaos.baulab.info/
  요약: 에이전트 간 상호작용이 유발하는 11가지 임계 실패 패턴 연구.

- **Beyond ReAct: A Planner-Centric Framework for Complex Tool-Augmented LLM Reasoning**
  arXiv:2511.10037
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://arxiv.org/html/2511.10037v1
  요약: ReAct 한계 극복을 위한 계획 중심 에이전트 프레임워크.

- **Robust and Efficient Tool Orchestration via Layered Execution Structures with Reflective Correction**
  arXiv:2602.18968
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://arxiv.org/html/2602.18968v2
  요약: 도구 오케스트레이션의 계층화 구조와 반성적 오류 수정 메커니즘.

- **A Survey for LLM Agent Trajectory Analysis: From Failure Attribution to Enhancement**
  ResearchGate (peer-reviewed)
  DR출처: DR-5.1 | 신뢰도: A
  URL: https://www.researchgate.net/publication/401193207_A_Survey_for_LLM_Agent_Trajectory_Analysis_From_Failure_Attribution_to_Enhancement
  요약: LLM 에이전트 궤적 분석의 체계적 서베이. 실패 귀인 방법론 정리.

- **A Systematic Approach to Causal Reasoning Using Agentic AI in Distributed System Failures**
  ResearchGate (peer-reviewed)
  DR출처: DR-5.1 | 신뢰도: A
  URL: https://www.researchgate.net/publication/399952170_A_Systematic_Approach_to_Causal_Reasoning_Using_Agentic_AI_in_Distributed_System_Failures
  요약: 분산 시스템 장애에서 에이전트의 인과 추론 능력의 구조적 한계. Claude 3.5 기반 RCA 11.34% 정확도.

### 모델 압축 & 함수 호출

- **Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes**
  arXiv:2305.02301
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://arxiv.org/abs/2305.02301
  요약: 소형 모델이 교사 모델의 추론 과정을 학습하여 대형 모델 성능을 달성하는 증류 기법.

- **ODIA: Oriented Distillation for Inline Acceleration of LLM-based Function Calling**
  arXiv:2507.08877
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://arxiv.org/abs/2507.08877
  요약: 실시간 함수 호출 가속화를 위한 의도 기반 증류 라우팅. 단순 호출 → 소형 모델, 복합 추론 → 대형 모델.

- **Quantification of Large Language Model Distillation**
  ACL Anthology, 2025
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://aclanthology.org/2025.acl-long.248.pdf
  요약: LLM 증류 효과의 정량적 측정. 파라미터 압축 대비 성능 손실 체계화.

- **Accuracy is Not All You Need**
  NeurIPS 2024 (OpenReview)
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://arxiv.org/html/2407.09141v1
  요약: 양자화 모델의 정확도와 함수 호출 안정성이 별개임을 실증. 4-bit에서 최대 24% 플립 현상.

- **Attn-QAT: 4-Bit Attention With Quantization-Aware Training**
  arXiv:2603.00040
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://arxiv.org/html/2603.00040v2
  요약: Attention 계층의 4-bit 양자화 인지 학습. 구조적 정밀도 유지 기법.

- **ToolACE: Winning the Points of LLM Function Calling**
  arXiv:2409.00920 (OpenReview NeurIPS)
  DR출처: DR-2.4 | 신뢰도: A
  URL: https://arxiv.org/html/2409.00920v1
  요약: LLM 함수 호출 능력 특화 학습 데이터셋과 훈련 방법론.

- **Tool Zero: Training Tool-Augmented LLMs via Pure RL from Scratch**
  arXiv:2511.01934
  DR출처: DR-2.4 | 신뢰도: A
  URL: https://arxiv.org/html/2511.01934v1
  요약: 사전 지식 없이 순수 강화학습으로 도구 활용 LLM 훈련. 도구 사용의 근본 메커니즘 분석.

- **SimpleTool: Parallel Decoding for Real-Time LLM Function Calling**
  arXiv:2603.00030
  DR출처: DR-2.4 | 신뢰도: A
  URL: https://arxiv.org/html/2603.00030v1
  요약: 실시간 함수 호출을 위한 병렬 디코딩 접근. 지연 시간 최소화.

- **Architecting Resilient LLM Agents: A Guide to Secure Plan-then-Execute Implementations**
  arXiv:2509.08646
  DR출처: DR-2.4 | 신뢰도: A
  URL: https://arxiv.org/pdf/2509.08646
  요약: LLM 에이전트의 보안 아키텍처. Plan-then-Execute 패턴의 안전한 구현.

- **The effect of four-bit quantization on multi-agent LLM coding performance**
  University of Groningen thesis (peer-reviewed)
  DR출처: DR-2.3 | 신뢰도: A
  URL: https://fse.studenttheses.ub.rug.nl/37068/1/Thesis-T-Lukkien.pdf
  요약: 4-bit 양자화가 다중 에이전트 코딩 성능에 미치는 영향 실증 연구.

- **Optimizing LLMs for Performance and Accuracy with Post-Training Quantization**
  NVIDIA Developer Blog
  DR출처: DR-2.3 | 신뢰도: B
  URL: https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/
  요약: PTQ의 실제 구현. NVFP4 포맷, INT8 비교. NVIDIA 공식 기술 문서.

- **Amazon Bedrock Model Distillation: Boost function calling accuracy while reducing cost and latency**
  AWS Machine Learning Blog
  DR출처: DR-2.3 | 신뢰도: B
  URL: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-model-distillation-boost-function-calling-accuracy-while-reducing-cost-and-latency/
  요약: AWS Bedrock에서 함수 호출 특화 모델 증류 실험 결과. 비용·지연 감소 수치.

- **LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression**
  ACL Findings 2024
  DR출처: DR-5.2 | 신뢰도: A
  URL: https://aclanthology.org/2024.findings-acl.57.pdf
  요약: 프롬프트 압축 기법 LLMLingua-2. Task-agnostic, 최대 20배 압축.

---

## Ch.3 — Harness & AgentOps 정의

### AgentOps 도구 공식 문서

- **LangSmith Observability** (LangChain 공식 문서)
  DR출처: DR-3.3 | 신뢰도: B
  URL: https://www.langchain.com/langsmith/observability
  요약: LangSmith 아키텍처 공식 문서. 트레이싱, 평가, 프롬프트 허브 기능.

- **Systematic debugging for AI agents: Introducing the AgentRx Framework**
  Microsoft Research Blog
  DR출처: DR-5.1 | 신뢰도: B
  URL: https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/
  요약: MSR의 AgentRx 프레임워크. 에이전트 체계적 디버깅 방법론. 궤적 분석 기반.

- **ulab-uiuc/AgentDebug** (GitHub 공식 저장소)
  DR출처: DR-5.1 | 신뢰도: B (1차 소스)
  URL: https://github.com/ulab-uiuc/AgentDebug
  요약: LLM 에이전트 디버깅 도구. 실패 궤적 분석 및 귀인 자동화.

- **What is AI Agent Evaluation?**
  Databricks Blog
  DR출처: DR-5.1 | 신뢰도: B
  URL: https://www.databricks.com/blog/what-is-agent-evaluation
  요약: 에이전트 평가의 개념 및 Databricks Mosaic AI의 접근 방식.

---

## Ch.5 — 실험 결과 분석

### 실패 분류 & 분석 방법론

- **Agents of Chaos** — 원본 연구 사이트
  DR출처: DR-5.1 | 신뢰도: A
  URL: https://agentsofchaos.baulab.info/
  (위 Ch.2에도 등재)

- **(PDF) Agents of Chaos** — ResearchGate
  DR출처: DR-2.1 | 신뢰도: A
  URL: https://www.researchgate.net/publication/401123335_Agents_of_Chaos
  요약: OpenClaw 에이전트의 11가지 임계 실패 패턴 연구 논문 원문.

- **AI agents of chaos? New research shows how bots talking to bots can go sideways fast**
  ZDNet
  DR출처: DR-2.1 | 신뢰도: B
  URL: https://www.zdnet.com/article/how-ai-agents-create-new-disasters-when-they-interact/
  요약: Agents of Chaos 연구의 산업 해설. 다중 에이전트 상호작용 위험.

### 비용 최적화

- **RouteLLM: Learning to Route LLMs with Preference Data**
  ICLR 2025 Proceedings
  DR출처: DR-5.2 | 신뢰도: A
  URL: https://proceedings.iclr.cc/paper_files/paper/2025/file/5503a7c69d48a2f86fc00b3dc09de686-Paper-Conference.pdf
  요약: 선호도 데이터로 학습하는 LLM 라우팅. 강력한 모델과 약한 모델 간 비용-성능 균형.

- **Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey**
  arXiv:2603.04445
  DR출처: DR-5.2 | 신뢰도: A
  URL: https://arxiv.org/html/2603.04445v1
  요약: LLM 추론의 동적 라우팅과 캐스케이딩 기법 서베이. 비용 최적화 전략 종합.

- **A Unified Approach to Routing and Cascading for LLMs**
  arXiv:2410.10347 (ETH Zurich / OpenReview)
  DR출처: DR-5.2 | 신뢰도: A
  URL: https://arxiv.org/html/2410.10347v3
  요약: 라우팅과 캐스케이딩의 통합 수학적 프레임워크.

- **Towards Generalized Routing: Model and Agent Orchestration for Adaptive and Efficient Inference**
  arXiv:2509.07571
  DR출처: DR-5.2 | 신뢰도: A
  URL: https://arxiv.org/html/2509.07571v1
  요약: 에이전트 오케스트레이션까지 확장된 일반화 라우팅 이론.

- **Lower cost and latency for AI using Amazon ElastiCache as a semantic cache with Amazon Bedrock**
  AWS Database Blog
  DR출처: DR-5.2 | 신뢰도: B
  URL: https://aws.amazon.com/blogs/database/lower-cost-and-latency-for-ai-using-amazon-elasticache-as-a-semantic-cache-with-amazon-bedrock/
  요약: 시맨틱 캐싱으로 LLM 비용 절감. AWS 공식 실험 결과.

- **Prompt caching vs semantic caching: How to make AI agents faster**
  Redis 공식 블로그
  DR출처: DR-5.2 | 신뢰도: B
  URL: https://redis.io/blog/prompt-caching-vs-semantic-caching/
  요약: 프롬프트 캐싱과 시맨틱 캐싱의 차이 및 에이전트 속도 최적화.

### VM & 인프라 리소스 관리

- **AgentCgroup: Understanding and Controlling OS Resources of AI Agents**
  arXiv:2602.09345
  DR출처: DR-5.3 | 신뢰도: A
  URL: https://arxiv.org/html/2602.09345v2
  요약: AI 에이전트의 OS 리소스 소비 분석. cgroup 기반 제어 메커니즘. 도구 호출 시 최대 15.4배 메모리 버스트.

- **GPU-Virt-Bench: A Comprehensive Benchmarking Framework for Software-Based GPU Virtualization Systems**
  arXiv:2512.22125
  DR출처: DR-5.3 | 신뢰도: A
  URL: https://arxiv.org/html/2512.22125v1
  요약: GPU 가상화 시스템의 성능 벤치마크 프레임워크. vGPU vs MIG vs passthrough 비교.

- **Performance Evaluation of Virtual Machines and Containers in High Performance Computing**
  RSIS International Journal (peer-reviewed)
  DR출처: DR-5.3 | 신뢰도: A
  URL: https://rsisinternational.org/journals/ijrsi/uploads/vol13-iss2-pg794-805-202603_pdf.pdf
  요약: HPC 환경에서 VM과 컨테이너의 성능 오버헤드 정량 비교.

- **Performance Overhead Based Analysis of Container based Virtualization with Type1, Type2 Hypervisor**
  ResearchGate (peer-reviewed)
  DR출처: DR-5.3 | 신뢰도: A
  URL: https://www.researchgate.net/publication/395887423_Performance_Overhead_Based_Analysis_of_Container_based_Virtualization_with_Type1_Type2_Hypervisor
  요약: Type1/Type2 하이퍼바이저 및 컨테이너 가상화의 오버헤드 분석.

- **How to Reduce KV Cache Bottlenecks with NVIDIA Dynamo**
  NVIDIA Developer Blog
  DR출처: DR-5.3 | 신뢰도: B
  URL: https://developer.nvidia.com/blog/how-to-reduce-kv-cache-bottlenecks-with-nvidia-dynamo/
  요약: LLM KV 캐시 병목 해소 방법. NVIDIA Dynamo 기반 메모리 최적화.

- **An architectural decision: Containers on bare metal or on virtual machines**
  CNCF 공식 블로그, 2025-11-20
  DR출처: DR-5.3 | 신뢰도: B
  URL: https://www.cncf.io/blog/2025/11/20/an-architectural-decision-containers-on-bare-metal-or-on-virtual-machines/
  요약: 베어메탈 vs VM 위 컨테이너 배포 아키텍처 결정 가이드.

- **VRAM Requirements in Agentic AI Systems: A Comprehensive Guide**
  AWS Builder Center
  DR출처: DR-5.3 | 신뢰도: B
  URL: https://builder.aws.com/content/31Yeh8Jz9yCtgz9uL6lseoUQpLB/vram-requirements-in-agentic-ai-systems-a-comprehensive-guide
  요약: 에이전트 시스템의 VRAM 요구사항 분석. 모델 크기·툴 호출 시나리오별 수치.

---

## Ch.7 — 지속 학습 & Self-immune

### 지속 학습 이론

- **Continual Learning for Large Language Models: A Survey**
  arXiv:2402.01364
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://arxiv.org/html/2402.01364v1
  요약: LLM의 지속적 학습 기법 서베이. Catastrophic forgetting 회피 전략 종합.

- **LoRA-based Parameter-Efficient LLMs for Continuous Learning in Edge-based Malware Detection**
  arXiv:2602.11655
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://arxiv.org/html/2602.11655v1
  요약: 엣지 환경의 지속 학습. LoRA 기반 파라미터 효율적 적응.

- **Real-Time Procedural Learning From Experience for AI**
  arXiv:2511.22074
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://arxiv.org/abs/2511.22074
  요약: 에이전트의 실시간 절차적 학습. 경험 기반 지식 갱신 메커니즘.

- **A Definition of Continual Reinforcement Learning**
  Google DeepMind 공식 연구
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://deepmind.google/research/publications/33910/
  요약: 지속적 강화학습의 수학적 정의. DeepMind의 공식 연구 결과.

- **Multi-Agent Deep Reinforcement Learning for Multi-Robot Applications: A Survey**
  MDPI Sensors, 2023
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://www.mdpi.com/1424-8220/23/7/3625
  요약: 다중 에이전트 심층 강화학습 서베이. 협업 패턴, 보상 설계, 확장성.

- **Data-Centric Evolution in Autonomous Driving: A Comprehensive Survey**
  arXiv:2401.12888
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://arxiv.org/html/2401.12888v1
  요약: 자율주행에서 데이터 중심 접근. 지속 학습 적용 사례 (Tesla FSD 분석 포함).

### 실제 배포 사례

- **ML Platform Meetup: Infra for Contextual Bandits and Reinforcement Learning**
  Netflix Technology Blog
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://netflixtechblog.com/ml-platform-meetup-infra-for-contextual-bandits-and-reinforcement-learning-4a90305948ef
  요약: Netflix의 프로덕션 ML 플랫폼. Contextual Bandit과 RL 인프라 구성.

- **Foundation Model for Personalized Recommendation**
  Netflix Technology Blog
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://netflixtechblog.com/foundation-model-for-personalized-recommendation-1a0bd8e02d39
  요약: Netflix 추천 시스템의 Foundation Model 적용. 지속 업데이트 아키텍처.

- **AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms**
  Google DeepMind Blog
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
  요약: DeepMind의 자율 알고리즘 설계 에이전트. 진화적 자기 개선 루프.

- **When bias begets bias: A source of negative feedback loops in AI systems**
  Microsoft Research Blog
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://www.microsoft.com/en-us/research/blog/when-bias-begets-bias-a-source-of-negative-feedback-loops-in-ai-systems/
  요약: AI 시스템 내 부정적 피드백 루프의 편향 증폭 메커니즘. MSR 공식 연구.

- **A dev's guide to production-ready AI agents**
  Google Cloud Blog
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://cloud.google.com/blog/products/ai-machine-learning/a-devs-guide-to-production-ready-ai-agents
  요약: 프로덕션 AI 에이전트 설계 가이드. Google Cloud의 실무 지침.

- **Architecting the production feedback loops**
  AWS Prescriptive Guidance
  DR출처: DR-7.2 | 신뢰도: B
  URL: https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/prod-monitoring-feedback.html
  요약: 프로덕션 AI 에이전트의 피드백 루프 설계. AWS 공식 처방 가이드.

---

## 미분류 / 크로스 챕터

- **Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning**
  arXiv:2511.04831
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://arxiv.org/html/2511.04831v1
  요약: NVIDIA Isaac Lab의 GPU 가속 시뮬레이션 프레임워크. 다중 에이전트 강화학습 환경.

- **(Mis-)use of standard Autopilot and Full Self-Driving Beta: Results from interviews with users**
  PMC (PubMed Central, peer-reviewed)
  DR출처: DR-7.2 | 신뢰도: A
  URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9996345/
  요약: Tesla FSD 사용자 인터뷰. 자율 에이전트에 대한 인간 신뢰 및 오용 패턴.

- **Fine-tuning LLMs for Function Calling with xLAM Dataset**
  Hugging Face Open-Source AI Cookbook (공식)
  DR출처: DR-2.4 | 신뢰도: B
  URL: https://huggingface.co/learn/cookbook/en/function_calling_fine_tuning_llms_on_xlam
  요약: 함수 호출 특화 파인튜닝. xLAM 데이터셋 사용 방법 공식 가이드.

---

## 색인: arXiv 논문 목록

| arXiv ID | 제목 요약 | 챕터 관련 | 신뢰도 |
|---|---|---|---|
| 2310.06770 | SWE-bench 원본 | Ch.2 | A |
| 2305.02301 | Distilling Step-by-Step | Ch.2 | A |
| 2402.01364 | Continual Learning for LLMs Survey | Ch.7 | A |
| 2407.09141 | Accuracy is Not All You Need | Ch.2 | A |
| 2409.00920 | ToolACE | Ch.2 | A |
| 2410.10347 | Unified Routing and Cascading | Ch.5 | A |
| 2503.13657 | Why Do Multi-Agent LLM Systems Fail | Ch.2/5 | A |
| 2507.08877 | ODIA (distillation for function calling) | Ch.2 | A |
| 2509.04979 | Internet 3.0 Web-of-Agents | Ch.1 | A |
| 2509.07571 | Generalized Routing | Ch.5 | A |
| 2509.08646 | Architecting Resilient LLM Agents | Ch.2/3 | A |
| 2511.01934 | Tool Zero (pure RL) | Ch.2 | A |
| 2511.10037 | Beyond ReAct | Ch.2 | A |
| 2511.22074 | Real-Time Procedural Learning | Ch.7 | A |
| 2512.07497 | How Do LLMs Fail In Agentic Scenarios | Ch.2/5 | A |
| 2512.22125 | GPU-Virt-Bench | Ch.5 | A |
| 2602.09345 | AgentCgroup | Ch.5 | A |
| 2602.11655 | LoRA Continuous Learning | Ch.7 | A |
| 2603.00030 | SimpleTool Parallel Decoding | Ch.2 | A |
| 2603.00040 | Attn-QAT | Ch.2 | A |
| 2603.04445 | Dynamic Model Routing Survey | Ch.5 | A |

---

*최종 업데이트: 2026-03-16 | 완료된 DR 기준: DR-1.1, 1.3, 1.4, 2.1, 2.3, 2.4, 3.2, 3.3, 5.1, 5.2, 5.3, 7.2*
*미시작 DR(1.2, 2.2, 3.1, 3.4, 4.x, 6.x, 7.1) 완료 시 이 파일에 추가할 것.*
