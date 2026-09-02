# Independent adversarial audit: 12-longest

## Executive decision

The candidate has a fresh, non-vacuous K reachability proof of the submitted
translated syntax under its own theory, but that theory is not a sound model of
the real Python program on the stated `List[str]` domain. The material defect is
`semantic.k:134`:

```k
rule pyLen(strVal(S)) => intVal(lengthString(S))
```

On the satisfying intended-domain input `["😀", "aa"]`, CPython's
`len` values are `1` and `2`; both the trusted canonical function and
`solution.py` return `"aa"`. Both freshly rebuilt K definitions instead return
the emoji. A direct test of the selected K primitive gives
`lengthString("😀") = 4`, not CPython's `1`. This is a concrete false-conclusion
witness for the rule and every theorem that identifies its length fold with
Python's longest-string contract. The formal claims contain no restriction
excluding non-BMP strings.

The proof therefore cannot be accepted as a partial-correctness proof of the
real generated Python program, even though all seven submitted K claims rebuild
and print `#Top`.

## 1. Input and provenance integrity

I treated every candidate log, trace, compiled object, and report as untrusted.
The provenance commands and bounded extracts are in
[`evidence/stage1_provenance.sh`](evidence/stage1_provenance.sh) and
[`evidence/stage1_provenance.log`](evidence/stage1_provenance.log).

- The rendered mode is internally consistent: `/reference/reference-semantics`
  does not exist and is not a symlink. There is no infrastructure breach.
- `/candidate/prompt.py` and `/reference/prompt.py` are byte-identical regular
  files, both SHA-256
  `aa62f2bdcae005c83ed5eede68f25a798ece3609af2bf7db30ef714aa7a33927`.
- `/candidate/py2mpy.py` and `/reference/py2mpy.py` are byte-identical regular
  files, both SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The required candidate source artifacts are present as regular files with
  the expected names: `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh`. The required metadata files and
  structured JSONL generation trace are also present as regular files. No
  required artifact is missing, changed, mistyped, or symlinked. There are no
  extra helper K source files to audit.
- Candidate extras are `verification-kompiled/` and `__pycache__/`. They are
  generated build/cache artifacts, not source integrity failures. I did not
  copy or use them.
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  the structured trace claim that generation completed and a clean combined
  proof printed four `#Top` lines. Those statements were not used as proof
  evidence. The trace also records earlier stuck claims and an opaque
  `stringAt` warning, reinforcing why reconstruction was necessary.

All source execution occurred in `/tmp/audit-work/12-longest-audit`. Reviewer
artifacts and bounded logs are under `/audit-output/evidence`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the intended domain is a
finite Python `List[str]`. The result is:

- `None` when the list is empty;
- otherwise, the earliest list element whose CPython `len` is maximal.

The type `str` includes arbitrary Python Unicode strings; neither the prompt nor
the formal preconditions restricts inputs to ASCII or the BMP.

### Source inspection

`solution.py` tests the empty list, initializes `result` with element zero,
iterates in list order, replaces `result` only on a strict length increase, and
returns it. Looping over the first element again is harmless because its length
equals the current best. This is the same algorithmic result as
`/reference/canonical.py`.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
solution_mpy_cmp_exit=0
SHA-256 both files:
17a16c7a8e00f962ce09491dd097b415eb98b18d7e92302eedd9dc792bbb0b16
```

The exact command and output are in
[`evidence/stage2_fidelity.sh`](evidence/stage2_fidelity.sh) and
[`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports the trusted canonical function and the scratch copy of the candidate
function. It tests:

- 13 directed cases: prompt examples, empty, singleton, strict-comparison
  boundaries, early and late ties, empty strings, control characters, and
  Unicode;
- all 7,381 lists of lengths zero through four over a fixed nine-string pool;
- 2,000 deterministic generated lists of lengths zero through twelve, with
  string lengths zero through sixteen.

Result: 9,394 cases, zero mismatches, exit zero. Thus the Python implementation
matches the canonical function on substantial finite evidence. This evidence
does not prove universal equivalence and does not repair the K semantics.

## 3. Clean proof reconstruction

K version `v7.1.293` was available. From source only, I built:

```text
kompile semantic.k --backend llvm --enable-search \
  --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-search-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

Both builds succeeded. The compiler emitted deprecation and unused-variable
warnings, not build errors. The first concrete harness attempt used
`krun --pattern` with an LLVM definition lacking `--enable-search`; that
reviewer-harness error is retained in
[`evidence/stage3_rebuild_and_execute.log`](evidence/stage3_rebuild_and_execute.log)
and was corrected with a separate search-enabled rebuild. It is not part of the
candidate verdict.

The corrected concrete run matched both Python functions on empty, singleton,
empty-string, ASCII growth, and tie cases, then deliberately stopped with an
exit-one comparison result at the Unicode boundary. The exact build, commands,
and first divergence are in
[`evidence/stage3_rebuild_and_execute.sh`](evidence/stage3_rebuild_and_execute.sh)
and
[`evidence/stage3_rebuild_and_execute_retry.log`](evidence/stage3_rebuild_and_execute_retry.log).

### Positive claims

Every submitted positive claim was selected independently. Because
`longest-nonempty` uses `longest-loop` as a circularity, its command selected
both labels after `longest-loop` had already been proved alone.

| Target | Selected labels | Result |
|---|---|---|
| `longest-loop` | `SPEC.longest-loop` | `#Top`, exit 0 |
| `longest-empty` | `SPEC.longest-empty` | `#Top`, exit 0 |
| `longest-nonempty` | `SPEC.longest-loop,SPEC.longest-nonempty` | `#Top`, exit 0 |
| `concrete-empty` | `SPEC.concrete-empty` | `#Top`, exit 0 |
| `concrete-first-tie` | `SPEC.concrete-first-tie` | `#Top`, exit 0 |
| `concrete-increasing` | `SPEC.concrete-increasing` | `#Top`, exit 0 |
| `concrete-late-tie` | `SPEC.concrete-late-tie` | `#Top`, exit 0 |

Commands and combined output are in
[`evidence/stage3_prove_claims.sh`](evidence/stage3_prove_claims.sh) and
[`evidence/stage3_prove_claims.log`](evidence/stage3_prove_claims.log).
Each target also has a separate `evidence/proof-*.log`.

This establishes closure under the candidate theory. It does not validate that
the theory is Python semantics.

## 4. Adequacy and real-program pinning

### Claim meanings

| Claim | Plain-language precondition | Plain-language postcondition |
|---|---|---|
| `longest-loop` | At a loop head, `N >= 0`; `result` is `BEST`; the symbolic sequence has identifier `ID`, current index `I`, and `N` remaining elements. | Execute the real loop body, the following return, and `functionEnd`; output exactly `firstInSeq(BEST,ID,I,N)`. |
| `longest-empty` | Fresh entry state; arguments are `seqVal(ID,0,0)`. | Terminate the modeled function and output exactly `noneVal`. |
| `longest-nonempty` | Fresh entry state; arguments are `seqVal(ID,0,N)` and `N > 0`. | Output exactly `strVal(firstInSeq(stringAt(ID,0),ID,0,N))`. |
| `concrete-empty` | Fresh entry state; argument is the empty `listVal`. | Output exactly `noneVal`. |
| `concrete-first-tie` | Fresh entry state; argument is `["a","b","c"]`. | Output exactly `"a"`. |
| `concrete-increasing` | Fresh entry state; argument is `["a","bb","ccc"]`. | Output exactly `"ccc"`. |
| `concrete-late-tie` | Fresh entry state; argument is `["aa","b","cc"]`. | Output exactly `"aa"`. |

The output cells are fixed to exact terms; the result is not a free variable,
tautology, or one-way implication. Existential final environment/function
variables frame irrelevant final internal state.

### Program identity

The entry claims use the macro `longestProgram`, rather than naming the file.
I parsed and fully macro-expanded both the submitted `solution.mpy` and
`longestProgram` with the fresh proof definition. Their KORE files are
byte-identical (`cmp` exit zero) and share SHA-256
`9852f2fc207637091522a41a52f53a4507a745deaa97b667e7e473ed26e8f9f4`.
See [`evidence/stage4_pinning.sh`](evidence/stage4_pinning.sh),
[`evidence/stage4_pinning.log`](evidence/stage4_pinning.log), and the two
`evidence/kast-*.kore` files. Thus the macros pin the submitted translated
program, not a substituted body.

### Satisfying states and substitutions

All four ground claims have trivially satisfiable preconditions. For the two
symbolic entry claims:

- `seqVal("empty",0,0)` is a satisfying `longest-empty` state.
- `seqVal("growth",0,3)` with
  `stringAt("growth",0)="a"`,
  `stringAt("growth",1)="bb"`, and
  `stringAt("growth",2)="ccc"` satisfies `longest-nonempty`.

The independent ground interpretation in
[`evidence/ground-witness.k`](evidence/ground-witness.k) builds and runs. The
empty substitution yields `noneVal`; the nonempty claimed fold reduces to
`"ccc"`. Both trusted canonical Python and candidate Python also return
`"ccc"` for the associated list. The log is
[`evidence/stage4_pinning.log`](evidence/stage4_pinning.log).

Adequacy nevertheless fails on Unicode, because the same result-constraining
fold uses the wrong length primitive. An ASCII satisfying example cannot
validate the whole formal domain.

## 5. Rule-by-rule static soundness review

The mechanical extraction and counts are in
[`evidence/stage5_static_extract_retry.log`](evidence/stage5_static_extract_retry.log):
40 local rules in `semantic.k`, 18 in `verification.k`, and seven claims. There
are no generated helper K files beyond `verification.k`.

### Complete local syntax and attribute inventory

| File/lines | Declaration inventory |
|---|---|
| `semantic.k:5-12` | Sorts `Expr`, `Stmt`; list sorts `Exprs`, `CmpOps`, `Strings`, `Stmts`; constructors `CmpOp(String,Expr)` and `Params(Strings)`. |
| `semantic.k:14-21` | Every `Expr` constructor: `NoneVal`, `Int`, `Str`, `Name`, `Call`, `Compare`, `Subscript`, `ListExpr`. |
| `semantic.k:23-30` | Every `Stmt` constructor: `Module`, `ImportFrom`, `FuncDef`, `If`, `Assign`, `For`, `Return(Expr)`, and `Return()`. |
| `semantic.k:38-49` | Sorts `Value`, `Values`, `Output`, `Function`; value constructors `noneVal`, `intVal`, `strVal`, `boolVal`, `listVal`; output `noOutput`; function constructors `noFunction`, `function`. |
| `semantic.k:50-57` | Configuration `<mpy>` with exactly `<k>`, `<args>`, `<env>`, `<function>`, and `<out>` cells. |
| `semantic.k:59-65` | Every local `KItem`: `exec`, `execStmt`, `invokeEntry`, `functionEnd`, `branch`, `forValues`, `returning`. |
| `semantic.k:67-72,142` | Functions `eval`, `lookup`, `pyLen`, `isEmpty`, `compare`, `head`, and `sizeValues`. None is declared `total`. |
| `verification.k:8,16` | Macros `longestLoopBody` and `longestProgram`. |
| `verification.k:31-32,40-41,77` | Functions `stringList`, `stringValues`, `expectedLongest`, `firstLongest`, and `firstInSeq`. |
| `verification.k:57` | `stringAt(String,Int) [function,total]`: the only local `total` declaration and the only opaque local function. It has no equations. |
| `verification.k:58` | Value constructor `seqVal(String,Int,Int)`. |

There are no `[functional]` declarations, priority rules, `[owise]` rules, or
`[concrete]` rules. The only simplification rules are
`semantic.k:129` and `semantic.k:130-132`. The two macro rules are
`verification.k:9-14` and `verification.k:17-27`.

### Every rule in `semantic.k`

| ID / lines | Rule | Judgment |
|---|---|---|
| S01 / 74 | `Module` schedules statements then entry invocation. | Sound for the submitted one-module program. |
| S02 / 76 | Empty `exec` disappears. | Sound list base case. |
| S03 / 77 | Statement head executes before the tail. | Sound source order. |
| S04 / 79 | `ImportFrom` is ignored. | Sound here: the only import is typing-only and has no runtime use. |
| S05 / 80-81 | `FuncDef` stores parameters/body. | Sound for the single submitted function; ignoring its name would be over-broad for unused multi-function programs. |
| S06 / 83-88 | Entry invocation binds the sole argument and initializes locals. | Sound for the exact one-parameter entry harness. No program computation is skipped. |
| S07 / 90-92 | Name assignment evaluates in the old environment, then updates. | Sound for both submitted assignments. |
| S08 / 94-96 | `If` evaluates its expression once and creates `branch`. | Sound for the pure used expressions. |
| S09 / 97 | True branch executes `THEN`. | Sound. |
| S10 / 98 | False branch executes `ELSE`. | Sound. |
| S11 / 100-102 | `For` evaluates its iterable once, then uses `forValues`. | Sound for list iteration. |
| S12 / 103 | Empty list iteration terminates. | Sound. |
| S13 / 104-106 | Nonempty list iteration binds the next value, executes the body, then recurs on the tail. | Sound order and state update. |
| S14 / 108-109 | Value-return evaluates the expression and creates `returning`. | Sound for used returns. |
| S15 / 110 | Bare return yields `noneVal`. | Sound but unused. |
| S16 / 112 | Return discards a pending sequential `exec`. | Sound abrupt return behavior for the modeled function. |
| S17 / 113 | Return discards pending loop iteration. | Sound abrupt return behavior; unused by this loop body. |
| S18 / 114-115 | At `functionEnd`, return writes `<out>` and consumes the call frame. | Sound for this single-frame harness. |
| S19 / 117 | Evaluate `NoneVal`. | Sound and used. |
| S20 / 118 | Evaluate integer literal. | Sound and used for zero/index zero. |
| S21 / 119 | Evaluate string literal. | Sound but unused by the submitted body. |
| S22 / 120 | Name evaluation performs lookup. | Sound. |
| S23 / 121 | `len(E)` evaluates `E`, then calls `pyLen`. | Structurally sound; its string case inherits S30. |
| S24 / 122-123 | Specialized `len(E) == 0` becomes `isEmpty(E)`. | Equivalent on the used list domain; no side-effecting expression is present. |
| S25 / 124-125 | `L > R` evaluates both pure sides and compares them. | Sound for the used `len` expressions, conditional on S30. |
| S26 / 126 | Subscript zero becomes `head`. | Sound because the earlier branch establishes nonemptiness. |
| S27 / 128 | Lookup a present map binding. | Sound for K maps. |
| S28 / 129 | Simplify lookup after same-key update to the new value. | True map equation over its full domain. |
| S29 / 130-132 | Simplify lookup past a different-key update. | True under the explicit key-inequality guard. |
| S30 / 134 | Python string length becomes K `lengthString`. | **Materially unsound as Python semantics.** Concrete witness below. |
| S31 / 135 | List length becomes recursive `sizeValues`. | Sound for finite modeled lists. |
| S32 / 137 | Empty list is empty. | Sound. |
| S33 / 138 | Nonempty list is not empty. | Sound. |
| S34 / 139 | Empty K string is empty. | Sound but unused by the submitted emptiness check. |
| S35 / 140 | Nonempty K string is not empty. | Sound under its guard; unused. |
| S36 / 143 | Empty value sequence has size zero. | Sound. |
| S37 / 144 | Cons sequence size is one plus tail size. | Sound and descending. |
| S38 / 146 | Integer equality returns the K integer equality Boolean. | Sound. |
| S39 / 147 | Integer greater-than returns the K integer-order Boolean. | Sound. |
| S40 / 149 | Head of a nonempty list is its first value. | Sound. |

### Every rule in `verification.k`

| ID / lines | Rule | Judgment |
|---|---|---|
| V01 / 9-14 | Expand `longestLoopBody`. | Exact submitted loop body. |
| V02 / 17-27 | Expand `longestProgram`. | Exact submitted `solution.mpy`; machine-checked by expanded KORE comparison. |
| V03 / 33 | `stringList` wraps `stringValues`. | Sound definitional conversion; unused by all claims. |
| V04 / 34 | Empty `Strings` converts to empty `Values`. | Sound; unused. |
| V05 / 35-36 | String cons converts to `strVal` cons. | Sound and descending; unused. |
| V06 / 43 | Empty expected list gives `noneVal`. | Sound relative to the candidate's metric; unused. |
| V07 / 44-45 | Nonempty expected list invokes `firstLongest`. | Sound definitional rule; unused. |
| V08 / 47 | Empty suffix keeps `BEST`. | Sound fold base; unused. |
| V09 / 48-50 | Strictly longer next string becomes best. | Sound K-metric fold branch; inherits the Python mismatch from S30. Unused. |
| V10 / 51-53 | Shorter/equal next string keeps first best. | Complementary, non-overlapping K-metric branch; inherits S30. Unused. |
| V11 / 60-61 | Zero-length `seqVal` is empty. | Sound under the stated abstract-sequence interpretation. |
| V12 / 62-63 | Positive-length `seqVal` is nonempty. | Sound; guard disjoint from V11. |
| V13 / 64-65 | Positive sequence head is `stringAt(ID,I)`. | Sound only under the named abstract-sequence interpretation. |
| V14 / 67-68 | Zero-length abstract iteration terminates. | Sound under that interpretation. |
| V15 / 69-74 | Positive abstract iteration binds `stringAt(ID,I)`, executes the real body, increments `I`, and decrements `N`. | State/control footprint matches list iteration; guards and recurring configuration match the loop claim. |
| V16 / 78-79 | Zero remaining elements return `BEST`. | Sound fold base. |
| V17 / 80-83 | A strictly longer abstract element becomes best. | Sound and descending relative to K `lengthString`; depends on S30 for Python intent. |
| V18 / 84-87 | A shorter/equal abstract element leaves best unchanged. | Complementary and descending relative to K `lengthString`; depends on S30. |

The guarded `firstLongest` and `firstInSeq` branches are pairwise disjoint and
exhaustive for their used nonnegative domains. Negative `N` is deliberately
uncovered, and the claims exclude it. `stringValues` is structurally complete.
The opaque `stringAt` has no overlapping equations because it has no equations
at all.

### Used-construct coverage

Every syntax construct in `solution.mpy` has a declaration and applicable
behavior:

| Submitted construct | Declaration/rules |
|---|---|
| `Module`, statement sequencing | `semantic.k:23`, S01-S03 |
| `ImportFrom` | `semantic.k:24`, S04 |
| `FuncDef`, `Params` | `semantic.k:10,25`, S05-S06 |
| `If` | `semantic.k:26`, S08-S10 |
| `Assign(Name,...)` | `semantic.k:27`, S07 |
| `For(Name,Name,...)` | `semantic.k:28`, S11-S13 |
| `Return(Expr)` | `semantic.k:29`, S14, S16-S18 |
| `NoneVal`, `Int`, `Name` | `semantic.k:14-17`, S19-S20, S22 |
| `Call(Name("len"),...)` | `semantic.k:18`, S23, S30-S31 |
| `Compare`, `CmpOp("==",...)`, `CmpOp(">",...)` | `semantic.k:7,19`, S24-S25, S38-S39 |
| `Subscript(...,Int(0))` | `semantic.k:20`, S26, S40 |

`Str`, `ListExpr`, bare `Return`, string truthiness, and general language
features are unused, so incomplete general Python coverage is not a defect in
this generated-semantics mode.

The configuration has all required state: current computation, injected
argument, local environment, one function body, and returned output. The
program has no heap mutation, allocation, I/O, exceptions on satisfying typed
inputs, nested calls, or observable identity behavior requiring more cells.
Evaluation-order shortcuts occur only over the submitted pure expressions.

### Required false-conclusion witness

[`evidence/stage5_length_witness_retry.log`](evidence/stage5_length_witness_retry.log)
records a direct execution of the selected primitive:

```text
lengthString("aa") -> 2
lengthString("é")  -> 1
lengthString("😀") -> 4
```

CPython gives `len("😀") == 1`. The full program witness is independently
recorded in
[`evidence/unicode_semantics_witness.py`](evidence/unicode_semantics_witness.py)
and
[`evidence/unicode_semantics_witness_both_backends.log`](evidence/unicode_semantics_witness_both_backends.log):

```text
input = ["😀", "aa"]
canonical Python = "aa"
candidate Python = "aa"
fresh LLVM K definition: expected "aa" -> #Bottom; emoji -> #Top
fresh Haskell proof definition: expected "aa" -> #Bottom; emoji -> #Top
```

The second witness `["😀😀", "abc"]` likewise returns `"abc"` in both Python
implementations but the emoji string in both K definitions. These are not
testing gaps or parser failures; the commands exit zero and discriminate the
two exact output patterns. They show a false task-level conclusion enabled by
S30. Restricting inputs after the fact to exclude these strings would silently
strengthen the prompt and the formal precondition.

No other inventoried rule is labeled unsound. The narrower evidence limitation
for V11-V15 is that `seqVal` is a proof-only representation with no
machine-checked equivalence theorem to `listVal`; its rules are coherent under
the explicit finite-sequence interpretation, and `stringAt` is an external
input element parameter rather than an oracle for the answer. That would be a
documented adequacy concern by itself, not a witnessed false equation. The
Unicode witness is independently decisive.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`. I created
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k), changing the concrete
growth result from the true `"ccc"` to the false `"bb"` while leaving a
trivially satisfiable entry state.

The dry run parsed and built the mutation with exit zero. The actual proof
exited one with `WarnStuckClaimState`; its residual is a fully terminated
configuration containing:

```text
<out> strVal("ccc") </out>
```

Thus the failure is the expected unmet result obligation, not a parser error,
missing import, timeout, unreachable mutation, or unrelated crash. Exact
commands and bounded first/last output are in
[`evidence/stage6_nonvacuity.sh`](evidence/stage6_nonvacuity.sh) and
[`evidence/stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log).

The proof is therefore non-vacuous and result-sensitive. This does not cure the
wrong string-length semantics.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the candidate K definition and K built-ins, the reconstructed
proof establishes partial correctness of the exact submitted translated
control flow for:

- the loop summary over nonnegative `seqVal` lengths;
- empty symbolic sequences returning `noneVal`;
- positive symbolic sequences returning `firstInSeq` under K's
  `lengthString` ordering;
- four specific ASCII `listVal` examples.

It does not formally establish that the result is earliest-maximal by CPython
Unicode length, nor a universal theorem over ordinary `listVal` inputs.
`expectedLongest`/`firstLongest`, despite their comment as an independent
contract model, are not referenced by any claim and also use the same
`lengthString` metric.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K compiler, Haskell prover, LLVM executor v7.1.293 | All builds, executions, and reachability closure. | Ordinary toolchain trust boundary. Fresh cross-backend results agree. |
| Imported K `INT`, `BOOL`, and `MAP` operations | Integer guards/comparisons and environment updates in all claims. | Acceptable low-level primitives for the used operations. |
| Imported K `STRING.lengthString` | Every string comparison, `firstInSeq`, symbolic entry theorem, and task interpretation. | **Illegitimate as the Python `len(str)` bridge on the stated domain**, by the concrete witnesses above. |
| `stringAt(ID,I) [function,total]` | Supplies symbolic input elements; affects branches and returned string. | Opaque but interpretation-parametric external input parameter, not itself an answer oracle. Its lack of evaluators is explicit. |
| `seqVal` plus V11-V15 | Replaces concrete list representation for the universal proof and feeds `stringAt` to the real loop body. | Coherent finite-sequence model for `N >= 0`, but its relation to ordinary `listVal` is informal rather than machine-checked; documented concern. |
| `firstInSeq` V16-V18 | Exact symbolic postcondition and loop invariant. | Truthful fold under K's metric; not an independent Python contract and inherits the fatal metric mismatch. |
| Macro pinning | Connects claim term to submitted `solution.mpy`. | Acceptable: expanded KORE is byte-identical. |
| Trusted translator | Connects `solution.py` syntax to `solution.mpy`. | Acceptable: trusted translator used, byte identity confirmed. |
| Canonical/candidate differential testing | Supports Python implementation-to-intent bridge on 9,394 finite cases. | Finite empirical evidence only; it does not substitute for the K proof. |
| Concrete K tests | Supports selected semantic paths. | Finite evidence; here it actively falsifies the critical Unicode bridge. |

Candidate `#Top` output, logs, trace, and compiled definitions are excluded from
the trust ledger because none was used.

### Gate and verdict rationale

- Real-program soundness gate: **FAIL**. S30 permits the demonstrated false
  Python conclusion on satisfying typed inputs.
- Intent adequacy gate: **FAIL**. The stated domain includes those Unicode
  strings, and the postcondition uses K's incompatible metric.
- Evidence/auditability gate: **PASS as evidence quality**. The sources,
  commands, clean builds, per-claim results, ground witnesses, static
  inventory, cross-backend counterexamples, and non-vacuity result are
  reproducible. Good evidence exposes rather than repairs the soundness
  failure.

The earliest material failure is real-program soundness. Under the required
decision boundary, a fresh `#Top` for a materially unsound generated semantics
is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
