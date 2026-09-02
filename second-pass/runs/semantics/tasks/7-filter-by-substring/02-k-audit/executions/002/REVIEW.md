# Independent adversarial review: 7-filter-by-substring

## Executive conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the full stated `List[str] × str` domain as
represented by the supplied semantics. I rebuilt every definition from source,
proved the loop and entry obligations, mechanically matched the executed K term
to trusted regeneration of `solution.mpy`, checked the proof-local bridges
against bridge-free fixed-semantics paths, and obtained the expected failure
from both a body mutation and an independent false postcondition.

The proof does not replace substring containment with an oracle:
`strContains` is the fully defined function from the supplied semantics, and
the fixed comparison path reduces to that same function. The proof's list
iterator bridge is a constructor-complete symbolic exposure of the supplied
list iterator, not a task-answer rule.

## 1. Input and provenance integrity

### Launcher record and semantics boundary

I first read `/audit-input.json`. It declares:

- problem `7-filter-by-substring`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`;
- complete input provenance; and
- mounted paths through its `container_paths` map.

The required `/reference/reference-semantics` is present, so the trusted mounts
agree with the rendered mode. This is not an infrastructure-failure case.

`/audit-campaign-lock.json` is byte-hashed as
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the hash recorded in `/audit-input.json`. Its parsed JSON value equals
the complete `audit_campaign` block in `/audit-input.json`.

### Required legacy-selected-stage1 records

I read and independently hashed all required records:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL trace under `/generation-evidence/codex-trace/`
- `/generation-evidence/usage.json`, which is present

The per-file values match the launcher records and the trace hash in
`/generation-result.json`. The 335-line trace parsed with zero malformed JSON
records. The generation report says `KPROVE_PASSED`, but I treated that only as
an untrusted historical claim. `evidence/01_generation_summary.log` records a
bounded summary of the complete records and trace; `evidence/01_integrity.log`
records the exact hashes and comparison commands.

The legacy layout does not require historical runtime metrics that were never
recorded. Their absence is not a candidate defect.

### Trusted-input comparisons

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- Recursive `diff -qr --no-dereference` between candidate and trusted
  `reference-semantics/` exits 0.
- Each tree contains exactly 25 descendants, all regular files or directories.
  Neither tree contains a symlink, special entry, missing entry, changed entry,
  or additional entry.
- The per-file semantics hash manifest in
  `evidence/01_integrity.log` is identical for both trees.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` requires:

> Given a list of strings and a substring, return, in their original order,
> exactly the input strings that contain the substring.

The documented cases include an empty list and a mixed list with matching and
nonmatching strings. The typed intended domain is every finite `List[str]` and
every `str`; no size bound is stated.

`/reference/canonical.py` implements this contract with a list comprehension:

```python
return [x for x in strings if substring in x]
```

`/candidate/solution.py` uses a fresh accumulator, iterates once in input order,
and appends exactly when `substring in string`. It has the same behavior and
does not mutate its input.

### Trusted regeneration

From the scratch copy, I ran:

```text
python3 ../trusted/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both commands exit 0. The regenerated and submitted files share SHA-256
`78e9c004ec76138d1019cc2f83c68fa31f8e86289c2098228d7975b141981d7e`.
See `evidence/02_program_fidelity.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical and the scratch copy
of the candidate as separate modules. It checks:

- both documented examples;
- empty list, empty string, and empty substring;
- true and false branches;
- prefix, middle, suffix, exact, and too-long substrings;
- duplicates, overlap, case sensitivity, NUL, non-ASCII, and emoji;
- all strings over `{a,b}` through length 2 and all lists of them through
  length 3; and
- 2,000 deterministic generated Unicode-containing cases.

The run reports `total_cases=4816 mismatches=0` and exits 0. This is finite
support for source equivalence, not a substitute for the K proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

All source inputs were copied to
`/tmp/audit-work/7-filter-by-substring/`. Before building, the fresh candidate
scratch tree contained no `*-kompiled` directory. I did not use any
candidate-provided compiled definition or cache.

The installed tools independently report K version `v7.1.293`.

### Concrete definition

The exact fresh commands and results are in
`evidence/03_reconstruct_initial_interrupted.log` and the named per-command
logs:

```text
kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. A trusted regeneration of `concrete_tests.mpy` is byte-identical to the
submitted test program. Running it with:

```text
krun concrete_tests.regenerated.mpy --definition audit-runtime-kompiled
```

exits 0 and ends in a complete generated configuration with
`<exit-code> 0 </exit-code>`; see `evidence/03_concrete_krun.log`.

### Proof definition and claims

The fresh proof definition was built with:

```text
kompile verification.k \
  --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module FILTER-VERIFICATION \
  --output-definition audit-verification-kompiled
```

Exit 0. Candidate and scratch `verification.k` and `spec.k` hashes remain
identical after the build.

There are two positive claims. I checked them as follows:

1. An exact loop-only copy proves independently:

   ```text
   kprove spec-loop-only.k \
     --definition audit-verification-kompiled \
     --spec-module FILTER-SPEC-LOOP-ONLY --output pretty
   ```

   Exit 0, `#Top`; `evidence/03_loop_claim.log`.

2. The entry theorem depends on the loop theorem as a circularity. After the
   exact loop claim had independently proved, I made that already-established
   claim a trusted lemma in an otherwise exact entry spec and ran:

   ```text
   kprove spec-entry-with-proved-loop.k \
     --definition audit-verification-kompiled \
     --spec-module FILTER-SPEC-ENTRY-WITH-PROVED-LOOP --output pretty
   ```

   Exit 0, `#Top`; `evidence/03_entry_with_proved_loop.log`.

3. Finally, the untouched submitted two-claim file proves as submitted:

   ```text
   kprove spec.k \
     --definition audit-verification-kompiled \
     --spec-module FILTER-SPEC --output pretty
   ```

   Exit 0, `#Top`; `evidence/03_all_claims.log`.

For completeness, I initially tried deleting the loop dependency from the
entry module. That non-equivalent diagnostic began unbounded symbolic
unrolling and was interrupted; its empty output and the command prefix are
preserved as `03_entry_without_loop_dependency.interrupted.log` and
`03_reconstruct_initial_interrupted.log`. It is not a failed candidate claim:
the real entry proof includes, and legitimately depends on, the independently
closed loop claim.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

The loop claim at `/candidate/spec.k:9` says:

- start at the real loop head over any unvisited string suffix `SS`;
- preserve the arbitrary continuation `CONT`;
- retain the original input, substring, and result reference bindings;
- update the loop target to the last visited string (or keep the prior target
  when the suffix is empty); and
- update the heap accumulator by appending, in order, precisely each remaining
  string satisfying the supplied `strContains` predicate.

The entry claim at `/candidate/spec.k:35` says:

- from the supplied semantics' initial module state, load the submitted module
  and call `filter_by_substring` on every modeled finite string list `SS` and
  substring `P`;
- return reference 0;
- leave heap location 0 containing
  `list(filterStrings(P, SS))`;
- retain the exact loaded function closure; and
- finish with the pinned allocation counters, empty call stack, `noRet`,
  `NoExc`, and exit code 0.

The result is not a free variable or implication. `filterStrings(P,SS)` is a
total recursively defined function of the two inputs.

### Mechanical program identity

I used K's own parser and macro expander on the fresh proof definition:

```text
kast ... --sort Module --expand-macros --output kore solution.mpy
kast ... --sort Module --expand-macros --output kore \
  --expression filterProgram
cmp solution.expanded.kore filterProgram.expanded.kore
```

`cmp` exits 0. Both expanded KORE files hash to
`3b7b7961061c51a71c67aad46f6efbe7b84668becece4a7f4e793adec95f9ff6`.
Thus the entry `<k>` cell loads the exact trusted-regenerated function binding
and body. `filterLoopBody` is the exact loop body within that term. The
typing-only import is present and follows the supplied import no-op rule; no
material operation is omitted.

This mechanical result is in `evidence/04_adequacy.log`. The macros are
manually maintained rather than automatically regenerated, but that is an
artifact-maintenance observation, not an identity gap for this immutable
candidate.

### Satisfiable preconditions and ground substitutions

The exact initial state in the entry claim is the supplied configuration with
module scope 0, builtins scope -1, empty heap, allocation location 0, and empty
stack. It is concretely satisfiable.

`spec-ground.k` instantiates two such states:

- `strings=[]`, `substring="a"`, formal result `[]`;
- `strings=["abc","xxa","z"]`, `substring="a"`, formal result
  `["abc","xxa"]`.

The ground K proof exits 0 with `#Top`. Both results equal both Python
implementations (`evidence/04_ground_python.log` and
`evidence/04_ground_kprove.log`).

### Domain

`StrSeq` is the free finite datatype `.StrSeq | ssCons(IntSeq,StrSeq)`.
`IntSeq` is the supplied free code-sequence datatype. Therefore the theorem is
not a finite unrolling: it covers every finite modeled list length, every
modeled string length, empty strings, and empty substrings. Every Python string
has such a code-sequence representation. The theorem is actually broader in
allowing arbitrary mathematical integers as codes; that does not invalidate
any intended Unicode-code-point case.

The supplied semantics explicitly permits unboxed `list(VS)` values as
read-only claim inputs (`semantics/core.k:62-67`). This program does not mutate
its input, so using that supported claim representation does not narrow the
source contract.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.tsv` contains one source-located row and decision
for every relevant K declaration or rule:

- 957 total entries;
- 712 rules: 695 fixed supplied rules and 17 proof-local rules;
- 237 syntax declarations: 227 fixed and 10 proof-local;
- 5 fixed evaluation contexts;
- 1 fixed configuration; and
- 2 reachability claims.

Flags are inventoried explicitly: 148 `function`, 110 `total`, 47 priority,
2 simplification, 26 `owise`, 35 concrete, 25 symbol, and 22
`no-evaluators` declarations. There are zero `functional`, `anywhere`, or
literal `[opaque]` attributes. The 22 `no-evaluators` functions are the fixed
semantics' opaque MD5, float, and sort primitives. None is reachable from this
program or either proof claim.

The assembled `reference-semantics/semantics.k` contains module assembly only;
the inventory covers all declarations and rules in every required helper file.
`evidence/05_rule_inventory_summary.txt` gives per-file counts.

Because this is `SUPPLIED_SEMANTICS`, the recursively identical reference tree
is the selected fixed semantics boundary. All fixed rules receive a row-level
selected-semantics decision. I additionally audited every rule on the reachable
path; unreachable float, sort, MD5, dict, set, range, subscript,
comprehension, and unrelated builtin rules cannot match any submitted program
term and cannot affect closure.

### Reachable fixed-semantics path

`evidence/05_used_construct_map.tsv` maps each submitted constructor to its
declaration and operational rules. The material path is:

1. `#loadAll` and statement sequencing in `core.k:124-127`;
2. the typing import no-op in `controls.k:35-44`;
3. exact closure binding in `functions.k:14-16`;
4. callee/argument evaluation in `call.k:20-21` and `core.k:185-191`;
5. frame allocation and parameter binding in `call.k:69-75` and
   `functions.k:62-66`;
6. empty result-list allocation in `list.k:13-15` and `core.k:117-121`;
7. assignment in `controls.k:9-18`;
8. for-loop evaluation/control in `controls.k:69-74`, target binding in
   `tuple.k:31-41`, and list iteration in `list.k:9-10`;
9. name lookup in `core.k:130-154`;
10. comparison evaluation in `operators.k:15-17` and string containment in
    `str.k:29-41`;
11. if branching in `controls.k:51-54`;
12. attribute/call dispatch in `call.k:15-24`;
13. the single heap update for `append` in `list.k:53-55`; and
14. strict return and frame restoration in `functions.k:77-90`.

The syntax strictness and comparison contexts enforce the necessary evaluation
order. The program has no exceptional typed path, output, closure escape,
input mutation, or allocation inside the loop. The loop only changes its
target binding and the result heap object, exactly the cells constrained by
the invariant. The entry claim pins all observable cells in this semantics.

### Proof-local extension inventory

All proof-local items are in `/candidate/verification.k`:

| Lines | Classification | Static decision |
|---|---|---|
| 7-15 | `StrSeq` and `strVals` representation | Two structural equations preserve order and string values. No result property is encoded. |
| 17-23 | list-iteration operational bridge | Reads/writes only `<k>`, accepts an arbitrary continuation, and has exactly the empty/cons cases of fixed `list.k:9-10`. |
| 26-33 | string-comparison operational bridge | Operands are already evaluated strings; it replaces fixed `Compare -> applyCmp -> strContains` with a true/false split on that same total function. |
| 37-48 | `filterAccStrings` total summary | Base plus disjoint `true`/`false` guards cover both `Bool` values; cons recursion strictly decreases `SS`; true branch performs the same right append. |
| 50-52 | `filterStrings` total wrapper | Single unconditional equation starts the accumulator at empty. |
| 54-57 | `lastCodes` total summary | Base keeps the prior loop target; cons recursion strictly decreases and returns the last visited string. |
| 60-76 | three program macros | KORE identity proves they are the submitted module/body, not execution shortcuts. |

There are no proof-local opaque symbols, arbitrary fresh values, broad return
rules, unguarded answer rules, fabricated results, or unmodeled used
constructs.

### Bridge connection and context containment

The fixed comparison route itself universally proves:

```text
Compare(str(P), CmpOp("in", str(S))) ~> CONT
  => strContains(P,S) ~> CONT
```

For iteration, the complete `.StrSeq` and `ssCons(S,SS)` cases prove the fixed
`#iterDone` and `#iterYield` outcomes. The bridge-free audit module imports the
fixed `MPY` semantics and only the independently justified two `strVals`
representation equations; it does **not** import either candidate operational
bridge. Exposing those structurally complete equations as a total
definitional function allows congruence below `#iterNext`. All three
connection claims exit 0 with `#Top`
(`evidence/05_bridge_connections.log`).

An earlier diagnostic left `strVals` as ordinary rules, exactly as in the
candidate. It stuck before fixed iteration because K does not simplify an
ordinary rule beneath `#iterNext`. That residual is preserved in
`05_bridgefree_proof.ordinary_equations_stuck.log`; it is a proof-engineering
fact, not a false outcome. The successful bridge-free theorem uses the same
two exhaustive equations and no task property.

The corresponding bridge-enabled three-claim check also exits 0 with `#Top`
(`evidence/05_bridge_enabled_check.log`). Every connection claim quantifies
over an arbitrary continuation and frames every other configuration cell, so
there is no continuation or state-footprint broadening.

### Body sensitivity

I changed the program term actually executed by `filterProgram`, replacing
the true branch's `append` with an empty statement. The mutated definition
builds successfully. Its proof exits 1 with `WarnStuckClaimState` and the
expected unmet equality between the appended and unchanged accumulators under
`strContains(P,S) == true`. See
`evidence/05_body_sensitivity.log`.

No rule was labeled unsound because the audit found no concrete or symbolic
false-conclusion witness. The bridge diagnostics establish the narrower facts
above rather than inferring unsoundness from an initial stuck proof.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; I created a fresh one at
`evidence/spec-vacuity.k`. It keeps the exact helper claim and changes only the
entry result obligation to prepend the substring to every result:

```text
list(filterStrings(P,SS))
  ==> list(vCons(str(P), filterStrings(P,SS)))
```

This is demonstrably false for the satisfying input
`strings=[]`, `substring="a"`: both Python implementations and the original
formal result are `[]`, while the mutation demands `["a"]`.

The dry run exits 0, establishing that the mutation parses and builds against
the fresh proof definition. The actual proof exits 1 with
`WarnStuckClaimState`. Its residual reaches the real final state
`0 |-> list(.ValSeq)` on the `SS = .StrSeq` branch and fails to unify it with
the false destination. This is the intended unmet result obligation, not a
parser error, timeout, missing import, or unrelated crash.

Exact mutation diff, commands, statuses, and bounded residual are in
`evidence/06_nonvacuity.log`.

Stage 6 result: **PASS**.

## 7. Proven-versus-assumed accounting

### Precisely proven

Under the supplied K semantics and the reviewed proof-local definitions, for
every finite `SS:StrSeq` and `P:IntSeq`, starting from the supplied initial
configuration, loading the exact submitted `solution.mpy` module and calling:

```text
filter_by_substring(list(strVals(SS)), str(P))
```

reaches `ref(0)` with heap location 0 containing the ordered subsequence of
`SS` whose elements satisfy the supplied contiguous-code-sequence
`strContains(P,_)` predicate. The final closure binding, allocation counters,
stack, return state, exception state, and exit code are also constrained as
shown in the entry claim.

This is a partial-correctness reachability theorem in the Kit sense. The loop
claim supplies the inductive circularity over arbitrary finite suffixes; it is
not a bounded test or finite unrolling.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, SMT reasoning, and hooked `INT`/`BOOL`/`STRING`/`MAP`/`LIST` operations | All machine checks | Standard unavoidable proof-system trust; acceptable. |
| Exact supplied `MPY` semantics tree | Concrete execution and theorem meaning | Mandated selected semantics; byte integrity established. Reachable rules were statically reviewed. |
| Trusted `/reference/py2mpy.py` | Source-to-`solution.mpy` bridge | Byte regeneration succeeds; acceptable mechanical bridge. |
| K macro expansion of `filterProgram` | Real-program pinning | Expanded KORE is identical to regenerated `solution.mpy`; no informal substitution remains. |
| Interpretation of `IntSeq` as Python string code sequences and `StrSeq` as finite lists | Human-facing contract bridge | Direct structural representation; formal containment is fully defined and agrees with Python on all intended code-point inputs. |
| Ordinary mathematical reading of `filterStrings` as stable filtering | Human-facing postcondition | Its exhaustive structural equations directly express the prompt; no opaque value is involved. |
| Trusted canonical implementation | Differential oracle only | 4,816 zero-mismatch cases support source equivalence; not used to close K claims. |
| 22 fixed opaque `no-evaluators` primitives (MD5, float, sort) | None | Unreachable from the submitted term and claims; they do not influence any result, branch, control state, or proof obligation here. |

The supplied concrete string-literal decoder is ASCII-only, but the theorem
does not use it for inputs: it quantifies directly over abstract `IntSeq`
strings. Thus non-ASCII source inputs are included in the formal domain, while
concrete source literals outside the supplied decoder's subset are not a
claimed language-frontend result.

Excluded behavior is limited to inputs outside `List[str] × str` and Python
features outside the supplied semantics. There is no fixed-size restriction,
example-only restriction, or material narrowing of the HumanEval contract.

### Gate accounting

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **PASS**.
- Gate C, trust and evidence auditability: **PASS**.

The generation log, candidate prose, and finite tests were not used as
substitutes for the reconstructed reachability proof.

VERDICT: PASS
LEGITIMACY: LEGIT
