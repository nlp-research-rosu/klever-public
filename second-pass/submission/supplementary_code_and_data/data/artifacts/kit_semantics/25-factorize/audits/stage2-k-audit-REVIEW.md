# Independent adversarial review: 25-factorize

## Assessment

The candidate contains a legitimate, unbounded partial-correctness proof of the
submitted `factorize` program for every positive integer, including `1`. A
fresh source build closes both positive claims, the postcondition fixes the
entire returned list, and fresh false-result and body mutations are rejected.
The proof does not replace execution with an oracle or a proof-local
operational rule.

I assign `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for one non-fatal
validation limitation: K proves equality with the recursively defined
trial-division sequence `factorAcc`, while the theorem that this sequence is
exactly the nondecreasing prime-factor multiset with the required product is
given as an ordinary mathematical argument, not as a machine-checked K
postcondition/lemma. The argument is sound and the recurrence fully constrains
the result, so this is not vacuity, a substituted-program proof, or a material
domain restriction.

The evidence index is
[`evidence/INDEX.md`](evidence/INDEX.md). Candidate `PROOF.md`, candidate build
directories, and generation reports were treated only as untrusted claims.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `25-factorize`, and condition
`kit-semantics`. The supplied trusted tree exists at
`/reference/reference-semantics`, so the mount agrees with the rendered mode;
there is no infrastructure contradiction.

I independently read and parsed:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- all required generation records: `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the complete structured trace: one 752,899-byte JSONL file with 447 valid
  events, including all 107 ordinary/custom tool calls and the final reported
  result.

The audit campaign lock is byte-hashed to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object exactly equals the
`audit_campaign` block.

Independent SHA-256 checks match every launcher-recorded regular-file digest:
canonical, trusted/candidate prompt, trusted/candidate translator, run/task
manifests, result, invocation, metrics, runtime metrics, usage, generation
prompt, last message, output log, and the trace JSONL. Independent pipeline
tree hashes also match:

- `/candidate`:
  `5a6500781bf3a49ff0fd5851b76d3a9f01ac614a940b0fc7151e040bcbd5f91c`;
- each supplied-semantics tree:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- generation trace tree:
  `dc14176733fad47e4ed9fecb8e7ce414559ef4d4f5ab9185518bc3aad8a426b5`.

The audit input also records alternate launcher digest values for those trees;
they agree between candidate and trusted semantics. The independently
recomputed pipeline hashes above are matched against the pipeline/result
records that define that hash algorithm.

A recursive entry-by-entry comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` finds zero missing, additional, changed,
mistyped, or symlinked entries. `/candidate` contains no symlinks. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts. All
required candidate proof artifacts are regular files and present.

Evidence:
[`01-provenance-check.log`](evidence/01-provenance-check.log) and
[`02-generation-records.log`](evidence/02-generation-records.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and domain

The trusted prompt asks `factorize(n: int)` to return the prime factors of the
input in nondecreasing order, repeated with their multiplicities, whose product
is the input. It documents:

- `8 -> [2,2,2]`;
- `25 -> [5,5]`;
- `70 -> [2,5,7]`.

The material domain is positive integers. `1` has the valid empty
factorization. Zero and negative integers cannot satisfy the stated
positive-prime/product contract; this interpretation is also consistent with
the trusted canonical implementation, which raises on negative input. Thus the
formal `N >= 1` restriction is not a material narrowing of the HumanEval
contract.

`solution.py` performs increasing trial division starting at `2`. On a
divisible remainder it appends the divisor and divides the remainder; otherwise
it increments the divisor. It returns the accumulated list. This differs from
the trusted canonical square-root stopping algorithm but is extensionally
equivalent on the positive domain.

### Trusted regeneration

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced 561 bytes with SHA-256
`ca302004dd3f1e0d603dc5dbb9771992e9dfcdde258cc3ea5c11875f6ffa5aa6`.
The submitted `solution.mpy` has the same size, hash, and bytes.

Exact command and result:
[`06-program-fidelity.log`](evidence/06-program-fidelity.log).

### Independent differential test

The reviewer-authored
[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical module and generated solution separately. It checks:

- all three documented examples and the empty-result boundary `1`;
- explicit prime/composite/repeated-factor and branch boundaries;
- every integer `1..300`;
- larger prime/composite cases `9973`, `65536`, and `99991`;
- 300 deterministic generated integers in `1..20000` (seed `2500729`).

There are 597 unique positive inputs, zero result mismatches, and zero failures
of nondecreasing order, primality of each factor, or product equality. For
diagnostic completeness, both implementations return `[]` at `0`, while the
canonical raises and the generated implementation returns `[]` at `-1`; those
values are outside the positive contract.

Exact command, scope, and result:
[`07-differential-test.log`](evidence/07-differential-test.log). This is finite
evidence, not a substitute for the symbolic proof.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/review-25-factorize` and copied only candidate
source artifacts plus trusted canonical/prompt/translator/semantics. Candidate
`runtime-kompiled`, `verification-kompiled`, caches, logs, and binaries were
not copied or consulted by any proof command. Copy commands are recorded in
the `03`–`05` evidence logs. The live tools report K version `7.1.293`
([`08-tool-versions.log`](evidence/08-tool-versions.log)).

### Fresh concrete definition

Command:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exits `0`. A fresh reviewer probe containing the exact function body and
assertions at `1,2,8,25,70,97` passes in CPython and, after trusted translation,
passes under:

```text
krun concrete-probe.mpy --definition audit-runtime-kompiled
```

`krun` exits `0` with `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code `0`;
the heap contains the expected lists. Evidence:
[`09-kompile-llvm.log`](evidence/09-kompile-llvm.log) through
[`12-krun-concrete-probe.log`](evidence/12-krun-concrete-probe.log).

### Fresh proof definition and positive claims

Command:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exits `0`
([`13-kompile-haskell.log`](evidence/13-kompile-haskell.log)).

The submitted spec as a whole then closes:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Exit status is `0` and the proof result is `#Top`
([`14-kprove-all-positive.log`](evidence/14-kprove-all-positive.log)).

I also selected the loop claim with its fully qualified label; it independently
exits `0` with `#Top`
([`15-kprove-factor-loop.log`](evidence/15-kprove-factor-loop.log)). The entry
claim requires the loop circularity, so its correct selected run retains both
labels:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.factor-loop,SPEC.factorize
```

That command also exits `0` with `#Top`
([`16-kprove-factorize-with-helper.log`](evidence/16-kprove-factorize-with-helper.log)).
An earlier diagnostic using an unqualified filter label was rejected before
proof and is transparently retained in the evidence index; it is not a target
proof result.

Compiler warnings concern unused variables in supplied string rules and
existential final local values. They do not represent stuck operations or
unclosed obligations.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`SPEC.factor-loop` assumes an exact running function frame:

- original loop-summary arguments satisfy `N >= 1` and `D >= 2`;
- the current locals are `n=N`, `divisor=D`, and `factors=ref(0)`;
- heap location `0` contains arbitrary sequence `A`;
- the exact closure binding, caller frame, counters, return state, exception
  state, exit code, and trailing `Return(factors) ~> #endcall` are present.

It proves that, if this loop terminates, control reaches the trailing return and
heap location `0` is exactly `factorAcc(A,N,D)`. The final local `n` and
`divisor` are existential because the public result does not observe them.

`SPEC.factorize` assumes `N >= 1`, an empty heap, and the exact
module-scope `factorize` closure. It calls the function with `N` and proves the
result is `ref(0)`, whose heap value is exactly
`list(factorAcc(.ValSeq,N,2))`. It also proves exactly one allocation,
restoration of environment/scope/stack, `noRet`, `NoExc`, and exit code `0`.
This is equality to a full sequence, not a free result, tautology, or one-way
property.

### Satisfiability and ground substitution

Concrete satisfying states include:

- loop claim: `N=1`, `D=2`, `A=.ValSeq`, exact local frame and heap;
- entry claim: `N=8`, exact closure, empty heap, normal caller state.

Ground evaluation of the claimed postcondition at
`1,2,8,25,70,97` equals both Python implementations in every case. A helper
witness with nonempty accumulator gives
`factorAcc([11],8,2)=[11,2,2,2]`. Evidence:
[`18-claim-witnesses.log`](evidence/18-claim-witnesses.log).

### Program identity

Reviewer code mechanically extracted the single regenerated
`FuncDef("factorize",...)` constructor and both `closureVal("n",...,0)`
occurrences in `spec.k`. After only two parser-inert normalizations—making the
empty `ListExpr` unit explicit and erasing explicit `.Stmts` list units—both
claim bodies match the regenerated body exactly, constructor for constructor.
The entry call is the symbolic
`Call(Name("factorize"),(Int(N),.Exprs))`.

Evidence:
[`program_pinning.py`](evidence/program_pinning.py) and
[`17-program-pinning.log`](evidence/17-program-pinning.log).

The only complete-module construct not in the entry claim is
`ImportFrom("typing","List")`. The supplied semantics' non-`math`
`ImportFrom` rule removes it without changing any cell, and it is typing-only
in the source. Normal module execution and `FuncDef` binding were independently
confirmed by the fresh LLVM probe.

The loop claim matches the real desugared `#while` control point and exact
trailing continuation. It neither introduces return nor accepts an arbitrary
continuation. No rule in `verification.k` matches a `<k>` program term.

### Intent bridge

Starting at empty `A`, positive `N`, and `D=2`, the `factorAcc` equations
describe unbounded increasing trial division:

1. A division appends `D`, changes the remainder from `N` to `N/D`, and
   preserves `original = product(accumulated) * remainder`.
2. A failed division increases `D`, so factors are appended in nondecreasing
   order.
3. An appended `D` must be prime: any prime divisor below `D` would have been
   tested and removed to exhaustion before `D` could divide the current
   remainder.
4. A reachable exit has remainder `1` (a remainder greater than `1` is tested
   against itself before the guard can become false), so the accumulated
   product is the original input.

This is a valid ordinary proof of the HumanEval interpretation, and the
differential/property test supports it. It is not itself encoded as K claims
about primality, ordering, and product. That machine-checking gap is the sole
reason for `CONCERNS` rather than `PASS`.

## 5. Rule-by-rule static soundness review

The reviewer-generated exhaustive inventory covers the trusted
`reference-semantics` tree, `verification.k`, and `spec.k`:

- 26 K files;
- 934 declarations: 228 syntax blocks, 698 rules, 5 contexts, 1
  configuration, and 2 claims;
- 460 equational and 238 operational rules;
- no `[functional]`, `[simplification]`, or `[simplify]` declarations;
- 25 supplied `[symbol]` declarations, of which 22 are explicitly
  `[no-evaluators]`;
- 45 priority-bearing rules and 35 `[concrete]` equations.

Every declaration/rule is enumerated with file, line, complete source block,
and attributes in
[`19-rule-inventory.log`](evidence/19-rule-inventory.log). Every supplied file
and all 698 rules receive an active-rule or constructor/guard-unreachability
disposition in
[`used-semantics-map.md`](evidence/used-semantics-map.md).

### Active fixed-semantics rules

The active execution slice includes:

- configuration, module sequencing, exact closure binding, lexical lookup,
  call-frame allocation/parameter binding/pop, and return;
- strict assignment, integer/list literals, and fresh heap allocation;
- `While/#while`, Bool truthiness, `If`, and expression-statement effects;
- left-to-right binary/comparison/callee/argument evaluation;
- integer `<=`, `==`, `%`, floor `//`, and `+`;
- attribute/bound-method routing and the complete in-place append heap update.

The active priority rule is the exact `append` interception. It updates only
the matched heap list and returns `noneV`; the loop claim represents that
state change exactly. Cell/ref priority alternatives are guard-inapplicable or
sort-disjoint. Function entry/pop accounts for every modified cell and keeps
the returned heap object alive.

Strictness generates mechanical heating/cooling rules from the inventoried
syntax attributes. The declared order agrees with Python for every used
construct: binary operands, comparison operands, callee then arguments, and
assignment/if/return expressions.

### Proof-local rules

`verification.k` has exactly one declaration and three rules:

| Extension | Class and complete domain | Static decision |
|---|---|---|
| `factorAcc(A,N,D)` | Definitional summary; proof uses `N>=1,D>=2` | Result-bearing but fully defined by guarded equations; never rewrites execution |
| `N < D -> A` | Base equation | Exactly the false while-guard branch |
| `D <= N && pyMod(N,D)==0` | Divisible equation | Exact append and supplied floor-division update; positive `D` rules out undefined division |
| `D <= N && pyMod(N,D)!=0` | Non-divisible equation | Exact unchanged remainder/accumulator and `D+1` update |

On the complete proof-use domain, the guards are exhaustive and pairwise
disjoint. The equations terminate as a function evaluation: divisible steps
strictly reduce positive `N` by a factor of at least two; non-divisible steps
increase `D` until either a division occurs or `N<D`. There is no totality
attribute, conflicting overlap, priority, simplification, or opaque value.

`factor-loop` is a derived reachability circularity, not an operational rule.
It executes one genuine supplied-semantics iteration before reapplication and
has the exact continuation, binding, control stack, counters, and observable
cells. It is the universal execution-to-`factorAcc` connection on every use
made by the entry claim.

### Opaque and unused theory

The supplied semantics' opaque float, sort, and MD5 symbols are listed by name
in `used-semantics-map.md`. None occurs in the submitted constructor tree,
reachable values, guards, result, heap postcondition, or proof-local rule.
`MPY-CONCRETE` is imported by `MPY-KRUN`, not by `VERIFICATION`. Therefore no
opaque interpretation or concrete-only rule contributes to either positive
claim.

No rule encodes a fixed answer, fabricates a value for a used operation,
replaces a program-defined call, or permits a false result on the intended
domain. I found no unsound rule and therefore make no unsupported unsoundness
claim requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not relied upon. I wrote the fresh
[`spec-audit-false.k`](evidence/spec-audit-false.k), which executes the exact
submitted closure at the satisfiable input `1` but changes the required heap
result from the true `[]` to the false `[2]`.

First:

```text
kprove spec-audit-false.k --definition audit-verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE --dry-run
```

exits `0`, proving the mutation parses and builds
([`21-false-mutation-dry-run.log`](evidence/21-false-mutation-dry-run.log)).

The actual proof command exits `1` with `WarnStuckClaimState`. Its residual has
`<k> ref(0) ~> .K </k>` and the actual
`0 |-> list(.ValSeq)`, which cannot unify with demanded `[2]`. This is the
expected unmet result obligation, not a parser error, timeout, or unrelated
crash
([`22-false-mutation-kprove.log`](evidence/22-false-mutation-kprove.log)).

I separately changed the program term actually stored in the claimed closure:
the initial divisor is `3` rather than `2`. At input `4` the fixed semantics
reaches `[4]`, so the original `[2,2]` obligation is rejected with another
meaningful stuck state. Evidence:
[`spec-body-sensitivity-audit.k`](evidence/spec-body-sensitivity-audit.k) and
[`23-body-sensitivity-kprove.log`](evidence/23-body-sensitivity-kprove.log).
This tests theorem dependence on the executed body, not merely an external
source file.

## 7. Proven versus assumed accounting

### What is machine-proved

Conditional on the trusted K backend and supplied MPY theory, for every
mathematical integer `N >= 1`, if the exact submitted `factorize(N)` closure
terminates, then it:

- returns `ref(0)`;
- leaves exactly one allocated heap list whose full sequence is
  `factorAcc(.ValSeq,N,2)`;
- restores the caller environment, scope allocation counter, and empty stack;
- leaves `noRet`, `NoExc`, and exit code `0`.

The helper claim proves, over arbitrary accumulator `A`, positive remainder
`N`, and divisor `D>=2`, that the exact loop transforms heap list `A` to
`factorAcc(A,N,D)` while preserving its exact continuation and frame.

This is partial correctness. K does not machine-prove termination here.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and reachability/circularity logic | All closure results | Standard unavoidable proof kernel/backend boundary; accepted |
| Trusted supplied MPY semantics | Value, evaluation order, heap, call/control, return, exceptions | Integrity-checked and relevant rules statically audited; accepted for the benchmark's selected semantics level |
| Trusted `py2mpy.py` | Source-to-constructor identity | Byte regeneration plus mechanical body comparison; accepted mandated translation boundary |
| Omitted typing import | Module-to-entry normalization | Fixed semantics proves it is a no-op; accepted |
| `factorAcc` equations | Entire result sequence | Proof-local but truthful, guarded, disjoint, terminating on all uses, and connected by the loop claim; accepted |
| Trial-division recurrence implies ordered prime factors with correct product | Human-facing intent | Sound informal mathematics, supported by property/differential tests, but not machine-checked; non-fatal concern |
| Positive-integer domain interpretation | Claim precondition | Supported by prime-factor/product contract and canonical behavior; no material domain narrowing |
| Independent canonical differential test | Program/intent bridge on 597 inputs | Finite empirical support only; never used as a universal proof |
| Supplied opaque float/sort/MD5 symbols | None: unreachable from both claims | Inert; no proof dependency |
| Termination argument | Total-correctness interpretation only | Informal and not claimed by the K reachability theorem |

### Decision

Gate A passes: fresh `#Top`, exact real-program execution, no unsound extension,
result and body sensitivity, and a satisfiable precondition. The theorem covers
the full material positive-integer domain without a bound, example-only
restriction, or unrolling limit. The only limitation is the explicitly
informal summary-to-prime-factor intent theorem. Under the benchmark's decision
boundary, that supports `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
