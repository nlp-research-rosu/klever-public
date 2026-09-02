VALIDATED

# Proof report

## What is proven

Under the supplied `MPY` reference semantics, the translated implementation

```python
def strlen(string: str) -> int:
    return len(string)
```

is partially correct for every model string `str(CS)` whose character-code
sequence `CS` is any finite `IntSeq`. If the exact function definition is
loaded and called in the pinned initial environment, the call returns
`isLen(CS)`, leaves no exception, and leaves exit code 0. The supplied
definition of `isLen` is:

```k
isLen(.IntSeq)                => 0
isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

Thus the result is the number of sequence elements. This is a partial
correctness result; it is not a separate liveness or resource-bound theorem.

## Formal claim and validation scope

The single positive target claim is `SPEC.strlen` in `spec.k`.

- Program boundary: exact module loading of the `FuncDef` in `solution.mpy`,
  followed by `Call(Name("strlen"), (str(CS), .Exprs))`. The program-defined
  body executes through the fixed call, frame, lookup, return, and pop rules.
- Input domain: `string` is a model string `str(CS)` for arbitrary finite
  `CS:IntSeq`. Non-string values and alternate initial bindings are excluded.
- Observable final state: the `<k>` result is exactly `isLen(CS)`; `<exc>` is
  `NoExc`; `<exit-code>` is 0. Environment, scope allocation, heap, stack, and
  return cells are also pinned, including the exact final module closure.
- Intended property: return the number of characters in the supplied string.

The module scope begins empty, the builtin scope is exactly `builtinsScope`,
and module loading binds `"strlen"` to the exact closure body. Consequently,
both the `strlen` binding and the `len` binding are fixed by the claim.

## Proof-extension inventory

There are no proof extensions.

`verification.k` only imports the supplied `MPY` module. It declares no local
syntax, function, totality attribute, equation, simplification rule, ordinary
rewrite, priority rule, operational bridge, trusted primitive, or opaque
symbol. `spec.k` contains only the positive target claim; it contains no
auxiliary circularity or lemma. The two negative-probe claims live in separate
modules and are not imported by the positive proof.

The relevant fixed-semantic path is:

1. module loading and fixed function-call/frame rules execute the exact body;
2. lookup selects `builtinV("len")` from `builtinsScope`;
3. `applyBuiltin("len", str(CS), .Vals)` reduces through `seqLen(str(CS))`;
4. `seqLen(str(CS))` reduces to `isLen(CS)`.

The two fixed `isLen` equations are constructor-disjoint, exhaustive over
`IntSeq`, and structurally decreasing. They are part of the supplied semantics,
not a proof-local summary or execution replacement.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 concrete-tests.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

The last two commands are wrapped by `prove.sh` so their expected non-zero
statuses are checked rather than treated as script failures.

Actual final reproducibility run:

```text
./prove.sh > proof-run.log 2>&1
Exit: 0
```

Key actual outputs:

```text
krun concrete-tests.mpy:
  <k> .K </k>
  <exc> NoExc </exc>
  <exit-code> 0 </exit-code>
Exit: 0

kprove spec.k:
  #Top
Exit: 0

kprove spec-vacuity.k:
  Warning (WarnStuckClaimState)
  residual <k> 0 ~> .K </k>, mutated destination 1
  [Error] Prover: backend terminated because the configuration cannot be
  rewritten further.
Exit: 1 (expected)

kprove spec-body-mutation.k:
  Warning (WarnStuckClaimState)
  residual <k> 0 ~> .K </k>, original destination
  isLen(iCons(97, .IntSeq)) = 1
  [Error] Prover: backend terminated because the configuration cannot be
  rewritten further.
Exit: 1 (expected)
```

The complete unabridged compiler, execution, proof, and mutation output is
preserved in `proof-run.log`.

Both kompilers exited 0. The supplied semantics emitted unused-variable
warnings in `strLt`. The LLVM build additionally emitted non-exhaustive-match
warnings for `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. None of those symbols is reachable on the fixed `strlen`/`len`
execution path; the warnings are nevertheless retained in `proof-run.log`.

## Gate results

### Gate A — PASS

- A1, identity and body sensitivity: `solution.mpy` is exactly regenerated by
  `python3 py2mpy.py solution.py`; the claim repeats that exact `FuncDef`,
  parameter, and `Return(Call(Name("len"), Name("string")))` body. No rule
  summarizes the program-defined function. Changing the body to `return 0`
  makes the one-character witness proof fail with residual result 0 versus
  required result 1 (`spec-body-mutation.k`, exit 1).
- A2, operational state: no operational bridge exists. Fixed semantics creates
  and pops the call frame. The claim pins the environment, module and builtin
  scopes, scope allocator, empty heap, heap allocator, empty stack, return
  state, exception state, and exit code.
- A3, binding/evaluation/control: the initial scope fixes `"strlen"` to the
  loaded exact closure and fixes `"len"` through `builtinsScope`. The supplied
  callee and argument rules evaluate the lookup and argument before dispatch;
  supplied return/pop rules restore the caller.
- A4, equations: there are no proof-local equations. The relevant fixed
  `isLen` cases are disjoint, exhaustive, and descending.
- A5, non-vacuity: `CS = .IntSeq` is realizable and the concrete empty-string
  example returns 0. Mutating its required result to 1 is rejected with a
  stuck state at 0 (`spec-vacuity.k`, exit 1).

### Gate B — PASS

- The prompt requests the length of a string; the formal result counts exactly
  the elements of its finite string code sequence.
- The prompt examples `"" -> 0` and `"abc" -> 3` pass under CPython and the
  LLVM reference semantics.
- The model theorem admits arbitrary integer code elements, which is broader
  than valid Python Unicode scalar values and therefore does not exclude any
  intended Python string. The symbolic result depends only on sequence shape.
- Concrete `Str` literal construction in the supplied semantics is ASCII-only.
  This does not narrow the symbolic input claim, which starts with `str(CS)`,
  but it is an excluded concrete-front-end behavior rather than a claim about
  full CPython Unicode decoding.

### Gate C — PASS

- Every local and imported dependency relevant to the proof is identified
  below.
- All claimed evidence has an existing artifact, exact command, oracle, input
  scope, and recorded result.
- Formal proof, fixed-semantics trust, finite tests, and excluded behaviors are
  stated separately.

## Trust boundary

| Component | Why outside this theorem | Effect and dependents | Evidence |
|---|---|---|---|
| Supplied `reference-semantics/semantics.k`, especially module loading, lookup, call/frame/return rules and `applyBuiltin`/`seqLen`/`isLen` | The task fixes this as the reference operational semantics; the target theorem executes under it rather than proving the semantics itself | Determines binding, control, state, exceptions, and the returned value of `SPEC.strlen` | LLVM execution, universal Haskell proof, false-result probe, and body mutation probe |
| Supplied `py2mpy.py` mappings for `FunctionDef`, `Return`, `Call`, and `Name` | Translation correctness is outside the K reachability claim | Establishes that `solution.mpy` represents `solution.py` | Exact regeneration command; regenerated output matches the checked artifact |
| K v7.1.293 compiler, LLVM backend, Haskell backend, and prover implementation | Tool implementation is the proof engine, not a theorem proved here | All executions and proof outcomes | Versions were checked; `prove.sh` reran from translation through all probes with exit 0 |
| CPython 3 used for finite source-level tests | Independent execution evidence only | Supports implementation-to-prompt alignment, not universal K closure | `python3 concrete-tests.py`, exit 0 |

There is no problem-local trusted primitive and no problem-local abstraction
whose value affects the result.

## Empirically supported facts

`concrete-tests.py` uses the exact implementation and checks:

```text
""           -> 0
"abc"        -> 3
"a b"        -> 3
"0123456789" -> 10
```

`python3 concrete-tests.py` exited 0. Translating the same artifact and running
it with the LLVM `MPY-KRUN` definition reached `.K`, `NoExc`, and exit code 0.
These are finite tests. Universal closure for arbitrary `CS:IntSeq` comes from
the positive `kprove` result, not from these examples.

The false-postcondition and body-mutation artifacts are negative validation
evidence. Their expected non-zero results do not count as positive target
proof commands.

## Excluded behavior

- Inputs that are not model strings and calls made in environments where
  `strlen` or `len` has a different binding.
- CPython behavior outside the supplied subset, including full concrete
  non-ASCII literal decoding and unmodeled exceptions.
- A proof of the supplied translator, reference semantics, K implementation,
  total correctness, termination bounds, or performance.
- Any claim that `#Top` by itself validates intent; the `VALIDATED` headline
  follows the separate Gate A, Gate B, and Gate C audit above.
