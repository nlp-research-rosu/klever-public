# Independent adversarial review: 22-filter-integers

## Audit conclusion

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied MPY model. A clean Haskell definition
rebuilt from trusted source closes the complete two-claim specification with
`#Top`; the claim executes the exact macro-expanded function body; the result is
fixed to a structurally recursive stable filter; and fresh false-result and
real-body mutations are rejected with the expected terminal heaps.

The result is not an unconditional proof over CPython's complete
`List[Any]` universe. The supplied, read-only `Val` grammar has no representation
for user-defined classes or `int` subclasses. The candidate explicitly records
that supplied-model boundary in its trust ledger and supplies
`IntegerSubclass(9)` as a concrete witness; both the canonical and submitted
Python functions retain that value. The theorem covers every `ValSeq` the fixed
model can express and imposes no candidate-created length or element
restriction. Campaign amendment v2 therefore maps this supplied-model
representation gap to `CONCERNS / LEGIT`, not to `FAIL`.

There is one additional, non-fatal auditability limitation. The proof-local
classifier simplification is true by constructor/sort exhaustion, and 22
constructor-family claims close using a fixed-semantics-only definition. A
single generic fixed-semantics connection claim over abstract `V:Val` remains
stuck because the supplied `isIntV` uses an `owise` equation that does not split
an abstract value. There is no false-conclusion witness; this is an absent
generic automation result, not evidence that the equation is unsound.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `22-filter-integers`, and
condition `kit-semantics`. `/reference/reference-semantics` is present, as this
mode requires.

All required pipeline-v3 records are present as regular files or real
directories:

- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`
- the structured trace
  `codex-trace/2026/07/29/rollout-2026-07-29T23-54-30-019fb15f-c25c-7aa1-8668-51ba3768aa4e.jsonl`

The trace contains 539 valid JSONL records and no malformed record. Its
function/custom-tool calls and agent messages were independently extracted to
`evidence/04-trace-actions.log`. Generation statements such as the prior
`VALIDATED` and `#Top` claims were treated only as untrusted history.

Integrity findings:

- The SHA-256 of `/audit-campaign-lock.json` is
  `e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`,
  exactly the value in `/audit-input.json`. Its parsed JSON is exactly equal to
  the embedded `audit_campaign` object.
- Every independently hashed required record matches its per-file recorded
  digest. The trace file itself hashes to
  `4384190d8552b47e936a4aa83d44fb58fe77a9c1024762ca1bb325bb217b5a7b`.
- Applying the pipeline's deterministic tree-digest algorithm directly to the
  mounts gives
  `be9f9438f18810c0e041553821068b75395ebd650b74d68f8826decc388b475c`
  for `/candidate`, exactly the generation result's workspace digest;
  `e017e7ddcdccc327e74147cf909748f8d5f3a5af556133d79bb556c08f867cb0`
  for each supplied-semantics tree, exactly the task-manifest digest; and
  `25d0673e23e897ff3b2a125151e43112147b228e1ad8725d306c7e2f4ee18560`
  for the trace tree, exactly `usage.json`'s source-trace digest. The launcher
  also records separate snapshot digests; the independent mounted-content
  checks do not rely on that opaque aggregate convention.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `b7bde4…b32`), and `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (SHA-256 `406485…b16`).
- `diff -qr --no-dereference` between the candidate and trusted
  `reference-semantics/` trees exits 0. There are no missing, additional,
  mistyped, non-regular, or symlinked entries.
- The required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are present as
  regular files. Candidate-built `runtime-kompiled/` and
  `verification-kompiled/` were never copied or used.

Exact hashes, comparisons, record summaries, and source listings are in
`evidence/01-record-hashes.log` through
`evidence/06-scratch-copy.log`, plus
`evidence/29-recorded-tree-hashes.log`. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks `filter_integers(values: List[Any])` to return, in
original order, only those elements that are Python integers. The trusted
canonical implementation is:

```python
return [x for x in values if isinstance(x, int)]
```

Consequently, CPython `bool` values and instances of user-defined `int`
subclasses are retained; non-integer objects are discarded. Both documented
examples follow that rule.

The candidate uses a result list, loops over every input element, appends the
element exactly when `isinstance(value, int)` is true, and returns the result.
It is algorithmically different only in using an explicit loop.

The trusted translator was copied to scratch and run as:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -l solution.regenerated.mpy solution.submitted.mpy
```

`cmp` exits 0. Both MPY files have SHA-256
`7f50d61e2d2bdfd5126b5b701e8abe222e80fa4e7d87cdccbc8039da1df30e28`.

`evidence/independent_differential.py` independently imports the trusted
canonical and submitted entry points from scratch. It checks the two examples,
empty and branch-boundary placements, `bool`, huge positive/negative integers,
`None`, containers, and an `int` subclass; exhaustively checks all 22,621 lists
of lengths 0–4 over a 12-value mixed pool; and checks 2,000 deterministic random
lists of lengths up to 40. It also compares retained object identities and
order. The command exits 0 with:

```text
documented_boundary_cases=12 exhaustive_lists=22621 random_lists=2000 mismatches=0
```

See `evidence/07-translation-and-differential.log`. There is no
canonical-versus-docstring contradiction.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/reconstruction`: trusted
semantics, translator, prompt, and canonical, plus the candidate's
`solution.py`, submitted MPY text, `verification.k`, and `spec.k`. No compiled
candidate definition or cache entered the reconstruction.

The live tools are K `v7.1.293`; `kompile`, `krun`, and `kprove` are
independently installed at `/usr/bin`. The following clean commands were run.

Concrete definition and independent execution:

```text
python3 py2mpy.py /audit-output/evidence/independent_concrete_tests.py \
  > independent_concrete_tests.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun independent_concrete_tests.mpy --definition audit-runtime-kompiled
```

The LLVM build exits 0. The concrete harness contains an AST-identical copy of
the submitted function and assertions for both examples, empty input, mixed
values, `bool`, and branch ordering. `krun` exits 0 with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.

Proof definition and positive target:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Both commands exit 0, and the complete spec prints `#Top`. The isolated
`SPEC.filter-loop` claim also exits 0 and prints `#Top`. An entry-only
diagnostic was interrupted after filtering out `SPEC.filter-loop` also removed
the circularity on which the entry proof depends; it is not a target-proof
failure. The actual positive target command loads both claims together, as K
requires for this auxiliary circularity, and closes both. The interruption and
exit 130 are preserved rather than hidden.

Build and proof outputs are in:

- `evidence/09-concrete-build.log` and `10-concrete-run.log`
- `evidence/11-proof-build.log`
- `evidence/12-positive-all-claims.log`
- `evidence/13-positive-filter-loop.log`
- `evidence/14-positive-filter-entry.log` (the diagnostic interruption)

The compiler reports several supplied-semantics non-exhaustiveness warnings
(`mapStrVS`, float conversion helpers, `joinCodes`, and out-of-bounds
`valSeqAt`) and unused-variable warnings. None of those helpers is reached by
this program or its postcondition.

## 4. Adequacy and real-program pinning

### Entry claim

`SPEC.filter-entry` has no length or element-type `requires` clause.
`INPUT:ValSeq` ranges over every finite algebraic sequence of values represented
by the supplied model. The initial state:

- executes `Call(Name("filter_integers"), (list(INPUT), .Exprs))`;
- binds that name in module scope 0 to a one-argument closure with
  `filterBody`;
- starts with the fixed builtins scope, empty heap, allocator 0, empty stack,
  `noRet`, `NoExc`, and exit code 0.

The post-state must contain `ref(0)`, allocate exactly heap location 0 as
`list(filterAcc(INPUT, .ValSeq))`, increment the heap allocator to 1, and
restore the caller's environment, scopes, stack, return, exception, and exit
cells. The result is not a free existential or an implication: its complete
sequence is fixed by `filterAcc`.

### Loop claim

`SPEC.filter-loop` starts at the real `#loop` control state with an arbitrary
finite remaining sequence, arbitrary accumulated result, the exact loop body,
and the exact continuation `Return(Name("result")) ~> #endcall`. It requires
the actual function frame, bindings, heap result object, allocator, stack
frame, and clean control cells. It finishes the loop, returns `ref(0)`,
deallocates the function scope, pops the exact frame, and changes the heap
result from `ACC` to `filterAcc(REST, ACC)`.

`ORIGINAL` and `OLD` are intentionally unconstrained and unused: after the
iterable has been evaluated, neither the original `values` binding nor the
previous loop-target value affects the remaining execution. The entry proof
executes the first constructor step before the circularity can match, then
reuses the loop claim only after semantic progress.

### Mechanical identity

A reviewer-created module binds `filter_integers` to `filterBody`. Both it and
the trusted regeneration of `solution.mpy` were parsed with the clean
definition using:

```text
kast ... --module VERIFICATION --expand-macros --output json
```

The two expanded constructor JSON files are byte-identical, with SHA-256
`4f94ef91027cb429f41fa4e06e7f5bcae3cc839753de72a64617939804a7489b`.
This includes the exact function name, parameter, docstring statement,
allocation, loop, classifier call, append, return, and typing import. The
typing-only import has no material effect on this function. An initial parser
diagnostic used the syntax module, which does not expose semantic macro
equations; that non-identity is preserved in
`evidence/15-program-pinning-kast.log`. Repeating with the semantic module
performs the intended expansion and proves identity in
`evidence/16-program-pinning-kast-corrected.log`.

### Satisfiable witnesses

`evidence/spec-ground-witnesses.k` instantiates the exact entry state with
`[]` and with model input `[1, noneV, true, -2]`. Both finite claims close
together with `#Top`. The corresponding Python inputs produce:

```text
[]                         -> []
[1, None, True, -2]        -> [1, True, -2]
```

for both trusted canonical and submitted functions, exactly matching the
formal heaps. See `evidence/17-ground-witness-proofs.log` and
`evidence/18-ground-witness-python.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` inventories every `configuration`, syntax or
function declaration, context, rule, simplification, priority/`owise` rule,
and claim in the 24 supplied K source files, `verification.k`, and `spec.k`.
The line-addressable result is
`evidence/k-declaration-rule-inventory.tsv`; every row is annotated with target
relevance and audit disposition in `evidence/k-rule-audit.tsv`.

The inventory contains 991 records:

- 981 supplied-semantics records and 10 proof-local records;
- 244 syntax declarations, including 160 function declarations;
- 739 rules: 681 ordinary, 28 `owise`, 29 priority, and one simplification;
- five contexts, one configuration, and two claims;
- 114 occurrences of `total`, 49 `concrete`, 29 named `symbol` productions,
  and no literal `[opaque]` attribute.

The row-by-row dispositions are: 128 target-slice records, 20 `Val`/`Iterable`
domain declarations, 10 proof-local records, 49 concrete-only unused records,
24 no-evaluator declaration records, and 760 other supplied records whose
labels are absent from both the expanded target and its summaries. This is an
exhaustive inventory, not a claim that the intentionally partial MPY language
is a full Python semantics.

### Used-construct map and operational review

The submitted MPY uses `Module`, `ImportFrom`, `FuncDef`, `Params`, `Expr`,
`Str`, `Assign`, `Name`, `ListExpr`, `For`, `If`, `Call`, `Attribute`, and
`Return`. The relevant declarations and rules are:

- `semantics/syntax.k`: constructor declarations and strict/sequence-strict
  evaluation annotations;
- `core.k`: the complete configuration, allocation, module sequencing, lexical
  lookup, left-to-right argument evaluation, truthiness, and sequence helpers;
- `functions.k` and `call.k`: closure selection, binding, stack-frame creation,
  return, frame cleanup, builtin and bound-method dispatch;
- `controls.k`: assignment, inert typing import, expression discard, branch,
  and `#loop` control;
- `list.k` and `tuple.k`: iteration, list allocation, target binding,
  `valSeqConcat`, and the in-place `append` heap update;
- `builtins.k`: `isinstance(_, int)` and the fixed `isIntV` equations.

Name lookup fixes both `isinstance` and `int` through the supplied builtins
scope; no proof rule chooses a binding textually. Callee and arguments evaluate
left to right. The result list allocates at 0, append updates that same heap
cell, and return preserves the returned reference while restoring the exact
caller control state. The loop claim admits no arbitrary continuation: it pins
`Return(result) ~> #endcall`. No proof-local priority rule preempts any of this
execution.

### Proof-local extension decisions

1. `filterLoopBody` and `filterBody` are syntax macros. They read or write no
   runtime cell. Correct semantic-module expansion establishes exact
   constructor identity with the submitted program.
2. `filterAcc` is a definitional mathematical summary, not an operational
   bridge. Its empty and `vCons` equations exhaust `ValSeq`; recursion strictly
   descends through `REST`; the accumulator is extended by the same supplied
   `valSeqConcat` operation used by `append`. It fixes membership and order.
3. `isIntV(V) => isInt(V) orBool isBool(V) [simplification]` is
   result-bearing but truthful. The fixed equations classify `Int` and `Bool`
   as true and all other `Val` constructors as false. The generated sort
   predicates state exactly that split. Guards do not overlap with conflicting
   right-hand sides, and there is no new opaque result.
4. `filter-loop` is an auxiliary circularity over exact real control and state,
   not a rewrite rule or oracle. `filter-entry` invokes the exact closure and
   fixes the observable result and all control cells.

A fixed-semantics-only Haskell definition was separately built. The generic
abstract classifier connection:

```text
<k> isIntV(V:Val) => isInt(V) orBool isBool(V) </k>
```

gets a meaningful implication-check residual because fixed `owise` evaluation
does not split `V`. It does not prove a contrary case. A second fixed-only spec
exhausts 22 data-constructor families (`Int`, `Bool`, `noneV`, every iterable,
references, closures, type/builtin/method values, keyword/cell markers, float,
set, dict, and md5 values); it exits 0 with `#Top`. Together with the sorted
signature inspection, this establishes the equation's truth, while the missing
single generic connection theorem remains the evidence limitation noted in the
conclusion. See `evidence/20-fixed-proof-build.log`,
`21-classifier-connection-proof.log`, and
`28-classifier-constructor-cases.log`.

No inventoried candidate rule encodes the requested output, replaces
program-defined execution with an oracle, fabricates a used operation, or can
be given a false-conclusion witness on the intended modeled domain.

### Supplied opaque/trusted symbols

The supplied tree contains named proof-domain primitives:

- `builtins.k`: `md5hexCodes`;
- `sort.k`: `sortVS`, `sortKeyVS`;
- `float.k`: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
  `gtF`, `eqF`, `floatFinite`, `ltFI`, `ltIF`, `eqIF`, `decStrToF`,
  `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.

None is called or appears in `filterAcc` or either postcondition. A `Float`
value may occur as an input element, but filtering it uses only its outer sort
and the fixed classifier; no opaque float operation is evaluated. Thus these
primitives are part of the global supplied trust boundary but have no value,
control, state, or result influence on this theorem.

## 6. Fresh non-vacuity test

The fresh mutation `evidence/spec-auditor-false.k` uses the satisfiable entry
state for `[1, noneV, true, -2]` but deliberately claims the output is
`[1, -2]`, incorrectly dropping `true`.

First:

```text
kprove spec-auditor-false.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDITOR-FALSE --dry-run
```

exits 0, establishing that the mutation parses and builds. The actual proof
command exits 1 with `WarnStuckClaimState`. Its terminal residual has
`<k> ref(0) ~> .K </k>` and:

```text
0 |-> list(vCons(1, vCons(true, vCons(-2, .ValSeq))))
```

which is precisely the unmet result obligation. See
`evidence/24-false-mutation-build.log` and
`evidence/25-false-mutation-proof.log`.

A separate body-sensitivity spec changes the closure term actually executed by
removing the `For` statement. It builds successfully and then exits 1 with
`WarnStuckClaimState`: the mutated closure returns `[]` where `[1]` is required.
This is not the invalid experiment of changing only an external source file;
the closure body inside the claim is materially different. See
`evidence/26-body-sensitivity-build.log` and
`evidence/27-body-sensitivity-proof.log`.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied MPY semantics and proof infrastructure, for every
finite `INPUT:ValSeq`, if the exact submitted `filter_integers` call reaches
the specified return state, it returns a fresh list reference whose sequence is
the stable filter of `INPUT` by the supplied `isinstance(_, int)` classifier.
Every represented `Int` and `Bool` is retained; every other represented value
constructor is discarded; relative order and object terms are preserved. The
call restores environment, scope allocator, stack, return state, exception
state, and exit code as stated. This is partial correctness, not a separate
resource bound or liveness theorem.

### Trust ledger

- **Trusted supplied semantics:** all fixed MPY declarations and rules,
  especially configuration, calls, lookup, allocation, loop control, append,
  return, and `isIntV`. They determine execution and all observable cells.
- **Trusted K infrastructure:** K 7.1.293, the parser/kompiler, LLVM and Haskell
  backends, Kore reachability engine, builtin integer/Boolean/string/map/list
  theories, generated sort predicates, and circularity discipline. Every
  machine result depends on this boundary.
- **Trusted translator:** `/reference/py2mpy.py`. The submitted MPY is
  byte-identical to its fresh output, so no informal source-to-MPY rewrite is
  hidden.
- **Proof-local mathematical definitions:** exact-body macros and `filterAcc`
  are checked rather than assumed. The classifier simplification is supported
  by fixed equations, sorted-constructor exhaustion, 22 fixed-only constructor
  proofs, and opposite-result mutations. Its single generic fixed-only
  connection theorem does not close, so universal automation is not claimed.
- **Unused opaque supplied primitives:** the 29 symbols listed in stage 5.
  They have no dependent target claim path.
- **Empirical CPython bridge:** differential testing is finite evidence that
  the submitted Python function matches canonical CPython behavior. It does
  not replace the K proof.
- **Representation boundary:** MPY has no user-class or subclass value
  constructor. `/candidate/PROOF.md` explicitly identifies user-defined
  classes and arbitrary subclasses as fixed-model exclusions and points to a
  CPython `int`-subclass test. `/candidate/differential-test.py` defines
  `IntegerSubclass(int)` and includes `IntegerSubclass(9)`; its zero-mismatch
  result entails that both its independent MRO oracle and submitted program
  retain the witness. The independent auditor test repeats that behavior
  against canonical. This is model-versus-CPython divergence in
  representability, not program-versus-canonical divergence.

### Gate and benchmark mapping

- Gate A, real-program soundness: **PASS**. The proof is result-constraining,
  executes the exact submitted body, has no unsound operational bridge or
  oracle, and rejects both result and body mutations.
- Gate B, intent adequacy: **limited only by the supplied representation
  boundary**. The formal theorem is unbounded and covers all values the fixed
  model represents. Under generic Kit terminology this prevents an
  unconditional full-CPython `VALIDATED` report.
- Gate C, auditability: evidence is reproducible and the trust boundary is
  explicit. The absent one-shot generic classifier connection theorem is
  recorded as a non-fatal evidence limitation; fixed-only constructor proofs
  and ordinary sorted-signature reasoning establish soundness.

Campaign amendment v2 applies because the domain gap originates solely in the
supplied read-only model, the theorem adds no narrowing, the candidate
documents the boundary with a concrete subclass witness, and the submitted
Python is canonical-faithful on that witness and throughout independent
testing. The correct benchmark mapping is therefore concerns but legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
