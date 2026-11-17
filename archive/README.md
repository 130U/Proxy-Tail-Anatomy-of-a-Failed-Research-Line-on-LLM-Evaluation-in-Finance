# Archive

Historical documents kept for the record. They describe what the project believed at the time and
are not current conclusions; the final account is the [report](../report/proxy_tail_postmortem.pdf)
and the [front page](../README.md).

| File | What it is |
|---|---|
| [README-before-closeout.md](README-before-closeout.md) | The project's front page on the morning of 2026-11-17, after T1g: the exploration map with its colour rules (🟢 publishable, 🟡 candidate, ⚪ closed or not distinctive, 🔴 not done) |
| [README-2026-11-16-tail-screening.md](README-2026-11-16-tail-screening.md) | The front page on 2026-11-16, when the project was about tail screening |
| [tasks-before-closeout.md](tasks-before-closeout.md) | The task index before closeout |
| [finqa_short_paper_draft_v0.md](finqa_short_paper_draft_v0.md) | The abandoned short-paper draft ("FinQA at Its Ceiling"). Its framing and several expected counts did not survive T1f and T1g |
| [commits-before.txt](commits-before.txt), [refs-before.json](refs-before.json) | Commit log and branch tips just before closeout |

Links inside the historical pages were adjusted to point at the current locations of the files.

## Branches and history

During the project each task ran on its own branch (`task/t1`, `task/t1a`, …). At closeout every
branch was merged into `main` without rewriting history, and the branches were then deleted from
GitHub. [refs-before.json](refs-before.json) lists the tip commit of each branch; any old file can be
read with

```sh
git show <commit>:<path>
```

T1d and T1g were first committed in local working copies and imported at closeout; the T1g import
includes commit `0c68d8a`, which holds the TAT-QA prediction made before any TAT-QA measurement.

## The closeout tag

The tag [`closeout-2026-11-17`](https://github.com/130U/proxy-tail/tree/closeout-2026-11-17) points at
the state of the repository at closeout, before the English release. It still contains the
documents in their original Chinese, the delivery ZIP packages, the concatenated review bundle, the
reading-copy PDFs, and older README variants from each branch.
