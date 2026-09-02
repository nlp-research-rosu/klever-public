# Independent adversarial review: 33-sort-third

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied semantics. The proof executes the
translated body, its generalized loop claim closes, the full entry proof closes
from a clean rebuild, and mutations of both the executed body and final result
are rejected. I assign `CONCERNS / LEGIT`, rather than `PASS`, because the
supplied semantics intentionally leaves the value-level meaning of symbolic
`sorted` and opaque sorted-list access outside K: the theorem is conditional on
the documented `sortVS`/`valSeqAt` contract, supported by ground execution and
finite differential tests but not a universal K connection theorem.

The complete command ledger is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). All executable work used source
copies in `/tmp/audit-work/33-sort-third`; no candidate definition or cache was
reused.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `33-sort-third`, condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- complete input provenance.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. There is no rendered-mode contradiction.

I read every record required for this layout: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete 238-line
JSONL trace. I also inspected the present legacy records
`legacy-metrics.json` and `legacy-run-input.json`. Historical
`runtime-metrics.json` is absent, but it is not required for this legacy layout.
The generation record claims `KPROVE_PASSED`; that claim was not used as proof
evidence.

The independently parsed trace has one start and one completion event, 38 tool
calls and 38 results, ten patch calls and results, and a session ID matching
the invocation/result records. See
[`generation-record-summary.log`](evidence/generation-record-summary.log) and
its reviewer script.

Integrity checks passed:

- The campaign-lock object is exactly equal to the `audit_campaign` block.
  The lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and `/audit-prompt.md` matches the lock's
  `999526823ad89bcd9b6e77db8f5f1189f629c86c9ecb308094b84c7161c04e5a`.
- Every recorded regular-file digest checked by
  [`integrity_check.py`](evidence/integrity_check.py) matches, including the
  trusted canonical, prompt, translator, run/task/result records, invocation,
  metrics, usage, prompt, output, and last-message files.
- The candidate prompt and translator are byte-identical to the trusted
  mounts.
- Candidate and trusted semantics have the same 25-entry recursive shape and
  byte-identical files. Every entry is a real directory or regular file; there
  are no links, additions, omissions, or mistyped entries.
- Independent legacy pipeline tree hashes are
  `3fc5c84a...` for the candidate (matching the stage-1 workspace record),
  `61020c40...` for the trace (matching `usage.json`), and `4e06397a...` for
  the supplied semantics (matching the manifest digest). The audit input also
  records launcher-layer tree hashes under a distinct digest scheme; recursive
  type-and-byte comparison independently establishes the mounted-tree identity.
- `/candidate`, `/generation-evidence`, and the trusted semantics are mounted
  read-only.

Evidence: [`integrity.log`](evidence/integrity.log),
[`mount-candidate.log`](evidence/mount-candidate.log), and the two companion
mount logs.

No audit-infrastructure breach was found.

## 2. Program fidelity and canonical comparison

The source contract says that `sort_third(l)` returns a list whose positions
not divisible by three equal the original positions, while the values at
indices divisible by three are those original every-third values in sorted
order. The trusted canonical copies the input, sorts `l[::3]`, assigns that
slice back, and returns the copy.

The submitted implementation computes `thirds = sorted(l[::3])`, traverses the
original list once with index `i`, appends `thirds[i // 3]` when
`i % 3 == 0`, and otherwise appends the original element. This is the same
transformation for finite plain lists whose selected elements can be sorted.
It also returns a fresh list and does not mutate the input.

Trusted regeneration was exact:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp --verbose regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both MPY files hash to
`a6f1d547a4bfc1dacc8f0808923b8277fc42e24ce17924fd8091c4b59469e58a`.
See [`translation-hashes.log`](evidence/translation-hashes.log).

The independent differential test imports `/reference/canonical.py` and the
scratch copy of the submitted solution. It covers the prompt examples, empty
and lengths around every modulo-three boundary, negative and duplicate values,
homogeneous strings and floats, all lists of lengths 0 through 7 over
`{-2,0,2}`, and 5,000 seeded random integer lists of lengths 0 through 80.
All 8,290 cases agreed, with no input mutation:

```text
cases=8290 mismatches=0 input_mutations=0
```

The exact generated inputs are
[`differential_inputs.jsonl`](evidence/differential_inputs.jsonl), SHA-256
`8350e442...`; the oracle/test is
[`differential_test.py`](evidence/differential_test.py).

## 3. Clean proof reconstruction

Only `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, the trusted
translator/prompt, and a fresh copy of the trusted semantics were placed in
scratch. Candidate `__pycache__`, compiled definitions, and any generated
caches were excluded.

The observed `kompile` and `kprove` version is K `v7.1.293`, matching the
campaign lock.

### Concrete definition

I compiled `MPY-KRUN` with the LLVM backend from the scratch source tree. The
build exited 0. A reviewer-authored translated K test module exercised empty,
one-, two-, three-, and four-element boundary lists, the second prompt example,
and a ten-element negative-value case. `krun` exited 0, ended with `.K`,
`NoExc`, and exit code 0. Evidence:
[`kompile-concrete.log`](evidence/kompile-concrete.log),
[`krun-concrete.log`](evidence/krun-concrete.log), and
[`audit_concrete_tests.py`](evidence/audit_concrete_tests.py).

The concrete compiler warned that several supplied `[total]` functions are
non-exhaustive over the complete `Val` universe. Only `valSeqAt` is on this
program's symbolic path; its deliberate opaque-total role is accounted for in
Stages 5 and 7.

### Proof definition and claims

The Haskell proof definition compiled from source with exit 0. The generalized
loop claim alone returned `#Top`, exit 0. The submitted unfiltered positive
command, which supplies that loop theorem while proving the entry claim, also
returned `#Top`, exit 0:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
#Top
```

Evidence: [`kompile-proof.log`](evidence/kompile-proof.log),
[`kprove-loop.log`](evidence/kprove-loop.log), and
[`kprove-all.log`](evidence/kprove-all.log).

For diagnostic clarity, filtering the helper out and asking for only
`SPEC.sort-third-correct` exits 1 at the real `#iterNext/#loopStep` state. This
does not contradict the positive command: the entry theorem intentionally uses
the separately proved loop circularity, and the unfiltered command proves both.
The residual is preserved in
[`kprove-correct.log`](evidence/kprove-correct.log).

## 4. Adequacy and real-program pinning

### Plain-language claims

`sort-third-loop` assumes:

- the active computation is exactly
  `#loop(list(INPUT), Name("value"), sortThirdBody) ~> CONT`;
- the current frame binds a nonnegative integer `i = I`, an arbitrary retained
  `l`, prior loop value `OLD`, result reference `HR`, and sorted-list reference
  `HT`;
- `HT` holds `SORTED` and `HR` holds already-built prefix `ACC`; and
- omitted scope/heap/configuration portions are framed.

It concludes that the loop is consumed and `CONT` resumes; `i` increases by
`vsLen(INPUT)`, `value` becomes the last iterated element (or stays `OLD` for
empty input), and the result heap becomes
`sortThirdAcc(INPUT, SORTED, I, ACC)`. All other framed state is preserved.

`sort-third-correct` starts from a clean module configuration and executes:

```text
#loadAll(sortThirdModule)
~> Call(Name("sort_third"), list(INPUT))
```

for arbitrary `INPUT:ValSeq`. It concludes with returned `ref(2)`, the function
binding installed in module scope, three allocations containing the every-third
slice, its `sortVS` result, and the complete `sortThird(INPUT)` result, heap
location 3, restored environment/stack/return state, no exception, and exit
code 0.

The result is not free: the returned reference is fixed to heap location 2,
whose contents are fixed by `sortThirdAcc`. This is an equality-bearing
post-state, not a tautology or one-way implication.

### Mechanical identity and witnesses

Trusted retranslation pins `solution.py` to `solution.mpy`. The reviewer
constructor identity claim expands `sortThirdModule`,
`sortThirdFunctionBody`, and `sortThirdBody` and compares the result to the
literal submitted MPY function binding/body. K proves it with `#Top`; the only
normalization is the external parser's `ListExpr()` versus K source syntax
`ListExpr(.Exprs)`. Evidence:
[`pinning-spec.k`](evidence/pinning-spec.k) and
[`kprove-pinning.log`](evidence/kprove-pinning.log).

The entry precondition is satisfiable. For example, take
`INPUT = .ValSeq` in the explicitly clean initial configuration. The concrete
example
`INPUT = [5,6,3,4,8,9,2]` is also satisfying. Direct substitution into the K
summary proves:

```text
sortThird([5,6,3,4,8,9,2]) = [2,6,3,4,8,9,5]
```

and both trusted canonical and submitted Python return the same list.
[`ground-summary-spec.k`](evidence/ground-summary-spec.k) closes with `#Top`
in [`kprove-ground-summary.log`](evidence/kprove-ground-summary.log).

Body sensitivity is genuine. I changed the else branch in the program term
actually expanded by `sortThirdModule` from `append(value)` to `append(999)`,
rebuilt successfully, and reran the original spec. The proof exited 1 with the
expected mismatch between prefixes containing `V` and `999`. Evidence:
[`verification-body-mutated.k`](evidence/verification-body-mutated.k),
[`kompile-body-mutation.log`](evidence/kompile-body-mutation.log), and
[`kprove-body-mutation.log`](evidence/kprove-body-mutation.log).

## 5. Rule-by-rule static soundness review

The complete source-oriented inventory is
[`k-source-inventory.json`](evidence/k-source-inventory.json), SHA-256
`c2513232...`. It records full text, line bounds, attributes, and normalized
hashes for every local sentence. The companion
[`k-source-dispositions.csv`](evidence/k-source-dispositions.csv) assigns a
review disposition and rationale to all 1,116 sentences, including all 706
rules. This is the exhaustive enumeration; the table below summarizes it.

| File | Syntax | Rules | Other material |
|---|---:|---:|---|
| `semantics/syntax.k` | 16 | 0 | AST grammar and strictness |
| `semantics/core.k` | 37 | 46 | one configuration |
| `semantics/iter.k` | 1 | 0 | iterator protocol declarations |
| `semantics/range.k` | 2 | 6 | unused here |
| `semantics/operators.k` | 0 | 10 | 2 contexts |
| `semantics/int.k` | 1 | 16 | integer arithmetic/comparison |
| `semantics/bool.k` | 0 | 13 | 1 context; unused bool-op paths |
| `semantics/float.k` | 34 | 121 | unused float paths/opaque symbols |
| `semantics/str.k` | 5 | 28 | docstring literal path is used |
| `semantics/set.k` | 6 | 12 | unused |
| `semantics/list.k` | 5 | 27 | iteration, allocation, append used |
| `semantics/tuple.k` | 4 | 21 | name target binding used |
| `semantics/subscript.k` | 15 | 40 | 2 contexts; slice/index used |
| `semantics/comprehension.k` | 3 | 7 | unused macros |
| `semantics/methods.k` | 27 | 75 | generic fallback imported; string methods unused |
| `semantics/controls.k` | 3 | 34 | assign/if/for/augassign used |
| `semantics/functions.k` | 4 | 15 | definition, call frame, return used |
| `semantics/builtins.k` | 38 | 137 | registry/dispatch support; other builtins unused |
| `semantics/call.k` | 3 | 21 | call evaluation/dispatch used |
| `semantics/sort.k` | 6 | 19 | opaque sort and allocating call used |
| `semantics/assert.k` | 0 | 3 | concrete tests only |
| `semantics/dict.k` | 12 | 28 | unused |
| `semantics/concrete.k` | 5 | 16 | LLVM-only helpers; not imported by proof main |
| `verification.k` | 8 | 11 | all candidate-local definitions |
| `spec.k` | 0 | 0 | 2 reachability claims |

Across the complete inventory there are 163 `[function]`, 123 `[total]`, 35
`[concrete]`, 26 `[owise]`, 45 priority attributes, 5 macro attributes, 25
explicit `symbol(...)` declarations, and 22 `no-evaluators` declarations.
There are no local `[simplification]` or `[functional]` declarations.

### Construct coverage and execution

| Submitted construct | Declaration/rules | Audited effect |
|---|---|---|
| module/function definition | `syntax.k`; `core.k:124-127`; `functions.k:14-16` | loads the real binding and closure |
| call/arguments | `call.k:16-32,38-50,69-75`; `core.k:183-191` | callee then left-to-right arguments, fresh frame, exact continuation |
| names/scopes | `core.k:130-181` | local lookup then builtins; `sorted` binding is pinned |
| list literal/allocation | `list.k:13-20`; `core.k:117-121` | fresh `result` at location 2 |
| slice `l[::3]` | `subscript.k:43-114` | bounds normalize to start 0, stop length, step 3; allocates location 0 |
| `sorted(...)` | `sort.k:18-37`; `call.k` dereference | dereferences slice, allocates location 1 containing `sortVS` |
| `for`/target binding | `controls.k:62-74`; `list.k:9-10`; `tuple.k:31-41` | structural list iteration and current-frame binding |
| `%`, `//`, `+`, `==` | `operators.k`; `int.k:9-27` | Python floored modulo/division for divisor 3 and integer branch test |
| `if` | `controls.k:50-54` | truthy Boolean branch, disjoint cases |
| subscripting `thirds` | `subscript.k:25-41` | heap dereference and nonnegative positional access |
| `result.append` | `call.k`; `list.k:52-55` | priority rule preserves receiver reference and updates heap in place |
| `i += 1` | `controls.k:20-23`; `int.k:9` | current-frame integer update |
| return/pop | `functions.k:77-90` | returns `ref(2)`, restores caller, preserves escaping heap |

Allocation and control footprints match the final claim: the slice, sorted
copy, and result consume locations 0, 1, and 2; appends allocate nothing;
callee scope 1 is removed; the return reference and all three lists remain.
The relevant priority rules preempt only their corresponding generic paths:
list slicing beats generic slicing, append beats pure method fallback, and heap
dereference beats generic value dispatch. Guards are disjoint on the actual
plain-frame/int/list path.

### Candidate-local extensions

The four constructor aliases (`sortThirdBody`, `sortThirdFunctionBody`,
`sortThirdClosure`, `sortThirdModule`) exactly name submitted syntax and do not
match or replace an operational `<k>` region. `thirdValue` has disjoint and
exhaustive `pyMod == 0` / `=/= 0` guards. `sortThirdAcc` and
`lastLoopValue` have disjoint empty/constructor equations and structurally
descend. `sortThird` is a one-equation definitional summary. All eight declared
functions are covered on their used domains; the 11 equations have no
conflicting overlap. There is no candidate priority rule, simplification,
opaque symbol, oracle, or execution-bypassing operational bridge.

The loop claim is a derived circularity, not a rewrite axiom asserted without
proof. Its arbitrary `CONT` is sound because the exact loop body contains no
return, break, exception, allocation, or cleanup effect; the fixed semantics
iterates to completion and resumes that continuation. The body mutation
demonstrates that it is sensitive to the displaced computation.

### Supplied boundary and unused rules

The only result-bearing opaque symbol on this proof path is the supplied
`sortVS`. `sort.k` routes the real `sorted` builtin to a fresh list containing
that symbol and provides ground Int/str insertion-sort equations. Symbolically,
`sortVS` is intentionally total and opaque. `valSeqAt` has correct constructor
equations for nonnegative in-bounds access and is deliberately `[total]` on an
opaque sequence. Thus the proof is parametric in these fixed language
primitives; it does not invent their values.

The other explicit opaque symbols are the supplied float primitives
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, plus `sortKeyVS` and `md5hexCodes`. None occurs in either claim or a
reachable target state.

The inventory classifies 715 fixed-semantics sentences as unreachable from the
submitted constructor term (other AST constructs, types, methods, builtins, or
concrete-only alternatives). I checked their heads and priority/owise overlaps
against the reachable terms; none can fire on or alter this proof. This review
does not claim that the intentionally minimal supplied language is a complete
Python semantics for those unused constructs.

I found no candidate or reachable fixed rule that enables a false conclusion
on the intended list-of-sortable-values domain. Accordingly, there is no
unsoundness allegation requiring a false-conclusion witness. The opaque-sort
issue is instead an explicit trust/evidence boundary.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created an independent mutation.
It leaves the execution and loop theorem unchanged but changes the final
result-bearing heap obligation from:

```text
2 |-> list(sortThird(INPUT))
```

to:

```text
2 |-> list(vCons(999, sortThird(INPUT)))
```

The mutated spec parses/builds and reaches the real final configuration. Proof
then exits 1 with `WarnStuckClaimState` on the unmet equality:

```text
sortThirdAcc(...) = vCons(999, sortThirdAcc(...))
```

This is the expected result obligation, not a parser error, timeout, or
unrelated crash. The satisfying ground witness `INPUT=[]` yields `[]` from
both Python implementations while the mutation requires `[999]`.

Evidence: [`spec-vacuity.k`](evidence/spec-vacuity.k),
[`kprove-vacuity.log`](evidence/kprove-vacuity.log),
[`vacuity_witness.py`](evidence/vacuity_witness.py), and
[`vacuity-witness.log`](evidence/vacuity-witness.log).

Non-vacuity gate: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the imported supplied K theory, for every finite `INPUT:ValSeq`, normal
execution of the exact submitted translated module from the claim's clean
configuration returns reference 2. Its list is:

```text
sortThirdAcc(
  INPUT,
  sortVS(buildVS(INPUT, 0, vsLen(INPUT), 3)),
  0,
  .ValSeq)
```

The fold preserves every non-multiple-of-three input value at its position and,
at every multiple of three, inserts the corresponding indexed value from the
supplied sorted every-third sequence. The proof also establishes the claimed
scope, heap, allocation, stack, return, exception, and exit-code post-state.
It is unrestricted in list length; it is not finite unrolling.

### Trust ledger

| Boundary | Influence | Status/evidence |
|---|---|---|
| K 7.1.293 frontend and Haskell reachability backend | parsing, compilation, symbolic execution, circularity soundness | toolchain/campaign assumption; fresh successful rebuild and mutation discrimination |
| Trusted `py2mpy.py` | Python-to-constructor identity | mounted hash, byte-identical regeneration |
| Supplied operational semantics | evaluation order, scopes, allocation, calls, loops, return | exact candidate/trusted semantics identity; exhaustive source inventory; concrete K executions |
| `sortVS` contract: ascending permutation of its input | all returned values at divisible-by-three indices and human “sorted” intent | fixed external builtin boundary, not candidate code; ground Int/str equations, K examples, and Python differential evidence; no symbolic universal K theorem |
| `valSeqAt` totality on opaque sorted sequences, with actual accesses in bounds | selected returned elements | fixed supplied boundary; constructor equations plus informal length/index argument; depends on `sortVS` preserving length |
| Canonical-to-rewrite equivalence | connection to original HumanEval implementation | algorithmic inspection and 8,290 finite differential cases; not a universal machine proof |

The same `sortVS`/`valSeqAt` terms appear in execution and the postcondition,
but this is not a candidate-created circular oracle: they are fixed external
language primitives deliberately outside the program-defined code being
proved. The theorem is interpretation-parametric/conditional on that named
contract. The limitation is that the supplied source contains comments and
ground implementations, not a bridge-free symbolic theorem proving ordering,
permutation, and length preservation for arbitrary `ValSeq`.

The proof does not establish full CPython behavior for heterogeneous
incomparable objects, user-defined comparison side effects, exceptions,
arbitrary object identity/aliasing, or unsupported Python constructs. Those are
outside this finite plain-list HumanEval execution model. Differential tests
support, but do not universally prove, the Python/K and summary/intent bridges.

Kit validation gates:

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS for the material HumanEval list domain,
  conditional on the supplied `sorted` primitive.
- Gate C, trust/evidence auditability: PASS with a disclosed finite-evidence
  limitation.

The proof is therefore legitimate and result-constraining, with a non-fatal
trust-boundary concern under the benchmark's decision mapping.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
