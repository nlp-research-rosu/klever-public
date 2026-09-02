# Independent adversarial review: 122-add-elements

## Executive finding

The candidate reconstructs successfully and its K entry claim genuinely
executes the constructor body in the submitted `solution.mpy`. The claim is
result-constraining and rejects both a body mutation and a false
postcondition. However, the submitted program and the proved summary implement
the wrong criterion on a material part of the stated integer domain.

The trusted canonical implementation at `/reference/canonical.py:20` includes
an element exactly when `len(str(elem)) <= 2`. The candidate at
`/candidate/solution.py:4` instead includes it when `abs(elem) < 100`. These
criteria differ on every negative two-digit integer. A minimal satisfying
source-contract witness is `arr = [-99], k = 1`: the canonical result is `0`,
while both the candidate and its proved K summary return `-99`.

This is not a bounded-domain issue, a timeout, or an infrastructure
uncertainty. It is a deterministic intended-domain implementation/specification
failure. Under the benchmark decision boundary, the candidate is not a
legitimate proof of the requested HumanEval contract.

## 1. Input and provenance integrity

The declared layout is `legacy-selected-stage1`, the declared semantics mode is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is present as
required. No mode/mount contradiction exists.

I read and checked:

- `/audit-input.json`, including `record_layout`, all `container_paths`, the
  embedded manifest, hashes, and integrity fields;
- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`,
  `legacy-metrics.json`, and `legacy-run-input.json`;
- all 613 JSONL records in the structured trace below
  `/generation-evidence/codex-trace/`.

`runtime-metrics.json` is absent, which is permitted for this historical
`legacy-selected-stage1` record. `usage.json` is present and was inspected. The
trace parsed with zero JSON errors; `codex-output.log` is valid UTF-8 with
39,909 lines. The full trace/tool-call inventory is in
`evidence/generation-trace-inventory.log`.

The campaign-lock JSON exactly equals the `audit_campaign` block in
`audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The task manifest equals the embedded manifest after accounting for the
launcher-added `config` field, which equals `manifest_config`.

Every required mounted record is a readable regular file or real directory,
not a symlink. Independently recomputed file hashes match all recorded file
hashes. The independently reproduced pipeline tree digest for the candidate is
`9354f4b1468414d811bd2b45d00ca1756ca3ced6abbf02a56b28db9a92921f1c`;
it matches the result and invocation input/output/retained-workspace records.
The corresponding semantics tree digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
and the trace tree digest is
`f212cb176dcd319468147a84ffed20acbded533c4858efd4883cdde9a44c4493`,
matching their recorded provenance fields.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. Recursive comparison of `candidate/reference-semantics` against
`/reference/reference-semantics` found exactly the same 24 regular files plus
one directory entry, with identical entry types, modes, sizes, and contents.
There are no missing, additional, mistyped, changed, or symlinked semantics
entries. The per-entry hashes and checks are in
`evidence/stage1-integrity.log`; the scratch-copy source manifest is
`evidence/scratch-source-manifest.sha256`.

Generation records claimed `KPROVE_PASSED` and 10,000 differential successes,
but they were treated only as untrusted history. In particular, the generation
trace shows that its randomized oracle used `len(str(abs(x))) <= 2`, which
repeated the candidate's mistake rather than calling the trusted canonical
entry point.

Stage 1 result: integrity gate passed; there is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py:2-15`, `arr` is a non-empty list of integers with
`1 <= len(arr) <= 100`, and `k` is an integer with
`1 <= k <= len(arr)`. The required result is the sum, among the first `k`
elements, of those having at most two digits. The trusted executable
interpretation is `/reference/canonical.py:20`:

```python
sum(elem for elem in arr[:k] if len(str(elem)) <= 2)
```

Thus `-9` qualifies because `str(-9)` has length two, while `-10` through
`-99` do not because the minus sign makes their string length three.

The candidate instead executes:

```python
if abs(element) < 100:
    total += element
```

That agrees for non-negative integers and for one-digit negatives, but
incorrectly includes all negative two-digit integers.

### Trusted translation

From a fresh scratch copy, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`7b5c94215b395cce642414d4e864a3643404201eabef94b6355fa8b8f264a779`;
`cmp` and the logged command exited 0. Therefore the submitted `solution.mpy`
is exactly the trusted translation of the submitted `solution.py`.
See `evidence/stage2-translation-byte-identity.log`.

### Independent differential test

`evidence/stage2_differential.py` imports the two Python entry points from
separate files and uses the trusted canonical function as the oracle. It covers:

- the documented example;
- minimum and maximum array lengths;
- `k = 1` and `k = len(arr)`;
- the branch boundaries
  `-1000, -100, -99, -10, -9, -1, 0, 9, 10, 99, 100, 1000`;
- 5,000 deterministic generated valid inputs with seed `12220260726`;
- an empty-array/zero-`k` diagnostic clearly labeled outside the contract.

All 5,009 intended-domain inputs are preserved in
`evidence/stage2-differential-inputs.json` (SHA-256
`69ec553a78314a967e188cd7dff9e5cfaf43a8065f4cd3f859e6d14b6d9dde58`).
The script exited 1 after finding 3,759 mismatches. The smallest is:

```text
arr=[-99], k=1, canonical=0, candidate=-99
```

The empty outside-contract diagnostic returned 0 from both implementations;
it does not cure the intended-domain failures. Exact results are in
`evidence/stage2-differential.log`.

Stage 2 result: failed program fidelity to the trusted HumanEval contract.

## 3. Clean proof reconstruction

All execution occurred in `/tmp/audit-work/122-add-elements-audit`. I copied
only source artifacts and the trusted supplied semantics. No candidate-provided
compiled definition or cache was copied or used. The live tools report K
version `v7.1.293`.

The following fresh commands were run:

| Purpose | Command | Exit/result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 |
| Load submitted module | `krun solution.mpy --definition audit-runtime-kompiled` | 0; `.K`, `NoExc`, exit code 0; closure body visible in scope 0 |
| Candidate smoke program | `krun concrete_tests.mpy --definition audit-runtime-kompiled` | 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module ADD-ELEMENTS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 |
| All original positive claims | `kprove spec.k --definition audit-verification-kompiled --spec-module ADD-ELEMENTS-SPEC` | 0 and `#Top` |
| Labeled loop claim alone | `kprove spec-labeled.k --definition audit-verification-kompiled --spec-module ADD-ELEMENTS-SPEC-LABELED --claims ADD-ELEMENTS-SPEC-LABELED.loop-invariant` | 0 and `#Top` |

The exact bounded outputs are in `evidence/stage3-kompile-llvm.log`,
`stage3-krun-solution.log`, `stage3-krun-candidate-tests.log`,
`stage3-kompile-haskell.log`, `stage3-kprove-all.log`, and
`stage3-kprove-loop-only.log`.

The original proof command proves the full two-claim set, including the entry
claim. As a diagnostic, I selected the entry label alone; removing the loop
circularity made symbolic execution continue unboundedly, so I manually
interrupted that non-authoritative filtered run with status 130 after about 85
seconds. This is recorded in `evidence/stage3-kprove-entry-only.log` and is not
used as a candidate defect or as a substitute for the successful original
all-claims run.

The candidate smoke test passes, but its fourth assertion expects `-99` for an
input beginning with `-99`. It therefore confirms the wrong implementation,
not the trusted contract.

Stage 3 result: clean verification succeeded under the submitted theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

The helper claim at `/candidate/spec.k:9-49` says: given an active loop over an
arbitrary non-empty `ValSeq` of integers, an integer accumulator, a local loop
frame, and no global shadowing of `abs`, execution consumes the loop and leaves
`total` equal to `qualifyingSumAcc` of the old accumulator and the whole input
sequence. The final loop-variable value is existential; the return-relevant
accumulator is not.

The entry claim at `/candidate/spec.k:54-108` says: choose integer sequences
`HEAD :: PREFIX` and `SUFFIX`, with total length at most 100. Call a closure
whose parameters and body are written explicitly, using
`arr = (HEAD :: PREFIX) ++ SUFFIX` and
`k = len(HEAD :: PREFIX)`, from the normal module/builtin configuration. If the
call terminates, its result is exactly
`qualifyingSumAcc(0, HEAD :: PREFIX)`. A non-empty prefix gives `k >= 1`, the
suffix decomposition gives `k <= len(arr)`, and the length guard covers the
source upper bound.

### Mechanical program identity

`evidence/stage4_pinning_and_witnesses.py` mechanically extracts the
`FuncDef` from `solution.mpy` and the `closureVal` from the entry claim. After
only list-syntax normalization (`.Stmts` terminators and whitespace), the two
constructor bodies have the same SHA-256:

```text
99b61d6b8450346419a018e80927eacf8cd9a198231b735cf4ef1842dec7751d
```

The parameter lists are both `["arr", "k"]`, and the closure parent is module
scope 0. The supplied `FuncDef` rule creates exactly this closure in scope 0,
so directly starting the call is a semantically inert normalization of module
loading, not a substituted body. The body still executes assignment, slicing,
iteration, builtin lookup/call, comparison, conditional addition, and return
through fixed semantics.

The destination is not a free variable or tautology. It fixes the returned
integer summary. Heap and allocation cells are existential at the end because
list slicing allocates and the source contract observes only the return value;
control, stack, return state, exception state, and exit code are pinned.

### Satisfiable witnesses and substitution

For `arr=[111,21,3,4000,5], k=3`, take
`HEAD=111`, `PREFIX=[21,3]`, `SUFFIX=[4000,5]`. Every entry precondition holds,
and the formal summary, candidate, and canonical all produce 24.

For `arr=[-99], k=1`, take `HEAD=-99` and both sequences empty. Every entry
precondition also holds. The formal result and candidate are `-99`, while the
canonical result is `0`. This directly locates the adequacy failure inside the
formal theorem rather than in an excluded input.

A helper-claim witness with `GLOBALS={}`, `ACC=5`, `V=21`, and
`VS=[3,4000]` satisfies all loop preconditions and has claimed final total 29.
All witness checks exited 0 in
`evidence/stage4-pinning-and-witnesses.log`.

### Body sensitivity

`spec-body-sensitivity.k` changes the threshold in the executed closure term
from 100 to 99 and keeps the original result obligation for ground input
`[99]`. It builds against the fresh proof definition. `kprove` exits 1 with
`WarnStuckClaimState`; the residual has result 0 while the destination requires
99. See `evidence/stage4-body-sensitivity.log`. This mutation changes the term
actually executed by the claim, not merely an external source file.

Stage 4 result: the claim pins and constrains the real submitted program, but
that program/formal result is inadequate for the trusted source contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5_inventory.py` produced the exhaustive machine-readable
inventory `evidence/stage5-rule-inventory.json` and the human-readable,
rule-by-rule table `evidence/stage5-rule-inventory.md`. It includes every
mounted supplied-semantics K file plus `verification.k` and `spec.k`.

Inventory totals are:

- 1,060 outer K sentences;
- 709 rules (695 fixed supplied-semantics rules and 14 proof-local rules);
- 230 syntax declarations;
- 148 declarations carrying `function`, `total`, or a functional attribute;
- 45 priority rules;
- 8 simplification rules;
- 5 contexts;
- one configuration and both reachability claims.

Every declaration, rule, attribute, file/module, line range, normalized hash,
and disposition is recorded. The independent canonical simplifier inventory
in `evidence/stage5-canonical-simplification-inventory.log` confirms exactly
the eight proof-local simplifiers.

The supplied tree contains intentionally opaque fixed symbols for features such
as symbolic float operations, sorting, and MD5:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, and
`md5hexCodes`; `floorFI`, `toF`, and `ceilF` are also symbolic fixed functions
outside some ground cases. None is reachable from this integer/list program or
affects either claim. There is no proof-local opaque result oracle.

### Used fixed-semantics path

The used construct map is explicit in the inventory. On the material path:

- the configuration supplies module scope 0, builtin scope -1, heap, stack,
  return, exception, and exit cells;
- `FuncDef` creates `closureVal(params, body, 0)`;
- call routing evaluates the callee and arguments left-to-right, allocates a
  fresh frame, binds parameters, executes the body, and restores caller
  control on return;
- assignment and augmented assignment update the active scope; integer
  addition uses the fixed `applyBin("+", Int, Int)` rule;
- list slicing evaluates bounds in order, normalizes the positive step,
  constructs the slice via `buildVS`, and allocates the new list;
- the `For` rule evaluates the iterable once, uses `#iterNext`, binds each loop
  target, executes the `If`, and resumes at the loop label;
- `abs` resolves through the builtin scope and its fixed integer rule;
- integer comparison selects the correct branch; `Return` sets the return cell,
  pops the frame, and resumes the saved continuation.

The fixed semantics' compile warnings identify some globally non-exhaustive
`[total]` functions. The float/string/sort cases are unused here.
`valSeqAt` is used only at indices constructed in-bounds by the positive-step
slice path. No witness on an intended execution reaches an unsupported used
construct, and no fixed rule contains task-specific `add_elements` or
qualification logic.

### All 14 proof-local rules

1. `intsOnly(.ValSeq) => true` and its recursive equation are truthful,
   terminating structural definitions and cover `ValSeq`.
2. `intValue(I:Int) => I` is truthful on integers. Declaring
   `intValue(Val)` total is not globally covered for non-integer `Val`
   constructors. Every result-bearing occurrence is guarded by `isInt`, so I
   found no false conclusion witness in either claim. This is a totality
   evidence gap outside the matched claim domain, not an asserted unsoundness.
3. The three `qualifyingSumAcc` equations are structurally decreasing. The
   `< 100` and `>= 100` guards are disjoint and exhaustive for integers. They
   faithfully summarize the candidate body, although that summary is not the
   canonical contract.
4. The `applyBuiltin("abs", V, .Vals)` and
   `applyBin("+", A, V)` refined-sort simplifiers agree with the fixed integer
   rules under `isInt`. They do not skip user-defined code, alter control, or
   fabricate a result.
5. The four MAP update/key/lookup simplifiers are standard, pairwise-compatible
   equations for the hooked finite-map update operation. Equal-key and
   distinct-key cases are separated by `=/=K`.
6. The `slAdjust` equation is the non-negative, positive-step clamp
   specialization for a prefix no longer than its prefix-plus-suffix list. The
   `buildVS` equation is the corresponding prefix extraction. Both are pure,
   result-bearing operational accelerators: they touch no cells and introduce
   no abrupt control effect. Ground claims proved under a fixed-only Haskell
   definition produce `#Top` for boundary witnesses; see
   `evidence/stage5-fixed-ground-kprove.log`.

The two slice accelerators are essential. Removing only them, rebuilding, and
rerunning the original claims exits 1 at a symbolic
`slAdjust/buildVS(vCons(HEAD, valSeqConcat(PREFIX,SUFFIX)),...)` residual;
see `evidence/stage5-no-slice-definition.diff`,
`stage5-kompile-no-slice.log`, and `stage5-kprove-no-slice.log`.

The candidate supplies no bridge-free, machine-checked universal connection
theorem for those two accelerators. Structural induction over `PREFIX` and the
fixed `vsLen`/`valSeqConcat`/`buildVS` equations supports their truth, and I
found no concrete or symbolic false-conclusion witness. Following the prompt's
decision boundary, I record this as a real proof-extension validation
limitation rather than label a rule unsound without the required witness. It
would independently warrant concern in an otherwise adequate proof, but it is
not the decisive failure here.

Stage 5 result: no witnessed materially unsound local rule; one totality gap
and two unproved universal bridge connections remain documented.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust or reuse. I created a fresh
mutation, `spec-vacuity-audit.k`, from the scratch copy. It changes only the
entry destination:

```text
qualifyingSumAcc(0, vCons(HEAD, PREFIX))
```

to:

```text
qualifyingSumAcc(0, vCons(HEAD, PREFIX)) +Int 1
```

The exact diff is `evidence/stage6-vacuity-mutation.diff`. The mutation parses
and reaches the proof backend. `kprove` exits 1 with `WarnStuckClaimState`
because the final summary cannot equal itself plus one; this is an unmet result
obligation, not a parser error, timeout, or unrelated crash. The bounded
residual and exit are in
`evidence/stage6-kprove-false-postcondition.log`.

The satisfying concrete witness `arr=[111,21,3,4000,5], k=3` returns 24, while
the mutation requires 25. This is recorded in
`evidence/stage6-ground-witness.log`.

Stage 6 result: non-vacuity passed.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditioned on the supplied MPY semantics, K backend, and the proof-local
equations, the successful reachability proof establishes partial correctness
of this exact submitted closure:

> For any integer list of length 1 through 100 and any valid `k`, represented
> by a non-empty prefix plus suffix, if the submitted function call terminates,
> it returns the sum of the first `k` integers whose absolute value is less
> than 100.

The helper claim supplies the arbitrary-length loop invariant. The proof is not
merely a finite unrolling, fixed-size theorem, example theorem, or
postcondition oracle.

It does **not** establish the trusted HumanEval property:

> Return the sum of the first `k` elements satisfying
> `len(str(elem)) <= 2`.

The negative-two-digit witness satisfies the formal precondition, so the gap
cannot be described as an excluded corner case.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K `v7.1.293`, Haskell reachability backend, LLVM runtime | All build, execution, and proof results | Normal external checker/toolchain trust |
| Trusted supplied MPY semantics plus hooked `INT`, `BOOL`, `MAP`, `LIST`, `STRING`, and `K-EQUAL` domains | Every operational step and proof-local MAP/int equation | Required supplied-semantics boundary; integrity verified recursively |
| Trusted `py2mpy.py` | Source-to-constructor identity | Byte identity proved for this artifact; the simple emitted constructors were mechanically compared with the claim |
| `intsOnly`, `qualifyingSumAcc`, guarded `intValue` | Loop invariant and final result | Equationally reviewed; `intValue [total]` is undercovered outside guarded integer uses |
| Refined `abs`/addition and four MAP simplifiers | Symbolic execution of loop/frame updates | Truthful specializations of fixed behavior; no new control or oracle |
| `slAdjust` and `buildVS` accelerators | Entry claim's symbolic slice | Pure and ground-validated, with an informal structural-induction justification; no candidate universal connection theorem |
| Differential testing | Program/canonical comparison only | Finite evidence, not a substitute for K proof; it supplies thousands of counterexamples to adequacy |
| Opaque fixed float/sort/digest symbols listed in Stage 5 | None | Unused and non-dependent |

### Decision

Clean `#Top`, real-body pinning, and non-vacuity are all present. They prove a
faithful theorem about the wrong submitted algorithm. The canonical-domain
counterexample is material and lies squarely within every source and formal
input bound. Consequently, the candidate cannot receive `PASS / LEGIT` or
`CONCERNS / LEGIT`; the benchmark explicitly maps a material source-contract
failure to `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
