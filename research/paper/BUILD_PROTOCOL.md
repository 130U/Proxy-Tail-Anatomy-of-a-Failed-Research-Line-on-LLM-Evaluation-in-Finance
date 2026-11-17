# Round seven manuscript and readable version: pre-execution agreement

Date: 2026-11-16. Local preparation only: no network access, no software installation, no model training, nothing sent to Fable. This round is not a new confirmatory experiment; the numbers cited come from existing frozen protocols and results.

## Content and comparison targets

The main manuscript centres on the finite-population problem with fixed stratification, uniform sampling without replacement, and certification only when all findings are zero. It must include the full conditions and key proofs, the strongest joint zero-finding rectangle control, the results for all 20 cells, and two stronger comparison targets: a non-rectangular safe region and a simple total-contamination-count certificate. The simple alternatives found by the independent review must go into the full text; they cannot be put only in an appendix or a response letter.

PIT and P2 are discussed as boundaries of the certificate chain; the products of six rounds are not stitched together into a finished unified method. The real SEntFiN baseline is only used to describe the existing task and a simple-model reference; it cannot serve as verification of the audit theorem or of a historical certificate. G0/G1, novelty and real full-chain acceptance keep their existing status.

## Build budget

Use the bundled Python, Playwright, local browser and Poppler already on this machine; obtain no new dependencies. ReportLab was planned originally, but the available environment has no TeX/math-rendering dependency, so the build instead converts restricted TeX to native MathML and lets an offline browser typeset it, to avoid writing a home-made formula-coordinate typesetter. The budget for first-round PDF generation and page-by-page rendering is 120 seconds of CPU wall clock, no GPU compute requested, and expected resident memory below 1GB (an estimate; not reported as measured unless actually measured). Typesetting fixes may use extra builds, each recording whether the mathematical content changed; research experiments are not rerun because of typesetting.

The target is a complete, reviewable English internal technical report of about 8–14 pages; if the full proofs and all controls need more pages, the content is kept rather than squeezed into an unreadable font size. The author line uses "Prepared for Theodore and Fable - internal working draft"; no institution, author consent or submission status is invented.

## Files and verification

- `manuscript.md`: the main editable content source; the independent review checks it paragraph by paragraph.
- `manuscript.tex`: the corresponding editable LaTeX manuscript; there is no local TeX compiler, so it cannot be called compiled and verified.
- `build_pdf.py`: the local PDF build script; it must not silently drop unsupported mathematical expressions.
- `output/pdf/audit_budgets_working_report.pdf`: the readable version typeset with the local browser's native MathML; it is not called a TeX compilation product; the browser uses an isolated context with the network disabled and does not visit reference links.
- Intermediate PDF page images are saved in the workspace `tmp/pdfs/` and do not enter the research archive. Check each page's rendering, formulas, tables, page numbers, text extraction and source-file identity; a successful checker run cannot replace visual inspection.

The deliverable currently specified is this focused manuscript. The full set of theory notes in the original WP0.3 `theory/notes.tex` is not an equivalent copy of this manuscript, and this PDF must not be used to silently mark that item's original TeX-compilation acceptance as complete.
