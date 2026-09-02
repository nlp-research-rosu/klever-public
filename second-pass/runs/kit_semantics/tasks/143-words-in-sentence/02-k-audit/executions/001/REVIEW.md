# Independent adversarial audit: 143-words-in-sentence

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I did not rely on candidate-provided
compiled definitions, proof logs, `#Top` output, `PROOF.md`, or generation
reports. All executable checks below used fresh source copies in
`/tmp/audit-work/audit-143`.

## 1. Input and provenance integrity

The declared layout is `pipeline-v3`, the condition is `kit-semantics`, and the
rendered semantics mode is `SUPPLIED_SEMANTICS`. The mode and mounts agree:
`/reference/reference-semantics` exists.

I read `/audit-input.json`, its `record_layout`, `container_paths`, hash records,
and integrity fields. I also read `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required JSON/text record under
`/generation-evidence`, and the complete structured trace. The generation
claims were not used as proof evidence.

The independent provenance check established:

- The campaign-lock file has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed JSON object exactly equals the `audit_campaign` block in
  `/audit-input.json`.
- Every required `pipeline-v3` record is a readable regular file rather than a
  symlink, and all recorded per-file hashes match.
- The generation output log was scanned in full: 1,352,454 bytes and 40,842
  lines. The required prompt, metrics, runtime metrics, usage, last message,
  invocation, run/task/result manifests, and output log are valid UTF-8.
- The sole trace file has the manifest-recorded SHA-256
  `00cdc125a55c70ec68d69dea24ef7905e87d89720ff4fc8b25f2bd36bc1671b9`.
  All 447 JSONL records parse: 134 `event_msg`, 310 `response_item`, and one
  each of `session_meta`, `turn_context`, and `world_state`.
- The mounted candidate tree's pipeline digest is
  `e8adec0aa7c3a087b2ea2c613e1909913e51502770343a8273444ef3776dde1c`,
  equal to `/generation-result.json`'s workspace digest. Its 801 entries
  contain no symlinks or unsupported nodes. All six required proof artifacts
  are readable regular files.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Recursive, no-dereference comparison of candidate and trusted
  `reference-semantics` finds exactly the same directory/file inventory and
  bytes. There are 24 regular files, no additions or omissions, and no
  symlinks. Their pipeline tree hashes both equal the task-manifest value
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
- `findmnt` reports every launcher/provenance/reference mount used here as
  read-only.

Evidence: [provenance.log](evidence/provenance.log),
[provenance_check.py](evidence/provenance_check.py), and
[mount-readonly.log](evidence/mount-readonly.log).

There is no input-integrity or audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From the trusted prompt and canonical implementation, the contract is:
for a sentence of length 1 through 100 consisting of words/letters separated
by spaces, retain exactly the words whose lengths are prime, preserve their
order, and join them with one space. The two documented results are `"is"` and
`"go for"`.

The trusted canonical implementation uses whitespace splitting, trial division
for each word length, and `" ".join`. The submitted `solution.py` uses a direct
character scan, recognizes ASCII space as the separator, and tests word length
against the complete prime list from 2 through 97. Since no word can exceed the
100-character sentence bound, this is a different but correct algorithm on the
source-contract domain. Leading, trailing, and repeated spaces do not cause
empty output words because length zero is not selected.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both MPY files have SHA-256
`6795fd3fd98dce542796f841629c7b0383e583016dc1264b66e55825a66c0e9b`;
the command exited 0. Evidence: [translation.log](evidence/translation.log).

### Independent differential testing

My test imports the trusted canonical and generated entry points separately and
also uses an independently written trial-division oracle. It covers:

- both examples;
- empty input as an outside-contract robustness case;
- minimum, maximum, leading/trailing/repeated-space, and all-space cases;
- every single-word length 1 through 100;
- every value adjacent to a bounded prime;
- representative two-word branch combinations whose total length is at most
  100; and
- 2,500 deterministic generated strings over ASCII letters and spaces.

All 2,968 cases agree among canonical, generated, and independent oracle;
there are zero mismatches. Evidence:
[differential_test.py](evidence/differential_test.py) and
[differential.log](evidence/differential.log).

This finite test supports implementation/intent alignment; it is not used as a
substitute for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts into scratch. The proof imported a fresh copy of
the trusted semantics, not candidate `*-kompiled` directories or caches.
The observed toolchain is K 7.1.293.

Fresh commands and results:

| Purpose | Exact command | Result |
|---|---|---|
| Proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled-fresh` | exit 0 |
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-fresh` | exit 0 |
| Concrete program | `krun concrete_audit.mpy --definition runtime-kompiled-fresh` | exit 0, `.K`, `NoExc`, exit-code 0 |
| Loop claim | `kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.scan-loop` | `#Top`, exit 0 |
| Complete positive claim set | `kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC` | `#Top`, exit 0 |

The concrete artifact mechanically extends the exact copied `solution.py` and
asserts both examples, lengths 1 and 2, repeated spaces, and length 100. Its
final configuration contains `"is"`, `"go for"`, `"aa bbb"`, and the expected
empty results.

Evidence:
[kompile-haskell.log](evidence/kompile-haskell.log),
[kompile-llvm.log](evidence/kompile-llvm.log),
[concrete_audit.py](evidence/concrete_audit.py),
[concrete-translate.log](evidence/concrete-translate.log),
[concrete-krun.log](evidence/concrete-krun.log),
[kprove-scan-loop.log](evidence/kprove-scan-loop.log), and
[kprove-full.log](evidence/kprove-full.log).

The candidate's two positive proof commands are the focused loop proof and the
simultaneous full claim set; both reconstructed successfully. As a supplemental
diagnostic, I selected only `SPEC.words-in-sentence`, thereby excluding its loop
circularity, and interrupted that unproductive unrolling after 180 seconds with
no output. This is not a failed submitted target: the entry theorem is
intentionally proved in the simultaneous claim set containing its auxiliary
circularity, and that set closed. The diagnostic is recorded in
[kprove-entry.log](evidence/kprove-entry.log).

Compiler warnings concern unused variables and fixed-semantics total functions
in unrelated domains. They do not alter the successful exit statuses or active
program paths.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.scan-loop` starts at the actual string-iteration loop head with:

- the real function binding and exact body;
- a remaining string `CS`;
- arbitrary current output `O`, current word `W`, and prior character `CH`;
- the actual local scope, function frame, continuation, empty heap, return,
  exception, and exit state.

It proves that the loop terminates its local computation and changes exactly:

- `result` to `scanOutput(CS, W, O)`;
- `word` to `scanWord(CS, W)`; and
- `char` to `scanLast(CS, CH)`.

All other displayed cells and the framed continuation are preserved.

`SPEC.words-in-sentence` starts in the initial configuration, loads
`#solutionModule`, and calls its `words_in_sentence` binding on `str(CS)`. Its
precondition is exactly `1 <= isLen(CS) <= 100`; it does not narrow the prompt's
letters-and-spaces domain and in fact allows a modeled superset. It proves the
returned computation is exactly `str(sentenceResult(CS))`, with the module
function binding retained and environment, scope allocator, empty heap, stack,
return, exception, and exit cells restored.

### Mechanical real-program identity

Using the fresh proof definition, I macro-expanded and emitted KORE for both
the regenerated submitted `solution.mpy` and the claim's `#solutionModule`.
`cmp` succeeded. Both KORE files have SHA-256
`2f72eb135b5c7e2ce9a067f25246eebedd818a6337f52b6b67eb9ca1dcf6f84a`.
Thus the entry claim executes the same function binding and constructor body as
the trusted translation, not a substituted helper program. Evidence:
[program-term-identity.log](evidence/program-term-identity.log).

The function body executes through fixed load, lookup, call, binding,
left-to-right expression evaluation, string iteration, tuple membership,
assignment, concatenation, final `strip`, return, and frame-pop rules. No
proof-local rule rewrites a `<k>` cell or bypasses those operations.

### Satisfiable witness and result constraint

`CS = iCons(97, iCons(97, .IntSeq))` represents `"aa"` and satisfies the
precondition with length 2. Both Python implementations and the independent
oracle return `"aa"`. A fresh fully ground K entry claim from the actual module
load/call configuration to `str(iCons(97, iCons(97, .IntSeq)))` closes with
`#Top`, exit 0. Evidence:
[ground-witness-spec.k](evidence/ground-witness-spec.k) and
[kprove-ground-witness.log](evidence/kprove-ground-witness.log).

I also changed the actual program term's emitted separator from `" "` to `"x"`
while retaining the original summary. The mutant definition compiled, but its
proof failed on the reachable case `C = 32` and `isLen(W) = 2`. The residual
explicitly contrasts accumulators ending in code 32 and code 120. This shows
the connection is sensitive to the executed body rather than merely to an
external source filename. Evidence:
[verification-body-mutant-audit.k](evidence/verification-body-mutant-audit.k),
[spec-body-mutant-audit.k](evidence/spec-body-mutant-audit.k),
[kompile-body-mutant.log](evidence/kompile-body-mutant.log), and
[kprove-body-mutant.log](evidence/kprove-body-mutant.log).

The intended-domain bridge is complete: the literal set in the program and
summary is exactly all primes at most 100. The independent oracle exhaustively
checks every possible word length 1 through 100.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried every local declaration and rule in the supplied
`semantics.k`, all 23 supplied helper files, `verification.k`, and `spec.k`.
The inventory has 960 line-addressed items:

- 239 syntax declarations;
- 713 rules;
- 5 evaluation contexts;
- 1 configuration; and
- 2 claims.

Each row records the immutable source hash, line, rule kind, attributes, and
normalized rule. This includes every `[function]`, `[total]`,
`[simplification]`, macro, `[owise]`, priority, `[concrete]`, `symbol`, and
`no-evaluators` occurrence. Evidence:
[rule_inventory.py](evidence/rule_inventory.py) and
[rule-inventory.log](evidence/rule-inventory.log).

### Mapping the submitted program to fixed semantics

| Program construct | Declaration and operative rule family |
|---|---|
| `Module`, `FuncDef`, parameters | `syntax.k`; module load/sequencing in `core.k`; closure creation, parameter binding, return/pop in `functions.k` and `call.k` |
| `Name`, `Int`, `Str` | declarations in `syntax.k`; lookup/literals in `core.k` and `str.k` |
| `Assign` and `BinOp("+", ...)` | strict assignment in `syntax.k`; local-scope writes in `controls.k`; ordered binary evaluation in `syntax.k`/`operators.k`; string concatenation in `str.k` |
| `For` over the input string | strict iterable evaluation in `syntax.k`; `#loop` control in `controls.k`; string `#iterNext` in `str.k`; target binding in `tuple.k` |
| `If` and comparisons | strict condition plus `#branch` in `syntax.k`/`controls.k`; ordered comparison contexts in `operators.k`; string equality in `str.k` |
| `len(word)` | callee lookup and ordered argument evaluation in `core.k`/`call.k`; builtin dispatch and `seqLen(str(...)) = isLen(...)` in `builtins.k` |
| membership in the prime tuple | tuple construction/iteration and membership routing in `tuple.k`; `#memberAcc` fold in `list.k`; integer values compare structurally |
| `result.strip()` | attribute/call routing in `call.k`; `strip`, `trimWS`, `revIS`, and `isWSC` equations in `methods.k` |
| final return | strict `Return`, `retV`, `#pop`, environment restoration, and frame removal in `functions.k` |

Evaluation is left-to-right where material: binary operands are `seqstrict`,
comparisons use explicit left/right contexts, calls evaluate the callee before
arguments and arguments through the ordered `#evalArgs` fold, and assignment,
`For`, `If`, and `Return` evaluate their designated expressions first.

The active rules account for all mutable state. Only local scope bindings
change in the body. The program allocates no heap object; the heap and heap
counter remain empty/zero. The call rules push the exact continuation and
caller environment; return/pop restores them, removes the local scope, resets
`scopeLoc`, and clears `ret`. No active priority rule changes that control
path. The generic call rule is `[owise]`, while the actual bound method and
builtin dispatches select their fixed, binding-sensitive paths.

### Supplied-semantics rule decisions

Every inventory row was reviewed for both truth on its declared MPY subset and
possible interference with the reachable theorem terms:

- `syntax.k`, `core.k`, `iter.k`, `str.k`, `operators.k`, `tuple.k`,
  `list.k`, `controls.k`, `functions.k`, `builtins.k`, `call.k`, and
  `methods.k` contain the active rule slice described above. Constructor cases,
  guards, evaluation contexts, priorities, scope/stack transitions, and
  recursive descent agree on all intended inputs.
- The remaining productions/rules in those partly active files, and all rules
  in `assert.k`, `bool.k`, `comprehension.k`, `concrete.k`, `dict.k`,
  `float.k`, `int.k`, `range.k`, `set.k`, `sort.k`, and `subscript.k`, require
  a construct, operator, value sort, heap reference, import, or builtin absent
  from both `solution.mpy` and the proof summaries. I checked their LHS domains
  and priorities for overlap with the active terms; none can rewrite an active
  configuration or result-bearing summary.
- `concrete.k` is imported only by the LLVM `MPY-KRUN` module, not the Haskell
  proof module. Its keyed-sort/deep-list rules are not reached by the audit
  smoke program.
- The fixed semantics declares opaque symbolic float operations, `sortVS`,
  `sortKeyVS`, and `md5hexCodes`. None appears in the submitted term,
  verification summaries, path conditions, or postcondition. Consequently no
  claim depends on an unconstrained interpretation of those primitives.
- The semantics intentionally models only a Python subset. In particular its
  ASCII/code-sequence string model is the selected semantics level. Every
  material operation of this submitted program is modeled and executed, and
  its letters-and-ASCII-space source domain stays within that model.

No supplied or proof-local rule can be given a false-conclusion witness on the
intended input domain. I therefore do not label any inventoried rule unsound.
Unused full-Python behavior is outside this theorem, rather than an oracle used
to close it.

### Proof-local extension decisions

`verification.k` has 12 syntax declarations and 18 rules:

1. Six compile-time macro declarations/rules:
   `#primeTuple`, `#emitSelected`, `#maybeEmit`, `#scanBody`, `#wordsBody`,
   and `#solutionModule`. Their expansion is the mechanically matched submitted
   program term. They do not rewrite runtime cells.
2. `primeLength` has two simplification equations. Their guards are exact
   Boolean complements, so they are disjoint and exhaustive for every integer.
   The finite set is exactly the program's tuple. The name does not smuggle in
   a program result: fixed tuple-membership execution is connected to the
   equations by the universally proved loop claim.
3. `emitWord` has one unguarded equation. It appends `W` and code 32 exactly
   when `primeLength(isLen(W))` is true, otherwise preserving `O`.
4. `scanOutput` and `scanWord` each have empty, separator, and non-separator
   cases. Empty versus `iCons` is constructor-disjoint; `C = 32` versus
   `C =/= 32` is complementary. Every recursive call consumes the tail.
5. `scanLast` has empty and constructor cases and consumes the tail.
6. `sentenceResult` has one unguarded equation composing the exact loop
   summaries, final word emission, and the fixed `strip` fold.

The `[total]` declarations have complete constructor/guard coverage. The
`no-evaluators` summary functions are not opaque: every use is reduced by the
listed explicit equations, and their value connection to execution is the
machine-checked `scan-loop` claim. There are no proof-local priority rules,
ordinary operational rewrites, opaque symbols, fresh values, trusted
primitives, or result-bearing oracles. The two claims are the only local
reachability lemmas.

The body-sensitivity residual supplies additional evidence that the summaries
do not bypass execution. The fresh false-result mutation below separately
establishes result constraint.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh
`SPEC-FALSE-AUDIT` retains the real loop claim and changes only the entry
postcondition from:

```k
str(sentenceResult(CS))
```

to:

```k
str(seqConcat(sentenceResult(CS), iCons(120, .IntSeq)))
```

This demands an extra `"x"`. It is demonstrably false for the satisfying
`"aa"` witness: both real Python implementations and the ground K proof return
`"aa"`, not `"aax"`.

The mutation built successfully:

```text
kprove spec-false-audit.k --definition verification-kompiled-fresh \
  --spec-module SPEC-FALSE-AUDIT --dry-run
exit 0
```

The real proof then exited 1 with `WarnStuckClaimState`. Its residual shows the
real stripped result on one side and that result concatenated with
`iCons(120, .IntSeq)` on the other, under the original length precondition and
a reachable prime-length final-word branch. This is the expected unmet
obligation, not a parser error, missing import, crash, timeout, or unreachable
mutation.

Evidence: [spec-false-audit.k](evidence/spec-false-audit.k),
[false-mutation-dry-run.log](evidence/false-mutation-dry-run.log), and
[kprove-false-mutation.log](evidence/kprove-false-mutation.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the exact supplied MPY proof semantics, for every modeled `IntSeq` input
whose length is 1 through 100, execution of the regenerated/submitted function
body from the displayed initial configuration reaches:

```k
str(sentenceResult(CS))
```

with the module function binding shown in the claim; restored environment and
scope allocation; empty heap and stack; `noRet`; `NoExc`; and exit code 0.
`sentenceResult` is fully defined by terminating equations that perform the
same character scan, fixed tuple selection, output concatenation, final-word
handling, and `strip` as the body. This is a partial-correctness reachability
theorem; it is not presented as a separate liveness theorem.

For the prompt's letters-and-spaces inputs, the finite tuple is exactly the
possible prime lengths, so the formal result is exactly the requested
prime-length-word filter in original order with single-space joining. The
formal precondition is not materially narrower than the source contract.

### Trust and evidence ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Supplied, hash-verified MPY semantics | Defines all execution, state, strings, and calls | Required trusted input. Every active rule was statically reviewed; concrete and proof executions were rebuilt. |
| K parser/compiler, generated strictness, Haskell backend, solver/runtime | Establishes `#Top` and symbolic implications | Standard proof-tool trust boundary; both positive runs and negative sensitivities were reproduced. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Regeneration is byte-identical; macro-expanded program KORE is also identical. |
| Code 32 and MPY `IntSeq` as ASCII space/string codes | Connects the model to the prompt's letter/space language | Directly matches the fixed semantics and the intended domain. Concrete K and Python tests support the bridge. |
| The displayed finite set is exactly the primes at most 100 | Connects the literal implementation/result to the word “prime” | Elementary bounded mathematics, exhaustively checked for every length 1–100 by an independent trial-division oracle. |
| Fixed-semantics float/sort/MD5 opaque symbols | Could affect other programs | No influence here: no active term, condition, summary, or claim contains them. |
| Candidate generation prose/logs and `PROOF.md` | None | Treated only as untrusted claims and not used to justify the verdict. |

There is no proof-local trusted primitive or empirical abstraction standing in
for program-defined execution. Differential and concrete tests support only
the Python/model and intent bridges; the universal program result comes from
the reconstructed K proof.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
auditability) all pass. There is no material adequacy gap or domain narrowing,
and the ordinary bounded-prime/encoding bridges are fully accounted for rather
than hidden. The candidate is therefore legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
