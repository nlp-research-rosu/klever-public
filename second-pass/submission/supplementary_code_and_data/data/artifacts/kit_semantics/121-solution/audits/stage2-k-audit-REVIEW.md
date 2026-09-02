# Independent adversarial audit — HumanEval/121 `solution`

## Overall finding

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full material source-contract domain: every non-empty finite
list of mathematical integers, with no list-length or integer-magnitude bound.
The positive claims reconstruct from source, the only operational bridge has a
bridge-free universal connection claim over the same context and state
footprint, the entry claim executes the exact translated function body, and a
fresh false-result mutation is rejected for the expected semantic reason.

Candidate prose, candidate compiled directories, and candidate logs were not
used as proof authority.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `121-solution`, and condition
`kit-semantics`. The rendered mode is consistent with the mounts:
`/reference/reference-semantics` exists as the required trusted tree.

The audit campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, and the independently computed lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. The generation run and audit campaign record
separate generator/auditor Kit revisions; that is provenance separation, not a
campaign-lock mismatch.

I inspected all required pipeline-v3 records:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured trace under `/generation-evidence/codex-trace`.

All are real regular files. Every directly recorded file SHA-256 in
`/audit-input.json` matches. The one structured trace file has the recorded
SHA-256
`8f7ea06860c038326b252a3869c16832368c383fc5c8e9403324d7d4e3d3d31d`;
all 562 JSON Lines parse, with one start and one completion event and no parse
errors. The generation records claim success and `#Top`, but those claims were
not relied on below.

Independent pipeline-v3 tree digests also match:

- candidate tree:
  `3d5522e3291a1045d1bb4bb13796ad5c916b05b6f4a45e19aa8b41bf86b5a253`;
- candidate and trusted semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- trace tree:
  `e105a9786810ba2da597e740c1af1669aa9e69c249319d83bc3dbf395e2dcec9`.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive, type-sensitive
manifest comparison of `/candidate/reference-semantics` against
`/reference/reference-semantics` found the same 25 entries, identical file
sizes and hashes, no extra or missing entries, and no symlinks or unsupported
types. All six required candidate proof artifacts are regular files.

Evidence:

- [stage1_integrity.py](evidence/stage1_integrity.py) and
  [stage1_integrity.log](evidence/stage1_integrity.log)
- [stage1_tree_records.py](evidence/stage1_tree_records.py) and
  [stage1_tree_records.log](evidence/stage1_tree_records.log)

Stage 1 result: PASS. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`: for a non-empty list of integers, return the sum
of precisely those odd-valued elements whose zero-based positions are even.
The examples require `12`, `9`, and `0` for the three documented inputs.

`/reference/canonical.py` implements this with `enumerate`, a comprehension,
and `sum`. `/candidate/solution.py` uses an accumulator and a zero-based
position counter. It initializes both to zero, iterates once over every input
element, adds the element exactly when both parity tests hold, increments the
position once, and returns the accumulator. This is a different but faithful
algorithm.

Using the trusted translator copied into `/tmp/audit-work/reconstruction`, I
ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0. Submitted and regenerated MPY both hash to
`bbb0ba552615ee6e36f623d4703b698f5685d8ae9ff2804a2dfe8b7b625ecb7e`;
`cmp` exited 0.

The independent differential script loads the copied trusted canonical entry
point and copied candidate entry point. It ran:

- all three documented examples;
- 12 explicit empty, singleton, parity, negative, and huge-integer boundaries;
- every list of lengths 0 through 6 over values `[-3, 3]` (137,257 cases);
- 5,000 deterministic random lists of lengths 1 through 100, including
  large-magnitude edge values.

Total: 142,272 cases; mismatches: 0. The empty case is additional robustness
evidence and is not used to broaden the formal non-empty contract. The complete
deterministic JSONL input stream is preserved with SHA-256
`753b52adf906f5f4a9b2f60c539e7e5c329dba79329df3867acba4ae9e54fb4e`.

Evidence:

- [stage2_translation.log](evidence/stage2_translation.log)
- [stage2_differential.py](evidence/stage2_differential.py),
  [stage2_differential.log](evidence/stage2_differential.log), and
  [stage2_inputs.jsonl](evidence/stage2_inputs.jsonl)

Stage 2 result: PASS.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`.
Candidate `runtime-kompiled`, `verification-base-kompiled`,
`verification-kompiled`, caches, binaries, and prior outputs were neither
copied nor used. The supplied semantics in scratch came from the trusted
reference tree.

With K 7.1.293, the following fresh commands and outcomes were recorded:

| Command | Outcome |
|---|---|
| `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition auditor-runtime-kompiled` | exit 0 |
| `kompile --backend haskell verification-base.k --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition auditor-verification-base-kompiled` | exit 0 |
| `kprove connection-spec.k --definition auditor-verification-base-kompiled --spec-module CONNECTION-SPEC` | exit 0, `#Top` |
| `kprove projection-positive.k --definition auditor-verification-base-kompiled --spec-module PROJECTION-POSITIVE` | exit 0, `#Top` |
| `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition auditor-verification-kompiled` | exit 0 |
| `kprove spec.k --definition auditor-verification-kompiled --spec-module SPEC` | exit 0, `#Top` |

The two ground projection claims were reported by `kore-exec` as trivial after
simplification; they are supporting checks, not the substantive connection.
The bridge-free symbolic loop connection and the full symbolic entry claim are
the substantive positive claims.

Compiler warnings concern unused variables and non-exhaustive helpers for
constructs such as string mapping, floats, and out-of-bounds subscripting.
None of those helpers is on this program's constructor path. No positive claim
timed out, crashed, or merely dry-ran.

As an additional fresh concrete check, the trusted translator produced a smoke
MPY containing the exact function plus the prompt examples, empty, negative,
and huge-integer assertions. `krun` against the fresh LLVM definition exited
0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0.

Evidence:

- [stage3_reconstruct.sh](evidence/stage3_reconstruct.sh) and
  [stage3_reconstruct.log](evidence/stage3_reconstruct.log)
- [stage7_concrete_smoke.py](evidence/stage7_concrete_smoke.py),
  [stage7_concrete_smoke.sh](evidence/stage7_concrete_smoke.sh), and
  [stage7_concrete_smoke.log](evidence/stage7_concrete_smoke.log)

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`SPEC.solution` starts in the standard module configuration with an empty
module scope, empty heap and stack, no pending return or exception, and exit
code 0. Its `<k>` cell:

1. loads one `FuncDef("solution", ...)`;
2. looks up that installed binding;
3. calls it on `list(vCons(HEAD, TAIL))`.

The precondition
`allInts(vCons(HEAD, TAIL))` means that the input is non-empty and every element
is a semantic K integer. `TAIL` is an arbitrary symbolic algebraic sequence;
there is no fixed length. K `Int` is unbounded.

The postcondition requires the final `<k>` result to be
`oddAtEvenSum(vCons(HEAD, TAIL), 0)`. It is not a free variable, an implication
with an unconstrained converse, or a tautology. The post-state also requires
the installed closure in module scope and normal restoration of the external
environment, heap, stack, return, exception, allocation, and exit cells.

### Connection claim in plain language

`CONNECTION-SPEC.loop` starts at the exact semantic `#loop` generated from the
real `for` statement. For any integer-only remaining sequence and nonnegative
current position, it consumes that loop while:

- increasing `position` by the remaining length;
- increasing `result` by the odd-at-even-position sum relative to the current
  position;
- setting the loop target `value` to the last consumed element (or preserving
  it for an empty remainder);
- preserving `lst`, the parent/outer scopes, arbitrary continuation, and every
  other configuration cell.

This claim imports `verification-base.k`, not the operational bridge.

### Mechanical source-to-claim identity

The auditor extracted the `Module(...)` argument actually present beneath
`#loadAll` in `spec.k`. Rule syntax spells empty statement-list identities as
`.Stmts`, whereas the program parser expects the corresponding omitted
surface-list form. An initial diagnostic `kast` attempt on the raw rule-syntax
term therefore failed at `.Stmts`; it did not run or test a proof. After the
single semantically inert normalization of deleting explicit ` .Stmts`
identities, both the submitted `solution.mpy` and extracted claim term parsed
as sort `Module` and produced byte-identical KORE:

`c6ed6ebe6010f7943caea440ff8f7e38bb6d56d4ecf87313726fda656e43cf5b`.

Thus the claim's installed binding and body are constructor-identical to the
trusted regeneration of the submitted program. No typing-only import,
substituted helper, call interception, or alternate body is involved.

Evidence:

- [stage4_prepare.py](evidence/stage4_prepare.py)
- [spec-module-extracted.mpy](evidence/spec-module-extracted.mpy) and
  [spec-module-extracted-program-syntax.mpy](evidence/spec-module-extracted-program-syntax.mpy)
- diagnostic [stage4_constructor_compare.log](evidence/stage4_constructor_compare.log)
  and successful
  [stage4_constructor_compare_normalized.log](evidence/stage4_constructor_compare_normalized.log)

### Satisfiable states and ground substitutions

`[5, 8, 7, 1]` is a concrete satisfying precondition witness:
`allInts(vCons(5,vCons(8,vCons(7,vCons(1,.ValSeq)))))` reduces to true.
A full-program ground instance of the entry claim closes to literal `12`.
Ground summary instances produce `12`, `9`, `0`, and `-3`; both Python
implementations produce those same values.

Evidence:

- [stage4-ground.k](evidence/stage4-ground.k)
- [stage4_ground_checks.sh](evidence/stage4_ground_checks.sh),
  [stage4_ground_checks.log](evidence/stage4_ground_checks.log), and
  [stage4_ground_python.py](evidence/stage4_ground_python.py)

The formal domain is the full material HumanEval domain. “Integers” is read in
the ordinary mathematical/HumanEval sense; semantic `Bool` is a distinct value
sort and is not silently admitted as an integer. Empty lists are expressly
outside the prompt's non-empty contract. The claim's unboxed structural list
is the supplied semantics' designated read-only external-input representation.
The program does not observe list identity or mutate the argument; the separate
LLVM smoke run also exercises heap-allocated list arguments.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The auditor mechanically inventoried every local declaration in the trusted
semantics tree, `verification-base.k`, `verification.k`, `spec.k`, and
`connection-spec.k`:

- 954 entries total;
- 233 syntax declarations;
- 713 rules;
- 5 contexts;
- 1 configuration;
- 2 claims.

Each row contains source file and line, declaration kind, attributes
(`function`, `total`, `no-evaluators`, `priority`, `simplification`,
`concrete`, `symbolic`, `owise`, strictness, and related attributes), a
statement hash/signature, relevance classification, and review decision.
Inventory SHA-256:
`47529db7dbb30d620556154da547d09b36ce93e75ceca8da916bf02e40b1ac4b`.

The classifications are 84 material fixed-semantics entries, 823
sort-disjoint/constructor-absent fixed entries, 21 `MPY-KRUN`-only entries,
23 proof extensions, one operational bridge, and two reachability claims.
“Unused” means the rule head or construct cannot occur on this submitted
program and summary path; it is not a claim that the supplied partial Python
semantics models every unused CPython behavior.

Evidence:

- [stage5_rule_inventory.py](evidence/stage5_rule_inventory.py)
- [stage5_rule_inventory.tsv](evidence/stage5_rule_inventory.tsv)
- [stage5_rule_inventory_summary.json](evidence/stage5_rule_inventory_summary.json)
- [stage5_rule_inventory.log](evidence/stage5_rule_inventory.log)

### Material fixed-semantics map

| Submitted construct | Declaration/rule path and finding |
|---|---|
| `Module`, `FuncDef`, statements, expressions, names, integers, calls | `syntax.k`; constructor declarations and strictness match the translated AST |
| Initial cells, module load, sequencing, lookup, argument evaluation | `core.k`; standard cells are pinned, statements sequence left-to-right, and lookup uses the installed/local bindings |
| Function definition, parameter binding, call frame, return, pop | `functions.k` and `call.k`; callee and arguments evaluate before dispatch, a fresh local frame binds `lst`, return discards only the callee remainder, and pop restores the caller |
| Assignment and augmented assignment | `controls.k`; the ordinary local-map rules apply because this unannotated frame has no closure-cell marker |
| `for value in lst` | `controls.k`, `iter.k`, `list.k`, and `tuple.k` target binding; the iterable is evaluated once, each head is bound, the body runs, and the tail recurs |
| Nested `if` | `controls.k` plus `truthy(Bool)` in `core.k`; only the selected branch runs |
| `%`, `+`, `==`, `!=` | `operators.k` and `int.k`; evaluation is left-to-right and integer operations use unbounded K integers and Python-style modulo |
| Final state | fixed return/pop rules; no bridge intercepts load, lookup, call, parameter binding, initialization, return, or pop |

No material fixed rule fabricates a result, skips a used operation, changes
evaluation order, or leaves an observable state effect unmodeled. Rules for
floats, strings, sets, dictionaries, sorting, comprehensions, methods,
subscripts, imports, and other builtins are constructor- or sort-disjoint from
this execution. Runtime-only concrete rules are not imported by either proof
definition. Consequently, no unused rule admits a false conclusion witness on
an intended input.

### Proof-local functions and rules

| Extension | Class, domain, overlap/coverage, and decision |
|---|---|
| `allInts` and its two equations | Definitional predicate; empty/cons cases are disjoint and exhaustive, recursion descends on the tail. It exactly guards integer-only sequences. Sound. |
| `definedProjectInt` | Definitional predicate equal to K's generated `isInt`; total over `Val`. Sound. |
| `projectIntTotal`, the `#Ceil` characterization, guarded cast orientations, integer collapse, and idempotence | Guarded sort refinement, not an oracle. On every reachable use, `isInt(V)` holds, so the partial cast denotes the already-existing integer. Overlaps reduce to the same integer. Outside the integer domain the symbol is not used by a result-bearing path. Sound for every use contributing to the claims. |
| Dynamic-sort `%` and `+` twins | Derived lemmas guarded by `isInt(V)`. On overlap with fixed `MPY-INT`, `projectIntTotal(V)` collapses to `V`, so both RHS values agree. They read/write no cells and do not change operand evaluation. Sound. |
| `oddContribution` | Total mathematical definition over two integers. Its guards are a Boolean condition and its exact negation, so they are disjoint and exhaustive. Sound. |
| `oddAtEvenSum` | Structural definition over every `ValSeq`. Empty/cons cases are disjoint; integer/non-integer cons guards are complementary; recursion descends. On `allInts`, it is precisely the contract sum. The non-integer branch cannot admit a target input or call the projection. Sound. |
| `lastAfter` | Structural, total empty/cons definition of the final loop-target local. It cannot affect the returned result. Sound. |

There is no fresh unconstrained result-bearing symbol. The recursive
mathematical summary is fixed by exhaustive equations, and the program-derived
loop value is connected to fixed execution by the auxiliary theorem.

### Sole operational bridge

The priority-40 rule in `verification.k` replaces only the exact semantic
`#loop`. Mechanical comparison found:

- the bridge's complete `<k>`, scopes, updates, frames, and guard are identical
  to `CONNECTION-SPEC.loop` (same normalized SHA-256
  `62fe7859be9c84dd70002051be8ccdea88959fbe27471426dcb1e7eaf1ede04f`);
- the loop body is exactly the `For` body in the real entry term (same
  normalized SHA-256
  `810863557f976b07a410498fba7665808040607515078e8ca95a3aebc0e81404`);
- the connection module does not import the bridge.

Both theorem and rule admit the same arbitrary continuation. Both frame the
same outer scopes and omitted cells. Both read the remaining iterator and
three locals, update only `position`, `result`, and `value`, and preserve
`lst`, control suffix, allocation, heap, stack, return, exception, and exit
state. The bridge introduces no return, pop, exception, or cleanup effect.
Priority merely selects the already-proved transition on the proved domain.

The bridge-free theorem closes universally with symbolic `REST`; it is not a
finite unrolling. A fresh body-sensitivity mutation changed the actual loop
term to `position += 2` on input `[1,3]` while demanding the original state.
The mutation dry-ran successfully and failed under both bridge-free and
bridge-enabled definitions. Both residuals contain the real changed result:
`position = 4`, `result = 4`, rather than demanded `2` and `1`. Thus the
operational bridge neither matches the changed body nor discards its effect.

Evidence:

- [stage5_bridge_compare.py](evidence/stage5_bridge_compare.py) and
  [stage5_bridge_compare.log](evidence/stage5_bridge_compare.log)
- [stage5-body-sensitivity.k](evidence/stage5-body-sensitivity.k),
  [stage5_body_sensitivity.sh](evidence/stage5_body_sensitivity.sh), and
  [stage5_body_sensitivity.log](evidence/stage5_body_sensitivity.log)

No materially unsound local rule was found. Accordingly, there is no
unsoundness allegation requiring a false-conclusion witness.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was inspected only as untrusted evidence and
was not reused. The auditor made a fresh concrete mutation of the complete
entry claim:

- satisfying input: `[5,8,7,1]`;
- true K/Python result: `12`;
- mutated demanded result: `13`.

The mutation still loads and calls the exact full function body. Its
`kprove --dry-run` command exited 0, proving the artifact parsed and compiled.
The actual proof exited 1 with `WarnStuckClaimState`; all final cells matched,
but the residual was `<k> 12 ~> .K </k>` rather than destination `13`. This is
the expected unmet result obligation, not a parser error, missing import,
timeout, or unrelated crash.

Evidence:

- [stage6_prepare.py](evidence/stage6_prepare.py)
- [stage6-false-result.k](evidence/stage6-false-result.k)
- [stage6_nonvacuity.sh](evidence/stage6_nonvacuity.sh) and
  [stage6_nonvacuity.log](evidence/stage6_nonvacuity.log)

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What the proof establishes

Relative to the supplied MPY semantics, for every non-empty finite semantic
list of K integers, if the submitted translated program reaches its normal
external return configuration, its returned value is the sum of exactly the
odd-valued elements at even zero-based positions. The theorem is symbolic in
the whole list tail and integer values. It is a partial-correctness theorem;
it does not claim a separate total-correctness, resource, or complexity bound.

The formal result comes from the bridge-free loop reachability proof and full
entry reachability proof. Differential and concrete tests support only the
translation/intent/model bridges; they do not replace either K proof.

### Trust ledger

| Boundary | Influence and assessment |
|---|---|
| Trusted supplied `reference-semantics` | Defines the theorem's execution model. Its exact trusted integrity passed, and every material rule was statically reviewed. The definition is intentionally a partial Python semantics; unsupported unused constructs are outside this program. Acceptable. |
| K 7.1.293 parser, kompiler, Haskell prover, LLVM runner, builtin integer/Boolean/map/list theories, and backend solvers | Low-level machine-checking and ordinary-mathematics trust boundary. They affect proof closure and concrete execution. Standard and explicit; acceptable. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py` to MPY constructors. Trusted by the benchmark; byte-identical candidate copy and byte-identical regeneration were independently checked. Acceptable. |
| External-input list representation | The theorem uses the supplied semantics' canonical unboxed read-only `list(ValSeq)` input. Every finite Python integer-list content maps structurally to it; this program neither mutates nor observes identity. Heap-ref list behavior was also concretely exercised. Acceptable and non-narrowing. |
| `oddAtEvenSum` to English contract | Ordinary structural mathematics: it advances positions by one and includes a value exactly under even-position and odd-value parity. Ground and broad differential evidence support the interpretation, but its universal meaning follows directly from its exhaustive recursive equations. Acceptable. |
| Canonical Python behavior | The trusted canonical implementation is an independent executable oracle for 142,272 recorded cases. This is finite adequacy evidence only. No K proof step assumes the test result. |
| Termination | Not claimed as a separate theorem. The source loop obviously traverses a finite structural list, and concrete runs terminate, but the reported status remains partial correctness. |

There is no proof-local trusted primitive, empirical value oracle, hidden
axiom for the task answer, or informal assumption that supplies the returned
value. The one execution shortcut is justified by a separately compiled,
bridge-free universal theorem over an identical context.

Gate A (real-program soundness): PASS.  
Gate B (full source-contract adequacy): PASS.  
Gate C (trust/evidence auditability): PASS.

The candidate is therefore a sound, result-constraining proof of the real
generated program over the unrestricted material HumanEval domain.

VERDICT: PASS
LEGITIMACY: LEGIT
