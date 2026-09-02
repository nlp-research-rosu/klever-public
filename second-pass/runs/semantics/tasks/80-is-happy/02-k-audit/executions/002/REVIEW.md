# Adversarial audit: HumanEval/80 `is_happy`

The candidate is not a legitimate proof under the supplied semantics. Both
positive `kprove` runs reconstruct to `#Top`, and the theorem is
result-constraining and pinned to the submitted constructor body. However, the
public proof closes using a proof-local priority rule that is not an equivalent
acceleration of fixed execution. On the valid input `"abc"`, fixed execution
increments local `i` from 0 to 1 before reaching `#pop`; the added rule reaches
the same control point while preserving `i = 0`. A fresh pair of claims proves
the false complete-state conclusion with the extension and rejects it under
the fixed proof definition. This is a concrete Gate A operational-state
failure, not merely missing documentation.

All paths below refer to the immutable candidate or reviewer evidence. All
build products were made under `/tmp/audit-work`; no candidate-provided
compiled definition or cache was used.

## 1. Input and provenance integrity

The launcher record declares:

- problem `80-is-happy`, condition `semantics`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- a required supplied-semantics mount.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all records required for
`legacy-selected-stage1`: `invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The historical `runtime-metrics.json` absence is allowed for this layout and
was not reconstructed. I also inspected the present legacy metrics and
run-input records.

The campaign block equals `/audit-campaign-lock.json`, whose SHA-256 is the
declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The run, task, result, invocation, generation metrics, usage, prompt, final
text, unstructured log, and trace-file hashes all equal their declarations.
The 641-line JSONL trace parses completely. The 1,389,623-byte unstructured
log was read completely and treated only as an untrusted generation record.

Every launcher-declared container path exists and is readable. No entry in
the candidate, trusted inputs, or generation evidence is a symlink. The
candidate prompt and translator are byte-identical to the trusted mounts:

- prompt:
  `f6df53687ee0d5e99ab8d7b0e23ccaa81bf7bb578c1789277336f0016d402ac0`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The required `/reference/reference-semantics` exists. Recursive comparison
found the same 25 directory/file entries, types, and file bytes in
`/candidate/reference-semantics`; there are no missing, additional, changed,
mistyped, or symlinked entries. A reviewer-defined content-manifest digest was
also recorded, separately from the launcher's differently defined aggregate
tree digest. Every candidate leaf and its SHA-256 is listed in the evidence.

Evidence and exact command:

- `/audit-output/evidence/provenance_check.py`
- `/audit-output/evidence/run_provenance.sh`
- `/audit-output/evidence/provenance.log` — exit 0

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for a Python string `s`, return false when its
length is below 3; otherwise return true exactly when every consecutive
three-character window contains three pairwise distinct characters.

The trusted canonical implementation checks each window with a `for` loop.
The submitted `/candidate/solution.py` uses an equivalent `while` loop:

- reject lengths below 3;
- at each `i`, reject equality of positions `(i,i+1)`, `(i,i+2)`, or
  `(i+1,i+2)`;
- increment `i` and return true after every window succeeds.

Running the trusted translator on the submitted Python regenerates
`solution.mpy` byte-for-byte. Both files have SHA-256
`c3e43c03f7251b48bd355e973769f1b7a1991fba34f9c068144d6634bfb503dc`.

The independent differential test imports the trusted canonical function and
the candidate function from separate modules. It covers the six documented
examples, empty and length-1/2/3 boundaries, each of the three equality
branches, later-window failures, NUL and non-ASCII characters, all 9,841
strings over `{a,b,c}` of lengths 0 through 8, and 5,000 seeded strings of
length 0 through 100. There were 14,866 comparisons and zero mismatches.

Evidence:

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/run_fidelity.sh`
- `/audit-output/evidence/fidelity.log` — translator, byte comparison, and
  differential test all exit 0

## 3. Clean proof reconstruction

I copied only proof source artifacts and the trusted supplied-semantics source
tree into `/tmp/audit-work/reconstruction`. The candidate's
`kore-exec.tar.gz`, bytecode, and every candidate-created compiled definition
were ignored.

The installed live toolchain is K 7.1.293. A fresh LLVM definition built from
`reference-semantics/semantics.k`. `krun solution.mpy` terminated normally.
A reviewer assertion harness embedding an AST-identical copy of the submitted
function also terminated at `.K`, `NoExc`, exit code 0 on documented and
branch-boundary inputs.

Fresh Haskell definitions and both target proofs succeeded:

1. `kompile verification.k --backend haskell --main-module
   VERIFICATION-BASE --syntax-module VERIFICATION-BASE --output-definition
   verification-base-kompiled` — exit 0.
2. `kprove spec.k --definition verification-base-kompiled --spec-module
   LOOP-SPEC` — exact `#Top`, exit 0.
3. `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module VERIFICATION --output-definition verification-kompiled` —
   exit 0.
4. `kprove spec.k --definition verification-kompiled --spec-module SPEC` —
   exact `#Top`, exit 0.

These commands establish closure only under the respective compiled theories;
they do not by themselves validate the added rules.

Evidence:

- `/audit-output/evidence/run_reconstruction.sh`
- `/audit-output/evidence/reconstruction/summary.log`
- `/audit-output/evidence/reconstruction/prove_loop.log`
- `/audit-output/evidence/reconstruction/prove_entry.log`
- the remaining build and concrete-run logs in
  `/audit-output/evidence/reconstruction/`

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`happy-loop-correct` in `/candidate/spec.k:8` starts at the fixed-semantics
internal `#while` for an arbitrary finite code sequence `IS` and index
`I >= 0`. It requires the solution, builtins, and local frames, no pending
return or exception, and a local `s = str(IS)` and `i = I`. It claims
reachability of `#pop` with return value `happyFrom(IS,I)`. Its final local
`i` is existential (`?FINAL_I`), so the claim deliberately establishes no
specific final counter value.

`is-happy-correct` in `/candidate/spec.k:49` starts at `isHappyBody` after
parameter binding. It quantifies over every finite `IntSeq`, requires a
well-separated solution, builtins, and local frame with `s = str(IS)`, and
starts with `noRet`, `NoExc`, and exit code 0. It claims reachability of
`#pop` with `retV(isHappySpec(IS))`. The final scopes are existential, but the
return value is not: this is a result-constraining postcondition.

For both claims, a concrete satisfying state is `L = 1`, `REST = .Map`,
`scopeLoc = 2`, empty heap, `heapLoc = 0`, empty stack, and `IS` equal to any
finite code sequence. In particular:

- `IS = .IntSeq` gives false;
- `IS = [97,98,99]` (`"abc"`) gives true;
- `IS = [97,97,98]` (`"aab"`) gives false.

Ground K claims for those substitutions close together with `#Top`. Both
trusted and candidate Python implementations return the same respective
values.

### Mechanical program identity

The trusted translator regenerates the submitted module. Independently, `kast
--expand-macros` was used on the regenerated module and on the three proof
macros. The extracted `FuncDef("is_happy", Params("s"), BODY)` body and
`isHappyBody` have the same normalized KAST and SHA-256
`a65f4200713e50069968ffe67592b2dd752ce9a464429931b16c1f4b96c08e1e`.
The extracted `While` condition/body also equal `happyLoopCondition` and
`happyLoopBody`. The exact binding is recorded by `isHappyClosure` and
`solutionScope` at `/candidate/verification.k:51-56`, consistently with the
fixed `FuncDef` load rule.

A separate body-sensitivity mutation changed the final
`Return(Bool(true))` in the actually executed `isHappyBody` term to
`Return(Bool(false))`, leaving the external Python source irrelevant. The
mutated definition built successfully, and the entry proof failed with a
reachable residual containing `retV(false)` where the original summary
requires true. Thus the claim is sensitive to the executed constructor body.

Evidence:

- `/audit-output/evidence/constructor_identity.py`
- `/audit-output/evidence/constructor-identity.log` — exit 0
- `/audit-output/evidence/ground-witnesses.k`
- `/audit-output/evidence/adequacy/ground_results.log` — `#Top`, exit 0
- `/audit-output/evidence/body-sensitivity-verification.k`
- `/audit-output/evidence/body-sensitivity/summary.log`
- `/audit-output/evidence/body-sensitivity/proof.log` — expected stuck claim,
  exit 1

The theorem is not finitely bounded: `IS` is an arbitrary algebraic
`IntSeq`. Modeling a Python string as its finite sequence of character code
points is an informal representation bridge, but equality and length are the
only observations, so the formal domain does not narrow the source string
contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and used fixed-semantics path

`/audit-output/evidence/rule-inventory.txt` enumerates every module, import,
configuration, context, syntax declaration, rule, claim, and every
attribute-bearing line in the supplied semantics, `verification.k`, and
`spec.k`. Totals are 29 modules, 235 syntax declarations, 711 rules, five
contexts, one configuration, and two claims. It includes all 55 textual
priority occurrences and every `function`, `total`, `symbol`,
`no-evaluators`, `concrete`, `owise`, macro, strictness, and sequencing
attribute. There are no candidate simplification rules.

The supplied tree is the fixed semantics selected by this
`SUPPLIED_SEMANTICS` condition. The whole tree was inventoried; only the
following constructor path can contribute to this program:

| Program construct | Fixed declaration/execution rules |
|---|---|
| `Module`, `FuncDef`, params and statement sequencing | `syntax.k`, `core.k` `#loadAll`/statement rules, `functions.k` function binding |
| `Name`, `len`, calls | `core.k` scope lookup and argument evaluation; `call.k` callee/argument dispatch; `builtins.k` `len`/`seqLen` |
| integer/Boolean literals and `+`, `<`, `==` | `core.k`, `operators.k`, `int.k`, `str.k` |
| `If` | strict syntax plus `controls.k` `#branch` |
| `Assign`, `AugAssign` | `controls.k` current-frame updates |
| `While` | `controls.k` `While => #while`, condition, loop label, and exit rules |
| string indexing | `subscript.k` contexts, `applyIndex`, and `intSeqAt` |
| `Return`/`#pop` | `functions.k` return and frame-pop rules |

Evaluation is left-to-right where material. The used operations neither
allocate nor mutate heap, output, or external state. The arbitrary `IntSeq`
model supports every equality/length case needed by the source contract. The
many fixed float, sorting, hashing, collection, comprehension, method, and
dictionary rules are constructor-disjoint and unreachable from this program.

### Candidate-local inventory

Every proof-local extension is classified below.

| Extension | Classification and result |
|---|---|
| `happyLoopBody`, `happyLoopCondition`, `isHappyBody` macros | Semantically inert names for constructor terms. Mechanical KAST equality passes. |
| `isHappyClosure` | Definitional constant for the exact parameter, body, and module scope. Sound. |
| `solutionScope` | Definitional constant binding only `is_happy` to that closure with builtins parent. Sound. |
| `safeAt` and its two equations | In-bounds structural accessor. Equations descend and agree with fixed `intSeqAt`; the `[total]` declaration leaves negative/out-of-bounds cases uninterpreted rather than equation-covered. All uses in `happyFrom` are guarded in-bounds. |
| priority rule `intSeqAt(IS,I) => safeAt(IS,I)` | Result-bearing operational bridge, guarded by `0 <= I < isLen(IS)`. Its equations are mathematically equal to fixed access by structural induction, and it changes no cells. The candidate supplies no bridge-free universal K connection theorem, so this remains an evidence/trust limitation even though no false in-bounds witness was found. |
| five `happyFrom` equations | Definitional summary. For `I >= 0`, the terminal and nonterminal guards partition the domain; the three equality failures and all-distinct recursive case are disjoint; recursion increases `I` toward the finite length. No dependent call uses `I < 0`. |
| two `isHappySpec` equations | Disjoint and exhaustive because `isLen(IS) >= 0`; they implement the length threshold and start the window scan at 0. |
| priority loop rule at `/candidate/verification.k:114-131` | Operational bridge installed for the public proof. **Unsound:** it skips real loop execution while preserving the local scope, including `i = 0`. The bridge-free loop theorem permits `i => ?FINAL_I` and therefore does not prove preservation of 0. |

The intended justification for the last rule is
`happy-loop-correct`, but its justification domain and conclusion are not the
rule's complete state transition:

1. The fixed `While` performs an inert step to `#while`, so the one-step
   syntactic difference is harmless.
2. The loop theorem correctly constrains the returned `happyFrom` value, but
   explicitly leaves final `i` unconstrained.
3. The installed rule omits any `<scopes>` rewrite. K therefore preserves
   `i = 0`, which is false whenever an all-distinct nonempty window executes.
4. The rule also omits the loop theorem's global/builtins-frame guards and
   several cells, so its match domain is broader than its justification
   domain. The concrete state witness below already fails even with all of
   those well-formed conditions satisfied.

### Required false-conclusion witness

`/audit-output/evidence/bridge-state-witness.k` uses the intended input
`"abc"` and the same valid solution, builtins, and local frames as the entry
theorem. It asks whether execution can reach `#pop`, return true, and still
have local `i = 0`.

- Under `VERIFICATION-BASE` (no loop bridge), `kprove` exits 1 with
  `WarnStuckClaimState`. Its residual is the real fixed-semantics state:
  `#pop`, `retV(true)`, and **`"i" |-> 1`**.
- Under `VERIFICATION` (bridge enabled), the identical false claim prints
  `#Top` and exits 0, preserving **`"i" |-> 0`**.

Exact commands and outputs are in:

- `/audit-output/evidence/adequacy/fixed_state_preservation.log`
- `/audit-output/evidence/adequacy/extended_state_preservation.log`
- `/audit-output/evidence/adequacy/summary.log`

This is a symbolic/concrete false conclusion enabled by the candidate rule on
a valid state and an intended-domain input. Although the public postcondition
existentially hides final scopes and the next real `#pop` would discard the
local frame, the extension itself changes the selected transition system and
can prove a false state property. The validation contract requires operational
bridges to preserve every affected cell, not only the final Boolean. This is
the fatal soundness defect.

## 6. Fresh non-vacuity test

I did not use any candidate vacuity artifact. The fresh module
`/audit-output/evidence/spec-vacuity.k` takes the satisfiable ground input
`"abc"` and changes the result-constraining postcondition from true to false.
The mutation parses and reaches the prover. `kprove` exits 1, prints
`WarnStuckClaimState`, and shows the expected unmet obligation: the reached
state contains `retV(true)` while the target requires `retV(false)`. It is not
a parser failure, missing import, timeout, or unrelated crash.

Evidence:

- `/audit-output/evidence/run_vacuity.sh`
- `/audit-output/evidence/vacuity.log` — no `#Top`, stuck claim present,
  exit 1

The original theorem is therefore non-vacuous and result-discriminating. This
does not repair the unsound operational bridge.

## 7. Proven versus assumed accounting

### What the successful runs establish

The loop run establishes, under `VERIFICATION-BASE` (fixed supplied semantics
plus `safeAt`, its in-bounds indexing bridge, and the declarative functions),
that the internal loop reaches `#pop` with return
`happyFrom(IS,I)` for arbitrary finite `IS` and `I >= 0`; it does not
establish a final value of local `i`.

The entry run establishes, under the larger `VERIFICATION` rewrite theory,
that the exact submitted body reaches `#pop` with
`retV(isHappySpec(IS))`. It is a theorem of that extended theory. Because the
larger theory contains the false loop transition demonstrated above, this is
not a sound reachability proof of the real generated program.

### Trust ledger

| Boundary | Influence and assessment |
|---|---|
| Supplied MPY semantics and K 7.1.293 compiler/Haskell/LLVM/SMT stack | Defines syntax, execution, and proof checking. This is the condition-selected fixed trust boundary; it was rebuilt from byte-verified sources. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy`. Byte regeneration and KAST comparison pass. |
| Direct-body claim versus a complete call | Fixed `FuncDef`, closure, scope, and call rules plus mechanical constructor equality connect the claim to the same function binding/body. Argument-evaluation behavior is not itself restated in the entry claim, but the prestate is exactly the post-binding frame. Acceptable for this immutable candidate. |
| `safeAt`/`intSeqAt` bridge | Affects every indexed character and hence branches and result. In-bounds equality follows by ordinary structural induction and has finite concrete support, but there is no separate bridge-free universal K theorem. This would be a non-fatal validation limitation if it were the only issue. |
| `happyFrom`/`isHappySpec` meaning | Ordinary induction equates the equations with “all consecutive triples are pairwise distinct.” A separate finite check mirrors the equations and compares them with both Python implementations on 14,841 inputs with zero mismatches (`summary-differential.log`). Testing is supporting evidence, not the universal proof. |
| Loop priority rule | Influences control, result, and local state and is required by the public proof stage. Its result is related to the loop theorem, but its state transition is false. This boundary is illegitimate and fatal. |
| Imported opaque fixed symbols | `md5hexCodes`, `sortVS`, `sortKeyVS`, and the float-family opaque symbols (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`) are present in the supplied theory but unreachable from this program and have no dependent target claim. |
| Python-string to finite `IntSeq` representation | Informal intent bridge. The theorem quantifies over all finite integer sequences, and this program observes only sequence length and integer equality, so it covers rather than narrows Python strings. |
| Differential and concrete tests | Finite evidence for implementation fidelity and summary intent only. They are not used as substitutes for K reachability. |

Gate A (real-program soundness) fails because of the witnessed operational
state mismatch. Intent/domain adequacy and non-vacuity otherwise pass, and the
evidence is reproducible. Under the benchmark decision boundary, a successful
`#Top` obtained in a theory containing this materially unsound proof rule is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
