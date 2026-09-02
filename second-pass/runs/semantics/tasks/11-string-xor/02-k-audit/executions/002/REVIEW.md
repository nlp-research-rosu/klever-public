# Independent adversarial review: 11-string-xor

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full source-contract domain. I reconstructed the definitions
from source, reran the target claims, mechanically pinned the theorem term to
the trusted translator output, exhaustively inventoried the K theory, changed
the executed body, and rejected a fresh false postcondition.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. This is coherent with the mounts:
`/reference/reference-semantics` is present and is a non-symlink directory.
The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json`, whose independently computed SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

All records required for `legacy-selected-stage1` are present, readable,
regular non-symlink files:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace below `/generation-evidence/codex-trace`.

`usage.json` is present and was also inspected. Historical runtime metrics are
not required for this record layout. The independently calculated hashes of
the campaign lock, run/task/result/invocation manifests, metrics, usage,
generation prompt/output/last message, trusted prompt, translator, and
canonical source all equal the launcher-recorded hashes. The one trace file
has the generation-result-recorded hash
`055ec471894dcb15496d7630a56efd2a051693fb99d9928e3c1e094fb4403c83`;
all 265 JSONL records parse. The trace contains 49 recorded execution calls,
one wait call, and the expected construction history. These generation
success reports remain untrusted claims and were not used as proof.

The candidate mount contains no symlink or special-file entries. The candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts.
Recursively comparing the submitted and trusted supplied-semantics trees gives
the same 25 relative entries, types, and file bytes, with no missing,
additional, renamed, or changed entry. An independent canonical JSON tree
manifest also gives the same digest for both semantics trees. The launcher's
tree-hash field uses a different manifest serialization; the audit records the
independent manifest digest rather than equating unlike hash namespaces.

Evidence:
[integrity script](/audit-output/evidence/stage1_integrity.py),
[integrity log](/audit-output/evidence/stage1_integrity.log), and
[bounded trace summary](/audit-output/evidence/generation_trace_summary.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `string_xor(a: str, b: str) -> str`: both inputs
contain only `0` and `1`, and the result is the pointwise binary XOR string.
The trusted canonical implementation applies a four-case equality/XOR helper
over Python `zip(a,b)`, so unequal inputs truncate to the shorter length. Empty
binary strings are therefore supported.

The candidate implements the same algorithm iteratively: it initializes an
empty result, iterates through `zip(a,b)`, appends `"0"` when the characters
are equal and `"1"` otherwise, and returns the accumulator. It neither fixes
the length nor strengthens the input contract.

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced SHA-256
`6dc4a5199d3c6f87b07ef8a7a901fad25e3105d323aa76e079880a67ce6be154`,
byte-identical to submitted `solution.mpy`.

The independent differential test imports both the trusted canonical entry
point and candidate entry point and also uses a separately written four-row
XOR table. It checks the documented example, both/one-sided empty cases, all
four branch pairs, both unequal-length directions, every pair of binary
strings whose individual length is at most six (16,129 pairs), and 2,000
deterministically generated pairs up to length 256. All 18,141 cases agree;
there are zero mismatches.

Evidence:
[differential script](/audit-output/evidence/differential_test.py) and
[translation/differential log](/audit-output/evidence/stage2_fidelity.log).

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/11-string-xor` and used new
output-definition names after confirming they did not exist. No
candidate-provided K definition or cache was reused. K reports version
7.1.293, matching the campaign record.

Fresh reconstruction performed:

1. LLVM compilation of supplied `semantics.k` with main module `MPY-KRUN` and
   syntax module `MPY-SYNTAX`: exit 0.
2. `krun concrete_tests.mpy` against that definition: exit 0, final `.K`,
   `NoExc`, and exit code 0.
3. Haskell compilation of `verification.k` with main module
   `STRING-XOR-VERIFICATION`: exit 0.
4. `loop-invariant` selected alone: `#Top`, exit 0.
5. the complete target set, selecting `loop-invariant` and
   `solution-correct`: `#Top`, exit 0.

The end-to-end claim intentionally uses the loop claim as its circularity, so
the valid target command includes both. A diagnostic that filtered the helper
claim out was interrupted and is not counted as a positive target run; it is
preserved in `stage3_reconstruction.log`. The clean completed run separately
proves the auxiliary and then proves the complete selected target set.

The compiler's LLVM warnings concern incomplete totalizations of operations
not reached by this program (`mapStrVS`, several float helpers, `joinCodes`,
and `valSeqAt`). They are addressed in Stage 5 and do not replace or weaken
the successful target runs.

Evidence:
[reconstruction script](/audit-output/evidence/stage3_reconstruction.sh) and
[completed reconstruction log](/audit-output/evidence/stage3_reconstruction_complete.log).

## 4. Adequacy and real-program pinning

### Entry-claim meanings

`loop-invariant` starts at the actual internal `#loop` for a string
`zipObjS(A,B)`, with the exact translated tuple target and exact translated
conditional body followed by an arbitrary continuation `CONT`. The current
scope contains original arguments, current result prefix, and current `x/y`.
The remaining code sequences are binary. It proves that the loop consumes the
shorter remaining suffix, appends the corresponding XOR codes, leaves `x/y`
at their last paired one-character strings (or their prior values when no pair
exists), preserves the arguments/parent/other scopes, and continues with
`CONT`.

`solution-correct` starts from a realizable initial configuration with empty
module scope, supplied builtins, empty heap/stack, and no return or exception.
For arbitrary finite binary code sequences `A` and `B`, it loads the submitted
module and calls the selected `"string_xor"` binding. It requires the returned
value to be exactly `str(xorAcc(.IntSeq,A,B))` and fixes the final module scope.
The return is not a fresh variable, existential, tautology, or one-way
implication.

### Mechanical program identity

The audit generated a reachability claim whose destination constructor term
was read directly from the trusted-regenerated `solution.mpy`. Under the fresh
candidate definition, `stringXorModule` equals that exact term and the claim
prints `#Top`. This includes the typing import, function binding, parameters,
docstring, assignments, `zip` loop, both branches, and return.

A separate body-sensitivity mutation changed the executed equal-bit branch
from appending `"0"` to appending `"1"` inside `stringXorLoopBody`. Because
`stringXorBody` and `stringXorModule` expand through that alias, this changes
the program term actually executed by the entry claim. The original
constructor-pinning claim then fails with `WarnStuckClaimState`, visibly
showing the mutated `"1"` constructor; the positive proof also fails on the
expected disagreement between output prefixes. Thus the proof is sensitive
to the real body, not merely an external source file.

### Satisfiable witnesses and concrete substitution

For `A = "010"` and `B = "110"` (code sequences
`48,49,48` and `49,49,48`), both binary predicates reduce to true.
The explicit loop entry state with environment 1, a disjoint singleton scope,
empty result, and empty initial `x/y` is realizable. A ground K execution
reaches result codes `49,48,48` (`"100"`) and final `x = y = "0"`.
The ground end-to-end initial configuration reaches the same `"100"`.
Trusted canonical Python, candidate Python, the independent XOR oracle, and
the formal `xorAcc` substitution all agree.

Evidence:
[pinning generator](/audit-output/evidence/generate_pinning_spec.py),
[adequacy witnesses](/audit-output/evidence/adequacy-ground.k),
[adequacy log](/audit-output/evidence/stage4_adequacy_complete.log),
[body mutation](/audit-output/evidence/body-mutation-verification.k), and
[body-sensitivity log](/audit-output/evidence/body_sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers the supplied assembly file, all 23 supplied
helper K files, candidate `verification.k`, and `spec.k`: 959 records
comprising 237 syntax declarations, one configuration, five contexts, 714
rules, and two claims. It enumerates every local function/total declaration,
opaque symbol, priority, concrete rule, ordinary rule, and claim. There are no
simplification or functional declarations. A one-row-per-ID ledger gives a
decision and justification for all 959 records.

Evidence:
[full inventory](/audit-output/evidence/rule_inventory.md),
[per-record decisions](/audit-output/evidence/rule_decisions.tsv), and
[static-review narrative and construct map](/audit-output/evidence/rule_review.md).

The material constructor/rule chain is:

- module loading and statement sequencing in `core.k`;
- the typing-only import no-op, assignments, expression discard, if, and for
  in `controls.k`;
- definition/call/parameter/return/frame rules in `functions.k` and `call.k`;
- lookup and left-to-right argument evaluation in `core.k`;
- `zip(str,str)` and its three disjoint iterator cases in `builtins.k`;
- tuple target unpacking in `tuple.k`;
- ordered operator dispatch in `operators.k`;
- exact string literal, equality, and concatenation equations in `str.k`.

Each material operation executes; no fixed rule skips the loop or fabricates
its result. The relevant priority rules are disjoint heap/cell cases and
cannot match this plain string/function frame. Configuration cells, call
continuation, scope allocation/deallocation, arguments, and return control are
preserved exactly.

Candidate `verification.k` adds only definitional mathematical helpers and
constructor aliases:

- `binaryCode` is exactly membership in ASCII `{48,49}`;
- the two guarded `xorCode` equations are disjoint and, on binary codes,
  exhaustive;
- `xorAcc` structurally recurses over paired suffixes and has disjoint
  shorter-input base cases;
- `binaryCodes` and `xorLastX/Y` are truthful structurally recursive
  definitions;
- the target/body/closure/module equations are exact aliases, not operational
  bridges.

The loop claim itself is the universal fixed-semantics connection theorem over
the exact target, body, scope, binary suffix domain, and arbitrary continuation
that the end-to-end claim needs. It introduces no abrupt effect and frames
only cells the concrete loop does not touch.

The supplied semantics has named opaque float, MD5, and sort primitives, but
none occurs in `solution.mpy`, a proof helper, a claim, or any dependent
execution. The compiler-reported incomplete totalizations are similarly
confined to unused operation-specific sublanguages. These are explicit
fixed-semantics coverage/trust boundaries, not proof-local oracles and not a
route to any XOR conclusion. The used typing import is materially inert: while
real CPython would bind `List`, the submitted function never reads it and
module-namespace fidelity is not the HumanEval result property.

No candidate rule has overlapping guards with conflicting right-hand sides,
non-descending recursion, false mathematics, task-answer encoding in an
operational rule, or unconstrained result-bearing abstraction. I therefore
found no unsound candidate rule and do not assert an unsoundness without a
false-conclusion witness.

## 6. Fresh non-vacuity test

The fresh mutation preserves the genuine loop claim but changes the
end-to-end destination by appending an extra ASCII `"0"` to every required
result. It is demonstrably false on the satisfying witness `A = B = ""`:
canonical and candidate Python both return `""`, whereas the mutation requires
`"0"`.

`kprove --dry-run` on the mutated module exits 0, establishing that the
mutation parses and builds. The actual proof exits 1 with
`WarnStuckClaimState`. Its residual is the expected unmet result equality:

`seqConcat(xorAcc(.IntSeq,A,B), iCons(48,.IntSeq))`
does not equal `xorAcc(.IntSeq,A,B)`.

This is a reachable result obligation, not a parser failure, missing import,
timeout, or unrelated crash.

Evidence:
[false mutation](/audit-output/evidence/spec-vacuity.k),
[ground witness](/audit-output/evidence/nonvacuity_witness.py), and
[build/proof log](/audit-output/evidence/stage6_nonvacuity.log).

## 7. Proven versus assumed accounting

The successful reachability proof establishes, under the supplied MPY
semantics, that for every pair of finite strings whose codes are all ASCII
`0`/`1`, terminating execution of the exact submitted module's
`string_xor(a,b)` returns a string of length `min(len(a),len(b))` whose code at
each paired position is `0` exactly when the two input bits agree and `1`
otherwise. It also establishes the claimed module scope and unchanged
heap/control cells. This covers empty inputs, unequal lengths, both branch
directions, and unbounded finite lengths; it is not a fixed-size unrolling.

The trust ledger is:

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K parser/compiler, Haskell reachability backend, LLVM concrete backend, and K built-in Int/Bool/String/Map/List theories | Proof checking and primitive mathematics | Standard machine-checked trust boundary; campaign and live version are both 7.1.293. |
| Trusted supplied MPY semantics | Program execution model | Required fixed semantics; candidate tree is byte-identical. Every material rule path was statically audited and freshly executed/proved. |
| Trusted `py2mpy.py` | Python-source to constructor bridge | Trusted benchmark input; fresh output is byte-identical to submitted `solution.mpy`. Constructor pinning connects that output to the theorem term. |
| ASCII codes 48/49 and the four-row XOR interpretation | Human-facing contract bridge | Encoded explicitly by guarded equations; checked on ground K witnesses and an independent Python truth table. |
| Typing-only import as a no-op | Final module namespace, not return value | Real binding is omitted by the supplied subset, but `List` is never read; no material result/control/state dependency. |
| Opaque float/MD5/sort symbols and unused incomplete totalizations | None | No occurrence or dependent on the submitted execution/proof path; not assumptions of this theorem. |
| Python differential evidence | Source/canonical adequacy only | 18,141 finite cases with zero mismatches; not used as a substitute for the universal K proof. |

The generation report, prior `#Top`, candidate smoke tests, and generated prose
were not accepted as proof. The verdict rests on clean reconstruction,
constructor-level identity, complete static review, body sensitivity, and the
fresh rejected false result.

VERDICT: PASS
LEGITIMACY: LEGIT
