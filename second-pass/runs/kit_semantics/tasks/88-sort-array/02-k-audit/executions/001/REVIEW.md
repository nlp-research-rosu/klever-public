# Independent adversarial audit — 88-sort-array

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt both definitions from
source, proved both entry claims independently, mechanically compared the
parsed submitted function body with the body executed by each claim, reviewed
all local semantics and proof rules, and rejected a fresh false result
mutation for the expected semantic mismatch.

The theorem covers the full source-contract domain: every finite list of
non-negative mathematical integers, including the empty list. It is not a
finite-size or example-only theorem. The meaning of the fixed `sortVS` symbol
as ascending sorting is an explicit supplied-semantics trust boundary; it is
not a task-local oracle introduced by `verification.k`.

The complete command record is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). Reviewer-authored scripts and
bounded logs are under [`evidence/`](evidence/).

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares:

- problem `88-sort-array`;
- condition `kit-semantics`;
- `record_layout: pipeline-v3`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- a mounted trusted semantics tree.

I read the launcher record, its `record_layout`, `container_paths`, hashes, and
integrity block before using candidate evidence. All launcher-declared mounts
and all required pipeline-v3 records were real readable regular files or real
directories. I found no symlinks or unsupported filesystem entries in the
candidate, reference, or generation-evidence trees.

The campaign lock was both:

1. structurally identical to `audit_input["audit_campaign"]`; and
2. byte-hash identical to the recorded
   `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The recorded hashes for `/run.json`, `/task.json`,
`/generation-result.json`, the trusted canonical/prompt/translator, the
candidate prompt/translator, and every required generation record matched
fresh SHA-256 calculations. In particular:

- candidate pipeline tree:
  `b98aefcb26a64daa334e6b44b95fa62afaad9ba6357bcf4058624d5b957ad4bc`,
  matching the generation result;
- supplied-semantics pipeline tree:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest and audit record;
- structured trace file:
  `d6c80bd348a862e124dea324e8eecee95f56de4237d9b59ca42b46ec994725c4`,
  matching the invocation and generation result.

The candidate `prompt.py` and `py2mpy.py` were byte-identical to their trusted
mounts. A recursive type/name/content comparison found the candidate
`reference-semantics/` exactly identical to
`/reference/reference-semantics/`: no missing, additional, changed,
mistyped, or linked entries.

I inspected `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The sole JSONL trace parsed completely (390 records); its pipeline tree digest
matched `usage.json`. The generation prose and prior `#Top` reports were
treated only as untrusted claims.

Evidence:

- [`evidence/audit_integrity.py`](evidence/audit_integrity.py)
- [`evidence/stage1-integrity.log`](evidence/stage1-integrity.log)

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and canonical comparison

Status: PASS.

### Source contract

For an input list of non-negative integers:

- return a new sorted list;
- use ascending order when `first + last` is odd;
- use descending order when that sum is even;
- do not modify the input;
- return `[]` for the empty list.

The trusted canonical implementation is the same conditional behavior, with a
separate empty case. The submitted implementation uses `sorted(array)` for the
empty branch and:

```python
sorted(array, reverse=(array[0] + array[-1]) % 2 == 0)
```

for the nonempty branch. This is extensionally equivalent on the intended
domain, returns a fresh list, and does not mutate the input.

### Translator fidelity

Using the trusted copied translator:

```bash
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated MPY files had the same
SHA-256:
`248075643509fa8a6beae2a973a22a21740fdf52995a86cfcafde36cc5458363`.

### Independent differential

The reviewer script imports the trusted canonical and generated entry points
as separate modules and also computes the contract independently. It checks
result equality, input preservation, and result freshness.

It passed 4,398 distinct cases:

- all lists of lengths 0 through 5 over values `0..4`;
- all documented examples;
- empty and singleton cases;
- both parity boundaries, duplicate-heavy cases, and very large integers;
- 500 seeded generated lists of lengths up to 30.

Observed branches were one empty case, 2,098 odd-sum cases, and 2,299 even-sum
cases, with zero mismatches.

Evidence:

- [`evidence/audit_differential.py`](evidence/audit_differential.py)
- [`evidence/stage2-fidelity.log`](evidence/stage2-fidelity.log)

## 3. Clean proof reconstruction

Status: PASS.

I copied only source artifacts into `/tmp/audit-work/reconstruction`, taking
the semantics, prompt, translator, and canonical implementation from trusted
mounts. I did not copy or use either candidate-provided kompiled directory.

Observed toolchain:

- K `v7.1.293`;
- Python `3.10.12`.

### Concrete definition

The trusted semantics compiled under LLVM with:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

Exit: 0.

A reviewer-authored source containing the exact submitted function plus empty,
singleton, both parity branches, prompt examples, and input-preservation
assertions translated and ran under the fresh definition. `krun` terminated
with `<exc>NoExc</exc>`, `<exit-code>0</exit-code>`, and exit 0.

One preserved earlier run failed because I had mistakenly assigned ascending
order to `[3,1,2,1]`, whose endpoint sum is even. I corrected the reviewer
expectation to `[3,2,1,1]` and reran successfully. This is an auditor test
authoring error, not a candidate failure; both logs remain visible.

### Proof definition and target claims

The Haskell definition was rebuilt with:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Exit: 0.

Each positive target claim was then run separately:

```text
SPEC.empty     -> #Top, exit 0
SPEC.nonempty  -> #Top, exit 0
```

The warnings are from the fixed supplied semantics. LLVM reported deliberately
underspecified total helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, and
`valSeqAt`); Haskell reported only unused tail variables in `strLt`. No build
or target-claim error occurred. The proof-relevant `valSeqAt` uses are
in-bounds, as reviewed in stages 4 and 5.

Evidence:

- [`evidence/concrete_cases.py`](evidence/concrete_cases.py)
- [`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`evidence/stage3-concrete.log`](evidence/stage3-concrete.log)
- [`evidence/stage3-concrete-attempt1-reviewer-error.log`](evidence/stage3-concrete-attempt1-reviewer-error.log)
- [`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)
- [`evidence/stage3-kprove-empty.log`](evidence/stage3-kprove-empty.log)
- [`evidence/stage3-kprove-nonempty.log`](evidence/stage3-kprove-nonempty.log)

## 4. Adequacy and real-program pinning

Status: PASS.

### Claims in plain language

`SPEC.empty` starts with:

- a call to `sort_array(ref(0))`;
- heap location 0 containing the empty list;
- the module scope binding `sort_array` to the submitted closure body;
- the normal builtins parent scope;
- empty call stack, no return in progress, no exception, and exit code 0.

It requires normal completion with `ref(1)`, the original empty list preserved
at location 0, a fresh empty list at location 1, and `heapLoc` advanced from 1
to 2.

`SPEC.nonempty` represents an arbitrary nonempty finite integer list as:

```text
intVals(iCons(F, IS))
```

Its precondition says:

- `F >= 0`;
- every integer in `IS` is non-negative;
- `L` equals the element at index `vsLen(IS)` of `F :: IS`, hence the last
  element.

Its postcondition preserves the input and puts this sequence in the fresh
result list:

```text
condRev(
  sortVS(intVals(iCons(F, IS))),
  pyMod(F + L, 2) == 0)
```

Thus an odd endpoint sum leaves the ascending supplied sort unchanged and an
even endpoint sum reverses it. The claim also constrains the final environment,
scopes, stack, return state, exception state, exit code, and heap allocation.
The return value is not free, tautological, or constrained by only a one-way
implication.

### Mechanical program identity

I parsed `solution.mpy` with `kast` and emitted the compiled spec as KAST with
`kprove --dry-run --emit-json-spec`. The reviewer script extracted:

- the `FuncDef("sort_array", ...)` parameter/body tree from `solution.mpy`;
- the `closureVal` parameter/body tree from each claim;
- the entry call and its source/result references.

Both claims had exact constructor-tree equality with the submitted function
body. The common parsed body digest was:

`1e496c4680609c008f96dede2a80cfe32a393500e69886a14acdd4ca884dc692`.

Each scope fixes the name to that closure, each entry calls `ref(0)`, and each
destination requires `ref(1)`. Omitting module loading from the claim is a
semantically inert normalization here: the exact binding and builtins parent
that module loading establishes are explicitly present. Manual duplication of
the closure body is a maintenance observation, not an identity gap in this
immutable candidate.

### Satisfiability and ground substitutions

The empty state is an immediate witness for `SPEC.empty`. Ground witnesses for
`SPEC.nonempty` included:

- `[0,1]`: `F=0`, `L=1`, odd branch, result `[0,1]`;
- `[2,4,3,0,1,5,6]`: `F=2`, `L=6`, even branch, result
  `[6,5,4,3,2,1,0]`;
- a list containing 41-digit non-negative integers.

Each satisfies the formal precondition. Substituting it into the result formula
agreed with both the trusted canonical and generated Python implementations.
The full `IntSeq` variable is unbounded; this is not bounded unrolling.

Evidence:

- [`evidence/audit_pinning.py`](evidence/audit_pinning.py)
- [`evidence/adequacy_witness.py`](evidence/adequacy_witness.py)
- [`evidence/stage4-pinning-adequacy.log`](evidence/stage4-pinning-adequacy.log)

## 5. Rule-by-rule static soundness review

Status: PASS for this theorem and intended domain.

The exhaustive source inventory contains 934 local items:

- 229 syntax declarations;
- 699 rules;
- 5 contexts;
- 1 configuration.

It covers every file in the 24-file supplied semantics tree and candidate
`verification.k`. Every item has a source location, full statement,
attributes, proof relevance, and an assessment in
[`evidence/rule-inventory.md`](evidence/rule-inventory.md). The inventory
records 109 declarations with `total`, 148 with `function`, 45 priority-bearing
statements, 35 concrete-bearing statements, 22 `no-evaluators` declarations,
and all `owise`, macro, strict, and sequential-strict attributes. There are no
local `functional` or `simplification` declarations.

### Program construct coverage

| Submitted construct | Fixed declaration/rule path |
|---|---|
| Function binding/body | `FuncDef`, `Params`, `closureVal`; mechanically preinstalled in the entry scope |
| Call and name lookup | `call.k` generic callee route; `core.k` `#look`, `#evalArgs`; `functions.k` frame/bind/pop |
| `if not array` | strict `If`, `UnaryOp`, heap-ref dereference, `truthy(list(...))`, `#branch` |
| `array[0]`, `array[-1]` | subscript contexts, heap dereference, unary integer minus, `normIdx`, `vsLen`, `valSeqAt` |
| Addition and modulo | integer `applyBin("+",...)`, `pyMod(...,2)` |
| Equality to zero | integer `applyCmp("==",...)` |
| Keyword argument | left-to-right `#evalArgs`, `KwArg`, `#kwTag` |
| `sorted` | builtin name lookup, argument dereference, fixed `sorted` rules, `sortVS`, `condRev`, fresh `#alloc` |
| Return | strict `Return`, `retV`, `#pop`, environment/stack restoration |

The execution preserves Python-relevant order: callee evaluation precedes
left-to-right argument evaluation; endpoint subscripts execute before parity;
the keyword is tagged after its value evaluates; the builtin argument is
dereferenced before the exact `sorted` rule; return unwinds the frame and
restores the caller.

Priority interactions are appropriate on this path:

- priority-40 heap dereferences preempt generic value dispatch;
- cell-reference rules are disabled because the exact frame has no `$cells`
  marker;
- the generic `Call` rule is `owise`;
- the no-key, reverse-keyword, and keyed `sorted` rules have disjoint argument
  shapes for this invocation.

The claims explicitly constrain all material cells: `<k>`, `<env>`,
`<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`,
and `<exit-code>`.

### Candidate proof extensions

`verification.k` contributes exactly:

```text
intVals(.IntSeq)                    => .ValSeq
intVals(iCons(I, IS))               => vCons(I, intVals(IS))
nonNegative(.IntSeq)                => true
nonNegative(iCons(I, IS))           => I >= 0 and nonNegative(IS)
```

Both symbols are definitional summaries. Their constructor cases are pairwise
disjoint, exhaustive over `IntSeq`, and strictly descend on the tail. They
have no configuration cells, state footprint, continuation, binding, or
control effect. `intVals` embeds the symbolic input sequence; `nonNegative`
states the source-domain predicate. They do not replace any program-defined
execution.

There is no proof-local:

- operational bridge;
- priority rule;
- simplification or derived lemma;
- auxiliary claim;
- opaque or fresh result oracle;
- rewrite mentioning `Call`, `Return`, a configuration cell, or the task's
  expected output.

### Opaque symbols and totality

The only result-bearing opaque symbol reached is the supplied
`sortVS(ValSeq)`. It is declared in trusted `semantics/sort.k`, reached only
through the fixed `sorted` builtin, and has a concrete insertion-sort twin for
LLVM. The task-local theory neither defines nor intercepts it. Its value
determines the returned order/permutation, so the theorem is conditional on
the supplied contract that `sortVS` is ascending sorting.

The other fixed opaque declarations—`sortKeyVS`, the float-family symbols,
and `md5hexCodes`—cannot match this integer-list program or its claim
conditions. They provide no leverage for closure.

`valSeqAt` is fixed and totalized outside its constructor equations, leaving
out-of-bounds or opaque access abstract. Both uses here are in bounds:

- index 0 of a statically nonempty list;
- normalized index `-1`, represented by index `vsLen(IS)` in `F :: IS`.

The precondition names the latter value as `L`, so no fabricated out-of-bounds
value enters the parity result. The other compiler totality warnings concern
unreachable float/map helpers.

`MPY-CONCRETE` is imported only into the LLVM main module, not the Haskell
proof module. Its rules cannot affect `#Top`.

I found no rule that can enable a false conclusion on the intended
non-negative-integer-list domain. Accordingly, I make no unsoundness claim and
there is no false-rule witness to report. The fixed semantics is intentionally
a Python subset; unused constructs that are incomplete outside that subset
are recorded as unused limitations in the inventory, not treated as a proof
shortcut.

Evidence:

- [`evidence/audit_rule_inventory.py`](evidence/audit_rule_inventory.py)
- [`evidence/rule-inventory.md`](evidence/rule-inventory.md)
- [`evidence/stage5-inventory.log`](evidence/stage5-inventory.log)

## 6. Fresh non-vacuity test

Status: PASS.

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer module
uses satisfying input `[0,2]`. Its endpoint sum is even, so the actual result
must be `[2,0]`; the mutated destination deliberately demands `[0,2]`.

The mutation first built successfully:

```text
kprove ... --spec-module AUDIT-FALSE-SPEC --dry-run
exit 0
```

The real proof command then exited 1 with `WarnStuckClaimState`, not a parse,
import, timeout, or unrelated backend error. The residual reached normal
termination with:

```text
0 |-> list([0,2])
1 |-> list([2,0])
```

which fails to unify with the false destination. This directly demonstrates
that the entry proof constrains the result and exercises the even branch.

Evidence:

- [`evidence/spec-audit-false.k`](evidence/spec-audit-false.k)
- [`evidence/stage6-mutation-dry-run.log`](evidence/stage6-mutation-dry-run.log)
- [`evidence/stage6-mutation-proof.log`](evidence/stage6-mutation-proof.log)
- [`evidence/stage6-mutation-validation.log`](evidence/stage6-mutation-validation.log)

## 7. Proven versus assumed accounting

Status: PASS.

### Formally established

Under the supplied MPY semantics, if either entry claim terminates:

- the actual parsed submitted closure body executes through the pinned
  `sort_array` binding;
- `[]` returns a fresh empty list;
- every nonempty finite non-negative integer list returns a fresh list
  `condRev(sortVS(input), even(first+last))`;
- the endpoint expression is evaluated by real subscript, integer addition,
  modulo, and comparison rules;
- the input heap object remains unchanged;
- allocation, normal return, environment restoration, empty stack, no
  exception, and exit code 0 have the post-state stated in the claims.

Combining this with the explicitly trusted supplied contract for `sortVS`
yields the HumanEval result: ascending for odd endpoint sum and descending for
even endpoint sum, without mutating the input.

### Trust ledger

1. **Supplied MPY semantics.** Trusted because this is
   `SUPPLIED_SEMANTICS` mode and the candidate copy is exactly the launcher
   mounted trusted tree. It covers binding, evaluation order, integers,
   lists, calls, allocation, and control used by the theorem.

2. **`sortVS` ascending-sort contract.** This is the only material
   result-bearing primitive. It is a fixed external builtin boundary, not
   program-defined code and not proof-local. The nonempty claim depends on it
   for ordering and permutation. An independent LLVM run compared its concrete
   insertion-sort path against the trusted canonical function on 344 cases
   (all lists of lengths 0 through 4 over `0..3`, plus prompt examples) in 22
   batches with zero mismatches. This finite evidence supports but does not
   universally prove the supplied contract.

3. **Trusted translator.** Translation correctness is part of the ordinary
   trust base. The exact trusted translator regenerated the submitted MPY
   byte-for-byte, and KAST comparison pins the proof to that result.

4. **K implementation and mathematical hooks.** `kompile`, `kprove`, the
   Haskell backend, the LLVM backend, and K's integer/Boolean/map/list hooks are
   trusted implementation components. The proof uses mathematical unbounded
   integers, appropriate for the Python integer operations in this contract.

5. **Canonical Python implementation and CPython.** These are empirical
   oracles only. The 4,398-case Python differential and 344-case LLVM
   differential are not substituted for the K theorem.

There are no proof-local assumed lemmas, operational bridges, result oracles,
or empirical summaries.

Evidence for the LLVM bridge:

- [`evidence/audit_k_differential.py`](evidence/audit_k_differential.py)
- [`evidence/stage7-k-differential.log`](evidence/stage7-k-differential.log)

### Scope and exclusions

- This is partial correctness, not a separate termination or resource-bound
  theorem.
- Negative integers, non-integer elements, non-list inputs, and exceptional
  calls are outside the prompt's stated domain.
- The theorem uses an isolated module/call state. Extra unrelated heap objects
  are not quantified, but the function reads only its argument and builtins;
  this is a semantically inert harness choice for the stated pure contract,
  not a material source-domain restriction.
- Universal correctness of the underlying sorting algorithm is the named
  supplied primitive contract, not a theorem derived inside `spec.k`.

### Gate and verdict rationale

- Gate A (real-program soundness): PASS. Exact body and binding, no execution
  bridge, sound structural proof functions, satisfiable states, and a rejected
  fresh false result.
- Gate B (intent adequacy): PASS. Empty plus symbolic nonempty claims exhaust
  the unrestricted finite source domain; return order, copy behavior, and
  non-mutation match the prompt.
- Gate C (trust/evidence): PASS. The sole material primitive boundary is
  explicit; all reviewer evidence, commands, scopes, outputs, and limitations
  are preserved and separated from formal proof.

The fixed `sortVS` boundary is an ordinary supplied-semantics primitive, not a
material adequacy gap or smuggled task conclusion. No candidate defect or
non-fatal limitation warrants downgrading the legitimate proof.

VERDICT: PASS
LEGITIMACY: LEGIT
