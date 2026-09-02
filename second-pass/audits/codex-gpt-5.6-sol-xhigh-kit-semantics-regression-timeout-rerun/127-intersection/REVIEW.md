# Independent adversarial audit: 127-intersection

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
translated program under the supplied MPY semantics. Fresh reconstruction
closed the loop circularity and both result claims, the proof executes a KAST-
identical copy of `solution.mpy`, and a fresh false-result mutation was rejected
for the expected semantic reason.

The status is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
human-facing primality bridge is not a separate machine-checked K theorem.
`scanPrime` is equationally determined by a bounded induction, but its
fold-oriented rules do not normalize important ground terms such as
`scanPrime(5,2,true)`. The mathematical induction is sound and finite testing
supports it, so this is an evidentiary limitation, not a witnessed
false rule.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. I recursively compared
it with `/candidate/reference-semantics` using `diff -r --no-dereference`.
There are no missing, extra, changed, mistyped, or symlinked entries in either
tree. The candidate `prompt.py` and `py2mpy.py` are regular files and byte-
identical to the trusted versions:

- prompt SHA-256:
  `aaebd5df799992f92d5d1e023101fa08b8a199d71be54536511e5ed071d5db1c`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The complete type, symlink, hash, and recursive-diff checks are in
`evidence/stage1-integrity.sh` and `evidence/stage1-integrity.log`. All required
candidate artifacts are regular files. The structured trace is present at
`/candidate/codex-trace/2026/07/23/rollout-2026-07-23T00-27-59-019f8d71-e4b4-78d0-b0a3-eaeee6a604a8.jsonl`
and contains 592 valid JSONL records with no malformed record.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as candidate claims. They
claim `VALIDATED`, aggregate `#Top`, 23,409 differential cases, and successful
negative probes. A bounded, digest-pinned extraction is in
`evidence/untrusted-claims-summary.log`; none of those claims was used as an
audit result.

Only source files were copied to `/tmp/audit-work/scratch`. Candidate
`runtime-kompiled/`, `verification-kompiled/`, `__pycache__/`, logs, and caches
were not copied or used. `evidence/source-artifact-manifest.log` records matching
candidate/scratch hashes for `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k`.

Integrity result: PASS. No infrastructure contradiction or candidate integrity
failure was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `intersection(interval1, interval2)` for two closed
integer intervals with `start <= end`. Let

`N = min(end1,end2) - max(start1,start2)`.

It must return `"YES"` exactly when `N` is prime, and `"NO"` otherwise,
including disjoint or endpoint-only intersections. The problem's notion of
closed-interval length is the endpoint difference, as its `(2,3)` example
explicitly treats length as 1 rather than cardinality 2.

The trusted canonical implementation computes the same `N`, first requires
`N > 0`, and applies trial division. Its docstring's third sample differs from
the mounted prompt's third sample, but the executable canonical function
returns the prompt-required answer on both; this prose discrepancy does not
change the oracle behavior.

### Submitted program

`/candidate/solution.py` selects the maximum left endpoint and minimum right
endpoint with explicit branches, sets `prime = (N > 1)`, scans every divisor
from 2 through `N-1`, and returns `"YES"` iff the flag remains true. It does not
break early after finding a divisor, but the flag is never reset, so this is
extensionally correct over all well-formed integer interval pairs.

Using only the trusted translator copied from `/reference`, I regenerated
`solution.mpy`. It is byte-identical to the submission, with SHA-256
`d4b037d992c4f7a790b11a3b47c960e6b01076996d082ab886f6db2c20d57c6d`.
The exact command and exit 0 are in
`evidence/stage2-translation-identity.log`.

`evidence/differential_test.py` imports the trusted canonical entry point from
`/reference/canonical.py` and the scratch candidate entry point. It checks:

- 19 named prompt, empty-intersection, endpoint, length, nesting, and every
  endpoint-branch boundary case;
- every ordered pair of the 153 well-formed intervals with endpoints in
  `[-8,8]`, totaling 23,409 cases;
- 4,000 deterministic generated cases around large positive and negative
  integer bases.

All 27,428 cases agreed, and all explicit expected answers passed. The complete
inputs and both results are preserved in
`evidence/differential-inputs.jsonl` (SHA-256
`359b2ff4b790fd6bf5b4c1b10566b9ff5bb54803dfd3f6207b3e9cdf548ad305`);
the command and exit 0 are in `evidence/differential-test.log`.

Program-fidelity result: PASS.

## 3. Clean proof reconstruction

The live K toolchain is K v7.1.293, recorded in
`evidence/kompile-version.log` and `evidence/kprove-version.log`.

From the isolated source copy I freshly built:

1. the LLVM concrete definition from
   `reference-semantics/semantics.k`, using `MPY-KRUN` and `MPY-SYNTAX`;
2. the Haskell proof definition from `verification.k`, using `VERIFICATION`
   and `MPY-SYNTAX`.

Both `kompile` commands exited 0. Exact commands and bounded outputs are in
`evidence/kompile-runtime.log` and
`evidence/kompile-verification.log`. Warnings concern unused variables and
known non-exhaustive total functions. The only warned function on this
program's path is `valSeqAt`; its missing empty/out-of-bounds cases are
unreachable because both claims supply exact two-element tuples and use only
indices 0 and 1. Other warned functions are in unused features.

`evidence/concrete_harness.py` contains a Python-AST-identical copy of the
submitted function plus seven normal/boundary assertions. Trusted translation
followed by the freshly built LLVM semantics reached `.K`, `NoExc`, and exit
code 0; see `evidence/krun-concrete-harness.log`.

I ran the positive claims separately while including their required
circularity:

| Target | Selection | Result |
|---|---|---|
| loop | `SPEC.divisor-loop` | exit 0, `#Top` |
| prime entry | `SPEC.divisor-loop,SPEC.intersection-prime` | exit 0, `#Top` |
| non-prime entry | `SPEC.divisor-loop,SPEC.intersection-not-prime` | exit 0, `#Top` |
| candidate aggregate command | all of `SPEC` | exit 0, `#Top` |

The corresponding records are
`evidence/kprove-divisor-loop.log`,
`evidence/kprove-intersection-prime-with-loop.log`,
`evidence/kprove-intersection-not-prime-with-loop.log`, and
`evidence/kprove-all-positive.log`.

For transparency, selecting `intersection-prime` alone excludes its loop
circularity and fails at the real loop
(`evidence/kprove-intersection-prime.log`). That is a dependency-selection
diagnostic, not a target failure: the loop claim was independently proved, and
the target plus its required helper closes.

Clean-reconstruction result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.divisor-loop` requires a complete function-frame state with divisor
`I >= 2`. It executes the exact submitted `#while`, preserves the arbitrary
continuation and stack, changes the divisor to `maxInt(I,N)`, and changes the
flag from `P` to `scanPrime(N,I,P)`. All other local bindings and all other
configuration cells are preserved.

`SPEC.intersection-prime` requires exact two-integer tuples `(A,B)` and `(C,D)`,
well-formedness `A <= B` and `C <= D`, and a true `scanPrime` summary for the
computed overlap length. It returns the exact MPY string value `"YES"`.

`SPEC.intersection-not-prime` has the same real input domain and complementary
false-summary precondition. It returns the exact MPY string value `"NO"`.
Because the summary has sort `Bool`, these entry branches partition the formal
well-formed domain.

### Program identity and result constraint

`evidence/structural_identity.py` parses both `solution.mpy` and the
`intersectionClosure` rule with the freshly built K parser. Parameters and the
entire statement-body KAST are equal, and the closure captures module scope 0.
It also checks that the concrete harness function is Python-AST-identical to
`solution.py`. The command exits 0 with `PROGRAM_PINNING=PASS` in
`evidence/structural-identity.log`.

The entry `<k>` cells therefore perform actual lookup, argument evaluation,
binding, every statement, loop execution through the proved circularity,
return, frame pop, and caller restoration. `intersectionClosure` only expands
to an exact closure value; it is not an operational bridge. The postconditions
are concrete strings, not free variables, tautologies, or one-way
implications.

`evidence/adequacy-witnesses.log` supplies a satisfying state for each claim:

- loop: `N=4, I=2, P=true`, realized by `(0,4),(0,4)`, ending at divisor 4
  with flag false;
- prime entry: `(-3,-1),(-5,5)`, overlap length 2, both Python functions and
  the formal postcondition return `"YES"`;
- non-prime entry: `(0,4),(0,4)`, overlap length 4, both Python functions and
  the formal postcondition return `"NO"`.

Adequacy/program-pinning result: PASS for the formal execution theorem, with
the summary-to-primality concern detailed in Stages 5 and 7.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventories every local configuration, syntax
declaration, function/total declaration, opaque `no-evaluators` symbol,
context, priority rule, ordinary rule, simplification, and claim in the
supplied semantics, `verification.k`, and `spec.k`. Each of the 942 rows in
`evidence/rule-inventory.tsv` contains its file, line, normalized declaration,
attributes, source role, decision class, and declaration digest. The aggregate
is SHA-256
`6d0a77ed99cd4af2b6b85979890ea7cbb55d4e0a3a6779a696e4a5c1f0daf7cc`.

The inventory contains:

- 1 configuration, 81 ordinary syntax declarations, 39 function
  declarations, 88 non-opaque total-function declarations, and 22 opaque
  total symbols;
- 5 contexts, 656 ordinary rules, 45 priority rules, and 2 simplification
  rules;
- 3 reachability claims.

Counts by every source file are in
`evidence/rule-inventory-summary.txt`. Top-level `semantics.k` is an assembly
module with imports but no local syntax or rule, so it contributes zero
declaration rows. All 22 opaque supplied symbols are confined to float,
sorting, and MD5 support and are unreachable from `solution.mpy`.

For the fixed supplied tree, each row is classified as defining the selected,
integrity-verified baseline. Unused constructor-specific rules cannot match
this program. The complete used-path map and its evaluation/control judgments
are in `evidence/used-construct-map.tsv`.

### Used supplied-semantics path

The submitted program uses `Module`, `FuncDef`, `Call`, exact tuple values,
`Name`, in-bounds `Subscript` at indices 0 and 1, `Int`, `Bool`, ASCII `Str`,
`Assign`, `If`, `BinOp` for `+`, `-`, `%`, integer comparisons, `While`, and
`Return`.

The inspected rules establish:

- configuration load installs the real closure in module scope 0;
- callee lookup precedes left-to-right argument evaluation;
- the closure call allocates one frame, binds both exact tuple values, and
  saves the caller continuation/environment;
- subscript evaluates object before index, and both accesses reduce by the
  in-bounds `valSeqAt` rules;
- strictness/contexts preserve Python evaluation order for assignments,
  branches, arithmetic, comparisons, and returns;
- assignments update only the current function scope;
- `%` uses Python-style `pyMod`; every executed divisor is at least 2, so no
  zero-denominator or negative-denominator discrepancy is reachable;
- the while condition is re-evaluated each iteration, the body sequences the
  flag update before divisor increment, and false exits preserve the suffix;
- return sets `retV`, discards the remaining callee body, and restores every
  caller cell from the saved frame;
- `"YES"` and `"NO"` are completely covered ASCII literals.

The exact two-element input restriction prevents the supplied semantics'
out-of-bounds underspecification from being reached. There is no allocation,
external state, exception, or opaque supplied primitive on the theorem path.

### Proof-local declarations and rules

There are exactly 11 proof-local inventory entries (K0929-K0939). Detailed
per-entry classifications are in
`evidence/proof-local-judgments.tsv`.

- `intersectionClosure` is an exact definitional literal. The independent KAST
  comparison proves complete body, parameter, and defining-scope identity.
- `overlapLength` has one unconditional, overlap-free equation for
  `min(B,D)-max(A,C)`.
- `maxInt(I+1,N) = maxInt(I,N)` under `I<N` is valid because integer
  discreteness gives `I+1 <= N`.
- The four direct `scanPrime` cases are mutually covering with the fold,
  modulo their intentional equational orientation: false is absorbing;
  `I<2<I..N` totalizes the unused off-domain region to false; `I>=N` returns
  the accumulated flag; and an in-range divisor returns false.
- The simplification
  `scanPrime(N,I+1,P) = scanPrime(N,I,P)` is true exactly under its guard
  `2 <= I < N` and `I` non-dividing. It folds one actual non-divisor loop step
  into the summary and strictly lowers its syntactic second argument.

Overlaps agree mathematically. For example, at `N=9`, the divisor equation
gives `scanPrime(9,3,true)=false`, while the non-divisor fold at 2 gives
`scanPrime(9,3,true)=scanPrime(9,2,true)`; together they determine the entry
summary as false. No conflicting Boolean conclusion follows.

The orientation is deliberately useful to the loop proof but is not a complete
ground evaluator. A direct ground claim
`scanPrime(5,2,true) => true` gets a meaningful stuck condition rather than
`#Top` (`evidence/scanprime-ground-prime-five.log`), whereas a directly
reducible composite case closes
(`evidence/scanprime-ground-composite.log`). The two critical-pair probes are
in `evidence/scanprime-critical-pair-divisor.log` and
`evidence/scanprime-critical-pair-fold.log`.

I also tested a putative false conclusion for concrete length 9. With the added
assumption `scanPrime(9,2,true)`, direct fixed execution returns `"NO"` and the
claim fails; adding the loop summary lets the conditional `"YES"` claim close.
Those records are
`evidence/composite-summary-without-loop.log` and
`evidence/composite-summary-with-loop.log`. This is not an unsound-rule
witness: the added true-summary assumption is inconsistent with the two
equations above, so it does not exhibit a satisfying formal state. It does
show why backend normalization alone is insufficient evidence for the
summary-to-primality bridge.

A reviewer-authored executable interpretation of all summary equations checked
38,628 guarded cases and the primality bridge for 1,011 lengths with no
mismatch (`evidence/summary-equation-tests.log`). This is finite supporting
evidence, not the universal justification. The universal justification is the
ordinary bounded induction: repeatedly apply the fold for a non-divisor;
encountering a divisor yields false, while reaching `I>=N` yields the initial
flag `N>1`.

There are no proof-local priority rules, operational bridge rules, or opaque
`no-evaluators` primitives. The loop claim is an auxiliary reachability
circularity, not an installed rewrite. It matches the real loop, preserves its
arbitrary continuation and stack, and frames every unchanged cell. The body
contains no abrupt control, allocation, output, or exception effect that could
make that framing too broad.

Static-soundness result: PASS. No rule is labeled unsound because no satisfying
concrete or symbolic false-conclusion witness exists. The non-normalizing
summary orientation is retained as the narrower evidence gap.

## 6. Fresh non-vacuity test

I did not reuse `/candidate/spec-vacuity.k`. The fresh mutation
`evidence/spec-auditor-vacuity.k` fixes both intervals to `(0,2)`, a satisfying
well-formed input with prime overlap length 2, and changes the required result
from `"YES"` to the false `"NO"`.

The mutation parsed and executed against the fresh proof definition. `kprove`
exited 1 with `WarnStuckClaimState`; the residual `<k>` contains the actual
`"YES"` code sequence while the target is `"NO"`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. The exact command and bounded residual are in
`evidence/kprove-auditor-vacuity.log`.

Non-vacuity result: PASS.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY definition and proof-local equations, the machine-
checked reachability proof establishes:

1. partial correctness of the exact submitted divisor loop with post-state
   divisor `maxInt(I,N)` and flag `scanPrime(N,I,P)`;
2. for every exact well-formed two-integer interval pair in the true-summary
   branch, actual execution of the submitted function returns exact `"YES"`;
3. for the complementary branch, actual execution returns exact `"NO"`;
4. complete preservation/restoration of all framed configuration cells shown
   in the claims.

It does not prove termination. The source loop plainly terminates for concrete
integer inputs because its divisor starts at 2 and increases toward fixed `N`,
but that liveness fact is outside these reachability claims.

### Trust and assumption ledger

| Boundary | Effect on result | Assessment |
|---|---|---|
| K v7.1.293, Haskell backend, SMT/reachability implementation | Executes symbolic rules and checks implications | Necessary low-level trust; fresh positive and negative runs reduce accidental misuse but do not prove the toolchain |
| Integrity-verified supplied MPY semantics | Defines values, scopes, evaluation order, loop/call/return behavior | Authorized fixed semantics; used path audited and concretely exercised |
| Trusted `py2mpy.py` | Bridges `solution.py` to MPY syntax | Acceptable trusted input; byte regeneration and KAST pinning verify the actual artifact |
| K built-in Int/Bool/String/Map/List operations | Arithmetic, conditions, strings, and state maps | Acceptable primitive boundary on the used mathematical domain |
| Proof-local `scanPrime` equations | Names the loop's mathematical result and controls entry-claim partition | Sound by bounded induction and connected to exact loop execution; concern because equivalence to primality is not a separate machine-checked K theorem and ground normalization is incomplete |
| `overlapLength` and `maxInt` equations | Endpoint result and invariant arithmetic | Direct ordinary mathematics; unconditional/guarded rules audited |
| 22 supplied opaque symbols | Float/sort/MD5 features | Unused and non-dependent |
| Differential and equation tests | Support Python/canonical/intent alignment | Finite empirical evidence only; not a substitute for K reachability or universal induction |

The intended-language bridge is otherwise tight: K and Python both use
unbounded integers for the used operations; tuple indices are in bounds;
modulo has a positive divisor; output strings are ASCII; and no external state
or unsupported exception behavior is reachable.

### Decision

Fresh reconstruction, exact-body sensitivity, full-state claims, sound
proof-local equations, and the fresh discriminating mutation make the proof
legitimate. The remaining limitation is specifically the informal
summary-to-primality induction and incomplete ground normalization evidence.
Under the requested decision boundary, that is `CONCERNS / LEGIT`, not a
failure and not an unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
