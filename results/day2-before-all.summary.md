# 평가 결과: day2-before-all

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 180건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 96% | 95% | 80% ±2 | 80% | 93% | 9.8 | 29.6 | $0.0049 |
| baseline | 96% | 94% | 85% ±2 | 84% | 93% | 1.0 | 9.8 | $0.0016 |

## 유형: keyword

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 94% ±4 | 95% | - | 8.2 | 25.2 | $0.0056 |
| baseline | 100% | 100% | 95% ±2 | 100% | - | 1.0 | 9.4 | $0.0019 |

## 유형: paraphrase

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 92% ±3 | 100% | - | 8.3 | 28.9 | $0.0049 |
| baseline | 100% | 100% | 98% ±0 | 100% | - | 1.0 | 10.2 | $0.0017 |

## 유형: vague

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 67% ±0 | 67% | - | 11.0 | 24.3 | $0.0032 |
| baseline | 100% | 100% | 74% ±6 | 67% | - | 1.0 | 7.4 | $0.0010 |

## 유형: multi_doc

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 80% | 73% | 51% ±4 | 40% | - | 9.0 | 43.4 | $0.0065 |
| baseline | 80% | 70% | 53% ±0 | 40% | - | 1.0 | 13.5 | $0.0018 |

## 유형: leak_probe

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 67% ±29 | 33% | - | 8.3 | 27.9 | $0.0044 |
| baseline | 100% | 100% | 83% ±14 | 100% | - | 1.0 | 8.2 | $0.0012 |

## 유형: negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 15.6 | 25.4 | $0.0035 |
| baseline | - | - | - | - | 100% | 1.0 | 7.7 | $0.0012 |

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 83% | 14.0 | 29.0 | $0.0037 |
| baseline | - | - | - | - | 83% | 1.0 | 7.3 | $0.0011 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 98% | 79% ±2 | 76% | 92% | 10.1 | 29.9 | $0.0046 |
| baseline | 100% | 97% | 83% ±3 | 82% | 92% | 1.0 | 9.3 | $0.0013 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 88% | 88% | 84% ±4 | 88% | 100% | 9.0 | 29.0 | $0.0058 |
| baseline | 88% | 88% | 88% ±0 | 88% | 100% | 1.0 | 10.8 | $0.0022 |

## 문항별 (공개분, 반복 평균)

| id | type | system | context recall | coverage | pass | rewrite |
|---|---|---|---|---|---|---|
| H01 | multi_doc | agentic | 100% | 67% | 3/3 | 0.0 |
| H01 | multi_doc | baseline | 100% | 67% | 3/3 | 0.0 |
| H02 | multi_doc | agentic | 100% | 89% | 3/3 | 0.0 |
| H02 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H03 | multi_doc | agentic | 67% | 50% | 0/3 | 0.3 |
| H03 | multi_doc | baseline | 50% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | agentic | 100% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | baseline | 100% | 50% | 0/3 | 0.0 |
| H05 | vague | agentic | 100% | 0% | 0/3 | 1.3 |
| H05 | vague | baseline | 100% | 22% | 0/3 | 0.0 |
| H06 | vague | agentic | 100% | 100% | 3/3 | 0.0 |
| H06 | vague | baseline | 100% | 100% | 3/3 | 0.0 |
| H07 | near_negative | agentic | - | 83% | 3/3 | 1.3 |
| H07 | near_negative | baseline | - | 83% | 2/3 | 0.0 |
| H08 | near_negative | agentic | - | 83% | 2/3 | 0.3 |
| H08 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| N01 | negative | agentic | - | 100% | 3/3 | 2.0 |
| N01 | negative | baseline | - | 100% | 3/3 | 0.0 |
| N02 | negative | agentic | - | 100% | 3/3 | 1.7 |
| N02 | negative | baseline | - | 100% | 3/3 | 0.0 |
| P01 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P01 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | agentic | 100% | 58% | 2/3 | 0.3 |
| P04 | keyword | baseline | 100% | 75% | 3/3 | 0.0 |
| P05 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P05 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | baseline | 100% | 92% | 3/3 | 0.0 |
| P08 | paraphrase | agentic | 100% | 60% | 3/3 | 0.0 |
| P08 | paraphrase | baseline | 100% | 80% | 3/3 | 0.0 |
| P09 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P09 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P11 | leak_probe | agentic | 100% | 67% | 1/3 | 0.0 |
| P11 | leak_probe | baseline | 100% | 83% | 3/3 | 0.0 |

총 비용(추정): 시스템 $0.587 + judge $1.355 = $1.942
