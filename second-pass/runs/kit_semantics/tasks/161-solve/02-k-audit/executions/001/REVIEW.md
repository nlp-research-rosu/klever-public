# Independent adversarial review: 161-solve

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied K model. Fresh reconstruction
closed both target claims with `#Top`, the executed function body is
constructor-identical to trusted regeneration of `solution.py`, and independent
mutations show that both the body and postcondition matter.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, solely because the fixed
supplied semantics has a material, documented ASCII/Unicode representation and
behavior gap. The proof covers every finite `IntSeq` admitted by that model
without candidate-imposed narrowing, the candidate explicitly records the
boundary and a concrete witness, and `solution.py` itself follows CPython's
Unicode `isalpha`/`swapcase` behavior. That is exactly campaign amendment v2's
documented supplied-model exception. No canonical/docstring contradiction was
found.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `161-solve`, and the expected
container mounts. I read it before inspecting candidate claims.

All required launcher records are present, regular, and readable:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the sole structured trace
  `codex-trace/2026/07/30/rollout-...jsonl`.

The structured trace has 527 valid JSON records. Its event/function-call
inventory is in `evidence/stage1_integrity.log`; generation assertions such as
the earlier `VALIDATED` report were treated only as untrusted history.

Independent SHA-256 checks match every recorded file hash checked by the
launcher manifest, including:

- campaign lock
  `053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`;
- prompt
  `fa29d7f413a74f20646e32cd02cb87cdd6766bf4f81745a92db8bcd19d9734d2`;
- translator
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- canonical
  `b26b53cdaa887f05a2d6d811bfe015acbb1c50154dd70b12d59d9bbbc2e442b0`;
- run/task/result and all generation-evidence files, including trace file
  `f2ae765cbc4c7603575f7244b552897fae0c13cdd7d5d2113a6e0432a16353aa`.

The parsed `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` object in `/audit-input.json`, including campaign v3 and the
recorded audit-prompt hash. Candidate `prompt.py` and `py2mpy.py` are
byte-identical to their trusted mounts.

The candidate and trusted `reference-semantics/` trees contain the same 24
regular files, no symlinks, no additions, and no omissions. A recursive,
type-sensitive `diff --no-dereference` is empty, and the evidence log lists the
independent SHA-256 of every semantics source. This is stronger than accepting
the manifest's aggregate-tree assertion without inspection.

All six required candidate proof artifacts are regular files. Candidate
`runtime-kompiled`, `verification-kompiled`, `lemma-kompiled`, and all caches
were ignored. Only source files were copied into
`/tmp/audit-work/161-solve/scratch`.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log` — exit 0, `STAGE1_INTEGRITY PASS`

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a Python string `s`:

1. if the string contains at least one letter, return a string in which every
   letter has its case swapped and every nonletter is unchanged;
2. if it contains no letters, return the reverse of the original string.

The determined examples are `"1234" -> "4321"`, `"ab" -> "AB"`, and
`"#a@C" -> "#A@c"`. Empty input has no letters and reverses to itself.

`solution.py` implements exactly this reading. It builds both the reverse and
the per-character transformed string in one pass, records whether any
`c.isalpha()` was true, and selects the appropriate result. This different
algorithm is equivalent to the canonical witness. In particular, it directly
uses CPython `str.isalpha()` and `str.swapcase()`, so Unicode case expansions
such as `"ß".swapcase() == "SS"` are retained.

### Trusted regeneration

Exact command:

```text
python3 /reference/py2mpy.py /tmp/audit-work/161-solve/scratch/solution.py > /tmp/audit-work/161-solve/scratch/regenerated-solution.mpy
```

Exit was 0. Both regenerated and submitted files hash to
`264f03a00c1b83794c68c804e7ab57802a9ffffb63c1ef3818ab7c0cd4898f36`,
and `cmp` exits 0. The regenerated artifact is preserved as
`evidence/regenerated-solution.mpy`.

### Independent differential

`evidence/differential_audit.py` imports the trusted canonical and the candidate
from the scratch copy and also uses a separately written direct transcription
of the docstring as the primary oracle. It covers:

- all three documented examples;
- 40 declared boundary cases;
- every string of length 0 through 4 over an 11-character alphabet spanning
  ASCII lower/upper letters, digits, punctuation, whitespace, accented and
  expanding-case letters, Greek, combining marks, and emoji;
- 20,000 deterministic random strings of length 0 through 32 using seed 161.

There were 34,716 distinct inputs and zero candidate-vs-contract,
canonical-vs-contract, or candidate-vs-canonical mismatches. This is finite
evidence, not a substitute for the K theorem.

The same script gives the material gap witness:

```text
SUPPLIED_MODEL_DIVERGENCE_WITNESS 'é1' CPYTHON= 'É1' ASCII_MODEL= '1é'
```

Evidence:

- `evidence/stage2_program_fidelity.sh`
- `evidence/stage2_program_fidelity.log` — exit 0,
  `STAGE2_PROGRAM_FIDELITY PASS`
- `evidence/differential_audit.py`

## 3. Clean proof reconstruction

All following definitions were built freshly below
`/tmp/audit-work/161-solve/scratch` from the copied candidate source and the
trusted semantics tree.

### Concrete definition and execution

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit was 0. Compiler non-exhaustiveness warnings concern unused fixed-model
helpers and are accounted for in Stage 5.

Fresh concrete cases were translated with the trusted translator and run using:

```text
krun concrete_cases.mpy --definition runtime-kompiled
```

Exit was 0 with `.K`. K and CPython agree on examples, empty input, one-letter
and one-nonletter inputs, odd-length reversal, letters at either boundary, and
ASCII case-range boundaries. The exact result bindings are in
`evidence/stage3_concrete_cases.log`.

The supplied-model witness is independently executable:

- CPython imports `concrete_unicode_gap.py` and returns `'É1'`;
- trusted translation succeeds;
- fresh `krun` stops at `strToCodes("\xc3\xa91")` and exits 113.

This is an expected fixed-semantics representation failure, not a candidate
proof failure. Source and translated witness are preserved in `evidence/`.

### Proof definition and target claims

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit was 0.

The loop claim was independently selected:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
```

Output was `#Top`; exit 0.

The required complete-spec invocation retains the loop circularity while
checking both the helper and entry claims:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Output was `#Top`; exit 0. This is the positive target-proof command.

As a diagnostic, selecting only `SPEC.solve-full-domain` also removes the
helper circularity from the proof module and consequently unrolls the symbolic
loop; I interrupted that non-target diagnostic after 90 seconds (exit 130).
It is preserved in `evidence/stage3_kprove_entry.log` and is not treated as
candidate failure or positive evidence.

### Proof-local constructor lemma

A separate definition omitting the candidate simplification was freshly built:

```text
kompile --backend haskell lemma-verification.k \
  --main-module LEMMA-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove lemma-spec.k --definition lemma-kompiled --spec-module LEMMA-SPEC
```

Both commands exit 0. The lemma proof prints `#Top` and
`WarnTrivialClaim`, establishing constructor disjointness without importing the
candidate rule.

Evidence:

- `evidence/stage3_runtime_build.log`
- `evidence/stage3_concrete_cases.log`
- `evidence/stage3_unicode_gap.log`
- `evidence/stage3_verification_build.log`
- `evidence/stage3_kprove_loop.log`
- `evidence/stage3_kprove_all.log`
- `evidence/stage3_lemma_build.log`
- `evidence/stage3_kprove_lemma.log`

Stage 3 passes.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiability

`SPEC.loop-invariant` begins at the actual fixed-semantics loop head:

```text
#loop(str(REST), Name("c"), loopBody)
```

For arbitrary finite remaining input and arbitrary initial accumulators, it
executes the loop and establishes:

- `c = lastChar(REST, C0)`;
- `has_letter = alphaAcc(REST, FOUND)`;
- `reversed_s = revISAcc(REST, REV)`;
- `swapped = toggleAcc(REST, SWAPPED)`.

The local `s` binding remains `str(INPUT)`. The claim preserves arbitrary
heap, heap counter, stack, outer scopes, and continuation while fixing the
actual call environment, scope counter, return/exception state, and exit code.
The invariant matches the fixed `#loop`/`#loopLbl` control flow and has no
return, break, exception, allocation, or frame-pop bridge.

A satisfying loop state is, for example, `REST=.IntSeq`, `C0=str(.IntSeq)`,
`FOUND=false`, `REV=.IntSeq`, `INPUT=.IntSeq`,
`SWAPPED=.IntSeq`, environment 1, a scope-1 map with the five named locals and
parent 0, scope counter 2, empty heap/stack, `noRet`, `NoExc`, and exit 0.

`SPEC.solve-full-domain` begins from the exact module configuration, loads and
binds `solve`, invokes it on arbitrary `str(INPUT)`, executes its body, returns
through the fixed frame machinery, and assigns the result to `answer`. It has
no `requires` clause or length bound. Its final state constrains:

```text
"answer" |-> solveResult(INPUT)
```

as an equality, not an implication or free value. The existentially irrelevant
post-state value `?SOLVE` does not weaken the exact `answer` obligation.
`INPUT=.IntSeq` and `INPUT=iCons(97,.IntSeq)` are concrete satisfying entry
witnesses.

### Mechanical body identity

Trusted regeneration already pins `solution.py` to `solution.mpy`.
Independently, I parsed:

1. the regenerated/submitted `solution.mpy`; and
2. `Module(FuncDef("solve", Params("s"), solveBody))`

with `kast --module VERIFICATION --sort Module --expand-macros --output json`.
Both expanded constructor trees hash to
`3c864e8ded4202f423c64500838ba59e0bc8e9ba804679349b7f67c32b26f46c`
and `cmp` exits 0. The entry claim's additional symbolic call/`answer`
assignment is a test harness around that exact binding and body.

Evidence:

- `evidence/stage4_body_pinning.log`
- `evidence/solution-expanded.json`
- `evidence/claim-body-expanded.json`

### Ground substitutions

Five ground `solveResult` claims close together with `#Top`: empty, letter plus
digit, no letters, ASCII case boundaries, and code 233 as the explicit fixed
model boundary. For the four modeled ASCII cases, the formal expected result,
candidate, and canonical all agree:

```text
''      -> ''
'a1'    -> 'A1'
'1#2'   -> '2#1'
'AzZa'  -> 'aZzA'
```

For `"é1"`, the formal fixed-model summary is `"1é"` while both Python
programs return `"É1"`; no Unicode equivalence is claimed.

Evidence:

- `evidence/ground-results.k`
- `evidence/ground_compare.py`
- `evidence/stage4_ground_results.log`

### Body sensitivity

A fresh claim changes the executed function term so alphabetic input returns
`reversed_s`, while leaving the one-character input `"a"` and expected original
result unchanged. It parses and executes to terminal `answer = "a"`, then exits
1 with `WarnStuckClaimState` because the original contract requires `"A"`.
Thus changing the actual body changes proof validity.

The earlier macro-declaration setup error is preserved separately and was not
counted as evidence.

Evidence:

- `evidence/body-sensitivity.k`
- `evidence/stage4_body_sensitivity.log`
- excluded setup attempt:
  `evidence/stage4_body_sensitivity_setup_error.log`

Stage 4 passes.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.py` inventories every local declaration and rule in
all 24 supplied semantics files plus `verification.k`. Its totals are
independently reconciled with `rg`:

- 251 syntax-declaration starts;
- 778 rule starts;
- 5 contexts and 1 configuration;
- 56 priority-rule records;
- 5 simplification-rule records;
- 75 concrete-rule records;
- 24 opaque `no-evaluators` declaration records;
- 122 records carrying `total`.

The full 1,035-record line-level inventory is
`evidence/rule_inventory.log`. The per-class and per-rule audit decisions,
including all 21 proof-local records, are in
`evidence/static_soundness.md`.

### Used syntax and operational path

Every constructor in `solution.mpy` maps to `syntax.k`: `Module`, `FuncDef`,
`Params`, `Expr`, `Str`, `Assign`, `Name`, `Bool`, `For`, `BinOp`, `If`,
`Call`, `Attribute`, `AugAssign`, `Return`, and the list units.

The actual path uses:

- `core.k` for configuration, module/statement sequencing, lexical lookup,
  literal evaluation, left-to-right argument evaluation, truthiness, and scope
  data;
- `str.k` for ASCII source literals, immutable concatenation, and string
  iteration;
- `operators.k` for `BinOp` dispatch;
- `methods.k` for the fixed `isalpha`, `swapcase`, reverse, ASCII
  classification, and case-map functions;
- `controls.k` for plain-local assignment, `If`, and the `For` protocol;
- `tuple.k` for binding each yielded character to `c`;
- `call.k` and `functions.k` for actual callee lookup, closure entry, parameter
  binding, return, frame pop, environment restoration, and scope deallocation.

The order and cell footprint are faithful for this program. Method calls are
pure fixed-function dispatches; the user function itself is not summarized or
intercepted. No exception, output, heap mutation, or allocation is skipped.

### Proof-local rules

There are no priority rules, operational bridges, opaque symbols, or trusted
program-derived primitives in `verification.k`.

- `loopBody` and `solveBody` are compile-time macros, mechanically shown exact.
- The one `==K` simplification is a bridge-free proven constructor lemma.
- `charAlpha` is exactly the fixed method's one-character predicate.
- `alphaAcc`, `toggleAcc`, and `lastChar` have constructor-disjoint base/step
  cases and structurally descend on `REST`.
- Alphabetic/nonalphabetic guards are Boolean complements, so they are
  disjoint and exhaustive.
- `solveResult` has complementary branches after total `alphaAcc`; it names a
  result but never rewrites executing program syntax.
- The loop circularity supplies the machine-checked connection from the exact
  real loop to those summaries.

Thus none of the task answer is assumed as an axiom. Removing or changing the
executed body is detected by the body-sensitivity probe.

### Supplied-model declarations outside the path

The Haskell proof imports `MPY`, not `MPY-CONCRETE`; concrete-only sorting and
deep-equality rules cannot contribute to `#Top`. All 24 opaque float/sort/MD5
symbols are absent from the program, helper claim, and postcondition.

Fresh LLVM compilation warns that fixed `[total]` declarations
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt` are not
equationally exhaustive over the enlarged `Val` constructors. None is
reachable here. Totality can leave such an unused term defined/opaque; it does
not provide a false equality for `solveResult`.

The only material language mismatch on the used path is the supplied
ASCII-only `strToCodes`/`isAlphaC`/`swapC` model. The candidate neither authored
nor strengthened that boundary. No candidate-authored unsound rule was found,
so no false-conclusion witness is asserted. The concrete Unicode witness is
reported as a model gap, not mislabeled as a proof-rule inconsistency.

Stage 5 passes for real-program soundness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer claim
`evidence/fresh-vacuity.k` executes the unmodified, exact `solveBody` on
satisfying input `"a"` but changes the result obligation to require lowercase
`"a"`.

Exact command:

```text
kprove /audit-output/evidence/fresh-vacuity.k \
  --definition verification-kompiled --spec-module FRESH-VACUITY
```

The claim parses and executes. Raw exit is 1 with `WarnStuckClaimState`; the
terminal residual contains:

```text
"answer" |-> str(iCons(65,.IntSeq))
```

which is `"A"`, while the mutation requires code 97 (`"a"`). The backend
reports that the terminal configuration cannot be rewritten further. This is
the expected unmet result obligation, not a parser error, timeout, or unrelated
crash.

The first reviewer postcheck looked for an unwrapped diagnostic phrase and
misreported the already valid raw run; the corrected bounded postcheck and raw
proof log are both preserved. Only the actual K residual is counted.

Evidence:

- `evidence/fresh-vacuity.k`
- `evidence/stage6_fresh_vacuity_raw.log`
- `evidence/stage6_fresh_vacuity.log` — corrected postcheck exit 0,
  `FRESH_NON_VACUITY EXPECTED_FAILURE_PASS`
- excluded wrapper-check log:
  `evidence/stage6_fresh_vacuity_check_error.log`

Stage 6 passes.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the fixed supplied semantics and K implementation, for every
finite `INPUT:IntSeq`, terminating execution of the exact translated
`solve` binding produces:

- `str(toggleAcc(INPUT,.IntSeq))` if the supplied ASCII character model finds
  at least one alphabetic code; otherwise
- `str(revIS(INPUT))`.

The proof additionally establishes the exact unbounded loop summary for
arbitrary remaining input and accumulators. It is not a finite unrolling.
Because this is reachability logic, the advertised theorem is partial
correctness, not a separate termination theorem.

### Trust ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| Trusted `py2mpy.py` | Python-AST to constructor identity | Real-program pinning | Byte-identical regeneration plus macro-expanded KAST identity. |
| Supplied `MPY` operational semantics | Binding, ordering, state, calls/returns, character model | Both claims | Integrity-checked fixed source; used rules reviewed; fresh concrete executions. This is the intended formal trust boundary. |
| K v7.1.293 frontend/Haskell backend | Compilation, symbolic execution, circularity, `#Top` | Formal result | Fresh definitions, isolated loop, complete target proof, independent lemma, and rejected mutations. |
| Built-in K integer/Boolean/string/map/list/equality hooks | Ordinary mathematical operations and constructor reasoning | Fixed and proof-local functions | Constructor lemma is independently checked; equations use straightforward finite structural recursion. |
| Proof-local functions | Result summary | Both claims | No opacity; complete guarded equations and a machine-checked loop-to-summary connection. |
| Natural-language bridge on modeled ASCII | “letter”, case swap, reverse | Intent adequacy | Direct equation inspection, ground K claims, concrete execution, and differential tests. |
| Supplied Unicode gap | Transfer from modeled strings/case rules to full CPython `str` | Full source-contract adequacy only | Explicit candidate trust ledger; fresh `"é1"` divergence witness; candidate Python agrees with CPython/canonical on tested Unicode and directly delegates classification/case mapping to CPython. |

The 24 supplied opaque symbols have no dependents in these claims. There is no
proof-local opaque value, empirical oracle in a rewrite rule, or informal
program-body summary.

### Empirical support and exclusions

The 34,716-case differential, concrete K examples, ground substitutions, and
mutation probes support only their recorded scopes. They do not replace the K
reachability proof.

Non-string arguments are outside the docstring's string contract. Full Unicode
classification/case mapping is outside the supplied formal model but not
outside `solution.py`; this is the documented supplied-model exception.
Termination is not a separately proved liveness theorem.

### Gate and benchmark decision

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **PASS relative to every value/behavior the fixed
  model represents**, with the material supplied Unicode boundary documented.
- Gate C, trust/evidence auditability: **PASS**.

The campaign-specific mapping nevertheless requires `CONCERNS / LEGIT` for
this documented supplied-model representation gap. It is not `FAIL`: the
candidate did not narrow the theorem, the theorem is unbounded over all finite
model strings, the boundary is explicit with a concrete witness, and the
submitted Python program is faithful on the CPython side of the gap. It is not
an unconditional `PASS` because the formal theorem cannot itself establish
full Unicode behavior under the fixed ASCII-only semantics.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
