# Model Matrix Results (Pilot)

- Generated: 2026-03-20T16:03:27.966823+00:00
- Runs/model: 2
- Harness: none

## T1_code_review

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 2 | 0 | 2 | 0 | 0.500 | 0.000 | 0.000 |
| openai/gpt-5.4-nano | 2 | 2 | 0 | 0 | 1.000 | 0.000 | 0.600 |
| qwen/qwen3.5-9b | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| google/gemini-3.1-flash-lite-preview | 2 | 0 | 1 | 1 | 0.250 | 0.000 | 0.200 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| nvidia/nemotron-3-super-120b-a12b | openai/gpt-5.4-nano | -1.000 | 0.0455 | 0.2730 | False |
| nvidia/nemotron-3-super-120b-a12b | qwen/qwen3.5-9b | 0.000 | 1.0000 | 1.0000 | False |
| nvidia/nemotron-3-super-120b-a12b | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| openai/gpt-5.4-nano | qwen/qwen3.5-9b | 1.000 | 0.0455 | 0.2730 | False |
| openai/gpt-5.4-nano | google/gemini-3.1-flash-lite-preview | 1.000 | 0.0455 | 0.2730 | False |
| qwen/qwen3.5-9b | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
