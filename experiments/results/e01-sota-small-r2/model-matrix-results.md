# Model Matrix Results (Pilot)

- Generated: 2026-03-20T17:12:19.737500+00:00
- Runs/model: 2
- Harness: none

## T1_code_review

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| google/gemini-3.1-flash-lite-preview | 2 | 0 | 1 | 1 | 0.250 | 0.000 | 0.125 |
| google/gemini-2.5-flash-lite | 2 | 1 | 1 | 0 | 0.750 | 0.000 | 0.400 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| google/gemini-3.1-flash-lite-preview | google/gemini-2.5-flash-lite | -0.500 | 0.2482 | 0.2482 | False |

## T2_multi_step

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| google/gemini-3.1-flash-lite-preview | 2 | 2 | 0 | 0 | 1.000 | 1.000 | 0.600 |
| google/gemini-2.5-flash-lite | 2 | 2 | 0 | 0 | 1.000 | 0.000 | 0.000 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| google/gemini-3.1-flash-lite-preview | google/gemini-2.5-flash-lite | 0.000 | 1.0000 | 1.0000 | False |
