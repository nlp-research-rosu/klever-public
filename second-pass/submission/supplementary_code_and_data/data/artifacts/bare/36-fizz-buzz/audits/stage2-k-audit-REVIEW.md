# Independent adversarial audit: 36-fizz-buzz

This review treats every candidate artifact and generation record as untrusted
evidence. I followed the mandated `using-kit` → `validating-proof` workflow and
the `writing-semantics` checks required by `GENERATED_SEMANTICS`. All execution
used source-only copies under `/tmp/audit-work/36-fizz-buzz-audit-002`; no
candidate-compiled definition or cache was copied or reused.

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, problem `36-fizz-buzz`, and
`semantics_mode = GENERATED_SEMANTICS`. Its `container_paths` resolve to the
mounted inputs used here. `/audit-campaign-lock.json` is a real regular file,
its SHA-256 is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and its parsed object is exactly equal to the `audit_campaign` block.
`/audit-prompt.md` also has the campaign-declared prompt hash.

I read the required legacy-selected-stage1 records: `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete structured
trace. The one JSONL trace contains 143 parseable records. I also inspected the
present legacy records. Historical runtime metrics are not required for this
layout and were not reconstructed. The generation claims `KPROVE_PASSED`; that
claim was not used as proof evidence.

All required records and candidate deliverables are regular, non-symlinked
entries. Every launcher-declared direct file hash independently recomputed to
the recorded value. The complete per-entry candidate and trace hashes are in
`evidence/stage1/provenance_check.log`; the independent checker is
`evidence/stage1/provenance_check.py`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. As required by generated
semantics mode, neither `/reference/reference-semantics` nor a candidate
`reference-semantics` exists. There is therefore no supplied-semantics
integrity comparison and no hidden baseline was inferred.

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted contract in `/reference/prompt.py:3` asks `fizz_buzz(n)` to return
the total number of decimal digit occurrences of `7` among nonnegative
integers below `n` that are divisible by 11 or 13. The documented results are
`0` at 50, `2` at 78, and `3` at 79. The trusted canonical implementation
(`/reference/canonical.py:7`) filters `range(n)`, concatenates the decimal
representations, and counts matching characters.

The candidate `/candidate/solution.py:1` uses a different but equivalent
algorithm: it scans `i` from zero while `i < n`; for qualifying values it
repeatedly removes the final decimal digit and increments the count when that
digit is seven. Empty and negative ranges execute no loop, matching Python
`range(n)`.

The trusted translator regenerated `solution.py` with exit 0. The regenerated
file and submitted `/candidate/solution.mpy` are byte-identical, both with
SHA-256
`19e2e2121b4f89efdc54d5e6cd45db27f2a50ad2788d7f4471088778dd5706d2`.
See `evidence/stage2/regenerate_check.sh` and
`evidence/stage2/regenerate_check.log`.

The independent differential imports the trusted canonical and candidate entry
points from separate paths. Its exact deterministic input set is preserved in
`evidence/stage2/differential_inputs.json` (SHA-256
`8f18a74a4379703c97976c0a336f01691e6e708a9f9dcfac4f60b083eea31a4f`).
It covers the examples, negatives, zero/empty iteration, divisibility and
digit-7 transition boundaries, every integer from -25 through 2000, seeded
larger values, and neighbors of larger qualifying numbers. All 2,206 inputs
matched. See `evidence/stage2/differential_test.py` and `.log`. This finite
evidence supports fidelity; it is not substituted for the universal K proof.

## 3. Clean proof reconstruction

Status: PASS.

The observed toolchain is K 7.1.293, matching the campaign lock
(`evidence/stage3/toolchain.log`). From the scratch source copy I built two
fresh Haskell definitions:

- Concrete: `kompile semantic.k --main-module SEMANTIC --syntax-module
  MPY-SYNTAX --backend haskell --output-definition concrete-kompiled`
  (`evidence/stage3/build_concrete.log`, exit 0).
- Proof: `kompile verification.k --main-module VERIFICATION --syntax-module
  MPY-SYNTAX --backend haskell --output-definition proof-kompiled`
  (`evidence/stage3/build_proof.log`, exit 0).

The original unmodified three-claim specification was then run with:

`kprove spec.k --definition proof-kompiled --spec-module SPEC`

It exited 0 and printed exactly `#Top`
(`evidence/stage3/kprove_all.log`).

I added labels only in a reviewer copy to invoke target claims with their
explicit dependency prefixes. The inner claim alone printed `#Top`; inner plus
outer printed `#Top`; inner plus outer plus entry printed `#Top`. These are
separate `kprove` invocations in `kprove_inner.log`,
`kprove_outer_with_inner.log`, and
`kprove_entry_with_invariants.log`. The outer claim intentionally uses the
inner circularity, and the entry uses both loop circularities. An extra
outer-without-inner diagnostic was interrupted by a ten-second timeout and is
recorded in `kprove_outer_isolated_diagnostic.log`; it is not a required proof
run and is not used as a verdict signal.

For generated-semantics validation, clean `krun` executions were compared with
both Python implementations at `N = -3, 0, 1, 11, 13, 77, 78, 79, 117, 178,
777`. All commands exited 0 and all 11 results matched. In particular, the
semantics reproduced the 77/78 boundary jump from 0 to 2, returned 3 at 79,
and returned 37 at 777. Exact subcommands, exits, and values are in
`evidence/stage3/concrete_compare.py` and `.log`.

## 4. Adequacy and real-program pinning

Status: PASS.

The three claims in `/candidate/spec.k` say:

1. Inner loop (`spec.k:8`): from an exact four-binding environment and any
   `X >= 0`, executing the real inner loop before arbitrary `REST` reaches that
   same `REST`, leaves `i` and `n` unchanged, sets `x` to zero, and increases
   `count` by `digitSevens(X)`.
2. Outer loop (`spec.k:19`): from `0 <= I <= N` and `x = 0`, executing the real
   outer loop before arbitrary `REST` reaches `REST`, sets `i` to `N`, restores
   `x = 0`, and increases `count` by `fizzFrom(I,N)`.
3. Entry (`spec.k:30`): with no input restriction, execution of the submitted
   module from input `N`, empty environment, and zero result reaches `.K`,
   returns `fizzFrom(0,N)`, and reaches the stated modeled local environment.
   For negative `N`, `fizzFrom(0,N)=0` and `fizzEnd(N)=0`, matching empty
   iteration.

Every precondition is satisfiable. Preserved examples include inner
`X=77,C=5` (destination count 7), outer `I=77,N=79,C=5` (destination count 8),
and entry inputs `-3, 0, 79, 178, 777`. Substituted entry results are
respectively `0, 0, 3, 5, 37` in the mathematical summary and both Python
implementations. See `evidence/stage4/claim_witnesses.py` and `.log`.

Pinning is mechanical. The reviewer extracted the entry claim's `<k>`-cell LHS
directly from the scratch `spec.k`, parsed both it and the trusted-regenerated
`solution.mpy` under `VERIFICATION`, expanded macros, and emitted KORE. The two
KORE files are byte-identical, with SHA-256
`ada0fa4a4fff5a8bafa2d2c6c20a68b70dfb6773e850e3b8bfbfdbd06d7b3122`.
See `evidence/stage4/pinning_check.py`, `.log`, and the two preserved KORE
files. Thus `INNER-LOOP` and `OUTER-LOOP` are semantically inert constructor
aliases, not substituted code.

A separate body-sensitivity mutation changes the constructor actually executed
by the claim so each digit seven increments by 2. At ground input 78 the clean
semantics reaches count/result 4; the false claimed result 2 is rejected with
`WarnStuckClaimState` and exit 1. The residual contains the completed mutated
configuration with `<result> 4 </result>`. See
`evidence/stage4/spec-body-mutation.k` and `body_mutation.log`.

The theorem covers every mathematical integer accepted by the annotated source
contract; it is not bounded to examples or fixed sizes.

## 5. Rule-by-rule static soundness review

Status: PASS.

The exhaustive declaration/rule analysis is preserved in
`evidence/stage5/rule_inventory.md`, with a mechanical source inventory in
`mechanical_inventory.log`. There are no generated helper K files.

`semantic.k` declares exactly the constructor subset used by the program:
module/function wrapper, statement sequence, assignment, while, if, return,
names, integer/Boolean values, binary operations, one-link comparisons, and
binary `or`. Its configuration contains only computation, input, local
environment, and result. It has 27 ordinary rules:

- entry binding and statement sequencing;
- left-to-right lookup/assignment;
- left-to-right `+`, `%`, and `//`;
- left-to-right `<`, `>`, and `==`;
- short-circuit `or`;
- guard-first if/while control;
- expression-first abrupt return that writes the result.

Every constructor in `solution.mpy` maps to these declarations and rules.
Negative inputs stop before remainder/division. On every executing path,
remainders and division have nonnegative dividends and positive literal
divisors, so K integer operations agree with Python for all used cases.
Short-circuit and both branch directions are preserved. The return rule clears
the function continuation and writes the computed integer; this is the
material effect required by the sole top-level modeled function. The initial
`x |-> 0` bookkeeping differs from CPython's unbound-local representation on
an empty loop but is never read before assignment on an active path and is
unobservable after return; it cannot affect the result or control.

`verification.k` has four `[function,total]` symbols and thirteen rules:

- `fizzEnd`: two exhaustive, disjoint integer cases.
- `digitSevens`: three exhaustive, disjoint cases; positive recursion strictly
  decreases by division by ten.
- `fizzContribution`: three exhaustive, disjoint divisibility cases.
- `fizzFrom`: two exhaustive, disjoint endpoint cases; recursion strictly
  decreases distance to `N`.
- one globally true, terminating right-association simplifier for integer
  addition;
- two compile-time exact loop macros.

There are no `[functional]` declarations, opaque/fresh values, priorities,
answer axioms, operational bridges, or rules that replace a program-derived
value with an unconstrained symbol. The loop claims match exact fixed-semantics
control and state and are proved circularities, not execution-bypassing
semantic rules. Function guards cover their complete domains without
conflicting overlaps; the recursive definitions descend. The sole
simplification is ordinary integer associativity.

All inventoried rules are sound on their full guard or, for the intentionally
minimal Python model, on every reachable use by this submitted program across
the intended input domain. No local rule admits a false task conclusion, so
there is no unsound-rule witness to report. Unsupported unused Python
constructs remain unmodeled, which is permitted in generated-semantics mode.

## 6. Fresh non-vacuity test

Status: PASS.

The candidate supplied no vacuity artifact. I created the fresh
`evidence/stage6/spec-vacuity-audit.k`, retaining the exact program and loop
claims while changing only the entry result obligation from `fizzFrom(0,N)` to
`fizzFrom(0,N) + 1`.

`kprove ... --dry-run` exited 0, so the mutation builds and parses
(`vacuity_dry_run.log`). The actual proof exited 1 with
`WarnStuckClaimState`; the residual is the expected failed implication
`fizzFrom(0,N) +Int 1 #Equals fizzFrom(0,N)`
(`vacuity_proof.log`). This is a reached result obligation, not a parser error,
timeout, or unrelated failure. `N=0` satisfies the original entry precondition
(there is none), both Python programs return 0, and the mutation demands 1
(`mutation_witness.py` and `.log`).

## 7. Proven versus assumed accounting

Status: PASS (Kit Gates A, B, and C pass; status `VALIDATED`).

Precisely, the successful reachability proof establishes partial correctness
of the exact regenerated constructor program under the audited generated
semantics: for every K integer `N`, the entry execution reaches the stated
final modeled configuration with result `fizzFrom(0,N)`. The helper equations
define that result as the finite sum, over nonnegative integers below `N`
divisible by 11 or 13, of the number of base-10 digits equal to seven. This is
the source contract. The proof also establishes the exact inner and outer loop
summaries used coinductively.

The accepted trust boundary is:

1. K 7.1.293, Haskell `kore-exec`, and the imported integer, Boolean, string,
   and map primitives.
2. The launcher-trusted translator as a syntactic bridge; exact regeneration
   and constructor/KORE identity check its application here.
3. The independently audited generated semantics as the model of the used
   Python subset. It is supported by exhaustive local rule review, clean
   concrete execution, and body sensitivity, not by a hidden reference
   semantics.
4. Ordinary base-10 arithmetic connecting the `digitSevens` recurrence to
   decimal digit occurrences and the `fizzFrom` recurrence to the finite
   contract set.
5. CPython and the canonical program only as the oracle for finite
   differential evidence; those tests are not used as a universal lemma.

No opaque symbol, empirical oracle, or informal program-body summary affects
the proved result. The detailed ledger is
`evidence/stage7/trust_ledger.md`. Excluded behavior is non-integer input,
unused Python language constructs, full CPython object/exception/module
semantics, and performance. None is material to the HumanEval integer
source-contract domain.

The clean proof is sound, result-constraining, non-vacuous, covers the complete
integer domain, and mechanically pins the real generated program. There is no
material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
