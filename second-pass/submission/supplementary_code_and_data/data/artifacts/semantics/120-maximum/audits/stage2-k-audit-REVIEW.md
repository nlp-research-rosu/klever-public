# Independent adversarial review: HumanEval 120 `maximum`

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics.  Fresh builds close both entry claims,
the formal domain includes the full HumanEval input domain, the claims execute a
constructor-identical copy of the submitted function body, and independent body
and postcondition mutations are rejected.

The non-fatal concern is the supplied semantics' intentionally opaque
`sortVS`.  K proves that the program returns the appropriate suffix of
`sortVS(VS)`, but the fact that `sortVS` is an ascending permutation is an
external primitive contract, not a theorem reconstructed here.  Concrete
insertion-sort equations and finite K/Python differential executions support
that contract; they do not prove it universally.  No false conclusion witness
was found on the intended integer-list domain, so this is an auditable trust
boundary rather than an unsoundness finding.

## 1. Input and provenance integrity

The launcher declares:

- `record_layout = legacy-selected-stage1`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `problem_id = 120-maximum`
- `condition = semantics`

The mode boundary is consistent: `/reference/reference-semantics` is present.
All launcher-required records for this layout are regular readable files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The trace contains one regular JSONL file and no symlinks; all 168 records parse.
Historical runtime metrics are not required for this legacy layout.

The complete campaign block in `/audit-input.json` equals
`/audit-campaign-lock.json`.  Its observed SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The observed hashes of the run, task, result, prompt, translator, canonical,
generation records, trace file, legacy records, and usage record all equal
their launcher/result values.

Candidate input integrity also passes:

- `cmp /candidate/prompt.py /reference/prompt.py` exits 0.
- `cmp /candidate/py2mpy.py /reference/py2mpy.py` exits 0.
- Recursive, no-dereference comparison of the two `reference-semantics/`
  trees exits 0.
- Both semantics trees contain the same directory/file paths and types,
  matching per-entry sizes and hashes; neither contains a symlink.

The generation records were read only as untrusted history.  They claim
`KPROVE_PASSED`, but no later finding relies on that marker, the candidate
`prove.log`, or generation-time compiled output.

Exact commands, hashes, entry manifests, trace-event inventory, and exits are
in [stage1-provenance.log](evidence/stage1-provenance.log), produced by
[stage1_provenance.sh](evidence/stage1_provenance.sh).  There is no
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an integer list `arr` of length 1 through 1000, with each element in
`[-1000,1000]`, and integer `k` satisfying `0 <= k <= len(arr)`, return an
ascending list containing the largest `k` elements, preserving multiplicity.
Although one prose sentence calls `k` positive, the numbered condition and
canonical implementation explicitly cover `k = 0`.

The trusted canonical implementation special-cases zero, sorts `arr` in place,
and returns its final `k` entries.  The candidate special-cases zero and returns
`sorted(arr)[-k:]`.  It does not reproduce the canonical's incidental input
mutation, but the source contract specifies the returned list, not mutation.

### Translation identity

In isolated scratch, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

using the trusted translator exits 0.  `cmp` against the submitted
`solution.mpy` exits 0; both have SHA-256
`d74f6342b2088b38daf852a3b75cb63a2eda931babf6bf77877779322f964556`.

### Independent differential

[differential_test.py](evidence/differential_test.py) imports both trusted
`canonical.py` and candidate `solution.py`, and compares each result with its
own oracle.  The exact corpus is retained in
[differential-inputs.jsonl](evidence/differential-inputs.jsonl), SHA-256
`dd823a4ab0afeae8ce70beedc6ff496b914bd1e90e85ffaf440550a680b93617`.

The corpus has 4,976 cases:

- all three documented examples;
- the requested empty-list/zero extension;
- `k = 0`, `k = 1`, `k = len(arr)`, duplicates, and element bounds;
- exhaustive arrays of lengths 1 through 4 over
  `{-1000,-1,0,1,1000}`, for every legal `k`;
- deterministic generated lists through length 1000; and
- explicit length-1000 cases.

The command exits 0 with `mismatches=0`.  Exact output and commands are in
[stage2-fidelity.log](evidence/stage2-fidelity.log).

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/maximum-120-audit`; no candidate-built definition, cache, or
`__pycache__` was copied.  The observed tool version is K `v7.1.293`.

The concrete definition was freshly built with:

```text
kompile /tmp/audit-work/maximum-120-audit/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/maximum-120-audit/runtime-kompiled
```

An auditor-authored program containing the exact candidate body and eight
example/branch/value-boundary assertions was translated with the trusted
translator and run through that definition.  `krun` exits 0 with `.K`,
`NoExc`, and `<exit-code> 0`.

The proof definition was freshly built with:

```text
kompile /tmp/audit-work/maximum-120-audit/verification.k \
  --backend haskell --main-module MAXIMUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/maximum-120-audit/verification-kompiled
```

This exits 0.  The original aggregate target and independently split copies of
each entry claim then give:

```text
kprove .../spec.k --definition .../verification-kompiled \
  --spec-module MAXIMUM-SPEC
#Top
[exit 0]

kprove .../spec-zero.k --definition .../verification-kompiled \
  --spec-module MAXIMUM-SPEC-ZERO
#Top
[exit 0]

kprove .../spec-positive.k --definition .../verification-kompiled \
  --spec-module MAXIMUM-SPEC-POSITIVE
#Top
[exit 0]
```

Compiler warnings concern unused variables or non-exhaustive helpers outside
the submitted program's reachable semantic slice; no build or proof command
failed.  Full bounded output is in
[stage3-reconstruction.log](evidence/stage3-reconstruction.log), with exact
commands in [stage3_reconstruction.sh](evidence/stage3_reconstruction.sh).

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The zero claim starts with an arbitrary `ValSeq` input and `k = 0`, with
`maximum` bound in module scope to a closure over `maximumBody`.  It requires no
additional condition.  It executes the call, allocates an empty list at heap
location 0, returns `ref(0)`, restores the caller frame, and leaves `NoExc`.

The positive claim starts with arbitrary `VS:ValSeq` and `K:Int`, under
`0 < K <= vsLen(VS)`.  It executes the same closure and requires:

- heap location 0 to contain `list(sortVS(VS))`;
- heap location 1 to contain the stride-1 suffix beginning at
  `vsLen(VS)-K` and ending at `vsLen(VS)`;
- the returned value to be exactly `ref(1)`;
- restored scope/stack/return cells and `NoExc`.

Together these claims include every source-contract value of `k` and every
allowed list length/value.  They do not narrow the HumanEval domain to fixed
sizes or examples.  Their broader `ValSeq` quantification is not used to
exclude any intended input.

### Mechanical body identity

The claim does not execute the whole module-load term, but it pins exactly one
function binding, parameter list, and body.  `kast --expand-macros` was run on
the submitted `solution.mpy` as `Module` and on `maximumBody` as `Stmts`.
[compare_constructor_terms.py](evidence/compare_constructor_terms.py) verifies:

```text
module_function_count=1
function_name=maximum
parameters=['arr', 'k']
constructor_terms_equal=True
```

The compared KASTs are retained as
[solution-expanded-kast.json](evidence/solution-expanded-kast.json) and
[maximumBody-expanded-kast.json](evidence/maximumBody-expanded-kast.json).
Thus list-sugar normalization is the only presentation difference.

There are no helper or loop claims.  The return is not free or tautological:
its reference, both allocated heap values, heap counter, scope, stack,
return-state, and exception state are constrained.

### Satisfying states and substitutions

`VS = [-3,5]` satisfies the zero claim with `K=0`, and satisfies the positive
claim with `K=1` and `K=2`.  Ground postcondition evaluation closes with
`#Top`; both Python implementations respectively return `[]`, `[5]`, and
`[-3,5]`.  These exact comparisons are in
[witness_outputs.py](evidence/witness_outputs.py) and
[stage4-pinning.log](evidence/stage4-pinning.log).

### Body sensitivity

An independent mutation changes the body actually placed in the claim's
closure so that the positive branch returns `[]`.  Its definition compiles,
but the original positive result obligation exits 1 with
`WarnStuckClaimState`: execution returns `ref(0)` with only an empty list at
heap 0, rather than the required sorted heap 0 and slice at heap 1.  This is
body sensitivity, not merely an edit to an external source file.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule-inventory.jsonl](evidence/rule-inventory.jsonl), generated by
[inventory_k.py](evidence/inventory_k.py), contains every complete local
`configuration`, `syntax`, `context`, `rule`, and `claim` block from the
supplied `semantics.k`, all 23 helper K files, and candidate
`verification.k`.  Multiline guards and attributes remain in each record.
The inventory has 931 records and SHA-256
`41b544743edafbfc51ebc8c163f7d1769f650f15f08c15747078544467cb6791`.
It explicitly records functions, `total`, symbols, `no-evaluators`, macros,
strictness, simplifications, priorities, concrete rules, and `owise` rules.

Every record has a theorem-slice decision:

| Decision | Count | Meaning |
|---|---:|---|
| `USED-SOUND` | 112 | Declaration/rule manually traced on reachable execution |
| `PROOF-LOCAL-SOUND` | 2 | Exact body macro declaration and expansion |
| `PROOF-LOCAL-SOUND-ON-DOMAIN` | 1 | `vsLen(sortVS(VS))` lemma |
| `SUPPLIED-OPAQUE-BOUNDARY` | 1 | Used `sortVS` primitive declaration |
| `SUPPLIED-OPAQUE-UNUSED-INERT` | 24 | Opaque primitive unreachable here |
| `SUPPLIED-UNUSED-INERT` | 791 | Sort/pattern/control unreachable here |

“Unused inert” is a decision about this theorem: those rules cannot match any
reachable term or cell state of the submitted program and therefore cannot
contribute to closure.  It is not a claim that this deliberately partial MPY
definition is a complete Python semantics for unrelated programs.

### Constructor-to-rule map and reachable control flow

The submitted `Module/FuncDef/Params/Stmts`, `If`, `Compare`, `Name`, `Int`,
`Return`, `ListExpr`, `Call`, `Subscript`, `Slice`, `UnaryOp`, and empty/list
productions all map to declarations in `syntax.k`.

The reachable semantic sequence was checked in full:

1. Normal lookup resolves the exact module binding of `maximum`.
2. The generic call route evaluates callee and arguments left-to-right.
3. The closure rule allocates a fresh scope/frame; `#bindP` binds `arr` and
   `k`.
4. Integer equality and Boolean truthiness select the correct `If` branch.
5. At `k=0`, the empty `ListExpr` allocates exactly heap location 0.
6. For `k>0`, normal lookup walks to the reserved builtins scope and resolves
   `sorted`; the specific sorted dispatch wins over the generic `owise`
   builtin route and allocates `list(sortVS(VS))`.
7. Subscript evaluation dereferences that fresh list, evaluates the negative
   lower bound, leaves upper/step absent, and uses the supplied slice rules.
   The precondition gives `len-K >= 0`, so the relevant clamp guard is
   satisfiable and the stride is 1.
8. `buildVS` selects exactly the indices from `len-K` to `len-1`; the slice
   allocates heap location 1.
9. `Return` pops the exact frame, restores environment/scope location, removes
   the callee scope, and preserves the escaping heap references.

The read/write footprint is therefore explicit: call/lookup read scopes;
the frame temporarily changes `env`, `scopes`, `scopeLoc`, `stack`, and `ret`;
the two constructors change `heap` and `heapLoc`; return restores all
call-control cells; no output or exception cell is fabricated.  The intended
valid inputs do not exercise unsupported error behavior.

Priority and overlap checks pass on this path.  Integer insertion-sort guards
`X <= Y` and `X > Y` are disjoint and exhaustive.  Ref-dereference rules only
preempt after the program has actually allocated a reference.  The specific
`sorted` dispatch precedes the generic `owise` call route.  Slice guard pairs
are complementary under step 1 and the source precondition.

### Candidate proof extensions

`maximumBody` is a syntax macro, not an execution bridge.  Its expansion was
mechanically shown identical to the submitted body.

The sole proof-local simplification is:

```text
vsLen(sortVS(VS)) => vsLen(VS)
```

For intended integer sequences this follows by structural induction from the
supplied concrete insertion sort: the empty sort has length zero; sorting
`vCons(X,R)` sorts `R` and inserts `X`; each guarded insertion case adds
exactly one element, and the integer guards partition the domain.  Thus the
rule does not encode which elements are maximal or bypass the function body.
Its unguarded `ValSeq` domain is broader than the concrete integer/string
equations, but no false conclusion witness exists on the intended integer-list
domain.  The narrower evidence limitation is that no bridge-free,
machine-checked universal length theorem was mounted; here length preservation
is also a direct consequence of the named permutation contract for the
external primitive.

### Used opaque boundary

`sortVS(ValSeq)` is declared `[function,total,symbol(sortVS),no-evaluators]`.
The fixed semantics supplies concrete insertion-sort equations for ground
integer and string sequences, while symbolic proof deliberately retains
`sortVS(VS)`.  This is an external builtin boundary, not a summary of
program-defined candidate code.  The K theorem is interpretation-conditional:
its value-level HumanEval conclusion depends on the contract that `sortVS`
returns an ascending permutation.

The semantics comments refer to a separate Lean proof/notes artifact, but no
such trusted mounted proof was available, so this audit does not credit it.
As finite support, [k-differential.py](evidence/k-differential.py) embeds 16
Python-oracle assertions spanning examples, zero, endpoint `k`, duplicates,
element bounds, and deterministic generated lists.  Fresh `krun` execution
ends at `.K`, `NoExc`, exit code 0.  A larger first batch was killed during
parsing and never treated as proof evidence; that infrastructure attempt is
preserved in [stage5-static-oom-attempt.log](evidence/stage5-static-oom-attempt.log).
The successful exact commands/results are in
[stage5-static.log](evidence/stage5-static.log).

No semantics or proof rule is labeled unsound, because the audit found no
concrete or symbolic false conclusion it enables on the intended domain.

## 6. Fresh non-vacuity test

The auditor-authored [spec-vacuity.k](evidence/spec-vacuity.k)
changes the positive destination's lower slice index from `len-K` to
`len-K+1`.  For the satisfying input `arr=[-3,5], K=1`, the program and original
postcondition produce `[5]`, while the mutated destination demands `[]`.

The parse/spec-build check:

```text
kprove .../spec-vacuity.k --definition .../verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
[exit 0]
```

succeeds.  The actual proof exits 1 with `WarnStuckClaimState`.  Its residual
contains the real leading
`valSeqAt(sortVS(VS), vsLen(VS)-K)` and the unmatched off-by-one
`buildVS(...,vsLen(VS)-K+1,...)`.  This is the expected reachable result
obligation, not a parser error, missing import, timeout, or unrelated crash.

The mutation, witness, exact commands, exit, and residual are retained in
[stage6-nonvacuity.log](evidence/stage6-nonvacuity.log),
[stage6_nonvacuity.sh](evidence/stage6_nonvacuity.sh), and
[mutation_witness.py](evidence/mutation_witness.py).

## 7. Proven versus assumed accounting

### Precisely established

Under the supplied semantics plus the one length simplification:

- Calling the exact submitted `maximum` body with `k=0` reaches a normal return
  of a freshly allocated empty list.
- Calling it with `0<k<=len(VS)` reaches a normal return of a freshly allocated
  stride-1 suffix of `list(sortVS(VS))`, beginning at `len(VS)-k`.
- Lookup, argument evaluation, allocation, slice control, return control, and
  all constrained state cells follow the supplied operational rules.
- The theorem is universal over `VS`/`K` under those entry conditions, not a
  finite unrolling or collection of examples.

This is partial correctness.  Differential tests and generation traces are not
substitutes for these K reachability proofs.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `prompt.py`, `canonical.py`, `py2mpy.py` | Contract, oracle, source-to-MPY identity | Acceptable; independently hashed and compared |
| Integrity-locked supplied MPY semantics | All execution claims | Acceptable selected semantics; reachable slice statically reviewed |
| K builtin Int/Bool/Map/List equality, arithmetic, parser, LLVM/Haskell backends | Rule execution and proof checking | Ordinary toolchain trust |
| `sortVS` means ascending permutation of integer `VS` | Human-facing “largest `k` in ascending order” conclusion; length lemma | Legitimate but concerning external primitive; concrete equations and finite differential support, no mounted universal proof |
| `vsLen(sortVS(VS)) = vsLen(VS)` | Negative-slice normalization and positive claim closure | Sound on intended domain by insertion/permutation reasoning; not independently machine-proved universally |
| Python differential, ground witnesses, K concrete assertions | Fidelity and empirical primitive bridge only | Finite evidence, never treated as universal proof |
| HumanEval return contract does not require mutating caller input | Candidate/canonical implementation bridge | Acceptable reading of prompt and tests |

The proof does not formally establish inside K that `sortVS` is ordered or a
permutation.  Conditional on that named supplied-primitive contract, an
ascending sort's final `k` elements are exactly the maximum `k` elements with
multiplicity, so the formal postcondition matches the HumanEval result
contract.  This informal/externally trusted intent bridge is material enough to
preclude an unqualified `PASS`, but it does not substitute another program,
narrow the source domain, make the result free, or enable a known false
conclusion.

Kit validation gates: Gate A passes (real body, sound reachable rules,
body/result sensitivity); Gate B passes conditionally on the explicit
`sortVS` primitive contract and covers the material source domain; Gate C is
auditable but limited to finite local evidence for that external contract.
Under the benchmark's decision boundary, the appropriate completed-audit
mapping is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
