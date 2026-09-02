VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `solution.py` is partially
correct for every input represented as `str(INPUT:IntSeq)`: if
`vowels_count` terminates, its returned integer is the number of occurrences
of `a/e/i/o/u` or `A/E/I/O/U`, plus one exactly when the final character is
`y` or `Y`.

The theorem includes module loading, lookup of the exact `vowels_count`
binding, argument evaluation and binding, execution of the exact translated
function body, loop control, local updates, return, frame popping, and the
final module scope. It has no input precondition. In particular, the empty
string is included and returns `0`.

This is a partial-correctness theorem. It does not separately prove
termination.

## Formal claim

`SPEC.vowels-count` in `spec.k` starts from the semantics' initial module
configuration, loads the exact `FuncDef` from `solution.mpy`, calls it with
`str(INPUT:IntSeq)`, and reaches:

```k
<k> vowelsTail(INPUT, .IntSeq) </k>
```

with an empty heap and stack, `NoExc`, exit code `0`, and only the loaded
closure plus the supplied builtins scope remaining.

`vowelsTail` is defined by:

```text
vowelsTail([], last) =
    bit(last == "y") + bit(last == "Y")

vowelsTail(c :: rest, previous) =
    bit(c occurs in "aeiouAEIOU")
    + vowelsTail(rest, [c])
```

The character codes in `verification.k` are, in order,
`97,101,105,111,117,65,69,73,79,85`; terminal `y/Y` are `121/89`.

`SPEC.loop-inv` is the circularity used at the exact recurring `#loop` state.
Starting with accumulator `COUNT`, remaining codes `CS`, and remembered
one-character sequence `LAST`, it returns
`COUNT +Int vowelsTail(CS, LAST)` and performs the exact return/frame-pop
transition.

## Proof-extension inventory

### `vowelsTail(IntSeq, IntSeq)`

- Class: definitional summary.
- Semantic role: names the mathematical value accumulated by the loop; it
  does not match or replace `<k>` execution.
- Domain: every pair of `IntSeq` values.
- Matched context: none.
- Justification scope: the two equations cover the two constructors
  `.IntSeq` and `iCons`; their domains are disjoint.
- Context containment: not applicable because this is not an operational
  bridge.
- State footprint: none.
- Value influence: determines the RHS result of both claims.
- Value justification: the base equation uses fixed `==K` and `intOf` for
  terminal `y/Y`; the step equation uses the supplied `strContains` and
  `intOf` on the exact literal-code sequence used by the program.
- Termination/coverage: the recursive equation strictly descends to `REST`;
  there are no overlapping equations and `[total]` is justified.
- Dependents: `SPEC.loop-inv` and `SPEC.vowels-count`.
- Control validation: not applicable; no execution is replaced.
- Value validation: the loop claim and full claim both print `#Top`; the
  concrete and differential evidence below has zero mismatches.

### `SPEC.loop-inv`

- Class: derived lemma (reachability circularity).
- Semantic role: reasons about, but does not replace with a proof-local
  rewrite, the exact fixed-semantics loop execution.
- Domain: all symbolic `CS`, `LAST`, `COUNT`, original input, current `char`,
  global map, builtins scope, heap, heap location, caller environment,
  continuation, and remaining call stack satisfying the complete displayed
  configuration in `spec.k`.
- Matched context: the exact `#loop` body; the exact post-loop `Stmts`
  sequence; `#endcall`; environment `1`; the exact four-key callee scope;
  caller frame; scope location `2`; and explicit heap, return, exception, and
  exit cells.
- Justification scope and context containment: identical to the claim's
  match domain. There are no omitted continuations or widened operational
  rules.
- State footprint: reads/updates `count`, `last`, and `char`; reads `s`;
  restores the caller environment; removes the callee scope and frame;
  preserves the heap, heap location, return state, exception state, exit
  code, globals, builtins, and remaining stack.
- Value influence: establishes the exact returned integer used by
  `SPEC.vowels-count`.
- Value justification: one fixed-semantics iteration contributes the same
  `strContains` bit as the recursive `vowelsTail` equation; the base case
  executes both terminal `y/Y` comparisons and the real return/pop rules.
- Justification: machine-checked directly using only `VERIFICATION` and the
  supplied `MPY` semantics.
- Dependents: `SPEC.vowels-count`.
- Control/value validation: the focused claim prints `#Top`; the whole spec
  prints `#Top`; the body mutation and false-result probes are both rejected.

There are no operational bridges, trusted primitives, opaque result symbols,
priority rules, or proof-local simplification rules.

## Exact commands and actual outputs

All commands are preserved in `prove.sh`. The final end-to-end command was:

```bash
./prove.sh
```

It exited `0`. Its constituent commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py solution.py | diff - solution.mpy
```

Both exited `0`; `diff` printed no output.

```bash
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

All exited `0`. `krun` ended with these exact relevant cells:

```text
<k> .K </k>
<env> 0 </env>
<scopeLoc> 1 </scopeLoc>
<heap> .Map </heap>
<heapLoc> 0 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The LLVM compiler also printed supplied-semantics warnings about unrelated
non-exhaustive total functions (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and out-of-bounds `valSeqAt`) plus unused `strLt` variables.

```bash
python3 differential_test.py
```

Exit `0`, exact output:

```text
checked: 41379
mismatches: 0
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit `0`. Its only diagnostics were the supplied `strLt` unused-variable
warnings.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv
```

Exit `0`; output included the exact success marker:

```text
#Top
```

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Exit `0`; this proves every claim in `spec.k`. Output included:

```text
#Top
```

Both proof runs also printed only unused-variable warnings in the supplied
`strLt` rules and for intentionally framed, unobserved invariant variables.

The A5 false-result probe was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited `1` with `WarnStuckClaimState`; the exact discriminating residual
was:

```text
<k>
  2 ~> .K
</k>
```

against the deliberately false target `3`.

The body-sensitivity probe was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited `1` with `WarnStuckClaimState`; after removing lowercase `u` from
the body literal, the exact discriminating residual on input `"u"` was:

```text
<k>
  0 ~> .K
</k>
```

against the original program's target `1`.

## Gate results

### Gate A — PASS

- A1: the entry claim executes the exact translated body. Regeneration is
  byte-identical to `solution.mpy`. The material body mutation is rejected
  with result `0` versus `1`.
- A2: there is no operational bridge. The invariant explicitly accounts for
  every active state cell and the return/frame-pop transition.
- A3: lookup, argument evaluation, parameter binding, local assignments,
  loop continuation, return, and cleanup all execute through the fixed
  semantics. The invariant uses the exact `Stmts` continuation shape.
- A4: `vowelsTail` has exhaustive, disjoint constructor equations and
  structural descent. No false or overlapping lemma was added.
- A5: the precondition is `true`; `""` and `"abcde"` are realizable
  witnesses. The false target `3` for `"abcde"` is rejected with actual
  result `2`. The focused and full proof runs exercise the invariant and
  entry claims.

### Gate B — PASS

- B1: the prompt accepts a string representing a word and states no
  non-emptiness precondition. The theorem covers every semantic string,
  including empty input. Uppercase vowels and uppercase terminal `Y` are
  included as required by the `"ACEDY" -> 3` example.
- B2: the supplied model represents strings as finite integer-code
  sequences. The exercised operations—iteration, one-character strings,
  substring membership, integer/Boolean addition, assignment, calls, and
  return—are all fixed semantic rules. Non-ASCII codes are treated as
  non-vowels unless equal to one of the explicitly listed ASCII vowel codes,
  matching the prompt's named vowel set.
- B3: `vowelsTail` directly states the human-facing count, while
  `SPEC.loop-inv` and `SPEC.vowels-count` separately prove that execution
  computes it.
- B4: the implementation agrees with both prompt examples and the stated
  terminal-`y` rule.

### Gate C — PASS

- Every generated/test artifact and exact command exists in the workspace.
- Both positive proof commands print `#Top` and exit `0`.
- Both negative probes have recorded non-zero exits and discriminating
  residual values.
- The independent Python oracle checks all strings of length `0..4` over
  `aAeEiIoOuUyYbz`, plus eight named boundary/example cases: 41,379 checks,
  zero mismatches.
- The LLVM K run checks eight concrete assertions and terminates at `.K` with
  `NoExc` and exit code `0`.

## Trust boundary

- The supplied files under `reference-semantics/` are treated as the fixed
  language model, not as proof extensions. Their rules affect value,
  control, state, and exceptions for both claims. Evidence: LLVM execution
  of eight assertions and agreement with an independent CPython oracle.
- K v7.1.293, its Haskell/LLVM backends, and the backend solver are trusted to
  compile and execute the displayed rules and claims. All formal conclusions
  depend on this toolchain.
- `py2mpy.py` is supplied and trusted only for AST transliteration.
  `python3 py2mpy.py solution.py | diff - solution.mpy` exits `0`, and the
  resulting function body is reproduced exactly in the entry claim.
- There are no proof-local trusted primitives or unproved operational
  bridges.

## Empirically supported facts

- CPython examples and boundaries: `"" -> 0`, `"abcde" -> 2`,
  `"ACEDY" -> 3`, `"yyy" -> 1`, `"rhythm" -> 0`, `"AEIOU" -> 5`,
  `"sky" -> 1`, and `"yellow" -> 2`.
- Independent oracle: `differential_test.py` uses Python's `.lower()` in an
  independently written count and reports 41,379 checks with zero
  mismatches.
- Supplied-semantics execution: `concrete-tests.mpy` evaluates the same eight
  assertions with no exception.

These finite results support adequacy; they are not used as substitutes for
the universal K claims.

## Excluded behavior

- Total correctness/termination is not established by these reachability
  claims.
- Behavior outside the supplied `MPY` model is not claimed, including
  unsupported Python constructs, CPython implementation details, I/O,
  concurrency, and exceptions not modeled by the reference semantics.
- The formal input sort permits arbitrary integer codes, including values
  that are not valid Unicode scalar values. This is a harmless superset for
  the theorem: only the explicitly named ASCII vowel codes contribute.
