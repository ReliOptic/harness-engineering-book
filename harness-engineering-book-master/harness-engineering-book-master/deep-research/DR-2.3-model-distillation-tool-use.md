# **DR-2.3 Ch.2 대규모 언어 모델의 증류 및 양자화가 도구 호출 안정성 및 함수 호출 정확도에 미치는 영향 분석**

## **1\. 서론: DR-2.3 설계 요건과 대규모 언어 모델 압축의 필연성**

현대의 인공지능 시스템은 단순한 텍스트 생성을 넘어 외부 애플리케이션 프로그래밍 인터페이스(API), 데이터베이스, 소프트웨어 도구와 실시간으로 상호작용하는 자율형 에이전트(Autonomous Agent)로 진화하고 있다.1 이러한 에이전트 아키텍처의 핵심 기저는 사용자의 자연어 질의를 분석하여 적절한 외부 도구를 선택하고, 해당 도구의 실행에 필요한 매개변수(Parameter)를 엄격한 구문 규칙에 맞추어 생성하는 '함수 호출(Function Calling)' 및 '도구 호출(Tool Calling)' 능력에 있다.1 복잡한 시스템 설계 요구사항을 정의하는 DR-2.3(Design Requirement 2.3)은 사용자 경험을 저해하지 않는 원활한 시뮬레이션 및 상호작용 환경을 보장하기 위해 시스템의 안정성, 응답성, 그리고 명령 처리의 명확성을 최우선 과제로 규정하고 있다.4

그러나 수백억에서 수천억 개의 파라미터를 지닌 고성능 대규모 언어 모델(LLM)을 클라우드 혹은 엣지(Edge) 디바이스에 배포하여 DR-2.3의 응답성 요건을 충족시키는 것은 물리적인 한계에 직면한다.3 완전 정밀도(Full-precision) 모델은 막대한 그래픽 처리 장치(GPU) 메모리를 요구하며, 함수 호출 과정에서 발생하는 토큰 생성의 지연 시간(Latency)은 피크 시간대에 2\~3초를 초과하여 사용자 경험을 심각하게 훼손한다.7 이를 극복하기 위해 산업계와 학계는 모델 증류(Model Distillation)와 양자화(Quantization)라는 두 가지 강력한 모델 압축 기술을 표준으로 채택하고 있다.9

모델 증류는 거대한 교사 모델(Teacher Model)이 지닌 복잡한 추론 패턴과 도구 호출 지식을 상대적으로 파라미터 수가 적은 학생 모델(Student Model)로 이전하는 기법이다.12 반면, 양자화는 모델의 가중치(Weight)와 활성화 함수(Activation)를 표현하는 부동소수점 데이터 타입을 FP16(16-bit)이나 FP32에서 INT8, INT4, 혹은 NVFP4와 같은 저비트(Low-bit) 정수 또는 특수 부동소수점 포맷으로 압축하여 메모리 풋프린트를 물리적으로 축소하는 기법이다.14 일반적인 자연어 처리(NLP) 벤치마크에서는 이러한 압축 기술들이 베이스라인 모델의 성능을 거의 손실 없이 보존하는 것으로 보고되어 왔다.18

하지만 도구 호출과 함수 호출은 본질적으로 구조화된 데이터(주로 JSON 형식)를 다루며, 단 하나의 괄호나 따옴표 누락조차 전체 시스템의 치명적인 구문 오류(Syntax Error)로 이어지는 고도의 취약성을 지닌다.19 본 장에서는 DR-2.3의 안정성 및 정확도 요건을 충족하기 위해, 모델 증류와 양자화가 LLM의 도구 호출 메커니즘에 가하는 비선형적인 파괴 현상과 이를 복구하기 위한 최신 학술적 접근법을 심층적으로 분석한다.

## **2\. 함수 호출 정확도의 평가 메커니즘과 지표의 한계**

압축된 대규모 언어 모델의 도구 호출 능력을 분석하기 위해서는 모델의 출력물을 평가하는 엄밀한 기준이 선행되어야 한다. 함수 호출의 평가는 단순한 텍스트 유사도 측정을 넘어, 코딩 및 컴파일러 수준의 구조적 무결성 검증을 요구한다.1

### **2.1. 추상 구문 트리(AST) 기반의 다단계 검증 아키텍처**

최신 연구 및 산업 표준은 함수 호출의 정확도를 검증하기 위해 추상 구문 트리(Abstract Syntax Tree, AST)를 활용한 다단계 파이프라인을 구축하고 있다.1 이 파이프라인의 첫 번째 단계는 구문 분석기(JSON Parser)를 통해 생성된 출력물이 JSON 포맷의 문법적 유효성을 갖추고 있는지 확인하는 것이다. 쉼표의 누락이나 이스케이프 문자의 오작동 등으로 인해 직렬화(Deserialization)가 불가능한 경우, 이 단계에서 즉각적인 실패로 처리된다.19

구문적 유효성이 확인되면, 두 번째 단계인 '함수 매칭(Function Matching)'이 수행된다. 이는 모델이 사용자의 질의에 응답하기 위해 선택한 API나 도구의 이름이 주어진 환경 맥락에서 논리적으로 타당한지, 그리고 정답 집합에 포함되어 있는지를 평가한다.1 세 번째 단계는 '매개변수 매칭(Parameter Matching)'으로, 가장 엄격하고 세밀한 검증이 이루어지는 구간이다. 이 단계에서는 AST 노드와 리프(Leaf)를 순회하며 각 필수 매개변수(Required Parameter)가 누락 없이 존재하는지, 해당 매개변수의 데이터 타입(문자열, 정수형, 배열 등)이 일치하는지, 그리고 할당된 실제 값(Value)이 의미론적으로 정확한지를 교차 검증한다.1 단 하나의 매개변수라도 타입이 어긋나거나 환각(Hallucination)에 기반한 값이 삽입될 경우, 전체 도구 호출은 실패한 것으로 간주된다.

### **2.2. 버클리 함수 호출 리더보드(BFCL)와 도메인 복잡성**

위와 같은 AST 기반 검증 체계를 대규모로 집대성한 벤치마크가 바로 버클리 함수 호출 리더보드(Berkeley Function Calling Leaderboard, BFCL)이다.22 BFCL은 모델이 다양한 프로그래밍 언어(Java, JavaScript, Python 등)와 REST API 환경에서 도구를 어떻게 다루는지 2,000개 이상의 질의-함수-응답 트리플렛을 통해 측정한다.24

단일 함수 호출의 경우 압축된 오픈소스 로컬 모델들도 독점적 거대 모델(Proprietary Models)에 필적하는 성능을 보여주지만, 시스템의 복잡도가 증가함에 따라 극명한 성능 격차가 발생한다.24 다중 함수 호출(Multiple Function Calls)이나 병렬 호출(Parallel Calls), 그리고 질의와 무관한 도구 집합이 주어졌을 때 이를 거부해야 하는 무관성 탐지(Irrelevance Detection) 시나리오에서는 모델의 기저에 있는 추론 용량(Reasoning Capacity)이 성능을 좌우한다.21 압축 기술은 이러한 극한의 논리적 분기점에서 예기치 않은 행동을 유발하는 주된 원인이 된다.

## **3\. 양자화(Quantization)가 도구 호출 안정성에 미치는 역학적 파괴 현상**

양자화는 LLM을 개인용 컴퓨터나 엣지 하드웨어에 배포 가능하게 만드는 핵심 동력이지만 16, 가중치를 낮은 비트 폭으로 매핑하는 과정에서 필연적으로 정보의 손실, 즉 양자화 오차(Quantization Error)를 수반한다.15 이 오차는 일반적인 언어 생성 태스크에서는 두드러지지 않으나, 엄격한 형식을 요구하는 도구 호출에서는 비선형적인 정확도 하락을 유발한다.

### **3.1. 비트(Bit) 정밀도 하락과 도구 공간 혼란(Tool-space Confusion)**

8-bit(INT8) 양자화 모델은 일반적으로 16-bit 부동소수점(FP16) 모델과 비교하여 평균 정확도 하락이 0.5% 미만에 그치며 높은 보존율을 보인다.16 그러나 4-bit 양자화 모델로 넘어가면 상황은 급변한다. 서던 일리노이 대학교(Southern Illinois University)의 연구팀이 Llama3.1-8b 모델을 다양한 정밀도로 양자화하여 BFCL 및 GeoEngine 벤치마크에서 평가한 결과, 4-bit 양자화는 함수 호출 성공률을 극단적으로 추락시키는 것으로 나타났다.27

| 모델 정밀도 및 양자화 포맷 | Llama3.1-8b BFCL 성공률 (%) | Llama3.1-8b GeoEngine 성공률 (%) |
| :---- | :---- | :---- |
| **완전 정밀도 (FP16)** | 63.04 | 63.91 |
| **8-bit 양자화 (Q8\_0)** | 44.35 | 53.04 |
| **혼합 정밀도 (Q4\_K\_M)** | 39.57 | 56.96 |
| **4-bit 양자화 (Q4\_1)** | 34.35 | 59.57 |
| **4-bit 양자화 (Q4\_0)** | 20.43 | 43.04 |

표 1\. 양자화 수준에 따른 Llama3.1-8b 모델의 함수 호출 성공률 비교 (데이터 출처: 27)

위 표에서 증명되듯, 4-bit(Q4\_0) 양자화 모델의 BFCL 성공률은 20.43%로, 원본 FP16 모델(63.04%) 대비 3분의 1 수준으로 급락했다.27 이는 양자화된 모델이 지닌 '도구 공간 복잡성(Tool-space Complexity)'에 대한 취약성 때문이다.27 LLM 에이전트는 사용자의 질의를 해결하기 위해 시스템 프롬프트에 제공된 수십 개의 도구 목록을 탐색해야 한다. 연구에 따르면, 컨텍스트 창(Context Window)에 46개의 다양한 도구 선택지가 주어졌을 때, 4-bit 모델은 수많은 선택지 속에서 추론의 갈피를 잡지 못하고 엉뚱한 도구를 선택하거나 아예 선택을 실패하는 극심한 혼란을 겪었다.27 반면 선택지를 19개로 줄였을 때는 정상적으로 도구를 선택하는 모습을 보였다.27 이는 정밀도 하락이 모델의 문맥 이해 능력을 파괴하는 것이 아니라, 다수의 선택지 간의 미세한 의미론적 차이를 구분하는 해상도(Resolution)를 훼손한다는 것을 명확히 보여준다.

### **3.2. JSON 구문 오류의 기술적 기전과 어텐션 메커니즘 붕괴**

함수 호출 성능 저하의 또 다른 핵심 원인은 모델이 반환하는 JSON 구조의 구문 오류이다.20 트랜스포머(Transformer) 아키텍처의 핵심인 셀프 어텐션(Self-Attention) 연산은 시퀀스 내의 각 토큰이 다른 모든 토큰과의 종속성을 포착하도록 설계되어 있다.29 어텐션 스코어는 쿼리(Q), 키(K), 값(V) 행렬의 연산 결과에 소프트맥스(Softmax)를 취하여 계산되는데 (![][image1]), 이 행렬들이 4-bit로 압축되면 가중치의 근사 오차(Approximation Error)가 발생한다.29

이러한 오차는 일반 텍스트에서는 문맥을 심각하게 해치지 않지만, JSON 포맷팅이라는 고도의 구조적 억압 속에서는 치명적으로 작용한다. 벤치마크 실험에 따르면, 모델이 코드를 마크다운(Markdown) 텍스트로 반환할 때보다 JSON 구조 내부에 삽입하여 반환하도록 지시받았을 때 코드 작성 능력이 현저히 감소했다.28 이는 모델의 연산 자원이 'JSON 형식을 맞추는 부담(Burden of JSON Formatting)'에 소모되기 때문이다.28 특히 소스 문서에서 따옴표나 특수 문자가 포함된 텍스트를 추출하여 JSON의 키-값 쌍(Key-Value Pair)으로 삽입할 때, 양자화 모델은 이스케이프(Escape) 처리에 실패하는 빈도가 급증한다.20 결국 닫히지 않은 문자열(Unterminated string literal)이나 괄호의 불일치와 같은 구문 오류를 발생시키며, 파서는 이를 읽어 들이지 못하고 시스템 전체의 오류를 유발하게 된다.19

### **3.3. '플립(Flips)' 현상과 기존 평가 지표의 기만성**

압축된 LLM의 함수 호출 능력을 정확도(Accuracy)나 퍼플렉서티(Perplexity)로 평가하는 기존의 패러다임은 중대한 결함을 지니고 있다.31 마이크로소프트의 "Accuracy is Not All You Need" 연구는 양자화가 유발하는 '플립(Flips)'이라는 현상을 통해 이 문제를 조명한다.31

플립이란 원본 베이스라인 모델에서 정답으로 분류되었던 응답이 양자화 이후 오답으로 뒤바뀌거나(Correct ![][image2] Incorrect), 역으로 오답이었던 응답이 우연히 정답으로 바뀌는(Incorrect ![][image2] Correct) 현상을 총칭하는 거리 지표(Distance Metric)이다.33

| 평가 모델 | 16-bit 베이스라인 정확도 (%) | 8-bit GPTQ 양자화 정확도 (%) | 정확도 변화율 (%) | 플립 발생 비율 (%) |
| :---- | :---- | :---- | :---- | :---- |
| **Llama3-8b-instruct** | 59.65 | 59.06 | \-0.59 | **24.24** |

표 2\. 함수 호출 환경(BFCL)에서 Llama3-8b 모델의 양자화에 따른 플립 현상 (데이터 출처: 36)

위 데이터를 분석하면 충격적인 사실을 알 수 있다. Llama3-8b 모델에 8-bit GPTQ 양자화를 적용하여 BFCL 함수 호출 벤치마크를 수행했을 때, 16-bit 모델과 8-bit 모델 간의 총합 정확도 차이는 불과 0.59% 감소에 그쳤다.36 이 수치만 본다면 양자화가 함수 호출 능력을 거의 완벽하게 보존한 것으로 해석할 수 있다. 그러나 개별 응답을 미시적으로 교차 검증한 결과, 전체 응답의 24.24%에서 플립 현상이 발생했다.36 즉, 전체 도구 호출 응답의 약 4분의 1이 베이스라인 모델과 완전히 다른 행동 양상을 보이기 시작한 것이다.

이는 양자화로 인한 텐서 단위의 근사(Approximation)가 결정 경계(Decision Boundary) 부근에 있는 확률값을 무작위로 뒤집어버림으로써 발생하는 구조적 노이즈이다.36 퍼플렉서티는 출력 토큰 값들이 서로 상쇄(Cancel out)되는 성질이 있어 이러한 미세한 행동 변화를 감지하지 못한다.32 따라서 함수 호출 안정성을 보장하기 위해서는 단순 정확도가 아닌, 원본 모델과의 확률 분포 차이를 엄밀하게 측정하는 쿨백-라이블러 발산(Kullback-Leibler Divergence, KLD)이나 플립 비율과 같은 거리 지표가 양자화 모델 검증의 필수 기준으로 도입되어야 한다.32

## **4\. 모델 증류(Model Distillation)가 함수 호출 역량에 미치는 영향 및 한계**

양자화가 가중치의 물리적 손실에서 기인한 오류를 유발한다면, 모델 증류는 데이터와 지식의 매핑 방식을 통해 도구 호출 능력을 재구성한다.12 모델 증류는 본래 대규모 교사 모델의 복잡한 출력 확률 분포(Soft labels)를 소규모 학생 모델이 모방하도록 훈련하여 효율성을 달성하는 기법이다.11 특히 지연 시간(Latency)이 사용자 경험을 좌우하는 대화형 에이전트 환경에서 증류는 필수적인 가속 도구로 자리 잡았다.2

### **4.1. ODIA 프레임워크: 인라인 가속과 의미론적 라우팅**

함수 호출의 병목을 해결하기 위해 고안된 대표적인 산업적 응용 사례가 ODIA(Oriented Distillation for Inline Acceleration) 프레임워크이다.2 LLM 기반의 함수 호출은 일반적으로 피크 시간대에 응답까지 2\~3초가 소요되어 사용자의 대기 시간을 급격히 증가시킨다.7 기존의 단순 압축 방식은 함수 호출 정확도를 훼손하므로, ODIA는 트래픽의 본질적 난이도를 분류하여 선택적으로 모델을 가동하는 이중 모델 아키텍처(Dual-model Architecture)를 도입했다.2

ODIA의 파이프라인은 오프라인 훈련 단계와 온라인 서빙 단계로 나뉜다. 오프라인에서는 실제 프로덕션 트래픽(사용자 질의, 대화 기록, 도구 정의 등)에서 '단순 질의(Simple Queries)'를 알고리즘 기반으로 필터링하여 분리한다.2 이후 대형 모델의 함수 호출 결과물을 바탕으로 소형 모델을 증류 학습시킨다. 학습된 소형 모델은 두 가지 컴포넌트로 구성되는데, 첫째는 질의가 소형 모델의 처리 범주에 속하는지 신속하게 판단하는 '의도 분류 모델(Intent Classification Model)'이고, 둘째는 실제로 도구의 매개변수를 생성하는 '매개변수 생성 모델(Parameter Generation Model)'이다.7

이 구조를 실제 대규모 음악 애플리케이션 서비스에 배포한 결과, 의도 분류 모델이 전체 트래픽의 60%를 단순 질의로 판별하여 소규모 매개변수 생성 모델로 라우팅했다.2 이 과정에서 함수 호출의 정확도 손실은 무시할 수 있는 수준(Negligible)이었으며, 동시에 응답 지연 시간(Response Latency)의 기대치를 45%, 중간값(Median)을 78%나 감소시키는 압도적인 성능 향상을 입증했다.2 이는 특정 도메인에 한정된 도구 호출 로직은 대형 모델의 방대한 일반 지식 없이도, 철저하게 타겟팅된 지식 증류를 통해 완벽하게 복제될 수 있음을 시사한다.

### **4.2. API 및 도구 호출 체인(Tool-call Chain) 최적화 방법론**

단순한 지식 증류를 넘어, 연속적인 도구 호출 체인(Tool Call Chain)을 학생 모델에 이식하기 위해서는 데이터 합성 및 증강 기법이 결합되어야 한다.39 Amazon Bedrock의 모델 증류 연구는 학생 모델이 도구의 명세(Specification)를 정확히 읽고, 언제 어떤 함수를 호출할지 파악하는 능력을 극대화하기 위해 '데이터 증강(Data Augmentation)'을 필수 과정으로 삼는다.1 교사 모델이 생성한 원시 데이터를 기반으로 다양한 예외 상황과 엣지 케이스(Edge cases)를 합성하여 학생 모델에 주입하며, 훈련 데이터 내의 도구 명세 포맷(JSON 형식의 시스템 프롬프트 등)을 실제 추론 시의 포맷과 완벽히 일치시킴으로써 형식적 일관성을 강제한다.1

또한, 특정 독점 모델의 도구 호출 로직을 로컬 오픈소스 모델에 이식하는 실험에서도 정교한 최적화가 요구된다.38 Claude 모델의 도구 호출 능력을 200억 개(20B)의 파라미터를 가진 오픈소스 모델로 증류하는 실험에서, 단순히 교사 모델의 응답 데이터를 주입하는 1차원적 접근으로는 Claude와 일치하는 도구 호출 체인을 생성하는 비율이 12%에 불과했다.38 그러나 DSPy 프레임워크를 적용하여 프롬프트를 개선할 기존 예제들을 탐색하고, GEPA 알고리즘을 통해 훈련 데이터의 변이(Mutation)를 지속적으로 테스트한 결과, 단 3단계의 반복 최적화만으로 로컬 모델의 도구 호출 일치율(Match Rate)을 93%까지 비약적으로 상승시켰다.38 이는 함수 호출 역량의 증류가 단순한 가중치 미세조정(Fine-tuning)을 넘어, 입력되는 컨텍스트(도구 정의 및 예제)의 질과 밀도에 의해 결정됨을 보여준다.

### **4.3. 모델 동질화(Homogenization)의 함정과 제로샷 일반화의 상실**

모델 증류의 이러한 성공 이면에는 에이전트 시스템의 장기적 안정성을 위협하는 근본적인 부작용이 존재한다. 바로 교사 모델에 의존함으로써 발생하는 '모델 동질화(Model Homogenization)' 현상이다.12 최근 학계의 분석에 따르면, 다수의 오픈소스 로컬 모델들이 소수의 강력한 폐쇄형 교사 모델(예: GPT-4)의 생성 데이터를 바탕으로 증류되면서, 원래 서로 다른 아키텍처와 사전 학습 데이터를 가졌음에도 불구하고 교사 모델과 동일한 인지 구조와 한계를 공유하게 되는 현상이 나타났다.12

함수 호출 영역에서 이러한 다양성의 상실은 심각한 시스템적 취약점을 낳는다.12 증류된 학생 모델은 훈련 데이터에 포함되었던 고정된 API나 도메인에 대해서는 교사 모델에 필적하는 놀라운 정확도를 보이지만, 완전히 새롭거나 복잡한 미지의 도구 명세(Zero-shot Tool API)가 주어졌을 때는 강건하게 대처하는 능력(Robustness)이 크게 훼손된다.12 더욱이, 교사 모델이 특정 상황에서 겪는 구조적 환각이나 편향성마저 학생 모델이 비판 없이 답습하게 되어, 예기치 않은 사용자 질의에 대해 시스템 전체가 동일한 방식으로 실패하는 위험을 증가시킨다.12 따라서 다중 에이전트 협업 시스템(LLM-MAs)을 구축할 때 모든 모델을 동일한 출처로 증류하는 것은 피해야 하며, 베이스 모델(Base LLM)의 독립성을 유지하는 방향의 설계가 필수적이다.12

## **5\. 도구 호출 안정성 복구를 위한 전략적 접근**

양자화가 유발하는 구문 오류와 모델 증류가 지닌 편향성의 한계를 극복하기 위해, 연구자들은 추론 과정의 디코딩(Decoding) 메커니즘을 통제하거나 모델 내부의 구조적 훈련 방식을 근본적으로 혁신하는 접근법을 고안하고 있다.

### **5.1. 제한적 해독(Constrained Decoding)의 도입과 부작용의 역설**

양자화 모델이 JSON 형식을 파괴하는 현상을 원천 차단하기 위해 엣지 배포 환경에서 가장 보편적으로 채택되는 기술이 '제한적 해독(Constrained Decoding)'이다.40 SGLang, Outlines, XGrammar와 같은 프레임워크는 사용자가 정의한 JSON 스키마를 바탕으로 정규표현식(Regex) 또는 문맥 자유 문법(Context-Free Grammar, CFG) 기반의 유한 상태 기계(Finite State Machine, FSM)를 구성한다.40 모델이 토큰을 순차적으로 생성할 때, 이 FSM은 문법 규칙에 위배되는 다음 토큰의 생성 확률을 강제로 0으로 만들어버린다.42

| 제약형 해독 프레임워크 | 문법 파싱 방식 | JSON 유효성 성공률 (%) | 지연 속도 페널티 (대략적) |
| :---- | :---- | :---- | :---- |
| **Guidance / llguidance** | CFG (Earley parser) | 98% | \~50us/토큰 |
| **XGrammar** | CFG (PDA) | 93% | \<40us/토큰 |
| **Llama.cpp** | CFG (GBNF grammar) | 97% | 가변적 |
| **Outlines** | FSM (정규표현식) | 96% | 복잡한 스키마에서 지연 심함 |

표 3\. JSONSchemaBench 기반 제한적 해독 프레임워크의 성능 비교 (데이터 출처: 42)

위 표에서 보듯, 제한적 해독은 양자화 모델에서도 93%\~98%에 달하는 압도적인 JSON 구문 유효성을 보장한다.42 그러나 NeurIPS 2024의 연구는 이러한 문법 강제가 '확률 분포의 왜곡(Distortion of Probability Distribution)'이라는 치명적인 역설을 낳는다고 경고한다.42 LLM이 가장 자연스럽다고 예측한 고확률 토큰이 단순히 JSON 문법에 맞지 않는다는 이유로 마스킹(Masking)되면, 모델은 남아있는 저확률 토큰들 사이에서 확률을 재정규화(Renormalization)해야 한다.42 이 과정에서 토큰 간의 상대적 확률 차이가 비정상적으로 증폭되며, 결과적으로 구문은 완벽하지만 의미론적으로는 문맥에 맞지 않는 환각(Hallucination) 텍스트나 잘못된 매개변수 값을 출력하게 된다.42

이러한 부작용을 완화하기 위한 최적의 실무적 대안은, JSON 스키마 설계 시 매개변수 필드 이전에 모델이 생각의 과정을 자유롭게 텍스트로 풀어낼 수 있는 chain\_of\_thought 필드를 배치하는 것이다.42 이는 양자화된 모델에게 제한된 구문 안에서도 스스로 논리를 전개할 수 있는 '생각의 여백'을 제공하여, 강제적 해독으로 인한 추론 능력의 저하를 상쇄한다.

### **5.2. 구조적 훈련의 내재화: 강화학습 기반 스키마 준수 (Think Inside the JSON)**

외부 파서를 통한 문법 강제(Externalization)의 한계를 인식한 최근의 딥러닝 연구는, 모델 자체가 복잡한 구조적 규칙을 내재화(Internalization)하도록 훈련하는 방향으로 선회하고 있다. DeepSeek R1의 강화학습(RL) 아키텍처를 기반으로 한 "Think Inside the JSON" 연구는 이를 극적으로 증명한다.43

해당 연구진은 파라미터 1.5B 규모의 소규모 학생 모델에 대해, 별도의 정답 라벨이 있는 훈련 데이터 없이 오직 '보상 함수(Reward Function)'만을 활용하여 모델을 훈련시켰다.43 모델이 JSON 구조와 스키마를 정확히 준수했을 때만 보상을 부여하는 그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO) 기법을 적용한 결과, 모델은 외부 프레임워크의 도움 없이도 98.7%의 유효 JSON 출력률(Baseline 82.3%에서 급격한 상승)을 달성했다.43 더욱이 스키마 유효성 검사 오류(Schema validation error)를 47%나 감소시켰다.43 이는 소규모 모델이라 할지라도, 적절한 추론 강화학습을 거친다면 양자화나 압축의 페널티를 이겨내고 스스로 엄격한 도구 호출 포맷을 완벽하게 생성할 수 있음을 입증하는 중대한 성과이다.43

## **6\. 고급 훈련 패러다임: 양자화 인지 증류(QAD)와 하이브리드 최적화**

일반적으로 엣지 환경에 LLM을 배포할 때는 사전 학습과 미세조정(Fine-tuning)을 모두 마친 후 마지막에 가중치를 깎아내는 사후 양자화(Post-Training Quantization, PTQ)를 적용한다.45 그러나 앞서 플립 현상에서 논의했듯, PTQ는 도구 호출과 같이 논리적 민감도가 극도로 높은 태스크에서는 치명적인 정확도 훼손을 유발한다.45 이에 대한 대안으로 모델이 훈련 과정에서부터 양자화 환경의 저정밀도 연산을 시뮬레이션하며 적응하는 양자화 인지 훈련(Quantization-Aware Training, QAT)이 대두되었으나 45, 최근의 첨단 연구는 여기서 한 걸음 더 나아간 '양자화 인지 증류(Quantization-Aware Distillation, QAD)'의 우수성을 조명하고 있다.46

### **6.1. 사후 양자화(PTQ) 및 QAT의 한계와 QAD의 부상**

현대의 고성능 LLM은 지도 학습 미세조정(Supervised Fine-Tuning, SFT) 단계를 넘어 인간 피드백 기반 강화학습(RLHF) 등 다단계의 얼라인먼트(Alignment) 파이프라인을 거친다.46 연구에 따르면, 이러한 복잡한 RL 파이프라인을 거친 모델에 기존의 QAT 방식을 적용하면 심각한 훈련 불안정성이 발생하며, 특정 도메인에서는 오히려 PTQ보다도 성능이 저하되는 현상이 나타난다.46 QAT는 주어진 훈련 데이터의 정답(Hard Labels)을 맞추기 위해 교차 엔트로피(Cross-entropy) 손실을 최적화하는데, 이 과정에서 원본 모델이 긴 시간 동안 학습했던 미세한 확률 분포가 급격하게 파괴되기 때문이다.46

이를 해결하는 혁신적인 기법이 QAD이다. QAD는 양자화된 학생 모델을 훈련할 때, 정답 데이터 대신 고정밀도(FP16 또는 BF16) 교사 모델의 출력 확률 분포(Soft Labels)를 직접 모방하도록 쿨백-라이블러 발산(KL-Divergence) 손실을 적용한다.46

### **6.2. NVFP4 양자화와 도구 호출 성능의 완벽한 복구**

NVIDIA의 연구진은 4-bit 양자화 포맷인 NVFP4를 기반으로 Llama Nemotron Super V1 모델에 QAD를 적용하는 실험을 진행했다.46 그 결과는 모델 압축 기술의 새로운 지평을 보여준다.

* **확률 분포의 완벽한 정렬:** 전통적인 QAT를 적용한 양자화 모델은 교사 모델 대비 KL 발산이 0.311로 측정되어 원본의 동작 방식에서 크게 벗어난 모습을 보였다.46 반면 QAD를 적용한 모델은 KL 발산이 0.004로 극소화되어, 사실상 FP16 교사 모델의 추론 메커니즘을 완벽하게 모사했다.46  
* **구문 및 형식 준수 능력(IFEval):** 함수 호출의 근간이 되는 엄격한 포맷 규칙과 제약 조건을 평가하는 IFEval 벤치마크에서, QAD가 적용된 Llama Nemotron Super V1(NVFP4)은 87.8점을 기록하여, 오히려 압축되지 않은 BF16 베이스라인 모델(87.5점)의 성능을 미세하게 능가하는 놀라운 안정성을 달성했다.46  
* **에이전트 중심 추론(AgentBench):** 긴 문맥의 에이전트 기반 추론 능력을 측정하는 AA-LCR 벤치마크에서도, Nemotron 3 Nano 30B 모델에 QAD를 적용했을 때 34.3점의 높은 성능을 보이며 기존의 PTQ(31.3점)나 훈련을 붕괴시킨 QAT(24.8점)를 압도했다.17

이러한 성능 복구의 핵심은 QAD가 제공하는 '암묵적 정규화(Implicit Regularization)' 효과에 있다.46 교사 모델의 부드러운 라벨은 단순히 정답을 넘어서 "오답들 사이의 상대적인 확률"이라는 방대한 정보를 포함하고 있다.48 양자화된 학생 모델이 이 확률 구조 전체를 흡수함으로써, 도구 선택의 결정 경계에서 발생하는 양자화 노이즈가 상쇄된다.46 특히 놀라운 점은, QAD를 통해 코딩(Coding) 데이터 도메인 하나만으로 훈련을 진행했음에도 불구하고 수학이나 일반 추론과 같은 타 도메인(Cross-domain)의 지식까지 보존되었다는 것이다.46 이는 함수 호출 및 도구 연동과 같이 구조적 복잡성이 높은 태스크의 경우, 단순한 태스크 특화 학습을 넘어 원본 모델의 뇌 구조(확률 분포)를 통째로 이식하는 QAD 기법이 엣지 환경 배포의 필수 요건임을 강력히 시사한다.

### **6.3. 하이브리드 최적화: 증류와 양자화의 결합과 과제**

최근의 산업적 배포는 극강의 경량화를 위해 증류를 거친 후 양자화를 수행하는(Distill ![][image2] Quantize) 하이브리드 압축 모델 체계를 추구한다.9 하지만 이 두 가지 접근법을 순차적으로 결합하는 파이프라인은 최적화 검색 공간(Optimization Search Space)을 기하급수적으로 확장시키는 문제를 야기한다.51 지식 증류를 통해 정교하게 구축된 도구 호출 체인 지식이, 후속되는 4-bit 양자화 단계에서 컨텍스트 처리 제약이나 텐서 병렬화(Tensor Parallel) 매개변수와의 충돌로 인해 순식간에 무력화될 수 있다.51

이를 방지하기 위해, 학계는 두 기술을 동시 다발적으로 적용하는 교차 최적화(Co-optimization) 전략에 주목하고 있다.51 파레토 최적(Pareto-optimal) 관점에서 2-bit 및 4-bit 양자화 오차를 실시간으로 보상하는 가중치 튜닝을 진행하거나 52, 매개변수 효율적 양자화 미세조정(예: PEQA, QLoRA)을 통해 양자화 척도(Scale)만을 업데이트하며 증류된 지식을 보호하는 방식이 연구되고 있다.47 이러한 통합 프레임워크는 멀티 에이전트 시스템(LLM-MAs)에서 여러 소형 에이전트들이 도구 호출 API를 정확하게 교환하고 상호작용하기 위한 구조적 토대가 된다.6

## **7\. 시스템 아키텍처 및 배포를 위한 종합 설계 제언**

본 제2장(Chapter 2)에서는 DR-2.3의 설계 요건을 충족하기 위한 전제 조건으로서, 대규모 언어 모델의 증류 및 양자화가 함수 호출의 안정성에 미치는 구조적 영향력을 다각도로 분석했다. 파라미터 압축은 자원의 절약을 보장하지만, 구조적 데이터를 처리하는 데 있어서는 구문 파괴, 도구 혼란, 그리고 보이지 않는 편향성이라는 막대한 비용을 청구한다. 이를 해결하고 안정적인 에이전트 시스템을 구축하기 위해 다음과 같은 핵심 설계 원칙을 도출할 수 있다.

1. **환상에서 벗어난 평가 패러다임의 확립:** 압축 모델의 함수 호출 역량을 정확도나 퍼플렉서티라는 단일 지표로 판단하는 것은 극히 위험하다. 양자화 과정에서 발생하는 미세한 텐서 근사치는 최대 24%에 달하는 무작위 '플립(Flips)' 현상을 유발하여 전체 시스템의 논리적 연속성을 파괴한다. 도구 호출 평가 시에는 반드시 추상 구문 트리(AST) 기반의 다단계 노드 검증을 채택하고, KL-Divergence 등의 거리 지표를 통해 확률 분포의 변형을 모니터링해야 한다.  
2. **도구 공간 복잡성에 대응하는 비트(Bit) 하한선 설정:** 4-bit 수준의 극한 양자화는 어텐션 메커니즘에 직접적인 스케일링 오류를 유발하여, 이스케이프 문자 처리 실패 및 JSON 구문 붕괴의 주범이 된다. 도구의 선택지가 20개 이상으로 주어지거나 복잡한 병렬 호출이 요구되는 프로덕션 환경에서는 8-bit(INT8) 또는 특수 부동소수점 포맷(NVFP4)을 압축의 한계선으로 설정해야 구조적 무결성을 지킬 수 있다.  
3. **의도 기반 라우팅을 통한 증류의 전략적 분배:** 지연 시간 단축을 위해 무분별하게 모델 전체를 증류 모델로 교체하는 것은 제로샷(Zero-shot) 대처 능력을 상실하는 모델 동질화의 함정으로 이어진다. ODIA 프레임워크가 입증했듯, 실시간 트래픽을 분석하여 명확하고 단순한 도구 호출은 증류된 소형 모델로 라우팅하고, 복합적인 추론이 필요한 질의는 베이스라인 대형 모델로 분기시키는 이중 아키텍처가 성능과 자원 효율의 최적점을 제공한다.  
4. **구조적 규제의 내재화와 QAD의 전면 도입:** 외부 파서를 활용한 제한적 해독(Constrained Decoding)은 JSON 형식을 강제하지만 동시에 논리적 추론 확률을 왜곡하는 부작용을 낳는다. 따라서 시스템 설계 시 JSON 스키마 내에 chain\_of\_thought 필드를 선행 배치하여 모델의 추론 여백을 보장해야 한다. 무엇보다, 사후 양자화(PTQ)의 파괴적 특성을 회피하기 위해 훈련 단계에서부터 교사 모델의 확률 분포를 모사하는 양자화 인지 증류(QAD)나 GRPO 기반의 강화학습을 파이프라인에 필수적으로 통합하여, 모델이 압축된 상태에서도 스스로의 구조적 논리를 지켜내도록 설계해야 한다.

#### **참고 자료**

1. Amazon Bedrock Model Distillation: Boost function calling accuracy ..., 3월 13, 2026에 액세스, [https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-model-distillation-boost-function-calling-accuracy-while-reducing-cost-and-latency/](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-model-distillation-boost-function-calling-accuracy-while-reducing-cost-and-latency/)  
2. ODIA: Oriented Distillation for Inline Acceleration of LLM-based Function Calling \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/abs/2507.08877](https://arxiv.org/abs/2507.08877)  
3. ODIA: Oriented Distillation for Inline Acceleration of LLM-based Function Calling \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2507.08877v1](https://arxiv.org/html/2507.08877v1)  
4. Exploring the potential of Virtual Reality to convey information about architectural barriers and solutions \- WebThesis \- Politecnico di Torino, 3월 13, 2026에 액세스, [https://webthesis.biblio.polito.it/30909/1/tesi.pdf](https://webthesis.biblio.polito.it/30909/1/tesi.pdf)  
5. \[2305.02301\] Distilling Step-by-Step\! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/abs/2305.02301](https://arxiv.org/abs/2305.02301)  
6. The effect of four-bit quantization on multi-agent LLM coding performance, 3월 13, 2026에 액세스, [https://fse.studenttheses.ub.rug.nl/37068/1/Thesis-T-Lukkien.pdf](https://fse.studenttheses.ub.rug.nl/37068/1/Thesis-T-Lukkien.pdf)  
7. ODIA: Oriented Distillation for Inline Acceleration of LLM-based Function Calling, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/393685691\_ODIA\_Oriented\_Distillation\_for\_Inline\_Acceleration\_of\_LLM-based\_Function\_Calling](https://www.researchgate.net/publication/393685691_ODIA_Oriented_Distillation_for_Inline_Acceleration_of_LLM-based_Function_Calling)  
8. ODIA: Oriented Distillation for Inline Acceleration of LLM-based Function Calling \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/pdf/2507.08877](https://arxiv.org/pdf/2507.08877)  
9. Making Large Language Models Lighter: Distillation, Quantization, and Pruning Explained | by Saran Raj k | Medium, 3월 13, 2026에 액세스, [https://medium.com/@saranraj22222/making-large-language-models-lighter-distillation-quantization-and-pruning-explained-7a4721109f1d](https://medium.com/@saranraj22222/making-large-language-models-lighter-distillation-quantization-and-pruning-explained-7a4721109f1d)  
10. LLMs | Quantization, Pruning & Distillation | Lec 14.2 \- YouTube, 3월 13, 2026에 액세스, [https://www.youtube.com/watch?v=FKhjxjjupLA](https://www.youtube.com/watch?v=FKhjxjjupLA)  
11. Knowledge Distillation for LLMs: Techniques Explained \- Newline.co, 3월 13, 2026에 액세스, [https://www.newline.co/@zaoyang/knowledge-distillation-for-llms-techniques-explained--7f55591b](https://www.newline.co/@zaoyang/knowledge-distillation-for-llms-techniques-explained--7f55591b)  
12. Quantification of Large Language Model Distillation \- ACL Anthology, 3월 13, 2026에 액세스, [https://aclanthology.org/2025.acl-long.248.pdf](https://aclanthology.org/2025.acl-long.248.pdf)  
13. A guide to Amazon Bedrock Model Distillation (preview) | Artificial Intelligence, 3월 13, 2026에 액세스, [https://aws.amazon.com/blogs/machine-learning/a-guide-to-amazon-bedrock-model-distillation-preview/](https://aws.amazon.com/blogs/machine-learning/a-guide-to-amazon-bedrock-model-distillation-preview/)  
14. Fine-Tuning LLMs: LoRA, Quantization, and Distillation Simplified \- DEV Community, 3월 13, 2026에 액세스, [https://dev.to/iamfaham/fine-tuning-llms-lora-quantization-and-distillation-simplified-12nf](https://dev.to/iamfaham/fine-tuning-llms-lora-quantization-and-distillation-simplified-12nf)  
15. Optimizing LLMs for Performance and Accuracy with Post-Training Quantization \- NVidia, 3월 13, 2026에 액세스, [https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/](https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/)  
16. Quantized Local LLMs: 4-bit vs 8-bit Performance Analysis | SitePoint, 3월 13, 2026에 액세스, [https://www.sitepoint.com/quantized-local-llms-4bit-vs-8bit-analysis/](https://www.sitepoint.com/quantized-local-llms-4bit-vs-8bit-analysis/)  
17. nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 \- Hugging Face, 3월 13, 2026에 액세스, [https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4)  
18. We ran over half a million evaluations on quantized LLMs—here's what we found, 3월 13, 2026에 액세스, [https://developers.redhat.com/articles/2024/10/17/we-ran-over-half-million-evaluations-quantized-llms](https://developers.redhat.com/articles/2024/10/17/we-ran-over-half-million-evaluations-quantized-llms)  
19. CallNavi, A Challenge and Empirical Study on LLM Function Calling and Routing \- Jacques Klein, 3월 13, 2026에 액세스, [https://jacquesklein2302.github.io/papers/2025-EASE25-CallNavi.pdf](https://jacquesklein2302.github.io/papers/2025-EASE25-CallNavi.pdf)  
20. Leveraging LLMs for Automated Correction of Malformed JSON | by Lilian Li \- Medium, 3월 13, 2026에 액세스, [https://medium.com/@lilianli1922/leveraging-llms-for-automated-correction-of-malformed-json-e3c1f8b789a6](https://medium.com/@lilianli1922/leveraging-llms-for-automated-correction-of-malformed-json-e3c1f8b789a6)  
21. Function Calling Methods in LLMs \- Emergent Mind, 3월 13, 2026에 액세스, [https://www.emergentmind.com/topics/function-calling-methods](https://www.emergentmind.com/topics/function-calling-methods)  
22. Leaderboards and benchmarks \- a clefourrier Collection \- Hugging Face, 3월 13, 2026에 액세스, [https://huggingface.co/collections/clefourrier/leaderboards-and-benchmarks](https://huggingface.co/collections/clefourrier/leaderboards-and-benchmarks)  
23. How to Use Gorilla, 3월 13, 2026에 액세스, [https://gorilla.cs.berkeley.edu/blogs/5\_how\_to\_gorilla.html](https://gorilla.cs.berkeley.edu/blogs/5_how_to_gorilla.html)  
24. Berkeley Function Calling Leaderboard \- Gorilla LLM, 3월 13, 2026에 액세스, [https://gorilla.cs.berkeley.edu/blogs/8\_berkeley\_function\_calling\_leaderboard.html](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)  
25. Evaluating an LLM for your use case \- Paul Simmering, 3월 13, 2026에 액세스, [https://simmering.dev/blog/llm-eval/](https://simmering.dev/blog/llm-eval/)  
26. Quantization vs Distillation in Neural Networks: A Comparison | by Aaditya ura | Medium, 3월 13, 2026에 액세스, [https://medium.com/@aadityaura\_26777/quantization-vs-distillation-in-neural-networks-a-comparison-8ef522e4fbec](https://medium.com/@aadityaura_26777/quantization-vs-distillation-in-neural-networks-a-comparison-8ef522e4fbec)  
27. Less is More: Optimizing Function Calling for LLM Execution on ..., 3월 13, 2026에 액세스, [https://www.engr.siu.edu/staff/iraklis.anagnostopoulos/files/papers/Less\_is\_More\_Optimizing\_Function\_Calling\_for\_LLM\_Execution\_on\_Edge\_Devices.pdf](https://www.engr.siu.edu/staff/iraklis.anagnostopoulos/files/papers/Less_is_More_Optimizing_Function_Calling_for_LLM_Execution_on_Edge_Devices.pdf)  
28. LLMs are bad at returning code in JSON \- Aider, 3월 13, 2026에 액세스, [https://aider.chat/2024/08/14/code-in-json.html](https://aider.chat/2024/08/14/code-in-json.html)  
29. Quantization of Large Language Models and the Impact on Output Performance, 3월 13, 2026에 액세스, [https://lup.lub.lu.se/student-papers/record/9178256/file/9178257.pdf](https://lup.lub.lu.se/student-papers/record/9178256/file/9178257.pdf)  
30. Attn-QAT: 4-Bit Attention With Quantization-Aware Training \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2603.00040v2](https://arxiv.org/html/2603.00040v2)  
31. Accuracy is Not All You Need \- OpenReview, 3월 13, 2026에 액세스, [https://openreview.net/pdf?id=QVG7j29Sta](https://openreview.net/pdf?id=QVG7j29Sta)  
32. Qwen3.5-35B-A3B quantization quality \+ speed benchmarks on RTX 5080 16GB (Q8\_0 vs Q4\_K\_M vs UD-Q4\_K\_XL) \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1rei65v/qwen3535ba3b\_quantization\_quality\_speed/](https://www.reddit.com/r/LocalLLaMA/comments/1rei65v/qwen3535ba3b_quantization_quality_speed/)  
33. (PDF) Accuracy is Not All You Need \- ResearchGate, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/382251771\_Accuracy\_is\_Not\_All\_You\_Need](https://www.researchgate.net/publication/382251771_Accuracy_is_Not_All_You_Need)  
34. Accuracy is Not All You Need | Read Paper on Bytez, 3월 13, 2026에 액세스, [https://bytez.com/docs/neurips/95234/paper?\_c=eyJ2IjoxLCJyZWxhdGVkIjpbImNvZGUiLCJyZWZlcmVuY2VzIiwiY29uZmVyZW5jZSJdfQ%3D%3D](https://bytez.com/docs/neurips/95234/paper?_c=eyJ2IjoxLCJyZWxhdGVkIjpbImNvZGUiLCJyZWZlcmVuY2VzIiwiY29uZmVyZW5jZSJdfQ%3D%3D)  
35. Accuracy is Not All You Need \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2407.09141v1](https://arxiv.org/html/2407.09141v1)  
36. Accuracy is Not All You Need \- OpenReview, 3월 13, 2026에 액세스, [https://openreview.net/forum?id=QVG7j29Sta¬eId=arI1iqqWrD](https://openreview.net/forum?id=QVG7j29Sta&noteId=arI1iqqWrD)  
37. How Fireworks evaluates quantization precisely and interpretably, 3월 13, 2026에 액세스, [https://fireworks.ai/blog/fireworks-quantization](https://fireworks.ai/blog/fireworks-quantization)  
38. Teaching Local Models to Call Tools Like Claude \- Tomasz Tunguz, 3월 13, 2026에 액세스, [https://tomtunguz.com/distilling-claude-into-local-models/](https://tomtunguz.com/distilling-claude-into-local-models/)  
39. Build faster, more cost-efficient, highly accurate models with Amazon Bedrock Model Distillation (preview), 3월 13, 2026에 액세스, [https://aws.amazon.com/blogs/aws/build-faster-more-cost-efficient-highly-accurate-models-with-amazon-bedrock-model-distillation-preview/](https://aws.amazon.com/blogs/aws/build-faster-more-cost-efficient-highly-accurate-models-with-amazon-bedrock-model-distillation-preview/)  
40. SimpleTool: Parallel Decoding for Real-Time LLM Function Calling \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2603.00030v1](https://arxiv.org/html/2603.00030v1)  
41. Case Study: Building Tool-Integrated LLM Systems Using Function Calling and Model Context Protocol, 3월 13, 2026에 액세스, [https://www.ziegler.us/cs-building-tool-integrated-llm-systems/](https://www.ziegler.us/cs-building-tool-integrated-llm-systems/)  
42. How Structured Outputs and Constrained Decoding Work | Let's Data Science, 3월 13, 2026에 액세스, [https://letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json](https://letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json)  
43. \[R\] Training LLMs for Strict JSON Schema Adherence via Reinforcement Learning and Structured Reasoning : r/MachineLearning \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/MachineLearning/comments/1iwxtmb/r\_training\_llms\_for\_strict\_json\_schema\_adherence/](https://www.reddit.com/r/MachineLearning/comments/1iwxtmb/r_training_llms_for_strict_json_schema_adherence/)  
44. Think Inside the JSON: Reinforcement Strategy for Strict LLM Schema Adherence \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2502.14905v1](https://arxiv.org/html/2502.14905v1)  
45. How Quantization Aware Training Enables Low-Precision Accuracy Recovery \- NVidia, 3월 13, 2026에 액세스, [https://developer.nvidia.com/blog/how-quantization-aware-training-enables-low-precision-accuracy-recovery/](https://developer.nvidia.com/blog/how-quantization-aware-training-enables-low-precision-accuracy-recovery/)  
46. Quantization-Aware Distillation for NVFP4 Inference Accuracy ..., 3월 13, 2026에 액세스, [https://research.nvidia.com/labs/nemotron/files/NVFP4-QAD-Report.pdf](https://research.nvidia.com/labs/nemotron/files/NVFP4-QAD-Report.pdf)  
47. Understanding the difficulty of low-precision post-training quantization of large language models \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2410.14570v1](https://arxiv.org/html/2410.14570v1)  
48. (PDF) Quantization-Aware Distillation for NVFP4 Inference Accuracy Recovery, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/400178491\_Quantization-Aware\_Distillation\_for\_NVFP4\_Inference\_Accuracy\_Recovery](https://www.researchgate.net/publication/400178491_Quantization-Aware_Distillation_for_NVFP4_Inference_Accuracy_Recovery)  
49. Ditto: Quantization-aware Secure Inference of Transformers upon MPC \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2405.05525v1](https://arxiv.org/html/2405.05525v1)  
50. What is LLM Distillation vs Quantization | Exxact Blog, 3월 13, 2026에 액세스, [https://www.exxactcorp.com/blog/deep-learning/what-is-llm-distillation-vs-quantization](https://www.exxactcorp.com/blog/deep-learning/what-is-llm-distillation-vs-quantization)  
51. 1 Introduction \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2601.20408v1](https://arxiv.org/html/2601.20408v1)  
52. AI performance research papers \- Red Hat, 3월 13, 2026에 액세스, [https://www.redhat.com/en/artificial-intelligence/research](https://www.redhat.com/en/artificial-intelligence/research)  
53. HuangOwen/Awesome-LLM-Compression \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HuangOwen/Awesome-LLM-Compression](https://github.com/HuangOwen/Awesome-LLM-Compression)  
54. Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2403.14608v5](https://arxiv.org/html/2403.14608v5)  
55. Advancing Model Refinement: Muon-Optimized Distillation and Quantization for LLM Deployment \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2601.09865v1](https://arxiv.org/html/2601.09865v1)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAh0lEQVR4XmNgGAWjYAQADiBOA2IedAlyACMQtwKxMboEuQBkUC8Qs6BLkANArisA4jgoGwUIALEkiVgOiOcD8WQg5mOAAm4grgbiWWTgHUD8FYibgZidgQJgAsSrgVgGXYJUIAzEi4FYHl2CHJAFxBHoguQAUKKdCsTS6BLkAFBS4IXSIxEAALrtE0qISOF1AAAAAElFTkSuQmCC>