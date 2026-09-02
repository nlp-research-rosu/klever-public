# Independent adversarial audit: 2-truncate-number

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program, but the theorem deliberately stops at the supplied semantics'
result-bearing, symbolically opaque `floatMod` primitive. The program body,
translation, and claim are pinned exactly; the proof reconstructs to `#Top`;
and fresh postcondition and body mutations are rejected. The remaining issue is
a non-fatal trust-boundary limitation: K does not prove the universal algebraic
connection between `floatMod(N, 1.0)` and the natural-language “decimal part.”
That connection is conditional on the supplied primitive contract and is
supported only by concrete and differential evidence.

This is therefore `CONCERNS / LEGIT`, not `FAIL`: the source domain is not
narrowed, no program-defined computation is replaced, and no false conclusion
witness was found on the intended positive finite-float domain.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `2-truncate-number`;
- condition `semantics`;
- mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. There is no mode/mount contradiction.

I independently checked all launcher-required records and mounted inputs.
`/audit-campaign-lock.json` is structurally identical to the
`audit_campaign` block, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The recorded hashes of `/run.json`, `/task.json`,
`/generation-result.json`, invocation/metrics/usage records, prompt,
transcript, last message, trusted canonical, trusted prompt, and trusted
translator all match. Every declared trace output also matches the hash in
`generation-result.json`.

The candidate prompt and translator are byte-identical to the trusted mounts.
A recursive path/type/content inventory found 25 entries in each supplied
semantics tree and exact equality at every entry. Neither tree, the candidate,
nor the structured trace contains a symlink.

The required legacy-selected-stage1 records were read. The structured trace is
valid JSONL with 137 events, including 23 tool calls and 23 corresponding
outputs. The 4,551-line transcript was scanned in full. Those records report a
generation-time `#Top`, but no generation claim was used as proof evidence.

Evidence:

- `evidence/integrity_check.sh`
- `evidence/stage1-integrity.log` — exit 0
- `evidence/inspect_generation_records.py`
- `evidence/stage1-generation-record-inspection.log`

No audit infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a positive finite floating-point input, split the number into its floor
integer part and a remaining fractional part smaller than one, and return that
fractional part. The sole documented example is `3.5 -> 0.5`.

The trusted canonical implementation and candidate implementation both execute:

```python
return number % 1.0
```

Using the trusted translator in scratch produced a file byte-identical to the
submitted `solution.mpy`; both have SHA-256
`5d32e9ddf2a574995accfcef87ffef589188b82d429829d07945f85142d5c4e0`.

The independent differential test imports the trusted and candidate entry
points separately. It covers the documented example, the smallest positive
binary64 value, points immediately around integer boundaries, exact integers,
large values, the maximum finite value, and 5,000 seeded random positive finite
binary64 values. It also probes zero and negatives as out-of-contract boundary
diagnostics. Results:

- 5,015 in-domain inputs;
- zero candidate/canonical mismatches;
- zero violations against the independent `math.modf` decomposition;
- six out-of-domain boundary inputs, also with zero candidate/canonical
  mismatches.

Exact commands and results are in:

- `evidence/stage2-regeneration.log` — exit 0
- `evidence/differential_test.py`
- `evidence/stage2-differential.log` — exit 0

There is no empty-container case or branch boundary in this scalar,
straight-line function; integer transitions are the material boundaries.

## 3. Clean proof reconstruction

All execution occurred from the fresh copy
`/tmp/audit-work/truncate2-reconstruction`. No candidate-built definition or
cache existed or was reused. The installed tools report K v7.1.293.

The fresh commands were:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled

krun concrete_tests.mpy --definition auditor-runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled

kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC
```

The LLVM build exited 0. It warned about six non-exhaustive `total` functions:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is
reachable from this program. The candidate concrete assertions reached `.K`,
`NoExc`, and exit code 0.

The Haskell build exited 0. Its only warnings are unused tail variables in two
ground string-order equations. The sole positive target claim then printed
`#Top` and exited 0.

Evidence:

- `evidence/stage3-tool-versions.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-krun-candidate-tests.log`
- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-positive.log`

The positive reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

There is no `requires` clause. The initial state has environment 0; an empty
module scope whose parent is the fixed builtins scope; empty heap and call
stack; locations 1 and 0; `noRet`; `NoExc`; and exit code 0. `N` may be any K
`Float`, so the claim does not narrow the positive source-contract domain.

The computation loads `solutionProgram` and calls the binding
`truncate_number` on the expression `Float(N)`. At completion:

- `<k>` contains exactly `floatMod(N, 1.0)`, with no free result variable and no
  framed continuation;
- the module scope contains exactly the closure loaded from the submitted body;
- the temporary call scope is gone;
- heap, heap location, stack, return state, exception state, and exit code have
  their required final values.

Thus this is a result-constraining exact reachability claim, not a tautology or
one-way implication.

### Mechanical program identity

Trusted regeneration first pins `solution.py` to `solution.mpy`. A separate
constructor-level check removes comments/whitespace, extracts the
`solutionProgram` macro RHS, and compares it with the regenerated term. Both
normalize to:

```text
Module(FuncDef("truncate_number",Params("number"),Return(BinOp("%",Name("number"),Float(1.0)))))
```

The claim loads that macro and calls the exact loaded binding. The destination
closure body repeats the same constructor term. There are no helper or loop
claims.

Evidence:

- `evidence/program_pinning.py`
- `evidence/stage4-program-pinning.log` — every check true, exit 0

### Satisfiable witness and substitution

Set `N = 3.5` in the exact initial configuration. This is a well-sorted,
satisfiable state. Both Python implementations return `0.5`, and fresh LLVM
execution of the actual translated function checks `3.5 -> 0.5`. The broader
LLVM suite also checks `1.5 -> 0.5`, integer boundaries, large inputs, and an
exactly encoded minimum binary64 subnormal.

An additional ground Haskell witness was attempted and is preserved in
`evidence/stage4-ground-witness-kprove.log`. It fails because the Haskell
backend lacks the `FLOAT.div` hook when the `[concrete]` `floatMod` equation
fires on a ground term. This is not used as proof success and does not affect
the symbolic target claim, which intentionally retains `floatMod` opaque.
Concrete witness execution is instead supplied by LLVM.

### Body sensitivity

The reviewer changed the term actually executed by the claim from
`BinOp("%", ...)` to `BinOp("+", ...)`, rebuilt a distinct Haskell definition,
and retained the original modulo result obligation. Compilation exited 0; proof
exited 1 with `WarnStuckClaimState` and the expected unmet equality:

```text
addF(N, 1.0) = floatMod(N, 1.0)
```

Evidence:

- `evidence/verification-body-mutation.k`
- `evidence/spec-body-mutation.k`
- `evidence/stage5-body-mutation-kompile.log`
- `evidence/stage5-body-mutation-kprove.log`

The theorem is sensitive to the submitted body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule-inventory.md` enumerates every local declaration or rule in the
assembly, all supplied helpers, `verification.k`, and `spec.k`, with source
line, full normalized text, and attributes. Its checked totals are:

- 228 syntax declarations;
- 696 rules;
- five contexts;
- one configuration;
- one claim;
- 145 function declarations, including 107 marked `total`;
- 25 symbols, 22 also marked `no-evaluators`;
- 45 priority-bearing rules;
- 35 concrete rules;
- no `functional` declarations and no `simplification` rules.

The top-level `reference-semantics/semantics.k` has no local operational rule;
it assembles the modules. `MPY` is the proof import. `MPY-CONCRETE` is imported
only by `MPY-KRUN`, not by the proof module.

The table below makes a decision for every numbered inventory range. “Inert”
means constructor, sort, operator, call target, or continuation guards make
every item in that range unreachable from the submitted program. Such items
cannot enable a false conclusion for this theorem. I found no intended-domain
false witness for any inert item, so I do not label those broader semantics
fragments unsound.

| Inventory range | Module | Static decision for this proof |
|---|---|---|
| 0001–0003 | `assert.k` | Correct truthy/failure routing for concrete smoke tests; absent from the target claim. |
| 0004–0017 | `bool.k` | Guarded short-circuit equations are pairwise complementary; inert. |
| 0018–0192 | `builtins.k` | Builtin-specific heads and folds are inert. `mapStrVS` has a compiler-reported totality coverage gap outside its int/string subset; it cannot match this program. |
| 0193–0216 | `call.k` | Items 0195–0196 and 0212 implement the real call path. Other callable/heap routes are sort- or binding-disjoint and inert. |
| 0217–0226 | `comprehension.k` | Syntax macros recurse structurally; no comprehension occurs. |
| 0227–0247 | `concrete.k` | Excluded from the proof definition; LLVM-only list equality/keyed-sort support is inert. |
| 0248–0284 | `controls.k` | Assignment/import/branch/loop rules are constructor-disjoint from the body; inert. |
| 0285–0368 | `core.k` | Configuration, load/sequencing, lookup, builtin scope, argument evaluation, and value declarations preserve the exact cells used here. Remaining heap/truth/list helpers are inert. |
| 0369–0408 | `dict.k` | All heads require dict constructors or subscript assignment; inert. |
| 0409–0563 | `float.k` | Items 0409–0410 and 0417–0419 are the result path. Other float/math heads are inert. The `floorFI`/`toF`/`ceilF` totality warnings concern unused `Val` alternatives. |
| 0564–0582 | `functions.k` | Items 0565, 0577–0580, and 0582 correctly load, bind, return, restore, and delete the temporary frame. Cell/closure variants are guarded and inert. |
| 0583–0599 | `int.k` | Sort-disjoint from float `%`; inert. |
| 0600 | `iter.k` | Declaration only; inert. |
| 0601–0632 | `list.k` | List constructors/operators/membership are absent; inert. |
| 0633–0734 | `methods.k` | Method-specific equations are inert. `joinCodes` has an unused non-string coverage warning. |
| 0735–0746 | `operators.k` | Item 0736 dispatches the fully evaluated float `BinOp`; ref priority rules cannot match either operand. Other items are inert. |
| 0747–0754 | `range.k` | No range object or iterator; inert. |
| 0755–0772 | `set.k` | No set value or operation; inert. |
| 0773–0797 | `sort.k` | Both opaque sort symbols and all sort routes are inert. |
| 0798–0830 | `str.k` | No string operation; inert. The compiler's unused-tail warnings do not change the guarded lexicographic equations. |
| 0831–0887 | `subscript.k` | No index or slice; inert. `valSeqAt`'s out-of-bounds/opaque totality gap cannot match this body. |
| 0888–0903 | `syntax.k` | `Module`, `FuncDef`, `Return`, `Call`, `Name`, `Float`, and `BinOp` declarations exactly cover the generated AST. `Return` strictness and `BinOp` `seqstrict(2,3)` preserve evaluation order. |
| 0904–0928 | `tuple.k` | Tuple/unpack target heads are absent; inert. |
| 0929–0930 | `verification.k` | A definitional syntax macro only. Its RHS is constructor-identical to trusted regeneration and does not bypass execution. |
| 0931 | `spec.k` | Exact, satisfiable, result-bearing claim analyzed in stage 4. |

### Exact reachable rule path

The actual symbolic path is:

1. Macro expansion 0929–0930 supplies the exact submitted module.
2. Core 0324–0326 loads and sequences it.
3. Function rule 0565 installs the closure in scope 0.
4. Call 0195, lookup 0328–0329, call 0196, and argument rules 0336–0338
   evaluate the selected binding and its sole argument left-to-right.
5. Call rule 0212 allocates a temporary scope and frame.
6. Binding rules 0578 then 0577 bind `number`; the higher-priority cell rule
   0579 is inapplicable because this is a plain frame without `"$cells"`.
7. Float literal rule 0410 and operator dispatch 0736 evaluate the expression.
   No ref-priority rule can match.
8. Float equation 0419 maps this exact `%` operation to
   `floatMod(N, 1.0)`.
9. Return and pop rules 0580 and 0582 restore every claimed cell and deliver
   that value to the empty continuation.

There is no proof-local operational bridge, priority rule, lemma,
simplification, or opaque symbol. The only result-bearing abstraction is the
fixed-semantics primitive `floatMod`.

### `floatMod` boundary

The relevant fixed declarations are:

```k
syntax Float ::= floatMod(Float, Float)
  [function, total, symbol(floatMod), no-evaluators]
rule floatMod(F1, F2)
  => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

For symbolic Haskell execution, `floatMod` is intentionally opaque. For fresh
LLVM execution, 272 ordinary/boundary/large positive cases passed against
CPython-expected results, as did a directly and exactly encoded minimum
binary64 subnormal. The initial generated suite's short `5e-324` source literal
failed: the K token retained the short decimal value while arithmetic rounded
to `4.9406564584124654e-324`. A direct token probe establishes that the exact
binary64 embedding returns the expected value. This is a concrete literal
embedding/translator evidence limitation. It does not alter `solution.mpy`,
whose only literal is exactly representable `1.0`, or the claim's symbolic
input.

Evidence:

- `evidence/generate_k_float_tests.py`
- `evidence/k-float-tests.py` and `evidence/k-float-tests.mpy`
- `evidence/stage5-locate-k-float-mismatch-final.log`
- `evidence/stage5-k-float-normal-suite-final.log`
- `evidence/float-token-probe.mpy`
- `evidence/stage5-float-token-probe-krun.log`
- `evidence/float-subnormal-exact-assert.mpy`
- `evidence/stage5-float-subnormal-exact-assert.log`

Some earlier exploratory float-localization logs used a shared scratch
filename concurrently and are superseded by the two `*-final.log` runs above;
they are retained rather than hidden.

## 6. Fresh non-vacuity test

The reviewer-authored mutation changes only the result obligation:

```text
floatMod(N, 1.0)  ->  floatMod(N, 2.0)
```

It is demonstrably false for the satisfying intended input `N = 1.5`:
CPython and concrete K give `1.5 % 1.0 = 0.5`, while
`1.5 % 2.0 = 1.5`.

The mutation dry run compiled successfully and exited 0. The actual proof then
exited 1 with `WarnStuckClaimState`. Its residual is the expected unmet
obligation:

```text
floatMod(N, 1.0) = floatMod(N, 2.0)
```

This is a meaningful reachable proof failure, not a parser error, timeout,
missing import, or unrelated backend failure.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6-vacuity-dry-run.log`
- `evidence/stage6-vacuity-kprove.log`

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied MPY semantics, from the exact initial state in `spec.k`, for
every K `Float` value `N`, executing the exact regenerated module, resolving
and calling its `truncate_number` binding, and executing its actual body reaches
an exact final state whose returned computation value is
`floatMod(N, 1.0)`. The call frame is removed, the module binding is retained,
no exception is present, and exit code remains zero. This is a
partial-correctness result; it is also structurally terminating along the
modeled straight-line path.

It does **not** internally prove a theorem such as
`0 <= floatMod(N,1.0) < 1` or
`floatMod(N,1.0) = N - floor(N)`. The natural-language interpretation remains
conditional on the supplied primitive's contract.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K parser, compiler, Haskell prover, and reachability calculus | All proof closure | Standard toolchain trust; fresh K v7.1.293 build and run recorded. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte-identity regeneration plus independent constructor-level macro comparison. |
| Supplied MPY operational semantics | Binding, evaluation, control, state | Candidate tree is exactly the trusted tree. Every reachable rule was reviewed; the full local inventory is preserved. |
| `floatMod(Float,Float)` | Entire returned value and postcondition | Fixed external primitive, not program-defined code. Symbolically opaque; concrete floor-based equation and LLVM evidence support it. The universal Python/decimal-part connection is assumed, not machine-proved. |
| K FLOAT hooks in LLVM | Concrete evidence only | `/Float`, `floorFloat`, `*Float`, `-Float`, and equality are trusted backend operations. Haskell lacks the ground `FLOAT.div` hook; this limits ground proof evidence but not the symbolic target proof. |
| Other opaque symbols (`md5hexCodes`, other float helpers, `sortVS`, `sortKeyVS`) | None | Imported but unreachable from this program and absent from all target obligations. |
| Python canonical and `math.modf` differential tests | Source/canonical and intent bridge | 5,015 positive finite examples, zero mismatches. Finite evidence only, not a universal proof. |

### Gate assessment and decision

- Real-program soundness: **PASS**. The actual body executes; there is no
  proof-local execution shortcut; state/control are preserved; the exact
  result is constrained; and both body and postcondition mutations are
  rejected.
- Intent adequacy: **PASS, conditional on the named fixed-semantics
  `floatMod` contract**. The formal domain does not narrow the source domain,
  and the program is identical to the trusted canonical implementation.
- Trust/evidence auditability: **PASS with limitation**. All evidence is
  reproducible and assumptions are explicit, but the result-bearing float
  primitive and its decimal-part interpretation are not universally proved in
  K. The short-min-subnormal literal probe further limits how concrete
  translator-generated tests should be interpreted.

Under the benchmark decision boundary, those non-fatal result-bearing
trust/intent limitations warrant `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
