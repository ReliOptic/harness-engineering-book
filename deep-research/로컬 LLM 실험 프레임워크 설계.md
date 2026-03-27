# **로컬 LLM 생태계의 주요 모델 및 실험 환경 조합 분석 보고서: 8GB VRAM 이하 환경을 중심으로**

## **\[섹션 A: 핵심 발견 (선행 실험의 로컬 LLM 포함 패턴, 자주 쓰이는 조합, 유의미한 결과 요약)\]**

2024년 6월 이후 로컬 대형 언어 모델(Large Language Model, LLM) 생태계는 모델의 단순한 파라미터 크기 경쟁에서 벗어나, 양자화(Quantization) 아키텍처의 효율성 극대화, 컨텍스트 윈도우(Context Window)의 기하급수적 확장, 그리고 외부 애플리케이션과의 상호작용을 위한 네이티브 함수 호출(Function Calling) 능력의 최적화라는 세 가지 축을 중심으로 급격한 패러다임 전환을 맞이하였다. 특히 오픈소스 생태계의 표준으로 자리 잡은 Ollama 및 llama.cpp 프레임워크 기반의 로컬 추론 환경에서는 GGUF(GPT-Generated Unified Format) 포맷이 사실상의 산업 표준으로 안착하였다. 수많은 선행 실험과 벤치마크 지표를 종합할 때, GGUF 포맷 중에서도 4-bit 양자화 방식인 Q4\_K\_M(K-quants 방식의 중간 수준 양자화) 모델이 추론 정밀도 보존과 비디오 랜덤 액세스 메모리(VRAM) 요구량 감소 사이에서 가장 이상적인 수학적 균형점을 제공하는 것으로 입증되었다.1 본 섹션에서는 하드웨어 제약이 뚜렷한 8GB VRAM 이하의 환경을 중심으로, 최근 출시된 모델들이 보여주는 아키텍처적 패턴, 성능 한계점, 그리고 산업계와 연구계에서 빈번하게 채택되는 실험적 조합의 유의미한 결과들을 심층적으로 분석한다.

### **1\. 8GB VRAM 환경의 물리적 한계와 GGUF 기반 메모리 할당 공식의 재정의**

현대의 대다수 엔트리급 및 메인스트림 로컬 AI 구축 사례에 있어서 8GB VRAM(예: NVIDIA RTX 3060, RTX 4060 등)은 가장 보편적이면서도 넘기 힘든 하드웨어 상한선으로 작용한다.4 선행 연구 및 실험 데이터에 따르면, GGUF 포맷을 구동할 때 발생하는 VRAM 소모량은 단순히 모델의 가중치(Weights)가 디스크에서 차지하는 물리적 크기에만 의존하지 않는 다차원적인 함수 관계를 띤다. llama.cpp 프레임워크의 내부 메모리 할당 메커니즘을 분석한 선행 가설에 따르면, 모델을 GPU에 적재할 때의 전체 VRAM 요구량은 모델을 구성하는 텐서의 크기, GPU로 오프로딩되는 레이어의 비율(gpu-layers), 그리고 활성화된 컨텍스트 길이에 따른 상태 저장 공간(ctx-size)의 합으로 산출된다.5 이를 수학적 공식으로 단순화하면, 전체 VRAM 사용량은 전체 레이어 수 대비 GPU 할당 레이어 수의 비율에 디스크 상의 모델 크기를 곱한 값에, 컨텍스트 길이에 비례하여 선형적으로 증가하는 키-값 캐시(KV Cache) 메모리 크기를 더한 값으로 정의할 수 있다.1

이러한 공식적 접근은 모델을 전적으로 GPU에 오프로딩하여 추론 속도를 극대화하고자 할 때, 모델 자체의 가중치 크기뿐만 아니라 텍스트 생성 과정에서 발생하는 동적인 메모리 할당이 매우 치명적인 제약 요인으로 작용함을 시사한다. 예를 들어, 7B에서 8B 파라미터 규모를 지닌 모델의 경우 Q4\_K\_M 양자화를 적용하면 디스크 상에서 약 4.6GB에서 5.5GB 내외의 용량을 차지하게 된다.2 그러나 이는 정적인 가중치 데이터일 뿐이며, 여기에 8K 토큰 수준의 컨텍스트를 처리하기 위한 KV 캐시 및 주의력(Attention) 메커니즘 연산용 버퍼를 더할 경우 실제 운영 체제 레벨에서 점유하는 VRAM은 약 6GB에서 7GB 수준으로 급등하게 된다.1 이는 8GB VRAM이라는 물리적 한계에 완벽히 부합하면서도 운영 체제의 백그라운드 프로세스가 사용할 최소한의 여유 공간(약 1GB 내외)을 남겨두는 가장 안정적인 조합이다. 반면, 컨텍스트 길이를 최신 모델들이 지원하는 32K 이상으로 확장하거나 1M 토큰이라는 극단적인 환경으로 늘릴 경우, 모델 가중치 자체는 4.3GB에 불과하더라도 전체 가중치 스케일의 KV 캐시만으로 100GB 이상이 추가로 요구되어 단일 GPU 환경에서는 즉각적이고 치명적인 OOM(Out of Memory) 크래시를 유발한다.8 결론적으로 8GB VRAM 한계 내에서는 8B 이하의 파라미터를 가진 모델을 채택하고, 활성 컨텍스트 윈도우를 8K 이하로 엄격히 제한하여 운영하는 파이프라인 설계가 가장 실패율이 낮은 표준 패턴으로 확립되었다.

### **2\. 후보 모델들의 구조적 부적합성 및 경량화 모델로의 전환 패러다임**

사용자가 질의에서 제시한 대형 후보 모델군인 Llama 3.3 70B, Qwen 2.5 Coder 32B, Mistral Small 3.1 24B, Phi-4 14B, Gemma 3 27B는 모두 2024년 6월 이후 출시되어 각 벤더사의 최상위 기술력이 집약된 오픈 가중치 모델들이다. 이들은 다중 스텝 추론, 복잡한 함수 호출, 그리고 에이전틱(Agentic) 워크플로우에서 기존의 독점적 상용 API(예: GPT-4o, Claude 3.5 Sonnet)에 필적하거나 이를 능가하는 성과를 보여주었다.7 그러나 8GB VRAM 이하라는 엄격하고 구체적인 제약 조건 앞에서는 이들 모두가 물리적 구조의 한계로 인해 구동이 원천적으로 불가능하거나, CPU 메모리로의 막대한 데이터 스와핑을 강제함으로써 토큰 생성 속도가 실사용이 불가능한 수준으로 급락하는 현상을 동반한다. 아래 표는 해당 대형 모델들의 Q4\_K\_M 양자화 기준 VRAM 요구량과 8GB 환경에서의 부적합 사유를 상세히 분석한 결과이다.

| 후보 모델명 | 파라미터 규모 | Q4\_K\_M VRAM 요구량 (추정치) | 8GB VRAM 환경 부적합 사유 및 물리적 한계점 |
| :---- | :---- | :---- | :---- |
| Llama 3.3 70B | 70 Billion | 40GB 이상 | Meta의 최상위 추론 모델로 단일 시스템에서는 최소 2개의 24GB GPU(RTX 3090/4090) 또는 48GB 이상의 워크스테이션급 VRAM(RTX A6000 등)이 강제된다. 8GB 환경에서는 로드조차 불가능하다.1 |
| Qwen 2.5 Coder 32B | 32 Billion | 22GB \~ 24GB | 코딩 및 다중 추론 벤치마크에서 압도적인 성능을 보이나, 모델 가중치 적재에만 20GB 이상이 필요하다. 16GB VRAM 환경에서도 컨텍스트를 8K로 제한하고 CPU 오프로딩을 병행해야 간신히 25 t/s로 구동되므로 8GB에서는 구동 불가하다.1 |
| Gemma 3 27B | 27 Billion | 18GB \~ 24GB | Google DeepMind의 다중 모달 모델로, 구조적으로 메모리 대역폭 요구량이 높다. 32GB VRAM 환경에서 Q4\_K\_M 양자화를 적용해야 컨텍스트를 포함하여 간신히 적재되며, 8GB 환경은 시도 자체가 무의미하다.1 |
| Mistral Small 3.1 24B | 24 Billion | 16GB \~ 18GB | 중간 규모 체급에서 가장 빠른 토큰 처리 속도를 자랑하지만, 여전히 16GB 이상의 하드웨어(예: RTX 4070 Ti SUPER)를 목표로 설계된 모델이다. 8GB VRAM에서는 메모리 오버플로우가 발생한다.7 |
| Phi-4 | 14 Billion | 10GB \~ 12GB | Microsoft의 고효율 모델이나, 14B 체급의 한계로 인해 Q4\_K\_M 파일 크기만 9.05GB에 달한다. 8K 컨텍스트를 더하면 10GB를 초과하여, 8GB GPU에서는 필연적으로 레이어의 상당 부분을 시스템 RAM으로 넘겨야 하므로 병목이 극심하다.15 |

이러한 물리적 한계점들은 선행 실험자들과 산업계의 로컬 LLM 적용 파이프라인을 근본적으로 변화시켰다. 연구자들은 70B나 32B와 같은 거대한 모델을 억지로 압축하기보다는, 대형 모델을 통해 정제된 데이터를 바탕으로 학습된 소형 파라미터 버전(3B\~8B 체급)을 채택하거나 '지식 증류(Knowledge Distillation)' 기법이 적용된 경량화 모델을 활용하는 방향으로 패러다임을 완전히 전환하였다. 즉, Llama 3.1 8B, Qwen 2.5 Coder 7B, Phi-4-mini (3.8B), Gemma 3 4B와 같은 모델들이 8GB VRAM 제약을 안정적으로 만족하면서도 대형 모델의 논리적 추론 구조와 네이티브 도구 호출 능력을 정교하게 모방할 수 있는 최적의 현실적 대안으로 부상한 것이다.1

### **3\. BFCL (Berkeley Function Calling Leaderboard) 기반 도구 호출 패턴의 진화와 에이전틱 능력 평가**

2024년 6월 기점 이후 출시된 로컬 모델들의 가장 파괴적인 혁신은 단순한 자연어 텍스트 생성을 넘어서서, 시스템 프롬프트에 정의된 API 명세서(API Documentation)를 정확히 해석하고 이에 부합하는 JSON 또는 XML 형태의 함수 호출 코드를 네이티브(Native)로 반환하는 능력을 모델의 가중치 자체에 내재화했다는 점이다.20 UC 버클리 대학에서 주도하는 Berkeley Function Calling Leaderboard (BFCL) V4 벤치마크의 실증적 결과에 따르면, 최신의 8B 체급 이하 로컬 소형 모델들은 단일 턴(Single-turn) 도구 호출 환경에서 과거 클라우드 기반의 대형 모델(예: 초기 GPT-4)에 필적하거나 이를 상회하는 70% 이상의 높은 AST(Abstract Syntax Tree) 파싱 정확도를 지속적으로 기록하고 있다.10

이러한 성과는 모델 아키텍처 내에서 함수 호출 포맷을 어떻게 인식하고 처리하는지에 따라 극명한 차이를 만들어낸다. Qwen 2.5 Coder 시리즈나 Llama 3.1 8B와 같은 모델들은 훈련 단계에서부터 도구 호출에 필요한 특수 토큰과 JSON 스키마 구조를 가중치 내부에 직접 학습시킨 'Native Function Calling'을 지원한다.20 이 방식은 사용자가 외부에서 복잡한 정규 표현식이나 파서(Parser)를 구축하지 않아도, 프레임워크 수준에서 안정적으로 도구 매개변수를 추출할 수 있게 해준다. 반면, 네이티브 지원이 미비하여 프롬프트 엔지니어링만으로 도구 호출을 강제해야 하는 구형 모델이나 일부 경량 모델의 경우, 긴 문맥 내에서 주의력이 분산되어 XML 태그를 누락하거나 필수 매개변수의 자료형을 혼동하는 등 포맷 민감도(Format sensitivity) 측면에서 치명적인 점수 하락이 발생함이 실험적으로 증명되었다.24

더욱 주목할 만한 점은 BFCL V4가 새롭게 도입한 다중 턴(Multi-turn) 상호작용 및 에이전틱(Agentic) 추론 평가에서의 한계 노출이다. BFCL V4는 웹 검색, 메모리 관리 등 실제 에이전트 환경과 유사한 다중 단계의 시나리오를 구성하여 모델을 평가하였다.25 연구 결과에 따르면, 8B 이하의 소형 로컬 모델들은 독립된 단일 함수 호출에서는 70\~80%의 높은 정확도를 보여 대형 모델과 유사한 지표를 기록하지만, 10개 이상의 복잡한 도구 명세가 주어지거나 여러 단계를 거쳐 상태(State)를 유지해야 하는 에이전틱 시나리오에서는 치명적인 논리적 결함을 드러낸다.26 이들은 이전 단계의 함수 실행 결과를 망각하여 환각(Hallucination)된 변수를 다음 함수에 주입하거나, 더 이상의 도구 호출이 필요 없는 상황(예: 최종 답변 도출)에서도 동일한 함수를 무한히 반복 호출하는 루프(Loop) 현상에 빠지는 취약점을 빈번하게 노출하였다. 이는 파라미터 제약으로 인해 확장된 컨텍스트 내에서 장기 의존성(Long-term dependency)을 유지하는 능력이 대형 모델 대비 구조적으로 부족하기 때문으로 분석된다.11

### **4\. 양자화(Quantization) 메커니즘이 코드 생성 및 다중 스텝 추론에 미치는 비선형적 영향**

GGUF 환경에서의 가중치 양자화는 단순히 파일 용량을 줄이는 선형적인 압축 과정이 아니라, 텐서 단위의 정밀도를 선택적으로 버림으로써 모델의 인지적 행동 패턴을 변화시키는 비선형적 메커니즘이다. 다양한 선행 실험, 특히 HumanEval과 같은 코드 생성 벤치마크 및 다중 스텝 추론(SWE-Bench)을 수행하는 환경에서 양자화가 미치는 영향에 대한 흥미롭고 일관된 패턴이 관찰되었다.2 일상적인 대화나 요약과 같은 자연어 생성 과제에서 Q4\_K\_M 양자화 모델의 결과물은 FP16(반정밀도 부동소수점) 기반의 원본 모델이 생성한 결과물과 인간의 눈으로 구별하기 어려울 만큼 높은 품질 보존율을 보여준다.

그러나 괄호의 여닫음, 변수명의 정확한 일치, 그리고 엄격한 JSON 스키마의 중괄호 구조 등 단 하나의 토큰 오차도 허용되지 않는 구문 규칙(Syntax Rule) 환경에서는 상황이 크게 달라진다. 4-bit 단위로 손실 압축된 가중치는 신경망의 깊은 레이어를 통과하며 오차를 누적시키고, 이는 종종 도구 호출 시 매개변수의 키(Key) 값을 미세하게 오타 내거나 불필요한 이스케이프 문자를 삽입하는 치명적 오류로 직결된다. 이러한 양자화 손실을 방어하기 위해 llama.cpp 생태계의 전문 연구자들은 중요도가 높은 임베딩(Embedding) 텐서와 최종 출력(Output) 텐서에 한하여 8-bit(Q8)의 높은 정밀도를 유지하고 나머지 은닉층(Hidden layers)만 압축하는 Q6\_K\_L이나 Q5\_K\_M과 같은 혼합 양자화(Mixed-precision Quantization) 포맷을 선호하는 경향을 보인다.2 하지만 8GB VRAM이라는 물리적 임계값을 전제로 할 경우, 고정밀 양자화를 채택하여 모델 용량을 6GB 이상으로 늘리면 KV 캐시를 위한 공간이 1\~2GB 미만으로 축소되어 불과 2K 수준의 컨텍스트만으로도 시스템이 다운되는 딜레마에 빠지게 된다. 따라서 파라미터 수를 7B에서 8B 체급 이하로 타협하더라도 가중치 압축률을 Q4\_K\_M 수준으로 유지하여 전체 VRAM의 약 20%에서 30%를 KV 캐시 변동성에 대응하기 위한 여유 버퍼로 남겨두는 설계가 시스템 안정성을 보장하는 '가장 실패율이 낮은' 최적의 실험 환경이자 산업계 표준으로 완전히 굳어졌음을 확인하였다.1

---

사용자가 원본 질의에서 후보군으로 검토를 요청한 70B, 32B 등의 대규모 모델들은 섹션 A에서 엄밀히 규명된 VRAM의 물리적 할당 한계 공식 및 KV 캐시의 구조적 한계로 인하여 배제하였다. 대신, 해당 거대 모델군을 개발한 동일 벤더사의 최신 아키텍처와 추론 알고리즘을 온전히 계승하면서도 지정된 모든 요구 조건(2024년 6월 이후 출시, 공식 Function Calling 지원, GGUF Q4\_K\_M 기준 8GB VRAM 이하 점유, 코드 및 멀티스텝 추론 벤치마크 지표 보유)을 완벽하게 충족하는 경량화 및 소형 파라미터 모델 4종을 엄선하여 최종 추천 라인업으로 구성하였다.

### **추천 로컬 모델 라인업 표**

다음 표는 추천 모델 4종의 주요 메타데이터, Ollama 구동을 위한 고유 ID, Q4\_K\_M 양자화 적용 시의 모델 가중치 VRAM 요구량, 함수 호출의 아키텍처적 지원 방식, 그리고 버클리 도구 호출 리더보드(BFCL V4) 상의 평가 정확도를 종합하여 정리한 것이다.

| 모델 (제작사 / 가족군) | Ollama ID | VRAM(Q4\_K\_M) | Tool Call 방식 | TCR(도구 호출 정확도) 출처 및 핵심 비고 |
| :---- | :---- | :---- | :---- | :---- |
| **Qwen 2.5 Coder (7B)** *(Alibaba Cloud)* | qwen2.5-coder:7b | 약 4.68 GB 2 | Native FC (완전 지원) | **BFCL V4**: 전체 정확도 상위권(약 76\~77% 내외). 특징: 단일 턴 및 병렬 호출에서 탁월. 가장 안정적인 JSON 스키마 인식률을 보유한 동급 최강 모델.10 |
| **Llama 3.1 (8B)** *(Meta)* | llama3.1:8b | 약 4.92 GB 6 | Native FC / Prompt | **BFCL V4**: 전체 정확도 약 72.8%. 특징: 범용 에이전트 및 RAG 파이프라인에서 가장 균형 잡힌 다목적 밸런스 제공. 단, 포맷 민감도 주의 요망.7 |
| **Phi-4-mini (3.8B)** *(Microsoft)* | phi4-mini | 약 2.50 GB 1\* | Native FC | **BFCL V4 / 자체 보고서**: 14B 모델의 추론력을 증류함. 특징: 8GB VRAM 환경에서도 최대 32K 이상의 거대한 컨텍스트 윈도우 캐시 확보가 가능한 극강의 효율성.19 |
| **Gemma 3 (4B)** *(Google DeepMind)* | gemma3:4b | 약 3.50 GB 30\* | Modelfile 템플릿 제어 / Prompt | **BFCL V4**: 전체 정확도 약 61\~67%. 특징: 공식 지원은 존재하나 Ollama 내부 파싱 충돌로 인해 커스텀 Modelfile을 통한 템플릿 우회(Workaround) 설정이 필수적임.10 |

*주의: 표기된 VRAM 요구량은 순수 모델 가중치 파일 크기를 의미하며, 추론 시 활성화되는 컨텍스트 길이에 따른 KV 캐시 할당량이 더해지면 실제 OS 상의 점유율은 모델에 따라 6GB에서 7.5GB 선까지 동적으로 상승한다.*

### **라인업 모델별 적합성 및 한계 심층 평가**

본 소절에서는 앞선 표에서 제시한 4종의 추천 모델들이 왜 8GB VRAM이라는 제약 조건 속에서 최적의 선택지인지, 그리고 각 모델이 지닌 아키텍처적 강점과 벤치마크 상의 한계점은 무엇인지를 깊이 있게 해체하여 분석한다.

**1\. Qwen 2.5 Coder 7B (Alibaba Cloud)** 2024년 하반기에 정식으로 출시된 Qwen 2.5 Coder 라인업은 8GB VRAM 이하의 로컬 하드웨어에서 코딩, 디버깅, 그리고 다중 스텝 추론의 기준점(Benchmark)을 재정의한 모델이다. 무려 18조(18 Trillion) 개에 달하는 방대한 코드 및 수학 중심의 토큰 데이터셋으로 사전 학습을 거쳤으며, 이 중에서도 특화된 미세 조정(Fine-tuning)을 거친 Instruct 버전은 BFCL 리더보드의 다양한 평가 항목에서 자신보다 두 배 이상 거대한 체급의 모델들을 상회하는 점수를 기록하고 있다.27 구조적으로 Q4\_K\_M 양자화를 적용할 경우 VRAM 점유율이 4.68GB에 불과하여, 8GB 환경 내에서도 약 16K에서 32K 사이의 컨텍스트 윈도우를 안정적으로 확보할 수 있는 엄청난 유연성을 제공한다.2 특히 에이전트 구축 시 가장 핵심이 되는 능력인 네이티브 JSON 포맷 출력 능력이 8B 이하 체급 중 단연 독보적이다. LangChain이나 LlamaIndex와 같은 외부 워크플로우 오케스트레이션 프레임워크와 연동할 때, 함수 호출의 매개변수 누락이나 파싱 오류(Parsing Error)가 가장 적게 관찰되는 매우 신뢰도 높은 조합을 구성할 수 있다.

**2\. Meta Llama 3.1 8B (Meta)** 2024년 7월에 대대적으로 공개된 Meta의 Llama 3.1 8B는 상위 체급인 70B 모델이 구축해 둔 탄탄한 지식 체계와 아키텍처의 강점을 그대로 이어받은 현존 최고의 오픈 가중치 올라운더(All-rounder) 모델이다.7 GGUF Q4\_K\_M 포맷으로 변환 시 약 4.92GB의 VRAM 메모리를 차지하며, 이는 8GB 시스템 RAM 구조에 정확히 핏(Fit)된다.6 이 모델은 MMLU, HumanEval 등 주요 글로벌 벤치마크에서 동급 파라미터 층위의 모든 모델을 압도하는 최상위권의 범용 추론 능력을 일관되게 유지한다.7 Ollama 프레임워크 내에서 도구 호출을 완벽하게 공식 지원하며, 시스템 프롬프트를 통해 여러 도구의 상세 명세를 제공할 때 뛰어난 지시 이행(Instruction Following) 능력을 발휘한다. 하지만, 극도로 복잡한 에이전틱 과제를 수행하거나 API가 엄격한 XML 포맷의 반환을 요구할 경우, 작은 파라미터 크기에서 기인하는 본질적인 포맷 민감도(Format sensitivity) 문제로 인해 XML 태그 누락이나 문법적 결함이 간헐적으로 관찰된다는 한계 또한 보고되고 있어 시스템 프롬프트의 정밀한 튜닝이 요구된다.10

**3\. Phi-4-mini 3.8B (Microsoft)** 초기 사용자의 질의에서 포함된 Phi-4 14B 모델이 8GB VRAM 제한을 초과하는 물리적 장벽에 부딪힘에 따라, 그 아키텍처적 우수성을 훼손하지 않으면서도 완벽한 대안으로 투입될 수 있는 모델이 바로 Phi-4-mini 3.8B이다.7 파라미터 수가 3.8B로 극히 제한적인 소형 모델임에도 불구하고 Q4\_K\_M 적용 시 요구되는 모델 자체의 메모리 풋프린트가 2.5GB 수준에 불과하다.1 이러한 경이로운 메모리 최적화는 8GB VRAM 환경에서 시스템 백그라운드 구동을 고려하더라도 남는 거의 모든 VRAM을 전적으로 컨텍스트 윈도우 캐시(이론상 최대 128K 이상 지원 가능)의 기하급수적 확장에 투자할 수 있음을 의미한다.19 Microsoft 특유의 고품질 합성 데이터(Synthetic Data)를 집중적으로 주입한 학습 레시피와 다중 모달 확장을 위한 LoRA(Low-Rank Adaptation) 라우팅 기술을 통해, 이 모델은 코딩 및 수학적 논리 추론 능력에서 일반적인 8B 체급의 모델들과 대등하게 경쟁하는 저력을 보여준다. 특히 하드웨어 자원이 극도로 제한된 엣지 디바이스나 오프라인 노트북 환경에서 반응성이 중요한 다이내믹 에이전트를 구축해야 할 때, 가장 높은 토큰 생성 속도(Tokens Per Second, TPS)와 짧은 지연시간을 보장하는 최고의 선택지로 평가받는다.7

**4\. Gemma 3 4B (Google DeepMind)** 2025년 3월에 새롭게 출시된 Google DeepMind의 Gemma 3 라인업 중 4B 모델은, 동급의 27B 및 12B 모델들이 공통적으로 겪고 있는 치명적인 메모리 요구량 팽창 문제를 영리하게 피해갈 수 있도록 설계된 고효율 소형 버전이다.13 이 모델은 구조적으로 128K에 달하는 광활한 컨텍스트 윈도우를 기본적으로 제공하며 텍스트와 비전을 아우르는 다중 모달(Multimodal) 능력을 가중치 내부에 내포하고 있다. Google 측은 문서와 기술 블로그를 통해 Gemma 3 아키텍처가 함수 호출을 완벽하게 공식 지원한다고 천명하였으나 39, 현재 Ollama 생태계 내부의 구동 레이어에서는 Gemma 3의 함수 호출 템플릿(Chat template)을 파싱하는 과정에서 이중 \<bos\>(Begin of Sentence) 토큰이 강제 삽입되거나 도구 호출 포맷의 인식이 불완전하게 이루어지는 등의 호환성 이슈가 지속적으로 보고되고 있다.22 이를 근본적으로 해결하기 위해서는 사용자가 Ollama 내에서 커스텀 Modelfile을 직접 작성하여, 도구 호출 태그와 하이브리드 시스템 프롬프트를 수동으로 매핑하는 정밀한 우회(Workaround) 설정이 필수적으로 동반되어야만 제 성능을 끌어낼 수 있다.31 BFCL V4 벤치마크 기준으로는 약 61%에서 67% 사이의 정확도를 기록하여 선두 그룹(Qwen 등)보다는 다소 아쉬운 모습을 보이지만, 양자화 인식 훈련(QAT)이 도입된 최신 아키텍처의 강력한 잠재력을 바탕으로 향후 템플릿 최적화 시 성능의 극적인 상승이 기대된다.10

## ---

**\[섹션 C: 프레임워크 실험 설계 변경 권고 (E01\~E03 수정 방향, compute 변수 측정 추가 방법, 방법론적 함정)\]**

최첨단 로컬 LLM을 평가하고 비교하기 위한 실험 설계는, 막대한 서버 인프라를 바탕으로 무한한 자원을 소모하는 클라우드 API 기반의 평가 모델과는 그 철학과 방법론의 궤를 근본적으로 달리해야 한다. 기존 문헌이나 평가 체계에서 성격 심리학, 다면 평가, 또는 단순 생성형 AI의 정성적 분석에서 차용되었을 법한 추상적인 'E01\~E03' 평가 축(Axis)은 복잡한 도구 호출과 에이전틱 파이프라인을 검증하는 데 있어 심각한 한계를 노출한다.43 따라서 해당 변수 축들을 로컬 LLM의 기계적 도구 호출 정확도, 컨텍스트 상태 유지력, 그리고 연산 효율성을 정량적으로 교차 평가하는 3차원 실험 프레임워크로 전면 해체 및 재구성할 것을 권고한다. 아울러 VRAM이 8GB로 엄격히 제한된 엣지 컴퓨팅 또는 로컬 워크스테이션 환경의 구조적 특성상, 모델의 추론 능력 못지않게 compute 자원 변수의 실시간적이고 정밀한 모니터링 체계 구축이 실험의 전체 신뢰성과 무결성을 좌우하는 핵심 축이 되어야 한다.

### **1\. E01\~E03 실험 변수 축의 현대적 재정의 (LLM 에이전트 중심)**

* **E01 (Task Accuracy & Format Sensitivity \- 작업 정확도 및 포맷 민감도)**  
  * **설계 수정 방향**: 과거 텍스트의 유창성이나 정성적 생성 품질을 평가하던 주관적 방식을 완전히 폐기해야 한다. 대신 BFCL V4 리더보드가 산업 표준으로 제시하고 있는 '구문 정확도(Abstract Syntax Tree, AST 평가 메커니즘)'를 실험의 가장 핵심적인 제1 평가 축으로 승격시켜야 한다.21  
  * **구체적 측정 지표**: 실험 파이프라인은 모델에게 시스템 프롬프트 형태로 제공된 복잡한 API 명세(Parameters, Type, Enums 등)를 바탕으로, 모델이 최종 반환한 JSON 또는 XML 객체가 문법적 치명상 없이 외부 코드 실행기에서 안전하게 파싱(Parsing) 가능한지를 이진법적으로 검증해야 한다(Format Sensitivity). 또한, 모델이 지시받지 않은 가상의 매개변수를 마음대로 창조해내는 '환각 매개변수(Hallucinated parameters)' 현상의 발현 빈도를 추적한다.24 단일 턴에서의 단순 호출과 여러 함수를 동시에 요청하는 병렬 함수 호출(Parallel call) 시나리오를 분리하여 가중치를 둔 성공률을 산출하는 것이 필수적이다.  
* **E02 (Multi-step Reasoning & Agentic Memory \- 다중 스텝 추론 및 맥락 유지력)**  
  * **설계 수정 방향**: 단발성 질문과 응답으로 구성된 독립된 Q\&A 형태의 정적인 실험 환경을 탈피해야 한다. 에이전트의 실제 작동 원리를 모사하여, 과거의 정보 상태(State)가 지속적으로 유지되고 누적되는 다중 턴 상호작용(Multi-turn interaction) 기반의 동적 환경으로 실험 스크립트를 재설계해야 한다.25  
  * **구체적 측정 지표**: 모델이 첫 번째 도구를 호출하여 외부 시스템으로부터 결과값을 반환받고 이를 다시 자신의 컨텍스트에 주입했을 때, 모델이 최초의 목적이나 과거의 맥락을 망각하지 않고 논리적 흐름에 맞는 다음 단계의 도구를 연쇄적으로 호출할 수 있는지(Agentic workflows)를 심층 평가한다.25 특히 대화 기록이 쌓여 누적 컨텍스트가 8K 임계점에 도달했을 때, 초기 지시사항을 무시하는 현상이나, 아무런 논리적 진전 없이 동일한 함수를 무한히 반복 호출하여 시스템 리소스를 고갈시키는 무한 루프(Infinite Loop) 발생 빈도를 강력한 페널티 지표로 기록해야 한다.27  
* **E03 (Resource Efficiency & Compute \- 자원 효율성 및 연산 성능)**  
  * **설계 수정 방향**: 오직 로컬 환경 검증만을 위해 존재하는 특화된 평가 축이다. 클라우드 모델 평가에서는 무시되지만, 8GB VRAM이라는 절대적인 물리적 임계점 내에서 모델이 보여주는 퍼포먼스와 연산 지연 사이의 처절한 트레이드오프(Trade-off) 궤적을 철저히 추적한다.  
  * **구체적 측정 지표**: GGUF Q4\_K\_M 양자화 수준에서 모델 가중치가 차지하는 디스크 물리 용량 대비 운영 체제가 실제로 할당하는 활성 VRAM 점유율의 팽창 비율을 분석한다. 또한 컨텍스트 윈도우가 늘어날 때마다 KV 캐시가 차지하는 메모리의 증가 기울기(Scaling slope)를 산출하고, 하드웨어의 소비 전력(Watt) 대비 모델이 뿜어내는 초당 토큰 생성 속도(Tokens Per Second)를 종합하여 자원 효율성 점수로 수치화한다.

### **2\. Compute 변수 측정 추가를 위한 파이프라인 방법론**

제한된 자원을 쥐어짜내는 로컬 환경에서의 극한 실험은 필연적으로 OOM 스파이크, 쓰레싱(Thrashing), 그리고 하드웨어 발열로 인한 스로틀링(Throttling)을 동반할 수밖에 없다. 따라서 프레임워크가 단순히 모델의 텍스트 응답 결과만을 수집하는 안일한 구조에서 벗어나, 운영 체제의 커널 및 프레임워크 하부 레벨에서 다음의 compute 관련 지표들을 실시간 1밀리초 단위로 수집하는 프로브(Probe)를 파이프라인에 이식해야 한다.

* **TTFT (Time To First Token) 및 TPS (Tokens Per Second)의 정밀 분리 측정**:  
  * **측정 방법**: Ollama API를 호출할 때 반환되는 JSON 응답 헤더 내부의 메타데이터 속성인 eval\_duration과 prompt\_eval\_duration을 명시적으로 파싱하거나, llama.cpp 엔진 구동 시 터미널로 출력되는 디버그 로그(--log-disable 해제)를 실시간 스트림으로 캡처한다. 이를 통해 모델이 방대한 프롬프트를 평가하고 이해하는 데 걸린 시간(Prompt processing)과, 첫 토큰 이후 실제 답변을 토해내는 생성 시간(Token generation)을 완벽히 분리하여 엑셀이나 데이터베이스에 기록한다. 이를 통해 컨텍스트가 길어질수록 프롬프트 연산 시간만이 기하급수적으로 늘어나는 특정 모델의 병목 지점을 정확히 식별할 수 있다.  
* **실시간 VRAM 스파이크 및 시스템 RAM 모니터링 체계 구축**:  
  * **측정 방법**: 실험을 주관하는 Python 기반의 자동화 스크립트 내부에 NVIDIA 관리 라이브러리인 pynvml을 임포트하거나, 운영 체제의 백그라운드에서 nvidia-smi \--query-gpu=memory.used \--format=csv \-l 1 커맨드를 서브프로세스 데몬으로 띄운다. 도구 호출 함수가 실행되며 컨텍스트 캐시가 가장 극단적으로 팽창하는 지점(최고 부하 시점)에서의 최대 메모리 스파이크(Peak VRAM)를 정확히 포착하고 기록하여 여유 메모리 마진을 분석한다.  
* **KV Cache 스케일링 동적 추적**:  
  * **측정 방법**: 모델 실행 파라미터 중 컨텍스트 윈도우 변수(ctx\_size 또는 num\_ctx)를 초기 2K부터 시작하여 4K, 8K로 2배수씩 점진적으로 증가시키며 모델을 반복 로드하는 스크립트를 작성한다. 이때 할당되는 compute 메모리 증가량을 선형 그래프로 플롯(Plot)하여, 해당 모델이 채택한 어텐션 메커니즘(예: Flash Attention 적용 여부, Group Query Attention 효율 등)이 로컬 메모리를 얼마나 영리하게 압축하고 있는지 그 효율성을 정량적으로 도출한다.

### **3\. 모델 비교를 오염시키는 유의미한 방법론적 함정 (Methodological Pitfalls)**

아무리 정교하게 설계된 평가 축을 갖추었다 하더라도, 로컬 환경의 특수성을 간과한 채 실험을 진행할 경우 벤치마크 결과의 무결성을 심각하고도 돌이킬 수 없이 훼손할 수 있는 몇 가지 기술적 함정들이 도사리고 있다. 다음의 변수들은 실험 통제군에서 반드시 사전 차단되어야 한다.

* **함정 A: 메모리 누수(Memory Leak)에 의한 누적 VRAM 팽창 및 서버 크래시**  
  * 최근 글로벌 커뮤니티에 보고된 Gemma 3 계열(12B 및 4B) 모델의 오픈 소스 실험 사례들에 따르면, 단일 환경에서 도구 호출 구동이 여러 차례 반복될수록 운영 체제의 시스템 RAM과 GPU의 VRAM 사용량이 반환되지 않고 지속적으로 누적 증가하는 치명적 현상이 발견되었다.45 이는 최종적으로 Ollama 서버 프로세스 전체의 강제 종료(Crash)를 유발한다. 따라서 다중 턴 벤치마크를 무인으로 자동화할 때, 매 실험 세션이 종료될 때마다 즉각적으로 이전 세션의 캐시를 해제하고 명시적인 모델 언로드(Unload) 과정을 삽입하는 커스텀 로직이 스크립트에 반드시 포함되어야만 벤치마크의 연속성을 보장할 수 있다.  
* **함정 B: 템플릿 충돌 메커니즘 및 이중 특수 토큰(Double \<bos\>) 주입 문제**  
  * Ollama나 llama.cpp와 같은 로컬 프레임워크가 모델을 파싱하여 구동할 때, 프레임워크 자체 로직에 의해 문장의 시작을 알리는 시작 토큰(\<bos\>, Begin of Sentence)을 강제로 추가하는 기능이 작동한다. 그런데 모델 제작사(예: Google DeepMind)가 정의한 자체 Chat template 내부에 이미 \<bos\> 토큰이 하드코딩되어 있을 경우, 두 메커니즘이 충돌하여 프롬프트의 맨 앞에 이중으로 토큰이 삽입되는 현상이 발생한다. 특히 Gemma 3 모델 라인업의 경우 이중 \<bos\> 토큰이 주입되면 모델의 주의력 텐서가 완전히 붕괴되어 사용자의 지시를 무시하거나 심각한 환각을 일으키는 버그가 존재한다.41 실험 데이터를 수집하기 전, 반드시 모델의 내부 템플릿 정합성을 사전 디버깅을 통해 철저히 검증해야 한다.  
* **함정 C: 하드웨어 전력 제한(TDP) 스로틀링에 의한 생성 지연율 데이터 왜곡**  
  * 제한된 워크스테이션 환경에서 Phi-4-reasoning 모델 등을 구동한 특정 이슈 리포트에 따르면, 운영 체제의 nvidia-smi 모니터링 상으로는 GPU 로드율이 100%에 도달한 것으로 표기됨에도 불구하고 하드웨어의 실제 물리적 전력 소모는 50W(해당 GPU의 TDP 한계인 165W에 한참 못 미치는 수치)에 불과하며, 단일 응답을 반환하는 데 무려 30분 이상이 소요되는 극단적인 병목 현상이 보고된 바 있다.17 이는 프레임워크 내부의 특정 커널 연산이 극도로 비효율적이거나 CPU와 GPU 간의 PCI-E 데이터 전송 병목에 기인한 것으로 풀이된다. 따라서 모델 간의 TPS(초당 토큰 생성 속도)를 단순히 텍스트 출력 시간만으로 비교해서는 안 되며, 하드웨어 센서에서 추출한 실제 전력 소모량(Power Draw) 로그 수치를 대조하여 벤치마크 점수에 스로틀링이나 드라이버 버그로 인한 왜곡이 개입되지 않았는지 교차 검증하는 과정이 필수적이다.  
* **함정 D: 시스템 프롬프트 변형에 따른 도구 호출 지능의 극단적 하락 (Prompt Variation)**  
  * 버클리 대학의 BFCL 연구팀이 발표한 프롬프트 민감도 논문에 따르면, 완전히 동일한 가중치를 지닌 모델이라도 도구의 사양과 명세서가 마크다운(Markdown), XML 태그, 또는 아무런 포맷이 없는 플레인 텍스트(Plain text) 중 어떤 형태로 제공되느냐에 따라 도구 호출의 성공률이 수십 퍼센트 이상 극심하게 요동치는 현상이 확인되었다.24 특히 8B 이하의 소형 로컬 모델들은 지능의 여유분이 적어 이러한 포맷 민감도에 치명적인 영향을 받는다. 따라서 다수의 로컬 모델을 실험대에 올려 횡단 비교(Cross-sectional comparison)를 수행할 때는, 외부에서 주입하는 도구 명세 제공 프롬프트를 철저히 단일한 포맷 규칙(예: OpenAI 호환 JSON 스키마 형식)으로 강제 고정하는 강력한 통제 변수 설정이 실험 설계의 첫 단추가 되어야 한다.  
* ---

  1 블로그 게시물, "Ollama VRAM Requirements for Local LLMs", LocalLLM.in, 날짜 미상, [https://localllm.in/blog/ollama-vram-requirements-for-local-llms](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)  
* 5 기술 블로그, "A formula that predicts GGUF VRAM usage from GPU layers and context length", Oobabooga Github IO, 날짜 미상, [https://oobabooga.github.io/blog/posts/gguf-vram-formula/](https://oobabooga.github.io/blog/posts/gguf-vram-formula/)  
* 12 커뮤니티 토론 데이터, "Tested some popular GGUFs for 16GB VRAM target", Reddit r/LocalLLM (Living-Interview-633), 약 2025년 작성 추정, [https://www.reddit.com/r/LocalLLM/comments/1if3vn3/tested\_some\_popular\_ggufs\_for\_16gb\_vram\_target/](https://www.reddit.com/r/LocalLLM/comments/1if3vn3/tested_some_popular_ggufs_for_16gb_vram_target/)  
* 18 플랫폼 기술 리뷰, "Ollama Models List 2025: 100+ Models Compared", Skywork AI (Dora), 2025년, [https://skywork.ai/blog/llm/ollama-models-list-2025-100-models-compared/](https://skywork.ai/blog/llm/ollama-models-list-2025-100-models-compared/)  
* 33 로컬 모델 라이브러리 디렉토리, "Ollama Library \- Qwen2.5 / Qwen3 / Llama3 / Gemma2 등", Ollama, 지속 업데이트, [https://ollama.com/library](https://ollama.com/library)  
* 9 기업 제공 자체 벤치마크 보드, "Self-Hosted LLMs — 2026 Rankings", Onyx App (Roshan Desai), 2026년 3월 12일 업데이트 추정, [https://onyx.app/self-hosted-llm-leaderboard](https://onyx.app/self-hosted-llm-leaderboard)  
* 10 온라인 리더보드 점수표, "Berkeley Function Calling Leaderboard (Score Data)", Berkeley CS Gorilla LLM, 지속 업데이트, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
* 43 학술 논문 및 연구 초록, "The Place of the FFM in Personality Psychology", ResearchGate, 2002년 1월, [https://www.researchgate.net/publication/232854240\_The\_Place\_of\_the\_FFM\_in\_Personality\_Psychology](https://www.researchgate.net/publication/232854240_The_Place_of_the_FFM_in_Personality_Psychology)  
* 13 공식 릴리스 노트 기술 문서, "Gemma 3 release date and variants", Google AI Developers, 2025년 3월 10일, [https://ai.google.dev/gemma/docs/releases](https://ai.google.dev/gemma/docs/releases)  
* 37 백과사전 항목, "Gemma (language model)", Wikipedia, 2025년 3월 12일 안정화 버전 릴리스 등 기록, [https://en.wikipedia.org/wiki/Gemma\_(language\_model](https://en.wikipedia.org/wiki/Gemma_\(language_model\))  
* 4 하드웨어 요구사항 계산 데이터베이스, "Llama 3.1 8B Q4\_K\_M GGUF size VRAM requirements", APXML 시스템 도구, 날짜 미상, [https://apxml.com/models/llama-3-1-8b](https://apxml.com/models/llama-3-1-8b)  
* 1 심층 분석 블로그, "How much VRAM do I need to run Ollama models locally?", LocalLLM.in, 날짜 미상, [https://localllm.in/blog/ollama-vram-requirements-for-local-llms](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)  
* 6 모델 가중치 파일 레포지토리 정보, "Meta-Llama-3.1-8B-Instruct-GGUF Repository Details", Hugging Face (SanctumAI 제공), 날짜 미상, [https://huggingface.co/SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF)  
* 8 시스템 메모리 이슈 보고 토론, "Amount of ram Qwen 2.5-7B-1M takes?", Reddit r/LocalLLaMA 커뮤니티, 날짜 미상, [https://www.reddit.com/r/LocalLLaMA/comments/1j79o3l/amount\_of\_ram\_qwen\_257b1m\_takes/](https://www.reddit.com/r/LocalLLaMA/comments/1j79o3l/amount_of_ram_qwen_257b1m_takes/)  
* 2 모델 가중치 및 양자화 스펙 시트, "Llamacpp imatrix Quantizations of Qwen2.5-Coder-7B-Instruct", Hugging Face (Bartowski 제공), 날짜 미상, [https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF](https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF)  
* 3 기술 인프라 튜토리얼 문서, "Running Full Qwen 2.5 Series with GPUStack", GPUStack.ai, 2024년 9월 29일, [https://gpustack.ai/running-full-qwen-2-5-series/](https://gpustack.ai/running-full-qwen-2-5-series/)  
* 29 코딩 목적 모델 추천 질의응답, "For 12GB VRAM what Qwen model is best for coding?", Reddit r/LocalLLaMA 커뮤니티, 약 2025년 추정, [https://www.reddit.com/r/LocalLLaMA/comments/1gtbtfl/for\_12gb\_vram\_what\_qwen\_model\_is\_best\_for\_coding/](https://www.reddit.com/r/LocalLLaMA/comments/1gtbtfl/for_12gb_vram_what_qwen_model_is_best_for_coding/)  
* 15 모델 가중치 레포지토리, "phi-4-GGUF", Hugging Face (Bartowski 제공), 날짜 미상, [https://huggingface.co/bartowski/phi-4-GGUF](https://huggingface.co/bartowski/phi-4-GGUF)  
* 16 메모리 점유 경험 토론, "Qwen 14b on 18gb of vram", Reddit r/LocalLLaMA 커뮤니티, 날짜 미상, [https://www.reddit.com/r/LocalLLaMA/comments/1gosrzh/qwen\_14b\_on\_18gb\_of\_vram/](https://www.reddit.com/r/LocalLLaMA/comments/1gosrzh/qwen_14b_on_18gb_of_vram/)  
* 17 오픈소스 이슈 트래킹 리포트, "Phi4-reasoning 14b VRAM and Power issue", Github Ollama Issues (\#10612), 날짜 미상, [https://github.com/ollama/ollama/issues/10612](https://github.com/ollama/ollama/issues/10612)  
* 7 종합 기술 동향 리뷰 기사, "Best Local LLM Models 2026", SitePoint, 날짜 미상, [https://www.sitepoint.com/best-local-llm-models-2026/](https://www.sitepoint.com/best-local-llm-models-2026/)  
* 45 소프트웨어 버그 트래커, "Gemma 3 memory usage bug", Github Ollama Issues (\#10341), 날짜 미상, [https://github.com/ollama/ollama/issues/10341](https://github.com/ollama/ollama/issues/10341)  
* 41 기술 가이드 및 사용자 커뮤니티 토론, "Gemma 3 GGUFs recommended settings (Unsloth 팀 권고 포함)", Reddit r/LocalLLaMA, 약 2025년 작성 추정, [https://www.reddit.com/r/LocalLLaMA/comments/1j9hsfc/gemma\_3\_ggufs\_recommended\_settings/](https://www.reddit.com/r/LocalLLaMA/comments/1j9hsfc/gemma_3_ggufs_recommended_settings/)  
* 14 하드웨어 아키텍처 토론, "Why didn't they design Gemma3 to fit in GPU memory?", Reddit r/Ollama, 날짜 미상, [https://www.reddit.com/r/ollama/comments/1jbwwxh/why\_didnt\_they\_design\_gemma3\_to\_fit\_in\_gpu\_memory/](https://www.reddit.com/r/ollama/comments/1jbwwxh/why_didnt_they_design_gemma3_to_fit_in_gpu_memory/)  
* 30 공식 모델 페이지 스펙 데이터, "Google Gemma-3-4b-it", Hugging Face, 날짜 미상, [https://huggingface.co/google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it)  
* 46 메모리 과다 소모 증상 보고서, "Gemma3 12B uses excessive memory", Reddit r/Ollama, 약 2025년 작성 추정, [https://www.reddit.com/r/ollama/comments/1jaydvn/gemma3\_12b\_uses\_excessive\_memory/](https://www.reddit.com/r/ollama/comments/1jaydvn/gemma3_12b_uses_excessive_memory/)  
* 20 기술 트렌드 코멘터리, "Ollama tool calling native JSON schema", Bluesky 프로필(dottxtai), 날짜 미상, [https://bsky.app/profile/dottxtai.bsky.social](https://bsky.app/profile/dottxtai.bsky.social)  
* 21 리더보드 아키텍처 공식 소개 블로그, "Berkeley Function Calling Leaderboard", Berkeley CS Gorilla LLM, 지속 업데이트, [https://gorilla.cs.berkeley.edu/blogs/8\_berkeley\_function\_calling\_leaderboard.html](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)  
* 25 오픈소스 프로젝트 릴리스 체인지로그, "BFCL Changelog (V4 Release 및 카테고리 개편 상세)", Github (ShishirPatil/gorilla 프로젝트), 2025년 7월 17일, [https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md](https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md)  
* 10 벤치마크 원시 데이터 보드, "Leaderboard Scores", Berkeley CS, 날짜 미상, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
* 23 리더보드 대시보드 홈, "Berkeley Function Calling Leaderboard (BFCL) V4 메인 페이지", Berkeley CS, 최종 업데이트 2025년 12월 16일, [https://gorilla.cs.berkeley.edu/leaderboard.html?ref=blog.langchain.com](https://gorilla.cs.berkeley.edu/leaderboard.html?ref=blog.langchain.com)  
* 10 벤치마크 점수 테이블 캡처본, "Leaderboard Scores Data Segment", Berkeley CS, 날짜 미상, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
* 25 벤치마크 변경 이력, "BFCL Agentic Domain Update Log", Github (ShishirPatil/gorilla 프로젝트), 날짜 미상, [https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md](https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md)  
* 26 학술 컨퍼런스 피어 리뷰 및 저자 반박문, "Rebuttal by Authors (BFCL Single-turn vs Agentic memory)", OpenReview, 2025년 4월 및 6월 수정, [https://openreview.net/forum?id=2GmDdhBdDk](https://openreview.net/forum?id=2GmDdhBdDk)  
* 38 프레임워크 모델 스펙 가이드, "Ollama Library \- Gemma 3 지원 세부 사항 및 벤치마크 결과", Ollama, 날짜 미상, [https://ollama.com/library/gemma3](https://ollama.com/library/gemma3)  
* 31 커스텀 모델 구현 지침서, "Ollama orieg/gemma3-tools:12b Modelfile 설정", Ollama, 날짜 미상, [https://ollama.com/orieg/gemma3-tools:12b](https://ollama.com/orieg/gemma3-tools:12b)  
* 22 사용자 주도 기술 가이드, "Giving native tool calling to Gemma 3 or really any model", Reddit r/LocalLLaMA, 약 2025년 작성 추정, [https://www.reddit.com/r/LocalLLaMA/comments/1jauy8d/giving\_native\_tool\_calling\_to\_gemma\_3\_or\_really/](https://www.reddit.com/r/LocalLLaMA/comments/1jauy8d/giving_native_tool_calling_to_gemma_3_or_really/)  
* 34 클라우드 개발 환경 플랫폼 AI 카탈로그, "Puter Developer AI Models (Qwen 2.5 Coder 7B 명세)", Puter Developer, 날짜 미상, [https://developer.puter.com/ai/models/](https://developer.puter.com/ai/models/)  
* 27 오픈소스 모델 테스트 결과 모음 리포지토리, "AI App Community Model Popular \- Qwen 2.5 Coder 7B 코딩 성능 비교", Github (uptonking 프로젝트), 날짜 미상, [https://github.com/uptonking/note4yaoo/blob/main/lib-ai-app-community-model-popular.md](https://github.com/uptonking/note4yaoo/blob/main/lib-ai-app-community-model-popular.md)  
* 11 아카이브 등록 학술 논문, "EGPO-4B Model Performance on BFCL", Arxiv (초록 2508.05118v4), 날짜 미상, [https://arxiv.org/html/2508.05118v4](https://arxiv.org/html/2508.05118v4)  
* 10 모델 벤치마크 성과 비교 보드, "Llama-3.1-8B-Instruct (Prompt) BFCL V4 Scores", Berkeley CS, 날짜 미상, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
* 24 프롬프트 엔지니어링 및 성능 연구 블로그, "BFCL V4 Prompt Variation Analysis (포맷 민감도 분석)", Berkeley CS Gorilla LLM, 날짜 미상, [https://gorilla.cs.berkeley.edu/blogs/17\_bfcl\_v4\_prompt\_variation.html](https://gorilla.cs.berkeley.edu/blogs/17_bfcl_v4_prompt_variation.html)  
* 28 엔터프라이즈 AI 플랫폼 성능 집계표, "Vellum LLM Leaderboard", Vellum.ai, 날짜 미상, [https://vellum.ai/llm-leaderboard](https://vellum.ai/llm-leaderboard)  
* 35 허깅페이스 모델 카드 및 배포 지침, "Meta-Llama-3.1-8B Model Guide", Hugging Face (Meta 제공), 날짜 미상, [https://huggingface.co/meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)  
* 36 아카이브 등록 학술 논문 및 부록 데이터, "RULER benchmark context length evaluation (Phi-4 언급)", Arxiv (초록 2507.11407v1), 날짜 미상, [https://arxiv.org/html/2507.11407v1](https://arxiv.org/html/2507.11407v1)  
* 19 신규 모델 기술 검증 보고서, "Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs", ResearchGate 커뮤니티 등재본, 2025년, [https://www.researchgate.net/publication/389581742\_Phi-4-Mini\_Technical\_Report\_Compact\_yet\_Powerful\_Multimodal\_Language\_Models\_via\_Mixture-of-LoRAs](https://www.researchgate.net/publication/389581742_Phi-4-Mini_Technical_Report_Compact_yet_Powerful_Multimodal_Language_Models_via_Mixture-of-LoRAs)  
* 10 벤치마크 결과 집계 테이블, "Gemma-3-4b-it (Prompt) BFCL V4 Score", Berkeley CS, 날짜 미상, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
* 44 컨퍼런스 기고 학술 문서(초안본), "BFCL Benchmark on Gemma-3-4b-it AST evaluation", OpenReview, 2025년, [https://openreview.net/pdf?id=2GmDdhBdDk](https://openreview.net/pdf?id=2GmDdhBdDk)  
* 42 아카이브 등록 학술 논문, "Agent Architecture Evaluation (Gemma-3-4B on BFCL)", Arxiv (초록 2603.08640v1), 2025년, [https://arxiv.org/html/2603.08640v1](https://arxiv.org/html/2603.08640v1)  
* 39 구글 개발자 공식 개발 문서, "Function calling capability in Gemma 3", Google AI Developers, 날짜 미상, [https://ai.google.dev/gemma/docs/capabilities/function-calling](https://ai.google.dev/gemma/docs/capabilities/function-calling)  
* 40 구글 혁신 및 기술 블로그 게시물, "Introducing FunctionGemma: Technology for Developers", Google Blog, 날짜 미상, [https://blog.google/innovation-and-ai/technology/developers-tools/functiongemma/](https://blog.google/innovation-and-ai/technology/developers-tools/functiongemma/)  
* 32 오픈소스 프로젝트 저장소, "gemma3-ollama-tools: Unlocking tool-calling", Github (IllFil 개발), 날짜 미상, [https://github.com/IllFil/gemma3-ollama-tools](https://github.com/IllFil/gemma3-ollama-tools)

#### **참고 자료**

1. Ollama VRAM Requirements: Complete 2026 Guide to GPU Memory for Local LLMs, 3월 19, 2026에 액세스, [https://localllm.in/blog/ollama-vram-requirements-for-local-llms](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)  
2. bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF](https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF)  
3. Running Full Qwen 2.5 Series – Performance and Resource Allocation Review, 3월 19, 2026에 액세스, [https://gpustack.ai/running-full-qwen-2-5-series/](https://gpustack.ai/running-full-qwen-2-5-series/)  
4. Llama 3.1 8B: Specifications and GPU VRAM Requirements \- ApX Machine Learning, 3월 19, 2026에 액세스, [https://apxml.com/models/llama-3-1-8b](https://apxml.com/models/llama-3-1-8b)  
5. A formula that predicts GGUF VRAM usage from GPU layers and context length, 3월 19, 2026에 액세스, [https://oobabooga.github.io/blog/posts/gguf-vram-formula/](https://oobabooga.github.io/blog/posts/gguf-vram-formula/)  
6. SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF)  
7. Best Local LLM Models 2026 | Developer Comparison \- SitePoint, 3월 19, 2026에 액세스, [https://www.sitepoint.com/best-local-llm-models-2026/](https://www.sitepoint.com/best-local-llm-models-2026/)  
8. Amount of ram Qwen 2.5-7B-1M takes? : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1j79o3l/amount\_of\_ram\_qwen\_257b1m\_takes/](https://www.reddit.com/r/LocalLLaMA/comments/1j79o3l/amount_of_ram_qwen_257b1m_takes/)  
9. Best Self-Hosted LLM Leaderboard 2026 | Open-Weight Model Rankings for Enterprise, 3월 19, 2026에 액세스, [https://onyx.app/self-hosted-llm-leaderboard](https://onyx.app/self-hosted-llm-leaderboard)  
10. Berkeley Function Calling Leaderboard (BFCL) V4 \- Gorilla LLM, 3월 19, 2026에 액세스, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
11. Reasoning through Exploration: A Reinforcement Learning Framework for Robust Function Calling \- arXiv, 3월 19, 2026에 액세스, [https://arxiv.org/html/2508.05118v4](https://arxiv.org/html/2508.05118v4)  
12. Tested some popular GGUFs for 16GB VRAM target : r/LocalLLM \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLM/comments/1if3vn3/tested\_some\_popular\_ggufs\_for\_16gb\_vram\_target/](https://www.reddit.com/r/LocalLLM/comments/1if3vn3/tested_some_popular_ggufs_for_16gb_vram_target/)  
13. Gemma releases | Google AI for Developers, 3월 19, 2026에 액세스, [https://ai.google.dev/gemma/docs/releases](https://ai.google.dev/gemma/docs/releases)  
14. Why didn't they design gemma3 to fit in GPU memory more efficiently? : r/ollama \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/ollama/comments/1jbwwxh/why\_didnt\_they\_design\_gemma3\_to\_fit\_in\_gpu\_memory/](https://www.reddit.com/r/ollama/comments/1jbwwxh/why_didnt_they_design_gemma3_to_fit_in_gpu_memory/)  
15. bartowski/phi-4-GGUF \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/bartowski/phi-4-GGUF](https://huggingface.co/bartowski/phi-4-GGUF)  
16. Qwen 14b on 18gb of VRAM? : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1gosrzh/qwen\_14b\_on\_18gb\_of\_vram/](https://www.reddit.com/r/LocalLLaMA/comments/1gosrzh/qwen_14b_on_18gb_of_vram/)  
17. phi4-reasoning:14b-q4\_K\_M extremely slow compared to other 14B models \#10612, 3월 19, 2026에 액세스, [https://github.com/ollama/ollama/issues/10612](https://github.com/ollama/ollama/issues/10612)  
18. Ollama Models List 2025: 100+ Models Compared \- Skywork.ai, 3월 19, 2026에 액세스, [https://skywork.ai/blog/llm/ollama-models-list-2025-100-models-compared/](https://skywork.ai/blog/llm/ollama-models-list-2025-100-models-compared/)  
19. (PDF) Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs \- ResearchGate, 3월 19, 2026에 액세스, [https://www.researchgate.net/publication/389581742\_Phi-4-Mini\_Technical\_Report\_Compact\_yet\_Powerful\_Multimodal\_Language\_Models\_via\_Mixture-of-LoRAs](https://www.researchgate.net/publication/389581742_Phi-4-Mini_Technical_Report_Compact_yet_Powerful_Multimodal_Language_Models_via_Mixture-of-LoRAs)  
20. .txt (@dottxtai.bsky.social) — Bluesky, 3월 19, 2026에 액세스, [https://bsky.app/profile/dottxtai.bsky.social](https://bsky.app/profile/dottxtai.bsky.social)  
21. Berkeley Function Calling Leaderboard \- Gorilla LLM, 3월 19, 2026에 액세스, [https://gorilla.cs.berkeley.edu/blogs/8\_berkeley\_function\_calling\_leaderboard.html](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)  
22. Giving "native" tool calling to Gemma 3 (or really any model) : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1jauy8d/giving\_native\_tool\_calling\_to\_gemma\_3\_or\_really/](https://www.reddit.com/r/LocalLLaMA/comments/1jauy8d/giving_native_tool_calling_to_gemma_3_or_really/)  
23. Berkeley Function Calling Leaderboard (BFCL) V4 \- Gorilla LLM, 3월 19, 2026에 액세스, [https://gorilla.cs.berkeley.edu/leaderboard.html?ref=blog.langchain.com](https://gorilla.cs.berkeley.edu/leaderboard.html?ref=blog.langchain.com)  
24. BFCL V4 • Agentic Part 3: Evaluating Format Sensitivity for Tool Calls, 3월 19, 2026에 액세스, [https://gorilla.cs.berkeley.edu/blogs/17\_bfcl\_v4\_prompt\_variation.html](https://gorilla.cs.berkeley.edu/blogs/17_bfcl_v4_prompt_variation.html)  
25. gorilla/berkeley-function-call-leaderboard/CHANGELOG.md at main \- GitHub, 3월 19, 2026에 액세스, [https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md](https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md)  
26. The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models | OpenReview, 3월 19, 2026에 액세스, [https://openreview.net/forum?id=2GmDdhBdDk](https://openreview.net/forum?id=2GmDdhBdDk)  
27. note4yaoo/lib-ai-app-community-model-popular.md at main \- GitHub, 3월 19, 2026에 액세스, [https://github.com/uptonking/note4yaoo/blob/main/lib-ai-app-community-model-popular.md](https://github.com/uptonking/note4yaoo/blob/main/lib-ai-app-community-model-popular.md)  
28. LLM Leaderboard \- Vellum AI, 3월 19, 2026에 액세스, [https://vellum.ai/llm-leaderboard](https://vellum.ai/llm-leaderboard)  
29. For 12gb Vram, what Qwen model is best for coding? : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1gtbtfl/for\_12gb\_vram\_what\_qwen\_model\_is\_best\_for\_coding/](https://www.reddit.com/r/LocalLLaMA/comments/1gtbtfl/for_12gb_vram_what_qwen_model_is_best_for_coding/)  
30. google/gemma-3-4b-it \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it)  
31. orieg/gemma3-tools:12b \- Ollama, 3월 19, 2026에 액세스, [https://ollama.com/orieg/gemma3-tools:12b](https://ollama.com/orieg/gemma3-tools:12b)  
32. IllFil/gemma3-ollama-tools: This project shows how to ... \- GitHub, 3월 19, 2026에 액세스, [https://github.com/IllFil/gemma3-ollama-tools](https://github.com/IllFil/gemma3-ollama-tools)  
33. library \- Ollama, 3월 19, 2026에 액세스, [https://ollama.com/library](https://ollama.com/library)  
34. AI Models \- Puter Developer, 3월 19, 2026에 액세스, [https://developer.puter.com/ai/models/](https://developer.puter.com/ai/models/)  
35. meta-llama/Llama-3.1-8B \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)  
36. EXAONE 4.0: Unified Large Language Models Integrating Non-reasoning and Reasoning Modes \- arXiv, 3월 19, 2026에 액세스, [https://arxiv.org/html/2507.11407v1](https://arxiv.org/html/2507.11407v1)  
37. Gemma (language model) \- Wikipedia, 3월 19, 2026에 액세스, [https://en.wikipedia.org/wiki/Gemma\_(language\_model)](https://en.wikipedia.org/wiki/Gemma_\(language_model\))  
38. gemma3 \- Ollama, 3월 19, 2026에 액세스, [https://ollama.com/library/gemma3](https://ollama.com/library/gemma3)  
39. Function calling with Gemma | Google AI for Developers, 3월 19, 2026에 액세스, [https://ai.google.dev/gemma/docs/capabilities/function-calling](https://ai.google.dev/gemma/docs/capabilities/function-calling)  
40. FunctionGemma: Bringing bespoke function calling to the edge \- Google Blog, 3월 19, 2026에 액세스, [https://blog.google/innovation-and-ai/technology/developers-tools/functiongemma/](https://blog.google/innovation-and-ai/technology/developers-tools/functiongemma/)  
41. Gemma 3 \- GGUFs \+ recommended settings : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1j9hsfc/gemma\_3\_ggufs\_recommended\_settings/](https://www.reddit.com/r/LocalLLaMA/comments/1j9hsfc/gemma_3_ggufs_recommended_settings/)  
42. PostTrainBench: Can LLM Agents Automate LLM Post-Training? \- arXiv.org, 3월 19, 2026에 액세스, [https://arxiv.org/html/2603.08640v1](https://arxiv.org/html/2603.08640v1)  
43. The Place of the FFM in Personality Psychology \- ResearchGate, 3월 19, 2026에 액세스, [https://www.researchgate.net/publication/232854240\_The\_Place\_of\_the\_FFM\_in\_Personality\_Psychology](https://www.researchgate.net/publication/232854240_The_Place_of_the_FFM_in_Personality_Psychology)  
44. The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models \- OpenReview, 3월 19, 2026에 액세스, [https://openreview.net/pdf?id=2GmDdhBdDk](https://openreview.net/pdf?id=2GmDdhBdDk)  
45. Gemma 3 12b (Q4\_K\_M) fills system RAM despite available VRAM (OLLAMA 0.6.5) \#10341, 3월 19, 2026에 액세스, [https://github.com/ollama/ollama/issues/10341](https://github.com/ollama/ollama/issues/10341)  
46. Gemma3 12B uses excessive memory. : r/ollama \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/ollama/comments/1jaydvn/gemma3\_12b\_uses\_excessive\_memory/](https://www.reddit.com/r/ollama/comments/1jaydvn/gemma3_12b_uses_excessive_memory/)