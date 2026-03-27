# DR-4.4 Ch.4 — Agent System Compute Requirements Benchmarking

**작성일**: 2026-03-21  
**관련 챕터**: Ch.4 (환경/제약 실험), Ch.5 (비용-신뢰도 해석), Ch.6 (Operational Compiler 경량화 기준)

> 이 문서는 Ch.4 실험 설계를 위한 연구 정리다.  
> 출판 원고에는 이 문서를 직접 인용하지 않고, 원문 출처를 확인해 직접 인용한다.

## 1. 연구 질문

1. agent runtime의 compute 요구사항을 어떤 단위로 측정해야 하는가?
2. 동일 task에서 model/harness/surface 차이가 compute profile에 어떤 형태로 반영되는가?
3. 저사양 VM(e2-micro 급)에서 "실행 가능"과 "재현 가능한 실험 가능"의 경계는 어디인가?

## 2. 핵심 결론

- agent compute 벤치마크는 평균 자원 사용량이 아니라 **피크/버스트/지연 꼬리(P99)** 를 중심으로 봐야 한다.
- compute 병목은 GPU 유무 이전에 CPU steal, RAM 압박, I/O 대기, 네트워크 지연이 결합되어 나타난다.
- e2-micro 급 환경은 실험에 유효하지만, "모든 기능을 한 VM에 올리는 구조"는 장기 실행에서 재현성 저하가 크다.
- tool-heavy agent의 실측에서는 도구 호출 구간에서 메모리/CPU가 비정상 버스트를 보이므로, 컨테이너/프로세스 단위 제어가 필수다.

## 3. 벤치마크 계측 프레임

### 3.1 필수 시스템 지표

- CPU: 평균, P95, P99, steal time
- Memory: RSS, peak RSS, OOM 이벤트 수
- Storage: read/write IOPS, queue depth, latency
- Network: API RTT, timeout rate, retry rate
- Runtime: TTFT, TPOT, wall-clock completion time

### 3.2 에이전트 지표와 결합

- TCR, IFR, TCA, MTTR, HOR과 시스템 지표를 동일 run id로 묶어서 저장
- 동일 task라도 "성공 run"과 "실패 run"의 리소스 곡선 차이를 비교

## 4. 환경 계층화 제안 (Ch.4 실험용)

| Tier | 예시 환경 | 목적 |
|---|---|---|
| Tier-L | e2-micro/free-tier | 실패 경계, 임계점 탐지 |
| Tier-M | 2~4 vCPU, 8~16GB RAM | 재현 가능한 본 실험 baseline |
| Tier-H | GPU/고성능 VM | 성능 상한 및 라우팅 비교 |

## 5. Ch.4 실험 직접 매핑

- E09/E10: long-horizon에서 CPU steal 증가와 goal drift 선후관계 기록
- E11: multi-agent 동시 실행 시 contention과 context 오염 선행 여부 비교
- E12: self-immune overhead의 compute 비용 계측
- E20: compute saturation 구간에서 harness=ON/OFF 역전 여부 확인

## 6. 최소 재현 프로토콜

1. 환경 스냅샷 고정(OS/Python/라이브러리 버전)
2. seed 고정 + task 입력 고정
3. run 당 시스템 메트릭 1~5초 간격 샘플링
4. 실패 run도 동일 포맷으로 저장
5. tier 간 비교 시 지표 정의를 바꾸지 않음

## 7. Ch.4 원고 반영용 문장 규칙

- "느려졌다" 대신 TTFT/TPOT/P99 지표로 수치화
- "자원 부족" 대신 OOM/steal/io-wait 이벤트를 명시
- compute 관련 결론은 반드시 task 성공/실패 지표와 함께 병기

## 8. 남은 검증 TODO

- tier별 비용 모델(시간당 비용 + 토큰 비용) 통합
- multi-agent N 증가에 따른 비선형 병목 지점 추정
- cgroup 제어 유무가 TCR/MTTR에 미치는 효과 계측

## 참고 출처 (원문 확인 대상)

- Google Cloud Compute Engine / E2 machine family 공식 문서
- Google Cloud Persistent Disk performance 문서
- Google Cloud Free Tier 공식 문서
- AgentCgroup: Understanding and Controlling OS Resources of AI Agents (arXiv:2602.09345)
- GPU-Virt-Bench (arXiv:2512.22125)
- NVIDIA KV cache bottleneck 최적화 기술 문서
- CNCF bare metal vs VM 컨테이너 아키텍처 가이드
