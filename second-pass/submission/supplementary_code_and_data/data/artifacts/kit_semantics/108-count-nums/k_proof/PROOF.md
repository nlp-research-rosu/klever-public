VALIDATED

## What is proven

Under the supplied MPY reference semantics, `count_nums` is partially correct
for every finite list whose elements are MPY integers.  The empty-list claim
returns `0`.  The symbolic nonempty claim covers an arbitrary integer head and
an arbitrary all-integer tail and returns `countNumsSpec` of the whole list.
`countNumsSpec` counts exactly those elements whose signed decimal digit sum is
positive, conditional on the named decimal-conversion contract in the trust
ledger below.

This is not a proof for finitely many selected lengths.  The outer invariant is
structural over an arbitrary `ValSeq`, and the inner invariant is structural
over an arbitrary `IntSeq` of decimal character codes.

## Formal claim

The two entry claims are:

- `SPEC.count-nums-empty`: the exact translated closure called on
  `list(.ValSeq)` reaches integer `0`.
- `SPEC.count-nums-nonempty`: for symbolic `I:Int` and `R:ValSeq`, with
  `allInts(R)`, the exact translated closure called on
  `list(vCons(I, R))` reaches `?RESULT:Int` and ensures
  `?RESULT ==Int countNumsSpec(vCons(I, R))`.

The proof also checks five supporting claims:

- `digit-loop`, an invariant for every remaining finite decimal-code sequence;
- `outer-loop-empty`, the recurrent base case with the exact return
  continuation and call frame;
- `outer-loop-step`, the recurrent case for one arbitrary integer head and an
  arbitrary all-integer tail;
- `call-setup-nonempty`, exact lookup, argument binding, frame creation, and
  `count = 0` initialization;
- `outer-loop-initial`, which connects that call state to the recurrent
  invariant.

All seven claims in `spec.k` are covered by the two positive `kprove` commands.

## Proof-extension inventory

The inventory below was rebuilt from the final `verification.k`, `spec.k`, and
`validation.k`.  Pure functions match only their displayed term in any
expression context, read no configuration cells, write no cells, and have no
control or exception effect.

| Extension | Class | Semantic role and complete domain | Matched context, containment, and state footprint | Value influence and value justification | Dependents and validation |
|---|---|---|---|---|---|
| `allInts` | Definitional summary | Total structural predicate on `.ValSeq` and `vCons(V,R)` | Pure term; constructor equations exhaust `ValSeq` | Restricts the target domain; each head uses fixed `isInt` | Nonempty outer and entry claims; arbitrary-tail proofs reached `#Top` |
| `definedProjectInt`, `projectIntTotal`, the `#Ceil` characterization, cast orientations, collapse, and idempotence | Derived lemma / definitional summary | Only projects `V:Val` when `isInt(V)`; otherwise no value-producing rule fires | Pure cast terms only; every use is under the same `isInt` guard; no evaluators manufacture an integer | Refines the fixed `Int < Val` subsort boundary and collapses to the original integer | Guarded dispatch twins and `countNumsSpec`; checked by both mutation probes |
| Guarded `applyCmp("<", V:Val, J:Int)` and `applyUn("-", V:Val)` twins | Derived lemmas | Exactly `isInt(V)`, which is the static match domain of the supplied `Int` equations | Arguments have already evaluated to values; the rules neither perform nor skip name lookup, binding, stack, heap, or control changes | RHSs are the supplied integer equations verbatim after the guarded projection: `<Int` and `0 -Int` | Negative branch and sign tests in the outer invariant; target proofs and body mutation |
| `magnitude` | Definitional summary | All integers, split by the disjoint and exhaustive guards `I < 0` and `I >= 0` | Pure term, no state | Exact absolute magnitude over mathematical integers | `signedDigitSum` and the source sign branches |
| `decimalCodes`, `strToCodes(Int2String(N)) => decimalCodes(N)`, and guarded `applyBuiltin("str", V, .Vals)` | Trusted primitive | Only nonnegative integers: `N >= 0`, or `isInt(V) and projectIntTotal(V) >= 0` | Matches the fixed builtin only after lookup and argument evaluation; no continuation or cells are changed.  Its domain is contained in the fixed integer-`str` rule and in the named primitive contract | Result-bearing: determines loop characters, branches, and final count. `decimalCodes(N)` is conditionally the exact finite ordinary ASCII base-10 representation returned by the supplied `Int2String/strToCodes` primitive | All digit, outer, and nonempty entry claims; supported by the supplied primitive equations, LLVM execution, and differential evidence; explicitly conditional |
| Structural `allDigitCodes` plus `allDigitCodes(decimalCodes(N)) => true` | Definitional summary plus trusted primitive fact | Constructor cases cover every `IntSeq`; trusted fact is guarded by `N >= 0` | Pure term; the trusted fact is no broader than the decimal primitive contract | Ensures each iterated one-character string is accepted by the fixed `int` builtin and represents a digit | `digit-loop`; concrete and differential decimal checks |
| `codeDigitSum` | Definitional summary | Total on both `IntSeq` constructors | Pure structural descent | Exact sum of `(code - 48)` | Inner invariant and `signedDigitSum` |
| `chooseFirst` | Definitional summary | Empty sequence, zero accumulator, and nonzero accumulator; guards are disjoint and exhaustive | Pure structural descent | Exact source accumulator: replace zero with the current digit, otherwise retain the first nonzero digit | Inner invariant and negative-number correction |
| `lastCode` | Definitional summary | Total structural recursion on `IntSeq` | Pure structural descent | Tracks the final `char`/`digit` locals after the inner loop | `digit-loop` post-state |
| `signedDigitSum` | Definitional summary | All integers, split by `< 0` and `>= 0` | Pure term | For negatives subtracts twice the first magnitude digit, turning its positive contribution into a negative one; for nonnegatives uses the ordinary sum. Human-facing decimal meaning is conditional on `decimalCodes` | `countNumsSpec` and the target postcondition |
| `countNumsSpec` | Definitional summary | Total on every `ValSeq`; integer and noninteger head guards are disjoint and exhaustive | Pure structural descent | Adds one exactly when `signedDigitSum(projectIntTotal(V)) > 0`; the noninteger totalization is unreachable under the target precondition | Outer invariants and nonempty target claim |
| `digit-loop` | Derived reachability lemma / circularity | Exact inner `#loop`, arbitrary finite `CS`, digit-code premise, and previous code in `[48,57]` | Reads and updates only the exact local bindings shown; preserves the symbolic stack and surrounding continuation; no abrupt control | Fixed MPY loop execution establishes the accumulator summaries | Proved `#Top`; used by outer claims |
| `outer-loop-empty` | Derived reachability lemma / circularity | Exact empty iterator, exact `Return(Name("count")) .Stmts ~> #endcall`, exact scope and single frame | Preserves root state, returns `C`, pops the exact call frame and local scope | Fixed MPY base-case, return, and frame-pop execution | Proved `#Top`; used by recurrent/entry reasoning |
| `outer-loop-step` | Derived reachability lemma / circularity | Exact nonempty iterator, `isInt(I)`, arbitrary `allInts(R)`, exact body and return continuation | Executes the body and inner loop, updates the listed locals/count, then follows the exact frame/return behavior | Establishes `C + countNumsSpec(vCons(I,R))` through the fixed body and recursive circularity | Proved `#Top`; body mutation is rejected |
| `call-setup-nonempty` | Derived reachability lemma | Exact closure body, call expression, root binding, argument list, and arbitrary all-integer tail | Reads the exact `count_nums` binding; creates scope `1`, binds `arr`, initializes `count`, and pushes the exact frame; does not summarize a result | RHS is the actual first outer-loop state, not an opaque program result | Proved `#Top`; connects the exact target closure to the invariant |
| `outer-loop-initial` | Derived reachability lemma | Exact first loop state with only `arr` and `count` locals and the exact return continuation/frame | Fixed body execution creates temporaries and eventually pops the exact scope/frame | Establishes the structural count summary from initial accumulator `C` | Proved `#Top`; used by the nonempty entry claim |
| `count-nums-empty`, `count-nums-nonempty` | Target reachability claims | Exact translated closure; empty or arbitrary finite all-integer list | Covers root scope, empty heap/stack, normal return, no exception, and exit code `0` | Constrains the returned integer to the stated result | Both proved `#Top`; false-result and body-mutation probes fail |

There is no rule that summarizes or replaces execution of the program-defined
`count_nums` body.  The exact closure body appears at the call boundary, and
the loop claims execute that body under the fixed semantics.  There is also no
fresh unconstrained result symbol: the only opaque value is the explicitly
trusted supplied decimal primitive.

Equation audit:

- Sign splits (`magnitude`, `signedDigitSum`) are disjoint and exhaustive.
- `chooseFirst` splits empty/cons and zero/nonzero accumulator cases
  exhaustively.
- `countNumsSpec` splits empty/cons and integer/noninteger heads exhaustively.
- Both guarded dispatch twins have exactly the fixed integer match domain.
- The `str` twin is narrowed to the reachable nonnegative domain; no false
  negative-integer case remains.
- Every structural recursive rule descends on its sequence tail.

## Exact commands and actual outputs

The complete reproducible command sequence is executable as:

```bash
./prove.sh
```

The significant commands actually run were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 concrete-tests.py
python3 differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.digit-loop,SPEC.outer-loop-empty,SPEC.outer-loop-step,SPEC.call-setup-nonempty,SPEC.outer-loop-initial,SPEC.count-nums-nonempty
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.count-nums-empty

kompile --backend haskell validation.k \
  --main-module VALIDATION \
  --syntax-module MPY-SYNTAX \
  --output-definition validation-kompiled
kprove spec-vacuity.k --definition validation-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition validation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

- Regenerating `solution.mpy` and comparing it to the delivered file:
  `TRANSLATION_MATCH_EXIT=0`.
- `python3 concrete-tests.py`: no assertion failure, exit `0`.
- `python3 differential_test.py`:
  `cases=12006 values=29719 mismatches=0 decimal_contract_failures=0`,
  exit `0`.
- LLVM `kompile`: exit `0`.
- `krun`: exit `0`, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`.
- Haskell `kompile` for `verification.k`: exit `0`; warnings were unused
  variables in the supplied read-only `str.k`.
- Six-claim nonempty/support `kprove`: `#Top`, exit `0`
  (`kprove-entry-nonempty.log`).
- Empty-entry `kprove`: `#Top`, exit `0`
  (`kprove-entry-empty.log`).
- Validation-definition `kompile`: exit `0`.
- False postcondition on witness `[11]`: exit `1`; residual result is `1`
  while the false target is `0` (`kprove-vacuity.log`).
- Mutated body (`count = 1`) on witness `[11]`: exit `1`; residual result is
  `2` while the old target is `1` (`kprove-body-mutation.log`).

The expected-failure commands are validation probes, not positive target-proof
commands.

## Gate results

### Gate A — PASS

- A1: the exact translated body executes through exact call setup, inner and
  outer loop claims, return continuation, and frame behavior. Changing the
  body initializer from `0` to `1` invalidates the old result (exit `1`,
  residual `2`).
- A2/A3: no program-body operational bridge exists. The dynamic-sort twins
  restate fixed integer equations after arguments have evaluated and affect no
  state or control. The supplied `str` primitive boundary affects only its
  returned value and is matched only after normal lookup/evaluation on a
  nonnegative integer.
- A4: guards, overlap, totality, descent, and the tightened nonnegative `str`
  domain pass the equation audit above.
- A5: `[11]` is a realizable witness. The genuine result is constrained to
  `1`; the false target `0` is rejected with exit `1`. All five auxiliary
  claims are included in the successful nonempty proof command.

### Gate B — PASS

The prompt requires an array of integers. The formal domain is every finite MPY
list containing only integers, including empty lists, arbitrary lengths, both
signs, zero, and unbounded mathematical integer magnitudes. The inner proof is
also unbounded in decimal length. No list-size, digit-count, magnitude, or
example-only restriction is present.

Relative to the named supplied decimal primitive contract,
`signedDigitSum` implements the prompt's rule that the first digit of a negative
number is signed negative. The implementation and specification agree on the
prompt examples and boundaries. Supplied-primitive opacity is a conditional
trust boundary, not candidate-domain narrowing.

### Gate C — PASS

Every unproved boundary and its value/control influence is listed below.
Concrete, differential, false-postcondition, and body-mutation artifacts and
commands exist in the workspace with actual outcomes recorded. Formal facts,
conditional conclusions, finite evidence, and exclusions are separated.

## Trust boundary

| Trusted component | Exact assumption and effect | Dependents | Evidence |
|---|---|---|---|
| Supplied `Int2String`/`strToCodes`; proof name `decimalCodes` and the guarded decimal rules | For every `N >= 0`, the fixed primitive returns the finite, nonempty ordinary ASCII base-10 digits of `N`, with `0` represented by code `48` and no sign/leading zeros. This value controls inner-loop iterations, sums, branches, and the returned count; it does not itself change state or control. | `allDigitCodes`, `digit-loop`, `signedDigitSum`, outer and nonempty entry claims | Exact fixed rule in `reference-semantics/semantics/builtins.k`, structural ASCII conversion in `str.k`, LLVM examples/boundaries, and the finite differential run |
| Supplied `py2mpy.py` translator | Its CPython-AST constructors faithfully represent the delivered `solution.py` in MPY. The theorem directly uses the resulting exact closure shape. | Program identity between Python source, `solution.mpy`, and `spec.k` | Regeneration/cmp exit `0`, concrete CPython checks, LLVM execution, and body-sensitive mutation |
| Supplied read-only MPY semantics and K toolchain/backend/solver | K's implementation and the supplied model correctly implement their documented reachability semantics. The theorem is formally about this model. | Every formal claim | Successful LLVM/Haskell compilation, concrete normal termination, and discriminating negative probes |

The human-facing statement “ordinary decimal digit sum” is conditional on the
first row. The K theorem unconditionally proves the surrounding program
structure and result relative to `decimalCodes`; finite evidence supports but
does not universally prove that external primitive contract.

## Empirically supported facts

- `concrete-tests.py` independently runs the Python implementation on all prompt
  examples plus `[-123, -100, -19, 0, 10, 99]`.
- `concrete-tests.mpy` runs those assertions under the LLVM-compiled supplied
  semantics and terminates normally.
- `differential_test.py` uses a separately written signed-string oracle. It
  covers the prompt/boundary cases, every singleton from `-5000` through
  `5000`, 2,000 deterministic random lists of lengths `0` through `20` with
  values up to `10^30` in magnitude, and very large decimal boundaries:
  12,006 cases and 29,719 values with zero mismatches.
- The same run checks that every tested nonnegative magnitude string is a
  nonempty sequence of decimal digits; zero contract failures occurred.
- The two K negative probes demonstrate postcondition sensitivity and
  program-body sensitivity on the realizable witness `[11]`.

These finite observations are evidence only; the universal result comes from
the symbolic claims, conditional on the trust ledger.

## Excluded behavior

- Lists containing nonintegers are outside the prompt's declared input domain
  and outside the target precondition.
- Infinite iterables and non-list iterables are outside the `array of integers`
  formalization used here.
- The Kit establishes partial correctness, not a separate total-correctness or
  resource-usage theorem.
- CPython implementation limits and behaviors absent from the supplied MPY
  model are not proved.
- The exact decimal conversion contract and translator/model correctness are
  trusted boundaries, not machine-checked universal theorems in this proof.
