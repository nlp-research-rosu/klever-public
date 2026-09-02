# Independent adversarial audit: 94-skjkasdkd

## Overall decision

**CONCERNS / LEGIT.** I reconstructed the proof from source, independently
proved every positive claim, confirmed that the proof macro is structurally
identical to the submitted `solution.mpy`, and rejected a fresh false-result
mutation for the expected unmet equality. The proof is result-constraining and
establishes partial correctness of the submitted program over the formal
integer-list domain.

The concerns are material to validation quality but do not make the proved
end-to-end result false:

1. Expected generation/provenance records are missing.
2. The trusted canonical implementation treats `1` as prime when no larger
   prime is present, while the submitted program and formal summary correctly
   treat `1` as non-prime. The prompt does not state the no-prime fallback
   explicitly.
3. One proof normalization for `For(..., Name(X), ...)` is over-broad outside
   the theorem's unboxed read-only-list representation. A concrete heap-reference
   witness makes the proof-extended semantics stop where fixed semantics
   continues. It does not fabricate an incorrect result on the main claim's
   match domain.
4. The bounded function-entry bridge has a transparent finite derivation, but
   the independently generated bridge-free machine proof reached the
   900-second audit bound. That timeout is inconclusive and is not used as a
   candidate failure.
5. The final bridge from the recursively defined trial-division summary to the
   ordinary mathematical phrase “largest prime” is supported by direct
   mathematics and differential evidence, not by a separate K theorem.

## 1. Input and provenance integrity

### Supplied-semantics boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. I recursively compared it with
`/candidate/reference-semantics` using:

```text
diff -r --no-dereference --brief \
  /reference/reference-semantics /candidate/reference-semantics
```

The command exited `0`. The candidate tree has exactly the same directories
and regular files; no semantics entry is missing, additional, mistyped, or a
symlink. The hashes and typed tree are preserved in
[integrity-comparisons.log](evidence/stage1/integrity-comparisons.log),
[source-hashes.log](evidence/stage1/source-hashes.log), and
[tree-and-types.log](evidence/stage1/tree-and-types.log).

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both
`cmp` checks exited `0`.

There is no infrastructure/mode contradiction, so a candidate verdict is
appropriate. Per the supplied-semantics boundary, the matching reference tree
fixes the language semantics but does not validate any rule in
`verification.k`.

### Candidate artifacts and missing provenance

The proof sources needed for reconstruction are regular files and present:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and the matching
`reference-semantics` tree. Candidate-provided `spec.json`, `prove.sh`,
concrete tests, prose/comments, and the `__pycache__` entry were treated as
untrusted claims and were not used as compiled proof evidence.

The following expected provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace identifiable by name

The exact check and nonzero presence-check status are in
[metadata-presence.log](evidence/stage1/metadata-presence.log). Their absence
limits provenance auditability, but it does not remove any source needed to
reconstruct the theorem.

The live toolchain was K `v7.1.337`; see
[toolchain.log](evidence/stage1/toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for the sum of the decimal digits of the largest prime
in a list of integers. It does not explicitly say what to return when the list
has no prime.

The trusted canonical implementation starts `maxx` at `0`, scans the list, and
digit-sums the selected value. Its nested `isPrime` has no explicit `n >= 2`
test. Consequently, it returns `1` on `[1]`, even though `1` is not prime.

The submitted implementation:

- starts `largest` and the digit accumulator at zero;
- only tests a number when it exceeds the current largest;
- initializes primality with `number >= 2`;
- tries every divisor from `2` while `divisor * divisor <= number`;
- digit-sums the selected value by `% 10` and `// 10`.

For finite integer lists, this implements the natural-language prime contract,
with an explicit effective fallback of `0` when no prime exists.

### Translation identity

I regenerated the program with the trusted translator copied from
`/reference/py2mpy.py`. The regenerated and submitted `solution.mpy` files
have the same SHA-256 hash
`6adc49642fc72665394f0abc7c9860d03b3df6e219924c30419c42d9a7ac5486`;
`cmp` exited `0`. See
[translation-fidelity.log](evidence/stage2/translation-fidelity.log).

### Independent differential test

[differential.py](evidence/stage2/differential.py) independently imports the
trusted canonical and generated entry points and uses a third, directly
implemented integer primality oracle. Its complete deterministic corpus is in
[differential-inputs.json](evidence/stage2/differential-inputs.json):

- all six documented examples;
- 17 named empty, sign, ordering, equality, trial-loop, divisibility, square,
  and decimal-digit boundaries;
- every list of length 0 through 3 over
  `[-3, 0, 1, 2, 3, 4, 5, 9, 11, 25]`;
- 500 generated lists from seed `940094`, lengths 0 through 10, with elements
  from `-50` through `5000`.

The exact command exited `0` over 1,634 cases:

```text
candidate_vs_canonical_mismatches=105
candidate_vs_math_oracle_mismatches=0
canonical_vs_math_oracle_mismatches=105
```

Every candidate/canonical mismatch had `1` present and no actual prime that
would supersede it. The smallest witness is `[1]`: formal/generated `0`,
canonical `1`. This is fully recorded in
[differential.log](evidence/stage2/differential.log). The discrepancy is a
real limitation of canonical equivalence on the prompt's stated integer-list
domain; it is not evidence that the submitted algorithm violates the ordinary
meaning of prime.

## 3. Clean proof reconstruction

All source needed for execution was copied into
`/tmp/audit-work/reconstruction`, with trusted Python inputs copied separately
under `/tmp/audit-work/trusted`. No candidate-built K definition or cache was
copied or reused. The copy manifest is
[scratch-copy.log](evidence/stage2/scratch-copy.log).

### Concrete definition

The supplied semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited `0`; warnings concerned unused or non-exhaustive constructs outside
the submitted program. See [kompile-llvm.log](evidence/stage3/kompile-llvm.log).

A reviewer-authored harness was formed from the copied `solution.py`, translated
with the trusted translator, and run through the fresh LLVM definition. It
covered the six examples plus empty, negative/zero, `1`, `2`, `3`, `4`, `5`,
`9`, `49`, and multi-digit-prime cases. `krun` exited `0` in a final
configuration with `.K`, `NoExc`, and exit code `0`. See
[make_concrete_harness.py](evidence/stage3/make_concrete_harness.py),
[concrete-harness-build.log](evidence/stage3/concrete-harness-build.log), and
[krun-concrete-harness.log](evidence/stage3/krun-concrete-harness.log).

### Proof definition and positive claims

The Haskell definition was freshly compiled:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled -I .
```

It exited `0`; see
[kompile-haskell.log](evidence/stage3/kompile-haskell.log).

Every one of the five positive claims was then run independently in the
candidate's staged dependency order. Earlier claims were trusted only after
their own independent successful run:

| Target proved in the command | Exit | Output evidence |
|---|---:|---|
| `SPEC.prime-loop` | 0 | `#Top` in [kprove-prime-loop.log](evidence/stage3/kprove-prime-loop.log) |
| `SPEC.digit-loop` | 0 | `#Top` in [kprove-digit-loop.log](evidence/stage3/kprove-digit-loop.log) |
| `SPEC.scan-loop`, trusting the two proved inner loops | 0 | `#Top` in [kprove-scan-loop.log](evidence/stage3/kprove-scan-loop.log) |
| `SPEC.entry-prefix`, trusting the proved scan and inner loops | 0 | `#Top` in [kprove-entry-prefix.log](evidence/stage3/kprove-entry-prefix.log) |
| `SPEC.main-correct`, trusting the four separately proved dependencies | 0 | `#Top` in [kprove-main-correct.log](evidence/stage3/kprove-main-correct.log) |

Thus the fresh dynamic reconstruction gate passes. The `#Top` results are not
used by themselves as evidence that the proof extensions are sound.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `prime-loop`: from a trial-division loop head with integer `number = N`,
  `divisor = D >= 2`, and Boolean `prime = B`, execution resumes the framed
  continuation with `prime = trialPrime(N,D,B)` and
  `divisor = trialDivisor(N,D,B)`. Other locals are preserved. If `B` is true,
  the precondition requires `N >= 2`.
- `digit-loop`: with `largest = N >= 0` and accumulator `A`, the decimal loop
  terminates its modeled computation with `largest = 0` and
  `digit_total = digitAcc(N,A)`, preserving the rest of the local map.
- `scan-loop`: scanning the remaining symbolic integer list `IS` from current
  `largest = CUR >= 0`, followed by the actual decimal loop and return, pops
  the exact function frame and returns
  `digitSum(largestPrime(IS,CUR))` to the saved continuation.
- `entry-prefix`: applying the exact submitted closure to an unboxed symbolic
  integer list reaches `digitSum(largestPrime(IS,0))`, with the scan claim
  discharging the unbounded computation.
- `main-correct`: loading the submitted module and calling `skjkasdkd` from the
  fixed initial configuration returns
  `digitSum(largestPrime(IS,0))` for every finite `IntList IS`, while producing
  the exact loaded closure and leaving the other specified cells unchanged.

Ground states satisfying every precondition, including all maps, stack frames,
and excluded-key conditions, are recorded in
[precondition-witnesses.md](evidence/stage4/precondition-witnesses.md).

### Exact program pin

The end-to-end claim does not parse a path at proof time; it uses the
`solutionModule` macro. I therefore compared parser output, not source
appearance. With `kast --expand-macros --output json`, the parsed submitted
`solution.mpy` and expanded `solutionModule` produced byte-identical KAST JSON
with SHA-256
`443918d64cf150646cd003745ea4b1313d8bfbdbd277363049d200ba06996bc8`.
The exact commands and `cmp` status `0` are in
[program-pin-kast-compare.log](evidence/stage4/program-pin-kast-compare.log).

This confirms that `<k>` loads and executes the submitted translated program,
not a substituted body. The macro includes all five initializations, the real
outer `For`, the real primality `While`, the real digit `While`, and the real
`Return`.

A discarded diagnostic attempt to embed the translator's source notation
directly inside a claim produced a parser error
([kprove-program-pin.log](evidence/stage4/kprove-program-pin.log)); it is not
counted as pinning evidence. The successful expanded-KAST identity is the
relevant check.

### Result constraint and concrete substitutions

The RHS has no fresh result variable or implication: it fixes the returned
integer to `digitSum(largestPrime(IS,0))`. The auxiliary claims connect the
actual loops and frame return to that same value.

Ground K summary checks for empty, `1`, prime/composite boundaries, a prime
square, later/larger primes, and decimal digits all normalized to their
expected values with `#Top`; see
[ground-summary-spec.k](evidence/stage4/ground-summary-spec.k) and
[kprove-ground-summaries.log](evidence/stage4/kprove-ground-summaries.log).

Concrete substitution gives:

```text
input=[2,4,11] formal=2 canonical=2 generated=2
input=[1]      formal=0 canonical=1 generated=0
```

See [concrete-substitutions.log](evidence/stage4/concrete-substitutions.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The inventory covers all 26 K files in the proof closure: the supplied
assembly/helper files, `verification.k`, and `spec.k`. It contains:

- 242 syntax declarations;
- 740 rules, including 10 simplification-tagged, 70 priority-tagged, and 29
  `owise` rules;
- 5 contexts;
- 1 configuration;
- 5 claims.

There are no `[functional]` declarations. The full normalized sentence for
every entry is in
[rule-inventory.md](evidence/stage5/rule-inventory.md) and structured form in
[rule-inventory.json](evidence/stage5/rule-inventory.json).
[annotated-inventory.md](evidence/stage5/annotated-inventory.md) assigns a
disposition and reason to all 1,160 inventoried sentences; its generation is
reproducible through
[inventory_k.py](evidence/stage5/inventory_k.py) and
[annotate_inventory.py](evidence/stage5/annotate_inventory.py).

The supplied tree is the selected fixed semantics. I reviewed the reachable
slice in detail and marked the remaining fixed rules as unreachable from this
integer-only program; importing unused syntax does not make the opaque float,
sort, string-order, or MD5 values influence control, state, or the
postcondition. The exact opaque/total/priority/simplification search is
[opaque-and-attribute-inventory.log](evidence/stage5/opaque-and-attribute-inventory.log).

### Used-construct mapping

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, statement lists, `FuncDef`, `Params` | `semantics/syntax.k`; load/sequencing in `core.k`; closure creation in `functions.k` |
| `Name`, `Int`, `Bool` | syntax plus lookup/literal rules in `core.k`; guarded proof normalizations |
| `Assign`, `AugAssign` | strict syntax and state updates in `controls.k`; exact non-cell normal forms in `verification.k` |
| `For` over the formal input | strict `For`, `#loop`, and `#iterNext` protocol in `controls.k`/`iter.k`; `asVals(IntList)` iterator cases in `verification.k` |
| `If`, `While`, `BoolOp("and",...)` | `controls.k` and short-circuit rules in `bool.k` |
| `Compare`, `BinOp("*","%","//","+")` | contexts/dispatch in `operators.k`; integer definitions and `pyMod` in `int.k` |
| Call, frame, parameter bind, return/pop | `call.k` and `functions.k`, with exact finite normalizations in `verification.k` |

Configuration and cell effects were checked through load, frame allocation,
environment switch, local map updates, stack push/pop, local-scope deletion,
and `scopeLoc` restoration. The program performs no heap allocation under the
formal unboxed read-only-list input representation, no output, and no exception
or exit-code change.

### Proof-local functions and summaries

`verification.k` adds 15 syntax declarations and 45 rules. The significant
classes are:

- two Map simplifications for deleting an explicit key and inserting a fresh
  key;
- guarded normal forms for non-cell Name lookup, assignment, augmented
  assignment, target binding, comparison, conditional, return, `For`, and call;
- two structural iterator cases for the symbolic `IntList`;
- six total mathematical functions:
  `trialPrime`, `trialDivisor`, `isPrime`, `largestPrime`, `digitAcc`, and
  `digitSum`;
- exact AST macros;
- one bounded function-entry operational bridge.

The normal forms preserve evaluation order because all skipped operands are
already values, literals, or side-effect-free local-name lookups. Their guards
exclude closure-cell and duplicate-Map branches. Overlapping Map-split and
generic normal forms agree on their RHS. The call normalization pins the exact
binding and preserves the arbitrary continuation. Return/frame effects remain
in the fixed semantics and in the proved scan claim.

The summary equations are disjoint and covering on every proof use:

- `trialPrime`/`trialDivisor` split on prior-false, loop-exit, divisible, and
  non-divisible cases. Recursive calls increase `D`; all claims use `D >= 2`,
  so the `pyMod` divisor is nonzero.
- `largestPrime` has empty, update, and complementary keep-current cases and
  structurally consumes `IntList`.
- `digitAcc` splits at `N <= 0`; for `N > 0`, decimal quotient strictly
  decreases.

These are definitional summaries, not opaque oracles. The proved loop claims
connect them to execution. No proof-local opaque value can select a branch or
determine the postcondition.

### Operational bridge review and witnesses

The bounded rule at `verification.k:307` matches the complete call-prefix
context: an exact `#applyK` term with no trailing K continuation, `env = 0`,
`scopeLoc = 1`, empty stack, the exact closure body and list argument, and a
Map where location `1` is fresh. It:

1. allocates frame `1` with parent `0`;
2. binds `lst`;
3. executes the five literal assignments;
4. evaluates the already-valued iterable once;
5. leaves the real list loop, digit loop, return, and `#endcall` in `<k>`.

It does not read or change heap, heap location, return state, exception, or
exit code. Its RHS and state changes equal the direct composition of the fixed
rules.

For additional evidence, I removed only this bridge, rebuilt the Haskell
definition successfully, and attempted the universal `entry-prefix` proof
against the remaining rules. The generator and exact diff are in
[nobridge-generation.log](evidence/stage5/nobridge-generation.log), and the
fresh build is in
[kompile-nobridge.log](evidence/stage5/kompile-nobridge.log). The proof used
active CPU until the explicit 900-second bound and exited `124` with no
residual; see
[kprove-entry-prefix-nobridge.log](evidence/stage5/kprove-entry-prefix-nobridge.log).
This is an evidence gap, not evidence of a false bridge.

One other operational rule has a concrete over-breadth witness. At
`verification.k:134`, the direct `For(T,Name(X),B) => #loop(V,T,B)` rule accepts
any `V:Val`. For a local `lst |-> ref(0)` with heap
`0 |-> list(.ValSeq)`, fixed semantics performs Name lookup and then the
priority heap dereference before forming `#loop(list(.ValSeq),...)`. The
proof-extended definition instead forms `#loop(ref(0),...)` and stops.

This false operational transition is exhibited by the same translated
submitted function called with a normally allocated empty list:

- fixed LLVM semantics completes all assertions with `.K`
  ([krun-concrete-harness.log](evidence/stage3/krun-concrete-harness.log));
- the proof-extended definition stops at `#loop(ref(0),...)`
  ([krun-proof-rules-heapref.log](evidence/stage5/krun-proof-rules-heapref.log)).

The rule should have been narrowed to `V:Iterable` or explicitly excluded
references. It does not apply to the main theorem's `list(asVals(IS))` value,
which the supplied semantics explicitly permits as an unboxed read-only claim
input, and on that match domain it is the exact fixed sequence. The witness
shows lost execution, not an admitted incorrect returned value, so it is a
scoped concern rather than a reason to call the reconstructed main theorem
false.

### Static conclusion

No rule encodes the requested digit sum as a task-specific answer, replaces a
used computation with an unconstrained result oracle, bypasses the real loops,
or permits an incorrect result on the formal entry domain. The exact result is
derived through proved loop and frame claims. The formal proof is therefore
sound for its stated match domain, with the global normalization and bridge
audit limitations stated above.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I authored
[spec-vacuity.k](evidence/stage6/spec-vacuity.k), changing only the
result-bearing destination from:

```text
digitSum(largestPrime(IS, 0))
```

to:

```text
digitSum(largestPrime(IS, 0)) +Int 1
```

The empty list is a satisfying witness: the real/formal result is `0`, while
the mutation requires `1`.

The mutated specification parsed and compiled successfully under `--dry-run`
with exit `0`; see
[vacuity-dry-run.log](evidence/stage6/vacuity-dry-run.log). The actual proof
then exited `1` with `WarnStuckClaimState` and the expected unmet implication:

```text
digitAcc(largestPrime(IS, 0), 0) +Int 1
#Equals
digitAcc(largestPrime(IS, 0), 0)
```

It ended with the prover's “configuration cannot be rewritten further” error,
not a parser error, timeout, missing import, or unrelated crash. See
[kprove-vacuity-mutation.log](evidence/stage6/kprove-vacuity-mutation.log).
This is meaningful result-sensitivity evidence.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics, for every finite structural `IntList IS`,
from the exact initial configuration in `main-correct`, if the translated
program terminates, loading and calling the exact submitted function produces
the integer term:

```text
digitSum(largestPrime(IS, 0))
```

The five reconstructed claims machine-check:

- trial-loop state evolution;
- decimal-loop state evolution;
- list scanning plus the real suffix and frame pop;
- function invocation;
- module load and end-to-end call.

This is a partial-correctness theorem. It is not a separate K termination
theorem, performance bound, theorem about non-integer elements, or theorem
about arbitrary Python behaviors outside the supplied subset.

### Trust ledger

The exact supplied-semantics opaque symbols visible to the proof definition
are `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
`gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, and `md5hexCodes`. The constructor-defined total
functions `valSeqAt` and `strLt` can also remain symbolic on opaque
nonconstructor inputs. None occurs in the submitted AST, a reachable guard,
an auxiliary claim, or the postcondition.

The fixed K primitives actually used are integer
`+Int`/`-Int`/`*Int`/`/Int`/`%Int` and comparisons, Boolean connectives,
String equality for identifier guards, K sequencing, structural `==K`, and
Map lookup, `in_keys`, insertion, replacement, and deletion. The proof also
trusts the generated configuration/cell machinery and reachability prover.

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.337`, Haskell/LLVM backends, parser, and hooked Int/Bool/String/Map/List operations | All builds, execution, and proofs | Necessary low-level toolchain trust; commands and outputs are preserved. |
| The byte-identical supplied MPY semantics | Meaning of the translated program | Selected semantics boundary. Reachable rules were statically reviewed; it is not a theorem of full CPython equivalence. |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` bridge | Acceptable trusted translator; byte identity was independently checked. |
| Unboxed `list(asVals(IS))` as the read-only external input representation | `scan-loop`, `entry-prefix`, `main-correct` | Explicitly supported by the supplied semantics. It excludes mutation/alias observations and exposes the over-broad heap-ref normalization concern. |
| Built-in K integer arithmetic and `pyMod` for positive divisors | Trial division and digit accumulation | Acceptable ordinary arithmetic boundary; every proof use has divisor at least 2. |
| Proof-local `trialPrime`, `trialDivisor`, `largestPrime`, `digitAcc`, `digitSum` | Final result | Not opaque: equations are exhaustive on all uses and connected to real execution by proved claims. |
| Informal number-theory statement that trial division through `d*d <= n` decides standard primality | Human-facing phrase “largest prime” | Correct ordinary mathematics, supported but not formalized as a separate K theorem; this contributes to `CONCERNS`. |
| Bounded call-prefix bridge | `entry-prefix` and `main-correct` | Exact finite static derivation; independent bridge-free build passed but its proof timed out, so universal machine evidence is incomplete. |
| Supplied opaque float/sort/MD5 and symbolic string-order functions | None | Unreachable from this program and absent from the result/control slice; listed in the inventory but not relied on. |
| Differential corpus | Source/canonical/intent bridge only | Finite empirical evidence, not a substitute for any K claim. |

### Gate summary and verdict rationale

- Dynamic reconstruction: **PASS**.
- Real-program identity and result constraint: **PASS**.
- Non-vacuity: **PASS**.
- Main theorem-domain soundness: **PASS**, with a documented off-domain
  non-conservative `For` normalization and incomplete bridge-free machine
  evidence.
- Intent/evidence adequacy: **LIMITED** by the informal primality bridge,
  missing provenance records, no-prime underspecification, and the canonical
  `1` discrepancy.

These limitations fit `CONCERNS / LEGIT`: they neither substitute a different
program nor make the formally claimed result free, vacuous, or false on its
stated domain. A `PASS` would overstate global proof-extension fidelity and
intent evidence; a `FAIL` would incorrectly treat an off-domain stuck witness
or an audit timeout as proof that the reconstructed end-to-end theorem is
false.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
