# Independent adversarial review: 139-special-factorial

## Executive finding

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the real translated program for every integer allowed by the source contract,
namely every mathematical integer `n > 0`. A clean proof of the complete
two-claim specification exits zero with `#Top`; the loop invariant also closes
when selected by itself. The entry claim is constructor-identical to the
trusted regeneration of `solution.mpy`, and its final `answer` is constrained
to the recursively defined product `1! * 2! * ... * n!`.

I assign `CONCERNS / LEGIT`, rather than `PASS`, for two non-fatal limitations.
First, the entry claim does not close if label filtering removes its separate
loop-invariant claim: the resulting run symbolically unrolls and eventually
returns an undecided/stuck condition. The submitted proof unit is the complete
`SPEC`, in which both claims are checked together and return `#Top`; thus this
is dependency coupling, not a false or unproved theorem in the submitted unit.
Second, the supplied language is much broader than this integer-only program
and contains compiler-reported non-exhaustive `total` declarations and
explicitly opaque facilities. The exhaustive dependency review found that none
is reachable from this theorem.

All candidate prose, logs, compiled artifacts, and prior proof claims were
treated as untrusted. All execution below used source copied into
`/tmp/audit-work/case` and reviewer-built definitions.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout `legacy-selected-stage1`;
- problem `139-special-factorial`;
- generation condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`.

The trusted `/reference/reference-semantics` mount exists, so the rendered mode
and trusted mounts are consistent. No infrastructure-stop condition arose.

I read the launcher record, its `record_layout`, `container_paths`, declared
hashes, and integrity fields before inspecting candidate artifacts. I then read
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, the required invocation and metrics records, all
three text records, the optional `usage.json`, and the complete structured
trace. Historical runtime metrics are absent, which is permitted for this
layout. The trace contains one readable JSONL file with 202 records.

The independent integrity script and full output are
[verify_integrity.py](evidence/verify_integrity.py) and
[stage1-integrity.log](evidence/stage1-integrity.log). Its command wrapper is
[run-stage1.sh](evidence/run-stage1.sh). It established:

- all 14 required files and five required directories were present and
  readable, with no required artifact replaced by a symlink;
- the campaign block equals the campaign lock, and the lock hash is exactly
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- every launcher-declared ordinary-file hash matches the mounted file;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions;
- candidate and trusted `reference-semantics` trees have the same 25 recursive
  entries, types, and bytes, with manifest hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- the candidate tree hash
  `731d79e06972ff8deb641b049287af52ba1182b00b956306ede2638ad3b9deaa`
  and trace tree hash
  `295774b603525eef0da13b2091a1e42562a2737830ed35b82592952b0a31af0e`
  match the recorded generation data.

The first exploratory log records that `jq` was unavailable; it was superseded
by the successful Python integrity audit above and was not used as evidence.
There are no missing, added, changed, mistyped, or symlinked supplied-semantics
entries.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt defines the Brazilian factorial for an integer `n > 0`:

`n! * (n-1)! * ... * 1!`.

Its documented example is `special_factorial(4) == 288`. The trusted canonical
program maintains the current ordinary factorial in `fact_i` and multiplies it
into `special_fact` for `i = 1, ..., n`. Candidate `solution.py` implements the
same recurrence with a `while` loop:

1. initialize `factorial = result = i = 1`;
2. while `i <= n`, update `factorial *= i`, then
   `result *= factorial`, then `i += 1`;
3. return `result`.

Running the trusted translator on the scratch copy produced
`solution.regenerated.mpy`. `cmp` returned zero, and both it and the submitted
`solution.mpy` have SHA-256
`31cb7e21f905df1583a395328f21ae7897b025872a95b95d4b016f75f73b3628`.

The independent differential test
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and scratch candidate entry point and also checks an
independent `math.factorial` product oracle. It covers the example, the contract
boundary, small branch transitions, larger fixed inputs, and 100 reproducible
random inputs in `1..60` (seed 139). All 109 intended-domain cases agreed. The
three explicitly out-of-contract probes `-3`, `-1`, and `0` also agreed but are
not used to enlarge the theorem. Exact inputs, results, command, and zero exit
status are in [stage2-program-fidelity.log](evidence/stage2-program-fidelity.log);
the wrapper is [run-stage2.sh](evidence/run-stage2.sh).

## 3. Clean proof reconstruction

I copied only source artifacts to scratch and did not copy or use any candidate
compiled definition or cache. With K version `v7.1.293`, the following fresh
commands completed:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The reviewer concrete driver was translated with the trusted translator and
executed with the fresh LLVM definition. It asserted results for `n=1`, `4`,
and `6`, plus an out-of-contract robustness probe at `0`; `krun` terminated
with `.K`, `NoExc`, and exit code 0. The driver, commands, and bounded log are
[concrete_driver.py](evidence/concrete_driver.py),
[run-stage3-build-and-concrete.sh](evidence/run-stage3-build-and-concrete.sh),
and [stage3-build-and-concrete.log](evidence/stage3-build-and-concrete.log).

The positive target is the complete `SPEC`, containing the entry theorem and
its inductive loop theorem:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --output pretty
```

It exited 0 and printed `#Top`; see
[run-all-positive-claims.sh](evidence/run-all-positive-claims.sh) and
[stage3-proof-all.log](evidence/stage3-proof-all.log). This clean conjunction
run checks both claims and permits the entry claim to use the separately checked
loop circularity.

I additionally selected each label to expose dependency behavior:

- `--claims SPEC.special-factorial-loop` exited 0 and printed `#Top`
  ([stage3-proof-loop.log](evidence/stage3-proof-loop.log)).
- `--claims SPEC.special-factorial-correct` exited 1
  ([stage3-proof-entry.log](evidence/stage3-proof-entry.log)). With the loop
  claim filtered out, the prover unrolled concrete symbolic iterations until
  it accumulated bounds through `14 <= N` and could not decide the remaining
  unbounded loop. It did not derive a counterexample or a false postcondition.

The latter diagnostic does not negate the successful submitted proof: selecting
only the entry label removes the inductive lemma on which it deliberately
depends. It is nevertheless a reproducibility limitation worth recording,
because the entry theorem is not independently portable without its companion
claim.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The precondition at `/candidate/spec.k:8` selects any unbounded K integer
`N > 0`. It starts with environment 0, an empty module scope whose parent is
the builtins scope, fresh scope location 1, empty heap and stack, no pending
return or exception, and exit code 0. Its `<k>` cell loads a module containing
the `special_factorial` binding and immediately assigns
`answer = special_factorial(N)`.

The postcondition requires completed computation `.K`, restored environment 0,
unchanged builtins, a module binding
`"answer" |-> specialFactorial(N)`, empty heap/stack, `noRet`, `NoExc`, and exit
code 0. `?REST` permits the expected function closure and other harmless module
bindings; it does not weaken the exact `answer` equality.

This precondition is inhabited. For example, substitute `N=1` into the exact
left-hand configuration: the empty scope/heap/stack and stated scalar cells
satisfy every cell condition and `1 > 0`.

### Loop claim in plain language

At `/candidate/spec.k:49`, for integers `N >= 1` and
`1 <= I <= N+1`, the current frame contains:

- `n = N`;
- `factorial = factorial(I-1)`;
- `result = specialFactorial(I-1)`;
- `i = I`.

It executes the real internal `#while` guard and the same three real update
statements, with an arbitrary continuation `CONT`. On exit it preserves that
continuation and establishes `factorial(N)`, `specialFactorial(N)`, and
`i=N+1`. A concrete satisfying state is `N=I=L=1`, `CONT=.K`, a current frame
at key 1 with all three accumulator values equal to 1 and parent scope 0, and
otherwise compatible framed scopes.

### Mechanical pinning and concrete substitutions

[check_program_pinning.py](evidence/check_program_pinning.py) independently
extracts the balanced `FuncDef("special_factorial",...)` constructor from the
trusted regenerated MPY and from the entry claim, normalizes only whitespace
outside string tokens, and compares them. The terms are identical, both with
SHA-256
`f5079cd641097ba17bd7a80f85f5cb079893b67020fb648364b2eb229eb4545d`.
Thus the claim executes the submitted binding and body; it is not merely a
source-name or external-file association.

Ground substitutions at `N=1,3,4,6` give claimed values
`1,12,288,24883200`, identical to both Python implementations. The same check
records the corresponding loop-exit `factorial(N)` and `i=N+1`. See
[stage4-pinning-and-body-sensitivity.log](evidence/stage4-pinning-and-body-sensitivity.log).

For body sensitivity, I changed only the executed constructor's final return
from `Return(result)` to `Return(factorial)`, leaving the required
`specialFactorial(N)` postcondition and loop lemma in place. The mutation
[spec-body-mutation.k](evidence/spec-body-mutation.k) parses, reaches the final
state, and exits 1 on the expected false equality between `factorial(N)` and
`specialFactorial(N)`. `N=3` is a concrete witness: the changed program returns
6 while the required result is 12. This confirms that the theorem is sensitive
to a material change in the program term.

## 5. Rule-by-rule static soundness review

The exhaustive machine-readable inventory is
[stage5-rule-inventory.log](evidence/stage5-rule-inventory.log), generated by
[inventory_k_sources.py](evidence/inventory_k_sources.py). It covers all 24
supplied K sources plus `verification.k` and `spec.k`, with file, line,
normalized sentence text, attributes, and sentence hash. The 936 inventoried
sentences comprise:

- 229 syntax declarations;
- one configuration;
- five contexts;
- 699 rules;
- two claims.

Attribute inventory includes 147 `function`, 109 `total`, 45 priority-bearing,
26 `owise`, 35 `concrete`, 22 `no-evaluators`, two `strict`, one `seqstrict`,
and five macro declarations. There are no `functional` or `simplification`
declarations.

The complete per-construct and per-file classification is
[stage5-static-classification.md](evidence/stage5-static-classification.md).
That artifact records a disposition for every inventoried group, including all
syntax, functions, opaque declarations, priorities, semantic rules, and proof
claims. The material dependency slice is:

| Used constructor/effect | Supplied implementation checked |
|---|---|
| `Module`, statement sequencing | `syntax.k`, `core.k`: left-to-right execution |
| `FuncDef`, `Params` | `functions.k`: exact body captured in a lexical closure |
| `Assign`, `Name`, `Int` | RHS evaluation, lexical lookup, current-frame update |
| `While` / `#while` | guard reevaluation, body execution, repeat/exit behavior |
| `Compare("<=")` | left/right evaluation and K unbounded integer `<=` |
| `AugAssign("*")`, `AugAssign("+")` | sequential lookup/update using the newly updated accumulator |
| `Call` | callee/argument order, frame allocation, parameter binding |
| `Return` | return recording, continuation discard, frame restoration, caller value |
| `#loadAll` and cells | module execution and the exact framed state changes |

All these rules are faithful on the exact integer-only states of this program.
Assignment order ensures `result` observes the just-updated `factorial`.
Call/return restores the caller and exposes the returned value to `answer`.
No material state mutation, exception, guard, or control effect is omitted.

The 45 explicit priorities concern heap references/cells, methods, sorting,
math, asserts, and other head-disjoint constructs. On this path only the generic
call fallback is selected after specialized call heads are inapplicable. I
found no overlap that can redirect an intended execution.

The complete candidate-local proof extension is only:

- `factorial(N) = 1` for `N <= 0`;
- `factorial(N) = factorial(N-1) * N` for `N > 0`;
- `specialFactorial(N) = 1` for `N <= 0`;
- `specialFactorial(N) = specialFactorial(N-1) * factorial(N)` for `N > 0`.

Each pair of guards is disjoint and exhaustive over K integers. Positive
recursion strictly decreases, and the proof uses only nonnegative factorial
arguments. The second recurrence is exactly `1! * ... * N!`, which equals the
prompt's reversed multiplication by ordinary integer associativity and
commutativity. These functions summarize invariant values; they do not replace
or rewrite any program operation. There are no candidate-local priorities,
opaque symbols, operational bridges, concrete-only equations, or task-answer
rules.

The supplied fixed semantics does contain deliberately restricted or opaque
facilities: float `no-evaluators`, opaque sort/MD5 helpers, ASCII-oriented
string facilities, and an under-specified out-of-bounds `valSeqAt`. Fresh
compilation also warns that `mapStrVS`, `floorFI`, `toF`, `ceilF`, and
`valSeqAt` are not syntactically exhaustive over their declared broad carriers.
None of these symbols occurs in, head-matches, or receives data from the
submitted term, invariant, result expression, or path condition. Therefore I
do not label those limitations unsound for this theorem: there is no satisfying
`N > 0` witness by which they can enable a false result here.

No inventoried rule reachable on the intended domain encodes the desired
answer, replaces a property-bearing computation with an oracle, fabricates a
value, or bypasses execution. Consequently there is no unsound-rule false
conclusion witness to report.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation. The fresh
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) changes the entry
postcondition from:

```text
"answer" |-> specialFactorial(N)
```

to:

```text
"answer" |-> specialFactorial(N) +Int 1
```

It preserves the real program body, precondition, and loop lemma. The
independent concrete witness is `N=1`: the precondition is true, both Python
programs return 1, and the mutated obligation requires 2.

The wrapper [run-stage6-nonvacuity.sh](evidence/run-stage6-nonvacuity.sh)
first ran `kprove --dry-run`, which exited 0 and showed that the mutation
successfully parses and builds against the fresh proof definition. The actual
proof exited 1 with `WarnStuckClaimState` at the final implication, specifically
the impossible equality between the computed `specialFactorial(...)` value and
that same value plus 1. It was not a parser error, missing import, timeout,
unreachable mutation, or unrelated crash. The bounded output and exact statuses
`WITNESS_EXIT=0`, `MUTATION_DRY_RUN_EXIT=0`, and
`MUTATION_KPROVE_EXIT=1` are in
[stage6-nonvacuity.log](evidence/stage6-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY K semantics, for every unbounded K integer `N > 0`,
executing the constructor-exact translated module and its call
`special_factorial(N)` reaches completed computation with no exception, empty
heap and stack, exit code 0, and:

```text
answer = specialFactorial(N) = 1! * 2! * ... * N!
```

The separate universally quantified loop claim proves the inductive
accumulator facts through all iterations; this is not a finite unrolling or a
proof for selected sizes. Trusted regeneration and constructor identity pin
that theorem to the submitted `solution.mpy`. The source rewrite and trusted
canonical program compute the same recurrence over the complete documented
domain.

### Trust and evidence boundary

- **K implementation and logic.** The K compiler, Kore/Haskell reachability
  prover, integer/Boolean/map/list builtins, and their decision procedures are
  trusted at the ordinary theorem-prover implementation boundary. I rebuilt
  with K `v7.1.293`; I did not independently verify the K kernel or solver.
- **Supplied semantics.** Its bytes are launcher-trusted and integrity-matched,
  but integrity alone is not correctness. I statically checked every rule
  group and the complete used dependency slice. The exact used operations have
  faithful control, state, and arithmetic behavior. The broader unused opaque
  and non-exhaustive facilities remain an explicit limitation.
- **Translator bridge.** The trusted translator is assumed to define the
  benchmark's Python-to-MPY encoding. Fresh regeneration proves byte identity,
  and the constructor comparison proves the claim uses that output. General
  equivalence of this translator to all CPython behavior is not claimed.
- **Mathematical summaries.** `factorial` and `specialFactorial` are transparent,
  guarded, decreasing recursive definitions checked in the proof theory. Their
  reading as ordinary factorial products uses standard integer arithmetic; no
  empirical or opaque bridge supplies the result.
- **Canonical and differential evidence.** The Python comparison supports
  source-rewrite fidelity and concrete boundary checks only. Its 109 positive
  tests are not substituted for the unbounded K proof.
- **Claim dependency.** The entry theorem relies on the separately checked loop
  circularity and closes in the complete two-claim target. Removing that claim
  makes the entry-only filtered run inconclusive; this is the principal
  non-fatal proof-packaging concern.

The proof is result-constraining, non-vacuous, covers the full `n > 0` contract,
and executes the real submitted program. The remaining concerns do not provide
a path to prove a false conclusion on the intended domain and do not materially
narrow that domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
