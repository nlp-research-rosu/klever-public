# Independent adversarial review: 1-separate-paren-groups

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed both definitions from
trusted/source artifacts, explicitly selected both positive claims, obtained
`#Top` with exit 0, mechanically matched the claimed closure to the regenerated
program KAST, reviewed every task-local proof rule, and rejected a fresh false
result claim with the expected stuck residual.

I did not rely on the candidate's `PROOF.md`, compiled definitions, generation
report, traces, or prior `#Top`. Those were treated only as untrusted historical
claims.

## 1. Input and provenance integrity

### Declared layout and mode

`/audit-input.json` declares:

- problem `1-separate-paren-groups`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a mounted trusted semantics tree at
  `/reference/reference-semantics`.

The trusted semantics mount is present, so it does not contradict the rendered
mode. The audit continued normally; no infrastructure-breach early exit was
required.

### Campaign and required records

The `audit_campaign` object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. The independently calculated lock digest is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded digest. K reports version 7.1.293, matching the
campaign lock.

Every `pipeline-v3` required record exists with the expected regular-file or
directory type:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured JSONL trace below
  `/generation-evidence/codex-trace/`.

Independently calculated file digests match the launcher records, including the
run/task/result/invocation records and every generation evidence file. The
trace's sole JSONL file hashes to
`7519ed38f77736960dae4961c14233d6fef280efebc39952ed5daa718b9e4acb`,
matching the per-file generation record. All 362 JSONL records parse; the
inventory found 78 tool calls and the final generation report, but none was
accepted as proof evidence.

### Trusted-input and supplied-semantics integrity

The following candidate artifacts are byte-identical to their trusted mounts:

- `/candidate/prompt.py` and `/reference/prompt.py`, SHA-256
  `ba4d0641a184fb3cdd632060a25d6408a7e91fe9d79b5c341407e74b80536327`;
- `/candidate/py2mpy.py` and `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

A recursive, no-dereference comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` reports no difference. Both trees contain the
same 25 regular K source files and directories, with identical per-file hashes.
No symlink exists anywhere in the candidate semantics, trusted semantics,
candidate mount, or generation-evidence tree. Thus there is no missing,
additional, changed, mistyped, or symlinked supplied-semantics entry.

Detailed commands, exit statuses, per-file hashes, record inventory, and trace
summary are in:

- `/audit-output/evidence/stage1_integrity.sh`;
- `/audit-output/evidence/stage1_integrity.log`;
- `/audit-output/evidence/trace_inventory.py`.

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt specifies a string consisting of separate balanced groups
of nested parentheses, with spaces ignored. The required output is the ordered
list of maximal top-level groups after removing spaces. For example,
`"( ) (( )) (( )( ))"` must produce `["()", "(())", "(()())"]`.

The intended input domain is therefore finite strings over ASCII space, `(`,
and `)` whose space-free projection is a balanced-parenthesis word: depth never
goes negative and ends at zero. Empty and spaces-only strings are harmless
boundary cases. Behavior on letters, unmatched delimiters, or other characters
is not part of this source contract.

The trusted canonical implementation increments depth on `(`, decrements it on
`)`, accumulates parentheses, and emits the accumulator when depth returns to
zero. The candidate implements the same behavior on the intended domain with a
string accumulator. Its `else` after testing `char == "("` would treat any
other non-space character as `)`, but the formal precondition excludes such
characters; this does not narrow the prompt's parenthesis-and-space domain.

### Trusted regeneration

In clean scratch space I ran:

```text
cd /tmp/audit-work/reconstruction &&
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated file is byte-identical to `/candidate/solution.mpy`; both hash
to `1d8ba86f3eaad4413c7c38e0f6630c8cdb532d378f30bf9ebe34f755ae6e22a9`.
This pins the submitted MPY module to `/candidate/solution.py` through the
trusted translator.

### Independent differential testing

`/audit-output/evidence/differential_audit.py` separately imports:

- the trusted entry point from `/reference/canonical.py`;
- the candidate entry point from `/candidate/solution.py`;
- an auditor-written top-level splitting oracle.

It includes the prompt example, empty and spaces-only inputs, adjacent groups,
deep nesting, branch boundaries, all balanced words from zero through seven
parenthesis pairs, and six spacing transformations. The preserved result set
contains 3,755 distinct inputs. All three implementations agree:

```text
TOTAL_DISTINCT_CASES=3755
MISMATCHES=0
```

The complete input/result corpus is
`/audit-output/evidence/differential_inputs_results.json`. Commands and status
are in `/audit-output/evidence/stage2_fidelity.log`. This finite evidence
supports program/canonical/intent alignment; it is not used as a substitute for
the universal K proof.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

### Isolation

Only source artifacts were copied to `/tmp/audit-work/reconstruction`:
trusted prompt/canonical/translator/reference semantics plus candidate
`solution.py`, `solution.mpy`, `verification.k`, and the spec sources. No
candidate `runtime-kompiled`, `verification-kompiled`, cache, binary,
`allRules.txt`, or generated definition was copied or used.

### Fresh builds and concrete definition

The LLVM definition was built from the trusted scratch semantics:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Running the regenerated submitted module under that definition
also exited 0 and produced a normal configuration. Logs:

- `/audit-output/evidence/stage3_llvm_build.log`;
- `/audit-output/evidence/stage3_solution_krun.log`.

The Haskell proof definition was independently built from scratch:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. The warnings are unused-variable warnings in the supplied
semantics/spec, not build failures. See
`/audit-output/evidence/stage3_haskell_build.log`.

### Every positive target claim

`spec.k` contains exactly two positive claims:
`SPEC.loop-invariant` and `SPEC.function-correct`. I explicitly selected both:

```text
timeout 300 kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant,SPEC.function-correct
```

Actual result:

```text
#Top
[exit 0]
```

The command and bounded output are in
`/audit-output/evidence/stage3_explicit_claims.log`. An unfiltered complete
`SPEC` run independently produced the same `#Top`, exit 0
(`/audit-output/evidence/stage3_all_claims.log`). The loop claim also closes
alone (`/audit-output/evidence/stage3_loop_claim.log`).

A diagnostic attempt to select only `function-correct` was interrupted after
approximately two minutes. That selection removes the separately stated loop
circularity on which the function claim depends, so it is not the candidate's
complete target-proof command and is not evidence that either submitted claim
fails. The interruption and exit 130 are preserved in
`/audit-output/evidence/stage3_function_claim.log`; it is superseded for the
positive gate by the explicit two-label run above.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` says:

> At the actual translated `for` loop head, for arbitrary remaining string
> suffix `S`, current depth `D`, current group `CUR`, and previously emitted
> groups `OUT`, fixed-semantics execution of the exact loop finishes with heap
> location `H` containing `scanParenGroups(S,D,CUR,OUT)`. It preserves the
> stack, return/exception/exit state, allocation counters, outer scopes, and
> framed heap; only the loop locals and group-list heap cell may change.

The post-loop values of `char`, `current`, and `depth` are existential because
the function only returns `groups`; those locals are popped and are not
observable. The output heap cell is not existential.

`SPEC.function-correct` says:

> For every `IntSeq S` accepted by `validParenInput`, lookup and call the
> pinned `separate_paren_groups` closure. If the call terminates, it returns
> `ref(0)`, heap location 0 contains
> `list(separateParenGroupsSpec(S))`, heap allocation advances from 0 to 1,
> the call stack is empty, return state is `noRet`, exception state is
> `NoExc`, and exit code is 0.

This is an equality-style result constraint, not a free variable, tautology,
or one-way implication.

### Constructor-level program identity

`/audit-output/evidence/pinning_check.py` parses both:

1. the trusted-regenerated `solution.mpy` function definition; and
2. the closure literally embedded in `SPEC.function-correct`.

It removes only explicit `.Stmts`/`.Exprs` unit tails needed to move the term
from K's rule parser to its standalone program parser. No statement or
expression is removed. KAST comparison reports:

```text
FUNCTION_NAME_IS_TARGET=True
PARAMETERS_KAST_EQUAL=True
BODY_KAST_EQUAL=True
DEFINING_SCOPE_IS_ZERO=True
TRANSLATED_BODY_SHA256=45b3c6a46d9e3d4ef550aadfc55ec233bc869f45e3f25bb3186c634ea17eb3a4
CLAIMED_BODY_SHA256=45b3c6a46d9e3d4ef550aadfc55ec233bc869f45e3f25bb3186c634ea17eb3a4
```

See `/audit-output/evidence/stage4_pinning.log`.

The fixed rule in `semantics/functions.k:14-16` installs
`FuncDef(F,Params(PNS),BODY)` as `closureVal(PNS,BODY,L)` without rewriting the
body. The omitted module-level `typing.List` import is handled by the supplied
non-math import no-op and is typing-only. Thus the entry claim is the permitted
semantically inert normalization of the submitted module: it begins after
installation but mechanically pins the exact selected binding and body.

### Satisfiable preconditions and concrete substitutions

Auditor-authored ground claims establish:

- `validParenInput("") == true`;
- `validParenInput("()") == true`;
- `validParenInput("( ) (( )) (( )( ))") == true`;
- `separateParenGroupsSpec("") == []`;
- `separateParenGroupsSpec("()") == ["()"]`.

Each selected claim printed `#Top` and exited 0. Evidence is in
`/audit-output/evidence/spec-witnesses.k` and the
`stage4_witness_*.log` files.

For the same three inputs, both trusted canonical Python and candidate Python
return equal results
(`/audit-output/evidence/stage4_python_witnesses.log`). An auditor-built LLVM
harness has an exact byte-for-byte `solution.py` prefix and appends only ground
assertions. It executes the empty, spaces-only, single, nested, adjacent, and
prompt inputs, ending with `.K`, `NoExc`, exit code 0:

- `/audit-output/evidence/make_concrete_harness.py`;
- `/audit-output/evidence/stage4_make_harness.log`;
- `/audit-output/evidence/stage4_krun_harness.log`.

An auxiliary ground K simplification of the full prompt-sized
`separateParenGroupsSpec` term timed out at both 30 and 180 seconds without
output. This reviewer-only helper is not the target proof: the universal
two-claim proof already closes and actual K execution of the prompt assertion
succeeds. Per the audit instructions, the timeout is preserved in
`stage4_witness_prompt_result.log` and
`stage4_witness_prompt_result_long.log` and is not converted into a candidate
defect.

### Intent bridge

On a `validParenInput` sequence, a direct induction over consumed characters
maintains:

- `D` is the nesting depth of the space-free unfinished `CUR`;
- `OUT` is exactly the ordered list of completed maximal top-level balanced
  groups from the consumed prefix;
- a space changes none of those values;
- `(` increments depth, and `)` decrements a positive depth;
- reaching depth zero appends exactly one completed group and clears `CUR`.

The domain predicate prevents negative prefixes and requires final depth zero,
so no unfinished group remains. Consequently `separateParenGroupsSpec` is the
requested top-level partition, not merely an arbitrary execution trace. The
3,755-case independent differential test supports this ordinary mathematical
bridge but does not replace the induction or K proof.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/rule_inventory.md` and `.json` enumerate every local K
sentence in the trusted supplied semantics, candidate `verification.k`, and
candidate `spec.k`, with exact file/line, normalized sentence, attributes, and
origin. Totals:

- 26 K source files;
- 943 sentences;
- 230 syntax declarations;
- 705 rules;
- 5 contexts;
- 1 configuration;
- 2 reachability claims.

Attributes include all 148 functions, 110 `total` declarations, 45 priorities,
35 `concrete` sentences, 26 `owise` rules, 22 `no-evaluators` declarations, 25
symbols, strictness/context declarations, and macros. There are no
`[simplification]` or `[functional]` sentences. The generation script and
summary are `/audit-output/evidence/k_inventory.py` and
`k_inventory.log`.

### Task-local rules

The task-local inventory has three function declarations and ten defining
rules:

1. `scanParenGroups`:
   - `.IntSeq` returns `OUT`;
   - `iCons` consumes one code;
   - code 32 preserves all accumulators;
   - code 40 appends to `CUR`, increments depth, and emits iff new depth is
     zero;
   - every other code follows the submitted source's literal `else`, appends
     to `CUR`, decrements depth, and emits iff new depth is zero.
2. `separateParenGroupsSpec` initializes scanner depth/current/output.
3. `validParenInput`/`validParenSuffix`:
   - empty accepts iff depth is zero;
   - space preserves depth;
   - open increments;
   - close at positive depth decrements;
   - close at nonpositive depth and any other code return false.

The cases are constructor-disjoint. For close-parenthesis depth, `D > 0` and
`D <= 0` are exhaustive and disjoint. The other-code guard excludes 32, 40,
and 41. Every recursive rule consumes one `IntSeq` constructor. Thus each
`[total]` declaration has truthful coverage and descent; none functions as an
unconstrained oracle.

These functions are definitional summaries. They do not rewrite `<k>`, skip a
call, preempt a supplied rule, allocate state, return abruptly, or alter
control. Their result affects the heap postcondition, but the universal loop
claim connects that result to fixed execution.

### Used semantics and control/state fidelity

Every construct in `solution.mpy` maps to fixed declarations/rules:

- name lookup, left-to-right callee/argument evaluation, closure frame
  allocation, parameter binding, return, and frame pop;
- statement sequencing and string/integer literals;
- fresh list allocation and in-place `append`;
- plain assignment and integer/string augmented assignment;
- one-time string iterable evaluation, one-character yield, target binding,
  loop step, and recurrence;
- strict/context-ordered comparison and conditional branching.

The entry/loop claims include every material state cell: `<k>`, `<env>`,
`<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`,
and `<exit-code>`. There is no omitted output, exception, call-stack, or
allocation effect relevant to this function.

Relevant fixed priority overlaps are benign and correctly guarded:

- closure-cell assignment/binding rules require a `"$cells"` marker absent
  from this plain closure;
- ref-valued augmented assignment does not apply to string/integer locals;
- the exact `append` priority retains the list reference and mutates only its
  heap cell;
- no task-local call interception exists, so ordinary `[owise]` call routing
  executes.

The detailed construct-to-rule map, per-task-local-rule judgments, priority
analysis, and state footprints are in
`/audit-output/evidence/static_assessment.md`.

### Opaque/trusted primitives

The supplied semantics contains opaque float, sort, and digest primitives,
including all 22 `no-evaluators` symbols listed in
`static_assessment.md`. None is reachable from the submitted function,
precondition, summary, or either claim. `MPY-CONCRETE` is imported only in the
LLVM runtime build, not `VERIFICATION`. No opaque value can influence this
program's branch, returned list, state, exception, or postcondition.

No task-answer rule, operational bridge, false equation, priority shortcut, or
unconstrained result-bearing abstraction was found. This audit therefore makes
no unsound-rule allegation and needs no false-conclusion witness. The narrower
boundary is simply that the supplied semantics is an intentionally partial
Python model; the used subset is reviewed above.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation is
`/audit-output/evidence/spec-audit-false.k`.

It calls the exact submitted closure through the pinned target name on the
satisfying valid input `"()"`. It preserves the correct return reference and
normal control cells but changes the result-bearing heap obligation from the
correct `["()"]` to the deliberately false `[]`.

The mutation first built successfully:

```text
kprove spec-audit-false.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE --dry-run
[exit 0]
```

The actual proof then exited 1 with `WarnStuckClaimState`, not a parser error,
missing import, timeout, or unrelated crash. Its residual is normal completion
with:

```text
<heap>
  0 |-> list(vCons(str(iCons(40,iCons(41,.IntSeq))),.ValSeq))
</heap>
```

That is the expected actual result `["()"]`, which cannot unify with the false
empty-list destination. Evidence:

- `/audit-output/evidence/stage6_nonvacuity.sh`;
- `/audit-output/evidence/stage6_false_dry_run.log`;
- `/audit-output/evidence/stage6_false_proof.log`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every finite `IntSeq S` such that:

- every code is ASCII space 32, open parenthesis 40, or close parenthesis 41;
- no space-free prefix has negative parenthesis depth;
- final depth is zero;

the actual submitted closure body is partially correct: if its call terminates,
it returns the fresh list reference 0 and heap location 0 contains exactly
`separateParenGroupsSpec(S)`, with normal stack/return/exception/exit state.
The loop claim universally establishes that the fixed loop execution transforms
arbitrary current/output accumulators according to `scanParenGroups`.

Together with the domain/spec induction in Stage 4, the stored list is exactly
the source contract's ordered, space-free top-level balanced groups.

### Trust and evidence ledger

| Boundary | Influence | Status |
|---|---|---|
| Trusted `/reference/py2mpy.py` | Converts candidate Python AST to the K constructor module. | Acceptable explicit benchmark boundary. Byte-identical regeneration and KAST pinning establish artifact identity, not universal translator correctness. |
| Trusted supplied reference semantics | Defines lookup, strings, integers, lists, iteration, calls, scopes/heaps, and control. | Acceptable selected semantics boundary. Candidate copy is byte/type identical; every used rule is statically mapped. The theorem is not a proof of full CPython. |
| K 7.1.293 frontend/Haskell backend | Parses, compiles, and checks reachability/circularity. | Standard proof-checker trust boundary. Fresh builds and repeated `#Top` runs are recorded. |
| `scanParenGroups`, `separateParenGroupsSpec`, domain functions | Determine the result/postcondition and applicability. | Proven definitions, not assumed or opaque. Equations are exhaustive/descending; loop execution is machine-connected to the scanner. |
| Spec-to-English partition interpretation | Connects the pure scanner/domain to “separate top-level balanced groups.” | Ordinary inductive argument given in Stage 4, supported by independent canonical/oracle differential testing. It is not used to bypass execution. |
| Trusted canonical and Python differential corpus | Supports implementation/intent alignment for 3,755 inputs. | Finite empirical evidence only; not a universal proof and not substituted for K. |
| LLVM concrete harness | Supports actual fixed-semantics execution on boundary/example inputs. | Finite empirical evidence only; exact source prefix is mechanically checked. |
| Supplied opaque float/sort/digest and unused rules | Could affect other programs. | Unreachable and nondependent here; explicitly excluded from this theorem. |

### Excluded behavior

- letters, tabs, other Unicode, invalid/unbalanced parentheses, and unmatched
  closes;
- equivalence of all MPY behaviors to CPython;
- module import side effects beyond the typing-only import;
- total correctness, resource exhaustion, and performance;
- unused float/sort/digest/dict/subscript language fragments.

These exclusions do not remove a material part of this HumanEval contract.

### Gate and benchmark decision

- Gate A (real-program soundness): **PASS**. Exact body and binding are pinned;
  fixed execution is not bridged; task-local equations are sound; result is
  constrained; the fresh false result is rejected.
- Gate B (intent adequacy): **PASS**. The precondition covers the full stated
  parenthesis-and-space domain without a finite-size bound, and the recursive
  spec denotes exactly the requested partition.
- Gate C (trust/evidence auditability): **PASS**. Commands, inputs, source
  artifacts, exact statuses, bounded logs, rule inventory, witnesses, and
  limitations are preserved.

Under the benchmark mapping, this is a sound, result-constraining proof of the
real generated program with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
