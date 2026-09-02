# Independent adversarial review: 41-car-race-collision

The candidate contains a legitimate, body-sensitive partial-correctness proof of
the submitted generated program. The proof was reconstructed from source,
closes without proof-local summaries or oracles, constrains the returned value,
and rejects both a false result and a changed function body. I assign
`CONCERNS / LEGIT`, rather than `PASS`, because the candidate omits all four
named generation/provenance records and has no structured generation trace.
Those omissions limit provenance auditability but do not affect the independently
reconstructed theorem.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted directory
`/reference/reference-semantics` exists and is a real directory, so there is no
mode/mount contradiction and no infrastructure breach.

The recursive comparison covered 25 entries below each semantics root.
`/candidate/reference-semantics` has exactly the same relative paths, entry
types, and bytes as `/reference/reference-semantics`; it has no additional,
missing, changed, mistyped, or symlinked entry. The candidate therefore did not
alter or extend the supplied semantics. See
[`stage1-integrity.log`](evidence/stage1-integrity.log) and
[`check_integrity.py`](evidence/check_integrity.py).

The following candidate/trusted files are regular files and byte-identical:

- `/candidate/prompt.py` and `/reference/prompt.py`, SHA-256
  `d4a9a6f17e6f65f8fa63bffa89d863ca691859fab85fff3f60f378d9340cc489`.
- `/candidate/py2mpy.py` and `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Missing provenance artifacts

The candidate is missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any root artifact whose name identifies it as a structured generation trace

The integrity script exits 1 only because of these five reported omissions.
There was consequently no untrusted generation record to cross-check. Candidate
`prove.sh`, concrete tests, bytecode cache, and prose comments were not trusted
or reused as proof evidence.

### Isolated reconstruction sources

All executable work occurred below `/tmp/audit-work/reconstruction/work`.
Candidate `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` were
copied as source; the semantics used in the work tree was copied from the
trusted reference tree. No candidate-built definition or cache was copied.
The post-copy comparisons all exit 0 in
[`stage3-reconstruction-sources.log`](evidence/stage3-reconstruction-sources.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a nonnegative integer `n`, there are `n` left-to-right cars and `n`
right-to-left cars. Each car from one set meets each car from the other set
once, because collisions do not change trajectories. Thus the collision count
is the number of cross-set pairs, `n * n = n²`. `n = 0` gives zero collisions.
The physical interpretation makes nonnegative integers the intended domain,
although the Python annotation itself only says `int`.

The trusted canonical entry point returns `n**2`. The submitted entry point is:

```python
def car_race_collision(n: int):
    return n * n
```

It is branchless and agrees with the canonical algorithm over the entire
intended domain. It also agrees for negative Python integers, although negative
car counts are outside the natural-language domain.

### Translation identity

Running the trusted `/reference/py2mpy.py` on the copied submitted
`solution.py` produced SHA-256
`8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659`,
exactly the SHA-256 of the submitted `solution.mpy`; `cmp` exited 0. Exact
command, hashes, and status are in
[`stage2-translation.log`](evidence/stage2-translation.log), with the
reviewer-authored driver in
[`check_translation.sh`](evidence/check_translation.sh).

### Independent differential execution

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical entry point and the copied submitted entry point independently. Its
scope was:

- no documented examples, because the trusted prompt contains none;
- fixed intended-domain cases `0, 1, 2, 3, 10, 50, 100, 1000, 2**31-1`;
- 500 deterministic generated integers in `[0, 1_000_000]`, seed `410041`;
- four probes of the stronger formal scope: `-1, -2, -10, -(2**31)`.

There is no program branch boundary beyond the empty/first-positive boundary.
All 509 intended-domain cases and all four formal-scope probes matched in both
value and type; mismatch count was zero. See
[`differential-inputs.json`](evidence/differential-inputs.json) and
[`stage2-differential.log`](evidence/stage2-differential.log).

## 3. Clean proof reconstruction

The independently installed toolchain was K version `v7.1.337`. `kup` was not
installed, but `kompile`, `krun`, and `kprove` were available and reported the
same version, so the mandatory live path was available. See
[`stage3-toolchain.log`](evidence/stage3-toolchain.log).

The fresh commands and results were:

| Purpose | Exact substantive command | Exit | Relevant result |
|---|---|---:|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 | Fresh LLVM definition |
| Concrete smoke run | `krun runtime_smoke.mpy --definition runtime-kompiled` | 0 | Final `<k> .K </k>`, `NoExc`, exit code 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled` | 0 | Fresh Haskell definition |
| Sole positive target claim | `kprove spec.k --definition verification-kompiled --spec-module SPEC` | 0 | `#Top` |

The full bounded outputs are
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log),
[`stage3-krun-runtime-smoke.log`](evidence/stage3-krun-runtime-smoke.log),
[`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log), and
[`stage3-kprove-positive.log`](evidence/stage3-kprove-positive.log).

The reviewer concrete program was regenerated with the trusted translator and
contains the exact two-line submitted implementation followed by assertions for
`0, 1, 2, 10, -3`. Its preparation record is
[`stage3-runtime-prepare.log`](evidence/stage3-runtime-prepare.log), and its
sources are [`runtime_smoke.py`](evidence/runtime_smoke.py) and
[`runtime_smoke.mpy`](evidence/runtime_smoke.mpy).

There is exactly one positive target claim in `spec.k`; it was run as part of
the complete `SPEC` module. No helper or loop claim exists.

The LLVM compiler warned about non-exhaustive matches in several unrelated
total functions (`mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`).
The Haskell build/proof only warned about unused variables in `strLt`. None of
those functions or string/float/list terms is reachable from this submitted
program, and none contributed to claim closure.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause. Its precondition therefore permits every K
mathematical integer `N` and requires this exact initial state:

- `<k>` contains `#runCarRaceCollision(N)`;
- environment location is module scope `0`;
- scope `0` is empty with parent `-1`, and `-1` is exactly `builtinsScope`;
- next scope location is `1`;
- heap and stack are empty, next heap location is `0`;
- return state is `noRet`, exception state is `NoExc`, and exit code is `0`.

Its postcondition requires:

- `<k>` to be exactly `N *Int N`;
- module scope `0` to contain the closure for
  `Return(BinOp("*", Name("n"), Name("n")))`;
- every other listed cell to have the same clean value as in the precondition.

Thus the result is not free, existential, tautological, or guarded by a one-way
implication. The same universally quantified `N` appears in the invocation and
the exact result expression.

### Actual submitted program execution

The `solutionModule` macro in `verification.k` is exactly the AST in the
byte-verified submitted `solution.mpy`. It is not a summary of the result.
`#runCarRaceCollision` expands to ordinary `#loadAll(solutionModule)` followed
by an ordinary call through `Name("car_race_collision")`.

The fixed-semantics path is:

1. load the module and sequence its sole `FuncDef`;
2. install the exact closure in scope `0`;
3. look up that closure by name;
4. evaluate the `Int(N)` argument;
5. allocate a callee scope and push a call frame;
6. bind parameter `n` to `N`;
7. evaluate both `Name("n")` operands left-to-right;
8. dispatch integer `*` to `N *Int N`;
9. execute `Return`, restore the caller frame, and remove the callee scope.

No proof-local rule intercepts `Call`, `BinOp`, lookup, return, frame popping, or
multiplication. The final module closure, environment, stack, return state,
heap, location counters, exception state, and exit code are all explicitly
checked by the postcondition.

### Satisfiable witnesses and body sensitivity

`N = 3` with the exact initial cells above is a concrete satisfying state. The
review also instantiated `N = 0, 3, -3`. The K ground claims all closed with
`#Top`, and both Python implementations returned `0, 9, 9`, respectively. See
[`spec-ground.k`](evidence/spec-ground.k),
[`stage4-ground-kprove.log`](evidence/stage4-ground-kprove.log), and
[`stage4-ground-python.log`](evidence/stage4-ground-python.log).

For a separate body-sensitivity check, I changed only the loaded body from
`n*n` to `n+n`, kept the result obligation `N*N`, and updated the expected
stored closure so the mismatch could only be result-bearing. The mutant
definition built (exit 0), while its proof failed (exit 1) with
`WarnStuckClaimState` and residual `N +Int N = N *Int N`. See
[`verification-body-mutant.k`](evidence/verification-body-mutant.k),
[`spec-body-mutant.k`](evidence/spec-body-mutant.k),
[`stage4-body-mutant-build.log`](evidence/stage4-body-mutant-build.log), and
[`stage4-body-mutant-proof.log`](evidence/stage4-body-mutant-proof.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k-rule-inventory.tsv`](evidence/k-rule-inventory.tsv) is the exhaustive
line-addressed inventory for the trusted assembled semantics, every helper K
file, `verification.k`, and `spec.k`. It records each declaration/rule, its
attributes, whether it is on the submitted program path, and its audit
disposition. [`k-program-path-inventory.tsv`](evidence/k-program-path-inventory.tsv)
is the 54-entity reached subset. The generating script and count log are
[`k_inventory.py`](evidence/k_inventory.py) and
[`stage5-inventory.log`](evidence/stage5-inventory.log).

Across 26 sources, the inventory contains 933 entities:

- 229 syntax declarations;
- 697 ordinary/macro/concrete rules;
- five evaluation contexts;
- one configuration;
- one target claim.

Attribute counts are 145 `function`, 107 `total`, 25 `symbol`, 22
`no-evaluators`, 45 priority-bearing, 35 concrete, 26 `owise`, five `macro`,
one `macro-rec`, two strict declarations, and one sequential-strict
declaration. There are no `functional` declarations and no simplification
rules.

Per-source entity counts and decisions are:

| Source | Count | Role and decision for this proof |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import file; imports trusted `MPY`, not `MPY-CONCRETE`, for proof |
| `syntax.k` | 16 | Used AST declarations and generated strictness are faithful |
| `core.k` | 84 | Used configuration, loading, lookup, argument evaluation, and helpers are faithful |
| `iter.k` | 1 | Unreached fixed declaration |
| `range.k` | 8 | Unreached fixed rules |
| `operators.k` | 12 | Reached generic `BinOp` dispatch is faithful; other rules unreached |
| `int.k` | 17 | Reached `Int * Int` rule is exact mathematical multiplication |
| `bool.k` | 14 | Unreached fixed rules |
| `float.k` | 155 | Unreached fixed/opaque/concrete-only rules |
| `str.k` | 33 | Unreached fixed rules |
| `set.k` | 18 | Unreached fixed rules |
| `list.k` | 32 | Unreached fixed rules |
| `tuple.k` | 25 | Unreached fixed rules |
| `subscript.k` | 57 | Unreached fixed/total rules |
| `comprehension.k` | 10 | Unreached fixed macro rules |
| `methods.k` | 102 | Unreached fixed rules |
| `controls.k` | 37 | Unreached fixed rules |
| `functions.k` | 19 | Reached definition, binding, return, and pop rules are faithful |
| `builtins.k` | 175 | Registry is present; builtin operational rules are unreached |
| `call.k` | 24 | Reached generic call and closure-frame rules are faithful |
| `sort.k` | 25 | Unreached fixed opaque/concrete sort boundary |
| `assert.k` | 3 | Unreached in the symbolic proof |
| `dict.k` | 40 | Unreached fixed rules |
| `concrete.k` | 21 | LLVM-only smoke semantics; not imported by the proof |
| `verification.k` | 4 | Two exact syntax declarations and two exact driver/macro rules |
| `spec.k` | 1 | The reviewed result-constraining target claim |

The inventory dispositions mean:

- `FIXED_USED_PATH_ACCEPTED`: individually checked against the real submitted
  control flow, cells, guards, and ordinary integer mathematics.
- `FIXED_UNUSED_REVIEWED`, `FIXED_TOTAL_UNUSED`,
  `FIXED_OPAQUE_UNUSED`, or `FIXED_CONCRETE_ONLY_UNUSED`: part of the
  byte-identical supplied semantics but unable to match any reachable term in
  this theorem. These are not being claimed as a universal certification of
  full Python; their broader coverage is outside this program.
- `PROOF_LOCAL_USED_EXACT`: exact syntax/driver structure, not a computation
  summary or operational bypass.
- `TARGET_CLAIM_REVIEWED`: the sole entry theorem described in Stage 4.

For the 879 unreached entities, no intended-domain `N` can place their left-hand
constructors in this program's execution. Accordingly, there is no false
conclusion witness they can enable for this theorem; I do not label them
unsound. Their broader-language coverage is the narrower evidence boundary.

### Proof-local extensions

`verification.k` declares no function, total/functional symbol, opaque value,
priority rule, simplification, lemma, helper claim, or answer-returning rewrite.
Its four entities are:

1. macro syntax `solutionModule`;
2. the exact AST macro equation;
3. syntax for `#runCarRaceCollision(Int)`;
4. a driver rewrite to ordinary module loading and ordinary calling.

The driver is a definitional entry harness, not an operational bridge: it
neither returns `N*N` nor skips the program-defined function.

### Configuration, control, overlap, and totality checks

- The fixed configuration and the entry claim agree on every cell.
- `BinOp` is sequentially strict in its two operands; the two `Name("n")`
  lookups are evaluated left-to-right. Neither lookup has side effects.
- Found-name and parent-fallthrough guards are disjoint. Cell-aware priority
  rules cannot fire because neither reached scope has a `"$cells"` marker.
- The generic call rule is `owise`; no math/hashlib/problem-local interception
  matches this call. Callable-constructor dispatch is disjoint, and the reached
  value is a `closureVal`.
- Plain parameter binding and cell-parameter binding do not overlap in the
  reached unannotated frame.
- Integer multiplication is disjoint from float and other operator cases by
  operand sorts and operator string. It is the truthful equation
  `applyBin("*", I1, I2) = I1 *Int I2`.
- Return deliberately discards the remaining callee suffix, sets the return
  state, and `#pop` restores the caller continuation, environment, stack, and
  scope allocator. This is the required abrupt-return behavior.
- No heap allocation, exception, output, or other observable state change occurs.
- The only reached total functions are ordinary, exhaustive data helpers such
  as `builtinsScope` and `appendVal`; no reached result is supplied merely by a
  `total` annotation.

### Opaque and concrete-only symbols

The 25 supplied `symbol(...)` boundaries are:

`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`,
`sortKeyVS`, and `md5hexCodes`.

Twenty-two carry `no-evaluators`; the other three are concrete float conversion
symbols. None appears in the submitted AST, reachable cells, target
postcondition, or proof residual. There is therefore no result-bearing opaque
abstraction in this proof and no circular operational/postcondition dependency.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation evidence
was trusted. I created the fresh
[`spec-vacuity.k`](evidence/spec-vacuity.k), changing the exact destination from
`N*N` to `N*N + 1` while leaving the execution and all state obligations
unchanged. `N = 3` is a satisfying witness: both Python implementations and the
positive K ground claim return 9, while the mutation demands 10.

The mutation dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0 and emitted a valid `kore-exec ... --prove ...` command, establishing
successful parsing/building. See
[`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log).

The real mutated proof:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its implication residual compares
`N *Int N +Int 1` with the reached `N *Int N`, followed by the normal final
configuration. This is the expected unmet result obligation, not a parser
error, missing import, timeout, or unrelated crash. See
[`stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every K mathematical integer `N`, starting
from the exact clean configuration in `spec.k`, execution of the driver that
loads the exact submitted module and calls `car_race_collision(N)` reaches a
configuration whose computation result is exactly `N *Int N`, whose module
scope contains the exact submitted closure, and whose other listed cells are
restored or unchanged exactly as specified.

This is a partial-correctness statement in the Kit sense. For this loop-free,
exception-free path the reconstructed symbolic execution also reaches the
destination directly; no invariant, circularity, helper claim, or assumed
termination argument is involved.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser, kompilers, Haskell prover/backend, and built-in mathematical integer/map/list/string operations | Machine checking and `*Int` | Necessary low-level trusted computing base; freshly executed, not candidate-produced |
| Trusted supplied MPY semantics | Meaning of the generated AST and all state transitions | Required by `SUPPLIED_SEMANTICS`; candidate tree was recursively identical; every reached rule was statically checked |
| Trusted `py2mpy.py` | Link from `solution.py` to the AST proved | Acceptable: trusted translator generated byte-identical `solution.mpy` |
| Exact `solutionModule` macro spelling | Link from submitted `.mpy` bytes to K execution | Not an assumption after byte comparison and direct AST inspection |
| The 25 supplied opaque symbols listed in Stage 5 | Other MPY programs only | Unreachable and non-influential here; acceptable but not validated as universal Python semantics |
| Physical collision story implies one collision per cross-set pair | Natural-language intent to `n²` | Informal combinatorial bridge, supported by the trusted canonical implementation; not itself a K theorem |
| Finite differential and concrete runs | Empirical implementation/intent and concrete-semantics support | 513 Python comparisons and five K smoke inputs; supporting evidence only, not a substitute for the universal K proof |
| Missing generation records/trace | Historical provenance | Concerning auditability omission, but no dependency of reconstructed theorem closure |

### Gate accounting

- Real-program soundness: **PASS**. The real body executes; there is no
  operational bridge or result oracle; state/control are preserved; satisfying,
  body-sensitivity, and false-result witnesses behave correctly.
- Intent adequacy: **PASS**. The intended natural-number result is `n²`, the
  formal theorem proves the stronger all-K-Int program result, and canonical and
  submitted Python agree.
- Reviewer evidence reproducibility: **PASS**, with a candidate-provenance
  concern. Commands, statuses, scripts, inputs, mutations, and bounded outputs
  are preserved below `evidence/`; the candidate's own generation records are
  absent.

The missing provenance bundle warrants `CONCERNS`, but there is no material
soundness or adequacy gap and no basis for `NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
