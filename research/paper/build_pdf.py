"""Offline Markdown -> restricted TeX/MathML -> Chromium PDF working-paper builder.

This is NOT a TeX compiler. Unknown mathematical commands fail closed. The caller
must complete the PDF skill authoring marker before using --render. --check only
parses the entire source in memory; it neither starts a browser nor writes a PDF.
Only local, already-installed Chromium and Playwright are used. No installations,
network requests, private research data, or model training are involved.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


PAPER_DIR = Path(__file__).resolve().parent
REPO_DIR = PAPER_DIR.parent.parent
RUNTIME = Path(
    r"C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1112-611-0_26.1112.611.0_x64__3k8sg7r9htsxt\dependencies"
)
DEFAULT_OUTPUT = PAPER_DIR / "output/pdf/audit_budgets_working_report.pdf"
DEFAULT_TEMP = REPO_DIR.parent / "tmp/pdfs"


class BuildError(ValueError):
    """The source or local rendering environment cannot be faithfully handled."""


def tag(name: str, body: str = "", **attrs: str) -> str:
    attributes = "".join(f' {k}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f"<{name}{attributes}>{body}</{name}>"


@dataclass(frozen=True)
class Atom:
    markup: str
    limits: bool = False


GREEK = dict(zip(
    ("alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa "
     "lambda mu nu xi omicron pi varpi rho varrho sigma varsigma tau upsilon phi "
     "varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega").split(),
    "αβγδεϵζηθϑικλμνξοπϖρϱσςτυϕφχψωΓΔΘΛΞΠΣΥΦΨΩ",
))
SYMBOLS = {
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠",
    "in": "∈", "notin": "∉", "subseteq": "⊆", "supseteq": "⊇", "subset": "⊂",
    "supset": "⊃", "cup": "∪", "cap": "∩", "times": "×", "cdot": "⋅",
    "circ": "∘", "pm": "±", "mp": "∓", "to": "→", "rightarrow": "→",
    "leftarrow": "←", "Rightarrow": "⇒", "Longrightarrow": "⟹",
    "Leftrightarrow": "⇔", "Longleftrightarrow": "⟺", "forall": "∀",
    "exists": "∃", "infty": "∞", "emptyset": "∅", "varnothing": "∅",
    "ell": "ℓ", "star": "⋆", "partial": "∂", "nabla": "∇", "approx": "≈",
    "equiv": "≡", "propto": "∝", "ldots": "…", "cdots": "⋯", "vdots": "⋮",
    "mid": "∣", "parallel": "∥", "land": "∧", "lor": "∨", "neg": "¬",
    "lceil": "⌈", "rceil": "⌉", "lfloor": "⌊", "rfloor": "⌋",
    "langle": "⟨", "rangle": "⟩", "vert": "|", "Vert": "‖",
}
BIG_OPERATORS = {"sum": "∑", "prod": "∏", "bigcup": "⋃", "bigcap": "⋂", "bigsqcup": "⨆"}
NAMED_OPERATORS = {"min", "max", "inf", "sup", "lim", "log", "exp", "sin", "cos", "tan", "arg", "det", "sign"}
SPACES = {",": "0.167em", ":": "0.222em", ";": "0.278em", " ": "0.333em", "quad": "1em", "qquad": "2em", "!": "-0.167em"}
FONT_VARIANTS = {"mathrm": "normal", "mathbf": "bold", "mathit": "italic", "mathsf": "sans-serif", "mathtt": "monospace", "mathcal": "script", "mathbb": "double-struck"}


class MathParser:
    """A deliberately bounded TeX math grammar with explicit unsupported failures."""

    def __init__(self, source: str, display: bool):
        self.source = source
        self.display = display
        self.tokens = re.findall(r"\\(?:[A-Za-z]+|.)|[^\s]", source)
        self.pos = 0
        self.commands: set[str] = set()

    def fail(self, message: str) -> None:
        raise BuildError(f"{message}; math={self.source!r}")

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def pop(self) -> str:
        token = self.peek()
        if token is None:
            self.fail("Unexpected end of formula")
        self.pos += 1
        return token  # type: ignore[return-value]

    def expect(self, value: str) -> None:
        if self.pop() != value:
            self.fail(f"Expected {value!r}")

    def parse(self) -> str:
        result = self.sequence()
        if self.peek() is not None:
            self.fail(f"Unconsumed token {self.peek()!r}")
        return result

    def sequence(self, stops: frozenset[str] = frozenset()) -> str:
        nodes: list[str] = []
        while self.peek() is not None and self.peek() not in stops:
            if self.peek() in {"}", "&", r"\\", r"\end", r"\right"}:
                self.fail(f"Unexpected separator {self.peek()!r}")
            nodes.append(self.scripted_atom().markup)
        return tag("mrow", "".join(nodes))

    def scripted_atom(self) -> Atom:
        base = self.atom()
        sub = sup = None
        while self.peek() in {"_", "^", "'"}:
            kind = self.pop()
            if kind == "'":
                prime = tag("mo", "′")
                sup = tag("mrow", (sup or "") + prime)
            else:
                script = self.atom().markup
                if kind == "_":
                    if sub is not None:
                        self.fail("Duplicate subscript")
                    sub = script
                else:
                    if sup is not None:
                        self.fail("Duplicate superscript")
                    sup = script
        under = base.limits and self.display
        if sub is not None and sup is not None:
            return Atom(tag("munderover" if under else "msubsup", base.markup + sub + sup))
        if sub is not None:
            return Atom(tag("munder" if under else "msub", base.markup + sub))
        if sup is not None:
            return Atom(tag("mover" if under else "msup", base.markup + sup))
        return base

    def literal_group(self) -> str:
        self.expect("{")
        depth = 1
        parts: list[str] = []
        while depth:
            token = self.pop()
            if token == "{":
                depth += 1
            elif token == "}":
                depth -= 1
                if not depth:
                    break
            if token.startswith("\\"):
                if token not in {r"\_", r"\%", r"\&", r"\{", r"\}", r"\#", r"\$", "\\ "}:
                    self.fail("Unsupported command inside a literal text group")
                token = token[1:]
            parts.append(token)
        # Tokenization discards spaces, so recover the original literal group
        # through a separate token-offset scan for text commands (see text_group).
        return "".join(parts)

    def text_group(self) -> str:
        start = self.pos
        text = self.literal_group()
        # Match positions in the original source to preserve all prose spacing.
        matches = list(re.finditer(r"\\(?:[A-Za-z]+|.)|[^\s]", self.source))
        open_at = matches[start].end()
        close_at = matches[self.pos - 1].start()
        raw = self.source[open_at:close_at]
        if "{" in raw or "}" in raw:
            # Nested text groups are valid only as grouping braces, not hidden commands.
            raw = raw.replace("{", "").replace("}", "")
        raw = re.sub(r"\\([_%&{}#$ ])", r"\1", raw)
        return raw if raw else text

    def delimiter(self) -> str:
        token = self.pop()
        if token == ".":
            return ""
        if token in {"(", ")", "[", "]", "|", "/"}:
            value = token
        elif token in {r"\{", r"\}"}:
            value = token[1:]
        elif token.startswith("\\") and token[1:] in SYMBOLS:
            self.commands.add(token[1:])
            value = SYMBOLS[token[1:]]
        else:
            self.fail(f"Unsupported delimiter {token!r}")
        return tag("mo", html.escape(value), stretchy="true", fence="true", symmetric="true")

    def atom(self) -> Atom:
        token = self.pop()
        if token == "{":
            contents = self.sequence(frozenset({"}"}))
            self.expect("}")
            return Atom(contents)
        if token in {"}", "^", "_", "&"}:
            self.fail(f"Missing base or unmatched token {token!r}")
        if not token.startswith("\\"):
            if token.isdigit():
                return Atom(tag("mn", token))
            if token.isalpha():
                return Atom(tag("mi", html.escape(token)))
            value = {"-": "−", "*": "∗"}.get(token, token)
            # TeX's ordinary parentheses/brackets/vertical bars have normal
            # glyph height. MathML otherwise stretches them to an unrelated
            # fraction or summation elsewhere in the surrounding mrow.
            return Atom(tag("mo", html.escape(value), stretchy="false"))
        command = token[1:]
        self.commands.add(command)
        if command in {"{", "}", "_", "%", "&", "#", "$"}:
            return Atom(tag("mo", html.escape(command), stretchy="false"))
        if command in SPACES:
            return Atom(tag("mspace", width=SPACES[command]))
        if command in GREEK:
            return Atom(tag("mi", GREEK[command]))
        if command in SYMBOLS:
            return Atom(tag("mo", SYMBOLS[command], stretchy="false"))
        if command in BIG_OPERATORS:
            return Atom(tag("mo", BIG_OPERATORS[command], largeop="true", movablelimits="true"), True)
        if command in NAMED_OPERATORS:
            return Atom(tag("mo", command, movablelimits="true"), command in {"min", "max", "inf", "sup", "lim"})
        if command in {"frac", "dfrac", "tfrac", "binom"}:
            numerator = self.atom().markup
            denominator = self.atom().markup
            if command == "binom":
                return Atom(tag("mrow", tag("mo", "(", stretchy="true", fence="true") + tag("mfrac", numerator + denominator, linethickness="0") + tag("mo", ")", stretchy="true", fence="true")))
            return Atom(tag("mfrac", numerator + denominator))
        if command == "sqrt":
            if self.peek() == "[":
                self.pop()
                degree = self.sequence(frozenset({"]"}))
                self.expect("]")
                return Atom(tag("mroot", self.atom().markup + degree))
            return Atom(tag("msqrt", self.atom().markup))
        if command in FONT_VARIANTS:
            variant = FONT_VARIANTS[command]
            body = self.atom().markup
            # Chromium does not propagate mathvariant on mstyle consistently.
            # Apply it directly to every identifier/number in the chosen group.
            body = re.sub(r"<(mi|mn)>", lambda m: f'<{m[1]} mathvariant="{variant}">', body)
            return Atom(tag("mstyle", body, mathvariant=variant))
        if command in {"rm", "bf"}:
            body = self.sequence(frozenset({"}", "&", r"\\", r"\end"}))
            variant = "normal" if command == "rm" else "bold"
            body = re.sub(r"<(mi|mn)>", lambda m: f'<{m[1]} mathvariant="{variant}">', body)
            return Atom(tag("mstyle", body, mathvariant=variant))
        if command in {"text", "textrm", "texttt", "operatorname"}:
            value = html.escape(self.text_group())
            if command == "operatorname":
                return Atom(tag("mo", value))
            # MathML trims/collapses ordinary mtext boundary spaces. Explicit
            # nonbreaking spaces preserve TeX text such as `no ` and ` satisfies `.
            value = re.sub(r"\s", "\u00a0", value)
            if command == "texttt":
                return Atom(tag("mtext", value, mathvariant="monospace"))
            return Atom(tag("mtext", value))
        if command == "left":
            opening = self.delimiter()
            contents = self.sequence(frozenset({r"\right"}))
            self.expect(r"\right")
            self.commands.add("right")
            return Atom(tag("mrow", opening + contents + self.delimiter()))
        if command == "not":
            relation = self.pop()
            negations = {r"\subseteq": "⊈", r"\supseteq": "⊉", r"\in": "∉", "=": "≠", r"\le": "≰", r"\ge": "≱"}
            if relation not in negations:
                self.fail(f"Unsupported negated relation {relation!r}")
            if relation.startswith("\\"):
                self.commands.add(relation[1:])
            return Atom(tag("mo", negations[relation]))
        if command in {"overline", "bar", "hat", "tilde", "vec"}:
            accents = {"overline": "¯", "bar": "¯", "hat": "^", "tilde": "~", "vec": "→"}
            return Atom(tag("mover", self.atom().markup + tag("mo", accents[command], stretchy="true"), accent="true"))
        if command == "begin":
            return self.environment(self.literal_group())
        self.fail(f"Unsupported TeX command \\{command}")
        raise AssertionError("unreachable")

    def environment(self, name: str) -> Atom:
        if name not in {"aligned", "cases", "matrix", "pmatrix", "bmatrix"}:
            self.fail(f"Unsupported TeX environment {name!r}")
        rows: list[str] = []
        cells: list[str] = []
        while True:
            cells.append(tag("mtd", self.sequence(frozenset({"&", r"\\", r"\end"}))))
            separator = self.pop()
            if separator == "&":
                continue
            rows.append(tag("mtr", "".join(cells)))
            cells = []
            if separator == r"\\":
                continue
            if separator != r"\end" or self.literal_group() != name:
                self.fail("Unmatched math environment")
            self.commands.add("end")
            break
        body = tag("mtable", "".join(rows), columnalign="left" if name in {"aligned", "cases"} else "center", rowspacing="0.35em", columnspacing="0.7em")
        delimiters = {"cases": ("{", ""), "pmatrix": ("(", ")"), "bmatrix": ("[", "]")}
        if name in delimiters:
            left, right = delimiters[name]
            body = tag("mrow", tag("mo", left, stretchy="true", fence="true") + body + (tag("mo", right, stretchy="true", fence="true") if right else ""))
        return Atom(body)


CSS = """
@page { size: A4; margin: 19mm 20mm 19mm 20mm; }
* { box-sizing: border-box; }
html { background: white; color: #111; }
body { width: 170mm; margin: 0 auto; font: 10.5pt/1.34 Cambria, 'Times New Roman', serif; }
h1 { font-size: 20pt; line-height: 1.13; font-weight: 700; text-align: center; margin: 0 0 15pt; }
h2 { font-size: 12.1pt; line-height: 1.2; margin: 17pt 0 7pt; break-after: avoid; }
h3 { font-size: 11pt; line-height: 1.2; margin: 12pt 0 5pt; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 4pt; break-after: avoid; }
p { margin: 0 0 7.3pt; text-align: justify; orphans: 3; widows: 3; }
p:has(+ .display-math) { break-after: avoid; }
.byline { text-align: center; font-size: 10pt; line-height: 1.45; margin: 0 0 18pt; }
.display-math { margin: 8pt 0 10pt; padding: 1pt 0; break-inside: avoid; text-align: center; }
math { font-family: 'Cambria Math', 'STIX Two Math', math; font-size: 1em; }
math[display=block] { margin: 0; }
mtext { font-family: Cambria, 'Times New Roman', serif; }
.math-with-punctuation { display: inline-block; white-space: nowrap; }
table { border-collapse: collapse; width: 100%; font-size: 9.2pt; line-height: 1.28; margin: 11pt 0 13pt; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th, td { padding: 5pt 6pt; text-align: left; vertical-align: top; border-bottom: 0.4pt solid #bbb; }
th { border-top: 1pt solid #111; border-bottom: 0.8pt solid #111; font-weight: 700; }
tbody tr:last-child td { border-bottom: 1pt solid #111; }
table.compact th, table.compact td { padding: 3.7pt 5pt; }
a { color: inherit; text-decoration: none; }
code { font: 8.8pt Consolas, monospace; overflow-wrap: anywhere; }
pre { white-space: pre-wrap; font: 8.8pt/1.3 Consolas, monospace; border-left: 1pt solid #999; padding-left: 9pt; }
ul, ol { margin: 5pt 0 9pt; padding-left: 19pt; }
li { margin-bottom: 4pt; }
blockquote { margin: 8pt 13pt; border-left: 1pt solid #777; padding-left: 10pt; }
hr { border: 0; border-top: 0.6pt solid #aaa; margin: 12pt 0; }
.references p { text-align: left; font-size: 9.5pt; line-height: 1.3; }
"""


class Markdown:
    def __init__(self, source: str):
        self.source = source
        self.display_count = 0
        self.inline_count = 0
        self.tables = 0
        self.commands: set[str] = set()
        self.title = "Working report"
        self.current_line = 0

    def math(self, source: str, display: bool) -> str:
        try:
            parser = MathParser(source, display)
            contents = parser.parse()
        except BuildError as exc:
            raise BuildError(f"Source line {self.current_line}: {exc}") from exc
        self.commands.update(parser.commands)
        self.display_count += int(display)
        self.inline_count += int(not display)
        number = self.display_count if display else self.inline_count
        attrs = {"xmlns": "http://www.w3.org/1998/Math/MathML", "display": "block" if display else "inline", "aria-label": source, "data-formula": f"{'display' if display else 'inline'}-{number}"}
        return tag("math", contents, **attrs)

    def inline(self, source: str) -> str:
        chunks: list[str] = []
        i = 0
        while i < len(source):
            if source.startswith("![", i):
                raise BuildError("Image embedding is not in this offline working-paper grammar")
            if source[i] == "$":
                end = i + 1
                while end < len(source) and (source[end] != "$" or source[end - 1] == "\\"):
                    end += 1
                if end >= len(source) or end == i + 1:
                    raise BuildError(f"Unmatched/empty inline math at source line {self.current_line}")
                markup = self.math(source[i + 1:end], False)
                i = end + 1
                punctuation = re.match(r"[.,;:!?\)\]]+", source[i:])
                if punctuation:
                    markup = tag("span", markup + html.escape(punctuation[0]), **{"class": "math-with-punctuation"})
                    i += len(punctuation[0])
                chunks.append(markup)
                continue
            if source.startswith(r"\(", i):
                end = source.find(r"\)", i + 2)
                if end < 0:
                    raise BuildError("Unmatched inline \\( formula")
                markup = self.math(source[i + 2:end], False)
                i = end + 2
                punctuation = re.match(r"[.,;:!?\)\]]+", source[i:])
                if punctuation:
                    markup = tag("span", markup + html.escape(punctuation[0]), **{"class": "math-with-punctuation"})
                    i += len(punctuation[0])
                chunks.append(markup)
                continue
            if source[i] == "`":
                end = source.find("`", i + 1)
                if end < 0:
                    raise BuildError("Unmatched inline code delimiter")
                chunks.append(tag("code", html.escape(source[i + 1:end])))
                i = end + 1
                continue
            if source.startswith("**", i):
                end = source.find("**", i + 2)
                if end < 0:
                    raise BuildError("Unmatched bold delimiter")
                chunks.append(tag("strong", self.inline(source[i + 2:end])))
                i = end + 2
                continue
            if source[i] == "*":
                end = source.find("*", i + 1)
                if end < 0:
                    raise BuildError("Unmatched italic delimiter")
                chunks.append(tag("em", self.inline(source[i + 1:end])))
                i = end + 1
                continue
            if source[i] == "[":
                match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", source[i:])
                if match:
                    url = match[2]
                    if re.match(r"(?i)(?:javascript|data|file):", url):
                        raise BuildError("Unsafe source link scheme")
                    chunks.append(tag("a", self.inline(match[1]), href=url))
                    i += len(match[0])
                    continue
            if source[i] == "\\" and i + 1 < len(source) and source[i + 1] in "$*_`[]":
                chunks.append(html.escape(source[i + 1]))
                i += 2
                continue
            chunks.append(html.escape(source[i]))
            i += 1
        return "".join(chunks)

    @staticmethod
    def cells(line: str) -> list[str]:
        line = line.strip().strip("|")
        cells: list[str] = []
        cell: list[str] = []
        in_math = False
        for i, char in enumerate(line):
            escaped = i > 0 and line[i - 1] == "\\"
            if char == "$" and not escaped:
                in_math = not in_math
            if char == "|" and not escaped and not in_math:
                cells.append("".join(cell).strip())
                cell = []
            else:
                cell.append(char)
        cells.append("".join(cell).strip())
        return cells

    def build(self) -> str:
        lines = self.source.splitlines()
        result: list[str] = []
        i = 0
        references = False
        while i < len(lines):
            self.current_line = i + 1
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line in {"$$", r"\["}:
                closing = "$$" if line == "$$" else r"\]"
                start = i + 1
                i = start
                while i < len(lines) and lines[i].strip() != closing:
                    i += 1
                if i == len(lines):
                    raise BuildError(f"Unclosed display formula at line {start}")
                result.append('<div class="display-math">' + self.math("\n".join(lines[start:i]), True) + "</div>")
                i += 1
                continue
            heading = re.match(r"^(#{1,4})\s+(.+)$", line)
            if heading:
                level = len(heading[1])
                if level == 1:
                    self.title = heading[2]
                if heading[2].startswith("References") and not references:
                    result.append('<section class="references">')
                    references = True
                result.append(tag(f"h{level}", self.inline(heading[2])))
                i += 1
                continue
            if re.fullmatch(r"[-*_]{3,}", line):
                result.append("<hr>")
                i += 1
                continue
            if line.startswith("```"):
                code: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code.append(lines[i])
                    i += 1
                if i == len(lines):
                    raise BuildError("Unclosed Markdown code block")
                result.append(tag("pre", tag("code", html.escape("\n".join(code)))))
                i += 1
                continue
            if line.startswith("|") and i + 1 < len(lines) and all(re.fullmatch(r":?-{3,}:?", c) for c in self.cells(lines[i + 1])):
                headers = self.cells(line)
                aligns = self.cells(lines[i + 1])
                if len(headers) != len(aligns):
                    raise BuildError("Table header/alignment column mismatch")
                rows: list[str] = []
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    cells = self.cells(lines[i])
                    if len(cells) != len(headers):
                        raise BuildError(f"Table column mismatch at line {i + 1}")
                    row = []
                    for value, alignment in zip(cells, aligns):
                        style = "text-align:right" if alignment.endswith(":") and not alignment.startswith(":") else "text-align:center" if alignment.startswith(":") and alignment.endswith(":") else "text-align:left"
                        row.append(tag("td", self.inline(value), style=style))
                    rows.append(tag("tr", "".join(row)))
                    i += 1
                self.tables += 1
                table_body = tag("thead", tag("tr", "".join(tag("th", self.inline(c)) for c in headers))) + tag("tbody", "".join(rows))
                result.append(tag("table", table_body, **{"class": "compact" if len(rows) > 10 else ""}))
                continue
            list_match = re.match(r"^(?:[-+*]|\d+\.)\s+", line)
            if list_match:
                ordered = line[0].isdigit()
                items: list[str] = []
                while i < len(lines):
                    match = re.match(r"^(?:[-+*]|\d+\.)\s+(.+)$", lines[i].strip())
                    if not match:
                        break
                    items.append(tag("li", self.inline(match[1])))
                    i += 1
                result.append(tag("ol" if ordered else "ul", "".join(items)))
                continue
            if line.startswith("> "):
                result.append(tag("blockquote", tag("p", self.inline(line[2:]))))
                i += 1
                continue
            parts = [lines[i].rstrip()]
            i += 1
            while i < len(lines) and lines[i].strip():
                next_line = lines[i].strip()
                if next_line.startswith(("#", "|", "```")) or next_line in {"$$", r"\["}:
                    break
                parts.append(lines[i].rstrip())
                i += 1
            # The initial metadata paragraph preserves the source's hard break.
            byline = parts[0].startswith("Prepared for ")
            content = "<br>".join(self.inline(p.strip()) for p in parts) if byline else self.inline(" ".join(p.strip() for p in parts))
            result.append(tag("p", content, **({"class": "byline"} if byline else {})))
        if references:
            result.append("</section>")
        return "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'; font-src 'none'; img-src 'none'; connect-src 'none';\"><title>" + html.escape(self.title) + "</title><style>" + CSS + "</style></head><body>" + "\n".join(result) + "</body></html>"


NODE_RENDERER = r"""
'use strict';
const fs = require('fs');
const path = require('path');
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const {chromium} = require(config.playwright);
(async () => {
  const context = await chromium.launchPersistentContext(config.profile, {
    executablePath: config.browser, headless: true,
    viewport: {width: 900, height: 1200},
    args: ['--disable-background-networking', '--disable-component-update',
      '--disable-default-apps', '--disable-sync', '--no-first-run',
      '--no-default-browser-check', '--disable-domain-reliability',
      '--disable-features=MediaRouter,OptimizationHints,AutofillServerCommunication,Translate',
      '--safebrowsing-disable-auto-update', '--disable-breakpad',
      '--metrics-recording-only', '--no-pings', '--disable-client-side-phishing-detection']
  });
  let intercepted = 0;
  try {
    await context.setOffline(true);
    await context.route('**/*', async route => { intercepted++; await route.abort(); });
    const page = context.pages()[0] || await context.newPage();
    await page.emulateMedia({media:'print'});
    await page.setContent(fs.readFileSync(config.html, 'utf8'), {waitUntil:'load'});
    await page.evaluate(() => document.fonts.ready);
    const layout = await page.evaluate(() => {
      const body = document.body.getBoundingClientRect();
      const overflows = [];
      for (const el of document.querySelectorAll('math,table,pre')) {
        const rect = el.getBoundingClientRect();
        const content = el.querySelector(':scope > mrow');
        const inner = content ? content.getBoundingClientRect() : rect;
        if (rect.right > body.right + 2 || rect.left < body.left - 2 || inner.width > body.width + 2 || el.scrollWidth > body.width + 2) {
          overflows.push({element:el.tagName, formula:el.dataset.formula || null,
            width:rect.width, innerWidth:inner.width, available:body.width});
        }
      }
      const probe = document.createElementNS('http://www.w3.org/1998/Math/MathML', 'math');
      probe.innerHTML = '<mfrac><mn>1</mn><mn>2</mn></mfrac>';
      document.body.append(probe);
      const fraction = probe.getBoundingClientRect();
      const numerator = probe.querySelector('mn').getBoundingClientRect();
      const mathmlSupported = fraction.height > numerator.height * 1.3;
      probe.remove();
      return {overflows, mathmlSupported, mathCount:document.querySelectorAll('math').length,
        textLength:document.body.innerText.length, bodyWidth:body.width};
    });
    if (!layout.mathmlSupported) throw Error('Native MathML fraction layout is unavailable');
    if (layout.overflows.length) throw Error('Formula/table overflow: '+JSON.stringify(layout.overflows));
    const header = '<div style="font:8px Cambria,serif;width:100%;padding:0 20mm;color:#555">Audit budgets for conditional financial-model certificates</div>';
    const footer = '<div style="font:9px Cambria,serif;width:100%;text-align:center;color:#333"><span class="pageNumber"></span> / <span class="totalPages"></span></div>';
    await page.pdf({path:config.output, format:'A4', printBackground:true,
      preferCSSPageSize:true, displayHeaderFooter:true, headerTemplate:header,
      footerTemplate:footer, margin:{top:'19mm',bottom:'19mm',left:'20mm',right:'20mm'},
      tagged:true, outline:true});
    console.log(JSON.stringify({renderer:'Chromium native MathML via local Playwright',
      browserVersion:context.browser().version(), interceptedRequests:intercepted, ...layout}));
  } finally { await context.close(); }
})().catch(e => { console.error(e.stack || String(e)); process.exitCode=1; });
"""


def find_browser(explicit: Path | None) -> Path:
    candidates = [explicit] if explicit else [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate.resolve()
    raise BuildError("No already-installed Chrome/Edge executable found; pass --browser")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Parse in memory only; no browser or PDF")
    mode.add_argument("--render", action="store_true", help="Create PDF; caller must run the skill marker first")
    parser.add_argument("--source", type=Path, default=PAPER_DIR / "manuscript.md")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tmp-dir", type=Path, default=DEFAULT_TEMP)
    parser.add_argument("--node", type=Path, default=RUNTIME / "node/bin/node.exe")
    parser.add_argument("--playwright", type=Path, default=RUNTIME / "node/node_modules/playwright")
    parser.add_argument("--browser", type=Path)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    raw = args.source.read_bytes()
    source = raw.decode("utf-8-sig")
    document = Markdown(source)
    content = document.build()
    summary = {
        "mode": "check" if args.check else "render",
        "source": str(args.source.resolve()),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "renderer": "Chromium native MathML via local Playwright; not a LaTeX compiler",
        "display_formulas": document.display_count,
        "inline_formulas": document.inline_count,
        "tables": document.tables,
        "math_commands": sorted(document.commands),
        "html_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "pdf_created": False,
    }
    if args.check:
        summary["elapsed_seconds"] = round(time.perf_counter() - started, 4)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    if not args.node.is_file() or not (args.playwright / "package.json").is_file():
        raise BuildError("Bundled Node/Playwright unavailable; supply existing local --node/--playwright")
    browser = find_browser(args.browser)
    args.tmp_dir.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix="audit-paper-", dir=args.tmp_dir)).resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    html_path = temp / "manuscript.html"
    html_path.write_text(content, encoding="utf-8")
    node_path = temp / "render.cjs"
    node_path.write_text(NODE_RENDERER, encoding="utf-8")
    config = {"html": str(html_path), "output": str(args.output.resolve()),
              "playwright": str(args.playwright.resolve()), "browser": str(browser),
              "profile": str(temp / "browser-profile")}
    config_path = temp / "render_config.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    run = subprocess.run([str(args.node), str(node_path), str(config_path)], capture_output=True,
                         text=True, encoding="utf-8", timeout=100,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    (temp / "renderer_stdout.txt").write_text(run.stdout, encoding="utf-8")
    (temp / "renderer_stderr.txt").write_text(run.stderr, encoding="utf-8")
    if run.returncode:
        raise BuildError(f"Local renderer failed; details in {temp}:\n{run.stderr.strip()}")
    summary["layout"] = json.loads(run.stdout.strip().splitlines()[-1])
    summary["browser"] = str(browser)
    summary["temporary_directory"] = str(temp)
    summary["output"] = str(args.output.resolve())
    summary["output_sha256"] = hashlib.sha256(args.output.read_bytes()).hexdigest()
    summary["pdf_created"] = True
    summary["elapsed_seconds"] = round(time.perf_counter() - started, 4)
    # pypdf is bundled. This is a structural check, not the required visual review.
    from pypdf import PdfReader
    pdf = PdfReader(args.output)
    summary["pages"] = len(pdf.pages)
    summary["extracted_text_characters"] = sum(len(page.extract_text() or "") for page in pdf.pages)
    (temp / "build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        print(f"PDF build refused: {error}", file=sys.stderr)
        raise SystemExit(2)
