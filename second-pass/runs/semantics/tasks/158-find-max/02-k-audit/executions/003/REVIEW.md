# Independent adversarial audit: 158-find-max

The candidate contains a legitimate partial-correctness proof of the generated
program. I reconstructed the proof from source, established constructor-level
program identity, audited every proof-local extension, supplied a bridge-free
connection theorem for the two operational accelerators, and obtained the
expected failure from both an executed-body mutation and a fresh false-result
mutation.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. This is consistent with the mounts:
`/reference/reference-semantics` exists and contains the supplied semantics.
There is no infrastructure breach.

The independent checker and its full output are
`/audit-output/evidence/provenance_check.py` and
`/audit-output/evidence/provenance-check.log`. It established:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable. The lock's
  actual SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`, and the parsed lock is exactly equal to the
  recorded `audit_campaign` object.
- All required legacy-selected-stage1 records are present, readable, regular
  mounts rather than symlinks: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  The optional-present `usage.json` was also read.
- Independently recomputed file hashes match every applicable recorded hash for
  the run, task, result, invocation, metrics, generation prompt/output/last/usage,
  canonical, trusted prompt, trusted translator, candidate prompt, and candidate
  translator.
- The one trace file has 403 valid JSONL records and no invalid line. Its
  SHA-256, and every invocation-declared evidence-file SHA-256, match the
  recorded values. The untrusted action/message summary is preserved in
  `/audit-output/evidence/generation-trace-summary.log`; it was not used as proof.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  versions.
- The candidate and trusted `reference-semantics` trees each have the same 24
  regular files (25 typed entries including the `semantics/` directory), no
  symlinks, and zero missing, additional, mistyped, or changed entries. Their
  reviewer-defined typed-manifest hashes are identically
  `2e6c7099dac526390aa6f80572eb3c472da85e2e4360176ab222cccddea4b38a`.

The proof-source artifacts were independently hashed and their scratch copies
were byte-compared to the mount in
`/audit-output/evidence/candidate-source-hashes.log`. All builds below used
those source copies plus a fresh copy of the trusted semantics. No
candidate-built definition or cache was copied or used.

## 2. Program fidelity and canonical comparison

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, the intended input is
a nonempty list of pairwise different strings. The result is a word having the
greatest number of distinct characters; among equal scores it is the
lexicographically least word. Nonemptiness is implicit in “return the word” and
is made operationally explicit by the trusted canonical's
`sorted(...)[0]`.

`/candidate/solution.py` implements a single fold. It starts with score zero,
updates both the best word and score on a strictly greater distinct-character
count, updates only the best word on an equal score and smaller word, and
otherwise preserves the accumulator. This is equivalent to the canonical
ordering for every nonempty list in the source domain.

### Translation identity

The trusted `/reference/py2mpy.py` was copied to scratch and run as:

```text
cd /tmp/audit-work/repro
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated MPY files have the same
SHA-256,
`1540848d93ea1f97b3b2355a5bd995a986cba1613b6dba2020b0ab9d8b65d947`.
See `/audit-output/evidence/translation-fidelity.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical and generated entry points. It covers:

- all three documented examples;
- the empty list, one-element lists, and empty-string elements;
- greater-score, smaller-score, equal-score/tie-update, and
  equal-score/tie-preserve paths;
- repeated characters, combining characters, non-ASCII code points, and emoji;
- 2,000 deterministic generated nonempty lists sampled without replacement.

The exact command and result are in
`/audit-output/evidence/differential-test.log`: 2,017 cases, zero nonempty
mismatches. The only mismatch is the explicitly tested `[]`: canonical Python
raises `IndexError`, while the generated program returns `""`. This is an
extra behavior outside the canonical's nonempty domain, not a domain narrowing
or a false result on the intended domain.

## 3. Clean proof reconstruction

The live tools are K v7.1.293
(`/audit-output/evidence/toolchain.log`). The scratch directory contained source
artifacts only when reconstruction began.

### Concrete definition

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0. The warnings concern exhaustiveness or unused variables in
unrelated fixed-semantics functions. The log is
`/audit-output/evidence/kompile-runtime.log`.

```text
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty
```

This exited 0 with final `.K`, `NoExc`, and exit code 0. The complete bounded
configuration is in `/audit-output/evidence/krun-concrete.log`.

### Proof definition and positive claims

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0
(`/audit-output/evidence/kompile-verification.log`).

The loop circularity was proved independently:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.find-max-loop-invariant
```

It printed `#Top` and exited 0
(`/audit-output/evidence/kprove-loop.log`).

The complete dependent claim set was then proved:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0
(`/audit-output/evidence/kprove-all-claims.log`). This run proves both positive
claims, with the loop claim available as the circularity required by the
contract.

For completeness, filtering to only `SPEC.find-max-contract` was a diagnostic
mistake: it also filtered out the circularity and caused unbounded concrete
unrolling. That CPU-active diagnostic was reviewer-interrupted and is explicitly
marked in
`/audit-output/evidence/kprove-contract-without-invariant-diagnostic.log`; it is
not treated as a claim result.

## 4. Adequacy and real-program pinning

### Claims in plain language

`find-max-loop-invariant` starts at the real supplied-semantics `#loop` over an
arbitrary finite `WordSeq`, with the real loop target and exact loop body. The
active function scope contains arbitrary current `best`, `max_unique`, prior
`word`, and prior `unique` values. At loop completion, execution resumes the
arbitrary continuation `KONT`; `best` and `max_unique` equal the mathematical
fold over the remaining words. The previous/final loop temporaries are
intentionally existential because they are not returned or used after the loop.

`find-max-contract` starts from the clean MPY initial state, loads a module
binding `find_max`, calls it on an arbitrary finite sequence of string values,
and requires the returned value to be exactly:

```text
str(bestWord(findMaxWords(WORDS, .IntSeq, 0)))
```

The post-state also fixes the module binding, empty heap, restored stack and
return state, `NoExc`, and exit code 0. The return is therefore constrained; it
is neither a fresh variable nor a one-way implication.

### Satisfiable entries and ground substitution

The concrete witness `WORDS = ["ba", "ab"]` satisfies the contract entry. A
corresponding loop witness uses the same iterator, `BEST = ""`, `SCORE = 0`,
and the exact scope described in the claim. Both trusted canonical Python and
generated Python return `"ab"`. The K summary reduces to best word `"ab"` and
score `2`. Evidence:

- `/audit-output/evidence/ground_witness.py`
- `/audit-output/evidence/ground-witness-python.log`
- `/audit-output/evidence/kprove-ground-witness.log` (`#Top`, exit 0)

### Mechanical program identity

The end-to-end claim uses proof-local names for the bodies. Identity was checked
at constructor level, not inferred from names:

1. `solution.mpy` was regenerated byte-for-byte with the trusted translator.
2. `/audit-output/evidence/make_body_identity_spec.py` mechanically parses the
   regenerated `FuncDef`, extracts its third argument, and makes only the
   MPY-parser normalization that writes two omitted empty statement lists as
   explicit `.Stmts`.
3. The generated reachability equality
   `findMaxFunctionBody => <extracted translated body>` printed `#Top` and
   exited 0. K reports it as trivial after normalization because the two
   constructor terms are identical. See
   `/audit-output/evidence/body-identity-spec-generation.log` and
   `/audit-output/evidence/kprove-body-identity.log`.

The attempted direct executable-parser comparison is retained only as
`/audit-output/evidence/program-pinning-parser-diagnostic.log`: the
`MPY-SYNTAX` parser correctly does not expose proof-local names.

### Body sensitivity

In a separately rebuilt scratch definition, the function-body term actually
used by the claim was changed from `Return(Name("best"))` to
`Return(Str("wrong"))`; no external source-only mutation was used. The mutation
and build are in:

- `/audit-output/evidence/body-sensitivity-mutation.diff`
- `/audit-output/evidence/kompile-body-sensitivity.log` (exit 0)

The proof then reached `str("wrong")` and failed the equality with
`bestWord(findMaxWords(...))`, emitting `WarnStuckClaimState` and exiting 1.
See `/audit-output/evidence/kprove-body-sensitivity.log`. This establishes that
the theorem depends on the executed body.

### Domain adequacy

`WordSeq` is inductive and unbounded; the proof is not a finite-size,
example-only, or bounded-unrolling theorem. It admits duplicate words, the
empty list, and arbitrary integer code sequences. Those are sound
over-approximations, not restrictions. In particular, every nonempty list of
pairwise different Python strings in the source contract has a corresponding
formal input.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/inventory_k.py` inventories every `configuration`,
`context`, `syntax`, `rule`, and `claim` declaration in all 24 fixed-semantics
files plus `verification.k` and `spec.k`. The complete 958-entry inventory,
including attributes and review classification, is
`/audit-output/evidence/k-inventory.tsv`; counts are in
`/audit-output/evidence/k-inventory-summary.log`.

The inventory contains:

- 695 fixed-semantics rules, 227 fixed-semantics syntax declarations, five
  contexts, and one configuration;
- 7 proof-local syntax declarations and 21 proof-local rules;
- 2 specification claims.

Unused fixed-semantics constructs remain within the launcher-selected trusted
semantics boundary. The task path was reviewed in detail. The relevant mapping
is:

| Generated construct/operation | Declaration and behavior |
|---|---|
| `Module`, statement sequences, names, literals | `semantics/syntax.k`; load/sequence/lookup/literal rules in `semantics/core.k` |
| `FuncDef`, call, parameter binding, return/pop | `semantics/functions.k` and `semantics/call.k` |
| `Assign`, `If`, `For` | `semantics/controls.k` |
| loop target binding | `semantics/tuple.k` (`#bindTgt(Name(...), ...)`) |
| list iteration | `semantics/list.k` and `semantics/iter.k` |
| `set(str)` and distinct-character count | `semantics/builtins.k`, `semantics/set.k`, and `isLen` in `semantics/core.k` |
| integer and string comparisons | `semantics/operators.k`, `semantics/int.k`, and `semantics/str.k` |

These rules preserve left-to-right callee/argument evaluation, lexical lookup,
function-frame creation/restoration, assignment to the current scope, one-time
iterable evaluation, ordered iteration, branch selection, and return control.
The material operations `set`, `len`, integer comparisons, and string order all
execute under fixed supplied rules.

### Every proof-local extension

All 28 proof-local entries are accounted for below.

| Entries in `verification.k` | Classification and decision |
|---|---|
| Lines 7-11: `WordSeq`, `wordVals`, and its two equations | Definitional input representation. The equations are constructor-preserving, disjoint, exhaustive over `WordSeq`, and structurally descending. |
| Lines 16-20: two priority-40 iterator rules | Operational bridges over the proof representation. They rewrite only the `<k>` cell, preserve the arbitrary continuation and every other cell, and exactly compose `wordVals` with the fixed empty/cons list-iterator rules. |
| Lines 23-35: `findMaxLoopBody` and equation | Definitional body name. It is the exact loop-body subtree of regenerated `solution.mpy`. |
| Lines 37-44: `findMaxFunctionBody` and equation | Definitional body name. Constructor identity with the entire regenerated function body is machine checked in Stage 4. |
| Lines 48-82: `BestState`, total `findMaxWords`, and five equations | Mathematical fold. The base case returns the accumulator. The four step guards are pairwise disjoint and exhaustive: greater, less, or equal; the equal case splits on `strLt` and its negation. Every recursive call consumes one `wCons`. RHS updates exactly match the Python branches. |
| Lines 84-88: total `bestWord`/`bestScore` and projections | Pure projections. `findMaxWords` totality ensures every reachable `BestState` reduces to `bestState`; neither projection introduces a value. |
| Lines 92-130: eight simplification rules | Two projections for each of the same four disjoint fold cases. Each RHS is precisely the corresponding `findMaxWords` equation under the identical guard. They accelerate symbolic simplification but do not replace program execution. |

No proof-local opaque or fresh result-bearing symbol exists. `findMaxWords`,
`bestWord`, and `bestScore` are completely defined. The projection
simplifications use the same symbol only after the separately proved loop
execution connects program state to the summary; this is not an oracle-shaped
operational rewrite.

### Operational-bridge connection

The two iterator bridges accept an arbitrary continuation (`...`) and omit all
non-`k` cells, so their required justification domain is equally general. I
created `bridgefree.k`, which imports only fixed `MPY` and independently defines
the truthful total constructor map `wordVals`; it does not import either
iterator bridge. The two connection claims quantify over arbitrary
`KONT:K`:

```text
#iterNext(list(wordVals(.WordSeq))) ~> KONT
  => #iterDone ~> KONT

#iterNext(list(wordVals(wCons(WORD, REST)))) ~> KONT
  => #iterYield(str(WORD), list(wordVals(REST))) ~> KONT
```

The bridge-free definition built, and both universal claims printed `#Top` and
exited 0. See
`/audit-output/evidence/kompile-bridgefree-functional.log` and
`/audit-output/evidence/kprove-bridge-connection.log`. The functional/total
annotation supplies evaluation for the independently justified constructor
map; it adds no equation or iterator conclusion.

The retained
`/audit-output/evidence/kprove-bridge-connection-nonfunction-diagnostic.log`
shows why the bridge is useful: without evaluation for `wordVals` beneath the
list constructor, the fixed engine leaves that proof representation stuck. It
does not exhibit a disagreeing value, state, or control result.

### Fixed opaque primitives

The supplied semantics contains opaque/concrete-only float operations,
`sortVS`, `sortKeyVS`, and `md5hexCodes`. The complete list is captured by the
inventory and source scan. None occurs in `solution.mpy`, `verification.k`,
either claim, or the result summary. They therefore have no dependent theorem
here. The task-relevant `strLt`, `dedupCodes`, `isLen`, list iteration, `set`,
and `len` operations all have exhaustive structural equations on the formal
input representation.

I found no unsound rule. Accordingly, there is no false-conclusion witness to
report; the required positive evidence instead consists of the bridge-free
connection, ground summary checks, body sensitivity, and non-vacuity failure.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. I copied the original spec to
scratch, changed only the contract result to the concrete string `"wrong"`,
and renamed the module/claim. The exact mutation is
`/audit-output/evidence/spec-vacuity.diff`.

The satisfying witness `["ba", "ab"]` returns `"ab"` in both Python
implementations, so the mutation is demonstrably false. It is also false for
the empty formal input.

Build-only validation:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
```

This exited 0 (`/audit-output/evidence/spec-vacuity-build.log`).

Actual mutation proof:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

This reached the normal final configuration, emitted `WarnStuckClaimState`, and
failed the implication
`"wrong" == bestWord(findMaxWords(WORDS, .IntSeq, 0))`. `kprove` exited 1;
the checking wrapper exited 0 only after confirming that nonzero status. See
`/audit-output/evidence/kprove-spec-vacuity.log`. The failure is therefore the
expected unmet result obligation, not a parser error, missing import, crash, or
unreachable mutation.

## 7. Proven versus assumed

### What the successful reachability proof establishes

For every finite formal list of strings represented by `WordSeq`, if the
submitted `find_max` execution reaches the function return under the supplied
MPY semantics, the returned string is the result of the completely defined
`findMaxWords` fold: maximum `len(dedupCodes(word))`, breaking equal scores by
`strLt`. The proof also establishes the loop accumulator relation and the
specified restored control/state cells. This is partial correctness; it does
not separately prove termination.

The fold has the requested human meaning by a direct induction over the input
sequence. Starting from score zero, a higher score replaces the current
candidate, a lower score preserves it, and an equal score retains the
lexicographically smaller word. After each prefix, the accumulator is therefore
the lexicographically least maximum-score word of that prefix. The empty-string
first element is also handled: score and best remain zero/empty, which is that
element. This mathematical bridge is independently supported, but not replaced,
by the zero-mismatch nonempty differential run.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 frontend, Haskell/LLVM backends, and K built-in Int/Bool/String/Map theories | All parsing, execution, and reachability | Standard machine-checking trust boundary; version recorded and fresh outputs preserved. |
| Launcher-selected supplied MPY semantics | Meaning of the Python subset | Required trusted semantics level; byte-identical candidate/trusted trees. All task-relevant operations are structurally defined and reviewed. |
| Trusted `py2mpy.py` | Python AST to MPY constructor bridge | Hash-verified and rerun; exact byte identity removes candidate translation discretion. |
| `WordSeq`/`wordVals` input representation | Maps formal string sequences to MPY list/string values | Truthful total constructor map; both iterator compositions have bridge-free universal proofs. |
| `findMaxWords`, `bestWord`, `bestScore` | Formal result specification | Fully defined, exhaustive, terminating mathematics; no opacity or oracle. Connected to execution by the loop claim. |
| Python string to integer-code sequence and `strLt` as Python lexical order | Human-intent interpretation | Ordinary code-point model. It agrees with Python lexicographic ordering on valid Python strings; finite Unicode probes also agree. |
| Concrete and differential tests | Translation/intent evidence on tested inputs | Finite evidence only; not used as a substitute for the K proof. |
| Fixed opaque float/sort/MD5 symbols | Unused language facilities | No influence on control, state, result, or either claim. |
| Termination | Outside partial-correctness theorem | Explicitly not claimed, as required by the benchmark. |

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and evidence auditability) all pass. The empty-list Python difference is an
extra generated behavior outside the canonical nonempty domain, not a material
adequacy gap. There is no finite-size restriction, substituted program,
unconstrained result, unsound rule, or unrecorded proof dependency.

VERDICT: PASS
LEGITIMACY: LEGIT
