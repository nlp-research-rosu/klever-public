# Independent adversarial audit: 96-count-up-to

## Outcome

The candidate contains a legitimate universal partial-correctness proof for the
submitted implementation over the complete stated domain of non-negative
integers. Fresh reconstruction closes all three claims, the false-result
mutation is rejected for the expected unmet result obligation, and the exact
program term is mechanically pinned.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, because the individually
generated semantics uses a monolithic exact-program lowering into a custom
`scan`/`trial` state machine. The lowering is faithful and non-oracular, but its
connection to Python is an audited informal bridge rather than a separately
proved compositional semantics. Two proof-side `[total]` declarations are also
broader than their equations off the reachable theorem domain. Neither concern
permits a false conclusion for `N >= 0`, so neither is a legitimacy failure.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `96-count-up-to`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- complete input provenance; and
- container mounts for the candidate, trusted prompt/canonical/translator,
  campaign lock, run/task/result records, and generation evidence.

I used the container paths, not the host provenance paths. The independent
checker `/audit-output/evidence/integrity_check.py` verified all required
launcher and legacy-selected-stage1 records as real readable regular files,
walked candidate/generation trees for symlinks or unsupported nodes, parsed all
207 structured-trace JSONL records, and checked all declared per-file hashes.
The output is `/audit-output/evidence/01-integrity.log`.

Specific results:

- `/audit-campaign-lock.json` hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the audit-input value, and its JSON object exactly equals the
  `audit_campaign` block.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the sole structured-trace JSONL file
  all match their recorded hashes.
- The mounted candidate has the exact stage-1 workspace tree digest
  `7666da4ff6c5e604ecac333bb785b4922c13131976bbd556b40518e5330d2869`
  recorded by both `generation-result.json` and `invocation.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions.
- `/reference/reference-semantics` is absent, as GENERATED_SEMANTICS requires.
- All required candidate deliverables exist: `solution.py`, `solution.mpy`,
  `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. The extra
  `__pycache__` is a regular cache artifact and was not used. No
  candidate-built K definition was present or reused.

The generation records were inspected only as untrusted historical claims.
Their structured contents and claimed build/proof actions are bounded in
`/audit-output/evidence/01-trace-summary.log`; nothing in those claims was used
as a proof result. Historical runtime metrics are absent, which is expressly
permitted for this legacy-selected-stage1 layout; the present `usage.json` was
inspected. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify: for every
non-negative integer `n`, return in ascending order all prime integers strictly
less than `n`. The examples establish that “first n integers” is not a length
requirement; the result is all primes below the bound.

`solution.py` starts `candidate` at two, tests divisors from two while
`divisor * divisor <= candidate`, appends candidates whose flag remains true,
and increments the candidate until it reaches `n`. It is a different but
equivalent algorithm to the canonical full trial division. No break is needed:
after a divisor is found the flag remains false.

Trusted regeneration command:

```text
python3 /tmp/audit-work/96-count-up-to/trusted/py2mpy.py /tmp/audit-work/96-count-up-to/candidate/solution.py > /tmp/audit-work/96-count-up-to/build/regenerated-solution.mpy
cmp -s /tmp/audit-work/96-count-up-to/build/regenerated-solution.mpy /tmp/audit-work/96-count-up-to/candidate/solution.mpy
```

Both files hash to
`f3d90b24a900cac792edf56af7c2e9b0b5d23a6318e23844a745a4867e85dc87`;
the command exits zero (`/audit-output/evidence/02-translation.log`).

The independent differential
`/audit-output/evidence/differential.py` imports the trusted canonical and
candidate modules separately. It tests all six documented examples, every
integer from 0 through 25, prime/square transition points, fixed cases through
1000, and 64 seed-recorded generated inputs. There are 104 unique inputs and
zero mismatches (`/audit-output/evidence/02-differential.log`). This supports
implementation fidelity but is not substituted for the K proof.

## 3. Clean proof reconstruction

All source inputs were copied to `/tmp/audit-work/96-count-up-to`. Builds went
to new directories under `build/`; the candidate cache and any historical
compiled output were ignored. The toolchain is K 7.1.293
(`/audit-output/evidence/03-toolchain.log`).

Fresh build commands:

```text
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/96-count-up-to/build/semantic-kompiled
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/96-count-up-to/build/verification-kompiled
```

Both exit zero (`03-kompile-semantics.log`,
`03-kompile-verification.log`). An earlier reviewer wrapper attempt tried an
unavailable `/usr/bin/time` and exited 127 before invoking `kompile`; it is
preserved as `03-kompile-semantics-attempt1.log` and has no bearing on the
successful clean build.

Positive claims were selected with their actual dependency closures:

```text
kprove spec.k --definition .../verification-kompiled --spec-module SPEC --claims SPEC.trial-correct --output pretty
kprove spec.k --definition .../verification-kompiled --spec-module SPEC --claims SPEC.trial-correct,SPEC.scan-correct --output pretty
kprove spec.k --definition .../verification-kompiled --spec-module SPEC --claims SPEC.trial-correct,SPEC.scan-correct,SPEC.count-up-to-correct --output pretty
```

Each command prints exactly `#Top` and exits zero
(`/audit-output/evidence/03-kprove-trial.log`,
`03-kprove-scan.log`, and `03-kprove-entry.log`).

The diagnostic selection of `scan-correct` alone removed its
`trial-correct` circularity, unrolled symbolic divisors, and eventually ended
with K's `DecidePredicateUnknown`; that nonzero run is preserved as
`03-kprove-scan-without-helper.log`. It is not a failed reconstruction of the
submitted proof, whose scan claim explicitly depends on the independently
closed trial claim.

The generated semantics was also freshly executed. Boundary runs for `N=0`
and `N=20` are in `03-krun-n0.log` and `03-krun-n20.log`.
`/audit-output/evidence/concrete_compare.py` runs 16 K cases spanning empty
loops, prime/composite/square branches, examples, and `N=97`; every K `nil` /
`cons` result equals both Python implementations, with all commands and exit
statuses in `03-concrete-compare.log`.

## 4. Adequacy and real-program pinning

Plain-language claims:

1. `trial-correct`, under `C >= 2` and `D >= 2`, says the remaining inner
   divisor loop advances to the next candidate and prepends `C` exactly when
   the existing flag and all remaining divisor tests both say prime.
2. `scan-correct`, under `C >= 2`, says scanning every candidate in `[C,N)`
   returns exactly `primesFrom(C,N)` in ascending order.
3. `count-up-to-correct`, under `N >= 0`, starts from the exact submitted
   module term and an empty result cell, reaches empty computation, and changes
   the result to `primesBelow(N)`.

The postconditions are equalities in destination cells/terms, not free result
variables, tautologies, or one-way implications.

`/audit-output/evidence/program_pinning.py` extracts the `Module` term from
`solution.mpy`, the whole-program semantic rule, and the entry claim. K's
parser produces the identical constructor KAST hash
`86365fdc6e3b663c7458b13d987e31f3ce08cdc8f478d80d27bcd53e798e1a5f`
for all three after erasing only internal generated-list unit spellings
`.Exprs` and `.Stmts`. Those spellings are accepted in rule syntax but are
represented by empty surface lists in `.mpy`; no operation, binding, or value
is changed. See `04-program-pinning.log`. The two preliminary parser attempts
are preserved and document exactly why that inert normalization was needed.

Body sensitivity is genuine. Reviewer mutation
`04-solution-body-mutated.mpy` changes the executed constructor
`Assign(Name("candidate"), Int(2))` to `Int(3)`. Fresh `krun` leaves that
mutated module stuck with an empty result because the exact lowering no longer
matches (`04-body-mutation-krun.log`). The corresponding mutated entry claim
in `04-spec-body-mutation.k` fails with `WarnStuckClaimState` and exit 1
(`04-body-mutation-kprove.log`). This changes the program term in the theorem,
not merely an external Python file.

Satisfiable witnesses are recorded in
`/audit-output/evidence/04-satisfying-witnesses.txt`:

- trial: `C=4, D=2, B=true, N=5, K=.K`;
- scan: `C=2, N=5, K=.K`;
- entry: `N=5`, exact program, empty result; and
- entry boundary: `N=0`.

For `N=5`, `primesBelow(5)` reduces to
`cons(2,cons(3,nil))`; both Python implementations return `[2,3]`, and fresh K
execution returns the same sequence. For `N=0`, all three return empty.

The formal domain is all unbounded K integers satisfying `N >= 0`, exactly the
source contract. It is not a finite-size proof, example proof, or bounded
unrolling.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
`/audit-output/evidence/05-rule-inventory.md`; the source-derived declaration
and rule index is `05-source-inventory.log`. The original candidate has exactly
three K sources and no hidden helper K file.

Inventory totals:

- syntax for `Module`, generated statement/expression lists, five used
  statement forms, six used expression forms, `CmpOp`, `PList`, and four
  internal control states;
- one three-cell configuration;
- five visible function symbols (`chooseCons`, `noFactor`, `isPrime`,
  `primesFrom`, `primesBelow`), all marked `[function,total]`;
- ten semantic rules and eight verification equations;
- three reachability claims; and
- no priority, simplification, `owise`, anywhere, fresh, opaque, or
  `[functional]` declaration.

Every `solution.mpy` constructor is declared and occurs inside the exact
whole-program match. The material effects map one-for-one:

- parameter `n` is read from `<n>` only after exact function/formal/body
  matching;
- initial candidate and flags become `scan(2,N)` and
  `trial(C,2,true,N)`;
- outer/inner guards become complementary integer guards;
- divisibility assignment and both increments are explicit transitions;
- forward append is equivalently represented by suffix recursion and ordered
  prepend; and
- return writes the sole observable result and preserves any continuation.

All reachable arithmetic uses unbounded integers. Remainder is used only with
`D >= 2`; guards do not overlap; list selection covers both Boolean values.
There is no source I/O, heap alias, mutation visible outside the returned list,
exception path, break, or external state to omit. Reversed allocation order is
unobservable and preserves the exact returned sequence.

Verification equations are disjoint and terminating on all theorem uses.
`noFactor(C,2)` is the standard primality characterization for `C >= 2`, since
every composite has a divisor at most its square root. `primesFrom` enumerates
the interval recursively and `primesBelow` starts it at two. No semantic rule
mentions those specification functions; conversely no verification equation
rewrites a program/control term. Thus the proof does not smuggle the task answer
into execution or replace a program-derived value with an unconstrained oracle.

Two narrow gaps remain:

- `[total] noFactor` is not equation-total on the entire declared sorts:
  `noFactor(0,0)` reaches a remainder-by-zero hole.
- `[total] primesFrom` is not equation-total when `C < N` and `C < 2`.

Every proof occurrence has respectively `C,D >= 2` or `C >= 2`, recursion
preserves those invariants, and the entry path starts at two. There is therefore
no concrete or symbolic intended-domain false conclusion witness. Under the
benchmark's decision rule these are over-broad declaration/evidence gaps, not
unsound-rule findings.

The S3 lowering is program-specific rather than compositional. It bypasses
individual AST small steps, but it does not bypass the property-bearing
computation: `scan`/`trial` still perform every loop test, remainder branch,
flag update, increment, ordered accumulation, and return, and C1/C2 prove that
state machine against independently defined result functions. Static mapping,
constructor identity, body mutation, and concrete comparisons find no false
case. The absence of a separate bridge-free Python-semantics theorem is the
principal reason for `CONCERNS`.

## 6. Fresh non-vacuity test

There was no candidate vacuity artifact to trust. I created
`/audit-output/evidence/06-spec-vacuity-audit.k` from the scratch spec, renamed
its module/entry label, and changed only the result obligation:

```text
<result> .K => cons(0, primesBelow(N)) </result>
```

This is false for the satisfying input `N=0`: actual and specified original
results are `nil`, while the mutation demands `cons(0,nil)`.

The mutation first passes `kprove --dry-run` with exit zero, so it builds and
parses successfully (`06-vacuity-dry-run.log`). The actual proof with both
required helper claims exits 1 and emits `WarnStuckClaimState`. Its residual
shows completed computation with actual
`primesFrom(2,N)` and the failed implication/equality against
`cons(0,primesFrom(2,N))` (`06-vacuity-proof.log`). This is the expected unmet
result constraint, not a parse error, timeout, missing import, unreachable
mutation, or unrelated crash. The proof is non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

The successful K proof establishes:

> Under the candidate's generated `MPY` semantics, for every integer `N >= 0`,
> executing the exact constructor tree regenerated from the submitted
> `solution.py`, from the initial `<n>N</n>` and empty result cell, reaches
> empty computation with result `primesFrom(2,N)`. That recursively contains
> exactly those integers in `[2,N)` for which no divisor from two through the
> square-root bound exists, in ascending order.

The complete ledger is
`/audit-output/evidence/07-trust-ledger.md`. Trusted/assumed boundaries are:

1. K 7.1.293 and built-in integer/Boolean/remainder, sequencing,
   configuration, function, and reachability machinery.
2. The launcher-trusted CPython-AST translator; exact regeneration is checked.
3. The exact whole-program source-to-`scan`/`trial` lowering. This is
   result-bearing only through a fully visible state machine and is audited as
   faithful, but its connection is informal rather than a separate universal
   theorem.
4. Ordinary mathematics connecting the visible `noFactor` equations to
   primality.
5. The structural `nil`/`cons` representation of Python integer lists.
6. Finite differential evidence: 104 Python/canonical and 16
   K/Python/canonical cases, used only to support the respective bridges.
7. Off-domain equation coverage gaps for two `[total]` annotations, which no
   theorem execution reaches.

There is no opaque or fresh result symbol, empirical oracle inside the
postcondition, trusted task-answer axiom, or hidden semantic helper. Termination
is not claimed by this partial-correctness audit, though the concrete loops
plainly advance toward finite bounds.

Gate summary:

- Real-program soundness and non-vacuity: pass.
- Intent/domain adequacy: pass; all non-negative integers are covered.
- Trust/evidence auditability: pass with the stated non-fatal generated-semantics
  and totality limitations.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
