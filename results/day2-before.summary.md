# 평가 결과: day2-before

- judge: claude-sonnet-5-5 (effort=high), pass 기준: coverage >= 0.6
- 반복: 3회, 검색: markdown 청킹 top-4, 시스템 LLM: claude-haiku-5-5
- 실행 120건, 에러 0건

## 전체

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 91% ±4 | 94% | 100% | 9.4 | 27.0 | $0.0049 |
| baseline | 100% | 96% ±1 | 100% | 100% | 1.0 | 9.4 | $0.0017 |

## 유형: keyword

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 94% ±4 | 95% | - | 8.2 | 25.2 | $0.0056 |
| baseline | 100% | 95% ±2 | 100% | - | 1.0 | 9.4 | $0.0019 |

## 유형: paraphrase

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 92% ±3 | 100% | - | 8.3 | 28.9 | $0.0049 |
| baseline | 100% | 98% ±0 | 100% | - | 1.0 | 10.2 | $0.0017 |

## 유형: leak_probe

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 67% ±29 | 33% | - | 8.3 | 27.9 | $0.0044 |
| baseline | 100% | 83% ±14 | 100% | - | 1.0 | 8.2 | $0.0012 |

## 유형: negative

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | - | - | - | 100% | 15.6 | 25.4 | $0.0035 |
| baseline | - | - | - | 100% | 1.0 | 7.7 | $0.0012 |

## 세트: public

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 90% ±5 | 91% | 100% | 9.5 | 28.2 | $0.0047 |
| baseline | 100% | 94% ±2 | 100% | 100% | 1.0 | 9.2 | $0.0014 |

## 세트: private

| system | context hit | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |
|---|---|---|---|---|---|---|---|
| agentic | 100% | 95% ±5 | 100% | 100% | 9.1 | 25.0 | $0.0054 |
| baseline | 100% | 100% ±0 | 100% | 100% | 1.0 | 10.0 | $0.0023 |

## 문항별 (공개분, 반복 평균)

| id | type | system | context hit | coverage | pass | rewrite |
|---|---|---|---|---|---|---|
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

총 비용(추정): 시스템 $0.396 + judge $0.894 = $1.291
