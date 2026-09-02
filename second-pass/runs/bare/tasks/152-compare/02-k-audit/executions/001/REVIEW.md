# Adversarial audit — 152-compare

The candidate has a legitimate, result-constraining partial-correctness proof
for equal-length lists of K integers under its generated semantics. The proof
was rebuilt from source, closes independently, executes an AST mechanically
shown equal to the submitted `solution.mpy`, is sensitive to a body change, and
rejects a concrete false result.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
formal claim states no equal-length or integer precondition while several
semantic helpers totalize invalid Python operations. That makes the formal
theorem broader than the prompt and broader than real Python behavior. In
addition, the recursive Python implementation raises `RecursionError` on valid
lists near the CPython recursion limit; the K model has an unbounded abstract
call stack. These limitations do not enable a false returned value on the
prompt's equal-length integer domain, and the requested standard is partial
correctness, not termination or total correctness.

All candidate prose, logs, traces, hashes, and prebuilt definitions were treated
as untrusted claims. All executable work used source-only copies under
`/tmp/audit-work/152-compare`. Reviewer scripts, mutations, and bounded logs are
under `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
`/reference/prompt.py`, `/reference/canonical.py`, and
`/reference/py2mpy.py`; `/reference/reference-semantics` is absent. This is the
required mode boundary, so there is no infrastructure breach. See
`evidence/02_integrity.log` and `evidence/02b_required_artifact_types.log`.

All required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
structured JSONL trace, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
There are no symlinks anywhere under `/candidate`. There are no helper K files,
so none are missing. No required artifact is missing, mistyped, or symlinked.

The candidate prompt is byte-identical to trusted `/reference/prompt.py`
(SHA-256
`b9449a0c09f62a6c759895e7539a750fab0bbf8c41f40c6ce7b077d4786e989f`).
The candidate translator is byte-identical to trusted
`/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

The extra `/candidate/semantic-kompiled`,
`/candidate/verification-kompiled`, and `/candidate/__pycache__` trees are
candidate-built outputs, not trusted sources. They were deliberately excluded
from scratch. Their presence is reported but is not an integrity failure.

The provenance records claim a successful bare generation and `#Top`. Their
contents were read only as claims. The complete files' sizes, hashes, structured
record counts, and claimed markers are recorded by
`evidence/provenance_summary.py` in
`evidence/20_provenance_summary.log`. Nothing in those records was used to
justify the verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two arrays of scores and guesses of equal length, return an array of the
same length whose element at index `i` is
`abs(game[i] - guess[i])`. Thus an exact guess contributes zero.

Trusted `/reference/canonical.py:21` implements this as
`[abs(x-y) for x,y in zip(game,guess)]`.

Candidate `/candidate/solution.py:1-7` is a recursive implementation:

1. return `[]` when `game` is empty;
2. compute `game[0] - guess[0]`;
3. negate it exactly when it is negative; and
4. prepend it to the recursive result on the two tails.

For equal-length integer lists this is the same componentwise absolute
difference. It does not mutate either input.

### Trusted translation identity

In scratch, the trusted translator regenerated `solution.mpy`; `cmp` succeeded
and both submitted and regenerated files had SHA-256
`8b1459d8f7e47fe17ad740613f5b14392282cdd23d81b304779d1994f6c83e5b`.
Exact command, exit 0, and hashes are in
`evidence/03_translation_identity.log`.

### Independent differential evidence

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the candidate entry point from their scratch copies. It covers:

- both documented examples;
- the empty case;
- zero, negative, and positive raw-difference branch boundaries;
- negative values and arbitrary-precision integer boundaries;
- every pair of equal-length lists of lengths 0 through 3 over `-3..3`
  (120,100 cases); and
- 500 deterministic generated pairs, lengths 0 through 64, with values in
  `[-10^12, 10^12]`.

All 120,609 cases matched. The deterministic input stream hash and zero mismatch
count are in `evidence/04_differential_test.log`. This is finite bridge evidence,
not a substitute for the K proof.

Two limitations were exposed:

- Unequal lengths are outside the explicit prompt domain. For
  `game=[1], guess=[]`, the canonical `zip` implementation returns `[]`, while
  the candidate raises `IndexError`. This witness is recorded in
  `evidence/04_differential_test.log`.
- Equal lists of length 1,000 are within the natural list domain, but the
  candidate raises `RecursionError` under the audited CPython 3.10 process,
  while the canonical implementation returns 1,000 elements. Length 900 still
  succeeds. See `evidence/python_recursion_boundary.py` and
  `evidence/21_python_recursion_boundary.log`. This is a termination/resource
  limitation. It does not refute a partial-correctness statement about normal
  returns, but it prevents treating the candidate as a total implementation for
  arbitrarily long real CPython lists.

## 3. Clean proof reconstruction

The source artifacts were copied to `/tmp/audit-work/152-compare` by the
recorded command in `evidence/01_scratch_copy.log`. No candidate-provided
compiled definition or cache was copied or referenced. The audited toolchain is
K v7.1.293.

### Fresh concrete definition

The following source-only build exited 0:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled
```

See `evidence/05_kompile_concrete.log`.

Fresh `krun` executions covered empty, zero difference, both sign branches, and
both prompt examples. Expected final values appear in:

- `evidence/06_krun_empty.log`
- `evidence/07_krun_zero.log`
- `evidence/08_krun_negative_branch.log`
- `evidence/09_krun_positive_branch.log`
- `evidence/10b_krun_example1_retry.log`
- `evidence/11_krun_example2.log`

One concurrently launched example-1 run encountered a transient Java-detection
failure (`evidence/10_krun_example1.log`, exit 2). The identical command was
rerun sequentially and succeeded with the expected `[0,0,0,0,3,3]`; the
failure is preserved and is not used as candidate evidence.

`evidence/k_python_bridge.py` then ran nine normal and boundary cases through
the freshly built semantics and compared the parsed K result with trusted
Python. The corrected run had zero mismatches
(`evidence/19b_k_python_bridge.log`). The earlier
`evidence/19_k_python_bridge.log` is an explicitly preserved reviewer-harness
regex error, not a semantic mismatch.

### Fresh proof definition and all positive claims

The source-only Haskell build exited 0:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

See `evidence/12_kompile_proof.log`.

`spec.k` contains exactly one positive claim. The independent command

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

exited 0 and printed exactly `#Top`; see
`evidence/13_kprove_positive.log`. Therefore the dynamic reconstruction gate
passes.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole entry claim at `/candidate/spec.k:6-7` has no `requires` clause.
Its inferred precondition is therefore: for arbitrary finite structural
`Values` lists `GS` and `US`, and arbitrary continuation `REST`, the `<k>` cell
starts with:

```text
execute(solutionProgram, VList(GS), VList(US)) ~> REST
```

Its postcondition is that execution produces the fully constrained value
`VList(expected(GS, US))` and preserves the exact same `REST`. The result is
not a fresh variable, tautology, or one-way condition.

There are no helper or loop claims. Recursive calls return to an instance of
the entry pattern on the two tails; K's reachability circularity is applied
after genuine semantic progress. A body mutation test confirms that closure is
not independent of the body.

### Exact submitted-program pin

`solutionProgram` is a total zero-argument K function whose only equation is the
complete constructor tree for the translated candidate program
(`/candidate/verification.k:8-28`). It does not replace the function's result;
it supplies the AST that the ordinary rules then execute.

The pin is supported at three independent levels:

1. trusted translation is byte-identical to submitted `solution.mpy`
   (`evidence/03_translation_identity.log`);
2. manual construct-by-construct inspection finds the equation identical to
   that translated term, with K list units `.Exprs` and `.Stmts` in place of
   the external parser's empty concrete lists; and
3. `evidence/make_pinning_spec.py` generated a claim from the exact scratch
   `solution.mpy` bytes, applying only those empty-list unit notations.
   `evidence/pinning-spec.k` built and proved `#Top` against the fresh
   definition (`evidence/28c_pinning_spec_dry_run.log` and
   `evidence/29_pinning_kprove.log`). `WarnTrivialClaim` is expected here:
   after evaluating the `solutionProgram` equation, the two ground AST terms
   are identical.

Earlier pinning attempts that used external empty-list syntax inside a claim,
and then a non-configuration functional claim, are preserved in
`evidence/28_pinning_spec_dry_run.log` and
`evidence/28b_pinning_spec_dry_run.log`; neither is used as evidence.

For body sensitivity, the reviewer changed the first subtraction from
`game[0]-guess[0]` to `game[0]-game[0]` in an isolated verification source.
The mutant compiled, but its positive proof exited 1 with an unmet equality
between the zero result and `expected(GS,US)`. See
`evidence/verification-body-mutant.k`,
`evidence/23_body_mutant_diff.log`,
`evidence/24_body_mutant_kompile.log`, and
`evidence/25_body_mutant_kprove.log`.

### Satisfying entry states and concrete substitution

Because there is no explicit precondition, the state

```text
GS   = VCons(VInt(1), VNil)
US   = VCons(VInt(0), VNil)
REST = .K
```

satisfies the entry pattern. The claimed result simplifies to `[1]`.
Fresh K execution returns `[1]`
(`evidence/09_krun_positive_branch.log`), and both trusted canonical Python and
candidate Python return `[1]`
(`evidence/04_differential_test.log` and
`evidence/19b_k_python_bridge.log`). Empty inputs likewise satisfy the entry
pattern and produce the claimed empty list.

The missing formal domain restriction is a real adequacy limitation. The
also-satisfying formal state `GS=[VInt(1)]`, `US=[]`, `REST=.K` returns `[1]`
under the generated semantics (`evidence/26_krun_unequal_off_domain.log`),
while candidate Python raises and canonical Python returns `[]`. The prompt
explicitly excludes this unequal-length witness, so it is not a false
conclusion on the intended domain; it demonstrates that the formal theorem
must not be reported as a theorem about all real Python inputs.

## 5. Rule-by-rule static soundness review

`evidence/18_static_inventory.log` is the mechanically extracted inventory. It
contains 20 local `syntax` declarations in `semantic.k`, 54 semantic rules, two
verification syntax declarations, four verification equations, and the one
entry claim.

### Syntax, configuration, and construct coverage

The local syntax inventory is exhaustive:

| Sort | Local productions |
|---|---|
| `Pgm` | `Module(Stmts)` |
| `Stmts`, `Stmt` | statement list; `FuncDef`, `Return`, `Assign`, `If` |
| `Params`, `Strings` | parameter wrapper and string list |
| `Expr`, `Exprs` | `Name`, `Int`, `ListExpr`, `BinOp`, `UnaryOp`, `Compare`, `Subscript`, `Call`; expression list |
| `CmpOps`, `CmpOp` | comparison list and operator/right-expression pair |
| `Index`, `Bound` | expression index; `Slice`; expression bound; `NoBound` |
| `Value`, `Values` | `VInt`, `VBool`, `VList`; `VNil`, `VCons` |
| `Env` | `EmptyEnv`, `Bind` |
| `Outcome` | `Ongoing`, `Returned` |
| `KItem` | `execute`, `invokeK`, `execK`, `evalK`, `evalExprsK`, `makeReturned`, `extractReturned`, `assignK`, `ifK`, `continueK`, `listHeadK`, `listTailK`, `binLeftK`, `binRightK`, `unaryK`, `compareLeftK`, `compareRightK`, `subscriptK`, `callArgK`, `callInvokeK` |

The configuration is the single `<k>` cell initialized with
`execute($PGM,$GAME,$GUESS)`. No heap, output, exception, or allocation cell is
present. That is adequate for this target's immutable integer/list operations:
the program performs no mutation, I/O, object-identity test, or observable
allocation.

Every constructor in `solution.mpy` is covered:

| Program construct | Declaration | Behavior |
|---|---|---|
| `Module`, `FuncDef`, `Params` | semantic lines 7, 10, 15 | exact invocation, lines 85-94 |
| statement sequencing, `If`, `Assign`, `Return` | lines 9-13 | lines 95-113 |
| `Name`, `Int`, `ListExpr` | lines 18-20 | lines 115-123 and 159-171 |
| `BinOp("-",...)`, `BinOp("+",...)` | line 21 | lines 125-132 |
| `UnaryOp("-")` | line 22 | lines 134-135 |
| `Compare(...,"==",...)`, `Compare(...,"<",...)` | lines 23, 28-29 | lines 137-143 |
| index `0` and slice `[1:]` | lines 24, 30-32 | lines 145-151 and 172-177 |
| recursive `Call(Name("compare"),...)` | line 25 | lines 153-157 |

The evaluator orders list elements, binary operands, comparison operands, and
call arguments left-to-right. Environments use front-shadowing, so assignment
updates `difference` without corrupting `game` or `guess`. `Returned` propagates
through `continueK` and prevents execution of the remaining statements. The
recursive call executes the same `Pgm` and returns through its own
`extractReturned`. These control and binding choices match the target body.

### Function, declaration, and special-attribute inventory

Semantic functions are:

- partial `lookupEnv`, `lookupAt`, `indexValue`, `dropValues`, and
  `concatValues`;
- total `headValue`, `tailValues`, `isEmptyValues`, and `valueAsInt`.

Verification adds total `solutionProgram` and total `expected`.
There are no explicit `functional` declarations, opaque symbols, priority
rules, `owise` rules, simplification rules, or proof-local ordinary operational
rewrites. Built-in `INT`, `BOOL`, and `STRING` operations come from
`domains.md`.

### Exhaustive semantic-rule decisions

“Limited” below means faithful on every reachable equal-length `VInt` input for
this program, but deliberately totalized or partial outside that intended
domain. No row is labeled unsound: no reviewed rule enables a false returned
value on a satisfying equal-length integer input.

| Lines | Rule | Decision |
|---|---|---|
| 85 | `execute => invokeK` | Sound administrative step; no state is dropped. |
| 86-94 | exact `Module(FuncDef("compare",...))` invocation | Sound for the pinned one-function module; binds both arguments in source order and retains `P`. |
| 95 | empty statement list to `Ongoing` | Sound fall-through representation. |
| 96 | `Return` evaluates its expression and ignores following statements | Sound abrupt return. |
| 97-98 | name assignment evaluates RHS first | Sound for the only assignment target used. |
| 99-100 | `If` evaluates its condition first | Sound evaluation order. |
| 102 | value plus `makeReturned` | Sound return wrapping. |
| 103 | top-level `extractReturned` | Sound return-value extraction. |
| 104-105 | assignment continuation with front binding | Sound shadowing/update for this immutable environment. |
| 106-108 | true branch | Sound; executes branch before the suffix. |
| 109-111 | false branch | Sound and disjoint from the true rule. |
| 112 | `Ongoing` continues with suffix | Sound normal control. |
| 113 | `Returned` discards suffix | Sound return propagation. |
| 115 | name evaluation via `lookupEnv` | Sound for bound names. |
| 116 | integer literal | Sound. |
| 117 | list-expression dispatch | Sound. |
| 118 | empty expression list | Sound empty list. |
| 119-120 | evaluate first list element | Sound left-to-right order. |
| 121-122 | evaluate remaining elements | Sound; saves the head value. |
| 123 | prepend saved head | Sound list construction. |
| 125-126 | begin binary expression with left operand | Sound. |
| 127-128 | evaluate right operand after left | Sound. |
| 129-130 | subtraction via `valueAsInt` | Sound for intended `VInt` operands; limited by off-domain coercions below. |
| 131-132 | list `+` via `concatValues` | Sound structural concatenation. |
| 134 | unary-expression dispatch | Sound. |
| 135 | integer unary minus | Sound arbitrary-precision integer negation. |
| 137-138 | single comparison dispatch | Sound for the target's one-comparator nodes. |
| 139-140 | right comparison operand after left | Sound. |
| 141-142 | saved list equals evaluated empty list iff saved list is empty | Sound for the exact `game == []` expression. |
| 143 | integer `<` | Sound; operand orientation is saved left `I`, evaluated right `J`, yielding `I < J`. |
| 145 | subscript evaluates container | Sound for constant indexes/slices used here. |
| 146 | dispatch to `indexValue` | Sound administrative step. |
| 147-148 | nonnegative list index | Sound on in-range target index; limited out of range by `headValue(VNil)`. |
| 149-151 | nonnegative `[N:]` via `dropValues` | Sound for the target's `[1:]`, including empty slices. |
| 153-154 | exact global `compare` call starts first argument | Sound for the pinned body, which cannot shadow or rebind `compare`. |
| 155-156 | second argument after first | Sound Python argument order. |
| 157 | recursive call invokes the retained program | Sound; it executes rather than summarizes the callee. |
| 159 | matching front environment binding | Sound. |
| 160-161 | skip nonmatching binding | Sound, disjoint from line 159 by the string guard, and structurally descending. |
| 163 | `VNil` is empty | Sound. |
| 164 | `VCons` is nonempty | Sound and exhaustive with line 163. |
| 165 | `headValue(VNil) => VInt(0)` | Limited totalization, not Python indexing. It is unreachable for intended equal-length indexing but explains the unequal-length mismatch. |
| 166 | head of `VCons` | Sound. |
| 167 | tail of `VNil` is `VNil` | Sound as a structural helper and for empty slicing. |
| 168 | tail of `VCons` | Sound. |
| 169 | `valueAsInt(VInt(I)) => I` | Sound and the only intended-domain case. |
| 170 | `valueAsInt(VBool(_)) => 0` | Limited/non-Python totalization; Python `True` behaves numerically as 1. No intended integer-score witness reaches it. |
| 171 | `valueAsInt(VList(_)) => 0` | Limited/non-Python totalization; real list subtraction raises. No intended integer-score witness reaches it. |
| 172 | index zero via `headValue` | Sound for nonempty lists; inherits line 165's off-domain totalization. |
| 173-174 | positive lookup decrements index | Sound structural descent for nonnegative indexes. |
| 175 | drop zero | Sound. |
| 176-177 | positive drop decrements count | Sound structural descent. |
| 178 | concatenate empty left list | Sound. |
| 179 | concatenate nonempty left list | Sound structural recursion. |

The limited rules have explicit false-real-Python witnesses only outside the
stated equal-length integer domain: unequal `[1],[]`, booleans, or nested list
elements. Accordingly, they are recorded as scope/evidence gaps rather than
called materially unsound. The CPython recursion-limit witness is on valid
integer lists, but concerns the omitted resource/exception model and
termination, not a rule deriving a wrong normal return.

### Exhaustive verification-rule decisions

| Lines | Extension | Class and decision |
|---|---|---|
| 9-28 | `solutionProgram => Module(...)` | Definitional program pin. It introduces the exact translated AST and does not bypass body execution. The external-file equality claim and body mutation validate identity and sensitivity. |
| 34-35 | `expected(GS,_) => VNil` when `GS` is empty | Definitional summary base case. Sound for the candidate and intended equal lengths. |
| 36-43 | negative-difference `expected` branch | Definitional summary. Produces `-(head(GS)-head(US))` and descends on both tails. |
| 44-51 | nonnegative-difference `expected` branch | Definitional summary. Produces the raw nonnegative difference and descends on both tails. |

The `expected` guards are pairwise disjoint: empty versus nonempty, then
`d < 0` versus `not(d < 0)`. They cover every structural `GS` and every integer
`d`, and recursion strictly descends `GS`. On equal lists of `VInt`, the two
nonempty branches are exactly `abs(game[i]-guess[i])`. `expected` never rewrites
an execution term and is not an operational bridge or oracle. Its off-domain
meaning inherits the explicit totalizations already identified.

There are no proof rules encoding the answer into program execution, no
unconstrained result-bearing symbol, no priority that preempts concrete
execution, and no silently fabricated behavior for a construct used on the
intended path.

## 6. Fresh non-vacuity test

The accepted reviewer mutation is `evidence/spec-vacuity.k`. It uses the
reachable, precondition-satisfying ground entry state with empty inputs, but
changes the result obligation from the true empty list to the deliberately
false singleton `[1]`.

The mutation built successfully:

```text
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit was 0; see `evidence/16_vacuity_ground_dry_run.log`.

The actual proof command exited 1 with `WarnStuckClaimState`; the residual
configuration is the real `VList(VNil)`, which does not unify with the false
destination. See `evidence/17_vacuity_ground_proof.log`. This is the expected
unmet result obligation and demonstrates non-vacuity.

For completeness, an earlier symbolic prepend mutation produced
`DecidePredicateUnknown` (`evidence/15_vacuity_proof.log`). It is explicitly
rejected as non-vacuity evidence because it was an unrelated backend decision
failure. The clean ground mutation above replaces it.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's generated semantics and built-in K integer/Boolean/string
theory, for arbitrary finite `Values` sequences `GS` and `US` and arbitrary
continuation `REST`, if execution from

```text
execute(solutionProgram, VList(GS), VList(US)) ~> REST
```

terminates normally through the modeled rules, it reaches

```text
VList(expected(GS,US)) ~> REST
```

The exact submitted translated AST is the value of `solutionProgram`. For
equal-length `VInt` lists, `expected` is componentwise absolute difference.
Thus the theorem specializes to the prompt's intended integer examples and
domain.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, reachability logic, and `domains.md` built-ins | all builds, executions, and proofs | Standard low-level trusted computing base; acceptable and explicitly versioned. |
| Trusted `/reference/py2mpy.py` | Python-source-to-AST identity | The translator itself is trusted input; byte identity proves only that the submitted `.mpy` is its output. |
| `solutionProgram` external-file bridge | real-program pinning and the entry proof | Ground K equality from exact `.mpy` bytes plus source mutation sensitivity makes this acceptable; it does not prove correctness by itself. |
| Reviewer static audit of generated semantics | bridge from K execution to the target Python subset | Necessary because generated mode has no reference semantics. All intended-path rules were checked; no proof-local oracle exists. |
| Mathematical reading of `expected` as absolute difference on equal `VInt` lists | bridge to natural-language postcondition | Elementary and supported by branch tests, but not a separate K theorem about the trusted canonical implementation. This is an informal intent bridge. |
| Finite differential and K/Python tests | empirical support for implementation and semantic bridges | Strong finite evidence (120,609 Python pairs; nine K/Python cases), not universal proof. |
| Unbounded integers, unbounded abstract call stack, and absence of Python resource exceptions | large-input behavior | Concerning but acceptable only for partial correctness. Real CPython `RecursionError` is explicitly excluded from the normal-return theorem. |
| Off-domain helper totalizations and unrestricted entry claim | unequal, Boolean, nested-list, or otherwise invalid inputs | Concerning. The proof must not be reported as real-Python correctness for these extra formal states. |

There are no opaque symbols, unconstrained result-bearing primitives, empirical
oracles used inside the proof, assumed helper claims, or proof-local operational
bridges. Candidate `PROOF.md` is absent and was not needed; candidate logs,
traces, and reported `#Top` were not treated as proof evidence.

### Decision

- Dynamic reconstruction: pass.
- Real-program identity and body sensitivity: pass.
- Result constraint and fresh non-vacuity: pass.
- Static soundness on the intended equal-length integer domain: pass.
- Natural-language/real-Python adequacy: concern due the unstated formal domain,
  totalized off-domain operations, numeric-type scope, and CPython recursion
  resources.
- Evidence auditability: pass, with failed reviewer attempts preserved and
  excluded rather than hidden.

The limitations prevent `PASS`, but none makes a false normal-return result
provable for the intended equal-length integer inputs. The reconstructed proof
therefore remains legitimate partial-correctness evidence.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
