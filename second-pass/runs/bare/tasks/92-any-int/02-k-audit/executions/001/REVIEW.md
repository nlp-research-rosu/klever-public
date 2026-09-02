# Independent adversarial audit: 92-any-int

## Outcome

The candidate contains a legitimate, non-vacuous K reachability proof of the
actual submitted `solution.mpy` under its generated semantics. Clean LLVM and
Haskell builds succeeded, every one of the seven claims independently closed
with `#Top`, the proof constrains the returned Boolean, and a fresh false
postcondition was rejected at the expected result conflict.

The verdict is `CONCERNS / LEGIT`, not `PASS`, because the generated Python
program is not extensionally equal to the trusted canonical implementation on
part of Python's integer domain. It uses `type(v) == int`, whereas the canonical
uses `isinstance(v, int)`. Consequently `(True, 1, 2)`, `(False, 0, 0)`, and
`(IntSubclass(1), 1, 2)` return `False` from the generated program but `True`
from the canonical function. The K semantics and claims faithfully prove the
generated program's behavior, including that discrepancy; they do not prove
the canonical behavior on those inputs.

The audit followed the mandated `using-kit`, `validating-proof`, and
`writing-semantics` workflows. In particular, the generated-semantics workflow
required fresh concrete execution in addition to symbolic proof, and the
validation workflow required program/body sensitivity and a result-changing
false mutation.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- `/reference/reference-semantics` does not exist, as required for
  `GENERATED_SEMANTICS`.
- `/reference/prompt.py`, `/reference/canonical.py`, and
  `/reference/py2mpy.py` are regular files.
- No entry under `/candidate` is a symlink.
- All required candidate source artifacts are present as regular files:
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh`.
- There are no missing, mistyped, or symlinked required artifacts.
- Candidate `prompt.py` is byte-identical to the trusted prompt (SHA-256
  `1d19b808...51e2`), and candidate `py2mpy.py` is byte-identical to the
  trusted translator (SHA-256 `406485ea...db16`).

The extra candidate entries are derived/untrusted evidence:
`verification-kompiled/`, `__pycache__/`, `codex-output.log`,
`codex-last.txt`, `metrics.json`, `run-input.json`, and `codex-trace/`. They are
not integrity failures, but none was reused for execution. There are no
candidate helper K source files beyond the three submitted K files.

I read the provenance claims as claims only. `run-input.json` identifies the
`bare` condition with no supplied semantics; `metrics.json` claims generation
exit 0 without timeout; `codex-last.txt` and `codex-output.log` claim a prior
`#Top`. The complete structured trace parses as 165 JSONL records. None of
those assertions contributed to the verdict. The fresh reconstruction below
is the evidence.

Evidence: [01_integrity.sh](evidence/01_integrity.sh) and
[01_integrity.log](evidence/01_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `any_int(x, y, z)` to return true exactly when all
three inputs are integers and at least one input equals the sum of the other
two; otherwise it returns false. The trusted canonical implements the integer
test with `isinstance(..., int)` and then tests:

1. `x + y == z`,
2. `x + z == y`, or
3. `y + z == x`.

The generated `solution.py` implements the same three equalities, but guards
them with `type(x) == int and type(y) == int and type(z) == int`. It therefore
agrees for exact built-in integers and rejects every non-exact-`int` object
before arithmetic. That is safe for floats and other numeric types, but differs
from the canonical for `bool` and subclasses of `int`.

### Translator fidelity

Running the trusted translator on the scratch copy of `solution.py` exited 0.
The regenerated and submitted `solution.mpy` files are byte-identical, both
with SHA-256
`5240ec9e4c19980dec3bdf45eb06f619883af762dd9287e7b77331902b736856`.

### Independent differential execution

The reviewer-authored differential script imports the trusted canonical and
generated entry points independently. Its fixed scope is:

- all four documented examples;
- zero/empty-like boundaries (`(0,0,0)`, `None`, and empty strings);
- a witness for each of the three equality branches and the no-equality branch;
- negative and 100-digit integer boundaries;
- a non-integer in each argument position;
- explicit Boolean and `int`-subclass witnesses;
- all 1,331 integer triples in `[-5,5]^3`; and
- 2,000 seeded triples from a documented pool of exact integers, very large
  integers, floats, Booleans, and `int` subclasses.

There were zero mismatches in the exhaustive ordinary-integer cube. Across all
3,350 cases there were 143 mismatches, all arising when a Boolean or
`int`-subclass input was treated as an integer by the canonical and the sum
property held. Three minimal witnesses are:

| Input | Canonical | Generated |
|---|---:|---:|
| `(True, 1, 2)` | `True` | `False` |
| `(False, 0, 0)` | `True` | `False` |
| `(IntSubclass(1), 1, 2)` | `True` | `False` |

This is a material implementation-to-canonical limitation. It does not show
that the K proof substituted a program: later stages establish that the proof
faithfully executes this differing generated program.

Evidence: [02_differential.py](evidence/02_differential.py),
[02_program_fidelity.sh](evidence/02_program_fidelity.sh), and
[02_program_fidelity.log](evidence/02_program_fidelity.log).

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/92-any-int`; candidate-built definitions and caches were not
copied or read by the tools. K version `v7.1.293` was used.

Fresh builds from `verification.k` succeeded:

- LLVM definition:
  `kompile ... --backend llvm --main-module ANY-INT-VERIFICATION
  --syntax-module ANY-INT-VERIFICATION`
- Haskell definition:
  `kompile ... --backend haskell --main-module ANY-INT-VERIFICATION
  --syntax-module ANY-INT-VERIFICATION`

The trusted-translator output and the proof wrapper were independently parsed
and macro-expanded with `kast`. Their KORE was byte-identical, with SHA-256
`d397a39a...064f`.

The fresh LLVM definition was concretely compared with independent execution
of generated `solution.py` on 13 normal and boundary cases: all prompt cases,
all equality branches, zero, a 40-digit boundary, float/non-integer positions,
Boolean inputs, an `int` subclass represented as a non-exact integer, and a
`Decimal`-class input. Every `krun` exited 0, reached an empty environment, and
matched Python.

The original seven-claim `spec.k` then exited 0 with `#Top`. To ensure no
single claim was hidden by the aggregate run, I made a semantics-preserving
reviewer copy that only adds labels and ran all seven labels separately. Each
command exited 0 and printed `#Top`:

- `int-first`
- `int-second`
- `int-third`
- `int-none`
- `nonint-first`
- `nonint-second`
- `nonint-third`

The labeled copy is preserved as
[03_spec-individual.k](evidence/03_spec-individual.k). Exact commands, status
codes, concrete outputs, and all eight positive proof results are in
[03_reconstruct.log](evidence/03_reconstruct.log); the driver and concrete
oracle are [03_reconstruct.sh](evidence/03_reconstruct.sh) and
[03_k_concrete_compare.py](evidence/03_k_concrete_compare.py).

No timeout, container error, or other infrastructure uncertainty occurred.

## 4. Adequacy and real-program pinning

Every entry claim starts with the exact `RunAnyInt` call in `<k>` and an empty
`<env>`. Every destination contains a literal `boolVal(true)` or
`boolVal(false)` and requires the environment to be empty. There is no free
result variable, existential result, tautological `ensures`, omitted result
cell, or unconstrained continuation.

The claims mean:

| Claim | Plain-language precondition | Postcondition | Satisfying witness |
|---|---|---|---|
| `int-first` | Three exact integers and `x+y=z` | `True` | `(1,2,3)` |
| `int-second` | Three exact integers, first equality false, `x+z=y` | `True` | `(1,3,2)` |
| `int-third` | Three exact integers, first two equalities false, `y+z=x` | `True` | `(3,1,2)` |
| `int-none` | Three exact integers and all equalities false | `False` | `(1,1,1)` |
| `nonint-first` | First value is modeled non-exact-integer | `False` | `(1.5,1,2)` |
| `nonint-second` | First is exact integer; second is not | `False` | `(1,1.5,2)` |
| `nonint-third` | First two are exact integers; third is not | `False` | `(1,2,3.0)` |

For all seven witnesses, K, generated Python, and canonical Python agreed with
the claimed result. These particular witnesses intentionally avoid the
canonical discrepancy; Stage 2 separately preserves counterexamples to
candidate-versus-canonical equivalence.

Collectively, the first four mutually exclusive conditions partition all K
integer triples, so they establish `True` iff one of the three equalities holds.
The last three claims partition triples of modeled numbers by the position of
the first `NonIntVal`, so they establish `False` if any input is not an exact
built-in integer. Thus the branch implications collectively provide the
required equivalence on the modeled numeric domain.

Real-program pinning has three independent checks:

1. trusted retranslation is byte-identical to submitted `solution.mpy`;
2. expanded submitted-program KORE is byte-identical to expanded
   `solutionProgram`; and
3. changing the body to `return False` changes Python's `(1,2,3)` result and
   makes the expanded KORE identity check fail.

The `RunAnyInt` macro only expands to
`Invoke(solutionProgram, X, Y, Z)`; it does not summarize or skip the function
body. There are no loops, helper claims, or auxiliary circularities to align.

The formal sort `Val` also admits internal `typeVal` terms, while the seven
claims cover external numeric representations (`IntVal` and `NonIntVal`) only.
For example, a `typeVal` passed as an argument can get stuck at `typeOf`. A
Python type object is not a number under the prompt, so this is an explicit
scope boundary rather than missing semantics for a used task-domain construct.

Evidence: [04_claim_witnesses.py](evidence/04_claim_witnesses.py),
[04_adequacy.sh](evidence/04_adequacy.sh),
[04_adequacy.log](evidence/04_adequacy.log),
[05_solution-body-mutation.py](evidence/05_solution-body-mutation.py),
[05_program_sensitivity.sh](evidence/05_program_sensitivity.sh), and
[05_program_sensitivity.log](evidence/05_program_sensitivity.log).

## 5. Rule-by-rule static soundness review

### Complete local syntax and attribute inventory

`semantic.k` declares:

- `Program`: `Module(Stmts)`.
- `Stmts`: injection of one `Stmt`.
- `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`.
- `Params`: exactly three `String` names.
- `Expr`: `Name`, `Int`, `Bool`, `BinOp`, `Call`, `Compare`, three-operand
  `BoolOp`, and four-operand `BoolOp`.
- `CmpOp`: an operator `String` and comparator `Expr`.
- `IntVal`: `intVal(Int)`.
- `NonIntVal`: `floatVal(Float)`, `boolVal(Bool)`, and
  `otherNumberVal(String)`.
- `Val`: `IntVal`, `NonIntVal`, and `typeVal(String)`.
- entry `KItem`: `Invoke(Program, Val, Val, Val)`.
- internal `KItem`s: `exec`, `eval`, `finishCall`, `typeOf`, `binLeft`,
  `binRight`, `compareLeft`, `compareRight`, `andThen`, and `orThen`.

`verification.k` adds only `solutionProgram : Program` and
`RunAnyInt(Val,Val,Val) : KItem`, both marked `[macro]`.

The configuration has only `<k>` and `<env>` cells. The environment starts as
`.Map`; no heap, output, allocation, exception, or call-stack cell is declared
because the submitted pure expression needs none.

There are no local K functions, `[total]` or `[functional]` declarations,
opaque attributes, priority rules, simplification rules, concrete rules,
`owise` rules, or `anywhere` rules. `otherNumberVal` carries an uninterpreted
class tag, but no rule inspects the tag; only its `NonIntVal` sort affects the
exact-type test. It therefore cannot act as a result oracle.

Construct coverage for `solution.mpy` is complete:

| Submitted construct | Declaration and execution |
|---|---|
| `Module`, `FuncDef`, `Params` | entry rule R1 |
| `Return` | R2 and R3 |
| variable `Name` and built-in `int` name | R6 and R7 |
| `Call(Name("type"), ...)` | R8–R10 |
| `BinOp("+",...)` | R11–R13 |
| `Compare(...,CmpOp("==",...))` | R14–R17 |
| four-way `and` | R19–R21 |
| three-way `or` | R22–R24 |

`Int`/`Bool` expression literals and three-way `and` are declared and
truthfully implemented but unused by this submitted body. Missing behavior for
other operators, other calls, other statement forms, and other Boolean arities
stops visibly and is acceptable under the generated-semantics minimal-coverage
boundary.

### All 24 semantic rules

| Rule | Source lines | Effect | Soundness decision |
|---:|---:|---|---|
| R1 | 61–63 | Match a module with one three-argument function, bind its three distinct actual parameter names in an empty map, and start its body with `finishCall` | Sound for the exact program and empty entry environment. It reads/writes only `<k>` and `<env>`. |
| R2 | 64 | Evaluate the expression in `Return(E)` | Exact control flow for the only statement. |
| R3 | 65–66 | Turn a returned `Val` into the final value and clear locals | Sound for the top-level invocation, whose `finishCall` suffix is exact. |
| R4 | 69 | Convert an AST integer literal to `intVal` | Truthful; unused by this body. |
| R5 | 70 | Convert an AST Boolean literal to `boolVal` | Truthful and keeps Python Boolean distinct from exact `int`; unused by this body. |
| R6 | 71 | Interpret `Name("int")` as the built-in integer type object | Sound under the explicitly assumed ordinary, unshadowed built-in environment. |
| R7 | 72–73 | Look up a local name in `<env>` | Standard map lookup; reads but does not mutate the environment. |
| R8 | 76 | Evaluate the argument of the exact `type(...)` call before `typeOf` | Correct left-to-right binding for this unshadowed built-in call. |
| R9 | 77 | Classify `IntVal` as exact type `"int"` | Truthful for the chosen external-value embedding. |
| R10 | 78 | Classify any `NonIntVal` as `"non-int"` | A property-preserving collapse because the only observer compares it with `"int"`. |
| R11 | 81 | Start a binary operation by evaluating its left expression | Correct evaluation order. |
| R12 | 82 | Save the left value, then evaluate the right expression | Correct evaluation order and binding. |
| R13 | 83–84 | Add two `intVal`s with K `+Int` | Matches arbitrary-precision CPython exact-integer addition. Other operands/operators stop visibly. |
| R14 | 88–89 | Start a one-comparator comparison by evaluating its left side | Correct evaluation order for the used comparison form. |
| R15 | 90–91 | Save the left value, then evaluate the comparator | Correct evaluation order and binding. |
| R16 | 92–93 | Compare two `intVal`s using `==Int` | Matches exact-integer equality. |
| R17 | 94–95 | Compare two abstract type objects using `==String` | Truthful for `"int"` versus `"non-int"` and fixes the branch result. |
| R18 | 100–101 | Expand three-way `and` into ordered continuations | Sound for Boolean-valued operands; unused by this body. |
| R19 | 102–103 | Expand four-way `and` into ordered continuations | Exactly the outer submitted expression. |
| R20 | 104 | Continue an `and` after `true` | Correct short-circuit control. |
| R21 | 105 | Preserve `false` and skip the next `and` operand | Correct; repeated application skips all remaining operands. |
| R22 | 107–108 | Expand three-way `or` into ordered continuations | Exactly the inner submitted expression. |
| R23 | 109 | Continue an `or` after `false` | Correct short-circuit control. |
| R24 | 110 | Preserve `true` and skip the next `or` operand | Correct; repeated application skips all remaining operands. |

The rules are non-overlapping on actual submitted control states. R6 and R7
would overlap in a reusable language instance whose local environment contained
a key `"int"`: `eval(Name("int"))` could then produce either the built-in type
or that local value. Similarly, R8 intentionally hardwires the standard
`type` binding. The submitted function's distinct parameters are only `x`,
`y`, and `z`, and the audit imports it in a fresh module without rebinding
built-ins, so no satisfying task-domain entry state reaches either overlap.
These are narrower reuse/environment assumptions, not claims of an unsound
target rule. No false conclusion witness exists on the fixed submitted program
under its stated ordinary-builtin entry environment.

The Boolean rules model only Boolean-valued operands, whereas general Python
`and`/`or` return arbitrary operands. Every operand in the submitted program is
a comparison and therefore produces `boolVal`; this narrowing is sound on every
reachable target state. Arithmetic is reached only after all three exact-type
checks have succeeded, so no overloaded non-integer arithmetic, exception, or
side effect is silently skipped.

### Verification macros

1. `solutionProgram => Module(FuncDef(...))` is a definitional macro, not an
   operational summary. Its expanded term is byte-identical to parsed
   `solution.mpy`.
2. `RunAnyInt(X,Y,Z) => Invoke(solutionProgram,X,Y,Z)` is an entry wrapper. It
   introduces no result and skips no program computation.

Neither macro encodes the answer. There is no proof-local result function,
opaque predicate, answer lemma, circular claim, operational bridge, or
program-derived oracle. The body-sensitivity mutation is rejected at the
program-identity connection.

The complete line-numbered inventory and automated counts (24 semantic rules,
two macro rules, seven claims) are in
[05_rule_inventory.log](evidence/05_rule_inventory.log), generated by
[05_rule_inventory.sh](evidence/05_rule_inventory.sh).

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation was
trusted. I created a fresh module whose first-branch precondition remains
`X +Int Y ==Int Z` but whose result is changed from `boolVal(true)` to
`boolVal(false)`.

The witness `X=1, Y=2, Z=3` satisfies the precondition. Generated Python and
fresh concrete K execution both return true. `kprove --dry-run` exited 0, which
establishes that the mutation parsed and built. The actual mutated proof exited
1 with `WarnStuckClaimState`; its residual was the expected final
`boolVal(true)` configuration, which cannot unify with the required
`boolVal(false)`. This was not a parser error, missing import, timeout, or
unreachable mutation.

Mutation: [06_spec-vacuity-audit.k](evidence/06_spec-vacuity-audit.k).
Commands and residual:
[06_nonvacuity.sh](evidence/06_nonvacuity.sh) and
[06_nonvacuity.log](evidence/06_nonvacuity.log).

## 7. Proven versus assumed accounting

### What is machine-checked

Relative to the submitted generated semantics, the seven successful
reachability claims establish:

- for every K integer triple, execution of the exact submitted constructor
  program from an empty environment returns true iff one of the three
  pair-sum equalities holds, and otherwise returns false; and
- for every modeled numeric triple containing a `NonIntVal`, execution returns
  false, partitioned by the first non-exact-integer position.

The proof also restores the environment to `.Map`. It is a partial-correctness
result under K reachability semantics. The concrete program is finite and the
symbolic runs fully execute it, but the report does not inflate that into a
general theorem about termination of arbitrary Python.

### Trust ledger

| Boundary or assumption | Influence | Assessment and evidence |
|---|---|---|
| K toolchain and imported `INT`, `BOOL`, `STRING`, `FLOAT`, and `MAP` definitions | Parsing, `+Int`, equality, Boolean guards, maps | Acceptable low-level K trust boundary; fresh K v7.1.293 builds and runs are logged. |
| Trusted `py2mpy.py` | Python-AST to constructor syntax | Given trusted input. Candidate copy matches it, regeneration is byte-identical, and parsed output equals the proof macro. |
| Exact Python values to K values | Determines exact-integer versus non-exact branch | Informal embedding: exact built-in `int` maps to `IntVal`; every other numeric type, including `bool` and `int` subclasses, maps to `NonIntVal`. It is sufficient for this exact-type guard and is concretely exercised, but is not a machine-checked CPython connection theorem. |
| Standard unshadowed global names `type` and `int` | Controls all exact-type checks | Necessary environment assumption. Fresh module imports satisfy it. Rebinding these globals is excluded. |
| `typeOf` as an external built-in primitive | Branch-controlling result | Its contract is explicit and exhaustive over external numeric sorts: `IntVal` gives `"int"` and `NonIntVal` gives `"non-int"`. No program-defined computation is replaced. |
| `otherNumberVal(String)` class tag | Represents non-exact numeric objects | The string is opaque but unobservable; rules use only the `NonIntVal` sort, so it cannot select or fabricate the final answer independently of the exact-type test. |
| No heap, output, exception, or stack model | Observable-state scope | Acceptable for this pure expression under exact built-in integer execution. Non-exact inputs short-circuit before arithmetic. |
| Generated-to-canonical equivalence | Natural-language/canonical adequacy | Not assumed and empirically false for Booleans and `int` subclasses. This is the material concern and is excluded from what the K proof establishes. |

There are no proof-local functions, unproved lemmas, simplifications, opaque
result symbols, or empirical summaries masquerading as proof. Differential
testing supports only the finite Python/K and generated/canonical bridges it
actually exercised; it is not used as a replacement for `kprove`.

### Validation gates and decision

- Gate A, real-program soundness: **PASS**. The actual program is pinned,
  operational rules execute its body, results and environment are constrained,
  every claim closes independently, the body connection is sensitive, and the
  false result mutation is rejected.
- Gate B, intent adequacy: **LIMITED**. Exact built-in integers and ordinary
  non-integer numbers match the contract, but the trusted canonical accepts
  Boolean and `int`-subclass inputs that the generated program rejects.
- Gate C, trust and auditability: **PASS**. All boundaries and exclusions are
  named, and commands, inputs, statuses, outputs, scripts, mutations, and
  bounded logs are preserved. The final completeness check is recorded in
  [07_manifest.log](evidence/07_manifest.log).

Accordingly, the formal proof is legitimate for the real generated program,
but the canonical/intent bridge has a documented material limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
