# Independent adversarial audit — 163-generate-integers

The candidate contains a legitimate, universal partial-correctness proof for the
generated program over the complete stated domain of positive integers. I did
not rely on the candidate's prior `#Top`, logs, or final report. I reconstructed
the definitions from source, proved the target claim afresh, mechanically pinned
the claim term to the trusted regenerated program, exhaustively inventoried the
K theory, and rejected independent body/result mutations.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mounts do not
contradict the rendered mode.

I inspected `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required legacy-selected-stage1
record under `/generation-evidence`, and all 139 JSONL events in the structured
trace. The trace contains 22 recorded function calls and 22 outputs; its prior
proof claims were treated only as untrusted history. See
`evidence/stage1-trace-summary.log` and the parser
`evidence/trace_summary.py`.

Independent integrity results are in `evidence/stage1-integrity.log`:

- Every required record and launcher-declared container path is present,
  readable, and of the required real file/directory type.
- The campaign block equals `/audit-campaign-lock.json`, whose SHA-256 is the
  recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All recorded per-file hashes for the run/task/result/invocation/metrics/usage,
  prompt, output, last message, canonical, candidate/trusted prompts, and
  candidate/trusted translators match.
- All hashes listed by `/generation-result.json`, including the JSONL trace,
  match their mounted files.
- A fresh launcher-format tree hash of `/candidate` is
  `b503467b42bcdfbad996570b1bdeb1c76fd6319dd443f49021807ebb665b56ff`;
  it matches both the retained workspace hash in the invocation and the
  workspace hash in the generation result.
- A fresh launcher-format trace-tree hash is
  `06875cb118872f953b9330adb4d02b7d8cb72b26e72e45625b529f6eea2e8dce`,
  matching `usage.json`.
- The candidate and trusted prompts are byte-identical. The candidate and
  trusted translators are byte-identical.
- Recursive type/path/content comparison found exactly 25 entries in each
  supplied-semantics tree, no missing or additional entry, no symlink, and no
  content difference. The trusted tree's fresh launcher-format hash is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  equal to the recorded manifest-format semantics hash.
- The seven required candidate proof artifacts are ordinary regular files, not
  symlinks.

`/audit-input.json` enriches its embedded task-manifest object with one `config`
field that is not physically present in `/task.json`; removing that enrichment
makes the objects equal, and the independently recorded `/task.json` hash
matches. This is metadata normalization, not a missing, unreadable, or corrupted
provenance mount.

Stage 1 result: pass; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify this contract: for two
positive integers `a` and `b`, return in ascending order those even decimal
digits among `2, 4, 6, 8` that lie in the inclusive interval with endpoints
`a` and `b`; endpoint order is irrelevant. Thus `(2,8)` and `(8,2)` both
produce `[2,4,6,8]`, while `(10,14)` produces `[]`.

`/candidate/solution.py` implements that contract directly. It starts with an
empty list and, in order, appends each of `2, 4, 6, 8` precisely when

```text
(a <= d <= b) or (b <= d <= a).
```

This is equivalent to the canonical clamp/range/comprehension algorithm on all
positive integers, not merely the examples.

I copied sources into `/tmp/audit-work` and regenerated the program with the
trusted translator. Fresh and submitted `solution.mpy` both have SHA-256
`dafb407d62efa4ca95522f0d622eef6ac8fc1f185dc7768678e93dd9a6a6d792`;
`cmp` exited 0. See `evidence/stage2-translation.log`.

The independent differential script `evidence/differential_test.py` imports the
trusted canonical and generated candidate under distinct module names. Its
scope was:

- all three documented examples;
- 17 empty-result, singleton, endpoint, and adjacent-boundary cases;
- all 121 ordered pairs over `1,2,3,4,5,6,7,8,9,10,14`;
- all 4,096 positive pairs with each endpoint in `1..64`;
- 1,000 deterministically generated positive pairs up to 1,000,000.

There were 5,096 unique pairs and zero mismatches. Full inputs, hashes, and
results are in `evidence/stage2-differential.log`. This finite test supports the
implementation-to-contract bridge; it is not being used as the K proof.

Stage 2 result: pass.

## 3. Clean proof reconstruction

All work was performed in `/tmp/audit-work` from source copies. No
candidate-provided kompiled definition or cache was used. The installed
`kompile`, `krun`, and `kprove` are K v7.1.293.

The exact command ledger is `evidence/COMMANDS.md`; every transcript ends with
the actual exit status. The material reconstruction results were:

| Operation | Result | Evidence |
|---|---|---|
| Trusted translation of reviewer concrete suite | exit 0 | `stage3-toolchain-and-test-generation.log` |
| Fresh LLVM `MPY-KRUN` build | exit 0 | `stage3-kompile-llvm.log` |
| Reviewer-authored concrete execution | exit 0; `.K`, `NoExc`, exit code `0` | `stage3-krun-independent.log` |
| Fresh Haskell `VERIFICATION` build | exit 0 | `stage3-kompile-haskell.log` |
| Sole positive target claim in `SPEC` | exit 0; `#Top` | `stage3-kprove-positive.log` |

The concrete suite source is `evidence/audit_concrete_tests.py`. It covers the
prompt examples, reversed bounds, all four singleton digit boundaries, empty
results, and full-span results.

The LLVM compiler warned that a few supplied total functions are non-exhaustive
on constructors such as `cellsMark`, and both builds reported unused variables
in `strLt`. None of those functions or string rules occurs on this program's
execution or proof path. More importantly, those warnings represent possible
stuckness outside the used subset; they do not fabricate a value used to close
this claim.

There is exactly one positive target claim. It closes under a clean source
reconstruction.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The claim in `/candidate/spec.k:6` starts from the ordinary empty module
configuration with module scope `0`, builtins scope `-1`, no heap objects, no
stack frames, no return/exception, and exit code `0`. Its precondition is
exactly:

```text
A > 0 and B > 0.
```

It loads one module defining `generate_integers`, calls that binding with the K
integers `A` and `B`, and requires the call to return `ref(0)`. At the
destination:

- scope `0` contains the exact closure for that function;
- heap object `0` is exactly `list(evenDigits(A,B))`;
- `heapLoc` advanced from `0` to `1`;
- the callee frame has been removed, the module environment is restored, the
  stack is empty, and return/exception/exit cells are normal.

`evenDigits(A,B)` is not a free or opaque value. It is the finite sequence
obtained by testing, in ascending order, whether each of `2,4,6,8` lies
inclusively between the endpoints.

### Mechanical program identity

The claim uses the macro `solutionModule`, not a file loader. I therefore did
not infer source identity by inspection alone. With the freshly built
definition I parsed and fully macro-expanded:

1. the claim's `solutionModule`, and
2. the trusted-regenerated `solution.mpy`.

The resulting KORE files
`evidence/stage4-claim-program.kore` and
`evidence/stage4-submitted-program.kore` are byte-identical, both with SHA-256
`82be447ca8be261d7dce56785962c49b27946b91e9a94c1f53cafb93650a8a04`.
The exact commands and successful `cmp` are in
`evidence/stage4-program-pinning.log`.

Thus the theorem executes the submitted function binding and body. The
`generateIntegersClosure` macro in the destination is also that exact body with
definition environment `0`; it does not replace execution.

### Satisfiability and concrete substitutions

The precondition is plainly satisfiable, for example by `(A,B)=(3,7)`,
`(10,14)`, and `(8,2)`. I instantiated those inputs in three independent ground
reachability claims. They closed with explicit result heaps `[4,6]`, `[]`, and
`[2,4,6,8]`, respectively (`evidence/spec-witnesses.k` and
`evidence/stage4-ground-witnesses.log`). Those values agree with both Python
implementations in `evidence/stage2-differential.log`.

There is no finite bound or example-only restriction: K `Int` is unbounded and
the sole formal restriction is positivity, exactly as in the source contract.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` generated
`evidence/rule-inventory.tsv`. It inventories every module/import/require,
syntax declaration, configuration, context, rule, and claim in the complete
trusted supplied-semantics tree plus candidate `verification.k` and `spec.k`.
The 1,109 records include:

- 702 rules;
- 233 syntax declarations;
- 49 priority-bearing entries;
- 26 entries involving opaque/no-evaluator declarations;
- 5 evaluation contexts;
- 1 configuration and 1 claim.

There are no `functional` declarations and no simplification rules. Every row
contains its source span, attributes, classification, rationale, and bounded
source excerpt. Counts and the generation exit status are in
`evidence/stage5-inventory-generation.log`.

### Used syntax and execution map

| Submitted constructor | Declaration/behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` module sequencing; `functions.k` exact closure creation |
| `Call`, `Name` | left-to-right callee/argument routing in `call.k`; lexical lookup in `core.k`; exact closure-frame rule |
| `Assign`, `ListExpr` | RHS strictness and scope write in `controls.k`; argument fold, allocation, and monotone heap location in `core.k`/`list.k` |
| `BoolOp("and"/"or")` | head-only, value-returning short-circuit rules in `bool.k` |
| `Compare(...,"<=")` | left then right evaluation in `operators.k`; exact unbounded integer comparison in `int.k` |
| `If` | strict condition and exhaustive true/false branch rules in `controls.k` |
| `Attribute(...,"append")`, `Call` | receiver first, then argument evaluation in `call.k`; the priority-40 append rule performs the exact in-place list-heap update in `list.k` |
| `Expr` | discards only the returned `noneV` after the append effect in `controls.k` |
| `Return` | evaluates its expression, sets `retV`, discards the remaining body, pops the exact frame, restores the caller environment/scope location, and preserves the escaping heap object in `functions.k` |

The concrete control/state trace is therefore: module load binds the exact
closure in scope `0`; the call allocates frame `1` and binds `a,b`; the empty
list allocates heap location `0`; four comparisons are evaluated with Python
short-circuit order; each true condition mutates that same heap object; return
pops frame `1` but deliberately retains heap object `0`. The claim constrains
every cell affected by this path.

Specialized priority rules for cell references, floats, md5, sorting, and other
constructs have guards or constructor heads disjoint from this configuration.
The proof imports `MPY`, not `MPY-KRUN`, so the runtime-only
`MPY-CONCRETE` rules cannot contribute to `#Top`.

### Candidate extensions

The candidate contributes no operational bridge, priority rule, opaque symbol,
oracle, simplification, or auxiliary circularity.

- `generateIntegersBody`, `solutionModule`, and
  `generateIntegersClosure` are syntax macros. Full macro expansion proves the
  first two are the real module/body; the closure macro fixes the same
  parameters, body, and environment.
- `betweenEndpoints` is a total definitional summary over K integers. Its
  single equation is exactly inclusive membership in either endpoint order.
- `keepDigit` has two disjoint and exhaustive equations over K `Bool`.
- `evenDigits` is a nonrecursive, terminating composition of those definitions
  for exactly `2,4,6,8`.

These summary functions occur only in the destination heap. They do not
intercept or rewrite any program construct, so there is no circular
program-derived abstraction and no missing connection theorem.

All opaque primitives in the supplied reference semantics are for floats,
hashing, or sorting and are absent from the constructor-level program and every
reachable state. The supplied semantics is intentionally a minimal Python
subset; unused unsupported cases may stick or use an explicitly declared
subset abstraction. No such case is used to derive this theorem. I found no
false conclusion enabled by any rule on the complete positive-input execution
domain, so there is no unsound-rule allegation requiring a false witness.

### Body sensitivity

As a separate operational-sensitivity check, I compiled
`evidence/verification-body-mutation.k`, whose executed function body was
materially changed to always allocate and return an empty list. The independent
ground claim for `(8,8) -> [8]` built successfully and then exited 1 with
`WarnStuckClaimState`; the residual exposes the actual empty heap. See
`evidence/stage5-body-mutation-build.log` and
`evidence/stage5-body-mutation-proof.log`.

Stage 5 result: pass.

## 6. Fresh non-vacuity test

The candidate provides no `spec-vacuity.k`, so no candidate mutation evidence
was trusted.

I created `evidence/spec-vacuity.k`. It executes the actual pinned program at
the satisfying positive input `(2,8)` but deliberately requires the wrong heap
`[2,4,6]`, omitting the required final `8`.

The mutation's dry run parsed and compiled successfully with exit 0
(`evidence/stage6-vacuity-dry-run.log`). The actual proof then exited 1 with
`WarnStuckClaimState` and the expected unmet obligation. Its residual contains
the fully executed real heap `[2,4,6,8]`, so failure is due to the reachable
result mismatch—not a parser error, missing import, timeout, or unrelated crash.
See `evidence/stage6-vacuity-proof.log`.

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What the K proof establishes

For every pair of unbounded K integers `A,B` satisfying `A>0` and `B>0`, from
the clean module configuration stated in `SPEC`, execution of the exact
trusted-regenerated `solution.mpy` function under the supplied MPY semantics
returns the sole newly allocated list reference. That list contains, in
ascending order and without extras or duplicates, exactly those members of
`[2,4,6,8]` inclusively between `A` and `B` in either order. The call restores
the environment/stack/return/exception cells and exits normally.

This is the requested partial-correctness theorem over the full source-contract
domain. The body is finite and has no loop or recursion; the symbolic proof in
fact executes all four branches to terminal configurations, but the verdict
does not rely on a stronger total-correctness interpretation.

### Trust ledger

1. **K toolchain and backend.** K v7.1.293, the Haskell backend, SMT arithmetic,
   and K's built-in `Int`, `Bool`, `Map`, and `List` theories are trusted. They
   affect execution and proof closure. Fresh build/proof transcripts support
   this boundary.
2. **Supplied MPY semantics.** This is the launcher-selected fixed semantics,
   not candidate-generated semantics. Its entire candidate copy is exactly the
   trusted tree. The used rules for lookup, calls, lists, integer comparisons,
   short-circuiting, state, and return were statically reviewed and concretely
   exercised. No opaque MPY symbol affects the result, control, state, or
   postcondition.
3. **Trusted translator.** The CPython-AST-to-constructor translator is outside
   the K theorem. Its mounted/candidate copies match, and fresh translation is
   byte-identical to the submitted program. This establishes the submitted
   `.py` to `.mpy` artifact bridge.
4. **Claim-term identity.** This is not informal: full K macro expansion and
   KORE byte comparison mechanically connect `solutionModule` to the
   regenerated `solution.mpy`.
5. **Intent bridge.** Ordinary mathematics connects `evenDigits` to the prompt:
   the only even decimal digits are `2,4,6,8`, each is included exactly under
   inclusive endpoint membership, and construction order is ascending.
   Differential testing against the independent canonical provides finite
   supporting evidence but is not substituted for the universal K proof.
6. **Execution model boundary.** Inputs are mathematical/Python integers, with
   arbitrary precision and only comparisons used. The natural-language
   positive-integer domain excludes nonpositive values and non-integer Python
   objects; the formal theorem excludes exactly those. No behavior outside that
   stated domain is claimed.

There is no externally trusted result-bearing primitive, empirical oracle,
proof-local operational bridge, or informal assumption that determines the
returned list. Gate A (real-program soundness), Gate B (intent adequacy), and
Gate C (trust/evidence auditability) all pass. Under the Kit terminology this is
`VALIDATED`; under the benchmark decision boundary it is `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
