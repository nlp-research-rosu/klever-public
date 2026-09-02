# Independent adversarial audit: 144-simplify

## Executive finding

The candidate's sole positive claim cleanly reconstructs: fresh definitions
compile, `kprove` prints `#Top`, the embedded closure body is mechanically equal
to the trusted regeneration of `solution.mpy`, a real body mutation breaks the
proof, and a false-result mutation is rejected. The Python implementation itself
also matches the natural-language mathematical contract.

The proof is nevertheless not a legitimate proof over the HumanEval input
domain. Its claim never supplies concrete decimal fraction strings. Instead it
supplies new terms `str(fractionCodes(A,B))`, and `verification.k` directly
defines how those new terms split and how their `numCodes(I)` components convert
to `I`. Neither constructor occurs in the trusted semantics, and there is no
equation or bridge-free reachability theorem relating either constructor to the
fixed `iCons` representation of actual decimal strings. The same unconstrained
integer labels drive both the execution bridges and the postcondition.

Thus the reconstructed theorem is non-vacuous but about a substituted,
proof-defined input representation. This materially narrows/replaces the
unrestricted valid-fraction string domain and meets the benchmark's
`FAIL / NOT_LEGIT` boundary.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, as required for this mode.
There is no semantics-mode contradiction and no audit infrastructure breach.

I independently checked all launcher-declared container paths and every record
required by this layout:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the complete structured trace (one JSONL file, 144 valid JSON records).

Historical `runtime-metrics.json` is absent, which is permitted for this legacy
layout. The campaign-lock JSON is exactly equal to the `audit_campaign` block,
and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All recorded direct hashes and all per-file hashes in
`generation-result.json` match their mounted files. `/task.json` is the exact
legacy subset of the enriched audit manifest; the only audit-only top-level
field is `config`.

The candidate prompt and translator are byte-identical to the trusted mounts.
The candidate and trusted `reference-semantics` trees each have 25 descendant
entries, have identical relative paths/types/file hashes, and contain no
symlinks. The candidate as a whole contains no symlinks. Candidate-built
definitions were not present or reused.

The generation records were read only as untrusted history. They report one
initial parse failure followed by `#Top`; none of those historical results was
accepted as proof evidence.

Evidence:

- [stage1_integrity.log](evidence/stage1_integrity.log)
- [trace_summary.log](evidence/trace_summary.log)
- [generation_log_inspection.log](evidence/generation_log_inspection.log)

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

For inputs `x = "A/B"` and `n = "C/D"`, where all four components are positive
whole numbers and denominators are nonzero, return `True` exactly when

`(A * C) / (B * D)`

is a whole number. Equivalently, because `B*D > 0`, return
`(A*C) % (B*D) == 0`.

The candidate implements exactly that integer test after splitting and parsing
the four components. It avoids the trusted canonical implementation's
floating-point division but preserves the stated mathematical behavior.

Running the trusted translator over the scratch copy produced SHA-256
`d59c7cca5edc79f46581c7072cafd3ce4342798676d80884fa5af2260b084c06`;
the submitted and regenerated `solution.mpy` files are byte-identical.

The independent differential script imports both trusted canonical and
candidate entry points and uses a separately written exact-divisibility oracle.
It checked:

- all three documented examples;
- minimum positive values, both Boolean branches, an exact divisibility
  boundary, a residue-one case, multi-digit components, and leading zeros;
- all 20,736 tuples `A,B,C,D` in `1..12`;
- 5,000 deterministic random tuples with components in `1..1,000,000`;
- empty strings and zero denominator as explicitly out-of-contract probes.

There were zero candidate/oracle mismatches and zero moderate
candidate/canonical mismatches. The invalid probes raised the same exception
classes in both Python implementations.

There is one deliberate intended-domain divergence at
`"9007199254740993/1" * "1/2"`: the exact answer and candidate are `False`,
while the canonical returns `True` because the half-integer rounds to an
integer-valued IEEE-754 float. The prompt states no magnitude bound, so this is
a bug in the canonical implementation relative to its prose contract, not a
candidate defect. It also means finite canonical agreement cannot replace
reasoning from the contract.

Evidence:

- [translator_regeneration.log](evidence/translator_regeneration.log)
- [differential_test.py](evidence/differential_test.py)
- [differential_test.log](evidence/differential_test.log)

Stage 2 result: PASS for the generated Python program.

## 3. Clean proof reconstruction

All work was done from copied sources below `/tmp/audit-work`; no candidate
compiled definition or cache was used.

The following fresh commands were run:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

Exit 0. An independently authored concrete program containing seven normal and
boundary assertions was translated with the trusted translator and executed
with the fresh LLVM definition. It ended with `.K`, `NoExc`, and exit code 0.

```text
kompile verification.k --backend haskell \
  --main-module SIMPLIFY-VERIFICATION \
  --syntax-module SIMPLIFY-VERIFICATION \
  --output-definition reviewer-verification-kompiled
```

Exit 0. The compiler warnings are in the fixed supplied semantics and do not
prevent the build.

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SIMPLIFY-SPEC
```

The command printed `#Top` and exited 0. The source inventory confirms that
`spec.k` contains exactly one positive target claim, so every positive target
was reconstructed.

Evidence:

- [kompile_llvm.log](evidence/kompile_llvm.log)
- [k_concrete_cases.py](evidence/k_concrete_cases.py)
- [krun_concrete.log](evidence/krun_concrete.log)
- [kompile_haskell.log](evidence/kompile_haskell.log)
- [kprove_positive.log](evidence/kprove_positive.log)

Stage 3 result: PASS as verification under the candidate-extended theory.

## 4. Adequacy and real-program pinning

### Plain-language claim

The precondition chooses arbitrary K integers `A,B,C,D > 0`, initializes the
standard empty module scope over the builtins scope, empty heap, fresh locations,
empty stack, `noRet`, `NoExc`, and exit code 0. Its two argument values are

```text
str(fractionCodes(A,B))
str(fractionCodes(C,D))
```

The postcondition requires the returned value to be exactly
`pyMod(A*C,B*D) == 0`; it also requires precisely two allocated split-list
objects, heap location 2, restored environment/scope location, empty stack,
`noRet`, `NoExc`, and exit code 0. This is an equality-constraining
postcondition, not a free variable, tautology, or one-way implication.

The precondition is satisfiable. For example, `A=1,B=5,C=5,D=1` makes every
guard true and the claimed result `True`. The witnesses
`(1,5,5,1)`, `(1,6,2,1)`, `(7,10,10,2)`, and `(1,1,1,1)` agree with the
claimed formula and both Python implementations.

### Program term

A reviewer script parsed the regenerated `FuncDef` and the proof's
`closureVal`. The normalized bodies have the same SHA-256,
`6f11248d0e5dd72578a48aba2c21637138bd2d673fc8437b7affcb19a38750ff`.
The parameter binding is `("x","n")`, the argument order is `(X,N)`, and the
closure captures scope 0. Directly applying this closure instead of first
loading and looking up the module binding is inert here: the body is
nonrecursive, refers only to its parameters and builtins, and the captured
scope/builtin parent is the same.

A separate mutation changed the actually executed outer `BinOp("%",...)` to
`BinOp("+",...)` in the wrapper. Its definition compiled, but the unchanged
claim produced `WarnStuckClaimState` and exited 1. This is genuine body
sensitivity, not an edit to an ignored external source file.

Evidence:

- [program_pinning.py](evidence/program_pinning.py)
- [program_pinning.log](evidence/program_pinning.log)
- [verification-body-mutation.k](evidence/verification-body-mutation.k)
- [kompile_body_mutation.log](evidence/kompile_body_mutation.log)
- [kprove_body_mutation.log](evidence/kprove_body_mutation.log)
- [claim_witness.log](evidence/claim_witness.log)

### Fatal input-domain mismatch

The mechanically pinned body does not receive the source-contract values.
For example, the actual K value for Python `"1/5"` is structurally

```text
str(iCons(49, iCons(47, iCons(53, .IntSeq))))
```

whereas the claim supplies `str(fractionCodes(1,5))`. These are different
constructors. No trusted file mentions `fractionCodes` or `numCodes`; the only
occurrences are the candidate declaration, its two proof rules, and the claim.
There is no equation, macro expansion, or auxiliary reachability theorem
connecting the terms.

Therefore constructor-level body pinning succeeds, but real-input pinning
fails. The theorem covers only the proof-created values, not all valid concrete
fraction strings.

Evidence:

- [abstract_constructor_search.log](evidence/abstract_constructor_search.log)
- [claim_witness.log](evidence/claim_witness.log)

Stage 4 result: FAIL on real-program input-domain adequacy.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-level inventory covers all 26 relevant K files: the assembled
supplied semantics, every supplied helper K file, `verification.k`, and
`spec.k`. It contains 1,101 declarations/records and 698 rules:

- 424 equational rules;
- 239 operational rules;
- 35 concrete-only rules;
- 45 priority rules;
- 25 supplied opaque/symbol declarations;
- 156 `function` and 115 `total` attribute occurrences;
- no `functional` declarations and no simplification rules.

Every record has a source range, full normalized text, classification, and
disposition in the inventory. The used-constructor map separately traces every
constructor in `solution.mpy` through evaluation order, lookup, calls,
allocation, tuple unpacking, integer arithmetic, return, and frame cleanup.

Evidence:

- [rule_inventory.log](evidence/rule_inventory.log)
- [used_construct_map.md](evidence/used_construct_map.md)

### Supplied semantics

The candidate's supplied tree is byte-identical to the trusted tree. The
Haskell proof imports `MPY`, not `MPY-KRUN`, so none of the 16
`concrete.k` rules contributes to `#Top`. Likewise, all 25 opaque float,
sort, and MD5 declarations are unreachable from this program. They do not
affect a string-split/integer-only theorem.

On the material path, the fixed rules preserve:

- left-to-right argument and binary-operand evaluation;
- ordinary scope lookup and builtin shadowing;
- split-list heap allocation and monotone heap locations;
- ordered tuple unpacking and local binding;
- ordinary closure call/return and stack restoration;
- exact unbounded integer multiplication, Python-style positive-divisor modulo,
  and Boolean equality.

The positive guards ensure the modulo divisor is nonzero. The fixed single- and
multi-digit conversion rules are reached only by actual `iCons` strings; valid
contract inputs contain only decimal digits. No fixed used rule encodes the
task answer.

### Candidate extensions

`verification.k` has exactly two local syntax declarations and three rules.
There are no local priorities, `total` declarations, simplification rules, or
auxiliary claims.

1. `numCodes(Int)` and `fractionCodes(Int,Int)` are fresh constructors, not
   defined encodings. They carry every symbolic input and result-bearing
   integer label. Disposition: illegitimate as a replacement for the concrete
   input representation.

2. `splitSep(fractionCodes(A,B),47,.IntSeq) => ...` is a result-bearing
   operational bridge/equation. It bypasses the fixed recursive scan and
   supplies both parsed components. Its constructor pattern is disjoint from
   the fixed `.IntSeq`/`iCons` equations, so there is no syntactic overlap, but
   there is also no bridge-free connection theorem.

   False-conclusion witness under an admitted opposite interpretation:
   if `fractionCodes(1,2)` denotes the valid concrete sequence for `"1/1"`,
   fixed split yields `["1","1"]`, whereas this rule yields labels `1,2`.
   With the other input `"1/1"`, fixed execution returns `True`, while the
   abstract postcondition is `pyMod(1,2)==0`, i.e. `False`. The absence of any
   encoding equations is exactly what leaves this opposite interpretation
   unexcluded.

3. `applyBuiltin("int",str(numCodes(I)),.Vals) => I` directly injects every
   arithmetic operand. Again its constructor pattern is disjoint from fixed
   concrete conversion, but no theorem connects it to decimal parsing. The same
   `I` appears in the bridge and postcondition.

   False-conclusion witness under an admitted opposite interpretation:
   if `numCodes(2)` denotes `iCons(51,.IntSeq)`, the valid concrete string
   `"3"`, fixed `int` returns 3 while the candidate rule returns 2. A name and
   an integer parameter do not prove that the underlying digits encode that
   integer.

4. `runSimplify` is an acceptable operational wrapper. It rewrites only the
   head computation to an ordinary application of the exact closure, preserves
   its continuation and all other cells, and has passed the program-body and
   body-sensitivity checks. It does not justify the two parsing bridges.

The complete proof-local record, including domains, state/value influence,
context, and witnesses, is in
[proof_extension_assessment.md](evidence/proof_extension_assessment.md).

Removing both disputed rules and rebuilding succeeds, but the proof then exits
1 with the expected residual
`splitSep(fractionCodes(A,B),47,.IntSeq)`. This establishes that `#Top`
depends on the unconnected bridge rather than fixed execution. A secondary
diagnostic that removed only the integer bridge was manually bounded and
interrupted after producing no result; it is not used as evidence for any
candidate defect.

Evidence:

- [verification-no-bridges.k](evidence/verification-no-bridges.k)
- [kompile_no_bridges.log](evidence/kompile_no_bridges.log)
- [kprove_no_bridges.log](evidence/kprove_no_bridges.log)
- [kprove_no_int_bridge.log](evidence/kprove_no_int_bridge.log)

Stage 5 result: FAIL. The wrapper and fixed material rules are sound, but both
result-bearing proof-local parsing bridges lack the mandatory universal
connection and substitute a proof-defined domain.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I authored a fresh mutation that
keeps the satisfiable precondition and all cells but changes the destination to
the negation of the actual divisibility Boolean:

```text
notBool (pyMod(A*C,B*D) == 0)
```

For `A=B=C=D=1`, the precondition is true, actual execution returns `True`, and
the mutated destination is `False`.

The mutation's `kprove --dry-run` exited 0, establishing that it parses and
builds against the fresh definition. Full `kprove` then exited 1 with
`WarnStuckClaimState`; the residual explicitly says the actual Boolean cannot
be proved equal to its negation. This is the expected unmet result obligation,
not a parser error, missing import, timeout, or unrelated crash.

Evidence:

- [spec-vacuity.k](evidence/spec-vacuity.k)
- [kprove_vacuity_dry_run.log](evidence/kprove_vacuity_dry_run.log)
- [kprove_vacuity.log](evidence/kprove_vacuity.log)

Stage 6 result: PASS. The candidate theorem is discriminating inside its own
extended theory. Non-vacuity does not supply the missing real-input connection.

## 7. Proven versus assumed accounting

### What `#Top` actually proves

Under the candidate-extended K theory, for all positive K integers
`A,B,C,D`, invoking the exact submitted function body on the two fresh values
`str(fractionCodes(A,B))` and `str(fractionCodes(C,D))` terminates at the
Boolean `pyMod(A*C,B*D)==0`, with the specified two abstract split lists in the
heap and the remaining control/state cells restored.

That is a genuine, result-constraining reachability theorem about those new
values. It is not a theorem that the submitted program has this result for
every concrete Python fraction string.

### Trust ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K 7.1.293 frontend, Haskell backend, SMT/hooks, built-in integer/Boolean/map/list theories | All compilation and reachability reasoning | Ordinary low-level proof trust; acceptable. |
| Trusted prompt and translator | Contract and Python-AST constructor identity | Hash-checked and byte-checked; acceptable. |
| Trusted supplied semantics | Language execution | Candidate copy is exact; used fixed path reviewed and concretely exercised. |
| Supplied float/sort/MD5 opaque symbols | Potential values in unrelated programs | Unreachable here; no influence on this claim. |
| Manual `runSimplify` wrapper | Chooses body, parameters, binding environment, and call context | Constructor equality plus body-sensitivity evidence makes this acceptable for the immutable candidate; lack of automatic regeneration is only a maintenance observation. |
| `fractionCodes` split bridge | Determines parsed numerator/denominator strings, allocations, and all downstream values | Illegitimate program-derived abstraction; no fixed-semantics connection theorem. |
| `numCodes` integer bridge | Determines all four arithmetic operands, branches, and final postcondition | Illegitimate and circular; no decimal encoding definition or connection theorem. |
| Python differential tests | Candidate-to-contract/canonical bridge on 25,746 moderate executions plus one precision boundary | Strong finite evidence for the Python implementation only; not a universal K connection theorem. |
| Ground claim witnesses | Satisfiability and formula checks | Establish nonempty abstract precondition and expected values, not input representation equivalence. |
| Partial-correctness interpretation | If execution reaches termination, postcondition follows | Standard scope of the Kit workflow; the fatal issue is theorem domain, not termination wording. |

### Gate accounting and decision

- Gate A (real-program soundness): FAIL. Body pinning and non-vacuity pass, but
  the two result-bearing program-derived bridges have no bridge-free universal
  connection theorem. Removing them exposes the fixed-semantics residual.
- Gate B (intent adequacy): FAIL. The source contract ranges over every valid
  concrete positive fraction string; the claim ranges only over
  `fractionCodes` terms.
- Gate C (trust/evidence): FAIL for the parsing abstraction. All reviewer
  commands and finite tests are reproducible, but finite tests cannot validate
  the missing universal bridge.

This is not an infrastructure or tool timeout verdict. The clean positive proof
succeeded. The failure is a candidate theorem/extension defect: it proves a
substituted abstract-input program. Under the benchmark-specific mapping,
materially narrowing/replacing the unrestricted HumanEval source-contract
domain is `FAIL / NOT_LEGIT`, even though the restricted theorem is
non-vacuous.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
