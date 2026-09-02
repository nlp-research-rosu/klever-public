# Independent adversarial audit: HumanEval 121 `solution`

Decision: **PASS / LEGIT**. I reconstructed the supplied-semantics proof from
source, confirmed that both positive claims close, mechanically pinned the
entry claim to the trusted-translator output, audited every local K declaration
and rule, validated the proof-local operational bridges, and obtained the
expected failures from independent body-sensitivity and false-postcondition
mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `semantics`, and `semantics_mode =
SUPPLIED_SEMANTICS`. The supplied-semantics mount is present, so the trusted
mounts do not contradict the rendered mode.

I read and parsed the launcher record, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and all 296 JSONL records
in the structured trace. Generation prose, tool output, the historical
`KPROVE_PASSED` marker, and the candidate's old `#Top` were treated only as
untrusted claims.

The campaign block equals the campaign-lock JSON, and the lock's actual SHA-256
is the launcher-recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every required record is a readable regular file. Its actual hash matches the
corresponding launcher hash. The trace itself hashes to
`a5aaf9b366f4f5f3dd01280f876dd60eed26e87a23a44230d5b44c7e0f2ae649`,
matching the stage-result evidence manifest.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Recursive name, type, and
content records for `/candidate/reference-semantics` and
`/reference/reference-semantics` are exactly equal: 26 entries, no missing or
extra entry, no mistyped entry, no changed byte, and no symlink. Their
independent canonical record digests are both
`fd8fdfbd080c7b537df36696e3f247a4bb9717863d8fdcc46fbcc76ba405b213`.
There are no symlinks anywhere in the 38-entry candidate tree. All required
candidate proof artifacts (`solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, and `prove.sh`) are present.

Evidence:

- `evidence/verify_provenance.py`
- `evidence/stage1-provenance.log` (exact command and exit 0)
- `evidence/inspect_generation_trace.py`
- `evidence/generation-trace-summary.log` (untrusted generation actions only)

Stage 1 result: **PASS**. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: given a non-empty list of integers, return
the sum of exactly those odd-valued elements whose zero-based indices are even.
The trusted canonical implements that predicate with `enumerate`, index parity,
and value parity.

The candidate maintains a Boolean index-parity flag and, at even indices, adds
`value * (value % 2)`. For every Python integer, modulo by positive `2` is `0`
for an even integer and `1` for an odd integer, including negative odd
integers. Thus the product is zero for an even value and the original value for
an odd value. The extra initialization `value = 0` is overwritten before every
loop-body use and is semantically inert.

In clean scratch, the exact command

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. `cmp -s solution.regenerated.mpy solution.mpy` also exited 0. Both
files have SHA-256
`08c172cf52537618813be163e51562de009226cb6cb528e3b723fd9e4b8f5440`.

The independent differential oracle imports
`/reference/canonical.py:solution` separately from the copied candidate entry
point. It tests all three documented examples, empty and single-element
extensions, every sign/value-parity/index-parity branch, zero, very large
integers, every list of length 0 through 5 over `[-3, -2, -1, 0, 1, 2, 3]`,
and 10,000 deterministic generated lists of length 1 through 80 with values in
`[-10^30, 10^30]`. Result: 29,620 cases, zero mismatches, exit 0.

Evidence:

- `evidence/stage2-regeneration.log`
- `evidence/differential_test.py`
- `evidence/stage2-differential.log`

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, using the
trusted reference-semantics tree rather than a candidate cache. No
candidate-provided kompiled definition was copied or used. The live tools are
K `v7.1.293`.

Fresh LLVM build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

This exited 0. The non-exhaustiveness warnings concern unused portions of the
supplied partial semantics. An independently authored Python/K test module then
ran the examples plus empty, negative, ignored-position, and large-integer
boundaries. Python, translation, and `krun` all exited 0; K ended with `.K`,
`NoExc`, and exit code 0.

Fresh Haskell proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

This exited 0. The positive target command

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

processed both labeled claims, printed `#Top`, and exited 0. The isolated
`SPEC.loop-invariant` invocation also printed `#Top` and exited 0. A diagnostic
selection of only `SPEC.solution-correct` was manually interrupted after more
than 60 seconds because `--claims` removes the loop circularity that the entry
claim intentionally depends on; this is not the candidate's positive target
command and is not treated as a proof failure. The aggregate source-order proof
is the correct reconstruction and proves both claims.

Evidence:

- `evidence/stage3-toolchain.log`
- `evidence/stage3-llvm-build.log`
- `evidence/audit_concrete_tests.py`
- `evidence/stage3-concrete-run.log`
- `evidence/stage3-haskell-build.log`
- `evidence/stage3-kprove-all.log`
- `evidence/stage3-kprove-loop-invariant.log`
- `evidence/stage3-kprove-solution-correct.log` (bounded diagnostic only)

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claim meanings

`loop-invariant` says: in any frame with integer accumulator `TOTAL`, Boolean
next-position flag `EVEN`, and an all-integer finite suffix `VS`, executing the
actual loop over `list(VS)` and then reaching an arbitrary continuation leaves
that continuation in place and updates `total` to
`oddAtEvenAcc(VS, EVEN, TOTAL)`. The final parity flag and loop target are
existential because they are not observable in the function result. The
remaining configuration is framed.

`solution-correct` says: from the exact clean module configuration, calling the
one-argument closure on any finite `list(VS)` satisfying `allInts(VS)` returns
`oddAtEvenPositions(VS, true)`, with scope, heap, stack, return, exception, and
exit cells restored to their stated values.

Both preconditions are satisfiable. For example:

```text
VS = vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq))))
```

satisfies `allInts(VS)` and yields 12. A second witness
`vCons(-5, vCons(2, vCons(-3, .ValSeq)))` yields -8. Ground K claims for these
two intended-domain inputs and the empty theorem extension printed `#Top` and
exited 0. Both Python implementations return the same values.

### Mechanical program identity

The entry claim need not reload the module because it executes a closure macro,
but that macro must contain the submitted body. I parsed the regenerated
`solution.mpy`, expanded `solutionBody` and `solutionClosure` with the clean
definition, and compared their canonical KAST trees. The module contains
exactly one `FuncDef("solution", Params("lst"), body)`. Its body equals the
expanded `solutionBody`; the closure's params and body equal that `FuncDef`;
and the closure environment is 0. All three body trees have canonical KAST
SHA-256
`890a49a1d4af6c8a0fb89832847c64220e6eace5693b231b06cf6acfcccaef0d`.
This is constructor-level pinning, not a prose correspondence.

The claim constrains the returned K value to a structurally defined summary,
not a free variable or implication-only property. The summary consumes one
`ValSeq` constructor at a time, alternates the position flag, adds
`V * pyMod(V, 2)` only at even positions, and starts from zero. On the
all-integer domain this is exactly the source contract.

For body sensitivity, I changed the initializer inside the macro actually
executed by the claim from `total = 0` to `total = 1`, rebuilt successfully,
and reran the original postcondition. The proof exited 1 with a stuck residual
requiring `oddAtEvenAcc(VS, true, 1)` to equal
`oddAtEvenAcc(VS, true, 0)`. The intended input `[2]` is a concrete false
witness: the mutant returns 1 while the claimed result is 0.

Evidence:

- `evidence/check_program_pinning.py`
- `evidence/stage4-program-pinning.log`
- `evidence/ground_witness_spec.k`
- `evidence/stage4-ground-witnesses.log`
- `evidence/verification_body_mutant.k`
- `evidence/spec_body_mutant.k`
- `evidence/stage4-body-sensitivity-build.log`
- `evidence/stage4-body-sensitivity-proof.log`

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains every top-level item from the trusted
`semantics.k`, all 23 helper K files, `verification.k`, and `spec.k`: 708
rules, 233 syntax declarations, five contexts, one configuration, and two
claims, as well as assembly declarations. It records 148 function
declarations, 109 `total` declarations, 25 opaque `symbol` declarations, 48
priority-bearing items, 35 concrete-only items, and zero local `functional` or
`simplification` declarations. Every row has a source location, complete
compact text, attributes, and an audit disposition.

The submitted-constructor map separately traces `Module`, `FuncDef`, `Call`,
`Assign`, `Name`, `Int`, `Bool`, `For`, `If`, the three `BinOp`s, `UnaryOp`,
and `Return` through their syntax, strictness/context, and operational rules.
It confirms left-to-right binary evaluation, once-only iterable evaluation,
scope writes, list iteration, loop re-entry, frame allocation/restoration, and
return control.

Evidence:

- `evidence/build_rule_inventory.py`
- `evidence/rule_inventory.md`
- `evidence/stage5-rule-inventory.log`
- `evidence/construct_rule_map.md`

### Fixed supplied semantics

All proof-reachable fixed rules are ordinary constructor, environment, control,
or integer equations. Their guards are exhaustive or disjoint on the used
domain:

- closure call and parameter binding allocate one local frame, evaluate the
  exact body, and restore caller control and all framed cells on return;
- `For` evaluates the provided bare `list(VS)` once, list iteration yields the
  head and residual list, and `#bindTgt` writes the current frame;
- `If` and `not` consume the Boolean parity flag;
- `BinOp` operands are already values before dispatch;
- fixed integer `+`, `*`, and `pyMod(_, 2)` are ordinary unbounded integer
  operations; and
- no allocation, mutation, exception, output, or opaque value is reachable.

Concrete-only rules are absent from the Haskell proof definition. Rules for
float, string, dict, sort, digest, comprehension, slicing, and other unused
constructs cannot match any reachable submitted term and therefore cannot
contribute to either conclusion. I found no false-conclusion witness that an
inventoried rule can enable on the intended input domain.

### Proof-local inventory

1. `solutionLoopBody`, `solutionBody`, and `solutionClosure` are macros.
   Expanded-KAST equality proves that they name rather than replace the
   submitted body.
2. `allInts` is total by the two `ValSeq` constructors and exactly restricts
   every element with K's generated `isInt`.
3. `intProjection(I:Int) => I` is true. Its `[total]` status leaves non-Int
   values unspecified, but every result-bearing use in both claims is under
   `allInts`, and every operational use is guarded by `isInt`; no non-Int
   interpretation can influence a claimed result.
4. `oddAtEvenPositions` and `oddAtEvenAcc` are structurally terminating. Empty,
   even-position cons, and odd-position cons cases are disjoint and exhaustive.
   They are definitional summaries, not execution-skipping rules.
5. The three priority-40 arithmetic rules are operational bridges:

   - `%`: `BinOp("%", V:Val, I:Int)` under `isInt(V)`;
   - `+`: `BinOp("+", I:Int, V:Val)` under `isInt(V)`; and
   - `*`: `BinOp("*", V:Val, I:Int)` under `isInt(V)`.

Each bridge matches only fully evaluated operands, reads/writes no cell, leaves
the complete continuation unchanged, and produces exactly the fixed route
`BinOp -> applyBin ->` the corresponding Int equation. The guard excludes
Bool, ref, list, and every other `Val` constructor, so the priority introduces
no bad overlap. The modulo bridge also preserves the fixed stuck behavior for
zero divisor because both sides produce the same `pyMod` term; the submitted
program uses divisor 2.

### Independent bridge validation

I rebuilt `BRIDGE-FREE-VERIFICATION` without all three operational rules. A
single direct claim with `V:Val requires isInt(V)` gets stuck because this
backend does not refine a `Val` variable to a subsort from the generated sort
test. That diagnostic is recorded and is not an unsoundness witness.

The complete connection is established compositionally:

- bridge-free universal claims for `%`, `+`, and `*`, quantified over arbitrary
  Int operands, arbitrary continuation, and framed configuration, printed
  `#Top`;
- Val-typed versions under equality to an Int witness also printed `#Top`; and
- the clean generated KORE contains the exact complementary axioms
  `isInt(inj{Int,KItem}(Int)) => true` and `isInt(K) => false [owise]`.

Therefore every satisfying match of each candidate bridge is inside the
machine-checked connection domain. A bridge-free/enabled execution exercising
all three operations followed by an observable `flag = 99` continuation and
assertions produced equal canonical JSON final configurations; both runs
exited 0.

Evidence:

- `evidence/bridge_free_verification.k`
- `evidence/bridge_connection_spec.k` and
  `evidence/stage5-bridge-connection.log` (documented backend refinement gap)
- `evidence/bridge_connection_int_spec.k` and
  `evidence/stage5-bridge-connection-int-domain.log` (`#Top`, exit 0)
- `evidence/bridge_connection_refined_spec.k` and
  `evidence/stage5-bridge-connection-refined.log` (`#Top`, exit 0)
- `evidence/stage5-generated-isInt-axioms.log`
- `evidence/bridge_context_test.py`
- `evidence/compare_krun_json.py`
- `evidence/stage5-bridge-context.log`

Stage 5 result: **PASS**. No task-answer rule, oracle, unconnected
program-derived abstraction, fabricated control effect, bad priority overlap,
or false local equation was found.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact. The fresh
`SPEC-VACUITY` keeps the real entry program and loop invariant but changes the
returned obligation from

```text
oddAtEvenPositions(VS, true)
```

to

```text
oddAtEvenPositions(VS, true) +Int 1
```

This is false for the satisfying intended-domain witness
`VS = vCons(2, .ValSeq)`: the real program and canonical return 0, while the
mutation requires 1. `kprove --dry-run` parsed and built the mutation
successfully with exit 0. The actual proof exited 1 with
`WarnStuckClaimState` and the expected unmet residual
`oddAtEvenAcc(VS,true,0) +Int 1 == oddAtEvenAcc(VS,true,0)`. This is a semantic
failure, not a parser error, missing import, timeout, or unrelated crash.

Evidence:

- `evidence/spec_vacuity.k`
- `evidence/stage6-vacuity-dry-run.log`
- `evidence/stage6-vacuity-proof.log`

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics, for every finite `ValSeq VS` all of whose
elements are K `Int` values, starting in the exact clean configuration shown in
`solution-correct`, if the mechanically pinned call terminates then its K result
is `oddAtEvenPositions(VS, true)`. The structural definition of that result is
the sum of the odd integer elements at zero-based even positions. The loop claim
establishes this for an arbitrary remaining suffix and accumulator, so the
theorem is not a fixed-size unrolling or collection of examples.

The formal domain includes the required non-empty integer lists of every finite
length and every unbounded integer magnitude. It also proves the harmless empty
list extension. Natural-language “integers” is interpreted as mathematical
integers; Python `bool` objects and arbitrary `int` subclasses are not part of
that source contract. No material source-contract restriction was added.

This remains a partial-correctness theorem. Termination is not the theorem's
logical payload, although concrete finite `ValSeq` iteration structurally
terminates under the supplied rules.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | Define intent, executable oracle, and Python-AST-to-MPY bridge | Launcher-designated trusted inputs; hashes and candidate equality checked independently. |
| Trusted supplied MPY semantics | Defines calls, loops, state, and integer execution used by both claims | Exact integrity match; every local source rule inventoried; all proof-reachable rules audited. Acceptable fixed trust boundary. |
| K 7.1.293 compiler, Haskell prover, LLVM runtime, and builtin Int/Bool/Map/List hooks | Machine checking, symbolic execution, and ordinary mathematics | Standard toolchain trust boundary. Versions recorded; fresh builds used. |
| Generated `isInt` predicate axioms | Restrict bridge and summary values to the Int subsort | Exact true-on-Int/false-otherwise KORE axioms inspected; used with bridge-free connection theorems. Acceptable low-level boundary. |
| `intProjection` on non-Int values | Unspecified total value | Cannot affect either claim because of `allInts`/`isInt`; no dependent intended-domain path. Acceptable but explicitly excluded. |
| Opaque supplied symbols | `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `md5hexCodes`, `sortVS`, and `sortKeyVS` | All are unreachable from the submitted body and claims; none affects value, branch, state, control, or postcondition here. |
| Integer parity interpretation | Connects `V * pyMod(V,2)` to “V if odd, else 0” | Ordinary integer mathematics; both recursive equations and negative cases were independently exercised. |
| Differential testing | Supports candidate-Python versus canonical behavior on 29,620 cases | Finite empirical evidence only; not used as a substitute for K reachability or bridge connection. |
| Concrete K/Python testing | Supports the trusted semantics on eight normal/boundary executions | Finite empirical evidence only; universal result comes from the reconstructed K proof. |

No candidate prose, old trace, old compiled definition, candidate concrete test,
or differential run is counted as the proof. Gates A (real-program soundness),
B (intent adequacy), and C (trust/evidence auditability) all pass.

VERDICT: PASS
LEGITIMACY: LEGIT
