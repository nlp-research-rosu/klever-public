VALIDATED

# Proof report

## What is proven

Under the supplied reference semantics, the exact translated module in
`solution.mpy` is loaded and `words_string` is called with
`str(CS)` for an arbitrary symbolic finite `CS:IntSeq`. If that execution
terminates, it returns `ref(0)`, whose heap object is exactly

```k
list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))
```

Thus every comma code (`44`) is changed to a space code (`32`), after which the
supplied whitespace-splitting definition returns the nonempty word tokens. The
claim is symbolic and unbounded; it is not a finite-size unrolling.

This is a partial-correctness theorem, as specified by the Kit workflow. It does
not separately prove termination.

## Formal claim and scope

The sole positive claim is `SPEC.words-string` in `spec.k`.

- Program boundary: `#loadAll` of the exact `Module(FuncDef(...))` generated
  from `solution.py`, followed by a call through the module binding.
- Input domain: every `CS:IntSeq`, with no length bound and no precondition.
  This includes the full prompt domain of finite strings whose words are
  separated by commas or spaces.
- Observable final state: `<k>` returns `ref(0)`; heap location `0` contains the
  result list; `<heapLoc>` is `1`; the module binding remains; the temporary
  call frame is gone; `<env>`, `<scopeLoc>`, `<stack>`, `<ret>`, `<exc>`, and
  `<exit-code>` are all constrained.
- Intended property: replace commas with spaces and split into nonempty words.

The final heap is closed rather than framed, so the theorem also establishes
that this invocation performs exactly the one result-list allocation from the
initial empty heap.

## Proof-extension inventory

The inventory is empty.

`verification.k` declares no syntax, function, equation, simplification rule,
operational rewrite, priority rule, trusted primitive, opaque term, or
auxiliary claim. It only imports the supplied `MPY` module. `spec.k` contains
the target claim and no proof-local rule.

`replaceC`, `splitWS`, `flushTok`, `seqConcat`, function lookup, method dispatch,
allocation, and return handling all come from the unmodified reference
semantics. They execute through fixed semantics; no rule intercepts or replaces
the candidate body. The negative claims in `spec-vacuity.k` and
`spec-body-mutation.k` are isolated validation probes and are not imported by
the positive proof.

## Exact commands and actual results

The complete reproducible runner is `./prove.sh`. It completed with exit code
`0`.

Translation and independent CPython differential test:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py
```

Actual result:

```text
CPYTHON_DIFFERENTIAL_OK cases=19614 mismatches=0
```

Concrete LLVM build and execution:

```bash
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both commands exited `0`. `krun` ended with `.K`, `NoExc`, and exit code `0`.
The smoke program checked both prompt examples, mixed/repeated separators,
leading/trailing whitespace, and the empty string. LLVM compilation emitted
non-exhaustiveness warnings for unrelated supplied functions; none is on the
`replace`/`split` execution path.

Symbolic Haskell build and positive target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target result:

```text
#Top
```

Both commands exited `0`. The compiler also reported only the supplied
`str.k` unused-variable warnings.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. For the realizable input
`""`, execution produced `0 |-> list(.ValSeq)`, rejecting the deliberately
false postcondition `0 |-> list(vCons(str(.IntSeq), .ValSeq))`.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. Replacing the body by
`return []` on input `"a"` produced an empty list and failed the original
one-word postcondition.

The toolchain reported K version `7.1.293`.

## Gate results

### Gate A — PASS

- A1: The claim loads the exact translated function body and fixed semantics
  performs lookup, argument binding, both method calls, return, and frame pop.
  The ground body mutation is rejected.
- A2: There is no operational bridge. The claim constrains the result, heap,
  allocation counter, binding, environments, call stack, return state,
  exception state, and exit code.
- A3: There is no shortcut around binding, evaluation order, continuation, or
  control transfer.
- A4: There are no proof-local equations, totality declarations, or opaque
  result symbols to audit.
- A5: The empty-string state is a satisfiable witness, and the false result
  mutation exits nonzero with the actual empty list visible in the residual.

### Gate B — PASS

The theorem is universal over finite `IntSeq` values and therefore is not
restricted to examples, lengths, or a bounded character count. On the prompt's
material domain—words separated by commas or ordinary spaces—the fixed
`replaceC` and `splitWS` equations state exactly the requested transformation.
The implementation matches the prompt and its examples.

The supplied model treats codes `32`, `9`, `10`, and `13` as whitespace,
whereas CPython's no-argument `str.split` recognizes additional Unicode
whitespace. This is an explicit reference-model boundary outside the prompt's
stated comma/space separator domain, not a bound introduced by the claim. The
candidate itself was also tested in CPython on broader whitespace.

### Gate C — PASS

The trust boundary is explicit and the evidence is reproducible. No
proof-local assumption contributes to closure. Universal proof relies on the
unmodified supplied semantics and the K prover; finite CPython and LLVM tests
are reported only as empirical validation, not as substitutes for the symbolic
claim. Both required negative probes exist, fail for the intended semantic
reason, and show their contradictory final heaps.

## Trust boundary

- Trusted fixed base: the read-only `reference-semantics/` files supplied by
  the task and K version `7.1.293`.
- The interpretation of `IntSeq` as Python text and the model's four-code
  whitespace predicate are reference-model choices.
- The theorem is partial correctness: termination is outside the reachability
  result.
- There are no added trusted primitives, operational bridges, derived lemmas,
  or definitional summaries.

## Empirically supported facts

`test_solution.py` uses an independently written character scanner as its
oracle. It checks the two prompt examples, boundary and broader-whitespace
cases, and every string of length zero through five over the seven-character
alphabet `aB0, \t\n`: 19,614 total comparisons and zero mismatches.

`smoke.py` independently checks four concrete cases through the LLVM reference
semantics. Its final configuration has `.K`, `NoExc`, and exit code `0`.
These are finite validation results; the unbounded result is supplied only by
`SPEC.words-string`.

## Excluded behavior

- Calls whose argument is not a modeled string are outside the prompt and the
  claim.
- Total termination, resource bounds, and CPython implementation details are
  not established.
- For characters outside the prompt's comma/ordinary-space separator contract,
  conclusions about exact CPython whitespace classification are conditional on
  the documented reference-model boundary.
