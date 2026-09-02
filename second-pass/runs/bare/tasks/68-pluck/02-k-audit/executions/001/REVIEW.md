# Independent adversarial audit: 68-pluck

This audit used K v7.1.293 and rebuilt from candidate source copies under
`/tmp/audit-work`. Candidate-provided `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, prose, logs, and traces were never
used as executable authority.

The reconstructed positive claim does print `#Top`, the submitted Python
program is correct, and a fresh false-result mutation is rejected. The K proof
is nevertheless not legitimate. On its formal entry path the generated
semantics reduces the property-bearing comprehension/min operation to the
undefined function `minEvenArray`; `verification.k` then gives that function
the desired scan result directly. There is no execution claim or connection
theorem deriving this equation from fixed semantics. An opposite completion of
the same undefined function makes K prove the exact submitted program returns
`[]` for every abstract array, including the satisfying input `[2]`, for which
both real Python implementations return `[2, 0]`. Thus the candidate's `#Top`
is closure under an answer-supplying proof equation, not a proof of the real
program computation.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- `/reference` contains exactly the regular files `canonical.py`, `prompt.py`,
  and `py2mpy.py`.
- `/reference/reference-semantics` does not exist, as required for
  `GENERATED_SEMANTICS`.
- Candidate `prompt.py` is byte-identical to trusted `/reference/prompt.py`
  (SHA-256
  `cd3be7d4325387ffeafdc0c15742e1e5f66dfe1e94b683910809f5c17a9c3a74`).
- Candidate `py2mpy.py` is byte-identical to trusted `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- All required generation/source artifacts are present as ordinary files:
  `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, one
  structured JSONL trace, `prompt.py`, `py2mpy.py`, `solution.py`,
  `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
  No symlink occurs anywhere under `/candidate`.
- There are no generated helper `.k` files beyond `semantic.k`,
  `verification.k`, and `spec.k`. `PROOF.md` and a candidate vacuity spec are
  absent, but neither was a required deliverable under the recorded bare
  generation prompt.
- Extra candidate artifacts are the two compiled-definition trees and a Python
  bytecode cache. They are untrusted build/cache output, were not copied into
  the reconstruction, and do not alter the source-integrity result.

The untrusted records claim a successful 1,436-second generation, six concrete
executions, and a final `#Top`. The 37,161-line output log also contains earlier
compiler/prover errors, and the 335-record structured trace ends with the same
success claim. Those records were read only as history; the fresh results below
are independent. Full bounded extraction, hashes, artifact types, JSON values,
trace counts, and command status are in
[`stage1-provenance.log`](evidence/stage1-provenance.log) (exit 0), produced by
[`inspect_provenance.py`](evidence/inspect_provenance.py).

Infrastructure boundary: **PASS**. Candidate provenance integrity: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `prompt.py` and `canonical.py`: for a finite array of non-negative
integers, return `[v, i]`, where `v` is the smallest even value and `i` is the
smallest index having that value. Return `[]` if the array is empty or has no
even member. Although the constraints say length 1 through 10,000, the prose
and an explicit example require the empty case, so this audit used lengths
0 through 10,000.

Candidate `solution.py` computes the lexicographic minimum of pairs
`[value,index]` produced for even values, with `default=[]`. Lexicographic
ordering first minimizes the value and then the index, so the algorithm matches
the contract on the intended integer domain. It is a different but equivalent
algorithm to the trusted filter/min/index implementation.

### Translator identity

Running the trusted translator on the copied `solution.py` regenerated a file
byte-identical to submitted `solution.mpy`; both have SHA-256
`e34a42c21da1effe94a40dbff2a858b9cddfc8a37602c74ba62efcc157366b26`.
The exact command and exit 0 are in
[`stage2-translation.log`](evidence/stage2-translation.log).

### Independent differential test

[`differential_pluck.py`](evidence/differential_pluck.py) independently imports
trusted `canonical.pluck` and candidate `solution.pluck`. It checked:

- all four documented examples;
- explicit empty, singleton, zero, no-even, tie, minimum-at-front/end, and very
  large integer boundaries;
- all 55,987 arrays of lengths 0 through 6 over values 0 through 5;
- 1,000 deterministic generated arrays (seed 680068), lengths 0 through 100,
  values 0 through \(10^{12}\);
- four length-10,000 cases covering all odd, last zero, competing first/last
  even values, and all-equal evens.

All 57,006 cases agreed, raised no exceptions, and preserved their inputs.
The script, exact generated-input scope, fixed inputs and outputs, command,
zero-mismatch summary, and exit 0 are in
[`stage2-differential.log`](evidence/stage2-differential.log).

Program fidelity: **PASS**.

## 3. Clean proof reconstruction

Only copied sources in `/tmp/audit-work/candidate-source` were used. Fresh
output directories were created below `/tmp/audit-work/build`; no candidate
definition or cache was referenced.

### Generated-semantics build and execution

Fresh LLVM compilation of `semantic.k` exited 0
([`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)). Importantly, it
diagnosed non-exhaustive `[total]` functions including `minEvenArray`,
`arrayAt`, `headInt`, `tailInts`, and `bindParams`.

Eight independently selected normal/boundary `VList` executions (the examples,
empty, all odd, tie, zero, and a later even) all terminated with an empty
`<k>` cell and matched both Python implementations. Commands, complete final
configurations, comparisons, and exit 0 are in
[`stage3-semantic-differential.log`](evidence/stage3-semantic-differential.log);
the driver is
[`semantic_python_differential.py`](evidence/semantic_python_differential.py).

This concrete success exercises the separate `VList -> minEvenInts` path. It
does not validate the entry proof's `VArray -> minEvenArray` path. Running the
base generated semantics on `VArray(68,0,1)` exits 113 at the residual
`minEvenArray(68,0,1)`:
[`stage5-base-semantics-varray.log`](evidence/stage5-base-semantics-varray.log).

### Proof build and all positive claims

Fresh Haskell compilation of `verification.k` exited 0
([`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)). `spec.k`
contains exactly one, unlabeled entry claim and no helper/loop claims. The
independent command

```text
kprove /tmp/audit-work/candidate-source/spec.k \
  --definition /tmp/audit-work/build/verification-kompiled-fresh \
  --spec-module SPEC
```

exited 0 and printed `#Top`; see
[`stage3-kprove-positive.log`](evidence/stage3-kprove-positive.log).

Dynamic reconstruction: **PASS as K-theory closure**. It is not by itself a
soundness result; Stages 4 and 5 reject the theory extension that causes this
closure.

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The sole claim starts with:

- `<k> solutionProgram ~> start`;
- arguments `VArray(ID,0,LENGTH)`;
- empty environment, function map, and stack;
- result `VNone`;
- arbitrary integers `ID` and `LENGTH`, constrained only by
  `LENGTH >=Int 0`.

The array elements do not reside in the configuration. They are observed only
through the undefined function `arrayAt(ID,OFFSET)`. Thus the formal input is
an abstract oracle-backed array, not the concrete `VList` representation used
in the successful semantics tests.

### Postcondition in plain language

At completion the claim requires:

- an empty `<k>` cell;
- the environment and stack restored to empty;
- the function map exactly `solutionFunctions`;
- the result exactly
  `specScanArray(ID,0,LENGTH,0,0,0,0)`.

The scan's equations return `[]` if no even value is found, otherwise the
smallest even value and its earliest zero-based index. The result is genuinely
constrained: there is no fresh/free right-hand-side result variable, tautology,
or one-way implication.

### Program identity

`verification.k` lines 70–84 expand `pluckBody` and `solutionProgram` to the
same constructor tree as submitted `solution.mpy`, including the comparison,
comprehension, `enumerate`, `min`, and empty default. Lines 86–87 give the
matching loaded function map. This exact-tree inspection, together with the
trusted byte-identical regeneration in Stage 2, adequately pins the syntax of
the submitted body. There are no helper or loop claims to misalign with control
flow.

### Satisfiable ground instances

[`stage4-array-witness.k`](evidence/stage4-array-witness.k) supplies ground
interpretations of `arrayAt` for five IDs, giving the arrays `[4,2,3]`, `[]`,
`[7,5,9]`, `[2,2]`, and `[5,0,3,0,4,2]`. These exhibit realizable states with
`LENGTH >= 0`. Fresh compilation exited 0
([`stage4-array-witness-kompile.log`](evidence/stage4-array-witness-kompile.log)).
Executing the actual submitted `solution.mpy` at the corresponding `VArray`
inputs produced `[2,1]`, `[]`, `[]`, `[2,0]`, and `[0,1]`, equal to both Python
implementations. Commands and exit 0 are in
[`stage4-ground-witness.log`](evidence/stage4-ground-witness.log), driven by
[`stage4-ground-witness.py`](evidence/stage4-ground-witness.py).

These finite instances show that the asserted scan gives the intended values
when `arrayAt` is supplied consistently. They do not prove that the fixed
semantics computes the scan. That missing universal connection is material:
fixed `semantic.k` cannot execute this entry representation at all.

Syntax pinning and result constraint: **PASS**. Real-execution/value pinning:
**FAIL**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`stage5-rule-inventory.md`](evidence/stage5-rule-inventory.md). It enumerates
all 23 `syntax` declarations, the configuration, and all 70 rule starts in
`semantic.k`; all four syntax declarations and all 13 rule starts in
`verification.k`; and the sole claim in `spec.k`. The machine-extracted
declaration/rule starts are independently preserved in
[`stage5-local-declarations.log`](evidence/stage5-local-declarations.log).
There are no local `[functional]` declarations, simplification rules, imported
helper K files, or auxiliary claims. The three priority rules are explicitly
inventoried.

### Used-construct coverage and normal control

Every submitted constructor is declared: `Module`, `FuncDef`, `Params`,
`Return`, `Call`, `Name`, `ListComp`, `ListExpr`, `CompFor`, `TupleExpr`,
`Compare`, `BinOp`, `Int`, `CmpOp`, and `KwArg`, plus their list sorts.
Module loading, function registration, argument binding, frames, explicit
return, caller restoration, and result storage preserve the relevant cells and
the exact continuation for the used path. Concrete `VList` processing uses
structurally descending `minEvenInts`; its parity cases are disjoint, and its
`<=` tie case correctly retains the earlier head index.

The contract scan in `verification.k` is also ordinary correct mathematics on
`LENGTH >= 0`: length decreases, parity cases cover all integers, the first
even initializes the best, only a strictly smaller later value replaces it,
and equality preserves the earlier index.

### Material proof-extension failure

The critical chain is:

1. `semantic.k` lines 217–225 replace the exact comprehension on a `VArray`
   with `VCandidatesArray(ID,OFFSET,LENGTH)`.
2. Lines 231–232 replace its `min(...,default=[])` consumer with
   `minEvenArray(ID,OFFSET,LENGTH)`.
3. `semantic.k` lines 60–61 declare `minEvenArray [function,total]` but give it
   no equation. The fresh compiler reports this, and base execution demonstrably
   stops there.
4. `verification.k` lines 62–63 add the only equation:
   `minEvenArray(...) => specScanArray(...)`, exactly the requested result.

This is a program-derived, result-bearing operational bridge, not a harmless
name for an already computed value. It has no auxiliary reachability claim from
the exact comprehension/min configuration, no equation in fixed semantics, and
no universal theorem showing that fixed execution produces the scan. The same
fresh symbol occurs on the operational path and is then defined to the
postcondition summary; that is circular answer injection under the proof
extension contract.

The scan equation itself describes the right mathematical answer if adopted as
an axiom. The defect is that the proof does not derive it. The required false
conclusion/value-sensitivity witness is concrete:

- [`stage5-wrong-oracle-verification.k`](evidence/stage5-wrong-oracle-verification.k)
  gives the otherwise unconstrained `minEvenArray` the opposite interpretation
  `[]`, while retaining the exact submitted program tree.
- [`stage5-wrong-oracle-spec.k`](evidence/stage5-wrong-oracle-spec.k) claims the
  program returns `[]` for every nonnegative length.
- Fresh Haskell compilation exits 0
  ([`stage5-wrong-oracle-kompile.log`](evidence/stage5-wrong-oracle-kompile.log)),
  and the corrected proof command exits 0 with `#Top`
  ([`stage5-wrong-oracle-kprove-corrected.log`](evidence/stage5-wrong-oracle-kprove-corrected.log)).
- Input `[2]` satisfies the domain, yet Stage 2 records both real Python
  implementations returning `[2,0]`. Therefore the opposite completion enables
  a demonstrably false theorem on the intended domain.

An initial reviewer invocation omitted the K include path and exited 113; it is
retained transparently in
[`stage5-wrong-oracle-kprove.log`](evidence/stage5-wrong-oracle-kprove.log).
The corrected parse/proof result above is the relevant experiment.

### Other inventoried limitations and witnessed false rules

- `arrayAt` is another equation-free `[function,total]` symbol. It can be an
  acceptable external symbolic-input observer only if its interpretation and
  the `VArray`-to-real-list bridge are explicit. It does not justify
  `minEvenArray`.
- The exact comprehension rules at semantic lines 208 and 217 accept arbitrary
  continuations, but their `VCandidates*` pseudo-values are justified only for
  the subsequent `minDefaultEmpty` consumer. False-context witness: directly
  returning the same comprehension on intended input `[2]` should return
  `[[2,0]]`, while these rules expose `VCandidates(2)` as the observable result.
- Extra, unused slice/index rules are globally inaccurate. Witnesses are
  `[][1:]` (Python returns `[]`, but `tailInts(.Ints)` is undefined), an empty
  `VArray` tail slice (the rule fabricates length -1), and index 0 of an empty
  array (Python raises `IndexError`, while the rule produces `arrayAt`). These
  forms are not used by submitted `solution.mpy`, so they are additional
  language-definition defects rather than the main target-path failure.
- `[total]` is unjustified for `chooseEven` over all declared `Val` results,
  `headInt`/`tailInts` on empty lists, `bindParams` on arity mismatch,
  `specScanArray` at negative lengths, and both opaque array functions. The
  actual positive path narrows several of these cases, but the attributes do not
  prove coverage.

Gate A (real-program soundness): **FAIL**. Gate B (intent adequacy): **FAIL**
because the universal claim is over an unconnected oracle-backed `VArray`
rather than real/concrete Python-list execution. Gate C (trust/evidence): the
finite evidence is reproducible, but it cannot replace the missing universal
connection theorem.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The audit created
[`stage6-spec-vacuity-audit.k`](evidence/stage6-spec-vacuity-audit.k), preserving
the exact entry state and changing the result obligation to `VList(.Ints)` for
every nonnegative length. This is false for the satisfying input `[2]`, whose
real result is `[2,0]`.

The mutation parses/builds successfully: `kprove --dry-run` exits 0 and emits a
valid `kore-exec` command
([`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)). The actual
proof exits 1 with `WarnStuckClaimState`; its residual specifically reports the
failed implication
`VList(.Ints) #Equals specScanArray(ID,0,LENGTH,0,0,0,0)`, followed by the
expected prover error
([`stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log)).

The positive claim is therefore result-constraining and non-vacuous under the
candidate theory. This does not repair the answer-supplying equation in that
theory.

Non-vacuity gate: **PASS**.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the combined theory formed by `semantic.k` plus every equation in
`verification.k`, for arbitrary `ID` and `LENGTH >= 0`, executing the exact
submitted constructor tree with argument `VArray(ID,0,LENGTH)` reaches an empty
computation, restores environment/stack, loads the expected function map, and
returns `specScanArray(ID,0,LENGTH,0,0,0,0)`.

That statement is conditional on the verification equation defining the
program-derived `minEvenArray` result to be exactly `specScanArray`. Because
that condition is the substantive correctness property, the reachability proof
does not independently establish the requested program theorem.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Installed K integer, Boolean, string, map, list, equality, parser, LLVM, and Haskell implementations | Arithmetic, paths, state, compilation/proof | Ordinary low-level toolchain trust; acceptable. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Accepted mounted authority; byte identity was independently checked. |
| Trusted `canonical.py` and natural-language reading | Intent oracle for differential tests | Appropriate for adequacy evidence, not a K theorem. |
| `arrayAt(ID,OFFSET)` | Every abstract array element and hence every result branch | Can be an external interpretation-parametric input primitive, but its `[total]` declaration lacks equations and the `VArray`/real-list representation bridge is only informal/finite. Concerning but not alone fatal if a genuine program connection theorem existed. |
| `VCandidates*` exact comprehension bridges | Replaces binder iteration, `%`, filtering, nested-list allocation, and candidate production | Task-specific operational summaries. The concrete `VList`/`minEvenInts` consumer has strong finite support and truthful recursive equations, but the arbitrary continuation match is unsound outside that consumer. |
| `minEvenArray` in fixed semantics | Entire result-bearing comprehension/min value on the entry path | Opaque and non-executable; illegitimate as a program-derived oracle. |
| `minEvenArray => specScanArray` in `verification.k` | Supplies the exact final postcondition value | Illegitimate answer-encoding operational bridge; no connection theorem. This is the decisive failure. |
| Python differential and eight concrete K `VList` runs | Implementation-to-intent and concrete-semantics evidence on tested inputs | Reproducible finite evidence only. They exercise a different input/summary path and cannot universally prove the `VArray` bridge. |
| Five ground `VArray` interpretations | Satisfiability and concrete substitution | Shows asserted results are plausible when `arrayAt` is supplied consistently; still conditional on the same proof equation. |
| Partial-correctness termination premise | Theorem only concerns terminating executions | Ordinary reachability-proof boundary. The contract scan itself structurally terminates for nonnegative finite length. |

### Decision

The candidate Python implementation is correct and the formal claim is
non-vacuous, exact-result-constraining, and syntactically pinned. Nevertheless,
the only universal K entry proof obtains the result from an undefined,
program-derived function whose proof-local equation restates the desired scan.
The machine-checked opposite interpretation proves a false result for `[2]`.
This meets the decision boundary for a materially unsound/answer-encoding proof
extension and is not a legitimate partial-correctness proof of the real
generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
