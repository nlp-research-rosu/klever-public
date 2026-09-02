# Independent adversarial audit: 8-sum-product

This audit used the required `using-kit` and `validating-proof` workflows. I
treated every candidate artifact, including `PROOF.md`, build products, logs,
traces, and prior `#Top` output, as untrusted evidence. All executable work used
source-only copies under `/tmp/audit-work`; no candidate-provided compiled
definition or cache was reused.

The reconstructed theorem is a legitimate partial-correctness proof of the
submitted program under the supplied MPY semantics. The proof executes the
exact submitted MPY AST, its result is universally constrained by structural
sum and product functions, both proof-local iterator accelerations have
machine-checked connections to the unaccelerated semantics, and a fresh false
result obligation is rejected for the expected reason.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mount does not
contradict the mode. The strict, symlink-aware comparison in
`evidence/compare_artifacts.py` recursively compared entry names, entry types,
and file bytes:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`84dc98e...fce03`);
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485e...64db16`);
- the candidate and trusted semantics trees each contain 26 entries, including
  24 regular files and two directories;
- all 24 semantics files are byte-identical;
- the candidate semantics tree has no missing, additional, mistyped, changed,
  or symlinked entry.

The comparison exited 0. Exact output and hashes are in
`evidence/03-integrity-comparison.log`.

### Required artifacts and untrusted generation claims

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
structured JSONL trace are all present as regular files. The complete candidate
inventory found no symlink among the required artifacts
(`evidence/01-candidate-inventory.log`). The structured trace is present at
`/candidate/codex-trace/2026/07/23/rollout-2026-07-23T04-29-52-019f8e4f-58cc-7262-ba9b-d786b2c89c21.jsonl`.

I read and independently summarized all five provenance sources in
`evidence/08-provenance-summary.log`. Both JSON documents parse, and all 432
JSONL lines parse. Those sources claim successful generation, three positive
proof runs, expected negative probes, and finite differential testing. None of
those claims was used as proof evidence without reconstruction.

The required proof sources are regular files. Source hashes before and after
the scratch copy agree (`evidence/30-source-hashes.log`). Candidate build
directories, Python bytecode, archives, mutation files, tests, `PROOF.md`, and
`prove.sh` are additional untrusted evidence, not inputs to the reconstructed
proof. They are not integrity failures because they are outside the recursively
fixed supplied-semantics tree.

Scratch isolation is recorded in `evidence/05-scratch-source-inventory.log`.
The source copy contained the submitted Python/MPY/K sources and the
integrity-checked semantics, but no candidate `*-kompiled` directory.

Stage 1 result: PASS. There is no infrastructure/mode breach and no provenance
integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires:

> For a finite list of integers, return a two-tuple containing the sum and
> product of all elements. The empty sum is 0 and the empty product is 1.

The documented examples are `[] -> (0, 1)` and
`[1, 2, 3, 4] -> (10, 24)`. The trusted canonical implementation initializes
the two accumulators to 0 and 1, visits the list from left to right, adds and
multiplies each element, and returns the two accumulators.

`solution.py` implements that algorithm. Its extra `number = 0` initialization
only fixes the final loop-target binding for the empty case; it does not change
the returned value.

### Translator fidelity

I regenerated the MPY artifact with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/generated-solution.mpy
cmp -s /tmp/audit-work/generated-solution.mpy /tmp/audit-work/source/solution.mpy
```

Both artifacts have SHA-256
`cdfc01628838ac253b1a60d7d4094f09600c8befbd49e0588911167c4a1245af`;
`cmp` exited 0 (`evidence/06-translator-identity.log`).

### Independent differential reconstruction

`evidence/differential_test.py` imports the trusted canonical entry point and
the scratch candidate entry point through distinct module objects. It does not
reuse candidate tests or proof equations. It exercised:

- the two prompt examples;
- empty, singleton, and multi-iteration loop boundaries;
- zero, positive, negative, sign-changing, and repeated elements;
- very large positive and negative Python integers;
- all 19,608 lists of length 0 through 5 over elements `-3..3`;
- 500 deterministic generated lists of length 0 through 20 with small,
  32-bit-scale, and 50-digit-scale integers.

All 20,126 cases returned a tuple equal to the canonical result; mismatches were
zero and the script exited 0 (`evidence/07-differential-test.log`).

Stage 2 result: PASS. The submitted program is materially equivalent to the
trusted canonical implementation on the intended domain.

## 3. Clean proof reconstruction

K v7.1.293 was independently available
(`evidence/02-toolchain.log`). I compiled three fresh definitions from the
scratch sources:

| Purpose | Fresh command/output | Result |
|---|---|---|
| Concrete semantics | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled` | exit 0; `evidence/09-build-concrete.log` |
| Connection theory without accelerations | `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition connection-audit-kompiled` | exit 0; `evidence/10-build-connection.log` |
| Target proof theory | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled` | exit 0; `evidence/11-build-proof.log` |

The positive claims were reconstructed as follows:

| Claim(s) | Result |
|---|---|
| `CONNECTION-SPEC.iter-empty-connection` | exit 0, `#Top`; `evidence/12-prove-connection-empty.log` |
| `CONNECTION-SPEC.iter-cons-connection` | exit 0, `#Top`; `evidence/13-prove-connection-cons.log` |
| `SPEC.loop-invariant` | exit 0, `#Top`; `evidence/14-prove-loop.log` |
| Complete `SPEC` module, containing the entry claim and its required loop circularity | exit 0, `#Top`; `evidence/16-prove-entry-with-invariant.log` |

The whole-program entry depends on `SPEC.loop-invariant` as a circularity.
For diagnostic purposes I once selected only `SPEC.sum-product`; that filter
removed the invariant from the selected proof set and caused unbounded
symbolic-list unrolling. I interrupted that non-target diagnostic with status
130 and recorded the reason in
`evidence/15-diagnostic-entry-without-helper.log`. It is not counted as a
candidate proof failure. The correct two-claim target command closed with
`#Top`.

I also generated a reviewer-authored concrete program with empty, singleton,
zero, negative, multi-element, and mixed-sign assertions. It ran under the
fresh LLVM definition to `.K`, `NoExc`, and exit code 0
(`evidence/concrete_boundary.py`,
`evidence/17-generate-concrete-boundary.log`,
`evidence/18-krun-concrete-boundary.log`).

The LLVM compiler reported non-exhaustive supplied helpers `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; the builds also reported
unused `strLt` pattern tails. None of those helpers occurs on the submitted
program, target-claim, loop-claim, or connection-claim paths. They are accounted
for in Stages 5 and 7 rather than hidden.

Stage 3 result: PASS. Every required positive claim closes under fresh
source-only definitions.

## 4. Adequacy and real-program pinning

### Claim meanings

`CONNECTION-SPEC.iter-empty-connection` has no guard. For any continuation and
framed machine state, it says that requesting the next item from the proof
embedding of an empty integer list produces `#iterDone`.

`CONNECTION-SPEC.iter-cons-connection` also has no guard. For any integer `I`,
tail `IS`, continuation, and framed state, it says that requesting the next item
from the embedded cons list produces `#iterYield(I, list(intListVals(IS)))`.

`SPEC.loop-invariant` has no explicit guard. At a real `#loop` head with
remaining embedded suffix `IS`, arbitrary integer accumulators `S` and `P`,
and prior loop-target value `N`, it:

- consumes the loop;
- changes `sum_value` to `sumFrom(S, IS)`;
- changes `product_value` to `productFrom(P, IS)`;
- changes `number` to `lastFrom(N, IS)`;
- preserves the original `numbers` binding, environment, continuation, other
  scopes, and all omitted machine cells.

The invariant matches the real `For` control form and exact two-statement body
from `solution.mpy`.

`SPEC.sum-product` has no guard beyond the constructor sort
`INPUT:IntList`, so its formal domain is every finite list of K mathematical
integers. It begins in the default MPY state, loads a `Module`, and calls the
loaded `"sum_product"` closure with `list(intListVals(INPUT))`. It requires the
final computation to be exactly:

```text
tuple(vCons(sumFrom(0, INPUT),
      vCons(productFrom(1, INPUT), .ValSeq)))
```

It also pins the final module binding, empty heap, allocation counters, empty
call stack, `noRet`, `NoExc`, and exit code 0. The return is not existential,
free, tautological, or guarded only by a one-way implication.

### Exact program identity

`evidence/check_program_pinning.py` balanced-parses the sole `#loadAll(...)`
argument in the entry claim and compares it, ignoring only whitespace, with the
submitted `solution.mpy`. The compact strings are exactly equal and the script
exits 0 (`evidence/23-program-pinning.log`). Combined with the trusted
translator byte-identity check, the theorem loads and calls the real generated
program rather than a substituted body.

The proof is body-sensitive. A reviewer-authored ground-empty version changing
only `product_value = 1` to `product_value = 0` parses successfully and then
fails with actual result `(0,0)` against required `(0,1)`
(`evidence/body_sensitivity_spec.k`,
`evidence/26-body-sensitivity-dry-run.log`,
`evidence/27-body-sensitivity-proof.log`).

### Satisfiable witnesses

The entry precondition is realized by the default configuration with
`INPUT = .IntList`. It returns `(0,1)`. Other concrete substitutions recorded
in `evidence/22-claim-witnesses.log` are:

| Python input / K `IntList` | Claimed result | Canonical | Candidate |
|---|---|---|---|
| `[]` / `.IntList` | `(0,1)` | `(0,1)` | `(0,1)` |
| `[2,-3]` / `intCons(2,intCons(-3,.IntList))` | `(-1,-6)` | `(-1,-6)` | `(-1,-6)` |
| `[0,5,-2]` / `intCons(0,intCons(5,intCons(-2,.IntList)))` | `(3,0)` | `(3,0)` | `(3,0)` |

A loop-claim witness chooses `L = 1`, `_SC` as the builtins and module scopes,
arbitrary integer `S`, `P`, and `N`, and any finite `IS`; the displayed local
scope is then a well-formed disjoint map entry. For `IS = .IntList`, the loop
leaves `S`, `P`, and `N` unchanged. For
`IS = intCons(2,intCons(-3,.IntList))`, it adds `-1`, multiplies by `-6`, and
sets the loop target to `-3`.

Stage 4 result: PASS. The claims are satisfiable, result-constraining, and pin
the real generated program and control flow.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` strips comments without damaging quoted `//`
operators, reconstructs multiline declarations, and inventories every K source
statement in the 24 supplied files, `semantics.k`, `verification.k`,
`connection-spec.k`, and `spec.k`. The full source text, line, classification,
and per-rule assessment are in `evidence/19-k-rule-inventory.log`.

The inventory contains:

- 232 syntax statements, including 110 `[function,total]` statements, 38 other
  `[function]` statements, strict/seqstrict/macro declarations, and all
  unannotated syntax;
- 664 ordinary rules and 43 priority rules (707 total rules);
- 39 supplied `[concrete]` rules, included verbatim in the inventory;
- one configuration and five explicit contexts;
- four reachability claims;
- no `[simplification]` rule and no `functional` declaration.

For every supplied rule, the inventory marks whether it is reached by the
pinned program/connection paths. Every unreached rule is explicitly classified
as part of the immutable supplied-semantics boundary and as unable to match a
term on an intended `list[int]` execution of this program. That classification
does not claim the deliberately partial MPY semantics is full CPython.

### Submitted-construct map

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module` and statement sequencing | `syntax.k:61`; `core.k:125-127` |
| unused `from typing import List, Tuple` | `syntax.k:43`; `controls.k:36` no-op, observationally correct here because neither imported name is used |
| `FuncDef` and call frame | `syntax.k:53`; `functions.k:14-16`; `call.k:20-21,69-75`; `functions.k:63-66,78-90` |
| local `Assign` and integer literals | strict statement syntax; `core.k:194`; `controls.k:9-11` |
| `Name` lookup | `syntax.k:12`; `core.k:131-154`; reached bindings are in the current pinned scope |
| `For` over the read-only unboxed input list | strict `For` syntax; `controls.k:69-74,85`; supplied list iteration at `list.k:9-10`, connected to the proof representation |
| `AugAssign` with `+` and `*` | strict `AugAssign` syntax; `controls.k:20-23`; exact integer cases `int.k:9,14` |
| return `TupleExpr` | strict `Return`; `tuple.k:15-16`; `functions.k:78-90` |

Evaluation is left-to-right through the supplied heating/cooling attributes and
`#evalArgs`. The input is evaluated once before `For`. Each yielded integer is
bound before the two body statements execute in order. `AugAssign` reads and
writes the current frame. Return stores the tuple, pops exactly one frame,
restores the caller environment, removes the callee scope, and leaves the
observed heap/exception/exit state pinned.

### Proof-local rule assessment

`verification.k` adds no result oracle and no rule for a program-defined call.
Its complete local inventory is:

1. `IntList ::= .IntList | intCons(Int,IntList)`: a free structural domain
   exactly representing finite integer lists.
2. `intListVals(.IntList) => .ValSeq` and
   `intListVals(intCons(I,IS)) => vCons(I,intListVals(IS))`: disjoint,
   exhaustive constructor equations with structural descent.
3. Two contextual exposure rules under
   `#iterNext(list(intListVals(...)))`: exact context liftings of those two
   equations. They alter only the active computation and preserve the arbitrary
   continuation and every omitted cell.
4. `sumFrom`: two disjoint, exhaustive equations; the cons case descends on
   `IS` after mathematical integer addition.
5. `productFrom`: the analogous structural multiplication equations.
6. `lastFrom`: the empty case preserves the prior target; the cons case
   structurally replaces it with each yielded integer, ending at the last.
7. Two priority-40 iterator accelerations: empty produces `#iterDone`; cons
   produces the exact head and embedded tail. They preempt only the two
   contextual exposure shapes.

The summary functions cover all `IntList` constructors, have no overlaps
between empty and cons, and strictly descend. Their `[total]` attributes are
therefore justified. No local symbol is opaque.

Both accelerations are universally connected to the unaccelerated
`VERIFICATION-BASE` definition by the independently rerun connection claims.
Their matched continuation is exactly as broad as the connection theorem's
continuation, and they read/write no state cell. Fresh downstream-continuation
claims additionally place membership and Boolean-negation consumers after both
empty and cons iterator steps. Base and accelerated definitions produce the
same observable results (`#Top` in
`evidence/20-bridge-context-base.log` and
`evidence/21-bridge-context-extended.log`).

A wrong-yield ground theorem was first dry-run successfully, then rejected with
the fixed execution residual `#iterYield(7, ...)` against false target
`#iterYield(8, ...)` (`evidence/wrong_bridge_spec.k`,
`evidence/24-wrong-bridge-dry-run.log`,
`evidence/25-wrong-bridge-proof.log`). An earlier probe with an unnecessarily
arbitrary continuation encountered an unrelated supplied float hook; it is
preserved and explicitly marked discarded in the `24a`/`25a` logs and is not
used as evidence.

### Supplied opaque and partial boundaries

The supplied proof definition imports 25 declared `symbol(...)` functions:

`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`.

Twenty-two also carry `no-evaluators`; `floorFI`, `toF`, and `ceilF` have
concrete equations but can remain abstract outside their covered symbolic
shapes. None can influence a branch, value, state, exception, or postcondition
in any target or auxiliary claim here. Likewise, the compiler's six
non-exhaustive-total warnings are all for unreachable helpers. Thus no
program-derived result is hidden behind an opaque or totalized oracle.

I found no candidate rule that enables a false conclusion on the intended
domain, so there is no unsoundness allegation requiring a false-conclusion
witness. The wrong-yield and body mutations instead demonstrate that plausible
unsound replacements are rejected by the actual fixed semantics and claim.

Stage 5 result: PASS. The used semantic path and every proof-local declaration
are sound; no answer-smuggling, execution bypass, inconsistent overlap, or
result-bearing oracle is present.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The reviewer-authored
`evidence/fresh_nonvacuity_spec.k` fixes the satisfying input to the empty
integer list, executes the exact submitted module and function body, and
changes only the required result from the true `(0,1)` to false `(1,1)`.

First, a dry run compiled the mutation to KORE and exited 0:

```text
kprove /audit-output/evidence/fresh_nonvacuity_spec.k \
  --definition verification-audit-kompiled \
  --spec-module FRESH-NONVACUITY-SPEC --dry-run
```

See `evidence/28-fresh-nonvacuity-dry-run.log`.

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual is
the fully executed actual result:

```text
tuple(vCons(0, vCons(1, .ValSeq)))
```

which does not unify with the false target. The final environment, scopes,
heap, stack, return, exception, and exit-code cells are otherwise the expected
ones. This is a reachable unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash
(`evidence/29-fresh-nonvacuity-proof.log`).

Stage 6 result: PASS. The proof is discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every finite `IntList` of arbitrary K
integers, loading the exact translated `solution.mpy` module and calling its
real `sum_product` function from the default state has the following
partial-correctness property:

- if execution terminates, the returned MPY value is exactly the two-element
  tuple whose first component is the structural sum from identity 0 and whose
  second component is the structural product from identity 1;
- the function closure is the exact submitted closure;
- the call frame is removed, allocation counters and empty heap are restored
  as claimed, the stack is empty, no return marker or exception remains, and
  the exit code is 0.

The loop claim proves the exact accumulator and loop-target effects for every
remaining suffix. The two connection claims establish the only operational
accelerations against the fixed supplied semantics. The structural equations
formally define the list embedding and accumulated values; they are not
empirical summaries.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Integrity-checked supplied MPY semantics | Defines syntax, evaluation, calls, scopes, loops, arithmetic, tuples, return, and state for all claims | Acceptable fixed semantics required by the problem. The complete inventory is preserved; all reached rules were audited. It is a partial MPY model, not full CPython. |
| K v7.1.293 compiler, Haskell prover/backend, LLVM backend, builtin integer/map/list hooks, and host execution | Establishes build, symbolic reachability, and concrete execution | Standard unavoidable machine-checking trust boundary. Fresh rebuilds avoid candidate binaries. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py` to the submitted MPY AST | Acceptable problem-supplied translator; fresh output is byte-identical and the entry claim embeds that exact output. |
| Trusted `/reference/canonical.py` and prompt | Define the external intent used for differential and adequacy checks | Acceptable trusted inputs. They do not replace the K proof. |
| `IntList`, `intListVals`, `sumFrom`, `productFrom`, `lastFrom` | Determine input representation, invariant state, and final result | Not assumed primitives: exhaustive, disjoint, terminating equations in the proof definition; used universally by the claims. |
| Iterator acceleration rules | Affect loop control and yielded values | Not assumed: both constructor cases have fresh `#Top` connection theorems, downstream-context checks, and a rejected opposite-value witness. |
| The 25 supplied opaque symbols listed in Stage 5 | Potentially affect floats, sorting, or MD5 in other programs | No influence on this theorem. They remain named but irrelevant supplied boundaries, not result assumptions. |
| CPython execution in differential tests | Supports candidate-to-canonical and intent alignment for 20,126 inputs | Finite empirical evidence only; it is not used as a universal proof. |
| Fresh LLVM assertion program | Supports concrete MPY behavior on seven boundary/representative inputs | Finite semantic bridge evidence only; universal correctness comes from the K claims. |
| Informal intent bridge | Interprets structural `sumFrom(0, xs)` and `productFrom(1, xs)` as ordinary sum/product and aligns finite K integers with `List[int]` | Acceptable and direct: the defining equations are exactly the standard identities and folds, and K/CPython both use unbounded integers for `+` and `*`. |

There is no external primitive, opaque symbol, differential oracle, or
informal assumption on which the proved return value depends.

### Scope and exclusions

The formal domain excludes non-lists, non-integer elements, floats, strings,
booleans-as-runtime-subclass values, arbitrary iterables, infinite inputs, and
mutation/aliasing behavior. Those are not required by the `List[int]` task
contract. The proof uses the supplied semantics' legal unboxed read-only list
representation; the program never mutates or aliases the input, so that
representation choice has no observable effect on the requested result.

The theorem is about the supplied MPY semantics, not every CPython behavior,
and follows the Kit's partial-correctness interpretation. Candidate prose,
candidate traces, differential tests, and concrete runs are supporting
evidence only; none substitutes for the reconstructed reachability proof.

### Decision

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
auditability) all pass. The proof cleanly reconstructs, constrains the intended
result, executes the exact submitted program, and contains no material
adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
