VALIDATED

# Proof report

## What is proved

`solution.py` implements `anti_shuffle(s)` by scanning the input once at the
outer level, maintaining the current word in sorted order by insertion. A
literal space (code point 32) terminates the current word and is copied to the
output. Thus every maximal space-delimited word has its characters sorted in
ascending Python/K string order, while every separator and its position among
the words is preserved.

The required target theorem is symbolic over `INPUT:IntSeq`. It therefore
covers every finite string represented by the supplied semantics, with no
bound on input length, number or length of words, number of spaces, or
character code values. The K claims establish partial correctness under the
supplied reference semantics.

## Formal claims

`spec.k` contains three reachability claims, all proved together:

1. `anti-shuffle-inner-loop` summarizes one invocation of the inner insertion
   loop for arbitrary `W:IntSeq`, inserted character `C:Int`, accumulated
   prefix `N:IntSeq`, insertion flag `I:Bool`, surrounding continuation
   `K:K`, and stack `STACK:List`.
2. `anti-shuffle-outer-loop` summarizes the outer scan for arbitrary remaining
   input `S:IntSeq`, completed result `R:IntSeq`, and current word `W:IntSeq`.
3. `anti-shuffle` loads the exact generated module, resolves and calls
   `anti_shuffle`, and proves that arbitrary `INPUT:IntSeq` returns
   `str(antiGo(INPUT, .IntSeq, .IntSeq))`.

The recursive mathematical summaries in `verification.k` are:

- `insertGo(W, C, N, I)`: scan `W`, copy every old character, and insert `C`
  immediately before the first strictly greater character, or append it if no
  such character exists.
- `antiGo(S, R, W)`: scan `S`; on code point 32 append `W` and one space to
  `R` and reset `W`; otherwise replace `W` with
  `insertGo(W, C, .IntSeq, false)`. At end, append `W`.

Starting each word with `.IntSeq`, structural induction on the equations for
`insertGo` shows that each consumed character is inserted exactly once,
existing characters are copied exactly once, and the result is ascending.
Structural induction on `antiGo` then shows that non-space characters are
partitioned into the same words, each word is sorted, and every literal space
is copied exactly once in its original separator position. This is the full
HumanEval contract, including empty strings and repeated, leading, and
trailing spaces.

## Proof-extension inventory

| Extension | Kind and domain | Coverage / overlap | State and control effect | Value influence | Connection to fixed semantics |
|---|---|---|---|---|---|
| `solutionModule()`, `solutionBody()` | Generated, zero-argument definitional aliases for the complete translated program and function body | Exact single definitions | None; syntax construction only | Selects the actual program executed by the entry theorem | `generate_program_module.py` derives them from `solution.py` through the fixed `py2mpy.py` translator; the entry claim executes them through the supplied loader and call rules |
| `antiInnerBody()`, `antiPostInsert()`, `antiOuterBody()`, `antiTail()` | Definitional aliases for exact AST subterms | Exact single definitions | None; syntax construction only | Identify loop heads and residual statements used in auxiliary claims | Their expansions are the generated program subterms; fixed MPY rules perform all execution |
| `insertGo(IntSeq, Int, IntSeq, Bool)` | Total definitional summary | Empty/cons cases are exhaustive and disjoint; recursion decreases the first `IntSeq`; the conditional partitions all Boolean/order cases | None | Computes the claimed post-loop locals | `anti-shuffle-inner-loop` proves fixed-semantics execution from the exact inner-loop head to those locals for arbitrary symbolic inputs and framed continuation |
| `antiGo(IntSeq, IntSeq, IntSeq)` | Total definitional summary | Empty/cons cases are exhaustive and disjoint; recursion decreases the first `IntSeq`; `C ==Int 32` and its complement partition the cons case | None | Computes the target return value | `anti-shuffle-outer-loop` and `anti-shuffle` prove fixed-semantics execution agrees with it for arbitrary symbolic inputs |
| `strLt(iCons(C,.IntSeq), iCons(D,.IntSeq)) => C <Int D` | Derived simplification lemma on singleton-character strings | Domain is exactly the singleton strings produced by string iteration; less/greater/equal cases are exhaustive and disjoint | None | Determines the insertion branch condition | `lemma-spec.k`, compiled against the unextended reference definition, proves all three order cases with `#Top` |
| Inner and outer loop claims | Auxiliary circularity reachability theorems | Symbolic and unbounded over every loop input/state parameter shown above | The inner claim frames arbitrary continuation and stack; the outer claim checks the exact return/pop configuration | Establish the two summaries used by the entry proof | They are K claims, not operational rewrites; both close under the fixed semantics |

There are no operational bridge rules, trusted primitives, opaque evaluators,
host-language calls, or axioms that replace program execution. The only
executable extension rule is the independently proved singleton `strLt`
simplifier. The other additions are constructors, equations for specification
functions, or proof claims.

## Exact commands and observed outcomes

The complete reproducible command sequence is recorded in `prove.sh`. The
principal commands and observations were:

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 generate_program_module.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove lemma-spec.k --definition lemma-kompiled --spec-module LEMMA-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

python3 test_solution.py
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
./mutation-probe.sh
```

Observed results:

- K version: `v7.1.293`.
- LLVM compilation exited 0. Concrete `krun` exited 0 with final
  `<k> .K </k>` and `<exit-code> 0 </exit-code>`.
- The bridge-free `lemma-spec.k` proof printed `#Top` and exited 0. Its three
  guarded claims cover singleton characters that are less, greater, or equal.
- The required `spec.k` command printed `#Top` and exited 0, proving all three
  claims in one invocation.
- Independent differential testing reported
  `differential_cases=5847 mismatches=0`.
- The deliberately false whole-program claim in `spec-vacuity.k` exited 1
  with `WarnStuckClaimState`; its empty-input witness returned the correct
  empty sequence rather than the claimed sequence with an extra character.
- `mutation-probe.sh` changed the generated function body to append `"X"`,
  regenerated the program term, and observed the target proof fail as
  expected. The wrapper exited 0 with
  `EXPECTED FAILURE: generated-body mutation invalidated the proof`.
- The complete `./prove.sh` run exited 0. Compiler messages were warnings from
  the supplied semantics, not proof failures.

## Gate results

### Gate A — proof-mechanism soundness: PASS

- **A1, body connection:** the target starts with the exact mechanically
  generated module, uses the supplied module loader/name lookup/call
  machinery, and reaches the generated function body. A body-only mutation
  invalidates the proof.
- **A2, state and control connection:** no extension performs Python
  execution. Claims expose the relevant `<k>`, environment, scopes, heap,
  heap-location, call stack, return, exception, and exit cells. Heap remains
  empty for this allocation-free implementation, and returns pass through the
  fixed call/return rules.
- **A3, primitive and dispatch connection:** loading, dispatch, binding,
  iteration, assignment, comparison, and return are executed by the supplied
  MPY semantics. The sole comparison simplifier is independently proved
  against that unextended semantics.
- **A4, equation discipline:** specification equations are total,
  structurally decreasing, and split into disjoint empty/cons and Boolean
  cases. No competing overlaps choose incompatible results.
- **A5, vacuity resistance:** the empty-input false-target probe fails, and a
  generated-body semantic mutation also fails.

### Gate B — theorem relevance to the full contract: PASS

- The entry claim is unbounded over every finite `IntSeq`; there is no finite
  test-size assumption or loop unrolling bound.
- The postcondition is the exact recursive meaning of sorting each
  space-delimited word and preserving every literal space.
- Empty input, one or many words, already sorted and reverse-sorted words,
  duplicate characters, punctuation, mixed case, and repeated/edge spaces are
  all included symbolically.
- The symbolic theorem imposes no character-code restriction. The supplied
  concrete source-string parser has an ASCII-oriented literal boundary, but
  that parser limitation is not a precondition of the symbolic `INPUT:IntSeq`
  theorem. Independent CPython tests include non-ASCII strings.

### Gate C — validation strength: PASS

- The independent oracle uses Python's `split(" ")`, per-word `sorted`, and
  `join`, rather than either K summary function. It checked all strings of
  length at most five over `" aB!z"`, the prompt examples and edge cases, and
  2,000 deterministic randomized ASCII/Unicode strings.
- A false postcondition and a source-body mutation both fail, demonstrating
  that the positive proof is neither vacuous nor detached from the submitted
  implementation.
- The comparison extension is validated separately against the frozen
  semantics in all order cases.

## Trust boundary

The trusted base is the supplied `reference-semantics/`, K's generated proof
machinery and backends, the K toolchain itself, and the fixed `py2mpy.py`
translation scheme. `generate_program_module.py` only packages that
translator's output as named K syntax aliases; the mutation probe audits that
the resulting body remains proof-relevant.

No proof-local function is treated as a trusted implementation of the Python
program. `insertGo` and `antiGo` are specification functions whose agreement
with actual MPY execution is proved by the reachability claims. The report
does not claim correctness of the reference semantics relative to all of
CPython, nor total correctness/termination beyond the partial-correctness
meaning of the K reachability proof.

## Empirically supported facts

The executable implementation matches the independent CPython oracle on 5,847
cases, including the original examples, whitespace edge cases, mixed
punctuation/case, duplicate characters, and Unicode samples. Concrete LLVM
execution of translated assertions also succeeds. These checks support the
model boundary and implementation intent; the unbounded coverage statement
comes from the symbolic theorem, not from testing.

## Excluded behavior

The HumanEval signature and contract require a string input. Behavior for
non-string Python objects is outside the theorem. The proof treats a separator
as the literal space character only; tabs and newlines are ordinary sortable
word characters, matching the contract's wording and examples. Exceptions,
resource exhaustion, implementation-defined Unicode collation beyond
code-point ordering, and equivalence of the supplied partial MPY semantics to
full CPython are not claimed.
