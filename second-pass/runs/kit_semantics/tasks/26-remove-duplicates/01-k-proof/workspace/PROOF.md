VALIDATED

# What is proven

Under the supplied MPY semantics, for every finite `ValSeq INPUT` satisfying
`allInts(INPUT)`, loading the translated `remove_duplicates` definition and
calling it on `list(INPUT)` reaches normal completion with:

- result value `ref(0)`;
- heap entry `0 |-> list(rdAcc(.ValSeq, INPUT, INPUT))`;
- `NoExc` and exit code `0`; and
- the module environment, empty call stack, and allocation counters in the
  final states stated by `SPEC.remove-duplicates`.

This is a partial-correctness reachability theorem. The Kit workflow does not
formally establish termination.

`rdAcc` is the order-preserving filter defined by:

```text
rdAcc(acc, [], all) = acc
rdAcc(acc, v :: rest, all) =
  rdAcc(acc ++ [v], rest, all)  if count(all, v) == 1
  rdAcc(acc,        rest, all)  otherwise
```

Consequently, from an empty accumulator it contains exactly the original input
integers whose total input multiplicity is one, in their original order.

# Formal claims

`SPEC.remove-duplicates-loop` is the loop invariant. At a loop head it relates:

- `REST`, the unprocessed input suffix;
- `ACC`, the current contents of the result-list heap object;
- `ALL`, the unchanged complete input used by `list.count`; and
- the final heap content `rdAcc(ACC, REST, ALL)`.

It quantifies over the same arbitrary continuation admitted by its `<k> ...`
frame. It observes the exact local bindings for `numbers` and `result`, permits
only the intentionally unobserved final value of local `number` to be
existential, and preserves all framed configuration cells.

`SPEC.remove-duplicates` starts with the complete translated module and an
initial MPY configuration. It executes module loading, exact closure creation,
argument binding, the function body, the loop, return, and frame cleanup.

# Proof-extension inventory

## `allInts`

- **Class:** Definitional summary.
- **Semantic role:** Precondition predicate only; it does not rewrite `<k>` or
  replace execution.
- **Domain:** Every `ValSeq`.
- **Matched context / state footprint:** Pure term context; reads and writes no
  configuration cells.
- **Equations:** Empty and `vCons` cases are exhaustive and disjoint. Recursion
  strictly descends through the tail.
- **Value influence:** Restricts both claims to the prompt's `List[int]`
  domain.
- **Justification:** `true` on empty and `isInt(head) and allInts(tail)` on a
  nonempty sequence.
- **Dependents:** Both claims.

## `rdAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical output without replacing any
  program term.
- **Domain:** Every accumulator, remaining sequence, and original sequence of
  sort `ValSeq`; the claims use it only under `allInts`.
- **Matched context / state footprint:** Pure term context; reads and writes no
  configuration cells.
- **Equations:** Empty and `vCons` cases are exhaustive and disjoint. The
  nonempty case contains one total Boolean conditional. Recursion strictly
  descends through `REST`.
- **Value influence:** Determines the claimed final result-list contents.
- **Value justification:** Its equation uses the supplied, defined
  `cntOccVS(ALL, V)` and appends `V` exactly when that count is one.
- **Dependents:** The loop and entry claims.

## `SPEC.remove-duplicates-loop`

- **Class:** Derived lemma / auxiliary reachability claim.
- **Semantic role:** Machine-checked fixed-semantics execution theorem used as
  the loop circularity; it is not an ordinary operational rule.
- **Domain:** `allInts(REST) andBool allInts(ALL)`, arbitrary result prefix
  `ACC`, heap location `H`, environment `L`, and current local `number`.
- **Matched context:** The exact `#loop` term and exact loop body, an arbitrary
  continuation quantified by the claim itself, the three relevant local
  bindings, the result heap object, and framed remaining cells.
- **Context containment:** The theorem proves the same framed continuation and
  configuration domain that the circularity accepts; it does not generalize an
  exact-suffix theorem to a wider suffix.
- **State footprint:** Reads `numbers`, `result`, `number`, and heap `H`; writes
  local `number` and heap `H`; preserves the input, environment, continuation,
  and every other framed cell.
- **Value influence:** Establishes the exact final result-list value.
- **Justification:** Fixed semantics executes the base case and one inductive
  iteration; recursive loop heads close coinductively. The focused proof printed
  `#Top`.
- **Control/value validation:** `spec-body-mutation.k` changes the comparison
  from count one to count two while retaining the original destination. It is
  rejected with a count-one residual.
- **Dependents:** `SPEC.remove-duplicates`.

There are no proof-local operational bridges, opaque result oracles, trusted
primitives, priority rules, concrete rules, or simplification lemmas.

# Reproduction commands and actual results

The exact runnable sequence is in `prove.sh`; its complete captured output is
in `prove-run.out`. The final end-to-end run exited `0`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 differential_test.py
```

Actual differential output:

```text
differential cases: 21531
mismatches: 0
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual results: both commands exited `0`. `krun` ended with `.K`, `NoExc`, and
`<exit-code> 0 </exit-code>` after five assertions. LLVM compilation emitted
only the warnings preserved in `prove-run.out`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.remove-duplicates-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive-proof outputs:

```text
#Top
#Top
```

All three commands exited `0`. The full, unfiltered `kprove` command is the
required positive target proof and proves every claim together, allowing the
entry claim to use the loop circularity. A diagnostic entry-only filtered run
was stopped because filtering out the invariant also removes the circularity;
it is not a required positive command and is not in `prove.sh`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both expected-failure probes exited `1` with `WarnStuckClaimState`.
`spec-vacuity.k` claimed that `[1]` returns `[]`; its residual contained the
actual heap `list(vCons(1, .ValSeq))`. `spec-body-mutation.k` changed the body
to retain count-two values; its residual included
`1 #Equals cntOccVS(ALL, V)` and the unmet append/result equality.

Artifact hashes from the validated run:

```text
2027484c70ffdeea2438b727ef88e50eb76b60470bb1b8d9f4adad1aaaa70af7  solution.py
0a1f3742d1a9870e83de95c510044b37d3cf3899be7c16f12e61b33bea7360de  solution.mpy
2ebd91be3260fa3cba17758d13378ea24b6a0ef9af9871d92cb84f352ffec089  verification.k
e123630fd45d0e74d2386de04b1426429c1681a6a25502f43350c0a81a87b3ba  spec.k
895c4da675e82b53e9944c51bac39550c9a687d414453795afa685bc9707feda  prove.sh
```

# Gate results

## Gate A — PASS

- **A1:** The entry claim contains the same constructor-level body as
  `solution.mpy`; all program-defined code executes under fixed semantics.
  The count-two body mutation invalidates the loop theorem.
- **A2:** No operational bridge skips state. The claims account for result
  allocation, heap append updates, scope changes, return state, call stack,
  exceptions, and exit code.
- **A3:** Module and local bindings, callee/argument evaluation, loop control,
  method dispatch, return, and frame cleanup execute under the supplied rules.
  The loop theorem quantifies over exactly the continuation it accepts.
- **A4:** The two proof-local functions have exhaustive, nonoverlapping,
  descending equations. No false global equation or opaque value is present.
- **A5:** `[1]` is a realizable `allInts` witness. The false `[]`
  postcondition is rejected and exposes the actual `[1]` result.

## Gate B — PASS

- **B1:** `allInts(INPUT)` matches `List[int]`; no length, sign, distinctness,
  or magnitude restriction is added.
- **B2:** For this domain the supplied model uses unbounded integers, integer
  equality, finite list order, `count`, and `append` consistently with the
  relevant Python behavior. The input is represented as the semantics'
  documented unboxed read-only list value; this function never mutates it.
- **B3:** The `rdAcc` equations are the keep-exactly-once, original-order
  property itself, not an opaque execution summary.
- **B4:** The implementation and property align formally and in all recorded
  concrete tests.

## Gate C — PASS

- **C1:** The trust ledger below names all components outside the theorem and
  their effects.
- **C2:** `smoke.py`, `smoke.mpy`, `differential_test.py`,
  `spec-vacuity.k`, `spec-body-mutation.k`, `prove.sh`, and
  `prove-run.out` exist and reproduce the reported evidence.
- **C3:** Formal results, finite evidence, trust assumptions, and exclusions
  are separated here. `#Top` is reported only as proof execution, not by
  itself as validation.

# Trust boundary

| Component | Why outside the theorem | Effects and dependents | Evidence |
|---|---|---|---|
| Supplied `py2mpy.py` | Translation correctness is an input assumption | Connects `solution.py` syntax to `solution.mpy`; affects program identity | Deterministic regeneration in `prove.sh`; generated constructor body was inspected against `spec.k` |
| Supplied `MPY` modules, especially core/functions/call/controls/list/methods/int | They are the fixed language model requested by the task | Define binding, control, heap, `count`, integer equality, append, return, and thus both claims | Concrete LLVM smoke run; body and false-result mutations; source audit |
| K v7.1.293 Haskell backend and solver | Proof-checker implementation is below the theorem | Determines `#Top` and rejection of mutations | Exact versions checked; reproducible positive and negative runs |
| MPY-to-CPython adequacy on `List[int]` | The K proof is about the supplied semantics, not a formal refinement of CPython | Affects the human-facing interpretation | Independent `Counter` oracle on 19,531 exhaustive and 2,000 deterministic random cases, zero mismatches |

No proof result is conditional on an unproved proof-local primitive.

# Empirical evidence

`smoke.py` runs the empty list, singleton, prompt example, all-duplicate, and
negative/zero/mixed-multiplicity cases through LLVM `krun`.

`differential_test.py` uses `collections.Counter`, independently of
`list.count` and `rdAcc`. It checks every sequence of lengths 0 through 6 over
`{-2,-1,0,1,2}` (19,531 cases), then 2,000 deterministic random integer lists
of lengths 0 through 40 over `[-100,100]`. It found zero mismatches. These are
finite adequacy observations, not a universal proof.

# Excluded behavior

- Inputs containing non-integers, nested heap objects, or aliases are outside
  `allInts`.
- Equivalence of the supplied reference semantics and all of CPython is not
  formally proved.
- Termination, performance, and resource bounds are not formal conclusions of
  this partial-correctness proof.
- Python behaviors absent from the supplied subset, including unrelated
  exceptions and reflection, are not claimed.
