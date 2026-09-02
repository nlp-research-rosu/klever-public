# Independent adversarial review — 110-exchange

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program over the generated model's domain:
finite `PyList` values containing K mathematical integers. Fresh definitions
were built from source, the actual submitted AST was pinned exactly, all
positive claims closed independently with their required loop circularity, and
a fresh wrong-result mutation failed at the expected obligation.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
documented limitations:

1. The prompt says lists of “numbers” but does not explicitly state “integers,”
   while the K model admits only integer elements. The conventional meaning of
   “even” makes integers the natural domain, and the candidate agrees with the
   canonical function on all 8,144 tested non-empty integer cases. Nevertheless,
   the two Python implementations demonstrably diverge on non-integral numeric
   inputs that Python accepts.
2. The equivalence between the formal threshold and the human-facing exchange
   property is an ordinary but informal mathematical bridge, not a separate K
   theorem about the English contract.
3. The one prioritized semantic shortcut was validated in the complete
   reachable program context and is unnecessary for claim closure. A still
   broader auditor-created connection claim stopped on K Map normalization.
   This is a narrow proof-evidence gap, not an unsoundness finding: no false
   conclusion witness exists, and the rule is the exhaustive parity equation.

All paths below are reviewer evidence unless explicitly identified as candidate
or trusted input.

## Stage 1 — Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted
`/reference/reference-semantics` path is absent, exactly as required. The
trusted reference mount contains only regular files
`canonical.py`, `prompt.py`, and `py2mpy.py`. There is therefore no
infrastructure breach and no hidden/supplied semantics was sought or used.
The live toolchain is K `v7.1.293`.

Evidence: `/audit-output/evidence/00-environment-and-boundary.log`.

### Required artifacts and file integrity

The following candidate artifacts are present as regular, non-symlink files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  one structured JSONL generation trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.

No candidate symlinks were found. Candidate `prompt.py` is byte-identical to
trusted `/reference/prompt.py` (SHA-256
`3ae7e8bd32a483624eaf7543bf375fec87e33e448f4c417e879a21a04dd0dba6`).
Candidate `py2mpy.py` is byte-identical to trusted
`/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
These hashes also agree with the untrusted `run-input.json` provenance claims.

Evidence:

- `/audit-output/evidence/01-candidate-inventory.log`
- `/audit-output/evidence/01-integrity-comparisons.log`

The candidate includes extra generated material:
`semantic-kompiled/` and `__pycache__/`. These are regular files/directories,
not required source artifacts. They were treated only as untrusted extras and
were neither copied into the reconstruction nor used by any audit command.
There is no candidate `PROOF.md` or `spec-vacuity.k`; neither was a required
deliverable in the recorded bare generation request. A fresh mutation was
created in Stage 6.

### Untrusted provenance claims

`metrics.json` claims generation exited zero without timeout.
`codex-last.txt`, `codex-output.log`, and the trace claim that the candidate's
script produced three displayed `#Top` lines: two pattern-based concrete runs
and one all-claims proof result. Earlier stuck proof attempts are also visible
in the log. None of those results was trusted; they were read solely to account
for provenance and then independently reconstructed.

Evidence:
`/audit-output/evidence/01-untrusted-generation-claims.log`.

Stage 1 result: **PASS**.

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

`/reference/prompt.py` asks whether any number of elements can be exchanged
between two non-empty lists so that every element in the first list is even.
For finite integer lists, let:

- `m = len(lst1)`,
- `e1 =` the number of even elements in `lst1`,
- `o1 = m - e1`,
- `e2 =` the number of even elements in `lst2`.

An exchange is possible exactly when there are at least `o1` even elements in
the second list to replace the odd elements in the first:
`e2 >= o1`. This is equivalent to `e1 + e2 >= m`.

The trusted canonical function counts `o1` and `e2`, returning `"YES"` iff
`e2 >= o1`. The candidate counts `e1 + e2`, returning `"YES"` iff that total is
at least `len(lst1)`. Thus the algorithms are mathematically equivalent on
integer lists. The candidate preserves the required `exchange(lst1, lst2)`
signature.

### Trusted regeneration

The submitted `solution.mpy` was regenerated in scratch using the trusted
translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/110-exchange/solution.py \
  > /tmp/audit-work/110-exchange/solution.regenerated.mpy
```

The submitted and regenerated files are byte-identical with SHA-256
`42d21b6d65119d8adddd91c16bfc0534b407c036e8aca9cb0cd8c1832c4ba8b6`.

Evidence:
`/audit-output/evidence/02-scratch-copy-and-translation.log`.

### Independent differential testing

The reviewer-authored test
`/audit-output/evidence/02_differential.py` imports the trusted canonical
function directly from `/reference/canonical.py` and the candidate function
from the scratch-copied `solution.py`; it does not reuse any K equations.
Its complete input/results corpus is
`/audit-output/evidence/02-differential-inputs.jsonl`.

The run covered:

- both documented examples;
- 117 empty-list boundary cases, although empty lists are outside the stated
  non-empty input assumption;
- exhaustive pairs of lists of lengths 0–2 over integers `-3..3`;
- 5,000 deterministic generated non-empty pairs, with lengths 1–12 and values
  in `-1000..1000`;
- explicit cases below, at, and above the decision threshold;
- zero, negative parity, one-iteration, and multi-iteration loop cases;
- two deliberately extended non-integral numeric cases.

Results:

```text
records=8263
case_counts={"boundary_empty_integer": 117,
             "extended_nonintegral": 2,
             "intended_nonempty_integer": 8144}
mismatch_counts={"extended_nonintegral": 2}
branch_gap_signs=[-1, 0, 1]
```

There were zero mismatches on the non-empty integer domain and zero on empty
integer boundaries. The two preserved non-integral mismatches are:

- `lst1=[0.5], lst2=[1.0]`: canonical `"YES"`, candidate `"NO"`;
- `lst1=[2.0,0.25], lst2=[3.0]`: canonical `"YES"`, candidate `"NO"`.

This does not falsify the integer theorem, but it prevents silently broadening
the bridge from `PyList[Int]` to every Python numeric value.

Evidence:

- `/audit-output/evidence/02-differential-run.log`
- `/audit-output/evidence/02-differential-mismatch-details.log`

Stage 2 result: **PASS on the conventional integer domain, with a documented
non-integral intent-scope concern**.

## Stage 3 — Clean proof reconstruction

### Scratch isolation and fresh builds

Only source artifacts were copied to `/tmp/audit-work/110-exchange`.
No candidate `*-kompiled` directory, binary, cache, or `.pyc` was copied.
The reviewer built:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0. A separate LLVM definition with `--enable-search` was also built
to support result-cell pattern checks. The first pattern-run attempt against
the ordinary LLVM build failed before execution because LLVM pattern search
requires that flag. That audit-harness error is preserved in
`03-concrete-cases.log`; it was not treated as candidate evidence.

Build evidence:

- `/audit-output/evidence/03-build-concrete-llvm.log`
- `/audit-output/evidence/03-build-concrete-llvm-search.log`
- `/audit-output/evidence/03-build-proof-haskell.log`

### Exact real-program pin

Fresh `kast --output kore --expand-macros` results were compared for:

1. submitted `solution.mpy`;
2. trusted-regenerated `solution.regenerated.mpy`;
3. `VERIFICATION.solutionProgram`.

All three are byte-identical after expansion. The two compared KORE terms have
the same SHA-256:
`265cdd0376a01c3557ec9ba57363c23faffe6f9a7573dcd13495701ec9531095`.
An independently generated body mutation (`even + 2` in the second loop) is
rejected by the same pin with `cmp` exit 1.

Evidence:

- `/audit-output/evidence/03-ast-pinning.log`
- `/audit-output/evidence/05-program-body-sensitivity.log`

### Fresh generated-semantics execution

`/audit-output/evidence/03_concrete_cases.py` ran the search-enabled fresh LLVM
semantics on eight cases and compared each with both Python functions:
the two prompt examples, both-empty, an empty-right odd case, below-threshold,
exact-threshold, negative integers, and zero. Every K pattern run printed
`#Top`, every command exited 0, both Python results agreed, and the test reported
`FAILURES: 0`.

Evidence:
`/audit-output/evidence/03-concrete-cases-search-enabled.log`.

### Every positive claim

The loop circularity was run alone:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-counts-even --output pretty --smt-timeout 5000
#Top
EXIT_STATUS: 0
```

Each entry target was then run independently together with its required loop
circularity:

```text
--claims SPEC.loop-counts-even,SPEC.exchange-yes  -> #Top, exit 0
--claims SPEC.loop-counts-even,SPEC.exchange-no   -> #Top, exit 0
```

Finally, the complete unfiltered three-claim suite printed `#Top` and exited 0.

Evidence:

- `/audit-output/evidence/03-kprove-loop-counts-even.log`
- `/audit-output/evidence/03-kprove-exchange-yes-with-helper.log`
- `/audit-output/evidence/03-kprove-exchange-no-with-helper.log`
- `/audit-output/evidence/03-kprove-all-positive.log`

A diagnostic command initially selected `exchange-yes` alone, thereby also
filtering out the circularity it needs, and was interrupted after about 90
seconds. It did not return a proof result. The exact incomplete command is
preserved in `/audit-output/evidence/03-kprove-exchange-yes.log`; the corrected
target-plus-helper command above is the required independent run.

Stage 3 result: **PASS**.

## Stage 4 — Adequacy and real-program pinning

### Claim meanings

`loop-counts-even` has no explicit `requires` clause. Its typed configuration
is its precondition: for any `PyList L`, integer accumulator `N`, old integer
loop value `OLD`, and arbitrary continuation `CONT`, executing the exact real
loop body:

- consumes the loop and resumes `CONT`;
- preserves `lst1`, `lst2`, and `result=noResult`;
- changes `even` to `N + countEven(L)`;
- changes `value` to the last element of `L`, or preserves `OLD` for `Nil`.

`exchange-yes` starts from the exact submitted `solutionProgram`, arbitrary
`PyList` inputs, empty environment, and `noResult`. Its precondition is:

```text
countEven(L1) + countEven(L2) >= length(L1)
```

It consumes all computation, gives the exact final environment, and constrains
the result to the concrete string `"YES"`.

`exchange-no` has the complementary strict precondition:

```text
countEven(L1) + countEven(L2) < length(L1)
```

It consumes all computation, gives the exact final environment, and constrains
the result to `"NO"`.

The entry preconditions are disjoint and exhaustive for K integers. The result
cell is not free, existential, tautological, or merely constrained by a
one-way implication.

### Satisfiable witnesses and substitution

Ground witnesses are recorded in
`/audit-output/evidence/04-claim-witnesses.log`:

- `exchange-yes`: `L1=[0]`, `L2=[1]`. Total even count and length are both 1,
  so the precondition holds; K, candidate Python, and canonical Python all give
  `"YES"`.
- `exchange-no`: `L1=[-4,-3,-2,-1]`, `L2=[-8,-7]`. Total even count is 3 and
  length is 4, so the strict precondition holds; all three executions give
  `"NO"`.
- `loop-counts-even`: `L=[2,1]`, `N=5`, `OLD=9`, `CONT=.K` with a complete
  exact environment and `noResult`. The claimed final values are
  `even=6`, `value=1`.

Both entry witnesses also satisfy the prompt's non-empty-list assumption.

The `<k>` term executes `solutionProgram`, whose expansion is exactly the
trusted-regenerated submitted `solution.mpy` as established in Stage 3.
The loop helper uses the exact body appearing in both real loops and the
arbitrary continuation is preserved.

Stage 4 result: **PASS**.

## Stage 5 — Rule-by-rule static soundness review

The complete declaration-by-declaration and rule-by-rule ledger is preserved
at `/audit-output/evidence/05_rule_inventory.md`; numbered source is in
`/audit-output/evidence/05-numbered-k-sources.log`.

### Exhaustive declaration inventory

`semantic.k` contains 13 `syntax` declaration lines and 29 ordinary rules.
They declare:

- AST lists and constructors: `Params`, `CmpOp`, `Int`, `Str`, `Name`,
  `BinOp`, `Compare`, `Call`, `Module`, `FuncDef`, `Assign`, `If`, `For`, and
  `Return`;
- `PyList = Nil | Cons(Int,PyList)`, values, and results;
- control terms `init`, `exec`, `eval`, `write`, `binRight`, `applyBin`,
  `cmpRight`, `applyCmp`, `doLen`, `branch`, `startFor`, `loop`, and `finish`;
- total function `length`.

`verification.k` contains five syntax declarations and eight rules:
the `countBody` and `solutionProgram` macros, and total functions `evenBit`,
`countEven`, and `lastValue`.

There are no local opaque symbols, `[functional]` declarations,
`[simplification]` rules, or uninterpreted result-bearing symbols. The only
local priority is `[priority(40)]` on the parity-counting shortcut.

### Exhaustive ordinary-rule decisions

The 29 semantic rules are inventoried as:

- S01–S02: `length` base/recursive equations;
- S03: exact external `exchange` invocation and argument/local initialization;
- S04–S06: empty sequencing, assignment scheduling, and map write;
- S07–S09: generic `If` scheduling and true/false branches;
- S10: prioritized parity-counting bridge;
- S11–S14: `For` scheduling, list-to-loop transition, and loop base/step;
- S15–S16: abrupt `Return`, result storage, and function-computation clearing;
- S17–S19: integer/string literals and name lookup;
- S20–S23: left-to-right binary evaluation, integer addition, and remainder;
- S24–S27: left-to-right comparison evaluation, equality, and `>=`;
- S28–S29: exact `len` call and structural list length.

The detailed ledger records a `Sound` decision and justification for every
rule. Key checks:

- **Configuration/cells:** `<k>`, `<env>`, and `<result>` cover all control,
  local state, and returned output used by this pure function. There is no used
  heap, allocation, I/O, exception, or external state.
- **Evaluation order:** assignments, binary operations, comparisons, iterable
  evaluation, and `len` arguments evaluate left-to-right as required.
- **Control:** loop steps write each element before the body; empty loops stop;
  the last loop variable persists; `Return` discards later statements and all
  remaining function computation.
- **State:** writes update one map key and preserve all others; loops preserve
  list bindings and result. The invocation wrapper initializes `value=0` even
  when a loop is empty. Python would leave that local unbound, but this program
  never reads it after an empty loop and it cannot affect the observable
  result. This is an internal-model over-specification, not a false return.
- **Numeric behavior:** K `Int` and Python integers are unbounded. The used
  remainder divisor is the fixed nonzero value 2, and testing equality with
  zero agrees for negative parity. Operations or types not used by the
  submitted AST remain visibly unmodeled.
- **Coverage/overlap:** structural function equations cover `Nil`/`Cons`
  disjointly and descend. `evenBit` guards are complementary and exhaustive.
  The true/false rules are disjoint. Other ordinary rules have distinct front
  control shapes.

### Prioritized operational bridge

S10 replaces execution of the exact idiom:

```text
if X % 2 == 0:
    Y = Y + 1
```

when `X` and `Y` are bound to integers. It changes only `Y`, adding
`evenBit(I)`, and resumes the identical statement suffix and outer
continuation. `evenBit` is not opaque: its two guarded equations give 1 exactly
for zero remainder and 0 otherwise.

The following independent sensitivity checks were performed:

1. S10 was removed in
   `/audit-output/evidence/05_semantic_no_bridge.k`, and a fresh Haskell
   definition built successfully.
2. The entire original proof suite still closes with `#Top` under the
   no-bridge semantics:
   `/audit-output/evidence/05-kprove-all-without-parity-bridge.log`.
   Thus S10 does not smuggle the final correctness conclusion or make an
   otherwise false claim provable.
3. Two auditor claims execute the generic fixed rules without S10 for the
   exact reachable identifiers and complete environment. Their guards split
   zero versus nonzero remainder, and they quantify over arbitrary remaining
   statements and continuation. Both close together with `#Top`:
   `/audit-output/evidence/05-kprove-parity-bridge-actual-context.log`.
   This checks result, state, and control containment in every context the real
   program supplies.
4. A broader symbolic-key connection attempt reached the intended final
   control/value states but stopped because the backend did not normalize a
   K Map update to the equivalent explicit map entry. The residuals are
   preserved in
   `/audit-output/evidence/05-kprove-parity-bridge-connection.log` and
   `/audit-output/evidence/05-kprove-parity-bridge-generic-execution.log`.

The broad residual is an evidence gap, not a false-conclusion witness. Ordinary
map-update semantics plus the complementary `evenBit` equations establish the
rule wherever its distinct-key map pattern matches. Accordingly, this review
does **not** label S10 unsound.

### Proof-local macros/functions and construct coverage

V01 `countBody` expands exactly to both submitted loop bodies. V02
`solutionProgram` expands to the complete submitted AST and is independently
pinned. V03–V04 define `evenBit`; V05–V06 define recursive `countEven`;
V07–V08 define recursive `lastValue`. All function rules are truthful,
guard-complete, non-overlapping, and structurally terminating where recursive.

Every syntactic constructor used in `solution.mpy` has a declaration and
execution path:

| Used form | Rules |
|---|---|
| `Module(FuncDef(...Params...))` | S03 |
| statement lists, `Assign`, `Name` | S04–S06, S19 |
| `For` | S11–S14 |
| `If` | S07–S10 |
| `Return` | S15–S16 |
| `Int`, `Str` | S17–S18 |
| `BinOp("+")`, `BinOp("%")` | S20–S23 |
| `Compare("==")`, `Compare(">=")` | S24–S27 |
| `Call(Name("len"),...)` | S28–S29 |

No used construct is fabricated by an unconstrained oracle or bypassed by an
answer-encoding rule.

Stage 5 result: **PASS, with the recorded broad-connection evidence gap and
generated-model scope limitations**.

## Stage 6 — Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. The reviewer created
`/audit-output/evidence/06_spec_vacuity_audit.k`, retaining the loop circularity
and the original `exchange-yes` precondition while changing the
result-constraining postcondition from `"YES"` to `"NO"`.

The mutation is demonstrably false for the satisfiable non-empty integer
witness `L1=Cons(0,Nil)`, `L2=Cons(1,Nil)`: its total even count equals
`length(L1)`, so the unchanged precondition holds and the real program returns
`"YES"`.

First, a `kprove --dry-run` build exited 0:
`/audit-output/evidence/06-vacuity-build-dry-run.log`.

The real mutation proof then exited 1 with `WarnStuckClaimState`. Its residual
has consumed computation, has the expected final environment, and contains:

```text
<result>
  "YES"
</result>
```

while the destination demands `"NO"`. This is the expected unmet
result obligation, not a parse error, missing import, timeout, unrelated crash,
or unreachable mutation.

Evidence:
`/audit-output/evidence/06-vacuity-expected-failure.log`.

Stage 6 result: **PASS**.

## Stage 7 — Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted generated semantics, for all finite `PyList` values `L1`
and `L2` containing K integers:

1. Each loop executes the exact submitted parity-counting body and adds exactly
   the number of even elements in its input list to `even`.
2. Starting the exact submitted program from `init(solutionProgram,L1,L2)`
   consumes the complete computation.
3. If `countEven(L1)+countEven(L2) >= length(L1)`, the result is exactly
   `"YES"`.
4. If the complementary strict inequality holds, the result is exactly `"NO"`.
5. The proof also fixes the complete final environment, including the final
   accumulator and loop-variable value.

This is a partial-correctness reachability result under the selected K theory.
It is not, by itself, a universal theorem about all CPython values, a formal
semantics equivalence with CPython, or a K proof of the English meaning of
“exchange.”

### Trust and assumption ledger

| Boundary | Role and influence | Dependents | Assessment/evidence |
|---|---|---|---|
| K `v7.1.293`, Haskell/LLVM backends, reachability engine | Compilation, concrete rewriting, symbolic closure | Every K result | Necessary low-level trusted computing base; fresh builds and exact exits/outputs are recorded. |
| K built-ins `INT`, `BOOL`, `STRING`, `MAP`, K sequences/lists | Arithmetic, comparisons, maps, strings, control representation | All semantic rules and claims | Acceptable standard primitive boundary. The review audited every local equation/bridge layered on top. |
| Trusted `/reference/py2mpy.py` | Maps `solution.py` CPython AST into the constructor term | Real-program identity | Explicit trusted input. Trusted regeneration is byte-identical; expanded KORE also matches the proof macro exactly. |
| `init` invocation wrapper | Interprets a call to the exact `exchange(lst1,lst2)` definition by binding arguments and executing its body | Both entry claims | Generated-semantics modeling boundary. It pins name, params, full body, and inputs; concrete and static checks support the used context. |
| Generated integer-only semantics | Models exactly the syntax/operations used by this submitted program | All formal conclusions | Audited rule by rule and concretely tested. It excludes floats, arbitrary Python objects, mutation/aliasing beyond local scalar state, exceptions, and other calls. |
| S10 parity bridge | Accelerates one program-derived `if`/increment | Loop and entry proofs in the submitted definition | Fully defined, exact-state/context connection proved on both reachable branches; all claims also prove with S10 removed. Broad symbolic-key Map-normalization theorem remains unchecked, with no false witness. |
| `evenBit`, `countEven`, `length`, `lastValue` | Mathematical summaries used in semantics/claims | Loop invariant, entry guards and final state | Not opaque. Complete, disjoint, terminating equations audited against ordinary mathematics. |
| Integer exchange equivalence `e2 >= o1` iff `e1+e2 >= len(lst1)` | Connects formal threshold to English task | Natural-language correctness conclusion | Correct elementary argument for integer lists, but informal rather than a separate K theorem. |
| `/reference/canonical.py` differential oracle | Empirical implementation-to-reference bridge | Fidelity/intent confidence only | Independent of K equations. Zero mismatches in 8,144 intended non-empty integer cases; finite testing is not substituted for the K proof. |
| Integer-domain interpretation | Treats “even numbers” as integer parity | Scope of the final natural-language conclusion | Conventional and consistent with K/canonical task usage, but prompt says “numbers.” Two float counterexamples prevent claiming broader Python-numeric equivalence. |

There are no opaque symbols, unconstrained result-bearing oracles, assumed
program-defined helper bodies, external I/O primitives, or candidate-provided
compiled artifacts in the trust base.

### Validation gates and verdict rationale

- **Gate A — real-program soundness: PASS.** The real AST is exactly pinned;
  program bodies execute; the sole operational bridge is value/control
  connected on the complete reachable context and is unnecessary for proof
  closure; preconditions are satisfiable; and the false result mutation is
  rejected.
- **Gate B — intent adequacy: PASS for finite integer lists, with concerns.**
  The formal threshold is the correct exchange criterion for integers and the
  prompt examples agree. The unstated integer restriction and witnessed float
  divergence are explicit limitations.
- **Gate C — trust/evidence auditability: PASS.** All builds, commands,
  statuses, bounded outputs, differential inputs/results, reviewer scripts,
  connection experiments, and mutation artifacts are preserved. Differential
  evidence is reported only as finite evidence.

The proof is therefore legitimate and pins the real generated program. The
scope and informal intent bridges are material enough to document as
`CONCERNS`, but they do not make a false integer-domain result provable and do
not justify `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
