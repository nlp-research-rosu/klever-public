# Independent adversarial audit: 5-intersperse

The candidate contains a legitimate partial-correctness proof. I did not rely
on the candidate's `#Top`, compiled directories, `PROOF.md`, tests, trace, or
final report. I reconstructed the definitions from copied source, reran the
proof, audited the formal claims and every task-local extension, and created a
new false mutation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `5-intersperse`, and condition
`kit-semantics`. This is consistent with the mounts: the trusted
`/reference/reference-semantics` tree is present.

All required launcher-owned inputs and pipeline-v3 records are regular,
readable files/directories:

- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation/invocation.json`, `metrics.json`, `runtime-metrics.json`,
  `usage.json`, `codex-last.txt`, `codex-output.log`, and `prompt.txt`
- the structured trace under `/generation/codex-trace/`
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`

The independently calculated SHA-256 values for every launcher-recorded file
match `/audit-input.json`. The trace contains one 314-line JSONL file; every
line parses, and its file hash matches the generation result. I streamed and
inspected the complete 16,123-line generation log and the complete structured
trace. Their reports of `VALIDATED`, `#Top`, tests, and mutations were treated
only as untrusted claims.

The protected-input checks pass:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The candidate and trusted `reference-semantics` trees have identical
  relative entries, file types, and bytes (25 entries in each review-local
  manifest). There are no missing, additional, changed, mistyped, or symlinked
  candidate semantics entries.
- No entry anywhere in the candidate tree is a symlink.
- All six required candidate proof artifacts are present as regular files.

Evidence:
`evidence/stage1-integrity.log`,
`evidence/stage1-generation-record-summary.log`,
`evidence/stage1_integrity.py`, and
`evidence/generation_record_summary.py`.

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: given a list of integers and an integer
`delimeter`, return a list with that delimiter inserted exactly once between
each pair of consecutive input elements. Empty input returns `[]`; a singleton
is unchanged.

The trusted canonical implementation handles empty input specially, appends
each element except the last followed by the delimiter, and then appends the
last element (`/reference/canonical.py:15-26`). The candidate instead iterates
over every element, appending the delimiter before an element exactly when the
result is already nonempty (`/candidate/solution.py:5-10`). These are different
algorithms with the same intended result.

Using the trusted translator copied from `/reference/py2mpy.py`, I regenerated
`solution.mpy` in scratch. It is byte-identical to the submitted file; both
have SHA-256
`280eebaf33f134914b4a86291b12cbcbc1a4f1e43338807d881f8de4243d413d`.

The independent differential test imports the copied trusted canonical entry
point and copied generated entry point. It checks:

- both documented examples;
- lengths zero, one, and two, covering the loop and `if result` boundaries;
- zero, negative, repeated, delimiter-equals-element, and unbounded-integer
  cases;
- every list of length 0 through 6 over `(-3,-1,0,1,2,7)` with delimiters
  `(-4,0,3)`, 167,961 exhaustive cases;
- 2,000 seeded cases of lengths 0 through 50 over values and delimiters in
  `[-10^9,10^9]`.

The final run covers 169,969 cases with zero result mismatches and zero input
mutations. Evidence:
`evidence/differential_audit.py`,
`evidence/stage2-translation.log`, and
`evidence/stage4-python-witness.log`.

## 3. Clean proof reconstruction

I copied only source artifacts to
`/tmp/audit-work/intersperse-audit`. No candidate `runtime-kompiled`,
`verification-kompiled`, cache, bytecode, or generated definition was copied
or used. The scratch source manifest is in
`evidence/stage2-scratch-copy.log`.

The live toolchain is K 7.1.293. Fresh reconstruction produced:

1. An LLVM definition from the copied supplied semantics:

   `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled`

   This exited 0. Its warnings concern unused variables and nonexhaustive
   functions in unrelated supplied modules.

2. A concrete driver whose `intersperse` `FunctionDef` AST is identical to
   `solution.py`. `krun` terminated with `.K`, `NoExc`, exit code 0, and these
   heap results:

   - `[]`
   - `[7]`
   - `[7,-2,8]`
   - `[1,4,2,4,3]`
   - `[0,0,0,0,0]`
   - `[-3,-3,-1,-3,2]`

3. A Haskell proof definition from copied `verification.k` and copied supplied
   semantics:

   `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled`

   This exited 0.

4. The candidate's unfiltered target proof:

   `kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC`

   This printed `#Top` and exited 0.

5. `SPEC.loop-invariant` selected alone printed `#Top` and exited 0. A second
   compositional run selected the entry claim while treating that independently
   proved helper as trusted for that run; it also printed `#Top` and exited 0.
   This avoids confusing the entry theorem's expected dependence on its loop
   circularity with an independent axiom.

The relevant bounded logs are
`evidence/stage3-toolchain.log`,
`stage3-kompile-llvm.log`,
`stage3-krun-concrete.log`,
`stage3-kompile-haskell.log`,
`stage3-kprove-all.log`,
`stage3-kprove-loop-invariant.log`, and
`stage3-kprove-entry-with-proved-helper.log`. A diagnostic that removed the
loop claim and consequently unrolled indefinitely is explicitly separated in
`evidence/stage3-focused-entry-note.md`; it is not a target-proof result.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` (`/candidate/spec.k:6`) says: starting at the real
supplied-semantics loop over an arbitrary remaining semantic list, with the
actual two-statement body, integer delimiter, exact local bindings, a
nonempty accumulated result list, and framed unrelated state, the loop
finishes and changes that heap list to
`intersperseAcc(current-result, remaining-input, delimiter)`. It also allows
the loop variable to take its final value.

`SPEC.intersperse-correct` (`/candidate/spec.k:25`) says: from an exact call to
the `intersperse` closure with semantic input list `INPUT` and integer `D`,
empty heap, allocator zero, module environment, empty stack, `noRet`, `NoExc`,
and exit code zero, execution returns `ref(0)`. Heap location zero contains
`list(intersperseAcc(.ValSeq, INPUT, D))`; the allocator becomes one, and the
environment, stack, return, exception, and exit states have their expected
restored values.

### Exact program identity

The claim does not replace the call with a summary. Its `<k>` cell executes a
normal `Call(Name("intersperse"), ...)`; the exact translated closure is fixed
in `<scopes>`. The `INTERSPERSE-BODY` macro
(`/candidate/verification.k:7-14`) expands to exactly the `For` body in the
byte-verified `/candidate/solution.mpy:5-10`, including the empty `else`
branch, delimiter append, and element append. Parameter order, result
initialization, loop target, return, defining scope, and binding name all
match.

I also ran the submitted `solution.mpy` itself under the fresh LLVM
definition. After module loading it produces exactly the module state assumed
by the entry claim: environment 0; builtins scope -1; scope 0 containing the
same `intersperse` closure and parent -1; scope allocator 1; empty heap with
heap allocator 0; empty stack; `noRet`; `NoExc`; exit code 0. See
`evidence/stage4-krun-submitted-solution.log`. Replacing `.K` in this
post-load state with the claim's call is therefore an exact function-entry
configuration, not a substituted program.

The entry precondition is satisfiable. One explicit state uses
`INPUT = [1,2]` and `D = 4` with the cells shown in the claim. Substitution in
the postcondition gives `[1,4,2]`. A reviewer-authored ground K claim for this
state prints `#Top`; both trusted canonical Python and generated Python also
return `[1,4,2]`. See `evidence/ground-witness.k`,
`stage4-ground-kprove.log`, and `stage4-python-witness.log`.

The postcondition is result-constraining: it fixes the returned reference,
the entire result sequence, allocation, stack, return state, exception state,
and exit code. `INPUT` and `D` occur in a total, defined summary; the result is
not a free existential, tautology, or implication.

The formal input domain contains the intended `List[int]`/`int` domain. It is
slightly stronger because input elements may be any MPY `Val`; the delimiter
is still an `Int`. Bare `list(INPUT)` is the supplied semantics' read-only
function-input representation. Because this program neither mutates nor
observes the identity of its input list, that representation has no material
effect on the prompt's return-value contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5-k-inventory.log`, produced by
`evidence/k_inventory.py`, enumerates every declaration, configuration,
context, rule, attribute, and claim with file and line. Across the complete
supplied semantics, `verification.k`, and `spec.k`, it records:

- 229 syntax declarations;
- 699 rules: 238 operational and 461 equational;
- one configuration and five explicit contexts;
- 147 function declarations and 108 `total` declarations;
- 45 priority rules, 35 concrete rules, 26 `owise` rules, and five macros;
- 25 explicit `symbol` declarations, 22 of them marked `no-evaluators`;
- no source-level `functional` declaration and no simplification rule;
- two reachability claims.

Per-source rule counts are:

| Source module | Rules | Syntax | Audit disposition |
|---|---:|---:|---|
| `MPY-ASSERT` | 3 | 0 | fixed, dormant |
| `MPY-BOOL` | 13 | 0 | fixed, dormant |
| `MPY-BUILTINS` | 137 | 38 | fixed; no task builtin call |
| `MPY-CALL` | 21 | 3 | relevant call path reviewed |
| `MPY-COMPREHENSION` | 7 | 3 | fixed, dormant |
| `MPY-CONCRETE` | 16 | 5 | LLVM only; excluded from proof module |
| `MPY-CONTROLS` | 34 | 3 | relevant assignment/if/for path reviewed |
| `MPY-CORE` | 46 | 37 | relevant configuration/evaluation path reviewed |
| `MPY-DICT` | 28 | 12 | fixed, dormant |
| `MPY-FLOAT` | 121 | 34 | fixed opaque/concrete boundary, dormant |
| `MPY-FUNCTIONS` | 15 | 4 | relevant closure/return path reviewed |
| `MPY-INT` | 16 | 1 | fixed; integer values only, no arithmetic |
| `MPY-ITER` | 0 | 1 | relevant iterator protocol |
| `MPY-LIST` | 27 | 5 | relevant list/append path reviewed |
| `MPY-METHODS` | 75 | 27 | generic method equations dormant |
| `MPY-OPERATORS` | 10 | 0 | fixed, dormant |
| `MPY-RANGE` | 6 | 2 | fixed, dormant |
| `MPY-SET` | 12 | 6 | fixed, dormant |
| `MPY-SORT` | 19 | 6 | fixed opaque boundary, dormant |
| `MPY-STR` | 28 | 5 | fixed, dormant |
| `MPY-SUBSCRIPT` | 40 | 15 | fixed, dormant |
| `MPY-SYNTAX` | 0 | 16 | used AST declarations reviewed |
| `MPY-TUPLE` | 21 | 4 | relevant loop-target binding reviewed |
| `VERIFICATION` | 4 | 2 | every task-local extension reviewed below |
| `SPEC` | 0 | 0 | two claims reviewed above |

For every supplied rule in the inventory, the decision is either
`relevant fixed-semantics rule, checked below` or `fixed and dormant for every
configuration admitted by these claims`. No supplied rule contains the task
name or task result. Dormant rules have different head symbols/sorts and
cannot rewrite this program's terms. This includes all float, sort, MD5,
dictionary, subscript, string, set, range, comprehension, assertion, and
operator-specific equations. Some of those fixed modules intentionally expose
partial or opaque behavior outside this task; I do not infer full CPython
faithfulness for them. That is a narrower, irrelevant language-coverage
limitation, not evidence of an unsound task proof.

The 25 supplied symbolic/opaque declarations are `md5hexCodes`;
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`; and `sortVS`, `sortKeyVS`. None is reachable from `solution.mpy`,
appears in either claim, or contributes to closure.

### Used-construct map and fixed-semantics checks

| Submitted construct | Declaration and execution rules | Review |
|---|---|---|
| `Module`, `ImportFrom`, `FuncDef` | `syntax.k:41-61`, `core.k:124-127`, `controls.k:35-44`, `functions.k:14-16` | Module statements sequence in order; the `typing` import is a runtime no-op; the exact closure is bound in scope 0. |
| `Call`, `Name`, arguments | `core.k:130-154,183-191`, `call.k:15-32,69-75` | Callee is looked up before left-to-right argument evaluation; the selected binding is the exact closure; a fresh callee scope/frame is pushed. |
| `Assign(result, [])` | `syntax.k:41`, `list.k:13-15`, `core.k:117-121`, `controls.k:9-18` | Empty list construction allocates heap location 0 and binds `result` to `ref(0)`. |
| `For` over `numbers` | `controls.k:62-74`, `list.k:9-10`, `tuple.k:31-41` | Input is evaluated once; each constructor yields one value; target binding updates `number`; empty rest ends the loop. |
| `If(result)` | `core.k:199-205`, `controls.k:50-54,93-97` | Priority-40 ref dereference occurs before generic truthiness. Empty output is false only in the first iteration; nonempty output is true thereafter. |
| `result.append(...)` | `call.k:15-24,52-67`, `list.k:18-20,52-55` | The bound receiver remains a ref because `append` is mutating. The priority-40 append rule performs the in-place heap update and returns `noneV`; `Expr` discards that value. |
| `Return(result)` | `functions.k:77-90` | Lookup returns `ref(0)`; return discards only the callee continuation, then frame pop restores the caller environment/stack while preserving the escaping heap object and monotonic heap allocator. |

The two relevant priority rules (`If(ref(...))` and list `append`) correctly
preempt their generic value/method routes and have the exact heap guards they
need. Other priority rules do not match this path. All lookups are covered by
the exact local/module maps, all append receivers are valid list heap
references, and every input iterator is a finite `ValSeq`. There is no
exception-producing used construct on the claim domain. Framed scopes and
heap entries in the loop claim are preserved.

### Task-local extensions

1. `INTERSPERSE-BODY` is a syntax macro, not an operational shortcut. Its only
   equation is the exact submitted loop body. The fresh compiled definition
   marks the symbol/rule as `macro`; it does not intercept `Call`, `For`,
   `append`, return, or any configuration cell. See
   `evidence/stage5-compiled-extension-check.log`.

2. `intersperseAcc(ACC, .ValSeq, D) => ACC` is the truthful base case.

3. `intersperseAcc(.ValSeq, vCons(X,REST), D)` starts the output with `X`
   without a leading delimiter and recurses on the strict tail.

4. The nonempty-accumulator/nonempty-input equation appends `D`, then `X`,
   then recurses on the strict tail.

The three summary cases are exhaustive and pairwise disjoint over the
constructors of `ACC` and `REST`. Every recursive case removes one constructor
from `REST`; `valSeqConcat` is the supplied structurally recursive list
concatenation. Thus the `total` declaration is justified. The summary touches
no configuration cell and never occurs at the head of program execution. It
is a definitional post-state summary, not an operational bridge or
program-derived oracle.

The loop claim supplies the connection theorem: after at least one real loop
step, its circularity matches the smaller remaining list and updated nonempty
accumulator. The empty-rest branch executes to the summary base case. It does
not bypass lookup, binding, evaluation, control, mutation, calls, return, or
frame cleanup.

There are no task-local opaque symbols, trusted primitives, concrete rules,
priority rules, simplification rules, or operational bridges. I found no
false task-local equation or semantic rule, so an unsound-rule false-conclusion
witness is not applicable.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation is
`evidence/fresh-false-mutation.k`. Its satisfiable input is `[1,2]` with
delimiter `4`, whose demonstrated real result is `[1,4,2]`; the mutation
instead requires `[2,4,1]`.

`kprove ... --dry-run` parsed and built the mutation successfully and exited
0 (`evidence/stage6-mutation-build.log`). The actual proof run then exited 1
with `WarnStuckClaimState`. Its residual is the fully terminated normal state:
`<k> ref(0) ~> .K`, `NoExc`, exit code 0, and heap location 0 containing
exactly `[1,4,2]`. That state cannot unify with the mutated destination
`[2,4,1]`; the backend reports that it cannot rewrite further. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unreachable mutation. See `evidence/stage6-mutation-proof.log`.

## 7. Proven versus assumed accounting

The successful reachability proof establishes, under the supplied MPY
semantics, that an exact invocation of the submitted `intersperse` closure on
any finite semantic list `INPUT` and integer `D` reaches the stated normal
post-state: returned `ref(0)`, heap value
`intersperseAcc(.ValSeq, INPUT, D)`, allocator 1, restored caller
environment/stack/return state, `NoExc`, and exit code 0. Interpreting the
three exhaustive summary equations gives precisely no delimiter for empty
input, the first element without a leading delimiter, and one delimiter
before every subsequent element.

This is reported as partial correctness, consistent with the required Kit
proof model. It does not claim arbitrary CPython behavior outside the
submitted program and formal domain.

The trust ledger is:

| Boundary | Dependence and assessment |
|---|---|
| K parser/compiler, Haskell prover/backend, LLVM backend, and K's built-in Int/Bool/Map/List/String theories | Foundational tool trust. The positive proof depends on the Haskell path; concrete evidence uses LLVM. Acceptable and explicit. |
| Supplied MPY semantics | The theorem is conditional on this fixed trusted semantics. Integrity was independently established. The used configuration, call, function, control, iterator, list, and heap rules were statically audited and concretely exercised. |
| Trusted `py2mpy.py` | Bridges Python source to the submitted MPY AST. The exact trusted translator regenerates the submitted bytes, so there is no candidate-controlled translation assumption. |
| Natural-language property and trusted canonical Python | The recursive summary directly states the insertion behavior. Differential testing supplies broad finite support for implementation-to-intent alignment; it is not used as a replacement for the universal K proof. |
| Supplied opaque float/sort/MD5 primitives | Present in the fixed language but unreachable and nondependent. No value, control, state, exception, or postcondition in this proof depends on them. |
| `INTERSPERSE-BODY` | Exact compile-time abbreviation, not an assumption. |
| `intersperseAcc` | Fully defined, total mathematical summary connected to real execution by the proved loop claim; not trusted or opaque. |

The candidate's `PROOF.md`, generation trace, prior compiled definitions,
candidate tests, and prior `#Top` contribute no trust to this decision.

All seven audit stages pass. The proof is fresh-reconstructible,
result-constraining, non-vacuous, uses the fixed supplied semantics, and pins
the real translated function without a task-answer rule or execution bypass.

VERDICT: PASS
LEGITIMACY: LEGIT
