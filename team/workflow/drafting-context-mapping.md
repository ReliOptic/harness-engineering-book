# Drafting Context Mapping

This document maps the generated deep-research summary files (`DR-X.X-summary.md`) to the specific chapters and sections in `chapter-map.md` to guide the drafter agent.

## Ch.1 — 지금 무슨 일이 일어나고 있는가

*   **Section 1~4. OpenClaw ecosystem & 대안 프레임워크**
    *   **Context File:** `DR-1.1-summary.md`
    *   **Instructions:** Use `DR-1.1-summary.md` to describe the monolithic AI agent dominance of OpenClaw and the subsequent fragmentation into micro-runtimes (lightweight, memory-safe, multi-agent frameworks) along with the adoption of advanced memory systems.
*   **Section 5~7. 에이전트 인터페이스 진화와 CLI 회귀**
    *   **Context File:** `DR-1.2-summary.md`
    *   **Instructions:** Use `DR-1.2-summary.md` to trace the shift from traditional UIs to agent-first surfaces (A2UI, Canvas, Voice, GUI Automation), explain the structural bloat of MCP, and detail the technical and economic rationale behind the market's return to agentic CLI.
*   **Section 8. AIE shout-out (Chip Huyen, AI Engineering, 2025)**
    *   **Context File:** `DR-1.3-summary.md`
    *   **Instructions:** Use `DR-1.3-summary.md` to explain the foundation of AI Engineering principles, focusing on Chip Huyen's insights regarding common pitfalls and architectural foundations in generative AI applications.

## Ch.2 — Agent가 모델로부터 무엇을 물려받는가

*   **Section 3. Capability Cliff & Benchmarks**
    *   **Context File:** `DR-2.1-summary.md`
    *   **Instructions:** Use `DR-2.1-summary.md` to explain how agent capabilities drop off dramatically under certain model benchmarks (e.g., SWE-bench, WebArena) and the taxonomy of failures.
*   **Section 5. Distillation Efficiency Frontier & Quantization Tax**
    *   **Context File:** `DR-2.3-summary.md`
    *   **Instructions:** Use `DR-2.3-summary.md` to detail how distillation and quantization affect model capability, focusing specifically on function calling performance and the efficiency trade-offs.
*   **Section 6. Mid-run model switching / Routing**
    *   **Context File:** `DR-2.2-summary.md`
    *   **Instructions:** Use `DR-2.2-summary.md` (OpenRouter analysis) to explain mid-run model switching, multi-provider request routing, fallback mechanisms, and cost-performance balancing.

## Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

*   **Section 1 & 4. Harness engineering이란 무엇인가 & AgentOps 정의**
    *   **Context File:** `DR-3.1-summary.md`
    *   **Instructions:** Use `DR-3.1-summary.md` to define the terminology of agent systems, separating agent harnesses, guardrails, and orchestration protocols (e.g., A2A, MCP).
*   **Section 7. CLI-Anything HARNESS.md — 독립적 수렴 사례**
    *   **Context File:** `DR-3.2-summary.md`
    *   **Instructions:** Use `DR-3.2-summary.md` to explain the CLI-Anything approach as a prime example of making software agent-native through HARNESS.md, showing practical application of harness engineering.
*   **Section 6 & 8. AgentOps 및 모니터링 생태계**
    *   **Context File:** `DR-3.3-summary.md`
    *   **Instructions:** Use `DR-3.3-summary.md` to describe the observability frameworks (Helicone, AgentOps, Weave, Braintrust) that enable tracking metrics like HOR (Harness Overhead Ratio) and MTTR.
*   **Agent Memory & Ontology (Supplementary for Harness)**
    *   **Context File:** `DR-3.4-summary.md`
    *   **Instructions:** Use `DR-3.4-summary.md` to incorporate ontology and memory structures as part of the agent's contextual engine and scaffold design.
