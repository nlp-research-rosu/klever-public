# Independent adversarial audit: 126-is-sorted

The submitted implementation agrees with the trusted canonical implementation on
the tested intended domain, the submitted MPY is the exact trusted translation,
the clean target proof closes with `#Top`, and a fresh false postcondition is
rejected.  Nevertheless, the generated semantics contains a result-bearing
fused generator rule that is false over its declared match domain.  A witness
produced by the trusted translator raises `AttributeError` in CPython but
terminates with `BoolVal(true)` in the candidate semantics; a reachability claim
for that false Boolean conclusion closes with `#Top`.  This is a Gate A
semantics-soundness failure, so the successful target `#Top` is not accepted as
a legitimate proof.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.  `/reference` contains exactly the
three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent and is not a symlink.  There is no
mode/mount contradiction, so this is a candidate audit rather than
`AUDIT_ERROR`.  The exact inventory and boundary test are in
[`evidence/stage1-mount-inventory.log`](evidence/stage1-mount-inventory.log).
No hidden or inferred reference semantics was sought or used.

### Required artifacts and comparisons

All artifacts needed for this candidate's source reconstruction are present as
regular, non-symlink files:

- `solution.py`, `solution.mpy`;
- `semantic.k`, `list-domain.k`, `verification.k`, `spec.k`;
- `prompt.py`, `py2mpy.py`, and `prove.sh`; and
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL generation trace.

There are no missing, changed, mistyped, or symlinked required source
artifacts.  Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`050a2b9defc209aa64d0777939ff3387ee7db918434d818789eab7b36578b7ca`),
and candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
See [`evidence/stage1-provenance.log`](evidence/stage1-provenance.log).

The candidate also contains extra generated `semantic-kompiled/` and
`__pycache__/` trees.  These are not provenance failures in generated-semantics
mode, but they were treated as untrusted build products, were not copied, and
were never used.  No candidate `PROOF.md` or `spec-vacuity.k` was supplied;
neither is a required source input to this reconstruction.

The first provenance wrapper records that the optional host utility `file(1)`
was unavailable after the hash and `cmp` checks had already completed.  Regular
file types and symlink status were independently established by `find
-printf`; this reviewer-wrapper issue is unrelated to the candidate and does
not affect the verdict.

### Untrusted generation claims

`run-input.json` identifies problem `126-is-sorted`, condition `bare`, and no
supplied semantics.  `metrics.json` claims a successful, non-timeout generation
run.  `codex-last.txt`, `codex-output.log`, and the trace claim that concrete
examples passed, the target printed `#Top`, and the candidate mutation failed.
Those statements were used only to identify claimed targets.  The complete
claim-bearing trace records were independently parsed in
[`evidence/stage1-structured-trace.log`](evidence/stage1-structured-trace.log);
the relevant log claims are bounded in
[`evidence/stage1-untrusted-generation-claims.log`](evidence/stage1-untrusted-generation-claims.log).

Every source used for execution was copied to
`/tmp/audit-work/126-is-sorted`, with hashes recorded in
[`evidence/stage1-scratch-copy.log`](evidence/stage1-scratch-copy.log).

**Stage 1 result:** PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite list of non-negative Python integers, return `True` exactly when:

1. the list is in nondecreasing (ascending, with equality allowed) order; and
2. no value occurs more than twice.

The examples establish that two occurrences are allowed and three are not.
The trusted canonical implementation first rejects multiplicity greater than
two and then checks each adjacent pair with `<=`.  The trusted sources are
quoted with line numbers in
[`evidence/stage2-trusted-inputs.log`](evidence/stage2-trusted-inputs.log).

Candidate `solution.py` returns:

```python
lst == sorted(lst) and all(lst.count(x) <= 2 for x in lst)
```

For finite integer lists, equality with the ascending sorted copy is equivalent
to nondecreasing order, and the generator is equivalent to the canonical
multiplicity test.  It also returns `True` on the empty list, as does the
canonical implementation.

### Trusted translation identity

The trusted translator was run on the scratch copy of `solution.py`.  Its
output has SHA-256
`e1fb2ad3b994d9f517e5d395c016188311410e12c5bac7168fd689623f4cbe4d`,
the submitted `solution.mpy` hash.  `cmp -l` produced no differences and exited
0.  Exact commands and statuses are in
[`evidence/stage2-translation-identity-rerun.log`](evidence/stage2-translation-identity-rerun.log);
the preserved wrapper is
[`evidence/check_translation.sh`](evidence/check_translation.sh).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point and the scratch candidate entry point through
separate module loaders.  It checks return types, results, and input
non-mutation.  Its deterministic corpus contains:

- all eight documented examples;
- empty, zero, one/two/three-duplicate, sorted/unsorted, first/middle/last-order,
  and large-integer boundary cases;
- every list of length 0 through 6 over values 0 through 4; and
- 5,000 seed-126 generated lists of length 0 through 24 over values 0 through
  10,000.

After deduplication it exercised 24,326 exact inputs, with 554 `True` and
23,772 `False` canonical results.  It found zero mismatches and exited 0.  The
input generators, explicit inputs, corpus hash, command, and results are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).
This is finite evidence, not a universal proof.

**Stage 2 result:** PASS; no implementation/canonical divergence was found on
the intended domain.

## 3. Clean proof reconstruction

No candidate definition or cache was reused.  From the scratch source copy I
built:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0.  Logs are
[`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) and
[`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log).
The independently installed `kompile`, `krun`, and `kprove` are K
v7.1.293; tool versions and fresh definition contents are recorded in
[`evidence/stage3-toolchain-and-definitions.log`](evidence/stage3-toolchain-and-definitions.log).

There is one positive target claim, in `spec.k`.  The only other
candidate-supplied claim is the candidate's expected-failure mutation.  The
independent positive run was:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It exited 0 and printed exactly `#Top`; see
[`evidence/stage3-positive-kprove.log`](evidence/stage3-positive-kprove.log).

Because this is generated-semantics mode, concrete execution was separately
tested from the LLVM build.  The independent harness
[`evidence/concrete_semantics_test.py`](evidence/concrete_semantics_test.py)
ran 15 normal and boundary lists through the freshly built K definition and
compared each result with both Python implementations.  These include empty,
singleton, one/two/three equal elements, increasing/decreasing, an interior
order break, both duplicate-bound outcomes, and large integers.  All `krun`
processes exited 0, all results matched, and the harness reported zero
mismatches; see
[`evidence/stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).

**Stage 3 result:** PASS.  This establishes fresh verification under the
candidate theory; it does not establish that every rule in that theory is
sound.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole entry claim has no `requires` clause, so its precondition is `true`
for every constructor `IS:IntList`, including lists containing negative K
integers (a formal domain broader than the prompt's non-negative domain).
Starting with the exact submitted function AST and argument `PyList(IS)`, it
requires termination at:

```text
BoolVal(isSortedContract(IS))
```

`IS` occurs on both sides; the returned value is not a fresh or unconstrained
right-hand-side variable.  `isSortedContract` reduces to
`eqIntLists(IS, sortInts(IS)) andBool countsAtMost(IS, IS, 2)`.  Thus the
destination is result-constraining, not a tautological wildcard or a one-way
implication.

### Program identity and control path

The exact `Module(...)` constructor embedded in `spec.k` was compared with the
entire submitted `solution.mpy` after removing only unquoted whitespace.  Both
normalized terms contain 300 characters and have SHA-256
`a16dba0bacf2edcdc318f32ddba854c2ff3b3842dbcdcd41eca8c045c8528b32`;
the check exited 0.  See
[`evidence/check_program_pinning.py`](evidence/check_program_pinning.py) and
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).
Together with the trusted byte-identical regeneration in Stage 2, the claim
pins the current submitted generated program.

A depth-1 diagnostic proof reaches:

```text
EvalStmt(Return(the submitted expression), "lst" |-> PyList(IS))
```

and exits nonzero only because of the deliberate depth bound.  At depth 2 the
same claim closes with `#Top`.  These traces show that the ordinary `Run` and
`EvalStmt(Return(...))` transitions are exercised rather than the initial
configuration being accepted without executing the entry rules.  See
[`evidence/stage4-depth1-trace.log`](evidence/stage4-depth1-trace.log) and
[`evidence/stage4-depth2-trace.log`](evidence/stage4-depth2-trace.log).

There are no helper or loop reachability claims to align with control flow.
Recursion for insertion sort, equality, and counting is encoded as K
functions.

### Satisfying states and ground substitutions

Because the precondition is `true`, for example:

- `IS = Nil` is satisfiable and the claimed result is `BoolVal(true)`;
- `IS = Cons(0, Cons(0, Cons(0, Nil)))` is satisfiable and the result is
  `BoolVal(false)`; and
- `IS = Cons(1, Cons(0, Nil))` is satisfiable and the result is
  `BoolVal(false)`.

The corresponding inputs `[]`, `[0,0,0]`, and `[1,0]` agree in the fresh K run,
candidate Python, and trusted canonical Python; the exact substitutions and
outputs are in
[`evidence/stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).

**Stage 4 result:** PASS for pinning, result constraint, realizability, and
actual submitted control flow.

## 5. Rule-by-rule static soundness review

### Complete local inventory

The declaration/rule search and counts are preserved in
[`evidence/stage5-rule-inventory.log`](evidence/stage5-rule-inventory.log).

Local syntax consists of:

- `IntList`: `Nil`, `Cons(Int, IntList)`;
- AST constructors: `Module`; `Params`; `CellVars`; `FreeVars`; `FuncDef`;
  `Return`; `Name`; `Int`; `Bool`; `Attribute`; `Call`; `BoolOp`; `Compare`;
  `GenExp`; `CmpOp`; and `CompFor`;
- runtime values: `IntVal`, `BoolVal`, and `PyList`;
- runtime computations: `Run` and `EvalStmt`; and
- function symbols: `eval`, `asList`, `asBool`, `eqValue`, `insertInt`,
  `sortInts`, `eqIntLists`, `countInt`, `countsAtMost`, `countsAtMostTwo`,
  `ascending`, `duplicateBound`, and `isSortedContract`.

All 13 helper symbols are declared `[function]`.  There are no local
`[total]`, explicit `[functional]`, `[simplification]`, `[concrete]`, `[owise]`,
priority, anywhere, macro, fresh, or opaque declarations or rules.  Constructor
productions have `[symbol(...)]` labels; these are parser/K labels, not opaque
result oracles.  The configuration contains only:

```text
<k> Run($PGM:Pgm, $ARGS:Value) </k>
```

There are 14 rules in `semantic.k`, 15 in `list-domain.k`, 3 in
`verification.k`, and 1 entry claim.

### Mapping of every submitted construct

`Module`, `FuncDef`, `Params`, `CellVars`, and `FreeVars` are parsed by the AST
syntax and consumed by `Run`; the actual parameter `"lst"` is bound to the
argument.  `Return` is consumed by `EvalStmt`.  `BoolOp("and",...)` is consumed
by the Boolean rule.  The list-equality branch uses `Compare`, `CmpOp("==")`,
`Call(Name("sorted"),...)`, and `Name`, then `asList`, `sortInts`,
`eqIntLists`, and `eqValue`.

The submitted `Call(Name("all"), GenExp(...))`, inner `Attribute`, `Call`,
`Compare`, `CmpOp("<=")`, `Int(2)`, `CompFor`, target `Name("x")`, source
`Name("lst")`, and `Bool(true)` are consumed together by the fused generator
rule at `semantic.k:83-91`; they are not evaluated component-by-component.
`PyList`, `Cons`/`Nil`, and K `Int` carry the input.  Thus every construct in
the submitted MPY has a declaration and an applicable rule path.

### `semantic.k`: all 14 rules

| ID | Rule | Static finding |
|---|---|---|
| S1 | `Run(Module(FuncDef("is_sorted", Params(X), _CV, _FV, BODY)), V)` → `EvalStmt(BODY, X |-> V)` | Correct for the exact top-level submitted function. It intentionally ignores closure metadata and is broader than the one supported body; unsupported closure behavior is outside the submitted path. |
| S2 | `EvalStmt(Return(E), RHO)` → `eval(E,RHO)` | Correct for the only statement and top-level return path. The continuation is framed and preserved. |
| S3 | `eval(Int(I),_)` → `IntVal(I)` | Correct. |
| S4 | `eval(Bool(B),_)` → `BoolVal(B)` | Correct. |
| S5 | `eval(Name(X),(X |-> V) _RHO)` → `V` | Correct map lookup for a bound name; unbound-name exceptions are unmodeled but unused. |
| S6 | `asList(PyList(IS))` → `IS` | Correct representation projection on its only used case. |
| S7 | `asBool(BoolVal(B))` → `B` | Correct representation projection on its only used case. |
| S8 | `eqValue(PyList(IS),PyList(JS))` → `eqIntLists(IS,JS)` | Correct list-value equality for explicit integer lists. |
| S9 | `eqValue(IntVal(I),IntVal(J))` → `I ==Int J` | Correct integer equality. |
| S10 | `eqValue(BoolVal(B),BoolVal(C))` → `B ==Bool C` | Correct Boolean equality. |
| S11 | `eval(BoolOp("and",E1,E2),RHO)` → eager `andBool` of both evaluations | Python short-circuits, while this rule evaluates both denotations. For the submitted expression both operands are pure, Boolean, total on finite `IntList`, and have no state or exception, so value/control behavior agrees. The broader syntax does not model every short-circuit program; that is an off-path coverage limitation, not a witnessed false result for this submitted term. |
| S12 | equality `Compare` → `eqValue` | Correct for the submitted equality and represented values. |
| S13 | `sorted` call → `PyList(sortInts(...))` | Correct provided the explicit insertion-sort equations below; Python allocation identity is unobservable in this program. |
| S14 | fused `all(source.count(x) <= LIMIT for x in source if true)` → `countsAtMost(IS,IS,LIMIT)` | **Unsound over its declared match domain.** It does not model generator-target binding and has no guard requiring `X =/=String SOURCE`. A concrete false-conclusion witness is given below. This rule is result-bearing and directly contributes to the positive target. |

The one-cell model omits heap allocation, iterator objects, and exceptions.
For the exact submitted expression over finite integer lists, `sorted` does not
mutate `lst`, the generated values are only observed by equality/Boolean
operations, and all helpers terminate.  Those omissions do not change the
submitted path.  They do matter for the broader S14 match domain.

### `list-domain.k`: all 15 rules

| ID | Rule | Static finding |
|---|---|---|
| L1 | `insertInt(I,Nil)` | Correct singleton insertion. |
| L2 | insert before head when `I <=Int J` | Correct. |
| L3 | retain head and recurse when `I >Int J` | Correct; guard is disjoint from and exhaustive with L2 over K integers, and recursion descends on the tail. |
| L4 | `sortInts(Nil)` | Correct empty sort. |
| L5 | sort tail then insert head | Standard terminating insertion sort on finite constructor lists. |
| L6 | `eqIntLists(Nil,Nil)` | Correct. |
| L7 | `Nil` versus `Cons` | Correct false case. |
| L8 | `Cons` versus `Nil` | Correct false case. |
| L9 | `Cons` versus `Cons` | Correct head equality conjoined with recursive tail equality; constructor cases are disjoint/exhaustive. |
| L10 | `countInt(_,Nil)` | Correct zero count. |
| L11 | equal head: one plus tail count | Correct. |
| L12 | unequal head: tail count | Correct; equality/inequality guards are disjoint/exhaustive and recursion descends. |
| L13 | `countsAtMost(_,Nil,_)` | Correct empty `all` result `true`. |
| L14 | check head count against limit and recurse over items | Correct for mathematical integer-list multiplicity; recursion descends on `ITEMS`. Rechecking duplicate items is redundant but value-preserving. |
| L15 | `countsAtMostTwo` → limit 2 | Correct definitional wrapper. |

No guards overlap with disagreeing right-hand sides.  All recursive equations
decrease a finite `IntList` argument, and the apparent functions are covered on
every value reached by the submitted program.

### `verification.k`: all 3 rules

| ID | Rule | Static finding |
|---|---|---|
| V1 | `ascending(IS)` → `eqIntLists(IS,sortInts(IS))` | A definition, not a machine-checked theorem that insertion sort characterizes nondecreasing order. The equivalence is valid for finite integer lists by the insertion-sort equations. |
| V2 | `duplicateBound(IS)` → `countsAtMostTwo(IS,IS)` | Correct definition of maximum multiplicity two. |
| V3 | `isSortedContract(IS)` → `ascending(IS) andBool duplicateBound(IS)` | Correct conjunction of the two predicates. |

These proof-side functions are imported into `semantic.k`, but no execution
rule rewrites directly to `isSortedContract`.  The target proof nevertheless
normalizes both the execution result and postcondition to the same list helper
terms, so the natural-language meaning of those helpers remains an informal
mathematical bridge rather than a separate K theorem.

### Concrete false-conclusion witness for S14

The S14 variables allow `X` and `SOURCE` to be the same string.  In Python,
generator-target binding then changes the meaning of `Name(SOURCE)` in the
element expression.  The preserved witness is:

```python
def is_sorted(lst):
    return all(lst.count(lst) <= 2 for lst in lst) and all(
        lst.count(x) <= 2 for x in lst
    )
```

The second generator causes the trusted translator to emit the same
`CellVars("lst"), FreeVars()` function shape accepted by this generated
grammar.  The submitted fused rule matches the first generator with
`X = SOURCE = "lst"`.  On input `[1]`, CPython binds the target `lst` to integer
`1`, then raises `AttributeError` when evaluating `lst.count`.  S14 instead
ignores that binding and counts in the outer list, so the fresh K semantics
returns `BoolVal(true)`.

The witness source, trusted-translator-identical MPY, and harness are
[`evidence/shadowing_witness.py`](evidence/shadowing_witness.py),
[`evidence/shadowing_witness.mpy`](evidence/shadowing_witness.mpy), and
[`evidence/run_shadowing_witness.py`](evidence/run_shadowing_witness.py).
The translator comparison exits 0, CPython exception, K exit 0/result true, and
discrepancy are recorded in
[`evidence/stage5-overbroad-rule-witness-rerun.log`](evidence/stage5-overbroad-rule-witness-rerun.log).

This is not merely a missing-semantics or timeout example.  The preserved
reachability claim
[`evidence/shadowing-false-claim.k`](evidence/shadowing-false-claim.k) builds
successfully and closes with `#Top` for `BoolVal(true)`, while CPython raises on
the same trusted-translated program and intended-domain input.  See
[`evidence/stage5-false-conclusion-kprove.log`](evidence/stage5-false-conclusion-kprove.log).

The exact submitted program uses `X = "x"` and `SOURCE = "lst"`, so this witness
does not show that the submitted Python function is incorrect.  It shows that
the result-bearing rule used by the target proof is false over its complete
declared match domain.  There is no guard narrowing the domain and no
independent full-domain binding/exception connection theorem.  Under the
required rule-by-rule and Kit Gate A audit, an off-path false rule cannot be
treated as a sound semantics merely because the target happens to use one
truthful instance.

### Operational body sensitivity

As a separate test, I changed the program's first comparison from
`lst == sorted(lst)` to `lst == lst` while retaining the original result
contract on input `[1,0]`.  The independent mutation
[`evidence/body-sensitivity-spec.k`](evidence/body-sensitivity-spec.k) parses
and builds (`--dry-run` exit 0), then the proof exits 1 with a stuck
`BoolVal(true)` state against the original false contract.  See
[`evidence/stage5-body-mutation-dry-run.log`](evidence/stage5-body-mutation-dry-run.log)
and
[`evidence/stage5-body-mutation-proof.log`](evidence/stage5-body-mutation-proof.log).
Thus the target is sensitive to the actual submitted body; this positive fact
does not cure S14's false full-domain equation.

**Stage 5 result:** FAIL.  S14 is a witnessed, result-bearing unsound semantics
rule that can prove a false conclusion on a non-negative integer-list input.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was not reused.  The fresh mutation
[`evidence/fresh-vacuity-spec.k`](evidence/fresh-vacuity-spec.k) executes the
unchanged exact submitted program on the satisfiable input `IS = Nil` but
changes the destination from the true contract result to `BoolVal(false)`.

First:

```text
kprove fresh-vacuity-spec.k --definition proof-kompiled \
  --spec-module FRESH-VACUITY-SPEC --dry-run
```

exited 0, demonstrating successful parsing/building
([`evidence/stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)).
The actual proof run exited 1 with `WarnStuckClaimState` after reaching
`BoolVal(true)`, the expected unmet result obligation
([`evidence/stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log)).
The failure was not a parser error, import error, timeout, crash, or unreachable
mutation.

**Stage 6 result:** PASS.  The target claim is result-constraining and
non-vacuous under the candidate theory.

## 7. Proven versus assumed accounting

### What the successful target reachability proof establishes

Conditional on all rules in the freshly compiled candidate definition, the
successful claim establishes this partial-correctness statement:

> For every finite constructor `IS:IntList`, executing the exact submitted MPY
> entry term `Run(Module(FuncDef(...submitted body...)), PyList(IS))` reaches
> `BoolVal(isSortedContract(IS))`.

After function normalization, that returned Boolean is:

```text
eqIntLists(IS, sortInts(IS))
andBool
countsAtMost(IS, IS, 2)
```

The proof is universal over K integer lists and therefore formally includes
negative integers, although the natural-language task only assumes
non-negative integers.  It is a statement about the exact current MPY term,
not a claim that an arbitrary future `solution.mpy` file will remain pinned.

The proof does not, by itself, establish that the candidate rules are CPython
semantics, that insertion-sort equality is the English notion of ascending
order, or that the generated semantics handles other translated programs.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser, LLVM/Haskell backends, reachability engine, and imported `INT`, `BOOL`, `STRING`, `MAP` hooks | Parsing, built-in arithmetic/equality/maps, execution, and proof closure | Ordinary unavoidable tool/primitive trust boundary; versions and fresh builds are recorded. |
| Trusted `/reference/py2mpy.py` | Links `solution.py` to the submitted constructor program | Exact output identity is machine-checked. Correctness of the trusted translator itself is an authorized trusted input, not proved by the candidate. |
| CPython behavior and `/reference/canonical.py` | Natural-language implementation oracle | Independently tested on 24,326 inputs; finite evidence only. |
| `insertInt`/`sortInts` mathematics | Meaning of `sorted` and `ascending` | Equations are exhaustive, non-overlapping, descending, and match ordinary insertion sort. The ascending-equivalence argument is informal mathematics, not a separate K lemma. |
| `eqIntLists`, `countInt`, and `countsAtMost` mathematics | Equality and duplicate-bound meaning | Exhaustive, non-overlapping recursive equations; ordinary mathematical justification plus concrete evidence. |
| Eager `andBool` for Python `and` | Evaluation order/control | Acceptable only for the exact submitted pure, total Boolean operands; broader short-circuit behavior is excluded. |
| Omitted heap/allocation/iterator cells | State, identity, mutation, exceptions | Acceptable for the exact typed, pure submitted path because no such observation is exposed; not a general Python semantics. |
| S14 fused generator rule | Directly determines the duplicate-bound branch and final target result | **Illegitimate as declared.** It is a program-derived, result-bearing operational summary with a witnessed false binding/exception conclusion and no full-domain connection theorem or narrowing guard. |

There are no candidate-local opaque symbols, fresh result symbols, declared
totality axioms, simplification lemmas, priorities, or auxiliary claims.
Differential and concrete tests support only their enumerated inputs; neither
substitutes for the K proof or repairs S14.

### Decision

Stages 1–4 and 6 show that this is not a provenance substitution, failed clean
build, unpinned program, free-result claim, or vacuous `#Top`.  The submitted
Python implementation itself appears correct.  The failure is instead the
mandatory static soundness gate: the proof definition contains and uses a
result-bearing semantic rule whose full match domain admits a trusted-
translator program and intended-domain input for which K proves a Boolean
return that real execution does not have.

Narrowing S14 to the exact non-shadowing binding shape, or modeling generator
binding and exceptions correctly and then rebuilding, could remove this
specific defect.  The read-only candidate does not contain that repair.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
