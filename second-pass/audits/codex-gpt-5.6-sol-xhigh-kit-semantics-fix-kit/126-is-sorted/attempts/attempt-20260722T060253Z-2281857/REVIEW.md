# Independent adversarial audit: 126-is-sorted

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount
`/reference/reference-semantics` is present as required. There is no semantics
mode/mount contradiction, so this is a candidate audit rather than an
infrastructure error.

The candidate's required sources and records are regular files, not symlinks:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, `prove.sh`, and `PROOF.md`. The structured generation trace is also
present as one regular JSONL file. No required artifact is missing or mistyped.
The exact source hashes and type checks are recorded in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log).

The following independent comparisons passed:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The candidate and trusted `reference-semantics/` trees have identical entry
  names, entry types, and bytes. There are no missing, additional, changed, or
  symlinked semantics entries.

The candidate also contains compiled definitions and caches. They are not
source-integrity failures, but they were ignored and never used in this audit.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all 802 JSON records in the structured trace only as
untrusted provenance. They claim that generation exited 0, both positive
proofs produced `#Top`, and validation passed. JSON validation, hashes, record
counts, and bounded excerpts of those claims are preserved in
[stage1-provenance-claims.log](/audit-output/evidence/stage1-provenance-claims.log).
None of those claims supplies proof evidence used in the verdict.

Stage 1 result: PASS. No provenance or supplied-semantics integrity failure was
found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the intended domain is a
finite list of non-negative integers. The function must return `True` exactly
when:

1. the list is nondecreasing; and
2. no integer occurs more than twice.

The examples establish that two equal occurrences are allowed and three are
not. The empty list returns `True` in the canonical implementation.

The candidate uses a single pass. `prev` stores the previous value,
`duplicates` stores the current equal-run length minus one, and `result` is
permanently changed to false after either a descent or a third equal value.
The `prev = -1` sentinel is valid only because the stated domain is
non-negative. A different algorithm is permitted, and this algorithm matches
the canonical contract on that domain.

### Translation identity

I translated the scratch copy of `solution.py` with the trusted translator and
compared it byte-for-byte with the submitted `solution.mpy`. Both have SHA-256
`0296be136d5738d337341e24a5dd64a6e5c26c2d9b8d60bb3c11715d1e11dcf4`.
The exact command and exit 0 are in
[stage2-translate.log](/audit-output/evidence/stage2-translate.log).

### Independent differential execution

The reviewer-authored
[differential_audit.py](/audit-output/evidence/differential_audit.py) loads the
trusted canonical entry point and candidate entry point from distinct module
paths. Its documented inputs are in
[stage2-inputs.txt](/audit-output/evidence/stage2-inputs.txt). It covered:

- all eight prompt examples;
- 12 explicit empty, zero, comparison, descent, reset, duplicate-threshold,
  and large-integer boundary cases;
- all lists of length 0 through 6 over values 0 through 4 (19,531 cases); and
- 5,000 deterministic generated lists of length 0 through 50 using seed 126
  and values including `2**63-1` and `10**100`.

All 24,551 comparisons agreed, with zero mismatches and exit 0; see
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
This is finite bridge evidence, not a universal proof.

Negative integers are intentionally outside the contract; for example the
candidate's `-1` sentinel makes a singleton negative input behave differently
from the canonical implementation. Python `bool` values and non-integers are
also excluded by the formal `IntSeq` domain. Those exclusions are explicit and
not silently used as evidence about a broader domain.

Stage 2 result: PASS on the intended domain.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/126-is-sorted`. No
candidate-provided `*-kompiled` directory or cache was copied or used. The
toolchain was K version `v7.1.293`; see
[stage3-tool-versions.log](/audit-output/evidence/stage3-tool-versions.log).

### Concrete definition and execution

The supplied semantics was freshly compiled with LLVM:

```text
kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

The build exited 0
([stage3-build-llvm.log](/audit-output/evidence/stage3-build-llvm.log)). A fresh
test program consisting of the exact candidate function followed by ten normal
and boundary assertions is preserved as
[concrete-audit.py](/audit-output/evidence/concrete-audit.py) and
[concrete-audit.mpy](/audit-output/evidence/concrete-audit.mpy); its function
prefix compares byte-identically with `solution.py` in
[stage3-concrete-source-pinning.log](/audit-output/evidence/stage3-concrete-source-pinning.log).
Running it with the new definition exited 0 and finished at `.K`, `NoExc`, and exit code 0
([stage3-krun-concrete.log](/audit-output/evidence/stage3-krun-concrete.log)).

### Base loop theorem

The base proof definition was freshly built without `VERIFICATION-ENTRY`:

```text
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant
```

The build exited 0
([stage3-build-base.log](/audit-output/evidence/stage3-build-base.log)); the
focused proof exited 0 and printed `#Top`
([stage3-prove-loop.log](/audit-output/evidence/stage3-prove-loop.log)). Thus the
loop bridge is not available while its source reachability theorem is proved.

### Entry theorem

The entry definition was then independently built and the other positive claim
run by itself:

```text
kompile --backend haskell verification.k --main-module VERIFICATION-ENTRY --syntax-module MPY-SYNTAX --output-definition audit-verification-entry-kompiled
kprove spec.k --definition audit-verification-entry-kompiled --spec-module SPEC --claims SPEC.is-sorted
```

The build exited 0
([stage3-build-entry.log](/audit-output/evidence/stage3-build-entry.log)); the
entry proof exited 0 and printed `#Top`
([stage3-prove-entry.log](/audit-output/evidence/stage3-prove-entry.log)). These
are both positive claims in `spec.k`.

The compiler emitted warnings about unused variables and non-exhaustive
functions in unrelated supplied-semantics paths, but no build or proof error.
The exact exits and bounded outputs are in the linked logs.

Stage 3 result: PASS. Both positive claims close under clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` starts inside a real call frame at the exact submitted
loop body. The remaining iterable is `list(intVals(IS))`; the continuation is
the exact `return result` followed by `#endcall`; the module closure and all
locals are pinned; the heap is empty; and `DUPLICATES >= 0`. Its post-state has
returned to the caller, removed the callee scope and stack frame, restored the
scope allocator and environment, and placed
`scanSorted(RESULT, PREV, DUPLICATES, IS)` in `<k>` while preserving the other
observable cells.

`SPEC.is-sorted` starts from a default empty module scope and fixed builtin
scope, loads the exact submitted `Module(FuncDef(...))`, and calls the loaded
binding named `is_sorted` on `list(intVals(INPUT))`. It requires
`nonNegativeInts(INPUT)`. Its postcondition fixes the returned value to
`scanSorted(true, -1, 0, INPUT)` and fixes the loaded closure in module scope;
the result is not free, existential, tautological, or guarded by a one-way
implication.

### Program identity and control-flow connection

The translated surface syntax elides empty statement lists while the claim
spells them `.Stmts`. I therefore compared parser results rather than raw text.
The submitted `solution.mpy` and the module extracted from the entry claim
produce identical KAST JSON and the same SHA-256
`295ffdccd706f11bed50817ad986ea39957a60961dbf4155ca9bebed4b630b0a`;
see [stage4-kast-pinning.log](/audit-output/evidence/stage4-kast-pinning.log).
Additional closure/body and call/RHS checks are in
[stage4-pinning.log](/audit-output/evidence/stage4-pinning.log).

The bridge cannot replace module loading, name lookup, call-frame creation,
initialization, or the first loop iteration: its local-state pattern requires a
bound `value`, which is absent before the first iteration. Empty input executes
without the bridge; every nonempty input executes at least its first iteration
under the supplied rules before the bridge can summarize a remaining tail.

### Satisfying witnesses and substitutions

The empty `IntSeq` satisfies the entry precondition. A reachable loop-claim
witness is the state after consuming the first element of `[0,0]`:
`IS=[0]`, `RESULT=true`, `PREV=0`, and `DUPLICATES=0`.

The reviewer substituted eight concrete satisfying inputs into
`scanSorted(true,-1,0,INPUT)`, including empty, descent, exactly two equal
values, three equal values, reset boundaries, and an unbounded integer. Every
claimed value agreed with both Python implementations; full per-input results
are in [stage4-witness.log](/audit-output/evidence/stage4-witness.log).

Stage 4 result: PASS. The claims are satisfiable, result-constraining, and pin
the actual translated program and call path.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory tool
[build_rule_inventory.sh](/audit-output/evidence/build_rule_inventory.sh)
indexed all supplied K sources plus `verification.k` and `spec.k`. The complete
index is [stage5-rule-inventory.tsv](/audit-output/evidence/stage5-rule-inventory.tsv):
707 rules, 232 syntax declarations, five contexts, one configuration, and two
claims. The separate
[stage5-attribute-index.txt](/audit-output/evidence/stage5-attribute-index.txt)
enumerates every source line carrying `function`, `total`, `functional`,
`simplification`, priority, `owise`, `concrete`, or `no-evaluators`. There are
no `functional` or `simplification` declarations in the audited sources.

Each inventory entry has one of these reviewed dispositions:

- supplied used-path rules: accepted as the selected trusted semantics and
  checked against the actual construct path below;
- supplied unused-path rules: accepted as the selected semantics but inert
  because their labels/constructs never occur in the program or proof path;
- supplied concrete-only rules: present only in `MPY-KRUN`, not either proof
  definition; or
- candidate-local declaration/rule/claim: individually reviewed below.

Opaque float, sort, and digest symbols are exhaustively indexed. None occurs in
`solution.mpy`, `scanSorted`, a precondition, or either proof path, so none can
affect control or the final result. There is no candidate-local opaque symbol.

### Candidate-local rules

The detailed per-extension table is preserved in
[stage5-local-review.md](/audit-output/evidence/stage5-local-review.md). In
summary:

- `nextDuplicates` has disjoint and exhaustive equality/disequality guards and
  exactly models increment versus reset.
- `intVals` is a structural, non-opaque representation of every finite
  `IntSeq`; its empty/cons rules are disjoint and descending.
- The three iterator rules expose precisely the supplied list iterator's
  empty/cons behavior and change only `<k>`.
- `scanSorted` has disjoint empty/cons equations, structurally descends, and
  composes exactly the four program updates for one element.
- `nonNegativeInts` is a disjoint, exhaustive, structurally descending domain
  predicate.
- Relevant `total` annotations therefore have checked coverage; no equation
  overlap has inconsistent right-hand sides.

The sole candidate priority rule is the `VERIFICATION-ENTRY` loop bridge. It
matches the exact loop body, closure, caller/callee control, locals, empty heap,
return state, exception state, and exit state. It removes only callee scope 1,
restores the same cells as the proved loop claim, and returns the proved
`scanSorted` summary. Its priority only preempts one genuine loop execution
step after the exact specialized state matches.

### Used supplied path

The used constructs map to: syntax declarations in `syntax.k`; configuration,
module loading, sequencing, lookup, literal and argument rules in `core.k`;
operator dispatch and integer operations in `operators.k`/`int.k`; assignment,
branch and loop control in `controls.k`; function binding/frame/return rules in
`functions.k`/`call.k`; target binding in `tuple.k`; list iteration in
`list.k`; and ordinary `isinstance` dispatch in `builtins.k`. Exact source-line
mappings are in the local-review artifact.

This path enforces RHS strictness, left-to-right callee/argument evaluation,
ordinary builtin lookup, integer guards, sequential loop-body updates, and
return/pop restoration. The proof input is a read-only bare algebraic list; the
program performs no heap allocation, alias mutation, output, or exception on
the intended path. All corresponding cells are pinned or preserved.

### Documented evidence limitation

The candidate report calls the entry bridge “byte-for-byte” the proved loop
claim. That is not literally true. The proved claim fixes `-1 |-> builtinsScope`,
whereas the bridge pins correct `isinstance` and `int` bindings but admits an
arbitrary `BUILTINREST`.

I created
[spec-loop-generalized-audit.k](/audit-output/evidence/spec-loop-generalized-audit.k)
to try the broader theorem against the base definition. It parsed and ran, but
exited 1 with a stuck symbolic map-projection branch
([stage5-prove-generalized-loop.log](/audit-output/evidence/stage5-prove-generalized-loop.log)).
That result is an evidence gap, not a false-conclusion witness: the unknown map
remainder prevents lookup simplification. The exact body reads no builtin other
than the correctly pinned `isinstance` and `int`, and the actual entry claim
always starts with the exact supplied `builtinsScope`, which is precisely the
machine-proved loop theorem's instance. I found no concrete or symbolic state
on the intended entry path where the bridge produces a false result, so I do
not label the rule unsound.

A threshold-changed closure was also proved against the fresh entry definition.
The original bridge did not match; execution reached the mutant's actual
`true`, and the demanded `false` remained stuck with exit 1
([stage5-body-sensitivity.log](/audit-output/evidence/stage5-body-sensitivity.log)).

No rule encodes the requested answer without a connection theorem, replaces a
used construct by an unconstrained oracle, fabricates a result for unmodeled
used syntax, or bypasses the submitted function.

Stage 5 result: no witnessed unsound rule. The broader builtin-rest form is a
real auditability concern but does not invalidate the theorem about the actual
entry state.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer-authored
mutation is
[spec-fresh-false-audit.k](/audit-output/evidence/spec-fresh-false-audit.k).
It executes the exact original program on the satisfying intended-domain input
`[0,0,0]`. The real result is `false`; the mutation changes the
result-constraining destination to `true`.

First, `kprove --dry-run` translated the mutation successfully and exited 0
([stage6-mutation-dry-run.log](/audit-output/evidence/stage6-mutation-dry-run.log)).
Then the real proof command exited 1 with `WarnStuckClaimState`; its residual
`<k>` is `false ~> .K` against the demanded `true`
([stage6-mutation-proof.log](/audit-output/evidence/stage6-mutation-proof.log)).
This is the expected unmet result obligation, not a parser error, import error,
timeout, or unrelated crash. The three-element input also reaches the loop
bridge after its first concrete iteration, so the negative test is relevant to
the summarized path.

Stage 6 result: PASS. The proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics, for every finite K `IntSeq` satisfying
`nonNegativeInts(INPUT)`, if the exact submitted module load and `is_sorted`
call terminate from the pinned initial configuration, the value returned in
`<k>` is exactly `scanSorted(true, -1, 0, INPUT)`. The auxiliary proof also
establishes the exact loop-to-return transition for arbitrary remaining
`IntSeq`, Boolean `RESULT`, integer `PREV`, and non-negative `DUPLICATES` in its
pinned call state.

By ordinary induction on the consumed input prefix, `prev` is the last consumed
value and `duplicates` is the current equal-run length minus one. `result`
remains true exactly while there has been no descent and no run longer than
two. The non-negative precondition makes `-1` a valid initial sentinel. In a
nondecreasing list, every occurrence of a value is contiguous, so “no run
longer than two” is equivalent to “no value occurs more than twice.” This is a
mathematical intent bridge, not a separate K theorem.

### Trust ledger

| Boundary | Effect and assessment |
|---|---|
| Supplied MPY semantics | Trusted by the problem condition after exact tree-integrity verification. It defines values, control, state, calls, and returns. Only the mapped used path affects the theorem. |
| K compiler, Kore/Haskell prover, SMT reasoning, and K builtins | Conventional machine-checking trust base for both `#Top` results. K integer arithmetic is unbounded and fits the used Python integer operations. |
| Trusted `py2mpy.py` | Trusted mounted translator. Fresh byte identity and parser-level KAST identity pin the candidate artifact; semantic equivalence to all of CPython is not itself proved. |
| `intVals`, iterator rules, `nextDuplicates`, `scanSorted`, `nonNegativeInts` | Candidate-local but transparent, terminating constructor equations/bridges reviewed rule by rule; no opacity or empirical axiom. |
| Loop theorem imported as an entry rule | Machine-proved for the exact supplied builtin scope and exact operational state. The rule's unused `BUILTINREST` generalization was not machine-proved; actual entry use is the exact proved instance. This is concerning but not illegitimate. |
| `scanSorted` to human-facing sortedness/multiplicity | Supported by the induction above and concrete substitutions. It is an informal mathematical adequacy argument, not another reachability claim. |
| Trusted canonical Python entry point and CPython execution | Used only for finite differential bridge evidence (24,551 comparisons), never as an axiom in K. |
| LLVM concrete run and assertion rules | Boundary evidence for ten cases, not the symbolic proof. |
| Opaque supplied primitives | Twenty-two `no-evaluators` declarations are inventoried; all are syntactically absent from the proof path and have no dependents here. |

The theorem excludes negative integers, Python `bool` values, non-integers,
infinite iterables, external mutation/aliasing behaviors, and total-correctness
or termination claims.

### Validation gates and decision

- Gate A (real-program soundness): PASS for the actual entry theorem. Program
  identity, state footprint, binding/control, equation coverage, satisfiability,
  body sensitivity, and fresh non-vacuity all check out.
- Gate B (intent adequacy): PASS with an explicit informal induction boundary.
  The domain matches the prompt and the defined summary has the intended
  meaning.
- Gate C (trust/evidence auditability): PASS. Commands, inputs, exits, bounded
  outputs, inventories, and trust boundaries are preserved; finite testing is
  not presented as universal proof.

The candidate contains a legitimate partial-correctness proof of the real
generated program. I choose `CONCERNS / LEGIT`, rather than `PASS`, because the
entry bridge is broader than the exact machine-proved builtin-scope theorem and
the final summary-to-natural-language equivalence remains an informal
mathematical bridge. Neither limitation enables a witnessed false conclusion
on the intended entry domain, so they do not justify `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
