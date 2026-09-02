# Independent adversarial review: 157-right-angle-triangle

## Bottom line

The candidate contains a real, freshly reconstructible K reachability proof of
the exact submitted `solution.mpy` term over K integers. The proof is
result-constraining, its two proof-local functions are transparent definitions
rather than execution-bypassing oracles, the generated semantics faithfully
executes every construct used by this program, and independent body and
postcondition mutations are rejected.

I assign `CONCERNS / LEGIT`, not `PASS`, because the trusted prompt has no type
annotation while the formal theorem and generated input grammar cover only
`Int`. The integer-side-length interpretation is supported by every prompt
example and is the material benchmark domain exercised here, but the proof does
not cover a broader interpretation involving positive non-integral Python
numbers. In addition, correspondence of this small generated semantics to
Python is audited structurally and by finite differential/concrete evidence; it
is not itself established by a separate machine-checked CPython connection
theorem. Neither limitation enables a false integer-domain theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. I read the launcher-owned input,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, the invocation and metrics records, `usage.json`,
both legacy records, `prompt.txt`, `codex-last.txt`, `codex-output.log`, and
the structured trace. The one trace file has 107 valid JSONL records. I treated
all generation prose and traces only as untrusted historical claims.

The required records and mounts are real, readable files/directories and not
symlinks. The campaign-lock JSON object exactly equals the campaign object in
`audit-input`; its mounted-file SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. Every audit-input per-file hash checked by the
reviewer matches, as does every invocation-declared evidence-file hash,
including the trace JSONL hash.

The independently computed mounted candidate content-tree digest is
`cb3c8a89d5423cb96504d8b8e31c3741fbb0d3c8041c783c448c44c6f6e5ef1f`.
It matches both `invocation.json`'s retained-workspace digest and
`generation-result.json`'s workspace digest. The independently computed trace
content-tree digest is
`59f548322726c524706db1f4fe5d4f2a17cd82ce32366e6470284cd5e9946f2b`,
matching `usage.json`'s source-trace digest. The launcher also records
audit-specific aggregate tree hashes under different fields; I did not equate
those with the pipeline content-tree encoding. Constituent files, the retained
workspace, and the structured trace all pass the independently reproducible
content checks.

The candidate `prompt.py` is byte-identical to `/reference/prompt.py`, and
candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`. No
`/reference/reference-semantics` exists, which is exactly the required
generated-semantics boundary; I did not search for or infer a hidden reference
semantics. No required candidate proof artifact is missing.

Evidence:

- [complete integrity output](evidence/01b-integrity-complete.log)
- [scratch-copy command](evidence/02-scratch-copy.log)

Stage 1 result: PASS. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says that the three arguments are side lengths and asks for
`True` exactly when they form a right-angled triangle. For positive side
lengths, this is equivalent to one of the three Pythagorean equations holding,
with each possible side treated as the hypotenuse. The two documented examples
are `(3,4,5) -> True` and `(1,2,3) -> False`.

The trusted canonical function returns the disjunction of the three squared
equalities. The generated `solution.py` additionally requires every side to be
positive before evaluating that disjunction. This addition is appropriate for
geometric side lengths and does not change any positive-length result. It does
cause a visible canonical divergence on non-length values such as `(0,0,0)`
and `(-3,4,5)`: canonical returns `True` from squares alone, while the
generated program returns `False`. I do not treat these witnesses as
in-domain counterexamples because zero and negative values are not triangle
side lengths. They remain recorded rather than silently omitted.

Using the trusted translator directly on the scratch copy regenerated
`solution.mpy` with byte identity. Both files have SHA-256
`d5ca368d0cd54dd51a7a7b8ea8a62b4ce92b31978b8484435101265b40c7301a`.

The independent differential test imports the trusted canonical and candidate
modules separately. Its scope was:

- both documented examples;
- all three Pythagorean branches and side orderings, near/non-right cases, zero
  boundaries, sign boundaries, a very large integer, and representative floats;
- all 15,625 triples in `[1,25]^3`;
- 5,000 seeded positive triples and 5,000 seeded signed triples;
- an arity-zero call to both functions (both raise `TypeError`; an “empty”
  scalar triple otherwise does not exist).

There were zero mismatches among 20,641 documented and positive-length cases.
The full 25,651-case run records six intentional zero/sign-boundary
mismatches, all explained by the positivity check. This is finite evidence,
not a universal proof.

Evidence:

- [trusted regeneration and byte comparison](evidence/03-regenerate-translation.log)
- [differential test source](evidence/differential_test.py)
- [differential results](evidence/04-differential.log)

Stage 2 result: PASS for positive side lengths, with the nonpositive canonical
scope difference and untyped/non-integral scope concern carried to Stages 4
and 7.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`; no
candidate-provided kompiled definition or cache was copied. The observed live
toolchain is K 7.1.293 and Python 3.10.12.

Fresh commands and results:

1. `kompile semantic.k --backend haskell --main-module MPY
   --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` exited 0.
2. Fresh `krun` executions covered `(3,4,5)`, `(1,2,3)`, the other two
   Pythagorean branch placements, each zero/sign guard boundary, and a
   21-digit-scaled 3-4-5 triple. Every run exited 0.
3. An automated comparison found zero disagreements between those K results
   and independent `solution.py` execution. It also records where canonical
   differs on nonpositive inputs.
4. `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module MPY-SYNTAX --output-definition verification-kompiled`
   exited 0.
5. `kprove spec.k --definition verification-kompiled --spec-module SPEC`
   exited 0 and printed `#Top`.
6. I copied each of the four claims into its own reviewer spec module and ran
   it independently. The universal claim and all three example claims each
   exited 0 and printed `#Top`.

The first reviewer-generated concrete wrappers contained literal `\n` text and
were rejected by the parser; those logs are preserved as `09-krun-*.log`.
After correcting only the reviewer generator, all `09b`/`09c` runs succeeded.
Likewise, `10-concrete-python-comparison.log` records an initially
over-escaped reviewer regex; `10b`/`10c` are the corrected successful
comparisons. These were test-harness errors before semantic execution, not
candidate failures or evidence used as success.

Evidence:

- [tool versions](evidence/06-toolchain.log)
- [fresh concrete build](evidence/07-kompile-concrete.log)
- [final K/Python concrete comparison](evidence/10c-concrete-python-comparison.log)
- [fresh proof build](evidence/11-kompile-proof.log)
- [all claims together](evidence/12-kprove-all.log)
- [universal claim alone](evidence/13a-kprove-universal.log)
- [example claims alone](evidence/13b-kprove-example-345.log),
  [13c](evidence/13c-kprove-example-123.log), and
  [13d](evidence/13d-kprove-example-534.log)

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language claims

The universal claim has no `requires` clause. Its initial configuration is an
empty environment and `noResult`, with arbitrary K integers `A`, `B`, and `C`.
It starts:

`run(solutionProgram, "right_angle_triangle", Args(A,B,C))`.

Its postcondition requires an empty computation, an empty final local
environment, and exactly:

`result(rightTriangle(A,B,C))`.

The function `rightTriangle` is not free or opaque: its only equation expands
to positivity of all three integers conjoined with the three-way Pythagorean
disjunction. Thus the result is fully constrained.

The other claims have the same initial/final cell requirements and fix the
arguments/results to `(3,4,5)/true`, `(1,2,3)/false`, and
`(5,3,4)/true`.

Every precondition is satisfiable. For example, the universal claim is
satisfied by the concrete initial state with `A=3,B=4,C=5`, `.Map`, and
`noResult`; each fixed claim's own displayed initial state is a witness.
Substitution gives `true`, `false`, and `true`, respectively, agreeing with
both Python implementations. Substituting `(0,0,0)` gives formal/candidate
`false` and canonical `true`, which is the already-disclosed invalid-length
scope difference.

### Program identity

`solutionProgram` expands to the complete `Module(FuncDef(...))` term rather
than to a result summary. A reviewer script isolated that rule RHS and compared
its whitespace-normalized constructor text with the trusted-regenerated
`solution.mpy`. Both normalized texts have SHA-256
`fe6d4c7a4441944a1214578d3ea35b0ab66b8df6b532a94d9f0d442c5a5b1e88`
and compare equal.

The generated `run` semantics then structurally selects the one function whose
name is the requested name, binds all three arguments, and evaluates its real
`Return` expression. No rule rewrites the call directly to `rightTriangle`.
Every material arithmetic, comparison, and Boolean operation in the body is
executed.

For body sensitivity, I changed the first positivity comparison in the
*executed `solutionProgram` term* from `a > 0` to `a == 0`, rebuilt a separate
proof definition successfully, and reran the `(3,4,5) -> true` claim. It exited
1 with a stuck final configuration containing `result(false)`. The theorem is
therefore sensitive to the body it claims to execute.

Evidence:

- [mechanical constructor comparison](evidence/05-program-pinning.log)
- [mutated executed program term](evidence/body-mutation-verification.k)
- [mutation build](evidence/14a-body-mutation-kompile.log)
- [expected body-mutation proof failure](evidence/14b-body-mutation-kprove.log)

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

There are exactly three candidate K files and no helper K files. The exhaustive
declaration/rule inventory is also preserved in
[rule-inventory.md](evidence/rule-inventory.md), with a mechanically generated
source index in [16-static-source-index.log](evidence/16-static-source-index.log).

### Syntax, configuration, and attributes

`MPY-SYNTAX` declares `Expr` (`Int`, `Name`, `BinOp`, `Compare`, `BoolOp`),
`CmpOp`, `Exprs`, `Params`, `Strings`, `Stmt` (`FuncDef`, `Return`), `Stmts`,
`Program` (`Module`), `Ints`, `Arguments` (`Args`), and `Input` (`Program` or
`run`). `MPY` declares `Value` (`iVal`, `bVal`), `Result`
(`noResult`, `result`), and the nine control items `bind`, `eval`,
`binRight`, `binApply`, `cmpRight`, `cmpApply`, `boolTail`, `boolMerge`,
and `publish`.

The configuration has only `<k>`, `<env>`, and `<result>` under `<mpy>`.
Those are exactly the control/local-binding/observable-result components this
pure function needs. There is no heap, I/O, exception, allocation, or other
source effect to model.

The only local attributes are `[function,total]` on `rightTriangle` and
`[function]` on the constant `solutionProgram`. There are no local priority,
`owise`, simplification, functional, anywhere, macro, or opaque declarations.

### All 19 operational rules

| # | Rule role | Static decision |
|---:|---|---|
| 1 | Select `run(Module(FuncDef(F,...)),F,Args(...))` | Sound for the exact submitted single-definition/single-return module. The repeated `F` pins the binding; body and arguments remain explicit. |
| 2 | Finish `bind(.Strings,.Ints)` | Sound exact-length base case. |
| 3 | Bind one parameter/argument and recur | Sound left-to-right pairing and map update; actual Python syntax has distinct parameters. |
| 4 | Evaluate `Int(I)` | Sound literal introduction. |
| 5 | Evaluate `Name(X)` by map lookup | Sound for the three bound integer parameters. |
| 6 | Begin `BinOp` by evaluating the left operand | Sound Python evaluation order. |
| 7 | After the left integer, evaluate the right operand | Sound sequencing and preservation of the left value. |
| 8 | Apply `"+"` as `+Int` | Sound for Python arbitrary-precision integer addition. |
| 9 | Apply `"*"` as `*Int` | Sound for Python arbitrary-precision integer multiplication. |
| 10 | Begin the one-link `Compare` by evaluating its left expression | Sound for every comparison in this term. |
| 11 | Preserve the left integer while evaluating the comparator | Sound sequencing. |
| 12 | Apply `">"` as `>Int` | Sound for integer comparison. |
| 13 | Apply `"=="` as `==Int` | Sound for integer equality. |
| 14 | Begin a nonempty `BoolOp` with its first operand | Sound on the actual nonempty translated lists. |
| 15 | Finish a Boolean fold at `.Exprs` | Sound accumulator base case. |
| 16 | Evaluate the next Boolean operand | Sound for this pure, total expression body. |
| 17 | Merge `"and"` with `andBool` | Sound Boolean conjunction. |
| 18 | Merge `"or"` with `orBool` | Sound Boolean disjunction. |
| 19 | Publish the Boolean, clear the local environment, and finish | Sound function-frame abstraction for a pure local computation; result is observable and preserved. |

Rules 2/3, 4/5/6/10/14, 8/9, 12/13, 15/16, and 17/18 are
constructor- or literal-disjoint. There are no problematic overlaps or
priority interactions. All actual operator strings have a matching rule.
Parameter and argument list lengths are both exactly three, so neither binding
stuck case is reachable in the submitted call.

The semantics evaluates all Boolean operands instead of implementing Python's
short-circuit skip. This would be incomplete for a hypothetical accepted term
whose skipped operand had an error or state effect. It is not an unsound rule
for this program: all operands are pure, total integer expressions; there are
no calls, mutations, exceptions, or I/O; and full evaluation produces the same
Boolean. An unsupported hypothetical operator gets visibly stuck rather than
fabricating a value. Per the generated-semantics boundary, missing coverage for
unused constructs is not a defect. I therefore record this as a reusability
limit, not a false-conclusion witness or local-rule unsoundness.

### Proof-local equations

`rightTriangle` is a definitional mathematical summary. Its one unguarded,
nonrecursive equation covers every `Int` triple, has no overlap, and terminates
in built-in integer/Boolean operations. It does not replace program execution.

`solutionProgram` is a definitional constant whose one equation exposes the
exact program constructor term. It introduces no result and is covered at its
only use. The body-sensitivity test independently confirms that it is the term
being executed.

There are no derived lemmas, auxiliary claims, operational proof bridges,
unconstrained fresh values, or task-answer rules in `verification.k`. No local
rule is labeled unsound, so there is no omitted false-conclusion witness for an
unsoundness allegation.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I ignored the absence/presence of any candidate vacuity artifact and created a
new `SPEC-VACUITY`. It runs the real `solutionProgram` on the satisfiable input
`(3,4,5)` but deliberately demands `result(false)`.

`kprove ... --dry-run` exited 0, showing the mutation parses and builds against
the fresh proof definition. The actual proof exited 1 with
`WarnStuckClaimState`; its final residual has `.K`, `.Map`, and
`result(true)`, which is exactly the unmet result obligation. This is neither a
parser failure nor an unreachable mutation.

Evidence:

- [false-result mutation](evidence/spec-vacuity.k)
- [successful mutation dry run](evidence/15a-vacuity-dry-run.log)
- [expected result-obligation failure](evidence/15b-vacuity-kprove.log)

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What is formally proven

Under the submitted `MPY` generated semantics and K's imported integer,
Boolean, string, map, and sequencing theory, for every K integer triple
`A,B,C`, the exact submitted function body, when invoked from the specified
empty configuration, reaches an empty computation and local environment with
the result:

`A>0 and B>0 and C>0 and (A²+B²=C² or A²+C²=B² or B²+C²=A²)`.

The three concrete claims are instances of that theorem. The successful proof
does not depend on candidate prose, old traces, old compiled definitions, or
differential testing.

### Trust ledger and limitations

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell backend, reachability implementation | All builds and proofs | Ordinary unavoidable machine-checking trust boundary. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, configuration and `~>` primitives | Every semantic/equational rule | Acceptable standard K primitives; integer operations align with Python's unbounded integers for this code. |
| Trusted `/reference/py2mpy.py` transliteration | Program identity | Acceptable launcher-designated trust; independently rerun with byte identity. |
| Generated `run`/binding/evaluation semantics as a model of this one pure Python function | Connection from K theorem to Python execution | Structurally audited and concretely checked, but not proved against full CPython. Acceptable with concern because it executes every used construct and models no result-bearing operation opaquely. |
| Full Boolean evaluation in place of short-circuit skipping | Boolean body result/control | Acceptable only because every actual operand is pure and total. Excluded for general reuse with erroring/effectful operands. |
| Mathematical interpretation of `rightTriangle` | Human-facing intent | Positive lengths plus one Pythagorean equality is the standard right-triangle characterization. This intent bridge is transparent and independently compared with canonical on the positive domain. |
| `Int` argument domain | The universal theorem's scope | Non-fatal concern: all trusted examples are integers, but the untyped prompt does not explicitly exclude positive floats or other numeric types. Those are not formally covered. |
| Differential and concrete tests | Empirical semantics/canonical bridge only | Finite support (zero positive mismatches in the recorded scope), never used as a substitute for the K proof. |
| Canonical behavior on zero/negative inputs | Fidelity outside geometric side lengths | Explicitly differs. The candidate returns the geometrically appropriate `False`; this is outside the positive-side-length domain, not a false K conclusion. |

Gate A (real-program soundness): PASS. Gate B (intent adequacy for integer side
lengths): PASS, with the broader untyped-numeric scope concern. Gate C
(auditability): PASS; all relied-upon dynamic evidence, commands, statuses, and
bounded outputs are preserved. The scope/trust limitations are enough to
withhold an unqualified `PASS`, but they do not make the reconstructed theorem
vacuous, substituted, domain-bounded by finitely many values, or unsound.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
