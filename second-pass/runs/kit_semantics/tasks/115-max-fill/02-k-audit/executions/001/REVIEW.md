# Independent adversarial review: 115-max-fill

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed the definitions and
proofs from source, did not use any candidate-compiled definition or cache, and
treated the candidate report and generation trace only as untrusted claims.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The
trusted `/reference/reference-semantics` tree is present, so the mount agrees
with the rendered mode.

I read the launcher manifest and all records required for `pipeline-v3`:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the 509-line JSONL trace under
  `/generation-evidence/codex-trace/2026/07/29/`.

Every required record is a readable regular file, none is a symlink, and every
individually recorded SHA-256 value reproduced. Examples include:

- campaign lock:
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- run/task/result:
  `57897a7c...`, `b04af19c...`, and `a08eff4f...`;
- trusted canonical/prompt/translator:
  `908d3898...`, `c3a39401...`, and `406485ea...`;
- generation invocation, metrics, runtime metrics, usage, final text, output,
  prompt, and trace file:
  `717aec36...`, `1396ca88...`, `05bfa4fe...`, `4fc3bde1...`,
  `971b1c4f...`, `f19329ef...`, `b6a26e02...`, and `4b666158...`.

The parsed `/audit-campaign-lock.json` object exactly equals the
`audit_campaign` block in `/audit-input.json`, and the independently computed
lock hash equals the recorded hash. The generation trace is structurally valid;
its final event merely claims success and was not used as proof evidence.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive comparison of
candidate and trusted supplied semantics found the same 24 regular files, no
extra or missing entry, no type difference, no symlink, and no byte
difference. Both trees also produced the same independent reviewer tree
digest. This checks the supplied-semantics integrity boundary; it does not
bless `verification.k`.

Evidence:

- `evidence/provenance_check.sh`
- `evidence/stage1-provenance.log` (exit 0)
- `evidence/generation_trace_audit.py`
- `evidence/stage1-generation-trace-summary.log` (exit 0)

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for the number of bucket lowerings needed to remove
all water. A row contributes `ceil(number_of_ones / capacity)`; contributions
are summed over a rectangular binary grid. The stated domain is 1 to 100 rows,
1 to 100 entries per row, equal row lengths, and integer capacity 1 to 10.

The trusted canonical implementation is:

```python
sum(math.ceil(sum(arr) / capacity) for arr in grid)
```

The candidate implementation maintains an integer accumulator and executes:

```python
total += (sum(row) + capacity - 1) // capacity
```

for every row. For nonnegative row sums and positive capacity, the latter is
the standard exact integer form of the former. On the documented bounds, the
canonical float conversion involves only small exactly represented integers
and does not change the ceiling result.

Running the trusted translator on the scratch copy of `solution.py` produced a
430-byte `solution.mpy` that is byte-identical to the submitted
`/candidate/solution.mpy` (translator exit 0, `cmp` exit 0).

I wrote a new differential test that imports the trusted canonical and the
candidate through separate module names. It covers the three examples, empty
extensions, minimum and maximum documented cases, all binary rows through
length 6 in three loop contexts at capacities 1 through 10, every
ceil-division transition around multiples of capacity for representative and
maximum row lengths, and 5,000 seeded valid grids across the full bounds.
Result: 11,889 cases, zero mismatches. In particular, the examples returned
6, 5, and 0, while the 100-by-100 all-one case at capacity 10 returned 1000 in
both implementations.

Evidence:

- `evidence/stage2-translation.log` (exit 0)
- `evidence/differential_test.py`
- `evidence/stage2-differential.log` (exit 0, `MISMATCHES=0`)

Differential testing is finite implementation evidence, not a substitute for
the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work`, copied the semantics
from the trusted reference mount, and ignored all three candidate
`*-kompiled` directories, `prove.log`, `kore-exec.tar.gz`, and caches. The
toolchain independently reported K 7.1.293 for `kompile`, `kprove`, and
`krun`, and Python 3.10.12 (`evidence/tool-versions.log`).

### Concrete definition

Exact command:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

This exited 0. A reviewer-authored smoke program containing the exact function
body and seven assertions was translated with the trusted translator and run:

```sh
krun /tmp/audit-work/reviewer-smoke.mpy \
  --definition /tmp/audit-work/reviewer-runtime-kompiled
```

It exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0.
The tests cover the three examples, a loop/ceil boundary, `[[1]]`, an empty
grid, and an empty row.

Evidence:

- `evidence/stage3-runtime-build.log` (exit 0)
- `evidence/concrete_smoke.py`
- `evidence/stage3-runtime-execution.log` (translator and `krun` exit 0)

### Target proof definition and claims

Exact build:

```sh
kompile --backend haskell verification.k \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

The build exited 0. I then ran dependency-complete positive selections:

```sh
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-loop

kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-loop,MAX-FILL-SPEC.grid-loop

kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module MAX-FILL-SPEC
```

All three commands exited 0 and printed `#Top`. The last command proves all
three claims, including the entry claim, in one invocation with both
circularities available.

Evidence:

- `evidence/stage3-proof-build.log`
- `evidence/stage3-kprove-sum-loop.log`
- `evidence/stage3-kprove-loop-claims.log`
- `evidence/stage3-kprove-all-positive.log`

### Bridge-free connection definition

I separately compiled `verification.k` with main module
`MAX-FILL-SUMMARY`, which does not import the two rules in
`MAX-FILL-VERIFICATION`:

```sh
kompile --backend haskell verification.k \
  --main-module MAX-FILL-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-connection-kompiled
```

Against that definition, `fixed-int-of` and `fixed-sum-dispatch` each exited 0
and printed `#Top`. `fixed-int-of` is reported as trivial because the supplied
fixed function equation simplifies it before operational rewriting; that is
still independent of the candidate's guarded twin.

Evidence:

- `evidence/stage3-connection-build.log`
- `evidence/stage3-kprove-fixed-int-of.log`
- `evidence/stage3-kprove-fixed-sum-dispatch.log`

The positive reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`sum-loop` says that, for any finite binary row `VS` and any integer
accumulator `A`, the supplied `#sumAcc(list(VS), A)` fold terminates at
`A + rowSum(VS)`.

`grid-loop` says that the actual translated `for` loop, starting with any
integer total `S`, consumes an arbitrary finite sequence of binary row lists,
adds `gridCost(GS,C)` to `total`, and leaves the loop variable equal to the
last row (or unchanged on the empty sequence). Its precondition requires
positive `C`, binary rows, the exact local scope shape, and no module-level
shadowing of `sum`.

`max-fill` says that normal lookup and invocation of the exact `max_fill`
closure on `list(GS)` and positive integer `C` returns exactly
`gridCost(GS,C)`. It starts with the ordinary module/builtins scope chain,
empty call stack and heap, `noRet`, `NoExc`, and exit code 0. The call rules
perform parameter binding, body execution, return, frame pop, scope cleanup,
and caller restoration.

The postcondition is result-constraining: `gridCost(GS,C)` occurs on the
right of the `<k>` rewrite and is fixed by guarded structural equations. It is
not a fresh right-hand variable, an implication-only property, or a tautology.

### Mechanical program identity

`evidence/pinning_check.py` extracts the regenerated `FuncDef` body, constructs
the corresponding closure term, normalizes only whitespace, and compares K
constructors. It found:

- translated byte identity: true;
- exactly one occurrence of the complete closure/body in the entry claim;
- two exact occurrences of the material `AugAssign` subtree, one in the loop
  circularity and one in the entry body.

Thus the entry claim executes the submitted binding and body. It does not
summarize a different implementation. The allowed normalization is only the
fixed semantics' closure representation of the translated `FuncDef` and
whitespace.

Evidence: `evidence/stage4-pinning.log` (exit 0).

### Satisfying witnesses and concrete substitution

`GS = [[1]]` and `C = 1` satisfy `allRows(GS)` and `C > 0`. The formal
precondition/summary claim and a ground execution of the exact entry term both
proved with `#Top`; `gridCost([[1]],1)` reduces to 1. Both Python
implementations also returned 1 in the independent differential run.

The supplied semantics explicitly permits bare `list(ValSeq)` values as
read-only logical inputs to claims. The program neither mutates nor observes
the identity of its input lists. As an additional representation check, I
proved a ground entry call for the normal heap-backed representation of
`[[1]]`: the outer grid is `ref(1)`, its row is `ref(0)`, and the heap holds
the two list objects. The supplied `For` and builtin-call dereference paths
also returned 1 with `#Top`.

Evidence:

- `evidence/ground-witness-spec.k`
- `evidence/stage4-ground-witness.log` (exit 0, `#Top`)
- `evidence/heap-input-witness-spec.k`
- `evidence/stage4-heap-input-witness.log` (exit 0, `#Top`)

Finally, a reviewer-authored body-sensitivity probe changed the closure term
actually executed from `Assign(total,0)` to `Assign(total,1)` while retaining
the old expected result 0 on the empty-grid extension. The proof exited 1 with
`WarnStuckClaimState` and residual result 1. This changes the theorem term,
not merely an external source file.

Evidence:

- `evidence/reviewer-body-mutation-spec.k`
- `evidence/stage4-body-sensitivity.log` (expected exit 1)

### Domain and intended result

`allRows` permits any finite number of finite rows and does not require
rectangularity; `C > 0` permits any positive capacity. This is a sound
superset of every documented input, including all sizes 1 through 100,
rectangular binary rows, and capacities 1 through 10. It does not narrow the
HumanEval domain.

For a binary row, `rowSum` is its number `n` of ones. With `C > 0`,
`bucketCost` is the supplied semantics' exact positive-divisor floor equation
for `(n+C-1)//C`. Writing `n=qC+r`, `0 <= r < C`, gives `q` for `r=0` and
`q+1` otherwise, exactly `ceil(n/C)`. `gridCost` structurally sums that
quantity across all rows. It therefore is the bucket-lowering count in the
prompt.

The adequacy and real-program-pinning gate passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` inventoried every module/import, configuration,
syntax declaration, function/total/opaque declaration, context, ordinary
rule, concrete rule, priority rule, simplification rule, and claim in the 23
trusted helper files, assembled `semantics.k`, `verification.k`, and `spec.k`.
The bounded inventory contains 1,104 records:

- 629 ordinary rules;
- 46 priority rules;
- 35 concrete rules;
- 6 simplification rules;
- 129 function declarations, including 24 opaque/no-evaluator declarations;
- 81 other syntax declarations, 5 contexts, 1 configuration, and 3 claims;
- module/import/end-module records needed to establish dependencies.

Of these, 192 fixed-semantics records are material to `max_fill`; the
inventory marks every other supplied record as inert for this target rather
than omitting it. The 34 proof-local records and all 3 claims are separately
marked for manual review.

Evidence:

- `evidence/inventory_k.py`
- `evidence/rule-inventory.tsv` (generator exit 0)

For every fixed rule marked inert, its leading constructor, callable name,
method name, value sort, or control marker cannot arise from `solution.mpy` or
the claims on the intended input path. Consequently it cannot enable a false
conclusion for an intended `max_fill` input. Missing coverage for those unused
constructs is not relevant under the supplied-semantics task boundary.

### Material supplied-semantics map

| Program construct | Fixed declarations and rules | Review |
|---|---|---|
| Module, function, parameters, names, integer literals | `semantics/syntax.k`; `core.k` lines 25-60, 123-131, 193-196; `functions.k` lines 13-20 | Constructor sorts agree with trusted translation; module load and lookup use the declared scope chain. |
| Call and closure invocation | `call.k` lines 18-32 and 69-75; `functions.k` lines 62-91 | Callee evaluates before arguments; arguments evaluate left-to-right; parameters bind in order; return discards only the callee suffix, then `#pop` restores caller continuation and cells. |
| Assignment and augmented assignment | `controls.k` lines 8-31 | RHS strictness precedes update. On this path `total` is an integer, so `applyBin("+",...)` is the fixed integer addition rule. |
| `for row in grid` | `controls.k` lines 62-75; `tuple.k` lines 30-41; `list.k` lines 8-10 | The iterable evaluates once; one head is bound before the exact body; the tail loops; empty list ends. The loop claim includes the retained target value. |
| `sum(row)` | `core.k` lines 183-191; `call.k` lines 26 and 34-50; `builtins.k` lines 46-56; `list.k` lines 8-10 | Lookup selects the builtin because the claim excludes module shadowing. Heap refs dereference before dispatch. `#sumAcc` consumes each element once and `intOf(I)=I`. |
| `+`, `-`, and `//` | `operators.k` lines 10-17; `int.k` lines 7-20 | Strict evaluation is left-to-right. Integer `+`/`-` are exact; positive-divisor `//` uses the standard floor via `pyMod`. No zero divisor is admitted. |
| Return and complete state | `functions.k` lines 77-91; `core.k` configuration | Result, return state, stack, environment, scope allocation, exception, exit code, and heap behavior match the claim's complete cells. |

I checked overlaps and priorities on this path. The fixed heap-dereference
rules preempt generic dispatch only for `ref` values. The list and integer
rules are sort/constructor disjoint. The two integer arithmetic paths used by
the body have no competing float, string, dict, or list rule. No material
fixed rule fabricates a result or suppresses a used control effect.

### Every proof-local declaration and rule

1. `definedProjectInt(V) = isInt(V)` is an exact sort discriminator.
   `projectInt` is a total opaque value only off its guard. The `#Ceil`,
   concrete-cast, symbolic-cast, and `projectInt(I)=I` simplifications all
   express the same guarded subsort projection. Their overlaps agree.

2. `rowVals(list(VS)) = VS` is constructor projection. `isListVal(V)` is
   `V ==K list(rowVals(V))`; constructor disjointness makes it false for a
   ground non-list and, symbolically, restricts `V` to precisely the list
   constructor and projected contents.

3. `allBinary` and `allRows` have disjoint empty/cons cases, descend
   structurally, and require every result-bearing projection to be under its
   matching integer/list guard. They state the domain; they do not assume the
   result.

4. `rowSum` has disjoint empty/cons cases and descends. On `allBinary`, every
   `intOf(V)` is the fixed integer value. Outside that guarded theorem domain,
   total opaque projection/function values may remain abstract, but no rule
   gives them a false concrete numeric interpretation and they cannot affect
   a target conclusion.

5. `bucketCost` uses disjoint and exhaustive integer guards `C>0` and
   `C<=0`. Only the positive rule is reachable from the target; it is exactly
   the fixed `//` equation. The nonpositive branch merely totalizes the
   summary and is never connected to program execution under a nonpositive
   capacity.

6. `gridCost` and `finalRow` use disjoint empty/cons cases and strictly
   descend. They are fold summaries; neither rewrites operational program
   syntax.

7. The guarded `intOf(V) => projectInt(V)` simplification overlaps the fixed
   `intOf(I) => I` rule only when `V` is an integer. Then
   `projectInt(I) => I`, so the right sides agree. The bridge-free
   `fixed-int-of` claim independently closes.

8. The only operational bridge is the priority-40 symbolic dispatch rule for
   `#applyK(toCall(builtinV("sum")), (V,.Vals))`. Its guard gives
   `V ==K list(rowVals(V))`, so every match is an instance of the fixed
   list-sum dispatch. Its right side is exactly
   `#sumAcc(list(rowVals(V)),0)`. It rewrites only the leading redex, frames
   the complete arbitrary continuation, introduces no abrupt control, and
   reads or writes no environment, scope, heap, allocation, stack, return,
   exception, or exit cell. On its syntactic overlap with the fixed list rule,
   the right sides are identical.

The bridge-free `fixed-sum-dispatch` theorem is universal over `VS` and the
framed continuation and was proved with a definition that excludes the
candidate bridge. As a ground context-sensitivity check, I added an immediate
observable continuation that adds 100 after summing `[1,1]`. Both a fixed
definition and a bridge-enabled definition proved the result 102 with
`#Top`. Thus the bridge neither discards nor changes the continuation.

Evidence:

- `evidence/bridge-context.k`
- `evidence/stage5-fixed-context-build.log`
- `evidence/stage5-fixed-context-proof.log`
- `evidence/stage5-bridged-context-build.log`
- `evidence/stage5-bridged-context-proof.log`

The two opaque projections are not result oracles on the theorem domain.
Fresh opposite-interpretation claims demanding `projectInt(1)=0` and
`rowVals(list([1]))=[]` both parsed, reached implication checking, emitted
`WarnStuckClaimState`, and exited 1.

Evidence:

- `evidence/projection-opposite-spec.k`
- `evidence/stage5-opposite-int.log`
- `evidence/stage5-opposite-row.log`

I found no materially unsound rule. In particular, there is no rule for which
a satisfying intended-domain state enables a false result, control state, or
observable-cell conclusion, so there is no required false-conclusion witness
to report.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh
`evidence/reviewer-nonvacuity-spec.k` changes the exact entry result on the
satisfying input `[[1]], capacity=1` from 1 to 2. The spec imports and parses
successfully against the fresh proof definition, then execution reaches:

```text
<k> 1 ~> .K </k>
```

That state cannot unify with the mutated destination 2. `kprove` emits
`WarnStuckClaimState` and the normal “cannot be rewritten further” prover
error, and exits 1. This is an unmet result obligation, not a parser failure,
missing import, timeout, or unrelated crash. The corresponding true ground
claim proved `#Top` in Stage 4.

Evidence:

- `evidence/reviewer-nonvacuity-spec.k`
- `evidence/stage6-nonvacuity.log` (expected exit 1)

The proof is non-vacuous and discriminates a false returned value.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied MPY definition plus the audited proof-local equations and
guarded dispatch twin, invoking the exact submitted `max_fill` closure on any
finite `list(GS)` of finite binary integer row lists and any positive integer
capacity reaches `gridCost(GS,C)`, with the stated environment, scopes,
allocation counters, stack, return, exception, and exit cells restored. The
auxiliary sum and grid loop claims establish the two unbounded structural
folds; this is not a bounded unrolling or finite-size theorem.

This is partial correctness in the Kit sense. The review does not add a
separate liveness theorem, although the reachability proof closes over every
finite algebraic input in its domain.

### Trust and assumptions

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, matching-logic compiler, Haskell/LLVM backends, integer/Boolean hooks, and solver | All proof and execution results | Standard unavoidable machine-checked-proof trust boundary; versions and fresh exits are recorded. |
| Trusted supplied MPY semantics | Meaning of translation, calls, lists, loops, `sum`, integer operators, and return | Required by `SUPPLIED_SEMANTICS`; candidate tree is byte-identical. Every target-path rule was statically reviewed and concretely exercised. |
| Trusted `/reference/py2mpy.py` | Source-to-`solution.mpy` bridge | Required trusted input; regeneration is byte-identical, and the claim body was mechanically compared at constructor level. |
| K integer division and `pyMod` | Meaning of `bucketCost` | Fixed supplied primitive/equations, used only with positive divisor. The ordinary quotient/remainder argument establishes the ceiling identity. |
| `projectInt` and `rowVals` off their guards | Only off-domain abstract terms | They are candidate opaque total symbols, but every target result-bearing use is guard-pinned. Opposite ground values are rejected; no target conclusion is conditional on an arbitrary interpretation. |
| Bare logical lists versus heap-backed source lists | Input representation | The supplied semantics explicitly admits unboxed read-only claim inputs. The program has no list mutation or identity observation; concrete execution and a heap-backed K witness agree. This is semantically inert for the claimed contract. |
| Natural-language “bucket lowerings” interpretation | `gridCost` to task intent | Ordinary mathematics: each lowering removes at most `C` units from one row, hence exactly `ceil(n/C)` lowerings per row. No empirical oracle is being substituted for a proof rule. |
| Differential test | Python rewrite/canonical agreement on tested values | Finite supporting evidence only; it is not used as a universal theorem or to justify an opaque K result. |

Excluded behavior is non-list rows, non-binary elements, nonpositive
capacity, input-list mutation or identity observations not present in the
program, and Python constructs outside the supplied MPY subset. Those
exclusions remove no documented HumanEval input.

Gate A passes: the exact body executes, all extensions are sound on their
complete result-bearing match domains, a satisfying witness exists, body and
result mutations fail, and control/value sensitivity checks pass.

Gate B passes: the formal domain is an unbounded safe superset of the complete
documented HumanEval domain, and the exact formal result is the requested
bucket-lowering count.

Gate C passes: all reviewer evidence, commands, scopes, exits, and bounded
outputs are preserved under `/audit-output/evidence/`, with formal proof,
finite empirical support, and trust assumptions clearly separated.

VERDICT: PASS
LEGITIMACY: LEGIT
