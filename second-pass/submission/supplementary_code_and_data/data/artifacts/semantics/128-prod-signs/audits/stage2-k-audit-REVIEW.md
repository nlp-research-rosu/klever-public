# Independent adversarial review: 128-prod-signs

The candidate is not a legitimate proof of the requested program. Fresh builds
and both positive `kprove` runs succeed, the claim is non-vacuous, and the
executed closure is mechanically identical to the submitted program. However,
the nonempty proof closes through a candidate-added priority-40 operational
rule that replaces the whole loop. That rule is false over its declared match
domain: it bypasses the supplied semantics' cell-aware loop-target binding and
can leave a captured heap cell stale. Fresh K proofs demonstrate different
observable results for the same integer-list loop under bridge-enabled and
fixed semantics. It also has no bridge-free connection theorem and directly
assumes the property-bearing computation that the proof needed to establish.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `128-prod-signs`, condition `semantics`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- a mounted trusted reference-semantics tree;
- complete input provenance.

There is no mode/mount contradiction. `/reference/reference-semantics` is
present as required for supplied-semantics mode.

I independently checked all launcher-required mounts and records. For this
legacy-selected layout, `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured JSONL trace are present,
readable regular files. No required candidate, reference-semantics, or
generation-evidence entry is a symlink. Historical `runtime-metrics.json` is
not required for this layout.

The campaign lock:

- is byte-hashed as
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash recorded in `/audit-input.json`; and
- parses to exactly the same JSON object as the `audit_campaign` block.

The mounted run, task, result, invocation, metrics, usage, generation text, and
trace-file hashes match the corresponding launcher/result records. The
structured trace contains 284 valid JSON records and no decoding failures.
The full 15,308-line Codex output was scanned as untrusted history; it contains
three historical `#Top` lines and several failed construction iterations, none
of which was used as proof evidence. See
[stage1-json-records.txt](/audit-output/evidence/stage1-json-records.txt),
[stage1-inventory-hashes.txt](/audit-output/evidence/stage1-inventory-hashes.txt),
[stage1-generation-records.txt](/audit-output/evidence/stage1-generation-records.txt),
and
[stage1-generation-trace-summary.txt](/audit-output/evidence/stage1-generation-trace-summary.txt).

The trusted/candidate integrity comparisons independently establish:

- `prompt.py` is byte-identical to `/reference/prompt.py`;
- `py2mpy.py` is byte-identical to `/reference/py2mpy.py`; and
- recursive `diff --no-dereference -ru` of the candidate and trusted
  `reference-semantics/` trees exits 0. Their inventories have identical
  entry names and types, with no missing, additional, mistyped, or symlinked
  semantics entry.

Evidence:
[stage1-integrity-comparisons.txt](/audit-output/evidence/stage1-integrity-comparisons.txt).
There is no audit infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted source contract says: for an array of integers, return the sum of
their magnitudes multiplied by the product of their signs (`1`, `-1`, or `0`);
return `None` for an empty array. The intended domain is not length- or
value-bounded.

The trusted canonical implementation returns `None` for empty input, otherwise
uses sign zero if any element is zero, sign `(-1)^n` for the count of negative
elements, and multiplies that sign by the sum of absolute values. The candidate
implements the same function as a single pass with `total` and `sign`
accumulators.

Running the trusted translator on `/candidate/solution.py` produced SHA-256
`05d22e224493b5302767cdeea8ba5a61d7a40d95ff651837f97a77f21a7dd70c`,
byte-identical to the submitted `solution.mpy`. See
[stage2-regeneration.txt](/audit-output/evidence/stage2-regeneration.txt).

The independent differential script imports the trusted canonical and candidate
entry points separately. It checks:

- all three documented examples;
- explicit empty, zero, positive, negative, multiple-negative, mixed-zero, and
  very-large-integer boundaries;
- every list of lengths 0 through 6 over values `-3..3`; and
- 10,000 seeded random lists of lengths 0 through 40, including values up to
  magnitude `10^100`.

All 147,268 comparisons matched in value and result type. Script and result:
[differential_test.py](/audit-output/evidence/differential_test.py) and
[stage2-differential.txt](/audit-output/evidence/stage2-differential.txt).
This is strong implementation evidence, not a universal K proof.

## 3. Clean proof reconstruction

I copied only source artifacts into
`/tmp/audit-work/128-prod-signs-audit`, did not copy or reuse any candidate
compiled definition, and created fresh output definitions.

The supplied concrete semantics compiled from source with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Full bounded log:
[stage3-kompile-runtime.txt](/audit-output/evidence/stage3-kompile-runtime.txt).

The proof definition compiled from `verification.k` and the fresh semantics
copy with the Haskell backend:

```text
kompile verification.k --backend haskell \
  --main-module PROD-SIGNS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. Log:
[stage3-kompile-proof.txt](/audit-output/evidence/stage3-kompile-proof.txt).
Compiler warnings concern unused variables and known non-exhaustive functions;
they are not build failures.

Each positive claim was then selected independently:

- `PROD-SIGNS-SPEC.prod-signs-empty`: exit 0 and `#Top`;
- `PROD-SIGNS-SPEC.prod-signs-nonempty`: exit 0 and `#Top`.

Exact commands and outputs:
[stage3-kprove-empty.txt](/audit-output/evidence/stage3-kprove-empty.txt) and
[stage3-kprove-nonempty.txt](/audit-output/evidence/stage3-kprove-nonempty.txt).

For independent concrete reconstruction, the reviewer-authored driver contains
an AST-exact copy of the submitted function plus seven boundary/normal
assertions. The AST comparison reported `FUNCTION_AST_EXACT_MATCH True`, and
`krun` under the newly compiled supplied semantics terminated with `.K`,
`NoExc`, and exit code 0. See
[k_concrete_driver.py](/audit-output/evidence/k_concrete_driver.py) and
[stage3-concrete-k.txt](/audit-output/evidence/stage3-concrete-k.txt).

Thus fresh dynamic verification under the candidate theory succeeds. It does
not establish that the candidate-added theory is sound.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`prod-signs-empty` starts a call to the submitted closure on the empty K list in
a clean root/builtins state. It requires the call to return `noneV`, preserve
normal control state, and account for the heap allocation of the empty list
literal used by `arr == []`.

`prod-signs-nonempty` starts the same call on
`vCons(I:Int, VS:ValSeq)`, requiring `allInts(VS)`. It therefore covers every
finite nonempty constructor list of arbitrary mathematical integers. The result
must equal:

```text
magnitudeSum(input) *Int signProduct(input)
```

where the first fold sums absolute magnitudes and the second flips for each
negative, becomes zero on a zero, and otherwise remains unchanged. There is no
fixed size, bounded unrolling, or example-only restriction. Together with the
empty claim, the formal domain covers the material source-contract domain.

### Program identity

I parsed both the submitted `solution.mpy` and `prodSignsFunction` through the
fresh K definition with macro expansion. A reviewer script then compared their
constructor trees. It confirmed:

- the submitted module has exactly one `FuncDef`, named `prod_signs`;
- parameters are identical;
- the entire statement body is identical; and
- the closure definition location is the root location `0`.

All checks are true in
[stage4-program-term-comparison.txt](/audit-output/evidence/stage4-program-term-comparison.txt);
the script is
[compare_program_term.py](/audit-output/evidence/compare_program_term.py).
The claim therefore executes the actual submitted binding and body, with only
the demonstrated module-to-closure construction omitted.

### Satisfiability and ground substitution

The empty claim is witnessed by `[]`. The nonempty precondition is witnessed by
`[-2, 0, 3]` (and independently by `[-2, -3]`). Substitution gives:

- `[]`: formal `None`, canonical `None`, candidate `None`;
- `[-2, 0, 3]`: magnitude `5`, sign `0`, formal result `0`, both Python
  results `0`;
- `[-2, -3]`: magnitude `5`, sign `1`, formal result `5`, both Python
  results `5`.

See
[witness_values.py](/audit-output/evidence/witness_values.py) and
[stage4-ground-witnesses.txt](/audit-output/evidence/stage4-ground-witnesses.txt).
The postcondition has no free result variable and is not a tautology.

Adequacy and source pinning therefore pass. The defect is how the nonempty
execution is discharged.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-level inventory contains 951 records:

- 928 configuration/syntax/context/rule records in the byte-identical supplied
  semantics;
- 5 syntax declarations and 16 rules in `verification.k`; and
- 2 target claims in `spec.k`.

Each record includes its file, line range, attributes, complete flattened
declaration, and a review classification. This includes all `function`,
`total`, macro, `owise`, strictness/context, priority, concrete, and
no-evaluator declarations in scope:
[stage5-rule-inventory.txt](/audit-output/evidence/stage5-rule-inventory.txt).
The inventory generator is
[inventory_k.py](/audit-output/evidence/inventory_k.py). Relevant sources were
also preserved verbatim with line numbers in
[stage5-material-semantics-sources.txt](/audit-output/evidence/stage5-material-semantics-sources.txt).

In supplied-semantics mode, the matching reference tree is the selected fixed
semantics rather than a candidate-authored language definition. Records in
unused modules (floats, sorting, dictionaries, sets, comprehensions, methods,
subscripts, ranges, builtins not invoked here, and concrete-only helpers) have
no target-proof redex or result/control/state dependency. Their opaque float,
sort, digest, and other stated trust boundaries therefore do not influence
these claims.

The material fixed-semantics path is:

| Program construct | Fixed declarations/rules |
|---|---|
| `Call`, argument order, closure frame | `core.k`, `call.k`, `functions.k` |
| names, literals, docstring discard | `core.k`, `str.k`, `controls.k` |
| empty-list literal/allocation and list equality | `list.k`, `operators.k`, `core.k` |
| `If` and truthiness | `controls.k`, `core.k` |
| integer comparisons/arithmetic | `operators.k`, `int.k` |
| assignment and return | `controls.k`, `functions.k` |
| ordinary list iteration/target binding | `controls.k`, `list.k`, `tuple.k` |

Evaluation order is left-to-right through strictness and `#evalArgs`; closure
calls allocate a frame, bind `arr`, execute the exact body, and pop normally.
The fixed loop protocol uses `#iterNext`, `#bindTgt`, the body, and a loop
continuation. No fixed-semantics target-slice rule was found to fabricate the
result.

### Candidate-local definitional rules

The candidate helpers are mostly truthful on their matched domain:

- `allInts` correctly recognizes constructor sequences of integers;
- `magnitudeAcc` has disjoint `< 0` and `>= 0` cases and strictly descends the
  tail;
- `signAcc` has disjoint negative/zero/positive cases and strictly descends;
- `magnitudeSum` and `signProduct` select initial accumulators 0 and 1;
- `lastInt` strictly descends a nonempty integer sequence; and
- the macro closure is the exact program term already mechanically checked.

There is a narrower totality defect: `allInts`, `magnitudeAcc`, `signAcc`,
`magnitudeSum`, `signProduct`, and `lastInt` are declared `total` more broadly
than their equations cover. In particular, opaque/non-constructor `ValSeq`
terms are uncovered, non-integer heads are uncovered by the numeric folds, and
`lastInt(.ValSeq)` is uncovered. The target's concrete integer-list instances
remain inside the covered equations, so these declarations do not supply the
main false witness, but they are not valid global totality claims.

### Decisive operational bridge defect

The rule at
[verification.k](/candidate/verification.k:74) is an operational bridge, not a
proved invariant claim. With priority 40, it preempts the fixed `For` rule for
the exact loop and replaces the entire finite iteration by three direct map
updates:

- `total := magnitudeAcc(...)`;
- `sign := signAcc(...)`;
- `value := lastInt(...)`.

Its complete match domain admits:

- any continuation after the loop (`...` in `<k>`);
- any parent and any surrounding cells;
- any current map containing integer-valued `total` and `sign`; and
- an integer list satisfying its guard.

It neither checks that the frame is a plain frame nor preserves the supplied
semantics' cell-aware `#bindTgt` behavior. It also has no bridge-free universal
connection claim. The nonempty target uses the same summary functions on its
right-hand side, so this bridge axiomatizes the property-bearing loop
computation.

The false-conclusion witness is concrete:

- loop input: `[1]`, within the intended integer-list domain;
- `total = 0`, `sign = 1`;
- `value = cellRef(0)` and `$cells = cellsMark("value")`;
- heap cell 0 initially contains `99`;
- immediately following observable continuation: `cellRef(0)`.

Under only the supplied semantics, `#bindTgt` writes `1` through cell 0, the
map continues to bind `value` to `cellRef(0)`, and the continuation observes
`1`. The fixed-semantics witness independently compiles and proves `#Top`:
[fixed-cell-witness.k](/audit-output/evidence/fixed-cell-witness.k) and
[stage5-fixed-cell-witness.txt](/audit-output/evidence/stage5-fixed-cell-witness.txt).

With the candidate bridge, the direct map update replaces the `value` binding
with integer `1`, leaves heap cell 0 stale at `99`, and the same continuation
observes `99`. The bridge-enabled false claim also proves `#Top`:
[bridge-cell-witness.k](/audit-output/evidence/bridge-cell-witness.k) and
[stage5-bridge-cell-witness.txt](/audit-output/evidence/stage5-bridge-cell-witness.txt).

This is a state-and-result divergence over a satisfiable match, not an
inference from finite differential testing. The rule is globally false even
though the submitted unannotated function happens to create a plain frame.
Unreachability from this one entry cannot validate a globally false proof rule,
and the rule's broad context has no connection theorem. Gate A
real-program/proof-extension soundness fails.

## 6. Fresh non-vacuity test

I created a fresh spec that changes the nonempty destination to:

```text
(magnitudeSum(input) *Int signProduct(input)) +Int 1
```

The mutation is false for the satisfying witness `[1]`: the actual/formal
result is `1`, while the mutant requires `2`.

`kprove --dry-run` exits 0, proving that the mutated module parses and builds:
[stage6-vacuity-dry-run.txt](/audit-output/evidence/stage6-vacuity-dry-run.txt).
The actual proof exits 1 with `WarnStuckClaimState`. Its residual says the
configuration reaches the unmutated summary and the implication would require
`summary +Int 1 == summary`:
[stage6-vacuity-failure.txt](/audit-output/evidence/stage6-vacuity-failure.txt).
The mutation itself is
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k).

Non-vacuity passes: the postcondition genuinely constrains the result. This
does not repair the unsound theory used to reach that result.

## 7. Proven versus assumed accounting

What the reconstructed `#Top` establishes is conditional:

> In the theory consisting of the supplied MPY semantics plus every rule in
> `verification.k`, the empty call reaches `noneV`, and a nonempty integer-list
> call reaches `magnitudeSum(input) * signProduct(input)`.

It does not establish that the candidate loop bridge is a consequence of the
supplied semantics.

| Boundary or assumption | Effect and assessment |
|---|---|
| K 7.1.293 parser/compiler/Haskell prover and matching-logic implementation | Ordinary machine-checking trust boundary; acceptable. |
| Byte-identical supplied MPY semantics | Defines the benchmark execution model. Material target slice reviewed; acceptable as the selected fixed semantics. |
| Mathematical unbounded K integers | Matches Python's unbounded integer behavior for the used operations; acceptable. |
| Trusted translator | Byte regeneration and constructor comparison connect source to MPY/closure; acceptable for this artifact. |
| Manual `prodSignsFunction` macro | Program-derived but mechanically identical in parameters/body/location; acceptable pinning bridge. |
| Candidate fold equations | Truthful for constructor integer sequences; partial/opaque outside that use despite over-broad `total` attributes. |
| Priority-40 loop-summary rule | Program-derived operational bridge; affects control, local state, heap-cell semantics, and the final result. It has no connection theorem and has a machine-checked false state/result witness. Illegitimate. |
| Opaque float/sort/digest and other unused supplied primitives | Imported but never reached by this program or either target claim; no dependency. |
| Canonical differential tests | Finite evidence for Python implementation equivalence only; not a proof of the K bridge. |
| Partial-correctness interpretation | Claims constrain terminating executions; they do not prove a general Python termination theorem. The modeled finite loop terminates, but this does not excuse the bridge. |

Gate summary:

- Fresh positive verification: **PASS** under the candidate theory.
- Gate A, real-program/proof-extension soundness: **FAIL** because of the
  false and unconnected operational bridge.
- Gate B, intent/domain adequacy: **PASS**; the claims cover unrestricted
  finite integer lists and state the intended result.
- Non-vacuity: **PASS**.
- Trust/evidence validation: **FAIL** for the indispensable bridge; concrete
  Python testing cannot replace its missing universal connection proof.

Because a materially unsound proof rule replaces the key loop computation and
can prove a false observable conclusion, successful reconstruction and
non-vacuity are insufficient. The benchmark decision is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
