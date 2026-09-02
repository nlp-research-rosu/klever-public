# Independent adversarial audit: 77-iscube

This review treats every candidate artifact and generation record as untrusted
evidence. I reconstructed the proof from source in `/tmp/audit-work`, did not
reuse any candidate `*-kompiled` directory or cache, and used the required
`using-kit` and `validating-proof` procedures.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required files at the root
of `/generation-evidence`, `codex-last.txt`, `codex-output.log`, `prompt.txt`,
and all 849 JSONL records in the structured trace. The trace inventory records
its event and payload types and the generation tool activity without treating
any of it as proof evidence.

Independent integrity results:

- The campaign object in `/audit-campaign-lock.json` equals the
  `audit_campaign` block in `/audit-input.json`; its SHA-256 is the recorded
  `ad5dfc...d745`.
- All launcher-declared pipeline-v3 records and provenance mounts are readable
  regular files/directories. The trace contains one regular JSONL file. No
  required record is missing or mistyped.
- Every recorded ordinary-file SHA-256 checked in `audit-input.json` matches,
  including the run/task/result manifests, invocation, generation metrics,
  runtime metrics, usage, prompt, final response, output log, trusted prompt,
  trusted translator, and canonical implementation.
- Every per-file evidence digest in `generation-result.json` matches. Its
  `outputs` object is identical to the one in `invocation.json`.
- An independent reimplementation of the pipeline tree digest gives
  `ca615660...a33a` for `/candidate`, exactly the workspace digest in
  `generation-result.json`; `4e06397a...89f` for each semantics tree, exactly
  the manifest digest; and `ce89c40d...96d3` for the structured trace, exactly
  the source digest in `usage.json`. The additional launcher snapshot digests
  use a distinct, unstated serialization; I did not substitute them for these
  independently reproducible byte/tree checks.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted prompt and translator.
- A type-and-content recursive comparison found 25 entries and zero
  differences between `/candidate/reference-semantics` and
  `/reference/reference-semantics`. Neither tree contains a symlink. There are
  no missing, additional, changed, or mistyped semantics entries.

Evidence:

- `evidence/integrity_check.py`
- `evidence/stage1-integrity.log`
- `evidence/trace_inventory.py`
- `evidence/stage1-trace-inventory.log`

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt requires `iscube(a)` for a valid integer `a`. It must return `True`
exactly when `a` is the cube of some integer. The examples require true for
`1`, `-1`, `64`, and `0`, and false for `2` and `180`. There is no numeric
bound in the source contract.

The canonical implementation takes `abs(a)`, computes a floating cube-root
approximation, rounds it, cubes the rounded integer, and compares it with the
magnitude. The generated implementation instead normalizes the sign and
linearly searches candidates from zero. For mathematical integers, the latter
implements the literal contract: nonnegative cubes are strictly increasing and
unbounded, and a negative integer is a cube exactly when its magnitude is the
cube of the negated root.

### Translation identity

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced SHA-256
`c9504db1b06add72cdc8d483b22171a63492d9b0cafea71d9be5b9c59223a283`.
The submitted `solution.mpy` has the same digest and is byte-identical.

Exact command and result are in `evidence/stage2-translation.log`:

```text
python3 ../trusted/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
byte_identity=true
exit_status: 0
```

### Independent differential testing

`evidence/differential_test.py` imports both trusted `canonical.py` and the
generated `solution.py`. It also uses an independently written exact
binary-search cube oracle. It covers:

- all six documented examples;
- negative, zero, positive, loop-zero-iteration, exact-hit, and adjacent
  non-cube branch boundaries;
- values immediately below, at, and above every cube with roots `0..300`,
  including signs;
- 2,000 deterministic generated integers in `[-2,000,000, 2,000,000]`;
- larger exact/adjacent cubes through root `100,000`.

There is no meaningful “empty” value in an integer-only domain. The 3,815
distinct executed inputs produced zero candidate/canonical mismatches, zero
candidate/contract-oracle mismatches, and zero canonical/oracle mismatches in
that executed set (`evidence/stage2-differential.log`, exit 0).

The canonical float algorithm is not universally equal to the literal prompt:
for `(10**15)**3` it returns `False` while the exact oracle returns `True`.
Executing the linear candidate on that input would require `10**15`
iterations, so this was explicitly recorded as a canonical-versus-contract
probe, not a differential execution. This does not count against the
candidate: its code and theorem implement the unrestricted source contract,
whereas this extreme behavior exposes a limitation of the reference
implementation.

## 3. Clean proof reconstruction

The scratch copy contains source artifacts and the trusted semantics only.
Candidate definitions, `.pyc` files, and caches were not copied or referenced.

### Concrete definition

The following fresh LLVM build exited 0:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
```

The independent concrete program begins with the exact nine-line
`solution.py` body and adds 16 assertions covering the examples and sign/loop
boundaries. Translation used the trusted translator. `krun` terminated with
`.K`, `NoExc`, and exit code `0`.

Evidence: `evidence/concrete_audit.py`,
`evidence/stage3-llvm-build.log`, and
`evidence/stage3-concrete-run.log`.

### Proof definitions and positive claims

Every fresh build exited 0, and every positive claim run below exited 0 and
printed `#Top`:

| Purpose | Fresh command/result evidence |
|---|---|
| Base Haskell definition | `evidence/stage3-haskell-base-build.log` |
| Exact source loading/closure identity | `evidence/stage3-proof-identity.log`: `#Top` |
| Bridge-free universal loop theorem | `evidence/stage3-proof-connection.log`: `#Top` |
| Connection-rule Haskell definition | `evidence/stage3-haskell-connection-build.log` |
| Source-`While` auxiliary theorem | `evidence/stage3-proof-source-connection.log`: `#Top` |
| Final Haskell definition | `evidence/stage3-haskell-verification-build.log` |
| Universal entry theorem | `evidence/stage3-proof-entry.log`: `#Top` |
| Candidate ground claims for 8 and 9 | `evidence/stage3-proof-ground-values.log`: `#Top` |
| Bridge-enabled connection at depth 1 | `evidence/stage3-proof-bridge-depth1.log`: `#Top` |

The builds emit only warnings. Four unused `strLt` variables and the
proof-local map value `S` are intentionally not referenced. LLVM also warns
about non-exhaustive supplied-semantics functions on constructors that the
program never creates. No warning affects a used redex or a result-bearing
proof-local symbol.

The clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Entry theorem in plain language

`SPEC.iscube-entry` has no `requires` clause. `INPUT` ranges over every K
`Int`. Its initial state has environment `0`, the builtins frame, a module
scope binding `"iscube"` to `iscubeClosure`, scope location `1`, empty heap and
stack, `noRet`, `NoExc`, and exit code `0`. It executes:

```k
Call(Name("iscube"), Int(INPUT))
```

and requires the returned value to be exactly `isCubeInt(INPUT)`, with all
explicit non-`k` cells preserved/restored. This is an equality-style result,
not a free variable, implication, or tautology.

`isCubeInt` searches the nonnegative magnitude from zero. `cubeSearch(A,I)`
returns true on `I^3=A`, false on `I^3>A`, and otherwise continues at `I+1`.
Thus the postcondition is true exactly when the input is an integer cube.

### Loop theorem and bridge

`CONNECTION.search-loop` starts at the real internal `#while` reached by the
submitted loop. It pins:

- the exact nested multiplication guard and `candidate += 1` body;
- the exact singleton source return and `#endcall` continuation;
- environment `1`;
- local bindings `"a" |-> A` and `"candidate" |-> C`;
- an arbitrary disjoint preserved scopes map `SC`;
- scope/heap locations, empty heap, exact one-frame stack, return state,
  exception state, and exit code.

It reaches `cubeSearch(A,C)`, restores environment/scope location, deletes the
callee frame, and empties the stack. It was proved against
`VERIFICATION-BASE`, which does not import the operational bridge. The sole
bridge in `connection-rule.k` has the identical left side, right side, cells,
and match domain. Therefore the bridge admits no configuration outside the
machine-checked theorem.

`SOURCE-CONNECTION.search-loop-source` imports that already connected bridge;
it is useful auxiliary evidence for the one fixed `While => #while` step, but
it is not used as the bridge's justification. The bridge-free
`CONNECTION.search-loop` is the justification.

### Mechanical program identity

There are three independent links:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. `evidence/program_term_compare.py` extracts the balanced `Module(...)`
   argument from `IDENTITY.solution-loads-exact-closure`, normalizes only the
   explicit/omitted `.Stmts` unit, and compares it with `solution.mpy`;
3. the identity reachability claim executes normal module loading and proves
   that this exact function definition creates the `iscubeClosure` used by the
   entry theorem.

The constructor comparison has equal compact lengths (418) and
`constructor_term_equal=True` (`evidence/stage4-program-term-compare.log`).
This is constructor-level program pinning, not reliance on an external source
filename.

### Satisfying states and concrete substitutions

Every K integer instantiates the entry precondition. The concrete states for
`-8`, `0`, `7`, and `27` are realizable examples. A fresh four-claim K spec
closed with `#Top`, yielding true, true, false, and true respectively; both
Python implementations give the same values
(`evidence/audit-ground-spec.k`,
`evidence/stage4-ground-instances.log`).

### Body sensitivity

I changed the `AugAssign` in the closure that the entry claim actually
executes from `+1` to `+2`, rebuilt a fresh final definition successfully, and
asked that input `27` still return true. The bridge for the original body did
not match. Fixed semantics reached `<k> false </k>`, the proof got
`WarnStuckClaimState`, and exited 1. The residual visibly contains the mutated
`Int(2)` closure.

Evidence: `evidence/body-mutation-spec.k`,
`evidence/stage4-body-mutation-setup.log`,
`evidence/stage4-body-mutation-build.log`, and
`evidence/stage4-body-mutation-proof.log`.

The theorem pins the real submitted body and covers the unrestricted integer
source domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` lexically inventories every source construct in all
24 supplied K files plus the eight relevant proof/spec files, preserving each
complete declaration/rule/claim with its path, line, guard, cells, and
attributes. The resulting `evidence/stage5-k-inventory.log` contains 1,142
items:

- 705 rules: 695 supplied-semantics rules and 10 proof-local rules;
- 230 syntax declarations;
- 6 positive claims;
- 1 configuration and 5 contexts;
- all modules, imports, requirements, priorities, `owise` attributes,
  strictness declarations, `function`/`total` declarations, symbols, and
  simplifications.

`evidence/static_rule_assessment.py` gives one disposition to every one of the
705 rules, every syntax declaration, and every claim. Its run ends with
`rule_decisions=705 syntax_decisions=230 claim_decisions=6` and exit 0
(`evidence/stage5-static-rule-assessment.log`).

### Mapping of the submitted program

The constructor map covers `Module`, `FuncDef`, `Params`, `If`, `Compare`,
`Name`, `CmpOp`, `Int`, `Assign`, `UnaryOp`, `While`, `BinOp`, `AugAssign`,
and `Return`.

The used operational path was checked in:

- `syntax.k`: the corresponding AST productions, `strict` evaluation for
  unary operations, assignment, conditionals, augmented assignment and
  return, `seqstrict(2,3)` for binary operators, and the two comparison
  contexts;
- `core.k`: configuration, module/statement sequencing, local name lookup,
  argument evaluation, integer literals, Boolean truthiness and value-list
  accumulation;
- `call.k` and `functions.k`: callee-before-arguments evaluation, ordinary
  closure invocation, frame creation, parameter binding, return and exact
  frame pop;
- `controls.k`: ordinary assignment, integer augmented assignment, both
  conditional branches, `While/#while/#whileCond`, and loop resumption;
- `operators.k` and `int.k`: left-to-right dispatch, mathematical unary minus,
  addition, multiplication, less-than and equality.

The initial and final cells agree with the supplied configuration. No heap
allocation, output, exception, floating point, collection mutation, external
state, or unmodeled control operation occurs.

The fixed semantics contains 22 explicitly symbolic/opaque `no-evaluators`
declarations for float, sorting, and MD5 operations. None is referenced by the
program, postcondition, proof-local functions, bridge, or used control path.
There is no proof-local opaque symbol.

### Proof-local declarations and rules

There are no proof-local `functional` declarations. The four local symbols
are:

- `cubeOf(Int) [function,total]`: one unconditional exact cube equation;
- `cubeSearch(Int,Int) [function,total]`: three disjoint and exhaustive
  `<`, `=`, `>` equations. Recursion advances by one and terminates on every
  ground integer because cubes are unbounded above;
- `isCubeInt(Int) [function,total]`: disjoint/exhaustive negative and
  nonnegative equations;
- `iscubeClosure [function,total]`: one unconditional closed constructor
  equation checked against the submitted program.

The remaining proof-local rules are:

1. the guarded exit-equality simplification. Under `not (I^3 < A)`, integer
   trichotomy leaves equality (both sides true) or greater-than (both false);
2. the guarded finite-map deletion identity. If key `1` is absent from
   `REST`, deleting the explicit `1 |-> S` entry yields exactly `REST`;
3. the priority-40 operational loop bridge. Its priority only selects an
   already proved transition; its full match domain and state footprint are
   identical to the bridge-free connection theorem.

No guards overlap with disagreeing right sides, all `total` declarations have
coverage, and the only recursion descends toward a ground stopping comparison.
No local rule encodes a free answer, fabricates a result for an unmodeled
construct, or bypasses execution without a universal connection theorem.

### Operational continuation sensitivity

A fresh reachable context replaces the bridge's expected return comparison
with `Return(Bool(false))`. For `A=1,C=0`, fixed semantics must observe and
return this false value; a broadened bridge would instead return the true
`cubeSearch(1,0)`.

The same claim closed with `#Top` under both the bridge-free base definition
and the bridge-enabled final definition. This shows the bridge does not match
or discard the alternate continuation.

Evidence: `evidence/bridge-continuation-spec.k`,
`evidence/stage5-bridge-continuation-fixed.log`, and
`evidence/stage5-bridge-continuation-extended.log`.

I found no materially unsound rule, so there is no false-conclusion witness to
report against a purported unsoundness.

## 6. Fresh non-vacuity test

I did not reuse `candidate/spec-vacuity.k`. The fresh mutation requires input
`27` to return `false`, although `27 = 3^3` and the unmutated ground claim
returns true.

`kprove --dry-run` parsed and built this mutated spec successfully with exit 0
(`evidence/stage6-fresh-vacuity-build.log`). The actual proof then:

- executed the reachable entry state;
- reached `<k> true ~> .K </k>`;
- reported `WarnStuckClaimState` against the `false` destination;
- exited 1 for the expected unmet result obligation.

This is not a parser error, timeout, unrelated crash, or unreachable mutation.
Evidence: `evidence/fresh-vacuity-spec.k` and
`evidence/stage6-fresh-vacuity-proof.log`.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` definition plus the audited local equations and one
connected bridge, for every K integer `INPUT`, the normal lookup and call of
the exact submitted `iscube` closure reaches the Boolean
`isCubeInt(INPUT)` while restoring/preserving the specified state. The loop
summary is itself proved universally from the fixed semantics. This is a
result-constraining partial-correctness theorem over the full source-contract
integer domain.

### Trust and informal boundary

- **K toolchain and logic:** K 7.1.293, its Haskell prover, parser, generated
  strictness rules, and built-in mathematical `Int`, `Bool`, `Map`, and `List`
  theories are foundational trusted primitives.
- **Supplied semantics:** the byte-verified reference semantics is the selected
  benchmark operational model. I reviewed the complete inventory and the full
  used path. Its unused float/sort/MD5 opaque symbols do not influence this
  theorem.
- **Translator bridge:** byte identity under the trusted translator plus the
  constructor comparison and identity claim connect Python source to the term
  executed by the proof. This is stronger than trusting candidate prose, but
  it still trusts the supplied translator's intended AST mapping.
- **Operational bridge:** not an assumption. Its program-derived result and
  complete state transition are established by the separately built,
  bridge-free universal connection claim.
- **Intent bridge:** ordinary integer mathematics establishes that scanning
  nonnegative candidates in increasing order is true exactly for cubes and
  that sign normalization preserves cubeness. This is transparent and does
  not introduce an oracle or domain restriction.
- **Termination:** the requested K result is partial correctness. The proof is
  not advertised as a K total-correctness theorem. Informally, both the Python
  loop and ground `cubeSearch` terminate for each integer because candidate
  cubes are unbounded, although extreme inputs can take impractically long.
- **Testing:** the 3,815-input differential run and concrete K assertions are
  finite corroboration only. They are not used in place of the universal K
  theorem or bridge connection.
- **Canonical limitation:** the float-based canonical implementation disagrees
  with the literal unrestricted contract on sufficiently huge exact cubes.
  The generated implementation and theorem follow the prompt's exact
  integer-cube property; no proof domain was narrowed to hide this issue.

### Decision

The proof reconstructs cleanly, is non-vacuous and result-constraining, executes
the real translated function with a mechanically checked identity link, covers
all mathematical integers, and uses no unjustified result-bearing abstraction.
The sole execution bridge has a bridge-free universal theorem over its complete
context and passes body, value, state, and continuation sensitivity checks.
There is no material adequacy or soundness gap.

VERDICT: PASS
LEGITIMACY: LEGIT
