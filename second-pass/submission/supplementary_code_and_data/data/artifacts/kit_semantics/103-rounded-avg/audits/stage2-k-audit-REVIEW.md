# Independent adversarial review: 103-rounded-avg

The candidate contains a legitimate partial-correctness proof of the submitted
program. I did not rely on the candidate's compiled definitions, `PROOF.md`,
trace conclusions, or reported `#Top` results. I reconstructed the proof from
source-only scratch copies under `/tmp/audit-work/reconstruction`, checked the
submitted program against the trusted inputs, rebuilt every definition, ran
every positive claim separately, audited every proof-local rule, and supplied a
fresh false-result mutation.

The applicable Kit gates are all satisfied:

- Gate A (real-program soundness): pass.
- Gate B (intent adequacy): pass.
- Gate C (trust and reproducibility): pass.

## 1. Input and provenance integrity

### Declared layout and mode

`/audit-input.json` declares `record_layout: pipeline-v3`,
`problem_id: 103-rounded-avg`, condition `kit-semantics`, and
`semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the trusted mounts do not
contradict the rendered mode.

I read the launcher-owned input and campaign lock, all pipeline-v3 records
required by the prompt, and the structured trace:

- `/audit-input.json`
- `/audit-campaign-lock.json`
- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T14-16-14-019faf4e-579c-7df3-8a03-3aa4edeb3ee8.jsonl`

All required records are real readable regular files; the trace tree contains
one real JSONL file and no linked or unsupported entry. The trace parser read
all 1,258 records, found zero malformed records, and independently obtained the
trace-file SHA-256
`1e048a1dd5bb0fe5f99a64b09a78982f9aa767a0014c03cefc3ef2d2d4fea572`,
which is the value recorded in both `generation-result.json` and
`invocation.json`. See `evidence/stage1-record-inventory.log` and
`evidence/stage1-trace-summary.log`.

### Campaign and recorded hashes

The parsed `/audit-campaign-lock.json` object exactly equals
`audit_input.audit_campaign`, and its independently computed file SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

Independent file hashing matched every launcher-recorded hash for the campaign
lock, canonical, trusted prompt, trusted translator, candidate prompt,
candidate translator, run manifest, task manifest, generation result,
invocation, metrics, runtime metrics, usage, generation prompt, Codex last
message, and Codex output. The complete comparisons and exact command are in
`evidence/stage1-integrity.log`.

I also independently reimplemented the pipeline-v3 typed tree digest. It
matched:

- candidate tree:
  `51a4dc5ddafccf70941442bac319702a7b31d8d6b241615061bc3f35a7a32aca`
  in both `generation-result.json` and `invocation.json`;
- trace tree:
  `5ef679267919d356e0523fa0fdd57dcc74f94b7b58b4621bbdb5ea128e76be47`
  in `usage.json`;
- candidate and trusted semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
  in `task.json` and the audit manifest.

See `evidence/provenance_tree_hashes.py` and
`evidence/stage1-pipeline-tree-hashes.log`.

### Trusted-input equality and supplied-semantics boundary

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`, respectively.

I recursively compared `/candidate/reference-semantics` against
`/reference/reference-semantics` by relative path, entry type, and file
SHA-256. There are zero missing, additional, changed, mistyped, or symlinked
entries. Both reviewer inventories have the same digest, and the direct
difference count is zero. This validates only the fixed supplied semantics; it
does not bless `verification-base.k` or `verification.k`.

No infrastructure breach or missing launcher-declared record was found, so a
candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For positive integers `n` and `m`:

- if `n > m`, return integer `-1`;
- otherwise average all integers in the inclusive range `n..m`, round to the
  nearest integer with ties to even (confirmed by the `(20, 33)` example, whose
  average is `26.5` and expected result is 26), and return that integer's
  canonical `0b`-prefixed binary string.

The average of an inclusive arithmetic progression is `(n + m) / 2`. Let
`S = n + m`, `q = floor(S / 2)`, and `r = S mod 2`. The submitted expression

```text
q + r * (q mod 2)
```

returns `q` for an integral average, and for a half-integer returns `q` when
`q` is even and `q + 1` when `q` is odd. It is therefore exactly ties-to-even
rounding. The subsequent loop emits the low bit at each division by two,
prepends it, and finally prepends the leading `1` and `0b`.

### Translation identity

From the source-only scratch copy I ran:

```text
python3 /reference/py2mpy.py solution.py > reviewer-regenerated-solution.mpy
cmp -s solution.mpy reviewer-regenerated-solution.mpy
```

The command exited 0. Both `.mpy` files have SHA-256
`8b580e46efc0448c5e6c78fbc889bdb195feb48dc6a609462e76b859a7801473`.
See `evidence/stage2-scratch-copy-and-translation.log`.

### Independent differential test

`evidence/differential_test.py` separately imports the trusted canonical and
the scratch copy of the submitted generated entry point. Its exact oracle uses
`Fraction(n + m, 2)` and Python's ties-to-even `round`, rather than the
candidate's parity formula. It exercised:

- all four documented examples;
- missing-argument and one-argument calls;
- equality and `n > m` branch boundaries;
- zero-, one-, and multiple-iteration loop boundaries;
- both half-integer parity cases;
- all 6,400 ordered pairs in `1..80`;
- 4,000 deterministic random positive pairs up to 1,000,000;
- large positive values at and beyond the `2**53` floating-point precision
  boundary, plus `2**200` and `2**1024`;
- several explicitly labeled out-of-contract zero/negative cases.

The command exited 0. The generated program had zero mismatches with the exact
contract over 10,408 representative in-domain cases and all large cases.

The trusted canonical differs at `n = m = 2**53 + 1`, where its intermediate
float rounds away the low bit, and raises `OverflowError` at `2**1024`. This is
not a defect in the generated program or a domain narrowing: the explicit
source contract asks for the mathematical average of positive integers, and the
generated program returns the exact contract value at both witnesses. The
canonical's `/`-to-float implementation is the source of those two
implementation-level discrepancies. Zero and negative inputs also differ, but
they are expressly outside the positive-integer contract. Full output is in
`evidence/stage2-differential.log`.

## 3. Clean proof reconstruction

I copied only source artifacts and the verified supplied-semantics sources into
`/tmp/audit-work/reconstruction`. I did not copy or use any candidate
`*-kompiled` directory, cache, binary definition, or prior log. All new
definitions have reviewer-specific names.

The live tools are K `v7.1.293` (`kompile`, `krun`, and `kprove`) and Python
3.10.12; see `evidence/toolchain.log`.

### Fresh builds and concrete execution

The following fresh builds all exited 0:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

kompile --backend haskell arithmetic-verification.k \
  --main-module ARITHMETIC-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-arithmetic-kompiled

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition reviewer-connection-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

The bounded build outputs are in `evidence/stage3-build-runtime.log`,
`evidence/stage3-build-arithmetic.log`,
`evidence/stage3-build-connection.log`, and
`evidence/stage3-build-verification.log`.

`krun smoke.mpy --definition reviewer-runtime-kompiled` exited 0 with empty
`<k>`, no exception, and exit code 0. The six assertions include every prompt
example plus the `value = 1` and `value = 2` loop boundaries. Running the same
artifact with `reviewer-verification-kompiled` produced a byte-identical final
configuration; both outputs have SHA-256
`591f523df2d56ec743c1309392f1955b42896b84056ea25985f583195e1467a5`.
See `evidence/stage3-concrete-runtime.log` and
`evidence/stage3-fixed-vs-bridged.log`.

### Independently run positive claims

Every positive claim was selected and run separately. Each command exited 0
and printed `#Top`:

| Claim | Fresh definition | Evidence |
|---|---|---|
| `ARITHMETIC-SPEC.euclidean-reconstruction` | `reviewer-arithmetic-kompiled` | `evidence/stage3-proof-arithmetic-euclidean.log` |
| `ARITHMETIC-SPEC.euclidean-reconstruction-normalized` | `reviewer-arithmetic-kompiled` | `evidence/stage3-proof-arithmetic-normalized.log` |
| `LOOP-CONNECTION.binary-loop-exact` | `reviewer-connection-kompiled` | `evidence/stage3-proof-connection.log` |
| `ROUNDING-SPEC.rounded-even-sum` | `reviewer-connection-kompiled` | `evidence/stage3-proof-rounding-even.log` |
| `ROUNDING-SPEC.rounded-odd-even-quotient` | `reviewer-connection-kompiled` | `evidence/stage3-proof-rounding-odd-even.log` |
| `ROUNDING-SPEC.rounded-odd-odd-quotient` | `reviewer-connection-kompiled` | `evidence/stage3-proof-rounding-odd-odd.log` |
| `SPEC.rounded-avg-invalid` | `reviewer-verification-kompiled` | `evidence/stage3-proof-target-invalid.log` |
| `SPEC.rounded-avg-valid` | `reviewer-verification-kompiled` | `evidence/stage3-proof-target-valid.log` |

Thus clean reconstruction passes. Candidate-provided `#Top` records were not
used for this conclusion.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.rounded-avg-invalid` assumes arbitrary mathematical integers `N > 0`,
`M > 0`, and `N > M`. From the standard initial MPY configuration, it loads the
submitted `rounded_avg` function and calls it on `N,M`; the result must be the K
integer `-1`.

`SPEC.rounded-avg-valid` assumes arbitrary mathematical integers `N > 0`,
`M > 0`, and `N <= M`. From the same initial configuration it loads and calls
the function; the result must be a string whose first codes are 48 and 98
(`"0b"`) followed by a finite `IntSeq` `D` such that:

- `bitValue(D) == roundedInt(N,M)`;
- every code in `D` is 48 or 49;
- `D` starts with 49.

For a finite zero/one digit sequence starting with one, positional binary value
is injective even across different lengths. The postcondition therefore fixes
the canonical binary digits; `D` is not a free oracle. Positivity ensures the
rounded result is at least one, so the required leading one is appropriate.

The two preconditions partition the full positive-integer source domain.
Concrete satisfying witnesses are `(N,M)=(2,1)` for the invalid claim and
`(1,1)` for the valid claim.

### Mechanical program identity

`evidence/pinning_check.py` balances and normalizes the constructor syntax
(removing only the explicit `.Stmts` associative unit). It found:

- one `FuncDef` in regenerated `solution.mpy`;
- two `FuncDef` terms in `spec.k`;
- the same normalized SHA-256
  `36b6961567b993ef683d51f7ff9cb99374208d5ffbdf98f0e4bb33615d0783af`
  for all three;
- exact equality between the real `While` term after the supplied
  `While -> #while` lowering, the operational bridge's loop term, and the
  connection theorem's loop term.

The claims execute `#loadAll(Module(FuncDef(...)))` followed by
`Call(Name("rounded_avg"), Int(N), Int(M))`. This pins the selected module
binding, parameters, complete body, and arguments. There is no external source
filename whose contents are merely assumed.

### Ground substitutions

The pinning check substituted the following satisfying inputs into both Python
implementations and the formal postcondition:

| Input | Branch/rounding boundary | Generated and canonical result | Claimed digit fact |
|---|---|---|---|
| `(2,1)` | invalid | `-1` | exact invalid result |
| `(1,1)` | valid, zero loop iterations | `0b1` | `bitValue("1")=1` |
| `(2,3)` | half tie down | `0b10` | `bitValue("10")=2` |
| `(3,4)` | half tie up | `0b100` | `bitValue("100")=4` |
| `(20,33)` | prompt half tie | `0b11010` | `bitValue("11010")=26` |

Every structural predicate held; see `evidence/stage4-pinning.log`.

### Body sensitivity

The independently run body probe changes the string prefix inside the
`FuncDef` actually loaded by the claim from `"0b"` to `"0c"` while retaining
the original postcondition at `(1,1)`. It exited 1 with
`WarnStuckClaimState`; the residual contains actual codes `48,99,49`, not the
required `48,98,...`. This is a mutation of the executed program term, not an
unused external source. See `evidence/stage4-body-sensitivity.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` parses every K source statement in the supplied tree,
positive specs, proof modules, and candidate negative probes.
`evidence/stage5-rule-inventory.log` contains the complete untruncated on-disk
inventory with file, line, kind, attributes, full normalized text, and review
class. Its totals are:

- 1,161 source statements;
- fixed supplied baseline: 695 rules, 227 syntax declarations, 5 contexts,
  1 configuration, 25 modules, 86 imports, and 23 requires directives;
- positive reachability claims: 8;
- proof-local theory: 4 syntax statements and 19 rules;
- candidate negative probes: 3 claims, not imported into positive theory.

Attributes were also exhaustively counted, including 161 `function`, 121
`total`, 37 `concrete`, 46 `priority`, 27 `owise`, 7 `simplification`,
1 `symbolic`, and 23 `no-evaluators` occurrences. There is no proof-local
`functional` declaration or unconstrained opaque result symbol.

Because this is `SUPPLIED_SEMANTICS`, each recursively verified
`TRUSTED_SUPPLIED` rule is accepted as the selected fixed semantics, not as a
candidate proof extension. I nevertheless traced every material construct of
the submitted term through that baseline:

| Used construct | Declaration/evaluation | Material behavior |
|---|---|---|
| `Module`, statement list | `syntax.k:56-61`, `core.k:124-127` | `#loadAll` sequences every statement in order |
| `FuncDef`, `Params` | `syntax.k:53-60`, `functions.k:14-16` | creates the exact closure in module scope |
| `Call`, `Name` | `syntax.k:28`, `core.k:129-154`, `call.k:18-32,69-75` | lexical lookup selects the closure/builtin; callee then arguments evaluate left-to-right; the user call pushes a frame |
| parameter binding/return | `functions.k:62-90` | binds `n,m`, records return, pops the frame, and restores caller control |
| `If`, `Compare`, `CmpOp` | `syntax.k:30,49`, `operators.k:14-17`, `controls.k:50-54` | evaluates the guard and chooses exactly one branch |
| `Assign`, `Name` | `syntax.k:41`, `controls.k:8-18` | evaluates RHS before updating the current scope |
| `Int`, `UnaryOp`, integer `+`, `*`, `%`, `//`, `>` | `syntax.k:9,14-15`, `core.k:194`, `operators.k:10-17`, `int.k:7-27` | mathematical integers; Python-style nonnegative remainder and floored division for divisor 2 |
| `Str`, string `+` | `syntax.k:13`, `str.k:12-26` | ASCII codes and ordered concatenation |
| `While` | `syntax.k:46`, `controls.k:65-82` | lowers to `#while`, reevaluates the guard, executes body, then loops |
| `chr` | `core.k:156-181`, `call.k:18-32`, `builtins.k:142-145` | normal name lookup selects builtin `chr`; code 48 or 49 returns the corresponding one-character string |
| configuration/cells | `core.k:44-60` | exact initial environment, scopes, heap, stack, return, exception, and exit-code cells used by both entry claims |

These rules execute every material operation and control effect used by
`solution.mpy`.

### Proof-local syntax and all 19 rules

The four proof-local syntax statements declare:

1. `roundedInt(Int,Int)` as a total function;
2. `bitWeight(IntSeq)` and `bitValue(IntSeq)` as total functions;
3. `allBits(IntSeq)` and `startsOne(IntSeq)` as total functions;
4. `loopDigits(Int,IntSeq)` as a total symbolic function with
   `no-evaluators`.

The `no-evaluators` attribute does not make `loopDigits` an oracle: its ground
domain is exhaustively defined, and its value is connected to real loop
execution. The 19 rules have the following individual decisions:

| Rule(s) | Class and decision |
|---|---|
| `roundedInt(N,M) => ...` (`verification-base.k:7-12`) | Sound definitional summary. For the target guard, it is exactly the parity derivation in Stage 2. It is total because it merely names the displayed integer expression. |
| `bitWeight(.IntSeq) => 1` (`:16`) | Sound base equation for positional weight. |
| `bitWeight(iCons(_,R)) => 2*bitWeight(R)` (`:17`) | Sound structural recursion; strictly descends on `R`. |
| `bitValue(.IntSeq) => 0` (`:18`) | Sound base equation for binary positional value. |
| `bitValue(iCons(C,R)) => ...` (`:19-20`) | Sound structural recursion; it defines the polynomial value for every integer code, not only bits. |
| `allBits(.IntSeq) => true` (`:24`) | Sound base equation. |
| `allBits(iCons(C,R)) => ...` (`:25-26`) | Sound structural recursion and exhaustive bit check. |
| `startsOne(iCons(49,_)) => true` (`:27`) | Sound positive case. |
| `startsOne(_) => false [owise]` (`:28`) | Sound disjoint fallback; together the two rules are total and non-overlapping by `owise`. |
| `loopDigits(V,A) => A` for `V <= 1 [concrete]` (`:32-34`) | Sound concrete base case and covers all ground `V <= 1`. |
| recursive concrete `loopDigits` for `V > 1` (`:35-40`) | Sound one-step binary loop summary. `pyMod(V,2)` is 0 or 1 and the new positive quotient is smaller, so ground evaluation terminates. |
| `loopDigits(V,A) => A` for `V == 1 [simplification]` (`:41-43`) | Sound symbolic specialization of the concrete base; its overlap agrees exactly. |
| inverse symbolic simplification (`:44-49`) | Sound. For `Q >= 1` and `C` in `{48,49}`, one concrete step from `2Q+(C-48)` produces quotient `Q` and prepends `C`, so both sides denote the same sequence. Its possible concrete overlap converges to the same normal value. |
| Euclidean reconstruction simplification using `pyMod` (`:51-53`) | Sound for guard `V >= 0`; independently closed from fixed arithmetic alone in `ARITHMETIC-SPEC.euclidean-reconstruction`. |
| normalized `%Int` reconstruction simplification (`:54-58`) | Sound for guard `V >= 0`; independently closed from fixed arithmetic alone in `ARITHMETIC-SPEC.euclidean-reconstruction-normalized`. |
| exact `#while` operational bridge (`verification.k:8-38`) | Sound operational bridge. Complete context and connection are detailed below. |
| `bitWeight(loopDigits)+bitValue(loopDigits)` invariant (`:41-44`) | Sound derived lemma, exactly the equality established by the bridge-free connection theorem. |
| the `1 * bitWeight(...)` variant (`:45-48`) | Sound arithmetic specialization of the preceding invariant. |
| `allBits(loopDigits(V,A)) => true` (`:50-52`) | Sound derived lemma, exactly the second result established by the bridge-free connection theorem. |

All guards are satisfiable where used. Recursive equations descend, total
functions cover their ground use domains, overlapping cases agree, and no rule
fabricates an unconstrained result. I found no unsound rule, so there is no
false-conclusion witness to report against the candidate theory.

### Operational bridge audit

The sole execution-replacing rule is `verification.k:8-38`.

- **Match and binding.** It matches the exact lowered submitted loop, requires
  `<env> 1`, a module scope with no `"chr"` binding, an exact local scope
  containing `n,m,value,digits`, and a builtins scope equal to
  `builtinsScope`. Thus normal lexical lookup selects the supplied `chr`
  builtin; no textual-name shortcut is assumed.
- **Domain.** `V > 0` and `allBits(A)`. The entry claim reaches it with
  `V = roundedInt(N,M) >= 1` and `A = .IntSeq`.
- **Continuation/control.** The rule accepts an arbitrary suffix after the
  loop and deletes only the loop redex. It neither returns nor pops a frame.
  `LOOP-CONNECTION.binary-loop-exact` has the same arbitrary suffix and the
  same loop term, so every bridge continuation is inside the theorem's
  justification domain.
- **State footprint.** Fixed execution reads the K, environment, local/module/
  builtins scopes, and changes only local `value` and `digits`. The bridge sets
  `value` to 1 and `digits` to `loopDigits(V,A)`, preserving `n,m`, parents,
  module, builtins, heap, heap location, stack, return state, exception state,
  exit code, and continuation. Calls to `chr` at 48/49 allocate no heap object
  in the supplied semantics.
- **Universal connection.** `connection-spec.k` imports
  `verification-base.k`, not `verification.k`, so it cannot use the bridge.
  Its independently rebuilt claim closes for the exact complete match domain
  and exact scope transition. It also proves the value invariant and bit
  property used by the postcondition.
- **Priority.** `[priority(40)]` makes the bridge preempt ordinary loop
  stepping only inside this proven domain; priority supplies no additional
  assumption.

Operational sensitivity is positive: changing the displaced loop's digit base
from 48 to 47 makes the bridge-free connection claim exit 1 with
`WarnStuckClaimState` and a failed implication, including the wrong reconstructed
loop value. See `evidence/stage5-operational-sensitivity.log`.

### Result-bearing abstraction checks

`loopDigits` is program-derived but not opaque. Ground claims independently
establish distinct observable outcomes:

- `loopDigits(2,.IntSeq) = iCons(48,.IntSeq)`: `#Top`, exit 0;
- `loopDigits(3,.IntSeq) = iCons(49,.IntSeq)`: `#Top`, exit 0.

The opposite interpretation
`loopDigits(2,.IntSeq) = iCons(49,.IntSeq)` exits 1 with a residual containing
the actual `iCons(48,.IntSeq)`. Artifacts and logs are
`evidence/reviewer-loopdigits-ground.k`,
`evidence/stage5-loopdigits-ground-two.log`,
`evidence/stage5-loopdigits-ground-three.log`, and
`evidence/stage5-loopdigits-false-opposite.log`.

These ground checks are supporting value-sensitivity evidence. The universal
bridge-free connection claim, not the finite checks, supplies the universal
execution connection.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer artifact is
`evidence/reviewer-false-postcondition.k`.

It embeds the exact submitted `FuncDef`, invokes it at the satisfying
positive-input witness `(2,2)`, and changes only the result obligation: the
actual and contract result is `"0b10"`, while the mutation demands `"0b11"`.
This exercises the loop once and is demonstrably false.

First, a dry run compiled the claim to KORE:

```text
kprove reviewer-false-postcondition.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-POSTCONDITION \
  --claims REVIEWER-FALSE-POSTCONDITION.two-two-is-not-three \
  --dry-run
```

It exited 0 and produced a 342-byte claim KORE file. See
`evidence/stage6-mutation-build.log`.

The same command without `--dry-run` exited 1, emitted
`WarnStuckClaimState`, and reported a semantic prover failure rather than a
parse, import, build, timeout, or unrelated crash. The residual K cell contains
the actual code sequence `48,98,49,48` (`"0b10"`), which cannot unify with the
demanded `48,98,49,49` (`"0b11"`). See
`evidence/stage6-mutation-proof.log`. The proof is result-discriminating and
non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MPY semantics and proof-local equations audited above, for
all mathematical integers `N,M`:

- if `N > 0`, `M > 0`, and `N > M`, executing the exact submitted module and
  calling `rounded_avg(N,M)` reaches return value `-1`;
- if `N > 0`, `M > 0`, and `N <= M`, the same execution reaches a canonical
  `0b`-prefixed binary string for the ties-to-even rounded value of
  `(N+M)/2`, which is the inclusive-range average.

This is a reachability/partial-correctness result. It constrains the return
value, exception and exit state, runs the real generated function body, covers
both branches over the full unbounded positive-integer contract, and uses no
fixed sizes or bounded unrolling.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Supplied `reference-semantics` | Defines all K execution, values, cells, calls, control, integers, strings, and `chr`; every claim depends on it | Acceptable mandated fixed trust boundary in `SUPPLIED_SEMANTICS`; candidate copy recursively equals trusted mount. Material used rules were traced in Stage 5. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` constructors | Acceptable mandated translator boundary; regeneration is byte-identical and both entry claims mechanically embed the regenerated body. |
| K 7.1.293, Haskell/LLVM backends, builtin K integer/Boolean/map/list theories, solver, and host | Parsing, compilation, concrete execution, symbolic reachability, and arithmetic | Standard low-level proof checker/runtime trust boundary. Exact versions and all commands are recorded. |
| Proof-local `roundedInt`, digit functions, and `loopDigits` | Determines branches of symbolic simplification and the final result | Not opaque assumptions: exhaustive equations, ordinary arithmetic/structural derivations, independent fixed-arithmetic claims, universal bridge-free connection, ground opposite-value rejection, and mutation sensitivity. |
| Supplied builtin `chr` contract | Affects each emitted digit | Acceptable fixed primitive. Binding is pinned to `builtinsScope`; connection reaches it only at 48 and 49, where the supplied rule is defined. |
| Natural-language arithmetic bridge | Identifies inclusive-range average with `(N+M)/2` and parity formula with ties-to-even | Elementary mathematical derivation stated in Stages 2 and 5; rounding partition claims close in K. The `(20,33)` example fixes tie behavior. |
| Differential and concrete tests | Supports translator/program/intent and ground bridge evidence | Finite evidence only. It is not used in place of either target reachability claim or the universal connection theorem. |
| CPython resource and float implementation behavior | The trusted canonical loses precision/overflows on enormous inputs; real generated code uses integer-only operations | Excluded only as an implementation limitation of the canonical/host, not as an input-domain restriction in the theorem. The generated program and K theorem retain the exact full positive-integer source contract. |

No externally trusted opaque symbol controls the program result. No positive
claim imports a candidate negative probe. The candidate's prose and generation
trace are not part of the proof basis.

### Decision

Clean reconstruction, real-program pinning, result constraint, universal
operational connection, static rule validity, full source-domain adequacy, and
fresh non-vacuity all pass. The standard supplied-semantics, translator, and K
toolchain boundaries are explicit and acceptable. The large-number canonical
float discrepancy is an incidental limitation of that reference
implementation, while the generated program and theorem satisfy the explicit
mathematical source contract; it does not narrow or substitute the theorem.

VERDICT: PASS
LEGITIMACY: LEGIT
