VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `solution.py` is partially
correct for every finite string represented as `str(S:IntSeq)`, with no bound
on the length of `S`.

For each source code point `C`:

- if `97 <= C <= 122`, the result contains
  `pyMod(C - 97 + 4, 26) + 97`;
- otherwise, the result contains `C` unchanged.

Thus lowercase ASCII letters are rotated four places with wraparound, and
characters outside that alphabet pass through. The prompt examples are all
instances of this theorem.

This is a K reachability proof of partial correctness. The reachability claim
does not separately assert a liveness theorem, although the modeled `for` loop
removes one `iCons` constructor per iteration on every finite input.

## Formal claim and scope

`spec.k` contains two claims:

1. `SPEC.encrypt-loop` is a circularity over symbolic `S:IntSeq`. Starting at
   the supplied semantics' real `#loop` term with arbitrary accumulator `A`,
   it executes the actual loop body and ends with
   `str(encryptFold(A, S))`. It also tracks Python's final binding of the loop
   target through `finalLoopChar`.
2. `SPEC.encrypt-entry` starts from the standard module configuration, loads
   the exact translated `FuncDef`, calls it with symbolic `str(S)`, and reaches
   `.K` with module variable `result` equal to
   `str(encryptResult(S))`. The claim also checks the final function binding,
   environment, scope allocator, heap, heap allocator, stack, return state,
   and exception state.

There is no `requires` restriction beyond the input being a string value. The
claim ranges over raw `IntSeq` constructors, not examples, fixed lengths, or a
bounded unrolling. Non-string arguments are outside the source contract.

The observable intended state is the returned value, represented by the
module-level `result`, together with normal completion and `NoExc`. The
`exit-code` cell is not part of the symbolic postcondition because this
program has no exit operation; the concrete LLVM run independently ended with
exit code 0.

`audit_identity.py` whitespace-normalizes `solution.mpy` and `spec.k`, extracts
the translated function term, and confirms it occurs exactly once as the
entry claim's loaded `FuncDef`.

## Proof-extension inventory

No proof-local rule intercepts a `Call`, loop, builtin, expression, return, or
other operational term. There are no operational bridges, proof-local trusted
primitives, opaque result oracles, priorities, concrete rules, or
simplification axioms.

| Extension | Class and domain | Semantic role and state footprint | Value/control influence | Justification and validation |
|---|---|---|---|---|
| `rot4Code(Int)` | Definitional summary; one unguarded total equation over all `Int` | Names the exact arithmetic expression used by the lowercase branch; matches no operational configuration and reads/writes no cells | Feeds only the mathematical result summary | Its RHS is the source expression after fixed-semantics dispatch of integer operations; ROT5 mutation is rejected |
| `encryptedChar(Int)` | Definitional summary; three total cases `C < 97`, `97 <= C <= 122`, and `C > 122` | Names the source `if` result for one code point; no operational replacement or state access | Selects the summarized output code | Guards are pairwise disjoint and exhaustive; the middle case uses `rot4Code`, outer cases preserve `C` |
| `encryptFold(IntSeq, IntSeq)` | Definitional summary; disjoint empty/cons cases | Tail-recursive left fold matching `out += ...`; no operational replacement or cells | Defines the target result and loop invariant | Recurses structurally on the second sequence argument; its one-step equation is exactly the loop body's accumulator update |
| `encryptResult(IntSeq)` | Definitional summary; one total equation | Initializes `encryptFold` with `.IntSeq`; no state | Final postcondition | Direct wrapper with complete coverage |
| `finalLoopChar(IntSeq, Val)` | Definitional summary; disjoint empty/cons cases | Tracks the actual `c` scope entry so the invariant preserves the complete local map | Affects only proof-local scope matching, not the returned ciphertext | Structural recursion reproduces Python's last-target binding; proved while fixed loop execution updates `c` |
| `SPEC.encrypt-loop` | Derived reachability claim over every `S:IntSeq`, accumulator, initial target value, and framed continuation | Executes fixed `#loop`, iterator yield, target binding, branch, builtins, arithmetic, concatenation, and scope writes | Supplies the circularity used by the entry proof; introduces no abrupt control | Machine-checked together with the entry claim; body and false-result probes reject altered behavior |
| `SPEC.encrypt-entry` | Target reachability claim over every `S:IntSeq` | Executes module loading, closure creation, lookup, argument evaluation/binding, body, return, frame pop, and result assignment | Constrains the full returned string and normal control state | Exact translated body occurs once in the entry program; complete proof prints `#Top` |

The loop claim's match context contains the exact loop body, loop target,
current function scope and parent/builtins binding. Its `<k>` continuation is
framed by the claim itself; fixed execution of this body has no `return`,
`break`, `continue`, exception-producing modeled branch, allocation, or other
effect that discards that continuation. The claim is machine-checked for that
framed context, rather than converted into an operational rewrite.

## Reproducible commands and actual results

The complete command record is executable as:

```bash
./prove.sh
```

`prove.sh` contains these positive target steps:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 audit_identity.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual final run results:

- translator/spec identity: `translated_function_occurrences_in_entry_spec=1`,
  exit 0;
- independent Python differential: `cases=1134 mismatches=0`, exit 0;
- LLVM `kompile`: exit 0;
- `krun`: final `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`, exit 0;
- Haskell `kompile`: exit 0;
- complete `kprove`: `#Top`, exit 0.

Compiler warnings in the supplied semantics concern unused variables and
non-exhaustive unrelated total functions. None of the non-exhaustive functions
listed by LLVM (`mapStrVS`, float helpers, `joinCodes`, or `valSeqAt`) is used
by this program or proof.

The runner also executes two expected-failure probes:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual probe results:

- `SPEC-VACUITY.false-result` changes the expected result for `encrypt("")`
  from `""` to `"a"`. It exits 1 with `WarnStuckClaimState`; the residual
  contains the actual `str(.IntSeq)`.
- `SPEC-BODY-MUTATION.rot5-does-not-prove-rot4` changes the executed shift
  constant from 4 to 5 while retaining the ROT4 result for `"a"`. It exits 1
  with `WarnStuckClaimState`; the residual contains code point 102 (`"f"`)
  instead of required code point 101 (`"e"`).

`prove.sh` treats either mutation succeeding as a runner failure and prints
`EXPECTED FAILURE` only for the observed non-zero exit.

## Gate results

### Gate A — PASS

- The exact program-defined function executes through frozen semantics.
- No operational bridge skips lookup, argument evaluation, binding, loop
  control, builtins, return, or state changes.
- All summary equations have exhaustive, non-overlapping constructor/guard
  coverage and structurally descending recursion where recursive.
- The empty string is a realizable witness because there is no precondition.
- The false-result mutation fails with the actual empty result.
- The independent ROT5 mutation fails with the changed fixed-semantics result,
  establishing body sensitivity.

### Gate B — PASS

- Input alignment: every arbitrary finite modeled string is covered, without a
  length or character-domain bound.
- Property alignment: the formal per-character equation is ROT4 on lowercase
  alphabet characters and identity outside that alphabet.
- All four examples in `prompt.py` are reproduced.
- Implementation alignment: `solution.py`, `solution.mpy`, the exact entry
  syntax, the loop invariant, and the postcondition describe the same
  operation.
- Model alignment: strings are code-point sequences in the supplied model.
  Source literals and every `chr` result here are ASCII; arbitrary other input
  code points take the pass-through branch, so the proof does not impose the
  model's ASCII-literal restriction on symbolic inputs.

### Gate C — PASS

- Every proof-local extension and its dependents are inventoried above.
- Positive, negative, identity, concrete, and differential evidence is
  reproducible from existing artifacts via `prove.sh`.
- Formal proof, conditional semantic trust, and finite empirical evidence are
  separated below.

## Trust boundary

The theorem is conditional on:

1. the supplied read-only `MPY` reference semantics, especially its rules for
   `#loadAll`, lookup/calls/frames, string iteration and concatenation,
   `ord`, `chr`, integer comparisons/arithmetic/`pyMod`, Boolean short-circuit,
   `If`, `AugAssign`, `Return`, and scope maps;
2. the fixed `py2mpy.py` CPython-AST transliteration;
3. the K toolchain and Haskell backend/solver implementing the reported
   reachability result correctly.

These components affect value, control, state, and the partial-correctness
interpretation of both target claims. They are supplied infrastructure rather
than proof-local assumptions. No additional trusted primitive is introduced
by `verification.k`.

The identity check and body mutation support the translator/program boundary.
LLVM examples and the independent Python differential support the relevant
semantic behavior, but finite evidence does not replace the universal K proof
under the supplied semantics.

## Empirically supported facts

`concrete_tests.py` is translated by the fixed translator and executed by
LLVM. It asserts the four prompt examples, empty input, wraparound `"xyz"`,
and pass-through `"a z!"`.

`differential_test.py` uses Python's independently implemented
`str.translate` with a `str.maketrans` ROT4 table as oracle. It checks the empty
string, every one-character ASCII string, alphabet and boundary examples,
Unicode pass-through examples, and 1,000 seed-0 random strings over ASCII
letters, digits, punctuation, and spaces: 1,134 cases and zero mismatches.

These runs are finite validation evidence only.

## Excluded behavior

- Calls whose argument is not a string are outside the prompt contract and
  the theorem.
- Behavior of unrelated constructs and builtins in the supplied partial
  Python semantics is not claimed.
- Total-correctness/liveness is not part of the Kit's K reachability theorem.
