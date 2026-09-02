# Independent adversarial audit: 137-compare-one

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted translated program under the fixed supplied MPY semantics. The
candidate did not alter the supplied semantics, narrow the theorem to examples
or bounded sizes, intercept program execution, or leave the return
unconstrained.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the fixed
supplied model has a documented representation/behavior gap for numeric strings
such as exponent notation and uses opaque symbolic floating-point primitives.
The theorem covers all values represented by that model and the submitted
Python program behaves correctly in CPython at the exhibited gap. This meets
campaign amendment v2 exception 1; it is not candidate-caused narrowing.

## 1. Input and provenance integrity

The declared record layout is `pipeline-v3`, the semantics mode is
`SUPPLIED_SEMANTICS`, and the trusted `/reference/reference-semantics` mount is
present. There is no rendered-mode contradiction and no infrastructure-stop
condition.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required generation-evidence
records, the full 285-line structured JSONL trace, and the generation prompt,
output, and final report. Generation records were treated only as untrusted
claims.

The independent integrity script and complete output are
[stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1_integrity.log](evidence/stage1_integrity.log). It found:

- the campaign block in `/audit-input.json` equals
  `/audit-campaign-lock.json`, and the lock's SHA-256 equals the recorded
  `053ed73c...dadd01`;
- every required pipeline-v3 record exists, is readable, has the expected
  ordinary file/directory type, and every recorded per-file SHA-256 checked by
  the script matches;
- the only trace file has the recorded SHA-256, all 285 lines parse as JSON,
  and its inventory exactly matches `/generation-result.json`;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts and have their recorded hashes;
- a portable reviewer digest covered all 824 candidate entries, and no
  candidate entry is a symlink;
- candidate and trusted supplied-semantics trees each contain the same 25
  descendants (26 including the root), with identical types and file bytes.
  Their independent normalized tree hashes are both
  `759a6317...20a682`.

Thus no missing, additional, changed, mistyped, or symlinked supplied-semantics
entry was found. Candidate-built `runtime-kompiled/`,
`verification-kompiled/`, caches, logs, and KORE files were not trusted or used
for reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The docstring in `/reference/prompt.py` requires `compare_one(a, b)` for
integers, floats, or strings representing real numbers. A string may use `.`
or `,` as its decimal point. The function must return the larger original
argument in its original type and return `None` when the represented values are
equal. Its four examples cover mixed int/float, int/comma-string, two strings,
and string/int equality.

The submitted `/candidate/solution.py`:

1. converts each string after replacing every comma with a dot;
2. leaves non-string integers and floats uncoerced;
3. returns `a` if its normalized value is greater, otherwise returns `b` if
   the reverse comparison is greater, otherwise returns `None`.

For ordinary real-number inputs, trichotomy makes the third case equality. The
function returns the original argument, not a converted float. NaN, invalid
numeric strings, exotic subclasses, and other unspecified classes are
docstring-underdetermined; the implementation's handling of those cases is
defensible and is not used to claim a defect.

### Trusted translation

I copied only `solution.py`, the trusted translator, and the trusted semantics
to `/tmp/audit-work/reconstruction`. This command:

```bash
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.mpy
cmp /tmp/audit-work/reconstruction/solution.mpy \
  /tmp/audit-work/reconstruction/submitted-solution.mpy
```

exited 0. The regenerated and submitted MPY files both hash to
`59992d3e...a105c`; see
[translator_identity.log](evidence/translator_identity.log).

### Independent differential

[independent_differential.py](evidence/independent_differential.py) imports the
trusted canonical function and the copied generated function by absolute path.
It uses an independently written docstring oracle, the four examples, eleven
explicit branch/boundary cases, a 16-by-16 Cartesian sample crossing every
`int`/`float`/`str` pairing, and 600 generated cases with seed
`13720260730`. The exact command was:

```bash
python3 /audit-output/evidence/independent_differential.py
```

It exited 0 over 871 contract cases with zero generated-program mismatches.
There were six canonical divergences, all caused by the canonical witness
coercing large integers to float (for example,
`9007199254740993` versus `9007199254740992.0`). The candidate correctly
returns the larger integer under the docstring, so those canonical differences
are not defects. Empty/invalid strings, NaN, infinity, Unicode digits, and
overflowing exponent strings were separately recorded as edge observations,
not silently treated as contract failures. Full inputs and results are in
[independent_differential.log](evidence/independent_differential.log).

## 3. Clean proof reconstruction

I did not copy either candidate kompiled directory. The proof definition was
built afresh from `/candidate/verification.k` plus the independently copied,
trusted semantics:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0 under K `v7.1.293`; see
[clean_kompile.log](evidence/clean_kompile.log). The warnings are unused
variables in fixed `str.k`, not errors or proof extensions.

I then ran each of the nine target claims separately:

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.<label>
```

The labels were `int-int`, `int-float`, `float-int`, `float-float`, `int-str`,
`str-int`, `float-str`, `str-float`, and `str-str`. Every command exited 0 and
printed exactly one `#Top`. The exact runner is
[run_positive_claims.sh](evidence/run_positive_claims.sh), the aggregate status
is [positive-claims-summary.log](evidence/positive-claims-summary.log), and the
nine complete bounded logs are `evidence/positive-<label>.log`.

The concrete definition was also built afresh:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun k_concrete_smoke.mpy --definition runtime-kompiled
```

Both commands exited 0. The independently authored smoke program covers all
four examples, all three result outcomes, and representative type pairings. It
ended in `.K`, `NoExc`, and exit code 0. See
[clean_llvm_kompile.log](evidence/clean_llvm_kompile.log),
[k_concrete_smoke.py](evidence/k_concrete_smoke.py), and
[clean_krun_smoke.log](evidence/clean_krun_smoke.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

The nine entry claims have no `requires` clause. Their effective precondition is
the complete standard initial MPY configuration plus one of the nine Cartesian
sort pairings:

- each argument is any K `Int`, any K `Float`, or any `str(IntSeq)`;
- the global scope is empty with the supplied builtins as its parent;
- the heap, stack, return state, and exception state are initially empty/normal.

Each claim loads `solutionModule()`, looks up and calls `compare_one`, and
requires the final `<k>` result to equal:

```text
numericValue(I:Int)   = I
numericValue(F:Float) = F
numericValue(str(C))  = decStrToF(replaceC(C, ',', '.'))

expectedCompare(A,B) =
  A     if numericValue(A) > numericValue(B)
  B     if not(A>B) and numericValue(B) > numericValue(A)
  noneV otherwise
```

The environment, heap, allocation counters, stack, return state, exception
state, and exit code must be restored exactly. Only the final scope map is
existential, because loading the function intentionally adds the global
binding. There are no loops or helper-function claims.

### Satisfiability and result constraint

The standard initial configuration with `A=1`, `B=2` satisfies
`SPEC.int-int`. A fresh ground instance proved `#Top` and exited 0, and both
Python implementations returned `2`; see
[spec-ground-witness.k](evidence/spec-ground-witness.k),
[ground_kprove.log](evidence/ground_kprove.log), and
[ground_python.log](evidence/ground_python.log).

The result is not a free variable, tautology, or one-way implication:
`expectedCompare` fixes it to one of the two original arguments or `noneV`
under exhaustive, disjoint guards.

### Mechanical program identity

There are two independent links:

1. trusted regeneration established byte identity between `solution.py` and
   submitted `solution.mpy`;
2. under the fresh proof definition, I executed regenerated `solution.mpy` and
   independently parsed/executed `solutionModule()`. Their complete final KORE
   configurations are byte-identical and share SHA-256
   `5fe0e823...a4ccc`.

The exact commands and hashes are in
[program_term_identity.log](evidence/program_term_identity.log); the two KORE
artifacts are
[direct-solution-final.kore](evidence/direct-solution-final.kore) and
[named-solution-final.kore](evidence/named-solution-final.kore).

A separate body-sensitivity definition materially changes the constructor term
actually loaded by the claim: the first greater-than branch returns `b` instead
of `a`. Its definition compiled successfully, and its claim for `(2,1) => 2`
failed with `WarnStuckClaimState`, exit 1, and actual residual `1 ~> .K`. See
[verification-body-mutation.k](evidence/verification-body-mutation.k),
[body_mutation_kompile.log](evidence/body_mutation_kompile.log), and
[body_sensitivity_kprove.log](evidence/body_sensitivity_kprove.log).

These checks pin the theorem to the submitted function binding and body, not
merely to an external source filename.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.tsv](evidence/rule_inventory.tsv), generated by
[make_rule_inventory.py](evidence/make_rule_inventory.py), inventories every
declaration block in the supplied `semantics.k` tree,
`verification.k`, and `spec.k`, with source hash, line, kind, attributes,
full normalized declaration, reachability disposition, and assessment.

The inventory has 1,033 entries:

- 247 syntax declarations;
- 771 ordinary rules;
- 5 contexts;
- 1 configuration;
- 9 claims.

Attribute-bearing entry counts are 164 `function`, 114 `total`, 27 `symbol`,
24 `no-evaluators`, 50 `concrete`, 30 `priority`, 28 `owise`, 4 `macro`,
2 `strict`, and 1 `seqstrict`. There are no `functional` declarations and no
`simplification` rules. Non-task supplied rules are still enumerated and
classified as unreachable by this constructor term; no such sort-disjoint
rule can rewrite a term on this execution path. Compiler-reported
non-exhaustive fixed helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`) are also off path and do not contribute to claim
closure.

I do not label any rule unsound on the intended task domain. Accordingly there
is no unsupported unsoundness allegation requiring a false-conclusion witness.
The narrower, evidenced supplied-model gaps are recorded below.

### Mapping the program to fixed semantics

| Program construct | Declaration/evaluation rules used |
|---|---|
| `Module`, `FuncDef`, statement sequence | `syntax.k`; `core.k` `#loadAll` and sequence rules; `functions.k` plain `FuncDef` rule |
| names and builtins | `core.k` `Name -> #look`, parent lookup, and `builtinsScope` |
| calls and parameters | `call.k` callee-first rule; `core.k` left-to-right `#evalArgs`; `call.k` plain `closureVal` frame rule; `functions.k` `#bindP` |
| `isinstance(x, str)` | ordinary lookup of `str` and `isinstance`; `builtins.k` `isStrV` equations |
| assignment | `syntax.k` RHS strictness; `controls.k` plain-name assignment |
| `x.replace(",", ".")` | `call.k` cooled `Attribute` and bound-method dispatch; `methods.k` one-character `replaceC` recursion |
| `float(string)` | type-object dispatch through `call.k`; `float.k` `applyBuiltin("float", str(...)) -> decStrToF(...)` |
| `>` comparisons | `operators.k` comparison contexts and dispatch; `int.k` int/int `>`; `float.k` `gtF`, `ltFI`, and `ltIF` cases |
| `if` | strict condition evaluation and `controls.k` `truthy`/`#branch` rules |
| `return` / fallthrough `None` | `core.k` `NoneVal`; `functions.k` `Return`, `#endcall`, and `#pop`, restoring control cells |

This path preserves callee and argument evaluation order, lexical lookup,
parameter binding, both conversions, both conditional comparisons, abrupt
return, frame popping, heap, counters, stack, exception state, and exit code.
No candidate priority rule preempts it.

### Proof-local extensions

`verification.k` adds only three function declarations and seven equations:

- `solutionModule()` is a nullary, total syntax abbreviation with one equation.
  Its exact constructor identity is mechanically checked above. It neither
  intercepts nor summarizes execution.
- `numericValue` is postcondition-only, deliberately not total over all `Val`.
  Its three disjoint equations are identity on `Int`/`Float` and exactly the
  fixed `replaceC` then `decStrToF` chain on `str(IntSeq)`.
- `expectedCompare` is postcondition-only, deliberately not total over
  unrelated `Val` constructors. If `P` is the forward `>` result and `Q` the
  reverse result, its guards are `P`, `not P and Q`, and
  `not P and not Q`: exhaustive and pairwise disjoint, with results `A`, `B`,
  and `noneV`.

There are no proof-local operational bridges, call intercepts, priorities,
opaque symbols, simplifications, algebraic lemmas, or circularities. The
program body executes under the fixed rules. Sharing fixed primitive terms
between execution and the postcondition makes the theorem parametric in those
primitives; it does not fabricate a result or replace program-defined code.

### Fixed opaque boundaries and overlap/totality

The task-relevant opaque fixed symbols are:

- `gtF(Float,Float)` for float/float `>`;
- `ltFI(Float,Int)` and `ltIF(Int,Float)` for exact mixed ordering;
- `decStrToF(IntSeq)` for string-to-float conversion;
- the concrete `intToF`/K floating hooks used inside the fixed decimal parser.

Each has one fixed dispatch path for the applicable constructor sorts, so no
proof-local overlap is introduced. Symbolic proof keeps them uninterpreted;
LLVM supplies their concrete equations. Because program execution and
`expectedCompare` use the same values and comparison atoms, the K reachability
result is sound for every interpretation of those atoms. The separate claim
that they denote CPython real-number parsing and ordering is a trust/adequacy
bridge, not something `#Top` proves.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` and wrote
[spec-fresh-vacuity.k](evidence/spec-fresh-vacuity.k). It executes the unchanged
real `solutionModule()` on the satisfying input `(1,2)` but changes the
result-constraining destination from the correct `2` to false value `1`.

First:

```bash
kprove /audit-output/evidence/spec-fresh-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY --dry-run
```

exited 0, establishing that the mutated artifact parsed and built; see
[fresh_vacuity_dry_run.log](evidence/fresh_vacuity_dry_run.log).

Then the same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. The residual has `2 ~> .K`, while the destination
requires `1`; see
[fresh_vacuity_kprove.log](evidence/fresh_vacuity_kprove.log). This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

## 7. Proven versus assumed accounting

### What is proved

For every pair in the complete modeled Cartesian product
`(Int | Float | str(IntSeq))²`, starting from the standard initial MPY state,
if the submitted translated call terminates, it:

- returns the original `A` on the forward modeled greater-than branch;
- otherwise returns original `B` on the reverse modeled greater-than branch;
- otherwise returns `noneV`;
- restores environment, heap, allocation counters, call stack, return state,
  exception state, and exit code as specified.

This is a partial-correctness theorem. It is not a separate termination theorem
and does not prove the CPython implementation of floating point from first
principles.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Supplied module loading, scope, call, control, and K builtins | All nine claims; binding, evaluation order, state, and return control | Acceptable fixed operational model; exact body executes, all state-bearing rules are on path, concrete smoke passes |
| `gtF`, `ltFI`, `ltIF` and K float hooks | Branches/results of every claim involving `Float` or converted strings | Acceptable but explicit low-level trust boundary; theorem is interpretation-parametric, fixed concrete equations and independent CPython differential support adequacy |
| `replaceC` | All string claims | Defined structural recursion; exact comma-to-dot operation, no opacity |
| `decStrToF` | All five claims with at least one string | Fixed opaque parser; structurally linked to execution, but its concrete decimal subset is not CPython-complete |
| `solution.py -> solution.mpy` translator | Real-program identity | Trusted mounted translator; byte-identical regeneration |
| Constructor abbreviation `solutionModule()` | Selects all executed code | Candidate-defined but mechanically identical to regenerated program execution; material body mutation rejected |
| Docstring interpretation over ordinary real numbers | Meaning of “larger” and equality | Ordinary trichotomy plus 871-case independent evidence; NaN/nonfinite/invalid/exotic cases are underdetermined and not used as failures |

### Supplied-model representation gap

The candidate explicitly records the decimal-parser and ASCII boundaries in
its trust ledger and excluded-behavior section
(`/candidate/PROOF.md`, especially lines 263-270 and 304-328), including the
exponent witness. I independently reproduced it:

- the exact submitted Python function returns `500.0` for
  `compare_one("1e2", 500.0)` and exits 0
  ([model_gap_cpython_import.log](evidence/model_gap_cpython_import.log));
- the same function body translated with the trusted translator and run under
  the fresh supplied LLVM model exits 113 after reaching a different comparison
  path
  ([model_gap_probe.py](evidence/model_gap_probe.py) and
  [model_gap_krun.log](evidence/model_gap_krun.log)).

This restriction originates in read-only `/reference/reference-semantics`
(`float.k`'s decimal-only `decStrToF` and `str.k`'s ASCII literal conversion),
not in candidate proof rules. The nine claims have no candidate-added guard and
cover all modeled `Int`, `Float`, and arbitrary finite `IntSeq` string values.
The Python implementation is faithful to CPython on the witness (and the
canonical helper agrees there). Therefore all four conditions of campaign
amendment v2 exception 1 hold. The gap is a non-fatal concern and cannot be
mapped to candidate `FAIL`.

### Gate and decision summary

- Gate A, real-program soundness: pass. The actual body executes, the theorem is
  result-constraining, program identity is mechanical, and fresh result/body
  mutations are rejected.
- Gate B, intent adequacy: covers the material source-contract types and
  unbounded modeled domains. The documented supplied-model exponent/ASCII
  boundary invokes the campaign's `CONCERNS / LEGIT` exception.
- Gate C, trust/evidence auditability: pass. Boundaries, dependents, commands,
  inputs, outputs, and limitations are explicit and independently reproduced.

All reviewer artifacts are under `evidence/`; their SHA-256 manifest is
[evidence_manifest.sha256](evidence/evidence_manifest.sha256).

VERDICT: CONCERNS
LEGITIMACY: LEGIT
