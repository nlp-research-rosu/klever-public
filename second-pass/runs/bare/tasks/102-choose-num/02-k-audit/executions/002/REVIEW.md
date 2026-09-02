# Independent adversarial audit: 102-choose-num

The candidate contains a legitimate partial-correctness proof of the submitted
generated program over the intended domain of positive integer endpoints. I
rebuilt both semantics and proof definitions from source, proved each claim
independently, mechanically pinned the theorem term to the trusted-translator
output, reviewed every local rule, and obtained meaningful failures from both a
body mutation and a false postcondition.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. I read
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all required generation records, the optional
`usage.json`, the complete 132-record structured trace, and the generation
output log. These records were treated only as historical claims.

The integrity gate passed:

- `/audit-campaign-lock.json` is a real file, its JSON object exactly equals
  the `audit_campaign` block, and its independently computed SHA-256 is the
  recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every record required by `legacy-selected-stage1` is present, readable, and
  non-symlinked. Historical `runtime-metrics.json` is not required for this
  layout. `usage.json` is present and was inspected.
- No linked or unsupported entry occurs below `/candidate`, `/reference`, or
  `/generation-evidence`.
- All independently computed file hashes match the corresponding values in
  `/audit-input.json`, `/generation-result.json`, and
  `/generation-evidence/invocation.json`, including the sole JSONL trace.
- The independently recomputed pipeline tree digest of `/candidate` is
  `16f74ef009145081c921bec498a10a3da9131a76862c77b99adf98ec85997397`,
  exactly the retained workspace digest in both `invocation.json` and
  `generation-result.json`. The trace-tree digest is
  `db7313014ab547a257db30a683464835f1ec1bae56228f93eef95da8d00bdde8`,
  exactly `usage.json`'s source trace digest.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  `/reference` copies.
- As required for generated semantics, `/reference/reference-semantics` does
  not exist. I did not search for or use a hidden baseline.

The generation log contains earlier failed proof attempts and a final `#Top`;
none was reused. Evidence:
[`provenance_check.py`](evidence/provenance_check.py) and
[`01-provenance.log`](evidence/01-provenance.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for positive integer endpoints `x` and `y`, return the
greatest even integer in the inclusive interval `[x,y]`, or `-1` if none
exists. The trusted canonical implementation makes the intended integer
endpoint interpretation explicit through integer parity and the four cases
`x>y`, even `y`, odd singleton, and odd `y` with room below it.

Candidate `solution.py` implements those same cases as a nested conditional
expression:

```python
return -1 if x > y else (y if y % 2 == 0 else (-1 if x == y else y - 1))
```

Running the trusted `/reference/py2mpy.py` against the copied solution exited
0. The regenerated file and submitted `solution.mpy` are byte-identical with
SHA-256
`7757e383294924605e9de6a6b1ca9a4f90bf92d041237aaea0b0e36cc3b1f754`.
See [`02-translation-identity.log`](evidence/02-translation-identity.log).

The independent differential test imported both trusted canonical and
candidate entry points and also used a separate arithmetic oracle. It covered
both documented examples, smallest positive values, empty and singleton
boundaries, every branch, exhaustive pairs `1..128`, 1,024 deterministic
generated pairs up to `10^12`, and arbitrary-precision cases. All 17,412 unique
cases matched; every branch was exercised and mismatch count was zero. See
[`differential_test.py`](evidence/differential_test.py) and
[`03-differential.log`](evidence/03-differential.log). This finite test supports
fidelity but is not used as the universal proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`; no candidate cache or
compiled definition was copied. The independently installed K toolchain is
version 7.1.293.

Fresh builds:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
# exit 0

kompile semantic.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-kompiled
# exit 0
```

Logs:
[`05-kompile-concrete.log`](evidence/05-kompile-concrete.log) and
[`06-kompile-proof.log`](evidence/06-kompile-proof.log).

Fresh LLVM execution used terms generated from the submitted constructor tree.
Eight runs covered all four branches, both prompt examples, boundaries, and an
arbitrary-precision case. Every `krun` exited 0 and its `VInt` result equaled
both Python implementations. See
[`concrete_semantics_test.py`](evidence/concrete_semantics_test.py) and
[`07-concrete-execution.log`](evidence/07-concrete-execution.log). The preserved
`07-concrete-execution-attempt1-reviewer-parser-error.log` records an initial
reviewer-regex error: all K runs had already exited 0 with correct visible
values, but the checker accidentally searched for a literal `\s`. The corrected
reviewer parser was rerun successfully.

The unmodified aggregate proof command exited 0 and printed `#Top`:

```text
kprove spec.k --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC
```

See [`08-kprove-positive.log`](evidence/08-kprove-positive.log). I also copied
the same eight claims into a labeled inspection spec without changing any
precondition or postcondition and ran each separately. All four exact-result
claims and all four contract claims exited 0 and printed `#Top`; see
[`spec-positive-labeled.k`](evidence/spec-positive-labeled.k) and
[`09-kprove-individual-claims.log`](evidence/09-kprove-individual-claims.log).

## 4. Adequacy and real-program pinning

The four exact-result preconditions and postconditions are:

1. `X>0`, `Y>0`, `X>Y`: execution returns `-1`.
2. `X>0`, `Y>0`, `X<=Y`, even `Y`: execution returns `Y`.
3. `X>0`, `Y>0`, `X<Y`, odd `Y`: execution returns `Y-1`.
4. `X>0`, `Y>0`, `X=Y`, odd `Y`: execution returns `-1`.

The four remaining claims use the identical precondition partition and require
the result to make `chooseNumContract(X,Y,R)` reduce to true. That predicate
requires either the sentinel exactly when the interval has no even member, or
an in-range even result whose next even successor is above `Y`. For integer
endpoints this is equivalent to greatest-even maximality.

The partition is mutually exclusive and exhaustive for positive integers:
first split on `X>Y`; in the nonempty case split on parity of `Y`; for odd `Y`,
split on `X<Y` versus `X=Y`. It is neither a finite-size restriction nor a
bounded unrolling. K `Int` also preserves Python's unbounded integer model.

Each precondition is satisfiable. Ground witnesses are `(13,12)`, `(1,2)`,
`(2,3)`, and `(3,3)` respectively. Substitution yields `-1`, `2`, `2`, and
`-1`; the K runs and both Python functions agree, and each contract predicate
is true. See
[`claim_witness_check.py`](evidence/claim_witness_check.py) and
[`16-claim-witnesses.log`](evidence/16-claim-witnesses.log).

The `<k>` cell executes `Run(chooseNumProgram,Int(X),Int(Y))`.
`chooseNumProgram` is a nullary definitional function whose right-hand side is
the full `Module(FuncDef("choose_num",Params("x","y"),Return(...)))` constructor
tree. To check this mechanically, I compiled an inspection definition exposing
`VERIFICATION` syntax, reduced both the submitted `solution.mpy` and the
`chooseNumProgram` term, and compared normalized KORE. The files are
byte-identical with SHA-256
`574cc8c798a6cd7ab5a2b52038e5ef9408729490e7c5093ff159cd0c6283ce71`.
See [`10-program-pinning.log`](evidence/10-program-pinning.log). The preserved
first attempt failed only because the ordinary proof definition exports
`MPY-SYNTAX`, which intentionally cannot parse the verification-only macro as
an external program; the separate inspection build corrected that parser scope.

Finally, changing the constructor actually executed by the claims from `y-1`
to `y-2` built successfully and made the original proof fail on the residual
`Y-2 = Y-1`. This is genuine body sensitivity, not an edit to an ignored
external file. See
[`verification-body-mutant.k`](evidence/verification-body-mutant.k),
[`12-body-mutation-build.log`](evidence/12-body-mutation-build.log), and
[`13-body-mutation-proof.log`](evidence/13-body-mutation-proof.log).

## 5. Rule-by-rule static soundness review

[`11-static-inventory-source.log`](evidence/11-static-inventory-source.log)
records the source inventory. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `owise`, `anywhere`, macro, or
opaque declarations. No generated helper K files exist.

Local syntax and configuration inventory:

- `Program` has `Module(Stmts)` and the explicit test harness
  `Run(Program,Expr,Expr)`.
- `Stmts` and `Strings` are K lists. `Stmt` has `FuncDef` and `Return`;
  `Params` carries the parameter strings.
- `Expr` has `Int`, `Bool`, `Name`, `UnaryOp`, `BinOp`, `Compare`, and
  `IfExp`; `CmpOp` carries an operator string and comparator.
- Runtime syntax is `VInt`/`VBool` and
  `emptyEnv`/`bind(Env,String,Val)`. The configuration contains only `<k>`,
  which is sufficient because this exact function is pure and has no heap,
  assignment, output, allocation, exceptions, or mutable state.
- Verification adds `chooseNumProgram`, `noEvenInRange`,
  `chooseNumContract`, and the continuation item `checkChooseNum`.

Every construct in `solution.mpy` maps to the declarations above:
`Module`, one `FuncDef`, two `Params`, one `Return`, three `IfExp` nodes,
comparisons `>` and `==`, names `x` and `y`, integer literals, unary minus,
modulo, and subtraction. The unused `Bool` constructor is harmless; missing
rules for unused Python constructs are permitted in generated-semantics mode.

All 22 local rules were reviewed:

- `lookup` hit returns the nearest binding; its miss rule recurses only when
  the strings differ. The rules are disjoint, and for the exact environment
  they resolve `y` immediately and `x` after one skip.
- `negate`, `subtract`, and `modulo` implement integer unary minus,
  subtraction, and modulo. The only divisor executed is literal `2`, so no
  zero-divisor behavior is abstracted.
- The two `compare` equations implement `>` and `==` on `VInt`. Their operator
  literals are disjoint and are exactly the operators used.
- `truth(VBool(B)) => B` is the standard guard projection.
- The nine `eval` equations cover integer and boolean literals, names, unary
  minus, subtraction, modulo, comparison, and both conditional outcomes.
  Constructor/operator patterns are disjoint. The `IfExp` guards are logical
  complements after a boolean condition is evaluated, and only the selected
  branch is evaluated, matching Python conditional-expression control.
- The single operational `Run` rule matches exactly one two-parameter function
  with a one-return body, binds the two arguments in parameter order, evaluates
  that body, and preserves the continuation. Although deliberately minimal and
  broader in its unused function-name metavariable, on the exact pinned
  single-function module it is equivalent to invoking that sole function.
  There are no omitted observable cells or abrupt effects for this pure body.
- `chooseNumProgram` is a complete equation for its nullary symbol and expands
  to the exact trusted-translator term. It names rather than summarizes or
  bypasses the body.
- `noEvenInRange(X,Y)` expands to `X>Y` or an odd singleton. This equation is
  true for every integer interval: any non-singleton nonempty interval contains
  two consecutive integers and hence an even integer.
- `chooseNumContract` expands to the sentinel case or to in-range evenness plus
  `Y<R+2`. For an even `R`, `R+2` is its next even successor, so the latter
  condition is exactly maximality.
- `checkChooseNum` runs only after a `VInt` has been produced, computes that
  predicate, and preserves any following continuation. It neither chooses nor
  fabricates the program result.

There is no program-derived opaque result, unconstrained oracle, smuggled task
answer, overlapping false equation, totalization assumption, execution-bypass
bridge, or fabricated behavior for a used construct. Consequently there is no
unsound-rule allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I ignored the candidate's lack of a mutation artifact and authored
[`spec-vacuity-auditor.k`](evidence/spec-vacuity-auditor.k). It changes the
even-upper exact result from `Y` to `Y+1`. The precondition is satisfiable at
`X=1,Y=2`, where actual execution returns `2` and the mutation demands `3`.

The mutated spec dry-run exited 0, establishing successful parsing and KORE
generation; see [`14-vacuity-dry-run.log`](evidence/14-vacuity-dry-run.log).
The real proof then exited 1 with `WarnStuckClaimState`, an implication-check
failure, final `<k> VInt(Y) </k>`, and the unmet equality `Y = Y+1`. This is the
expected reachable result obligation, not a parser error, timeout, or unrelated
crash. See [`15-vacuity-proof.log`](evidence/15-vacuity-proof.log).

## 7. Proven versus assumed accounting

What is machine-checked: under the local generated semantics, for all positive
K integers `X,Y`, evaluation of the exact submitted constructor program returns
the branch-specific values above; those values also satisfy the encoded
greatest-even contract. The claims are result-constraining and discriminate
against both an executed-body error and an off-by-one postcondition.

Trust and assumption ledger:

- K 7.1.293, its Haskell/LLVM backends, and the imported `INT`, `BOOL`, and
  `STRING` builtins are trusted primitives. They affect arithmetic, strings,
  guards, and proof execution. This is the ordinary K trust boundary.
- The trusted CPython-AST translator is outside the theorem. Byte identity of
  its regenerated output supplies the source-to-constructor bridge.
- The generated semantics is not externally blessed. Its complete used subset
  was audited above and dynamically compared against two independent Python
  executions on representative normal, boundary, branch, and large inputs.
  Testing is finite supporting evidence; rule-by-rule semantics review and the
  symbolic K proof carry the universal argument.
- The source phrase “positive numbers” is interpreted as positive integers.
  This is supported by the requested even-integer operation and by the trusted
  canonical implementation's parity case split. The formal domain is
  unbounded, not finitely narrowed.
- The elementary equivalence between the encoded successor condition and
  greatest-even maximality is an ordinary mathematical intent bridge. It is
  exact for integer intervals and introduces no unproved result-bearing symbol.
- No opaque symbol, empirical oracle, external function contract, auxiliary
  lemma, loop invariant, simplification axiom, or termination assumption is
  needed. The theorem is partial-correctness as requested, although this finite
  expression also concretely terminates on the formal domain.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
reproducibility) all pass. The candidate's historical `#Top` and prose were not
used as proof evidence; only the fresh reconstruction was accepted.

VERDICT: PASS
LEGITIMACY: LEGIT
