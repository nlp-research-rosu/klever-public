VALIDATED

## What is proven

Under the supplied MPY semantics, `is_bored` returns the number of sentences
whose first word is `I`, for every finite symbolic MPY string. Sentences are
delimited by `.`, `?`, or `!`; leading modeled whitespace is ignored; and `I`
is a word when followed by modeled whitespace, a delimiter, or end-of-input.

This is a partial-correctness reachability theorem. It is not a separate
termination proof.

## Formal claim

`SPEC.is-bored` starts from the exact `is_bored` closure, exact translated
body, argument `str(IS:IntSeq)`, caller scope, empty heap, and empty stack. It
reaches:

```k
boredoms(IS)
```

`IS` has no length bound: it is an arbitrary finite `IntSeq`. `boredoms`
folds the complete sequence through the state `(count, at_start, pending_i)`.
`LOOP-SPEC.loop` is the bridge-free coinductive proof of that fold over the
exact recurring loop head and actual combined `If; Return` statement suffix.

The KORE parses of `solution.mpy` and `proof-program.mpy` are byte-identical
after macro expansion (`cmp` exit 0), establishing that the body in the proof
is the body generated from `solution.py`.

## Proof-extension inventory

### Program-body macros

`BORED-LOOP-BODY` and `BORED-FUNCTION-BODY` are parse-time representation
aliases for `solution.mpy`. They replace no execution, read or write no cell,
and affect no value. `kast` plus `cmp` validates their exact expansion.

### Definitional summaries

`isDelimiter`, `flag`, `charIsWhitespace`, `charIsI`, `scanStep`, `scan`,
`finishScan`, `scanResult`, and `boredoms` are definitional summaries.

- Their context is purely mathematical; they do not match an MPY computation.
- `isDelimiter` covers the three delimiter codes and their disjoint
  complement.
- `charIsWhitespace` and `charIsI` use complementary, exhaustive guards.
- `flag` covers both Booleans.
- `scanStep` is one total nested conditional.
- `scan` descends structurally from `iCons(C, REST)` to `REST`.
- These symbols influence the claimed result, and their exhaustive equations
  fix that result rather than leaving an oracle.

### One-character strip comparison bridges

The two priority-40 rules in `verification-base.k` replace only the exact
expressions:

```k
Compare(Call(Attribute(Name("c"), "strip"), .Exprs), CmpOp("==", Str("")))
Compare(Call(Attribute(Name("c"), "strip"), .Exprs), CmpOp("!=", Str("")))
```

Their matched context pins environment `1`, the complete local map, and
`c = str(iCons(C, .IntSeq))`; the continuation and unrelated scopes/cells are
framed and preserved. The skipped fixed execution performs local lookup,
bound-method creation, zero-argument call dispatch, pure strip, and comparison.
It writes no state and has no modeled exceptional or control effect on this
domain.

`CONNECTION-SPEC` proves both operators under the exhaustive partitions
`isWSC(C)` and `notBool isWSC(C)`, using `connection.k`, which imports only
the fixed MPY semantics and does not import either bridge. Thus all accepted
bindings, values, continuations, and state frames lie inside the connection
theorem.

### Loop bridge

The rule in `verification.k` replaces the exact loop head, exact
`BORED-LOOP-BODY`, actual combined `If; Return` `Stmts` suffix, and `#endcall`.
It also pins:

- environment `1 => 0`;
- the exact module binding and local scope, while preserving arbitrary scope
  `B` at `-1`;
- scope location `2 => 1`;
- empty heap and heap location `0`;
- the exact `.K` caller frame, popped to an empty stack;
- `noRet`, `NoExc`, and exit code `0`.

`LOOP-SPEC.loop` proves this complete match domain in
`verification-base-kompiled`, which does not import the loop bridge. That proof
does depend on the independently connected strip bridges. The bridge therefore
preserves returned value, bindings, control, stack, scope removal, heap,
exception state, and exit state over every configuration it accepts.

## Commands and actual results

The complete reproducible command sequence is in `prove.sh`; `./prove.sh`
exited 0. Important positive commands were:

```bash
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
# Exit: 0; final <k> .K and <exit-code> 0

kompile --backend haskell connection.k \
  --main-module CONNECTION --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
# Output: #Top   Exit: 0

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove loop-spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
# Output: #Top   Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
# Output: #Top   Exit: 0
```

The proof logs `connection-proof.out`, `loop-proof.out`, and
`target-proof.out` each contain `#Top`.

Negative checks:

```text
spec-vacuity.k:                exit 1, WarnStuckClaimState
mutation-spec.k:               exit 1, WarnStuckClaimState
connection-mutation-spec.k:    exit 1, WarnStuckClaimState
```

The first changes the result to `boredoms(IS) +Int 1`; the residual contains
the rejected equality `finishScan(...) +Int 1 == finishScan(...)`. The second
replaces the loop body with an empty body. The third changes `strip` to
`upper`; on a space character fixed execution reaches `false`, not the claimed
`true`.

The toolchain was K `v7.1.293`.

## Gate results

- Gate A — PASS. Exact program KORE identity holds. Every operational bridge
  has a bridge-free universal connection theorem over its complete match
  domain. Equations are exhaustive, disjoint where guarded, and structurally
  descending. Empty input is a realizable witness. Result, body, and
  connection mutations are all rejected.
- Gate B — PASS. The theorem covers every finite MPY `IntSeq`, not bounded
  lengths. Its scanner-state meaning is exactly the prompt property under the
  supplied delimiter and whitespace model. `solution.py` uses Python
  `strip()`, so the implementation itself follows Python whitespace behavior.
- Gate C — PASS. Commands, outputs, negative probes, identity evidence,
  differential evidence, and the fixed-model boundary are reproducible and
  explicitly separated below.

## Trust boundary

The theorem is conditional on the supplied reference semantics, K frontend,
Haskell backend, and their built-in integer, Boolean, string, map, and
reachability machinery. No program-defined operation is left opaque, and no
unproved result-bearing oracle is introduced.

The supplied MPY `isWSC` recognizes only codes 32, 9, 10, and 13, whereas
CPython `str.strip()` recognizes additional whitespace. This is witnessed by
`"I\vwork"`:

```text
CPython solution.py result: 1
MPY model-boundary.mpy result: 0, krun exit 0
```

Thus the K theorem is about all values of the supplied model, while equivalence
to CPython on additional Unicode/ASCII whitespace remains conditional on this
documented model boundary. No input length or MPY-representable code is removed
from the formal theorem.

## Empirical evidence

`differential.py` compares the state-machine implementation with an independent
sentence-split/word-split oracle. It checks the prompt examples, all strings of
length 0 through 5 over an eight-character boundary alphabet, and 5,000
deterministic random strings including non-ASCII and additional whitespace:

```text
differential cases=42456 mismatches=0
```

`smoke.py` also executes under the required LLVM definition and covers empty or
ordinary sentences, multiple delimiter kinds, leading modeled whitespace,
standalone `I`, `Idea`, and a later non-leading `I`.

These finite checks support intent and model adequacy; the universal result is
established by the K claims, not by testing.

## Excluded behavior

Non-string arguments are outside the prompt’s stated input type. Total
correctness/termination and fidelity outside the supplied MPY model are not
claimed. The K theorem has no finite-length, fixed-example, or bounded-unrolling
restriction.
