# Independent adversarial review: 2-truncate-number

This review treats every candidate and generation record as untrusted evidence.
All executable checks used a source-only copy under
`/tmp/audit-work/fresh`; neither candidate kompiled directory nor any
candidate cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem and condition
(`2-truncate-number`, `kit-semantics`). The supplied-semantics mount required by
that declaration is present at `/reference/reference-semantics`.

All pipeline-v3 records required by the audit prompt were present, readable,
and of the expected regular-file or directory type:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace under `/generation/codex-trace`;
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`.

The trace contains one regular JSONL file, no symlinks, and 196 independently
parsed JSON objects. The required JSON records also parsed. Their contents
describe a successful generation and claim prior `#Top`, negative mutations,
and 1,521 tests. Those statements were not relied on; the relevant claims were
reconstructed independently. A bounded record summary is in
`evidence/01_generation_record_summary.log`.

Independent SHA-256 results match the launcher-recorded values for the
canonical source, prompt, translator, run/task/result/invocation manifests, all
three metrics/usage records, generation prompt, generation final text,
generation output log, and the sole trace file. In particular, the trace file
hash is
`55513bbe1958273a69282b857436a8c13f5d1e4ba55bb3ffe8afeab8a8146a0b`,
matching the per-file value in `/generation-result.json`. The launcher also
records aggregate tree/manifest hashes whose private aggregation format is
not needed for the stronger content check below.

`cmp` establishes byte identity between candidate and trusted `prompt.py`, and
between candidate and trusted `py2mpy.py`. A recursive,
no-symlink-dereference `diff` establishes exact identity between
`/candidate/reference-semantics` and
`/reference/reference-semantics`: no file is missing, additional, changed, or
mistyped. Neither tree contains a symlink. The entire candidate tree also has
zero symlinks. Commands, statuses, and hashes are preserved in
`evidence/01_provenance.sh` and `evidence/01_provenance.log`.

The intact candidate mount contains every required proof artifact:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. It also contains candidate-built definitions and caches; these were
deliberately excluded from the scratch copy.

Stage result: provenance and supplied-semantics integrity pass. There is no
audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the decimal/fractional leftover of a positive
floating-point number. For the meaningful stated decomposition, the intended
domain is positive finite Python floats. The trusted canonical implementation
is:

```python
return number % 1.0
```

The candidate implementation uses exactly the same expression and signature.
Its extra module docstring does not change the Python result.

The scratch preparation copied only source artifacts and the exact supplied
semantics. Before either build, it confirmed zero symlinks and zero
`*-kompiled` directories. Running the trusted translator as:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `regenerated-solution.mpy` is byte-identical to the submitted
`solution.mpy`; both hash to
`8e263c2b21c5292db4ee26dfcd6ad1074c462f89cf4647058319b514151fa97b`.

The reviewer-authored differential oracle imports the trusted canonical module
and scratch candidate module independently. The function is scalar, so there
is no meaningful empty-container case and it has no branch boundary. The test
therefore covers the documented example, integer and neighboring-float
boundaries, the smallest positive subnormal, minimum normal, values around
`1.0`, `2.0`, and `2**52`, the maximum finite float, a 3,999-value fractional
grid, and 4,096 deterministic random positive finite binary64 values. Result:

```text
documented=1
positive_finite_boundaries=12
positive_finite_grid=3999
positive_finite_generated=4096
total=8108 mismatches=0
```

The script, complete input construction, command, and exit 0 are preserved in
`evidence/02_differential.py`, `evidence/02_prepare_and_fidelity.sh`, and
`evidence/02_fidelity.log`.

Stage result: the generated Python program is faithful to the trusted
canonical behavior on the material source-contract domain, and the submitted
constructor program is exactly the trusted translation.

## 3. Clean proof reconstruction

K 7.1.293 was used. The following fresh definitions were created only under
`/tmp/audit-work/fresh`:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Both commands exited 0. The LLVM definition executed the regenerated module
and a reviewer-authored five-case assertion module. Both `krun` commands
exited 0; the assertions ended with `.K`, `NoExc`, and exit code 0.

There is one positive target claim, `SPEC.truncate-number`. The independent
command was:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`. The exact source-only preparation, compilation,
execution, proof commands, compiler output, and statuses are in
`evidence/03_rebuild_and_prove.sh` and
`evidence/03_rebuild_and_prove.log`.

The compilers report fixed-semantics warnings: unused variables in `str.k`,
and LLVM non-exhaustiveness warnings for several unrelated declared-total
helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`). None occurs in the target execution trace, none is a proof-local
extension, and no warning changed a command's zero status. They are recorded
as narrow, unused fixed-semantics coverage limitations, not as proof evidence
or as an unsoundness finding.

Stage result: every positive target-proof claim closes from a clean build.

## 4. Adequacy and real-program pinning

### Entry precondition and postcondition

The claim has no explicit `requires` condition. Its sort variable permits any
`F:Float`, which includes the intended positive finite subset rather than
narrowing it. In plain language, its initial state is:

- `<k>` calls the name `truncate_number` with exactly one float argument;
- environment 0 contains exactly that name bound to a one-parameter closure;
- the closure body is exactly
  `Return(BinOp("%", Name("number"), Float(1.0)))`;
- the closure's defining environment is 0, whose parent is the fixed builtins
  scope;
- scope/heap allocation counters are 1 and 0, heap and stack are empty,
  return state is `noRet`, exception state is `NoExc`, and exit code is 0.

The postcondition says the call completes with
`floatMod(F, 1.0)` in `<k>`. Because all other cells occur without rewrites,
they must return to their initial values: the temporary call frame and scope
are gone, no heap object was allocated, return state is cleared, and there is
no exception or exit-code change. This is a result-constraining equality, not
a free result, implication-only condition, or tautology.

### Mechanical program identity

`evidence/04_constructor_pinning.py` parses balanced constructor applications
from the trusted regeneration and from the claim. It mechanically extracts:

```text
FuncDef("truncate_number",Params("number"),
  Return(BinOp("%",Name("number"),Float(1.0))))
```

and constructs the closure that the fixed `FuncDef` rule produces. It is
identical to the actual claim term:

```text
closureVal(("number",.ParamNames),
  (Return(BinOp("%",Name("number"),Float(1.0))).Stmts),0)
```

The function name, parameter constructor, body constructor, and defining
environment all match. Python type annotations are intentionally absent from
the trusted translator's executable constructor term.

The translated module's only preceding statement is the module docstring.
Under the fixed rules, `Module` exposes its statements, the ASCII `Str`
literal becomes a value, and `Expr(_:Val)` discards that value without
changing a configuration cell. The subsequent fixed `FuncDef` rule creates
the exact closure above. The fresh concrete execution of
`regenerated-solution.mpy` confirms the resulting module scope and unchanged
heap, counters, stack, return, exception, and exit-code cells. Thus the claim
starts after a demonstrated semantically inert normalization; it does not
substitute another function body.

### Satisfiability and concrete substitution

`F = 3.5` inhabits `Float` and, together with the explicitly written initial
cells, is a concrete satisfying state. Substitution yields the claimed term
`floatMod(3.5, 1.0)`. Both trusted canonical Python and candidate Python return
`0.5`; the independently built LLVM semantics passes the same assertion.
Additional substitutions at `0.5`, `1.0`, and `123.875` agree with both Python
implementations and the LLVM assertions. The constructor comparison and
Python witness output are in `evidence/04_pinning_and_witnesses.log`.

An additional, non-required attempt to make the Haskell prover reduce those
ground float values exited 1 because the Haskell backend lacks the
`FLOAT.div` hook used by the fixed concrete equation. The error is explicitly
preserved in `evidence/04_pinning_and_witnesses.log`. It is not a stuck
logical obligation and is not used as non-vacuity evidence. It also does not
affect the symbolic target proof, where `floatMod` is deliberately opaque, or
the fresh LLVM concrete witnesses.

Stage result: the entry state is satisfiable; the claim pins and executes the
real translated body; concrete substitutions agree with the trusted program
and concrete supplied semantics.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.py` scans the assembled supplied semantics, every
helper `.k` file, `verification.k`, and `spec.k`. The final exhaustive
inventory is `evidence/05_rule_inventory_v3.tsv`. It contains each source
location, complete compact source statement, attributes, and a per-entry
disposition. It enumerates:

- 227 syntax declarations;
- 695 rules;
- 5 explicit contexts;
- 1 configuration;
- 1 claim;
- 25 `requires`, 27 module, 88 import, and 27 end-module assembly records.

Across those entries it identifies 145 statements carrying `function`, 107
carrying `total`, no `functional` declaration, 22 carrying the
`no-evaluators` opaque attribute, 45 priority-bearing statements, no
simplification rule, 35 concrete-equation statements, 26 `owise` statements,
and 3 macro-bearing syntax statements (four macro productions). The final inventory has
1,096 records including assembly, or 929 semantic/specification statements
when assembly is excluded.

`verification.k` contributes only a requirement, module wrapper, and
`imports MPY`. It declares no syntax, function, totality assertion, opaque
symbol, equation, lemma, priority, simplification, operational rule, or
auxiliary claim. Therefore there is no proof-local rule that can encode the
answer, preempt execution, fabricate a result, or make the theory
inconsistent. `spec.k` contributes only the reviewed entry claim.

Each fixed rule not reachable from this target is marked
`FIXED_SUPPLIED_NOT_TARGET_REACHABLE`; this is not a claim that the supplied
subset is a complete Python semantics. Those rules contain no simplification
axiom or unguarded equality that can fire without its own constructor, and the
target path never constructs those symbols. The inventory separately marks
the exact module-normalization and target-execution ranges. No task-local
symbol or rule occurs in the supplied tree.

### Used-construct map and execution order

The actual constructor terms map to fixed declarations and rules as follows:

| Construct | Fixed source and effect |
|---|---|
| `Module`, statement list | `syntax.k`; `core.k:123-127` loads and sequences |
| docstring `Expr(Str(...))` | `str.k:13-17`, `controls.k:46-48`; value is discarded |
| `FuncDef`, `Params`, `Return` | `syntax.k`; `functions.k:14-16` creates the pinned closure |
| `Call`, `Name`, argument list | `call.k:18-21`, `core.k:129-191`; callee then argument, left-to-right |
| closure application | `call.k:69-74`; allocates one temporary scope and pushes the exact continuation |
| parameter binding | `functions.k:63-66`; binds `number` to `F` |
| `BinOp("%", Name(...), Float(...))` | generated `seqstrict` contexts, `operators.k:12`, `float.k:20-21,39` |
| return and cleanup | `functions.k:78-90`; records result, pops the exact frame, restores cells |
| returned modulo value | `float.k:37-39`; fixed `floatMod` primitive |

The operational trace is deterministic on the written state: generic `Call`
first resolves the exact scope-0 closure, evaluates the sole argument, creates
scope 1 with parent 0, binds `number`, evaluates the return expression
left-to-right, dispatches `%` on two `Float` values, and then pops the frame.
The claim explicitly covers every configuration cell that these rules read or
write.

Relevant overlaps are safe:

- the generic call rule is `owise`; no fixed math-call interception matches
  `Call(Name("truncate_number"), ...)`;
- the local scope contains `truncate_number` and later `number`, so lookup does
  not fall through; cell-aware priority rules have false `"$cells"` guards;
- closure, builtin, type, and bound-method dispatches are constructor
  disjoint;
- float and integer `%` dispatches are sort-disjoint;
- no heap-reference priority rule matches the float operands;
- the single return rule reaches a real pushed frame, and pop restores exactly
  the continuation and cells written by the call rule.

There is no loop, allocation, mutation, output, exceptional branch, or helper
claim in this program.

### Opaque and total symbols

Of the 22 fixed opaque symbols, only `floatMod` is reachable. It is declared:

```k
syntax Float ::= floatMod(Float, Float)
  [function, total, symbol(floatMod), no-evaluators]
rule floatMod(F1, F2)
  => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

This is a general, supplied implementation-level primitive for float modulo,
not a proof-local summary of `truncate_number`. It does not skip the
program-defined body: fixed operand evaluation and `%` dispatch reach it. In
the symbolic Haskell proof it remains one exact function of both operands,
so the theorem is interpretation-parametric rather than able to choose an
arbitrary result. The concrete equation is floor-based, as Python `%` is; with
divisor `1.0` it is the ordinary fractional-part expression. The independent
LLVM assertions and 8,108-case CPython differential test support the concrete
bridge but are not presented as its universal proof.

This is an acceptable low-level supplied-semantics trust boundary. It affects
the returned value only and no control or state cell. There is no circular
program-derived oracle: the candidate neither introduced `floatMod` nor added
an equation about it. The source canonical itself uses the corresponding
Python primitive.

No unsound rule was identified. Accordingly this review makes no unsoundness
allegation for which a false-conclusion witness would be required. The fixed
compiler warnings noted in Stage 3 are retained as narrower, unused coverage
gaps rather than mislabeled as unsoundness.

Stage result: the fixed rules execute every material operation, all
proof-local-extension categories are empty, and no rule permits a false
conclusion on the intended input domain.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not reused. The reviewer-authored
`/tmp/audit-work/fresh/audit-spec-vacuity.k` keeps the exact precondition and
executed body but changes the postcondition to the input `F`. This is
demonstrably false at the satisfying witness `F = 3.5`, where both Python
implementations and LLVM return `0.5`.

The fresh mutation parsed and executed against the clean Haskell definition.
It exited 1 with `WarnStuckClaimState`; the reached configuration contains
`floatMod(F, 1.0)` and the unmet implication is the equality between that term
and `F`. This is the expected result-bearing residual, not a parser error,
missing import, timeout, backend-hook crash, or unreachable mutation.

A second reviewer-authored sensitivity claim changes the closure term actually
executed from `% 1.0` to `% 2.0` while retaining the original result
obligation. It also parsed and exited 1 with `WarnStuckClaimState`; its reached
term is `floatMod(F, 2.0)` and the unmet equality compares it with
`floatMod(F, 1.0)`. This independently confirms body sensitivity.

The exact mutation sources, commands, both exit statuses, full residuals, and
the wrapper's final expected-failure confirmation are in
`evidence/06_nonvacuity_and_body_sensitivity.sh` and
`evidence/06_nonvacuity_and_body_sensitivity.log`.

Stage result: the positive proof is non-vacuous and sensitive to both its
result obligation and the executed function body.

## 7. Proven versus assumed accounting

### What is machine-proved

Relative to the exact supplied `MPY` semantics, for every K value `F:Float`,
starting in the explicitly written, satisfiable module state, executing the
actual submitted `truncate_number` closure returns exactly
`floatMod(F, 1.0)`. The proof includes name lookup, argument evaluation and
binding, the program-defined return expression, binary-operator dispatch,
return control, frame deletion, and restoration of every written state cell.
It is a partial-correctness reachability theorem; it does not separately prove
total correctness.

### Trust and evidence ledger

| Boundary | Influence | Status and support |
|---|---|---|
| Trusted prompt and canonical | Defines intended result/domain | Launcher-mounted, independently hashed and read |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Candidate copy matches; trusted regeneration is byte-identical |
| Supplied reference semantics | All operational meaning | Exact recursive candidate/trusted identity; rebuilt from source |
| K 7.1.293 compiler and Haskell prover | Symbolic execution and `#Top` | Standard toolchain trust; exact commands and outputs preserved |
| LLVM backend and float hooks | Concrete semantic witnesses | Five fresh assertions pass; finite evidence only |
| `floatMod(Float,Float)` | Entire returned value | Acceptable fixed primitive; general concrete equation inspected, 8,108 Python comparisons and LLVM witnesses; symbolic theorem remains explicitly conditional on this primitive |
| Docstring/type-annotation normalization | Source-to-entry pinning | Constructor-level script plus fixed rules and fresh module execution |
| Positive finite interpretation | Human-facing domain | Prompt decomposition and canonical behavior; formal K claim is broader, not narrower |
| Termination | Total-correctness aspect | Not claimed; the reachability result is partial correctness, though concrete straight-line runs terminate |

The failed supplemental ground Haskell float-hook probe is an evidentiary tool
limitation only. It is explicitly separated from both the successful symbolic
proof and the successful concrete LLVM checks.

### Gate conclusions and decision

Gate A passes: the real body executes with no local bridge or lemma; state,
binding, value, and control are pinned; and both fresh negative probes are
rejected for the expected logical residual.

Gate B passes: the formal domain contains the full material positive-finite
source domain, the implementation is exactly the canonical `% 1.0` algorithm,
and the supplied general modulo primitive connects it to the requested
fractional result. No finite-size restriction or bounded unrolling appears.

Gate C passes: every claimed reviewer test has a preserved artifact, exact
command, input scope, oracle, exit status, and output. Empirical checks are
used only to support the low-level concrete primitive and intent bridge, never
as a replacement for `kprove`.

The proof is therefore sound, result-constraining, non-vacuous, and about the
real generated program on the material source-contract domain. The named
low-level primitive and backend limitation do not create a material adequacy
gap.

VERDICT: PASS
LEGITIMACY: LEGIT
