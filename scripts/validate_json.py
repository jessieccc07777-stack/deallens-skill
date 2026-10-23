#!/usr/bin/env python
"""Validate a DealLens description JSON against the schema rules.

Usage: python validate_json.py <file.json>
Exits non-zero and prints every problem found; prints PASS when clean.
"""
import json
import sys

XS = {40, 310, 580, 840}
YS = {50, 210, 390, 530}


def fail(problems: list[str], msg: str) -> None:
    problems.append(msg)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    problems: list[str] = []
    try:
        j = json.load(open(sys.argv[1], encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        sys.exit(f"FATAL: not valid JSON: {e}")

    for key in ("company", "roundName", "round", "holders"):
        if key not in j:
            fail(problems, f"missing top-level key: {key}")
    if "round" in j:
        r = j["round"]
        if r.get("preMoney") is None or r.get("newMoney") is None:
            fail(problems, "round requires preMoney and newMoney")

    # holders
    holders = j.get("holders", [])
    if not holders:
        fail(problems, "holders is empty")
    total = 0.0
    ids = set()
    for i, h in enumerate(holders):
        hid = h.get("id") or f"#{i}"
        ids.add(hid)
        for lang in ("en", "zh"):
            if not h.get(lang):
                fail(problems, f"holder {hid}: missing {lang} name")
        if h.get("post") is not None:
            total += float(h["post"])
        elif h.get("money") is not None and "round" in j:
            total += float(h["money"]) / (j["round"]["preMoney"] + j["round"]["newMoney"]) * 100
        elif h.get("pre") is not None and "round" in j:
            keep = j["round"]["preMoney"] / (j["round"]["preMoney"] + j["round"]["newMoney"])
            total += float(h["pre"]) * keep
        else:
            fail(problems, f"holder {hid}: needs one of post / pre / money")
    if holders and abs(total - 100) > 0.05:
        fail(problems, f"ownership sums to {total:.3f}%, expected 100 (+/-0.05)")

    # clauses & edges
    clauses = j.get("clauses", [])
    edges = j.get("edges", [])
    cids = set()
    for c in clauses:
        cid = c.get("id")
        if not cid:
            fail(problems, "clause missing id"); continue
        if cid in cids:
            fail(problems, f"duplicate clause id: {cid}")
        cids.add(cid)
        for f in ("tag", "plain", "rh", "ob"):
            if f not in c or not isinstance(c[f], dict) or "en" not in c[f] or "zh" not in c[f]:
                fail(problems, f"clause {cid}: {f} must be {{en, zh}}")
        if c.get("x") not in XS or c.get("y") not in YS:
            fail(problems, f"clause {cid}: position ({c.get('x')},{c.get('y')}) off grid")
        for rel in c.get("related", []):
            pass  # checked after all ids known
    for c in clauses:
        for rel in c.get("related", []):
            if rel not in cids:
                fail(problems, f"clause {c['id']}: related -> unknown id {rel}")
    if clauses and not any(c.get("anchor") for c in clauses):
        fail(problems, "clauses: no anchor (cap table) node")
    for e in edges:
        for k in ("f", "t", "en", "zh"):
            if k not in e:
                fail(problems, f"edge missing {k}: {e}")
        if e.get("f") not in cids or e.get("t") not in cids:
            fail(problems, f"edge references unknown node: {e.get('f')} -> {e.get('t')}")

    # review overlay (optional, written back by dealreview)
    LEVELS = {"red", "major", "minor", "ok"}
    for c in clauses:
        rv = c.get("review")
        if rv is None:
            continue
        cid = c.get("id", "?")
        if rv.get("level") not in LEVELS:
            fail(problems, f"clause {cid}: review.level must be one of {sorted(LEVELS)}")
        for f in ("issue", "floor", "trade"):
            v = rv.get(f)
            if not isinstance(v, dict) or not v.get("en") or not v.get("zh"):
                fail(problems, f"clause {cid}: review.{f} must be {{en, zh}}")
    rm = j.get("reviewMeta")
    if rm is not None and not isinstance(rm, dict):
        fail(problems, "reviewMeta must be an object {tool, date, note{en,zh}}")

    # postReview overlay (optional, written back by dealreview after redlines)
    pr = j.get("postReview")
    if pr is not None:
        if not isinstance(pr, dict):
            fail(problems, "postReview must be an object {tool, date, basis{en,zh}, clauses{...}}")
        else:
            b = pr.get("basis")
            if not isinstance(b, dict) or not b.get("en") or not b.get("zh"):
                fail(problems, "postReview.basis must be {en, zh}")
            for cid, pc in (pr.get("clauses") or {}).items():
                if cid not in cids:
                    fail(problems, f"postReview.clauses: unknown clause id {cid}")
                if pc.get("level") is not None and pc.get("level") not in LEVELS:
                    fail(problems, f"postReview.clauses.{cid}: level must be one of {sorted(LEVELS)}")
                if pc.get("status") not in ("redlined", "pending"):
                    fail(problems, f"postReview.clauses.{cid}: status must be redlined or pending")
                ch = pc.get("change")
                if not isinstance(ch, dict) or not ch.get("en") or not ch.get("zh"):
                    fail(problems, f"postReview.clauses.{cid}: change must be {{en, zh}}")

    if problems:
        print("FAIL")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print(f"PASS: {len(holders)} holders, {len(clauses)} clauses, {len(edges)} edges, ownership = {total:.2f}%")


if __name__ == "__main__":
    main()
