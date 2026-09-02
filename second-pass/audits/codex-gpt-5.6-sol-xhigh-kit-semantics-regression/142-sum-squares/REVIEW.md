# Independent adversarial review: 142-sum-squares

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed both proof definitions from source, independently
proved both positive claims, checked that the entry claim embeds the regenerated
program, reviewed every source-level K rule, and obtained the expected stuck
residual from a fresh false postcondition. The candidate's prior `#Top`,
compiled directories, logs, trace, and `PROOF.md` were not reused as authority.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with that mode: `/reference/reference-semantics` exists. There is therefore no
infrastructure breach.

I read the candidate's `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the one structured trace only as untrusted claims. The
trace has 742 valid JSONL records and no malformed record. Those artifacts claim
successful proofs and validation, but none was used to establish this verdict.
Their hashes, sizes, claimed metadata, and bounded summaries are in
[`01-provenance.log`](evidence/01-provenance.log); the reader is
[`provenance_audit.py`](evidence/provenance_audit.py).

All required candidate artifacts are ordinary files or directories. There are
no symlinks anywhere under `/candidate`. In particular:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- A recursive content comparison and a separate path/type manifest comparison
  both show exact identity between `/candidate/reference-semantics` and
  `/reference/reference-semantics`.
- The candidate semantics tree has no missing, additional, mistyped, changed, or
  symlinked entry.
- `solution.py`, `solution.mpy`, `verification.k`, and `spec.k` are present as
  ordinary files.

The exact checks all exited 0; see
[`01-integrity.log`](evidence/01-integrity.log) and
[`integrity_check.sh`](evidence/integrity_check.sh). Candidate-provided
`*-kompiled` directories, bytecode, caches, logs, mutations, and reports are
additional non-source artifacts outside the integrity-controlled semantics
tree. I ignored them. There is no missing, changed, extra, mistyped, or
symlinked required artifact to report.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For a finite list of integers, use zero-based indices. Square an element at an
index divisible by 3. Otherwise cube it if the index is divisible by 4.
Otherwise leave it unchanged. Return the sum of those contributions. Thus an
index divisible by both 3 and 4 takes the square branch, and the empty list
returns 0.

The trusted canonical implementation constructs the transformed list and calls
`sum`. The submitted `solution.py` instead maintains `total` and `index` while
iterating directly over the input. Its `elif index % 4 == 0` is equivalent to
the prompt's additional “not divisible by 3” condition because the preceding
`if index % 3 == 0` has already failed. It does not mutate the input. Over the
stated domain, this is a faithful alternative algorithm.

### Translation identity

I copied `solution.py` and the submitted `solution.mpy` into scratch, copied the
trusted `/reference/py2mpy.py`, and ran:

```text
python3 /tmp/audit-work/142-sum-squares/py2mpy.py \
  /tmp/audit-work/142-sum-squares/solution.py \
  > /tmp/audit-work/142-sum-squares/solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`ddffe8eb486904178e20562c853356ac3649e34976571477af2eb62b0f478148`;
`cmp` exited 0. The exact record is
[`02-translation.log`](evidence/02-translation.log), driven by
[`translate_check.sh`](evidence/translate_check.sh).

### Independent differential test

[`differential_audit.py`](evidence/differential_audit.py) imports the trusted
canonical entry point and the copied candidate entry point from distinct
explicit paths. It also uses an independently written direct contract oracle.
The preserved deterministic input set is
[`differential-inputs.jsonl`](evidence/differential-inputs.jsonl), SHA-256
`dc35631c4481a9f0950eea29e143b2fcc78b3dc423c330ae164c6bf55f772c8f`.

The 10,351 cases comprise:

- all three documented examples;
- empty and every prefix length 0 through 14 of a signed marker sequence,
  exercising unchanged, square-only, cube-only, and the index-12
  both-divisible precedence boundary;
- very large positive and negative Python integers;
- all lists of length 0 through 5 over `{-3,-1,0,1,2,4}` (9,331 cases);
- 1,000 deterministic random lists of length 0 through 40.

The command `python3 /audit-output/evidence/differential_audit.py` exited 0 with
`MISMATCHES=0`. Complete bounded output is in
[`02-differential.log`](evidence/02-differential.log). This supports program
fidelity and the intent bridge; it is not used as a substitute for the K proof.

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to
`/tmp/audit-work/142-sum-squares`. No candidate-provided compiled definition or
cache was copied or referenced. The available K toolchain is v7.1.293.

### Fresh concrete definition

I built the supplied source semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The command exited 0
([`03-kompile-llvm.log`](evidence/03-kompile-llvm.log)). I translated the
reviewer-authored [`concrete_checks.py`](evidence/concrete_checks.py) with the
trusted translator and ran the resulting
[`concrete_checks.mpy`](evidence/concrete_checks.mpy) under both CPython and the
fresh LLVM definition. Both commands exited 0, including empty, documented,
negative, cube, and index-12 precedence cases:
[`03-concrete-cpython.log`](evidence/03-concrete-cpython.log) and
[`03-concrete-krun.log`](evidence/03-concrete-krun.log).

The LLVM build reports non-exhaustiveness warnings for some supplied total
helpers involving `cellsMark`, floats, joins, and out-of-bounds sequence access.
None of those symbols or sorts occurs in the submitted program or its proof.
They are unchanged trusted-baseline code and do not feed a proof-local
extension.

### Fresh proof definitions and every positive claim

I independently built the two Haskell definitions:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exited 0; see
[`03-kompile-haskell-base.log`](evidence/03-kompile-haskell-base.log) and
[`03-kompile-haskell-final.log`](evidence/03-kompile-haskell-final.log).

`spec.k` has exactly two positive target claims. Both were run independently:

```text
kprove spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
# #Top; exit 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC
# #Top; exit 0
```

The unabridged bounded records are
[`03-kprove-loop.log`](evidence/03-kprove-loop.log) and
[`03-kprove-entry.log`](evidence/03-kprove-entry.log). Each contains `#Top` and
`EXIT_STATUS: 0`. Clean reconstruction therefore passes.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`LOOP-SPEC.loop` has no explicit `requires` clause. Its precondition is the
fully specified loop-head configuration:

- remaining iterator `list(intVals(IS))`;
- the submitted `value` target and exact submitted two-branch body;
- continuation exactly `Return(Name("total")) .Stmts ~> #endcall`;
- local frame 1 with arbitrary integer `index=I`, integer `total=A`, arbitrary
  old `value`, and an arbitrary integer-list binding for `lst`;
- caller/module frame 0, arbitrary supplied builtins scope, `scopeLoc=2`,
  empty heap at location 0, exact `frame(.K,0,1)`, `noRet`, `NoExc`, and exit
  code 0.

Its postcondition says that executing that remaining loop, return, and frame
pop yields `sumSquaresFrom(IS,I,A)` in `<k>`, restores environment 0, removes
frame 1, restores `scopeLoc=1`, and preserves the other observable cells.

`SPEC.entry` also has no explicit `requires` clause. Its precondition is the
standard initial configuration and an arbitrary finite `IS:IntSeq`. It loads a
literal `Module(FuncDef(...))`, calls `sum_squares` with
`list(intVals(IS))`, and requires the result to be
`sumSquaresFrom(IS,0,0)`. Its post-state also pins the exact installed closure
and every configuration cell.

### Pinning results

The independent structural checker
[`pinning_and_witness.py`](evidence/pinning_and_witness.py) establishes:

```text
ENTRY_LOADS_EXACT_SOLUTION_MPY=True
LOOP_TARGET_MATCHES_REAL_FOR=True
LOOP_BODY_MATCHES_REAL_FOR=True
LOOP_BRIDGE_CONTEXT_IDENTICAL_TO_LOOP_CLAIM=True
ALL_STRUCTURAL_PINNING_CHECKS=True
```

The first comparison normalizes only explicit `.Stmts` list terminators: the
translator omits surface units that the spec spells out, but the parsed K list
term is the same. No program constructor, operator, literal, name, or body
statement is normalized away. The complete result is
[`04-pinning-witness.log`](evidence/04-pinning-witness.log).

The entry proof therefore executes definition loading, name lookup, argument
evaluation/binding, all three initial assignments, and the real loop body. It
does not prove a substituted function. The main bridge matches exactly the
independently proved loop configuration, including the return continuation,
call terminator, stack frame, scopes, heap, return state, exception state, and
exit code. It has no broader continuation wildcard.

The arbitrary `INPUT` and `OLD` variables in the loop theorem are not result
oracles. Once the iterator has been constructed, the body never reads `lst`,
and the next yield overwrites `value`; the theorem is simply stronger than its
reachable instances. In the actual entry path, `INPUT` is the original input.

### Satisfying states and concrete substitutions

An entry witness is `IS=.IntSeq` in the exact initial configuration. It
satisfies every precondition and all three interpretations give 0. The evidence
also substitutes `[1,2,3]`, `[-1,-5,2,-1,-5]`, and
`[2,-3,5,-7,11]` into `sumSquaresFrom`; the formal fold, trusted canonical, and
candidate Python results are respectively 6, -126, and 1386.

A reachable nonempty loop witness is the state after consuming the first four
elements of `[2,-3,5,-7,11]`:
`IS=iCons(11,.IntSeq)`, `I=4`, `A=55`, `OLD=-7`, with the exact cells listed
above. The claimed suffix result is `55 + 11^3 = 1386`, equal to both Python
implementations. The complete serialized states appear in
[`04-pinning-witness.log`](evidence/04-pinning-witness.log).

The returned value is not free and the postcondition is not tautological:
`sumSquaresFrom` is recursively constrained by exhaustive equations, and the
entry RHS uses the same symbolic `IS` supplied to the actual call.

## 5. Rule-by-rule static soundness review

### Exhaustive inventories

[`05-rule-inventory.log`](evidence/05-rule-inventory.log) contains every
numbered source line and a declaration index for `semantics.k`, all 22 supplied
helper K files, `verification.k`, and `spec.k`.
[`05-rule-review-ledger.log`](evidence/05-rule-review-ledger.log) gives one
explicit decision, source location, module, attributes, normalized full rule,
and rationale for every one of the 705 source-level rules:

```text
FIXED_USED=38
FIXED_BRIDGE_PREMISE=2
FIXED_RUNTIME_ONLY=16
FIXED_UNUSED=639
DEFINITIONAL=7
OPERATIONAL_BRIDGE=3
TOTAL_RULES=705
```

The first four categories are the 695 byte-verified supplied-semantics rules.
The selected semantics is the trusted normative level in this mode. I checked
the 38 rules on the proof path and the two list-iterator premises against the
program's evaluation, binding, control, cells, and arithmetic. The other fixed
rules have redexes or sorts absent from `solution.mpy`; no proof-local equation
calls them, so they cannot contribute a false conclusion to this theorem.
`MPY-CONCRETE` is runtime-only and is not imported into either Haskell proof
definition.

The exact declaration/attribute census is in
[`05-declaration-attributes.log`](evidence/05-declaration-attributes.log):
230 syntax headlines, 151 declaration lines carrying `function`, 112 carrying
`total`, 25 carrying `symbol`, 22 carrying `no-evaluators`, 48 priority rules,
35 concrete rules, 26 owise rules, five contexts, one configuration, and two
claims. There are zero `functional`, `simplification`, or `anywhere` entries.
This evidence enumerates each decorated declaration and rule rather than only
reporting counts.

The 22 supplied opaque/no-evaluator symbols are `md5hexCodes`; `sortVS` and
`sortKeyVS`; and the float helpers `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. The additional supplied `symbol` declarations `floorFI`, `toF`, and
`ceilF` have concrete equations. None of these 25 symbols occurs in the
program, spec postcondition, loop theorem, or a proof-local definition. There
is no proof-local opaque primitive.

### Construct-to-semantics map

| Submitted construct | Declaration and rules used |
|---|---|
| `Module`, `Stmts` | `syntax.k:56,61`; `core.k:124-127` loads and sequences |
| `FuncDef`, `Params` | `syntax.k:53,57,60`; `functions.k:14-16` installs the exact closure |
| `Call(Name(...), ...)` in the entry | `syntax.k:28`; `core.k:131-134,189-191,214-215`; `call.k:20-21,69-74` |
| `Assign`, `Name`, `Int` | `syntax.k:9,12,41`; strict RHS evaluation; `core.k:131-134,194`; `controls.k:9-11` |
| `For` and name target | `syntax.k:45`; `controls.k:65,69-74,85`; `tuple.k:31-34` |
| List iteration | `iter.k:8`; fixed `list.k:9-10`; exact local exposure rules `verification.k:14-19` |
| `If` | `syntax.k:49`; `controls.k:51-54`; `core.k:199-205` truthiness |
| `BinOp` | `syntax.k:15` left-to-right `seqstrict`; `operators.k:12`; `int.k:9,14-15,20` |
| `Compare`/`CmpOp("==",...)` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:26`; Boolean truthiness |
| `Return` | `syntax.k:50`; `functions.k:78-90` returns, pops the exact frame, restores cells |

All constructors in `solution.mpy` are covered. The strict/seqstrict
declarations enforce RHS, condition, iterable, return expression, and binary
operand evaluation before the listed operational rules.

### Proof-local rule decisions

The ten candidate-authored rules are:

1. Two `intVals` equations. `.IntSeq` and `iCons` are disjoint and exhaustive;
   recursion descends structurally. They only embed mathematical integers as
   `ValSeq`.
2. Two priority-40 iterator exposures. Each is exactly one `intVals` equation
   followed by the corresponding fixed list rule. They accept the same
   arbitrary `<k>` suffix as the fixed rules and touch no other cell.
3. Three `squareContribution` equations. Their guards are pairwise disjoint and
   exhaustive for the positive fixed divisors 3 and 4. They encode square,
   cube, and unchanged contributions with the correct precedence.
4. Two `sumSquaresFrom` equations. The empty case returns the accumulator; the
   cons case consumes exactly one head, increments the index, adds exactly its
   contribution, and structurally descends.
5. One priority-30 loop bridge. Its complete matched configuration is identical
   to `LOOP-SPEC.loop`, which was independently proved under
   `VERIFICATION-BASE`, where this bridge does not exist.

The bridge reads the iterator, index, accumulator, target, continuation,
environment/scopes, frame, and control-state cells. It restores the caller
environment, removes the local scope and frame, and preserves the arbitrary
builtins scope and module map. It requires and preserves an empty heap and
location 0. It neither drops an admitted continuation nor abstracts an
observable cell.

Operational sensitivity was checked independently of postcondition
non-vacuity:

- [`spec-audit-body-mutant.k`](evidence/spec-audit-body-mutant.k) changes the
  real square operation in the loop theorem to `V+V`. It dry-runs successfully,
  then its base proof exits 1 with `WarnStuckClaimState` and the expected
  residual `A + (V+V)` versus `A + V*V`
  ([dry run](evidence/05-body-sensitivity-dry-run.log),
  [proof](evidence/05-body-sensitivity-proof.log)).
- [`verification-audit-iterator-mutant.k`](evidence/verification-audit-iterator-mutant.k)
  changes the exposed head from `V` to `0`. The mutated definition builds, the
  spec dry-runs, and the loop proof exits 1 with the expected residual missing
  the symbolic head contribution
  ([build](evidence/05-iterator-mutant-kompile.log),
  [dry run](evidence/05-iterator-sensitivity-dry-run.log),
  [proof](evidence/05-iterator-sensitivity-proof.log)).

No rule encodes an unconstrained answer, bypasses an unproved program-defined
body, fabricates a used construct, or has a conflicting proof-local overlap.
No rule is labeled unsound, so there is no unsupported unsoundness allegation
requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not reuse or rely on the candidate's `spec-vacuity.k`. Starting from the
scratch spec, I created the distinct
[`spec-audit-false.k`](evidence/spec-audit-false.k), renamed the entry module
`SPEC-AUDIT-FALSE`, and changed only the result obligation:

```text
sumSquaresFrom(IS, 0, 0)
```

to

```text
sumSquaresFrom(IS, 0, 0) +Int 1
```

This is demonstrably false for the satisfying empty witness: actual/formal
result 0, mutant target 1. The mutation successfully parsed and built through:

```text
kprove spec-audit-false.k --definition verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE --dry-run
# exit 0
```

The actual proof command:

```text
kprove spec-audit-false.k --definition verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE
```

exited 1 with `WarnStuckClaimState`. Its residual explicitly compares
`sumSquaresFrom(IS,0,0)+Int 1` with `sumSquaresFrom(IS,0,0)` in the reached
post-state. This is the intended unmet implication, not a parse error, missing
import, timeout, crash, or unreachable mutation. See
[`06-false-mutation-dry-run.log`](evidence/06-false-mutation-dry-run.log) and
[`06-false-mutation-proof.log`](evidence/06-false-mutation-proof.log).

## 7. Proven versus assumed accounting

### What is proved

Conditional on the supplied K semantics and K toolchain, for every finite
`IS:IntSeq`, executing the exact regenerated `sum_squares` program from the
specified initial configuration reaches a returned value
`sumSquaresFrom(IS,0,0)`. The defining equations make that value the
left-to-right sum of `V*V` at indices divisible by 3, otherwise `V*V*V` at
indices divisible by 4, otherwise `V`. The theorem also pins the resulting
closure binding and all configuration cells shown in `SPEC.entry`.

This is partial correctness. It is not presented as a separate liveness theorem
or as coverage of non-integer elements.

### Trust ledger

| Boundary | Dependents and effect | Assessment |
|---|---|---|
| Byte-verified supplied `MPY` semantics | All concrete and symbolic execution: values, evaluation order, calls, scopes, loop control, returns | Required and acceptable trusted input in `SUPPLIED_SEMANTICS` mode. Used rules were additionally inspected. |
| K v7.1.293 compiler, Kore/Haskell prover, LLVM backend, SMT and builtin Int/Bool/Map/List hooks | Parsing, compilation, symbolic closure, and arithmetic | Standard unavoidable proof-tool trusted computing base. |
| Trusted `py2mpy.py` | Bridge from `solution.py` to the K AST | The generated bytes were independently reproduced and the resulting AST was manually/structurally pinned. Translator implementation correctness remains a trusted input by problem statement. |
| Structural correspondence between finite Python integer lists and `IntSeq`/`intVals` | Relates the formal domain to the prompt domain | Direct constructor-by-constructor informal bridge; exhaustive local equations and concrete witnesses support it. No finite-width mismatch exists because both K `Int` and Python integers here are arbitrary precision. |
| Reading `sumSquaresFrom` as the prompt's indexed sum | Natural-language adequacy | Directly exposed by three disjoint contribution equations and a structural left fold; not an opaque oracle. |
| CPython canonical and differential testing | Program-to-intent corroboration only | Finite evidence over 10,351 inputs; not used for universal K closure. |
| Supplied opaque/symbol helpers | No claim dependency | All are syntactically unreachable here, so they affect neither value, control, state, nor the theorem. |

There is no unproved candidate-authored primitive. The iterator bridges are
fixed-rule compositions, and the only whole-loop bridge is backed by a freshly
reconstructed auxiliary reachability theorem over its exact context.

### Decision

All seven required stages pass. The proof reconstructs cleanly, constrains the
actual result, embeds the exact trusted translation of the submitted program,
has a sound proof-local extension set, and rejects a fresh false result. The
formal domain and indexed fold match the natural-language contract without a
material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
