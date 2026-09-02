# Independent adversarial audit: 104-unique-digits

The candidate reconstructs to `#Top`, and its Python implementation is faithful
to the HumanEval reference. The proof is nevertheless not legitimate. Its two
priority rules replace the program-defined digit helper and the source `for`
loop without a bridge-free connection theorem. The loop summary does not even
pin the helper binding. A reviewer-authored body mutation and ground witness
show that these rules can prove a false result for the intended positive input
`[1]`.

All candidate files, generation records, prose, and prior outputs were treated
only as untrusted evidence. Builds and experiments were performed from source
under `/tmp/audit-work/workspace`; reviewer evidence is under
`/audit-output/evidence`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, as required for that mode.

The required records are present, readable, regular files (not symlinks):

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the JSONL trace at
  `/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T04-04-01-019f8e37-af4b-79f1-8bcf-7cf47a8789cf.jsonl`.

The optional legacy auxiliary records were also inspected. The complete
presence, type, symlink, file-hash, tree-hash, and recursive-diff transcript is
in [stage1-integrity.log](evidence/stage1-integrity.log), and auxiliary record
contents and hashes are in
[stage1-legacy-aux-records.log](evidence/stage1-legacy-aux-records.log).

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`; the lock's independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. See
[stage1-campaign-match.log](evidence/stage1-campaign-match.log).

Important independent checks:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`bebe5af4...e0507c`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485ea...db16`).
- A no-dereference recursive comparison found no missing, additional, changed,
  mistyped, special, or symlinked entry between the candidate and trusted
  reference-semantics trees.
- The independently reconstructed pipeline tree digest of the mounted
  candidate is `e3460123...cbe4`, matching both the retained workspace digest
  in `invocation.json` and `generation-result.json`.
- The independently reconstructed pipeline tree digest of each semantics tree
  is `4e06397a...789f`, matching the manifest-form semantics digest in
  `/audit-input.json`.

`/audit-input.json` also contains alternate legacy/auditor digest fields (for
example `candidate_tree_sha256 = 619ea8...` and alternate semantics digests).
Those are a distinct, undocumented digest scheme: the same record explicitly
retains the pipeline and legacy variants. I did not use those alternate fields
as the sole integrity check; exact file comparison and the retained pipeline
workspace digest establish the mounted artifact's identity.

All 518 trace lines parsed as JSON, totaling 777,416 bytes. The generation log
contains 44,587 lines / 1,388,929 bytes. The bounded inventories in
[stage1-trace-inventory.log](evidence/stage1-trace-inventory.log) and
[stage1-generation-log-inventory.log](evidence/stage1-generation-log-inventory.log)
cover the structured events, commands, failures, mutations, final proof run,
and the candidate's explicit decision to introduce the opaque digit predicate.
The generation evidence remains a claim, not proof evidence.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for an arbitrary finite list of positive integers,
retain exactly those elements whose decimal digits are all odd, preserve
duplicates, and return the retained elements in increasing order. The prompt
states no length or integer bound.

The canonical implementation converts every number to decimal characters and
checks that every digit is odd. The submitted implementation repeatedly checks
parity and divides by ten. For a positive integer, parity is the parity of its
last decimal digit, so this is a different but faithful algorithm.

Trusted regeneration with

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

produced byte-identical output to the submitted `solution.mpy`; both have
SHA-256 `261f5d54...a23e`. See
[stage2-translation.log](evidence/stage2-translation.log).

The independent differential oracle imports `/reference/canonical.py`
directly and compares it with the scratch copy of submitted `solution.py`. It
tested:

- both documented examples;
- empty, singleton, duplicate, sorted/reverse, zero-digit, trailing-even, and
  internal-even branch cases;
- one very large positive integer;
- every singleton from 1 through 9,999; and
- 2,000 deterministic generated lists of length 0 through 30 with values up to
  `10**30`.

All 12,011 comparisons agreed, with zero mismatches. The exact scope and seed
are in [differential_test.py](evidence/differential_test.py), and the complete
result is in [stage2-differential.log](evidence/stage2-differential.log).
This is strong finite implementation evidence, not a proof of the K
abstractions.

## 3. Clean proof reconstruction

Only source artifacts were copied to scratch. Candidate definitions,
`__pycache__`, and caches were not reused. The independently observed toolchain
was K 7.1.293 for `kompile`, `krun`, and `kprove`; see
[stage3-toolchain.log](evidence/stage3-toolchain.log).

Fresh concrete reconstruction:

```text
kompile .../reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .../runtime-audit-kompiled
```

exited 0. A reviewer-authored translated program exercised empty input,
single-digit odd/even values, both examples, an internal-even case, duplicates,
and sorting. `krun` ended in `.K`, `NoExc`, and exit code 0. See
[stage3-llvm-build.log](evidence/stage3-llvm-build.log),
[stage3-concrete-translate.log](evidence/stage3-concrete-translate.log), and
[stage3-concrete-run.log](evidence/stage3-concrete-run.log).

Fresh proof reconstruction:

```text
kompile .../verification.k --backend haskell \
  --main-module UNIQUE-DIGITS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .../verification-audit-kompiled
```

exited 0. `spec.k` contains exactly one positive claim. The independent command

```text
kprove .../spec.k \
  --definition .../verification-audit-kompiled \
  --spec-module UNIQUE-DIGITS-CORRECT
```

printed `#Top` and exited 0. See
[stage3-proof-build.log](evidence/stage3-proof-build.log) and
[stage3-positive-proof.log](evidence/stage3-positive-proof.log).

Thus verification closure is reproducible. This stage does not establish that
the added theory is sound.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The precondition `positiveInts(INPUT)` says that `INPUT` is a finite `ValSeq`
containing only K integers strictly greater than zero. It does not impose a
fixed size or numeric upper bound. `INPUT = vCons(1, .ValSeq)` is a concrete
satisfying witness.

From the pristine module configuration, the `<k>` cell loads two functions and
calls `unique_digits` on the bare list value `list(INPUT)`. The postcondition
requires:

- returned value `ref(1)`;
- the two loaded closures in module scope;
- heap location 0 containing `filterOddAcc(.ValSeq, INPUT)`;
- heap location 1 containing
  `sortVS(filterOddAcc(.ValSeq, INPUT))`;
- heap allocation counter 2, empty call stack, `noRet`, `NoExc`, and exit 0.

The return is not a free variable or tautology. Stage 6 confirms that `ref(1)`
is genuinely constrained.

### Constructor-level source identity

The candidate claim uses syntax macros for the two bodies. I parsed and
macro-expanded both the exact `Module` in the claim and trusted-regenerated
`solution.mpy`, emitted KORE, and compared them byte-for-byte. Both expanded
terms have SHA-256 `0b437317...8bbaf`; see
[stage4-program-pinning.log](evidence/stage4-program-pinning.log).
Accordingly, the claim text does pin the submitted function names, parameters,
bindings, and bodies. The unboxed read-only input is semantically inert for
this function because the function never mutates `x`.

### Result adequacy failure

For satisfying input `[1]`, the claimed result specializes to

```text
list(sortVS(filterOddAcc(.ValSeq, vCons(1, .ValSeq))))
```

and whether `1` is retained depends on the unconstrained symbol
`oddDigits(1)`. For `[2]`, the same issue occurs with `oddDigits(2)`. Both
Python implementations return `[1]` and `[]`, respectively, but the formal
postcondition does not determine either fact. It repeats the same opaque symbol
introduced by execution.

More decisively, a body-sensitivity experiment changed the helper body actually
loaded by the claim to `return False`, while changing the final scope only to
record that new closure and leaving the result-bearing heap obligation
unchanged. The expanded mutated `Module` hash is `bed66d4c...51ce`, distinct
from the submitted program hash. Nevertheless, `kprove` printed `#Top` and
exited 0. See [spec-body-mutation.k](evidence/spec-body-mutation.k),
[stage4-mutated-term-difference.log](evidence/stage4-mutated-term-difference.log),
and [stage4-body-sensitivity.log](evidence/stage4-body-sensitivity.log).

That mutation really returns `[]` on `[1]` in both Python and fresh fixed LLVM
execution; see
[concrete-mutated-helper.py](evidence/concrete-mutated-helper.py) and
[stage4-mutated-fixed-execution.log](evidence/stage4-mutated-fixed-execution.log).
After adding only the true intended ground facts `oddDigits(1) => true` and
`sortVS([1]) => [1]`, the candidate loop bridge proves that this mutated
program's result heap contains `[1]`. The false ground claim printed `#Top`;
see [witness-verification.k](evidence/witness-verification.k),
[spec-false-conclusion-witness.k](evidence/spec-false-conclusion-witness.k),
[stage4-false-witness-build-2.log](evidence/stage4-false-witness-build-2.log),
and
[stage4-false-conclusion-proof.log](evidence/stage4-false-conclusion-proof.log).

This is a concrete false-conclusion witness on the intended positive domain,
not merely an artifact-maintenance concern.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[stage5-rule-inventory.log](evidence/stage5-rule-inventory.log) enumerates the
complete source block and location for every local configuration, syntax
declaration, context, rule, and claim in the supplied semantics,
`verification.k`, and `spec.k`. The inventory contains 951 items:

- 235 syntax declarations;
- 1 configuration;
- 5 explicit contexts;
- 709 rules; and
- 1 claim.

It also classifies function/total/symbol/no-evaluator declarations, concrete,
priority, `owise`, macro, strictness, and ordinary rules. There are no local
`functional` or `simplification` rules in the candidate or supplied source.
The inventory script itself is preserved at
[k_rule_inventory.py](evidence/k_rule_inventory.py).

Items 0001-0928 are the supplied fixed semantics. I assessed every item at the
selected semantics level. On the used positive-integer path, the rules for
module loading, scope lookup, closure creation, calls/returns, allocation,
assignment, list iteration, `if`/`while`/`break`, integer `%` and `//`,
comparison/truth, append, and allocation preserve the expected cells,
evaluation order, and control behavior. Fresh concrete execution exercises
this path. I found no false-conclusion witness for these fixed used-path rules.

The unused range, float, string, set, tuple, subscript, comprehension, dict, and
unselected builtin/method cases have disjoint constructor or operation-name
heads and do not contribute to this claim. Their fixed opaque symbols are
inert here. I do not label an off-path rule unsound without a witness.

The relevant fixed abstraction is `sortVS` in
`semantics/sort.k:18`. It is an intentionally opaque model of the external
Python `sorted` builtin in proof builds, with concrete insertion-sort rules in
LLVM builds. The entry theorem remains parametric in `sortVS`; concrete K runs
and the independent differential suite support its intended interpretation.
This is an explicit low-level supplied trust boundary, not a proof of sorting
inside this claim.

The submitted constructors map to fixed rules as follows:

| Submitted construct | Declaration / execution rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53-60`; `functions.k:14-16` |
| `Name`, calls, argument order | `core.k:130-191`; `call.k:18-32,69-75`; `functions.k:62-90` |
| `Int`, `Bool`, assignment | `core.k:193-196`; `controls.k:8-31` |
| `%`, `//`, integer comparisons | `operators.k:10-20`; `int.k:9-27` |
| `If`, `While`, `Break`, `For` | `controls.k:50-108`; `list.k:9-10`; `tuple.k:31-41` |
| list literal and `append` | `list.k:12-20,52-55`; `call.k:15-24` |
| `sorted(result)` | `core.k:156-181`; `call.k:26-50`; `sort.k:18-42` |

### Candidate items 0929-0951

The exact per-item decisions are:

- **0929 — `oddDigits(Int)`**: illegitimate result-bearing abstraction. It is
  declared `[function, total, symbol, no-evaluators]` but has no equations and
  no bridge-free universal theorem connecting it to `oddDigitsBody`. `total`
  does not give it the decimal-digit meaning.
- **0930-0933 — `filterOddAcc`**: structurally descending and its true/false
  guards are disjoint if `oddDigits(N)` denotes a Boolean. Its claimed meaning
  is conditional on the illegitimate oracle, so it cannot establish the
  HumanEval filter.
- **0934-0936 — `lastInput`**: sound, total structural recursion; it returns
  the old value on empty input and the final input value otherwise.
- **0937-0940 — `positiveInts`**: sound, total structural characterization of
  finite sequences of strictly positive K integers. Integer and non-integer
  cases are disjoint.
- **0941-0948 — four body macros and expansion rules**: sound syntax
  normalization. Mechanical expansion proves exact equality with
  `solution.mpy`.
- **0949 — helper-call priority rule**: unsound operational bridge. It
  preempts execution of the program-defined helper and returns the opaque
  `oddDigits(N)`. It has no connection theorem. It omits guards on the active
  return state, stack, scopes, exception state, and other cells; its `...`
  accepts contexts broader than a normal call. Even in the valid original
  context its returned value is unconstrained.
- **0950 — source-loop priority rule**: unsound operational bridge. It
  preempts list iteration and all helper calls, directly fabricates the
  accumulator using `filterOddAcc`, and updates `n` using `lastInput`. It does
  not inspect or pin the `_all_digits_odd` binding in the module/parent scope,
  nor does it have a bridge-free loop theorem. Omitted return, stack,
  exception, allocation, and control cells broaden its match domain.
- **0951 — entry claim**: source-identical, domain-wide, and
  result-constraining, but it closes only relative to items 0929, 0949, and
  0950. Its postcondition repeats rather than discharges the opaque predicate.

Priority 40 makes items 0949 and 0950 preempt the fixed call and loop rules; it
does not justify equivalence.

### False witnesses for each rule labeled unsound

For item 0949, fixed `solution._all_digits_odd(2)` is `False`. Because
`oddDigits(2)` has no candidate definition, the opposite interpretation
`oddDigits(2) => true` is admitted. With that interpretation, a ground claim
that loads the exact submitted helper, calls it on `2`, and returns `true`
prints `#Top`. See
[helper-witness-verification.k](evidence/helper-witness-verification.k),
[spec-helper-false-witness.k](evidence/spec-helper-false-witness.k),
[stage5-helper-false-witness-build.log](evidence/stage5-helper-false-witness-build.log),
[stage5-helper-false-conclusion-proof.log](evidence/stage5-helper-false-conclusion-proof.log),
and [stage5-helper-fixed-python.log](evidence/stage5-helper-fixed-python.log).
This witnesses a false result for the helper bridge on positive input `2`.

For item 0950, the `return False` helper mutation and `[1]` experiment described
in Stage 4 are the witness. Fixed execution returns `[]`; the priority loop rule
ignores the changed binding and proves `[1]` when supplied the correct intended
ground digit/sort facts. This directly witnesses binding, body-sensitivity, and
value failure.

No candidate bridge-free universal connection claim exists for either rule.
Finite testing cannot supply one.

## 6. Fresh non-vacuity test

I created a fresh spec that changes only the result obligation from the actual
sorted-list reference `ref(1)` to accumulator reference `ref(0)`. The unchanged
precondition is satisfiable, for example by
`INPUT = vCons(1, .ValSeq)`. The mutation parsed and built successfully.

`kprove` exited 1 with `WarnStuckClaimState`. The residual explicitly shows the
actual `<k>` result `ref(1)`, so this is the expected unmet obligation, not a
parse error, timeout, or unrelated crash. See
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) and
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

The claim is therefore non-vacuous with respect to its return reference. That
does not make the operational bridges sound.

## 7. Proven versus assumed accounting

What the successful reachability run actually establishes is:

> In the extended theory where the exact submitted module is loaded, but calls
> to its helper are rewritten to an arbitrary total Boolean symbol and its
> source loop is rewritten to a summary over that same symbol, every
> `positiveInts(INPUT)` state reaches `ref(1)` with heap contents described by
> `sortVS(filterOddAcc(.ValSeq, INPUT))`.

It does **not** establish that `oddDigits(N)` is true exactly when every decimal
digit of `N` is odd, that the real helper computes that symbol, or that the real
loop produces `filterOddAcc`.

Trust ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| Supplied MPY operational semantics and K integer/map/list primitives | All execution and state | Accepted selected-semantics boundary; candidate tree is byte-identical to trusted tree |
| Partial Python model / positive-int subset | Evaluation, exceptions, object behavior | Adequate for the stated positive-integer contract and used constructs |
| `sortVS` supplied opaque builtin | Final result ordering | Explicit external builtin assumption; acceptable conditionally, finitely supported by concrete K and differential tests |
| `oddDigits` candidate opaque symbol | Branches, filter membership, final result | Illegitimate program-derived oracle; no equations or connection theorem |
| Helper priority bridge | Helper value and skipped call control | Illegitimate; false ground witness at `2` |
| Loop priority bridge | Binding, all iterations, accumulator, final result | Illegitimate; false body/binding witness at `[1]` |
| Body macros | Program identity | Mechanically validated exact expansion |
| Differential tests | Python implementation fidelity and finite semantic behavior | Empirical only; cannot replace either universal bridge theorem |

Gate A (real-program soundness) fails with machine-checked false witnesses.
Gate B's input domain is not materially narrowed, but summary-to-property
adequacy fails because the decisive digit property remains arbitrary. Gate C
evidence is reproducible, yet it explicitly exposes rather than discharges the
illegitimate trust boundary.

Under the benchmark decision rule, a proof that executes summaries capable of
proving false results for a materially changed program is `FAIL / NOT_LEGIT`,
even though the retained positive claim reconstructs to `#Top` and the
submitted Python program is correct.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
