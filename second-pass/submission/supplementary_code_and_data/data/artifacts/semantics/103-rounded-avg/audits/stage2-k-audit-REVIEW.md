# Independent adversarial review: 103-rounded-avg

This audit reconstructed the proof from source and treated all candidate and
generation records as untrusted evidence. The proof is legitimate: its two
local equations expose the actual translated function body to the fixed
semantics, all four positive claims close from a clean build, the guards cover
the unrestricted positive-integer source domain, and independent body and
postcondition mutations fail. The concern is a real implementation/reference
disagreement at very large integers: the trusted canonical uses binary64
division and ceases to implement the exact prose contract above its precision
range, whereas the generated integer program and theorem remain exact.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1` and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, as this mode requires.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the invocation and metrics records,
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the single
structured JSONL trace. Historical runtime metrics are not required for this
legacy-selected-stage1 layout. The historical `#Top`, final response, commands,
and claimed differential results were not reused.

The campaign-lock file hashes to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value, and its JSON object equals the campaign block in
`audit-input.json`. All nine required generation records are real regular
files. Their independently calculated SHA-256 values match the launcher
records. The trace's only file hashes to the value recorded by
`generation-result.json`, and an independent typed tree hash matches
`usage.json`.

The current candidate tree independently hashes to
`44d6c4faa59f45ac201313c4d4f2a3960743ef4c7e1d2b728cce33ccbbd7f40c`,
matching both the invocation's retained-workspace hash and the stage result's
workspace hash. The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`.

The candidate and trusted supplied-semantics trees have identical entry names,
entry types, and file contents. Each typed-tree manifest hashes to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
Neither tree contains a symlink or unsupported entry; there is no missing,
additional, mistyped, or changed semantics entry. Thus there is no
infrastructure breach and no semantics-integrity failure.

Evidence: `evidence/provenance_check.py` and
`evidence/stage1-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract says that `n` and `m` are positive integers. If `n > m`,
the result is `-1`. Otherwise, compute the arithmetic mean of every integer in
the inclusive interval, round it to the nearest integer using the canonical
Python implementation's half-even tie behavior, and return the rounded integer
in Python `bin` form.

`solution.py` uses the identity

`average(n..m) = (n + m) / 2`

for a nonempty consecutive-integer interval. It sets
`average = (n+m)//2`; when the sum is odd, it increments exactly when the lower
neighbor is odd. This is precisely half-even rounding. It then calls `bin`.
The inverted interval returns `-1` before any arithmetic.

A fresh run of the trusted translator followed by `cmp` exited 0:

`python3 /reference/py2mpy.py /candidate/solution.py | cmp - /candidate/solution.mpy`

Therefore the submitted `solution.mpy` is byte-identical to trusted
regeneration.

The independent differential script imports both trusted canonical and
generated entry points and uses a separately implemented `Fraction`/half-even
oracle. It covers the four examples, inverted/empty and singleton boundaries,
each parity branch, every pair in `[1,200]^2`, 5,000 deterministic generated
cases with seed 103, and six large precision/overflow boundaries. Across
45,018 inputs there are zero generated-versus-exact-contract mismatches.

There are three canonical-versus-exact mismatches and one canonical exception.
For example, at `n=m=2**53+1`, the canonical converts through binary64 and
returns the binary form of `2**53`, while the generated program returns the
exact binary form of `2**53+1`. At `n=m=10**309`, the canonical raises
`OverflowError`. This is not a narrowing of the submitted theorem: the K claims
and generated Python program cover arbitrary positive integers. It is a
non-universal bridge to the trusted canonical implementation and is the reason
for `CONCERNS` rather than `PASS`. I judge the generated behavior to satisfy
the mathematical prose contract more faithfully on these inputs, so this does
not invalidate the proof of the submitted program.

Evidence: `evidence/differential_test.py` and
`evidence/stage2-program-fidelity.log`.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/103-rounded-avg` from candidate source artifacts,
the trusted prompt and translator, and the trusted supplied-semantics tree. No
candidate-built definition, cache, or `*-kompiled` directory was copied.

K version 7.1.293 was independently available. Fresh LLVM and Haskell builds
both exited 0. The concrete assertion module terminated with `.K`,
`NoExc`, and `<exit-code> 0</exit-code>`. Its function definition is
AST-identical to `solution.py`.

The combined target command

`kprove spec.k --definition audit-verification-kompiled --spec-module ROUNDED-AVG-SPEC`

exited 0 and printed `#Top`. I also copied each unchanged candidate claim into
a distinct audit module and ran it independently. The inverted, integral,
half-down, and half-up commands each exited 0 and printed `#Top`.

The only build warnings concern unused variables in supplied `strLt` rules and
some concrete-backend non-exhaustive total functions outside the target path.
There was no proof warning, stuck state, or nonzero positive target.

Evidence: `evidence/stage3-clean-reconstruction.log` and the four
`evidence/audit-claim-*.k` files.

## 4. Adequacy and real-program pinning

The four entry claims state:

1. For positive `N,M` with `N>M`, the call returns integer `-1`.
2. For positive `N<=M` and even `N+M`, it returns
   `"0b" + binCodes((N+M)/2)`.
3. For a valid odd sum whose lower neighbor is even, it returns the lower
   neighbor in binary.
4. For a valid odd sum whose lower neighbor is odd, it returns the upper
   neighbor in binary.

The guards are pairwise disjoint and exhaustive for positive integers. The
four concrete satisfying witnesses `(2,1)`, `(1,5)`, `(2,3)`, and `(1,2)`
respectively make the claim result, generated Python result, and canonical
result agree.

`roundedAvgBody` does not summarize the result or bypass execution. An audit
script parses `solution.mpy` and the right-hand side of the
`roundedAvgBody` equation with fresh `kast`, extracts their constructor trees,
and obtains the same SHA-256
`07a9a74728e54323df9d64695ff3bf980b86bf7ca9d8e969de666e3fd4dafd57`.

`roundedAvgCall(N,M)` expands to a fixed-semantics `Call` of a closure with
parameters `("n","m")`, that exact body, and definition scope 0. Loading the
actual one-definition module would bind exactly that closure in scope 0;
directly supplying it only omits a semantically inert binding and lookup. The
body neither reads its own function name nor performs another module-level
effect. Every claim initializes scope 0 and builtins scope -1 consistently
with that closure.

Fixed semantics then performs normal callee/argument evaluation, parameter
binding, local assignments, integer operations, conditionals, builtin lookup,
`bin`, return, frame pop, and restoration of environment, scopes, stack,
return state, exception state, heap, and allocation counters. The result is a
specific `str(...)` or `-1`, not a free variable, tautology, implication-only
postcondition, or opaque candidate oracle.

For body sensitivity, I changed the executed AST term from `average + 1` to
`average + 2` while leaving all four claims unchanged. The mutant built
successfully, but `kprove` exited 1 with a stuck implication in the half-up
claim. The satisfying witness `(1,2)` distinguishes the mutant's `"0b11"`
from the required `"0b10"`.

Evidence: `evidence/constructor_pinning.py`,
`evidence/claim_witnesses.py`, `evidence/make_body_mutant.py`,
`evidence/verification-body-mutant.k`,
`evidence/spec-body-mutant.k`, and
`evidence/stages4-6-adequacy-static-nonvacuity.log`.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory covers the assembled semantics, every supplied
helper K file, candidate `verification.k`, and `spec.k`: 697 rules, 229 syntax
declarations, five contexts, one configuration, and four claims. It records
every complete source block and line number. There are 147 function-bearing
declarations, 109 total-bearing declarations, 25 symbol-bearing declarations,
22 `no-evaluators` declarations, 35 concrete-only rules, 41 priority rules, 26
`owise` rules, and four macro declarations. There are no `functional`,
`simplification`, `simplify`, `anywhere`, or alias declarations.

The used constructor/rule path is:

- `syntax.k`: `Int`, `Name`, `UnaryOp`, `BinOp`, `Compare`, `CmpOp`, `Call`,
  `Assign`, `If`, `Return`, statement/argument lists, parameters, and strict or
  sequentially strict evaluation.
- `core.k`: the stated configuration, statement sequencing, lexical lookup
  through scopes 1, 0, and -1, builtins registry, left-to-right argument
  evaluation, integer literals, truthiness, and value-list append.
- `operators.k` and `int.k`: ordinary integer unary minus, addition, modulo,
  floor division by 2, `>`, and `==`. `pyMod` is the correct floor-modulo
  equation for the used positive divisor.
- `controls.k`: local assignment and truthiness-based branch selection.
- `call.k` and `functions.k`: callee-first evaluation, exact closure frame
  creation, parameter binding, abrupt return within that frame, caller
  continuation restoration, frame deletion, and `scopeLoc` restoration.
- `builtins.k`: resolved one-argument `bin` and the descending `binCodes` /
  `binAcc` recurrence. Its nonnegative/negative guards partition integers; all
  target arguments are positive.

The configuration and rules preserve evaluation order, bindings, allocation,
control, and every observable target cell. Ref, cell, collection, float, sort,
method, loop, dict, comprehension, and concrete-only priorities are
constructor- or guard-disjoint from this integer/string path.

Candidate `verification.k` adds only two unconditional one-step definitional
equations. They are terminating, nonoverlapping, cover their declared domains,
and introduce no opaque value, priority, simplifier, arithmetic lemma, control
effect, wildcard continuation, or state rewrite. `spec.k` adds no rule.

The fixed semantics contains 25 symbol-bearing boundaries:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs in or can
affect the target's execution or postcondition. `binCodes` is not opaque; its
complete used-domain equations are visible and descending.

All rules were assessed by source file and family in the companion assessment.
The supplied language is intentionally a restricted Python subset, so the
assessment does not recast unused support as a full CPython model. No
false-conclusion witness was found for a rule that can match the target domain,
and no rule is labeled unsound.

Evidence: `evidence/rule_inventory.py`,
`evidence/static-rule-inventory.md`, and
`evidence/static-rule-assessment.md`.

## 6. Fresh non-vacuity test

`spec-vacuity-audit.k` leaves the real program term, all initial cells, and the
integral-mean guard unchanged, but changes the destination from
`bin((N+M)/2)` to `bin((N+M)/2+1)`. It is well-formed and reached the prover;
there was no parser failure, missing import, crash, or timeout.

The command

`kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-VACUITY`

exited 1. `WarnStuckClaimState` reports a failed implication between the
program's `binAcc((N+M)/2,...)` result and the mutated
`binAcc((N+M)/2+1,...)` destination under the original satisfiable guard. The
ground witness `(1,5)` requires `"0b100"` in the mutation while the program
returns `"0b11"`. This is the expected unmet result obligation.

Evidence: `evidence/spec-vacuity-audit.k` and
`evidence/stages4-6-adequacy-static-nonvacuity.log`.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following under the supplied
MPY semantics: from the explicitly stated initial cells, for every pair of
positive mathematical integers, executing the closure containing the exact
submitted function body reaches the precise K integer/string result described
by the applicable one of the four exhaustive claims, while restoring the
listed caller state. This is a partial-correctness theorem. It is not merely a
test result or a theorem about a substituted result function.

The trust ledger is:

- K 7.1.293, its Haskell reachability backend, and K's integer, Boolean,
  string, map, list, and equality hooks are foundational trusted primitives.
- The launcher-supplied semantics is the fixed language boundary. Its
  target-used rules were statically checked; its 25 opaque symbols are unused
  by this theorem.
- The trusted translator is an input boundary. Byte identity and mechanical
  constructor comparison connect `solution.py`, `solution.mpy`, and the body
  executed by the claims.
- The arithmetic-series identity reducing the inclusive interval mean to
  `(n+m)/2`, and the parity characterization of half-even rounding, are
  ordinary mathematical arguments outside the K claim. They are exact for the
  complete positive-integer domain.
- The meaning of ASCII codes 48 and 98 and the descending `binCodes` equations
  connect the K string to Python's `bin` representation. These equations are
  fixed and inspected, not candidate-provided assumptions.
- Concrete and differential tests are finite supporting evidence only. They
  are not used as a substitute for the K proof.
- The trusted canonical is not a universal oracle for the prose contract
  because its float conversion loses precision and can overflow on valid large
  positive integers. This is a documented nonfatal validation limitation, not
  an assumption hidden inside the proof.

Gate A (real-program soundness and non-vacuity) passes. Gate B passes against
the mathematical source contract with the documented canonical-reference
disagreement. Gate C passes for reproducibility and trust disclosure. The
canonical disagreement is material enough to prevent an unqualified `PASS`,
but it does not make a false K conclusion provable, substitute the program,
narrow the domain, or invalidate the theorem. The appropriate benchmark
mapping is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
