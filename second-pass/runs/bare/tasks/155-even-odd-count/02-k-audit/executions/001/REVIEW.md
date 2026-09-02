# Independent adversarial audit: 155-even-odd-count

This audit treated every candidate artifact, cache, log, trace, and prior
`#Top` as untrusted. All executable artifacts were copied from source into
`/tmp/audit-work/rebuild`; the candidate's `semantic-kompiled/` and
`definition-kompiled/` directories were not used.

The reconstructed K proof is a legitimate, result-constraining
partial-correctness proof of the submitted program under the generated
semantics. It is not a proof that the program meets the full trusted task
intent: on the valid input `0`, the submitted program and its K specification
return `(0, 0)`, while the trusted canonical implementation returns `(1, 0)`.
There is also a non-reachable over-breadth in the generated `//` semantics.
Those limitations warrant `CONCERNS / LEGIT`, rather than `PASS` or `FAIL`.

## 1. Input and provenance integrity

### Trusted semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. The required check
`test ! -e /reference/reference-semantics` exited 0, so there is no contradictory
trusted semantics mount and no infrastructure breach. The trusted inputs
`/reference/prompt.py`, `/reference/canonical.py`, and `/reference/py2mpy.py`
are regular files.

The candidate copies of `prompt.py` and `py2mpy.py` are byte-identical to the
trusted files:

- prompt SHA-256:
  `8e85f42e3477e802ebd61afb54ef97ef1dd36e242780e51d22074ec019a3657f`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Evidence: `evidence/provenance/provenance_checks.sh` and
`evidence/provenance/provenance_checks.log`.

### Required and extra artifacts

All required generation/provenance artifacts were present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. A regular structured trace was
present at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-52-05-019f89e2-1d58-7402-a397-37019fa95ca8.jsonl`.
No symlink was found anywhere under `/candidate`. No required artifact was
missing, changed, mistyped, or symlinked.

The additional `definition.k` is a legitimate build helper. The extra
`semantic-kompiled/`, `definition-kompiled/`, and `__pycache__/` entries are
candidate-produced build/cache output. They were recorded, treated as
untrusted, and ignored during reconstruction; their presence is not a source
integrity failure.

The untrusted provenance files claim a bare/generated-semantics run, exit 0,
and a final `KPROVE_PASSED`. The log also records earlier parser and stuck-claim
failures before the claimed final `#Top`. None of these claims was used as proof
evidence. Their hashes and bounded relevant excerpts are in
`evidence/provenance/untrusted_generation_claims.log`.

Stage result: integrity passed; no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

The prompt requires `even_odd_count(num)` for an integer `num`, returning
`(number of even decimal digits, number of odd decimal digits)`. The trusted
canonical implementation iterates over `str(abs(num))`. Therefore:

- sign is not a digit;
- every nonzero absolute integer contributes all of its decimal digits;
- `0` has one digit, which is even, so the canonical result is `(1, 0)`.

The submitted `solution.py` normalizes a negative input, initializes both
counters, repeatedly classifies `num % 2`, and divides `num` by 10. This is
equivalent for every nonzero integer. Its `while num > 0` executes zero times
for `num == 0`, producing `(0, 0)` instead of `(1, 0)`.

### Translation fidelity

The trusted command

`python3 /reference/py2mpy.py /tmp/audit-work/rebuild/candidate-src/solution.py`

regenerated an artifact byte-identical to `/candidate/solution.mpy`; both have
SHA-256
`27f1ddc4e5c550a671e1ee9e493b5196c65148fcd2f5e3aafe4632e587494b4f`.
Thus the submitted MPY term is the faithful trusted translation of the
submitted Python source.

### Independent differential test

`evidence/differential/differential_test.py` imports the trusted canonical and
submitted entry points from separate explicit paths. It covers:

- both documented examples;
- the empty-loop/sign/parity/decimal boundaries;
- every integer in `[-5000, 5000]`;
- 1,000 deterministic random integers in `[-10**30, 10**30]`.

The command exited 1 because it intentionally treats any mismatch as failure.
Across 11,003 unique inputs it found exactly one mismatch:

`input=0 canonical=(1, 0) generated=(0, 0)`.

Evidence: `evidence/differential/differential_test.log`.

Stage result: source-to-MPY fidelity passed; implementation-to-contract
fidelity has a concrete valid-domain discrepancy at zero.

## 3. Clean proof reconstruction

### Fresh sources and tools

The scratch copies of `semantic.k`, `verification.k`, `spec.k`, and
`definition.k` were byte-identical to the candidate sources; see
`evidence/reconstruction/source-copy-identity.log` and
`source-copy-hashes.log`. K caches and definitions were built under new names
in scratch.

The tools were K `v7.1.293` and Python `3.10.12`
(`evidence/reconstruction/tool_versions.log`).

### Fresh builds

Both builds completed with exit 0:

| Purpose | Source and output | Evidence |
|---|---|---|
| Concrete generated semantics | `semantic.k` to `semantic-fresh-kompiled` using the Haskell backend | `evidence/reconstruction/kompile-semantic.log` |
| Proof definition | `definition.k` to `definition-fresh-kompiled` using the Haskell backend | `evidence/reconstruction/kompile-definition.log` |

### Concrete generated-semantics execution

`evidence/concrete/concrete_compare.py` invoked the fresh definition on eleven
normal and boundary inputs: `-12, 123, 0, -1, 1, -2, 2, -10, 10, 101, 222`.
This exercises the negative-normalization branch, empty loop, positive loop,
even and odd branches, and multiple iterations. Every K result matched the
submitted Python implementation; the script exited 0. The recorded zero case
also independently shows the canonical discrepancy:

`k=(0, 0) submitted_python=(0, 0) canonical_python=(1, 0)`.

Evidence: `evidence/concrete/concrete_compare.log`.

### Every positive claim

The original, unchanged `SPEC` module closed with `#Top`, exit 0
(`evidence/reconstruction/kprove-all.log`).

For independent claim selection, the reviewer-created `spec-audit.k` changes
only the module name and adds labels; its exact diff is
`evidence/reconstruction/spec-audit.diff`.

- `SPEC-AUDIT.loop-invariant` alone printed `#Top` and exited 0
  (`kprove-loop-invariant.log`).
- The end-to-end claim depends on the loop circularity. Selecting the
  end-to-end claim while filtering the loop claim out reached the 120-second
  diagnostic bound; this is dependency evidence, not a candidate failure
  (`kprove-end-to-end.log`). The loop claim was first proved independently as
  above. A second run marked that exact already-proved loop claim trusted, so
  the only untrusted target left was the end-to-end claim; it printed `#Top`
  and exited 0 (`kprove-end-with-proven-loop-final.log`).

Two earlier reviewer attempts to encode the trusted attribute directly in a
temporary harness produced parser errors and are retained as bounded diagnostic
logs. They are not proof or non-vacuity evidence. The successful command used
K's documented `--trusted` option.

Stage result: clean reconstruction passed. Both targets close, including an
independent sequential check of the auxiliary loop claim followed by the entry
claim.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim at `/candidate/spec.k:8` has precondition `N >= 0`, exact
three-variable environment values `num=N`, `even=E`, `odd=O`, arbitrary input
cell, and `noResult`. It says that executing the real loop followed by the real
return consumes all remaining decimal digits, leaves `num=0`, updates the
counters to `evenFrom(E,N)` and `oddFrom(O,N)`, clears computation, and returns
that exact pair.

The entry claim at `/candidate/spec.k:25` has no additional `requires` clause.
For every mathematical K integer `N`, from empty environment and `noResult`, it
says the complete program clears computation, ends with `num=0`, ends with the
two recursively specified counters, and returns exactly `expected(N)`. This is
an exact cell rewrite, not a free result variable, tautology, or one-way
implication.

### Program identity

The entry claim uses `solutionProgram()` rather than parsing a filename during
the proof. This is a definitional alias, not an opaque oracle:

- `solutionProgram` expands to the exact `Module(FuncDef(...))`;
- `functionBody` expands to the exact translated statement sequence;
- `numNegative`, `numPositive`, `digitIsEven`, `digitBody`,
  `returnedCounts`, and `returnCounts` expand to the exact subtrees in
  `solution.mpy`.

Comparing `/candidate/verification.k:47-72` with
`/candidate/solution.mpy:1-13` finds no substituted statement, operator,
constant, binding, or continuation. The trusted translator byte-identity check
then pins that term to the submitted `solution.py`.

As an additional body-sensitivity check, the reviewer changed the aliased
`even = 0` statement to `even = 1` in a separate scratch definition. The
mutation built successfully, but the unchanged end claim failed with the
residual `evenFrom(0,N) = evenFrom(1,N)`. Evidence:
`evidence/adequacy/body-mutation.diff`,
`kompile-body-mutation.log`, and `kprove-body-mutation.log`.

### Satisfying witnesses and ground substitutions

`evidence/adequacy/spec-ground.k` exhibits:

- loop state `N=12, E=0, O=0`, satisfying `N >= 0`, with exact result `(1,1)`;
- entry state `N=-12`, satisfying the unconditional entry claim, with exact
  result `(1,1)`;
- entry state `N=0`, also satisfying it, with exact result `(0,0)`.

All three ground claims printed `#Top`, exit 0
(`evidence/adequacy/kprove-ground.log`). For `-12`, both Python
implementations return `(1,1)`. For `0`, the submitted Python returns the
claimed `(0,0)`, while the canonical returns `(1,0)`. Thus the formal claim
faithfully constrains the real program but its zero postcondition is not the
trusted task result.

Stage result: real-program pinning and result constraint passed; intent
adequacy is limited at zero.

## 5. Rule-by-rule static soundness review

Full numbered sources are preserved in
`evidence/static/numbered_sources.log`.

### Local declaration inventory

There are no imported candidate helper K files beyond `semantic.k`,
`verification.k`, `spec.k`, and the import-only `definition.k`.

| File/lines | Exhaustive local declarations | Assessment |
|---|---|---|
| `semantic.k:5-26` | `Pgm: Module`; `Stmts` list; `Stmt: FuncDef, Assign, AugAssign, If, While, Return`; `Params`; `Strings`; `Expr: Int, Name, UnaryOp, BinOp, Compare, TupleExpr`; `Exprs`; `CmpOp`; `CmpOps` | Covers every constructor in the submitted MPY term. Some list/operator generality is intentionally partial outside the term. |
| `semantic.k:36-51` | values `intVal`, `boolVal`, `pairVal`, `noResult`; functions `eval`, `envGet`, `negVal`, `addVal`, `modVal`, `divVal`, `ltVal`, `gtVal`, `eqVal`; K items `exec`, `loop` | No function is declared `total`; unsupported/mistyped values therefore stop rather than being fabricated. |
| `semantic.k:53-59` | cells `<k>`, `<env>`, `<input>`, `<result>` | Sufficient for this pure, single-entry integer function. No heap, allocation, I/O, exception, or call-stack construct occurs in the submitted program. |
| `verification.k:7-12` | total functions `absNum`, `evenDigits`, `oddDigits`, `evenFrom`, `oddFrom`, `expected` | Guard coverage, disjointness, and descent are checked below. |
| `verification.k:38-45` | total nullary AST aliases `numPositive`, `numNegative`, `digitIsEven`, `returnedCounts`, `digitBody`, `functionBody`, `returnCounts`, `solutionProgram` | Each has one unconditional equation and expands to an exact submitted subtree. |

There are no local opaque or fresh symbols, priority rules, macros, aliases in
the K-attribute sense, `functional` declarations, or simplification rules.
There are no ordinary rules in `spec.k`; it contains exactly the two
reachability claims reviewed in stage 4. All 14 local `total` declarations are
the six mathematical helpers and eight nullary AST aliases listed above.

### Operational semantics: all 29 rules

| ID and source | Rule | Static assessment |
|---|---|---|
| S1 `semantic.k:61` | `envGet` | Deterministic Map lookup. All actual reads are of bound `num`, `even`, or `odd`. Missing lookup remains stuck. |
| S2 `:63` | `eval(Int)` | Exact integer-literal embedding. |
| S3 `:64` | `eval(Name)` | Delegates to S1; correct for the exact local environment. |
| S4 `:65` | unary `-` | Pure operand evaluation followed by S12; exact on used integer values. |
| S5 `:66` | binary `+` | Pure two-operand evaluation followed by S13. This AST form is not used by the submitted term. |
| S6 `:67` | binary `%` | Pure evaluation followed by S14. The submitted use has nonnegative left operand and divisor 2. |
| S7 `:68` | binary `//` | Pure evaluation followed by S15. The submitted use has nonnegative left operand and divisor 10. |
| S8 `:69` | comparison `<` | Exact single-comparison evaluation for the initial sign test. |
| S9 `:70` | comparison `>` | Exact single-comparison evaluation for the loop guard. |
| S10 `:71` | comparison `==` | Exact single-comparison evaluation for parity. |
| S11 `:72` | two-element tuple | Evaluates the two pure name operands and constructs the returned pair. |
| S12 `:74` | `negVal` | Mathematical integer negation, matching Python arbitrary-precision negation. |
| S13 `:75` | `addVal` | Mathematical integer addition, matching counter increments. |
| S14 `:76` | `modVal` | Uses K `%Int`; correct on the reachable nonnegative dividend/nonzero divisor. |
| S15 `:77` | `divVal` | Uses K `/Int`; correct on the reachable nonnegative dividend/divisor 10, but over-broad for negative dividends as detailed below. |
| S16 `:78` | `ltVal` | Exact mathematical integer less-than. |
| S17 `:79` | `gtVal` | Exact mathematical integer greater-than. |
| S18 `:80` | `eqVal` | Exact mathematical integer equality. |
| S19 `:82-86` | module/function entry | Matches the exact function and parameter, binds input `N`, and executes captured `BODY`. Preinitializing counters is redundant because the actual first reads follow unconditional zero assignments; it would be too broad for a different body. |
| S20 `:88` | empty `exec` | Correctly consumes an empty statement list. |
| S21 `:89` | nonempty `exec` | Enforces left-to-right statement sequencing with the rest as continuation. |
| S22 `:91-92` | assignment | Evaluates the pure RHS in the old environment, then updates the named local. |
| S23 `:94-95` | `+=` | Reads the old local, evaluates the pure RHS, adds, and updates. It is exact for the two counter increments. |
| S24 `:97-99` | true `If` | Guarded by exact `boolVal(true)`; executes only the then list. |
| S25 `:100-102` | false `If` | Guarded by exact `boolVal(false)`; disjoint from S24 and executes only the else list. |
| S26 `:104` | `While` entry | Moves to a stable `loop` head used by the circularity. |
| S27 `:105-107` | true loop | Evaluates the guard before every iteration, sequences the body, then returns to the same loop head. |
| S28 `:108-110` | false loop | Disjoint from S27 and exits without executing the body. |
| S29 `:112-114` | return | Evaluates the pure returned tuple in the current environment, sets the sole result, and discards the remaining function-body continuation, matching abrupt return in this one-frame harness. |

The `eval` rules have disjoint constructor/operator heads. S24/S25 and S27/S28
have disjoint Boolean guards. Assignment uses the old map on the RHS. Sequence,
loop reconstruction, and return give the correct control order. The program has
no side-effecting expressions, allocation, calls, exceptions, or external state
whose order or cells could have been lost.

S15 is deliberately classified as a narrower, non-target over-breadth rather
than silently accepted. `evidence/static/negative-div.mpy` and
`negative-division.log` give a concrete witness with intended integer input
`-1`: the broad generated rule evaluates `-1 /Int 10` to `0`, while Python
`-1 // 10` is `-1`. The actual submitted program cannot reach that matched
operand: its first `If` negates every negative input, the other branch already
has `num >= 0`, and the loop preserves nonnegativity. The loop claim likewise
requires `N >= 0`. Therefore this false broader-language behavior cannot enable
a false conclusion in either audited target claim. It remains a reuse
limitation and supports `CONCERNS`, not a material soundness failure of this
program proof. Division/modulo by zero and general exception behavior are also
unmodeled, but both submitted divisors are fixed nonzero literals.

S19's counter preinitialization has the same target-versus-reuse distinction.
For the submitted body, the next relevant statements overwrite both entries
with zero before either is read, so no input produces different submitted
behavior. A different body could observe a fabricated binding; such bodies are
outside this individually generated program semantics.

### Verification functions: all 19 equations

| ID and source | Equation | Static assessment |
|---|---|---|
| V1 `verification.k:14` | negative `absNum` | Correct for `N < 0`. |
| V2 `:15` | nonnegative `absNum` | Correct, disjoint from V1, and together exhaustive on `Int`. |
| V3 `:17` | base `evenFrom(E,N)=E` | Correct for `N <= 0`. Reachable uses end at zero. |
| V4 `:18-19` | even-digit `evenFrom` step | Correctly increments and divides when `N>0` and even. |
| V5 `:20-21` | odd-digit `evenFrom` step | Correctly preserves the even accumulator when `N>0` and odd. |
| V6 `:23` | base `oddFrom(O,N)=O` | Correct for `N <= 0`. |
| V7 `:24-25` | even-digit `oddFrom` step | Correctly preserves the odd accumulator. |
| V8 `:26-27` | odd-digit `oddFrom` step | Correctly increments it. |
| V9 `:29` | `evenDigits` | Defines the zero-initialized even accumulator. |
| V10 `:30` | `oddDigits` | Defines the zero-initialized odd accumulator. |
| V11 `:32-34` | `expected` | Constructs the exact pair from the two counts of `absNum(N)`. It intentionally inherits the model's zero behavior. |
| V12 `:47` | `numPositive` | Exact loop-guard subtree. |
| V13 `:48` | `numNegative` | Exact sign-test subtree. |
| V14 `:49-51` | `digitIsEven` | Exact modulo/equality subtree. |
| V15 `:52` | `returnedCounts` | Exact returned tuple subtree. |
| V16 `:54-58` | `digitBody` | Exact parity branch followed by decimal division. |
| V17 `:60` | `returnCounts` | Exact one-statement return continuation used by the loop claim. |
| V18 `:62-69` | `functionBody` | Exact complete translated body, in order. |
| V19 `:71-72` | `solutionProgram` | Exact module/function wrapper. |

For `evenFrom` and `oddFrom`, the base guard `N <= 0` is disjoint from both
recursive guards. On `N > 0`, `N %Int 2 == 0` and `N %Int 2 =/= 0` are
disjoint and exhaustive. Division by 10 produces a smaller nonnegative integer,
so recursion descends. `E` and `O` need no restriction. The remaining total
functions each have one unconditional equation. Thus all local totality,
coverage, overlap, and descent obligations are met.

V11 is a truthful definition of the submitted algorithm's mathematical
summary, not an oracle replacing execution. The operational program still
executes; the loop claim connects its exact loop/body/environment to V3-V8.
There is no fresh value shared circularly between an execution bridge and the
postcondition.

### Used-construct coverage

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax `semantic.k:5,8,15-16`; S19 |
| statement lists | `:7`; S20-S21 |
| `If` and empty else | `:11`; S24-S25 and `exec(.Stmts)` |
| `Assign`, `AugAssign` | `:9-10`; S22-S23 |
| `While` | `:12`; S26-S28 |
| `Return` | `:13`; S29 |
| `Int`, `Name`, unary `-` | `:18-20`; S2-S4, S12, S1/S3 |
| `%`, `//` | `:21`; S6-S7, S14-S15 |
| `<`, `>`, `==` | `:22,25-26`; S8-S10, S16-S18 |
| two-element tuple | `:23-24`; S11 |

Stage result: the semantics and proof equations are sound on every reachable
state of the submitted program. The negative-floor-division witness and
redundant entry initialization limit reuse but do not make either target theorem
false.

## 6. Fresh non-vacuity test

The reviewer-created `evidence/nonvacuity/spec-vacuity.k` preserves the loop
claim and changes only the entry result obligation by requiring the even count
to be `evenDigits(absNum(N)) + 1`. The exact mutation is in
`spec-vacuity.diff`.

This mutation is demonstrably false for the satisfying entry input `N=1`: the
program returns `(0,1)`, while the mutation requires `(1,1)`.

- `kprove ... --dry-run` exited 0, confirming the mutated artifact parsed and
  built (`kprove-vacuity-dry-run.log`).
- The real proof run exited 1 with `WarnStuckClaimState`, after execution
  reached `.K`, on the expected unmet equality
  `evenFrom(0,N) +Int 1 = evenFrom(0,N)`
  (`kprove-vacuity.log`).

This was not a parser error, timeout, unrelated crash, or unreachable mutation.
Stage result: non-vacuity passed.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Conditional on the audited generated semantics and K's trusted built-ins, for
every mathematical integer input, if the submitted translated program
terminates then:

- it executes the exact submitted body;
- it finishes with `num=0`;
- its counters equal the accumulator functions in `verification.k`;
- its returned pair is exactly those two counters.

The generalized loop circularity establishes the corresponding statement for
any `N >= 0` and arbitrary integer accumulators `E,O`.

The proof does not establish the trusted natural-language result for `0`, and
as a partial-correctness proof it is not a separate termination theorem.

### Trust ledger

| Boundary | Dependents and status |
|---|---|
| K parser/compiler, Haskell backend, reachability prover, and imported `INT`, `BOOL`, `MAP`, `K-EQUAL`, and list machinery | Trusted low-level proof infrastructure. All formal claims depend on it. This is an ordinary acceptable trust boundary. |
| Trusted `/reference/py2mpy.py` | External syntactic bridge from `solution.py` to `solution.mpy`. Byte identity was checked; it does not supply the correctness result. Acceptable. |
| Module-entry harness S19 | Supplies function invocation/input binding outside the translated body. It matches the exact function/parameter and executes captured `BODY`; redundant counter bindings cannot affect this body. Acceptable for this single-entry program, not reusable Python-call semantics. |
| Atomic expression primitives S1-S18 | Program operations are pure and all reachable values/types/divisors are covered. Negative `//` outside the reachable operand invariant is empirically false to Python and explicitly excluded from the theorem bridge. Concerning but not theorem-invalidating. |
| Abrupt return S29 | Trusted as the single-frame control model; exact for the submitted return and no observable continuation/state is lost. Acceptable within scope. |
| V1-V11 mathematical summaries | Not opaque: guarded, exhaustive equations fix every result-bearing value, and the loop execution claim connects them to the body. Formally used and statically justified. |
| V12-V19 AST aliases | Not opaque: each has one exact constructor equation. Static source comparison and trusted translation pin them to the real MPY term; the body mutation confirms proof sensitivity. Acceptable, though the filename-to-alias equality is an audited source fact rather than a separate K theorem. |
| Loop circularity | Machine-proved independently, then used as the end claim's auxiliary. Acceptable. |
| Concrete K-versus-submitted-Python bridge | Eleven branch/boundary cases, zero mismatches. Finite empirical support only; it does not replace the K proof or universal semantic audit. |
| Submitted-versus-canonical bridge | 11,003 finite cases plus source reasoning. It exposes, rather than resolves, the zero mismatch. The natural-language intent bridge therefore fails at a valid input. |

There are no candidate opaque symbols, unconstrained result variables, fresh
oracles, proof-local simplification axioms, priority overrides, or empirical
facts used as a substitute for reachability proof.

### Gate and decision summary

- Real-program soundness: passed. The fresh proofs close, exact execution is
  pinned, body and postcondition mutations are rejected, and no reachable rule
  enables a false target conclusion.
- Intent adequacy: limited. The formal theorem truthfully proves `(0,0)` for
  zero, while the trusted contract/canonical requires `(1,0)`.
- Trust/evidence auditability: passed with the explicitly scoped generated
  semantics boundary. The negative-division over-breadth is recorded and
  excluded by a proved/reviewed reachable-state invariant.

The proof is therefore legitimate for the real generated program, but the
candidate implementation and its postcondition do not fully meet the trusted
task intent. That is a material concern without making the reconstructed
program theorem false.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
