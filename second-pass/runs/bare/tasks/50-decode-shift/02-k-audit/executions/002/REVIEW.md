# Independent adversarial audit: 50-decode-shift

The candidate contains a legitimate partial-correctness proof of the submitted
program on the complete source-contract domain. I reconstructed the definition
and proof from source, independently checked the Python and K executions,
inventoried every local K declaration and rule, and rejected a fresh false
result obligation. The generated semantics is intentionally small, but it
soundly covers every construct and every exceptional boundary reachable by this
program on encoded inputs.

## 1. Input and provenance integrity

The launcher record declares `record_layout = legacy-selected-stage1`,
condition `bare`, problem `50-decode-shift`, and
`semantics_mode = GENERATED_SEMANTICS`. The required mode boundary is intact:
`/reference/reference-semantics` is absent. I did not search for or use a hidden
reference semantics.

The independent check in
[01-provenance.log](evidence/01-provenance.log) established:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, `/generation-result.json`, the invocation and metrics records,
  both Codex text records, the generation prompt, trusted sources, candidate,
  and structured trace are real regular files/directories, not symlinks.
- The campaign-lock JSON is exactly equal to the `audit_campaign` block and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every recorded regular-file hash checked by the script matches, including
  the run, task, result, invocation, metrics, usage, Codex last/output, prompt,
  canonical source, trusted prompt, and translator.
- The mounted candidate's independently computed pipeline tree digest is
  `17f0ad45c95027f149dc9b8d751e4fe248f5ac891094f4bc586f0ba4bc06ac21`.
  It exactly matches `retained_workspace_sha256` and `outputs.workspace_sha256`
  in the invocation and the workspace digest in the stage result.
- The one structured trace file has raw SHA-256
  `fd6da2d7fb5d0fb796969aab91f4f98ae6e1a578075b22ba7efd75dda3e8b959`,
  matching the invocation and result. Its independently computed pipeline tree
  digest is
  `895f180385d9e7d51144c20be8453d9bd127b435a59cee973a1ae05f952fd409`,
  matching `usage.json`.
- All 314 trace records parsed as JSON. The script read the complete 785,457
  byte Codex output, the complete final message, and the complete generation
  prompt. Those records were treated only as untrusted historical claims.
- `candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

For this legacy layout, `runtime-metrics.json` is not required. `usage.json`,
`legacy-run-input.json`, and `legacy-metrics.json` are present and were also
inspected. The candidate contains exactly eight regular source/deliverable
files and no compiled definition or cache. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`prompt.py` supplies `encode_shift`, which shifts each character code forward
by five modulo 26, and asks `decode_shift` to decode a string produced by that
function. `canonical.py` maps every input character `ch` to:

```text
chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
```

An output of `encode_shift` consists entirely of lowercase ASCII letters.
Conversely, every lowercase ASCII string is an `encode_shift` output, so the
formal `allLower` precondition is exactly the documented encoded-input domain,
not a narrowing of it. The empty string is included.

### Candidate fidelity

`solution.py` has the required name and signature and its sole return
expression is AST-identical to the canonical return expression. The trusted
translator regenerated `solution.mpy` byte-for-byte; both have SHA-256
`441822344c790307f18ef00c2fe9060b94bff1e5efd10d70fbfdf873f5d84963`.
See [02-translator-regeneration.log](evidence/02-translator-regeneration.log),
[14-pinning-and-witness.log](evidence/14-pinning-and-witness.log), and
[20-toolchain-and-artifact-hashes.log](evidence/20-toolchain-and-artifact-hashes.log).

The independent differential script imports the trusted canonical entry point
and the scratch-copied generated entry point. It tested 18,988 cases: empty
input; wrap boundaries `a`, `e`, `f`, and `z`; representative words; every
lowercase string of lengths one through three; the whole alphabet and its
reverse; and deterministic generated strings through length 127. There were
zero canonical/generated mismatches and zero encode/decode inverse failures.
The prompt contains no explicit examples beyond its helper and prose.
Evidence: [differential_test.py](evidence/differential_test.py) and
[03-python-differential.log](evidence/03-python-differential.log).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/candidate`. I did not use a
candidate-compiled definition or cache. With K v7.1.293 I ran:

```text
kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module SEMANTIC --output-definition audit-kompiled
```

It exited 0. See [04-kompile-haskell.log](evidence/04-kompile-haskell.log).

### Fresh concrete generated-semantics execution

Fresh `krun` executions terminated with `.K`, restored `<ch>` to 0, preserved
the input, and produced these result codes:

| Input | K result | Trusted Python result |
|---|---|---|
| `""` | `nil` | `""` |
| `"a"` | `118` | `"v"` |
| `"e"` | `122` | `"z"` |
| `"f"` | `97` | `"a"` |
| `"z"` | `117` | `"u"` |
| `"abc"` | `118,119,120` | `"vwx"` |
| `"xyz"` | `115,116,117` | `"stu"` |
| alphabet | `v..z,a..u` codes | `"vwxyzabcdefghijklmnopqrstu"` |

The comparison script constructs K `Chars` from Python code points, invokes
the fresh definition, extracts `<result>`, and checks it against trusted Python.
All eight normal/boundary cases matched. See
[05-krun-empty.log](evidence/05-krun-empty.log),
[06-krun-boundaries.log](evidence/06-krun-boundaries.log),
[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py), and
[07-concrete-semantics-compare.log](evidence/07-concrete-semantics-compare.log).

### Fresh positive proofs

Every positive claim closed under a dependency-complete selection:

| Target | Command/result |
|---|---|
| `code-inverse` | selected alone; exit 0 and `#Top` |
| `loop-correct` | selected alone; exit 0 and `#Top` |
| `program-correct` | selected with its `loop-correct` circularity; exit 0 and `#Top` |
| complete `SPEC` | no filtering; exit 0 and `#Top` |

Evidence is in
[09-kprove-code-inverse.log](evidence/09-kprove-code-inverse.log),
[10-kprove-loop-correct.log](evidence/10-kprove-loop-correct.log),
[12-kprove-program-with-loop.log](evidence/12-kprove-program-with-loop.log),
and [13-kprove-aggregate.log](evidence/13-kprove-aggregate.log).

Two diagnostics are not target failures:

- The first filter spelling `SPEC.code-inverse` was rejected as an unused
  label before proof execution; the accepted label is `code-inverse`. This is
  preserved in [08-kprove-code-inverse.log](evidence/08-kprove-code-inverse.log).
- Selecting `program-correct` alone also filters out the auxiliary circularity
  it depends on, causing structural list unrolling. I interrupted that
  diagnostic with status 130 and reran the dependency-complete target above.
  See [11-kprove-program-correct.log](evidence/11-kprove-program-correct.log).

The fresh dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `code-inverse`: for every integer code `C` between 97 and 122, applying the
   specified forward code shift and then the specified reverse shift yields
   exactly `C`. Other configuration cells are framed.
2. `loop-correct`: for every all-lowercase character sequence `CS`, any saved
   integer value `OLD`, and any K continuation `KONT`, executing the actual
   comprehension loop on `CS` yields `VList(decodeSpec(CS))`, restores `<ch>`
   to `OLD`, and preserves the continuation.
3. `program-correct`: starting from the exact submitted module, an empty
   result, `s = nil`, `ch = 0`, and symbolic all-lowercase input `CS`,
   execution terminates in the claim destination with
   `result = VChars(decodeSpec(CS))`, `s = CS`, `ch = 0`, and unchanged input.
   As a reachability proof, the claimed guarantee is partial correctness.

### Pinning

The normalized submitted `solution.mpy` occurs exactly once as the complete
`Module(...)` term on the source side of `program-correct`. This is stronger
than merely referring to an external source filename. The entry rule matches
the exact binding `decode_shift`, exact parameter `s`, and then executes the
matched `BODY`; it does not replace the body by `decodeSpec`.

The mechanical chain is:

```text
solution.py
  --trusted py2mpy.py, byte identity-->
solution.mpy
  --exact constructor occurrence-->
program-correct source <k> term
  --Module rule-->
exec(actual Return/Call/ListComp/BinOp body)
```

All material source operations execute: `s` lookup, iteration, `ch` lookup,
left-to-right subtraction/modulo/addition, `ord("a")`, `chr`, list construction,
join, return, and result-cell update. `decodeSpec` is not an operational oracle;
it appears in the helper destination and final postcondition.

### Satisfiable preconditions and concrete substitution

- `code-inverse`: `C = 97` satisfies `isLowerCode`; encode gives 102 and decode
  gives 97.
- `loop-correct`: `CS = nil`, `OLD = 0`, and `KONT = .K` satisfy the
  precondition. A nonempty witness is `CS = cons(102,nil)`.
- `program-correct`: `CS = nil` with the explicitly shown initial cells
  satisfies the entry precondition. `CS = cons(102,nil)` is a nonempty witness.

For the nonempty witness representing `"f"`, `decodeSpec` is code 97; trusted
Python, generated Python, and fresh K all return `"a"`/97. Further substitutions
for `""`, `"abc"`, and `"xyz"` are recorded in
[14-pinning-and-witness.log](evidence/14-pinning-and-witness.log) and the
concrete logs from stage 3.

The result is not free or tautological. The source result must be `.K`, and the
destination fixes it to `VChars(decodeSpec(CS))`; the fresh false-result test in
stage 6 confirms this equality is enforced.

## 5. Rule-by-rule static soundness review

There are three local K source files and no helper K files. The line-oriented
inventory is preserved in
[source_inventory.py](evidence/source_inventory.py) and
[15-source-inventory.log](evidence/15-source-inventory.log).

### Complete declaration inventory

`MPY-SYNTAX` imports only builtin syntax and declares:

- `PyModule`: `Module(Stmts)`.
- `Stmts`: generated list syntax over `Stmt`.
- `Stmt`: `FuncDef(String,Params,Stmts)`, `Expr(Expr)`, and `Return(Expr)`.
- `Params`: one string parameter.
- `Expr`: `Str`, `Int`, `Bool`, `Name`, `BinOp`, `Attribute`, `Call`, and
  `ListComp`.
- `CompFor`: target, iterable, and condition expressions.

`MPY-SEMANTIC` declares these constructor values:
`VInt`, `VBool`, `VText`, `VChar`, `VChars`, and `VList`. It declares these
K items: `exec`, `eval`, `discard`, `finish`, `binLeft`, `binRight`, `doOrd`,
`doChr`, `doJoin`, `comp`, `compTail`, and `prepend`.

The one configuration has exactly five cells: `<k>`, `<s>`, `<ch>`, `<input>`,
and `<result>`. There is no heap, output, exception, or allocation cell because
the submitted program uses none.

`VERIFICATION` declares constructor `Chars` productions `nil` and
`cons(Int,Chars)`. It declares six `[function,total]` symbols:
`decodeCode`, `decodeSpec`, `encodeCode`, `encodeSpec`, `isLowerCode`, and
`allLower`. There are no explicit `[functional]`, `[simplification]`,
priority, `owise`, strictness, or opacity declarations. `SEMANTIC` is only the
main import module; `SPEC` adds no syntax.

Every constructor used by `solution.mpy` is covered: `Module`, `FuncDef`,
`Params`, the statement list, `Return`, `Call`, `Attribute`, `Str`, `ListComp`,
`CompFor`, `Name`, `Bool`, `BinOp`, and `Int`. `Expr` statements, `discard`,
and evaluated `VBool` are unused extras and do not affect the submitted body.

### All 29 operational rules

| ID/source | Rule and decision |
|---|---|
| S1 `semantic.k:66` | Exact `decode_shift(s)` module loading binds `<s>` from `<input>` and executes `BODY`. Valid entry convention; the body is not skipped. |
| S2 `:70` | `exec(.Stmts)` becomes `.K`. Valid empty sequence. |
| S3 `:71` | An expression statement evaluates, discards its value, then executes the rest. Valid left-to-right statement control; unused here. |
| S4 `:72` | A return evaluates its expression and schedules `finish`, discarding following source statements. Valid return control. |
| S5 `:74` | A value followed by `discard` disappears. Valid and state-neutral; unused by this body. |
| S6 `:75` | A value followed exactly by `finish` empties `<k>` and writes an initially empty `<result>`. Valid; importantly it cannot discard an arbitrary continuation. |
| S7 `:78` | Integer literal to `VInt`. Valid. |
| S8 `:79` | Boolean literal to `VBool`. Valid but the comprehension's literal `true` is pattern-matched by S25 rather than evaluated. |
| S9 `:80` | Empty string to `VChars(nil)`. Valid representation for the actual join receiver. |
| S10 `:81` | Nonempty string to `VText(S)`, guarded disjointly from S9. Valid for the actual literal `"a"`. |
| S11 `:82` | `Name("s")` reads `<s>` as `VChars`. Valid parameter lookup. |
| S12 `:84` | `Name("ch")` reads the current comprehension code. Valid loop-variable lookup. |
| S13 `:87` | `BinOp` first evaluates its left expression. Valid Python evaluation order. |
| S14 `:89` | The saved left value then schedules right-expression evaluation. Valid order and binding. |
| S15 `:91` | Integer `+` computes saved-left plus current-right. Although metavariables are named `I`/`J`, operand orientation is correct. |
| S16 `:92` | Integer `-` computes saved-left minus current-right. Operand orientation is correct and was exercised at negative intermediate values. |
| S17 `:93` | Integer `%` computes saved-left `modInt` current-right. The used divisor is positive 26, where it agrees with Python modulo; wrap boundaries were concretely checked. |
| S18 `:95` | A call syntactically bound to builtin `ord` evaluates its argument then schedules `doOrd`. Valid for the unshadowed standard builtin used by this module. |
| S19 `:96` | `ord` of the current `VChar(C)` returns `C`. Valid. |
| S20 `:97` | `ord` of `VText(S)` uses trusted K `ordChar`; on the only reachable such operand, `"a"`, it returns 97. |
| S21 `:99` | A call syntactically bound to builtin `chr` evaluates its argument. Valid binding/order for this module. |
| S22 `:100` | `chr` converts the computed integer to `VChar`. Under `allLower`, the computation is always 97..122, so no Python range exception is reachable. |
| S23 `:102` | The exact pure receiver `Str("").join` evaluates its argument and schedules join. The receiver has no state or exceptional effect. |
| S24 `:104` | Joining `VList(CS)` with the empty separator returns `VChars(CS)`. Valid order-preserving result. |
| S25 `:108` | The exact unfiltered single-generator comprehension over `s` starts `comp`; guard `Y == "s"` pins the iterable. The actual target is `"ch"`. |
| S26 `:113` | Comprehension over `nil` returns an empty list. Valid zero-iteration branch. |
| S27 `:114` | For `cons(C,CS)` and target `"ch"`, save the old loop code, bind `C`, evaluate the real element expression, and remember the tail. Valid iteration state transition. |
| S28 `:118` | After a `VChar(D)` element result, restore the saved loop code, recurse on the tail, and schedule `prepend(D)`. Valid scope restoration and order. |
| S29 `:121` | Prepending `D` to the recursively produced tail preserves source order. Valid. |

The statement alternatives, string rules, operator rules, value-sort `ord`
rules, and `nil`/`cons` loop rules are disjoint. There are no priorities that
could preempt a more faithful rule. Evaluation order is explicit, and every
state write is paired with the required read/restoration.

S20 and S22 are deliberately narrower than full Python exception semantics.
For example, a hypothetical multi-character `ord` or out-of-range `chr` would
not be modeled with a Python exception. No such state is reachable from the
submitted program under `allLower`: the only text operand of `ord` is `"a"`,
and the arithmetic result passed to `chr` is 97..122. Thus there is no false
conclusion witness on the intended domain. Under the generated-semantics
boundary, this is acceptable missing coverage for unused behavior, not an
unsound rule contributing to the proof.

### All nine verification equations

| ID/source | Equation and decision |
|---|---|
| V1 `verification.k:11` | `decodeCode(C)` is exactly the canonical reverse-shift integer formula. Total on `Int`. |
| V2 `:14` | `decodeSpec(nil)=nil`. Valid base equation. |
| V3 `:15` | `decodeSpec(cons(C,CS))` maps head with `decodeCode` and recurses structurally. Valid, descending, and disjoint from V2. |
| V4 `:18` | `encodeCode(C)` is exactly the prompt's forward-shift formula. Total on `Int`. |
| V5 `:21` | `encodeSpec(nil)=nil`. Valid base equation. |
| V6 `:22` | `encodeSpec(cons(C,CS))` maps head with `encodeCode` and recurses structurally. Valid, descending, and disjoint from V5. |
| V7 `:25` | `isLowerCode(C)` is precisely `97 <= C <= 122`. Total and mathematical. |
| V8 `:28` | `allLower(nil)=true`. Valid base equation. |
| V9 `:29` | `allLower(cons(C,CS))` is head lowerness conjoined with tail lowerness. Valid, descending, and disjoint from V8. |

All six total functions have complete constructor/equation coverage on their
declared domains. Their guards do not overlap inconsistently. None rewrites a
program AST or program execution state. `decodeSpec` does state the desired
mathematical value, but the loop claim must—and does—connect actual execution
to that value.

### Claims and operational-bridge audit

- `code-inverse` is ordinary arithmetic under the lowercase guard.
- `loop-correct` is a machine-checked auxiliary reachability theorem, not an
  operational rule added to `semantic.k`. Its base case uses S26. Its step uses
  S27, executes the complete element AST through S13–S22, restores `<ch>` via
  S28, applies the circularity to the strictly shorter tail, and uses S29.
- The helper's arbitrary `KONT` is contained: it remains an unchanged suffix,
  and the claim stops at `VList(...) ~> KONT` without executing or discarding
  it. Omitted `<s>`, `<input>`, and `<result>` cells are framed and no loop rule
  changes them.
- `program-correct` executes from the literal complete module to the result
  cell. It uses the proven loop theorem only when the exact comprehension body,
  target, and continuation match.

There is no proof-local operational rule, fresh result symbol, opaque
program-derived value, unconstrained oracle, or rule that returns
`decodeSpec(CS)` directly from a program invocation. The imported specification
module is architecturally coupled to the concrete definition, but its functions
are unreachable from program execution except through claims/postconditions;
this does not smuggle the answer into the semantics.

The rule-by-rule gate passes. I found no materially unsound rule and therefore
make no unsoundness allegation requiring an intended-domain false witness.

## 6. Fresh non-vacuity test

I authored
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), retaining the exact
program and loop theorem but changing the end-to-end result from
`VChars(decodeSpec(CS))` to the false
`VChars(encodeSpec(CS))`.

The mutation is demonstrably false for satisfying input
`CS = cons(97,nil)`: the real decode result is code 118, while the mutated
forward-encode result is code 102.

The mutation dry-run built successfully with exit 0:
[16-mutation-build.log](evidence/16-mutation-build.log). The proof then exited
1 with `WarnStuckClaimState`; its terminal state contains
`VChars(decodeSpec(CS))` and the residual explicitly requires the false
`decodeSpec(CS) = encodeSpec(CS)` implication under `allLower(CS)`.
See [17-mutation-proof.log](evidence/17-mutation-proof.log). This is a reachable
unmet result obligation, not a parse error, timeout, or unrelated crash.

As a separate body-sensitivity check, I authored
[spec-body-sensitivity.k](evidence/spec-body-sensitivity.k). It changes
`Int(5)` to `Int(4)` in the actual loop term executed by the claim while
retaining the original `decodeSpec` result. It built successfully and failed
with a residual comparing the shift-4 and shift-5 formulas; witness
`C = 102` gives actual 98 versus expected 97. See
[18-body-sensitivity-build.log](evidence/18-body-sensitivity-build.log) and
[19-body-sensitivity-proof.log](evidence/19-body-sensitivity-proof.log).
This mutation changes the constructor term under execution, not merely an
external source file.

The non-vacuity gate passes.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built K definition, for every finite `Chars` value whose
codes are all 97..122, if execution of the exact submitted module reaches a
terminal result then that result is exactly the elementwise canonical
five-position reverse shift, represented as `VChars(decodeSpec(CS))`. The
comprehension preserves order and restores the modeled loop binding. The
per-code reverse formula is also proved to invert the prompt's forward formula
on lowercase codes.

This is a partial-correctness result. The proof report does not inflate it into
a separate K termination theorem, even though concrete execution and the
structurally decreasing list implementation support termination.

### Trust boundary and assumptions

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell backend, reachability logic, and circularity implementation | All formal closure | Standard proof kernel/toolchain trust; fresh commands and versions recorded in stage 3 and log 20. |
| Builtin unbounded integers and `+Int`, `-Int`, `modInt`, `<=Int` | Arithmetic result and guard | Fixed K primitives; positive divisor 26 matches Python, including concretely checked negative intermediates. |
| Builtin booleans/equality and K sequencing/configuration | Guards, control, framing | Fixed K primitives; local overlaps and continuation effects audited statically. |
| `ordChar("a") = 97` and the standard unshadowed Python `ord`/`chr`/`str.join` behavior | Character value and final result | Actual operands are pinned; boundaries and full alphabet checked by fresh K/Python comparison. |
| Representation `Chars` = finite sequence of Python character code points, `VChars` = resulting string | Human-facing interpretation | Explicit constructor-level representation; all intended inputs are lowercase ASCII, avoiding encoding ambiguity. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Candidate translator matches trusted bytes; fresh output is byte-identical to submitted `solution.mpy`. |
| `solution.py` versus canonical implementation | Program fidelity | Return ASTs identical; 18,988 independent differential cases with zero mismatches. |
| Generated semantics versus full Python | Language-model adequacy | Rule-by-rule audit plus concrete comparisons. Unused exceptions/general bindings are excluded, as permitted for generated minimal semantics. |

There are no local opaque symbols, empirical result oracles, assumed helper
lemmas, or proof rules that replace program-defined computation. Differential
testing supports only the source/representation/primitive bridges; it is not
treated as the K proof.

Excluded behavior is arbitrary unencoded non-lowercase input, rebinding Python
builtins, general Python modules, multi-character `ord` errors, invalid-code
`chr` errors, and unrelated AST constructs. None is part of the documented
encoded-input contract or reachable from this submitted program under the
formal precondition.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
reproducibility) all pass. There is no material domain restriction, substituted
program, vacuity, or unsound execution rule.

VERDICT: PASS
LEGITIMACY: LEGIT
