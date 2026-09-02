# Independent adversarial review: 35-max-element

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of its submitted program under the supplied MPY semantics. I rebuilt both
definitions from source, ran all eight positive claims through their two spec
modules, obtained fresh exit-0 `#Top` results, mechanically pinned the entry
claims to the regenerated program term, audited all 55 proof-local rules, proved
the comparison bridge equations again without the three operational
`applyCmp(">")` simplifications, and rejected fresh false-result and body
mutations.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the fixed
supplied model has documented behavior/representation gaps on source-contract
inputs that CPython handles. The concrete witness
`[[1, 9], [2], [1, 10]]` returns `[2]` from both the trusted canonical function
and the submitted Python function, but the unmodified supplied semantics stops
at `#iterYield(ref(0), ...) ~> #maxCont0`: it has no nested-list ordering
branch. Non-ASCII string literals also fail at the supplied input encoding.
The candidate did not create either restriction, its theorem covers every
normally returning `max` domain that the fixed model implements, and its Python
program is faithful to canonical on the gap. This is the supplied-model
exception in campaign amendment v2.

## 1. Input and provenance integrity

Status: **PASS**.

- `/audit-input.json` declares `record_layout: pipeline-v3`,
  `semantics_mode: SUPPLIED_SEMANTICS`, problem `35-max-element`, and the
  expected container mounts. `/reference/reference-semantics` is present.
- `/audit-campaign-lock.json` is a regular file, hashes to the recorded
  `e71e1d...d40d0e`, and its parsed object is exactly equal to the
  `audit_campaign` object in `/audit-input.json`.
- I inspected all pipeline-v3 records required by the prompt:
  `/run.json`, `/task.json`, `/generation-result.json`, the six JSON/text
  records under `/generation-evidence`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and all 594 JSONL records in the structured
  trace. Every trace record parsed. These generation records were used only as
  untrusted historical claims.
- All launcher-recorded individual file hashes recomputed exactly, including
  the canonical, prompt, translator, campaign lock, manifests, generation
  records, output log, and prompt. The trace file's SHA-256
  `bea7a58e...b5a7c1` matches `/generation-result.json`.
- Independently applying the pipeline tree-hash implementation to the mounted
  candidate produces `8a6526d1...749d2`, exactly the successful generation
  workspace hash. The trusted and candidate semantics trees both produce
  `4495a50f...29ad1`, exactly the pipeline manifest semantics hash, and a
  recursive `diff -qr` exits 0. The audit manifest also contains alternate
  directory-content digest fields whose canonicalization is not declared; I
  did not conflate those with the pipeline tree-hash namespace. Direct
  recursive comparison is decisive here.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted versions. Candidate and trusted supplied-semantics trees
  contain the same 24 regular files, with no missing, additional, mistyped, or
  symlinked entry. No candidate artifact is a symlink.
- All required proof artifacts are present as regular files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
  `PROOF.md`.

Evidence:

- [core records and manifests](evidence/01-core-records.log)
- [individual hashes and recursive semantics comparison](evidence/01-hash-integrity.log)
- [campaign equality and declared hash checks](evidence/02-source-and-claims.log)
- [structured trace inspection](evidence/01-trace-inspection.log)
- [pipeline tree hashes](evidence/01-tree-hashes.log)

The first inventory command attempted `jq`, which is absent, then continued.
The records were subsequently read with `sed` and parsed with Python. This did
not affect the integrity result.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS**, with one invalid-input exception-class observation.

The trusted prompt says to return the maximum element in a list. The trusted
canonical implementation seeds `m` with the first element, replaces it only
when a later element is strictly greater, and therefore retains the first
maximum on ties. A successful result presupposes a nonempty list whose elements
are mutually orderable. The empty list has no maximum; the canonical happens
to raise `IndexError`.

The submitted implementation is:

```python
def max_element(l: list):
    return max(l)
```

That is a different algorithm but has the same value and first-tie behavior for
ordinary nonempty comparable Python values. Running the trusted translator on
the submitted `solution.py` produced SHA-256
`b040afa3...b8791`, byte-identical to submitted `solution.mpy`.

The independent differential script imports `/reference/canonical.py` and
`/candidate/solution.py` directly. It exercised:

- both documented examples;
- empty, singleton, replacement, keep, and tie boundaries;
- negative integers, booleans, homogeneous and mixed floats/integers, the
  `2**53` comparison boundary, infinities, NaNs, and signed zero;
- ASCII and Unicode strings;
- incomparable mixed values;
- nested lists and tuples as supplied-model-gap witnesses;
- 150 seeded generated nonempty integer lists and 50 seeded generated string
  lists.

All 220 nonempty/boundary/generated comparisons matched in returned type,
representation, and selected list-element identity, or in exception class.
There were zero material mismatches. The sole recorded difference was empty
input: canonical raises `IndexError`, while `max([])` raises `ValueError`.
Because the contract asks for a maximum element and none exists, this is an
excluded exceptional boundary rather than a result-domain defect.

Evidence:

- [trusted regeneration and tool versions](evidence/02-regeneration-and-toolchain.log)
- [differential script](evidence/differential_test.py)
- [complete differential inputs and results](evidence/02-differential.log)

## 3. Clean proof reconstruction

Status: **PASS**.

I copied only source artifacts to `/tmp/audit-work/rebuild`; the candidate's
`runtime-kompiled`, `verification-kompiled`, caches, binaries, and prior proof
outputs were not copied or used.

Fresh concrete reconstruction:

```text
kompile --backend llvm \
  /tmp/audit-work/rebuild/reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/rebuild/runtime-kompiled
```

This exited 0. The reviewer smoke program was translated with the trusted
translator and run with the fresh definition. It finished with `<k> .K </k>`,
`NoExc`, and exit code 0 on examples, both comparison branches, ties,
booleans, strings, mixed numerics, floats, and the `2**53` boundary. An initial
wrapper attempt reported only that `/usr/bin/time` was absent; the actual
`kompile` command was immediately run directly and succeeded.

Fresh proof reconstruction:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/rebuild/fresh-verification-kompiled

kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC-STR
```

The build exited 0. Each independent module proof exited 0 and printed exactly
the success signal `#Top`. `SPEC` contains and therefore ran six positive
claims; `SPEC-STR` contains and ran the remaining two. Compiler warnings are
unused-variable warnings in the fixed `str.k`, not stuck claims.

Evidence:

- [fresh LLVM build](evidence/03-kompile-llvm-retry.log)
- [fresh concrete successful execution](evidence/03-krun-concrete.log)
- [fresh Haskell build](evidence/03-kompile-haskell.log)
- [fresh `SPEC` proof](evidence/03-kprove-module-SPEC.log)
- [fresh `SPEC-STR` proof](evidence/03-kprove-module-SPEC-STR.log)

## 4. Adequacy and real-program pinning

Status: **PASS relative to the supplied model**, with the model-gap concern
described below.

### Claims in plain language

The four auxiliary circularities say:

1. `max-int-numeric-acc`: an integer-seeded fixed `#maxAcc` over any finite
   numeric remainder reaches `maxIntNumericVS(seed, remainder)`.
2. `max-float-numeric-acc`: a float-seeded fixed `#maxAccF` over any finite
   numeric remainder reaches `maxFloatNumericVS(seed, remainder)`.
3. `max-general-numeric-acc`: a general-value fixed `#maxAccV`, with a numeric
   seed and numeric remainder, reaches the strict-comparison numeric summary.
4. `max-general-str-acc`: the same fixed `#maxAccV`, with a string seed and
   all-string remainder, reaches the lexicographic string summary.

The four entry claims load and bind the exact `max_element` function, call it
through ordinary MPY name lookup and function-call rules, and require it to
return the corresponding summary for an integer-, float-, Boolean-, or
string-headed nonempty list. The numeric tail may contain any mixture of
`Int`, `Bool`, and `Float`; the string tail is all `Str`. Recursive
preconditions do not bound length.

### Mechanical program identity

Whitespace-normalizing the trusted regenerated program gives:

```text
Module(FuncDef("max_element",Params("l"),Return(Call(Name("max"),Name("l")))))
```

That exact constructor term occurs four times in `spec.k`, once in each entry
claim. The exact body occurs both in each loaded function and in each
post-load closure binding. The only source normalization is omission of the
typing annotation by the trusted translator; it has no runtime effect.

The fixed rules, not proof shortcuts, perform module loading, definition
binding, `Name("max_element")` lookup, frame allocation, parameter binding,
`Return`, `Name("max")` lookup through the builtins parent, argument
evaluation, `max` dispatch, iterator folding, frame pop, and return. The entry
postconditions constrain the final result and explicitly constrain environment,
scopes, scope counter, heap, heap counter, stack, return cell, exception cell,
and exit code. Read-only list arguments use the supplied model's documented
bare `list(ValSeq)` representation; the submitted body does not mutate them.

Concrete satisfying witnesses exist for every entry and auxiliary
precondition. For example:

- integer seed `1`, remainder `[2, -3]` gives `2`;
- float seed `1.5`, remainder `[-2, 3.25]` gives `3.25`;
- Boolean seed `False`, remainder `[True, False]` gives `True`;
- string seed `"ant"`, remainder `["zebra", "yak"]` gives `"zebra"`.

Every substituted summary equals both Python implementations. A body mutation
that changes the executed constructor body to `Return(Int(0))` contains no
original program term; its fresh proof reaches `0` while demanding `1` and
fails with `WarnStuckClaimState`, exit 1.

Evidence:

- [mechanical constructor comparison and fixed-rule map](evidence/04-program-pinning.log)
- [satisfying witnesses and substituted results](evidence/04-claim-witnesses.log)
- [body-sensitivity execution](evidence/04-body-sensitivity.log)

### Domain alignment and campaign amendment

The claims cover every nonempty list on which the fixed supplied `max` fold
normally returns: arbitrary numeric mixtures and homogeneous strings. The
fixed seed rules admit only `Int`, `Float`, `Bool`, and `Str`; incomparable
numeric/string mixtures correctly have no successful comparison path.

The supplied model cannot implement every CPython-orderable value class or
input encoding:

- **Concrete divergence witness:** for
  `[[1, 9], [2], [1, 10]]`, canonical and submitted Python both return `[2]`.
  Fresh MPY execution represents the inner lists as references but stops at
  `#maxCont0` because the fixed semantics has no list/list ordering rule.
- **Encoding witness:** translating `["é", "😀", "Ω"]` succeeds, but fresh
  MPY execution fails in the supplied scanner/string-literal path; the fixed
  concrete string rule is ASCII-only. The symbolic `Str` entry claim itself
  ranges over arbitrary `IntSeq`, so this is an input-encoding gap rather than
  an extra theorem precondition.

The candidate explicitly records nested list/tuple and user-comparison
behavior as fixed language-model boundaries in `PROOF.md`. The audit trust
ledger below adds the required concrete witnesses. The theorem has no
candidate-added restriction inside the model's successful domain, and the
submitted Python is canonical-faithful on both witnesses. Campaign amendment
v2 therefore maps this limitation to `CONCERNS / LEGIT`, not
`FAIL / NOT_LEGIT`.

Evidence:

- [nested-list fixed-model stuck state](evidence/03-krun-model_gap_nested.log)
- [Unicode supplied-encoding failure](evidence/03-krun-model_gap_unicode.log)
- [Python gap witnesses in the differential run](evidence/02-differential.log)

## 5. Rule-by-rule static soundness review

Status: **PASS**.

### Exhaustive inventory

The reviewer inventory enumerates every module/import, configuration, syntax
declaration, context, rule, guard, attribute, and claim in the supplied
`semantics.k`, all 23 supplied helper files, `verification.k`, and `spec.k`.
It contains 1,434 declaration records, including all functions, total symbols,
opaque/no-evaluator symbols, priorities, simplifications, concrete/symbolic
rules, ordinary operational rules, and all eight claims.

- [inventory generator](evidence/rule_inventory.py)
- [complete 1,434-record inventory](evidence/05-rule-inventory.tsv)
- [raw declaration/rule index](evidence/05-rule-inventory.log)
- [program-relevant fixed-rule excerpts](evidence/05-relevant-supplied-rules.log)

The supplied tree is immutable trusted input, not candidate-authored proof
theory. Nevertheless, I mapped every constructor used by `solution.mpy` to the
fixed syntax and inspected all rules reachable from this program:
configuration and `#loadAll`; statement sequencing and `FuncDef`; lookup and
builtin scope; callee-before-argument evaluation; closure frame allocation and
parameter binding; strict `Return` and frame pop; list dereference; iterator
order; integer, float, general-value, and string `max` folds; and all numeric
and string comparison dispatch. The fixed rules preserve the continuation and
all cells they omit. No candidate rule changes allocation, binding, lookup,
evaluation order, control transfer, heap, exceptions, output, or exit status.

### All 55 proof-local rules

The following table is exhaustive by family; the exact individual entries,
guards, and attributes are in the inventory cited above.

| `verification.k` lines | Rules | Classification and decision |
|---|---:|---|
| 7–18, 44–55, 66–90 | 16 | Four guarded projection families (`Int`, `Float`, `Bool`, `Str`): `#Ceil` characterization, concrete guarded cast, symbolic inverse, and static-sort collapse. **Sound.** Matching sort guards are exact and mutually exclusive. `[total]` leaves off-sort values uninterpreted, but no target-dependent use occurs outside its matching guard. |
| 29–41, 92–109 | 10 | `isNumericV`, structural `allNumericVS`/`allStrVS`, `codesOf`, and the four-case `numericView`. **Sound.** Empty/cons equations are disjoint and descending; the view partitions the three numeric subsorts and their exact negation. |
| 113–129 | 11 | Exhaustive `numericGt` table. **Sound.** Nine numeric pairs exactly reuse fixed `>Int`, `boolAsInt`, `gtF`, `ltFI`, and `ltIF`; the two `nOther` cases agree on their only overlap and return false. |
| 22–25, 132–139 | 3 | Dynamic `applyCmp(">")` simplifications for guarded integer, numeric, and string values. **Sound derived bridges.** Their domains partition into the fixed static-sort equations; the numeric RHS matches all nine fixed sort-pair rules and the string RHS is exactly fixed `strLt(M,V)`. A bridge-free universal check is described below. |
| 143–151 | 3 | Sort-disjointness simplifications. **Sound in this K model.** `Int`, `Float`, and `Bool` are distinct `Val` injections; Python's Boolean numeric behavior is modeled by explicit promotion, not sort overlap. |
| 155–205 | 10 | Four structural fold summaries: two rules each for general numeric/string folds and three each for integer/float specialized folds. **Sound definitional summaries.** They descend on `ValSeq`; base, same-sort, and cross-sort handoff equations match the fixed fold transitions. They do not rewrite any `<k>` state. |
| 60–64 | 2 | `maxFOpaque` concrete/symbolic wrapper. **Acceptable but conditional trusted-primitive boundary.** Concrete and symbolic attributes separate the two orientations. It isolates only fixed K `FLOAT.max`, reads/writes no cell, and no theorem asserts an independent float value; float conclusions are interpretation-parametric in that primitive. |

This accounts for all 55 rules and all 16 local syntax declarations.
`verification.k` adds no priority rule and no rule matching `Call`,
`#loadAll`, `#maxAcc0`, a user-function body, return, exception, or frame
operation. The only opaque result-bearing local symbol is `maxFOpaque`; its
dependents and limitation are in the trust ledger.

The eight claims are also exhaustive:

- four accumulator circularities match only `#maxAcc`, `#maxAccF`, or
  `#maxAccV`, retain the arbitrary continuation suffix, and touch no state
  cell;
- four entry claims execute the exact function term and constrain the complete
  final state.

### Bridge-free comparison validation

To avoid accepting the candidate's comparison rules merely because they helped
close its proof, I made a scratch definition that removed only the three
`applyCmp(">")` simplifications. Against that definition I stated all nine
static numeric sort-pair equations and the string equation. They use only the
fixed supplied comparison dispatch plus the independently inspected
projection/view definitions. The definition compiled, all ten universal claims
closed with `#Top`, and `kore-exec` reported them as simplifier-trivial. Thus
every dynamic bridge match is contained in an independently fixed static-sort
case.

Evidence:

- [bridge-free definition source](evidence/bridgefree-verification.k)
- [bridge-free universal claims](evidence/bridgefree-spec.k)
- [exact bridge-removal diff and fresh build](evidence/05-bridgefree-kompile.log)
- [bridge-free ten-claim `#Top`](evidence/05-bridgefree-kprove.log)

No rule encodes the task's answer, introduces an unconstrained program-derived
oracle, bypasses the submitted body, or can enable a false result on the
intended modeled domain. I therefore make no unsound-rule allegation and no
false-conclusion witness is required.

## 6. Fresh non-vacuity test

Status: **PASS**.

I did not rely on candidate `spec-vacuity.k`. The fresh auditor mutation keeps
the exact submitted program term and a satisfiable input `[1, 3, 2]`, but
changes the result obligation from the true `3` to false `2`.

```text
kprove auditor-false.k --definition fresh-verification-kompiled \
  --spec-module AUDITOR-FALSE --dry-run
# exit 0

kprove auditor-false.k --definition fresh-verification-kompiled \
  --spec-module AUDITOR-FALSE
# exit 1, WarnStuckClaimState
```

The residual is the expected unmet obligation: `<k> 3 ~> .K </k>` cannot
unify with destination result `2`. Both trusted canonical and submitted Python
also return `3`. This is neither a parser error nor an unrelated crash.

Evidence:

- [fresh false mutation](evidence/auditor-false.k)
- [dry-run, proof command, statuses, and residual](evidence/06-fresh-mutation.log)

## 7. Proven versus assumed accounting

Status: **PASS with documented non-fatal trust/model limitations**.

### Precisely proven

Conditional on the supplied MPY semantics and K reachability engine, the
machine-checked result is:

> For every finite nonempty supplied-model list whose values are either any
> mixture of `Int`/`Bool`/`Float` or are all `Str`, executing the exact
> regenerated `max_element` binding and body from the stated initial
> configuration reaches the recursive fixed-fold summary, retains the first
> element on strict-comparison ties, and ends with the explicitly stated
> environment, scopes, counters, heap, stack, return, exception, and exit-code
> cells.

This is a partial-correctness statement. The proof does not separately certify
CPython, the translator, the K implementation, or a total-correctness
termination theorem.

### Trust ledger

| Boundary | Effect and dependents | Evidence and judgment |
|---|---|---|
| K 7.1.293 prover and supplied MPY semantics | Defines all execution, cells, builtins, and proof calculus; all claims depend on it. | Fixed benchmark input; rebuilt on both LLVM and Haskell. Accepted foundational boundary. |
| Trusted `py2mpy.py` | Connects Python source to the constructor program. | Regeneration is byte-identical; constructor term occurs exactly in every entry claim. Accepted source bridge. |
| K `INT`, `BOOL`, `STRING`, maps/lists, and sort predicates | Fix arithmetic, comparison, strings, containers, and generated sort membership. | Standard imported primitives plus relevant fixed-rule inspection. Accepted low-level boundary. |
| Fixed opaque float comparisons `gtF`, `ltFI`, `ltIF` | Select float/mixed-numeric branches. | The proof reuses exactly these named fixed primitives; LLVM tests cover homogeneous, mixed, infinity, and `2**53` cases. Universal CPython float equivalence is assumed, not proved. Non-fatal concern. |
| Local `maxFOpaque = FLOAT.max` wrapper | Can affect float result and later comparisons; float and mixed claims depend on it. | Interpretation-parametric wrapper around a fixed primitive, not a program-derived oracle; concrete LLVM uses the real hook. Accepted conditional boundary, reported as a concern rather than hidden. |
| Bare read-only `list(ValSeq)` claim input | Avoids heap allocation for externally supplied read-only arguments. | Explicitly permitted by fixed `core.k`; the function only reads it. Allocated-list concrete smoke follows the ref-deref path and agrees. Accepted representation bridge. |
| Nested-list/tuple ordering gap in supplied model | Excludes normally returning CPython values outside fixed `max` behavior. | Concrete witness: Python returns `[2]`; unmodified MPY stops at `#maxCont0`. Candidate documents the boundary and is Python-faithful. Campaign-v2 `CONCERNS / LEGIT` exception. |
| Non-ASCII literal encoding gap | Prevents concrete MPY construction of some CPython strings. | Unicode Python witness returns `"😀"`; supplied concrete input fails. Symbolic `Str` theorem remains unbounded over `IntSeq`. Campaign-v2 model-gap concern. |
| Differential evidence | Supports source fidelity and primitive/model bridges only. | 221 recorded cases, zero material mismatches; finite evidence is not substituted for the K proof. Properly limited. |
| Partial-correctness interpretation | Does not independently prove termination or behavior on excluded exceptional inputs. | Explicit theorem limitation. Acceptable for the requested proof class. |

### Gate summary and verdict rationale

- Gate A (real-program soundness): **PASS**. Exact body executes; bridges are
  independently checked; state/control are preserved; satisfying witnesses,
  false-result rejection, and body sensitivity all hold.
- Gate B (intent adequacy): **PASS inside every normally returning behavior
  represented by the fixed model**. The broader CPython source contract has
  fixed-model behavior/encoding gaps, explicitly witnessed above.
- Gate C (trust and evidence): **PASS**. Commands, scopes, oracles, statuses,
  and limitations are reproducible and separated from formal conclusions.

Without campaign amendment v2, the supplied-model gap would be a
sound-but-limited scope issue. All four amendment conditions hold: the gap is
in the read-only supplied model, not candidate theory; the theorem covers the
entire fixed successful domain; this ledger gives concrete divergence
witnesses; and submitted Python is canonical-faithful on those witnesses.
Accordingly the benchmark mapping is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
