# Independent adversarial audit: 48-is-palindrome

The candidate contains a freshly reconstructable, non-vacuous partial-correctness
proof of the submitted `solution.mpy` under its generated K semantics. The proof
is result-constraining and the local semantic rules do not contain an oracle,
answer axiom, execution bypass, or false proof lemma.

The audit nevertheless finds a concrete limitation in the bridge from Python
`str` inputs to K `String` configuration values. The installed K documentation
states that non-Latin-1 string support is incomplete. Correspondingly, passing
the valid verbatim runtime input `"🙂a🙂"` through `$ARG` makes fresh `krun`
execution return `false`, while both Python implementations and a ground K proof
term return `true`. I do not attribute this to a false local rewrite rule:
the ground proof-term experiment refuted that stronger hypothesis. It is an
input-encoding/runtime bridge limitation, so the proof is legitimate but does
not provide an unqualified end-to-end validation for every Python Unicode
string.

## 1. Input and provenance integrity

### Semantics-mode boundary

This is a `GENERATED_SEMANTICS` audit. `/reference/reference-semantics` is
neither present nor a symlink, as required. The trusted mount contains exactly
the three expected regular files at its root:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

There is no trusted-mount contradiction and therefore no infrastructure breach.
The check, file types, hashes, K version, and exit statuses are recorded in
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log).

### Candidate artifact integrity

All required candidate source artifacts are present and are regular files:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The generation metadata and evidence
files `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
the structured JSONL trace are also regular files. No required artifact is
missing, mistyped, or symlinked.

The candidate prompt is byte-identical to `/reference/prompt.py` and the
candidate translator is byte-identical to `/reference/py2mpy.py`:

- prompt SHA-256:
  `6d590205867a7577346310fe8cba6e45655e25a7ef57acb964a6d34b02363081`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

`run-input.json` names problem `48-is-palindrome`, condition `bare`, and no
supplied semantics; its recorded prompt and translator hashes agree with the
trusted files.

The extra candidate directories `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, and their contents are generated
caches, not source proof artifacts. They were treated as untrusted extras and
were never copied into or used by the clean reconstruction.

The prior prose and logs claim that the candidate workflow exited zero and
printed `#Top`. Those claims were not relied upon. The read-only trace summary
and bounded command extraction are preserved by
[`evidence/inspect_generation_trace.py`](evidence/inspect_generation_trace.py)
and in the Stage 1 log.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires:

> For a Python string `text`, return `True` exactly when the string is a
> palindrome, and `False` otherwise.

The documented examples cover the empty string, two positive nonempty cases,
and one negative case. The intended typed domain is all Python `str` values;
the prompt gives no ASCII-only or Latin-1-only restriction.

The trusted canonical implementation compares mirrored characters
`text[i]` and `text[len(text)-1-i]`, returns `False` at the first mismatch, and
returns `True` after every pair agrees. The candidate Python implementation is:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

For Python strings, equality with the code-point-reversed string is equivalent
to the canonical mirrored-character loop.

### Trusted retranslation

The audit copied only source files to
`/tmp/audit-work/48-is-palindrome`, ran the trusted translator, and compared the
result with the submitted `solution.mpy`. Both files have SHA-256:

`8278b02d667e625ef15bdd083acb6461d92384f78a36828c230508569475e863`

The byte comparison exited zero. Exact commands and statuses are in
[`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports `/reference/canonical.py` and the scratch copy of `solution.py`. Its
scope was:

- all four documented examples;
- empty, one-character, even/odd, first-pair mismatch, interior mismatch, and
  center-boundary cases;
- NUL, whitespace, quoting, combining characters, Latin-1, emoji, and long
  strings;
- every string of length 0 through 5 over
  `('a', 'b', '0', 'é', '🙂', U+0301)`;
- 1,000 deterministic generated strings, seed `480048`, of lengths 0 through
  64 over a broader Unicode/control alphabet.

After deduplication, 10,312 inputs were tested: 313 returned `True`, 9,999
returned `False`, and there were zero mismatches or non-Boolean results.
The complete input/result JSONL is
[`evidence/differential_inputs.jsonl`](evidence/differential_inputs.jsonl),
SHA-256
`ca2f22438d0754a409d75f221ff62386cc4c5da2e962642246f524b5a7a04768`.

This finite differential evidence strongly supports Python implementation
fidelity. It is not used as a replacement for the K proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

### Clean source and builds

The audit copied candidate source artifacts one at a time into
`/tmp/audit-work/48-is-palindrome/source`; no candidate `*-kompiled` directory
was copied. The scratch `__pycache__` was subsequently created by the
reviewer's Python import test and is irrelevant to K compilation.

Fresh definitions were built from source with K 7.1.293:

```text
kompile .../source/semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition .../build-final/semantic-llvm-kompiled

kompile .../source/verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition .../build-final/verification-haskell-kompiled
```

Both commands exited zero. The source tree contains exactly one positive
target claim, at `spec.k:6`.

### Positive proof

The independently executed target command was:

```text
kprove .../source/spec.k \
  --definition .../build-final/verification-haskell-kompiled \
  --spec-module SPEC
```

It exited zero and printed exactly `#Top`. See
[`evidence/stage3_reconstruction.log`](evidence/stage3_reconstruction.log).

### Concrete generated-semantics execution

The fresh LLVM definition was compared with both Python implementations on 20
normal and boundary inputs. Eighteen agreed. With verbatim Unicode supplied
through the runtime configuration interface, two did not:

| Input | Trusted canonical | Candidate Python | Fresh `krun` |
|---|---:|---:|---:|
| `🙂a🙂` | `True` | `True` | `false` |
| `áa` (`a`, U+0301, `a`) | `True` | `True` | `false` |

The isolated reversal probe in
[`evidence/stage4_adequacy_and_unicode_probe.log`](evidence/stage4_adequacy_and_unicode_probe.log)
shows the runtime results:

```text
"🙂a🙂"  -> "\x82\x99\x9f\xf0a\x82\x99\x9f\xf0"
"áa"   -> "a\x81\xcca"
```

Thus the runtime path reversed the non-Latin-1 characters' encoded units, not
Python code points. This is judged further in Stages 5 and 7.

Two earlier reviewer attempts are retained as
`stage3_reconstruction_attempt1_malformed_cli.log` and
`stage3_reconstruction_attempt2_bad_result_parser.log`. They record,
respectively, a malformed reviewer `-cARG` argv shape and an over-escaped
reviewer regex. Neither is candidate evidence. The final log uses corrected
commands and parsing.

Stage 3 result: **positive proof PASS; concrete full-Unicode bridge CONCERN**.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim and no loop/helper claim.

Its precondition is an exact configuration:

- `<k>` contains the complete submitted constructor program followed by
  `#invoke("is_palindrome", PyString(S))`;
- `S` is universally quantified over K sort `String`;
- `<functions>` is `.Map`;
- `<env>` is `.Map`;
- there is no additional `requires` condition.

Its postcondition requires:

- `<k>` to contain exactly `PyBool(isPalindrome(S))`;
- `<functions>` to contain the loaded submitted function body;
- `<env>` to be restored to `.Map`.

`isPalindrome(S)` rewrites to
`S ==String reverseString(S)`. The result is therefore a specific Boolean
expression, not a free variable, one-way implication, or unconstrained
existential.

### Program identity and control flow

The `Module(FuncDef(...))` term in the claim is textually the same AST as the
trustedly regenerated `solution.mpy`: function name `is_palindrome`, parameter
`text`, and body `return text == text[::-1]`. The Stage 4 log records the exact
program, claim, semantics, and postcondition occurrences.

The claim executes the real path:

```text
Module -> #load -> #invoke -> Return -> Compare
       -> Name lookup -> Subscript/Slice -> string comparison
       -> #return -> environment restoration
```

No helper claim substitutes a different body, and no rule recognizes the
function name to fabricate the task answer.

### Satisfiable witnesses and substitution

Every entry precondition is satisfied, for example, by the exact displayed
initial cells with `S = ""`, `S = "ab"`, or `S = "aba"`.

| Satisfying `S` | Claimed modeled result | Canonical Python | Candidate Python |
|---|---:|---:|---:|
| `""` | `true` | `True` | `True` |
| `"ab"` | `false` | `False` | `False` |
| `"aba"` | `true` | `True` | `True` |

For the formal ground K term `S = "🙂a🙂"`,
[`evidence/spec-unicode-formal-expected.k`](evidence/spec-unicode-formal-expected.k)
builds and proves `PyBool(true)` with `#Top`. Supplying the visually same
verbatim token through `$ARG` instead produces `false`. This isolates the
limitation to the runtime input/representation bridge rather than the entry
claim's program identity or result constraint.

Stage 4 result: **PASS with the Unicode bridge limitation carried forward**.

## 5. Rule-by-rule static soundness review

### Complete local syntax and attribute inventory

There are no generated helper K files beyond `semantic.k`, `verification.k`,
and `spec.k`.

| Location | Local declaration(s) |
|---|---|
| `semantic.k:7` | `Program ::= Module(Stmt)` |
| `semantic.k:9-10` | `Stmt ::= FuncDef(String, Params, Stmt) \| Return(Expr)` |
| `semantic.k:12` | `Params ::= Params(String)` |
| `semantic.k:14-20` | `Expr ::= Name(String) \| Int(Int) \| Str(String) \| UnaryOp(String, Expr) \| Subscript(Expr, Slice) \| Compare(Expr, CmpOp) \| PyVal` |
| `semantic.k:22` | `CmpOp ::= CmpOp(String, Expr)` |
| `semantic.k:23` | `Slice ::= Slice(Bound, Bound, Bound)` |
| `semantic.k:24` | `Bound ::= Expr \| NoBound` |
| `semantic.k:26-28` | `PyVal ::= PyString(String) \| PyInt(Int) \| PyBool(Bool)` |
| `semantic.k:35` | `Function ::= #function(String, Stmt)` |
| `semantic.k:37-43` | `KItem ::= #load(Stmt) \| #invoke(String, PyVal) \| #return \| #returnFrame(Map) \| #compareRight(CmpOp) \| #compareValues(PyVal, String) \| #applySlice(Slice) \| #unaryMinus` |
| `semantic.k:91` | `reverseString(String) : String [function]` |
| `semantic.k:92` | `reverseStringN(String, Int) : String [function]` |
| `verification.k:7` | `isPalindrome(String) : Bool [function]` |

The configuration is exactly `<py>` containing `<k>`, `<functions>`, and
`<env>`. Every cell is read or changed by the used program path.

Local attribute totals:

- `[function]`: `reverseString`, `reverseStringN`, `isPalindrome`;
- `[total]`: none;
- `[functional]`: none;
- opaque symbols: none;
- priority rules: none;
- simplification rules: none;
- `anywhere` or macro rules: none.

Imported `String`, `Int`, `Bool`, and `Map` hooks are part of the K built-in
trust boundary, not candidate-local declarations.

### Used-construct coverage

Every constructor in `solution.mpy` is declared and modeled:

- `Module`, `FuncDef`, and `Params`: loading and invocation rules;
- `Return`: evaluation and return-frame rules;
- `Compare`, `CmpOp("==", ...)`, and `Name`: ordered left/right evaluation,
  lookup, and string equality;
- `Subscript`, `Slice`, `NoBound`, `UnaryOp("-", Int(1))`: the exact
  `[::-1]` slice bridge plus its supporting declarations;
- K `String`, `Int`, and Boolean values: imported hooks and local `PyVal`
  wrappers.

`Str` expression evaluation and the generic integer/unary-minus rules are
sound but not independently reached by this exact program's slice bound,
because the exact pure `UnaryOp("-", Int(1))` syntax is consumed by the
specialized slice rule. Missing semantics for other Python constructs is not a
defect in this generated-semantics mode.

### Exhaustive local rule inventory and decision

| # | Location | Rule role and decision |
|---:|---|---|
| 1 | `semantic.k:53` | `Module(FD) => #load(FD)`. Preserves the continuation; sound module-loading schedule for the one-function subset. |
| 2 | `semantic.k:55-56` | Loads exactly one `FuncDef` into an initially empty function map. Matches the submitted module and makes no result assumption. |
| 3 | `semantic.k:58-60` | Looks up the selected function, installs its single parameter binding, saves the old environment, and schedules a return frame. Sound for the actual one-argument call. |
| 4 | `semantic.k:63` | `Return(E)` evaluates `E` before returning. Correct evaluation order. |
| 5 | `semantic.k:64-65` | A computed `PyVal` returns and restores the saved environment. Preserves the returned value and exact relevant state. |
| 6 | `semantic.k:68` | Integer literal to `PyInt`. Ordinary literal semantics. |
| 7 | `semantic.k:69` | String literal to `PyString`. Ordinary literal semantics. |
| 8 | `semantic.k:70-71` | Name lookup from the exact environment. Correct binding for `text`; no name-based oracle. |
| 9 | `semantic.k:73` | Schedules unary-minus operand evaluation. Correct order. |
| 10 | `semantic.k:74` | Integer unary minus as `0 -Int I`. Ordinary integer mathematics. |
| 11 | `semantic.k:77` | Schedules the comparison's left expression first. Matches Python order. |
| 12 | `semantic.k:78-79` | After the left value, schedules the right expression and retains the left value/operator. Matches the used single comparison. |
| 13 | `semantic.k:80-81` | String `==` produces `PyBool(LEFT ==String RIGHT)`. Correct under the built-in K string equality contract. |
| 14 | `semantic.k:84` | Evaluates the subscript base before applying the slice. Correct for the used expression. |
| 15 | `semantic.k:85-87` | Exact bridge for `PyString(S)[::-1]` to `reverseString(S)`. It accepts only the submitted pure `NoBound, NoBound, -1` form, preserves the continuation and state, and introduces no fresh value. Sound under the modeled K-string-unit contract; the Python/K runtime encoding limitation is documented below. |
| 16 | `semantic.k:94` | Initializes reversal at `lengthString(S)`. Truthful definition over the built-in sequence operations. |
| 17 | `semantic.k:95` | Zero-length reversal returns empty. Disjoint from the recursive guard and mathematically correct. |
| 18 | `semantic.k:96-98` | Prepends the last one-unit substring and recurses on `N-1` for `N>0`. The guard is disjoint from the base case and strictly descends. Calls originating at `lengthString(S)` remain nonnegative. The helper is intentionally partial for unrelated negative `N` and is not declared `[total]`. |
| 19 | `verification.k:8` | Defines `isPalindrome(S)` as equality with the modeled reverse. This is a definitional result summary, not an execution rewrite; it has one exhaustive equation and no overlap. |

The complete numbered sources, declarations, attributes, and built-in string
documentation are preserved in
[`evidence/stage5_static_and_unicode_witness.log`](evidence/stage5_static_and_unicode_witness.log).

### Unicode boundary: narrower evidence gap, not a claimed false rule

`semantic.k:89-90` says the helper reverses Unicode code points and matches
Python. The installed K documentation at
`/usr/include/kframework/builtin/domains.md:1681` says, however, that K string
support is incomplete beyond Basic Latin and Latin-1.

The audit tested two hypotheses:

1. A ground proof term with verbatim `PyString("🙂a🙂")` reaches
   `PyBool(true)` and proves with `#Top`.
2. The same visual token passed through the concrete `$ARG` runtime interface
   reaches `PyBool(false)`.

Because the formal ground term succeeds, there is no concrete false-conclusion
witness against Rules 15-18 themselves. In accordance with the audit
requirement, those rules are not labeled unsound. The evidenced defect is
narrower: no candidate artifact defines or validates a uniform,
all-Python-`str` encoding into the K runtime configuration, and the natural
verbatim route disagrees outside Latin-1.

The failed stronger-hypothesis experiments are retained in
`stage5_static_and_unicode_witness_attempt1_escape_representation.log` and
`stage5_static_and_unicode_witness_attempt2_ground_term_check.log`; the final
classification is based on the successful final Stage 5 experiment.

Stage 5 result: **local static soundness PASS; Unicode runtime bridge CONCERN**.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; none was trusted.

The audit created a fresh mutation in scratch and preserved it as
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k). It keeps the
exact submitted program, universal input, function-map post-state, and restored
environment, but changes the result obligation to the false universal result
`PyBool(false)`.

This mutation is demonstrably false for the satisfying precondition witness
`S = ""`: fresh K execution and the candidate Python implementation both return
`true`.

The mutation:

- parsed and built successfully with `kprove --dry-run` (exit 0);
- then failed proof with exit 1;
- emitted `WarnStuckClaimState`;
- reported that destination unification succeeded but the implication check
  failed;
- left the meaningful residual condition
  `S ==String reverseStringN(S, lengthString(S))`.

This was not a parser error, timeout, missing import, or unreachable mutation.
Exact commands, statuses, residual, and witness are in
[`evidence/stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log).

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the freshly compiled candidate theory, for every abstract K `String` `S`,
starting from the exact submitted `solution.mpy` constructor program with empty
function and environment maps, execution of `is_palindrome(S)`, if it
terminates, returns:

```text
PyBool(S ==String reverseString(S))
```

equivalently `PyBool(isPalindrome(S))`; it also loads the exact submitted
function body and restores the environment to empty. The theorem is universal
over K `String`, not restricted to the four examples.

It is a partial-correctness theorem. It does not itself prove termination,
CPython implementation details outside the modeled subset, behavior on
non-`str` arguments, or a uniform external encoding of every Python Unicode
string into `$ARG`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell prover, LLVM executor, and reachability logic | Fresh build, `#Top`, mutation failure | Standard unavoidable toolchain trust boundary; independently rebuilt and exercised. |
| Built-in `Map`, `Int`, `Bool`, `==String`, `lengthString`, `substrString`, and `+String` hooks | Environment/call rules, equality, reversal | Acceptable primitive boundary for the supported K domain. Value-bearing for the final result. |
| Candidate `reverseString` and `reverseStringN` | Slice result and `isPalindrome` | Not opaque: three guarded, descending equations define the value. Sound by ordinary sequence mathematics assuming the built-in string-unit contract. |
| Candidate `isPalindrome` | Claim postcondition | Transparent definition, not an oracle. It deliberately shares the modeled reverse operation with the program result; the bridge to human “palindrome” is the standard equality-with-reverse characterization. |
| Trusted translator plus byte-identity regeneration | Program identity | Acceptable and directly checked; it establishes that the K constructor program is the translation of the submitted Python implementation. |
| Trusted canonical function and 10,312-case differential | Candidate Python versus task implementation | Strong finite empirical evidence only. It does not prove the K theorem. |
| Informal Python/K intent bridge | Meaning of `String`, slicing, and palindrome | Adequate for Basic Latin/Latin-1 and supported by ordinary mathematics and tests; concerning for unrestricted Python Unicode. |
| Runtime `$ARG` encoding of non-Latin-1 Python strings | Concrete end-to-end execution | Documented limitation. Verbatim `🙂a🙂` gives a different concrete result from Python even though the corresponding ground proof term succeeds. No uniform bridge is stated or proved. |
| Termination | Total function behavior | Outside partial correctness. Concrete executions terminate; no total-correctness theorem was claimed. |

There are no local opaque symbols, unproved priority lemmas, simplification
axioms, auxiliary circularities, or trusted program-defined helpers.

### Gate conclusions and decision

- **Real-program soundness:** pass. The exact translated program executes, the
  result is constrained, all local rules are accounted for, the sole positive
  claim freshly closes, and the false-result mutation is rejected.
- **Intent adequacy:** limited. The abstract proof matches equality with the
  modeled reverse, and both Python implementations agree broadly, but the
  concrete Python-`str`/K-`String` bridge is not valid end-to-end for all
  Unicode strings accepted by the prompt.
- **Evidence auditability:** pass. Reviewer scripts, complete differential
  inputs, exact commands, bounded logs, failed reviewer attempts, ground
  checks, and mutation evidence are preserved under `/audit-output/evidence/`.

The limitation does not make a false local rule or false formal ground claim
provable, so it is not a `FAIL / NOT_LEGIT`. It prevents an unqualified `PASS`
for the full Python `str` intent domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
