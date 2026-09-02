# Independent adversarial review: 0-has-close-elements

## Executive conclusion

The candidate contains a machine-checked, non-vacuous partial-correctness
theorem about the real generated function, but it is substantially narrower
than the natural-language contract and one advertised auxiliary loop claim is
not pinned to the real continuation.

The legitimate entry theorem is:

> For arbitrary K `Float` values `A`, `B`, and `T`, if
> `floatLt(absF(subF(A,B)),T)` holds, calling the generated
> `has_close_elements` body on the exactly two-element list `[A,B]` returns
> `true`.

This does not prove the required Boolean equivalence for arbitrary input lists.
It proves neither the non-close/`false` case nor any other list length. The
candidate's `innerRun` macro also omits the outer loop's `i += 1` from the
recurring outer-loop body. That helper is not used by the real entry proof:
an auditor-authored spec containing only the entry claim also closes with
`#Top`.

The result is therefore `CONCERNS / LEGIT`, not a proof of the full HumanEval
contract.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted tree
`/reference/reference-semantics` is present, so there is no trusted-mount
contradiction and no infrastructure breach.

A recursive, no-dereference comparison of
`/candidate/reference-semantics` against the trusted tree found no missing,
additional, changed, mistyped, or symlinked entry. The candidate tree contains
no symlinks. The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Exact commands, checks, and
hashes are in [stage1-integrity.log](evidence/stage1-integrity.log).

All required candidate source artifacts used by the proof were regular files:

- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `reference-semantics/`;
- `verification.k` and `spec.k`;
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`.

The structured trace was present as one 1,038-line valid-JSONL file. I read the
metadata, final report, log, and trace only as untrusted generation claims. The
candidate claimed three `#Top` results, a restricted `SOUND-BUT-LIMITED`
theorem, and zero differential mismatches. The candidate log itself contains
many historical `#Top` and stuck-state strings, demonstrating why token
occurrence is not reconstruction evidence. Hashes, event counts, and the exact
untrusted final message are preserved in
[stage1-untrusted-claims.log](evidence/stage1-untrusted-claims.log).

Candidate-provided `runtime-kompiled/`, `verification-kompiled/`,
`branch-verification-kompiled/`, caches, binaries, and `kore-exec.tar.gz` were
not copied into or used by the audit build.

Stage 1 result: integrity passes; no missing or altered required artifact and
no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`, the intended entry
point is:

```python
has_close_elements(numbers: List[float], threshold: float) -> bool
```

It returns `True` exactly when there are two distinct positions in `numbers`
whose absolute difference is strictly less than `threshold`; otherwise it
returns `False`. Strict equality to the threshold is not close. Empty and
singleton lists return `False`.

The canonical program examines ordered pairs with distinct indices. The
candidate program at `/candidate/solution.py:4` examines each unordered pair
once by maintaining `0 <= i < j < len(numbers)`. It caches the length but does
not mutate the list. On the stated `List[float]` domain this is an equivalent
algorithm, including negative/zero thresholds, infinities, NaNs, and signed
zero under ordinary CPython float operations.

### Trusted translation

I ran the trusted translator from `/reference/py2mpy.py` over the scratch copy
of `solution.py`. The regenerated file was byte-identical to submitted
`solution.mpy`; both SHA-256 values are:

```text
6d1f624a584313b239dff221507508bae805284f13f94e551afd995417c1e1be
```

The exact command and exit 0 are in
[stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

[stage2_differential.py](evidence/stage2_differential.py) imports the trusted
entry point directly from `/reference/canonical.py` and the generated entry
point directly from the scratch copy of `solution.py`. It does not reuse any K
equation or candidate test oracle.

The input scope, recorded in
[stage2-input-manifest.txt](evidence/stage2-input-manifest.txt), was:

- both documented examples and 17 additional targeted boundary/control cases;
- every list of length 0 through 4 over nine boundary float values, crossed
  with ten boundary thresholds;
- 2,500 deterministic generated cases of lengths 0 through 8, seed 790622.

The values include NaN, both infinities, signed zero, the minimum positive
subnormal, maximum finite values, strict-equality and `nextafter` boundaries,
negative/zero/NaN/infinite thresholds, early and late true branches, and
no-pair cases.

Actual result:

```text
tested=76329
mismatches=0
EXIT_STATUS: 0
```

See [stage2-differential.log](evidence/stage2-differential.log). This is strong
finite fidelity evidence, not a universal proof.

Stage 2 result: the submitted Python and MPY are faithful to each other, and no
candidate/canonical divergence was found.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reconstruction`. Every build output was created there. No
candidate-provided compiled definition or cache was used. The installed tools
reported K version `v7.1.293`.

### Fresh concrete definition

Command:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit
```

It exited 0. The compiler reported non-exhaustive `[total]` equations for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; these are
addressed in Stage 5. Full bounded output is in
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).

### Fresh proof definition

Command:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

It exited 0. See
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

### Every positive target claim

Each claim was selected and run independently:

```bash
kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC --claims SPEC.inner-loop-true

kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC --claims SPEC.outer-loop-true

kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC --claims SPEC.entry-true
```

All three commands exited 0 and printed `#Top`. Exact commands and outputs are
in:

- [stage3-kprove-inner.log](evidence/stage3-kprove-inner.log);
- [stage3-kprove-outer.log](evidence/stage3-kprove-outer.log);
- [stage3-kprove-entry.log](evidence/stage3-kprove-entry.log).

These fresh results establish closure under the rebuilt fixed semantics and
proof source. They do not by themselves establish adequacy or soundness.

Stage 3 result: all required builds and positive claims reconstruct cleanly.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

`inner-loop-true` (`/candidate/spec.k:6`) assumes:

- a callee frame containing the exact two-element float list `[A,B]`;
- `threshold=T`, `i=0`, `j=1`, and cached `n=2`;
- an active function frame and no exception;
- `abs(A-B) < T`, represented by the opaque fixed-semantics predicate.

It says the stated `innerRun` computation reaches `#pop` with
`retV(true)`.

`outer-loop-true` (`/candidate/spec.k:32`) has the same list and close-pair
condition, but starts at `i=0`, `j=0`, `n=2` and the outer `#while`. It says the
function reaches `#pop` with `retV(true)`.

`entry-true` (`/candidate/spec.k:58`) starts in the module frame with the
function name bound to `targetClosure`. It calls the closure on exactly
`[A,B]` and `T`, under the same close-pair condition, and requires the final
`<k>` result to be literally `true`.

The entry result is not a free variable, tautology, or one-way implication in
place of a claimed equivalence. It is a concrete result constraint. However,
the formal theorem itself is only one close-pair/true branch; it never claims
or proves the full natural-language equivalence.

### Exact body pinning

The submitted MPY body is at `/candidate/solution.mpy:3-22`.
`targetClosure` is at `/candidate/verification.k:8-32`.
[stage4_pinning_check.py](evidence/stage4_pinning_check.py) independently
builds the constructor tree with the trusted translator and compares
whitespace-normalized macro expansions.

Results:

```text
targetClosure_normalized_constructor_identity=True
outerRun_normalized_constructor_identity=True
innerRun_normalized_constructor_identity=False
```

See [stage4-pinning.log](evidence/stage4-pinning.log).

The entry `<k>` starts at a `Call`, not at the submitted top-level
`Module(...)`. This is an artifact-to-theorem bridge: the spec manually places
the exact translated closure in the module scope. The omitted top-level
`ImportFrom("typing","List")` is observationally a no-op in the supplied
semantics (`controls.k` routes every non-`math` import to `.K`). The normalized
constructor check establishes that the installed closure has the exact
parameter order, body, and defining scope produced by the submitted MPY.

This is adequate pinning for the entry function but remains a manually checked
source-to-spec bridge rather than direct execution of the MPY `Module` term.

### Auxiliary `innerRun` defect

The actual outer loop body is:

```text
Assign(j = i + 1)
While(inner)
AugAssign(i += 1)
```

The fixed while rule retains that entire body inside
`#loopLbl(#while(C,B))`. `outerRun` correctly contains all three statements at
`/candidate/verification.k:71-84`.

In contrast, the recurring outer `#while` stored inside `innerRun` at
`/candidate/verification.k:49-63` contains `Assign(j=...)` and the inner
`While`, but omits the final `AugAssign(i += 1)`. Therefore the
`inner-loop-true` LHS is not the actual reachable inner-loop configuration.
This is a helper pinning failure, although not an unsound semantic rewrite:
`innerRun` is only a macro, and its close-pair assumption causes an immediate
`Return(true)` before the differing suffix can execute.

To determine whether this defect contaminates the real entry theorem, I
created [spec-entry-only-audit.k](evidence/spec-entry-only-audit.k), which
contains the entry claim and no helper claims. It independently printed
`#Top` and exited 0:
[stage4-entry-only-proof.log](evidence/stage4-entry-only-proof.log). Thus the
real entry result does not rely on the mismatched helper.

### Satisfiable ground state

The single witness

```text
A = 1.0
B = 1.25
T = 0.5
abs(A-B) = 0.25 < 0.5
```

satisfies every claim precondition. Both trusted canonical Python and generated
Python returned `True`; see
[stage4-witness-python.log](evidence/stage4-witness-python.log).

I also translated and executed an auditor-authored MPY witness with the fresh
LLVM definition. It terminated with `<k> .K </k>`, `NoExc`, and exit code 0:
[stage4-witness-krun.log](evidence/stage4-witness-krun.log). The source and
translated test are
[stage4_witness_program.py](evidence/stage4_witness_program.py) and
[stage4-witness.mpy](evidence/stage4-witness.mpy).

### Adequacy gap

The intended precondition admits arbitrary `List[float]` values and arbitrary
float thresholds. The formal precondition instead requires:

- exactly two elements;
- the sole unordered pair is already assumed close;
- only the `True` result.

Empty, singleton, longer-list, non-close, strict-boundary, and all `False`
behaviors are unproved. The theorem therefore does not establish the complete
program contract even though the generated Python happens to agree with the
canonical implementation in Stage 2.

Stage 4 result: the entry theorem pins and executes the real generated function
body and constrains its result, but scope adequacy fails and the unused inner
helper is not a real control-flow state.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[stage5-rule-inventory.txt](evidence/stage5-rule-inventory.txt) inventories
every local `requires`, module/import, configuration, context, syntax
declaration, rule, and claim from:

- `reference-semantics/semantics.k`;
- every helper `.k` file in `reference-semantics/semantics/`;
- `verification.k` and `spec.k`.

The inventory contains 1,104 line-addressed records: 698 rules, 230 syntax
declarations, 5 contexts, 1 configuration, and 3 claims. It separately tags
functions, total declarations, opaque/no-evaluator symbols, concrete rules,
priorities, `owise`, macros, and operational versus equational rules. There
are no local `[simplification]` or `[functional]` declarations.

[stage5-static-assessment.md](evidence/stage5-static-assessment.md) supplies
the categorical decision applying to every inventory record and the detailed
used-path map. The complete fixed tree was read; unused baseline rules were
distinguished from rules that can contribute to these claims.

### Proof-local extension inventory

`verification.k` adds exactly:

| Extension | Class | Decision |
|---|---|---|
| `targetClosure` macro | Definitional syntactic abbreviation | Exact generated closure; sound and used by entry. |
| `outerRun` macro | Definitional syntactic abbreviation | Exact reachable outer computation; sound. |
| `innerRun` macro | Definitional syntactic abbreviation | No operational rewrite, but its stored continuation is not the real continuation. |

It adds no function, `[total]` or `[functional]` declaration, opaque symbol,
priority rule, ordinary operational rule, simplification rule, result oracle,
or task-answer equation. Consequently there is no proof-local operational
bridge and no skipped program-defined body requiring a connection theorem.

### Used semantic path

Every submitted construct maps to fixed declarations and rules:

- name lookup and the builtins scope in `core.k`;
- left-to-right callee and argument evaluation, closure frame creation, and
  binding in `call.k` and `functions.k`;
- current-scope `Assign`/`AugAssign`, `If`, `While`, and loop continuations in
  `controls.k`;
- integer `+` and `<` in `int.k`;
- list length in `builtins.k`/`core.k`;
- list subscripting and index normalization in `subscript.k`;
- float subtraction, absolute value, and `<` dispatch in `float.k`;
- abrupt return, frame pop, scope restoration, no-exception state, and final
  Boolean result in `functions.k`.

The reachable calls use exact arity. Arguments and operands evaluate
left-to-right. The claim list is a bare `list(ValSeq)` value, so no heap
allocation, alias, or mutation rule is exercised. `i=0`, `j=1`, and length 2
make both relevant `valSeqAt` calls constructor-headed and in bounds. Return
correctly discards the remaining loop continuation and restores the caller
frame.

No overlaps or priorities on the used plain-frame/bare-list path allow a
different observable result. The cell/ref priority rules have unsatisfied
shape or guard conditions.

### Opaque float trust boundary

Under the Haskell proof backend, `subF`, `absF`, and `floatLt` are supplied
`[function,total,symbol,no-evaluators]` primitives
(`/reference/reference-semantics/semantics/float.k:50-56,103-105`). Their
`[concrete]` equations are used only in LLVM.

These are externally supplied fixed primitives, not abstractions of
program-defined code. The formal theorem is conditional on their named
predicate. Fixed execution recomputes that exact predicate, so the proof is
parametric in its interpretation: if it is true, the function takes the early
return. The proof does not establish a universal theorem equating those
symbols with CPython IEEE-754 operations. Concrete K execution and the 76,329
Python differential cases support only that empirical bridge.

### Totality warnings and unused fixed-semantics discrepancy

The fresh LLVM compiler warned of incomplete equations behind several
`[total]` declarations. Only `valSeqAt` occurs on this proof path, and only its
complete in-bounds equations at
`subscript.k:11-14` are reached. The remaining warned functions are
unreachable. This is an evidence/coverage limitation, not a false conclusion
enabled on a claim state.

The supplied fixed semantics also contains a global Python mismatch:

```k
applyCmp(">=", F1, F2) => notBool floatLt(F1, F2)
applyCmp("<=", F1, F2) => notBool gtF(F1, F2)
```

at `float.k:128-129`. False-conclusion witness: let `F1=NaN` and `F2=0.0`.
Python/IEEE says both `NaN >= 0.0` and `NaN <= 0.0` are false, while both K
right-hand sides are true because the corresponding `<` and `>` comparisons
are false. Neither `>=` nor `<=` occurs in `solution.mpy`, any claim, or a
reachable proof state. This is a documented limitation of the trusted supplied
baseline; it is not a candidate rule and cannot enable the submitted `<`
theorem.

Stage 5 result: no materially unsound candidate proof rule or execution bypass
was found. The real entry path is sound under the supplied primitive boundary.
The inner helper has an adequacy/pinning defect, and the supplied baseline has
unused global limitations with concrete witnesses.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. I created a distinct reviewer
mutation, [spec-audit-mutation.k](evidence/spec-audit-mutation.k), changing the
entry result from `true` to `noneV` while preserving the satisfiable close-pair
precondition and every initial cell.

First, the mutation was compiled to KORE:

```bash
kprove spec-audit-mutation.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-AUDIT-MUTATION \
  --dry-run
```

It exited 0 and produced KORE, so this was not a parser/import/build failure.
See [stage6-mutation-dry-run.log](evidence/stage6-mutation-dry-run.log).

Then:

```bash
kprove spec-audit-mutation.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-AUDIT-MUTATION
```

It exited 1 with `WarnStuckClaimState`. The residual contains:

```text
<k>
  true ~> .K
</k>
```

while the destination requires `noneV`. This is the expected unmet
result obligation, not an unrelated crash or unreachable mutation. Full
output is in [stage6-mutation-proof.log](evidence/stage6-mutation-proof.log).
The ground witness from Stage 4 demonstrates the mutation is false on a
satisfying input.

Stage 6 result: non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Subject to the supplied MPY theory, for all K floats `A`, `B`, and `T`:

```text
floatLt(absF(subF(A,B)),T)
```

implies that executing the exact generated closure on the bare
two-element list `[A,B]` terminates along the proved path with returned value
`true`, restores the caller frame, retains `NoExc`, and retains exit code 0.

This is a partial-correctness statement. In this fixed two-element,
close-pair scope, the symbolic execution also follows a finite terminating
path, but no total-correctness theorem is claimed.

### Trust ledger

| Boundary | Status and influence |
|---|---|
| Trusted prompt, canonical program, and translator | Authoritative mounted inputs. The translator establishes the Python-to-MPY artifact used by the proof; its correctness is trusted by the task. |
| Supplied reference semantics | Fixed theorem theory after exact tree-integrity verification. Core lookup/call/control/state rules are assumed as the selected semantics level. |
| K built-in integers, booleans, maps, lists, strings, and backend | Low-level trusted K/toolchain boundary for rewriting and `#Top`. Fresh build/run evidence uses K v7.1.293. |
| `subF`, `absF`, `floatLt` | Opaque, result-bearing supplied primitives in Haskell. All three positive claims depend on them. The formal conclusion is conditional on their exact atom; LLVM and differential tests are finite bridge evidence. |
| Closure/source pinning | Independently checked normalized constructor identity. The entry spec installs the exact closure instead of executing the submitted top-level `Module`; the annotation-only import is a no-op. This is a reviewer-checked informal artifact bridge. |
| `?FINALSCOPES` | Existentially permits the post-call scope map. The observable Boolean, caller environment, scope location, heap, stack, return state, exception, and exit code remain constrained; it does not free the result. |
| Python differential test | Finite evidence that the generated algorithm matches the canonical entry point on 76,329 documented/boundary/generated inputs. It is not part of the K proof and supplies no universal theorem. |
| Unused `innerRun` helper | Not a trusted boundary and not used by the isolated entry proof. Its continuation mismatch is an auxiliary adequacy defect. |
| Full HumanEval intent | Not proved. Arbitrary list lengths and the `False` direction remain outside the formal theorem. |

### Final decision

The entry claim reconstructs with the trusted source, executes the exact
generated function body through fixed lookup/call/loop/subscript/return rules,
constrains the result to `true`, has a concrete satisfying state, and rejects a
fresh false result. An entry-only proof also closes, so the mismatched helper
cannot smuggle or substitute the entry result. Those facts make the contained
entry theorem legitimate.

The verdict is not `PASS` because:

- the theorem covers only an exactly two-element already-close input and only
  the `True` result, far short of the natural-language contract;
- the spec pins a manually installed exact closure rather than starting from
  the submitted `Module` term;
- the symbolic float-to-Python bridge is conditional/empirical;
- `innerRun` does not match the actual inner-loop continuation;
- the supplied baseline has unused totality gaps and a NaN comparison
  discrepancy.

None of those concerns makes a false entry conclusion provable under the
stated close-pair precondition, and no candidate operational bridge, oracle, or
unsound proof-local rule was found.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
