# Model Matrix Results (Pilot)

- Generated: 2026-03-20T16:12:43.458522+00:00
- Runs/model: 1
- Harness: none

## T2_multi_step

| model | n | success | partial | fail | TCR(cont) | TCA | IFR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 1 | 1 | 0 | 0 | 1.000 | 0.000 | 0.000 |
| openai/gpt-5.4-nano | 1 | 1 | 0 | 0 | 1.000 | 1.000 | 0.200 |
| qwen/qwen3.5-9b | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| google/gemini-3.1-flash-lite-preview | 1 | 1 | 0 | 0 | 1.000 | 1.000 | 0.200 |

### Pairwise Significance (success rate)

| model_a | model_b | delta | p | p_holm | sig<0.05 |
| --- | --- | ---: | ---: | ---: | --- |
| nvidia/nemotron-3-super-120b-a12b | openai/gpt-5.4-nano | 0.000 | 1.0000 | 1.0000 | False |
| nvidia/nemotron-3-super-120b-a12b | qwen/qwen3.5-9b | 1.000 | 0.1573 | 0.9438 | False |
| nvidia/nemotron-3-super-120b-a12b | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| openai/gpt-5.4-nano | qwen/qwen3.5-9b | 1.000 | 0.1573 | 0.9438 | False |
| openai/gpt-5.4-nano | google/gemini-3.1-flash-lite-preview | 0.000 | 1.0000 | 1.0000 | False |
| qwen/qwen3.5-9b | google/gemini-3.1-flash-lite-preview | -1.000 | 0.1573 | 0.9438 | False |
