# Independent adversarial audit: HumanEval 60 `sum_to_n`

This audit completed all seven required stages against fresh source copies and K
definitions. The candidate's one positive reachability claim does rebuild and
close with `#Top`, and a fresh off-by-one mutation confirms that the claim is
result-constraining. Those facts are not sufficient for legitimacy: the
candidate's generated semantics gives Python floor division (`//`) the meaning
of K's truncating division (`/Int`). A concrete witness at an argument satisfying
the claimed input domain makes the K theory prove `-3 // 2 == -1`, although
Python evaluates it to `-2`. This is a witnessed, globally false semantic rule,
not a timeout or an evidence gap. The candidate also narrows the unqualified
`int` input contract to `N >= 0` and differs from the trusted canonical function
at `n=-2` and `n=-3`.

The resulting decision is **FAIL / NOT_LEGIT**. The failure is a candidate
soundness failure, not an audit-infrastructure failure.

## Audit isolation and evidence

`/candidate` was read only. Candidate-built
`/candidate/verification-kompiled/`, bytecode, logs, reports, and traces were
never used as definitions or proof results. The source reconstruction lives
under `/tmp/audit-work/fresh`; fresh definitions were emitted there as
`semantic-kompiled-audit/` and `verification-kompiled-audit/`. Reviewer-authored
tests, mutations, and bounded logs are under
[`/audit-output/evidence/`](evidence/).

The live toolchain was K `v7.1.293`; paths and version outputs are recorded in
[`environment.log`](evidence/environment.log). Every executed source copied
from `/candidate` or `/reference` remained byte-identical to its origin, as
shown in
[`scratch-source-integrity.log`](evidence/scratch-source-integrity.log).

## 1. Input and provenance integrity

### Generated-semantics boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, including as a dangling symlink, as
required. The trusted inputs `/reference/canonical.py`,
`/reference/prompt.py`, and `/reference/py2mpy.py` are regular, non-symlink
files. There is therefore no mount contradiction and no basis for
`AUDIT_ERROR`.

The complete type, mode, size, and symlink inventory is in
[`stage1-integrity.log`](evidence/stage1-integrity.log). No required candidate
source or claim artifact is missing, mistyped, changed against a required
trusted counterpart, or symlinked:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are regular files.
- `prompt.py` and `py2mpy.py` are byte-identical to the trusted mounted files.
- `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`
  are regular files.
- The only candidate K source files are those three K files; there is no
  generated helper K file to inventory.
- The structured trace is one regular JSONL file. Its type, hash, and the
  candidate's short claims are recorded in
  [`stage1-untrusted-claims.log`](evidence/stage1-untrusted-claims.log).

The candidate also contains `verification-kompiled/`, `__pycache__/`, and
`prove.sh`. These are additional generated outputs, not substitutes for any
required source. They were ignored for reconstruction. No candidate-compiled
definition or cache was copied into the audit definitions.

### Untrusted generation claims

`run-input.json` identifies problem `60-sum-to-n` and the `bare` condition.
`metrics.json` claims a successful, non-timeout generation. `codex-last.txt`,
`codex-output.log`, and the structured trace claim that examples passed and
`kprove` printed `#Top`. They also reveal an earlier parser failure followed by
later successful runs. None of this was accepted as proof evidence.

All 101 structured-trace records were parsed by the reviewer-authored
[`read_generation_trace.py`](evidence/read_generation_trace.py); the extracted
human-readable messages, calls, patches, and record-type counts are in
[`stage1-generation-trace.log`](evidence/stage1-generation-trace.log).
Encrypted reasoning blobs were recorded by presence/length and were neither
interpretable nor trusted.

**Stage 1 result:** PASS. There is no infrastructure breach or required-source
integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt declares:

```python
def sum_to_n(n: int):
    """sum_to_n is a function that sums numbers from 1 to n."""
```

It gives the examples `30 -> 465`, `100 -> 5050`, `5 -> 15`, `10 -> 55`,
and `1 -> 1`. The trusted canonical entry point executes
`sum(range(n + 1))`. Thus it returns the triangular number for nonnegative
integers and the empty-sum value `0` for negative integers.

The submitted implementation is:

```python
def sum_to_n(n: int):
    return n * (n + 1) // 2
```

This is equivalent to the canonical implementation for every `n >= -1`, but
not for all Python integers: for example, it returns `1` at `n=-2` and `3` at
`n=-3`, while the canonical implementation returns `0`.

### Trusted translation reconstruction

From `/tmp/audit-work/fresh`, the exact command was:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
sha256sum solution.mpy solution.regenerated.mpy
cmp -- solution.mpy solution.regenerated.mpy
```

It exited `0`; both files have SHA-256
`e1450114979c8fb27a984a4763e80a16edf6c7d6e3bca86d3246d11bc0552c13`.
See
[`stage2-translation-identity.log`](evidence/stage2-translation-identity.log).
The submitted `.mpy` artifact is therefore exactly the trusted translator's
output for the submitted Python.

### Independent differential execution

The independent oracle runner is
[`differential_test.py`](evidence/differential_test.py), with all fixed and
generated inputs preserved in
[`differential-inputs.json`](evidence/differential-inputs.json). It loads the
trusted canonical and candidate entry points from separate file modules and
does not reuse K equations. The exact command was:

```text
python3 /audit-output/evidence/differential_test.py \
  /tmp/audit-work/fresh/canonical.py \
  /tmp/audit-work/fresh/solution.py \
  /audit-output/evidence/differential-inputs.json
```

The run covered all five documented examples, the empty/range boundary around
`-1/0`, neighboring values, ten representative inputs, and 32 deterministic
generated nonnegative integers. It performed 53 comparisons:

- 50 nonnegative comparisons, with zero mismatches;
- `n=-1`, which also matched at `0`;
- `n=-2`, canonical `0` versus candidate `1`;
- `n=-3`, canonical `0` versus candidate `3`.

The script deliberately exited `1` because those two mismatches are retained
in [`stage2-differential.log`](evidence/stage2-differential.log).

The candidate is branchless. The canonical implementation's material range
boundary is the transition from an empty `range(n + 1)` to a nonempty one, and
the audit exercised both sides.

**Stage 2 result:** The artifact is faithfully translated, and it agrees with
the canonical program throughout the formal proof domain `n >= 0`. It does not
agree throughout the prompt's unqualified `int` domain. Because the prompt
states no nonnegative precondition, this is a real implementation/intent and
specification-domain limitation, not a claim of proof unsoundness by itself.

## 3. Clean proof reconstruction

The audit compiled two independent definitions from source. The exact core
commands were:

```text
kompile --backend llvm semantic.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled-audit

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

Both exited `0`; see
[`stage3-build-concrete.log`](evidence/stage3-build-concrete.log) and
[`stage3-build-proof.log`](evidence/stage3-build-proof.log).

`spec.k` contains one entry claim and no helper or loop claims. The independent
positive proof command was:

```text
kprove spec.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC
```

It exited `0` and printed exactly `#Top`, recorded in
[`stage3-positive-proof.log`](evidence/stage3-positive-proof.log).

For the required generated-semantics execution check, the reviewer-authored
[`concrete_semantics_compare.py`](evidence/concrete_semantics_compare.py) ran
the fresh LLVM definition on the ten inputs in
[`concrete-inputs.json`](evidence/concrete-inputs.json): `-3`, `-2`, `-1`,
`0`, `1`, `2`, `5`, `30`, `100`, and `1000`. Every `krun` exited `0`, and
every K result matched the submitted Python. The same two negative cases
differed from the canonical Python, exactly as in Stage 2. The complete
commands and configurations are in
[`stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).

**Stage 3 result:** PASS as a reconstruction gate. The sole positive target
claim closes under the submitted theory, and concrete generated-semantics
execution matches the generated program on all tested inputs. This says
nothing yet about whether every semantic rule is truthful.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The only entry claim says:

- Start with the exact constructor term for the submitted one-function module,
  followed by `invoke("sum_to_n", N)`, and with `<result> noResult`.
- Assume `N >=Int 0`.
- Consume the entire computation to `.K`.
- End with the result exactly `sumSpec(N)`, where `sumSpec(N)` is defined as
  `(N *Int (N +Int 1)) /Int 2`.

This is an equality-like, result-bearing reachability destination. It has no
fresh right-hand-side result variable, no omitted result cell, no tautological
`ensures`, and no one-way implication standing in for a required equivalence.

### Literal program identity and control flow

The reviewer independently extracted the balanced `Module(...)` term from
`spec.k` rather than trusting `prove.sh`. After whitespace normalization, that
term and `solution.mpy` have the same SHA-256
`229cbd6a2c39b0f1bb7b60e74f9a02a14c6bc3c06da7aa60b74300949c8dd75d`.
See
[`claim_grounding.py`](evidence/claim_grounding.py) and
[`stage4-claim-grounding.log`](evidence/stage4-claim-grounding.log).

There are no loop or auxiliary claims. The operational rule binds the module's
function name and the invoked function name with the same K variable `F`, so a
different invocation does not execute. It passes the actual parsed body `E`,
actual parameter name `P`, and actual argument `V` into `evalExpr`; it does not
replace the body by `sumSpec` or an opaque answer. The `<k>` and `<result>`
matches are exact rather than ellipsis-framed, so the rule does not silently
discard an arbitrary continuation or overwrite an existing result.

### Satisfying states and ground substitution

`N=0` is a concrete state satisfying the precondition:

```text
<k> [exact submitted Module term] ~> invoke("sum_to_n", 0) </k>
<result> noResult </result>
```

The claim predicts result `0`; both Python implementations and fresh K
execution return `0`. Additional satisfying substitutions `N=1`, `2`, `30`,
and `100` give respectively `1`, `3`, `465`, and `5050` in the claim and both
Python implementations. The grounding log records all comparisons and exits
`0`.

### Domain adequacy

The formal claim covers all nonnegative K integers. It does not cover negative
Python integers even though the prompt's type is `int` and contains no explicit
precondition. This omission matters because the generated and canonical
programs demonstrably diverge for `n <= -2`. The claim is adequate for its
stated nonnegative subset, but not for the entire typed behavior exposed by the
trusted canonical entry point.

**Stage 4 result:** Real-program pinning and result constraint pass. Intent
adequacy has a documented negative-input gap.

## 5. Exhaustive local rule and declaration review

The numbered sources, attribute search, and imported K division contract are
preserved in
[`stage5-source-inventory.log`](evidence/stage5-source-inventory.log). There
are no generated helper K files. Imported K builtin modules are an external
toolchain boundary; the inventory below exhausts every candidate-local syntax
declaration, configuration, rule, and claim.

### Declaration inventory

| Location | Local declaration | Role and assessment |
|---|---|---|
| `semantic.k:8` | `Program ::= Module(Function)` `[symbol(Module)]` | Constructor syntax used by `solution.mpy`; truthful structural representation. |
| `semantic.k:9` | `Function ::= FuncDef(String, Params(String), Statement)` `[symbol(FuncDef)]` | Represents the submitted one-name, one-parameter function. Minimal but sufficient. |
| `semantic.k:10` | `Statement ::= Return(Expr)` `[symbol(Return)]` | The only submitted statement. It intentionally omits unused statements. |
| `semantic.k:12` | `Expr ::= Int(Int)` `[symbol(IntLiteral)]` | Submitted literal constructor. |
| `semantic.k:13` | `Expr ::= Name(String)` `[symbol(Name)]` | Submitted local-name constructor. |
| `semantic.k:14` | `Expr ::= BinOp(String, Expr, Expr)` `[symbol(BinOp)]` | Submitted binary-expression constructor. Operator coverage is supplied by separate equations. |
| `semantic.k:22` | `KItem ::= invoke(String, Int)` `[symbol(invoke)]` | Entry mechanism for an integer argument. |
| `semantic.k:23` | `KItem ::= noResult` `[symbol(noResult)]` | Initial result sentinel. |
| `semantic.k:25` | `Int ::= evalExpr(Expr, String, Int)` `[function]` | Program-derived, result-bearing evaluator. It is not opaque and is defined structurally for every expression reached by the submitted program. |
| `verification.k:8` | `Int ::= sumSpec(Int)` `[function]` | Definitional mathematical summary used only in the postcondition. |
| `semantic.k:38-42` | `<mpy><k>...invoke...</k><result>...</result></mpy>` | Complete state for this pure, single-call subset. No heap, store, stack, allocation, I/O, or exception cell is needed by the submitted program. |
| `spec.k:6-18` | One reachability claim | Exact submitted program, `N >= 0`, exact final result. Reviewed in Stage 4. |

There are **no candidate-local** `[total]`, `[functional]`, `[simplification]`,
`[priority]`, `[owise]`, `[concrete]`, `[hook]`, macro, opaque-symbol,
priority-rule, simplification-rule, or auxiliary-claim declarations. The
`[symbol(...)]` attributes name constructors; they do not add equations or
oracles.

### Rule inventory

| Rule | Complete local rule domain and effect | Assessment |
|---|---|---|
| `semantic.k:29` | `evalExpr(Int(I), _P, _V) => I` | Correct for Python integer literals. Ignoring the binding is correct. |
| `semantic.k:30` | `evalExpr(Name(P), P, V) => V` | Correct for the sole local parameter. Repeated `P` enforces exact string equality. An unbound different name has no fabricated value. |
| `semantic.k:31-32` | `evalExpr(BinOp("+", L, R), P, V) => evalExpr(L,P,V) +Int evalExpr(R,P,V)` | Correct for the pure submitted expression. K and Python use unbounded integers here. |
| `semantic.k:33-34` | Analogous `*` equation using `*Int` | Correct for the pure submitted expression and unbounded integer multiplication. |
| `semantic.k:35-36` | Analogous `"//"` equation using `/Int` | **Unsound over its declared domain.** Python `//` rounds down; K `/Int` rounds toward zero. Concrete and proved false witness below. |
| `semantic.k:44-45` | Exact module/function/return plus matching invocation rewrites to `.K` and `evalExpr(E,P,V)` | Correct as a big-step rule for the declared single-function/single-return subset. It executes the actual body and preserves exact call binding, control, and result state. |
| `verification.k:9` | `sumSpec(N) => (N *Int (N +Int 1)) /Int 2` for every K integer | A terminating, fully covered definitional summary. It does not replace execution. On the target `N >= 0` domain its divisor is nonzero and its value is the submitted formula. |

### Construct-to-rule coverage

The submitted term uses `Module`, `FuncDef`, `Params`, `Return`, `BinOp`,
`Name`, `Int`, strings, and the labels `"//"`, `"*"`, and `"+"`. The structural
constructors map to the declarations above; the exact module rule exposes the
actual returned expression; `Name("n")` is connected to `Params("n")` and the
invoked integer argument; the three used operator labels each have an equation.
Built-in strings and mathematical integers come from `STRING` and `INT`.
Nothing in `solution.mpy` reaches an undeclared or unruled construct.

The `evalExpr` equations have structurally disjoint top constructors, and the
three `BinOp` equations have disjoint string labels. Recursive calls descend
strictly into `L` and `R`. `evalExpr` is not declared total; unsupported
operators and unbound names therefore need not be assigned an invented result.
The actual expression is pure and total for `N >= 0`, so any evaluator argument
order is observationally immaterial here. The configuration has no mutable
state or allocation to preserve.

Probes confirm that an unsupported `"-"` operator and an unbound name do not
fabricate results, while a mismatched function invocation leaves the exact
configuration unexecuted. Division by zero aborts the LLVM hook rather than
modeling a Python exception; the submitted body always divides by literal `2`,
so that unused behavior is not treated as a separate target-program defect.
These outputs are in
[`stage5-semantic-probes.log`](evidence/stage5-semantic-probes.log).

### Concrete false-conclusion witness for the floor-division rule

The imported K documentation explicitly states that `/Int` implements
t-division and rounds toward zero. Python floor division rounds toward negative
infinity. The reviewer program
[`negative-dividend.mpy`](evidence/semantic-probes/negative-dividend.mpy)
corresponds to:

```python
def probe(n):
    return -3 // 2
```

It is accepted by the candidate's declared syntax and uses the same `"//"`
rule. Invoking it with integer argument `0` uses a value satisfying the target
claim's `N >= 0` input domain. Fresh `krun` returns `-1` with exit `0`; Python
returns `-2`. The companion `3 // -2` probe likewise returns K `-1` versus
Python `-2`.

More strongly, the reviewer claim
[`spec-floor-unsound.k`](evidence/spec-floor-unsound.k) states that the first
probe returns `-1`. The exact command was:

```text
python3 -c 'print("PYTHON_REFERENCE=-3 // 2 =", -3 // 2)'
kprove spec-floor-unsound.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-FLOOR-UNSOUND
```

Python printed `-2`; `kprove` exited `0` with `#Top`. Source hashes prove that
the preserved reviewer claim is identical to the executed scratch copy. See
[`stage5-floor-rule-false-proof.log`](evidence/stage5-floor-rule-false-proof.log).
This is the required concrete false conclusion enabled by the rule; it is not
an inference from a timeout or a missing rule.

For the submitted target claim specifically, `N >= 0` implies
`N * (N + 1) >= 0`, and the divisor is positive `2`, so truncation and floor
division coincide along that exact execution path. Thus the audit does **not**
claim that the clean target instance returns a wrong result. The failure is
that the candidate installed an unguarded, globally false language equation
which can prove a false Python claim. Under the proof-extension soundness
contract, a globally false equation cannot be excused solely because its bad
instances are absent from one target path; it must be narrowed or implemented
truthfully.

`sumSpec` is not an opaque oracle: its sole equation fixes its value, and the
program body is independently evaluated. There is no rule that rewrites an
invocation directly to `sumSpec`, no circular fresh symbol shared between
execution and postcondition, and no proof-local lemma or simplification
smuggling the requested answer.

**Stage 5 result:** FAIL. The floor-division equation is materially unsound as
a semantic rule and has a machine-checked false-conclusion witness.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate negative test was
trusted. The reviewer-authored
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) keeps the exact program
and precondition but changes the result obligation from `sumSpec(N)` to the
false `sumSpec(N) +Int 1`. At satisfying witness `N=0`, it demands `1` although
the program returns `0`.

The build-only command was:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
```

It exited `0`, demonstrating that the mutation parses and builds. Source
hashes in
[`stage6-vacuity-build.log`](evidence/stage6-vacuity-build.log) show that the
preserved mutation is byte-identical to the scratch artifact.

The actual mutation proof command omitted `--dry-run`. It exited `1` and
reported `WarnStuckClaimState`, with an implication failure requiring:

```text
N *Int (N +Int 1) /Int 2 +Int 1
#Equals
N *Int (N +Int 1) /Int 2
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. The residual is preserved in
[`stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log).

**Stage 6 result:** PASS. The positive target claim is non-vacuous and
discriminates a false result.

## 7. Proven versus assumed accounting and decision

### What the successful reachability proof establishes

Under the candidate's submitted K theory, for every mathematical K integer
`N >= 0`, the literal constructor term in `solution.mpy`, followed by
`invoke("sum_to_n", N)` and an empty result cell, rewrites to an empty
computation whose result is:

```text
(N *Int (N +Int 1)) /Int 2
```

The theorem is partial correctness: if the modeled execution reaches the
destination, that result is fixed. In this case the local structural equations
also concretely terminate on the target term, but `kprove` is still a
reachability proof under the supplied theory, not a proof that the theory is a
faithful Python semantics.

It does **not** formally establish:

- that every local semantic equation implements Python;
- behavior for negative inputs excluded by `N >= 0`;
- the canonical implementation's empty-range behavior for negative inputs;
- a K theorem that the triangular closed form equals an independently modeled
  iteration or `sum(range(n + 1))`;
- Python exceptions or arbitrary translated programs.

### Trust and assumption ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K parser, Haskell/LLVM backends, reachability engine, and K builtin `INT`/`STRING` modules | All builds, runs, and proofs | Ordinary external toolchain trust boundary. Version and commands are reproducible. |
| Trusted mounted `py2mpy.py` | Source-to-`.mpy` identity | Byte identity is established for this artifact. The audit does not claim a universal translator correctness theorem. |
| `+Int` and `*Int` over unbounded K integers | `evalExpr`, `sumSpec`, target proof | Acceptable primitive bridge for Python integer addition/multiplication in this pure program. |
| `/Int` | `"//"` evaluator rule, `sumSpec`, target proof | K primitive itself is well-defined as truncating division. The candidate's unconditional identification with Python floor division is illegitimate and directly enables the false proof in Stage 5. Its specific target use is value-safe only because the dividend is nonnegative and divisor is `2`. |
| `evalExpr` | Concrete execution and entry claim | Program-derived but not opaque: structural equations expose the actual body. No oracle is assumed. One constituent equation is nevertheless globally false. |
| `sumSpec` | Entry postcondition | Fully defined summary, not an execution bridge. Its equality to the submitted closed-form body is reduced by K. |
| Triangular-number identity as the meaning of “sum numbers from 1 to n” | Human-facing intent | Ordinary mathematical argument plus finite differential evidence, not a separate K theorem. |
| Differential and concrete tests | Python/K and candidate/canonical bridges on tested cases | Finite evidence only. Fifty nonnegative differential cases and ten K/candidate cases passed; two negative canonical divergences remain visible. |

There are no local opaque values, uninterpreted result oracles, empirical
primitives, priority assumptions, simplification lemmas, or auxiliary
reachability claims.

### Gate summary

- **Real-program soundness (Gate A): FAIL.** Program identity, body
  sensitivity, result constraint, and fresh non-vacuity pass, but the
  unconditional floor-division equation is false and makes a concrete false
  Python claim provable with `#Top`.
- **Intent adequacy (Gate B): FAIL / limited independently of Gate A.** The
  theorem covers the nonnegative subset and agrees with the canonical there,
  but the prompt has no stated nonnegative precondition, and the generated
  implementation differs from the trusted canonical on negative integers.
  The summary-to-natural-language bridge is also mathematical/informal rather
  than an independently modeled K summation theorem.
- **Auditability (Gate C): PASS for this audit record.** Source artifacts,
  inputs, scripts, exact commands, statuses, bounded outputs, positive proof,
  false semantic witness, and non-vacuity residual are preserved. Finite tests
  are not presented as universal proof.

The clean `#Top` and successful non-vacuity mutation show that this is a real,
result-constraining proof under the submitted theory. They cannot legitimize a
theory containing a witnessed false semantic equation. Because Gate A fails,
the candidate does not contain a legitimate partial-correctness proof of the
real generated Python program under a sound generated semantics.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
