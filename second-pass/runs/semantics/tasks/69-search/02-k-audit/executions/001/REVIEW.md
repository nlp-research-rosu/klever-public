# Independent adversarial audit — 69-search

## Audit conclusion

The candidate is **not a legitimate proof of the real generated program**. A
fresh build does reproduce the submitted `#Top`, and the entry claim genuinely
constrains the returned value. The closure, however, depends on
`/candidate/verification.k:77-86`, an unproved operational bridge that replaces
the entire property-bearing nested loop with the desired `greatestFreq`
summary. The rule admits an arbitrary continuation and does not preserve the
loop's bindings. A reviewer-authored witness proves the concretely false result
`99` for positive input `[2]` when this bridge is enabled, while the same
program returns `2` under both Python and the supplied K semantics.

The candidate also declares a new `IntValSeq` constructor family using the
spellings `.ValSeq` and `vCons`. K treats those as distinct productions from the
supplied semantics' `ValSeq` constructors. Without the bridge, the original
target becomes stuck at `#iterNext(list(ALL:IntValSeq))`; it is not a proof by
structural induction over the real list representation.

The decisive evidence is:

- Candidate bridge proves the false `99` claim with `#Top`:
  [stage5_bridge_test.log](evidence/stage5_bridge_test.log).
- Supplied semantics alone proves the correct result `2`, then rejects `99`
  with residual `<k> 2 ~> .K </k>`:
  [stage5_fixed_context.log](evidence/stage5_fixed_context.log).
- Removing only the bridge leaves the original target stuck at the shadow
  sequence:
  [stage5_original_no_bridge.log](evidence/stage5_original_no_bridge.log).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
infrastructure-mode contradiction.

The recursive, no-symlink-following comparison found 24 regular files in each
semantics tree and no missing, additional, changed, mistyped, or symlinked
entry. `diff --no-dereference --recursive --brief` exited 0. Every paired file
also has the same size and SHA-256 digest. The complete commands and per-file
inventory are in [stage1_integrity.sh](evidence/stage1_integrity.sh) and
[stage1_integrity.log](evidence/stage1_integrity.log).

The candidate's `/candidate/prompt.py` and `/candidate/py2mpy.py` are regular
files and are byte-identical to their trusted mounted counterparts:

- `prompt.py` SHA-256:
  `62a5a2d0332d73a27da26ab1a46a7302d27bff719d9d354887d0a27a7cdc776a`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

No candidate path inspected in the required source set is a symlink. The
candidate's `__pycache__`, smoke files, mutation files, and `prove.sh` are
auxiliary, untrusted artifacts outside the semantics-integrity comparison.
They were not reused as proof evidence.

### Missing provenance evidence

The following requested untrusted provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured trace file matching `*trace*` or `*.jsonl`

These omissions reduce generation auditability but do not create an
infrastructure error and are not the basis of the substantive failure verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a non-empty list of positive integers, return the greatest positive integer
`v` whose frequency in the complete list is at least `v`. Return `-1` if no
such integer exists. This is the contract in `/reference/prompt.py:2-12`, and
`/reference/canonical.py:6-26` implements it by building a frequency array and
retaining the greatest qualifying index.

The candidate implementation in `/candidate/solution.py:1-11` is a different
but correct quadratic algorithm on that domain. For each value occurring in the
list, it recounts the value over the complete list and updates a monotone
maximum when `count >= value`.

### Trusted translation

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/69-search/solution.py > /tmp/audit-work/69-search/regenerated-solution.mpy
```

exited 0. The regenerated output is byte-identical to
`/candidate/solution.mpy`, with shared SHA-256
`dfdc8b41c7811f37945c70b0180db5eba0777a86cb249789b8242b9a7e0e52e1`.
See [stage2_run.sh](evidence/stage2_run.sh) and
[stage2_results.log](evidence/stage2_results.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently loads
`/reference/canonical.py` and the scratch copy of `solution.py`. It records:

- all three documented examples;
- smallest positive, exact-frequency, just-below-frequency, multiple-qualifier,
  repeated-value, and large-value boundaries;
- all 19,530 lists of lengths 1 through 6 over values 1 through 5;
- 500 deterministic generated lists of lengths 1 through 40 over values 1
  through 50, seed `690069`;
- explicit empty, zero, and negative out-of-contract probes.

The script exited 0 with zero intended-domain mismatches. The empty, zero, and
negative probes differ, as expected outside the stated precondition:
canonical Python respectively raises `ValueError`, returns `-1`, and raises
`IndexError`, while the generated implementation returns `-1`, `0`, and `-1`.
Those differences do not contradict the intended contract.

This differential evidence supports implementation-to-canonical fidelity only
over the recorded finite scope. It is not a substitute for the K reachability
proof.

## 3. Clean proof reconstruction

All proof sources needed for execution were copied to
`/tmp/audit-work/69-search`. The supplied semantics was copied from the trusted
mount after integrity comparison. No candidate-provided compiled definition,
cache, or trace was copied or used.

The installed toolchain is K `v7.1.337`, build date 2026-06-18. The exact
commands and bounded outputs are in
[stage3_build_run.sh](evidence/stage3_build_run.sh) and
[stage3_build_run.log](evidence/stage3_build_run.log).

Fresh results:

1. LLVM build of `reference-semantics/semantics.k`, main module `MPY-KRUN`,
   syntax module `MPY-SYNTAX`: exit 0.
2. `krun` of the reviewer-authored translated concrete smoke program: exit 0.
3. Haskell build of `verification.k`, main module `SEARCH-VERIFICATION`,
   syntax module `MPY-SYNTAX`: exit 0.
4. `kprove spec.k --definition verification-kompiled --spec-module
   SEARCH-SPEC`: exit 0 and output `#Top`.

`SEARCH-SPEC` contains exactly one positive target claim, so every positive
target was run. The builds emitted supplied-semantics warnings, including
non-exhaustiveness in unrelated float/string/list helpers in the LLVM build and
unused string-rule variables. None is on this program's used path, and the
files are byte-identical to the authoritative supplied tree.

Thus the reconstruction gate confirms the candidate's closure claim. It does
not validate the extensions that caused closure.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`/candidate/spec.k:8-30` starts in a manually constructed module state with a
`search` closure whose body is `#searchBody`. Its argument is
`list(ALL:IntValSeq)`. The precondition says:

- `ALL` is not the custom sequence's empty constructor; and
- every custom sequence element is an integer greater than zero.

The postcondition rewrites the returned `<k>` value to
`greatestFreq(ALL)`. All other displayed cells must be restored to their
starting values: environment 0, the two starting scopes, scope location 1,
empty heap and stack, no return state, no exception, and exit code 0.

This is result-constraining, not a free right-hand variable, tautology, or
one-way implication. Stage 6 confirms that an off-by-one result does not prove.

### Program body pinning

The three macro expansions at `/candidate/verification.k:8-28` reproduce,
statement for statement, the translated function body in
`/candidate/solution.mpy:2-15`. The trusted translator identity from Stage 2
supports that textual link.

There are nevertheless two material pinning gaps:

1. The claim does not execute the submitted `Module(FuncDef(...))`. It manually
   installs a closure and starts at `Call`. The manually installed body is
   exact, so this is a limited module-loading assumption rather than the
   decisive failure.
2. More importantly, the claimed outer loop body does not execute. After call,
   argument evaluation, initial `result = -1`, and lookup of `lst`, the
   proof-local rule at `verification.k:77-86` replaces the whole outer loop
   with `result = greatestFreq(ALL)`. Consequently the inner counting loop,
   comparisons, per-iteration assignments, and accumulator evolution are not
   proved under fixed semantics.

There are no helper or loop reachability claims connecting the skipped loop to
the summary.

### Satisfying states and substitutions

The custom sequence values denoting `[1]`, `[2]`, and the first documented
example satisfy the entry precondition. Ground claims for them build and prove
with expected results `1`, `-1`, and `2`; see
[ground-witness-spec.k](evidence/ground-witness-spec.k) and
[stage4_ground_witness_final.log](evidence/stage4_ground_witness_final.log).
Both Python implementations return the same values, as recorded in Stage 2.

Two earlier syntax-disambiguation attempts exited 113 before proof and are
preserved in `stage4_ground_witness.log` and
`stage4_ground_witness_retry.log`; they are not counted as proof results. Their
diagnostic is itself relevant: it shows the distinct generated labels
`.ValSeq_MPY-CORE_ValSeq` and
`.ValSeq_SEARCH-VERIFICATION_IntValSeq`.

The successful ground claims still use the candidate bridge. They exhibit
satisfiable preconditions and result constraint, but do not supply the missing
execution-to-summary theorem.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[build_rule_inventory.py](evidence/build_rule_inventory.py) generated the
line-addressable [rule_inventory.md](evidence/rule_inventory.md). It covers all
26 relevant K files: the 24 supplied-semantics files, `verification.k`, and
`spec.k`. Counts are:

- 954 declaration blocks total;
- 237 `syntax` declarations;
- 710 `rule` declarations;
- 5 contexts;
- 1 configuration;
- 1 claim.

Attribute searches find 151 function blocks, 112 total blocks, no
`functional` declarations, 7 macro blocks, no simplification rules, 35
concrete blocks, 26 `owise` blocks, 46 priority blocks, 25 `symbol` blocks, and
no hooks.

Inventory entries 1-928 are from the byte-identical supplied semantics. Their
decision is **accepted at the selected supplied-semantics level**: the task
declares this exact tree authoritative, so candidate legitimacy is assessed
relative to it rather than by replacing it with an inferred Python semantics.
Unused breadth does not affect this program. The actually exercised supplied
rules are mapped below and were also checked against their source behavior.
Inventory entries 929-953 are all proof-local declarations and rules; every
one is decided individually here. Entry 954 is the entry claim reviewed in
Stage 4.

### Every proof-local declaration and rule

| Inventory entry | Source | Decision |
|---:|---|---|
| 929 | `verification.k:8` `#innerBody` macro syntax | Accept. A name only; no execution effect by itself. |
| 930 | `verification.k:9-12` inner-body macro equation | Accept. Exact expansion of translated lines 7-9. |
| 931 | `verification.k:14` `#outerBody` macro syntax | Accept. A name only. |
| 932 | `verification.k:15-22` outer-body macro equation | Accept. Exact expansion of translated lines 5-14. |
| 933 | `verification.k:24` `#searchBody` macro syntax | Accept. A name only. |
| 934 | `verification.k:25-28` search-body macro equation | Accept. Exact expansion of translated lines 3-15. |
| 935 | `verification.k:33` `IntValSeq` constructors | **Illegitimate pinning device.** These are new overloaded productions, not refinements of the supplied constructors. The two generated K labels are distinct. |
| 936 | `verification.k:34` subsort `IntValSeq < ValSeq` | Type-correct, but does not equate either constructor family. It injects shadow sequences into `ValSeq` while fixed list iteration still recognizes the supplied constructors only. |
| 937 | `verification.k:36` `allPositive` total function | Sound over the custom two-constructor datatype; coverage is complete. |
| 938 | `verification.k:37` empty `allPositive` equation | Sound: the empty custom sequence is vacuously all-positive. |
| 939 | `verification.k:38-39` cons `allPositive` equation | Sound structural recursion with a decreasing tail. |
| 940 | `verification.k:41` `nonEmpty` total function | Sound over the custom datatype; coverage is complete. |
| 941 | `verification.k:42` empty `nonEmpty` equation | Sound. |
| 942 | `verification.k:43` cons `nonEmpty` equation | Sound. |
| 943 | `verification.k:48` `frequency` total function | Sound over the custom datatype; coverage is complete. |
| 944 | `verification.k:49` empty frequency equation | Sound: frequency is zero. |
| 945 | `verification.k:50-51` cons frequency equation | Sound structural counting equation. |
| 946 | `verification.k:53` `chooseFreq` total function | Sound if its two guarded equations are considered together. |
| 947 | `verification.k:54-57` qualifying `chooseFreq` equation | Sound: returns `X` exactly under the stated positive/frequency/larger guard. |
| 948 | `verification.k:58-61` fallback `chooseFreq` equation | Sound. Its guard is the Boolean complement of entry 947, so the pair is disjoint and exhaustive. |
| 949 | `verification.k:63-64` `greatestFreq` functions | Soundly declared total over the custom datatype; recursive equations cover empty and cons cases. |
| 950 | `verification.k:65-66` `greatestFreq` initializer | Sound definitional equation: scan the complete sequence with initial best `-1`. |
| 951 | `verification.k:67` `greatestFreqFrom` base | Sound: return the accumulated best at end of scan. |
| 952 | `verification.k:68-69` `greatestFreqFrom` step | Sound structural fold over the custom tail. |
| 953 | `verification.k:77-86` priority-40 loop rewrite | **Unsound operational bridge.** It skips property-bearing execution, has no connection theorem, accepts arbitrary continuations and omitted cells, and enables the concrete false conclusion below. |

The mathematical functions in entries 937-952 truthfully define the desired
fold over the shadow datatype. That does not justify entry 953. Using the same
`greatestFreq` symbol in the bridge and postcondition is circular: it proves the
program returns the summary only after a rule directly replaces the program's
loop by that summary.

### Used-construct coverage and fixed control flow

| Submitted construct | Declaration and fixed supplied rules | What the positive proof does |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` | Skipped by manual initial state. |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` | Skipped by manually installed closure. |
| `Call`, argument evaluation, frame push | `syntax.k:28`; `core.k:185-191`; `call.k:20-21,69-75` | Executes under supplied rules. |
| `Name` lookup | `syntax.k:12`; `core.k:130-154` | Executes for callee, `lst`, and final `result`. |
| `Int`, unary `-` | `syntax.k:9,14`; `core.k:194`; `operators.k:10`; `int.k:7` | Executes for initial `-1`. |
| `Assign` | `syntax.k:41`; `controls.k:9-18` | Initial and bridge-injected result assignments execute; loop-local assignments do not. |
| outer and inner `For` | `syntax.k:45`; `controls.k:69-74`; `list.k:9-10` | Outer fixed rule is preempted by entry 953; inner loop never executes. |
| `If` | `syntax.k:49`; `controls.k:51-54` | Loop-body branches never execute in the target proof. |
| `Compare` and integer comparisons | `syntax.k:30,32`; `operators.k:14-17`; `int.k:22-27` | Loop-body comparisons never execute. |
| `AugAssign` and integer `+` | `syntax.k:44`; `controls.k:20-31`; `int.k:9` | Counting update never executes. |
| `Return`, frame pop | `syntax.k:50`; `functions.k:78-90` | Executes after the bridge and restores the caller state. |

This mapping covers every construct in `solution.mpy`. Evaluation order is
provided by the supplied `strict`/`seqstrict` declarations. Calls, initial
lookup/assignment, return, and frame cleanup are faithful. The essential nested
loop is not.

### Complete bridge analysis

Entry 953 matches:

- an already evaluated `For(Name("value"), list(ALL:IntValSeq), #outerBody)`;
- any continuation admitted by `<k> ... </k>`;
- any current environment location `L`;
- any map `M` in that scope and any parent;
- completely omitted heap, heap allocator, call stack, return, exception, and
  exit-code cells;
- guards that `lst` is `list(ALL)`, `result` is `-1`, and `ALL` is all-positive.

It does not require `ALL` to be non-empty. Priority 40 preempts the supplied
ordinary `For` transition once the iterable has evaluated.

The fixed loop reads `lst`; binds `value` for every outer element; initializes
and updates `count`; binds `item` for every inner element; evaluates both
comparisons; and may update `result`. Entry 953 preserves none of the
`value`/`count`/`item` binding effects. Its RHS merely assigns the final summary
to `result`. The original continuation only returns `result`, so the lost
bindings are hidden after the callee frame is removed. The rule itself is much
broader: its `...` accepts a continuation that reads any lost binding.

There is no bridge-free universal connection theorem over this match domain,
no loop invariant claim, and no exact auxiliary execution claim. Finite Python
tests do not fill that gap.

### Required false-conclusion witness

[bridge_context.py](evidence/bridge_context.py) uses the exact nested loop but
sets `value = 99` before it and returns `value` immediately after it. Input
`[2]` is a satisfying non-empty positive input.

Fixed behavior:

- Python returns `2`, not `99`.
- Reviewer concrete `krun` under the supplied LLVM definition exits 0 with
  assertions `probe([2]) == 2` and `probe([2]) != 99`.
- A Haskell definition importing the supplied semantics but no candidate bridge
  proves the ground K claim `=> 2` with `#Top`.
- The corresponding `=> 99` claim exits 1 with `WarnStuckClaimState` and final
  residual `<k> 2 ~> .K </k>`.

Those artifacts are
[fixed-context-verification.k](evidence/fixed-context-verification.k),
[fixed-context-spec.k](evidence/fixed-context-spec.k),
[fixed-context-false-spec.k](evidence/fixed-context-false-spec.k), and
[stage5_fixed_context.log](evidence/stage5_fixed_context.log).

Bridge-enabled behavior:

- [bridge-unsound-spec.k](evidence/bridge-unsound-spec.k) states the false
  `=> 99` result using the candidate bridge.
- `kprove` exits 0 and prints `#Top`, recorded in
  [stage5_bridge_test.log](evidence/stage5_bridge_test.log).

The bridge skips the iteration that should overwrite `value` with `2`, so the
arbitrary continuation observes the stale `99`. This is a concrete false
conclusion enabled on the intended positive-input domain, not merely an
unproved suspicion.

Removing only the bridge from the candidate definition also makes the original
target fail at `#iterNext(list(ALL:IntValSeq))`; see
[verification-no-bridge.k](evidence/verification-no-bridge.k),
[original-spec-no-bridge.k](evidence/original-spec-no-bridge.k), and
[stage5_original_no_bridge.log](evidence/stage5_original_no_bridge.log). This
shows both that closure depends on the bridge and that the shadow sequence is
not consumed by fixed list iteration.

## 6. Fresh non-vacuity test

The candidate's body-mutation artifact was treated only as an untrusted claim.
The reviewer instead created
[fresh-vacuity-spec.k](evidence/fresh-vacuity-spec.k), changing the
result-bearing destination from `greatestFreq(ALL)` to
`greatestFreq(ALL) +Int 1`.

This mutation is demonstrably false for the satisfying input `[1]`: both Python
implementations return 1, whereas the mutation requires 2.

Results in [stage6_nonvacuity.sh](evidence/stage6_nonvacuity.sh) and
[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log):

1. `kprove ... --dry-run` exits 0, so the mutation parses and builds.
2. The actual proof exits 1 with `WarnStuckClaimState`.
3. The residual reaches the result obligation and reports the failed
   implication between `greatestFreqFrom(ALL, ALL, -1)` and that value plus 1.

This is valid non-vacuity evidence: the submitted claim discriminates a false
result. It does not repair the unsound connection between execution and the
correct result.

## 7. Proven versus assumed accounting

### What the reconstructed `#Top` actually establishes

Under the candidate-extended theory, for an abstract value built from the
candidate's custom `IntValSeq` constructors, if `nonEmpty(ALL)` and
`allPositive(ALL)`, then a call from the manually seeded closure state rewrites
to the custom mathematical fold `greatestFreq(ALL)` and restores the displayed
caller cells.

That theorem is conditional on the priority-40 rule that directly replaces the
whole nested loop by the fold. It is not a fixed-semantics theorem that the
submitted loop computes that fold, and it is not a theorem over concrete
runtime `ValSeq` constructors.

### Trust and assumption ledger

1. **Supplied semantics (accepted task boundary).** The 24 byte-identical
   files, K's integer/Boolean/string/map/list primitives, rewrite engine, and
   Haskell/LLVM backends are trusted. This is acceptable because the rendered
   mode explicitly selects that semantics. The exhaustive inventory records
   every declaration.

2. **Supplied opaque/symbol primitives (accepted but unused here).** The exact
   25 symbol declarations are:
   `md5hexCodes`; `sortVS`; `sortKeyVS`; `intFloatDiv`; `divII`; `floatMod`;
   `floatLt`; `absF`; `floorFI`; `toF`; `ceilF`; `subF`; `divF`; `addF`;
   `mulF`; `powF`; `gtF`; `eqF`; `decStrToF`; `divFloatIntV`; `intToF`;
   `truncF`; `roundF`; `roundFN`; and `sqrtF`.
   They are all in the trusted supplied tree, and none is reachable from this
   integer/list/counting program or its proof. They therefore do not influence
   control, observable state, or the final result here.

3. **Trusted translator and manual body bridge (limited).** Byte identity from
   trusted `py2mpy.py` proves the submitted `.mpy` is the translation of
   `solution.py`. Static comparison proves the manual `#searchBody` macros have
   the same AST statements. The K claim does not execute module load or
   `FuncDef`, so that small state-seeding bridge remains informal. It is
   concerning but not the decisive defect.

4. **Mathematical summary (truthful as a definition).** `frequency`,
   `chooseFreq`, and `greatestFreqFrom` are exhaustive, non-overlapping,
   descending equations over the custom datatype. The informal argument that
   their fold denotes the natural-language greatest qualifying frequency is
   straightforward and is empirically supported by the differential tests.
   Those facts do not show the real program computes the fold.

5. **Program-to-summary operational bridge (illegitimate).**
   `verification.k:77-86` is neither a trusted external primitive nor a derived
   lemma. It replaces program-defined code that is the theorem's central
   computation. It has no independent connection theorem, is context-broad,
   changes observable local bindings, and proves the concrete false `99`
   witness. Every successful entry proof depends on it.

6. **Custom `IntValSeq` interpretation (illegitimate pinning assumption).**
   The proof informally treats its new productions as the supplied list
   constructors, but K assigns distinct labels. Fixed list iteration gets stuck
   on the custom sequence. No injection/equivalence theorem connects custom
   sequences to real runtime lists.

7. **Differential bridge (finite empirical support only).** The 19,530
   exhaustive-small and 500 deterministic generated comparisons support the
   Python rewrite's intended-domain behavior. They neither prove universal
   equivalence nor validate the K loop bridge.

8. **Partial-correctness boundary.** As usual for a reachability proof of this
   form, termination is not established by the theorem. Concrete execution and
   the finite structure of the Python loops make termination plausible for the
   intended finite inputs, but that is outside what the successful candidate
   claim proves.

### Decision

The fresh positive proof and the fresh non-vacuity test both behave as claimed,
but Gate A real-program soundness fails. The operational bridge can prove a
false conclusion and the proof datatype is not the real list datatype. Under
the required decision boundary, an execution-bypassing, materially unsound
proof rule and substituted input representation require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
