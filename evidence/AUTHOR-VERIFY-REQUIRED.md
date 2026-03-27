# 저자 직접 확인 필요 항목 — 2026-03-27

> 이 파일은 집필방향 재정렬 과정에서 도출된 실재성 검증 과제 목록이다.
> 출판 전에 저자(Kiwon)가 직접 확인하고 처리한다.

---

## 검증 원칙

책에 등장하는 모든 프로젝트·리포지토리는 GitHub에서 별(star) 100개 이상,
실제 커밋 이력이 있는 공개 리포지토리를 기준으로 인용한다.
확인 불가 또는 생성된 수치인 경우: 해당 수치 서술을 삭제하고 구조적 주장만 유지.

---

## 항목 목록

### 1. OpenClaw
- **현재 서술**: 250,829+ Stars, Node.js V8, 430K LoC, Peter Steinberger 개발
- **확인 필요**: 이 이름의 공개 GitHub 리포지토리가 존재하는가?
  Claude Code(Anthropic)를 포함한 실제 프레임워크의 익명화인가?
- **처리**: 실명 확인 시 실명 사용. 익명화인 경우 "이 책에서는 익명으로 서술한다" 각주 추가.
  수치(스타, LoC)가 생성된 것이면 삭제하고 "대규모 오픈소스 에이전트 프레임워크" 수준으로 서술.

### 2. ZeroClaw, Nanobot, NullClaw
- **현재 서술**: 각각 Rust 26,700+, Python 33,100+, Zig 678KB 수치 포함
- **확인 필요**: 실제 리포지토리 존재 여부 및 스타 수
- **처리**: 확인 불가 시 구체 수치 삭제. "Rust 기반 초경량 에이전트 프레임워크" 수준 서술 유지.

### 3. MiroFish
- **현재 서술**: Guo Hangjiang 학부생 개발, GitHub 18k+ Stars, 샨다 그룹 3,000만 위안 투자
- **확인 필요**: GitHub에서 "MiroFish" 또는 유사 swarm intelligence 에이전트 프로젝트 검색.
  투자 보도 출처(언론 기사) 확인.
- **처리**: 확인 시 실명 인용. 미확인 시 구체 수치·투자금 삭제, 구조적 관찰(군집 시스템에서
  개별 에이전트 harness 품질이 전체 신뢰도를 결정하는 패턴)만 유지.

### 4. gogcli, gws, mogcli
- **현재 서술**: 2026년 3월 9일 단일 주 안에 독립적으로 공개. gogcli(OpenClaw 개발자),
  gws(Google DevRel), mogcli(Microsoft CoreAI VP).
- **확인 필요**: GeekNews Weekly #348(2026-03-09)에서 언급된 실제 리포지토리 URL 확인.
  Justin Poehnelt(gws), Jared Palmer(mogcli)가 실제로 이 도구를 공개했는지.
- **처리**: 확인 시 실명 + URL 인용. 미확인 시 "동일 주에 독립적으로 공개된 CLI 도구들" 수준 서술.

### 5. Project Vend (Anthropic 자판기 에이전트 실험)
- **현재 서술**: Anthropic 내부 프로젝트. CEO 에이전트 "Seymour Cash". WSJ 레드팀 공격.
  Phase 1 자본금 20% 손실, Phase 2 흑자 전환. 모델: Sonnet 3.7→4.0→4.5.
- **확인 필요**: 이 사례의 공개 출처(논문, 블로그, 언론 보도) 존재 여부.
  Anthropic 공식 발표 또는 인용 가능한 출처인가?
- **처리**: 출처 있으면 인용 형식으로 서술. 출처 없으면 Preface와 §3에서
  "이 패턴이 보고된 사례" 수준으로 격하하거나 직접 관찰 사례로 대체.
  CEO 에이전트 이름 "Seymour Cash"는 픽션 캐릭터처럼 보이므로 삭제 검토.

---

## 처리 기한

Ch.1 최종 완성 전. Preface는 Project Vend 출처 확인 후 재검토.

---

## 처리 결과 기록

| 항목 | 확인 결과 | 처리 방법 | 처리 날짜 |
|------|-----------|-----------|----------|
| OpenClaw | | | |
| ZeroClaw/Nanobot/NullClaw | | | |
| MiroFish | | | |
| gogcli/gws/mogcli | | | |
| Project Vend | | | |
