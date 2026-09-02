# Independent adversarial audit — 17-parse-music

The reconstructed K commands do print `#Top`, but the candidate is not a
legitimate proof under the supplied semantics. The decisive defect is the
candidate-local priority rule for `str.split()`: it preempts the supplied split
rule, replaces the result with a proof-only iterator, and skips the supplied
semantics' heap allocation. The entry claim then proves an exact allocator
state that is false for fixed-semantics execution of the real program. The
candidate also provides no connection theorem or defining equations from its
opaque `musicCodes(M)` term to concrete input strings.

There was no audit-infrastructure breach. K v7.1.337 was available, the rendered
mode was `SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` was present
as required.

## 1. Input and provenance integrity

I treated every candidate artifact as untrusted evidence and did not execute
candidate-built definitions or caches.

The exact integrity procedure and transcript are
[`stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`stage1_integrity.log`](evidence/stage1_integrity.log). It checked paths with
`find -P`, compared types and link targets, compared file bytes, and separately
searched for symlinks.

- `/candidate/prompt.py` is a regular file byte-identical to
  `/reference/prompt.py` (`cmp` exit 0; both SHA-256
  `713553ae9220b08678d575238a702f883cc1d37b1986a6bfa010f8d641601d36`).
- `/candidate/py2mpy.py` is a regular file byte-identical to the trusted
  translator (`cmp` exit 0; both SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The candidate and trusted `reference-semantics/` trees have the same paths,
  entry types, and link targets (`diff` exit 0). Every one of the 24 K files is
  byte-identical, with no missing, additional, mistyped, changed, or symlinked
  entry. In particular, `semantics.k` has SHA-256
  `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`
  in both trees.
- The requested provenance artifacts `/candidate/run-input.json`,
  `/candidate/metrics.json`, `/candidate/codex-last.txt`, and
  `/candidate/codex-output.log` are all missing. No structured generation trace
  was present. This removes provenance evidence but did not prevent independent
  reconstruction.
- The candidate contains `/candidate/__pycache__/solution.cpython-310.pyc`.
  It was treated as an untrusted cache and ignored.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From `/reference/prompt.py` and `/reference/canonical.py`, the intended function
takes a space-delimited finite sequence of valid musical tokens and returns the
corresponding beat counts:

| token | result |
|---|---:|
| `o` | 4 |
| `o|` | 2 |
| `.|` | 1 |

The canonical implementation splits on the literal ASCII space, discards empty
parts, and dictionary-looks-up each token. The submitted implementation uses
`str.split()` and an `if`/`elif`/`else`; on the intended domain of valid tokens
with ASCII-space separators it implements the same mapping.

The trusted translator command was:

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

It exited 0. `cmp -s` against submitted `solution.mpy` exited 0, and both files
have SHA-256
`fd131af8a2ebf3749359fb81b36453db2da86229334451021cb9b4bbfb0a92f8`.
Commands and statuses are in
[`stage2_run.log`](evidence/stage2_run.log).

### Independent differential test

[`stage2_differential.py`](evidence/stage2_differential.py) independently loads
the trusted canonical entry point and generated entry point. Its complete
generated corpus is [`stage2_inputs.json`](evidence/stage2_inputs.json), and
machine-readable results are
[`stage2_results.json`](evidence/stage2_results.json).

The 1,217 distinct intended-domain cases include the documented example, empty
input, each individual token, every branch transition, leading/trailing and
repeated ASCII spaces, all note sequences of length 0 through 5 with one- and
two-space separators, and 500 deterministic generated sequences of length 0
through 50. The script exited 0 with zero mismatches.

Seven explicitly out-of-domain probes remain visible in the results. Tabs,
newlines, and invalid tokens differ: the canonical code raises `KeyError`, while
the generated code either splits the extra whitespace or maps an unknown token
to 1. These tests are finite evidence only. They support equivalence on the
documented valid space-delimited domain and do not prove it universally.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`, used the
trusted supplied-semantics tree (which Stage 1 proved byte-identical to the
candidate tree), and created all compiled definitions from scratch. No
candidate-provided compiled directory or cache was copied.

The exact commands and bounded outputs are in
[`stage3_reconstruction.sh`](evidence/stage3_reconstruction.sh) and
[`stage3_reconstruction.log`](evidence/stage3_reconstruction.log). Results:

| operation | result |
|---|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| `krun concrete-test.mpy --definition runtime-kompiled` | exit 0; final `<k> .K </k>` |
| `kompile verification.k --backend haskell --main-module PARSE-MUSIC-BASE --syntax-module MPY-SYNTAX --output-definition verification-base-kompiled` | exit 0 |
| `kprove spec.k --definition verification-base-kompiled --spec-module PARSE-MUSIC-LOOP-SPEC` | exit 0; `#Top` |
| `kompile verification.k --backend haskell --main-module PARSE-MUSIC-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| `kprove spec.k --definition verification-kompiled --spec-module PARSE-MUSIC-ENTRY-SPEC --branching-allowed 100` | exit 0; `#Top` |

The inventory found exactly two positive claims, so both targets were run. Fresh
compilation emitted several supplied-semantics totality warnings, accounted for
in Stage 5; none is on this program's path. Proof closure is therefore genuine
closure under the candidate-augmented theory, but it does not validate the
extensions in that theory.

## 4. Adequacy and real-program pinning

### Claim meanings

The loop claim at `/candidate/spec.k:9` says: for any finite abstract `Music`
sequence and any existing output prefix `A`, executing the exact submitted loop
from `musicIter(M)` consumes the loop, changes `beats` from `A` to
`musicAcc(A,M)`, and changes `note` from its prior value to
`musicLast(prior,M)`. It leaves the framed cells unchanged.

The entry claim at `/candidate/spec.k:32` says: from the exact clean initial
configuration, load the submitted program macro and call `parse_music` on
`str(musicCodes(M))`; execution ends with return value `ref(0)`, heap location
0 containing `musicAcc(.ValSeq,M)`, no other heap entries, `heapLoc = 1`, empty
stack, no pending return or exception, and exit code 0.

The macros `parseMusicLoopBody`, `parseMusicBody`, and `parseMusicProgram`
expand to the exact submitted `solution.mpy`, including the function body and
typing import. Thus the `<k>` cell names the submitted program rather than a
different handwritten algorithm.

Both preconditions are formally satisfiable. A fully instantiated loop state
for `M = whole(.Music)` and entry states for `M = .Music` and
`M = whole(.Music)` are recorded in
[`stage4_claim_witnesses.md`](evidence/stage4_claim_witnesses.md). Under the
candidate's intended informal encoding, the corresponding concrete inputs are
`""` and `"o"`; both Python implementations return `[]` and `[4]`.

### Real-program failure

The formal input term is not pinned to those strings. `musicCodes` is an opaque
new `IntSeq` constructor with no equations. More decisively, even granting the
intended encoding, the proof-only split bridge changes the fixed semantics'
state:

```k
rule <k> #applyK(toCall(boundMethodV(str(musicCodes(M:Music)), "split")), .Vals)
      => musicIter(M) ... </k>
     [priority(35)]
```

The supplied split rule at `semantics/methods.k:72` performs
`#alloc(list(splitWS(...)))`. The candidate rule preempts it and performs no
allocation.

[`ground-o.mpy`](evidence/ground-o.mpy) executes the exact translated function
on the valid input `"o"` under fixed concrete semantics. The command and full
configuration are in
[`stage4_bridge_witness.log`](evidence/stage4_bridge_witness.log). Python gives
`[4]` in both implementations, while fixed K execution ends with:

```text
heap 0 |-> list(vCons(4, .ValSeq))
     1 |-> list(vCons(str(iCons(111, .IntSeq)), .ValSeq))
heapLoc = 2
```

The entry claim instead proves the exact heap containing only location 0 and
`heapLoc = 1`. This is a concrete false full-configuration conclusion on a
satisfying intended input, enabled by the bridge.

As an independent dependency check, I removed only that bridge in
[`verification-no-split-bridge.k`](evidence/verification-no-split-bridge.k).
The modified definition compiled successfully (exit 0), but the entry proof
exited 1 with `WarnStuckClaimState` at
`splitWS(musicCodes(M),.IntSeq,.ValSeq)`. Its residual already has the split
list at heap location 1 and `heapLoc = 2`. This is an expected proof failure,
not a parser, import, timeout, or infrastructure error.

The proof therefore executes the program's outer syntax but substitutes a
property-bearing operation with a state-changing oracle. It does not pin fixed
execution of the real translated program.

## 5. Rule-by-rule static soundness review

The exhaustive, source-located inventory is
[`stage5_rule_inventory.tsv`](evidence/stage5_rule_inventory.tsv), generated by
[`stage5_inventory.py`](evidence/stage5_inventory.py); its logged summary is
[`stage5_inventory.log`](evidence/stage5_inventory.log). Every one of its 957
rows has a reachability scope and review disposition.

The inventory contains 928 supplied-semantics entries and all 29
candidate-local declarations, rules, and claims. It enumerates one
configuration, five contexts, 80 ordinary syntax declarations, 122
function-syntax entries, 25 opaque function-syntax entries, one candidate
opaque syntax entry, eight macros, 624 ordinary rules, 32 concrete rules, 26
`owise` rules, 31 priority rules, and two claims. There are 157 occurrences of
`function`, 117 of `total`, and no local `[functional]` or simplification
declaration. `semantics.k` itself only assembles modules; operational entries
are in its helper files.

The detailed disposition of each of the 29 candidate entries and the
supplied-semantics used-path mapping is
[`stage5_candidate_assessment.md`](evidence/stage5_candidate_assessment.md).
The submitted constructs map as follows:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `ImportFrom`, statement sequence | `syntax.k`; `core.k:123-127`; non-math import no-op in `controls.k:33-44` |
| `FuncDef`, call, parameter, return | `functions.k:14-16,63-90`; `call.k:15-24,69-74` |
| `Assign`, `Name`, `ListExpr`, string/int literals | `controls.k:9-18`; `core.k:117-121,130-154,193-196`; `list.k:12-20`; `str.k:13-17` |
| `Attribute(...,"split")`, zero-argument call | `call.k:15-24`; fixed split in `methods.k:70-86` |
| `For` and iterator protocol | `controls.k:62-74`; protocol declaration in `iter.k`; target binding in `tuple.k:30-41` |
| string `==` and `If` | `operators.k:14-17`; `str.k:24-26`; `controls.k:50-54` |
| `beats.append` | mutating-method routing in `call.k:52-67`; heap update in `list.k:52-55` |

Candidate-local findings:

- `musicAcc` and `musicLast` are constructor-complete total functions with
  disjoint equations and structural descent. Their equations correctly map
  whole/half/quarter to 4/2/1 and correctly track the last note.
- The four iterator rules truthfully yield `"o"`, `"o|"`, and `".|"` from
  their corresponding `Music` constructors.
- The four program-fragment macros match submitted `solution.mpy`.
- The loop-summary rule is supported by the separately reconstructed exact loop
  claim. However, the rule frames an arbitrary continuation while the proved
  claim's `<k>` cell is exact. No bridge-free universal context theorem is
  supplied. Because the exact loop body has no abrupt control and I found no
  false continuation witness, I record this as a context-justification gap,
  not as an additional unsoundness finding.
- `musicCodes` is an unconnected result-bearing opaque constructor.
- The priority-35 split rule is an operational bridge with no connection
  theorem. Its complete state footprint differs from fixed semantics: it reads
  the same receiver but omits the split-list heap write and allocator
  increment. The `"o"` witness above proves that it enables a false conclusion;
  it is materially unsound for this entry claim.

All 24 supplied K files are the selected trusted baseline. The used rules
preserve the relevant binding, left-to-right evaluation, branch control,
function stack, heap writes, and allocation. The supplied opaque float,
keyed-sort, MD5, and related symbols are absent from this program and its proof
helpers. Compiler non-exhaustiveness warnings concern `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none is reachable here. I found no
used-path false witness against the supplied baseline.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity file. The fresh mutation
[`spec-vacuity.k`](evidence/spec-vacuity.k) changes the entry's
result-constraining heap obligation to require the returned list to begin with
99:

```k
.Map => 0 |-> list(vCons(99, musicAcc(.ValSeq, M)))
```

`M = .Music` is a satisfying witness for the original precondition. The
corresponding concrete empty input returns `[]` in both Python implementations,
so the mutation is demonstrably false.

Commands and output are in
[`stage6_nonvacuity.sh`](evidence/stage6_nonvacuity.sh) and
[`stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log):

- Both Python witness checks exited 0.
- `kprove ... --dry-run` exited 0 and emitted KORE, proving the mutation parsed
  and built successfully.
- Actual `kprove` exited 1 with `WarnStuckClaimState`. The residual reaches the
  original final configuration and fails the expected implication because
  `musicAcc(.ValSeq,M)` cannot equal
  `vCons(99,musicAcc(.ValSeq,M))`.

The candidate proof is therefore result-constraining and non-vacuous under its
augmented theory. This successful discrimination does not repair the unsound
operational bridge used to reach that result.

## 7. Proven versus assumed accounting

What `#Top` precisely establishes is conditional on the candidate-augmented
theory: for abstract `M:Music`, calling the exact program macro on the abstract
value `str(musicCodes(M))`, after replacing its `split()` operation by
`musicIter(M)` and its loop by the proven summary, reaches `ref(0)` with output
sequence `musicAcc(.ValSeq,M)` and the candidate's one-allocation final state.
The auxiliary proof separately establishes the abstract iterator loop's output
and final note binding.

Trust and assumption ledger:

| Boundary | Effect | Assessment |
|---|---|---|
| K v7.1.337, Haskell/LLVM backends, K integer/string/map/list primitives | Parsing, execution, and reachability checking | Necessary low-level trusted base; commands reconstructed successfully. |
| Supplied reference semantics | Python-subset execution model | Required selected semantics; integrity passed. Used path reviewed. |
| Trusted `py2mpy.py` | Python-to-`.mpy` syntax bridge | Acceptable here because byte-identity regeneration passed. |
| `musicAcc`, `musicLast`, iterator equations | Expected values for abstract `Music` | Truthful, exhaustive, descending definitions. |
| Independently proved loop claim | Abstract loop execution summary | Machine-checked for exact `<k>`; rule reuse has the documented continuation-scope gap. |
| `musicCodes(M)` | Concrete input-string representation | Illegitimate/unproved: no equations or bridge-free theorem relate it to concrete ASCII codes. |
| Candidate split rewrite | Converts abstract input to iterator and skips fixed split | Illegitimate: result-bearing operational bridge, no connection theorem, and concrete false allocator-state witness. Both entry result and exact final-state proof depend on it. |
| Supplied opaque float/sort/MD5 functions | Potential external operations | Irrelevant; none can influence these claims. |
| Differential testing | Natural-language/canonical bridge on 1,217 cases | Finite supporting evidence only; not a K proof or universal theorem. |
| Valid-token, ASCII-space domain | Excludes invalid tokens and non-space whitespace | Matches canonical behavior tested here; generated behavior is broader outside it. |

The candidate thus has a non-vacuous proof in a materially altered semantics,
not a partial-correctness proof of the real generated program under the supplied
semantics. The fixed-semantics allocator counterexample and the bridge-removed
stuck proof satisfy the required false-conclusion and dependency checks. This
falls squarely under “materially unsound semantics or proof rules” and
“substituted program behavior,” requiring `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
