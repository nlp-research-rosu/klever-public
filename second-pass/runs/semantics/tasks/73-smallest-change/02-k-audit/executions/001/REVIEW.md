# Adversarial proof review: 73-smallest-change

The reconstructed K files compile and all three submitted positive claims print
`#Top`, but this is not a legitimate proof of the submitted program. The
result-bearing claim proves a proof-local `#targetCall` recurrence. Two
priority-40 rules replace real closure execution with that recurrence, and no
bridge-free theorem connects the recurrence to the submitted `solution.mpy`.
The proof does not load or reference `solution.mpy`; a material mutation of that
file leaves a freshly rebuilt proof at `#Top`.

This is a candidate failure, not an audit-infrastructure failure. The rendered
mode is `SUPPLIED_SEMANTICS`, the required trusted semantics mount exists, the K
toolchain runs, and the candidate semantics tree exactly matches the trusted
tree.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required for
`SUPPLIED_SEMANTICS`. The reviewer-authored integrity checker recursively
compared names, entry types, symlink status, and SHA-256 content for the trusted
and candidate trees. Both contain 25 entries. There are no missing, additional,
mistyped, changed, or symlinked candidate semantics entries:

- Command and result: [stage1-semantics-integrity.log](evidence/stage1-semantics-integrity.log)
- Checker source: [check_integrity.py](evidence/check_integrity.py)

The mount therefore does not contradict the rendered semantics mode. This is
not an `AUDIT_ERROR` case.

### Prompt, translator, and required artifacts

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256 `a91bec8bc0f85124b068553a370cb6c2b8564b2e298289f578e913cb77f619bf`).
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
(SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
See [stage1-trusted-file-comparison.log](evidence/stage1-trusted-file-comparison.log).

The candidate contains regular-file `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, `prompt.py`, and `py2mpy.py`. No candidate entry is a
symlink. The complete candidate inventory is in
[stage1-artifact-inventory.log](evidence/stage1-artifact-inventory.log).
Candidate-built `__pycache__` content was not used.

The following requested provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation-trace file is present. This is a provenance/evidence
gap, not a malformed trusted mount. Evidence:
[stage1-required-claims-files.log](evidence/stage1-required-claims-files.log).

All execution inputs were copied to `/tmp/audit-work/audit73`; candidate
compiled definitions and caches were ignored. Initial scratch hashes are in
[stage1-scratch-copy-hashes.log](evidence/stage1-scratch-copy-hashes.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

For an integer array, the answer is the number of mirrored index pairs
`(i, n-1-i)` whose values differ. Every unequal pair needs at least one change,
one change to either member repairs that pair, and the pairs are disjoint.
Consequently this mismatch count is exactly the minimum number of element
changes needed to make the array palindromic.

The trusted canonical implementation iterates over the first half of the array
and increments once for each unequal mirrored pair.

The candidate uses a recursive helper on an inclusive interval:

- `left >= right` returns zero;
- an unequal outer pair contributes one;
- both branches recurse on `left + 1, right - 1`.

Mathematically this computes the same mismatch count for integer arrays when
the Python call returns normally.

### Trusted retranslation

The trusted translator regenerated the submitted AST with exit 0. The
regenerated and submitted `solution.mpy` files are byte-identical, both with
SHA-256
`3149f2b775bce3cf3815542741c6b54072b1e070bbd9af809d6f9d01da78b06f`.
Exact command and result:
[stage2-translator-byte-identity.log](evidence/stage2-translator-byte-identity.log).

### Independent differential test

The reviewer-authored test imports `/reference/canonical.py` and the isolated
candidate `solution.py` independently. Its corpus contains:

- all three documented examples;
- explicit empty, singleton, equal-pair, unequal-pair, odd-center, inner/outer
  branch, negative, and large-integer boundaries;
- every array of lengths 0 through 8 over `{-1, 0, 1}` (9,841 cases);
- 2,000 deterministic random arrays of lengths 0 through 80 over nine
  representative/boundary integers;
- two length-2,200 recursion-boundary arrays.

The full 11,853-input corpus is preserved in
[differential-inputs.json](evidence/differential-inputs.json); generator/oracle
source is [differential_test.py](evidence/differential_test.py).

There were 11,851 matches and two material divergences. With CPython 3.10.12's
default recursion limit 1,000:

- `[0] * 2200`: canonical returns `0`; candidate raises `RecursionError`.
- A 2,200-element all-mismatch case: canonical returns `1100`; candidate raises
  `RecursionError`.

The differential command therefore intentionally exits 1 with two recorded
mismatches; see [stage2-differential.log](evidence/stage2-differential.log).
The prompt gives no maximum length, so this is a real Python
implementation/intent limitation. It is not the primary legitimacy failure,
which is independently established by the K pinning audit below.

## 3. Clean proof reconstruction

K, `kompile`, `krun`, and `kprove` are independently installed at
`/usr/bin`; all report K v7.1.337. See
[stage3-tool-versions.log](evidence/stage3-tool-versions.log).

### Concrete definition

The concrete definition was freshly built from the isolated, integrity-checked
source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit was 0. The warnings are bounded and preserved in
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).

The trusted translator also regenerated `concrete-tests.mpy` byte-identically
from `concrete-tests.py`:
[stage3-concrete-test-translation.log](evidence/stage3-concrete-test-translation.log).
Running that regenerated program with the fresh LLVM definition exited 0,
ended with `<k> .K </k>`, `NoExc`, and exit code 0. The six assertions cover
empty, singleton, unequal pair, and the three documented examples:
[stage3-krun-regenerated-concrete-tests.log](evidence/stage3-krun-regenerated-concrete-tests.log).

### Proof definition and positive claims

The proof definition was freshly built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit was 0; see [stage3-kompile-proof.log](evidence/stage3-kompile-proof.log).

The aggregate command and every claim selected independently exited 0 and
printed `#Top`:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.public-entry-bridge
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.helper-entry-bridge
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.smallest-change-correct
```

Evidence:

- [stage3-kprove-all.log](evidence/stage3-kprove-all.log)
- [stage3-kprove-public-entry.log](evidence/stage3-kprove-public-entry.log)
- [stage3-kprove-helper-entry.log](evidence/stage3-kprove-helper-entry.log)
- [stage3-kprove-correctness.log](evidence/stage3-kprove-correctness.log)

Thus fresh verification under the candidate's extended theory succeeds. That
does not establish that the extensions describe the real program.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

`public-entry-bridge` has no explicit precondition. From an application of the
proof-local `#mainClosure` to `ref(H)`, with any continuation and otherwise
framed configuration, it claims one can reach
`#targetCall(mainCall, ref(H), 0, 0)` with the same continuation.

`helper-entry-bridge` likewise has no explicit precondition. It replaces an
application of the proof-local `#helperClosure` to `(ref(H), L, R)` with
`#targetCall(helperCall, ref(H), L, R)`.

`smallest-change-correct` starts only from the synthetic
`#targetCall(KIND, ref(H), L, R)`. It requires:

- heap location `H` contains `list(VS)`;
- `<ret>` is `noRet`, `<exc>` is `NoExc`, and `<exit-code>` is zero;
- for `mainCall`, `targetValid` is unconditionally true;
- for `helperCall`, `0 <= L <= len(VS)` and `-1 <= R < len(VS)`.

It claims the target reduces to:

- `changeRange(VS, 0, len(VS)-1)` for `mainCall`;
- `changeRange(VS, L, R)` for `helperCall`;

with the continuation and every explicitly listed non-`<k>` cell unchanged.
This is an exact result constraint, not a free variable or implication-only
postcondition.

### Satisfiability and ground substitution

The preconditions are satisfiable:

- Public bridge/main target: `H=0`, `VS=[1,2]`, empty continuation. The claimed
  result is `1`; both trusted canonical and candidate Python return `1`.
- Helper bridge/helper target: `H=0`, `VS=[1,2,3,4]`, `L=1`, `R=2`. The helper
  validity predicate is true and the claimed result is `1`. Candidate
  `_smallest_change` returns `1`; the canonical algorithm on the inclusive
  slice `[2,3]` also returns `1`.

Exact K-shaped states and Python/formula checks are in
[stage4-ground-witnesses.log](evidence/stage4-ground-witnesses.log), produced
by [claim_witnesses.py](evidence/claim_witnesses.py).

### Failure to execute or pin `solution.mpy`

No `requires`, import, claim, build command, or proof command consumes
`solution.mpy`. No claim starts from `Module(...)`, loads the submitted module,
looks up its installed `smallest_change` binding, or executes its submitted
closure body. Instead:

1. `verification.k:7-49` manually duplicates two AST bodies and constructs two
   proof-local closure constants.
2. Priority-40 rules at `verification.k:73-86` rewrite applications of those
   closures directly to `#targetCall`.
3. Rules at `verification.k:90-116` implement the answer recurrence directly.
4. The result claim starts at that recurrence, not at either submitted
   function.

The textual body copies happen to match the submitted AST, but that is not a
machine-checked program connection.

A direct body-sensitivity experiment makes the gap observable. In scratch,
the public function in `solution.mpy` was changed to `Return(Int(999))`.
The mutated program SHA-256 was
`54a2ce78cfdbaf15d5b34df5415c52579c62d0d47cef53500ab85efefb9df532`,
distinct from the submitted SHA-256. With the proof source left unchanged, a
fresh Haskell definition built successfully and
`SPEC.smallest-change-correct` still printed `#Top`:

- [stage4-body-sensitivity-hashes.log](evidence/stage4-body-sensitivity-hashes.log)
- [stage4-body-sensitivity-build.log](evidence/stage4-body-sensitivity-build.log)
- [stage4-body-sensitivity-proof.log](evidence/stage4-body-sensitivity-proof.log)

For the satisfying intended-domain input `[1,2]`, that mutated program returns
`999`, while the unchanged theorem concludes `1`. This is the required
concrete false-conclusion witness for treating the synthetic theorem as a
theorem about an arbitrary/current `solution.mpy`: the proof does not observe
the program body at all.

This experiment does not assert that the hand-written recurrence is
mathematically false for the original small-input algorithm. It establishes
the narrower and decisive defect: the proof is insensitive to, and therefore
does not pin, the program it purports to verify.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer rebuilt an exhaustive source inventory for all K files in the
supplied semantics, `verification.k`, and `spec.k`. It contains 1,099 records:

- 711 ordinary rules;
- 237 syntax declarations;
- 47 priority-attributed declarations/rules;
- 149 function-attributed declarations;
- 110 total-attributed declarations;
- 25 symbol declarations, 22 with `no-evaluators`;
- 8 macro-attributed declarations;
- 26 `owise` declarations/rules;
- one configuration, five contexts, and three claims;
- zero `simplification` declarations;
- zero `functional` declarations.

Every record includes its location, normalized source, attributes, and audit
classification:
[k-rule-inventory.md](evidence/k-rule-inventory.md). The generating script and
count log are [k_rule_inventory.py](evidence/k_rule_inventory.py) and
[stage5-rule-inventory-generation.log](evidence/stage5-rule-inventory-generation.log).

The 25-file candidate semantics tree is the exact supplied baseline. Under the
rendered mode it is the selected fixed semantics, not a candidate-generated
language definition. Its rules are classified as accepted fixed
`SUPPLIED_SEMANTICS`; candidate-specific proof conclusions are not blessed by
that integrity result. All unused baseline facilities remain outside this
program's theorem. Every construct used by `solution.mpy` is separately mapped
to syntax, evaluation/control, call, state, and result rules in
[used-construct-map.md](evidence/used-construct-map.md).

### Relevant fixed semantics

The submitted program needs `Module`, statement sequencing, `FuncDef`,
`Params`, `Name`, `Call`, user-call frames, parameter binding, `Return`, `If`,
integer literals/arithmetic/comparison, list heap dereference, subscript, and
`len`.

The fixed call path evaluates callee and arguments left-to-right, then
`call.k:69-74` allocates a scope, changes `<env>`/`<scopeLoc>`, pushes a frame,
binds parameters, runs the body, and uses `functions.k:78-90` to return, pop,
restore the caller, and deallocate the scope. Recursive calls repeat this path.
The candidate priority rules preempt that path exactly at `#applyK`.

The relevant supplied configuration has `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The synthetic target rules touch only `<k>` and read the list
heap. That makes the target theorem easy to frame but does not prove equivalence
to the skipped binding, control, and call behavior.

### Candidate proof-local declarations and rules

The proof-local inventory was assessed as follows:

- `#helperBody`/`#mainBody` macros: faithful textual AST copies for this
  candidate, but manually maintained and not imported from the program.
- `#helperClosure`/`#mainClosure`: faithfully package those copied bodies with
  the intended parameter lists and definition scope; still synthetic entries.
- `changeRange`: two disjoint guards (`L >= R` and `L < R`), complete over
  integers. The recursive width decreases by two. Its equations correctly
  count unequal mirrored endpoints for in-bounds intended-domain indices.
- `TargetCall`, `#targetCall`, `#addMismatch`: fresh proof-control syntax.
- Main target rule: directly changes the wrapper target into a helper target at
  indices `0` and `len(VS)-1`.
- Helper base/recursive target rules: disjoint `L >= R`/`L < R` guards and the
  correct mismatch-bit recurrence for in-bounds integer arrays.
- `#addMismatch`: correctly adds zero or one after the inner result.
- `targetAnswer`: constructor-disjoint equations that name the same recurrence.
- `targetValid`: total, constructor-disjoint, and satisfiable; helper bounds
  keep every recursive subscript in bounds.

No false mathematical equation or overlap witness was found for these
recurrence/summary functions on the intended integer-array domain. They are not
rejected as globally false rules. Their defect is their role as a substituted
implementation.

### Operational bridge audit

The two rules at `verification.k:73-86` are operational bridges, regardless of
their comments:

- **Matched context:** exact proof-local closure constructors and arities at
  `#applyK`, after argument evaluation, but with arbitrary continuation and all
  other cells omitted/framed.
- **Priority:** 40, preempting the ordinary closure-dispatch rule.
- **State skipped:** environment change, scope insertion/deletion,
  scope-location movement, stack push/pop, parameter bindings, name lookup,
  builtin `len`, condition/subscript evaluation, recursive closure lookup and
  call, return state, and control unwinding.
- **Result influence:** total. The bridge selects `#targetCall`, whose
  recurrence and `targetAnswer` determine the final result.
- **Purported justification:** the two entry claims import the bridge rules
  themselves. Those claims close by the same rewrite they are supposed to
  justify and are not bridge-free universal connection theorems.
- **Connection theorem:** absent.

A bridge-free variant removed only these two rules. It built successfully:
[verification-no-bridges.k](evidence/verification-no-bridges.k),
[spec-no-bridges.k](evidence/spec-no-bridges.k), and
[stage5-no-bridges-build.log](evidence/stage5-no-bridges-build.log).

Both real-entry connection claims then failed with meaningful stuck states at
the fixed call-frame/`#bindP` execution rather than reaching `#targetCall`:

- [stage5-no-bridges-public-proof.log](evidence/stage5-no-bridges-public-proof.log)
- [stage5-no-bridges-helper-proof.log](evidence/stage5-no-bridges-helper-proof.log)

In the same bridge-free definition, the synthetic
`smallest-change-correct` claim still printed `#Top`:
[stage5-no-bridges-synthetic-proof.log](evidence/stage5-no-bridges-synthetic-proof.log).
This cleanly separates what was proved (the target recurrence) from what was
assumed (the real-call connection).

The bridges may be extensionally plausible for the original pure recurrence on
bounded integer arrays, but plausibility and finite tests do not replace the
required universal connection theorem. The body-sensitivity witness in Stage 4
also shows the proof theory has no dependency on the current program body.
Accordingly this is an execution-bypassing, answer-encoding proof extension,
not an acceptable low-level primitive.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted.

The first reviewer mutation changed the symbolic result to
`targetAnswer(...) + 1`. It parsed successfully with `--dry-run`, but the
Haskell backend explored irrelevant imported float branches and failed on a
missing `FLOAT.int2float` hook. That run is preserved in
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log) and
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log), but it is
explicitly not counted as non-vacuity evidence because the failure was an
unrelated backend error.

The valid fresh mutation grounds the same off-by-one obligation at a
demonstrably satisfiable intended-domain state:

```text
heap[0] = list([1,2])
#targetCall(mainCall, ref(0), 0, 0)  =>  2
```

The correct target result for `[1,2]` is `1`, confirmed by both Python
implementations in Stage 4. The mutation source is
[spec-audit-vacuity-ground.k](evidence/spec-audit-vacuity-ground.k).

Its `kprove --dry-run` exited 0, so the spec built successfully:
[stage6-ground-vacuity-dry-run.log](evidence/stage6-ground-vacuity-dry-run.log).
The actual proof exited 1 with `WarnStuckClaimState`; the residual is exactly
`<k> 1 ~> .K </k>`, which does not unify with the demanded `2`:
[stage6-ground-vacuity-proof.log](evidence/stage6-ground-vacuity-proof.log).

Therefore the synthetic target theorem is non-vacuous and
result-discriminating. This does not repair the missing real-program
connection.

## 7. Proven versus assumed accounting

### Precisely what the successful proof establishes

Under `VERIFICATION`—which includes the two priority operational bridges—the
machine-checked result establishes:

1. the proof-local closure-application terms rewrite to corresponding
   proof-local `#targetCall` terms;
2. for any heap list `VS`, the main synthetic target yields the recursive
   mirrored mismatch count;
3. for helper-valid `L,R`, the helper synthetic target yields the mismatch
   count on that inclusive interval;
4. the synthetic execution preserves the framed non-`<k>` cells and
   continuation;
5. a ground off-by-one result is rejected.

It does not establish that loading or calling the submitted `solution.mpy`
reaches those targets, that the copied macros remain equal to the submitted
program, or that CPython returns normally on every prompt-domain array.

### Trust boundaries

The full dependency-by-dependency accounting is in
[trust-ledger.md](evidence/trust-ledger.md). In summary:

- **Acceptable low-level trust:** K v7.1.337 and its Haskell/LLVM backends;
  builtin integer, boolean, string, map, list, equality, and
  compiler-generated strictness machinery; the byte-identical fixed supplied
  semantics; the audit-designated trusted translator and canonical oracle.
- **Relevant supplied primitive:** total `valSeqAt`. Its globally abstract
  out-of-bounds behavior is concerning in general but acceptable here because
  `targetValid` and the shrinking recurrence make every intended helper access
  in bounds.
- **All opaque/symbol declarations:** `intFloatDiv`, `divII`, `floatMod`,
  `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
  `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
  `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and
  `md5hexCodes`. All are in the trusted supplied semantics and unused by this
  integer/list program. The candidate adds no opaque `symbol`.
- **Acceptable proof-local mathematics:** guarded `changeRange`,
  `targetAnswer`, and `targetValid` equations, conditional on starting at the
  synthetic target.
- **Empirical bridges only:** byte-identical translation; six concrete K
  assertions; the finite differential corpus. These support their tested
  relationships and never substitute for a K reachability connection theorem.
- **Informal intent bridge:** the standard argument that one change is
  necessary and sufficient per unequal mirrored pair. This supports the
  mismatch-count interpretation but does not link execution to the summary.
- **Concerning runtime boundary:** supplied K recursion is unbounded relative
  to CPython's recursion limit; the two recorded long arrays expose the
  difference.
- **Illegitimate assumption:** the two priority call bridges. They replace
  program-defined execution, determine the result through a hand-written
  recurrence, lack a bridge-free universal connection theorem, fail the
  bridge-removal test, and fail body sensitivity.

### Gate and decision accounting

- Fresh verification gate: **passes under the submitted extended theory**.
- Result constraint/non-vacuity: **passes for the synthetic target theorem**.
- Real-program soundness/pinning: **fails**.
- Natural-language adequacy: mismatch-count intent is supported on ordinary
  arrays, but the recursive Python implementation has a documented unbounded
  input-domain runtime divergence.
- Evidence auditability: commands, sources, statuses, inputs, and bounded logs
  are preserved; candidate provenance metadata is missing.

The decisive decision-boundary condition is that the proof bypasses the real
program and proves a substituted recurrence. A fresh `#Top`, passing small
tests, truthful recurrence equations, and successful non-vacuity do not cure
that defect.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
