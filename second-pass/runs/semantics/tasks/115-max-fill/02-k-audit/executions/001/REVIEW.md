# Adversarial audit: 115-max-fill

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied semantics. I assign
`CONCERNS / LEGIT`, not `PASS`, because four requested provenance artifacts are
absent, the typed input representation is connected to ordinary supplied
lists by four universal one-step constructor claims plus a static
representation argument rather than one end-to-end bridge-free theorem, and
`ceilDiv` is declared total outside its proved positive-capacity domain. None
of those limitations enables a false conclusion on the entry claim's domain.

All candidate files were treated as untrusted. Builds and experiments used
only the scratch copy under `/tmp/audit-work/115-max-fill`; no candidate
compiled definition, cache, proof log, archive, or reported result was reused.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the mode.

`evidence/01_integrity.log` records types, hashes, comparisons, and statuses.
The candidate's `prompt.py` and `py2mpy.py` are regular files and byte-identical
to `/reference/prompt.py` and `/reference/py2mpy.py` (`cmp`, exit 0).
Recursive `diff --no-dereference -qr` between the candidate and trusted
`reference-semantics/` trees exits 0. Both trees have the same 24 regular
source files, no symlinks, no missing/additional/mistyped entries, and
identical per-file SHA-256 hashes.

The source proof artifacts `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are regular files. The candidate also contains untrusted
`__pycache__/solution.cpython-310.pyc` and `kore-exec.tar.gz`; neither was
copied into or used by a build. The archive only lists `spec.kore`,
`kore-exec.sh`, `vdefinition.kore`, `kore-exec.log`, and `error.log`
(`evidence/01b_untrusted_archive.log`). The unavailable diagnostic `file`
utility returned 127, but `tar -tzf` returned 0; this does not affect any audit
gate.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. These are evidence/provenance gaps,
not substitutes for the fresh reconstruction below.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the number of bucket lowerings needed to empty
each row independently. A row contains one unit for every `1`, and one
lowering removes at most `capacity`, so the result is
`sum(ceil(sum(row)/capacity) for row in grid)`. The documented domain is a
nonempty rectangular 1-to-100 by 1-to-100 bit grid and capacity 1 through 10.
The trusted canonical implementation states exactly that expression.

The submitted `solution.py` initializes an accumulator, iterates every row,
computes `sum(row)`, adds `(water + capacity - 1) // capacity`, and returns the
accumulator. For positive integer capacity this equals the canonical row
ceiling on the intended domain.

Trusted retranslation used:

```text
python3 /reference/py2mpy.py /tmp/audit-work/115-max-fill/solution.py
```

It exited 0. The regenerated and submitted MPY files are byte-identical and
both hash to
`9c812511c5008c54821890698023cc9f2abbe5d247631bf7b3d679bddef2fb47`
(`evidence/01_integrity.log`).

The independent script `evidence/differential_test.py` imports the trusted
canonical and scratch-copy generated entries and uses a third `divmod`-based
oracle. It covers all three examples; empty grid/row cases; minimum and
maximum capacities; 100-by-100 all-zero/all-one grids; every bit row of width
0 through 8 at every legal capacity; exhaustive representative three-row
combinations; and 1,000 deterministic samples over the full documented
dimension range. Exact command and result:

```text
python3 /audit-output/evidence/differential_test.py
EXIT_STATUS: 0
total_cases: 17097
mismatch_count: 0
```

See `evidence/02_differential.log`.

## 3. Clean proof reconstruction

The audit used K version v7.1.337. The exact commands and bounded outputs are
in `evidence/03_rebuild_and_positive_proofs.log` and
`evidence/03b_individual_positive_proofs.log`.

From source in the clean scratch tree:

1. `kompile reference-semantics/semantics.k --backend llvm
   --main-module MPY-KRUN --syntax-module MPY-SYNTAX
   --output-definition runtime-kompiled` exited 0.
2. `krun concrete-tests.mpy --definition runtime-kompiled` exited 0 with
   `.K`, `NoExc`, and exit code 0 after all three assertions.
3. `kompile verification.k --backend haskell --main-module MAX-FILL-DATA
   --syntax-module MPY-SYNTAX --output-definition bridge-check-kompiled`
   exited 0.
4. `kprove spec.k --definition bridge-check-kompiled
   --spec-module MAX-FILL-BRIDGE-SPEC` exited 0 and printed `#Top`.
5. `kompile verification.k --backend haskell
   --main-module MAX-FILL-VERIFICATION --syntax-module MPY-SYNTAX
   --output-definition verification-kompiled` exited 0.
6. `kprove spec.k --definition verification-kompiled
   --spec-module MAX-FILL-SPEC` exited 0 and printed `#Top`.

Every bridge claim was then selected separately by its fully qualified label;
all four exited 0 and printed `#Top`. The main claims were selected as
`sum-fold`, then `sum-fold,fill-loop`, then
`sum-fold,fill-loop,max-fill-correct`, so each target was proved with only its
needed preceding circularities; all runs exited 0 and printed `#Top`.

The earlier unqualified selector attempts in
`evidence/03_rebuild_and_positive_proofs.log` returned 113 with `Unused
filtering labels` before proof execution. They were corrected using the
toolchain's required `MODULE.label` spelling; the successful reruns are the
ones used as evidence.

Compiler warnings concern unused variables and unrelated non-exhaustive
fixed-semantics functions. No build/proof timed out, and every positive
target's actual success signal is both exit 0 and `#Top`.

## 4. Adequacy and real-program pinning

The claims mean:

- `bridge-sum-empty` and `bridge-sum-step`: under supplied semantics, one
  `sum`-fold transition over `rowVals` is the ordinary empty/head list
  iterator transition, for arbitrary accumulator and continuation.
- `bridge-loop-empty` and `bridge-loop-step`: one supplied `for`-loop
  transition over `gridVals` is the ordinary empty/head list iterator
  transition, for arbitrary target, body, and continuation.
- `sum-fold`: supplied iterator-based `sum` over a typed symbolic row returns
  the exact integer fold `rowTotal(A,IS)`.
- `fill-loop`: with a real `max_fill` frame and `C>0`, the real submitted loop
  consumes all represented rows, changes `result` to `fillTotal(A,GS,C)`, and
  leaves `row`/`water` at their real final values.
- `max-fill-correct`: from a clean configuration and `C>0`, loading and calling
  the submitted function returns exactly `maxFillSpec(GS,C)`.

`#runMaxFill` does not summarize the function. Its RHS contains the same
`Module(FuncDef(...))` AST as regenerated `solution.mpy`, followed by a real
`Call(Name("max_fill"),...)`. The function body, name lookup, call frame,
parameter binding, loop, `sum`, assignments, integer arithmetic, and return
all execute under supplied rules. `MAX_FILL_LOOP_BODY` is a macro expanding to
the exact submitted loop subtree.

The input uses `list(symGrid(GS))`, a typed sequence representation, rather
than reducing `gridVals(GS)` and losing element-sort information in symbolic
execution. The representation relation is
`symGrid(GS) ~ gridVals(GS)` and `symRow(IS) ~ rowVals(IS)`. Stage 5 audits its
constructor transitions and trust consequences.

The entry result is not free or existential: the destination `<k>` is
`maxFillSpec(GS,C)`. Control/resource cells are pinned to a clean call and
normal return. Only final `scopes` is existential because module/function
loading changes and deallocates scope entries.

Satisfiable ground instances in `evidence/04_ground_instances.k` cover:

- empty grid, capacity 1: result 0;
- `[[1]]`, capacity 1: result 1;
- `[[1,1,1],[0,1,0]]`, capacity 2: result 3.

Together and separately, each `kprove` run exits 0 with `#Top`
(`evidence/04_ground_instances.log`). Both Python implementations and the
independent oracle return the same values. The formal domain allows arbitrary
finite integer rows and requires only `C>0`; this is broader than the prompt's
bit/dimension constraints, and the submitted integer algorithm/specification
remain aligned on that broader domain.

## 5. Rule-by-rule static soundness review

`evidence/inventory_k.py` generated
`evidence/rule_inventory.md`, an exhaustive source-located inventory of all
967 local declarations across the supplied semantics, `verification.k`, and
`spec.k`: 718 rules, 236 syntax declarations, 7 claims, 5 contexts, and 1
configuration. It inventories every `function`, `total`, priority, concrete,
symbol/no-evaluator, owise, macro, strictness, and other declaration. There
are no local `functional`, `simplification`, or `opaque` attributes.

The 935 supplied-semantics declarations are byte-identical to the selected
trusted baseline. The reachable program path uses the fixed syntax,
configuration/load/lookup, function/call, control, list/iterator, sum, operator,
and integer modules. Every submitted construct is mapped to its declaration
and rules in `evidence/05_static_review.md`; unused float, string, set, dict,
sort, comprehension, method, range, tuple, subscript, and assertion operations
have no reachable redex in this program.

All 32 declarations in `verification.k` and 7 claims in `spec.k` are
individually disposed in `evidence/05_static_review.md`. The important results
are:

- `rowVals`, `gridVals`, `rowTotal`, `fillTotal`, `maxFillSpec`, `finalRow`,
  and `finalWater` have constructor-disjoint, exhaustive, descending
  equations.
- `ceilDiv(N,C)` is exactly supplied Python-style `(N+C-1)//C` for `C>0`.
  Its `[total]` declaration is too broad at `C=0`, where modulo/division by
  zero does not produce an integer normal form. Every claim that can depend on
  it requires `C>0`; the witness `ceilDiv(0,0)` shows the coverage gap, but no
  false entry-domain conclusion is enabled.
- The two priority-40 dispatch rules preserve every cell and arbitrary
  continuation. The typed sum/loop cases are exhaustive over `IntSeq` and
  `GridRows`; they yield exactly the same head and related tail as supplied
  list iteration. They do not introduce a fresh result oracle, return,
  exception, allocation, binding, or state update.
- The four bridge claims are proved in `MAX-FILL-DATA`, which imports supplied
  MPY but not the proposed bridges. Each is universal in its constructor tail
  and continuation (and, for loops, target/body), and together they cover both
  constructors of each input sort. Their destinations match the typed rules
  under the explicit representation relation.
- `rowTotal`/`fillTotal` are independent of `symRow`/`symGrid`, so using the
  same unconstrained symbol in execution and postcondition cannot make the
  proof circular.

Two independent sensitivity experiments reinforce the static review:

- Changing the submitted body's numerator offset from `Int(1)` to `Int(2)`
  builds successfully, then `fill-loop` fails with a residual equating the two
  distinct `fillTotal` expressions (`evidence/05_body_mutation.log`).
- Changing the typed sum bridge to yield `I+1` builds successfully, then
  `sum-fold` fails with the residual
  `rowTotal(A+I+1,IS)=rowTotal(A+I,IS)`
  (`evidence/05_bridge_mutation.log`).

I also attempted a separate whole-program proof over ordinary
`rowVals/gridVals`, importing no bridge rules
(`evidence/05_fixed_representation.k`). It builds, but K gets stuck after
symbolic `rowVals(IS)` loses its element sort and admits an arbitrary
non-int/non-bool head (`evidence/05_fixed_representation.log`). This is not a
false-behavior witness: every ground `IntSeq` reduces to integer-only
`rowVals`, and the candidate's universal constructor cases retain exactly that
fact. Still, the candidate does not contain one machine-checked,
whole-program, bridge-free connection theorem; the final stitching from the
four exhaustive cases to the compact typed representation is a transparent
static argument. I count this as a documented validation concern, not an
unsound rule. No concrete or symbolic witness was found in which an
inventoried candidate rule enables a false conclusion on `C>0`.

## 6. Fresh non-vacuity test

`evidence/06_false_postcondition.k` is reviewer-authored and changes the entry
destination from `maxFillSpec(GS,C)` to the demonstrably false
`maxFillSpec(GS,C)+1`. A satisfying witness is `GS=.GridRows, C=1`: execution
returns 0 while the mutation requires 1.

The dry run:

```text
timeout 300s kprove /audit-output/evidence/06_false_postcondition.k \
  -I /tmp/audit-work/115-max-fill \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The actual proof invocation built the spec, reached the destination shape, and
failed with `WarnStuckClaimState` and the precise unmet equality:

```text
fillTotal(0,GS,C) +Int 1 = fillTotal(0,GS,C)
EXIT_STATUS: 1
```

It did not time out, crash, or fail to parse. Full command/output:
`evidence/06_false_postcondition.log`. The proof is result-discriminating and
non-vacuous.

## 7. Proven versus assumed accounting

What the successful reachability proof establishes is:

> For every finite `GridRows` value and integer `C>0`, if the exact submitted
> `max_fill` function terminates under the supplied MPY semantics from the
> pinned clean configuration, its returned integer is
> `fillTotal(0,GS,C)`, i.e. the sum over rows of
> `(rowSum+C-1)//C`.

This is partial correctness. It is not a separate termination theorem, a proof
of all CPython behavior, or a proof about capacity zero/non-integer inputs.

The trust/assumption ledger is:

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied MPY semantics and K v7.1.337's compiler/Haskell backend/builtin integer, Boolean, map, and list theories | Every reachability result | Required selected-semantics trust boundary; candidate copy is byte-identical and rebuilt fresh. |
| Trusted `/reference/py2mpy.py` transliteration | Link from `solution.py` to `solution.mpy`/driver AST | Acceptable; fresh output is byte-identical. |
| `symRow/symGrid` representation relation | Symbolic sum, loop, and entry proof | Four bridge-free universal constructor cases plus exhaustive static simulation and sensitivity checks support it. The lack of one end-to-end bridge-free theorem is the main formal-evidence concern. |
| Ordinary integer identity `ceil(n/c)=(n+c-1)//c` for integer `n`, `c>0` | Link from `maxFillSpec` to prompt/canonical intent | Acceptable mathematics on the intended domain. |
| Prompt constraints (bits, row length at most 100, capacity 1..10) | Avoidance of canonical float precision/overflow differences | The formal theorem is broader for the submitted integer implementation; on the intended domain the bridge is exact. |
| Differential execution against trusted canonical and independent `divmod` oracle | Empirical implementation-to-intent support | 17,097 finite cases, zero mismatches; supportive only, not a substitute for the K proof. |
| Unused fixed-semantics opaque/concrete primitives (float operations, sort, MD5, etc.) | None on the reachable path | Excluded; they cannot affect this theorem. |
| `ceilDiv` totality at `C=0` | No entry or loop claim (`C>0` everywhere) | Over-broad declaration concern, outside the theorem; not used to prove an in-domain falsehood. |

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent
adequacy) passes on the documented domain. Gate C is reproducible for all
auditor-generated evidence, but the missing generation metadata/logs and the
case-wise rather than end-to-end representation connection justify retaining
concerns. The candidate remains legitimate: it executes the real submitted
body, constrains the returned value, rejects false mutations, and contains no
materially unsound proof rule on its stated domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
