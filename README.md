# troubleshooting-rag

개인 트러블슈팅 기록(마크다운)을 대상으로 한 **Self-RAG** 실험.
단순 RAG(baseline)와 Self-RAG(agentic)를 같은 골든셋으로 비교하고, 그 과정에서 발견한 **평가 누수**를 수치로 기록한다.

> 상태: 정리 중 (Day 1 — 구조 정리 / 프로바이더 전환 완료, 평가 미실행)

## 구조

```
src/
  config.py        경로 설정
  loader.py        data/ 하위 .md 로드
  splitter.py      recursive / markdown-header 청킹
  vectorstore.py   FAISS + bge-m3 로컬 임베딩
  indexing.py      인덱스 빌드 (cache/ 에 저장)
  retriever.py     top-k 검색
  baseline.py      단순 RAG (retrieve → generate)
  graders.py       retrieval / hallucination / answer grader, query rewriter
  nodes.py         LangGraph 노드 + 분기 로직
  graph.py         Self-RAG 그래프
  llm.py           Claude 호출 래퍼 (호출 수·토큰 집계)
  compare.py       baseline vs agentic 비교 실행
data/
  public/          공개 문서
  private/         로컬 전용 (gitignore) — 팀 프로젝트 내부 기록
```

## Self-RAG 흐름

```
retrieve → grade_documents ─┬─ (관련 문서 없음) → transform_query → retrieve
                            └─ generate → grade_generation ─┬─ hallucination → generate
                                                            ├─ not relevant  → transform_query
                                                            └─ relevant      → END
```

## 실행

```bash
cp .env.example .env          # ANTHROPIC_API_KEY 입력
uv sync
uv run python src/indexing.py # 최초 1회 (bge-m3 ~2GB 다운로드)
uv run python src/compare.py
```

- LLM: Claude Haiku 5.5 (생성 effort=medium, grader effort=low)
- 임베딩: `BAAI/bge-m3` (로컬, 키 불필요)
- `data/private/`는 레포에 없으므로, 클론 환경에서는 `data/public/` 기준으로 결과가 달라진다.

## 결과

_TODO (Day 2~4): 골든셋 기준 hit@4, 답변 통과율, 질문당 LLM 호출 수·지연시간 — 누수 제거 전/후, baseline/agentic_

## 알려진 문제 (수정 예정)

- [ ] query rewriter 프롬프트 예시에 평가 질문의 정답 키워드가 포함됨 (평가 누수)
- [ ] baseline과 agentic의 생성 프롬프트가 다름 (추측 허용 여부) → 비교 교란
- [ ] rewrite 2회 이후 hallucination 체크를 건너뜀
- [ ] 환각 시 동일 입력으로 재생성 (피드백 없음)
- [ ] answer grader / rewriter가 원 질문이 아닌 재작성된 질문을 사용
- [ ] 관련 문서 0개여도 빈 context로 생성
- [ ] 검색마다 FAISS 인덱스 재로드
