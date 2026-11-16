"""Independent, bounded exact-arithmetic checks for paper_review.md.

Reads no data, imports no author implementation, trains no model, and writes no
files. This is exploratory mathematical review, not a confirmation experiment.
"""
from fractions import Fraction
from functools import reduce
from itertools import product
from math import comb
import json


def miss_probability(population, audited, contaminated):
    if population - contaminated < audited:
        return Fraction(0)
    return Fraction(comb(population - contaminated, audited),
                    comb(population, audited))


def total_count_risk(population, allocation, total_count, profiles):
    # Monotonicity reduces K >= total_count to K == total_count.
    return max(reduce(lambda a, b: a * b,
                      (miss_probability(population, n, q)
                       for n, q in zip(allocation, profile)), Fraction(1))
               for profile in profiles)


def main():
    balanced_checks = 0
    for population in (2, 3, 5):
        for threshold in (2, 3):
            layers = 2 * threshold - 1
            profiles = [q for q in product(
                range(min(population, threshold) + 1), repeat=layers)
                if sum(q) == threshold]
            for audited in range(population + 1):
                actual = total_count_risk(
                    population, [audited] * layers, threshold, profiles)
                expected = Fraction(population - audited, population) ** threshold
                assert actual == expected, (population, threshold, audited)
                balanced_checks += 1

    population, layers, threshold = 20, 3, 2
    alpha = Fraction(1, 20)
    profiles = [q for q in product(range(3), repeat=3) if sum(q) == 2]
    best_cost = 61
    minimizers = []
    visited = 0
    for allocation in product(range(21), repeat=3):
        visited += 1
        risk = total_count_risk(population, allocation, threshold, profiles)
        if risk > alpha:
            continue
        cost = sum(allocation)
        if cost < best_cost:
            best_cost, minimizers = cost, [allocation]
        elif cost == best_cost:
            minimizers.append(allocation)

    assert best_cost == 48 and minimizers == [(16, 16, 16)]
    print(json.dumps({
        'scope': 'independent exploratory arithmetic verification; not training',
        'balanced_designs_checked': balanced_checks,
        'fixed_allocations_visited': visited,
        'count_profiles_per_allocation': len(profiles),
        'total_K_le_1_optimum': best_cost,
        'minimizers': minimizers,
        'minimizer_worst_risk': str(total_count_risk(
            population, minimizers[0], threshold, profiles)),
        'within_one_layer_q2_n15': str(miss_probability(20, 15, 2)),
        'within_one_layer_q2_n16': str(miss_probability(20, 16, 2)),
        'r6_N20_balanced_total_count_risk': str(Fraction(3, 5) ** 6),
    }, indent=2))


if __name__ == '__main__':
    main()
