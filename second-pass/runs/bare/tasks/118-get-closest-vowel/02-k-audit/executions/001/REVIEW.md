# Independent adversarial audit: 118-get-closest-vowel

This audit used only source copied from `/candidate` into
`/tmp/audit-work`; no candidate-provided kompiled definition or cache was
reused. The live toolchain was K v7.1.293, Python 3.10.12, and Java 17
([tool versions](evidence/00-tool-versions.log)).

The positive K proof does reconstruct and the claims are non-vacuous, but the
candidate is not a legitimate proof of the real generated program. A
task-specific operational rule decides membership from the identifier
`"vowels"` without reading that identifier's binding. A one-line body mutation
from `vowels = "aeiouAEIOU"` to `vowels = ""` remains freshly provable as the
original theorem and returns `"A"` in K for `"bAb"`, while real Python returns
`""`. This is a concrete binding-, body-, control-, and result-fidelity failure.
There is also a real-input-domain discrepancy at long strings: the recursive
Python candidate raises `RecursionError`, while the canonical loop and the
unbounded K machine return normally.

## 1. Input and provenance integrity

### Condition-aware semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. The path
`/reference/reference-semantics` does not exist and is not a symlink, as
required. No hidden or inferred reference semantics was used. The candidate's
own `semantic.k` was therefore audited on its merits.

### Trusted-file comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`0eec1170b109fb6d89c6ef7ccf3407439aa820f170e9377d84d5fef4a8da296d`).
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
The recursive type/symlink inventory found no symlinked candidate entry.
See [integrity evidence](evidence/01-integrity.log) and
[source hashes](evidence/01-source-hashes.log).

All generation-required source artifacts were present as regular files:

- `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`;
- the generated helper `program.k`;
- `prove.sh`.

The candidate also contains `check_program_module.py`, generation
metadata/logs, a JSONL trace, and `semantic-kompiled/`. These are extra
non-source evidence, not trusted inputs. The compiled directory was deliberately
not copied to either fresh build.

`run-input.json`, `metrics.json`, `codex-last.txt`, the 50,543-line
`codex-output.log`, and the 459-record structured trace were read only as
untrusted claims. They claim a successful generation and one final `#Top`;
none was used as proof evidence. Their bounded summaries are in
[metadata/log signals](evidence/01-untrusted-metadata.log) and
[trace summary](evidence/01-trace-summary-python.log). An initial optional
`jq` summary attempt failed because `jq` is absent
([preserved failed attempt](evidence/01-trace-summary.log)); the Python JSONL
summary replaced it and exited 0. This tooling detail is not a candidate
failure.

Stage 1 result: no provenance-integrity failure and no infrastructure-mode
breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a string containing English letters, inspect eligible interior positions
from right to left. Return the first character that is one of
`aeiouAEIOU` and whose immediate left and right neighbors are both
non-vowels. The first and last characters can never qualify. Return `""` when
no eligible character exists. The trusted canonical implementation performs
exactly that right-to-left loop.

The candidate uses a different recursive algorithm. It checks the rightmost
eligible three-character window and either returns its middle character or
recurses on the string with its last character removed. Mathematically this is
equivalent while normal recursion remains available.

### Translation and proof-program identity

The exact command

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/candidate-src/solution.fresh.mpy
```

exited 0. The fresh output is byte-identical to the submitted
`solution.mpy` ([translation](evidence/02-translate.log),
[byte comparison](evidence/02-mpy-byte-identity.log)).

An independent reviewer checker reconstructed the complete
`SOLUTION-PROGRAM` module from that fresh MPY term, including explicit empty
`Stmts` list units. It was byte-identical to `program.k`
([checker](evidence/check_program_pinning.py),
[result](evidence/02-program-pinning.log)). Thus the K claims pin the submitted
constructor program, not a substituted AST.

### Independent differential evidence

The independent script imports `/reference/canonical.py` and the scratch
candidate under distinct module names. It covered:

- all four documented examples;
- explicit empty, length-1, length-2, immediate-success, and every failed-window
  branch shape;
- all 21,845 strings of lengths 0 through 7 over `aAbB`, representing
  lower/uppercase vowel/consonant categories;
- 2,000 deterministic random ASCII-letter strings of lengths 0 through 32.

There were zero mismatches across 23,766 unique inputs (corpus SHA-256
`a41dbb8171b0a166615487bfac2f0bfd3a14f71800f33811b9f0f08b138c0c90`).
See [script](evidence/differential_test.py),
[serialized inputs](evidence/02-differential-inputs.json), and
[run](evidence/02-differential.log).

The prompt, however, specifies no maximum word length. A separate valid-domain
boundary probe found that all-consonant strings of lengths 1000, 1100, and
1500 return `""` from the canonical loop but raise `RecursionError` from the
candidate under the audited Python 3.10.12 runtime. A length-1500 input ending
in immediate `bAb` still returns `"A"`, confirming that recursion depth—not
string parsing—is the distinction. See
[long-input script](evidence/long_input_boundary.py) and
[results](evidence/02-long-input-boundary.log).

Stage 2 result: exact source/MPY/program pinning passes and the algorithms agree
on broad bounded data, but the generated Python implementation has a material
valid-input exception divergence because it replaced the canonical loop with
unbounded recursion.

## 3. Clean proof reconstruction

### Fresh definitions

Only `semantic.k`, `verification.k`, `program.k`, `spec.k`, and the freshly
translated MPY file were copied into two empty source build directories.

- LLVM concrete build:
  `kompile semantic.k --backend llvm --main-module MPY --syntax-module
  MPY-SYNTAX --output-definition concrete-kompiled --warnings none`
  exited 0
  ([log](evidence/03-kompile-concrete.log)).
- Haskell proof build:
  `kompile semantic.k --backend haskell --main-module MPY --syntax-module
  MPY-SYNTAX --output-definition proof-kompiled --warnings none`
  exited 0
  ([log](evidence/03-kompile-proof.log)).

### Concrete generated-semantics execution

A normal smoke run of `"yogurt"` ended with
`pyStr(snoc(.Chars,vow(v_u)))`, empty environment, and empty stack
([full bounded log](evidence/03-krun-yogurt-smoke.log)).

The fresh LLVM definition was then run on 22 normal and boundary strings,
including all prompt examples and all major conditional/recursive shapes.
Every `krun` exited 0; K, canonical Python, and candidate Python agreed on every
one ([script](evidence/k_semantics_differential.py),
[inputs](evidence/03-k-semantics-inputs.json),
[results](evidence/03-k-semantics-differential.log)).

On the valid input `"b" * 1000`, however, the same fresh K definition returns
`""` while candidate Python raises `RecursionError`
([script](evidence/k_long_boundary.py),
[result](evidence/03-k-long-boundary.log)). The generated semantics models an
unbounded call stack and no Python recursion exception.

### Positive claims

The original unmodified proof command

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC --warnings none
```

exited 0 and printed exactly `#Top`
([log](evidence/03-kprove-all.log)).

For claim-level auditability, a scratch spec added labels and changed nothing
else ([labeled spec](evidence/03-spec-labeled.k)). Its aggregate proof also
exited 0 with `#Top`
([log](evidence/03-kprove-labeled-all-serial.log)). Each of the 13 labeled
claims was then run serially as the only untrusted target while the other 12
aggregate-proven mutual circularities were marked trusted for that diagnostic
run. All 13 commands exited 0 and printed `#Top`; the corresponding logs are
`evidence/03-kprove-case-01-serial.log` through
`evidence/03-kprove-case-13-serial.log`. The unmodified aggregate proof—not
these diagnostic trust flags—is the evidence that all 13 close together.

An earlier attempt to launch 14 Haskell backends concurrently was discarded:
some jobs were OOM-killed with code 137, and two recursive targets selected
alone lacked their mutual circularities. Those failed diagnostic logs are
preserved without being treated as candidate evidence
(`evidence/03-kprove-labeled-all.log` and the non-`serial` per-case logs).
Serial reruns removed the resource uncertainty.

Stage 3 result: fresh concrete/proof builds and the complete positive target
proof mechanically pass. This establishes closure only under the submitted K
theory; Stage 5 shows that theory is materially unsound.

## 4. Adequacy and real-program pinning

There are no explicit `requires` clauses. Each claim's typed constructor pattern
is its precondition. Every claim begins with the exact invocation

```text
invoke("get_closest_vowel", pyStr(...)) ~> KREST
```

under `<program> solutionProgram </program>`, with arbitrary caller
continuation, environment, and stack. Every destination is a concrete
`callResult(...) ~> KREST`; the environment and stack are preserved. No
right-only existential, free result variable, implication, or tautological
postcondition appears.

The 13 cases have these plain-language pre/postconditions:

| Case | Input-shape precondition | Required returned value |
|---:|---|---|
| 1 | empty word | `""` |
| 2 | length 1 | `""` |
| 3 | length 2 | `""` |
| 4 | length at least 3, suffix consonant-vowel-consonant | that suffix vowel |
| 5 | length 3, middle character consonant | `""` |
| 6 | length at least 4, current middle consonant, predecessor suffix consonant-consonant | `closestSpec` of input without its final character |
| 7 | length at least 4, current middle consonant, predecessor suffix vowel-vowel-consonant | `closestSpec` of input without its final character |
| 8 | length at least 4, current middle consonant, predecessor suffix consonant-vowel-consonant | `closestSpec` of input without its final character |
| 9 | length 3, left and middle characters vowels | `""` |
| 10 | length at least 4, left/middle vowels and their predecessor a vowel | `closestSpec` of input without its final character |
| 11 | length at least 4, left/middle vowels and their predecessor a consonant | `closestSpec` of input without its final character |
| 12 | length 3, suffix consonant-vowel-vowel | `""` |
| 13 | length at least 4, suffix consonant-vowel-vowel | `closestSpec` of input without its final character |

Cases 1–3 cover short words. For words of length at least 3, cases 4–13
partition the last three character categories and the predecessor categories
needed after recursion. The recursive right-hand sides remove one character;
`closestSpec` is deterministic and structurally decreasing. Collectively the
claims constrain the result for every finite tagged `Chars` value.

One satisfiable common caller state is
`KREST=.K`, `ENV=.Map`, `STACK=.Frames`,
`program=solutionProgram`. Concrete witnesses for cases 1–13 are respectively
`""`, `"b"`, `"ba"`, `"bAb"`, `"bbb"`, `"bbbb"`, `"aabb"`,
`"babb"`, `"aab"`, `"aaab"`, `"baab"`, `"baa"`, and `"bbaa"`.
Substitution into each postcondition agreed with both Python implementations
([witness script](evidence/claim_witnesses.py),
[results](evidence/04-claim-witnesses.log)).

The calls execute `functionBody(solutionProgram,...)`; `solutionProgram` was
independently pinned byte-for-byte to the trusted translation in Stage 2.
Recursive calls go through the same `invoke` machine state. The claims stop at
the caller-visible `callResult`, so they preserve rather than discard arbitrary
caller continuations.

Two scope qualifications remain:

1. Claims begin after conversion to tagged `pyStr(Chars)`, not at
   `start(word(S))`. The `start`, `normalize`, `litChars`, and `litChar` rules
   supply an executable bridge, and the claims are stronger over all tagged
   `Chars`, but no separately named universal raw-String connection theorem is
   proved.
2. `Chars` is a tagged abstraction. Terms such as `con("a")` are syntactically
   constructible even though `litChar("a")` always produces `vow(v_a)`.
   Actual English inputs are canonicalized correctly; noncanonical tagged terms
   have no direct Python-string interpretation.

Stage 4 result: the formal claims are satisfiable, exhaustive,
result-constraining, and pinned to the submitted AST. Adequacy nevertheless
depends on the semantics being faithful, which fails in Stage 5.

## 5. Rule-by-rule static soundness review

The mechanical inventory is preserved in
[rule inventory](evidence/05-rule-inventory.log). Locally there are 38
`syntax` declaration lines and 85 rules in `semantic.k`, seven rules in
`verification.k`, one generated-program rule, and 13 claims.

### Syntax, attributes, and configuration inventory

`MPY-SYNTAX` declares every local constructor below:

- AST: `Module`; list-valued `Stmts`; `FuncDef`, `Assign`, `If`, `Return`;
  `Params` and `ParamNames`; `Name`, `Str`, `Int`, `Call`, `Compare`, `CmpOp`,
  `UnaryOp`, `Subscript`; `Exprs`, `CmpOps`, `Index`, `Slice`, `Bound`, and
  `NoBound`.
- Runtime categories: ten `Vowel` constants; `vow` and `con`; `.Chars` and
  `snoc`; `z` and `s`; `pyStr`, `pyNat`, `pyNeg`, `pyBool`, `vowelSet`, and
  input wrapper `word`.
- Machine categories: `start`, `invoke`, `execMachine`, `doStmt`, `returning`,
  `branch`, `lenBranch`, `memberBranch`, `callResult`, `tailReturn`, `unwrap`;
  `frame`, `.Frames`, `push`; and `normal`/`returned`.

The four-cell configuration is `<k>`, immutable `<program>`, current `<env>`,
and call `<stack>`. No heap, allocation, I/O, exception, or recursion-limit
cell exists. That omission is harmless for the target's ordinary bounded
operations, but not for the long-input CPython behavior documented above.

The 24 semantic functions are:
`normalize`, `call`, `functionBody`, `functionEnv`, `returnValue`, `exec`,
`execRest`, `execStmt`, `choose`, `eval`, `evalCompare`, `evalUnary`,
`evalIndex`, `evalSliceLast`, `asBool`, `lookupVal`, `litChars`, `litChar`,
`intNat`, `lenChars`, `asChars`, `natLt`, `fromEnd`, and `isVowelChar`.
`verification.k` adds `closestSpec`; `program.k` adds `solutionProgram`.

There are no `[total]`, `[functional]`, `[simplification]`, or explicit numeric
priority declarations, and no opaque/uninterpreted result symbol. Sixteen AST
productions use `[symbol]`. The only local priorities are `[owise]` on the
fallbacks for `normalize`, generic machine `If`, generic `returning`, and
`litChar`. All functions deliberately remain partial outside the submitted
program's construct/value shapes; unsupported cases become stuck rather than
silently acquiring an oracle, except for the membership bridge identified
below.

### Mapping from the submitted MPY program

| Submitted construct | Declaration | Behavior used |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | lines 10–17 | `functionBody`, `functionEnv`, `execMachine` |
| assignment, `Name`, string literals | lines 13, 19–20 | assignment update, `lookupVal`, `eval(Str)` |
| `If`, `Compare`, `CmpOp` | lines 14, 23–24 | specialized length/membership branches or generic `evalCompare` |
| one-argument `Call`, `Int` | lines 21–22 | built-in `len` or recursive `call` |
| `Return` | line 15 | abrupt local return through `returning` |
| `Subscript`, `UnaryOp` | lines 25–26, 29 | negative index through `pyNeg`/`fromEnd` |
| `Slice(NoBound,-1,NoBound)` | lines 30–31 | remove-last-character rule |

No used constructor lacks a declaration or a terminating rule path on the
ordinary valid inputs exercised in Stage 3.

### Exhaustive semantic-rule disposition

The following table accounts for every one of the 85 `semantic.k` rules.

| Lines | Rules | Static decision |
|---|---|---|
| 81–82 | two `normalize` equations | Sound: `word(S)` canonicalizes; `[owise]` leaves other `Val`s unchanged. |
| 84 | `start` | Sound for this single-entry task; selects the required function and preserves the remaining computation. |
| 88–97 | invocation, frame push/pop, two `callResult` continuations | Sound on the one-function module. The frame contains the complete caller continuation and environment; pop restores both. |
| 99–100 | empty/nonempty statement scheduler | Sound left-to-right sequencing. |
| 101–103 | assignment | Sound for the pure target expressions; exactly one map binding is updated after evaluation. |
| 104–112 | specialized `len(word) < 3` and four length branches | Sound on the matched target syntax. The four structural shapes are disjoint/exhaustive and agree with `natLt(lenChars(...),3)`. |
| 113–117 | specialized comparison against `Name("vowels")` | **Unsound operational bridge.** It evaluates only the left operand and never looks up/evaluates the right-hand binding. Concrete false witness below. |
| 118–125 | four `memberBranch` equations | Sound for a one-character tagged string and the intended `vowelSet`: `vow`/`con` and `in`/`not in` are a disjoint exhaustive product. |
| 126–131 | generic `[owise]` `If` and two Boolean branches | Sound wherever `eval` produces `pyBool`; specialized rules preempt it. |
| 132–139 | `Return`, recursive-return call, generic returning expression | Sound control behavior: current function remainder is discarded, while the caller continuation remains in its frame. The call argument slice is evaluated before invocation. |
| 145–147 | big-step `call` | Sound for the single one-argument function, conditional on the following body/environment/exec equations. |
| 150–151 | `functionBody` | Sound exact pattern for the submitted one-function module; otherwise deliberately partial. |
| 154–155 | `functionEnv` | Sound exact one-parameter binding; otherwise partial. |
| 158 | `returnValue` | Sound for returned executions; a normal fall-through is deliberately unsupported. |
| 164–176 | two `exec`, two `execRest`, three `execStmt`, two `choose` equations | Sound standard big-step sequencing, early return, assignment, and Boolean branch behavior on the target statement subset. |
| 187–203 | `lookupVal` plus ten `eval` equations | Sound on used expression forms. `vowelSet` is a value abstraction of the exact literal preserving the only used observation (membership); constant/other-string and `len`/other-call guards are disjoint. Expression-index and slice-index patterns are sort-disjoint. |
| 205–213 | three comparison, unary minus, negative index, remove-last slice, and Boolean projection equations | Sound on used values. Negative indexing is structurally correct when in range; the program's length test guarantees indices -1 through -3 are in range. |
| 219–235 | two `litChars` and eleven `litChar` equations | Sound on English-letter inputs. The ten vowel literals and `[owise]` consonant case are disjoint; recursion shortens the string. |
| 239–245 | five `intNat` and two `lenChars` equations | Sound. The general positive rule overlaps 1, 2, and 3 but reaches the same right-hand values as the specialized equations and strictly decreases. Negative integers are unused. |
| 248 | `asChars` | Sound projection, deliberately partial for non-strings. |
| 251–253 | three `natLt` equations | Sound, disjoint structural comparison. |
| 256–257 | two `fromEnd` equations | Sound for positive in-range indices and structurally decreasing. Zero/out-of-range cases remain visibly stuck. |
| 260–261 | two `isVowelChar` equations | Sound and exhaustive for the tagged `Char` sort. |

Evaluation order, state, and control are otherwise coherent: expressions in the
target are pure; statements execute left to right; assignment is the only
state update; calls push and pop exact frames; return discards only the current
function remainder; and no target operation allocates or produces I/O.

`verification.k` contains one function and seven equations:

- lines 14–16: lengths 0, 1, and 2 return empty;
- lines 17–18: a final consonant-vowel-consonant returns that vowel;
- lines 19–20: a consonant middle fails and removes the last character;
- lines 21–22: vowel left and vowel middle fail and remove the last character;
- lines 23–24: consonant-vowel-vowel fails and removes the last character.

Those equations are pairwise disjoint, exhaustive over finite `Chars`, and
structurally decreasing. They are a truthful definitional summary, not an
operational replacement. `program.k`'s sole `solutionProgram` equation is the
exact pinned AST established in Stage 2.

### Concrete false-conclusion witness for the unsound rule

The operational bridge at semantic lines 113–117 matches the expression text
`Name("vowels")` but has no cell pattern or guard requiring
`ENV["vowels"] = vowelSet`. It rewrites directly to
`memberBranch(OP, eval(L,...),...)`; the actual right operand is absent from
both the rewrite and the resulting computation. It therefore changes branch,
control, and final result when the binding is anything other than the encoded
constant.

The reviewer made exactly one source mutation:

```text
-    vowels = "aeiouAEIOU"
+    vowels = ""
```

The mutated Python, trusted-translator output, and independently pinned
`program.k` are preserved as
[mutated source](evidence/05-body-mutation-solution.py),
[mutated MPY](evidence/05-body-mutation-solution.mpy), and
[mutated program](evidence/05-body-mutation-program.k). The exact diff is
[here](evidence/05-body-mutation-diff.log); `diff` exit 1 is its expected
“files differ” status. Trusted translation and program pinning both passed
([translation](evidence/05-body-mutation-translate.log),
[pinning](evidence/05-body-mutation-pinning.log)).

For the satisfying intended-domain input `"bAb"`:

- original Python returns `"A"`;
- mutated Python returns `""`, because no character is a member of `""`
  ([Python witness](evidence/05-body-mutation-python.log));
- the freshly built mutated K program still returns
  `pyStr(snoc(.Chars,vow(v_A)))`
  ([K witness](evidence/05-body-mutation-krun.log));
- the unchanged 13-claim theorem still prints `#Top` and exits 0
  ([proof witness](evidence/05-body-mutation-kprove.log)).

At the false transition, the machine environment contains the mutated empty
string binding, yet the bridge selects the vowel branch solely because the
left character is tagged `vow(v_A)`. This is the required concrete false
conclusion: K returns `"A"` while execution of the program body it purports to
model returns `""`. The bridge is not justified by its complete match domain,
does not preserve binding lookup, and makes the proof insensitive to a
result-bearing program statement. A guard that actually checks the binding, or
use of the already-defined generic evaluator, would be required.

This is not merely thin evidence or an unused over-broad rule. The rule
preempts the generic `If` rule via `[owise]`, lies directly on every membership
path in the positive proof, and hardcodes the task-relevant meaning of a
program variable name.

Stage 5 result: Gate A real-program soundness fails.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. The reviewer copied the original
spec into a new `SPEC-VACUITY` module and changed only case 4's
result-constraining postcondition from “return the bracketed vowel” to “return
the empty string”:

```text
- => callResult(pyStr(snoc(.Chars, vow(V)))) ~> KREST
+ => callResult(pyStr(.Chars)) ~> KREST
```

The mutation is preserved at
[06-spec-vacuity.k](evidence/06-spec-vacuity.k). Input `"bAb"` satisfies that
claim's precondition and demonstrably returns `"A"` in both original Python
implementations.

`kprove ... --dry-run` exited 0, establishing that the mutated artifact and
module build successfully
([dry run](evidence/06-vacuity-dry-run.log)). The actual proof exited 1 with
`WarnStuckClaimState`. Its residual contains
`callResult(pyStr(snoc(.Chars,vow(V))))`, which cannot unify with the mutated
empty-string destination
([proof log](evidence/06-vacuity-kprove.log)). This is the expected reachable,
unmet result obligation—not a parser error, missing import, timeout, or
unrelated crash.

Stage 6 result: non-vacuity passes. It does not repair the unsound theory used
by the positive proof.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under all rules in the submitted K definition, the 13 mutually supporting
reachability claims prove that executing the pinned `solutionProgram` from any
of their finite tagged-`Chars` invocation configurations reaches a
caller-visible `callResult` equal to the structurally defined `closestSpec`,
while restoring the caller environment/stack and preserving its continuation.
This is a result-constraining partial-correctness statement inside the submitted
abstract machine.

It does **not** independently establish that every operational rule is a sound
model of Python, that the named variable actually has the value assumed by the
membership shortcut, that raw K strings and tagged `Chars` are universally
connected by a proved theorem, that real CPython has an unbounded call stack,
or that the recursive Python implementation returns normally on all prompt
inputs.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler/prover/backends and imported `BOOL`, `INT`, `STRING`, `MAP`, and list machinery | all builds, execution, and proof | Normal low-level trust boundary; exact versions and fresh commands are recorded. |
| Trusted `/reference/py2mpy.py` transliteration | source-to-MPY link | Acceptable and byte-checked. |
| `solutionProgram` constructor equation | all claims | Acceptable; independently byte-pinned to fresh trusted translation. |
| K string `lengthString`/`substrString`, map lookup/update, unary `Nat` representation | input conversion and expression execution | Acceptable low-level primitives on English-letter inputs; exercised concretely. |
| `litChar` vowel/consonant tagging and `vowelSet` abstraction | every branch/result and `closestSpec` bridge | Equations are explicit and truthful for the only observed operation on the exact constant; finite K/Python differentials support but do not prove the universal bridge. |
| `closestSpec` | recursive claim postconditions | Acceptable explicit mathematics: exhaustive, disjoint, decreasing equations. It does not replace execution. |
| 13 reachability claims as mutual circularities | recursive closure | Machine-checked together by the aggregate `#Top`; claim-level serial diagnostics are recorded. |
| Specialized membership rule keyed only by `Name("vowels")` | every non-base branch and final result | **Illegitimate.** It is a program-derived, result-bearing operational bridge with no binding guard or connection theorem. The English-input false witness changes Python's result while K and the proof remain unchanged. |
| Unbounded K frames and absent recursion exception | long recursive executions | Material real-Python model gap. At length 1000, K/canonical return `""`; candidate Python raises `RecursionError`. |
| Differential testing | source/canonical and K/Python bridges on tested data only | Empirical support only. It cannot replace rule validity or a universal connection theorem. |
| Candidate logs, trace, `codex-last.txt`, prior `#Top`, and compiled cache | none | Untrusted claims; excluded from reconstruction. |

Validation gates:

- Gate A — real-program soundness: **FAIL**. The membership bridge is false
  over its admitted configurations and is demonstrably body-insensitive.
- Gate B — intent adequacy: **FAIL**. The prompt has no length limit, while
  real candidate Python raises on sufficiently long valid words and K does not
  model that exception.
- Gate C — trust/evidence auditability: **FAIL for the candidate report**. The
  candidate did not disclose either material boundary; its four concrete K
  examples and prior `#Top` could not validate them. This audit's replacement
  evidence is reproducible but cannot retroactively make the theory sound.

The positive reconstruction and non-vacuity result therefore show only that K
can discriminate postconditions inside the submitted theory. The false
operational rule means that theory is not a legitimate semantics of the
result-bearing program behavior, so the required decision is `FAIL /
NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
