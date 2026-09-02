# Independent adversarial audit: 149-sorted-list-sum

The candidate is not a legitimate proof of the submitted program under the
fixed supplied semantics. Fresh reconstruction does produce `#Top`, the entry
claim is result-constraining, and its expanded function term exactly matches the
fresh translation. However, both positive claims depend on a proof-local
priority rule that replaces the real `for` loop over an arbitrary continuation.
That rule is false on a nonempty, contract-valid list: fixed semantics binds the
loop target `word`, while the rule preserves a scope in which `word` is absent.
The bridge-free versions of both target claims stop at the genuine symbolic
iterator residual.

## 1. Input and provenance integrity

The launcher record declares:

- problem `149-sorted-list-sum`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

This is internally coherent: `/reference/reference-semantics` is present. The
campaign object in `/audit-input.json` is exactly equal as parsed JSON to
`/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

All layout-required records are readable regular files, and the required roots
are real directories rather than symlinks. I inspected `/run.json`,
`/task.json`, `/generation-result.json`, the invocation and metrics records,
the present optional `usage.json`, both Codex text logs, the generation prompt,
and the 329-record structured trace. The absent
`/generation-evidence/runtime-metrics.json` is not required for
`legacy-selected-stage1`. The legacy metrics and run-input records named by the
invocation were also present and matched their invocation-recorded hashes.
Generation claims were not used as proof evidence.

Every directly launcher-recorded content hash matches the mounted file,
including the canonical source, prompt, translator, run/task/result manifests,
invocation, metrics, usage, prompt, Codex logs, and the sole trace JSONL file.
There are no symlinks below `/candidate` or `/generation-evidence`.

The candidate prompt and translator are byte-identical to their trusted
versions. A recursive `lstat`/content comparison found exactly 25 entries in
each supplied-semantics tree and no missing, additional, mistyped, changed, or
symlinked entry. The independently defined type/path/content manifest digest is
the same for both trees:
`c8a860cf7a9e5fff3110c2dd13c2f9505aac1d7f0ef69ac7527cbc9f5c0032ad`.
Thus there is no infrastructure breach and no semantics-integrity failure.

Evidence:

- `evidence/stage1_integrity.log`
- `evidence/check_integrity.py`
- `evidence/generation_inspection.log`
- `evidence/inspect_generation.py`
- `evidence/tool_versions.log`

The independently installed tools report K `v7.1.293`, matching the campaign
lock.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `sorted_list_sum(lst)` on a list of strings. It
must remove odd-length strings, preserve duplicates, and return the remaining
strings in ascending length order with alphabetical order as the tie-breaker.
Although one prompt sentence says all words may have the same length, its
examples contain mixed lengths and the trusted canonical handles mixed
lengths. I therefore treated arbitrary finite `list[str]` inputs as the
material source-contract domain.

The trusted canonical lexically sorts the input in place, filters even lengths,
then performs a stable length sort. The candidate filters first and returns
`sorted(sorted(even_words), key=len)`. This is result-equivalent: the inner
lexical sort supplies the tie order for the stable outer length sort.

Fresh translation used:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/149-sorted-list-sum/solution.regenerated.mpy
```

It exited zero. The regenerated and submitted files are byte-identical and
share SHA-256
`39fcb6e88010732b87b6c5dee672f79d7d5b9e807254fb8074454cc36ed79662`.
See `evidence/stage2_translation.log`.

The independent differential script imports both mounted Python entry points.
It covers both documented examples, empty list/string cases, the odd/even
branch boundary, all-odd/all-even inputs, duplicates, lexical ties, mixed
lengths, Unicode, every list of length 0 through 4 over an eight-string pool,
and 1,000 seeded generated lists. All 5,693 returned results and their types
matched. The canonical mutated 4,986 input copies by sorting; the candidate
mutated none. That side effect is not required by the return-value contract and
even the canonical does not delete odd values from the input object.

Evidence:

- `evidence/differential_test.py`
- `evidence/stage2_differential.log`

This finite differential supports implementation fidelity; it is not a
universal proof.

## 3. Clean proof reconstruction

I copied source artifacts only to
`/tmp/audit-work/149-sorted-list-sum`, using the trusted semantics tree and
translator. No candidate-built definition or cache was copied.

The concrete definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited zero. Independent translated assertions then ran with:

```text
krun k_concrete_tests.mpy \
  --definition runtime-audit-kompiled --output pretty
```

That also exited zero with final `.K`, `NoExc`, and exit code `0`. The tests
cover the examples, empty input/string, each filter branch, ties, duplicates,
and mixed lengths. See `evidence/stage3_kompile_llvm.log`,
`evidence/k_concrete_tests.py`, and `evidence/stage3_krun_concrete.log`.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module HUMANEVAL-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited zero. The unmodified complete spec then exited zero and printed
`#Top`:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module HUMANEVAL-SPEC
```

See `evidence/stage3_kompile_haskell.log` and
`evidence/stage3_kprove_all.log`.

Because the two source claims are unlabeled, I added labels without changing
their bodies, requirements, or ensures. JSON comparison confirmed the original
and labeled claim-term multisets are identical. Each was then run separately:

```text
kprove /audit-output/evidence/spec-labeled.k \
  -I /tmp/audit-work/149-sorted-list-sum \
  --definition verification-audit-kompiled \
  --spec-module HUMANEVAL-SPEC-LABELED --claims loop-contract

kprove /audit-output/evidence/spec-labeled.k \
  -I /tmp/audit-work/149-sorted-list-sum \
  --definition verification-audit-kompiled \
  --spec-module HUMANEVAL-SPEC-LABELED --claims entry-point
```

Both exited zero and printed `#Top`. See
`evidence/stage3_claim_compare.log`,
`evidence/stage3_kprove_loop_claim.log`, and
`evidence/stage3_kprove_entry_claim.log`.

These are successful verification runs under the candidate-extended theory.
They do not establish that the added theory is sound.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim has no Boolean `requires`; its precondition is structural. The
`<k>` cell contains the candidate's exact loop over
`list(strVals(INPUT))`, followed by arbitrary `CONT`. The current frame must
contain exactly `lst` and `even_words`, with the accumulator at heap location
`H`. Other scope and heap entries are framed. It claims the loop disappears,
the accumulator becomes `evenAppend(ACC, INPUT)`, and every shown scope entry
is unchanged.

The entry claim starts from an empty module frame, empty heap, allocation
counters 1 and 0, empty call stack, `noRet`, `NoExc`, and exit code 0. It
defines `sorted_list_sum` and calls it on an arbitrary structurally encoded
list of strings. It claims termination at `ref(2)`, with:

- heap 0: the even-length filter result;
- heap 1: `sortVS` of that result;
- heap 2: `sortKeyVS` of heap 1 with builtin `len`;
- heap allocation counter 3 and the expected global function binding.

The returned value is therefore constrained; it is not a free variable,
tautology, or one-way implication.

Both preconditions are satisfiable. `INPUT = .StrList` supplies an empty
example. A nonempty example is
`sCons(iCons(97, iCons(97, .IntSeq)), .StrList)`, representing `["aa"]`.
Five ground interpretations of the entry postcondition, including both prompt
examples and tie/duplicate cases, agree with both Python implementations. See
`evidence/claim_ground_instances.py` and
`evidence/stage4_ground_instances.log`.

### Mechanical program identity

I parsed the freshly regenerated `solution.mpy` with the fresh proof
definition and expanded macros. I also emitted the original spec as JSON.
There is exactly one `FuncDef` in the program and exactly one in the entry
claim. Their complete constructor JSON objects are equal and share SHA-256
`2c466ac780a60de08b29b42829d93153cc7fcbaf738588c4bd4398de541af858`.
This compares the binding, parameter list, and complete body, not source text
or an external hash alone.

Evidence:

- `evidence/compare_program_term.py`
- `evidence/stage4_kast_solution.log`
- `evidence/stage4_program_term_compare.log`

A material mutation changed the executed claim term from filtering remainder
`0` to filtering remainder `1`, updated the stored closure consistently, but
kept the even-filter result obligation. The spec compiled, reached the changed
loop, and failed at the symbolic iterator residual. This confirms body
sensitivity of the actual claim term. See
`evidence/spec-body-mutation.k` and
`evidence/stage4_body_sensitivity.log`.

The input is a bare `list(ValSeq)` rather than a heap reference. The supplied
core explicitly permits bare list values as read-only claim inputs, and this
candidate does not mutate `lst`; this is a semantically inert claim-input
normalization for this function.

### Fatal operational-bridge counterexample

`verification.k:71-93` adds this operational rule at priority 40:

```text
#loop(list(strVals(INPUT)), Name("word"), filterBody) ~> CONT
  => CONT
```

It updates only the `even_words` heap object. Its match domain accepts
arbitrary `CONT`, while its scope pattern and right-hand side contain no
`word` binding. Fixed semantics at `tuple.k:32-34` binds `word` on every
nonempty yielded element, and Python `for` targets remain bound after the
loop.

A concrete false-conclusion witness uses the contract-valid input `["aa"]`,
the exact loop body, a normal builtins/global/local chain, an empty accumulator,
and the immediate continuation `Name("word")`:

- fixed semantics proves that the loop appends `"aa"`, adds
  `"word" |-> "aa"` to the local scope, and evaluates the continuation to
  `"aa"` (`evidence/bridge-context-witness.k`,
  `evidence/stage4_bridge_witness_fixed.log`: exit 0, `#Top`);
- specializing the candidate bridge to the same observable continuation
  proves a transition to `Name("word")` while the scope still lacks `word`
  (`evidence/bridge-spurious-transition-extended.k`,
  `evidence/stage4_spurious_transition_extended.log`: exit 0, `#Top`);
- removing the bridge leaves that same symbolic transition stuck at
  `#iterNext(list(strVals(INPUT)))`
  (`evidence/bridge-spurious-transition.k`,
  `evidence/stage4_spurious_transition_no_bridge.log`: exit 1 with
  `WarnStuckClaimState`).

Thus the bridge-enabled theory admits the false conclusion that a nonempty
loop can skip its target-binding state effect. The candidate comment that
`word` is dead in the submitted suffix does not narrow the rule: `CONT:K` is
arbitrary. There is no bridge-free universal connection theorem over that
complete domain.

This is material to the positive result. I compiled an otherwise identical
definition with only this bridge removed. JSON comparison confirms the two
reviewer-labeled claims are the same as the originals. Both then fail at the
genuine symbolic iterator residual:

- `evidence/verification-no-bridge.k`
- `evidence/stage4_no_bridge_diff.log`
- `evidence/stage5_no_bridge_claim_compare.log`
- `evidence/stage5_no_bridge_loop_claim.log`
- `evidence/stage5_no_bridge_entry_claim.log`

The entry claim happens not to read `word` after its loop, but a globally false
operational rule cannot be admitted merely because one current suffix does not
observe the lost state. It is exactly the rule on which entry closure depends.

## 5. Rule-by-rule static soundness review

`evidence/stage5_rule_inventory.log`, generated by
`evidence/build_rule_inventory.py`, is the exhaustive source-level inventory
for the trusted semantics copy, `verification.k`, and `spec.k`. It contains
947 sentences:

- 705 rules;
- 234 syntax declarations;
- 5 contexts;
- 1 configuration;
- 2 claims.

It records every source range and full normalized sentence, including all
`function`, `total`, `symbol`, `no-evaluators`, `concrete`, `owise`, priority,
macro, and strictness attributes. There are no local `functional` or
`simplification` declarations.

`evidence/stage5_rule_dispositions.log`, generated by
`evidence/assess_rule_inventory.py`, assigns a disposition to every one of the
947 entries. Its totals are:

- 129 accepted program-relevant fixed rules and 69 relevant declarations;
- 9 accepted concrete reference rules;
- 2 conditionally accepted result-bearing opaque primitives;
- 16 accepted proof-local definitions/macros;
- 531 unused fixed rules, 142 unused declarations, 26 unused concrete rules,
  and 20 unused opaque primitives with no submitted-program redex;
- 1 rejected unsound proof rule, 1 rejected fixed-semantics loop claim, and
  1 target claim dependent on the rejected rule.

For unused constructs I assert no unsoundness: they have no matching redex in
the submitted term or claims, and I found no relevant false-conclusion witness.
The compiler's non-exhaustiveness warnings concern unused total functions such
as float/helper projections and do not affect this program path.

### Program-construct map

| Submitted construct | Declaration and operational rules | Audit |
|---|---|---|
| `Module`, `FuncDef`, name binding/call | `syntax.k:53,61`; `core.k:124-132`; `functions.k:14-20`; `call.k:69-74` | Exact closure body and lexical parent; call frame, parameter binding, and return/pop cells align. |
| `even_words = []` | strict `Assign` in `syntax.k:41`; argument/list allocation in `core.k:185-191`, `list.k:13-15`; assignment in `controls.k:9-18` | Evaluates RHS first, allocates heap 0, then binds local. |
| `for word in lst` | strict iterable in `syntax.k:45`; `controls.k:69-74`; list iteration `list.k:9-10`; target bind `tuple.k:32-41` | Fixed semantics iterates left to right and binds `word`; the proof bridge fails this footprint. |
| `if ...` | strict guard plus `controls.k:51-54` | Correct branch selection through `truthy`. |
| `len(word) % 2 == 0` | name/call routing in `core.k`/`call.k`; `builtins.k:17-26`; `int.k:15,19-20,26`; `operators.k:10-17` | `isLen` and divisor-2 `pyMod` give the intended parity test. |
| `even_words.append(word)` | attribute/callee evaluation `call.k:15-24`; mutable-method routing `call.k:52-60`; `list.k:53-55` | Preserves argument order and appends in place to heap 0. |
| nested `sorted`, `key=len` | left-to-right argument evaluation `core.k:185-191`; lookup/call rules; `sort.k:18-37,49,61-62` | Allocates lexical sort at heap 1 and keyed sort at heap 2; symbolic sort values are opaque trust boundaries. |
| `return` | strict return plus `functions.k:77-90` | Returns ref 2, restores caller frame, preserves escaping heap objects. |

### Proof-local extensions

- `StrList`, `strVals`: constructor encoding for arbitrary finite string
  sequences; its two equations are disjoint and structurally descending.
- `evenAppend [function,total]`: the empty and two constructor cases are
  exhaustive. The parity guards are disjoint, divisor 2 is nonzero, and
  recursion descends on `StrList`. It is a truthful filter/append definition.
- `filterBody`, `solutionBody`: macros. The expanded solution body is
  mechanically identical to the submitted translation.
- `solutionClosure`, `solutionGlobals`: complete one-rule definitional
  functions matching the actual module binding.
- `verification.k:71-93`: rejected operational bridge, with the false state
  transition witnessed above.

Relevant fixed-semantics guards are disjoint or agree on overlap. The priority
rules used for dereference, allocation, method routing, and concrete keyed sort
preserve the cells touched by the displaced fixed operation on this path. The
candidate priority-40 loop rule is the sole program-relevant rejected rule.

### Opaque sorting boundary

`sortVS` and `sortKeyVS` are supplied `function,total,symbol,no-evaluators`
primitives. The proof-mode theorem returns exactly terms containing those
symbols; it does not prove lexical ordering or stable key ordering inside K.
The concrete-only module evaluates lexical string sorting and stable keyed
sorting by real key calls, and the fresh K/Python tests support that intended
bridge on finitely many cases.

This is an explicit fixed external primitive boundary rather than a
proof-local oracle replacing program-defined code. It would be an evidence
limitation in an otherwise sound proof, but it cannot justify or repair the
false loop bridge.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. I created
`evidence/spec-vacuity-audit.k`, which retains the exact entry precondition and
execution but changes the result object at heap 2 to `list(.ValSeq)`.
`INPUT = ["aa"]` satisfies the precondition and both Python implementations
return `["aa"]`, so the mutation is demonstrably false.

The dry run:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/149-sorted-list-sum \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited zero, establishing that the mutation parses and builds. See
`evidence/stage6_vacuity_dry_run.log`.

The actual proof with the same command minus `--dry-run` exited 1 with
`WarnStuckClaimState`. The final configuration unified with the destination,
but the implication failed on:

```text
.ValSeq
  #Equals
sortKeyVS(sortVS(evenAppend(.ValSeq, INPUT)), builtinV("len"))
```

See `evidence/stage6_vacuity_proof.log`. This is the expected unmet
result-content obligation, not a parser error, timeout, missing import, or
unrelated crash. The candidate theorem is non-vacuous and result-constraining.
Non-vacuity does not imply soundness of its theory.

## 7. Proven versus assumed accounting

### What the successful run establishes

Under the combined theory consisting of the supplied `MPY` modules plus every
rule in candidate `verification.k`, K proves that, for every `INPUT:StrList`,
the exact submitted function term reaches `ref(2)` from the stated initial
configuration and leaves the three heap entries described in the entry
postcondition. It also proves the loop-summary claim as stated.

That conditional statement is precise, but it is not a theorem of the fixed
semantics because the added theory contains the false loop transition. Once
that rule is removed, neither positive claim closes.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell prover, LLVM runner | All machine results | Ordinary toolchain trust; versions recorded and sources rebuilt fresh. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Trusted benchmark translator; regeneration is byte-identical and the expanded constructor comparison independently pins the claim. |
| Supplied operational semantics on the used path | Binding, evaluation order, heap allocation, calls, loop execution, return | Audited rule-by-rule for the used term and supported by fresh concrete execution. |
| `sortVS` | Lexical inner sort, heap 1, final tie order | Fixed external opaque primitive in proof mode; conditional contract, finitely supported by concrete K and Python tests. |
| `sortKeyVS(..., builtinV("len"))` | Stable length sort, returned heap 2 | Fixed external opaque primitive in proof mode; conditional contract, finitely supported by concrete K and Python tests. |
| `StrList`/`IntSeq` representation | Formal input-domain bridge | Structurally enforces a finite list of string values. Valid Python code-point sequences are included; arbitrary K integers make it over-broad, not domain-narrowing. |
| `evenAppend` | Filtered accumulator formula | Truthfully defined by complete, disjoint, descending equations; no separate assumption. |
| Priority-40 loop summary | Entire loop, accumulator, control continuation, local scope | Illegitimate. It is program-derived, has no bridge-free universal connection theorem, accepts arbitrary continuations, and loses the nonempty-loop target binding. Both target claims depend on it. |
| Differential and ground tests | Python equivalence and intended interpretations of opaque sorts | Finite empirical evidence only; not a substitute for a K connection theorem or reachability proof. |

### Decision

The clean `#Top`, exact program pinning, full structural input domain, and
meaningful failed mutation are positive findings. They do not outweigh Gate A:
the proof depends on a materially unsound operational bridge with an explicit
false-conclusion witness, and the targets fail under the otherwise identical
bridge-free definition. Under the benchmark decision boundary this is a failed,
not merely limited, proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
