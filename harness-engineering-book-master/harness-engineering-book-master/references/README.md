# references/ — 사용 가이드

## 목적

DR 딥리서치는 직접 인용하지 않는다.
DR이 인용한 원문 중 공신력 있는 출처만 이 디렉토리에 정리해두고, 집필 시 이 목록에서 직접 인용한다.

## 파일

| 파일 | 내용 |
|---|---|
| `BIBLIOGRAPHY.md` | 모든 챕터 공신력 문헌 통합 목록 (A/B 등급 분류) |

## 신뢰도 등급

- **A등급**: arXiv 논문, ACL/NeurIPS/ICLR/ICML 게재, 동료심사 저널, Stanford HAI, DeepMind/MSR 공식 연구
- **B등급**: AWS/Google/NVIDIA/Microsoft/Netflix/OpenAI/Anthropic 공식 블로그, 공식 GitHub 저장소, McKinsey 보고서

## 인용하지 않는 출처 유형

- Reddit 게시물
- YouTube 영상
- 개인 Medium 블로그
- dev.to 개인 포스트 (주요 기업 공식 계정 제외)
- 비공식 비교 기사

## 업데이트 규칙

미시작 DR(1.2, 2.2, 3.1, 3.4, 4.x, 6.x, 7.1) 완료 시 `BIBLIOGRAPHY.md` 해당 챕터 섹션에 추가.
각 항목 형식:
```
- **[제목]**
  [저자/출처], [연도]
  DR출처: [DR-X.X] | 신뢰도: [A/B]
  URL: [url]
  요약: [한 줄 설명]
```
