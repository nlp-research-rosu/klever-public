# Independent adversarial review: 151-double-the-difference

## Overall assessment

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted `solution.mpy` over arbitrary finite lists of the
supplied model's `Int` and `Float` values. I rebuilt both definitions from
source, proved the loop circularity and the entry theorem together with
`#Top`/exit 0, mechanically matched the proof closure body to a trusted
regeneration of `solution.mpy`, and rejected fresh body and result mutations.

The result is qualified rather than unreserved. The supplied model treats
`Bool` as disjoint from `Int`, so `[True]` returns 0 in K while both submitted
Python and the trusted canonical return 1. The formal precondition excludes
Bool. I do not treat Bool or nonstandard numeric classes as a material
narrowing of this HumanEval prompt's ordinary list-of-numbers domain, but the
CPython/model disagreement is real. Also, the proof-local dynamic-`Val`
dispatch equations are sound by exhaustive algebraic-sort cases, but the
fixed-only backend did not independently discharge that abstract case split;
the static Int connection claims did close.

The evidence index is `/audit-output/evidence/INDEX.md`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`;
- `semantics_mode`: `SUPPLIED_SEMANTICS`;
- problem `151-double-the-difference`;
- candidate `/candidate`;
- trusted inputs below `/reference`;
- generation records below `/generation-evidence`.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` is present. The candidate's
`reference-semantics/` has exactly the same 24 regular files. A recursive
entry-by-entry byte comparison found no missing, additional, changed,
mistyped, or symlinked entry. No symlink exists anywhere below `/candidate`,
`/reference`, or `/generation-evidence`.

I read all required pipeline-v3 records:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the one 540-record JSONL structured trace below
  `/generation-evidence/codex-trace/`.

Every recorded file hash checked by the independent script matches. The
structured trace's file hash also matches the per-file manifest in
`generation-result.json`. `/audit-campaign-lock.json` is byte-hash-correct and
its parsed object exactly equals the `audit_campaign` block embedded in
`audit-input.json`. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
the trusted mounts. All required proof artifacts are regular files.

The candidate's compiled definitions, logs, traces, and `PROOF.md` were treated
only as untrusted historical claims. No candidate cache or compiled definition
was reused.

Evidence:

- `/audit-output/evidence/provenance_check.py`
- `/audit-output/evidence/01-provenance.log`
- `/audit-output/evidence/trace_inventory.py`
- `/audit-output/evidence/01-trace-inventory.log`

Stage 1: pass; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt requires `double_the_difference(lst)` to sum the squares of positive
odd integers, ignore negative values and non-integers, and return 0 on an empty
list. Its examples require 10 for `[1,3,2,0]`, 0 for `[-1,-2,0]`, 81 for
`[9,-2]`, and 0 for `[0]`.

The trusted canonical uses a comprehension with:

```python
i > 0 and i % 2 != 0 and "." not in str(i)
```

The submitted solution uses an explicit loop, `isinstance(number, int)`,
positivity, oddness by `% 2 == 1`, and `number * number`. The extra local
`number = 0` initializes the loop target but cannot affect the returned
accumulator.

The candidate implementation matches the natural-language contract for
ordinary Python ints and floats. It uses unbounded Python integer arithmetic
and has no list-length bound.

### Trusted regeneration

I regenerated with:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

`cmp` exited 0. The submitted and trusted-regenerated MPY files are
byte-identical.

### Independent differential

`differential_test.py` imports the trusted canonical and scratch-copied
generated entry points separately. It exercised:

- all four documented examples;
- empty, negative odd/even, zero, positive even/odd, and mixed branch
  boundaries;
- ordinary floats, Bool, large integers, scientific-notation floats,
  infinity, and NaN;
- 2,500 deterministic generated lists, seed 151, lengths 0 through 12.

Across 2,517 cases there were zero candidate-versus-contract mismatches. There
were 583 candidate-versus-canonical mismatches. Those are caused by the
canonical's string heuristic rather than the candidate violating the stated
contract. For example, the canonical counts `1e-5` and positive infinity
because their string forms contain no decimal point; the candidate correctly
ignores those non-integers. Mixing such a float with a very large integer also
forces the canonical sum to a rounded float. These discrepancies are preserved
rather than hidden.

Both Python implementations return 1 for `[True]`. That agrees with CPython's
`bool`-as-`int` subclass behavior but differs from the supplied K model, as
discussed in Stages 4 and 7.

Evidence:

- `/audit-output/evidence/02-regeneration.log`
- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/02-differential.log`

Stage 2: candidate matches the stated contract; canonical edge discrepancies
and the Bool model boundary are documented.

## 3. Clean proof reconstruction

I copied only source artifacts and the trusted semantics to
`/tmp/audit-work/candidate-src`. The candidate's `runtime-kompiled/` and
`verification-kompiled/` directories were not copied or consulted. K reports
version 7.1.293.

Fresh LLVM build:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. The warnings about non-exhaustive supplied helpers such as
`mapStrVS`, `floorFI`, and `valSeqAt` concern unreachable constructs for this
program.

Fresh Haskell proof build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit 0. Its only warnings were unused variables in supplied `str.k`.

Reviewer-authored concrete programs were translated with the trusted
translator and run on the fresh LLVM definition. Empty, prompt, all branch,
mixed Int/Float, and large-Int cases ended with `.K`, `NoExc`, and exit code 0.
The separate Bool boundary program also confirms the supplied model's result
0 for `[True]`.

Positive proof commands:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
```

Output `#Top`, exit 0.

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Output `#Top`, exit 0. This command proves both claims as one dependency unit,
letting the whole-function claim use the loop circularity.

A diagnostic selection of only `SPEC.double-the-difference` was interrupted
after about 30 seconds because `--claims` removes the auxiliary loop
circularity from the proof set. That diagnostic is not the authored target
proof command and does not contradict the successful all-claims
reconstruction.

Evidence:

- `/audit-output/evidence/03-toolchain.log`
- `/audit-output/evidence/03-kompile-llvm.log`
- `/audit-output/evidence/03-kompile-haskell.log`
- `/audit-output/evidence/03-concrete-execution.log`
- `/audit-output/evidence/03-kprove-loop-invariant.log`
- `/audit-output/evidence/03-kprove-all.log`
- `/audit-output/evidence/03-kprove-target.log`

Stage 3: pass.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` starts at a stable loop head with:

- remaining iterable `list(VS)`;
- current local accumulator `S`;
- prior local target `OLD`;
- the exact function and local scopes;
- precondition `numericVals(VS)`.

It claims that consuming the suffix finishes the loop, changes `result` to
`S + dtd(VS)`, and changes `number` to the last suffix value, or leaves it as
`OLD` for an empty suffix. It frames the continuation and omitted
configuration cells. A concrete satisfying state is
`VS=.ValSeq`, `INPUT=.ValSeq`, `OLD=0`, `S=0`, with the displayed scopes.

`SPEC.double-the-difference` starts with an ordinary call to the exact
`double_the_difference` closure in an otherwise initial configuration.
`numericVals(VS)` requires every arbitrary finite list element to be a model
Int or Float. The postcondition requires the returned `<k>` value to be
`dtd(VS)` and pins the module scope, scope allocator, heap, heap allocator,
stack, return state, exception state, and exit code back to their initial
values. A satisfying witness is `VS=.ValSeq`; both formal result and actual
result are 0.

`dtd` is not free: it is a total structural definition. Empty is 0, a model
Float contributes 0, and an Int contributes its square exactly when positive
and odd. Hence the postcondition is result-constraining.

### Mechanical source pinning

The entry claim does not execute the top-level `Module/FuncDef` loader. It
instead pins the exact function name, parameter list, defining scope, and
closure body. This is allowed only if that closure really is the regenerated
program.

I parsed two complete modules with the fresh definition and
`kast --expand-macros --output kore`:

1. the trusted-regenerated `solution.mpy`;
2. the same function binding using proof macro `dtdBody`.

The expanded KORE files are byte-identical and share SHA-256
`fed72e387cf57cf206f9dad4c410f9293a71cccc89f0d4c1dd64ec6c7949593d`.
Thus the claim executes the submitted binding and body, including both
initial assignments, nested guards, multiplication, loop, and return.

The fixed semantics expressly permits bare `list(VS)` values as read-only claim
inputs. The source does not mutate the argument, so this representation does
not omit a material state effect.

### Concrete substitution and sensitivity

Ground `dtd` claims and both Python functions agree:

- `[] -> 0`;
- `[-3,-2,-1,0,1,2,3] -> 10`;
- `[1.5,3,-5,7.0,5] -> 34`.

A fresh body mutation changed multiplication to addition in the actual inline
closure term. It parsed successfully and executed to 2 on `[1]`; the original
required result 1 was rejected with `WarnStuckClaimState`. This is genuine body
sensitivity, not a mutation of an external file ignored by the claim.

The theorem is unbounded: symbolic `ValSeq` ranges over all finite algebraic
lists, not fixed examples or bounded unrolling.

The known adequacy limitation is Bool. In the supplied semantics,
`isIntV(true)` is false; the formal precondition also excludes Bool. In
CPython, the submitted and canonical functions count `True`. Bool and numeric
classes absent from the supplied semantics are not part of the material
ordinary Int/Float contract proved here, but this prevents claiming full
CPython equivalence.

Evidence:

- `/audit-output/evidence/04-constructor-identity.log`
- `/audit-output/evidence/04-proof-body.mpy`
- `/audit-output/evidence/04-witness-values.k`
- `/audit-output/evidence/witness_compare.py`
- `/audit-output/evidence/04-witnesses-config.log`
- `/audit-output/evidence/04-audit-body-mutation.k`
- `/audit-output/evidence/04-body-sensitivity-inline.log`

Stage 4: real-program pinning passes; CPython Bool equivalence is excluded.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and fixed semantics

`rule_inventory.py` inventories every source declaration in
`reference-semantics/semantics.k`, all 23 helper K files, `verification.k`, and
`spec.k`. The inventory contains:

- 718 rules;
- 231 syntax declarations;
- five contexts;
- one configuration;
- two claims;
- all modules, imports, and requires.

Each row records attributes including `function`, `total`, `functional`,
`macro`, `no-evaluators`, `symbol`, `priority`, `simplification`, `concrete`,
`symbolic`, `owise`, `preserves-definedness`, and strictness. It distinguishes
the fixed executed slice from fixed constructs unreachable by this program.
All fixed rows are byte-identical to the trusted supplied baseline. Fixed
unreachable rules cannot introduce a term on this program's path because no
used constructor or rule produces their labels.

Program-to-semantics mapping:

| Program construct | Declaration/behavior |
|---|---|
| function binding/body | `syntax.k` `FuncDef`, `functions.k` closure binding; the claim pins the resulting closure |
| `Call`, name lookup, arguments | `call.k` callee route and closure-frame rule; `core.k` `#look` and left-to-right `#evalArgs` |
| `Assign`, `AugAssign` | `controls.k` scope updates |
| `For` over a list | `controls.k` `#loop/#loopStep`; `list.k` `#iterNext/#iterYield/#iterDone` |
| nested `If` | syntax strictness plus `controls.k` `#branch` and `core.k` Bool truthiness |
| `isinstance(_, int)` | normal lookup of `builtinV("isinstance")`, `call.k` dispatch, `builtins.k` `isIntV` |
| `>`, `%`, `==`, `*`, `+` | `operators.k` evaluation/dispatch and `int.k` arithmetic, comparison, and `pyMod` |
| `Return` | `functions.k` `retV`, `#pop`, environment restoration and frame deallocation |

The used fixed rules preserve evaluation order, bindings, scope allocation,
the call stack, return state, heap, exception state, and exit code. There is no
proof-local priority rule and no proof-local rule that matches a `<k>` program
configuration.

The supplied opaque symbols are:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`.
None is reachable from this submitted body: Float inputs are only classified
and skipped; they never undergo Float arithmetic or comparison.

### All 23 proof-local rules

The detailed individual ledger is
`/audit-output/evidence/05-proof-local-review.md`. Its conclusions are:

1. `numericVals`, `dtd`, `oddIntSquare`, and `lastNumber` are terminating,
   exhaustive structural definitions. Int, Float, and `[owise]` cases are
   disjoint; the guarded dynamic `dtd` simplifications overlap the static cases
   only with equal right-hand sides.
2. `definedProjectInt`, the cast-`#Ceil` equation, and guarded
   `projectIntTotal` equations totalize the built-in `Val`-to-`Int` projection.
   `projectIntTotal` is opaque only off the Int domain. Every value-influencing
   use is guarded by `isInt`; Int collapse and idempotence fix its used value.
3. `isIntV` and the guarded dynamic `applyCmp/applyBin` rules are exact
   case-compressions of supplied static Int rules. The comparison, modulo, and
   multiplication operator names and operand order match the source.
4. `dtdLoopBody` and `dtdBody` are compile-time macros, mechanically shown to
   expand to the exact submitted constructors. They do not bypass execution.

A fresh fixed-only Haskell definition, importing no candidate extension,
proved universal static Int connection claims for `isIntV`, `>`, `%`, and `*`
with `#Top`. A stronger formulation over abstract `V:Val` and guard
`isInt(V)` became stuck because the backend did not derive the algebraic sort
case split. This is not a false-conclusion witness: exhaustive ground Val
constructors make `isIntV(V) = isInt(V)`, and the cast is defined exactly for
the Int injection. I record the missing bridge-free abstract proof as a
mechanization/evidence limitation.

The opposite interpretation `projectIntTotal(3) => 4` built and was rejected;
execution left 3. There is no result-bearing oracle, task-answer rule,
operational shortcut, fabricated return, or unconstrained postcondition.

No inventoried proof-local rule is labelled unsound. Accordingly, there is no
required false-conclusion witness for an unsoundness allegation.

Evidence:

- `/audit-output/evidence/rule_inventory.py`
- `/audit-output/evidence/05-rule-inventory.tsv`
- `/audit-output/evidence/05-rule-inventory-summary.log`
- `/audit-output/evidence/05-proof-local-review.md`
- `/audit-output/evidence/05-fixed-only.k`
- `/audit-output/evidence/05-fixed-connection-spec.k`
- `/audit-output/evidence/05-fixed-connection-build.log`
- `/audit-output/evidence/05-fixed-connection-proof.log`
- `/audit-output/evidence/05-fixed-connection-dynamic.log`
- `/audit-output/evidence/05-projection-opposite.k`
- `/audit-output/evidence/05-projection-opposite.log`

Stage 5: sound on the complete claim domain, with the stated abstract-sort
mechanization limitation.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` and created
`audit-spec-vacuity.k`. It retains the actual loop circularity and changes the
entry result from `dtd(VS)` to the false `dtd(VS) +Int 1`.

The exact empty-list initial configuration satisfies the precondition:
`numericVals(.ValSeq) = true`, the true return is 0, and the mutation requires
1.

Dry run:

```text
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

Exit 0, proving the mutation parses and builds.

Actual proof:

```text
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
```

Exit 1 with `WarnStuckClaimState`. The residual is the expected unmet
obligation:

```text
dtd(VS) +Int 1 #Equals dtd(VS)
```

This is a reached false result obligation, not a parser error, timeout,
unrelated crash, or unreachable mutation.

Evidence:

- `/audit-output/evidence/06-audit-spec-vacuity.k`
- `/audit-output/evidence/06-fresh-vacuity.log`

Stage 6: pass.

## 7. Proven versus assumed accounting

### Formally established

Under the unchanged supplied semantics plus the audited proof-local
definitions, for every arbitrary finite `ValSeq` containing only model Ints and
Floats, an ordinary call to the exact submitted
`double_the_difference` closure from the displayed initial configuration
reaches return value:

```text
sum(I * I for each model Int I in order when I > 0 and pyMod(I,2) == 1)
```

Model Floats contribute zero. Call lookup, parameter binding, the exact body,
loop iteration, all guards and integer operations, accumulator updates, return,
frame cleanup, and all pinned cells execute under fixed rules. This is a
partial-correctness theorem, not a separate liveness theorem or a universal
full-CPython equivalence theorem.

### Trusted or informal boundaries

1. **Supplied MPY semantics.** The 24 exact trusted files define the language
   model. Every target claim depends on their configuration, calls, scopes,
   iteration, operations, and returns. This is the required benchmark trust
   boundary, not candidate-authored semantics.
2. **K implementation.** K 7.1.293, kompilers, Haskell reachability backend,
   LLVM concrete backend, solver, and proof checker are trusted.
3. **K built-ins.** Unbounded Int/Bool arithmetic, Map/List operations,
   generated `isInt`/`isFloat` predicates, subsort injections/casts, equality,
   and definedness are trusted mathematical/runtime primitives.
4. **Proof-local total projection.** `projectIntTotal` is arbitrary off the Int
   domain but fixed to the built-in cast on every used path. No off-domain
   value reaches control, state, result, `dtd`, or a postcondition.
5. **Dynamic-Val case argument.** Static fixed connections are
   machine-checked. The abstract-`Val` lifting is justified by exhaustive
   algebraic sort cases but was not independently closed by the fixed backend.
   This is a non-fatal evidence limitation.
6. **Bare list input representation.** The fixed semantics designates bare
   `list(VS)` as the read-only representation for symbolic claim inputs. The
   source does not mutate or expose identity, making this bridge adequate here.
7. **CPython intent bridge.** Differential tests are finite evidence only.
   They support ordinary Int/Float agreement but do not make the K theorem a
   full CPython theorem. Bool is a demonstrated disagreement; Decimal,
   Fraction, list subclasses, and numeric classes absent from the supplied
   model are not covered.
8. **Unused opaque supplied symbols.** All 22 are inventoried in Stage 5 and
   have no dependent target path or claim.

There is no empirical bridge used to make the K reachability claim close.
Python differential and LLVM concrete runs support fidelity and model-boundary
analysis only; neither substitutes for `kprove`.

### Decision

Gate A passes: the proof is sound, body-sensitive, and non-vacuous. Gate B
covers the material unbounded Int/Float source-contract domain. The Bool/Int
CPython disagreement and the unclosed fixed-only abstract-sort connection
probe are non-fatal trust/evidence limitations, so the proof remains
legitimate but warrants concerns rather than an unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
