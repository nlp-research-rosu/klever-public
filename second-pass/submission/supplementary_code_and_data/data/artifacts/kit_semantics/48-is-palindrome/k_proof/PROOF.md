VALIDATED

# What is proven

Under the supplied `MPY` semantics, the claim `SPEC.is-palindrome` proves the
following partial-correctness property for every symbolic `S:IntSeq`:

1. Start with the semantics' exact initial configuration.
2. Load the constructor translation of `solution.py`.
3. Resolve `is_palindrome` through the module environment, call its real
   program-defined closure with `str(S)`, and execute its body.
4. Store the returned value in the harness variable `__result`.
5. Terminate with

   ```k
   __result |-> (S ==K buildIS(S, isLen(S) -Int 1, -1, -1))
   ```

The supplied slice rules define that `buildIS` term as the input sequence
visited from its final index down to index zero. Thus the result is true exactly
when the modeled string equals its reversal. The claim also fixes the final
environment, scopes, scope allocator, heap, heap allocator, call stack, return
state, exception state, and exit code; the call cannot satisfy the theorem by
silently changing another modeled cell.

This is a reachability/partial-correctness theorem in the model. It is not a
claim that the K semantics, translator, or proof engine are themselves proven
correct.

# Formal claim

The only positive target claim is `SPEC.is-palindrome` in `spec.k`. Its domain
is every value of the semantic string form `str(S:IntSeq)`. It excludes
non-string inputs, matching the prompt's annotated `text: str` contract.

The claim starts with:

```k
#loadAll(
  Module(
    FuncDef("is_palindrome", Params("text"),
      Return(
        Compare(
          Name("text"),
          CmpOp("==",
            Subscript(
              Name("text"),
              Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
    Assign(
      Name("__result"),
      Call(Name("is_palindrome"), str(S:IntSeq)))))
```

This is the constructor tree in `solution.mpy`, followed only by the result
assignment used to observe the call. The destination requires `.K`, the exact
reversal-equality result, restored call state, `NoExc`, and exit code zero.
There are no loops, so the Kit workflow requires no loop-invariant claim.

# Proof-extension inventory

The inventory was rebuilt from the actual proof files with:

```bash
rg -n "^(module|  imports|  syntax|  rule|  claim|requires)|\\[(function|total|simplification|concrete|priority)" verification.k spec.k
```

Actual result:

```text
spec.k:1:requires "verification.k"
spec.k:3:module SPEC
spec.k:4:  imports VERIFICATION
spec.k:6:  claim [is-palindrome]:
verification.k:1:requires "reference-semantics/semantics.k"
verification.k:3:module VERIFICATION
verification.k:4:  imports MPY
```

There are no proof-local functions, equations, simplification rules,
operational rewrites, priorities, auxiliary claims, trusted primitives, or
opaque result symbols. Consequently, there is no proof extension to classify
as a definitional summary, derived lemma, operational bridge, or trusted
primitive, and no extension record with a widened context or state footprint.

`isLen`, `buildIS`, `intSeqAt`, `slStart`, `slStop`, and `slStep` are part of
the supplied fixed semantics. They are not additions in `verification.k`.
`SPEC.is-palindrome` is the target theorem itself and is not used as a
circularity.

# Exact commands and actual outputs

Tool versions:

```text
kompile/krun/kprove: K v7.1.293, build Fri Oct 03 13:32:35 CDT 2025
python3: Python 3.10.12
```

Translation and syntax check:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py py2mpy.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
```

All three commands exited 0.

Concrete LLVM build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Both commands exited 0. `krun` ended with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. The LLVM build printed
non-fatal warnings from the supplied semantics about several unrelated
non-exhaustive helper matches and unused `strLt` variables.

Independent CPython differential test:

```bash
python3 differential-test.py
```

Actual output and exit:

```text
cases=1369 mismatches=0
Exit: 0
```

Symbolic Haskell build and the sole positive target-proof command:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof output and exit:

```text
#Top
Exit: 0
```

The Haskell build and proof also printed only the supplied `strLt` unused
variable warnings.

A5 false-result mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
WarnStuckClaimState
reached: __result |-> true
required: __result |-> false
Exit: 1
```

A1 material-body mutation:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both copies of the function body in that claim use `Return(Bool(false))`, so
the destination closure still matches the mutated body. Actual result:

```text
WarnStuckClaimState
reached: __result |-> false
required: __result |-> true
Exit: 1
```

The full recorded run was:

```bash
./prove.sh > prove-run.out 2>&1
```

It exited 0. `prove-run.out` contains the concrete final configuration, the
`cases=1369 mismatches=0` line, the positive `#Top`, both stuck mutation
states, and both `EXPECTED FAILURE` confirmations.

# Gate results

## Gate A — PASS

- **A1 program identity and body sensitivity:** The claim embeds the translated
  function body and executes it through `FuncDef`, module name lookup,
  `closureVal`, argument binding, `Return`, and frame pop. There is no rule that
  replaces the function call. The material `return False` mutation exits 1 and
  reaches the wrong result.
- **A2 operational-state preservation:** There are no operational bridges. The
  claim explicitly constrains every configuration cell in the supplied
  semantics and observes the added module binding and result binding.
- **A3 binding, evaluation, and control fidelity:** Fixed semantics performs
  lookup of `is_palindrome` and `text`, evaluates the slice before comparison,
  and performs the normal return/pop sequence. No proof rule pins a binding or
  discards a continuation.
- **A4 consistency and rule validity:** No proof-local equations or rules exist,
  so there are no coverage, overlap, totality, priority, or simplification
  obligations introduced by this proof.
- **A5 result constraint and non-vacuity:** The empty string is a realizable
  witness, exercised concretely. The false postcondition for that witness is
  rejected with exit 1 and a residual showing actual `true` versus required
  `false`.

## Gate B — PASS

- **B1 input-domain alignment:** The formal input is a semantic string
  `str(S:IntSeq)`, matching the prompt's `str` domain. Non-string behavior is
  intentionally outside the theorem.
- **B2 language-model adequacy:** For the operations used here, the supplied
  model evaluates string equality and the `[::-1]` slice over sequences of
  integer character codes. Python's full object model, Unicode storage details,
  and exceptions outside the typed domain are not modeled. These differences
  do not change equality-with-reversal for an in-domain string.
- **B3 summary-to-property adequacy:** There is no proof-local summary. The
  postcondition uses the fixed slice semantics directly:
  `buildIS(S, isLen(S)-1, -1, -1)`. Inspection of the supplied equations shows
  decreasing indices from the last element to the first. This interpretation
  remains conditional on adequacy of the supplied reference semantics and is
  empirically supported, not a separate metatheorem about CPython.
- **B4 implementation-to-intent alignment:** The implementation returns
  equality with the reversed text, which is the prompt's palindrome predicate.
  All supplied examples agree.

## Gate C — PASS

The proof command, negative probes, concrete K artifact, differential artifact,
tool versions, output log, input scopes, oracles, and exit statuses are all
recorded and reproducible. Formal, conditional, empirical, and excluded claims
are separated below.

# Trust boundary

| Unproved component | Why it is outside the theorem | Influence and dependents | Evidence |
|---|---|---|---|
| `py2mpy.py` translations of `FunctionDef`, `Return`, `Compare`, `Subscript`, `Slice`, and literals | The K theorem begins at the emitted constructor program | Selects the body, binding, and value computed by `SPEC.is-palindrome` | Regeneration exits 0; `solution.mpy` and the claim contain the same function constructor tree; CPython and K concrete results agree on prompt cases |
| Supplied rules `#loadAll`, `FuncDef`, `#look`, `#applyK(toCall(closureVal(...)))`, `#bindP`, `Return`, `#pop`, and `Assign` | The reference semantics is the theorem's trusted operational foundation | Binding, control, scopes, stack, return state, and result storage for the target claim | Exact final-state claim, concrete LLVM execution, and rejected body mutation |
| Supplied `Subscript`/`#sl*`, `doSlice(str(...))`, `slStart`, `slStop`, `slStep`, `isLen`, `buildIS`, `intSeqAt`, and string `applyCmp("==",...)` equations | These fixed rules define modeled reverse slicing and string equality | Directly determines the returned Boolean and formal postcondition | Equation inspection, five concrete K assertions, positive symbolic proof, and rejected false-result mutation |
| K v7.1.293 compiler, LLVM backend, Haskell backend, `kore-exec`, SMT integration, and runtime | The proof does not verify its implementation stack | All compilation, execution, and proof results | Exact versions, independent LLVM/Haskell runs, positive and negative outcomes |
| Correspondence between a CPython `str` and the model's finite `IntSeq` | It is a model-adequacy relation, not a reachability claim inside K | Transfer of the formal result to the HumanEval/CPython intent | Prompt examples, ASCII K execution, and an independent Python two-pointer oracle including Unicode samples |

No value-bearing program-derived abstraction or operational bridge is trusted.
Finite tests support the model and implementation evidence in this ledger; they
do not prove universal equivalence between CPython and the K model.

# Empirically supported facts

- `concrete-tests.py` asserts the four prompt examples plus `"ab"` through the
  LLVM K semantics. The final K configuration has `.K`, `NoExc`, and exit code
  zero.
- `differential-test.py` compares `solution.is_palindrome` with an independent
  two-pointer oracle. It covers the prompt examples and all strings of lengths
  zero through five over `("a", "b", "é", "🙂")`: 1,369 listed cases and zero
  mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are expected-failure validation
  probes. Each exits 1 with a result-specific stuck state.

# Excluded behavior

- Inputs that are not strings, including any incidental CPython behavior of
  other sliceable objects.
- A proof of the complete CPython language, Python exception model, concrete
  Unicode representation, the supplied K semantics, `py2mpy.py`, or K itself.
- A universal proof that every CPython Unicode string is represented by exactly
  one semantic `IntSeq`; the K theorem is parametric over the model sequence,
  while the Unicode transfer evidence is finite.
- Total-correctness, complexity, or resource bounds. The reported formal
  result is the Kit workflow's partial-correctness reachability theorem.

The final runner marker may therefore be `KPROVE_PASSED` because the only
positive target-proof command printed `#Top` and exited 0. That execution marker
is separate from the `VALIDATED` proof-quality headline above.
