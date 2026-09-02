# Independent adversarial audit — 94-skjkasdkd

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program over the full finite-list-of-integers
source domain. The submitted program is mechanically pinned to the theorem,
all five claims reconstruct from source and close, and a fresh false-result
mutation is rejected for the expected logical reason.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
non-fatal limitations:

1. `verification.k:307-339` is an operational bridge over function entry. Its
   transition is exact for the immutable submitted body by rule-by-rule
   composition, and bridge-free ground executions agree, but the candidate
   supplies no bridge-free universal K connection theorem. An independent
   universal attempt was bounded at 120 seconds and timed out; that timeout is
   only an evidence limitation.
2. `trialPrime` and `trialDivisor` are declared `[total]` more broadly than
   their Python-like modulo behavior supports at divisor zero. All theorem
   paths maintain divisor at least 2, so this cannot affect any intended list
   input, but the declarations are unnecessarily global.
3. The bridge from the executable trial-division/digit definitions to the
   human words “prime” and “sum of digits” is ordinary mathematical reasoning,
   not a separate K theorem. Differential testing supports it only finitely.

No candidate rule was labeled materially unsound without a false-conclusion
witness. I found no false conclusion enabled by the immutable theory on an
intended integer-list input.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- problem `94-skjkasdkd`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. The infrastructure does not contradict the rendered semantics
condition.

I read and inspected every record required by `legacy-selected-stage1`:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the complete JSONL trace under
  `/generation-evidence/codex-trace/`;
- `/generation-evidence/usage.json`, which is present.

Historical runtime metrics are not part of this imported legacy record and
were not reconstructed.

All required mounts and records are real readable files/directories. No linked
or unsupported entry occurs anywhere in the candidate supplied-semantics tree,
trusted supplied-semantics tree, or generation-evidence tree.

### Campaign and hashes

The JSON object in `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` object in `/audit-input.json`. Its independently computed
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

Independent regular-file hashes match the launcher values, including:

- canonical:
  `d1dd5909bcdd2600d7171948865387fc85a1592dbb57baae6e7dd90e93b22daa`;
- prompt:
  `1c6ca165f1b5548225ce755ffb9fe188813105f3eac8cfb3f515326db7f25812`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- invocation:
  `1a7d310baedad973b3ec839b23eb7c98f0bcd8337b33188161caecc3f6055702`;
- metrics:
  `abf639925708b7f2dec44a8fd19b608efde591455088b6d33ffa344baff94a9a`;
- generation log:
  `863c1fc30bab83bc5bf233c592b8fb49086c759a9efc138a3924df4781799584`;
- trace JSONL:
  `1ce3f42c6bbc2c1516b7e336158235d3a7c10cde89eb2f3499e1473de93e274b`.

The independently computed pipeline tree digest of the candidate is
`721e5534cf6255f7b877a3fbfd636c79b6f3598b83e9614a3b8ffb2a182b19ff`,
matching the retained workspace hash in the generation records. The candidate
and trusted supplied-semantics trees both have pipeline digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
The generation trace tree digest is
`36f06ce3563bf607a7e263282ca482b2b6d8c31ea1d8127c070575d34f0cc259`,
matching the usage record. The launcher also records legacy/package tree
digests produced by other normalization algorithms; I did not substitute one
algorithm for another and instead performed the byte-level comparisons below.

### Trusted-input comparisons

- `cmp /candidate/prompt.py /reference/prompt.py` exited 0.
- `cmp /candidate/py2mpy.py /reference/py2mpy.py` exited 0.
- Recursive, no-dereference comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` exited 0.
- The tree comparison found no missing, additional, changed, mistyped, or
  symlinked entry.

The untrusted generation trace contains 781 parsed JSONL events, including 65
shell calls, 29 patch calls, and the claimed final success. I iterated over the
entire structured trace and separately inspected the 100,976-line generation
output. These records were treated only as historical claims.

Evidence:

- `evidence/01-integrity.sh`
- `evidence/01-integrity.log`
- `evidence/trace_summary.py`
- `evidence/generation-trace-summary.log`
- `evidence/generation-output-inspection.log`

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` says: for a list of integers, find the largest prime
value and return the sum of its decimal digits. It gives six examples and
states no size bound, non-emptiness requirement, positivity restriction, or
guarantee that a prime is present. The intended domain is therefore every
finite Python list whose elements are integers. With no prime, the natural
result is 0.

The candidate implements exactly that contract:

1. initialize `largest` to 0;
2. scan every element;
3. for a value larger than the current candidate, perform trial division from
   2 while `divisor * divisor <= number`;
4. retain it iff it is at least 2 and no divisor is found;
5. accumulate decimal digits of the largest retained prime.

This is a different implementation from the trusted canonical code, which is
allowed.

### Trusted regeneration

In the scratch copy I ran:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both commands exited 0. The submitted and regenerated constructor files both
hash to
`6adc49642fc72665394f0abc7c9860d03b3df6e219924c30419c42d9a7ac5486`.
Thus `solution.mpy` is exactly the trusted translation of `solution.py`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and generated entry point. Its oracle uses `math.isqrt` and an
independent divisor loop; it does not reuse the proof equations.

The test covered:

- all six documented examples;
- empty and all-nonpositive lists;
- 0, 1, 2, 3, and 4 boundaries;
- true and false `number > largest` paths;
- the `number >= 2` boundary;
- divisible and non-divisible trial-loop paths;
- repeated/equal values;
- no-prime inputs;
- multi-digit primes;
- every list of length 0 through 3 over `[-3, 15]`;
- 3,000 fixed-seed random lists with 0 through 25 elements in
  `[-100, 100000]`.

Total generated-program cases: 10,266. Generated-versus-independent-oracle
mismatches: 0.

The trusted canonical has a real source-contract defect: its `isPrime(1)`
returns true. Consequently it returns 1 for `[1]`, `[0,1]`, and sampled lists
that contain 1 but no actual prime. There were 495 such
canonical-versus-oracle mismatches. The generated candidate returns 0 and
therefore agrees with the natural-language contract. This divergence is
material and recorded, but it is not evidence that the candidate is wrong.

Evidence:

- `evidence/02-regenerate.sh`
- `evidence/02-regenerate.log`
- `evidence/differential_test.py`
- `evidence/02-differential.log`

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. The supplied semantics came from the trusted
reference mount. No candidate-built definition, cache, `spec.json`, prior log,
or prior `#Top` was used.

Installed tools independently reported K version `v7.1.293`.

### Concrete definition

The reviewer concrete harness contains the exact function AST from
`solution.py`; an independent AST comparison exited 0. The harness includes
empty, 1, 2, composite-only, negative/mixed, multi-prime, and prompt-derived
cases.

Fresh commands:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
krun concrete-audit.mpy --definition reviewer-runtime-kompiled
```

Both exited 0. The final concrete configuration has `.K`, `NoExc`, empty
stack, and exit code 0.

### Proof definition and positive claims

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition reviewer-verification-kompiled -I .
```

It exited 0. The expected fixed-semantics warnings concern unused variables in
`str.k`; the LLVM definition additionally warns about non-exhaustive functions
for constructs unused by this program. No build failed.

Every positive claim was then independently rerun in dependency order:

| Target | Dependencies admitted only after their independent success | Exit | Output |
|---|---|---:|---|
| `SPEC.prime-loop` | none | 0 | `#Top` |
| `SPEC.digit-loop` | none | 0 | `#Top` |
| `SPEC.scan-loop` | proven prime/digit claims | 0 | `#Top` |
| `SPEC.entry-prefix` | proven scan/prime/digit claims | 0 | `#Top` |
| `SPEC.main-correct` | proven entry/scan/prime/digit claims | 0 | `#Top` |

The exact commands, output, and statuses are preserved in:

- `evidence/03-reconstruct.sh`
- `evidence/03-reconstruct-summary.log`
- `evidence/03-kompile-llvm.log`
- `evidence/03-krun-concrete.log`
- `evidence/03-kompile-haskell.log`
- `evidence/03-kprove-prime-loop.log`
- `evidence/03-kprove-digit-loop.log`
- `evidence/03-kprove-scan-loop.log`
- `evidence/03-kprove-entry-prefix.log`
- `evidence/03-kprove-main-correct.log`

Clean reconstruction therefore passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`prime-loop`

: Precondition: current divisor is at least 2; if `prime` is true then the
  number is at least 2; the named locals are distinct ordinary-frame entries.
  Postcondition: the real `#while` trial loop consumes, preserving `number`,
  setting `prime` to `trialPrime(N,D,B)`, and setting `divisor` to
  `trialDivisor(N,D,B)`. The arbitrary continuation `K` is preserved.

`digit-loop`

: Precondition: `largest` is nonnegative and the named locals are distinct
  ordinary-frame entries. Postcondition: the real digit loop consumes,
  setting `largest` to 0 and `digit_total` to `digitAcc(N,A)`, while preserving
  continuation and unrelated state.

`scan-loop`

: Precondition: the actual list-loop head contains an arbitrary unbounded
  `IntList`, current `largest >= 0`, the complete fixed suffix
  (digit loop, return, and `#endcall`), and a realizable function frame.
  Postcondition: the function returns
  `digitSum(largestPrime(IS,CUR))`, pops the exact frame, restores caller
  environment and allocation cursor, and resumes the saved continuation.

`entry-prefix`

: Precondition: direct application of the exact closure/body to one
  integer-list value, caller environment 0, empty stack, fresh scope location
  1, `noRet`, and no existing scope entry 1. Postcondition: the exact result
  `digitSum(largestPrime(IS,0))`, with caller cells restored.

`main-correct`

: Precondition: the full supplied initial configuration and an arbitrary
  recursive `IntList`. There is no size bound. Postcondition: after loading
  the exact submitted function and calling it, `<k>` contains exactly
  `digitSum(largestPrime(IS,0))`; the module binding is the exact submitted
  closure and every other observable cell has the specified final value.

The RHS result is not free, existential, tautological, or merely implied. It
is a concrete recursive function of the entire symbolic input.

### Constructor-level program identity

I parsed both:

1. the exact regenerated/submitted `solution.mpy`; and
2. the `solutionModule` term used by `main-correct`;

under the fresh proof definition with macro expansion enabled and KORE output.
The two expanded KORE terms are byte-identical, length 9,714, with hash
`60ffc8617a4edd1e03d18baffd741d840d2e23fafd5e8ce381cfb7731a97a5d5`.

This proves mechanical constructor-level identity of the function name,
parameter, binding, and complete body. No source-to-proof regeneration
assumption is used for this immutable artifact.

Evidence: `evidence/04-kast-compare.sh` and
`evidence/04-kast-compare.log`.

### Satisfiable preconditions and concrete substitution

`evidence/04-precondition-witnesses.md` gives a complete satisfying state for
each claim. A single consistent end-to-end witness is input `[2]`:

- candidate Python: 2;
- trusted canonical Python: 2;
- independent oracle: 2;
- `largestPrime(intCons(2,.IntList),0)`: 2;
- `digitSum(2)`: 2.

The loop witnesses choose `N=2`, `D=2`, `B=true`, digit accumulator 0,
fresh callee location 1, empty rests, and an ordinary caller scope. Every
precondition evaluates true.

### Body sensitivity

I performed two distinct probes.

First, I changed only the actual program term used by `solutionModule` to
`return 1`, leaving the proof summaries and operational bridge unchanged.
The changed submitted `.mpy` and changed claim term were mechanically pinned
to one another, and their KORE hash differs from the immutable program. On
input `[2]`, fixed execution ends at 1; the claim demanding 2 fails with
`WarnStuckClaimState`. The full end-to-end theorem also fails. This is the
required body-sensitivity result.

Evidence:

- `evidence/04-program-sensitivity.sh`
- `evidence/04-program-sensitivity-summary.log`
- `evidence/04-program-mut-kast-pin.log`
- `evidence/04-program-mut-ground.log`
- `evidence/04-program-mut-main.log`

Second, as an operational-bridge stress test, I changed the shared
`#functionBody` macro itself. That also changes the bridge's LHS, so it changes
the proof extension as well as the program. In that coupled theory, the old
RHS summary can still prove result 2 even though fixed execution of the
changed body returns 1. This is not a counterexample to the immutable expanded
rule: it changes that rule. It is, however, strong evidence that a separately
machine-checked connection theorem would improve maintenance safety.

Evidence:

- `evidence/04-body-sensitivity.sh`
- `evidence/04-body-sensitivity-summary.log`
- `evidence/04-body-mut-kast-pin.log`
- `evidence/04-body-mut-ground-with-bridge.log`
- `evidence/04-body-mut-ground-without-bridge.log`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I generated and independently count-checked an exhaustive lexical inventory
of every local K sentence in:

- `reference-semantics/semantics.k`;
- all 23 helper files under `reference-semantics/semantics/`;
- `verification.k`;
- `spec.k`.

Counts:

- 26 files;
- 1,160 local sentences;
- 740 ordinary/macro/simplification rules;
- 242 syntax declarations;
- 5 contexts;
- 1 configuration;
- 5 claims;
- 25 file `requires`, 88 imports, and all module boundaries.

Every record includes source, exact line span, complete text, attributes,
normalized hash, decision, and rationale. Independent `rg` counts match the
inventory for all 740 rules, 242 syntax declarations, 5 contexts, and 5
claims.

Evidence:

- `evidence/rule_inventory.py`
- `evidence/05-rule-inventory.json`
- `evidence/05-rule-inventory.md`
- `evidence/05-rule-inventory.log`
- `evidence/05-inventory-validation.log`

### Supplied semantics

All 1,087 supplied-semantics sentence records are byte-identical to the
trusted tree. Under `SUPPLIED_SEMANTICS`, this tree defines the fixed semantics
level. Each record is classified in the inventory as:

- material fixed module;
- fixed but unreachable from this program/proof; or
- concrete-only (`MPY-CONCRETE`, absent from the proof definition).

Unused float, string, dict, set, tuple, comprehension, range, sorting, and
method operations cannot contribute to claim closure. Material syntax and
rules were inspected for configuration, loading, closure binding, call/return,
name lookup, assignment, evaluation order, integer arithmetic, list
iteration, conditionals, and loops.

The exact map from every submitted constructor to its declaration and
operational rules is in `evidence/05-used-construct-map.md`.

Key material facts:

- K `Int` is unbounded, matching Python integers for the used operations.
- `%` and `//` use Python-style floor arithmetic; every reachable divisor is
  positive.
- `strict`, `seqstrict`, and comparison contexts preserve Python evaluation
  order.
- the function does not mutate or allocate its input;
- fixed call/pop rules preserve heap, restore caller environment, remove the
  callee scope, and reset `scopeLoc`;
- `MPY-CONCRETE` is not imported by `VERIFICATION`.

### Candidate proof extensions

The inventory makes an individual decision for every candidate rule. The
extension groups are:

1. **Two Map simplifications (`verification.k:7-12`).** Map deletion and
   insertion are guarded by key absence and are true Map normalizations.

2. **Twenty fixed-rule specializations (`verification.k:18-176`).** These
   cover name lookup, assignment, literal cooling, augmented assignment,
   target binding, comparison, `If`, `Return`, `For`, exact function binding,
   and one exact comparison assignment. Each guard pins a plain current frame,
   excludes closure-cell ambiguity where relevant, and performs the same
   value/control/state transition as the supplied rule sequence. Priorities
   select equivalent paths; they do not change results.

3. **Input representation (`verification.k:181-190`).** `IntList` is an
   unbounded recursive sort, not a fixed-size enumeration. `asVals` is an
   opaque proof-side representation only in the sense that it is not globally
   reduced to `vCons`; the two iterator rules completely expose its
   `.IntList` and `intCons` cases. The program only iterates the input, so no
   observable input behavior is unconstrained and no result oracle is
   introduced.

4. **Mathematical definitions (`verification.k:194-248`).**
   `trialPrime`/`trialDivisor` have disjoint reachable guards and advance the
   divisor; `largestPrime` structurally consumes the list; `digitAcc` strictly
   reduces every positive number by a factor of 10. `isPrime` and `digitSum`
   are transparent wrappers. The same symbols are not opaque values injected
   by an execution bridge.

5. **AST macros (`verification.k:251-302,341-343`).** These expand to the exact
   submitted constructors. Full-module equality is machine checked in Stage
   4.

6. **Entry operational bridge (`verification.k:307-339`).** Its complete match
   has:

   - the exact immutable closure body and exact one-list argument;
   - no continuation suffix (`CONT = .K`);
   - caller env 0;
   - empty stack;
   - fresh scope location 1;
   - an arbitrary scope map with location 1 absent.

   It changes exactly `<env>`, `<scopes>`, `<scopeLoc>`, and `<stack>`. It
   frames heap, heap cursor, return, exception, and exit cells, all of which
   the skipped fixed prefix also leaves unchanged. Its RHS is the direct
   composition of supplied call-frame allocation, one parameter binding, five
   literal assignments, and one-time evaluation of `Name("lst")` for `For`.
   It does not summarize a loop iteration or manufacture the final result.

   Removing only this bridge still proves fixed ground executions for:

   - `[1] -> 0`;
   - `[2] -> 2`;
   - `[13] -> 4`.

   Those three bridge-free K claims all exit 0 with `#Top`
   (`evidence/05-bridge-ground-summary.log`). They provide distinct observable
   outcomes but remain finite evidence. The audit-only universal entry theorem
   without the bridge reached the 120-second bound
   (`evidence/05-bridge-free-universal-entry.log`). This timeout is not treated
   as a false rule or candidate failure; it leaves the stated connection
   evidence limitation.

### Totality and overlap

On all theorem-reachable paths:

- trial divisor starts at 2;
- it only increments;
- modulo is therefore defined;
- the `D*D > N` and `D*D <= N` branches partition integers;
- divisible/non-divisible branches are disjoint;
- list and digit guards are complementary;
- recursion descends.

Globally, the `[total]` declarations for `trialPrime` and `trialDivisor` are
too broad at `D=0`. Ground probing records that the compiled theory proves
`trialPrime(0,0,true) => true` and reduces the corresponding divisor summary
to 1. Python evaluation of `0 % 0` would raise. No submitted execution can
reach this state: initialization fixes divisor 2 and every update adds 1.
Accordingly, this is recorded as an over-broad totality/evidence limitation,
not as an unsound conclusion on the intended input domain.

Evidence: `evidence/05-totality-trial-prime-zero-true.log`,
`evidence/05-totality-trial-prime-zero-false.log`, and
`evidence/05-totality-trial-divisor-zero.log`.

### Static conclusion

No rule encodes the task answer, replaces a result-bearing source computation
with an unconstrained oracle, fabricates used state, discards a continuation,
or narrows the input to finitely many sizes. The only operational bridge skips
a fixed, branch-free prefix and has the exact immutable body in its match.

## 6. Fresh non-vacuity test

No candidate-provided vacuity artifact was relied upon.

I copied the immutable spec in scratch and changed only the end-to-end result:

```k
=> digitSum(largestPrime(IS, 0)) +Int 1
```

The mutated spec is preserved as
`evidence/spec-vacuity-review.k`.

Validation:

1. `kprove ... --dry-run` exited 0, establishing successful parse and spec
   build.
2. The actual proof exited 1 with `WarnStuckClaimState`.
3. The residual says the configurations unify but the implication fails
   because
   `digitAcc(largestPrime(IS,0),0) +Int 1` cannot equal
   `digitAcc(largestPrime(IS,0),0)`.
4. Concrete satisfying witness `[2]` gives actual result 2 and mutated target
   3.

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. The proof is
discriminating and result-constraining.

Evidence:

- `evidence/06-nonvacuity.sh`
- `evidence/06-nonvacuity-summary.log`
- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-proof.log`
- `evidence/06-vacuity-witness.log`

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every finite recursive `IntList` of arbitrary K integers, starting from
the supplied initial configuration, loading the exact submitted
`solution.mpy` function and calling it with the corresponding read-only list
has this partial-correctness property:

> If execution terminates normally, the returned K value is exactly
> `digitSum(largestPrime(IS,0))`, the call stack is empty, caller environment
> and allocation cursor are restored, no exception is present, and the other
> final cells equal the claim's RHS.

The helper definitions calculate the digit sum of the largest value at least
2 that survives complete trial division through its square root. Ordinary
number theory identifies that value as the largest prime.

The proof is universal over list length and integer magnitude. It is not an
examples-only, bounded-unrolling, or fixed-size theorem. As a partial-
correctness proof it does not separately prove termination, although the
concrete Python loops do terminate for every finite integer list.

### Trust ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| K toolchain/backend `v7.1.293` | Parsing, compilation, symbolic execution | Necessary foundational trust; fresh independent builds and runs used |
| Trusted supplied semantics | All program execution | Required by `SUPPLIED_SEMANTICS`; candidate tree is byte-identical |
| K builtin Int/Bool/Map/List operations | Arithmetic, guards, environments | Standard fixed-semantics primitives; used domains avoid zero division |
| Trusted translator | Python-to-constructor artifact | Trusted translator regenerates byte-identical `solution.mpy`; this proves artifact identity, not a universal translator-correctness theorem |
| `asVals(IntList)` representation | Symbolic input iteration | Constructor-complete empty/cons iterator rules; full unbounded domain; no result influence beyond list elements |
| Proof-local fixed-rule specializations | Evaluation and local state | Exhaustive static comparison shows equal transitions and complete guards |
| Entry-prefix operational bridge | Call frame and five initializations | Exact static composition for immutable body; three bridge-free ground outcomes; missing machine universal connection is the principal concern |
| Trial/digit mathematical meaning | Human-facing “prime” and decimal digit sum | Transparent equations plus ordinary factor/square-root argument; 10,266 independent tests; not a separate K intent theorem |
| `[total]` outside reachable divisor domain | Only hypothetical helper calls with `D=0` | Over-broad, explicitly excluded from all entry/loop preconditions and source flow; non-fatal concern |
| Differential testing | Python/intent bridge on sampled inputs | Zero candidate/oracle mismatches; finite evidence only |
| Trusted canonical implementation | Cross-check | Agrees except its documented `1`-is-prime bug; not used as a proof axiom |

### Gate summary

- Real-program identity and result constraint: pass.
- Fresh reconstruction: pass.
- Full source-contract domain: pass; no finite bound or strengthened input
  precondition.
- Static soundness on every intended execution: pass.
- Non-vacuity: pass.
- Evidence/auditability: pass, with the universal entry-bridge connection and
  global helper-totality limitations documented above.

These limitations justify `CONCERNS`, but neither enables a false conclusion
for the immutable generated program on an intended input. The proof therefore
remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
