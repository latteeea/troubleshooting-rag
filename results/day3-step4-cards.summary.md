# 평가 결과: day3-step4-cards

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: card top-4, 시스템 LLM: claude-haiku-5-5
- 실행 180건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 96% | 94% | 90% ±1 | 89% | 100% | 9.1 | 28.9 | $0.0062 |
| baseline | 96% | 94% | 91% ±1 | 91% | 100% | 1.0 | 10.4 | $0.0022 |

## 유형: keyword

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 100% ±0 | 100% | - | 8.0 | 23.8 | $0.0047 |
| baseline | 100% | 100% | 100% ±0 | 100% | - | 1.0 | 10.1 | $0.0021 |

## 유형: paraphrase

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 96% ±0 | 100% | - | 8.6 | 28.1 | $0.0058 |
| baseline | 100% | 100% | 95% ±0 | 100% | - | 1.0 | 10.2 | $0.0022 |

## 유형: vague

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 67% | 67% | 67% ±0 | 67% | - | 8.1 | 23.9 | $0.0054 |
| baseline | 67% | 67% | 67% ±0 | 67% | - | 1.0 | 7.8 | $0.0019 |

## 유형: multi_doc

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 90% | 79% ±4 | 67% | - | 8.1 | 38.5 | $0.0082 |
| baseline | 100% | 90% | 81% ±4 | 73% | - | 1.0 | 14.6 | $0.0027 |

## 유형: leak_probe

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 83% ±14 | 100% | - | 10.0 | 101.0 | $0.0236 |
| baseline | 100% | 100% | 100% ±0 | 100% | - | 1.0 | 19.4 | $0.0040 |

## 유형: negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 14.0 | 16.0 | $0.0038 |
| baseline | - | - | - | - | 100% | 1.0 | 6.3 | $0.0015 |

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 11.2 | 17.4 | $0.0042 |
| baseline | - | - | - | - | 100% | 1.0 | 8.1 | $0.0018 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 94% | 91% | 88% ±1 | 90% | 100% | 9.4 | 31.4 | $0.0069 |
| baseline | 94% | 91% | 90% ±2 | 92% | 100% | 1.0 | 10.6 | $0.0023 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 94% ±0 | 88% | 100% | 8.4 | 23.1 | $0.0044 |
| baseline | 100% | 100% | 93% ±2 | 88% | 100% | 1.0 | 10.1 | $0.0019 |

## 문항별 (공개분, 반복 평균)

| id | type | system | context recall | coverage | pass | rewrite |
|---|---|---|---|---|---|---|
| H01 | multi_doc | agentic | 50% | 44% | 1/3 | 0.0 |
| H01 | multi_doc | baseline | 50% | 56% | 2/3 | 0.0 |
| H02 | multi_doc | agentic | 100% | 100% | 3/3 | 0.0 |
| H02 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H03 | multi_doc | agentic | 100% | 100% | 3/3 | 0.0 |
| H03 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H04 | multi_doc | agentic | 100% | 100% | 3/3 | 0.0 |
| H04 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H05 | vague | agentic | 0% | 0% | 0/3 | 0.0 |
| H05 | vague | baseline | 0% | 0% | 0/3 | 0.0 |
| H06 | vague | agentic | 100% | 100% | 3/3 | 0.0 |
| H06 | vague | baseline | 100% | 100% | 3/3 | 0.0 |
| H07 | near_negative | agentic | - | 100% | 3/3 | 0.0 |
| H07 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| H08 | near_negative | agentic | - | 50% | 3/3 | 2.0 |
| H08 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| N01 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N01 | negative | baseline | - | 100% | 3/3 | 0.0 |
| N02 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N02 | negative | baseline | - | 100% | 3/3 | 0.0 |
| P01 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P01 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | agentic | 100% | 100% | 3/3 | 0.3 |
| P03 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P05 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P05 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P08 | paraphrase | agentic | 100% | 60% | 3/3 | 0.0 |
| P08 | paraphrase | baseline | 100% | 67% | 3/3 | 0.0 |
| P09 | keyword | agentic | 100% | 100% | 3/3 | 0.3 |
| P09 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P11 | leak_probe | agentic | 100% | 83% | 3/3 | 0.0 |
| P11 | leak_probe | baseline | 100% | 100% | 3/3 | 0.0 |

총 비용(추정): 시스템 $0.754 + judge $1.349 = $2.103
