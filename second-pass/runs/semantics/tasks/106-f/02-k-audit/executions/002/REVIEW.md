# Independent adversarial audit — HumanEval 106-f

The candidate reconstructs and proves a real reachability theorem about the
submitted program. It is not vacuous, does not substitute another body, and
does not use an operational shortcut. The review nevertheless records a
non-fatal formalization concern: the result predicate `outputOK` is declared
`[function, total]` but its equations define only successful cases. K's LLVM
exhaustiveness checker flags it, and there is no separate checked theorem
stating that `outputOK == true` is equivalent to the source-level result
property. Ground opposite-result probes are rejected, so this is an evidence
and intent-bridge limitation rather than a witnessed false rule.

All reviewer-created scripts, mutations, exact commands, exit statuses, and
bounded outputs are under `/audit-output/evidence/`. The command index is
`evidence/COMMANDS.md`.

## 1. Input and provenance integrity

`/audit-input.json` declares problem `106-f`, condition `semantics`,
`semantics_mode = SUPPLIED_SEMANTICS`, and record layout
`legacy-selected-stage1`. The supplied-semantics mount is present, as required;
there is no mode/mount contradiction.

I checked the container paths rather than the host provenance strings.
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, and every record required by this legacy layout are
present, regular/readable objects. The required generation records are:

- `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured `codex-trace/`;
- `usage.json`, which is present and was therefore also checked.

Historical runtime metrics are absent, which is permitted for this layout.
The one trace file contains 706 valid JSONL records: 485 `response_item`, 218
`event_msg`, and one each of `session_meta`, `world_state`, and
`turn_context`. Its declared SHA-256 matches. The trace and prose report a
successful candidate run, but I did not use that claim as proof evidence.

The campaign block in `/audit-input.json` is byte-for-byte the parsed JSON
object in `/audit-campaign-lock.json`; the lock digest is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. Every individually recorded hash checked in
`evidence/01_integrity_checks.log` matches, including the run/task/result and
invocation records, canonical program, prompt, translator, generation prompt,
metrics, usage, last message, output log, and trace.

The candidate contains no symlink. Its `reference-semantics/` and the trusted
`/reference/reference-semantics/` have the same 25 relative entries, entry
types, and file bytes. The candidate prompt and translator are byte-identical
to `/reference/prompt.py` and `/reference/py2mpy.py`. The launcher aggregate
tree hash does not document its serialization algorithm; I therefore computed
a separate deterministic per-entry manifest digest and, more importantly,
compared every relevant entry's type and bytes directly rather than comparing
unlike aggregate encodings.

There is no infrastructure breach. Evidence:
`evidence/01_integrity_checks.sh` and
`evidence/01_integrity_checks.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `f(n)` to return a list with one entry for each
`i = 1..n`: the entry is `i!` when `i` is even and
`1 + ... + i` when `i` is odd. The example is
`f(5) == [1, 2, 6, 24, 15]`. Because a list of size `n` is meaningful only for
`n >= 0`, I treat the material source-contract domain as nonnegative integers.
The behavior on negative integers was tested as a diagnostic but is not needed
to justify that domain interpretation.

The canonical implementation recomputes the factorial or sum with an inner
loop for each index. `solution.py` uses an equivalent one-pass algorithm:
`factorial` and `total` are updated at each `i`, the appropriate accumulator is
appended, and `i` is incremented.

### Translation identity

Using the trusted copied translator, I regenerated the MPY term. Both the
submitted and regenerated files have SHA-256
`df32d7402b425e332cf43fe54e6dead3182c62b558d3eb51f28c2396fa43feb7`;
`cmp` exited 0. See `evidence/02_translation_identity.log`.

### Independent differential evidence

`evidence/02_differential.py` separately imports the trusted canonical function
and reconstructed generated function. It also implements a third oracle using
`math.factorial(i)` and `i * (i + 1) // 2`. The run covers:

- negative diagnostics `-5` and `-1`;
- the empty boundary `0`;
- first odd/even paths and transitions `1..10`;
- the documented `5`, plus `20` and `50`;
- 200 seeded (`seed = 106`) nonnegative inputs in `0..80`.

All 215 cases agree among canonical, generated, and the independent oracle;
the mismatch count is zero. Exact inputs and per-case result digests are in
`evidence/02_differential.log`. This is finite program-fidelity evidence, not a
replacement for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`, using the
trusted supplied-semantics tree and trusted translator. No candidate compiled
definition or cache was copied or reused.

The live tools are K 7.1.293. Fresh builds succeeded:

- LLVM `MPY-KRUN` definition:
  `evidence/03_build_runtime.log`, exit 0;
- Haskell `VERIFICATION` definition:
  `evidence/03_build_verification.log`, exit 0.

Independent concrete MPY assertions for `n = 0,1,2,3,5,8` ran under the fresh
LLVM definition. The final configuration has `<k> .K </k>` and
`<exit-code> 0 </exit-code>`. See `evidence/03_concrete_tests.py` and
`evidence/03_krun_concrete.log`.

Every positive target was then run independently against the fresh Haskell
definition:

| Target | Exact selection/composition | Result |
|---|---|---|
| `loop-correct` | `--claims loop-correct` | exit 0, `#Top` |
| `f-symbolic` | `--claims loop-correct,f-symbolic --trusted loop-correct` | exit 0, `#Top` |
| `f-zero` | `--claims f-zero` | exit 0, `#Top` |
| `f-five` | `--claims f-five` | exit 0, `#Top` |

The four transcripts are
`evidence/03_prove_loop_correct.log`,
`evidence/03_prove_f_symbolic.log`,
`evidence/03_prove_f_zero.log`, and
`evidence/03_prove_f_five.log`. The symbolic entry proof manually composes
with `loop-correct` via `--trusted`; the exact trusted claim was separately
proved first under the same source definition.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` starts at the literal loop head with local `n = N`, `i = I`,
factorial accumulator `F`, triangular accumulator `T`, and a heap list
`PREFIX`. Under `1 <= I <= N + 1`, it consumes the loop, ends with
`i = N + 1`, extends the same heap list by an existential suffix `OUTPUT`, and
requires `outputOK(OUTPUT, I, N, F, T)`. The final accumulator values are
existential because they are unobservable after the loop.

`f-symbolic` starts with a call of `f(N)` in a scope containing the submitted
closure. For `N >= 0`, it returns `ref(0)`, allocates heap location 0 to a list
`OUTPUT`, restores the caller frame, and requires
`outputOK(OUTPUT, 1, N, 1, 0)`.

`f-zero` and `f-five` are fully ground entry claims. They constrain the heap to
`[]` and `[1,2,6,24,15]`, respectively.

### Satisfiable starts and concrete substitution

Each entry precondition is satisfiable:

- `loop-correct`: choose `N = 0`, `I = 1`, `F = 1`, `T = 0`,
  `PREFIX = .ValSeq`, and an empty module map. This is also the reachable loop
  state after initialization in `f(0)`.
- `f-symbolic`: choose `N = 0` or `N = 5` in the explicitly given scope/heap
  state.
- `f-zero` and `f-five`: their fully ground initial maps are valid
  configurations.

For `N = 0`, the symbolic postcondition reduces by the base equation because
`1 > 0`, and both Python functions return `[]`. For `N = 5`, the predicate
consumes `1,2,6,24,15` through odd/even guards and reaches its base at
`I = 6 > 5`; both Python functions return that list. For the reachable loop
state `N = 2, I = 1, F = 1, T = 0`, the suffix is `[1,2]` and the final index is
3, again agreeing with both implementations.

### Mechanical program identity

The entry claims do not load `solution.mpy`; they install the function binding
directly. This is acceptable here because it is mechanically pinned:

1. `solution.mpy` parses as `Module(FuncDef("f", Params("n"), BODY))`.
2. The fixed `FuncDef` rule in `semantics/functions.k:14` installs
   `closureVal("n", .ParamNames, BODY, 0)` in the module frame.
3. All three entry claims contain that exact binding.
4. The extracted submitted module and extracted entry-claim module parse to
   byte-identical KORE, SHA-256
   `ecfc4d85c3df34d69dd02cb2af741955d57a4264ef294a7a5208c0388c278f75`.
5. The submitted `While` and the helper claim's `#while`, normalized back to
   `While`, also parse to byte-identical KORE, SHA-256
   `217d722308b39320cb97157c24553c751f52cf73d09219b9e852653372f718ea`.

See `evidence/04_constructor_compare.py` and
`evidence/04_constructor_compare.log`.

A body-sensitivity mutation changes the term actually executed by the claim:
`total += i` becomes `total += 2`. It parses successfully, executes on `n = 1`,
reaches heap `[2]`, and fails to unify with the correct `[1]` target. The
internal `kprove` exit is 1 with `WarnStuckClaimState`. See
`evidence/spec-body-mutation.k`,
`evidence/04_body_mutation_dry_run.log`, and
`evidence/04_body_mutation_proof.log`.

The result is not a free variable: `OUTPUT` is tied to the allocated heap list,
and ground wrong-predicate probes fail. The remaining limitation is the
formal meaning of the partial `outputOK` equations, discussed next.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_inventory_k.py` inventories every declaration block with source
line range and full text. `evidence/05_rule_inventory.log` contains 1,107
declarations: 228 syntax declarations, 702 rules, 5 contexts, 4 claims, one
configuration, and all module/import/require declarations. It finds 146
function declaration blocks, 108 marked total, 25 marked `symbol`, 45
priority declarations, 35 concrete declarations, 26 `owise` declarations,
four simplification rules, and no `[functional]` declaration.

The following row-level decision covers every inventoried rule in each file;
the evidence log provides the one-by-one text and locations.

| File | Rules | Static decision and relevance |
|---|---:|---|
| `semantics.k` | 0 | Import aggregation only; `MPY` excludes concrete-only rules and `MPY-KRUN` adds them. |
| `syntax.k` | 0 | All 16 syntax blocks are constructor grammar. Strictness gives the used RHS/operand evaluation order. |
| `core.k` | 46 | Used allocation, sequencing, lookup, literals, truthiness, argument evaluation, and finite-sequence helpers preserve the modeled cells and evaluation order. Guards/priorities separate cell/ref cases. |
| `functions.k` | 15 | The used `FuncDef`, binding, return, frame-pop rules preserve binding and control for this non-nested function. No closure escapes. |
| `call.k` | 21 | The used callee/argument/closure and bound-method routes evaluate left-to-right; append retains its receiver ref. |
| `controls.k` | 34 | Used assignment, integer aug-assignment, `If`, and `While` rules match the real control flow. Import and loop-control subset rules are unused. |
| `operators.k` | 10 | Used dispatch/deref rules preserve operand order; the submitted operands are integers, not refs. |
| `int.k` | 16 | Used `+`, `*`, `%`, `<=`, and `==` rules are ordinary unbounded integer arithmetic; `pyMod(_,2)` is well-defined. |
| `list.k` | 27 | Used list construction, allocation, append, and `valSeqConcat` perform the actual heap update. No list execution is replaced by a summary. |
| `bool.k` | 13 | Truth/short-circuit rules are faithful but unused except the shared Boolean result path. |
| `assert.k` | 3 | Concrete-test-only assertion behavior; not imported into a proof shortcut. |
| `range.k` | 6 | Finite range iteration; unused by the submitted optimized implementation. |
| `iter.k` | 0 | Protocol syntax only. |
| `tuple.k` | 21 | Unused constructor/iteration/unpacking subset. |
| `subscript.k` | 40 | Unused indexing/slicing subset. Its acknowledged total OOB abstraction does not occur on a proof path. |
| `methods.k` | 75 | The generic method equations are unused; append is implemented in `list.k`. |
| `str.k` | 28 | Unused ASCII/string subset. |
| `set.k` | 12 | Unused finite-code set subset. |
| `dict.k` | 28 | Unused ordered-dict subset. |
| `comprehension.k` | 7 | Unused macros. |
| `builtins.k` | 137 | Unused by this program. `md5hexCodes` is an explicit opaque primitive but has no dependent submitted term or claim. |
| `float.k` | 121 | All float operations and their opaque symbolic primitives are unused and sort-disjoint from the integer execution. |
| `sort.k` | 19 | Opaque `sortVS`/`sortKeyVS` are unused. |
| `concrete.k` | 16 | Imported only into LLVM `MPY-KRUN`, never the Haskell proof definition; it supports runtime testing only. |
| `verification.k` | 7 | Three `outputOK` equations and four finite-sequence simplifications, analyzed below. |

### Used-construct coverage

Every submitted constructor is declared and has a material execution route:

| Submitted constructor | Declaration | Material rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53,57,61` | `core.k:124-127`, `functions.k:14-16` |
| `Assign`, `Name`, `Int` | `syntax.k:9,12,41` | `controls.k:9-18`, `core.k:130-154,194` |
| `ListExpr` | `syntax.k:17` | `list.k:13-15`, `core.k:117-121,183-191` |
| `While` | `syntax.k:46` | `controls.k:77-85` |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:14-17`, integer comparison rules |
| `AugAssign`, `BinOp` | `syntax.k:15,44` | `controls.k:20-31`, `operators.k:12`, integer `+`, `*`, `%` |
| `If`, `Expr` | `syntax.k:49,52` | `controls.k:48,51-54` |
| `Call`, `Attribute` | `syntax.k:28-29` | `call.k:15-32,52-74`, `list.k:52-55` |
| `Return` | `syntax.k:50` | `functions.k:77-90` |

The active cells are `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. The entry claims
pin every cell changed by call/allocation/return. Omitted cells in the loop
claim are framed; this loop neither allocates a scope/heap location nor changes
stack, return, exception, or exit status.

### Proof-extension audit

There is no proof-local operational bridge, priority rule, opaque result
symbol, or rule that intercepts a program call. The extensions are:

| Extension | Class | Decision |
|---|---|---|
| `outputOK` and its three equations | Definitional result summary | The equations are truthful, pairwise guard-disjoint, and recursively advance `I`. They affect only the loop and symbolic-entry postconditions. Coverage is incomplete; see below. |
| `concat(concat(A,B),C) = concat(A,concat(B,C))` | Derived simplification | Valid by induction on finite `A`; no cells or control affected. |
| `concat(A,empty) = A` | Derived simplification | Valid by induction on finite `A`. |
| `concat(P,A)=concat(P,B) -> A=B` | Derived simplification | Left cancellation for finite constructor sequences. |
| `P=concat(P,A) -> empty=A` | Derived simplification | Follows from finite sequence length/cancellation. |

The simplification equations are globally broader than the concrete prefixes
reached from `f`, but remain true for the intended finite `ValSeq` domain. No
false conclusion witness exists for them.

`outputOK` is the only static concern. Its declaration at
`verification.k:8-9` is `[function, total]`, but it has no equations returning
`false` for:

- an empty sequence while `I <= N`;
- a nonempty sequence while `I > N`;
- an incorrect integer head;
- a non-integer head.

The fresh LLVM compile reports `outputOK` as a non-exhaustive total match; see
`evidence/05_build_verification_llvm_diagnostics.log`. This means the source
does not itself provide a checked equivalence between `outputOK == true` and
the intended list property. I did not label any equation unsound: each equation
has a true conclusion over its guard, and the required false-conclusion witness
does not exist. In fact, independent K probes show:

- the valid ground predicate proves `#Top`;
- `outputOK([2],1,1,1,0)` fails with an unmet implication;
- `outputOK([noneV],1,1,1,0)` also fails.

See `evidence/spec-predicate-probes.k` and the three
`evidence/05_predicate_*.log` files. Thus the current prover does discriminate
the tested wrong results, but the reverse intent bridge remains an inspected
informal induction rather than a machine-checked lemma. This limitation is the
reason for concerns rather than an unqualified pass.

The 25 imported `symbol(...)` declarations are exhaustively listed in
`evidence/05_opaque_symbol_inventory.txt`: 22 float/conversion symbols,
`sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs in `solution.mpy`,
`verification.k`, or any target claim's execution/postcondition, so none can
influence control, state, or result here.

## 6. Fresh non-vacuity test

`evidence/spec-vacuity.k` retains the exact unmodified submitted closure and
changes only the prompt-example result: its last element is constrained to 16
instead of 15.

The mutation dry-run exits 0, so it parses and builds against the fresh proof
definition. The proof then executes to the actual final heap
`[1,2,6,24,15]`, which does not unify with
`[1,2,6,24,16]`. It emits `WarnStuckClaimState`; the internal `kprove` exit is
1. This is the expected unmet result obligation, not a parser error, timeout,
or unrelated crash. See `evidence/06_false_mutation_dry_run.log` and
`evidence/06_false_mutation_proof.log`.

The proof is therefore non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

### What is formally established

Conditional on the supplied MPY semantics and the seven proof-local equations,
the successful reachability proofs establish partial correctness of the exact
submitted constructor term:

- the literal loop transforms a starting prefix into a prefix plus a suffix
  accepted by `outputOK`, with final `i = N + 1`;
- for every mathematical integer `N >= 0`, calling the exact submitted `f`
  closure returns a fresh list reference whose sequence is accepted by
  `outputOK(_,1,N,1,0)`;
- the exact ground calls at 0 and 5 return `[]` and
  `[1,2,6,24,15]`.

This is partial correctness. Termination is not part of the formal theorem,
although the concrete loop increments `i` toward the fixed bound.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and built-in Int/Bool/Map/List theories | All proofs | Necessary low-level trust; versions and fresh execution recorded. |
| Trusted `py2mpy.py` mapping CPython AST to MPY constructors | Source-to-term identity | Benchmark-declared trusted input; regeneration is byte-identical. Translator correctness itself is not re-proved. |
| Supplied MPY operational semantics | Program execution | Trusted fixed baseline, independently byte-checked and statically reviewed. The used integer/list/call/control subset executes every material operation. |
| Four proof-local finite-sequence equations | Loop and symbolic entry | Ordinary finite-list mathematics; no operational execution is skipped and no false witness was found. |
| Separately proved `loop-correct` passed to the entry run with `--trusted` | `f-symbolic` | Manual theorem composition. Acceptable because the exact claim independently closed under the same fresh definition, but no proof object links the two processes. |
| Informal induction from `outputOK` reductions to “factorial on even indices, triangular sum on odd indices” | Human-facing contract | Mathematically direct and supported by opposite ground probes, but weakened auditability by the non-exhaustive `[total]` declaration and absence of a checked iff lemma. Non-fatal concern. |
| 25 fixed-semantics opaque symbols | None | Imported but unreachable and absent from every target term/postcondition; no theorem conclusion depends on their interpretation. |
| Differential and concrete tests | Program/canonical and execution bridges | 215 Python cases and six MPY concrete cases with zero failures. Finite supporting evidence only. |
| Domain interpretation `N >= 0` | `f-symbolic` | Matches the prompt's “list of size n” contract. Negative behavior agrees empirically but is outside the formal claim. |

There is no empirical oracle shared between execution and postcondition, no
answer-encoding rule, no substituted program, and no materially narrowed
meaningful source domain. The proof's non-exhaustive result predicate and
manual intent bridge prevent an unqualified pass, but the fresh opposite-result
and body-sensitivity failures show that they do not make a false target close.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
