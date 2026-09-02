# Independent adversarial review: 71-triangle-area

The candidate contains a cleanly reconstructable, body-sensitive, non-vacuous
K proof about its exact generated program **for integer arguments**. It does not
prove the HumanEval source contract over ordinary non-integral side lengths.
That is a material source-domain restriction, so the benchmark's explicit
decision rule makes the candidate not legitimate despite the sound restricted
theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout:
legacy-selected-stage1`, `semantics_mode: SUPPLIED_SEMANTICS`, problem
`71-triangle-area`, and condition `semantics`. I used only the launcher
`container_paths`, not the host provenance paths.

The infrastructure is intact:

- `/audit-campaign-lock.json` is a regular non-symlink file, has the recorded
  SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals `/audit-input.json`'s `audit_campaign`
  block.
- All records required for `legacy-selected-stage1` were present, readable, and
  non-symlinked: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` was present and
  inspected. Historical `runtime-metrics.json` is not required for this layout.
- Every launcher-recorded regular-file hash checked independently matched,
  including the run/task/result manifests, invocation, metrics, usage, prompt,
  final text, output log, trusted canonical, prompt, translator, and campaign
  lock. The sole trace JSONL file has SHA-256
  `1dfea5cd723ad155213ee00858d693138f8d866c9474f6cb3563d4617ffed92f`,
  matching the generation result's per-file record.
- The 114 structured trace events were inventoried, including every message,
  tool call, patch, output, and status category. Generation evidence was treated
  only as an untrusted record of what the generator claimed.
- `/reference/reference-semantics` is present as required by supplied-semantics
  mode. Recursive content comparison and a separate path/type/symlink-target
  comparison against `/candidate/reference-semantics` both exited 0. There are
  no missing, additional, changed, mistyped, or symlinked entries.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts. No symlink exists below `/candidate`, `/reference`, or
  `/generation-evidence`.

Evidence:
`evidence/01-provenance/check_provenance.py`,
`check_provenance.log`, `check_semantics.sh`, `check_semantics.log`,
`candidate_manifest.log`, `trace_inventory.py`, `trace_inventory.log`, and
`generation-output-key-lines.log`.

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: given three side lengths, return `-1` if any
pair sums to no more than the third side; otherwise compute Heron's formula and
return the area rounded to two decimal places. The signature has no integer
type annotation or textual integer-only restriction.

`solution.py` implements the same control test and the same left-associated
Heron expression as `/reference/canonical.py`; it merely eliminates the
canonical's intermediate `area` assignments. Regeneration with the trusted
translator produced SHA-256
`fe6ca27695274d5365f24048106704555a9b9b8c3ea5456929cee3bb7044f26c`
for both submitted and regenerated `solution.mpy`; `cmp` exited 0.

The independent differential runner compared observable values, types, and
exception classes/messages over:

- both documented examples;
- equality and invalidity at each of the three branch boundaries;
- just-valid floating-point values at each branch boundary;
- zero, negative, mixed-sign, Boolean, large-integer, and arity cases;
- representative integer, floating, isosceles, scalene, and equilateral cases;
- 500 deterministic generated integer triples and 500 deterministic generated
  floating triples.

All 1,023 comparisons matched. This is finite fidelity evidence, not a
universal proof.

Evidence: `evidence/02-fidelity/translation.log`,
`differential.py`, `differential-inputs.json`, and `differential.log`.

## 3. Clean proof reconstruction

I copied only candidate source artifacts to
`/tmp/audit-work/candidate-clean`, excluded the candidate `__pycache__`, and
used no candidate-built definition or cache. K, `krun`, and `kprove` were all
version 7.1.293.

Fresh commands and outcomes:

| Command | Exit | Relevant result |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 | Fresh concrete definition |
| `krun smoke.mpy --definition audit-runtime-kompiled` | 0 | Empty final `<k>` cell, exit code 0 |
| `kompile verification.k --backend haskell --main-module TRIANGLE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 | Fresh proof definition |
| `kprove spec.k --definition audit-verification-kompiled --spec-module TRIANGLE-SPEC` | 0 | `#Top` |

I also copied each of the five positive claims into a separate reviewer module
and ran it independently. `AUDIT-LOAD-SPEC`,
`AUDIT-INVALID-FIRST-SPEC`, `AUDIT-INVALID-SECOND-SPEC`,
`AUDIT-INVALID-THIRD-SPEC`, and `AUDIT-VALID-SPEC` each exited 0 and printed
`#Top`. Compiler warnings concern fixed-semantics non-exhaustive helpers in the
LLVM build and unused variables in `str.k`; none is a failed target claim.

Evidence: all files under `evidence/03-reconstruction/`, especially
`kompile-runtime.log`, `krun-smoke.log`, `kompile-proof.log`,
`kprove-aggregate.log`, the five `kprove-audit-*.log` files, and
`spec-individual.k`.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. Loading `triangleAreaModule` in an empty module scope binds
   `triangle_area` to `triangleAreaClosure`.
2. For integer `A,B,C`, if `A+B <= C`, calling that closure returns `-1`.
3. If the first comparison is false and `A+C <= B`, it returns `-1`.
4. If the first two comparisons are false and `B+C <= A`, it returns `-1`.
5. If all three sums are strictly greater, it returns `expectedArea(A,B,C)`.

The four call guards are satisfiable and partition all K integer triples. Ground
witnesses are respectively `(1,1,3)`, `(1,3,1)`, `(3,1,1)`, and `(3,4,5)`.
Both Python implementations return `-1`, `-1`, `-1`, and `6.0`; the fresh LLVM
witness program accepts all four assertions.

### Exact program identity

A reviewer script inserted the regenerated `solution.mpy` module term into a
fresh load claim, changing only the translator's omitted empty-else list item to
its explicit constructor unit `.Stmts`. This generated claim requires that
loading the exact submitted constructor term bind the same closure/body used by
the call claims. It exited 0 with `#Top`. This mechanically checks function
name, parameters, constructor body, and definition environment; it is stronger
than relying on the handwritten `triangleAreaModule` comment.

Changing the actual executed `triangleAreaBody` constructor from `return -1` to
`return -2`, recompiling, and rerunning the original spec caused an expected
exit 1. The stuck state contains `<k> -2 ~> .K </k>` against the original `-1`
postcondition. Thus the theorem is sensitive to the body actually executed, not
merely to an external `solution.py`.

Evidence: `evidence/04-adequacy/make_pinning_spec.py`, `pinning-spec.k`,
`kprove-pinning.log`, `mutate_executed_body.py`,
`body-mutation-kompile.log`, `body-mutation-kprove.log`, `witnesses.py`,
`witnesses.mpy`, and `concrete-witnesses.log`.

### Material adequacy failure

Every formal entry claim binds `A:Int, B:Int, C:Int` and uses `+Int`/`<=Int`.
No claim covers K `Float` arguments or mixed numeric arguments. This is not a
harmless proof encoding: the prompt speaks of unannotated side lengths, which
ordinarily include non-integral lengths, and neither the canonical nor candidate
Python implementation restricts inputs to integers. The supplied semantics also
has concrete float arithmetic and comparison paths.

The satisfying source-contract witness `(5.5, 6.25, 7.75)` returns `17.03` in
trusted canonical Python, candidate Python, and the fresh LLVM assertion run,
but it cannot satisfy any formal claim because its arguments are `Float`, not
`Int`. Therefore the candidate materially narrows the real program's
source-contract domain.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory covers 26 K files and 943 entries:

- fixed supplied semantics: 695 rules, 227 syntax declarations, 5 contexts, and
  1 configuration;
- candidate-local artifacts: 5 syntax declarations, 5 function rules, and 5
  claims;
- attributes across the inventory include 151 `function`, 107 `total`, 22
  `no-evaluators`, 35 `concrete`, 45 `priority`, 26 `owise`, 25 `symbol`, and
  no `simplification` or `functional` entry.

Every entry, source location, attributes, source text, scope, and decision is in
`evidence/05-static/rule-inventory.tsv`. The fixed tree is the immutable
supplied baseline selected by this benchmark. The used execution path was
separately mapped through module loading, statement sequencing, closure
binding, frame allocation/pop, lookup, assignment, left-to-right call and
operand evaluation, integer arithmetic/comparison, short-circuit `or`, `If`,
return, float promotion/arithmetic, exponentiation, and rounding in
`evidence/05-static/used-rule-map.md`.

Candidate `verification.k` adds no priority, simplification, `total`,
`functional`, opaque, or operational bridge rule:

- `triangleAreaBody`, `triangleAreaClosure`, and `triangleAreaModule` are exact
  constructor aliases.
- `semiPerimeter` and `expectedArea` are terminating definitional summaries.
  Fully expanded, they are exactly the `divII`, `intToF`, `subF`, `mulF`,
  `powF`, and `roundFN` term produced by executing the real body.

These rules do not preempt `<k>` execution, allocate state, alter control, or
introduce a fresh result. There are no guard overlaps or recursion. The
program-to-summary connection is witnessed by ordinary execution reaching the
same expanded term, visible again in the false-mutation residual. I found no
candidate-local unsound rule. Consequently there is no unsoundness allegation
for which a false-conclusion witness is required.

The used opaque float primitives are a genuine trust boundary, but not a
smuggled answer: they belong to the supplied semantics, the program executes to
the same applications, and the postcondition cannot choose their values
independently.

## 6. Fresh non-vacuity test

The fresh `AUDIT-SPEC-VACUITY` mutation keeps the valid integer precondition but
changes its result-constraining postcondition from `expectedArea(A,B,C)` to
`-1`. `(3,4,5)` satisfies the guard and both Python implementations return
`6.0`, making the mutation demonstrably false.

`kprove ... --dry-run` parsed and built the mutation successfully with exit 0.
The actual proof exited 1 with `WarnStuckClaimState`: the reached `<k>` term is
the complete `roundFN(powF(mulF(...)),2)` expression, which cannot unify with
`-1`. This is the intended unmet obligation, not a parser error, timeout,
missing import, or unrelated crash.

Evidence: `evidence/06-nonvacuity/spec-vacuity.k`,
`vacuity-build.log`, and `vacuity-kprove.log`.

## 7. Proven versus assumed accounting

Under the supplied K theory, the successful reachability proof establishes that
the exact submitted function, called from the shown empty state on arbitrary K
integer arguments, follows its three comparisons and returns either `-1` or the
fully constrained structural Heron/rounding term selected by the four guards.
Body and postcondition mutations show that this is discriminating.

It does not establish the same theorem for non-integer lengths. It also does not
internally prove IEEE-754 behavior, CPython overflow/NaN/exception behavior,
Python's numeric interpretation of the opaque float symbols, or Heron's
geometric theorem. Those boundaries are supplied float primitives
`divII`, `intToF`, `subF`, `mulF`, `powF`, and `roundFN`, ordinary K built-ins,
the trusted translator, and the informal mathematical bridge from Heron's
formula to triangle area. The exact dependent claims and evidence are recorded
in `evidence/07-accounting/trust-ledger.md`.

The differential run supports source/canonical fidelity only on its recorded
finite inputs. The smoke tests support the supplied concrete float bridge only
on their finite assertions. Neither substitutes for the K proof.

Using the Kit terminology, real-program soundness and non-vacuity pass for the
integer theorem, while intent adequacy fails because of the material
integer-only restriction. That would be `SOUND-BUT-LIMITED`; this benchmark
explicitly maps a material narrowing of the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
