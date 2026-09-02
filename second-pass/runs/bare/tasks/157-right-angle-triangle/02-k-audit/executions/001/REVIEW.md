# Independent adversarial review: 157-right-angle-triangle

Assessment: the candidate contains a legitimate, result-constraining K proof of
the submitted generated program. The proof is not vacuous and does not replace
program execution with an oracle. I assign concerns, rather than an unqualified
pass, because the prompt never explicitly states a numeric domain and the
candidate adds positivity checks that disagree with the trusted canonical
implementation on zero and signed Pythagorean triples. On the ordinary
geometric domain of positive side lengths, the implementations agree.

All candidate prose, traces, caches, and prior `#Top` output were treated only
as untrusted claims. All executable artifacts were copied from source and
rebuilt below `/tmp/audit-work`; candidate-provided kompiled definitions were
not used.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount is consistent
with that mode: `/reference/reference-semantics` is absent as both a normal
path and a symlink. There is therefore no infrastructure breach and no hidden
reference semantics was sought or used.

The candidate prompt and translator are regular files and are byte-identical
to the trusted mounts:

| Artifact pair | SHA-256 | `cmp` |
|---|---|---|
| candidate/trusted `prompt.py` | `badc999ecbcb5e6dd1dbb3d1c1b89f9b624e434dd4afebf241d035353b2b0a79` | exit 0 |
| candidate/trusted `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

The required source artifacts `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are present as regular files. The
provenance files `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the JSONL generation trace are also present as regular
files. No symlink exists anywhere under `/candidate`. No required artifact is
missing, changed, mistyped, or symlinked.

Additional candidate artifacts are `run-3-4-5.mpy`, `__pycache__/`, and the
candidate-built `semantic-kompiled/` and `verification-kompiled/` directories.
The first is an optional concrete witness. The latter three are generated
cache/build output and were explicitly excluded from reconstruction.

The untrusted generation records claim that a combined `kprove` run printed
`#Top`. The structured trace contains 107 valid JSON records with no parse
errors. Those claims were not credited until independently reconstructed.

Evidence:

- [stage1-integrity.log](/audit-output/evidence/stage1-integrity.log) records
  paths, types, hashes, comparisons, required-file checks, and the fresh tool
  versions. K is `v7.1.293`.
- [stage1-untrusted-claims.log](/audit-output/evidence/stage1-untrusted-claims.log)
  records the candidate's provenance claims and bounded prior output.
- [inspect_generation_trace.py](/audit-output/evidence/inspect_generation_trace.py)
  and [stage1-trace-summary.log](/audit-output/evidence/stage1-trace-summary.log)
  parse and summarize every trace record without executing trace content.
- [stage1-source-copy.log](/audit-output/evidence/stage1-source-copy.log)
  records the exact source-only scratch copy.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for a Boolean indicating whether three side lengths
form a right-angled triangle. The trusted canonical implementation returns
true exactly when one of

`a² = b² + c²`, `b² = a² + c²`, or `c² = a² + b²`

holds. It does not explicitly test positivity. The candidate computes the same
three disjuncts but additionally requires `a > 0`, `b > 0`, and `c > 0`.
Positivity is mathematically appropriate for “lengths,” but it is an additional
domain interpretation not stated as a Python precondition.

### Translation identity

Running the trusted translator on the copied candidate `solution.py` produced
a file byte-identical to submitted `solution.mpy`. Both have SHA-256
`d5ca368d0cd54dd51a7a7b8ea8a62b4ce92b31978b8484435101265b40c7301a`.
The exact command and exit 0 are in
[stage2-translation.log](/audit-output/evidence/stage2-translation.log).

### Independent differential

[stage2_differential.py](/audit-output/evidence/stage2_differential.py) imports
the trusted canonical entry point and candidate entry point from their exact
paths. Its independent cases are recorded in
[stage2-differential-inputs.json](/audit-output/evidence/stage2-differential-inputs.json).
The run covered:

- both documented examples;
- all three Pythagorean orientations;
- zero, negative, near-equality, large, and floating-point boundaries;
- empty/incorrect arities;
- every integer triple in `[-12,12]^3`;
- every positive triple in `[1,12]^3`; and
- 5,000 deterministic random triples in `[-1000,1000]^3`.

Results in [stage2-differential.log](/audit-output/evidence/stage2-differential.log):

| Scope | Cases | Mismatches |
|---|---:|---:|
| Prompt examples | 2 | 0 |
| Branch/boundary cases | 18 | 8 |
| Empty/arity cases | 4 | 0 |
| Exhaustive `[-12,12]^3` | 15,625 | 229 |
| Exhaustive positive `[1,12]^3` | 1,728 | 0 |
| Seeded broad sample | 5,000 | 0 |

The broad-domain mismatches are not random false positives. For example,
canonical returns true and candidate returns false for `(0,0,0)`,
`(-3,-4,-5)`, and signed variants of `(3,4,5)`. The random sample happened not
to contain a signed Pythagorean equality, while the exhaustive and targeted
sets did. No result divergence was found on the positive-length domain.

Judgment: this is not a substituted or incorrect algorithm for positive side
lengths. It is a documented intent-domain limitation relative to the trusted
canonical function, and it is the reason for `CONCERNS`.

## 3. Clean proof reconstruction

Only `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
and the concrete source witness were copied to scratch. No candidate kompiled
file or cache was copied.

Fresh Haskell-backend builds succeeded:

| Definition | Exact-command log | Exit |
|---|---|---:|
| `semantic.k`, main `MPY`, syntax `MPY-SYNTAX` | [stage3-kompile-semantic.log](/audit-output/evidence/stage3-kompile-semantic.log) | 0 |
| `verification.k`, main `VERIFICATION`, syntax `MPY-SYNTAX` | [stage3-kompile-verification.log](/audit-output/evidence/stage3-kompile-verification.log) | 0 |

The original four-claim specification closed together with `#Top` and exit 0
([stage3-kprove-all-claims.log](/audit-output/evidence/stage3-kprove-all-claims.log)).
Because the claims were unlabeled, I also copied each unchanged claim into its
own scratch spec module and ran it independently:

| Claim | Meaning | Result |
|---|---|---|
| 1 | universal symbolic integer claim | `#Top`, exit 0 |
| 2 | `(3,4,5) -> true` | `#Top`, exit 0 |
| 3 | `(1,2,3) -> false` | `#Top`, exit 0 |
| 4 | `(5,3,4) -> true` | `#Top`, exit 0 |

The exact logs are
[claim 1](/audit-output/evidence/stage3-kprove-claim-1.log),
[claim 2](/audit-output/evidence/stage3-kprove-claim-2.log),
[claim 3](/audit-output/evidence/stage3-kprove-claim-3.log), and
[claim 4](/audit-output/evidence/stage3-kprove-claim-4.log). The preserved
single-claim specs are under
[stage3-individual-specs](/audit-output/evidence/stage3-individual-specs/).

For generated-semantics validation, eight wrappers were produced from the
hash-checked submitted `solution.mpy`, not from the proof-local constant. The
case list is
[stage3-concrete-cases.json](/audit-output/evidence/stage3-concrete-cases.json);
the generator and exact hashes are recorded by
[generate_krun_inputs.py](/audit-output/evidence/generate_krun_inputs.py) and
[stage3-generate-inputs.log](/audit-output/evidence/stage3-generate-inputs.log).
Every `krun` exited 0 with `.K`, empty environment, and a Boolean result.

[stage3_compare_concrete.py](/audit-output/evidence/stage3_compare_concrete.py)
then compared each K result with fresh CPython calls:

| Input | K | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `(3,4,5)` | true | true | true |
| `(1,2,3)` | false | false | false |
| `(5,3,4)` | true | true | true |
| `(0,0,0)` | false | false | true |
| `(-3,-4,-5)` | false | false | true |
| `(30000,40000,49999)` | false | false | false |
| `(30000,40000,50000)` | true | true | true |
| `(30000,40000,50001)` | false | false | false |

There were zero K-versus-candidate mismatches. Exact per-case `krun` commands,
outputs, and statuses are the `stage3-krun-*.log` files; the aggregate
comparison is
[stage3-concrete-comparison.log](/audit-output/evidence/stage3-concrete-comparison.log).

Dynamic reconstruction gate: pass.

## 4. Adequacy and real-program pinning

### Claim preconditions and postconditions

None of the four claims has a `requires` clause.

1. For arbitrary K integers `A`, `B`, and `C`, begin with exactly the runner
   call, empty environment, and `noResult`. The destination requires consumed
   computation `.K`, still-empty environment, and exactly
   `result(rightTriangle(A,B,C))`.
2. The same initial state at `(3,4,5)` must finish with exactly `result(true)`.
3. The same initial state at `(1,2,3)` must finish with exactly `result(false)`.
4. The same initial state at `(5,3,4)` must finish with exactly `result(true)`.

All entry preconditions are satisfiable. For claim 1, the concrete state with
`A=3`, `B=4`, `C=5`, `.Map`, and `noResult` is a witness; claims 2–4 literally
provide satisfying ground states. The postconditions contain no fresh or free
result variable, tautology, implication, or existential escape.

### Pinning

The `<k>` cell runs `solutionProgram`, a nullary proof-local function. Its sole
equation expands to the complete submitted MPY term and then the normal MPY
rules evaluate that term. It does not rewrite an invocation to an answer.

I independently parsed the actual `solution.mpy` and the `solutionProgram`
constant, normalized each under the fresh verification definition, and
compared their final program configurations. They were byte-identical, with
SHA-256
`d9ec2b17385824267f350be38964113593478585b5171c736e5fd185bf010978`.
The successful commands and diff are in
[stage4-actual-program-final.log](/audit-output/evidence/stage4-actual-program-final.log),
[stage4-constant-program-final.log](/audit-output/evidence/stage4-constant-program-final.log),
and [stage4-program-final-diff.log](/audit-output/evidence/stage4-program-final-diff.log).
Two earlier parser experiments failed before execution because the default
syntax module cannot parse the verification-local constant; those failures are
preserved in `stage4-program-constant-identity.log` and
`stage4-program-constant-custom-parser.log` and were not counted as evidence.
The reviewer parser wrapper is
[kast_verification_parser.sh](/audit-output/evidence/kast_verification_parser.sh).

Concrete substitution confirms claim 1 at `(3,4,5)` and `(1,2,3)` against both
Python implementations. At `(0,0,0)`, which also satisfies the formal claim's
unrestricted integer entry state, the K result and candidate result are both
false while canonical is true. Thus the K claim pins the real submitted
program; it does not prove broad-domain canonical equivalence.

Adequacy/pinning gate: pass for the submitted program, with the domain concern
identified in stage 2.

## 5. Rule-by-rule static soundness review

There are no generated helper K files beyond `semantic.k`, `verification.k`,
and `spec.k`. The complete numbered sources and filtered declarations are in
[stage5-static-declarations.log](/audit-output/evidence/stage5-static-declarations.log).

### Local syntax inventory

| Declaration | Productions and role | Review |
|---|---|---|
| `Expr` | `Int`, `Name`, `BinOp`, `Compare`, `BoolOp` | Exactly the expression constructors used |
| `CmpOp` | operator string plus right expression | Covers the submitted single comparisons |
| `Exprs` | comma-separated `Expr` list | Carries Boolean operands |
| `Params` | wraps `Strings` | Carries the three parameters |
| `Strings` | comma-separated `String` list | Parameter binding list |
| `Stmt` | `FuncDef`, `Return` | Exactly the submitted statements |
| `Stmts` | juxtaposed `Stmt` list | Module/function bodies |
| `Program` | `Module(Stmts)` | Submitted top-level term |
| `Ints` | comma-separated `Int` list | Runner arguments |
| `Arguments` | `Args(Ints)` | Runner argument wrapper |
| `Input` | `Program` or `run(Program,String,Arguments)` | Configuration input |
| `Value` | `iVal(Int)`, `bVal(Bool)` | Internal evaluated values |
| `Result` | `noResult`, `result(Bool)` | Observable return state |
| `KItem` | `bind`, `eval`, `binRight`, `binApply`, `cmpRight`, `cmpApply`, `boolTail`, `boolMerge`, `publish` | Explicit evaluation/control frames |
| `Bool` extension | `rightTriangle(Int,Int,Int)` | Fully defined postcondition function |
| `Program` extension | `solutionProgram` | Fully defined name for the exact MPY term |

There are two local function declarations:
`rightTriangle` is `[function,total]`, and `solutionProgram` is `[function]`.
There are no `[functional]` declarations, opaque symbols, priority rules,
`[simplification]` rules, `[concrete]` rules, macros, `owise` rules, or
proof-local ordinary operational bridges.

### Construct coverage

The trusted translator mapping is recorded in
[stage5-translator-constructs.log](/audit-output/evidence/stage5-translator-constructs.log).
Every constructor in submitted `solution.mpy` is both declared and consumed:

| Submitted construct | Declaration | Operational handling |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | `Program`, `Stmt`, `Params` | exact runner destructuring and binding |
| `BoolOp("and"/"or",...)` | `Expr`, `Exprs` | `eval`, `boolTail`, `boolMerge` |
| `Compare`, `CmpOp(">" / "==",...)` | `Expr`, `CmpOp` | left/right frames and comparison application |
| `BinOp("+" / "*",...)` | `Expr` | left/right frames and integer application |
| `Name` | `Expr` | map lookup |
| `Int(0)` | `Expr` | integer value |
| MPY statement/expression lists | `Stmts`, `Exprs`, `Strings` | built-in list constructors plus consuming rules |
| proof runner `Args(A,B,C)` | `Arguments`, `Ints` | pairwise binding |

### Ordinary semantic rules

| # | Source line | Rule | Static judgment |
|---:|---:|---|---|
| 1 | 55 | exact `run` dispatch | Selects the sole function only when requested name equals defined name; evaluates its actual return expression |
| 2 | 60 | empty `bind` | Correct base case |
| 3 | 61 | cons `bind` | Binds one parameter to one integer and structurally descends |
| 4 | 64 | `eval(Int)` | Correct integer literal |
| 5 | 65 | `eval(Name)` | Correct lookup from the environment |
| 6 | 68 | begin `BinOp` | Enforces left operand first |
| 7 | 69 | continue `BinOp` | Enforces right operand second and preserves left value |
| 8 | 70 | apply `+` | K unbounded integer addition matches Python integer addition |
| 9 | 71 | apply `*` | K unbounded integer multiplication matches Python integer multiplication |
| 10 | 73 | begin `Compare` | Enforces left operand first |
| 11 | 76 | continue `Compare` | Enforces right operand second and preserves left value |
| 12 | 77 | apply `>` | Correct operand order: left `I >Int` right `J` |
| 13 | 78 | apply `==` | Correct integer equality |
| 14 | 83 | begin `BoolOp` | Starts with the first operand |
| 15 | 84 | empty Boolean tail | Returns the accumulated Boolean |
| 16 | 85 | nonempty Boolean tail | Evaluates the next operand and preserves accumulator/operator/rest |
| 17 | 88 | merge `and` | Correct Boolean conjunction and structural descent |
| 18 | 91 | merge `or` | Correct Boolean disjunction and structural descent |
| 19 | 95 | `publish` | Requires exact end context and `noResult`, clears locals, and publishes exactly the computed Boolean |

The empty/cons, operator, and constructor cases are disjoint. No priority is
needed. Binding and expression recursion structurally descend, so all used
operations terminate. There is no heap, allocation, I/O, exception, loop, or
call-stack behavior in the submitted expression that the configuration omits.
`publish` matches an exact trailing context and therefore cannot discard a
continuation.

Rules 14–18 eagerly evaluate all Boolean operands rather than short-circuiting.
This would not be a complete semantics for arbitrary Python expressions: an
unreachable unbound name or failing expression could distinguish it. I do not
label these rules unsound for the submitted program because every actual
operand is a pure, total, Boolean-valued comparison over bound K integers, and
no operand changes any cell. On that complete match domain, eager evaluation
has the same Boolean, state, and control outcome. The concrete tests exercise
both true and false prefixes. This is a narrow generated-semantics boundary,
not a false conclusion witness on the intended submitted-program domain.

### Verification equations

| Equation | Class | Coverage/overlap | Judgment |
|---|---|---|---|
| `rightTriangle(A,B,C)` | definitional summary used only in the postcondition | One unguarded equation covers every integer triple; no overlap; terminating | Exactly the positivity and three squared-equality tests executed by the candidate |
| `solutionProgram` | definitional program constant | One ground equation; no overlap; terminating | Dynamically shown identical to parsed submitted `solution.mpy`; execution is not skipped |

`rightTriangle` does not occur in an operational bridge, and
`solutionProgram` does not return or predict a Boolean. No same-symbol
operational/postcondition circularity exists. The proof equations use ordinary
K integer and Boolean mathematics and do not encode a false result.

No rule is judged unsound, so there is no claimed unsoundness requiring a false
conclusion witness. The only narrower evidence gap is general-Python
short-circuit behavior outside the fixed submitted program; it is explicitly
excluded rather than mislabeled.

Static soundness gate: pass.

## 6. Fresh non-vacuity test

I created a fresh scratch spec that changes the ground `(3,4,5)` result
obligation from `result(true)` to `result(false)`. The entry state is
satisfiable and both Python implementations return true for that input.
The preserved mutation is
[stage6-spec-vacuity.k](/audit-output/evidence/stage6-spec-vacuity.k).

The dry run parsed and built the proof input successfully with exit 0:
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).
The real proof then exited 1 with `WarnStuckClaimState`. Its residual is a
fully terminated configuration containing `result(true)`, which cannot unify
with the mutated `result(false)` destination:
[stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation.

Non-vacuity gate: pass.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the freshly compiled MPY definition, for every K integer triple
`A,B,C`, the exact submitted program term, invoked through the exact runner
configuration with empty environment and `noResult`, reaches `.K`, restores
the empty environment, and returns:

`A>0 and B>0 and C>0 and (A²+B²=C² or A²+C²=B² or B²+C²=A²)`.

The three ground claims are redundant executable instances of that theorem.
The result is constrained, the real body executes, and the false-result
mutation is rejected.

### Trust ledger and limitations

| Boundary | Influence | Status and evidence |
|---|---|---|
| K compiler, Haskell backend, reachability engine | Parsing, rewriting, proof closure | Trusted toolchain boundary; fresh version/build/proof logs recorded |
| K `Int`, `Bool`, `Map`, and list hooks | All arithmetic, logic, bindings, and traversal | Acceptable standard primitives; no local redefinition |
| Trusted `py2mpy.py` | Python AST to MPY identity | Trusted mounted input; byte identity and regenerated output checked |
| `solutionProgram` equation | Chooses the body being proved | Not assumed: parsed-normal-form identity with submitted `solution.mpy` checked |
| Minimal `run`/binding/evaluation semantics | Connects MPY term to Python behavior | Individually reviewed; exact used constructs covered; eight K/CPython ground comparisons |
| Eager Boolean evaluation | Control/evaluation-order bridge | Acceptable only because every fixed operand is pure, total, bound, and Boolean-valued; not claimed as general Python semantics |
| K mathematical integers versus CPython integers | Numeric results | Acceptable for this expression: CPython integers and K integers are unbounded, and only `+`, `*`, `>`, `==` are used |
| `rightTriangle` meaning | Human-facing property | Fully defined rather than opaque; its connection to “right angle” uses the ordinary Pythagorean theorem and the informal convention that lengths are positive |
| Candidate versus canonical equivalence | Intent bridge | Empirically exact on tested positive lengths; explicitly false on some non-positive integers; no universal canonical-equivalence theorem is claimed |
| Differential and concrete tests | Finite bridge evidence | Reproducible finite evidence only; not substituted for K reachability proof |

There are no opaque result symbols, unconstrained oracles, empirical rewrite
rules, proof-local simplifications, auxiliary loop claims, or informal
invariants. The proof does not establish semantics for unused Python
constructs, floating-point inputs, arbitrary malformed MPY, general
short-circuit exceptions, or broad-domain equality with the canonical
function.

Gate summary:

- Real-program soundness and non-vacuity: pass.
- Intent adequacy: sound for positive geometric side lengths; documented
  ambiguity/divergence outside that domain.
- Trust and evidence auditability: pass.

The candidate is therefore legitimate, with concerns limited to the
natural-language/canonical input-domain bridge rather than proof soundness.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
