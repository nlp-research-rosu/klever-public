# Independent adversarial audit: 135-can-arrange

## Outcome

The candidate reconstructs to a sound, result-constraining, non-vacuous K
reachability proof for **every finite sequence of K integers**. It executes a
constructor term mechanically equal to the trusted-regenerated `solution.mpy`;
the proof-local comparison bridge agrees with the fixed supplied semantics; and
both a body mutation and a false-result mutation are rejected as expected.

It is not, however, a proof over the full source-contract domain. The trusted
prompt has an unannotated `arr` parameter and never says that array elements are
integers. Duplicate-free arrays of ordinarily ordered strings and finite floats
satisfy the stated contract, and both the trusted canonical function and the
submitted Python function handle them. The supplied semantics also executes
those examples. The entry claim nevertheless requires `ints(VS)`, which
universally excludes string and float elements. This is an infinite,
behaviorally material restriction, not an encoding-only normalization.

The K result is therefore `SOUND-BUT-LIMITED` at intent adequacy. The benchmark
prompt explicitly maps a material narrowing of the HumanEval source-contract
domain to `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher record declares:

- problem `135-can-arrange`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

No infrastructure breach was found.

### Launcher and campaign records

I read `/audit-input.json` before treating any candidate or generation material
as evidence. All records required for `legacy-selected-stage1` were present and
readable:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

`/generation-evidence/usage.json` was present and inspected. The optional legacy
records `legacy-metrics.json` and `legacy-run-input.json` were also inspected.
Historical runtime metrics are not required for this layout and were not
reconstructed.

`/audit-campaign-lock.json` has SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the hash recorded in `/audit-input.json`. Its parsed object is exactly
equal to the `audit_campaign` block. The installed K tools report version
`7.1.293`, matching the lock.

The independent check in
[`evidence/provenance_check.py`](evidence/provenance_check.py) recomputed every
launcher-recorded mounted-file hash. All matched. Its complete result is
[`evidence/stage1-provenance.log`](evidence/stage1-provenance.log), exit 0.

### Trusted-input comparisons

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`, SHA-256
  `c69d29724082028ac075ad280590d3c1081894ff2e8db4e3cfb88476bb44ec3c`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `/reference/reference-semantics` is present, as required in
  `SUPPLIED_SEMANTICS` mode.
- Candidate and trusted supplied-semantics trees each contain 25 entries.
  Recursive path/type/mode/size/content comparison found zero differences and
  no symlinks. The reviewer's documented tree digest is
  `d93ca0e80e636b3cae696d4a628337de2f11a1d6c708589aecbbb5957d2bd4f5`
  for each tree.
- The candidate tree and structured-trace tree contain no symlinks or special
  entries.

Thus there is no missing, added, changed, mistyped, or symlinked supplied
semantics artifact. This integrity result does not bless candidate rules in
`verification.k`; those are audited in Stage 5.

### Generation records as untrusted evidence

The structured JSONL trace contains 420 parseable records: 98 tool calls, 98
corresponding outputs, 87 reasoning records, 99 token-count events, and the
session events/messages. I parsed every record with
[`evidence/trace_inventory.py`](evidence/trace_inventory.py); the bounded,
command-oriented inventory is
[`evidence/stage1-generation-trace-inventory.log`](evidence/stage1-generation-trace-inventory.log).
The raw trace file hash matches its invocation manifest. The untrusted trace
claims two final `#Top` results, but no later audit stage relies on that claim.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From the trusted `prompt.py` and `canonical.py`, the function must return the
largest index `i >= 1` for which the current element is not greater than or
equal to its predecessor. On ordinarily totally ordered values this is exactly
`arr[i] < arr[i - 1]`. If there is no such index, it returns `-1`. The prompt
says elements are duplicate-free. It does not state that elements are integers
and the function signature has no type annotation.

The canonical implementation scans indices 1 through the end, overwriting its
answer on each descent. The submitted implementation scans elements while
maintaining `index`, `previous`, and `result`; it performs the same overwrite
on each descent. Initializing `previous` to zero is harmless because the first
element is guarded by `index > 0`.

### Trusted regeneration

I regenerated the constructor term in scratch with:

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`4dde0d7b511f2a3c2602db1b91e749358bcd70effeb56595c4be59684e30ba3d`.
`cmp` and the logged command exited 0:
[`evidence/stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) independently
loads the trusted canonical entry point and submitted entry point and compares
both with a third, independently written adjacent-pair oracle. It covers:

- both documented examples;
- empty and singleton arrays;
- first-comparison rise/drop;
- a last-position drop;
- all descending and multiple-drop cases;
- negative and arbitrary-size Python integers;
- every permutation, of every length 0 through 5, of
  `[-2, -1, 0, 1, 2]`;
- 300 seed-135 unique integer lists of lengths 0 through 50;
- representative duplicate-free float, string, and tuple arrays.

There were 637 integer cases, 3 exploratory ordered non-integer cases, and zero
mismatches. Exact command, scope, oracle, result, and exit 0 are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log). This is
finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/135-can-arrange`. No candidate-built definition or cache was
copied or reused.

### Concrete definition and execution

Fresh LLVM build:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0:
[`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log).
Warnings concern non-exhaustive supplied-baseline functions unused by this
program (for example float helpers and out-of-bounds indexing).

The concrete assertion program was independently regenerated with the trusted
translator, compared byte-for-byte with the submitted `concrete-tests.mpy`,
and run:

```text
krun regenerated-concrete-tests.mpy --definition runtime-kompiled
```

It reached `.K`, `NoExc`, and exit-code 0; command exit 0:
[`evidence/stage3-concrete-regenerate-and-run.log`](evidence/stage3-concrete-regenerate-and-run.log).

### Proof definition and positive claims

Fresh Haskell build:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0:
[`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log).

Every positive target claim was then run independently:

```text
kprove spec.k --definition verification-kompiled --claims loop-correct
```

Output `#Top`, exit 0:
[`evidence/stage3-kprove-loop-correct.log`](evidence/stage3-kprove-loop-correct.log).

```text
kprove spec.k --definition verification-kompiled --trusted loop-correct
```

Output `#Top`, exit 0:
[`evidence/stage3-kprove-function-correct.log`](evidence/stage3-kprove-function-correct.log).

The second command treats the exact `loop-correct` claim as an available lemma
and proves the only remaining claim. This does not add an unproved candidate
assumption: the same lemma was proved immediately beforehand from the same
`spec.k` against the same freshly built definition.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` says:

- execution is at the real `#loop` over an arbitrary remaining `ValSeq`;
- the loop target and body are the translated target and exact submitted loop
  body;
- the current frame has the submitted function's five locals;
- `index >= 1`, `previous` is an integer, and every remaining element is an
  integer;
- after the suffix is scanned and the real `return result` executes, control is
  at `#pop` and the return cell contains
  `arrangeScan(VS, INDEX, PREVIOUS, RESULT)`.

A concrete satisfying state is `VS = .ValSeq`, `L = 1`,
`ARRAY = list(.ValSeq)`, `OLD_CURRENT = 7`, `INDEX = 1`,
`PREVIOUS = 7`, `RESULT = -1`, `PARENT = parent(0)`,
`OTHER = .Map`, and `ret = noRet`. Its post-summary is `-1`.

`function-correct` says:

- start from the supplied semantics' fresh module configuration;
- load the exact `can_arrange` binding and call it with any finite integer
  `ValSeq`;
- reach a `<k>` result equal to `arrangeResult(VS)`;
- preserve `NoExc` and exit-code 0.

`VS = .ValSeq` is a concrete satisfying entry input; `ints(.ValSeq)` reduces to
true and the result is `-1`.

### Result constraint and concrete substitutions

Ground summary claims for empty, singleton, both documented examples, and a
descending list all returned `#Top`, exit 0:
[`evidence/ground-summary-spec.k`](evidence/ground-summary-spec.k) and
[`evidence/stage4-ground-summaries.log`](evidence/stage4-ground-summaries.log).
Those values also appear in the independent Python differential run.

The end-to-end postcondition is not a free variable or implication: the final
`<k>` value is exactly the recursively defined integer
`arrangeResult(VS)`. `arrangeScan` updates the accumulator to the current index
on every descent and otherwise retains it, so its terminal accumulator is the
largest descent index, or the initial `-1`.

### Mechanical program pinning

Pinning consists of three independent links:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. the complete constructor literal in the reviewer pinning claim is
   mechanically equal to regenerated `solution.mpy` modulo whitespace and the
   parser's two spellings of empty `.Stmts` lists:
   [`evidence/constructor_text_compare.py`](evidence/constructor_text_compare.py),
   [`evidence/stage4-constructor-text-compare.log`](evidence/stage4-constructor-text-compare.log)
   (`434` normalized characters on each side, match true, exit 0);
3. K proves `solutionProgram` and `arrangeBody` equal those exact constructor
   literals:
   [`evidence/pinning-spec.k`](evidence/pinning-spec.k),
   [`evidence/stage4-program-pinning-config.log`](evidence/stage4-program-pinning-config.log)
   (`#Top`, exit 0).

An initial attempt used bare functional claims. The Haskell backend rejected
that unsupported claim shape before executing any claim (exit 113), so it is
not counted as evidence. The diagnostic is preserved in
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log);
the successful configuration-claim replacement is the evidence used.

The immutable candidate does not automatically regenerate `solutionProgram`
from `solution.mpy`; that is an artifact-maintenance observation, not a pinning
failure after the mechanical comparison above.

### Body sensitivity

I changed the executed loop assignment from `result = index` to
`result = index + 1` in a fresh proof source. This changes `arrangeBody` and,
because `solutionProgram` contains that function term, changes the actual
program term executed by the entry claim:

- mutation:
  [`evidence/body-mutated-verification.k`](evidence/body-mutated-verification.k);
- exact diff:
  [`evidence/stage5-body-mutation-diff.log`](evidence/stage5-body-mutation-diff.log);
- clean mutated build: exit 0,
  [`evidence/stage5-body-mutation-kompile.log`](evidence/stage5-body-mutation-kompile.log);
- mutated `[2, 1]` execution reaches result `2`: `#Top`, exit 0,
  [`evidence/body-mutation-ground-spec.k`](evidence/body-mutation-ground-spec.k),
  [`evidence/stage5-body-mutation-ground-result.log`](evidence/stage5-body-mutation-ground-result.log);
- unchanged loop theorem fails with `WarnStuckClaimState`, exit 1, exposing
  `arrangeScan(..., INDEX +Int 1)` versus
  `arrangeScan(..., INDEX)`:
  [`evidence/stage5-body-mutation-loop-expected-failure.log`](evidence/stage5-body-mutation-loop-expected-failure.log).

This is separate from the Stage 6 postcondition mutation.

### Fatal domain mismatch

The formal entry domain is exactly finite `ValSeq`s satisfying `ints(VS)`.
That includes duplicate integer sequences (a sound strengthening beyond the
prompt's uniqueness assumption) but excludes every sequence containing a
string or float.

The exclusion is machine-visible:

```text
ints(vCons(str(S), REST)) => false
ints(vCons(F:Float, REST)) => false
```

Both universal exclusion claims returned `#Top`, exit 0:
[`evidence/domain-exclusion-spec.k`](evidence/domain-exclusion-spec.k) and
[`evidence/stage4-domain-exclusion.log`](evidence/stage4-domain-exclusion.log).

This restriction is not supported by the trusted prompt. In particular,
ordinary finite floats and strings have an unambiguous total order, the arrays
in the test contain no duplicates, and the canonical algorithm uses no
integer-specific operation. The submitted program and supplied semantics
successfully execute:

- `[1.25, -2.5, 3.75, 0.5]`, result `3`;
- `["ant", "bee", "ape", "zebra", "yak"]`, result `4`.

The reviewer program is
[`evidence/out-of-proof-tests.py`](evidence/out-of-proof-tests.py), its trusted
translation is
[`evidence/out-of-proof-tests.mpy`](evidence/out-of-proof-tests.mpy), and the
LLVM K run reaches `.K`, `NoExc`, exit-code 0:
[`evidence/stage4-out-of-proof-k-execution.log`](evidence/stage4-out-of-proof-k-execution.log).
The independent differential test also checks both Python implementations on
these value classes.

This excludes infinite, ordinary source-contract families and is therefore a
material narrowing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/k_rule_inventory.py`](evidence/k_rule_inventory.py) inventories every
local syntax declaration, configuration, context, rule, and claim in the 25
supplied K files plus candidate `verification.k` and `spec.k`. The corrected
complete inventory is
[`evidence/stage5-exhaustive-rule-inventory-v2.log`](evidence/stage5-exhaustive-rule-inventory-v2.log),
exit 0.

Inventory totals:

- 944 records;
- 232 syntax declarations;
- 704 rules (466 equational and 238 `<k>` semantic rules);
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims;
- 109 `total` declarations;
- 45 priority rules;
- 26 `owise` rules;
- 35 concrete rules;
- 25 `symbol` declarations, including 22 `no-evaluators` declarations;
- no local `[simplification]` rule and no local `[functional]` declaration.

There are 928 supplied-baseline records and 16 candidate-local records. The
supplied records are the selected, integrity-checked semantics boundary. The
opaque float, sort, digest, slicing, dictionary, comprehension, and other
unused declarations are not reachable from this submitted program. No
proof-local rule can route execution to them.

### Used constructor-to-semantics map

| Submitted construct | Declaration and material supplied rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module sequencing/load in `core.k:124-127`; closure binding in `functions.k:14-16` |
| Function `Call` | callee/argument evaluation in `call.k:19-21`; frame push in `call.k:69-74`; parameter binding in `functions.k:63-75` |
| `Assign`, `Name` | RHS strictness from `syntax.k`; local write in `controls.k:9-18`; lookup and scope-chain rules in `core.k:130-154` |
| `For` over `list(VS)` | `controls.k:65-74`; list iterator rules `list.k:9-10`; target binding `tuple.k:31-41` |
| nested `If` | strict guard and branches in `controls.k:51-54` |
| `Int`, unary `-` | literal rule `core.k:194`; dispatch `operators.k:10`; integer equation `int.k:7` |
| integer `+` | sequential operand evaluation from `syntax.k`; dispatch `operators.k:12`; equation `int.k:9` |
| comparisons `>` and `<` | comparison contexts/dispatch `operators.k:14-17`; fixed integer rules `int.k:22,24`; guarded proof-local `<` bridge below |
| `Return` | strict return expression and abrupt return rules `functions.k:77-90` |

Evaluation order is the translator order: assignment RHS, for iterable, if
guard, comparison operands, and return expression evaluate before their
consumer. Function entry allocates a scope, parameters and locals bind in that
scope, the list iterator yields in order, and return sets `retV` before
`#pop`. The proof's cells and control suffix match this flow. The loop performs
no heap allocation or external effect on the formal bare-list input.

### Every candidate-local declaration and rule

| Location | Extension | Classification and decision |
|---|---|---|
| `verification.k:8` | `arrangeBody [function]` | Definitional syntax name; no opacity or totality assertion. |
| `verification.k:9` | `arrangeBody => ...` | Exact submitted loop constructor sequence; mechanical pin and body sensitivity pass. |
| `verification.k:18` | `solutionProgram [function]` | Definitional syntax name; does not intercept a call. |
| `verification.k:19` | `solutionProgram => Module(...)` | Exact complete regenerated program after expanding `arrangeBody`; program-defined function still executes. |
| `verification.k:29` | `ints [function,total]` | Structural domain predicate; both `ValSeq` constructors are covered. |
| `verification.k:30` | `ints(.ValSeq) => true` | Correct base case. |
| `verification.k:31` | `ints(vCons(V,R)) => isInt(V) andBool ints(R)` | Correct descending structural equation; disjoint from base. |
| `verification.k:37` | `intValue [function,total]` | A total Int-valued projection. It is arbitrary for non-Ints, but every result-bearing use in these claims is guarded by `isInt`; see bridge validation. |
| `verification.k:38` | `intValue(I:Int) => I` | Exact identity on the complete guarded domain; no overlap. |
| `verification.k:40` | guarded symbolic `applyCmp("<",L,R)` | Operational/equational bridge. On its complete guard both values are Int injections, so `intValue` reduces to the fixed integer operands. It reads/writes no cells and changes no continuation/control effect. |
| `verification.k:47` | `arrangeResult`, `arrangeScan` functions | Transparent mathematical summary; it does not rewrite a program term. |
| `verification.k:49` | initial `arrangeResult` equation | Correctly initializes index 0, previous 0, result -1. |
| `verification.k:50` | empty `arrangeScan` equation | Returns the accumulated latest violating index. |
| `verification.k:51` | recursive `arrangeScan` equation | Consumes one element, increments the absolute index, carries current as previous, and updates exactly on a descent. Guard covers every use under `ints`; recursion strictly descends the tail. |
| `spec.k:9` | `loop-correct` claim | Real loop/body/control suffix; satisfiable; proved independently and body-sensitive. |
| `spec.k:39` | `function-correct` claim | Real program binding/body; exact result; satisfiable; proved using the independently established loop lemma. Its `ints(VS)` restriction is sound but fatally inadequate to the source contract. |

No candidate-local priority, `owise`, simplification, concrete-only, opaque
`no-evaluators`, or unconstrained oracle declaration exists.

### Comparison bridge validation and overlaps

The proof-local `applyCmp` rule overlaps the fixed
`applyCmp("<", I:Int, J:Int) => I <Int J` rule on ground integers. Both
right-hand sides agree because `intValue(I) => I`.

I built a separate Haskell definition importing only the supplied semantics,
with no `verification.k`:
[`evidence/fixed-verification.k`](evidence/fixed-verification.k),
[`evidence/stage5-kompile-fixed-semantics.log`](evidence/stage5-kompile-fixed-semantics.log).
The bridge-free universal claim

```text
Compare(I:Int, CmpOp("<", J:Int)) => I <Int J
```

returned `#Top`, exit 0:
[`evidence/bridge-free-comparison-spec.k`](evidence/bridge-free-comparison-spec.k),
[`evidence/stage5-bridge-free-int-compare.log`](evidence/stage5-bridge-free-int-compare.log).
Int-sorted variables cover the bridge's complete `isInt` guard in the initial
K value algebra.

Ground value-sensitivity witnesses `0 < 1 = true` and `1 < 0 = false` both
returned `#Top`, exit 0:
[`evidence/comparison-value-spec.k`](evidence/comparison-value-spec.k),
[`evidence/stage5-comparison-value-witnesses.log`](evidence/stage5-comparison-value-witnesses.log).
The opposite interpretation `0 < 1 = false` built and failed with a residual
`true`, `WarnStuckClaimState`, exit 1:
[`evidence/comparison-opposite-spec.k`](evidence/comparison-opposite-spec.k),
[`evidence/stage5-comparison-opposite-expected-failure.log`](evidence/stage5-comparison-opposite-expected-failure.log).

There is therefore no concrete or symbolic false-conclusion witness for this
rule on the theorem domain, and it is not labeled unsound.

### Static conclusion

No candidate rule encodes an operational answer, bypasses a program-defined
call, fabricates state, or introduces a result-bearing oracle. `arrangeScan`
appears only as a transparent specification/loop summary; fixed semantics
executes the actual body and the circularity connects that execution to the
summary. All candidate equations have disjoint constructor cases or agreeing
overlaps, covered uses, and structural descent.

The static soundness gate passes for the integer theorem. The defect is intent
domain adequacy, not semantic unsoundness.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k` that was relied on. I created a
fresh ground entry claim for the satisfying input `VS = .ValSeq`, retaining the
real program and fresh initial configuration but mutating the required result
from `-1` to `0`:
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k).

Exact command:

```text
timeout 60s kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

The spec parsed and executed. It reached the actual final `<k>` value `-1`,
then emitted `WarnStuckClaimState` because that value does not unify with
destination `0`; exit status was 1. This was not a parser error, missing import,
timeout, or unrelated crash. Full bounded output:
[`evidence/stage6-false-empty-result.log`](evidence/stage6-false-empty-result.log).

The proof is result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the supplied K semantics and K toolchain, for every finite
`ValSeq` consisting only of K `Int` values, execution from the specified fresh
module state:

1. loads the exact trusted-regenerated submitted `can_arrange` body;
2. calls that binding with `list(VS)`;
3. follows the real assignment, loop, comparison, and return rules;
4. reaches a `<k>` result equal to `arrangeResult(VS)`;
5. leaves exception state `NoExc` and exit-code 0.

The transparent recursion defining `arrangeResult` returns the latest index at
which a strict descent occurs, or `-1`. The proof covers unbounded finite list
lengths and unbounded mathematical integers; it is not a fixed-size unrolling
or finite-example theorem.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler, Haskell reachability backend, builtin Int/Bool/Map/List theory and SMT reasoning | All machine results | Ordinary unavoidable toolchain trust. |
| Integrity-checked supplied MPY semantics | Concrete and symbolic execution | Authorized fixed semantics boundary. Relevant rules were mapped; imported opaque primitives are unreachable in the integer theorem. |
| Trusted `py2mpy.py` translation | Source-to-constructor link | Byte-identical candidate translator and trusted independent regeneration; constructor pinning is mechanical. |
| `--trusted loop-correct` in the function command | Function claim | Acceptable theorem chaining only because the exact claim independently produced `#Top` first against the same fresh definition. |
| `intValue` on non-integer `Val`s | None on the formal entry domain | Arbitrary total projection outside its result-bearing guards. On-domain identity and comparison connection are independently validated. |
| Mathematical reading of transparent `arrangeScan` as “largest descent index” | Human-facing property | Direct structural definition plus finite differential support; testing is not substituted for the K execution proof. |
| Assumption that the prompt intended integer-only arrays | Full requested contract | Unsupported by the trusted prompt and contradicted by ordinary accepted Python/string/float witnesses. This is the fatal limitation. |
| Differential tests | Program/canonical fidelity and domain witnesses | Finite evidence only; not used as a universal K proof. |

### Gate and benchmark decision

- Gate A, real-program soundness: **PASS** for the formal integer domain.
- Gate B, intent adequacy: **FAIL** because `ints(VS)` materially narrows the
  untyped source-contract domain.
- Gate C, trust/evidence auditability: **PASS**; assumptions, commands, inputs,
  and bounded outputs are preserved.
- Kit-style status: **SOUND-BUT-LIMITED**.
- Benchmark mapping: a materially narrowed HumanEval domain is
  **FAIL / NOT_LEGIT**, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
