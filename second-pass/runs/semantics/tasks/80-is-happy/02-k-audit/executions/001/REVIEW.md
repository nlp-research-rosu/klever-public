# Independent adversarial audit: 80-is-happy

## Decision

The candidate is **FAIL / NOT_LEGIT**.

Both submitted positive claims reconstruct and print `#Top`, and the Python
implementation matches the trusted reference on the recorded differential
suite. Those facts do not make the proof legitimate. The proof-local loop rule
at `/candidate/verification.k:114-131` is not the state transition established
by the loop claim: for the satisfying input `"abc"`, fixed semantics reaches
`#pop` with local `i = 1`, while the installed rule reaches `#pop` with local
`i = 0`. The audit machine-checks all three parts of that witness:

- fixed semantics proves the correct `i = 1` state;
- fixed semantics rejects the false `i = 0` state and prints a residual with
  `i |-> 1`;
- enabling the proof-local rule proves that same false `i = 0` state as
  `#Top`.

See
[the witness source](/audit-output/evidence/scripts/bridge-sensitivity.k),
[fixed-correct log](/audit-output/evidence/logs/26-bridge-fixed-correct.txt),
[fixed-false log](/audit-output/evidence/logs/27-bridge-fixed-false.txt), and
[bridge-enabled-false log](/audit-output/evidence/logs/28-bridge-enabled-false.txt).
This is a concrete false conclusion enabled on the intended input domain, not
an inference from a timeout or tool failure.

There is a second, independent adequacy failure: neither positive claim
executes `solution.mpy`, loads its `Module`, installs its `FuncDef`, looks up
`is_happy`, or binds a real call. The entry claim starts at a manually copied
macro body in manually constructed scopes. A syntactically valid mutation of
the final return in `solution.mpy` from `true` to `false` leaves a fresh proof
build and the main `#Top` unchanged. See
[the mutation](/audit-output/evidence/artifacts/pinning-mutated-solution.mpy),
[dependency/diff log](/audit-output/evidence/logs/34-pinning-dependency-and-diff.txt),
[fresh build](/audit-output/evidence/logs/35-build-pinning-mutated-proof.txt),
and [unchanged proof result](/audit-output/evidence/logs/36-prove-pinning-mutated-main.txt).

All work used K v7.1.337 and fresh scratch definitions below
`/tmp/audit-work/80-is-happy-audit`. Candidate-built definitions, caches, and
the submitted `kore-exec.tar.gz` were not used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the required trusted directory
`/reference/reference-semantics` is present as a real directory. There is no
semantics-mode/mount contradiction, so this is a candidate audit rather than an
`AUDIT_ERROR`. The mount and complete type/mode inventory is in
[02-mount-and-artifact-inventory.txt](/audit-output/evidence/logs/02-mount-and-artifact-inventory.txt).

The candidate and trusted prompt are byte-identical, as are the candidate and
trusted translator:

- prompt `cmp` exit: 0
  ([log](/audit-output/evidence/logs/04-prompt-integrity.txt));
- translator `cmp` exit: 0
  ([log](/audit-output/evidence/logs/05-translator-integrity.txt)).

A recursive, non-dereferencing comparison of
`/candidate/reference-semantics` with
`/reference/reference-semantics` exits 0 with no output
([06-semantics-tree-integrity.txt](/audit-output/evidence/logs/06-semantics-tree-integrity.txt)).
The trees contain the same 24 K files with the hashes recorded in
[07-integrity-hashes.txt](/audit-output/evidence/logs/07-integrity-hashes.txt).
No candidate entry is a symlink, and there are no missing, additional,
mistyped, or changed entries in the supplied-semantics tree.

### Missing generation records

The following requested candidate records are all missing:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`.

No filename suggesting a structured trace, JSONL trace, or trajectory is
present. This is recorded with exit 1 in
[03-required-generation-artifacts.txt](/audit-output/evidence/logs/03-required-generation-artifacts.txt).
The omissions reduce provenance auditability, although they are not the basis
for treating the K proof as failed.

The candidate also contains a Python bytecode cache and
`kore-exec.tar.gz`. They were treated as untrusted prebuilt artifacts, hashed,
and ignored
([38-ignored-candidate-binaries.txt](/audit-output/evidence/logs/38-ignored-candidate-binaries.txt)).
Only source artifacts were copied to scratch; the initial scratch manifest and
hashes are in
[08-scratch-source-manifest.txt](/audit-output/evidence/logs/08-scratch-source-manifest.txt).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a Python string `s`, `is_happy(s)` must return `False` when
`len(s) < 3`. Otherwise it must return `True` exactly when every contiguous
three-character window contains three pairwise distinct characters. The
trusted examples are:

- false: `"a"`, `"aa"`, `"aabb"`, `"xyy"`;
- true: `"abcd"`, `"adb"`.

The trusted canonical function implements that definition by iterating
`i = 0 .. len(s)-3` and rejecting a window when any of its three character
pairs are equal. The submitted `solution.py` uses a `while` loop and splits
the three disjuncts into three `if` statements. On the intended domain of
Python strings, that is the same algorithm.

Numbered copies of the prompt, canonical function, submitted Python/MPY,
specification, verification file, and candidate shell script are preserved in
[09-core-sources-numbered.txt](/audit-output/evidence/logs/09-core-sources-numbered.txt).

### Translation identity

The trusted `/reference/py2mpy.py` was run on the scratch copy of
`solution.py`. The regenerated and submitted `solution.mpy` are byte-identical
with SHA-256
`c3e43c03f7251b48bd355e973769f1b7a1991fba34f9c068144d6634bfb503dc`.
The exact command, hashes, and exit 0 are in
[10-regenerate-solution-mpy.txt](/audit-output/evidence/logs/10-regenerate-solution-mpy.txt);
the regenerated artifact is
[regenerated-solution.mpy](/audit-output/evidence/artifacts/regenerated-solution.mpy).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/scripts/differential_test.py)
imports the trusted canonical entry point and submitted generated entry point
from separate module paths. It also compares both against the direct
declarative oracle:

`len(s) >= 3 and all(len(set(s[i:i+3])) == 3 for i in range(len(s)-2))`.

The exact 8,300 inputs are preserved in
[differential-inputs.json](/audit-output/evidence/differential-inputs.json).
They comprise:

- all documented examples;
- empty, lengths 1 and 2, and the length-3/length-4 loop boundaries;
- a distinct witness for each of the three equality branches, both in the
  first window and after successful earlier windows;
- all strings over `abc` of lengths 0 through 7;
- 5,000 seeded strings of lengths 0 through 100 over `abcdβ🙂`;
- long happy and late-failing strings.

Result: `TOTAL_INPUTS: 8300`, `UNIQUE_INPUTS: 8135`, `MISMATCHES: 0`, exit 0
([11-differential-test.txt](/audit-output/evidence/logs/11-differential-test.txt)).
This is strong finite evidence for program-to-contract fidelity, not a
universal K proof or a substitute for real-program pinning.

## 3. Clean proof reconstruction

K v7.1.337 was available independently in `/usr/bin`; version evidence is in
[01-toolchain.txt](/audit-output/evidence/logs/01-toolchain.txt).

### Concrete definition and execution

From `/tmp/audit-work/80-is-happy-audit/source`, the supplied semantics was
freshly compiled:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The command exits 0
([13-build-runtime.txt](/audit-output/evidence/logs/13-build-runtime.txt)).
The compiler reports non-exhaustive total-function warnings in unused
`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`; these are accounted for
in stages 5 and 7.

A reviewer script appended branch/boundary assertions to the exact submitted
`solution.py`, and the trusted translator produced the MPY harness. The
artifacts are
[reviewer-concrete.py](/audit-output/evidence/artifacts/reviewer-concrete.py)
and
[reviewer-concrete.mpy](/audit-output/evidence/artifacts/reviewer-concrete.mpy).
Both Python execution and `krun reviewer-concrete.mpy --definition
runtime-kompiled` exit 0
([Python log](/audit-output/evidence/logs/16-python-concrete-harness.txt),
[K log](/audit-output/evidence/logs/17-k-concrete-harness.txt)).

### Positive target claims

The loop proof definition was freshly built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE \
  --output-definition verification-base-kompiled
```

It exits 0
([18-build-proof-base.txt](/audit-output/evidence/logs/18-build-proof-base.txt)).
Then:

```text
kprove spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
```

exits 0 and prints `#Top`
([19-prove-loop-spec.txt](/audit-output/evidence/logs/19-prove-loop-spec.txt)).

The public proof definition was independently built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

It exits 0
([20-build-proof-main.txt](/audit-output/evidence/logs/20-build-proof-main.txt)).
Then:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exits 0 and prints `#Top`
([21-prove-main-spec.txt](/audit-output/evidence/logs/21-prove-main-spec.txt)).

These are the two positive target claims in `spec.k`, so every positive target
was run. Stage 5 shows why the second `#Top` is unusable as a proof of the real
program.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`happy-loop-correct` starts at the internal `#while` loop head. Its
precondition says:

- the current environment location is a nonreserved `L`;
- scope 0 is the manually defined `solutionScope`, scope -1 is
  `builtinsScope`, and scope `L` has exactly `s = str(IS)` and `i = I` with
  parent 0;
- `I >= 0`;
- the remaining map has none of the three reserved/current keys;
- heap, allocation counters, stack, and scope counter are arbitrary but framed;
- no exception is active and exit code is zero;
- after the loop, `Return(True)` and `#endcall` are the exact continuation.

Its postcondition reaches `#pop`, stores `happyFrom(IS,I)` in `<ret>`, and
leaves final `i` existentially unconstrained as `?FINAL_I`.

`is-happy-correct` does not start at a module or a call. Its precondition says
the K cell already contains the manually named `isHappyBody` followed by
`#endcall`, and a preconstructed local scope already binds `s = str(IS)`.
Locations 0, -1, and `L` must be distinct and absent from `REST`; other cells
are framed, with no exception and exit code zero. Its postcondition reaches
`#pop`, permits any final scopes, and requires the return value to be exactly
`isHappySpec(IS)`.

The result is therefore syntactically constrained; it is not a free return
variable or a one-way implication.

### Satisfiable states and ground substitutions

For both claims, choose `L = 1`, `REST = .Map`, `scopeLoc = 2`, empty heap,
`heapLoc = 0`, empty stack, `NoExc`, and exit code 0. For the loop claim choose
`I = 0`. With `IS = [97,98,99]` (the code sequence for `"abc"`), all
preconditions hold. The analogous entry states for empty, `"aba"`, and
`"abcd"` also satisfy the entry precondition.

The reviewer instantiated those states in four K claims:

- empty sequence returns false;
- `"abc"` returns true;
- `"aba"` returns false;
- `"abcd"` returns true.

The file builds in dry-run mode and all four claims print `#Top`
([source](/audit-output/evidence/scripts/ground-substitutions.k),
[dry-run](/audit-output/evidence/logs/31-ground-substitutions-dry-run.txt),
[proof](/audit-output/evidence/logs/32-ground-substitutions-proof.txt)).
The same results appear for both Python functions in the differential log.

### Real-program pinning failure

The formal entry claim never contains:

- `Module(...)` or `#loadAll(Module(...))`;
- the submitted `solution.mpy` as an input;
- `FuncDef("is_happy", ...)`;
- `Call(Name("is_happy"), ...)`;
- the `Name` lookup selecting the submitted binding;
- `#applyK(toCall(closureVal(...)))`, frame allocation, or `#bindP`.

Instead, `/candidate/verification.k:40-56` separately defines `isHappyBody`,
`isHappyClosure`, and `solutionScope`. The source comment at
`/candidate/spec.k:47` says the closure “connects this exact body to the
translated function,” but there is no reachability claim establishing that
connection. `isHappyClosure` is merely an equation for a newly declared
constant, and the public entry claim never evaluates that constant.

The proof build inputs do not reference the contents of `solution.mpy`.
Changing the MPY program's final return to `false`, rebuilding from K source in
a new scratch directory, and rerunning the main proof still gives exit 0 and
`#Top`. That body-sensitivity failure is direct evidence that the formal claim
proves the copied body configuration rather than the submitted program
artifact.

The trusted translation identity and manual textual comparison make it
plausible that the original copied macro denotes the same body. They do not
machine-check module loading, binding, call entry, or dependency on the real
program, and the required audit criterion expressly requires the `<k>` cell to
execute the submitted `solution.mpy`. Stage 4 therefore fails independently of
the unsound bridge in stage 5.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The complete line-addressed source inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md), generated by the
preserved
[inventory script](/audit-output/evidence/scripts/inventory_k.py). It contains
the complete source block for every module, import, configuration, syntax,
context, rule, and claim in all 24 supplied-semantics files plus
`verification.k` and `spec.k`.

Inventory totals are:

- 1,073 entries;
- 711 rules;
- 235 syntax declarations;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 29 modules and 90 imports.

The attribute scan records 154 function-bearing blocks, 116 total-bearing
blocks, 25 symbol-bearing blocks, 54 priority-bearing blocks, 30 `owise`
blocks, 57 concrete-bearing blocks, 7 macro-bearing blocks, one recursive
macro, three strict blocks, and one sequentially strict block. There are no
`functional`, `simplification`, or `anywhere` declarations in the audited
sources.

The per-file decision below covers every inventoried source block; the full
text and line for each individual block remains in the inventory.

| File | Rule/syntax count | Static decision |
|---|---:|---|
| `semantics.k` | 0 rules, assembly imports | Exact trusted assembly; no problem-specific extension. |
| `syntax.k` | 16 syntax blocks | Constructor grammar and strictness declarations match the MPY AST subset. |
| `core.k` | 46 rules, 37 syntax blocks | Configuration, sequencing, lookup, literal, allocation, truthiness, and sequence helpers follow the selected subset. Relevant rules are mapped below. |
| `iter.k` | 0 rules, 1 syntax block | Iterator protocol declaration only; unused by the theorem. |
| `range.k` | 6 rules, 2 syntax blocks | Ordinary range arithmetic/iteration; unused. |
| `operators.k` | 10 rules, 2 contexts | Left/right evaluation and operator dispatch; `+`, `<`, and `==` paths are relevant and consistent with the program. |
| `int.k` | 16 rules, 1 syntax block | Integer operator equations are ordinary arithmetic on the used `+`, `<`, and `==` paths. Division/modulo paths are unused. |
| `bool.k` | 13 rules, 1 context | Boolean comparison/truthiness/short-circuit rules follow the selected subset; only Boolean truthiness is relevant. |
| `float.k` | 121 rules, 34 syntax blocks | Float subsystem and opaque primitive equations are unused. Its named opaque boundaries are listed in stage 7. |
| `str.k` | 28 rules, 5 syntax blocks | Code-sequence equality and single-character string behavior used here are structurally sound. Literal conversion is ASCII-only, but the claims inject `IntSeq` directly. |
| `set.k` | 12 rules, 6 syntax blocks | Character-set behavior; unused by the formal proof. |
| `list.k` | 27 rules, 5 syntax blocks | List construction/equality/iteration; unused by the formal proof. |
| `tuple.k` | 21 rules, 4 syntax blocks | Tuple construction/binding; unused. |
| `subscript.k` | 40 rules, 15 syntax blocks, 2 contexts | Evaluation order and string indexing match the used path when indices are in bounds. Fixed `intSeqAt` is partial; the candidate bridge is reviewed separately. |
| `comprehension.k` | 7 rules, 3 syntax blocks | Macro expansion for comprehensions; unused. |
| `methods.k` | 75 rules, 27 syntax blocks | String/list method subset; unused. |
| `controls.k` | 34 rules, 3 syntax blocks | Used assignment, `if`, `while`, and integer `AugAssign` rules have the required evaluation/control flow. |
| `functions.k` | 15 rules, 4 syntax blocks | Used `Return`/`#pop` control is consistent. Module definition, real call entry, parameter binding, and frame creation are bypassed by the claims. |
| `builtins.k` | 137 rules, 38 syntax blocks | Used `len(str(IS)) = isLen(IS)` path is structurally exact. Other builtins, including opaque MD5, are unused. |
| `call.k` | 21 rules, 3 syntax blocks | The `len` callee/argument route is used and preserves lookup/order. The user-function call route exists in fixed semantics but is not exercised by the entry claim. |
| `sort.k` | 19 rules, 6 syntax blocks | Opaque trusted sort boundary; unused. |
| `assert.k` | 3 rules | Used only by the concrete reviewer harness, not the proof. |
| `dict.k` | 28 rules, 12 syntax blocks | Dictionary subset; unused. |
| `concrete.k` | 16 rules, 5 syntax blocks | LLVM-only concrete sort/list legs; not imported into the Haskell proof module and irrelevant to claim closure. |
| `verification.k` | 16 rules, 8 syntax blocks | Three truthful body macros and recursive specification helpers, one unproved result bridge, and one materially false operational bridge; detailed below. |
| `spec.k` | 2 claims | Both are satisfiable and result-constraining, but the entry claim bypasses real program loading/calling. |

No supplied-semantics file contains `happy`, `is_happy`, or another
problem-specific answer rule
([39-problem-name-search.txt](/audit-output/evidence/logs/39-problem-name-search.txt)).
The LLVM compiler's totality warnings identify evidence gaps for unused
constructs rather than a false conclusion used by this theorem. I do not label
those unused declarations unsound without a witness.

### Mapping every construct used by `solution.mpy`

| MPY construct | Declaration | Relevant execution rules |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`, `syntax.k:56` | `core.k:124-127`; present but bypassed by proof |
| `FuncDef`, `Params` | `syntax.k:53`, `syntax.k:57` | `functions.k:14-16`; bypassed |
| `Call(Name("len"), s)` | `syntax.k:28`, `syntax.k:12` | `core.k:131-154`, `call.k:20-21,31`, `builtins.k:21-26` |
| `Int`, `Bool` | `syntax.k:9,11` | `core.k:194-195` |
| `Compare` | `syntax.k:30,32` | `operators.k:15-17`, `int.k:22-27`, `str.k:25-26` |
| `BinOp("+",...)` | `syntax.k:15` | sequential strictness, `operators.k:12`, `int.k:9` |
| `Subscript` | `syntax.k:22` | `subscript.k:27-41`, with candidate bridge at `verification.k:66-68` |
| `If` | `syntax.k:49` | strict guard plus `controls.k:51-54` |
| `Assign` | `syntax.k:41` | strict RHS plus `controls.k:9-18` |
| `While` | `syntax.k:46` | `controls.k:65-85` |
| `AugAssign` | `syntax.k:44` | strict RHS plus `controls.k:20-31`; used integer path |
| `Return` | `syntax.k:50` | `functions.k:78-90` |

The used path has left-to-right `BinOp` evaluation, evaluates `len` through
normal name lookup and argument evaluation, mutates only the local `i`, and
keeps heap/allocation cells framed. In-bounds indexing follows from the loop
guard `i + 2 < len(s)`. The proof does not use list allocation, exceptional
index behavior, imports, closures, or any fixed opaque primitive.

### Every proof-local declaration and rule

1. `happyLoopBody` and its macro equation (`verification.k:8-32`) are an exact
   syntactic copy of the four translated loop-body statements. This is a
   sound macro.
2. `happyLoopCondition` and its macro equation (`:34-38`) exactly copy the
   translated guard. This is a sound macro.
3. `isHappyBody` and its macro equation (`:40-49`) exactly copy the translated
   function body. It is a sound macro as text, but no formal rule connects it
   to the submitted file.
4. `isHappyClosure` and its equation (`:51-52`) construct the closure that
   fixed `FuncDef` would install for that copied body. The nullary definition
   is total and nonoverlapping. It is not an execution/connection theorem.
5. `solutionScope` and its equation (`:54-56`) construct the expected module
   scope for the copied closure. It is total and nonoverlapping, but is assumed
   as the initial state rather than derived by module execution.
6. `safeAt` (`:61-64`) has disjoint constructor equations for index 0 and
   positive indices. On a nonempty finite sequence and an in-bounds
   nonnegative index, it returns the selected integer by structural descent.
   Its `[total]` declaration is broader than its equations: empty, negative,
   and opaque-sequence cases have no defining equation. All theorem uses are
   guarded in bounds, so I record the broader declaration as an evidence gap,
   not a false value equation.
7. `intSeqAt(IS,I) => safeAt(IS,I)` (`:66-68`, priority 60) is a
   result-bearing operational bridge. Its guard is the valid-index condition,
   and the two recursive definitions agree on ground finite sequences. Ground
   witnesses produce 97 and 99 as expected, while the opposite value 98 for
   index 0 is rejected
   ([correct witnesses](/audit-output/evidence/logs/41-value-sensitivity-correct.txt),
   [opposite witness](/audit-output/evidence/logs/42-value-sensitivity-wrong.txt)).
   Nevertheless, no bridge-free universal connection claim proves equality
   over the bridge's complete symbolic match domain. The same fresh `safeAt`
   terms feed both program comparisons and `happyFrom`, so the successful loop
   claim is circular evidence for this connection, not an independent
   justification. With no false ground witness I do **not** call the equation
   mathematically unsound; I record the missing universal connection theorem
   as a Gate A evidence failure.
8. The five `happyFrom` equations (`:71-100`) are mutually exclusive on
   `I >= 0`: no remaining window gives true; the first, second, and third
   equality cases give false with earlier unequal guards; the pairwise-distinct
   case recurses at `I+1`. The recursion advances toward `isLen(IS)`. As with
   `safeAt`, `[total]` is broader than the guarded equations for negative
   indices, but the only callers use nonnegative indices.
9. The two `isHappySpec` equations (`:102-106`) have disjoint and exhaustive
   length guards because `isLen(IS) >= 0`. They encode the requested
   length-under-3 rule and otherwise call `happyFrom(IS,0)`.
10. The loop-summary operational rule (`:114-131`, priority 40) is
    **unsound**. The auxiliary loop claim allows the local `i` to change to
    existential `?FINAL_I`; it does not prove that `i` remains 0. The installed
    rule omits any `<scopes>` rewrite and therefore preserves `i = 0` while
    jumping directly to `#pop`.

The required false-conclusion witness for item 10 is `"abc"`:

- initial `i = 0`;
- its only window is pairwise distinct;
- fixed execution runs `AugAssign`, so `i = 1`;
- the next guard is false, and fixed execution reaches `#pop` with
  `retV(true)` and `i = 1`;
- the installed rule instead reaches the same `#pop`/return state with
  `i = 0`.

The bridge has the exact trailing `Return(True) ~> #endcall` continuation, so
the defect is not an arbitrary-suffix argument. It is a direct state-footprint
mismatch. The fact that a later fixed `#pop` would deallocate the local frame
does not make the asserted intermediate rewrite true, and the rule can prove a
false reachability claim whose destination observes that frame. The logs
listed in the Decision section demonstrate exactly that false claim.

There are no proof-local simplification rules, functional declarations, or
opaque `[symbol]` declarations. The two priorities are the `intSeqAt` bridge
at 60 and the false loop operational bridge at 40.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. The reviewer created the distinct
[spec-vacuity-reviewer.k](/audit-output/evidence/mutations/spec-vacuity-reviewer.k).
It preserves the public entry precondition and changes the result-bearing
postcondition from:

`retV(isHappySpec(IS))`

to:

`retV(notBool isHappySpec(IS))`.

This is demonstrably false for the satisfying state `L = 1`, `REST = .Map`,
`IS = [97,98,99]` (`"abc"`): both Python functions and the ground K
substitution return true, while the mutation asks for false. It is also false
on the short-string branch in the residual selected by the prover.

`kprove ... --dry-run` exits 0, so the mutation parses and builds successfully
([29-vacuity-mutation-dry-run.txt](/audit-output/evidence/logs/29-vacuity-mutation-dry-run.txt)).
The actual proof exits 1 with `WarnStuckClaimState`; its residual is at `#pop`
with `retV(false)` under `isLen(IS) < 3`, where the negated destination requires
the opposite result
([30-vacuity-mutation-proof.txt](/audit-output/evidence/logs/30-vacuity-mutation-proof.txt)).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

The candidate claim is therefore non-vacuous and result-discriminating.
Passing non-vacuity does not repair the unsound operational bridge or the
real-program pinning failure.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

The loop `#Top` establishes, under `VERIFICATION-BASE` (the supplied semantics
plus candidate `safeAt`, `happyFrom`, `isHappySpec`, copied-body macros, and
the `intSeqAt` bridge), that the specified internal loop configuration reaches
`#pop` with return value `happyFrom(IS,I)`, assuming termination and the stated
precondition.

The public `#Top` establishes, under the still larger `VERIFICATION` theory
that includes the false loop operational rule, that the manually copied
`isHappyBody` in a preconstructed environment reaches `#pop` with
`isHappySpec(IS)`, again as partial correctness.

It does **not** establish:

- termination;
- execution of the submitted `solution.mpy`;
- module loading, selected function binding, parameter binding, or call-frame
  entry for `is_happy`;
- the state-faithful loop transition asserted by `verification.k:114-131`;
- a bridge-free universal equivalence between fixed `intSeqAt` execution and
  `safeAt`;
- universal equivalence between Python strings and arbitrary K `IntSeq`
  inputs.

### Trust ledger

| Boundary | Dependents and effect | Assessment |
|---|---|---|
| K v7.1.337 frontend, Haskell/LLVM backends, Kore reachability engine, and K's `Int`, `Bool`, `Map`, `List`, and `String` hooks | All build, execution, and proof results | Necessary low-level trust boundary; tool identity and exact outputs are recorded. |
| Trusted prompt, canonical function, and translator mounted under `/reference` | Contract restatement, differential oracle, MPY identity | Acceptable trusted inputs mandated by the audit. |
| Byte-identical supplied semantics | All K execution | Correct integrity boundary for `SUPPLIED_SEMANTICS`; relevant rules were statically checked and concretely exercised. |
| Proof-local copied `isHappyBody`, `isHappyClosure`, and `solutionScope` | Public claim's program identity, binding, and body | Concerning and ultimately illegitimate here: textual equality is informal, and no actual module/call connection claim exists. The pinning mutation proves formal insensitivity to `solution.mpy`. |
| `safeAt` and the guarded `intSeqAt` bridge | Every symbolic character comparison, `happyFrom`, loop claim, and public result | Ground behavior is supported, but the required bridge-free universal connection theorem is absent; use of the same abstraction in execution and postcondition is circular. |
| Installed loop summary rule at `verification.k:114-131` | Closure of the public entry claim | Illegitimate. It fabricates a false `i = 0` intermediate state for `"abc"`; the fixed/extended witness is machine-checked. |
| Recursive `happyFrom` / `isHappySpec` equations | Meaning of the final return | Ordinary mathematics with disjoint guards and descent on intended calls; they truthfully express the window property. They do not connect the copied body to the submitted program artifact. |
| Finite differential suite | Python implementation-to-contract bridge for 8,300 recorded inputs | Useful empirical support only; no universal theorem and no replacement for K program pinning. |
| Concrete LLVM harness | Supplied semantics on selected ASCII normal/boundary executions | Finite dynamic evidence only. It does not validate the symbolic operational bridge. |
| Python `str` to K `IntSeq` correspondence | Natural-language input domain versus formal domain | Informal. Claims quantify over arbitrary integer code sequences; concrete `strToCodes` is ASCII-only. Unicode Python cases were differentially tested, but not passed through K literal conversion. |

The 25 fixed-semantics `[symbol(...)]` opaque primitives are:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. The symbolic `strLt` and total `valSeqAt` can also
remain abstract on opaque arguments. None occurs in `solution.mpy`, either
positive claim, `happyFrom`, or `isHappySpec`; consequently none can affect
this theorem's branch, return, state, exception, or postcondition. Exact source
locations are in
[37-opaque-symbols-and-proof-attributes.txt](/audit-output/evidence/logs/37-opaque-symbols-and-proof-attributes.txt).

### Gate accounting

- Fresh build and target execution: pass; both target claims print `#Top`.
- Real-program soundness (Gate A): fail; the public proof imports a concretely
  false operational bridge, lacks a universal result-bridge connection, and
  does not pin actual program execution.
- Intent adequacy (Gate B): the Python algorithm aligns with the prompt on all
  tested cases, and the recursive summary is mathematically faithful, but the
  formal entry theorem is only about a copied/prebound body state.
- Auditability (Gate C): reviewer evidence is reproducible; candidate
  generation/provenance records are absent.
- Fresh non-vacuity: pass; the negated result mutation builds and fails for the
  expected unmet obligation.

The successful differential tests and non-vacuity mutation show that this is
not a trivial free-result proof. They cannot legitimize a proof whose theory
contains a demonstrated false operational rule and whose entry claim is
insensitive to the submitted MPY program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
