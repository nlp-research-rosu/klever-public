# Independent adversarial audit — HumanEval 84 `solve`

Conclusion: the candidate contains a legitimate, result-constraining proof for
the complete stated finite domain.  I assign `CONCERNS / LEGIT`, rather than
`PASS`, because one generated semantic rule is broader than its justification:
tuple-literal subscripting skips evaluation of unselected elements.  That
difference is inert for this exact program (all elements are pure string
literals), so it does not permit a false conclusion on an intended input and
does not invalidate the proof.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `84-solve`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- no mounted reference semantics.

I read the launcher-owned audit input and campaign lock, then the records
required for this layout: `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the JSONL trace.  The trace has 356 valid JSON records and no
malformed line.  These generation records were treated only as claims.
Historical `runtime-metrics.json` is absent, which is permitted for this
legacy-selected layout.

Independent integrity findings:

- `/audit-campaign-lock.json` is byte-hash
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the audit-input hash, and its parsed object exactly equals the
  embedded campaign block.
- Trusted hashes independently reproduce as canonical
  `1ff15bd351232cf563e357042abb5f32fabc29ba50f1bf62358fbf0060176c1b`,
  prompt
  `5b69b9b354c92bcb61d5e63ec962c1df7cc559708ce12f54b705344d47dc5b28`,
  and translator
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Independent pipeline tree hashing gives candidate digest
  `0fd0b2738f0c86928b937d37518429e0060c8192300a3b92b08c3b91c9c578a9`,
  matching both the generation result and retained-workspace invocation
  records.  The trace tree digest
  `c00493b24fe31fc461c2080e4b3197306a0a3280f4135fb850d0967eeb15de5e`
  matches `usage.json`; its sole file hash also matches the invocation and
  result records.
- All required mounts and records are regular and readable.  No symlink occurs
  below `/candidate`, `/generation-evidence`, or `/reference`.
- `/reference/reference-semantics` is absent, as required.  I did not infer or
  use a hidden semantics.
- All required candidate proof sources are present.  Candidate-provided
  `semantic-kompiled-haskell/` was deliberately excluded from reconstruction.

Commands, type checks, hashes, and statuses are preserved in
`evidence/stage1_integrity.sh` and `evidence/stage1_integrity.log` (overall
exit 0).  There is no infrastructure breach.

## 2. Program fidelity and canonical comparison

The trusted contract is: for an integer `N` with `0 <= N <= 10000`, sum the
decimal digits of `N` and return that sum's base-two numeral as a string without
a prefix.  Thus `1000 -> "1"`, `150 -> "110"`, `147 -> "1100"`, and the
explicit lower bound gives `0 -> "0"`.  There is no empty value in the declared
integer domain.

`/candidate/solution.py` extracts the five possible decimal positions, adds
them, and indexes a 37-entry table containing the binary strings for 0 through
36.  On this domain, 9999 supplies the maximum index 36; 10000 supplies index
1.  The implementation therefore covers the complete contract domain.

Trusted regeneration command:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/84-solve/regenerated-solution.mpy
```

It exits 0, and `cmp` establishes byte identity with submitted
`solution.mpy`; both hash to
`d4c0890bb55d57ae5c6f803c7bc12dd0d735074d767c8269bcdd473cbcf84d36`.

`evidence/differential_test.py` independently loads the trusted canonical and
candidate entry points.  It checks the documented examples, zero and both
domain endpoints, values adjacent to every decimal-place boundary, 127
seeded representative inputs, and exhaustively every integer 0 through 10000.
Result: 10,001 unique inputs, zero mismatches, exit 0.  The exact runner and
output are `evidence/stage2_program_fidelity.sh` and
`evidence/stage2_program_fidelity.log`.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/84-solve`; no compiled
candidate definition or cache was copied.  The installed independently
invoked tools report K version 7.1.293.

Fresh build commands:

```text
kompile --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled semantic.k

kompile --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled semantic.k
```

Both exit 0.  Logs are `evidence/stage3_kompile_haskell.log` and
`evidence/stage3_kompile_llvm.log`.

Fresh LLVM `krun` executions at
`0,1,9,10,99,100,147,150,999,1000,9999,10000` all exit 0 and match the
trusted Python result.  The script records each complete final configuration
in `evidence/stage3_concrete_semantics.log`.

I then ran every target claim separately:

```text
kprove /tmp/audit-work/84-solve/spec.k \
  --definition /tmp/audit-work/84-solve/verification-kompiled \
  --spec-module SPEC --claims <claim>
```

The claims are `SPEC.inputs-00000-00999`,
`inputs-01000-01999`, `inputs-02000-02999`,
`inputs-03000-03999`, `inputs-04000-04999`,
`inputs-05000-05999`, `inputs-06000-06999`,
`inputs-07000-07999`, `inputs-08000-08999`,
`inputs-09000-09999`, and `SPEC.input-10000`.  Each of the eleven commands
exits 0 and prints `#Top`.  Individual bounded logs and the aggregate command
record are `evidence/stage3_kprove_*.log` and
`evidence/stage3_all_positive_claims.log`.

Each run also prints `WarnTrivialClaim`: the fully ground `checkRange` function
simplifies to `true` before reachability rewriting.  This is concrete K
evaluation, not by itself proof of honesty.  Stages 4–6 establish source
pinning, rule truth on the target, body sensitivity, and rejection of a false
result.

## 4. Adequacy and real-program pinning

There are eleven entry claims and no symbolic precondition.  Each start state
is the ground, satisfiable cell `<k> checkRange(L,U) </k>` and each destination
requires that cell to contain `true`.  The intervals are half-open:
`[0,1000)`, `[1000,2000)`, ..., `[9000,10000)`, and `[10000,10001)`.
Their disjoint union is exactly the source-contract domain.

`checkRange` is a proof-time finite fold, not a claimed source loop.  For each
integer it calls `checkInput`, which compares:

```text
runProgram(solutionProgram, N)
```

with:

```text
oracleBinary(oracleDigitSum(N))
```

`runProgram` pattern-matches the actual one-function module, binds its actual
parameter string, and evaluates its actual `Return` expression.  The returned
string is therefore constrained by equality to an independently defined
decimal-digit-sum/binary conversion, not a free variable, implication, or
tautological shared oracle.

Mechanical constructor pinning used the fresh definition:

```text
kast solution.mpy --definition verification-kompiled \
  --module MPY-SYNTAX --sort Pgm --output json
kast --expression solutionProgram --definition verification-kompiled \
  --module VERIFICATION --sort Pgm --expand-macros --output json
```

The two JSON constructor terms are byte-identical and hash to
`3309d2a7ad317251d807b41f215e09229e5751334e453412aceba72d2e1301ca`.
Thus the manually embedded macro is the current trusted-regenerated
`solution.mpy` term.  Manual embedding is a maintenance risk, but not an
identity gap for this immutable candidate.

One representative for every interval—`0,1000,2000,...,10000`—was compared
three ways: trusted canonical Python, candidate Python, and fresh LLVM K
execution.  All eleven agree.  See
`evidence/stage4_pinning_and_witnesses.log`.

For body sensitivity, I changed the first string literal inside the actually
executed `solutionProgram` macro from `"0"` to `"WRONG"`; I did not merely
change the external Python file.  The mutated definition builds, but the first
target claim exits 1 with `WarnStuckClaimState` and residual `<k> false`.
Artifacts are `evidence/verification-body-mutation.k`,
`evidence/stage4_body_mutation.diff`, and the two
`stage4_body_mutation_*.log` files.

## 5. Rule-by-rule static soundness review

The complete line-numbered inventory is
`evidence/stage5_rule_inventory.md`; source extraction is in
`evidence/stage5_declaration_extract.log`.  There are three local K source
files and no helper K file.  The inventory contains:

- constructor syntax for `Module`, `FuncDef`, `Params`, `Return`, six
  expression forms, nonempty expression lists, three values, and two value-list
  forms;
- fourteen `[function]` symbols;
- one `solutionProgram` macro;
- nineteen operational semantic rules;
- thirteen verification equations including the macro equation; and
- eleven reachability claims.

There are no local `total`, `functional`, `simplification`, priority, opaque,
context, or alias declarations.

Every semantic rule was reviewed:

| Rules | Judgment |
|---|---|
| S1–S3: parameter lookup and integer/string literals | Faithful for the submitted binding and literals. |
| S4–S6: integer `+`, `//`, `%` | Faithful for nonnegative operands and positive literal divisors. Python and K differ outside some integer/divisor cases, but none is reachable here. |
| S7: tuple construction | Truthful `VCons` construction for the pure expressions. |
| S8: tuple-literal subscript | Selects directly with `evalNthExpr`, skipping unselected evaluations. Every target element is a pure string literal and every target index is 0..36, so the target result and all observable state agree. The rule is over-broad for reusable Python semantics: outside this fixed program, an unselected `1 // 0` would raise in Python but could be skipped here. That is a narrower generality/evidence limitation, not an intended-domain unsoundness claim; there is no intended input witnessing a false target conclusion. |
| S9–S10: tuple/integer projections | Truthful and partial on wrong value kinds rather than result-fabricating. |
| S11–S12: `evalExprs` | Correct singleton/cons construction with structural descent. |
| S13–S15: `evalNthExpr` | Correct zero and positive-index cases; shapes/guards are disjoint and recursion descends. |
| S16–S17: `nthValue` | Correct guarded list indexing; unused by the direct target path. |
| S18: `runProgram` | Executes the exact body and binding; no oracle replaces program execution. |
| S19: configuration rule | Consumes the program, preserves input, and computes `runProgram` in result. |

The configuration has only `<k>`, `<input>`, and `<result>`.  The submitted
function is a pure single return expression, so no heap, allocation, mutation,
I/O, exception stack, or call stack is materially omitted.  K function
evaluation need not preserve CPython operand order when operands are pure; all
target operations are pure and defined.  The direct tuple rule changes eager
order only for side-effect-free string literals, so no target control or state
effect is lost.

Every verification equation was reviewed:

| Rules | Judgment |
|---|---|
| V1: `solutionProgram` | Exact macro term by fresh constructor comparison. |
| V2–V3: `oracleDigitSum` | Disjoint guards cover all nonnegative integers; recursive division decreases and the equations are ordinary decimal digit-sum mathematics. |
| V4–V7: binary zero/positive conversion | Disjoint zero, one, and greater-than-one cases; positive recursion decreases. |
| V8–V9: append bit | Disjoint and complete for reachable remainders 0 and 1. |
| V10: `sameValue` | Truthful string equality on both reachable `VStr` arguments. |
| V11: `checkInput` | Compares real execution with the independent specification; it is result-bearing but not opaque or circular. |
| V12–V13: `checkRange` | Correct base/step fold with disjoint cases and finite descent on every claimed interval. |

No equation overlaps inconsistently; no reachable function call lacks a rule;
no rule supplies an unconstrained fresh value; no local rule encodes the task
answer as an operational rewrite.  The string table is program data and is
executed through the exact AST.  The source-contract bound makes exhaustive
finite claims adequate here; this is not a fixed-size narrowing of an
unrestricted domain.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`, so no candidate mutation evidence
was relied on.  I created `evidence/spec-vacuity-audit.k` with the fresh claim:

```text
<k> checkRange(10000, 10001) => false </k>
```

This changes the result-constraining destination.  Its start is unconditional
and satisfiable; input 10000 gives `"1"` in both Python implementations and
the original K computation gives `true`.

Validation commands:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The dry run exits 0, establishing that the mutation parses and builds.  The
proof exits 1 with `WarnStuckClaimState`; the residual `<k>` contains `true`
and cannot unify with destination `false`.  This is the expected unmet
obligation, not a parser error, missing import, timeout, or unrelated crash.
See `evidence/stage6_mutation_dry_run.log` and
`evidence/stage6_mutation_kprove.log`.

## 7. Proven versus assumed accounting

What the successful reachability proofs establish is precise: under the local
generated K definition, for every integer `N` from 0 through 10000, evaluating
the exact submitted constructor body through `runProgram` returns the same
`VStr` as the recursively defined binary representation of the recursively
defined decimal digit sum.  This is a partial-correctness statement; the
concrete ground reductions also terminate for every claimed input.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell prover/backend, and LLVM executor | All machine results | Standard unavoidable proof-tool trust; independently rebuilt and cross-checked. Acceptable. |
| Imported K `INT`, `BOOL`, and `STRING` primitives (`+Int`, `/Int`, `%Int`, comparisons, Boolean conjunction/equality, string concatenation/equality) | Expression semantics and mathematical oracle | Fixed low-level primitives, not task-specific answer rules. Their used nonnegative/positive cases agree with ordinary arithmetic. Acceptable. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Launcher-trusted mount; byte regeneration and constructor comparison are recorded. Acceptable. |
| Generated source-language semantics | Connection from constructor program to Python behavior | Audited rule by rule and concretely tested on boundaries. S8 is intentionally flagged as over-broad outside the fixed pure tuple; this is the reason for `CONCERNS`. |
| Manual `solutionProgram` macro | Program term used by claims | Mechanically equal to current trusted-regenerated AST; body mutation affects the proof. Acceptable for this immutable candidate, with maintenance risk only. |
| `oracleDigitSum`/`oracleBinary` meaning | Bridge from formal postcondition to English contract | Transparent terminating equations justified by ordinary mathematics. They are not opaque symbols. Exhaustive Python differential testing is supporting evidence, not a substitute for the K proof. Acceptable. |
| Trusted canonical Python implementation | Differential oracle | Used only for program/intent evidence. It is not imported by K and does not close any claim. |

There are no opaque symbols, empirical result oracles, assumed helper claims,
proof-local simplification axioms, or trusted program-defined bodies.  The
generation report, old `#Top`, and candidate compiled cache contribute nothing
to the conclusion.

Kit gate accounting:

- Gate A (real-program soundness): pass.  Fresh claims close; exact AST
  identity, intended-domain rule truth, result constraint, body sensitivity,
  and false-result rejection are established.
- Gate B (intent adequacy): pass.  The formal union covers the complete stated
  finite domain and the postcondition matches the requested digit-sum binary
  string.
- Gate C (trust/evidence auditability): pass with a documented non-fatal
  generated-semantics limitation.  All commands, scripts, inputs, and bounded
  outputs are preserved under `/audit-output/evidence`.

The limitation does not make a false conclusion provable for the submitted
program, so the proof remains legitimate; it prevents an unqualified `PASS`
for the generated language definition's broader advertised syntax.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
