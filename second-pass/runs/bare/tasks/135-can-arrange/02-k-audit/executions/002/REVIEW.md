# Independent adversarial review: 135-can-arrange

The candidate's sole target claim does reconstruct and close with `#Top`, and
the claim is non-vacuous and mechanically pinned to the submitted constructor
body. It is nevertheless not a legitimate proof of the full generated Python
program under the source contract. The generated semantics idealizes away a
real, exercised Python control effect: on valid distinct-integer arrays of
length 1000 and 1200, the submitted recursive Python raises
`RecursionError`, while the trusted canonical loop returns the required result
and the K theorem is unrestricted in length. The formal model also admits only
integer arrays even though the untyped source contract and both Python
implementations admit other distinct comparable values. Those are material
source-domain/real-program gaps, which this benchmark maps to `FAIL /
NOT_LEGIT`. A globally over-broad slice rule has an additional concrete false
semantic witness.

All candidate reports, cached outputs, and generation traces were treated only
as untrusted claims. All execution below used source copied to
`/tmp/audit-work/reconstruction-135`; no candidate-provided compiled
definition or cache was reused.

## 1. Input and provenance integrity

The launcher record is `/audit-input.json`, with:

- problem `135-can-arrange`;
- condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted inputs `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

The independent checker and complete output are
`/audit-output/evidence/check_integrity.py` and
`/audit-output/evidence/01-integrity.log`. It established:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, `/generation-result.json`, all launcher-declared provenance
  files, and all required `legacy-selected-stage1` records are readable,
  regular files or real directories as appropriate.
- `/audit-campaign-lock.json` is exactly equal as a JSON object to the
  `audit_campaign` block. Its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The mounted candidate's independently computed length-delimited pipeline
  tree digest is
  `f4db0986b1e167d34f56d91f230011e727c972aab9cc3b4c96a59f147b284d12`,
  exactly the retained workspace hash in both the invocation and stage-1
  result.
- The structured trace's corresponding digest is
  `00f74b1c43178e4a0342c5b477a008432b7d472bd0052b48320169d4412a307d`,
  exactly `usage.json`'s recorded `source_trace_sha256`. The sole JSONL
  member independently hashes to the separately recorded
  `a7aae3076a52f861b29bf43a913801b28157059f99a56fd346e7269846ba3f65`.
  The additional audit-input tree-digest fields use a distinct launcher
  encoding; every constituent file and the legacy pipeline trees were
  independently matched to their recorded hashes.
- Every stage-result evidence-member hash matches, including
  `codex-last.txt`, `codex-output.log`, the JSONL trace,
  `legacy-metrics.json`, `legacy-run-input.json`, `prompt.txt`, and
  `usage.json`.
- The trusted canonical, prompt, translator, run manifest, task manifest,
  invocation, result, metrics, prompt, output, last-message, and usage hashes
  all match the hashes recorded by the launcher.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- The candidate and trace trees contain no symlinks or unsupported entries.

The required generation records were read as untrusted history. The full
structured trace contains 199 valid JSON lines and 37 paired tool calls; the
reviewer-authored parser read every line and recorded its command/result
inventory in `/audit-output/evidence/02-generation-trace-summary.log`.
Generation history claims a successful `#Top`; that claim was not relied upon.

`runtime-metrics.json` is absent. This is permitted for
`legacy-selected-stage1`; the historical runtime metrics were never recorded
and are not reconstructed. `usage.json` is present and was inspected.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist and
`mount_reference_semantics` is false. No hidden or inferred reference
semantics was used. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, for an array with no
duplicate values the function must return the largest index `i`, with
`1 <= i < len(arr)`, for which `arr[i]` is not greater than or equal to
`arr[i - 1]`. For ordinary totally ordered elements this is exactly
`arr[i] < arr[i - 1]`. If there is no such index, it must return `-1`.

The canonical implementation scans all adjacent pairs, updating the result at
every drop. The candidate uses recursion on `arr[1:]`: a drop found in the
tail is shifted by one and outranks the head pair; otherwise it checks the
head pair. That recurrence is mathematically correct when the recursive calls
return normally.

### Translator fidelity

The trusted translator was run independently:

```text
python3 /tmp/audit-work/trusted-135/py2mpy.py \
  /tmp/audit-work/reconstruction-135/solution.py \
  > /tmp/audit-work/reconstruction-135/solution.regenerated.mpy
```

`cmp` exited 0. Both the regenerated and submitted files have SHA-256
`399c04a7eb3bef35a8538c19d17eca0fe7af34f9573486b4d4d1c6ccc0e838a8`.
Exact commands and statuses are in
`/audit-output/evidence/03-translation-identity.log`.

### Differential testing

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical entry point and the scratch copy of the generated entry point. Its
deterministic scope was:

- both documented examples;
- empty and singleton arrays;
- both length-two branch boundaries;
- every return branch and multiple-drop behavior;
- negative and arbitrary-precision integers;
- distinct float and string arrays;
- all 46,234 permutations of lengths 0 through 8;
- 1,000 seeded random distinct-integer arrays of lengths 0 through 60;
- valid distinct-integer arrays of lengths 900, 1000, and 1200.

There were 47,249 cases and two mismatches. With Python 3.10.12 and its
recorded recursion limit of 1000:

```text
len=1000 ascending:
  canonical = ("return", -1)
  generated = ("raise", "RecursionError", ...)

len=1200 descending:
  canonical = ("return", 1199)
  generated = ("raise", "RecursionError", ...)
```

The script deliberately exited 1. Exact results are in
`/audit-output/evidence/04-differential-test.log`. These arrays satisfy the
stated no-duplicates contract. This is a result/control divergence of the real
generated Python, not a K-tool or audit failure.

The prompt has no integer-only type annotation or prose restriction. Both
Python implementations also return 3 on the valid distinct comparable arrays
`[1.25, -4.5, 7.75, 0.0]` and
`["ant", "bee", "yak", "cat"]`, as recorded in
`/audit-output/evidence/22-noninteger-domain-witness.log`. The K value grammar
at `semantic.k:38-42` only permits `seq` of `Int`; these source-domain values
cannot instantiate the theorem.

Stage 2 therefore fails full program/contract fidelity even though the
candidate agrees with the canonical on all tested shorter integer cases.

## 3. Clean proof reconstruction

The observed toolchain was K v7.1.293; commands and versions are in
`/audit-output/evidence/05-toolchain.log`.

Only these source artifacts were copied to scratch:

```text
solution.py
solution.mpy
semantic.k
verification.k
spec.k
prove.sh
```

Candidate `__pycache__`, `kprove.log`, compiled definitions, and any caches
were excluded. The trusted translator regenerated a separate
`solution.regenerated.mpy`.

### Fresh builds

The concrete definition was rebuilt with:

```text
kompile semantic.k --backend llvm \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition concrete-fresh-kompiled
```

It exited 0. The complete bounded log is
`/audit-output/evidence/06-kompile-concrete.log`.

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition proof-fresh-kompiled
```

It exited 0. The log is
`/audit-output/evidence/07-kompile-proof.log`.

The compiler issued a material warning for `get`: despite `[function, total]`,
the empty-sequence case is non-exhaustive. This is assessed in Stage 5 rather
than treated as a build failure.

### Every positive target claim

`spec.k` contains exactly one claim. It was independently run with:

```text
kprove spec.k --definition proof-fresh-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0. See
`/audit-output/evidence/08-kprove-positive.log`. Thus mechanical closure under
the submitted theory passes.

### Generated-semantics concrete reconstruction

`/audit-output/evidence/concrete_semantics_compare.py` invoked the regenerated
`solution.mpy` through the fresh LLVM definition on empty, singleton,
length-two ascending and descending, both documented cases, a multiple-drop
case, and a negative-integer case. It independently compared each final K
integer with both Python implementations. All eight agreed and all `krun`
processes exited 0. Commands, inputs, results, and the zero-mismatch summary
are in `/audit-output/evidence/09-concrete-semantics-compare.log`.

Fresh dynamic reconstruction therefore passes for the modeled short-input
subset. It does not repair the Stage 2 mismatch between that model and real
Python on unrestricted array length.

## 4. Adequacy and real-program pinning

### Plain-language formal claim

The single entry claim at `spec.k:10-18` starts with:

```text
invoke("can_arrange", arrayVal(A, O, N)) ~> K
```

in an arbitrary caller environment `ENV`, arbitrary stack `FRAMES`, arbitrary
continuation `K`, and an exact one-entry definitions map binding
`"can_arrange"` to `canArrangeFunction`.

Its precondition says:

- `O >= 0`;
- `N >= 0`;
- `O + N <= arrSize(A)`.

Thus `arrayVal(A,O,N)` is an in-bounds integer-array view. The postcondition
requires the invocation to become exactly:

```text
value(intVal(answer(A, O, N))) ~> K
```

while preserving the caller environment, definitions, stack, and
continuation. The returned integer is not free or existential.

`answer` is a recursive mathematical summary: for length at most one it is
`-1`; otherwise a non-`-1` tail answer is shifted by one, and if the tail has
no drop the result is 1 exactly when the head pair drops, else `-1`.

### Exact constructor/body pinning

The entry claim begins at `invoke` rather than at module loading, which is
permitted only if the definitions binding is the actual submitted binding and
body. Two independent constructor-level comparisons establish that fact:

1. `kast --expand-macros` converted the trusted-regenerated
   `solution.mpy` and `solutionProgram` to canonical KORE. `cmp` exited 0;
   both files were 6,356 bytes with SHA-256
   `79c5f4359c868a102f874b2043c7ed16a04a3aacae3fef42f7995304ca985d55`.
   See `/audit-output/evidence/10-program-macro-pinning.log`.
2. The reviewer-only, constructor-only wrapper
   `/audit-output/evidence/pinning.k` maps a `Function` to the corresponding
   one-binding module. `programOf(canArrangeFunction)` and the regenerated
   `solution.mpy` again produced byte-identical canonical KORE with the same
   hash. The wrapper build and comparison are
   `/audit-output/evidence/11-kompile-pinning.log` and
   `/audit-output/evidence/12-claim-body-pinning.log`.

The operational semantics then interprets the exact `If`, recursive `Call`,
`Assign`, comparisons, slices, indices, and returns. There is no proof rule
rewriting an invocation directly to `answer`.

### Satisfiable entry states and concrete substitutions

A concrete satisfying state is:

```text
A = seq(1,2,4,3,5)
O = 0
N = 5
ENV = .Map
FRAMES = .List
K = .K
```

Its guards are `0 >= 0`, `5 >= 0`, and `5 <= arrSize(A) = 5`.
Reviewer-authored ground claims for this state, the empty state, and a
descending array all closed with `#Top`; their expected results 3, -1, and 4
also matched both Python implementations. See
`/audit-output/evidence/ground-spec.k` and
`/audit-output/evidence/13-ground-claim-substitutions.log`.

### Body and result sensitivity

The reviewer changed the function term actually stored in `<defs>` to the
materially different body `return 0`, rebuilt that definition successfully,
and reran the same universal result obligation. K reached `intVal(0)` and
failed the `answer` postcondition with `WarnStuckClaimState`; kprove exited 1.
See:

- `/audit-output/evidence/body-mutated-verification.k`;
- `/audit-output/evidence/body-mutated-spec.k`;
- `/audit-output/evidence/14-kompile-body-mutation.log`;
- `/audit-output/evidence/15-body-sensitivity.log`.

The separate false-result mutation in Stage 6 also fails cleanly.

### Adequacy judgment

Constructor pinning and K-level result constraint pass. Real-program adequacy
does not:

- the K call stack is unbounded and has no `RecursionError`, while the actual
  recursive Python demonstrably raises on valid length-1000/1200 inputs;
- the K theorem only has integer arrays, while the untyped source contract and
  Python implementations accept other distinct comparable values.

The K theorem is therefore about a materially narrowed, idealized execution
model, not the full generated Python program required by the prompt.

## 5. Rule-by-rule static soundness review

The lexical inventory is
`/audit-output/evidence/16-rule-inventory.log`: 41 rules in `semantic.k`,
seven in `verification.k`, and one target claim. There are no priority,
`simplification`, `functional`, `opaque`, `concrete`, `owise`, or `anywhere`
declarations.

### Syntax, functions, macros, and configuration

`MPY-SYNTAX` declares every constructor used by `solution.mpy`:

- program and statement forms: `Pgm`, `Stmts`, `FuncDef`, `Return`, `Assign`,
  and `If`;
- expression forms: `Int`, `Name`, `Call`, `Compare`, `CmpOp`, `Subscript`,
  `Slice`, `NoBound`, `BinOp`, and `UnaryOp`;
- list carriers: `Params`, `Strings`, `Exps`, `CmpOps`, and `Ints`;
- values and stored functions: `Arr = seq(Ints)`, `intVal`, `boolVal`,
  `arrayVal`, and `function`.

The operational module declares the continuation markers `invokeEntry`,
`load`, `install`, `invoke`, `exec`, `eval`, `value`, `assignTo`, `branch`,
`callValue`, `applyLen`, `sliceFromOne`, `indexAt`, `unaryMinus`, `binLeft`,
`binRight`, `cmpLeft`, `cmpRight`, `doReturn`, and `noReturn`.

The configuration has exactly the material state:

- `<k>` for computation;
- `<env>` for the active local environment;
- `<defs>` for function bindings;
- `<stack>` for saved caller environments.

There is no unused heap, allocation, exception, or recursion-depth cell. The
absence of the last two is a real-Python adequacy gap, not hidden state.

Six local symbols are declared `[function,total]`:
`appendStmts`, `get`, `arrSize`, `intsSize`, `answer`, and `answerStep`.
`canArrangeFunction` and `solutionProgram` are syntax macros.

### Operational and helper rules

Every local rule is inventoried below. “Sound on target path” means its
accepted match may be too broad globally but all matches generated by this
submitted body under the target precondition are within the truthful subset.

| ID | Source | Rule and judgment |
|---|---|---|
| S01 | `semantic.k:78` | `appendStmts(.Stmts,MORE) = MORE`; true list identity. |
| S02 | `semantic.k:79` | Cons case for `appendStmts`; structurally decreases and is true. S01/S02 cover all `Stmts`. |
| S03 | `semantic.k:91` | `Module` schedules `load`; faithful module sequencing. |
| S04 | `semantic.k:92` | Empty module body finishes; faithful. |
| S05 | `semantic.k:93-94` | Loads one `FuncDef`, then the rest; faithful order. |
| S06 | `semantic.k:95-96` | Installs/overwrites the named definition; agrees with sequential Python definition binding for this module. |
| S07 | `semantic.k:97` | Selects the benchmark entry name `can_arrange`; a driver convention, not a task-answer shortcut. |
| S08 | `semantic.k:102-105` | Resolves the exact one-parameter function, saves the full caller environment, binds the argument, and pushes the caller frame. Correct for the submitted calls. |
| S09 | `semantic.k:107` | Empty statement execution is complete. An implicit Python `None` return is unmodeled, but every path in this body explicitly returns. |
| S10 | `semantic.k:108-109` | Assignment evaluates its RHS before writing and then continues; correct order. |
| S11 | `semantic.k:110-111` | Writes the evaluated value in the active local environment; correct for `result`. |
| S12 | `semantic.k:113-114` | Evaluates an `if` guard before selecting a branch and preserves following statements. |
| S13 | `semantic.k:115-116` | True branch plus continuation via truthful `appendStmts`. |
| S14 | `semantic.k:117-118` | False branch plus continuation; disjoint from S13. |
| S15 | `semantic.k:120` | Evaluates a return expression and discards following source statements, matching abrupt return. |
| S16 | `semantic.k:121-123` | At the exact `doReturn ~> noReturn` boundary, restores and pops the caller frame while preserving the outer continuation. Correct binding/control footprint. |
| S17 | `semantic.k:126` | Integer literal to `intVal`; faithful. |
| S18 | `semantic.k:127-128` | Name lookup from the active environment; faithful for every bound name used here. Unbound-name exceptions are outside the model but unreachable in this body. |
| S19 | `semantic.k:130` | Evaluates unary-minus operand first. |
| S20 | `semantic.k:131` | Arbitrary-precision integer negation; agrees with Python integers. |
| S21 | `semantic.k:133` | Evaluates the sole `len` argument first; exact submitted call shape. |
| S22 | `semantic.k:134` | Array-view length is `N`; truthful for valid views. |
| S23 | `semantic.k:136-137` | Evaluates a sole user-function argument, excluding `len`; disjoint from S21 for concrete names. |
| S24 | `semantic.k:138` | Passes the evaluated value to binding-resolving S08; preserves continuation. |
| S25 | `semantic.k:140-141` | Schedules the exact `[1:]` slice used by the body. |
| S26 | `semantic.k:142-143` | Replaces `[1:]` by `(O+1,N-1)` without a guard. It is truthful on the target path, where the preceding branch establishes `N > 1`, but globally false on empty views. The concrete false witness below makes this an actual semantic unsoundness, not merely missing evidence. |
| S27 | `semantic.k:145` | Evaluates the receiver before the integer index; faithful for the submitted indices. |
| S28 | `semantic.k:146-147` | Reads `get(A,O+I)` but omits Python bounds/negative-index behavior. The actual body reaches indices 0 and 1 only with `N > 1`, so its target-path reads are in bounds. Invalid reads expose the totality gap below. |
| S29 | `semantic.k:149-150` | Evaluates binary left operand before right. |
| S30 | `semantic.k:151-152` | Stores the left value while evaluating the right. |
| S31 | `semantic.k:153-154` | Computes stored-left plus evaluated-right; true for integer `+`. |
| S32 | `semantic.k:156-157` | Evaluates the single comparison's left operand first. |
| S33 | `semantic.k:158-159` | Stores the left value while evaluating the right. |
| S34 | `semantic.k:160-161` | Computes left `<=` right; variable orientation is correct. |
| S35 | `semantic.k:162-163` | Computes left `!=` right; correct. |
| S36 | `semantic.k:164-165` | Computes left `<` right; correct. S34-S36 are operator-disjoint. |
| S37 | `semantic.k:172` | `arrSize(seq(IS)) = intsSize(IS)`; true and covers the sole `Arr` constructor. |
| S38 | `semantic.k:173` | Empty integer-list size is zero. |
| S39 | `semantic.k:174` | Cons-list size is one plus tail size; structurally decreases and, with S38, is total. |
| S40 | `semantic.k:175` | `get` at zero returns the nonempty list head; true where it matches. |
| S41 | `semantic.k:176-177` | Positive-index `get` drops a head and decrements the index; true where it matches and descends. It has no empty-list or negative-index rule, contradicting the declaration that `get` is total over all `Arr × Int`. |

### Concrete false conclusion witness for S26

The reviewer-authored program
`/audit-output/evidence/slice-empty.mpy` computes
`len(arr[1:])`. On the valid empty input, the rebuilt semantics exits 0 with
`intVal(-1)`, while Python evaluates `len([][1:])` to 0:

```text
K:      value ( intVal ( -1 ) )
Python: 0
```

The exact command and output are
`/audit-output/evidence/17-slice-rule-false-witness.log`. This witness is on an
intended-domain value and is enabled directly by S26 followed by S22. The
submitted `can_arrange` body does not reach S26 for that input because it takes
the base branch, so this false rule is not the source of the target `#Top`.
It nevertheless prevents validating `semantic.k` as a sound semantics over
the rule's declared match domain.

### `get` totality gap, not an unsupported unsoundness label

The compiler explicitly reports a non-exhaustive match for `[total] get`.
`/audit-output/evidence/get-empty.mpy` attempts `arr[0]` on an empty array. The
fresh concrete backend exits 113 on residual `get(seq(.Ints),0)`, whereas
Python raises `IndexError`; see
`/audit-output/evidence/18-get-totality-gap.log`.

This is a concrete coverage/exception-model gap. It does not produce a false
ground integer equality, so this review does not label S40 or S41 themselves
unsound. The target claim's in-bounds precondition and control flow ensure
that every `get` used by the proof has a finite nonnegative index below the
backing sequence length. An informal induction then justifies S40/S41 on that
restricted use domain.

### Proof-local rules and macros

| ID | Source | Rule and judgment |
|---|---|---|
| V01 | `verification.k:12-13` | `answer=-1` for `N<=1`; correct base definition. |
| V02 | `verification.k:14-19` | For `N>1`, recurses on `(O+1,N-1)` and compares the head pair through `answerStep`; strictly descends. V01/V02 are disjoint and cover all integer `N`. |
| V03 | `verification.k:21-22` | A non-`-1` tail result is shifted by one; correct because any tail drop has a larger original index than the head pair. |
| V04 | `verification.k:23-24` | If the tail has no drop and `Y<X`, returns local index 1. |
| V05 | `verification.k:25-26` | If the tail has no drop and `Y>=X`, returns `-1`. V03-V05 are disjoint and cover all integer `R,X,Y`. |
| V06 | `verification.k:31-45` | `canArrangeFunction` is program data, not execution replacement. Constructor equality with the trusted-regenerated function body is machine-checked in Stage 4. |
| V07 | `verification.k:47-61` | `solutionProgram` is the whole submitted constructor program; canonical KORE equality is machine-checked in Stage 4. It is not used to rewrite results. |

`answer` encodes the desired mathematical recurrence only in the
postcondition. It never preempts `invoke`, `exec`, `eval`, calls, or returns.
The successful reachability claim is the connection theorem from execution
of the exact body to this summary. Thus the task answer is not smuggled into
an operational bridge.

The low-level `get` symbol appears in both index execution and the `answer`
summary. Its valid-index equations are ordinary array-selection mathematics,
not task-specific correctness. Their Python-array interpretation is a trust
bridge accounted for in Stage 7, with finite evidence but no separate
machine-checked Python semantics.

### Construct coverage

Every constructor in the submitted `solution.mpy` maps to the declarations
and rules above. Omitted translator constructs are unused and therefore not a
defect under `GENERATED_SEMANTICS`. For the actual safe control path, binding,
left-to-right evaluation, branch selection, recursive call/return, caller
environment restoration, statement continuation, and integer results are all
modeled. The material missing real-Python effects are recursion depth,
exceptions, and slice allocation/resource failure.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. The fresh mutation is
`/audit-output/evidence/spec-vacuity-audit.k`. It changes the documented
ground result obligation from 3 to the demonstrably false value 4:

```text
invoke("can_arrange", arrayVal(seq(1,2,4,3,5),0,5))
  => value(intVal(4))
```

This is a reachable, satisfying input: `O=0`, `N=5`, and the backing size is
5. Both Python implementations return 3.

The mutation compiled to KORE successfully under:

```text
kprove --dry-run spec-vacuity-audit.k \
  --definition proof-fresh-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The dry run exited 0; see
`/audit-output/evidence/19-vacuity-build.log`.

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual
configuration contains exactly `value(intVal(3))`, which cannot unify with
the mutated `value(intVal(4))` destination. This is the expected unmet result
obligation, not a parser error, missing import, timeout, or unrelated crash.
See `/audit-output/evidence/20-vacuity-proof-failure.log`.

Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's K theory, for any finite K integer sequence `A`, any
nonnegative in-bounds view `(O,N)`, the exact submitted `can_arrange` function
binding, and arbitrary caller environment, stack, and continuation, symbolic
execution of:

```text
invoke("can_arrange", arrayVal(A,O,N))
```

reaches:

```text
value(intVal(answer(A,O,N)))
```

with caller control state restored. The proof is all-length within that
idealized K model, executes the actual constructor body, is sensitive to body
and result mutations, and does not rely on a task-answer operational rewrite.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM executor, Haskell prover, and reachability logic | All machine results | Normal foundational tool trust; versions and fresh commands are recorded. |
| Trusted `py2mpy.py` transliteration | Program-term identity | Launcher-trusted input; output is byte-identical to submitted `solution.mpy`. |
| Built-in K `Int`, `Bool`, `String`, `Map`, and `List` operations | Arithmetic, guards, binding/state | Acceptable low-level K trust. K arbitrary-precision integers agree with Python integers for modeled operations. |
| `arrayVal(seq(IS),O,N)` as a Python sequence view | `len`, slicing, indexing, `answer` | Informal representation bridge. It is adequate for pure, in-bounds integer operations below resource limits; it omits identity, allocation, exceptions, and recursion/resource limits. |
| `get` as valid integer-array selection | Program index results and `answer` | Equations are mathematically correct on the target's in-bounds uses; finite concrete evidence supports them. The `[total]` declaration is globally non-exhaustive. |
| `answer` means “largest drop index or -1” | Human-facing postcondition | Straightforward informal induction plus 51,234 zero-mismatch differential checks against the independently implemented trusted canonical. Artifact and output: `/audit-output/evidence/summary_differential.py` and `/audit-output/evidence/21-summary-differential.log`. Finite tests do not replace the mathematical argument. |
| No CPython recursion-depth/exception semantics | Full real-program theorem | Illegitimate for the unrestricted source contract: valid length-1000/1200 integer inputs demonstrate a real control/result divergence. |
| Integer-only `Arr`/`Val` grammar | Formal input domain | Materially narrows the untyped array contract; valid float/string arrays executed by both Python implementations are outside the theorem. |
| Unguarded S26 slice rule | Soundness of generated semantics | Illegitimate globally; it proves the concrete false result `len([][1:]) = -1` in K. Target control flow happens not to exercise the bad match. |
| Candidate generation report, `kprove.log`, and differential claims | None | Not trusted; all material claims were independently reconstructed. |

The finite program differential in Stage 2 supports short-input equivalence
only. The summary differential supports the `answer` intent bridge only. They
are not substitutes for the reachability proof.

### Gate and decision accounting

- Mechanical closure: **PASS**. Fresh kprove printed `#Top` and exited 0.
- Constructor pinning/result constraint/non-vacuity: **PASS**.
- Real-program soundness: **FAIL** for the full requested domain because the
  semantics proves an unbounded ideal recursion while real Python raises on
  valid long inputs. The generated semantics also contains the witnessed
  globally false S26 rule.
- Intent/domain adequacy: **FAIL** because the formal theorem is integer-only
  and omits valid source-contract behavior.
- Evidence auditability: **PASS** for the reconstructed commands and bounded
  artifacts, but reproducibility cannot cure the failed soundness/adequacy
  gates.

Within an idealized, unbounded-stack, exception-free integer-array model, the
candidate has a meaningful and non-vacuous reachability proof. That is
sound-but-materially-limited progress, not a legitimate proof of the full
HumanEval source contract. The benchmark instruction explicitly maps such
material source-domain narrowing to `FAIL / NOT_LEGIT`, rather than
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
