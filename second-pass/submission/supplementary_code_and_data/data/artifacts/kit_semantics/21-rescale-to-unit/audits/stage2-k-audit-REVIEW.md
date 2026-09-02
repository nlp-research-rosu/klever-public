# Independent adversarial review: 21-rescale-to-unit

## Overall assessment

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program on the material successful-return domain: finite
homogeneous float lists of length at least two whose computed extrema differ.
The proof was reconstructed from source, closes over an unbounded symbolic
tail, embeds the submitted MPY constructor term, executes the real body, and
constrains both the returned reference and its heap contents.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
Haskell proof names the supplied float min/max primitives with opaque aliases,
and because it proves the exact canonical rescaling formula rather than a
separate floating-point theorem that the observed extrema are always exactly
0 and 1. Those are explicit, conditional trust/intent bridges; they do not
permit a false program-execution conclusion or substitute another body.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and `mount_reference_semantics: true`.
The required trusted `/reference/reference-semantics` tree is present. There is
therefore no rendered-mode contradiction and no infrastructure breach.

I read and independently checked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the complete structured trace
  `/generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T07-21-59-019fadd3-151d-7843-8bed-e9c328e1a798.jsonl`.

The reviewer script `evidence/provenance_check.py` parsed all 522 JSONL trace
records and checked every pipeline-v3 required record. Command:

```text
python3 /audit-output/evidence/provenance_check.py
```

It exited 0 and ended with `PROVENANCE_CHECK_PASS`; bounded output is in
`evidence/provenance_check.log`.

The campaign-lock JSON exactly equals the `audit_campaign` block and its
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All directly recorded hashes for the canonical, prompt, translator, run/task
manifests, stage result/invocation, generation logs, metrics, usage, and trace
file match their mounted bytes.

The candidate and trusted `prompt.py` files are byte-identical; so are their
`py2mpy.py` files. Recursive type-and-content comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found 25 entries, no missing or additional
entry, no type change, no byte change, and no symlink. This comparison does not
bless `verification.k`, which is reviewed separately below.

Independent per-file SHA-256 manifests are preserved as:

- `evidence/candidate_file_hashes.txt` (777 candidate files plus command
  header/status);
- `evidence/reference_file_hashes.txt`; and
- `evidence/generation_file_hashes.txt`.

Generation reports and candidate prose/logs were treated only as untrusted
claims. None was used as a build input or as proof of correctness.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks `rescale_to_unit(numbers: List[float])` to transform a
list of at least two numbers linearly so its minimum becomes 0 and maximum
becomes 1. The trusted canonical computes:

```text
lo = min(numbers)
hi = max(numbers)
[(x - lo) / (hi - lo) for x in numbers]
```

The submitted `solution.py` computes the same expression in a `for` loop. Its
extra `number = numbers[0]` initializes the loop target before the loop. It is
unobservable on the documented nonempty domain and does not alter the earlier
`min`/`max` exception on an empty list.

There is an unavoidable source-contract edge ambiguity: an all-equal list has
at least two elements, but no transform can make its sole distinct value both
0 and 1. The trusted canonical and submitted implementation both raise
`ZeroDivisionError` for such a nonempty list. I therefore treat differing
extrema as the implicit successful-return domain of the prompt/canonical, not
as a material finite-size restriction. The proof does not establish
exceptional behavior for equal-extrema lists.

### Trusted regeneration

From `/tmp/audit-work/proof` I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`213f41f35632675980ad448036dce91cb9e9847f64b1c86627caa8032ec5837c`.
See `evidence/translator_regeneration.log`.

### Independent differential test

`evidence/differential_test.py` independently loads the trusted canonical and
submitted entry points. It records every generated input in
`evidence/differential_inputs.json` (SHA-256
`471ec31cf54b59150e43f61698b5bf6c5c9d5557e00c40cefc5a5e414da3057e`).
It covers the documented example; empty, singleton, two-element, equal-range,
ascending/descending, duplicate-extrema, signed-zero, subnormal, overflow,
infinity, and NaN boundaries; and 2,000 deterministic generated lists of
length 2 through 25.

```text
python3 /audit-output/evidence/differential_test.py
```

Exit was 0: 2,013 cases, 2,004 canonical returns, 9 matching exception cases,
and zero mismatches. The documented result was
`[0.0, 0.25, 0.5, 0.75, 1.0]`. Full bounded output is in
`evidence/differential_test.log`.

This run also records a floating-point intent limitation:
`[-1e308, 0.0, 1e308]` yields `[0.0, 0.0, nan]` in both Python
implementations because the range overflows. Differential equality supports
program-to-canonical fidelity, not a universal theorem about the natural
language extrema property.

## 3. Clean proof reconstruction

Only candidate source files (`solution.py`, `solution.mpy`, `verification.k`,
and `spec.k`) and the trusted translator/prompt/canonical/semantics were copied
to `/tmp/audit-work/proof`. Candidate `runtime-kompiled`,
`verification-kompiled`, caches, logs, and archives were neither copied nor
used.

The live tools were independently present at K version 7.1.293. Fresh commands:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit 0; see `evidence/kompile_llvm.log`.

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit 0; see `evidence/kompile_haskell.log`.

Reviewer-authored concrete tests were translated with the trusted translator:

```text
python3 py2mpy.py /audit-output/evidence/concrete_audit.py > concrete-audit.mpy
krun concrete-audit.mpy --definition runtime-audit-kompiled
```

Both exited 0. The documented case, length-two ascending/descending cases,
negative values, and duplicate extrema all passed; the final configuration had
`.K`, `NoExc`, and exit code 0. See `evidence/concrete_krun.log` and
`evidence/concrete_krun_checks.log`.

The required positive target is a mutually supporting set of four claims. I
ran it intact:

```text
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0 (`evidence/kprove_all.log`). I also selected
`SPEC.min-float-loop`, `SPEC.max-float-loop`, and `SPEC.scale-loop` one at a
time; each printed `#Top` and exited 0
(`evidence/kprove_min_float_loop.log`,
`evidence/kprove_max_float_loop.log`, and
`evidence/kprove_scale_loop.log`).

An isolated diagnostic selecting only `SPEC.rescale-to-unit` was interrupted:
`--claims` removes the three supporting circularities, so it is not the
candidate's positive target and was beginning unbounded loop unrolling. This
diagnostic is explicitly marked in
`evidence/kprove_rescale_to_unit.log`; the intact four-claim target above is the
relevant independent reconstruction.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `min-float-loop`: for any finite all-float tail `VS` and float accumulator
   `M`, the supplied `#minAccF(list(VS), M)` iterator fold reaches
   `minTailF(VS, M)`, framing the rest of the configuration.
2. `max-float-loop`: the analogous statement for `#maxAccF` and `maxTailF`.
3. `scale-loop`: in a scope containing the actual loop variables and a heap
   list at `H`, the exact submitted `for` body consumes any finite all-float
   `VS`, appends one exact `(number - LO) / (HI - LO)` value per element,
   leaves the loop target at `lastVal(VS, CURRENT)`, and leaves the active
   continuation intact.
4. `rescale-to-unit`: starting from the complete initial MPY configuration,
   load the exact module and call `rescale_to_unit` on
   `vCons(FIRST:Float, vCons(SECOND:Float, REST))`. If `REST` is all floats and
   the interpreted extrema differ, normal execution returns `ref(0)`, allocates
   exactly one result list at heap location 0 containing the `scaleAcc`
   sequence, restores the caller frame, and ends with empty stack, `noRet`,
   `NoExc`, and exit code 0.

The postcondition is result-constraining: it fixes the returned value to
`ref(0)` and fixes heap location 0 to an ordered sequence whose recursive
equations fix every element. It is not a free variable, tautology, or
one-directional implication standing in for equality.

### Mechanical program identity

`evidence/program_term_compare.py` mechanically extracts the balanced
constructor term under the entry claim's `#loadAll`, normalizes only
whitespace/comments and the parser-equivalent empty syntax
`ListExpr()`/`ListExpr(.Exprs)`, and compares it to regenerated
`solution.mpy`. It also compares the function name, parameter, and entire
closure body on the post-state side.

```text
python3 /audit-output/evidence/program_term_compare.py
```

Exit 0 reported `module_constructor_identity=yes` and
`closure_body_identity=yes`; see `evidence/program_term_compare.log`. The claim
therefore pins the submitted binding and body, not a substituted summary
program.

### Satisfying states and concrete substitution

`evidence/claim_witness.py` exhibits:

- entry substitution `FIRST=2.0`, `SECOND=-2.0`, `REST=[6.0, 2.0]`, for which
  all floats hold and extrema `-2.0` and `6.0` differ;
- satisfiable ground states for both extrema-loop claims and the scale-loop
  claim; and
- the interpreted claim heap `[0.5, 0.0, 1.0, 0.5]`.

Both trusted canonical and submitted Python return exactly that list. The
command exited 0; see `evidence/claim_witness.log`.

The same evidence records matching boundary exceptions: empty lists raise
`ValueError`; singleton and all-equal lists raise `ZeroDivisionError`.

### Body sensitivity

I created a fresh `evidence/spec-body-audit.k` that changes both occurrences of
the actually executed body from `Return(Name("result"))` to
`Return(Name("numbers"))`, leaving the target result/heap obligation intact.

```text
kprove spec-body-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-BODY-AUDIT
```

The proof reached a returned input `list(...)`, emitted
`WarnStuckClaimState`, and exited 1. See `evidence/body_sensitivity.log`.
Thus body sensitivity was tested on the claim term actually executed, not by
editing an unused external source file.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/build_rule_inventory.py` inventories every source-level `requires`,
module/import, configuration, syntax declaration, context, rule, and claim
from all 24 supplied K files plus `verification.k` and `spec.k`. Its output
`evidence/rule_inventory.tsv` contains a source location, full normalized
statement (including guards/attributes), subtype, decision, and decision basis
for every record.

Inventory totals are:

```text
26 sources
238 syntax declarations
722 rules
5 contexts
1 configuration
4 claims
```

Rule subtypes include 635 ordinary, 45 priority, 35 concrete-only, and 7
simplification rules. Syntax classification includes all function/total
declarations and 28 opaque-symbol declarations. The generating command exited
0; counts per source are in `evidence/rule_inventory_summary.txt` and
`evidence/build_rule_inventory.log`.

Every supplied-semantics row is marked `ACCEPTED_SUPPLIED_LEVEL`: it is part of
the selected, byte-identical supplied baseline, not a candidate modification.
I nevertheless read the complete source and traced every used constructor
through its concrete rules. `evidence/used_construct_map.md` gives the
constructor-level map for the actual module, import, definition, call,
allocation, lookup, min/max folds, index, loop, append, arithmetic, return, and
frame pop.

### Used fixed-semantics path

- Configuration and allocation account for every changed cell. The entry
  starts from the complete initial configuration, allocates result heap 0,
  advances `heapLoc` to 1, restores environment/scope location, and constrains
  stack, return, exception, and exit-code cells.
- `seqstrict` on `BinOp` and the common argument evaluator preserve
  left-to-right operand/argument evaluation. Call routing performs real name
  lookup, builtin selection, argument binding, function-frame creation, body
  execution, return, and frame pop.
- `ImportFrom("typing","List")` uses the supplied non-math no-op. CPython would
  bind `List`, but the name is typing-only and is never read, so this is
  semantically inert for the submitted body.
- The two-element minimum input makes `numbers[0]` in bounds. The supplied
  compiler warns that the globally total `valSeqAt` lacks an empty constructor
  equation, but that unmatched case cannot occur under this entry precondition.
- The supplied list iterator, target binder, append rule, and heap write
  exactly account for loop control and state. The scale circularity is itself
  proved with an arbitrary framed continuation; there is no proof-local abrupt
  return or continuation-discarding bridge.
- The source body's subtraction and division remain the supplied `subF` and
  `divF` operations. Min/max seed, traversal, and completion remain the supplied
  iterator rules.

### Every proof-local declaration and rule

The 42 `verification.k` inventory records are individually marked
`REVIEWED_SOUND` with their basis:

- `allFloatVS` and `definedProjectFloat` are exhaustive total predicates.
- `projectFloatTotal` is a guarded total name for the existing Val-to-Float
  projection. Its `#Ceil` characterization is exactly the supplied `isFloat`
  sort predicate. The concrete/symbolic orientations agree on their overlap
  and are used only under `isFloat`.
- The dynamic-sort `applyBin("-")` simplification is the supplied Float
  subtraction rule after that guarded projection. On a statically Float first
  argument it overlaps the fixed rule with the same `subF(F1,F2)` result.
- `minFOpaque` and `maxFOpaque` are pure, result-bearing aliases for the
  supplied `minFloat` and `maxFloat` primitives. They match no configuration,
  continuation, environment, or state cell. Their two simplification rules
  conservatively name the fixed two-Float primitive values; no other equation
  constrains the aliases.
- `minTailF`, `maxTailF`, `minVF`, and `maxVF` are exhaustive, guard-disjoint,
  constructor-descending pure definitions. Their non-float/empty totalization
  cases do not claim Python min/max behavior and are never used by the entry
  claim.
- `scaleAcc` is exhaustive and constructor-descending. Its float case uses the
  same `subF`, `divF`, and `valSeqConcat(..., singleton)` terms as the executed
  expression and supplied append rule. Its non-float totalization is excluded
  by `allFloatVS`.
- `lastVal` is an exhaustive constructor-descending definition of Python's
  final loop-target binding.

There are no candidate-local priority rules, K-cell operational bridges,
whole-call intercepts, result fabrication rules, axioms for the final answer,
or rules that pop/return without executing the body. Total functions have
constructor coverage or are explicitly opaque trusted primitives. Guards are
disjoint where right-hand sides differ; overlapping dynamic/static
subtraction rules agree.

I found no unsound candidate-local rule, so there is no claimed unsoundness for
which a false-conclusion witness is required. The narrower evidence gap is the
conditional interpretation of opaque float primitives discussed in stage 7.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. Starting from the scratch
copy, I created `evidence/spec-false-result-audit.k`, changed the entry module
name, and changed only the result-bearing postcondition from `=> ref(0)` to the
demonstrably false `=> noneV`. The satisfying input from stage 4 returns
`ref(0)`.

First, the mutation built successfully:

```text
kprove spec-false-result-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT-AUDIT \
  --dry-run
```

Exit 0; see `evidence/false_mutation_build.log`.

Then:

```text
kprove spec-false-result-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT-AUDIT
```

`kprove` exited 1 with `WarnStuckClaimState`. The residual specifically has
`<k> ref ( 0 ) ~> .K </k>` and cannot unify with `noneV`; it is not a parser
error, missing import, timeout, or unrelated crash. See
`evidence/false_mutation_proof.log`, which ends with
`EXPECTED_FALSE_RESULT_OBLIGATION_FAILURE_OBSERVED`.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics extended by the reviewed pure definitions and
float aliases, for every finite K `ValSeq` tail and every input

```text
vCons(FIRST:Float, vCons(SECOND:Float, REST))
```

such that `allFloatVS(REST)` and the interpreted extrema are unequal, if the
entry execution reaches normal completion, it returns `ref(0)`. Heap location
0 contains, in input order, exactly the recursively defined sequence

```text
(element - minVF(INPUT)) / (maxVF(INPUT) - minVF(INPUT))
```

using the supplied Float primitives. Module loading, binding, all program
statements, both extrema traversals, index access, loop iterations, every
append, return, and frame restoration execute under fixed semantics. The
symbolic tail is unbounded; this is not finite unrolling. As a partial
correctness theorem it does not prove termination.

### Trust ledger

| Boundary | Dependents and effect | Assessment/evidence |
|---|---|---|
| Entire byte-identical supplied MPY semantics | All control, state, calls, allocation, and primitive dispatch | Accepted by the rendered `SUPPLIED_SEMANTICS` boundary; integrity checked recursively. Used rules were traced statically and exercised concretely. |
| Supplied `Float`, `subF`, `divF`, `eqF`, `minFloat`, and `maxFloat` primitives/hooks | Extrema precondition and every output element | Legitimate low-level numeric trust boundary. LLVM concrete execution checks several distinct outcomes, but no Haskell symbolic IEEE theory is available. |
| Proof-local `minFOpaque`/`maxFOpaque` aliases | Both fold summaries, precondition, and final heap formula | Sound conservative names conditional on denoting the supplied min/max primitives. No independent universal numerical theorem is proved; this is the main concern. |
| Guarded `projectFloatTotal` and cast simplifications | Float extraction in folds/arithmetic | Reviewed derived sort projection; guard is exactly `isFloat`; overlaps agree. |
| Trusted `py2mpy.py` translation | Source-to-constructor identity | Trusted benchmark bridge; regeneration is byte-identical and the embedded claim term is mechanically identical. This does not itself prove general translator correctness. |
| CPython canonical as behavioral oracle | Program-fidelity and intent bridge | 2,013 independent cases, zero mismatches, including errors and numeric boundaries. Finite evidence only. |
| Formula-to-natural-language extrema property | Human-facing intent | The exact canonical formula is proved structurally. The separate algebraic/IEEE claim “min is exactly 0 and max exactly 1” is informal and fails on overflow/non-finite edge cases, as the recorded `[-1e308,0,1e308]` example shows. Material ordinary finite HumanEval cases are covered. |
| No termination theorem | Liveness | Acceptable for the requested partial-correctness proof; no termination claim is made. |

### Gate decisions and verdict rationale

- Gate A (real-program soundness): PASS. Fresh `#Top`, exact constructor
  identity, complete state accounting, reviewed extensions, satisfying states,
  body sensitivity, and a rejected false result all support this decision.
- Gate B (intent adequacy): PASS for the material canonical successful-return
  domain, with a non-fatal limitation. The theorem fixes the canonical formula
  over unbounded list length. Equal-extrema inputs are the prompt/canonical's
  inconsistent/exceptional edge, not silently claimed as successful returns.
  IEEE overflow/non-finite behavior and the formula-to-English property remain
  an explicit informal bridge.
- Gate C (trust/evidence auditability): PASS with a documented trust-boundary
  concern. Every unproved primitive and empirical bridge is named with its
  dependents and reproducible evidence; testing is not represented as a
  universal K proof.

The concerns do not make a false K conclusion provable, bypass execution,
substitute another program, bound the symbolic list length, or leave the result
unconstrained. They therefore warrant `CONCERNS / LEGIT`, not
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
