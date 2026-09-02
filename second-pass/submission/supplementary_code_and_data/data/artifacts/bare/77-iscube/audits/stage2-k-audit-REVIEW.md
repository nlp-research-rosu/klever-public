# Independent adversarial review: 77-iscube

The candidate contains a legitimate, result-constraining partial-correctness
proof of its submitted program. I reconstructed both definitions solely from
source, reran every claim, checked the generated semantics rule by rule, pinned
the claim program to the trusted retransliteration, and obtained the expected
failure from fresh body and postcondition mutations. No candidate-produced
compiled definition, trace conclusion, or prior `#Top` was trusted.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. The campaign object in
`/audit-campaign-lock.json` is structurally identical to the
`audit_campaign` object in `/audit-input.json`, and the lock's SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

I checked all records required for this layout:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace;
- the present optional `/generation-evidence/usage.json`; and
- the historical `legacy-metrics.json` and `legacy-run-input.json`.

Every required object is a real regular file or real directory. Neither the
candidate tree nor the trace tree contains a symlink or unsupported filesystem
entry. The structured trace consists of one valid JSONL file with 382 parsed
records. A historical `runtime-metrics.json` is absent, which the
`legacy-selected-stage1` rules explicitly permit.

All launcher-recorded regular-file hashes recomputed exactly. This includes the
trusted prompt, translator, canonical implementation, run/task/result records,
generation prompt/output/last/metrics/usage, and the sole trace JSONL file.
The retained-workspace digest recomputed with the pipeline's published
`sha256_tree` algorithm as
`3b1f3d508fbac7cf3d76dab301ea969394befd37ed5e6e8a9c94b974c231873f`,
matching both `generation-result.json` and `invocation.json`. The corresponding
trace-tree digest is
`d5e6eff85dcf7f6f130985df4032292744181364733f8d4b174cd9df0423c02a`,
matching `usage.json`. The two additional launcher tree fields in
`audit-input.json` use an unstated serialization and therefore are recorded
separately in the evidence rather than incorrectly compared as pipeline-tree
digests.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
their trusted mounted versions. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist. Thus there is no supplied
semantics to search for or compare, and no semantics-mode infrastructure
contradiction.

Evidence:
[provenance checker](/audit-output/evidence/provenance_check.py),
[provenance log](/audit-output/evidence/stage1-provenance.log), and
[generation output hashes](/audit-output/evidence/stage1-generation-output-hashes.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a valid integer `a`, return `True`
exactly when `a` is the cube of some integer. Its examples include positive
and negative cubes, zero, and non-cubes. The trusted canonical implementation
normalizes with `abs`, approximates a cube root using floating-point power and
rounding, then checks the rounded integer's cube.

The submitted [solution.py](/candidate/solution.py) is a different but
contract-faithful exact-integer algorithm. It normalizes negative input, starts
`n` at zero, increments until `n**3 >= abs(a)`, and returns whether equality
holds. The sign branch boundary is at `a = 0`; the loop's zero-iteration
boundary is also `a = 0`; and equality is tested on both sides of each cube.
K mathematical integers agree with Python integers for all operations used.

Running the trusted translator from the scratch copy produced
`regenerated-solution.mpy`; `cmp -s` against the submitted
[solution.mpy](/candidate/solution.mpy) exited 0. This establishes byte
identity, not merely visual similarity.

The independent differential test imports both trusted canonical `iscube` and
candidate `iscube`, and also uses an independently written integer binary-search
oracle. It covers:

- all six documented examples;
- `-2,-1,0,1,2` for the sign, zero-iteration, first-iteration, and equality
  boundaries;
- both signs of `r**3-1`, `r**3`, and `r**3+1` for roots `0..40`, `100`,
  `1000`, `10000`, and `100000`;
- every integer from `-5000` through `5000`; and
- 2,000 deterministic generated integers from `[-1000000,1000000]`.

There is no meaningful “empty” scalar integer case. All 12,156 unique inputs
agreed, with zero mismatches. These tests are finite evidence only; the
universal result comes from the K claims and the static reasoning below.

Evidence:
[differential script](/audit-output/evidence/differential_test.py),
[differential log](/audit-output/evidence/stage2-differential.log),
[trusted regeneration log](/audit-output/evidence/stage2-regenerate.log), and
[byte-identity log](/audit-output/evidence/stage2-byte-identity.log).

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the trusted inputs into
`/tmp/audit-work/rebuild`. Source hashes in scratch equal the read-only
candidate hashes. I did not copy or use `*-kompiled`, `.kprove-*`, or any other
candidate cache. The observed `kompile`, `krun`, and `kprove` version is
K 7.1.293.

Fresh builds succeeded:

- LLVM `semantic.k`, main module `MPY`, syntax module `MPY-SYNTAX`;
- Haskell `verification.k`, main/syntax module `VERIFICATION`; and
- Haskell `verification.k`, main/syntax module `GAP-VERIFICATION`.

The fresh LLVM definition concretely executed 18 sign/cube-neighbor cases, and
each K result agreed with both Python implementations. Separate ground runs for
`-8` and `-9` returned `true` and `false`, respectively. These executions cover
both `If` branches, an initially false `While`, true and false loop guards,
all three modeled arithmetic operators, both comparisons, assignment,
environment lookup, sequencing, module/function setup, invocation, and return.

Every positive claim was then run under a fresh Haskell definition. Entry
claims were selected together with their loop invariant, because selecting an
entry alone removes the circularity it depends on. Each command printed
`#Top` and exited 0:

| Claim | Fresh result |
|---|---|
| `CUBE-SPEC.cube-loop` | `#Top`, exit 0 |
| `CUBE-SPEC.nonnegative-cube` with `cube-loop` | `#Top`, exit 0 |
| `CUBE-SPEC.negative-cube` with `cube-loop` | `#Top`, exit 0 |
| `GAP-SPEC.gap-loop` | `#Top`, exit 0 |
| `GAP-SPEC.positive-noncube` with `gap-loop` | `#Top`, exit 0 |
| `GAP-SPEC.negative-noncube` with `gap-loop` | `#Top`, exit 0 |

As a cross-check, proving each complete spec module also printed `#Top` and
exited 0. An early reviewer diagnostic that selected
`nonnegative-cube` without `cube-loop` was interrupted after it began
unbounded loop unrolling; it is preserved and is not used as positive evidence.

Evidence:
[scratch source hashes](/audit-output/evidence/stage3-scratch-source-hashes.log),
[LLVM build](/audit-output/evidence/stage3-kompile-llvm.log),
[cube build](/audit-output/evidence/stage3-kompile-cube.log),
[gap build](/audit-output/evidence/stage3-kompile-gap.log),
[concrete comparison](/audit-output/evidence/stage3-concrete-compare.log),
[cube module proof](/audit-output/evidence/stage3-prove-cube-module.log), and
[gap module proof](/audit-output/evidence/stage3-prove-gap-module.log).
The per-claim logs are in `/audit-output/evidence/stage3-prove-*.log`.

## 4. Adequacy and real-program pinning

The claims in [spec.k](/candidate/spec.k) say:

| Claim | Plain-language precondition | Plain-language postcondition |
|---|---|---|
| `cube-loop` | `a=N^3`, `0<=I<=N`, and the loop starts with `n=I` | The actual loop is consumed, `a` is unchanged, and `n=N` |
| `nonnegative-cube` | Input is `N^3` for `N>=0` | The complete program returns `true` |
| `negative-cube` | Input is `-N^3` for `N>0` | The complete program returns `true` |
| `gap-loop` | `a=N^3+D`, `0<=N`, `0<D<(N+1)^3-N^3`, and `0<=I<=N+1` with `n=I` | The actual loop is consumed, `a` is unchanged, and `n=N+1` |
| `positive-noncube` | Input is `N^3+D` under the open-gap conditions | The complete program returns `false` |
| `negative-noncube` | Input is `-(N^3+D)` under the same conditions | The complete program returns `false` |

The result cell is fixed to `BoolVal(true)` or `BoolVal(false)` in every entry
claim. It is not existential, unconstrained, a tautology, or one side of an
insufficient implication. The only existential cells are the final function
map and environment, which are irrelevant after the fixed result and empty
computation have been reached.

Every precondition is satisfiable. Ground witnesses are:

- `cube-loop`: `N=2, I=1`, hence `a=8, n=1`, ending at `n=2`;
- `gap-loop`: `N=2, D=1, I=1`, hence `a=9, n=1`, ending at `n=3`;
- entry claims: inputs `8`, `-8`, `9`, and `-9` for the four partitions.

For those four entry witnesses, the claimed values are respectively `true`,
`true`, `false`, and `false`; both Python implementations agree.

The entry term starts with `iscubeProgram`, an ordinary one-step abbreviation
in [verification.k](/candidate/verification.k). To check program identity
mechanically, I parsed the submitted `solution.mpy` into a fresh initialized
configuration and separately initialized `iscubeProgram` then took its one
abbreviation step. The resulting KORE configurations are byte-identical:
both have SHA-256
`b1aa7e5b568a5f0acf8f695bed71571c1ee4e650bd2d335d37cc737ed8f5fa9f`.
This proves constructor-level identity, including the empty `else` statement
list, rather than relying on the candidate's prose.

As a separate body-sensitivity check, I changed the increment in the program
term actually executed by a fresh claim from `n+1` to `n+2`. The mutant
definition built successfully. On satisfying input `1`, it reached
`BoolVal(false)` and the expected-`true` proof failed with
`WarnStuckClaimState` and exit 1. Thus changing the body changes the theorem's
execution and invalidates the expected result.

The four entry domains cover every mathematical integer: for
`m=abs(a)`, choose the unique `N>=0` with
`N^3 <= m < (N+1)^3`. If `m=N^3`, one of the cube claims applies; otherwise
`D=m-N^3` satisfies the gap precondition. The sign selects the positive or
negative claim, with zero included in the nonnegative cube case. This is an
unbounded partition, not finitely many sizes or a bounded unrolling.

Evidence:
[ground witnesses](/audit-output/evidence/stage4-claim-witnesses.log),
[source KORE](/audit-output/evidence/source-initial.kore),
[expanded-claim KORE](/audit-output/evidence/claim-after-abbrev.kore),
[KORE comparison](/audit-output/evidence/stage4-pinning-cmp.log),
[body mutant](/audit-output/evidence/body-mutant-verification.k), and
[body-mutant failure](/audit-output/evidence/stage4-prove-body-mutant.log).

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

[semantic.k](/candidate/semantic.k) declares:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: the generated empty-separator list of `Stmt`;
- `Params`: one string parameter;
- `Expr`: `Int`, `Name`, strict unary operation, strict two-argument binary
  operation, and a comparison with strict left operand;
- `CmpOp`: one string operator and one expression;
- `Stmt`: `FuncDef`, `If`, `Assign`, `While`, and `Return`;
- values `IntVal` and `BoolVal`, with `Value` declared a `KResult` and embedded
  into `Expr`;
- `Function`: `function(String,Stmts)`; and
- continuation `KItem`s `exec`, `invoke`, `assignTo`, `ifKont`, `whileKont`,
  `compareKont`, and `returnKont`.

Its configuration has exactly the state used by this program: `<k>`, a
function map `<funs>`, variable map `<env>`, and `<result>`. There is no unused
heap, allocation counter, I/O cell, exception cell, or call stack.

[verification.k](/candidate/verification.k) adds the `iscubeProgram` syntax
constant, the `cube(Int)` function with `[function,total]`, and no opaque
symbol. There are no local priority rules, `functional` declarations, macros,
or other helper files. The only local simplification rules are the two guarded
gap lemmas. [spec.k](/candidate/spec.k) contains exactly the six claims listed
in stage 4.

### Complete operational rule inventory

The 23 ordinary semantic rules were checked individually:

1. `Module(STMTS) => exec(STMTS)` enters module execution.
2. `exec(.Stmts) => .K` ends an empty statement list.
3. `exec(S REST) => S ~> exec(REST)` preserves statement order.
4. `FuncDef` installs the sole function in an initially empty function map.
5. `invoke(IntVal(A))` selects the `"iscube"` binding, binds its actual
   parameter in an empty environment, and executes the stored body.
6. `Int(I) => IntVal(I)` preserves integer literals.
7. `Name(X)` reads the corresponding environment value.
8. unary `"-"` computes exact integer negation.
9. binary `"+"` computes exact integer addition.
10. binary `"*"` computes exact integer multiplication.
11. `Compare` evaluates its right operand after retaining the evaluated left
    integer and operator.
12. comparison `"<"` produces the matching Boolean.
13. comparison `"=="` produces the matching Boolean.
14. `Assign(Name(X),E)` evaluates `E` before storing.
15. `assignTo` updates exactly key `X` in `<env>`.
16. `If` evaluates its condition before selecting a branch.
17. a true condition executes only the then-list.
18. a false condition executes only the else-list.
19. `While` evaluates its condition.
20. a true loop condition executes the body and then repeats the same loop.
21. a false loop condition consumes the loop.
22. `Return(E)` evaluates `E` before returning.
23. `returnKont` discards the remaining current-function computation and
    writes the value into an initially empty result cell.

The `strict` attributes generate standard heating/cooling rules for unary
operand 2, binary operands 2 and 3, and comparison operand 1. `strict(2,3)` is
not a left-to-right `seqstrict` declaration despite the nearby comment.
However, every expression occurring in this submitted body is pure: its
subexpressions only read `<env>` and perform total integer operations. The
possible order does not affect value, control, or any observable cell. The
comparison rule then evaluates its right operand after the left value, also
without a side effect.

The function-map and empty-environment restrictions are intentionally minimal:
the submitted module has one single-argument function and the entry
configuration makes exactly one top-level invocation. All names (`a` and `n`)
are bound before use. The broad `_REST` in the return rule represents
unexecuted statements in this function; the language has no nested call
construct or caller frame that it could incorrectly discard. The entry
configuration has no post-invocation continuation. Accordingly the rule
preserves the complete control behavior of every reachable submitted-program
state.

Every constructor in `solution.mpy` maps to the inventory above:
`Module`, `FuncDef`, `Params`, statement-list sequencing, `If`, both `Compare`
operators, `Name`, `Int`, `Assign`, unary `-`, `While`, binary `*` and `+`,
and `Return`. No used construct is handled by fabrication, an oracle, or a
fallback rule.

### Complete proof-extension inventory

1. `iscubeProgram => Module(...)` is a definitional constructor
   abbreviation. It reads or writes no cell, introduces no value, and does not
   skip execution. Its complete expanded term is mechanically identical to the
   trusted retransliteration, as shown in stage 4. All four entry claims depend
   on it.
2. `cube(I) => I*I*I` is a total definitional summary over all K integers. Its
   unconditional equation covers the entire declared domain, has no overlap,
   and terminates in one rewrite. It affects input expressions, invariant
   values, and postcondition arithmetic, but does not replace a program
   operation.
3. Gap simplifier 1 concludes `I < N+1` under the complete guard printed at
   `verification.k:36`. If its conclusion were false, the given
   `I<=N+1` would imply `I=N+1`; then
   `D<(N+1)^3-N^3` would imply `N^3+D<I^3`, contradicting the final guard
   `I^3<N^3+D`. The rule is valid throughout its guard.
4. Gap simplifier 2 concludes `I == N+1` under the complete guard printed at
   `verification.k:46`. If the conclusion were false, integral
   `I<=N+1` would give `I<=N`. Since both are nonnegative,
   `I^3<=N^3`; positive `D` then contradicts
   `I^3>=N^3+D`. The rule is valid throughout its guard.

The two simplifiers have different left-hand predicates, do not overlap as
equations for one symbol, do not alter any configuration cell, do not
summarize the loop, and introduce no fresh result-bearing value. Their only
dependents are `gap-loop` and the two non-cube entry claims. A finite supporting
check enumerated 706,800 satisfying instances of the first guard and 29,760 of
the second for `N=0..30`, with zero false conclusions. The mathematical
derivations above, not that finite check, justify universality.

The loop claims match the exact `While` constructor and body in the program.
Their `<env>` maps are exact (`a` and `n` only), and their framed `<k>` suffix
is safe because the loop body has no abrupt control or state beyond those two
variables. Each circular step executes the fixed semantic rules before
returning to the same loop head with `n+1`; neither claim is an operational
rewrite in `verification.k`.

I found no unsound rule and therefore make no unsoundness allegation requiring
a false-conclusion witness. The exhaustive source inventories are preserved in
[semantic source log](/audit-output/evidence/stage5-semantic-source.log),
[verification source log](/audit-output/evidence/stage5-verification-source.log),
and [spec source log](/audit-output/evidence/stage5-spec-source.log).
The guard test is
[stage5-rule-guard-check.log](/audit-output/evidence/stage5-rule-guard-check.log).

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation. The fresh
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) invokes the unchanged
submitted program on input `2` but requires `BoolVal(true)`. Input `2`
satisfies the original positive-noncube domain with `N=1, D=1`, and its actual
result is demonstrably `false`.

`kprove --dry-run` parsed and built the mutation successfully (exit 0). The
real proof then exited 1 with `WarnStuckClaimState`; its residual has empty
`<k>`, `a=2`, `n=2`, and
`<result> BoolVal(false) ~> .K </result>`, which fails to unify with the
required `true`. This is the expected unmet result obligation, not a parser
error, missing import, timeout, or unrelated crash.

Evidence:
[dry-run log](/audit-output/evidence/stage6-vacuity-dry-run.log) and
[failed-proof log](/audit-output/evidence/stage6-vacuity-proof.log).

## 7. Proven versus assumed accounting

Under the reviewed MPY definition, the successful reachability claims establish
partial correctness for four unbounded input partitions: all nonnegative
cubes, all negative cubes, all positive integers strictly between consecutive
nonnegative cubes, and their negatives. Cubes return `true`; open-gap values
return `false`. The helper claims establish the exact loop exit counter,
`N` or `N+1`, while preserving normalized `a`. The elementary integer
partition argument in stage 4 shows that these claims cover the prompt's full
integer domain.

The trust ledger is:

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and standard `INT`, `BOOL`, `MAP`, `K-EQUAL`, and `MAP-SYMBOLIC` modules | Parsing, arithmetic, maps, simplification, concrete execution, and reachability | Normal low-level toolchain trust; version recorded and fresh builds used |
| Trusted `py2mpy.py` | Python-AST-to-constructor bridge | Acceptable: trusted mount matches candidate byte-for-byte and fresh output matches submitted `solution.mpy` byte-for-byte |
| Candidate-generated `semantic.k` versus Python behavior | Meaning of every executed constructor and state transition | Acceptable after exhaustive used-construct review plus fresh boundary execution; there is no hidden or supplied reference semantics in this mode |
| `cube` equation | Inputs and invariant arithmetic | Acceptable truthful total definition, not opaque |
| Two gap simplification lemmas | Symbolic loop branch closure | Acceptable derived mathematics under complete guards; no state/control effect and no false guard instance found |
| Integer cube-gap partition | Connection from the four formal families to “all integers” | Acceptable elementary well-ordering/monotonicity argument; not a finite-size restriction |
| Differential tests | Python/canonical/semantic bridge on tested inputs | Supporting finite evidence only, never used as a universal proof |

There is no opaque result symbol, external oracle, empirical rule, fabricated
result, or task-answer semantic rule. The proof does not establish a general
Python semantics, behavior for invalid non-integer inputs, or an independent
termination-complexity theorem; those are outside the partial-correctness
contract. Manual duplication of the constructor tree in `verification.k` is an
artifact-maintenance risk, but the immutable candidate is mechanically pinned
and body-sensitive, so it is not a proof defect.

Kit Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(trust/evidence auditability) all pass. Fresh reconstruction, program pinning,
static rule validity, full unbounded domain coverage, and non-vacuity support a
legitimate proof with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
