# Adversarial audit: 99-closest-integer

## Overall finding

The candidate does **not** contain a legitimate proof of the full HumanEval
source contract. A clean rebuild does close all eleven submitted claims with
`#Top`, and the term named `solutionProgram` is mechanically identical to the
trustedly regenerated `solution.mpy`. The proof is also result-constraining and
body-sensitive.

Those positive facts do not establish the required theorem:

1. The seven symbolic claims quantify over a synthetic
   `rationalString(N,D)` K constructor, not over the real `pyStr(S)` input
   accepted by `solution.py`. No claim connects arbitrary source strings to
   that constructor. The only claims over actual strings are four fixed
   examples. This materially narrows an unrestricted string source-contract
   domain.
2. The generated `Decimal` conversion semantics used for real `pyStr` inputs
   is materially false or partial on inputs for which the submitted Python
   program terminates. For `" 2.5 "`, Python returns 3 but K returns 0. For
   `"1_000.5"`, Python returns 1001 but K aborts. Thus the generated semantics
   is not a sound model of the real generated program over its accepted input
   domain.

The benchmark decision rule maps the first defect alone to `FAIL /
NOT_LEGIT`; the concrete semantics counterexamples independently reinforce
that decision.

The complete exact-command index is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). All execution was from fresh
source copies under `/tmp/audit-work/candidate`; no candidate-built definition
or cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout` =
`legacy-selected-stage1`, condition `bare`, and `semantics_mode` =
`GENERATED_SEMANTICS`. The mounted inputs are consistent with that mode:
`/reference/reference-semantics` is absent. There is no supplied or inferred
hidden semantics.

The campaign object in `/audit-campaign-lock.json` is byte-for-byte equal as
parsed JSON to the `audit_campaign` block in `/audit-input.json`, and the lock
hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value.

Every launcher-declared mount and every record required for
`legacy-selected-stage1` was present, readable, a real file/directory rather
than a symlink, and of the expected type:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured trace under `/generation-evidence/codex-trace/`;
- optional historical `/generation-evidence/usage.json`, which was present and
  checked.

Historical runtime metrics are not required for this legacy layout and were
not reconstructed. The structured trace contains 154 valid JSONL records, 26
tool calls and 26 corresponding outputs, and no JSON parse errors. It records
the historical candidate claim that one aggregate `kprove` run printed
`#Top`; this was treated only as untrusted history and independently rerun.

All individually recorded SHA-256 values match. The pipeline tree digest
recomputed independently for `/candidate` is
`e6a87cb4839b11cfe9646941c4e168c30c01d5de3099b969a87e7cfd9643c990`,
matching the retained workspace hash in both invocation and generation-result
records. The recomputed structured-trace tree digest is
`aed59568d918d2003d559b5edf232c2f0d7a3d9042b2b478473e22a9245f0f2c`,
matching `usage.json`; the sole trace file also matches its separately recorded
file hash. An additional reviewer-defined path/type/file-hash manifest was
computed for both trees.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Every required proof
artifact (`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
`spec.k`, and `prove.sh`) is a regular file. No required artifact is missing,
changed, mistyped, or symlinked.

Evidence:

- [`evidence/integrity_check.py`](evidence/integrity_check.py) and
  [`evidence/01-integrity.log`](evidence/01-integrity.log), exit 0;
- [`evidence/trace_summary.py`](evidence/trace_summary.py) and
  [`evidence/01-trace-summary.log`](evidence/01-trace-summary.log), exit 0;
- [`evidence/00-tool-versions.log`](evidence/00-tool-versions.log): K
  v7.1.293 and Python 3.10.12.

Stage result: provenance and audit infrastructure are intact. This is a
candidate verdict, not an `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `closest_integer(value)` to take a string
representing a number and return its nearest integer. Exact half ties must be
rounded away from zero; e.g. `14.5 -> 15` and `-14.5 -> -15`. The prompt states
no finite-size or finite-example bound.

The trusted canonical implementation trims some trailing zeros, converts with
binary `float`, handles text ending in `.5` specially, and otherwise uses
Python `round`. The candidate instead converts with `Decimal`, adds or
subtracts an exact half according to sign, and converts to `int`. For every
finite `Decimal` value this candidate algorithm implements the stated
nearest/ties-away rule.

### Trusted regeneration

Exact command:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy &&
cmp -s /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/candidate/solution.regenerated.mpy &&
sha256sum /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/candidate/solution.regenerated.mpy
```

Exit was 0. Both files have SHA-256
`2b5c8519404cc2114c057ce044ba6085fb57df75861e95e9c12005d775d5500e`.
See [`evidence/02-regeneration.log`](evidence/02-regeneration.log).

### Independent differential testing

[`evidence/differential_test.py`](evidence/differential_test.py) independently
loads the trusted canonical and candidate entry points. Its contract oracle
uses a `Decimal` integer ratio plus integer quotient/remainder comparison; it
does not reuse the candidate's add/subtract-half algorithm. It exercised:

- all four documented examples;
- the empty string separately as an out-of-contract boundary;
- zero and both sign branches around `±0.5`;
- leading-point, explicit-plus, trailing-zero, scientific, large, and
  high-precision forms;
- 240 seeded fixed-decimal inputs and 71 seeded/systematic scientific inputs.

Across 336 valid cases the candidate had zero contract-oracle mismatches. The
empty string caused exceptions in both Python implementations. The canonical
had nine contract mismatches on scientific half ties and values affected by
binary-float precision. Those divergences favor the prompt's mathematical
contract and therefore are not candidate defects; a different correct
algorithm is allowed.

Command `python3 /audit-output/evidence/differential_test.py` exited 0.
Complete inputs and results are in
[`evidence/02-differential.log`](evidence/02-differential.log).
This finite testing supports implementation-to-contract fidelity only; it is
not a K proof.

## 3. Clean proof reconstruction

Only candidate source files and trusted inputs were copied to
`/tmp/audit-work`. The candidate mount contained no K compiled definition, and
no historical definition/cache was copied. The concrete and proof definitions
were independently created with explicit fresh output directories:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition semantic-audit-kompiled
```

Exit 0; see
[`evidence/03-kompile-semantic.log`](evidence/03-kompile-semantic.log).

```text
kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition verification-audit-kompiled
```

Exit 0; see
[`evidence/03-kompile-verification.log`](evidence/03-kompile-verification.log).

The candidate has one positive target-proof command covering all eleven
unlabelled claims:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

It exited 0 and printed exactly `#Top`; see
[`evidence/03-kprove-positive.log`](evidence/03-kprove-positive.log). Thus
closure under the submitted semantics/theory is independently confirmed.

For generated-semantics validation,
[`evidence/semantic_differential.py`](evidence/semantic_differential.py)
executed the freshly built LLVM definition and compared each final `<result>`
with both the real candidate Python function and the independent contract
oracle. Twenty-three ordinary, sign, half-boundary, scientific,
high-precision, and large-number inputs agreed. Two accepted Python inputs did
not:

- `value = " 2.5 "`: Python candidate = 3, oracle = 3, K = 0, `krun` exit 0.
  K's final environment contains `number = exactNum(25,100)`.
- `value = "1_000.5"`: Python candidate = 1001, oracle = 1001, while K invokes
  `String2Int("1_0005")`, aborts, and `krun` exits 255.

The aggregate reviewer command exits 1 because these two mismatches are
intentional findings, not because of audit infrastructure. Full commands and
bounded outputs are in
[`evidence/03-semantic-differential.log`](evidence/03-semantic-differential.log).

Stage result: clean proof reconstruction succeeds, but clean concrete
reconstruction refutes the generated semantics' fidelity over the real
program's accepted domain.

## 4. Adequacy and real-program pinning

### Plain-language claim scope

The eleven entry claims say:

1. For synthetic argument `rationalString(N,D)`, D>0, the exact program returns
   `roundNearestAway(N,D)`.
2. For every nonnegative I, abstract positive half tie `(2I+1)/2` returns I+1.
3. The corresponding abstract negative half tie returns -(I+1).
4. Abstract positive quarter point `(4I+1)/4` returns I.
5. Abstract positive three-quarter point `(4I+3)/4` returns I+1.
6. Abstract negative quarter point returns -I.
7. Abstract negative three-quarter point returns -(I+1).
8–11. Actual strings `"10"`, `"15.3"`, `"14.5"`, and `"-14.5"` return the
   documented values.

Every claim starts with `<env> .Map` and `<result> noResult`; every
postcondition fixes `<result>` to a particular `pyInt` and fixes the final
environment. There is no free return variable, tautology, or one-way
property-only implication. There are no loop or helper claims because the
submitted body has neither loops nor program-defined helpers.

Every precondition is satisfiable. Reviewer substitutions were N=7,D=2 for
claim 1, I=2 for claims 2–7, and the stated ground values for claims 8–11.
All eleven substituted results matched both Python implementations. See
[`evidence/adequacy_witness.py`](evidence/adequacy_witness.py) and
[`evidence/04-adequacy-witness.log`](evidence/04-adequacy-witness.log), exit 0.

### Program identity

The proof does not read `solution.mpy` dynamically; `verification.k` defines a
functional `solutionProgram` term. A reviewer script extracted that RHS,
regenerated `solution.mpy` with the trusted translator, normalized only the
two equivalent spellings of the empty `Stmts` list, parsed both as sort
`Program`, and compared their JSON KASTs. Both canonicalized KASTs have SHA-256
`63cfef4ad2b0dc1f6e6ff62cd4d0951100d56fd2a7b720ff6f0aab948229ddae`
and are structurally equal. See
[`evidence/program_term_compare.py`](evidence/program_term_compare.py) and
[`evidence/04-program-term-compare.log`](evidence/04-program-term-compare.log).

An attempted direct functional reachability claim is retained in
`04-program-identity*.log`; the installed Haskell backend reports functional
claims unsupported. The successful KAST comparison supplies the requested
mechanical constructor-level comparison without treating that backend
limitation as a candidate defect.

Body sensitivity was tested by changing the positive branch in the term
actually executed by a reviewer claim from addition to subtraction. The
mutated definition compiled (exit 0), and its `"14.5" -> 15` proof failed
(exit 1) after reaching `pyInt(14)`. See
[`evidence/body-mutant-verification.k`](evidence/body-mutant-verification.k),
[`evidence/body-mutant-spec.k`](evidence/body-mutant-spec.k),
[`evidence/04-body-mutant-build.log`](evidence/04-body-mutant-build.log), and
[`evidence/04-body-mutant-proof.log`](evidence/04-body-mutant-proof.log).

### Material adequacy failure

Exact body identity is not enough. Claims 1–7 execute that body with a value of
K constructor `rationalString`, which is not the `pyStr` constructor used for a
real Python string. The rule

```text
rationalString(N,D) ~> toDecimal => exactNum(N,D)
```

bypasses all lexical conversion. No claim proves that arbitrary
`pyStr(S) ~> toDecimal` yields the corresponding N/D, nor even states a
relation among S, N, and D. Therefore the universal abstract-number theorem
cannot be instantiated to any unproved real source string. Only four fixed
`pyStr` examples are formal entry claims.

Finitely many examples do not prove the prompt's unrestricted domain. This is
the benchmark's explicit materially-narrowed-domain failure, not merely an
artifact-maintenance concern.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md), supported by
[`evidence/05-static-declaration-scan.log`](evidence/05-static-declaration-scan.log).
It enumerates:

- all syntax for `Program`, `Stmts`, five statement forms, six expression
  forms, values, results, and ten continuation items;
- all four configuration cells;
- 36 rules in `semantic.k`;
- three equations in `verification.k`;
- six parser functions, `exponentPosition [function,total]`,
  `solutionProgram [function]`, and `roundNearestAway [function]`;
- all eleven reachability claims.

There are no priority, simplification, owise, opaque-attribute, macro, or local
helper-module rules. `rationalString` is nevertheless inventoried as a
result-bearing abstract constructor because it controls the universal proof.

Every constructor used by `solution.mpy` maps to an explicit path: module
loading; statement sequencing; assignment; literals and lookup; `Decimal` and
`int` calls; exact rational addition/subtraction; comparison; branch; and
return. The `<k>`, `<arg>`, `<env>`, and `<result>` cells suffice for this
one-function body. Evaluation is left-to-right. Return correctly discards the
remaining function continuation; positive-branch concrete runs demonstrate
that the trailing negative return does not execute. Exact-rational arithmetic,
positive-denominator guards, comparison, and truncation are mathematically
valid. The two `roundNearestAway` guards are disjoint and cover every N under
D>0.

The textual builtin rules for `Decimal` and `int` would be over-broad as a
reusable Python semantics because they do not perform general binding lookup.
For the exact submitted module, however, the loader fixes the import and there
is no shadowing; no false conclusion witness exists on the actual control flow,
so these are recorded as limited rather than labelled unsound.

### Unsound used conversion rules and required witnesses

`semantic.k:86` unconditionally treats every `pyStr(S)` Decimal conversion as
`parseDecimal(S)`. `semantic.k:146-151` removes the first dot and chooses the
denominator from the total string length. This assumes every non-dot character
is a digit/sign, even though the real imported `Decimal` accepts surrounding
whitespace and underscores.

Concrete false-conclusion witness:

```text
S = " 2.5 ", P = 2
parseMantissaAt(S,P)
  => exactNum(String2Int(" 25 "), 10^(5-2-1))
  => exactNum(25,100)
```

Python's real conclusion is `Decimal(" 2.5 ") = 5/2`. The false K conclusion
propagates through the actual submitted body to result 0, whereas the real
program and contract oracle return 3. This is not merely missing evidence: it
is a witnessed false semantic result on a terminating input.

For the independently useful boundary `"1_000.5"`, the real program terminates
with 1001 but the same rule path calls the partial builtin
`String2Int("1_0005")` and aborts. That is a material used-construct coverage
gap.

### Result-bearing abstraction

`semantic.k:87` maps `rationalString(N,D)` directly to `exactNum(N,D)`. Taken as
a definition of a synthetic abstract input, the equation itself is not
mathematically false. It is not, however, a universal connection theorem for
the fixed `pyStr` conversion path: it contains no S and imports no proof that a
string parses to N/D. Claims 1–7 depend on this bridge, while the final
postconditions depend on the resulting exact number. Using the same N,D in
the input abstraction and result summary is conditional reasoning, not proof
of source string parsing.

Stage result: the local theory has a concrete semantic unsoundness on a used
operation and a material source-domain connection gap.

## 6. Fresh non-vacuity test

The reviewer-authored
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) uses the exact
submitted `solutionProgram`, the satisfiable actual input `"14.5"`, and changes
only the required result from the true 15 to the false 14.

Spec build/dry run:

```text
kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run
```

Exit 0; see
[`evidence/06-vacuity-build.log`](evidence/06-vacuity-build.log).

Proof:

```text
kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY-AUDIT
```

Exit 1 with `WarnStuckClaimState`. The residual has `.K`, the expected final
environment, and actual `<result> pyInt(15) </result>`, which cannot unify with
the mutated `pyInt(14)` target. See
[`evidence/06-vacuity-proof.log`](evidence/06-vacuity-proof.log).

This is meaningful non-vacuity evidence: the mutation parses, builds, reaches
the result-bearing obligation, and fails for exactly the intended mismatch.
Non-vacuity passes, but it cannot repair an inadequate/unsound theorem.

## 7. Proven versus assumed accounting

### What `#Top` precisely establishes

Under the submitted K theory:

- for every K integer N and positive K integer D, a configuration whose
  argument is the synthetic constructor `rationalString(N,D)` and whose
  computation is the exact submitted AST reaches `.K`, the exact three-entry
  environment, and `pyInt(roundNearestAway(N,D))`;
- the six half/quarter abstract families reach their stated specialized
  integer results;
- the four literal `pyStr` examples reach their stated results.

This is a partial-correctness reachability result under the candidate's
generated semantics. It is not a universal theorem over `pyStr(S)`, and it is
not by itself a theorem about CPython `Decimal`.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.293 backends and builtin INT/STRING/BOOL/MAP hooks | All builds, execution, proofs | Standard low-level toolchain trust boundary; version recorded and fresh builds used. Acceptable. |
| Trusted `py2mpy.py` | Program identity | Launcher hash matched; submitted term regenerated byte-identically. Acceptable. |
| `solutionProgram` functional equation | Every claim | Proof-local definition, but exact constructor identity was mechanically checked and body mutation was sensitive. Acceptable. |
| Exact-rational arithmetic and `roundNearestAway` equations | All symbolic results | Guarded, disjoint, complete over D>0, and ordinary integer mathematics. Acceptable. |
| Generated AST operational rules | Every claim | Mostly faithful for this exact body, but the used Decimal conversion path has a concrete false-result witness. Illegitimate as a universal real-program boundary. |
| `rationalString(N,D)` direct conversion | Claims 1–7 | Conditional abstract primitive with no connection to real strings. It may support an abstract-number theorem, but cannot discharge the HumanEval string contract. Materially inadequate. |
| Concrete `parseDecimal` equations as a model of CPython `Decimal` | Claims 8–11 and any attempted real-string generalization | No universal bridge theorem; finite tests only; concretely false/partial on accepted inputs. Illegitimate for the required domain. |
| Reviewer differential tests | Candidate implementation fidelity and finite semantic checks | Reproducible finite evidence only. They neither replace `kprove` nor universally validate an abstraction. |
| Trusted canonical implementation | Differential comparison | Empirical comparator, not proof axiom. Its nine prompt-contract mismatches were retained and judged rather than hidden. |

There are no opaque-attributed symbols. The only opaque-in-effect,
result-bearing boundary is the synthetic `rationalString` representation and
its unproved relation to actual input text.

### Gate and decision summary

- Clean verification: **PASS** — all eleven submitted claims close with fresh
  `#Top`.
- Real-program soundness (Kit Gate A): **FAIL** — real accepted strings have a
  witnessed false/aborting semantic path, and the universal proof bypasses that
  path.
- Intent adequacy (Kit Gate B): **FAIL** — seven abstract-number families plus
  four actual examples do not cover the unrestricted HumanEval string domain.
- Non-vacuity/result sensitivity: **PASS**.
- Evidence auditability (Kit Gate C): reviewer evidence is reproducible, but
  later evidence cannot cure Gates A/B.

The proof therefore establishes a genuine but limited theorem inside the
candidate's theory, not the required partial-correctness theorem of the real
generated program. Under the benchmark's explicit mapping, this materially
narrowed domain and materially unsound generated semantics require failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
