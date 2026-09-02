SOUND-BUT-LIMITED

# What is proven

Under the supplied `MPY` semantics, the translated body of
`file_name_check` is partially correct for every internal string value
`str(CS)`:

- it returns `"No"` for the empty sequence;
- for a nonempty sequence, it returns `"No"` if the dot count is not one,
  the first code is not one of `A`-`Z` or `a`-`z`, the last four codes are
  not `.txt`, `.exe`, or `.dll`, or the number of ASCII digit codes exceeds
  three; and
- it returns `"Yes"` in each of the three allowed-extension cases when all
  preceding checks hold and the ASCII digit count is at most three.

The claims also require the call to restore the caller environment, module
scope, scope allocator, empty heap, heap allocator, empty stack, return state,
exception state, and exit code. This is a partial-correctness result as defined
by the Kit workflow; it is not a separate liveness theorem.

The positive target command over the complete `SPEC` module printed `#Top` and
exited 0. This execution result is separate from this report's
`SOUND-BUT-LIMITED` proof-quality headline.

# Formal claim

The program boundary is an invocation of the module binding

```k
"file_name_check" |->
  closureVal(("file_name", .ParamNames), fileNameCheckBody, 0)
```

with the argument `str(CS)`. `fileNameCheckBody` is a parse-time macro whose
expanded KORE term is mechanically compared with `solution.mpy`.

The ten claims in `spec.k` form a complete case partition:

1. `empty-name`;
2. nonempty `bad-dot-count`;
3. `bad-initial` after exactly one dot;
4. `bad-extension` after the dot and initial checks;
5. `too-many-digits-txt`;
6. `too-many-digits-exe`;
7. `too-many-digits-dll`;
8. `valid-name-txt`;
9. `valid-name-exe`; and
10. `valid-name-dll`.

For `.exe` and `.dll`, the preconditions include the failure of earlier suffix
tests, matching Python `or` short-circuit order. The cases cover empty and
nonempty `IntSeq` values; within the nonempty case, integer disequality/equality,
Boolean complement, the three distinct suffixes, and `> 3`/`<= 3` partition
the paths.

Realizable witnesses include:

| Claim class | Witness |
|---|---|
| empty | `""` |
| bad dot count | `"abc"` |
| bad initial | `"1.txt"` |
| bad extension | `"a.pdf"` |
| too many digits | `"a1234.txt"`, `"a1234.exe"`, `"a1234.dll"` |
| valid | `"a.txt"`, `"a.exe"`, `"a.dll"` |

# Proof-extension inventory

There are no operational bridges, opaque result-bearing program summaries,
trusted proof-local primitives, loop circularities, or auxiliary execution
claims. The actual function body executes under the fixed `MPY` rules.

## `fileNameCheckBody`

- **Class:** definitional/syntactic summary.
- **Semantic role:** parse-time alias only; it expands to the exact `Stmts`
  tree and is absent as a runtime operation.
- **Domain and matched context:** the sole terminal
  `fileNameCheckBody` wherever a `Stmts` value is expected.
- **Justification scope and containment:** `proof-program.mpy` embeds the macro
  as the function body. Expanding macros for it and for `solution.mpy` produced
  byte-identical 14,414-byte KORE files.
- **State footprint:** none. After expansion, fixed semantics reads/writes the
  normal call cells.
- **Value/control influence:** it supplies all program statements, so all
  claims depend on its exact expansion.
- **Validation:** changing the final translated `Return(Str("Yes"))` to
  `Return(Str("No"))` made the KORE comparison fail with `cmp` exit 1.

## `decimalDigitCount(CS)`

- **Class:** definitional summary.
- **Semantic role:** names the sum of ten fixed-semantics `cntSub` calls; it
  does not replace program execution.
- **Domain:** all `CS:IntSeq`; one unguarded equation, hence exhaustive with no
  overlap.
- **Matched context:** any occurrence of
  `decimalDigitCount(CS)` in a constraint.
- **Justification scope and containment:** the equation is exactly the
  left-associated sum computed by the ten source `count` calls. For a
  singleton ASCII digit pattern, fixed `cntSub` counts its occurrences.
- **State footprint:** none.
- **Value influence:** only digit-case preconditions; it determines the
  `> 3` versus `<= 3` partition.
- **Dependents:** all six digit-tail claims.
- **Validation:** positive claims on both sides of the threshold close;
  concrete and differential tests include three and four digit witnesses.

## `fileExtensionIs(CS, EXT)`

- **Class:** definitional summary.
- **Semantic role:** names fixed `doSlice` of the last four codes followed by
  fixed string equality; it does not replace source slicing or comparison.
- **Domain:** all `CS:IntSeq` and `EXT:IntSeq`; one exhaustive, nonoverlapping
  equation.
- **Matched context:** any constraint occurrence.
- **Justification scope and containment:** exact fixed-semantics terms
  `doSlice(str(CS), someB(-4), noB, noB)` and `applyCmp("==", ...)`.
- **State footprint:** none; string slices are values in this semantics.
- **Value influence:** suffix-path preconditions only.
- **Dependents:** `allowedFileExtension` and the six extension-specific claims.
- **Validation:** all `.txt`, `.exe`, and `.dll` positive and too-many-digit
  claims close; invalid and long-extension concrete cases are rejected.

## `allowedFileExtension(CS)`

- **Class:** definitional summary.
- **Semantic role:** disjunction of the three `fileExtensionIs` values; no
  execution is replaced.
- **Domain:** all `CS:IntSeq`; one exhaustive, nonoverlapping equation.
- **Matched context:** the `bad-extension` precondition.
- **Justification scope and containment:** its right-hand side enumerates
  exactly `.txt`, `.exe`, and `.dll`.
- **State footprint:** none.
- **Value influence:** determines only the invalid-extension claim domain.
- **Dependents:** `SPEC.bad-extension`.
- **Validation:** the invalid-extension proof closes; concrete tests include
  `"abc.atxt"`, `"a.b.txt"`, uppercase extension, and trailing-dot cases.

## `N >Int 3 => false requires N <=Int 3`

- **Class:** derived lemma.
- **Semantic role:** simplifies an integer comparison already produced by
  fixed execution; it does not bypass a Python operation or control rule.
- **Domain:** every mathematical integer `N` satisfying `N <= 3`. The guard
  and right-hand side are consistent everywhere in that domain.
- **Matched context:** any simplifier context containing `N >Int 3` under the
  guard. Mathematical equality is context-independent.
- **State footprint:** none.
- **Value/control influence:** lets the fixed `If` semantics take its false
  branch on the three valid-name claims.
- **Justification:** `lemma-spec.k` proves the same implication using an
  independently compiled `MPY`-only definition that does not contain this
  proof-local rule.
- **Dependents:** `valid-name-txt`, `valid-name-exe`, and `valid-name-dll`.
- **Validation:** the bridge-free audit printed `#Top`; before this lemma the
  valid claims stopped at the symbolic `#branch`, while after it all three
  printed `#Top`.

# Exact commands and actual outputs

The executable record is `prove.sh`. The relevant commands actually run were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py
```

Output:

```text
checked=181727 mismatches=0
```

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Output: exit 0. The compiler emitted warnings in supplied, unused or
domain-restricted total functions; it produced the LLVM definition.

`prove.sh` copies `solution.py`, appends eight assertions, translates that
temporary file with the fixed translator, and runs:

```bash
krun "$proof_tmp/concrete.mpy" --definition runtime-kompiled
```

Output: exit 0 with final `<k> .K </k>`, `<ret> noRet </ret>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Output: exit 0. The only displayed Haskell-build warnings were unused
variables in supplied `strLt` rules.

The exact program-identity commands are recorded in `prove.sh` as two `kast`
calls with `--module VERIFICATION --sort Module --expand-macros --output kore`,
followed by `cmp`.

Actual result:

```text
PROGRAM_IDENTITY_MATCH bytes=14414
MUTATED_PROGRAM_IDENTITY_STATUS=1 (expected nonzero)
```

The independent lemma audit used:

```bash
kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-kompiled
kprove lemma-spec.k \
  --definition audit-kompiled \
  --spec-module LEMMA-SPEC
```

Actual output and exit:

```text
WarnTrivialClaim: Claim proven without rewriting
#Top
exit 0
```

The required positive target command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and exit:

```text
#Top
exit 0
```

The false-result mutation used:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual contains
`str(iCons(89, iCons(101, iCons(115, .IntSeq))))`, i.e. `"Yes"`, while the
mutated destination requires `"No"`.

# Gate results

## Gate A — PASS

- **A1:** the exact closure binding, parameters, body, argument, and module
  environment are in every claim. The macro-expanded body matches
  `solution.mpy`; a material return mutation breaks the identity check.
- **A2:** no operational bridge skips state. All operational cells are present
  and fixed at the destination; the call frame is created and popped by MPY.
- **A3:** normal name lookup, bound-method lookup, argument evaluation,
  short-circuiting, return, and frame pop execute under fixed semantics. There
  is no bridge with a broader continuation or abrupt-control abstraction.
- **A4:** all three definitional functions have exhaustive, nonoverlapping
  equations. The only proof-local lemma is true throughout its guard and has a
  bridge-free MPY-only proof.
- **A5:** the listed ground witnesses make every claim class realizable. The
  false-result mutation is rejected with a stuck residual showing the actual
  opposite result.

## Gate B — FAIL

The formal predicates align with the prompt:

- a singleton-count sum counts only ASCII digits `0`-`9`;
- exactly one dot plus a four-code `.txt`, `.exe`, or `.dll` suffix fixes the
  substring after the only dot;
- membership in the explicit 52-code alphabet enforces a Latin first letter;
  and
- that first-letter condition also makes the prefix before the dot nonempty.

However, the supplied MPY semantics is explicitly a limited code-sequence
model, not a full CPython Unicode/text and exception semantics, and this proof
does not machine-check an encoding theorem relating every Python `str` to
`IntSeq`. The implementation-to-CPython bridge is strongly tested, including
Unicode elsewhere in a name, but remains empirical. Therefore intent adequacy
for the unrestricted natural-language Python-string contract is not fully
formal, and the required headline is `SOUND-BUT-LIMITED`.

## Gate C — PASS

All assumptions, commands, inputs, oracles, results, mutations, and exclusions
are named here and have existing artifacts. The positive target, independent
lemma audit, body identity check, body mutation, false-result mutation,
concrete MPY assertions, and independent CPython differential test are
reproducible through `prove.sh`, `test_solution.py`, `lemma-spec.k`,
`proof-program.mpy`, and `spec-vacuity.k`.

# Trust boundary

| Component | Why outside this theorem | Effect | Dependents | Evidence |
|---|---|---|---|---|
| Supplied `reference-semantics/` | Fixed input, not proved here | Defines execution, values, state, and exceptions | All K claims | LLVM concrete runs and Haskell proofs |
| K frontend, Haskell backend, SMT hooks | Verification infrastructure | Parsing, rewriting, implication checks | All K results | Exact versions ran successfully; outputs above |
| `py2mpy.py` | Fixed source translator | Maps CPython AST to MPY syntax | Program identity | Regeneration plus expanded-KORE equality |
| Python `str` to MPY `IntSeq` correspondence | No complete encoding theorem in supplied model | Limits CPython/Unicode intent conclusion | Gate B conclusion | 181,727-case independent differential test |

There is no unproved proof-local trusted primitive and no proof-local rule that
replaces program-defined execution.

# Empirically supported facts

`test_solution.py` uses a regex-based shape oracle plus an independent scan for
ASCII digits. It does not reuse the implementation's dot-count/suffix
expression. Its deterministic input scope is:

- 19 curated prompt, boundary, malformed, digit-threshold, and Unicode cases;
- every string of length zero through five over `aZ09.txedl?`; and
- 5,000 seeded strings of length zero through twenty drawn from ASCII letters,
  digits, punctuation, spaces, and `é`, `中`, and `🙂`.

After set deduplication the run checked 181,727 inputs with zero mismatches.
This is finite evidence, not a universal equivalence theorem.

The LLVM run executes eight assertions covering the prompt examples, digit
threshold, multiple dots, a misleading long extension, an empty prefix, and a
valid mixed alphanumeric `.dll` name. It terminates with no exception and exit
code zero.

# Excluded behavior

- A complete formal correspondence with CPython Unicode strings.
- Non-string arguments and their Python exceptions.
- Filesystem-specific filename restrictions not stated in the prompt.
- A separate termination/liveness theorem; the Kit result is partial
  correctness.
- Correctness of the supplied semantics, translator, K implementation, or SMT
  solver themselves.
- Performance or complexity bounds.
