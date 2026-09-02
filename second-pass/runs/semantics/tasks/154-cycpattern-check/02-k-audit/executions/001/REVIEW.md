# Independent adversarial audit: 154-cycpattern-check

## Executive decision

The candidate's two K reachability claims can be reconstructed from source and
both close with exit status 0 and `#Top`. The claims are non-vacuous,
body-sensitive, and constrain the return value to the recursively defined
`rotationsLoop(A, B, B)`. The embedded closure body is the exact submitted
`solution.mpy` function body.

That is not a proof of the requested contract on the stated domain. Neither the
prompt nor the entry claim excludes the empty second string. On the satisfying
input `a = ""`, `b = ""`, the trusted canonical implementation returns `True`
(the empty string is a substring), while the submitted implementation and its
formal postcondition both return `False`. The independent differential run
found this same discrepancy for all 96 tested cases with `b == ""`. Thus the K
claim faithfully summarizes an incorrect implementation/specification pair
rather than proving the intended result. This is a material adequacy failure,
not merely thin evidence.

There is also a narrower proof-extension evidence gap: the proof-local
`s[1:]` operational bridge is mathematically consistent with the supplied
semantics and passed fixed-versus-extended continuation-sensitive execution,
but the candidate supplies no bridge-free universal connection theorem. A
reviewer-authored universal attempt exposed the unproved symbolic equality
between `buildIS(...)` and `dropOne(S)`. No false conclusion witness was found
for this rule, so this review does **not** label it unsound.

## Audit setup and evidence conventions

- Rendered mode: `SUPPLIED_SEMANTICS`.
- Scratch root: `/tmp/audit-work/154-cycpattern-check`.
- Reviewer evidence: `/audit-output/evidence`.
- Candidate-provided compiled/cache artifacts were not copied or reused.
- Toolchain: K `v7.1.337`, recorded in
  [tool_versions.log](evidence/tool_versions.log).
- The required skills were applied in order: `using-kit`, then
  `validating-proof`. `writing-semantics` was not used because this is not
  `GENERATED_SEMANTICS`.

The complete per-sentence source inventory is
[k_rule_inventory.md](evidence/k_rule_inventory.md). It contains full text,
source line ranges, attributes, hashes, and classifications for every local K
sentence in the trusted supplied-semantics tree, `verification.k`, and
`spec.k`.

## 1. Input and provenance integrity

### Mode boundary

The trusted `/reference/reference-semantics` mount exists, as required for
`SUPPLIED_SEMANTICS`. There is no rendered-mode/mount contradiction, so this is
not an infrastructure error.

The candidate `reference-semantics/` tree:

- is present;
- has no symlinks;
- has exactly the same recursive entry set and file types as the trusted tree;
- is byte-identical to the trusted tree (`diff -rq --no-dereference` exit 0).

The candidate prompt and translator are byte-identical to the trusted mounted
versions:

- `prompt.py` SHA-256:
  `66607b421ed8b5eb91de52ca96f1b071ecc536edf716451650816ae4e7701f64`;
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Exact checks, paths, types, hashes, and statuses are in
[stage1_integrity.log](evidence/stage1_integrity.log).

### Missing and extra/stale artifacts

The following explicitly requested provenance artifacts are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

No structured generation-trace artifact was present under `/candidate`.

There are no candidate symlinks. The candidate additionally contains
`__pycache__/solution.cpython-310.pyc` and `kore-exec.tar.gz`; these are
compiled/cache evidence, not source, and were deliberately ignored.

`/candidate/spec.json` is stale and does not serialize the current
`/candidate/spec.k`. It contains a `While`, `#while`, and `AugAssign`-based
claim, while current `spec.k` contains a `For`-based closure and no `While` or
`AugAssign`. This was treated only as a provenance inconsistency and was not
used in reconstruction. See
[stage1_spec_json_provenance.log](evidence/stage1_spec_json_provenance.log).

The missing logs and stale JSON reduce candidate evidence quality, but the
source artifacts needed for independent reconstruction are present.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract restatement

For string inputs `a` and `b`, return `True` exactly when some cyclic rotation
of `b` occurs as a contiguous substring of `a`.

The trusted canonical implementation sets `pat = b + b`, considers every
length-`len(b)` window of `a`, and compares it with every length-`len(b)`
rotation window in `pat`. With `b == ""`, its loop ranges are nonempty and the
empty slices compare equal, so it returns `True`.

### Submitted algorithm

The candidate begins with `pattern = b`. For each original character of `b`,
it:

1. checks whether the current pattern occurs in `a`;
2. returns `True` on success;
3. otherwise moves the first current character to the end by
   `pattern = pattern[1:] + char`.

For nonempty `b`, before iteration `k` the pattern is
`b[k:] + b[:k]`, so all `len(b)` rotations are checked. For empty `b`, the loop
has no iteration and the function returns `False`.

### Translation fidelity

A fresh translation was performed with the trusted translator:

```text
python3 /tmp/audit-work/154-cycpattern-check/reference/py2mpy.py \
  /tmp/audit-work/154-cycpattern-check/candidate/solution.py \
  > /tmp/audit-work/154-cycpattern-check/regenerated-solution.mpy
```

The regenerated and submitted `.mpy` files are byte-identical, both with
SHA-256
`fc0856f0a0475b9c73186876195c6c73e91dabf18cd514e0d4fe6d64b7c9548b`.
See
[stage2_translation_and_differential.log](evidence/stage2_translation_and_differential.log).

### Independent differential testing

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports
`/reference/canonical.py` and the scratch copy of the submitted
`solution.py`. Its scope is:

- all six documented examples;
- explicit empty, length, containment, rotation, duplicate-character, and
  Unicode boundaries;
- every pair over alphabet `{a,b}` with each argument length 0 through 5;
- 300 deterministic generated pairs over `{a,b,c}` with seed 154.

After deduplication, 4,246 pairs were executed. All documented examples
matched. There were 96 mismatches, all and only cases with `b == ""`:

```text
("", ""): canonical=True, candidate=False
("a", ""): canonical=True, candidate=False
...
```

The script intentionally exited 1 because mismatches were found. The complete
inputs and results are in
[differential_cases.json](evidence/differential_cases.json), with result-record
SHA-256
`13d0c0aa6dfe2596d82d132f0c80c821e97b11faaa0e35ee8cce071b234ea138`.

This is a material result divergence on an input not excluded by either the
natural-language prompt or the K entry precondition.

## 3. Clean proof reconstruction

No candidate-built definition, cache, `pyc`, archive, log, or serialized KAST
was reused. Only source files were copied to scratch, and the scratch
`reference-semantics` came from the trusted mount.

### Concrete definition

The trusted supplied semantics was freshly built with LLVM:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit status was 0. The compiler emitted unrelated non-exhaustiveness warnings
for unused language functions. Full bounded output is in
[stage3_runtime_build.log](evidence/stage3_runtime_build.log).

The reviewer harness
[concrete_harness.py](evidence/concrete_harness.py), freshly translated to
[concrete_harness.mpy](evidence/concrete_harness.mpy), exercised all examples
and empty/branch boundaries. `krun` ended with `.K`, `NoExc`, and exit code 0.
The harness intentionally asserts the submitted implementation's empty result
as `False`, documenting concrete program behavior rather than validating the
natural-language contract. See
[stage3_concrete_run.log](evidence/stage3_concrete_run.log).

### Loop-summary definition and claim

Fresh build:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
```

Exit 0; see
[stage3_proof_base_build.log](evidence/stage3_proof_base_build.log).

Independent positive claim:

```text
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-LEMMA \
  --output pretty
```

Exit 0 and `#Top`; see
[stage3_proof_loop.log](evidence/stage3_proof_loop.log).

### Entry definition and claim

Fresh build:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0; see
[stage3_proof_entry_build.log](evidence/stage3_proof_entry_build.log).

Independent positive claim:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
```

Exit 0 and `#Top`; see
[stage3_proof_entry.log](evidence/stage3_proof_entry.log).

Each positive spec module contains exactly one target claim, so every positive
target was run independently.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

The `SPEC-LEMMA.loop-invariant` precondition is an exact callee-loop-head
configuration:

- `<k>` contains the actual `#loop(str(REM), Name("char"), BODY)` followed by
  the function's `Return(False)` and `#endcall`;
- local frame 1 binds `a`, `b`, `char`, and `pattern`;
- environment 1 has parent frame 0;
- the stack head is exactly `frame(CONT, 0, 1)`;
- `<ret>` is `noRet`;
- frame counters have the expected callee values.

There is no explicit `requires`; constructor and map matching are the
precondition.

The postcondition states that the complete loop/function execution:

- yields `rotationsLoop(A, P, REM)` immediately before the arbitrary `CONT`;
- restores environment 0;
- removes local frame 1;
- resets `scopeLoc` to 1;
- pops exactly the matching call frame.

A concrete satisfying witness is:

- `A = codes("hello")`;
- `B = codes("ell")`;
- `P = codes("ell")`;
- `REM = codes("ell")`;
- `CH = .IntSeq`;
- `G = .Map`;
- `BS = builtinsScope`;
- `CONT = .K`;
- `REST = .List`.

All scope keys are distinct and all constructor constraints are satisfiable.

### Entry claim in plain language

The entry precondition has no `requires` and allows arbitrary `IntSeq` values
`A` and `B`. It fixes:

- a call to `cycpattern_check(str(A), str(B))`;
- module frame 0 containing `cycpattern_check`;
- the exact two parameter names;
- the exact closure body copied from submitted `solution.mpy`;
- empty heap and stack, `noRet`, and `NoExc`.

The postcondition is the Boolean term `rotationsLoop(A, B, B)`. This is a
result-constraining equivalence-style reachability target, not a free variable,
tautology, or one-way implication.

The spec does not execute the outer `Module(FuncDef(...))` load. Because the
submitted module contains only that function definition, the pinned frame-0
closure is exactly the post-load state the supplied semantics produces. This
is a manual AST-fidelity bridge, checked against the byte-identical translated
program.

### Concrete substitutions

Reviewer-authored ground K claims are in
[ground_witnesses.k](evidence/ground_witnesses.k). They normalize the formal
summary for four satisfying inputs and close together with `#Top`; the backend
reports them as trivial after function normalization. See
[stage4_ground_witnesses.log](evidence/stage4_ground_witnesses.log).

| `a` | `b` | Formal `rotationsLoop` | Submitted Python | Canonical Python |
|---|---|---:|---:|---:|
| `"hello"` | `"ell"` | `True` | `True` | `True` |
| `"abcd"` | `"abd"` | `False` | `False` | `False` |
| `"abab"` | `"baa"` | `True` | `True` | `True` |
| `""` | `""` | `False` | `False` | `True` |

The last row is a satisfying entry-precondition state and directly refutes
adequacy to the intended result.

### Body sensitivity

In
[spec-body-mutation.k](evidence/spec-body-mutation.k), the embedded body was
materially changed from `pattern = b` to `pattern = ""`, while the original
postcondition was retained. The mutated spec dry-built with exit 0 and then
failed with `WarnStuckClaimState`; its residual exposes:

```text
rotationsLoop(A, .IntSeq, B) =/= rotationsLoop(A, B, B)
```

See [stage4_body_sensitivity.log](evidence/stage4_body_sensitivity.log). This
shows the proof is sensitive to the embedded program body.

### Adequacy decision

The entry claim pins the submitted program and its actual result, but its
postcondition is not the intended predicate on the full admitted domain. The
proof therefore cannot establish partial correctness for the requested
contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The generated inventory covers 26 files and records:

- 704 rules;
- 229 syntax declarations;
- 2 claims;
- 1 configuration;
- 5 contexts;
- 22 explicit `no-evaluators` opaque-symbol declarations;
- 35 concrete-only rules;
- 3 simplification rules;
- 47 sentences with priority attributes;
- 109 sentences with `total`;
- no `functional` declaration.

All records appear with complete source text in
[k_rule_inventory.md](evidence/k_rule_inventory.md), generated by
[inventory_k.py](evidence/inventory_k.py). Generation output and inventory hash
are in [stage5_inventory.log](evidence/stage5_inventory.log).

### Supplied-semantics rule disposition

The 695 rules and 227 syntax declarations under the trusted supplied-semantics
tree are the selected fixed language model, not candidate proof extensions.
Their exact provenance is integrity-confirmed. Each is therefore classified in
the inventory as a fixed-semantics declaration/rule; it is authoritative for
the K execution being proved. This does not automatically establish Python
adequacy, so every rule family reachable from `solution.mpy` was reviewed
below. Unreachable rule families cannot contribute to either positive claim.

| File/family | Rules | Syntax | Target relevance and decision |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Exact trusted assembly/import graph. |
| `syntax.k` | 0 | 16 | Declares every AST constructor used by `solution.mpy`; strictness is compatible with the reviewed control rules. |
| `core.k` | 46 | 37 | Configuration, sequencing, lookup, literals, argument evaluation, shared sequences. Used rules preserve the reviewed cells and left-to-right order. |
| `iter.k` | 0 | 1 | Iterator protocol declaration used by the `For`. |
| `str.k` | 28 | 5 | String iteration, concatenation, and substring membership used by the program. Structural equations are exhaustive and terminating on `IntSeq`. |
| `operators.k` | 10 | 0 | Routes `+` and `in` after operand evaluation. Used cases select the string rules. |
| `controls.k` | 34 | 3 | Assignment, `If`, `For`, target binding, and loop continuations. Used transitions match the real body and scope updates. |
| `functions.k` | 15 | 4 | Closure/frame lifecycle, return, and pop. The loop summary reproduces its exact result/control/scoping footprint. |
| `call.k` | 21 | 3 | Callee and arguments evaluate before the exact closure call; frame allocation/binding agrees with the entry state. |
| `subscript.k` | 40 | 15 | Fixed slice evaluation is pure for a string; the exact used `s[1:]` form is preempted by the proof-local bridge reviewed below. |
| `bool.k` | 13 | 0 | Imported Boolean behavior; no problematic target dependency. |
| `int.k` | 16 | 1 | Ground `Int(1)` literal support; no arithmetic-domain abstraction affects the result. |
| `assert.k` | 3 | 0 | Used only by reviewer concrete harnesses, never by the proof claims. |
| `builtins.k` | 137 | 38 | Builtins frame is present, but no builtin call occurs in the submitted function. Opaque MD5 is unreachable. |
| `comprehension.k` | 7 | 3 | Unused. |
| `concrete.k` | 16 | 5 | Imported only by `MPY-KRUN`, not by the proof definition; target uses none of its special cases. |
| `dict.k` | 28 | 12 | Unused. |
| `float.k` | 121 | 34 | Unused; all float opaque primitives are unreachable. |
| `list.k` | 27 | 5 | Unused. |
| `methods.k` | 75 | 27 | Unused. |
| `range.k` | 6 | 2 | Unused. |
| `set.k` | 12 | 6 | Unused. |
| `sort.k` | 19 | 6 | Unused; opaque sort primitives are unreachable. |
| `tuple.k` | 21 | 4 | Supplies ordinary target binding imported by controls; the `Name` target case is faithful. Tuple-specific rules are unused. |

The fixed semantics contains 22 explicit opaque `no-evaluators` symbols:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. None is reachable from either target claim. Compiler warnings also
identify broad total functions in unused modules; none is in the target
dependency slice.

### Used construct mapping

| Submitted construct | Declaration | Operational rules |
|---|---|---|
| `Module`, statement list | `syntax.k` | `core.k` `#loadAll` and statement sequencing |
| `FuncDef`, `Params`, `Call`, `Return` | `syntax.k` | `functions.k`, `call.k` |
| `Assign`, `Name` | `syntax.k` | `controls.k` assignment; `core.k` lookup |
| `Str`, `Bool`, `Int` | `syntax.k` | `str.k` and `core.k` literal rules |
| `For(Name("char"), Name("b"), ...)` | `syntax.k` | `controls.k` `#loop`; `tuple.k` name target; `str.k` iterator |
| `If` | `syntax.k` | `controls.k` `#branch`; proof-local symbolic branch rules |
| `Compare(..., "in")` | `syntax.k` | `operators.k`; `str.k` `strContains` |
| `BinOp("+", ...)` | `syntax.k` | `operators.k`; `str.k` `seqConcat` |
| `Subscript(..., Slice(Int(1), NoBound, NoBound))` | `syntax.k` | fixed `subscript.k`; preempted by reviewed proof-local bridge |

No used construct is fabricated or left without a declaration/rule.

### Candidate proof-extension inventory and decisions

`verification.k` adds 2 syntax declarations and 9 rules. It adds no opaque
symbol, external oracle, `functional` declaration, or unconstrained fresh
result.

| Extension | Class and complete-domain review | Decision |
|---|---|---|
| Two symbolic `#branch(C,...)` rules, lines 8–11 | Derived symbolic execution rules. Guards `C` and `notBool C` are disjoint and exhaustive for `C:Bool`; each agrees with the fixed `true`/`false` branch. Omitted cells are preserved. Ground overlap has the same RHS. | Sound. |
| `dropOne`, lines 15–17 | Total definitional summary over the two `IntSeq` constructors. It returns empty on empty and the tail on nonempty. Equations are disjoint, exhaustive, and descending. | Sound ordinary sequence mathematics. |
| Exact `Subscript(str(S), Slice(Int(1), NoBound, NoBound))` rule, lines 19–27, priority 30 | Operational bridge. It preempts fixed evaluation of a ground lower bound and two absent bounds. It changes only `<k>` and retains arbitrary continuation/cells; string slicing here is pure. `dropOne(S)` is extensionally `S[1:]`. | No false witness; semantically credible, but candidate lacks the required bridge-free universal connection theorem. Evidence gap documented below. |
| `rotationsLoop` declaration and three simplification rules, lines 31–43 | Total definitional summary. Empty `REM` yields `false`; nonempty `REM` yields `true` exactly under `strContains(P,A)`, otherwise recurses on the strict tail with the same pattern update as the program. Guards are complementary and RHSs do not overlap. | Sound characterization of the submitted loop. It is **not** equivalent to the requested predicate for empty `B`. |
| Promoted loop-summary rule, lines 51–94, priority 30 | Operational bridge derived from `SPEC-LEMMA.loop-invariant`, which closed in a definition that did not contain this bridge. Its LHS, continuation, bindings, environment, exact scope map, stack frame, return state, and state rewrites match the proved claim. Omitted heap/exception/exit cells are preserved in both. The theorem is quantified over the same arbitrary `CONT` and `REST`. | Sound promotion of the independently closed auxiliary claim. |

### Slice-bridge validation

The candidate contains no independent theorem connecting its slice bridge to
the fixed semantics. The reviewer built
[slice-connection-verification.k](evidence/slice-connection-verification.k)
against `MPY` with only a separate structural `dropOneConnection` function and
no operational bridge. The build exited 0. The universal arbitrary-continuation
claim in
[slice-connection-spec.k](evidence/slice-connection-spec.k) did not close. Its
residual is the expected unproved equality:

```text
buildIS(S, clampHi(1, isLen(S), 1), isLen(S), 1)
= dropOneConnection(S)
```

An additional inductive formulation also did not close because symbolic
`buildIS` remained opaque to rewriting. Logs:

- [stage5_slice_connection_build.log](evidence/stage5_slice_connection_build.log);
- [stage5_slice_connection_proof.log](evidence/stage5_slice_connection_proof.log);
- [stage5_slice_inductive_proof.log](evidence/stage5_slice_inductive_proof.log).

These failures are not counterexamples. The bridge equation is true by
constructor reasoning, and no false rule conclusion was found. Consistent with
the audit instruction, this is reported as a narrower missing universal-proof
gap, not as unsoundness.

The reviewer also used
[slice_continuation_harness.py](evidence/slice_continuation_harness.py) to put
an observable assignment and returned suffix after the bridge on empty,
one-character, and multi-character strings. Fixed `MPY-KRUN` execution and
bridge-enabled `VERIFICATION` execution both exited 0 and produced byte-identical
JSON final configurations, SHA-256
`b04943d00d9f89a9ed55d2c087f8f310ffa7d58660a4c3180dd166dc9d6233ab`.
See
[stage5_slice_operational_sensitivity.log](evidence/stage5_slice_operational_sensitivity.log).

### Static-soundness conclusion

No candidate rule is labeled unsound because no concrete or symbolic false
conclusion witness was found. The proof-local rules form a coherent execution
summary of the submitted algorithm. The decisive false witness applies instead
to the bridge from that summary to the task's intended postcondition:
`A = .IntSeq`, `B = .IntSeq` gives formal/candidate `false` but intended/canonical
`true`.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted.

The reviewer created [spec-vacuity.k](evidence/spec-vacuity.k) by changing the
entry result from:

```k
rotationsLoop(A, B, B)
```

to:

```k
notBool rotationsLoop(A, B, B)
```

This mutation changes the result-constraining obligation. It is demonstrably
false for the satisfying input `a = "hello"`, `b = "ell"`: the submitted
program and original summary are `True`, while the mutation requires `False`.

The mutated spec:

1. dry-built successfully with exit 0;
2. ran against the fresh `verification-kompiled`;
3. failed with exit 1 and `WarnStuckClaimState`;
4. exposed the unmet equality
   `notBool rotationsLoop(A,B,B) = rotationsLoop(A,B,B)`.

This is the expected reachable postcondition failure, not a parse error,
missing import, timeout, or unrelated crash. Exact commands and bounded output
are in [stage6_false_mutation.log](evidence/stage6_false_mutation.log).

The proof is therefore non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied MPY semantics and the reviewed proof extensions,
the machine-checked claims establish:

1. From the exact loop/call-frame state in `SPEC-LEMMA`, executing the submitted
   loop and the following `return False` unwinds the call and yields
   `rotationsLoop(A, P, REM)` to the saved continuation.
2. From the exact post-module-load closure state in `SPEC`, calling the exact
   submitted `cycpattern_check` body on `str(A), str(B)` yields
   `rotationsLoop(A, B, B)`.
3. `rotationsLoop` structurally computes the submitted algorithm: check one
   current pattern per remaining original character, return true on the first
   containment, otherwise rotate and recur; return false when no character
   remains.

This is a partial-correctness statement in the Kit sense. The proof result does
not by itself establish the human-facing meaning of the summary.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, builtin Int/Bool/Map/List/String theories | All builds, concrete runs, and proofs | Ordinary unavoidable toolchain trust. Fresh source reconstruction reduces artifact trust. |
| Trusted supplied MPY semantics | Both claims | Required selected semantics. Tree identity was checked. Used language subset was statically reviewed. |
| Trusted `py2mpy.py` | Source-to-`.mpy` fidelity | Byte-identical translator mount and byte-identical regeneration establish the submitted AST bridge. |
| Manual post-load closure embedding in `spec.k` | Entry claim pins the program | Exact current AST and body-sensitive failure support it. It is not dynamically linked to `solution.mpy`, so provenance comparison remains necessary. |
| Proof-local symbolic branch rules | Loop proof | Guarded, disjoint, and equal to fixed ground behavior. Acceptable derived rules. |
| Proof-local `dropOne` plus slice operational bridge | Loop proof | Value and control behavior are mathematically correct and empirically continuation-sensitive, but no bridge-free universal K connection theorem is present. Concerning evidence gap, not witnessed unsoundness. |
| `SPEC-LEMMA.loop-invariant` promoted as a rule | Entry proof | Acceptable: independently closed without the promotion and exact in context/state footprint. |
| `rotationsLoop` definition | Formal return result | Fully defined, non-opaque, and structurally tied to program execution. It is not a proof of the natural-language predicate on empty `B`. |
| Informal statement “`rotationsLoop(A,B,B)` means some rotation of `B` is in `A`” | Task-level correctness conclusion | True for nonempty `B`; false for empty `B`. This is the illegitimate adequacy bridge that determines the verdict. |
| Differential tests | Python/canonical intent bridge and finite program evidence | 4,246 finite cases; cannot replace proof. They expose, rather than discharge, the empty-input defect. |
| Explicit supplied opaque symbols | None of the target claims | All 22 are unreachable and cannot influence control, result, state, or postcondition here. |

### Gate summary

- Fresh verification/reconstruction: **PASS** — both target claims close with
  fresh definitions.
- Result constraint and non-vacuity: **PASS** — false-result and body mutations
  fail for the expected obligations.
- Real-program pinning: **PASS with a manual AST-fidelity boundary** — current
  translated body is exact.
- Proof-extension validation: **CONCERN** — no false rule witness, but the
  slice bridge lacks a bridge-free universal connection theorem.
- Natural-language/canonical adequacy: **FAIL** — admitted empty-`b` states
  produce the wrong result.
- Candidate provenance/evidence: **CONCERN** — four required files are missing
  and `spec.json` is stale, though independent reconstruction was possible.

The empty-input counterexample is within every entry precondition and changes
the required Boolean result. Consequently, the reconstructed K proof is a
legitimate execution summary of the submitted code but is **not** a legitimate
partial-correctness proof of problem 154's actual contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
