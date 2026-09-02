# Independent adversarial audit: 102-choose-num

## Audit result

The candidate contains a legitimate partial-correctness proof of the submitted
generated program over positive integer inputs. I rebuilt both definitions from
source, executed the generated semantics independently, ran every one of the
eight target claims in isolation, reviewed every local declaration and rule,
and obtained a discriminating failure from a fresh false result mutation. No
candidate-provided compiled definition, cache, `#Top`, trace conclusion, or
prose report was trusted.

The formal result is not obtained through an oracle or execution shortcut.
`chooseNumProgram` expands to the exact constructor tree regenerated from
`solution.py`; that tree is evaluated by the candidate's expression semantics.
The four exact-result claims form an exhaustive partition of all positive
integer endpoint pairs. The four additional claims run the same program before
checking the greatest-even-number predicate.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. The trusted mount
contains only:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

There is no trusted/candidate mode contradiction and hence no infrastructure
breach. K is independently available as version `v7.1.293`; `kompile`,
`kprove`, and Python version checks all exited zero. Exact output is in
[`evidence/stage1-integrity.log`](evidence/stage1-integrity.log).

### Required artifacts and identity

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are all regular files. There are no
candidate symlinks. No required generation artifact is missing or mistyped.
The nested structured trace is present as one regular JSONL file and all 132
records parse successfully.

The candidate prompt and translator are byte-identical to the trusted files:

| Artifact | SHA-256 |
|---|---|
| trusted and candidate `prompt.py` | `3b2e226ef819e4547fbd11a4ee933844a256dcd27e6d79fc1da3d380ff755d18` |
| trusted and candidate `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |

These values also agree with the untrusted `run-input.json` claims. Scratch
copies of all proof sources compare byte-for-byte with the candidate sources.

The candidate has additional `semantic-kompiled/`, `__pycache__/`, and two
handwritten concrete-run inputs. They are extras, not integrity failures, and
none was copied into or used by the reconstruction. There is no candidate
`PROOF.md`; it was not a required generation deliverable and its absence did
not prevent independent auditing.

### Untrusted generation claims

`metrics.json` claims an exit code of zero, and `codex-last.txt`,
`codex-output.log`, and the structured trace claim that one aggregate proof
printed `#Top`. The trace also records intermediate parse/proof failures before
the final artifacts. These records were read only as provenance claims. The
verdict below depends exclusively on the fresh runs recorded by this audit.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

On positive integer endpoints `x` and `y`, the function must return the
greatest even integer in inclusive interval `[x,y]`, or `-1` if the interval
contains no even integer. The trusted canonical implements the exhaustive
cases:

1. `x > y`: return `-1`;
2. `x <= y` and `y` even: return `y`;
3. `x < y` and `y` odd: return `y - 1`;
4. `x == y` and `y` odd: return `-1`.

The prompt says “positive numbers,” while the result is specifically an even
integer and the trusted canonical uses integer parity. The formal and audited
domain is therefore positive integers, which is the coherent benchmark domain.

`solution.py` implements exactly this partition as one conditional expression.
It is a different surface presentation of the canonical branches but not a
material algorithmic divergence.

### Fresh translation identity

The command

```text
python3 /reference/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/regenerated.mpy
```

exited zero. The regenerated file is byte-identical to submitted
`solution.mpy`; both have SHA-256
`7757e383294924605e9de6a6b1ca9a4f90bf92d041237aaea0b0e36cc3b1f754`.
See [`evidence/stage2-fidelity.log`](evidence/stage2-fidelity.log).

### Independent differential testing

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point directly from `/reference/canonical.py` and the
generated entry point from the scratch `solution.py`. It compares both with a
separate endpoint-search contract oracle over:

- both documented examples;
- ten explicit empty, singleton, adjacency, branch-boundary, and large cases;
- every pair `x,y` in `[1,100]`;
- 1,000 deterministic generated pairs in `[1,10^12]`.

There were 11,002 unique cases and zero mismatches. The complete deterministic
input list is [`evidence/differential-inputs.json`](evidence/differential-inputs.json),
SHA-256 `c6c774e83be66d93e3e9810508bc91b6590feda8d73fa5f048204bb7529627dc`.
This is finite bridge evidence only; it is not used as a substitute for the K
proof or the static semantics review.

## 3. Clean proof reconstruction

Only the candidate's source files were copied to `/tmp/audit-work`. Candidate
compiled definitions and caches were neither copied nor referenced.

Two distinct Haskell definitions were freshly built:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile semantic.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited zero. Their main modules are respectively `MPY` and
`VERIFICATION`; their fresh `definition.kore` hashes differ, confirming the
separate concrete/proof builds. Full commands, exit statuses, hashes, and
outputs are in
[`evidence/stage3-reconstruction.log`](evidence/stage3-reconstruction.log).

### Generated-semantics execution

Fresh `Run(Module(...),Int(X),Int(Y))` inputs were created from regenerated
`solution.mpy`, not from candidate concrete-run files. All eight runs exited
zero, consumed the computation, and agreed with both Python implementations:

| Input | Purpose | K/Python result |
|---|---|---:|
| `(12,15)` | prompt example / odd upper endpoint | `14` |
| `(13,12)` | empty interval | `-1` |
| `(13,13)` | odd singleton | `-1` |
| `(12,12)` | even singleton | `12` |
| `(1,2)` | smallest even endpoint | `2` |
| `(2,3)` | odd upper endpoint with room | `2` |
| `(1,1)` | smallest positive boundary | `-1` |
| `(999999999999,1000000000000)` | large boundary | `1000000000000` |

### Positive target proofs

The submitted aggregate command exited zero and printed `#Top`. Because the
candidate claims are unlabeled, I also copied each claim verbatim into a
separate scratch spec module and ran eight independent commands:

```text
kprove spec-NN.k --definition proof-kompiled --spec-module SPECNN
```

For each `NN` from `01` through `08`, `kprove` exited zero and printed `#Top`.
Thus aggregate closure did not hide a failing individual claim.

## 4. Adequacy and real-program pinning

Every claim additionally requires `X>0` and `Y>0`. Their plain-language
preconditions and postconditions are:

| Claims | Additional precondition | Postcondition |
|---|---|---|
| 1 and 5 | `X > Y` | exact result `-1`; respectively contract checker returns true |
| 2 and 6 | `X <= Y` and `Y` even | exact result `Y`; respectively checker returns true |
| 3 and 7 | `X < Y` and `Y` odd | exact result `Y-1`; respectively checker returns true |
| 4 and 8 | `X == Y` and `Y` odd | exact result `-1`; respectively checker returns true |

These guards are satisfiable, pairwise case-separated, and exhaustive over
positive integer pairs. Witnesses `(2,1)`, `(1,2)`, `(2,3)`, and `(1,1)`
satisfy cases 1/5, 2/6, 3/7, and 4/8 respectively. Substitution yields
`-1`, `2`, `2`, and `-1`; both trusted and generated Python implementations
produce those values. Machine-readable witness results are in
[`evidence/stage4-5-static.log`](evidence/stage4-5-static.log).

`chooseNumProgram` is not a free or opaque program variable. The auditor
extracted its complete balanced constructor right-hand side from
`verification.k` and compared its normalized token stream with submitted
`solution.mpy`. Both normalized streams have SHA-256
`c7337330439842b0cfba0b333185fe2606482a45d4ec94a615dfd89b97f61f80`.
The extracted artifact is
[`evidence/extracted-chooseNumProgram.mpy`](evidence/extracted-chooseNumProgram.mpy).

Concrete execution of `Run(chooseNumProgram,Int(12),Int(15))` produces the
same complete configuration as execution of the raw regenerated module:
`<k> VInt(14) ~> .K </k>`. The `Run` rule then evaluates the submitted return
expression through `eval`; it does not replace that expression with the
claimed answer. The exact-result destinations contain `VInt(-1)`, `VInt(Y)`,
or `VInt(Y-1)`, not an unconstrained right-hand variable. The checker claims
place `checkChooseNum` after program execution and require the resulting
Boolean to be exactly true.

There are no helper or loop claims and no circularity that could match
unrelated control flow.

## 5. Rule-by-rule static soundness review

The exhaustive source-level inventory, with domains and adjudications, is
preserved in
[`evidence/rule-inventory.md`](evidence/rule-inventory.md). The source grep and
attribute counts are in
[`evidence/stage4-5-static.log`](evidence/stage4-5-static.log).

### Local syntax, configuration, and attributes

`MPY-SYNTAX` declares `Program` (`Module`, `Run`), statement and string lists,
`Stmt` (`FuncDef`, `Return`), `Params`, `Expr` (`Int`, `Bool`, `Name`,
`UnaryOp`, `BinOp`, `Compare`, `IfExp`), and `CmpOp`.

`MPY` has a single `<k>` cell, values `VInt`/`VBool`, and immutable environment
constructors `emptyEnv`/`bind`. It declares the functions `lookup`, `negate`,
`subtract`, `modulo`, `compare`, `truth`, and `eval`.

`VERIFICATION` declares the functions `chooseNumProgram`, `noEvenInRange`, and
`chooseNumContract`, plus continuation item `checkChooseNum`.

All ten local function declarations have `[function]`. There are no local
`total`, `functional`, `simplification`, `concrete`, `owise`, opaque, priority,
or precedence declarations. There are no helper K files.

### All 18 `semantic.k` rules

1. `lookup` hit returns the latest matching binding: correct.
2. Guarded `lookup` miss descends past a different string key: correct and
   disjoint from rule 1.
3. Integer `negate`: correct.
4. Integer `subtract`: correct.
5. Integer `modulo`: correct for the submitted literal divisor `2`.
6. Integer comparison tag `>`: correct.
7. Integer comparison tag `==`: correct and tag-disjoint from rule 6.
8. `truth(VBool(B))`: correct Boolean unwrapping.
9. Evaluation of `Int`: correct.
10. Evaluation of `Bool`: correct; this expression constructor is unused by
    the submitted program.
11. Evaluation of `Name`: correct lookup; actual names `x` and `y` are bound.
12. Evaluation of unary `-`: correct delegation to rules 3 and recursive eval.
13. Evaluation of binary `-`: correct for pure integer operands.
14. Evaluation of binary `%`: correct for the submitted `% 2`.
15. Evaluation of `Compare`: correct for submitted tags `>` and `==`.
16. True `IfExp` branch: correctly evaluates only `THEN`.
17. False `IfExp` branch: correctly evaluates only `ELSE`; its guard is the
    Boolean complement of rule 16.
18. `Run`: matches the actual sole two-argument function with one
    `Return(E)`, binds both integer arguments, evaluates `E`, and preserves the
    continuation.

No explicit strictness order is declared for recursive pure operands. This
cannot alter submitted-program behavior: the operands have no state, I/O,
allocation, or intended-domain exception, while conditional branches remain
lazy. The one-cell configuration is adequate because the actual function has
no mutable state, heap, output, exceptions, nested calls, or allocation.

`lookup` and the operator functions are intentionally partial outside their
supported forms and are not marked total. Every term reachable from the
submitted program is covered. General Python zero-division and type-error
behavior is not modeled, but the only modulus divisor is literal positive `2`
and all formal arguments are integers. This is a narrower off-program
coverage limitation, not a false rule on the intended domain.

The `Run` driver ignores the spelling of the sole function name. It is a
direct-entry driver rather than a general Python name-resolution model; the
actual claim supplies exactly one function and the exact body, so no alternate
binding is selected.

### All 4 `verification.k` rules

1. `chooseNumProgram` is a definitional constant equal to the exact submitted
   constructor tree. It does not summarize the result or bypass execution.
2. `noEvenInRange(X,Y)` is true exactly for an empty integer interval or an
   odd singleton. This is mathematically valid for all K integers.
3. `chooseNumContract(X,Y,R)` is valid: for an even in-range `R`, the next
   possible larger even integer is `R+2`, so `Y<R+2` characterizes maximality;
   the sentinel branch uses rule 2.
4. The checker rule consumes an already computed `VInt(R)`, evaluates rule
   3, and preserves any subsequent continuation. It occurs after rather than
   instead of program execution.

The guard pairs for lookup and conditional selection are disjoint; comparison
and binary-operation rules are tag-disjoint. No priority can preempt the real
execution. No fresh, existential, opaque, or unconstrained symbol influences a
branch, result, state, exception, or postcondition.

I found no materially unsound local rule and therefore make no unsoundness
allegation requiring a false-conclusion witness. The noted missing behavior is
strictly outside the used construct/state set permitted for generated minimal
semantics.

As a separate body-sensitivity check, I changed the real odd branch from
`y-1` to `y-3` in scratch, rebuilt, and reran the original case-3 claim. The
proof exited 1 with `WarnStuckClaimState`, exposing
`Y +Int -3` versus `Y +Int -1`. This confirms that the claim depends on the
program body. See
[`evidence/body-sensitivity.log`](evidence/body-sensitivity.log).

## 6. Fresh non-vacuity test

The fresh mutation is
[`evidence/spec-vacuity-fresh.k`](evidence/spec-vacuity-fresh.k). It retains
the satisfiable even-upper-endpoint precondition but changes the exact result
from `VInt(Y)` to `VInt(Y +Int 2)`.

Witness `X=1,Y=2` satisfies the precondition. Both Python implementations and
fresh K execution return `2`; the mutated destination requires `4`.

The dry-run command parsed and built the mutation successfully and exited zero.
The actual proof command then exited 1, did not print `#Top`, and produced
`WarnStuckClaimState` with the failed implication `Y = Y +Int 2`, followed by
“cannot be rewritten further.” This is the expected unmet result obligation,
not a parse failure, missing import, timeout, or unrelated crash. Commands and
statuses are in
[`evidence/stage6-nonvacuity.log`](evidence/stage6-nonvacuity.log); the raw
residual is
[`evidence/stage6-vacuity-proof.raw.log`](evidence/stage6-vacuity-proof.raw.log).

Two reviewer-harness attempts are separately preserved:
`stage4-5-static-attempt1.log` records an external-parser and regex issue later
corrected, and `body-sensitivity-attempt1.log` records an overly specific log
matcher. Neither was a candidate build/proof failure; the corrected runs exit
zero and retain the underlying raw evidence.

## 7. Proven versus assumed accounting

### What the K reachability proof establishes

Under the freshly compiled semantics, for all K integers `X,Y` with
`X>0` and `Y>0`, terminating execution of the exact submitted translated
program returns:

```text
-1,  if X > Y;
Y,   if X <= Y and Y is even;
Y-1, if X < Y and Y is odd;
-1,  if X = Y and Y is odd.
```

The same execution also makes `chooseNumContract(X,Y,R)` true. By elementary
integer reasoning audited in stage 5, this means `R` is the greatest even
integer in `[X,Y]`, or `-1` exactly when no such integer exists. The claims are
partial-correctness reachability claims; they do not assert behavior outside
their positive-integer preconditions.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K parser/compiler, Haskell backend, reachability logic, and standard `INT`, `BOOL`, `STRING`, and list primitives | All parsing, rewriting, arithmetic, Boolean, and proof closure | Necessary low-level trusted computing base; version and fresh builds recorded. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to the constructor program | Approved trusted input. Fresh byte-identical regeneration pins the submitted `.mpy`. |
| Candidate-generated semantics | Defines execution of the constructor program | Not blindly trusted: every local declaration and rule was audited, construct coverage mapped, and concrete executions compared independently. |
| `Run` direct-entry driver | Parameter binding and transition into the return expression | Acceptable exact-program bridge; it executes the body and preserves continuation. No result is assumed. |
| K unbounded integers versus Python integers | Numeric values, subtraction, parity, comparisons | Aligned for this program and intended domain; Python integers are also unbounded and no overflow occurs. |
| Mathematical interpretation of the contract predicate | Connects exact results/checker to “greatest even integer” | Fully justified by consecutive-integer parity and the next-even value `R+2`; not an empirical oracle. |
| Differential testing | Supports source/canonical/semantics adequacy on finite cases | Supplemental finite evidence only; no proof claim depends on treating it as universal. |

There are no candidate-local opaque symbols, external value oracles, empirical
rewrite bridges, assumed helper lemmas, simplification axioms, totality
assertions, or circular loop summaries.

Excluded behavior includes non-integer arguments, arbitrary translated
programs, general calls, mutation, heap/IO, exceptions, and unused Python
operators. None occurs in the real submitted program or the positive-integer
claim domain, so this minimal generated-semantics scope creates no material
adequacy gap.

### Gate and decision summary

- Real-program soundness: pass. The exact body executes; all rules are sound on
  reachable intended states; body and result mutations are detected.
- Intent adequacy: pass. The exhaustive exact-result partition and checker
  match the trusted positive-integer task contract.
- Trust/evidence auditability: pass. Commands, inputs, statuses, bounded logs,
  static inventory, raw negative residuals, and reviewer scripts are preserved
  under `evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
