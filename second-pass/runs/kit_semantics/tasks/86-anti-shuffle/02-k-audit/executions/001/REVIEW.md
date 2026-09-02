# Independent adversarial review: 86-anti-shuffle

The candidate contains a legitimate, freshly reconstructible K
partial-correctness proof of the submitted translated program. The formal result
is non-vacuous, unbounded over finite `IntSeq` inputs, and is not obtained through
an execution-skipping bridge or an opaque result oracle.

I assign `CONCERNS / LEGIT`, rather than `PASS`, for one non-fatal validation
limitation: the K theorem proves equality to the fully defined recursive
functional summary `antiGo`, while the universal theorem that this summary is
equivalent to “split on literal spaces, sort every word, and rejoin preserving
all spaces” is given only by an informal induction. A broad independent
differential test supports that intent bridge on 42,371 strings, but finite
testing is not a universal proof. This limitation does not narrow the input
domain or allow a false K result.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `86-anti-shuffle`, and condition
`kit-semantics`. The mounted trusted semantics is present, as required for this
mode. There is no rendered-mode contradiction and no audit infrastructure
breach.

I independently checked the launcher records with
[`provenance_check.py`](/audit-output/evidence/provenance_check.py). The exact
results are in
[`01-provenance.log`](/audit-output/evidence/01-provenance.log):

- `/audit-campaign-lock.json` is a regular file, has the recorded SHA-256
  `ad5dfc...d745`, and its JSON object equals the `audit_campaign` block in
  `/audit-input.json`.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
  and `prompt.txt` are all present as regular files. Every byte hash equals the
  corresponding pipeline-v3 hash in `/audit-input.json`.
- The structured trace consists of one regular JSONL file. All 972 records
  parse as JSON. Its file hash is
  `24b97a...52d8`, matching `invocation.json`; its pipeline tree hash is
  `c05fe5...aa4`, matching `usage.json`.
- The current `/candidate` pipeline tree hash is
  `2b2b69...b7a`, matching both `invocation.json` and
  `/generation-result.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts. The trusted canonical hash is the recorded
  `ddca6b...162`.
- The candidate and trusted `reference-semantics/` manifests contain exactly
  the same 25 directory/file entries, modes, and file hashes. Neither tree
  contains a symlink or unsupported file type. Their pipeline tree hash is
  `4e0639...9f`, matching `/task.json` and the trusted manifest hash recorded in
  `/audit-input.json`. A direct recursive `diff` also exited 0.

I inspected the generation records, trace, and 3.5 MB output log only as
untrusted history. They claim successful proofs and tests, but no conclusion
below depends on those claims or on the candidate-provided compiled
definitions, caches, `vacuity.log`, or `PROOF.md`.

All required candidate source artifacts are present: `solution.py`,
`solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`. The
candidate also supplies the generated program module and auxiliary lemma spec.
There are no missing, additional, changed, mistyped, or linked entries in the
supplied-semantics copy.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a string, treat literal U+0020 space as
the word separator; replace every word by its characters in ascending
character/ASCII order; preserve word order and every blank space. The trusted
canonical implements this as `s.split(' ')`, `sorted` on each resulting word,
and `' '.join(...)`. Consequently, leading, trailing, and repeated spaces are
preserved; tabs and newlines are sortable word characters, not separators.

The candidate `solution.py` is an insertion-sort implementation. It scans the
input, keeps the current word sorted by inserting each non-space character
before the first greater character, flushes that word at each literal space,
and appends the last word at the end. It accepts the full intended `str` input
domain; there is no length, character, or word-count restriction.

Using the trusted translator in a clean scratch tree, I ran:

```text
python3 py2mpy.py solution.py > auditor-regenerated.mpy
cmp -s auditor-regenerated.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`1d7065...db5`. Regenerating `program-generated.k` also produced byte identity
with the submitted file, SHA-256 `a1281b...156`. Exact commands and hashes are
in [`02-fidelity.log`](/audit-output/evidence/02-fidelity.log).

The independent differential test is
[`differential_test.py`](/audit-output/evidence/differential_test.py). It loads
the trusted and submitted entry points from explicit paths. Its deterministic
corpus includes:

- all three documented examples;
- empty, one-character, leading/trailing/repeated-space, and all-space inputs;
- insertion comparison boundaries `<`, `==`, and `>`;
- NUL, tab, newline, ASCII boundary characters, Unicode, and the maximum
  Unicode code point;
- every string of length 0 through 5 over `" aA!0~\t\n"`; and
- 5,000 seeded generated strings of length 0 through 100.

The run exited 0 with `cases=42371`, corpus hash
`7c346e...e3df`, and `mismatches=0`. The script separately checks both equality
to the trusted canonical and the split/sort/join contract. This is strong finite
evidence, not a substitute for the K proof or a universal intent theorem.

## 3. Clean proof reconstruction

I copied only source artifacts and the trusted supplied-semantics sources to
`/tmp/audit-work/anti-shuffle`. I did not copy or refer to any candidate
`*-kompiled` directory. The available independent K tools report version
7.1.293; see
[`03-tool-versions.log`](/audit-output/evidence/03-tool-versions.log).

### Concrete definition

The auditor-authored boundary program is preserved as
[`03-auditor-concrete.py`](/audit-output/evidence/03-auditor-concrete.py). It
contains the exact submitted body plus assertions for the prompt examples,
empty input, one and multiple spaces, leading/trailing spaces, all three
insertion comparison outcomes, and a tab-containing word.

Fresh commands:

```text
python3 py2mpy.py auditor-concrete.py > auditor-concrete.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
krun auditor-concrete.mpy --definition runtime-audit-kompiled
```

All exited 0. The final concrete configuration has `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. See
[`03-llvm-build.log`](/audit-output/evidence/03-llvm-build.log) and
[`03-concrete-krun.log`](/audit-output/evidence/03-concrete-krun.log).

### Bridge-free lemma definition

I freshly compiled the unextended supplied semantics:

```text
kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition lemma-audit-kompiled
kprove lemma-spec.k --definition lemma-audit-kompiled \
  --spec-module LEMMA-SPEC
```

Both exited 0; the proof printed `#Top`. This one invocation contains and closes
all three less/greater/equal singleton-string claims. The `WarnTrivialClaim`
messages mean the fixed semantics and guards already simplify the claims; the
proof-local singleton simplifier was not imported into this definition. See
[`03-lemma-build.log`](/audit-output/evidence/03-lemma-build.log) and
[`03-lemma-prove-all.log`](/audit-output/evidence/03-lemma-prove-all.log).

### Target definition

I then built the proof definition and ran the candidate's complete positive
claim bundle:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Both exited 0 and the proof printed `#Top`. The spec module contains exactly
the inner-loop, outer-loop, and whole-program claims, so the single unfiltered
invocation proves every declared target together, with the loop claims
available as circularities. Evidence:
[`03-verification-build.log`](/audit-output/evidence/03-verification-build.log)
and
[`03-target-prove-all.log`](/audit-output/evidence/03-target-prove-all.log).

The compiler warnings are unused-variable warnings in the claims and
non-exhaustiveness warnings for unrelated supplied-library functions. They are
not proof failures and none of the warned library functions occurs on this
program's execution path.

## 4. Adequacy and real-program pinning

### Claims in plain language

`anti-shuffle-inner-loop` has no explicit `requires`. Its typed starting state
is inside the exact `anti_shuffle` function frame with no return or exception
pending. It starts at the already-evaluated inner string-loop head over
remaining characters `IS`; the inserted character is the singleton `C`, the
partial result is `A`, and `B` says whether insertion already happened. It
executes the real inner body and following post-insertion statements, preserves
the arbitrary continuation and stack, and leaves `word` and `new_word` equal
to `insertGo(IS,C,A,B)` with `inserted=true`. The final `old_char` is
existential because it is scratch state.

`anti-shuffle-outer-loop` also has no explicit `requires`. It starts in the
exact call frame at the outer loop head, with remaining input `S`, completed
output `R`, current word `W`, and arbitrary scratch locals. It executes the
real outer body, the function tail, return, and `#endcall`, pops the exact call
frame, and returns `str(antiGo(S,R,W))`. The theorem is valid for arbitrary
`R` and `W`; the reachable entry instance starts both empty.

`anti-shuffle` starts in the pristine supplied configuration with any finite
`INPUT:IntSeq`. It loads `solutionModule()`, resolves the public function name
through the module scope, evaluates the argument, executes the function body,
and returns `str(antiGo(INPUT,.IntSeq,.IntSeq))`. The module closure remains in
scope and every heap, stack, return, exception, and exit cell is constrained.

All three preconditions are satisfiable. For example:

- inner: `IS=A=R=ORIGINAL=WORD=OLD=.IntSeq`, `C=98`, `B=false`, and
  `STACK=.List` in the displayed exact scopes;
- outer: `S=[98,97,32,97]` (`"ba a"`), `R=W=.IntSeq`, empty scratch strings,
  `INSERTED=false`, and the displayed single call frame; and
- entry: `INPUT=[98,97,32,97]` in the displayed initial configuration.

The whole-program ground claims preserved in
[`04-auditor-ground-spec.k`](/audit-output/evidence/04-auditor-ground-spec.k)
execute the actual load/call path for `""`, `"ba a"`, and `"aa"`. They prove
the literal results `""`, `"ab a"`, and `"aa"` from the freshly built
definition; `kprove` exited 0 with `#Top`. Both trusted and submitted Python
implementations print the same three results. See
[`04-ground-pinning.log`](/audit-output/evidence/04-ground-pinning.log) and
[`04-ground-python.log`](/audit-output/evidence/04-ground-python.log).

### Constructor-level identity and body sensitivity

The entry claim does not call a summary oracle. `solutionModule()` expands to
the complete translated `Module(FuncDef(...))`; the normal supplied loader,
lookup, call, binding, loop, assignment, comparison, return, and frame-pop
rules execute it. The regenerated `solution.mpy` and generated module are
byte-identical to the submitted artifacts. The four nullary helper aliases
are the actual inner-loop body, its following statements, the outer-loop body,
and the function tail visible in that same constructor tree. Their occurrence
at the circularity heads must unify with the executing body; they do not
replace execution.

I independently changed the final source operation from
`result += word` to `result += 'X'`, regenerated both the `.mpy` and generated
K program term, and rebuilt the proof definition. The mutation is preserved in
[`04-body-mutation.patch`](/audit-output/evidence/04-body-mutation.patch).
Compilation exited 0, but the target proof exited 1 with
`WarnStuckClaimState`. For the satisfiable empty-input branch, the residual
actual value is `str(iCons(88,.IntSeq))` and the displayed loaded closure body
contains `Str("X")`. Thus the program term actually executed by the theorem
changed and the original result obligation rejected it. See
[`04-body-mutation-build.log`](/audit-output/evidence/04-body-mutation-build.log)
and
[`04-body-mutation-prove.log`](/audit-output/evidence/04-body-mutation-prove.log).

## 5. Rule-by-rule static soundness review

The exhaustive line-addressed inventory is
[`05-rule-inventory.md`](/audit-output/evidence/05-rule-inventory.md), generated
by
[`inventory_rules.py`](/audit-output/evidence/inventory_rules.py). It contains
950 entries: 232 syntax declarations, 706 rules, five contexts, one
configuration, and six claims. Per-file counts and the full flattened text of
every multiline declaration/rule are included.

The supplied tree accounts for the configuration, all five contexts, 695
rules, and 227 syntax declarations. Under `SUPPLIED_SEMANTICS`, this
hash-locked tree is the fixed operational theory. I nevertheless traced every
constructor used by `solution.mpy` through its material rules:

| Used construct | Declaration and operational path |
|---|---|
| `Module`, statement lists | `syntax.k`; `core.k` `#loadAll`, list sequencing, `.Stmts` |
| `FuncDef`, `Params`, `Call` | `functions.k` closure creation; `call.k` callee then left-to-right argument evaluation, fresh scope/frame, parameter binding |
| `Name`, `Assign` | `core.k` lexical lookup; `controls.k` strict RHS then current-scope write |
| `Str`, string iteration | `str.k` ASCII literal conversion for the only literals `""` and `" "`; `#iterNext` yields singleton strings |
| `For` | `controls.k` evaluates the iterable once, uses `#loop`, binds each target, runs the body, and resumes through `#loopLbl` |
| `If` | strict guard evaluation, `truthy`, and disjoint true/false `#branch` rules |
| `UnaryOp("not")`, `BoolOp("and")` | operator dispatch plus `bool.k` truthiness and left-to-right short circuit |
| string `==` and `<` | compare contexts, string dispatch, code-sequence equality, and lexicographic `strLt` |
| string `+`, `AugAssign` | `seqConcat` and the current-scope update rule |
| `Return` | strict return value, `retV`, exact frame pop, restored environment/scope |

This path preserves evaluation order and all material cells. Strings are
values, so this program allocates no heap object. A call allocates a scope and
stack frame and the fixed return rules remove exactly that frame. Guards for
string iteration, boolean short circuit, space equality, and character order
are disjoint and exhaustive on the typed states reached here. The only
language-model limitation on this path is that source string literals are
ASCII-only; the program's literals are ASCII, while the symbolic input is
injected directly as an arbitrary `IntSeq`, so this does not restrict the
theorem's input domain.

All other supplied declarations and rules are pattern-disjoint from this
program and never appear in a residual or postcondition. This includes lists,
tuples, dictionaries, sets, comprehensions, ranges, slicing, methods, sorting,
floats, arithmetic builtins, hashing, and the LLVM-only concrete keyed-sort
module. The supplied opaque/no-evaluator symbols are:

`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`,
and `md5hexCodes`.

The concrete-only `floorFI`, `toF`, and `ceilF` are likewise opaque on some
symbolic values. None can influence this program's control, state, result, or
claims. LLVM warned that several unrelated `[total]` functions are not
syntactically exhaustive (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`). That is a limitation of the fixed supplied library, but no
matching term is reachable here and no false conclusion about the intended
string input can be witnessed from them. I therefore record an irrelevant
fixed-theory evidence boundary, not a candidate proof unsoundness.

The proof-local inventory is small enough to decide individually:

- `solutionModule()` and `solutionBody()` are nullary, total definitional
  aliases with one equation each. Regeneration established their exact source
  constructor identity.
- `antiInnerBody()`, `antiPostInsert()`, `antiOuterBody()`, and `antiTail()`
  are nullary syntax aliases with one exhaustive equation each. They name exact
  subterms and do not rewrite a running `<k>` computation into a result.
- `insertGo` has disjoint empty/cons equations. The cons equation structurally
  decreases its first argument; its Boolean/order conditional is total.
  It copies each remaining old character and inserts `C` once iff `B` was
  false.
- `antiGo` has disjoint empty/cons equations, structurally decreases its first
  argument, and splits the cons case on the total equality `C ==Int 32`. It
  appends the current word and one space on the separator branch, otherwise
  invokes the fully defined insertion summary.
- The singleton simplification
  `strLt(iCons(C,.IntSeq),iCons(D,.IntSeq)) => C <Int D` overlaps the fixed
  lexicographic equations only compatibly: the `<`, `>`, and `==` integer cases
  respectively yield `true`, `false`, and `strLt(.IntSeq,.IntSeq)=false`.
  The three bridge-free lemma claims cover exactly this trichotomy under the
  unextended supplied definition.
- The three reachability claims are auxiliary/entry theorems, not operational
  rewrites installed in `verification.k`. The inner theorem preserves an
  arbitrary continuation and stack and contains no abrupt effect. The outer
  theorem accepts only the exact tail, `#endcall`, and call frame it proves; it
  does not generalize an exact-return theorem to an arbitrary continuation.

There are no proof-local priority rules, `functional` declarations, opaque
symbols, host calls, unconstrained fresh result values, operational bridges,
or rules encoding the task answer in place of execution. No inventoried
proof-local rule has a false conclusion witness on the intended domain.

The remaining adequacy question is not rule soundness: `antiGo` is a truthful,
fully defined execution summary, but the K files do not contain a separate
universal theorem that its output satisfies an independently stated
sorted-word predicate or equals a formalization of the trusted canonical.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation is
[`06-auditor-vacuity.k`](/audit-output/evidence/06-auditor-vacuity.k). It keeps
the complete entry configuration but changes the RHS to prefix code 90 to the
actual symbolic result:

```text
str(iCons(90, antiGo(INPUT, .IntSeq, .IntSeq)))
```

This is demonstrably false for the satisfying empty input: the submitted
program and canonical both return `.IntSeq`, not `[90]`.

First, the dry run:

```text
kprove auditor-vacuity.k --definition verification-audit-kompiled \
  --spec-module AUDITOR-VACUITY --dry-run
```

exited 0 and emitted a valid `kore-exec --prove` command, establishing that the
mutated spec parses and builds. Then the same command without `--dry-run`
exited 1 with `WarnStuckClaimState`, not a parser error, crash, or timeout. The
reachable residual contains `<k> str(.IntSeq) ~> .K </k>` and the condition
`INPUT #Equals .IntSeq`; it cannot unify with the prefixed destination. Exact
bounded logs are
[`06-vacuity-dry-run.log`](/audit-output/evidence/06-vacuity-dry-run.log) and
[`06-vacuity-prove.log`](/audit-output/evidence/06-vacuity-prove.log).

This establishes that the positive entry theorem constrains the returned
value and rejects a meaningful false alternative.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied semantics and proof-local equations, for every finite
`INPUT:IntSeq`, if the translated submitted program executes from the shown
initial configuration to termination, its value is exactly:

```text
str(antiGo(INPUT, .IntSeq, .IntSeq))
```

The proof also establishes the exact inner insertion-loop and outer-loop
summaries used to reach that result, including scope, stack, return, exception,
heap, and exit-cell behavior. This is an unbounded symbolic theorem, not a
finite-size proof. It covers the intended Python-string domain and in fact the
larger K domain of arbitrary integer code sequences. It is a partial-
correctness theorem; total correctness, resource bounds, and full CPython
equivalence are not claimed.

### Trusted or external boundaries

- **K 7.1.293 compiler, Haskell prover, LLVM runtime, and builtin theories.**
  These are the machine-checking base. Every reconstructed result is
  conditional on their correctness.
- **Hash-locked supplied MPY semantics.** This is the benchmark-selected
  operational model. The proof uses its real loader, lookup, calls, scopes,
  loops, strings, comparisons, assignments, returns, and configuration cells.
  Equivalence of this partial semantics to all of CPython is outside the
  theorem.
- **Trusted `py2mpy.py`.** Source-to-constructor translation is outside the K
  reachability theorem, but trusted regeneration produced byte identity.
- **Unused opaque library symbols.** The complete list is given in stage 5.
  They are present in the fixed imported theory but have no dependent claim or
  reachable occurrence in this program, so their interpretations cannot
  affect the result.
- **Trusted canonical Python entry point.** It is an independently executable
  oracle for finite differential evidence, not an axiom used by `kprove`.

### Empirical and informal bridges

- The 42,371-case differential run supports equality of the submitted Python
  implementation to the trusted canonical on examples, branch boundaries,
  exhaustive small strings, long random strings, and Unicode boundaries.
- The transparent mathematical argument for the source contract is:
  `insertGo(W,C,.IntSeq,false)` inserts `C` exactly once before the first
  greater character of an already sorted `W` (or appends it), preserving
  sortedness and multiplicity. Induction over each word therefore keeps `W`
  sorted; induction over `antiGo` flushes that word and exactly one literal
  space at every code 32 while preserving word order. This proves the intended
  meaning on paper, but that sortedness/permutation invariant is not separately
  machine-checked in the submitted K artifacts.

Gate A passes: execution is real, program-pinned, sound under the fixed theory,
and non-vacuous. Material domain alignment passes: the theorem is symbolic and
unbounded and does not strengthen the HumanEval precondition. Evidence
auditability also passes. The missing machine-checked universal
summary-to-contract theorem is a non-fatal informal intent bridge, which maps
to `CONCERNS / LEGIT` under the benchmark decision boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
