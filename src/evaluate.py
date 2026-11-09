"""골든셋 기반 baseline vs agentic 평가.

사용 예:
    uv run python src/evaluate.py --label day2-before
    uv run python src/evaluate.py --label smoke --reps 1 --ids P04,N01

지표 (system별):
    context_hit   : 생성에 실제로 들어간 문서에 expected_docs가 하나라도 있는가 (negative 제외)
    context_recall: expected_docs 중 생성에 들어간 문서의 비율 (multi_doc 문항에서 의미 있음)
                    - baseline: 검색 top-k / agentic: grader 필터 후 최종 문서
    coverage      : judge가 판정한 key_points 포함 비율 (0~1)
    pass          : coverage >= PASS_THRESHOLD
    abstain       : negative/near_negative 문항에서 "기록 없음"으로 답하고 지어내지 않았는가
    calls/tokens/cost/latency : 시스템 실행 비용 (judge 비용은 별도 집계)

출력:
    results/<label>.raw.json    전체 실행 기록 (답변 원문 포함, gitignore — 비공개 문서 내용이 들어갈 수 있음)
    results/<label>.summary.md  집계표 (비공개 문항은 개별 행 없이 합계만)
"""

import argparse
import json
import statistics
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

import llm
import nodes
from baseline import answer_question
from config import ROOT_DIR
from graph import run_agentic_rag
from vectorstore import get_embedding_model

EVAL_DIR = ROOT_DIR / "eval"
RESULTS_DIR = ROOT_DIR / "results"
GOLDEN_FILES = {
    "public": EVAL_DIR / "golden_public.yaml",
    "private": EVAL_DIR / "golden_private.yaml",
}

JUDGE_MODEL = "claude-sonnet-5-5"
JUDGE_EFFORT = "high"
PASS_THRESHOLD = 0.6
NEGATIVE_TYPES = {"negative", "near_negative"}
TYPE_ORDER = ["keyword", "paraphrase", "vague", "multi_doc", "leak_probe", "negative", "near_negative"]
STRATEGY = "markdown"
K = 4

# 병렬 실행 시 노드의 진행 로그가 뒤섞이므로 끈다.
nodes.print = lambda *args, **kwargs: None


# ---------------------------------------------------------------- judge

class PointVerdict(BaseModel):
    point: str = Field(description="채점 기준 문장 (입력 그대로)")
    covered: bool = Field(description="답변이 이 내용을 실질적으로 담고 있으면 true")


class JudgeVerdict(BaseModel):
    points: list[PointVerdict]
    abstained: bool = Field(description="답변이 '관련 기록이 없다/찾을 수 없다'는 취지로 답했으면 true")
    fabricated: bool = Field(description="질문에 대한 구체적 사례·원인·수치를 근거 없이 지어냈으면 true")


JUDGE_PROMPT = """너는 RAG 시스템 답변을 채점하는 평가자다.
질문, 채점 기준(key points), 시스템 답변이 주어진다.

규칙:
- 각 key point마다 답변이 그 내용을 실질적으로 담고 있는지 판정한다. 표현이 달라도 의미가 같으면 covered=true.
- 답변이 key point와 모순되거나, 막연하게만 언급하면 covered=false.
- 답변에 key point 외의 내용이 더 있어도 감점하지 않는다.
- abstained: 답변이 관련 기록을 찾지 못했다는 취지인지.
- fabricated: 기록에 없을 법한 구체적 사례·원인·수치를 사실처럼 단정했는지.
- points는 입력된 key point 순서 그대로, 같은 개수로 반환한다."""


def judge(question: str, key_points: list[str], answer: str) -> JudgeVerdict:
    numbered = "\n".join(f"{i}. {p}" for i, p in enumerate(key_points, start=1))
    user = f"질문:\n{question}\n\n채점 기준:\n{numbered}\n\n시스템 답변:\n{answer}"
    return llm.structured(
        JUDGE_PROMPT, user, JudgeVerdict, effort=JUDGE_EFFORT, tag="judge", model=JUDGE_MODEL
    )


# ---------------------------------------------------------------- run

def load_golden(sets: list[str]) -> list[dict]:
    items = []
    for name in sets:
        path = GOLDEN_FILES[name]
        if not path.exists():
            print(f"[skip] {path} 없음")
            continue
        for item in yaml.safe_load(path.read_text(encoding="utf-8")):
            item["set"] = name
            items.append(item)
    return items


def run_system(system: str, question: str) -> dict:
    if system == "baseline":
        result = answer_question(question=question, strategy=STRATEGY, k=K)
        return {"answer": result["answer"], "sources": result["sources"], "rewrite_count": 0, "rewritten_question": None}
    if system == "agentic":
        result = run_agentic_rag(question=question, strategy=STRATEGY)
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "rewrite_count": result["rewrite_count"],
            "rewritten_question": result["rewritten_question"],
        }
    raise ValueError(system)


def evaluate_one(item: dict, system: str, rep: int) -> dict:
    record = {
        "id": item["id"], "set": item["set"], "type": item["type"],
        "system": system, "rep": rep, "question": item["question"],
    }

    llm.reset_usage()
    start = time.perf_counter()
    try:
        out = run_system(system, item["question"])
    except Exception as e:  # 한 건 실패가 전체 실행을 멈추지 않게 기록만 한다
        record["error"] = f"system: {type(e).__name__}: {e}"
        return record
    record["latency_s"] = round(time.perf_counter() - start, 2)
    record["usage"] = llm.get_usage()
    record.update(out)

    filenames = {s["filename"] for s in out["sources"]}
    record["source_files"] = sorted(filenames)
    is_negative = item["type"] in NEGATIVE_TYPES
    expected = set(item["expected_docs"])
    record["context_hit"] = None if is_negative else bool(filenames & expected)
    record["context_recall"] = None if is_negative or not expected else len(filenames & expected) / len(expected)

    llm.reset_usage()
    try:
        verdict = judge(item["question"], item["key_points"], out["answer"])
    except Exception as e:
        record["error"] = f"judge: {type(e).__name__}: {e}"
        return record
    record["judge_usage"] = llm.get_usage()

    covered = [p.covered for p in verdict.points][: len(item["key_points"])]
    record["points_covered"] = covered
    record["coverage"] = sum(covered) / len(item["key_points"])
    record["abstained"] = verdict.abstained
    record["fabricated"] = verdict.fabricated
    if is_negative:
        record["pass"] = verdict.abstained and not verdict.fabricated
    else:
        record["pass"] = record["coverage"] >= PASS_THRESHOLD
    return record


# ---------------------------------------------------------------- summary

def _mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def _fmt(v, pct=False, digits=2):
    if v is None:
        return "-"
    return f"{v * 100:.0f}%" if pct else f"{v:.{digits}f}"


def summarize(records: list[dict], label: str, reps: int) -> str:
    ok = [r for r in records if "error" not in r]
    errors = [r for r in records if "error" in r]
    systems = sorted({r["system"] for r in records})

    lines = [f"# 평가 결과: {label}", ""]
    lines.append(f"- judge: {JUDGE_MODEL} (effort={JUDGE_EFFORT}), pass 기준: coverage >= {PASS_THRESHOLD}")
    lines.append(f"- 반복: {reps}회, 검색: {STRATEGY} 청킹 top-{K}, 시스템 LLM: {llm.MODEL_NAME}")
    lines.append(f"- 실행 {len(records)}건, 에러 {len(errors)}건")
    lines.append("")

    def block(title, subset):
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| system | context hit | context recall | coverage | pass | negative 정답 | 호출/질문 | 지연(s) | 비용/질문 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for system in systems:
            rs = [r for r in subset if r["system"] == system]
            pos = [r for r in rs if r["type"] not in NEGATIVE_TYPES]
            neg = [r for r in rs if r["type"] in NEGATIVE_TYPES]
            # 반복 간 편차: rep별 평균 coverage의 표준편차
            by_rep = defaultdict(list)
            for r in pos:
                by_rep[r["rep"]].append(r["coverage"])
            rep_means = [statistics.mean(v) for v in by_rep.values() if v]
            cov = _mean([r["coverage"] for r in pos])
            cov_txt = _fmt(cov, pct=True)
            if len(rep_means) > 1:
                cov_txt += f" ±{statistics.stdev(rep_means) * 100:.0f}"
            lines.append(
                f"| {system} "
                f"| {_fmt(_mean([float(r['context_hit']) for r in pos]), pct=True)} "
                f"| {_fmt(_mean([r.get('context_recall') for r in pos]), pct=True)} "
                f"| {cov_txt} "
                f"| {_fmt(_mean([float(r['pass']) for r in pos]), pct=True)} "
                f"| {_fmt(_mean([float(r['pass']) for r in neg]), pct=True)} "
                f"| {_fmt(_mean([r['usage']['calls'] for r in rs]), digits=1)} "
                f"| {_fmt(_mean([r['latency_s'] for r in rs]), digits=1)} "
                f"| ${_fmt(_mean([r['usage']['cost_usd'] for r in rs]), digits=4)} |"
            )
        lines.append("")

    block("전체", ok)
    for t in TYPE_ORDER:
        subset = [r for r in ok if r["type"] == t]
        if subset:
            block(f"유형: {t}", subset)
    for s in ["public", "private"]:
        subset = [r for r in ok if r["set"] == s]
        if subset:
            block(f"세트: {s}", subset)

    # 문항별 (공개분만)
    lines.append("## 문항별 (공개분, 반복 평균)")
    lines.append("")
    lines.append("| id | type | system | context recall | coverage | pass | rewrite |")
    lines.append("|---|---|---|---|---|---|---|")
    grouped = defaultdict(list)
    for r in ok:
        if r["set"] == "public":
            grouped[(r["id"], r["system"])].append(r)
    for (qid, system), rs in sorted(grouped.items()):
        recalls = [r.get("context_recall") for r in rs if r.get("context_recall") is not None]
        lines.append(
            f"| {qid} | {rs[0]['type']} | {system} "
            f"| {_fmt(_mean(recalls), pct=True) if recalls else '-'} "
            f"| {_fmt(_mean([r['coverage'] for r in rs]), pct=True)} "
            f"| {sum(r['pass'] for r in rs)}/{len(rs)} "
            f"| {_fmt(_mean([r['rewrite_count'] for r in rs]), digits=1)} |"
        )
    lines.append("")

    sys_cost = sum(r["usage"]["cost_usd"] for r in ok)
    judge_cost = sum(r.get("judge_usage", {}).get("cost_usd", 0) for r in ok)
    lines.append(f"총 비용(추정): 시스템 ${sys_cost:.3f} + judge ${judge_cost:.3f} = ${sys_cost + judge_cost:.3f}")
    if errors:
        lines.append("")
        lines.append("## 에러")
        for r in errors:
            lines.append(f"- {r['id']} / {r['system']} / rep{r['rep']}: {r['error'][:200]}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--systems", default="baseline,agentic")
    parser.add_argument("--sets", default="public,private")
    parser.add_argument("--ids", default="", help="쉼표로 구분한 문항 id만 실행")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--from-raw", default="", help="쉼표로 구분한 기존 raw 라벨들을 합쳐 재집계만 한다 (API 호출 없음)")
    args = parser.parse_args()

    if args.from_raw:
        golden = {it["id"]: it for it in load_golden(["public", "private"])}
        records = []
        for lbl in args.from_raw.split(","):
            records += json.loads((RESULTS_DIR / f"{lbl}.raw.json").read_text(encoding="utf-8"))
        for r in records:  # 이전 버전 raw에는 context_recall이 없을 수 있다
            if "context_recall" not in r and r.get("context_hit") is not None:
                expected = set(golden[r["id"]]["expected_docs"])
                r["context_recall"] = len(set(r["source_files"]) & expected) / len(expected)
        _save(records, args.label, max(r["rep"] for r in records))
        return

    items = load_golden(args.sets.split(","))
    if args.ids:
        wanted = set(args.ids.split(","))
        items = [it for it in items if it["id"] in wanted]
    systems = args.systems.split(",")

    get_embedding_model()  # 스레드 시작 전 1회 로드 (동시 로드 경합 방지)

    jobs = [(it, s, rep) for rep in range(1, args.reps + 1) for it in items for s in systems]
    print(f"{len(items)}문항 x {len(systems)}시스템 x {args.reps}회 = {len(jobs)}건 실행")

    records = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate_one, *job) for job in jobs]
        for i, fut in enumerate(as_completed(futures), start=1):
            r = fut.result()
            records.append(r)
            status = "ERR" if "error" in r else ("PASS" if r["pass"] else "fail")
            print(f"[{i}/{len(jobs)}] {r['id']} {r['system']} rep{r['rep']}: {status}", flush=True)

    _save(records, args.label, args.reps)


def _save(records: list[dict], label: str, reps: int) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    records.sort(key=lambda r: (r["id"], r["system"], r["rep"]))
    raw_path = RESULTS_DIR / f"{label}.raw.json"
    raw_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = summarize(records, label, reps)
    summary_path = RESULTS_DIR / f"{label}.summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(summary)
    print(f"saved: {raw_path}\n       {summary_path}")


if __name__ == "__main__":
    main()
