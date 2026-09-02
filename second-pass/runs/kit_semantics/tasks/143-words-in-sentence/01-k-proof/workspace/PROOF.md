VALIDATED

# What is proven

Under the supplied `MPY` reference semantics, `solution.mpy` is partially
correct for every modeled string `str(CS)` whose length is between 1 and 100.
If the call terminates, it returns the words whose lengths are prime, in their
original order, separated by one ASCII space.

The proof executes the program-defined function body. It does not replace the
call, the loop, tuple membership, `len`, string concatenation, `strip`, return,
or frame cleanup with an operational rewrite.

# Formal claim

The whole-program claim starts in the reference initial configuration with:

```k
#loadAll(#solutionModule)
~> Call(Name("words_in_sentence"), str(CS))
```

and proves that the final computation is:

```k
str(sentenceResult(CS))
```

under:

```k
1 <=Int isLen(CS) andBool isLen(CS) <=Int 100
```

`sentenceResult` is an exact recursive fold:

- code `32` terminates the current word;
- every other code extends the current word;
- `emitWord` retains a word exactly when its length is one of
  `2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
  67, 71, 73, 79, 83, 89, 97`;
- retained words preserve encounter order; and
- the final reference-semantics `strip` removes the accumulator's trailing
  separator.

The theorem's modeled-string domain is stronger than the prompt's
letters-and-spaces restriction: the claim permits any `IntSeq` codes but uses
only code `32` as a separator. The length restriction exactly matches the
prompt.

The auxiliary `scan-loop` claim proves the loop base and inductive cases. It
tracks all three locals changed by the loop:

```text
result -> scanOutput(remaining, word, result)
word   -> scanWord(remaining, word)
char   -> scanLast(remaining, char)
```

The simultaneous full proof uses this claim to discharge the loop in the
whole-program claim.

# Proof-extension inventory

## Exact program macros

`#primeTuple`, `#emitSelected`, `#maybeEmit`, `#scanBody`, `#wordsBody`, and
`#solutionModule` are compile-time macros. They do not rewrite runtime
configurations. Their expansion is byte-identical KORE to the K parser's result
for `solution.mpy`.

- Class: syntactic aliases, not semantic proof extensions.
- Domain and matched context: only their exact displayed syntax.
- State footprint and value influence: none at runtime.
- Justification and validation: `kast --expand-macros` on both program forms
  followed by `cmp`; exit 0.
- Dependent claims: `scan-loop` and `words-in-sentence`.

## `primeLength`

Two `[simplification]` equations define `primeLength(N)` as true for the
displayed finite prime set and false for its complement.

- Class: definitional summary.
- Domain: every mathematical integer.
- Coverage and overlap: the guards are exact Boolean complements, so coverage
  is total and overlap is impossible.
- Matched context: the symbol only; no `<k>` or state cells are matched.
- State footprint: none.
- Value influence: selects whether `emitWord` appends a word and therefore
  affects the returned result.
- Value justification: the loop claim machine-checks the connection between
  the source tuple-membership execution and these equations on every integer.
  Trial-division differential tests independently check every possible word
  length 1 through 100.
- Dependents: `emitWord`, `scan-loop`, and `words-in-sentence`.
- Control validation: not applicable; no execution is replaced.

## `emitWord`

The single total equation returns the old accumulator for a non-prime word
length, or concatenates the word and one trailing space for a prime length.

- Class: definitional summary.
- Domain: every pair of `IntSeq` values.
- Coverage and overlap: one unguarded equation.
- Matched context and state footprint: a pure term; no runtime cell.
- Value influence: result accumulator and final postcondition.
- Value justification: definition plus the fixed-semantics inductive loop
  proof.
- Dependents: `scanOutput`, `sentenceResult`, and both claims.

## `scanOutput`, `scanWord`, and `scanLast`

These functions summarize the exact state transition of the character loop.

- Class: definitional summaries and derived simplification equations.
- Domain: all remaining, current-word, output, and prior-character `IntSeq`
  values.
- Coverage and overlap: empty versus `iCons`; the `scanOutput` and `scanWord`
  constructor cases split on `C == 32` versus `C =/= 32`. Those guards are
  disjoint and exhaustive.
- Descent: every recursive equation consumes the `R` tail of the remaining
  sequence.
- Matched context: pure summary terms only. They never match `<k>`, bindings,
  continuations, stacks, heaps, exceptions, or return state.
- State footprint: none directly; their values specify the exact final values
  of the loop's `result`, `word`, and `char` bindings.
- Value influence: `scanOutput` and `scanWord` determine the returned string;
  `scanLast` constrains the otherwise unobserved final local.
- Value justification: base/step definitions and the machine-checked
  `scan-loop` reachability claim over fixed execution.
- Dependents: `scan-loop`, `sentenceResult`, and `words-in-sentence`.

## `sentenceResult`

Its one total equation composes `scanOutput`, `scanWord`, the final
`emitWord`, and the exact reference `strip` functions `trimWS`/`revIS`.

- Class: definitional summary.
- Domain and coverage: every `IntSeq`, one unguarded equation.
- Matched context and state footprint: pure term only.
- Value influence: exact whole-program result.
- Value justification: definitions and the whole-program proof from the real
  loaded body.
- Dependent claim: `words-in-sentence`.

## `scan-loop` claim

This is the loop circularity and an auxiliary fixed-semantics execution
theorem.

- Class: derived reachability lemma.
- Matched context: the actual `#loop(str(CS), Name("char"), #scanBody)` at
  environment 1; the exact module, builtins, and local scopes; an empty heap;
  heap location 0; one function frame; `noRet`; `NoExc`; and exit code 0. The
  active continuation is framed and is preserved.
- Justification scope and containment: the claim is proved universally over
  its complete matched `CS`, local accumulator values, character value,
  continuation, and saved frame continuation. Every application in the entry
  claim has exactly that configuration.
- State footprint: it writes only the three local bindings named above and
  preserves the environment, module and builtin scopes, heap, allocation
  counters, stack, return state, exception state, exit code, and active
  continuation.
- Control and value validation: fixed semantics executes one loop iteration
  before the circularity recurs. The separator-body mutation changes code 32
  to code 120 and makes this proof fail with a stuck state.
- Dependent claim: `words-in-sentence`.

There are no proof-local operational bridges, priority rewrites, trusted
primitives, fresh opaque values, or result-bearing oracles.

# Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

It executes these relevant commands:

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_examples.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive results:

```text
LLVM kompile exit: 0
krun exit: 0
krun <exit-code>: 0
AST_IDENTITY: PASS
focused scan-loop kprove: #Top, exit 0
simultaneous full kprove: #Top, exit 0
```

The concrete K state contains:

```text
example_1       = "is"
example_2       = "go for"
boundary_prime  = "bb ccc eeeee"
boundary_nonprime = ""
```

The supplied semantics emits compiler warnings about unused variables and
non-exhaustive functions in unrelated semantic domains. Compilation and all
used executions exit 0.

Independent differential command and output:

```bash
python3 test_solution.py
```

```text
DIFFERENTIAL_CASES=6958
DIFFERENTIAL_MISMATCHES=0
```

False-postcondition mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

The mutation appends code 120 (`"x"`) to the required result.

```text
exit: 1
WarnStuckClaimState
```

A satisfiable witness is `"aa"`:
`CS = iCons(97, iCons(97, .IntSeq))`, whose length is 2.

Body-sensitivity mutation:

```bash
kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-kompiled
kprove spec-body-mutant.k \
  --definition verification-body-mutant-kompiled \
  --spec-module SPEC-BODY-MUTANT
```

The mutant emits `"x"` (code 120) instead of a space (code 32).

```text
kompile exit: 0
kprove exit: 1
WarnStuckClaimState
```

# Gate results

## Gate A — PASS

- A1: `solution.mpy` and `#solutionModule` have identical expanded KORE. The
  exact loaded function body executes. The separator-body mutation is rejected.
- A2: there is no operational bridge. The loop claim accounts for every cell
  used by the call and loop and exactly specifies all mutated locals.
- A3: the exact module closure binding, local frame, builtin `len` binding,
  evaluation order, continuation, return state, stack, and exception state are
  part of fixed execution. No abrupt effect is introduced by proof-local rules.
- A4: every proof-local equation is truthful on its complete domain. Guards
  are complementary or constructor-disjoint, totality is covered, and recursive
  summaries descend on an `IntSeq` tail.
- A5: the precondition has ground witnesses; the result is constrained; the
  false-postcondition mutation exits 1 with a stuck claim.

## Gate B — PASS

- Formal input: a modeled string of length 1 through 100. This includes the
  prompt's letters-and-spaces inputs.
- Observable state: the returned string. Function-local bindings are removed
  by the real return/frame-pop semantics; heap, exception, and exit state are
  also constrained.
- Intended property: retain exactly prime-length words, preserve their order,
  and separate them with one space.
- The finite set is exactly the primes possible for word lengths at most 100.
  Every possible single-word length is independently tested with a
  trial-division oracle.
- Both prompt examples match under CPython and the concrete K LLVM semantics.

## Gate C — PASS

- All named artifacts and commands exist in this directory.
- The exact end-to-end runner exits 0.
- The two positive proof commands print `#Top` and exit 0.
- Concrete LLVM assertions cover both prompt examples and prime/non-prime
  boundary behavior.
- The independent oracle uses trial division rather than the proof's finite
  prime equations. Its 6,958 cases include all lengths 1–100, every bounded
  two-word length pair, prompt/spacing boundaries, and 2,000 deterministic
  random strings; there are zero mismatches.
- Both required mutation styles are reproducible and rejected.

# Trust boundary

Formally established facts are conditional on:

1. the supplied, unmodified `reference-semantics/` definition;
2. the K parser/compiler, Haskell prover backend, LLVM runtime backend, and
   their underlying solvers/runtimes; and
3. the standard interpretation of `IntSeq` length and code 32 as a space in
   the supplied Python model.

No additional proof-local primitive is trusted. The adequacy fact that the
displayed finite set is exactly the primes at most 100 is independently
supported by trial division over every possible word length.

# Empirically supported facts

- CPython behavior agrees with an independent trial-division oracle on 6,958
  documented cases.
- Concrete LLVM K execution agrees on the two prompt examples and two boundary
  cases, with assertions and exit code 0.
- Parsed `solution.mpy` and the proof's exact program macro have identical
  expanded KORE.
- Changing either the required result or the executed body invalidates the
  proof.

These finite checks support intent and toolchain integration; they are not
used as substitutes for the universal K reachability proof.

# Excluded behavior

- The K claims establish partial correctness, not a separate liveness theorem.
- Non-string arguments and strings outside the prompt's length bound are not
  covered by the whole-program claim.
- Python behavior outside constructs modeled by the supplied reference
  semantics is not claimed.
- The source-level prompt's wording says “letters” while its examples contain
  spaces. The formal theorem treats code 32 as the separator and proves a
  superset of the stated letters-and-spaces inputs.
