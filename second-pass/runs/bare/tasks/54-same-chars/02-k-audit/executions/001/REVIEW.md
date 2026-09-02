# Independent adversarial audit: 54-same-chars

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under its generated K semantics. The
proof was rebuilt without candidate caches, every one of the seven positive
claims independently closed, the body is proof-sensitive, and a fresh false
result claim was rejected for the expected reason.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
bridge from K's string/set primitives to the full CPython `str` domain is not a
machine-checked part of the theorem. In particular, CPython accepts strings
containing lone surrogate code points, while fresh `krun` probes show that K's
scanner rejects those inputs. This is a documented input/model boundary, not a
false semantic rule inside the K domain and not a reason to label the proof
illegitimate.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount satisfies the
required boundary:

- `/reference/reference-semantics` does not exist.
- `/reference` contains exactly the regular files `canonical.py`, `prompt.py`,
  and `py2mpy.py`; no symlink was found.
- The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `a2ce51239856ceea4cc73764367af0452d8811af16b6bb1a9e2cb540ef726862`).
- The candidate's `py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `solution.py`, `solution.mpy`, `semantic.k`, `solution-program.k`,
  `verification.k`, and `spec.k` are present, regular, non-symlink files.
  No required artifact is missing, mistyped, changed where a trusted
  counterpart exists, or symlinked.
- `run-input.json` says the generation was `bare` with no supplied semantics,
  consistent with the rendered mode and mount.

The candidate also contains `verification-kompiled/`, `__pycache__/`,
`prove.sh`, and `embed_mpy.py`. These are additional generated/helper
artifacts, not trusted inputs. The precompiled definition and bytecode were
never used. `PROOF.md` and `spec-vacuity.k` are absent, but neither was a
required generation deliverable; a fresh mutation was authored in stage 6.

The structured trace, `codex-last.txt`, and `codex-output.log` claim that the
candidate obtained `#Top`. Those claims were read but were not credited as
proof evidence. The complete reproducible provenance inventory and bounded
excerpts are in:

- `/audit-output/evidence/01-provenance.sh`
- `/audit-output/evidence/01-provenance.log`

There is no infrastructure-mode contradiction, so a candidate verdict is
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`, `same_chars(s0,
s1)` must return whether the two input words contain the same distinct
characters. Order and multiplicity do not matter. The trusted implementation is
`set(s0) == set(s1)`.

The submitted `/candidate/solution.py` preserves the required signature and
returns exactly `set(s0) == set(s1)`. It is correct over the ordinary intended
domain of two Python strings. The surrogate-code-point boundary is discussed
below rather than silently excluded.

### Translation identity

In scratch, the trusted translator was run as:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/regenerated-solution.mpy
```

It exited 0. `cmp` against the submitted `solution.mpy` exited 0, and both
files have SHA-256
`50ea732f523d5b7b821b7f2c3a1055e0456cf1e8b9b57d306d967066453a8d07`.

### Independent differential test

`/audit-output/evidence/02-differential.py` imports the trusted canonical entry
point and the copied candidate entry point by distinct absolute paths. It does
not reuse K equations. Its 16,660 input pairs comprise:

- all six documented examples;
- 13 explicit empty, one-sided-empty, duplicate, order, case, Unicode,
  combining-character, NUL, and newline boundaries;
- every pair of strings of length 0 through 4 over `("a", "b", "é")`
  (14,641 pairs);
- 2,000 deterministic generated pairs over ASCII, Latin-1, supplementary
  Unicode, combining, NUL, and newline characters, with seed `540054` and
  deliberate coverage of both results.

The corpus digest was
`dd9f0c9e6f577d64c9a84fbbe86337aa4ec605f36816949f6a2934bda43c876e`.
There were 4,337 oracle-true and 12,323 oracle-false cases, zero documented
expectation failures, and zero candidate/canonical mismatches. This is finite
bridge evidence, not a universal theorem.

Commands, statuses, scope, and results are in:

- `/audit-output/evidence/02-program-fidelity.sh`
- `/audit-output/evidence/02-program-fidelity.log`
- `/audit-output/evidence/02-differential.py`

## 3. Clean proof reconstruction

All source needed for execution was copied to fresh directories below
`/tmp/audit-work`. No candidate `*-kompiled` directory or cache was copied or
referenced. K reports version `v7.1.293`.

### Concrete definition and execution

The generated semantics was freshly compiled with LLVM:

```text
kompile /tmp/audit-work/reconstruction/semantic.k \
  --backend llvm --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/semantic-kompiled
```

The command exited 0. Eleven fresh `krun` executions covered empty/equal,
one-sided-empty, duplicate-only, order-only, unequal-set, documented true and
false, Latin-1, decomposed Unicode, and supplementary Unicode inputs. Every
run exited 0 and matched both independent Python implementations. Both Boolean
branches and all submitted syntax constructs were exercised.

An initial reviewer harness run compiled LLVM successfully but then stopped on
the reviewer's malformed result-parsing regular expression. It made no
candidate judgment. That failed harness record is preserved in
`03-rebuild.log`; after correcting the harness, reconstruction restarted in a
new empty `/tmp/audit-work/reconstruction` directory. The clean successful
record is `03-rebuild-clean.log`.

### Proof definition and every positive claim

The proof definition was freshly compiled with Haskell:

```text
kompile /tmp/audit-work/reconstruction/verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/proof-kompiled
```

It exited 0. Running the original `spec.k` with module `SPEC` exited 0 and
printed `#Top`.

Because the submitted claims are unlabeled, the reviewer created
`spec-labeled.k`, changing only the module name and adding distinct labels to
exact copies of all seven claims. Each was selected in an independent
`kprove` invocation:

1. `SPEC-LABELED.universal`
2. `SPEC-LABELED.example-1`
3. `SPEC-LABELED.example-2`
4. `SPEC-LABELED.example-3`
5. `SPEC-LABELED.example-4`
6. `SPEC-LABELED.example-5`
7. `SPEC-LABELED.example-6`

Every invocation exited 0 and printed `#Top`. Exact commands, all concrete
inputs, outputs, and statuses are in:

- `/audit-output/evidence/03-rebuild.sh`
- `/audit-output/evidence/03-concrete-compare.py`
- `/audit-output/evidence/03-rebuild-clean.log`

Thus the positive reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The universal claim has no explicit `requires` clause. Its typed precondition
is any `S0:String` and `S1:String` in the initial generated-language
configuration:

```text
<k> solutionProgram </k>
<s0> S0 </s0>  <s1> S1 </s1>
<env> .Map </env>
<result> noResult </result>
```

It requires termination with an empty `<k>` cell, the two formal parameters
bound to the supplied strings, and exactly:

```text
result(boolValue(sameCharsSpec(S0, S1)))
```

The result is not a fresh or unconstrained variable. `sameCharsSpec` rewrites
unconditionally to `charSet(S0) ==K charSet(S1)`.

The six other entry claims use the six prompt inputs as exact preconditions and
require the documented concrete results: `true`, `true`, `true`, `false`,
`false`, and `false`. Each prompt input state is therefore a concrete
satisfying witness for its claim. For the universal claim, examples of
satisfying initial states are:

- `S0 = "ab", S1 = "ba"`, whose required result is `true`;
- `S0 = "ab", S1 = "aa"`, whose required result is `false`;
- `S0 = "", S1 = ""`, whose required result is `true`;
- `S0 = "", S1 = "a"`, whose required result is `false`.

The trusted canonical function, candidate Python function, direct mathematical
set calculation, and fresh K execution agree on these substitutions. See
`04-pinning.py` and `04-static-source.log`.

### Exact program pinning

`solutionProgram` is not a substituted algorithm. The reviewer independently
constructed the expected K wrapper around the submitted, trusted-regenerated
`solution.mpy`; it is byte-identical to `solution-program.k`. Unfolding it
produces exactly:

```text
Module(FuncDef("same_chars", Params("s0", "s1"),
  Return(Compare(
    Call(Name("set"), Name("s0")),
    CmpOp("==", Call(Name("set"), Name("s1")))))))
```

The `<k>` cell therefore executes the actual translated body. The proof has no
loop or helper-function claim to misalign with control flow.

As a separate body-sensitivity test, the reviewer changed only the translated
body's second argument from `s1` to `s0`, rebuilt a new Haskell definition, and
reran the universal claim. The build exited 0, but `kprove` exited 1 with
`WarnStuckClaimState`. Its residual showed `boolValue(true)` on states where
`charSet(S0)` and `charSet(S1)` need not agree. The concrete witness `S0 = ""`,
`S1 = "a"` makes the mutation return `true` while the real program and
contract return `false`. This establishes body sensitivity rather than mere
syntactic reachability. Evidence:

- `/audit-output/evidence/05-body-sensitivity.sh`
- `/audit-output/evidence/05-body-sensitivity.log`

The real-program pinning and result-constraint gate passes.

## 5. Rule-by-rule static soundness review

The numbered sources, declaration scan, and relevant installed K builtin
documentation are preserved in:

- `/audit-output/evidence/04-static-source.sh`
- `/audit-output/evidence/04-static-source.log`

### Exhaustive local declaration inventory

`semantic.k` declares:

1. `Program ::= Module(Function)`.
2. `Function ::= FuncDef(String, Params, Statement)`.
3. `Params ::= Params(String, String)`.
4. `Statement ::= Return(Expr)`.
5. Three `Expr` productions: `Name(String)`, `Call(Expr, Expr)`, and
   `Compare(Expr, CmpOp)`.
6. `CmpOp ::= CmpOp(String, Expr)`.
7. Three `Value` productions: `stringValue(String)`, `setValue(Set)`, and
   `boolValue(Bool)`.
8. Two `Result` productions: `noResult` and `result(Value)`.
9. `charSet(String)` as a local `[function]`.
10. Five internal `KItem` productions: `eval(Expr)`, `makeSet`,
    `compareRight(Expr)`, `compareValues(Value)`, and `finishReturn`.
11. One configuration with `<k>`, `<s0>`, `<s1>`, `<env>`, and `<result>`.

It contains two `[concrete]` equations for `charSet` and nine operational
rules. `solution-program.k` adds the `[function]` constant
`solutionProgram` and one unfolding rule. `verification.k` adds the
`[function, total]` symbol `sameCharsSpec(String, String)` and one
unconditional equation. `spec.k` adds seven reachability claims.

There are no local `[functional]` declarations, opaque symbols, priority
rules, `[simplification]` rules, `[owise]` rules, ordinary rules in a proof
module, auxiliary loop claims, or omitted helper K modules.

### Mapping every submitted construct

| Submitted construct | Declaration | Executing rule(s) |
|---|---|---|
| `Module` | Program production | Module/function-entry rule |
| `FuncDef` | Function production | Same entry rule |
| `Params("s0","s1")` | Params production | Same entry rule binds both values |
| `Return` | Statement production | Return scheduling and finish-return rules |
| `Compare` | Expr production | Compare-left, compare-right, and equality rules |
| `CmpOp("==", ...)` | CmpOp production | Equality-specific compare rule |
| `Call(Name("set"), E)` | Expr productions | Set-call and make-set rules |
| `Name` | Expr production | Environment lookup rule |
| String tokens | imported `STRING-SYNTAX` | K String hooks and environment rules |

No submitted construct is parsed but left without behavior.

### Equational rules

1. `charSet("") => .Set` is the correct base case.
2. For nonempty `S`, `charSet(S)` inserts the first one-code-point substring
   and recurses on the remaining substring. The guard is disjoint from the
   base case and, using K's String hooks, the recursive string is shorter.
   Imported `|Set` is mathematical union, so order and duplicates disappear.
   The equations cover all concrete K Strings and do not overlap. The absence
   of `[total]` makes symbolic `charSet(S)` remain uninterpreted; it does not
   assert an unjustified total simplification.
3. `solutionProgram` unconditionally unfolds to the exact translated body.
   It is a definitional program constant, not an execution bypass.
4. `sameCharsSpec(S0,S1)` unconditionally unfolds to
   `charSet(S0) ==K charSet(S1)`. Its `[total]` attribute is justified by
   unconditional coverage over its declared String arguments. There is no
   overlap or recursive descent obligation.

### Operational rules

1. The module-entry rule takes the sole translated function body and binds its
   two distinct actual parameter names to `<s0>` and `<s1>`. Ignoring the
   function-name token and accepting generic parameter tokens makes the small
   semantics broader than this one source program, but the fixed submitted
   term has the correct name and distinct parameters. No false conclusion on
   the intended program/input domain follows.
2. The return rule schedules expression evaluation followed by
   `finishReturn`.
3. Name lookup returns exactly the value stored under the name.
4. The set-call rule recognizes the standard builtin name and evaluates its
   argument before conversion.
5. The make-set rule converts only a `stringValue(S)` to
   `setValue(charSet(S))`.
6. The compare rule schedules the left operand first.
7. The compare-right rule preserves the evaluated left value while evaluating
   the right operand.
8. The equality rule accepts the two set values and returns their generic K
   equality. Imported K Set is associative, commutative, idempotent
   mathematical set data, and imported `==K` is total term equality.
9. The finish-return rule consumes the completed return continuation and
   changes `noResult` to exactly `result(V)`.

For the actual single-return program, these rules preserve Python's left-to-
right evaluation, binding, control, and observable result. The semantics has
no heap, output, exception, or allocation cell. Python's temporary set
allocations are unobservable in this function; string elements are hashable,
so no intended exception is omitted. The direct-entry configuration is an
explicit harness model of calling the named entry point with `S0` and `S1`.
It assumes the standard builtin `set` binding is not monkey-patched, as does
the trusted canonical execution environment.

### Soundness decision and model limitation

No local rule was found that encodes an answer independently of execution,
fabricates an unconstrained result, bypasses the submitted body, or yields a
false conclusion on the modeled intended input domain. Therefore this review
makes no unsound-rule allegation requiring a false-conclusion witness.

The important narrower gap is that `charSet` models Python's external `set`
builtin. During the universal proof its `[concrete]` equations do not expand,
and the final specification deliberately uses the same symbol. This makes the
formal theorem conditional/parametric in the audited `charSet` contract; it is
not by itself a universal connection theorem between K hooks and CPython.
That boundary is acceptable for real-program soundness because `set` is a
fixed external primitive rather than program-defined code, the equations are
truthful on their modeled ground domain, and the actual program body still
executes. It is nevertheless a reason for `CONCERNS`, because the
summary-to-natural-language bridge remains partly mathematical and empirical.

The installed K documentation also warns that its Unicode String support is
incomplete beyond Latin-1. Fresh scalar-value probes for U+0100, emoji, and
U+10FFFF agreed with Python, as did NUL and backslash cases. However, two lone
surrogate probes were rejected by K's scanner with exit 255, while CPython's
canonical function returned normal Boolean values. No K rule produced a false
answer; those Python inputs are outside the executable K token domain. The
complete probe commands and diagnostics are in `04-static-source.log`.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The reviewer authored
`/audit-output/evidence/06-spec-vacuity.k` in scratch and preserved it in the
evidence directory. It executes the actual `solutionProgram` with
`S0 = S1 = ""` but changes the result obligation to
`result(boolValue(false))`. The entry state is satisfiable, and the mutation is
demonstrably false: both Python implementations, ordinary set mathematics,
and fresh K execution return `true`.

The mutation first passed:

```text
kprove .../spec-vacuity.k --definition .../proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

with exit 0, establishing that it parsed and built. The actual selected proof
then exited 1 with `WarnStuckClaimState`. The residual is the fully executed
configuration with an empty `<k>` cell and
`result(boolValue(true))`, which cannot match the mutated required `false`.
This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash.

Evidence:

- `/audit-output/evidence/06-spec-vacuity.k`
- `/audit-output/evidence/06-nonvacuity.sh`
- `/audit-output/evidence/06-nonvacuity.log`

The proof is non-vacuous and discriminates the returned Boolean.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the submitted generated semantics, for arbitrary representable K Strings
`S0` and `S1`, if execution of the exact submitted translated program from the
initial empty environment/no-result configuration terminates, its specified
terminal configuration contains:

```text
result(boolValue(charSet(S0) ==K charSet(S1)))
```

It also establishes the six concrete prompt claims. The theorem constrains the
result, executes the body, and is sensitive to both body and postcondition.
As a partial-correctness result, it is not reported as a separate proof of
termination for every Python input.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K parser, reachability logic, Haskell/LLVM backends | All proof and execution | Accepted low-level proof-tool trust; fresh builds and cross-backend runs reduce cache risk. |
| K String hooks (`lengthString`, `substrString`, String equality/tokenization) | Character splitting, domain, termination behavior | Accepted for representable K Strings; concerning as a bridge to all CPython strings because lone surrogates are rejected and installed docs warn of incomplete Unicode support. |
| K Set hooks (`.Set`, `SetItem`, `\|Set`) and `==K` | Duplicate elimination and final Boolean | Accepted mathematical primitive boundary, documented as idempotent set union and total equality; ground behavior was independently exercised. |
| `charSet` equations | Meaning assigned to Python's external `set` builtin | Concrete, guarded, disjoint, decreasing definition; not opaque. Universal CPython equivalence is informally reasoned and finitely tested, not machine-checked. All result claims depend on this contract. |
| Direct-entry module rule | Models the external harness call | Acceptable for this fixed entry point; assumes two String arguments and the standard builtin binding. It is not a general Python module/call semantics. |
| Trusted translator and exact wrapper check | Connects `solution.py`, `solution.mpy`, and `solutionProgram` | Trusted translator matched byte-for-byte; independent wrapper equality and body-sensitivity mutation pin the proof to the real submitted program. |
| Trusted canonical Python implementation | Differential oracle | Supports only the tested bridge: 16,660 Python pairs plus 11 K/Python concrete cases and boundary probes. It does not replace the reachability proof. |
| `sameCharsSpec` | Final formal property | Truthful total abbreviation for the modeled set equality; does not replace program execution. Its connection to full CPython behavior inherits the String/Set boundary above. |

There are no local opaque values, unconstrained oracles, proof-local
simplification axioms, semantic priority shortcuts, or assumed loop
invariants.

### Gate summary

- Real-program soundness: **PASS**. The actual translated body executes; state,
  evaluation order, return control, and result are preserved; body and false
  postcondition mutations are rejected.
- Intent adequacy: **LIMITED, LEGIT**. The function and K model implement
  distinct-character set equality on representable K Strings, but the formal
  domain does not include every value CPython permits as `str`, and the
  external primitive bridge is not universally machine-checked.
- Evidence auditability: **PASS**. Commands, scopes, exit statuses, bounded
  outputs, scripts, mutation, and the initial reviewer-harness error are
  preserved under `/audit-output/evidence/`.

The limitations warrant `CONCERNS`; they do not furnish a false conclusion
witness within the K theorem's executable domain, a substituted program, a
vacuous result, or an unsound proof rule. The proof is therefore legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
