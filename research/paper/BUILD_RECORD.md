# Build and reading-version acceptance of the focused technical report

Date: 2026-11-16. The final deliverable is a 10-page A4 English [reading PDF](output/pdf/audit_budgets_working_report.pdf), with about 4,636 words of body text, 19 display formulas, 157 inline formulas and 3 tables. The editable [Markdown](manuscript.md) and [LaTeX](manuscript.tex) are attached separately. This PDF was typeset by local Chromium with native MathML and **is not a TeX compilation result**; the specified compilation acceptance of the original full theory notes.tex has not been completed by this.

## Content and identity checks

The [independent paper review](../reports/paper_review.md) responds to PR01–PR06 item by item and compared all 176 mathematical expressions in the two source manuscripts; in the end they agree exactly in order, ignoring only whitespace. The Direct, Box and Balanced costs and the exact savings for all 20 cells also agree with the existing results JSON. A problem where the definition of D was wrongly escaped was found and fixed; the integer convention for the box budget has been written down. The review supports positioning this as an internal technical report and keeps the scientific gaps in originality, practical use and G0/G1.

| File | Final SHA256 |
|---|---|
| manuscript.md | a9cd81ab194e54bb583dab69cbc7f3440745468b2f701ee6146e66c02d844ce0 |
| manuscript.tex | f4b423e730e235c38d816d4f50ea61fa2a6cb6b16d0aac94b906e29f144c02f2 |
| build_pdf.py | 52de49e5d830fbb0be69d24c28229d4bb3cdb1c751dfd3688fbdf25b895db8cb |
| Final PDF | dabaf18262c037aabd8d3c2a67047bfc16f0047ad1b0f6e34789efd782b3f1f8 |

Machine-readable build information is in [BUILD_RESULT.json](BUILD_RESULT.json). The PDF may contain metadata such as the generation time, so a rebuild is not promised to be byte-identical; the content-source hashes are used to check the version reviewed this time.

## Local build and visual inspection

Run according to the [pre-execution agreement](BUILD_PROTOCOL.md). The marker required by the PDF skill was run successfully once before the first generation; after that only the typesetting was fixed and rebuilt, and the marker was not repeated. The existing Python, Playwright, Chrome 157.0.8103.78 and Poppler were used, and no dependencies were installed. An isolated temporary browser profile, an offline context, request interception and a CSP forbidding external resources were all enabled; the request count recorded by this build was 0.

The first internal build took 1.7981 seconds and produced 10 pages. Looking through the Poppler images page by page revealed that ordinary parentheses should not stretch with the whole expression, that leading and trailing spaces in math text were lost, and that some punctuation was orphaned. Only the builder was modified: ordinary delimiters are not stretched automatically, explicitly paired delimiters stretch locally, text whitespace is kept, adjacent punctuation is bound, and lead-in sentences are kept together with their formulas; the hashes of the manuscript body and math source did not change.

The final internal build took 1.4061 seconds; the outer command took about 3.39 seconds of wall clock, and Poppler rendering about 1.85 seconds. No GPU training; peak memory not measured. The run detected 176 math nodes, native fractions were available, and the lists of formulas and tables overflowing horizontally were empty. pypdf confirmed 10 pages and extracted 33,006 characters; text extraction does not replace a layout check.

The main agent looked at 100dpi renderings of all 10 final pages: no clipping, overlap, missing glyph boxes, broken table rows or missing pages were observed. The accuracy formula, the hypergeometric ratio, the definition of D, the rectangle max risk, the order separation, the threshold optimization, the semantic formulas and the complete 20-cell table were checked in particular. Table headers repeat across pages and all 20 rows are kept; page numbers run continuously from 1/10 to 10/10. The current PDF uses native MathML font styles and does not claim pixel-for-pixel agreement with TeX glyph typesetting.

## Reproduction

From the repository root, in an existing Python environment:

```powershell
python research/paper/build_pdf.py --check
python research/paper/build_pdf.py --render
```

`--check` only parses in memory; `--render` needs Chrome or Edge, Node, Playwright and pypdf already present on the machine. By default it points to the bundled runtime used this time; on another machine you can pass `--node`, `--playwright`, `--browser`; nothing is downloaded automatically. Unknown math commands, unavailable native MathML or overflowing formulas cause an explicit failure. Temporary HTML, the profile and the rendered page images do not enter the research archive.

This round only added typesetting, a content review and an independent exact mathematical check; no existing model experiment was rerun. The 1 existing test for the private-data boundary of packaging passed again; the 106 integration unit tests of round six still belong to the earlier run record and are not passed off as 106 tests newly run in this round.
