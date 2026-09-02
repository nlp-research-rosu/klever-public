# Independent adversarial audit: `0-has-close-elements`

This is a completed seven-stage audit in `SUPPLIED_SEMANTICS` mode. The
candidate's compiled definitions, logs, trace conclusions, and prior `#Top`
were not reused as authority. All executable reconstruction used source copied
to `/tmp/audit-work/reconstruction`; evidence and reviewer-authored probes are
under `evidence/`.

Headline decision: **FAIL / NOT_LEGIT**. The positive claims reconstruct and
the result is non-vacuously constrained, but the entry claim invokes the
program on a proof-only `ValSeq` constructor. Two priority rules give that
constructor iterator behavior which the selected fixed semantics does not
have. A fresh ground witness shows the corresponding fixed-semantics entry
execution stuck while the extended execution proves the claimed return.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. `/reference/reference-semantics`
exists as a directory, so there is no infrastructure breach and a candidate
verdict is appropriate.

The independent `lstat`/SHA-256 comparison in
[`stage1-integrity.log`](evidence/stage1-integrity.log) found:

- 25 entries in each semantics tree, with identical relative paths, entry
  types, and file bytes;
- no missing, additional, changed, mistyped, or symlinked candidate semantics
  entry;
- byte-identical candidate/trusted `prompt.py` with SHA-256
  `00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a`;
- byte-identical candidate/trusted `py2mpy.py` with SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- all required generation reports and proof/source artifacts as regular
  files; and
- one regular structured trace containing 959 valid JSON records.

`run-input.json`, `metrics.json`, `codex-last.txt`, all 3,383,048 bytes of
`codex-output.log`, and every structured-trace record were read and summarized
only as untrusted claims. The bounded summary is
[`stage1-untrusted-generation-summary.log`](evidence/stage1-untrusted-generation-summary.log).
Those reports claim an exit-0 generation and positive `#Top`, but also
explicitly admit that the exact bridge LHS is stuck without the extension.
Neither claim was used in place of reconstruction. Candidate-provided
`*-kompiled` directories and Python caches were not copied.

## 2. Program fidelity and candidate-versus-canonical checks

The contract from the trusted prompt and canonical implementation is:
for a list of floats and a float threshold, return `True` exactly when two
different indices contain values whose absolute difference is **strictly**
less than the threshold. Empty and singleton lists return `False`; equality
with the threshold is not close.

The canonical implementation returns immediately on finding a qualifying
ordered pair. `solution.py` instead visits all ordered pairs, skips equal
indices, and accumulates a Boolean that can change only from false to true.
This is a different but extensionally equivalent algorithm on its stated
domain.

Trusted translation of the scratch copy of `solution.py` exited 0. `cmp`
against the submitted `solution.mpy` exited 0; both MPY files have SHA-256
`e8a521119af77c53d4ac2158bb0ee8a2126a2bf726cdde7cec5e032fd245a37e`.
See [`stage2-regenerate-mpy.log`](evidence/stage2-regenerate-mpy.log).

The independent differential uses three implementations: the trusted
canonical entry point, the generated entry point, and a separately written
unordered-index-pair oracle. It ran 45,226 cases with zero mismatches:

- both documented examples;
- empty and singleton lists;
- self-index, `<`, `==`, and `>` threshold boundaries;
- zero/negative thresholds, duplicates, signed zero, subnormals, overflow,
  infinities, and NaNs;
- all lists of length 0–4 over seven finite values at nine thresholds
  (25,209 cases); and
- 20,000 cases from fixed seed `20260723`.

The script, exact deterministic input construction, compressed complete input
artifact, digest, command, result, and exit status are
[`differential_test.py`](evidence/differential_test.py),
[`differential-inputs.jsonl.gz`](evidence/differential-inputs.jsonl.gz), and
[`stage2-differential.log`](evidence/stage2-differential.log). This is finite
bridge evidence, not a universal K proof.

## 3. Clean proof reconstruction

The scratch source copy contains only candidate source artifacts plus the
trusted semantics and trusted reference inputs. Its hashes are recorded in
[`scratch-source-copy.log`](evidence/scratch-source-copy.log). The installed
tools independently reported K version `v7.1.293`.

Fresh concrete reconstruction:

- `kompile --backend llvm reference-semantics/semantics.k --main-module
  MPY-KRUN --syntax-module MPY-SYNTAX --output-definition
  runtime-audit-kompiled` exited 0
  ([log](evidence/stage3-kompile-llvm.log));
- a reviewer-authored program containing the exact generated implementation
  and ten normal/boundary assertions was translated with the trusted
  translator; and
- `krun concrete_checks.mpy --definition runtime-audit-kompiled` exited 0
  with final `.K`, `NoExc`, and exit code 0
  ([source](evidence/concrete_checks.py),
  [MPY](evidence/concrete_checks.mpy),
  [run](evidence/stage3-krun-concrete-checks.log)).

Fresh proof reconstruction:

- `kompile --backend haskell verification.k --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  verification-audit-kompiled` exited 0
  ([log](evidence/stage3-kompile-haskell.log));
- `SPEC.inner-loop` alone exited 0 and printed `#Top`
  ([log](evidence/stage3-kprove-inner.log));
- `SPEC.outer-loop`, with its required `inner-loop` circularity selected,
  exited 0 and printed `#Top`
  ([log](evidence/stage3-kprove-outer-with-dependency.log)); and
- `SPEC.target`, with both required circularities selected, exited 0 and
  printed `#Top`
  ([log](evidence/stage3-kprove-target-with-dependencies.log)).

Thus verification under the candidate's **extended** theory reconstructs.
This mechanical gate does not establish that the theory is a sound extension
of the selected semantics.

## 4. Adequacy and real-program pinning

### Plain-language claims

`inner-loop` starts at the exact inner `#loop` body over a remaining
`FloatSeq`. The local frame fixes `numbers`, `threshold`, accumulator
`result`, outer value/index, inner index, and reset `elem2`. It claims that
finishing the remaining loop changes `result` to `innerAcc(...)`, increments
`j` by the remaining length, resets `elem2`, and otherwise preserves the
framed state.

`outer-loop` starts at the exact outer `#loop` over a remaining `FloatSeq`.
Its local frame fixes the full input, threshold, accumulator, outer index, and
reset locals. It claims that finishing the outer loop changes `result` to
`outerAcc(...)`, increments `i` by the remaining length, and leaves `j`,
`elem`, and `elem2` reset.

`target` starts from the initial module configuration, loads the submitted
function, calls it, and claims the returned `<k>` value is
`outerAcc(false, 0, INPUT, INPUT, THRESHOLD)`. It also pins the module closure,
scope allocator, heap, stack, return state, exception state, and exit code.
There is no explicit side condition: `INPUT` ranges over every finite
`FloatSeq` and `THRESHOLD` over K `Float`.

### Program text versus argument representation

The submitted MPY and the program inside target's `#loadAll` parse to identical
KORE ASTs, digest
`f5e979a20fd535830056bda0eef91308dd469249ad6eef97f11d49239e4db7db16`;
see [`stage4-program-ast-pinning.log`](evidence/stage4-program-ast-pinning.log).
The spelling difference is only that the claim writes empty statement lists
as `.Stmts`. Therefore the target does load the real submitted body.

The call argument is not a real runtime list representation, however. It is
`list(floatVals(INPUT))`. Fixed `ValSeq` has only `.ValSeq` and
`vCons(Val, ValSeq)` constructors, and fixed `list.k` iterates exactly those
forms. Candidate `verification.k` adds `floatVals(FloatSeq)` as a third,
proof-only `ValSeq` constructor.

### Satisfying state and ground witness

`INPUT = .FloatSeq` and `THRESHOLD = 0.5` satisfy every entry variable sort and
the complete initial configuration. The claimed summary reduces to false.
Both trusted canonical Python and generated Python return false for
`([], 0.5)`.

Three fresh ground entry probes isolate the representation issue:

1. With the actual runtime empty list `list(.ValSeq)`, the submitted body
   under `VERIFICATION-BASE` (no iterator bridges) exits 0 with `#Top`
   ([artifact](evidence/ground-actual-empty-base.k),
   [log](evidence/stage4-ground-actual-empty-base.log)).
2. With the target's `list(floatVals(.FloatSeq))`, the same body under
   `VERIFICATION-BASE` exits 1 with `WarnStuckClaimState` at
   `#iterNext(list(floatVals(.FloatSeq)))`
   ([artifact](evidence/ground-proof-empty-base.k),
   [log](evidence/stage4-ground-proof-empty-base.log)).
3. The identical proof-only ground entry under `VERIFICATION` exits 0 with
   `#Top` after the bridge is added
   ([artifact](evidence/ground-proof-empty-extended.k),
   [log](evidence/stage4-ground-proof-empty-extended.log)).

This is the required false-conclusion witness for the operational extension:
on a concrete state satisfying the formal target precondition, fixed semantics
does not reach the claimed false result, while the bridge-enabled theory says
it does. The corresponding intended runtime empty list is a different term
and does execute. The theorem therefore substitutes an extended
representation for the real input.

Six ground substitutions of `outerAcc` (empty, singleton, strict equality,
strictly close, duplicates, and negative threshold) were also evaluated under
the concrete supplied float interpretation and matched both Python
implementations. The LLVM runner ended in `.K` with exit 0
([runner](evidence/summary-runner.k),
[log](evidence/stage4-krun-ground-summaries.log)). This supports the summary's
intended meaning but cannot repair the missing fixed-semantics connection.

The result itself is not free or tautological: it is the recursively defined
`outerAcc`, and Stage 6 rejects a false replacement. Adequacy fails specifically
at real-program input pinning.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 26 selected source files:
the trusted wrapper/helpers, `verification.k`, and `spec.k`. It contains 952
sentences: 231 syntax declarations, 712 rules, five contexts, one
configuration, and three claims. Attributes/classifications include 147
functions, 109 `total` declarations, zero `functional` declarations, 22
`no-evaluators` opaque symbols, 47 priority rules, 35 concrete rules, six
simplifications, and 645 ordinary rules.

Every sentence, full compact text, source span, module, attributes, disposition,
and rationale is recorded in
[`rule-inventory.tsv`](evidence/rule-inventory.tsv) and
[`rule-assessment.tsv`](evidence/rule-assessment.tsv). The disposition totals
are:

- 906 exact supplied fixed-semantics sentences accepted as the selected
  language model;
- 22 supplied opaque boundaries, of which only `subF`, `absF`, and `floatLt`
  influence this theorem;
- 10 accepted proof-local definitional declarations/equations;
- eight locally valid but unconnected encoding equations/simplifications;
- two bridge-dependent loop circularities;
- one target failing real-program pinning;
- one failing runtime-representation syntax extension; and
- two failing operational bridges.

The construct-to-rule map is
[`used-construct-map.md`](evidence/used-construct-map.md). On the used path,
the supplied rules preserve left-to-right expression/call evaluation, ordinary
scope lookup and builtin shadowing, local assignment, exact nested-loop
control, frame allocation/pop, and all configuration cells. The target has no
program heap allocation; the plain float list is a read-only value. The return
rule discards only the remaining callee computation and restores the caller
continuation from the stack.

### Proof-local definitions and guards

`FloatSeq` is an ordinary finite structural datatype. `floatLen` has disjoint
empty/cons equations and decreases structurally. `innerAcc` has an empty case
and two cons cases guarded by the exhaustive, disjoint `I ==Int J` and
`I =/=Int J`; it increments `J` exactly once and adds the proximity test only
for a distinct index. `outerAcc` has disjoint empty/cons cases, advances the
outer index, and runs the inner fold over the full input. These equations are
truthful definitions, not unconstrained oracles.

The empty-encoding simplifications overlap their ordinary empty equations with
the same result. No conflicting RHS, non-descent, or false mathematical case
was found in those summary equations. The loop claims match the real source
bodies and local-frame updates. Their problem is dependency on the input
encoding and bridges, not a separate accumulator error.

### Runtime-representation extension

`syntax ValSeq ::= floatVals(FloatSeq)` extends a fixed datatype used by
inherited `total` functions. A fresh LLVM compilation exposed concrete
non-exhaustiveness warnings for, among others,
`vsLen(floatVals(_))`, `valSeqConcat(floatVals(_), _)`, and
`hasRefVS(floatVals(_))`; see
[`stage4-kompile-summary-runner.log`](evidence/stage4-kompile-summary-runner.log).
For example, `vsLen(floatVals(.FloatSeq))` has no inherited defining equation
despite `vsLen` remaining declared total. I do not use that warning alone as a
separate target unsoundness verdict because the target does not call
`vsLen` on this form; it is narrower consistency evidence that this is not an
ordinary runtime list datatype.

### Operational bridges

The two priority-40 rules accept:

```text
#iterNext(list(floatVals(.FloatSeq))) ~> CONT
#iterNext(list(floatVals(fCons(F, FS)))) ~> CONT
```

and respectively produce `#iterDone ~> CONT` and
`#iterYield(F, list(floatVals(FS))) ~> CONT`. They preserve the arbitrary
continuation exactly, introduce no abrupt control effect, and omit no explicit
state update; relative to the *intended encoding*, their head/tail mapping is
mathematically plausible.

That is insufficient for an operational bridge. Fresh `VERIFICATION-BASE`
probes prove the encoding equations at exposed top level and the canonical
`.ValSeq`/`vCons` iterator transitions
([log](evidence/stage5-kprove-bridge-fixed.log)), while the exact bridge LHSs
are stuck without the extension:

- empty form: exit 1 and `WarnStuckClaimState`
  ([log](evidence/stage5-kprove-bridge-exact-without-extension.log));
- cons form: exit 1 and `WarnStuckClaimState`
  ([log](evidence/stage5-kprove-bridge-exact-cons-without-extension.log)).

The extended forms both prove
([log](evidence/stage5-kprove-bridge-extended.log)). Thus no universal
connection theorem covers the bridges' complete match domain. The ground entry
witness in Stage 4 shows the false reachability conclusion they enable, so
this is a material Gate A failure rather than an unlabeled evidence gap.

### Opaque values and priorities

`subF`, `absF`, and `floatLt` are supplied, result-bearing opaque functions for
Haskell proof and have concrete LLVM equations. The program execution and
`innerAcc` use the same fixed primitives. They are therefore an explicit
low-level supplied-semantics boundary, not candidate-created task-answer
oracles. The theorem is conditional on their supplied interpretation; finite
LLVM/Python tests support but do not universally prove the CPython bridge.

No other priority rule or unused supplied construct contributes to target
closure. The only proof-local priority rules are the two failing iterator
bridges.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not reused. The reviewer mutation changes
only the target result from
`outerAcc(false, 0, INPUT, INPUT, THRESHOLD)` to `true`, in a distinct module
`AUDIT-FALSE-SPEC`. It is demonstrably false at the satisfying empty input:
the original summary and both Python implementations return false.

The generated and preserved mutation is
[`audit-false-spec.k`](evidence/audit-false-spec.k). `kprove --dry-run` exited
0 and produced the backend command, establishing that the mutation parsed and
built ([log](evidence/stage6-false-mutation-dry-run.log)). Actual proof exited
1 with `WarnStuckClaimState`; the residual says the terms unify but the
condition implication fails and exhibits the unmet equality
`true = outerAcc(false, 0, INPUT, INPUT, THRESHOLD)`
([log](evidence/stage6-false-mutation-proof.log)).

This is a meaningful expected proof failure, not a parser error, missing
import, timeout, unreachable mutation, or unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

What the successful reachability run establishes precisely is:

> Under `VERIFICATION`—the trusted supplied MPY semantics plus the candidate's
> `FloatSeq` encoding, summary equations, simplifications, and iterator
> bridges—the exact submitted function body, when called on
> `list(floatVals(INPUT))`, reaches
> `outerAcc(false, 0, INPUT, INPUT, THRESHOLD)` with the target's stated final
> cells, assuming the reachability/partial-correctness interpretation.

It does **not** establish that statement for the fixed runtime list
representation or for execution under the unextended supplied semantics.

Trust and assumption ledger:

| Boundary | Effect | Assessment |
|---|---|---|
| K v7.1.293 prover/backends and K builtins | Foundation for all machine results | Necessary toolchain trust |
| Trusted supplied MPY semantics | Defines language, state, calls, loops, floats | Acceptable selected semantics; integrity verified |
| Trusted `py2mpy.py` | Connects Python source to submitted MPY | Acceptable; exact regeneration and KORE AST checks passed |
| `subF`, `absF`, `floatLt` | Determine proximity branch and returned Boolean | Acceptable named supplied opaque boundary; concrete and differential evidence is finite |
| `floatLen`, `innerAcc`, `outerAcc` | Mathematical summary/postcondition | Truthful exhaustive recursive definitions |
| Loop circularities | Summarize the two real loops | Body/state shape is adequate, but closure depends on illegitimate bridges |
| `floatVals` as a `ValSeq` constructor | Replaces canonical runtime list representation | Concerning and target-critical |
| Two iterator bridge rules | Turn fixed-stuck proof values into yielded/done iteration | Illegitimate; no connection theorem and a ground false-conclusion witness |
| Differential and LLVM tests | Support source equivalence and concrete summary interpretation | Strong finite evidence only; not a K proof substitute |

Stages 1 and 2 pass. Stage 3 confirms genuine `#Top` under the extended theory.
Stage 6 confirms result constraint. Nevertheless, Stages 4 and 5 fail the
mandatory real-program soundness gate: the theorem proves execution of a
substituted proof representation using rules that add behavior absent from the
fixed semantics. This falls directly within `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
