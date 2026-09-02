# Independent adversarial audit — 153-Strongest-Extension

The candidate is **not a legitimate proof of the requested program contract**.
Fresh reconstruction does reproduce `#Top`, and a fresh false-result mutation
is correctly rejected. Those positive facts establish only seven fixed
extension-list executions under the candidate's own theory. That theory has an
execution-relevant semantic defect: it implements Python case classification
as ASCII-only. Fresh K witness claims prove two concrete return values that are
false of both the trusted canonical Python and the submitted Python on valid
Unicode string inputs.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` does not exist, as required for
`GENERATED_SEMANTICS`. I did not search for or use any hidden reference
semantics.

The candidate's `run-input.json` is an untrusted claim that this was problem
`153-Strongest-Extension`, condition `bare`, with no supplied semantics. Its
recorded prompt and translator hashes agree with independently computed
hashes. `metrics.json` claims exit 0, no timeout, and an 852-second run.
`codex-last.txt`, `codex-output.log`, and the structured trace claim the
candidate regenerated the MPY, ran concrete examples, and obtained `#Top`.
Those reports were not used as proof evidence; every relevant operation was
repeated from source.

Integrity results:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`c0ecd987...a3144ca`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485ea...4db16`).
- All required candidate source and provenance artifacts are present as
  regular, non-symlink files: `run-input.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`,
  `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
  `prove.sh`, and `verification-input.mpy`.
- One structured JSONL trace is present, is a regular file, and all 273 records
  parse.
- There are no candidate helper `.k` source files beyond `semantic.k`,
  `verification.k`, and `spec.k`.
- Extra candidate-built `semantic-kompiled/`, `verification-kompiled/`,
  `__pycache__/`, and `.pyc` artifacts are present. They are not integrity
  substitutes and were not copied or reused.
- No required artifact is missing, changed, mistyped, or symlinked. A
  candidate `PROOF.md` and candidate `spec-vacuity.k` are absent, but neither
  was a required generation deliverable.

Exact checks, statuses, and the candidate tree inventory are in
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log). The script
exited 0.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

For a class-name string and a nonempty list of extension-name strings, assign
each extension the score

`number of uppercase letters - number of lowercase letters`.

Return `class_name + "." + the earliest extension having maximal score`.
Digits, punctuation, emoji, and other uncased characters contribute zero.
The trusted canonical implementation uses Python's `str.isalpha`,
`str.isupper`, and `str.islower`, so its character classification is Unicode,
not ASCII-only. Both Python implementations raise `IndexError` on an empty
extension list; normal returned-value behavior therefore has the implicit
nonempty-list boundary used by the canonical source.

The submitted implementation computes the first extension's score, computes
each later score, and replaces the current winner only for strict `>`.
Omitting the canonical's explicit `isalpha()` conjunct does not change
single-character contributions: a character for which Python reports
`isupper()` or `islower()` is a cased alphabetic character. The strict update
preserves the earliest tie.

### Translator identity

I regenerated the MPY only with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0. The regenerated and submitted files are byte-identical,
both with SHA-256
`d9f8d0fa5709221787385385e4d65fe81e32148f33399f3a28c14dec786b1184`.
The preserved regenerated term is
[regenerated-solution.mpy](/audit-output/evidence/regenerated-solution.mpy).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports
`Strongest_Extension` independently from `/reference/canonical.py` and the
scratch copy of `solution.py`. It covers:

- both prompt examples;
- an empty extension list, empty class/name strings, and singleton lists;
- strict-replacement, tie, negative-score, punctuation, digit, and uncased
  branches;
- non-ASCII upper/lower/titlecase, non-Latin, numeric, and emoji characters;
- every extension list of lengths 1–3 over a nine-string branch pool; and
- 2,000 deterministic generated cases (seed 153).

All 2,829 comparisons agree, with zero mismatches. The exact commands and
results are in [stage2_run.sh](/audit-output/evidence/stage2_run.sh) and
[stage2_run.log](/audit-output/evidence/stage2_run.log), both exiting 0.
This is finite fidelity evidence for the submitted Python; it is not a
universal K proof.

## 3. Clean proof reconstruction

All source inputs were copied to `/tmp/audit-work/candidate-src`. No
candidate-built definition or cache was copied. K version
`v7.1.293` was used.

Fresh builds:

```text
kompile --backend llvm /tmp/audit-work/candidate-src/semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/semantic-kompiled-fresh

kompile --backend haskell /tmp/audit-work/candidate-src/verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition /tmp/audit-work/verification-kompiled-fresh
```

Both exited 0. Fresh `kast` output for submitted `solution.mpy` and for
`StrongestProgram` is byte-identical; each KORE file has SHA-256
`dc36b7af...6b734c`. The terms are preserved as
[submitted-solution.kore](/audit-output/evidence/submitted-solution.kore) and
[strongest-program-macro.kore](/audit-output/evidence/strongest-program-macro.kore).

Fresh LLVM executions agree with both Python implementations on the prompt
case, tie case, an empty-name singleton, punctuation/digits, and all-negative
scores. A boundary Unicode execution does not:

| Input | Candidate K result | Canonical Python | Submitted Python |
|---|---|---|---|
| `("C", ["é", "É"])` | `C.é` | `C.É` | `C.É` |

This run exits normally with an empty `<k>` cell; it is a semantic result
divergence, not a stuck term or tool failure. An additional exploratory attempt
to pass an empty `Values` term through `krun -cEXTENSIONS` failed in the config
parser, while both Python implementations raise `IndexError` on `[]`.
That parser attempt is recorded in
[stage3_empty_list_boundary.log](/audit-output/evidence/stage3_empty_list_boundary.log)
and is not treated as proof or non-vacuity evidence.

The exact submitted aggregate proof command

```text
kprove /tmp/audit-work/candidate-src/spec.k \
  --definition /tmp/audit-work/verification-kompiled-fresh \
  --spec-module SPEC
```

exited 0 and printed `#Top`. I also made a label-only reproduction of the seven
claims, [spec-labeled.k](/audit-output/evidence/spec-labeled.k), and selected
each claim independently with `--claims SPEC-LABELED.case01` through
`case07`. Every one exited 0 and printed `#Top`.
[stage3_reconstruct.sh](/audit-output/evidence/stage3_reconstruct.sh) and
[stage3_reconstruct.log](/audit-output/evidence/stage3_reconstruct.log) preserve
all build, execution, structural-pin, aggregate-proof, and per-claim commands
and statuses. The reconstruction script exited 0.

## 4. Adequacy and real-program pinning

Every entry claim has the same structural precondition: `<k>` contains the
exact `StrongestProgram ~> #start`; `<env>` and `<functions>` are empty maps;
`<result>` is `noResult`; and the input cells contain the listed values. There
is no `requires` clause. In claims 2–7, `C:String` permits every K class-name
string; the extension list remains a fixed literal.

| Claim | Plain-language precondition | Plain-language postcondition |
|---|---|---|
| 1 | Class `Slices`; extensions `SErviNGSliCes, Cheese, StuFfed` | Normal completion returning `Slices.SErviNGSliCes` |
| 2 | Any class `C`; extensions `AA, Be, CC` | Return `C.AA` (first maximal tie) |
| 3 | Any `C`; extensions `abc, AB, A-b` | Return `C.AB` (strictly stronger later item) |
| 4 | Any `C`; extensions `a-1, --, A!` | Return `C.A!` (uncased characters score zero) |
| 5 | Any `C`; extensions empty-string, `123, !` | Return `C.` (first zero-score item) |
| 6 | Any `C`; extensions `abcd, a, xy` | Return `C.a` (least-negative score) |
| 7 | Any `C`; singleton `Zz` | Return `C.Zz` |

Formally, each RHS uses `refStrongest(fixed Values)` rather than the displayed
literal, but the guarded reference equations reduce to exactly these strings.
The `<result>` cell is rewritten to an exact `returned(strVal(...))`; it is not
a free variable, tautology, or one-way implication. The final `<k>` is `.K`.
Only final environment and function maps are existentially framed.

Every precondition is satisfiable. For claim 1 the literal state itself is a
witness; for claims 2–7, substituting `C = "Witness"` yields ordinary ground
states. [stage4_claim_witnesses.py](/audit-output/evidence/stage4_claim_witnesses.py)
records all seven states and checks each reduced claimed result against both
Python implementations; all agree. The command log is
[stage4_run.log](/audit-output/evidence/stage4_run.log).

The macro is an exact parse-tree alias, as established by the fresh KORE
identity check. No operational helper claim replaces a loop or function body:
the actual submitted constructor tree executes under `MPY-SEMANTIC`.

The material adequacy gap is theorem scope. No claim has a symbolic extension
list, symbolic extension names, a loop invariant, or a quantified score/maximal
postcondition. The proof therefore establishes seven fixed list executions,
not the requested result for arbitrary nonempty lists of strings. Symbolic
`C` only generalizes a prefix that does not affect selection.

## 5. Rule-by-rule static soundness review

The full line-addressed inventory is preserved in
[rule_inventory.md](/audit-output/evidence/rule_inventory.md), with the raw
declaration extraction in
[stage5_soundness_witness.log](/audit-output/evidence/stage5_soundness_witness.log).
The complete local inventory follows.

### Declarations, configuration, and construct coverage

`MPY-SYNTAX` declares: `Program = Module(Stmts)`; separatorless `Stmts`;
two-string `Params`; comma-list `Exprs`; comma-list `CmpOps`; statements
`FuncDef`, `Assign [strict(2)]`, `AugAssign [strict(3)]`,
`If [strict(1)]`, `For [strict(2)]`, and `Return [strict]`; expressions
`Int`, `Str`, `Name`, `BinOp [strict(2,3)]`, `Compare [strict(1)]`,
`Subscript [strict(1)]`, `Slice`, `Attribute [strict(1)]`, and
`Call [strict(1)]`; plus `CmpOp` and `Bound`.

The runtime declares `intVal`, `strVal`, `listVal`, `boolVal`, and
`boundStringMethod`; semicolon-list `Values`; `Value` as both `KResult` and
`Expr`; `function(Params,Stmts)`; `noResult`/`returned`; and internal items
`exec`, `setVar`, `loopValues`, `loopString`, and `#start`.
`isUpperChar` and `isLowerChar` are the only `[function, total]` declarations.
There are no local `[functional]`, `[simplification]`, priority, `owise`,
`anywhere`, or opaque declarations.

The configuration contains computation, local environment, function table,
two input cells, and result. The submitted program needs no heap, allocation,
I/O, or exceptions on its nonempty normal domain.

Every constructor in `solution.mpy` is covered:

| Used construct | Declaration/rules |
|---|---|
| `Module`, statement list, `FuncDef`, entry call | S01–S05 |
| `Int`, `Str`, `Name` | S06–S08 |
| `Assign`, `AugAssign` | S09–S12 |
| index `0`, slice `[1:]` | S13–S14 |
| list and string `For` | S15–S20 |
| `Attribute`, zero-argument case calls | S21–S25 |
| `If` | S26–S27 |
| integer/string `BinOp` | S28–S29 |
| single strict-greater `Compare` | S30 |
| terminal `Return` | S31 |

### Ordinary semantic rules

| IDs | Rules and decision |
|---|---|
| S01–S03 (`semantic.k:78–80`) | Module and statement sequencing. Sound left-to-right execution. |
| S04 (`:82–83`) | Installs a capture-free function. Sound for this top-level, default-free definition. |
| S05 (`:87–92`) | Exact entry driver for the loaded name, parameters, body, and fresh local bindings. It reads the input cells and does not fabricate a result. Sound for this target invocation. |
| S06–S10 (`:95–103`) | Literal wrapping, lookup, assignment, and loop-variable update. Sound for the target state model. |
| S11–S12 (`:105–108`) | Integer `+=` and `-=`. Sound. |
| S13–S14 (`:111–113`) | Nonempty-list index zero and `[1:]`. Sound for all normal states reaching them; empty-list exceptions are unmodeled. |
| S15–S17 (`:117–120`) | Ordered list loop initialization, empty case, and step. Sound; final loop variables persist as in Python. |
| S18–S20 (`:122–128`) | String loop from index zero through `lengthString`, taking `[I:I+1]`. Sound for exercised K strings subject to the builtin string-hook boundary. |
| S21 (`:134`) | Defines uppercase as code point 65–90. **Materially unsound for Python `str.isupper` on valid Unicode inputs; false-conclusion witness U1 below.** Its unguarded `[total]` domain also exceeds the stated one-character use of `ordChar`; no separate target-program witness is asserted for multi-character direct calls. |
| S22 (`:135`) | Defines lowercase as code point 97–122. **Materially unsound for Python `str.islower`; witness U2.** It has the same over-broad totality gap. |
| S23 (`:137`) | Binds an arbitrary named string attribute. It is over-broad but cannot produce a result except through modeled call rules; the target only reaches the two intended names. |
| S24 (`:138–139`) | Routes `isupper()` to S21. The control plumbing is exact, but its value conclusion inherits U1. |
| S25 (`:140–141`) | Routes `islower()` to S22 and inherits U2. |
| S26–S27 (`:143–144`) | Boolean branch selection. Sound. |
| S28 (`:146`) | Integer addition. Mathematically sound and unused by this tree. |
| S29 (`:147`) | String concatenation. Sound subject to the builtin K String bridge. |
| S30 (`:148–149`) | Exact target comparison: evaluated left integer against the right name's current integer. Sound for this constructor and environment. |
| S31 (`:151–152`) | Consumes terminal `Return` and sets `<result>`. Sound at the submitted body's last-statement context. It is not a general abrupt-return rule for an arbitrary continuation; because no such continuation is reachable in this body, I record a reuse limitation rather than claim another target-program unsoundness. |

`BinOp [strict(2,3)]` does not itself enforce Python's left-to-right operand
order, but all target additions have side-effect-free operands. `Compare`
evaluates only the left operand because S30 performs the exact right-name
lookup; the target's RHS is a side-effect-free name. Thus neither restricted
evaluation design yields a false conclusion for this submitted tree.

The semantics has no allocation. Function definition and the task-specific
entry driver preserve the only binding behavior needed. The two loops perform
state updates before their bodies and recur afterward. Rule guards for the
string loop (`I >= length` versus `I < length`) and `If` rules are disjoint.
There are no local priorities or simplifications that alter overlaps.

### Verification macro and mathematical functions

- V01 (`verification.k:9–40`) is the `StrongestProgram` macro. Its expansion is
  byte-identical in KORE to submitted `solution.mpy`.
- V02–V04 (`:52–57`) define `refDelta` by upper, lower, and neither. Their
  guards are disjoint and exhaustive relative to S21/S22's Booleans. They
  inherit the Python mismatch demonstrated by U1/U2, so the purported
  contract function is not independent at this result-bearing primitive.
- V05 (`:59`) starts `refStrengthAt` at zero.
- V06–V07 (`:60–65`) are disjoint base/recursive rules; the index increments
  toward `lengthString`.
- V08 (`:67–68`) initializes `refSelect` from a nonempty `strVal` list.
- V09 (`:69`) returns the best at the empty tail.
- V10–V11 (`:70–75`) replace on strict greater and retain on less-or-equal.
  The guards are disjoint/exhaustive over integer scores and correctly preserve
  the first tie.

These reference functions are definitional summaries; they do not rewrite or
bypass the operational program body. None is declared total, and non-string
list elements can remain undefined. There are no auxiliary claims, opaque
symbols, result oracles, proof-local simplifications, or operational bridges.

### Required false-conclusion witnesses

[spec-unsound-witness.k](/audit-output/evidence/spec-unsound-witness.k) contains
two fresh ground reachability claims:

- **U1, S21/S24:** for `("C", ["--", "É"])`, K proves `returned("C.--")`
  with `#Top` and exit 0. Canonical and submitted Python both return `C.É`.
- **U2, S22/S25:** for `("C", ["é", "--"])`, K proves
  `returned("C.é")` with `#Top` and exit 0. Both Python programs return
  `C.--`.

Latin-1 `É` and `é` parse and execute normally in the fresh K definition, so
these are satisfying intended-domain witnesses. They isolate uppercase and
lowercase respectively: the companion classification is false for both
strings in each witness. Exact commands, `#Top` outputs, Python results, and
statuses are in
[stage5_soundness_witness.sh](/audit-output/evidence/stage5_soundness_witness.sh)
and [stage5_soundness_witness.log](/audit-output/evidence/stage5_soundness_witness.log).
This is direct evidence that the candidate theory can prove false conclusions
about the real generated program.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I created
[spec-vacuity-auditor.k](/audit-output/evidence/spec-vacuity-auditor.k) from
the singleton entry state `("C", ["Zz"])` and changed the exact required result
from the demonstrably correct `C.Zz` to `C.WRONG`.

The dry run parsed and built successfully with exit 0. The real proof run
exited 1 with `WarnStuckClaimState`; its residual has empty `<k>` and the
reached `<result> returned(strVal("C.Zz"))`, which does not unify with the
mutated destination. This is the expected unmet result obligation, not a
parser error, timeout, unrelated crash, or unreachable mutation.

The mutation source, exact commands, statuses, and bounded residual are in
[stage6_nonvacuity.sh](/audit-output/evidence/stage6_nonvacuity.sh),
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log), and
[stage6_mutation_proof.raw.log](/audit-output/evidence/stage6_mutation_proof.raw.log).
Stage 6 passes: the submitted proof is result-constraining and non-vacuous for
its narrow claims.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the rules in the candidate's generated K theory, execution of the exact
submitted constructor tree, from fresh state, reaches `.K` and the stated
result for seven particular extension lists. The first class is fixed as
`Slices`; the other six claims quantify only over the class-name K String.
Because list contents and lengths are fixed, K unfolds all loops concretely.
There is no theorem for arbitrary extension names, list length, or a universal
maximal-score/tie invariant.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical Python, and translator mounts | Intent, executable oracle, and Python-to-MPY identity | Authorized trusted inputs. Prompt/translator identity and MPY regeneration were checked. |
| K compiler/prover and builtin `INT`, `BOOL`, `MAP` | Arithmetic, guards, map state, and proof execution | Ordinary low-level toolchain trust; acceptable. |
| K `STRING` hooks: concatenation, length, substring, `ordChar` | Iteration, classification, and final result | Necessary implementation boundary. Concrete testing supports exercised ASCII/Latin-1 mechanics but does not prove equivalence to Python Unicode strings. |
| S01–S20, S23, S26–S31 | Program loading, state, loops, control, and return | Audited as sound for the exact target normal executions, with documented non-reusable omissions for exceptions/general return contexts. |
| S21/S24 (`isupper`) | Scores, winner branch, returned extension, and reference postcondition | **Illegitimate:** U1 is a machine-checked false-result witness. |
| S22/S25 (`islower`) | Same | **Illegitimate:** U2 is a machine-checked false-result witness. |
| `refDelta/refStrength/refSelect` | Exact postcondition value | Equations are terminating and guarded for submitted uses, but `refDelta` shares the faulty classification primitive with execution. It is not an independent universal bridge to the prompt. |
| `StrongestProgram` macro | Pins proof execution to submitted MPY | Acceptable; fresh KORE terms are identical. |
| Python differential test | Submitted-Python to canonical bridge on 2,829 inputs | Strong finite empirical support only; it does not repair K semantics or prove universal equivalence. |
| Seven positive `#Top` results | Closure under the candidate theory | Genuine but limited verification evidence; neither validates the theory nor broadens fixed extension lists. |
| Fresh false mutation | Result sensitivity | Valid non-vacuity evidence only. It does not establish semantic fidelity. |

There are no opaque result symbols, unconstrained empirical oracles, helper
reachability claims, allocations, or I/O assumptions. The central problem is
instead a fully defined but false result-bearing primitive, used by both
execution and the postcondition helper.

### Decision

Clean proof reconstruction and non-vacuity succeed, but two independent
grounds require rejection:

1. The generated semantics admits and freshly proves concrete returned values
   that are false of the real submitted Python program on valid Unicode string
   inputs. This is a material semantic unsoundness with explicit witnesses,
   not merely thin evidence.
2. Even over the ASCII fragment where the rules agree, `spec.k` proves only
   seven fixed extension lists. It does not state or prove the task's general
   nonempty-list contract.

Candidate `#Top`, provenance reports, trace, and finite differential evidence
cannot substitute for the missing general theorem or cure the false semantic
rules.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
