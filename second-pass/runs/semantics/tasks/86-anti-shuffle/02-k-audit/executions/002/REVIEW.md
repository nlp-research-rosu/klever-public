# Independent adversarial audit: 86-anti-shuffle

The candidate does not contain a legitimate partial-correctness proof of the
real generated program. Fresh reconstruction reproduces all three advertised
`#Top` results, the submitted Python program is extensionally faithful to the
trusted canonical implementation on substantial finite evidence, and the main
claim is syntactically pinned to the translated body. However, the end-to-end
proof closes through three proof-local operational rules that do not preserve
fixed-semantics execution. Most decisively, a mutation of the program term
actually executed by the claim changes the concrete result but the old
universal theorem still proves `#Top`.

This is a candidate proof defect, not an infrastructure failure.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `86-anti-shuffle`;
- generation condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `record_layout: legacy-selected-stage1`;
- complete provenance.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all records required for this
layout:

- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json` (present and inspected);
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the sole 526-record JSONL trace below
  `/generation-evidence/codex-trace/`.

Historical runtime metrics are not required for this legacy-selected layout
and were not reconstructed. The trace parsed with zero malformed records. Its
generation claims, including three prior `#Top` reports, were not trusted.
The exact trace parsing summary and the 66 proof-relevant generation tool calls
are in `evidence/stage1-trace-summary.log`.

### Independent hashes and types

`evidence/stage1-integrity.log` records the independent checks and exits 0:

- the campaign-lock hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
  and its parsed JSON equals the `audit_campaign` block exactly;
- all launcher-declared hashes for the run, task, result, invocation, metrics,
  usage, prompt, output log, last message, trace file, canonical, trusted
  prompt, and translator match;
- the launcher-enriched task manifest core is consistent with `/task.json`;
- the complete candidate mount has 39 ordinary file/directory entries and no
  symlink or special entry;
- all five required proof artifacts are ordinary files. Their independent
  SHA-256 values are recorded in that log.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The trusted
`/reference/reference-semantics` exists as required for supplied mode.
Recursive path/type/content comparison found exactly 24 files, one nested
directory, no additional or missing entry, no symlink, and byte identity
between `/candidate/reference-semantics` and the trusted tree.

Candidate-provided `prove.log`, `kore-exec.tar.gz`, bytecode, and any implied
compiled state were ignored. There is no missing launcher record, malformed
mount, semantics-mode contradiction, or other infrastructure breach.

Stage 1 result: **integrity gate passes**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires `anti_shuffle(s)` to:

1. treat the input as a string split on the literal space character;
2. preserve word order and every blank-space position;
3. replace each word by its characters in ascending character/ASCII order.

The trusted canonical implementation is:

```python
return ' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
```

The candidate uses an equivalent explicit loop: start with an empty result,
iterate over `s.split(" ")`, append the sorted word and one space, and remove
the one deliberately added final space. Initializing `word = ""` before the
loop is harmless. The empty string still creates one empty split field, so the
final slice is well defined and returns empty. Leading, trailing, and repeated
spaces are preserved.

### Trusted regeneration

Only trusted inputs were copied to `/tmp/audit-work/86-anti-shuffle`. The exact
regeneration was:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
```

Both commands exited 0
(`evidence/stage2-translate.log`,
`evidence/stage2-translation-identity.log`). Thus the submitted
`solution.mpy` is byte-identical to translation by the trusted translator.

### Independent differential test

`evidence/stage2_differential.py` independently imports the copied trusted
canonical and generated modules. Its inputs are specified reproducibly in
`evidence/stage2-differential-inputs.json`:

- all three documented examples;
- 23 named empty, one/multiple-space, leading/trailing-space, ordering,
  punctuation, tab/newline, NUL, combining-character, Unicode, and astral
  boundaries;
- every string of length 0 through 5 over an eight-character alphabet
  containing NUL, literal space, tab, ASCII, accented, and astral characters;
- 1,000 seeded random strings of length 0 through 60.

The exact run exited 0 with 38,475 cases, ordered input hash
`939201d4aea7556246beb9c1b5754cba6213bf7867e5f992c4c3e9a7538e0a92`,
and zero mismatches (`evidence/stage2-differential.log`). This finite evidence
supports implementation fidelity; it is not used as a universal K proof.

Stage 2 result: **the generated Python program faithfully implements the
source contract**.

## 3. Clean proof reconstruction

All builds used the source-only scratch copy. No candidate-provided definition,
cache, binary, archive, or proof log was copied. The installed independent
toolchain reports K v7.1.293.

### Concrete definition

The concrete test translation was independently regenerated and compared
byte-for-byte. Then:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun regenerated-concrete-tests.mpy \
  --definition runtime-kompiled --output none
```

Both commands exited 0. See `evidence/stage3-kompile-llvm.log` and
`evidence/stage3-krun-concrete.log`.

### Every positive proof target

The candidate's `prove.sh` identifies three positive targets. Each definition
was separately rebuilt, and each proof was run independently:

| Target | Fresh commands | Result |
|---|---|---|
| Word result | `kompile verification.k --backend haskell --main-module ANTI-SHUFFLE-BASE --syntax-module MPY-SYNTAX --output-definition word-verification-kompiled`; `kprove spec.k --definition word-verification-kompiled --spec-module WORD-SPEC` | build 0; proof 0 and `#Top` |
| Loop invariant | `kompile verification.k --backend haskell --main-module ANTI-SHUFFLE-LOOP-VERIFICATION --syntax-module MPY-SYNTAX --output-definition loop-verification-kompiled`; `kprove spec.k --definition loop-verification-kompiled --spec-module ANTI-LOOP-SPEC` | build 0; proof 0 and `#Top` |
| End-to-end | `kompile verification.k --backend haskell --main-module ANTI-SHUFFLE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled`; `kprove spec.k --definition verification-kompiled --spec-module ANTI-SHUFFLE-SPEC` | build 0; proof 0 and `#Top` |

Exact bounded outputs are in the six
`evidence/stage3-kompile-{word,loop,full}.log` and
`evidence/stage3-kprove-{word,loop,full}.log` files. Warnings concern unused
variables and fixed-semantics exhaustiveness; no build or proof failed.

Stage 3 result: **the advertised verification results reproduce**, but only
under the candidate-extended theory. This is not yet a soundness finding.

## 4. Adequacy and real-program pinning

### Claims in plain language

`WORD-SPEC.sort-word-summary` says: for any code sequence `W`, from a module
scope containing only the fixed builtins and with two fresh heap locations,
execute the actual nested `list(W)`, `sorted`, and empty-separator `join`
expression; the returned value is `sortWord(W)`. Final heap and allocator are
existential.

`ANTI-LOOP-SPEC.anti-loop` says: for any typed remaining `Words`, result prefix
`A`, and exact local/global/builtin scope chain, execute the custom-iterator
loop and then read `result`; the read value is `A` concatenated with
`emitWordSeq(WS)`. Final scopes, heap, and allocator are existential.

`ANTI-SHUFFLE-SPEC.anti-shuffle-correct` says: from the empty initial
module/heap configuration, for every symbolic `IntSeq` input `S`, directly
call a closure with parameter `s` and body `antiBody`; its returned value is
exactly `antiShuffleSpec(S)`.

The entry domain is unrestricted symbolic `IntSeq`, not finitely many sizes or
examples. It therefore does not materially narrow the source string domain.
The postcondition constrains the actual return value and is not a free
variable, tautology, or one-way implication.

### Constructor-level identity

The main claim directly constructs the closure rather than loading the full
module and looking up `anti_shuffle`. This omits only the inert intermediate
binding step: the claim fixes the same parameter list, definition environment
0, and body. `evidence/stage4_pinning.py` independently extracts and tokenizes
the trusted regenerated function body, expands both K macros, and compares the
constructor sequences. It reports:

```text
FUNCTION_BODY_TOKEN_EQUAL=True
LOOP_BODY_TOKEN_EQUAL=True
EXACT_CLOSURE_LITERAL_COUNT=1
PINNING_FAILURES=0
```

Thus the entry term syntactically pins the submitted function body.

### Satisfiable states and concrete substitution

Every claim precondition is satisfiable:

- word claim: `W = "ba"`, empty heap, `N = 0`;
- loop claim: one remaining word `"ba"`, empty prefix/input-compatible local
  frame, empty heap, `N = 0`;
- entry claim: `S = "ba a"` in the exact empty initial configuration.

The independent Python implementations both return `"ab a"` for the entry
witness. `evidence/stage4-ground-spec.k` substitutes the corresponding code
sequence into the exact claimed closure and result; its proof exits 0 with
`#Top` (`evidence/stage4-ground-proof.log`).

### Body sensitivity: fatal failure

The executed K program body was then materially changed from:

```text
AugAssign(Name("result"), "+", Str(" "))
```

to:

```text
AugAssign(Name("result"), "+", Str("!"))
```

This was not a source-only mutation: the modified macro occurs inside the
closure body actually executed by the claim. Mechanical comparison against the
trusted translation of the corresponding mutated Python again reports exact
function and loop body identity
(`evidence/stage4-body-mutation-pinning.log`). Trusted concrete semantics
executes the mutated program successfully and confirms:

```python
anti_shuffle("ba a") == "ab!a"
```

(`evidence/stage4-body-mutation.py`,
`evidence/stage4-body-mutation.mpy`,
`evidence/stage4-krun-body-mutation.log`).

Nevertheless, the candidate end-to-end postcondition was left unchanged,
still specifying the original space result. The mutated full definition built
successfully, and:

```text
kprove stage4-body-mutation-spec.k \
  --definition body-mutation-kompiled \
  --spec-module ANTI-SHUFFLE-SPEC
```

exited 0 with `#Top`
(`evidence/stage4-kompile-body-mutation.log`,
`evidence/stage4-kprove-body-mutation.log`). The loop summary changes its LHS
along with the macro but continues to assert the old result on its RHS. This
proves that exact syntactic pinning does not make the theorem depend on fixed
execution of the body.

Stage 4 result: **real-program execution pinning fails materially**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5_inventory.py` inventories every module/import, configuration,
syntax declaration, context, rule, guard, attribute, claim, priority,
simplification, and opaque declaration in all 24 fixed K files plus
`verification.k` and `spec.k`. The complete output
`evidence/stage5-rule-inventory.log` contains:

- 26 K files and 1,255 declaration records;
- 713 rules: 695 fixed and 18 proof-local;
- 236 syntax records;
- 112 `total` occurrences;
- 48 priority occurrences;
- 22 fixed opaque `no-evaluators` declarations;
- two proof-local simplifications;
- three claims.

The constructor-to-rule map and a decision for every proof-local syntax
declaration and all 18 proof-local rules are in
`evidence/stage5-static-review.md`. The material fixed execution slice covers
module/call frames, lookup and builtin shadowing, strict left-to-right
evaluation, assignment, allocation, split/list/sorted/join, iteration and
target binding, return/pop, and slicing. Fixed rules outside this
constructor-reachable slice cannot contribute to these claims. The fixed
files are the immutable selected semantics; their general Python-subset
limitations are not candidate-authored extensions.

The pure local macros and equations are sound:

- `antiBody` and `antiLoopBody` are exact macros;
- `sortWord`, `wordVals`, `splitWords`, `emitWordSeq`, and
  `antiShuffleSpec` are guarded, structurally recursive definitions;
- the `splitWords` separator/non-separator guards are exhaustive and disjoint;
- `wordsObj` iteration is a coherent typed sequence iterator;
- the two `seqConcat` simplifications are ordinary right identity and
  associativity, agree on overlaps, and orient toward smaller/right-associated
  terms.

Three local priority rules are operational bridges and are unsound.

### Unsound split bridge: `verification.k:98-105`

The bridge rewrites the fixed split dispatch directly to `wordsObj`:

```text
#applyK(toCall(boundMethodV(str(S), "split")), ("sep", .Vals))
  => wordsObj(splitWords(...))
```

Its complete match admits any continuation and omits `<heap>` and
`<heapLoc>`. Fixed `methods.k:94-96` instead allocates a list and returns its
fresh reference. Priority 35 preempts that fixed priority-40 rule. There is no
bridge-free universal connection theorem. In particular, a value-only
iteration argument cannot justify the changed allocation and result
representation in every admitted continuation.

False-conclusion witness on the intended string domain: for the identical
ground split redex on `"a b"` from an empty heap, fixed semantics proves return
`ref(0)`, heap location 0 containing `["a","b"]`, and allocator 1
(`evidence/stage5-split-fixed.log`, `#Top`). The bridge-enabled definition
proves return `wordsObj(["a","b"])` with the heap still empty and allocator
still 0 (`evidence/stage5-split-extended.log`, `#Top`). The two transitions
cannot both describe fixed execution.

### Unsound word bridge: `verification.k:109-120`

This rule replaces the entire unevaluated
`"".join(sorted(list(word)))` syntax by `str(sortWord(W))`. It preempts:

- lookup of `word`, `list`, and `sorted`;
- callee and argument evaluation;
- `list(word)` allocation;
- `sorted(...)` allocation;
- their potential binding/control failures;
- all heap and allocator effects.

Its only guard checks the current `word` map entry. Its arbitrary scope,
continuation, heap, allocator, and builtin-binding domain is much broader than
`WORD-SPEC`, whose environment is specifically an empty module plus builtins,
whose expression receives a literal `str(W)` instead of `Name("word")`, and
whose final heap is existential. That narrow value theorem is not a complete
state/context connection theorem.

False-conclusion witness using the real builtin environment and word `"ba"`:
fixed semantics proves the expected string and also proves allocations at
locations 0 and 1 with final allocator 2
(`evidence/stage5-word-fixed.log`, `#Top`). The bridge proves the same returned
string while falsely retaining an empty heap and allocator 0
(`evidence/stage5-word-extended.log`, `#Top`).

### Unsound loop bridge: `verification.k:128-143`

This rule erases:

```text
#loop(wordsObj(WS), Name("word"), antiLoopBody)
```

and updates only `result`. Its match accepts an arbitrary K continuation and
does not update the iteration target `word`, execute per-iteration allocations,
or preserve the full fixed state transition. The cited `ANTI-LOOP-SPEC` is not
a universal bridge theorem: it has the exact suffix `~> Name("result")` and
existential final scopes, heap, and allocator. It cannot justify a state
rewrite for every suffix.

False-conclusion continuation witness: for a one-word `"ba"` loop followed by
`Name("word")`, execution without the final summary binds `word` and returns
`"ba"` (`evidence/stage5-loop-fixed.log`, `#Top`). The full bridge-enabled
definition accepts the same suffix, skips target binding, and returns the
stale empty string (`evidence/stage5-loop-extended.log`, `#Top`). The body
sensitivity result in Stage 4 separately shows a false final return, not merely
an unobserved allocation difference.

These are concrete false state/result conclusions, not unsupported suspicions.
They occur with valid string inputs and real program-compatible environments.

### Opaque/trusted declarations

All 22 fixed opaque symbols are inventoried. Only `sortVS(ValSeq)` is reachable
from this program. It is explicitly the supplied semantics' trusted primitive
for ascending sort, is intentionally outside the program-defined code, and
affects every returned word and the postcondition. Treating it conditionally
as the selected semantics' `sorted` operation is an acceptable fixed trust
boundary here; the differential suite supplies finite support for the intended
Python bridge but is not a universal connection theorem. The remaining 21
opaque float, keyed-sort, and MD5 symbols are unreachable.

Stage 5 result: **Gate A / real-program soundness fails** because all three
operational bridges lack the required complete connection and enable witnessed
false conclusions.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created the independent
`evidence/stage6-false-spec.k`, using the satisfying input `"ba a"` but
mutating the expected return from the true `"ab a"` to the false `"ab b"`.
This changes the result-constraining obligation directly.

The dry-run command:

```text
kprove stage6-false-spec.k --definition verification-kompiled \
  --spec-module STAGE6-FALSE-SPEC --dry-run
```

exited 0 and emitted the valid `kore-exec` invocation
(`evidence/stage6-false-dry-run.log`), so this is not a parse/import/build
failure. The real proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual contains the actual:

```text
str(iCons(97, iCons(98, iCons(32, iCons(97, .IntSeq)))))
```

which is `"ab a"`, and cannot unify with the false `"ab b"` destination
(`evidence/stage6-false-kprove.log`).

Stage 6 result: **the main claim is result-discriminating and non-vacuous in
this narrow sense**. This does not repair its dependence on unsound execution
bridges.

## 7. Proven-versus-assumed accounting and decision

### What the successful K runs actually establish

The fresh `#Top` runs establish closure of:

1. a narrow word-result claim under fixed semantics plus pure helper equations;
2. a loop-result claim under the custom iterator and word operational bridge;
3. the end-to-end reachability claim under all candidate helpers and all three
   operational bridges.

Therefore, the end-to-end `#Top` establishes only:

> Under the extended theory in `verification.k`, if the exact closure call
> terminates from the formal initial state, it reaches the term
> `antiShuffleSpec(S)`.

It does not establish that fixed supplied semantics executes the submitted
body to that result. The body mutation proves the distinction concretely.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell prover, and builtin Int/Bool/String/Map/List theories | All build/proof results | Normal machine-checking trust boundary. |
| The byte-identical supplied semantics | All program execution claims | Benchmark-selected fixed model. Its partial-Python limitations are outside candidate authorship; the submitted construct slice is materially covered. |
| Trusted `py2mpy.py` and the mechanical constructor comparison | Python-to-K program identity | Byte regeneration and token comparison support this bridge. |
| `sortVS =` ascending Python-style sort | `sortWord`, loop result, final postcondition | Explicit fixed external primitive. Acceptable only conditionally; finite differential tests support, but do not universally prove, its Python intent. |
| IntSeq-to-Python string/code-point interpretation | Human-facing string theorem | Informal representation bridge, empirically supported over recorded ASCII/Unicode cases. |
| Partial-correctness termination convention | All reachability claims | The theorem is partial correctness; no separate total-termination theorem is claimed. |
| Candidate split bridge | Loop and end-to-end proofs | Illegitimate: changes result representation/allocation and lacks a complete connection theorem. |
| Candidate word bridge | Loop and end-to-end proofs | Illegitimate: bypasses lookup/evaluation and two allocations; narrow word value claim does not justify it. |
| Candidate loop bridge | End-to-end proof | Illegitimate and correctness-smuggling: arbitrary-context state mismatch and old theorem survives an actual body-result mutation. |

Differential testing, generation traces, the prior `prove.log`, and prose are
not counted as K proofs. They support only the specific finite implementation
and representation bridges described above.

### Decision

The source program is correct, its translation is faithful, the positive
commands reproduce, the formal domain is not materially narrowed, and a false
postcondition is rejected. Those facts cannot overcome Gate A failure. The
candidate makes false fixed-semantics transitions provable and proves the old
answer for a materially changed executed body. Under the benchmark decision
boundary, this is a materially unsound, execution-bypassing proof theory.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
