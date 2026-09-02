VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, loading the exact translated
`solution.py` body and calling `string_to_md5` is partially correct for every
finite modeled string:

- `str(.IntSeq)` returns `noneV`.
- Every nonempty `str(CS)` returns `str(md5hexCodes(CS))`.

The two cases are exhaustive and the nonempty case is symbolic and unbounded;
there is no input-length limit or finite unrolling. The claims also require the
complete final machine state: computation finished, module environment restored,
temporary call scope removed, no heap allocation, empty stack, no pending
return, no exception, and exit code zero.

The digest value is conditional on the supplied semantics' named
`md5hexCodes` trusted primitive. The proof does not assume an equation that
states the desired digest.

## Formal claim

Program boundary:

- Load the exact `Import("hashlib")` and `FuncDef("string_to_md5", ...)`
  translated from `solution.py`.
- Invoke that loaded closure through normal name lookup, parameter binding,
  call-frame creation, branch execution, return, frame pop, and assignment to
  the harness variable `result`.
- Include the standard-library MD5 operation only through the fixed reference
  semantics' supplied primitive boundary.

Input domain:

- `SPEC.empty-input`: the unique empty modeled string.
- `SPEC.nonempty-input`: arbitrary `CS:IntSeq` satisfying
  `notBool (CS ==K .IntSeq)`.

Observable result:

- Empty input: `result |-> noneV`.
- Nonempty input: `result |-> str(md5hexCodes(CS))`.

These claims are in `spec.k`; together they cover every finite `IntSeq` shape
represented by the fixed model.

## Proof-extension inventory

Reinspection of `verification.k` and `spec.k` found no proof extension:

- `verification.k` only imports the supplied `MPY` module.
- There are no proof-local functions, equations, simplification rules,
  ordinary rewrites, priorities, opaque symbols, casts, operational bridges,
  or auxiliary circularities.
- Both claims in `spec.k` are positive target claims. Neither can be used as a
  loop circularity because the program contains no loop.

The unproved components used by the claims are already part of the frozen
reference semantics, not additions in `verification.k`. They are classified
and recorded in the trust ledger below.

## Exact commands and actual outputs

The complete reproducible command sequence is `prove.sh`. It was run as:

```bash
./prove.sh > proof-run.log 2>&1
```

Actual exit: `0`. The complete 482-line output is preserved in
`proof-run.log`.

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual exit: `0`; no diagnostic output.

Concrete reference-semantics build and execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke-empty.mpy --definition runtime-kompiled
```

Actual exits: `0`, `0`. The final configuration contains:

```text
<k> .K </k>
0 |-> scope ( "result" |-> noneV ... )
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The mandated LLVM build warns about several unrelated non-exhaustive functions
in the supplied semantics. A nonempty LLVM probe reaches the intentionally
evaluator-free primitive and exits `113`:

```text
[Error] krun: runtime-kompiled/interpreter ...
md5hexCodes ( iCons ( 72 , ... iCons ( 100 , .IntSeq ) ... ) )
EXPECTED_OPAQUE_LLVM_FAILURE exit=113
```

The Haskell execution can preserve that opaque value and completes:

```bash
krun smoke.mpy --definition verification-kompiled
```

Actual exit: `0`; its final scope contains both:

```text
"empty_result" |-> noneV
"digest_result" |-> str ( md5hexCodes ( iCons ( 72 , ... ) ) )
```

Symbolic build and all required positive target proofs:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.empty-input

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.nonempty-input

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual exits: `0`, `0`, `0`, `0`. Each of the three `kprove` commands printed:

```text
#Top
```

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1`, with `WarnStuckClaimState`. The residual final scope has
`"result" |-> noneV`, which cannot match the deliberately false
`"result" |-> 0`. `prove.sh` records:

```text
EXPECTED_VACUITY_FAILURE exit=1
```

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual exit: `1`, with `WarnStuckClaimState`. The material mutation replaces
the nonempty branch's digest return with `Return(NoneVal)` while retaining the
original digest postcondition for the realizable input `"a"`. The residual has
`"result" |-> noneV`. `prove.sh` records:

```text
EXPECTED_BODY_MUTATION_FAILURE exit=1
```

Independent differential evidence:

```bash
python3 test_solution.py
```

Actual exit: `0`; output:

```text
DIFFERENTIAL_CASES=213 MISMATCHES=0
PROMPT_EXAMPLE=3e25960a79dbc69b674cd4ec67a72c62
UTF8_BOUNDARY text='π' codepoints=[960] bytes=[207, 128]
```

## Gate results

Gate A — PASS.

- A1: The exact program body executes under fixed semantics. The claims start
  from module load and include the exact closure body, binding, argument, and
  environment. The body-mutation probe is rejected.
- A2: No proof-local execution is skipped. Every configuration cell is
  explicitly constrained before and after execution.
- A3: Fixed rules perform the function lookup, argument evaluation, parameter
  binding, branch, return, and control-stack restoration. The supplied
  standard-library route is isolated as a named external trust boundary.
- A4: There are no proof-local equations, total functions, or simplification
  rules to check for truth, overlap, coverage, or descent.
- A5: Empty input and concrete nonempty input `"a"` are realizable witnesses.
  The false-postcondition mutation is rejected with a stuck residual showing
  the actual result.

Gate B — PASS.

- B1: Empty plus arbitrary nonempty `IntSeq` claims cover the complete modeled
  string domain without a size bound.
- B2: The solution uses real CPython UTF-8 and is faithful on Unicode. The
  supplied K model is explicitly ASCII-oriented and treats encoding as an
  identity on code sequences. This is a fixed-model boundary, not a theorem
  restriction; the theorem covers every `IntSeq` admitted by that model. The
  concrete `π` code-point/UTF-8-byte divergence is recorded.
- B3: The formal result is the fixed semantics' exact opaque
  `md5hexCodes(CS)` summary. Its interpretation as the lowercase MD5 digest is
  conditional on the named supplied primitive contract and independently
  tested; it is not installed as a proof equation.
- B4: `solution.py` implements the prompt directly, returns `None` exactly for
  empty strings, and uses CPython's UTF-8 bytes and lowercase `hexdigest` for
  every nonempty string.

Gate C — PASS.

- Every unproved component and dependent claim is listed below.
- Every reported command is present in `prove.sh`; complete output is present
  in `proof-run.log`.
- Formal results, conditional trust, finite evidence, and excluded behavior
  are separated.

## Trust boundary

### Supplied MD5 route and value

- Extension: fixed rules
  `Call(Attribute(Name("hashlib"), "md5"), (E, .Exprs)) => E ~> #md5`,
  `str(CS) ~> #md5 => md5Obj(CS)`,
  `applyMethod(md5Obj(CS), "hexdigest", .Vals) =>
  str(md5hexCodes(CS))`, and the evaluator-free declaration
  `md5hexCodes(IntSeq)`.
- Class: trusted primitive supplied by the frozen reference semantics.
- Semantic role: models the external standard-library operation and supplies
  its result value; it is not program-defined code.
- Domain: the exact single-positional-argument `hashlib.md5` syntax used by
  `solution.py`, a modeled string argument, and a zero-argument `hexdigest`.
- Matched context: the active `<k>` item with an arbitrary preserved suffix;
  no other cell is matched or changed by these rules.
- Justification scope: conditional trust that this supplied route denotes the
  imported CPython `hashlib.md5` binding for this exact source, which does not
  rebind `hashlib`.
- Context containment: the source has the exact imported name, call arity,
  receiver, method, and continuation shape. The route evaluates `E` first and
  preserves its continuation.
- State footprint: reads/evaluates the argument in `<k>`; writes no scope,
  heap, allocation, stack, return, exception, or exit-code cell.
- Value influence: determines the entire nonempty returned string and its
  postcondition.
- Value justification: the named external contract says
  `md5hexCodes(CS)` denotes the lowercase MD5 hex digest of the encoded input.
  There is deliberately no K equation or evaluator that assumes a particular
  digest.
- Dependents: `SPEC.nonempty-input`; the empty-input claim does not depend on
  the digest value.
- Control validation: Haskell `krun` completes the full empty/nonempty smoke
  program with the continuation and all state cells intact. The target claims
  execute the same fixed route.
- Value validation: `test_solution.py` compares the executable CPython
  implementation with the independent OpenSSL 3.0.2 MD5 engine on 213 cases
  with zero mismatches. This is finite evidence, not a universal K theorem.

### Supplied string-encoding model

- Component: fixed rule
  `applyMethod(str(CS), "encode", str(_), .Vals) => str(CS)`.
- Class: trusted primitive/model abstraction supplied by the frozen semantics.
- Effect: its value feeds `md5hexCodes`, but it changes no control or state
  cell.
- Exact conditional scope: faithful to UTF-8 for ASCII code sequences. For
  non-ASCII Python strings it is a recorded model boundary.
- Dependents: `SPEC.nonempty-input`.
- Evidence: `π` has source code point `[960]` but UTF-8 bytes `[207, 128]`.
  The Python implementation itself uses UTF-8 correctly and the differential
  corpus includes Unicode.

### Supplied import/binding abstraction

- Component: the fixed semantics treats ordinary `Import` as a no-op and
  recognizes the exact syntax `Name("hashlib").md5` directly.
- Class: trusted external binding/control abstraction.
- Effect: pins the external binding and bypasses a modeled module object; it
  changes no user-visible state represented by the claims.
- Exact conditional scope: this source executes `import hashlib` before the
  function call and never rebinds `hashlib`.
- Dependents: `SPEC.nonempty-input`.
- Evidence: exact source/claim syntax, successful fixed-semantics control
  execution, and the body-sensitivity rejection. No claim is made that this
  import model is adequate for arbitrary Python programs or rebinding.

## Empirically supported facts

- CPython `solution.py` agrees with OpenSSL's separate MD5 implementation on
  213 explicit and deterministic-random cases, including empty input, the
  prompt example, standard MD5 vectors, NUL/whitespace, long ASCII, and
  Unicode. Mismatch count: zero.
- The prompt example evaluates to
  `3e25960a79dbc69b674cd4ec67a72c62`.
- LLVM `krun` concretely validates the empty branch and all control/state
  cleanup. Haskell `krun` validates the same control path for nonempty input
  while retaining the opaque digest term.
- These are finite observations. Universal correctness in K is only the
  conditional symbolic theorem stated above.

## Excluded behavior

- Non-string Python arguments are outside the prompt's stated string domain.
- The proof does not derive the MD5 compression algorithm, collision
  resistance, cryptographic security, or the concrete value of
  `md5hexCodes`; that value is the supplied named trust boundary.
- The supplied K string model does not reproduce UTF-8 byte expansion for
  non-ASCII code points. The actual Python implementation does; the formal
  K-to-CPython correspondence on those values is conditional on this recorded
  model boundary.
- The supplied LLVM backend cannot evaluate nonempty `md5hexCodes` terms and
  exits `113`; this is expected from its `no-evaluators` declaration. The
  positive symbolic target proofs do not use the LLVM evaluator.
- The K workflow proves partial correctness. No separate asymptotic cost,
  resource bound, or total-correctness theorem is claimed.
