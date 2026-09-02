# Independent adversarial audit: 128-prod-signs

The candidate implementation and its generated semantics appear faithful on the
intended domain, and every submitted K claim reconstructs successfully.
Nevertheless, the candidate does **not** contain a K reachability theorem for
the required result on an arbitrary nonempty input. It proves initialization,
one loop iteration at a time, loop exit, and three fixed examples, but never
states or closes the universal nonempty entry-to-return claim. Under the stated
decision boundary this is a missing/non-result-constraining proof, not merely a
documentation concern.

All candidate prose, logs, traces, and prebuilt definitions were treated as
untrusted. All execution below used fresh definitions under
`/tmp/audit-work/128-prod-signs`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`.
- The candidate's required JSON, generation records, prompt, translator,
  Python/MPY program, and three K source files are regular files. No required
  artifact is missing, mistyped, or symlinked.
- The structured trace is present as one regular JSONL file and parses as 135
  JSON records with no malformed line.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`b909f864...6aca7`), and `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (`406485ea...db16`).
- Additional top-level candidate entries are `prove.sh`, `__pycache__/`,
  `semantic-kompiled/`, `verification-kompiled/`, and `codex-trace/`. The
  compiled directories and Python cache were ignored and never copied into the
  clean proof path. `prove.sh` and the trace are supplementary records, not
  proof sources.

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
complete JSONL trace were read only as claims. They report an exit-zero
generation and prior `#Top`, but none was used to establish the result.

Evidence:

- [01_provenance.log](/audit-output/evidence/01_provenance.log)
- [01_untrusted_generation_summary.log](/audit-output/evidence/01_untrusted_generation_summary.log)
- [01_toolchain.log](/audit-output/evidence/01_toolchain.log)

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For a finite list of integers:

- return `None` for the empty list;
- otherwise return the sum of all absolute values multiplied by the product of
  each element's sign, where negative, zero, and positive signs are `-1`, `0`,
  and `1`.

Thus any nonempty list containing zero returns zero. With no zero, the magnitude
sum is positive and its sign is determined by the parity of negative elements.
This is the behavior of `/reference/canonical.py`.

`/candidate/solution.py` implements the same recurrence. `total` accumulates
`abs(x)`: the negative branch subtracts `x`, while the nonnegative branch adds
`x`. `sign` starts at one, flips on every negative, and becomes zero on a zero.
The explicit empty check returns `None`. The signature remains
`prod_signs(arr)`.

### Translation identity

The trusted translator was copied from `/reference`, not from the candidate,
and run as:

```text
python3 py2mpy.py solution.py > regenerated_solution.mpy
cmp -s regenerated_solution.mpy solution.mpy
```

Both MPY files have SHA-256
`f89ded5d120c6c7181dbb71b22dbf7bb07017c9989de832e6b7c9a820ff683d0`;
`cmp` exited zero.

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) independently
loads `/reference/canonical.py` and the scratch copy of `solution.py`. It checks:

- the three documented behaviors and branch boundaries `-1`, `0`, and `1`;
- empty, singleton, zero-position, even/odd-negative, and 100-digit integer
  cases;
- all 19,608 lists of lengths 0 through 5 over values `-3..3`;
- 500 deterministic random lists of lengths 0 through 64 over
  `[-10^12, 10^12]`.

The 20,121 comparisons had zero mismatches. This is finite fidelity evidence,
not a substitute for a universal K theorem.

Evidence:

- [02_translation_identity.log](/audit-output/evidence/02_translation_identity.log)
- [02_differential.log](/audit-output/evidence/02_differential.log)

## 3. Clean proof reconstruction

K version `v7.1.293` was independently available. `kup` was absent, but the
installed `kompile`, `krun`, and `kprove` binaries all ran, so the approved Kit
workflow remains on its live-verification path.

Only these source artifacts were copied into scratch: `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, the trusted
translator, trusted prompt, and trusted canonical implementation. No candidate
compiled definition or cache was copied.

### Fresh concrete definition

Exact build command:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-kompiled
```

It exited zero. The fresh LLVM definition then executed the actual submitted
`solution.mpy` on 12 normal and boundary lists: empty, documented examples,
single negative/zero/positive values, even and odd negative counts, zero in
multiple positions, and a 32-bit boundary pair. Every `krun` exited zero and
the K result matched both Python implementations. In particular:

```text
[]                              -> none
[1,2,2,-4]                      -> -9
[0,1]                           -> 0
[-1,-2,-3]                      -> -6
[2147483647,-2147483648]        -> -4294967295
```

Evidence:

- [03_llvm_kompile.log](/audit-output/evidence/03_llvm_kompile.log)
- [concrete_semantics_test.py](/audit-output/evidence/concrete_semantics_test.py)
- [03_concrete_semantics.log](/audit-output/evidence/03_concrete_semantics.log)

### Fresh proof definition and positive claims

Exact proof build and aggregate proof commands:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition audit-verification-kompiled

kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Both exited zero, and `kprove` printed `#Top`.

For independent claim execution, an audit copy of `spec.k` was given labels
only; claim bodies were unchanged. Each of these nine selectors independently
exited zero and printed `#Top`:

```text
SPEC-LABELED.empty
SPEC-LABELED.init
SPEC-LABELED.step-neg
SPEC-LABELED.step-pos
SPEC-LABELED.step-zero
SPEC-LABELED.exit
SPEC-LABELED.example-main
SPEC-LABELED.example-zero
SPEC-LABELED.example-neg3
```

Evidence:

- [03_haskell_kompile.log](/audit-output/evidence/03_haskell_kompile.log)
- [03_kprove_all.log](/audit-output/evidence/03_kprove_all.log)
- Individual `03_kprove_*.log` files in
  [evidence/](/audit-output/evidence/)

The reconstructed `#Top` results are genuine results for the claims that were
submitted. They do not establish that those claims collectively state the
requested theorem.

## 4. Adequacy and real-program pinning

### Program identity

The proof uses `<k> boot(solutionProgram) ...</k>`, where the three nullary
functions in `/candidate/verification.k` expand as:

```text
solutionProgram -> Module(FuncDef("prod_signs", Params("arr"), solutionBody))
solutionBody    -> the full translated function body
solutionLoopBody -> the exact translated loop body
```

Direct comparison maps every constructor in `/candidate/solution.mpy` to these
expansions. The independent
[program-pin.k](/audit-output/evidence/program-pin.k) uses the complete raw MPY
constructor term as the destination of a `boot(solutionProgram)` claim; it
normalizes to the same term and prints `#Top`. The fresh Haskell definition also
produced byte-identical final configurations when run from raw `solution.mpy`
and from the parsed `solutionProgram` symbol on empty, documented, and mixed
sign/zero inputs.

Evidence:

- [04_program_pin_claim_boot.log](/audit-output/evidence/04_program_pin_claim_boot.log)
- [04_program_pin_runtime_success.log](/audit-output/evidence/04_program_pin_runtime_success.log)

The embedding is therefore a faithful definitional copy of the real submitted
MPY program; it is not a substituted algorithm.

### Plain-language meaning and satisfiability of every claim

| Claim | Preconditions | Postcondition actually proved |
|---|---|---|
| `spec.k:7` | Empty input and all initial cells | The real program terminates with `result(none)` |
| `spec.k:16` | Arbitrary nonempty input `X, IS` and all initial cells | Execution reaches the first loop head with `total=0`, `sign=1`, `x=0` |
| `spec.k:32` | A loop head whose next value `X` is negative | Exactly one real iteration advances the tail, adds `magnitude(X)`, and multiplies the tracked sign by `integerSign(X)` |
| `spec.k:47` | Same, with `X > 0` | The analogous one-iteration positive transition |
| `spec.k:62` | Same, with `X == 0` | The analogous one-iteration zero transition |
| `spec.k:77` | Empty loop tail with arbitrary `total=T`, `sign=S` | The real trailing return produces exactly `T * S` |
| `spec.k:86` | Fixed input `[1,2,2,-4]` | Final locals are fixed and the result is `contract(...) = -9` |
| `spec.k:98` | Fixed input `[0,1]` | Final locals are fixed and the result is `contract(...) = 0` |
| `spec.k:110` | Fixed input `[-1,-2,-3]` | Final locals are fixed and the result is `contract(...) = -6` |

Every precondition is satisfiable. Concrete states for every claim, including
`X=-1`, `X=1`, and `X=0` witnesses for the three guarded steps, are recorded in
[claim_witnesses.md](/audit-output/evidence/claim_witnesses.md). Substitution
agrees with K, the candidate Python, and trusted Python: for example,
`[1,2,2,-4]` gives `9 * -1 = -9`, `[0,1]` gives `1 * 0 = 0`, and
`[-1,-2,-3]` gives `6 * -1 = -6`.

### Material adequacy failure

There is no claim with the following essential scope:

```text
for every IS:Ints,
boot(solutionProgram) with input(IS)
  => termination with result(contract(IS))
```

The only arbitrary nonempty entry claim, `spec.k:16`, stops at loop
initialization and has no returned-value postcondition. The three symbolic loop
claims cover one iteration each. The exit claim returns arbitrary `T*S`, but no
reachability claim connects the initialized `T=0,S=1`, an arbitrary-length
loop, and `contract(originalInput)`. The original list remains in the
environment, but it is not used in a proved loop invariant or final
postcondition.

These local theorems are plausible ingredients for a separate induction.
`kprove #Top` over them is not a proof of that unstated induction or of its
entry-to-exit composition.

To confirm the gap dynamically, the auditor added the natural universal claim
to a copy containing **all nine original claims**. The artifact parsed and
reached the prover, but exited 1 with `WarnStuckClaimState`; even the symbolic
one-element negative branch retained an unmet equality involving
`integerSign(_I)`. This diagnostic does not allege a false semantic rule. It
shows that the missing intended claim is neither present nor incidentally
closed by the submitted auxiliary claims.

Evidence:

- [spec-with-entry.k](/audit-output/evidence/spec-with-entry.k)
- [04_original_plus_intended_entry.log](/audit-output/evidence/04_original_plus_intended_entry.log)

This is the decisive legitimacy failure.

## 5. Rule-by-rule static soundness review

There are no candidate helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`. Candidate compiled outputs were excluded.

### Complete local declaration inventory

`semantic.k` declares:

- `Pgm`: `Module(Stmts)`;
- list sorts `Stmts`, `Exprs`, `CmpOps`, `Strings`, and `Ints`;
- `Params(Strings)`;
- statements `FuncDef`, `Return`, `Assign`, `If`, and `For`;
- expressions `Name`, `Int`, `ListExpr`, `BinOp`, `UnaryOp`, `Compare`, and
  `NoneVal`;
- `CmpOp`;
- values `Int`, `Bool`, `none`, and `listVal(Ints)`;
- external input `input(Ints)`;
- internal `Function` and `Result` sorts;
- internal K items `boot`, `exec`, `start`, `eval`, `store`, `bind`, `branch`,
  `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `forStart`, `loop`, and
  `returnK`.

The configuration has exactly the needed cells: `<k>`, `<input>`,
`<function>`, `<env>`, and `<result>`. There is no heap, allocation, output,
exception, or call-stack syntax because the translated program uses none.

`verification.k` adds five `[function,total]` mathematical symbols:
`magnitude`, `integerSign`, `sumMagnitudes`, `productSigns`, and `contract`.
It also adds the fully defined `[function]` nullary constants
`solutionLoopBody`, `solutionBody`, and `solutionProgram`.

There are no local `[simplification]`, `[functional]`, `[concrete]`, priority,
`owise`, `anywhere`, macro, or opaque declarations. No rule is an operational
bridge or oracle that replaces program-defined execution.

### All 36 semantic rules

| Rule location | Rule and decision |
|---|---|
| `semantic.k:71` | `boot(Module(SS))` schedules module statements then `start`; faithful. |
| `semantic.k:73` | Empty statement execution becomes `.K`; faithful. |
| `semantic.k:74` | A statement head executes before its tail; faithful sequential order. |
| `semantic.k:76` | The exact `prod_signs` definition is stored; faithful for the only used function. |
| `semantic.k:79` | `start` binds the single input list and schedules the stored body; faithful. |
| `semantic.k:84` | Assignment evaluates its RHS before storing; faithful. |
| `semantic.k:85` | Store updates an existing binding; faithful. |
| `semantic.k:87` | Store inserts an absent binding; the absence guard makes it disjoint from line 85. |
| `semantic.k:91` | Loop bind updates an existing target; faithful. |
| `semantic.k:93` | Loop bind inserts an absent target; disjoint by the absence guard. |
| `semantic.k:97` | `If` evaluates its condition before branching; faithful. |
| `semantic.k:98` | True selects the then-list; faithful. |
| `semantic.k:99` | False selects the else-list; faithful and disjoint from line 98. |
| `semantic.k:101` | `For(Name(X),E,BODY)` evaluates its iterable first; faithful. |
| `semantic.k:102` | A list value initializes the loop; faithful. |
| `semantic.k:103` | Empty integer list exits the loop; faithful. |
| `semantic.k:104` | Nonempty loop binds the head, executes the body, then recurs on the tail; faithful iteration order and state. |
| `semantic.k:106` | `Return(E)` evaluates `E` before returning; faithful. |
| `semantic.k:107` | A returned value discards the remaining function continuation and sets the result; faithful for both actual top-level returns. There are no calls or cleanup constructs whose frames could be lost. |
| `semantic.k:110` | Integer literals evaluate to the same unbounded K integer; faithful. |
| `semantic.k:111` | `NoneVal` evaluates to `none`; faithful. |
| `semantic.k:112` | The only used list literal, `[]`, evaluates to the empty list value; faithful. |
| `semantic.k:113` | Names read their current map binding; faithful. |
| `semantic.k:116` | Unary operation evaluates its operand before dispatch; faithful for unary minus. |
| `semantic.k:117` | Binary operation evaluates the left operand first; matches Python order. |
| `semantic.k:118` | The saved left value is combined only after evaluating the right operand; faithful. |
| `semantic.k:120` | Integer addition uses K's unbounded integer addition; faithful. |
| `semantic.k:121` | Binary integer subtraction uses `I1 - I2`; faithful. |
| `semantic.k:122` | Integer multiplication uses `I1 * I2`; faithful. |
| `semantic.k:123` | Unary minus computes `0 - I`; faithful. Its overlap with line 121 when the saved left operand is zero has the same RHS, so it is consistent. |
| `semantic.k:125` | Comparison evaluates its left expression first; faithful. |
| `semantic.k:126` | The single used comparator then evaluates its RHS while saving the left value; faithful. Chained comparisons are intentionally unmodeled and unused. |
| `semantic.k:129` | Integer `<` compares saved left against evaluated right; faithful. |
| `semantic.k:130` | Integer `==` is faithful. |
| `semantic.k:131` | Empty-list equality returns true when the saved left is also empty; faithful. |
| `semantic.k:132` | Comparing a nonempty saved left list with the evaluated empty RHS returns false; this is exactly the used `arr == []` direction. |

All statement/expression constructors in `solution.mpy` map to the syntax and
rules above. The model intentionally omits nonempty list literals, general list
equality, chained comparison, calls, exceptions, and unrelated Python
constructs. None is used by the submitted program, so this minimal coverage is
acceptable under `GENERATED_SEMANTICS`.

The function body executes through ordinary semantic rules. State updates,
loop order, guards, return control, and all result-affecting operations are
modeled rather than summarized.

### All 14 verification rules

| Rule location | Rule and decision |
|---|---|
| `verification.k:13` | Negative magnitude is `0-I`; mathematically true. |
| `verification.k:14` | Nonnegative magnitude is `I`; disjoint from line 13 and complete with it. |
| `verification.k:16` | Negative integer sign is `-1`; true. |
| `verification.k:17` | Zero sign is `0`; true. |
| `verification.k:18` | Positive sign is `1`; all three sign cases are disjoint and complete. |
| `verification.k:20` | Empty magnitude sum is zero; true base case. |
| `verification.k:21` | Nonempty magnitude sum recurses on the strict tail; true and terminating. |
| `verification.k:23` | Empty sign product is one; true multiplicative identity. |
| `verification.k:24` | Nonempty sign product recurses on the strict tail; true and terminating. |
| `verification.k:26` | Empty contract returns `none`; matches the prompt. |
| `verification.k:27-28` | Nonempty contract is magnitude sum times sign product; matches the prompt and is disjoint from line 26. |
| `verification.k:33-40` | `solutionLoopBody` expands to the translated loop body exactly. |
| `verification.k:43-51` | `solutionBody` expands to the translated function body exactly. |
| `verification.k:54-56` | `solutionProgram` expands to the translated module exactly. |

The five total functions have complete, non-overlapping cases and structural
descent where recursive. The three program constants are nullary and each has
one complete defining equation. No local equation or operational rule was
found unsound, so this review makes no unsupported unsoundness allegation and
needs no false-rule witness. The defect is the absent theorem, not a false rule.

Inventory evidence:

- [05_source_inventory.log](/audit-output/evidence/05_source_inventory.log)

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. The auditor created a fresh
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) that keeps the
documented input `[1,2,2,-4]` and all final locals but changes the required
result from `-9` to `0`.

The satisfiable starting state is the ordinary initial configuration with that
input. Both Python implementations and the fresh K semantics return `-9`, so
the mutation is demonstrably false.

Build-only command:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

It exited zero, establishing that the mutation parses and builds. The same
command without `--dry-run` exited 1 with `WarnStuckClaimState`. Its residual
configuration is fully terminated and contains:

```text
<result> result ( -9 ) </result>
```

against the mutated `result(0)` destination. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash.

Evidence:

- [06_vacuity_dry_run.log](/audit-output/evidence/06_vacuity_dry_run.log)
- [06_vacuity_proof.log](/audit-output/evidence/06_vacuity_proof.log)

The submitted concrete result claims are non-vacuous. This does not repair the
absence of a universal nonempty result claim.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted generated semantics and K built-ins, the reconstructed
proof establishes exactly:

1. correct execution for the empty input;
2. correct initialization for every nonempty integer list;
3. correct execution of one negative, positive, or zero loop iteration from an
   arbitrary matching loop state;
4. correct return of `T*S` once an empty loop tail is already reached; and
5. complete correct executions for three fixed nonempty inputs.

It does **not** establish a reachability claim from an arbitrary nonempty entry
configuration to `result(contract(originalInput))`.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K frontend, LLVM/Haskell backends, and reachability engine | Build, execution, and `#Top` checking for every claim | Standard unavoidable tool trust; fresh builds avoid candidate caches. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, and list machinery | Unbounded arithmetic, comparisons, maps, and collection constructors | Acceptable low-level primitive boundary. K unbounded integers match Python integers on the intended arithmetic domain. |
| Trusted `/reference/py2mpy.py` | Bridge from `solution.py` to `solution.mpy` | Explicitly trusted input; fresh regeneration is byte-identical. |
| Candidate generated semantics | Defines the modeled MiniPy subset | No external semantics was allowed in this mode. All local rules were audited and concretely cross-checked; no oracle or answer-smuggling rule exists. Coverage is deliberately limited to used constructs. |
| `solutionProgram`/body constants | Pin proof claims to the submitted translated program | Fully defined, syntactically exact, machine-normalized to the raw constructor term, and concretely runtime-equivalent in tested cases. Acceptable. |
| `magnitude`, `integerSign`, list folds, and `contract` | Formal mathematical result definition | Exhaustive truthful equations with no opacity. Acceptable definitions, but the missing universal entry theorem never connects them to all executions. |
| Python/K intent bridge | Relates the generated subset semantics and loop algorithm to the natural-language task | Supported by static construct mapping, 12 K/Python boundary comparisons, and 20,121 Python differential comparisons. The testing is finite and cannot replace the missing K claim. |
| Candidate logs, trace, prior `#Top`, and prebuilt definitions | Historical generation evidence | Assigned no trust and excluded from reconstruction. |

There are no proof-local opaque symbols, unconstrained result values, priority
shortcuts, simplification axioms, or empirical oracles. Termination beyond the
finite-list intended domain and unused Python constructs are outside the
theorem/model.

### Decision

The implementation is strongly supported as correct, the generated semantics
is sound for the submitted program, and every claim the candidate actually
wrote is legitimate. But the required partial-correctness theorem for arbitrary
nonempty input is missing. The only arbitrary entry claim stops before the
loop, and no proved invariant or summary connects it to the intended returned
value. Per the explicit decision boundary, a missing or non-result-constraining
proof is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
