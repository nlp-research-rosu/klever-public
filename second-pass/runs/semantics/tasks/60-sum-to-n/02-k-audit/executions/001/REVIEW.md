# Independent adversarial audit: 60-sum-to-n

## Executive decision

The candidate contains a legitimate, freshly reconstructible K proof for its
formal nonnegative-integer domain. The proof executes the exact submitted
`solution.mpy`, constrains the returned integer to the closed-form triangular
expression, is sensitive to a body change, and rejects a fresh false
postcondition.

The result is not an unqualified pass. The natural-language prompt annotates
`n` as `int` but never states `n >= 0`; the formal claim does. The candidate
differs from the trusted canonical implementation on negative integers (for
example, at `-2`). Also, the final bridge from the closed form to “sum from 1 to
n” is elementary but not itself formalized in K, and the required generation
metadata/log artifacts are absent. These are intent/provenance limitations, not
ways to prove a false K result on the claimed domain.

The evidence index is
[`evidence/EVIDENCE_INDEX.md`](evidence/EVIDENCE_INDEX.md).

## Stage 1 — Input and provenance integrity

### Mode and trusted-mount boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. There is no infrastructure breach.

The candidate and trusted semantics trees were recursively compared with
symlinks not dereferenced:

```text
diff --no-dereference -r \
  /reference/reference-semantics \
  /candidate/reference-semantics
```

The command exited 0 with no output
([`03_semantics_tree_diff.log`](evidence/03_semantics_tree_diff.log)).
The candidate tree has no missing, additional, changed, mistyped, or symlinked
entry. Candidate `prompt.py` and `py2mpy.py` are respectively byte-identical to
the trusted mounted copies
([`04_prompt_diff.log`](evidence/04_prompt_diff.log),
[`05_translator_diff.log`](evidence/05_translator_diff.log)).

The complete file/type inventories are in
[`01_candidate_inventory.log`](evidence/01_candidate_inventory.log) and
[`02_trusted_inventory.log`](evidence/02_trusted_inventory.log). No candidate
entry is a symlink. The candidate includes untrusted build remnants
`kore-exec.tar.gz` and `__pycache__/`; neither was copied into the reconstruction
or used. `smoke.py`, `smoke.mpy`, and `prove.sh` were treated as claims only.

### Missing required provenance artifacts

The following required reads could not be performed because the files are
absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace (`*trace*.json` or `*trace*.jsonl`) is present.
The exact presence check intentionally exited 1 and is preserved in
[`06_provenance_presence.log`](evidence/06_provenance_presence.log). This is a
candidate bundle/provenance integrity concern. It did not prevent independent
source reconstruction because the trusted prompt, canonical implementation,
translator, supplied semantics, solution, and K proof sources are all present.

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says that `sum_to_n(n: int)` “sums numbers from 1 to n” and
gives:

```text
sum_to_n(30)  = 465
sum_to_n(100) = 5050
sum_to_n(5)   = 15
sum_to_n(10)  = 55
sum_to_n(1)   = 1
```

The trusted canonical body is `sum(range(n + 1))`. For nonnegative integers
this is `0 + 1 + ... + n`; at `n = 0` it is 0. For negative integers,
`range(n + 1)` is empty and the canonical result is 0.

The candidate body is:

```python
def sum_to_n(n: int):
    return n * (n + 1) // 2
```

This is an acceptable different algorithm for nonnegative integers. It is not
equivalent to the canonical function for most negative integers.

### Trusted regeneration

The trusted `/reference/py2mpy.py` regenerated the scratch copy of
`solution.py`; `cmp -s` against the submitted `solution.mpy` exited 0
([`07_regenerate_solution_mpy.log`](evidence/07_regenerate_solution_mpy.log),
[`08_solution_mpy_identity.log`](evidence/08_solution_mpy_identity.log)).
The submitted and regenerated term hashes are both:

```text
e1450114979c8fb27a984a4763e80a16edf6c7d6e3bca86d3246d11bc0552c13
```

### Independent differential test

The reviewer-authored test
[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical entry point and scratch candidate entry point independently. Inputs
are recorded in
[`differential_inputs.json`](evidence/differential_inputs.json): all five
documented examples; boundary/empty cases `-2,-1,0,1,2`; every integer
`0..5000`; 1,000 seeded generated nonnegative integers up to 1,000,000; and 100
seeded generated negative integers.

The run exited 0 for its declared nonnegative domain
([`09_differential.log`](evidence/09_differential.log)):

```text
documented_examples=5 status=PASS
intended_nonnegative_cases=5998 ... mismatches=0
outside_formal_domain_negative_cases=98 ... mismatches=97
boundary_results=[(-2, 0, 1), (-1, 0, 0), (0, 0, 0), (1, 1, 1), (2, 3, 3)]
```

There are no candidate branches. The canonical range’s empty/nonempty boundary
is nevertheless exercised at `-1/0`, and the formal domain boundary is
exercised at `0/1`. The negative divergence is material if the annotation
`int` is read as the complete contract; if “from 1 to n” is read conventionally
as requiring nonnegative `n`, it lies outside the intended domain. Because the
prompt does not resolve that ambiguity, it remains a verdict-level concern.

## Stage 3 — Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reconstruction`. Candidate caches, archives, and compiled
definitions were not copied or reused. The scratch source remained
byte-identical to the candidate source after the experiments
([`24_scratch_source_identity.log`](evidence/24_scratch_source_identity.log));
all source hashes are in
[`25_source_hashes.log`](evidence/25_source_hashes.log).

The live toolchain was independently queried:

```text
K version v7.1.337, build date Thu Jun 18 07:59:56 CDT 2026
```

See [`10_k_versions.log`](evidence/10_k_versions.log).

### Fresh concrete definition

Command:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([`11_runtime_kompile.log`](evidence/11_runtime_kompile.log)). The compiler
reported general non-exhaustive-totality warnings discussed in Stage 5; none is
on the submitted program’s path.

The reviewer-authored
[`concrete_harness.py`](evidence/concrete_harness.py) was translated with the
trusted translator and executed against that fresh definition. It asserts
results for `0,1,2,30,100` and, outside the claim domain, the submitted body’s
result `sum_to_n(-2) == 1`. `krun` exited 0 in a final `.K` configuration with
`NoExc` and exit code 0
([`22_harness_translation.log`](evidence/22_harness_translation.log),
[`23_independent_concrete_harness.log`](evidence/23_independent_concrete_harness.log)).
The separately submitted smoke artifact also ran, but it is only secondary
evidence ([`12_concrete_smoke.log`](evidence/12_concrete_smoke.log)).

### Fresh proof definition and all positive claims

Command:

```bash
kompile verification.k \
  --backend haskell \
  --main-module SUM-TO-N-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0
([`13_verification_kompile.log`](evidence/13_verification_kompile.log)).

The source inventory contains exactly one positive reachability claim and no
helper claims. It was run independently:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-TO-N-SPEC
```

The command exited 0 and printed `#Top`
([`14_positive_claim.log`](evidence/14_positive_claim.log)). The backend also
printed `DecidePredicateUnknown` warnings while simplifying; those warnings did
not replace the complete success signal, and the later false mutations show
that the prover did not indiscriminately close related claims.

Stage 3 result: **PASS**.

## Stage 4 — Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `N` is a K unbounded integer and `N >= 0`.
- `<k>` contains `#runSumToN(N)`.
- the current environment is module scope 0;
- module scope 0 is empty and has parent builtins scope `-1`;
- scope allocator is 1;
- heap and stack are empty, heap allocator is 0;
- there is no pending return or exception, and exit code is 0.

Postcondition:

- `<k>` contains exactly `triangular(N)`, not an existential or free result;
- module scope 0 contains the exact `sum_to_n` closure loaded from
  `solution.mpy`;
- the environment, allocators, empty heap/stack, return state, exception state,
  and exit code are restored/preserved exactly as written in the claim.

Thus the claim does more than assert an implication about a free value. It
requires actual computation consumption, an exact result, and a fully pinned
final state.

### Exact program and call

The reviewer pinning script
[`pinning_check.py`](evidence/pinning_check.py) extracts the balanced argument of
`#loadAll(...)` from `verification.k`. The embedded `Module(...)` equals the
submitted `solution.mpy` modulo layout, and the rule immediately appends:

```text
Call(Name("sum_to_n"), Int(N), .Exprs)
```

Both checks passed
([`16_pinning_and_ground_values.log`](evidence/16_pinning_and_ground_values.log)).
There is no substituted helper body and no loop claim.

The complete real control path is: load the exact function into scope 0; look
up that binding; evaluate `N`; allocate call scope 1; bind `"n"`; evaluate the
strict integer expression; return; pop the call frame; restore transient cells.
The postcondition’s stored closure also pins the loaded body, while the returned
value separately pins its execution.

### Satisfiability and ground substitution

A concrete satisfying initial state is the claim’s written state with `N = 2`.
The precondition `2 >= 0` is true. Substitution gives:

```text
triangular(2) = 3
canonical.sum_to_n(2) = 3
candidate.sum_to_n(2) = 3
```

The same comparison was made for `0,1,2,5,10,30,100,1000`; all four columns
`(N, claim result, canonical result, candidate result)` agree
([`16_pinning_and_ground_values.log`](evidence/16_pinning_and_ground_values.log)).

### Body sensitivity

A distinct mutation changed the executed body from `n + 1` to `n + 2` and also
updated the expected stored closure, leaving the target mathematical result
unchanged. The mutated Haskell definition built successfully
([`17_body_mutation_kompile.log`](evidence/17_body_mutation_kompile.log)).
Its proof exited 1 with `WarnStuckClaimState`; the residual explicitly requires
equality between the `N*(N+2)//2` execution result and `N*(N+1)//2`
([`18_body_mutation_proof_expected_failure.log`](evidence/18_body_mutation_proof_expected_failure.log)).
For example `N=2` witnesses `4 != 3`. This distinguishes execution sensitivity
from mere closure-body pinning.

Stage 4 result: **PASS on the explicit `N >= 0` domain**, with the prompt-domain
limitation recorded in Stages 2 and 7.

## Stage 5 — Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated
[`STATIC_RULE_INVENTORY.md`](evidence/STATIC_RULE_INVENTORY.md) is a
5,000-plus-line verbatim, source-line-indexed inventory of every top-level
dependency, module/import, local syntax declaration, configuration, context,
rule, claim, alias, guard, and attached attribute in the assembled semantics,
all helper K files, `verification.k`, and `spec.k`.

Aggregate inventory:

| Item | Count |
|---|---:|
| syntax declarations | 229 |
| configurations | 1 |
| contexts | 5 |
| ordinary rules | 697 |
| reachability claims | 1 |
| aliases | 0 |
| function-bearing blocks | 147 |
| total-bearing blocks | 108 |
| functional-bearing blocks | 0 |
| simplification-bearing blocks | 0 |
| concrete-bearing blocks | 36 |
| priority-bearing blocks | 45 |
| owise-bearing blocks | 26 |
| symbol declarations | 25 |
| no-evaluator declarations | 22 |

The per-file counts and every individual item appear in that inventory. The
decision covering every inventoried item is
[`STATIC_REVIEW_DECISIONS.md`](evidence/STATIC_REVIEW_DECISIONS.md). Its module
rule counts cover all 695 fixed supplied-semantics rules plus both
candidate-authored rules.

### Candidate extensions

There are only two candidate rules:

1. `#runSumToN(N) => #loadAll(EXACT_MODULE) ~> EXACT_CALL`.
   This is an exact launch expansion. It touches no cell, preserves any
   surrounding continuation, introduces no return/exception/frame effect, and
   does not replace program-defined computation with a value. Exact module and
   binding pinning, plus the body-sensitivity failure, justify its complete
   match domain.
2. `triangular(N) => (...)`. This is a definitional summary, not an operational
   bridge: no program term rewrites to `triangular`. It has one unguarded,
   nonrecursive, nonoverlapping equation over `Int`. The RHS is the same fixed
   `pyMod`/integer expression reached by the real floor-division rule, with
   literal divisor 2.

The candidate adds one runner syntax declaration and one `[function,total]`
integer syntax declaration. It adds no priority, simplification, concrete,
opaque/no-evaluator, or auxiliary-claim extension. Neither rule is an oracle or
answer-bypassing rewrite.

### Used fixed-semantics route

Every constructor in the submitted term maps as follows:

| Construct | Fixed declaration/rule family |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` load/sequencing |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` closure storage |
| `Call`, `Exprs` | `syntax.k`; `call.k` generic callee/argument route |
| `Name("sum_to_n")`, `Name("n")` | `syntax.k`; `core.k` lexical lookup |
| `Return` | strict `syntax.k`; `functions.k` return/pop |
| `BinOp` | sequentially strict `syntax.k`; `operators.k` dispatch |
| integer `+`, `*`, `//` | `int.k`, including transparent `pyMod` |
| `Int(1)`, `Int(2)`, `Int(N)` | `syntax.k`; `core.k` literal rule |

Evaluation order is left-to-right for `BinOp` and explicit for callee/arguments.
The just-loaded lexical binding is selected. Scope allocation, parameter
binding, stack push, return state, frame pop, and scope cleanup are all reflected
in the claim’s cells. The fixed zero-division gap is unreachable because the
divisor is 2. No branch, loop, heap allocation, collection, float, string,
sort, digest, assertion, import, or concrete-only rule is on the proof path.

Overlaps on the path are controlled by distinct operator strings and argument
sorts. Special call interceptors require different syntactic callees; the
generic `[owise]` call is selected for `Name("sum_to_n")`. Cell/heap priority
rules require `"$cells"` or `ref`, neither present. None of the 45 fixed
priority rules is enabled on the target path.

### Opaque symbols and evidence gaps

The fixed semantics declares these 25 symbols:

```text
md5hexCodes, intFloatDiv, divII, floatMod, floatLt, absF,
floorFI, toF, ceilF, subF, divF, addF, mulF, powF, gtF, eqF,
decStrToF, divFloatIntV, intToF, truncF, roundF, roundFN,
sqrtF, sortVS, sortKeyVS
```

All are inert for this integer-only term. The proof result contains none. The
candidate adds no opaque symbol.

The LLVM compiler warned that the fixed declarations `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt` are not exhaustively covered despite
totality declarations. This audit does **not** label those rules unsound: no
concrete or symbolic false equality witness was established, and no such head
is reachable here. The narrower finding is a general supplied-semantics
coverage gap outside this theorem. Unused subset omissions likewise do not
fabricate a result for any used construct.

No candidate rule was found unsound, so there is no candidate false-conclusion
witness to report. The two deliberate false witnesses are instead rejection
tests in Stages 4 and 6.

Stage 5 result: **PASS** for the target proof.

## Stage 6 — Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. The fresh reviewer mutation
[`spec-vacuity.k`](evidence/spec-vacuity.k) changes the result-bearing target:

```k
<k> #runSumToN(N) => triangular(N) +Int 1 </k>
```

All initial/final cells and `requires N >=Int 0` remain reachable and unchanged.
`N=0` is a satisfying witness: the executed result is 0 while the mutated
target is 1.

First, the exact mutated source parsed and built:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SUM-TO-N-SPEC-VACUITY \
  --dry-run
```

Exit status was 0
([`19_vacuity_dry_run.log`](evidence/19_vacuity_dry_run.log)).

Then the real proof command exited 1:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SUM-TO-N-SPEC-VACUITY
```

It produced `WarnStuckClaimState` at the final implication and displayed the
unmet equality between the actual triangular expression and that expression
plus 1
([`20_vacuity_proof_expected_failure.log`](evidence/20_vacuity_proof_expected_failure.log)).
This is the expected semantic residual, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation.

Stage 6 result: **PASS**.

## Stage 7 — Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics and K’s unbounded integer theory, for every
integer `N >= 0`, starting from the exact initial cells in `spec.k`, execution
of the exact submitted module followed by the exact call to its `sum_to_n`
binding reaches a state whose computation result is:

```text
(N * (N + 1) - pyMod(N * (N + 1), 2)) / 2
```

The function closure remains in module scope exactly as submitted; the transient
call scope, stack, return state, heap, exception state, and allocators have the
post-state required by the claim. Because one of consecutive integers is even,
this expression is mathematically `N(N+1)/2`. The K theorem is a
partial-correctness theorem in the requested sense; this straight-line model
also visibly reaches the post-state.

### Trust and assumption ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Byte-identical `/reference/reference-semantics` | Entire K execution | Authorized fixed trust boundary in `SUPPLIED_SEMANTICS` mode. Its active rules were statically traced; concrete and symbolic builds were fresh. |
| K v7.1.337 parser, kompilers, LLVM/Haskell backends, rewriting engine and SMT | Build, `krun`, `kprove`, arithmetic implication | Necessary foundational tool trust. Exact commands/statuses are recorded. |
| K built-in unbounded `Int`, arithmetic, Boolean, Map/List and sequencing primitives | Expression value, scopes/stack, proof closure | Acceptable low-level trust boundary. It does not encode the task answer. |
| Trusted `/reference/py2mpy.py` | Python-source to submitted-term bridge | Submitted term is byte-identical to trusted regeneration; the wrapper independently embeds that term. |
| Candidate `#runSumToN` launch rule | Entry into real program | Not an empirical oracle. It expands to the exact module and call; pinning and body-sensitivity evidence validate it. |
| Candidate `triangular` name | Formal postcondition | Transparent equation, no opacity. The actual program reduces independently to the same fixed expression. |
| Elementary identity `0+...+N = N(N+1)/2` for `N>=0` | Natural-language intent | Informal mathematical bridge, not a separate K claim. It is standard and supported by ground/differential evidence, but the finite evidence is not a universal proof. |
| Canonical/candidate differential sample | Implementation-to-reference evidence | 5,998 nonnegative cases with zero mismatches. Empirical only. It also exposes 97 negative mismatches rather than hiding them. |
| The 25 supplied opaque symbols | No target dependent | Inactive. No branch, state, result, exception, or postcondition in this claim depends on them. |
| Formal precondition `N>=0` and `Int` sort | Theorem scope | Explicit restriction. It excludes negative and non-integer Python inputs; the prompt does not explicitly state the restriction. |

The proof does not establish candidate behavior for negative integers,
floats/bools/other Python objects, or arbitrary CPython features. It does not
turn differential testing, candidate prose, a prior archive, or a generated
trace into proof evidence.

### Final rationale

- A `FAIL / NOT_LEGIT` result is not warranted: clean reconstruction closes;
  the exact submitted program executes; the result is constrained; proof-local
  rules are transparent and sound on their domains; body and postcondition
  mutations fail for the expected obligations.
- A `PASS / LEGIT` result would overstate intent/provenance adequacy: required
  provenance files are missing, the prompt/formal-domain boundary is implicit,
  negative integers expose a canonical divergence, and the summation-identity
  bridge is informal rather than a separate K theorem.
- Therefore the proof is legitimate but carries documented concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
