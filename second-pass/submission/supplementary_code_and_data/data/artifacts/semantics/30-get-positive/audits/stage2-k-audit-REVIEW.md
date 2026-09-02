# Independent adversarial audit: 30-get-positive

The candidate contains a sound, non-vacuous K proof for arbitrary finite lists
of **integers**, and that proof executes the submitted function body. It does
not prove the full source contract, which asks about a list of “numbers” and
places no integer-only restriction on the input. The trusted canonical and the
generated Python function both accept ordinary numeric floats; the K entry
claim cannot represent them because it quantifies only over `IntSeq`. Under the
benchmark’s explicit decision rule, this material HumanEval-domain narrowing is
`FAIL / NOT_LEGIT`, even though the integer-only theorem itself is sound.

## 1. Input and provenance integrity

### Declared layout and mounts

`/audit-input.json` declares:

- problem `30-get-positive`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- `mount_reference_semantics: true`.

This agrees with the rendered audit condition. The trusted
`/reference/reference-semantics` tree is present. Therefore this is not the
infrastructure-contradiction case.

All launcher-required records for `legacy-selected-stage1` are real, readable
regular files, and the declared directory mounts are real directories:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`;
- the structured `/generation-evidence/codex-trace/`;
- the optional, present `/generation-evidence/usage.json`;
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`.

No required record, declared mount, candidate proof deliverable, or supplied
semantics entry is symlinked or mistyped. Historical runtime metrics are not
required for this legacy layout and were not reconstructed.

### Hashes and campaign lock

The campaign lock JSON is exactly equal to the `audit_campaign` block in
`/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Independent SHA-256 checks matched the recorded hashes for the run manifest,
task manifest, generation result, invocation, metrics, usage, generation
prompt, last message, output log, canonical, trusted prompt, trusted
translator, candidate prompt, and candidate translator. Every output listed
inside the invocation/result evidence map also matched, including the one
JSONL trace file.

The structured trace contains 300 valid JSON records with no parse failures:
52 function calls, 52 function-call outputs, one task start, and one task
completion. It was inventoried only as untrusted generation history; no
reported prior `#Top` was accepted as proof evidence.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` — exit 0, `STAGE1_INTEGRITY_OK`
- `evidence/generation_trace_inventory.py`
- `evidence/generation_trace_inventory.log` — exit 0,
  `GENERATION_TRACE_FULL_PARSE_OK`

### Prompt, translator, and supplied-semantics identity

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The candidate `reference-semantics/` and trusted
`/reference/reference-semantics/` trees have exactly the same relative
directories, regular files, sizes, and per-file SHA-256 values. There are no
missing, additional, changed, or linked entries. This establishes integrity of
the selected fixed semantics, but does not bless the proof-local additions in
`verification.k`.

Stage 1 result: **PASS**. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says:

> Return only positive numbers in the list.

It gives two integer examples, but the signature is merely `l: list`; it does
not say “integers” or otherwise exclude non-integral numbers. The trusted
canonical returns, in original order and with duplicates preserved, every
element satisfying Python’s `e > 0`:

```python
return [e for e in l if e > 0]
```

The generated implementation uses an empty result list, visits the input from
left to right, appends each `x` for which `x > 0`, and returns the result. It is
algorithmically equivalent to the canonical implementation over ordinary
numeric inputs.

### Trusted regeneration

The trusted translator independently regenerated `solution.mpy` from the
submitted `solution.py`. `cmp` exited 0. Both the submitted and regenerated
constructor files have SHA-256
`f89d5ec0a7acf90c31ffe400ceaba3d0cb4541b997eb34f372421069bc02948e`.

Evidence:

- `evidence/check_translation.sh`
- `evidence/check_translation.log` — translator exit 0, byte-identity exit 0

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical and
the scratch copy of the generated solution under distinct module names. It
checks output identity and verifies that neither implementation mutates its
input.

The retained run covered:

- both documented examples;
- empty input;
- singleton `-1`, `0`, and `1` branch boundaries;
- all-positive, all-nonpositive, alternating, duplicate, and order cases;
- arbitrary-size positive and negative Python integers;
- negative zero, the smallest positive subnormal float, finite mixed
  int/float lists, and infinities;
- a Boolean behavior observation (not relied on for the domain decision);
- every list of length 0 through 6 over `{-1, 0, 1}`;
- 1,000 deterministic generated lists of length 0 through 30.

There were 2,108 cases and zero mismatches. The retained corpus fingerprint is
`029e5553613ddd3e170ba4eb67c0083526391eb6da0cbe3e8d2578068df7b54c`.
In particular, ordinary float inputs work in both real Python
implementations: `[0.5]` returns `[0.5]`, and mixed negative/zero/positive
floats are filtered in the expected way.

Evidence:

- `evidence/differential_test.py`
- `evidence/differential_test.log` — exit 0, `MISMATCHES 0`

Stage 2 result: **program fidelity PASS**. The float observations become
important to theorem adequacy in Stage 4.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/30-get-positive` and used
the trusted supplied-semantics tree. I did not copy or use any candidate-built
definition or K cache. The observed tools are K 7.1.293.

### Concrete definition

Command:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

Result: exit 0. The warnings are fixed-semantics unused-variable and
non-exhaustive-total-function warnings; there is no build error.

The concrete assertion harness was independently regenerated and was
byte-identical to the submitted harness. CPython exited 0. `krun` exited 0 with
`.K`, `NoExc`, and exit code 0 after the two examples, empty input, and an
all-nonpositive boundary case.

Evidence:

- `evidence/kompile-llvm.log`
- `evidence/concrete-execution.log`

### Proof definition and positive claims

Command:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled
```

Result: exit 0 (`evidence/kompile-haskell.log`).

The loop label was then selected independently:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.filter-loop --smt-timeout 10000
```

Result: `#Top`, exit 0
(`evidence/kprove-filter-loop.log`).

The authoritative target command contains both claims, so the entry claim can
use the separately stated loop lemma:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --smt-timeout 10000
```

Result: `#Top`, exit 0
(`evidence/kprove-all-claims.log`).

As a diagnostic, selecting only `SPEC.get-positive-correct` removes the loop
lemma from the selected claim set and led to sustained concrete unrolling. I
interrupted that diagnostic; it is not the candidate’s required proof command
and is not treated as a candidate failure. The exact observation is retained
in `evidence/kprove-entry-only-termination-note.txt`.

Stage 3 result: **PASS**. Every positive target claim closes in a fresh
source-built definition.

## 4. Adequacy and real-program pinning

### Plain-language claims

`filter-loop` says:

- start at the real loop head with an arbitrary finite integer tail `INPUT`,
  current result-list contents `PREFIX`, ordinary bindings for `l`, `result`,
  and `x`, and any continuation `CONT`;
- execute the loop body;
- resume exactly `CONT`;
- preserve the framed state except that `x` may have its final loop value and
  the result object becomes `filterPositive(PREFIX, INPUT)`.

`get-positive-correct` says:

- start with the exact `get_positive` closure bound in module scope, an empty
  heap, fresh heap location 0, empty call stack, no pending return or exception,
  and a bare list value encoding any finite `IntSeq`;
- execute a real call to that closure;
- return `ref(0)`;
- leave heap location 0 containing exactly
  `filterPositive(.ValSeq, INPUT)`;
- restore scope location, stack, return state, exception state, and exit code.

The postcondition is result-constraining: it fixes both the returned reference
and the exact list stored at that reference. It is not a free result variable,
tautology, or one-way implication.

### Mechanical program pinning

The claim does not execute the top-level `Module`/`FuncDef` load. Instead, it
starts after that semantically inert setup with the closure explicitly bound.
This normalization is legitimate only if the binding and body are identical.

I parsed and macro-expanded:

1. the trusted-regenerated submitted `solution.mpy`; and
2. `Module(FuncDef("get_positive", Params("l"), getPositiveBody))`.

Both expanded to byte-identical KORE constructor terms with SHA-256
`712eca0709b632b0ab22edeeb6f9c686a2861de4c855f028dfc63bb811bf5298`.
Thus the closure in the entry claim contains the same function name,
parameter, statement order, guard, append call, and return as the submitted
program.

Evidence:

- `evidence/check_program_term.sh`
- `evidence/check_program_term.log` — both `kast` exits 0, `cmp` exit 0
- `evidence/submitted-program-expanded.kore`
- `evidence/claim-program-expanded.kore`

### Satisfying states and concrete substitution

`evidence/reviewer-k/spec-ground.k` gives fully ground states for both claim
preconditions:

- entry input `[-2, 0, 3, 5]`, which reaches `ref(0)` with heap list `[3, 5]`;
- loop prefix `[7]` and remaining input `[-2, 3]`, which reaches prefix
  `[7, 3]` and resumes `.K`.

Both ground claims printed `#Top` and exited 0
(`evidence/kprove-ground-witnesses.log`). The exact entry input also returns
`[3, 5]` in both trusted and generated Python functions
(`evidence/differential_test.log`). Hence neither formal precondition is
empty, and the claimed result agrees with both Python implementations on a
satisfying instance.

### Body sensitivity

I changed the actually executed guard from `x > 0` to `x > 1` in a separate
closure and corresponding loop claim. Macro expansion produced a different
program KORE hash
`8c7dab19b565d3af2d05ec24572bb1019ae778cb94a15d957736f534f053e87c`.
The mutation definition built successfully, but the proof failed with
`WarnStuckClaimState` and exit 1. Input `[1]` is a direct false witness: the
submitted body returns `[1]`, while the mutated body returns `[]`.

Evidence:

- `evidence/reviewer-k/verification-body-mutation.k`
- `evidence/reviewer-k/spec-body-mutation.k`
- `evidence/body-mutation-build.log` — exit 0
- `evidence/body-mutation-term-comparison.log` — expected constructor
  difference
- `evidence/body-mutation-proof.log` — expected proof exit 1 and residual

### Fatal domain inadequacy

The formal entry variable has sort `IntSeq`, whose only constructors are
`.IntSeq` and `iCons(Int, IntSeq)`. It cannot contain a K `Float` or any other
non-`Int` numeric value. Therefore the theorem cannot be instantiated even at
the simple source-contract input `[0.5]`.

That exclusion is material:

- the prompt says “numbers,” not “integers”;
- its `list` annotation supplies no element restriction;
- the trusted canonical and generated implementation both return `[0.5]` for
  `[0.5]`;
- positive, zero, and negative floats exercise the property-bearing branch,
  so this is not a typing-only or observationally inert omission;
- the supplied semantics has a `Float` value sort, so this is not an audit
  infrastructure failure.

The two integer examples do not narrow an otherwise unrestricted “numbers”
contract to integers. The K proof establishes an unrestricted finite-size
theorem only **inside the smaller integer element domain**.

Stage 4 result: **real-program pinning PASS; source-contract adequacy FAIL**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventoried every top-level source declaration
from the supplied assembled semantics, every helper K file, `verification.k`,
and `spec.k`. The retained TSV contains 943 entries:

- 703 rules;
- 232 syntax declarations;
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims.

It identifies 108 `total` declarations, 25 opaque-symbol declarations, 29
priority rules, no `functional` declarations, and no simplification rules.
It includes `semantics/concrete.k` even though that module is imported only by
`MPY-KRUN`, not by the Haskell proof.

Every inventory row has an explicit reachability and audit disposition in
`evidence/k-rule-assessment.tsv`. The source inventory and disposition summary
are:

- `evidence/k-rule-inventory.tsv`
- `evidence/k-rule-inventory-summary.log`
- `evidence/k-rule-assessment.tsv`
- `evidence/k-rule-assessment-summary.log`

The exact submitted-constructor mapping is in
`evidence/used-construct-map.md`.

### On-path fixed semantics

The proof path uses the fixed declarations/rules for:

- statement sequencing and integer/list values;
- lexical lookup and the pinned closure binding;
- left-to-right callee and argument evaluation;
- fresh result-list allocation;
- parameter and loop-target binding;
- integer literal and integer `>` evaluation;
- `if` branching;
- list iteration protocol;
- bound-method routing and in-place `append`;
- return, frame pop, and restoration of the caller state.

The relevant rules preserve evaluation order, heap location monotonicity,
scope allocation/deallocation, the active continuation, exception state, and
the exact returned reference. The append priority rule is more specific than
generic bound-method dispatch and writes only the referenced result-list heap
entry. The integer comparison rules are sort-disjoint from other comparison
cases. The input list is read but never mutated, so the supplied semantics’
bare read-only list representation loses no observable behavior for this
program.

The 25 fixed opaque symbols cover float operations, sorting, MD5, and similar
primitives. None occurs in the submitted integer-domain execution term or
postcondition. `MPY-CONCRETE` rules support only the LLVM tests and are absent
from the proof definition. Other supplied-semantics constructs are excluded by
constructor/control unification. These fixed, out-of-path limitations are not
used to close either claim.

### Proof-local inventory and decisions

There are five proof-local syntax declarations and eight proof-local rules:

1. `getPositiveBody` and its macro rule. **Sound.** Mechanical expansion is
   the exact submitted function body.
2. `positiveLoopBody` and its macro rule. **Sound.** Mechanical expansion is
   the exact submitted `if`/`append` body.
3. `intVals(IntSeq)`. **Sound as a theorem-input representation.** It has no
   result-bearing oracle value; it exposes only a structurally finite integer
   sequence.
4. Empty `intVals` iterator rule. **Sound operational bridge.** It returns
   `#iterDone`, changes no other cell, and preserves the entire continuation.
5. Cons `intVals` iterator rule. **Sound operational bridge.** It yields the
   exact integer head and a tail representation, changes no other cell, and
   preserves the entire continuation.
6. `filterPositive` empty rule. **Sound.** Filtering no remaining items leaves
   the accumulator.
7. `filterPositive` cons rule. **Sound.** It descends on the sequence tail and
   dispatches on exactly `I >Int 0`.
8. `filterPositiveBranch` true rule. **Sound.** It appends exactly `I` and
   continues on the tail.
9. `filterPositiveBranch` false rule. **Sound.** It leaves the accumulator and
   continues on the tail.

The apparent count of nine above treats the `intVals` syntax declaration
separately; the actual local inventory remains five declarations and eight
rules.

The `.IntSeq`/`iCons` iterator cases are disjoint and exhaustive. They do not
overlap the fixed `.ValSeq`/`vCons` list iterator cases. The true/false branch
rules are disjoint and exhaustive, and their total declaration is justified.
All recursive equations descend on a proper tail. There is no proof-local
opaque symbol, simplification rule, conflicting priority, unguarded oracle, or
rule that encodes the desired answer.

### Bridge-free connection

The candidate did not include a separate connection theorem for `intVals`, so
I constructed a reviewer-only transparent materializer:

```text
materializeInts(.IntSeq) = .ValSeq
materializeInts(iCons(I, IS)) = vCons(I, materializeInts(IS))
```

It imports the fixed semantics but not the candidate’s `intVals` iterator
rules. Two universal reachability claims then execute the fixed native-list
iterator over the complete bridge domains:

- empty maps to `#iterDone`;
- arbitrary `I, IS` maps to
  `#iterYield(I, list(materializeInts(IS)))`.

Both connection claims printed `#Top` and exited 0:

- `evidence/reviewer-k/verification-connection.k`
- `evidence/reviewer-k/spec-iterator-connection.k`
- `evidence/iterator-connection-proof.log`

The claims retain an arbitrary `<k>` suffix, so their justification domain
contains every continuation accepted by the bridge. Their state footprint is
identical: only the iterator redex changes, with every configuration cell
framed.

A stronger experimental whole-program spec directly over the opaque total
term `materializeInts(INPUT)` got stuck because the backend did not case-split
that function at the iterator redex
(`evidence/connection-proof.log`, exit 1). This does not contradict the two
successful complete pattern-domain connection claims; it records a backend
normalization limitation rather than supplying evidence for the theorem.

### Claims as extensions

The loop claim preserves arbitrary `CONT` rather than discarding or replacing
it. Its RHS permits only the expected final `x` binding and accumulator update;
all other framed scope/heap entries and omitted cells are preserved. Its
standalone `#Top` is the universal execution connection used by the entry
claim.

The entry claim executes `Call`, lookup, binding, allocation, the exact loop,
append effects, return, and frame pop. It does not replace the program with
`filterPositive`; that function appears only as the constrained value reached
after execution.

No proof-local rule was found unsound, so this review makes no unsupported
unsound-rule allegation requiring a false-rule witness. The failure is the
claim’s smaller domain, with `[0.5]` as the explicit excluded source-contract
witness.

Stage 5 result: **sound for the stated integer theorem; no answer smuggling**.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k` to trust. I created a fresh module
that retains the genuine loop lemma but changes the entry postcondition to
demand one extra trailing integer `1` in every returned list.

Satisfying false witness:

```text
INPUT = .IntSeq        Python input = []
actual heap list = []  mutated required list = [1]
```

The mutation parsed and built successfully:

```text
kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run
```

Result: exit 0 (`evidence/vacuity-build.log`).

The actual proof command:

```text
kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --smt-timeout 10000
```

Result: exit 1 with `WarnStuckClaimState`. The residual has reached
`ref(0)`, shows heap location 0 containing `.ValSeq`, and explicitly includes
`INPUT = .IntSeq`. Thus the failure is the expected unmet result obligation,
not parsing, a missing import, a timeout, or an unreachable mutation.

Evidence:

- `evidence/reviewer-k/spec-vacuity.k`
- `evidence/vacuity-build.log`
- `evidence/vacuity-proof.log`

Stage 6 result: **PASS**. The positive proof is non-vacuous and
result-discriminating.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditional on the supplied K semantics and K prover, for every finite
`IntSeq`:

1. the exact submitted `get_positive` closure can be called from the pinned
   initial state;
2. its real loop examines every encoded integer from left to right;
3. it appends exactly the integers strictly greater than zero;
4. it returns `ref(0)`, whose heap value is the stable-order mathematical
   filter of the input;
5. it restores the caller’s control, scope-allocation, stack, return,
   exception, and exit-code cells as claimed.

This is a legitimate partial-correctness theorem for arbitrary-size finite
integer lists. It is not a theorem about all numeric lists admitted by the
source contract.

### Trust ledger

| Boundary | Dependents | Evidence and disposition |
|---|---|---|
| K 7.1.293 frontend, Haskell backend, and reachability logic | Every `#Top` | Foundational accepted tool boundary; definitions were rebuilt from source. |
| Trusted supplied semantics | All execution steps | Candidate tree is entry-identical to the trusted mount. On-path rules were reviewed; no candidate semantics modification exists. |
| Trusted `py2mpy.py` translation | Source-to-constructor bridge | Trusted regeneration is byte-identical; candidate translator is byte-identical to trusted. |
| Macro-to-submitted-body identity | Real-program pinning | Machine-checked by expanded KORE constructor equality. |
| `intVals` symbolic input representation | Loop induction and entry domain | Transparent two-case representation; bridge-free fixed-list connection claims close over both complete match domains. |
| Built-in K integer/list/map operations | Comparison, append, filter equations | Ordinary mathematical/fixed-semantics primitives; no opaque result symbol reaches the postcondition. |
| Interpretation of `filterPositive` as stable positive filtering | Human-facing integer theorem | Direct exhaustive structural equations plus concrete witnesses; no oracle. |
| Differential testing | Python implementation fidelity and domain witness | Finite evidence only; 2,108 cases and zero mismatches. It is not used as a substitute for the K proof. |
| Partial-correctness scope | Final theorem wording | The proof does not claim behavior outside its precondition or replace termination/semantics assumptions with testing. |

The source-contract adequacy bridge fails: no theorem or named trusted
assumption extends `IntSeq` to non-integer numbers. The successful float
differential cases demonstrate that this omitted behavior is both real and
material, but finite tests do not repair the missing universal K claim.

### Gate and verdict mapping

- Kit Gate A, real-program soundness: **PASS** for the integer theorem.
- Kit Gate B, intent adequacy: **FAIL** because `IntSeq` materially narrows
  the unrestricted numeric element domain.
- Kit Gate C, trust/evidence auditability: **PASS** for the integer theorem;
  all reviewer evidence and boundaries are retained.

In generic Kit terminology this is a sound-but-limited theorem. The controlling
benchmark prompt explicitly maps a `SOUND-BUT-LIMITED` result caused by
materially narrowing the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
