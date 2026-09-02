# Independent adversarial audit: HumanEval 55-fib

## Audit outcome

The candidate contains a legitimate partial-correctness proof for the material
source-contract domain, nonnegative integer Fibonacci indices. I rebuilt both
definitions from source, proved the recursive execution theorem separately,
proved the complete exact-module spec, mechanically matched the claims to fresh
trusted translator output, reviewed every local K declaration and rule, and
rejected fresh body and result mutations.

The proof has the ordinary trust boundary of a generated, task-subset language
semantics: K's standard integer/Boolean/map operations, the K toolchain, the
trusted translator, and the audited correspondence between the small semantics
and the used Python constructs. There is no task-answer oracle, opaque
program-derived result, trusted claim, or execution-bypassing rule.

## Stage 1 — Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, problem `55-fib`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. I used its `container_paths`, not its
host-only provenance paths.

The launcher-owned inputs were intact:

- `/audit-campaign-lock.json` is a real regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
  as recorded in `/audit-input.json`, and its decoded JSON object exactly
  equals the `audit_campaign` block.
- `/run.json`, `/task.json`, and `/generation-result.json` have the recorded
  hashes `16ab5496...`, `23959b85...`, and `1e44e43...`.
- All required `legacy-selected-stage1` records were present, regular,
  readable, and inspected: `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the one-file,
  159-record structured trace. The optional recorded `usage.json` was also
  inspected. Historical runtime metrics are not required for this layout.
- Direct file hashes for the generation records match the invocation and audit
  manifests. In particular, the trace JSONL is `a01fb391...`, the generation
  output is `9919ce17...`, and `usage.json` is `e75e69d4...`.
- An independent pipeline-format tree hash of `/candidate` is
  `2e10edca497d0e4ab9fc79a0f758565f3c0e409c3b2dcceee15b1c5d63ae2af6`,
  exactly the retained/output workspace hash in `invocation.json` and
  `generation-result.json`. The analogous trace tree hash is
  `a5ceb4fa...`, exactly `usage.json`'s `source_trace_sha256`.
- Candidate `prompt.py` and `py2mpy.py` byte-match the trusted mounted files;
  their SHA-256 values are `b99ee738...` and `406485ea...`.
- The trusted canonical hash is the recorded `cddc54d1...`.
- No symlink exists in `/candidate`, `/generation-evidence`, or `/reference`.
  The required proof artifacts `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh` are all regular and readable.

The generated-semantics boundary is correct: neither
`/reference/reference-semantics` nor `/candidate/reference-semantics` exists.
I did not seek or infer a hidden semantics.

The generation trace and prose were treated only as claims. The trace includes
an intermediate experiment using a CLI `--trusted` flag; that experiment is
irrelevant to the submitted theorem because the final sources and `prove.sh`
contain no trusted marker or trust flag, and the clean audit proof below uses
none.

Evidence:

- `evidence/01_integrity_check.sh` and `01_integrity_check.log`
- `evidence/01_generation_record_summary.py`,
  `01_generation_record_summary.sh`, and `01_generation_record_summary.log`

Stage 1 result: PASS. There is no infrastructure breach.

## Stage 2 — Program fidelity and canonical comparison

### Source contract

The trusted prompt requires entry point `fib(n: int)` to return the n-th
Fibonacci number, with examples `fib(10)=55`, `fib(1)=1`, and `fib(8)=21`.
The trusted canonical implementation defines the standard nonnegative
sequence:

- `F(0) = 0`
- `F(1) = 1`
- `F(n) = F(n-1) + F(n-2)` for `n > 1`

The candidate uses the equivalent nonnegative-domain implementation
`if n <= 1: return n; else return fib(n-1)+fib(n-2)`. This is a different
branch spelling but the same algorithmic recurrence on every intended input.

The formal `N >= 0` domain is not a material narrowing. “n-th Fibonacci
number” conventionally has nonnegative indices here, and the trusted canonical
has no normal result for a negative integer: it recurses until Python raises
`RecursionError`. The generated implementation happens to return `n` for
negative inputs, but those extra behaviors are outside the canonical
normal-return contract and are not claimed by the theorem.

### Trusted regeneration

In the clean scratch tree I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp submitted-solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`f0b3bfa90a88ce6cdfe7aaed7d6cce9463433792a6efbdb09677369f13c301e1`;
`cmp` exited 0. Thus the submitted `.mpy` is byte-identical to output from the
trusted translator.

### Independent differential

`evidence/02_differential.py` independently imports the trusted canonical and
generated entry points and compares both with a separately implemented
iterative Fibonacci oracle. It covers the documented examples, branch
boundaries `0,1,2`, every input `0..12`, and deterministic generated
representatives through `20`. All 18 distinct inputs matched and the script
exited 0. An empty case is inapplicable to this scalar integer interface.

Evidence:

- `evidence/02_translation_check.sh` and `02_translation_check.log`
- `evidence/02_differential.py` and `02_differential.log`

Stage 2 result: PASS.

## Stage 3 — Clean proof reconstruction

I copied only candidate source artifacts and trusted inputs to
`/tmp/audit-work/55-fib-independent-audit`. I copied no candidate-built
definition, cache, proof output, or `spec.json`.

Observed tools were Python 3.10.12 and K 7.1.293. I made distinct concrete and
proof builds:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-proof-kompiled
```

Both commands exited 0. The fresh LLVM definition executed the fresh trusted
translation as follows:

| ARG | K result | generated Python | trusted canonical |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 |
| 8 | 21 | 21 | 21 |
| 10 | 55 | 55 | 55 |
| 12 | 144 | 144 | 144 |

Every `krun` exited 0 and reached an integer followed by `.K`; this covers both
guard outcomes, the zero-recursion boundary, and recursive execution.

I then ran the recursive connection claim independently:

```text
kprove spec.k --definition verification-proof-kompiled \
  --spec-module SPEC --claims SPEC.fib-invoke --output pretty
```

It exited 0 and printed exactly `#Top`. Finally I ran the complete proof file,
which includes both positive claims:

```text
kprove spec.k --definition verification-proof-kompiled \
  --spec-module SPEC --output pretty
```

It also exited 0 and printed exactly `#Top`. No candidate cache, compiled
definition, prior `#Top`, or trust flag contributed.

Evidence:

- `evidence/03_rebuild_and_run.sh` and `03_rebuild_and_run.log`
- `evidence/03_kompile_concrete.log` and `03_kompile_proof.log`
- `evidence/03_krun_n{0,1,2,8,10,12}.log`
- `evidence/03_kprove_fib_invoke.log` and
  `03_kprove_all_claims.log`

Stage 3 result: PASS.

## Stage 4 — Adequacy and real-program pinning

### Claims in plain language

`SPEC.fib-invoke` says: for every integer `N >= 0`, given the exact singleton
`fib` binding and its exact submitted body, executing `invoke("fib",N)` returns
`fibMath(N)` before an arbitrary continuation `REST`. The external argument,
arbitrary saved environment, exact function map, and continuation are
preserved. Its precondition is satisfiable; for example, take `N=0`, `<arg> 0`,
`<env> .Map`, the displayed singleton function map, and `REST=.K`.

`SPEC.fib-module` says: for every integer `N >= 0`, starting with the exact
submitted module, `<arg>N`, empty environment, and empty function map, the
module loads that exact binding, invokes the required entry point, and returns
`fibMath(N)`. A witness is `N=0` with the displayed empty initial cells.

Both destinations constrain the actual `<k>` result to the same `N`'s
`fibMath(N)`. There is no fresh result variable, tautological `ensures`,
implication-only target, or omitted result cell.

Concrete substitution agrees across all three meanings:

| Satisfying N | Claimed `fibMath(N)` | generated Python | canonical Python |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 |
| 10 | 55 | 55 | 55 |

### Mechanical program identity

I freshly parsed `regenerated-solution.mpy` with `kast`, freshly emitted the
spec KAST with `kprove --dry-run`, and compared constructor objects:

- parsed program hash:
  `7b322429a99307ad114e61d7d49064793138ea0d1c87c4de294c2eefe6d3a914`
- `fib-module` left-hand program hash: the same value
- parsed function-body hash:
  `a66dfa49304803f03f2a2688d8046bdf1a8d16d9405a8cf32fe499fc0bb718de`
- the body in `fib-invoke` and the function-map destination in `fib-module`:
  the same value

All three object-equality checks were true. Type annotations omitted by the
trusted translator are typing-only for this function; no material operation,
binding, or control construct was normalized away.

### Control and body sensitivity

A fresh, bridge-free ground claim executed `invoke("fib",5)` in fixed semantics
with saved environment `"sentinel" |-> 42`, `<arg>99`, and an immediate
observable continuation `applyBin("+",100)`. It proved destination `105` with
`#Top`, demonstrating return-value propagation, environment restoration,
argument preservation, and continuation preservation.

For body sensitivity I generated a translated mutant whose executed base case
is `return n + 1`. Its program KAST hash
`997f925e129e605552914b053adb5dcaa55d2dbb48c999c6159dc0a47b0d1c2c`
differs from the original. A mechanical check established that this exact
mutated term—not merely an external source file—is the left side of the
mutation claim. The claim builds, then `kprove` exits 1 with
`WarnStuckClaimState`; at `ARG=0` it reaches result `1` instead of
`fibMath(0)=0`.

Evidence:

- `evidence/04_constructor_pinning.py`,
  `04_constructor_pinning.sh`, and `04_constructor_pinning.log`
- `evidence/05_context_and_body_sensitivity.sh` and its log
- `evidence/05_context_dry_run.log` and `05_context_proof.log`
- `evidence/05_body_mutation_compare.py`,
  `05_body_mutation_dry_run.log`, and `05_body_mutation_proof.log`

Stage 4 result: PASS.

## Stage 5 — Rule-by-rule static soundness review

The exhaustive inventory is in `evidence/05_rule_inventory.md`, backed by
line-numbered extraction in `evidence/05_static_extract.log`. It covers:

- 28 local syntax/configuration/control/result declarations;
- 24 operational rules in `semantic.k`;
- the `fibMath` function declaration and both equations;
- both reachability claims;
- the absence of every local `total`, `functional`, `simplification`,
  `concrete`, `trusted`, priority, `owise`, and opaque declaration.

### Construct coverage

| Submitted construct | Declaration | Execution rules |
|---|---|---|
| module and statement sequence | `Program`, `Stmts` | R1-R3 |
| one-parameter `fib` definition | `FuncDef`, `Params`, `function` | R4-R5 |
| integer and local `n` | `Int`, `Name` | R6-R7 |
| `+` and `-` | `BinOp` | R8-R11 |
| `n <= 1` | `Compare`, `CmpOp` | R12-R14 |
| `if` | `If`, `finishIf` | R15-R17 |
| direct recursive call | `Call`, `prepareCall`, `invoke`, `functionEnd` | R18-R20, R24 |
| return/unwind | `Return`, `makeReturn`, `returned` | R21-R24 |

Every constructor in the trusted translator output is declared and has the
needed rule path. Missing semantics for unused Python constructs is allowed in
`GENERATED_SEMANTICS` mode and is not a defect.

### Evaluation, state, and control

R8-R9 and R12-R13 impose left-to-right operand evaluation. R17 evaluates the
guard before selecting one of the disjoint Boolean rules R15/R16. R18 evaluates
the call argument before function lookup/invocation. These match the used
Python expressions.

The only authored state changes are function registration (R4), replacement
of locals while saving the complete caller map in `functionEnd` (R20), and
restoration of that exact map (R24). R23 discards pending statement-list
continuations after `return`; the `functionEnd` delimiter prevents it from
crossing into caller control. The function map, external argument, and caller
continuation are preserved. There is no heap, I/O, mutation, exception,
closure, or other state in the submitted program that needs a cell.

K integers implement the used arbitrary-precision integer `+`, `-`, and `<=`.
Map lookup/insertion supplies the only local and function bindings. Unsupported
operators, missing names, malformed call shapes, or absent returns remain
visibly stuck rather than fabricating a result.

### Proof extensions

`fibMath` is a definitional summary, not an operational bridge. Its base
equation applies exactly on `0 <= N <= 1`; its recurrence applies exactly on
`N > 1`. The guards are disjoint, cover all proved inputs, and the recurrence
strictly descends to a base case. It is deliberately not declared total, so
uncovered negative values receive no fabricated equation.

`fib-invoke` is the bridge-free universal connection theorem from the exact
fixed-semantics invocation configuration to `fibMath`. It was proved
independently. Its match domain includes the full exact function binding,
arbitrary saved environment, arbitrary `<arg>`, and arbitrary continuation;
its destination preserves every cell and that continuation. It may then act as
a proved recursive circularity/helper for `fib-module`; it is not an ordinary
rule in `verification.k` and does not preempt fixed execution.

No inventoried rule encodes a task answer, introduces an unconstrained value,
bypasses the function body, overlaps inconsistently, or claims false totality.
Accordingly there is no unsound-rule allegation requiring a false-conclusion
witness. The fresh negative witnesses in Stages 4 and 6 test sensitivity, not
an alleged semantic unsoundness.

Evidence:

- `evidence/05_rule_inventory.md`
- `evidence/05_static_extract.sh` and `05_static_extract.log`

Stage 5 result: PASS.

## Stage 6 — Fresh non-vacuity mutation

I ignored the candidate's mutation as proof and authored
`false-result-spec.k` in scratch. It executes the exact real submitted module
at the satisfying input `ARG=2` but changes the result obligation to
`fibMath(2)+1 = 2`. Independent Python execution establishes that the real
generated function returns `1`, so the mutation is concretely false.

First I ran:

```text
kprove false-result-spec.k --definition verification-proof-kompiled \
  --spec-module FALSE-RESULT-SPEC --dry-run --output none
```

It exited 0, so the mutation parses and builds. I then ran the same command
without `--dry-run` and with `--output pretty`. It exited 1 with
`WarnStuckClaimState`; the residual is the fully executed actual configuration
with `<k> 1 ~> .K </k>`, `ARG=2`, empty restored environment, and the exact
loaded submitted body. The failure is the intended unmet result obligation,
not a parser error, missing import, timeout, or unrelated crash.

Evidence:

- `evidence/06_false_result_mutation.sh` and
  `06_false_result_mutation.log`
- `evidence/06_false_result_dry_run.log` and
  `06_false_result_proof.log`

Stage 6 result: PASS.

## Stage 7 — Proven-versus-assumed accounting

### Precisely proven

Under the freshly built `SEMANTIC` operational semantics and the two truthful
`fibMath` equations, for every K integer `N >= 0`:

1. invoking the exact registered body translated from the submitted
   `solution.py` reaches `fibMath(N)`, preserves an arbitrary caller
   continuation and `<arg>`, and restores an arbitrary caller environment; and
2. executing the exact submitted translated module from its initial empty maps
   loads that exact body and reaches `fibMath(N)`.

This is a result-constraining, all-path K reachability proof. In Kit terms it is
a partial-correctness theorem; it does not make a separate resource-bounded
CPython termination guarantee.

### Trust and assumption ledger

| Boundary | Influence | Dependents | Judgment/evidence |
|---|---|---|---|
| K 7.1.293 parser, compiler, LLVM executor, Haskell prover | Parsing, execution, proof closure | All K results | Ordinary low-level trust boundary; two independent fresh builds and actual exit/output logs. |
| K standard `INT`, `BOOL`, `MAP`, list, sequencing, and cell machinery | Integer values/operations, guards, environments, syntax lists, control | All rules and claims | Acceptable fixed primitives; no task-specific result is hidden in them. |
| Trusted `/reference/py2mpy.py` | Python AST to constructor term | Program identity | Launcher-trusted input; submitted term is byte-identical to fresh output and claims are constructor-identical to that output. |
| Generated subset semantics versus idealized Python behavior | Meaning of the used constructors | Real-program adequacy | Audited rule by rule; direct binding/order/control/state comparison plus K/Python boundary and recursive concrete tests. No used construct is abstracted or skipped. |
| `fibMath`'s standard recurrence denotes “n-th Fibonacci number” | Human-facing result meaning | Both postconditions | Equations are explicit, disjoint, descending, and the standard mathematical definition; concrete canonical/iterative differentials give finite corroboration. |
| Intended domain is nonnegative integers | Theorem scope | Both claims | Supported by the phrase “n-th Fibonacci,” the `0/1` canonical bases, and the absence of any canonical normal result for negative inputs. This is not a finite-size restriction. |
| Idealized execution omits CPython recursion/resource limits and non-integer misuse | Exceptional/resource behavior only | Comparison with a concrete runtime | Acceptable for the requested partial-correctness theorem; no normal returned Fibonacci result in the material domain is changed. These behaviors are not claimed. |

There is no opaque symbol, empirical value oracle, proof-local operational
rewrite, trusted claim, hidden lemma, or unproved program-body summary.
Differential tests support only the finite Python/semantics correspondence they
exercise; they are not presented as the universal K proof.

### Validation gates and decision

- Gate A, real-program soundness: PASS. Fixed execution is exact and
  constructor-pinned; the connection claim closes independently; context,
  body, and false-result sensitivity checks all behave correctly.
- Gate B, intent adequacy: PASS. The theorem covers every nonnegative integer,
  not fixed examples or a bounded unrolling, and its recurrence is exactly the
  source contract.
- Gate C, trust/evidence auditability: PASS. Assumptions are explicit and all
  commands, inputs, exits, and bounded outputs are preserved under
  `/audit-output/evidence`.

Overall, the reconstructed proof is sound, non-vacuous, result-constraining,
and mechanically pins the real generated program over the material HumanEval
domain. The benchmark mapping is therefore `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
