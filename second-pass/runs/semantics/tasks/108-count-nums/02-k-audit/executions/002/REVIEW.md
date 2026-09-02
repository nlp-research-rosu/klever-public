# Independent adversarial review: 108-count-nums

The candidate’s implementation is faithful, its submitted program is pinned
mechanically, all fresh positive proof runs close, and a fresh false
postcondition is rejected. The proof is nevertheless not legitimate: five
proof-local operational rewrite rules are materially broader than their
supporting claims. Fresh bridge-free/bridge-enabled witnesses show that those
rules enable conclusions contrary to fixed-semantics execution.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1` and `semantics_mode = SUPPLIED_SEMANTICS`. The mounted
`/reference/reference-semantics` exists, as this mode requires.

The launcher-owned records are intact:

- The JSON value in `/audit-campaign-lock.json` is exactly equal to the
  `audit_campaign` block in `/audit-input.json`; its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  as recorded.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt` are regular files and independently
  reproduce their recorded hashes.
- The sole structured trace is a regular JSONL file with 661 readable
  records and raw SHA-256
  `0eb50b984d91e220da0552dadae039628de386da86689a5b77fc984b7be8e3ed`.
  Its hash also matches the per-file output hash in the stage-1 result.
- The complete 80,135-line `codex-output.log` was read and indexed. It and
  the trace contain historical failed attempts as well as the final success;
  none was used as proof evidence.
- A historical `runtime-metrics.json` is absent, but that record is not
  required for `legacy-selected-stage1`. The present `usage.json` was
  inspected as required.

The trusted prompt and translator independently hash to the recorded values.
Candidate copies are byte-identical to them. The candidate and trusted
supplied-semantics trees have identical recursive manifests: the same 24
regular files, the same relative names, and the same file hashes. Neither
tree, nor any other mounted input tree, contains a symlink. All five required
candidate proof artifacts are present as regular files.

Evidence:
[integrity script](/audit-output/evidence/audit_integrity.py),
[integrity log](/audit-output/evidence/01-integrity.log), and
[generation trace inspection](/audit-output/evidence/01-generation-trace-inspection.log).
There is no infrastructure breach.

## 2. Program fidelity and canonical comparison

The source contract is: given a finite array of integers, count elements whose
decimal digit sum is positive. For a negative integer, the most significant
decimal digit carries the negative sign; for example, `-123` contributes
`-1 + 2 + 3 = 4`. The documented results are `0` for `[]`, `1` for
`[-1, 11, -11]`, and `3` for `[1, 1, 2]`.

The candidate implements the same contract with arithmetic loops:

- `positive_digit_sum` repeatedly adds `n % 10` while `n > 0`.
- `negative_digit_sum` accumulates all but the leading magnitude digit while
  `n >= 10`, then subtracts the remaining leading digit.
- `signed_digit_sum` selects the appropriate helper, and `count_nums` counts
  positive results.

Running the trusted translator over the scratch copy produced SHA-256
`047da4fbb79a015327f8843735ad63ab646bbbf86b1c9530e2652b9b2f43b808`,
byte-identical to submitted `solution.mpy`. See
[translation log](/audit-output/evidence/02-translation-identity.log).

The independent differential test imports the trusted canonical and submitted
entry points separately. It covers the three documented examples, empty input,
all sign/loop/decimal/result boundaries, every list through length four over
nine selected boundary values, and 2,000 deterministic arrays containing
integers up to 100 decimal digits. It tested 9,421 arrays and found zero
mismatches. See
[differential script](/audit-output/evidence/differential_test.py) and
[results](/audit-output/evidence/02-differential.log).

This finite evidence supports implementation-to-contract fidelity; it is not
used as a substitute for a universal K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`.
Candidate compiled definitions and caches were neither copied nor reused. The
supplied semantics used for rebuilding came from the trusted reference mount.
The live toolchain reports K `v7.1.293`.

A fresh LLVM definition compiled from
`reference-semantics/semantics.k`. The independently regenerated concrete test
program was byte-identical to its submitted translation, and `krun` terminated
with `<exc> NoExc </exc>` and `<exit-code> 0 </exit-code>`.

Six fresh Haskell definitions were compiled in the candidate’s staged order.
Every positive target command exited zero and printed `#Top`:

| Target module | Fresh definition | Result |
|---|---|---|
| `POSITIVE-LOOP-SPEC` | `COUNT-NUMS-VERIFICATION-BASE` | exit 0, `#Top` |
| `NEGATIVE-LOOP-SPEC` | `COUNT-NUMS-VERIFICATION-BASE` | exit 0, `#Top` |
| `POSITIVE-FUNCTION-SPEC` | `DIGIT-LOOP-LEMMAS` | exit 0, `#Top` |
| `NEGATIVE-FUNCTION-SPEC` | `DIGIT-LOOP-LEMMAS` | exit 0, `#Top` |
| `SIGNED-FUNCTION-SPEC` | `DIGIT-FUNCTION-LEMMAS` | exit 0, `#Top` |
| `COUNT-LOOP-WITH-N-SPEC` | `SIGNED-DIGIT-LEMMA` | exit 0, `#Top` |
| `COUNT-LOOP-SPEC` (two claims) | `COUNT-LOOP-WITH-N-LEMMA` | exit 0, `#Top` |
| `COUNT-NUMS-SPEC` | `COUNT-LOOP-LEMMA` | exit 0, `#Top` |

The exact commands and exit statuses are in
[the reconstruction driver](/audit-output/evidence/run_positive_proofs.sh),
[the summary](/audit-output/evidence/03-reconstruction-summary.log), and the
individual bounded `03-*.log` files. These successes establish closure under
the staged theory; they do not validate that theory’s added rules.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `POSITIVE-LOOP-SPEC`: for any nonnegative `N` and any integer accumulator
  `A`, the exact positive loop ends with local `n = 0` and
  `total = positiveFold(N, A)`.
- `NEGATIVE-LOOP-SPEC`: for nonnegative magnitude `N`, the exact negative loop
  leaves the leading digit in `n` and the lower-digit accumulation in
  `total`.
- The positive and negative function claims apply the exact corresponding
  closures to every nonnegative integer and return their mathematical digit
  summaries in an otherwise clean initial configuration.
- `SIGNED-FUNCTION-SPEC` applies the exact signed helper to any K integer in a
  scope containing the exact helper bindings and returns `signedDigitSum(N)`.
- `COUNT-LOOP-WITH-N-SPEC` covers an arbitrary all-integer list tail when `n`
  is already bound. It advances `count` by `countFold`, preserves `arr`, and
  leaves `n` bound to the last iterated value.
- `COUNT-LOOP-SPEC` separately covers the empty initial loop (where `n` stays
  absent) and a nonempty all-integer initial loop.
- `COUNT-NUMS-SPEC` applies the exact `count_nums` closure to an arbitrary
  `ValSeq` satisfying `allInts(VS)` and requires the returned value to equal
  `countPositive(VS)`.

Thus the formal entry domain is unbounded in both list length and integer
magnitude; it does not reduce the HumanEval contract to examples or bounded
sizes.

### Satisfying states and ground substitution

The loop preconditions are satisfiable, for example with environment location
1, parent 0, `N = 109`, and `A = 7`. The function preconditions are satisfied
by `N = 109` in the stated clean configurations; the signed claim is satisfied
by `N = -109`. The count-loop and entry preconditions are satisfied by
`VS = vCons(-1, vCons(11, vCons(-11, .ValSeq)))`, `C = 0`, location 1, and
the stated helper bindings.

Fresh ground K simplification proves:
`positiveDigitSum(109) = 10`, `negativeDigitSum(109) = 8`,
`signedDigitSum(-109) = 8`, `signedDigitSum(-123) = 4`,
`allInts([-1,11,-11]) = true`, and
`countPositive([-1,11,-11]) = 1`. Both Python implementations also return 1
on that entry witness. See
[ground K claims](/audit-output/evidence/audit-witness-spec.k),
[ground proof log](/audit-output/evidence/04-ground-witness-kprove.log), and
[Python comparison](/audit-output/evidence/04-witness-python.log).

### Mechanical program identity

Using the freshly compiled syntax, the reviewer parsed submitted
`solution.mpy` and expanded every candidate macro. The four proof closure
bodies and parameter lists are exactly constructor-equal to the four submitted
`FuncDef` bodies; all closure definition environments are 0. The three helper
bindings are exactly the corresponding submitted closures. See
[constructor checker](/audit-output/evidence/constructor_identity.py) and
[result](/audit-output/evidence/04-constructor-identity.log).

The entry claim directly invokes the exact `count_nums` closure instead of
executing the top-level module-loading statements. Because the helper bindings
and closure body are mechanically identical, this is semantically inert
normalization, not a substituted program. The returned value is constrained
by equality to `countPositive(VS)`, not left free.

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains 1,210 declarations: 252 syntax
declarations, 737 rules, five contexts, one configuration, nine claims, and
all module/import/require scaffolding. Each row records complete rule text,
attributes, target relevance, and a review decision. See
[rule inventory](/audit-output/evidence/rule-inventory.tsv) and
[inventory builder](/audit-output/evidence/build_rule_inventory.py).

### Used fixed-semantics path

Every construct in `solution.mpy` maps to the supplied declarations and rules:

- `Module`/`FuncDef` load plain closures into scope 0.
- `Name`, the scope chain, parameter binding, call frames, `Return`, and frame
  pop implement helper calls and restore control state.
- `Assign` and integer `AugAssign` update the current scope.
- strict `BinOp`/`Compare` evaluation and the integer rules implement
  `+`, `-`, `%`, `//`, `<`, `>`, and `>=`.
- `If`, `While`, `For`, `#iterNext`, list iteration, and `#bindTgt(Name, V)`
  implement the actual control flow and loop-target update.

On this path, evaluation order, bindings, call/return control, scope updates,
and arbitrary-precision integer arithmetic agree with the submitted program.
No heap allocation, exception, floating-point, string, dict, set, sorting, or
external-state behavior affects the symbolic entry claim. The supplied opaque
float functions, `sortVS`, `sortKeyVS`, and `md5hexCodes` are imported but
unreachable from every target result dependency.

The proof-side mathematical functions have disjoint guards and descending
recursion on intended uses. `digitQuot` is floor division by positive 10;
the positive and negative folds encode the two loops; `positiveBit` encodes
the branch; and `countFold` is used only beneath `allInts`. `countFold` is
declared total but has no defining equation for a non-integer list head. That
is a coverage limitation outside every claimed `allInts` path, not a witness
of a false conclusion on the source domain.

All statement/closure macros are exact by the constructor check. The two
digit-loop rewrite rules at
[verification.k:145](/candidate/verification.k:145) and
[verification.k:159](/candidate/verification.k:159) have bridge-free claims
with the same guards, continuation framing, cells, and state updates. The
empty initial count-loop rule at
[verification.k:220](/candidate/verification.k:220) does not execute the body
or observe a helper binding and is also valid.

### Materially unsound operational bridges

Five rules do not satisfy context containment. Their priority 40 causes them
to preempt fixed execution throughout a match domain broader than the theorem
used to justify them. The reviewer supplied concrete false-conclusion
witnesses, not merely an absence-of-proof objection:

| Candidate rule | Omitted context and false witness | Bridge-free behavior | Bridge-enabled behavior |
|---|---|---|---|
| Positive and negative helper rules at [177](/candidate/verification.k:177) and [182](/candidate/verification.k:182) | The supporting claims require a clean `noRet` configuration, but the rules constrain only `<k>` and the integer guard. With intended integer input `1` and `<ret> retV(42) </ret>`, fixed execution reaches a `Return` that cannot fire. | Nonzero with `WarnStuckClaimState` | Exit 0, `#Top`, fabricating `1` and `-1` |
| Signed-helper rule at [191](/candidate/verification.k:191) | The supporting claim pins `digitFunctionBindings`; the rule omits all scope cells. Rebind `negative_digit_sum` to the exact closure `return 99` and apply the signed closure to intended integer `-1`. | Returns 99; proves the `99` claim and rejects `-1` | Exit 0, `#Top` for `-1` |
| Count loop with existing `n` at [200](/candidate/verification.k:200) | The supporting claim pins the module helper bindings; the rule does not. On integer list `[-1]`, rebind `signed_digit_sum` to return 99. | Executes the real body and leaves `count = 1` | Exit 0, `#Top` for fabricated `count = 0` |
| Nonempty initial count loop at [230](/candidate/verification.k:230) | Same omitted binding and same intended list witness, starting before `n` exists. | Executes the real first iteration and leaves `count = 1, n = -1` | Exit 0, `#Top` for fabricated `count = 0, n = -1` |

The exact witness modules are in
[operational-bridge-witness-spec.k](/audit-output/evidence/operational-bridge-witness-spec.k).
[The driver](/audit-output/evidence/run_bridge_witnesses.sh) records every
argument vector and validates that expected failures are genuine stuck claims.
The corresponding bounded `05-helper-*`, `05-signed-*`,
`05-count-with-n-*`, and `05-count-initial-*` logs preserve the results.

The helper `retV` witness is a syntactically valid state in the rules’ declared
match domain. The signed and count witnesses additionally use normal
`noRet`/empty-stack control state and intended integer inputs; only a binding
that the rules failed to constrain differs. Calling these bad states
unreachable cannot justify globally false reusable rules. The rules would
need either the complete cells/continuation/bindings of their proved claims or
bridge-free universal connection theorems over their present domains. They
have neither.

These false rules are not inert. The staged dependency chain imports the
helper rules to prove the signed function, the signed rule to prove the
with-`n` count loop, the with-`n` rule to prove the initial count loop, and the
initial loop rules to close the final entry claim. Therefore the final `#Top`
depends on a theory containing materially unsound execution shortcuts.

Gate A (real-program soundness) fails. Program identity and domain adequacy do
not cure this failure.

## 6. Fresh non-vacuity test

The reviewer created a distinct mutation that changes the final entry result
from `countPositive(VS)` to `countPositive(VS) +Int 1`. Its precondition is
satisfiable; `VS = .ValSeq` makes the real and original specified result 0,
while the mutation demands 1.

The mutated spec compiles successfully under `kprove --dry-run` (exit 0).
Actual proof exits 1 with `WarnStuckClaimState`; the residual explicitly
contains the failed obligation equating the fold with that fold plus 1. This
is a meaningful result failure, not a parser error, timeout, missing import,
or unreachable mutation.

Evidence:
[mutation](/audit-output/evidence/spec-vacuity-audit.k),
[dry run](/audit-output/evidence/06-vacuity-dry-run.log), and
[failed proof](/audit-output/evidence/06-vacuity-proof.log).
The entry theorem is discriminating, but non-vacuity does not make its
unsound proof extensions valid.

## 7. Proven versus assumed accounting

What the fresh successful proof literally establishes is conditional on the
extended K theory: for every finite `ValSeq` satisfying `allInts`, applying
the exact submitted `count_nums` closure in the stated initial configuration
reaches `countPositive(VS)`. The constructor identity, ground summary values,
and false-postcondition rejection are all independently reproducible.

The trust ledger is:

- K’s integer, Boolean, map/list, equality, and reachability machinery, plus
  the K 7.1.293 compiler/backend, are foundational trusted primitives.
- The supplied semantics is the selected fixed execution model. Its used
  integer/list/call/control rules were reviewed and have no target-path
  counterexample. Its unrelated opaque float, sort, string-order, subscript
  totalization, and MD5 boundaries cannot influence this theorem.
- The trusted translator is used only for source-to-constructor fidelity;
  byte regeneration and constructor comparison support that bridge.
- The canonical Python implementation and the 9,421 differential cases are
  finite empirical evidence of implementation intent, not proof axioms.
- Partial correctness assumes termination. On valid finite integer lists the
  program in fact terminates because each digit loop strictly decreases a
  nonnegative magnitude by base-10 quotient and the list loop is finite.
- There is no result-bearing external primitive on the target path.
  `intValue` and the digit/count summaries are candidate-defined equations,
  not external oracles.
- The five broad operational bridges above are illegitimate assumptions:
  they replace program-defined execution on states outside their supporting
  theorems, and machine-checked witnesses show wrong results or fabricated
  progress.

The formal input restriction `allInts(VS)` matches the material HumanEval
source domain and is not a finite/bounded narrowing. The failure is instead
the proof’s unsound local theory. Under the benchmark decision boundary,
fresh `#Top`, exact program pinning, differential agreement, and non-vacuity
cannot rescue a proof that relies on materially unsound operational rules.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
