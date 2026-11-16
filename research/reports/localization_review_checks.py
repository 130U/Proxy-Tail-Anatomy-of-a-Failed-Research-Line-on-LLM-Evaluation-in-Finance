"""Independent finite checks; exploratory reviewer artifact, stdlib only.

Does not import the author's risk or optimization functions. Run from any cwd.
Budgets were recorded in localization_review.md before first execution.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import hashlib
import json
import statistics
import sys
import time

START = time.perf_counter()
COUNTS = {"risk_comparisons": 0, "allocation_evaluations": 0,
          "conjunction_allocation_evaluations": 0, "prefix_flatten_checks": 0}


def budget():
    if time.perf_counter() - START > 60:
        raise RuntimeError("reviewer's 60-second budget exceeded")
    if COUNTS["risk_comparisons"] > 10_000:
        raise RuntimeError("risk-comparison budget exceeded")
    if COUNTS["allocation_evaluations"] > 100_000:
        raise RuntimeError("allocation budget exceeded")
    if COUNTS["conjunction_allocation_evaluations"] > 500_000:
        raise RuntimeError("conjunction allocation budget exceeded")


def miss(N, n, q):
    return Fraction(comb(N-q, n), comb(N, n)) if N-q >= n else Fraction(0)


def independent_greedy(Ns, ns, k):
    q = [0]*len(Ns)
    probability = Fraction(1)
    for unused in range(k):
        candidates = [(Fraction(max(N-n-j, 0), N-j), h)
                      for h, (N, n, j) in enumerate(zip(Ns, ns, q)) if j < N]
        ratio, h = max(candidates)
        probability *= ratio
        q[h] += 1
    return probability, tuple(q)


def enumerate_risks(Ns, ns, counter):
    maxima = [Fraction(-1)]*(sum(Ns)+1)
    for q in product(*(range(N+1) for N in Ns)):
        COUNTS[counter] += 1
        probability = Fraction(1)
        for N, n, count in zip(Ns, ns, q):
            probability *= miss(N, n, count)
        k = sum(q)
        maxima[k] = max(maxima[k], probability)
    budget()
    return maxima


def verify_greedy():
    cases = [(Ns, ns) for d in range(1, 4)
             for Ns in product(range(1, 4), repeat=d)
             for ns in product(*(range(N+1) for N in Ns))]
    cases += [((2,)*4, ns) for ns in product(range(3), repeat=4)]
    for Ns, ns in cases:
        exact = enumerate_risks(Ns, ns, "allocation_evaluations")
        for k, expected in enumerate(exact):
            got, allocation = independent_greedy(Ns, ns, k)
            assert got == expected, (Ns, ns, k, expected, got, allocation)
            COUNTS["risk_comparisons"] += 1
            if len(set(Ns)) == 1 and 1 <= k <= len(Ns):
                ordered = tuple(sorted(ns))
                flattened = ordered[:k] + (ordered[k-1],)*(len(Ns)-k)
                reduced, _ = independent_greedy(Ns, flattened, k)
                assert reduced == expected, (Ns, ns, k, flattened, expected, reduced)
                assert sum(flattened) <= sum(ns)
                COUNTS["prefix_flatten_checks"] += 1
        budget()
    return len(cases)


def verify_conjunction():
    alpha = Fraction(1, 20)
    rows = []
    for d in range(2, 9):
        Ns = (2,)*d
        best = None
        best_ns = None
        direct_best = None
        for ns in combinations_with_replacement(range(3), d):
            # One member from every stratum is the unique minimal bad count.
            direct_risk = Fraction(1)
            for n in ns:
                direct_risk *= Fraction(2-n, 2)
            if direct_risk <= alpha:
                direct_best = min(sum(ns), direct_best if direct_best is not None else sum(ns))
            exact = enumerate_risks(Ns, ns, "conjunction_allocation_evaluations")[d]
            if exact <= alpha and (best is None or sum(ns) < best):
                best, best_ns = sum(ns), ns
        k = 5  # min integer k with 2**(-k) <= 1/20
        closed_form = (d+k+1)//2 if d >= k else d+1
        assert best == closed_form, (d, best, closed_form)
        assert direct_best == 2, (d, direct_best)
        rows.append({"layers": d, "population_per_layer": 2,
                     "direct_cost": direct_best, "total_count_cost": best,
                     "total_count_samples": best_ns})
    return rows


def verify_final_table():
    """Independent final-artifact replay under a separately recorded budget."""
    root = Path(__file__).resolve().parents[2]
    data = json.loads((root/'research/planning/localization_results.json').read_text(encoding='utf-8'))
    assert data['status'] == 'complete' and len(data['cases']) == 48
    for relative, expected in data['source_sha256'].items():
        assert hashlib.sha256((root/relative).read_bytes()).hexdigest() == expected, relative
    proof = data['proof_note_at_start']
    assert hashlib.sha256((root/proof['path']).read_bytes()).hexdigest() == proof['sha256']
    old = json.loads((root/'research/planning/threshold_results.json').read_text(encoding='utf-8'))
    old_index = {(r['threshold'], r['layer_population']): r for r in old['rows']}
    alpha = Fraction(1, 20)
    prefix_count = risk_calls = 0
    threshold_savings = []
    family_counts = {}
    for row in data['cases']:
        family = row['family']
        family_counts[family] = family_counts.get(family, 0)+1
        N, d, k = row['N'], row['d'], row['k']
        if family == 'sharpness_bounds':
            assert row['status'] == 'bounds_only' and not row['globally_exact_costs_computed']
            r, m = row['r'], row['k_N']
            factor = Fraction(N-1, N)
            assert factor**m <= alpha < factor**(m-1)
            assert 1 <= m <= r and r == N*N and d == 2*r-1
            assert Fraction(row['total_over_direct_ratio_lower_exact']) == Fraction(2*N*N-N, r+m-1)
            assert Fraction(row['total_over_direct_ratio_upper_exact']) == Fraction(d, r)
            box_cost = r*((19*N+19)//20)
            assert box_cost > d  # Hence min(Box, optimal Total K) is optimal Total K.
            saving_lower = Fraction(2*N*N-N-(r+m-1), 2*N*N-N)
            expected_savings = {4: Fraction(1, 14), 8: Fraction(17, 60),
                                16: Fraction(97, 248), 32: Fraction(449, 1008)}
            assert saving_lower == expected_savings[N]
            continue
        assert row['status'] == 'optimal_comparison'
        total = row['total_count']
        reported = int(total['cost_exact'])
        assert sum(total['samples']) == reported
        got, _ = independent_greedy((N,)*d, total['samples'], k)
        assert got == Fraction(total['risk_exact']) and got <= alpha
        direct = int(row['direct']['cost_exact'])
        box = int(row['box']['cost_exact'])
        if family == 'threshold':
            reference = old_index[(k, N)]
            assert direct == reference['direct']['cost']
            assert box == reference['rectangle']['cost']
            direct_probability = Fraction(1)
            for n in sorted(row['direct']['samples'])[:k]:
                direct_probability *= Fraction(N-n, N)
            assert direct_probability == Fraction(row['direct']['risk_exact']) <= alpha
            assert box == (d-k+1)*((19*N+19)//20)
            box_probability = max((miss(N, n, b+1) for n, b in
                                   zip(row['box']['samples'], reference['rectangle']['count_upper_box'])
                                   if b < N), default=Fraction(0))
            assert box_probability == Fraction(row['box']['risk_exact']) <= alpha
            for prefix in combinations_with_replacement(range(N+1), k):
                prefix_count += 1
                if prefix_count > 500_000 or risk_calls > 100_000 or time.perf_counter()-START > 15:
                    raise RuntimeError('final-table reviewer budget exceeded; no partial optimum')
                cost = sum(prefix[:-1]) + (d-k+1)*prefix[-1]
                if cost >= reported:
                    continue
                risk_calls += 1
                candidate, _ = independent_greedy((N,)*k, prefix, k)
                assert candidate > alpha, ('found cheaper total-count allocation', row['case_id'], prefix, cost)
            if N == 2:
                expected = 2*d-k+1 if k < 5 else d-(k-5)//2
                assert reported == expected
        elif family == 'and':
            assert direct == box == 2
            assert reported == (d+1 if d < 5 else (d+6)//2)
        elif family == 'star':
            required = (19*N+19)//20
            assert direct == box == required
            expected = min(a+(d-1)*b for a in range(N+1) for b in range(a, N+1)
                           if max(miss(N, a, 2), Fraction((N-a)*(N-b), N*N)) <= alpha)
            assert reported == expected
        else:
            raise AssertionError(family)
        simple = min(box, reported)
        saving = Fraction(simple-direct, simple)
        assert simple == Fraction(row['strong_simple_cost_exact'])
        assert saving == Fraction(row['direct_saving_vs_strong_simple_exact'])
        if family == 'threshold':
            threshold_savings.append(saving)
        else:
            assert saving == 0
    assert family_counts == {'threshold': 20, 'and': 8, 'star': 16, 'sharpness_bounds': 4}
    assert sum(s > 0 for s in threshold_savings) == 5
    assert statistics.median(threshold_savings) == 0 and max(threshold_savings) == Fraction(1, 11)
    return {'status': 'independent_final_table_passed', 'case_counts': family_counts,
            'prefixes_enumerated': prefix_count, 'risk_calls_for_cheaper_designs': risk_calls,
            'source_and_proof_hashes_match': True, 'elapsed_seconds': time.perf_counter()-START}


def verify_pooled_scope():
    """One previously supplied out-of-class input, no optimization or search."""
    root = Path(__file__).resolve().parents[2]
    data = json.loads((root/'research/planning/pooled_scope_check.json').read_text(encoding='utf-8'))
    N, d, M, s, m = (data[k] for k in ('N_per_stratum', 'strata', 'total_documents',
                                      'excluded_total_count_minimum', 'audited_documents'))
    assert (N, d, M, s, m) == (32, 2047, 65504, 1024, 192)
    assert M == N*d and d == 2*s-1
    probability = Fraction(1)
    for j in range(m):
        probability *= Fraction(M-s-j, M-j)
        if time.perf_counter()-START > 2:
            raise RuntimeError('pooled single-input review budget exceeded')
    independent_binomial = Fraction(comb(M-s, m), comb(M, m))
    assert probability == independent_binomial == Fraction(data['zero_finding_risk_exact'])
    assert probability <= Fraction(1, 20)
    assert m < data['fixed_quota_direct_lower'] == s
    assert data['not_part_of_48_fixed_quota_rows'] and data['feasible_not_claimed_optimal']
    return {'status': 'independent_pooled_scope_check_passed', 'audits': m,
            'risk_decimal_for_display_only': float(probability), 'exact_risk_le_one_twentieth': True,
            'fixed_quota_direct_lower': s, 'not_part_of_48_rows': True,
            'elapsed_seconds': time.perf_counter()-START}


if __name__ == "__main__":
    if '--verify-pooled' in sys.argv:
        print(json.dumps(verify_pooled_scope(), indent=2))
        raise SystemExit(0)
    if '--verify-results' in sys.argv:
        print(json.dumps(verify_final_table(), indent=2))
        raise SystemExit(0)
    designs = verify_greedy()
    rows = verify_conjunction()
    print(json.dumps({"status": "independent_exploratory_checks_passed",
                      "risk_designs": designs, "counts": COUNTS,
                      "conjunction_rows": rows,
                      "elapsed_seconds": time.perf_counter()-START}, indent=2))
