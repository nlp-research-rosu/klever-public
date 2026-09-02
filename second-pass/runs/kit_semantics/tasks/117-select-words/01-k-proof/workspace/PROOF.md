VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every finite `IntSeq` string `S` and
every integer `N >= 0`, the exact translated `select_words` definition is
partially correct:

- the function definition is loaded and selected through normal name lookup;
- `S` and `N` are bound through the normal function-call rules;
- the translated Python body executes, including list allocation, iteration,
  comparisons, concatenation, append, return, and frame cleanup;
- the returned value is `ref(0)` and heap location `0` contains
  `list(selectScan(S, N, .IntSeq, 0, .ValSeq))`.

`selectScan` is the mathematical property definition. It scans left to right,
uses code 32 as the word separator, never emits an empty word, increments the
current count exactly when the character is absent from
`"aeiouAEIOU"`, and appends the completed word exactly when the count equals
`N`. `valSeqConcat` preserves encounter order.

This is a partial-correctness result in the Kit sense. It does not make a
separate liveness, complexity, or resource-bound claim.

## Formal claims and validation scope

`SPEC.select-words-loop` is the loop circularity. At the exact loop head it
relates:

- the unprocessed suffix `S`;
- locals `word`, `count`, and `ch`;
- the closed ordinary local frame containing `s`, `n`, and `result`; and
- heap location `H` containing the accumulated list `A`

to `wordAfter(S, WORD)`, `countAfter(S, COUNT)`,
`charAfter(S, OLDCH)`, and `scanAccum(S, N, WORD, COUNT, A)`.
The continuation and all unmentioned cells are framed unchanged.

`SPEC.select-words` is the entry theorem. Its left side starts at
`#loadAll(Module(FuncDef(...))) ~> Call(...)` in the complete initial
configuration. Its right side constrains the returned reference, selected-word
heap contents, final module binding, allocation counters, empty call stack,
`noRet`, `NoExc`, and exit code 0.

Validation scope:

- Program boundary: the exact `FuncDef` and all program-defined operations in
  `solution.mpy`.
- Input domain: every `str(IntSeq)` represented by the semantics and every
  natural-number argument `N >= 0`. This is a superset of the prompt's promised
  letters-and-spaces strings.
- Observable final state: returned reference and its heap list, plus the
  lifecycle cells constrained by the entry claim.
- Intended property: all and only space-delimited, nonempty words with exactly
  `N` non-vowel characters, in source order.

Both claims were proved together, so the entry theorem had the loop claim
available as a circularity.

## Proof-extension inventory

### Exact AST names

Extensions: `charLoopBody`, `afterCharLoop`, and `selectWordsBody`, with one
unconditional equation each.

- Class: definitional summary.
- Semantic role: names exact MPY syntax trees; it does not replace an MPY
  operational transition.
- Domain and matched context: every occurrence of the corresponding proof-only
  `Stmts` symbol; no guard, continuation, binding, or state is matched.
- Justification scope and context containment: each right side is the literal
  AST emitted in `solution.mpy`; expansion is valid in every syntax context in
  which the name can occur.
- State footprint: none.
- Value/control influence: these names determine the exact source body used by
  both claims.
- Value justification: not result-bearing; the equations only expand syntax.
- Dependents: both target claims.
- Control/value validation: `prove.sh` regenerates `solution.mpy` directly
  from `solution.py`; manual comparison of the final constructor tree with
  these equations is exact. The body-sensitivity probe changes the initial
  `count` assignment and the original result theorem is rejected.

### Mathematical result and loop-state summaries

Extensions: `selectScan`, `scanAccum`, `flushSelected`, `wordAfter`,
`countAfter`, and `charAfter`, including their `[simplification]` equations.

- Class: definitional summary.
- Semantic role: describes mathematical results and expected loop-local state;
  none of these symbols occurs in the source computation or rewrites an MPY
  program term.
- Domain: all declared `IntSeq`, `Int`, and `ValSeq` arguments.
- Matched context: pure applications of the named functions. No `<k>` term,
  continuation, control stack, binding, or operational cell is matched.
- Justification scope and context containment: the equations are definitions
  over the complete constructor domains.
- State footprint: none directly. Their values constrain the loop's local
  scope and the selected-word heap cell.
- Value influence: `scanAccum` affects the result list; `wordAfter` and
  `countAfter` affect the final flush; `charAfter` constrains the last loop
  target; `selectScan` is the entry postcondition.
- Value justification: exhaustive recursive equations that descend on `S`.
  Space/non-space, equal/not-equal count, empty/nonempty word, and
  vowel/non-vowel guards cover the full use domain.
- Dependents: `SPEC.select-words-loop` and `SPEC.select-words`.
- Control validation: not applicable; these equations do not replace
  execution.
- Value validation: the loop claim and entry claim both print `#Top`; the
  false-result probe is rejected on `("b", 1)`; 7,729 independent
  differential checks report zero mismatches.
- Equation audit: guard pairs are disjoint, except no overlapping equations
  remain with different right sides. Base equations terminate immediately;
  recursive equations consume one `iCons`; `flushSelected` is nonrecursive;
  `selectScan` expands once into the other structurally recursive definitions.

### Loop circularity

Extension: `SPEC.select-words-loop`.

- Class: derived lemma (auxiliary reachability claim).
- Semantic role: executes the fixed `#loop` rules and the exact Python loop
  body, then supplies a reusable universal loop theorem to the entry proof.
  It is not an ordinary rewrite in `verification.k`.
- Domain: all finite suffixes `S`, all integer local counts and words, all list
  accumulators, and `N >= 0`, with `result` pinned to a heap location containing
  a list.
- Matched context: exact `#loop(str(S), Name("ch"), charLoopBody)` at the head
  of `<k>` with the existing continuation framed; environment `L`; a closed
  ordinary local scope with the six source locals and parent 0; heap entry
  `H |-> list(A)`; all other cells and map entries framed and preserved.
- Justification scope and context containment: the claim proves precisely that
  matched configuration. The body contains no abrupt control, so the framed
  continuation is preserved by every fixed-semantics step.
- State footprint: reads `s`, `n`, `word`, `count`, `ch`, and `result`; writes
  `word`, `count`, `ch`, and heap entry `H`; preserves the remaining scope,
  heap, continuation, stack, return, exception, allocation, and exit cells.
- Value influence: determines every selected element and the loop-local values
  used by the final flush.
- Value justification: the exhaustive definitions above match the exact branch
  predicates in `charLoopBody`.
- Dependents: `SPEC.select-words`.
- Control validation: the focused loop proof printed `#Top`; the full proof
  printed `#Top`; the body mutation was rejected after fixed execution reached
  an empty result rather than the required `["b"]`.
- Value validation: the false postcondition was rejected with the concrete
  reached heap containing `["b"]`.

There are no proof-local operational bridges, priority rules, opaque result
oracles, or trusted primitives.

## Reproducible commands and actual results

The complete recorded runner is:

```bash
./prove.sh
```

Actual final line: `all positive checks passed; both negative probes failed as expected`

Actual exit: 0.

The runner contains these exact positive proof commands:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual `kprove` stdout in `proof-positive.out`:

```text
#Top
```

Actual `kprove` exit: 0. The Haskell compilation exited 0; its only diagnostics
were the supplied `str.k` unused-variable warnings for `As` and `Bs`.

Concrete execution uses the required module selection:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

Actual result: exit 0 with `.K` in `<k>` and `NoExc`; the complete final
configuration is in `krun-smoke.out`. LLVM compilation emitted only warnings
from unused or nonexhaustive supplied semantics functions outside this
program's exercised paths.

Differential command:

```bash
python3 test_solution.py
```

Actual output:

```text
differential checks: 7729; mismatches: 0
```

The scope was the five prompt examples, the empty-string boundary case, every
string over `"aB "` of lengths 0 through 6 paired with `n = 0..6`, and six
structured cases paired with `n = 0..11`. The oracle independently uses Python
`str.split()` plus a consonant-count comprehension.

False-postcondition command:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. For the satisfiable witness
`s = "b", n = 1`, the reached heap contains `["b"]` while the mutation requires
`[]`. Full output is in `vacuity.out`; the exit is in `vacuity.exit`.

Body-sensitivity command:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. Changing initial `count` from
0 to 1 reaches `[]` for `s = "b", n = 1`, while the original theorem requires
`["b"]`. Full output is in `body-mutation.out`; the exit is in
`body-mutation.exit`.

## Gate results

### Gate A — PASS

- A1: the exact program-defined function executes under fixed semantics.
  `solution.mpy` is regenerated from the unmodified translator, and the
  function-body mutation invalidates the original result.
- A2: no operational bridge skips state. The loop theorem explicitly tracks
  the local scope and result heap entry; framed cells are preserved.
- A3: the entry claim exercises loading, lookup, argument evaluation and
  binding, allocation, append, return, and frame pop. The loop claim pins a
  closed ordinary local frame and exact list binding, while preserving an
  arbitrary continuation.
- A4: all proof-local functions have exhaustive, terminating, compatible
  equations. No false off-domain rule, opacity, or execution preemption was
  found.
- A5: `("b", 1)` realizes the precondition, produces `["b"]`, and the false
  `[]` postcondition is rejected with exit 1.

### Gate B — PASS

- B1: the only precondition is `N >= 0`. The formal string domain is broader
  than the prompt's promised letters-and-spaces domain, so no intended input is
  excluded.
- B2: the supplied model represents strings as finite integer-code sequences
  and lists as heap objects. For the operations used here—iteration, ASCII
  literal equality/membership, concatenation, comparison, and append—this
  preserves the value distinctions needed by the prompt. CPython behaviors
  outside the supplied subset are excluded below.
- B3: implementation refinement to `selectScan` is formally proved.
  `selectScan`'s equations directly define the requested word boundary,
  consonant count, empty-token, and order behavior. The finite differential
  run independently supports, but does not replace, this formal connection.
- B4: all prompt examples and the empty-input case pass under both CPython and
  the supplied LLVM semantics.

### Gate C — PASS

- C1: the trust ledger below names all components outside the proof-local
  theorem. There is no hidden proof-local oracle.
- C2: every cited artifact and exact command exists. Positive proof, concrete
  execution, differential, false-result, and body-mutation evidence are
  reproducible through `prove.sh`.
- C3: this report separates the K theorem, conditional trust in the supplied
  semantics/toolchain, finite empirical evidence, and excluded behavior.

## Trust boundary

| Component | Why outside this theorem | Influence | Dependents | Evidence |
|---|---|---|---|---|
| Supplied `reference-semantics/` MPY rules | Fixed theory required by the task; not reproved here | Value, control, heap, scopes, exceptions | Both claims | LLVM prompt-example execution, CPython differential tests, direct source inspection |
| `py2mpy.py` | Fixed translator supplied by the task | Program identity | Entry claim/body comparison | `prove.sh` regenerates `solution.mpy`; translation succeeds deterministically |
| K v7.1.293 compiler and Haskell/LLVM backends | Verification toolchain trusted computing base | Compilation, symbolic closure, concrete execution | All machine results | Exit codes, `#Top`, concrete `.K`, and discriminating negative probes |
| CPython oracle in `test_solution.py` | Finite validation evidence, not part of the theorem | Adequacy evidence only | Gate C evidence | 7,729 checks, zero mismatches |

## Empirically supported facts

The prompt examples and empty case terminate with no K exception. The
independent Python oracle agrees on 7,729 recorded inputs. These are finite
evidence only; universal correctness comes from the two reachability claims
under the supplied K theory.

## Excluded behavior

- `n < 0`, non-integer `n`, and non-string `s` are outside the formal input
  contract.
- Inputs that violate the prompt's letters-and-spaces promise are proved
  against the implementation's literal non-vowel rule, but no English
  linguistic interpretation is claimed for punctuation or other symbols.
- Behaviors absent from the supplied subset—full CPython exception behavior,
  object identity details outside the modeled heap, concurrency, I/O, and
  implementation performance—are not claimed.
- The result is conditional on the supplied reference semantics, translator,
  and K toolchain. It is not an independent proof that those components
  implement all of CPython.
- Termination bounds and resource usage are not claimed.
