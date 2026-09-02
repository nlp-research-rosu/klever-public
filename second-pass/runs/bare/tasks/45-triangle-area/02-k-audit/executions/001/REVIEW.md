# Independent adversarial audit: 45-triangle-area

The candidate's K claims reconstruct successfully and are non-vacuous, but the
proof is not a legitimate proof of the real generated Python program. The
symbolic entry claim admits every K integer, while the generated division
semantics always returns an exact rational pair. Real Python `/` returns a
binary float (or raises `OverflowError`). A positive, satisfying input,
`a = 9007199254740993, h = 1`, therefore gives a concrete false-conclusion
witness: K concludes the exact value `9007199254740993/2`, whereas both the
trusted canonical and submitted Python functions return the rounded float
`4503599627370496.0`.

All execution below used reviewer copies in
`/tmp/audit-work/45-triangle-area`. Candidate-provided compiled definitions and
caches were never used.

## 1. Input and provenance integrity

The `GENERATED_SEMANTICS` mount boundary is valid:
`/reference/reference-semantics` does not exist. This is not an infrastructure
breach. The check, artifact types, hashes, comparison commands, and exit status
are in [stage1_integrity.log](evidence/stage1_integrity.log).

Required/input artifacts were assessed as follows:

| Artifact | Status |
|---|---|
| `/candidate/run-input.json` | Regular file; identifies problem `45-triangle-area`, condition `bare`, and no supplied semantics. |
| `/candidate/metrics.json` | Regular file; untrusted claim of exit 0, no timeout, and 640-second generation. |
| `/candidate/codex-last.txt` | Regular file; untrusted claim that all claims produced `#Top`. |
| `/candidate/codex-output.log` | Regular file; fully scanned as untrusted provenance. It contains failed intermediate attempts and a final `KPROVE_PASSED` claim. |
| structured trace | One regular JSONL file; all 308 records parsed. |
| `/candidate/prompt.py` | Regular and byte-identical to `/reference/prompt.py` (`cmp` exit 0). |
| `/candidate/py2mpy.py` | Regular and byte-identical to `/reference/py2mpy.py` (`cmp` exit 0). |
| `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, `prove.sh` | All present as regular files. |

No symlink exists anywhere under `/candidate`. The candidate has no extra K
source/helper file. Extra non-source artifacts are `toy-kompiled/`,
`verification-kompiled/`, `__pycache__/`, and the generation/provenance files.
The two compiled trees and bytecode were excluded from reconstruction. There is
no candidate `PROOF.md` or `spec-vacuity.k`; neither was a required generation
deliverable, and no claim was inferred from their absence.

The reviewer parser read the full structured trace and full 607,528-byte
`codex-output.log`. It found 73 trace tool calls, seven textual `#Top` markers
in the output log, sixteen error markers, and one stuck-claim marker. Those
counts document the untrusted history; they are not proof evidence. See
[inspect_provenance.py](evidence/inspect_provenance.py) and
[stage1_provenance_trace.log](evidence/stage1_provenance_trace.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks `triangle_area(a, h)` to return the area of a triangle
from side/base `a` and height `h`, with the example `triangle_area(5, 3) == 7.5`.
The trusted canonical implementation is:

```python
return a * h / 2.0
```

The submitted implementation is:

```python
return a * h / 2
```

For ordinary Python integer and float inputs these calculate the same Python
float. The prompt states no type or magnitude bound. Geometry suggests
nonnegative inputs, but the code itself also accepts negative numeric values.

The trusted translator was run independently:

```text
python3 /reference/py2mpy.py /tmp/audit-work/45-triangle-area/solution.py \
  > /tmp/audit-work/45-triangle-area/regenerated_solution.mpy
```

It exited 0, and `cmp` against the submitted `solution.mpy` exited 0. Both files
have SHA-256
`dfeb6ac63836b0ff5014334a279dd1e5f625a17de4a5aba7e45e034ccab07b8a`.
Exact commands and statuses are in
[stage2_translate_identity.log](evidence/stage2_translate_identity.log).

The independent differential test imported the trusted and submitted entry
points separately. It covered:

- the documented example;
- zero/empty-magnitude cases, negative values, unit and half-area boundaries;
- values around `2**53`, large finite values, and integer-to-float overflow;
- every pair in `[-25,25] x [-25,25]`;
- 500 seeded large-integer pairs and 500 seeded float pairs.

There is no source branch, so there is no branch boundary beyond arithmetic
representation/exception boundaries. All 3,621 cases agreed, including matching
exception behavior; mismatch count was zero. This supports implementation
fidelity but is finite evidence, not a universal theorem. See
[differential_test.py](evidence/differential_test.py) and
[stage2_differential.log](evidence/stage2_differential.log).

## 3. Clean proof reconstruction

The reviewer copied only source artifacts and trusted inputs into scratch. K
v7.1.293 and Python 3.10.12 were used; versions are recorded in
[tool_versions.log](evidence/tool_versions.log).

Fresh concrete semantics build:

```text
kompile semantic.k --backend llvm --main-module TINY-PYTHON \
  --syntax-module TINY-PYTHON-SYNTAX \
  --output-definition fresh-concrete-kompiled
```

Result: exit 0. See
[stage3_build_concrete.log](evidence/stage3_build_concrete.log).

Fresh proof-definition build:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module TINY-PYTHON-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Result: exit 0. See [stage3_build_proof.log](evidence/stage3_build_proof.log).

Because the candidate claims are unlabeled, the reviewer copied each unchanged
claim into its own scratch spec module and ran it independently:

| Claim | Exact proof command | Result |
|---|---|---|
| symbolic integers | `kprove spec-symbolic.k --definition fresh-verification-kompiled --spec-module SPEC-SYMBOLIC` | exit 0, `#Top` |
| documented example | `kprove spec-example.k --definition fresh-verification-kompiled --spec-module SPEC-EXAMPLE` | exit 0, `#Top` |
| zero case | `kprove spec-zero.k --definition fresh-verification-kompiled --spec-module SPEC-ZERO` | exit 0, `#Top` |
| original combined spec | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC` | exit 0, `#Top` |

The bounded outputs are
[stage3_prove_symbolic.log](evidence/stage3_prove_symbolic.log),
[stage3_prove_example.log](evidence/stage3_prove_example.log),
[stage3_prove_zero.log](evidence/stage3_prove_zero.log), and
[stage3_prove_combined.log](evidence/stage3_prove_combined.log).

Fresh concrete `krun` executions of the actual submitted `solution.mpy` produced
`PyNum(15,2)` for `(5,3)` and `PyNum(0,2)` for `(0,99)`, with empty final
`<k>` cells. See
[stage3_krun_example.log](evidence/stage3_krun_example.log) and
[stage3_krun_zero.log](evidence/stage3_krun_zero.log).

Generated-semantics comparison against actual Python passed on the documented,
zero, negative, and last-exact-half cases but failed on three of seven
representation/exception boundary cases:

- `(9007199254740993,1)`: exact K half versus rounded Python float;
- `(10**308,1)`: exact K integer-valued rational versus the nearby representable
  Python float;
- `(10**309,1)`: normal K result versus Python `OverflowError`.

The tester deliberately exits 1 when it finds these semantic mismatches. This
is a candidate-semantics failure, not a build, parser, or infrastructure error.
See [semantic_differential.py](evidence/semantic_differential.py) and
[stage3_semantic_differential.log](evidence/stage3_semantic_differential.log).

## 4. Adequacy and real-program pinning

The three entry claims mean:

1. For every unbounded K integer pair `A,H`, starting with
   `triangleProgram`, `Args(A,H)`, an empty environment, and `noResult`,
   execution must consume `<k>`, bind `a` and `h`, and set the result exactly
   to `PyNum(A*H,2)`.
2. The same exact transition at `A=5,H=3`, with result `PyNum(15,2)`.
3. The same exact transition at `A=0,H=99`, with result `PyNum(0,2)`.

There are no `requires` clauses. Thus every K integer pair satisfies the
symbolic precondition; `(5,3)`, `(0,99)`, `(9007199254740993,1)`, and
`(10**309,1)` are explicit satisfying states. The two ground claims have their
own exact satisfying initial states.

The postconditions are not free variables, tautologies, or one-way predicates.
They require `.K`, exact final bindings, and exact `PyNum` constructor results.
The proof is therefore strongly result-constraining.

`verification.k`'s `triangleProgram` rule expands to the exact normalized
constructor tree in submitted `solution.mpy`. The independent identity check is
in [stage4_pinning.log](evidence/stage4_pinning.log). A reviewer spec using the
literal constructor tree directly also closed with `#Top`; see
[stage4_prove_direct.log](evidence/stage4_prove_direct.log). Thus this is not a
substituted-program failure. There are no helpers or loops to match.

Concrete substitution gives:

| Input | Claimed exact value | Canonical Python | Submitted Python | Agreement |
|---|---:|---:|---:|---|
| `(5,3)` | `15/2` | `7.5` | `7.5` | yes |
| `(0,99)` | `0` | `0.0` | `0.0` | yes |
| `(9007199254740993,1)` | `9007199254740993/2` | `4503599627370496.0` | same | no |
| `(10**309,1)` | a normal exact half | `OverflowError` | `OverflowError` | no |

Full states/outcomes are in
[stage4_entry_witness.log](evidence/stage4_entry_witness.log).

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[stage5_rule_inventory.md](evidence/stage5_rule_inventory.md); source discovery
and searches for special attributes are in
[stage5_source_inventory.log](evidence/stage5_source_inventory.log).

### Syntax, configuration, and special declarations

Local syntax consists of:

- `PyNum(Int,Int)` and its `KResult` injection;
- expression alternatives `PyVal`, `Int`, `Name`, and strict `BinOp`;
- two-name `Params`;
- strict `Return`, two-parameter `FuncDef`, and one-statement `Module`;
- integer-pair `Args`;
- `noResult` or `PyVal` result;
- proof-local `triangleProgram`.

The configuration has `<k>`, `<args>`, `<env>`, and `<result>` cells. There is
no heap, call stack, exception cell, float value, object/type state, output, or
allocation state.

There are no local functions, total/functional declarations, simplification or
concrete rules, `owise` rules, macros, aliases, priorities, opaque symbols,
hooks, or proof-local lemmas. `BinOp [strict(2,3)]` and `Return [strict]`
generate standard heating/cooling behavior. `strict` does not enforce Python's
left-to-right order, but all submitted operands are pure name/literal
expressions, so this gap has no false witness for this program.

### Complete local rule judgments

| Rule | Behavior | Judgment |
|---|---|---|
| R1 `Module(FuncDef(...))` | Entry harness replaces the module/function wrapper with the exact body and binds the two integer arguments. | Acceptable for this exact pure, two-parameter submitted term. It ignores the function name and omits a real Python call stack, so it is broader than needed, but no false conclusion witness exists on the submitted constructor tree. |
| R2 `Int(I)` | Produces `PyNum(I,1)`. | Sound for the used literal `2`. |
| R3 `Name(X)` | Reads `X` from `<env>`. | Sound for `a` and `h`, which R1 always binds. Missing-name exception behavior is unused. |
| R4 pair multiplication | Multiplies numerators and denominators componentwise. | Sound rational arithmetic; on the reached denominator-1 inputs its numerator matches Python arbitrary-precision integer multiplication. |
| R5 pair division | Returns `(AN*BD)/(AD*BN)` when `BN != 0`. | Mathematically sound rational arithmetic but materially unsound as the semantics of the submitted Python `/`. It fabricates an exact normal result where Python rounds or raises. |
| R6 `Return(V)` | Consumes `<k>` and writes `V` to `<result>`. | Sound for the top-level entry harness, which has no continuation or call stack. |
| R7 `triangleProgram` | Expands to the exact submitted constructor tree. | Sound syntactic abbreviation; it carries no task answer and does not bypass R1-R6. |
| G1/G2 strictness rules | Evaluate binary operands and the return expression to `KResult`. | Adequate for the pure submitted body. |

Rule fronts/operators are disjoint; there is no local priority or overlap
conflict. The division guard is true for the submitted literal divisor `2`.
`PyNum` also admits malformed/noncanonical pairs, but those are not reachable
from an entry precondition and are not being labeled unsound on the intended
program path.

Construct coverage is complete for the submitted MPY term:
`Module`/`FuncDef`/`Params` use R1; `Return` uses G2/R6; both `BinOp` nodes use
G1 plus R4/R5; `Name` uses R3; and `Int(2)` uses R2.

### Required false-conclusion witness for R5

Take the positive, geometry-compatible entry input:

```text
A = 9007199254740993
H = 1
```

It satisfies C1 with no side condition. R1-R4 and R5 conclude:

```text
<result> PyNum(9007199254740993, 2) </result>
```

The candidate explicitly defines this as an exact numerator/denominator value,
namely `4503599627370496.5`. Actual Python terminates normally and returns
`4503599627370496.0` because of binary-float rounding. The direct K and Python
commands, outputs, and exit statuses are in
[stage5_rounding_witness.log](evidence/stage5_rounding_witness.log).

A second witness, `A=10**309,H=1`, makes K return normally while Python raises
`OverflowError`; see
[stage5_overflow_witness.log](evidence/stage5_overflow_witness.log). The first
witness alone is sufficient because the real program terminates normally with
an observable result different from the proved exact value.

This rule is the sole rule labeled unsound. The narrower issues in R1,
strictness order, missing-name behavior, and malformed `PyNum` values are
reported as scope gaps rather than unsound rules because no false conclusion
witness exists for them on the submitted program's entry path.

## 6. Fresh non-vacuity test

The reviewer-authored mutation changes only the documented example's required
result from the true `PyNum(15,2)` to the false `PyNum(16,2)`. Input `(5,3)`
satisfies the mutated precondition. The preserved mutation is
[spec-vacuity.k](evidence/spec-vacuity.k).

The scratch and preserved copies are byte-identical (`cmp` exit 0):
[stage6_mutation_identity.log](evidence/stage6_mutation_identity.log).

The mutation parsed and built successfully:

```text
kprove spec-vacuity.k --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Result: exit 0; see
[stage6_mutation_build.log](evidence/stage6_mutation_build.log).

The live mutation proof command exited 1 with `WarnStuckClaimState`. Its
reachable residual has empty `<k>`, the expected environment, and actual
`<result> PyNum(15,2) </result>`, which cannot unify with the mutated
destination `PyNum(16,2)`. This is the expected unmet result obligation, not a
parser error, missing import, timeout, or unrelated crash. See
[stage6_mutation_proof.log](evidence/stage6_mutation_proof.log).

The proof therefore passes the non-vacuity/result-sensitivity test. That does
not repair the real-program semantics failure.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the candidate's generated K theory, the exact submitted constructor tree
always reduces for any K integers `A,H` to empty `<k>`, exact parameter
bindings, and `PyNum(A*H,2)`. The two ground instances also reduce to their
specified pairs. This closure is machine checked and non-vacuous.

It does not establish that the real Python function returns the mathematical
rational `A*H/2` for every Python integer. That connection depends on R5, which
is false on satisfying inputs.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 parser, LLVM/Haskell backends, reachability engine | All builds, runs, and `#Top` results | Ordinary low-level trusted tool boundary; versions and fresh commands are recorded. |
| Imported `INT`, `STRING`, and `MAP` syntax/operations, including `*Int` and map lookup/update | R1-R5 and all claims | Acceptable K built-in primitive boundary. No contradictory behavior was observed. |
| Trusted `/reference/py2mpy.py` | Python-source to MPY syntax bridge | Acceptable trusted input; regenerated output is byte-identical. This is syntactic evidence only. |
| `triangleProgram` abbreviation | Every entry claim | Acceptable: exact tree identity and a direct-tree proof were independently checked. |
| R1's module-as-entry invocation harness | Every entry claim | Informal execution bridge. Acceptable for this exact pure two-argument body, though it is not a general Python call semantics. |
| `PyNum` exact-rational interpretation and R5 as Python `/` | Symbolic result and both ground results | Illegitimate on the full formal domain. It affects the final result and exception behavior, has no connection theorem, and is refuted by positive ground witnesses. |
| Canonical/source agreement | Natural-language implementation bridge | Empirically supported on 3,621 cases, including boundaries; finite only. |
| Integer-only `Args` | The entire theorem domain | Adequacy limitation: the prompt has no integer-only restriction and ordinary nonintegral lengths are unproved. |

There are no fresh opaque result symbols, proof-local mathematical lemmas,
unproved total functions, or simplification equations. Candidate prose, logs,
compiled definitions, and traces establish nothing beyond their status as
untrusted claims.

Gate A (real-program soundness) fails because R5 makes a false returned-value
conclusion provable for a satisfying, normally terminating input. Gate B
(intent adequacy) is additionally limited by integer-only inputs and absence of
real Python float/exception behavior. Gate C evidence is independently
reproducible, but successful evidence accounting cannot cure Gate A.

The candidate therefore has a real, discriminating proof of its own exact
rational toy semantics, not a legitimate partial-correctness proof of the real
generated Python program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
