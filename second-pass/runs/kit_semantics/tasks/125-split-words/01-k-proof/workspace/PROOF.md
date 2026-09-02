VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `split_words` is partially
correct for every finite string represented by an arbitrary symbolic
`CS:IntSeq`. The proof is not a bounded unrolling. It executes the exact
translated function body through ordinary lookup, call, allocation, method,
branch, return, and frame-pop rules.

The four claims in `spec.k` exhaustively partition the model's string domain:

1. the empty string returns `0`;
2. a nonempty string whose whitespace split differs from `[txt]` returns that
   whitespace-split list;
3. a nonempty string with no modeled whitespace and at least one comma returns
   `txt.split(",")`;
4. a nonempty string with neither delimiter returns the number of occurrences
   of `b, d, f, h, j, l, n, p, r, t, v, x, z`.

The list-returning claims constrain both the returned reference and its exact
heap value. All claims also constrain the environment, scopes, scope
allocator, heap allocator, call stack, return state, and exception state.

## Formal claim

Let

```text
P(CS) = splitWS(CS, .IntSeq, .ValSeq)
S(CS) = vCons(str(CS), .ValSeq)
```

For all finite `CS:IntSeq`, the claims establish:

```text
CS = empty
  => result = 0

CS != empty and P(CS) != S(CS)
  => result points to list(P(CS))

CS != empty and P(CS) = S(CS) and strContains(",", CS)
  => result points to list(splitSep(CS, 44, .IntSeq))

CS != empty and P(CS) = S(CS) and not strContains(",", CS)
  => result = oddAlphabetCount(CS)
```

`oddAlphabetCount` is definitionally the sum of the supplied `cntSub`
function on the thirteen singleton code sequences 98, 100, ..., 122. Because
these are exactly `b, d, ..., z` and are pairwise distinct, it directly states
the requested count of lowercase letters with odd zero-based alphabet index.

The claims are partial-correctness reachability claims. They do not separately
prove termination, although the implementation contains no program loop and
the fixed string functions structurally recurse over finite sequences.

## Proof-extension inventory

The inventory was rebuilt from `verification.k` and `spec.k`. There are no
proof-local operational bridges, priority rules, simplification rules,
`[concrete]` rules, opaque symbols, or auxiliary circularity claims. The four
claims in `spec.k` are target goals and are not used as proof assumptions.

### `splitWordsBody`

- Extension: `syntax Stmts ::= "splitWordsBody" [function, total]` and its one
  unconditional equation.
- Class: definitional summary.
- Semantic role: names the exact `Stmts` tree generated for `split_words`; it
  does not replace execution. After expansion, the fixed semantics executes
  every program operation.
- Domain: the single nullary term `splitWordsBody`; the equation is
  unconditional, exhaustive, nonrecursive, and has no overlapping equation.
- Matched context: any occurrence of that proof-local `Stmts` constant. In the
  target claims it occurs only as the body of the exact
  `closureVal(("txt", .ParamNames), ..., 0)` bound to `"split_words"` in module
  scope 0.
- Justification scope: all occurrences of the nullary alias, so its match
  domain and definition domain coincide.
- Context containment: the equation merely expands an AST constant and makes
  no claim about a continuation, binding, or operational state.
- State footprint: none for the equation. The expanded body subsequently uses
  the fixed semantics, which reads/writes the cells constrained by the claims.
- Value influence: indirect influence on every returned value and list heap
  object because it is the program body.
- Value justification: constructor-for-constructor comparison with regenerated
  `solution.mpy`; the call, split, list construction, branches, thirteen
  `count` calls, and return expression agree.
- Justification: transparent syntactic abbreviation of the translated body.
- Dependents: all four claims in `SPEC`.
- Control validation: `smoke.mpy` executes the same translated body through all
  three result modes and terminates at `.K`; the `mutatedSplitWordsBody` probe
  replaces the count return with `0` and is rejected with residual result `0`
  instead of `3`.
- Value validation: the body mutation above and the independent differential
  test both discriminate its result.
- Validation: A1–A4 PASS; no displaced execution or opaque result exists.

### `oddAlphabetCount(CS)`

- Extension: `syntax Int ::= oddAlphabetCount(IntSeq) [function, total]` and
  its one unconditional equation.
- Class: definitional summary.
- Semantic role: names the mathematical count expression; it never rewrites a
  program expression or skips fixed execution.
- Domain: every `CS:IntSeq`; the equation is exhaustive, nonrecursive, and has
  no overlap.
- Matched context: any `oddAlphabetCount(CS)` term. In the proof it occurs only
  as the result in `split-words-count`.
- Justification scope: every `IntSeq`, identical to the match domain.
- Context containment: it is a pure value definition and accepts no
  continuation, control stack, binding, or framed state.
- State footprint: none.
- Value influence: the postcondition of `split-words-count`.
- Value justification: the equation is exactly the same left-associated sum
  of the same thirteen fixed-semantics `cntSub` computations reached by
  executing the program. Each singleton is one required odd-index lowercase
  ASCII letter.
- Justification: direct exhaustive definition of the contract's finite
  thirteen-letter predicate, not an assumed result theorem.
- Dependents: `SPEC.split-words-count`.
- Control validation: not applicable; the function does not affect execution.
- Value validation: `"abcdef"` evaluates to `3`; changing the expected result
  to `4` is rejected; 828 independent CPython/oracle comparisons have zero
  mismatches.
- Validation: A4–A5 and B3 PASS.

## Reproducible commands and actual results

The complete command record is executable as:

```bash
./prove.sh
```

It exited `0`. Its substantive commands and outputs were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Both exited `0`. The final regenerated `solution.mpy` SHA-256 is
`9ff948f61b7b9af0a06011f43d344b544d013e8f8c31fda72f15fc2e7727c944`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit: `0`. It emitted only warnings from the supplied reference definition.

```bash
krun smoke.mpy --definition runtime-kompiled
```

Exit: `0`. Relevant final output:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

```bash
python3 differential_test.py
```

Exit: `0`. Output:

```text
cases=828 mismatches=0
```

```bash
python3 -c 'from solution import split_words; print(repr(split_words("\v")))'
```

Exit: `0`. Output:

```text
[]
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both exited `0`. The target proof output was:

```text
#Top
```

A focused rerun explicitly naming all four required claims also exited `0` and
printed `#Top`:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.split-words-empty,SPEC.split-words-whitespace,SPEC.split-words-comma,SPEC.split-words-count
```

False-postcondition mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Exit: `1`, as expected. The stuck residual contained:

```text
<k> 3 ~> .K </k>
```

while the destination required `4`.

Material body mutation:

```bash
kompile --backend haskell mutation-verification.k \
  --main-module MUTATION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-verification-kompiled
kprove spec-body-mutation.k \
  --definition mutation-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Compilation exited `0`. The proof exited `1`, as expected. Its stuck residual
contained:

```text
<k> 0 ~> .K </k>
```

while the destination required `3`.

The K tools used were version `v7.1.293`.

## Gate results

### Gate A — PASS

- A1: the exact program-defined body executes under the fixed semantics. The
  material count-body mutation changes the result and invalidates the probe.
- A2: no operational bridge exists. Return values, allocated lists, heap
  locations, scopes, stack, return state, and exception state are constrained.
- A3: each claim pins the `"split_words"` binding to the exact closure in
  module scope 0 and uses ordinary callee lookup, argument evaluation, method
  dispatch, return, and frame restoration.
- A4: both proof-local functions have one unconditional, exhaustive,
  terminating equation. There are no overlaps or false off-domain rules.
- A5: satisfiable witnesses are `""`, `"Hello world!"`, `"Hello,world!"`, and
  `"abcdef"` for the four claims. The false result and body mutations both
  fail with discriminating residuals.

### Gate B — PASS

- B1: the four claims collectively cover every finite `IntSeq`; there is no
  size bound or example-only restriction.
- B2: the theorem covers every string value representable by the fixed model.
  The supplied `isWSC` recognizes only codes 9, 10, 13, and 32, while CPython
  also recognizes vertical tab (11) and other whitespace. This is a fixed-model
  boundary, not candidate domain narrowing. A concrete witness is `"\v"`:
  CPython `solution.py` returns `[]`, while the K smoke assertion confirms that
  the supplied model returns integer `0`. The theorem is therefore adequate
  conditionally on the supplied model's whitespace table.
- B3: `oddAlphabetCount` directly enumerates all and only the thirteen required
  odd zero-based lowercase alphabet positions; execution reaches the identical
  fixed `cntSub` sum.
- B4: the implementation follows delimiter precedence and the requested count.
  All prompt examples pass, and the independent oracle reports zero mismatches.

### Gate C — PASS

Every evidence artifact exists, every command is recorded in `prove.sh`, the
negative probes have their expected nonzero outcomes, and the fixed-model
boundary is explicit rather than presented as CPython equivalence.

## Trust boundary

| Component | Why outside the theorem | Influence | Dependents | Evidence |
|---|---|---|---|---|
| Supplied `reference-semantics/` | Fixed operational model mandated by the task | Value, control, allocation, state, exceptions | All four claims | LLVM smoke execution, symbolic proof, negative probes; whitespace divergence explicitly witnessed |
| Supplied `py2mpy.py` | Fixed AST translator mandated by the task | Program identity | All four claims | Reproducible regeneration of `solution.mpy`; exact body constructors embedded by `splitWordsBody` |
| K backend/toolchain v7.1.293 | Trusted proof checker/runtime implementation | Proof execution | All formal results | All builds and runs exit as recorded; target prints `#Top` |
| CPython `str.split` behavior | Intended-language adequacy oracle, not a K proof axiom | Whitespace classification | Gate B comparison only | Vertical-tab witness and independent differential oracle |

There are no additional trusted proof-local primitives.

## Empirically supported facts

- `differential_test.py` uses an independently written oracle based on
  `any(char.isspace())`, `str.split`, comma precedence, and per-character
  membership in `"bdfhjlnprtvxz"`. It checks the examples, explicit boundaries,
  and every string of lengths 1–3 over a nine-character alphabet including
  comma, space, tab, vertical tab, and non-ASCII characters: 828 cases, zero
  mismatches.
- `smoke.mpy` exercises whitespace-list, comma-list, integer-count, empty,
  empty-token, and reference-model vertical-tab behavior under LLVM.
- These finite tests support implementation intent and model-boundary
  documentation; the unbounded K claims, not the tests, establish the formal
  target theorem.

## Excluded or conditional behavior

- Non-string arguments are outside the prompt's stated input contract.
- The result is conditional on the supplied reference semantics. In
  particular, its four-code whitespace table is not claimed to equal
  CPython's full Unicode whitespace classification.
- As a reachability proof, the formal result is partial correctness rather
  than a separate total-correctness theorem.
