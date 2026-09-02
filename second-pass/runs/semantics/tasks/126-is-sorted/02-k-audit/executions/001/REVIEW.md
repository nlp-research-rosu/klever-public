# Independent adversarial audit: 126-is-sorted

## Decision

The candidate's sources rebuild, and both submitted claims print `#Top`.
Nevertheless, this is not a legitimate proof of the submitted program. The
entry theorem is copied verbatim into `verification.k` as a priority-10 rewrite,
so the prover can replace the initial call with the desired result before
executing the function. The proof also has no source dependency on
`solution.mpy`: a syntactically valid mutation changing the submitted function
to `return False` still rebuilds the proof and produces `#Top`.

The separately reported loop proof does not repair this. It relies materially
on another operational bridge that replaces the entire loop body with the
desired state update. No bridge-free connection claim proves that this summary
is the result of executing the supplied semantics. Static arithmetic inspection
suggests that summary is truthful on the claimed ordinary-local frame, so I do
not label its equation mathematically false; the defect is that the candidate
assumes the key execution connection instead of proving it.

These are candidate defects, not infrastructure uncertainty. The trusted
supplied-semantics mount is present and internally consistent, and the K
toolchain rebuilt and ran normally.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` exists as required. There is no mode/mount
contradiction.

I recursively compared candidate and trusted semantics paths, entry types,
permissions, symlink targets, and bytes. The two trees are identical; there are
no missing, additional, mistyped, changed, or symlinked entries inside
`reference-semantics/`. The candidate's `prompt.py` and `py2mpy.py` are also
byte-identical to the trusted files:

- `prompt.py`: SHA-256
  `050a2b9defc209aa64d0777939ff3387ee7db918434d818789eab7b36578b7ca`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Evidence:

- `/audit-output/evidence/stage1/mount-and-artifact-inventory.log`
- `/audit-output/evidence/stage1/trusted-input-integrity.log`
- `/audit-output/evidence/stage1/source-artifacts.log`

The requested provenance artifacts `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are all missing. No structured
generation trace is present. This prevents checking the generation narrative,
but it does not prevent independent source reconstruction. The candidate also
contains `kore-exec.tar.gz`, `__pycache__/solution.cpython-310.pyc`, and no
source-level `PROOF.md`; I did not use the archive or bytecode.

All execution used fresh sources below `/tmp/audit-work`. In particular, the
scratch manifest contained no candidate `*-kompiled` directory, cache, bytecode,
or archived backend:

- `/audit-output/evidence/stage3/fresh-source-manifest.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite list of nonnegative integers, return true exactly when:

1. adjacent elements are nondecreasing; and
2. no integer occurs more than twice.

The canonical implementation makes “more than 1 duplicate” precise by
rejecting a count greater than two, then checking all adjacent `<=`
comparisons. The empty list is true by the canonical implementation's `all`
semantics.

### Candidate implementation

`solution.py` scans left to right with:

- `result`, which is set false on a descent and never restored;
- `previous`, initially zero; and
- `repeats`, the length of the current equal run, with values over two setting
  `result` false.

On the promised nonnegative domain, the initial comparison against zero is
correct. If a list is nondecreasing, all occurrences of one value are
contiguous, so limiting equal runs to two is equivalent to the canonical count
condition. On negative inputs the initial zero matters: `[-1]` returns false in
the candidate and true in the canonical implementation. This is outside the
stated domain and confirms that the domain restriction is material.

### Translation identity

I regenerated the MPY program with:

```text
python3 /reference/py2mpy.py /candidate/solution.py
```

The regenerated file is byte-identical to submitted `solution.mpy`; both have
SHA-256
`50bbea9e74cff486c6dd53e951326b22fdec005065fc2f7f225388df2693d1fe`.
See `/audit-output/evidence/stage2/translator-byte-identity.log`.

### Independent differential test

`/audit-output/evidence/stage2/differential_test.py` independently imports the
trusted canonical entry point and candidate entry point. It checks:

- all eight documented examples;
- 14 explicit empty, zero, first-element, descent, equality, and repeat-count
  boundary cases;
- every list of length 0 through 7 over values 0 through 4 (97,656 cases); and
- 10,000 deterministic generated lists of length 0 through 30 over values 0
  through 20.

All branches and the repeat thresholds below 2, at 2, and at 3 were observed.
There were zero mismatches in 107,678 in-domain comparisons. The command exited
0. The complete scope and output are in
`/audit-output/evidence/stage2/differential-test.log`. This is strong finite
fidelity evidence, not a K proof.

## 3. Clean proof reconstruction

Toolchain:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

`kup` was absent, but independently installed `/usr/bin/kompile`,
`/usr/bin/kprove`, and `/usr/bin/krun` all worked. See
`/audit-output/evidence/stage3/toolchain.log`.

I copied the trusted semantics tree, candidate proof sources, and freshly
translated MPY sources to `/tmp/audit-work/reconstruction`. I did not copy or
use candidate compiled definitions.

### Concrete definition

The following fresh LLVM build exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The freshly translated `smoke.mpy` then ran to a final configuration with
`.K`, empty stack, `NoExc`, and exit code 0. Its assertions cover empty, sorted,
descent, two-equal, and three-equal cases. Evidence:

- `/audit-output/evidence/stage3/kompile-runtime.log`
- `/audit-output/evidence/stage3/krun-smoke.log`

The compiler emitted non-exhaustiveness warnings for several unused supplied
helpers. None of those helpers is on this program's execution path.

### Loop claim

Fresh Haskell compilation of module `IS-SORTED-VERIFICATION` exited 0. Fresh
proof of the only loop claim also exited 0 and printed `#Top`:

```text
kprove spec.k --definition loop-verification-kompiled \
  --spec-module IS-SORTED-LOOP-SPEC --output pretty
```

Evidence:

- `/audit-output/evidence/stage3/kompile-loop-proof.log`
- `/audit-output/evidence/stage3/kprove-loop.log`

### Entry claim

Fresh Haskell compilation of `IS-SORTED-WITH-LOOP-LEMMA` exited 0. Fresh proof
of the only entry claim exited 0 and printed `#Top`:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module IS-SORTED-SPEC --output pretty
```

Evidence:

- `/audit-output/evidence/stage3/kompile-entry-proof.log`
- `/audit-output/evidence/stage3/kprove-entry.log`

Thus the dynamic reconstruction gate succeeds. The following stages explain
why those `#Top` results do not constitute the required real-program proof.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

The loop precondition places execution at a `#loop` over the proof-local list
carrier `intsToVals(IS)`, followed by the exact manually restated loop body,
`Return(Name("result"))`, and `#endcall`. The current frame contains:

- boolean `result = OK`;
- integer `previous = PREV`;
- integer `repeats = COUNT`;
- integer `number`;
- the proof-only `"$plain"` marker; and
- arbitrary disjoint ordinary locals.

The current environment equals the frame saved on the caller stack; the frame
is absent from `BASE`; and the listed local names and cell marker are disjoint
from `LOCALS`.

The postcondition says the remaining sequence is folded by `scanAll`, its
boolean component is returned to arbitrary caller continuation `CONT`, the
callee scope is deleted, the caller environment and saved scope location are
restored, the stack frame is popped, and `ret` is reset.

A concrete satisfying state is:

```text
FRAME=SAVED=1, CALLER=0, CURRENT=2, OK=true,
PREV=1, COUNT=1, NUMBER=1, IS=[2,2], LOCALS=.Map,
BASE containing only frames 0 and -1, CONT=.K, STACK=.List.
```

All disjointness and equality side conditions hold, and the claimed scan result
is true.

### Entry claim in plain language

The entry precondition has no `requires` clause. For any finite K `IntSeq`
`INPUT`, it starts at an application of the manually defined
`isSortedClosure` to `list(intsToVals(INPUT))`, in a standard-looking initial
configuration: environment 0, module and builtins frames, scope location 1,
empty heap and stack, `noRet`, and `NoExc`.

The postcondition constrains the returned K value to
`scanResult(scanAll(true, 0, 0, INPUT))` and requires all listed state cells to
return to their initial values. It is not a free variable, tautology, or
one-way implication. The false-postcondition test in Stage 6 confirms this
result constraint.

The formal input is broader than the prompt: it permits all K integers. On
nonnegative sequences, the fold is exactly the intended nondecreasing/run-limit
predicate. On negative sequences, it exactly follows the candidate's
zero-initialized scan rather than the prompt's excluded behavior.

Ground substitutions in
`/audit-output/evidence/stage4/concrete_claim_witnesses.py` compare the K fold,
canonical Python, and candidate Python for empty, zero, descent, and repeat
boundaries. All eight in-domain witnesses agree. The recorded `[-1]` witness
has K/candidate false and canonical true. See
`/audit-output/evidence/stage4/concrete-claim-witnesses.log`.

### Failure to pin the submitted program

The `<k>` cell does not load or execute `Module(FuncDef(...))` from
`solution.mpy`. Instead, `verification.k:22-32` manually defines a macro
`isSortedClosure`, and the claim directly applies that value. The macro happens
to restate the current submitted function body accurately, but neither
`spec.k` nor `verification.k` reads `solution.py` or `solution.mpy`.
`/audit-output/evidence/stage4/proof-source-dependency.log` finds only a comment
mentioning `solution.mpy`.

I tested body sensitivity with a fresh, syntactically valid MPY mutation:

```text
Return(Bool(false))
```

The mutated program parses and loads under the fresh runtime definition, and
the loaded closure visibly contains `Return(Bool(false))`. I then performed a
fresh proof build in a directory containing that mutated `solution.mpy`, with
the unchanged candidate proof sources. The entry proof still exited 0 and
printed `#Top`.

Evidence:

- mutation: `/audit-output/evidence/stage4/solution-body-mutated.mpy`
- concrete parse/load: `/audit-output/evidence/stage4/mutated-body-parses.log`
- fresh build: `/audit-output/evidence/stage4/kompile-mutated-body-proof.log`
- unchanged `#Top`: `/audit-output/evidence/stage4/kprove-mutated-body.log`

For the satisfying in-domain input `[]`, that mutated program returns false
while the claimed scan result is true. This is a concrete source-pinning
counterexample. It does not allege that the current candidate Python function
is incorrect; it demonstrates that the reported proof is insensitive to the
program artifact it purports to prove.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/stage5/inventory_k.sh` inventories every K source file,
hash, module/import, configuration, syntax declaration, context, rule, claim,
and relevant attribute (`function`, `functional`, `total`, `symbol`, `macro`,
priority, simplification, `owise`, and `concrete`). Its complete 1,600-line
result is:

- `/audit-output/evidence/stage5/exhaustive-k-inventory.txt`
- command log:
  `/audit-output/evidence/stage5/exhaustive-k-inventory.log`

Totals are 732 rules, 234 syntax declarations, two claims, one configuration,
and five explicit contexts. Of those, the candidate proof extension contributes
37 rules and seven syntax declarations; the supplied semantics contributes 695
rules and 227 syntax declarations.

The following table accounts for every supplied-semantics rule by file. “Fixed”
means the file is byte-identical to the trusted supplied tree and therefore
defines the selected semantics level; it does not confer trust on
`verification.k`.

| Supplied file | Rules / syntax | Audit decision |
|---|---:|---|
| `semantics.k` | 0 / 0 | Fixed module aggregation; `MPY` is used for proof and `MPY-KRUN` for concrete execution. |
| `assert.k` | 3 / 0 | Fixed, smoke-only; absent from target call. |
| `bool.k` | 13 / 0 | Fixed; target uses boolean literals/conjunctions. Relevant cases agree with K Bool operations. |
| `builtins.k` | 137 / 38 | Fixed; individual builtins are not called by the candidate function. |
| `call.k` | 21 / 3 | Fixed; closure application, frame allocation, left-to-right argument binding are relevant. |
| `comprehension.k` | 7 / 3 | Fixed and unreachable from target syntax. |
| `concrete.k` | 16 / 5 | Fixed; imported by `MPY-KRUN`, not the proof's `MPY` module. |
| `controls.k` | 34 / 3 | Fixed; assignment, augmented assignment, `If`, and `For` rules are relevant and were checked against the proof bridges. |
| `core.k` | 46 / 37 | Fixed; configuration, sequencing, name lookup, literals, and shared list helpers are relevant. |
| `dict.k` | 28 / 12 | Fixed and unreachable from target syntax. |
| `float.k` | 121 / 34 | Fixed and unreachable; all float opaque symbols are irrelevant to this integer program. |
| `functions.k` | 15 / 4 | Fixed; function definition, parameter binding, return, frame pop, state restoration are relevant. |
| `int.k` | 16 / 1 | Fixed; `+`, `<`, `==`, and `>` cases used by the program agree with integer mathematics. |
| `iter.k` | 0 / 1 | Fixed iterator protocol declaration. |
| `list.k` | 27 / 5 | Fixed; ordinary `vCons` list iteration is relevant to the real representation. |
| `methods.k` | 75 / 27 | Fixed and unreachable from target syntax. |
| `operators.k` | 10 / 0 | Fixed; comparison evaluation order and dispatch are relevant. |
| `range.k` | 6 / 2 | Fixed and unreachable from target syntax. |
| `set.k` | 12 / 6 | Fixed and unreachable from target syntax. |
| `sort.k` | 19 / 6 | Fixed and unreachable from target syntax. |
| `str.k` | 28 / 5 | Fixed and unreachable from target behavior. |
| `subscript.k` | 40 / 15 | Fixed and unreachable from candidate algorithm. |
| `syntax.k` | 0 / 16 | Fixed declarations for all submitted MPY constructs. |
| `tuple.k` | 21 / 4 | Fixed target binding declaration/rule is relevant to `For`; tuple operations are otherwise unreachable. |

The supplied opaque/symbol boundary consists of `md5hexCodes`, the float
helpers listed in `float.k`, and `sortVS`/`sortKeyVS`; the exhaustive inventory
lists each exact declaration. None can occur in this program or its
postcondition. The proof-local `intsToVals` is separately discussed below.

### Used-syntax coverage and control flow

| Submitted construct | Declaration | Fixed behavior used |
|---|---|---|
| `Module`, statement list | `syntax.k:56,61` | `core.k:124-127` loads and sequences statements. |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` creates the closure. |
| `Name` | `syntax.k:12` | `core.k:130-154` walks the scope chain. |
| `Int`, `Bool` | `syntax.k:9-12` | `core.k:193-196` produces K values. |
| `Assign` | `syntax.k:41` | strict RHS, then `controls.k:9-18` updates the current frame. |
| `AugAssign` | `syntax.k:44` | strict RHS, local lookup/update in `controls.k:20-31`; integer `+` in `int.k`. |
| `If` | `syntax.k:49` | strict condition and truth branch in `controls.k:50-54`. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | left-to-right contexts in `operators.k:14-17`; integer comparisons in `int.k:22-27`. |
| `For` | `syntax.k:45` | iterable evaluated once; `controls.k:62-75` and `list.k:9-10` drive iteration and target binding. |
| `Return` | `syntax.k:50` | strict value, return state, stack/frame pop, environment restoration in `functions.k:77-90`. |
| Function application | internal `#applyK` | `call.k:69-74` allocates the frame, binds parameters, executes the body, and adds `#endcall`. |

No program-used construct lacks a fixed rule. The proof-local rules do not fill
an actual language gap; they accelerate or replace already modeled execution.

### All 37 `verification.k` rules

1. **Lines 8 and 23 — `isSortedLoopBody` and `isSortedClosure` macros.**
   These are definitional syntactic restatements. They match the current
   translated body, but the equality is only manually maintained and does not
   pin `solution.mpy`, as the body-sensitivity test demonstrates.

2. **Line 36 — specialized closure application.** This operational bridge
   preempts `call.k:69-74`, creates a frame already populated with dummy locals
   and the proof-only `"$plain"` marker, then executes the restated body. For
   this exact closure, the dummy values are overwritten or unobserved and the
   frame is later deleted, so static state-footprint inspection found no
   target-domain false conclusion. It has no bridge-free universal connection
   theorem and is not justified merely by calling it a constructor-form
   instance.

3. **Lines 66, 71, 77, 83, and 89 — lookup shortcuts.** Line 66 is the fixed
   direct lookup specialized to marked ordinary frames. The four named variants
   return the explicit map value and are correct on the target's ordinary
   boolean/integer bindings. Their guards are broader than the `"$plain"`
   target frame. For example, on an annotated frame with
   `"result" |-> cellRef(7)`, a matching `"$cells"` marker, and heap
   `7 |-> cellV(true)`, line 71 can return the reference whereas the fixed cell
   lookup returns `true`. That is a global overbreadth witness, but the state is
   not reachable in this unannotated `is_sorted` call. I therefore record the
   narrower reuse/scope gap and do not use it as a target-domain false-result
   allegation.

4. **Lines 96 and 109 — parameter binding shortcuts.** Line 96 replaces the
   preinserted `lst`; line 109 is the fixed map update restricted to marked
   frames. They agree with fixed binding on the target frame. Guards prevent
   duplicate explicit keys.

5. **Lines 116 and 122 — loop target binding shortcuts.** The generic marked
   rule and named `number` rule perform the same current-frame update as
   `tuple.k:31-40` on the target's ordinary local.

6. **Lines 134, 140, 151, and 162 — assignment shortcuts.** The generic marked
   update and named `result`, `previous`, and `repeats` updates agree with
   `controls.k:9-11` on the target. Explicit-key map patterns and negative
   membership guards make their overlaps agree.

7. **Lines 174 and 183 — augmented-assignment shortcuts.** Both apply
   `applyBin` to the old value and new value exactly as `controls.k:20-23`.
   For the used `repeats += 1`, `int.k:9` supplies ordinary integer addition.

8. **Line 198 — direct return shortcut.** Given the claimed Boolean local, the
   fixed strict evaluation looks up that Boolean and then applies
   `functions.k:78-79`. The shortcut produces the same `retV` and `#pop`, and
   both fixed and shortcut return rules discard the function's remaining
   continuation. This is an operational bridge without a machine connection
   claim, though static inspection found no false target case.

9. **Lines 210, 226, 243, 259, 276, and 289 — direct `If` guards.** The `<` /
   `>=`, `==` / `=/=`, and `> 2` / `<= 2` guards are pairwise disjoint and
   exhaustive over K integers. Given direct integer locals, each branch is the
   result of fixed name lookup, integer comparison, Boolean truthiness, and
   `If` selection. No overlap gives conflicting right-hand sides.

10. **Line 304 — map-delete simplification.** Under
    `notBool N in_keys(BASE)`, deleting explicit key `N` from
    `(N |-> S) BASE` equals `BASE`. This is ordinary finite-map mathematics and
    matches the frame deletion performed by `#pop`.

11. **Lines 313 and 315 — `intsToVals` iterator rules.** `intsToVals` at line
    309 is an otherwise opaque proof-local `ValSeq` constructor. These rules
    decree that it iterates as empty/cons according to its `IntSeq` argument.
    They extensionally mimic `list.k:9-10`, but there is no equation or
    bridge-free theorem connecting
    `list(intsToVals(iCons(...)))` to the real
    `list(vCons(...))` representation. The program only iterates the value, so
    static inspection found no contradictory target outcome, but the input
    representation is assumed rather than connected.

12. **Line 322 — whole-loop-body operational bridge.** It consumes the exact
    restated body immediately before `#loopLbl`, preserves the label and all
    framed cells, and replaces four assignments/conditionals with:

    ```text
    result := OK and PREV <= X and nextRepeats(X,PREV,COUNT) <= 2
    previous := X
    repeats := nextRepeats(X,PREV,COUNT)
    ```

    Case analysis shows this arithmetic is truthful for Boolean `OK` and
    integer locals: descent makes `result` false; equality increments the run
    and inequality resets it to one; a run above two makes `result` false. The
    bridge admits the exact loop-label context and preserves its continuation.
    I found no false conclusion witness on the intended input domain and
    therefore do not call the equation false.

    It is nevertheless an unproved operational bridge. No claim without this
    rule establishes execution of the four real statements to the summarized
    state. Removing only this rule builds successfully, then the loop proof
    exits 1 with a meaningful stuck state at the first heated comparison:

    - diff:
      `/audit-output/evidence/stage5/no-body-summary-diff.log`
    - build:
      `/audit-output/evidence/stage5/kompile-no-body-summary.log`
    - failed proof:
      `/audit-output/evidence/stage5/kprove-no-body-summary.log`

    Thus the submitted loop `#Top` materially depends on the bridge it should
    have proved.

13. **Lines 355 and 357 — `nextRepeats`.** Equality and disequality guards are
    disjoint and exhaustive; the equations implement increment/reset and
    terminate immediately.

14. **Lines 363 and 365 — `scanAll`.** Empty/cons equations are exhaustive over
    `IntSeq`; recursion strictly descends the tail. The fold matches the
    line-322 arithmetic.

15. **Line 375 — `scanResult`.** Projects the Boolean from `scanState`; it is
    total over the normalized `ScanState` result used here.

16. **Line 380 — `isSortedContract`.** Merely names the scan initialized with
    `(true,0,0)`. It is mathematically the prompt predicate only under the
    promised nonnegative domain. The entry claim does not use this name.

17. **Line 390 — copied loop lemma rewrite.** Its configuration, conditions,
    and result restate the separately submitted loop claim. Using a proven
    reachability claim compositionally can be legitimate, but this proof of the
    lemma inherits the unproved line-322 execution summary and proof-local list
    carrier.

18. **Line 438 — exact entry theorem as a rewrite.** This is the decisive
    failure. Its left-hand side, result, and state transformation are the entry
    claim itself, generalized only from concrete `builtinsScope` to an arbitrary
    `BUILTINS:Scope`. It has priority 10, so it preempts the priority-40 call
    bridge and all fixed execution. The false-postcondition residual in Stage 6
    visibly starts after this rule has rewritten the call to `scanResult`.

    No separate, bridge-free entry/setup claim proves this rewrite from the
    fixed call and loop behavior. The rule assumes the theorem the entry
    `kprove` invocation purports to establish. Removing exactly this rule still
    builds, but a bounded diagnostic made no progress for over three minutes
    before reviewer interruption (exit 130):

    - diff:
      `/audit-output/evidence/stage5/no-entry-bridge-diff.log`
    - build:
      `/audit-output/evidence/stage5/kompile-no-entry-bridge.log`
    - bounded command and status:
      `/audit-output/evidence/stage5/kprove-no-entry-bridge.log` and
      `/audit-output/evidence/stage5/kprove-no-entry-bridge.status.txt`

    That interrupted diagnostic is not treated as proof failure or
    infrastructure failure. Reliance is established directly by the rule's
    exact match, highest priority, the Stage 6 residual, and the successful
    program-body mutation.

The principal rejection is therefore not an unsupported allegation that a
particular arithmetic equation is false. It is the witnessed source-pinning
failure and theorem-as-operational-axiom structure, both explicitly
disallowed for a real-program proof.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I wrote a fresh distinct module,
`/audit-output/evidence/stage6/spec-vacuity.k`, changing the entry result to:

```text
notBool scanResult(scanAll(true, 0, 0, INPUT))
```

This is demonstrably false for the satisfying precondition instance
`INPUT=.IntSeq`: the program/fold result is true and the mutation demands
false.

The exact command was:

```text
timeout --signal=TERM --kill-after=5s 60s \
  kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module IS-SORTED-VACUITY-SPEC --output pretty
```

The spec parsed and built, reached the result obligation, and exited 1 with
`WarnStuckClaimState`. Its residual requires equality between
`scanResult(...)` and its negation. This is the expected unmet obligation, not a
parser error, missing import, timeout, or unrelated crash. Complete evidence is
`/audit-output/evidence/stage6/kprove-false-mutation.log`.

The candidate theory is therefore discriminating with respect to its assumed
scan result. This non-vacuity pass does not establish that the result came from
executing `solution.mpy`.

## 7. Proven versus assumed accounting

### What the successful reachability runs actually establish

Under the supplied semantics plus all rules in `verification.k`:

1. a loop over the proof-local `intsToVals` carrier reaches the scan result,
   because iteration is defined for that carrier and the exact loop body is
   replaced by the scan-step bridge; and
2. an application of the manually restated `isSortedClosure` reaches the scan
   result, because an imported priority rewrite states exactly that transition.

The entry `#Top` does not independently derive the entry transition from the
fixed supplied semantics. It confirms closure under a theory that already
contains the target transition.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted supplied semantics tree | All fixed execution | Acceptable by the rendered `SUPPLIED_SEMANTICS` boundary; candidate tree is byte-identical. |
| K parser/compiler/Haskell/LLVM backends v7.1.337 | All dynamic evidence | Normal tool trust; fresh rebuilds and expected positive/negative behavior were observed. |
| Supplied opaque float, MD5, and sort symbols | Potential values in unrelated programs | Acceptable here because none is reachable from the submitted integer/list program or claims. |
| Manual `isSortedClosure` and `isSortedLoopBody` restatement | Which program body is reasoned about | Concerning and ultimately inadequate: current text matches, but the proof has no dependency on `solution.mpy`; body mutation leaves `#Top` unchanged. |
| `intsToVals` plus its iterator rules | Symbolic input and every loop iteration | Unproved empirical/mathematical bridge to real `vCons` lists; locally plausible for iteration, but no universal connection theorem. |
| Whole-body rule at `verification.k:322` | Result, previous value, repeat count, loop induction | Illegitimate as proof evidence without a bridge-free execution claim; removal makes the loop proof stuck. Static case analysis supports truth but cannot substitute for the required K connection. |
| `nextRepeats`, `scanAll`, `scanResult` | Formal postcondition | Acceptable pure mathematical definitions with exhaustive guards/descent. |
| Copied loop claim as line-390 rewrite | Entry composition | Conditional on the loop proof, which itself depends on the body bridge. |
| Exact entry rule at `verification.k:438` | Entire final theorem, control, result, and state | Illegitimate: it is the target theorem installed as an operational axiom and preempts real execution. |
| Differential testing | Candidate-to-canonical intent bridge on sampled inputs | Strong finite support only; it neither proves universal equivalence nor repairs K execution pinning. |
| Informal nonnegative-domain argument | Scan fold to natural-language property | Mathematically straightforward and supported by tests, but downstream of the failed real-program proof gate. |

### Gate summary

- Fresh dynamic reconstruction: **PASS** — both submitted claims exit 0 with
  `#Top`.
- Real-program soundness/pinning: **FAIL** — actual MPY body is not executed or
  dependency-pinned; key execution and the entire entry theorem are assumed as
  rewrites.
- Intent adequacy of the Python implementation on nonnegative integers:
  **PASS as finite plus informal evidence**, with the negative-input exclusion
  explicitly material.
- Fresh non-vacuity: **PASS** — opposite result is rejected for the expected
  obligation.
- Trust/evidence auditability: **FAIL for proof legitimacy** — missing
  provenance files and, materially, no universal connection claims for the
  result-bearing operational bridges.

The correct decision is `FAIL / NOT_LEGIT`: successful reconstruction and
non-vacuity cannot rescue a proof that assumes its entry theorem and remains
valid after a material mutation of the submitted program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
