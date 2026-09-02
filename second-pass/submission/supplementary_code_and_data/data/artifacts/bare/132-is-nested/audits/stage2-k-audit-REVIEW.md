# Independent adversarial audit: 132-is-nested

## Executive finding

The candidate contains a legitimate, universal partial-correctness proof for
the submitted bracket-only program. Fresh K builds and proofs close, the formal
result is constrained, the proof-side program term is the trusted translation
of `solution.py`, and a fresh false-result mutation is rejected.

The result is marked `CONCERNS / LEGIT`, rather than an unqualified pass,
because the generated semantics is deliberately task-specific in two
non-result-bearing details and the final automaton-to-HumanEval-intent bridge is
a transparent mathematical argument supported by differential testing, not a
separate K theorem against `canonical.py`. These limitations do not narrow the
bracket-string domain, bypass program execution, or permit a false target result.

All candidate and generation artifacts were treated as untrusted and read-only.
All builds and experiments used `/tmp/audit-work/132-is-nested`; preserved
reviewer artifacts and bounded logs are in `/audit-output/evidence`.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` declares:

- problem `132-is-nested`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

The complete check is preserved in
`evidence/01_provenance_check.py` and `evidence/01_provenance.log` (exit 0).
It established:

- `/audit-campaign-lock.json` is a real regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals the `audit_campaign` block.
- Every record required for `legacy-selected-stage1` is present, readable, and
  non-symlinked: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. The present `usage.json` was also
  inspected. The retained legacy records were inspected as well.
- All audit-input per-file hashes match the mounted bytes, including the run,
  task, result, invocation, generation prompt, output, last message, metrics,
  usage, canonical, trusted prompt, and trusted translator.
- Every evidence leaf hash listed by both `generation-result.json` and
  `invocation.json` matches. In particular, the single JSONL trace file is
  `605e6f24...6578e`.
- Independently reproducing the pipeline `sha256_tree` algorithm gives
  `b92da64b...b39eaf` for `/candidate`, equal to both retained workspace
  records, and `1c313c75...14cfe4` for the trace tree, equal to
  `usage.json`'s source-trace digest.
- The launcher-recorded aggregate snapshot digests
  (`6a9f7335...d3c814` for the candidate and
  `005067ca...35ef7ef` for the trace) were read and recorded. Their aggregate
  serialization is not declared in the record, so no guessed directory hash
  was substituted for them; integrity was independently checked through every
  recorded leaf hash plus the reproducible stage tree digests above.
- All 313 structured-trace lines parse as JSON. The whole generation output was
  read for marker counts. Its prior `#Top`, tests, and final report were used
  only as untrusted historical claims.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required by
  `GENERATED_SEMANTICS`. No hidden or inferred reference semantics was used.
- The required proof artifacts are real files. The candidate's crash bundle
  `kore-exec.tar.gz` and Python bytecode cache were inventoried but never used.

There is no infrastructure breach and no missing declared record.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, the input is any
finite string consisting only of `[` and `]`. The result is true exactly when
there are indices `i < j < k < l` whose characters are `[`, `[`, `]`, `]`:
equivalently, `[[]]` is a subsequence. This is the canonical meaning of a valid
subsequence containing a nested pair.

The submitted `solution.py` implements a four-state streaming recognizer:

- state 0: no useful left bracket yet;
- state 1: one left bracket has been seen;
- state 2: two left brackets have been seen;
- state 3: the first subsequent right bracket has been seen;
- a right bracket in state 3 returns true.

Its `else` treats any non-`[` character as `]`, but that is exact on the
prompt's bracket-only domain.

### Trusted regeneration

`evidence/03_regenerate_mpy.sh` ran the trusted mounted translator against the
scratch copy. `evidence/03_regenerate_mpy.log` records exit 0, byte-comparison
exit 0, and identical SHA-256
`422d76458dc1ecd1503304f4ada4deea5a4f1193aaa3f5427cff102efb0fbe0a`.
Thus the submitted `solution.mpy` is exactly the trusted translation of
`solution.py`.

### Independent differential test

`evidence/02_differential.py` independently imports the trusted canonical and
submitted entry points and also uses a separately written fixed-word
subsequence oracle. The run in `evidence/02_differential.log` covered:

- all six documented examples;
- empty input and explicit branch/shortest-result boundaries;
- every one of the 131,071 bracket strings of lengths 0 through 16;
- 2,000 deterministic random strings of lengths 17 through 1,000.

There were 133,071 unique inputs and zero mismatches (exit 0). This is strong
finite fidelity evidence, not a substitute for the K theorem.

## 3. Clean proof reconstruction

Only these source files were copied into scratch: the prompt, translator,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`, plus separate trusted references. No candidate kompiled directory,
cache, or crash bundle was copied.

The live toolchain is K 7.1.293
(`evidence/04_tool_versions.log`). The fresh commands and outcomes were:

1. Concrete definition:

   ```text
   kompile semantic.k --backend llvm --main-module SEMANTIC \
     --syntax-module MPY-SYNTAX \
     --output-definition audit-semantic-kompiled
   ```

   Exit 0; see `evidence/05_build_concrete.log`.

2. Generated-semantics executions:

   `evidence/06_concrete_compare.py` ran 18 normal and boundary cases, including
   empty iteration, both bracket constructors, all automaton boundaries, all
   prompt examples, and early return with an unvisited suffix. Every `krun`
   exited 0 and matched both Python implementations; see
   `evidence/06_concrete_compare.log`.

3. Proof definition:

   ```text
   kompile verification.k --backend haskell --main-module VERIFICATION \
     --syntax-module MPY-SYNTAX \
     --output-definition audit-verification-kompiled
   ```

   Exit 0; see `evidence/07_build_proof.log`.

4. Full candidate specification:

   ```text
   kprove spec.k --definition audit-verification-kompiled \
     --spec-module SPEC
   ```

   It printed `#Top` and exited 0; see `evidence/08_kprove_all.log`.

The claims are cumulative: state 0 may invoke state 1, state 1 may invoke state
2, state 2 may invoke state 3, and the entry claim invokes state 0.
`evidence/claim-subsets.k` and `evidence/09_kprove_claim_subsets.log`
independently reconstruct this dependency order:

- state 3 alone: `#Top`, exit 0;
- states 2 and 3: `#Top`, exit 0;
- states 1, 2, and 3: `#Top`, exit 0;
- states 0, 1, 2, and 3: `#Top`, exit 0.

Together with the full run, every positive claim was freshly exercised and
closed.

## 4. Adequacy and real-program pinning

### Claims in plain language

Each loop claim begins with the actual `iterate("bracket", BS, loopBody)`
computation followed by the function's final `Return(false)`. It fixes the
stored function body, integer state, input local, loop local, and empty result.

- State-0 claim: continuing over `BS` from no matched target character returns
  `scan(0, BS)`.
- State-1 claim: continuing after one useful `[` returns `scan(1, BS)`.
- State-2 claim: continuing after two useful `[` characters returns
  `scan(2, BS)`.
- State-3 claim: continuing after two `[` and one subsequent `]` returns
  `scan(3, BS)`.

All four postconditions set `<result>` to that Boolean and finish the wrapper;
the result is not free. `_ORIG` and `_CUR` are irrelevant locals, not result
oracles: the next loop step overwrites `bracket`, and the final Boolean return
does not read either value.

The entry claim says: for every finite `BString BS`, starting with the submitted
module term, empty function/environment maps, and `noResult`, execution finishes
with `boolVal(scan(0, BS))`.

### Satisfiable preconditions and substitutions

Concrete reachable loop heads are:

- state 0 after prefix `""`, with the dummy current value;
- state 1 after prefix `"["`, current bracket `[`;
- state 2 after prefix `"[["`, current bracket `[`;
- state 3 after prefix `"[[]"`, current bracket `]`.

The entry precondition is realized, for example, by `BS = .BString` and by
`BS = lbr lbr rbr rbr .BString`. `evidence/12_claim_witnesses.py` substitutes
seven suffixes into every loop precondition and eight values into the entry
precondition. All 36 claimed results match both Python implementations; see
`evidence/12_claim_witnesses.log`.

### Mechanical program identity

Program identity has three independent links:

1. trusted regeneration is byte-identical, as shown in stage 2;
2. `evidence/11_constructor_compare.sh` parses the regenerated term and the
   exact constructor term represented in the proof pin through K; their KORE
   bytes are identical with SHA-256
   `2c0d6d3f9fe5c241abc832893a3489c1d4eb8a78db9892db54b27105c1e7d92c`
   (`evidence/11b_constructor_compare.log`);
3. `evidence/pin-check.k` proves that `theSolution` expands to that exact
   constructor tree. K reports a trivial normalized claim, then `#Top`, exit 0
   (`evidence/10c_pin_check.log`).

The external `.mpy` grammar spells an empty statement-list argument as a blank,
while a K definition spells the same unit `.Stmts`. The initial reviewer probes
that exposed those parser representations are retained in
`evidence/10_pin_check.log`, `evidence/10b_pin_check.log`, and
`evidence/11_constructor_compare.log`; they are parser-test failures, not target
proof failures.

The proof-local AST aliases are manually maintained rather than generated from
`solution.mpy`. For this immutable candidate, the mechanical comparison above
pins them exactly; lack of an automatic maintenance step is not a proof defect.

### Body sensitivity

`evidence/verification-body-mutant.k` changes the proof-side program term itself
from `state = 0` to `state = 1`. It is not merely an external source edit. The
mutant definition builds successfully (`evidence/13_build_body_mutant.log`),
but the original constructor pin gets `WarnStuckClaimState` and inner exit 1
(`evidence/14_body_sensitivity.log`). The theorem is sensitive to the body it
executes.

## 5. Rule-by-rule static soundness review

The exhaustive line-level inventory is
`evidence/15_rule_inventory.md`; its mechanical extraction is
`evidence/15_inventory_extract.log`. The only local K files are `semantic.k`,
`verification.k`, and `spec.k`. There are no helper K files, priorities,
`owise` rules, simplification rules, macros, hooks, opaque symbols, or
operational bridges.

### Syntax, configuration, and attributes

`MPY-SYNTAX` declares exactly the used lower AST: two bracket constructors,
inductive bracket strings, module/function/parameter constructors, comparison
lists, six expression forms, statement lists, and five statement forms.
`SEMANTIC` adds the integer/Boolean/string value wrappers, result and stored
function constructors, `start`, `iterate`, and four cells:
`<k>`, `<functions>`, `<env>`, and `<result>`.

The semantic functions `eval`, `add`, `compare`, `getVal`, `choose`, and
`getString` are partial: unsupported or mistyped terms stick visibly. The four
proof-local functions `loopBody`, `solutionBody`, `theSolution`, and `scan` are
declared `[function,total]`. The three nullary AST aliases have one exhaustive
equation each. `scan` is equation-complete for every state the theorem can
reach (0–3).

### All 30 semantic rules

| IDs | Lines | Review |
|---|---:|---|
| S01–S03 | 59–61 | Module exposure and nonempty/empty statement-list sequencing preserve left-to-right execution. |
| S04 | 63–64 | `FuncDef` stores the exact parameter/body pair under its name. |
| S05 | 66–70 | `start` requires the exact `is_nested`/one-string binding, installs the input local, and executes that stored body; it pins binding rather than selecting by name alone. |
| S06–S07 | 79–80 | Name lookup uses the current map and unwraps only an actual `Val`; missing locals stick. |
| S08–S11 | 81–84 | Integer, Boolean, and the two bracket literals map to their exact values. |
| S12–S13 | 85–87 | Pure addition and one-link comparison evaluate their exact operands; every submitted comparison has that form. |
| S14 | 89 | Addition uses K unbounded integers, matching the used Python integer behavior. |
| S15–S16 | 91–92 | Integer equality and less-than are the ordinary operations. |
| S17–S20 | 93–100 | The four one-character bracket-equality cases are exhaustive, disjoint, and truthful. |
| S21–S22 | 103–104 | Boolean `choose` branches are constructor-disjoint and select the correct statement list. |
| S23 | 107–108 | Assignment evaluates its pure RHS in the old environment, then updates the named local. |
| S24 | 110–112 | `If` evaluates the pure guard in the current environment and executes exactly one branch. |
| S25 | 116–118 | `For` evaluates the iterable before loop-body execution and initializes the loop target before `iterate`. The dummy pre-iteration binding is overwritten before every nonempty body execution. |
| S26 | 121 | `getString` unwraps exactly a bracket-string value. |
| S27 | 123 | Empty iteration terminates without executing the body. |
| S28–S29 | 124–129 | Left/right steps bind the corresponding one-character string, execute the body, then continue with the suffix. |
| S30 | 133–136 | `Return` evaluates the pure expression in the current frame, discards the continuation, clears the one-call wrapper maps, and stores the result. This correctly handles the early return inside the loop. |

S25 deliberately binds the loop variable to an empty `BString` before an empty
loop, whereas CPython leaves a previously unbound loop target unbound. This
would distinguish a different program that reads that local after an empty
loop. The submitted program does not: its next operation is literal
`Return(false)`, which neither reads `bracket` nor exposes the local map, and
S30 then removes the frame. Thus no false conclusion witness exists for this
program on any intended input. This is a task-specific reuse limitation, not a
material target unsoundness.

S30 likewise models the complete one-function wrapper rather than a reusable
Python call stack. There are no nested calls, later module observations, output,
exceptions, allocation, or external state in the submitted program. Concrete
early-return and empty-loop tests confirm the material result/control behavior.

### All 12 verification equations

| IDs | Lines | Classification and review |
|---|---:|---|
| V01–V03 | 9–28 | Truthful definitional AST aliases. Mechanical pinning proves exact expansion. They name execution; they do not replace it. |
| V04 | 35 | `scan(_, .BString) = false`: no remaining input can complete the target. |
| V05–V06 | 37–38 | State 0 consumes `[` to state 1 and ignores `]`. |
| V07–V08 | 40–41 | State 1 consumes a second `[` to state 2 and retains its first `[` across `]`. |
| V09–V10 | 43–44 | State 2 ignores extra `[` and consumes the first useful `]` to state 3. |
| V11–V12 | 46–47 | State 3 ignores `[` and returns true on the next `]`; the suffix is then irrelevant. |

These equations terminate on the suffix and are pairwise constructor/state
disjoint. `scan` is a postcondition definition only: no execution rule rewrites
a program operation to `scan`, so there is no circular result-bearing oracle or
operational bridge.

The `[total]` attribute permits an unspecified Boolean for out-of-range,
nonempty calls such as `scan(4, lbr .BString)`, but no equation, program
transition, claim, or postcondition produces such a call. More strongly,
`evidence/verification-scan-nototal.k` removes only that attribute; the
definition rebuilds and the complete proof still prints `#Top` and exits 0
(`evidence/16_build_scan_nototal.log`,
`evidence/17_prove_scan_nototal.log`). Closure does not depend on the
out-of-range totalization.

### Construct coverage and evaluation/control fidelity

Every constructor in regenerated `solution.mpy` maps to the declarations and
rules above: module/function loading (S01–S05), literals and names (S06–S11),
addition/comparison (S12–S20), assignment (S23), branching (S21–S24), iteration
(S25–S29), and return (S30). State changes, lookup, RHS/guard evaluation,
per-character binding, loop continuation, and early-return continuation
discarding are all modeled. No used construct is skipped or replaced with an
unconstrained value.

No local rule was classified as materially unsound, so there is no unsupported
unsoundness allegation lacking the required false-conclusion witness.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is `evidence/spec-vacuity-fresh.k`. It keeps all
four real loop claims but changes the entry result from
`boolVal(scan(0, BS))` to the universally constant `boolVal(false)`.

The mutation is demonstrably false at the satisfying entry state
`BS = lbr lbr rbr rbr .BString` (`"[[]]"`): trusted canonical, submitted
Python, and fresh concrete K execution all return true.

The dry run:

```text
kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-FRESH --dry-run
```

builds successfully and exits 0 (`evidence/18_vacuity_dry_run.log`). The real
mutation run exits 1 inside `kprove`, reports `WarnStuckClaimState`, and exposes
the unmet implication `false = scan(0, BS)` while the reached result is
`boolVal(scan(0, BS))`; see `evidence/19_vacuity_expected_failure.log`.
This is a reachable result-obligation failure, not a parser error, timeout, or
unrelated crash.

## 7. Proven versus assumed accounting

### What is formally proved

Under the freshly built local K definition, for every finite constructor
`BString BS`:

```text
<k> exact-translated-solution ~> start(BS) </k>
<functions> .Map </functions>
<env> .Map </env>
<result> noResult </result>
```

partially correctly reaches a final wrapper state with empty function/local
maps and:

```text
<result> boolVal(scan(0, BS)) </result>
```

The four helper claims formally characterize execution from every reachable
loop automaton state. The proof is unbounded in string length; it is not finite
unrolling or example-only reasoning. It executes assignments, tests,
iteration, and returns under the audited operational rules.

This is partial correctness. The report does not upgrade it to a separate
machine-checked total-correctness theorem, although ordinary finite-list
execution clearly decreases the `BString` suffix.

### Why the postcondition is the intended result

Ordinary mathematical reasoning establishes the intent bridge:
`scan(q, BS)` is the greedy fixed-word subsequence automaton for the remaining
characters of `[[]]`. Its four states record how many target characters have
been retained. For a fixed target word, greedily taking the earliest matching
character succeeds exactly when some matching subsequence exists. Therefore
`scan(0, BS)` is true exactly when `[[]]` is a subsequence.

The trusted canonical also returns true exactly when two increasing opening
indices can be paired with two decreasing closing indices; this is equivalent
to indices `i < j < k < l` spelling `[[]]`. The independent 133,071-input
differential run supports, but does not universally prove, that source bridge.

### Trust ledger

| Boundary | Dependents | Judgment |
|---|---|---|
| K 7.1.293 parser, compiler, reachability calculus, LLVM and Haskell backends | All builds/executions/proofs | Necessary foundational trust; version recorded and both backends reconstructed independently. |
| Installed `domains.md`: K sequencing/list units, unbounded `Int`, `Bool`, `String` tokens, and `Map` lookup/update | Every semantic rule using built-ins | Acceptable low-level mathematical/runtime primitives; no task answer is encoded there. |
| Trusted mounted prompt, canonical, and `py2mpy.py` | Contract, source oracle, source-to-constructor link | Launcher-designated trusted inputs; bytes and hashes verified. |
| CPython and the reviewer differential scripts | Finite fidelity and witness evidence | Empirical only; never substituted for the K proof. |
| Human mathematical interpretation of `scan` and the canonical algorithm | Formal-postcondition-to-HumanEval-intent bridge | Transparent and strongly tested, but not a separate machine-checked equivalence theorem; retained as a non-fatal concern. |
| Dummy empty-loop target and one-call frame cleanup | Intermediate local/wrapper state | Task-specific abstractions proven result-inert for this exact body; unsuitable as general Python semantics, but they cannot affect the target result. |

There are no opaque program-derived symbols, trusted task-answer primitives,
proof-local operational bridges, priority shortcuts, fabricated used
constructs, or empirical values embedded in execution.

### Excluded behavior

The theorem does not cover non-string inputs, characters other than `[` and
`]`, arbitrary Python programs, nested calls, general exception behavior,
module-global observation after return, concurrency, or I/O. None is in the
source contract or submitted program. The bracket-only input domain is complete
and unrestricted in length.

### Gate and benchmark decision

- Gate A (real-program soundness): pass. Exact body, full execution,
  result constraint, satisfying witnesses, body sensitivity, and fresh
  non-vacuity are established.
- Gate B (intent adequacy): pass. The complete bracket-only HumanEval domain is
  covered and the postcondition is the nested-subsequence property.
- Gate C (trust/evidence auditability): pass. All assumptions, commands, inputs,
  exits, mutations, and finite evidence are recorded.

The proof is legitimate. The concerns are non-fatal auditability/reuse
limitations, not a narrowed theorem or an unsound success.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
