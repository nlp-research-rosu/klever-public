# Independent adversarial audit — 144-simplify

## Audit conclusion

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the exact translated generated program on the formal domain of canonical
positive-decimal fraction strings. Both generated definitions were rebuilt
from source, all four positive claims independently closed with `#Top` and exit
0, the submitted translation was reproduced byte-for-byte, and a deliberately
false result claim failed only after the real body executed to the opposite
Boolean.

I assign `CONCERNS / LEGIT`, rather than an unqualified pass, for three bounded
reasons:

1. The result-bearing symbolic string equations are mathematically consistent
   with K's installed hook contracts and all ground/operational tests, but the
   bridge-free universal K claims remain stuck because the backend treats the
   string hooks opaquely. The proof is therefore conditional on a named
   low-level conversion/splitting contract.
2. The universal claim quantifies canonical `Int2String` spellings only. It
   does not formally cover arguably valid alternative decimal spellings such
   as leading-zero components, although the generated Python implementation
   handles them.
3. The trusted canonical implementation is not a universal behavioral oracle:
   its floating-point quotient test disagrees with the mathematical contract
   at large magnitudes and can raise `OverflowError`. The generated modulo
   implementation and K theorem follow the natural-language mathematical
   contract instead.

No reviewed rule was found to enable a false conclusion on the intended formal
input domain. No rule is labeled unsound below without the required witness.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` does not exist. `/reference` contains exactly
the three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`.
This is consistent with the rendered mode; there is no infrastructure breach.
The recursive candidate scan found no symlinks.

All required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. One structured JSONL trace is
present. There is no candidate `PROOF.md` or `spec-vacuity.k`; neither is a
required source artifact. There are no generated helper K files.

The candidate also contains four candidate-built `*-kompiled` directories,
one `__pycache__`, and a `.pyc`. They are extra execution artifacts, not source
integrity failures, and were excluded from every audit command.

Evidence:

- [`01-mount-and-artifact-integrity.log`](evidence/01-mount-and-artifact-integrity.log)
- [`02-trusted-input-comparison.log`](evidence/02-trusted-input-comparison.log)

### Trusted-input comparison

The candidate prompt is byte-identical to `/reference/prompt.py`
(`2a0addf5…735`), and the candidate translator is byte-identical to
`/reference/py2mpy.py` (`406485ea…b16`). Both `cmp` commands exited 0.

### Untrusted generation claims

I read the four requested metadata/prose files and the structured trace solely
as untrusted claims. `run-input.json` identifies problem `144-simplify`,
condition `bare`, and no supplied semantics; its recorded prompt/translator
hashes agree with the trusted files. `metrics.json` claims a successful,
non-timeout generation. `codex-last.txt` and the final trace message claim that
`prove.sh` produced `#Top`. The trace also records an earlier stuck universal
claim before a direct conversion simplification was added. None of those
claims was used as proof evidence.

The trace has 216 lines and SHA-256
`ac4ec736…0eaff`; `codex-output.log` is 1,360,524 bytes. Relevant bounded
excerpts, hashes, and the candidate's claimed commands/results are preserved
in [`05-untrusted-generation-claims.log`](evidence/05-untrusted-generation-claims.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

For positive integers `A,B,C,D`, inputs are strings `x = "A/B"` and
`n = "C/D"`. Their product is a whole number exactly when

```text
(A * C) mod (B * D) = 0.
```

The trusted canonical splits both strings, converts the four components,
computes numerator and denominator products, then tests whether the
floating-point quotient equals its integer truncation. The generated solution
splits and converts the same components and directly tests divisibility with
integer modulo. The latter is a different algorithm but is the exact
mathematical predicate in the prompt.

### Translation fidelity

Using only the trusted copied translator, I regenerated `solution.mpy` from the
scratch copy of `solution.py`. The regenerated and submitted files both hash to
`7ecb2f74…ef3d` and `cmp` exited 0. See
[`03-translation-identity.log`](evidence/03-translation-identity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical and generated entry points and uses the direct
divisibility predicate as a third oracle. It exercises:

- the three documented examples;
- the minimum valid components and both sides of the remainder boundary;
- true and false/cross-cancellation branches;
- all `12^4 = 20,736` quadruples with each component in `1..12`;
- 2,000 deterministic random quadruples in `1..1,000,000`;
- large precision and overflow boundaries; and
- six invalid/empty cases, recorded separately as outside the promised domain.

The command exited 0 after 22,748 valid cases with zero generated-versus-
contract mismatches. It found two canonical-versus-generated mismatches:

- `9007199254740993/2 * 1/1`: canonical `True`, generated/oracle `False`,
  because the non-integral quotient rounds to a floating-point integer.
- a 401-digit numerator over `3`: canonical raises `OverflowError`,
  generated/oracle return `False`.

Those are material discrepancies on the prompt's unbounded positive-integer
wording. They show a limitation in the trusted reference implementation, not a
false result from the generated program. Empty/malformed/zero-denominator
cases are outside the stated contract; their differing exception behavior is
not part of the theorem. Full results and exact scope are in
[`04-differential-test.log`](evidence/04-differential-test.log).

## 3. Clean proof reconstruction

All candidate-built definitions and caches were ignored. Source artifacts were
copied to `/tmp/audit-work/review-144/source`; fresh definitions were created
only below `/tmp/audit-work/review-144/build`.

The audit toolchain was K `v7.1.293` and Python `3.10.12`
([`06-toolchain-versions.log`](evidence/06-toolchain-versions.log)).

### Fresh builds

| Definition | Exact source/backend purpose | Result |
|---|---|---|
| Base concrete semantics | `kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/review-144/build/semantic-kompiled` | exit 0 |
| Proof semantics | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/review-144/build/verification-kompiled` | exit 0 |

The exact logs are
[`07-fresh-concrete-build.log`](evidence/07-fresh-concrete-build.log) and
[`08-fresh-proof-build.log`](evidence/08-fresh-proof-build.log).

### Independent positive-claim runs

Each claim was selected and run separately with `--spec-module SPEC` and its
fully qualified label:

| Claim | Evidence | Exit/output |
|---|---|---|
| `SPEC.simplify-general` | [`09-proof-simplify-general.log`](evidence/09-proof-simplify-general.log) | 0, `#Top` |
| `SPEC.example-true` | [`10-proof-example-true.log`](evidence/10-proof-example-true.log) | 0, `#Top` |
| `SPEC.example-false-one` | [`11-proof-example-false-one.log`](evidence/11-proof-example-false-one.log) | 0, `#Top` |
| `SPEC.example-false-two` | [`12-proof-example-false-two.log`](evidence/12-proof-example-false-two.log) | 0, `#Top` |

The only diagnostics are harmless warnings that existential final maps are not
otherwise referenced.

### Generated-semantics concrete reconstruction

[`concrete_semantics_test.py`](evidence/concrete_semantics_test.py) ran the
submitted, independently regenerated program term with the fresh base
definition and compared the return value with independent Python execution.
All 12 runs exited 0 and agreed. They include all prompt examples, minimum
positive components, zero/nonzero remainder boundaries, cross-cancellation,
ordinary false input, values around `2^53`, and a 401-digit integer. Every
submitted construct executes on every run. Commands and results are in
[`13-concrete-semantics-vs-python.log`](evidence/13-concrete-semantics-vs-python.log).

## 4. Adequacy and real-program pinning

### Claim meanings

`SPEC.simplify-general` starts with empty functions/environment maps, no result,
the closed `simplifyProgram` module, and an invocation on
`Int2String(A)/Int2String(B)` and `Int2String(C)/Int2String(D)`. Its
precondition is exactly `A,B,C,D > 0`. It requires complete consumption of
`<k>` and fixes the final result to:

```text
boolVal(((A * C) % (B * D)) == 0).
```

Final `<functions>` and `<env>` maps are existential because they are internal
execution state; the observable return is not existential or free.

The other three entry claims have no additional precondition and assert the
three prompt examples' exact Boolean results. There are no helper, loop,
circularity, or auxiliary claims, so no summary claim can bypass real control
flow.

### Exact program identity

The claim uses `simplifyProgram`, whose sole rule expands to a closed
`Module(...)` AST. After removing only insignificant K whitespace, that RHS is
byte-identical to the submitted `solution.mpy` term; both compact forms hash to
`e7693808…20f1`. Combined with the trusted-translator byte identity from Stage
2, this pins the claim's executing term to the submitted generated program.
See [`14-real-program-pinning.log`](evidence/14-real-program-pinning.log).

This is static closed-term pinning rather than loading the filename from within
the claim. A one-token body mutation of the pinned AST (`== 0` to `== 1`)
rebuilt successfully and made the universal proof fail on the resulting
`== 0` versus `== 1` obligation:
[`verification-body-mutant.diff`](evidence/verification-body-mutant.diff),
[`26-body-mutation-build.log`](evidence/26-body-mutation-build.log), and
[`27-body-mutation-proof.log`](evidence/27-body-mutation-proof.log).

### Satisfiable witnesses

`A=B=C=D=1` satisfies every general precondition and yields `True` in the
claimed expression, trusted canonical, and generated implementation.
Additional satisfying substitutions exercise both results:

| `(A,B,C,D)` | Claimed result | Canonical | Generated |
|---|---:|---:|---:|
| `(1,1,1,1)` | `True` | `True` | `True` |
| `(1,6,2,1)` | `False` | `False` | `False` |
| `(2,3,3,2)` | `True` | `True` | `True` |
| `(7,10,10,2)` | `False` | `False` | `False` |

The executable witness record is
[`claim_witness.py`](evidence/claim_witness.py) with results in
[`15-claim-witnesses.log`](evidence/15-claim-witnesses.log).

## 5. Rule-by-rule static soundness review

The full declaration/rule record, including complete domains and a decision for
every entry, is [`rule-inventory.md`](evidence/rule-inventory.md). Numbered
source with hashes is preserved in
[`23-audited-k-sources.log`](evidence/23-audited-k-sources.log).

### Exhaustive local inventory

There are 15 local syntax declarations:

1. `ParamList`; 2. `Params`; 3. the eight `Expr` constructors (`Name`, `Int`,
   `Str`, `Attribute`, `Call`, `Subscript`, `BinOp`, `Compare`);
4. `CmpOp`; 5. the three `Stmt` constructors (`FuncDef`, `Assign`, `Return`);
6. `Stmts`; 7. `Module`; 8. the seven `PyVal` constructors (`intVal`,
   `boolVal`, `strVal`, `pairList`, `builtinInt`, `splitMethod`,
   `slashSplit`); 9. `decimalValue` injected into `Int`; 10. `PyVal` injected
   into `Expr`; 11. `PyVals`; 12. `Function`; 13. `Result`; 14. the 13 `KItem`
   control constructors; and 15. the closed `simplifyProgram` module constant.

The four-cell configuration contains only used state: computation, stored
functions, local environment, and result.

There are exactly two local `[function]` declarations, `slashSplit` and
`decimalValue`; neither is declared `[total]`. Their base equations are the
only `[owise]` rules. There are no local `[functional]`, fresh, opaque,
uninterpreted-result, hook, macro, or explicit `priority(N)` declarations.
There are three proof-local `[simplification]` rules.

### All 32 semantic rules

- S01–S03 enter a module and execute a statement list left to right.
- S04 stores the top-level function; S05 invokes the exact two-argument stored
  body and binds `x,n`.
- S06–S07 evaluate assignment RHSs then update the environment.
- S08–S09 evaluate the return expression, consume the remaining top-level
  function continuation, and set the result.
- S10–S13 evaluate integer/string literals, resolve unshadowed builtin `int`,
  and perform environment lookup.
- S14–S18 evaluate receiver, method, callee, and argument in Python order and
  dispatch `str.split("/")`.
- S19 splits a string at its first slash into the two modeled components.
- S20–S21 apply integer conversion through `decimalValue`/`String2Int`.
- S22–S25 evaluate subscripting base then index and implement indices 0 and 1.
- S26–S29 evaluate binary operands left to right and implement integer
  multiplication and guarded nonzero-divisor modulo.
- S30–S32 evaluate the comparison left to right and implement integer
  equality.

Every rule is individually described and decided in the linked inventory. On
the formal input domain, these rules preserve binding, left-to-right
evaluation, state updates, and the only control transfer. The return rule's
arbitrary `_REST`, builtin-name rule, and two-element split model would be too
broad for a reusable general Python semantics, but the submitted program has
no caller continuation, no `int` shadowing, and exactly one slash with
nonempty components. No intended input reaches the problematic contexts.

The concrete outside-domain witness `"1/2/3","1/1"` produces `#Bottom` in the
generated semantics, whereas the generated Python happens to return `False`
after indexing only the first two split elements. This is evidence of the
model's declared domain limit, not an intended-domain unsoundness witness; the
prompt promises valid two-component fractions. See
[`21-out-of-domain-semantics-gap.log`](evidence/21-out-of-domain-semantics-gap.log)
and Stage 2's invalid-case record.

### All four verification rules

V01 is the `simplifyProgram` closed-term expansion. It is a transparent
abbreviation, not an oracle or substituted body; Stage 4 proves exact identity.

V02 specializes `slashSplit` to
`Int2String(A) + "/" + Int2String(B)`. K's installed contract says integer
strings are nonempty digits optionally prefixed by a sign. Therefore neither
component contains `/`; the concatenation has exactly one separator; the
base `findString`/`substrString` rule returns the two original component
strings. This is result-bearing but does not encode the task answer.

V03 rewrites `decimalValue(Int2String(I))` to `I`; V04 rewrites
`String2Int(Int2String(I))` to `I`. They are the decimal conversion inverse
law. V03 and its base `[owise]` equation agree through V04; V02 and the base
split `[owise]` equation likewise agree. The three simplifications have no
conflicting RHSs, recursive descent, or unguarded task-property conclusion.

The installed hook declarations/contracts are preserved in
[`20-k-builtin-contracts.log`](evidence/20-k-builtin-contracts.log).
Ground positive and negative/zero split/conversion claims all close with
`#Top` under the base definition alone
([`connection-base.k`](evidence/connection-base.k),
[`16-ground-connection-checks.log`](evidence/16-ground-connection-checks.log)).
The complete base and proof-extended observable configurations are identical
on five true/false/minimum/large witnesses
([`extension_sensitivity_test.py`](evidence/extension_sensitivity_test.py),
[`22-extension-sensitivity.log`](evidence/22-extension-sensitivity.log)).

Bridge-free universal claims for V02–V04 do not close: they stop at opaque
symbolic `slashSplit(Int2String(...))` or
`String2Int(Int2String(I))` equalities. The residuals are preserved in
[`17-universal-split-connection-attempt.log`](evidence/17-universal-split-connection-attempt.log),
[`18-universal-decimal-connection-attempt.log`](evidence/18-universal-decimal-connection-attempt.log),
and [`19-universal-builtin-connection-attempt.log`](evidence/19-universal-builtin-connection-attempt.log).
This is the principal proof-evidence concern. It is not a concrete or symbolic
false-conclusion witness: the equations follow from the fixed external hook
contract and ordinary string mathematics, and all checked ground cases agree.

### Construct-to-rule coverage

`Module`/`FuncDef`/`Params` use S01–S05; `Assign` uses S06–S07; `Return`
uses S08–S09; literals/names use S10–S13; `Attribute`/`Call`/split/int use
S14–S21; subscripts use S22–S25; `*` and `%` use S26–S29; comparison uses
S30–S32. Thus every constructor in `solution.mpy` maps to syntax, evaluation
order, state effects, and a terminal rule on the formal domain.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. I created
[`spec-vacuity.k`](evidence/spec-vacuity.k) in scratch. It invokes the exact
program on the satisfiable input `"1/5","5/1"` but changes the required result
from the demonstrably correct `true` to `false`.

The mutation dry-built successfully with exit 0
([`24-vacuity-mutation-build.log`](evidence/24-vacuity-mutation-build.log)).
The real proof run exited 1 with `WarnStuckClaimState`, after executing the
entire submitted body to an empty `<k>` and
`result(boolVal(true))`. That is the expected unmet result obligation, not a
parse/import error, timeout, unreachable claim, or unrelated crash. See
[`25-vacuity-mutation-proof.log`](evidence/25-vacuity-mutation-proof.log).

This establishes that the positive proof discriminates the returned Boolean.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the compiled generated semantics and the listed external primitive
contracts, K proves partial correctness of the exact translated generated body:
for arbitrary K integers `A,B,C,D > 0`, execution on canonical decimal strings
`A/B` and `C/D`, if it terminates, consumes the computation and returns exactly
whether `B*D` divides `A*C`. The straight-line semantics also executes to that
state in all concrete reconstruction tests. The three prompt examples are
separately proved.

The theorem does not prove the trusted canonical's floating-point behavior,
general CPython object/exception semantics, behavior on malformed fractions,
zero denominators, multiple slashes, alternate string encodings, or all
possible decimal spellings.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K frontend, Haskell backend, reachability logic | All build/proof results | Standard toolchain trust. Fresh builds and exact exit/output logs prevent reliance on candidate binaries but cannot prove the prover itself. |
| Imported `INT`, `STRING`, `BOOL`, `MAP` primitives | Entire semantics; especially split/conversion and arithmetic result | Acceptable low-level fixed-semantics boundary. Installed contracts were inspected; representative ground and end-to-end cases agree. |
| `Int2String`/`String2Int` inverse and symbolic split specialization V02–V04 | Universal general claim | Sound ordinary mathematics over the installed decimal-string contract, but not independently universally discharged by K because the hooks are opaque. This is a documented concern, not an unconstrained oracle: values are fixed and opposite ground results are rejected by execution. |
| Trusted translator's AST-to-term faithfulness | Python-to-`solution.mpy` bridge | Byte identity establishes provenance, while the exhaustive construct map/static semantics review and concrete differential tests support meaning. Translator identity alone is not treated as a correctness proof. |
| Generated semantics as a Python subset | K-to-generated-Python bridge | Audited rule by rule and compared on boundary/large cases. It is intentionally partial outside valid two-component positive fractions. |
| `simplifyProgram` closed AST copy | Real-program pinning | Token-identical to the submitted trusted-translator output. A body mutation breaks the theorem. Acceptable static pin, though not dynamic file loading. |
| Natural-language interpretation of “whole number” as divisibility | Formal-result-to-intent bridge | Direct elementary arithmetic. The generated implementation matches it on all 22,748 tested valid inputs; the canonical's floating-point defects are explicitly excluded rather than silently adopted. |
| Finite differential and concrete tests | Empirical support only | They support the Python/semantics and builtin bridges for their stated inputs. They are not substituted for `kprove` or claimed as universal proofs. |

### Final decision

The proof is freshly reproducible, result-constraining, body-sensitive, and
pins the real submitted generated program. The semantic/proof rules do not
smuggle the requested Boolean or replace program execution with an
unconstrained value. The remaining universal string-hook bridge and domain
wording limitations are genuine audit concerns, but they do not furnish a
false conclusion on the intended formal domain and do not make the proof
illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
