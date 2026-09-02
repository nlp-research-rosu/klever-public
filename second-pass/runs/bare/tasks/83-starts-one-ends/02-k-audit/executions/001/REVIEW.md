# Independent adversarial review: 83-starts-one-ends

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness proof of the submitted generated program for every positive integer input. I independently rebuilt both K definitions, ran each positive entry claim separately, checked concrete execution against Python, verified exact program pinning, audited every local rule, changed the program body, and created a fresh false postcondition. The positive claims closed; both negative probes failed for the expected result mismatch.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, for two non-material limitations: the K theory defines the desired count by elementary inclusion-exclusion but does not formalize decimal strings/sets and prove that cardinality bridge inside K, and the generated semantics has one deliberately broad expression-statement discard rule whose fidelity was established only for the actual docstring occurrence. Neither limitation enables a false conclusion for the fixed submitted program on its positive-integer domain.

## 1. Input and provenance integrity

### Trusted-mount boundary

This is `GENERATED_SEMANTICS`. `/reference/reference-semantics` is absent as required. There is therefore no hidden or inferred reference semantics in this audit. The first check in [stage1-provenance.log](evidence/stage1-provenance.log) exited 0. No infrastructure breach occurred.

### Untrusted generation records

I read all of:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- all 6,663 lines/250,599 bytes of `/candidate/codex-output.log`
- all 141 JSONL records/266,771 bytes of the structured trace at `/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-55-05-019f8977-00e7-74e3-8113-548ceabd44ea.jsonl`

They claim a bare, no-supplied-semantics generation, exit 0, concrete results `1, 18, 180, 18000`, and a combined `#Top`. Those statements were treated only as claims. The complete bounded extraction is in [stage1-untrusted-records.log](evidence/stage1-untrusted-records.log); the trace had no malformed JSON lines.

### Integrity results

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256 `501c2ec4...a8391`, `cmp` exit 0).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256 `406485ea...db16`, `cmp` exit 0).
- Required regular, non-symlink artifacts are present: `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, `prove.sh`, the four named provenance records, and the structured trace.
- `find /candidate -type l` found no symlinks. No required artifact is missing, changed, mistyped, or symlinked.
- The only candidate-local K source files are `semantic.k`, `verification.k`, and `spec.k`; there are no undisclosed helper K files.
- Extra candidate artifacts are `proof-output.txt`, `semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, and generation logs/traces. They are not source-integrity failures, but none was trusted or used in reconstruction.

Hashes, type checks, commands, and statuses are in [stage1-provenance.log](evidence/stage1-provenance.log). Only the source artifacts were copied to `/tmp/audit-work/review-83`; candidate compiled definitions and caches were not copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a positive integer `n`, return the number of `n`-digit positive decimal integers whose first digit is `1` or whose last digit is `1`.

The trusted canonical implementation is:

- `1` when `n = 1`;
- `18 * 10 ** (n - 2)` when `n > 1`.

For `n > 1`, inclusion-exclusion gives:

- first digit fixed to `1`: `10^(n-1) = 10 * 10^(n-2)`;
- last digit fixed to `1`: `9 * 10^(n-2)`;
- both fixed to `1`: `10^(n-2)`;
- union: `(10 + 9 - 1) * 10^(n-2) = 18 * 10^(n-2)`.

`/candidate/solution.py` implements exactly these two branches. The extra `else` is behaviorally immaterial.

### Trusted translation

I ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/review-83/solution.py > /tmp/audit-work/review-83/regenerated-solution.mpy
cmp -s /tmp/audit-work/review-83/regenerated-solution.mpy /tmp/audit-work/review-83/solution.mpy
```

Both commands exited 0. The regenerated and submitted `.mpy` files are byte-identical. See [stage2-fidelity.log](evidence/stage2-fidelity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports `/reference/canonical.py` and the scratch copy of the generated `solution.py`. The trusted prompt has no documented examples. The test therefore covered:

- the `n = 1` singleton branch;
- the adjacent `n = 2` branch boundary;
- every `n` from 1 through 30;
- fixed ordinary/large representatives through 100;
- deterministic seeded generated values through 120;
- 70 distinct positive inputs in total;
- an independent brute-force enumeration of all `n`-digit integers for `n = 1..5`.

There were zero canonical/generated mismatches, and the brute-force counts were `1, 18, 180, 1800, 18000`. An “empty” value is inapplicable to this scalar integer signature. Inputs `0, -1, -2` were recorded only as out-of-domain diagnostics and did not affect the verdict. Exact inputs and results are in [stage2-fidelity.log](evidence/stage2-fidelity.log), exit 0.

## 3. Clean proof reconstruction

K version `v7.1.293` was available independently. The fresh output paths did not exist before compilation. I used:

```text
kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition fresh-semantic-kompiled
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled
```

Both exited 0 from `/tmp/audit-work/review-83`.

### Generated-semantics concrete reconstruction

Fresh LLVM execution of the actual regenerated/submitted `solution.mpy` produced:

| Input | K result | independent Python result | Status |
|---:|---:|---:|---|
| 1 | 1 | 1 | match |
| 2 | 18 | 18 | match |
| 3 | 180 | 180 | match |
| 5 | 18000 | 18000 | match |
| 10 | 1800000000 | 1800000000 | match |

These include both branch boundaries and normal values. Every `krun` exited 0 with `.K`, `control normal`, and the stated concrete result.

### Positive claims

I ran each target claim independently:

```text
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.positive-n-one
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.positive-n-gt-one
```

Each printed exactly `#Top` and exited 0. A combined all-claims run also printed `#Top` and exited 0. The complete commands, configurations, outputs, and statuses are in [stage3-reconstruction.log](evidence/stage3-reconstruction.log). This is independent reconstruction; no candidate definition, cache, saved `proof-output.txt`, or prior `#Top` was used.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.positive-n-one` starts from the exact initialized machine and the literal submitted program followed by `entry("starts_one_ends", 1)`. It requires execution to consume the complete `<k>` computation, register the exact function body, bind `"n"` to `1`, restore normal control, and change `noResult` to `result(qualifyingCount(1))`.

`SPEC.positive-n-gt-one` has the same exact initialized program and state, uses symbolic integer `N`, and requires `N > 1`. It requires the corresponding exact final function cell, `"n" |-> N`, normal control, and `result(qualifyingCount(N))`.

Together, the hard-coded `1` claim and the guarded `N > 1` claim partition exactly the positive integers.

### Program identity and control-flow alignment

The `<k>` term in both claims is the complete constructor tree from `solution.mpy`: `Module`, the exact function name and parameter, the exact docstring, the `n == 1` test, `return 1`, and `return 18 * 10 ** (n - 2)`. The tree and literal values are not abstracted by a function name or oracle. Trusted retranslation already established byte identity of that submitted term.

There are no loop/helper reachability claims. The proof follows the real module-registration, entry, statement sequencing, branch, expression, return, and call-completion rules. The final function, environment, control, and result cells are all constrained; there are no right-only existential result variables, omitted result cells, tautologies, or one-way implications standing in for equality.

### Satisfiable witnesses and concrete substitutions

[adequacy-ground.k](evidence/adequacy-ground.k) replaces the helper-valued postconditions with exact integers:

- `n = 1` satisfies the first entry state and requires `result(1)`;
- `n = 2` satisfies `N > 1` and requires `result(18)`.

Both ground claims printed `#Top` and exited 0. [ground_witness.py](evidence/ground_witness.py) separately evaluated the claimed inclusion-exclusion definition, trusted canonical Python, and generated Python; all three returned `1` at `n = 1` and `18` at `n = 2`. See [stage4-adequacy.log](evidence/stage4-adequacy.log).

The separate body-sensitivity test in Stage 5 further confirms that the literal body matters to closure.

## 5. Rule-by-rule static soundness review

The full numbered sources and machine-extracted declaration inventory are preserved in [stage5-static-extract.log](evidence/stage5-static-extract.log). An initial reviewer-only regex error is transparently retained in [stage5-static-extract-attempt1.log](evidence/stage5-static-extract-attempt1.log); it did not invoke or assess the candidate proof.

### Exhaustive local syntax/configuration inventory

`semantic.k` contains the following local productions:

| Sort | Productions | Role and assessment |
|---|---|---|
| `Pgm` | `Module(Stmts)` | Exact translator constructor used. |
| `Stmts` | `List{Stmt, ""}` | Juxtaposed translator statement list. |
| `Stmt` | `FuncDef(String, Params, Stmts)`; `Return(Expr)`; `If(Expr, Stmts, Stmts)`; `Expr(Expr)` | Exactly the four statement constructors in the submitted term. |
| `Params` | `Params(String)` | Exact one-parameter function shape. |
| `Expr` | `Int(Int)`; `Str(String)`; `Name(String)`; `BinOp(String, Expr, Expr)`; `Compare(Expr, CmpOp)` | Covers every expression constructor in the submitted term. |
| `CmpOp` | `CmpOp(String, Expr)` | Covers the single `==` comparator. |
| `FunctionValue` | `noFunction`; `function(String, String, Stmts)` | Internal single-function registry, sufficient for this one-function module. |
| `Control` | `normal`; `returned` | Tracks normal versus abrupt return control. |
| `Result` | `noResult`; `result(Int)` | Makes the observable integer result explicit. |
| `KItem` | `exec(Stmts)`; `entry(String, Int)`; `endCall` | Internal execution/call continuations. |
| `Int` extension | `evalInt(Expr, Map) [function]` | Partial pure evaluator; all target uses have equations. |
| `Bool` extension | `evalBool(Expr, Map) [function]` | Partial pure evaluator for the target equality. |

The `[symbol(...)]` attributes on translator constructors only assign stable K labels; they assert no equations. `verification.k` adds five `[function]` `Int` symbols: `decimalMiddles`, `startsWithOne`, `endsWithOne`, `startsAndEndsWithOne`, and `qualifyingCount`.

There are no local `[total]`, `[functional]`, `[simplification]`, `[priority]`, `[owise]`, `[concrete]`, `[symbolic]`, `[anywhere]`, macro, alias, fresh, or opaque declarations. There are no priority rules, simplification rules, proof-local operational bridges, circularities, or helper claims. The five verification functions and two semantic evaluator functions are ordinary partial K functions; unmatched applications remain visibly irreducible.

The configuration has exactly the required cells: `<k>`, one `<function>` registry, local `<env>`, `<control>`, and `<result>`. There is no heap, allocation, I/O, or exception cell because the submitted positive-domain program uses none of those behaviors.

### Syntactic-construct coverage map

| Submitted construct | Declaration | Behavior used |
|---|---|---|
| `Module` | `Pgm` | module-to-`exec` rule |
| juxtaposed function body / `.Stmts` | `Stmts` | normal sequencing, empty completion, returned discard |
| `FuncDef` | `Stmt` | register exact name, parameter, body |
| docstring `Expr(Str(...))` | `Stmt`, `Expr` | discard the pure constant expression statement |
| `If` | `Stmt` | complementary `evalBool` guards |
| `Return` | `Stmt` | evaluate integer, set result and returned control |
| `Compare(Name("n"), CmpOp("==", Int(1)))` | `Compare`, `Name`, `CmpOp`, `Int` | map lookup, integer literal, integer equality |
| `BinOp("*", ...)` | `BinOp` | K integer multiplication |
| `BinOp("**", ...)` | `BinOp` | K integer exponentiation |
| `BinOp("-", ...)` | `BinOp` | K integer subtraction |

All used constructors have a declaration and an applicable rule path. Unknown operator strings or unsupported expression shapes get stuck rather than receiving fabricated results.

### Exhaustive semantic-rule inventory

| ID | Rule | Static assessment |
|---|---|---|
| S1 | `Module(SS) => exec(SS)` | Truthful module sequencing for this function-only module. |
| S2 | `exec(.Stmts) => .K` | Correct statement-list completion. It overlaps S4 only when control is returned and the list is empty; both right sides are `.K`. |
| S3 | `exec(S SS) => S ~> exec(SS)` when `control = normal` | Correct left-to-right statement sequencing. |
| S4 | `exec(_SS) => .K` when `control = returned` | Correctly discards the remaining statements after return. Guard is disjoint from S3. |
| S5 | `FuncDef(F, Params(P), BODY)` registers `function(F,P,BODY)` | Correct for the actual one-function, one-parameter module. It preserves the literal body. |
| S6 | `entry(F,N)` selects the registered matching `F`, installs `P |-> N`, and schedules `BODY ~> endCall` | Binding is pinned by the function-cell pattern, not by an unguarded textual name. Exact target call has one integer argument. |
| S7 | `endCall` changes `returned` back to `normal` | Correct call-harness completion after the result has been stored. |
| S8 | `Expr(_E) => .K` | Correct for the only reachable occurrence, the constant-string function docstring. Scope limitation discussed below. |
| S9 | `If(COND,THEN,_) => exec(THEN)` when `evalBool` is true | Correct branch selection. |
| S10 | `If(COND,_,ELSE) => exec(ELSE)` when `notBool evalBool` | Correct complementary branch; no overlap with S9 for a reduced Bool. |
| S11 | `Return(E)` sets `returned` and `result(evalInt(E,ENV))` from normal/no-result state | Correct for the target's pure, total-on-domain integer expressions; no continuation is silently skipped beyond S4's ordinary return behavior. |
| S12 | `evalInt(Int(I),_) => I` | Integer literal identity. |
| S13 | `evalInt(Name(X),(X |-> I) M) => I` when `X` is not in `keys(M)` | Unique map binding lookup; target environment is exactly `"n" |-> N`. |
| S14 | `evalInt(BinOp("+",A,B),ENV)` | Truthful unbounded integer addition; unused by this program. |
| S15 | `evalInt(BinOp("-",A,B),ENV)` | Truthful unbounded integer subtraction; target computes `N - 2`. |
| S16 | `evalInt(BinOp("*",A,B),ENV)` | Truthful unbounded integer multiplication. |
| S17 | `evalInt(BinOp("**",A,B),ENV)` | Truthful integer exponentiation on the reachable domain: the branch is executed only for `N > 1`, hence exponent `N-2 >= 0`. |
| S18 | `evalBool(Compare(A,CmpOp("==",B)),ENV)` | Truthful integer equality for the target guard. |

The recursive expression equations need no source evaluation-order mechanism because all modeled target operands are pure and side-effect free. The translator's nesting already fixes Python precedence: subtraction is inside exponentiation, which is inside multiplication.

S8 is broader than its actual justification: for example, another program containing `Expr(Name("missing"))` would be silently discarded in K while Python would raise `NameError`. That is a concrete broader-language fidelity witness, but it is not reachable for any positive input to the fixed submitted program, whose only `Expr` statement is the literal docstring. Under the required decision rule, I do **not** label S8 materially unsound on the intended domain; I record it as a generated-semantics scope/evidence limitation. Narrowing it to `Expr(Str(_))` would improve reuse without changing this proof.

### Exhaustive verification-rule inventory

| ID | Rule/domain | Classification and assessment |
|---|---|---|
| V1 | `decimalMiddles(K) => 10 ^Int K`, `K >= 0` | Definitional summary for the number of length-`K` decimal strings. Guard covers every dependent call. |
| V2 | `startsWithOne(N) => 10 * decimalMiddles(N-2)`, `N > 1` | Truthful count `10^(N-1)` with first digit fixed. |
| V3 | `endsWithOne(N) => 9 * decimalMiddles(N-2)`, `N > 1` | Truthful count: nine nonzero leading choices and arbitrary middle digits. |
| V4 | `startsAndEndsWithOne(N) => decimalMiddles(N-2)`, `N > 1` | Truthful intersection count. |
| V5 | `qualifyingCount(1) => 1` | Truthful singleton case. |
| V6 | `qualifyingCount(N) => startsWithOne(N) + endsWithOne(N) - startsAndEndsWithOne(N)`, `N > 1` | Truthful inclusion-exclusion; algebraically equals the program's `18 * 10^(N-2)`. |

These equations are disjoint or agreeing on all overlaps: V5's ground `1` does not overlap V6's `N > 1`; all dependent calls from V6 satisfy V1–V4 guards. Recursive descent is finite (V6 expands through V2–V4 to V1 and built-ins). No function is asserted total outside the positive domain. These helpers occur only in the destination postcondition; they do not replace or accelerate source execution. There is no program-derived opaque value, oracle, circular execution/spec symbol, or task-answer operational rewrite.

`spec.k` has exactly two reachability claims, inventoried in Stage 4. It has no ordinary or simplification rules.

### State, overlap, and body sensitivity

For the actual program, state changes are limited and explicit: function registration, local parameter binding, return control, and result storage. S3/S4 guards enforce return control; S9/S10 guards partition equality; binding selection is structural; all other cells are either explicitly rewritten or framed.

To test body sensitivity, [stage5-body-sensitivity.sh](evidence/stage5-body-sensitivity.sh) changed both occurrences of the literal program coefficient from `18` to `19` while retaining the concrete `n = 2` result obligation `18`. The mutation parsed (`--dry-run` exit 0), then `kprove` exited 1 with `WarnStuckClaimState` and a residual `result(19)`. See [body-sensitivity.k](evidence/body-sensitivity.k) and [stage5-body-sensitivity.log](evidence/stage5-body-sensitivity.log). This shows the proof executes and depends on the real body.

No rule in the intended-domain proof admits a concrete or symbolic false conclusion witness. Accordingly, no rule is labeled materially unsound.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was trusted.

I created [spec-vacuity.k](evidence/spec-vacuity.k) fresh by changing the result obligations to:

```text
result(qualifyingCount(1) +Int 1)
result(qualifyingCount(N) +Int 1)
```

The program, execution configuration, and `N > 1` precondition remained unchanged. For the satisfying witness `N = 2`, the real/canonical/generated result is `18`, while the mutated obligation is `19`.

The exact validation sequence was:

```text
kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.positive-n-gt-one --dry-run
kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.positive-n-gt-one
```

The dry run exited 0, proving the mutation parsed and built. The proof exited 1 with `WarnStuckClaimState`; its residual explicitly compared the mutated inclusion-exclusion value plus 1 against `18 * 10^(N-2)` under `N > 1`. This is the expected unmet result obligation, not a parser error, missing import, timeout, unreachable mutation, or unrelated crash. Full diff, commands, statuses, and residual are in [stage6-nonvacuity.log](evidence/stage6-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the reviewed generated MPY semantics and K's built-in mathematical integer/Boolean/map operations:

- from the exact initialized configuration containing the exact submitted `solution.mpy`;
- for the fixed input `1`, or for every symbolic integer `N > 1`;
- if execution terminates (the Kit's partial-correctness interpretation);
- the computation is consumed, the exact source function remains registered, the parameter environment contains the input, control is normal, and the result equals `qualifyingCount(input)`;
- the reviewed equations reduce `qualifyingCount(1)` to `1` and, for `N > 1`, to `18 * 10^(N-2)`.

The proof does not merely show that some result exists. It constrains the exact integer, and both body and postcondition mutations are rejected.

### Trust ledger

| Boundary | Dependents/effect | Status |
|---|---|---|
| K compiler, Haskell/LLVM backends, reachability engine | Parsing, concrete execution, symbolic closure | Necessary low-level trusted computing base; independently rebuilt with installed K `v7.1.293`. |
| K built-ins `INT`, `BOOL`, `MAP` (`+Int`, `-Int`, `*Int`, `^Int`, equality, map lookup/keys) | Branch choice and every returned value | Acceptable fixed primitives outside the program theorem. Reachable exponent is nonnegative and Python/K both use unbounded mathematical integer behavior for these tested operations. |
| Trusted `/reference/py2mpy.py` | Python-source-to-constructor bridge | Explicitly trusted by the audit problem; candidate copy matches it and fresh output is byte-identical. |
| Generated `semantic.k` | Meaning of the submitted `.mpy` term | Not assumed: rebuilt, concretely checked, exhaustively reviewed, and body-sensitivity tested. Its only documented reuse limitation is broad S8. |
| Verification helpers V1–V6 | Destination value and natural-language count | Not opaque and not assumed as an oracle: all have guarded equations and an elementary inclusion-exclusion derivation. |
| Informal statement that V1–V6 are the cardinality of the decimal-number property | Bridge from algebraic helper to human-facing intent | Mathematically compelling and independently brute-forced for `n=1..5`, but not represented as sets/decimal strings and proved as a K cardinality theorem. This is the principal `CONCERNS` limitation. |
| `/reference/canonical.py` and CPython differential execution | Program/intent corroboration on finite inputs | Trusted oracle only for testing. Seventy differential inputs and five brute-force cases support the bridge; they are not substituted for the universal K proof. |
| Candidate logs, trace, `proof-output.txt`, and compiled definitions | None in the audit conclusion | Untrusted evidence only; excluded from reconstruction. |

There are no opaque symbols, fresh result-bearing values, empirical operational bridges, source-body summaries, proof-local semantic rewrites, or unproved helper reachability claims. The generated semantics excludes general Python exceptions, multiple functions, arbitrary calls, heaps, and side effects; those behaviors are absent from the submitted program on the positive-integer domain.

### Validation gates and decision

- **Gate A — real-program soundness: PASS.** Exact program identity, complete target construct semantics, complete state/result constraint, individual `#Top` runs, satisfiable witnesses, body sensitivity, and false-postcondition rejection all pass.
- **Gate B — intent adequacy: PASS with a documented limitation.** Domain and formula match the trusted prompt/canonical program. The formula-to-decimal-cardinality bridge is elementary but informal rather than an internal K theorem.
- **Gate C — trust/evidence auditability: PASS.** All reviewer artifacts, exact inputs, commands, exit statuses, positive outputs, and expected negative residuals are preserved below `evidence/`.

The limitations do not substitute a program, admit an unconstrained oracle, weaken the result, or enable a false claim for the submitted program. They warrant `CONCERNS`, not `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
