# Independent adversarial audit: 8-sum-product

## Outcome

The candidate contains a genuine, non-vacuous partial-correctness proof under
the supplied semantics, but the formal entry theorem is narrower than the
HumanEval contract. `SPEC.sum-product` proves exact execution only for lists of
exactly four arbitrary K integers. The separately proved loop and `For` suffix
claims are universal over finite integer sequences, but they are not a
universal theorem for invoking the submitted function.

This is a legitimate proof of the real function body on its stated formal
domain, not a proof of the full all-length contract. That material scope
limitation determines `CONCERNS / LEGIT`. I found no unsound proof-local rule
and therefore make no unsupported unsoundness allegation.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no infrastructure-mode
contradiction.

I recursively compared `/candidate/reference-semantics` against the trusted
tree with:

```text
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
```

It exited 0 with no differences. Separate path/type and symlink checks found
no missing, additional, changed, mistyped, or symlinked entry in either
semantics tree. The candidate prompt and translator are regular files and are
byte-identical to their trusted versions. Their SHA-256 values also match the
untrusted hashes stated in `run-input.json`:

- prompt:
  `84dc98e731928675a91c68cbff1f89d0677596f849fa0e6b34fa9b40335fce03`
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The required candidate source/deliverable artifacts
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`, and the provenance artifacts `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log`, are all present as regular files.
One structured JSONL trace is present; it has 1,055 valid JSON lines and no
malformed line.

I treated all provenance prose and prior outputs as untrusted claims. In
particular, the claimed exit 0 in `metrics.json`, prior `#Top` reports, and the
candidate's `SOUND-BUT-LIMITED` assessment played no role in accepting the
proof. Candidate `*-kompiled` directories and caches were not copied or used.

Evidence:

- [stage1_2_checks.log](evidence/logs/stage1_2_checks.log)
- [provenance_summary.log](evidence/logs/provenance_summary.log)
- [source_manifest.log](evidence/logs/source_manifest.log)
- reviewer scripts
  [stage1_2_checks.sh](evidence/stage1_2_checks.sh),
  [provenance_summary.py](evidence/provenance_summary.py), and
  [source_manifest.sh](evidence/source_manifest.sh)

Integrity result: pass; no infrastructure breach and no required-artifact
integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`, the entry
point is `sum_product(numbers: List[int]) -> Tuple[int, int]`: for any finite
list of integers, return the sum of all elements and their product. The empty
sum is 0 and the empty product is 1. The documented examples are `[] -> (0,1)`
and `[1,2,3,4] -> (10,24)`.

### Source inspection and translation

`/candidate/solution.py:4-11` initializes `total=0` and `product=1`, iterates
once over every element, adds the element to `total`, multiplies it into
`product`, and returns the pair. The extra initialization `number=0` does not
affect the result: on an empty list `number` is not returned, and on a
nonempty list the `for` target overwrites it.

Using the trusted translator in the scratch directory:

```text
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
cmp /tmp/audit-work/reconstruction/solution.mpy \
  /tmp/audit-work/reconstruction/regenerated-solution.mpy
```

Both commands exited 0. The submitted `solution.mpy` is therefore byte-exact
trusted translation output.

### Independent differential test

The reviewer-authored differential test loads the trusted canonical and
scratch candidate modules independently. It covers:

- both documented examples;
- empty, one-element, two-element, zero, negative, sign-changing, large
  integer, and length boundaries;
- every list of length 0 through 4 over `{-3,-1,0,1,2}`; and
- 1,000 deterministic generated lists of lengths 0 through 20 with elements
  in `[-1000,1000]`.

After deduplication, 1,723 inputs were compared. There were zero value or
return-type mismatches. The exact generated input JSON is preserved at
[differential_inputs.json](evidence/inputs/differential_inputs.json), with
SHA-256
`7258f017709dbd7c2563696ef05b3ee80daa2e5fcfeff1d14e1473feeaaa9abb`.

Evidence:

- [differential_test.py](evidence/differential_test.py)
- commands, scope, status, and result in
  [stage1_2_checks.log](evidence/logs/stage1_2_checks.log)

Program-fidelity result: pass. The testing is finite evidence, not a proof of
universal equivalence.

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the already integrity-checked
semantics tree to `/tmp/audit-work/reconstruction`. No candidate definition,
cache, binary, or KORE file entered the reconstruction. The source hashes in
the scratch copy equal the candidate source hashes; reviewer-built
definitions have the `audit-` prefix. See
[source_manifest.log](evidence/logs/source_manifest.log).

The live tool was K v7.1.293. The independent reconstruction ran these
positive targets in order:

| Operation | Result |
|---|---|
| `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| `kompile --backend haskell verification.k --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition audit-verification-base-kompiled` | exit 0 |
| `kprove spec.k --definition audit-verification-base-kompiled --spec-module LOOP-SPEC` | exit 0, `#Top` |
| `kprove spec.k --definition audit-verification-base-kompiled --spec-module SPEC` | exit 0, `#Top` |
| `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| `kprove spec.k --definition audit-verification-kompiled --spec-module FOR-SPEC` | exit 0, `#Top` |

Those are all three claims inventoried in `spec.k`. In particular,
`LOOP-SPEC` and the target entry `SPEC` were proved in
`VERIFICATION-BASE`, where the operational bridge in module `VERIFICATION`
is not imported.

The fresh LLVM definition also executed a reviewer-authored translated module
containing assertions for `[]`, `[1,2,3,4]`, and `[-2,3,0,5]`. `krun` exited
0 with `.K`, `NoExc`, and exit code 0.

Evidence:

- exact reconstruction driver:
  [reconstruct_proofs.sh](evidence/reconstruct_proofs.sh)
- [build_runtime.log](evidence/logs/build_runtime.log),
  [build_verification_base.log](evidence/logs/build_verification_base.log),
  [prove_loop_spec.log](evidence/logs/prove_loop_spec.log),
  [prove_entry_spec.log](evidence/logs/prove_entry_spec.log),
  [build_verification_bridge.log](evidence/logs/build_verification_bridge.log),
  and [prove_for_spec.log](evidence/logs/prove_for_spec.log)
- concrete source [k_concrete_audit.py](evidence/k_concrete_audit.py),
  translated input [k_concrete_audit.mpy](evidence/inputs/k_concrete_audit.mpy),
  and [concrete_krun.log](evidence/logs/concrete_krun.log)

Clean-reconstruction result: pass.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

`LOOP-SPEC.sum-product-loop` (`/candidate/spec.k:6-42`) starts at the exact
internal loop head with:

- any finite `ValSeq VS` whose elements all satisfy `isInt`;
- integer accumulator bindings `SUM` and `PRODUCT`;
- the exact two `AugAssign` body statements;
- the exact return and `#endcall` continuation;
- a complete local scope and caller frame; and
- empty heap, clean return/exception state, and exit code 0.

It says that real fixed-semantics execution consumes the remaining loop,
returns `(sumFrom(VS,SUM), productFrom(VS,PRODUCT))`, pops the frame, restores
the caller environment and scope location, deletes the local scope, and leaves
all other stated cells as shown.

`FOR-SPEC.sum-product-for` (`spec.k:48-84`) states the corresponding result
one step earlier, at the exact `For` statement. It has the same integer-domain
precondition and final state.

`SPEC.sum-product` (`spec.k:90-155`) starts at direct invocation of an exact
`closureVal` for the submitted body. Its formal input pattern is not an
arbitrary list: it is exactly `[A,B,C,D]`, where each of `A`, `B`, `C`, and
`D` has K sort `Int`. It returns the two fold summaries seeded by 0 and 1,
with the caller state fully restored. There is no free result variable,
tautological `ensures`, or one-way implication standing in for equality.

### Real-program identity

The target `<k>` cell does not begin at the outer
`#loadAll(Module(...))` term from `solution.mpy`. It begins at an exact
invocation of the function closure and therefore assumes that module loading
and binding have already happened. This is not a substituted computation:

- trusted regeneration pins `solution.py` to `solution.mpy`;
- the exact translated function body occurs once in `solution.mpy`;
- the exact closure occurs twice in `spec.k` (the invoked closure and its
  module binding); and
- `SPEC` uses the bridge-free proof definition, so the body executes under
  the supplied call, binding, assignment, loop, return, and frame-pop rules.

The independent structural comparison records both body pinning and a
byte-normalized equality between the loop theorem's entire configuration
contract and the operational bridge:
[structural_checks.log](evidence/logs/structural_checks.log).

The omission of module loading from the formal entry claim is an explicit
trust/adequacy boundary. The full translated module was concretely executed
in Stage 3, and the supplied semantics makes the `typing` import a no-op, but
there is no separate universal reachability claim connecting
`#loadAll(solution.mpy)` to the preseeded closure state.

The claim also supplies `list(VS)` directly rather than a heap `ref` created
by `ListExpr`. The supplied semantics explicitly permits bare list values as
read-only claim inputs, and this program only iterates over the input. Thus no
mutation, alias, identity, allocation, or exception behavior is lost on this
program path.

### Satisfiable witnesses and substitutions

Each precondition has a concrete state:

- `SPEC`: `A=1, B=2, C=3, D=4`, the shown module scope, and any concrete
  builtins scope satisfy the source pattern; the result is `(10,24)`.
- `LOOP-SPEC`: `VS=.ValSeq`, `SUM=0`, `PRODUCT=1`, `number=0`, and
  `parent(0)` satisfy `allIntVals`; the result is `(0,1)`.
- `FOR-SPEC`: `VS=[2,3]`, `SUM=0`, `PRODUCT=1`, `number=0`, and
  `parent(0)` satisfy `allIntVals`; the result is `(5,6)`.

For all three witnesses, the fold summaries, trusted canonical Python, and
candidate Python results agree. The exact output is in
[ground_claim_witnesses.log](evidence/logs/ground_claim_witnesses.log).
The `[2,3]` exact loop state was additionally proved both without and with the
bridge; both runs closed with `#Top`.

### Adequacy limitation

The natural-language domain is every finite integer list. The only exact
function-invocation theorem has length exactly four. Empty and other lengths
are covered by concrete tests and by universal internal loop/`For` suffix
theorems, but no K theorem composes those suffix theorems with arbitrary-list
function invocation. Tests and an informal composition argument cannot fill
that formal gap.

Adequacy result: the real body is pinned and the stated result is constrained,
but the entry theorem is materially narrower than the requested contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and supplied-semantics boundary

The reviewer inventory covers `reference-semantics/semantics.k`, all 23
supplied helper `.k` files, `verification.k`, and `spec.k`. It contains 944
records:

- 230 local syntax declarations;
- 702 ordinary rules;
- 3 simplification rules;
- 5 contexts;
- 1 configuration; and
- 3 claims.

Across those declarations the inventory records 148 `[function]` records,
108 `[total]`, no `[functional]`, 46 priority records, 25 `[symbol]`, and no
`[opaque]`. Every declaration and rule is individually listed with source
file, line, attributes, normalized text, and audit classification in
[rule_inventory.txt](evidence/rule_inventory.txt). The generation command and
summary are in [inventory.log](evidence/logs/inventory.log), and the generator
is [inventory_k.py](evidence/inventory_k.py).

In `SUPPLIED_SEMANTICS` mode, every rule under `reference-semantics/` is the
byte-verified trusted baseline selected by the problem. Those records are
marked `TRUSTED_SUPPLIED_BASELINE`; this does not bless anything in
`verification.k`. `MPY-CONCRETE` is imported only by the LLVM runtime module,
not either Haskell proof module. Compiler non-exhaustiveness warnings in
unused supplied float/string/subscript helpers are visible in the build logs;
none lies on this program's integer/list path.

There is no candidate-generated `semantic.k` or generated semantic helper to
audit in this mode.

### Used-construct coverage

The following fixed-semantics path covers every constructor in
`solution.mpy`:

| Submitted construct | Declaration and operational coverage |
|---|---|
| `Module`, `ImportFrom("typing",...)`, `FuncDef`, `Params` | `semantics/syntax.k`; `#loadAll` and statement sequencing in `core.k`; non-`math` import no-op in `controls.k`; closure binding in `functions.k` |
| direct `closureVal` invocation | `toCall/#applyK` and left-to-right argument machinery in `core.k`; closure frame allocation, parameter binding, and continuation push in `call.k`/`functions.k` |
| `Assign(Name(...), Int(...))` | strict RHS syntax; integer literal and name lookup in `core.k`; current-scope update in `controls.k` |
| `For(Name(...), Name("numbers"), BODY)` | strict iterable evaluation and one-time list dereference in `controls.k`; list `#iterNext` empty/cons rules in `list.k`; target binding in `tuple.k` |
| ordered `AugAssign` for `+` then `*` | statement sequencing in `core.k`; current-scope read/update in `controls.k`; fixed integer `applyBin` equations in `int.k` |
| `Return(TupleExpr(...))` | left-to-right tuple evaluation/construction in `tuple.k`; return, `#endcall`, and full frame pop in `functions.k` |

The ten-cell configuration is `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.
Every claim and the bridge includes every one of these cells. The initial
assignments allocate no heap object; loop target/accumulator changes remain in
the local scope; return sets and clears `<ret>`, restores the caller frame,
and deletes the local scope. Integer addition and multiplication are unbounded
K integers, matching the intended mathematical integer behavior.

### Exhaustive proof-local extension decisions

`verification.k` has three syntax declarations and ten rules. Their decisions
are:

1. `allIntVals(ValSeq) [function,total]` and its empty/cons equations
   (`verification.k:8-11`) are a pure definitional predicate. Empty and cons
   cover every `ValSeq`, do not overlap, and recursion strictly descends.
2. `sumFrom` and its two equations (`verification.k:15-19`) are a pure,
   deliberately partial accumulator fold. Empty and integer-headed cons cases
   are disjoint, recursion descends, and `allIntVals` guarantees coverage at
   every use.
3. `productFrom` and its two equations (`verification.k:21-25`) have the same
   valid coverage/descent argument using integer multiplication.
4. The `applyBin("+",ACC:Int,V:Val)` simplification
   (`verification.k:29-31`) is a derived sort-refined restatement of the
   supplied `applyBin("+",Int,Int)` equation. `isInt(V)` justifies the
   projection; on overlap the right sides agree.
5. The corresponding multiplication simplification
   (`verification.k:32-34`) is valid for the same reason. The `+` and `*`
   rules have disjoint operator literals.
6. The map-deletion simplification (`verification.k:37-39`) is valid map
   algebra: deleting key 1 from `1 |-> LOCAL OUTER` yields `OUTER` when the
   guard states key 1 is absent from `OUTER`. It normalizes the fixed `#pop`
   result and does not bypass `#pop`.
7. The priority-40 rule (`verification.k:49-86`) is an operational bridge.
   It is not an oracle. Its complete normalized configuration, guard, result,
   control effects, and state effects are exactly equal to the independently
   proved bridge-free `LOOP-SPEC.sum-product-loop` theorem. The base theorem
   imports `VERIFICATION-BASE`, not the bridge-bearing module.

The bridge reads the exact finite integer iterator and four local bindings;
it consumes precisely the loop, exact return expression, and `#endcall`;
restores environment 0 and scope location 1; removes local scope 1; empties
the exact singleton stack; and preserves empty heap, heap location 0, clean
return/exception cells, exit code 0, and arbitrary outer scopes. It has no
cell ellipses, continuation frame, or broader guard.

Operational and value sensitivity were checked independently:

- the exact ground `[2,3]` state proves `(5,6)` with both the bridge-free and
  bridge-enabled definitions;
- replacing the exact continuation with `return (99,100)` still proves
  `(99,100)` under the bridge-bearing definition, showing the narrow bridge
  does not capture that context; and
- changing the product body from `*=` to `-=` builds but does not prove the
  old product. The residual is `(5,-4)`, so the bridge did not swallow the
  changed body.

Commands and results are in
[bridge_ground_base.log](evidence/logs/bridge_ground_base.log),
[bridge_ground_extended.log](evidence/logs/bridge_ground_extended.log),
[bridge_changed_context.log](evidence/logs/bridge_changed_context.log),
[bridge_body_mutation_dry_run.log](evidence/logs/bridge_body_mutation_dry_run.log),
and [bridge_body_mutation.log](evidence/logs/bridge_body_mutation.log).
The inputs and driver are
[spec-bridge-audit.k](evidence/spec-bridge-audit.k) and
[run_bridge_audit.sh](evidence/run_bridge_audit.sh).

No proof-local opaque or fresh result-bearing symbol exists. `sumFrom` and
`productFrom` are exhaustively defined on their guarded domain and are
connected to fixed execution by the bridge-free universal loop theorem.
There is no encoded task answer, unconstrained oracle, fabricated result,
unused-construct shortcut, or execution-bypassing rule in the target entry
proof. I therefore do not label any inventoried proof-local rule unsound and
have no false-conclusion witness to report for such a label.

Static-soundness result: pass.

## 6. Fresh non-vacuity test

I did not reuse or rely on `/candidate/spec-vacuity.k`. The fresh mutation
[spec-audit-vacuity.k](evidence/spec-audit-vacuity.k) invokes the exact closure
on the satisfying input `[-2,3,0,5]`. Real execution and both Python
implementations return `(6,0)`; the mutation instead demands `(6,1)`.

Using the bridge-free proof definition:

```text
kprove spec-audit-vacuity.k \
  --definition audit-verification-base-kompiled \
  --spec-module SPEC-AUDIT-VACUITY --dry-run
```

exited 0, establishing that the mutation parsed and built. The same command
without `--dry-run` exited 1 with `WarnStuckClaimState`. Its residual complete
configuration has `<k> tuple(vCons(6,vCons(0,.ValSeq)))`, exactly the expected
unmet result obligation. This was not a parser error, missing import, timeout,
or unrelated failure.

Evidence:

- [run_vacuity_test.sh](evidence/run_vacuity_test.sh)
- [vacuity_dry_run.log](evidence/logs/vacuity_dry_run.log)
- [vacuity_proof.log](evidence/logs/vacuity_proof.log)

Non-vacuity result: pass.

## 7. Proven versus assumed accounting

### What is machine proved

Subject to the supplied semantics and proof-local equations audited above:

- For every four K integers `A,B,C,D`, if execution of the exact submitted
  function closure on `[A,B,C,D]` terminates, the stated returned tuple has
  fold sum from 0 as its first component and fold product from 1 as its
  second, with all specified control/state cells restored.
- For every finite all-integer `ValSeq` and integer starting accumulators, the
  exact loop/return/frame-pop suffix has the corresponding fold summaries at
  termination under the bridge-free supplied semantics.
- The exact `For` suffix has the same universal partial-correctness result,
  using the independently justified exact loop bridge.

These are partial-correctness reachability results. The proof does not itself
establish a separate liveness theorem, although termination of this finite
structural list loop follows by ordinary finite-list reasoning.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted supplied MPY semantics | Defines all syntax, control, state, call, list iteration, integer arithmetic dispatch, return, and allocation behavior used by every claim | Required and acceptable by `SUPPLIED_SEMANTICS`; tree integrity passed |
| K toolchain/backend, K integer and map primitives, generated `isInt` predicate | Underlies `#Top`, integer `+Int/*Int`, map update/deletion, and the guarded Val-to-Int projection | Normal low-level proof trust boundary |
| Trusted `py2mpy.py` | Connects `solution.py` to the submitted K constructor program | Acceptable syntactic bridge; byte regeneration passed |
| Direct closure-entry model | Omits formal module loading and assumes the exact closure binding and a direct read-only list value | Concerning but not false here: body is structurally pinned, full module runs concretely, and the omitted import/binding path cannot affect this function's result |
| Exact loop operational bridge | Affects only `FOR-SPEC`, including value, frame pop, and all state cells | Acceptable: exact bridge-free universal connection theorem plus ground, context, and body-sensitivity evidence |
| Canonical-to-candidate intent bridge | Supports the claim that the different Python implementation realizes the HumanEval behavior | Empirical only: 1,723 zero-mismatch cases; it does not replace the K proof |
| Finite-list termination argument | Explains why the exact loop bridge does not introduce termination absent from the fixed execution | Ordinary informal structural argument; not claimed as a K liveness theorem |

There are no proof-local opaque symbols or externally trusted result oracles.
The 25 `[symbol]` records in the inventory belong to the trusted supplied
semantics; none supplies the sum/product result on the used path.

### Excluded conclusion and verdict rationale

Nothing machine-checked here proves:

```text
for every finite-length integer list, invoking sum_product returns its sum
and product
```

The universal internal suffix claims and differential tests strongly support
that statement, but the exact invocation theorem remains length four. This
does not make any proved conclusion false, vacuous, or about a substituted
program, so `FAIL / NOT_LEGIT` would be unwarranted. It does prevent an
unqualified `PASS`, because the natural-language contract's input domain is
not fully covered.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
