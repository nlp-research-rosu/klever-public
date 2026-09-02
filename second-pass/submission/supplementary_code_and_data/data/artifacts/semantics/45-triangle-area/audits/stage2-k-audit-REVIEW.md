# Independent adversarial review: 45-triangle-area

The candidate's positive K claim does reconstruct to `#Top`, pins the submitted
constructor body, and rejects meaningful mutations. It is nevertheless not a
legitimate partial-correctness proof of the real Python program over the source
contract. The result-bearing `divII` primitive is opaque in the proof and its
supplied concrete equation disagrees with CPython on a satisfying input inside
the claim's unbounded integer domain. In addition, the claim materially narrows
an untyped length/height contract to integers and the submitted implementation
is not behaviorally identical to the trusted canonical at an unbounded-integer
boundary.

The complete command ledger is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). All builds and experiments used
fresh sources below `/tmp/audit-work/proof`; no candidate-provided compiled
definition or cache was copied or used.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `45-triangle-area`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- complete input provenance.

The rendered mode and mounts are consistent: the trusted
`/reference/reference-semantics` directory exists. This is not an infrastructure
breach.

I parsed the launcher record, campaign lock, `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, the complete 5,114-line `codex-output.log`, `prompt.txt`, and
all 107 JSONL events in the structured trace. `usage.json` is present even
though it is optional for this historical layout. Historical
`runtime-metrics.json` is absent and is not required for
`legacy-selected-stage1`.

The independently checked provenance facts are:

- `/audit-campaign-lock.json` is structurally identical to the campaign block
  and has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required record is readable, is the required real file/directory type,
  and is not a symlink. Every recorded individual-file hash and every evidence
  hash in `/generation-result.json` matches.
- An independent length-delimited tree digest of `/candidate` is
  `feda1cea532479721dbaa720ab401310790d9ec627b4f086c981c2b24beea079`,
  matching both the generation result and invocation workspace hashes.
- The corresponding trace-tree digest is
  `6a0bd4249eae81ae2418e7a133fbb2ce430e02eaec8f1d7c449d5461cd9c1e6d`,
  matching `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- The submitted and trusted supplied-semantics trees have identical entry
  names, types, modes, and file bytes. Their independently reproduced
  length-delimited tree digest is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded manifest digest. Neither tree contains a symlink,
  special entry, missing entry, or additional entry.

Evidence:
[`stage1-integrity.log`](evidence/stage1-integrity.log),
[`integrity_check.py`](evidence/integrity_check.py),
[`stage1-generation-record-summary.log`](evidence/stage1-generation-record-summary.log),
and
[`generation_record_summary.py`](evidence/generation_record_summary.py).
The generation records' earlier `#Top` and success marker were treated only as
untrusted claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `triangle_area(a, h)` to return the area of a triangle
from a side length and height, with example `triangle_area(5, 3) == 7.5`. It
states no integer type, positivity restriction, or magnitude bound. The trusted
canonical returns:

```python
return a * h / 2.0
```

The candidate returns:

```python
return a * h / 2
```

For ordinary bounded Python integers and floats these calculate the same
numeric value. They are not behaviorally identical throughout the unbounded
Python-integer domain.

### Translation identity

Running the trusted translator on the copied `solution.py` produced a byte-for-
byte identical `solution.mpy`. Both submitted and regenerated files have
SHA-256
`dfeb6ac63836b0ff5014334a279dd1e5f625a17de4a5aba7e45e034ccab07b8a`.
Evidence: [`stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

The independent test used `/reference/canonical.py` as oracle. It exercised the
documented example, zeros, signs, units, arity errors, large conversion
boundaries, floats, infinities, NaN, booleans, 2,000 seeded integer pairs, and
500 seeded finite-float pairs. There are no program branches; sign, zero,
numeric conversion, and arity are the material boundaries.

Of 2,518 ordinary cases, one diverged:

```text
a = 10**308
h = 2
canonical: OverflowError("int too large to convert to float")
submitted: 1e+308
```

The canonical first forms `2 * 10**308` and divides by the float literal `2.0`;
CPython's conversion of that numerator overflows. CPython's integer true-
division algorithm for the submitted `/ 2` expression returns the finite
`1e308`. The prompt has no magnitude bound, and these are positive integer side
and height values, so this is a material source-fidelity divergence rather than
an excluded test.

The script separately records broader numeric-protocol discrepancies:
`Decimal` operands raise in the canonical but return a value in the submitted
program, while `Fraction(1,3), Fraction(1,1)` return different value types and
unequal results. Those extra protocol cases are not needed for the verdict.

Evidence:
[`differential_test.py`](evidence/differential_test.py) and
[`stage2-differential.log`](evidence/stage2-differential.log). Exit 1 is the
script's deliberate mismatch signal, not a tool or infrastructure failure.

## 3. Clean proof reconstruction

I copied only candidate source proof artifacts and the trusted translator into
scratch, placed a fresh copy of the trusted supplied semantics at the relative
path imported by the proof, and regenerated both constructor programs. No
`*-kompiled` directory, candidate cache, or candidate-built definition was
reused.

Fresh LLVM reconstruction:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both commands exited 0. The four submitted small smoke assertions ended with
`.K`, `NoExc`, and modeled exit code 0. The compiler's non-exhaustiveness
warnings concern unused functions such as `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and out-of-bounds `valSeqAt`; none occurs on this target
path.

Fresh Haskell reconstruction and the only positive target claim:

```sh
kompile verification.k \
  --backend haskell \
  --main-module TRIANGLE-AREA-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-AREA-SPEC
```

The compile exited 0. `kprove` exited 0 and printed `#Top`. Evidence:
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log),
[`stage3-krun-smoke.log`](evidence/stage3-krun-smoke.log),
[`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log), and
[`stage3-kprove-positive.log`](evidence/stage3-kprove-positive.log).

This establishes proof closure under the submitted theory, not yet a validated
theorem about CPython.

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole entry claim has no explicit `requires` clause. Its sorted variables
and constructor arguments make its formal domain every pair of K integers
`A,H`. It starts in the exact initial module configuration: environment 0,
empty module scope with the builtins parent, empty heap and stack, allocation
locations 1 and 0, `noRet`, `NoExc`, and exit code 0.

It loads `triangleAreaProgram`, calls `triangle_area(Int(A), Int(H))`, and
requires termination with:

- `<k>` equal to `divII(A *Int H, 2)`;
- the exact function closure installed in module scope;
- the call frame removed and environment restored;
- unchanged empty heap/stack and allocation counters; and
- `noRet`, `NoExc`, and exit code 0.

The return is not a free variable, implication-only condition, or unconstrained
cell. It is syntactically result-constraining.

### Constructor and control-flow identity

A mechanical whitespace/comment-insensitive comparison proves that the
`triangleAreaProgram` rule's `Module(...)` right-hand side is exactly the
trusted-regenerated `solution.mpy` constructor tree. The claim explicitly
executes `#loadAll(triangleAreaProgram)` and then the named call.

The target path is:

1. `#loadAll` exposes the real `FuncDef`;
2. `FuncDef` installs its closure;
3. ordinary name lookup selects that exact binding;
4. call and argument rules evaluate `A` then `H`, create the function frame,
   and bind `a` and `h`;
5. `Return` strictness evaluates the nested multiplication before division;
6. integer multiplication produces `A *Int H`;
7. integer true division produces `divII(A *Int H, 2)`; and
8. `Return/#pop` restores all claimed cells.

There is no helper or loop claim. Evidence:
[`constructor_identity.py`](evidence/constructor_identity.py) and
[`stage4-constructor-identity.log`](evidence/stage4-constructor-identity.log).

### Satisfiability and substitutions

The entry state is concretely realizable, for example with `A=5,H=3`. The
claimed result substitutes to `divII(15,2)`, and both Python implementations
return `7.5`; the fresh concrete K smoke execution also accepts that equality.
The same agreement is recorded for `(0,9)` and `(-3,6)`.

At the equally satisfying formal input `A=10**308,H=2`, the claimed result is
`divII(2*10**308,2)`. The submitted Python implementation returns `1e308`,
the canonical raises `OverflowError`, and the concrete supplied semantics
rejects an assertion that the submitted function returns `1e308`. Evidence:
[`ground_witness.py`](evidence/ground_witness.py),
[`stage4-ground-witness.log`](evidence/stage4-ground-witness.log),
[`overflow-witness.py`](evidence/overflow-witness.py),
[`overflow-witness.mpy`](evidence/overflow-witness.mpy),
[`stage4-python-submitted-overflow.log`](evidence/stage4-python-submitted-overflow.log),
[`stage4-python-canonical-overflow.log`](evidence/stage4-python-canonical-overflow.log),
and [`stage4-krun-overflow.log`](evidence/stage4-krun-overflow.log).

### Body sensitivity

I changed the constructor actually executed by the claim from `a*h/2` to
`(a+h)/2`, changed the expected final closure to the same mutated body, and
left only the original result obligation unchanged. The mutated definition
built successfully. Its proof exited 1 with a meaningful stuck residual:

```text
divII(A +Int H, 2) == divII(A *Int H, 2)
```

Thus the theorem is sensitive to the executed body, rather than merely to an
external source file. Evidence:
[`verification-body-mutated.k`](evidence/verification-body-mutated.k),
[`spec-body-mutated.k`](evidence/spec-body-mutated.k),
[`stage4-body-mutation-kompile.log`](evidence/stage4-body-mutation-kompile.log),
and
[`stage4-body-mutation-kprove.log`](evidence/stage4-body-mutation-kprove.log).

### Adequacy failure

The formal claim only accepts `Int(A), Int(H)`. The prompt does not restrict
lengths to integers, the canonical and submitted programs both return the
expected value on ordinary float lengths such as `(5.5,3.25)`, and the supplied
syntax has float values. Excluding all non-integer lengths is a material
narrowing of the source-contract domain. Under this audit prompt's explicit
mapping, that limitation is `FAIL / NOT_LEGIT`, not a non-fatal concern.

Even within the formal integer domain, the concrete `divII` counterexample
below breaks the bridge to the real program.

## 5. Rule-by-rule static soundness review

The generated exhaustive inventory is
[`stage5-rule-inventory.md`](evidence/stage5-rule-inventory.md), produced by
[`build_rule_inventory.py`](evidence/build_rule_inventory.py). It lists the
complete source block, attributes, target-path relevance, and assessment for
every local entry:

- 228 syntax declarations;
- 696 rules;
- five contexts;
- one configuration;
- one claim;
- 147 function-bearing declarations;
- 108 total-bearing declarations;
- 45 priority-bearing entries;
- 35 concrete-bearing entries;
- 26 `owise` entries;
- 22 `no-evaluators` opaque declarations;
- four macro-bearing and one `macro-rec` declaration; and
- zero `functional`, alias, simplification, or `simp` declarations.

The 22 explicit `no-evaluators` symbols are `sortVS`, `sortKeyVS`,
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, and `md5hexCodes`.
`floorFI`, `toF`, and `ceilF` are also proof-opaque outside their
concrete-only equations. All except `divII` are inert on this constructor path.

The only candidate-local extension is:

```k
syntax Module ::= "triangleAreaProgram" [function, total]
rule triangleAreaProgram => Module(...)
```

This is a terminating definitional summary with one exact equation, no overlap,
no state effect, and constructor identity established mechanically. It is
sound.

The ordinary target-path rules for module loading, sequencing, definition
binding, local name lookup, left-to-right argument evaluation, call-frame
creation, parameter binding, strict `Return` evaluation, integer
multiplication, and frame popping preserve the complete configuration and
match this program's real control flow. None is an operational shortcut for
program-defined code. The target path uses no priority bridge; priority rules
for cell references, collections, methods, assertions, and math-call
interceptions are syntactically or sort-disjoint and unreachable here.

For every inventoried unused rule, I checked applicability and overlaps against
the submitted constructor path. I did not label an unused rule unsound without
a false conclusion witness on this task's intended inputs; the inventory
records the narrower finding that it is not exercised and supplies no
correctness conclusion to this proof.

### Result-bearing primitive failure

The decisive rule is
`reference-semantics/semantics/float.k:31`:

```k
syntax Float ::= divII(Int, Int)
  [function, total, symbol(divII), no-evaluators]
rule divII(I1:Int, I2:Int)
  => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11)
  [concrete]
rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

`divII` is result-bearing: it is the program's return value and the complete
postcondition. For symbolic proof it is opaque, and exactly the same symbol
appears on the operational path and in the destination. That shape is only
acceptable as an external trusted primitive if its stated contract is true on
the complete matched domain, or if the theorem is honestly reported as
conditional/interpretation-parametric.

The candidate comments identify it unconditionally as Python true division.
The concrete rule is not a universal connection theorem to CPython integer
true division. It converts the complete numerator to binary64 before dividing.
For `I1=2*10**308,I2=2`, that conversion overflows before the division, whereas
CPython evaluates the submitted integer `/` expression to finite `1e308`.

Concrete false-conclusion witness on the intended and formal domains:

```python
def triangle_area(a, h):
    return a * h / 2

assert triangle_area(10 ** 308, 2) == 1e308
```

The trusted-translated witness exits 0 in CPython but, under the supplied
concrete K semantics, reaches `AssertionError` and modeled exit code 1. Thus the
rule enables the false observable conclusion that this real program fails the
assertion. The witness is positive, integral, satisfies the claim's
precondition, has no source-contract magnitude exclusion, and does not rely on
division by zero or an unused construct.

The dispatch rule at `float.k:32` is structurally accurate only conditional on
the `divII` contract. Because the bridge is false on its accepted target
domain, the reconstructed `#Top` does not validate the claim as a theorem about
the real generated program. This is a Gate A soundness failure, not merely
thin empirical support.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh mutation preserved
the exact submitted program and all state obligations but changed the
postcondition from:

```k
divII(A *Int H, 2)
```

to:

```k
divII((A *Int H) +Int 1, 2)
```

It is demonstrably false for the satisfying state `A=5,H=3`: the real result is
`7.5`, while the mutation asks for `8.0`. The distinct spec parsed against the
fresh proof definition and executed. `kprove` exited 1 with
`WarnStuckClaimState`, and its residual showed precisely:

```text
divII(A *Int H +Int 1, 2) == divII(A *Int H, 2)
```

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash. The positive theorem is therefore
discriminating even though its Python bridge is invalid. Evidence:
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) and
[`stage6-false-postcondition-kprove.log`](evidence/stage6-false-postcondition-kprove.log).

## 7. Proven versus assumed accounting

### What the reachability proof actually establishes

Under the supplied symbolic K theory, for arbitrary K integers `A,H`, the exact
submitted constructor module loads, its exact function binding is called from
the pinned initial state, the body symbolically executes, and the final
configuration contains the opaque term `divII(A *Int H,2)` with the function
binding preserved and call state restored. This is a valid structural
reachability fact about that abstract theory. It does not establish that
`divII` denotes CPython's returned float on all those inputs, nor that the
integer-only theorem covers the source contract.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K toolchain v7.1.293 and standard `INT`, `BOOL`, `MAP`, `LIST`, strictness, and reachability machinery | Proof execution, mathematical integer multiplication, cells | Ordinary foundational trust; fresh build and mutation behavior are consistent. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Acceptable here: trusted hash matched and independent regeneration was byte-identical. |
| Candidate `triangleAreaProgram` function | Program term loaded by the claim | Acceptable: exact single equation, mechanical identity, body-sensitivity failure. |
| Fixed module/call/return operational rules | Binding, evaluation order, stack, scopes, return | Acceptable on this exact path; the complete footprint is pinned and no shortcut bypasses the body. |
| Opaque `divII(I1,I2)` and `[total]` assertion | Entire returned value and postcondition | Illegitimate for the advertised theorem. It is shared between execution and postcondition, has no valid bridge-free universal CPython connection, and its concrete equation has the preserved task-domain counterexample. |
| `Int2Float` and `/Float` hooks used by the concrete `divII` equation | Concrete interpretation of the result | These may faithfully implement their individual binary64 operations, but composing them after eager numerator conversion does not implement CPython integer true division. They do not repair the bridge. |
| Other 21 `no-evaluators` symbols and concrete-only opaque helpers | None on this program | Inert for all target claims; no verdict effect. |
| Candidate's four small smoke tests | Finite evidence for normal values | Reproducible but thin; they support only the tested inputs and miss the counterexample. |
| Independent differential evidence | Canonical/submitted and CPython/K bridges | 2,517 ordinary cases agree, but the one material ordinary mismatch invalidates universal fidelity. Finite agreement is not a theorem. |
| Mathematical statement “triangle area is `a*h/2`” | Human-facing intent | True informally for ordinary numeric lengths, but not formally connected to the opaque K result over the complete claim domain. |

Gate accounting:

- **Gate A — real-program soundness: FAIL.** Program identity and non-vacuity
  pass, but the result-bearing `divII` bridge is false on a satisfying claimed
  input.
- **Gate B — intent adequacy: FAIL.** The theorem materially restricts an
  untyped length/height contract to integers, and source fidelity also diverges
  at a positive unbounded-integer boundary.
- **Gate C — trust/evidence auditability: FAIL for the candidate's universal
  Python bridge.** Its only concrete support was four small smoke cases; there
  is no valid universal connection theorem, and independent evidence supplies a
  counterexample.

The positive `#Top`, exact body pinning, and successful non-vacuity gate do not
overcome a false result-bearing semantic bridge or the material domain
narrowing. Under the benchmark decision boundary, this is a reconstructed but
non-legitimate abstract proof rather than partial correctness of the real
generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
