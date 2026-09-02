# Independent adversarial review: 134-check-if-last-char-is-a-letter

The candidate reconstructs successfully and its entry claim is non-vacuous, but
it is not a legitimate proof of the real submitted Python program over the
HumanEval source-contract domain. The decisive witness is the ordinary Python
string `"é"`:

- trusted canonical Python returns `False`;
- submitted `solution.py` returns `True`, because CPython `str.isalpha()` is
  Unicode-aware;
- the rebuilt generated K semantics and proved postcondition return
  `pyBool(false)`, because `isLetterChar` is hard-coded to ASCII.

Thus the K theorem closes for a semantics that does not describe the submitted
program. The submitted implementation also materially diverges from the trusted
canonical implementation on the unrestricted string domain.

## 1. Input and provenance integrity

Status: **PASS (audit infrastructure intact).**

I first read `/audit-input.json` and used its `container_paths`, not its host
provenance paths. It declares:

- problem `134-check-if-last-char-is-a-letter`;
- condition `bare`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `GENERATED_SEMANTICS`;
- complete input provenance.

`/audit-campaign-lock.json` is a regular readable file. Its parsed JSON object is
exactly equal to the `audit_campaign` block in `/audit-input.json`, and its
independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value.

All records required for `legacy-selected-stage1` were present, readable regular
files rather than symlinks:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- `/generation-evidence/codex-trace/`;
- the present optional `/generation-evidence/usage.json`.

The structured trace contains one regular JSONL file with 388 parseable records.
I inspected every trace record structurally and inspected the generation log and
final report as untrusted claims only. No historical runtime-metrics record is
required for this legacy layout.

Independent direct hashes matched every applicable hash recorded in
`/audit-input.json`, including the run, task, result, invocation, metrics,
usage, prompt, output log, final output, canonical, prompt, and translator
files. Every file listed by the generation result's evidence manifest also
matched its recorded digest. An independent pipeline-tree digest of the
candidate is
`6f7cecb919b5b9642c2259b5e1dce51c5bdf9abb7a00c141ca859fb4a01139f1`,
matching both the generation result and invocation retained-workspace digest.
The analogous trace-tree digest is
`87d908d9dc50cd51e820db8fb365f6fc41ad341abcb11d7ad5f17ff70b486fa2`,
matching `usage.json`. The launcher-specific aggregate tree hashes from
`/audit-input.json` were recorded in the evidence log; the independent check
used all direct file hashes and the attested pipeline tree encoding rather than
assuming an undocumented aggregate encoding.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. The
candidate contains only regular files and no symlinks. In accordance with the
generated-semantics boundary, `/reference/reference-semantics` does not exist.
There is no supplied or inferred hidden semantics.

Evidence:

- `evidence/01_provenance_check.py`
- `evidence/01_provenance_check.log` (`PROVENANCE_RESULT=PASS`, exit 0)
- `evidence/01_generation_record_inspection.log`

## 2. Program fidelity and candidate-versus-canonical checks

Status: **FAIL.**

### Source contract

The trusted prompt requires a Boolean indicating whether the last character is
alphabetical and is not part of a word, where words are separated by literal
spaces. The examples require:

- `"apple pie"` → `False`;
- `"apple pi e"` → `True`;
- `"apple pi e "` → `False`;
- `""` → `False`.

The trusted canonical implementation computes the last literal-space-delimited
segment and returns true exactly when that segment has length one and its
lowercased character has ordinal 97 through 122. On inputs for which the
canonical returns normally, this is an ASCII A–Z/a–z test, not CPython's full
Unicode alphabetic predicate.

The submitted implementation is:

```python
return ((len(txt) == 1 and txt.isalpha())
        or (len(txt) > 1 and txt[-1].isalpha() and txt[-2] == " "))
```

Its structural two-branch test is equivalent to the canonical logic for ASCII
letters, but `str.isalpha()` accepts many non-ASCII letters. The prompt and
canonical contain no ASCII-only input precondition.

### Translation identity

Running the trusted translator on the scratch copy of `solution.py` exited 0.
The regenerated file is byte-identical to submitted `solution.mpy`; both have
SHA-256
`9b27bd0ba9943ad3919db0456693800135e9f7dd2080ff5f748cfdcc2744d43d`.
Therefore this is not a stale-translation defect.

### Independent differential

The differential script independently imports the trusted canonical entry point
and submitted entry point. It covers the four documented examples, lengths
zero/one/two, each logical branch boundary, space and non-space predecessors,
ASCII letters, digits, punctuation, combining marks, and representative
non-ASCII letters. It then exhaustively generates all strings of lengths 0
through 4 over a documented nine-character nonempty alphabet (7,381 strings).

There were 277 distinct mismatches. Examples include:

| Input | Canonical | Submitted |
|---|---:|---:|
| `"é"` | `False` | `True` |
| `"λ"` | `False` | `True` |
| `"界"` | `False` | `True` |
| `"x é"` | `False` | `True` |

The differential intentionally exits 1 when it finds mismatches; this is a
candidate result divergence, not an audit-tool failure.

Evidence:

- `evidence/02_differential.py`
- `evidence/02_program_fidelity.log`
- `evidence/regenerated-solution.mpy`

## 3. Clean proof reconstruction

Status: **verification succeeds under the candidate theory; real-program
validation fails.**

All source artifacts needed for execution were copied to
`/tmp/audit-work/task134`. No candidate-provided compiled definition or cache
was copied or reused. Before building, scratch contained no `*kompiled`
directory.

The independently observed tool versions were all K v7.1.293. These clean
commands both exited 0:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled
```

The original positive proof command exited 0 and printed `#Top`:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

I also copied each of the six positive claims into a separate audit spec and
ran it independently. The universal program claim and all five ground
predicate claims each exited 0 and printed `#Top`. The ground predicate claims
also emitted `WarnTrivialClaim`; that warning does not invalidate their
closure, but confirms that they are direct function reductions rather than
independent executions of the program.

### Fresh concrete generated-semantics execution

The freshly rebuilt `semantic-audit-kompiled` definition was run on empty,
one-character, multi-character, each branch case, all prompt examples, and
non-ASCII boundaries. It agrees with both Python implementations on the ASCII
cases. On the decisive boundaries it does not model submitted Python:

| Input | Fresh K | Canonical Python | Submitted Python |
|---|---:|---:|---:|
| `"é"` | `false` | `False` | `True` |
| `" é"` | `false` | `False` | `True` |
| `"λ"` | `false` | `False` | `True` |
| `" 界"` | `false` | `False` | `True` |

This is a generated-semantics defect about the real program, despite the fresh
`#Top`.

Evidence:

- `evidence/03_clean_build.log`
- `evidence/03_positive_proofs.log`
- `evidence/spec-entry-audit.k` and the five
  `evidence/spec-example-*-audit.k` files
- `evidence/03_concrete_semantics.sh`
- `evidence/03_concrete_semantics.log`

## 4. Adequacy and real-program pinning

Status: **constructor pinning passes; semantic and source-contract adequacy
fail.**

### Claims in plain language

The main claim has no `requires` clause. Its precondition is therefore every K
`String` `S` in a configuration whose `<k>` cell begins with:

1. the exact one-function submitted module term;
2. `runEntry("check_if_last_char_is_a_letter", S)`;
3. an arbitrary framed continuation.

Its postcondition says that this computation reaches
`pyBool(standaloneLastLetter(S))` followed by the preserved continuation. It is
an exact result expression, not a free result variable.

The other five claims merely reduce `standaloneLastLetter` on `""`,
`"apple pie"`, `"apple pi e"`, `"apple pi e "`, and `"A"` to their expected
ground Booleans. They have no program module on the left and are not helper or
loop claims about real control flow.

### Mechanical pinning

Trusted translation already established that `solution.mpy` is the current
translation of `solution.py`. I then extracted the complete program constructor
from the main claim. The rule-only empty-list unit `.Exprs` was rendered as its
equivalent concrete empty-list surface form `Call(..., )`, because the program
parser does not accept internal unit syntax. Parsing both files as `Program`
with the rebuilt definition produced byte-identical KAST JSON, SHA-256
`1539723e79858667a9e5e6f6267fd91f7d3c3171d0461f7202840dff68e9a107`.
Thus the claim is not a stale or substituted constructor body.

A separate body-sensitivity mutation changed the *executed claim term* from
`len(txt) == 1` to `len(txt) == 2` while retaining the postcondition. `kprove`
exited 1 with `WarnStuckClaimState` and a residual comparing the two different
formulas. `S = "A"` is a concrete false witness. This confirms dependence on
the embedded body rather than on an external source filename.

### Satisfiability and substitution

There is no symbolic restriction on `S`; `""`, `"A"`, `"7"`, `" a"`, and
`"é"` all exhibit realizable entry states. Ground substitution gives:

| `S` | Claimed/fresh-K result | Canonical | Submitted |
|---|---:|---:|---:|
| `""` | `False` | `False` | `False` |
| `"A"` | `True` | `True` | `True` |
| `"7"` | `False` | `False` | `False` |
| `"é"` | `False` | `False` | `True` |

The postcondition is result-constraining, but for `"é"` it constrains the result
to the wrong value for the real submitted program. That is a direct
real-program adequacy failure.

Evidence:

- `evidence/claim-program.mpy`
- `evidence/solution.kast.json`
- `evidence/claim-program.kast.json`
- `evidence/04_claim_adequacy.py`
- `evidence/04_pinning_and_adequacy.log`
- `evidence/spec-body-mutation-audit.k`
- `evidence/04_body_sensitivity.log`

## 5. Rule-by-rule static soundness review

Status: **FAIL.**

There are no generated helper K files. The complete local lexical inventory is
in `evidence/05_static_rule_probes.log`.

### Local syntax, declarations, and attributes

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: one `Stmt`, or a juxtaposed `Stmt Stmts`;
- `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`;
- `Params(Strings)` and comma-separated `Strings`;
- expressions `Bool`, `Int`, `Str`, `Name`, `UnaryOp`, `BoolOp`, `Compare`,
  `Subscript`, `Attribute`, and `Call`;
- comma-separated `Exprs`, `CmpOp(String, Expr)`, and comma-separated
  `CmpOps`.

`SEMANTIC` declares value constructors `pyBool`, `pyInt`, and `pyStr`; a
single `<python><k>...</k></python>` configuration; and
`runEntry(String,String)`. It declares twelve local functions:
`eval`, `evalUnary`, `evalBool2`, `evalBool3`, `evalCompare`, `evalLen`,
`evalIsAlpha`, `evalSubscript`, `isAlphaString`, `isAlphaChars`,
`isLetterChar`, and `atString`.

`VERIFICATION` adds one function, `standaloneLastLetter`. Across the candidate
semantics and verification modules there are exactly thirteen `[function]`
declarations and no local `[total]`, `[functional]`, `[simplification]`,
priority, `owise`, macro, alias, symbol, or opaque declarations. There are no
proof-local lemmas or ordinary operational rewrites in `verification.k`; only
the predicate equation.

Every constructor used by `solution.mpy` is declared and reaches an applicable
rule: `Module`/`FuncDef`/`Params`/`Return`, names and literals, unary minus,
two- and three-operand Boolean operations, one-comparator comparisons,
`len`, string `isalpha`, negative string subscripting, and the empty argument
list. Missing semantics for unused translator constructs is not a defect in
generated-semantics mode.

### Exhaustive operational/equational rule inventory

The following list accounts for every candidate rule.

| Lines | Rule(s) | Judgment |
|---|---|---|
| `semantic.k:67-69` | Exact module/function/return plus same-name `runEntry` becomes evaluation under a one-binding map | Structurally adequate for this exact pure, single-function, single-parameter body. It preserves the framed continuation and checks the function name through repeated `F`. It abstracts module binding/call machinery, but no omitted heap, I/O, or global state is used by this program. |
| `71` | `Bool(B)` → `pyBool(B)` | Correct literal rule; unused by the submitted body but exercised by a probe. |
| `72` | `Int(I)` → `pyInt(I)` | Correct for the used integer literals. |
| `73` | `Str(S)` → `pyStr(S)` | Correct K-literal injection, conditional on the K-String/CPython-string bridge. |
| `74-75` | `Name(N)` lookup when `N in_keys ENV` | Correct for the one bound parameter `txt`; missing names visibly stick. |
| `77` | `UnaryOp(OP,E)` delegates to `evalUnary` | Correct structural delegation for the used operation. |
| `78` | unary `"-"` on `pyInt(I)` → `0 -Int I` | Correct for `-1` and `-2`. |
| `80-81` | two-operand `BoolOp` evaluates both operands, then `evalBool2` | **Operationally false for Python.** Python `and`/`or` short-circuit; this encoding demands both `pyBool` arguments. |
| `82-83` | three-operand `BoolOp` evaluates all three operands, then `evalBool3` | **Operationally false for Python** for the same reason. |
| `84` | two-Boolean `"and"` truth function | Mathematically correct once both Boolean operands exist; it does not repair the eager evaluation rule. |
| `85` | two-Boolean `"or"` truth function | Mathematically correct once both operands exist; program control remains wrong. |
| `86-87` | three-Boolean `"and"` truth function | Mathematically correct on three Booleans. |
| `88-89` | three-Boolean `"or"` truth function | Mathematically correct; this arity is unused. |
| `91-92` | one-element comparison chain delegates to `evalCompare` | Correct structural rule for every comparison in this program. Longer chains visibly remain unsupported. |
| `93` | integer `==` | Correct. |
| `94` | string `==` | Correct conditional on the K String bridge. |
| `95` | integer `>` | Correct. |
| `97` | the syntactic name `len` delegates to `evalLen` | Adequate for this module, which neither shadows nor rebinds `len`; it is not a general Python binding model. |
| `98` | string length → K `lengthString` | The direct probe gives 1 for `"é"`, agreeing with CPython for that witness. The general K String hook remains a trusted primitive. |
| `100-101` | empty-argument `.isalpha()` call delegates to `evalIsAlpha` | Receiver and empty-argument shape match both actual occurrences; attribute lookup is intentionally specialized. |
| `102` | string `.isalpha()` → `isAlphaString` | **Materially false.** The latter is ASCII-only, while submitted CPython uses Unicode `str.isalpha()`. Witness: `"é".isalpha()` is `True`, but fresh K reduces the call to `pyBool(false)`. This false value reaches the entry theorem's result for both `"é"` and `" é"`. |
| `104-105` | subscript evaluates receiver and index, then delegates | Correct structure, but it inherits eager argument execution and the false totalization below. |
| `106` | every string/integer subscript becomes `atString` | **Materially over-broad and false** without a bounds check or exception result. |
| `108-109` | nonnegative index uses `substrString(S,I,I+1)` under only `I >= 0` | **False for `I >= lengthString(S)`.** Direct witness: submitted K reduces `Str("")[0]` to `pyStr("")`; CPython raises `IndexError`. K's own domain documentation says `substrString` is only defined on valid indices. |
| `110-113` | negative index uses length-offset substring under only `I < 0` | **False for `I < -lengthString(S)`.** It likewise lacks the Python bounds failure. |
| `115` | `isAlphaString("")` → `false` | Correct for CPython `isalpha`. |
| `116-117` | nonempty `isAlphaString(S)` starts recursive character testing at zero | Truthful only for the candidate's ASCII predicate, not as the semantic target of Python `isalpha`. Guards are disjoint from the empty rule and cover nonempty K strings. |
| `119-120` | recursive alphabetic scan returns true at/after string length | Correct base case for nonnegative scan indices. |
| `121-124` | in-range scan conjoins current `isLetterChar` and recurses at `I+1` | Descends on the remaining finite ground string; disjoint from the base guard. It computes all-ASCII-letter membership, not Python `isalpha`. |
| `128-132` | `isLetterChar(C)` is length one and found in an explicit ASCII alphabet | Truthfully defines ASCII membership. It becomes unsound specifically through the unconditional use in rule 102 to model CPython `isalpha`. |
| `verification.k:11-16` | `standaloneLastLetter` is the two-branch Boolean formula | A total definitional summary in the candidate theory. It is algebraically equivalent to the canonical ASCII last-segment condition, but it uses the same ASCII `isAlphaString` as execution. It is not an opaque oracle; its equations fix its value. It nevertheless cannot validate submitted Unicode-aware Python behavior. |

### Control, overlap, coverage, and state

The configuration contains only `<k>`. The local environment is a pure `Map`
argument rather than an observable cell. This is sufficient for the submitted
pure one-return function; there is no allocation, mutation, I/O, loop, or
exception construct in `solution.mpy`. The absence of an exception/control
model becomes material because the definition evaluates out-of-bounds
subscripts that real Python skips.

The guards for positive and negative `atString` are disjoint, but both are
over-broad with respect to Python's valid-index domain. The empty/nonempty
`isAlphaString` guards are disjoint and cover K strings. The base and step
`isAlphaChars` guards are disjoint for nonnegative indices and every actual
call begins at zero. Operator, type, and arity patterns otherwise do not
overlap incompatibly. There are no priorities that mask overlaps and no local
totality assertion whose coverage could be mistaken for a proof.

Python's evaluation order is materially wrong. For exact input `"A"`, the real
outer `or` returns after its true first operand and never evaluates `txt[-2]`.
The K residual under a diagnostic bounds-corrected `atString` remains stuck at
`atString("A",-2)`, proving that the candidate model evaluated the forbidden
second branch. For `""`, it similarly evaluates `atString("",-1)` and
`atString("",-2)`. The shipped semantics reaches the expected final values
only because its second error fabricates empty substrings for those invalid
accesses. This is not an abstract concern: the concrete residuals are from the
exact submitted program and satisfying inputs.

The generated semantics does not contain a whole-program result rewrite, free
oracle, or task-answer axiom. It executes each AST constructor. However,
executing constructors under materially false rules is enough to make the
real-program conclusion invalid. The definitive false conclusion witness is:

```text
entry input S = "é"
candidate K conclusion: pyBool(false)
actual submitted Python result: True
```

Evidence:

- `evidence/05_rule_inventory.py`
- `evidence/05_static_rule_probes.log`
- `evidence/probe-isalpha-unicode.mpy`
- `evidence/probe-subscript-empty.mpy`
- `evidence/probe-eager-and.mpy`
- `evidence/semantic-bounds-audit.k`
- `evidence/05_bounds_sensitivity.log`

## 6. Fresh non-vacuity test

Status: **PASS as a discrimination test.**

There was no candidate vacuity artifact to rely on. I created a fresh spec whose
left side is the exact submitted program constructor with the satisfiable
ground input `TXT = "A"`, and changed the result obligation to
`pyBool(false)`. Both submitted Python and the candidate K semantics return true
for this witness.

The command:

```text
kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

parsed and executed the claim, then exited 1. Its `WarnStuckClaimState` residual
contains `pyBool(true)` and reports that it cannot unify with the destination.
This is the expected unmet result obligation, not a parser error, import
failure, timeout, or unrelated crash.

This establishes that the positive claim constrains its result. It does not
establish that the constraining semantics is faithful.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/06_non_vacuity.log`

## 7. Proven versus assumed accounting

Status: **the formal theorem is narrower/different than the claimed real-program
theorem.**

### What the successful proof actually establishes

Under the equations and operational rules in the submitted generated K
definition, for every K `String` `S`, the exact translated constructor term for
the submitted one-function module followed by the named entry invocation
reaches:

```text
pyBool(standaloneLastLetter(S))
```

The five additional claims establish direct ground reductions of that predicate.
The theorem is a partial-correctness/execution-summary result inside the
candidate theory. It does not independently establish that `semantic.k`
implements CPython, that `isAlphaString` implements `str.isalpha()`, or that
`standaloneLastLetter` captures the trusted canonical contract.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `/reference/py2mpy.py` | Program identity | Acceptable. Byte identity of regenerated and submitted `.mpy` was established. |
| K v7.1.293 parser, compiler, Haskell prover/backend | All dynamic evidence and formal closure | Necessary low-level tool trust. Rebuilt from source; no candidate cache used. |
| Built-in `Bool`, `Int`, `String`, and `Map` modules/hooks, including Boolean operations, comparisons, `lengthString`, `substrString`, `findString`, lookup, and membership | All semantic rules | Ordinary low-level K trust. It does not bless calling `substrString` outside its documented valid domain or equating ASCII membership with CPython `isalpha`. |
| `runEntry` one-function binding/call rule | Main claim | Informally audited and acceptable for this exact pure module shape; no general Python call theorem exists. |
| `evalIsAlpha` → ASCII recursive predicate | Main claim and postcondition | **Illegitimate as a model of submitted Python.** Ground opposite-behavior witnesses exist. |
| Eager `evalBool2`/`evalBool3` | Main claim | **Illegitimate operational model.** Exact-input bounds-sensitivity residuals show evaluation real Python skips. |
| Totalized `evalSubscript`/`atString` | Main claim for short strings | **Illegitimate.** Ground out-of-range witness returns empty string instead of `IndexError`; this fabrication compensates for eager Boolean evaluation. |
| `standaloneLastLetter` equation | Main postcondition and five examples | Fully equational, not opaque. The bridge from this ASCII predicate to the English/canonical contract is informal plus finite differential evidence. |
| CPython/K String correspondence | Source-to-semantics bridge | Only finitely exercised. The decisive operation does not correspond because the candidate explicitly replaces Unicode `isalpha` with ASCII. |

There are no opaque symbols, external result oracles, proof-local
simplifications, priorities, totality axioms, or auxiliary lemmas. The repeated
use of `isAlphaString` in execution and the postcondition is not unconstrained
circularity because its equations define an ASCII value. The problem is more
direct: that defined value is not the submitted program's value.

### Decision

Gate A (real-program soundness) fails on the concrete `"é"` result witness and
on false Boolean/subscript operational behavior. Gate B (intent adequacy) also
fails because `solution.py` diverges from the trusted canonical over ordinary
Python strings. Gate C evidence is reproducible, but cannot repair Gates A or B.

Even an interpretation that limits the result to ASCII strings would materially
narrow the unrestricted HumanEval string contract. Under the benchmark's
explicit mapping, such a `SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`, not a
concern-level legitimate proof. Here the formal precondition is not even
narrowed; the semantics simply assigns the wrong meaning to used operations.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
