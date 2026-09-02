# Independent adversarial review: 158-find-max

The candidate reconstructs to a real, non-vacuous K reachability proof of its
own byte-oriented model, and its claimed `solutionAST` is mechanically the same
constructor program as trusted regeneration of `solution.py`. It is not a
legitimate proof of the HumanEval program over the source string domain. The
generated semantics implements `len(set(s))` as a count of distinct UTF-8
bytes, not distinct Python Unicode characters. A valid, nonempty,
different-word input witnesses a false result:

```text
input:             ["😀", "abc"]
candidate Python:  "abc"
trusted canonical: "abc"
fresh K execution: "😀"   (the K model assigns "😀" count 4)
```

This is a material domain narrowing to ASCII/byte strings. Under the benchmark
decision boundary, that is `FAIL / NOT_LEGIT`, even though the internal K
claims close and the proof is discriminating.

## 1. Input and provenance integrity

The launcher record is readable and declares:

- problem `158-find-max`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required legacy-selected-stage1
generation records, the present `usage.json`, and all 272 JSON records in the
structured trace. Historical runtime metrics are not required for this layout.
The generation reports (`SUCCEEDED`, `KPROVE_PASSED`, and the prose final
report) were treated only as untrusted claims.

Integrity checks:

- `/audit-campaign-lock.json` is byte-hashed to the recorded
  `ad5dfcc0...1a78d745`, and its parsed object exactly equals the campaign block
  in `/audit-input.json`.
- Every launcher-recorded regular-file hash checked by
  `check_provenance.py` matches: run/task/result/invocation/metrics/usage,
  generation prompt/output/last, canonical, prompt, and translator.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The candidate tree has two real directories and nine regular files; the
  reference tree has three regular files; the generation tree has five real
  directories and nine regular files. None contains a symlink or unsupported
  node.
- An independent length-prefixed pipeline tree digest of `/candidate` is
  `3803cc77...96e9b2`, exactly matching the retained/output workspace digest in
  both `invocation.json` and `generation-result.json`. The independent trace
  tree digest is `425d086b...3bb6d`, exactly matching `usage.json`; its only
  JSONL file independently hashes to the `e4710c92...529b53` recorded by the
  invocation/result manifests.
- `/reference/reference-semantics` is absent, as required in
  `GENERATED_SEMANTICS`; `/candidate/reference-semantics` is also absent.
- Required proof artifacts `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh` are real regular files.

There is no infrastructure breach. Reproducible details and exact hashes are in
[`01-provenance.log`](evidence/01-provenance.log), with the reviewer script in
[`check_provenance.py`](evidence/check_provenance.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks for a word from a list of different strings that has
the largest number of unique characters, breaking ties by Python
lexicographic order. The trusted canonical implements:

```python
sorted(words, key=lambda x: (-len(set(x)), x))[0]
```

The normal-result domain is therefore a nonempty list of pairwise different
Python strings. The prompt does not spell out “nonempty,” but the required
result must be a member of the input and the trusted canonical indexes `[0]`.
On the separately required empty boundary, the canonical raises `IndexError`;
the candidate returns `""`. I record that divergence, but do not manufacture a
normal-return empty-list contract that the trusted canonical itself lacks.

`solution.py` is a left-to-right accumulator. It updates on a higher distinct
character count and, after the update, performs the tie comparison. The second
comparison is harmless in the higher-count branch because `word == best`.

Trusted regeneration used:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp -s /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
```

Both commands exited 0. Both terms have SHA-256
`65fdcbb262c7d5ed2d66958afb5f260004155a4467c8cc2241d68f914a49b1a8`;
see [`02-regeneration.log`](evidence/02-regeneration.log).

The independent differential test covers all three examples; empty and
singleton boundaries; greater-count and both tie directions; repeated
characters; empty strings; NUL, combining, precomposed, BMP, and non-BMP
Unicode strings; 205 exhaustive ordered lists from a small word pool; and
2,000 deterministic broader generated inputs. All 2,205 generated inputs are
nonempty and have different words. There were zero intended-domain
mismatches. The sole fixed mismatch was empty input:

```text
canonical: raise IndexError
candidate: return ""
```

The script, deterministic input construction, input digest, and results are in
[`differential_test.py`](evidence/differential_test.py) and
[`03-differential.log`](evidence/03-differential.log).

## 3. Clean proof reconstruction

Only the source files were copied to `/tmp/audit-work/clean-build`. No
candidate-compiled definition or cache was present or reused.

### Fresh builds

| Purpose | Exact command | Result |
|---|---|---|
| LLVM generated semantics | `kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | exit 0, but warns that `[total] distinctCount` is non-exhaustive |
| LLVM search semantics | same command with `--enable-search --output-definition concrete-search-kompiled` | exit 0 with the same warning |
| Haskell generated semantics | `kompile --backend haskell semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-haskell-kompiled` | exit 0 |
| Haskell proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION --output-definition proof-kompiled -I .` | exit 0 |

Logs are
[`04-build-concrete.log`](evidence/04-build-concrete.log),
[`07-build-concrete-search.log`](evidence/07-build-concrete-search.log),
[`09-build-semantic-haskell.log`](evidence/09-build-semantic-haskell.log), and
[`05-build-proof.log`](evidence/05-build-proof.log).

The LLVM warning is operationally real: with search enabled, empty input
matches, but every tested nonempty input becomes `#Bottom`. This is caused by
declaring a function total while restricting all defining equations with
`[concrete]`. The submitted workflow uses Haskell, so I also executed the
semantics under Haskell rather than treating an LLVM backend discrepancy as a
substitute for the requested audit.

Under Haskell, all ASCII examples and branch/boundary cases match candidate
Python. Actual Unicode configurations show that K `String` operations here
scan bytes: for example, `"東京"` receives count 6 and `"😀"` receives count 4.
The decisive complete-program witness is:

```text
python3 ... solution.find_max(["😀", "abc"])
# PYTHON_RESULT 'abc'

krun solution.mpy --definition semantic-haskell-kompiled \
  -cINPUT='cons("😀", cons("abc", nil))' --output pretty
# <best> "\xf0\x9f\x98\x80" </best>
# <bestCount> 4 </bestCount>
# <result> result(strVal("\xf0\x9f\x98\x80")) </result>
```

Both processes exited 0. See
[`12-unicode-counterexample.log`](evidence/12-unicode-counterexample.log).

### Positive proof targets

Every positive claim was freshly exercised:

| Target | Exact selection | Result |
|---|---|---|
| `program-initializes` | `--claims SPEC.program-initializes` | exit 0, `#Top` |
| `loop-correct` | `--claims SPEC.loop-correct` | exit 0, `#Top` |
| `find-max-correct` with its proved circularity | `--claims SPEC.loop-correct,SPEC.find-max-correct` | exit 0, `#Top` |
| complete spec | no filtering | exit 0, `#Top` |

The logs are
[`13-kprove-program-initializes.log`](evidence/13-kprove-program-initializes.log),
[`14-kprove-loop-correct.log`](evidence/14-kprove-loop-correct.log),
[`18-kprove-end-with-loop-dependency.log`](evidence/18-kprove-end-with-loop-dependency.log),
and [`17-kprove-all-claims.log`](evidence/17-kprove-all-claims.log).
Selecting only `find-max-correct` also filters out the loop circularity and
unrolls; that diagnostic was stopped and is not interpreted as failure of the
target that closes with its dependency.

Thus clean proof reconstruction succeeds under the supplied theory. `#Top`
does not cure the false Python semantics identified above.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `loop-correct` has no `requires` clause. For any finite `REST`, any starting
   strings/integers in the five local cells, and `noResult`, it executes the
   exact loop body followed by `return best`. It requires the final result to
   be the word component of `maxCandidate(REST,
   candidate(BEST,BESTCOUNT))`. Final local-cell values are existential.
2. `program-initializes` has no `requires` clause. For any `WORDS`, with the
   configured initial local cells, executing `solutionAST` reaches the exact
   loop-and-return continuation with `best = ""` and `bestCount = -1`.
3. `find-max-correct` has no `requires` clause. For every finite constructor
   `Words` value in the initial configuration, executing `solutionAST` consumes
   `<k>` and requires the observable result to be exactly
   `result(strVal(findMaxSpec(WORDS)))`. This is an equality-shaped result
   constraint, not a free result, tautology, or one-way implication.

All preconditions are satisfiable. Examples are:

- loop claim: `REST = nil`, `BEST = ""`, `BESTCOUNT = -1`,
  `_OLDWORD = ""`, `_OLDCOUNT = 0`;
- initialization claim: `WORDS = nil` and the displayed initial cells;
- end claim: `WORDS = cons("ba", cons("ab", nil))` and the displayed initial
  cells.

For the last state, candidate Python and canonical Python both return `"ab"`;
fresh K execution also matches result `"ab"`. For
`cons("😀", cons("abc", nil))`, both Python implementations return `"abc"`,
but the claimed K result reduces to the byte-model choice `"😀"`.

### Mechanical source pinning

The trusted translator establishes source-to-`solution.mpy` identity. To check
`solutionAST`, I ran the parsed `solution.mpy` and a one-token program
`solutionAST` to depth 1 under the fresh proof definition and compared the
complete KORE configurations. `cmp` exited 0; both files hash to
`9ded476e4bc3d6f2df88b66e1bebe345ec2d9c5c66a462fbad011511dab8b072`.
This demonstrates the same function binding and constructor body, including
empty statement lists; see
[`22-program-pinning-mechanical-compare.log`](evidence/22-program-pinning-mechanical-compare.log).

The module-entry rule is a minimal function harness: it matches exactly
`find_max` with parameter `words`, supplies the argument through the
`<words>` cell, and executes the parsed body. It omits general Python function
objects/call stacks, but no material binding, argument side effect, or control
effect exists in this submitted function.

A body-sensitivity mutation changed the count assignment inside
`solutionLoopBody` from the submitted nested `len(set(word))` call to `Int(0)`.
This changes the term executed by every loop/program claim. The mutated
definition built, but `loop-correct` exited 1 with
`WarnStuckClaimState`; see
[`body-mutation-verification.k`](evidence/body-mutation-verification.k) and
[`24-body-mutation-expected-failure.log`](evidence/24-body-mutation-expected-failure.log).
The theorem is therefore sensitive to the pinned body.

Pinning passes. Adequacy fails because the pinned body is interpreted by an
incorrect generated string semantics.

## 5. Rule-by-rule static soundness review

There are no generated helper K files beyond `semantic.k`,
`verification.k`, and `spec.k`. The local inventory contains 39 syntax
productions in `semantic.k`, seven proof-side syntax productions, one
configuration, 42 semantic rules, nine verification equations, and three
claims. There are no explicit priority rules and no `[functional]`
declarations. The extraction log is
[`27-rule-inventory-extraction.log`](evidence/27-rule-inventory-extraction.log).

### Syntax, configuration, functions, and opaque values

The semantic syntax is exhaustively:

- `Pgm`: `AST`, `runFindMax(AST,Words)`;
- `AST`: `Module(FuncDef)`; `FuncDef`: name, parameters, statement list;
  `Params`: one string;
- `Stmts`: juxtaposed `List{Stmt,""}`;
- `Stmt`: `Assign`, `For`, `If`, `Return`;
- `Expr`: `Name`, `Str`, `Int`, `UnaryOp`, `Call`, `Compare`;
  `CmpOp`: operator string plus right expression;
- `Words`: `nil`, `cons(String,Words)`;
- `Value`: `strVal`, `intVal`, `boolVal`, `wordsVal`, and later `setVal`;
- `Result`: `noResult`, `result(Value)`;
- `KItem`: `exec`, `eval`, `store`, `negate`, `callArg`, `cmpLeft`,
  `cmpRight`, `branch`, `startFor`, `loop`, `finishReturn`;
- `Int` functions: `distinctCount(String)` and
  `distinctCountFrom(String,Int)`.

Proof-side syntax is exhaustively `solutionLoopBody`, `solutionAST`,
`candidate`, `consider`, `maxCandidate`, `candidateWord`, and `findMaxSpec`.

The configuration has exactly the used components: `<k>`, input `<words>`,
locals `<best>`, `<bestCount>`, `<word>`, `<count>`, and observable
`<result>`. There is no unused heap, allocation, I/O, or exception cell.

The eight local functions are:

| Function | Attributes and coverage |
|---|---|
| `distinctCount` | `[function,total]`; its only defining rule is `[concrete,simplification]`, so symbolic values remain opaque and LLVM reports a non-exhaustive total function |
| `distinctCountFrom` | `[function]`; three concrete/simplification equations partition reachable index states and descend by incrementing the index |
| `solutionLoopBody`, `solutionAST` | constant `[function]` aliases, each with one exact equation |
| `consider` | `[function]`; three guarded equations |
| `maxCandidate` | `[function]`; `nil` and `cons` equations |
| `candidateWord`, `findMaxSpec` | `[function]`; one constructor projection and one fold initialization equation |

`distinctCount(S)` is the only result-bearing opaque symbol during the
symbolic proof. The axiom at line 177 constrains it to be nonnegative, but no
bridge-free universal theorem connects it to Python `len(set(S))`. The same
symbol occurs in program execution and the postcondition fold, so the
reachability proof is parametric over a score function; sharing the name does
not prove the score is Python distinct-character count.

### All 42 semantic rules

| Rules | Review |
|---|---|
| 70, 72: two entry rules | The first matches the exact target name/parameter and executes its body; the second is an unused explicit-input variant. Sound as a minimal top-level invocation harness for this body. |
| 78, 79: empty/nonempty statement sequencing | Standard left-to-right sequencing; disjoint and complete for `Stmts`. |
| 82, 83, 85, 87, 89: assignment plus four stores | Evaluates the RHS before writing the named local. Every target used by `solution.mpy` is covered. Unknown names visibly stick rather than fabricate a value. |
| 93, 94, 95, 97, 99, 101, 103: literals and name lookup | Correct for the two literal sorts and five names used by the program. Values are read from the corresponding cells. |
| 107, 108: unary minus | Operand-first evaluation and unbounded integer negation correctly model the submitted `-1`. |
| 113, 114, 115: calls, `set`, and `len` | Rule 113 evaluates the argument before the operation. Rule 114 safely keeps the source string because only cardinality is observed. Rule 115 is a result-bearing primitive bridge and is **false as a Python bridge when combined with 160–173**: it maps `len(set("😀"))` to 4 rather than 1. Binding is pinned to builtins without general environment lookup; this is acceptable for the unshadowed submitted program but does not repair the false value model. |
| 118, 120, 122, 124, 126: comparison evaluation and `>`, `==`, `<` | Left then right evaluation is explicit; operand orientation is correct. Integer operations are ordinary mathematics. UTF-8 byte lexicographic order agrees with Python code-point lexicographic order for valid encoded strings, so no separate false witness was found here. |
| 130, 132, 134: conditional and two branches | Predicate-first; `B` and `notBool B` guards are disjoint and exhaustive. |
| 138, 140, 142, 143: `for` setup, empty, and `cons` iteration | Snapshots the immutable constructor list and updates `word` before each exact body execution. Correct for this non-mutating submitted loop; finite `Words` gives structural termination. |
| 148, 149, 151: return evaluation and completion with/without continuation | Evaluates the expression, records the value once, and discards the pending in-function continuation. This preserves the abrupt return effect required by the submitted final return. |
| 160, 162, 164, 169: distinct-count recursion | Guards are disjoint on reachable nonnegative indices, recursion descends toward `lengthString`, and ground execution terminates. The implementation scans one K string byte at a time via `lengthString`, `substrString`, and `findString`; it therefore computes distinct bytes, not Python Unicode characters. This is the material semantic unsoundness. |
| 176: `S <String S => false` | Ordinary irreflexivity; sound. |
| 177: `distinctCount(S) >=Int 0 => true` | True of the ground byte-count recursion and of intended cardinality, but used as an unproved symbolic axiom. I classify the unsupported symbolic totalization as a trust/evidence gap, not as a second independent false equation. |

The six simplification rules are exactly 160, 162, 164, 169, 176, and 177.
There are no other simplifications, total declarations, priorities, or opaque
local symbols.

### All nine verification equations

- Lines 11 and 25 expand the exact loop body and complete submitted AST.
- The three `consider` equations have disjoint, exhaustive integer-order
  domains: higher score; equal score plus lexicographically smaller word; and
  lower score or a non-smaller tie. Their right-hand sides exactly match the
  program transition relative to whatever `distinctCount` means.
- The two `maxCandidate` equations structurally fold `nil`/`cons`.
- `candidateWord` is the constructor projection.
- `findMaxSpec` initializes the fold with `candidate("",-1)`.

These equations are mathematically consistent relative to an arbitrary
nonnegative score function. They do not independently establish that the score
has the source meaning.

### Construct coverage

Every constructor in `solution.mpy` is declared and reaches a rule:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax 10–12; exact entry rule 70–71 |
| juxtaposed statement lists | syntax 15; rules 78–79 |
| `Assign` | syntax 16; rules 82–90 |
| `For` | syntax 17; rules 138–145 |
| `If` | syntax 18; rules 130–135 |
| `Return` | syntax 19; rules 148–152 |
| `Name`, `Str`, `Int` | syntax 21–23; rules 93–104 |
| `UnaryOp` | syntax 24; rules 107–108 |
| nested `Call` | syntax 25; rules 113–115 |
| `Compare`, `CmpOp` with `>`, `==`, `<` | syntax 26–27; rules 118–127 |
| input list | `Words` syntax 30–31; loop rules 140–145 |

Missing semantics for unused Python constructs is not a defect in generated
minimal-semantics mode.

### Required false-conclusion witness

The false conclusion is not hypothetical. Input
`cons("😀",cons("abc",nil))` satisfies the source domain: it is nonempty,
contains different Python strings, and both implementations terminate.
Python has `len(set("😀")) = 1` and `len(set("abc")) = 3`, hence must return
`"abc"`. Rules 115 and 160–173 assign the emoji four distinct UTF-8 bytes, so
fresh K execution returns `"😀"`. The complete result/control/cell witness is
preserved in
[`12-unicode-counterexample.log`](evidence/12-unicode-counterexample.log).

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted. I created the
fresh module `SPEC-VACUITY` with the realizable initial input
`cons("a",nil)` and changed the required result to `"wrong"`.

The mutation is in
[`spec-false-result.k`](evidence/spec-false-result.k). A dry run:

```text
kprove spec-false-result.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, proving that the artifact parses and builds. The actual proof command
exited 1 with `WarnStuckClaimState`; its residual is a terminated configuration
with `best = "a"`, `bestCount = 1`, and
`result(strVal("a"))`, which cannot unify with `"wrong"`. This is the expected
unmet result obligation, not a parser error, timeout, missing import, or
unreachable mutation. See
[`25-false-mutation-dry-run.log`](evidence/25-false-mutation-dry-run.log) and
[`26-false-mutation-expected-failure.log`](evidence/26-false-mutation-expected-failure.log).

The proof is non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the successful K proof actually proves

Under the Haskell-compiled candidate theory, for every finite K `Words` term in
the displayed initial configuration, the exact constructor body regenerated
from `solution.py` terminates with:

```text
result(strVal(candidateWord(
  maxCandidate(WORDS, candidate("", -1)))))
```

where `maxCandidate` is a left fold whose score is the theory's
`distinctCount` symbol and whose tie breaker is K string order. It also proves
the exact initialization and loop-summary claims. It does not prove that
`distinctCount` is Python Unicode `len(set(s))`.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K compiler, Haskell backend, `kprove` reachability engine | All proof closure | Ordinary machine-checking trust boundary; fresh rebuild and mutation evidence support use |
| K unbounded integer and Boolean hooks | counts, guards, control | Acceptable ordinary-mathematics primitive |
| K `lengthString`, `substrString`, `findString` | score and final result | Executable primitive, but byte-oriented in this model; materially incompatible with Python strings |
| K `<String` | tie branch and final result | Acceptable for valid UTF-8 lexicographic ordering in the tested/used setting; no contrary witness found |
| `distinctCount` `[total]` plus nonnegativity simplification | every score comparison and postcondition | Result-bearing symbolic abstraction with no bridge-free universal connection theorem; compiler reports non-exhaustiveness |
| `set`/`len` binding by name | selected operation and value | Fixed external builtins are a reasonable minimal boundary for this unshadowed function, but their claimed value contract is false on Unicode |
| trusted `py2mpy.py` and constructor comparison | source-to-claim identity | Acceptable: trusted regeneration is byte-identical and depth-1 KORE states compare equal |
| `Words`/K `String` representation as Python list/string | theorem domain | List structure is adequate for this immutable loop. String representation is the failed bridge because score semantics uses bytes |
| Python differential tests | implementation-versus-canonical bridge | Finite evidence only: 2,205 generated cases plus fixed boundaries; it supports implementation fidelity but is not the K proof |
| body and false-result mutations | body sensitivity/non-vacuity | Strong reproducible evidence that the internal theorem depends on execution and constrains the result |

The internal reachability proof passes reconstruction, pinning, and
non-vacuity. Real-program soundness fails at the result-bearing
`len(set(s))` bridge, and intent adequacy fails on a material part of the
unrestricted Python string domain. Restricting the theorem to ASCII/byte
strings would be a narrowed HumanEval contract, which this benchmark
explicitly maps to `FAIL / NOT_LEGIT`, not a legitimate concern-only result.
The complete command/status index is
[`evidence/INDEX.md`](evidence/INDEX.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
