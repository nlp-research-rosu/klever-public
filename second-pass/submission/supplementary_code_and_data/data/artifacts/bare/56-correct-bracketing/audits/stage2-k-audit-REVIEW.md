# Independent adversarial audit: 56-correct-bracketing

The candidate cleanly reconstructs and its submitted claims are non-vacuous,
but it does **not** contain a universal proof about the real string-input
execution of the generated program. Its unbounded theorem replaces the
runtime input value `SVal(String)` and `forString` execution route with a new
`SeqVal(BracketSeq)` value and separate `forBracketSeq` rules. No universal,
bridge-free theorem connects those routes. The only claims that execute real
strings are four fixed examples. Under the benchmark's real-program-pinning
and unrestricted-domain rules, that is not a legitimate proof of the target
contract.

## 1. Input and provenance integrity

I treated all generation records and everything in `/candidate` as untrusted
evidence.

The launcher declares:

- problem `56-correct-bracketing`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required
`/generation-evidence` records, the optional-present `usage.json`, the complete
33,269-line `codex-output.log`, and all 424 JSONL trace records. The structured
trace contains 92 tool calls and 92 corresponding outputs; its history
includes several failed/stuck proof iterations before the final untrusted
`#Top` claim. The bounded traversal is preserved in
[`stage1-generation-record-inspection.log`](/audit-output/evidence/stage1-generation-record-inspection.log).

All required mounts and records are real regular files/directories, with no
symlinked entry. The campaign-lock JSON object is byte-for-byte consistent
with the campaign block in `/audit-input.json`, and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

Every recorded regular-file hash checked independently matches, including:

- trusted canonical, prompt, and translator;
- candidate prompt and translator;
- run, task, result, invocation, metrics, usage, and generation prompt;
- Codex last message and output log;
- the sole structured-trace JSONL file and all files named in the result's
  evidence map.

The candidate prompt and translator are byte-identical to the trusted mounts.
The candidate tree's installed pipeline digest is
`bc5fe6d1c6dc5e2670bd6868a9153a0e2305cdeab899479cbb5b435dbec7ddf9`,
which exactly equals both the generation result and invocation's retained
workspace digest. The trace tree's installed pipeline digest is
`fd8daf18537f94d81de70be61f17022eae9b64b2a4ab0361d0fe6ab811266451`,
which exactly equals `usage.json`'s source-trace digest; its only file also
matches the result manifest.

`/audit-input.json` additionally contains opaque candidate/trace tree values
generated with an unstated directory serialization. Recomputing with the
installed `pipeline_contract.sha256_tree` produces the pipeline values above,
not those two opaque values. Because all contained regular-file hashes and
the independently documented pipeline tree hashes match their generation
records, this is a hash-algorithm auditability observation, not evidence of a
changed or malformed mount.

As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` is absent. I did not search for or infer a
hidden semantics. Full checks and exact values are in
[`stage1-provenance-final.log`](/audit-output/evidence/stage1-provenance-final.log);
the checker is
[`audit_provenance.py`](/audit-output/evidence/audit_provenance.py).
There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that `brackets` is a string over the alphabet
`<` and `>`, and the function returns true exactly when it is correctly
balanced: no prefix has more closes than opens, and the final counts are
equal. The trusted canonical implementation keeps a depth, rejects a negative
prefix, and accepts exactly when the final depth is zero
(`/reference/canonical.py:20`).

The candidate implementation uses the same algorithm
(`/candidate/solution.py:1`). Regeneration with the trusted translator:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/proof/solution.py \
  > /tmp/audit-work/proof/solution.regenerated.mpy
```

exited zero. Both submitted and regenerated MPY files have SHA-256
`3039e272296d96e5905974965b5613d576d5dba41743b002a2acff18e3d09409`,
and `cmp` exited zero.

The independent differential script
[`differential_test.py`](/audit-output/evidence/differential_test.py) compares
the trusted canonical, candidate Python, and an independently written stack
oracle. It checks:

- all four documented examples;
- empty, singleton, prefix-negative, final-positive, nested, sequential, and
  deep boundary cases;
- every one of the 8,191 strings of lengths 0 through 12;
- 1,000 seeded strings of lengths 13 through 512.

All 9,203 evaluations agree, with zero mismatches. The exact command, named
inputs, seed, result digest, and exit statuses are in
[`stage2-fidelity-differential.log`](/audit-output/evidence/stage2-fidelity-differential.log).
Thus the generated Python implementation itself is faithful on the intended
domain.

## 3. Clean proof reconstruction

I copied only `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` to `/tmp/audit-work/proof`.
Candidate-compiled directories, `expanded.k`, archives, caches, logs, and
traces were not copied or used.

Fresh builds from source were:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-llvm-kompiled

kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-haskell-kompiled
```

Both exited zero. See
[`stage3-clean-build.log`](/audit-output/evidence/stage3-clean-build.log).

Fresh concrete execution used the real submitted `solution.mpy` and the LLVM
definition on 12 normal/boundary inputs, including `""`, `"<"`, `">"`,
`"<>"`, `"<<"`, `">>"`, `"<<>>"`, `"<><>"`, `"<>>"`, `"><<>"`,
`"<<><>>"`, and a depth-16 balanced input. Every `krun` exited zero and
matched both Python implementations. Commands and parsed K results are in
[`stage3-concrete-semantics.log`](/audit-output/evidence/stage3-concrete-semantics.log).

The original positive command:

```text
kprove spec.k --definition audit-haskell-kompiled --spec-module SPEC
```

exited zero and printed `#Top` for all seven claims. I also added labels only,
without changing claim terms, and independently ran:

- the mutually recursive loop-claim pair;
- the universal claim with its two circularities;
- each of the four concrete examples by itself.

Every selection exited zero and printed `#Top`. Exact commands and outputs are
in
[`stage3-positive-proofs.log`](/audit-output/evidence/stage3-positive-proofs.log).
This establishes closure under the submitted theory; it does not by itself
establish that the theory proves the requested theorem.

## 4. Adequacy and real-program pinning

### Plain-language claims and witnesses

The claims in `/candidate/spec.k` say:

1. `loop-zero`: starting the **surrogate** `forBracketSeq` loop with depth zero
   returns `bracketSeqSpec(BS, 0)`.
2. `loop-positive`: starting that surrogate loop with any `D > 0` returns
   `bracketSeqSpec(BS, D)`.
3. `universal-correctness`: load the candidate function body, invoke it with
   `SeqVal(BS)`, and return `bracketSeqSpec(BS, 0)`.
4. Four fixed `SVal(String)` inputs return the documented Boolean results.

Every precondition is satisfiable. Ground witnesses include:

- loop-zero: `BS` representing `"<>"`, `D = 0`;
- loop-positive: already-processed prefix `"<"`, remaining `BS` representing
  `">"`, `D = 1`;
- universal: `BS` representing `"<<>>"`;
- each literal example as written.

For each, substituting the ground value into the claimed summary agrees with
both Python implementations. The witness record is in
[`stage4-pinning-witnesses.log`](/audit-output/evidence/stage4-pinning-witnesses.log).

### Exact submitted body

`correctProgram()` is not an arbitrary replacement body. After its
`targetLoopBody()` and `targetTail()` definitions simplify, it is the exact
constructor tree regenerated into `solution.mpy`. I mechanically compared
depth-limited KORE states:

- the real `solution.mpy` after module removal;
- `correctProgram()` after its one additional definitional expansion.

Both KORE files have SHA-256
`6b5801377d8fe1b4f8309d5887c43f021d5f054656851d92c49f590f9bffcf0f`,
and `cmp` exits zero. A mutation changing the executed `targetLoopBody` open
branch from `depth + 1` to `depth - 1` builds, but makes the original proof
fail with a real stuck residual. This confirms body sensitivity. Evidence is
in
[`stage4-body-sensitivity.log`](/audit-output/evidence/stage4-body-sensitivity.log)
and the mutation is
[`body-sensitivity.patch`](/audit-output/evidence/body-sensitivity.patch).

### Material input/execution substitution

Despite exact body identity, the universal entry state is not a real program
input state:

- the generated configuration takes `$INPUT:String` and invokes the function
  with `SVal($INPUT)` (`/candidate/semantic.k:65`);
- real string iteration dispatches to `forString`
  (`/candidate/semantic.k:136`);
- the universal claim manually supplies the newly introduced
  `SeqVal(BS)` (`/candidate/spec.k:35`);
- that value dispatches to separate `forBracketSeq` rules
  (`/candidate/semantic.k:138`).

Consequently, the universally quantified loop never executes the material
real-string rules at lines 140–145. The four fixed examples do execute those
rules, but four examples do not prove an unrestricted HumanEval input domain.

The candidate defines `bracketSpec(String, Int)` and complete string-recursive
equations in `/candidate/verification.k:9`, but no claim uses that function
and no claim connects it to actual `SVal/forString` execution.

I made the missing obligation explicit without importing any operational
shortcut. The reviewer definition adds only a truthful constructor renderer:

```text
noBrackets()       -> ""
openBracket(BS)    -> "<" + render(BS)
closeBracket(BS)   -> ">" + render(BS)
```

It then asks the exact candidate body, invoked with
`SVal(render(BS))`, to return `bracketSeqSpec(BS, 0)`, retaining the
candidate's two circularities unchanged. The definition and spec build
successfully, but `kprove` exits 1 with `WarnStuckClaimState`; the residual
shows the unproved relation between `bracketSeqString(BS)` and
`bracketSeqSpec(BS, 0)`. See
[`stage4-actual-string-bridge.log`](/audit-output/evidence/stage4-actual-string-bridge.log),
[`bridge-definition.k`](/audit-output/evidence/bridge-definition.k), and
[`spec-actual-string-attempt.k`](/audit-output/evidence/spec-actual-string-attempt.k).
This failed attempt does not show the desired theorem is false; it shows the
candidate did not establish the required universal connection.

Three ground fixed-versus-surrogate K executions (`""`, `"<>"`, and `">"`)
agree, and the broader Python/K differentials also agree. Those are finite
evidence that the intended bridge is plausible, not a universal reachability
proof. See
[`stage5-ground-representation.log`](/audit-output/evidence/stage5-ground-representation.log).

Therefore the candidate does not pin the unrestricted real-string execution
required by the source contract. It proves an extended-semantics surrogate
execution plus four real examples.

## 5. Rule-by-rule static soundness review

The complete inventory is
[`rule-inventory.md`](/audit-output/evidence/rule-inventory.md). It enumerates:

- every local syntax production and generated list;
- every function and `[total]` declaration;
- all 39 rules in `semantic.k`;
- all 11 equations in `verification.k`;
- the configuration, cells, continuations, and all seven claims;
- the declaration/rule mapping for every constructor used by
  `solution.mpy`.

There are no local priority rules, explicit `[simplification]` rules, opaque
symbols, or trusted claims.

The used source constructs are all modeled: module/function loading,
single-argument invocation, name lookup, shadowing assignment, left-to-right
arithmetic and comparison, `if`, string `for`, early/final return, and the
result cell. Addition, subtraction, equality, less-than, string slicing, and
loop binding have the correct operand order and state effects for this
program.

The noteworthy static findings are:

- `targetLoopBody`, `targetTail`, and `correctProgram` are exact definitional
  expansions, not answer oracles.
- `bracketSeqSpec` has structurally decreasing, constructor-exhaustive
  equations. Its two close rules have disjoint and exhaustive integer guards.
- `bracketSpec` likewise describes the intended stack checker, but is dead
  with respect to every submitted claim.
- `SeqVal` and `forBracketSeq` form a coherent new execution model, but their
  value/control effects determine the universal result and lack the required
  connection theorem to real strings.
- The return-unwind rule discards an arbitrary K suffix rather than stopping
  at `functionBoundary`. It is exact for every reachable return of this
  top-level program (early return must discard the loop/tail/boundary; final
  return discards the boundary). It would be too broad for nested calls, which
  this semantics does not model. I found no false-conclusion witness for that
  rule on the intended top-level input domain, so I record the narrower reuse
  limitation and do not label the rule unsound.

I found no locally false rule or equation and therefore make no unsupported
unsound-rule allegation. The failure is adequacy/real-program pinning, not
logical inconsistency: a sound theorem about the surrogate value type is being
presented as a theorem about all source strings.

## 6. Fresh non-vacuity test

The fresh mutation
[`spec-vacuity-audit.k`](/audit-output/evidence/spec-vacuity-audit.k) retains
the submitted two loop circularities and changes the universal result
obligation from:

```text
result(BVal(bracketSeqSpec(BS, 0)))
```

to the false constant:

```text
result(BVal(false))
```

The satisfying counterexample is `BS = noBrackets()`, corresponding to real
input `""`: canonical Python, candidate Python, and concrete K all return
true, while the mutation requires false.

`kprove --dry-run` exits zero, confirming the mutated artifact parses and
builds. The actual proof exits 1, contains `WarnStuckClaimState`, contains no
`#Top`, and leaves the expected unmet equality:

```text
false #Equals bracketSeqSpec(BS, 0)
```

This is a meaningful reachable result failure, not a parser error, timeout,
or unrelated crash. Exact commands, exits, and residual are in
[`stage6-false-mutation.log`](/audit-output/evidence/stage6-false-mutation.log).
The submitted theorem is result-constraining and non-vacuous under its
surrogate theory.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's generated semantics:

- the exact submitted function body, when manually invoked with any
  `SeqVal(BS)`, terminates through the modeled control rules with result
  `bracketSeqSpec(BS, 0)`;
- the two mutually recursive `forBracketSeq` invariants hold at depth zero and
  every positive depth;
- four concrete real-string invocations return their expected Booleans.

This is a partial-correctness statement under the submitted theory. It is not
a universal theorem for `SVal(S)` inputs over `[<>]*`.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K `INT`, `BOOL`, `STRING`, `MAP`, list, cell, and backend machinery | Arithmetic, comparisons, substrings, maps, symbolic execution, all claims | Ordinary low-level trust boundary; acceptable. |
| Trusted `py2mpy.py` and byte-identical regeneration | Connects `solution.py` to `solution.mpy` | Independently checked; acceptable. |
| `correctProgram`/helper constructor expansions | Connects the readable claim term to the submitted body | Exact KORE comparison plus body-sensitivity mutation; acceptable. |
| Generated concrete `SVal/forString` semantics | Real-string example claims and concrete runs | Rule review and finite concrete evidence support it; no material used-construct gap found. |
| `bracketSeqSpec` equations | Universal postcondition | Truthful exhaustive mathematical definition over `BracketSeq`; acceptable for the surrogate theorem. |
| `SeqVal/forBracketSeq` as representation of real strings | Entire universal execution, branch behavior, result, and source-domain coverage | **Illegitimate for the requested theorem without a universal connection theorem.** Only ground tests and an informal bijection support it; the candidate provides no proof connecting it to `SVal/forString`. |
| Python/K differential evidence | Implementation and finite semantics confidence | Reproducible and mismatch-free, but finite; cannot replace the missing K theorem. |
| Human interpretation “`BracketSeq` is exactly `[<>]*`” | Summary-to-source-contract bridge | Mathematically plausible but only informal in the candidate, while the operational representation changes too. |

### Gate and decision mapping

- Clean verification: **PASS** — fresh builds and all positive claims produce
  `#Top`.
- Non-vacuity: **PASS** — the false result mutation is rejected correctly.
- Rule consistency on the modeled terms: **PASS** — no false local rule was
  found.
- Real-program soundness/pinning: **FAIL** — the unbounded proof uses a
  different result-bearing input representation and loop transition system,
  with no bridge-free universal connection to the real route.
- Source-contract adequacy: **FAIL** — actual real strings are proved only at
  four fixed values; finite examples cannot establish the unrestricted
  HumanEval domain.
- Evidence auditability: **PASS with limitation** — the evidence is
  reproducible, but it supports only finite bridge instances.

This is not a timeout, tool failure, malformed mount, or other infrastructure
uncertainty. It is a candidate-level proof-adequacy defect. Because the
candidate's universal theorem does not pin the real generated program on its
actual source-contract input representation, the benchmark decision is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
