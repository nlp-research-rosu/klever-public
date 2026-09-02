# Independent adversarial audit — 148-bf

The candidate contains a legitimate partial-correctness proof for the submitted
program under the supplied semantics. I reconstructed the definitions from
source, obtained a fresh `#Top`, mechanically pinned the proof term to the
translated program body, reviewed all source-level K entries, and obtained the
expected failures from both a false-result mutation and an executed-body
mutation.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3`,
`condition: semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, as required for that mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required files at the root of
`/generation-evidence`, and all 622 JSON records in the single structured trace
file. The generation prose, transcript, compiled directories, and prior
`KPROVE_PASSED` assertion were treated only as untrusted historical claims.

Independent checks found:

- `/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block and
  its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every pipeline-v3 required record is a regular readable file or directory of
  the expected kind. The trace has one regular JSONL file and no malformed
  record.
- The recorded SHA-256 values for the run/task/result/invocation manifests,
  prompt, metrics, runtime metrics, usage, transcript, final message, trusted
  canonical, prompt, and translator all equal hashes independently computed
  from the mounted files.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Candidate `reference-semantics/` and trusted
  `/reference/reference-semantics/` have exactly the same 25-entry recursive
  manifest, types, paths, sizes, and file hashes. Neither tree contains a
  symlink. The reviewer-defined manifest digest for either tree is
  `a672ebc5644e3ffe3d963c31999f660850e86840b0c497807fea7c85e6706751`.
- All required proof artifacts—`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`—are regular files.

The complete checker and transcript are
[provenance_check.py](/audit-output/evidence/provenance_check.py) and
[stage1-provenance-final.log](/audit-output/evidence/stage1-provenance-final.log).
The earlier `stage1-provenance.log` records a reviewer-script comparison error:
the embedded task block has a launcher-added `config` key absent from
`/task.json`. Correcting that reviewer-only comparison produced the clean run;
it was not a mount or candidate discrepancy.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for `bf(planet1, planet2)` on string inputs. The
planet order is Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.
For two valid names, the result must be the tuple of planets strictly between
them in solar order. If either name is invalid, the result must be empty.
Equal valid names consequently have no planet strictly between them.

The trusted canonical implementation explicitly rejects equal names, looks up
the two indices, and returns the corresponding open slice. The candidate omits
the explicit equality test; its reversed/equal branch evaluates
`planets[second + 1:first]`, which is empty when the indices are equal. Thus the
two implementations agree on that boundary.

Running the trusted translator over the mounted `solution.py` recreated the
submitted `solution.mpy` byte-for-byte. Both SHA-256 values are
`3f657ffd4d066c0d77ca1927b490720f80cac27830b713caaf4bdf9cfee6a7fa`;
see [stage2-regeneration.log](/audit-output/evidence/stage2-regeneration.log).

The independent differential test imports both entry points and also uses a
third, index-free contract oracle. Its 939 unique string pairs include:

- all three documented examples;
- all 64 ordered pairs of valid names, including equal, adjacent, first/last,
  and both orderings;
- empty, case-shifted, whitespace-adjacent, NUL-containing, and Unicode
  invalid strings in both argument positions; and
- 200 deterministic generated invalid strings with seed 148.

There were zero mismatches. The script and successful transcript are
[differential_test.py](/audit-output/evidence/differential_test.py) and
[stage2-differential-final.log](/audit-output/evidence/stage2-differential-final.log).
The preserved first run found seven discrepancies caused by my oracle failing
to special-case equal valid names; both Python implementations returned the
correct empty tuple. I fixed the reviewer oracle and retained that diagnostic
as `stage2-differential.log`.

Program fidelity passes.

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the trusted mounted inputs to
`/tmp/audit-work/148-bf-audit`. I did not copy or use
`/candidate/runtime-kompiled`, `/candidate/verification-kompiled`,
`/candidate/__pycache__`, or any candidate cache.

The active toolchain is K v7.1.293 and Python 3.10.12
([stage0-toolchain.log](/audit-output/evidence/stage0-toolchain.log)).
Fresh builds were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module BF-VERIFICATION --syntax-module BF-VERIFICATION \
  --output-definition reviewer-verification-kompiled
```

Both exited 0. Logs are
[stage3-kompile-llvm.log](/audit-output/evidence/stage3-kompile-llvm.log) and
[stage3-kompile-haskell.log](/audit-output/evidence/stage3-kompile-haskell.log).

The original positive target command was then run unchanged except for the
fresh definition name:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module BF-SPEC
```

It processed all three claims, exited 0, and printed `#Top`. The bounded
transcript is
[stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log).

I also translated and ran an independently authored concrete program containing
the submitted function plus ten normal/boundary assertions through the fresh
LLVM definition. Python execution, translation, and `krun` all exited 0; see
[concrete-tests.py](/audit-output/evidence/concrete-tests.py) and
[stage3-concrete-tests.log](/audit-output/evidence/stage3-concrete-tests.log).

The LLVM compiler warned that several supplied `[total]` functions are not
constructor-exhaustive. This is addressed under Stages 5 and 7; it did not
prevent either fresh build or touch an unconstrained case in this proof.

Clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Claim meanings and coverage

The first entry claim starts at `#validCases(0, 0)` in the ordinary initial
configuration. Three disjoint controller rules traverse

```text
(0,0), (0,1), ... (0,7), (1,0), ... , (7,7)
```

exactly once. At each of the 64 states it calls the submitted function body on
the corresponding valid names and executes a real `Assert` comparing the
return to the explicit open interval in the eight-planet sequence. The claim's
destination requires `.K`, `NoExc`, and exit code 0. A false assertion changes
the latter two cells, so this is result-constraining even though 64 return
checks are combined into one reachability claim.

The second entry claim quantifies over arbitrary `IntSeq` values `A` and `_B`.
Its precondition says `A` differs from every valid planet encoding. It proves
that calling the body on `str(A), str(_B)` returns the empty tuple. This covers
every first-invalid string and relies on the program's real short-circuiting,
which correctly makes the second value irrelevant.

The third entry claim says `A` equals one of the eight valid encodings while
`B` differs from all eight. It proves the same empty tuple for every
valid-first/invalid-second string pair.

These domains are exhaustive for the contract's string inputs:

```text
both valid (8 × 8)  OR  first invalid  OR  first valid and second invalid.
```

The finite 64-case component is not a bounded approximation of an unrestricted
valid domain: the source contract has exactly eight valid names. All remaining
strings are covered symbolically rather than by examples.

Each entry precondition has a concrete witness. The reviewer claims use
Mercury/Neptune for the valid component, `""`/Neptune for first-invalid, and
Earth/`""` for valid-first/second-invalid. They prove respectively the literal
six-planet tuple and two literal empty tuples, print `#Top`, and exit 0
([spec-ground-witnesses.k](/audit-output/evidence/spec-ground-witnesses.k),
[stage4-ground-witnesses.log](/audit-output/evidence/stage4-ground-witnesses.log)).
The same results agree with both Python implementations in Stage 2.

### Program identity

Trusted regeneration establishes the `solution.py` to `solution.mpy` link. To
check the next link mechanically, I extracted the sole translated function
body using the trusted translator, parsed it as `Stmts`, expanded macros with
the fresh definition, and compared its KORE to expanded `bfBody`. The KORE
files are byte-identical and both hash to
`644ce421a13ba7d711e970a2448745204080a98b6c33ca4a964b00488bb61d7d`;
see [stage4-body-pinning.log](/audit-output/evidence/stage4-body-pinning.log).

`bfRun` is a syntax macro, not an execution rewrite. Its closure has the exact
source name-independent invocation data: parameters `planet1, planet2`, no
remaining parameters, the identical `bfBody`, and definition scope 0. Under
the fixed `FuncDef` rule, loading the actual module binds exactly
`closureVal(Params, Body, 0)` in the initial module scope; `bfRun` directly
constructs that same closure value. It then enters the ordinary fixed call,
binding, body, return, and frame-pop rules. The proof therefore omits only
module-load steps already accounted for by this mechanical constructor
comparison; it does not substitute a different function or summary.

As a separate body-sensitivity test, I changed the `"Earth"` literal in the
executed `bfBody` to `"EarthX"` while leaving the result definition unchanged.
The mutated definition built successfully, but its target proof exited 1 with
`WarnStuckClaimState`, `AssertionError`, and exit code 1. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[spec-body-mutated.k](/audit-output/evidence/spec-body-mutated.k),
[stage4-body-mutation-kompile.log](/audit-output/evidence/stage4-body-mutation-kompile.log)
and
[stage4-body-mutation-proof.log](/audit-output/evidence/stage4-body-mutation-proof.log).
This mutation changes the K term actually executed by the claim.

Real-program pinning and adequacy pass.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), generated by
[rule_inventory.py](/audit-output/evidence/rule_inventory.py). It contains 970
source-level entries: 727 rules, 237 syntax declarations, five contexts, and
one configuration. Every entry records its source and line, complete normalized
text, attributes (`function`, `total`, `macro`, `priority`, `owise`,
`concrete`, `no-evaluators`, and others), semantic role, and audit disposition.
Per-file counts are in
[rule-inventory-summary.txt](/audit-output/evidence/rule-inventory-summary.txt).

### Used-constructor map

| Submitted construct | Declaration and material rule families |
|---|---|
| `Module`, `FuncDef`, direct closure call | `syntax.k`; `core.k` load/sequence/lookup; `functions.k` define/bind/return/pop; `call.k` callee/arguments/closure dispatch |
| `Assign`, `Name` | `syntax.k`; `controls.k` assignment; `core.k` lexical lookup |
| `TupleExpr`, tuple membership/equality/index | `tuple.k`; shared argument evaluation in `core.k`; membership fold in `list.k` |
| `Str`, arbitrary string values | `str.k` literal/code rules and structural equality |
| `BoolOp("or")` | left-to-right contexts and disjoint truthy branches in `bool.k` |
| `Compare("not in")`, integer `<` | `operators.k`, `tuple.k`, `list.k`, and `int.k` |
| `Call(Attribute(..., "index"), ...)` | bound-method and argument routing in `call.k`; `idxOfVS` in `tuple.k` |
| `Int`, `BinOp("+")`, `If` | `core.k`, `int.k`, and `controls.k` |
| `Subscript(..., Slice(...))` | bound evaluation, clamping, and `buildVS` in `subscript.k` |
| `Return` | strict value evaluation and frame restoration in `functions.k` |
| proof-harness `Assert` | `assert.k`; failure changes `<exc>` and `<exit-code>` |

The relevant rules preserve left-to-right evaluation, create one fresh function
scope, bind the two parameters and locals there, read the immutable tuple
structurally, and restore the initial environment/scope/stack/return cells on
pop. Tuple literals and tuple slices are values, so this program performs no
heap allocation. Membership and `idxOfVS` descend through ground
constructor sequences. Slice bounds are ground non-negative indices in
`0..7`, the step is `noB`/1, and every `valSeqAt` call made by `buildVS` is
in-bounds.

### Proof-local entries

The local theory has:

- `bfBody`, `bfCall`, and `bfRun` macros. `bfCall` is unused; `bfBody` and
  `bfRun` are mechanically pinned as described above.
- Four total mathematical definitions: nullary `planetVals`,
  `expectedBetween(Int,Int)`, and exhaustive maps `planetCodes(Planet)` and
  `planetPosition(Planet)`. The last two are unused by the final claims.
- A finite eight-constructor `Planet` sort and eight ground `planetExpr`
  equations. `planetExpr` is not declared total and is called only at its eight
  defined ground arguments.
- Three mutually exclusive `#validCases` rules. Their transition graph has
  exactly 64 unique states and no gap or duplicate.

There is no proof-local `claim`, simplification, priority, `owise`,
`no-evaluators`, fresh opaque result, oracle, or rule that rewrites a submitted
program operation to its answer. `expectedBetween` occurs only on the expected
side of an assertion; it does not replace execution. `#validCases` is a fresh
controller that schedules real body calls and assertions, and it reads/writes
no program state beyond the standard `<k>` sequencing. Mechanical checks are
in
[proof_local_checks.py](/audit-output/evidence/proof_local_checks.py) and
[stage5-proof-local-checks-final2.log](/audit-output/evidence/stage5-proof-local-checks-final2.log).

The expected result reuses supplied `doSlice`, but this is not a circular
proof-local abstraction: the candidate body still must compute the correct two
indices, choose their order, and execute its own slice. Static inspection of
the relevant supplied equations shows that for the only admitted domain
(length 8, non-negative endpoints, step 1), `slStart`/`slStop` clamp correctly
and `buildVS` returns exactly the strict open interval. The literal
Mercury/Neptune witness independently fixes the six returned strings rather
than leaving `doSlice` opaque.

### Supplied-semantics boundary

The imported fixed semantics contains opaque float/sort/digest symbols:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None
appears in the program term, the expected result, a guard, or a claim.

The LLVM warnings identify non-exhaustive total functions such as `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. All but `valSeqAt` are
outside the dynamic trust cone. `valSeqAt` is reached only on concrete
nonempty `vCons` sequences at an in-bounds non-negative index, where an
ordinary defining equation applies; the unconstrained total case is never
used. Consequently these broad supplied declarations create no false
conclusion witness for this theorem. I do not label them unsound merely from a
global coverage warning; they are recorded as trust-boundary limitations.

No inventoried proof-local or relevant supplied rule enables a false conclusion
on the intended input domain. Static soundness passes.

## 6. Fresh non-vacuity test

I authored
[spec-vacuity-reviewer.k](/audit-output/evidence/spec-vacuity-reviewer.k). It
uses the concrete satisfying input Mercury/Neptune but falsely requires the
empty tuple.

The dry run parsed and built the claim successfully with exit 0
([stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log)).
The actual proof exited 1 with `WarnStuckClaimState`. Its residual displays the
six actual values Venus, Earth, Mars, Jupiter, Saturn, Uranus against the false
empty target
([stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log)).

This is a reachable, result-bearing failure, distinct from the executed-body
mutation in Stage 4. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied semantics and the standard initial configuration, the exact
submitted `bf` body has the following partial-correctness behavior for every
pair of string values:

- if both values are the encodings of valid planet names, the returned tuple is
  exactly the planets strictly between them in the fixed solar order;
- if either value is not a valid name, the returned tuple is empty; and
- execution returns with the initial module environment restored, empty heap
  and stack, `noRet`, `NoExc`, and exit code 0.

The valid part is an exhaustive proof over the contract's finite 8×8 valid
domain. The invalid part is symbolic over arbitrary `IntSeq` string contents.
This is not merely differential testing and not merely the historical
candidate `#Top`; it is the fresh reachability result in Stage 3.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler, Haskell backend, reachability engine, SMT solver, and built-in integer/Boolean/String/Map/List hooks | All machine-checked claims | Necessary low-level proof-system trust; version and fresh outputs are recorded. |
| Byte-identical supplied semantics | Meaning of calls, strings, tuples, control, slices, and assertions | Selected fixed-semantics boundary. All source entries were inventoried; the relevant trust cone was reviewed rule-by-rule. |
| Trusted `py2mpy.py` | Source-to-`solution.mpy` link | Acceptable benchmark input. Byte regeneration and KORE body comparison independently check its use on this source. |
| Direct-closure normalization in `bfRun` | All entry claims | Acceptable and mechanically justified: name/parameters/body/scope anchor equal the closure created by fixed module-load semantics. It skips no function-body operation. |
| K `str(IntSeq)` representation of arbitrary Python strings | Symbolic invalid-input coverage | Non-fatal representation bridge. Valid literals are ASCII and ground; every other `IntSeq` is handled uniformly as invalid. Python Unicode/NUL cases were additionally tested, but finite tests are only evidence for this bridge. |
| `planetVals`, min/max, and supplied ground slice equations as the natural-language “between” interpretation | Valid-pair postcondition | Ordinary finite mathematics, statically checked for all eight positions and backed by literal ground witness claims. No opaque answer symbol is involved. |
| Imported float/sort/MD5 opaque symbols and unrelated broad total declarations | None of these claims | Inert. They affect neither control nor result and are not assumptions of this theorem. |
| Python differential tests | Source/canonical agreement and representation evidence | Empirical support only; not used as a substitute for the K proof. |

Gate A (real-program soundness and non-vacuity), Gate B (intent/domain
adequacy), and Gate C (trust/evidence auditability) all pass. The full exact
command index, including reviewer-script diagnostics and every exit status, is
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
