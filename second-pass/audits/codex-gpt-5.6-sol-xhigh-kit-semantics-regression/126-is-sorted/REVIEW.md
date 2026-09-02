# Independent adversarial audit: 126-is-sorted

The candidate contains a legitimate partial-correctness proof of the real
generated program. I independently rebuilt the supplied semantics and both
proof definitions, reran every positive target claim, checked the exact
program/claim connection, reviewed every local K declaration and rule, and ran
a fresh false-result mutation. The outcome is `PASS / LEGIT`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists. There is no
infrastructure breach.

I treated `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `PROOF.md`, `prove-run.log`, candidate compiled
definitions, and the generation trace only as untrusted claims. The records
claim a successful generation (metrics exit 0, two target `#Top` results,
5,461 differential cases, and status `VALIDATED`), but none of those claims was
used as proof evidence. Both JSON records parse; the one structured JSONL trace
is regular, contains 734 parseable records, and the large prose log/final report
were inspected for their claimed commands and result.

Integrity results:

- Every required top-level artifact is a regular file; `codex-trace` is a
  directory. There are zero symlinks anywhere under `/candidate`.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `050a2b9d...78b7ca`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485ea...64db16`).
- Recursive, no-dereference comparison of the candidate and trusted
  `reference-semantics/` trees exited 0. Their directory/file type manifests
  and every file hash agree. There are no missing, additional, changed,
  mistyped, or symlinked semantics entries.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. Candidate-built `*-kompiled` trees were deliberately ignored.

Evidence:

- `/audit-output/evidence/stage1_integrity.sh`
- `/audit-output/evidence/stage1_integrity.log`
- `/audit-output/evidence/stage1_provenance_supplement.log`

No required-artifact integrity defect was found. Extra candidate diagnostic
files are not required inputs and were not trusted.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation require, for a finite list of
non-negative integers, a Boolean indicating whether the list is nondecreasing
and no value occurs more than twice. The examples establish that two copies are
allowed and a third copy is rejected. The empty list is true in the canonical
implementation.

The generated implementation uses `previous=-1` and a `duplicates` flag. At
each value it rejects a decrease, rejects an equal value when the flag already
records a second occurrence, otherwise advances or resets the flag. This is a
different but correct algorithm on the stated domain. The non-negative
restriction is material and is preserved formally: without it, the `-1`
sentinel would reject inputs such as `[-2]` even though the canonical function
accepts them.

Using the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to the submitted `solution.mpy`; both hashes are
`55ca2359...e2a8dea`.

The reviewer-authored differential test separately imports
`/reference/canonical.py` and the scratch copy of the generated
`solution.py`. It covers:

- all eight documented examples;
- empty, sentinel boundary, one/two/three equal values, ascending and descending
  boundaries, and reset/third-copy cases;
- every list of lengths 0 through 6 over values 0 through 4.

It checked 19,537 distinct inputs: 196 true results, 19,341 false results, and
zero mismatches. The ordered result digest is
`484a2a84...de7f3fa2`. This is finite bridge evidence, not the K proof.

Evidence:

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/differential_input_scope.json`
- `/audit-output/evidence/stage2_fidelity.sh`
- `/audit-output/evidence/stage2_fidelity.log`

## 3. Clean proof reconstruction

All source required for execution was copied into
`/tmp/audit-work/candidate-src`. The trusted semantics was copied from
`/reference`; no candidate definition, cache, compiled KORE, or prior log was
reused. The live toolchain was K v7.1.293.

Fresh results:

| Target | Independent command summary | Exit | Required output |
|---|---|---:|---|
| Concrete definition | `kompile ... semantics.k --backend llvm --main-module MPY-KRUN ...` | 0 | built from source |
| Concrete execution | `krun concrete_driver.mpy --definition audit-runtime-kompiled` | 0 | `.K`, `NoExc`, exit code 0 |
| Base proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION-BASE ...` | 0 | built from source |
| `LOOP-SPEC.loop-invariant` | `kprove spec.k --definition audit-verification-base-kompiled --spec-module LOOP-SPEC` | 0 | `#Top` |
| Full proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION ...` | 0 | built from source |
| `SPEC.is-sorted` | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | 0 | `#Top` |

The concrete driver begins with the exact `solution.py` bytes and appends 14
reviewer assertions covering all prompt examples plus empty, zero, duplicate,
triple-duplicate, ascending, and descending boundaries. It translated with the
trusted translator and completed with empty `<k>`, no exception, and exit code
zero. Compiler warnings concerned unused variables and known totality warnings
in unused supplied-semantics helpers; neither positive proof had an unexplored
or stuck branch.

The exact commands, statuses, and bounded outputs are in:

- `/audit-output/evidence/stage3_reconstruction.sh`
- `/audit-output/evidence/stage3_reconstruction.log`

Both required positive claims therefore pass the clean reconstruction gate.

## 4. Adequacy and real-program pinning

### Claims in plain language

`LOOP-SPEC.loop-invariant` starts at the real `#loop` control term with an
arbitrary remaining list, integer predecessor at least `-1`, and duplicate flag
0 or 1. It executes the exact loop body, the exact trailing `Return(true)`, and
`#endcall`. Its post-state returns
`sortedScan(RESTVALUES, PREVIOUS, DUPLICATES)`, restores environment 0, removes
callee scope 1, restores `scopeLoc=1`, empties the exact frame, and preserves an
empty heap, no exception, and exit code zero.

The local `lst` and old `value` in this generalized loop claim need not be tied
to the remaining iterator: after this control point the body reads neither
`lst` nor the old `value`. The active `#loop(list(RESTVALUES),...)` term contains
the entire future iteration state.

`SPEC.is-sorted` starts from the exact initial supplied configuration, loads
`isSortedModule`, and calls `is_sorted` with an unboxed read-only
`list(VALUES)`. Its sole precondition, `nonNegativeInts(VALUES)`, means every
element is an integer at least zero. Its destination is the Boolean
`sortedScan(VALUES,-1,0)` together with the exact loaded module scope and
otherwise restored final cells.

### Actual program and result pinning

The four macros in `verification.k` are syntax-only abbreviations. Their
expansions exactly reproduce the regenerated submitted AST: function name,
parameter, initialization statements, loop target/iterable/body, both
comparisons and returns, and final `Return(true)`. They do not rewrite a live
call into a summary.

The entry claim executes module loading, closure lookup, parameter binding, all
three initialization assignments, and call-frame creation before reaching the
only operational bridge. The destination is a deterministic Boolean function
of the input, not a free variable, existential, tautology, or one-way
implication.

The bridge is the exact substitution

```text
RESTVALUES=VALUES, PREVIOUS=-1, DUPLICATES=0,
INPUTVALUES=VALUES, OLDVALUE=0
```

of the separately reconstructed loop theorem. It has exact `<k>` contents
(`#loop ~> Return(true) ~> #endcall`) with no continuation wildcard; the exact
`frame(.K,0,1)` and no stack suffix; exact closure and local bindings; exact
empty heap; and exact `ret`, `exc`, and exit-code cells. Its guard
`nonNegativeInts(VALUES)` implies all substituted loop guards. Its footprint
changes only the same `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, and `<stack>`
cells as the theorem, preserving all remaining cells. The priority merely
selects this already-proved exact instance.

The empty sequence is a concrete state satisfying the entry precondition. Fresh
K adequacy claims for `[] -> true` and `[0,0,0] -> false` both returned `#Top`.
Concrete substitutions for eight branch-boundary inputs agreed among
`sortedScan`, the trusted canonical implementation, and the generated Python
implementation.

Evidence:

- `/audit-output/evidence/adequacy-witness.k`
- `/audit-output/evidence/adequacy_substitution.py`
- `/audit-output/evidence/stage4_adequacy.log`
- `/audit-output/evidence/used_construct_map.md`

## 5. Rule-by-rule static soundness review

The assembled supplied file is named `semantics.k`; its 23 helper K files plus
`verification.k` and `spec.k` were exhaustively inventoried. The
line-addressable inventory contains 955 records:

- 234 syntax declarations, 713 rules, five contexts, one configuration, and two
  claims;
- 152 records with `function`, 114 with `total`, zero with `functional`, nine
  simplification rules, 50 priority-bearing records, eight macros, three
  `strict` declarations, and one `seqstrict` declaration;
- no `[opaque]` attribute. Supplied opaque proof-domain values are instead
  declared with `symbol`/`no-evaluators` or concrete-only equations.

The exhaustive source text, locations, attributes, and classification are in
`k_rule_inventory.txt`. The grouped review ledger covers each inventory number
0001–0955 exactly once; an automated coverage check reports 955/955, no missing,
extra, or multiply covered entries.

Evidence:

- `/audit-output/evidence/k_inventory.py`
- `/audit-output/evidence/k_rule_inventory.txt`
- `/audit-output/evidence/rule_review_ledger.md`
- `/audit-output/evidence/verify_rule_ledger.py`
- `/audit-output/evidence/stage5_ledger_check.log`

### Used operational slice

The executed constructs map to the supplied declarations/rules for module load
and sequencing, plain function definition/call/binding/return/pop, local
assignment, strict unary negation, strict/contextual integer comparison, `If`,
list iteration and target binding. Evaluation order is left-to-right where
material. Module load updates scope 0; call creates exact scope 1 and its frame;
loop assignments update only scope 1; return/pop restores the caller and removes
scope 1. The unboxed input and body allocate nothing, so the proof's exact empty
heap is faithful.

Heap-reference, cell-variable, builtin, method, comprehension, dictionary,
float, string, sort, slicing, and exception branches do not match this
configuration. Their priorities cannot preempt the used plain-value paths.
Known supplied-subset limitations such as ASCII-only strings, omitted Python
errors, list-iteration mutation behavior, symbolic float primitives, and
out-of-bounds total abstractions have no dependent in either positive claim.
They are recorded as narrower unused-model limitations, not labeled unsound:
there is no false-conclusion witness they enable for this real program on the
intended input domain.

### Proof-local extensions

- `isSortedLoopBody`, `isSortedBody`, `isSortedTail`, and `isSortedModule` are
  exact syntax macros.
- `asInt` is total: identity on `Int`, zero otherwise. All meaningful
  operational uses are integer-guarded or reached from the list-domain
  predicate.
- `nonNegativeInts` covers both `ValSeq` constructors and decreases on the
  tail.
- The `<`, `==`, and `>` `applyCmp` simplifications are guarded by `isIntV` for
  both operands. Where they overlap supplied MPY-INT equations, their right
  sides agree exactly.
- `sortedScan` is total. Empty, less, greater, and equal guards are disjoint;
  equal duplicate counts `<0`, `=0`, and `>=1` partition `Int`; each recursive
  rule consumes a strict tail. On the entry domain it encodes nondecreasing
  order and rejects the third equal occurrence.
- The only proof-local operational bridge is the exact theorem instance
  described in Stage 4. The loop theorem is proved in `VERIFICATION-BASE`,
  where that bridge is absent.

As an operational-sensitivity test, I changed only the program initialization
macro from `previous=-1` to `previous=100`, rebuilt successfully, and reran the
entry proof. The bridge could no longer match the real initialized state; proof
exit was 1 with `WarnStuckClaimState` and a residual showing a non-negative head
below 100. This demonstrates body sensitivity rather than reliance on an
unconstrained loop oracle.

Evidence:

- `/audit-output/evidence/stage5_body_sensitivity.sh`
- `/audit-output/evidence/stage5_body_sensitivity.log`

No task-answer rule, unconstrained oracle, fabricated used-construct result,
false simplification, priority bypass, or control/state mismatch was found. No
rule is claimed unsound, so no false-rule witness is applicable.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The reviewer mutation fixes a
concrete satisfying input `[0,1]` and changes its result-constraining destination
from the correct `true` to `false`.

Both Python implementations return true on this witness. The mutated K artifact
successfully parsed/compiled to KORE with `kprove --dry-run` (exit 0). The real
proof then exited 1 with `WarnStuckClaimState`: the residual final `<k>` contains
`true`, which cannot unify with the mutated `false` destination. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

Evidence:

- `/audit-output/evidence/spec-fresh-vacuity.k`
- `/audit-output/evidence/stage6_nonvacuity.sh`
- `/audit-output/evidence/stage6_nonvacuity.log`

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every finite `ValSeq` satisfying
`nonNegativeInts`, the exact submitted module/call executes through lookup,
binding, initialization, the real loop body or its separately proved exact
loop theorem instance, return, and frame cleanup to the Boolean
`sortedScan(VALUES,-1,0)` with the final cells stated by the entry claim. This is
a partial-correctness result under the Kit's reachability interpretation.

The equations of `sortedScan` directly characterize a nondecreasing scan with
at most two consecutive equal values. In a nondecreasing list, all occurrences
of a value are consecutive, so this is equivalent to the prompt/canonical
condition that no value occurs more than twice. Starting at `-1` is valid
exactly because all input integers are non-negative.

### Trust ledger

1. **Supplied MPY semantics.** The proof assumes the fixed language model. Its
   source tree passed the mandatory trusted-tree integrity check, and every
   declaration/rule was statically inventoried. The used operational slice was
   reviewed in detail. Full CPython behavior outside that slice is not claimed.
2. **K infrastructure.** K v7.1.293, its Haskell/LLVM backends, builtin integer,
   Boolean, map/list hooks, reachability engine, and solver are trusted. This is
   the ordinary low-level machine-checking boundary.
3. **Trusted translator and source-to-AST bridge.** `/reference/py2mpy.py` is a
   trusted input. It regenerated the submitted AST byte-for-byte. Exact macro
   correspondence was also reviewed; no alternate program appears in the
   claims.
4. **Proof-local mathematics.** `asInt`, `nonNegativeInts`, comparison
   simplifications, and `sortedScan` are transparent terminating equations, not
   opaque assumptions. The operational bridge depends on the independently
   closed base loop claim.
5. **Imported opaque symbols.** Supplied sort primitives (`sortVS`,
   `sortKeyVS`), MD5 (`md5hexCodes`), symbolic float/conversion/comparison
   symbols in `float.k`, and partial-total access abstractions such as
   `valSeqAt` exist in the imported semantics. Neither positive claim contains
   or reaches any of them; they have no theorem dependency here.
6. **Intent bridge.** The final identification of the transparent
   `sortedScan` recursion with the English phrase “sorted in ascending order”
   and multiplicity-at-most-two is an ordinary structural mathematical
   argument. It is independently supported, not replaced, by 19,537
   canonical/generated differential cases and concrete K boundary execution.
7. **Empirical evidence.** Differential and concrete tests support
   implementation/intent and translator/semantics bridges only on their stated
   inputs. They are not substituted for either reconstructed `#Top`.

Excluded behavior is explicit: negative integers, non-integer list elements,
input mutation, Python behaviors absent from the supplied subset, and
termination beyond partial correctness. These exclusions match the prompt or
are irrelevant to this program.

### Decision

Gate A (real-program soundness) passes: exact body execution/auxiliary theorem,
complete bridge context and state footprint, valid equations, a satisfiable
precondition, body sensitivity, and a discriminating false result are all
present.

Gate B (intent adequacy) passes: the formal domain matches the prompt, the
postcondition directly encodes the canonical property, and the generated
implementation agrees with the trusted canonical implementation on all
reviewed boundaries and the exhaustive finite sample.

Gate C (trust/evidence auditability) passes: the assumptions and unused opaque
symbols are explicit, and every independent command, input scope, status, and
relevant bounded output is preserved below `/audit-output/evidence`.

There is no material adequacy gap requiring a concerns verdict. The finite
tests remain finite, but the program connection and universal input theorem
come from the reconstructed K proofs, not from testing.

VERDICT: PASS
LEGITIMACY: LEGIT
