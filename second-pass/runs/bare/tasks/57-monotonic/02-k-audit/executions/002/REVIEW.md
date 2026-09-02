# Independent adversarial audit: 57-monotonic

The candidate contains a freshly reconstructible, non-vacuous K proof about the
exact submitted program **for every finite list of mathematical integers**. Its
generated semantics is sound for the operations used on that subdomain, and I
found no rule that enables a false conclusion there.

It is nevertheless not a legitimate proof of the full HumanEval source
contract. The trusted prompt specifies only `l: list`; it does not restrict
elements to integers. Both trusted and submitted Python functions terminate and
return the intended result on, for example, float and string lists. The K value
domain admits only `IntList`. This excludes infinite, material families of
valid inputs. Under the benchmark's explicit mapping, this Kit
`SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares problem `57-monotonic`, condition `bare`, record
layout `legacy-selected-stage1`, and mode `GENERATED_SEMANTICS`. I used only the
launcher `container_paths`, not the host provenance paths.

The campaign lock is a regular file, has the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and is exactly equal as a JSON object to the `audit_campaign` block. All
launcher-declared mounts and all records required for
`legacy-selected-stage1` are present, readable, correctly typed, and not
symlinks:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, the present `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured `codex-trace/`.

Every directly recorded file hash matches. The independently recomputed
pipeline tree digest of `/candidate` is
`7e71e87628e750abdb7ac27d78c3d22d3bfaa543d368fce535129d0e3a8fbea4`,
matching both the result and invocation records. The independently recomputed
trace tree digest is
`197809696a1c8f388d08ed253d5c8c8d2ba6ec74cad19156fa3b2cb9b87b7507`,
matching `usage.json`. The one trace file also has its exact independently
verified recorded file hash.

The trace contains 186 valid JSONL records and no parse failures. I inspected
all tool-action/result records through a bounded event inventory. It records a
prior successful proof, but that was treated only as an untrusted claim.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts.
No candidate, reference, or generation-evidence entry is symlinked. As required
for `GENERATED_SEMANTICS`, `/reference/reference-semantics` is absent; the
candidate also has no `reference-semantics/`. There is no semantics-mode or
mount contradiction and no infrastructure breach.

Evidence:

- [final provenance check](evidence/stage1-provenance-check-final.log)
- [mounted inventory and hashes](evidence/stage1-mounted-inventory-hashes.log)
- [generation trace inventory](evidence/stage1-generation-trace-inventory.log)
- [generation output index](evidence/stage1-generation-output-index.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks whether the elements of a list are monotonically
increasing or decreasing. The trusted canonical returns true exactly when the
list equals its ascending Python sort or its reverse sort. The submitted
function returns the same Boolean expression directly:

```python
def monotonic(l: list):
    return l == sorted(l) or l == sorted(l, reverse=True)
```

For every finite list whose elements are mutually orderable under Python, this
is equivalent to “nondecreasing or nonincreasing.” Empty, singleton, and
constant lists satisfy both directions.

### Translation identity

From the trusted translator I ran:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/57-monotonic/solution.regenerated.mpy
cmp -s /tmp/audit-work/57-monotonic/solution.regenerated.mpy \
       /candidate/solution.mpy
```

The comparison exited 0. Both files have SHA-256
`defbbe28aa5bde39b5092455096db10e76684b1ab0401e4e6a08151ef2de27b7`.
See [translation identity](evidence/stage2-translation-identity.log).

### Independent differential test

The reviewer-authored test imports `monotonic` directly from the trusted
canonical and submitted solution. Its independent oracle uses adjacent `<=`
and `>=` comparisons rather than sorting. It covers:

- all three documented examples;
- empty, singleton, equal-pair, first-disjunct, second-disjunct, peak, valley,
  duplicate, and large-integer boundaries;
- mixed numeric, float, and string cases;
- every list of length 0–7 over `(-2, -1, 0, 1, 2)`;
- every list of length 0–5 over each of `(-1.5, 0.0, 0.25)` and
  `("a", "b", "c")`.

All 18 explicit cases and 98,384 generated cases agreed; mismatch count was
zero. This is finite evidence about the Python implementation, not a substitute
for the K proof.

Evidence:

- [differential script](evidence/differential_test.py)
- [exact input scope](evidence/stage2-differential-inputs.md)
- [differential results](evidence/stage2-differential-results.log)

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/57-monotonic`; candidate
`build/` contents and `__pycache__` were not used. K 7.1.293 was available at
`/usr/bin/{kompile,krun,kprove}`.

### Generated semantics

The fresh concrete build command was:

```text
kompile semantic.k --backend llvm \
  --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX \
  --output-definition build-audit/semantic-llvm-kompiled
```

It exited 0. Ten normal and boundary runs of the trusted-regenerated
`solution.mpy` covered empty, singleton, equal, increasing, decreasing,
nonmonotonic peak/valley, duplicate, negative, and large-integer inputs. Every
`krun` exited 0, and every K Boolean equaled an independent Python adjacent-pair
oracle.

The first reviewer comparison run incorrectly reported ten mismatches because
its output regex was over-escaped, even though the logged K outputs were
correct. I preserved that log, corrected only the parser, and reran the same
commands successfully. This was a reviewer-harness defect, not candidate
evidence.

Evidence:

- [LLVM build](evidence/stage3-kompile-semantic-llvm.log)
- [corrected concrete comparisons](evidence/stage3-concrete-semantics-results-rerun.log)
- [preserved initial reviewer-parser failure](evidence/stage3-concrete-semantics-results.log)
- [concrete test script](evidence/concrete_semantics_test.py)

### Proof definition and positive claims

The fresh proof build command was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module SEMANTIC-SYNTAX \
  --output-definition build-audit/verification-haskell-kompiled
```

It exited 0. The immutable original spec was then proved with:

```text
kprove spec.k \
  --definition build-audit/verification-haskell-kompiled \
  --spec-module SPEC
```

This exited 0 and printed `#Top`.

For claim-by-claim reconstruction, I created a semantically identical copy with
labels only. The installed frontend encoded an attribute label as, for example,
`SPEC-LABELED.label(universal)`. Using those exact generated labels, each of the
universal claim and three example claims independently exited 0 and printed
`#Top`. The earlier unqualified-label attempts exited 113 before proving; that
CLI-selection diagnostic is preserved and was not treated as a proof failure.

Evidence:

- [Haskell build](evidence/stage3-kompile-verification-haskell.log)
- [original four-claim proof](evidence/stage3-kprove-original-all-claims.log)
- [each isolated positive claim](evidence/stage3-kprove-each-claim-qualified.log)
- [labeled spec](evidence/spec-labeled.k)
- [label diagnostics](evidence/stage3-kprove-label-diagnostics.log)

## 4. Adequacy and real-program pinning

### Claim meanings

All four claims have implicit precondition `true`; their K sorts add the
material domain constraint.

1. Universal claim: for any `L : IntList`, run the submitted program on
   `listVal(L)` and reach `#monotonicSpec(L)`.
2. Increasing example: run `[1,2,4,20]` and reach `boolVal(true)`.
3. Nonmonotonic example: run `[1,20,4,10]` and reach `boolVal(false)`.
4. Decreasing example: run `[4,1,0,-10]` and reach `boolVal(true)`.

The universal postcondition is not free or existential. It reduces to:

```text
boolVal(
  eqIntLists(L, sortInts(L))
  or
  eqIntLists(L, reverseInts(sortInts(L))))
```

There are no helper or loop claims to pin. The configuration has only `<k>`,
and the complete fixed function body is executed by `#run`.

Every precondition is satisfiable. For example, `L = nil`,
`L = cons(2,cons(1,nil))`, and the three prompt lists are ground `IntList`
values. The differential log shows both Python implementations on those
inputs; the concrete K log shows the corresponding formal results.

### Mechanical real-program identity

Trusted regeneration first establishes source-to-`.mpy` identity. A separate
reviewer script then extracts the balanced constructor RHS of
`rule solutionProgram => ...` and compares constructor/string/punctuation
tokens with the regenerated `.mpy`. Both sides have 82 tokens and token digest
`42f5c149ca69b7376dffa7868d52e91183d6f933f65f33bad70be9b34200d9b9`.
They are identical.

The proof-local constant therefore names the exact function binding and body.
The lack of automatic source-to-proof regeneration is only a maintenance
observation for this immutable candidate.

Evidence:

- [program-term comparison script](evidence/compare_program_term.py)
- [program-term comparison result](evidence/stage4-program-term-comparison.log)

### Body sensitivity

I changed the program term actually executed by the claim: the descending
`sorted(..., reverse=True)` call became a second ascending `sorted(...)` call.
The mutated definition compiled. Its ground claim for `[2,1]` then exited 1
with `WarnStuckClaimState`, showing actual result `boolVal(false)` against
required `boolVal(true)`. This is the expected semantic effect, not a parser or
tool failure.

Evidence:

- [body-mutated definition](evidence/verification-body-mutated.k)
- [body-mutated spec](evidence/spec-body-mutated.k)
- [mutation build](evidence/stage4-body-mutation-build.log)
- [expected proof failure](evidence/stage4-body-mutation-proof-expected-failure.log)

### Fatal adequacy gap

The source signature is `l: list`, not `list[int]`, and neither the prompt nor
canonical imposes an integer-only condition. Both Python implementations return
`True` on `[0.5, -1.5]` and `["b", "a"]`. By contrast, the formal input is
necessarily `listVal(IntList)`, whose elements are K `Int`; attempting the
string list as a K argument fails at parsing because the semantics has no such
value.

This is not a finite-test complaint: all integer lengths and integer magnitudes
are universally covered. It is a type-domain omission excluding infinitely
many terminating, contract-valid inputs. That is material narrowing of the
HumanEval contract and is fatal under the benchmark decision rule.

See [domain-narrowing witness](evidence/stage7-domain-narrowing-witness.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains 22 local syntax/declaration groups, 30 local
rules, and four claims. There are no candidate helper K files beyond
`semantic.k`, `verification.k`, and `spec.k`. There are no local `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, macro, trusted,
or opaque declarations.

The full per-rule analysis and used-constructor map are in:

- [exhaustive rule inventory](evidence/stage5-rule-inventory.md)
- [mechanical declaration index](evidence/stage5-mechanical-declaration-index.log)
- [numbered source listing](evidence/stage2-and-static-source-listing.log)

The important conclusions are:

- `Module`, the single `FuncDef`, single parameter, `Return`, parameter lookup,
  both `sorted` call shapes, `BoolOp("or")`, list equality, and the literal
  reverse keyword are all declared and evaluated.
- The exact program has no observable heap mutation, allocation identity, I/O,
  exception handling, or alias effect, so the single `<k>` cell is sufficient.
- Function lookup selects the exact sole binding. Hard-coding the builtin
  `sorted` call is valid because this module has no rebinding.
- The eager `or` rule differs from general Python short-circuit control, but
  both operands in this exact body are pure and total on every claimed
  `IntList`; no result, state, exception, or control difference exists on the
  claim domain.
- Insertion-sort guards `I <=Int J` and `I >Int J` are mutually exclusive and
  exhaustive. Recursive sort, insert, reverse, append, and equality equations
  descend structurally and cover the used constructor domains.
- `solutionProgram` is an exact definitional constant, not an execution bypass.
  `#monotonicSpec` is a fully defined result postcondition, not an opaque
  oracle. No proof-local bridge replaces program-defined computation.
- Equality with ascending sort is equivalent to nondecreasing order, and
  equality with its reverse is equivalent to nonincreasing order, for finite
  integer lists. This elementary intent bridge is reviewed informally rather
  than proved as a separate K lemma.

The generated semantics is intentionally not a general Python semantics. Its
lookup behavior and partial evaluator would not be adequate for arbitrary
different modules, but minimal coverage of unused constructs is not a defect in
`GENERATED_SEMANTICS`. I found no rule that enables a false conclusion on the
fixed program's claimed integer-list domain; consequently there is no semantic
unsoundness witness to report. The adverse finding is formal-domain narrowing,
not a false K rule.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`. I created a fresh mutation using the
unmodified submitted program and a realizable input:

```text
claim <k>
        #run(solutionProgram, listVal(nil))
      => boolVal(false)
      </k>
```

The empty list is monotonic, and both Python implementations return `True`.
The mutated spec passed `kprove --dry-run` with exit 0, establishing that it
parsed and built against the fresh definition. Actual `kprove` exited 1 with
`WarnStuckClaimState`; the residual was exactly:

```text
<k>
  boolVal ( true ) ~> .K
</k>
```

Thus the positive theorem constrains the result and the mutation failed because
of the expected unmet obligation.

Evidence:

- [fresh mutation](evidence/spec-vacuity.k)
- [mutation dry-run/build](evidence/stage6-vacuity-mutation-build.log)
- [expected mutation failure](evidence/stage6-vacuity-mutation-proof-expected-failure.log)

## 7. Proven versus assumed accounting

### What is machine-checked

Under the candidate's generated K theory, for every finite K integer list `L`,
executing the exact trusted-regenerated submitted AST reaches the Boolean saying
that `L` equals its ascending insertion sort or the reverse of that sort. The
three prompt instances are also machine-checked. The theorem is body-sensitive
and result-constraining.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
| --- | --- | --- |
| K 7.1.293 parser, Haskell/LLVM backends, and reachability implementation | All builds and proofs | Standard unavoidable toolchain trust; version and clean commands recorded. |
| Imported K `INT`, `BOOL`, `STRING`, and generated list machinery | Integer comparisons/equality, Boolean operations, string-name comparison, AST lists | Acceptable low-level mathematical/runtime primitives. |
| Trusted `py2mpy.py` | Source-to-AST bridge | Byte regeneration and constructor-level proof-term identity verified. |
| Generated `semantic.k` | Meaning of the used Python subset | Exhaustively reviewed and concretely tested for the fixed program on integer lists. It is not treated as a supplied or general Python semantics. |
| Builtin `sorted` model as insertion sort | Both execution and postcondition values | Equations are exhaustive and mathematically truthful on `IntList`; concrete end-to-end comparisons support, but do not universally prove, the CPython bridge. |
| Eager modeling of `or` | Evaluation control | Acceptable only because both exact operands are pure and total on every claimed input; no general short-circuit theorem is claimed. |
| “equals sort or reverse sort” means monotonic | Human-facing property | Informal elementary argument for finite total integer orders; no separate K characterization lemma. |
| `IntList` represents the source contract | The theorem's entire input scope | Illegitimate for the full task: prompt/canonical allow other mutually orderable values, including floats and strings. This is the fatal adequacy gap. |

There are no opaque result symbols, unproved proof-local lemmas, trusted claims,
priority shortcuts, or unconstrained fresh values. Differential tests support
only implementation/semantic bridges over tested inputs; they are not counted
as the universal proof.

### Gate and benchmark decision

- Gate A — real-program soundness: **PASS** for the stated `IntList` theorem.
- Gate B — intent adequacy: **FAIL** because the formal sort materially narrows
  the source-contract domain.
- Gate C — trust/evidence auditability: **PASS** for the limited theorem; all
  trust boundaries and finite evidence are explicit and reproducible.
- Kit status: `SOUND-BUT-LIMITED`.
- Benchmark mapping: material HumanEval domain narrowing is
  `FAIL / NOT_LEGIT`, not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
