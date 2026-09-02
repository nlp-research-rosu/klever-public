# Independent adversarial review: 24-largest-divisor

This review applies the required seven stages in order. All candidate prose,
compiled definitions, caches, logs, traces, and prior `#Top` results were
treated as untrusted claims. Execution used a source-only copy under
`/tmp/audit-work/audit-24`; no candidate-provided kompiled directory was used.

The reconstructed proof is legitimate. It proves partial correctness for the
meaningful HumanEval domain `n >= 2`, pins the exact translated function body,
and constrains the result to a transparent descending-divisor specification.
I found no operational bridge, result oracle, false proof-local equation, or
material domain narrowing.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `24-largest-divisor`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `pipeline-v3`;
- a mounted trusted reference-semantics tree.

All pipeline-v3 required files were readable real regular files, and all
required roots were real directories. The full list checked includes
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all seven required generation records, the
structured trace, the three trusted source inputs, `/candidate`, and both
semantics trees. Recursive scans found no symlink or unsupported entry in the
trees relevant to integrity. See
[stage1-integrity.log](evidence/stage1-integrity.log).

The campaign object embedded in `/audit-input.json` is exactly equal as a JSON
object to `/audit-campaign-lock.json`. The independently observed lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded hash.

Every recorded regular-file digest checked independently matched, including:

- run, task, result, invocation, generation metrics, runtime metrics, usage,
  prompt, Codex output, and Codex last-message records;
- trusted canonical, prompt, and translator;
- the candidate prompt and translator.

The pipeline-v3 tree digest of the mounted candidate is
`553cb747ae25e84a0f158de85a6460c20dac1dca647d7b44346e3a9d61f94573`,
exactly the `workspace_sha256` in `/generation-result.json`. The trace tree
digest is
`d63b866280e18b1c199616f3e0a3ca5b98076ab81f766e4aafdec3b6243cdb8f`,
exactly `usage.json`'s `source_trace_sha256`. The audit-input also carries
launcher snapshot identifiers made with an undeclared alternate encoding;
the independently reproducible pipeline digests, individual file hashes, and
recursive byte/type comparisons are the checks used here.

The embedded audit manifest differs from `/task.json` only by the audit
launcher’s added `config` key. The task file itself matches its recorded hash,
and condition, problem, inputs, result, invocation, and generation evidence
are mutually consistent. Generation status records say exit 0, no OOM, and no
timeout; those remain provenance claims rather than proof evidence.

### Supplied-semantics boundary

`/reference/reference-semantics` is present, as required for
`SUPPLIED_SEMANTICS`. Candidate and trusted trees each contain exactly 25
entries. Relative paths, entry types, sizes, and SHA-256 file digests are
identical; there are no missing, additional, changed, mistyped, or symlinked
entries. Both pipeline tree digests are
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
Candidate `prompt.py` and `py2mpy.py` are also byte-identical to their trusted
mounts.

The full 259-record structured trace was JSON-parsed, and all 652,029 bytes of
`codex-output.log` were read. The trace contains the original invocation,
tool calls, generated patches, claimed proof runs, and final report. They were
used only to understand provenance. A bounded action summary is in
[generation-trace-summary.log](evidence/generation-trace-summary.log); none of
its claimed results were accepted without reconstruction.

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

`/reference/prompt.py` asks `largest_divisor(n: int) -> int` to return the
largest number that evenly divides `n` and is smaller than `n`; the documented
example is `15 -> 5`. `/reference/canonical.py` scans downward from `n - 1`
and returns the first divisor.

The meaningful positive-proper-divisor domain is `n >= 2`. For `n = 1` no
positive proper divisor exists and the canonical program reaches division by
zero; for nonpositive inputs the stated positive-divisor problem has no
contract result. Thus the claim precondition `N >=Int 2` expresses the
contract’s defined domain rather than materially narrowing it.

Candidate `/candidate/solution.py` implements the same descending scan with:

```python
divisor = n - 1
while n % divisor != 0:
    divisor = divisor - 1
return divisor
```

For `n >= 2`, `divisor` stays positive, decreases after each failed test, and
must reach `1`. The first successful test is therefore the largest positive
proper divisor.

### Trusted regeneration

The trusted `/reference/py2mpy.py` regenerated the candidate program in
scratch. The regenerated and submitted `solution.mpy` are byte-identical and
share SHA-256
`dfeae40e927213369b88e91ab649f8cceb179f11256be1094e3ec8a8b8673a06`.
The exact command and exit 0 are in
[translator-regeneration.log](evidence/translator-regeneration.log).

### Independent differential test

The reviewer-authored
[differential_independent.py](evidence/differential_independent.py) imports
both trusted `canonical.py` and generated `solution.py`. Its independent
oracle computes `n / least_prime_factor(n)`, rather than reusing the descending
algorithm. It also executes the two proof-summary equations.

Coverage was:

- the documented example;
- minimum valid input `2`;
- loop boundaries `2` (zero iterations), `3` and `4` (one iteration);
- primes, composites, squares, and prime powers;
- every integer from 2 through 2000;
- 256 deterministic generated draws from `[2, 10000]`.

There were 2,201 unique inputs and zero mismatches among canonical, generated,
proof summary, and independent oracle. The deterministic input scope and hash
are recorded in
[differential-independent.log](evidence/differential-independent.log).
An “empty” case is inapplicable because the function takes one integer.

## 3. Clean proof reconstruction

Only candidate source artifacts needed for execution were copied. Trusted
prompt, translator, and reference semantics were copied from `/reference`.
Candidate `runtime-kompiled`, `verification-kompiled`, `__pycache__`, and all
other candidate caches were excluded.

### Concrete definition

The fresh LLVM build command was:

```text
kompile --backend llvm reference-semantics/semantics.k
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX
  --output-definition audit-runtime-kompiled
```

It exited 0. Warnings concern non-exhaustive total functions in unrelated
float/list helpers and unused variables in `str.k`; none is reached by this
integer program. Exact output is in
[kompile-llvm.log](evidence/kompile-llvm.log).

A reviewer concrete program used the exact function body and asserted results
for 15, 2, 3, 4, 7, 49, and 100. Translation is recorded in
[concrete-translate.log](evidence/concrete-translate.log). Fresh `krun`
finished with `.K`, empty stack, `noRet`, `NoExc`, and exit code 0; see
[krun-concrete.log](evidence/krun-concrete.log). Running submitted
`solution.mpy` itself produced the exact closure later pinned by the claim;
see [krun-solution-load.log](evidence/krun-solution-load.log).

### Proof definition and claims

The fresh Haskell command was:

```text
kompile --backend haskell verification.k
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
  --output-definition audit-verification-kompiled
```

It exited 0; see [kompile-haskell.log](evidence/kompile-haskell.log).

The loop claim was run alone:

```text
kprove spec.k --definition audit-verification-kompiled
  --spec-module SPEC --claims SPEC.loop-invariant
```

It printed `#Top` and exited 0:
[kprove-loop-invariant.log](evidence/kprove-loop-invariant.log).

The required all-claims target was then run:

```text
kprove spec.k --definition audit-verification-kompiled
  --spec-module SPEC
```

It printed `#Top` and exited 0:
[kprove-all-claims.log](evidence/kprove-all-claims.log). This invocation proves
both the circularity and entry target together, which is required because the
entry proof uses the loop claim.

As a diagnostic, selecting only `SPEC.largest-divisor` was interrupted after
approximately 112 seconds with no output: label selection had excluded the
needed loop circularity. This is not a failed target-proof command; a helper
claim need not be reproved by unbounded loop unrolling after being removed
from the selected spec. The bounded diagnostic is preserved in
[kprove-largest-divisor.log](evidence/kprove-largest-divisor.log). The
whole-spec proof is the relevant independent reconstruction and closed in
under five seconds.

Fresh concrete entry claims `15 -> 5` and `2 -> 1` also printed `#Top` and
exited 0 without using the symbolic loop circularity:
[kprove-concrete-witnesses.log](evidence/kprove-concrete-witnesses.log).

The dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` says: for any `N >= 2`, `D >= 1`, and saved caller
continuation `CONT`, begin at the real internal `#while` for the submitted
condition/body with locals `n=N`, `divisor=D`, the exact submitted closure,
the exact live call frame, and every configuration cell fixed. Executing the
loop, real return, and frame pop yields
`largestDivisorAtOrBelow(N,D) ~> CONT`, removes the callee scope/frame, and
restores the caller environment and scope counter.

`SPEC.largest-divisor` says: for any unbounded mathematical integer `N >= 2`,
call the exact module binding `largest_divisor(N)` from a post-module-load
state. If execution terminates, the returned value is
`largestDivisorAtOrBelow(N,N-1)`, with heap, counters, stack, return,
exception, exit-code, and module state preserved or restored as specified.

### Mechanical source pinning

The reviewer script [pinning_check.py](evidence/pinning_check.py) uses K’s
parser on submitted `solution.mpy` and on the `closureVal` extracted directly
from the entry claim. It unwraps the parsed `Module/FuncDef/Params` term and
compares the parameter and body KAST trees to the claim binding. The result:

```text
trusted_regeneration_byte_equal=True
function_name="largest_divisor"
parameter_constructor_equal=True
body_constructor_equal=True
claim_defining_location=0
entry_k_executes_named_call=True
entry_result_constrained_to_summary=True
```

See [pinning-check.log](evidence/pinning-check.log). Type annotations are the
only source-level material absent from the constructor term, and they are
semantically inert for this implementation. The module-load run independently
shows that fixed semantics creates the same binding/body. This satisfies the
allowed post-load constructor normalization; the proof does not substitute a
different program.

### Satisfiability and result constraint

An entry witness is `N=15` with the exact claim cells: env 0; builtins at -1;
the parsed closure at module scope 0; scopeLoc 1; empty heap and stack; no
return or exception; exit code 0. `15 >= 2`, so the precondition is
satisfiable. The formal result becomes `largestDivisorAtOrBelow(15,14)=5`;
trusted canonical and generated Python both return 5.

A loop witness is `N=15`, `D=14`, `CONT=.K`, locals at scope 1, and the exact
single saved frame shown in the claim. Both helper preconditions hold, and
the summary/result is 5. At the formal boundary `N=2`, the target summary is
`largestDivisorAtOrBelow(2,1)=1`, also matching both Python programs and the
fresh concrete K claim.

The result is neither a free variable nor a tautology. Its two equations fix a
unique value on every used input.

### Body sensitivity

`spec-body-mutation.k` changes the closure term actually executed by the claim:
the return becomes `divisor - 1` while the demanded result remains 5 for
input 15. It parsed successfully, then fixed semantics terminated at concrete
result 4 and `kprove` exited 1 with `WarnStuckClaimState`. See
[body-mutation-dry-run.log](evidence/body-mutation-dry-run.log) and
[body-mutation-kprove.log](evidence/body-mutation-kprove.log). This is a
proper body mutation, not an external source-file edit disconnected from the
claim term.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [rule_inventory.py](evidence/rule_inventory.py) parsed
all supplied K files plus `verification.k` and `spec.k`. The resulting
[rule-inventory.tsv](evidence/rule-inventory.tsv) contains source location,
complete escaped source sentence, classification, attributes, relevance,
decision, and rationale for each of 933 top-level items:

| Item | Count |
|---|---:|
| Syntax declarations | 228 |
| Ordinary rules | 697 |
| Contexts | 5 |
| Configuration | 1 |
| Claims | 2 |

The rules comprise 459 equational and 238 operational rules. Attribute counts
include 149 function declarations, 107 total declarations, 46 priority
occurrences, 26 `owise`, 36 concrete rules, 25 symbol declarations, and 22
`no-evaluators`. There are no `functional`, `simplification`, `anywhere`, or
proof-local priority/total/opaque declarations. Per-file counts and every
opaque record are in
[rule-inventory-summary.log](evidence/rule-inventory-summary.log).

Because this is `SUPPLIED_SEMANTICS`, every fixed-semantics inventory item is
also byte-identical to the trusted selected semantics. Unused items were not
silently ignored: each is inventoried and marked unreachable because its
constructors, dispatch name, or value sort cannot arise from this program or
its claims. No unreachable fixed rule can overlap the exact integer-loop
redexes. No false-conclusion witness was found for an item in the dependency
slice, so no rule is labeled unsound.

### Used construct map and operational review

[used-construct-map.tsv](evidence/used-construct-map.tsv) maps every submitted
constructor—`Module`, `FuncDef`, `Params`, statement sequencing, `Assign`,
`Name`, `Int`, `BinOp("-")`, `BinOp("%")`, `Compare/CmpOp("!=")`, `While`,
`Return`, and the entry `Call`—to exact declarations and rules.

The material path is sound:

- configuration and module load create module scope 0 and the exact closure;
- lookup follows the pinned scope chain, with local `n`/`divisor` present;
- strictness/contexts give left-to-right integer operand and argument
  evaluation;
- call setup allocates scope 1, binds `n`, saves `CONT`, and appends
  `#endcall`;
- assignment changes only current-scope `divisor`;
- while reevaluates its guard and returns through the same loop head;
- positive-divisor `pyMod` equals Python floored modulo and never divides by
  zero under `D>=1`;
- return discards only the callee suffix, records the value, then frame pop
  restores caller control/environment and deallocates the callee scope;
- no heap, output, exception, or allocation behavior is abstracted.

Higher-priority cell/reference rules have guards or value constructors
disjoint from the exact plain integer frame. Generic `owise` call/operator
rules dispatch only after the concrete applicable cases. The claims pin the
continuation, stack, binding, and every observable cell, so there is no
broadened operational bridge context.

### Proof-local extension review

`verification.k` contributes exactly one function declaration and two rules:

```text
L(N,D) = D        if D>=1 and pyMod(N,D)=0
L(N,D) = L(N,D-1) if D>1  and pyMod(N,D)!=0
```

This is a definitional mathematical summary, not an operational bridge: no
program constructor or cell appears on either left-hand side.

The guards are disjoint. For `D>1`, integer remainder is either zero or
nonzero, so one rule applies. At `D=1`, `pyMod(N,1)=0`, so the base rule
applies. Recursion strictly decreases positive `D`; no false totalization
outside the used domain is asserted because the symbol is not `[total]`.

For `N>=2` and `1<=D<N`, elementary induction on `D` establishes that
`L(N,D)` is the greatest positive `d<=D` dividing `N`: if `D` divides `N`,
maximality is immediate; otherwise every divisor at most `D` is at most
`D-1`, and the induction hypothesis applies. Setting `D=N-1` gives exactly
the prompt’s largest positive proper divisor. This is a transparent
mathematical interpretation of complete equations, not an unconstrained
oracle or task-answer rewrite.

`SPEC.loop-invariant` is an auxiliary reachability circularity over fixed
execution. It adds no ordinary rule and matches exact loop/call state.
`SPEC.largest-divisor` is the target. The fresh `#Top`, false-result residual,
and body residual jointly show that neither claim closes vacuously.

### Opaque and total symbols

The supplied proof definition imports 25 fixed-semantics symbol abstractions:
`md5hexCodes`; `sortVS`; `sortKeyVS`; and the float-domain symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.

None appears in `solution.mpy`, the claim binding/body, the preconditions, the
summary, or any reached dispatch. They influence neither control nor result.
Compiler warnings about unrelated non-exhaustive total helpers likewise have
no dependency on this theorem. There is no candidate proof-local opaque
symbol.

The static soundness gate passes.

## 6. Fresh non-vacuity test

Candidate `spec-vacuity.k` was inspected only as untrusted evidence. The
reviewer instead created a different persistent mutation:
[spec-audit-false.k](evidence/spec-audit-false.k).

Its exact executable closure is unchanged, and its valid witness is `n=49`.
The result-constraining postcondition is deliberately changed from the true
result 7 to false result 8.

First:

```text
kprove spec-audit-false.k --definition audit-verification-kompiled
  --spec-module SPEC-AUDIT-FALSE --dry-run
```

exited 0 and emitted the backend command, proving the mutation parsed and
built; see
[false-mutation-dry-run.log](evidence/false-mutation-dry-run.log).

The real proof command then exited 1 with `WarnStuckClaimState`. Its terminal
residual contains `<k> 7 ~> .K </k>`, which does not unify with target 8:
[false-mutation-kprove.log](evidence/false-mutation-kprove.log). This is the
expected unmet result obligation, not a parser error, timeout, backend crash,
or unreachable mutation.

The fresh non-vacuity gate passes.

## 7. Proven versus assumed accounting

### Formally established by K

Under the supplied `MPY` definition, for every unbounded K integer `N>=2`, if
the exact submitted `largest_divisor` call terminates from the pinned
post-module-load configuration, it returns
`largestDivisorAtOrBelow(N,N-1)`. The proof includes actual lookup, argument
evaluation, parameter binding, assignment, every loop test and decrement,
return, caller-continuation restoration, scope cleanup, and all specified
cells. The loop result is universally connected to the summary by the
machine-checked circularity.

### Independently established ordinary mathematics

The complete, guarded summary equations define the first divisor found while
descending from `D`. The induction in Stage 5 shows that, at `D=N-1`, this is
the largest positive proper divisor. This bridge is not an empirical guess,
name-based assertion, or fresh interpretation; it follows directly from the
equations used in the K theorem.

### Trusted boundaries

- K v7.1.293, its Haskell/LLVM implementations, builtin integer/Boolean/map/
  list theories, and host execution are trusted proof infrastructure.
- The mounted supplied semantics is the selected fixed execution model. Its
  candidate copy is byte-identical; the dependency slice was additionally
  reviewed rule by rule.
- The trusted translator is the syntactic Python-to-constructor boundary.
  Byte regeneration plus KAST identity validates this artifact instance;
  translator correctness in general is outside the K theorem.
- Python/K agreement for unbounded integer subtraction, positive-divisor
  modulo, comparison, and truthiness is an accepted low-level model boundary.

These boundaries are acceptable here: none injects the task answer, skips
program-defined computation, or leaves a result-bearing value unconstrained.
All supplied opaque abstractions are unreachable.

### Empirical support only

The 2,201-input differential run, concrete `krun` assertions, concrete K
witness claims, and negative probes support the translator/model/intent
bridges on their stated finite scopes. They are not used as substitutes for
the universal K proof.

### Excluded conclusions

- The theorem is partial correctness, not a K liveness theorem. Separately,
  ordinary descent to divisor 1 establishes termination for `n>=2`.
- Inputs below 2 are outside the defined positive-proper-divisor contract.
- Unused Python constructs and full CPython behavior outside the supplied
  subset are not proved.
- No candidate `PROOF.md`, compiled definition, generation trace, or prior
  output is part of the trust argument.

The reviewer evidence set is checksummed in
[evidence-manifest.log](evidence/evidence-manifest.log).

All three Kit validation gates pass: real-program soundness, intent adequacy,
and evidence auditability. The proof covers the full material contract domain
and has no material adequacy or trust-boundary limitation.

VERDICT: PASS
LEGITIMACY: LEGIT
