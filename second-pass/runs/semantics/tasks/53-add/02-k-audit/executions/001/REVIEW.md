# Independent adversarial review: 53-add

## Outcome

The candidate contains a legitimate, result-constraining K reachability proof for
the submitted integer-addition program. The proof was reconstructed from source,
the sole positive claim closed with `kprove` exit 0 and `#Top`, the embedded AST
was independently pinned to the submitted `solution.mpy`, and fresh result and
body mutations were rejected for the expected semantic reasons.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because all four
requested candidate provenance records and any structured generation trace are
absent. Those files were designated untrusted and the proof does not depend on
them, so their absence does not make the reconstructed theorem unsound; it does
leave a concrete generation-auditability gap.

All candidate material was treated as untrusted. Builds and experiments used
only the source copy under `/tmp/audit-work/53-add`; candidate bytecode and any
candidate-generated caches were not used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is
therefore no infrastructure-mode contradiction and a candidate verdict is
permitted.

The candidate `reference-semantics/` is also a real directory. Recursive
`diff -qr --no-dereference` found no missing, additional, changed, mistyped, or
symlinked entry relative to the trusted tree. Both trees contain 24 regular K
source files. No symlink exists anywhere under `/candidate`. The complete
topology, hashes, and comparison commands are in
[`evidence/01_integrity.log`](evidence/01_integrity.log), produced by
[`evidence/01_integrity.sh`](evidence/01_integrity.sh).

This identity establishes only that the candidate used the supplied semantics;
it does not bless `verification.k`, which was reviewed separately.

### Prompt, translator, and candidate artifacts

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. The matching
SHA-256 digests are recorded in `evidence/01_integrity.log`.

The proof-critical candidate artifacts are regular files and present:

- `solution.py`
- `solution.mpy`
- `spec.k`
- `verification.k`
- `prompt.py`
- `py2mpy.py`
- the complete supplied `reference-semantics/` tree

The candidate also contains `prove.sh`, `concrete-tests.mpy`, and a compiled
Python `__pycache__/solution.cpython-310.pyc`. These are additional evidence,
not source authorities. The bytecode was not copied or executed. No
candidate-provided `*-kompiled` definition or K cache was present or reused.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. Consequently there was no
candidate generation narrative to corroborate, but also none was trusted as a
substitute for reconstruction. This missing provenance is the reason for the
`CONCERNS` verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt specifies `add(x: int, y: int)`: add the two numbers, with
examples `add(2, 3) == 5` and `add(5, 7) == 12`. The trusted canonical entry
point returns `x + y`. Given the annotations and the MPY sorts, the intended
formal input domain is pairs of mathematical/Python integers.

The submitted `solution.py` is:

```python
def add(x: int, y: int):
    return x + y
```

It is the canonical algorithm. It is branch-free and has no collection-valued
"empty" case; zero is the relevant identity/boundary input. It uses Python's
arbitrary-precision integer addition, matching K's `Int`.

### Trusted translation

In scratch, the trusted translator was run as:

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -s regenerated-solution.mpy solution.mpy` exited 0, and both
files have SHA-256
`67c61c16675c9cff80240867fcd0afd5bbbc0cdcd75147d9acb520ce116c98ee`.
Commands and results are in
[`evidence/02_prepare_and_translate.log`](evidence/02_prepare_and_translate.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) loads the
trusted canonical and candidate entry points independently by absolute path. It
does not import candidate bytecode or reuse proof equations. Its preserved
input set is
[`evidence/differential-inputs.json`](evidence/differential-inputs.json):

- the two documented examples;
- explicit zero, sign, cancellation, negative, 64-bit edge, and
  arbitrary-precision cases;
- the Cartesian product of 11 boundary values;
- 5,000 deterministic generated pairs from
  `[-10^12, 10^12]`, seed `530053`.

After deduplication, 5,128 input pairs were tested. The canonical result, the
candidate result, and Python's direct `x + y` agreed with integer result type on
every case. Mismatch count was zero and the command exited 0; see
[`evidence/02_differential.log`](evidence/02_differential.log).

This test is finite evidence about the Python-to-intent bridge. Universal
correctness comes from the K claim and direct source/translation inspection,
not from the test count.

## 3. Clean proof reconstruction

### Clean source preparation

Only explicitly selected source files were copied to
`/tmp/audit-work/53-add`; the candidate `__pycache__` and any derived
definitions were excluded. Before compilation, the exact scratch output
directories `runtime-kompiled` and `verification-kompiled` were removed.
Preparation is logged in `evidence/02_prepare_and_translate.log`.

The installed live tools were independently detected as K version
`v7.1.337`, build date `2026-06-18`.

### Concrete definition

The supplied source semantics was freshly compiled:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Compilation exited 0. The candidate's concrete assertions then ran with:

```text
krun concrete-tests.mpy --definition runtime-kompiled
```

This exited 0 with `.K`, `NoExc`, and exit code 0. The LLVM build emitted
non-exhaustiveness warnings for several unused general-purpose total functions:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are
discussed in Stage 5; none is reachable from the submitted add program.

### Proof definition and every positive claim

The proof definition was freshly compiled from source:

```text
kompile verification.k \
  --backend haskell \
  --main-module ADD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Compilation exited 0. `spec.k` contains exactly one positive target claim. It
was independently run:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC
```

`kprove` exited 0 and printed an exact `#Top` line. The complete bounded build
and proof record is
[`evidence/03_reconstruct.log`](evidence/03_reconstruct.log), generated by
[`evidence/03_reconstruct.sh`](evidence/03_reconstruct.sh).

The remaining compiler warnings concern unused variables in two `strLt`
equations. They do not change those equations and are irrelevant to the target
trace.

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The sole claim quantifies `X:Int` and `Y:Int` with no additional `requires`
clause. Its initial state is:

- `<k>` contains `#callAdd(X, Y)`;
- current environment is module scope 0;
- module scope 0 is empty and has the builtins scope `-1` as parent;
- the builtins scope is exactly `builtinsScope`;
- next scope location is 1;
- heap is empty and next heap location is 0;
- call stack is empty;
- return state is `noRet`;
- exception state is `NoExc`;
- exit code is 0.

This precondition is satisfiable for every pair of K integers. A concrete
satisfying state with `X=2`, `Y=3` is preserved in
[`evidence/spec-ground.k`](evidence/spec-ground.k).

### Postcondition in plain language

At termination, `<k>` must be exactly the integer `X +Int Y`. The environment,
heap, heap location, stack, return state, exception state, and exit code must
have their original values. Module scope 0 must retain the newly loaded `add`
closure whose parameters and body exactly match the submitted AST; the
builtins scope is unchanged.

This is an exact result and exact final-state constraint. It is not a free
variable, tautology, existential oracle, one-way implication, or a claim that
only constrains an unrelated cell.

### Actual-program pin

`verification.k` does not read a path at proof time; its fresh entry symbol
expands to an embedded `#loadAll(Module(...))` AST and then an ordinary call.
That makes syntactic pinning essential. The audit established it in two
independent steps:

1. the trusted translator regenerated submitted `solution.mpy` byte-for-byte;
2. [`evidence/program_pin.py`](evidence/program_pin.py) balanced and extracted
   the argument of `#loadAll` from `verification.k`, normalized whitespace
   only, and compared it with submitted `solution.mpy`.

Both normalized token sequences were:

```text
Module(FuncDef("add",Params("x","y"),Return(BinOp("+",Name("x"),Name("y")))))
```

The comparison exited 0 with `normalized_byte_sequence_equal=True`; see
[`evidence/04_pinning_and_ground.log`](evidence/04_pinning_and_ground.log).
Thus the proof wrapper executes the submitted translated body, not a substitute.

### Control-flow correspondence

There are no loops or helper claims. The real fixed-semantics path is:

1. `#loadAll` sequences the exact `FuncDef`.
2. `FuncDef` stores a closure with the exact parameters, body, and defining
   environment in module scope 0.
3. `Call` evaluates `Name("add")`, resolves that closure through scope lookup,
   and evaluates `Int(X)` then `Int(Y)` left-to-right.
4. Closure dispatch allocates a temporary scope and frame, binds `x=X` and
   `y=Y`, and executes the real `Return(BinOp(...))` body.
5. `BinOp`'s `seqstrict(2,3)` evaluation resolves `x`, then `y`; generic
   operator dispatch reaches the supplied integer equation
   `applyBin("+", I1:Int, I2:Int) => I1 +Int I2`.
6. `Return` records the value, and `#pop` restores the caller environment,
   removes the temporary scope, resets `scopeLoc`, empties the stack/return
   state, and leaves the sum in `<k>`.

No rule replaces the addition body with a summary or oracle.

### Ground substitution

The ground satisfying claim `#callAdd(2,3) => 5` exited 0 with `#Top`.
Fresh LLVM executions asserted the results for `(2,3)`, `(0,0)`, `(-10,3)`,
`(2^63-1,1)`, and a cancelling pair of 101-digit integers. They ended with
`.K`, `NoExc`, and exit code 0. Both Python implementations independently
returned the same expected values. Sources and outputs are
[`evidence/ground-tests.mpy`](evidence/ground-tests.mpy),
[`evidence/spec-ground.k`](evidence/spec-ground.k), and
`evidence/04_pinning_and_ground.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/05_rule_inventory.txt`](evidence/05_rule_inventory.txt) is the
exhaustive source-line inventory: 228 local `syntax` declarations, 696 rules, 5
contexts, 1 configuration, and 1 claim, for 931 entries total.
[`evidence/05_attribute_inventory.txt`](evidence/05_attribute_inventory.txt)
separately indexes function/total, priority, `owise`, concrete,
`no-evaluators`, symbol, strictness, and macro attributes. No local
`functional` or `simplification` declaration exists. The generation commands
and per-file counts are in
[`evidence/05_inventory.log`](evidence/05_inventory.log).

The decision below applies to every source-line item indexed for each row.
“Accepted/inert” means the item was reviewed at the supplied MPY-subset level,
does not syntactically occur in or match the target execution path, and cannot
contribute to closure of this claim. It is not a claim that the minimal MPY
subset models all exceptional or dynamic behavior of full Python.

| Source | Syntax / rules / contexts | Target relation and decision |
|---|---:|---|
| `semantics.k` | 0 / 0 / 0 | Import/assembly module only; accepted. |
| `syntax.k` | 16 / 0 / 0 | Declares every submitted AST construct; accepted/used. |
| `core.k` | 37 / 46 / 0 plus configuration | Load, sequence, lookup, literals, argument evaluation, values, and cells reviewed; accepted/used. Other helpers accepted/inert. |
| `functions.k` | 4 / 15 / 0 | Exact unannotated closure creation, parameter binding, return, and frame restoration; accepted/used. Annotated-closure rules are inert. |
| `call.k` | 3 / 21 / 0 | Callee lookup, left-to-right arguments, and closure dispatch; accepted/used. Builtin/method cases are inert. |
| `operators.k` | 0 / 10 / 2 | `BinOp` dispatch is accepted/used; reference/object and compare cases are inert. |
| `int.k` | 1 / 16 / 0 | Generic integer `+` equation is accepted/used; other integer operations are inert. |
| `assert.k` | 0 / 3 / 0 | Inert in the proof; used only by reviewer concrete smoke tests. |
| `bool.k` | 0 / 13 / 1 | Accepted/inert. |
| `builtins.k` | 38 / 137 / 0 | Accepted/inert; no builtin call is reachable. Opaque MD5 is an unused trust boundary. |
| `comprehension.k` | 3 / 7 / 0 | Accepted/inert macros and rules. |
| `concrete.k` | 5 / 16 / 0 | LLVM-only concrete helpers; not imported by the Haskell proof definition and inert. |
| `controls.k` | 3 / 34 / 0 | Accepted/inert; the submitted body has no assignment, branch, or loop. |
| `dict.k` | 12 / 28 / 0 | Accepted/inert minimal dictionary subset. |
| `float.k` | 34 / 121 / 0 | Accepted/inert for this theorem; its opaque proof-domain float symbols are unused trust boundaries. |
| `iter.k` | 1 / 0 / 0 | Iterator syntax only; inert. |
| `list.k` | 5 / 27 / 0 | Accepted/inert. |
| `methods.k` | 27 / 75 / 0 | Accepted/inert. |
| `range.k` | 2 / 6 / 0 | Accepted/inert. |
| `set.k` | 6 / 12 / 0 | Accepted/inert. |
| `sort.k` | 6 / 19 / 0 | Accepted/inert; opaque sort primitives are unused trust boundaries. |
| `str.k` | 5 / 28 / 0 | Accepted/inert. |
| `subscript.k` | 15 / 40 / 2 | Accepted/inert. |
| `tuple.k` | 4 / 21 / 0 | Accepted/inert. |
| `verification.k` | 1 / 1 / 0 | Fresh entry definition; accepted/used and analyzed below. |
| `spec.k` | 0 / 0 / 0 plus 1 claim | Exact result/final-state reachability claim; accepted. |

### Used-construct map and rule interactions

| Submitted construct | Declaration | Operational rules |
|---|---|---|
| `Module` | `syntax.k:61` | `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` |
| `Call` | `syntax.k:28` | `call.k:19-21,69-74`; `core.k:185-191` |
| `Name` | `syntax.k:12` | `core.k:130-154` |
| `Int` | `syntax.k:9` | `core.k:194` |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:77-90` |
| `BinOp("+",...)` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; `int.k:9` |
| `#callAdd` | `verification.k:7` | `verification.k:9-16` |

Configuration and state footprints agree with the claim. The temporary call
scope is allocated at 1 and then deallocated; no heap allocation occurs;
module scope retains only the loaded closure; stack and return cells are
restored; no exception or exit rule is reachable.

Relevant overlaps are benign or refuted by the concrete configuration:

- unannotated and annotated function forms have different arity;
- closure, builtin, type, and bound-method dispatch constructors are disjoint;
- the higher-priority cell lookup/binding rules require a `"$cells"` marker,
  absent from both target frames, so ordinary lookup/binding is selected;
- integer, Boolean, float, string, list, and tuple operator equations are
  sort-disjoint on this `Int × Int` call;
- the generic `Call` rule is `owise`, but there is no matching special
  interception for `Name("add")`.

The used total helper `appendVal` has exhaustive empty/cons equations and
strict descent. `builtinsScope` is a fixed total map constant. `applyBin` is
intentionally extensible rather than globally total, but the exact used
`("+", Int, Int)` case exists. No target reasoning uses a totality annotation
to fabricate the result.

### Proof-local extension record

`#callAdd` is a definitional entry adapter, not an operational bridge over an
existing program operation:

- **Domain:** any two K integers and any surrounding configuration on which
  the fresh symbol occurs.
- **Matched context:** only the fresh `#callAdd(X,Y)` item; the continuation and
  all non-`<k>` cells are framed and preserved.
- **Effect:** inject the exact submitted module AST followed by an ordinary
  call with literal arguments.
- **State footprint:** the rule itself changes only `<k>`; all later state
  changes come from supplied semantics.
- **Value influence:** indirect, through execution of the loaded body.
- **Overlap/priority:** one unguarded rule for a fresh constructor, no
  priority, no competing fixed-semantics rule.
- **Justification:** exact AST equality with `solution.mpy`; no computation is
  skipped and no answer is stated in the rule.
- **Dependent:** the one entry claim.

There are no proof-local functions, `total`/`functional` declarations, opaque
symbols, priority rules, simplifications, lemmas, helper claims, loop
circularities, or result summaries.

### Opaque symbols and narrow coverage gaps

The supplied proof semantics declares the following opaque or effectively
opaque result symbols:

- sort/digest: `sortVS`, `sortKeyVS`, `md5hexCodes`;
- float/conversion: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  and `sqrtF`.

None can occur in the submitted syntax or the target trace, affect a branch,
flow into the result, or appear in the postcondition. Their interpretations
therefore do not affect this theorem.

The LLVM compiler's non-exhaustiveness warnings identify broader-domain
coverage gaps in unused total functions. This review does not label those
rules unsound: no false conclusion witness exists on the intended add input
domain because the functions are unreachable. The narrower finding is that
those parts of the supplied semantics would need separate validation before
auditing a program that uses them.

No rule encodes the task answer, substitutes another program, bypasses the
function body, or introduces an unconstrained oracle into the target result.

### Operational body sensitivity

As an independent sensitivity check, the embedded body was changed from `+`
to `-` in a fresh scratch proof definition while retaining the original
expected result for `(2,3)`. The mutated definition compiled successfully.
`kprove` exited 1 with `WarnStuckClaimState` and terminal
`<k> -1 ~> .K </k>` against the required result 5. This demonstrates that the
body is executed and controls the result. Sources and bounded output are:

- [`evidence/verification-body-mutation.k`](evidence/verification-body-mutation.k)
- [`evidence/spec-body-mutation.k`](evidence/spec-body-mutation.k)
- [`evidence/05_body_sensitivity.log`](evidence/05_body_sensitivity.log)

No claimed rule unsoundness remains, so no false-conclusion witness is needed.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` is present. The audit created a fresh ground
mutation,
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k), with the same
satisfiable initial/final cells as the positive ground claim but the false
result:

```text
<k> #callAdd(2, 3) => 6 </k>
```

The exact checks were:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC-VACUITY-AUDIT \
  --dry-run

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC-VACUITY-AUDIT
```

The dry run exited 0, establishing successful parsing/building. The proof
exited 1 with `WarnStuckClaimState`; its terminal configuration visibly
contains `<k> 5 ~> .K </k>`, which cannot unify with required result 6. It did
not fail because of a parser error, missing import, timeout, or unrelated
backend crash. The bounded record is
[`evidence/06_nonvacuity.log`](evidence/06_nonvacuity.log), generated by
[`evidence/06_nonvacuity.sh`](evidence/06_nonvacuity.sh).

The proof is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied MPY semantics and K's builtin theories, for arbitrary K
integers `X` and `Y`, starting from the exact entry configuration in `spec.k`,
execution of the embedded translated `add` module and call reaches:

- return value `X +Int Y`;
- module scope containing the exact loaded `add` closure;
- restored environment, scope allocator, empty heap, heap allocator, empty
  stack, `noRet`, `NoExc`, and exit code 0.

This is partial correctness at the selected semantics level. It does not prove
behavior for arbitrary Python objects or all constructs present elsewhere in
the supplied MPY semantics.

### Trust ledger

| Boundary | Dependence | Assessment |
|---|---|---|
| K parser/compiler, Haskell reachability prover, and kernel/backend implementation | All machine-checking | Standard unavoidable low-level trust boundary; live version and exact outputs recorded. |
| K builtin `Int`, `+Int`, `Map`, `List`, equality, and strictness-generated machinery | Integer result and state execution | Acceptable ordinary mathematical/runtime primitives; no task-specific conclusion. |
| Supplied MPY source semantics | Translation execution | Required fixed semantics, byte-identical to trusted mount, rebuilt and statically audited on the used path. |
| Trusted `/reference/py2mpy.py` | Python-source to MPY-AST bridge | Explicitly trusted input; fresh output is byte-identical to submitted `solution.mpy`. |
| Embedded-AST-to-file pin | The theorem's program identity | Independently checked by balanced extraction and normalized token equality; body-sensitivity mutation supports execution dependence. |
| `/reference/canonical.py` and CPython | Intent/differential oracle | Trusted reference plus finite empirical support only; not used as a substitute for K proof. |
| Opaque supplied float/sort/digest symbols | None | Inert for this theorem; changing any interpretation cannot affect target control or result. |
| Candidate `prove.sh`, concrete assertions, prose/logs, bytecode | None | Untrusted and not relied upon; all relevant results independently reconstructed. |
| Missing candidate generation records | Provenance only | Auditability concern, not a logical assumption of the theorem. |

### Intent and evidence gates

- **Real-program soundness:** pass. The real translated body executes, no
  operational bridge or result oracle is used, the final result is exact, a
  satisfying state exists, the body mutation is detected, and the false result
  mutation is rejected.
- **Intent adequacy:** pass for the annotated integer domain. The theorem,
  submitted source, canonical source, examples, arbitrary-precision behavior,
  and differential evidence all agree.
- **Evidence/auditability:** concern. The reviewer evidence is reproducible and
  complete, but the four requested candidate provenance records and structured
  trace are absent. Non-integer Python values, including Python's dynamic
  object-overloading cases, are excluded by the formal `Int` domain.

The missing provenance does not permit a false K conclusion, and the excluded
non-integer behavior is aligned with the prompt's `int` annotations. Therefore
the candidate remains legitimate, with the documented auditability limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
