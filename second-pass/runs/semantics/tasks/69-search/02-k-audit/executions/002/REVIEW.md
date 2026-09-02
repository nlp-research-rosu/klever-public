# Independent adversarial review: 69-search

## 1. Input and provenance integrity

The audit infrastructure is intact. `/audit-input.json` declares
`record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
trusted mounts agree.

I independently checked the launcher inputs before using any candidate
artifact:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matches the recorded hash, and parses to exactly the `audit_campaign` object
  in `/audit-input.json`.
- All records required for `legacy-selected-stage1` are present, regular,
  readable, and non-symlinked: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  `usage.json` is present and was also checked. The absence of historical
  `runtime-metrics.json` is permitted for this layout.
- The independently computed hashes of every launcher-recorded regular file
  match `/audit-input.json`. The one structured trace file is 292 JSONL lines
  and matches the per-file hash in `generation-result.json`. The generation
  output is 16,646 lines. I inspected their commands, results, final claim, and
  the trace event structure only as untrusted generation history.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted prompt and translator.
- Recursive entry-type, relative-path, size, and byte-hash comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` succeeds for all 25 entries. There are no
  missing, additional, mistyped, changed, or symlinked semantics entries.
- All required candidate proof artifacts are regular files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`.

The full reproducible checks and independent tree manifests are in
`evidence/01_integrity.py`, `evidence/01-integrity.log`, and
`evidence/01-generation-records.log`. No candidate verdict is caused by an
infrastructure defect.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for any non-empty list of positive integers, return
the greatest positive integer whose frequency in the list is at least that
integer; return `-1` if none exists. The contract has no bound on list length
or integer magnitude.

`/candidate/solution.py` implements a quadratic nested-loop algorithm. For
each list value it counts equal elements, then retains the greatest value whose
count is at least the value. This differs from the trusted histogram algorithm
but implements the same contract over the intended domain.

In scratch, I ran the trusted translator as:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

The regenerated file is byte-identical to the submitted `solution.mpy`; both
have SHA-256
`dfdc8b41c7811f37945c70b0180db5eba0777a86cb249789b8242b9a7e0e52e1`.

The independent differential script imports the trusted canonical and
generated functions separately. It checked:

- all three documented examples;
- 11 branch/boundary cases, including exact frequency thresholds, one below
  and one above a threshold, multiple qualifying values, and a large sparse
  value;
- all 3,905 non-empty lists of lengths 1 through 5 over values 1 through 5;
- 2,000 seeded lists of lengths 1 through 30 over values 1 through 50.

There were zero mismatches across all 5,919 intended-domain cases. Empty and
non-positive lists were recorded separately: the implementations can diverge
there, but those inputs violate the explicit source precondition. Evidence is
in `evidence/02_differential.py` and `evidence/02-differential.log`.

Program fidelity therefore passes. This finite testing supports the
implementation-to-canonical bridge; it is not a universal K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/69-search`, used the trusted
semantics copy, and did not reuse any candidate definition or cache. The live
toolchain is K v7.1.293.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition 03-runtime-kompiled
krun 03_concrete_smoke.mpy --definition 03-runtime-kompiled --output none
```

Both commands exited 0. The concrete program contains the actual translated
nested-loop function and eight assertions spanning examples and branch
boundaries. See `evidence/03-concrete-build-run.log`.

Fresh proof reconstruction:

```text
kompile verification.k --backend haskell \
  --main-module SEARCH-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition 03-verification-kompiled
kprove spec.k --definition 03-verification-kompiled \
  --spec-module SEARCH-SPEC
```

The build exits 0. The submitted spec has one positive target claim; its
independent proof exits 0 and prints `#Top`. See
`evidence/03-symbolic-build-proof.log`. Compiler warnings concern unused
variables and non-exhaustive functions in unrelated parts of the supplied
semantics; no build or backend failure occurred.

This stage establishes proof closure under the candidate's extended theory. It
does not establish that the extension is sound.

## 4. Adequacy and real-program pinning

### Formal claim

The sole entry claim starts in an exact empty-heap, empty-stack module
configuration. Scope 0 binds `search` to a one-argument closure with body
`#searchBody`; the argument is the bare value `list(ALL:IntValSeq)`. Its
precondition is:

```text
nonEmpty(ALL) andBool allPositive(ALL)
```

Its postcondition requires the call to reduce exactly to
`greatestFreq(ALL)`. The result is not a free variable, tautology, or one-way
implication.

I parsed the submitted `solution.mpy` module and a module containing the
claimed `#searchBody` using the fresh definition with macro expansion. The two
KORE constructor terms are byte-identical, with SHA-256
`94d1a0b7dd206da880e91e6d1b7257fb2f7d911eef48b3d98aed129f30494e16`.
Thus the function binding and body are mechanically pinned even though the
claim starts at a direct closure call rather than module loading. Evidence is
`evidence/04-program-pinning.log`.

### Material input-domain substitution

The claim does not range over the supplied semantics' list sequences.
`verification.k:33-34` declares new productions:

```text
syntax IntValSeq ::= ".ValSeq" | vCons(Int, IntValSeq)
syntax ValSeq ::= IntValSeq
```

These are not the “same constructors” as asserted by the candidate comment.
Fresh KORE parsing shows:

- a real supplied-semantics `[1]` sequence uses
  `LblvCons...MPY-CORE...ValSeq...Val...ValSeq` and
  `Lbl.ValSeq...MPY-CORE...ValSeq`;
- the claim's conceptual `[1]` uses
  `LblvCons...SEARCH-VERIFICATION...IntValSeq...Int...IntValSeq` and
  `Lbl.ValSeq...SEARCH-VERIFICATION...IntValSeq`.

Their KORE hashes differ. The first is a normal `ValSeq`; the second is a
distinct constructor tree injected into `ValSeq`. See
`evidence/04-sequence-constructor-mismatch.log`.

This difference is operational. The supplied list iterator has rules only for
the two `MPY-CORE` constructors. With the proof-only bridge removed, a
satisfying formal witness corresponding textually to `[1]` gets stuck at:

```text
#iterNext(list(vCons(1, .ValSeq))) ~> #loopStep(...)
```

The bridge-free build succeeds and `kprove` exits 1 with
`WarnStuckClaimState`; see `evidence/04-fixed-vs-bridge-witness.log`. Removing
the bridge and rerunning the original universal claim produces the same
genuine residual (`evidence/05-no-bridge-residual.log`).

The local equations make the ghost value `oneSeq` a satisfiable formal
precondition: the bridge-enabled theory proves the ground conceptual results
`[1] -> 1`, `[2] -> -1`, `[2,2] -> 2`, and the first example to `2`. Both
Python implementations return those values for real lists
(`evidence/04-ground-witnesses.log` and `evidence/02-differential.log`).
However, this conceptual correspondence is informal and contradicted at the
constructor level. No real source list is an `IntValSeq` constructor tree.

The theorem therefore substitutes a ghost input domain for the unrestricted
HumanEval domain. This is a material adequacy failure, not a harmless
normalization or maintenance observation.

### Body and context sensitivity

A reviewer-authored mutation changes the actual closure body from `count += 1`
to `count += 2`. It no longer matches the bridge and the proof exits 1 with a
reachable loop residual (`evidence/04-body-sensitivity.log`). This shows
syntactic body sensitivity, but it does not validate the bridge's meaning.

More importantly, the bridge's `...` admits arbitrary continuations and it
does not preserve the loop's local writes. A fresh witness initializes
`count = 99`, executes the exact bridged outer loop on conceptual input `[1]`,
then returns `count`. Real Python and the fixed concrete K execution return
`1`, because the loop overwrites and increments `count`. The bridge-enabled
theory instead proves `#Top` for return value `99`, because it skips all loop
writes and changes only `result`. Exact commands and outputs are in
`evidence/04-bridge-context-witness.log`.

This is a concrete false-conclusion witness for the bridge rule on a positive,
non-empty input under the very ghost-to-list interpretation the candidate
needs.

## 5. Rule-by-rule static soundness review

`evidence/05-rule-inventory.txt` is the exhaustive, line-addressable inventory
of all modules, imports, configurations, syntax declarations, contexts,
ordinary rules, attributes, and the claim. It contains 227 supplied-semantics
syntax declarations and 695 supplied-semantics rules, plus 10 local syntax
declarations, 15 local rules, and one claim. There are no local
`simplification`, `functional`, `anywhere`, or opaque-symbol declarations. The
per-file counts and compiled labels are in `evidence/05-static-summary.log`.

Every supplied-semantics rule is assigned below; this is the selected fixed
semantics, not candidate proof material:

| Modules | Rules | Static disposition |
|---|---:|---|
| `MPY-CORE` | 46 | Fixed configuration, scope, literal, sequencing, lookup, allocation, truth, and sequence helpers. Used-path rules preserve the modeled cells and ordinary unbounded-integer behavior. |
| `MPY-CALL`, `MPY-FUNCTIONS` | 36 | Fixed left-to-right call, argument binding, frame, return, and pop behavior. The entry claim exercises these rules without a discovered overlap or control defect. |
| `MPY-CONTROLS`, `MPY-LIST`, `MPY-OPERATORS`, `MPY-INT`, `MPY-ITER` | 87 | Fixed assignment, loop protocol, list iteration, comparison, and integer arithmetic. Concrete execution validates the used ground path. The ghost constructors do not match these list-iteration rules. |
| `MPY-ASSERT`, `MPY-CONCRETE` | 19 | Used only by the fresh LLVM smoke run; not imported into the Haskell proof module. |
| `MPY-BOOL`, `MPY-BUILTINS`, `MPY-COMPREHENSION`, `MPY-DICT`, `MPY-FLOAT`, `MPY-METHODS`, `MPY-RANGE`, `MPY-SET`, `MPY-SORT`, `MPY-STR`, `MPY-SUBSCRIPT`, `MPY-TUPLE` | 507 | Fixed selected-semantics rules. They contain no `search`-specific conclusion and do not occur on the reconstructed proof path except ordinary Boolean/value infrastructure. Their unused gaps cannot justify the local bridge. |
| `MPY-SYNTAX`, assembled `MPY`/`MPY-KRUN` | 0 | Declarations/import composition only. |

The 15 local rules are exhaustively classified as follows:

| Local extension | Count | Decision |
|---|---:|---|
| `#innerBody`, `#outerBody`, `#searchBody` macros | 3 | Valid syntax macros. Fresh macro expansion is constructor-identical to the submitted body. |
| `allPositive` | 2 | True, disjoint, structurally terminating equations over the ghost sequence sort. |
| `nonEmpty` | 2 | True, disjoint, total equations over the ghost sequence sort. |
| `frequency` | 2 | True structural recurrence over the ghost sequence sort. |
| `chooseFreq` | 2 | The guard and its negation are disjoint and exhaustive; right-hand sides implement the stated selection step. |
| `greatestFreq`, `greatestFreqFrom` | 3 | Structurally descending, total definitional fold; it computes the intended frequency condition over ghost sequences. |
| Outer `For` accelerator at `verification.k:77-86` | 1 | Illegitimate and unsound operational bridge. |

The two local `IntValSeq` constructor productions and its subsort declaration
are syntax rather than rules. They are nevertheless the source of the
real-domain substitution described in Stage 4.

### Operational bridge audit

The accelerator matches:

- the exact outer `For` syntax and `#outerBody`;
- any active continuation admitted by `<k> ... ... </k>`;
- any current scope map containing `lst` and `result`;
- ghost `lst = list(ALL)`, `result = -1`, and `allPositive(ALL)`;
- no particular stack, return, exception, heap, heap-location, or continuation
  state.

It replaces the loop with a single assignment of
`greatestFreq(ALL)` to `result`, at priority 40. Real execution reads `lst` and
writes `value`, `item`, `count`, and sometimes `result`; the bridge preserves
only the final `result` summary. There is no bridge-free universal connection
claim, no loop invariant claim, and no derivation covering its arbitrary
continuation and state footprint. The bridge-free proof instead gets stuck.

The `count = 99` witness described in Stage 4 is the required false conclusion:
the fixed program returns `1`, while this rule enables a proof that the same
loop region followed by an admitted continuation returns `99`. Thus the
priority rule is not a sound theorem about its complete match domain. It also
fabricates progress for ghost list values on which fixed `#iterNext` has no
rule. The target `#Top` depends on precisely this bridge.

The complete explicit-symbol inventory is
`evidence/05-opaque-symbols.log`. The supplied semantics declares 25 named
symbols: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
`toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs on this proof's
path or in its result. There is no proof-local opaque value to justify the
bridge.

## 6. Fresh non-vacuity test

I did not rely on the candidate's mutation. The fresh
`06_false_postcondition.k` changes the destination to:

```text
greatestFreq(ALL) +Int 1
```

For satisfying conceptual input `[1]`, the real and generated Python result is
`1` while the mutated destination is `2`.

The mutation dry-run exits 0, proving the artifact parses and builds. The
actual `kprove` exits 1 with `WarnStuckClaimState`. Its residual says the
configuration unifies with the destination but the implication between
`greatestFreqFrom(ALL, ALL, -1)` and that value plus one fails. This is the
expected unmet result obligation, not a parser error, timeout, unreachable
mutation, or unrelated crash. See `evidence/06-false-postcondition.log`.

The claim is therefore result-constraining and non-vacuous. This does not cure
the substituted input representation or unsound bridge.

## 7. Proven versus assumed accounting and verdict

The successful reachability proof establishes only this conditional statement:
under the supplied semantics plus all candidate extensions, for any
`SEARCH-VERIFICATION.IntValSeq` ghost constructor tree satisfying the local
positive/non-empty predicates, an exact call to the exact submitted closure
body reaches the local `greatestFreq` fold. The proof closes because the
priority bridge replaces the entire property-bearing loop.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied K semantics and K built-in Int/Bool/String/Map/List/K-equality hooks | Concrete execution and all proof steps | Acceptable selected fixed-semantics boundary. It does not bless local proof rules. |
| Exact source-to-`solution.mpy` translation | Program identity | Strong: trusted regeneration is byte-identical. |
| Macro body equals submitted function body | Entry closure | Strong: fresh macro-expanded KORE terms are byte-identical. |
| Local `greatestFreq` equations | Formal postcondition | Acceptable mathematics over the local ghost datatype; fully defined rather than opaque. |
| `IntValSeq` represents real positive Python lists | Entire universal input claim | Illegitimate. Compiled constructors are distinct, and fixed list iteration cannot consume them. |
| Outer-loop bridge equals fixed execution | Sole positive target proof | Illegitimate. No connection theorem exists; bridge-free proof is stuck; a fresh continuation witness gives a false observable result. |
| 5,919 Python differential cases | Implementation-to-canonical equivalence | Useful finite empirical support only; not a universal execution connection and not a K proof. |
| Eight fixed-semantics concrete K assertions | Used ground MPY behavior | Useful finite support only. |
| 25 supplied opaque/named symbols | None on the proof path | Acceptable but irrelevant trust boundary. |

The candidate algorithm appears correct, and the submitted target is
non-vacuous, but the K proof is not a proof of that real algorithm over the
HumanEval domain. It proves a ghost-sequence theorem using an operational rule
that both bypasses the nested loops and is observably false over its admitted
continuations. Under the benchmark decision boundary, a substituted program
domain or materially unsound proof rule is `FAIL / NOT_LEGIT`, irrespective of
the fresh `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
