"""Independent, offline finite sanity checks for the path peer review.

These checks do not replace the proofs and do not use real model outputs.
No third-party packages or network calls are used.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, comb, log, sqrt
import json


def es_from_distribution(q, a):
    left, total = a, F(0)
    for value, mass in sorted(q.items(), reverse=True):
        used = min(left, mass)
        total += value * used
        left -= used
        if not left:
            return total / a
    raise AssertionError("Insufficient probability mass")


def r1_checks():
    cases = 0
    grid = (F(0), F(1, 100), F(1, 20), F(1, 5), F(1, 2), F(1))
    for sizes in ((1,), (2,), (1, 1), (1, 2), (2, 2), (1, 1, 1)):
        for u in product(grid, repeat=len(sizes)):
            knots = sorted(set((F(0), F(1)) + u))
            q = {}
            for lo, hi in zip(knots, knots[1:]):
                value = sum(b for b, ug in zip(sizes, u) if (lo + hi) / 2 <= ug)
                q[value] = q.get(value, F(0)) + hi - lo
            assert sum(q.values()) == 1
            for a in (F(1, 2), F(1, 5), F(1, 20)):
                target = sum(b * min(F(1), ug / a) for b, ug in zip(sizes, u))
                assert es_from_distribution(q, a) == target
                cases += 1
    return cases


def d1_checks():
    # Six documents, two fixed disjoint strata. Each document has fixed head influence.
    influences = ({0}, {0}, {1}, {1}, {2}, {0, 2})
    strata = (set(range(3)), set(range(3, 6)))
    checked = 0
    for mask in range(64):
        contamination = {i for i in range(6) if mask & (1 << i)}
        affected = set().union(*(influences[i] for i in contamination))
        assert affected <= {0, 1, 2}
        for n0, n1 in product(range(4), repeat=2):
            designs = list(product(combinations(range(3), n0), combinations(range(3, 6), n1)))
            misses = sum(not contamination.intersection(set(s0) | set(s1)) for s0, s1 in designs)
            observed = F(misses, len(designs))
            expected = F(1)
            for layer, n in zip(strata, (n0, n1)):
                available = 3 - len(contamination & layer)
                expected *= F(comb(available, n) if available >= n else 0, comb(3, n))
            assert observed == expected
            checked += 1
    return checked


def zero_audit_minimum(n_population, budget, alpha):
    for n in range(n_population + 1):
        good = n_population - budget - 1
        probability = F(comb(good, n) if good >= n else 0, comb(n_population, n))
        if probability <= alpha:
            return n
    raise AssertionError("No audit gate")


if __name__ == "__main__":
    result = {
        "purpose": "Finite mathematical sanity checks, not empirical research findings",
        "r1_comonotone_attainment_exact_cases": r1_checks(),
        "d1_stratified_miss_probability_exact_cases": d1_checks(),
        "p4_best_hoeffding_radius_C120_G1_alpha05": sqrt(log(20) / 240),
        "p4_min_equal_independent_clusters_for_radius_below_005": int(log(20) / (2 * .05**2)) + 1,
        "zero_failure_iid_one_sided_95pct_upper_n120": 1 - .05**(1 / 120),
        "zero_failure_iid_n_for_1pct_at_95pct": ceil(log(.05) / log(.99)),
        "zero_failure_iid_n_for_5pct_at_95pct": ceil(log(.05) / log(.95)),
        "N120_zero_discovery_audit_counts_alpha05": {
            str(b): zero_audit_minimum(120, b, F(1, 20)) for b in (0, 2, 5, 10)
        },
        "limitations": [
            "R1 check verifies attainability on a finite grid; the universal upper bound is reviewed analytically.",
            "D1 check enumerates sampling probabilities, not all possible audit or training mechanisms.",
            "R2 LP was not run for this review; equivalence was reviewed analytically.",
            "No original corpus, checkpoint, human annotation, or external paper was newly audited.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
