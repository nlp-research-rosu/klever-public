# Independent adversarial review: 26-remove-duplicates

The candidate contains a legitimate partial-correctness proof of the generated
program. I treated every candidate artifact and generation trace as untrusted,
rebuilt from source in `/tmp/audit-work`, and used the supplied semantics only
after establishing exact integrity against the trusted mounted tree.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, problem `26-remove-duplicates`, condition `semantics`,
and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mount is consistent
with the rendered mode.

The independent checker at `evidence/stage1_integrity.py` performed the
following checks; its complete output and status 0 are in
`evidence/stage1_integrity.log`.

- `/audit-campaign-lock.json` is a real regular file, its parsed object exactly
  equals the `audit_campaign` block, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are real, readable regular
  files: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` is present and was also
  inspected. Historical runtime metrics are not required for this legacy
  layout.
- Every launcher-recorded direct file hash checked by the script matches,
  including the run/task/result/invocation records, generation prompt/output,
  metrics, usage, canonical program, trusted prompt, and translator.
- The trace consists of one regular JSONL file containing 567 parseable events,
  exactly one matching session ID, and one `task_complete` event. Its raw file
  hash matches the result/invocation evidence map; the independent
  length/type/size tree hash matches `usage.json`.
- The mounted candidate tree has independent pipeline-tree hash
  `930f922364fa1e3b2a0c5a18d8be66c26f22624b4ab3820abccab1cb20ce05f9`,
  matching both the retained-workspace hash in `invocation.json` and the
  workspace hash in `generation-result.json`.
- The candidate and trusted `prompt.py` files are byte-identical. The candidate
  and trusted `py2mpy.py` files are byte-identical.
- Recursive entry/type/content comparison found no missing, additional,
  changed, mistyped, linked, or unsupported entry in
  `/candidate/reference-semantics`. Both semantics trees have independent
  pipeline-tree hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
- All five required candidate proof artifacts are present as regular files.

The generation log's prior `KPROVE_PASSED` marker and its reported `#Top`
results were not used as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py:4` requires a function on a list
of integers that removes every value occurring more than once while preserving
the order of the remaining values. The trusted canonical implementation in
`/reference/canonical.py:8` counts all occurrences and retains an element when
its count is at most one.

The submitted `/candidate/solution.py:4` traverses the input in order, appends
an element exactly when `numbers.count(number) == 1`, and returns the fresh
result list. For an element reached by this traversal its count is at least
one, so `count == 1` is equivalent to the canonical `count <= 1`. The
implementation therefore meets the contract for every finite `List[int]`,
including arbitrary-size integers.

Trusted regeneration was run from the scratch copy:

```sh
python3 /tmp/audit-work/trusted/py2mpy.py solution.py \
  > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both MPY files have SHA-256
`28e2c81f975de56588d6d8da06d0630811bd0846298e9451cacf91ea6474850e`;
the command exited 0 (`evidence/translator_regeneration.log`).

`evidence/differential_test.py` independently imports both entry points and
also cross-checks a separately coded singleton-occurrence specification. It
tested:

- 14 directed cases covering empty, singleton, the documented example,
  count-one/count-two/count-three branch boundaries, ordering, negative/zero
  values, long unique/duplicate lists, and very large integers;
- all 97,656 lists of lengths 0 through 7 over `{-2,-1,0,1,2}`; and
- 2,000 seeded cases of lengths 0 through 40 with small and 130-bit integers.

There were zero mismatches and the command exited 0
(`evidence/differential_test.log`). These tests support the source-intent
bridge; they are not being substituted for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/candidate-scratch` and did
not reuse any candidate-provided compiled definition or cache. The independently
reported tool version is K 7.1.293 (`evidence/tool_versions.log`).

The concrete definition and reviewer-authored boundary assertions were built
and run with:

```sh
python3 /tmp/audit-work/trusted/py2mpy.py \
  /audit-output/evidence/k_concrete_tests.py > audit-concrete-tests.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun audit-concrete-tests.mpy \
  --definition audit-runtime-kompiled --output pretty
```

The command exited 0. The final configuration has `.K`, `NoExc`, exit code 0,
and the expected result lists (`evidence/concrete_rebuild_and_run.log`).
Compiler totality warnings concern unused string/float/subscript helpers, not a
construct on this program's path.

The proof definition was freshly built with:

```sh
kompile verification.k --backend haskell \
  --main-module REMOVE-DUPLICATES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0 (`evidence/proof_rebuild.log`). `spec.k` contains four positive
claims: `loop-invariant`, `entry-empty`, `entry-keep`, and `entry-drop`.

The reusable invariant was proved independently:

```sh
kprove spec.k --definition audit-verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty
```

It printed `#Top` and exited 0 (`evidence/prove_loop_invariant.log`). The three
entry claims were then proved together, reusing that already-proved claim as a
lemma:

```sh
kprove spec.k --definition audit-verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty
```

It printed `#Top` and exited 0 (`evidence/prove_all_entries.log`). This split
does not assume an unproved invariant: the first command proves precisely the
claim named as trusted in the second command. `entry-empty` was additionally
selected and rerun by itself; it also printed `#Top` and exited 0
(`evidence/prove_entry_empty.log`). A non-target diagnostic that filtered to
`entry-keep` while also filtering out its lemma was bounded and interrupted;
it does not alter these successful target commands
(`evidence/prove_entry_keep_attempt.md`).

## 4. Adequacy and real-program pinning

The claims mean the following.

- `loop-invariant` (`/candidate/spec.k:9`): with `numbers = ALL`,
  `result` pointing to `ACC`, and a loop over `REST`, executing the actual loop
  body and then the arbitrary continuation `CONT` produces the same
  continuation with `result` equal to `ACC` followed, in `REST` order, by
  precisely those values whose count in `ALL` is one. Its precondition requires
  both sequences to contain only integers. It is stronger than necessary
  because it does not require `REST` to be a suffix of `ALL`.
- `entry-empty` (`spec.k:43`): the exact function closure called on the empty
  integer list allocates location 0, returns `ref(0)`, and stores the empty list
  there.
- `entry-keep` (`spec.k:64`): for nonempty `V :: REST`, when all values are
  integers and the first value occurs exactly once, the returned list starts
  with `V` and then applies the invariant summary to `REST`.
- `entry-drop` (`spec.k:93`): for the complementary first-value branch, the
  first value is absent and the returned list is the invariant summary of
  `REST`.

Empty, keep, and drop are exhaustive: every list is empty or nonempty, and the
integer equality `count == 1` or its Boolean negation partitions every
nonempty case. The helper claim matches real control flow after the first
iteration has bound `number`; the nonempty entry claims execute that first
iteration and then reuse the invariant on the remaining loop.

All preconditions are satisfiable. Ground witnesses are `[]`, `[7]`, and
`[7,7]`; the more general documented witness
`[1,2,3,2,4]` was also substituted. The claimed values are respectively
`[]`, `[7]`, `[]`, and `[1,3,4]`, equal to both Python implementations
(`evidence/claim_witnesses.log`).

The claim does not merely name a similarly shaped function. The mechanical
KAST comparison in `evidence/program_pinning.py` parses the trusted-regenerated
`solution.mpy`, extracts its `FuncDef` parameter and body constructors, expands
`#removeDuplicatesClosure`, and compares the constructor trees. Parameters,
body, and module environment 0 are exactly equal
(`evidence/program_pinning.log`). The only omitted module statement is
`ImportFrom("typing","List")`, which the supplied fixed semantics reduces to
`.K` through the non-math `ImportFrom` rule.

The return is constrained, not free: all entry claims require the returned
`ref(0)`, the exact heap location and allocation increment, and the exact list
contents given by the terminating `keepSinglesAcc` equations. A body-sensitivity
probe changed the actual expanded claim body from `count == 1` to
`count == 2` while leaving the summary and claims unchanged
(`evidence/mutations/body-verification.k`). The mutated definition built
successfully, but the invariant proof exited 1 with `WarnStuckClaimState` and
an unmet `cntOccVS` implication (`evidence/body_mutation_build.log` and
`evidence/body_mutation_proof.log`). Thus the successful theorem is sensitive
to the program term it executes.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.tsv` is the exhaustive source inventory. It contains
943 individually identified and assessed items: 702 rules, 231 syntax
declarations, five evaluation contexts, four claims, and one configuration.
The rule breakdown is 459 function equations, 238 ordinary semantic rules,
three simplification equations, and two macro equations. It records 148
function attributes, 109 `total` attributes, 45 priority uses, 35 concrete
uses, 26 `owise` uses, 22 opaque `no-evaluators` declarations, six macro
declarations, and all strictness attributes. There are no local `functional`
declarations. The inventory was generated with status 0 by
`evidence/build_rule_inventory.py`; per-file counts and every source block,
guard, attributes, materiality decision, and assessment are preserved in the
TSV (`evidence/rule_inventory_build.log`).

The exact constructor-to-rule path is in `evidence/construct_map.md`. It maps
every constructor in `solution.mpy` to declarations and rules for module/import
handling, closure creation and calls, local binding, fresh allocation, name
lookup, list creation, iteration, target binding, condition evaluation,
`list.count`, `list.append`, expression discard, return, and frame pop.

The material fixed-semantics rules preserve the relevant behavior:

- call evaluation is callee-first and arguments are left-to-right;
- the input list is read without mutation, `For` traverses it left-to-right,
  and the fresh result list cannot alias it;
- `cntOccVS` has a zero base case and complementary structural-equality
  branches, so it equals integer-list occurrence count;
- integer `==`, Boolean truth, and `If` select exactly the source branch;
- `append` updates only the result heap cell and preserves order;
- return/pop restores control and the caller environment while preserving the
  returned reference and heap.

The proof-local inventory is small and contains no operational bridge,
priority rule, or opaque result:

1. `allInts` and its two equations are exhaustive structural recursion over
   `ValSeq` and correctly recognize K integer values.
2. `keepSinglesAcc` and its three simplification equations have disjoint
   base/cons shapes, complementary `count == 1` guards, and strict descent on
   `REST`. They truthfully define the requested ordered filter.
3. `#removeDuplicatesBody` and `#removeDuplicatesClosure` are compile-time
   constructor aliases whose exact expansions were mechanically checked
   against the translated program. They do not replace runtime execution.

`keepSinglesAcc` is result-bearing, but it occurs only in the postcondition and
invariant; it does not intercept a call or skip a program operation. Its
complete recursive equations determine every use. There is consequently no
oracle, circular value abstraction, task-answer rewrite, or smuggled return.

The 22 imported opaque fixed-semantics symbols are `sortVS`, `sortKeyVS`,
`md5hexCodes`, and 19 float/conversion primitives. None occurs in the
program, proof-local rules, path condition, or postcondition. The Haskell proof
imports `MPY`, not the LLVM-only `MPY-CONCRETE` rules. Thus no opaque or
concrete-only symbol influences control or result. I found no material rule
with a false conclusion witness on the intended `List[int]` domain and do not
label any rule unsound.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation. The fresh mutation
`evidence/mutations/spec-vacuity.k` changes the satisfiable empty-input
postcondition from an empty result list to `[999]` and uses a distinct spec
module.

First, the mutated claim was compiled with `kprove --dry-run`; this exited 0,
showing that the mutation parses and builds
(`evidence/vacuity_mutation_build.log`). The actual proof command was:

```sh
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC-VACUITY \
  --claims REMOVE-DUPLICATES-SPEC-VACUITY.entry-empty --output pretty
```

It exited 1 with `WarnStuckClaimState`. The residual is the fully executed
empty-input state with `ref(0)` and heap `0 |-> list(.ValSeq)`, which does not
unify with the false `[999]` destination
(`evidence/vacuity_mutation_proof.log`). This is an expected unmet result
obligation, not a parse error, missing import, timeout, or unreachable probe.

## 7. Proven versus assumed accounting

The successful reachability proof establishes this partial-correctness
statement: for every finite K `ValSeq` whose elements are K integers, calling
the exact translated `remove_duplicates` closure from the stated fresh module
state, if execution reaches return, produces a fresh returned list containing,
in original order, exactly the input values whose total occurrence count is
one. The invariant is structural and unbounded; this is not finite unrolling
or a proof of only the tested sizes.

The trust ledger is:

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell backend, `kore-exec`, and reachability/circularity calculus | All machine-checked closure | Necessary low-level proof-checker trust |
| Trusted `py2mpy.py` | Source-to-MPY bridge | Acceptable: mounted hash matched and regeneration was byte-identical |
| Trusted supplied MPY semantics and K builtin Int/Bool/String/Map/List operations | Execution of every material source construct | Acceptable: exact trusted-tree integrity, exhaustive source inventory, material path review, and independent concrete execution |
| `cntOccVS`, `valSeqConcat`, `allInts`, `keepSinglesAcc` | Count, order, formal domain, and result | Not opaque assumptions: all have exhaustive guarded structural equations |
| Twenty-two fixed opaque symbols | None | Inert; no theorem dependency |
| Python canonical equivalence and `List[int]` intent | HumanEval intent bridge | Ordinary count argument plus broad finite differential evidence; not used to close K claims |
| Termination | Not established by a separate total-correctness theorem | Outside the requested partial-correctness result; all observed finite executions terminate |

No `PROOF.md`, generation trace, prior compiled definition, or finite
differential run was used in place of the K proof. The exact evidence-producing
commands and statuses are collected in `evidence/COMMANDS.md`.

Kit Gate A passes (real program, sound extensions, result constraint,
body-sensitivity, and non-vacuity). Gate B passes (unrestricted finite
`List[int]` domain and exact source contract). Gate C passes (explicit trust
ledger and reproducible evidence). Under the benchmark mapping, this is a
legitimate proof with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
