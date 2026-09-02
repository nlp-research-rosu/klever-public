# Independent adversarial review: 145-order-by-points

## Executive finding

The candidate’s Python implementation appears extensionally correct, its
translation is exact, its hand-written program term is mechanically identical
to the submitted `solution.mpy`, and all eight submitted K claims reproduce
`#Top` from a clean build. The proof nevertheless does not establish the
HumanEval contract.

The decisive defect is the proof-side keyed-sort rule in the supplied
semantics. It replaces `sorted(nums, key=digit_sum)` with the opaque total term
`sortKeyVS(VS, digitSumClosure)`. That term has no proof-side equations, the
sort rule never invokes the program-defined `digit_sum` closure, and the
candidate’s postcondition repeats the same opaque term. There is no
bridge-free universal theorem connecting it to stable ascending keyed sorting.
The proof is therefore a correct execution summary only under an unconstrained
oracle interpretation, not a partial-correctness proof of the source contract.

This is a candidate-legitimacy failure, not an audit infrastructure failure.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mounted inputs do not
contradict the rendered mode.

I read `/audit-input.json` first and used its `container_paths` rather than its
host provenance paths. I then inspected:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete structured trace at
  `/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T07-15-12-019f8ee6-b7c9-78d3-a232-26d20a84627f.jsonl`.

`usage.json` was present and was inspected. Historical runtime metrics are not
required for this legacy-selected layout. All 173 trace records parsed as JSON;
there were no malformed records. The prior generation report asserted that
eight claims passed, but I treated that only as an untrusted claim and did not
reuse its build products.

Independent checks found:

- every required record was a readable regular file, and every trace entry was
  a real directory or regular file;
- the campaign-lock object exactly equaled the `audit_campaign` object, and its
  SHA-256 matched the recorded hash;
- all launcher-recorded regular-file hashes checked in
  [stage1_integrity.log](evidence/stage1_integrity.log) matched;
- the independently computed manifest hash of `/candidate` was
  `77d360adf0fe635ab12018b9dcc857bd47881701a8ecf6798ef56c169b721d56`,
  matching both the generation result and invocation’s retained-workspace
  hash;
- the trace manifest hash matched `usage.json`’s source-trace hash;
- no symlinks or unsupported entries occurred under the candidate, reference,
  or generation-evidence trees.

The candidate’s `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. A recursive, no-symlink-following comparison of the candidate and
trusted `reference-semantics/` trees exited 0 with no differences. The trusted
and candidate semantics manifest hashes both independently evaluated to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
Per-entry hashes are in
[stage1_tree_manifest.log](evidence/stage1_tree_manifest.log).

Stage 1 result: PASS. There is no provenance or mount breach and no supplied
semantics integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For an arbitrary finite list of Python integers, return a new list in stable
ascending order by each integer’s “points.” The canonical point function writes
the magnitude in decimal digits and negates only the most-significant digit for
a negative number. Thus the points of `123` are `1+2+3 = 6`, while the points
of `-123` are `-1+2+3 = 4`. Equal-point items retain their original relative
order. The documented examples include the empty list.

The candidate computes the magnitude’s digit sum arithmetically and, for a
negative input, subtracts twice the most-significant magnitude digit. This is
the same formula:

`sum(magnitude digits) - 2 * most-significant digit`.

It then uses Python’s stable `sorted(..., key=digit_sum)`.

### Trusted regeneration

The command

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/source/solution.py
```

regenerated a file byte-identical to the submitted `solution.mpy`. Both files
had SHA-256
`d3438d6347aebcc2df8ae88efa69d7f0063d52be5dccb4380056b3b6148276d6`.
See [stage2_fidelity.log](evidence/stage2_fidelity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical and generated Python entry points. It checks:

- the two documented examples;
- nine empty, singleton, sign, decimal-boundary, duplicate, and stability
  cases;
- all 7,381 tuples of length 0 through 4 over
  `{-20,-11,-10,-1,0,1,10,11,20}`;
- 2,000 deterministic random lists, using lengths 0 through 30 and integers
  ranging from small values to signed 80-digit values.

All 9,392 cases agreed, and neither implementation mutated the input. The
command exited 0 with zero mismatches; see
[stage2_fidelity.log](evidence/stage2_fidelity.log). This is strong finite
evidence that the implementation matches the canonical function. It is not a
universal proof and cannot discharge the K oracle discussed below.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/source` and copied the
trusted translator and semantics separately. I did not copy or use any
candidate-provided kompiled directory or cache. The independently observed K
version was v7.1.293.

### Concrete definition and execution

The supplied semantics were rebuilt with LLVM using `MPY-KRUN`, which is the
module that includes the concrete-only keyed-sort implementation. A
reviewer-authored program embedded the exact submitted functions and asserted
empty, zero, documented negative, decimal-boundary, tie, duplicate, and
stability cases.

My first expected list for one negative-boundary assertion was wrong:
`-10` and `-100` both have point `-1`, so stability places `-100` before the
later `-11`, whose point is `0`. The semantics correctly rejected that
reviewer error. I corrected only the expected result and reran the already
cleanly built definition. The corrected run ended with `.K`, `NoExc`, and exit
code 0. The failed reviewer assertion is preserved in
[stage3_build.log](evidence/stage3_build.log), and the corrected run is in
[stage3_concrete_retry.log](evidence/stage3_concrete_retry.log). This initial
test-oracle typo is not a candidate defect.

### Proof definition and positive claims

The proof definition was rebuilt with Haskell from `verification.k` and the
clean source copy of the supplied semantics. The original, unmodified
`spec.k` proved as a whole with exit 0 and `#Top`.

I also made a label-only scratch copy and ran each claim independently:

| Claim | Plain-language result | Exit | Output |
|---|---|---:|---|
| `ds0` | `digit_sum(0) = 0` | 0 | `#Top` |
| `ds1` | `digit_sum(1) = 1` | 0 | `#Top` |
| `ds11` | `digit_sum(11) = 2` | 0 | `#Top` |
| `ds_neg1` | `digit_sum(-1) = -1` | 0 | `#Top` |
| `ds_neg11` | `digit_sum(-11) = 0` | 0 | `#Top` |
| `ds_neg12` | `digit_sum(-12) = 1` | 0 | `#Top` |
| `ds_neg123` | `digit_sum(-123) = 4` | 0 | `#Top` |
| `order_symbolic` | allocate a list containing `sortKeyVS(VS,digitSumClosure)` | 0 | `#Top` |

The summary and exact per-claim logs are in
[stage3_prove_each.log](evidence/stage3_prove_each.log) and
`evidence/kprove_*.log`. These results establish closure under the supplied
theory. They do not by themselves validate that theory against the HumanEval
property.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Preconditions and postconditions

Each of the seven helper claims starts in a concrete initial configuration,
loads the submitted module, calls `digit_sum` on one fixed integer, and
constrains the returned K value to the stated fixed result. Every helper
precondition is satisfiable.

The target order claim starts from:

- `<k> #runOrderByPoints(list(VS)) </k>` for an unrestricted `ValSeq`;
- module environment 0, `initialScopes`, scope location 1;
- empty heap and heap location 0;
- empty call stack, `noRet`, and `NoExc`.

It requires termination at `ref(0)`, with the heap changed exactly to:

```text
0 |-> list(sortKeyVS(VS, digitSumClosure))
```

and heap location changed to 1. The scopes must become `loadedScopes`; the
environment, stack, return state, and exception state are fixed. This is not a
free result variable or a tautology: it constrains allocation, returned
reference, heap, binding, and control state. It is nevertheless only a
constraint to an opaque result-bearing symbol.

Concrete satisfying preconditions for the empty list, the documented example,
and a stable-tie example are spelled out in
[stage4_ground_witness.log](evidence/stage4_ground_witness.log). Both Python
implementations give the same concrete results. Under the formal proof
definition, however, even these ground target results remain
`sortKeyVS(..., digitSumClosure)` rather than reducing to those lists.

### Mechanical pinning

`verification.k` manually names the two bodies and assembles
`solutionModule`. To avoid trusting visual similarity, I:

1. parsed the trusted regeneration of `solution.mpy` with the clean MPY
   parser into canonical KAST;
2. extracted the independently rebuilt equations for `solutionModule`,
   `digitSumBody`, and `orderByPointsBody`;
3. expanded the two nullary body functions in the module equation; and
4. compared the complete canonical constructor trees.

The expanded proof term and trusted-translator term were both 4,207 bytes and
had the same SHA-256
`26d0e0f38ff53384e5a3082a101df8d7fc076aa2af2e43e3beba09d18d3b2ce9`.
The comparison reported `constructor_identity: True`; see
[stage4_constructor_compare.log](evidence/stage4_constructor_compare.log).

The entry rule really loads that module, name lookup selects the module’s
`order_by_points` closure, and the selected `digit_sum` key is the closure with
the submitted body. The immutable candidate is therefore pinned despite its
manual proof-term maintenance.

Stage 4 result: program identity PASS; intended-result adequacy FAIL because
the constrained result is the unconnected opaque sort summary.

## 5. Rule-by-rule static soundness review

[RULE_INVENTORY.md](evidence/RULE_INVENTORY.md) exhaustively records all source
items from `semantics.k`, its 23 helper K files, and `verification.k`. It
contains 233 syntax declarations, one configuration, five contexts, and 704
rules, with line spans, complete guards/cells, and relevant attributes.
[RULE_REVIEW.md](evidence/RULE_REVIEW.md) assigns a disposition to every
inventoried module and maps every constructor used by `solution.mpy` to its
declaration and rules.

No candidate proof-local simplification lemma, priority rule, mathematical
lemma, or execution shortcut exists in `verification.k`. Its seven nullary
function equations are exact definitions, and its two entry rules only load
and call the exact program. The relevant core, integer, control, binding,
call/return, allocation, and `abs` rules faithfully execute the submitted
constructs over the intended list-of-integers domain. Unused partial-language
features and other opaque primitives do not affect this proof.

### Decisive keyed-sort bridge

The material rules are `sort.k:49` and `sort.k:61-62`:

```k
syntax ValSeq ::= sortKeyVS(ValSeq, Val)
  [function, total, symbol(sortKeyVS), no-evaluators]

rule <k> #applyK(toCall(builtinV("sorted")),
                 (list(VS), kwV("key", KV), .Vals))
      => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

The rule preserves the allocation and ordinary continuation, but it bypasses
every invocation of the program-defined key closure. In the Haskell proof
definition there are no equations fixing `sortKeyVS` as a permutation, an
ascending order, a stable order, or the result of real closure calls.
`[total]` establishes only definedness. The concrete implementation in
`concrete.k` does perform real key calls and stable insertion, but that module
is deliberately absent from the proof definition.

This is a result-bearing operational abstraction. It directly affects the
returned heap and the source property. There is no bridge-free universal
connection theorem over its complete domain. The seven fixed helper examples
do not prove the key function for arbitrary integers, and neither the concrete
LLVM run nor differential testing proves the universal connection.

The candidate postcondition repeats `sortKeyVS(VS, digitSumClosure)`. That is
the circular pattern of using the same fresh abstraction in execution and the
claimed result; it does not establish what the abstraction computes.

### Required false-conclusion witness

Take the satisfying intended input `[1, 11]`. The points are respectively 1
and 2, so stable ascending order is `[1, 11]`. Both trusted canonical Python
and generated Python return `[1, 11]`.

As an opposite-interpretation probe, I added only:

```k
rule sortKeyVS(VS:ValSeq, _:Val) => revVS(VS)
```

to a scratch proof definition. This supplies a contract-violating but otherwise
admissible interpretation for the original equation-free symbol. The clean
definition built successfully, and a ground claim that the submitted program
returns `[11, 1]` for `[1, 11]` printed `#Top` and exited 0. Exact commands and
output are in
[stage5_opposite_interpretation.log](evidence/stage5_opposite_interpretation.log).

This is the concrete false-conclusion witness: the bridge plus candidate claim
is compatible with an interpretation that reverses a strictly ordered input.
The finding is not that the supplied rule has a false defining equation—it has
no defining equation—but that it replaces a property-bearing computation with
an unconstrained oracle and leaves the required equality unfixed.

A separate body-sensitivity experiment changed the actual compiled
`digit_sum` return to `999`; the mutated program term is confirmed in
[stage5_body_term_check.log](evidence/stage5_body_term_check.log). The
unrestricted order claim still printed `#Top` because the same changed closure
syntax appears inside the opaque postcondition. See
[stage5_body_sensitivity.log](evidence/stage5_body_sensitivity.log). Thus the
claim is syntactically body-sensitive, but not semantically connected to what
the body computes.

Stage 5 result: FAIL at real-program/source-property Gate A.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh mutation uses the
satisfying singleton input `[1]` but changes the required heap result to an
empty list. Both Python implementations return `[1]`, and the corrected
concrete K execution likewise supports that result.

The mutated spec parsed and built successfully under `kprove --dry-run` with
exit 0. The actual proof exited 1 with `WarnStuckClaimState`; its residual
showed the exact unmet obligation:

```text
.ValSeq #Equals sortKeyVS(vCons(1, .ValSeq), digitSumClosure)
```

The failure was not a parser error, timeout, missing import, or unrelated
crash. The mutation and exact commands are in
`/tmp/audit-work/source/spec-vacuity.k` and
[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log).

This confirms that the formal postcondition is discriminating with respect to
the opaque result term. It does not repair the missing connection between that
term and correct keyed sorting.

Stage 6 result: PASS for formal non-vacuity.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY theory, if the target execution terminates from the
stated initial configuration, then:

- it loads the exact submitted two-function module;
- it selects and calls the exact `order_by_points` closure;
- it selects the exact `digit_sum` closure as the `key` value;
- it returns fresh reference 0 with no exception and with normal call-stack and
  return-state restoration; and
- heap location 0 contains
  `list(sortKeyVS(VS, digitSumClosure))`.

The seven helper claims additionally establish the submitted `digit_sum` body
on exactly seven concrete integers. They do not establish its mathematical
meaning for all integers.

### Trust and assumption ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K’s built-in unbounded integer, Boolean, map, and list theories | Arithmetic, guards, scopes, heap | Acceptable ordinary low-level foundation. |
| Used supplied MPY operational rules other than keyed sort | Binding, evaluation order, loops, calls, returns, allocation, `abs` | Acceptable on the submitted program path; clean concrete execution supports the bridge to Python behavior. |
| Trusted translator | Python AST to constructor term | Acceptable here because trusted regeneration is byte-identical and the executed manual module is mechanically constructor-identical. |
| `sortKeyVS(VS, KV)` | Entire output list, ordering, stability, permutation, and all program-defined key calls | Illegitimate as the result-bearing conclusion of this proof: opaque, equation-free, no universal connection theorem, and accepts the documented opposite interpretation. |
| Seven concrete helper claims | Seven `digit_sum` evaluations | Formally proved but materially insufficient for arbitrary integers. |
| LLVM concrete keyed-sort rules | Finite concrete executions with real key calls | Useful empirical evidence only; absent from the Haskell proof definition. |
| Python differential testing | 9,392 tested inputs | Strong finite implementation evidence, not a universal K connection theorem. |
| Partial-correctness termination condition | No termination theorem is claimed | Acceptable in principle, but it cannot turn the opaque result summary into the intended postcondition. |

### Final decision

The clean `#Top` is real, the claim is non-vacuous, and the candidate pins the
submitted program. Nevertheless, the only unrestricted target claim proves
the opaque summary introduced by the same keyed-sort bridge. Because a
contract-violating ground interpretation is admitted and no connection theorem
executes or characterizes the property-bearing computation, the proof does not
establish stable ascending order by the specified digit points. Under the
benchmark’s decision boundary, an unconstrained result-bearing oracle is
`FAIL / NOT_LEGIT`, even when differential tests strongly suggest the actual
Python implementation is correct.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
