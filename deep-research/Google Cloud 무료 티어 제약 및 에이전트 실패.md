# **Google Cloud 무료 티어(e2-micro) 환경 내 자율형 AI 에이전트 운영의 다차원적 제약 사항 및 시스템 실패 패턴 분석 보고서**

## **서론 및 클라우드 네이티브 AI 에이전트의 컴퓨팅 요구사항**

거대 언어 모델(Large Language Model, LLM)의 추론 능력이 비약적으로 향상됨에 따라, 단순한 질의응답을 넘어 외부 API와 상호작용하고 스스로 도구를 선택하며 다단계 추론(Chain of Thought)을 수행하는 자율형 AI 에이전트(Autonomous AI Agent) 시스템이 소프트웨어 아키텍처의 핵심으로 부상하고 있다. 이러한 에이전트 애플리케이션을 구축하기 위해 개발자들은 LangChain, LangGraph, AutoGPT, CrewAI와 같은 복잡한 추상화 프레임워크를 광범위하게 도입하고 있다. 이러한 프레임워크들은 본질적으로 대량의 대화 맥락(Context)을 메모리에 유지하고, 동시다발적인 비동기 네트워크 요청을 처리하며, 지속적인 상태 전이(State Transition)를 관리해야 하므로 상당한 컴퓨팅 자원을 요구한다.

이러한 상황에서 초기 개발 비용을 최소화하기 위해 개인 개발자와 스타트업들은 퍼블릭 클라우드 제공업체의 무료 티어(Free Tier) 인프라를 적극적으로 활용하려 시도한다. 그중에서도 Google Cloud Platform(GCP)의 Compute Engine 서비스가 제공하는 e2-micro 인스턴스 기반의 Always Free 프로그램은 가장 널리 선택되는 진입점 중 하나이다.1 해당 프로그램은 특정 북미 리전(us-central1, us-east1, us-west1 등)에서 매월 1대의 e2-micro 가상 머신 인스턴스, 30GB의 표준 영구 디스크(Standard Persistent Disk), 그리고 일정량의 무료 네트워크 이그레스(Egress) 대역폭을 영구적으로 제공한다.2

그러나 웹 서버나 단순한 스크립트를 구동하는 데 초점이 맞추어진 극소형 클라우드 인스턴스 위에서, 방대한 메모리 소비와 높은 I/O 대역폭을 요구하는 현대적인 AI 에이전트를 상시 운영(Always-on)하는 것은 필연적으로 아키텍처의 물리적 한계와 충돌하게 된다.5 GCP 무료 티어의 제약 사항은 단순히 사양이 낮다는 것을 넘어, 하이퍼바이저(Hypervisor) 레벨에서의 엄격한 자원 스로틀링(Throttling), 리눅스 커널의 극단적인 메모리 회수 매커니즘, 그리고 스토리지의 물리적 입출력 한계 등 시스템 전반에 걸친 복잡한 기술적 장벽을 형성한다.8

더욱이 클라우드 네트워크 라우팅 정책과 과금 체계의 맹점은 무료 티어 환경을 사용하고 있음에도 불구하고 예기치 않은 과금 쇼크(Billing Shock)를 유발하는 치명적인 실패 패턴으로 이어진다.11 본 보고서는 Google Cloud 무료 티어 환경이 지닌 구체적인 컴퓨팅, 메모리, 스토리지, 네트워크 제약 사항을 심층적으로 해부하고, 이 환경에서 LangChain 및 Python 비동기 기반의 AI 에이전트를 운영할 때 발생하는 연쇄적인 시스템 실패 패턴의 근본 원인을 운영체제와 클라우드 인프라 관점에서 규명한다. 아울러 이러한 제약을 극복하고 과금 위험을 회피하기 위한 클라우드 네이티브 아키텍처 최적화 전략을 제시한다.

## **Compute Engine 하드웨어 및 시스템 할당 제약의 심층 분석**

GCP의 무료 티어 인프라를 이해하기 위해서는 가상 머신에 물리적 자원이 어떻게 매핑되고 제어되는지를 파악하는 것이 필수적이다. e2-micro 인스턴스는 전용(Dedicated) 하드웨어 자원을 할당받는 것이 아니라, 호스트 서버의 물리적 코어를 다수의 가상 머신이 시분할(Time-slicing) 방식으로 공유하는 공유 코어(Shared-core) 아키텍처를 기반으로 작동한다.

### **CPU 컴퓨팅 자원의 동적 분할 및 버스트 크레딧 매커니즘**

Google Compute Engine의 E2 머신 제품군은 비용 효율성을 극대화하기 위해 설계되었으며, 그중에서도 e2-micro는 가장 낮은 수준의 지속적인 컴퓨팅 성능을 보장받는다.8 해당 인스턴스는 운영체제 상에서 2개의 가상 CPU(vCPU)를 보유한 것으로 인식되지만, 실제로는 각 vCPU가 물리적 코어의 12.5%에 해당하는 CPU 시간(CPU Time)만을 지속적으로 할당받을 수 있도록 엄격하게 제한되어 있다.10 결과적으로 e2-micro 인스턴스가 2개의 vCPU를 통해 확보할 수 있는 총 시스템 성능은 단일 물리 코어의 25%에 불과하다.10

이러한 극단적인 제한을 보완하고 단기적인 트래픽 급증을 처리하기 위해 GCP는 하이퍼바이저 레벨에서 CPU 버스트(Bursting) 기능을 제공한다.8 버스트 기능은 인스턴스의 부하가 12.5%의 기준선을 초과할 때, 가용 가능한 호스트 서버의 잉여 CPU 사이클을 활용하여 일시적으로 각 vCPU가 물리적 코어의 100% 성능에 도달할 수 있도록 허용하는 기술이다.8

하지만 이 버스트 자원은 토큰 버킷(Token Bucket) 알고리즘에 의해 통제되며, 크레딧 형태로 누적되고 소진된다.8 e2-micro의 경우, 인스턴스가 100%의 CPU 사용률을 지속할 때 버스트 상태를 유지할 수 있는 시간은 최대 30초에 불과하다.8

다음 표는 E2 공유 코어 머신 타입별 CPU 자원 할당 및 버스트 지속 시간의 물리적 한계를 비교한 것이다.

| 인스턴스 타입 | 가시적 vCPU 수 | 코어당 지속 보장 할당률 | 시스템 총 지속 CPU 비율 | 100% 부하 시 최대 버스트 시간 | 물리적 RAM 할당량 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| e2-micro | 2 | 12.5% | 25.0% | 30 초 | 1.0 GB |
| e2-small | 2 | 25.0% | 50.0% | 60 초 | 2.0 GB |
| e2-medium | 2 | 50.0% | 100.0% | 120 초 | 4.0 GB |

30초의 버스트 시간이 초과되어 누적된 CPU 크레딧이 모두 소진되면, 하이퍼바이저는 강제로 해당 가상 머신의 CPU 접근을 차단하고 12.5% 수준으로 자원을 스로틀링(Throttling)한다.10 이때 인스턴스 내부의 리눅스 운영체제에서는 프로세스가 실행을 대기하고 있음에도 불구하고 하이퍼바이저가 코어를 내어주지 않아 발생하는 대기 시간인 CPU Steal Time(%st) 지표가 급격히 상승하게 된다.17

AI 에이전트가 로컬에서 데이터를 임베딩하거나 대규모 JSON 페이로드를 역직렬화(Deserialization)하는 연산을 수행할 때, 이 작업이 30초를 초과하게 되면 CPU Steal Time의 급증과 함께 시스템 전체의 응답성이 마비되며 사실상 정지 상태에 빠지게 된다.10

### **절대적 메모리 한계와 OOM(Out of Memory) 처리 정책**

e2-micro 인스턴스가 지닌 또 다른 치명적 결함은 물리적 주메모리(RAM)가 단 1GB로 고정되어 있다는 점이다.4 이 1GB의 공간은 오로지 애플리케이션만을 위한 것이 아니다. 최신 우분투(Ubuntu)나 데비안(Debian) 리눅스 커널을 구동하고, systemd, journald, 보안 모니터링 에이전트, SSH 데몬 등을 백그라운드에서 실행하는 데 기본적으로 약 150MB에서 300MB의 메모리가 영구적으로 할당된다. 따라서 애플리케이션 환경이 실제로 가용할 수 있는 사용자 공간(User Space) 메모리는 약 700MB 남짓이다.

퍼블릭 클라우드 환경의 컴퓨팅 최적화 철학에 따라, GCP의 Compute Engine 기본 이미지들은 디스크의 불필요한 마모를 방지하고 예측 가능한 성능을 제공하기 위해 스왑 파티션(Swap Partition)이나 스왑 파일(Swap File)을 완전히 비활성화한 상태로 인스턴스를 프로비저닝한다.5 스왑 공간이 없다는 것은 물리적 메모리가 100% 한계에 도달하는 순간, 운영체제가 디스크 공간을 가상 메모리로 활용하여 시스템 다운을 지연시킬 수 있는 최후의 완충 지대가 전혀 존재하지 않음을 의미한다.

이러한 환경에서 애플리케이션 메모리 누수가 발생하거나 순간적인 데이터 로드로 인해 RAM 가용량이 고갈되면, 리눅스 커널은 시스템 커널 패닉을 방지하기 위해 즉각적으로 'OOM(Out of Memory) Killer' 메커니즘을 발동시킨다.6 OOM Killer는 내부 휴리스틱 알고리즘에 따라 메모리 점유율이 가장 높고 시스템의 안정성 유지에 덜 중요하다고 판단되는 프로세스에 가장 높은 oom\_score를 부여한 뒤, 자비 없이 SIGKILL 시그널을 전송하여 프로세스를 강제 종료(Kill)시킨다.5

이 과정은 애플리케이션 레벨의 예외 처리(Exception Handling)를 무시하고 OS 커널 레벨에서 즉각적으로 집행되므로, Python 스크립트나 AI 에이전트 애플리케이션은 사용자에게 어떠한 에러 로그나 타임아웃 메시지도 남기지 못한 채 침묵 속에서 증발해버리는(Silent Crash) 현상을 겪게 된다.5 관리자는 오직 SSH 접속을 통해 dmesg 명령어로 커널 링 버퍼를 조회하여 Out of memory: Killed process (python)라는 사후 로그를 확인함으로써 시스템 붕괴의 원인을 짐작할 수 있을 뿐이다.5

### **영구 디스크(Persistent Disk)의 구조적 성능 제약 및 과금 함정**

GCP의 무료 티어는 인스턴스 당 매월 최대 30GB의 '표준 영구 디스크(Standard Persistent Disk, pd-standard)' 스토리지를 무료로 제공한다.1 컴퓨팅 분야에서 디스크 입출력 성능은 애플리케이션의 반응 속도를 좌우하는 중추적인 역할을 하지만, GCP의 영구 디스크 성능 산정 방식은 디스크의 볼륨 크기(GB)에 정비례하여 최대 성능 한계선이 설정된다는 독특한 특징을 갖는다.9

표준 영구 디스크는 기계식 하드 디스크 드라이브(HDD) 스핀들 기반의 인프라 위에 구축되어 있으며, 주로 대규모 순차 입출력(Sequential I/O)이나 콜드 데이터 스토리지 목적으로 설계된 가장 낮은 등급의 스토리지이다.23 GCP 공식 문서에 명시된 성능 지표에 따르면, pd-standard의 경우 1GB당 Read IOPS(초당 입출력 횟수)는 0.75, Write IOPS는 1.5로 고정되어 있다.9

이를 무료 티어에서 제공되는 최대치인 30GB 용량에 대입하여 산출할 경우 다음과 같은 극단적인 성능 한계값에 도달한다.

| 스토리지 속성 | 단위 용량(GB)당 성능 한도 | 무료 티어 30GB 기준 총 최대 성능 | 최신 SSD(참고치) |
| :---- | :---- | :---- | :---- |
| Read IOPS | 0.75 IOPS / GB | 22.5 IOPS | 10,000+ IOPS |
| Write IOPS | 1.50 IOPS / GB | 45.0 IOPS | 10,000+ IOPS |
| Read Throughput | 0.12 MB/s / GB | 3.6 MB/s | 500+ MB/s |
| Write Throughput | (인스턴스 한도 적용) | 최대 400 MB/s (IOPS 병목으로 실도달 불가) | 500+ MB/s |

불과 22.5 단위의 Read IOPS와 45 단위의 Write IOPS는 현대적인 데이터베이스 시스템이나 빈번한 로깅을 수행하는 컨테이너 환경을 구동하기에는 사실상 불가능에 가까운 수치이다.9 이와 같은 극심한 I/O 병목 현상은 프로세서가 디스크로부터 데이터를 읽어오기 위해 끝없이 대기하게 만들며, I/O 대기열(Queue Depth) 포화로 인해 시스템 전반의 응답 시간을 수십 초에서 수 분 단위로 지연시킨다.7

더욱 문제가 되는 것은 GCP 콘솔의 인터페이스 설계로 인한 사용자 과금 함정(Billing Trap)이다. Google Cloud 콘솔에서 새로운 VM 인스턴스를 생성할 때, 부트 디스크의 기본 설정값은 pd-standard가 아닌 SSD 기반의 혼합형 스토리지인 균형 있는 영구 디스크(Balanced Persistent Disk, pd-balanced)로 지정되어 있다.23 pd-balanced는 기가바이트 당 6 IOPS를 제공하여 pd-standard 대비 훨씬 나은 성능을 보여주지만, 이는 Always Free 티어의 혜택 범위에 포함되지 않는다.24 사용자가 인스턴스 생성 과정에서 명시적으로 디스크 유형을 표준 디스크로 변경(Downgrade)하지 않을 경우, 월말에 스토리지 사용 명목으로 요금이 청구되며 무료 티어의 의미가 퇴색되는 결과를 초래한다.26

## **네트워크 트래픽 이그레스(Egress) 제한 및 과금 논리의 복잡성**

퍼블릭 클라우드 인프라를 도입할 때 관리자들을 가장 곤혹스럽게 만드는 요소는 복잡하게 얽힌 네트워크 과금 체계이며, 이그레스(Egress, 아웃바운드 데이터 전송) 비용은 클라우드 요금 폭탄을 유발하는 가장 주된 원인으로 지목된다.30 GCP 무료 티어 역시 네트워크 정책에 있어 여러 차례 개편을 거쳤으며, 서비스 라우팅 계층(Network Service Tiers)과 데이터 목적지에 따라 과금 방식이 완전히 달라지는 난해한 구조를 띠고 있다.

### **Premium Tier와 Standard Tier의 구조적 차이**

Google Cloud는 타 클라우드 제공업체와 차별화된 라우팅 선택권으로 프리미엄 티어(Premium Tier)와 스탠다드 티어(Standard Tier)라는 이원화된 네트워크 인프라를 제공한다.33

프리미엄 티어는 GCP 인스턴스에서 출발한 트래픽이 목적지 사용자와 가장 가까운 엣지(Edge) 포인트에 도달할 때까지 인터넷 서비스 제공자(ISP)의 퍼블릭 망을 타지 않고, 전적으로 Google의 자체 프라이빗 글로벌 광케이블 백본망을 통해 라우팅되는 방식이다.34 이 방식은 네트워크 혼잡도를 피하고 극히 낮은 지연 시간(Low Latency)과 높은 패킷 도달 신뢰성을 보장하지만, 상대적으로 높은 데이터 전송 비용을 수반한다.33 반면 스탠다드 티어는 데이터가 가상 머신이 위치한 리전을 벗어나자마자 곧바로 퍼블릭 인터넷(통신사 및 일반 ISP 네트워크)으로 던져지며, 전통적인 BGP 라우팅을 거쳐 목적지에 도달하는 방식이다.34 스탠다드 티어는 신뢰성이나 라우팅 최적화 면에서는 프리미엄 티어에 뒤처지지만 비용 효율성 면에서 큰 장점을 지닌다.33

### **역사적 과금 정책과 2026년 기준 100GB / 200GB 이그레스 무료 한도**

전통적으로 GCP Always Free 프로그램은 북미 지역(미국 서부, 중부, 동부 등)의 VM에서 출발하여 중국과 호주를 제외한 전 세계 목적지로 향하는 프리미엄 티어 네트워크 이그레스 트래픽을 매월 1GB로 엄격히 제한해 왔다.1 1GB라는 용량은 정적 텍스트 기반의 단순 웹페이지를 운영하기에는 적합할지 모르나, 대용량 이미지를 호스팅하거나 지속적인 API 통신을 수행하는 현대적 웹 애플리케이션 및 에이전트 환경에서는 며칠 만에 고갈될 수 있는 극소량의 한도이다.13

그러나 클라우드 시장의 벤더 락인(Vendor Lock-in) 해소 요구와 경쟁 심화에 따라, GCP는 네트워크 무료 할당 정책을 대폭 완화하는 중요한 결정을 내렸다.37 최근 업데이트된 정책에 따르면, 프리미엄 티어 환경에서 특정 자격을 충족하는 대상 목적지로 전송되는 '인터넷 데이터 전송 아웃(Internet data transfer out)' 한도가 매월 1GB에서 무려 100GB로 상향 조정되었다.37 이는 중소규모의 워크로드나 백엔드 에이전트가 외부 데이터베이스나 서드파티 API와 통신할 때 발생하는 이그레스 과금에 대한 엄청난 심리적, 재정적 완충재 역할을 한다.37

또한, 네트워크 계층을 스탠다드 티어(Standard Tier)로 전환할 경우, 퍼블릭 망을 사용한다는 전제 하에 계정 내 모든 리전을 합산하여 매월 최대 200GB의 아웃바운드 트래픽을 무료로 제공받을 수 있다.4

다음 표는 2026년 기준 GCP 네트워크 티어별 무료 제공 이그레스 트래픽 한도를 비교한 것이다.

| 네트워크 서비스 티어 | 라우팅 인프라 | 매월 무료 제공 아웃바운드 (Egress) 한도 | 초과 시 요금제 (북미 기준) |
| :---- | :---- | :---- | :---- |
| Premium Tier | Google 프라이빗 글로벌 백본 | 최대 100GB (인터넷 목적지 기준 상향) | \~$0.12 / GB |
| Standard Tier | 퍼블릭 인터넷 (트랜짓 ISP) | 최대 200GB (모든 리전 합산) | \~$0.085 / GB |

### **과금 쇼크를 유발하는 숨겨진 청구 항목**

그럼에도 불구하고 100GB나 200GB의 무료 이그레스 대역폭이 모든 네트워크 과금으로부터 사용자를 완벽히 보호해 주는 것은 아니다. 클라우드 네트워크 아키텍처의 복잡성으로 인해 사용자는 'Always Free'라는 문구 뒤에 숨겨진 다양한 형태의 인프라 사용 비용과 직면하게 된다.

가장 대표적인 숨겨진 비용은 **IPv4 고정 IP 대여료**이다.31 클라우드 제공업체들은 IPv4 주소의 글로벌 고갈 문제에 대응하기 위해 퍼블릭 IP 주소 할당에 대한 과금을 강화하고 있다. GCP 역시 인스턴스나 로드 밸런서, NAT 게이트웨이에 할당된 퍼블릭 IPv4 주소에 대해 시간당 과금을 적용하며, 이는 한 달 내내 가동할 경우 IP 주소 하나당 약 $3.65의 고정 비용을 발생시킨다.31 이 비용은 무료 티어 크레딧으로 상쇄되지 않으며, 인스턴스를 중지(Stop)해 두더라도 고정 IP를 예약(Reserve)한 상태로 유지하면 계속해서 요금이 부과된다.31

또한 **Cloud NAT 및 피어링 네트워크 비용** 역시 치명적인 과금 함정이다. 만약 보안 강화를 위해 e2-micro 인스턴스에 외부 공인 IP를 부여하지 않고, 내부 프라이빗 서브넷에 배치한 뒤 Cloud NAT를 통해 인터넷으로 아웃바운드 연결을 설정할 경우, NAT 게이트웨이의 시간당 가동 비용(월 약 $32.40)과 NAT가 처리하는 바이트(GB) 단위 데이터 처리 요금이 추가로 부과된다.31 이 과정에서 발생하는 데이터 전송 비용은 100GB 무료 이그레스 한도와 무관하게 청구될 수 있다. 더불어 목적지가 통신사 피어링 네트워크(Carrier Peering Network)를 거쳐 도달해야 하는 특정 로케이션일 경우, 예외적인 프리미엄 과금율이 적용되어 무료 티어를 우회한 요금이 청구되기도 한다.12

## **시간 기반 과금 풀(Pool)과 다중 인스턴스의 위험성**

GCP의 무료 티어 컴퓨팅 혜택은 특정 '단일 인스턴스' 자체를 무료로 영구 고정해 주는 물리적 개념이 아니라, 계정 단위로 '특정 시간 풀(Time Pool)'을 제공하는 논리적 크레딧 상계 방식으로 운영된다.3

매월 1일, GCP는 사용자의 계정에 해당 월의 전체 시간(예를 들어 31일이 있는 달의 경우 31일 x 24시간 \= 744시간)에 해당하는 e2-micro 컴퓨팅 크레딧을 채워 넣는다.3 사용자가 특정 북미 리전 내에 e2-micro 인스턴스를 하나 띄워 한 달 내내 24시간 중단 없이 실행한다면, 소비된 인스턴스 가동 시간이 할당된 744시간과 정확히 일치하므로 과금서 상에서 이 비용이 100% 할인(Discount) 처리되어 최종 0원으로 청구되는 매커니즘이다.27

그러나 이러한 논리적 구조는 치명적인 오작동 시나리오를 잉태한다. 만약 개발자가 여러 에이전트를 테스트하기 위해 리소스 격리 차원에서 동시에 2대의 e2-micro 인스턴스를 병렬로 생성하고 가동했다고 가정해 보자. GCP 시스템은 이를 차단하지 않고 정상적으로 가동을 허용한다. 하지만 이 2대의 인스턴스가 각각 시간을 소모하기 시작하므로, 744시간의 무료 크레딧 풀은 월 한 달이 채 지나기도 전인 약 15.5일(372시간 x 2대) 만에 완전히 고갈되어 버린다.3 무료 풀이 고갈된 이후 월말까지 남은 기간 동안 발생하는 2대 분량의 인스턴스 컴퓨팅 요금은 모두 정상가로 누적되어 신용카드로 청구된다.45

이 현상은 자동화된 오토스케일링(Auto-scaling) 그룹이나 관리형 인스턴스 그룹(MIG)을 테스트 용도로 잘못 설정하여 예기치 않게 인스턴스 수가 늘어나는 경우, 단 며칠 만에 수만 원 단위의 요금을 발생시키는 트리거로 작용한다. 시간 단위 과금 제도는 본질적으로 사용자가 언제든 인스턴스를 지우고 다시 생성할 수 있는 엄청난 유연성을 제공하지만, 그 대가로 인프라 운영자가 계정 내 인스턴스의 누적 구동 시간에 대해 철저한 감사를 수행해야 하는 책임의 무게를 지운다.

## **AI 에이전트 구동 시 발생하는 연쇄적 실패 패턴과 근본 원인 (Root Cause) 분석**

위에서 기술한 컴퓨팅(12.5% 지속 코어), 메모리(1GB 및 스왑 부재), 스토리지(22.5 IOPS), 네트워킹 한계는 독립적으로 작용하지 않는다. 이들은 서로 밀접하게 연관되어 병목을 유발하며, LangChain 기반의 복잡한 RAG(Retrieval-Augmented Generation) 파이프라인이나 AutoGPT, CrewAI와 같은 다중 에이전트 워크로드를 구동할 때 치명적이고 예측 불가능한 연쇄 붕괴(Cascading Failure)를 초래한다.48

### **패턴 1: 프레임워크 오버헤드와 1GB RAM의 충돌에 의한 OOM (Out-of-Memory) Silent Crash**

Python 언어로 작성된 AI 에이전트를 e2-micro 환경에 배포하는 순간 마주하는 가장 첫 번째이자 잦은 실패는 메모리 포화에 따른 강제 종료(OOM Kill)이다.5

LangChain, LangGraph, LlamaIndex와 같은 에이전트 오케스트레이션 프레임워크들은 내부적으로 수십 개의 Pydantic 모델, 데이터 직렬화/역직렬화 엔진, 수백 개의 의존성(Dependency) 패키지 트리를 로드한다.21 단지 애플리케이션 코드를 메모리에 적재(Import)하고 FastAPI 웹 서버를 띄우는 것만으로도 수백 메가바이트의 메모리가 초기화 과정에서 증발해버린다.50 여기에 더해 배포의 편의성을 위해 Docker 컨테이너 런타임 위에서 프로세스를 감쌀 경우, Docker 데몬이 사용하는 추가적인 오버헤드로 인해 실가용 메모리는 300\~400MB 이하로 급감한다.53

이 상태에서 외부 사용자가 들어와 에이전트에게 복잡한 질문을 던지고, 에이전트가 그 질문을 처리하기 위해 빅쿼리(BigQuery)에서 데이터를 불러오거나 거대한 크롤링 JSON 응답을 메모리에 할당(Deserialize)하게 되면, RAM 사용량은 순식간에 임계점(1GB)을 돌파하게 된다.6 특히 대화형 에이전트의 필수 요소인 ConversationBufferMemory와 같은 모듈은 대화 기록이 길어질수록 컨텍스트 문자열의 크기를 선형적으로 증가시키며 메모리 누수와 유사한 효과를 유발한다.55

리눅스 운영체제는 스왑 파티션이 비활성화된 상태에서 RAM을 초과하는 할당 요청이 들어오면, OOM Killer 메커니즘을 즉각 발동시켜 oom\_score가 가장 높은 프로세스(가장 뚱뚱해진 Python 에이전트 프로세스)의 목을 자른다.5 이때 Python 프로세스는 예외(Exception)를 포착할 시간조차 주어지지 않고 SIGKILL(-9) 신호를 받아 즉사하기 때문에, 사용자는 API가 무한히 로딩되다 끊어지는 현상을 보게 되며 서버에는 어떠한 파이썬 스택 트레이스 에러 로그도 남지 않는 유령 같은 크래시(Silent Crash)가 발생한다.5

다음 표는 일반적인 Python 기반 다중 에이전트 파이프라인 구동 시 초기화 및 런타임 메모리 할당 추정치를 보여준다 (e2-micro 1GB 한계 상황).

| 시스템 구성요소 | 추정 메모리 점유율 (상시) | 순간 피크(Peak) 점유율 | 비고 |
| :---- | :---- | :---- | :---- |
| OS 커널 및 필수 백그라운드 데몬 | \~200 MB | \~250 MB | sshd, systemd, GCP 에이전트 |
| 컨테이너 런타임 (Docker 데몬) | \~100 MB | \~150 MB | 도커 컨테이너 활용 시 |
| Python 런타임 및 에이전트 프레임워크 (LangChain) | \~250 MB | \~400 MB | Pydantic, HTTPX 등 패키지 종속성 |
| 대화 메모리 유지 및 대용량 JSON 파싱 | \~100 MB | **500+ MB** | **가변적, OOM 발생의 주원인** |
| **누적 메모리 요구량** | **\~650 MB** | **1,300+ MB** | **1GB(1024MB) 초과로 OOM Trigger** |

### **패턴 2: 스왑 우회 시도와 I/O 병목이 빚어내는 System Lock-up (Swap Thrashing)**

앞서 설명한 OOM 현상에 진저리가 난 수많은 개발자들은 리눅스의 fallocate와 mkswap 명령어를 이용해 임의로 2GB\~4GB 크기의 스왑 파일(Swap file)을 강제로 생성하고 활성화하는 우회 전략을 선택한다.5 이는 램이 부족할 때 디스크를 메모리처럼 빌려 쓰는 전통적인 해결책이지만, e2-micro의 30GB 표준 영구 디스크 위에서는 오히려 끔찍한 연쇄 재앙을 불러오는 기폭제가 된다.9

에이전트가 다량의 외부 문서를 요약하거나 크롤링한 데이터를 파싱하기 시작하면 RAM은 즉시 고갈되고 커널은 데이터를 스왑 공간(디스크)으로 밀어내는 페이징(Paging) 작업을 시작한다.57 문제는 pd-standard 30GB의 쓰기 성능 한도가 초당 불과 45 IOPS(입출력 횟수)라는 점에 있다.9 메모리와 디스크 사이에서 초당 수천 번의 미세한 페이지 인/아웃(Page In/Out) 요청이 빗발치는데, 디스크 컨트롤러는 초당 단 45회의 쓰기 동작만을 소화할 수 있으므로 엄청난 병목이 발생한다.

이러한 상태를 스왑 쓰래싱(Swap Thrashing)이라고 부른다.7 CPU는 스왑 파일에서 데이터를 읽고 쓰기를 기다리기 위해 자신의 사이클 대부분을 I/O 대기(I/O Wait, top 명령어에서의 %wa 지표) 상태로 허비하며 사실상 어떠한 유효한 연산도 수행하지 못하게 된다.17

이 상황이 발생하면 에이전트의 작동이 완전히 멈추는 것은 물론, OS 커널 자체가 디스크 응답을 대기하는 상태에 빠지므로 관리자가 문제 상황을 파악하기 위해 SSH로 인스턴스에 접속하려는 시도조차 타임아웃되어 불가능해진다.19 이 경우 사용자는 Google Cloud 콘솔에서 인스턴스를 강제로 강제 재부팅(Hard Reboot)시키는 것 외에는 시스템의 통제권을 되찾을 방법이 없다.58

### **패턴 3: CPU Steal Time 급증에 따른 비동기 이벤트 루프(Asyncio Event Loop) 질식**

최신 에이전트 프레임워크의 또 다른 특징은 외부 LLM API(예: OpenAI GPT, Anthropic Claude 등)나 서치 엔진(Tavily, SerpAPI 등)과의 통신 시 블로킹(Blocking)을 방지하고 동시성을 높이기 위해 Python의 asyncio 라이브러리를 적극적으로 활용한다는 것이다.60

Python의 asyncio는 단일 스레드(Single-thread) 내에서 동작하며, 운영체제의 epoll 시스템 콜을 활용하여 여러 코루틴(Coroutine) 간의 컨텍스트 스위칭을 관장하는 이벤트 루프(Event Loop) 아키텍처를 기반으로 한다.62 이 구조가 제 성능을 발휘하려면 이벤트 루프가 끊김 없이 주기적으로 CPU 사이클을 선점할 수 있어야 한다.61

그러나 e2-micro 환경에서는 30초의 버스트 크레딧이 바닥나면 하이퍼바이저가 가상 머신의 CPU 접근을 물리적으로 제한(Throttling)한다.8 앞서 설명한 CPU Steal Time(%st)이 치솟기 시작하면, 리눅스 커널 수준에서 실행 지연이 발생하며, 이는 고스란히 단일 스레드 기반의 Python 이벤트 루프를 장시간 동안 얼어붙게(Freeze) 만든다.10

이벤트 루프가 질식하면 외부 LLM 제공업체의 API로부터 수신된 패킷을 적절한 타이밍에 처리하지 못해 클라이언트 측의 소켓 타임아웃 예외(Socket Timeout Exception)가 대량으로 발생하게 된다.61 에이전트 입장에서는 LLM이 응답을 하지 않은 것으로 간주하여 동일한 추론 요청을 재전송(Retry)하게 되고, 이는 다시 CPU 부하를 발생시키는 악순환의 고리를 형성한다. Cloud Run과 같은 프론트엔드 환경이나 Nginx와 같은 리버스 프록시가 에이전트에게 라우팅을 시도하는 경우, 에이전트가 제때 응답하지 못해 사용자에게는 502 Bad Gateway 혹은 504 Gateway Time-out 에러가 반환된다.58

### **패턴 4: 재귀적 자율 루프에 의한 네트워크 이그레스 폭발과 과금 쇼크**

AI 에이전트, 특히 AutoGPT나 Firecrawl과 같은 능동적 크롤러가 결합된 아키텍처는 사용자의 단일 프롬프트 한 번으로 수십에서 수백 번의 후속 API 요청과 웹 페이지 크롤링을 스스로 수행하는 구조를 가진다.48 만약 개발자가 무료 티어의 100GB 혹은 200GB 네트워크 이그레스 한도를 맹신하고 에이전트의 재시도(Retry) 횟수나 크롤링 깊이(Depth)를 엄격히 제한하지 않은 채 배포한다면 심각한 과금 쇼크를 경험할 수 있다.11

에이전트가 앞서 언급한 CPU 지연이나 메모리 부족으로 인해 불완전한 파싱 에러를 겪게 될 경우, 에이전트는 환각(Hallucination)에 빠져 자신의 에러를 복구하기 위해 끊임없이 외부 검색 API를 호출하거나 무한 루프(Infinite Loop)를 돌며 대용량의 컨텍스트를 외부로 재전송하는 현상이 빈번하게 보고된다.11

이러한 무한 루프가 주말 동안 방치될 경우, 불과 이틀 만에 수백 GB의 이그레스 데이터가 외부로 빠져나가며 정상적인 사용 범위를 초과하게 된다.11 이는 기가바이트 당 약 $0.08 \~ $0.12의 비용을 발생시켜, 무료 서버를 운영하기 위해 생성했던 클라우드 계정에 수십 달러 이상의 청구서가 날아오는 뼈아픈 결과를 초래한다.31 통신사 피어링 네트워크와 같이 이그레스 비용이 비싼 라우트를 거치게 되면 그 타격은 배가된다.11

## **클라우드 네이티브 아키텍처 최적화 및 제약 우회 전략**

e2-micro 환경의 물리적 한계를 정면으로 돌파하려는 시도는 필연적으로 실패를 초래한다. 자율형 에이전트의 POC(Proof of Concept)나 경량 서비스 운영을 안정적으로 이끌어가기 위해서는, 한정된 자원을 억지로 짜내는 대신 시스템의 무거운 부분을 분리하여 외부로 위임(Offloading)하고 클라우드 네이티브 철학에 입각한 극단적 경량화 전략을 채택해야 한다.

### **1\. 무거운 프레임워크의 탈피와 경량화된 엔드포인트 설계**

수백 메가바이트의 메모리를 기본적으로 점유하는 거대한 LangChain 생태계와 무거운 객체 지향 추상화 계층을 과감히 걷어내는 것이 최적화의 첫걸음이다.49 메모리 한계가 1GB인 서버에서는 추상화가 제공하는 개발 편의성보다 런타임 메모리 효율이 절대적 우위를 점해야 한다.

LangChain 대신 가벼운 FastAPI 엔드포인트를 구축하고, 외부 LLM API(예: OpenAI, Anthropic 등)를 직접 호출하는 순수 Python 구현체로 에이전트 로직을 재작성하는 방식이 강력히 권장된다.51 다중 에이전트의 라우팅이나 도구 호출(Tool Calling)은 프레임워크에 의존하지 않고도 단순한 조건문 분기나 함수 호출 형태로 구성할 수 있으며, 이 방식을 취할 경우 초기 메모리 점유율을 100MB 이하 수준으로 방어할 수 있다.49

### **2\. 서버리스(Serverless) 전환과 상태 분리(Stateless Architecture)**

모놀리식(Monolithic) 접근 방식을 버리고, e2-micro 인스턴스에 부여된 짐을 분산시켜야 한다. 에이전트의 핵심 비즈니스 로직과 무거운 연산, 특히 외부 API와의 비동기 통신이 집중되는 부분은 컨테이너 기반 서버리스 서비스인 **Cloud Run**으로 분리 배포하는 것이 비용과 성능 측면에서 압도적으로 유리하다.2 Cloud Run은 매월 2백만 건의 요청을 항상 무료로 제공하며, 트래픽 유입 시에만 자원이 동적으로 스케일 아웃(Scale-out)되고 유휴 시에는 제로(0)로 축소되어 비용 누수를 막아준다.2

이와 함께, 인스턴스의 램(RAM) 메모리를 갉아먹는 대화 기록(Conversation History)이나 에이전트의 중간 상태(Intermediate State)를 로컬 메모리에 보관해서는 안 된다. 상태 데이터는 완전히 비국지화(Externalization)하여 GCP의 관리형 NoSQL 데이터베이스인 **Firestore**나 외부의 Redis 기반 KV 스토어에 위임해야 한다.2 Firestore 역시 매월 1GB의 스토리지를 무료로 제공하므로 2, 에이전트가 각 세션별 대화의 스냅샷과 상태 트랜지션 로그를 데이터베이스에 즉시 기록하고 로컬 램에서는 데이터를 해제하는 패턴(Stateless Agent)을 적용하면, 어떠한 대용량 질의가 들어오더라도 OOM 발생을 원천 차단할 수 있다.55

이 아키텍처 하에서 e2-micro 인스턴스는 단지 가벼운 크론 잡(Cron Job)을 돌리거나, 데이터베이스에서 이벤트를 구독하여 간헐적인 폴링(Polling)을 수행하는 극히 저부하의 오케스트레이션(Control Plane) 용도로만 제한적으로 활용되어야 한다.48

### **3\. 디스크 스왑 최소화 및 표준 스토리지 함정 회피**

OOM 킬러를 피하기 위해 스왑 파일을 설정해야만 하는 상황이라면, 반드시 리눅스의 커널 파라미터인 vm.swappiness 값을 1에서 10 사이의 극단적으로 낮은 값으로 조작해야 한다. 기본값(통상 60)을 유지할 경우 커널은 공격적으로 페이징을 시도하게 되지만, 낮은 값을 부여하면 물리적 램이 정말로 100% 한계에 도달해 붕괴하기 직전의 응급 상황에서만 최후의 보루로 디스크를 사용하도록 강제할 수 있으며, 이를 통해 22.5 IOPS의 디스크 병목을 유예할 수 있다.9

또한 인스턴스 초기 프로비저닝 과정에서 과금 함정을 피하기 위해, 부트 디스크 유형을 디폴트 값인 pd-balanced에서 반드시 pd-standard로 수동 변경해야만 완전 무료 혜택을 온전히 누릴 수 있다.23 더불어 디스크 I/O를 악화시키는 로컬 로깅(Local Logging)을 전면 금지하고, 모든 애플리케이션 로그와 에러 트레이스는 메모리 버퍼를 거쳐 Google Cloud Logging API(Ops Agent)로 비동기 전송되도록 파이프라인을 구축해야 스토리지의 극심한 지연을 회피할 수 있다.7

### **4\. 네트워크 이그레스 폭탄 방어 설계**

무료 티어 네트워크의 맹점으로 인한 과금 쇼크를 막기 위한 다중 방어막 구축이 필수적이다.

첫째, 지연 시간에 극도로 민감한 프로덕션 서비스가 아니라면, 인스턴스의 네트워크 계층 설정을 100GB 프리미엄 티어(인터넷 목적지 한정)에 의존하는 대신 \*\*스탠다드 티어(Standard Tier)\*\*로 명시적으로 변경하여 계정 전체적으로 200GB의 넉넉한 퍼블릭 망 무료 이그레스 대역폭을 확보하는 것이 안전하다.4

둘째, 고정 IPv4 주소 사용에 따른 월 고정 비용($3.65)을 피하기 위해 임시(Ephemeral) IP를 활용하거나, DDNS(Dynamic DNS) 솔루션을 결합해 유동 IP 기반의 라우팅 구조를 갖추어야 한다.31

셋째, 어플리케이션 계층에서의 방어이다. 에이전트의 무한 루프나 재귀적 웹 크롤링 시도를 원천 차단하기 위해, 코드 레벨에서 지수 백오프(Exponential Backoff)를 적용한 엄격한 재시도 횟수 제한(Max Retry Limit)을 강제해야 한다.11 외부로 전송되는 모든 데이터 페이로드는 GZIP 등을 통해 압축하여 이그레스 바이트 크기를 최소화하고, 빈번하게 요청되는 LLM 답변이나 임베딩 텍스트는 로컬 메모리 캐시(LRU)나 외부 인메모리 스토어에 적재하여 외부 네트워크 통신을 극단적으로 억제해야 한다.69

마지막으로, 클라우드 운영의 기본 원칙인 청구 예산 알림(Budgets and Alerts)을 Cloud Billing 콘솔에서 필수로 구성해야 한다. 누적 비용이 $0.1 이상의 미세한 금액이라도 발생하는 즉시 이메일이나 웹훅을 통해 알림이 발생하도록 구성하여, 에이전트의 오작동이나 정책 위반으로 인한 대규모 과금을 조기에 탐지하고 인스턴스를 즉각 정지시킬 수 있는 자동화된 보안망을 갖추어야만 구글 클라우드 무료 티어의 혜택을 안전하게 온존할 수 있다.12

#### **참고 자료**

1. Compute Engine | Google Cloud, 3월 13, 2026에 액세스, [https://cloud.google.com/products/compute](https://cloud.google.com/products/compute)  
2. Free Trial and Free Tier Services and Products \- Google Cloud, 3월 13, 2026에 액세스, [https://cloud.google.com/free](https://cloud.google.com/free)  
3. Upgraded from f1-micro to e2-micro for Always Free tier? : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/plbi7y/upgraded\_from\_f1micro\_to\_e2micro\_for\_always\_free/](https://www.reddit.com/r/googlecloud/comments/plbi7y/upgraded_from_f1micro_to_e2micro_for_always_free/)  
4. GitHub \- cloudcommunity/Cloud-Free-Tier-Comparison: Comparing the free tier offers of the major cloud providers like AWS, Azure, GCP, Oracle etc., 3월 13, 2026에 액세스, [https://github.com/cloudcommunity/Cloud-Free-Tier-Comparison](https://github.com/cloudcommunity/Cloud-Free-Tier-Comparison)  
5. Debugging and Preventing Out-of-Memory (OOM) Issues on Google Compute Engine, 3월 13, 2026에 액세스, [https://medium.com/@moksh.9/debugging-and-preventing-out-of-memory-oom-issues-on-google-compute-engine-1be055554ba3](https://medium.com/@moksh.9/debugging-and-preventing-out-of-memory-oom-issues-on-google-compute-engine-1be055554ba3)  
6. Python process OOM killed on Vertex AI despite low data size \- Stack Overflow, 3월 13, 2026에 액세스, [https://stackoverflow.com/questions/78306360/python-process-oom-killed-on-vertex-ai-despite-low-data-size](https://stackoverflow.com/questions/78306360/python-process-oom-killed-on-vertex-ai-despite-low-data-size)  
7. How to Troubleshoot Compute Engine VM Performance Issues \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-17-how-to-troubleshoot-compute-engine-vm-performance-issues-using-cloud-monitoring-metrics/view](https://oneuptime.com/blog/post/2026-02-17-how-to-troubleshoot-compute-engine-vm-performance-issues-using-cloud-monitoring-metrics/view)  
8. General-purpose machine family for Compute Engine \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/general-purpose-machines](https://docs.cloud.google.com/compute/docs/general-purpose-machines)  
9. Persistent Disk performance overview | Compute Engine \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/disks/performance](https://docs.cloud.google.com/compute/docs/disks/performance)  
10. Are the e2 instances throttled? : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/rc8ye9/are\_the\_e2\_instances\_throttled/](https://www.reddit.com/r/googlecloud/comments/rc8ye9/are_the_e2_instances_throttled/)  
11. GCP Egress Cost: Everything you should Know \- Tata Communications, 3월 13, 2026에 액세스, [https://www.tatacommunications.com/knowledge-base/mcc/gcp-egress-cost](https://www.tatacommunications.com/knowledge-base/mcc/gcp-egress-cost)  
12. Why am I being charged on Google Free Tier Compute Engine?? : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/1qan2ix/why\_am\_i\_being\_charged\_on\_google\_free\_tier/](https://www.reddit.com/r/googlecloud/comments/1qan2ix/why_am_i_being_charged_on_google_free_tier/)  
13. Free Tier : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/sgs1es/free\_tier/](https://www.reddit.com/r/googlecloud/comments/sgs1es/free_tier/)  
14. E2 CPU Usage Goes Up Over Time on Google Compute Engine \[closed\] \- Stack Overflow, 3월 13, 2026에 액세스, [https://stackoverflow.com/questions/66120638/e2-cpu-usage-goes-up-over-time-on-google-compute-engine](https://stackoverflow.com/questions/66120638/e2-cpu-usage-goes-up-over-time-on-google-compute-engine)  
15. Key concepts for burstable performance instances \- Amazon Elastic Compute Cloud, 3월 13, 2026에 액세스, [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html)  
16. Troubleshooting compute instance performance issues \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-performance](https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-performance)  
17. Understanding CPU Steal Time \- when should you be worried? \- Scout Monitoring, 3월 13, 2026에 액세스, [https://www.scoutapm.com/blog/understanding-cpu-steal-time-when-should-you-be-worried](https://www.scoutapm.com/blog/understanding-cpu-steal-time-when-should-you-be-worried)  
18. Very high CPU Steal Time with "t2.micro" located on "us-east-2b" | AWS re:Post, 3월 13, 2026에 액세스, [https://repost.aws/questions/QUEyNT7rncQnaA-x0DXRWGgg/very-high-cpu-steal-time-with-t2-micro-located-on-us-east-2b](https://repost.aws/questions/QUEyNT7rncQnaA-x0DXRWGgg/very-high-cpu-steal-time-with-t2-micro-located-on-us-east-2b)  
19. SSH Connection Issues and CPU Usage Spikes on GCP Free Tier with e2-micro Instance, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/18qqa19/ssh\_connection\_issues\_and\_cpu\_usage\_spikes\_on\_gcp/](https://www.reddit.com/r/googlecloud/comments/18qqa19/ssh_connection_issues_and_cpu_usage_spikes_on_gcp/)  
20. Understanding dynamic resource management in E2 VMs | Google Cloud Blog, 3월 13, 2026에 액세스, [https://cloud.google.com/blog/products/compute/understanding-dynamic-resource-management-in-e2-vms](https://cloud.google.com/blog/products/compute/understanding-dynamic-resource-management-in-e2-vms)  
21. Open Source TypeScript Large Language Models (LLM) \- SourceForge, 3월 13, 2026에 액세스, [https://sourceforge.net/directory/large-language-models-llm/typescript/](https://sourceforge.net/directory/large-language-models-llm/typescript/)  
22. Troubleshoot OOM events | Google Kubernetes Engine (GKE), 3월 13, 2026에 액세스, [https://docs.cloud.google.com/kubernetes-engine/docs/troubleshooting/oom-events](https://docs.cloud.google.com/kubernetes-engine/docs/troubleshooting/oom-events)  
23. Persistent Disk | Compute Engine \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/disks/persistent-disks](https://docs.cloud.google.com/compute/docs/disks/persistent-disks)  
24. Google Cloud Persistent Disk Explainer | NetApp, 3월 13, 2026에 액세스, [https://www.netapp.com/learn/gcp-cvo-blg-google-cloud-persistent-disk-explainer/](https://www.netapp.com/learn/gcp-cvo-blg-google-cloud-persistent-disk-explainer/)  
25. How to Migrate a Compute Engine Persistent Disk Between Standard \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-17-how-to-migrate-a-compute-engine-persistent-disk-between-standard-and-ssd-storage-types/view](https://oneuptime.com/blog/post/2026-02-17-how-to-migrate-a-compute-engine-persistent-disk-between-standard-and-ssd-storage-types/view)  
26. E2 Micro not free as Google free tier claims : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/p91j7l/e2\_micro\_not\_free\_as\_google\_free\_tier\_claims/](https://www.reddit.com/r/googlecloud/comments/p91j7l/e2_micro_not_free_as_google_free_tier_claims/)  
27. Why gcp compute engine in free tier actually not free? : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/17loepc/why\_gcp\_compute\_engine\_in\_free\_tier\_actually\_not/](https://www.reddit.com/r/googlecloud/comments/17loepc/why_gcp_compute_engine_in_free_tier_actually_not/)  
28. How to Tune Persistent Disk IOPS and Throughput by Selecting Correct Disk Type, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-17-how-to-tune-persistent-disk-iops-and-throughput-by-selecting-correct-disk-type-and-size/view](https://oneuptime.com/blog/post/2026-02-17-how-to-tune-persistent-disk-iops-and-throughput-by-selecting-correct-disk-type-and-size/view)  
29. How do I need to configure the free tier e2-micro vm? : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/1hw209y/how\_do\_i\_need\_to\_configure\_the\_free\_tier\_e2micro/](https://www.reddit.com/r/googlecloud/comments/1hw209y/how_do_i_need_to_configure_the_free_tier_e2micro/)  
30. The Hidden Costs In Google Cloud Platform You Need To Know \- Medium, 3월 13, 2026에 액세스, [https://medium.com/google-cloud/the-hidden-costs-in-google-cloud-platform-you-need-to-know-9342b7fc1e0c](https://medium.com/google-cloud/the-hidden-costs-in-google-cloud-platform-you-need-to-know-9342b7fc1e0c)  
31. The Hidden Cloud Tax: How IPv4 Rent and Egress Fees Are Silently Crushing 2026 Budgets | CloudCostChefs, 3월 13, 2026에 액세스, [https://www.cloudcostchefs.com/blog/cloud-networking-costs-ipv4-egress-2026](https://www.cloudcostchefs.com/blog/cloud-networking-costs-ipv4-egress-2026)  
32. GCP Egress Pricing | Tips to Avoid Hidden Fees \- CloudBolt, 3월 13, 2026에 액세스, [https://www.cloudbolt.io/gcp-cost-optimization/gcp-egress-pricing/](https://www.cloudbolt.io/gcp-cost-optimization/gcp-egress-pricing/)  
33. How to Compare and Choose Between Premium and Standard Network Service Tiers \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-17-how-to-compare-and-choose-between-premium-and-standard-network-service-tiers-on-google-cloud/view](https://oneuptime.com/blog/post/2026-02-17-how-to-compare-and-choose-between-premium-and-standard-network-service-tiers-on-google-cloud/view)  
34. Network Service Tiers overview \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/network-tiers/docs/overview](https://docs.cloud.google.com/network-tiers/docs/overview)  
35. Network pricing \- Google Cloud, 3월 13, 2026에 액세스, [https://cloud.google.com/vpc/network-pricing](https://cloud.google.com/vpc/network-pricing)  
36. GCP Always Free Tier \- LowEndTalk, 3월 13, 2026에 액세스, [https://lowendtalk.com/discussion/179990/gcp-always-free-tier](https://lowendtalk.com/discussion/179990/gcp-always-free-tier)  
37. Navigating Google Cloud Egress: What to Expect for 2025 \- Oreate AI Blog, 3월 13, 2026에 액세스, [http://oreateai.com/blog/navigating-google-cloud-egress-what-to-expect-for-2025/8bc57118fae799886b0a82fb49d02478](http://oreateai.com/blog/navigating-google-cloud-egress-what-to-expect-for-2025/8bc57118fae799886b0a82fb49d02478)  
38. Amazon AWS Joins Google Cloud In Removing Egress Costs \- Forrester, 3월 13, 2026에 액세스, [https://www.forrester.com/blogs/aws-joins-google-cloud-in-removing-egress-costs/](https://www.forrester.com/blogs/aws-joins-google-cloud-in-removing-egress-costs/)  
39. Free data transfer out to internet when moving out of AWS, 3월 13, 2026에 액세스, [https://aws.amazon.com/blogs/aws/free-data-transfer-out-to-internet-when-moving-out-of-aws/](https://aws.amazon.com/blogs/aws/free-data-transfer-out-to-internet-when-moving-out-of-aws/)  
40. Announcement of pricing changes for Cloud Storage | Google Cloud, 3월 13, 2026에 액세스, [https://cloud.google.com/storage/pricing-announce](https://cloud.google.com/storage/pricing-announce)  
41. Free Google Cloud features and trial offer, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/free/docs/free-cloud-features](https://docs.cloud.google.com/free/docs/free-cloud-features)  
42. Does e2-micro 'always free' work with standard tier 200gb free egress? \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/1k7c2xt/does\_e2micro\_always\_free\_work\_with\_standard\_tier/](https://www.reddit.com/r/googlecloud/comments/1k7c2xt/does_e2micro_always_free_work_with_standard_tier/)  
43. does standard tier network circumvent the 1GB/month free egress limit? \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/16a84q1/does\_standard\_tier\_network\_circumvent\_the/](https://www.reddit.com/r/googlecloud/comments/16a84q1/does_standard_tier_network_circumvent_the/)  
44. Networking overview for VMs | Compute Engine \- Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/networking/network-overview](https://docs.cloud.google.com/compute/docs/networking/network-overview)  
45. Is this true? GCP provides e2-micro always free : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/1kjw4u7/is\_this\_true\_gcp\_provides\_e2micro\_always\_free/](https://www.reddit.com/r/googlecloud/comments/1kjw4u7/is_this_true_gcp_provides_e2micro_always_free/)  
46. Google Cloud Free Tier VM : r/googlecloud \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/googlecloud/comments/13n78i6/google\_cloud\_free\_tier\_vm/](https://www.reddit.com/r/googlecloud/comments/13n78i6/google_cloud_free_tier_vm/)  
47. How to set up an Always Free compute instance \- Google Groups, 3월 13, 2026에 액세스, [https://groups.google.com/g/gce-discussion/c/Ll1BfUNtnQ0](https://groups.google.com/g/gce-discussion/c/Ll1BfUNtnQ0)  
48. Langchain, Langchain.js, vs AutoGPT for local agent development : r/LocalLLaMA \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/13svump/langchain\_langchainjs\_vs\_autogpt\_for\_local\_agent/](https://www.reddit.com/r/LocalLLaMA/comments/13svump/langchain_langchainjs_vs_autogpt_for_local_agent/)  
49. I am considering using Langchain but unsure given the feedback I'm seeing online \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LangChain/comments/1j8l2qi/i\_am\_considering\_using\_langchain\_but\_unsure\_given/](https://www.reddit.com/r/LangChain/comments/1j8l2qi/i_am_considering_using_langchain_but_unsure_given/)  
50. AI vs Human Cost Efficiency in Call Centers | PDF \- Scribd, 3월 13, 2026에 액세스, [https://www.scribd.com/document/903682546/ChatGPT-AI-vs-Human-Cost-LLM-Orchestrator](https://www.scribd.com/document/903682546/ChatGPT-AI-vs-Human-Cost-LLM-Orchestrator)  
51. Rejected for not using LangChain/LangGraph? : r/LocalLLaMA \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1ow3anq/rejected\_for\_not\_using\_langchainlanggraph/](https://www.reddit.com/r/LocalLLaMA/comments/1ow3anq/rejected_for_not_using_langchainlanggraph/)  
52. How to Deploy LangChain Applications on Cloud Run with Vertex AI Backend \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-17-how-to-deploy-langchain-applications-on-cloud-run-with-vertex-ai-backend/view](https://oneuptime.com/blog/post/2026-02-17-how-to-deploy-langchain-applications-on-cloud-run-with-vertex-ai-backend/view)  
53. Web application for personal use using Compute Engine in Free Tier \- Stack Overflow, 3월 13, 2026에 액세스, [https://stackoverflow.com/questions/77539625/web-application-for-personal-use-using-compute-engine-in-free-tier](https://stackoverflow.com/questions/77539625/web-application-for-personal-use-using-compute-engine-in-free-tier)  
54. How to Fix 'AI Platform' Training Errors \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-01-24-ai-platform-training-errors/view](https://oneuptime.com/blog/post/2026-01-24-ai-platform-training-errors/view)  
55. My LangChain agent used to repeat the same mistakes every run. Added persistent memory — now it learns from failures automatically. \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LangChain/comments/1rpuoxz/my\_langchain\_agent\_used\_to\_repeat\_the\_same/](https://www.reddit.com/r/LangChain/comments/1rpuoxz/my_langchain_agent_used_to_repeat_the_same/)  
56. LLM Poc Roadmap | PDF | Postgre Sql \- Scribd, 3월 13, 2026에 액세스, [https://www.scribd.com/document/903682572/Llm-Poc-Roadmap](https://www.scribd.com/document/903682572/Llm-Poc-Roadmap)  
57. How to run DNF without going OOM on GCP e2-micro \- Server Fault, 3월 13, 2026에 액세스, [https://serverfault.com/questions/1120367/how-to-run-dnf-without-going-oom-on-gcp-e2-micro](https://serverfault.com/questions/1120367/how-to-run-dnf-without-going-oom-on-gcp-e2-micro)  
58. Installation takes forever, then ends without forum actually starting \- Self-hosting \- Discourse Meta, 3월 13, 2026에 액세스, [https://meta.discourse.org/t/installation-takes-forever-then-ends-without-forum-actually-starting/343609?tl=en](https://meta.discourse.org/t/installation-takes-forever-then-ends-without-forum-actually-starting/343609?tl=en)  
59. Known issues | Compute Engine | Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/compute/docs/troubleshooting/known-issues](https://docs.cloud.google.com/compute/docs/troubleshooting/known-issues)  
60. How to Monitor Asyncio Event Loop Performance with OpenTelemetry Metrics \- OneUptime, 3월 13, 2026에 액세스, [https://oneuptime.com/blog/post/2026-02-06-monitor-asyncio-event-loop-performance-opentelemetry/view](https://oneuptime.com/blog/post/2026-02-06-monitor-asyncio-event-loop-performance-opentelemetry/view)  
61. Event loop load metrics · Issue \#322 · MagicStack/uvloop \- GitHub, 3월 13, 2026에 액세스, [https://github.com/MagicStack/uvloop/issues/322](https://github.com/MagicStack/uvloop/issues/322)  
62. Is there a way to tell if an asyncio event loop is at full capacity? \- Stack Overflow, 3월 13, 2026에 액세스, [https://stackoverflow.com/questions/58021338/is-there-a-way-to-tell-if-an-asyncio-event-loop-is-at-full-capacity](https://stackoverflow.com/questions/58021338/is-there-a-way-to-tell-if-an-asyncio-event-loop-is-at-full-capacity)  
63. Overhead of Python asyncio tasks | Hacker News, 3월 13, 2026에 액세스, [https://news.ycombinator.com/item?id=35073136](https://news.ycombinator.com/item?id=35073136)  
64. OpenClaw Guide: Build a Personal Agent with Internet Access Using Firecrawl, 3월 13, 2026에 액세스, [https://www.firecrawl.dev/blog/openclaw-firecrawl-guide](https://www.firecrawl.dev/blog/openclaw-firecrawl-guide)  
65. Why are people hating LangChain so much, organisations are also not preferring projects built on top of LangChain \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/LangChain/comments/1gmfyi2/why\_are\_people\_hating\_langchain\_so\_much/](https://www.reddit.com/r/LangChain/comments/1gmfyi2/why_are_people_hating_langchain_so_much/)  
66. Running Large Language Models on Google Cloud Platform via Cloud Run, VertexAI and PubSub \- LLMOps on GCP \- Mark Edmondson, 3월 13, 2026에 액세스, [https://code.markedmondson.me/running-llms-on-gcp/](https://code.markedmondson.me/running-llms-on-gcp/)  
67. Troubleshoot the Logging agent | Google Cloud Documentation, 3월 13, 2026에 액세스, [https://docs.cloud.google.com/logging/docs/agent/logging/troubleshooting](https://docs.cloud.google.com/logging/docs/agent/logging/troubleshooting)  
68. Better access to observability data for Virtual Machines | Google Cloud Blog, 3월 13, 2026에 액세스, [https://cloud.google.com/blog/products/operations/better-access-to-observability-data-for-virtual-machines](https://cloud.google.com/blog/products/operations/better-access-to-observability-data-for-virtual-machines)  
69. Google Cloud Pricing Models and Examples for 11 Services \[2025\] \- Finout, 3월 13, 2026에 액세스, [https://www.finout.io/blog/google-cloud-pricing](https://www.finout.io/blog/google-cloud-pricing)  
70. Pricing Overview | Google Cloud, 3월 13, 2026에 액세스, [https://cloud.google.com/pricing](https://cloud.google.com/pricing)