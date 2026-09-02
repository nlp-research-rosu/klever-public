# Independent adversarial audit: 143-words-in-sentence

## Executive finding

The candidate's two advertised proof commands do reconstruct cleanly and print
`#Top`, the submitted `.mpy` is the trusted translation of `solution.py`, the
claim macro expands to that exact program, the postcondition is
result-constraining, and fresh non-vacuity and body-sensitivity mutations both
fail as they should.

Those facts are not enough to make this a proof of the real program. The
end-to-end claim supplies the function with `str(sentenceCodes(W))`, but
`sentenceCodes` is an opaque constructor with no equations connecting it to
the characters of W or the separating spaces. A priority-30 operational rule
then declares, without a bridge-free connection theorem, that this string's
real `.split()` operation returns the equally opaque `wordsVals(W)`. The
iterator rules subsequently expose exactly W, which is also the W used in the
postcondition. This is a circular, result-bearing oracle.

A ground opposite-interpretation witness makes the defect concrete. Let
W0 be `["aa", "bbb", "cccc"]`, for which `validWords(W0)` is true and
`sentenceLen(W0)` is 11. Because the candidate never constrains
`sentenceCodes(W0)`, interpret it as the concrete character sequence `"x"`.
The real generated program and canonical implementation both return `""` on
`"x"`, and fixed `.split()` returns `["x"]`. The candidate priority bridge
instead admits `wordsVals(W0)`, leading to `"aa bbb"`. This is a false
conclusion on a valid intended-domain input. The machine-checked opposite
probe is in `evidence/split-bridge-opposite.log`.

Accordingly, the reconstructed `#Top` proves a theorem only in the candidate's
unsound extended theory. Gate A fails and the proof is not legitimate.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `143-words-in-sentence`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

The supplied-semantics mount is present, so the trusted mounts agree with the
rendered semantics mode. There is no infrastructure breach.

I independently checked the launcher records rather than following the
host-only provenance paths:

- the `audit_campaign` object is exactly equal to
  `/audit-campaign-lock.json`;
- the campaign lock hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  equal to the recorded hash;
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace are all present, regular/readable, and match their recorded hashes;
- the one trace file has hash
  `8f5496e58388bbe60aa2724d979e71edcc998db563fbb94e931c5c92f0202ba6`;
  all 451 JSONL records parse as JSON;
- historical runtime metrics are not required for this legacy layout and were
  not reconstructed;
- the generation records merely claim successful smoke and proof runs; that
  claim was not trusted.

The candidate prompt and translator are byte-identical to the trusted mounts.
The candidate and trusted `reference-semantics/` trees each have 25 entries.
An independent relative-path/type/content manifest is exactly identical, with
manifest hash
`51f08087b8dea320fefa19f91e0da934cbfdc8a7ce4e4f4c688a38725e409976`.
Recursive `diff --no-dereference` also exited 0. No symlinks occur anywhere
under the candidate semantics, reference mounts, or generation evidence.

All five required candidate proof artifacts are regular files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`.
Candidate caches, the `.pyc`, `spec.json`, and the supplied `kore-exec.tar.gz`
were ignored and never reused.

Reproducible records:

- `evidence/integrity_check.py` and `evidence/integrity_check.log`;
- `evidence/mounted-file-sha256.txt` (77 independently hashed mounted files);
- `evidence/symlinks.txt` (empty).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For a sentence of length 1 through 100 consisting of words separated by a
space, return, in original order and separated by single spaces, exactly those
words whose lengths are prime. The documented examples are:

- `"This is a test"` → `"is"`;
- `"lets go for swimming"` → `"go for"`.

The trusted canonical implementation splits on whitespace, tests each word
length for compositeness, and joins the prime-length words.

### Candidate implementation

`/candidate/solution.py` splits the sentence, loops over the words, and retains
lengths in the complete prime list up to 100:
`2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97`.
Because the whole sentence has length at most 100, no word can have a larger
in-domain prime length. `_plain = 0` is semantically inert in Python and is
used only as a proof-frame marker.

Fresh trusted regeneration was streamed directly into `cmp`:

```text
python3 py2mpy.py solution.py | cmp -s - solution.mpy
exit 0
```

Thus submitted `solution.mpy` is byte-identical to the output of the trusted
translator.

The independent differential test imports `/reference/canonical.py` and the
scratch copy of the generated implementation under distinct module names. It
tests the examples, the empty robustness case, all one-word lengths 1–100,
systematic two-word branch boundaries, and 500 seeded generated sentences.
After stable de-duplication there were 1,388 exact inputs and zero mismatches.
The reproducible input sequence is fixed by the script and seed 143; its
canonical JSON hash is
`db078928d3f5f40e12588ca3d5844963a56cc9661e2099882f309f4e75c42e7d`.

Evidence: `evidence/differential_test.py` and
`evidence/program-fidelity.log`.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/143`. No candidate-compiled
definition, cache, `.pyc`, proof trace, or tarball was copied. K was independently
reported as version 7.1.293.

### Concrete definition

The supplied semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Compilation exited 0. A reviewer-authored program containing the exact
generated function and eight assertions was translated with the trusted
translator and run with:

```text
krun concrete_cases.mpy --definition runtime-kompiled
```

It exited 0 at `<k> .K </k>`, with empty stack, `noRet`, `NoExc`, and exit code
0. Cases included both examples, mixed branch behavior, lengths 1, 2, 97, and
100, a total sentence length of exactly 100, and empty robustness.

Evidence: `evidence/concrete_cases.py` and
`evidence/concrete-execution.log`.

### Proof definition and every positive target

The Haskell definition was freshly compiled:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. The loop claim was first proved without trusting any candidate
claim:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant --output pretty
```

Actual result: exit 0 and `#Top`.

The end-to-end command was then run exactly as intended, with the now
independently closed loop claim trusted as a lemma:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant,SPEC.words-in-sentence-correct \
  --trusted SPEC.loop-invariant --output pretty
```

Actual result: exit 0 and `#Top`.

This establishes clean closure under the candidate's complete theory. It does
not validate that theory. Evidence: `evidence/proof-reconstruction.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the real `#loop` control point with an abstract
list `list(wordsVals(W))`. The current result is `str(A)`; `word`, `n`, and
the map remainder are framed; `_plain` is 0 and `$cells` is excluded. It
claims loop completion at `.K`, with the result replaced by
`str(filterWords(A,W))`; final `word` and `n` are existential, while the map
remainder and parent are preserved.

`SPEC.words-in-sentence-correct` starts from the complete initial
configuration, loads `solutionProgram`, and calls
`words_in_sentence(str(sentenceCodes(W)))`. It requires every modeled word to
be nonempty ASCII alphabetic and the modeled sentence length to be 1–100.
It claims the exact returned value `str(filterWords(.IntSeq,W))`, the expected
module binding, one allocated list in the heap, empty call state, `NoExc`, and
exit code 0.

The postcondition is not a free variable, tautology, or one-way implication.
The false-postcondition mutation in stage 6 confirms that it constrains the
actual returned string.

### Program identity

I parsed both submitted `solution.mpy` and `solutionProgram`, expanded macros,
rendered constructor-level JSON, and compared the byte streams. `cmp` exited
0. Therefore the function binding and body executed by the claim are the exact
submitted translated program, not a substituted body. Evidence:
`evidence/program-term-comparison.log`.

A material body-sensitivity mutation changed the executed `primeTest` branch
from 97 to 96. Constructor comparison then exited 1, and the standalone loop
claim failed with `WarnStuckClaimState` on the resulting
`selectWord`/`filterWords` mismatch. This changes the actual claim term, not
merely an external source file. Evidence:
`evidence/verification-body-mut.k` and
`evidence/body-sensitivity.log`.

### Satisfiable precondition and concrete substitution

Take W = `["aa","bbb","cccc"]`, corresponding under the intended representation
to `"aa bbb cccc"`. The independent ground K checks establish:

- `validWords(W) = true`;
- `sentenceLen(W) = 11`;
- `filterWords(.IntSeq,W) = codes("aa bbb")`.

Both Python implementations return `"aa bbb"` on that sentence. Thus the
entry precondition is satisfiable and the claimed result is meaningful.
Evidence: `evidence/ground-witness.k` and
`evidence/ground-witness.log`.

### Pinning failure

The body is pinned, but the real input-to-word-list execution is not.
`sentenceCodes(W)` is not mechanically or equationally equal to the concrete
space-separated character sequence, and `wordsVals(W)` is not equationally
equal to the concrete `ValSeq`. The proof-local split and iterator rules create
that relationship by fiat. Consequently, exact body identity does not repair
the missing value connection between a real input and the ghost W driving the
postcondition.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inspected all 2,211 lines in the supplied semantics and all candidate K
sources. `evidence/rule-inventory.txt` is a source-ordered, 1,284-line
inventory containing every configuration, syntax declaration, context, rule,
claim, function/total/macro/priority/concrete/owise attribute, and explicit
opaque/no-evaluator/trusted marker. It covers all 24 supplied semantics files,
`semantics.k`, `verification.k`, and `spec.k`. The generator is preserved as
`evidence/build_rule_inventory.sh`.

The supplied tree contains 695 rules. The candidate adds 12 syntax
declarations, 25 rules (including macro-expansion rules), ten priority-30
operational rules, five function/total declarations, and two claims. There
are no candidate simplification rules.

### Mapping the submitted program to fixed semantics

| Program construct | Declaration and fixed behavior |
|---|---|
| `Module`, statements | `syntax.k`; `core.k` `#loadAll` and left-to-right sequencing |
| `FuncDef`, call, return | `functions.k` frame creation/binding/pop and `call.k` callee/argument routing |
| `Name` | `core.k` lexical lookup and builtins scope |
| `Assign` | strict RHS in `syntax.k`; current-scope update in `controls.k` |
| string/int literals | `str.k` and `core.k` |
| `sentence.split()` | `call.k` attribute/call routing and `methods.k` `splitWS` plus allocation |
| `for` | `controls.k` `#loop/#iterNext/#loopStep`; list iterator in `list.k` |
| `len(word)` | `call.k`, `builtins.k` `seqLen`, and `core.k` `isLen` |
| integer/string equality | `operators.k`, `int.k`, and `str.k` |
| short-circuit `or` | `bool.k` head-only context and truthiness rules |
| `if` | `controls.k` branch rules |
| string `+` | left-to-right `BinOp` strictness, `operators.k`, and `str.k` `seqConcat` |

The configuration's environment, scopes, heap/allocation counter, call stack,
return state, exception, and exit-code cells are all present. The fixed rules
implement the needed evaluation order and control effects. Concrete execution
confirmed this path on normal and boundary values.

Rules in `assert.k`, `comprehension.k`, `concrete.k`, `dict.k`, `float.k`,
`range.k`, `set.k`, `sort.k`, `subscript.k`, and the unused portions of
`builtins.k`/`methods.k` were inventoried and inspected but cannot match the
submitted program's proof path. Their opaque float, sort, MD5, and total
out-of-bounds boundaries therefore have no dependent claim here.
`MPY-CONCRETE` is imported only by the LLVM definition, not the Haskell proof
definition.

### Candidate extension inventory and dispositions

| Candidate extension | Class and domain | Review |
|---|---|---|
| `.WordSeq`, `wCons` | proof-local datatype | Ordinary free constructors; acceptable. |
| `wordsVals(W)` | opaque, result-bearing `ValSeq` projection | No equations fix its value. It influences iteration, every loop branch, and the final result. |
| two `#iterNext(list(wordsVals(...)))` rules | priority-30 operational bridges | They define the ghost sequence's observable elements as W. No bridge-free theorem connects `wordsVals(W)` to a fixed-semantics list. Circular with the split bridge and postcondition. |
| `sentenceCodes(W)` | opaque, result-bearing `IntSeq` projection | No base/recursive equations, spacing equation, or connection claim. Even ground W does not reduce to character codes. |
| `sentenceLen` (three equations) | total definitional summary | Constructor-complete, descending, and correct for nonempty words separated by one space. |
| `validWords` (two equations) | total definitional predicate | Constructor-complete, descending, and correctly enforces nonempty ASCII alphabetic code sequences. |
| `primeLength` (one exhaustive equation) | total definitional predicate | Exactly matches the candidate's prime list on the entry domain 1–100. It is not a universal primality predicate above 100, but neither implementation nor entry theorem purports to use it there. |
| `selectWord` (three guarded equations) | total definitional summary | Guards are exhaustive and pairwise disjoint: prime/empty accumulator, prime/nonempty accumulator, and non-prime. Equations match separator insertion. |
| `filterWords` (two equations) | total structural fold | Constructor-complete and descending; truthfully folds `selectWord`. |
| `primeTest`, `solutionLoopBody`, `solutionBody`, `solutionProgram` | syntax macros | Macro-expanded constructor terms exactly match submitted `solution.mpy`; no runtime oracle. |
| split rule at lines 144–152 | priority-30 operational and result-bearing bridge | **Unsound/illegitimate.** It preempts fixed `splitWS`, fabricates `wordsVals(W)`, and has no bridge-free universal connection theorem. False witness below. |
| direct `#bindTgt(word)` | priority-30 operational shortcut | On the actual plain frame it has the same map update as fixed `tuple.k`. Its written match domain is broader (it does not itself exclude `$cells`), and no universal connection claim is provided. No reachable intended-input false result was found independent of the split defect. |
| direct assignments to `n` and `result` | priority-30 operational shortcuts | On the exact reachable plain map they preserve all fixed cells and perform the same update. They are proof-engineering shortcuts without machine-checked connection theorems. |
| direct `len(word)` | priority-30 binding/evaluation shortcut | Correct only because the actual entry state fixes the module/builtin chain and the program never shadows `len`; the rule's written match domain does not establish that binding. No reachable intended-input counterexample exists in this fixed program, but the connection is informal. |
| direct reads of `n`, `word`, and `result` | priority-30 lookup shortcuts | Match exact current-scope entries and are equivalent on the reachable plain frame. Their global domain is over-broad for cell-marked frames, but those frames are unreachable for this capture-free submitted function. |

The local update/lookup shortcuts read and write only `<k>`, `<env>`, and
`<scopes>` and preserve heap, counters, stack, return, exception, and exit
cells. The split bridge reads `<k>`, then uses fixed `#alloc`, which writes
heap and heapLoc. Its allocation/control footprint resembles fixed split, but
its allocated value is precisely the unproved result-bearing abstraction.
Correct state shape cannot justify a fabricated value.

### Concrete false-conclusion witness for the split/iterator abstraction

Use ground W0 = `["aa","bbb","cccc"]`. Its candidate guards are true and its
modeled length is 11. There is no equation constraining
`sentenceCodes(W0)`. An allowed opposite interpretation assigns it
`codes("x")`, an intended-domain sentence. Under real Python:

```text
"x".split() == ["x"]
canonical.words_in_sentence("x") == ""
generated.words_in_sentence("x") == ""
```

The candidate bridge instead returns `wordsVals(W0)`, and its iterator bridges
expose `"aa"`, `"bbb"`, and `"cccc"`, yielding `"aa bbb"`. Thus the extension
can enable the false conclusion:

```text
words_in_sentence("x") == "aa bbb"
```

The machine probes establish both sides:

1. With the candidate bridge present, the wrong destination
   `list(wordsVals(W0))` proves `#Top`, even after adding the ground
   projection rewrite to `"x"`; the priority bridge preempts it.
2. With an explicit ground function interpretation and the candidate bridge
   removed, supplied `splitWS` proves the actual heap list `["x"]` with
   `#Top` and rejects the `wordsVals(W0)` destination with
   `WarnStuckClaimState`.

Artifacts and exact commands are in:

- `evidence/verification-opposite-probe.k`;
- `evidence/bridge-wrong-spec.k`;
- `evidence/verification-opposite-fixed.k`;
- `evidence/bridge-fixed-spec.k`;
- `evidence/bridge-wrong-fixed-spec.k`;
- `evidence/split-bridge-opposite.log`.

This is the false-conclusion witness required to label the rule unsound. It
also demonstrates the Kit result-bearing-abstraction failure: the same ghost W
appears in the operational bridge and final summary, with no independent value
connection.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh mutation changes
only the entry destination from:

```text
str(filterWords(.IntSeq,W))
```

to:

```text
str(seqConcat(filterWords(.IntSeq,W), iCons(120,.IntSeq)))
```

That demands an extra trailing ASCII `x`. For the satisfying witness
`"aa bbb cccc"`, the real result is `"aa bbb"` and the mutated result is
`"aa bbbx"`.

The mutated spec parsed and reached the final return state. `kprove` exited 1
with `WarnStuckClaimState`; the residual is exactly:

```text
filterWords(.IntSeq,W)
#Equals
seqConcat(filterWords(.IntSeq,W), iCons(120,.IntSeq))
```

It was not a parser error, missing import, timeout, or unrelated backend
failure. Therefore the successful original claim is non-vacuous and
result-discriminating. This does not repair the unsound theory used to obtain
it.

Evidence: `evidence/spec-vacuity.k` and
`evidence/non-vacuity.log`.

## 7. Proven versus assumed accounting

### What the successful K reachability proof establishes

Under the supplied semantics plus all rules in candidate `VERIFICATION`, and
using the separately closed loop circularity, any candidate configuration
matching the entry claim's ghost-W precondition reaches the exact
`filterWords(.IntSeq,W)` result and specified final cells. The standalone loop
claim establishes the corresponding fold over `list(wordsVals(W))`. This is a
partial-correctness reachability result in that extended theory.

It does not establish that a real space-separated string is represented by
`sentenceCodes(W)`, that fixed Python `.split()` returns `wordsVals(W)`, or
that the ghost W in the postcondition is the actual word sequence of the
input.

### Trust ledger

| Boundary | Effect/dependents | Assessment |
|---|---|---|
| K 7.1.293 frontend/backend and K mathematical hooks | All compilation, rewriting, and proof closure | Normal low-level tool trust. Fresh builds and discriminating mutations provide reproducibility, not a proof of the toolchain. |
| Byte-identical supplied semantics | Intended execution model | Required trusted baseline; integrity passed. Used operations were also concretely exercised. |
| ASCII code-sequence string model | Input characters, splitting, length, concatenation | Formal language limitation. The proof domain is nonempty ASCII alphabetic words with exact single ASCII spaces. |
| `sentenceCodes(W)` intended meaning | Entry input, split result, modeled length | **Unproved and illegitimate.** No equations or connection theorem; opposite meanings are admitted. |
| `wordsVals(W)` intended meaning | Heap list, iteration, loop result | **Unproved and illegitimate.** Opaque result-bearing value observed only by candidate rules. |
| priority-30 split and iterator bridges | Every word seen by the real body and final result | **Unsound.** Circular with W in the postcondition and refuted by the ground opposite-interpretation witness. |
| direct lookup/assignment/len shortcuts | Loop execution | Informally equivalent on the reachable plain frame, but lack bridge-free universal connection claims and are written more broadly than their justification. Secondary concern, not needed for the verdict. |
| separately trusted loop lemma in the second command | End-to-end closure | Acceptable because the exact lemma independently proved `#Top` first under the same theory. |
| Canonical/generated differential tests | Implementation agreement on 1,388 finite cases | Finite empirical evidence only. It supports source fidelity and cannot validate a universal K bridge. |
| Concrete LLVM assertions | Supplied semantics behavior on eight cases | Finite evidence only; not a substitute for the reachability proof or a universal bridge theorem. |

### Gate results and decision

- Gate A, real-program soundness: **FAIL**. The result-bearing split/iterator
  abstraction has no bridge-free universal connection theorem and admits a
  concrete false conclusion on `"x"`.
- Gate B, intent adequacy: the stated W-domain otherwise models the material
  length-1–100 single-space ASCII contract, and the body/postcondition express
  the desired filter. The missing real-input/W connection prevents this from
  being an adequate theorem about that domain.
- Gate C, evidence auditability: fresh builds, exact commands, finite
  differential/concrete evidence, ground witnesses, body sensitivity, and
  non-vacuity are preserved. They do not discharge Gate A.

Because a materially unsound, result-bearing operational bridge is essential
to closure, this is not merely a thin-evidence concern. The required benchmark
mapping is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
