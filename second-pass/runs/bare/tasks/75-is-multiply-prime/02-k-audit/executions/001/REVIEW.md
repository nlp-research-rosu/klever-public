# Independent adversarial audit: 75-is-multiply-prime

## Decision

**CONCERNS / LEGIT.**

The candidate contains a cleanly reconstructible, result-constraining K
reachability proof over its generated semantics. The submitted Python source
regenerates the submitted MPY file byte-for-byte with the trusted translator;
the term executed by the claim is the same MPY term; a fresh Haskell definition
builds; the sole target claim exits 0 with exactly `#Top`; the generated
semantics executes correctly in a fresh LLVM build; and both a body-sensitivity
mutation and a false-postcondition mutation fail for the expected semantic
reason.

The concern is about the intent bridge, not real-program soundness. The formal
postcondition defines “three-prime product below 100” by the same finite set of
22 values that the implementation tests. The equation is a consistent and
correct finite characterization, and the characterization was independently
checked below, but K does not define primality or prove that the finite set is
equivalent to the natural-language existential property. That last bridge is
ordinary mathematical reasoning plus finite differential evidence. Under the
requested decision boundary, this is an informal intent bridge and therefore
`CONCERNS`, not an unsound proof and not `FAIL`.

All candidate logs, compiled definitions, prose, and traces were treated only
as untrusted claims. All executable reconstruction used source copied to
`/tmp/audit-work`; no candidate-provided compiled definition or cache was used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the three expected regular files at its top level:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` is absent, as this mode requires. There is no
mount contradiction and therefore no infrastructure breach. See
`evidence/stage1-integrity-corrected.log`.

### Candidate artifacts and types

The following required control/source artifacts exist and are regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`solution-program.k`, `verification.k`, `spec.k`, `definition.k`, and
`prove.sh`. `prove.sh` is executable. The structured JSONL generation trace is
also a regular file. No symlink exists anywhere under `/candidate`.

The candidate additionally contains `__pycache__/`, `definition-kompiled/`,
and `semantic-kompiled/`. These are extra generated/cache artifacts, not source
integrity failures. They were not copied into scratch and were never used.
`PROOF.md` and a candidate `spec-vacuity.k` are absent; neither was a required
generation deliverable, and the audit did not infer evidence from their
absence.

The candidate prompt and translator are byte-identical to the trusted versions:

| Artifact | Trusted SHA-256 | Candidate SHA-256 | Result |
|---|---|---|---|
| `prompt.py` | `f471343f29b4ca3b2e1da0d10fd5459e0f13b7a9cef2897ed4ce88e88bde5db9` | same | exact |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | same | exact |

There are no missing, changed, mistyped, or symlinked required artifacts.

### Untrusted generation claims

`run-input.json` claims problem `75-is-multiply-prime`, condition `bare`, and
no supplied semantics. `metrics.json` claims a successful, non-timeout
generation. `codex-last.txt`, `codex-output.log`, and the 127-record structured
trace claim that the generator compiled, ran concrete cases, and obtained
`#Top`. Those claims were read but were not accepted as proof evidence.

The complete JSONL was parsed by `evidence/trace_summary.py`; its SHA-256 is
`27be93a4e71b990c0deadc304814cc1770ca101a3ef3283ecbf78d06633f7b04`.
The prior generation actions and success/error claims are summarized in
`evidence/stage1-trace-summary.log` and
`evidence/stage1-generation-claims.log`. The authoritative provenance record
is `evidence/stage1-integrity-corrected.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

For an integer `a` strictly less than 100, `is_multiply_prime(a)` must return
`True` exactly when `a` is the product of three positive primes. Repetition is
allowed, as shown by the canonical three independent prime loops; order is
irrelevant. The documented example is `30 = 2 * 3 * 5`.

The trusted canonical function checks primes from 2 through 100 and searches
all ordered triples. On the intended domain this is equivalent to exactly three
prime factors counted with multiplicity. Negative integers, 0, and 1 are false.

The candidate implements a straight disjunction over:

`8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50, 52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99`.

This is a different algorithm from the canonical search, which is acceptable.

### Translator and MPY identity

Only source artifacts were copied to `/tmp/audit-work/rebuild`. Running the
trusted `/reference/py2mpy.py` there regenerated `solution.mpy` with SHA-256
`2ed20f37c9f9cc534ea932248a2599788f3e6de80cc7303669d627aef0439709`.
`cmp` established byte identity with the submitted
`/candidate/solution.mpy`. See `evidence/stage2-regenerate.log`.

The normalized RHS of `solutionProgram` in `solution-program.k` is also exactly
the submitted MPY term: both normalized strings have length 926 and compare
equal. This is recorded by `evidence/program_pinning.py` and
`evidence/stage2-program-pinning.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the generated entry point. Its third oracle
counts prime factors and does not reuse the candidate list or K equations.

The input set contains:

- the documented example 30;
- numeric zero as the relevant empty/neutral boundary (there is no collection
  input for which an empty case exists);
- every nonnegative intended-domain integer from 0 through 99, thereby
  exercising every equality arm and both sides of every branch boundary;
- strict-upper-bound case 99;
- selected negative boundaries, including `-1`, `-2`, `-100`, and `-101`;
- one negative integer of magnitude `10^100`;
- 32 deterministic generated negative integers with seed `20260723`.

All three implementations agreed on all 138 inputs. The exact input list,
seed, 22 true values, zero mismatches, command, and exit 0 are in
`evidence/stage2-differential.log`.

The formal domain deliberately excludes `a >= 100`. As an explicit scope
control, the generated function and canonical function diverge at 105 and 125,
which are products of three primes but outside the stated bound. This does not
contradict the theorem; it demonstrates why its `A <Int 100` precondition
matters. See `evidence/stage2-out-of-domain-control.log`.

Differential testing is finite evidence only. Completeness over the infinite
negative part of the domain follows informally because a product of positive
primes is positive and every equality in the implementation is positive.

## 3. Clean proof reconstruction

### Toolchain and isolation

The independent toolchain was:

- K `v7.1.293`, build date 2025-10-03;
- Python `3.10.12`.

See `evidence/toolchain.log`. The initial scratch manifest in
`evidence/stage2-regenerate.log` contains only copied source/trusted inputs and
no compiled directory. Explicit output directories were then created in
scratch. `XDG_CACHE_HOME` was directed to `/tmp/audit-work/cache`.

### Fresh generated-semantics build and execution

The concrete definition was built from `semantic.k`:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

It exited 0 (`evidence/stage3-kompile-concrete.log`). Fresh `krun` executions
of the regenerated MPY program produced:

| `A` | K result | Python generated | Python canonical |
|---:|---:|---:|---:|
| -7 | false | false | false |
| 0 | false | false | false |
| 8 | true | true | true |
| 10 | false | false | false |
| 30 | true | true | true |
| 97 | false | false | false |
| 98 | true | true | true |
| 99 | true | true | true |

Each `krun` command and full final configuration is in the corresponding
`evidence/stage3-krun-*.log`. The corrected automated comparison reports zero
mismatches in `evidence/stage3-concrete-comparison-corrected.log`.

The first reviewer comparison script run failed because its regular expression
was over-escaped; that reviewer error is preserved in
`evidence/stage3-concrete-comparison.log`, and the source was corrected before
the successful comparison. It is not candidate evidence or a candidate
failure.

### Fresh proof build and every positive claim

The proof definition was built from `definition.k` and its source imports:

```text
kompile definition.k --backend haskell --main-module DEFINITION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

It exited 0 (`evidence/stage3-kompile-proof.log`). A fresh source search found
exactly one target claim, the unlabeled entry claim in `spec.k`; there are no
auxiliary or loop claims (`evidence/stage3-claim-inventory.log`).

The independent target command was:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It exited 0 and printed exactly `#Top`
(`evidence/stage3-kprove-spec.log`). Thus the dynamic reconstruction gate
passes.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole entry claim has this precondition:

- `A` is a K `Int`;
- `A < 100`;
- `<k>` contains exactly `solutionProgram`;
- `<arg>` contains `A`;
- the local `<env>` is empty;
- `<result>` is `noResult`.

There is no lower bound. The state is satisfiable: for example, `A = 30`,
empty environment, and `noResult` meets every condition.

Its postcondition says that execution consumes the entire computation
(`solutionProgram => .K`), preserves `<arg> A`, restores the environment to
`.Map`, and changes the result to:

```text
Bool(isThreePrimeProductBelow100(A))
```

This is an exact result rewrite, not a free RHS variable, existential,
tautology, or one-way implication. The claim therefore constrains the
observable return value.

### Actual-program execution

`solutionProgram` has one nullary defining equation whose RHS is the submitted
MPY term. Stage 2 established term identity independently. From there:

1. the module-entry rule binds the actual parameter name `"a"` to `Int(A)`;
2. the real `Return(BoolOp(...))` body is placed under `execute`;
3. the return rule calls the expression evaluator on that real expression;
4. each real `Compare(Name("a"), CmpOp("==", Int(...)))` is evaluated;
5. the real 22-element `or` list is consumed before the result is produced.

There is no helper function or loop in the submitted solution and no helper or
loop reachability claim to audit.

The generated semantics models the intended external call by treating the
single module-level unary function as the entry point and taking its argument
from `<arg>`. It does not model general Python module loading or dynamic name
resolution. For this exact one-function, pure program, the binding and control
path match the intended `is_multiply_prime(a)` call. The ignored `_F` name
would be over-broad for a reusable general Python semantics, but it cannot
select a different body in this exact pinned singleton module.

### Concrete substitutions

`evidence/spec-ground.k` substitutes two satisfying states:

- `A = 30`, demanded result `Bool(true)`;
- `A = 10`, demanded result `Bool(false)`.

Both ground claims close together with `#Top` and exit 0 in
`evidence/stage4-kprove-ground.log`. Both values also match the generated and
canonical Python functions in
`evidence/stage4-python-ground-corrected.log`.

The first one-line reviewer Python command used a hyphenated filename as a
module name and failed to import it; that reviewer error is preserved in
`evidence/stage4-python-ground.log` and was replaced by the path-based
`evidence/ground_compare.py`.

### Body sensitivity

A separate operational-sensitivity mutation replaces the program equality arm
`a == 30` with `a == 31` in both `solution.py` and the pinned
`solutionProgram` term. The trusted translator regenerates a term matching the
mutated wrapper. The mutated program is false at 30 where the canonical is
true, and true at 31 where the canonical is false
(`evidence/body-mutation-check.log`).

Fresh concrete K execution changes accordingly
(`evidence/body-mutation-krun-a30.log` and
`evidence/body-mutation-krun-a31.log`). A fresh Haskell build succeeds, but the
original target claim exits 1 with `WarnStuckClaimState`; its residual visibly
compares the original `A ==Int 30` specification arm with the mutated
`A ==Int 31` execution arm (`evidence/body-mutation-kprove.log`). This confirms
that the successful proof depends on the submitted body.

## 5. Rule-by-rule static soundness review

The authoritative numbered source and attribute search is
`evidence/stage5-source-inventory-corrected.log`. It found four local
`[function]` declarations, one local `[simplification]` rule, and no local
`total`, `functional`, `concrete`, `priority`, `owise`, or `anywhere`
attribute. There are no opaque local symbols. The earlier inventory script
stopped while counting absent attributes because of reviewer-side `pipefail`;
that failed run is preserved as `evidence/stage5-source-inventory.log` and was
corrected.

### Exhaustive local syntax inventory

| ID | Declaration | Role and assessment |
|---|---|---|
| S1 | empty sort `Pgm` | Root MPY program sort; used. |
| S2 | empty sort `Stmt` | Statement sort; used. |
| S3 | empty sort `Expr` | Expression sort; used. |
| S4 | empty sort `Params` | Parameter-list wrapper sort; used. |
| S5 | empty sort `CmpOp` | Comparison-operation sort; used. |
| S6 | `Stmts ::= List{Stmt, ""}` | Zero-or-more statement sequence; singleton function body and singleton return body are used. |
| S7 | `Exprs ::= List{Expr, ","}` | Boolean operand sequence; the 22 operands are used. |
| S8 | `Strings ::= List{String, ","}` | Parameter-name sequence; singleton `"a"` is used. |
| S9 | `CmpOps ::= List{CmpOp, ","}` | Comparison chain; singleton `==` is used. |
| S10 | `Pgm ::= Module(Stmts)` | Submitted root constructor; used. |
| S11 | `Stmt ::= FuncDef(String, Params, Stmts)` | Submitted function definition; used. |
| S12 | `Stmt ::= Return(Expr)` | Submitted return; used. |
| S13 | `Params ::= Params(Strings)` | Submitted unary parameter list; used. |
| S14 | `Expr ::= Name(String)` | Submitted parameter reference; used only under comparison. |
| S15 | `Expr ::= Int(Int)` | Submitted integer literal; used. |
| S16 | `Expr ::= Bool(Bool)` | Boolean expression/result wrapper; used in the result, not as a submitted source literal. |
| S17 | `Expr ::= BoolOp(String, Exprs)` | Submitted `"or"` expression; used. |
| S18 | `Expr ::= Compare(Expr, CmpOps)` | Submitted one-operation comparisons; used. |
| S19 | `CmpOp ::= CmpOp(String, Expr)` | Submitted `"=="` operations; used. |
| S20 | `Result ::= noResult \| Expr` | Initial result sentinel and final Boolean expression; both used. |
| S21 | `KItem ::= execute(Stmts)` | Internal control marker for the selected function body; used. |
| S22 | `Bool ::= evalBool(Expr, Map) [function]` | Big-step evaluator. It is intentionally not total over all declared `Expr`; every actual use is covered. |
| S23 | `Bool ::= evalOr(Exprs, Map) [function]` | Finite list evaluator; empty/nonempty cases cover actual lists. |
| S24 | `Pgm ::= solutionProgram [function]` | Nullary name for the exact submitted MPY term; fully defined by one equation. |
| S25 | `Bool ::= isThreePrimeProductBelow100(Int) [function]` | Formal postcondition predicate; fully defined for every integer by one unguarded equation. |

`definition.k` adds no syntax or rule. `spec.k` adds only the entry claim.

### Construct-to-rule coverage

| MPY construct/tag | Declaration | Behavioral rule(s) |
|---|---|---|
| `Module` + singleton `FuncDef` | S10, S11 | R6 enters the exact body and binds the singleton parameter. |
| `Params("a")` | S8, S13 | R6 stores `"a" |-> Int(A)`. |
| `Return` | S12 | R7 consumes it, clears the local environment, and sets the result. |
| `BoolOp("or", ...)` | S17 | R3 delegates to `evalOr`; R4/R5 consume the list. |
| `Compare(Name("a"), CmpOp("==", Int(I)))` | S14, S15, S18, S19 | R2 reads the exact singleton binding and applies K integer equality. |
| expression/statement/list separators | S6–S9 | K-generated list constructors, with R4/R5 supplying Boolean list behavior. |
| strings and integers | imported `STRING`/`INT` syntax | Standard K token and hook semantics. |

There is no used assignment, heap, allocation, I/O, exception, loop, general
call, multi-function binding, or non-Boolean `or` operand.

### Exhaustive local rule inventory

| ID | Rule | Classification and review |
|---|---|---|
| R1 | `evalBool(Bool(B), _) => B` | Definitional evaluator equation. Correct; a Boolean literal evaluates to itself and the environment is irrelevant. |
| R2 | singleton-bound `Compare(Name(X), CmpOp("==", Int(I))) => A ==Int I` | Definitional evaluator equation. The pattern requires exactly the environment produced by R6, exactly one comparison operator, tag `"=="`, and an integer literal. Correct for every actual comparison. |
| R3 | `evalBool(BoolOp("or", ES), ENV) => evalOr(ES, ENV)` | Definitional evaluator equation. Correct for the used Boolean-valued operands. |
| R4 | `evalOr(.Exprs, _) => false` | Base equation. Python `or` of no operands is not surface syntax, but this internal fold identity is correct and is reached after consuming the actual list. |
| R5 | nonempty `evalOr` uses `orElseBool` | Recursive equation. The list strictly shortens. K's standard `orElseBool` is short-circuiting; all used operands are pure Boolean comparisons, so value and effects agree with Python. |
| R6 | module/singleton-function entry rule | Ordinary operational rule. It preserves `<arg>`, requires empty `<env>`, binds the exact singleton parameter, and enters the exact body. It abstracts the external harness call. The wildcard function name is broader than needed but cannot select another function in the pinned program. |
| R7 | `execute(Return(E))` consumes control, clears env, and stores `Bool(evalBool(E, ENV))` | Ordinary operational rule. Correct for the actual pure Boolean expression; no skipped state, exception, output, allocation, or continuation exists in the modeled configuration. Unsupported expressions remain stuck through `evalBool` rather than receiving fabricated results. |
| R8 | `solutionProgram => Module(...)` | Definitional summary, not an operational shortcut. Its RHS is independently pinned to submitted `solution.mpy`. It exposes, rather than bypasses, the real body. |
| R9 | `isThreePrimeProductBelow100(A) =>` finite disjunction `[simplification]` | Definitional postcondition summary. Unguarded, terminating, nonrecursive, and the only equation for its symbol, so there is no overlap or coverage gap. It affects the result obligation but does not replace execution. Its natural-language meaning is the documented informal bridge discussed below. |

The entry claim C1 is the sole reachability claim and was analyzed in Stage 4.

### Guards, overlap, totality, and control

- R1, R2, and R3 have disjoint outer expression constructors.
- R4 and R5 are the disjoint empty and nonempty list cases.
- R6 and R7 have disjoint front-of-`<k>` forms.
- R8 is a complete nullary definition.
- R9 is one unguarded equation over every K integer.
- No local rule has a priority or guard. No local equation pair overlaps.
- No local function is declared `total`; unsupported declared syntax therefore
  stops visibly. The actual term uses only covered cases.
- Evaluation is left-to-right/short-circuit through the recursive head and
  standard `orElseBool`. Because all operands are pure comparisons, even an
  order discrepancy would not change state, but the selected operator also
  matches Python's short-circuit behavior.
- The explicit state footprint is `<k>`, `<arg>`, `<env>`, and `<result>`.
  `<arg>` is preserved. R6 allocates the one local binding; R7 removes it.
  There is no hidden candidate heap, call stack, output, or exception cell.
- R7 introduces completion only for an exact `execute(Return(E))` computation;
  it does not use a framed `...` continuation and therefore cannot discard an
  arbitrary suffix.

### Mathematical review of R9

For positive primes ordered `p <= q <= r` with `p*q*r < 100`:

- `p = 2, q = 2`: `r` is one of `2,3,5,7,11,13,17,19,23`;
- `p = 2, q = 3`: `r` is one of `3,5,7,11,13`;
- `p = 2, q = 5`: `r` is `5` or `7`;
- `p = 2, q = 7`: `r` is `7`;
- `p = 3, q = 3`: `r` is one of `3,5,7,11`;
- `p = 3, q = 5`: `r` is `5`;
- all other ordered cases are at least `3*7*7` or `5^3`, both above 100.

Their products are exactly the 22 values in R9 and in `solution.py`.
Commutativity covers all orderings; repetition is retained. Negative values,
0, and 1 are not products of positive primes. Thus no concrete or symbolic
false-conclusion witness exists for R9 on the intended domain.

R9 does encode the finite target set as the formal specification. It is not an
operational rule and cannot make the execution return a value it did not
compute. Nevertheless, K proves equality to that finite definition, not a
separate formalization of primality and existential factorization. This is the
principal documented concern.

### Builtin trust

The proof imports K's standard `INT`, `BOOL`, `MAP`, `LIST`, and `STRING`
domains. Relevant standard declarations show total hooked integer
multiplication/equality, Boolean `orBool`/`orElseBool`, and map/list
constructors. The exact inspected lines are in
`evidence/stage5-builtin-boundary.log`. These are ordinary low-level language
primitives, not candidate-supplied correctness conclusions.

No local rule was found unsound. Accordingly, this review does not manufacture
an “unsoundness witness.” The two mutations are sensitivity and non-vacuity
evidence, not allegations that an original rule is false.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was used. The reviewer-authored
`evidence/spec-vacuity.k` keeps the actual execution and precondition but
changes the result obligation to:

```text
Bool(notBool isThreePrimeProductBelow100(A))
```

This is meaningfully false. `A = 30` satisfies `A < 100`; Stage 3 concrete K
execution and Stage 4 ground proof show the actual result is `Bool(true)`,
whereas the mutation demands `Bool(false)`.

The mutation first passed KORE generation:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit status was 0 (`evidence/stage6-vacuity-dry-run.log`), ruling out a parser,
import, or build failure.

The real mutation proof command then exited 1:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY
```

It produced `WarnStuckClaimState` while checking the destination implication.
The residual visibly compares the execution's equality disjunction to the
negation of the formal result predicate. This is the expected unmet
result obligation, not a timeout, crash, unreachable mutation, or unrelated
error. See `evidence/stage6-vacuity-kprove.log`.

The proof is therefore non-vacuous and discriminates a false return-value
postcondition.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Relative to the freshly compiled candidate semantics, standard K builtins, and
R9's finite predicate definition, the successful claim establishes:

> For every K integer `A < 100`, if the exact submitted MPY term starts with
> argument `A`, empty local environment, and `noResult`, then its modeled
> execution reaches an empty computation and empty local environment with
> result `Bool(isThreePrimeProductBelow100(A))`, while preserving `A`.

This is a partial-correctness statement. The straight-line term and finite fold
also execute concretely on all tested cases, but no broader claim about
arbitrary Python programs or inputs outside `A < 100` is made.

### Trust ledger

| Boundary | Influence and dependents | Evidence | Assessment |
|---|---|---|---|
| K v7.1.293 compiler, parser, Haskell prover, LLVM runner | All syntax, execution, and proof closure | Fresh version record, builds, runs, and proof logs | Necessary low-level trusted computing base; acceptable. |
| Standard K `INT`, `BOOL`, `MAP`, `LIST`, `STRING` hooks/rules | Arithmetic, comparison, Boolean fold, binding, and parsing | Builtin declarations inspected; standard K distribution | Acceptable primitive boundary; not task-specific. |
| Trusted `/reference/py2mpy.py` | Python-AST-to-MPY identity | Candidate/trusted byte identity; fresh translation byte identity | Explicitly trusted input and reproducibly applied; acceptable. |
| `solutionProgram` textual embedding | Determines which body the K claim executes | Normalized term identity and body-sensitivity mutation | Machine-audited definitional link; acceptable, not opaque. |
| Generated direct-entry harness in R6/R7 | Connects a module containing one unary function to the intended external call and return | Rule-level audit, eight concrete K/Python comparisons, 138 Python differentials | Sound for the exact submitted pure singleton program; intentionally not a general Python semantics. |
| `evalBool`/`evalOr` big-step semantics | Determines every returned Boolean and short-circuit path | Exhaustive used-construct review, fresh concrete executions, successful body mutation | Program-derived but fully equational on every used term; no opaque oracle or unconstrained result. |
| R9 finite prime-product characterization | Determines the formal expected result | Exhaustive hand enumeration; complete 0..99 differential; selected negatives; canonical and independent factor-count oracle | Correct, but equivalence to the natural-language prime existential is not a K theorem. This is the reason for `CONCERNS`. |
| Trusted canonical Python entry point | Differential oracle for intended behavior | 138 zero-mismatch intended-domain cases | Trusted reference input and finite evidence; not a substitute for K proof. |
| Positivity/commutativity and completeness of the ordered prime-triple case split | Bridges R9 to the English contract | Explicit mathematical case split above | Ordinary informal mathematics; convincing but outside the machine-checked theorem. |

There are no candidate-defined opaque symbols, fresh symbolic oracles,
assumed loop invariants, proof-local operational bridges, priority overrides,
or unproved helper reachability claims. The same symbolic value is not used
circularly to replace program execution and satisfy the postcondition.

Candidate `#Top` output, compiled definitions, generation traces,
`codex-last.txt`, and prose were not included in the trust ledger because none
was trusted or reused.

### Validation gates

- **Gate A — real-program soundness: PASS.** The actual MPY term executes; the
  result is constrained; local equations are truthful on every use; a body
  mutation changes execution and breaks the proof; a false result obligation
  is rejected.
- **Gate B — intent adequacy: PASS with a documented informal bridge.** The
  strict integer domain and all 22 results align with the prompt and canonical
  function. The lack of a K-level prime/existential definition limits what is
  machine-checked but does not create a false conclusion.
- **Gate C — trust and evidence auditability: PASS.** Sources, scripts, exact
  commands, exit statuses, outputs, mutations, and finite input scope are
  preserved. Differential evidence is explicitly not presented as universal
  proof.

The proof is legitimate. It receives `CONCERNS` rather than `PASS` because its
final bridge from a manually enumerated finite predicate to the
natural-language notion of three prime factors is not formalized in K.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
