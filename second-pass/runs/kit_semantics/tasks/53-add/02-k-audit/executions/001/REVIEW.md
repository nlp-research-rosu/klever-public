# Independent adversarial audit: HumanEval 53-add

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full annotated HumanEval domain. I rebuilt both definitions
from trusted source, independently obtained `#Top` with exit 0 for the sole
positive claim, mechanically pinned the claim's constructor term to a fresh
trusted translation of `solution.py`, reviewed the complete imported rule
surface, and rejected fresh result and body mutations for the expected semantic
reasons. There are no candidate-authored proof rules, lemmas, functions,
summaries, or operational bridges.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `53-add`, and condition
`kit-semantics`. This agrees with the prompt. The trusted
`/reference/reference-semantics` mount is present, so there is no
mode/mount contradiction.

I read the launcher manifest and all pipeline-v3 records:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the one JSONL file below `/generation-evidence/codex-trace/`.

All required records, trusted mounts, and candidate proof artifacts are regular
files or directories; there are no symlinks or special entries below
`/candidate`, `/reference`, or `/generation-evidence`. The campaign-lock JSON
exactly equals the `audit_campaign` block in `/audit-input.json`, and its
independently computed SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded direct hash checked by the reviewer matches, including
the canonical source, trusted/candidate prompt, trusted/candidate translator,
run and task manifests, stage-1 result and invocation, all generation evidence
files, and the structured trace.

The structured trace contains 231 valid JSON records with no parse failures.
The generation output contains 17,442 decoded lines. These records were
inspected only as untrusted history; their three historical `#Top` lines and
final success report were not used as proof results. See
`evidence/stage1-generation-record-inspection.log`.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate `reference-semantics/` and trusted tree each have exactly 25
entries and are recursively identical by type, relative path, size, and file
hash. There are no missing, additional, mistyped, changed, or symlinked
semantics entries. The reviewer's deterministic semantics-tree digest is
`a81671cf50ee4947d460a3c8396a39cf0c31bd9a56a95d127f4e92d796b4a410`
on both trees. Independently reproducing the pipeline-v3 length-delimited tree
algorithm gives candidate workspace digest
`9941be0c0148107fb6e87969b13e54e390fea33d7b88ed2a7190917050db522f`,
exactly matching `/generation-result.json`; both semantics trees give the task
manifest's
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
and the trace tree gives the usage record's
`5a9ab443dce45543ff9170def950caaae58a3f2477f69806bcd980a874585f47`.
A second reviewer serialization hashed all 778 candidate-tree entries
(81,072,885 bytes) to
`d91ab64f5c65eafc18fc3228e7ffa5f6bea56e0b67706d7ccf099baa4b50fff8`;
this is deliberately an additional digest, not a replacement for the matched
pipeline binding.

The complete checks and exact hashes are in
`evidence/stage1-integrity.log`. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt declares:

```python
def add(x: int, y: int):
    """Add two numbers x and y"""
```

with examples `add(2, 3) == 5` and `add(5, 7) == 12`. The trusted canonical
implementation returns `x + y`. The intended source-contract domain is every
pair of Python integers; the annotations do not require floats, strings,
lists, or arbitrary objects.

The candidate implementation is:

```python
def add(x: int, y: int):
    return x + y
```

It matches the canonical return AST. Running the trusted
`/reference/py2mpy.py` in scratch regenerated:

```text
Module(
  FuncDef("add", Params("x", "y"),
    Return(BinOp("+", Name("x"), Name("y")))))
```

The regenerated file and submitted `solution.mpy` are byte-identical, both
with SHA-256
`67c61c16675c9cff80240867fcd0afd5bbbc0cdcd75147d9acb520ce116c98ee`.
The exact command and exit 0 are in `evidence/stage2-regeneration.log`.

I wrote an independent differential driver,
`evidence/differential_test.py`, which separately imports
`/reference/canonical.py` and the scratch copy of candidate `solution.py`.
It checks both documented examples, zero and sign transitions, cancellation,
32- and 64-bit edges, 100-digit values, and 200 deterministic random
80-digit pairs (seed `530053`). Addition has no control-flow branch boundary
and no meaningful empty case for two required integer arguments. All 217 cases
also agreed with the independent `operator.add` oracle; mismatches were zero.
Every generated input and the exact exit-0 command are preserved in
`evidence/stage2-differential.log`.

## 3. Clean proof reconstruction

Only candidate source artifacts and the trusted semantics tree were copied to
`/tmp/audit-work/reconstruction`. Candidate-provided `runtime-kompiled/`,
`verification-kompiled/`, caches, binaries, logs, and traces were not copied or
used. The audit outputs are separately named
`reviewer-runtime-kompiled/` and `reviewer-verification-kompiled/`;
`evidence/stage3-scratch-isolation.log` records the isolation checks.

The installed tools are K v7.1.293. The fresh concrete build was:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. Fresh `krun` executions of `solution.mpy` and the exact function
constructor applied to four ground inputs also exited 0. The final state had
`.K`, environment 0, empty heap and stack, `noRet`, `NoExc`, exit code 0, and:

```text
"example_2_3" |-> 5
"example_5_7" |-> 12
"mixed_sign" |-> 5
"zero" |-> 0
```

See `evidence/stage3-kompile-llvm.log`,
`evidence/stage3-krun-load.log`, and
`evidence/stage3-krun-tests.log`.

The fresh proof build was:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. Static enumeration finds exactly one positive target claim,
`SPEC.add-correct`. The independent target command was:

```bash
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed exact `#Top`; see
`evidence/stage3-kprove-positive.log`. Compiler warnings concern unused
variables in off-path string rules and non-exhaustive off-path helpers in the
concrete definition. They are not parser, build, or proof failures and none of
the warned symbols occurs on the add execution path.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`SPEC.add-correct` has no explicit `requires` clause. Its formal precondition
is:

- arbitrary `X:Int` and `Y:Int`;
- the exact normal MPY module configuration: environment 0, builtins at scope
  -1, an empty module scope 0 whose parent is -1, next scope location 1, empty
  heap and stack, `noRet`, `NoExc`, and exit code 0; and
- the exact translated module is loaded and then its `add` binding is called
  with `Int(X)` and `Int(Y)`.

The postcondition requires the `<k>` result to be exactly `X +Int Y`. It also
requires the caller environment, allocator counters, empty heap and stack,
return/exception state, and exit code to have their expected final values, and
requires scope 0 to contain the exact loaded `add` closure. The result is not a
free variable, tautology, oracle, or one-way property.

The precondition is satisfiable. For example, `X = 2`, `Y = 3` in the
displayed initial configuration is a ground witness. Substitution makes the K
postcondition `5`; the trusted canonical and candidate Python functions both
return `5`, and the fresh concrete K execution returns `5`.

### Mechanical program identity

`evidence/pinning_check.py` independently:

1. compares the candidate and canonical return ASTs;
2. extracts the balanced `Module(...)` argument of `#loadAll` from the claim;
3. tokenizes constructor names, strings, variables, and punctuation; and
4. requires exact token identity with freshly regenerated `solution.mpy` and
   with the expected `FuncDef("add", Params("x","y"), Return(BinOp("+",...)))`.

It also checks the exact closure body required in the final scope. All checks
exit 0 (`evidence/stage4-pinning.log`). The 32 constructor tokens are
identical. The translator's omission of Python type annotations is a
demonstrated typing-only normalization: it ignores annotations and emits the
same parameter names and body.

The operational path is:

| Submitted/claim construct | Declaration and fixed execution |
|---|---|
| `Module` / `FuncDef` / `Params` | `syntax.k`; `core.k` loads and sequences statements; `functions.k` binds the exact closure in scope 0 |
| `Call(Name("add"), Int(X), Int(Y))` | `call.k` evaluates the callee, then `core.k` evaluates arguments left-to-right |
| closure invocation | `call.k` allocates scope 1, pushes the exact continuation/frame, and invokes `functions.k` parameter binding |
| `Return(BinOp("+", Name("x"), Name("y")))` | strictness evaluates both names through `core.k` lookup; `operators.k` dispatches the binary operation |
| integer `+` | `int.k` rewrites exactly to `X +Int Y` |
| return/pop | `functions.k` records the value, restores environment 0, removes scope 1, restores `scopeLoc`, and empties the frame stack |

No helper claim replaces any part of this path. A fresh operational-sensitivity
mutation changed the `BinOp` in the actually executed claim term and in its
required final closure from `"+"` to `"*"`. It compiled, then failed with exit
1 and a genuine stuck implication comparing `X *Int Y` with `X +Int Y`.
`X = 2`, `Y = 3` witnesses `6 != 5`. See
`evidence/reviewer-body-mutation.k`,
`evidence/stage4-body-mutation-dry-run.log`, and
`evidence/stage4-body-mutation-proof.log`.

## 5. Rule-by-rule static soundness review

`evidence/stage5-rule-inventory.log` is the exhaustive inventory of the
supplied `semantics.k`, all 23 helper K files, candidate `verification.k`, and
the positive spec. It records the exact file, line, normalized declaration,
attributes, path classification, decision, and witnesses where applicable.
Its 1,209 entries comprise:

- 695 rules, 227 syntax declarations, one configuration, five contexts, and
  one target claim;
- 107 `total`, 146 `function`, 45 priority, 26 `owise`, 36 `concrete`, 22
  `no-evaluators`, 25 `symbol`, four macro, one macro-recursive, two strict,
  and one sequential-strict declaration occurrences; and
- no `functional` or simplification declarations.

Candidate `verification.k` has only a `requires`, module/import wiring, and
`endmodule`. Therefore the local extension count is zero: no local syntax,
function, totality assertion, opaque symbol, ordinary rule, priority rule,
simplification, lemma, auxiliary claim, or operational bridge can contribute
to closure.

The inventory marks the 22 fixed rules actually exercised by addition. Each is
faithful over its complete match domain on this path:

- module loading and statement sequencing preserve every cell except the
  intended scope binding;
- lookup selects the actual scope-0 `add` closure and then the callee's exact
  `x` and `y` bindings;
- the shared argument loop evaluates `X` before `Y` and appends both without
  abstraction;
- the unannotated-closure rule has an exact continuation, scope, environment,
  allocator, and stack transition;
- parameter binding is positional and exact for two parameters and two
  arguments;
- `BinOp` dispatch sees two `Int` values, so Bool, Float, list, ref-dereference,
  method, and interception rules are sort- or constructor-disjoint;
- `applyBin("+", I1:Int, I2:Int) => I1 +Int I2` is ordinary integer
  mathematics; and
- return/pop preserves the value and restores every claimed caller cell.

Relevant priorities do not hide alternate behavior. Ref/cell priority rules
cannot match the integer arguments or plain closure. No Call interceptor
matches `Name("add")`; the generic call route is selected. The annotated
closure rule is constructor-disjoint from `closureVal`. The integer-addition
rule does not overlap the Bool/Float/list cases at two `Int` operands. There
is no allocation or state mutation in the body, and the temporary call scope
is the only state change.

The supplied semantics intentionally imports a much larger, incomplete Python
subset. Its proof-domain opaque or concrete-only symbols are:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `md5hexCodes`, `sortVS`, and `sortKeyVS`. None can occur in, affect a
branch of, or constrain the result of this theorem.

The full inventory also records concrete off-path divergences from full
CPython rather than silently treating the supplied subset as a full Python
semantics. Required false-conclusion witnesses include:

- `Import("definitely_missing_module") => .K`, whereas CPython raises
  `ModuleNotFoundError`;
- the multi-digit conversion rules give `int("ab")` the integer `540`, whereas
  CPython raises `ValueError`;
- the arithmetic-eval fallback gives `eval("6/2")` the result `6`, whereas
  CPython returns `3.0`;
- `isIntV(true) => false`, whereas `isinstance(True, int)` is true in CPython;
- the empty-pattern count fold gives `"a".count("") == 0`, whereas CPython
  returns `2`; and
- proof-side shallow equality makes two distinct refs to structurally equal
  nested lists or tuples unequal, whereas CPython recursively compares them.

These are genuine limitations of unused fixed constructs, not candidate
extensions. They cannot enable a false conclusion on the intended `Int × Int`
domain here: the mechanically pinned term contains no Import, conversion,
eval, isinstance, string method, list, tuple, ref, Float, sort, or digest
constructor, and no used rule can synthesize one from `Int`, `Name`, `BinOp`,
`Return`, or the closure lifecycle. They therefore do not materially weaken
this theorem or justify changing its verdict. Accordingly, I classify them as
narrower off-path full-CPython fidelity limitations, not as unsoundness
witnesses on this theorem's intended domain; there is no satisfying add input
on which one can fire.

## 6. Fresh non-vacuity test

I inspected but did not rely on candidate `spec-vacuity.k`. The fresh reviewer
mutation is `evidence/reviewer-false.k`. It leaves the exact program body and
all state obligations unchanged and replaces only the result with the false
`X +Int Y +Int 2`. The precondition remains satisfiable; `X = 2`, `Y = 3`
requires the false result `7` instead of `5`.

First:

```bash
kprove reviewer-false.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE \
  --dry-run
```

exited 0, proving that the mutation parses and builds
(`evidence/stage6-false-dry-run.log`). The real proof command without
`--dry-run` exited 1 with `WarnStuckClaimState`. Its reached configuration has
`X +Int Y` in `<k>`, all expected final cells, and the failed implication:

```text
X +Int Y +Int 2
#Equals
X +Int Y
```

This is the intended unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash. The bounded raw log is
`evidence/stage6-false-proof.log`.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied `MPY` definition, for every pair of K integers `X` and `Y`,
starting in the exact normal module configuration, loading the exact trusted
translation of submitted `solution.py` and invoking its loaded `add` binding
reaches `X +Int Y` with the displayed final scope and with the caller
environment, heap, allocation counters, stack, return state, exception state,
and exit code restored or unchanged as specified. This is a result-constraining
reachability/partial-correctness theorem, not a conclusion inferred from tests.

### Trust ledger

| Boundary | Dependence and assessment |
|---|---|
| Supplied MPY rules | The theorem depends on the exact module, call, scope, return, and integer-dispatch rules inventoried above. They are fixed trusted inputs and are faithful on this complete path. No proof-local rule preempts them. |
| K primitives/toolchain | `+Int`, Bool/Map/List operations used by the configuration, strictness generation, kompilation, Haskell prover, backend, and SMT reasoning are trusted. K v7.1.293 was independently invoked. This is the normal low-level proof checker boundary. |
| Trusted translator | The theorem does not formally prove CPython-AST-to-MPY correctness. For the only relevant nodes, inspection shows direct mappings for `FunctionDef`, `Return`, `BinOp(Add)`, and `Name`; fresh regeneration is byte-identical and constructor pinning is exact. This is an acceptable, explicit source-to-model boundary. |
| Python `int` to K `Int` intent bridge | The source annotations select integers; both models use arbitrary-precision integer addition with no overflow result. The bridge is additionally supported, not proved, by the 217-case differential run. |
| Imported opaque symbols | All 25 are listed in Stage 5. None is reachable and no claim depends on one, so no value-level correctness conclusion is conditional on an opaque program-derived oracle. |
| CPython canonical and `operator.add` | Used only as finite differential oracles. Their agreement supports the translator/intent bridge but is not an axiom, K rule, connection theorem, or substitute for `#Top`. |

Excluded from the theorem are non-integer inputs, an adversarial pre-existing
module state or rebinding, full-Python behavior outside the supplied subset,
and the correctness of the translator, K implementation, backends, and SMT
solver themselves. These exclusions do not narrow the annotated HumanEval
contract.

### Gate and verdict mapping

- Gate A (real-program soundness): PASS. Clean `#Top`, exact program identity,
  no extensions or bridges, exact state footprint, satisfiable precondition,
  and successful negative/body-sensitivity discrimination.
- Gate B (intent adequacy): PASS. The unrestricted formal `Int × Int` domain
  and exact integer-sum result match the source contract and examples.
- Gate C (trust and auditability): PASS. Every audit test, mutation, command,
  input scope, exit status, and bounded relevant output is preserved below
  `evidence/`; formal and empirical conclusions are separated.

The proof is therefore legitimate and has no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
