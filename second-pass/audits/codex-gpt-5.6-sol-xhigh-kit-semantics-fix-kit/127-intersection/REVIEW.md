# Independent adversarial audit: 127-intersection

## Audit conclusion

**CONCERNS / LEGIT.** The candidate contains a legitimate, non-vacuous
partial-correctness proof of the actual translated program under the supplied
MPY semantics. Clean reconstruction closed the loop claim and every entry claim
independently, the proof macro expands to the exact submitted `solution.mpy`
AST, and a fresh false-result mutation is rejected with the actual opposite
result in the residual.

The documented concern is limited: the K entry postconditions end in the
candidate-defined `trialPrime`/`primeAnswer` summary. Static review establishes
the ordinary mathematical trial-division argument, but the factor-at-most-
square-root theorem connecting that summary to the natural-language word
“prime” is not itself a K claim. Per the requested decision boundary, this is
an informal intent bridge, so it warrants `CONCERNS` rather than an unqualified
`PASS`; it does not make a false result provable.

All candidate prose, traces, logs, compiled definitions, and prior verdicts
were treated as untrusted claims. Builds and experiments used only copied
source under `/tmp/audit-work/127-intersection`; candidate-provided compiled
directories and caches were never reused.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is present as a real directory, so there is no
mode/mount contradiction and no infrastructure breach.

The following checks all passed:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k` are regular, non-symlink candidate files.
- One structured JSONL generation trace is present and all 310 records parse as
  JSON. Its assertions, like the candidate's `VALIDATED` and `#Top` reports,
  were not used as proof evidence.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`, SHA-256
  `aaebd5df799992f92d5d1e023101fa08b8a199d71be54536511e5ed071d5db1c`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Recursive name, type, symlink, and content comparisons found no missing,
  additional, changed, mistyped, or symlinked entry in the candidate
  `reference-semantics/` tree. It is exactly the trusted supplied tree.

The candidate also contains `runtime-kompiled/`, `verification-kompiled/`,
`__pycache__/`, test files, and prior proof reports. Those are not required
source-integrity failures and were deliberately excluded from the scratch copy.
No required source artifact was missing or altered.

Evidence: [provenance log](evidence/01-provenance.log),
[untrusted-claim summary](evidence/01-untrusted-claims.log), and
[scratch-copy log](evidence/01-scratch-copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

Inputs are two closed intervals `(A,B)` and `(C,E)` of integers with `A <= B`
and `C <= E`. Let

```text
L = min(B,E) - max(A,C).
```

The examples establish geometric interval length, not a count of included
integers: a touching intersection has length 0 and `(2,3)` has length 1. The
required answer is exactly `"YES"` when `L` is prime and `"NO"` otherwise;
disjoint intervals have negative `L` and therefore return `"NO"`.

The trusted canonical computes the same endpoints, requires `length > 0`, and
uses divisor search. The submitted program uses explicit endpoint branches and
a square-root-bounded divisor loop. It is a different but equivalent algorithm
on the intended domain.

### Translation identity

Running the trusted translator afresh on the copied `solution.py` produced
`solution.regenerated.mpy` with SHA-256
`7574c86e26b0404f4bacf0c7268a88195fa39100bce893b9a84ffdf66c5d98b7`,
byte-identical to submitted `solution.mpy`. The command and `cmp` exit 0 are in
[translation identity](evidence/02-translation-identity.log).

### Independent differential reconstruction

The reviewer-authored [differential script](evidence/differential_test.py)
loads the trusted canonical and submitted solution from explicit paths. A third
oracle computes the endpoint formula and scans every divisor from 2 through
`length-1`; it does not reuse the submitted square-root loop.

It covered:

- all three prompt examples and the canonical docstring example;
- disjoint, touching, singleton, length 1, lengths 2/3/4/5, square and
  composite lengths, negative coordinates, and large prime/composite lengths;
- equality and strict sides of both endpoint branch conditions;
- all 23,409 pairs formed from the 153 ordered intervals with endpoints in
  `[-8,8]`; and
- 2,000 deterministic random ordered interval pairs with endpoints in
  `[-1000,1000]`.

All 25,431 comparisons agreed among canonical, submitted, and independent
oracle; mismatch count was zero. The complete deterministic input list is
[preserved here](evidence/differential-inputs.json), with commands and results
in [the differential log](evidence/02-differential.log). This is finite bridge
evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

The live toolchain was Python 3.10.12 and K v7.1.293; exact version commands are
in [the toolchain log](evidence/00-toolchain.log).

From the clean source copy, I built:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

Both exited 0. A reviewer-authored MPY harness whose function AST is identical
to submitted `solution.py` then passed 12 normal/boundary assertions under the
fresh LLVM definition. Evidence: [harness translation](evidence/03-concrete-harness-translation.log),
[LLVM build](evidence/03-kompile-llvm.log),
[LLVM execution](evidence/03-krun-concrete.log), and
[Haskell build](evidence/03-kompile-haskell.log).

Every positive claim was then exercised independently. Each entry run retained
`SPEC.prime-loop`, because that claim is the explicit circularity summarizing
the real loop; it selected only one entry target besides that auxiliary claim.

| Positive target | Fresh result |
|---|---|
| `SPEC.prime-loop` | `#Top`, exit 0 ([log](evidence/03-kprove-prime-loop.log)) |
| `SPEC.intersection-c-gt-a-e-lt-b` | `#Top`, exit 0 ([log](evidence/03-kprove-c-gt-a-e-lt-b.log)) |
| `SPEC.intersection-c-gt-a-e-ge-b` | `#Top`, exit 0 ([log](evidence/03-kprove-c-gt-a-e-ge-b.log)) |
| `SPEC.intersection-c-le-a-e-lt-b` | `#Top`, exit 0 ([log](evidence/03-kprove-c-le-a-e-lt-b.log)) |
| `SPEC.intersection-c-le-a-e-ge-b` | `#Top`, exit 0 ([log](evidence/03-kprove-c-le-a-e-ge-b.log)) |

The mechanical [positive-proof summary](evidence/03-positive-proof-summary.log)
confirms exactly one `#Top` and one recorded zero status per log.

For transparency, an early diagnostic selected an entry claim alone and thereby
filtered out its loop circularity. I stopped that irrelevant unrolling run; it
is documented in [the diagnostic note](evidence/03-diagnostic-entry-only-aborted.md)
and is not candidate evidence.

LLVM reported supplied-semantics coverage warnings, considered in stage 5.
Haskell compilation and proof parsing reported only unused variables in
supplied `str.k` and in the framed loop claim. No positive command timed out,
stuck, or exited nonzero.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.prime-loop` starts at the exact internal `#while` head with fixed module
and callee scopes, `N >= 2`, `D >= 2`, `length=N`, `is_prime=true`, and
`divisor=D`. It executes the real guard/body until the loop exits, leaves all
unmodified state pinned, changes `is_prime` to `trialPrime(N,D)`, and permits
only the now-dead final divisor to be existential. Its framed `<k>` continuation
and stack are not modified by this loop body.

The four entry claims share `A <= B` and `C <= E` and partition all inputs as:

| Endpoint case | Exact postcondition value |
|---|---|
| `C > A`, `E < B` | `primeAnswer(E-C)` |
| `C > A`, `E >= B` | `primeAnswer(B-C)` |
| `C <= A`, `E < B` | `primeAnswer(E-A)` |
| `C <= A`, `E >= B` | `primeAnswer(B-A)` |

Those four expressions are exactly
`min(B,E)-max(A,C)`. The partition includes equality boundaries and allows a
negative length in the two disjoint cases.

### Program identity, control flow, and result constraint

Fresh `kast` parsing of submitted `solution.mpy` and macro expansion of
`SOLUTION-MODULE` produced byte-identical JSON ASTs, SHA-256
`9d6d690715cfce1c069ab9155289585d4b0b175d13ddeb4e4ca1fd41ffb76655`.
See [program-pinning AST evidence](evidence/04-program-pinning-ast.log).

The entry `<k>` cell executes `#loadAll(SOLUTION-MODULE)`, looks up and calls the
loaded `intersection` closure, binds both exact tuple arguments, executes the
submitted body, returns, and pops the frame. There is no proof-local rule for
`Call`, `#applyK`, `While`, `Return`, or a configuration cell. The final `<k>`
cell is directly the single `primeAnswer(...)` value—not a free variable,
tautology, implication, or unconstrained oracle. Entry claims also constrain
module scope, allocator counters, heap, stack, return/exception state, and exit
code after the call.

Every precondition is satisfiable. Reviewer witnesses and substitutions are:

| Claim | Witness `(interval1, interval2)` | Claimed length/result |
|---|---|---|
| first endpoint case | `(0,10),(2,7)` | 5 / `YES` |
| second endpoint case | `(0,5),(2,5)` | 3 / `YES` |
| third endpoint case | `(2,7),(0,5)` | 3 / `YES` |
| fourth endpoint case | `(2,7),(2,7)` | 5 / `YES` |
| loop | `N=5,D=2` | `trialPrime(5,2)=true` |

Both Python implementations agree with every substituted entry result; exact
checks are in [claim witnesses](evidence/04-claim-witnesses.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory covers all 26 K source files used or required by the
definition: top-level supplied `semantics.k`, all 23 helper files, candidate
`verification.k`, and `spec.k`. It contains 1,116 addressed records, including:

- 705 rules: 599 ordinary, 45 priority, 35 concrete-attributed, and 26 owise;
- 233 syntax declarations, including every `function`, `total`, macro, strict,
  and symbol/no-evaluators declaration;
- five contexts, one configuration, and five claims; and
- no `simplification` rule and no `functional` declaration.

Counts were independently reconciled against source-line searches. The full
line-addressed inventory is [05-rule-inventory.tsv](evidence/05-rule-inventory.tsv),
its hashes and counts are [summarized here](evidence/05-rule-inventory-summary.txt),
and validation is in [05-rule-inventory-validation.log](evidence/05-rule-inventory-validation.log).

Every record has an explicit relevance, decision, and basis in
[05-rule-decisions.tsv](evidence/05-rule-decisions.tsv). The 928 supplied
syntax/rule/context/configuration records are accepted as the fixed semantics
selected by the problem after byte-identity verification; used cases receive
the additional behavioral review below, while unreached cases are explicitly
outside the program path. The proof-local decisions comprise eight exact macro
records, eight true total-definition records, one sound auxiliary claim, and
four result-constraining targets. No rule was classified unsound.

### Used language and state behavior

[The used-construct map](evidence/05-used-construct-map.md) maps every AST
construct to declaration and executing rules. The important conclusions are:

- module load and statement sequencing preserve the exact submitted body;
- `FuncDef` creates the exact closure; generic call routing performs lookup,
  left-to-right argument evaluation, exact two-parameter binding, frame push,
  body execution, return, and frame pop;
- assignments evaluate RHS first and update the plain callee frame;
- exact two-element tuples and indexes 0/1 reduce through concrete in-bounds
  subscript equations;
- comparison contexts and `seqstrict` binary operations preserve evaluation
  order; every arithmetic/comparison dispatch is the matching integer case;
- `BoolOp("and")` is head-first and short-circuiting;
- `While` reevaluates the real guard, executes the real body, and returns to the
  exact `#while` head summarized by the auxiliary claim;
- return control discards the rest of the body, restores the caller, and yields
  the exact ASCII string value; and
- all cells changed by load/call/return are pinned in the entry claims.

Relevant priority alternatives for closure cells or heap references are
inapplicable: the function has a plain local frame and inputs are unboxed tuple
values. Relevant generic `Call` and `Compare` rules marked owise are selected
only after no specialized rule matches. There is no allocation on the proof
path and no exceptional tuple or modulo case: tuple shape is exact and every
reached divisor is at least 2.

The proof definition imports `MPY`, not `MPY-KRUN`, so the 16 concrete-only
rules in `semantics/concrete.k` do not participate in symbolic proof. The
supplied tree contains 25 symbol-attributed functions, including opaque float,
sort, and MD5 operations; none can be produced by this program. The one used
partially totalized helper, `valSeqAt`, always reduces through its in-bounds
rules on exact tuple shapes. Thus LLVM's non-exhaustiveness warnings do not
introduce an opaque or fabricated result on the intended domain.

### Proof-local extensions

| Extension | Class | Soundness decision |
|---|---|---|
| Four macro declarations/expansions | Definitional syntax | Accepted: macro expansion is exactly the parsed submitted MPY AST and performs no operational rewrite. |
| Four `trialPrime` equations | Definitional summary | Accepted: guards are pairwise disjoint and exhaustive. The recursive case increases `D` while `D*D <= N`; the other cases return the correct trial-division result. No state is read or changed. |
| Two `primeAnswer` equations | Definitional summary | Accepted: `trialPrime` versus its negation is an exhaustive/disjoint Bool split with exact `YES`/`NO` code sequences. |
| `SPEC.prime-loop` | Derived auxiliary reachability claim | Accepted: exact real loop head/body, truthful base/divisor/recursive cases, and correct state framing. |
| Four entry claims | Target theorems | Accepted: exhaustive satisfiable domain partition, exact program load/call, and direct intended result summary. |

There are no proof-local simplification, concrete, priority, opaque-symbol, or
operational-bridge rules. In particular, no candidate rule encodes a return at
call/loop level, replaces computation with an oracle, or silently handles an
unmodeled used construct. I make no unsound-rule finding, so there is no false-
conclusion witness to report for such a finding.

## 6. Fresh non-vacuity test

I did not reuse candidate `spec-vacuity.k`. The fresh reviewer mutation is
[reviewer-false-result.k](evidence/reviewer-false-result.k). It uses the
satisfying second-case input `(0,5),(2,5)`, whose intersection length is 3, but
changes the result-constraining destination from actual `"YES"` to false
`"NO"`.

The mutation first built successfully with `kprove --dry-run`, exit 0; its KORE
artifact and hashes are recorded in [the mutation-build log](evidence/06-mutation-build.log).
The actual proof then exited 1 with `WarnStuckClaimState`. Its reachable residual
contains `str(iCons(89,iCons(69,iCons(83,...))))`—actual `"YES"`—which cannot
unify with mutated `"NO"`. This is the expected unmet result obligation, not a
parse error, missing import, timeout, or unrelated crash. See
[the full proof log](evidence/06-mutation-proof.log) and
[the independent validation](evidence/06-mutation-validation.log).

The proof is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics and the audited proof-local definitions, for
all K integers `A,B,C,E` satisfying `A<=B` and `C<=E`, if the exact submitted
translated call terminates, its returned value is

```text
primeAnswer(min(B,E) - max(A,C)).
```

The loop claim formally connects real loop execution to `trialPrime`, and the
entry claims connect real module load/call/return execution to that result.
This is partial correctness. The K claims do not prove liveness; termination on
the formal domain follows separately because either a divisor sets the Boolean
false or integer `divisor` increases until its square exceeds fixed `length`.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted supplied `reference-semantics/` | Defines syntax, values, evaluation, state, calls, control, and arithmetic for every claim | Acceptable and mandated by `SUPPLIED_SEMANTICS`; byte identity is established. Used constructs were also reviewed and concretely exercised. Broader unused-language correctness is not claimed. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py` to the proved MPY AST | Acceptable designated trusted input. Fresh regeneration proves artifact identity, not universal translator correctness. |
| K v7.1.293 compiler, Haskell/LLVM backends, SMT/rewrite engine | Builds and checks all dynamic evidence | Conventional low-level toolchain trust boundary; positive and negative controls behaved discriminatingly. |
| `trialPrime` equations and `primeAnswer` encoding | Affect the final value of every entry claim | Not assumed: their guards, recursion, and string results were audited rule by rule, and loop execution is formally connected to them. |
| Composite-factor square-root theorem | Connects `trialPrime(N,2)` to ordinary mathematical primality | True elementary mathematics, but informal rather than a separate K theorem. This is the sole verdict concern. Differential evidence supports but does not prove it universally. |
| Supplied opaque float/sort/MD5 symbols and out-of-bounds totalization | Could affect unrelated programs | Unreached here; none affects control, state, or result on exact entry inputs. |
| Python implementation limits, resource exhaustion, interrupts, malformed tuples, non-integer elements, or reversed endpoints | Outside the formal execution/domain | Explicitly excluded; the prompt and claims require two ordered integer pairs. |

Formally proved facts, ordinary mathematical reasoning, finite tests, and
excluded behavior are thus separated. Candidate `PROOF.md`, generation traces,
prior `#Top` output, and differential tests were never substituted for the
fresh K proof.

### Gate and verdict rationale

- Real-program soundness: **PASS**. The body executes under fixed semantics,
  no operational bridge exists, proof-local equations are true, state is
  preserved, witnesses exist, and the fresh false result is rejected.
- Intent adequacy: **PASS with a documented formalization limitation**. Domain,
  endpoint length, strings, and Python behavior align; the summary-to-primality
  bridge is an elementary but informal mathematical argument.
- Trust/evidence auditability: **PASS**. Commands, statuses, bounded logs,
  scripts, inputs, complete rule inventory, and negative control are preserved.

The reconstruction is therefore sound, result-constraining, and pinned to the
real generated program. The informal summary-to-natural-language bridge is a
limitation but not an illegitimate proof device, yielding the required
`CONCERNS / LEGIT` pairing.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
