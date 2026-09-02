# Independent adversarial audit: 91-is-bored

## Executive conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt every positive proof from
source in a clean scratch tree, independently checked source-to-MPY and
constructor-level program identity, audited the proof-local bridges and summary
equations, and obtained a meaningful failure from a fresh false-result
mutation.

The result is `CONCERNS / LEGIT`, not `PASS`, because the supplied read-only
semantics recognizes only character codes 32, 9, 10, and 13 as whitespace,
whereas the submitted Python uses CPython `str.strip()` and therefore recognizes
additional whitespace. This is the documented supplied-model identification
gap covered by campaign amendment v2 exception 1: the candidate did not create
or further narrow it; the theorem quantifies over every finite `IntSeq`; the
candidate's trust ledger records it with the concrete `"I\vwork"` witness; and
the submitted Python behaves consistently with the docstring on that witness.
I reproduced the divergence independently in stage 7.

## 1. Input and provenance integrity

The launcher record declares:

- problem `91-is-bored`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a required supplied semantics mount.

All required pipeline-v3 records were present, readable, and regular where a
regular file was required: `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, all six named generation
JSON/text/log records, and the structured trace tree. The candidate, canonical,
prompt, translator, and `/reference/reference-semantics` mounts were present.
No required semantics entry was a symlink or unsupported file type.

The campaign object embedded in `/audit-input.json` is JSON-identical to
`/audit-campaign-lock.json`, and the lock's direct SHA-256 is the recorded
`053ed73c...add01`. Every direct file hash checked by
[stage1_integrity.log](evidence/stage1_integrity.log) matches its launcher
record, including the canonical, trusted/candidate prompts, trusted/candidate
translators, run/task/result records, generation records, prompt, output log,
and trace JSONL file.

Independent pipeline tree hashing gave:

- candidate: `1b7903fd...bd12`, matching the final workspace hash in both
  `/generation-result.json` and `invocation.json`;
- candidate and trusted semantics: `4495a50f...9ad1` for each, matching the
  task/run manifest semantics hash;
- trace directory: `6f1e0ebf...faea`, matching `usage.json`.

The commands and full values are in
[stage1_tree_hashes.log](evidence/stage1_tree_hashes.log). In addition, a
recursive, no-dereference comparison of the two semantics trees found no
missing, additional, changed, mistyped, or linked entry. Candidate `prompt.py`
and `py2mpy.py` are byte-identical to their trusted mounts.

I parsed all 967 structured trace events independently: zero malformed JSON
lines, 230 indexed tool/patch calls, and complete assistant-message and
success/error marker indexes. See
[stage1_trace_index.log](evidence/stage1_trace_index.log). The trace and the
4.3-million-byte `codex-output.log` contain many failed construction attempts
before the final artifacts. They were treated only as untrusted history; none
was used as proof evidence.

Stage 1 result: pass. There is no infrastructure breach, so a candidate verdict
is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted docstring says the input is a string of words, sentences are
delimited by `.`, `?`, or `!`, and the result is the number of sentences that
start with the word `I`. Its examples require:

- `"Hello world"` to return `0`;
- `"The sky is blue. The sun is shining. I love this weather"` to return `1`.

The trusted canonical is a helper witness. It splits on `[.?!]\s*` and counts
segments whose first two characters are exactly `"I "`.

### Submitted program

`solution.py` performs a character scan with state:

- `count`: already recognized boredoms;
- `at_start`: no non-whitespace character has yet occurred in the current
  sentence;
- `pending_i`: the first non-whitespace character was `I`, and its word
  boundary is still to be determined.

A delimiter counts a pending `I` and resets sentence state. Leading whitespace
is skipped. A pending `I` is counted when followed by whitespace, a delimiter,
or end-of-input; `Idea` and `Ix` are not counted. This is a defensible reading
of the docstring. Behavior for commas and exotic word boundaries is not
specified; the program treats `"I, too"` as not beginning with the token `I`.

Using the trusted translator from the clean copy:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0, and `cmp` against the submitted `solution.mpy` exited 0. Both MPY
files have SHA-256 `2fe10ae9...cacd`. Evidence:
[stage2_fidelity.log](evidence/stage2_fidelity.log).

### Independent differential

[stage2_differential.py](evidence/stage2_differential.py) independently imports
the trusted canonical and submitted entry points. It also implements a
separate split-based oracle for the candidate's documented reading, rather
than reusing the proof equations. Scope:

- both documented examples;
- 32 explicit empty, delimiter, word-boundary, leading-whitespace,
  non-ASCII, and branch-boundary cases;
- every string of length 0 through 5 over `I`, `x`, space, tab, `.`, `?`, `!`,
  and comma;
- 10,000 deterministic random strings of length 0 through 40 over a broader
  alphabet containing multiple CPython whitespace characters and non-ASCII
  text.

There were 46,805 unique cases, zero candidate-versus-independent-resolution
mismatches, and 10,495 candidate-versus-canonical mismatches. All canonical
mismatches had the candidate count larger. Representative causes were:

- standalone `I` or `I` immediately before a sentence delimiter;
- leading whitespace before the first word;
- a word boundary represented by tab, newline, vertical tab, form feed,
  non-breaking space, or em space rather than an ASCII space.

These mismatches do not violate a docstring-determined behavior. They arise
where the canonical chooses a narrower boundary rule than the plain
description. The documented examples pass. The large finite differential is
supporting evidence, not a substitute for the K proof.

Stage 2 result: pass, with the supplied-model whitespace concern accounted for
in stage 7.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/case91`; no
candidate-provided `*-kompiled` directory, cache, proof log, or KORE output was
copied or reused. The fresh toolchain reports K `v7.1.293`.

The reconstruction wrapper and exact per-command logs are
[stage3_reconstruct.sh](evidence/stage3_reconstruct.sh) and the
`stage3_*.log` files. The first wrapper invocation stopped after translation
because of a reviewer-authored brace-group `exit` mistake; it attempted no K
build and is preserved as `stage3_reconstruct_attempt1.*`. The corrected
wrapper uses subshells. This reviewer tooling error is not candidate evidence.

Fresh results:

| Command/purpose | Exit | Relevant result |
|---|---:|---|
| LLVM `kompile` of trusted supplied semantics | 0 | new `audit-runtime-kompiled` |
| `krun` of 12 new concrete assertions | 0 | final `<k> .K`, `<exit-code> 0` |
| Haskell `kompile connection.k` | 0 | new bridge-free connection definition |
| `kprove connection-spec.k` | 0 | `#Top` |
| Haskell `kompile verification-base.k` | 0 | new loop-connection definition without loop bridge |
| `kprove loop-spec.k` | 0 | `#Top` |
| Haskell `kompile verification.k` | 0 | new target definition |
| `kprove spec.k` | 0 | `#Top` |

The exact outputs are
[stage3_kprove_connection.log](evidence/stage3_kprove_connection.log),
[stage3_kprove_loop.log](evidence/stage3_kprove_loop.log), and
[stage3_kprove_target.log](evidence/stage3_kprove_target.log). The concrete
execution is in
[stage3_krun_concrete.log](evidence/stage3_krun_concrete.log).

The LLVM compiler reported non-exhaustiveness warnings for fixed-model
functions used only by other programs (`mapStrVS`, several float conversions,
`joinCodes`, and out-of-bounds `valSeqAt`). None is reachable from
`solution.mpy` or from its postcondition. Haskell builds reported only unused
source variables. No positive proof timed out, crashed, or relied on a
candidate cache.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

`LOOP-SPEC.loop` starts at the exact MPY `#loop` for the submitted loop body,
with arbitrary finite remaining input `IS`, current count `N`, booleans `A`
and `P`, exact local/function frames, exact post-loop `If; Return; #endcall`
continuation, empty heap, and exact call stack. It reaches
`scanResult(IS,N,A,P)`, restores the caller environment, deletes the local
frame, resets `scopeLoc`, pops the frame, and leaves return/exception/exit
state normalized.

`SPEC.loop` states the same helper result for the target definition with the
actual builtins scope.

`SPEC.is-bored` starts with an exact binding of `is_bored` to the macro-expanded
submitted body, calls it on arbitrary `str(IS:IntSeq)` in the exact empty
caller state, and returns `boredoms(IS)` while preserving the explicitly
framed heap, stack, scope, return, exception, and exit state.

### Program identity

The claim need not execute the whole module because its precondition pins the
exact closure binding and body. I independently parsed:

```text
kast solution.mpy ... --sort Module --output kore
kast proof-program.mpy ... --sort Module --output kore
```

under the fresh verification definition. The resulting KORE files are
byte-identical, both SHA-256 `79ef4834...be3`. This mechanically establishes
that `BORED-FUNCTION-BODY` and `BORED-LOOP-BODY` expand to the translated
submitted constructor tree. Evidence:
[stage4_kore_identity.log](evidence/stage4_kore_identity.log).

### Satisfiability and concrete substitution

The public precondition is realized by the exact empty module/caller state with
`IS = .IntSeq`. The loop precondition is realized after the empty-input call's
four initial assignments with:

```text
IS = ORIG = CUR = .IntSeq
N = 0, A = true, P = false, B = builtinsScope
env = 1, scopeLoc = 2, heap = .Map, heapLoc = 0
stack = ListItem(frame(.K, 0, 1))
```

It is also realized for `"I work"` with its six code points in `IS`.

Fresh ground entry claims for `"" => 0` and `"I work" => 1` both close with
`#Top`. Candidate and canonical Python both return the same respective values.
See [stage4-witness-spec.k](evidence/stage4-witness-spec.k) and
[stage4_witness.log](evidence/stage4_witness.log). A first reviewer version of
that ground spec had one excess parenthesis and was rejected by the parser; the
attempt is preserved separately and was not treated as proof evidence.

The return is not free, existential, or tautological. `boredoms(IS)` reduces
through total, constructor-covered equations to a structural fold over every
element of `IS`. The fresh false result mutation in stage 6 confirms that the
claim discriminates `1` from `2`.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[stage5_rule_inventory.md](evidence/stage5_rule_inventory.md) inventories all
1,059 source-level syntax declarations, configuration/context declarations,
rules, and claims from:

- every file in the trusted supplied semantics;
- `verification-base.k`, `verification.k`, and `connection.k`;
- all positive connection/loop/target specs;
- the candidate's negative mutation files, explicitly marked as untrusted
  negative evidence rather than positive-proof dependencies.

Each inventory row includes source location, normalized complete declaration
block, attributes, materiality, and review disposition. It contains 764 fixed
semantic rules, 22 candidate rules (including one negative-only mutation
rule), seven positive claims, and three candidate negative-only claims. It
also enumerates all function/total, macro, priority, simplification, concrete,
owise, strictness, and opaque declarations. The 26 explicitly
`no-evaluators` symbols are all in supplied float, sort, or MD5 support; none
is transitively reachable from this program or postcondition. There is no
proof-local opaque symbol.

For rules marked `INERT_FIXED_MODEL_NO_CLAIM_DEPENDENCY`, the constructor and
call inventory demonstrates that neither the submitted program nor any
result-bearing proof summary can match them. I therefore do not make
unsupported claims about their full CPython fidelity; under the benchmark's
required false-conclusion-witness rule they are inert for this theorem, not an
unsoundness finding. All material fixed rules and every proof-local rule were
reviewed in detail below.

### Construct-to-semantics map

| Submitted construct | Declaration and material execution |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` `#loadAll` and left-to-right statement sequencing |
| `FuncDef`, call, params, return | `functions.k` closure creation, `call.k` callee/argument routing and frame push, `functions.k` `#bindP`, `Return`, `#endcall`, and `#pop` |
| `Name` | `core.k` current-scope lookup and parent traversal; exact local maps in the claims select the intended bindings |
| `Int`, `Bool`, `Str` | literal rules in `core.k` and ASCII literal conversion in `str.k`; every program literal is ASCII |
| `Assign`, `AugAssign("+")` | state writes in `controls.k`; integer addition in `int.k` |
| `For` over a string | strict iterable evaluation; `controls.k` `#loop/#loopStep`; `str.k` `#iterNext` yielding one-character strings; `tuple.k` name-target binding |
| `If` | strict condition evaluation, `truthy(Bool)`, and disjoint `#branch` rules in `controls.k` |
| delimiter `BoolOp("or",...)` | left-to-right, value-returning short-circuit rules in `bool.k` |
| `Compare` on strings | ordered comparison contexts/dispatch in `operators.k`; structural string equality/inequality in `str.k` |
| `c.strip()` | exact local lookup, bound-method and call routing in `call.k`; `strip`, `trimWS`, `revIS`, and `isWSC` in `methods.k`; the two independently connected proof bridges below |
| state/call cleanup | exact `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>` cells in the loop theorem and bridge |

Strict/sequence-strict syntax establishes the expected evaluation order.
Delimiter comparison short-circuiting cannot skip a side effect because all
three operands are pure comparisons. String iteration is structural over the
entire finite `IntSeq`, so there is no unrolling bound.

### Proof-local definitions

`BORED-LOOP-BODY` and `BORED-FUNCTION-BODY` are syntax macros. Their exact
constructor identity is established in stage 4; they perform no execution and
introduce no value.

The result functions are ordinary mathematical definitions:

- `isDelimiter` has three singleton-true cases and one disjoint complement;
- `flag` covers both booleans;
- `charIsWhitespace` partitions `isWSC(C)` and its Boolean negation;
- `charIsI` partitions `C == 73` and `C =/= 73`;
- `scanStep` is one nested conditional whose branches exactly mirror the
  submitted assignments and count increments;
- `scan` has a base case and structurally descends from `iCons(C,REST)` to
  `REST`;
- `finishScan`, `scanResult`, and `boredoms` are direct compositions.

Their guards are exhaustive and pairwise disjoint, recursive calls descend,
and overlapping right-hand sides do not disagree. `A` is intentionally unused
by `finishScan`; only `P` controls the real post-loop increment.

### Strip-comparison operational bridges

The two priority-40 rules in `verification-base.k` match only the exact
`c.strip() == ""` and `c.strip() != ""` expressions, environment `1`, an exact
five-binding local map, and a one-character `c`. They frame the continuation,
unrelated scopes, and all omitted cells.

The skipped fixed execution performs local binding lookup, bound-method
creation, zero-argument evaluation, pure `strip`, and structural comparison.
It does not allocate, mutate, return, raise a modeled exception, or alter
control on this domain.

`connection.k` imports only the fixed supplied MPY semantics. Its four claims
cover equality and inequality under the exhaustive `isWSC(C)` /
`notBool isWSC(C)` partition, with the same arbitrary continuation and framed
state accepted by the bridges. The fresh bridge-free suite closes with `#Top`.

I additionally placed an observable `#notB` continuation after the comparison
for a space and a non-space. Both the fixed definition and bridge-enabled
definition close with `#Top`; the opposite space interpretation gets stuck at
`false`, with `WarnStuckClaimState`. Exact evidence:
[stage5_kprove_strip_fixed.log](evidence/stage5_kprove_strip_fixed.log),
[stage5_kprove_strip_bridge.log](evidence/stage5_kprove_strip_bridge.log), and
[stage5_kprove_strip_opposite.log](evidence/stage5_kprove_strip_opposite.log).
Thus binding, value, arbitrary suffix, and state framing are contained in the
universal justification domain.

### Loop operational bridge

The priority-40 loop bridge matches the exact submitted loop body, the actual
combined `If; Return` `Stmts` suffix, `#endcall`, exact function and local
frames, environment restoration, local-scope deletion, scope location, empty
heap and heap counter, exact stack frame/pop, return state, exception state,
and exit code. It admits no arbitrary continuation.

`LOOP-SPEC.loop` is byte-for-byte the same complete match domain and was proved
in the fresh `verification-base` definition, which does not import the loop
bridge. It depends only on the separately connected strip bridges. Therefore
the loop bridge has a bridge-free universal connection theorem over every
configuration it can match.

A fresh body-sensitivity test replaced both the loop body and corresponding
function-body constructor with an empty loop body. On the ground input `"I"`,
fixed execution reached `0`; the original result obligation `1` was rejected
with `WarnStuckClaimState`. This changes the term actually executed by the
claim, not merely an external Python file. Evidence:
[stage5-body-mutation.k](evidence/stage5-body-mutation.k) and
[stage5_kprove_body_mutation.log](evidence/stage5_kprove_body_mutation.log).

### Static conclusion

No proof-local rule encodes the task answer without derivation, fabricates a
used construct, substitutes a different program, introduces an unconstrained
result-bearing oracle, or discards a reachable continuation/state effect.
Priority only selects bridges within their independently proved domains.
There is no concrete or symbolic false-conclusion witness for a material rule.

Stage 5 result: pass.

## 6. Fresh non-vacuity test

I inspected the candidate `spec-vacuity.k` only as untrusted evidence and wrote
a new ground mutation,
[stage6-false-result-spec.k](evidence/stage6-false-result-spec.k).

Its precondition is the same exact public closure/body/state as the positive
claim, with the realizable input `"I work"`. Stage 4 independently established
that candidate Python, canonical Python, and a ground K claim all return `1`.
The mutation changes only the required result to `2`.

The mutation parsed and built successfully. `kprove` exited 1 and emitted
`WarnStuckClaimState`; the residual configuration visibly contains the actual
submitted closure/body and `<k> 1 ~> .K </k>`, which cannot match destination
`2`. This is the expected unmet result obligation, not a timeout, parser
failure, unreachable mutation, or unrelated crash. Full command and residual:
[stage6_nonvacuity.raw.log](evidence/stage6_nonvacuity.raw.log).

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied MPY/K theory, for every finite `IS:IntSeq`, if the
exact translated `is_bored` closure called in the stated initial configuration
terminates in the claim's terminal form, it reaches `boredoms(IS)`. The returned
integer is the structural scanner fold described above, and the explicit
caller state is restored. This is partial correctness, not a separate
termination theorem.

The auxiliary theorem formally connects the exact real loop execution,
including frame cleanup and result, to `scanResult`. The connection suite
formally connects both used `strip` comparisons to `isWSC(C)` for all integer
character codes under the fixed model. The equations then formally reduce
`boredoms` over an arbitrary finite sequence; there is no size bound.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| K frontend, generated strictness, Haskell reachability backend, LLVM runtime, and builtin Int/Bool/String/Map/List theories | parsing, execution, circularity, arithmetic, maps, and all claims | Ordinary toolchain trust boundary; exact K `v7.1.293` commands and fresh outputs preserved |
| Supplied read-only MPY operational semantics | all program execution | Required fixed model; exact candidate/trusted tree identity established; material rule path statically audited |
| Proof-local strip bridges | branch values and therefore final count | Not assumed: four bridge-free universal claims, fixed-vs-bridged suffix probes, and rejected opposite interpretation |
| Proof-local loop bridge | final result and complete call/frame state | Not assumed: bridge-free universal loop theorem over its exact full context; fresh real body mutation rejected |
| Scanner equations | final postcondition | Truthful, total, disjoint/covered, and structurally descending; connected to real loop execution |
| Body macros and prebound closure entry | real-program identity | Fresh trusted translation plus byte-identical macro-expanded KORE |
| Docstring-to-word-boundary reading | human-facing meaning of the mathematical scanner | Informal but explicit; documented examples and 46,805 independent cases support it. Canonical edge mismatches were judged against the docstring, not treated as failures by identity alone |
| Termination | total correctness | Not proved and not required; theorem is explicitly partial correctness. The operational fold is over finite algebraic strings |
| Explicitly opaque supplied float/sort/MD5 symbols and other unused fixed rules | none | No constructor/call dependency from this program or postcondition; all 26 no-evaluator symbols are inventoried and inert |

### Supplied-model representation/identification gap

The fixed rule at `reference-semantics/semantics/methods.k:85-86` defines
`isWSC(C)` as membership in `{32, 9, 10, 13}`. CPython considers vertical tab
code 11 whitespace. On `"I\vwork"`:

- the submitted Python returns `1`;
- the canonical helper returns `0`;
- the clean MPY execution returns `0` and exits 0.

[stage7_model_boundary.log](evidence/stage7_model_boundary.log) records the
fresh translation, K execution, `"\v".isspace() == True`, and both Python
results. The candidate's `PROOF.md` had already named the same boundary and
witness, satisfying the documentation requirement; this audit independently
verified it.

This is model-versus-CPython, not program-versus-docstring. The submitted
Python's use of `str.strip()` behaves naturally on the gap. The theorem does
not exclude code 11 or any other `IntSeq` value and introduces no additional
candidate restriction; it proves the model's behavior for those values.
Accordingly, campaign amendment v2 exception 1 mandates `CONCERNS / LEGIT`.

### Gate and verdict summary

- Gate A, real-program soundness: pass.
- Gate B, intent adequacy: pass for the material string domain and the
  candidate's defensible docstring reading; the supplied whitespace-model gap
  is explicit and non-fatal.
- Gate C, trust/evidence auditability: pass; all independent commands,
  positive results, negative residuals, source inventories, and finite test
  scopes are preserved under `/audit-output/evidence/`.

The proof is sound, result-constraining, unbounded over finite modeled strings,
and pins the real translated program. The sole material limitation is the
documented supplied-model whitespace identification gap, which maps to
concerns rather than failure under the campaign amendment.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
