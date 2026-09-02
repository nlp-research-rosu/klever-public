VALIDATED

## What is proven

Under the supplied `MPY` semantics, calling the exact translated
`count_upper` closure on any `str(CODES:IntSeq)` returns
`countUpperEven(CODES)`. This is a partial-correctness theorem: every terminating
execution from the stated call configuration has that result.

`countUpperEven` examines the first character, adds one exactly when that
one-character string occurs in `"AEIOU"`, removes the first two characters, and
repeats. It therefore denotes the number of uppercase vowels at offsets
0, 2, 4, and so on.

## Formal claims and scope

- Program boundary: `SPEC.count-upper` starts at
  `Call(Name("count_upper"), str(CODES))`. The module binding is pinned to the
  exact parameter list and translated function body from `solution.mpy`, so
  fixed semantics performs name lookup, argument evaluation and binding,
  function-frame creation, every body statement, return, and frame teardown.
- Input domain: every value of the supplied semantics' `str(IntSeq)` type.
  Non-string Python values are excluded.
- Observable final state: the returned integer. The claim also fixes the
  module and builtins scopes, empty heap and stack, environment, return and
  exception cells, allocation counters, and exit code; they are restored or
  preserved as shown in `spec.k`.
- Loop claim: `SPEC.loop-invariant` starts at the exact internal `#while` term
  and exact ordinary function frame. From accumulator `ACC` and remaining codes
  `CODES`, it empties `remaining` and changes `count` to
  `ACC +Int countUpperEven(CODES)`.

## Proof-extension inventory

### `countUpperEven` declaration and equations

- Class: definitional summary.
- Semantic role: names the result; it does not rewrite or replace a Python
  program term.
- Domain: all `IntSeq`. The base equation matches `.IntSeq`; the step equation
  is guarded by `notBool (CODES ==K .IntSeq)`. The cases are disjoint and
  exhaustive.
- Matched context and justification scope: occurrences of
  `countUpperEven(CODES)` in proof terms, under exactly the two equation
  domains. No continuation, binding, control stack, or state cell is matched.
  The equation domain and justification domain are identical.
- State footprint: none.
- Value influence: fixes the loop accumulator and target claim's return value.
- Value justification: the step uses the same supplied operations reached by
  execution: `intSeqAt(CODES, 0)`, membership through `strContains`, and the
  `[2:]` suffix through `buildIS`, `clampHi`, and `isLen`. The recursive
  argument is shorter by one or two elements, so the definition terminates.
- Justification and dependents: a direct recursive definition of the requested
  count; both claims depend on it. `SPEC.count-upper` is the universal
  fixed-semantics connection theorem from the exact invocation to this value.
- Control validation: not applicable because no execution is intercepted.
- Value validation: fixed-semantics concrete witnesses produce 0, 1, and 3;
  the opposite result 0 for `"aBCdEf"` is rejected with a residual result of 1.
- Validation: equation coverage, disjointness, defined indexing on the
  nonempty case, and recursive descent were audited.

### Integer right-association simplification

- Extension: `(A +Int B) +Int C => A +Int (B +Int C)`.
- Class: derived lemma.
- Semantic role: normalizes a proof-side integer expression; it does not match
  Python syntax or an operational configuration.
- Domain and context: all mathematical integers, in any simplifier context.
  The justification is equally universal, so context containment is exact.
- State footprint and control influence: none.
- Value influence and justification: preserves the integer value by
  associativity. Its one-way right-associated form terminates and has no
  competing local equation.
- Dependents: the inductive loop obligation and, transitively, the entry claim.
- Validation: the source and target are equal for all integers; no opaque value
  or execution step is introduced.

### `SPEC.loop-invariant`

- Class: derived reachability lemma used coinductively.
- Semantic role: proves the exact fixed-semantics behavior of the loop; it is a
  claim, not an operational rewrite added to `MPY`.
- Domain: all `ORIGINAL:IntSeq`, `CODES:IntSeq`, and `ACC:Int` in environment
  location 1, with the exact three-binding ordinary function frame and exact
  loop body shown in `spec.k`.
- Matched context: the claim universally frames the trailing `<k>`
  continuation, other scopes, and all omitted configuration cells. Its proved
  justification has that same universal framing, so no broader bridge context
  exists.
- State footprint: reads `remaining` and `count`; preserves `s`, environment,
  other scopes, heap, stack, return/exception state, and continuation; writes
  only `remaining` and `count`.
- Value and control influence: supplies the accumulated result and consumes the
  normally completing loop. The body contains no return, break, continue,
  exception-producing operation on the stated domain, allocation, or output.
- Justification: the empty-string branch is the base case. The nonempty branch
  adds the head's membership Boolean, assigns the `[2:]` suffix, and re-enters
  the same exact loop-head claim; the summary step and integer associativity
  close the inductive obligation.
- Dependents: `SPEC.count-upper`.
- Control/value validation: focused `kprove` returned `#Top`; LLVM runs covered
  zero and multiple iterations; the false-result and mutated-body probes were
  both rejected.

There are no proof-local operational bridges, opaque result oracles, trusted
primitives, priority rules, or concrete-only rules.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh > prove.log 2>&1
```

It exited 0. `prove.sh` contains the exact translation, identity, CPython,
LLVM, Haskell, proof, and negative-probe commands. The actual log is
`prove.log`; its key outputs were:

```text
SOLUTION_TRANSLATION_MATCH=PASS
CONCRETE_HARNESS_BODY_MATCH=PASS
SPEC_PROGRAM_IDENTITY=PASS
CPYTHON_CONCRETE_ASSERTS=5 PASS
cases=177161
mismatches=0
KRUN_SOLUTION_LOAD=PASS
KRUN_CONCRETE_ASSERTS=5 PASS
#Top
KPROVE_LOOP_INVARIANT=PASS
#Top
KPROVE_ALL_CLAIMS=PASS
EXPECTED FAILURE: false-result mutation rejected
EXPECTED FAILURE: mutated body rejected
```

The positive proof commands were:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both `kprove` commands printed `#Top` and exited 0. The LLVM build used
`--main-module MPY-KRUN --syntax-module MPY-SYNTAX`; both `krun` executions
ended with `.K`, `NoExc`, exit code 0.

The two negative commands exited 1 as required. Each printed
`WarnStuckClaimState`; each residual contained `<k> 1 ~> .K </k>` while its
destination required 0. Compiler warnings in `prove.log` concern supplied,
unchanged reference rules (unused `strLt` variables and concrete-backend
coverage in unrelated helpers); no warning occurred in a proof-local rule.

## Gate results

### Gate A — PASS

- A1: `solution.py` regenerates byte-identical `solution.mpy`.
  `identity_test.py` checks that `SPEC.count-upper` contains exactly that
  translated parameter list and body. The target executes the exact closure
  under fixed semantics. Changing `count = 0` to `count = 1` in
  `spec-body-mutation.k` makes the expected zero result fail.
- A2: no operational bridge exists. The target claim includes the relevant
  environment, scopes, allocation, heap, stack, return, exception, and exit
  cells. The loop claim changes only its two declared local bindings.
- A3: fixed `MPY` rules perform lookup, argument evaluation/binding, ordered
  statement execution, return, and frame restoration. No local rule pins or
  skips a binding or control action.
- A4: the summary cases are exhaustive, disjoint, defined, and decreasing.
  The only algebra lemma is globally valid and one-way terminating.
- A5: `"aBCdEf"` is a realizable witness with result 1. The false result 0 was
  rejected. Empty, zero-result, one-result, and three-result executions were
  also exercised.

### Gate B — PASS

- The formal domain is precisely string values, matching the prompt's input
  type; no hidden length, ASCII-input, or nonempty restriction is imposed.
- `IntSeq` is the supplied string representation. Symbolic inputs can contain
  arbitrary integer codes, covering all valid Python Unicode code points (and
  a harmless superset). The only source literal is ASCII `"AEIOU"`.
- The summary's head/member/drop-two recursion is exactly the human-facing
  property "uppercase vowels in even indices." The universal K claim connects
  execution to that definition, and the prompt's three examples agree.
- The implementation and the intended property align.

### Gate C — PASS

- The trust ledger below names every unproved boundary and its effect.
- Every claimed identity check, concrete run, differential test, proof, and
  mutation has an existing artifact, exact command in `prove.sh`, actual output
  in `prove.log`, and recorded result.
- Formal conclusions, finite evidence, trust assumptions, and excluded
  behavior are separated in this report.

## Trust boundary

- Supplied `reference-semantics/semantics.k` and its imported `MPY` modules:
  fixed and read-only by task stipulation. They determine value, control, state,
  call, string, indexing, slicing, comparison, and loop behavior; both formal
  claims depend on them. LLVM execution supplies independent finite evidence
  for the exercised paths but does not prove the semantics correct with
  respect to CPython.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and host runtime:
  trusted proof infrastructure. All proof results depend on it.
- `py2mpy.py`: supplied fixed source-to-constructor translator. It affects the
  source/program identity boundary. Regeneration equality plus
  `identity_test.py` checks the exact artifact and exact body used by the claim;
  the theorem does not prove the translator correct in general.

No external primitive, opaque value, or unproved program helper is trusted by
this proof.

## Empirically supported facts

- `concrete_tests.py` runs the three prompt examples, the empty boundary, and
  `"AEIOU"` under CPython and the LLVM semantics. All five assertions pass.
  The harness body is checked against `solution.py`.
- `differential_test.py` uses an independently structured
  `enumerate`/modulo/sum oracle. It exhaustively checks all strings of lengths
  0 through 5 over `AEIOUaeiouZ`, then adds the three prompt examples and two
  Unicode cases: 177,161 cases and zero mismatches.
- These finite tests support adequacy and implementation identity; they are not
  used as a universal proof.

## Excluded behavior

- Inputs that are not Python strings.
- Total correctness/termination as a K liveness theorem. The code decreases the
  remaining string by two characters each iteration, but the reachability
  claims establish partial correctness.
- A proof that the supplied MPY semantics, translator, K implementation, or SMT
  solver is correct with respect to CPython.
- Concrete `.mpy` literal loading beyond the supplied ASCII literal model.
  This does not restrict the symbolic `str(IntSeq)` input theorem; Unicode
  behavior is additionally checked only as finite CPython evidence.
