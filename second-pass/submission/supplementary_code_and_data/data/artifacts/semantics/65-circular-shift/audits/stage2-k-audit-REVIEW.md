# Independent adversarial audit: 65-circular-shift

The candidate has a reproducible, non-vacuous K reachability proof of its
submitted program on **nonnegative** shifts. It does not prove the HumanEval
source contract over its full documented integer domain. Both K entry claims
add `SHIFT >=Int 0`, although the prompt states no such precondition, and the
submitted implementation is observably different from the trusted canonical
for negative shifts. For example:

```text
circular_shift(12, -1)
trusted canonical: "12"
submission:        "21"
```

That is a material program-fidelity and theorem-domain failure. Under the
benchmark's explicit mapping for a materially narrowed HumanEval contract, the
candidate is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

### Declared layout and semantics boundary

- `/audit-input.json` declares `record_layout` =
  `legacy-selected-stage1`, problem `65-circular-shift`, condition
  `semantics`, and `semantics_mode` = `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` is present, as required for that mode.
  There is no mode/mount contradiction and therefore no infrastructure breach.
- `/audit-campaign-lock.json` is JSON-identical to the `audit_campaign` block
  in `/audit-input.json`. Its independently computed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.

The independently checked launcher and evidence hashes all match:

- `/run.json`:
  `321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0`
- `/task.json`:
  `9768e3687286f8dd0d1de34a19a615794145b00a6ff1b29116f31828721dd3ff`
- `/generation-result.json`:
  `1e1a4c60b227be6af1661763db25701c71835c992e3d1b30ed4e074f540fc10b`
- generation invocation, metrics, usage, prompt, last message, output log,
  legacy records, and the sole structured-trace JSONL file all match their
  launcher/stage-result leaf hashes.
- The structured trace contains 367 valid JSON events. The generation output
  log contains 37,706 lines. These records were inspected only as untrusted
  claims; their reported `KPROVE_PASSED` marker was not used as proof evidence.

For the declared legacy layout, every required record is present, readable,
regular, and non-symlinked. `usage.json` is present and was inspected.
Historical runtime metrics not recorded by this legacy layout are not required.

### Candidate input integrity

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- A recursive path/type/mode/size/byte comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` found no missing, additional, changed,
  mistyped, or symlinked entries.
- No symlinks or special filesystem entries occur below `/candidate`,
  `/reference`, or `/generation-evidence`.

Evidence:

- `evidence/01_integrity_check.py`
- `evidence/01_integrity.sh`
- `evidence/01_integrity.log` — exit 0
- `evidence/01_generation_summary.py`
- `evidence/01_generation_summary.log` — exit 0

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` says to convert the integer `x` to its decimal string,
shift that string's characters right by `shift`, return a string, and return the
reversal when `shift` is greater than the string length. It gives the examples
`(12, 1) -> "21"` and `(12, 2) -> "12"`. It states no
`shift >= 0` precondition.

The trusted canonical makes the behavior precise:

```python
s = str(x)
if shift > len(s):
    return s[::-1]
return s[len(s) - shift:] + s[:len(s) - shift]
```

Thus the trusted function has defined behavior for negative integer shifts as
well as nonnegative shifts.

### Submitted program

The submission uses:

```python
return s[-shift:] + s[:-shift]
```

This is equivalent to the canonical slice formula when
`0 <= shift <= len(s)`, including `shift == 0` and `shift == len(s)`.
It is not equivalent for negative shifts. For `x=12, shift=-1`, the canonical
split index is `3` and returns `"12"`; the submitted split index is `1` and
returns `"21"`.

The trusted translator regenerated `solution.mpy` with SHA-256
`ea135d25f2f2f0824e0fe9055892c5a7024291d5df41e5b27007257cae091901`.
It is byte-identical to the submitted `solution.mpy`.

The independent differential test covered:

- both documented examples;
- `x=0`, one-digit values, negative `x`, and a large 81-digit value;
- `shift=0`, `shift=len`, `shift=len+1`, and negative boundaries;
- a complete grid of 47 selected `x` values by shifts `-12..20`;
- 1,000 deterministic generated signed integers of 1–120 digits with shifts
  in `[-150, 180]`.

There were 2,589 comparisons. There were zero mismatches on nonnegative shifts
and 245 mismatches on negative shifts. The bounded log records the first 40
mismatches and the deterministic case-list hash.

Evidence:

- `evidence/02_differential.py`
- `evidence/02_fidelity.sh`
- `evidence/02_fidelity.log`

The differential command exits 1 specifically because it found semantic
mismatches. Translation and byte-identity checks both exit 0.

**Stage 2 finding:** fatal candidate defect. The generated implementation is
not equivalent to the trusted canonical over the unrestricted integer-shift
domain stated by the source artifact.

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to
`/tmp/audit-work/reconstruction`. The candidate's compiled definitions and
caches were neither copied nor used. The concrete semantics came from the
trusted `/reference/reference-semantics` copy.

The independently installed toolchain reports K v7.1.293. Fresh commands and
results were:

```text
kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled --warnings none
exit 0

krun solution.mpy --definition audit-runtime-kompiled --output pretty
exit 0; final <k> is .K and scope 0 contains the submitted closure

kompile verification.k \
  --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled --warnings none
exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims CIRCULAR-SHIFT-SPEC.normal-shift \
  --depth 300 --warnings none
#Top; exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims CIRCULAR-SHIFT-SPEC.oversize-shift \
  --depth 300 --warnings none
#Top; exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC --depth 300 --warnings none
#Top; exit 0
```

Evidence:

- `evidence/03_reconstruction.sh`
- `evidence/03_reconstruction.log`
- `evidence/03a_kompile_concrete.log` through
  `evidence/03f_kprove_combined.log`

**Stage 3 finding:** pass. Every submitted positive claim closes in a clean
definition. This fact alone does not repair the domain mismatch.

## 4. Adequacy and real-program pinning

### Claims in plain language

Both claims start from the exact nine-cell state expected immediately after
loading the function: environment 0, scope 0 containing only
`circular_shift`, the supplied builtins scope at -1, empty heap and stack,
fresh counters, no pending return or exception, and exit code 0.

The `normal-shift` claim says:

- `X`, `SHIFT`, and `LEN` are integers;
- `LEN` is the length of the code sequence for `str(X)`;
- `0 <= SHIFT <= LEN`;
- calling the submitted `circular_shift(X, SHIFT)` returns
  `circularShiftSpec(X, SHIFT, LEN)`.

The `oversize-shift` claim has the same state and length relation, but requires
`SHIFT >= 0` and `SHIFT > LEN`. Its result is the reversal branch of
`circularShiftSpec`.

The destination is result-constraining. It is not a free variable, existential
result, tautology, or one-way implication. The call consumes its frame and
returns the specific `Val` constructed by `circularShiftSpec`; all observable
cells return to the entry values.

### Mechanical program pinning

The constructor term embedded in the audit's module-load claim was compared
mechanically with the trusted regeneration of `solution.mpy`. After expanding
the external parser's omitted empty `Stmts` list to the inner parser's explicit
`.Stmts`, the constructor strings are identical (403 normalized characters).

A separate K reachability claim then executes that exact
`Module(FuncDef(...))` term from the initial configuration and proves that it
loads `circularShiftClosure` into scope 0. That claim prints `#Top` and exits 0.
This mechanically connects module loading, binding, parameters, body, and
defining environment to the closure used by both entry claims.

### Satisfying states and ground results

The following entry states satisfy the formal preconditions:

| Branch | `X` | `SHIFT` | `LEN` | canonical | submission |
|---|---:|---:|---:|---|---|
| normal | 12 | 1 | 2 | `"21"` | `"21"` |
| exact boundary | 12 | 2 | 2 | `"12"` | `"12"` |
| oversize | 12 | 3 | 2 | `"21"` | `"21"` |
| negative-`X` normal | -123 | 1 | 4 | `"3-12"` | `"3-12"` |
| negative-`X` boundary | -123 | 4 | 4 | `"-123"` | `"-123"` |
| negative-`X` oversize | -123 | 5 | 4 | `"321-"` | `"321-"` |

The independently translated K assertion program for those states terminates
with `.K` and exit code 0. Three direct ground
`circularShiftSpec` claims for `(12,1,2)`, `(12,2,2)`, and `(12,3,2)` also
close with `#Top` against the concrete code sequences for `"21"`, `"12"`,
and `"21"`.

A body-sensitivity mutation swaps the two concatenation operands in the actual
closure bound by the entry claim. The proof exits 1 with
`WarnStuckClaimState`; its residual is exactly the unequal
prefix-plus-suffix versus suffix-plus-prefix obligation. The witness
`X=12, SHIFT=1, LEN=2` makes the difference concrete (`"12"` versus `"21"`).

Evidence:

- `evidence/04_constructor_compare.py`
- `evidence/04_satisfying_states.py`
- `evidence/04_adequacy.sh`
- `evidence/04_adequacy.log`
- `evidence/04b_pinning_proof.log` — `#Top`, exit 0
- `evidence/04e_ground_postcondition.log` — `#Top`, exit 0
- `evidence/04f_body_sensitivity.log` — expected stuck claim, exit 1

**Stage 4 finding:** the claims pin and constrain the real submitted program,
but only over their explicitly narrowed nonnegative-shift domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.log` records the SHA-256 of, and every
`requires`, module/import, configuration, syntax declaration, context, rule,
claim, and special attribute occurrence in:

- the supplied assembled `semantics.k`;
- all 23 supplied helper K files;
- candidate `verification.k`;
- candidate `spec.k`.

The first-line inventory contains 699 rules, 230 syntax declarations, five
contexts, and two claims. It includes all `[function]`, `[total]`,
`[concrete]`, `[owise]`, priority, macro, strictness, and simplification
occurrences. The full source paths and line numbers are retained rather than
relying on the candidate's prose.

### Used-construct mapping

Every constructor in `solution.mpy` has a fixed-semantics path:

| Program construct | Declaration and material behavior |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` `#loadAll` and left-to-right statement sequencing |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` binds an exact `closureVal` in the current scope |
| `Call`, `Name` | `call.k` evaluates callee then arguments; `core.k` performs lexical/builtin lookup |
| closure invocation | `call.k` allocates the callee scope, pushes the complete continuation and caller state; `functions.k` binds parameters and pops on return |
| `Assign` | strict RHS in `syntax.k`; `controls.k` updates the current scope |
| `str(x)` | builtin binding in `core.k`; call routing in `call.k`; `builtins.k` maps integer input to `str(strToCodes(Int2String(x)))` |
| `len(s)` | `builtins.k` maps string length to structural `isLen` |
| `Compare(..., ">")` | ordered contexts in `operators.k`; integer comparison in `int.k` |
| `If` | strict condition in `syntax.k`; `controls.k` branches on `truthy` |
| unary `-` | strict operand in `syntax.k`; dispatch in `operators.k`; integer negation in `int.k` |
| `Subscript`/`Slice` | ordered object/bound contexts and slice-index normalization in `subscript.k` |
| string `+` | left-to-right `BinOp`; `str.k` structural `seqConcat` |
| `Return` | strict expression; `functions.k` discards the function-body suffix, records the value, restores the complete continuation and cells, and deallocates only the callee scope |

The program does not allocate lists, mutate the heap, perform I/O, throw an
exception on the stated integer inputs, or use loops. The relevant priority
rules select heap dereference and closure/call paths only where their guards
match; none preempts this program with a proof-specific answer.

The supplied float, sort, dict, comprehension, collection, iterator, and method
families are fully inventoried but unreachable from this exact closure and
entry state. Their opaque primitives do not contribute to either proof.
The supplied semantics is deliberately partial outside its modeled subset, but
every material operation used here has an execution rule and is exercised by
the fresh concrete runs.

### Candidate-local extensions

1. `syntax IntSeq ::= intCodes(Int)`

   This is a fresh opaque constructor with no evaluator and no independent
   equations. It can influence the branch through `isLen`, and the returned
   string through `buildIS` and `seqConcat`.

2. `strToCodes(Int2String(X)) => intCodes(X) [simplification]`

   This is a pure, result-bearing symbolic abstraction of the fixed integer
   string conversion. Its exact match domain is every integer `X`; it touches
   no state cell, continuation, binding, exception, or control stack. It is not
   an answer rule: it does not choose a branch or manufacture the final shifted
   sequence. The subsequent proof remains parametric in the entire code
   sequence.

   However, it is the only universal connection between the fixed conversion
   and `intCodes`, and the same symbol occurs in the program execution and the
   postcondition. A fresh bridge-free definition that merely declares the
   opaque constructor was tested:

   - the fixed ground conversion for `12` proves equal to
     `iCons(49,iCons(50,.IntSeq))`;
   - the bridge-free universal connection to the opaque constructor is stuck;
   - the bridge-free ground connection to the opaque constructor is stuck;
   - importing the candidate simplification makes the universal connection
     trivially close.

   Therefore no independent, bridge-free machine theorem justifies this
   abstraction. This is a validation/trust-boundary gap, not a demonstrated
   mathematically false rule: `intCodes(X)` can consistently be interpreted as
   the exact decimal code sequence, and no concrete false-conclusion witness
   was found. Accordingly, this review does **not** label the rule unsound.
   It does label the claimed connection conditional on that intended
   interpretation rather than independently proved.

3. `circularShiftClosure`

   This is a syntax macro, not an execution shortcut. Its expansion is the
   exact loaded closure, as established in Stage 4.

4. `circularShiftSpec`

   It is a `[function]` with two rules. Guards `SHIFT > LEN` and
   `SHIFT <= LEN` are disjoint and exhaustive over integers; their right-hand
   sides agree with the submitted reversal and suffix-plus-prefix branches.
   There is no overlap, missing guard case, task-answer oracle, state mutation,
   or abrupt-control bridge.

   The function is not the full source contract for negative shifts. On
   `X=12, SHIFT=-1, LEN=2`, its suffix-plus-prefix rule denotes `"21"`, while
   the canonical contract denotes `"12"`. Because the entry claims exclude
   that input, this is an adequacy/domain failure rather than a false equation
   on the rule's stated definition.

Evidence:

- `evidence/05_inventory.sh`
- `evidence/05_rule_inventory.log` — exit 0
- `evidence/05_bridge_probe.sh`
- `evidence/05_bridge_probe.log` — all expected outcomes observed
- `evidence/05b_ground_actual.log`
- `evidence/05c_universal_without_bridge.log`
- `evidence/05d_ground_opaque_without_bridge.log`
- `evidence/05e_candidate_bridge_enabled.log`

**Stage 5 finding:** no witnessed rule makes a false result provable on the
formal nonnegative domain, and no task answer is smuggled into a shortcut.
There is nevertheless no bridge-free universal theorem for the proof-local
symbolic code projection. Independently, the formal rules and claims encode
only the submitted program's nonnegative behavior, not the full canonical
contract.

## 6. Fresh non-vacuity test

The audit created a new `AUDIT-SPEC-VACUITY` module. Its entry state uses the
actual submitted closure and the satisfiable input `X=12, SHIFT=1`. It mutates
only the result obligation, demanding the demonstrably false `"12"` instead
of the real `"21"`.

```text
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run --warnings none
exit 0

kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --warnings none
exit 1
```

The dry run proves the mutation parses and builds. The proof fails for the
expected semantic reason with `WarnStuckClaimState`. The residual `<k>` cell
contains `str(iCons(50,iCons(49,.IntSeq)))`, the actual `"21"`, which does not
unify with the mutated destination `str(iCons(49,iCons(50,.IntSeq)))`,
the demanded `"12"`. This is not a parser failure, timeout, missing import,
or unrelated crash.

Evidence:

- `evidence/06_spec_vacuity.k`
- `evidence/06_nonvacuity.sh`
- `evidence/06_nonvacuity.log` — expected outcomes, wrapper exit 0
- `evidence/06a_mutation_dry_run.log` — exit 0
- `evidence/06b_mutation_proof.log` — expected stuck claim, exit 1

**Stage 6 finding:** pass. The reconstructed proof is result-sensitive and
non-vacuous.

## 7. Proven versus assumed accounting and decision

### What the successful K proof establishes

Conditional on the supplied semantics and the candidate's symbolic code
projection, the two reachability claims establish:

> For every integer `X` and every **nonnegative** integer `SHIFT`, execution of
> the exact submitted `circular_shift` closure terminates its call frame with
> the reversal of `str(X)` when `SHIFT` exceeds its length, and otherwise with
> the suffix of length `SHIFT` followed by the remaining prefix.

This is a genuine partial-correctness statement about the submitted body on
that narrowed domain. It is not merely a differential test, trace assertion,
or copied `#Top`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler/prover and Haskell/LLVM backends | all dynamic proof evidence | ordinary toolchain trust; versions and fresh commands recorded |
| supplied `MPY` semantics and K builtins for integers, strings, maps, lists, `Int2String`, and SMT arithmetic | all execution and proof steps | required supplied-semantics trust boundary; exact tree integrity checked; every material rule reviewed and concretely exercised |
| partial-correctness termination premise | reachability interpretation | acceptable; the exact loop-free body terminates on the claimed integer inputs in concrete execution |
| `intCodes` symbolic projection | symbolic length, branch condition, slices, and both final results | concerning proof-local abstraction; consistent and empirically grounded, but its bridge-free universal connection does not prove |
| constructor normalization of omitted empty `Stmts` | source-to-closure comparison | inert parser normalization; exact module-load reachability claim independently closes |
| Python differential evidence | source-contract and implementation bridge | finite evidence only; it supports equivalence on tested nonnegative cases and directly refutes equivalence on negative witnesses; it is not substituted for K proof |

No candidate prose, generation trace, compiled candidate definition, or
candidate cache is treated as trusted.

### Gate accounting

- Clean K verification: **PASS**. Both positive claims independently and
  jointly close with `#Top`.
- Real-body pinning and non-vacuity: **PASS**.
- Proof-extension independence: **limitation**. The symbolic string-code bridge
  has no independent connection theorem, though no false-conclusion witness
  justifies calling it unsound.
- Intent/domain adequacy: **FAIL**. `SHIFT >= 0` materially narrows a source
  contract that states no such restriction, and the submitted program is
  concretely wrong against the trusted canonical outside that restriction.
- Reproducibility/evidence: **PASS**. Reviewer-authored scripts, exact commands,
  bounded logs, exit statuses, hashes, ground witnesses, body mutation, and
  false-result mutation are preserved under `/audit-output/evidence`.

Even if the proof-local symbolic projection were accepted as a named trust
boundary, the negative-shift counterexample and explicit K precondition
independently force the benchmark's `FAIL / NOT_LEGIT` outcome. A sound theorem
over a materially narrowed HumanEval domain is not a legitimate proof of the
requested contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
