# Independent adversarial audit: 103-rounded-avg

## Outcome

This is a legitimate, result-constraining partial-correctness proof of the
currently submitted function body under the supplied MPY semantics, but it does
not merit an unqualified pass.

The proof was rebuilt from source and all four positive claims independently
closed with exit status 0 and `#Top`. The only candidate-local K definitions are
transparent constructors for the exact submitted body and its direct call; they
do not summarize the result, bypass execution, or introduce an opaque oracle.
A false-result mutation and a body-sensitivity mutation were both rejected for
the expected semantic reason.

There are three documented limitations:

1. The literal positive-integer domain is unbounded, and the candidate differs
   from the trusted canonical Python implementation at values above the
   binary64 exact-integer boundary. For `n = m = 2**53 + 1`, the canonical
   implementation returns `bin(2**53)` after its float conversion, while the
   candidate returns `bin(2**53 + 1)`.
2. The direct-call harness contains a manually audited exact copy of the MPY
   body, rather than mechanically importing or hashing `solution.mpy`.
   Consequently, changing `solution.py`/`solution.mpy` alone does not invalidate
   the proof build. This is an artifact-drift risk, not a false theorem about
   the current body.
3. The requested generation-provenance files are absent.

These limitations warrant `CONCERNS / LEGIT`. They do not enable a false K
conclusion about the current generated body.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory exists as a real directory, so
there is no mode/mount contradiction and no infrastructure breach. The live
toolchain is K v7.1.337; see
[00-toolchain.log](evidence/00-toolchain.log).

The recursive candidate-versus-trusted semantics check compared relative entry
names, entry types, link targets, and every regular file byte-for-byte:

- entry/type/link diff exit: 0;
- every semantics file comparison exit: 0;
- no missing, additional, mistyped, changed, or symlinked semantics entry.

The candidate `prompt.py` and `py2mpy.py` are also byte-identical to their
trusted mounted versions. Hashes and all comparisons are in
[01-integrity.log](evidence/01-integrity.log). The complete candidate file/type
and hash manifest is [22-candidate-manifest.log](evidence/22-candidate-manifest.log).

### Missing and auxiliary artifacts

The following requested provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any structured generation trace

There is no candidate `PROOF.md` or `spec-vacuity.k` to rely on. The candidate
does include `prove.sh`, runtime test sources, and two `__pycache__` files.
Those auxiliary and compiled-Python artifacts were treated as untrusted and
were not used as proof evidence. No candidate-built K definition or K cache was
present or copied.

The proof-relevant regular sources (`solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, and the supplied semantics tree) are present. The scratch
copy manifest is [02-scratch-copy.log](evidence/02-scratch-copy.log).

**Stage result:** semantics, prompt, translator, and proof-source integrity pass;
generation provenance is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For positive integers `n` and `m`:

- if `n > m`, return integer `-1`;
- otherwise take the inclusive arithmetic sequence from `n` through `m`,
  round its average to the nearest integer using the canonical Python
  half-even behavior, and return that integer's `bin(...)` string.

The canonical implementation sums the inclusive range and evaluates
`round(summation / count)`. The candidate uses the arithmetic-sequence identity
that the exact average is `(n + m) / 2`, then performs half-even rounding using
integer quotient and parity:

- even `n + m`: return the integral midpoint;
- odd `n + m`: retain an even lower neighbor and increment an odd lower
  neighbor.

This is a correct constant-time implementation of the exact mathematical
contract for positive integers.

### Trusted translation

Running the trusted translator afresh produced a file byte-identical to the
submitted `solution.mpy`. Both hashes are
`a943f545c83667a196c79bca2f373ac2e233d3835eee3a3c67c19652c1e0f6e8`;
translator and comparison exits were both 0. See
[03-translation-fidelity.log](evidence/03-translation-fidelity.log).

### Independent differential reconstruction

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and candidate entry point independently. Its exact inputs
and results are preserved in
[differential-inputs.jsonl](evidence/differential-inputs.jsonl) and
[differential-results.jsonl](evidence/differential-results.jsonl).

The 15,018 cases comprise:

- all four documented examples;
- the minimal equal interval and an inverted/empty interval;
- all parity/rounding branch boundaries;
- every pair in the positive square `1..100 × 1..100`;
- 5,000 deterministic generated cases with bounded interval width;
- six cases around `2**53`;
- one explicitly marked zero-boundary case outside the positive contract.

There were zero mismatches in the documented, small exhaustive, generated, or
ordinary boundary sets. There were two mismatches at the binary64 boundary:

- `(9007199254740993, 9007199254740993)`: canonical rounds after float
  conversion to `9007199254740992`; candidate returns `9007199254740993`.
- `(9007199254740995, 9007199254740995)`: canonical returns
  `9007199254740996`; candidate returns `9007199254740995`.

The script deliberately exited 1 to keep those divergences visible; see
[04-differential.log](evidence/04-differential.log). This is material on the
literal unbounded positive-integer domain. It is an implementation-to-canonical
limitation, while the candidate remains aligned with the exact mathematical
wording of the prompt.

**Stage result:** source-to-MPY fidelity passes; ordinary-domain equivalence is
strongly supported, but universal canonical equivalence is false.

## 3. Clean proof reconstruction

All work occurred below `/tmp/audit-work`. Candidate caches and compiled
definitions were not reused.

### Concrete definition

The supplied semantics was freshly compiled with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

The build exited 0
([05-kompile-concrete.log](evidence/05-kompile-concrete.log)). Fresh execution
of the translated runtime assertion program exited 0 and reached `.K`,
`NoExc`, and exit code 0
([06-krun-runtime-tests.log](evidence/06-krun-runtime-tests.log)).

The LLVM build reported fixed-semantics non-exhaustiveness warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is on
the submitted program's execution path. These are recorded as fixed-semantics
coverage limitations, not silently treated as candidate rules.

### Proof definition and positive claims

The proof definition was freshly compiled with:

```text
kompile verification.k --backend haskell \
  --main-module ROUNDED-AVG-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

This exited 0; the only warnings were unused pattern variables in the supplied
`str.k` ([07-kompile-proof.log](evidence/07-kompile-proof.log)).

The unmodified four-claim module exited 0 and printed `#Top`
([08-kprove-all.log](evidence/08-kprove-all.log)). To ensure that aggregate
success did not mask a claim, I placed each unchanged claim in a separate
reviewer module and ran it independently:

| Claim | Preserved spec | Evidence | Exit/result |
|---|---|---|---|
| inverted interval | [spec-inverted.k](evidence/spec-inverted.k) | [09-kprove-inverted.log](evidence/09-kprove-inverted.log) | 0, `#Top` |
| integral midpoint | [spec-integral.k](evidence/spec-integral.k) | [10-kprove-integral.log](evidence/10-kprove-integral.log) | 0, `#Top` |
| half-even down | [spec-half-even-down.k](evidence/spec-half-even-down.k) | [11-kprove-half-even-down.log](evidence/11-kprove-half-even-down.log) | 0, `#Top` |
| half-even up | [spec-half-even-up.k](evidence/spec-half-even-up.k) | [12-kprove-half-even-up.log](evidence/12-kprove-half-even-up.log) | 0, `#Top` |

Each log records the exact command, work directory, output, and exit status.

**Stage result:** clean dynamic reconstruction passes for every positive
target.

## 4. Adequacy and real-program pinning

### Claim meaning, coverage, and witnesses

All claims require positive `N` and `M`. Their disjoint cases exhaust that
domain:

| Branch | Plain-language precondition | Exact postcondition | Witness |
|---|---|---|---|
| inverted | `N > M` | return integer `-1` | `(2,1)` |
| integral | `N <= M` and `N+M` even | return `"0b" + binary((N+M)/2)` | `(1,3)` |
| half-even down | `N <= M`, sum odd, lower midpoint even | return the lower even midpoint in binary | `(2,3)` |
| half-even up | `N <= M`, sum odd, lower midpoint odd | return lower midpoint plus one in binary | `(3,4)` |

The `<k>` destination is an exact value, not a free variable, implication-only
condition, or tautology. The unchanged cells require the call frame to be
popped and the caller environment, scopes, heap, stack, return state, and
exception state restored.

[ground_witnesses.py](evidence/ground_witnesses.py) substitutes the four
satisfying states and compares each formal branch result with both Python
implementations. All four agree; see
[18-ground-witnesses.log](evidence/18-ground-witnesses.log).

### Current-program connection

`roundedAvgBody` is a transparent nullary `[function, total]` definition whose
right-hand side is the submitted MPY function body. After normalizing explicit
empty `.Stmts` terminators, its statements, names, operators, branch nesting,
and final call match `solution.mpy` exactly.

`roundedAvgCall(N,M)` is also transparent. It produces a fixed-semantics call
of:

```text
closureVal(("n", "m", .ParamNames), roundedAvgBody, 0)
```

with arguments `(N,M)`. The supplied module-load and `FuncDef` rules install
that same closure body, parameter list, and defining environment 0. The actual
module scope additionally contains the name `rounded_avg`; the submitted body
never reads that name, so its absence from the direct harness cannot affect
binding, control, state, or result. `bin` resolves through the unchanged parent
builtin scope. There is no loop or loop-summary claim.

The direct harness therefore executes the actual current body under the fixed
rules for parameter binding, statements, returns, and frame popping. It is not
an operational bridge to an answer formula.

Two sensitivity experiments distinguish semantic pinning from mechanical file
coupling:

- Replacing the executed `roundedAvgBody` with `Return(Int(777))`, recompiling,
  and rerunning the original claims produced a real stuck claim at result
  `777`, exit 1. The mutation and logs are
  [body-sensitivity-verification.k](evidence/body-sensitivity-verification.k),
  [27-body-sensitivity-kompile.log](evidence/27-body-sensitivity-kompile.log),
  and [28-body-sensitivity-kprove.log](evidence/28-body-sensitivity-kprove.log).
  This shows the proof is body-sensitive and does not bypass execution.
- Replacing only `solution.py`, regenerating `solution.mpy` as
  `Return(Int(777))`, but leaving `verification.k` unchanged still allowed a
  fresh rebuild and `#Top`. See
  [pinning-mutated-solution.py](evidence/pinning-mutated-solution.py),
  [pinning-mutated-solution.mpy](evidence/pinning-mutated-solution.mpy),
  [16-pinning-mutation-kompile.log](evidence/16-pinning-mutation-kompile.log),
  and [17-pinning-mutation-kprove.log](evidence/17-pinning-mutation-kprove.log).
  This demonstrates the lack of an automatic source hash/import dependency.

The second experiment is a real auditability concern: future source drift would
require repeating the manual body comparison. It does not make the theorem
about the current, independently matched body false.

**Stage result:** the formal claims are satisfiable, exhaustive, and
result-constraining; the current function body is semantically pinned through a
transparent direct-entry harness, with a documented manual-coupling risk.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[k_inventory.py](evidence/k_inventory.py) reconstructed every local
configuration, context, syntax declaration, semantic rule, proof-local rule,
and target claim. The final line-addressable inventory is
[k-rule-inventory.tsv](evidence/k-rule-inventory.tsv), with summary
[k-rule-inventory-summary.txt](evidence/k-rule-inventory-summary.txt).

The 936 inventoried entries are:

- supplied semantics: 1 configuration, 5 contexts, 227 syntax declarations,
  and 695 rules;
- candidate verification: 2 syntax/function declarations and 2 defining
  rules;
- candidate specification: 4 reachability claims.

Attribute inventory found 147 function declarations, 109 total declarations,
35 concrete entries, 45 priority entries, 26 `owise` entries, 22
`no-evaluators` entries, and 25 named `symbol(...)` entries. There are no
`functional` or `simplification` entries. The full logical declaration and
per-entry assessment are in the TSV; the focused opaque/priority/candidate view
is recorded in [31-inventory-focus-refresh.log](evidence/31-inventory-focus-refresh.log).

Because this is supplied-semantics mode and the tree is byte-identical to the
trusted baseline, all 928 fixed-semantics entries are classified as the
selected semantics rather than as candidate proof extensions. This does not
extend that trust to `verification.k`.

### Candidate-local extensions

1. **`roundedAvgBody` declaration and rule.** This is a definitional AST alias.
   Its single unguarded rule completely covers the nullary symbol. It names no
   result formula and does not rewrite any fixed operational redex to an
   answer. After expansion, every submitted statement executes under the
   supplied semantics. There is no overlap, recursion, opacity, priority, or
   totality gap.
2. **`roundedAvgCall` declaration and rule.** This is a direct-entry
   constructor. Its single unguarded rule covers all two-`Int` applications and
   creates the exact closure call. It writes no cell, fabricates no return
   value, and does not preempt a fixed rule. Binding, argument order, closure
   environment, continuation, and frame behavior are supplied by the ordinary
   call rules.

Both extensions are locally sound. Their current-source connection is the
manual structural check discussed in Stage 4.

### Used operational path

[used-construct-map.md](evidence/used-construct-map.md) maps every submitted
AST construct to its declaration and operational rules. The relevant path is:

- module/function syntax and the direct-entry closure connection;
- left-to-right parameter and argument binding;
- statement sequencing;
- integer literals and name lookup;
- strict/sequence-strict unary, binary, and comparison evaluation;
- ordinary local assignment;
- `If` truth and branch selection;
- `Return`, frame pop, and restoration;
- builtin `bin` dispatch and `binCodes`/`binAcc`.

For satisfying states:

- both parameters are K mathematical integers;
- all `//` and `%` divisors are the positive constant 2;
- local assignments use the ordinary non-cell frame rule;
- the only external name is `bin`, selected from the fixed builtins scope;
- the average is positive, so only the non-negative `bin` rule is reachable;
- there is no heap allocation, list aliasing, exception, loop, output, or
  user-defined callback.

The integer `+`, `//`, `%`, `>`, and `==` rules implement the operations used by
the source. `binCodes` and `binAcc` recursively encode non-negative integers and
strictly decrease their positive argument. Rule guards on this path are
disjoint or agree; evaluation order and return control match the submitted
program.

### Opaque and unused boundaries

The fixed tree contains opaque float operations, `sortVS`, `sortKeyVS`, and
`md5hexCodes`. None is reachable from the submitted body or appears in a
postcondition. The concrete-only keyed sort and deep list equality rules are
also absent from the proof module. The LLVM non-exhaustiveness warnings concern
unused fixed functions and do not affect a branch, result, state, exception, or
termination assumption here.

No candidate-local ordinary rule, priority rule, simplification, opaque symbol,
or oracle encodes the requested answer. I found no unsound inventoried rule on
the proof path and therefore make no unsupported unsoundness allegation. The
source-only coupling experiment is an evidence-and-pinning limitation, not a false
rule witness.

**Stage result:** static soundness passes for the candidate extensions and the
used fixed-semantics path.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity test. I created
[spec-vacuity.k](evidence/spec-vacuity.k), changing the integral branch result
from `bin((N+M)/2)` to the demonstrably false
`bin((N+M)/2 + 1)`. The original precondition is retained; `(N,M)=(1,3)`
satisfies it and both Python implementations return `"0b10"`, not `"0b11"`.

The mutated module successfully parsed and compiled to KORE with exit 0
([19-vacuity-dry-run.log](evidence/19-vacuity-dry-run.log)). Its real proof run
exited 1 with `WarnStuckClaimState`; the residual shows the unmet equality
between the executed binary result and the off-by-one `binAcc` term, followed
by the expected “configuration cannot be rewritten further” error. See
[20-vacuity-kprove.log](evidence/20-vacuity-kprove.log).

This is a reachable, result-bearing failure, not a parser error, missing import,
timeout, or unrelated crash.

**Stage result:** non-vacuity passes.

## 7. Proven versus assumed accounting

### What is formally established

Conditional on the supplied MPY semantics, each successful reachability claim
establishes partial correctness of the direct invocation of the exact current
body:

- for every positive inverted pair, termination yields `-1`;
- for every positive non-inverted pair, termination yields the fixed
  K-string/binary formula for the appropriate integral, half-even-down, or
  half-even-up branch;
- the call restores the specified caller cells and does not leave an exception.

This is partial correctness. The claims do not themselves establish termination,
although this straight-line program and the decreasing positive `binAcc`
computation are operationally terminating on the stated domain.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.337 compiler, Haskell backend, and builtin integer/Boolean/map/list hooks | all builds and proofs | Ordinary machine-checking trust boundary; versions and outputs preserved. |
| Byte-identical supplied MPY semantics | all claims | Authorized fixed-semantics boundary in this mode. Candidate did not modify it. |
| Trusted `py2mpy.py` translation | source-to-MPY identity | Machine-run byte comparison passes; this does not connect `solution.mpy` mechanically to the proof helper. |
| Manual current-body/direct-entry connection | theorem-to-submitted entry point | Exact AST/parameter/environment inspection plus body-sensitivity evidence. Acceptable for the current artifact, but vulnerable to future drift. |
| Fixed `bin`/`binCodes` model | all valid-interval postconditions | Defined in the supplied semantics and tested on ground cases. Universal equivalence to CPython `bin` is a semantics trust, not separately proved here. |
| Arithmetic-sequence midpoint and half-even interpretation | bridge from branch formulas to prompt wording | Ordinary informal mathematics, supported by the branch witnesses and differential run. |
| Canonical equivalence | implementation-to-reference bridge | Finite evidence only, and universally false on the literal unbounded positive domain because canonical code converts through binary64. |
| Opaque float/sort/MD5 symbols and concrete-only rules | none | Unreachable and result-independent; they contribute no assumption to claim closure. |
| Missing generation metadata | provenance only | Reduces traceability but does not change the reconstructed K theorem. |

Differential tests, concrete assertions, and prose are not treated as substitutes
for the K proof. They support only translation, current-body adequacy, ground
interpretation, and the documented canonical limitation.

### Final gate assessment

- Clean verification: **pass**.
- Candidate proof-extension soundness: **pass**.
- Current-body execution and result constraint: **pass**, with manual
  source-coupling concern.
- Non-vacuity: **pass**.
- Natural-language/canonical adequacy: **concern** because of the unbounded
  binary64 divergence.
- Evidence/provenance auditability: **concern** because generation metadata is
  missing.

The reconstructed proof is sound and discriminating for the real current
generated body. The canonical-domain discrepancy, manual artifact coupling,
and missing provenance prevent `PASS`, but none makes a false result provable
under the claimed preconditions.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
