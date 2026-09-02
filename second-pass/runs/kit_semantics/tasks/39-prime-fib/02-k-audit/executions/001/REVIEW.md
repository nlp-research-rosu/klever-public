# Independent adversarial review: 39-prime-fib

Outcome: the candidate contains a legitimate symbolic partial-correctness
proof of the submitted program for positive integer ordinals `N >= 1`. The
proof is body-sensitive, result-constraining, and uses the supplied semantics
without an operational shortcut. I assign `CONCERNS`, rather than `PASS`,
because the final result is a backward-folding, non-total summary term whose
identification with “the N-th prime Fibonacci number” is validated by ordinary
mathematics and finite execution evidence, not by a separate K theorem. The
implicit-positive-domain reading also matters: the rewrite and canonical
implementation differ at `n = 0`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `39-prime-fib`, and condition
`kit-semantics`. I read every required pipeline-v3 record named by the prompt:
`/run.json`, `/task.json`, `/generation-result.json`, all six generation
metadata/text files, and all 652 JSONL records in the structured trace. The
generation report's `VALIDATED`/`#Top` claims were treated only as untrusted
history. The bounded extraction is
[01_trace_extract.log](/audit-output/evidence/01_trace_extract.log), generated
by [01_trace_extract.py](/audit-output/evidence/01_trace_extract.py).

The infrastructure gate passes:

- `/audit-campaign-lock.json` is exactly equal, as parsed JSON, to the
  `audit_campaign` block in `/audit-input.json`, and its SHA-256 is the recorded
  `ad5dfc...d745`.
- Every required mount/record is a real readable file or directory. No symlink
  occurs under `/candidate`, `/reference`, or `/generation-evidence`; neither
  semantics tree contains a special entry.
- Every recorded direct file hash checked successfully, including the run,
  task, result, invocation, metrics, runtime metrics, usage, prompt, output log,
  final message, canonical program, trusted prompt, and translator.
- The pipeline-v3 canonical tree hash of `/candidate` is
  `a0bd2a...672c6`, exactly the generation result's `workspace_sha256`. The
  trace tree hash is `32ace9...e927`, exactly `usage.json`'s
  `source_trace_sha256`; the JSONL file hash is the independently recorded
  `c366b2...d66c5`.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted mounts.
- `diff -r --no-dereference` reports no difference between candidate and
  trusted `reference-semantics/`. Both trees have pipeline hash
  `4e0639...89f`, matching the task manifest. There are no missing, additional,
  mistyped, changed, or linked entries.

The exact commands, expected hashes, file types, exit statuses, and outputs are
in [01_integrity.log](/audit-output/evidence/01_integrity.log), with the
reproducible driver [01_integrity.sh](/audit-output/evidence/01_integrity.sh).
There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `prime_fib(n)`, the N-th number that is both a
Fibonacci number and prime, with examples `2, 3, 5, 13, 89` for `n = 1..5`.
The trusted canonical repeatedly appends the next Fibonacci number, tests it by
trial division, decrements `n` for primes, and returns when the positive
ordinal count reaches zero.

The candidate rewrite maintains consecutive Fibonacci state `(a,b)`, advances
it, trial-divides the new `a` through `divisor * divisor <= a`, increments
`count` using Python's Boolean-as-integer behavior, and returns after `count`
reaches `n`. For positive integer `n`, this is extensionally the same search.

Trusted regeneration was exact:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.submitted.mpy solution.regenerated.mpy
```

Both commands exited 0. Both files have SHA-256
`35e6dc...ad5e`; see
[02_fidelity.log](/audit-output/evidence/02_fidelity.log).

The independent differential script
[02_differential.py](/audit-output/evidence/02_differential.py) imports both
the trusted canonical entry point and the generated entry point. It checks:

- all five documented examples;
- the lower intended boundary and every `n` in `1..11`, in a seeded generated
  order;
- all executable lines of the generated function;
- branch witnesses for `a < 2`/`a >= 2`, entering/skipping the divisor loop,
  divisible/non-divisible modulo results, outer repetition, and outer exit.

There were zero mismatches. The values through `n=11` end in
`2971215073`. The complete run and exit 0 are in
[02_fidelity.log](/audit-output/evidence/02_fidelity.log).

The nearest empty/outside-domain observation is material to scope:
`canonical.prime_fib(0) == 1`, while `solution.prime_fib(0) == 0`. I accept
`N >= 1` as the intended contract because “N-th” denotes a positive ordinal
and every example starts at one. If the annotation `n: int` were instead read
as an unrestricted all-integer contract, this would be a material narrowing
and the verdict would be `FAIL`; that is not the natural reading of this
prompt.

## 3. Clean proof reconstruction

All execution occurred in `/tmp/audit-work/39-prime-fib-audit`. Only source
artifacts were copied there. Candidate `runtime-kompiled/`,
`verification-kompiled/`, bytecode, caches, traces, and prior logs were not
used. The live toolchain is K v7.1.293.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0. Fresh MPY programs consisting of the exact submitted function plus
one call produced:

| Input | K result | Python generated | Python canonical on intended domain |
|---|---:|---:|---:|
| `1` | `2` | `2` | `2` |
| `5` | `89` | `89` | `89` |
| `0` (excluded) | `0` | `0` | `1` |

The LLVM build and complete final configurations are in
[03_kompile_llvm.log](/audit-output/evidence/03_kompile_llvm.log),
[03_krun_n1.log](/audit-output/evidence/03_krun_n1.log),
[03_krun_n5.log](/audit-output/evidence/03_krun_n5.log), and
[03_krun_n0.log](/audit-output/evidence/03_krun_n0.log).

Fresh proof reconstruction:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. Every declared positive target then closed:

| Target | Independent command result | Evidence |
|---|---|---|
| `SPEC.inner-loop` | `#Top`, exit 0 | [03_kprove_inner.log](/audit-output/evidence/03_kprove_inner.log) |
| `SPEC.outer-loop`, trusting the already closed exact inner claim | `#Top`, exit 0 | [03_kprove_outer.log](/audit-output/evidence/03_kprove_outer.log) |
| `SPEC.prime-fib`, trusting the already closed exact inner and outer claims | `#Top`, exit 0 | [03_kprove_entry.log](/audit-output/evidence/03_kprove_entry.log) |

The staged `--trusted` labels do not leave an unproved assumption: each exact
claim was separately closed before its later use. The full clean driver is
[03_build_and_prove.sh](/audit-output/evidence/03_build_and_prove.sh).

## 4. Adequacy and real-program pinning

The claims mean:

1. `inner-loop`: from the actual internal divisor-loop head, with
   `A >= 0` and `D >= 2`, execution consumes the loop, advances `divisor` to
   some final integer, and leaves
   `is_prime = primeScan(A,D,P)`.
2. `outer-loop`: from the actual internal Fibonacci-loop head, with
   `N >= 1`, `A >= 0`, and `B >= 1`, execution consumes the loop and leaves
   `a = primeFibSearch(N,C,A,B)`. Other final locals are existential because
   this theorem does not claim their values.
3. `prime-fib`: in the fixed initial caller configuration, lookup and call of
   the `prime_fib` closure on arbitrary `N >= 1` returns
   `primeFibSearch(N,0,0,1)` while restoring the caller's environment, scope
   allocator, heap, heap allocator, stack, return state, exception state, and
   exit code.

All preconditions are satisfiable. Concrete witnesses are
`A=8,D=2,P=true` for the inner claim; `N=5,C=0,A=0,B=1` with arbitrary
well-sorted auxiliary locals for the outer claim; and the exact ground entry
configuration with `N=5`. The summary interpretation gives false for the inner
witness and gives 89 for the outer/entry witness. The same 89 is returned by
both Python implementations and fresh LLVM execution; see
[04_summary_witness.log](/audit-output/evidence/04_summary_witness.log).

Real-program pinning is mechanical, not merely visual. The reviewer script
[04_pinning.py](/audit-output/evidence/04_pinning.py):

- recursively expands `primeFibBody`, `primeFibOuter`, and `primeFibInner`;
- parses that expansion and the trusted regenerated `.mpy` with K's parser;
- compares the complete constructor trees;
- verifies that each `#while` anchor differs from its corresponding source
  `While` macro only at the intended internal control constructor; and
- confirms that the entry call selects `"prime_fib"` bound to
  `closureVal("n", primeFibBody, 0)`.

Every comparison is exact and passed; see
[04_pinning.log](/audit-output/evidence/04_pinning.log) and the preserved
[expanded body](/audit-output/evidence/04_macrobody_expanded.txt). Starting
after the module's `FuncDef` is sound here: the module contains only that
definition, and the claim pre-binds the same function name, parameter, defining
environment, and mechanically identical body.

The result is not a free variable or tautology. A fresh body-sensitivity claim
changes the actually executed closure constructor `b = 1` to `b = 3` while
retaining the old destination. It builds, executes to concrete result `3`, and
fails with `WarnStuckClaimState`; see
[04_body_sensitivity.k](/audit-output/evidence/04_body_sensitivity.k) and
[04_body_sensitivity.log](/audit-output/evidence/04_body_sensitivity.log).

There is one non-fatal adequacy limitation. The summary equations are oriented
to fold a reached successor back to its predecessor so loop circularities can
close. Consequently a new diagnostic claim
`primeFibSearch(1,0,0,1) => 2` does not normalize forward and fails on the
opaque ground summary; see
[04_ground_summary.log](/audit-output/evidence/04_ground_summary.log). This is
not a failure of the candidate's positive theorem: the universally proved loop
claims connect actual execution to the summaries. It does mean that the
numeric and human-facing interpretation of the final term is not itself a
second machine-checked K theorem.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[04_inventory.log](/audit-output/evidence/04_inventory.log), generated by
[04_inventory.py](/audit-output/evidence/04_inventory.py). It enumerates every
source syntax declaration, configuration, context, rule, claim, and
attribute-bearing line across the supplied semantics, `verification.k`, and
`spec.k`, with file hashes and per-file counts. In total it found 232 syntax
declaration heads, one configuration, five contexts, 707 rules (695 in the
fixed supplied semantics and 12 local rules), and three claims. It separately
lists every `function`, `total`, `symbol`, `no-evaluators`, priority,
`simplification`, `concrete`, macro, strictness, and `owise` occurrence.

The 695 supplied rules are classified as the immutable trusted language
baseline. This is exactly the tree selected by `SUPPLIED_SEMANTICS`; it is not
candidate-authored proof theory. Every baseline rule exercised by this program
was then path-reviewed. Rules for unused lists, tuples, dictionaries, sets,
strings, floats, comprehensions, methods, sorting, builtins, and assertions
cannot match a reachable program constructor here and contribute no proof
step.

### Used supplied-semantics map

| Program construct | Declaration/effective rules | Review |
|---|---|---|
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll` and statement sequencing | Concrete runs load the module in order. The entry theorem begins from the equivalent exact binding. |
| `Int`, `Bool`, `Name` | `core.k` literal and lexical-scope lookup rules | Every name is bound. Higher-priority cell-reference lookup is disabled because the frame has no `"$cells"` entry. |
| `BinOp` | `syntax.k [seqstrict]`; `operators.k`; `int.k` | Left-to-right evaluation is preserved. `+`, `*`, and `%` use integer rules; `Int + Bool` maps false/true to 0/1 exactly as Python. |
| `Compare`/`CmpOp` | the two `operators.k` contexts and integer comparison rules | Left then right evaluation; `<`, `<=`, `>=`, and `==` have the required mathematical-integer meaning. |
| `Assign` | `syntax.k [strict(2)]`; `controls.k` scope update | RHS evaluates before the current local map is updated. The higher-priority cell-write rule cannot match. |
| `If` | `syntax.k [strict(1)]`; `controls.k` `#branch` rules | The condition is evaluated once and selects exactly one branch. |
| `While` | `controls.k` source-to-`#while`, condition, `truthy`, and `#loopLbl` rules | The condition is reevaluated each iteration; normal continuation is preserved. There is no break, continue, return, allocation, or exception in either loop. |
| `Call`/argument | `call.k`, `core.k #evalArgs`, `functions.k #bindP` | Name lookup selects the pinned closure; the sole argument is evaluated and bound in a newly allocated local frame. |
| `Return`/frame pop | `functions.k` return, `#pop`, and stack-frame rules | The value is evaluated, the function continuation is discarded as Python return requires, the local scope is removed, and caller state is restored. |

The divisor never reaches zero (`2` initially and incremented by one), so the
positive-denominator `pyMod` path matches Python. K integers and CPython
integers are both unbounded for these operations. No heap object is allocated,
no external state is touched, and no exception-producing path is reachable on
the proved domain.

### All 12 local rules

- Five macro rules (`primeFibInner`, `primeFibInnerCore`, `primeFibOuter`,
  `primeFibOuterCore`, `primeFibBody`) are compile-time constructor
  abbreviations. The constructor comparison above proves their exactness.
  They introduce no runtime rewrite, priority, state change, or abrupt control.
- `primeScan` has four simplification equations: loop-exit/base, divisible
  false, non-divisible fold, and false-flag absorption. Each is true over its
  guard. `D >= 2` excludes zero division. The fold decreases the represented
  scan index, and absorption terminates.
- `primeFibSearch` has three simplification equations: exited-loop base,
  just-crossed-boundary result, and one-iteration fold. The fold exactly maps
  `(C,A,B)` to `(C+primeBit(B),B,A+B)` and decreases constructor size in its
  chosen orientation.

Neither local function is declared `total`; there is no local opaque/symbolic
primitive, `functional` declaration, priority, `owise`, concrete rule, or
ordinary operational bridge. All seven non-macro local equations are
`[simplification]` equations over summaries only.

The overlaps are sound:

- `primeScan(...,false)` overlaps other cases only at result false. More subtle
  fold/base and fold/divisor critical pairs are also mathematically equal:
  for example `primeScan(5,3,P)` may fold to `primeScan(5,2,P)` or exit with
  `P`, and both represent `P`; `primeScan(9,3,true)` may return false or fold
  to the scan starting at 2, which is also false.
- `primeFibSearch` base/fold overlap occurs only when a prime bit crosses the
  boundary. The base yields the successor's `A = B`, and the boundary equation
  yields the same `B`. Predecessors of a successor state are unique.

A bounded counterexample search checked all four `primeScan` equations on
7,260 guarded witnesses and the three search equations on 1,273 witnesses,
finding zero counterexamples; see
[04_rule_checks.log](/audit-output/evidence/04_rule_checks.log). This finite
check supports, but does not replace, the static arguments above.

The broad supplied baseline contains 25 named symbolic/opaque-boundary
functions: `md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
`gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`; and `sortVS`, `sortKeyVS`. None occurs in the translated
body, summaries, claims, path conditions, or residuals. The compiler's
non-exhaustive warnings concern similarly unused baseline functions and do not
affect this theorem.

I found no unsound local rule and therefore make no unsoundness allegation
requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
[05_false_n5.k](/audit-output/evidence/05_false_n5.k) uses the satisfiable
ground input `N=5` but changes the required result to `88`. Trusted canonical
Python, generated Python, and fresh LLVM execution all establish the witness
result is 89.

The mutation compiled successfully and reached the proof backend. `kprove`
exited 1 with `WarnStuckClaimState`; its residual contains

```text
88 #Equals primeFibSearch ( 5 , 0 , 0 , 1 )
```

rather than a parser error, timeout, missing import, or unrelated crash. The
exact command and bounded output are
[05_false_n5.log](/audit-output/evidence/05_false_n5.log), driven by
[05_nonvacuity.sh](/audit-output/evidence/05_nonvacuity.sh). The proof is
discriminating and non-vacuous.

## 7. Proven versus assumed accounting

What the K proof establishes is:

> For every K integer `N >= 1`, every terminating execution of the exact
> submitted `prime_fib` closure under the supplied MPY semantics returns
> `primeFibSearch(N,0,0,1)`. The two universal auxiliary theorems establish that
> the actual divisor loop and actual Fibonacci loop have the `primeScan` and
> `primeFibSearch` summaries, respectively.

It does not prove termination, existence of arbitrarily many Fibonacci primes,
behavior for `N <= 0`, non-integer calls, or correctness of unused Python
features.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Exact supplied MPY tree | All K execution and proofs | Authorized fixed semantics; integrity-checked. Its used integer, scope, call, loop, and return rules were path-reviewed. |
| K v7.1.293, Haskell/LLVM backends, SMT solver, and builtin integer/Boolean/map/list hooks | Compilation, execution, symbolic closure | Ordinary proof-tool trust boundary. Fresh cross-backend reconstruction reduces reliance on candidate caches. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte-identical candidate/trusted translator and byte-identical regenerated/submitted MPY provide a mechanical bridge. |
| `primeScan` means primality when called as `primeScan(A,2,A>=2)` | Human contract | Ordinary divisor-pair theorem: every composite `A >= 2` has a divisor no larger than its square root. Correct but not separately formalized in K. |
| `primeFibSearch` means the remaining Fibonacci-prime search | Human contract | Its equations match one Fibonacci update and one `primeScan` bit; the outer reachability theorem connects actual execution to it. The final intent interpretation remains an audited mathematical bridge. |
| Positive-ordinal interpretation `N >= 1` | Entry claim/domain | Natural reading of “N-th” and all examples; the observed `n=0` divergence is explicitly excluded and is a non-fatal scope caveat. |
| Differential `n=1..11`, summary witnesses `n=1,5`, LLVM `n=1,5` | Empirical support only | Reproducible, zero mismatches, and useful for the bridges above; not a universal substitute for the K proof. |
| 25 unused supplied opaque/symbol functions listed in stage 5 | None | They do not influence control, state, result, path condition, or claim closure in this task. |

Gate A passes: the fixed semantics executes the exact body, both loop
connections close, no operational bridge or result oracle exists, the local
equations are truthful, and fresh body/result mutations are rejected.

Gate B passes under the positive-ordinal interpretation: the symbolic domain is
unbounded `N >= 1`, not finitely unrolled, and the summary matches the material
source contract. The `n=0` observation is outside that intended domain.

Gate C is reproducible, but the backward-folding summaries do not normalize
ground initial terms to numerals, so their human-facing interpretation relies
on the stated mathematical bridge and finite independent evidence. Under the
benchmark decision boundary, that is a non-fatal trust/evidence limitation and
therefore `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
