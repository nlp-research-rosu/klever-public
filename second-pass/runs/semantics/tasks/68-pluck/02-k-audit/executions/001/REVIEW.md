# Independent adversarial audit: 68-pluck

This audit used the required `using-kit` then `validating-proof` workflow. The
rendered mode is `SUPPLIED_SEMANTICS`; consequently I did not use
`writing-semantics`. I treated every file under `/candidate` as untrusted, made
a source-only copy under `/tmp/audit-work/68-pluck`, and built every definition
there. K was available independently at version 7.1.337 even though `kup` was
not installed; see
[`evidence/00_environment.log`](evidence/00_environment.log).

The final assessment is **CONCERNS / LEGIT**. The proof reconstructs, is
non-vacuous, executes the submitted program AST, and has no materially unsound
proof-local rule. The concerns are evidence/bridge limitations rather than a
false or vacuous theorem: the theorem names its answer using an executable
`scanPluck` fold instead of formally stating a minimum/first-index predicate,
the equivalence of that fold to the English contract remains an audited
mathematical argument plus finite differential evidence, `asInt` is declared
`total` more broadly than its sole equation, and the expected generation
metadata/trace artifacts are absent.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required for
`SUPPLIED_SEMANTICS`. There is no infrastructure-mode contradiction, so a
candidate verdict is appropriate.

I recursively compared the candidate semantics tree against the trusted tree
with:

```text
diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
```

It exited 0 with no differences. A recursive type inventory found only ordinary
directories and regular files in that tree and no symlinks anywhere under
`/candidate`. Thus the candidate semantics tree has no missing, additional,
changed, mistyped, or symlinked entry. The complete commands, statuses,
inventories, and hashes are in
[`evidence/01_provenance.log`](evidence/01_provenance.log).

### Prompt, translator, and candidate artifacts

Both byte comparisons passed:

- `/candidate/prompt.py` equals `/reference/prompt.py`, SHA-256
  `cd3be7d4325387ffeafdc0c15742e1e5f66dfe1e94b683910809f5c17a9c3a74`.
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The required proof sources `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, and the complete supplied-semantics tree are present as
regular files. The following expected provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace (`*trace*` or `*.jsonl`)

Their absence limits reconstruction of the generation history, but it does not
substitute for or invalidate the fresh proof reconstruction below. Candidate
`prove.log`, `prove.sh`, `concrete_tests.py`, `concrete_tests.mpy`, and the
`__pycache__` entry were read or inventoried only as untrusted claims and were
not build inputs. No candidate `PROOF.md` or `spec-vacuity.k` was relied on.

**Stage 1 result:** integrity of every proof-relevant trusted/source artifact
passes; provenance metadata is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an array of non-negative integers, return `[v, i]`, where `v` is the
smallest even array value and `i` is the least index at which that value occurs.
Return `[]` when there is no even value, including the empty-array case. The
prompt's `1 <= nodes.length` constraint conflicts with its explicit empty-input
example; both the canonical implementation and the formal theorem cover the
empty case. The upper length bound is 10,000, while node values have no stated
upper bound.

The trusted canonical implementation filters even values, chooses their
minimum, and uses `arr.index` for the first occurrence. The candidate instead
scans once. Its `-1` sentinel is safe on the specified non-negative domain; it
replaces the candidate only for an even first value or a strictly smaller even
value. Equality therefore retains the earlier index. The index increments once
for every input element. This is a different but contract-equivalent algorithm
on the intended domain.

### Translation identity

I regenerated the term from the scratch copy of `solution.py` with the trusted
translator. `cmp` exited 0, and both submitted and regenerated files have
SHA-256
`5475741a3170980a2cf1714b3ba196e9afdb76777d1910af137995663b48ba7b`.
Commands and results are in
[`evidence/02_program_fidelity.log`](evidence/02_program_fidelity.log).

### Independent differential test

The reviewer-authored test
[`evidence/02_differential.py`](evidence/02_differential.py) imports
`/reference/canonical.py` and the scratch copy of the generated
`solution.py`. Its exact deterministic scope is:

- all four documented examples;
- named empty, singleton, all-odd, zero, first/later/equal-minimum, huge-integer,
  and 10,000-element boundary cases;
- all arrays of lengths 0 through 6 over values 0 through 5;
- 2,500 pseudorandom arrays using seed `680024`, lengths 0 through 100, and
  values 0 through 1,000,000.

That is 58,504 inputs, manifest SHA-256
`f044bfd3f126ff5f7c026f1e4668bbfe9556d1fae5c5d29d5f0646d2b87b5cc6`.
The run exited 0 with zero result mismatches and zero input mutations. The
script is the complete reproducible input generator; named large inputs are
also identified by length and hash in the log.

**Stage 2 result:** pass. No material program/canonical divergence was found on
the intended domain.

## 3. Clean proof reconstruction

I copied source files only, removed the two explicitly named scratch build
directories, and rebuilt:

1. `reference-semantics/semantics.k` with LLVM, main module `MPY-KRUN`;
2. `verification.k` with Haskell, main module `PLUCK-VERIFICATION`.

Neither candidate-compiled definitions nor caches were present or reused. The
LLVM definition loaded `solution.mpy` to a terminal configuration with `.K`,
empty stack, `NoExc`, and exit code 0. The exact bounded logs are in
[`evidence/03_reconstruction.log`](evidence/03_reconstruction.log).

Every positive target claim was then run:

- `PLUCK-SPEC.pluck-loop` independently: exit 0, `#Top`.
- `PLUCK-SPEC.pluck-correct`, with the just-proved loop claim selected and
  marked trusted as the explicit compositional dependency: exit 0, `#Top`.

The second invocation includes both claim labels and
`--trusted PLUCK-SPEC.pluck-loop`; it does not silently trust an untested
artifact because the loop claim was proved in the immediately preceding
independent invocation. A separate repetition is in
[`evidence/03_correct_recheck.log`](evidence/03_correct_recheck.log).

The compiler emitted non-exhaustiveness warnings for shared supplied-semantics
operations such as float conversions, `mapStrVS`, `joinCodes`, and
`valSeqAt`, plus unused-variable warnings in `strLt`. None of those
non-exhaustive operations occurs on the submitted program's execution path.
They are reported as trust/model boundaries below rather than misclassified as
a candidate proof failure.

**Stage 3 result:** pass. Both target claims close from clean source builds.

## 4. Adequacy and real-program pinning

### Claim meanings

`pluck-loop` says: if execution is at the exact `#loop` form for the submitted
for-loop, the current scope binds `smallest = B`, `smallest_index = BI`,
`index = I`, and `value = LAST`, and every remaining list element is a
non-negative integer, then consuming that remaining loop reaches the original
continuation `K`. The four locals become the four projections of
`scanPluck(VS, B, BI, I, LAST)`; `arr`, the parent, and all framed
configuration cells are preserved. The claim is an execution summary, so it
validly allows arbitrary already-reached values of `B`, `BI`, `I`, and
`LAST`; it does not assume an unproved prefix invariant.

`pluck-correct` says: from the exact initial MPY configuration, load a module
containing the submitted `pluck` body, invoke that closure on the semantic list
`VS`, and reach `ref(0)`. The module scope contains that exact closure; heap
location 0 contains `list(pluckResult(VS))`; the allocator advanced once; the
temporary call frame is gone; the stack and return state are reset; and there
is no exception with exit code 0. Its sole data precondition is
`allNonNegative(VS)`.

The postcondition is result-constraining. `ref(0)`, heap key 0, the list
contents, allocator, scopes, stack, return, exception, and exit-code cells are
all fixed. `pluckResult(VS)` is a recursively defined function, not a fresh
variable, existential oracle, tautology, or implication-only condition.

### Exact submitted-program pinning

The entry claim uses a normal verification harness: it first executes the
submitted module and then calls its `pluck` entry point with a symbolic
argument. I extracted the `Module(...)` subterm embedded in `spec.k`, parsed
both it and `solution.mpy` with the freshly built syntax, and compared canonical
KORE. The two KORE files are byte-identical, SHA-256
`654006d8a26c54a989fced05684e2344550932bc422a1e81c63a20d31f8d1779`.
See
[`evidence/04_program_pinning.log`](evidence/04_program_pinning.log) and
[`evidence/embedded-program.mpy`](evidence/embedded-program.mpy).

Thus the claim does not replace the program with `scanPluck`; it symbolically
executes the real AST. `scanPluck` appears only in the loop summary and final
specification.

### Satisfiable preconditions and ground substitutions

Examples of satisfying entry inputs are `.ValSeq` (empty),
`[4,2,3]`, `[5,0,3,0,4,2]`, and `[7,5,9]`. A loop-head witness is any exact
loop configuration with, for example, `VS = [4,2,3]`, `B = BI = -1`,
`I = 0`, and `LAST = 0`; all other cells can be the corresponding reachable
entry-call state.

Reviewer-authored K ground tests executed the actual body on six satisfying
inputs. They terminated with `.K`, `NoExc`, exit code 0, and heap results:

- `[] -> []`
- `[4,2,3] -> [2,1]`
- `[5,0,3,0,4,2] -> [0,1]`
- `[7,5,9] -> []`
- `[6,2,9,2] -> [2,1]`
- `[9,7,0] -> [0,2]`

Ground `pluckResult` reachability checks closed with `#Top`, and both Python
implementations printed the same six results. Artifacts and exact commands are
in [`evidence/ground_tests.py`](evidence/ground_tests.py),
[`evidence/ground-summary-spec.k`](evidence/ground-summary-spec.k), and
[`evidence/04_ground_checks.log`](evidence/04_ground_checks.log).

**Stage 4 result:** pass. The precondition is satisfiable, the submitted AST is
pinned, and its actual returned object is constrained.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/05_rule_inventory.txt`](evidence/05_rule_inventory.txt) is the
source-located exhaustive inventory over `semantics.k`, every supplied helper K
file, `verification.k`, and `spec.k`. It lists hashes, module/import edges,
every syntax declaration, configuration, context, rule, claim, and every line
carrying function/total/symbol/priority/owise/strictness attributes. The
inventory has 235 syntax-declaration starts, 716 rule starts, five contexts, one
configuration, and two claims. It found no `functional` or `simplification`
declaration. The supplied semantics contains its documented
`no-evaluators`/opaque boundaries; the candidate proof-local module contains
none.

The following table gives the disposition applied to every inventoried entry
in each file. “Unused” means no constructor or function from that module can be
reached by this program after the import graph and actual AST are considered;
it is still present in the inventory and remains part of the supplied-semantics
trust boundary.

| File/module | Inventory entries | Static disposition |
|---|---:|---|
| `semantics.k` / `MPY`, `MPY-KRUN` | assembly only | Import graph is coherent. `MPY-CONCRETE` is included only in LLVM, not in the proof definition. |
| `syntax.k` | 16 | AST constructors and strict/seqstrict annotations match the trusted translator. Used forms are `Module`, `FuncDef`, `Params`, `Assign`, `AugAssign`, `For`, `If`, `Return`, `Name`, `Int`, `UnaryOp`, `BinOp`, `Compare`/`CmpOp`, `ListExpr`, and `Call`. |
| `core.k` | 84 | Configuration, module sequencing, lookup, allocation, literal evaluation, argument order, and sequence helpers are coherent on the used path. All ten observable cells are either pinned by the entry claim or framed/preserved by the helper. |
| `iter.k` | 1 | Declares the iterator protocol only; no behavior or oracle is introduced. |
| `range.k` | 8 | Arithmetic and iterator rules are guarded and decreasing; unused here. |
| `operators.k` | 12 | Unary/binary/compare evaluation preserves operand order. Used integer dispatch is exact; heap-deref rules are not used for the raw integer elements. |
| `int.k` | 17 | `-`, `+`, `%`, `==`, and `<` rules used by this body agree with integer/Python arithmetic. `pyMod(V,2)` is defined and its divisor is never zero. |
| `bool.k` | 14 | Truth/short-circuit rules are coherent; only ordinary boolean results indirectly matter here. |
| `float.k` | 155 | Documented opaque float primitives and concrete twins are supplied-semantics trust boundaries, not candidate additions. No float constructor or rule is reachable here. |
| `str.k` | 33 | String iteration/arithmetic/order rules are unused. The compiler's unused-variable warning does not change any conclusion. |
| `set.k` | 18 | Set helpers are terminating and unused. |
| `list.k` | 32 | Used rules are the exact list iterator, list-literal left-to-right evaluation, allocation, and structural list equality in the ground harness. The symbolic input is a bare immutable semantic `list(VS)`; returned list syntax allocates once. |
| `tuple.k` | 25 | `#bindTgt(Name(...), V)` is used by `For`; it updates exactly the current scope. Tuple-only paths are unused. |
| `subscript.k` | 57 | Index/slice functions, including the documented total-but-underspecified out-of-bounds boundary, are unused. |
| `comprehension.k` | 10 | Macro expansions are unused and cannot preempt this AST. |
| `methods.k` | 102 | String/list method helpers are unused. The warned broad `joinCodes` totality has no dependent claim here. |
| `controls.k` | 37 | Assignment and augmented assignment update the current locals; `If` uses integer truth/comparisons; `For` evaluates the iterable once, binds one element, executes the body, and returns to the structurally smaller tail. Break/while/import paths are unused. |
| `functions.k` | 19 | `FuncDef`, parameter binding, return, and frame pop match the call path. The return discards the remaining function continuation, stores the returned reference, restores the caller environment, and leaves escaped heap allocation intact. |
| `builtins.k` | 175 | The builtins scope is available, but the body invokes none. Opaque `md5hexCodes` and broad unused total helpers have no control/result influence here. |
| `call.k` | 24 | Callee lookup and argument evaluation are left-to-right. The closure rule binds the submitted body and exact argument, pushes a frame, and restores it on return. No syntactic call interception applies to `pluck`. |
| `sort.k` | 25 | `sortVS`/`sortKeyVS` are documented opaque trusted primitives, but no `sorted` call occurs and neither symbol appears in a claim. |
| `assert.k` | 3 | Unused by the theorem; used only in reviewer concrete harnesses where failures set exit code 1. |
| `dict.k` | 40 | Dict syntax, updates, equality, and lookup are unused. |
| `concrete.k` | 21 | LLVM-only deep equality/keyed-sort rules are unused by the submitted body and absent from the Haskell proof definition. |
| `verification.k` | 29 (8 syntax, 21 rules) | Every proof-local declaration/rule is analyzed individually below. |
| `spec.k` | 2 claims | Both exact reachability claims are analyzed in Stage 4 and reconstructed in Stage 3. |

The used-construct coverage map is:

| Submitted construct | Declaration | Execution rules |
|---|---|---|
| `Module`, statement sequence, empty `Stmts` | `syntax.k:56,61` | `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` |
| `Name` lookup | `syntax.k:12` | `core.k:130-154` |
| `Assign` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18` |
| `Int`, `UnaryOp("-")` | `syntax.k:9,14` | `core.k:194`; `operators.k:10`; `int.k:7` |
| `For` over `list(VS)` | `syntax.k:45` (`strict(2)`) | `controls.k:65-74`; `list.k:9-10`; candidate integer iterator specialization |
| `If` | `syntax.k:49` (`strict(1)`) | `controls.k:51-54`; `core.k:199-205` |
| `BinOp("%")`, `BinOp("+")` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; `int.k:9,15,19-20` |
| `Compare`, `CmpOp("=="/"<")` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:22,26` |
| `AugAssign("+")` | `syntax.k:44` (`strict(3)`) | `controls.k:20-31`; `int.k:9` |
| `ListExpr`, empty `Exprs` | `syntax.k:17,37` | `list.k:13-15`; `core.k:117-121,183-191` |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:77-90` |
| `Call` of `pluck` | `syntax.k:28` | `call.k:18-21,69-75`; `functions.k:62-90` |

No submitted constructor relies on an absent semantic rule or on an unrelated
opaque operation.

### Proof-local extension decisions

`verification.k` contains no hidden import, macro, simplification, opaque
symbol, `no-evaluators`, or unguarded program-call interception.

- `asInt`: the one equation `asInt(I:Int) => I` is a truthful projection.
  Every result-bearing use is under `isInt(V)` derived from
  `allNonNegative`, or in the iterator rule's explicit guard. Its `[total]`
  attribute is broader than its equations: on a non-integer `Val`, it is an
  unspecified total value. That is a real reuse/evidence concern, but the
  intended precondition excludes every such use. I found no satisfying
  intended-domain state in which the unspecified case can influence a branch
  or result, so I do **not** label it unsound.
- The priority-40 iterator rule is an operational specialization. On
  `isInt(V)`, `V` is an integer injection and `asInt(V)` is that same integer.
  Its right-hand side is therefore exactly the supplied rule in `list.k`;
  arbitrary continuation and every omitted cell are preserved. I compiled a
  definition importing only fixed `MPY` and proved the bridge-free universal
  connection for every integer head, tail, and continuation. It exited 0 with
  `#Top`; see
  [`evidence/iter-bridge-connection.k`](evidence/iter-bridge-connection.k) and
  [`evidence/05_iter_bridge_check.log`](evidence/05_iter_bridge_check.log).
  This rule does not fabricate a value, pop control, or skip the loop body.
- `pluckTake` is a truthful Boolean formula for “even and either no candidate
  or strictly smaller.” It is unused by both claims and cannot affect closure.
- The four guarded `nextBest` equations are mutually exclusive and exhaustive
  over integers: odd; even with sentinel; even/non-sentinel and smaller; and
  even/non-sentinel and greater-or-equal. The four `nextBestIndex` equations
  use the identical partition and update the index exactly when the value
  updates. Equal values retain the earlier index.
- The two `scanPluck` equations are constructor-exhaustive on `ValSeq`. The
  recursive rule removes one `vCons`, increments the index once, records the
  current value as `LAST`, and calls the two just-audited update functions.
  It terminates structurally. Its broad declared domain inherits the
  `asInt` caveat only outside `allNonNegative`.
- `stateBest`, `stateBestIndex`, `stateIndex`, and `stateLast` are exact,
  non-overlapping projections from the sole state constructor `pstate`.
- The two `pluckResult` guards (`best == -1` and `best =/= -1`) are disjoint
  and exhaustive. The first yields empty; the second yields exactly two
  elements, best then its retained first index.
- The two `allNonNegative` equations are constructor-exhaustive and decreasing.
  They require each head to be an integer at least zero and recursively require
  the tail. This is the exact formal input domain used by both claims.

The ordinary-mathematics induction behind the intent bridge is: after scanning
each prefix, `B = -1` exactly when that prefix has no even value; otherwise
`B` is its least even value and `BI` is the first index of that value. The four
update cases preserve this fact, and the base case yields the requested output.
This argument is valid, but it is not itself encoded as a separate K claim
against a mathematical minimum/first-index predicate. That distinction is one
reason for `CONCERNS`, not a claim that a rule is false.

No inventoried candidate rule was classified as unsound. Accordingly there is
no false-conclusion witness to report for an alleged unsound rule; narrower
gaps such as broad unused totality and informal intent connection are stated
as such.

**Stage 5 result:** sound on the complete claimed/intended domain; documented
non-material trust/evidence concerns remain.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I copied `spec.k` in scratch
and changed only the result-bearing heap postcondition from
`list(pluckResult(VS))` to `list(.ValSeq)`, i.e. the deliberately false theorem
that every satisfying input returns an empty list. The mutation is preserved
at [`evidence/spec-vacuity.k`](evidence/spec-vacuity.k).

`kprove --dry-run` exited 0, establishing that the mutated specification parses
and builds against the clean proof definition. The real mutation proof then
exited 1, not by timeout, parser error, missing import, or unrelated crash. It
reported `WarnStuckClaimState` on the branch
`stateBest(scanPluck(...)) =/= -1`; the residual heap contains the actual
two-element result while the destination requires empty. The concrete
satisfying witness `[4,2,3]` printed `[2,1]`.

The exact diff, commands, exit statuses, bounded residual, and witness are in
[`evidence/06_nonvacuity.log`](evidence/06_nonvacuity.log). This demonstrates
that the positive proof genuinely constrains the return value.

**Stage 6 result:** pass.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied MPY semantics and proof-local definitions, for every finite
`ValSeq` whose elements satisfy `allNonNegative`, starting from the exact
initial configuration in `pluck-correct`, loading the exact submitted module
and invoking `pluck` reaches the exact terminal state described in Stage 4.
The returned reference points to `list(pluckResult(VS))`. The separately
proved loop circularity establishes the exact local-state fold for every
remaining tail and arbitrary continuation.

This is a partial-correctness reachability result. It does not claim behavior
for negative elements, booleans treated as Python integers, non-integers,
non-list inputs, malformed calls, or alternate initial heaps/scopes. It does
not independently prove CPython as a whole or make a separate formal
termination claim.

### Trust and assumption ledger

| Boundary | Dependents and influence | Assessment/evidence |
|---|---|---|
| Supplied MPY semantics and K built-in Int/Bool/Map/List hooks | All execution, state, allocation, call, and arithmetic conclusions | Authorized fixed semantics; candidate tree is byte-identical. Relevant rules were statically checked. |
| K compiler/Haskell prover/LLVM runtime v7.1.337 | `#Top`, concrete execution, parsing | Standard low-level toolchain trust; versions and fresh commands recorded. |
| Trusted `py2mpy.py` as the Python-AST-to-MPY bridge | Identity of Python source and executed MPY AST | Candidate translator matches trusted mount; regeneration is byte-identical. This is a trusted front-end, not proved inside K. |
| Independently proved `pluck-loop` claim | Entry proof's loop execution | Acceptable compositional dependency: separately exit 0/`#Top`, then explicitly trusted in the entry invocation. |
| Candidate priority iterator specialization | Symbolic exposure of integer list heads | Acceptable derived operational bridge; exact fixed-semantics connection independently proved without importing it. |
| `asInt` totality outside integer inputs | Could be value-bearing if reused on non-integer lists | Concerning but inert here: every dependent reachable use is integer-guarded by the formal precondition. |
| `scanPluck` means “least even and first index” | Bridge from K postcondition to English task intent | Mathematically audited and strongly differentially supported, but no separate K minimum/first-index theorem. This is the principal adequacy limitation. |
| Trusted canonical Python implementation | Oracle for differential/ground tests only | 58,504 zero-mismatch cases; finite evidence, not a universal proof and not used to close K claims. |
| Opaque float/sort/md5 and incomplete unused helpers in supplied semantics | None: no corresponding constructor/symbol is reachable or appears in the claims | Acceptable inert supplied-semantics boundary for this theorem; would require renewed audit if the program used them. |
| Missing generation metadata and structured trace | Auditability of how the candidate was produced | Evidence concern only; the independent source reconstruction does not rely on those claims. |

The proof does not use candidate prose, candidate traces, candidate compiled
definitions, candidate `#Top`, or differential testing as a substitute for K
reachability. Differential evidence supports only the Python/intent bridges
identified above.

**Stage 7 result:** the formal execution theorem is legitimate and its trust
boundary is explicit. The informal summary-to-English bridge and incomplete
generation provenance justify concerns but do not enable a false conclusion or
detach the proof from the submitted program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
