"""Independent exact document-level audit randomization checks.

No project imports; no candidate formula is used as either minimax oracle.
Run from repository root:
  ..\\130U-FinLLM\\.venv\\Scripts\\python.exe research\\reports\\randomization_review_checks.py
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product, permutations
from math import comb
import argparse
import json
from pathlib import Path
from time import perf_counter

MAX_DOCUMENTS = 10
MAX_PAYOFFS = 20_000_000
MAX_SECONDS = 120
START = perf_counter()
COUNTS = {"payoff_intersections": 0, "auditsets": 0,
          "minimal_bad_sets": 0, "strategy_support_actions": 0}


def cap(amount):
    COUNTS["payoff_intersections"] += amount
    if COUNTS["payoff_intersections"] > MAX_PAYOFFS:
        raise RuntimeError("INCOMPLETE: payoff cap exceeded")
    if perf_counter() - START > MAX_SECONDS:
        raise RuntimeError("INCOMPLETE: time cap exceeded")


def mask_of(items):
    result = 0
    for item in items:
        result |= 1 << item
    return result


def bad_sets(d, n, r):
    return [
        mask_of(layer * n + offset for layer, offset in zip(layers, offsets))
        for layers in combinations(range(d), r)
        for offsets in product(range(n), repeat=r)
    ]


def action_sets(total):
    by_size = [[] for _ in range(total + 1)]
    for action in range(1 << total):
        by_size[action.bit_count()].append(action)
    return by_size


def whole_layer_support(d, n, budget):
    q, t = divmod(budget, n)
    support = []
    for full in combinations(range(d), q):
        fixed = mask_of(layer * n + j for layer in full for j in range(n))
        if t == 0:
            support.append(fixed)
        else:
            for layer in range(d):
                if layer not in full:
                    for partial in combinations(range(n), t):
                        support.append(fixed | mask_of(layer * n + j for j in partial))
    assert support and len(set(support)) == len(support)
    assert all(action.bit_count() == budget for action in support)
    return support


def direct_risks(support, bads):
    # Explicit uniform distribution over labelled document sets.
    cap(len(support) * len(bads))
    return [
        Fraction(sum((action & bad) == 0 for action in support), len(support))
        for bad in bads
    ]


def candidate_formula(d, n, r, m):
    # THIRD DIAGNOSTIC ONLY. Neither independent oracle calls this.
    if m == d * n:
        return Fraction(0)
    q, t = divmod(m, n)

    def choose(a, b):
        return comb(a, b) if 0 <= b <= a else 0

    return (
        Fraction(choose(d - q - 1, r))
        + (1 - Fraction(t, n)) * choose(d - q - 1, r - 1)
    ) / choose(d, r)


def sequential_layer_risk(d, n, r, m):
    """Direct conditional avoidance probabilities; not candidate_formula."""
    q, t = divmod(m, n)
    if q > d - r:
        return Fraction(0)
    survive_full = Fraction(1)
    for j in range(q):
        survive_full *= Fraction(d - r - j, d - j)
    # After avoiding r occupied strata, exactly r of the d-q remaining
    # strata are occupied. Partial sampling hits its unique bad doc with t/n.
    return survive_full * (1 - Fraction(r * t, n * (d - q)))


def pooled_binomial_risk(d, n, r, m):
    total = d * n
    if m > total - r:
        return Fraction(0)
    return Fraction(comb(total - r, m), comb(total, m))


def verify_results(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "complete"
    assert data["sources_unchanged_during_run"] is True
    alpha = Fraction(data["alpha_exact"])
    assert alpha == Fraction(1, 20)
    expected = {f"threshold-r{r}-N{n}" for r in (2, 3, 4, 5, 6)
                for n in (2, 5, 10, 20)}
    expected |= {f"and-d{d}-N2" for d in (2, 3, 4, 5, 6, 8, 12, 20)}
    expected |= {f"sharpness-N{n}" for n in (4, 8, 16, 32)}
    assert len(data["cases"]) == 32
    assert {row["case_id"] for row in data["cases"]} == expected
    risk_evaluations = 0
    summaries = {}
    compact_rows = []
    for row in data["cases"]:
        assert row["status"] == "complete"
        d, n, r = row["d"], row["N"], row["k"]
        assert all(type(x) is int for x in (d, n, r))
        assert 1 <= r <= d and n >= 1
        for key, evaluate in (("randomized_optimal", sequential_layer_risk),
                              ("pooled_srs_optimal", pooled_binomial_risk)):
            result = row[key]
            m = result["audits"]
            assert type(m) is int and 1 <= m <= d * n
            actual = evaluate(d, n, r, m)
            previous = evaluate(d, n, r, m - 1)
            risk_evaluations += 2
            assert actual == Fraction(result["risk_exact"]), (row["case_id"], key)
            assert previous == Fraction(result["previous_audits_risk_exact"])
            assert actual <= alpha < previous, (row["case_id"], key, "minimality")
        m = row["randomized_optimal"]["audits"]
        pooled = row["pooled_srs_optimal"]["audits"]
        assert m <= pooled
        q, t = divmod(m, n)
        construction = row["randomized_optimal"]["construction"]
        assert construction["full_strata"] == q
        assert construction["partial_documents"] == t
        saving = Fraction(pooled - m, pooled)
        assert Fraction(row["saving_vs_pooled_exact"]) == saving
        lo, hi = row["fixed_direct_cost_bounds"]
        assert [Fraction(x) for x in row["saving_vs_fixed_direct_bounds_exact"]] == [
            Fraction(lo - m, lo), Fraction(hi - m, hi)]
        assert row["fixed_costs_exact"] is (row["family"] != "sharpness_bounds")
        compact_rows.append([row["case_id"], m, pooled, str(saving)])
        if perf_counter() - START > MAX_SECONDS:
            raise RuntimeError("INCOMPLETE: time cap exceeded during result verification")
    for family in ("threshold", "and", "sharpness_bounds"):
        subset = [row for row in data["cases"] if row["family"] == family]
        savings = sorted(Fraction(row["saving_vs_pooled_exact"]) for row in subset)
        middle = len(savings) // 2
        median = (savings[middle - 1] + savings[middle]) / 2
        actual = {
            "cases": len(subset),
            "strict_gain_vs_pooled": sum(value > 0 for value in savings),
            "median_saving_vs_pooled_exact": str(median),
            "strict_gain_vs_fixed_direct_lower": sum(
                row["randomized_optimal"]["audits"] < row["fixed_direct_cost_bounds"][0]
                for row in subset),
        }
        assert data["summaries"][family] == actual
        summaries[family] = actual
    assert risk_evaluations == 128
    return {
        "status": "PASS", "rows": 32, "exact_risk_evaluations": risk_evaluations,
        "results_sha256": sha256(path.read_bytes()).hexdigest(),
        "summaries": summaries, "audit_counts": compact_rows,
        "scope_limit": "round-8 cost bounds inherited; not independently reoptimized here",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-results", type=Path)
    args = parser.parse_args()
    rows = []
    parameter_pairs = []
    examples = {}
    expected_rows = 0
    for d in range(1, MAX_DOCUMENTS + 1):
        for n in range(1, MAX_DOCUMENTS // d + 1):
            parameter_pairs.append([d, n])
            actions = action_sets(d * n)
            COUNTS["auditsets"] += 1 << (d * n)
            for r in range(1, d + 1):
                bads = bad_sets(d, n, r)
                assert len(set(bads)) == len(bads)
                COUNTS["minimal_bad_sets"] += len(bads)
                bounds = []
                for m, choices in enumerate(actions):
                    # Oracle 1: all labelled audit sets against uniform minimal
                    # bad-set prior, minimized by direct integer counting.
                    cap(len(choices) * len(bads))
                    miss_counts = [
                        sum((action & bad) == 0 for bad in bads)
                        for action in choices
                    ]
                    lower = Fraction(min(miss_counts), len(bads))
                    # Oracle 2: direct worst payoff of the explicit support.
                    support = whole_layer_support(d, n, m)
                    COUNTS["strategy_support_actions"] += len(support)
                    risks = direct_risks(support, bads)
                    worst = max(risks)
                    assert min(risks) == worst, (d, n, r, m, "not equalized")
                    assert lower == worst, (d, n, r, m, lower, worst)
                    predicted = candidate_formula(d, n, r, m)
                    assert predicted == lower, (d, n, r, m, predicted, lower)
                    rows.append([d, n, r, m, str(lower), len(choices),
                                 len(bads), len(support)])
                    bounds.append(lower)
                # Derived only from the independently enumerated payoff table.
                slopes = [b - a for a, b in zip(bounds, bounds[1:])]
                assert all(a <= b for a, b in zip(slopes, slopes[1:]))
                assert all(slope <= 0 for slope in slopes)
                expected_rows += 1
                if (d, n, r) in {(1, 2, 1), (3, 2, 2), (5, 2, 3)}:
                    examples[f"d={d},N={n},r={r}"] = [str(x) for x in bounds]

    # Explicit expected-budget mixture, with no closed-form oracle.
    bads = bad_sets(3, 2, 2)
    risks2 = direct_risks(whole_layer_support(3, 2, 2), bads)
    risks3 = direct_risks(whole_layer_support(3, 2, 3), bads)
    mixture_risks = [(a + b) / 2 for a, b in zip(risks2, risks3)]
    assert max(mixture_risks) == min(mixture_risks) == Fraction(1, 4)

    # Counterexample to expected budget imposed only on bad worlds.
    orders = list(permutations(range(2)))
    bad_only_costs = {}
    for bad in (1, 2, 3):
        costs = []
        failures = 0
        for order in orders:
            hit = False
            cost = 0
            for doc in order:
                cost += 1
                if bad & (1 << doc):
                    hit = True
                    break
            costs.append(cost)
            failures += not hit
        assert failures == 0
        bad_only_costs[str(bad)] = str(Fraction(sum(costs), len(costs)))
    assert max(Fraction(v) for v in bad_only_costs.values()) == Fraction(3, 2)

    payload = {
        "status": "PASS",
        "scope": "all d,N>=1 with d*N<=10; all 1<=r<=d; all 0<=m<=d*N",
        "parameter_pairs": parameter_pairs,
        "pair_count": len(parameter_pairs),
        "risk_budget_cases": len(rows),
        "convexity_tables_checked": expected_rows,
        "counts": COUNTS,
        "examples": examples,
        "expected_mixture": {"d": 3, "N": 2, "r": 2, "mean_budget": "5/2",
                             "min_risk": str(min(mixture_risks)),
                             "max_risk": str(max(mixture_risks))},
        "bad_only_budget_counterexample": {
            "d": 1, "N": 2, "r": 1, "bad_mask_expected_costs": bad_only_costs,
            "clean_cost": 2, "all_bad_world_risks": 0,
            "fixed_clean_budget_value_at_3/2": "1/4"},
        "case_rows_sha256": sha256(
            json.dumps(rows, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(perf_counter() - START, 6),
        "limits": {"max_payoffs": MAX_PAYOFFS, "max_seconds": MAX_SECONDS},
        "limitations": [
            "finite checks support but do not replace the general proof",
            "no adaptive policy trees are enumerated",
            "no empirical model or real audit labels were tested",
            "no external novelty or literature review was performed",
        ],
    }
    if args.verify_results is not None:
        payload["author_table_verification"] = verify_results(args.verify_results)
        payload["elapsed_seconds"] = round(perf_counter() - START, 6)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
