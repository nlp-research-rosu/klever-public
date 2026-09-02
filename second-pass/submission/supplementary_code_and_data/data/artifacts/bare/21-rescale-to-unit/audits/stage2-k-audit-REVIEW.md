# Independent adversarial review: 21-rescale-to-unit

This review treats all candidate and generation records as untrusted evidence. I
reconstructed the semantics and proof from source in
`/tmp/audit-work/21-rescale-to-unit-audit`; no candidate-provided compiled
definition or cache was copied or used.

The candidate's seven reachability claims do close and are non-vacuous, but
they are not a proof of the HumanEval contract. They cover only fixed examples
and symbolic lists of lengths 2, 3, and one special length-4 shape, rather than
arbitrary lists of at least two elements. In addition, the generated semantics
replaces CPython floating-point arithmetic with exact rational arithmetic. A
finite-float witness makes that abstraction observably false. Either defect is
material; the benchmark's explicit mapping makes the finite-size domain
narrowing `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher record declares:

- problem `21-rescale-to-unit`, condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required selected-stage1
generation records, `usage.json`, and the structured trace. The campaign block
in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`; the lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

The independent checker and its complete bounded output are
[`provenance_check.py`](/audit-output/evidence/provenance_check.py) and
[`01-provenance.log`](/audit-output/evidence/01-provenance.log). It established:

- every required record is a regular readable file;
- every recorded file-level hash matches, including run, task, result,
  invocation, metrics, usage, prompt, output log, final text, canonical,
  trusted prompt, and trusted translator;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- no symlinks occur under `/candidate`, `/reference`, or
  `/generation-evidence`;
- `/reference/reference-semantics` is absent, as generated-semantics mode
  requires;
- the trace is one regular JSONL file, has 302 valid events and zero malformed
  lines, and its file digest matches the stage result;
- recomputing the installed pipeline tree digest gives
  `ae17697bd3144f0e3f976ac94f0b3d34ebfcd3ab6954fb625889691da4200fd6`
  for `/candidate`, exactly the retained workspace digest in
  `invocation.json`;
- recomputing the same tree digest for the trace gives
  `51f1c651148bfafc5711d77a5e311c14e3f29d6ebde8e670b7346fa6e9cca2e0`,
  exactly `usage.json`'s source-trace digest.

The audit-layer manifest also records its own tree-digest fields, while the
stage records use the installed pipeline tree routine above. The independently
recomputed stage digests and all artifact hashes agree with the mounted data.
There is no provenance or infrastructure breach, so a candidate verdict is
appropriate.

The generation records claim `KPROVE_PASSED`. I used that only as a claim to
recheck. Historical runtime metrics absent from this legacy-selected record
were neither reconstructed nor treated as a defect.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says that, given a list of numbers with at least two
elements, the function must apply a linear transform so the smallest value
becomes 0 and the largest becomes 1. The trusted canonical implementation
computes:

```text
lo = min(numbers)
hi = max(numbers)
[(x - lo) / (hi - lo) for x in numbers]
```

The submitted `solution.py` is the same algorithm, with only local-variable and
formatting differences (`minimum`, `maximum`, and `number`). It preserves the
entry-point name and signature.

### Trusted translation

In clean scratch I ran:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -l regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`69c695ed27f93cc676020bc8a8c4adf2af65d50eb54ef1f213fe312d3b512682`.
See [`02-translation.log`](/audit-output/evidence/02-translation.log).

### Independent differential test

[`differential.py`](/audit-output/evidence/differential.py) imports the trusted
canonical and submitted entry points independently. It ran 44 cases:

- the documented example;
- empty, singleton, and constant-list boundaries, comparing exceptions;
- ascending and descending two-point lists;
- repeated minima and maxima;
- min/max at different positions;
- negative and fractional values;
- a wide-magnitude case;
- three deterministic generated cases for every length from 2 through 12.

All 44 outcomes matched, including exception types/messages, with exit 0 and
zero mismatches. The full inputs and outputs are in
[`03-differential.log`](/audit-output/evidence/03-differential.log).
This establishes implementation fidelity on those cases, not a universal
theorem.

## 3. Clean proof reconstruction

The available tools were K version 7.1.293. Only the source files copied from
the candidate and the trusted translator output were used.

### Concrete semantics

I built a fresh LLVM definition:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

It exited 0; see
[`04-kompile-concrete.log`](/audit-output/evidence/04-kompile-concrete.log).
Fresh `krun` executions covered:

- `[1, 2]` -> `[0, 1]`;
- `[2, 1]` -> `[1, 0]`;
- prompt example `[1,2,3,4,5]` -> `[0,1/4,1/2,3/4,1]`;
- repeated extrema `[-2,-2,5,5]` -> `[0,0,1,1]`;
- a length-6 list `[3,-1,7,0,7,5/2]` ->
  `[1/2,0,1,1/8,1,7/16]`.

Every execution exited 0. The complete final configurations are in
[`05-krun-concrete.log`](/audit-output/evidence/05-krun-concrete.log) and
agree with the independent Python cases in stage 2.

### Proof definition and all positive claims

I built a fresh Haskell definition:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

It exited 0; see
[`06-kompile-proof.log`](/audit-output/evidence/06-kompile-proof.log).
The original positive command:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`; see
[`07-kprove-all.log`](/audit-output/evidence/07-kprove-all.log).

To check every claim independently, I made
[`spec-labeled.k`](/audit-output/evidence/spec-labeled.k), changing only the
module name and adding labels to the seven unchanged claim bodies. Each of
`claim-01` through `claim-07` was selected in a separate `kprove` command.
All seven exited 0 and printed `#Top`; see
[`08-kprove-each.log`](/audit-output/evidence/08-kprove-each.log).

Thus clean reconstruction succeeds for exactly the submitted claims. This
does not answer whether those claims prove the requested unrestricted theorem.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each entry claim

| Claim | Precondition | What its postcondition proves |
|---|---|---|
| 1 | `true` | The one fixed prompt example of length 5 returns `[0,1/4,1/2,3/4,1]`. |
| 2 | `true` | The fixed length-4 input `[-5,0,5,5]` returns `[0,1/2,1,1]`. |
| 3 | `A < B` | Every ascending two-element rational list `[A,B]` returns `[0,1]`. |
| 4 | `A < B < C` | Every strictly ascending three-element rational list returns `[0,(B-A)/(C-A),1]`. |
| 5 | `A < B < C` and `A != C` | The same ascending length-3 result equals the local `rescaleSpec`. |
| 6 | `A < B < C` | The descending length-3 list `[C,B,A]` returns `[1,(B-A)/(C-A),0]`. |
| 7 | `A < B` | The special length-4 list `[A,A,B,B]` returns `[0,0,1,1]`. |

[`claim_witnesses.py`](/audit-output/evidence/claim_witnesses.py) supplies a
ground state satisfying every precondition. Each claimed result agrees with
both Python implementations; see
[`10-claim-witnesses.log`](/audit-output/evidence/10-claim-witnesses.log).
The claims are therefore satisfiable and result-constraining.

### Mechanical program identity

`verification.k` defines `solutionProgram` as a constructor tree. It is not an
oracle or a summary result: `verify` expands it into module loading and an
actual invocation, so the assignments, min/max calls, subtraction, division,
and comprehension execute under `semantic.k`.

I independently parsed both the submitted `solution.mpy` and the normalized
RHS of the `solutionProgram` rule to KORE using the fresh proof definition.
The only normalization is omission of explicit empty K list units
(`.Strings`, `.Stmts`) in program surface syntax. The two KORE files are byte
identical with SHA-256
`9398feb77f7e305f60ce6228d1aafd7edd0395aee8450ba28203b23dab932c72`.
The normalized RHS is
[`solutionProgram-rhs.mpy`](/audit-output/evidence/solutionProgram-rhs.mpy);
the successful comparison is
[`09b-program-pinning-normalized.log`](/audit-output/evidence/09b-program-pinning-normalized.log).

The earlier
[`09-program-pinning.log`](/audit-output/evidence/09-program-pinning.log)
records a reviewer-side parser attempt that incorrectly put rule-only explicit
list-unit spelling into the program parser. It failed before comparison and is
not candidate evidence; the corrected constructor comparison above succeeded.

Body sensitivity was also checked. The reviewer artifact
[`verification-body-mutant.k`](/audit-output/evidence/verification-body-mutant.k)
changes the numerator in the constructor tree actually executed by the claim
from `number - minimum` to `maximum - minimum`.
[`spec-body-mutant.k`](/audit-output/evidence/spec-body-mutant.k) keeps the
original example result. The mutant definition built successfully
([`12-body-mutant-build.log`](/audit-output/evidence/12-body-mutant-build.log)),
but proof failed with the reached value `[1,1,1,1,1]`
([`13-body-mutant-proof.log`](/audit-output/evidence/13-body-mutant-proof.log)).
This is a valid body-sensitivity test because it changes the program term
executed by the claim.

### Fatal domain inadequacy

No claim quantifies over an arbitrary `Rats` tail or arbitrary list length.
The symbolic claims have fixed constructor lengths 2, 3, or the single
four-element pattern `[A,A,B,B]`. The two other claims are fixed examples.
There is no induction/circularity, recursive-list execution theorem, or
universal connection claim that could generalize these finite shapes.

For example, `[3,-1,7,0,7,2.5]` is a valid nonconstant length-6 input. Concrete
execution succeeds, but no target claim states or proves its result, let alone
the result for every length-6 or arbitrary-length list. Finite testing cannot
fill this gap.

The source contract says “at least two elements,” not “at most five” or “one
of these shapes.” This materially narrows the HumanEval domain. Under the
benchmark instruction, even a sound finite-size theorem maps to
`FAIL / NOT_LEGIT`.

The formal claims also say nothing about constant lists. CPython raises
`ZeroDivisionError` for such inputs while the rational semantics gets stuck at
division by zero. The task's desired min/max normalization implicitly needs
distinct extrema, but that necessary precondition/exception behavior is not
formalized.

## 5. Rule-by-rule static soundness review

The exhaustive lexical inventory is preserved in
[`14-static-inventory.log`](/audit-output/evidence/14-static-inventory.log).
There are 28 rules in `semantic.k`, 9 rules in `verification.k`, and 7 claims.
There are no other helper K files.

### Declarations, configuration, and attributes

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- list sorts `Stmts`, `Strings`, and `Rats`;
- `Params`, `CellVars`, and `FreeVars`;
- statement constructors `ImportFrom`, `FuncDef`, `Assign`, and `Return`;
- expression constructors `Name`, `Call`, `BinOp`, `ListComp`, and `Bool`;
- `CompFor`;
- runtime `Value` alternatives `Rat`, `vlist(Rats)`, and `noResult`;
- stored `Definition` as `function(Params, Stmts)`.

`SEMANTIC` has exactly four active cells: `<k>`, `<functions>`, `<env>`, and
`<result>`. They are all read or written. It adds `boot`, `exec`, and `invoke`
as computations. Its function declarations are `eval`, `evalComp`, `prepend`,
`evalNumber`, `minValue`, `maxValue`, `minRats`, and `maxRats`.

`VERIFICATION` adds function symbols `solutionProgram`, `rescaleSpec`, and
`scaleRats`, plus the proof-harness computations `verify`, `collect`, and
`done`.

No local declaration has `[total]`, `[functional]`, `[concrete]`, priority,
macro, alias, anywhere, or opaque attributes. Eleven symbols have `[function]`;
their equations are intentionally partial outside the modeled term shapes.
Only three rules have `[simplification]`, inventoried below. There are no
priority rules and no unconstrained fresh result symbols.

Every constructor used by `solution.mpy` is mapped: module/import/function
loading uses rules S01–S04; invocation and sequential statements use S05–S07;
names and min/max calls use S08–S10 and S19–S28; `BinOp("-",...)` and
`BinOp("/",...)` use S11 and S13–S15; and the list comprehension with its
literal `Bool(true)` generator uses S12 and S16–S18.

### `semantic.k`: all 28 rules

| ID / line | Rule role | Static decision |
|---|---|---|
| S01 / 64 | `boot(Module(SS),ARG)` loads then invokes the named entry point. | Faithful for the one submitted module and entry point. |
| S02 / 66 | Empty statement execution terminates. | Sound. |
| S03 / 67 | `ImportFrom` is erased. | Sound for the actual typing-only import after annotations are transliterated away; over-broad for runtime imports, which the submitted term does not use. |
| S04 / 69–70 | A `FuncDef` registers its parameter/body then continues. | Sound for this capture-free single function. Ignored cell/free metadata is inert here. |
| S05 / 72–74 | Invocation looks up a one-parameter definition and initializes its environment. | Sound for this exact binding and fresh top-level invocation. No call stack is needed by the program. |
| S06 / 76–77 | Assignment evaluates its pure RHS in the old environment, updates the name, then continues. | Correct sequencing for the two assignments. |
| S07 / 79–81 | Return discards remaining statements, sets the result, and leaves the continuation. | Correct for Python return and for the following proof `collect` continuation. |
| S08 / 95 | General value-name lookup in the map. | Sound with unique K map keys. |
| S09 / 97 | Syntactic call to `min` invokes `minValue`. | Correct for this program because `min` is not shadowed. Globally over-broad as Python name resolution, but no intended input changes the binding. |
| S10 / 98 | Syntactic call to `max` invokes `maxValue`. | Same decision as S09. |
| S11 / 100 | A `BinOp` value dispatches to numeric evaluation. | Sound for the only used operators `-` and `/`; unsupported operators visibly remain partial. |
| S12 / 102–103 | A list comprehension iterates the source list. | It ignores the predicate argument. That is globally false for a term with `Bool(false)` (Python would produce `[]`, this rule would include elements), but the submitted constructor has literal `Bool(true)` for every intended input. Therefore this is a non-reusable over-broad rule, not a false-result witness for the fixed submitted program. |
| S13 / 105 | Numeric name lookup requires a rational value. | Sound on the claim domains. |
| S14 / 106–107 | Python subtraction is modeled as exact `-Rat`. | Mathematically sound over `Rat`, but not a sound rule for CPython float subtraction; see the concrete false conclusion witness below. |
| S15 / 108–109 | Python division is modeled as exact `/Rat`. | Mathematically sound for nonzero rational denominators, but not a sound rule for CPython float division; see the witness below. Division-by-zero exceptions are not modeled. |
| S16 / 111 | Comprehension over an empty rational list returns empty. | Sound. |
| S17 / 112–114 | Comprehension over a cons evaluates the element under a temporary iteration-variable binding and recurses. | Sound for this pure comprehension; it also correctly avoids leaking the Python 3 comprehension variable. |
| S18 / 116 | `prepend` constructs a rational list. | Sound. |
| S19 / 118 | `minValue` seeds `minRats` with the nonempty head. | Sound for nonempty lists. |
| S20 / 119 | `maxValue` seeds `maxRats` with the nonempty head. | Sound for nonempty lists. |
| S21 / 121 | Minimum fold base case. | Sound. |
| S22 / 122–123 | Minimum keeps `M` when `M < R`. | Sound over totally ordered rationals. |
| S23 / 124–125 | Minimum keeps `M` when equal. | Sound. |
| S24 / 126–127 | Minimum replaces `M` when `M > R`. | Sound. |
| S25 / 129 | Maximum fold base case. | Sound. |
| S26 / 130–131 | Maximum keeps `M` when `M > R`. | Sound. |
| S27 / 132–133 | Maximum keeps `M` when equal. | Sound. |
| S28 / 134–135 | Maximum replaces `M` when `M < R`. | Sound. |

The comparison guards for S22–S24 and S26–S28 are mutually exclusive and
exhaustive over `Rat`; recursive calls strictly shorten `Rats`. Function rules
used by the claims have no conflicting overlaps. Statement evaluation is
left-to-right because each `exec` rule consumes the head and explicitly leaves
the remaining `Stmts` computation. All program expressions are pure, so
functional evaluation does not suppress a used state effect. There is no
allocation, heap, output, exception, or other state cell to preserve in this
minimal model.

### `verification.k`: all 9 rules

| ID / line | Rule role | Static decision |
|---|---|---|
| V01 / 9 | `R +Rat (-1 *Rat R) = 0` simplification. | True for every rational. |
| V02 / 10 | `R /Rat R = 1` when `R != 0`. | True and correctly guarded. |
| V03 / 11 | `0 /Rat R = 0` when `R != 0`. | True and correctly guarded. |
| V04 / 17–31 | Expands `solutionProgram` to a concrete constructor tree. | Definitional macro; mechanically identical to trusted regeneration, with body sensitivity demonstrated. It does not summarize a result. |
| V05 / 38–40 | `verify` executes module statements, invokes the real function, then collects. | Proof harness equivalent to the `boot` execution prefix; it does not bypass the body. |
| V06 / 42–45 | `collect` moves the returned value into `done` and clears harness cells. | Result-preserving for this return-only property. It abstracts local/module bookkeeping, so it would not prove a property of those cells. |
| V07 / 52–53 | `rescaleSpec` computes min/max then pointwise scaling for a nonempty list. | Truthful definitional summary over exact rationals; it replaces no program execution. |
| V08 / 55 | Empty `scaleRats` returns empty. | Sound. |
| V09 / 56–58 | Nonempty scaling applies `(X-LO)/(HI-LO)` and recurses when extrema differ. | Sound over exact rationals and strictly descending on the list. |

The three simplification equations are true, guarded where division requires
it, and non-overlapping in a harmful way. `rescaleSpec` and `scaleRats` remain
partial when extrema are equal, consistent with the guarded uses. No rule
encodes an unconstrained oracle, guesses the requested answer, fabricates a
fresh result, or skips the program-defined body.

### Concrete false-conclusion witness for the numeric semantics

The exact-rational choice is not merely a harmless rounding abstraction. Use
the finite, distinct Python floats:

```text
[-1e308, 1e308]
```

Both the trusted canonical and submitted Python compute `[0.0, nan]`: the
denominator overflows to positive infinity and the maximum's numerator also
overflows, so the second division is `inf / inf`. The rebuilt K semantics,
given the corresponding exact integers, uses S14 and S15 and terminates with
`vlist(0,1)`.

The reviewer script, exact generated `krun` command, both Python observations,
and K final configuration are in
[`numeric_model_witness.py`](/audit-output/evidence/numeric_model_witness.py)
and
[`11b-numeric-model-witness.log`](/audit-output/evidence/11b-numeric-model-witness.log).
The script exits 0 only after observing this divergence. The prior
[`11-numeric-model-witness.log`](/audit-output/evidence/11-numeric-model-witness.log)
records a reviewer script bug that compared two `nan` values with `==`; the
underlying outputs already showed the same divergence, and the corrected
predicate is preserved in `11b`.

This witness lies in the stated source type and size domain: two finite,
distinct floats. It shows the combined S14/S15 language bridge can enable the
false Python conclusion that the maximum becomes exactly 1. Thus the generated
semantics proves an idealized rational program, not the real CPython numerical
behavior over the contract's unrestricted float domain.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust or reuse. I created
[`spec-vacuity-audit.k`](/audit-output/evidence/spec-vacuity-audit.k) from
claim 3 and changed the result-constraining endpoint from 1 to 2:

```text
verify(solutionProgram, vlist(A,B)) => done(vlist(0,2))
requires A < B
```

`A=0, B=1` is a concrete satisfying witness and the true result is `[0,1]`.
The mutation dry-run compiled successfully and exited 0; see
[`15-vacuity-build.log`](/audit-output/evidence/15-vacuity-build.log). The real
proof then exited 1 with `WarnStuckClaimState`; its residual explicitly contains
`done(vlist(0,1))`, which does not unify with the false destination. See
[`16-vacuity-proof.log`](/audit-output/evidence/16-vacuity-proof.log).

This is meaningful non-vacuity evidence for the narrow rational claim. It does
not repair the missing arbitrary-length theorem or the false float-model
bridge.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on K 7.1.293, its Haskell reachability prover, the built-in
rational/Boolean/map/string domains, `semantic.k`, and the three true
simplifications, the submitted reachability proof establishes all seven
finite-shape statements listed in stage 4. The concrete constructor body
executes: it loads the function, binds the argument, computes rational min and
max, performs exact-rational subtraction/division for every element, and
returns the listed exact-rational value. The false-postcondition and body
mutations show these claims constrain and depend on the result and body.

It does **not** establish:

- correctness for arbitrary list length;
- the task contract for all lists of at least two elements;
- CPython IEEE-754 behavior;
- behavior for equal extrema or Python exceptions;
- a universal equivalence between `rescaleSpec` and program execution (claim 5
  has length 3 only);
- correctness merely because the finite differential suite passed.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, LLVM/Haskell backends, and `kprove` implementation | All dynamic evidence and closure | Ordinary toolchain trust boundary; acceptable for a K proof audit. |
| Built-in `RAT`, `BOOL`, `MAP`, and `STRING` modules | All semantic and proof arithmetic/state | Acceptable for the internal exact-rational theorem. |
| Exact rationals standing for Python floats | S14, S15, all seven formal results, `rescaleSpec` | Illegitimate for the claimed real-program/source-domain theorem; refuted by the finite-float witness. |
| Hardwired unshadowed `min`/`max` binding | S09, S10 and all results | Acceptable for this exact module: no assignment/import shadows either builtin. |
| Typing-only import erasure and ignored closure metadata | Module loading/program identity | Acceptable for this capture-free program and trusted translator output. |
| Comprehension predicate ignored by S12 | Comprehension execution | Over-broad semantics, but the actual program has literal `Bool(true)` for every input; no false conclusion for this fixed term was found from this rule alone. |
| `verify`/`collect` result harness and cell cleanup | Shape of all seven claim destinations | Acceptable for a return-value-only theorem; it does not justify claims about cleared cells. |
| Three rational simplification rules | Symbolic closure | Acceptable ordinary mathematics, with nonzero guards on division. |
| Manually embedded `solutionProgram` | All seven claim bodies | Discharged for the immutable candidate by trusted regeneration, byte-identical KORE constructor comparison, and executed-body mutation. |
| Trusted canonical and 44-case differential suite | Python implementation fidelity and finite adequacy evidence | Reproducible finite evidence only; it is not a proof or a bridge theorem. |
| Generalization from fixed list sizes to arbitrary lists | Required source contract | No such lemma, invariant, claim, or justified assumption exists. This is missing proof, not a permissible trust boundary. |

### Gate and benchmark decision

- Real-body/result gate: the claims execute the pinned constructor body and
  pass non-vacuity, but the theorem does not soundly bridge the real Python
  program because exact rational operations have a concrete false Python
  conclusion witness.
- Intent-adequacy gate: failed independently because finitely many fixed list
  sizes and shapes do not cover the unrestricted “at least two elements”
  contract.
- Evidence gate: the recorded rebuild, differential, pinning, body mutation,
  and false-postcondition mutation are reproducible, but finite evidence cannot
  cure either failure.

The clean `#Top` is legitimate only for the narrow idealized claims. It is not
a legitimate partial-correctness proof of the real generated program over the
HumanEval source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
