# Independent adversarial audit: 9-rolling-max

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. Fresh builds close the loop and entry
claims, the proof term is the macro-expanded submitted `solution.mpy`, a
material body mutation breaks the loop invariant, and a fresh false-result
mutation reaches the real result and is rejected.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
non-fatal limitations:

1. all four required provenance records are absent;
2. the two symbolic iterator bridges are truthful and independently connected
   in this audit, but the submitted proof omits a bridge-free connection theorem
   and does not declare its exhaustive `intsVS` embedding as a function; and
3. the identification of the recursively defined `rollingAcc` fold with the
   natural-language “maximum of every prefix” property is a straightforward
   informal induction supported by differential evidence, not a separate K
   theorem.

No false conclusion witness was found for any candidate rule. The bridge issue
is therefore reported as the narrower derivation/evidence gap required by the
audit instructions, not mislabeled as unsoundness.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` exists as a real directory, so the mount does
not contradict the rendered mode.

The candidate source artifacts needed for the proof are regular files and the
semantics root is a real directory. See
[stage1-required-source-types.log](evidence/stage1-required-source-types.log).
No symlink exists anywhere below `/candidate`.

The recursive, no-dereference comparison

```text
diff -ruN --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
```

exited 0. Every candidate semantics entry has the same type and contents as the
trusted tree, with no missing, additional, changed, mistyped, or symlinked
entry. Candidate `prompt.py` and `py2mpy.py` also compare byte-for-byte equal to
their trusted versions (both `cmp` exit 0). Full entry types, hashes, commands,
and statuses are in [stage1-integrity.log](evidence/stage1-integrity.log).
Candidate source hashes are preserved in
[stage1-candidate-source-hashes.log](evidence/stage1-candidate-source-hashes.log).

The following explicitly requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

There is no structured generation trace. These absences prevent provenance
corroboration but do not substitute for, or defeat, the fresh source audit.
`PROOF.md` and a candidate vacuity spec are also absent; neither was used as
evidence. The candidate contained no compiled K definition. A copied Python
`__pycache__` was explicitly discarded from scratch before building; see
[stage3-discard-copied-pycache.log](evidence/stage3-discard-copied-pycache.log).

All candidate and trusted artifacts used for execution were copied into
`/tmp/audit-work/9-rolling-max-audit`. All builds and mutations occurred there.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of integers, return a same-length list whose element at
position `i` is the maximum of the input prefix through `i`. The empty input
returns the empty list. The documented example is:

```text
[1, 2, 3, 2, 3, 4, 2] -> [1, 2, 3, 3, 3, 4, 4]
```

This restatement follows `/reference/prompt.py` and
`/reference/canonical.py`. The intended domain is finite Python `list[int]`;
Python integers and the K `Int` model are unbounded. Non-list inputs and lists
containing non-integers are outside the stated domain.

### Source inspection

`solution.py` implements the same prefix fold using a `first` flag. On the first
element it initializes `maximum` to that element; on later elements it updates
with `max(maximum, number)`; it appends exactly once per iteration. Its initial
`maximum = 0` and `number = 0` values are unobservable on empty input and are
overwritten appropriately for non-empty input. Thus negative-only inputs do not
incorrectly inherit zero.

The trusted command

```text
python3 trusted-reference/py2mpy.py candidate-source/solution.py \
  > regenerated-solution.mpy
```

exited 0, and `cmp candidate-source/solution.mpy
regenerated-solution.mpy` exited 0. See
[stage2-retranslate.log](evidence/stage2-retranslate.log) and
[stage2-mpy-byte-identity.log](evidence/stage2-mpy-byte-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports
the trusted canonical entry point and the scratch candidate entry point. It
tests:

- the documented example;
- empty and singleton lists;
- later values below, equal to, and above the current maximum;
- duplicate, increasing, decreasing, negative-only, mixed-sign, and
  arbitrary-precision cases;
- every list of lengths 0 through 5 over `{-2,-1,0,1,2}`; and
- deterministic seeded lists of lengths 0, 1, 2, 3, 8, 9, 16, 32, and 257,
  with 40 generated cases per length.

All 4,239 de-duplicated preserved inputs had identical returns and zero
mismatches. The concrete claim witness also matched:

```text
witness_input=[3, 1, 4]
canonical_witness=[3, 3, 4]
candidate_witness=[3, 3, 4]
```

The exact command, exit 0, scope, count, result, and input hash are in
[stage2-differential.log](evidence/stage2-differential.log); all generated
inputs are in [differential-inputs.json](evidence/differential-inputs.json).
The initially attempted reviewer harness had a Python syntax error before
either implementation loaded; that attempt is honestly preserved in
[stage2-differential-script-error.log](evidence/stage2-differential-script-error.log)
and has no bearing on the candidate.

## 3. Clean proof reconstruction

K was independently available at version v7.1.337. Exact tool paths and
versions are in [stage3-toolchain.log](evidence/stage3-toolchain.log).
No candidate K definition or K cache was present or reused.

### Fresh concrete definition

The fresh LLVM command was:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0; see [stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).
The compiler reported non-exhaustive total-function warnings in unrelated
`mapStrVS`, float, join, and subscript helpers. None can occur on this program
path.

An independently authored driver was translated with the trusted translator
and executed under that definition. It covers empty, singleton, all comparison
boundaries, the documented example, negative inputs, and large integers.
`krun` exited 0 with `.K`, empty stack, `NoExc`, and exit code 0. The driver and
translation are [audit-concrete-driver.py](evidence/audit-concrete-driver.py)
and [audit-concrete-driver.mpy](evidence/audit-concrete-driver.mpy); the run is
[stage3-krun-audit-driver.log](evidence/stage3-krun-audit-driver.log).

### Fresh proof definition and positive claims

The fresh Haskell command was:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0; see
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

The loop target was independently selected:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.rolling-max-loop
```

It exited 0 and printed `#Top`; see
[stage3-kprove-loop.log](evidence/stage3-kprove-loop.log).

The complete intended target set was then run:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`, thereby closing both the loop circularity and
the entry theorem; see
[stage3-kprove-all-targets.log](evidence/stage3-kprove-all-targets.log).

For transparency, an entry-only diagnostic using `--claims
SPEC.rolling-max-correct` was interrupted with status 130 after approximately
12 minutes of active CPU because filtering the helper loop claim also removes
the circularity on which the entry proof depends. It produced neither
`#Top` nor a stuck residual and is not treated as candidate evidence or a
candidate failure. Its bounded record is
[stage3-kprove-entry.log](evidence/stage3-kprove-entry.log). The actual,
unfiltered intended proof closed in about seven seconds.

## 4. Adequacy and real-program pinning

### Plain-language claims

`rolling-max-loop` has no textual `requires`; its K sorts and cells are its
precondition. It starts at the real supplied-semantics `#loop` head over an
arbitrary finite `IntSeq`, in a function-local scope containing `result`,
`first`, `maximum`, `number`, and `numbers`. It permits an arbitrary
continuation. At loop exit it requires:

- the continuation is preserved;
- the result heap list is the old accumulator followed by the recursively
  defined rolling maxima;
- `first` is false iff a first element was consumed;
- `maximum` is the final running maximum;
- `number` is the last element when one exists; and
- unrelated bindings, heap entries, and omitted configuration cells are
  preserved.

`rolling-max-correct` starts in the complete supplied initial configuration
with arbitrary `INPUT:IntSeq`. It loads `rollingMaxModule`, calls
`rolling_max` with exactly `list(intsVS(INPUT))`, and requires return `ref(0)`.
It fixes heap location 0 to the complete result
`rollingAcc(INPUT,true,0,.ValSeq)`, fixes allocation, fixes the installed
closure body and parameter, and requires empty stack, `noRet`, `NoExc`, and
exit code 0.

### Exact program identity

Both the submitted `solution.mpy` and the proof term `rollingMaxModule` were
parsed with the fresh proof definition, expanded with `kast --expand-macros`,
and emitted as KORE. `cmp` exited 0 and both files have SHA-256:

```text
1cbd12781e499b8dd0e3139eccd373d70bccce1fa68a9eca0ba48f46d7a83b61
```

Commands and hashes are in
[stage4-expanded-module-identity.log](evidence/stage4-expanded-module-identity.log);
the preserved expanded terms are
[submitted-module-expanded.kore](evidence/submitted-module-expanded.kore) and
[proof-module-expanded.kore](evidence/proof-module-expanded.kore). Thus the
`<k>` cell executes the submitted AST, not a substituted algorithm.

The loop macro is the exact `For` body inside that identity. It follows real
control flow: target bind, `If(first)`, maximum update, `append`, then the
supplied loop continuation.

### Satisfying states and concrete substitution

[spec-ground-witness.k](evidence/spec-ground-witness.k) provides fully ground,
satisfiable witnesses:

- loop witness: input `[3,1,4]`, heap object 7 initially `[2]`, `first=true`,
  `maximum=99`, `number=-5`, and empty continuation; the required post-state
  is result `[2,3,3,4]`, `first=false`, `maximum=4`, `number=4`;
- entry witness: the exact initial configuration on input `[3,1,4]`, with
  explicit post-result `[3,3,4]`.

Both claims exit 0 with `#Top`; see
[stage4-kprove-ground-witnesses.log](evidence/stage4-kprove-ground-witnesses.log).
Both Python implementations return the same `[3,3,4]`, as recorded in the
differential log. The returned value is therefore neither free nor a
one-directional tautology: the claim fixes the returned reference, the entire
referenced list, allocation, control, and exception state.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[K-RULE-INVENTORY.md](evidence/K-RULE-INVENTORY.md) is the exhaustive,
source-located inventory of all 25 K source files in scope. It contains 957
entries:

```text
configuration=1
context=5
syntax=236
rule=713
claim=2
```

It includes every local syntax declaration, ordinary rule, priority rule,
function/total declaration, macro, context, configuration, and claim. The
special-attribute extraction is
[k-special-attributes.txt](evidence/k-special-attributes.txt).

[RULE-DECISION-LEDGER.md](evidence/RULE-DECISION-LEDGER.md) assigns a decision
to every inventory row. The 928 supplied-semantics entries are the
byte-identical selected semantics. The ledger lists every active declaration
and rule chain used by the program; every supplied row in the exhaustive
complement is classified inactive by a disjoint top symbol, AST constructor,
receiver constructor, builtin/method string, or value sort.
`semantics/concrete.k` is additionally excluded from the Haskell proof import
graph (`VERIFICATION` imports `MPY`, not `MPY-KRUN`).

The active mapping covers module loading and statement order, import, closure
creation, frame lifecycle, argument evaluation, literals and lookup, list
allocation, assignment, `For`/target binding/loop control, `If`, builtin
`max`, mutating `append`, return, heap, scopes, stack, return, exception, and
exit cells. Evaluation and binding are left-to-right and all state-changing
rules preserve the cells claimed by the invariant.

The supplied semantics has 25 symbolic/opaque float, sort, and MD5 operations,
all named in the decision ledger. None is syntactically or operationally
reachable from this program or any result helper. No opaque value influences a
branch, result, state, exception, or claim.

### Candidate-local inventory

`verification.k` has exactly nine syntax declarations and 18 rules:

- three exact macros and their three expansion rules;
- `intsVS` plus two structural equations;
- two priority-40 iterator bridges;
- five total mathematical/local-state functions with 11 equations:
  `nextRolling`, `rollingAcc`, `firstAfter`, `maximumAfter`, and
  `numberAfter`.

There are no local opaque symbols, simplification rules, `[functional]`
declarations, or unguarded result oracles. The only local priority rules are
the two iterator bridges.

All total functions are covered by the algebraic constructors of their input
sorts and recurse on a strict tail. Guards/cases are disjoint except
`firstAfter`'s intentional overlaps; both overlaps have the same `false`
right-hand side. `rollingAcc` is a definitional summary used in the
postcondition, not an operational rule that replaces the submitted body.

### Iterator bridge validation

The empty and cons bridge rules match only:

```text
#iterNext(list(intsVS(.IntSeq)))
#iterNext(list(intsVS(iCons(I,R))))
```

They read and rewrite only the leading `<k>` computation, preserve every cell
and arbitrary suffix, are disjoint, and yield exactly empty or head-plus-tail
iterator results. They never replace a program-defined helper body.

A first bridge-free attempt retained the submitted ordinary `intsVS` syntax
and equations but removed both bridges. The definition built, yet the
universal connection claim got meaningfully stuck at the unchanged nested
`intsVS` term: without a function declaration, its ordinary rewrite does not
evaluate beneath `list`. See
[verification-no-bridges-ordinary.k](evidence/verification-no-bridges-ordinary.k),
[bridge-connection-ordinary.k](evidence/bridge-connection-ordinary.k), and
[stage5-kprove-bridge-connections.log](evidence/stage5-kprove-bridge-connections.log).
This is the submitted derivation gap.

The audit then used only the independently justified structural interpretation:
declare `intsVS` `[function,total]`, retain its same exhaustive and descending
empty/cons equations, and still omit both bridges. Under this bridge-free
theory, universal empty and cons connection claims and a ground observable
continuation-preservation witness all exit 0 with `#Top`. See
[verification-connection-theory.k](evidence/verification-connection-theory.k),
[bridge-connection.k](evidence/bridge-connection.k),
[stage5-kompile-connection-theory.log](evidence/stage5-kompile-connection-theory.log),
and
[stage5-kprove-bridge-connections-function-theory.log](evidence/stage5-kprove-bridge-connections-function-theory.log).

The candidate should ideally have included this bridge-free theorem or made the
embedding a total function. Nevertheless, the equations fully fix every
ground interpretation, the bridge matches that independently checked
interpretation on its complete domain, and no opposite-result witness is
admitted. It is therefore sound with a validation concern, not an
unconstrained oracle or false rule.

### Body sensitivity

The audit changed only the loop body from
`result.append(maximum)` to `result.append(number)`. The mutant definition
built, but its proof exited 1 with `WarnStuckClaimState`. The residual exposes
the exact false obligation equating a sequence appended with
`maxInt(MAXIMUM,I)` to one appended with `I`. See
[verification-body-mutant.k](evidence/verification-body-mutant.k),
[spec-body-mutant.k](evidence/spec-body-mutant.k), and
[stage5-kprove-body-mutant.log](evidence/stage5-kprove-body-mutant.log).
The proof is materially sensitive to the program body.

No rule is labeled unsound because no rule enables a false conclusion on the
intended input domain. The concrete false obligations instead behaved as an
honest proof should: they got stuck.

## 6. Fresh non-vacuity test

The fresh mutation in [spec-vacuity.k](evidence/spec-vacuity.k) uses the
satisfiable entry input `[3,1,4]` and changes only the final result element from
the true 4 to the false 5:

```text
expected false heap list: [3,3,5]
actual heap list:         [3,3,4]
```

The dry run built and translated successfully with exit 0; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log). The real
proof then exited 1 with `WarnStuckClaimState`. Its reachable residual has
`ref(0)` at `<k>`, clean control cells, and heap object 0 equal to
`[3,3,4]`; it cannot unify with the mutated destination. See
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

This is an expected unmet result obligation, not a parser error, missing
import, timeout, unreachable mutation, or unrelated crash. The positive theorem
is discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics and the structural meaning of `intsVS`, for
every finite K `IntSeq` of integers, execution of the exact submitted
`rolling_max` module from the stated initial configuration returns the result
reference with its heap list equal to:

```text
rollingAcc(INPUT, true, 0, .ValSeq)
```

It also establishes fresh result allocation, the final module binding, empty
stack, reset return state, no assertion exception, and exit code 0. The loop
claim establishes the complete loop-carried local and heap transformation with
an arbitrary continuation. This is a partial-correctness statement; behavior
outside the formal input domain is excluded.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 compiler, Haskell/LLVM backends, and K builtin integer/Boolean/map/list/string operations including `maxInt` | All builds and proofs | Ordinary low-level machine-checking trust boundary. |
| `/reference/reference-semantics` | All operational execution | Required supplied, trusted semantics; candidate tree is recursively identical. Only the actually used subset is mapped to Python behavior here. |
| Trusted `/reference/py2mpy.py` | Submitted AST identity | Translator is trusted input; its output is byte-identical to submitted MPY. |
| Macro-expanded KORE identity | Real-program pinning | Machine-checked byte identity between submitted and proof ASTs. |
| Structural `intsVS` interpretation | Arbitrary symbolic input, loop circularity, entry result | Exhaustive/disjoint/descending definition; bridge-free universal connection succeeds in the reviewer-authored total-function theory. Concern: theorem/attribute absent from submission. |
| `rollingAcc` means “maximum of every prefix” | Natural-language adequacy | Its equations directly implement that fold and are valid by structural induction; ground K and 4,239 differential inputs support the bridge. Concern: no separate K adequacy theorem. |
| Differential testing | Candidate-to-canonical bridge on tested inputs only | Zero mismatches, reproducible and broad, but finite empirical evidence is not a universal proof. |
| Missing generation provenance | Historical/audit trail only | Concerning loss of evidence; it does not affect the fresh reconstruction. |

The supplied semantics contains opaque operations, but none is a dependent of
either claim. No task answer is smuggled into an execution rule; `rollingAcc`
only states the mathematical postcondition while the actual submitted body
executes. The body-sensitivity and false-result tests demonstrate that neither
the program nor result can be changed freely.

### Excluded behavior and final rationale

The theorem does not cover non-list inputs, non-integer elements, full CPython
exception behavior outside this used subset, or any unused supplied construct.
It does not use provenance prose, traces, candidate tests, or finite
differential testing as a substitute for K reachability.

The fresh proof is sound, result-constraining, non-vacuous, and pins the real
generated program. The missing provenance and formally unsubmitted adequacy/
connection lemmas are limitations of auditability and intent bridging, but
they do not permit a false conclusion on the intended domain. That matches the
decision boundary for `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
