# Independent adversarial audit — 161-solve

The candidate is **not a legitimate proof of the real generated program**.
Fresh reconstruction does produce `#Top`, and a fresh false-postcondition
mutation is correctly rejected. However, the proof is about an ASCII-only,
program-specific evaluator that is materially false for Python strings, while
the submitted `solution.py` itself also diverges from the trusted canonical
implementation on valid Unicode inputs. These are candidate defects with
concrete witnesses, not audit-infrastructure uncertainty.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount is consistent
with that mode: `/reference/reference-semantics` does not exist. There is
therefore no infrastructure breach and no supplied language definition to
infer or use.

The candidate `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`fa29d7f413a74f20646e32cd02cb87cdd6766bf4f81745a92db8bcd19d9734d2`),
and its `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
Those hashes also equal the untrusted values in `run-input.json`. See
[stage1-integrity-comparison.log](/audit-output/evidence/stage1-integrity-comparison.log).

All expected candidate records and source deliverables are present as regular
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, the structured JSONL trace, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`; `prove.sh` is executable. None is a symlink or mistyped object.
There are no candidate helper K files. No required source artifact is missing
or changed. The complete type and tree evidence is in
[stage1-required-artifact-types.log](/audit-output/evidence/stage1-required-artifact-types.log)
and
[stage1-filesystem-inventory.log](/audit-output/evidence/stage1-filesystem-inventory.log).

The extra `semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, and
`.pyc` entries are candidate-built evidence, not trusted inputs. They were not
copied into the build tree and were never used. A source-only copy was made
under `/tmp/audit-work`; see
[stage1-source-copy.log](/audit-output/evidence/stage1-source-copy.log).

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all structured trace records only as untrusted claims.
They report a bare/no-supplied-semantics run, exit 0, and a final `#Top`, while
the longer log also records several discarded compiler/backend failures during
generation. Their bounded summary, hashes, record counts, and terminal claims
are preserved in
[stage1-untrusted-provenance.log](/audit-output/evidence/stage1-untrusted-provenance.log).
None was used as proof of correctness.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify this behavior for a
Python string:

1. Examine every character using Python `str.isalpha`.
2. If at least one character is a letter, replace each *letter* with its
   `swapcase` result and leave every non-letter unchanged.
3. If there are no letters, reverse the entire string.

The canonical implementation realizes that contract with an explicit
per-character loop. The submitted implementation instead uses:

```python
return s.swapcase() if any(c.isalpha() for c in s) else s[::-1]
```

This is equivalent for ordinary ASCII because ASCII non-letters are unchanged
by `swapcase`. It is not equivalent over the prompt's unrestricted Python
`str` domain: some cased Unicode characters are not `isalpha()`, yet
`swapcase()` changes them.

Regenerating from the scratch `solution.py` with the trusted translator
produced byte-identical `solution.mpy`; both have SHA-256
`914d9811632a2b1c06304570e53c89b82af04a1c79fdde6d9f7e11b42e8d94eb`.
See
[stage2-translation-identity.log](/audit-output/evidence/stage2-translation-identity.log).

The independent differential harness imported the trusted canonical entry
point and the scratch candidate entry point. It exercised all three documented
examples, the empty string, branch boundaries, Unicode boundaries, and every
string of length 0 through 4 over the representative alphabet
`a, Z, 0, #, é, Ⅰ, U+0345, 🙂`. Among 4,692 distinct inputs it found 2,466
mismatches. The minimal recorded witness is:

```text
input       = "aⅠ"
canonical   = "AⅠ"
candidate   = "Aⅰ"
```

Here `Ⅰ`.isalpha() is false, so the canonical code leaves it unchanged, while
the candidate's whole-string `swapcase()` changes it. The harness, bounded
command log, and complete input/result JSONL are
[differential_test.py](/audit-output/evidence/differential_test.py),
[stage2-python-differential.log](/audit-output/evidence/stage2-python-differential.log),
and
[differential-results.jsonl](/audit-output/evidence/differential-results.jsonl).
The nonzero harness status deliberately reports the observed mismatches.

This is a material implementation-to-contract divergence on a valid intended
input, independently of any K issue.

## 3. Clean proof reconstruction

All reconstruction used the source-only scratch copy and distinct fresh output
directories below `/tmp/audit-work/build`; no candidate definition or cache was
reused. The live toolchain was K 7.1.293, recorded in
[stage3-toolchain.log](/audit-output/evidence/stage3-toolchain.log).

The generated semantics compiled from source with the Haskell backend:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC
  --syntax-module MPY-SYNTAX
  --output-definition /tmp/audit-work/build/semantic-fresh-kompiled
```

It exited 0; see
[stage3-build-semantic.log](/audit-output/evidence/stage3-build-semantic.log).
The proof definition likewise compiled from `verification.k` and exited 0; see
[stage3-build-verification.log](/audit-output/evidence/stage3-build-verification.log).

`spec.k` contains one positive target claim. The independent command

```text
kprove spec.k
  --definition /tmp/audit-work/build/verification-fresh-kompiled
  --spec-module SPEC
```

exited 0 and printed exactly `#Top`; see
[stage3-positive-claim.log](/audit-output/evidence/stage3-positive-claim.log).
Thus the candidate's verification claim really does close under its submitted
theory.

Fresh concrete execution agrees with both Python implementations on the empty
case, all prompt examples, and focused ASCII branch boundaries. It disagrees
with the submitted Python program on 8 of 14 focused Unicode-inclusive cases:

| Input | Fresh K | Candidate Python | Canonical Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `"1234"` | `"4321"` | `"4321"` | `"4321"` |
| `"#a@C"` | `"#A@c"` | `"#A@c"` | `"#A@c"` |
| `"é"` | `"é"` | `"É"` | `"É"` |
| `"é1"` | `"1é"` | `"É1"` | `"É1"` |
| `"ß"` | `"ß"` | `"SS"` | `"SS"` |

In addition, the claimed concrete conversion to Unicode code points converts
`pstr("αΒ")` into `206::177::206::146` and ultimately reverses those bytes.
The commands, every per-case status, and results are in
[semantic_concrete_test.py](/audit-output/evidence/semantic_concrete_test.py),
[stage3-semantic-concrete-differential.log](/audit-output/evidence/stage3-semantic-concrete-differential.log),
[semantic-concrete-results.jsonl](/audit-output/evidence/semantic-concrete-results.jsonl),
and
[stage5-pstr-multibyte-witness.log](/audit-output/evidence/stage5-pstr-multibyte-witness.log).

Clean reconstruction therefore verifies closure but independently refutes the
generated semantics' claimed fidelity.

## 4. Adequacy and real-program pinning

The sole entry claim has no `requires` clause. In plain language, its
precondition is:

- `<k>` contains the hard-coded `Module(FuncDef("solve", ...))` constructor
  tree;
- `<input>` is any `S:PString`;
- `<result>` is `noResult`;
- the `isalpha` and `swapcase` call argument lists, and the generator's
  translated filter list, are unconstrained `Exprs` variables.

The actual submitted program is an instance because its two call-argument
lists are empty and the translator's no-filter generator sentinel is
`Bool(true)`.

The postcondition consumes `<k>`, preserves `<input>`, and requires `<result>`
to be exactly:

```text
expected(S)
= ifPString(hasAlpha(S), swapCase(S), reverse(S))
```

This is result-constraining: the result is neither free nor guarded by a
one-way implication. There are no helper or loop claims. The `<k>` AST in
`spec.k` structurally matches the byte-verified submitted `solution.mpy`;
the only generalization is the argument/filter variables just described.
The numbered source comparison is in
[stage5-numbered-sources.log](/audit-output/evidence/stage5-numbered-sources.log).

The precondition is satisfiable. Examples include
`S=.PString`, `S=97::98::.PString` (`"ab"`), and
`S=233::.PString` (`"é"`). Ground substitution shows the adequacy failure:

| Satisfying input | Claimed/fresh-K result | Candidate Python | Canonical Python |
|---|---|---|---|
| `.PString` | `""` | `""` | `""` |
| `97::98::.PString` | `"AB"` | `"AB"` | `"AB"` |
| `233::.PString` | `"é"` | `"É"` | `"É"` |

The last fresh K configuration is preserved in
[stage3-krun-direct-unicode-codepoint.log](/audit-output/evidence/stage3-krun-direct-unicode-codepoint.log);
the independent Python comparison is in
[stage3-semantic-concrete-differential.log](/audit-output/evidence/stage3-semantic-concrete-differential.log).

Accordingly, the claim pins the submitted constructor tree syntactically, but
its execution rules do not pin the real Python program semantically. Repeating
the same local functions in `expected` turns the proof into a correct
characterization of the candidate evaluator, not a correctness proof of the
generated Python program.

## 5. Rule-by-rule static soundness review

The complete candidate-local inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). It enumerates
every syntax production, configuration cell, function/`total` attribute, and
all 22 ordinary rules across `semantic.k` and `verification.k`, maps every
submitted constructor to its rule, and gives an individual assessment for
each. There are:

- 21 ordinary semantic/function rules in `semantic.k`;
- one definitional rule in `verification.k`;
- eight functions declared `total`, counting `expected`, and four additional
  functions not declared total;
- no `[functional]` declarations, opaque symbols, priority rules,
  simplification rules, macros, aliases, strictness declarations, or
  candidate helper K files.

The three-cell configuration is sufficient for the exact pure one-expression
body: computation, implicit input, and result. The top rule matches the actual
`solve(s)`/`Return(E)` structure and changes only the result. Abstract
`reverse/reverseAcc` is a standard structurally decreasing reversal;
`ifPString` has disjoint true/false rules. The local ASCII `isAlpha` and
`toggle` equations are internally exhaustive, and the structural list
functions are terminating and non-overlapping on normalized `PString`.

The material failures are result-bearing operational bridges:

1. **Concrete string conversion (`semantic.k:50-51`).** The file says Python
   strings are lists of Unicode code points, but fresh
   `pstr("αΒ")` becomes UTF-8 byte values. The intended input `"αΒ"` is a
   concrete false-conclusion witness; fresh K returns a byte-reversed value
   instead of Python `"Αβ"`.
2. **`any/isalpha` bridge (`semantic.k:90-94`).** It replaces the actual
   generator/method execution with ASCII-only `hasAlpha`. For the valid input
   `"é"` (`S=233::.PString`), Python `isalpha()` is true while the rule derives
   false.
3. **`swapcase` bridge (`semantic.k:98`).** It replaces Python `str.swapcase`
   with ASCII-only `swapCase`. On the same satisfying input, the bridge returns
   code point 233 while Python returns `"É"` (code point 201).
4. **Whole-program rule (`semantic.k:113-115`).** It inherits those false
   bridges. Fresh execution with `S=233::.PString` concludes `"é"` although
   the submitted program concludes `"É"`.

The ground Python primitive values, including the separate candidate-versus-
canonical `"aⅠ"` witness, are preserved in
[stage5-unicode-rule-witnesses.log](/audit-output/evidence/stage5-unicode-rule-witnesses.log).
These are witnesses on the prompt's actual Python-string domain, not
hypothetical unused constructs.

The `evalBool` pattern also ignores arbitrary `_ARGS` and `_IFS`, and the
`swapcase` pattern ignores arbitrary arguments. That is an unjustified broader
match domain than the exact submitted empty-argument/`Bool(true)` instance.
I treat this separately as an unsupported overbreadth rather than relying on
it for the verdict; the concrete actual-program witnesses above already
establish unsoundness.

Finally, `verification.k` defines `expected(S)` with exactly the same
`hasAlpha`, `swapCase`, and `reverse` symbols produced by execution. The
equation is a coherent local definition and does not introduce an opaque
oracle, but there is no bridge-free connection theorem from real Python
behavior to those symbols. In fact the witnesses disprove such a connection.
Thus the rule does not independently justify the task answer.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created the fresh mutation
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), preserving
the entry precondition and actual program AST while changing the result
obligation from `expected(S)` to `reverse(S)`.

The mutation is meaningfully false for the satisfying input
`S=97::98::.PString` (`"ab"`): the submitted body returns `"AB"`, while the
mutated postcondition requires `"ba"`. The independent witness is in
[stage6-ground-witness.log](/audit-output/evidence/stage6-ground-witness.log).

`kprove --dry-run` parsed and built the mutated claim successfully, exiting 0;
see
[stage6-mutation-dry-run.log](/audit-output/evidence/stage6-mutation-dry-run.log).
The actual proof then exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet equality:

```text
ifPString(hasAlpha(S), swapCase(S), reverseAcc(S,.PString))
= reverseAcc(S,.PString)
```

See
[stage6-mutation-proof.log](/audit-output/evidence/stage6-mutation-proof.log).
This is a valid non-vacuity result: the positive claim discriminates its
postcondition. It does not cure the false semantics.

## 7. Proven versus assumed accounting

Precisely stated, the successful reachability proof establishes:

> For every candidate-local `PString S` and every argument/filter `Exprs`
> accepted by the hard-coded claim pattern, executing that constructor tree
> under `SEMANTIC` consumes `<k>` and changes `noResult` to
> `ifPString(hasAlpha(S), swapCase(S), reverse(S))`.

It does **not** establish that `hasAlpha` is Python `str.isalpha`, that
`swapCase` is Python `str.swapcase`, that `pstr` faithfully embeds every Python
string, or that the submitted `solution.py` equals the trusted canonical
function.

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K 7.1.293 Haskell backend and imported `BOOL`, `INT`, `STRING` operations | Compilation, arithmetic/boolean evaluation, and string hooks used by every proof/run | Normal low-level trust boundary. The candidate's *use* of the string hooks in `pstrAt` is empirically false as a Python bridge. |
| Trusted `py2mpy.py` | Syntactic Python-AST-to-constructor bridge | Acceptable trusted input; byte identity proves the submitted `.mpy` is its output. It supplies no semantic correctness by itself. |
| `PString` as Unicode code-point lists and `pstr/pstrAt` | Concrete-input bridge; affects all concrete K runs | Illegitimate as submitted over the unrestricted domain; `"αΒ"` is a counterexample. |
| ASCII `isAlpha/hasAlpha` | Controls the `IfExp` branch and final result | Illegitimate replacement for Python `isalpha`; `"é"` is a counterexample. |
| ASCII `toggle/swapCase` | Determines the then-branch and final result | Illegitimate replacement for Python `swapcase`; `"é"` is a counterexample. |
| `evalBool`, `evalString`, and whole-program rules | Program-derived operational summaries | No bridge-free universal connection theorem exists, and concrete actual-program witnesses refute value fidelity. |
| `expected` | Final result specification | Locally well-defined, but concerning/circular as an intent bridge because it repeats the same false semantic primitives. |
| Structural `reverse`, `reverseAcc`, `ifPString` | Local list mathematics | Acceptable ordinary mathematical definitions over abstract `PString`. |
| Differential/concrete tests | Empirical Python fidelity and K/Python comparison | Finite evidence only. Here it supplies counterexamples, so no universal inference is needed to refute the claimed bridges. |

There are no opaque symbols or declared external primitives. The unproved
informal bridge is instead the candidate's assertion that its ASCII,
program-specific rules mean Python Unicode operations; that assertion is both
value-bearing and false.

Gate accounting:

- Real-program soundness: **FAIL** because result-bearing semantic bridges
  produce false conclusions for satisfying intended inputs.
- Result constraint/non-vacuity: **PASS**.
- Intent adequacy: **FAIL** because the submitted Python implementation
  materially diverges from the trusted canonical function and the K evaluator
  diverges from both.
- Evidence auditability: reviewer reconstruction and counterexamples are
  reproducible; the evidence manifest is
  [evidence-manifest.log](/audit-output/evidence/evidence-manifest.log).

The clean `#Top` is genuine only for the candidate's unsound local theory.
Because the proof relies on materially false semantics and the generated
program itself is not faithful to the trusted contract, the required decision
is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
