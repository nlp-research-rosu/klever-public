# Independent adversarial review: 47-median

The candidate is **not a legitimate partial-correctness proof of the real
generated task program**. Its K claims do reconstruct and close, the claim term
does pin the submitted `solution.mpy`, and a false-postcondition mutation is
properly rejected. Those positive facts establish only a theorem about the
submission's own wrong upper-middle-pair algorithm under its own materially
unsound/restricted semantics.

There are three independently fatal findings:

1. `solution.py` differs from the trusted canonical on the entire general
   even-length branch. The candidate averages sorted indices `n//2` and
   `n//2+1`; the canonical averages `n//2-1` and `n//2`.
2. The only universal claim is restricted to K integer lists of length at least
   three. The canonical works on length-one and length-two lists and on
   comparable numeric lists containing floats. This materially narrows the
   source-contract domain.
3. The generated semantics makes false Python-behavior conclusions. In
   particular, it models every integer `/` as an exact `floatVal` pair, so a
   claim-domain input containing four `10**400` integers returns normally in K
   while CPython raises `OverflowError`. Its incomplete `nthInt` is also marked
   `[total]` and can be exposed as a fabricated result-bearing term after K has
   consumed the computation.

The command ledger is in `evidence/COMMANDS.md`; reviewer scripts, mutations,
and bounded logs are all under `evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `47-median`, condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- no mounted reference semantics.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required legacy-selected
generation record, optional `usage.json`, the legacy records that were present,
the complete structured JSONL trace, and all candidate/reference entries.
`evidence/generation_trace_summary.log` is a bounded record-by-record rendering
of the 209-line trace; it treats the generation's `#Top` and final report only
as untrusted historical claims.

Integrity results:

- The campaign object is exactly equal to `/audit-campaign-lock.json`, whose
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All required mounts and records are readable regular files/real directories.
  No entry in the candidate, reference, or generation-evidence trees is a
  symlink or unsupported type.
- Every recorded per-file hash matches: run/task/result/invocation/metrics,
  prompt, usage, Codex output/last message, trusted canonical/prompt/translator,
  candidate prompt/translator, and the JSONL trace. The invocation and result
  evidence maps are identical.
- The independently recomputed pipeline tree hash for `/candidate` is
  `43b78374...`, exactly the retained workspace hash in both
  `generation-result.json` and `invocation.json`. The independently recomputed
  trace tree hash is `bff1f21e...`, exactly `usage.json`'s source-trace hash.
  `audit-input.json` also carries separate audit-snapshot tree digests under
  its own packaging scheme; all mounted constituent files and the provenance
  tree anchors above match.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required in
  `GENERATED_SEMANTICS` mode.

The complete independent hashes/types are in
`evidence/stage1_integrity-final2.log`; source-only scratch-copy hashes are in
`evidence/scratch_copy_hashes.log`. There is no infrastructure breach, so a
candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`prompt.py` says to return the median of the list. The trusted canonical sorts
the input, returns the element at `n//2` for odd length, and returns the average
of the two central elements at `n//2-1` and `n//2` for even length.

The prompt's second doctest says `15.0` for
`[-10,4,6,1000,10,20]`, which contradicts both the ordinary meaning of
"median" and the trusted canonical: the canonical returns `8.0`. The candidate
explicitly chose the doctest's erroneous upper pair and returns `15.0`.
Because the benchmark designates `/reference/canonical.py` as trusted and
requires direct differential comparison to it, that choice is a program
fidelity failure, not a permissible alternative implementation.

### Translation fidelity

Running the trusted translator on scratch `solution.py` produced SHA-256
`22ebb0b2...`, byte-identical to submitted `solution.mpy`
(`evidence/translation_identity.log`). Thus the submitted `.mpy` accurately
represents the submitted Python; it is the Python algorithm itself that is
wrong.

### Differential results

`evidence/differential.py` independently imports the trusted canonical and
submitted functions. It covers both doctests, empty/length-one/length-two
boundaries, the first odd/even branch sizes, order/duplicate/negative cases,
integer lengths 1 through 12, and float lengths 1 through 8, with a fixed seed
and every generated input recorded.

The run covered 164 inputs and found 81 mismatches
(`evidence/differential.log`, expected exit 1). Representative witnesses:

| Input | Trusted canonical | Submission |
|---|---:|---:|
| `[-10,4,6,1000,10,20]` | `8.0` | `15.0` |
| `[2,10]` | `6.0` | `IndexError` |
| `[1,2,3,4]` | `2.5` | `3.5` |
| `[1.5,-2.0,8,4.25]` | `2.875` | `6.125` |

Odd-length cases generally agree. Empty input raises `IndexError` in both.
The branch-wide even divergence is material on the intended domain.

## 3. Clean proof reconstruction

All candidate-built definitions/caches were ignored. Only source artifacts and
trusted inputs were copied to `/tmp/audit-work/candidate-src`. The live tools
are K `v7.1.293` (`evidence/toolchain.log`).

### Fresh builds

Concrete generated semantics, excluding the proof-local module from the main
import closure:

```text
kompile --backend llvm semantic.k \
  --main-module MEDIAN-SEMANTICS \
  --syntax-module MEDIAN-SYNTAX \
  --output-definition concrete-kompiled
```

Exit 0. The compiler warned that `[total] nthInt` has the uncovered pattern
`nthInt(nil,_)` (`evidence/build-concrete.log`).

Proof definition:

```text
kompile --backend haskell semantic.k \
  --main-module SEMANTIC \
  --syntax-module MEDIAN-SYNTAX \
  --output-definition proof-kompiled
```

Exit 0 (`evidence/build-proof.log`).

### Positive claims

The exact submitted `spec.k` closes as a whole:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
#Top
EXIT_STATUS=0
```

I made an otherwise identical scratch spec with declaration labels and replayed
each claim separately. Main, odd example, and even example each printed
`#Top` and exited 0. See `evidence/kprove-all-positive.log`,
`evidence/kprove-main-rerun.log`, `evidence/kprove-example-odd.log`, and
`evidence/kprove-example-even.log`.

### Generated-semantics execution

Fresh `krun` agrees with the submitted Python on ordinary modeled integer
inputs: odd `[3,1,2,4,5]` gives `intVal(3)`, the submitted even doctest gives
`floatVal(30,2)`, `[1,2,3,4]` gives `floatVal(7,2)`, and negative/duplicate
cases agree under the intended rational interpretation.

Boundary and large-integer checks expose gaps:

- Empty and length-two runs each exit 113 at `nthInt(nil,0)` rather than
  modeling Python exceptions.
- Four `10**400` integers satisfy the main claim's K precondition. Submitted
  Python raises `OverflowError: integer division result too large for a float`;
  K consumes `<k>` and returns
  `floatVal(2*10**400,2)` with exit 0.

Python observations, exact `krun` commands, statuses, and outputs are preserved
in `evidence/concrete_checks.log`.

Fresh reconstruction therefore confirms the historical `#Top`, but also
confirms that it is a theorem under an inadequate/unsound candidate theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Main claim:** for any K `Ints` list `IS` with `lenInts(IS) >= 3`,
   execute the manually embedded submitted `median` constructor body to
   completion and put `promptMedian(IS)` in the result cell.
2. **Odd example:** execute the same body on `[3,1,2,4,5]`, consume the
   computation, and return `intVal(3)`.
3. **Even example:** execute the same body on
   `[-10,4,6,1000,10,20]`, consume the computation, and return
   `floatVal(30,2)`.

The returned value is constrained; it is not a fresh variable, tautology, or
one-way implication. There are no loops, helper bodies, or helper reachability
claims.

### Program identity

Trusted regeneration proves `solution.py -> solution.mpy` byte identity.
Removing whitespace, each of the three `<k>` constructor terms compares equal
to all of `solution.mpy` (`evidence/program_term_comparison.log`). The omitted
Python parameter annotation is a typing-only transliterator behavior and does
not alter the entry-point return computation.

The term is manually duplicated rather than sourced automatically, which is a
maintenance risk but not a failure for this immutable candidate. A genuine
body-sensitivity mutation changed the executed term's second even index from
`middle + 1` to `middle + 0`; the main proof then exited 1 at the changed result
equality (`evidence/body-mutation-source.log` and
`evidence/body-mutation-kprove.log`). Thus the theorem depends on the embedded
body.

### Satisfiable precondition and substituted results

`[9,1,5]` and `[1,2,3,4]` both satisfy `len >= 3`.

- On `[9,1,5]`, the claim, submitted Python, trusted canonical, and K all
  produce 5.
- On `[1,2,3,4]`, the claim/K produce `floatVal(7,2)` and the submission
  produces `3.5`, but the trusted canonical produces `2.5`.

See `evidence/precondition_witnesses.log`. The second witness shows that the
formal result is faithful to the wrong submitted program, not the real task.

### Domain and intent

The main theorem permits arbitrarily long integer lists but requires length at
least three. It therefore excludes canonical terminating cases of length one
and two, and its `Ints` syntax excludes floats even though the unqualified
Python `list` contract/canonical support comparable numeric lists. This is a
material domain narrowing. Under the benchmark's explicit mapping, such a
`SOUND-BUT-LIMITED` domain restriction is `FAIL / NOT_LEGIT`, not a concern.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.md` is the exhaustive inventory: all local syntax,
cells, functions, four `[total]` declarations, opaque/result-bearing terms,
37 semantic rules, two proof-local equations, construct coverage, overlaps,
guards, state, and control. There are no local priorities, simplification
rules, `[functional]` declarations, or auxiliary claims.

In compact form:

- R01-R02 (environment lookup), R03-R11 (literal/name/call/subscript
  evaluation), R12-R14 (integer `+`, length `//`, length `%`), R16-R19
  (integer truth/length), R20-R26 (in-range indexing and insertion sort),
  R27-R37 (body, branch, continuation, module entry, and return) are sound on
  their stated used cases. Sort/insert recursion descends; paired guards are
  disjoint.
- The special immediate-return `if` rule R30 overlaps general R31. On the
  modeled pure expressions and integer condition, both ground paths converge,
  preserve the same cells, and discard the same continuation. I found no false
  conclusion witness for its accepted used domain, so I do not label this
  overlap unsound.
- Minimal syntax coverage is otherwise acceptable in generated-semantics mode:
  every constructor in `solution.mpy` has syntax and behavior; unused Python
  constructs need not be modeled.

Material failures:

1. **R15, `binopVal("/", intVal(I), intVal(J)) => floatVal(I,J)`: unsound.**
   It claims exact rational pairs model Python float division. The four
   `10**400` witness produces a normal K result but a Python `OverflowError`.
   This is a concrete false conclusion on the main theorem domain, not merely
   an untested edge.
2. **`nthInt [function,total]`: unjustified and result-bearing.** Its equations
   omit empty and negative-index cases; the fresh LLVM compiler reports the
   non-exhaustive match. More strongly, K proves the reviewer claim that the
   length-two submitted program consumes `<k>` and normally returns
   `floatVal(10 +Int nthInt(nil,0),2)`, while submitted Python raises
   `IndexError`. The exact witness claim and `#Top` are
   `evidence/spec-oob-totality-witness.k` and
   `evidence/oob-totality-witness-kprove.log`.
3. **V02, the `promptMedianSorted` result definition: false as the task
   reference.** It duplicates the submitted upper-pair formula. The concrete
   witness `[1,2,3,4]` gives `7/2` versus canonical `5/2`. It does not bypass
   the submitted body's execution, but it supplies the wrong correctness
   target and has no connection theorem to the canonical median.
4. **`floatVal` is an opaque result boundary without a truthful bridge.** No
   equation relates the pair to CPython rounding, overflow, signed zero, or
   actual float values. Both the operational division and postcondition depend
   on the same representation, so their agreement is not evidence that the
   representation has Python meaning.

The proof does not replace the body with `promptMedian`; fixed candidate
execution reaches a syntactically matching expression. Hence this is not a
vacuous operational-oracle proof. It is nevertheless illegitimate because the
executed program is wrong and the semantics/postcondition bridge can prove
false behavior.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a fresh
scratch `SPEC-VACUITY` that leaves the exact program and precondition unchanged
but changes the main result obligation from `promptMedian(IS)` to `intVal(0)`.

The mutation is demonstrably false at satisfying input `[9,1,5]`, where both
Python implementations and K return 5.

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --claims SPEC-VACUITY.main --dry-run
EXIT_STATUS=0

kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --claims SPEC-VACUITY.main
WarnStuckClaimState
... intVal(0) #Equals ifVal(...)
EXIT_STATUS=1
```

The artifact builds successfully, reaches the result implication, and fails
for the expected unmet equality. It is not a parser error, timeout, unrelated
crash, or unreachable mutation. See `evidence/spec-vacuity.k`,
`evidence/vacuity-dry-run.log`, and `evidence/vacuity-kprove.log`.

The submitted theorem is therefore result-constraining and non-vacuous. This
positive gate does not cure the wrong program, narrowed domain, or false
semantics.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the candidate K definition, for every K constructor list of
mathematical integers whose modeled length is at least three, the exact
submitted constructor body rewrites to the value named by the candidate's
`promptMedian` definition. It also establishes the two submitted example
claims. Nothing in the K theorem establishes that this value is the trusted
canonical median or that `floatVal` is a CPython float result.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, reachability prover | All builds/runs/proofs | Ordinary low-level tool trust; acceptable. |
| Imported K `INT`/`STRING` operations and generated K-list syntax | Arithmetic, guards, environments, lists | Ordinary low-level primitives; acceptable for mathematical integers/strings. |
| Trusted `py2mpy.py` | Program-term identity | Acceptable; independently regenerated byte-identical `.mpy`. |
| Manual constructor copy in each claim | Program pinning | Mechanically equal now and body-sensitive; acceptable for immutable candidate, with maintenance risk only. |
| Candidate insertion-sort/length/in-range-index equations | Program execution and `promptMedian` | Audited directly; sound on in-range mathematical integer inputs. No finite test is treated as a universal proof. |
| `nthInt [total]` outside covered equations | Indexing, result definedness, main proof reasoning | Illegitimate global totality/result boundary; false-normal-return witness reproduced. |
| `floatVal(I,J)` as exact Python `/` | Every even result and main postcondition | Illegitimate; overflow witness falsifies it on the claim domain, and no universal connection theorem exists. |
| `promptMedianSorted` meaning "median" | Main postcondition | Illegitimate; it duplicates the wrong submitted even formula and conflicts with trusted canonical on a concrete satisfying input. |
| Integer-only, length-at-least-three precondition | Universal theorem scope | Material source-contract narrowing; benchmark requires `FAIL / NOT_LEGIT`. |
| Differential/concrete tests | Fidelity and bridge evidence | Finite evidence only. Here it supplies decisive counterexamples; it is not used as a substitute for a universal K proof. |

### Gate/accounting conclusion

- Fresh verification: **PASS** (`#Top` for all positive claims).
- Real-program/body pinning and non-vacuity subchecks: **PASS** for the
  submitted body.
- Gate A semantic soundness: **FAIL** because R15 and uncovered result-bearing
  `nthInt` enable false Python conclusions.
- Gate B intent/domain adequacy: **FAIL** because the submitted program and
  `promptMedian` disagree with the trusted canonical on even lists, and the
  universal theorem materially narrows the source domain.
- Evidence reproducibility: all cited scripts, inputs, commands, outputs, and
  statuses are preserved, but evidence quality cannot make a false theorem
  legitimate.

The candidate's reconstructed `#Top` is genuine closure under its supplied
theory, but it is not a proof of the real HumanEval task. The required mapping
is therefore `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
