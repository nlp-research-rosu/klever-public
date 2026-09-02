# Independent adversarial audit: 114-minSubArraySum

## Outcome

**CONCERNS / LEGIT.** The candidate contains a freshly reproducible,
result-constraining partial-correctness proof of the submitted translated
program under its generated K semantics. The proof executes the program bodies;
it does not replace either recursive function with an oracle. The translated
program is pinned both by byte-identical regeneration and by a successful
auxiliary claim whose left side directly embeds the translated `Module` term.
The proof rejects both a false postcondition and a reachable body mutation.

The concern is a material but non-fatal intent/semantics bridge limitation. The
prompt allows every non-empty integer list, while the real CPython candidate is
recursive and raises `RecursionError` on a valid 1,100-element list for which
the trusted iterative canonical implementation returns `1`. The K semantics
has unbounded call depth and no exception semantics. Thus the formal result is
a legitimate partial-correctness theorem for normal returns in the modeled
language, not a total-correctness or full CPython-behavior theorem for every
prompt-domain list.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. Both
`/reference/reference-semantics` and `/candidate/reference-semantics` are
absent, as required. The trusted inputs are regular files, the K tools are
independently installed, and K reports version 7.1.293. There is no mode/mount
contradiction and therefore no infrastructure breach. See
[00_environment.log](/audit-output/evidence/00_environment.log).

### Required artifacts and provenance

All of the following candidate artifacts exist as regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
structured JSONL trace, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
There are no symlinks anywhere under `/candidate`. The complete type inventory
is in [01_provenance.log](/audit-output/evidence/01_provenance.log).

The candidate prompt is byte-identical to
[the trusted prompt](/reference/prompt.py), SHA-256
`4bdb0afd53bc0e28529bafba0538d6b3a566ad5f476fb7f1016cfabe823f1c3f`.
The candidate translator is byte-identical to
[the trusted translator](/reference/py2mpy.py), SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
No required source artifact is missing, changed, mistyped, or symlinked.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. These are additional generated
caches, not source integrity failures. They were treated as untrusted and were
not copied into the scratch reconstruction.

`run-input.json` claims problem `114-minSubArraySum`, condition `bare`, with no
supplied semantics; `metrics.json` claims a successful, non-timeout generation.
The prose/log/trace claim that 19,607 Python cases passed and `kprove` produced
`#Top`. These were not relied upon. Hashes, bounded excerpts, the trace record
inventory, and all such untrusted claims are preserved in
[01b_untrusted_claims.log](/audit-output/evidence/01b_untrusted_claims.log);
the trace parser is
[untrusted_trace_summary.py](/audit-output/evidence/untrusted_trace_summary.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `minSubArraySum(nums)` to return the least sum of
any non-empty contiguous subarray of a non-empty integer list. Its examples are
`[2,3,4,1,2,4] -> 1` and `[-1,-2,-3] -> -6`.

The [trusted canonical implementation](/reference/canonical.py) applies
Kadane's method to negated values and returns the negative of the maximum
negated subarray sum. The special all-positive case selects the least element.
It is defined only for non-empty lists; its generator `max` raises `ValueError`
on `[]`.

The [candidate implementation](/candidate/solution.py) uses two recursive
functions:

- `min_prefix_sum([H]) = H`; otherwise it returns the smaller of `H` and
  `H + min_prefix_sum(tail)`.
- `minSubArraySum([H]) = H`; otherwise it returns the smaller of the best
  subarray wholly in the tail and the best prefix beginning at `H`.

These equations are mathematically correct for every non-empty finite integer
list. The candidate does not mutate its input.

### Trusted translation

In clean scratch, the trusted translator regenerated `solution.mpy` with
SHA-256
`5824615b9afe1a35b69f5a428651e2361081b01cc0274796f1516e8c04dd9838`.
It is byte-identical to the submitted file. The command and exit status are in
[02_prepare_and_translate.log](/audit-output/evidence/02_prepare_and_translate.log).

### Independent differential testing

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical entry point and the scratch copy of the generated entry
point. It also uses a separately written brute-force oracle. It covered:

- both documented examples;
- negative, zero, and positive singletons;
- both length-one/longer branches;
- prefix-wins, tail-wins, combined-wins, and equality branch boundaries;
- a mixed list whose minimum is internal;
- arbitrary-precision integers;
- all 19,607 lists of lengths 1 through 5 over values `-3..3`;
- 500 deterministic generated lists of lengths 1 through 12 over
  values `-50..50`.

There were zero value mismatches in those normally returning cases. Empty input
is outside the contract; canonical raised `ValueError` and candidate raised
`RecursionError`. Exact results and exit 0 are in
[03_differential.log](/audit-output/evidence/03_differential.log).

There is one material intended-domain divergence. On Python 3.10.12 with
recursion limit 1000, input `[1] * 1100` makes the canonical implementation
return `1` and the candidate raise `RecursionError`. The independently
reproducible witness is
[recursion_boundary_test.py](/audit-output/evidence/recursion_boundary_test.py),
with output in
[16_recursion_boundary.log](/audit-output/evidence/16_recursion_boundary.log).
This is judged as an implementation-to-intent and generated-semantics-to-CPython
limitation. It does not produce a wrong normal return, so it does not invalidate
the claimed partial-correctness theorem, but it prevents a `PASS` verdict.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/114-minSubArraySum-audit`. No candidate `*-kompiled` directory
or candidate Python cache was copied or used.

### Fresh concrete definition and execution

The concrete definition was built from
[semantic.k](/candidate/semantic.k) with:

```text
kompile --backend haskell semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled
```

It exited 0; see
[04_build_concrete.log](/audit-output/evidence/04_build_concrete.log).
Fresh `krun` executions returned:

| Input | K result | Independent Python result |
|---|---:|---:|
| `[2,3,4,1,2,4]` | `1` | `1` |
| `[-1,-2,-3]` | `-6` | `-6` |
| `[7]` | `7` | `7` |
| `[0,0]` | `0` | `0` |
| `[5,-7]` | `-7` | `-7` |
| `[4,-6,2,-5,7]` | `-9` | `-9` |
| `[10^30,-10^31,10^30]` | `-10^31` | `-10^31` |

Every `krun` exited 0 with empty environment and stack, restored depth `z`, and
the expected `pyInt` in `<k>`. Commands and full bounded configurations are in
[05_concrete_execution.log](/audit-output/evidence/05_concrete_execution.log).

### Fresh proof definition and positive claims

The proof definition was built from source with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0; see
[06_build_proof.log](/audit-output/evidence/06_build_proof.log).
The exact original command

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`; see
[07_prove_original.log](/audit-output/evidence/07_prove_original.log).

The claims have a legitimate dependency order:

1. the prefix-helper claim is its own recursive circularity;
2. the target-call claim uses the already checked prefix-helper and its own
   recursive circularity;
3. the entry claim uses the call-level claims.

Reviewer copies added labels but did not change claim bodies. A prefix-only
suite, a prefix-plus-target suite, and the complete three-claim suite each
exited 0 and printed `#Top`. This reconstructs every positive claim with its
required predecessor claims, rather than silently assuming one:
[09_prove_cumulative_dependencies.log](/audit-output/evidence/09_prove_cumulative_dependencies.log).

As a dependency diagnostic, filtering the specification down to the target
claim alone produces a genuine stuck recursive prefix call, and filtering to
the entry alone causes unbounded unfolding until a reviewer-set 20-second
timeout. The prefix claim alone closes. This is expected because K's filtering
removes the circularities on which the selected claim depends; it is not the
candidate's declared all-claims proof. The diagnostic is retained in
[08_prove_each_claim.log](/audit-output/evidence/08_prove_each_claim.log).

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

| Claim | Precondition | Postcondition |
|---|---|---|
| Prefix helper, [spec.k:8](/candidate/spec.k:8) | The computation is an exact call to the submitted `min_prefix_sum` closure on `cons(H,T)`. The function map is the submitted map. Caller environment, continuation, stack, entry/args, and call depth are arbitrary but well-sorted. | The call reaches `returned(D, pyInt(minPrefix(cons(H,T)))) ~> K`, having restored the caller environment, stack, and depth and preserved all other cells. |
| Target call, [spec.k:21](/candidate/spec.k:21) | The computation is an exact call to the submitted `minSubArraySum` closure on non-empty `cons(H,T)`, with the same compositional caller state. | It reaches `returned(D, pyInt(minSubarray(cons(H,T)))) ~> K`, restoring the caller state. |
| Entry, [spec.k:35](/candidate/spec.k:35) | The exact submitted module representation starts with entry `"minSubArraySum"`, argument `cons(H,T)`, empty function/environment/stack cells, and depth `z`. | Module loading and invocation consume the computation and leave exactly `pyInt(minSubarray(cons(H,T))) ~> .K`; the functions cell is exactly the submitted function map and the other mutable cells are restored. |

There is no explicit `requires`; non-emptiness is enforced by the constructor
pattern `cons(H,T)`. There is no right-only free result variable and no
one-way implication. The result is fixed by recursive functions over the
entire symbolic input. The call-level `returned` marker is an internal
control-fidelity marker; the ordinary semantic rule subsequently rewrites it
to its value. The entry claim constrains the actual final `pyInt`.

### Satisfying states and ground substitution

For all three claims, take
`H=4`, `T=cons(-6,cons(2,cons(-5,cons(7,nil))))`.
For each call claim additionally take `K=.K`, `D=z`, `RHO=.Map`,
`STACK=.List`, empty `ARGS`, and any string `ENTRY`. For the entry claim use
its specified empty cells. These states are well-sorted and satisfiable.

The formal summaries are `minPrefix = -5` and `minSubarray = -9`.
The candidate helper returns `-5`; the candidate entry, trusted canonical, and
reviewer brute-force oracle all return `-9`. The executable substitutions are
in [claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[10_claim_witnesses.log](/audit-output/evidence/10_claim_witnesses.log).

### Actual program identity and body sensitivity

`solutionProgram` is not an oracle: its only equation expands to a literal
`Module` term. `solutionFunctions` similarly expands to the two literal
closures. Manual source comparison shows the same constructors as the
byte-verified `solution.mpy`; the empty `else` lists appear as K's canonical
`.Stmts`.

As a stronger check, the reviewer embedded the regenerated `Module` term
directly on an entry claim's left side, bypassing `solutionProgram`. The
direct-term suite dry-ran successfully, then exited 0 with `#Top`:
[spec-direct-program.k](/audit-output/evidence/spec-direct-program.k) and
[15_direct_program_pinning.log](/audit-output/evidence/15_direct_program_pinning.log).
The postcondition's function-map equality also forces module loading to create
exactly `solutionFunctions`.

A reachable body-sensitivity mutation changed only the target singleton body
from `return nums[0]` to `return 0`, consistently in both literal program
representations. Concrete K execution on `[7]` returned `0`. The mutated proof
definition and spec built, but `kprove` exited 1 with the unmet condition
`H = 0` on the singleton branch. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[solution-body-mutated.mpy](/audit-output/evidence/solution-body-mutated.mpy),
and [14_body_sensitivity.log](/audit-output/evidence/14_body_sensitivity.log).
The proof is therefore sensitive to the real body.

## 5. Rule-by-rule static soundness review

The source inventory, hashes, attributes, and line-numbered files are preserved
in [11_static_inventory.log](/audit-output/evidence/11_static_inventory.log).
There are 45 semantic rules, 6 verification equations, and 3 claims: 54 local
behavior declarations in total.

### Local syntax and configuration inventory

Every local syntax declaration is:

- `IntList`: `nil`, `cons(Int,IntList)`.
- `Value`: `pyInt`, `pyBool`, `pyList`, `funref`, `builtin`.
- `Values`: comma-separated `Value`; `Strings`: comma-separated `String`;
  `Depth`: `z` or `s(Depth)`.
- `Program`: `Module(Stmts)`; `Params`: `Params(Strings)`; `Stmts`: a
  juxtaposed list of `Stmt`.
- `Stmt`: `FuncDef`, `If`, `Assign`, `Return`.
- `Exprs`: comma-separated `Expr`.
- `Expr`: `Int`, `Name`, `Call`, `BinOp`, `Compare`, `Subscript`.
- `CmpOps`: juxtaposed `CmpOp`; `CmpOp`: an operator string and expression.
- `Index`: `Expr` or `Slice`; `Slice`: three bounds; `Bound`: `Expr` or
  `NoBound`.
- Runtime `Function`: `closure(Params,Stmts)`; `Frame`: `frame(Map,K)`.
- `KItem`: `exec`, `invoke`, `choose`, `storeName`, `returning`, `returned`,
  `callOne`, `applyOne`, `callTwo`, `callTwoSecond`, `applyTwo`, unary
  `apply`, binary `apply`, `binLeft`, `binRight`, `compareLeft`,
  `compareRight`, `singletonTest`, `listHead`, and `sliceTail`.
- Verification syntax: `minPrefix(IntList)`, `minSubarray(IntList)`,
  constant `solutionFunctions : Map`, and constant
  `solutionProgram : Program`.

The configuration has exactly the state used by this program: `<k>`, immutable
entry arguments, a function map, current local environment, call stack, and
call depth. A heap, allocation counter, I/O, or exception cell is absent
because the modeled program performs no mutation, allocation-visible
operation, or I/O. The missing exception/resource model is nevertheless the
documented recursion-limit concern.

### Construct-to-semantics coverage

The submitted term uses `Module`, `FuncDef`, `Params`, statement/expression
lists, `If`, `Assign`, `Return`, `Int`, `Name`, unary and binary `Call`,
`BinOp("+")`, single `Compare("==")`, `Subscript(...,Int(0))`,
`Slice(Int(1),NoBound,NoBound)`, and `CmpOp`. Each is declared above and has
the scheduling/evaluation/application rules below. Both true and false
condition branches, recursive calls, both `min` branches, indexing, slicing,
assignment, return, stack push/pop, and the two function bodies were exercised
by fresh execution or proof.

### Semantic rules S01-S45

Every semantic rule was reviewed against the supported program states:

| ID / source | Rule role | Decision |
|---|---|---|
| S01 [89](/candidate/semantic.k:89) | `Module` schedules all definitions then invokes configured entry/args. | Sound; preserves all cells and uses the actual function table built by S04. |
| S02 [93](/candidate/semantic.k:93) | Empty `exec` becomes `.K`. | Sound list base. |
| S03 [94](/candidate/semantic.k:94) | Non-empty `exec` schedules head then tail. | Sound left-to-right statement order. |
| S04 [96](/candidate/semantic.k:96) | `FuncDef` installs/overwrites its closure. | Sound for module-level definitions; later definitions replace earlier ones as in Python. |
| S05 [99](/candidate/semantic.k:99) | `invoke` forms a user-function application. | Sound for the configured single-argument entry. |
| S06 [102](/candidate/semantic.k:102) | `If` evaluates its condition before branch choice. | Sound evaluation order. |
| S07 [103](/candidate/semantic.k:103) | True choice executes then-list. | Sound. |
| S08 [104](/candidate/semantic.k:104) | False choice executes else-list. | Sound. |
| S09 [106](/candidate/semantic.k:106) | Name assignment evaluates RHS before store. | Sound for all submitted assignments. |
| S10 [107](/candidate/semantic.k:107) | Store updates the local map. | Sound state update; old binding is replaced. |
| S11 [110](/candidate/semantic.k:110) | `Return` evaluates its expression then marks return. | Sound evaluation order. |
| S12 [111](/candidate/semantic.k:111) | Return discards the current function suffix, restores the exact saved environment/continuation, pops one frame, and decrements depth. | Sound abrupt control. The complete current continuation is intentionally discarded; the caller continuation comes from the top frame and no observable modeled cell is omitted. |
| S13 [115](/candidate/semantic.k:115) | `returned(D,V)` exposes `V`. | Sound for the only producer, S12; the depth marker is proof/control bookkeeping. |
| S14 [118](/candidate/semantic.k:118) | Integer literal becomes `pyInt`. | Sound, using unbounded K integers. |
| S15 [119](/candidate/semantic.k:119) | Local-name lookup. | Sound on submitted states. |
| S16 [121](/candidate/semantic.k:121) | Function-name lookup. | Sound on submitted states. |
| S17 [123](/candidate/semantic.k:123) | Syntactic `len` resolves to builtin. | Sound because submitted local/function maps never bind `"len"`. |
| S18 [124](/candidate/semantic.k:124) | Syntactic `min` resolves to builtin. | Sound because submitted local/function maps never bind `"min"`. |
| S19 [128](/candidate/semantic.k:128) | Unary call evaluates callee first. | Sound left-to-right order. |
| S20 [129](/candidate/semantic.k:129) | Then evaluates unary argument. | Sound. |
| S21 [130](/candidate/semantic.k:130) | Applies unary callee to evaluated argument. | Sound. |
| S22 [132](/candidate/semantic.k:132) | Binary call evaluates callee first. | Sound. |
| S23 [133](/candidate/semantic.k:133) | Then evaluates first argument. | Sound. |
| S24 [134](/candidate/semantic.k:134) | Then evaluates second argument. | Sound. |
| S25 [135](/candidate/semantic.k:135) | Applies binary callee to both values. | Sound. |
| S26 [139](/candidate/semantic.k:139) | User call selects exact closure, installs one-parameter local environment, saves entire caller continuation/environment, pushes frame, increments depth. | Sound for the two one-argument submitted closures; all relevant state is preserved. |
| S27 [145](/candidate/semantic.k:145) | Builtin `len` returns structural list length. | Sound for `pyList`. |
| S28 [146](/candidate/semantic.k:146) | Binary integer `min` uses `intMin`. | Sound for submitted integer calls. |
| S29 [149](/candidate/semantic.k:149) | Binary expression evaluates left operand first. | Sound. |
| S30 [150](/candidate/semantic.k:150) | Then evaluates right operand. | Sound. |
| S31 [151](/candidate/semantic.k:151) | Integer `+` returns K integer sum. | Sound ordinary arithmetic. |
| S32 [153](/candidate/semantic.k:153) | Comparison evaluates left operand first. | Sound. |
| S33 [154](/candidate/semantic.k:154) | Then evaluates comparator. | Sound. |
| S34 [155](/candidate/semantic.k:155) | Integer `==` returns a Python boolean value. | Sound ordinary equality. |
| S35 [160](/candidate/semantic.k:160) | Priority-40 bridge fuses syntactic `len(E) == 1` into one evaluation of `E`. | Sound on the submitted non-empty-list states; detailed bridge audit below. |
| S36 [162](/candidate/semantic.k:162) | Singleton list makes fused test true. | Sound. |
| S37 [163](/candidate/semantic.k:163) | Two-or-more-element list makes fused test false. | Sound for every non-singleton state reachable from the non-empty precondition. |
| S38 [166](/candidate/semantic.k:166) | Index-zero evaluates base once. | Sound for used literal index. |
| S39 [167](/candidate/semantic.k:167) | Head of non-empty integer list becomes `pyInt`. | Sound. |
| S40 [169](/candidate/semantic.k:169) | Tail slice evaluates base once. | Sound for the only submitted slice. |
| S41 [171](/candidate/semantic.k:171) | `[1:]` returns structural tail. | Sound because the program never mutates or observes list identity. |
| S42 [175](/candidate/semantic.k:175) | `length(nil)=0`. | Sound base. |
| S43 [176](/candidate/semantic.k:176) | `length(cons(_,T))=1+length(T)`. | Sound, structurally descending. |
| S44 [177](/candidate/semantic.k:177) | `intMin(I,J)=I` when `I<=J`. | Sound. |
| S45 [178](/candidate/semantic.k:178) | `intMin(I,J)=J` when `I>J`. | Sound; guard is disjoint from S44 and together they cover all K integers. |

S15-S18 can overlap in a more general Python-like program that shadows a
builtin or function name. S35 syntactically assumes the `"len"` binding and
has no `nil` result rule. Concrete off-scope witnesses are an environment that
binds `"len"` or an empty list: the generated semantics may choose the builtin
or become stuck where general Python would use the binding or return false.
Neither state is reachable from any submitted claim precondition: a call
replaces the local map with only `"nums"`, the fixed function map contains only
the two submitted names, and recursion takes a tail only after proving the
current list has at least two elements. Empty input is explicitly outside the
contract. These are narrower coverage/reusability gaps, not an unsoundness
claim on the intended domain; there is no concrete or symbolic witness by
which they enable a false theorem conclusion for a non-empty intended input.

S35 is the sole operational bridge. Its matched continuation is arbitrary but
preserved, it evaluates `E` exactly once, it changes no state cell, and it
introduces no abrupt control. The reviewer removed S35-S37, rebuilt the
definition, and executed the same submitted program through the ordinary
callee/argument/`length`/equality path. Singleton `[7]` and recursive
`[4,-6,2,-5,7]` executions produced byte-identical complete final
configurations with and without the bridge. See
[semantic-no-fused.k](/audit-output/evidence/semantic-no-fused.k) and
[12_bridge_comparison.log](/audit-output/evidence/12_bridge_comparison.log).
The static constructor split supplies the universal justification on the
reachable non-empty domain; the concrete runs are sensitivity evidence, not a
replacement for that reasoning.

### Verification equations V01-V06 and claims C01-C03

| ID / source | Classification and decision |
|---|---|
| V01 [13](/candidate/verification.k:13) | `minPrefix([H])=H`: truthful definitional-summary base. |
| V02 [14](/candidate/verification.k:14) | `minPrefix(H::J::T)=min(H,H+minPrefix(J::T))`: truthful; every non-empty prefix is `[H]` or `H` plus a tail prefix. Structural descent is strict. |
| V03 [16](/candidate/verification.k:16) | `minSubarray([H])=H`: truthful definitional-summary base. |
| V04 [17](/candidate/verification.k:17) | `minSubarray(H::J::T)=min(minSubarray(J::T),minPrefix(H::J::T))`: truthful; every non-empty contiguous subarray is wholly in the tail or begins at `H`. Structural descent is strict. |
| V05 [25](/candidate/verification.k:25) | `solutionFunctions`: exact definitional constant for the two closures. It does not rewrite execution and is checked by module-loading equality and direct-term proof. |
| V06 [48](/candidate/verification.k:48) | `solutionProgram`: exact definitional constant for the submitted module. It expands before ordinary execution and carries no result summary. |
| C01 [8](/candidate/spec.k:8) | Prefix execution circularity. Sound exact-call summary; it independently closes and executes the actual helper body. |
| C02 [21](/candidate/spec.k:21) | Target execution circularity. Sound exact-call summary using C01 and itself on a structurally smaller list. |
| C03 [35](/candidate/spec.k:35) | End-to-end module claim. Sound consumer of C01/C02; pins empty initial cells, exact entry/argument, loaded map, final result, and control state. |

The six symbols `length`, `intMin`, `minPrefix`, `minSubarray`,
`solutionFunctions`, and `solutionProgram` have `[function]`. There are no
`[total]` or `[functional]` declarations. `length` and `intMin` are in fact
covered on their complete declared domains; `minPrefix` and `minSubarray` are
intentionally partial on `nil`, matching the claim domain. There are no local
simplification rules, concrete rules, opaque symbols, `owise` rules, or other
priority rules. No rule encodes a result into operational execution, fabricates
a value for a used construct, or bypasses a submitted function body.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. The reviewer created
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), preserving
the two call-level claims and changing only the end-to-end result obligation
from:

```text
pyInt(minSubarray(cons(H,T)))
```

to:

```text
pyInt(minSubarray(cons(H,T)) +Int 1)
```

`kprove --dry-run` exited 0, so the mutation parsed and built against the fresh
definition. Actual `kprove` exited 1 with `WarnStuckClaimState`; the reached
configuration contains the correct
`pyInt(minSubarray(cons(H,T)))`, and the failed implication is exactly:

```text
minSubarray(cons(H,T)) +Int 1
#Equals
minSubarray(cons(H,T))
```

No parser error, missing import, timeout, or unrelated crash caused the
failure. `[7]` is a satisfying ground witness: actual result `7`, mutated
obligation `8`. Commands, statuses, and residual are in
[13_non_vacuity.log](/audit-output/evidence/13_non_vacuity.log). Non-vacuity
passes.

## 7. Proven versus assumed accounting

### What is machine-proved

Conditional on the compiled theory, for every finite non-empty K `IntList`:

1. the exact submitted `min_prefix_sum` body, invoked from the submitted
   function map in any modeled caller environment/stack/continuation/depth,
   is partially correct with result `minPrefix(list)` and restores caller
   control/state;
2. the exact submitted `minSubArraySum` body is partially correct with result
   `minSubarray(list)` and restores caller control/state;
3. the exact translated module, started with the named entry, one list
   argument, and empty runtime cells, loads its definitions and is partially
   correct with final normal value `pyInt(minSubarray(list))`.

The theorem is result-constraining and body-sensitive. It is not a theorem that
CPython terminates normally on every finite list.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and reachability-logic implementation | Every build, execution, and proof result | Ordinary toolchain trust boundary; independently rebuilt, but not verified here. |
| Built-in K `Int`, `Bool`, `String`, `Map`, `List`, `+Int`, comparisons, map update/lookup, and list constructors | All semantic and mathematical rules | Acceptable low-level primitive boundary. K integers match Python arbitrary-precision integer values absent resource exhaustion. |
| Trusted mounted `py2mpy.py` | Source-to-`Module` identity | Explicitly trusted by the audit problem; byte identity of regenerated/submitted output was checked. |
| Generated MPY semantics as a model of the used Python subset | The bridge from K execution to `solution.py` | Audited rule-by-rule and concretely against Python. Acceptable for normal execution of the submitted subset, but not a full Python semantics. |
| Unbounded modeled call stack and omitted exceptions/resource limits | Universal K input domain versus real CPython | Concerning. The `[1]*1100` witness shows the bridge is false for full CPython behavior unless conditioned on no `RecursionError`. This is the main verdict concern. |
| Structural sharing for `nums[1:]` instead of Python list allocation | Recursive bodies | Acceptable here because the program performs no mutation, identity observation, or allocation observation. |
| Informal mathematical connection from V01-V04 to “least non-empty contiguous subarray sum” | Human-facing contract | Correct by the exhaustive structural decomposition in Stage 5, but not a separate machine-checked theorem over an independently defined subarray relation. This is a modest intent-bridge limitation. |
| Finite differential and concrete tests | Empirical semantics/Python and intent bridge | Reproducible supporting evidence only. The 20,118 normally returning cases do not prove universal equivalence, and the recursion mismatch remains explicit. |

There are no opaque symbols, unconstrained result oracles, external calls, or
candidate-supplied compiled artifacts in the reconstructed proof. Candidate
prose, traces, and differentials were not used as proof.

### Gate conclusions

- **Gate A — real-program soundness: PASS for the modeled normal-execution
  subset.** Program bodies execute, the exact module is pinned, the sole
  bridge is sound on every reachable non-empty state, state/control is
  preserved, the body mutation is detected, and the false result mutation is
  rejected.
- **Gate B — intent adequacy: LIMITED.** The recursive CPython implementation
  raises on a valid long input and the generated semantics omits that
  exceptional behavior. The English-property bridge is also mathematical
  reasoning rather than a separate K theorem. These limitations prevent
  `PASS` but do not make the normal-return partial-correctness theorem false.
- **Gate C — trust/evidence auditability: PASS.** Assumptions, exclusions,
  commands, statuses, normally returning differential scope, and the
  counterexample at the recursion boundary are all explicit and reproducible.

Reviewer-authored artifacts and bounded logs are under
[evidence/](/audit-output/evidence). Their copy/diff/hash record is
[17_preserve_review_artifacts.log](/audit-output/evidence/17_preserve_review_artifacts.log).

VERDICT: CONCERNS
LEGITIMACY: LEGIT
