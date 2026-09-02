# Independent adversarial review: 126-is-sorted

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program over the full HumanEval input domain.
Fresh reconstruction produced `#Top`, the claim mechanically pins the
trusted-regenerated constructor tree, every local rule has been inventoried,
and a fresh false body mutation was rejected at the expected boolean residual.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
generated semantics uses a high-level fused rule for the exact
`all(lst.count(x) <= 2 for x in lst)` generator expression, and the equivalence
between equality-with-insertion-sort and the prose notion of nondecreasing order
is audited by transparent equations and ordinary mathematics rather than a
separate machine-checked connection theorem. Neither limitation admits an
unconstrained value or a witnessed false conclusion on the intended domain.

## 1. Input and provenance integrity

`/audit-input.json` declares `legacy-selected-stage1`,
`GENERATED_SEMANTICS`, problem `126-is-sorted`, and condition `bare`. I read and
inspected the required `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. `usage.json` was present and inspected.
The available legacy records (`legacy-run-input.json` and
`legacy-metrics.json`) were also inspected. Historical runtime metrics are not
required for this layout.

All required launcher and provenance mounts are readable real files or real
directories. No symlink or unsupported entry occurs in the candidate,
reference, or generation-evidence trees. The campaign-lock file has SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly its recorded hash, and its parsed JSON is exactly equal to the
`audit_campaign` block.

The independently checked per-file hashes all match, including:

| Artifact | SHA-256 |
|---|---|
| Trusted canonical | `bed865a8a209214a78c72dba6d004bb72108e1af9fa16082c3f454f188d2c2ad` |
| Trusted/candidate prompt | `050a2b9defc209aa64d0777939ff3387ee7db918434d818789eab7b36578b7ca` |
| Trusted/candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| Run manifest | `16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24` |
| Task manifest | `854bc058a7aea78397b5178ccdb4e46a7f4b449e2de1f6cf1d89d3aded77cae8` |
| Generation result | `c148ceea84d1841ab6e116e3a5da203517b1dac187beaa6031da2df4593194ec` |
| Invocation | `fea1a1b1cd683608c9eeb6fc75063097a9d28b40deceec7b0c5e700f99ac8a98` |
| Generation output log | `d639c64300e51de7a68d67848eaf9c5fa327fa2132a6c64609168bcc3aa19ac4` |
| Structured JSONL trace file | `bf2c2fbfb27961163bfa15c4913ecd2db1d2b692daceb3362337a65291b84997` |

The mounted candidate independently reproduces the generation invocation and
result’s retained-workspace digest
`b75b9ad4eb06e857e342dbeae39aa7daa067d5ef12c1c7075e0385d112ef5a94`.
The structured trace reproduces `usage.json`’s source-trace digest
`6a3f0099f3568ab8c576e074feb4d921c001174bcc6ec776bba041364f869c80`,
and every evidence-file hash in `generation-result.json` matches. The two
additional audit-input aggregate fields (`candidate_tree_sha256` and
`generation_codex_trace_sha256`) use an aggregate encoding not specified in the
launcher document; the independently reproducible retained-workspace,
source-trace, and per-file checks above bind the mounted contents without
relying on that undocumented encoding.

The trace is valid JSONL with 234 records, one session ID, and 40 extracted tool
calls. Generation reports and its prior `#Top` were treated only as untrusted
claims. Full evidence is in
[integrity_check.log](/audit-output/evidence/stage1/integrity_check.log) and
[generation_records_inspection.log](/audit-output/evidence/stage1/generation_records_inspection.log).

The candidate prompt and translator are byte-identical to the trusted mounts.
As required for generated-semantics mode,
`/reference/reference-semantics` is absent; no hidden or inferred reference
semantics was used. All required proof artifacts are present as real files.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is:

> For any finite list of non-negative integers, return true exactly when the
> list is nondecreasing and no integer occurs more than twice.

“Ascending” must mean nondecreasing here because the prompt explicitly expects
`[1, 2, 2, 3, 3, 4]` to return true. The trusted canonical counts
multiplicities, rejects a count above two, and checks every adjacent pair.

The candidate implementation is:

```python
def is_sorted(lst):
    return lst == sorted(lst) and all(lst.count(x) <= 2 for x in lst)
```

On ordinary finite integer lists, equality with `sorted(lst)` is equivalent to
nondecreasing order, and the generator enforces the same multiplicity bound as
the canonical. The different algorithm is therefore acceptable. It introduces
no domain restriction; its quadratic counting cost is irrelevant to partial
correctness.

Fresh translation used the trusted command:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -s regenerated-solution.mpy solution.mpy` also exited 0, and
both files have SHA-256
`e1fb2ad3b994d9f517e5d395c016188311410e12c5bac7168fd689623f4cbe4d`.

The independent differential script imports the trusted canonical and scratch
candidate entry points and compares both to a separately written
adjacent-order/`Counter` oracle. It exercised:

- 21 documented and branch-boundary cases;
- all 21,845 lists of lengths 0 through 7 over values 0 through 3; and
- 10,000 deterministic generated lists of lengths 0 through 30 over values
  0 through 100.

All 31,866 comparisons agreed, including empty/singleton lists, ordered and
inverted pairs, duplicate counts 1/2/3, zero, and very large integers.
`MISMATCH_COUNT=0`, exit 0. See
[differential_test.py](/audit-output/evidence/stage2/differential_test.py) and
[stage2.log](/audit-output/evidence/stage2/stage2.log).

## 3. Clean proof reconstruction

Only explicit source artifacts were copied to
`/tmp/audit-work/candidate-fresh`; no candidate-provided kompiled definition or
cache was copied or used. K reports version 7.1.293.

The generated semantics was freshly built for concrete execution:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
```

Exit: 0.

Twelve fresh `krun solution.mpy` executions covered empty, singleton, exactly
two duplicates, three duplicates, order inversions, the prompt’s representative
lists, zero, and very large integers. Every run exited 0 and its `BoolVal`
agreed with the canonical, candidate Python function, and direct oracle.
`FAILURE_COUNT=0`. The first reviewer run had a logging-parser typo that looked
for a literal `\s`; the visible K results were correct, the parser was fixed,
and the clean definition was not rebuilt or altered. The successful comparison
is preserved in
[concrete-semantics-fixed.log](/audit-output/evidence/stage3/concrete-semantics-fixed.log);
the initial reviewer-side error remains in
[reconstruction.log](/audit-output/evidence/stage3/reconstruction.log).

The proof definition was independently built:

```text
kompile --backend haskell semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled
```

Exit: 0. `spec.k` contains exactly one positive claim. The required proof was:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC
```

Actual output and status:

```text
#Top
POSITIVE_PROOF_EXIT_STATUS=0
POSITIVE_PROOF_TOP_COUNT=1
```

See [positive-claim.log](/audit-output/evidence/stage3/positive-claim.log) and
[proof-reconstruction.log](/audit-output/evidence/stage3/proof-reconstruction.log).
Thus every positive target claim closes under a clean source build.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause. Its universal `IS:IntList` therefore ranges
over every finite constructor list of mathematical integers. This is broader
than, and does not narrow, the prompt’s non-negative-integer domain.

The starting state is the single `<k>` cell containing:

```text
Run(exact submitted is_sorted module, PyList(IS))
```

The destination fixes the returned value to:

```text
BoolVal(isSortedContract(IS))
```

Unfolding the fully defined functions makes that:

```text
BoolVal(
  eqIntLists(IS, sortInts(IS))
  andBool countsAtMost(IS, IS, 2)
)
```

The result is not free, existential, tautological, or guarded by a one-way
implication. There are no auxiliary or loop claims to bypass the entry claim.
The source has no explicit Python loop; its generator is handled by the audited
semantic rule discussed in Stage 5.

The precondition is realizable. For example,
`IS = Nil` gives the exact initial state
`Run(module, PyList(Nil))`; fresh K and both Python implementations return true.
Other concrete substitutions agree:

| `IS` | Claimed result | Canonical | Candidate Python | Fresh K |
|---|---:|---:|---:|---:|
| `Nil` / `[]` | true | true | true | true |
| `[0, 0]` | true | true | true | true |
| `[0, 0, 0]` | false | false | false | false |
| `[2, 1]` | false | false | false | false |

### Mechanical program identity

A reviewer script extracted the `Module(...)` term actually under the claim’s
`Run`. After insignificant-whitespace normalization, its SHA-256 equals that of
trusted-regenerated `solution.mpy`:

```text
a16dba0bacf2edcdc318f32ddba854c2ff3b3842dbcdcd41eca8c045c8528b32
```

The complete 27-element constructor sequence is identical. Both terms were
then independently parsed with `kast --module MPY-SYNTAX --sort Pgm --output
kore`; the KORE files are byte-identical with SHA-256
`166bf0f7d6aa2dc5247b332192e01cede8d9864a249ae33ded9e71bdafc15d4d`.
All commands exited 0. See
[pinning_check.py](/audit-output/evidence/stage4/pinning_check.py) and
[pinning.log](/audit-output/evidence/stage4/pinning.log).

The Stage 6 mutation changes `Int(2)` inside this executed constructor term,
not merely `solution.py`, and changes the reachable boolean. This provides
body-sensitivity evidence in addition to textual pinning.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[RULE_INVENTORY.md](/audit-output/evidence/stage5/RULE_INVENTORY.md). Its
mechanical source scan is
[inventory_check.log](/audit-output/evidence/stage5/inventory_check.log).
Totals are:

```text
TOTAL_RULE_COUNT=32
TOTAL_SYNTAX_DECLARATION_COUNT=24
TOTAL_FUNCTION_DECLARATION_COUNT=13
```

There are 15 list-domain rules, 14 operational/expression rules, and 3
verification definitions. There is one single-cell configuration. There are no
local `[total]`, `[functional]`, `[simplification]`, `[concrete]`, `[owise]`,
`[anywhere]`, priority, macro, alias, context, or opaque declarations. Every
syntax declaration and every rule is assigned an ID, source line, domain,
overlap/coverage analysis, descent argument, state/value effect, and decision
in the inventory.

The construct map is complete for `solution.mpy`:

- `Module`, `FuncDef`, `Params`, `CellVars`, and `FreeVars` are recognized by
  the `Run` rule;
- `Return` is consumed by `EvalStmt`;
- `Name`, `Int`, `BoolOp`, `Compare`, and `sorted` calls have explicit
  evaluator equations;
- `Attribute`, `GenExp`, `CompFor`, the inner `count`, and outer `all` are
  consumed by the exact fused pattern; and
- `PyList`, `Cons`, and `Nil` represent all formal inputs.

The helper equations are structurally recursive. Insertion’s `<=`/`>` guards
and count’s `==`/`=/=` guards are disjoint and exhaustive over K integers.
Constructor cases are disjoint. Every recursive call descends through a finite
tail. The exact program’s functions are therefore covered and terminating.

The configuration omits heap, stack, I/O, and allocation cells because the
exercised program is pure. Its environment is the explicit K `Map` passed to
`EvalStmt`; no rule mutates it. Python left-to-right/short-circuit distinctions
cannot change the exact program’s value or state because both operands are
boolean-valued, the count traversal is pure and total on plain integer lists,
and there are no exceptions on the intended domain. Unsupported other ASTs may
stick visibly; generated-semantics mode permits missing unused constructs.

The most important rule is `semantic.k:83-91`. It fuses the exact term
`all(source.count(x) <= LIMIT for x in source)` into
`countsAtMost(IS, IS, LIMIT)`. This does not return the task answer or introduce
a fresh symbol. `countInt` and `countsAtMost` have exhaustive recursive
equations, so the rule’s result is fixed for every finite integer list. Checking
every duplicate occurrence affects cost, not the conjunction. The source
binding and no-filter sentinel are pinned in the pattern. I find no false
conclusion witness over its complete `PyList`/integer match domain.

`ascending`, `duplicateBound`, and `isSortedContract` are likewise transparent
definitions, not opaque oracles. The proof closes because execution and the
postcondition reduce to the same fully defined mathematical operations. The
ordinary-mathematics bridge is:

- insertion sort returns a nondecreasing permutation;
- a finite list equals that ascending sort exactly when it was already
  nondecreasing; and
- checking each occurring value’s `count <= 2` is exactly the prompt’s
  duplicate condition.

These facts are sound, and the differential evidence found no counterexample.
They are not separately stated as K lemmas, which is the first non-fatal
concern. The fused rule is not connected to a lower-level generic
generator/method-call semantics by an auxiliary K theorem, which is the second
non-fatal concern. Because this is the declared generated semantics rather than
a proof-local rewrite layered over a supplied fixed semantics, and because the
equation is transparent and universally justified by its recursive definitions,
these limitations do not make the proof illegitimate.

No rule is labeled unsound, so no false-conclusion witness is being omitted.
The narrower evidence limitations are stated above.

## 6. Fresh non-vacuity test

I did not rely on the candidate’s `mutation-spec.k`. The fresh reviewer mutation
is preserved as
[audit-false-spec.k](/audit-output/evidence/stage6/audit-false-spec.k).
It changes the limit inside the program term actually executed by the claim
from `Int(2)` to `Int(1)`, keeps the original result obligation, and grounds the
input to `[0, 0]`.

This witness satisfies the original entry precondition. The original program
and postcondition are true, while the mutated body returns false.

The mutation first built successfully:

```text
kprove audit-false-spec.k \
  --definition verification-haskell-kompiled \
  --spec-module AUDIT-FALSE-SPEC --dry-run
DRY_RUN_EXIT_STATUS=0
```

The actual proof command then exited 1:

```text
kprove audit-false-spec.k \
  --definition verification-haskell-kompiled \
  --spec-module AUDIT-FALSE-SPEC
```

Relevant actual residual:

```text
Warning (WarnStuckClaimState)
<k>
  BoolVal ( false ) ~> .K
</k>
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
MUTATED_PROOF_EXIT_STATUS=1
```

There was no parser, import, timeout, or unrelated failure. See
[false-mutation-dry-run.log](/audit-output/evidence/stage6/false-mutation-dry-run.log),
[false-mutation-proof.log](/audit-output/evidence/stage6/false-mutation-proof.log),
and [mutation-run.log](/audit-output/evidence/stage6/mutation-run.log).
The proof is therefore non-vacuous and body-sensitive.

## 7. Proven versus assumed accounting

### Precisely what is proved

Under the freshly built K definition, for every finite `IS:IntList`, executing
the exact constructor term regenerated from the submitted `solution.py` on
`PyList(IS)` reaches:

```text
BoolVal(
  eqIntLists(IS, sortInts(IS))
  andBool countsAtMost(IS, IS, 2)
)
```

This is a universal theorem, not a finite-size proof. Its domain includes all
non-negative integer lists required by HumanEval and even negative K integers.
Interpreting the recursively defined operations as ordinary integer-list sort,
equality, count, and conjunction yields exactly the requested result. The claim
is a partial-correctness result; it does not claim a complexity bound or model
arbitrary Python objects, monkeypatched builtins, list subclasses, mutation,
I/O, or exceptions outside the stated input domain.

### Trust ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and reachability logic | Parsing, execution, and `#Top` | Necessary low-level trusted toolchain; version matches the campaign lock. |
| Imported K `INT`, `BOOL`, and `MAP` modules | Integer arithmetic/comparison, boolean conjunction, environment lookup | Acceptable standard primitive boundary. No task answer is imported. |
| Trusted `py2mpy.py` | Python-AST-to-constructor identity | Acceptable and exact for this source: candidate translator hash matches and trusted regeneration is byte-identical. |
| `PyList(IntList)` representation | Restricts values to finite mathematical integer lists | Adequate for the prompt’s plain list-of-integers domain; deliberately excludes irrelevant Python object behavior. |
| `sorted` → `sortInts` (`semantic.k:77-78`) | First conjunct and returned result | Transparent insertion-sort equations plus concrete K/Python agreement. Acceptable. |
| Fused generator/count rule (`semantic.k:83-91`) | Duplicate branch and final result | Fully value-fixed by recursive equations and sound by structural audit; no opaque oracle. Concerning only because no separate lower-level machine-checked connection theorem exists. |
| Equality-with-sort ↔ nondecreasing prose contract | Human-facing intent | Ordinary finite-list mathematics and 31,866 zero-mismatch differential cases support it. Concerning only because it is not a separate K theorem. |
| Finite differential evidence | Candidate/canonical/oracle bridge on tested inputs | 31,866 cases, zero mismatches. Empirical support only, not substituted for the universal K proof. |
| Finite K/Python concrete evidence | Generated-semantics execution bridge | 12 targeted normal/boundary cases, zero mismatches. Empirical support only; static rule review supplies the universal argument. |

There are no opaque symbols, fresh result variables, assumed lemmas,
simplification rules, totality assertions, or proof-only operational rewrites.
The candidate’s prose, prior traces, and prior `#Top` are not in the trust
ledger.

### Validation gates and verdict rationale

- Gate A, real-program soundness: **PASS**. The exact body executes under the
  generated definition, every result-bearing function has exhaustive equations,
  the claim is satisfiable/result-constraining, parsed program identity holds,
  and the false body mutation is rejected.
- Gate B, intent adequacy: **PASS**. The formal domain does not narrow the
  HumanEval domain, and the result is equivalent to the prose contract.
- Gate C, trust/evidence auditability: **PASS with disclosed limitations**.
  Commands, scripts, logs, finite evidence scopes, and the full trust boundary
  are preserved. The two unmechanized semantic/intent bridges warrant concerns
  but do not admit a false result.

The evidence manifest is
[evidence-manifest.sha256](/audit-output/evidence/stage7/evidence-manifest.sha256).
There is no bounded-size restriction, substituted program, failed positive
claim, vacuity, or material semantic unsoundness. The candidate is legitimate,
with the non-fatal limitations above.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
