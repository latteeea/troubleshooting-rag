# 평가 결과: day3-step3-bugs

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 180건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 96% | 94% | 79% ±2 | 77% | 93% | 8.9 | 29.2 | $0.0048 |
| baseline | 96% | 94% | 80% ±3 | 79% | 100% | 1.0 | 10.1 | $0.0016 |

## 유형: keyword

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 92% ±4 | 90% | - | 7.7 | 26.2 | $0.0053 |
| baseline | 100% | 100% | 92% ±2 | 86% | - | 1.0 | 10.9 | $0.0021 |

## 유형: paraphrase

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 89% ±3 | 100% | - | 8.0 | 29.2 | $0.0049 |
| baseline | 100% | 100% | 92% ±6 | 100% | - | 1.0 | 10.7 | $0.0017 |

## 유형: vague

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 67% ±0 | 67% | - | 9.4 | 25.3 | $0.0033 |
| baseline | 100% | 100% | 67% ±0 | 67% | - | 1.0 | 7.2 | $0.0010 |

## 유형: multi_doc

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 80% | 70% | 53% ±0 | 40% | - | 8.3 | 40.0 | $0.0061 |
| baseline | 80% | 70% | 53% ±0 | 40% | - | 1.0 | 13.4 | $0.0018 |

## 유형: leak_probe

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 50% ±0 | 0% | - | 8.3 | 34.7 | $0.0055 |
| baseline | 100% | 100% | 75% ±25 | 67% | - | 1.0 | 8.6 | $0.0012 |

## 유형: negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 14.3 | 19.9 | $0.0026 |
| baseline | - | - | - | - | 100% | 1.0 | 6.5 | $0.0011 |

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 83% | 9.5 | 29.2 | $0.0042 |
| baseline | - | - | - | - | 100% | 1.0 | 7.0 | $0.0010 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 97% | 75% ±1 | 73% | 92% | 9.0 | 28.2 | $0.0042 |
| baseline | 100% | 97% | 79% ±3 | 75% | 100% | 1.0 | 9.4 | $0.0013 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 88% | 88% | 86% ±2 | 88% | 100% | 8.6 | 31.4 | $0.0062 |
| baseline | 88% | 88% | 84% ±4 | 88% | 100% | 1.0 | 11.8 | $0.0023 |

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
| H05 | vague | agentic | 100% | 0% | 0/3 | 0.3 |
| H05 | vague | baseline | 100% | 0% | 0/3 | 0.0 |
| H06 | vague | agentic | 100% | 100% | 3/3 | 0.0 |
| H06 | vague | baseline | 100% | 100% | 3/3 | 0.0 |
| H07 | near_negative | agentic | - | 100% | 3/3 | 0.0 |
| H07 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| H08 | near_negative | agentic | - | 100% | 2/3 | 0.3 |
| H08 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| N01 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N01 | negative | baseline | - | 100% | 3/3 | 0.0 |
| N02 | negative | agentic | - | 100% | 3/3 | 1.7 |
| N02 | negative | baseline | - | 100% | 3/3 | 0.0 |
| P01 | paraphrase | agentic | 100% | 87% | 3/3 | 0.0 |
| P01 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | agentic | 100% | 42% | 1/3 | 0.0 |
| P04 | keyword | baseline | 100% | 42% | 0/3 | 0.0 |
| P05 | paraphrase | agentic | 100% | 67% | 3/3 | 0.0 |
| P05 | paraphrase | baseline | 100% | 89% | 3/3 | 0.0 |
| P06 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P08 | paraphrase | agentic | 100% | 60% | 3/3 | 0.0 |
| P08 | paraphrase | baseline | 100% | 67% | 3/3 | 0.0 |
| P09 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P09 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P11 | leak_probe | agentic | 100% | 50% | 0/3 | 0.0 |
| P11 | leak_probe | baseline | 100% | 75% | 2/3 | 0.0 |

총 비용(추정): 시스템 $0.577 + judge $1.333 = $1.910
