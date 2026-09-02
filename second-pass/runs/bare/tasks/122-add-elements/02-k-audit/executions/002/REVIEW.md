# Independent adversarial review: 122-add-elements

## Executive finding

The candidate has a freshly reproducible, non-vacuous K reachability proof about
the exact submitted `solution.mpy`. The generated semantics executes the
constructs in that program faithfully on the tested integer-list states, and I
did not find a proof-local rule that makes a false conclusion about that
submitted program provable on the intended integer-input domain.

It is nevertheless not a proof of the trusted HumanEval contract. The trusted
canonical implementation includes an integer only when `len(str(elem)) <= 2`.
The candidate instead includes it when `-100 < elem < 100`. Consequently every
integer from `-99` through `-10` is included by the candidate but excluded by
the trusted canonical implementation. A satisfying in-domain witness is
`arr = [-99], k = 1`: the formal postcondition, submitted Python, and generated
K semantics all return `-99`; the trusted canonical implementation returns
`0`. This is a material property mismatch, not a thin-testing concern.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1`, the condition is
`bare`, and the semantics mode is `GENERATED_SEMANTICS`.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, and every record required by this layout were
  readable real files. This includes `invocation.json`, `metrics.json`,
  `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the
  structured trace. Historical `runtime-metrics.json` is absent, as permitted
  for this layout.
- The campaign object in `/audit-input.json` is structurally identical to
  `/audit-campaign-lock.json`. The lock hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- All individually declared hashes for the run/task/result/invocation records,
  generation logs, prompt, usage, canonical source, trusted prompt, and
  translator match the independently hashed mounted files.
- Recomputing the pipeline tree digest from `/candidate` gives
  `8906df6e552422a7235dde70d9e8fecfb4a2f3a59ec56d9b8939901b0067fd1a`,
  matching the retained workspace digest in the generation result and
  invocation. Recomputing the trace tree digest gives
  `d2de03d529314fbf48bb4634934459617e3ea312fd0dca95e8f6de7fcd02f28b`,
  matching `usage.json`.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- No symlink or unsupported filesystem node occurs below `/candidate`,
  `/generation-evidence`, or `/reference`.
- `/reference/reference-semantics` is absent. That is exactly the required
  boundary for `GENERATED_SEMANTICS`; no hidden supplied semantics was sought
  or used.
- The sole JSONL trace contains 201 well-formed records. I parsed every record
  and inspected all recorded tool calls and agent result records. The
  generation transcript's `#Top` and `KPROVE_PASSED` statements were treated
  only as claims and were not reused as proof evidence.

The complete hash/type inventory is in `evidence/01_provenance.log`; the
bounded generation-record inspection is in
`evidence/01_generation_records.log`. Reviewer scripts are
`evidence/01_provenance.py` and `evidence/01_generation_records.py`. There is
no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

From `/reference/prompt.py:2-15` and `/reference/canonical.py:6-20`, the input
is a non-empty integer array with `1 <= len(arr) <= 100` and an integer
`1 <= k <= len(arr)`. The result is the sum, among the first `k` elements, of
exactly those elements for which `len(str(elem)) <= 2`. The documented example
returns `24` from `21 + 3`.

### Translation fidelity

In clean scratch I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited zero. Both files hash to
`c51f69d4c2834a4e00bf348ef1ede2dcee74c4d7623993bbe71b04bfa1c90206`.
Thus `/candidate/solution.mpy` is the exact trusted translation of
`/candidate/solution.py`. See `evidence/02_translation.log`.

### Implementation discrepancy

`/candidate/solution.py:7` tests:

```text
-100 < value and value < 100
```

That is not equivalent to `/reference/canonical.py:20`. For negative values,
the minus sign contributes to the canonical string length. Therefore:

- `-1` through `-9` are included by both;
- `-10` through `-99` are excluded canonically but included by the candidate;
- `-100` and smaller are excluded by both.

The independent deterministic differential script
`evidence/02_differential.py` exercised the example, the out-of-contract empty
case, all material value boundaries, `k = 1`, `k = len(arr)`, a length-100
case, and 500 seeded generated arrays. Of 516 cases, 515 were in-domain.
There were 390 mismatches, including 384 generated-case mismatches. Concrete
examples include:

```text
arr=[-99], k=1       canonical=0     candidate=-99
arr=[-99,99,100], k=3 canonical=99   candidate=0
```

The script deliberately exits 1 when a mismatch is found; its complete bounded
results and exit are in `evidence/02_differential.log`. This material divergence
already prevents the candidate from proving the requested source contract.

## 3. Clean proof reconstruction

Only the source artifacts and trusted reference inputs were copied to
`/tmp/audit-work/122-add-elements`. No candidate-built definition or K cache
was copied or used. The observed tools were K 7.1.293 and Python 3.10.12
(`evidence/00_tool_versions.log`).

### Generated semantics build and concrete execution

This fresh command exited zero:

```text
kompile semantic.k --backend haskell \
  --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX \
  --output-definition auditor-semantic-kompiled
```

See `evidence/03_semantic_build.log`. Using only that definition, independent
`krun` executions covered the documented example, an empty/zero-iteration
out-of-contract state, the lower negative boundary, all comparison boundaries,
and a length-100 state. Every run exited zero and the K result equaled the
submitted Python result:

| Case | K | submitted Python | trusted canonical |
|---|---:|---:|---:|
| documented example | 24 | 24 | 24 |
| empty, `k=0` (outside contract) | 0 | 0 | 0 |
| `[-100,-99], k=2` | -99 | -99 | 0 |
| all branch boundaries | -1 | -1 | 108 |
| `range(-50,50), k=100` | -50 | -50 | 1180 |

Exact commands, full relevant configurations, statuses, and comparisons are in
`evidence/03_concrete_compare.log`; the driver is
`evidence/03_concrete_compare.py`. This supports the generated semantics'
connection to the submitted program, while also reproducing its disagreement
with the trusted function.

### Proof definition and positive claims

The proof definition was built freshly:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled
```

It exited zero (`evidence/03_verification_build.log`). The two positive claims
were then exercised as follows:

- The complete spec command exited 0 and printed `#Top`
  (`evidence/03_kprove_all.log`).
- `ADD-ELEMENTS-SPEC.loop-invariant` was selected independently; it exited 0
  and printed `#Top` (`evidence/03_kprove_loop-invariant.log`).
- The entry contract was run with its required loop-invariant circularity
  explicitly loaded; it exited 0 and printed `#Top`
  (`evidence/03_kprove_contract_with_invariant.log`).

Thus clean reconstruction succeeds. This establishes closure under the supplied
generated semantics and definitions; it does not cure the contract mismatch.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-invariant` at `/candidate/spec.k:8-21` says: begin at the exact submitted
loop followed by `return total`, with an environment containing `arr=A`,
`k=K`, `total=T`, `i=I`, and an integer `value`; assume
`0 <= I <= K <= size(A)`. If this computation terminates, it finishes with
result `T + sumRange(A,I,K)`.

`add-elements-contract` at `/candidate/spec.k:24-32` says: begin with the
`solutionProgram` macro, empty environment, input `A,K`, and no result; assume
`1 <= K <= size(A) <= 100`. If execution terminates, it finishes with
`sumRange(A,0,K)`.

Both claims constrain the observable result by equality in the rewritten
`<result>` cell. The result is not a free variable, implication-only
postcondition, or tautology.

### Program identity

There are two independent pinning checks:

1. Trusted regeneration gives byte identity between `solution.py` and
   `solution.mpy` as described in stage 2.
2. Fresh `kast --expand-macros` output for `solution.mpy` is byte-identical to
   fresh expanded KAST for `solutionProgram`. The two files share hash
   `364077f7b78869925fa2eebe6a9968c445561356796f0aa28786b07bd3739123`;
   see `evidence/04_program_pinning.log`,
   `evidence/04_solution_file.kast`, and
   `evidence/04_solution_macro.kast`.

The module-entry rule binds the configuration inputs to the actual function
parameters and executes `BODY`; it does not replace the body by a result oracle.
The loop macro expands to the actual constructor-level loop.

### Satisfying witnesses and substitutions

`evidence/04_claim_witnesses.log` records:

- Entry witness: `A=[-99], K=1`. Its precondition is true. The formal result is
  `-99`; submitted Python also returns `-99`; trusted canonical Python returns
  `0`.
- Loop witness: `A=[21,3], K=2, I=1, T=21, value=21`. Its precondition is true
  and the formal result is `21 + 3 = 24`, matching both Python implementations
  on that positive-only case.

### Body sensitivity

In a separate scratch definition I changed the loop's actually executed update
from `total + value` to `total + 1`. The changed source is preserved as
`evidence/04_body_mutation_verification.k`. It compiled successfully.
Executing its `solutionProgram` on `[21],1` returned `1`. Its proof then exited
1 with `WarnStuckClaimState` on the expected obligation equating `T + 1` with
`T + intAt(A,I)`. See `evidence/04_body_sensitivity.log`.

Therefore the proof is sensitive to the body term it executes. The adequacy
failure is instead that the formal summary intentionally matches the submitted
but incorrect body.

## 5. Rule-by-rule static soundness review

There are exactly three local K files: `semantic.k`, `verification.k`, and
`spec.k`; no helper K file is hidden elsewhere. The extracted declaration/rule
index is `evidence/05_rule_inventory.log`.

### Complete local syntax and configuration inventory

- `/candidate/semantic.k:7`: `Program ::= Module(Stmts)`.
- Line 8: the two-string `Params` form.
- Line 10: statement lists.
- Lines 11-15: `FuncDef`, `Assign`, `While`, `If`, and `Return`.
- Lines 17-23: `Int`, `Name`, `UnaryOp`, `BinOp`, `BoolOp`, `Compare`, and
  `Subscript`.
- Line 24: `CmpOp`.
- Lines 34-36: values (`Int`, `Bool`, `List`), K results, and
  `noResult`/`result`.
- Line 40: result-bearing `intAt(List,Int) : Int [function,total]`.
- Lines 45-57: all 13 continuation forms: `exec`, `setVar`, `ifBranches`,
  `whileBody`, `negate`, `addRight`, `addLeft`, `andRight`, `compareRight`,
  `lessThanLeft`, `subscriptIndex`, `getAt`, and `doReturn`.
- Lines 59-68: the complete configuration: `<k>`, `<env>`, immutable input
  `<arr>`/`<n>`, and `<result>`, under `<mpy>`.
- `/candidate/verification.k:9` and line 21: `solutionLoop` and
  `solutionProgram` syntax macros.
- Lines 33 and 39: `smallContribution(Int)` and
  `sumRange(List,Int,Int)`, both `[function,total]`.

There are no local priority rules, simplification rules, opaque declarations,
standalone `functional` declarations, or other ordinary semantic symbols.

Every constructor in `solution.mpy` maps to the inventory: `Module`, `FuncDef`,
`Params`, statement-list sequencing, `Assign`, `While`, `If`, `Return`, `Int`,
`Name`, unary minus, integer addition, short-circuit `and`, one `<` comparison,
and list subscript. No used source construct is unmodeled.

### Complete operational and equation inventory

The following assessment covers every local rule individually:

| Lines | Rule(s) | Static judgment |
|---|---|---|
| `semantic.k:41` | `intAt(ListItem(I) REST,0) => I` | Correct zero-based head lookup for integer lists. |
| `semantic.k:42-43` | positive-index `intAt` recursion | Correctly removes one head and decrements the index; strict descent for intended in-bounds indices. |
| `semantic.k:70-74` | exact module entry | Binds `arr` and `k` to configuration inputs and executes the actual body. This is an entry harness, not a correctness summary. |
| `semantic.k:76` | empty `exec` | Correctly completes an empty statement list. |
| `semantic.k:77` | nonempty `exec` | Correct left-to-right statement sequencing. |
| `semantic.k:79` | assignment evaluation | Evaluates the RHS before updating the named target. |
| `semantic.k:80-81` | assignment store | Correct map update for the used name targets. |
| `semantic.k:83` | `If` setup | Evaluates the guard before either branch. |
| `semantic.k:84` | true branch | Selects exactly the then-list. |
| `semantic.k:85` | false branch | Selects exactly the else-list. |
| `semantic.k:87` | `While` setup | Evaluates the guard before the loop decision. |
| `semantic.k:88` | true loop step | Executes the body and returns to the same guard/loop head. |
| `semantic.k:89` | false loop exit | Ends the loop without executing the body. |
| `semantic.k:91` | `Return` expression | Evaluates the returned expression first. |
| `semantic.k:92-93` | return completion | Stores the value and discards the remaining function-body continuation, as Python return requires. No call stack is needed by this one-entry language. |
| `semantic.k:95` | integer literal | Exact K/Python arbitrary-precision integer value. |
| `semantic.k:96-97` | name lookup | Selects the currently bound environment value. |
| `semantic.k:99` | unary-minus setup | Evaluates the operand first. |
| `semantic.k:100` | unary-minus result | Exact integer negation. |
| `semantic.k:102` | addition setup | Evaluates the left operand first. |
| `semantic.k:103` | addition right operand | Then evaluates the right operand. |
| `semantic.k:104` | addition result | Exact integer addition. |
| `semantic.k:106` | `and` setup | Evaluates the left operand first. |
| `semantic.k:107` | true `and` | Evaluates and returns the right operand. |
| `semantic.k:108` | false `and` | Short-circuits to false. |
| `semantic.k:110` | comparison setup | Evaluates the left operand first. |
| `semantic.k:111` | comparison right operand | Then evaluates the right operand. |
| `semantic.k:112` | comparison result | Computes exact integer `<`. |
| `semantic.k:114` | subscript setup | Evaluates the list expression first. |
| `semantic.k:115` | subscript index | Then evaluates the index. |
| `semantic.k:116` | subscript result | Delegates to the in-bounds integer-list `intAt` equations. |
| `verification.k:10-19` | `solutionLoop` macro | Pure syntactic expansion to the submitted loop; mechanically checked against the translated tree. |
| `verification.k:22-28` | `solutionProgram` macro | Pure syntactic expansion to the submitted module; mechanically checked against `solution.mpy`. |
| `verification.k:34-35` | in-range `smallContribution` | Truthfully returns the value for the submitted test `-100 < I < 100`. |
| `verification.k:36-37` | out-of-range `smallContribution` | Truthfully returns zero for the complementary submitted branch. |
| `verification.k:40-41` | `sumRange` base | Returns zero exactly when the range is empty or reversed. |
| `verification.k:42-44` | `sumRange` recursion | Adds the current contribution and increments the index; it strictly approaches `K` under `I<K`. |

For `smallContribution`, the two guards are disjoint and exhaustive over
integers. For `sumRange`, `I>=K` and `I<K` are likewise disjoint and
exhaustive. The recursive index increases by one and therefore descends in
distance to `K`. `evidence/05_equation_checks.log` independently reports no
guard overlap, no uncovered integer, no mismatch with the submitted Python
summary across 1,000 seeded cases, but 108 mismatches against the trusted
canonical in that sample.

The two reachability claims at `/candidate/spec.k:8-21` and lines 24-32 are the
only proof claims. The first is the loop circularity; the second executes the
initializations and applies that verified circularity. There is no operational
bridge in `verification.k`, no task answer rule that bypasses execution, and no
fresh program-derived oracle.

### Static limitations, not invented unsoundness claims

`intAt` is declared total but its equations determine a value only for
in-bounds lists whose traversed items are integers. On negative/out-of-bounds
indices or non-integer K-list items it remains an unspecified total Int. That
does not produce a false conclusion on the source domain: the prompt requires
integer arrays, and both claim preconditions keep every executed index between
zero and `size(A)-1`. The formal K precondition uses `A:List` rather than an
explicit all-elements-Int predicate, so outside the source domain the theorem
is interpretation-parametric in this unspecified lookup instead of modeling
Python exceptions. This is a language-model boundary, not evidence that an
intended-domain false result can be proved.

No other rule has an overlap, guard, binding, continuation, state-footprint, or
evaluation-order defect. In particular, I do not label any local rule
mathematically unsound: the concrete false witness in this audit is against
the trusted task property, not against the K characterization of the submitted
body.

## 6. Fresh non-vacuity test

I authored `evidence/06_spec_vacuity.k`, copied it to scratch, and changed only
the entry result obligation from:

```text
result(sumRange(A,0,K))
```

to the deliberately false:

```text
result(sumRange(A,0,K) +Int 1)
```

The loop circularity remained available, so the mutation exercised the real
entry path. `krun` first demonstrated the satisfying witness `[21],1`, which
returns `21`. The mutated spec parsed and built far enough to enter the prover,
then `kprove` exited 1 with `WarnStuckClaimState`; its residual requires the
computed range sum plus one to equal the computed range sum. This is the
expected unmet obligation, not a parser error, missing import, timeout, or
unreachable mutation. Exact commands and the residual are in
`evidence/06_nonvacuity.log`.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the generated K semantics, starting from the exact submitted constructor
program and the formal precondition `1 <= K <= size(A) <= 100`, partial
correctness establishes:

```text
result =
  sum over i in [0,K) of
    (A[i] if -100 < A[i] < 100 else 0)
```

For intended integer arrays, the local `intAt`, `smallContribution`, and
`sumRange` equations fix every result-bearing value. The proof executes the
program-defined loop; it does not replace the loop by the summary. The theorem
is partial-correctness only: termination is not the reported logical result.

It does **not** establish the trusted result
`sum(elem for elem in arr[:k] if len(str(elem)) <= 2)`.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 kernel, Haskell backend, reachability/circularity implementation | Proof closure and all symbolic execution | Standard unavoidable trusted computing base; version recorded. |
| Built-in `INT`, `BOOL`, `LIST`, `MAP`, `MAP-SYMBOLIC`, `size`, lookup/update, and Boolean/Int operations | Values, guards, environment, proof constraints | Standard K primitives; no task-specific conclusion is hidden here. |
| Trusted `/reference/py2mpy.py` | Python-AST-to-constructor identity | Launcher-designated trusted input; byte identity of regenerated output was checked. |
| Generated module-entry harness | Argument binding and invocation control | Acceptable for this single exact function: exact name/parameters are matched and `BODY` executes. KAST pinning and body sensitivity validate it. |
| `intAt` equations | Array lookup, branches, final result | Fully fixed for intended in-bounds integer lists. Unspecified outside that domain; no claim of Python exception fidelity is made there. |
| `smallContribution` and `sumRange` | Formal postcondition | Truthful, total definitional summaries of the submitted algorithm, checked by the K proof and arithmetic review. They encode the wrong HumanEval criterion. |
| Concrete and differential tests | Python/K and submitted/canonical bridges | Finite evidence only. They support the tested bridges and expose the actual mismatch; they do not replace the reachability proof. |
| Source-contract bridge | Whether the formal summary means “at most two digits” as trusted | Refuted, not assumed: `[-99],1` is a concrete in-domain counterexample. |

Kit Gate A (real-program soundness and non-vacuity) passes for the theorem
actually written. Gate B (intent adequacy) fails materially because the written
postcondition characterizes the wrong result on valid HumanEval inputs. The
evidence and trust boundaries are reproducible, so this is not an
infrastructure or auditability uncertainty. Under the benchmark decision
boundary, a sound proof of this substituted property is not a legitimate proof
of the requested task.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
