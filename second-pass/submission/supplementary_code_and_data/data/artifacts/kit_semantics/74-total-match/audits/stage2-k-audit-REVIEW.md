# Independent adversarial audit: 74-total-match

## Executive finding

The candidate contains a legitimate, non-vacuous partial-correctness proof for
the real generated program. I rebuilt both K definitions from trusted source,
proved the loop claim and both result branches, mechanically matched each entry
claim's executed module to the trusted regeneration of `solution.mpy`, reviewed
all proof-local rules, inventoried the complete imported rule set, and made two
independent false mutations fail for the expected semantic reason. The proof is
unbounded over finite lists of strings; it is not a collection of fixed examples
or bounded unrollings.

The detailed command/evidence index is
[`evidence/INDEX.md`](evidence/INDEX.md).

## 1. Input and provenance integrity

I first read `/audit-input.json`. It declares `record_layout: pipeline-v3`,
problem `74-total-match`, generation condition `kit-semantics`, and
`semantics_mode: SUPPLIED_SEMANTICS`. Its `container_paths` resolve the mounted
candidate, trusted Python inputs, supplied semantics, and generation records.
The required `/reference/reference-semantics` tree is present, so the trusted
mount does not contradict the rendered mode.

I independently read all pipeline-v3 records required by the prompt:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt` under
  `/generation-evidence`;
- the one 399-record JSONL rollout under
  `/generation-evidence/codex-trace/`.

The generation prose, logs, reported `#Top`, and structured events were treated
only as historical claims. No candidate result below relies on them.

The independent integrity checker and its complete output are
[`integrity_check.py`](evidence/integrity_check.py) and
[`01-integrity.log`](evidence/01-integrity.log). In particular:

- `/audit-campaign-lock.json` is a field-for-field match for the 14-field
  campaign block in `/audit-input.json`, and its SHA-256 is
  `ad5df41e52a1cc0560902304cac87558274139f22f4b7bcf705c021583f581e5`,
  exactly the recorded campaign-lock hash.
- Every directly recorded file hash matches the mounted file. This includes
  `run.json` (`3b99...`), `task.json` (`eeb5...`),
  `generation-result.json` (`8d16...`), all seven named generation-evidence
  records, the generation prompt (`c5f7...`), and the trace member
  (`80d352...`). Full hashes are preserved in the log.
- The pipeline tree hash recomputed from `/candidate` is
  `92e759a77b03b4e2e1d6ca3f70ba1a2df6e7d56a7f6271afe1a678196e83c3aa`,
  exactly the stage output hash recorded by both `generation-result.json` and
  `invocation.json`.
- The recomputed structured-trace tree hash is
  `416374171b0f507cc222615bb5a2187d4748e091551984278df806d884c60a72`,
  exactly the hash in `usage.json`.
- The trusted and candidate prompt files are byte-identical, as are the trusted
  and candidate translator files.
- The trusted and candidate reference-semantics trees each contain the same 24
  regular K files, contain no symlinks, have no missing or additional entries,
  are recursively byte-identical under `diff -qr --no-dereference`, and both
  have pipeline tree hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
  This is also the trusted-semantics hash in the generation manifest.

The launcher also records composite candidate, semantics, and trace hashes whose
serialization algorithm is not encoded in the audit record. I recorded those
values without pretending that a different tree-hash algorithm is comparable;
the executable integrity anchors above were recomputed using the pipeline's
declared tree algorithm and, for semantics, a direct recursive comparison.

All required provenance records are regular, readable files; all required
candidate proof artifacts are present; and no candidate entry is a symlink.
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: given two lists of strings, return the list
whose strings contain fewer total characters; when the two totals are equal,
return the first list. The trusted canonical implementation computes
`sum(len(s) for s in list)` on each input and selects the first exactly when its
total is `<=` the second.

The generated `solution.py` implements the same contract with a helper that
initializes an integer accumulator, iterates over every string, adds its length,
and returns the accumulator. `total_match` calls that helper twice and uses the
same `<=` tie rule. It neither mutates nor copies either input and returns one of
the original list objects.

I ran the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py`. The regenerated file is byte-identical to the submitted
`solution.mpy`; the exact command, `cmp`, hashes, and exit 0 are in
[`02-translation.log`](evidence/02-translation.log). Python syntax compilation
also exited 0 in [`04-python-syntax.log`](evidence/04-python-syntax.log).

The independent differential harness
[`differential_test.py`](evidence/differential_test.py) loads the trusted
canonical and generated functions as separate modules, checks both value and
selected-object identity, and covers:

- all 5 documented examples;
- 10 hand-selected boundary cases, including empty inputs, equality, both
  strict branches, Unicode, NUL, and a long string;
- 24,336 exhaustive small pairs; and
- 2,000 deterministic generated pairs.

All 26,351 cases agreed. The run exercised 16,048 first-list selections, 10,303
second-list selections, and 5,808 equal-total cases. The inputs and exact result
are in [`03-differential.log`](evidence/03-differential.log). This testing
supports source fidelity but is not used as a substitute for the symbolic K
proof.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/74-total-match`, copied the
reference semantics from the trusted mount, and did not copy or use any
candidate-built definition, cache, or backend output. The installed K version
was `7.1.293`.

The fresh reconstruction results were:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| Submitted module execution | `krun solution.mpy --definition audit-runtime-kompiled` | exit 0; final `.K`, `NoExc`, exit code 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| Loop claim | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.sum-loop` | `#Top`, exit 0 |
| First entry and loop dependency | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.sum-loop,SPEC.entry-first` | `#Top`, exit 0 |
| Second entry and loop dependency | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.sum-loop,SPEC.entry-second` | `#Top`, exit 0 |
| Complete specification | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | `#Top`, exit 0 |

The corresponding bounded logs are
[`05-kompile-llvm.log`](evidence/05-kompile-llvm.log),
[`06-krun-module.log`](evidence/06-krun-module.log),
[`07-kompile-haskell.log`](evidence/07-kompile-haskell.log),
[`08-kprove-sum-loop.log`](evidence/08-kprove-sum-loop.log),
[`09b-kprove-entry-first-with-loop.log`](evidence/09b-kprove-entry-first-with-loop.log),
[`10b-kprove-entry-second-with-loop.log`](evidence/10b-kprove-entry-second-with-loop.log),
and [`11-kprove-all.log`](evidence/11-kprove-all.log). The compiler warnings are
limited to unused variables and nonexhaustive, unused helper functions in the
fixed semantics; they do not change the successful build or proof results.

Two exploratory logs named `09-kprove-entry-first.log` and
`10-kprove-entry-second.log` selected an entry while omitting its necessary
loop circularity and were abandoned. They are not treated as proof runs. The
dependency-complete `09b` and `10b` runs and the unfiltered `11` run are the
authoritative positive-target runs.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiability

`sum-loop` says: in a positive-numbered function scope whose module has no
shadowing `len`, executing the actual `for string in strings:
total += len(string)` loop over a finite string-valued sequence consumes the
loop, changes `total` from `ACC` to `totalLenFrom(ACC, ITEMS)`, and leaves
`string` equal to the old value for an empty iteration or the last iterated
string otherwise. It preserves the continuation and all other cells. A
satisfying state exists, for example `L = 1`, `ITEMS = .ValSeq`, any integer
`ACC`, any `OLD`, and a module map with no `len`.

`entry-first` says: from the exact initial MPY configuration, for arbitrary
finite `A` and `B` containing only strings, when `totalLen(A) <= totalLen(B)`,
loading the exact submitted module and calling `total_match(list(A), list(B))`
returns exactly `list(A)`. It also fixes the final two module closures and
requires empty heap and stack, `noRet`, `NoExc`, and exit code 0. A witness is
`A = ["a"]`, `B = ["b"]` (or two empty lists).

`entry-second` has the same exact execution and final-state conditions under
`totalLen(A) > totalLen(B)`, and returns exactly `list(B)`. A witness is
`A = ["a"]`, `B = [""]`.

The integer guards are disjoint and exhaustive. `ValSeq` is the semantics'
finite sequence datatype, and the recursive `onlyStrings` predicate imposes no
length bound. The result is an exact constructor term, not a free variable,
tautology, implication-only postcondition, or unconstrained oracle.

### Program pinning

Both entry claims execute `#loadAll(Module(...)) ~> Call(...)`; they do not
summarize or bypass the generated function bodies. The auditor-authored
[`constructor_compare.py`](evidence/constructor_compare.py) extracted each
claim's `Module` term, applied only the demonstrated inert spelling
normalization between an omitted empty statement list and `.Stmts`, then used
`kast --expand-macros --sort Module -o json`. The regenerated
`solution.mpy`, `entry-first`, and `entry-second` all produced the same
constructor JSON and canonical hash
`ad0544944e102977908974656204815fc469dc9963873ce29678cc8de74ce82a`.
The exact comparison is in
[`14-constructor-compare.log`](evidence/14-constructor-compare.log).

Concrete satisfying substitutions were also executed independently. The
auditor's [`k_ground_witness.py`](evidence/k_ground_witness.py) asserts the
equal-total, first-strict, and second-strict Python cases; its trusted
translation and K execution both exit 0, with `.K`, `NoExc`, and exit code 0,
in [`12-translate-ground-witness.log`](evidence/12-translate-ground-witness.log)
and [`13-krun-ground-witness.log`](evidence/13-krun-ground-witness.log). These
agree with both Python implementations and with the symbolic claim
substitutions.

Finally, I checked actual-body sensitivity. The checked mutation changes the
comparison constructor in the executed module from `<=` to `>` while retaining
the original expected first result for equal one-character inputs. It parses
and builds, but `kprove` exits 1 with a stuck state whose actual result is
`["b"]` and required result is `["a"]`. See
[`18-body-mutation-inspection.log`](evidence/18-body-mutation-inspection.log),
[`19-body-mutation-dry-run.log`](evidence/19-body-mutation-dry-run.log), and
[`20-body-mutation-proof.log`](evidence/20-body-mutation-proof.log). This
changes the term that the claim executes, not merely an external source file.

## 5. Rule-by-rule static soundness review

The exhaustive machine-readable-to-human inventory is
[`rule-inventory.md`](evidence/rule-inventory.md), produced by
[`rule_inventory.py`](evidence/rule_inventory.py). It covers all 24 supplied
semantics files plus `verification.k` and `spec.k`, with file, line, normalized
text, attributes, material-path classification, and review disposition for
every item. Its totals are 945 items: 231 syntax declarations, 705 rules, 5
contexts, 1 configuration, and 3 claims. It separately identifies 150
`function` declarations, 111 `total` declarations, 22 `no-evaluators` opaque
declarations, 45 priority rules, 27 `owise` rules, 35 `concrete` rules, and the
single simplification rule. No `functional` declaration is present. The
inventory run exited 0 in
[`15-rule-inventory.log`](evidence/15-rule-inventory.log).

### Proof-local declarations and rules

`verification.k` adds exactly five named mathematical functions and nine
equations, plus one simplification rule:

1. `onlyStrings(.ValSeq) => true` and the `vCons` equation use the supplied
   `isStrV` recognizer recursively. They exactly characterize finite
   string-valued argument sequences.
2. `stringCodes(str(CS)) => CS` and its `owise` equation make the projection
   total. The fallback can be reached as a standalone function but is
   unreachable in all uses that affect the claims because those uses are
   guarded by `isStrV`/`onlyStrings`.
3. The sole simplification,
   `seqLen(V) => isLen(stringCodes(V)) requires isStrV(V)`, agrees with the
   supplied concrete string-length equation: `isStrV` is true exactly for
   `str(CS)`, for which `stringCodes` is `CS`. Its overlap therefore has the
   same result, rather than strengthening or inventing a length.
4. `totalLen` and `totalLenFrom` are ordinary structural left folds over
   `ValSeq`, starting at zero and adding the supplied integer length of each
   string code sequence. Their empty/cons equations are disjoint, decreasing,
   exhaustive, and match the actual accumulator update.
5. `lastLoopValue` structurally returns `OLD` for no iteration and otherwise
   recurses with the current head as the remembered value. This exactly models
   the final Python loop target.

There are no proof-local opaque symbols, `no-evaluators` declarations,
priorities, `concrete` rules, external hooks, or ordinary rules that rewrite
the program's `<k>` execution. In particular, no rule recognizes
`total_match`, returns the task answer, allocates an unconstrained result, or
bypasses a call. `sum-loop` is a reachability circularity with exact
configuration context, not a global semantic rewrite. Because the extension
contains no operational bridge rule, the Kit operational-bridge theorem
obligation is not applicable.

### Supplied semantics and material path

I mapped every constructor used by `solution.mpy` to the inventoried supplied
declarations and rules. The material path consists of:

- `Module`, `FuncDef`, `Params`, `Assign`, `For`, `AugAssign`, `Return`, `If`,
  `Compare`, `CmpOp`, `Call`, `Name`, `Int`, `NoneVal`, and statement
  sequencing;
- the configuration cells, `#loadAll`, module/builtin scope lookup, lexical
  parent lookup, function definition and closure creation;
- left-to-right call and argument evaluation, parameter binding, frame
  push/pop, return propagation, and exception/exit side conditions;
- list iteration, tuple/list target binding, name assignment, integer `+`,
  integer `<=`, conditional truth, and the `len` builtin;
- `seqLen(str(CS)) => isLen(CS)` and the structural `IntSeq` length.

The fixed rules evaluate the called function first and its arguments in order;
the helper frame's parent is module scope 0; `len` falls through that scope to
the builtins scope; its string argument is mapped to `seqLen` and then
`isLen`; the `for` consumes each finite list head in sequence; the
`AugAssign` performs integer addition; `Return` unwinds the exact active frame;
and the selected input list is returned without heap allocation. This explains
the claimed final module closures, scope location 1, empty heap/stack, and
absence of exception.

All overlaps and relevant priorities on this path are recorded in the
inventory. The selected call, loop, return, comparison, arithmetic, lookup, and
builtin rules are either constructor-disjoint or guard-disjoint at the states
used here; their priorities enforce the intended control/evaluation order.
None supplies a result that is not computed from `A` and `B`.

The 22 supplied opaque/no-evaluator declarations belong to fixed float, sort,
and MD5 support. Constructor and guard reachability analysis shows that none is
reachable from this program or any claim. The remaining fixed-semantics items
are likewise marked inactive only after checking their outer constructor,
function head, or guard. This audit does not assert that every unused feature
is a full Python model; it establishes that the exact used subset is closed and
sound for the submitted program. Because the candidate semantics tree is
byte-identical to the required supplied baseline, there are no candidate
semantic substitutions to bless.

I found no unsound proof-local or used semantic rule, so there is no
false-conclusion witness to report. The narrower boundary is the ordinary
trusted-semantics/modeling boundary accounted for in stage 7, not an unsound
rule.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. I authored
[`audit-vacuity.k`](evidence/audit-vacuity.k) in scratch. It executes the exact
module on the satisfying equal-total input `A = ["a"]`, `B = ["b"]` but changes
the result-constraining postcondition from the required first list to the second
list.

`kprove --dry-run` successfully parsed and constructed the backend command
([`16-vacuity-dry-run.log`](evidence/16-vacuity-dry-run.log)). The real proof
then reached a semantic stuck claim: the actual value was the code sequence for
`"a"` while the postcondition required the code sequence for `"b"`. It emitted
`WarnStuckClaimState` and exited 1
([`17-vacuity-proof.log`](evidence/17-vacuity-proof.log)). Thus the failure is
the expected unmet result obligation, not a parse error, missing import,
timeout, unrelated crash, or unreachable mutation.

Together with the independent executed-body mutation in stage 4, this
establishes both postcondition sensitivity and program-body sensitivity.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every pair of finite `ValSeq` values `A`
and `B` satisfying `onlyStrings`:

- if the sum of their represented string lengths satisfies
  `totalLen(A) <= totalLen(B)`, execution of the exact regenerated/submitted
  module call reaches `list(A)`;
- if `totalLen(A) > totalLen(B)`, that execution reaches `list(B)`;
- normal execution leaves exactly the two expected module closures, no active
  call stack or heap entries, no pending return, no exception, and exit code
  zero.

The loop claim proves the accumulator summary for an arbitrary finite sequence,
so this statement has no fixed-size or unrolling bound. Per the task, I report
this as partial correctness; the verdict does not depend on claiming stronger
termination or resource guarantees.

### Trust and informal boundaries

1. **Supplied semantics.** The fixed MPY files, including K's configuration and
   primitive Python-subset behavior, are the selected trusted semantics level.
   Their material path was nevertheless audited for adequacy, and candidate
   integrity was established recursively. This is an acceptable benchmark
   trust boundary.
2. **K implementation and mathematical builtins.** Parsing, macro expansion,
   KORE generation, the Haskell/LLVM backends, SMT integration, and hooked
   integer, Boolean, map, list, and sequence operations are trusted. These are
   the ordinary proof-engine trust base, not candidate axioms.
3. **Translator/source bridge.** The mounted translator is trusted. Byte-exact
   regeneration plus constructor-level comparison pins both claims to the
   generated program. This bridge is mechanically checked and acceptable.
4. **Source-domain modeling bridge.** A Python finite `list[str]` is represented
   by unboxed `list(ValSeq)` and each string by `str(IntSeq)`; Python `len`
   corresponds to the number of represented code points. The theorem uses no
   string-content property, mutation, alias-sensitive change, or encoding
   conversion. This bridge is informal at the CPython-to-K boundary but direct,
   and the symbolic claim includes arbitrary finite code sequences. The
   differential and ground executions support this bridge without replacing
   the K proof.
5. **Canonical and concrete Python runs.** The trusted canonical function and
   CPython are empirical fidelity oracles only. They are not axioms used to
   close the reachability claims.

There are no proof-local opaque primitives, empirical lookup tables, task-answer
axioms, or unproved operational bridges. Inputs outside the stated
`list[str]` domain, Python environment mutation/monkeypatching, exceptions for
out-of-domain values, performance, and resource exhaustion are outside the
source contract and proof.

The Kit validation gates are therefore: proof success **PASS**, semantic
extension soundness **PASS**, and theorem adequacy **PASS**. No material domain
narrowing or trust-boundary limitation remains that warrants `CONCERNS`.

VERDICT: PASS
LEGITIMACY: LEGIT
