# Independent adversarial audit: 20-find-closest-elements

The candidate reconstructs to `#Top`, and its Python implementation agrees well
with the trusted canonical implementation. It is nevertheless not a legitimate
proof of that implementation. The symbolic proof skips the property-bearing
`While` with a priority operational rule that writes the desired exhaustive-scan
summary directly. No bridge-free reachability theorem connects the real loop to
that summary. The result-bearing summary symbols are then repeated in the
postcondition. A material mutation of the displaced loop computation leaves the
claim at `#Top`, while fixed execution of that mutation has a concrete wrong
result. In addition, the claim invokes a manually copied body and never reads
the submitted `solution.mpy`.

This is a candidate failure, not an infrastructure failure. The trusted mounts
match `SUPPLIED_SEMANTICS`, K is available, fresh builds work, and the required
positive claim closes.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present as required for
`SUPPLIED_SEMANTICS`. The candidate `reference-semantics/` tree has exactly the
same directories and regular files, no symlinks, and no missing, additional,
mistyped, or byte-different entries. Recursive `diff --no-dereference` exited
0. The candidate `prompt.py` and `py2mpy.py` are also byte-identical to their
trusted counterparts. Exact types, hashes, comparisons, and commands are in
[01-integrity.log](evidence/01-integrity.log) and
[01-integrity.cmd](evidence/01-integrity.cmd).

There is therefore no rendered-mode/mount contradiction and no basis for
`AUDIT_ERROR`.

### Provenance artifacts

The following requested generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present at candidate top level. These are
provenance/auditability gaps, not the source of the proof verdict. The available
proof sources (`solution.py`, `solution.mpy`, `spec.k`, and `verification.k`)
are regular files. Candidate `__pycache__/` is a built cache and was neither
copied into the clean proof source set nor trusted. Candidate `prove.sh` and
concrete tests were inspected only as untrusted claims.

All execution inputs were copied from source to
`/tmp/audit-work/reconstruction`; the supplied semantics in that tree was
copied from the trusted `/reference` mount, not from a candidate cache.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of at least two floating-point numbers, return two elements from
distinct positions whose absolute difference is minimal, ordered smaller first.
Duplicates are permitted and can therefore yield `(x, x)`. The prompt does not
specify a tie policy; the trusted canonical implementation keeps the first
minimum encountered by its nested index order.

The candidate initializes from indices `(0,1)`, orders that pair, then
enumerates every unordered pair `(i,j)` with `i < j`. It orders each candidate
pair, updates only on a strictly smaller gap, and therefore preserves the same
first-minimum behavior as the canonical directed-pair scan.

### Translation identity

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`. `cmp` exited 0, and both artifacts have SHA-256
`f0f84a4058e0dc8d831ac3e6be24da7f226d1a48d036f3c4e9d5ff24ed40750b`.
See [02-regenerate-mpy.log](evidence/02-regenerate-mpy.log) and the preserved
[regeneration script](evidence/regenerate_mpy.sh).

### Independent differential testing

The reviewer-authored [differential_test.py](evidence/differential_test.py)
imports `/reference/canonical.py` independently from the scratch candidate
module. Its corpus includes:

- both documented examples;
- empty and singleton boundary inputs;
- initial swap/no-swap, later swap/no-swap, update/no-update, wrap, duplicate,
  negative, fractional, strict-tie, signed-zero, infinity, and NaN cases;
- all 19,525 lists of lengths 2 through 6 over
  `[-3.0, -1.0, 0.0, 1.0, 3.0]`;
- 1,500 deterministic generated lists of lengths 2 through 12.

There were 21,039 intended-domain cases and zero mismatches. Complete inputs
are preserved in
[differential_inputs.json](evidence/differential_inputs.json); command and
summary are in [03-differential.cmd](evidence/03-differential.cmd) and
[03-differential.log](evidence/03-differential.log).

For the two out-of-contract inputs, the canonical implementation returned
`None`, while the candidate raised `IndexError`. This does not violate the
stated length-at-least-two contract, but it is an explicit excluded behavior.

Program fidelity therefore passes as finite evidence. It does not compensate
for a missing K connection proof.

## 3. Clean proof reconstruction

K v7.1.337 was independently available at `/usr/bin/kompile` and
`/usr/bin/kprove`. No candidate-built definition was reused.

The clean commands were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The LLVM build exited 0
([04 log](evidence/04-kompile-runtime.log)); the Haskell proof build exited 0
([05 log](evidence/05-kompile-verification.log)). `spec.k` contains one positive
target claim, `[entry-point]`. Its fresh proof exited 0 and printed `#Top`
([06 log](evidence/06-kprove-positive.log)).

The independent concrete harness embeds a function AST identical to
`solution.py` and checks six ordinary/boundary examples. AST identity and fixed
LLVM execution both exited 0
([08 log](evidence/08-harness-fidelity.log),
[10 status](evidence/10-krun-concrete.status)). The same ground harness also
exited 0 under an independently compiled LLVM definition containing the proof
extensions ([12 build](evidence/12-kompile-verification-llvm.log),
[13 status](evidence/13-krun-bridge-enabled.status)).

An optional reviewer ground `kprove` attempt encountered the Haskell backend's
documented missing `FLOAT.gt` hook and exited 1
([11 log](evidence/11-kprove-ground.log)). This is not used against the
candidate: the positive symbolic proof, LLVM concrete execution, and Python
ground substitution all remained available.

Stage 3 reconstruction passes: the candidate really does obtain fresh
`#Top`. The remaining stages determine that this `#Top` is obtained under an
illegitimate proof extension.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim begins in the standard empty module configuration and directly
invokes:

```text
closureVal(("numbers", .ParamNames), findClosestBody, 0)
```

on an unboxed list
`floatVals(fCons(A, fCons(B, FS)))`. Its precondition is
`0 <=Int floatSeqLen(FS)`, so the full input always has at least two Float
elements. It demands a tuple whose first and second elements are respectively
`closestLowVS` and `closestHighVS`, starting the modeled scan at `(i,j)=(0,1)`
with the ordered `(A,B)` pair. It also demands restoration of the original
environment, scopes, heap, stack, return, exception, and exit-code cells.

This is an equality-style result constraint, not a free result variable or a
one-way implication. Stage 6 confirms it is discriminating.

### Satisfiable precondition and substitutions

For example, take `A = 2.0`, `B = 1.0`, and `FS = .FloatSeq`. Then
`floatSeqLen(FS) = 0`, satisfying the precondition, and the ground scan equations
give `(1.0, 2.0)`. The reviewer substituted this state and both documented
examples into a direct implementation of the formal `PairState/scanPairsVS`
equations and compared them with both Python entry points. All three agreed:

```text
[2.0, 1.0]                         -> (1.0, 2.0)
[1.0, 2.0, 3.0, 4.0, 5.0, 2.2]  -> (2.0, 2.2)
[1.0, 2.0, 3.0, 4.0, 5.0, 2.0]  -> (2.0, 2.0)
```

See [formal_substitution_check.py](evidence/formal_substitution_check.py) and
[14-formal-substitution.log](evidence/14-formal-substitution.log).

### Pinning failure

The `<k>` cell does not load or parse `/candidate/solution.mpy`. It skips the
submitted `Module`, its `ImportFrom`, its `FuncDef`, and normal entry-point name
lookup. Instead, `verification.k` manually defines `findClosestBody` and the
claim manually constructs a closure around it.

The copied body currently matches the translated function body by static review,
and the concrete harness confirms AST identity. That is useful evidence, but it
is not proof-local body sensitivity. The reviewer changed the submitted scratch
`solution.mpy` return from `(best_low,best_high)` to the materially wrong
`(best_high,best_low)`, then rebuilt the K definition and reran the claim. The
proof still exited 0 with `#Top`, because neither `verification.k` nor `spec.k`
reads `solution.mpy`. Exact mutation, hashes, build, and proof are preserved in
[solution-body-mutation.mpy](evidence/solution-body-mutation.mpy) and
[15-body-sensitivity.log](evidence/15-body-sensitivity.log).

Thus the formal target is a manually substituted AST, not a proof
cryptographically or syntactically driven by the submitted program artifact.
More importantly, even that copied AST's loop is not executed, as Stage 5
shows.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer rebuilt an inventory from `semantics.k`, all 23 supplied helper K
files, `verification.k`, and `spec.k`. It contains 978 individually
line-addressed entries:

- 244 syntax declarations;
- 727 rules;
- 1 configuration;
- 5 contexts;
- 1 claim.

Attributes are independently tagged: 159 function declarations, 119 `total`,
26 `symbol`, 23 `no-evaluators`, 46 priority rules, 37 concrete rules, 2
simplification rules, 26 `owise`, 6 macro plus 1 macro-rec declaration, and 616
ordinary rules. There are no local `functional` declarations.

Every row has an audit decision and rationale in
[k_inventory_review.tsv](evidence/k_inventory_review.tsv). The extraction tool
and corrected run are
[inventory_k.py](evidence/inventory_k.py) and
[07b-inventory-corrected.log](evidence/07b-inventory-corrected.log).

The 928 supplied-semantics entries are byte-identical to the trusted fixed
baseline and therefore accepted as the selected semantics level. Intentional
baseline abstractions such as opaque sorting, ASCII strings, assertion handling,
and partial builtin coverage are unused by this program. The exact program-used
syntax-to-rule mapping is
[used_construct_map.tsv](evidence/used_construct_map.tsv). It covers module
loading, imports, functions/calls/returns, scopes, name lookup, assignment,
subscript, tuple unpacking, evaluation order, `If`, `While`, integer operations,
opaque float operations, and all affected cells.

The 49 proof-local entries and the target claim are summarized below; the TSV
enumerates them without grouping.

### Proof-local definitions

1. **AST fragments, `verification.k:7-57`.** The loop condition and body macros,
   and the `findClosestBody` equation, textually match the translated function.
   Their ordinary syntax is accurate. The body is nevertheless a manual copy,
   giving the pinning gap described above.

2. **Float-list conversion and access, lines 58-80.** `floatVals` and
   `floatSeqLen` are structurally exhaustive and descending. The
   `vsLen(floatVals(FS))` simplification agrees with the baseline recursive
   length. `floatAt` and the specialized `valSeqAt` equation are correct for
   in-bounds indices. `floatAt` is declared `total` outside those equations;
   for example `floatAt(.FloatSeq,0)` and an index beyond a two-element list
   have no evaluator equation. The LLVM compiler reports this
   non-exhaustiveness. This is an over-broad abstract totalization, not a false
   equation on the target path, whose indices are in bounds.

3. **Pair definitions, lines 87-116.** Projections and tuple construction are
   ordinary constructor equations. `orderPairState` and `considerPair` use
   `gtF` versus `notBool gtF`; their guards are disjoint and exhaustive.
   `considerOrdered` uses strict `floatLt` on ordered gaps and therefore
   preserves the earlier pair on ties. These equations match the candidate's
   update logic under the supplied float primitives.

4. **Recursive scan models, lines 124-177.** On the invariant
   `0 <= I < J < len`, `scanPairs`/`scanPairsVS` enumerate `(i,j)` in the same
   lexicographic order as the real loop, incrementing `j` or advancing
   `(i,j)` at the list boundary. Their valid-domain equations descend.
   Their `total` declarations extend beyond that invariant; arbitrary bad
   indices can access out of bounds or fail to descend. `lastOrderedPair` is
   unused and lacks a length-at-least-two guard. These are localized helper
   scope/totality gaps; no intended-domain false equation was found.

5. **Opaque projections, lines 185-200.** `closestLowVS` and `closestHighVS`
   are `total`, `symbol`, `no-evaluators` functions. Their only equations are
   `[concrete]` evaluators reducing ground calls to projections of
   `scanPairsVS`. LLVM ground executions and the differential suite support
   those concrete equations. In the Haskell symbolic proof, however, these
   terms stay opaque. They directly determine the returned tuple and occur
   unchanged in the target postcondition. They are program-derived,
   result-bearing abstractions, not external primitives.

6. **Priority loop rule, lines 201-223.** This rule matches the exact `While` at
   environment 1, reads the unboxed `numbers` list and loop locals, deletes the
   loop from `<k>`, sets `i=len-1` and `j=len`, and overwrites
   `best_low`, `best_high`, `low`, and `high` with the opaque closest
   projections. Other scopes and all omitted configuration cells are framed.
   Its guard is `0 <= I < J < len` and `I < len-1`. At `priority(40)`, it
   preempts the fixed `While` rule before the condition or body executes.

There is no auxiliary reachability claim proving that fixed execution of the
loop reaches this state. There is no bridge-free universal connection theorem,
no loop invariant claim, and no derivation of the result-bearing opaque values.
The recursive scan equations describe the desired answer but do not connect
that answer to execution. The same opaque symbols on the bridge RHS and in the
postcondition are circular, not evidence of value fidelity.

### Operational-sensitivity witness

The reviewer changed the loop comparison from
`candidate_gap < best_high-best_low` to
`candidate_gap < best_high-best_high`. This material mutation prevents updates
for the finite witness `[1.0, 10.0, 2.0]`; fixed K/Python execution returns the
initial pair `(1.0, 10.0)`, while the trusted canonical result is `(1.0, 2.0)`
([19 fixed K run](evidence/19-krun-operational-fixed.log),
[21 comparison](evidence/21-operational-mutation-compare.log)).

The proof-local loop pattern expands to that changed body, but the scan summary
on its RHS is unchanged. Rebuilding and reproving the mutated definition still
prints `#Top`
([verification-operational-mutation.k](evidence/verification-operational-mutation.k),
[20b log](evidence/20b-operational-sensitivity.log)). This is a concrete
body-sensitivity failure: the successful proof does not depend on the
property-bearing update computation it claims to summarize.

The accompanying list-literal `krun` remains on fixed semantics because a
literal is heap-allocated, while the bridge deliberately matches the entry
claim's unboxed external-list representation. That narrower context is
recorded in the same log and is not misreported as a bridge mismatch.

Removing the priority bridge compiles, but a bounded depth-100 proof exits 1
with a residual in the real loop condition
([24 build](evidence/24-kompile-no-bridge.log),
[27 residual](evidence/27-kprove-no-bridge-depth.log)). This bounded diagnostic
is not itself the verdict; it confirms which extension supplies closure.

I found no intended-domain input on which the unmodified scan summary disagrees
with the unmodified Python algorithm. Accordingly, I do **not** claim that the
original bridge equation is extensionally false; the 21,039-case differential
evidence suggests it is likely true. The narrower and decisive defect is that
the candidate assumes exactly that property as an operational rewrite instead
of proving it. This is an answer-encoding proof rule, which is illegitimate even
when the encoded answer happens to be true.

## 6. Fresh non-vacuity test

The fresh mutation changes the result obligation from `(low,high)` to the
demonstrably false `(high,high)`. The satisfying input `[1.0,2.0]` has original,
formal-scan, and both Python results `(1.0,2.0)`, so the mutation incorrectly
demands `(2.0,2.0)`.

The mutation is preserved as
[spec-vacuity.k](evidence/spec-vacuity.k). Its dry-run build exited 0
([16 log](evidence/16-vacuity-build.log)). The actual proof exited 1 with
`WarnStuckClaimState`; the residual explicitly contains the unmet
`closestHighVS == closestLowVS` obligation
([17 log](evidence/17-vacuity-proof.log)).

Non-vacuity therefore passes. This shows that the postcondition constrains the
result relative to the proof-local opaque functions. It does not validate the
missing connection between those functions and real loop execution.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied semantics **plus** all proof-local equations and the priority
loop rewrite, a direct call of the manually defined `findClosestBody` on an
unboxed symbolic Float list of length at least two reaches a tuple containing
the exact `closestLowVS` and `closestHighVS` terms installed by that rewrite,
while restoring the surrounding call configuration.

It does not establish, without the proof extension, that:

- the submitted `solution.mpy` artifact is the executed program;
- the fixed-semantics `While` computes `scanPairsVS`;
- the opaque closest projections equal the values produced by the program loop;
- the exhaustive scan has the natural-language closest-pair meaning for all
  inputs.

### Trust and assumptions

The complete ledger is [trust_ledger.tsv](evidence/trust_ledger.tsv). In brief:

- The byte-identical supplied semantics, K v7.1.337 toolchain, and builtin K
  mathematical theories are acceptable fixed trust boundaries.
- The supplied `gtF`, `floatLt`, `subF`, and related opaque float primitives are
  accepted conditionally because they belong to the selected trusted semantics;
  LLVM provides their concrete evaluators.
- The trusted translator and byte identity validly connect `solution.py` to
  `solution.mpy`.
- The trusted canonical implementation and 21,039 differential cases provide
  finite implementation-to-intent evidence only.
- The manual `findClosestBody` link is informal/static and is not body-sensitive.
- Proof-local `closestLowVS`/`closestHighVS` are not acceptable external trust
  boundaries: they summarize program-defined computation and affect the final
  result.
- The priority loop bridge is illegitimate because it assumes the central
  correctness conclusion and has no independent connection theorem.
- Partial correctness excludes empty/singleton inputs and makes no claim about
  behavior outside the Float-list, length-at-least-two domain.

The positive `#Top`, concrete executions, differential tests, and successful
non-vacuity check are all genuine evidence. None substitutes for the absent
loop connection proof. The candidate therefore meets the mechanical replay
gate but fails real-program soundness and pinning.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
