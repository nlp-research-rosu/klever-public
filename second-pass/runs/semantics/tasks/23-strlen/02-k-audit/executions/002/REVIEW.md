# Independent adversarial audit: 23-strlen

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied reference semantics. I independently reconstructed
the proof, checked that the theorem executes the byte-identical translated
program, audited the proof-reachable semantics and all candidate-local rules,
and obtained meaningful failures from both a body mutation and a false
postcondition mutation.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The corresponding trusted semantics tree
is present at `/reference/reference-semantics`; there is no rendered-mode
contradiction.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the invocation and metrics records,
`usage.json`, `codex-last.txt`, the complete 6,260-line `codex-output.log`,
`prompt.txt`, and every one of the 149 JSONL trace events. These generation
records claim that the original run succeeded, but I did not use that claim as
proof evidence. The complete-read summary is in
[`01_generation_record_summary.log`](evidence/01_generation_record_summary.log).

The independent provenance checker established all of the following:

- The campaign object in `/audit-input.json` equals
  `/audit-campaign-lock.json`; the lock's actual SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every required record for `legacy-selected-stage1` is a readable regular
  file, not a symlink. Historical `runtime-metrics.json` is absent, which is
  permitted for this layout.
- All individually recorded SHA-256 values for the run/task/result manifests,
  invocation, metrics, usage, prompt, output, last message, canonical program,
  trusted prompt, translator, trace, and legacy auxiliary records match the
  mounted bytes.
- `/candidate` has no symlinked entries.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Candidate `reference-semantics/` and the trusted reference tree contain the
  same 25 relative entries with identical entry types and file bytes. There
  are no missing, additional, mistyped, changed, or symlinked semantics
  entries.

The executable checker and full bounded output are
[`01_provenance_check.py`](evidence/01_provenance_check.py) and
[`01_provenance_check.log`](evidence/01_provenance_check.log). There is no
audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for every input of the annotated type
`str`, `strlen(string)` returns the number of characters in `string`. The
documented examples are `strlen("") == 0` and `strlen("abc") == 3`. The trusted
canonical implementation is `return len(string)`.

Candidate `solution.py` has the required signature and the same implementation:

```python
def strlen(string: str) -> int:
    return len(string)
```

Running the trusted `/reference/py2mpy.py` on candidate `solution.py` produced
a file byte-identical to submitted `solution.mpy`. Both hashes are
`508c92dec7b8810291f0fa18ef567c25d5e8f398d62952cff2bd359697d6aebf`.

The independent differential script compiles the trusted and candidate source
bytes directly, so the untrusted adjacent `.pyc` cannot satisfy an import. It
tested:

- the two documented examples;
- empty and singleton strings;
- NUL, newline, Latin-1, combining-character, emoji, and lone-surrogate cases;
- lengths 255, 256, and 4096; and
- 500 deterministically generated strings of lengths 0 through 128.

All 512 comparisons against the trusted canonical entry point agreed. The
program has no branches, so the empty/nonempty boundary is the only algorithmic
branch boundary. Artifacts and exact commands are
[`02_differential.py`](evidence/02_differential.py) and
[`02_translation_and_differential.log`](evidence/02_translation_and_differential.log).
This testing supports fidelity; it is not substituted for the K theorem.

## 3. Clean proof reconstruction

I copied source artifacts to
`/tmp/audit-work/23-strlen-independent/rebuild`, ignored the candidate
`__pycache__`, and created new output definitions named
`audit-runtime-kompiled` and `audit-verification-kompiled`. No
candidate-provided kompiled definition or K cache existed or was reused.

The independent toolchain is K v7.1.293, matching the campaign lock. The exact
fresh build and run results were:

1. `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled`
   exited 0.
2. `krun solution.mpy --definition audit-runtime-kompiled` exited 0 with an
   empty `<k>` cell, the expected `strlen` closure in module scope, empty heap
   and stack, `NoExc`, and exit code 0.
3. A separately authored constructor program ran `strlen` assertions for
   lengths 0, 1, 3, and 9; it exited 0 with the same clean final state.
4. `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled`
   exited 0.
5. The sole positive target command,
   `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC`,
   exited 0 and printed `#Top`.

Evidence is in
[`03_toolchain.log`](evidence/03_toolchain.log),
[`03_llvm_build.log`](evidence/03_llvm_build.log),
[`03_concrete_runs.log`](evidence/03_concrete_runs.log),
[`03_runtime_checks.mpy`](evidence/03_runtime_checks.mpy),
[`03_haskell_build.log`](evidence/03_haskell_build.log), and
[`03_positive_proof.log`](evidence/03_positive_proof.log).

The LLVM compiler reported non-exhaustive-totality warnings in the supplied
baseline for `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`, plus unused variables in `strLt`. None of those symbols or rules is
reachable from this program or claim. The Haskell proof build reported only
the unused `strLt` variables.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

For every finite K `IntSeq` named `S`, the precondition starts in the standard
empty module configuration with standard builtins, no heap, no stack, no
return or exception, and argument value `str(S)`. The claim loads the module,
calls `strlen`, and requires the final `<k>` result to be exactly `isLen(S)`.
It also requires:

- module scope to contain the exact loaded `strlen` closure;
- the caller environment and scope allocator to be restored;
- heap and heap allocator to remain unchanged;
- an empty stack, `noRet`, `NoExc`, and exit code 0.

There is no side-condition, finite-size bound, example-only restriction, free
result variable, tautological implication, or loop/helper claim. The program
contains no loop.

### Mechanical program identity

There are two independent identity links:

1. Trusted regeneration established
   `solution.py -> solution.mpy` byte identity.
2. I parsed submitted `solution.mpy` and macro expression `strlenModule`
   against the fresh definition with macro expansion and KORE output. The two
   normalized files are byte-identical, both with SHA-256
   `703f28ca1382545a4fee56d79feb9730906b2c17b7fcc173d519243a42094284`.

See
[`04_program_pinning.log`](evidence/04_program_pinning.log),
[`04_submitted_program.kore`](evidence/04_submitted_program.kore), and
[`04_claim_macro_program.kore`](evidence/04_claim_macro_program.kore).
Omission of source annotations is demonstrably typing-only: the trusted
translator emitted exactly the constructor body used by the proof.

The actual execution route is:

```text
#invokeStrlen(str(S))
  -> #loadAll(exact submitted Module)
  -> bind exact strlen closure
  -> resolve and call that closure
  -> bind string = str(S)
  -> execute Return(Call(Name("len"), Name("string")))
  -> resolve standard builtin len
  -> applyBuiltin("len", str(S), .Vals)
  -> seqLen(str(S))
  -> isLen(S)
  -> return/pop while restoring all framed state
```

Every material operation therefore executes under fixed semantics. The
candidate wrapper does not replace the body or its `len` computation with an
oracle.

### Satisfiability, substitution, and body sensitivity

`S = .IntSeq` is a satisfying pre-state witness and requires result 0.
`S = iCons(97, .IntSeq)` is another and requires result 1. A fresh two-claim
ground spec closed with `#Top`; Python canonical and candidate executions also
give 0 for `""` and 1 for `"a"`. The first ground-spec attempt in the preserved
log failed only because my evidence-file `requires` path was relative to the
wrong directory; after changing that reviewer-authored path to an absolute
scratch path, the unchanged claims closed. This was an audit-harness correction,
not a candidate failure. See
[`04_ground_spec.k`](evidence/04_ground_spec.k) and
[`04_ground_proofs.log`](evidence/04_ground_proofs.log).

For body sensitivity, I created a distinct definition whose executed module
body is `return 0`, and changed the final scope expectation to that same
mutated closure while retaining the length result obligation. The definition
built successfully, but the proof exited 1 with `WarnStuckClaimState` and the
unmet equality `0 = isLen(S)`. The concrete witness
`S = iCons(97, .IntSeq)` has actual 0 and demanded 1. This mutation changes the
term executed by the claim, rather than merely changing an external source
file. See
[`04_verification_body_mut.k`](evidence/04_verification_body_mut.k),
[`04_spec_body_mut.k`](evidence/04_spec_body_mut.k), and
[`04_body_sensitivity.log`](evidence/04_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The line-addressed inventory contains every declaration block requested by the
audit: 229 syntax declarations, 697 rules, five contexts, one configuration,
and the one target claim, for 933 records. Attribute counts include 145
`function`, 107 `total`, 35 `concrete`, 26 `owise`, 45 explicit priority rules
(1 at 39, 41 at 40, 3 at 45), four macros, one recursive macro, 22
`no-evaluators` declarations, and no `functional` or simplification rules.

The full declaration text for every record is in
[`05_rule_inventory.tsv`](evidence/05_rule_inventory.tsv), generated by
[`05_rule_inventory.py`](evidence/05_rule_inventory.py). A second exhaustive
ledger attaches a target-reachability and soundness disposition to all 933
records:
[`05_rule_assessment.tsv`](evidence/05_rule_assessment.tsv), generated by
[`05_rule_assessment.py`](evidence/05_rule_assessment.py).

Per source file, the inventory is:

| File | Syntax | Rules | Other | Target role |
|---|---:|---:|---:|---|
| `semantics.k` | 0 | 0 | imports only | assembles supplied modules |
| `semantics/syntax.k` | 16 | 0 | 0 | used constructors and strict return |
| `semantics/core.k` | 37 | 46 | 1 configuration | load, sequencing, lookup, arguments, `isLen` |
| `semantics/functions.k` | 4 | 15 | 0 | closure, parameter, return, pop |
| `semantics/call.k` | 3 | 21 | 0 | callee/argument dispatch and user call |
| `semantics/builtins.k` | 38 | 137 | 0 | exact `len(str)` path |
| `semantics/assert.k` | 0 | 3 | 0 | concrete test only |
| `semantics/bool.k` | 0 | 13 | 1 context | unreachable |
| `semantics/comprehension.k` | 3 | 7 | 0 | unreachable |
| `semantics/concrete.k` | 5 | 16 | 0 | unreachable in proof |
| `semantics/controls.k` | 3 | 34 | 0 | unreachable |
| `semantics/dict.k` | 12 | 28 | 0 | unreachable |
| `semantics/float.k` | 34 | 121 | 0 | unreachable |
| `semantics/int.k` | 1 | 16 | 0 | unreachable; `+Int` is a K builtin, not an `applyBin` rule |
| `semantics/iter.k` | 1 | 0 | 0 | unreachable |
| `semantics/list.k` | 5 | 27 | 0 | unreachable |
| `semantics/methods.k` | 27 | 75 | 0 | unreachable |
| `semantics/operators.k` | 0 | 10 | 2 contexts | unreachable |
| `semantics/range.k` | 2 | 6 | 0 | unreachable |
| `semantics/set.k` | 6 | 12 | 0 | unreachable |
| `semantics/sort.k` | 6 | 19 | 0 | unreachable |
| `semantics/str.k` | 5 | 28 | 0 | input is already `str(S)`; literal rules unreachable |
| `semantics/subscript.k` | 15 | 40 | 2 contexts | unreachable |
| `semantics/tuple.k` | 4 | 21 | 0 | unreachable |
| `verification.k` | 2 | 2 | 0 | exact macro and execution entry |
| `spec.k` | 0 | 0 | 1 claim | target theorem |

The assessment ledger classifies 52 fixed-semantics records as reachable and
valid, 854 supplied-baseline records as syntactically unreachable from this
target, 22 supplied opaque declarations as unreachable, all four
candidate-local records as valid, and the remaining record as the target
claim.

### Used-construct mapping and soundness

`solution.mpy` uses only `Module`, `FuncDef`, `Params`, `Return`, `Call`, and
`Name`; its input is supplied directly as semantic value `str(S)`. Those
constructors map to `syntax.k`, while their behavior maps to the proof-reachable
slice in `core.k`, `functions.k`, `call.k`, and `builtins.k` listed above.

The relevant static checks pass:

- Configuration and cells: the claim pre-state is exactly the standard
  configuration. Module loading writes only the `strlen` closure. Function
  entry allocates one temporary scope and stack frame; return/pop restores the
  environment, removes that frame, resets `scopeLoc`, and preserves heap,
  exception, and exit cells.
- Binding and evaluation: `Call` evaluates the callee before arguments.
  Lexical lookup selects module `strlen`, local parameter `string`, and the
  standard root binding `len`. No `math`/`hashlib` priority interceptor matches,
  and none of the special `sum`/`all`/`any`/`min`/`max` dispatch rules overlaps
  `builtinV("len")`.
- Result computation: fixed rule
  `applyBuiltin("len", OBJ, .Vals) => seqLen(OBJ)` and the sort-disjoint rule
  `seqLen(str(IS)) => isLen(IS)` connect real builtin execution to the summary.
  `isLen` is neither fresh nor opaque: its disjoint, exhaustive equations are
  `isLen(.IntSeq) = 0` and
  `isLen(iCons(_, S)) = 1 +Int isLen(S)`. Recursion strictly descends.
- Control: strictness evaluates the return expression; `Return` records that
  exact value and pops the real call frame. No proof-local return shortcut,
  exception shortcut, allocation, or state fabrication exists.
- Overlap and priority: the applicable name/call/length rules are either
  guard-disjoint or constructor-disjoint. No target-reachable explicit priority
  rule preempts them.

The use of `isLen(S)` in both fixed execution and the postcondition is not a
circular oracle: the fixed builtin rules and exhaustive `isLen` equations
independently determine its value.

### Candidate-local rules

`verification.k` adds exactly two syntax declarations and two rules:

1. `strlenModule` is a compile-time definitional macro. Its RHS is
   mechanically identical to submitted `solution.mpy`.
2. `#invokeStrlen` is a fresh entry symbol.
3. The `strlenModule` macro equation merely names that exact constructor term.
4. The `#invokeStrlen(V)` rule prepends an exact module load and ordinary
   function call while preserving the existing continuation and omitting no
   state cell. It is an execution wrapper, not an operational bridge that
   skips or summarizes a program-defined operation.

There are no proof-local functions, `total`/`functional` declarations, opaque
symbols, priority rules, simplification rules, semantic summaries, helper
claims, or answer-encoding rewrites.

### Supplied opaque and partial facilities

The imported fixed baseline declares the following proof-side symbolic
primitives: `absF`, `addF`, `ceilF`, `decStrToF`, `divF`, `divFloatIntV`,
`divII`, `eqF`, `floatLt`, `floatMod`, `floorFI`, `gtF`, `intFloatDiv`,
`intToF`, `md5hexCodes`, `mulF`, `powF`, `roundF`, `roundFN`, `sortKeyVS`,
`sortVS`, `sqrtF`, `subF`, `toF`, and `truncF`. Twenty-two carry
`no-evaluators`; the other three have concrete-only equations. None can occur
in the target term, affect a branch, result, state, exception, or claim
condition, or contribute to closure.

The non-exhaustive-totality compiler warnings likewise concern unreachable
facilities. I therefore make no unsupported global Python-fidelity claim about
those unused portions of this intentionally partial supplied semantics. The
target proof relies only on the audited exact slice above, and I found no
target-reachable unsound rule requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I created a fresh spec that leaves the program, precondition, final cells, and
module body unchanged but demands `isLen(S) +Int 1` as the returned result.
This is false for the satisfying witness `S = .IntSeq`: actual result 0,
demanded result 1.

The mutation dry-run exited 0, proving that it parsed and built against the
fresh definition. The actual proof exited 1 with `WarnStuckClaimState`; its
residual explicitly reports the failed implication
`isLen(S) +Int 1 = isLen(S)`. This is the expected unmet obligation, not a
parser error, timeout, unrelated crash, or unreachable mutation.

See
[`06_spec_vacuity.k`](evidence/06_spec_vacuity.k) and
[`06_vacuity.log`](evidence/06_vacuity.log).

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied MPY semantics, for every finite `IntSeq S`, execution from
the standard clean state loads the submitted `strlen` function, calls it on
`str(S)`, and reaches a final state whose returned value is exactly the
structural length `isLen(S)`. The theorem also establishes normal control
return, no exception, exit code 0, unchanged heap, empty stack, restored
environment/allocation cells, and the exact expected module binding.

This covers the full HumanEval source-contract domain of Python strings. It is
not a bounded unrolling or finite-size theorem. Modeling strings as finite code
sequences is slightly over-broad because `IntSeq` does not restrict each
integer to a valid Unicode scalar/code point; the extra values do not weaken
the theorem, because length depends only on sequence structure.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293, Haskell/LLVM backends, and K built-in integer/boolean/map/list rewriting | All machine checking and ordinary `+Int` normalization | Standard accepted verification toolchain boundary; version and fresh commands recorded |
| Trusted `/reference/py2mpy.py` | Source-AST to constructor identity | Accepted trusted input; byte regeneration and independent expanded-KORE comparison eliminate candidate substitution |
| Supplied reference semantics for module load, lexical lookup, call frames, return, and `len(str)` | Value, control, and final state of the theorem | Accepted mode-selected baseline; every target-reachable rule was statically audited and concretely exercised |
| Python `str` to finite code-sequence interpretation | Human-facing meaning of `isLen(S)` | Ordinary representation bridge; no domain narrowing, and 512 independent Python differential cases include Unicode/boundary values |
| Twenty-five supplied symbolic float/digest/sort primitives | None | Imported but unreachable; no claim dependency |
| Trusted canonical implementation and differential testing | Empirical source-intent evidence only | Not used as a substitute for K reachability |

There is no empirical bridge or opaque symbol on the result path, and no
informal assumption identifies a program-derived oracle with the postcondition.

### Gate and decision summary

- Gate A (real-program soundness): PASS. Exact program identity, fixed execution,
  state/control fidelity, ground witnesses, body sensitivity, and false-result
  rejection all hold.
- Gate B (intent adequacy): PASS. The theorem covers unrestricted finite
  strings and proves the requested length, with no material source-contract
  narrowing.
- Gate C (trust/evidence auditability): PASS. Commands, outputs, scripts,
  mutations, inventory, and trust boundaries are preserved and reproducible.

The candidate therefore meets the benchmark's `PASS / LEGIT` boundary. The
compiler observations are confined to unused supplied-semantics facilities and
do not create a material adequacy or soundness gap for `strlen`.

VERDICT: PASS
LEGITIMACY: LEGIT
