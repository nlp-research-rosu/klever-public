# Independent adversarial audit: 22-filter-integers

## Executive decision

The candidate's 17 submitted reachability claims reconstruct successfully, and
the individual claims appear sound over the candidate's deliberately small
`PyVal` model.  That is not, however, a partial-correctness proof of the
HumanEval contract.

The only whole-program entry claims use two concrete prompt inputs.  The
remaining claims are evaluator reductions for empty, one-head, or fixed-length
lists and two examples about a separately defined filter function.  There is no
whole-program claim for an arbitrary input list and no universal connection
claim from `comprehend(VList(VS), ...)` to
`VList(onlyIntegerInstances(VS))`.  A fresh audit formulation of that missing
modeled-domain theorem builds but gets stuck on exactly that equality.

The entry claims also place a hard-coded `solutionModule()` in the `<program>`
cell rather than parsing or otherwise referring to the submitted
`solution.mpy`.  The hard-coded term is textually the same as the current
submitted term, so the two concrete theorems do describe the current program.
But that identity is an external audit observation, not a proof dependency:
after a material scratch mutation of `solution.mpy`, concrete execution changed
to `[]` while the entry proof still closed with `#Top`.

These are material theorem-scope and pinning failures, not mere thin testing.
The candidate proves correct examples and local equations, not the requested
general result.

## 1. Input and provenance integrity

### Mode and trusted mount boundary

The rendered mode is `GENERATED_SEMANTICS`.  The trusted mount contains exactly
the expected trusted inputs at its root:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` is absent, including as a symlink.  This is
consistent with the rendered mode, so there is no infrastructure breach and a
candidate verdict is appropriate.  See `evidence/01-provenance.log`.

### Candidate artifact types and comparisons

All of the following candidate artifacts are regular files, not symlinks:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`.  The structured trace is present as
one regular JSONL file.  A recursive symlink search found none anywhere below
`/candidate`.

The candidate and trusted copies are byte-identical:

| Artifact | SHA-256 |
|---|---|
| `prompt.py` | `b7bde40423debe285816bdcee858624a7ded823a414e8cf0e71d1185fc6cdb32` |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |

Those hashes also agree with the untrusted hash claims in `run-input.json`.
The condition recorded there says no kit and no supplied semantics, which is
consistent with generating `semantic.k`.

Additional candidate-side artifacts are `__pycache__/` and three compiled
definition trees: `semantic-kompiled/`, `semantic-proof-kompiled/`, and
`verification-kompiled/`.  They are extra build/cache evidence, not trusted
source.  None was copied into scratch or used by this audit.  `codex-trace/` is
additional generation evidence.  No `PROOF.md` or candidate
`spec-vacuity.k` exists; neither was a deliverable of the recorded bare
generation prompt.

The scratch copy command and its zero status are in
`evidence/02-scratch-copy.log`.  Only source files were copied.  The complete
source and tool hash/listing record is in
`evidence/15-source-and-tool-inventory.log`.

### Untrusted generation claims

The audit read and parsed `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all 316 JSONL trace records without importing or
executing candidate code.  The bounded summary and hashes are in
`evidence/03-untrusted-claims.log`.

The final candidate claim is that all 17 claims produced `#Top`.  Earlier parts
of the log also contain stuck proofs and compiler errors during construction.
Neither the final success claim nor the earlier failures were trusted.  Fresh
reconstruction below independently confirms the final positive executions.

**Stage 1 result:** PASS.  No provenance or generated-semantics mount integrity
failure was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For an input `values: List[Any]`, `filter_integers` must return the stable
subsequence containing exactly the elements `x` for which
`isinstance(x, int)` is true.  It must preserve order and duplicates.  Empty
input yields empty output.  Python booleans and user-defined subclasses of
`int` are included because both satisfy `isinstance(x, int)`.

The trusted canonical implementation is:

```python
return [x for x in values if isinstance(x, int)]
```

The submitted implementation is the same algorithm, with `value` in place of
`x`.  There is no source-level implementation discrepancy.

### Trusted translation

The exact command was:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
sha256sum solution.mpy regenerated-solution.mpy
cmp --verbose solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`2c9616677b79795d1805d8100b5fabfb5a915713692b441027cef321ab554607`;
`cmp` exited 0.  See `evidence/04-mpy-regeneration.log`.  Thus the submitted
`solution.mpy` is byte-identical to a fresh translation of the submitted
Python by the trusted translator.

### Independent Python differential

`evidence/differential.py` imports the oracle directly from
`/reference/canonical.py` and the generated entry point from the clean scratch
copy.  It does not reuse K equations.  It covers:

- both documented examples;
- empty input and exact true/false predicate boundaries;
- booleans and three user-defined `int` subclass values;
- zero, negative, and arbitrarily large Python integers;
- order and duplicates;
- strings, finite and non-finite floats, bytes, complex values, tuples, lists,
  list subclasses, dictionaries, sets, `None`, and a plain object;
- 200 deterministic generated lists, with seed `220022`, lengths 0 through 24,
  sampled from 33 typed atoms.

The script prints every typed input and both results.  Its exact invocation,
complete case record, exit 0, and summary
`total_cases=211, mismatches=0` are in
`evidence/05-python-differential.log`.

**Stage 2 result:** PASS for implementation fidelity.  Finite differential
testing supports, but does not prove, equivalence; here the stronger source
inspection also shows the two bodies are the same list-comprehension algorithm.

## 3. Clean proof reconstruction

K reports version `v7.1.293`.  All output directories named below were created
fresh under `/tmp/audit-work/22-filter-integers/src`; no candidate-compiled
definition or cache was used.

### Generated-semantics build and concrete execution

The LLVM definition was rebuilt with:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition fresh-semantic-kompiled
```

It exited 0 (`evidence/06-kompile-llvm.log`).  A direct first prompt execution
is preserved in `evidence/07a-krun-prompt1.log`.

The independent generated-semantics comparator then ran six cases: both prompt
examples, empty input, the bool/int boundary, every runtime constructor, and an
order/duplicate case.  It obtained trusted Python expectations from
`/reference/canonical.py`, ran fresh `krun` commands, and checked the exact
`<return>` cell.  All six corrected cases exited 0 and matched; see
`evidence/generated_semantics_differential.py` and
`evidence/07c-generated-semantics-differential-corrected.log`.

The retained `evidence/07b-generated-semantics-differential.log` is an initial
reviewer-harness failure: two configuration inputs used the internal printed
empty-list form `.PyVals`, which the concrete input scanner does not accept.
The errors were parser errors, not candidate execution divergences.  Replacing
those two input spellings with the concrete grammar's `VList()` made the same
cases run and match.  This initial nonzero is not used as candidate evidence.

### Proof build and aggregate reconstruction

The Haskell proof definition was rebuilt with:

```text
kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition fresh-verification-kompiled
```

It exited 0 (`evidence/08-kompile-haskell.log`).  The unchanged candidate spec
was then run with:

```text
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`
(`evidence/09-kprove-all-original.log`).  K emitted
`WarnTrivialClaim` for 15 claims, meaning they closed without operational
rewriting.  The two concrete whole-program entry claims did not receive that
warning.

### Every claim run independently

For independent selection, the audit added only labels to a scratch copy of
the 17 otherwise unchanged claims.  The exact artifact is
`evidence/spec-labeled.k`.  Each claim was run as:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.<audit-label>
```

Every run exited 0 and printed `#Top`.  The logs are
`evidence/10b-kprove-c01.log` and
`evidence/10-c02-int-head.log` through
`evidence/10-c17-filter-model-example.log`; the labeled aggregate rerun is
`evidence/10a-kprove-labeled-all.log`.

**Stage 3 result:** PASS.  Every submitted positive claim reconstructs.  This
establishes verification under the submitted theory, not adequacy of the
claims.

## 4. Adequacy and real-program pinning

### Complete claim-scope inventory

There are no `requires` or `ensures` clauses in `spec.k`; well-sortedness and
the explicit cells/terms are the only preconditions.

| Claims | Plain-language precondition and postcondition |
|---|---|
| C01 | An empty modeled list comprehension at the front of `<k>` becomes an empty modeled list. |
| C02-C03 | One `VInt` or `VBool` head is prepended, while the same comprehension remains on the arbitrary tail. |
| C04-C09 | One `VString`, `VFloat`, nested `VList`, `VDict`, `VNone`, or `VOpaque` head is skipped, while the same comprehension remains on the arbitrary tail. |
| C10 | Evaluating the filter expression on the fixed list `["a", 3.14, 5]` equals a separately defined filter model on that fixed list. |
| C11 | From empty function/environment/return cells, load hard-coded `solutionModule()`, invoke it on `["a", 3.14, 5]`, terminate, install the function/binding, and return `[5]`. |
| C12 | The same exact entry state for `[1,2,3,"abc",{},[]]` terminates and returns `[1,2,3]`. |
| C13 | Evaluator-only empty-list example returns empty. |
| C14 | Evaluator-only fixed bool/int boundary list returns `[True,False,0,-4]`. |
| C15 | Evaluator-only fixed length-nine list, with symbolic payloads for each constructor, equals the separately defined filter model on that same fixed-length list. |
| C16 | The separately defined filter model contains only integer-instance constructors on one fixed seven-element example. |
| C17 | The separately defined filter model has one expected concrete value on that same example. |

C02-C09 are sound one-head reductions, but their destinations still contain
`comprehend` on unconstrained `VS`.  They are not an induction/circularity
claim that the tail returns `onlyIntegerInstances(VS)`.  C15 has symbolic
payloads but fixed list length.  C16 is not connected to an actual entry
execution.  Consequently no claim says:

```text
for every VS:PyVals,
running filter_integers(VList(VS))
returns VList(onlyIntegerInstances(VS))
```

The audit preserved precisely that natural modeled-domain formulation in
`evidence/spec-universal-audit.k`.  Its dry run builds successfully
(`evidence/13a-universal-target-dry-run.log`), but proof exits 1 with
`WarnStuckClaimState`.  The residual is the unmet equality between
`comprehend(VList(VS), ...)` and
`VList(onlyIntegerInstances(VS))`
(`evidence/13b-universal-target-proof.log`).  Failure of this added claim is
not evidence that the true theorem is false; it demonstrates that the
candidate has not supplied the invariant/connection needed to prove it.

### Satisfying entry states and concrete substitution

C11's explicit initial configuration is a satisfying state: `<k>` contains
`bootstrap ~> invoke(...)`, `<program>` contains `solutionModule()`, and the
function, environment, and return cells are `.Functions`, `.Env`, and
`noResult`.  C12 has the same cells and its second concrete input.  Neither has
an additional logical guard.

For C11, trusted canonical Python and submitted Python both return `[5]`;
fresh K execution returns `result(VList(VInt(5), .PyVals))`.  For C12, both
Python implementations return `[1,2,3]`; fresh K returns the corresponding
modeled list.  The Python substitutions are in
`evidence/05-python-differential.log`, and the K substitutions are in
`evidence/07c-generated-semantics-differential-corrected.log`.

The two concrete entry postconditions therefore constrain the result correctly.
They simply do not quantify over the intended domain.

### Pinning to `solution.mpy`

The `<program>` cell in C11 and C12 is `solutionModule()`, a zero-argument
function declared in `verification.k`.  It rewrites to a hand-copied AST.  A
line-by-line audit shows that AST is the same term as the current submitted
`solution.mpy`, which also freshly regenerates from `solution.py`.

No K claim parses or names `solution.mpy`, however, and `prove.sh` regenerates
the file without comparing it to `solutionModule()`.  To test body sensitivity,
the audit replaced scratch `solution.mpy` with a valid term whose body is
`Return(ListExpr())`.  Fresh `krun` then returned an empty list on the first
prompt input (`evidence/12a-mutated-body-krun.log`), proving the mutation was
material and reachable.  Without changing `verification.k` or the claim, C11
still exited 0 with `#Top`
(`evidence/12b-mutated-body-kprove.log`).  The original and mutated terms are
preserved as `evidence/solution-original.mpy` and
`evidence/solution-body-mutated.mpy`.

Thus current-file identity is supported by external static inspection, but
the proof itself is not body-sensitive to the submitted artifact.

**Stage 4 result:** FAIL.  The target general entry theorem is absent, and the
K proof is not intrinsically pinned to the submitted MPY file.

## 5. Rule-by-rule static soundness review

The full numbered source is preserved in
`evidence/15-source-and-tool-inventory.log`.  There are no additional
candidate-authored K source helpers beyond `semantic.k`, `verification.k`, and
the claims in `spec.k`.

### Local syntax and configuration inventory

`semantic.k` declares all of the following local syntax:

- `Module`: `Module(Stmts)`.
- `Stmts`: an empty-separator list of `Stmt`.
- `Stmt`: `ImportFrom(String, Strings)`, `FuncDef(String, Params, Stmts)`,
  and `Return(Expr)`.
- `Params`: `Params(Strings)`.
- `Strings`: comma-separated `String`.
- `Expr`: `Name(String)`, `Int(Int)`, `Bool(Bool)`, `Str(String)`,
  `ListExpr(Exprs)`, `Call(Expr, Exprs)`, and
  `ListComp(Expr, CompFors)`.
- `Exprs`: comma-separated `Expr`.
- `CompFor`: `CompFor(Expr, Expr, Exprs)`.
- `CompFors`: an empty-separator list of `CompFor`.
- `PyVal`: `VInt(Int)`, `VBool(Bool)`, `VString(String)`,
  `VFloat(String)`, `VList(PyVals)`, `VDict`, `VNone`, and
  `VOpaque(String)`.
- `PyVals`: comma-separated `PyVal`.
- `RuntimeFunction`: `function(String, Stmts)`.
- `Functions`: `.Functions` or
  `bindFunction(String, RuntimeFunction, Functions)`.
- `Env`: `.Env` or `bind(String, PyVal, Env)`.
- `Result`: `noResult` or `result(PyVal)`.
- `KItem`: `bootstrap`, `load(Stmts)`, `invoke(String, PyVal)`,
  `exec(Stmts)`, and `finish(PyVal)`.

The configuration has exactly the state needed by this closed program:
`<k>`, `<program>`, `<functions>`, `<env>`, and `<return>`.  It has no heap,
allocation counter, I/O, exception, or call-stack cells.  Those omissions are
sound for this one pure function over already constructed modeled values.

`verification.k` adds:

- `solutionModule():Module [function]`;
- `filterExpression():Expr [function]`;
- `filterCondition():Expr [function]`;
- `onlyIntegerInstances(PyVals):PyVals [function,total]`;
- `containsOnlyIntegerInstances(PyVals):Bool [function,total]`.

There are no `[functional]`, `[simplification]`, `[concrete]`, `[opaque]`, or
explicit numeric-priority declarations in either file.  `VOpaque` is merely a
constructor name; it is not an unconstrained K opaque symbol.  The two
`[owise]` rules below are the only priority-like fallback rules.

### Mapping the actual submitted term

| Submitted construct | Declaration and execution rule |
|---|---|
| `Module` | `Module(Stmts)`; `bootstrap` reads its `Stmts`. |
| `ImportFrom("typing",...)` | `ImportFrom`; the load rule discards it.  This is sound here because the import affects annotations only. |
| `FuncDef("filter_integers", Params("values"), ...)` | `FuncDef`/`Params`; load installs the exact body and single parameter. |
| `Return` | `exec(Return(E))` evaluates the expression and proceeds to `finish`. |
| `ListComp` | The exact single-`CompFor` evaluator invokes `comprehend`. |
| target `Name("value")` | Bound in a fresh comprehension environment and looked up by the `Name` rules. |
| iterable `Name("values")` | Looked up in the invocation environment. |
| `Call(Name("isinstance"), Name("value"), Name("int"))` | The exact special call rule computes `pythonIsInteger` on the bound value. |
| statement/expression/list tails | Generated K list syntax supplies the `.Stmts`, `.Exprs`, `.CompFors`, `.Strings`, and `.PyVals` units visible after parsing. |

Every construct used by the submitted MPY term has a declaration and a
reachable rule.  Extra syntax for literals and empty list expressions is
sound but mostly unused by this program.

### `semantic.k` rule inventory and decisions

| ID | Rule | Static decision |
|---|---|---|
| S01 | `bootstrap => load(SS)` from `Module(SS)` | Sound: exposes the exact stored module statements while preserving the continuation. |
| S02 | `load(.Stmts) => .K` | Sound finite-list base case. |
| S03 | `load(ImportFrom(_,_) SS) => load(SS)` | Sound for this import, whose names are used only in erased annotations.  It is intentionally not a general Python import model. |
| S04 | Loading `FuncDef` installs `bindFunction` then loads the tail | Sound for the closed one-function module; it preserves the active continuation and functions cell. |
| S05 | `invoke(F,V) => exec(BODY)` when the top binding is `F`; environment becomes the single parameter binding | Sound for the actual single-parameter top-level call.  It would be incomplete for closures, recursion, or nested calls, none of which occurs. |
| S06 | `exec(Return(E)) => finish(eval(E,ENV))` | Sound for the actual one-statement body.  The modeled expression is pure, so absence of an explicit Python evaluation stack has no observable effect here. |
| S07 | `finish(V) => .K` and return cell becomes `result(V)` | Sound normal return for this top-level call; no continuation/control frame is discarded. |
| S08 | `eval(Int(I),_) => VInt(I)` | Sound literal encoding. |
| S09 | `eval(Bool(B),_) => VBool(B)` | Sound literal encoding. |
| S10 | `eval(Str(S),_) => VString(S)` | Sound literal encoding. |
| S11 | Lookup from matching top `bind(X,V,_)` returns `V` | Sound lexical lookup for this linked environment. |
| S12 | Lookup skips a nonmatching binding when `X =/=String Y` | Sound, disjoint from S11, and descending on the finite environment. |
| S13 | Empty `ListExpr` evaluates to empty `VList` | Sound; nonempty list-expression semantics is absent but unused. |
| S14 | Exact `isinstance(E,int)` call returns `VBool(pythonIsInteger(eval(E,ENV)))` | Sound for the actual unshadowed builtins and pure argument.  It is deliberately not general call semantics. |
| S15 | Exact one-generator/name-target `ListComp` becomes `comprehend` | Sound for the submitted expression. |
| S16 | `pythonIsInteger(VInt(_)) => true` | Sound for the modeled integer constructor. |
| S17 | `pythonIsInteger(VBool(_)) => true` | Sound and correctly captures Python's `bool`-is-an-`int` behavior. |
| S18 | `pythonIsInteger(_) => false [owise]` | Disjoint fallback and total over the eight declared `PyVal` constructors.  Sound only under the intended reading that all other constructors are non-integer instances; see the representation limitation below. |
| S19 | `comprehend` on empty modeled list returns empty | Sound recursion base. |
| S20 | Nonempty `comprehend` evaluates condition and element under `bind(X,V,ENV)`, then recurses on `VS` | Sound for the submitted pure `Name("value")` element and pure `isinstance` condition; recursion strictly decreases the finite list. |
| S21 | `keepIf(VBool(true),V,TAIL) => prepend(V,TAIL)` | Sound true branch. |
| S22 | `keepIf(VBool(false),_,TAIL) => TAIL` | Sound false branch for this pure element expression. |
| S23 | `prepend(V,VList(VS)) => VList(V,VS)` | Sound list construction preserving order and duplicates. |

The partial `eval`, `comprehend`, `keepIf`, and `prepend` functions cover every
form in the actual reachable program.  Partiality on unused forms is permitted
in generated-semantics mode.  S11/S12, S19/S20, and S21/S22 have disjoint
patterns/guards.  S16-S18 are disjoint because `[owise]` applies only when the
specific rules do not.  No local rule has an overlapping contradictory
right-hand side.

The semantics has no state-changing expression, allocation, exceptional, or
output behavior.  Python condition-before-element order is not represented by
an explicit evaluation stack, but both reachable subexpressions are pure name
lookup/type testing, so this does not change any result or modeled state.

### `verification.k` rule inventory and decisions

| ID | Rule | Class and static decision |
|---|---|---|
| V01 | `solutionModule()` expands to the copied submitted module term | Definitional closed term; truthful for the current candidate, but not file-linked or body-sensitive.  It does not itself replace execution after expansion. |
| V02 | `filterExpression()` expands to the exact submitted list comprehension | Truthful closed definitional abbreviation. |
| V03 | `filterCondition()` expands to the exact submitted `isinstance` call | Truthful closed definitional abbreviation. |
| V04 | `onlyIntegerInstances(.PyVals) => .PyVals` | Sound stable-filter base. |
| V05 | `VInt` head is retained | Sound. |
| V06 | `VBool` head is retained | Sound in Python. |
| V07 | `VString` head is skipped | Sound. |
| V08 | `VFloat` head is skipped | Sound. |
| V09 | nested `VList` head is skipped | Sound. |
| V10 | `VDict` head is skipped | Sound. |
| V11 | `VNone` head is skipped | Sound. |
| V12 | `VOpaque` head is skipped | Sound only if `VOpaque` is restricted to non-`int` instances; this encoding contract is informal. |
| V13 | `containsOnlyIntegerInstances(.PyVals) => true` | Sound base. |
| V14 | `VInt` head recurses | Sound. |
| V15 | `VBool` head recurses | Sound. |
| V16 | Every other nonempty head returns false `[owise]` | Sound and disjoint over the declared constructors under the same `VOpaque` interpretation. |

`onlyIntegerInstances` is total on `PyVals`: the base and all eight possible
head constructors are covered, guards do not overlap, and recursion descends
on the tail.  `containsOnlyIntegerInstances` is likewise total: base,
`VInt`, `VBool`, and the `[owise]` noninteger heads cover the domain.

`onlyIntegerInstances` encodes the task's mathematical answer, but it does not
replace program execution in S01-S23.  It appears in evaluator-only
postconditions and examples.  Its equations are not an unconstrained oracle.
The defect is the absence of the universal connection theorem relating actual
`comprehend` execution to this truthful summary.

### Intended-domain representation gap

K integers are arbitrary precision, so `VInt` is a good model of ordinary
Python integer payloads.  The model has no constructor or explicit encoding
rule for a user-defined subclass of `int`.  A concrete intended-domain witness
is:

```python
class MyInt(int):
    pass

filter_integers([MyInt(7)]) == [MyInt(7)]
```

The Python differential includes this boundary and both Python
implementations retain it.  If such a value were placed in the generic
`VOpaque` constructor, S18/V12 would instead skip it.  Because the candidate
never defines `VOpaque` as the encoding of every otherwise unmodeled Python
object, this audit records the narrower defect: the Python-to-`PyVal` bridge is
incomplete for the full `List[Any]` domain.  It does **not** label S18 or V12
globally unsound over their declared K domain, and therefore does not invent an
unsound-rule conclusion beyond the evidence.

No other materially unsound semantic or proof-local rule was found.  In
particular, there are no arbitrary rewrites, fresh result-bearing symbols,
control-discarding bridges, false arithmetic lemmas, or task-answer rules that
preempt actual `comprehend` execution.

**Stage 5 result:** The inventoried rules are sound for the bounded modeled
program, subject to the explicit value-encoding limitation.  This does not
repair the missing target claim or file pin.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact.  The audit created
`evidence/spec-vacuity.k`, changing C11's exact result from the true `[5]` to
the false `[6]` while retaining its satisfiable initial state.

The mutation was first checked with:

```text
kprove spec-vacuity.k --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

It built successfully and exited 0
(`evidence/11a-vacuity-dry-run.log`).  The real proof command without
`--dry-run` exited 1, emitted `WarnStuckClaimState`, and displayed the terminal
return cell `result(VList(VInt(5), .PyVals))`, which cannot unify with the
mutated destination `[6]` (`evidence/11b-vacuity-proof.log`).

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unreachable mutation.

**Stage 6 result:** PASS for non-vacuity of the concrete C11 result constraint.
It does not show discrimination of a universal theorem, because no universal
entry theorem exists.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the candidate's generated semantics and proof-local function equations,
the successful runs establish:

1. the nine base/one-head comprehension reductions C01-C09;
2. evaluator results for several empty or fixed-length lists;
3. two concrete full-configuration executions corresponding to the prompt
   examples;
4. two fixed examples about the separately defined stable-filter model.

They do not establish the output for arbitrary list length, do not universally
connect actual execution to `onlyIntegerInstances`, do not universally connect
actual output to `containsOnlyIntegerInstances`, and do not quantify over the
natural `List[Any]` domain.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and `kprove` reachability implementation | All dynamic results | Necessary foundational trust; rebuilt from source-facing K files. |
| Imported K `BOOL`, `INT`, `STRING`, and generated list machinery | All parsing/evaluation and helper equations | Ordinary low-level semantics trust; no candidate modification. |
| Trusted `/reference/prompt.py` and `/reference/canonical.py` | Natural-language intent and differential oracle | Authoritative task inputs. |
| Trusted `/reference/py2mpy.py` | Python-to-MPY syntax bridge | Acceptable external translator boundary; submitted term is byte-identical to fresh output. |
| Equality of current `solution.mpy` and hand-copied `solutionModule()` | C11/C12 as statements about the submitted program | Independently inspected and true for this candidate, but not machine-linked; body-sensitivity test shows the proof ignores later file changes. |
| `PyVal` as a model of Python values | All K-to-Python intent conclusions | Informal and finite-tested.  Adequate for declared ordinary constructors, incomplete for user-defined `int` subclasses and the full `Any` universe. |
| Python fact that `bool` is an `int` instance | S17, V06, V15 and related results | Correct and independently exercised. |
| `VOpaque(String)` means a non-integer opaque value | S18, V12, V16 and C09/C15 | Informal encoding contract.  It is not a K opaque oracle, but its Python correspondence is not universal. |
| Equations for `onlyIntegerInstances` | C10, C15-C17 and the missing desired target | Exhaustive, disjoint, descending, and mathematically truthful over `PyVals`.  No universal execution connection was proved. |
| Python differential over 211 cases | Source implementation/canonical bridge | Strong finite evidence only; zero mismatches. |
| K/Python comparison over six modeled cases | Generated-semantics adequacy bridge | Finite evidence only; zero corrected mismatches. |
| Partial correctness/termination scope | Reachability claims | Concrete claims terminate.  No arbitrary-input reachability claim exists, so there is no universal partial-correctness result to qualify. |

No candidate compiled definition, `#Top` transcript, prose report, or
generation trace is included in the trust base.

### Gate summary and verdict rationale

- Fresh reconstruction: PASS for all submitted claims.
- Concrete result constraint/non-vacuity: PASS for C11.
- Static rule soundness: PASS on the declared bounded `PyVal` model, with the
  documented representation limitation.
- Real-program body sensitivity: FAIL; claims use a hard-coded duplicate and
  ignore `solution.mpy`.
- Target theorem adequacy: FAIL; there is no arbitrary-list whole-program
  claim or universal execution-to-filter connection.
- Reproducibility: PASS; exact commands, statuses, bounded outputs, scripts,
  mutations, and source listings are preserved under `evidence/`.

The candidate's successful claims are honest but materially weaker than the
requested proof.  Correct implementation and finite execution agreement cannot
substitute for the missing K theorem.  Therefore the candidate does not contain
a legitimate partial-correctness proof of the real generated program over the
intended domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
