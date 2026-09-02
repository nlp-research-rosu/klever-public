# Adversarial proof audit: 71-triangle-area

## Audit outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted MPY program under the supplied K semantics. It does not introduce
an execution bridge or result oracle: fixed semantics executes the exact
function body, and the valid result is constrained to the exact structural
composition of the supplied float primitives.

The result is `CONCERNS / LEGIT`, rather than `PASS`, because the theorem is
integer-only and the numerical meaning of `divII`, `intToF`, `subF`, `mulF`,
`powF`, and `roundFN` remains a supplied opaque trust boundary during
`kprove`. The proof therefore does not itself establish a universal
Python-level theorem about Heron's formula, floating-point rounding, exceptional
large integers, or repeated calls in one loaded module. The missing generation
provenance files also reduce auditability. None of these limitations is a
candidate-created shortcut that can prove an incorrect result term.

The audit used K 7.1.337. All execution, mutation, and build work occurred in
`/tmp/audit-work`; `/candidate` was treated as read-only. Reviewer scripts and
bounded logs are in [`evidence/`](evidence/).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. This is consistent, so there is no
infrastructure breach.

The recursive command

```text
diff --no-dereference -rq /candidate/reference-semantics /reference/reference-semantics
```

exited 0. There are no missing, additional, changed, mistyped, or symlinked
entries in the candidate semantics tree. Candidate `prompt.py` and `py2mpy.py`
are byte-identical to their trusted counterparts (`cmp` exit 0 for each).
No symlink exists anywhere under `/candidate`. Exact commands and statuses are
in [`01_integrity.log`](evidence/01_integrity.log), and candidate file types and
hashes are in [`01_candidate_manifest.log`](evidence/01_candidate_manifest.log).

The candidate also contains ancillary `prove.sh`, `smoke.mpy`, a regular
`__pycache__` directory, and a `.pyc`. These are additional evidence, not
trusted inputs. No candidate-built K definition was present or reused; the
Python cache was neither copied nor executed.

### Missing provenance evidence

The following requested untrusted provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace (`*trace*` or `*.jsonl`) is present. Therefore
there were no generation claims in those files to inspect. This omission is an
auditability concern, but the executable source needed to reconstruct and
validate the proof is present.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt and canonical implementation specify a three-argument
function `triangle_area(a,b,c)`. If any pair sum is less than or equal to the
remaining side, it returns `-1`. Otherwise it computes

```text
s = (a+b+c)/2
sqrt(s(s-a)(s-b)(s-c))
```

and returns that area rounded to two decimal places. The documented examples
are `(3,4,5) -> 6.00` and `(1,2,10) -> -1`.

The submitted `solution.py` uses exactly that branch order and expression. Its
only material source-level difference from `canonical.py` is returning the
rounded expression directly instead of first storing it in `area`.

### Trusted retranslation

The trusted translator was run against the scratch copy:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
```

Both translation and comparison exited 0, establishing byte identity with the
submitted `solution.mpy`; see
[`02_translation.log`](evidence/02_translation.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry and submitted Python entry. It covers:

- both documented examples;
- the zero-length boundary (there is no collection-valued “empty” input for
  this fixed-arity function);
- equality and adjacent-valid cases for each of the three short-circuit
  branches;
- signed, negative, large, and equilateral cases;
- ordinary float and near-boundary float cases;
- the complete integer cube `[-8,20]^3`;
- 10,000 deterministic random nonnegative integer triples;
- an `8^3` half-step float grid; and
- an equilateral `10^400` case that makes both Python implementations raise the
  same `OverflowError`.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py \
  /tmp/audit-work/trusted/canonical.py \
  /tmp/audit-work/candidate-src/solution.py
```

It exited 0 with 34,918 cases and zero mismatches. Full named results and scope
are in [`02_differential.log`](evidence/02_differential.log). This is finite
program-fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/candidate-src`. The
candidate Python cache and any external build state were ignored. The following
fresh commands were run.

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Concrete smoke | `krun smoke.mpy --definition runtime-kompiled` | exit 0; `.K`, `NoExc`, exit code 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module TRIANGLE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| All claims | `kprove spec.k --definition verification-kompiled --spec-module TRIANGLE-SPEC` | exit 0; `#Top` |

The corresponding logs are
[`03_kompile_runtime.log`](evidence/03_kompile_runtime.log),
[`03_smoke.log`](evidence/03_smoke.log),
[`03_kompile_verification.log`](evidence/03_kompile_verification.log), and
[`03_kprove_all.log`](evidence/03_kprove_all.log).

The LLVM compile reported supplied-semantics coverage warnings for functions
such as `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`.
None occurs on this program's execution slice. The Haskell build and proofs
reported only unused-variable warnings in `str.k`.

To avoid relying on one aggregate `#Top`, I made a scratch labeled copy of the
spec. Normalizing away only the inserted labels and module-name change gives
byte identity with `spec.k`; the `diff` exited 0 in
[`03_labeled_spec_identity.log`](evidence/03_labeled_spec_identity.log).
Each of the five positive claims was then selected independently:

| Claim | Selection | Evidence |
|---|---|---|
| Module load | `--claims TRIANGLE-SPEC-LABELED.load-module` | exit 0, `#Top`; [`03_kprove_load-module.log`](evidence/03_kprove_load-module.log) |
| First invalid branch | `--claims TRIANGLE-SPEC-LABELED.invalid-first` | exit 0, `#Top`; [`03_kprove_invalid-first.log`](evidence/03_kprove_invalid-first.log) |
| Second invalid branch | `--claims TRIANGLE-SPEC-LABELED.invalid-second` | exit 0, `#Top`; [`03_kprove_invalid-second.log`](evidence/03_kprove_invalid-second.log) |
| Third invalid branch | `--claims TRIANGLE-SPEC-LABELED.invalid-third` | exit 0, `#Top`; [`03_kprove_invalid-third.log`](evidence/03_kprove_invalid-third.log) |
| Valid branch | `--claims TRIANGLE-SPEC-LABELED.valid` | exit 0, `#Top`; [`03_kprove_valid.log`](evidence/03_kprove_valid.log) |

Because this is supplied-semantics mode, no generated-semantics validation
obligation applies.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

1. With module environment 0 and an empty module map, loading
   `triangleAreaModule` installs the name `triangle_area` with exactly
   `triangleAreaClosure`.
2. For arbitrary K integers `A,B,C`, if `A+B <= C`, calling the closure returns
   `-1`.
3. If the first comparison is false and `A+C <= B`, it returns `-1`.
4. If the first two comparisons are false and `B+C <= A`, it returns `-1`.
5. If all three pair sums are strictly greater than the remaining side, it
   returns `expectedArea(A,B,C)`.

The four call preconditions partition all integer triples in the program's
left-to-right short-circuit order. Each call claim pins `env`, both scope
frames, `scopeLoc`, empty heap and heap counter, empty stack, and `noRet`.

### Satisfiable witnesses and ground results

The witnesses are:

- first invalid branch: `(1,2,3)`;
- second invalid branch: `(2,4,2)`;
- third invalid branch: `(4,2,2)`; and
- valid branch: `(3,4,5)`.

The loader's explicitly written initial cells are themselves a satisfying
state. [`claim_witnesses.py`](evidence/claim_witnesses.py) records every guard
truth value and shows both Python implementations returning the claimed ground
result. It exited 0; see
[`04_claim_witnesses.log`](evidence/04_claim_witnesses.log).

A reviewer-generated MPY program appended assertions for those witnesses plus
`(2,2,3) -> 1.98` to the unchanged submitted function, using the trusted
translator. Concrete K execution exited 0 with `.K`, `NoExc`, and exit code 0;
see [`04_krun_witnesses.log`](evidence/04_krun_witnesses.log).

### Actual-program identity

The proof does not call a same-named opaque helper. `triangleAreaClosure`
contains `triangleAreaBody`, and fixed call semantics binds its three
parameters and executes that body.

[`ast_pin_check.py`](evidence/ast_pin_check.py) extracts the candidate's body,
closure, and module equations, composes the body into the module, normalizes
only K's equivalent explicit/implicit empty `Stmts` identity, and compares the
result with submitted `solution.mpy`. Both normalized SHA-256 values are

```text
c002156c969715b87687dfcb56d767973f5b02aa4740884f55fb1c3513bd133e
```

and both `MODULE_AST_MATCH` and `CLOSURE_SHAPE_MATCH` are true in
[`04_ast_pin.log`](evidence/04_ast_pin.log). Combined with the byte-identical
trusted retranslation and successful loader claim, this pins the closure to the
real submitted program.

The direct call claims start with an empty module map rather than the
post-loader map containing `triangle_area`. That extra global binding is not
read by this body: it uses only the three parameters, local `s`, and builtin
`round`. Thus the difference does not change this execution, although the spec
does not provide a general composition theorem for arbitrary global-sensitive
functions.

### Result constraint

The invalid claims require the concrete result `-1`. The valid claim requires
the single term `expectedArea(A,B,C)`, whose only equation fully expands to the
same supplied primitive terms produced by execution. It contains no free result
variable, implication-only escape, or unconstrained oracle.

## 5. Rule-by-rule static soundness review

[`k_inventory.py`](evidence/k_inventory.py) inventoried the complete supplied
tree, `verification.k`, and `spec.k`. The resulting
[`05_rule_inventory.log`](evidence/05_rule_inventory.log) contains exact
line-numbered text for 1,110 K blocks:

- 232 syntax declarations;
- one configuration;
- five contexts;
- 700 rules; and
- five claims.

It also enumerates all function, `total`, opaque `symbol`,
`no-evaluators`, priority, `owise`, concrete, `functional`, and simplification
occurrences. There are no `functional` or simplification blocks. The
module-by-module decision for every fixed rule, complete used-construct map,
cell/control review, and each proof-local equation are in
[`05_static_rule_review.md`](evidence/05_static_rule_review.md).

### Fixed execution slice

The relevant fixed rules provide:

- module statement sequencing and exact function installation;
- a fresh plain closure frame, left-to-right argument evaluation, exact
  parameter binding, and frame restoration;
- strict left-to-right binary operands and comparison operands;
- head-only, left-to-right short-circuit `or`;
- ordinary mathematical integer addition/comparison;
- local assignment of `s`;
- builtin lookup and call of `round`; and
- return, continuation discard inside the function, and exact frame pop.

The program allocates no heap object and mutates no observable caller state.
Priority rules for references, cells, methods, math attributes, and collections
cannot match this execution. No unused construct rule defines a candidate
symbol or appears in the result.

### Proof-local extensions

`verification.k` adds exactly five single-equation functions:

1. `triangleAreaBody`: the exact submitted body;
2. `triangleAreaClosure`: a closure over that body and environment 0;
3. `triangleAreaModule`: the exact one-function module;
4. `semiPerimeter(A,B,C)`: `divII(A+B+C,2)`; and
5. `expectedArea(A,B,C)`: the exact structural composition of the fixed float
   primitives.

Each equation is exhaustive for its declared arguments, terminating, and has
no same-symbol overlap. None is an operational rewrite that intercepts a
program term. None is a candidate opaque symbol, priority rule, ordinary
state-changing rule, or simplification.

As an independent body-sensitivity check, I changed only the exponent in
`triangleAreaBody` from `Float(0.5)` to `Float(1.0)`. The mutated verification
definition compiled with exit 0, but the valid claim exited 1 with
`WarnStuckClaimState` on the expected unequal `powF(...,0.5)` and
`powF(...,1.0)` terms. The mutation, build, and residual are
[`05_verification-body-mutation.k`](evidence/05_verification-body-mutation.k),
[`05_body_mutation_build.log`](evidence/05_body_mutation_build.log), and
[`05_body_mutation_proof.log`](evidence/05_body_mutation_proof.log).

No candidate-local rule was found unsound, so this review makes no unsupported
unsoundness allegation and needs no false-conclusion witness against such a
rule.

### Supplied float boundary and concrete evidence

The result uses six fixed supplied symbols:

```text
divII, intToF, subF, mulF, powF, roundFN
```

They are `function,total,symbol,no-evaluators` during proof, with separate
`[concrete]` LLVM equations. The proof establishes their exact composition but
does not prove their universal Python meaning.

To test the matching fresh-entry bridge, 150 cases (the complete integer cube
`[-1,3]^3` plus 25 deterministic random nonnegative triples) were run in 150
isolated K configurations against canonical-generated expected results. All
150 passed:
[`05_k_bridge_manifest.json`](evidence/05_k_bridge_manifest.json) and
[`05_k_bridge_isolated_all.log`](evidence/05_k_bridge_isolated_all.log).

A sequential batch of the same cases exposed a supplied concrete-runtime
limitation. After 99 preceding calls, `(2,3,3)` produced `2.01`; the isolated
call produced the canonical `2.83`. The isolation and state probe are recorded
in [`05_bisect_k_bridge.log`](evidence/05_bisect_k_bridge.log),
[`05_krun_k_bridge_isolated.log`](evidence/05_krun_k_bridge_isolated.log), and
[`05_krun_k_bridge_state_probe.log`](evidence/05_krun_k_bridge_state_probe.log).
Larger sequential batches were killed with exit 137 and are retained as
resource-failure evidence, not candidate failures, in
`05_krun_k_bridge_large.log` and `05_krun_k_bridge_medium.log`.

Every target claim starts from its stated fresh entry state, so the isolated
tests match the proved configurations. Repeated calls in one loaded module are
not proved and remain an explicit semantics/evidence concern.

The `10^400` equilateral differential witness also shows that both real Python
implementations raise `OverflowError`, while the supplied symbolic `divII` is a
total opaque term. This is an exception-model/termination bridge limitation,
not a wrong returned-value proof: partial correctness does not establish
normal termination for real Python inputs outside the faithful primitive
range.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I created the independent
[`06_spec-vacuity-fresh.k`](evidence/06_spec-vacuity-fresh.k), changing the
first invalid branch's required result from `-1` to `-2`. The satisfying input
`(1,2,3)` demonstrates that this mutation is false.

The mutation parsed and built through:

```text
kprove spec-vacuity-fresh.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-SPEC-VACUITY-FRESH \
  --dry-run
```

with exit 0; see
[`06_mutation_dry_run.log`](evidence/06_mutation_dry_run.log). The actual proof
command

```text
kprove spec-vacuity-fresh.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-SPEC-VACUITY-FRESH
```

exited 1 with `WarnStuckClaimState`; the residual has `-1 ~> .K` where the
destination requires `-2`. This is the expected unmet result obligation, not a
parser error, timeout, missing import, or unrelated crash. Full output is in
[`06_mutation_proof.log`](evidence/06_mutation_proof.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied K definition, from each explicitly stated fresh
configuration and for arbitrary K integers `A,B,C`:

- fixed semantics loads the exact submitted function as
  `triangleAreaClosure`;
- each of the three invalid short-circuit regions returns exactly `-1`;
- the strict-valid region executes the real body and returns exactly
  `expectedArea(A,B,C)`;
- that result expands to the exact program-produced composition of the six
  fixed float primitives; and
- the pinned caller-visible scope, heap, allocation counters, stack, and return
  state are restored as claimed.

This is partial correctness under the selected semantics. It is not a
termination theorem for CPython and not a universal theorem that the opaque
float term denotes the mathematical area.

### Trust ledger

| Boundary | Influence | Status |
|---|---|---|
| K 7.1.337 compiler, Haskell prover, LLVM runtime, and K builtins | Proof checking and concrete execution | Ordinary toolchain trust. Fresh builds and independent mutations reduce, but cannot eliminate, this assumption. |
| Trusted supplied semantics | All language control/state behavior | Required selected semantics. Candidate tree is an exact, non-symlinked copy. Used rules were statically checked. |
| Trusted translator | Python-to-MPY identity | Acceptable trusted input; retranslation is byte-identical. |
| Manual proof constants for module/body/closure | Real-program pinning | Mechanically composed and hash-equal to submitted MPY; loader and body-sensitivity proofs support the link. |
| `divII`, `intToF`, `subF`, `mulF`, `powF`, `roundFN` | Entire valid result | Concerning but legitimate fixed primitive boundary. K proves structural use; isolated concrete and Python tests are finite evidence only. |
| K mathematical integer/Boolean/Map/List operations | Guards, binding, cells | Ordinary low-level trust boundary. |
| `expectedArea` means Heron's formula rounded like Python | Human-facing intent | Structurally evident and empirically supported, but not separately proved as nonlinear real mathematics or IEEE/Python rounding. |
| Formal input sort `Int` | Theorem domain | Narrower than the prompt's untyped notion of side lengths. Float inputs are tested but not formally proved. |
| CPython overflow and repeated-call behavior | Exceptions and broader contexts | Excluded from the formal fresh-entry theorem; concrete witnesses document the gap. |
| Missing generation metadata/logs | Provenance auditability | Concern; does not replace or undermine the independently reconstructed proof. |

### Gate decisions

- Real-program soundness: **PASS**. Exact body execution, no operational
  bridge/oracle, satisfiable states, body sensitivity, and a rejected false
  result mutation.
- Intent adequacy: **PASS with limitations**. The integer fresh-entry theorem
  matches the submitted algorithm, but float inputs, exceptional huge integers,
  repeated calls, and the universal numerical meaning of the opaque primitives
  are outside the proved bridge.
- Trust/evidence auditability: **PASS with concerns**. Reproducible source,
  commands, logs, independent differential tests, and rule inventory exist;
  generation provenance is absent and the key numerical bridge remains finite.

These limitations warrant `CONCERNS`, not `FAIL`: the successful proof is
sound and result-constraining under the fixed supplied semantics, pins the real
submitted AST, and rejects both body and postcondition mutations. The
limitations do not let a false candidate-local result be proved.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
