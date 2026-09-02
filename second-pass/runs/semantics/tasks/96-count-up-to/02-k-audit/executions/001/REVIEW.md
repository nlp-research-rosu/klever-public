# Independent adversarial audit: 96-count-up-to

Decision: **CONCERNS / LEGIT**. The proof reconstructs cleanly, constrains the
returned list, and its proof-local rules are sound on the complete domains in
which they are used. The concerns are auditability limitations rather than a
false theorem: the candidate omits all named generation-provenance artifacts,
and the formal entry claims begin at the exact function-body invocation state
rather than symbolically loading the submitted `Module(FuncDef(...))` and
calling its exported name. Byte-identity, exact body comparison, concrete K
execution, and differential testing support that last bridge, but the candidate
does not state it as a top-level reachability claim.

All candidate files were treated as untrusted and read-only. Sources used for
execution were copied to `/tmp/audit-work/96-count-up-to`; no candidate-built
definition or cache was used. The evidence command logs record the working
directory, exact argv, exit status, and bounded output.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists. Therefore
there is no infrastructure breach and a candidate verdict is appropriate.

The candidate is missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured trace recognizable by a `*trace*` or `*.jsonl` filename

This is recorded in
[02_stage1_integrity.log](/audit-output/evidence/02_stage1_integrity.log).
Because those files do not exist, there were no untrusted claims in them to
inspect. Their absence limits provenance and is one reason for `CONCERNS`; it
does not alter the independently reconstructed K result.

All core submitted sources are regular files. The top-level
`.proof-build.PW4J5z/` and `__pycache__/` directories are candidate-generated
build/cache evidence and were ignored. The candidate's `prompt.py` and
`py2mpy.py` are byte-identical to the trusted mounted versions:

- prompt SHA-256:
  `87a89ca2716858e3f17b04c2b3a30af694d0daa68da3e197f801a408d3b6bfb5`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The recursive, no-dereference comparison between
`/candidate/reference-semantics/` and
`/reference/reference-semantics/` found no missing, additional, changed, or
mistyped entry. Neither tree contains a symlink or another non-file/non-directory
entry. Thus the candidate uses exactly the supplied semantics; that integrity
result does not bless anything in `verification.k`. See
[02_stage1_integrity.log](/audit-output/evidence/02_stage1_integrity.log) and
[03_stage1_hashes_and_copy.log](/audit-output/evidence/03_stage1_hashes_and_copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a non-negative integer `n`, return the increasing
list of every prime integer strictly less than `n`. Hence `0`, `1`, and `2`
return `[]`; `3` returns `[2]`; and the documented examples include
`5 -> [2,3]`, `11 -> [2,3,5,7]`, and
`20 -> [2,3,5,7,11,13,17,19]`.

The trusted canonical implementation scans each `i` in `[2,n)`, tests divisors
in `[2,i)`, and appends `i` exactly when none divides it. The submitted
[solution.py](/candidate/solution.py:1) is a different but equivalent while-loop
implementation. It starts at candidate 2, scans every divisor from 2 to
`candidate - 1`, leaves `is_prime` false after any divisor is found, conditionally
appends the candidate, then increments the candidate and resets the divisor
state. Its outer guard is `candidate < n`, so the result contains no value at
or above `n`.

Running the trusted translator over the scratch copy of `solution.py` produced
a file byte-identical to submitted `solution.mpy`. Both hashes are
`b7281d4d4cfc59b4bbfc0642162bd813928025a7a4858c8abea1730fda9486d4`,
and `cmp` exited 0. The regenerated artifact is
[solution.regenerated.mpy](/audit-output/evidence/solution.regenerated.mpy);
the exact command and comparison are in
[09_translation_identity.log](/audit-output/evidence/09_translation_identity.log).

The independent
[differential_test.py](/audit-output/evidence/differential_test.py) imports
`/reference/canonical.py` and the scratch copy of generated `solution.py` as
separate modules. It checked every integer from 0 through 150, selected values
through 400, a deterministic random sample, and all documented examples: 179
distinct intended-domain inputs in total. There were zero mismatches. The
complete input list, oracle paths, command, exit 0, and result are preserved in
[11_differential_python_final.log](/audit-output/evidence/11_differential_python_final.log).
This is finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

Tooling was independently available as K `v7.1.337`; no installation or
candidate tool wrapper was needed. See
[01_toolchain.log](/audit-output/evidence/01_toolchain.log).

The concrete LLVM definition was rebuilt from the scratch copy of the supplied
semantics with main module `MPY-KRUN`. `kompile` exited 0. Its warnings concern
non-exhaustive supplied-semantics helper functions on types unused by this
program; they did not prevent construction. The build record is
[13_kompile_concrete.log](/audit-output/evidence/13_kompile_concrete.log).

The reviewer-authored
[concrete_tests.py](/audit-output/evidence/concrete_tests.py) contains the exact
submitted function body and assertions for `n = 0,1,2,3,4,5,6,11,20`. It was
transliterated with the trusted translator to
[concrete_tests.mpy](/audit-output/evidence/concrete_tests.mpy). Fresh `krun`
execution ended with `.K`, `NoExc`, and exit code 0; the heap includes the
expected returned sequences. See
[12_concrete_test_translation.log](/audit-output/evidence/12_concrete_test_translation.log)
and [14_krun_concrete.log](/audit-output/evidence/14_krun_concrete.log).

Three separate Haskell definitions were then rebuilt from source so that each
lemma was proved only with the intended earlier layer:

| Target | Proof definition | Fresh result |
|---|---|---|
| inner divisor-loop claim | `COUNT-UP-TO-BASE` (no loop bridge) | exit 0, `#Top` |
| outer candidate-loop claim | `COUNT-UP-TO-WITH-INNER` | exit 0, `#Top` |
| both entry claims | `COUNT-UP-TO-WITH-OUTER` | exit 0, `#Top` each |

The build logs are
[15_kompile_inner_proof.log](/audit-output/evidence/15_kompile_inner_proof.log),
[17_kompile_outer_proof.log](/audit-output/evidence/17_kompile_outer_proof.log),
and
[19_kompile_entry_proof.log](/audit-output/evidence/19_kompile_entry_proof.log).
The four independent positive proof logs are:

- [16_kprove_inner.log](/audit-output/evidence/16_kprove_inner.log)
- [18_kprove_outer.log](/audit-output/evidence/18_kprove_outer.log)
- [20_kprove_entry.log](/audit-output/evidence/20_kprove_entry.log)
- [21_kprove_boundary.log](/audit-output/evidence/21_kprove_boundary.log)

Each has both required success signals: process exit 0 and literal `#Top`.
[40_evidence_status_summary.log](/audit-output/evidence/40_evidence_status_summary.log)
summarizes those signals. No candidate-provided compiled definition, cache,
`#Top`, or trace contributed to these runs.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the four claims

1. **Inner divisor loop.** The precondition has integer
   `2 <= D <= C`, candidate `C`, divisor `D`, incoming Boolean `B`, the standard
   local bindings, and an existing result list. Executing the actual inner
   `#while` advances `divisor` to `C` and changes `is_prime` to
   `B and noDivisor(C,D,C)`. It leaves the continuation, result heap, and other
   bindings framed.

2. **Outer candidate loop.** The precondition has
   `2 <= I <= N`, candidate `I`, `is_prime = true`, `divisor = 2`, and result
   sequence `VS`. Executing the actual outer loop advances candidate to `N`,
   resets the two scratch variables, and changes the result to
   `primesAcc(VS,I,N)`.

3. **Entry for `N >= 2`.** The precondition is the real function-call body
   state: local frame 1 binds only `n = N`, heap and heap location are empty/0,
   the stack contains the caller frame, and `ret`/`exc` are normal. The `<k>`
   cell contains the exact submitted body statement sequence followed by
   `#endcall`. The postcondition returns `ref(0)` and constrains heap location 0
   to `list(primesAcc(.ValSeq,2,N))`, with the callee frame popped.

4. **Boundary for `0 <= N < 2`.** The precondition is the same exact body
   invocation state. The outer loop is skipped, and the returned heap object is
   exactly `list(.ValSeq)`.

The two entry preconditions cover every non-negative K integer without a gap:
`0 <= N < 2` or `N >= 2`. They exclude negative integers and non-integer Python
values, exactly as the prompt's intended domain does.

The statement sequence in both entry claims matches
[solution.mpy](/candidate/solution.mpy:3) constructor-for-constructor after K's
empty-list notation is made explicit (`ListExpr()` versus
`ListExpr(.Exprs)`). The helper claims match the two actual `While` bodies,
including the divisor test, in-place list append, increments, and resets.
There is no substituted algorithm inside the claims.

The formal result is not a free value or a one-way implication.
`primesAcc(.ValSeq,2,N)` is constrained by terminating equations to append
exactly those `I` for which `noDivisor(I,2,I)` holds. For `I >= 2`, that is
ordinary mathematical primality: no integer from 2 through `I-1` divides `I`.

Satisfiable witnesses include:

- inner claim: `C=5,D=2,B=true` (outgoing true), and
  `C=6,D=2,B=true` (outgoing false);
- outer claim: `VS=[],I=2,N=5`, producing `[2,3]`;
- main entry: `N=5`;
- boundary entry: `N=0`.

[claim_witness_test.py](/audit-output/evidence/claim_witness_test.py) evaluates
the formal summary equations on ground terms and compares them with both Python
implementations. For `N=0,1,2,3,5,11,20`, all three values agree; see
[26_claim_witnesses.log](/audit-output/evidence/26_claim_witnesses.log).

The remaining pinning limitation is explicit: the candidate entry claims begin
after the supplied call semantics has created frame 1. They do not themselves
start from `#loadAll(Module(FuncDef(...)))` and prove name resolution plus the
top-level call. This is not an execution-bypassing rule—the exact body and
exact call-frame lifecycle execute, and fresh concrete K tests exercise
definition, lookup, call, return, and pop—but the universal source-file-to-entry
connection is established by exact syntactic inspection rather than by a
candidate auxiliary reachability claim. This limitation supports `CONCERNS`,
not `FAIL`, because no alternate binding or body is admitted by the actual
entry precondition.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and fixed semantics

The complete machine-generated inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md), produced by
[build_k_inventory.py](/audit-output/evidence/build_k_inventory.py). It covers
all 26 K files and inventories 944 source-located blocks:

- 230 syntax declarations;
- 704 rules;
- 5 contexts;
- 1 configuration;
- 4 claims.

It also classifies every `[function]`, `[total]`, `[symbol]`,
`[no-evaluators]`, `[concrete]`, `[priority]`, `[owise]`, strictness, and macro
attribute. The summary and exact generating command are in
[25_build_rule_inventory_final.log](/audit-output/evidence/25_build_rule_inventory_final.log).

Every entry under `reference-semantics/` is classified as part of the fixed,
trusted supplied-semantics level because the tree is byte-identical to the
trusted mount. Unused baseline rules are not silently promoted to candidate
lemmas. The proof-relevant path through that baseline is:

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, statement lists | `syntax.k`; `core.k` `#loadAll` and sequential statement rules |
| `FuncDef`, `Params`, `Return` | `functions.k` closure installation, binding, return and frame-pop rules |
| `Call`, `Attribute(...,"append")` | `call.k` callee-before-arguments routing; bound-method dispatch |
| `Name`, `Assign`, `AugAssign` | `core.k` lexical lookup; `controls.k` current-scope updates |
| `ListExpr()` and `append` | `list.k` left-to-right element evaluation, `#alloc`, and in-place heap update |
| `While`, `If`, `Expr` | `controls.k` condition evaluation, truthiness branch, loop continuation, discard |
| `BinOp("%",...)`, `BinOp("+",...)` | sequential operand strictness, `int.k` `pyMod` and integer addition |
| integer comparisons | ordered `Compare` contexts and `int.k` `<`/`==` rules |
| `Int`, `Bool` | `core.k` literal rules |

The fixed configuration starts at module environment 0, uses a real scope map,
monotonic heap allocation, an explicit call stack, `ret`, and `exc` cells.
Assignment evaluates its RHS first; `BinOp` evaluates left then right; `Compare`
evaluates left then its wrapped right; calls evaluate callee then arguments;
`While` re-evaluates its condition each iteration. The proof entry state and
post-state account for the list allocation, in-place append writes, local
binding mutations, return value, frame deallocation, environment restoration,
and heap escape. Complete listings of the relevant fixed modules are preserved
as the `23_semantics_*.log` files under `/audit-output/evidence/`.

The proof imports `MPY`, not `MPY-CONCRETE`. Concrete-only deep equality is used
only in the independent assertion run. No float, sort, MD5, dict, set,
subscript, comprehension, range, or string result can enter this program's
sort-correct execution path.

### Candidate-local declaration and rule decisions

There are three local syntax declarations and nine local rules in
[verification.k](/candidate/verification.k:9). There are no local
`[simplification]` or `[functional]` declarations.

1. `noDivisor(C,D,HI)` is `[function,total,symbol,no-evaluators]`.
   - `D >= HI -> true` is the correct empty-interval case.
   - `D < HI` and `pyMod(C,D)==0 -> false` correctly detects a divisor.
   - `D < HI` and nonzero remainder recurses at `D+1`; it strictly descends on
     `HI-D`.
   - The guards are disjoint and cover every proof use, because every claim
     enforces `D >= 2`. The declaration is over-broad as a globally total
     `Int^3` function: at `D=0<HI`, the supplied `pyMod(C,0)` has no ordinary
     divisor meaning. No candidate claim or promoted rule can reach that case,
     and there is no false-conclusion witness on the intended domain. I
     therefore record a narrow out-of-domain totality gap, not an unsound rule.

2. `appendIfPrime(VS,I,Bool)` is fully and disjointly defined:
   `false -> VS`; `true -> VS ++ [I]`. Both equations are ordinary list
   mathematics.

3. `primesAcc(VS,I,N)` has disjoint guards `I>=N` and `I<N`. The former returns
   `VS`; the latter uses `appendIfPrime` and recurses at `I+1`. The recursion
   terminates for all integer `I,N` and exactly defines the intended increasing
   sequence.

4. The inner priority-40 rule is an operational bridge over the exact submitted
   divisor loop. It reads the pinned local bindings, writes only `divisor` and
   `is_prime`, preserves the heap and trailing computation, and uses the
   fully-defined `noDivisor` value.

5. The outer priority-40 rule is an operational bridge over the exact submitted
   candidate loop. It reads/writes the pinned local bindings, mutates only the
   existing result list in heap location 0, and summarizes it with the
   fully-defined `primesAcc`. It does not fabricate allocation, return, stack,
   exception, or frame behavior.

The promoted rules omit `scopeLoc`, `heapLoc`, `stack`, `ret`, `exc`, and
`exit-code`, while the candidate's original lemma claims explicitly pin most of
those cells. To test that apparent context generalization rather than assume it
safe, the reviewer created
[bridge-validation.k](/audit-output/evidence/bridge-validation.k):

- a bridge-free universal inner connection claim imports only
  `COUNT-UP-TO-BASE` and copies the promoted inner rule's complete match domain;
- a universal outer connection claim imports the independently validated inner
  layer but not the proposed outer bridge;
- both quantify over arbitrary trailing K and leave exactly the cells omitted
  by the promoted rules unconstrained.

Both universal connection claims exit 0 with `#Top`:
[27_kprove_inner_full_bridge_domain.log](/audit-output/evidence/27_kprove_inner_full_bridge_domain.log)
and
[28_kprove_outer_full_bridge_domain.log](/audit-output/evidence/28_kprove_outer_full_bridge_domain.log).
Ground fixed-versus-extended witnesses with an immediate observable
`n := 99` continuation also agree for both bridges; all four runs close with
`#Top` in logs
[29](/audit-output/evidence/29_inner_context_fixed.log),
[30](/audit-output/evidence/30_inner_context_extended.log),
[31](/audit-output/evidence/31_outer_context_fixed.log), and
[32](/audit-output/evidence/32_outer_context_extended.log).
This establishes context containment, state-footprint preservation, and
continuation fidelity over the actual promoted domains.

Operational body sensitivity was tested separately with
[bridge-body-sensitivity.k](/audit-output/evidence/bridge-body-sensitivity.k).
It changes the divisor-hit assignment from `false` to `true` while retaining
the original `[2,3]` obligation at `N=5`. The mutation builds successfully, the
exact bridges do not match it, and the proof exits 1 with
`WarnStuckClaimState`; the residual heap is concretely `[2,3,4]`. See
[33_bridge_body_sensitivity_dry_run.log](/audit-output/evidence/33_bridge_body_sensitivity_dry_run.log)
and
[34_bridge_body_sensitivity_expected_failure.log](/audit-output/evidence/34_bridge_body_sensitivity_expected_failure.log).

No candidate-local rule was found that encodes an unconstrained task answer,
replaces program-derived behavior with an oracle, bypasses a mismatched body,
or enables a false conclusion on the intended domain. Consequently there is no
unsoundness allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

The candidate has no `spec-vacuity.k`; its absence is recorded in
[36_vacuity_artifact_check.log](/audit-output/evidence/36_vacuity_artifact_check.log).
The fresh reviewer mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It leaves the exact
entry execution unchanged but changes the result-bearing postcondition from
`primesAcc([],2,N)` to `primesAcc([],3,N)`. This is demonstrably false at the
satisfying input `N=3`: the real and canonical results are `[2]`, while the
mutated summary is `[]`.

The mutated spec builds successfully: `kprove --dry-run` exits 0 and emits the
backend command, as recorded in
[37_vacuity_dry_run.log](/audit-output/evidence/37_vacuity_dry_run.log). The
actual proof exits 1 with `WarnStuckClaimState`. Its residual is the expected
failed implication
`primesAcc(.ValSeq,2,N) #Equals primesAcc(.ValSeq,3,N)` under `N >= 2`, not a
parse error, missing import, timeout, or unrelated crash. See
[38_vacuity_expected_failure.log](/audit-output/evidence/38_vacuity_expected_failure.log).
The proof is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics, for every K integer `N` in the stated exact
function-body invocation configuration:

- if `N >= 2` and execution terminates, it returns a reference to a heap list
  equal to the incoming empty list followed, in increasing order, by each
  integer `I` with `2 <= I < N` for which no integer `D` with
  `2 <= D < I` divides `I`;
- if `0 <= N < 2` and execution terminates, it returns a reference to the empty
  list;
- the call frame is popped, the caller environment and scope allocator are
  restored, no exception is introduced, and the returned list remains in the
  heap.

This is partial correctness. The K claims do not constitute a separate
termination theorem, even though the concrete program's two integer loop
variants plainly decrease (`C-D` and `N-I`) on the guarded domains.

### Trust ledger

1. **Supplied MPY semantics.** The exact trusted reference tree defines syntax,
   evaluation order, environments, heap allocation, lists, calls, and returns.
   This is the selected semantics-level trust boundary. It is acceptable by the
   audit condition and was integrity-checked recursively.

2. **K implementation and built-in theories.** `kompile`, `kprove`,
   `kore-exec`, LLVM execution, SMT implication checking, and K's Int, Bool,
   Map, List, String, and equality hooks are trusted. Every reconstructed claim
   depends on this ordinary machine-checking boundary.

3. **Positive-divisor modular arithmetic.** `pyMod` is supplied semantics.
   Candidate uses it only at divisors at least 2. Its connection to ordinary
   divisibility and the elementary theorem “an integer `I>=2` is prime iff no
   `D` in `[2,I)` divides it” are informal mathematics, transparent but not
   separately formalized as a K `prime` theorem.

4. **Candidate-local result symbols.** `noDivisor`, `appendIfPrime`, and
   `primesAcc` carry `symbol`/`no-evaluators`, but they are not opaque oracles:
   their ordinary K equations are available to `kprove`, disjoint and covering
   on every proof use, and their values flow into both loop summaries and the
   final heap postcondition.

5. **Imported opaque/concrete-only symbols.** The supplied proof definition
   declares `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`,
   `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
   `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
   `truncF`, `roundF`, `roundFN`, `sqrtF`, and `md5hexCodes` as symbols whose
   proof behavior is partly or wholly opaque/concrete-only. The exhaustive
   locations are in
   [41_symbol_trust_ledger.log](/audit-output/evidence/41_symbol_trust_ledger.log).
   None can occur in the submitted integer/list program or its claims, so none
   influences control, state, return value, or postcondition.

6. **Translator/source bridge.** `/reference/py2mpy.py` is trusted by the audit
   input boundary. Its output is byte-identical to the submitted `.mpy`. The
   exact function-body constructors were compared to the claims. This is strong
   syntactic evidence, but the candidate does not machine-check that comparison
   inside K.

7. **Top-level binding bridge.** The supplied definition/call rules and
   concrete K runs support the transition from the submitted
   `Module(FuncDef(...))` to the exact invocation configuration used in the
   theorem. The candidate has no symbolic auxiliary claim for that top-level
   transition. This is the principal theorem-pinning limitation, but it does
   not create an alternate body or unconstrained return.

8. **Empirical evidence.** The 179-input differential run and nine-input
   concrete K run support Python/MPY fidelity on their recorded inputs only.
   Neither substitutes for the universal K reachability claims or the
   bridge-free loop validation.

The formal intent matches the natural-language task on non-negative integers,
the reconstructed proof is discriminating, and no materially unsound
candidate extension was found. Missing provenance and the absent top-level
symbolic load/call claim prevent a clean `PASS`, but neither invalidates the
legitimate body-level partial-correctness proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
