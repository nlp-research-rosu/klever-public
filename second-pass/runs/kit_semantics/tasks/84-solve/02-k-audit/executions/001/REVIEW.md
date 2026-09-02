# Independent adversarial review: HumanEval 84 `solve`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the complete stated domain. This conclusion comes from a fresh
source-only reconstruction and a rule-by-rule audit, not from the candidate's
`PROOF.md`, logs, traces, or precompiled definitions.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `84-solve`, and condition
`kit-semantics`. The rendered mode and trusted mounts agree:
`/reference/reference-semantics` is present.

I independently checked the launcher-owned records as follows:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly equals the `audit_campaign` object in `/audit-input.json`, and
  matches the recorded lock hash.
- `/run.json`, `/task.json`, `/generation-result.json`, and all required
  pipeline-v3 generation records are present, regular, readable, and have the
  recorded hashes. This includes `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace.
- The structured trace contains one regular JSONL file with 1,349
  successfully parsed records. The generation output has 580,063 bytes and
  16,861 lines. These were inspected only as untrusted construction history.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `5b69b9b354c92bcb61d5e63ec962c1df7cc559708ce12f54b705344d47dc5b28`).
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- I recursively compared `/candidate/reference-semantics` with
  `/reference/reference-semantics`. All 24 files have the same relative names,
  entry types, and bytes; neither tree contains symlinks, and neither has an
  additional or missing entry.
- The seven proof sources needed for reconstruction are regular candidate
  files rather than symlinks. Candidate-provided `*-kompiled` directories and
  caches were not used.

The executable check and its complete summary are
`evidence/integrity_check.py` and `evidence/stage1-integrity.log`. No
infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says that for an integer `N` satisfying
`0 <= N <= 10000`, `solve(N)` returns a string containing the base-two
representation of the sum of `N`'s decimal digits. Although the prose says
"positive", the explicit constraint and trusted canonical function include
zero. The canonical implementation is:

```python
bin(sum(int(i) for i in str(N)))[2:]
```

The submitted `solution.py` extracts exactly five decimal digits using `% 10`
and `// 10`, sums them, and returns the corresponding literal binary string
for each possible sum from 0 through 36. Five digits suffice for every input
in the stated domain, including `10000`; the implementation does not claim to
work outside that domain.

### Trusted translation identity

In a clean scratch directory I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited zero. Both MPy files have SHA-256
`65fa95b7e7f94340d67500dd31807f4cf935ca8a169df0a322337071c835de43`.
The exact command record is `evidence/stage2-fidelity.log`.

### Independent differential test

`evidence/differential_test.py` separately imports the trusted canonical entry
point and the generated entry point. It checks:

- the three documented examples `1000`, `150`, and `147`;
- the lower and upper domain endpoints and decimal width boundaries;
- a witness for every proof partition boundary at sums
  `0, 7, 8, 15, 16, 23, 24, 31, 32, 36`;
- 253 seeded representative inputs; and
- exhaustively, every integer from `0` through `10000`.

There is no empty value in an integer input domain; `N=0` is the applicable
lower-boundary case. All 10,001 exhaustive comparisons agreed, with zero
mismatches. The command exited zero; see `evidence/stage2-fidelity.log`.
This is independent behavioral evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to
`/tmp/audit-work/84-solve`. No candidate-built definition or cache was copied
or referenced. The available `kompile`, `krun`, and `kprove` are K
v7.1.293; version logs are under `evidence/toolchain-*.log`.

### Fresh definitions and concrete run

The following fresh builds exited zero:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

kompile bridge-verification.k --backend haskell \
  --main-module BRIDGE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition bridge-audit-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

The bounded logs are `evidence/stage3-kompile-llvm.log`,
`evidence/stage3-kompile-bridge-haskell.log`, and
`evidence/stage3-kompile-proof-haskell.log`.

I translated the submitted body plus assertions at the documented examples,
domain endpoints, and every sum-partition boundary. Fresh LLVM execution:

```text
krun concrete-test.mpy --definition runtime-audit-kompiled
```

exited zero with an empty `<k>` cell, `NoExc`, an empty call stack, and exit
code zero. The preserved input and log are `evidence/concrete-test.mpy` and
`evidence/stage3-krun-concrete.log`.

### Fresh positive proofs

The bridge-free suite, which imports only the supplied `MPY` definition,
exited zero and printed `#Top`; see
`evidence/stage3-proof-bridge-suite.log`.

I then selected every positive target claim separately. Each command used the
fresh `verification-audit-kompiled` definition, exited zero, and printed
`#Top`:

| Claim | Evidence |
|---|---|
| `SPEC.digit-sum-bound` | `evidence/stage3-proof-digit-sum-bound.log` |
| `SPEC.solve-sum-00-07` | `evidence/stage3-proof-solve-sum-00-07.log` |
| `SPEC.solve-sum-08-15` | `evidence/stage3-proof-solve-sum-08-15.log` |
| `SPEC.solve-sum-16-23` | `evidence/stage3-proof-solve-sum-16-23.log` |
| `SPEC.solve-sum-24-31` | `evidence/stage3-proof-solve-sum-24-31.log` |
| `SPEC.solve-sum-32-36` | `evidence/stage3-proof-solve-sum-32-36.log` |

The aggregate target suite independently exited zero and printed `#Top` as
well (`evidence/stage3-proof-target-suite.log`). Compiler warnings concern
unused variables in the fixed semantics/spec and do not alter these success
signals.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

Let

```text
N = D0 + 10*(D1 + 10*(D2 + 10*(D3 + 10*D4)))
S = D0 + D1 + D2 + D3 + D4.
```

`digitDomain` requires `D0..D3` to be digits. It permits either `D4=0`, or
`D4=1` with all four lower digits zero. Independent enumeration found exactly
10,001 unique tuples and exactly the values `0..10000`. Thus it neither omits
nor adds a source-contract input. `SPEC.digit-sum-bound` proves the pure fact
`0 <= S <= 36`.

Each program claim starts from the full initial MPy configuration, loads
`solutionModule`, calls its binding named `solve` on `N`, and requires one of
the following exhaustive, disjoint sum ranges:

| Claim | Additional precondition | Satisfying witness |
|---|---|---|
| `solve-sum-00-07` | `S < 8` | `N=0`, digits `(0,0,0,0,0)`, `S=0` |
| `solve-sum-08-15` | `8 <= S < 16` | `N=8`, digits `(8,0,0,0,0)`, `S=8` |
| `solve-sum-16-23` | `16 <= S < 24` | `N=79`, digits `(9,7,0,0,0)`, `S=16` |
| `solve-sum-24-31` | `24 <= S < 32` | `N=699`, digits `(9,9,6,0,0)`, `S=24` |
| `solve-sum-32-36` | `32 <= S` | `N=5999`, digits `(9,9,9,5,0)`, `S=32` |

All entry preconditions are therefore satisfiable. Ground substitution gives,
respectively, `"0"`, `"1000"`, `"10000"`, `"11000"`, and `"100000"` in
both Python implementations, and each string decodes to its stated `S`.
The executable witness record is `evidence/stage4-pinning.log`.

The postcondition is not a tautology or a free result. The returned K value is
the same `str(?CODES)` constrained by:

```text
canonicalBin(?CODES) andBool decodeBin(?CODES) ==Int S
```

`canonicalBin` permits exactly `"0"` or a nonempty bit string beginning in
`"1"`; `decodeBin` is ordinary positional base-two decoding. For every
nonnegative `S`, those conditions select a unique string. They therefore state
the exact result required by the prompt rather than a one-way approximation.

The final `<scopes>` cell is existential because module loading necessarily
leaves the real `solve` closure in scope zero. The result, continuation,
environment, allocator counters, heap, call stack, return state, exception,
and exit code remain constrained. The program has no loops and the target
proof uses no loop or helper circularity.

### Mechanical program pinning

`solutionModule` is a nullary function whose right-hand side is the full MPy
module. I mechanically extracted that right-hand side from `verification.k`
and byte-compared it with trusted regeneration. Both have the same SHA-256
`65fa95b7e7f94340d67500dd31807f4cf935ca8a169df0a322337071c835de43`;
see `evidence/stage4-pinning.log`. Under `#loadAll`, the fixed semantics installs
and calls that exact body.

For an independent body-sensitivity check, I changed the executed branch for
digit sum 5 from `Return(Str("101"))` to `Return(Str("0"))` inside
`solutionModule`, redirected the spec to that changed K file, and rebuilt it.
The mutant definition compiled with exit zero. The corresponding target claim
then exited one with `WarnStuckClaimState`; its residual reaches the changed
return on the satisfiable `S=5` path. See:

- `evidence/stage4-body-mutation.diff`
- `evidence/verification-body-mutant.k`
- `evidence/spec-body-mutant.k`
- `evidence/stage4-body-mutant-kompile.log`
- `evidence/stage4-body-mutant-proof.log`

This mutation changes the term actually executed by the claim and demonstrates
dependence on the submitted body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` scanned every declaration in the 24 supplied
semantics files (including the assembled `semantics.k`), `verification.k`,
`spec.k`, and the bridge-only files. The exhaustive 954-row inventory is
`evidence/rule-inventory.tsv`; counts and all opaque declarations are in
`evidence/rule-inventory-summary.txt`.

The inventory contains:

- 706 rules: 466 equational, 238 operational, and 2 proof-local
  simplification rules;
- 232 syntax declarations, including 150 function declarations, 112 marked
  total, and none marked functional;
- 10 reachability claims, 5 contexts, and 1 configuration;
- 45 declaration blocks with priority attributes, 35 with `concrete`, 27 with
  `owise`, and 22 supplied `no-evaluators` opaque boundaries.

Every row records source file, line, module, declaration kind, attributes,
normalized declaration, declaration-block hash, and audit disposition. All
fixed-semantics rows are accepted as the selected, byte-verified supplied
semantics. I also read all 2,211 source lines and checked the complete used
execution path. The 22 opaque boundaries are float, sorting, and MD5
operations; none is syntactically present in the submitted program or
reachable from a target claim. `MPY-CONCRETE` is used only by the LLVM smoke
definition; the Haskell proof module imports `MPY`, not `MPY-CONCRETE`.

`evidence/used-construct-map.md` maps every submitted constructor to its
declaration and operational rules. In particular:

- configuration and cells are created by `MPY-CORE`;
- module loading and statement sequencing preserve order;
- function definition, lookup, argument evaluation, frame push, parameter
  binding, return, frame pop, and saved allocator restoration match the actual
  call;
- strictness/contexts evaluate assignment RHSs, binary operands, comparisons,
  conditions, and return values in the required order;
- `%` and `//` dispatch through the fixed integer rules;
- assignments update only the local scope; this program performs no heap
  allocation or external state change;
- all guards and priorities on the used route are compatible, and no exception
  or abrupt-control rule is bypassed.

The candidate's diagnostic, negative, vacuity, and pre-existing mutant specs
are not imported by the positive target definition and contribute no rule to
claim closure.

### Every proof-local declaration

`verification.k` contributes exactly 16 declarations. Their dispositions are:

1. `solutionModule`'s syntax declaration and sole equation are a definitional
   name for the mechanically identical submitted AST. They do not skip the
   body.
2. The decimal-remainder simplifier
   `((D+10*Q)%10+10)%10 => D` is guarded by `0 <= D < 10`. For every integer
   `Q`, the left side is the normalized remainder of a number congruent to
   `D` modulo 10, so the equality is true.
3. The quotient simplifier `(D+10*Q-D)/10 => Q` has numerator exactly `10*Q`,
   so it is true for every integer `Q` under the stated digit guard.
4. `decodeBin` has disjoint empty/cons equations, recurses on the strict tail,
   and is standard positional decoding.
5. `allBinDigits` has disjoint empty/cons equations, recurses on the strict
   tail, and exactly recognizes ASCII codes 48 and 49.
6. `canonicalBin` has the disjoint cases `"0"`, leading `"1"` plus all bits,
   and an `owise` false case; these are exhaustive over `IntSeq`.
7. `digitDomain` has one unconditional total equation and precisely defines
   the decimal tuple domain established above.

The two simplifiers have distinct root operations and no conflicting overlap.
Neither has a totality assertion or priority attribute. All proof-local
recursive definitions have exhaustive constructors and strict structural
descent. There are no candidate-local opaque values, operational return/frame
bridges, fabricated values, answer oracles, or rules that intercept a program
call.

The arithmetic rules are also connected to fixed execution, not merely
asserted:

- `bridge-verification.k` imports only the supplied `MPY` definition.
- The four universal bridge-free claims cover `applyBin("%",D+10Q,10)`,
  `applyBin("//",D+10Q,10)`, and both exact expanded pure terms, with arbitrary
  continuation `REST:K`. The freshly reconstructed suite prints `#Top`.
- Fresh opposite witnesses under the fixed definition reject `83 % 10 = 4`
  and `83 // 10 = 9`; the stuck residuals expose the correct values 3 and 8.
  See `evidence/stage5-bridge-opposite-wrong-mod.log` and
  `evidence/stage5-bridge-opposite-wrong-floordiv.log`.

These simplifiers preserve a pure integer value in any context; they read,
write, or abstract no cell and introduce no control effect. The universal
connection claims, not the ground probes, justify them.

No inventoried candidate-local rule is unsound, so there is no unsoundness
finding requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation
`evidence/fresh-false-spec.k` uses the satisfiable ground input `N=147` but
changes the result obligation from the real `"1100"` to `"111"`.

First:

```text
kprove fresh-false-spec.k \
  --definition verification-audit-kompiled \
  --spec-module FRESH-FALSE-SPEC --dry-run
```

exited zero, establishing that the mutation parses and builds. The actual
proof command without `--dry-run` exited one with `WarnStuckClaimState`.
Crucially, the residual has the completely executed real return
`str(iCons(49,iCons(49,iCons(48,iCons(48,.IntSeq)))))`, i.e. `"1100"`, and
fails to unify with the false `"111"` destination. This is an expected unmet
result obligation, not a parser error, timeout, unrelated crash, or
unreachable mutation. Exact bounded logs are
`evidence/stage6-false-dry-run.log` and
`evidence/stage6-false-proof.log`.

## 7. Proven versus assumed accounting

### What is formally established

Conditional on the supplied semantics and standard K toolchain, the successful
reachability claims establish:

> For every integer `N` in `0..10000`, executing the exact submitted
> `solution.mpy` binding from the pinned initial MPy configuration reaches a
> normal return containing the unique canonical binary representation of the
> sum of `N`'s decimal digits. The continuation and call stack are empty,
> return/exception state is reset, the heap and allocator counters are
> unchanged, and the exit code is zero. Module scope retains the loaded
> function binding.

This is the requested partial-correctness result. It is not inferred from
`PROOF.md`, the generation trace, concrete tests, or an external summary.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, SMT reasoning, and K built-in integer/Boolean/map/string hooks | Foundational execution and proof checking | Standard unavoidable proof-tool trust; acceptable |
| The 24-file supplied MPy semantics | Defines evaluation, cells, calls, integer operations, and ASCII strings | Required trusted input in `SUPPLIED_SEMANTICS`; byte integrity passed and every used rule was statically audited |
| Trusted `py2mpy.py` | Maps the Python AST to the MPy constructor term | Launcher-designated trusted input; inspected on every used node and regenerated byte identity passed |
| `solutionModule` | Selects the executed program body | Not an assumption: its equation is mechanically identical to trusted regeneration and is body-sensitive |
| Two integer simplifiers | Accelerate symbolic remainder and quotient terms | Not opaque assumptions: true guarded equalities with fresh bridge-free universal `#Top` proofs |
| `decodeBin`, `allBinDigits`, `canonicalBin`, `digitDomain` | State the postcondition and domain | Fully defined, terminating mathematical functions; no oracle or unconstrained interpretation |
| Uniqueness of canonical positional base-two notation and Horner decimal representation | Connects the formal predicates to the natural-language contract | Elementary mathematics checked in the static audit; exact finite-domain enumeration and differential execution provide additional independent evidence |
| Twenty-two supplied opaque float/sort/MD5 symbols | Could affect other MPy programs | Unreachable from this submitted AST and absent from every target dependency; no influence on value, state, control, or proof closure here |
| Differential and concrete tests | Support Python/MPy fidelity on ground executions | Reproducible, and the Python differential is exhaustive over the finite contract domain; explicitly not used as a replacement for symbolic proof |

Gate A passes: the real body executes, the only proof extensions are sound,
the result is constrained, body sensitivity holds, and the false result is
rejected. Gate B passes: the exact full source-contract domain and exact result
are covered. Gate C passes: all assumptions and evidence are named and
reproducible, with no result-bearing opaque boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
