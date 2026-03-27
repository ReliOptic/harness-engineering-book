# Model Matrix Results (Pilot)

- Generated: 2026-03-20T17:09:18.145871+00:00
- Runs/model: 2
- Harness: none

## T1_code_review

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 2 | 1 | 1 | 0 | 0.750 | 0.000 | 0.025 |
| openai/gpt-5.4-nano | 2 | 0 | 2 | 0 | 0.500 | 0.000 | 1.000 |
| qwen/qwen3.5-9b | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| google/gemini-3.1-flash-lite-preview | 2 | 0 | 1 | 1 | 0.250 | 0.000 | 0.150 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| nvidia/nemotron-3-super-120b-a12b | openai/gpt-5.4-nano | 0.500 | 0.2482 | 1.0000 | False |
| nvidia/nemotron-3-super-120b-a12b | qwen/qwen3.5-9b | 0.500 | 0.2482 | 1.0000 | False |
| nvidia/nemotron-3-super-120b-a12b | google/gemini-3.1-flash-lite-preview | 0.500 | 0.2482 | 1.0000 | False |
| openai/gpt-5.4-nano | qwen/qwen3.5-9b | 0.000 | 1.0000 | 1.0000 | False |
| openai/gpt-5.4-nano | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| qwen/qwen3.5-9b | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |

## T2_multi_step

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 2 | 2 | 0 | 0 | 1.000 | 0.000 | 0.000 |
| openai/gpt-5.4-nano | 2 | 2 | 0 | 0 | 1.000 | 0.500 | 0.400 |
| qwen/qwen3.5-9b | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| google/gemini-3.1-flash-lite-preview | 2 | 2 | 0 | 0 | 1.000 | 1.000 | 0.200 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| nvidia/nemotron-3-super-120b-a12b | openai/gpt-5.4-nano | 0.000 | 1.0000 | 1.0000 | False |
| nvidia/nemotron-3-super-120b-a12b | qwen/qwen3.5-9b | 1.000 | 0.0455 | 0.2730 | False |
| nvidia/nemotron-3-super-120b-a12b | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| openai/gpt-5.4-nano | qwen/qwen3.5-9b | 1.000 | 0.0455 | 0.2730 | False |
| openai/gpt-5.4-nano | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| qwen/qwen3.5-9b | google/gemini-3.1-flash-lite-preview | -1.000 | 0.0455 | 0.2730 | False |
