# 평가 결과: day3-step1-prompt

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 180건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 96% | 94% | 81% ±1 | 80% | 73% | 9.8 | 27.1 | $0.0046 |
| baseline | 96% | 94% | 81% ±1 | 80% | 93% | 1.0 | 10.3 | $0.0017 |

## 유형: keyword

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 94% ±4 | 95% | - | 8.6 | 27.0 | $0.0054 |
| baseline | 100% | 100% | 93% ±4 | 90% | - | 1.0 | 11.2 | $0.0021 |

## 유형: paraphrase

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 93% ±2 | 100% | - | 7.9 | 23.8 | $0.0041 |
| baseline | 100% | 100% | 93% ±4 | 100% | - | 1.0 | 10.9 | $0.0018 |

## 유형: vague

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 67% ±0 | 67% | - | 10.8 | 23.1 | $0.0034 |
| baseline | 100% | 100% | 67% ±0 | 67% | - | 1.0 | 7.2 | $0.0010 |

## 유형: multi_doc

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 80% | 70% | 53% ±0 | 40% | - | 8.2 | 32.5 | $0.0052 |
| baseline | 80% | 70% | 53% ±0 | 40% | - | 1.0 | 13.9 | $0.0018 |

## 유형: leak_probe

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 58% ±14 | 33% | - | 8.3 | 29.4 | $0.0048 |
| baseline | 100% | 100% | 75% ±25 | 67% | - | 1.0 | 8.3 | $0.0012 |

## 유형: negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 16.0 | 22.7 | $0.0036 |
| baseline | - | - | - | - | 100% | 1.0 | 6.5 | $0.0011 |

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 33% | 17.0 | 39.8 | $0.0048 |
| baseline | - | - | - | - | 83% | 1.0 | 7.2 | $0.0010 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 97% | 79% ±1 | 76% | 67% | 10.4 | 26.9 | $0.0041 |
| baseline | 100% | 97% | 79% ±2 | 76% | 92% | 1.0 | 9.8 | $0.0014 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 88% | 88% | 85% ±2 | 88% | 100% | 8.6 | 27.4 | $0.0057 |
| baseline | 88% | 88% | 86% ±2 | 88% | 100% | 1.0 | 11.6 | $0.0023 |

## 문항별 (공개분, 반복 평균)

| id | type | system | context recall | coverage | pass | rewrite |
|---|---|---|---|---|---|---|
| H01 | multi_doc | agentic | 100% | 67% | 3/3 | 0.0 |
| H01 | multi_doc | baseline | 100% | 67% | 3/3 | 0.0 |
| H02 | multi_doc | agentic | 100% | 100% | 3/3 | 0.0 |
| H02 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H03 | multi_doc | agentic | 50% | 50% | 0/3 | 0.0 |
| H03 | multi_doc | baseline | 50% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | agentic | 100% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | baseline | 100% | 50% | 0/3 | 0.0 |
| H05 | vague | agentic | 100% | 0% | 0/3 | 1.3 |
| H05 | vague | baseline | 100% | 0% | 0/3 | 0.0 |
| H06 | vague | agentic | 100% | 100% | 3/3 | 0.0 |
| H06 | vague | baseline | 100% | 100% | 3/3 | 0.0 |
| H07 | near_negative | agentic | - | 83% | 2/3 | 1.7 |
| H07 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| H08 | near_negative | agentic | - | 83% | 0/3 | 1.0 |
| H08 | near_negative | baseline | - | 100% | 2/3 | 0.0 |
| N01 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N01 | negative | baseline | - | 100% | 3/3 | 0.0 |
| N02 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N02 | negative | baseline | - | 100% | 3/3 | 0.0 |
| P01 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P01 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | agentic | 100% | 58% | 2/3 | 0.7 |
| P04 | keyword | baseline | 100% | 50% | 1/3 | 0.0 |
| P05 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P05 | paraphrase | baseline | 100% | 78% | 3/3 | 0.0 |
| P06 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P08 | paraphrase | agentic | 100% | 60% | 3/3 | 0.0 |
| P08 | paraphrase | baseline | 100% | 73% | 3/3 | 0.0 |
| P09 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P09 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P11 | leak_probe | agentic | 100% | 58% | 1/3 | 0.0 |
| P11 | leak_probe | baseline | 100% | 75% | 2/3 | 0.0 |

총 비용(추정): 시스템 $0.559 + judge $1.331 = $1.890
