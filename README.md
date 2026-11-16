# Proxy Tail

**What does a cheap model miss in the tail?**

Language models are often used as screens: a cheap model reads everything and passes its top 1% to an expensive model or a person. This project asks how much of the true top survives as the screen gets more selective, and how wide the cheap model's net must be to keep it.

## The question

Let `A` be the expensive model's score and `B` the cheap model's score for the same item. For a target share `p` of items:

- **Overlap.** What fraction of the top `p` by `A` is also in the top `p` by `B`?
- **Widening.** What share `p1 ≥ p` must the cheap model pass so that a fixed fraction (say 90%) of the top `p` by `A` gets through?

Correlation, accuracy and AUC describe the middle of the joint distribution. They do not answer either question, because both depend on whether extreme scores occur together.

## The conjecture

Put both scores on a common (Laplace) scale and suppose that when `A` is large, `B ≈ αA` plus smaller fluctuations. Then the cheap model's net must be about

```
p1 ≈ p^α
```

- `α = 1`: the widening factor `p1 / p` is a constant, and the cheap model is reliable in the tail.
- `α < 1`: the widening factor grows without bound as the screen tightens.
- Under Gaussian dependence with correlation `ρ`, `α = ρ²`.

The statement is unproved here. The tools behind it are standard: selection tables for the Gaussian case, tail dependence coefficients, and conditional extremes models.

## Status

Nothing in this repository is established yet.

A first look, on two simple lexical classifiers standing in for the cheap and expensive models (score correlation 0.92, 14,284 financial headlines), showed:

| Top share by the reference model | Widening needed, most positive end | Most negative end | Gaussian benchmark |
|---|---:|---:|---:|
| 10% | 1.8× | 1.3× | 1.6× |
| 5% | 2.7× | 1.8× | 2.0× |
| 2% | 4.6× | 2.5× | 2.5× |
| 1% | 6.3× | 3.5× | 3.0× |

Both models are lexical, the "reference" is itself a model, and the sample includes training data. This shows only that the effect exists and is cheap to measure. Whether it holds between tiers of large language models is the open question.

## Plan

1. Check prior work: retrieve-then-rerank theory, selection under non-Gaussian dependence, extreme value methods applied to model scores, proxy-based filtering in databases.
2. Derive the Gaussian case in full, then state the general result with its assumptions.
3. Score a public corpus of at least 100,000 financial headlines with two model tiers, using scores that can be strictly ranked.
4. Plot the widening factor against the selected share for both tails, against the Gaussian benchmark, with an estimate of `α`.

The project stops if the same law and measurement already exist, if model tiers turn out to match the Gaussian benchmark in both tails, or if strictly ranked scores cannot be obtained.

No model is trained in this project.
