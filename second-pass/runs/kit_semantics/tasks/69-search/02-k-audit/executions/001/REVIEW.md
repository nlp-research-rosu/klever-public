# Independent adversarial review: HumanEval 69-search

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics. I rebuilt both definitions from source,
proved the claims again, mechanically pinned the whole-program claim to the
trusted regeneration of `solution.mpy`, audited every proof-local extension,
and obtained meaningful failures from fresh body and result mutations.

## 1. Input and provenance integrity

Result: pass; there is no audit-infrastructure breach.

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `69-search`, and condition
`kit-semantics`. The declared container paths resolve to readable mounts. The
trusted `/reference/reference-semantics` tree is present, as required for this
mode.

I read the launcher records and every pipeline-v3 generation record:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- all 399 JSONL records in the one structured trace file under
  `/generation-evidence/codex-trace/`.

The generation report's claims of `#Top`, validation, mutations, and
differential coverage were treated only as untrusted history. None is used as
proof evidence below.

The campaign-lock comparison and mounted-file checks are reproduced by
[`stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`stage1_integrity.log`](evidence/stage1_integrity.log). In particular:

- the SHA-256 of `/audit-campaign-lock.json` is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value recorded in `/audit-input.json`;
- its parsed JSON object equals the `audit_campaign` block exactly;
- the direct hashes of `/run.json`, `/task.json`,
  `/generation-result.json`, all required generation evidence files, the
  trace, and the trusted Python inputs match their recorded hashes;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`cmp` exit 0), and `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (`cmp` exit 0);
- `diff -qr --no-dereference` between candidate and trusted
  `reference-semantics/` exits 0, and a separate entry-type inventory is
  identical. Thus there are no missing, additional, changed, mistyped, or
  symlinked semantics entries;
- no symlink occurs anywhere in `/candidate`, `/reference`, or
  `/generation-evidence`.

The required candidate proof sources—`solution.py`, `solution.mpy`,
`verification.k`, and `spec.k`—are regular readable files. Candidate-provided
compiled definitions were not copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

Result: pass on the full intended domain.

The trusted prompt says: for a non-empty finite list of positive integers,
return the greatest positive integer whose frequency in the list is at least
that integer; return `-1` if none exists. The trusted canonical implementation
computes frequencies and scans all positive values through `max(lst)`.

The submitted implementation instead scans each list element as a candidate,
counts its occurrences with a nested loop, and retains the greatest qualifying
candidate. This is equivalent on the contract domain: every positive integer
with nonzero frequency occurs in the list, while a positive integer absent from
the list has frequency zero and cannot qualify.

In the source-only scratch tree, the command

```text
python3 py2mpy.py solution.py > solution.mpy
```

exited 0. The regenerated and submitted files are byte-identical and both have
SHA-256
`d7712f14ff4383eb242edd097e0bf26e4828c137019b5ff35c3cfb47458cd0cc`.
See [`stage2_program_fidelity.log`](evidence/stage2_program_fidelity.log).

I wrote an independent differential test that imports the trusted canonical
entry point and the submitted implementation separately and also uses an
independent set/count/max contract oracle. The preserved script is
[`differential_audit.py`](evidence/differential_audit.py). It covers:

- all three documented examples;
- frequency just below, equal to, and above a candidate;
- answer-update and no-update ordering boundaries;
- one-element, large-value, and large-length cases;
- every list over values 1 through 6 for lengths 1 through 7;
- threshold cases for values 1 through 50 at counts `v-1`, `v`, and `v+1`;
- 2,000 seeded generated lists of lengths up to 100.

The command ran 338,234 intended-domain cases, corpus SHA-256
`e18dcaa7faecefae98f4ca439236283cd603fcfcf9ce54bec021fb8f407a27e7`,
and reported `mismatch_count=0` with exit 0. On the explicitly tested but
out-of-contract empty list, the canonical raises `ValueError` while the
submitted implementation returns `-1`; this is not a contract-domain
divergence because the prompt requires a non-empty list.

## 3. Clean proof reconstruction

Result: pass.

I copied only candidate-authored source/spec files and the trusted mounted
semantics and Python inputs into `/tmp/audit-work/reconstruction`. No
candidate-provided `runtime-kompiled`, `verification-kompiled`, cache, or
generated binary was copied.

The exact source-only reconstruction is in
[`stage3_reconstruction.sh`](evidence/stage3_reconstruction.sh), with the
bounded transcript in
[`stage3_reconstruction.log`](evidence/stage3_reconstruction.log). The
commands and outcomes were:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
# exit 0

krun concrete_reconstruction.mpy \
  --definition audit-runtime-kompiled
# exit 0; <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
# exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
# exit 0; #Top
```

The independent concrete program is
[`concrete_reconstruction.py`](evidence/concrete_reconstruction.py); it
executes the examples and branch-boundary cases through the trusted LLVM
semantics.

I also ran the positive claims in dependency order using K's fully qualified
claim filters. The transcript is
[`stage3_individual_claims.log`](evidence/stage3_individual_claims.log):

```text
--claims SPEC.inner-loop
# exit 0; #Top

--claims SPEC.inner-loop,SPEC.outer-loop
# exit 0; #Top

--claims SPEC.inner-loop,SPEC.outer-loop,SPEC.search-program
# exit 0; #Top
```

The outer claim legitimately uses the independently closed inner-loop
circularity, and the whole-program claim uses both loop claims. An initial
audit attempt used unqualified filter names, which K rejected as unused; a
second attempt filtered out the inner dependency while retaining the outer
claim and was stopped. Those discarded audit-interface attempts are preserved
with explicit `attempt` names and are not candidate failures or proof evidence.

The compilers emit warnings about unrelated unused variables and
non-exhaustive total functions in portions of the supplied semantics not
reached by this program. The used integer, list, loop, call, and return paths
compile and execute, and no warning changes the reconstructed proof result.

## 4. Adequacy and real-program pinning

Result: pass.

The three claims mean:

| Claim | Precondition | Postcondition |
|---|---|---|
| `inner-loop` | `candidate` is an integer and every value in the remaining list `REM` is a positive integer | the real inner-loop body terminates with `frequency` increased by exactly `frequencyOf(candidate, REM)`; the list, candidate, answer, and heap binding are preserved |
| `outer-loop` | every value in `FULL` and `REM` is a positive integer | the real outer-loop body folds `updateAnswer` over every remaining candidate, producing `searchSummary(REM, FULL, A)` |
| `search-program` | `INPUT` is a non-empty finite `ValSeq` and `allPositive(INPUT)` | loading and calling the submitted function returns exactly `searchSummary(INPUT, INPUT, -1)` and restores the caller environment, empty stack, return state, exception state, and exit code |

The whole-program `<k>` cell contains `#loadAll(Module(FuncDef(...)))`,
followed by `Call(Name("search"), ref(0))`; it does not invoke a replacement
summary rule. The function definition, local initialization, both nested
loops, comparisons, assignments, return, name binding, frame creation, and
frame pop all execute under the fixed supplied semantics.

I extracted the `Module` argument from the whole-program claim, normalized
only three explicit `.Stmts` empty-list spellings to the translator's
equivalent empty fields, parsed both it and the trustedly regenerated
`solution.mpy` with `kast`, and compared their KORE constructor trees. Both
trees have SHA-256
`c4b58e58bdc74bf5a0b23ac62bf4b4c40baf93ad7c24bb65314cc7f4c25d1409`;
`cmp` exits 0. See
[`stage4_program_pinning.log`](evidence/stage4_program_pinning.log) and
[`extract_spec_program.py`](evidence/extract_spec_program.py).

The entry precondition is satisfiable; for example,
`INPUT = vCons(1, .ValSeq)`. The ground K extension checks prove
`allPositive(vCons(1,.ValSeq)) => true`. For the satisfying documented input
`[4,1,2,2,3,1]`, K reduces the claimed summary to `2`, and both trusted
canonical Python and submitted Python return `2`.

The result definition has the intended meaning. `frequencyOf(x,FULL)` is
structural occurrence counting. `updateAnswer(A,x,n)` returns `x` exactly
when `n >= x` and `x > A`, and otherwise returns `A`. Induction over
`searchSummary` therefore maintains the greatest qualifying candidate seen so
far. Since every input value is positive and the initial accumulator is `-1`,
the final result is the greatest qualifying value, or `-1` when the qualifying
set is empty. Repeated occurrences merely revisit the same candidate and
cannot lower the accumulator.

Body sensitivity is independently demonstrated by
[`audit_body_mutation.k`](evidence/audit_body_mutation.k): only the comparison
inside the actual `Module` executed by `search-program` changes from `>=` to
`>`, while the postcondition remains unchanged. The satisfying input `[1]`
then returns `-1` instead of `1`. `kprove` builds the mutation but exits 1 with
`WarnStuckClaimState`; the residual contains the mutated closure body and a
final `-1`. See
[`stage4_body_sensitivity.log`](evidence/stage4_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

Result: pass.

The source-complete inventory is
[`rule_inventory.md`](evidence/rule_inventory.md), generated by
[`rule_inventory.py`](evidence/rule_inventory.py). It records complete source
blocks, source lines, attributes, and whether the source file is on the
submitted path. Across the supplied semantics, `verification.k`, and `spec.k`
it contains:

- 1 configuration, 234 syntax declarations, 5 contexts, 718 rules, and 3
  claims;
- 155 function declarations, 114 `total` declarations, 0 `functional`
  declarations, 23 `no-evaluators`/opaque entries, 45 priority entries, 9
  simplification entries, 37 concrete entries, 27 `owise` entries, and 4
  macro entries.

The submitted syntax-to-semantics mapping is complete:

| Used construct | Declaration and execution rules |
|---|---|
| `Module`, statement sequences | `syntax.k:61`; `core.k:124-127` |
| integer literals and unary `-` | `syntax.k:9,14`; `core.k:194`; `int.k:7` |
| `Name` and local binding | `syntax.k:12`; `core.k:130-154`; `controls.k:9-18`; `tuple.k:31-41` |
| `BinOp("+",...)` | `syntax.k:15`; `operators.k:12`; `int.k:9` |
| `Compare` with `==`, `>=`, `>` | `syntax.k:30,32`; `operators.k:14-17`; `int.k:24-26` |
| `If` | `syntax.k:49`; `controls.k:50-54` |
| `For` over the input list | `syntax.k:45`; `controls.k:62-74,104-108`; `list.k:9-10`; target binding in `tuple.k:31-41` |
| `FuncDef`, `Call`, parameter binding | `syntax.k:28,53`; `functions.k:14-20,63-75`; `call.k:18-21,69-75` |
| `Return` and call-frame pop | `syntax.k:50`; `functions.k:77-90` |

Strictness and contexts give the required evaluation order: assignment
evaluates its RHS, `For` evaluates the iterable once, binary operators evaluate
left then right, comparisons evaluate left then right, and the call layer
evaluates the callee and arguments before dispatch. The loop rules consume the
list in order and bind each yielded value before the body. The function-call
rules allocate a fresh local scope, push the exact continuation, bind `lst`,
execute the body, and restore all caller/control cells on `#pop`. The program
does not mutate its input list, allocate objects during the call, perform I/O,
or raise an exception on the precondition, so the supplied semantics'
snapshot-list iteration is adequate here.

The candidate contributes 7 proof-local syntax declarations and 23 rules:

| Extension group | Classification and audit |
|---|---|
| `isIntVal`, `definedProjectInt`, and their three equations (`verification.k:10-15`) | Definitional sort test. The `Int` case and `owise` complement are disjoint and exhaustive over `Val`; no state or control is affected. |
| `projectIntTotal`, cast definedness/orientation, identity, and idempotence (`verification.k:17-34`) | Definitional totalization of the existing `Val :> Int` projection. On the only admitted domain, `isIntVal(V)`, it is fixed to the underlying integer. Its value outside that guard is unspecified but no target-dependent rule uses it there. It is pure and does not replace a program operation. |
| four guarded `applyCmp`/`applyBin` simplifications (`verification.k:39-57`) | Derived integer-dispatch lemmas. When both operands satisfy `isIntVal`, their right-hand sides are exactly the fixed `MPY-INT` operations. On overlap with fixed concrete rules, both sides agree. They affect values but not control or state, and they do not intercept a `<k>` computation. |
| `allPositive` (`verification.k:60-65`) | Transparent structural precondition. Empty is true; a cons requires an integer greater than zero and recursively checks the tail. |
| `frequencyOf` (`verification.k:68-76`) | Transparent structural occurrence count. The integer/non-integer guards are complementary; recursion strictly descends the sequence. |
| `updateAnswer` (`verification.k:79-85`) | Transparent one-step maximum update. The three integer guards are pairwise disjoint and exhaustive: qualifying/larger, below frequency threshold, and qualifying/not larger. |
| `searchSummary` (`verification.k:88-107`) | Transparent structural fold. The integer/non-integer guards are complementary and recursion strictly descends. On `allPositive` inputs only the exact integer branch is reachable. |

There are no candidate-local priority rules, ordinary operational rewrites,
frame/control bridges, exception rules, or heap/state rules. In particular,
there is no rule of the form “program invocation rewrites to summary”; the
summary is reached only through the proved loop claims and fixed execution.
There is also no circular opaque oracle shared between execution and the
postcondition.

The 23 inventoried opaque/no-evaluator entries include fixed-semantics
facilities for floats, sorting, and MD5 that are unreachable from
`solution.mpy`. The only candidate-local opaque declaration is the guarded
integer projection just discussed. Thus no unused fixed opaque primitive
influences a branch, result, state cell, exception, or proof obligation for
this program.

Ground value checks in
[`extension_ground.k`](evidence/extension_ground.k) close with `#Top` for
integer recognition/projection, all four dispatch operations, a satisfiable
precondition, all three update branches, frequency counting, and the
documented summary result. Exact opposite interpretations in
[`extension_false.k`](evidence/extension_false.k)—`projectIntTotal(1)=2`,
`1+2=4`, and the documented summary being `3`—all exit 1 with
`WarnStuckClaimState` and residual values `1`, `3`, and `2`, respectively.
See
[`stage5_extension_witnesses.log`](evidence/stage5_extension_witnesses.log).

No inventoried candidate rule was found unsound, so there is no unsoundness
allegation requiring a false-conclusion witness. Compiler warnings on
out-of-path supplied functions identify limitations of the fixed trusted
subset, not a rule used to establish this theorem.

## 6. Fresh non-vacuity test

Result: pass.

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation
[`audit_false_result.k`](evidence/audit_false_result.k):

- fixes the satisfiable input to `vCons(1,.ValSeq)`;
- leaves the exact executed program unchanged;
- replaces the correct whole-program result
  `searchSummary(INPUT,INPUT,-1)` with the false result `0`.

The exact `kprove` command is in
[`stage6_nonvacuity.sh`](evidence/stage6_nonvacuity.sh). It parses and builds
successfully, then exits 1 with `WarnStuckClaimState`. The residual in
[`stage6_false_result_bounded.log`](evidence/stage6_false_result_bounded.log)
contains the complete final configuration with `<k> 1 ~> .K </k>`, so the
failure is the expected unmet result obligation—not a parser error, timeout,
missing import, unrelated crash, or unreachable mutation. The wrapper records
`stage6_nonvacuity_exit=0` after verifying the expected nonzero proof exit and
absence of `#Top`.

## 7. Proven versus assumed accounting

The successful K reachability proof establishes the following:

> Under the supplied `MPY` semantics, for every non-empty finite `ValSeq` whose
> elements are positive integers, if the exact submitted `search` execution
> terminates from the claim's initial state, it returns
> `searchSummary(INPUT,INPUT,-1)` with no exception and with the pinned caller,
> stack, heap, return, and exit-code state. The transparent summary equals the
> greatest positive input integer whose frequency is at least its value, or
> `-1` if none qualifies.

The proof is symbolic over arbitrary finite list length and arbitrary positive
integer values. It is not a finite-size unrolling.

Trust and evidence ledger:

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Byte-identical supplied `reference-semantics/` | Defines all program execution and cells for every claim | Accepted benchmark trust boundary. It was rebuilt from trusted source; all used constructs were audited. |
| K v7.1.293 frontend, LLVM backend, Haskell backend, and backend arithmetic/SMT | Parses, compiles, executes, and closes the reachability claims | Accepted toolchain trust boundary. Candidate compiled artifacts were excluded. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Accepted after byte identity of the translator and byte identity of trusted regeneration. |
| Proof-local `projectIntTotal` outside `isIntVal` | A total but unspecified integer for non-integer `Val` inputs | Acceptable and non-influential: every result-bearing use is guarded, and the theorem precondition makes all list elements integers. |
| Structural-summary-to-contract induction | Explains why the exact fold is the greatest qualifying value or `-1` | Accepted ordinary mathematics. It uses the complete, terminating equations; it is not an empirical oracle or an assumed program execution. |
| CPython canonical/implementation and independent differential oracle | Finite evidence for implementation-to-contract agreement | Supporting evidence only. It does not replace any K claim or universal connection. |
| Generation logs, candidate `PROOF.md`, prior builds, and candidate mutation logs | Historical candidate claims | Not trusted and not used in the decision. |

Gate A passes: the real program executes; proof-local rules are value-correct,
guarded, and non-operational; the theorem is result-constraining; body and
opposite-value probes are rejected. Gate B passes: the formal precondition is
exactly the full HumanEval domain—non-empty finite positive-integer lists—with
no bound on length or values, and the exact result matches the source
contract. Gate C passes: reconstruction, identity, differential, inventory,
ground/opposite, body-sensitivity, and fresh non-vacuity artifacts are
independently reproducible below `/audit-output/evidence/`.

Excluded behavior is explicit: empty lists, non-positive or non-integer
elements, Python behavior outside the supplied language subset, resource
bounds, and a separate liveness theorem. None narrows the HumanEval contract.

VERDICT: PASS
LEGITIMACY: LEGIT
