VALIDATED

## What is proven

Under the supplied MPY semantics, the exact loaded closure for
`check_if_last_char_is_a_letter` has the following partial-correctness
property for every finite `IntSeq` string representation:

- the empty string returns `false`;
- a nonempty string whose final modeled character is not alphabetic returns
  `false`;
- a one-character alphabetic string returns `true`;
- a longer string with an alphabetic final character returns whether the
  immediately preceding character is code 32, the literal space.

The proof is not a finite collection of lengths. `IS:IntSeq` remains symbolic
and unbounded in all three target claims. The cases partition the full modeled
string domain by emptiness and the fixed semantics' alphabetic predicate.

This is a partial-correctness result in the Kit sense. The target is the
function call after module loading: its exact global binding, closure body,
argument, environment, stack, heap, return state, exception state, and exit
code are present in each claim. All program-defined operations execute through
the supplied semantics.

## Formal claim

The result is named by `standaloneLastLetter(IS)`:

1. `false` when `isLen(IS) ==Int 0`;
2. `false` when the length is positive and the final code is not `isAlphaC`;
3. `true` when the length is one and the sole code is `isAlphaC`;
4. for length greater than one with an alphabetic final code,
   `intSeqAt(IS, isLen(IS) -Int 2) ==Int 32`.

The three reachability claims in `spec.k` are:

- `target-empty`: `isLen(IS) ==Int 0`;
- `target-nonalpha`: positive length and a nonalphabetic final code;
- `target-alpha`: positive length and an alphabetic final code.

These preconditions are exhaustive because `IntSeq` is an algebraic finite
sequence, `isLen` is its structural nonnegative length, and `Bool` is
two-valued. The destination directly contains `standaloneLastLetter(IS)`,
avoiding an unnecessary partial-term equality wrapper.

Program scope: exact call of the target closure from its module-level binding.
Input domain: every `str(IS:IntSeq)` value in MPY. Observable final state: the
Boolean result and every MPY state cell; the claims require all non-result
cells to be preserved. Intended property: the final character is alphabetic
and is a one-character final space-delimited word.

## Proof-extension inventory

### `standaloneLastLetter`

- Extension: one `[function, total]` symbol with the four guarded equations
  listed above.
- Class: definitional summary.
- Semantic role: names the required result; it never matches a `<k>` term and
  never replaces program execution.
- Domain: all `IntSeq` terms. The four guards are pairwise disjoint and
  exhaustive: length zero; positive/nonalpha; length one/alpha; length greater
  than one/alpha.
- Matched context: only `standaloneLastLetter(IS)` as an equational term; no
  continuation, control stack, binding, or configuration cell is matched.
- Justification scope and containment: structural sequence length, in-bounds
  final/penultimate indexing, the supplied `isAlphaC`, and code 32 for literal
  space. Every equation's match is exactly its stated guard.
- State footprint: none.
- Value influence: the target destination result.
- Value justification: the guarded equations define the prompt predicate, and
  `target-empty`, `target-nonalpha`, and `target-alpha` are the bridge-free
  universal execution connection theorems for the complete partition.
- Dependents: all three target claims and the model-boundary witness.
- Control/value validation: no operational bridge exists. The positive claims
  print `#Top`; the false-result and changed-body probes are both rejected.

### Nonempty/empty constructor disjointness

- Extension:
  `iCons(C, REST) ==K .IntSeq => false [simplification]`.
- Class: derived lemma.
- Semantic role: simplifies the non-emptiness conjunct in the supplied
  `str.isalpha` equation; it does not replace execution.
- Domain and matched context: every integer head and `IntSeq` tail, in any
  equational context.
- Justification scope and containment: free-constructor disjointness between
  `iCons` and `.IntSeq`; the rule states exactly that domain.
- State footprint: none.
- Value influence: intermediate `isalpha` simplification and therefore the
  result.
- Value justification: constructor disjointness.
- Dependents: `target-nonalpha`, `target-alpha`, and the model-boundary claim.
- Validation: the full target proof passes, while both result and body
  mutations fail.

### Singleton constructor injectivity

- Extension:
  `iCons(C, .IntSeq) ==K iCons(D, .IntSeq) => C ==Int D
  [simplification]`.
- Class: derived lemma.
- Semantic role: normalizes equality of the one-character strings produced by
  indexing; it does not replace execution.
- Domain and matched context: all integer codes `C` and `D`, in any
  equational context.
- Justification scope and containment: injectivity of the same singleton
  constructor; the matched and justified domains coincide.
- State footprint: none.
- Value influence: the final comparison with the one-character space string.
- Value justification: constructor injectivity.
- Dependents: `target-alpha`.
- Validation: the universal target proof and the two negative probes.

There are no proof-local operational bridges, opaque result oracles, trusted
primitives, priority rules, concrete rules, or auxiliary circularities.

## Exact commands and actual outputs

The complete recorded run was:

```bash
./prove.sh > prove.log 2>&1
```

Actual exit: `0`. The complete 388-line stdout/stderr record is in
`prove.log`. The script ran these commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove spec-model-boundary.k \
  --definition verification-kompiled \
  --spec-module SPEC-MODEL-BOUNDARY
```

Actual relevant outputs and exits:

- both translations exited 0; `solution.mpy` SHA-256 is
  `d0a42ece2155635b68c0773c720a18ece548ce1a5dc07275f6350a8a3431717a`;
- LLVM compilation exited 0 with the supplied-semantics non-exhaustive-match
  warnings recorded in `prove.log`;
- `krun` exited 0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`;
- `python3 test_solution.py` exited 0 and printed exactly:

```text
differential cases: 9337
mismatches: 0
unicode witness 'é': solution=True, oracle=True
```

- Haskell compilation exited 0 with four unused-variable warnings from the
  supplied `str.k`;
- the required `kprove spec.k ...` command exited 0 and printed `#Top`;
- the model-boundary witness exited 0 and printed `#Top`.

The negative commands were:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

- the false-result mutation exited 1 with `WarnStuckClaimState`, residual
  `<k> false ~> .K </k>`, and the destination `true`;
- the changed-body mutation exited 1 with `WarnStuckClaimState`, residual
  `<k> true ~> .K </k>`, while the correct empty-input destination reduces to
  `false`.

`prove.sh` checks both nonzero exits and printed:

```text
EXPECTED FAILURE: false-result mutation was rejected
EXPECTED FAILURE: body mutation was rejected
```

## Gate results

### Gate A — PASS

- A1: each target claim starts with the exact global binding and exact closure
  body translated from `solution.py`; lookup, argument evaluation, binding,
  body execution, return, and frame cleanup use fixed semantics. Replacing the
  body by `return True` makes the empty-input connection fail.
- A2: no execution is bridged. The heap, heap location, scope location, stack,
  return state, exception state, environment, globals, and exit code are
  explicitly preserved.
- A3: there is no proof-local control rewrite or continuation frame. The
  supplied call/return semantics handles all control.
- A4: the summary equations are true on disjoint exhaustive guards; the two
  simplifications are free-constructor facts. No recursive descent or
  overlapping-equation issue exists.
- A5: `.IntSeq` is a satisfiable witness. Mutating its required result from
  `false` to `true` is rejected with the concrete residual `false`.

### Gate B — PASS

- B1: the theorem covers every finite MPY string, with no size bound. The
  three cases are exhaustive and the source contract asks for strings.
- B2: MPY's `Str` literal conversion and `isAlphaC` are ASCII-only, whereas
  CPython `str.isalpha()` recognizes Unicode letters. This is a supplied
  fixed-model boundary, not candidate-added narrowing. The theorem covers all
  `IntSeq` values under MPY. The checked code-point-233 witness returns `false`
  in MPY (`#Top`) while the real Python implementation and oracle return
  `True` for `"é"`.
- B3: the execution-to-summary connection is formally proved. The
  summary-to-prompt reading is direct: alphabetic final code plus either
  length one or literal-space predecessor.
- B4: the Python implementation uses `str.isalpha()` and a literal `" "`
  predecessor, matching the contract's alphabetic-character and
  space-separated-word language. Prompt examples all pass.

Gate B therefore passes relative to the required supplied-semantics boundary;
CPython Unicode behavior is separately validated but is not falsely claimed as
a theorem of the ASCII-only model.

### Gate C — PASS

Every artifact and command cited here exists, all output is preserved in
`prove.log`, and the trust boundary and finite nature of empirical evidence are
explicit. No unrecorded proof-local assumption affects the result.

## Trust boundary

- The supplied, unmodified `reference-semantics/` modules are trusted as the
  operational definition of MPY. All target claims depend on their call,
  string, indexing, Boolean, scope, and return rules.
- K v7.1.293, its LLVM/Haskell backends, and their solver/runtime are trusted
  to implement compilation, execution, and reachability checking.
- The ASCII-only `strToCodes`/`isAlphaC` behavior is a recorded fixed-model
  boundary. It affects alphabetic classification but does not narrow the
  symbolic MPY domain.
- No proof-local primitive or operational bridge is trusted.

## Empirically supported facts

- `smoke.py` begins with the exact contents of `solution.py`; this is checked
  by `test_solution.py`. LLVM `krun` executes eight assertions: all four prompt
  examples plus `"A"`, `"1"`, `"x Y"`, and `"xy"`.
- The independent oracle uses `txt.split(" ")[-1]`, checks that the final
  space-delimited word has length one, and then applies CPython `isalpha()`.
  It does not reuse the proof summary equations.
- Differential scope is every string of lengths 0 through 5 over
  `(" ", "a", "Z", "1", "!", "\t")`, plus six Unicode cases. There were 9,337
  comparisons and zero mismatches.
- These finite tests support implementation intent and the model-boundary
  analysis; they do not replace the universal K proof.

## Excluded behavior

- Non-string Python arguments are outside the prompt and the formal domain.
- CPython's Unicode alphabet tables are outside the supplied ASCII-only MPY
  model. The source implementation's Unicode behavior is tested, not formally
  derived from MPY.
- This report makes no claim about unrelated constructs that trigger the
  supplied semantics' compilation warnings.
- As required by the Kit, the theorem is reported as partial correctness, not
  as a separate liveness theorem.
