# Independent adversarial review: 143-words-in-sentence

## Executive decision

The fresh K proofs do reconstruct and are non-vacuous, and the claims
mechanically execute the constructor term generated from the submitted
`solution.py`. However, the generated semantics does not faithfully model the
real Python program over the full stated source domain.

The decisive witness is the valid one-word sentence `"λλλ"`:

- it has Python length 3, is within `1 <= len(sentence) <= 100`, and consists
  only of letters;
- both the trusted canonical implementation and submitted `solution.py` return
  `"λλλ"`;
- the freshly built K semantics evaluates `lengthString("λλλ")` to `6` and
  returns `""`.

Thus the task-shaped `If` rule in `semantic.k` can make a false result
conclusion about the real generated program. Restricting the theorem-to-Python
bridge to ASCII would materially narrow a contract that says “letters,” not
“ASCII letters.” Under the benchmark's controlling decision rule this is
`FAIL / NOT_LEGIT`, not a non-fatal concern.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. The trusted mount correctly has no
`/reference/reference-semantics`, so there is no supplied-semantics
contradiction and no infrastructure-stop condition.

I read all records required for this layout:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete 299-record JSONL trace below
  `/generation-evidence/codex-trace/`.

No required record is missing, unreadable, mistyped, or symlinked. Historical
runtime metrics are absent, which is permitted for this legacy layout.

Independent integrity results are in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log):

- the campaign object in `/audit-input.json` equals
  `/audit-campaign-lock.json`;
- the lock digest is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly as declared;
- every declared regular-file digest checked by the launcher manifest matches,
  including run/task/result/invocation/metrics/usage, generation prompt/logs,
  canonical, trusted prompt, and trusted translator;
- the independently computed trace-tree digest is
  `5615297576ddc1598f2f2bdbdbcba0fd97d47b80cc6d6f73d29ffacd95301849`,
  matching `usage.json`;
- the mounted candidate's public pipeline tree digest is
  `f16e6c9680a47e8788652cc7543c27430c4f30783b72174ed2d4122505cba7c3`,
  matching the stage-1 workspace digest;
- `/audit-input.json` also records launcher-specific
  `candidate_tree_sha256 =
  a3b8af42af1f746aac2f8a884c8d87522df4df2b9d4c7dc2bd81dbc8b6b15e2f`.
  and `generation_codex_trace_sha256 =
  a473403714ec5246015e441aafdfdf124fde9cf3b973b7e6e428664a6b44fbeb`.
  Their alternative tree encoding is not declared in the mount, so I did not
  equate them with the public pipeline encoding. The individual trace-file
  digest, trace pipeline digest, per-file hashes, and stage-workspace digest
  all independently match their generation records.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. The full structured trace parsed as 299 valid records, with 57 tool
calls and 57 corresponding outputs; see
[stage1-trace-inventory.log](/audit-output/evidence/stage1-trace-inventory.log).
The 1,119,524-byte generation output was treated only as an untrusted
construction history; its relevant success and earlier-failure markers are
recorded in
[stage1-generation-output-markers.log](/audit-output/evidence/stage1-generation-output-markers.log).

Stage 1 result: **PASS; no audit infrastructure breach**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From the trusted prompt and canonical implementation, the entry point accepts a
Python string of length 1 through 100 representing space-separated words and
returns, in original order and separated by one space, precisely the words
whose Python lengths are prime. The two documented results are `"is"` and
`"go for"`. The prompt says the sentence contains only letters; the examples
make clear that separator spaces are also part of the representation.

The submitted implementation uses `sentence.split(" ")`, a fixed list of all
25 primes through 97, and preserves order while building the output. The fixed
list is valid under the length-100 bound. It differs syntactically from the
canonical trial-division algorithm, which is allowed.

### Translator identity

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced SHA-256
`616c3c9149a1480e170f3b1819c5f26a5da81b48a41d78f0035109bd4fabc10e`,
identical to the submitted `solution.mpy`; `cmp` exited 0. Exact command and
status are in
[stage2-translator-identity.log](/audit-output/evidence/stage2-translator-identity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) independently
imports both Python entry points and uses a separate trial-division oracle. Its
9,919 unique inputs include:

- both examples and the requested empty boundary;
- every one-word length 1 through 100;
- every feasible pair of positive word lengths whose total sentence length is
  at most 100;
- witnesses for no selection, first selection, subsequent append, and the
  length-100 boundaries;
- non-ASCII letters;
- 5,000 deterministic generated inputs.

It reports zero in-scope mismatches; see
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
The retained initial run additionally records that tab-delimited input differs
because the candidate uses literal-space splitting; tabs are outside the
documented space-separated/letters model.

Stage 2 result: **PASS for the Python implementation and trusted
translation**. This finite test does not validate the K semantics.

## 3. Clean proof reconstruction

All candidate source required for execution was copied to
`/tmp/audit-work/clean`; no candidate-built definition or cache was copied or
used.

### Fresh builds

- LLVM compilation of `semantic.k` exited 113 because rule S21 uses `SY` and
  `SZ` on the right-hand side and binds them only through side-condition
  equalities. Evidence:
  [stage3-build-semantic-llvm.log](/audit-output/evidence/stage3-build-semantic-llvm.log).
  This is a candidate portability/coverage limitation, not an infrastructure
  failure.
- Haskell compilation of the same `semantic.k` exited 0:
  [stage3-build-semantic-haskell.log](/audit-output/evidence/stage3-build-semantic-haskell.log).
  Haskell is an approved concrete-execution backend.
- Fresh Haskell compilation of `verification.k` exited 0:
  [stage3-build-verification-haskell.log](/audit-output/evidence/stage3-build-verification-haskell.log).

### Concrete generated-semantics execution

The fresh Haskell semantics was run on 12 normal/boundary inputs and compared
with both Python implementations. Eleven ASCII/space cases match, including
both examples, empty input, lengths 1/2/4/100, both accumulation branches,
repeated spaces, and the `2 + 1 + 97 = 100` boundary.

The twelfth case is a genuine semantic mismatch, not a parser or tool failure:

```text
input: "λλλ"
krun exit: 0
K result: ""
canonical result: "λλλ"
candidate Python result: "λλλ"
```

See
[stage3-concrete-semantics.log](/audit-output/evidence/stage3-concrete-semantics.log).
A direct fresh term evaluation shows `lengthString("λλλ") => 6`:
[stage5-unicode-length.log](/audit-output/evidence/stage5-unicode-length.log).

### Positive proof claims

Every positive claim reconstructed from scratch, exited 0, and printed `#Top`:

| Claim | Modular treatment | Evidence |
|---|---|---|
| `loop-invariant` | proved independently | [log](/audit-output/evidence/stage3-proof-loop-invariant.log) |
| `symbolic-contract` | proved while trusting only the already-proved `loop-invariant` label | [log](/audit-output/evidence/stage3-proof-symbolic-contract.log) |
| `example-one` | independent ground proof | [log](/audit-output/evidence/stage3-proof-example-one.log) |
| `example-two` | independent ground proof | [log](/audit-output/evidence/stage3-proof-example-two.log) |
| `length-boundaries` | independent ground proof | [log](/audit-output/evidence/stage3-proof-length-boundaries.log) |
| `composite-hundred` | independent ground proof | [log](/audit-output/evidence/stage3-proof-composite-hundred.log) |

The modular `--trusted loop-invariant` use is not an unproved assumption: the
exact same definition and claim were first proved separately.

Stage 3 result: **the K closure gate passes, but concrete fidelity to Python
fails on a satisfying Unicode-letter input**.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable states

| Claim | Precondition | Postcondition | Satisfying witness |
|---|---|---|---|
| `loop-invariant` | `k` begins with the exact submitted loop body; `env` has separated string bindings for `result` and `word`; residual `RHO` contains neither key | loop terminates and `env` equals `loopEnv`/`selectedWords`; functions and result cell are framed | `WS=WCons("aa",WNil)`, `A=""`, `OLD=""`, `RHO=.Map`, `FS=.Map`, `RES=NoneVal`; post-result binding is `"aa"` and final word is `"aa"` |
| `symbolic-contract` | no `requires`; empty maps/result and exact `load(solutionProgram) ~> invoke(...S...) ~> finishProgram` | result is `selectedWords(splitWords(S),"")`; cleanup maps are empty | `S="aa aaaa"` gives `"aa"` in K and both Python implementations |
| `example-one` | fixed documented input | result `"is"` | the displayed initial configuration |
| `example-two` | fixed documented input | result `"go for"` | the displayed initial configuration |
| `length-boundaries` | fixed length-100 `aa`/97-character input | returns both words | the displayed initial configuration |
| `composite-hundred` | fixed 100-character word | result empty | the displayed initial configuration |

Every entry configuration is realizable. The `<result>` cell is equated to a
specific summary or ground string, not a free variable or one-way implication.
Concrete substitutions and comparison with both Python implementations are
recorded in the Stage 3 concrete log. The same substitution exposes the
failing `S="λλλ"` bridge: the K post term reduces to `""`, unlike the two real
Python results.

### Mechanical program identity

The trusted translator first established submitted `.mpy` identity. I then:

1. parsed that submitted program to KAST JSON under the fresh proof
   definition;
2. evaluated the claim's `solutionProgram` function as a term;
3. emitted its normalized KAST JSON;
4. compared the two byte-for-byte.

Both normalized artifacts have SHA-256
`a1bd874384ed6beb129dd3683fde8d924db4d24c62d938518b56dffe8bd0c52c`;
`cmp` exited 0. See
[stage4-constructor-pinning-json.log](/audit-output/evidence/stage4-constructor-pinning-json.log).
Thus the claims do not substitute a different body.

### Body sensitivity

A separate scratch definition changed the first executed
`solutionPrimes` entry from `Int(2)` to `Int(4)` while leaving the contract
summary unchanged. It compiled successfully, and the loop proof exited 1 with
a `WarnStuckClaimState` residual comparing the `2` and `4` membership
conditions:

- mutation: [verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k);
- build: [stage4-body-mutation-build.log](/audit-output/evidence/stage4-body-mutation-build.log);
- rejected proof: [stage4-body-mutation-proof.log](/audit-output/evidence/stage4-body-mutation-proof.log).

This mutation changes the program term actually executed by the claim and
shows genuine body sensitivity.

Stage 4 result: **program pinning and result constraint pass; adequacy to the
real Python execution model fails on Unicode letters**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory, including every syntax production, attribute, rule,
and claim, is preserved in
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). The source set
has 22 rules in `semantic.k`, 18 in `verification.k`, and six claims. There are
no other helper K files, no local `priority`, `simplification`, or `functional`
attributes, and no unequated opaque result symbols.

### Construct and configuration coverage

The submitted program uses `Module`; statement lists; `FuncDef`, `Assign`,
`For`, `If`, and `Return`; `Params`; expression/operator lists; `Str`/`Int`;
`Name`, `Attribute`, `Call`, `Compare`, `ListExpr`, `BinOp`; and `CmpOp`.
All map to declarations and behavior. The configuration models computation,
function bindings, local bindings, and returned value. No heap, allocation,
I/O, exception, or concurrency effect is used by this program.

Load, call, and statement execution are left-to-right. The loop performs
`put ~> body ~> remaining-loop`; return writes `<result>`. The exact submitted
outer/nested `If` is handled atomically by S16. That shortcut preserves its
continuation and all framed cells and is correct for the intended pure
membership/concatenation operation on ASCII strings. It is not an
unconstrained oracle: the integer list comes from the executed AST, and the
contract list is separately expanded.

### Semantic rules S1–S22

- **S1–S2 (`splitWords`)**: disjoint no-space/first-space cases, faithful to
  `split(" ")`, including empty tokens; recursion strictly shortens the suffix.
- **S3–S5 (`load`/`invoke`)**: correctly load the submitted one-parameter
  function, resolve its binding, and create its local parameter environment.
- **S6–S9 (`exec`, literal assignment, exact `For`)**: preserve sequencing and
  correctly obtain the submitted string's word sequence.
- **S10–S12 (`loop`/`put`)**: correct zero/one-step behavior. `put` requires an
  existing target, which the submitted `word=""` initialization establishes.
- **S13–S15 (`memberInt`, `conditionalAppend`)**: true equations, disjoint
  cases, and recursive descent. Non-`Int` list heads remain visibly
  unmodeled; the submitted list contains only `Int`.
- **S16 (exact nested `If`)**: materially unsound as a Python semantic rule on
  the full source domain. Concrete false-conclusion witness:

  ```text
  env before: result |-> Str(""), word |-> Str("λλλ")
  NUMS: submitted solutionPrimes
  K/S16 conclusion: result |-> Str("")
  actual Python nested If: len("λλλ") == 3, so result becomes Str("λλλ")
  ```

  The discrepancy propagates through S22 to the observable return value.
  [semantic.k](/candidate/semantic.k:113) uses K `lengthString`; the direct
  test establishes the wrong value 6 for this Python string.
- **S17–S20 (generic equality/choice/name assignment)**: equations are correct
  on their exact string-binding domains. S16 preempts them for the submitted
  nested conditional.
- **S21 (nested concatenation)**: its equation is mathematically correct when
  both source map entries are strings. Haskell unification fixes the
  side-condition variables uniquely. LLVM rejects the RHS-only-variable
  encoding; the submitted execution path is preempted by S16, so this is a
  portability/evidence gap rather than the false-result cause.
- **S22 (`Return`)**: correctly copies the bound value to `<result>` and
  preserves other cells.

The potentially overlapping groups are actually disjoint: S16's call/in-list
shape differs from S17's name/equality shape; assignment rules distinguish
literal, name, and nested binop; split guards are mutually exclusive; and
`choose` cases use different Boolean constructors.

### Verification rules V1–V18

- **V1–V4** expand the exact program list, loop body, body, and module.
  Mechanical pinning validates them.
- **V5–V9** define the independent contract list, membership, append, and
  structural selection. Trial division confirms that both source/proof lists
  are exactly the primes through 100:
  [stage5-prime-characterization.log](/audit-output/evidence/stage5-prime-characterization.log).
- **V10–V12** summarize the loop's result and final-word map effects correctly
  under the loop claim's separated-map guards.
- **V13 (`finishProgram`)** is a proof-harness cleanup primitive. It clears
  internal function/environment cells but leaves the observable result
  untouched. Consequently, empty-map postconditions describe
  program-plus-cleanup rather than raw Python locals. This is explicit and is
  not the cause of the false return result.
- **V14–V18** are truthful, structurally recursive `wellFormedWords` and
  `renderWords` equations, but no claim uses them.

`wordEnv` is declared `[total]`, although its `WCons` equation covers only maps
with a separated string `"word"` binding. For example,
`wordEnv(WCons("x",WNil),.Map)` has no defining equation. All proof uses are
inside the covered entry domain, so there is no separate false return-equality
witness from this declaration on an entry state; it remains an over-broad
totality evidence gap.

Stage 5 result: **internal equations are otherwise coherent, but S16 has the
required concrete false-result witness on a satisfying source input**.

## 6. Fresh non-vacuity test

I created a new spec module that executes the actual pinned program on
`"This is a test"` but changes the required result from `"is"` to the false
alternative `"test"`:
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k).

`kprove --dry-run` exited 0, establishing that the mutation parses and builds:
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).
The actual proof exited 1 with `WarnStuckClaimState`; the residual final
configuration contains `Str("is")` while the destination requires
`Str("test")`:
[stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).

This is a reachable unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash.

Stage 6 result: **PASS; the proof is non-vacuous and result-discriminating**.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's K theory:

1. the exact constructor loop transforms a covered result/word map according
   to `selectedWords` for every finite K `WordSeq`;
2. using that independently proved lemma, the exact submitted constructor
   module, from empty function/environment maps and `NoneVal`, reaches
   `Str(selectedWords(splitWords(S),""))` for every K `String S`, followed by
   the explicit cleanup marker;
3. the four ground result claims hold.

This is a sound, non-vacuous partial-correctness statement about the supplied K
model. It is not a legitimate proof of the real Python program over the full
source contract because the model's string-length operation has a false
observable bridge.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K Haskell backend and builtin `Int`, `Bool`, `Map`, equality | all proofs | Standard proof-tool trust boundary; acceptable. |
| K string `findString`, `substrString`, and concatenation | splitting/output | Concrete ASCII cases and equations support their uses; acceptable for those cases. |
| K `lengthString` as Python `len` | S16, membership, every result theorem | **Illegitimate for the full source domain**: `"λλλ"` evaluates to 6 in K versus 3 in Python and changes the returned result. |
| Task-shaped atomic S16 | loop lemma and all entry claims | Manually inspectable and faithful on ASCII, but has the above concrete false conclusion and no source precondition excluding it. |
| Finite list equals primality under length 100 | human-facing property | Ordinary finite mathematics, independently exhaustively checked; acceptable. It does not justify lengths beyond the source bound. |
| `loop-invariant` passed with `--trusted` in the second invocation | symbolic contract | Acceptable modular theorem reuse because the exact claim was first proved with exit 0/`#Top`. |
| `finishProgram` cleanup | empty final maps | Explicit proof-harness abstraction; concerning only for raw local-state interpretation and irrelevant to the return value. |
| Over-broad `wordEnv [total]` | loop summary definedness | Concerning global declaration; covered on every claim entry state and not the witnessed result error. |
| Trusted translator plus KAST identity | source/body pinning | Acceptable; both byte and constructor-level comparisons pass. |
| Differential and concrete tests | empirical bridges only | Finite evidence, not a substitute for K proof. The K test is what exposes the decisive semantic mismatch. |

Gate accounting:

- fresh verification closure: **PASS**;
- real-program soundness / generated-semantics fidelity: **FAIL**;
- intent/domain adequacy: **FAIL** because a valid letter-only, length-3 source
  input is excluded by the byte-oriented bridge;
- non-vacuity: **PASS**;
- evidence reproducibility: **PASS**, with the noted LLVM and over-broad
  totality limitations.

The failure is a candidate semantic/model defect, not a timeout, backend
crash, malformed mount, or other audit infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
