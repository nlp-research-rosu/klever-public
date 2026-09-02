# Independent adversarial review: 117-select-words

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed both K definitions
from source, independently proved the loop claim and the complete two-claim
specification, mechanically pinned the claim's constructor term to the
trusted-regenerated `solution.mpy`, checked a literal ground result, rejected a
material mutation of the executed body, exhaustively inventoried the K sources,
and rejected a fresh false postcondition.

I did not rely on the candidate's compiled definitions, logs, `PROOF.md`, or
reported `#Top`.

## 1. Input and provenance integrity

### Declared layout and infrastructure

`/audit-input.json` declares:

- problem `117-select-words`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the launcher container paths used in this audit.

The trusted `/reference/reference-semantics` tree is present, as required for
this mode. There is no contradictory hidden/generated-semantics condition, so
the infrastructure-stop rule does not apply.

All required pipeline-v3 records are present and readable:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/runtime-metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- the 397-line structured trace at
  `/generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T02-15-07-019f9820-b0e7-7a62-afb4-ee4e0c84353c.jsonl`.

I parsed the complete JSONL trace and inventoried all 63 ordinary function
calls, 22 custom calls, their outputs, and all assistant messages. The
generation records merely claim that generation succeeded; none is used as
proof evidence. Bounded generation summaries are preserved in
`evidence/generation-trace-summary.log` and
`evidence/generation-output-summary.log`.

### Campaign lock and hashes

The JSON value of `/audit-campaign-lock.json` deep-equals the
`audit_campaign` block in `/audit-input.json`. Its independently computed
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the declared value.

Independent hashes of the mounted canonical, prompt, translator, run/task
manifests, stage-1 result, and every required generation record match the
launcher-declared hashes. The trace itself hashes to
`9a2161b83185b01010e2c33b20a3b47ceccf2c156c1a11a066174f6eea5caddb`,
also exactly as recorded in `/generation-result.json`.

One untrusted telemetry field is internally different:
`usage.json.source_trace_sha256` says
`1a1d3eae7e7d4f04c1e24764c3e37d08c6e41ec8e19ef04b4cf8e25a915bcca8`.
That is not the mounted trace's byte hash. This is not a launcher-declared mount
failure: `usage.json` itself has the correct launcher hash, and the stage-1
result records the correct trace hash. It has no bearing on the independently
reconstructed proof.

Exact commands and results are in:

- `evidence/run_integrity_checks.sh`;
- `evidence/stage1-integrity.log`; and
- `evidence/stage1-reviewer-tree-hashes.log`.

### Candidate/trusted comparisons and artifact types

`cmp` establishes byte identity for:

- `/candidate/prompt.py` versus `/reference/prompt.py`; and
- `/candidate/py2mpy.py` versus `/reference/py2mpy.py`.

`diff -qr --no-dereference` reports no difference between
`/candidate/reference-semantics` and
`/reference/reference-semantics`. The reviewer content-manifest digest for each
tree is the same:
`06160f82a2076306c4a3074692c5615b898a13fa1c7c888b1dc7cb20944fff1e`.
Both trees contain exactly 24 regular files. There are no symlinks anywhere
under `/candidate`, `/reference`, or `/generation-evidence`; hence there are no
missing, additional, mistyped, or symlinked supplied-semantics entries.

All six required candidate proof artifacts are regular, nonempty files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-built `runtime-kompiled`,
`verification-kompiled`, `__pycache__`, logs, and traces were not copied into
the reconstruction.

Stage 1 result: **PASS**. No audit infrastructure breach or candidate
provenance-integrity defect was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, the contract is:
for a string containing only letters and spaces and a natural number `n`,
return, in encounter order, all whitespace-delimited words containing exactly
`n` consonants. Vowels are the case-insensitive ASCII letters `a`, `e`, `i`,
`o`, and `u`. Empty input returns an empty list.

The canonical implementation uses `s.split()`, counts each character whose
`.lower()` is not one of the five lowercase ASCII vowels, and retains words
whose count equals `n`.

The candidate implementation scans the input character by character. A literal
space flushes a nonempty current word when its count equals `n`; a nonspace
character extends the word and increments the count exactly when it is absent
from `"aeiouAEIOU"`. A final flush handles a trailing word. On the promised
letters-and-spaces domain, this is equivalent to the canonical algorithm,
including leading, trailing, and repeated spaces and `n = 0`.

### Trusted regeneration

In the source-only scratch directory
`/tmp/audit-work/117-select-words-audit`, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. The submitted `solution.mpy` is therefore byte-for-byte
the trusted translator's output for the submitted `solution.py`.

### Independent differential testing

`evidence/differential_test.py` imports the trusted canonical and generated
entry points through separate explicit file paths and does not reuse any K
summary equation. It covers:

- all five documented examples;
- 18 explicit empty, spacing, final-flush, vowel/consonant, count-boundary, and
  Unicode-letter cases;
- every string over `"aBEc "` of length 0 through 6, paired with every
  `n` from 0 through 7; and
- 3,000 deterministic generated strings of length 0 through 64 over ASCII
  letters and spaces, with `n` from 0 through 69.

Result:

```text
checks=159271
mismatches=0
differential_exit=0
```

As an additional domain check, I scanned every Unicode code point. No
non-ASCII alphabetic character outside `"aeiouAEIOU"` has Python `.lower()`
equal to a one-character ASCII vowel, so the two vowel tests do not silently
diverge on prompt-valid Unicode letters.

Evidence:

- `evidence/stage2-fidelity.log`;
- `evidence/differential_test.py`; and
- `evidence/stage2-unicode-domain.log`.

Stage 2 result: **PASS**. No program/canonical divergence was found on the
intended domain.

## 3. Clean proof reconstruction

### Isolation

I created `/tmp/audit-work/117-select-words-audit` from source files only. The
semantics copied there came from the trusted `/reference/reference-semantics`,
after the exact recursive comparison. No candidate-built definition, cache, or
generated backend artifact was reused.

The installed tools independently report K version `v7.1.293`.

### Fresh concrete definition

I built the trusted supplied semantics:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

Exit status: 0. The compiler emitted supplied-semantics nonexhaustiveness
warnings for functions outside the exercised program path and unused-variable
warnings in `strLt`; no build error occurred.

I generated `reviewer-smoke.mpy` from
`evidence/reviewer-smoke.py` with the trusted translator and ran:

```text
krun reviewer-smoke.mpy --definition reviewer-runtime-kompiled
```

Exit status: 0. The final configuration contains `.K`, `NoExc`, exit code 0,
an empty stack, and the expected heap results for the examples and boundary
assertions. See:

- `evidence/stage3-kompile-llvm.log`; and
- `evidence/stage3-krun-reviewer-smoke.log`.

### Fresh proof definition and positive claims

I then built:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

Exit status: 0. Only the irrelevant supplied `strLt` unused-variable warnings
were emitted.

I independently ran the loop claim:

```text
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.select-words-loop
```

Result: `#Top`, exit 0.

I then ran the complete spec, which makes the loop circularity available to the
entry theorem and proves both positive claims:

```text
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

Result: `#Top`, exit 0.

Exact bounded logs:

- `evidence/stage3-kompile-haskell.log`;
- `evidence/stage3-kprove-loop.log`; and
- `evidence/stage3-kprove-all.log`.

Stage 3 result: **PASS**. Every positive target claim closes in a fresh
source-built definition.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

`SPEC.select-words-loop` assumes `N >= 0` and a realizable loop-head state:

- `S` is the unprocessed finite string suffix;
- the ordinary local scope contains exactly `s`, `n`, `result`, `word`,
  `count`, and `ch`;
- `result` refers to heap location `H`, which holds accumulated list `A`; and
- the active computation starts with the real `#loop` and exact loop body,
  followed by an arbitrary framed continuation.

It proves that the loop finishes, preserves the framed state, changes the
result heap entry to `scanAccum(S,N,WORD,COUNT,A)`, and changes the three
loop-local values to `wordAfter`, `countAfter`, and `charAfter`.

`SPEC.select-words` assumes only a finite semantic string `S` and natural
integer `N >= 0` in the complete initial configuration. It loads a module
defining `select_words`, resolves and calls that binding, binds `s` and `n`,
executes the whole submitted body, and returns `ref(0)`. The postcondition
requires heap location 0 to hold exactly
`list(selectScan(S,N,.IntSeq,0,.ValSeq))`; it also constrains the final module
binding, heap and scope counters, stack, return state, exception state, and
exit code. The return is not a free variable, tautology, or one-way
implication.

### Mechanical constructor pinning

The pinning chain is:

1. trusted translator regeneration is byte-identical to `solution.mpy`;
2. `kast` parses both the trusted-regenerated constructor text and the
   reviewer-normalized explicit constructor text to byte-identical KORE
   (`constructor_cmp_exit=0`);
3. `evidence/spec-program-identity.k` checks that the three proof-side AST
   aliases normalize to that complete function body, and `kprove` returns
   `#Top`, exit 0; and
4. the entry claim places that body in the loaded `FuncDef`, while the fixed
   semantics stores and dispatches the same closure body.

The identity claim is reported as trivial after compiler normalization because
the nullary `[function,total]` AST names are expanded during preprocessing;
that is the intended constructor equality, not an execution theorem.
Reviewer-only parser-format iterations before the final normalized artifact are
preserved separately and did not modify candidate inputs.

Evidence:

- `evidence/solution-expanded-normalized.mpy`;
- `evidence/stage4-kast-constructor-compare.log`;
- `evidence/spec-program-identity.k`; and
- `evidence/stage4-program-identity.log`.

### Satisfiable witness and concrete substitution

The precondition is satisfiable, for example with semantic string `"b"` and
`N = 1`. `evidence/spec-ground-witness.k` substitutes those values into the
whole-program configuration and replaces the summary postcondition with the
literal heap list `["b"]`.

```text
kprove spec-ground-witness.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-GROUND-WITNESS
```

Result: `#Top`, exit 0. Independently:

```text
canonical ['b']
generated ['b']
```

See `evidence/stage4-ground-witness.log` and
`evidence/stage4-python-witness.log`.

### Body sensitivity

`evidence/spec-reviewer-body-mutation.k` materially changes the executed
`FuncDef` and stored closure body by initializing `count` to 1 instead of 0.
For `"b", 1`, it retains the original literal `["b"]` obligation. Fixed
execution reaches an empty result list, and the proof fails with
`WarnStuckClaimState`, exit 1. The residual shows the mutated closure body and
`0 |-> list(.ValSeq)`. This tests the program term itself, not an external
source file.

Stage 4 result: **PASS**. The theorem pins and is sensitive to the actual
translated program, and its result is materially constrained.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` extracted every top-level declaration from
`reference-semantics/semantics.k`, all 23 supplied helper files,
`verification.k`, and `spec.k`. The exhaustive
`evidence/k-rule-inventory.tsv` contains, after its header:

- 231 syntax declarations;
- 717 rules;
- five evaluation contexts;
- one configuration;
- two reachability claims; and
- all module/import/require declarations.

There are 38 proof-local entries and 1,062 byte-identical supplied-semantics
entries. `evidence/stage5-rule-review.md` gives the individual disposition of
every proof-local declaration/rule and the reachability disposition of every
supplied entry.

### Supplied semantics and used-construct coverage

The supplied tree contains no `select_words`, consonant, vowel-literal, or
problem-117 task rule. Its 22 `no-evaluators` symbols are confined to MD5,
float, and sort operations, none of which occurs in the program, summaries, or
claims. Its 35 `[concrete]` rules are not imported into the proof's `MPY`
module. Other unused fixed rules have root symbols or sorts the submitted term
never constructs and cannot contribute to claim closure.

The reachable fixed rules were checked individually:

- configuration, module loading, and statement sequencing;
- function definition, lookup, callee/argument evaluation, parameter binding,
  frame push, return, and frame pop;
- list allocation, local assignment, name lookup, and heap mutation;
- single-pass string iteration and `ch` target binding;
- strict/short-circuit evaluation of `If`, `BoolOp("and")`, comparison, and
  arithmetic/string operators;
- exact ASCII string literals, string concatenation and membership; and
- bound-method dispatch and in-place list append.

Their control and state footprint matches the program. The result list is
allocated once at heap location 0. Loop steps write only `word`, `count`, `ch`,
and the list at the referenced heap location. String concatenation allocates
no hidden heap object. `append` mutates that exact list and its `noneV` result
is discarded. The loop body contains no return, break, continue, exception,
output, or allocation, so the loop claim's arbitrary trailing continuation
and framed cells are valid. Return and frame cleanup remain in fixed semantics
outside the loop circularity.

### Every proof-local rule

There are nine proof-local `[function,total]` symbols and 22 equations:

- AST equations `charLoopBody`, `afterCharLoop`, and `selectWordsBody` exactly
  name the submitted constructor fragments.
- `flushSelected` has three disjoint cases: unequal count; equal count with
  empty word; and equal count with nonempty word.
- `selectScan` composes a completed-word scan with the final word/count flush.
- `scanAccum` has one empty case, three exhaustive space cases, and
  complementary nonspace vowel/nonvowel cases.
- `wordAfter` has empty, space, and nonspace cases.
- `countAfter` has empty, space, nonspace-vowel, and
  nonspace-nonvowel cases.
- `charAfter` has empty and cons cases.

Every recursive rule consumes one `iCons`; `flushSelected` is nonrecursive and
`selectScan` expands once. Space/nonspace, equality/inequality,
empty/nonempty, and vowel/nonvowel guards are exhaustive and pairwise disjoint,
or agree where constructor specialization could overlap. The exact
rule-by-rule findings, with inventory IDs K1067 through K1100, are in
`evidence/stage5-rule-review.md`.

The summary functions are result-bearing, but they never occur at the head of
the `<k>` cell and never replace an MPY operation. Their values are connected
to fixed execution by the universal symbolic loop and entry reachability
claims. They are therefore definitional postcondition summaries, not
operational bridges or opaque oracles.

There are no proof-local operational rules, priorities, macros, opaque terms,
`functional` declarations, or trusted primitives. No rule encodes an
unconnected answer, bypasses real execution, fabricates a used operation, or
silently narrows the input domain. I found no unsound rule, so there is no
false-rule witness to report.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I inspected no candidate mutation as authority. I created the fresh
`evidence/spec-reviewer-false-result.k` and
`evidence/run_false_mutation.sh`.

The satisfiable witness is `s = "a b"` and `n = 1`. Both trusted canonical and
generated Python implementations return `["b"]`. The mutation executes the
correct program body but demands literal result `["a"]`.

```text
kprove spec-reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT
```

The spec builds successfully. `kprove` exits 1 with
`WarnStuckClaimState`. The reached residual has:

```text
0 |-> list(vCons(str(iCons(98, .IntSeq)), .ValSeq))
```

which is literal `["b"]`, while the destination demands `["a"]`. This is the
expected reachable result mismatch, not a parse failure, missing import,
timeout, or unrelated crash. The wrapper validates the expected nonzero status
and exits 0.

Evidence: `evidence/stage6-false-mutation.log`.

Stage 6 result: **PASS**. The proof is non-vacuous and discriminates a false
result obligation.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditional on the supplied MPY semantics and K toolchain, for every finite
`IntSeq` string `S` and every mathematical integer `N >= 0`, if the submitted
translated function terminates from the specified initial configuration, it
returns reference 0 whose heap object is exactly
`selectScan(S,N,.IntSeq,0,.ValSeq)`. The fixed execution also leaves the
constrained module binding, counters, stack, return, exception, and exit cells
in the post-state stated by the claim.

The equations defining `selectScan` establish: scan left to right; treat code
32 as the separator; never emit an empty token; count a character precisely
when the one-character string is absent from `"aeiouAEIOU"`; append a word
precisely when the count equals `N`; and preserve encounter order. This covers
the entire promised letters-and-spaces source domain, not finitely many sizes
or examples. The formal string domain is broader than the prompt's, and the
only input restriction, `N >= 0`, is exactly the natural-number requirement.

This is a partial-correctness result. The report does not elevate finite
concrete tests to a proof of termination, complexity, or full CPython
equivalence.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| `/reference/reference-semantics` and imported K builtin theories (`INT`, `BOOL`, `STRING`, `MAP`, `LIST`, `K-EQUAL`) | Define all value, control, scope, heap, equality, and arithmetic behavior for both claims | Acceptable benchmark-fixed trust boundary. The candidate copy is byte-identical; every program-reachable rule was statically checked and fresh concrete execution passed. |
| `/reference/py2mpy.py` | Maps `solution.py` to the program constructor term | Acceptable trusted input. Byte regeneration and KORE constructor comparison establish identity for this submission; this audit does not prove the translator correct for all Python. |
| K v7.1.293 compiler, Haskell prover/backend, LLVM backend, and solver machinery | Parsing, compilation, symbolic reachability, simplification, and concrete execution | Standard trusted computing base. Fresh dual-backend builds, positive proofs, a ground theorem, body sensitivity, and a discriminating false mutation provide independent checks. |
| Proof-local mathematical summaries | Constrain loop locals and the final heap result | Formally connected, not assumed: exhaustive definitions plus the symbolic loop and entry claims connect them to fixed execution. No opaque summary remains. |
| English “consonant” interpretation | Relates the exact non-`aeiouAEIOU` predicate to the HumanEval wording | Adequate on the prompt's letters-only domain and exactly matches the trusted canonical behavior there. Unicode-wide casing scan found no hidden letter-domain divergence. |
| Differential tests and concrete smoke cases | Empirical fidelity/adequacy evidence | Finite supporting evidence only. They do not replace the universal K proof. |

### Gate and decision accounting

- Gate A (real-program soundness): **PASS**. Exact body execution, complete
  state footprint, no bridge/oracle, satisfiable ground witness, body
  sensitivity, and false-result rejection all hold.
- Gate B (intent adequacy): **PASS**. The formal precondition includes the full
  source-contract domain and the postcondition states the requested selection
  property without a finite bound.
- Gate C (trust and evidence auditability): **PASS**. All reviewer evidence,
  commands, statuses, scripts, positive outputs, and negative residuals are
  preserved under `/audit-output/evidence`.

There is no material adequacy, soundness, or pinning gap. The internal
generation-telemetry hash observation is unrelated to proof legitimacy and is
fully superseded by the fresh reconstruction.

VERDICT: PASS
LEGITIMACY: LEGIT
