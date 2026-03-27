# **DR-5.3Ch.5 가상 머신(VM) 및 컨테이너 환경에서의 LLM 기반 에이전트 리소스 관리 아키텍처 및 커널 수준 최적화에 대한 심층 연구 보고서**

## **서론: 정적 추론에서 에이전틱 AI(Agentic AI)로의 패러다임 전환과 인프라의 과제**

인공지능 생태계는 사용자의 프롬프트에 수동적으로 응답하는 정적 언어 모델의 시대를 지나, 복잡한 워크플로우 전반에 걸쳐 자율적으로 추론, 계획, 행동을 조율하는 에이전틱 AI(Agentic AI) 시대로 급격히 진입하고 있다.1 이러한 근본적인 역할 변화는 기반 시스템, 특히 가상 머신(VM) 및 다중 테넌트(Multi-tenant) 클라우드 환경의 아키텍처 설계에 전례 없는 복잡성을 부여한다.1 과거의 대규모 언어 모델(LLM) 배포가 주로 모델의 가중치를 메모리에 적재하고 연산 장치(GPU)의 활용률을 극대화하는 정적인 파이프라인 최적화에 머물렀다면, 현대의 에이전트 환경은 완전히 다른 리소스 동역학을 요구한다.1 에이전트는 외부 도구인 컴파일러, 데이터베이스, 패키지 매니저, 웹 브라우저 등을 동적으로 호출하며, 이 과정에서 예측 불가능한 운영체제(OS) 수준의 리소스 변동성을 유발하기 때문이다.2

이러한 지능적 자율성의 경계를 결정짓는 가장 핵심적인 하드웨어 자원은 연산 능력(Compute) 이전에 GPU 비디오 메모리(VRAM)이다.1 VRAM의 용량과 관리 효율성은 에이전트가 유지할 수 있는 컨텍스트의 길이, 동시에 수행 가능한 작업의 수, 그리고 실시간 도구 오케스트레이션의 매끄러움을 결정하는 시스템의 생명선과 같다.1 VRAM 요구량을 과소평가하거나 양자화(Quantization) 수준을 잘못 선택할 경우 시스템 크래시, 치명적인 속도 저하, 그리고 에이전트의 자율성 붕괴로 직결된다.1 시스템 아키텍트의 관점에서 VRAM은 단순한 하드웨어 사양이 아니라, 단일 GPU에 모델이 적재될 수 있는지, 수백 명의 동시 사용자를 처리할 수 있는지, 나아가 상용 배포가 경제적으로 타당한지를 좌우하는 전략적 제약 조건이다.1

에이전트 인프라를 설계할 때는 하드웨어 사양을 먼저 결정하기보다는 구체적인 사용 사례를 기준으로 워크로드를 정의하는 것이 필수적이다.3 단순한 채팅이나 문서 요약은 소형 모델로도 충분하며, 코딩 지원이나 추론 작업은 중형 모델에서 최적의 효율을 보인다.3 특히 에이전트 워크로드는 가장 거대하고 똑똑한 단일 모델(예: 70B 파라미터)을 무리하게 구동하여 하드웨어 병목에 시달리는 것보다, 하드웨어 한계 내에서 최적화된 중소형 모델(예: 8B\~14B 파라미터)을 활용하여 빠른 추론과 빈번한 도구 호출을 반복하는 것이 전체적인 시스템 처리량 및 작업 달성률 측면에서 월등히 유리하다.3 경험 법칙에 따르면 16비트 부동소수점(FP16) 정밀도를 기준으로 10억 개(1B)의 파라미터당 약 2GB의 VRAM이 요구되며, 이는 모델 가중치뿐만 아니라 컨텍스트 윈도우 확장에 따른 KV 캐시(Key-Value Cache) 증가량을 고려할 때 보수적으로 산정되어야 한다.3

본 보고서는 이와 같이 고도로 동적이고 예측 불가능한 LLM 에이전트 워크로드를 VM 및 컨테이너 환경에서 안정적이고 효율적으로 구동하기 위한 전방위적인 리소스 관리 방법을 조사한다. 하드웨어 가상화 계층에서의 GPU 프로비저닝(vGPU 및 MIG), 리눅스 커널 수준의 리소스 통제 메커니즘인 cgroups v2, 쿠버네티스(Kubernetes) 환경의 동적 리소스 할당(DRA), 최신 eBPF 기반의 도구 단위 리소스 제어(AgentCgroup), 그리고 샌드박스 보안 격리에 이르는 심층적인 아키텍처를 분석하여 차세대 에이전틱 인프라의 청사진을 제시한다.

## **하드웨어 가상화와 하이퍼바이저 오버헤드 분석**

대규모 AI 모델 훈련 및 추론 워크로드를 배포할 때 가장 먼저 직면하는 인프라 설계의 분기점은 베어메탈(Bare Metal) 서버와 가상 머신(VM) 기반 환경 간의 선택이다.5 전통적인 하이퍼바이저 기반 가상화 모델은 테넌트 간의 강력한 격리(Isolation)와 오케스트레이션의 유연성을 제공하지만, 가상화 명령어 에뮬레이션과 메모리 및 스토리지 관리의 복잡성 증가로 인해 무시할 수 없는 성능 오버헤드를 수반하는 것으로 알려져 왔다.7

과거의 일부 벤치마크 테스트에서는 Kubernetes를 VM 위에 배포했을 때 베어메탈 대비 네트워크 대역폭 및 RAM 지연 시간에서 최대 100% 이상의 오버헤드가 발생한다는 극단적인 결과가 보고되기도 하였다.9 특히 VM 내부에서 다시 컨테이너를 구동하는 중첩 가상화(Nested Virtualization) 아키텍처의 경우, 추가적인 컨텍스트 스위칭으로 인해 CPU 바운드 워크로드에서 평균 20%에서 30%에 달하는 성능 페널티가 발생하며 I/O 집약적인 애플리케이션에서는 그 성능 저하 폭이 더욱 큰 것으로 측정되었다.7

그러나 하드웨어 지원 가상화 기술의 비약적인 발전과 GPU 패스스루(Passthrough), 최신 vGPU 소프트웨어 스택의 도입은 베어메탈과 가상화 환경 간의 역사적인 성능 격차를 사실상 소멸시키는 단계에 이르렀다.5 최근의 MLPerf 벤치마크 연구에 따르면, vGPU를 활용하는 현대적인 VM 플랫폼 기반 컨테이너는 AI/ML 워크로드에서 베어메탈 성능의 최대 99%를 유지할 수 있는 것으로 확인되었다.5 하이퍼바이저로 인해 발생하는 지연 시간(Latency) 오버헤드는 불과 2%에서 5% 수준으로 억제되며, 다단계 캐싱 전략과 반가상화(Paravirtualization)가 적용된 지능형 컨테이너 오케스트레이션을 결합할 경우 중첩 가상화 환경의 전체 처리량 감소를 8% 수준까지 방어할 수 있다.7

이러한 성능 보존의 핵심은 GPU 장치에 대한 물리적 접근 방식을 어떻게 가상화 계층에 매핑하느냐에 달려있다. AMD RX 9060 XT 등을 활용한 로컬 LLM 벤치마크나 Proxmox 환경에서의 테스트 사례를 보면, LXC(Linux Containers)와 같이 호스트 커널을 직접 공유하는 운영체제 수준 가상화를 사용하거나, IOMMU를 통한 전체 디바이스 패스스루(Full device passthrough)를 적용할 경우 가상 환경 내부의 GPU 접근 성능은 베어메탈의 네이티브 애플리케이션 프로세스와 사실상 동일한 지표를 나타낸다.12 완전한 장치 패스스루는 논리적으로 대상 디바이스를 호스트 OS에서 분리하여 가상 머신의 메모리 맵에 직접 연결하므로 하드웨어의 모든 컴퓨팅 잠재력을 제로 오버헤드로 활용할 수 있게 한다.12 단일 물리 GPU를 독점적으로 사용할 경우, K280Q와 같은 vGPU 프로필을 거치는 것보다 패스스루 모드에서 월등히 높은 원시 성능 점수를 기록하는 현상은 이러한 아키텍처의 특성을 방증한다.15

결론적으로 수십억 단위 이상의 파라미터를 가지는 거대 모델을 며칠에 걸쳐 훈련하는 극단적 연산 집약형 작업이나 최저 지연 시간과 최대 처리량이 동시에 요구되는 전용 인프라에서는 여전히 베어메탈 서버가 선호된다.6 그러나 다중 테넌트의 동적인 요청을 처리해야 하는 에이전트 추론 클라우드 환경에서는 2\~5% 수준의 미미한 가상화 오버헤드를 감수하더라도 VM과 컨테이너가 제공하는 리소스 분할, 격리, 확장성의 이점을 취하는 것이 현대 AI 인프라의 황금 표준(Golden standard)으로 자리 잡았다.5

## **GPU 다중화 및 격리 아키텍처: vGPU 대 MIG의 역학**

다중 테넌트 VM 환경에서 단일 물리적 GPU를 여러 LLM 에이전트 워크로드에 효율적으로 분할하고 격리하는 것은 클라우드 인프라의 핵심 경제성을 결정한다.16 Nebius의 다중 테넌트 추론 클라우드 전략에서도 언급되었듯, 이 분야의 가장 어려운 과제는 과도한 프로비저닝으로 인한 자원 낭비, 시끄러운 이웃(Noisy neighbor) 현상으로 인한 지연 시간 붕괴, 그리고 컨텍스트 스위치 오버헤드를 방지하면서 다수의 고객 모델을 단일 하드웨어에서 안전하게 구동하는 런타임 수준의 격리(Isolation)를 달성하는 것이다.17 NVIDIA 생태계를 기준으로, 이러한 GPU 가상화 및 공유 기술은 크게 시간적 분할 방식인 vGPU(Time-slicing)와 공간적 분할 방식인 MIG(Multi-Instance GPU)로 양분된다.18

| 특성 | vGPU (시간적 분할 / Time-Slicing) | MIG (공간적 분할 / Multi-Instance GPU) |
| :---- | :---- | :---- |
| **분할 방식** | 스케줄러를 통한 순차적 리소스 할당 (시간 교대) | 독립적인 하드웨어 파티션 (코어, 메모리 물리적 분리) |
| **격리 수준** | 논리적 격리, 워크로드 스파이크 시 간섭 가능성 존재 | 물리적 하드웨어 격리, 상호 간섭 없음 (Noisy neighbor 배제) |
| **성능 예측성** | 워크로드 수요에 따라 변동 폭 큼 | 엄격한 리소스 보장으로 매우 예측 가능한 지연 시간 유지 |
| **적합한 워크로드** | 대형 모델, 배치 크기가 큰 무거운 연산, I/O 집약적 작업 | 소형 모델, 배치 크기가 작은 가벼운 추론, 개발/테스트 환경 |
| **최대 VM 집적도** | A100 기준 최대 10개 VM (A100-4c 프로필 적용 시) | A100 기준 최대 7개 인스턴스/VM (A100-5c 프로필 적용 시) |
| **메모리 대역폭** | 할당된 타임 슬라이스 동안 전체 대역폭 독점 활용 가능 | 파티션 크기에 비례하여 대역폭이 엄격히 분할 및 제한됨 |

표 1: LLM 에이전트 워크로드를 위한 vGPU(시간 분할) 및 MIG(공간 분할) 가상화 기술 비교 18

### **시간 분할 기반의 vGPU (Time-Slicing)**

vGPU의 시간 분할(Time-slicing) 기술은 물리적 GPU 하드웨어를 쪼개는 대신 소프트웨어 스케줄러를 통해 워크로드를 순차적으로 처리하는 방식이다.19 베스트 에포트(Best-effort) 라운드 로빈 알고리즘을 활용하여 여러 가상 머신이 짧은 시간 동안 전체 GPU 코어와 메모리 대역폭에 접근할 수 있도록 권한을 교대한다.18

이러한 특성으로 인해 vGPU는 대형 모델과 대규모 배치 크기를 처리하는 무거운 추론 워크로드에서 강점을 발휘한다.19 타임 슬라이스 동안 해당 VM이 물리적 GPU의 방대한 메모리 대역폭 전체를 활용할 수 있기 때문에, 대량의 데이터 입출력이 요구되는 I/O 집약적 워크로드(예: IPSec을 포함한 NFV 작업이나 대용량 RAG 처리)에서 전체적인 처리량(Throughput)이 MIG 환경을 상회한다.19 또한, A100 GPU를 기준으로 최대 10개의 VM을 수용할 수 있어 VM 집적도 측면에서도 유연한 리소스 확장이 가능하다.19 그러나 시간 할당을 위해 다른 VM의 처리가 끝날 때까지 대기해야 하는 구조적 한계로 인해, 다수의 VM이 동시에 스파이크를 일으킬 경우 지연 시간(Latency)이 무작위로 치솟는 현상을 피할 수 없다.17

### **하드웨어 공간 분할 기반의 MIG (Multi-Instance GPU)**

MIG 기술은 단일 물리적 GPU를 최대 7개의 완전히 독립적인 인스턴스로 물리적으로 파티셔닝한다.18 각 인스턴스는 전용 컴퓨팅 코어, L2 캐시, 그리고 고대역폭 메모리 리소스를 독점적으로 할당받아 동시에 독립적으로 작동한다.18 VM 간에 다중 테넌시를 달성하려면 하이퍼바이저가 각각의 MIG 인스턴스를 개별 VM에 매핑할 수 있도록 vGPU 기술과의 결합이 필수적이다.18

MIG의 가장 큰 장점은 완벽한 하드웨어 격리를 통해 이웃 테넌트의 간섭을 원천 차단한다는 점이다.18 하나의 에이전트 인스턴스가 무한 루프에 빠지거나 극단적인 부하를 일으켜도, 다른 파티션에서 구동 중인 에이전트의 성능이나 안정성에는 어떠한 영향도 미치지 않는다.16 이는 SLA(서비스 수준 계약) 준수가 필수적인 프로덕션 추론 환경에서 지연 시간의 일관성과 예측 가능성을 보장하는 핵심 기반이 된다.18 가벼운 모델이나 소규모 배치 작업을 실행할 경우, VM은 타임 슬라이스를 기다릴 필요 없이 할당된 코어를 지속적으로 점유하므로 vGPU 방식보다 훈련 시간 단축 및 처리량 향상 측면에서 월등한 효율을 보여준다.19 단, 메모리 대역폭 역시 파티션 비율에 맞춰 쪼개어지므로 메모리 바운드(Memory-bound) 특성이 극심한 특정 대규모 LLM 디코딩 단계에서는 대역폭 갈증 현상이 발생할 수 있다.19

## **LLM 추론 환경의 저수준 병목 현상과 시스템 최적화**

VM 기반의 다중 테넌트 환경에서 LLM 에이전트를 구동할 때 발생하는 성능 저하의 원인은 단순히 GPU 연산력 부족에만 기인하지 않는다.24 복잡한 시스템 계층 전반에 걸쳐 하드웨어 원시 요소(FLOPs, 대역폭, 인터커넥트)와 런타임 소프트웨어 스택 간의 상호 작용에서 눈에 보이지 않는 다양한 지연 세금(Latency tax)과 병목(Bottleneck)이 발생한다.24

첫 번째 숨겨진 병목은 토큰화(Tokenization) 및 전처리 과정이다.24 다중 테넌트 시스템에 트래픽이 집중될 경우 CPU 코어에서 수행되는 토큰화 작업이 직렬화되면서 추론이 시작되기도 전에 수십 밀리초의 지연이 추가로 발생하며, 이는 확장을 가로막는 첫 번째 장벽이 된다.24

두 번째이자 가장 치명적인 병목은 추론의 두 단계인 프리필(Prefill)과 디코딩(Decode) 간의 하드웨어 요구 특성 차이와 KV 캐시(Key-Value Cache) 관리에서 비롯된다.4 프리필 단계는 입력 프롬프트 전체가 모델의 어텐션 및 피드포워드 네트워크 층을 한 번에 통과하는 과정으로, 전송된 바이트당 연산량(Arithmetic intensity)이 매우 높은 전형적인 컴퓨팅 바운드(Compute-bound) 특성을 지닌다.26 반면, 토큰을 하나씩 생성하는 디코딩 단계에서는 매 생성 시마다 GPU HBM(High Bandwidth Memory)으로부터 수십 기가바이트에 달하는 전체 모델 가중치와 KV 캐시를 반복적으로 불러와야 하므로 절대적인 메모리 대역폭 바운드(Memory-bound) 상태에 빠진다.26

특히 다중 문서 분석, 심층 연구, 코드 생성과 같이 수만에서 10만 개 이상의 긴 컨텍스트 윈도우(Long context)를 요구하는 에이전트 작업의 경우, 단일 추론 요청만으로도 수백 기가바이트에서 테라바이트 급의 KV 캐시 메모리가 소비될 수 있다.4 LLaMA2-70B 모델(FP16 정밀도)을 예로 들면, 단일 토큰의 KV 캐시에 약 2.6MB가 필요하며, 4,000토큰의 컨텍스트만 유지하더라도 세션당 10.4GB의 VRAM이 고갈된다.28 값비싸고 제한된 GPU VRAM이 한계에 도달하면 추론 시스템은 불가피하게 KV 캐시의 일부를 호스트 CPU DRAM이나 스토리지로 축출(Eviction)해야 하며, 이후 재사용 시 이를 다시 GPU로 로딩하는 과정에서 심각한 재계산(Recomputation) 지연과 PCIe 대역폭 병목이 발생한다.4

이러한 물리적 대역폭의 한계를 극복하기 위해 최근 인프라 아키텍처는 혁신적인 하드웨어-소프트웨어 공동 설계를 채택하고 있다.26 DualPath와 같은 최적화된 데이터 경로 설계는 네트워크 인터페이스 카드(NIC) 중심의 트래픽 관리를 통해 KV 캐시 오프로딩 트래픽과 지연 시간에 민감한 모델 추론 통신을 분리하여 병렬 처리의 충돌을 방지한다.30 또한 기존 스토리지의 한계를 뛰어넘어 순차 읽기 최대 14GB/s, 무작위 읽기 3.3백만 IOPS를 지원하는 PCIe 4.0 및 PCIe 5.0 기반의 엔터프라이즈 NVMe SSD와 CXL(Compute Express Link) 메모리 확장 기술이 도입되고 있다.27 이를 통해 수많은 에이전트 세션의 KV 캐시를 CPU와 스토리지 풀에 분산 저장하고 딥 I/O 파이프라인 최적화와 6-플레인 병렬성을 통해 즉각적으로 검색(Retrieval)함으로써 VRAM 용량의 물리적 한계를 획기적으로 확장할 수 있다.27

## **Linux Cgroups를 활용한 OS 레벨 리소스 제어 메커니즘**

가상 머신 내에서 LLM 에이전트를 컨테이너화하여 안전하게 구동하고, 무분별한 리소스 독점으로 인한 노드 마비를 방지하기 위해 Linux 제어 그룹(Control Groups, cgroups)이 핵심 커널 메커니즘으로 활용된다.31 과거의 cgroups v1은 CPU, 메모리, 블록 I/O 등 각 컨트롤러가 독립적이고 파편화된 계층 구조를 가져 관리가 복잡했으며, 권한 위임(Delegation)의 보안 취약점이 존재했다.33 이를 극복하기 위해 현대의 컨테이너 런타임 및 Kubernetes 환경은 단일 통합 계층 구조(Unified hierarchy)를 기반으로 안전한 루트리스(Rootless) 컨테이너 위임을 지원하는 cgroups v2를 표준으로 채택하고 있다.31

### **CPU 대역폭 통제 및 CFS 스케줄러 동역학**

CPU 자원 관리는 cgroups v2의 cpu 컨트롤러와 완전 공정 스케줄러(Completely Fair Scheduler, CFS)의 연동을 통해 이루어진다.31 컨테이너가 소비할 수 있는 절대적인 CPU 시간의 상한선(하드 리밋)은 cpu.max 파일에 \<quota\> \<period\> 형식으로 정의된다.31 커널은 통상적으로 100,000 µs (100 ms)의 주기를 기준으로 삼으며, 에이전트 프로세스가 도구 실행 등을 위해 해당 주기 내에 자신에게 할당된 쿼터(Quota)를 모두 소진할 경우, 호스트의 다른 물리적 CPU 코어들이 완전히 유휴 상태이더라도 해당 프로세스를 강제로 대기 상태로 밀어 넣는다.31 이러한 'CPU 스로틀링(Throttling)' 현상은 에이전트의 지연 시간을 비선형적으로 증가시키는 주요 원인이 된다.31

반면 시스템 부하가 높아 여러 컨테이너가 한정된 CPU 자원을 두고 경합(Contention)할 때 우선순위를 결정하는 것은 cpu.weight 값(1\~10,000 범위, 기본값 100)이다.31 Kubernetes 매니페스트에 선언된 resources.requests.cpu 값(millicpu 단위)은 다음 수식에 의해 커널의 cpu.weight로 정밀하게 변환되어 스케줄링의 기준점이 된다.31

![][image1]  
(단, Kubernetes 1 CPU Unit \= 1024 CPU shares로 맵핑됨 31)

### **메모리 품질 서비스(QoS) 프레임워크와 Thrashing의 딜레마**

메모리는 에이전트 워크로드에서 단일 컨테이너가 노드 전체를 붕괴시킬 수 있는 가장 위험한 자원이다.25 기존 cgroups v1의 단순한 단일 제한 방식(memory.limit\_in\_bytes)에서 진화하여, cgroups v2는 컨테이너의 메모리 사용량이 통과해야 하는 4개의 섬세한 수위 조절 관문(Watermarks)으로 구성된 메모리 품질 서비스(QoS) 계층을 도입했다.33

| 컨트롤 인터페이스 | 설정 목적 및 커널 동작 메커니즘 | 대응 강도 |
| :---- | :---- | :---- |
| **memory.min** | 극단적인 시스템 메모리 압박 하에서도 커널이 절대 회수(Reclaim)하지 않고 보장하는 최소한의 하드 보장 영역이다. | 하드 보장 (Hard Guarantee) |
| **memory.low** | 베스트 에포트(Best-effort) 보호 경계선이다. 노드 전체 메모리가 고갈되지 않는 한 이 임계치 이하의 메모리는 회수 대상에서 제외된다. | 소프트 보장 (Soft Guarantee) |
| **memory.high** | 프로세스 작동을 강제로 중단시키지(OOM Killed) 않으면서, 메모리 할당 속도를 강제로 늦추고 커널이 공격적으로 메모리 회수를 시작하도록 유도하는 스로틀 포인트이다. | 소프트 리밋 (Throttle Point) |
| **memory.max** | 프로세스가 절대 초과할 수 없는 물리적 한계선이다. 회수를 시도해도 이 값을 초과할 경우 커널 OOM 킬러가 작동하여 cgroup 내 프로세스를 강제 종료한다. | 하드 리밋 (Hard Limit) |

표 2: Linux cgroups v2의 계층적 메모리 제어 인터페이스 분석 31

에이전트 워크로드의 안정성을 위해 메모리 한계를 설정할 때, 시스템 아키텍트는 Kubernetes 환경 특유의 **스래싱(Thrashing)** 딜레마를 반드시 이해해야 한다.42 일반적으로 Kubernetes 워크커 노드는 예측 가능한 성능을 위해 스왑 공간(Swap space)을 비활성화한 상태로 운영된다.43 이 상태에서 컨테이너의 메모리 사용량이 memory.high 임계치를 초과하여 커널이 강한 회수 압박(Reclaim pressure)을 가할 경우, 스왑 공간이 없으므로 프로세스가 힙(Heap)에 직접 할당한 익명 페이지(Anonymous pages)는 디스크로 내보낼 수 없다.42

따라서 커널은 유일하게 회수 가능한 자원인 파일 기반 캐시(Page cache)를 강제로 비워버리는 선택을 하게 된다.42 만약 에이전트가 로컬 데이터베이스를 파싱하거나 대용량 라이브러리를 지속적으로 참조해야 하는 상황이라면, 필수적인 페이지 캐시가 계속해서 지워지고 다시 로드되는 악순환에 빠진다.42 이로 인해 디스크 I/O가 폭주하고 엄청난 양의 소프트/하드 페이지 폴트(Page faults)가 발생하며 프로세스는 사실상 정지 상태인 스래싱에 빠지게 된다.42 즉, 스왑이 없는 환경에서 memory.high를 무턱대고 낮게 설정하는 것은 메모리를 절약하는 것이 아니라 시스템의 캐시 효율을 파괴하여 치명적인 성능 저하를 초래하는 결과를 낳는다.43

이러한 부작용을 방지하기 위해서는 memory.low를 통해 필수 워킹셋(Working set)이 불필요하게 회수되는 것을 보호하고, memory.high와 memory.max 사이에 충분한 헤드룸(Headroom)을 두어 커널이 부드럽게 메모리를 정리할 수 있는 여유를 제공해야 한다.44 Gitaly와 같은 대규모 시스템의 튜닝 사례에서는 memory.low를 최대 한계의 10%(0.1 \* memory.max)로, memory.high를 75%(0.75 \* memory.max) 수준으로 동적 설정하는 하이브리드 접근법을 채택하여 안정성을 확보하고 있다.44

### **블록 디바이스 대역폭 및 I/O 제어**

에이전트가 코드 저장소를 복제하거나 대규모 데이터 세트를 스토리지에 기록하는 작업을 수행할 때, 이웃 테넌트의 디스크 I/O 자원을 고갈시키지 않도록 io.max (또는 blkio) 컨트롤러를 통한 제한이 수반되어야 한다.37 cgroups v2는 특정 블록 디바이스에 대해 초당 읽기/쓰기 바이트(BPS) 및 작업 수(IOPS)의 상한을 설정할 수 있는 유연성을 제공한다.45 특히, cgroups v2의 메모리 컨트롤러와 I/O 컨트롤러는 긴밀하게 통합되어 있어, 프로세스가 페이지 캐시를 변경하여 발생하는 더티 페이지(Dirty pages)의 비동기적 디스크 쓰기(Writeback) 작업을 원래 변경을 유발한 cgroup의 소유로 정확히 추적(Foreign pages tracking)하여 I/O 부하를 격리한다.32

## **에이전트 워크로드의 리소스 변동성 기형과 eBPF 기반 AgentCgroup**

기존의 마이크로서비스나 배치(Batch) 작업에 맞춰 설계된 리소스 오케스트레이션 패러다임은 샌드박스 내부에서 임의의 외부 도구를 동적으로 호출하는 LLM 코딩 에이전트(예: Claude Code, OpenHands, SWE-agent) 환경에서 심각한 구조적 결함을 드러낸다.2

최근 수행된 SWE-rebench 벤치마크 기반의 144개 소프트웨어 엔지니어링 작업 분석 연구는 이러한 리소스 동역학의 기형적(Anomalous) 특성을 수치로 증명한다.2 에이전트가 단일 작업을 완수하기 위한 엔드투엔드(End-to-end) 지연 시간 중 모델 추론에 소요되는 시간보다 OS 레벨의 실행(도구 호출, 컨테이너 및 사용자 네임스페이스 초기화 등)에 소요되는 시간이 무려 56%에서 74%를 차지하는 것으로 나타났다.2 즉, 에이전트 시스템 성능 최적화의 핵심 전장은 LLM 엔진 내부가 아니라 OS 커널 및 샌드박스 인프라에 있다.25

가장 눈에 띄는 현상은 도구 주도형(Tool-call-driven) 메모리 스파이크 현상이다.2 에이전트 시스템은 대기 상태일 때 약 185MB의 베이스라인 메모리만을 소비하지만, 컴파일러(gcc), 테스트 러너(pytest), 또는 패키지 매니저(npm)와 같은 특정 도구를 호출하는 순간 불과 1\~2초 이내에 메모리 사용량이 최대 2.9GB에서 4GB까지 폭발적으로 치솟는다.2 이러한 98.5%의 메모리 버스트는 오직 도구 호출 구간에서만 집중적으로 발생하며, 최고치 대 평균치 비율(Peak-to-average ratio)이 무려 15.4배에 달한다.2 반면, 동일 구간에서 CPU 이용률은 멀티 코어 환경에서 175%를 기록하는 반면 전체 평균은 13% 미만에 그치는 등 CPU와 메모리의 상관관계가 작업에 따라 극명하게 엇갈린다.2 이는 FaaS(서버리스) 워크로드가 대개 1.5배 미만의 메모리 변동성을 보이는 것과 비교할 때 차원이 다른 예측 불가능성이다.2

| 워크로드 프로필 | 유휴(Idle) 메모리 공간 | 메모리 최고/평균 비율 | CPU 변동폭 및 동역학 | 실행 결정성 (Determinism) |
| :---- | :---- | :---- | :---- | :---- |
| **일반적인 서버리스/FaaS** | 128 MB \~ 512 MB | 약 1.5 배 | 짧고 예측 가능한 스파이크 | 결정적 (반복 시 일관된 자원 소비) |
| **AI 코딩 에이전트 워크로드** | 약 185 MB 베이스라인 | **최대 15.4 배** | 평균 \< 13%, 피크 시 \> 175% | **비결정적** (동일 작업에도 1.8배 분산 존재) |

표 3: 일반 클라우드 워크로드와 AI 에이전트 샌드박스 워크로드 간의 OS 레벨 리소스 동역학 상세 비교 2

### **전통적 제어의 3대 불일치와 eBPF의 개입**

연구자들은 이러한 기형적 변동성 앞에서 기존 Kubernetes의 리소스 제어 방식이 세 가지 근본적인 불일치(Mismatch) 한계에 직면한다고 지적한다.2

1. **세분성 불일치 (Granularity Mismatch)**: 컨테이너 단위로 설정된 정적인 cgroup 정책은 수십 MB의 git status와 518MB 이상을 소비하는 pytest 간의 극적인 도구별 리소스 수요 차이를 분리하여 통제하지 못한다.2  
2. **반응성 불일치 (Responsiveness Mismatch)**: 사용자 공간(User-space)의 데몬이 cgroup 메트릭을 폴링(Polling)하고 스로틀링을 지시하는 방식은 1초 미만 단위로 발생하는 에이전트의 순간적인 폭발적 버스트를 추적하기에 너무 느리다.2  
3. **적응성 불일치 (Adaptability Mismatch)**: HPA(Horizontal Pod Autoscaler)처럼 과거의 리소스 소비 이력을 바탕으로 미래를 예측하는 통계적 방식은 언어 모델의 추론 경로에 따라 완전히 다른 도구를 호출하는 비결정적이고 상태를 지닌(Stateful) 에이전트 실행 흐름 앞에서는 무용지물이 된다.2

이러한 한계를 근본적으로 돌파하기 위해 최근 **AgentCgroup**이라는 인텐트 기반(Intent-driven)의 eBPF(Extended Berkeley Packet Filter) 리소스 컨트롤러 아키텍처가 제안되었다.2 AgentCgroup은 컨테이너 경계를 넘어 내부에서 실행되는 '도구 호출(Tool-call)의 경계'에 맞춰 계층적 cgroup 구조를 실시간으로 구성한다.2

작동 방식의 핵심은 양방향 리소스 협상(Bidirectional resource negotiation)과 커널 레벨의 집행(In-kernel enforcement)이다.2 에이전트는 앞으로 실행할 도구의 리소스 필요량을 OS에 사전에 선언(Declare)하고, 커널 내부에서 극도로 짧은 지연 시간으로 동작하는 eBPF 프로그램(sched\_ext 스케줄러 확장 및 memcg\_bpf\_ops 훅)이 즉각적으로 런타임 적응형 정책을 집행한다.2 이를 통해 다중 테넌트 환경에서 특정 에이전트의 컴파일 작업이 스파이크를 일으켜도 커널 공간에서 지연 없이 리소스 상한을 차단하므로 노드의 안전을 확보하고 유휴 자원의 낭비를 극적으로 줄일 수 있다.2

## **Kubernetes 환경의 오케스트레이션 및 동적 리소스 할당 (DRA)**

VM 계층과 Linux 커널 계층 위에서 대규모 클러스터 단위로 에이전트 인스턴스의 라이프사이클을 관리하는 최종 오케스트레이터는 Kubernetes이다.53 Kubernetes는 앞서 논의한 cgroups의 메커니즘을 추상화하여 Pod 및 컨테이너 단위의 requests와 limits로 매핑함으로써 자원을 스케줄링하고 품질 보증 수준(QoS)을 분류한다.31

에이전트 서비스의 안정성을 보장하기 위해 워크로드 특성에 따라 QoS 클래스를 적절히 할당해야 한다.31 CPU와 메모리의 requests와 limits를 동일하게 설정하여 **Guaranteed (보장됨)** 클래스를 부여받은 Pod는 노드 자원이 고갈되는 상황에서도 독립적인 cgroup 가중치를 유지하여 OOM 킬러나 CPU 스로틀링의 1차 희생양이 되는 것을 방지할 수 있다.31 반면 도구 호출에 의한 스파이크를 허용해야 하는 샌드박스 워크로드는 requests보다 높은 limits를 설정하는 **Burstable (버스트 가능)** 구성을 통해 일시적인 자원 초과 사용의 유연성을 확보할 수 있다.31 아울러 특정 테넌트나 네임스페이스가 물리적 한계를 넘어 GPU나 메모리를 독점하는 것을 막기 위해 ResourceQuota를 배포하여 네임스페이스 수준의 총량 제한(예: GPU 8개, 메모리 256GB 제한)을 강제하는 것이 엔터프라이즈 환경의 핵심 모범 사례이다.53

### **장치 할당의 패러다임 전환: 동적 리소스 할당 (DRA)**

기존의 Kubernetes 환경에서 GPU나 AI 가속기를 컨테이너에 할당하는 방식은 전통적인 디바이스 플러그인(Device Plugins) API에 의존했다.56 그러나 이 방식은 단순히 노드에 부착된 장치의 수량(정수형 카운트)만을 계산하여 특정 컨테이너에 단독으로 끼워 넣는 매우 경직된 구조를 지녀, 다양한 VRAM 요구량이나 특정 세대의 텐서 코어가 필요한 에이전트 워크로드를 유연하게 스케줄링하는 데 한계가 뚜렷했다.56

데이터 센터의 전력 및 하드웨어 비용이 기하급수적으로 상승함에 따라 리소스 배치 효율을 극대화하기 위해 쿠버네티스 1.34 및 1.35 릴리스에서 \*\*DRA (Dynamic Resource Allocation, 동적 리소스 할당)\*\*가 정식 도입(GA)되었다.56 DRA는 스토리지 볼륨을 동적으로 프로비저닝하는 PV/PVC(Persistent Volume Claim) 모델의 철학을 컴퓨팅 디바이스 할당에 그대로 이식한 혁신적인 API 구조를 지닌다.57

클러스터 관리자나 디바이스 드라이버는 노드에 장착된 하드웨어를 단순히 숫자가 아닌 풍부한 속성(메모리 용량, 코어 수, 세대 정보 등)을 담은 DeviceClass 객체로 분류하여 제공한다.56 에이전트 애플리케이션 운영자는 Pod 매니페스트 내에 하드코딩된 리소스 수량 대신 ResourceClaim 또는 동적으로 클레임을 생성하는 ResourceClaimTemplate을 참조하도록 선언한다.57

특히 공통 표현 언어(CEL, Common Expression Language)를 활용하여 "A100 이상이면서 VRAM 40GB 이상인 가속기"와 같이 극도로 세밀한 하드웨어 속성 필터링(Fine-grained filtering)을 수행할 수 있다.57 또한 단일 ResourceClaim을 여러 컨테이너나 Pod가 공유하도록 구성함으로써, 초기화 컨테이너(Init container)가 모델 가중치를 VRAM에 미리 로드해 두고 이후 본 애플리케이션 컨테이너가 해당 리소스를 물려받아 사용하는 등 고도화된 디바이스 공유(Device sharing) 시나리오를 구현할 수 있다.57

YAML

\# DRA 기반의 GPU 동적 요청을 위한 ResourceClaimTemplate 예제 구조 \[60\]  
apiVersion: resource.k8s.io/v1  
kind: ResourceClaimTemplate  
metadata:  
  name: agent-gpu-resourceclaimtemplate  
  namespace: agent-inference-service  
spec:  
  spec:  
    devices:  
      requests:  
      \- exactly:  
        allocationMode: ExactCount  
        count: 1  
        deviceClassName: gpu.nvidia.com  
        name: gpu

## **에이전트 옵저버빌리티(Observability)와 보안 샌드박싱 아키텍처**

에이전트가 가상 머신 내에서 프로덕션 궤도에 오르면, 정적인 시스템 지표 모니터링만으로는 시스템의 건전성을 담보할 수 없다.61 전통적인 로그 집계 시스템이나 프로메테우스(Prometheus) 기반의 임계값 알람은 시스템의 상태를 사후적(Post-hoc)으로만 보여주며, 복잡한 비선형적 인과 관계를 지닌 에이전트의 내부 의사결정 흐름을 반영하지 못한다.62 에이전트 자체가 클러스터의 상태에 대한 멘탈 모델(Mental model)을 구축하고 자가 치유를 수행하기 위해서는 지연된 시각의 로그가 아니라 실시간 커널 동작 상태를 캡처하는 데이터 파이프라인이 필요하다.62

### **eBPF 중심의 AI 사이드카(Sidecar) 패턴**

이러한 한계를 극복하기 위해 Kubernetes 환경에서는 주 애플리케이션 컨테이너와 동일한 Pod에 배치되어 로컬 네트워크 네임스페이스와 스토리지를 공유하는 사이드카(Sidecar) 컨테이너 패턴이 널리 확장되어 활용된다.64

단순히 로그를 수집하여 외부 플랫폼으로 전송하던 과거의 프록시 형태를 넘어, 차세대 'AI 사이드카'는 4\~8B 수준의 경량화된 지능형 추론 모델을 직접 내장하는 구조로 진화하고 있다.63 이 지능형 사이드카는 eBPF를 활용하여 주 컨테이너에서 발생하는 CPU 스로틀링 시그널, 메모리 회수 패턴, 커널 공간의 시스템 콜(Syscall) 이벤트를 제로 계측(Zero-instrumentation) 방식으로 실시간 수집한다.63 수집된 데이터를 바탕으로 로컬 레벨에서 즉각적인 임베딩 편차(Embedding drift)나 OOM(Out-of-Memory) 위협을 의미론적으로 파악하여 선제적으로 경고하거나 워크로드를 차단하며, 이러한 로컬 신호들이 컨트롤 플레인의 '클러스터 브레인'으로 집계되어 전체 노드의 동적 리소스 할당을 재조정하는 '에이전틱 옵스(Agentic Ops)' 생태계를 형성한다.62

### **보안 최전선: 다중 테넌트 샌드박스 격리 기술**

에이전트는 근본적으로 사람의 지시를 받아 코드를 생성하고 실행하며 외부와 네트워크 통신을 수행하므로 악의적인 프롬프트 인젝션이나 신뢰할 수 없는 코드(Untrusted code)의 실행 위협에 항상 노출되어 있다.69 에이전트가 구동되는 샌드박스 환경이 뚫릴 경우 다중 테넌트 VM 클러스터 전체가 오염될 위험이 존재하므로, 보안 강도와 성능 오버헤드 간의 균형을 맞춘 격리 기술 선택이 필수적이다.70

1. **컨테이너 및 프로세스 수준 격리**: 일반적인 Docker나 샌드박스 런타임(Sandbox runtime)은 설정이 간편하고 성능 오버헤드가 사실상 전무하지만, 호스트 커널을 그대로 공유하므로 Linux 권한 상승 취약점에 노출될 위험이 상존한다.70 따라서 읽기 전용 파일 시스템 마운트, Linux Capabilities 드롭(Drop)과 같은 최소 권한 원칙(Least privilege) 적용이 수반되어야 한다.70  
2. **gVisor (사용자 공간 커널)**: Google이 개발한 gVisor는 런타임에 호스트 커널과 컨테이너 사이에 사용자 공간 커널을 삽입하여 시스템 콜(Syscall)을 엄격히 가로채고 필터링한다.70 별도의 게스트 커널을 부팅할 필요가 없어 메모리 풋프린트가 작고 시작 속도가 빠르지만, I/O 작업이 빈번한 워크로드에서는 10\~30%에 달하는 통신 오버헤드가 발생한다.71  
3. **Firecracker MicroVM 및 Kata Containers**: AWS에서 개발한 Firecracker는 KVM 기반의 초경량 가상 머신(MicroVM)을 생성하여 각 에이전트 워크로드마다 독립적인 게스트 Linux 커널을 할당하는 하드웨어 수준의 완벽한 격리를 제공한다.71 해커가 호스트를 탈취하려면 게스트 커널과 KVM 하이퍼바이저 방어벽을 동시에 뚫어야 하므로 다중 테넌트 환경에서 최고의 보안성을 자랑한다.70 보안성이 뛰어남에도 불구하고 최적화된 설계를 통해 125ms 이내의 쾌속 부팅이 가능하며 VM당 메모리 오버헤드가 5MB 미만으로 억제되므로, Kata Containers와 결합하여 Kubernetes 파드에 투명하게 통합될 때 프로덕션급 에이전트 배포를 위한 가장 이상적인 샌드박싱 아키텍처로 평가받는다.70

더불어 에이전트가 외부 서비스 연동을 위해 요구하는 API 키와 같은 민감한 크리덴셜은 에이전트 컨테이너 내부 환경 변수로 직접 노출하지 않고, 사이드카 형태의 외부 프록시를 통해 요청 패킷에 안전하게 인젝션(Injection)하는 심층 방어(Defense in depth) 기법을 병행하여 샌드박스 탈취 시의 피해를 국소화해야 한다.70

## **결론**

VM 환경에서 대규모 언어 모델(LLM) 기반의 에이전트를 프로덕션 클라우드 레벨로 서비스하기 위한 아키텍처 설계는 기존의 마이크로서비스 인프라와는 완전히 궤를 달리하는 파괴적 혁신을 요구한다. 에이전트 워크로드는 극도로 무거운 GPU VRAM 의존성 및 추론 연산의 한 축과, OS 샌드박스 환경 내에서 도구 호출을 통해 예측 불가능한 메모리 버스트(최대 15.4배) 및 비결정적 리소스 스파이크를 유발하는 또 다른 한 축이 공존하는 양면적 특성을 지닌다.

이를 통제하기 위해 시스템 아키텍트는 하드웨어 가상화 계층에서 워크로드의 배치 크기와 지연 시간 민감도에 따라 시간 분할(vGPU)과 물리적 공간 분할(MIG)을 전략적으로 선택하여 다중 테넌트 간의 리소스 간섭을 격리해야 한다. 또한 Linux cgroups v2의 정교한 메모리 QoS 메커니즘을 적용함에 있어 스왑리스(Swapless) 쿠버네티스 노드 환경에서의 치명적인 스래싱 위험을 회피하기 위해 무리한 하드 리밋 지정을 지양하고 여유율(Headroom) 기반의 최적화를 수행해야 한다.

가장 중요한 것은 전통적인 컨테이너 기반의 정적 리소스 통제의 한계를 넘어서는 것이다. eBPF 기술을 결합하여 커널 수준에서 밀리초 단위의 도구 호출에 반응하는 AgentCgroup의 적용, Kubernetes DRA를 통한 하드웨어 가속기의 동적 속성 매핑, 그리고 Firecracker 마이크로VM과 결합된 AI 사이드카 기반의 실시간 에이전틱 옵스(Agentic Ops) 파이프라인 구축이 필수적으로 뒷받침되어야 한다. 이와 같이 하드웨어 병목(KV 캐시 대역폭) 완화부터 커널 제어, 쿠버네티스 스케줄링, 그리고 보안 격리에 이르는 수직적인 풀스택(Full-stack) 융합 설계만이 차세대 에이전틱 AI 클라우드가 직면한 자원 고갈과 변동성의 혼돈을 극복하고 시스템의 확장성 및 안정성을 담보하는 유일한 해답이 될 것이다.

#### **참고 자료**

1. VRAM Requirements in Agentic AI Systems: A Comprehensive Guide \- AWS Builder Center, 3월 14, 2026에 액세스, [https://builder.aws.com/content/31Yeh8Jz9yCtgz9uL6lseoUQpLB/vram-requirements-in-agentic-ai-systems-a-comprehensive-guide](https://builder.aws.com/content/31Yeh8Jz9yCtgz9uL6lseoUQpLB/vram-requirements-in-agentic-ai-systems-a-comprehensive-guide)  
2. AgentCgroup: Understanding and Controlling OS Resources of AI Agents \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2602.09345v2](https://arxiv.org/html/2602.09345v2)  
3. How to Run Large Language Models Locally: Hardware, VRAM, and Setup Explained | by Mehul Gupta | Data Science in Your Pocket | Medium, 3월 14, 2026에 액세스, [https://medium.com/data-science-in-your-pocket/how-to-run-large-language-models-locally-hardware-vram-and-setup-explained-7caec36ef181](https://medium.com/data-science-in-your-pocket/how-to-run-large-language-models-locally-hardware-vram-and-setup-explained-7caec36ef181)  
4. How to Reduce KV Cache Bottlenecks with NVIDIA Dynamo, 3월 14, 2026에 액세스, [https://developer.nvidia.com/blog/how-to-reduce-kv-cache-bottlenecks-with-nvidia-dynamo/](https://developer.nvidia.com/blog/how-to-reduce-kv-cache-bottlenecks-with-nvidia-dynamo/)  
5. An architectural decision: Containers on bare metal or on virtual machines | CNCF, 3월 14, 2026에 액세스, [https://www.cncf.io/blog/2025/11/20/an-architectural-decision-containers-on-bare-metal-or-on-virtual-machines/](https://www.cncf.io/blog/2025/11/20/an-architectural-decision-containers-on-bare-metal-or-on-virtual-machines/)  
6. Bare Metal vs. Traditional VMs: Which is Better for LLM Training? \- Runpod, 3월 14, 2026에 액세스, [https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-llm-training](https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-llm-training)  
7. Optimizing Nested Virtualization for Multi-Cloud Performance \- IJIRCT, 3월 14, 2026에 액세스, [https://www.ijirct.org/download.php?a\_pid=2503033](https://www.ijirct.org/download.php?a_pid=2503033)  
8. Performance Evaluation of Virtual Machines and Containers in High Performance Computing \- RSIS International, 3월 14, 2026에 액세스, [https://rsisinternational.org/journals/ijrsi/uploads/vol13-iss2-pg794-805-202603\_pdf.pdf](https://rsisinternational.org/journals/ijrsi/uploads/vol13-iss2-pg794-805-202603_pdf.pdf)  
9. VM overhead 10x higher than expected \- Bare metal approx: 150% faster than VM's : r/kubernetes \- Reddit, 3월 14, 2026에 액세스, [https://www.reddit.com/r/kubernetes/comments/183cb5p/bare\_metal\_vs\_vm\_vm\_overhead\_10x\_higher\_than/](https://www.reddit.com/r/kubernetes/comments/183cb5p/bare_metal_vs_vm_vm_overhead_10x_higher_than/)  
10. Performance Overhead Based Analysis of Container based Virtualization with Type1, Type2 Hypervisor \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/publication/395887423\_Performance\_Overhead\_Based\_Analysis\_of\_Container\_based\_Virtualization\_with\_Type1\_Type2\_Hypervisor](https://www.researchgate.net/publication/395887423_Performance_Overhead_Based_Analysis_of_Container_based_Virtualization_with_Type1_Type2_Hypervisor)  
11. Virtual Machines vs. Bare Metal: Choosing the Right Infrastructure for AI Training, 3월 14, 2026에 액세스, [https://blog.nebulablock.com/virtual-machines-vs-bare-metal-choosing-the-right-infrastructure-for-ai-training/](https://blog.nebulablock.com/virtual-machines-vs-bare-metal-choosing-the-right-infrastructure-for-ai-training/)  
12. How we improved AI inference on macOS Podman containers | Red Hat Developer, 3월 14, 2026에 액세스, [https://developers.redhat.com/articles/2025/06/05/how-we-improved-ai-inference-macos-podman-containers](https://developers.redhat.com/articles/2025/06/05/how-we-improved-ai-inference-macos-podman-containers)  
13. The Real Performance Penalty of GPU Passthrough into a VM (It's... boring) : r/LocalLLaMA, 3월 14, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1lkzynl/the\_real\_performance\_penalty\_of\_gpu\_passthrough/](https://www.reddit.com/r/LocalLLaMA/comments/1lkzynl/the_real_performance_penalty_of_gpu_passthrough/)  
14. What performance impact does Proxmox virtualization have on GPU-accelerated LLM inference? \- Reddit, 3월 14, 2026에 액세스, [https://www.reddit.com/r/Proxmox/comments/1hsucgk/what\_performance\_impact\_does\_proxmox/](https://www.reddit.com/r/Proxmox/comments/1hsucgk/what_performance_impact_does_proxmox/)  
15. Grid K2 performance difference between pass-through mode and vGPU, 3월 14, 2026에 액세스, [https://forums.developer.nvidia.com/t/grid-k2-performance-difference-between-pass-through-mode-and-vgpu/162423](https://forums.developer.nvidia.com/t/grid-k2-performance-difference-between-pass-through-mode-and-vgpu/162423)  
16. GPU-Virt-Bench: A Comprehensive Benchmarking Framework for Software-Based GPU Virtualization Systems \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2512.22125v1](https://arxiv.org/html/2512.22125v1)  
17. The multi-tenant inference cloud is coming. Who's actually solving GPU isolation? \- Reddit, 3월 14, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1ouarc6/the\_multitenant\_inference\_cloud\_is\_coming\_whos/](https://www.reddit.com/r/LocalLLaMA/comments/1ouarc6/the_multitenant_inference_cloud_is_coming_whos/)  
18. Deployment — NVIDIA Virtual GPU (vGPU): FAQ, 3월 14, 2026에 액세스, [https://docs.nvidia.com/vgpu/faq/latest/deployment.html](https://docs.nvidia.com/vgpu/faq/latest/deployment.html)  
19. VMware vSphere 7 with NVIDIA AI Enterprise time-sliced vGPU vs ..., 3월 14, 2026에 액세스, [https://www.vmware.com/techpapers/2022/vgpu-vs-mig-perf.html](https://www.vmware.com/techpapers/2022/vgpu-vs-mig-perf.html)  
20. Comparing Multi-Instance GPU (MIG) and Time-Slicing for GPU Resource Sharing, 3월 14, 2026에 액세스, [https://openmetal.io/resources/blog/mig-vs-time-slicing-gpu-sharing/](https://openmetal.io/resources/blog/mig-vs-time-slicing-gpu-sharing/)  
21. Sharing is caring: How to make the most of your GPUs part 2 \- Multi-instance GPU \- Red Hat, 3월 14, 2026에 액세스, [https://www.redhat.com/en/blog/sharing-caring-how-make-most-your-gpus-part-2-multi-instance-gpu](https://www.redhat.com/en/blog/sharing-caring-how-make-most-your-gpus-part-2-multi-instance-gpu)  
22. Virtual GPU vs. GPU Passthrough: Key Differences Explained \- Scale Computing, 3월 14, 2026에 액세스, [https://www.scalecomputing.com/resources/virtual-gpu-vs-gpu-passthrough](https://www.scalecomputing.com/resources/virtual-gpu-vs-gpu-passthrough)  
23. Time-Slicing GPUs in Kubernetes — NVIDIA GPU Operator, 3월 14, 2026에 액세스, [https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)  
24. The Hidden Bottlenecks in LLM Inference: Why TFLOPs and VRAM Don't Determine Performance \- virtualizationvelocity, 3월 14, 2026에 액세스, [https://www.virtualizationvelocity.com/home/the-hidden-bottlenecks-in-llm-inference](https://www.virtualizationvelocity.com/home/the-hidden-bottlenecks-in-llm-inference)  
25. OS-Level Challenges in LLM Inference and Optimizations \- eunomia, 3월 14, 2026에 액세스, [https://eunomia.dev/blog/2025/02/18/os-level-challenges-in-llm-inference-and-optimizations/](https://eunomia.dev/blog/2025/02/18/os-level-challenges-in-llm-inference-and-optimizations/)  
26. LLM Inference Benchmarking \- Measure What Matters | DigitalOcean, 3월 14, 2026에 액세스, [https://www.digitalocean.com/blog/llm-inference-benchmarking](https://www.digitalocean.com/blog/llm-inference-benchmarking)  
27. Breaking Through the Memory Wall: How CXL Transforms RAG and KV Cache Performance, 3월 14, 2026에 액세스, [https://www.asteralabs.com/breaking-through-the-memory-wall-how-cxl-transforms-rag-and-kv-cache-performance/](https://www.asteralabs.com/breaking-through-the-memory-wall-how-cxl-transforms-rag-and-kv-cache-performance/)  
28. KV Cache Meets NVMe: The Key to Accelerating LLM Inference, 3월 14, 2026에 액세스, [https://www.memblaze.com/en/about-company/news/792.html](https://www.memblaze.com/en/about-company/news/792.html)  
29. \[2601.19910\] Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/abs/2601.19910](https://arxiv.org/abs/2601.19910)  
30. DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2602.21548v1](https://arxiv.org/html/2602.21548v1)  
31. Kubernetes: Pod resources.requests, resources.limits, and Linux ..., 3월 14, 2026에 액세스, [https://itnext.io/kubernetes-pod-resources-requests-resources-limits-%D1%82%D0%B0-linux-cgroup-dcc176fa1400](https://itnext.io/kubernetes-pod-resources-requests-resources-limits-%D1%82%D0%B0-linux-cgroup-dcc176fa1400)  
32. How to Understand Docker Container Cgroups in Depth \- OneUptime, 3월 14, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-08-how-to-understand-docker-container-cgroups-in-depth/view](https://oneuptime.com/blog/post/2026-02-08-how-to-understand-docker-container-cgroups-in-depth/view)  
33. Diagnosing Linux cgroups v2 Memory Throttling & OOM-Killed Containers \- Netdata, 3월 14, 2026에 액세스, [https://www.netdata.cloud/academy/diagnosing-linux-cgroups/](https://www.netdata.cloud/academy/diagnosing-linux-cgroups/)  
34. pacoxu, 3월 14, 2026에 액세스, [https://pacoxu.wordpress.com/](https://pacoxu.wordpress.com/)  
35. Limiting Container Resources — SingularityCE User Guide 4.1 documentation, 3월 14, 2026에 액세스, [https://docs.sylabs.io/guides/4.1/user-guide/cgroups.html](https://docs.sylabs.io/guides/4.1/user-guide/cgroups.html)  
36. Limiting Container Resources — Apptainer User Guide main documentation, 3월 14, 2026에 액세스, [https://apptainer.org/docs/user/main/cgroups.html](https://apptainer.org/docs/user/main/cgroups.html)  
37. Chapter 23\. Setting system resource limits for applications by using control groups | Managing, monitoring, and updating the kernel | Red Hat Enterprise Linux, 3월 14, 2026에 액세스, [https://docs.redhat.com/en/documentation/red\_hat\_enterprise\_linux/8/html/managing\_monitoring\_and\_updating\_the\_kernel/setting-limits-for-applications\_managing-monitoring-and-updating-the-kernel](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/setting-limits-for-applications_managing-monitoring-and-updating-the-kernel)  
38. How to Configure Memory Limits with Cgroups on Talos Linux \- OneUptime, 3월 14, 2026에 액세스, [https://oneuptime.com/blog/post/2026-03-03-configure-memory-limits-with-cgroups-on-talos-linux/view](https://oneuptime.com/blog/post/2026-03-03-configure-memory-limits-with-cgroups-on-talos-linux/view)  
39. Memory Controller · cgroup2, 3월 14, 2026에 액세스, [https://facebookmicrosites.github.io/cgroup2/docs/memory-controller.html](https://facebookmicrosites.github.io/cgroup2/docs/memory-controller.html)  
40. server/status: prefer \`memory.high\` for memory limit detection for cgroups v2 · Issue \#114774 · cockroachdb/cockroach \- GitHub, 3월 14, 2026에 액세스, [https://github.com/cockroachdb/cockroach/issues/114774](https://github.com/cockroachdb/cockroach/issues/114774)  
41. AgentCgroup: Understanding and Controlling OS Resources of AI Agents \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/publication/400661614\_AgentCgroup\_Understanding\_and\_Controlling\_OS\_Resources\_of\_AI\_Agents](https://www.researchgate.net/publication/400661614_AgentCgroup_Understanding_and_Controlling_OS_Resources_of_AI_Agents)  
42. Cgroup V2 memory limits and their potential for thrashing, 3월 14, 2026에 액세스, [https://utcc.utoronto.ca/\~cks/space/blog/linux/CgroupV2MemoryLimitsAndThrashing](https://utcc.utoronto.ca/~cks/space/blog/linux/CgroupV2MemoryLimitsAndThrashing)  
43. How do memory limits in Kubernetes work with cgroup v2 memory.high? \- Server Fault, 3월 14, 2026에 액세스, [https://serverfault.com/questions/1166165/how-do-memory-limits-in-kubernetes-work-with-cgroup-v2-memory-high](https://serverfault.com/questions/1166165/how-do-memory-limits-in-kubernetes-work-with-cgroup-v2-memory-high)  
44. cgroup: Add CgroupV2 \`memory.high\` and \`memory.low\` configs (\#5443) · Issue \- GitLab, 3월 14, 2026에 액세스, [https://gitlab.com/gitlab-org/gitaly/-/issues/5443](https://gitlab.com/gitlab-org/gitaly/-/issues/5443)  
45. Control Group v2 — The Linux Kernel documentation, 3월 14, 2026에 액세스, [https://www.kernel.org/doc/html/v6.1/admin-guide/cgroup-v2.html](https://www.kernel.org/doc/html/v6.1/admin-guide/cgroup-v2.html)  
46. Control Group v2 \- The Linux Kernel documentation, 3월 14, 2026에 액세스, [https://docs.kernel.org/admin-guide/cgroup-v2.html](https://docs.kernel.org/admin-guide/cgroup-v2.html)  
47. Practicing cgroup v2 \- by Charles Vissol \- Medium, 3월 14, 2026에 액세스, [https://medium.com/@charles.vissol/practicing-cgroup-v2-cad6743bba0c](https://medium.com/@charles.vissol/practicing-cgroup-v2-cad6743bba0c)  
48. AgentCgroup: Understanding and Controlling OS Resources of AI Agents \- arXiv.org, 3월 14, 2026에 액세스, [https://www.arxiv.org/pdf/2602.09345](https://www.arxiv.org/pdf/2602.09345)  
49. AgentSight: Keeping Your AI Agents Under Control with eBPF-Powered System Observability \- eunomia, 3월 14, 2026에 액세스, [https://eunomia.dev/en/blog/posts/agentsight\_paper/](https://eunomia.dev/en/blog/posts/agentsight_paper/)  
50. AgentCgroup: Understanding and Controlling OS Resources of AI Agents \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/pdf/2602.09345](https://arxiv.org/pdf/2602.09345)  
51. agentcgroup/agentcg/README.md at main · eunomia-bpf ... \- GitHub, 3월 14, 2026에 액세스, [https://github.com/eunomia-bpf/agentcgroup/blob/main/agentcg/README.md](https://github.com/eunomia-bpf/agentcgroup/blob/main/agentcg/README.md)  
52. \[Literature Review\] AgentCgroup: Understanding and Controlling, 3월 14, 2026에 액세스, [https://www.themoonlight.io/en/review/agentcgroup-understanding-and-controlling-os-resources-of-ai-agents](https://www.themoonlight.io/en/review/agentcgroup-understanding-and-controlling-os-resources-of-ai-agents)  
53. Running Self-Hosted LLMs on Kubernetes: A Complete Guide \- OneUptime, 3월 14, 2026에 액세스, [https://oneuptime.com/blog/post/2026-01-29-self-hosted-llms-on-kubernetes](https://oneuptime.com/blog/post/2026-01-29-self-hosted-llms-on-kubernetes)  
54. Deploy LLMs on Kubernetes: Complete Guide with Examples | by Amaresh Pelleti | Medium, 3월 14, 2026에 액세스, [https://medium.com/@amareswer/deploy-llms-on-kubernetes-complete-guide-with-examples-4fbd04d38d40](https://medium.com/@amareswer/deploy-llms-on-kubernetes-complete-guide-with-examples-4fbd04d38d40)  
55. Resource Management for Pods and Containers \- Kubernetes, 3월 14, 2026에 액세스, [https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)  
56. Kubernetes: Get the Most from Dynamic Resource Allocation \- The New Stack, 3월 14, 2026에 액세스, [https://thenewstack.io/kubernetes-get-the-most-from-dynamic-resource-allocation/](https://thenewstack.io/kubernetes-get-the-most-from-dynamic-resource-allocation/)  
57. Dynamic Resource Allocation | Kubernetes, 3월 14, 2026에 액세스, [https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/)  
58. Dynamically allocate devices to workloads with DRA | Google Kubernetes Engine (GKE), 3월 14, 2026에 액세스, [https://docs.cloud.google.com/kubernetes-engine/docs/how-to/deploy-dra-workloads](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/deploy-dra-workloads)  
59. Kubernetes 1.26: Alpha API For Dynamic Resource Allocation, 3월 14, 2026에 액세스, [https://kubernetes.io/blog/2022/12/15/dynamic-resource-allocation/](https://kubernetes.io/blog/2022/12/15/dynamic-resource-allocation/)  
60. Securing AI in Kubernetes: Best Practices for LLMs and RAGs \- Veeam, 3월 14, 2026에 액세스, [https://www.veeam.com/blog/securing-ai-kubernetes-llms-rags-protection.html](https://www.veeam.com/blog/securing-ai-kubernetes-llms-rags-protection.html)  
61. How are you bridging the context gap for AI agents in Kubernetes: Are we moving past traditional logs toward eBPF-driven "Agentic Ops"? | ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/post/How\_are\_you\_bridging\_the\_context\_gap\_for\_AI\_agents\_in\_Kubernetes\_Are\_we\_moving\_past\_traditional\_logs\_toward\_eBPF-driven\_Agentic\_Ops](https://www.researchgate.net/post/How_are_you_bridging_the_context_gap_for_AI_agents_in_Kubernetes_Are_we_moving_past_traditional_logs_toward_eBPF-driven_Agentic_Ops)  
62. Why Kubernetes Needs an “AI Sidecar” — and What It Should Look Like \- Medium, 3월 14, 2026에 액세스, [https://medium.com/@mrschneider/why-kubernetes-needs-an-ai-sidecar-and-what-it-should-look-like-36a826b53483](https://medium.com/@mrschneider/why-kubernetes-needs-an-ai-sidecar-and-what-it-should-look-like-36a826b53483)  
63. \[Whitepaper\] Monitoring Kubernetes: the sidecar pattern \- Sensu, 3월 14, 2026에 액세스, [https://sensu.io/resources/whitepaper/whitepaper-monitoring-kubernetes-the-sidecar-pattern](https://sensu.io/resources/whitepaper/whitepaper-monitoring-kubernetes-the-sidecar-pattern)  
64. Sidecar Containers \- Kubernetes, 3월 14, 2026에 액세스, [https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)  
65. How to Implement Kubernetes Sidecar Patterns \- OneUptime, 3월 14, 2026에 액세스, [https://oneuptime.com/blog/post/2026-01-30-kubernetes-sidecar-patterns/view](https://oneuptime.com/blog/post/2026-01-30-kubernetes-sidecar-patterns/view)  
66. Kubernetes Sidecar Containers: Use Cases and Best Practices \- groundcover, 3월 14, 2026에 액세스, [https://www.groundcover.com/blog/kubernetes-sidecar](https://www.groundcover.com/blog/kubernetes-sidecar)  
67. ebpf usecases analysis \- eunomia, 3월 14, 2026에 액세스, [https://eunomia.dev/others/usecases/](https://eunomia.dev/others/usecases/)  
68. AI Agent Sandboxing & Progressive Enforcement: The Complete Guide \- ARMO, 3월 14, 2026에 액세스, [https://www.armosec.io/blog/ai-agent-sandboxing-progressive-enforcement-guide/](https://www.armosec.io/blog/ai-agent-sandboxing-progressive-enforcement-guide/)  
69. Securely deploying AI agents \- Claude API Docs, 3월 14, 2026에 액세스, [https://platform.claude.com/docs/en/agent-sdk/secure-deployment](https://platform.claude.com/docs/en/agent-sdk/secure-deployment)  
70. How to sandbox AI agents in 2026: MicroVMs, gVisor & isolation strategies | Blog, 3월 14, 2026에 액세스, [https://northflank.com/blog/how-to-sandbox-ai-agents](https://northflank.com/blog/how-to-sandbox-ai-agents)  
71. A field guide to sandboxes for AI \- Luis Cardoso, 3월 14, 2026에 액세스, [https://www.luiscardoso.dev/blog/sandboxes-for-ai](https://www.luiscardoso.dev/blog/sandboxes-for-ai)

[image1]: <data:image/png;base64,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>