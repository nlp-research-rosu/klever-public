# Independent adversarial audit: 122-add-elements

This audit was performed from trusted mounts and fresh scratch builds. Candidate
reports, compiled definitions, logs, traces, `PROOF.md`, and prior `#Top`
outputs were treated only as untrusted claims.

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares:

- `record_layout = pipeline-v3`
- `problem_id = 122-add-elements`
- `condition = kit-semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`

The supplied-semantics mount required by that mode is present at
`/reference/reference-semantics`. There is no rendered-mode contradiction.

All required pipeline-v3 records are present, readable, regular files, and not
symlinks:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL file below `/generation-evidence/codex-trace/`

The independently computed SHA-256 values of all launcher-recorded individual
files match `/audit-input.json` and `/generation-result.json`. In particular,
the campaign lock hash is
`053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`,
and the parsed campaign block in `/audit-input.json` is equal to
`/audit-campaign-lock.json`.

The structured trace contains one file and 512 valid JSONL records with zero
malformed lines. The 2,016,885-character generation output, trace, metrics,
usage, invocation, prompt, and final report were inspected only as provenance,
not accepted as proof evidence. The bounded record summary enumerates all 47
generation-time shell calls.

Candidate mount checks:

- `prompt.py` is byte-identical to `/reference/prompt.py`.
- `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- All required candidate proof artifacts are regular files.
- The candidate tree contains no symlinks.
- A fresh deterministic typed-tree digest of the mounted candidate was
  `d6fe7806b1243b798b02b1c8435d837ebeb2c0d38f8be99665490b46da2f0389`.

The supplied semantics integrity check compared relative entry names, entry
types, and file bytes recursively. Both trees contain the same 25 entries,
their independently computed typed-tree digests are both
`5e76fed0f65155942b148f0dba24b583b8d01cec4884747c05083692c74848fb`,
and neither tree contains a symlink. There are no missing, additional, changed,
or mistyped candidate semantics entries.

Evidence:

- `/audit-output/evidence/audit_provenance.py`
- `/audit-output/evidence/stage1-provenance.log`
- `/audit-output/evidence/summarize_generation_records.py`
- `/audit-output/evidence/stage1-generation-record-summary.log`
- `/audit-output/evidence/toolchain-versions.log`

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

### Contract

The docstring requires a non-empty integer array with
`1 <= len(arr) <= 100` and `1 <= k <= len(arr)`. The result is the sum of
values having at most two decimal digits among the first `k` positions.

The candidate implements a single pass with a `remaining` counter. It adds an
element exactly when `-99 <= element <= 99` and breaks after the first `k`
positions. Treating `-` as a sign rather than a digit is a direct, defensible
reading of “digits.”

The trusted canonical uses `len(str(elem)) <= 2`. It consequently excludes
negative two-digit values. For example:

```text
arr = [-99], k = 1
candidate = -99
docstring reading = -99
canonical = 0
```

This canonical divergence is not a candidate defect under the campaign's
docstring-first rule. The documented example is not contradictory and all
three implementations return `24` for it.

### Translation identity

In scratch, the trusted translator was run as:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

It exited 0. `cmp -s` exited 0, and both submitted and regenerated files have
SHA-256
`d66ee2ebfcbb593829d8d9aac35c45002b6e9476b2f82cce15a6d7d732548c82`.

### Independent differential

The reviewer-authored test imports `/reference/canonical.py` and the scratch
copy of the candidate entry point. Its independent docstring oracle sums
values whose magnitudes are at most 99.

Scope:

- the documented example;
- empty and invalid-`k` observations, explicitly kept outside the formal
  contract;
- element boundaries `-100`, `-99`, `99`, and `100`;
- `k = 1`, `k = len(arr)`, and early-stop behavior;
- minimum and maximum permitted lengths;
- arbitrary-size Python integers;
- exhaustive products of 11 boundary values for lengths 1 through 4 and every
  valid `k`;
- 2,000 seeded generated cases with lengths 1 through 100.

Result:

```text
domain_cases=64821
candidate_docstring_mismatches=0
canonical_docstring_mismatches=24715
candidate_canonical_mismatches=24715
```

Every candidate/canonical mismatch is explained by negative two-digit values,
not by a violation of docstring-determined behavior. Outside-contract behavior
was recorded but was not used to narrow or reject the theorem.

Evidence:

- `/audit-output/evidence/stage2_translate.sh`
- `/audit-output/evidence/stage2-translation.log`
- `/audit-output/evidence/independent_differential.py`
- `/audit-output/evidence/stage2-differential.log`

## 3. Clean proof reconstruction

Status: PASS.

Only source files were copied to `/tmp/audit-work/122-add-elements`. All
candidate-provided `*-kompiled` directories, caches, and binaries were ignored.
The trusted reference semantics, not a candidate compiled definition, was
used.

The installed tools independently report K v7.1.293.

### Fresh proof definitions

The bridge-free definition was built with:

```text
kompile verification-base.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-audit-kompiled
```

Exit: 0.

The bridge-bearing definition was built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit: 0.

The only compiler diagnostics were supplied-semantics unused-variable warnings
and unused bridge variables. They do not change rule meaning.

### Fresh positive claims

Every submitted positive proof artifact was rerun:

| Claim | Definition | Result |
|---|---|---|
| `LOOP-SPEC.loop-connection` | bridge-free | `#Top`, exit 0 |
| `SPEC.add-elements` | bridge-bearing | `#Top`, exit 0 |
| `LOOP-WITNESS-BASE.boundary-witness` | bridge-free | `#Top`, exit 0 |
| `LOOP-WITNESS-EXTENDED.boundary-witness` | bridge-bearing | `#Top`, exit 0 |

The two witness claims both start from total 5, sequence
`[99, -100, 7]`, and remaining count 2, and both constrain the result to 104
with the same modeled final state.

### Fresh concrete definition

The LLVM concrete definition was rebuilt from the trusted semantics with
`MPY-KRUN`/`MPY-SYNTAX`. A reviewer-authored translated program executed the
documented example and all four filter boundaries. `krun` exited 0 with:

```text
documented       |-> 24
lower_excluded   |-> 0
lower_included   |-> -99
upper_included   |-> 99
upper_excluded   |-> 0
prefix_stop      |-> 5
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

Evidence:

- `/audit-output/evidence/stage3-kompile-base.log`
- `/audit-output/evidence/stage3-kompile-verification.log`
- `/audit-output/evidence/stage3-kprove-loop.log`
- `/audit-output/evidence/stage3-kprove-entry.log`
- `/audit-output/evidence/stage3-kprove-witness-base.log`
- `/audit-output/evidence/stage3-kprove-witness-extended.log`
- `/audit-output/evidence/stage3_concrete.sh`
- `/audit-output/evidence/stage3-concrete.log`

## 4. Adequacy and real-program pinning

Status: PASS.

### Entry theorem in plain language

`SPEC.add-elements` assumes:

- `INPUT` is a finite `ValSeq` whose every member has K sort `Int`;
- `1 <= vsLen(INPUT) <= 100`;
- `1 <= K <= vsLen(INPUT)`;
- the ordinary initial module configuration has an empty heap and stack,
  normal return/exception/exit cells, and the standard builtins scope.

It loads one function named `add_elements`, calls that binding with
`list(INPUT)` and `K`, and requires the final `<k>` value to be
`qualifyingPrefix(INPUT, K)`. The final global function closure is constrained
to the same parameters and body, the call frame is gone, the caller
environment is restored, the heap remains empty, and normal control state is
required.

`qualifyingPrefix` is a structural definition: for positive `N` and a
non-empty sequence it adds the head exactly when the represented integer lies
in `[-99,99]`, then recurses on the tail and `N-1`; nonpositive `N` or an
exhausted sequence contributes zero.

### Mechanical source-to-claim identity

K's parser was used to emit JSON for the regenerated `solution.mpy` and for
the dry-run entry claim. The exact `Module(FuncDef(...))` under the claim's
`#loadAll` is constructor-identical to the parsed submitted module:

```text
solution_module_hash=6b70c5b248b3cf1306fa1169e58f0bd39b9cf4fc69a79dafcec188d51cdbbaef
claim_loaded_module_hash=6b70c5b248b3cf1306fa1169e58f0bd39b9cf4fc69a79dafcec188d51cdbbaef
module_constructor_identity=True
```

The one claim-side closure also has exactly the source parameters and body.
This establishes pinning after trusted regeneration; it is not merely a
textual resemblance or an external-source assertion.

Evidence:

- `/audit-output/evidence/compare_program_term.py`
- `/audit-output/evidence/stage4-kast-solution.log`
- `/audit-output/evidence/stage4-dry-run-spec.log`
- `/audit-output/evidence/stage4-program-pinning.log`

### Loop connection and context containment

The only operational bridge matches:

- the exact translated `#loop(list(VS), Name("element"), BODY)`;
- the exact singleton `Return(Name("total")) .Stmts`;
- `#endcall`;
- environment 1 and the exact five-entry local map;
- the exact module and builtin scopes;
- scope location 2;
- exactly one stack frame with continuation `.K`, caller environment 0, and
  saved location 1;
- normal return, exception, and exit cells;
- no additional `<k>` continuation.

Its guard is `allInts(VS) and 0 <= N and N <= vsLen(VS)`. It returns
`S + qualifyingPrefix(VS,N)`, deletes the callee scope, restores the caller,
and preserves heap and heap location.

`LOOP-SPEC.loop-connection` has the same program-visible cells, body, guards,
result, and state transition. It imports only `VERIFICATION-BASE`, so it
cannot use the operational bridge it justifies. Its fresh bridge-free proof
closed.

At compiled level, the bridge and candidate claim have identical logical side
conditions and all ten program-visible configuration cells. K automatically
adds an eleventh `generatedCounter` bookkeeping cell. Because the candidate
claim omits it, claim completion allows an existential final counter, while
the compiled operational rule frames the cell unchanged. This is the only
compiled structural difference, and the candidate report's statement of
literal full-cell identity was therefore slightly imprecise.

The difference is not a soundness gap:

- the bridge preserves the counter rather than inventing a value;
- none of the executed loop/call rules performs a freshness operation;
- the match has no following continuation that could observe later
  allocation;
- a reviewer-strengthened, bridge-free universal claim explicitly requiring
  `<generatedCounter> COUNTER </generatedCounter>` preservation also returned
  `#Top`, exit 0.

Thus the complete compiled state effect of the bridge is independently
connected to fixed execution.

Evidence:

- `/audit-output/evidence/compare_loop_bridge.py`
- `/audit-output/evidence/stage4-bridge-claim-comparison.log`
- `/audit-output/evidence/audit-loop-spec-full-state.k`
- `/audit-output/evidence/stage4-full-state-connection.log`

### Satisfiability and concrete substitution

A satisfying entry state is:

```text
INPUT = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
K = 4
```

It satisfies every entry conjunct. `qualifyingPrefix(INPUT,4)` reduces to 24;
the candidate Python implementation, canonical helper witness, fresh concrete
K execution, and reviewer local K evaluation all produce 24.

### Body sensitivity

The reviewer-authored sensitivity claim changes the executed loop body's
upper comparison from 99 to 98 while retaining the original summary. This
changes the K term inside `#loop`; it does not merely edit an unused external
source file.

The artifact parsed and executed, then failed with exit 1 and
`WarnStuckClaimState`. Its residual exposes the reachable 99 boundary where
the changed body excludes a value the summary includes. This independently
demonstrates dependence on the actual body.

Evidence:

- `/audit-output/evidence/audit-loop-body-mutation.k`
- `/audit-output/evidence/stage4-body-sensitivity.log`

## 5. Rule-by-rule static soundness review

Status: PASS.

### Exhaustive inventory

The exact line-by-line inventory is
`/audit-output/evidence/stage5-rule-inventory.log`. It includes every
`requires`, module/import, syntax line, configuration, context, rule, claim,
and end-module line in the trusted supplied semantics and local proof files.

The fixed supplied tree contains 244 syntax-declaration lines, 764 rule
starts, and five contexts:

| File | Syntax | Rules | Contexts | Relevance |
|---|---:|---:|---:|---|
| `semantics.k` | 0 | 0 | 0 | module aggregation |
| `assert.k` | 0 | 3 | 0 | unused |
| `bool.k` | 0 | 16 | 1 | used for `BoolOp("and",...)` |
| `builtins.k` | 40 | 154 | 0 | no candidate builtin call |
| `call.k` | 3 | 21 | 0 | used for call routing and closure entry |
| `comprehension.k` | 3 | 7 | 0 | unused |
| `concrete.k` | 6 | 26 | 0 | LLVM testing only; absent from proofs |
| `controls.k` | 3 | 34 | 0 | assignment, `if`, `for`, and `break` |
| `core.k` | 41 | 51 | 0 | configuration, sequencing, lookup, values |
| `dict.k` | 12 | 28 | 0 | unused |
| `float.k` | 43 | 146 | 0 | unused; inputs are K integers |
| `functions.k` | 4 | 15 | 0 | function binding, return, frame pop |
| `int.k` | 1 | 19 | 0 | unary minus, integer comparison/arithmetic |
| `iter.k` | 1 | 0 | 0 | iterator protocol declarations |
| `list.k` | 5 | 27 | 0 | list iteration |
| `methods.k` | 27 | 75 | 0 | unused |
| `operators.k` | 0 | 10 | 2 | evaluation and dispatch |
| `range.k` | 2 | 6 | 0 | unused |
| `set.k` | 6 | 12 | 0 | unused |
| `sort.k` | 7 | 25 | 0 | unused |
| `str.k` | 5 | 28 | 0 | no source string operation |
| `subscript.k` | 15 | 40 | 2 | unused by final implementation |
| `syntax.k` | 16 | 0 | 0 | all source constructor declarations |
| `tuple.k` | 4 | 21 | 0 | unused |

Every fixed rule is part of the selected supplied model. Rules in unused
modules are constructor-, operator-, or sort-disjoint from this program and
cannot contribute to either positive claim. The task-smuggling search found
no `add_elements` or task-summary symbol in the supplied tree. Supplied opaque
float, sorting, and MD5 symbols are unreachable from the submitted term.

The used fixed-semantics path is:

| Source construct | Declaration and operational rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and sequence rules |
| `FuncDef`, parameter binding | `functions.k` function-binding and `#bindP` rules |
| `Call(Name(...), ...)` | `call.k` callee/argument routing and closure-call rule; `core.k` left-to-right argument evaluation |
| literals and names | `core.k` literal and lexical lookup rules |
| `Assign`, `AugAssign` | `controls.k`; integer `applyBin` in `int.k` |
| `For` over a list | `controls.k` `For/#loop/#loopStep`; `list.k` `#iterNext` |
| `If`, `Break` | `controls.k` truth branch and loop-control rules |
| `Compare` | `operators.k` left/right contexts and dispatch; `int.k` comparison equations |
| unary `-` | `operators.k` and `int.k` |
| `BoolOp("and",...)` | `bool.k` left-to-right short-circuit rules |
| `Return` and normal call end | `functions.k` return, `#endcall`, and `#pop` |

This path preserves evaluation order, binding, loop control, caller
restoration, scopes, heap, stack, return/exception state, and exit code.

### Candidate-local rule inventory

`verification-base.k` adds six syntax declarations and exactly 16 rules;
`verification.k` adds exactly one ordinary operational rule.

| Local extension | Rules | Classification and decision |
|---|---:|---|
| `allInts` | 2 | Definitional. Empty/cons cases are exhaustive and structurally descending. |
| `definedProjectInt` | 1 | Definitional alias for the generated sort predicate. |
| cast `#Ceil` characterization | 1 | Derived sort lemma: a `Val -> Int` projection is defined exactly on represented `Int` values. |
| `projectIntTotal` guarded projection/orientation/collapse | 4 | Totalized projection. On `isInt`, it is the same integer; off-domain output is unconstrained but never value-bearing in these claims. |
| guarded `applyCmp` twin | 1 | Derived dispatch lemma. Guarded by `isInt(V)` and the six supported equality/ordering operators; agrees with `int.k`. |
| guarded integer `applyBin("+",...)` twin | 1 | Derived dispatch lemma. Guarded by `isInt(V)`; agrees with integer addition. |
| `qualifyingValue` | 1 | Total mathematical definition of the inclusive `[-99,99]` filter. |
| `qualifyingVal` | 2 | Disjoint and exhaustive `isInt`/`not isInt` cases. Only the integer case is reachable under `allInts`. |
| `qualifyingPrefix` | 3 | Disjoint and exhaustive over `N <= 0`, empty positive input, and nonempty positive input; recursive descent consumes a constructor. |
| exact loop summary | 1 | Operational bridge, justified by the bridge-free universal connection and strengthened full-state connection described in Stage 4. |

`projectIntTotal` is the only candidate-local opaque symbol. It is not an
oracle for program output: all operational and postcondition uses are guarded
by integer membership, and its equations fix the value on that domain. Fresh
ground checks returned 99 and -100 for the corresponding represented
integers; an opposite claim `projectIntTotal(99) => 98` parsed and failed with
exit 1 and a stuck residual containing 99.

The summary definitions also freshly reduced the boundary prefix and
documented example to 99 and 24. Their finite ground checks support the static
equation review; the universal loop connection, not those checks, is what
connects program execution to the summary.

The bridge priority 30 makes it preempt one-step unfolding only on its exact
connected configuration. Its match does not admit a broader continuation,
stack, local-map shape, or guard. No candidate-local rule encodes a call-level
answer, fabricates an unmodeled operation, or permits a false conclusion on
the intended domain.

Evidence:

- `/audit-output/evidence/stage5-rule-inventory.log`
- `/audit-output/evidence/stage5-inventory-counts.log`
- `/audit-output/evidence/stage5-opaque-priority-search.log`
- `/audit-output/evidence/stage5-task-smuggling-search.log`
- `/audit-output/evidence/audit-local-lemmas.k`
- `/audit-output/evidence/stage5-local-lemmas.log`
- `/audit-output/evidence/audit-projection-opposite.k`
- `/audit-output/evidence/stage5-projection-opposite.log`

No unsound rule was found, so there is no unsupported unsoundness allegation
requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

Status: PASS.

The candidate's submitted `spec-vacuity.k` was not relied upon. The
reviewer-authored mutation preserves the actual loaded function, entry
precondition, and final state, but changes the result obligation to:

```text
qualifyingPrefix(INPUT, K) +Int 1
```

The concrete satisfying witness `INPUT = [1]`, `K = 1` returns 1, so the
mutated target requires the false result 2.

Command:

```text
kprove audit-spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
```

The mutation parsed and executed. It exited 1 with `WarnStuckClaimState`; the
residual specifically rejects:

```text
qualifyingPrefix(INPUT, K) +Int 1
#Equals
qualifyingPrefix(INPUT, K)
```

This was an expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated backend failure.

Evidence:

- `/audit-output/evidence/audit-spec-vacuity.k`
- `/audit-output/evidence/stage6-false-postcondition.log`

## 7. Proven versus assumed accounting

Status: PASS.

### What is machine-checked

Under the supplied MPY semantics, for every finite represented integer list
`INPUT` with length 1 through 100 and every represented integer `K` with
`1 <= K <= len(INPUT)`, if the submitted function call terminates normally,
its returned integer is exactly the sum of values in the first `K` positions
whose magnitudes are at most 99. The module binding and function body are the
trusted translation of the submitted Python source, and the claimed normal
final control/state is reached.

The theorem is symbolic in the complete input sequence and `K`; it is not a
finite-size unrolling or collection of examples.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Supplied read-only MPY semantics | Entire modeled execution | Required fixed model; candidate copy is byte/type identical. Used rules were statically mapped and concretely checked. |
| K compiler, Haskell prover, LLVM backend, SMT/integer hooks | Parsing, rewriting, proof closure, arithmetic | Standard toolchain trust boundary, version recorded. |
| Trusted `py2mpy.py` | Python-to-constructor bridge | Candidate translator is identical; regenerated output is byte-identical; parsed module is constructor-identical to the claim. |
| `projectIntTotal` | Symbolic integer comparison and addition | Candidate-local totalized cast; exact under `isInt`; off-domain value cannot affect either claim; opposite interpretation rejected. |
| `qualifyingPrefix` family | Formal postcondition and invariant summary | Fully defined structural mathematics; universal bridge-free loop theorem connects it to execution. |
| Operational loop bridge | Skips loop, return, and frame-pop execution in the entry proof | Exact program/context rule; candidate bridge-free theorem closes; reviewer-strengthened full-state theorem also closes. |
| K `generatedCounter` cell | Internal freshness bookkeeping | Candidate claim omitted explicit preservation, but the bridge frames it and the region uses no freshness. Explicit preservation was independently proved universally. |
| Negative-number reading of “digits” | Human-facing result meaning | Defensible docstring-first interpretation; canonical divergence is documented, not treated as a proof oracle. |
| Differential and concrete tests | Finite implementation/model evidence | Support only tested cases; not used as a substitute for either universal K claim. |
| Termination | Liveness | Not separately claimed. This audit and the candidate report correctly characterize the result as partial correctness. |

There is no documented or discovered supplied-model representation gap on the
material contract domain: K integers are unbounded, list length and `k` are
symbolic under the exact prompt bounds, and all source constructs used by the
submitted program are modeled.

### Gate and benchmark decision

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS.
- Gate C, trust and evidence auditability: PASS.

The proof reconstructs, constrains the result, executes the real translated
program up to an independently connected exact loop summary, covers the full
docstring domain, and rejects fresh false body and result mutations. The
automatically generated counter-cell omission in the candidate's prose was
independently checked and does not leave a material soundness or adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
