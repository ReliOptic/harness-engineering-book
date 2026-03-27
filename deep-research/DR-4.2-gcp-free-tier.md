# DR-4.2 Ch.4 — GCP Free Tier Constraints (Index)

**작성일**: 2026-03-21  
**관련 챕터**: Ch.4 (실험 환경), Ch.5 (비용/병목 해석)

## 문서 관계

- 이 파일은 Ch.4 집필용 요약 인덱스다.
- DR-4.2의 정식 상세 보고서는 아래 파일을 기준으로 한다.
  - `deep-research/DR-4.2-GCP-free-tier-constraints.md`

## 핵심 요약 (집필 반영용)

- e2-micro는 공유 코어 구조로 sustained 구간에서 CPU throttle이 발생할 수 있다.
- RAM 1GB 환경은 Python 기반 agent에서 OOM 위험이 높다.
- 표준 디스크 성능 한계(IOPS/throughput)가 tool-heavy 작업 지연을 유발한다.
- free-tier라고 해도 네트워크/고정 IP/NAT 구성에 따라 과금이 발생할 수 있다.
- 장기 실행 에이전트는 monolithic 단일 VM보다 역할 분리(제어 plane vs 실행 plane)가 안전하다.

## Ch.4로 연결되는 포인트

- §2 실험 환경: "제약은 불편이 아니라 실험 조건" 서술 근거
- E09~E12: compute 병목과 failure pattern 상관 분석 배경
- E20: saturation 반례 설계의 현실적 경계값 설명 근거

## 원문 확인 대상

- Google Cloud Free Tier 공식 문서
- Compute Engine E2 머신/디스크/네트워크 공식 문서
- `DR-4.2-GCP-free-tier-constraints.md`의 참고문헌 목록
