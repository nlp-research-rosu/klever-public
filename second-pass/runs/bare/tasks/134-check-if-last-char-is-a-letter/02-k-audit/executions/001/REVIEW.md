# Independent adversarial audit: 134-check-if-last-char-is-a-letter

## Decision summary

The candidate has a reproducible, non-vacuous `#Top` proof under its own K
theory, but it does **not** contain a legitimate partial-correctness proof of
the real submitted Python program over the stated/formal input domain.

The decisive defect is a result-bearing semantic bridge. The formal entry claim
has no ASCII precondition and ranges over every K `String`, while the submitted
Python uses CPython's Unicode-aware `str.isalpha()`. The generated semantics
instead defines `isalpha` using only the literal characters `A-Z` and `a-z`.
On the concrete satisfying input `"K"` (U+212A KELVIN SIGN), fresh K execution
returns `false`, while both `/reference/canonical.py` and the submitted
`solution.py` return `True`. This is a concrete false-result witness for the
theory used by the proof, not merely an untested corner.

There are additional material language-model defects: the `len` bridge does not
match CPython for some Unicode strings, Boolean operators are modeled eagerly
rather than with Python short-circuit control, and indexing omits `IndexError`.
For example, the K rules evaluate `"a"[-2]` as `"a"`, while CPython raises
`IndexError`.

The infrastructure was sufficient to reach a candidate verdict. The required
mode invariant held, fresh sources compiled, all positive claims ran, and the
fresh false mutation failed for the expected unmet result.

## 1. Input and provenance integrity

### Semantics-mode boundary

This run is rendered as `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. No hidden or inferred
reference semantics was sought or used. This is not an infrastructure breach.
The independently installed tools report K version `v7.1.293`.

### Artifact types and provenance

The complete top-level/type inventory and hashes are in
[01-provenance-inventory.log](/audit-output/evidence/01-provenance-inventory.log).
All required generation and source artifacts are regular files, not symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- the structured JSONL trace under `codex-trace/`
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`

The generator's required filename is singular `semantic.k`; the absence of a
separate `semantics.k` is not a mistyping. There are no candidate helper K
files. Candidate-provided `semantic-kompiled/` and `verification-kompiled/`
directories are additional untrusted build products; they were not copied,
read as definitions, or reused.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. The
comparison and complete source listing are in
[03-source-integrity-and-content.log](/audit-output/evidence/03-source-integrity-and-content.log).
There are no missing, changed, mistyped, additional, or symlinked required
source artifacts.

### Untrusted generation claims

`run-input.json` says the condition was `bare` with no supplied semantics.
`metrics.json` says generation exited 0. `codex-last.txt`, `codex-output.log`,
and the trace claim that all concrete checks passed and `kprove` produced
`#Top`. Those were treated only as claims. The bounded generation-log evidence
is in
[02-untrusted-generation-claims.log](/audit-output/evidence/02-untrusted-generation-claims.log).
The complete 388-line JSONL trace was independently parsed with no malformed
records; its untrusted final claims are summarized in
[23-structured-trace-summary.log](/audit-output/evidence/23-structured-trace-summary.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The prompt asks for `True` exactly when the last character is alphabetic and
stands alone rather than being part of a word, where words are separated by
literal spaces.

The trusted canonical implementation makes that precise by taking
`txt.split(' ')[-1]` and returning true exactly when that final token has length
one and its lowercased character has an ordinal in `97..122`. Thus its ordinary
successful domain is effectively ASCII-letter based, with Python-specific
Unicode edge behavior: for example, `"K".lower()` is `"k"` and is accepted,
whereas `"é"` is rejected; a character such as `"İ"` whose lowercase expands
to two code points causes the canonical `ord` call to raise `TypeError`.

The submitted implementation instead returns:

```python
(len(txt) == 1 and txt.isalpha()) or (
    len(txt) > 1 and txt[-1].isalpha() and txt[-2] == " "
)
```

This is equivalent to the canonical algorithm for the ordinary ASCII cases,
but `str.isalpha()` accepts many non-ASCII letters.

### Translation fidelity

All source files were copied to `/tmp/audit-work/source`; no candidate build
output was copied. Running the trusted `/reference/py2mpy.py` on the scratch
`solution.py` produced a file byte-identical to the submitted `solution.mpy`
(both SHA-256
`9b27bd0ba9943ad391bdb0456693800135e9f7dd2080ff5f748cfdcc2744d43d`).
The exact command, hashes, and `cmp` status 0 are in
[04-scratch-copy-and-translation.log](/audit-output/evidence/04-scratch-copy-and-translation.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and scratch candidate as separate modules. It covers:

- all four documented examples;
- empty, length-one, and length-two boundaries;
- each `len`, final-`isalpha`, and penultimate-space branch boundary;
- all strings of lengths 0 through 4 over
  `['a', 'Z', '0', ' ', '\t', 'é', 'α']`;
- 40 deterministic random strings per length 0 through 12 over a broader
  alphabet, seed 134.

Among 3,232 unique inputs it found 129 mismatches. Small witnesses include:

- `"é"`: canonical `False`, candidate `True`;
- `"α"`: canonical `False`, candidate `True`;
- `"İ"`: canonical raises `TypeError`, candidate returns `True`;
- `"x é"`: canonical `False`, candidate `True`.

The complete scope, command, status, and first 100 mismatches are in
[05-differential-results.log](/audit-output/evidence/05-differential-results.log).
The prompt places no ASCII restriction on `txt`, so these are material
divergences on the intended string domain, not violations of a stated
precondition.

Stage 2 result: **FAIL** for canonical program fidelity. Translation provenance
itself passes.

## 3. Clean proof reconstruction

### Fresh builds

Only scratch-copied source was used.

- Fresh LLVM concrete definition:
  `kompile semantic.k --backend llvm --main-module SEMANTIC
  --syntax-module MPY-SYNTAX --output-definition
  /tmp/audit-work/build/concrete-kompiled` — exit 0
  ([06-build-concrete-llvm.log](/audit-output/evidence/06-build-concrete-llvm.log)).
- Fresh Haskell proof definition:
  `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  /tmp/audit-work/build/proof-kompiled` — exit 0
  ([07-build-proof-haskell.log](/audit-output/evidence/07-build-proof-haskell.log)).
- A separate fresh Haskell concrete definition also compiled with exit 0
  ([09-build-concrete-haskell.log](/audit-output/evidence/09-build-concrete-haskell.log)).

The first LLVM batch runner was interrupted after 107 seconds while an
interpreter subprocess had made no bounded result. That run is explicitly
excluded from semantic evidence and is recorded in
[08-concrete-semantics-results.log](/audit-output/evidence/08-concrete-semantics-results.log).
This backend incident is not used against the candidate. Haskell is an approved
concrete backend and completed the same tests.

### Fresh concrete execution

[concrete_semantics_compare.py](/audit-output/evidence/concrete_semantics_compare.py)
ran the freshly built Haskell semantics on 12 normal and boundary inputs and
compared each result with both Python implementations. All `krun` commands
exited 0. ASCII cases and documented examples agreed. Four Unicode cases
disagreed with the real submitted program:

| Input | Fresh K | submitted Python | canonical Python |
|---|---:|---:|---:|
| `"é"` | `False` | `True` | `False` |
| `"x é"` | `False` | `True` | `False` |
| `"α"` | `False` | `True` | `False` |
| `"x α"` | `False` | `True` | `False` |

Commands and complete configurations are in
[10-concrete-haskell-results.log](/audit-output/evidence/10-concrete-haskell-results.log).
The sharper ground witness `"K"` produces K `false` while both Python
implementations produce `True`; see
[19-unicode-real-program-witness.log](/audit-output/evidence/19-unicode-real-program-witness.log).

### Fresh positive proofs

Running the original spec as a batch produced `#Top` and exit 0
([11-kprove-all-original.log](/audit-output/evidence/11-kprove-all-original.log)).

The candidate's six claims were then copied exactly into
[spec-audit-labeled.k](/audit-output/evidence/spec-audit-labeled.k), with only
auditor-added labels, and selected one at a time. Every run printed `#Top` and
exited 0:

| Claim | Evidence |
|---|---|
| universal entry claim | [12-kprove-entry.log](/audit-output/evidence/12-kprove-entry.log) |
| empty string | [13-kprove-empty.log](/audit-output/evidence/13-kprove-empty.log) |
| `"apple pie"` | [14-kprove-apple-pie.log](/audit-output/evidence/14-kprove-apple-pie.log) |
| `"apple pi e"` | [15-kprove-apple-pi-e.log](/audit-output/evidence/15-kprove-apple-pi-e.log) |
| trailing space | [16-kprove-trailing-space.log](/audit-output/evidence/16-kprove-trailing-space.log) |
| `"A"` | [17-kprove-single-letter.log](/audit-output/evidence/17-kprove-single-letter.log) |

The five ground helper claims emitted `WarnTrivialClaim`, meaning they simplify
without operational rewriting; this does not invalidate them, but they add no
independent connection theorem.

Stage 3 result: **PASS** for mechanical reconstruction; **FAIL** for concrete
agreement between the generated semantics and the real program.

## 4. Adequacy and real-program pinning

### Claims in plain language

The entry claim has no explicit `requires` clause. Its typed variable `S`
therefore ranges over every K `String`. It says:

> Starting from the exact submitted `Module(FuncDef(...))` AST followed by
> `runEntry("check_if_last_char_is_a_letter", S)`, execution reaches
> `pyBool(standaloneLastLetter(S))`, preserving any trailing `<k>` continuation.

The five remaining claims have no preconditions and state the ground truth
values of `standaloneLastLetter` on the documented examples plus `"A"`.

There are no loops or auxiliary loop claims. The entry rule's single-function,
single-parameter control shape matches the real submitted program. The AST in
the claim is structurally identical to the trusted regeneration of
`solution.mpy`; it is not a substituted program.

### Satisfiability and result constraint

A concrete satisfying entry state is:

```text
<python>
  <k> [the exact submitted Module AST]
       ~> runEntry("check_if_last_char_is_a_letter", "A")
  </k>
</python>
```

There are no other state cells or preconditions. Substitution gives:

- `S = ""`: claimed result `false`; both Python implementations return `False`;
- `S = "A"`: claimed result `true`; both Python implementations return `True`;
- `S = "K"`: claimed/generated-K result `false`; both Python implementations
  return `True`.

The result is not a free variable, tautology, existential, or one-way
implication. It is constrained to an exact `pyBool` term, and the false mutation
in Stage 6 confirms that the constraint is exercised.

### Pinning failure

`standaloneLastLetter` is a fully defined summary, not an unconstrained oracle.
However, it repeats the modeled source expression and shares the same
`isAlphaString` helper used by the operational `evalIsAlpha` rule. Thus the
entry proof establishes agreement with the candidate's model of `isalpha`, not
with CPython's operation. There is no bridge-free connection theorem from
CPython `str.isalpha()` or `len()` to these K helpers, and the ground witnesses
disprove such a theorem over the claim's complete domain.

Stage 4 result: **FAIL**. The K syntax is pinned, but the real operation values
and therefore the real program result are not.

## 5. Rule-by-rule static soundness review

The source-level declaration/rule extraction is preserved in
[20-static-source-inventory.log](/audit-output/evidence/20-static-source-inventory.log).
There are no generated helper K files beyond `semantic.k` and
`verification.k`.

### Syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: one statement or a statement followed by statements;
- `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`;
- `Params` and comma-separated `Strings`;
- `Expr`: `Bool`, `Int`, `Str`, `Name`, `UnaryOp`, `BoolOp`, `Compare`,
  `Subscript`, `Attribute`, and `Call`;
- comma-separated `Exprs`, `CmpOp`, and comma-separated `CmpOps`.

`SEMANTIC` declares value constructors `pyBool`, `pyInt`, and `pyStr`; twelve
local `[function]` symbols (`eval`, `evalUnary`, `evalBool2`, `evalBool3`,
`evalCompare`, `evalLen`, `evalIsAlpha`, `evalSubscript`, `isAlphaString`,
`isAlphaChars`, `isLetterChar`, and `atString`); a single `<python><k>`
configuration; and `runEntry`. `VERIFICATION` adds the thirteenth local
`[function]`, `standaloneLastLetter`.

There are no local `[total]` or `[functional]` declarations, opaque local
symbols, priorities, `[owise]` rules, simplification rules, concrete rules,
strictness attributes, macros, or aliases.

Every constructor in `solution.mpy` is declared and covered:

| Used construct | Declaration/behavior |
|---|---|
| `Module`, single `FuncDef`, `Params`, `Return` | program/statement syntax and entry rule S1 |
| `BoolOp` with two and three operands | S8-S13 |
| `Compare`, `CmpOp("==")`, `CmpOp(">")` | S14-S17 |
| `Call(Name("len"), ...)` | S18-S19 |
| `Call(Attribute(..., "isalpha"), .Exprs)` | S20-S21 |
| `Name("txt")` | S5 |
| `Subscript` | S22-S25 |
| `UnaryOp("-", Int(...))` | S3, S6-S7 |
| `Str(" ")` | S4 |

`Bool` literal syntax, multi-statement bodies, multiple parameters, and chained
comparisons are unused; missing general behavior for them is not charged as a
defect.

### Exhaustive semantic rule inventory

The following table accounts for every ordinary rule in `semantic.k`.

| ID / lines | Rule role | Assessment |
|---|---|---|
| S1 / 67-69 | Consume the exact one-function module plus matching `runEntry`; bind its sole parameter and evaluate the sole `Return` expression. | Sound for this exact program shape. It preserves the trailing `<k>` frame. It is deliberately not a general Python call/return model. |
| S2 / 71 | `Bool` literal to `pyBool`. | Sound, though unused by the submitted AST. |
| S3 / 72 | `Int` literal to `pyInt`. | Sound. |
| S4 / 73 | `Str` literal to `pyStr`. | Sound. |
| S5 / 74-75 | Environment lookup for `Name`, guarded by membership. | Sound on the one-entry map used here; guard avoids fabricated missing bindings. |
| S6 / 77 | Dispatch `UnaryOp` after evaluating its expression. | Sound for the used pure integer operand. |
| S7 / 78 | Integer unary minus. | Sound. |
| S8 / 80-81 | Dispatch two-operand `BoolOp` by evaluating both operands. | Not Python control semantics: it is eager. Actual Python `and`/`or` short-circuit and return an operand. All target operands eventually produce booleans, so the operand-return difference does not change ASCII results, but the eager control reaches protected subscripts that Python skips. |
| S9 / 82-83 | Dispatch three-operand `BoolOp` by evaluating all operands. | Same control defect as S8. On submitted input `"a"`, Python's first `or` branch is true and the second branch is never evaluated; K evaluates the second branch, including the invalid `txt[-2]`, then masks the fabricated result. |
| S10 / 84 | Boolean two-way `and`. | Correct Boolean algebra after both operands have been produced; it does not repair S8's missing short circuit. |
| S11 / 85 | Boolean two-way `or`. | Correct Boolean algebra after eager evaluation. |
| S12 / 86-87 | Boolean three-way `and`. | Correct Boolean algebra after eager evaluation. |
| S13 / 88-89 | Boolean three-way `or`. | Correct Boolean algebra after eager evaluation. |
| S14 / 91-92 | Dispatch one-link comparisons after evaluating both expressions. | Sound for pure used expressions; chained comparisons are unmodeled but unused. |
| S15 / 93 | Integer equality. | Sound. |
| S16 / 94 | String equality. | Sound as K string equality and adequate for the literal-space comparison. |
| S17 / 95 | Integer greater-than. | Sound. |
| S18 / 97 | Hardwire `Name("len")` calls. | Sound for this unshadowed submitted program; it would not model rebinding, which is absent. |
| S19 / 98 | Map Python `len(str)` to K `lengthString`. | **Unsound over the formal string domain.** Fresh execution gives `lengthString("α") = 2` and `lengthString("K") = 3`, while CPython `len` gives 1 for each. The exact witness is in [24-unicode-length-witness.log](/audit-output/evidence/24-unicode-length-witness.log). |
| S20 / 100-101 | Hardwire zero-argument string attribute call `"isalpha"`. | Binding is adequate for the target because every receiver is a string and no rebinding occurs. Its value bridge S21 is false. |
| S21 / 102 | Map Python `str.isalpha()` to `isAlphaString`. | **Materially unsound.** With the exact submitted program and input `"K"`, K reaches `pyBool(false)` while both Python programs return `True`; see [19-unicode-real-program-witness.log](/audit-output/evidence/19-unicode-real-program-witness.log). This false result is inside the universal entry claim's domain. |
| S22 / 104-105 | Evaluate subscript receiver and index. | The dispatch is pure but inherits S23-S25's missing exception behavior. |
| S23 / 106 | Map string subscript to `atString`. | **Unsound as Python indexing** because it always fabricates a string result and has no exception branch. |
| S24 / 108-109 | Nonnegative index as `substrString(S,I,I+1)`, guarded only by `I >= 0`. | **Unsound** for `I >= len(S)`: Python raises `IndexError`; no bounds guard exists. The target uses negative indexes, but global false rules are not justified merely by off-path intent. |
| S25 / 110-113 | Negative index translated by adding string length, guarded only by `I < 0`. | **Unsound** for `I < -len(S)`. The concrete conclusion enabled by S23/S25 is `evalSubscript(pyStr("a"), pyInt(-2)) => pyStr("a")`, whereas CPython raises `IndexError`; see [18-out-of-bounds-semantics-witness.log](/audit-output/evidence/18-out-of-bounds-semantics-witness.log). The input string `"a"` is in the intended domain, and the submitted AST contains the `-2` subscript that eager S9 reaches. |
| S26 / 115 | Empty `isAlphaString` is false. | Internally correct for both ASCII membership and Python `isalpha`. |
| S27 / 116-117 | Nonempty string starts recursive character scan at zero. | Internally sound as part of the candidate's ASCII predicate. Guard is disjoint from S26. |
| S28 / 119-120 | Character scan is true at/past length. | Internally sound for calls starting at zero. |
| S29 / 121-124 | Scan the current character and recurse at `I+1`. | Internally terminating for reachable `I >= 0` and disjoint from S28. There is an intentional partial gap at `I < 0`, but no call supplies such an index. |
| S30 / 128-132 | A one-character string is a letter iff found in the literal ASCII alphabet. | A consistent and terminating definition of **ASCII** membership, not of CPython `str.isalpha()`. It becomes illegitimate through the S21 bridge. It explicitly excludes the `"K"` witness and all non-ASCII alphabetic characters. |

The guards for `atString` partition all integers and do not overlap, but their
coverage is the problem: invalid Python indexes are included. The empty and
nonempty `isAlphaString` rules are disjoint. The two `isAlphaChars` guards are
disjoint; recursive calls strictly increase `I` toward finite string length.
Operator-specific rules have disjoint literal operators or value sorts. No
priority or simplification interaction exists.

### Verification rule and claims

`verification.k` has exactly one rule:

| ID / lines | Classification | Assessment |
|---|---|---|
| V1 / 11-16 | Definitional summary `standaloneLastLetter(S)`. | It is unguarded, deterministic, and internally agrees with the modeled source expression. It does not replace K execution. It is not independent evidence for Python meaning because it uses the same `isAlphaString` and `atString` helpers as the semantics. Its dependents are the entry claim and five ground claims. |

`spec.k` has exactly six reachability claims: one universal entry claim and the
five ground summary claims inventoried in Stages 3 and 4. There are no
proof-local lemmas, circularities, operational bridges, simplification axioms,
or opaque result symbols in the proof module.

### State, control, calls, and trust boundary

The configuration has only `<k>`; there is no store, heap, output, allocation,
exception, or call stack. That is adequate for the target's ordinary pure
successful executions, but the missing exception/control representation is
material to Python indexing and short-circuit evaluation. `len` and `isalpha`
bindings are hardwired; this is acceptable for the exact unshadowed target,
but their value semantics must still be correct.

Imported K Boolean, integer, map, and string operations are low-level
primitives. Using them as K mathematics is acceptable. Equating the observed K
string hooks to CPython Unicode `len`, indexing, and `isalpha` without a
connection theorem is not. The ground counterexamples show this is a smuggled
and false correctness bridge rather than a merely thin trust boundary.

Stage 5 result: **FAIL**. S19, S21, and S23-S25 admit the concrete false
conclusions required above; S8-S9 additionally misrepresent real control and
expose the invalid-index bridge during target execution.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The auditor-authored
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k) uses the
exact submitted AST and the satisfying input `"A"`, but mutates the
result-constraining destination to `pyBool(false)`.

The mutation was first parsed/compiled with:

```text
kprove spec-vacuity-audit.k
  --definition /tmp/audit-work/build/proof-kompiled
  --spec-module SPEC-VACUITY-AUDIT
  --dry-run
```

It exited 0; see
[21-mutation-dry-run.log](/audit-output/evidence/21-mutation-dry-run.log).
The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
shows the reachable computation at `pyBool(true)`, which cannot unify with the
mutated `pyBool(false)` destination:
[22-mutation-proof-expected-failure.log](/audit-output/evidence/22-mutation-proof-expected-failure.log).

This is the expected semantic failure, not a parse error, missing import,
timeout, or unrelated crash.

Stage 6 result: **PASS**. The formal proof is non-vacuous and
result-constraining.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's generated K theory, for every K `String S`, the exact
submitted MPY AST followed by `runEntry(..., S)` rewrites to:

```text
pyBool(standaloneLastLetter(S))
```

The summary unfolds to the same K-level Boolean expression computed by the
candidate evaluator. The proof also establishes the five ground summary values.
This is a genuine, non-vacuous theorem about the supplied K equations.

It does **not** establish that those equations are CPython semantics, that the
submitted Python is extensionally equal to the trusted canonical function over
all strings, or that the shared `isAlphaString` summary has Python's
`str.isalpha()` meaning.

### Trust and assumption ledger

| Boundary | Dependents | Judgment |
|---|---|---|
| Trusted prompt, canonical implementation, and translator mounts | Intent and source provenance | Acceptable trusted inputs. Prompt/translator byte identity and translation byte identity were checked. |
| K Boolean, integer, map, and raw string hooks | All semantic evaluation | Acceptable as primitives of the K theory. Their equivalence to CPython operations is a separate bridge, not automatically trusted. |
| `lengthString` represents Python `len(str)` | Branch guards, indexing, entry result | Illegitimate over the universal domain; the `"α"` and `"K"` length witnesses disprove it. |
| ASCII `isAlphaString` represents Python `str.isalpha()` | Both program execution and postcondition | Illegitimate and circular as correctness support; the same helper occurs on both sides, and `"K"` disproves the value bridge. |
| `substrString`/`atString` represents Python indexing | Final and penultimate character tests | Illegitimate without bounds/exception behavior; `"a"[-2]` is a concrete false conclusion. |
| Eager `evalBool2/3` represents Python `and`/`or` | All branch control | Concerning and operationally false. The final ASCII result happens to agree for this pure expression, but K evaluates target subterms Python skips. |
| `standaloneLastLetter` expresses the English/canonical property | Entry postcondition | Only an informal bridge. Differential evidence disproves universal equivalence to the canonical implementation. |
| Finite differential and concrete tests | Empirical bridge support only | Reproducible evidence, not a proof. They support ordinary ASCII cases and expose the material Unicode failures. |
| Termination | Reachability interpretation | The audit concerns partial correctness. The K equations concretely terminate on tested inputs; no claim of CPython total correctness is inferred. |

### Final judgment

Mechanical Gate A5 non-vacuity passes, and all positive claims close from clean
source. Nevertheless, real-program Gate A fails because result-bearing
semantics rules make false conclusions on satisfying inputs in the formal and
intended domain. Program-fidelity Gate B also fails because the submitted
Python diverges materially from the trusted canonical function on unrestricted
strings. Finite tests and the candidate's prior `#Top` cannot repair either
universal bridge.

Accordingly, this is a clean candidate failure, not `AUDIT_ERROR`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
