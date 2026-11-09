# 평가 결과: day2-before-hard

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 60건, 에러 0건

## 전체

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 88% | 83% | 57% ±2 | 50% | 83% | 10.6 | 34.8 | $0.0049 |
| baseline | 88% | 81% | 61% ±2 | 50% | 83% | 1.0 | 10.4 | $0.0014 |

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

## 유형: near_negative

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | - | - | - | - | 83% | 14.0 | 29.0 | $0.0037 |
| baseline | - | - | - | - | 83% | 1.0 | 7.3 | $0.0011 |

## 세트: public

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 100% | 94% | 59% ±3 | 50% | 83% | 11.2 | 32.7 | $0.0044 |
| baseline | 100% | 92% | 65% ±3 | 50% | 83% | 1.0 | 9.6 | $0.0012 |

## 세트: private

| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|---|
| agentic | 50% | 50% | 50% ±0 | 50% | - | 8.3 | 43.0 | $0.0073 |
| baseline | 50% | 50% | 50% ±0 | 50% | - | 1.0 | 13.9 | $0.0020 |

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

총 비용(추정): 시스템 $0.190 + judge $0.461 = $0.651
