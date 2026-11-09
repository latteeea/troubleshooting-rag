# 평가 결과: day3-step2-verify

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 180건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 96% | 94% | 75% ±2 | 76% | 100% | 9.3 | 32.6 | $0.0055 |
| baseline | 96% | 94% | 80% ±1 | 80% | 87% | 1.0 | 10.2 | $0.0017 |

## 유형: keyword

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 85% ±5 | 86% | - | 8.6 | 33.1 | $0.0068 |
| baseline | 100% | 100% | 92% ±4 | 90% | - | 1.0 | 11.5 | $0.0022 |

## 유형: paraphrase

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 87% ±2 | 100% | - | 8.5 | 30.8 | $0.0053 |
| baseline | 100% | 100% | 91% ±3 | 100% | - | 1.0 | 10.6 | $0.0017 |

## 유형: vague

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 67% ±0 | 67% | - | 10.1 | 31.4 | $0.0043 |
| baseline | 100% | 100% | 67% ±0 | 67% | - | 1.0 | 7.6 | $0.0010 |

## 유형: multi_doc

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 80% | 70% | 47% ±7 | 33% | - | 8.5 | 42.4 | $0.0066 |
| baseline | 80% | 70% | 53% ±0 | 40% | - | 1.0 | 13.5 | $0.0018 |

## 유형: leak_probe

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 100% | 58% ±14 | 33% | - | 10.0 | 49.3 | $0.0079 |
| baseline | 100% | 100% | 75% ±25 | 67% | - | 1.0 | 7.9 | $0.0012 |

## 유형: negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 14.3 | 24.3 | $0.0037 |
| baseline | - | - | - | - | 100% | 1.0 | 6.7 | $0.0011 |

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 100% | 8.7 | 20.7 | $0.0028 |
| baseline | - | - | - | - | 67% | 1.0 | 6.4 | $0.0010 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 97% | 71% ±3 | 71% | 100% | 9.3 | 31.2 | $0.0049 |
| baseline | 100% | 97% | 78% ±3 | 76% | 83% | 1.0 | 9.4 | $0.0013 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 88% | 88% | 83% ±0 | 88% | 100% | 9.3 | 35.9 | $0.0071 |
| baseline | 88% | 88% | 84% ±4 | 88% | 100% | 1.0 | 12.3 | $0.0024 |

## 문항별 (공개분, 반복 평균)

| id | type | system | context recall | coverage | pass | rewrite |
|---|---|---|---|---|---|---|
| H01 | multi_doc | agentic | 100% | 67% | 3/3 | 0.0 |
| H01 | multi_doc | baseline | 100% | 67% | 3/3 | 0.0 |
| H02 | multi_doc | agentic | 100% | 67% | 2/3 | 0.0 |
| H02 | multi_doc | baseline | 100% | 100% | 3/3 | 0.0 |
| H03 | multi_doc | agentic | 50% | 50% | 0/3 | 0.0 |
| H03 | multi_doc | baseline | 50% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | agentic | 100% | 50% | 0/3 | 0.0 |
| H04 | multi_doc | baseline | 100% | 50% | 0/3 | 0.0 |
| H05 | vague | agentic | 100% | 0% | 0/3 | 0.0 |
| H05 | vague | baseline | 100% | 0% | 0/3 | 0.0 |
| H06 | vague | agentic | 100% | 100% | 3/3 | 0.0 |
| H06 | vague | baseline | 100% | 100% | 3/3 | 0.0 |
| H07 | near_negative | agentic | - | 100% | 3/3 | 0.0 |
| H07 | near_negative | baseline | - | 100% | 3/3 | 0.0 |
| H08 | near_negative | agentic | - | 100% | 3/3 | 0.0 |
| H08 | near_negative | baseline | - | 67% | 1/3 | 0.0 |
| N01 | negative | agentic | - | 100% | 3/3 | 1.0 |
| N01 | negative | baseline | - | 100% | 3/3 | 0.0 |
| N02 | negative | agentic | - | 100% | 3/3 | 1.3 |
| N02 | negative | baseline | - | 100% | 3/3 | 0.0 |
| P01 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P01 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P02 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P03 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P04 | keyword | agentic | 100% | 8% | 0/3 | 0.0 |
| P04 | keyword | baseline | 100% | 42% | 1/3 | 0.0 |
| P05 | paraphrase | agentic | 100% | 67% | 3/3 | 0.0 |
| P05 | paraphrase | baseline | 100% | 67% | 3/3 | 0.0 |
| P06 | paraphrase | agentic | 100% | 100% | 3/3 | 0.0 |
| P06 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | agentic | 100% | 100% | 3/3 | 0.0 |
| P07 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P08 | paraphrase | agentic | 100% | 60% | 3/3 | 0.0 |
| P08 | paraphrase | baseline | 100% | 80% | 3/3 | 0.0 |
| P09 | keyword | agentic | 100% | 87% | 3/3 | 0.0 |
| P09 | keyword | baseline | 100% | 100% | 3/3 | 0.0 |
| P10 | paraphrase | agentic | 100% | 92% | 3/3 | 0.0 |
| P10 | paraphrase | baseline | 100% | 100% | 3/3 | 0.0 |
| P11 | leak_probe | agentic | 100% | 58% | 1/3 | 0.0 |
| P11 | leak_probe | baseline | 100% | 75% | 2/3 | 0.0 |

총 비용(추정): 시스템 $0.648 + judge $1.330 = $1.978
