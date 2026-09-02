# Independent adversarial review: 119-match-parens

The candidate's five positive claims can be reconstructed and do constrain the
return value, but the proof is not legitimate. Proof-local operational rules
replace the program-defined `is_good` call with `goodValue` without a
bridge-free connection theorem. A mutation that changes the helper body term
actually bound in the claimed program still proves the old helper summary and
the old entry theorem. On the concrete intended-domain input `["", ""]`, that
mutated program returns `No`, while the extended K theory proves `Yes`.

A second, independent witness shows that the proof-local `#forceGood` driver
ignores the actual value on which the branch is supposed to depend. It selects
THEN for an empty (falsey) value where the direct branch rule selects ELSE.
Thus the successful `#Top` results are closure under a materially unsound,
execution-bypassing extension, not a partial-correctness proof of the real
program.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1`, and the rendered
semantics mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mode and mounts do not
contradict one another.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required generation records, and
the complete structured trace. The trace contains one JSONL file with 977
parseable events and no malformed line. `usage.json` is present and was also
inspected. Historical runtime metrics are not required for this legacy layout.

Independent checks found:

- The campaign-lock JSON object exactly equals the `audit_campaign` block, and
  its SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required launcher/generation file is a readable regular file, every
  declared per-file hash matches, and the structured-trace file hash is
  `89df1143a53ef1bf73bcecf95c184b8c593e52c541be58ccdeec87629f3ea5ce`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Recursive name, type, and byte comparison of the complete candidate and
  trusted `reference-semantics/` trees found no missing, additional, changed,
  mistyped, or symlinked entry. There are no symlinks anywhere in the
  candidate.
- All five required proof artifacts are present and readable. Candidate-built
  `kore-exec.tar.gz` and `__pycache__` were not used.

The detailed checker and complete mounted-file hashes are in:

- `/audit-output/evidence/check_provenance.py`
- `/audit-output/evidence/01_provenance_check.log`
- `/audit-output/evidence/01_mounted_sha256.log`
- `/audit-output/evidence/01_required_record_inventory.log`
- `/audit-output/evidence/01_generation_json_records.log`
- `/audit-output/evidence/01_generation_text_records.log`

The generation report's prior claim of five `#Top` results was treated only as
an untrusted claim.

Stage 1 result: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`prompt.py` specifies a list of exactly two strings. Each string consists only
of `(` and `)`. The function must return `Yes` iff one of the two concatenation
orders is a balanced-parenthesis string, otherwise `No`. No length bound is
stated.

The canonical implementation checks both orders. Its scan rejects a negative
prefix and accepts at the end exactly when the final balance is zero.

The candidate's `is_good` uses `T` as its truthy witness and the empty string as
its falsey witness. `match_parens` tries `lst[0] + lst[1]`, then the reverse,
and returns `Yes` on either truthy result. On the stated parenthesis-only
domain, this is the same algorithmic property as the canonical implementation.

### Translation fidelity

In the clean scratch tree, I ran:

```text
python3 py2mpy.py solution.py > regenerated.mpy
cmp -s regenerated.mpy solution.mpy
```

Both `solution.mpy` files have SHA-256
`a6071588cfead0d98f814794ceb72ffda603737241e408b1bbee3a57d0e71b03`;
`cmp` exited 0. See
`/audit-output/evidence/02_translation_fidelity.log` and
`/audit-output/evidence/artifacts/regenerated.mpy`.

### Independent differential execution

`/audit-output/evidence/differential_test.py` imports the trusted canonical
entry point and the scratch copy of the candidate entry point independently.
It exercised:

- the two documented examples;
- empty, one-sided empty, early-negative, final-positive, first-order-only,
  and second-order-only boundaries;
- every ordered pair of component strings with each length from 0 through 6
  (16,129 pairs);
- 5,000 deterministic generated pairs with each component length from 0
  through 256.

There were 21,141 total invocations, zero targeted-case failures, and zero
mismatches. Exact command and output:
`/audit-output/evidence/02_differential.log`.

Stage 2 result: PASS. This is finite evidence of implementation fidelity, not
a substitute for a K proof.

## 3. Clean proof reconstruction

All sources needed for execution were copied to
`/tmp/audit-work/119-match-parens`. No candidate-compiled definition or cache
was copied. The live tools report K version `v7.1.293`.

### Fresh concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0. The candidate's five-assertion concrete test exited 0. A
reviewer-authored eight-assertion test covering examples and branch boundaries
also translated and ran with exit 0:

```text
python3 py2mpy.py audit-concrete.py > audit-concrete.mpy
krun audit-concrete.mpy --definition audit-runtime-kompiled --output none
```

Evidence:

- `/audit-output/evidence/03_llvm_build.log`
- `/audit-output/evidence/03_candidate_concrete.log`
- `/audit-output/evidence/03_auditor_concrete.log`
- `/audit-output/evidence/artifacts/audit-concrete.py`

The LLVM build warns about several fixed-semantics total functions outside
their defining equations. Of the warnings, only `valSeqAt` is related to this
program, and both actual indexes are provably in bounds for the required
two-element input. The other warnings concern unused float, join, and builtin
constructs.

### Fresh proof definition and every positive claim

```text
kompile verification.k --backend haskell \
  --main-module MATCH-PARENS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0. I then independently ran the candidate's dependency-ordered
proof targets:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module MATCH-PARENS-SPEC --claims loopCorrect --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect --trusted loopCorrect --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect,isGoodCorrect \
  --trusted loopCorrect,loopFirstCorrect --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims goodBranchCorrect --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensCorrect \
  --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect \
  --output pretty
```

Every command printed `#Top` and exited 0. The exact bounded logs are
`/audit-output/evidence/03_prove_*.log`.

Stage 3 reconstruction result: PASS. This establishes closure only under the
candidate's added theory; it does not establish that the theory is sound.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `loopCorrect`: from an `is_good` loop frame that already has a `char`
   binding, with nonnegative current balance and a fresh frame location, scan
   the remaining string, return `goodValue(S,B)`, pop the frame, restore the
   caller, and preserve heap and exceptional state.
2. `loopFirstCorrect`: the same result from the first-iteration form before
   `char` exists.
3. `isGoodCorrect`: for any string and fresh callee location, applying
   `isGoodClosure` returns `goodValue(S,0)` and restores the caller's state.
4. `goodBranchCorrect`: for nonnegative balance, branch selection based on the
   helper's `goodValue` witness agrees with the Boolean scan `goodFrom`.
5. `matchParensCorrect`: for arbitrary parenthesis-only sequences `A` and `B`,
   and fresh locations for the entry/helper frames, applying the exact
   two-element-list entry closure returns `Yes` iff either concatenation is
   `goodFrom`, otherwise `No`, while preserving the caller's other state.

The entry domain is not finitely bounded. `parensOnly` recursively covers every
finite `IntSeq`; the list shape is exactly two strings, as required by the
source contract.

### Constructor-level pinning

`/audit-output/evidence/generate_pinning_spec.py` derives K right-hand-side
terms from the trusted translator's in-memory constructor tree for
`solution.py`. It does not copy the corresponding bodies from
`verification.k`. Five reachability claims mechanically compare:

- `isGoodLoopBody`;
- `isGoodBody`;
- `matchParensBody`;
- `isGoodClosure`;
- `matchParensClosure`.

The final configuration-form pinning proof printed `#Top` and exited 0. See
`/audit-output/evidence/04_generate_pinning_config.log`,
`/audit-output/evidence/04_prove_pinning_config.log`, and
`/audit-output/evidence/artifacts/pinning-spec.k`. Two earlier reviewer harness
attempts are retained: one exposed a nested empty-list parsing issue and the
next exposed the backend's unsupported functional-claim form. The final
configuration claims eliminate both harness issues.

Thus the immutable named body and closure terms are constructor-identical to
the trusted translation. Omitting module loading is not itself a defect here:
the entry state explicitly binds `is_good` to the pinned helper closure.

### Satisfiable precondition and concrete substitution

Take:

```text
A = .IntSeq
B = .IntSeq
N = 1
BASE = .Map
MODULELOCALS = .Map
CALLER = 0
HEAP = .Map
HEAPLOC = 0
STACK = .List
CONT = .K
```

All freshness, `N >= 1`, and `parensOnly` conditions hold. Both Python
implementations return `Yes`. The corresponding ground K claim has the
explicit result `str(strToCodes("Yes"))`; it printed `#Top` and exited 0.
Evidence: `/audit-output/evidence/04_ground_witness.log` and
`/audit-output/evidence/artifacts/ground-witness.k`.

### Body-sensitivity failure

Pinning the original terms is not enough because proof-local rules preempt
their execution.

I created a fresh mutant in which the translated `is_good` body is exactly:

```text
Return(Str("")) .Stmts
```

The actual K term was changed in `isGoodBody`, and `isGoodClosure` still
contains that changed body. This is not an external-source-only mutation.
Source-derived pinning against the trusted translator printed `#Top` for the
changed helper body and closure:

- `/audit-output/evidence/artifacts/body-mutated.py`
- `/audit-output/evidence/artifacts/body-mutated.mpy`
- `/audit-output/evidence/artifacts/verification-body-mutated.k`
- `/audit-output/evidence/artifacts/pinning-body-mutated.k`
- `/audit-output/evidence/04_body_mutant_pinning.log`

The mutated Python program returns `No` on `["", ""]`
(`/audit-output/evidence/04_body_mutant_python.log`). Nevertheless:

- mutated `isGoodCorrect` printed `#Top`, exit 0;
- mutated `matchParensCorrect` printed `#Top`, exit 0;
- a ground mutated-program claim for the false result `Yes` printed `#Top`,
  exit 0.

See `/audit-output/evidence/04_body_mutant_is_good.log`,
`/audit-output/evidence/04_body_mutant_positive.log`, and
`/audit-output/evidence/04_body_mutant_false_ground.log`.

This is a concrete false-conclusion witness on a satisfying intended-domain
input. It demonstrates that the purported helper connection and entry proof do
not depend on the helper body they claim to verify.

Stage 4 result: FAIL.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/k_rule_inventory.py` lexically inventories every
declaration, rule, context, configuration, and claim in the 24 supplied
semantics source files, `verification.k`, and `spec.k`. The final inventory is
`/audit-output/evidence/05_rule_inventory_final2.log`.

It contains 989 records:

- 1 configuration;
- 5 contexts;
- 154 function declarations;
- 84 other syntax declarations;
- 738 ordinary rules;
- 2 simplification rules;
- 5 reachability claims.

For `verification.k` specifically, it contains every one of its 9 function
declarations, 2 other syntax declarations, 43 ordinary rules, and 2
simplification rules. The following grouping names every candidate rule and
records its decision.

| Candidate lines | Rules and decision |
|---|---|
| 8, 15 | Fresh Map insertion and deletion simplifiers. Correct under their freshness guards; they are symbolic forms of the hooked Map operations. |
| 21, 31, 44 | Literal assignment and `balance +/-= 1` fusions. Correct on the matched plain frame and integer binding; they preserve the fixed rule's cells and evaluation result. |
| 57 | `For(Name("char"), Name("s"), BODY)` to `#loop(str(S),...)`. Correct where matched: lookup is pinned to a direct string binding and has no side effect. |
| 69 | Operational bridge from applying `isGoodClosure` to a hard-coded loop/frame state. Illegitimate as a proof extension: it preempts execution of the closure body, and the alleged connection theorem `isGoodCorrect` is proved using this same bridge. The helper-body mutant above is the required false-result witness. |
| 101, 122, 144 | The two exact entry `If(Call(...))` bridges and `#runIsGood => goodValue`. They skip lookup, both subscripts, concatenation evaluation, helper application, and return. Their only proposed connection is `isGoodCorrect`, which is circular through line 69. The same pinned helper-body mutant makes this bridge chain prove `Yes` when the changed real helper makes the program return `No`. |
| 146 | Introduces `#forceGood(S,0)` while retaining an arbitrary actual value `V`; it supplies no equality between `V` and `goodValue(S,0)`. This exposes the unconstrained-value defect in lines 167-193. |
| 149, 152 | Direct `#goodBranch` cases for exactly `T` and empty. These agree with fixed truthiness for the helper's two actual witnesses. |
| 157, 160 | `#expectedBranch` Boolean cases. Guards are disjoint and exhaustive. |
| 167, 172, 180, 188 | The structural `#forceGood` driver ignores `_V` and chooses/reconstructs a branch solely from `S` and `B`. This family is over-broad; line 167 gives a concrete false transition for an opposite value. |
| 201 | Literal-string Return fusion. It evaluates the ASCII literal, sets `ret`, discards the function continuation, and enters `#pop`, matching fixed Return control. |
| 210, 221 | Character equality fusions. The guards `C == 40` and `C =/= 40` are disjoint/exhaustive and match string equality. |
| 232, 242 | `balance < 0` fusions. Correct, disjoint, and exhaustive over integers. |
| 252, 262 | `balance == 0` fusions. Correct, disjoint, and exhaustive over integers. |
| 272, 283 | Character-comparison `If` fusions. Correct under the pinned direct character binding. |
| 294, 304 | Negative-balance `If` fusions. Correct under the pinned integer binding. |
| 314, 324 | Zero-balance `If` fusions. Correct under the pinned integer binding. |
| 337, 347, 357 | Definitions of the loop, helper, and entry bodies. Their original terms are exactly source-derived, as the pinning proof establishes. |
| 374, 378 | Helper and entry closure definitions. Parameter lists, bodies, and defining environment 0 are source-faithful. |
| 385, 386 | `goodFrom`. Structurally recursive and total on `IntSeq`; it implements prefix-safe balance. |
| 396, 401 | `goodValue`. Structurally recursive and total; it returns exactly `T` or empty using the same scan. |
| 411, 412 | `parensOnly`. Structurally recursive and total; it accepts exactly codepoints 40 and 41. |
| 416, 419 | `expectedAnswer`. Guards are complements and right-hand sides are `Yes`/`No`; there is no overlap with different results. |

No candidate function is opaque: `goodFrom`, `goodValue`, and `parensOnly`
have complete structural equations. There is no candidate `[functional]`
declaration. Candidate `[total]` annotations are confined to those three
complete functions.

### Opposite-value false witness

`/audit-output/evidence/artifacts/opposite-value-witness.k` uses the
intended-domain empty string but deliberately supplies the opposite actual
value, `str(.IntSeq)`. Two ground claims show:

1. `str(.IntSeq) ~> #forceBranch(.IntSeq, THEN, ELSE)` writes `marker = 1`
   (THEN), because lines 146 and 167 ignore the actual value.
2. `str(.IntSeq) ~> #goodBranch(THEN, ELSE)` writes `marker = 2` (ELSE), the
   correct choice for the same falsey value.

Both claims printed `#Top`, exit 0. This is not merely a missing proof: it is a
machine-checked witness that the extended rewrite relation admits a false
branch transition. See
`/audit-output/evidence/05_opposite_value_witness.log`.

### Used fixed-semantics construct map

The selected supplied semantics is an integrity-checked trust boundary. All
928 fixed-semantics inventory records are classified as baseline rules rather
than candidate proof extensions. For the real submitted program, every used
constructor is covered as follows:

| Program construct | Fixed declarations/rules |
|---|---|
| `Module`, statement lists | `syntax.k:41-61`; `core.k:124-127` |
| `FuncDef`, parameters, closure | `syntax.k:53-60`; `functions.k:14-16`; `call.k:69-74` |
| `Name`, `Int`, `Str` | `core.k:130-154,193-205`; `str.k:13-17` |
| `Assign`, `AugAssign` | `controls.k:8-31` |
| `For`, string iteration, target bind | `controls.k:62-74`; `iter.k:8`; `str.k:8-10`; `tuple.k:31-40` |
| `If`, truthiness | `controls.k:50-54`; `core.k:198-205` |
| `Compare` | `operators.k:14-20`; `str.k:24-30`; `int.k:22-27` |
| string `BinOp("+")` | `operators.k:10-17`; `str.k:20-26` |
| list `Subscript` 0/1 | `subscript.k:6-41`; the formal list shape makes both accesses in bounds |
| `Call`, argument order, frame lifecycle | `call.k:18-21,69-74`; `core.k:183-191`; `functions.k:62-90` |
| `Return` | `functions.k:77-90` |

The fixed tree declares 25 explicitly symbolic/opaque functions:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`. None can occur in this program or its
proof obligations: there is no float, MD5, sorted, or keyed-sort syntax.
Their complete inventory and concrete legs are retained in the Stage 5 log.

### Claim assessment

- `loopCorrect` and `loopFirstCorrect` genuinely reason over the real loop
  state and appear mathematically sound.
- `isGoodCorrect` is not a connection theorem for line 69 because it imports
  and uses line 69.
- `goodBranchCorrect` states a true mathematical relationship, but its
  machine closure relies on the globally false `#forceGood` driver.
- `matchParensCorrect` has an adequate domain and result, but its closure uses
  the invalid helper bridge and the invalid branch driver.

Stage 5 result: FAIL.

## 6. Fresh non-vacuity test

I created a distinct ground spec that keeps the original program and satisfying
empty/empty entry state but mutates the required result from `Yes` to `No`:

`/audit-output/evidence/artifacts/spec-vacuity-auditor.k`.

Compilation-only command:

```text
kprove spec-vacuity-auditor.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDITOR \
  --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,falseEmptyIsNo \
  --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect \
  --dry-run
```

This exited 0, so the mutation built successfully. Running the same claim
without `--dry-run` exited 1 with `WarnStuckClaimState`. The residual contains
`str(iCons(89, iCons(101, iCons(115, .IntSeq))))`, namely `Yes`, which cannot
unify with the mutated `No` destination. This is the expected unmet result
obligation, not a parser error, crash, timeout, or unrelated stuck state.

Evidence:

- `/audit-output/evidence/06_false_mutation_dry_run.log`
- `/audit-output/evidence/06_false_mutation_proof.log`

Stage 6 result: PASS. The original claim is non-vacuous and
result-constraining. Non-vacuity does not repair the unsound execution bridge.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the candidate's complete extended rewrite theory, the five stated
reachability claims close. In particular, for unbounded parenthesis-only
`IntSeq` values and the stated fresh-map conditions, the proof-defined entry
closure reaches the recursively defined `expectedAnswer(A,B)`. The theorem is
not a tautology or free-result claim.

That conditional fact is weaker than the requested fact because the extended
theory is not a sound execution theory for the bound helper.

### Trust ledger

| Boundary | Effect and assessment |
|---|---|
| Supplied K semantics | Trusted by `SUPPLIED_SEMANTICS` mode and byte/type identical to the reference tree. It models all material source constructs. Acceptable baseline. |
| K built-in Int, Bool, String, Map, List, and equality hooks | Affect arithmetic, codepoints, scopes, and sequence structure. Ordinary low-level K trust boundary; acceptable. |
| K compiler/backend and reachability logic | Establish `#Top` relative to the loaded theory. Necessary low-level trust boundary; accepted, but it does not certify added-rule truth. |
| Trusted translator | Establishes source-to-constructor fidelity. Byte regeneration and source-derived pinning support this bridge. Acceptable. |
| `goodFrom`, `goodValue`, `parensOnly`, `expectedAnswer` | Fully equational proof-local mathematics, not opaque. Their equations are terminating, appropriately covered, and consistent. Acceptable in isolation. |
| Line 69 helper-call bridge | Program-derived, result- and control-bearing. It has no bridge-free universal connection theorem; the theorem offered as its justification uses the bridge itself. The body mutation shows a false result. Illegitimate. |
| Lines 101/122/144 entry-call bridge | Skips material lookup, indexing, concatenation, helper call, return, and frame lifecycle. Its only helper connection is the circular line-69 theorem. The same false mutation witnesses the failure. Illegitimate. |
| Lines 146/167-193 branch driver | Program-derived control abstraction. It leaves the actual value unconstrained and can select the opposite observable branch. The ground marker witness proves this. Illegitimate. |
| 25 fixed opaque symbols | Listed in Stage 5. None is reachable from this program or any result obligation, so none affects the theorem. Acceptable excluded boundary. |
| Differential tests | Support only Python implementation-to-canonical behavior for the 21,141 tested inputs. They neither universally prove equivalence nor justify a K operational bridge. |
| Human-facing balance interpretation | `goodFrom` directly implements the standard nonnegative-prefix/final-zero definition, and `expectedAnswer` checks both concatenations. This intent bridge is straightforward and domain-complete. |

### Gate results and decision

- Gate A, real-program soundness: FAIL. The proof is body-insensitive at the
  program-defined helper and contains a concrete false branch rule.
- Gate B, intent adequacy: PASS in isolation. The entry domain is the full
  source-contract domain and the postcondition is the requested result.
- Gate C, evidence auditability: PASS for the reconstructed evidence. All
  commands, scripts, mutations, and bounded logs are retained under
  `/audit-output/evidence/`.

The Gate A failure is decisive. The body-mutant false theorem and the
opposite-value branch witness meet the benchmark's false-conclusion-witness
requirement. A clean `#Top`, correct implementation, adequate domain, and
successful non-vacuity test cannot make an unsound execution theory legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
