# Independent adversarial audit: 2-truncate-number

## Overall decision

The candidate's sole reachability claim rebuilds and proves successfully, is
result-constraining, and executes the exact function body text embedded in the
claim. It does **not**, however, execute the submitted `solution.mpy` program.
The claim starts from a manually fabricated post-module-load scope, and there is
no K claim connecting `Module(...)` in `solution.mpy` to that scope. A material
mutation of the separately submitted program leaves the candidate proof at
`#Top`. Under the audit's explicit real-program-pinning requirement, this is a
proof of a substituted invocation state, not a proof of the submitted program.

No candidate-local K rule is labelled unsound. The decisive defect is claim
adequacy/program identity, not logical inconsistency or vacuity.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `2-truncate-number`, and the
launcher container paths used in this audit. The trusted
`/reference/reference-semantics` mount is present, so the mounts do not
contradict the rendered mode.

I inspected every required pipeline-v3 record:

- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation/invocation.json`, `/generation/metrics.json`,
  `/generation/runtime-metrics.json`, and `/generation/usage.json`
- `/generation/codex-last.txt`, `/generation/codex-output.log`, and
  `/generation/prompt.txt`
- the 196-line structured JSONL trace under `/generation/codex-trace`

All are readable regular files, not symlinks. Every JSONL line parses. Direct
SHA-256 values for the trusted canonical, prompt, translator, all launcher
records, and all individual generation evidence files match the values recorded
by the launcher and invocation/result manifests. The generation agent's
`VALIDATED`, `#Top`, mutation, and differential-test reports were treated only
as untrusted claims and independently rerun below.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. A recursive type/path/size/hash comparison of the 24-file candidate
`reference-semantics` tree against `/reference/reference-semantics` reports
zero differences and no symlinks: there are no missing, additional, changed, or
mistyped semantics entries. Candidate proof deliverables are present as regular
files. Thus there is no audit infrastructure breach.

Evidence:

- `evidence/01_provenance_check.py`
- `evidence/01_provenance_check.log` — exact command, hashes, record keys,
  trace event counts, tree comparisons, and exit 0

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`, the intended input is a positive floating-point
number that can be decomposed into an integer part and a leftover decimal part
smaller than 1. The function must return that leftover. The documented example
is `truncate_number(3.5) == 0.5`. The trusted
`/reference/canonical.py` resolves the intended operational meaning as:

```python
return number % 1.0
```

The meaningful intended domain is positive finite Python binary64 values;
NaN and infinity do not have the stated decomposition. There is no collection
"empty" case and there are no branches in this implementation. Zero was tested
as the boundary adjacent to the strictly positive domain.

### Source and translation identity

`/candidate/solution.py` also returns `number % 1.0` with no alternate control
path or side effect. Regenerating with the trusted translator:

```text
python3 /tmp/audit-work/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
```

exited 0. Both files have SHA-256
`8e263c2b21c5292db4ee26dfcd6ad1074c462f89cf4647058319b514151fa97b`.
See `evidence/02_translation_identity.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical and candidate entry
points through separate module loaders. It tests the prompt example; zero;
the smallest positive subnormal; values immediately below, at, and above
integer boundaries; the largest finite float; representative small and very
large positives; a 2,064-value grid; and 10,000 deterministic random positive
finite bit patterns. It does not reuse candidate tests or equations.

```text
python3 /audit-output/evidence/02_differential.py
total_inputs=12083 mismatches=0
```

The command exited 0; full scope and seed are in
`evidence/02_differential.log`. The implementation therefore agrees with the
trusted canonical on all tested inputs. This finite evidence does not prove the
K theorem.

## 3. Clean proof reconstruction

I copied only source artifacts and the independently verified supplied
semantics into `/tmp/audit-work/candidate`. Candidate
`runtime-kompiled`, `verification-kompiled`, caches, and logs were not copied or
used. Source-copy hashes are in `evidence/03_source_copy_hashes.log`.

The live tools are K v7.1.293 (`evidence/03_tool_versions.log`). Fresh commands
and results were:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
Exit: 0

kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
Output: #Top
Exit: 0
```

See `evidence/03_kompile_verification.log` and
`evidence/03_kprove_spec.log`. Static inventory confirms that `spec.k` contains
exactly one positive target claim, so every positive target was rerun.

I also freshly built the concrete definition:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
Exit: 0
```

`krun solution.mpy --definition fresh-runtime-kompiled` exits 0 with `.K`,
`NoExc`, and exit code 0, and its final module scope contains the expected
closure. An independently translated witness module calling `3.5`, `1.0`, and
`123.875` also exits 0 with all assertions discharged. See
`evidence/03_kompile_runtime.log`,
`evidence/03_krun_solution_module.log`,
`evidence/04_auditor_witness.py`, and
`evidence/04_krun_satisfying_witnesses.log`.

Fresh compilation emitted warnings about unused variables and several
non-exhaustive unrelated total functions. They did not alter either build's
zero status and are accounted for in Stage 5.

A separate ground Haskell diagnostic tried to reduce the concrete destination
`0.5`. It parsed, but the Haskell backend exited nonzero on an unsupported
`FLOAT.div` hook rather than deciding the claim
(`evidence/04_ground_witness_proof.log`). This was not a target claim or the
Stage 6 mutation, and it is not used against the candidate. Concrete witness
comparison was performed with the freshly built LLVM definition instead.

## 4. Adequacy and real-program pinning

### What the entry claim says

`/candidate/spec.k:6` has no `requires` clause. Its precondition is therefore:

- `F` may be any K `Float`, not specifically a positive finite binary64 value;
- `<k>` begins with
  `Call(Name("truncate_number"), (F, .Exprs))`;
- environment 0 and scope 0 already exist;
- scope 0 already maps `"truncate_number"` to a manually written
  `closureVal` with parameter `number` and body
  `Return(BinOp("%", Name("number"), Float(1.0)))`;
- the builtins scope, counters, heap, stack, return state, exception state, and
  exit code are fixed to the displayed initial values.

The postcondition is exact rather than free or tautological: `<k>` must contain
`floatMod(F, 1.0)`, and every displayed state cell must again have the same
value. The result is not introduced existentially and there is no implication
that could make it unconstrained.

This precondition is satisfiable. Taking `F = 3.5` and the displayed finite maps
gives a ground state. Both trusted and candidate Python functions return `0.5`
(`evidence/04_ground_python.log`), and the LLVM witness discharges the same
concrete assertion.

### Real-program pinning failure

The actual translated program `/candidate/solution.mpy:1` begins with:

```text
Module(
  Expr(Str(...))
  FuncDef("truncate_number", Params("number"),
    Return(BinOp("%", Name("number"), Float(1.0)))))
```

The claim's `<k>` cell never contains or loads this `Module`. It bypasses
`#loadAll`, statement sequencing, the docstring expression, and `FuncDef`,
starting instead from a manually asserted scope. `/candidate/verification.k`
only imports `MPY`; it contains no auxiliary module-loading reachability claim
or connection theorem. The exact embedded body is good evidence about the
surrogate state, but it is not execution of the submitted `solution.mpy` as
required by this audit.

The decisive sensitivity experiment is
`evidence/04_body_sensitivity.log`:

1. `evidence/04_auditor_mutated_solution.py` materially changes the separately
   submitted program body to `% 2.0`.
2. At satisfying input `3.5`, the trusted canonical returns `0.5` and the
   mutated program returns `1.5`.
3. The unchanged candidate `spec.k` and fresh proof definition still print
   `#Top` and exit 0.

This differs from the candidate's `spec-body-mutation.k`, which changes the
closure body *inside the surrogate claim*. That negative probe only shows that
the theorem is sensitive to its embedded closure; it does not connect that
closure to the separately submitted program.

Consequently, the positive `#Top` proves the behavior of the manually
constructed call state, not partial correctness of the real submitted module.
This is a material adequacy failure under the stated decision boundary.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.txt` is a line-addressed inventory of the assembled
`semantics.k`, every supplied helper K file, `verification.k`, and `spec.k`.
The inventory contains:

- 929 total local items;
- 227 syntax declarations, including 146 functions, 107 `total`
  declarations, 25 named symbols, and 22 `no-evaluators` opaque symbols;
- 695 ordinary semantic rules, including 32 concrete rules, 29 priority rules,
  and 26 `owise` rules;
- 5 evaluation contexts, 1 configuration, and 1 reachability claim;
- 0 `functional` declarations and 0 simplification rules.

Every item includes its complete collapsed declaration/rule, source line,
attributes, and a disposition. `verification.k` has zero local extensions:
no syntax, function, totality axiom, opaque symbol, lemma, priority,
simplification, ordinary rewrite, bridge, or helper claim. There is therefore
no candidate rule capable of smuggling the answer or bypassing execution.

`evidence/05_used_path_review.md` maps every construct in `solution.mpy` to its
syntax and operational rules. In summary:

- `core.k:49,125-127` configures, loads, and sequences a module;
- `str.k:14` and `controls.k:48` evaluate/discard the docstring;
- `functions.k:14-16` installs a `FuncDef` closure;
- `call.k:20-21,69-74`, `core.k:131-154,189-191`, and
  `functions.k:63-90` implement lookup, left-to-right arguments, frame
  allocation, parameter binding, return, and restoration;
- `syntax.k:15` gives `BinOp` left-to-right `seqstrict` evaluation,
  `operators.k:12` dispatches it, and `float.k:21,37-39` handles the literal
  and float `%`.

The state footprint is coherent on this path: the call allocates temporary
scope 1 and a stack frame, binds `number`, executes the exact embedded body,
then removes the scope and restores environment 0, scope counter 1, empty stack,
and `noRet`. The body does not touch heap, allocation, output, or exception
state. Relevant priority rules have guards that are false for this ordinary
non-cell closure, and the float percent rule is sort-disjoint from integer
percent. No incompatible overlap was found.

### Result-bearing primitive and trust boundary

`reference-semantics/semantics/float.k:37` declares:

```text
floatMod(Float, Float)
[function, total, symbol(floatMod), no-evaluators]
```

The symbolic proof leaves this term opaque. Line 39 faithfully dispatches the
program's evaluated `%` to that exact symbol. Line 38 has an LLVM-only concrete
floor-modulo equation. Thus `floatMod` is a fixed language primitive outside
the program-defined body, not a candidate proof-local oracle. The formal
theorem establishes only that the body returns this exact primitive term; its
human interpretation as Python's fractional part remains conditional on the
supplied primitive and input encoding.

On positive finite values with divisor exactly `1.0`, the equation is the
ordinary floor-based fractional part. Normal and near-integer LLVM probes pass.
The candidate's 1,521-test Python script does **not** independently test this K
primitive—it compares Python code with `math.modf`—so it supports implementation
intent only.

A fresh smallest-subnormal source-literal assertion failed
(`evidence/05_boundary_probe.log`). Observation
(`evidence/05_subnormal_observe.log`) shows why: the translated raw input and
expected `5e-324` tokens remain
`0.49999999999999998e-323`, while `% 1.0` produces
`0.49406564584124654e-323`, which is the actual minimum binary64 subnormal used
by CPython (`evidence/05_subnormal_python.log`). This is evidence of a missing
decimal-token-to-CPython-binary64 input/literal bridge, not a false target
result: the observed target result agrees with CPython, and `solution.mpy`
itself uses only exactly representable `1.0`. I therefore record the narrower
bridge limitation and do not label `floatMod` or the target result unsound.

LLVM warned that six unrelated `total` functions are not exhaustive on an
internal `cellsMark` value (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). None occurs on this program's path. The inventory
does not turn incompleteness warnings into unsoundness: no concrete or symbolic
false conclusion witness on the intended target domain was found.

No inventoried rule is labelled unsound, so there is no omitted false-rule
witness. The static failure remains the separately evidenced absence of a
real-program connection.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation
`evidence/06_false_mutation.k` changes the result-bearing destination from
`floatMod(F, 1.0)` to `F`, leaving execution and every state cell unchanged.
This is demonstrably false for the satisfying input `F = 3.5`, where both
Python implementations return `0.5`.

First, the mutation built successfully:

```text
kprove auditor-false-result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDITOR-FALSE-RESULT \
  --dry-run
Exit: 0
```

Then the actual proof:

```text
kprove auditor-false-result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDITOR-FALSE-RESULT
Exit: 1
```

failed for the expected unmet obligation, not a parser/import/crash:

```text
Warning (WarnStuckClaimState)
#Not ( F #Equals floatMod(F, 1.0) )
<k> floatMod(F, 1.0) ~> .K </k>
```

Exact commands, complete bounded residual, and exit statuses are in
`evidence/06_false_mutation_build.log` and
`evidence/06_false_mutation_proof.log`. The target claim is therefore
non-vacuous and discriminates its result. Non-vacuity does not cure the
real-program-pinning failure.

## 7. Proven versus assumed accounting

### What the successful proof actually establishes

Relative to the supplied `MPY` theory, for any K `Float F`, **if** execution
starts in the manually displayed configuration where scope 0 already contains
the displayed one-parameter closure, then calling that closure terminates in
the displayed restored state with `<k>` equal to `floatMod(F, 1.0)`.

This is a strong, non-vacuous partial-correctness statement about that call
configuration. It executes name lookup, argument evaluation, binding, the
embedded body, `%` dispatch, return, and frame cleanup. It neither proves total
correctness in general nor proves an algebraic range theorem such as
`0 <= result < 1`.

### Assumptions and trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover | All closure and proof results | Ordinary toolchain trust; fresh build and proof evidence preserved |
| Unmodified supplied `MPY` operational semantics | Binding, order, control, cells, `%` dispatch | Fixed semantics; all local declarations/rules inventoried, used path reviewed |
| Opaque `floatMod(F,1.0)` | Entire returned value and formal destination | Acceptable only as a conditional fixed primitive; symbolic proof gives it no IEEE/Python interpretation |
| LLVM concrete `floatMod` equation | Concrete adequacy tests | Empirical bridge only; normal/near-boundary tests pass |
| Decimal K `Float` token versus Python binary64 input | Domain interpretation | Incomplete bridge; smallest-subnormal literal probe exposes different raw encodings |
| Trusted translator | Python source to submitted `solution.mpy` | Regeneration is byte-identical |
| Candidate versus canonical Python differential | Implementation-to-intent bridge | 12,083 finite tests, zero mismatches; finite evidence only |
| `solution.mpy Module` to manually populated claim scope | Program identity | **Illegitimate/missing proof boundary**: no K connection claim, and an actual-program mutation leaves `#Top` unchanged |

The candidate `PROOF.md`, generated trace, prior compiled definitions, and
reported differential results were not used as proof substitutes.

### Gate summary and verdict rationale

- Provenance/infrastructure: pass.
- Python implementation and translator fidelity: pass.
- Fresh positive proof reconstruction: pass (`#Top`, exit 0).
- Result constraint and fresh non-vacuity: pass.
- Candidate-local rule soundness: no local extensions; no unsound-rule finding.
- Real submitted program pinning: **fail**.
- Natural-language intent: the Python implementation is correct on tested
  positive finite inputs, but the K theorem is only a structural
  `floatMod` result conditional on the stated primitive/input bridge.

The audit decision boundary explicitly classifies a proof of a substituted
program, or one that does not pin the real generated program, as
`FAIL / NOT_LEGIT`. The clean `#Top` and successful non-vacuity probe cannot
override that failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
