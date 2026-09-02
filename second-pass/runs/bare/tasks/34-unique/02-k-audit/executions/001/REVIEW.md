# Independent adversarial audit: 34-unique

Decision: **CONCERNS / LEGIT**.

The candidate contains a cleanly reconstructible, non-vacuous K reachability
proof that is pinned to the submitted translated program and is sound on its
represented domain of finite integer lists. The principal limitations are that
the symbolic postcondition reuses the same `dedupInts` and `sortInts` functions
used by the generated semantics (so `kprove` reports the claim as trivial and
does not independently prove the words “sorted” and “unique”), and that the K
model does not represent the broader non-integer inputs accepted by the Python
implementation. No rule was found that enables a false result on the intended
integer-list domain.

All candidate artifacts were treated as untrusted evidence. Candidate-built
definitions and caches were not used. Fresh work was performed below
`/tmp/audit-work/34-unique`; reviewer scripts, mutations, and bounded logs are
preserved in `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as this mode requires. The trusted
tree contains only:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

There is therefore no infrastructure contradiction and no hidden or inferred
reference semantics was used. See
[`artifact-inventory.log`](evidence/artifact-inventory.log).

### Required artifacts and types

The required candidate artifacts `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh` are
all regular files. The requested untrusted provenance files `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, and the JSONL generation
trace are also present and regular. There are no symlinks anywhere under
`/candidate`.

No required artifact is missing or mistyped. There are no candidate helper K
files beyond the three declared K sources. Additional top-level material is
`__pycache__/`, `semantic-kompiled/`, `verification-kompiled/`,
`kore-exec.tar.gz`, and `codex-trace/`. These are untrusted generated caches or
diagnostics, not source inputs; all were inventoried and ignored for
reconstruction.

The untrusted claims say that generation exited 0 in 335 seconds and that
`kprove` produced `#Top`. The complete 131-record JSONL trace parses without a
malformed record and contains the same final claim. These statements were not
used as proof evidence. See
[`generation-trace-summary.log`](evidence/generation-trace-summary.log).

### Trusted-file comparison

Byte comparisons and hashes show:

- candidate `prompt.py` equals trusted `/reference/prompt.py`;
- candidate `py2mpy.py` equals trusted `/reference/py2mpy.py`;
- their SHA-256 values are respectively
  `c48cad1505632ee1c7534d4b5dc430767155942186f1f0eb2c3e46074c1111a6`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Exact commands, comparison statuses, and hashes are in
[`provenance.log`](evidence/provenance.log). All relevant source artifacts were
copied to scratch before execution.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `unique(l: list)` to return the sorted unique elements
of the input list. The trusted canonical implementation is:

```python
return sorted(list(set(l)))
```

Thus, on normal return, the result is a Python list in ascending order with one
representative of each distinct input value. CPython additionally requires
members to be hashable for `set` and mutually orderable for `sorted`; inputs
outside those conditions raise rather than return normally.

The candidate is:

```python
return sorted(set(l))
```

For every input on which either expression normally returns, the explicit
`list(...)` in the canonical implementation is redundant because `sorted`
accepts any iterable and itself returns a list. The two implementations also
exhibit the same relevant exceptions for unhashable or non-orderable members.

### Translation fidelity

Running the trusted translator from the scratch copy:

```text
python3 /tmp/audit-work/34-unique/reference/py2mpy.py \
  /tmp/audit-work/34-unique/candidate-source/solution.py \
  > /tmp/audit-work/34-unique/regenerated-solution.mpy
```

exited 0. The regenerated term is byte-identical to submitted `solution.mpy`;
both have SHA-256
`7c0cfa7a98969b3f9b780674f2e26b0a959757bae15d017b1ec0ee8479f84b72`.

### Independent differential execution

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and scratch-copied candidate under distinct module names. Its input
scope is:

- the documented example;
- empty, singleton, duplicate, sorted, reverse, negative, zero, equal, and
  extreme-integer cases;
- sortable strings, booleans/integers, tuples, and floats;
- unhashable and non-mutually-orderable exception cases;
- every list of lengths 0 through 6 over `[-2,-1,0,1,2]`;
- 1,500 deterministic generated integer lists, seed `340034`, lengths 0
  through 30, values from -1000 through 1000.

The expanded run covered 21,048 inputs, observed zero result/exception
mismatches, and observed no input mutation. Its ordered input digest, commands,
and exit 0 are in
[`differential-expanded.log`](evidence/differential-expanded.log).

## 3. Clean proof reconstruction

K version `v7.1.293` was used; version commands and statuses are in
[`toolchain-version.log`](evidence/toolchain-version.log).

No candidate `*-kompiled` directory or cache was copied. From source, the audit
built:

1. an LLVM concrete definition from `candidate-source/semantic.k`, main module
   `MPY`, syntax module `MPY-SYNTAX`, output
   `/tmp/audit-work/34-unique/concrete-kompiled`;
2. a Haskell proof definition from `candidate-source/verification.k`, main
   module `VERIFICATION`, syntax module `MPY-SYNTAX`, output
   `/tmp/audit-work/34-unique/proof-kompiled`.

Both `kompile` commands exited 0. Exact commands and statuses are in
[`clean-build.log`](evidence/clean-build.log).

### Concrete generated-semantics execution

The fresh LLVM definition executed the actual scratch copy of submitted
`solution.mpy` on seven cases:

- documented list;
- empty list;
- all-equal list;
- the insertion `<=` boundary `[1,2]`;
- the insertion `>` boundary `[2,1]`;
- negatives, zero, and duplicates;
- very large positive and negative integers.

Every `krun` exited 0, produced a fully evaluated `VList`, and matched both
Python implementations. This set exercises empty/singleton/recursive expression
lists, equal/unequal removal, empty/recursive deduplication and sorting, and
both guarded insertion branches. The exact `krun` commands, complete bounded
results, and zero mismatch count are in
[`concrete-compare-corrected.log`](evidence/concrete-compare-corrected.log).

For transparency,
[`concrete-compare.log`](evidence/concrete-compare.log) is an earlier reviewer
harness run in which every `krun` itself exited 0 but the harness failed to
accept whitespace in K's pretty printer. The corrected parser changed no
candidate or K source and the corrected run above supersedes that harness
failure.

### Positive claims

The two candidate claims were copied without logical changes into separate
reviewer modules and independently run:

```text
kprove spec-symbolic.k --definition proof-kompiled \
  --spec-module SPEC-SYMBOLIC
kprove spec-example.k --definition proof-kompiled \
  --spec-module SPEC-EXAMPLE
```

Each exited 0 and printed `#Top`. The exact commands and outputs are in
[`positive-proofs.log`](evidence/positive-proofs.log). The original, unmodified
two-claim `candidate-source/spec.k` was also run against the fresh definition;
it exited 0 and printed `#Top`, as recorded in
[`positive-original-spec.log`](evidence/positive-original-spec.log).

K emitted `WarnTrivialClaim` (“Claim proven without rewriting”) for both
claims. This is not an execution failure. It is explained by K's simplification
of `[function]` equations on both sides, and it motivates the adequacy and
static checks below.

## 4. Adequacy and real-program pinning

### Symbolic entry claim

The first claim has no explicit `requires` clause. In plain language:

> Starting with the exact translated AST of a one-argument `unique` whose body
> is `return sorted(set(l))`, applied to `VList(L)`, the `<k>` cell reaches
> `VList(uniqueSpec(L))`.

`uniqueSpec(L)` is defined as `sortInts(dedupInts(L))`. For a well-formed
integer-list encoding
`L = ListItem(VInt(i1)) ... ListItem(VInt(in))`, that is a concrete,
input-dependent result. It is neither a free return variable nor a one-way
boolean implication.

Although the syntactic K precondition accepts any K `List`, meaningful complete
evaluation is only defined when its elements are `VInt`. On other K list
contents, the same partial function terms can remain on both sides and the
claim does not establish a Python result. The effective theorem domain is
therefore finite integer lists, a limitation recorded in the verdict.

A satisfying state is obtained with `L = .List`. Another is
`L = ListItem(VInt(2)) ListItem(VInt(1))`; substitution yields
`VList(ListItem(VInt(1)) ListItem(VInt(2)))`, matching K, candidate Python, and
canonical Python in the concrete comparison log.

### Concrete example claim

The second claim also has no explicit `requires` clause. It starts `run` on the
same exact function AST and the prompt's documented `ListExpr`. Its
postcondition is the fully concrete list `[0,2,3,5,9,123]`. The entry
configuration itself is a satisfying state, and the result matches both Python
implementations.

### Pinning

Both `<k>` cells contain exactly:

```text
Module(
  FuncDef("unique", Params("l"),
    Return(Call(Name("sorted"), Call(Name("set"), Name("l"))))))
```

This is byte-for-byte the trusted-translator output from the actual submitted
`solution.py`. The claims do not invoke a substitute helper, oracle, or
unconstrained function body. There are no loop or auxiliary reachability
claims to match.

As a body-sensitivity check, the reviewer changed the scratch program to
`return set(l)`, translated it with the trusted translator, and ran it. Fresh K
execution changed to `VSet(...)`; a reachability claim demanding the original
`VList(uniqueSpec(L))` then exited 1 with `WarnStuckClaimState`. The mutation,
exact commands, and output are in
[`body-sensitivity.log`](evidence/body-sensitivity.log), with the mutated
artifacts preserved as
[`body-mutation.py`](evidence/body-mutation.py),
[`body-mutation.mpy`](evidence/body-mutation.mpy), and
[`spec-body-sensitivity.k`](evidence/spec-body-sensitivity.k).

## 5. Rule-by-rule static soundness review

There are no generated helper K files. The complete source-level declaration
and rule extraction is in
[`rule-inventory-source.log`](evidence/rule-inventory-source.log).

### Syntax, configuration, and attributes

The local syntax inventory is exhaustive:

| Result sort | Productions |
|---|---|
| `Program` | `Module(Stmts)` |
| `Stmt` | `FuncDef(String, Params, Stmts)`; `Return(Expr)` |
| `Stmts` | `List{Stmt, ""}` |
| `Params` | `Params(Strings)` |
| `Strings` | `List{String, ","}` |
| `Expr` | `Int(Int)`; `Name(String)`; `ListExpr(Exprs)`; `Call(Expr, Exprs)` |
| `Exprs` | `List{Expr, ","}` |
| `Val` constructors | `VInt(Int)`; `VList(List)`; `VSet(List)` |
| `Val` functions | `apply(Program,Val)`; `eval(Expr,String,Val)`; `makeSet(Val)`; `sortSet(Val)`; `run(Program,Expr)` |
| `List` functions | `evalExprs(Exprs,String,Val)`; `dedupInts(List)`; `removeInt(Int,List)`; `sortInts(List)`; `insertInt(Int,List)` |
| verification `List` function | `uniqueSpec(List)` |

All eleven named functions carry `[function]`. There are no `[total]`,
`[functional]`, `[simplification]`, priority, `owise`, macro, alias, opaque,
fresh-symbol, or trusted-rule declarations. Every local function has visible
equations. The source configuration has only
`<k> run($PGM:Program, $ARGS:Expr) </k>`; there are no hidden state, heap,
environment, allocation, I/O, exception, or call-stack cells.

### Construct coverage

Every construct in submitted `solution.mpy` is declared and consumed:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` | `Program`; destructured by `apply` |
| `FuncDef` | `Stmt`; exact sole-definition shape consumed by `apply` |
| `Params("l")` | `Params`/`Strings`; binds `X` in `apply` |
| `Return` | `Stmt`; exact body passed to `eval` |
| outer `Call(Name("sorted"),...)` | `Expr`; `eval` selects `sortSet` |
| inner `Call(Name("set"),...)` | `Expr`; `eval` selects `makeSet` |
| `Name("l")` | `Expr`; exact-name lookup returns the argument value |

`ListExpr`, `Int`, and `Exprs` are not in the source body but are required for
the configured runtime argument and the concrete example; all are covered by
`eval`/`evalExprs`. Missing semantics for unrelated translator constructs is
permitted in generated-semantics mode and cannot silently match this program.

### Exhaustive equation inventory

| ID | Exact rule family | Static decision |
|---|---|---|
| S1 | `apply(Module(FuncDef(_F, Params(X), Return(E))), V) => eval(E,X,V)` | Sound for the target's sole, one-parameter, single-return definition. It directly evaluates the real body and binds the real argument. `_F` broadens reuse to other sole functions but cannot alter this exact program. |
| S2 | `eval(Int(I),_,_) => VInt(I)` | Faithful unbounded integer literal evaluation. |
| S3 | `eval(Name(X),X,V) => V` | Faithful for the bound parameter `l`; exact string equality prevents a different name from matching. |
| S4 | `eval(ListExpr(ES),X,V) => VList(evalExprs(ES,X,V))` | Faithful for runtime integer list literals; order is preserved. |
| S5 | `eval(Call(Name("set"),E),X,V) => makeSet(eval(E,X,V))` | Sound for the actual unshadowed builtin call and pure integer argument. It does not model arbitrary Python name rebinding. |
| S6 | `eval(Call(Name("sorted"),E),X,V) => sortSet(eval(E,X,V))` | Sound for the actual unshadowed builtin call on the `VSet` produced by S5. |
| S7 | `evalExprs(.Exprs,_,_) => .List` | Correct empty argument-list base case. |
| S8 | singleton `evalExprs(E:Expr,X,V)` | Correct singleton case; concrete singleton execution reached it. |
| S9 | recursive `evalExprs((E,ES),X,V)` | Preserves left-to-right element order and structurally descends through `ES`. The grammar separates it from S8. |
| S10 | `makeSet(VList(L)) => VSet(dedupInts(L))` | Correct abstract integer-set construction: later equal integers are discarded. Its internal order is not observable in the submitted program except through sorting. |
| S11 | `sortSet(VSet(L)) => VList(sortInts(L))` | Correct on the representation invariant established by S10. A syntactically hand-built `VSet` may contain duplicates, but no intended input reaches such a value; this is an over-broad representation boundary, not an intended-domain false-rule witness. |
| S12 | `dedupInts(.List) => .List` | Correct base case. |
| S13 | head `dedupInts` rule | Retains one head and removes every later equal value before recursion. The recursive argument is shorter than the original list. |
| S14 | `removeInt(_, .List) => .List` | Correct base case. |
| S15 | equal-head `removeInt` rule | Correctly removes an equal integer and descends. |
| S16 | unequal-head `removeInt` rule with `I =/=Int J` | Correctly preserves a distinct integer and descends. Its guard is disjoint from S15 and together they cover integer heads. |
| S17 | `sortInts(.List) => .List` | Correct insertion-sort base case. |
| S18 | head `sortInts` rule | Sorts the shorter tail, then inserts the head. |
| S19 | `insertInt(I,.List) => ListItem(VInt(I))` | Correct empty insertion. |
| S20 | insertion with `I <=Int J` | Correctly places `I` before the first no-smaller head. |
| S21 | insertion with `I >Int J` | Correctly preserves the smaller head and descends. S20/S21 are disjoint and exhaustive over K integers. |
| S22 | `run(P,ARG) => apply(P,eval(ARG,"",VList(.List)))` | Correctly evaluates the configured list expression and directly invokes the sole submitted function. The dummy environment is irrelevant because list elements are integer literals. |
| V1 | `uniqueSpec(L) => sortInts(dedupInts(L))` | A truthful definitional summary on well-formed integer lists. It does not replace LHS program execution, but it shares the semantic helper implementations, so it is not an independent machine-checked sortedness/uniqueness theorem. |

For finite `VInt` lists, all recursive equations descend structurally. The
equality/inequality and `<=`/`>` guards are mutually exclusive and exhaustive.
There are no conflicting overlaps. Insertion sort produces nondecreasing order;
`dedupInts` preserves exactly one occurrence of each integer; sorting then makes
the retained representative order irrelevant. These facts follow by ordinary
structural induction, but the candidate did not state or prove those induction
lemmas separately in K.

The source expression is pure and has no user-observable intermediate state, so
the equational evaluator's lack of explicit `seqstrict` continuations causes no
difference for this program. Directly interpreting `Return(E)` also preserves
the only control effect present. Python allocation identities and resource
failures are outside the represented observation.

Two intentionally narrow evidence gaps were not mislabeled as unsoundness:

- name-based builtin selection would be wrong for a different module that
  shadows `set` or `sorted`, but the submitted module has no such binding;
- `VSet(List)` lacks an enforced no-duplicates sort invariant, but every
  intended call to `sortSet` receives S10's deduplicated result.

Neither admits a false conclusion for an actual intended integer-list
execution, so no false-conclusion witness exists within that domain. They
limit reuse of the semantics rather than invalidate this proof.

## 6. Fresh non-vacuity test

The reviewer-created mutation is
[`spec-vacuity.k`](evidence/spec-vacuity.k). It changes the symbolic
postcondition from:

```text
VList(uniqueSpec(L))
```

to:

```text
VList(ListItem(VInt(0)) uniqueSpec(L))
```

The original precondition remains satisfiable. For witness `L = .List`, both
Python implementations and fresh K execution return `[]`; the mutation demands
`[0]`.

`kprove --dry-run` exited 0, showing that the mutation parsed and built against
the fresh proof definition. Actual `kprove` exited 1 with
`WarnStuckClaimState`; the residual explicitly contains the failed equality
between `ListItem(VInt(0)) sortInts(dedupInts(L))` and
`sortInts(dedupInts(L))`. The witness script exited 0. Exact commands, statuses,
and residual are in
[`false-mutation.log`](evidence/false-mutation.log). This is an expected unmet
result obligation, not a parser error, missing import, crash, or unreachable
mutation.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted generated K semantics:

1. applying the exact submitted AST to an encoded list reaches
   `VList(sortInts(dedupInts(L)))`;
2. running the exact AST on the documented concrete expression reaches the
   exact expected integer list;
3. the result is discriminating—an added result element is rejected; and
4. the result is body-sensitive—a modeled body change to `return set(l)`
   changes execution and invalidates the list-result claim.

For well-formed finite integer encodings, the audited definitions of
`dedupInts` and `sortInts` mean that the result is precisely the ascending list
of distinct input integers.

### Trust ledger and limitations

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293, Haskell/LLVM backends, `domains.md`, K `Int` and `List` | Parsing, integer comparisons, collection representation, concrete execution, and proof closure | Necessary low-level tool/library trust; acceptable. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to the exact AST in `solution.mpy` and both claims | Explicitly trusted input; byte identity was independently checked. |
| Generated AST evaluator (`apply`, `eval`, `evalExprs`, `run`) | Connects the submitted AST to K values and control | Audited rule-by-rule and concretely exercised. Sound for this pure one-function program, but not a general Python semantics. |
| Integer `set` contract (`makeSet`, `dedupInts`, `removeInt`) | Determines which values survive | Equations are visible, terminating on represented inputs, and mathematically correct; no opaque oracle. |
| Integer `sorted` contract (`sortSet`, `sortInts`, `insertInt`) | Determines result order and list type | Equations are visible, guarded, terminating on represented inputs, and mathematically correct; no opaque oracle. |
| Summary `uniqueSpec` | Symbolic postcondition | Truthful but definitionally reuses the two semantic helpers. Its human-facing meaning rests on the audited informal induction, not a separate K property theorem. This is the main evidence concern. |
| Python candidate-to-canonical bridge | Shows implementation matches the trusted reference | Source reasoning plus 21,048 finite differential cases. Strong empirical support, not a universal K theorem. |
| Generated-semantics-to-Python bridge | Shows the small K model agrees with concrete Python behavior | Seven normal/boundary K comparisons exercise every local rule branch. Finite evidence plus static reasoning; not a formal CPython refinement proof. |

There are no opaque symbols, fresh result variables, proof-local operational
bridges, trusted claims, priority shortcuts, or unconstrained oracles.

The proof does **not** establish:

- total correctness or termination for arbitrary K `List` contents;
- behavior for Python strings, floats, tuples, booleans, mixed types,
  unhashable elements, or exceptions, despite the Python implementation and
  canonical implementation agreeing on the tested examples;
- arbitrary Python scoping, builtin shadowing, side effects, exceptions,
  allocation identity, or resource behavior;
- a separately machine-checked theorem that `uniqueSpec` is sorted and
  duplicate-free.

These limitations do not enable a false result on the represented
integer-list domain, and the proof executes the real submitted body rather
than substituting a result oracle. They do, however, prevent a `PASS`: the
formal evidence for the English contract is partly an audited mathematical
bridge, and the prompt's unqualified `list` domain is broader than the K
value model. The appropriate decision is therefore `CONCERNS / LEGIT`, not
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
