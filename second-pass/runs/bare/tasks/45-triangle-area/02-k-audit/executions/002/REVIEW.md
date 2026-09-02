# Independent adversarial review: 45-triangle-area

The candidate's K claims reconstruct and are non-vacuous, and the claim term is mechanically identical to the submitted translated program. They nevertheless do **not** constitute a legitimate partial-correctness proof of the real Python program. The generated semantics interprets Python true division on integers as exact rational arithmetic. Real Python returns an IEEE-754 `float`, including rounding and overflow behavior. This discrepancy produces false conclusions for concrete inputs satisfying the candidate's unrestricted integer precondition. In addition, the theorem excludes ordinary float inputs admitted and handled by both Python implementations.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1`, the condition is `bare`, and the rendered semantics mode is `GENERATED_SEMANTICS`.

I read and checked:

- `/audit-input.json`, including `record_layout`, `container_paths`, all recorded hashes, and all integrity fields;
- `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete structured trace at `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-56-38-019f8941-7ef9-7792-8750-f0c2d41d7fbc.jsonl`;
- the additionally retained legacy records `legacy-metrics.json` and `legacy-run-input.json`.

All required paths are real regular files or real directories; no required record or candidate source artifact is symlinked or mistyped. The structured trace contains one regular JSONL file with 308 valid JSON records. The campaign lock JSON object equals the `audit_campaign` block in `/audit-input.json`, and its SHA-256 is the recorded `ad5df...d745`.

Independent file hashes match every applicable hash in `/audit-input.json`. The candidate's `prompt.py` and `py2mpy.py` are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`. The independently recomputed size-tagged candidate-tree digest is `6c70aca7...0d312c1`, matching both the retained workspace digest in `/generation-result.json` and the retained-workspace digest in `invocation.json`. The independently recomputed trace-tree digest is `9b038313...d3a0d`, matching `usage.json`; every individual generation-evidence hash also matches the evidence map in `/generation-result.json`.

Generated-semantics mode is internally consistent: `/reference/reference-semantics` does not exist, so no hidden or supplied semantics was used. The generation logs and reported prior `#Top` were treated only as untrusted history.

Evidence: [integrity checker](/audit-output/evidence/check_provenance.py), [command log](/audit-output/evidence/01-provenance.log) (exit 0).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt says that `triangle_area(a, h)` takes a triangle side length and height and returns the area; the documented example is `triangle_area(5, 3) == 7.5`. The trusted canonical implementation is `a * h / 2.0`.

The candidate implementation is:

```python
def triangle_area(a, h):
    return a * h / 2
```

For ordinary Python integer and float inputs, this computes the same result as the canonical implementation. The literal `2` instead of `2.0` can matter for exotic numeric classes, but no such type is specified in the prompt, and it is not the decisive defect here.

I regenerated `solution.mpy` using the trusted `/reference/py2mpy.py`. `cmp` exited 0, and both submitted and regenerated files have SHA-256 `dfeb6ac6...ab07b8a`.

The independent differential test imports the trusted canonical entry point and the submitted entry point from distinct files. It covers:

- the documented example;
- zero-side, zero-height, both-zero, unit, sign, and 32-bit magnitude boundaries;
- all 48 points in a declared integer grid;
- 200 seeded random integer pairs;
- six explicit ordinary-float cases;
- 100 seeded random float pairs.

All 364 cases matched in both value and return type or exception outcome. There is no meaningful “empty” value for this scalar numeric API; zero values are the applicable empty/boundary analogue. The implementation is branchless, so there are no branch boundaries beyond the arithmetic boundaries tested.

Evidence: [input manifest](/audit-output/evidence/differential_inputs.json), [differential script](/audit-output/evidence/differential_test.py), and [fidelity log](/audit-output/evidence/02-fidelity.log) (all commands exit 0; mismatch count 0).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/candidate`; no candidate-built definition or cache was copied or reused.

Fresh commands and results:

- `kompile semantic.k --backend llvm --main-module TINY-PYTHON --syntax-module TINY-PYTHON-SYNTAX --output-definition concrete-kompiled` — exit 0.
- `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module TINY-PYTHON-SYNTAX --output-definition proof-kompiled` — exit 0.
- `kprove spec.k --definition proof-kompiled --spec-module SPEC` — exit 0, `#Top`.
- Each of the three positive claims was copied without changing its obligation into a one-claim module and proved independently. All three isolated commands exited 0 and printed `#Top`.

Fresh LLVM execution of the actual submitted `solution.mpy` terminated normally for `(5,3)`, `(0,0)`, and `(-4,3)`, producing respectively `PyNum(15,2)`, `PyNum(0,2)`, and `PyNum(-12,2)`. A corrected independent comparison over eight normal/boundary integer cases found zero mismatches after interpreting the pair as an exact rational.

The first version of the reviewer comparison helper failed to recognize whitespace between `PyNum` and `(`, although the logged K executions themselves succeeded. I corrected only that reviewer regex and reran the helper; [the corrected log](/audit-output/evidence/03b-concrete-compare.log) exits 0 with eight agreements. The original failed helper run remains visible in [the reconstruction log](/audit-output/evidence/03-reconstruction.log), which also contains the successful clean builds and all four successful proof commands.

Thus the dynamic reconstruction gate passes **under the candidate's generated semantics**. This does not validate that semantics against Python.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. The symbolic entry claim starts with `triangleProgram`, arbitrary K integers `A` and `H` in `Args`, an empty environment, and `noResult`. It requires termination with an empty `<k>` cell, bindings `a = PyNum(A,1)` and `h = PyNum(H,1)`, and result `PyNum(A *Int H,2)`.
2. The example claim is the same reachability statement fixed at `(5,3)`, requiring `PyNum(15,2)`.
3. The zero claim is fixed at `(0,99)`, requiring `PyNum(0,2)`.

There is no hidden `requires` clause. For the symbolic theorem, the type annotations in `Args(A:Int,H:Int)` are the formal domain restriction. All RHS variables are bound on the LHS; the returned value is not free or existential. The claims rewrite `<k>` to `.K` and constrain both the environment and result. A satisfying entry state is the initial configuration with `Args(5,3)`, `.Map`, and `noResult`; fresh concrete execution exhibits it and reaches the claimed result. Substituting `A=5,H=3` gives `PyNum(15,2)`, agreeing with both Python implementations' `7.5` on that input.

### Program identity

Trusted regeneration establishes `solution.py -> solution.mpy`. A reviewer script then removes only whitespace and mechanically compares the submitted constructor term with the RHS of `triangleProgram` in `verification.k`. The token strings and normalized SHA-256 values are identical:

```text
Module(FuncDef("triangle_area",Params("a","h"),Return(BinOp("/",BinOp("*",Name("a"),Name("h")),Int(2)))))
```

The alias rule expands to that term and then the ordinary semantic rules execute every material `Module`, binding, `Name`, `Int`, multiplication, division, and `Return` operation. There are no helpers or loops. This is acceptable immutable-artifact pinning.

A body-sensitivity test changed the divisor in the **executed `triangleProgram` rule** from `Int(2)` to `Int(3)`, rebuilt successfully, and reran the original concrete `(5,3)` result obligation. `kprove` exited 1 with `WarnStuckClaimState` and residual `PyNum(15,3)`, so the proof genuinely depends on the executed body.

Evidence: [constructor comparison](/audit-output/evidence/constructor_compare.py) and [pinning/body-mutation log](/audit-output/evidence/05-pinning.log).

### Material adequacy failures

The exact-rational interpretation is not Python's true-division behavior, even within the claimed unrestricted integer domain:

- Satisfying input `A = 2**53 + 1`, `H = 1`: K terminates with exact mathematical result `9007199254740993/2`. Both trusted canonical Python and submitted Python terminate with a float whose exact `as_integer_ratio()` is `4503599627370496/1`. The K conclusion is false of the real return value.
- Satisfying input `A = 10**400`, `H = 1`: K terminates with an exact rational result. Both Python implementations raise `OverflowError`. The K claim fabricates normal termination and a result where the real generated program has an exception.

These are not merely representation preferences: they are distinct observable outcomes caused by the semantics rule for `/`.

The theorem also materially narrows the source contract to integers. Both Python implementations accept `triangle_area(0.5, 0.25)` and return `0.0625`, while `Args` is declared as `Args(Int,Int)` and the generated semantics rejects `Args(0.5,0.25)` at parse time (exit 113). The prompt is untyped and describes lengths, the example expects a fractional area, and ordinary float lengths are material behavior. Under the benchmark's decision rule, this narrowing alone maps to `FAIL / NOT_LEGIT`.

Evidence: [numeric-model witnesses](/audit-output/evidence/numeric_model_witness.py), [witness log](/audit-output/evidence/04-numeric-model-witness.log), and [float-domain log](/audit-output/evidence/07-domain-gap.log).

## 5. Rule-by-rule static soundness review

There are no local helper K files beyond `semantic.k`, `verification.k`, and `spec.k`.

### Complete local declaration inventory

`semantic.k` syntax:

1. `PyVal ::= PyNum(Int,Int)`.
2. `KResult ::= PyVal`.
3. `Exp ::= PyVal`.
4. `Exp ::= Int(Int)`.
5. `Exp ::= Name(String)`.
6. `Exp ::= BinOp(String,Exp,Exp) [strict(2,3)]`.
7. `Params ::= Params(String,String)`.
8. `Stmt ::= Return(Exp) [strict]`.
9. `Stmt ::= FuncDef(String,Params,Stmt)`.
10. `Stmt ::= Module(Stmt)`.
11. `Args ::= Args(Int,Int)`.
12. `Result ::= noResult`.
13. `Result ::= PyVal`.

`verification.k` adds exactly one production, `Stmt ::= triangleProgram`.

There are no declared local `[function]`, `[total]`, `[functional]`, opaque, priority, simplification, or concrete symbols or rules. There are no local lemmas. The only claims are the three entry claims in `spec.k`. Because all were proved in isolation, no positive claim relies on another positive claim as a circularity.

The configuration contains exactly `<k>`, `<args>`, `<env>`, and `<result>` under `<triangle>`. Every cell is read or written by the actual run. The `strict` attributes compiler-generate heating/cooling machinery for `BinOp` operands and the `Return` expression; no reviewer- or candidate-authored hidden helper rules exist. `strict(2,3)` does not enforce Python's left-to-right order as strongly as `seqstrict`, but the actual operand forms are pure, total environment lookups, so no false conclusion is enabled for this submitted body by that ordering gap.

### Complete ordinary-rule inventory and assessment

1. **Module/entry harness** (`semantic.k` lines 42–44): rewrites the one-function module to its body, takes two integers from `<args>`, and initializes the empty map with parameter bindings. It reads `<k>`, `<args>`, and `<env>`; it writes `<k>` and `<env>`; `<result>` is preserved. This is broader than Python module loading because it ignores the function name and directly invokes the body. For the mechanically fixed term, distinct parameters, empty environment, and only body in this task, it faithfully supplies the entry arguments. Its broader reuse domain is an evidence limitation, not the witnessed task failure.
2. **Integer literal** (line 46): `Int(I) => PyNum(I,1)`. This truthfully embeds a K integer into the candidate's pair representation. It reads/writes only `<k>`.
3. **Name lookup** (lines 47–48): retrieves the unique map value bound to the name. With the actual distinct `a`/`h` bindings, this matches Python local lookup and preserves every other cell.
4. **Pair multiplication** (lines 50–51): multiplies numerators and denominators with exact unbounded K integer arithmetic. It is correct as rational-pair mathematics and matches Python's arbitrary-precision integer multiplication for this body's reachable inputs.
5. **Pair division** (lines 52–54): cross-multiplies exact numerator/denominator pairs when the divisor numerator is nonzero. This is mathematically correct exact rational division, but it is **materially unsound as the semantics of the submitted Python `/` operation**. The `2**53+1` witness enables the false conclusion that the real return equals an exact half; the `10**400` witness enables the false conclusion that the real program normally returns rather than raising `OverflowError`. These witnesses are in the formal claim's own input domain.
6. **Return** (lines 56–57): with the whole `<k>` cell exactly `Return(V)` and result exactly `noResult`, consumes the computation and writes `V`. It has no wildcard continuation, so it does not discard an arbitrary suffix. It is faithful for this single-statement body.
7. **`triangleProgram` expansion** (`verification.k` lines 9–11): expands a fixed name to the exact constructor tree. It does not compute a result, skip body execution, use an oracle, or change cells. Mechanical identity and the executed-body sensitivity test justify it as a definitional program alias.

All constructs in `solution.mpy` map to the inventoried syntax and rules: `Module` and `FuncDef` use rule 1; `Params` is consumed there; `Return` uses generated strictness plus rule 6; `BinOp("*")` and `BinOp("/")` use generated strictness and rules 4–5; `Name("a")`/`Name("h")` use rule 3; and `Int(2)` uses rule 2.

The authored operational rules have distinct outer heads, and the two `BinOp` rules have disjoint operator strings; there is no local overlap or priority dependence. The division guard correctly excludes a reachable zero numerator in the divisor pair. There is no recursion, loop, allocation, I/O, heap, exception cell, or call stack. For the actual body, evaluation monotonically reduces constructor expressions to `PyVal`, and `Return` then writes the sole observable result. The missing exception model becomes material at Python float overflow, as witnessed above.

The pair syntax permits denominator zero, and the arithmetic rules are not guarded by a global well-formedness invariant. For example, `BinOp("/",PyNum(1,1),PyNum(1,0))` would reduce despite not denoting an ordinary rational divisor. No such pair is reachable from this submitted program's integer initial states, so I do not label this a task-domain unsoundness without the required intended-domain witness; it is a narrower global-reuse/coverage gap. The two Python true-division witnesses above, by contrast, are reachable and decisive.

The imported K `INT`, `MAP`, and strictness machinery are ordinary low-level trusted primitives. No rule directly encodes the task's answer, introduces a fresh result, uses an unconstrained oracle, or bypasses the fixed constructor body. The illegitimate conclusion arises from modeling the property-bearing Python division operation with the wrong numeric semantics.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact; none was submitted. I created a fresh `SPEC-VACUITY` claim for the satisfying input `(5,3)` and changed only the result obligation from the true `PyNum(15,2)` to the false `PyNum(16,2)`.

- `kprove ... --dry-run` exited 0, demonstrating successful parsing and KORE construction.
- The actual `kprove` exited 1 with `WarnStuckClaimState`.
- The residual final configuration contains `.K`, the expected bindings, and actual result `PyNum(15,2)`, directly exposing the unmet result obligation.

This is meaningful non-vacuity evidence: the original K theorem constrains the result under its own semantics. It does not cure the semantics-to-Python failure.

Evidence: [fresh mutation](/audit-output/evidence/spec-vacuity.k), [runner](/audit-output/evidence/run_nonvacuity.sh), and [log](/audit-output/evidence/06-nonvacuity.log).

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the candidate-defined `TINY-PYTHON` transition system, for every unbounded K integer pair `A,H`, starting the fixed submitted constructor term with an empty map and `noResult` reaches `.K`, binds `a` and `h` to denominator-one pairs, and stores the exact pair `PyNum(A *Int H,2)`. The two ground claims establish instances already covered by that symbolic statement. The proof is result-constraining and non-vacuous within that model.

### Trust and assumption ledger

- **K toolchain and reachability engine:** K v7.1.293, Haskell `kprove`, and LLVM `krun` are trusted to implement the compiled rules. All builds were fresh.
- **K built-ins:** unbounded `Int`, `*Int`, `=/=Int`, `Map`, map lookup/update, cells, and compiler-generated strictness are trusted low-level operations. They do not encode the target answer.
- **Translator bridge:** `/reference/py2mpy.py` is a trusted benchmark input. Byte-identical regeneration and token-level comparison connect `solution.py`, `solution.mpy`, and `triangleProgram`.
- **Entry harness bridge:** direct module-to-body invocation is an informal generated-semantics design choice. It is adequately pinned for this body and these bindings, but it is not a general Python module/call semantics.
- **Python numeric bridge:** the proof assumes exact rational meaning for `/` on integer operands. This boundary is illegitimate because it is property-bearing and demonstrably false for satisfying inputs; no bridge-free connection theorem exists, and concrete opposite outcomes were observed.
- **Input-domain bridge:** `Args(Int,Int)` is assumed to cover the source contract. It does not cover ordinary float lengths accepted by both real Python implementations; this is a material narrowing.
- **Differential evidence:** 364 finite canonical-versus-candidate Python comparisons and eight finite K-versus-Python ordinary integer comparisons support implementation fidelity only on those cases. They are not universal proofs and cannot replace the failed numeric-semantics connection.

Gate A (real-program soundness) fails because the exact-rational division rule enables false result and control/exception conclusions. Gate B (intent adequacy) also fails because the formal domain excludes material ordinary-float inputs. Gate C evidence is reproducible, but finite testing cannot repair either failure.

The candidate therefore has a successful and discriminating proof of a small exact-rational transition system, not a legitimate partial-correctness proof of the real generated Python program over the HumanEval source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
