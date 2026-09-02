# Independent adversarial audit: 116-sort-array

## Audit result

The submitted K claims are reproducible, result-constraining proofs about the
actual submitted `solution.mpy`. The generated semantics executes the submitted
program rather than replacing it with an oracle, and the fresh non-vacuity
mutation is rejected for the expected result mismatch.

The proof is nevertheless materially limited as a proof of the HumanEval
contract. It proves symbolic entry-point behavior only for lists of lengths
zero through three. Lists of lengths five and six occur only as fixed ground
examples. There is no entry claim quantified over an arbitrary `Ints` list and
no inductive/circular claim that establishes correctness for every finite
non-negative input array. The two property-named claims additionally check
ordering and multiplicities for only one fixed example. This is a Gate B
intent-adequacy limitation, not a soundness failure in the claims that were
actually submitted.

The trusted prompt is internally inconsistent. Its prose says to order
non-negative integers lexicographically by `(number of one bits, integer
value)`, while all displayed results use ordinary numeric order. Both the
trusted canonical implementation and the candidate follow the prose ordering,
not the displayed results.

All commands below were run against reviewer-created scratch copies under
`/tmp/audit-work/116-sort-array`. Candidate-provided compiled definitions were
not used.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted
`/reference/reference-semantics` path does not exist, while
`/candidate/semantic.k` is present as a regular file. The trusted mounts
therefore do not contradict the rendered mode. No hidden or inferred reference
semantics was used.

The complete type-aware candidate/reference manifest, hashes, regular-file
checks, and mode check are in
[`evidence/stage1-integrity.log`](evidence/stage1-integrity.log). There were no
missing, changed, mistyped, or symlinked required source artifacts:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`
  are regular files.
- The structured generation trace is present as one regular JSONL file.
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, and `spec.k` are regular files.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`, SHA-256
  `dc8d425f9133ada84c2a380d6cab8321aba622d443cee4d54bcc98c4859a2289`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, `NOTES.md`, and `prove.sh`. These are
extra untrusted build/evidence artifacts, not trusted inputs. The compiled
directories and bytecode were ignored. No candidate `spec-vacuity.k` or
`PROOF.md` was present; neither was a required generation deliverable.

### Untrusted generation claims

I read `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
and the structured trace only as claims. Their bounded contents and summaries
are preserved in
[`evidence/stage1-untrusted-claims.log`](evidence/stage1-untrusted-claims.log)
and
[`evidence/stage1-generation-summary.log`](evidence/stage1-generation-summary.log).
They claim a successful combined `kprove`, KORE AST linkage, four concrete
runs, and 3,000 Python comparisons. The generation log also records several
earlier parse and stuck-proof failures. None of those claims or prior `#Top`
outputs was used as audit proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

The prose contract in trusted `prompt.py` is:

> For an array of non-negative integers, return its elements ordered first by
> ascending population count and then by ascending integer value.

For example, the prose ordering sends `[1, 5, 2, 3, 4]` to
`[1, 2, 4, 3, 5]`, because `4` has one set bit while `3` has two. The displayed
prompt output `[1, 2, 3, 4, 5]` is therefore inconsistent with the prose. The
negative displayed example is outside the stated domain and is inconsistent
with the trusted canonical implementation as well.

Trusted `canonical.py` performs an initial numeric sort and then a stable sort
by `bin(x)[2:].count("1")`. On non-negative integers this is exactly
lexicographic sorting by `(x.bit_count(), x)`. For negative integers its string
slice still counts the one digits of the magnitude.

Candidate `solution.py` is a recursive insertion sort. `count_ones` uses
`int.bit_count`; `comes_before(a,b)` implements
`(popcount(a),a) <= (popcount(b),b)`; `insert_sorted` recursively inserts into
the sorted tail; and `sort_array` recursively sorts the tail then inserts the
head. It does not mutate the input.

### Translation identity

I regenerated the MPY term using the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/116-sort-array/candidate-src/solution.py \
  > /tmp/audit-work/116-sort-array/trusted-regenerated-solution.mpy
cmp trusted-regenerated-solution.mpy candidate-src/solution.mpy
```

The comparison exited 0. Both files have SHA-256
`914cbcea1a3b771d1d2d753a4b028d2559f181c5cc1b736c3bc98cd558882034`.
The exact command, status, and hashes are in
[`evidence/stage2-translation-identity.log`](evidence/stage2-translation-identity.log).

### Independent differential test

Reviewer-authored
[`evidence/differential_test.py`](evidence/differential_test.py) loads the
trusted canonical and candidate entry points independently and uses a separate
prose oracle `sorted(values, key=(bit_count,value))`. It covers:

- all three documented examples;
- empty, singleton, duplicate, comparator-true, comparator-false, and
  equal-popcount tie boundaries;
- every tuple over values `0..7` through length four;
- large values around powers of two through 128 bits; and
- 3,000 deterministic generated arrays of lengths zero through fourteen.

The 7,696 intended-domain cases had zero candidate/canonical mismatches and
zero candidate/prose-oracle mismatches. Both Python implementations disagreed
with every displayed prompt result in the ways implied by the prompt
inconsistency. The script, exact command, exit 0, inputs, and aggregate results
are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).

This is finite program-fidelity evidence, not a universal K proof.

## 3. Clean proof reconstruction

### Fresh definitions

Only source files were copied to scratch; the copy manifest is in
[`evidence/stage2-scratch-copy.log`](evidence/stage2-scratch-copy.log). The
available independent K installation is K v7.1.293; versions are recorded in
[`evidence/stage3-toolchain.log`](evidence/stage3-toolchain.log).

The generated semantics was rebuilt from `semantic.k`:

```text
kompile semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/116-sort-array/semantic-fresh-kompiled
```

The proof definition was separately rebuilt from `verification.k`:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/116-sort-array/verification-fresh-kompiled
```

Both exited 0. Their complete bounded logs are
[`evidence/stage3-kompile-semantic.log`](evidence/stage3-kompile-semantic.log)
and
[`evidence/stage3-kompile-verification.log`](evidence/stage3-kompile-verification.log).
The compiler warnings concern intentionally unused pattern variables; none is a
parse, structural, coverage, or backend failure.

### Fresh concrete generated-semantics execution

Reviewer-authored
[`evidence/concrete_semantics_compare.py`](evidence/concrete_semantics_compare.py)
ran the fresh semantics on 13 cases: empty, singleton, both equal-popcount tie
directions, lower/higher-popcount branches, the distinguishing prompt inputs,
duplicates, wide popcounts, negative magnitudes, and 64-bit boundaries. Each
`krun` exited 0. Every final K list agreed with both candidate Python and the
trusted canonical. The exact per-case commands and outputs are in
[`evidence/stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).

### Every positive claim, independently

Reviewer-authored
[`evidence/prove_each_claim.sh`](evidence/prove_each_claim.sh) invoked each
claim separately using its fully qualified `SPEC.<label>` name. All 22 runs
exited 0 and printed exactly one `#Top`:

| Claim group | Independently reconstructed result |
|---|---|
| `count-correct`, `comparator-correct` | exit 0, `#Top` |
| `insert-empty`, `insert-at-front` | exit 0, `#Top` |
| empty, singleton, and both pair path claims | exit 0, `#Top` |
| all six length-three path claims | exit 0, `#Top` |
| six fixed end-to-end entry examples | exit 0, `#Top` |
| fixed `example-ordered` and `example-permutation` | exit 0, `#Top` |

The aggregate log is
[`evidence/stage3-prove-each-summary.log`](evidence/stage3-prove-each-summary.log);
the full bounded output and exact command for every claim is preserved
separately below [`evidence/stage3-claims/`](evidence/stage3-claims/).

## 4. Adequacy and real-program pinning

### Program identity

`verification.k` introduces `solutionProgram` and `solutionDefs` only as
macros. I expanded `solutionProgram` with the fresh proof definition and
separately parsed and expanded the trusted-regenerated `solution.mpy`. The two
14,844-byte KORE terms were byte-identical and shared SHA-256
`9a96d862db22077a3e400f6230d59118251f082ee1d8fd8b26e24fb749ee635b`.
The exact commands and status are in
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).

Thus:

- every `#run(solutionProgram, ...)` entry claim executes the submitted AST;
- helper claims using `evalCall(..., solutionDefs)` use the submitted function
  definitions;
- the macro rules add no alternative function result and do not bypass the
  interpreter; and
- there is no right-hand-side-only free result variable or existential oracle.

### Plain-language claim inventory and satisfying witnesses

Reviewer-authored
[`evidence/precondition_witnesses.py`](evidence/precondition_witnesses.py)
exhibits a satisfying ground state for every claim and compares each claimed
ground result with Python. All 22 witnesses passed; sort-entry witnesses agree
with both Python implementations. Exact values are in
[`evidence/stage4-precondition-witnesses.log`](evidence/stage4-precondition-witnesses.log).

| Claim | Precondition in plain language | Postcondition in plain language | Satisfying witness |
|---|---|---|---|
| `count-correct` | Any mathematical integer `N` | Executing submitted `count_ones(N)` returns `popcount(N)` | `N=-5`, result `2` |
| `comparator-correct` | `A` and `B` are non-negative | Submitted comparator returns the model key-order Boolean | `A=1,B=3`, result `true` |
| `insert-empty` | No restriction | Inserting `X` into empty returns the model insertion | `X=3`, result `[3]` |
| `insert-at-front` | `X` comes before/equal to head `Y` | Submitted insertion returns model insertion at the front | `X=1,Y=3,YS=[2]`, result `[1,3,2]` |
| `sort-empty-symbolic` | Empty input | Submitted entry point equals `sortModel([])` | `[]` |
| `sort-singleton-symbolic` | Any singleton | Submitted entry point equals `sortModel` | `[3]` |
| `sort-pair-before` | `A` comes before/equal to `B` | Submitted entry point equals `sortModel([A,B])` | `[1,3]` |
| `sort-pair-after` | `A` does not come before/equal to `B` | Submitted entry point equals `sortModel([A,B])` | `[3,1]` |
| `sort-triple-abc` | `B<=key C` and `A<=key B` | Submitted entry point equals the three-element model result | `[0,1,2]` |
| `sort-triple-bac` | `B<=key C`, `A>key B`, `A<=key C` | Same | `[2,1,4]` |
| `sort-triple-bca` | `B<=key C`, `A>key B`, `A>key C` | Same | `[4,1,2]` |
| `sort-triple-acb` | `B>key C`, `A<=key C` | Same | `[1,4,2]` |
| `sort-triple-cab` | `B>key C`, `A>key C`, `A<=key B` | Same | `[2,4,1]` |
| `sort-triple-cba` | `B>key C`, `A>key C`, `A>key B` | Same | `[4,2,1]` |
| `example-one` | Fixed input `[1,5,2,3,4]` | Exact result `[1,2,4,3,5]` | The fixed input |
| `example-three` | Fixed input `[1,0,2,3,4]` | Exact result `[0,1,2,4,3]` | The fixed input |
| `empty` | Fixed empty input | Exact empty result | `[]` |
| `duplicates` | Fixed duplicate input | Exact result `[0,1,1,3,3]` | The fixed input |
| `wide-popcounts` | Fixed six-element input | Exact result `[0,1,2,8,3,7]` | The fixed input |
| `negative-extension` | Fixed out-of-domain negative input | Exact magnitude-popcount result `[-4,-2,-6,-5,-3]` | The fixed input |
| `example-ordered` | Fixed model computation | Its adjacent keys are ordered | `[1,5,2,3,4]` |
| `example-permutation` | Fixed model computation | Its submitted multiplicity predicate returns true | `[1,5,2,3,4]` |

The six triple preconditions are satisfiable and partition the possible
insertion paths after the tail pair is sorted. The pair preconditions likewise
partition their two paths.

### Material theorem-scope gap

No entry claim has the form
`#run(solutionProgram, listV(IS:Ints)) => listV(sortModel(IS))`, and no
submitted invariant or auxiliary reachability claim inducts over arbitrary
`IS`. Consequently, reconstructed `#Top` results establish:

- arbitrary values only at fixed list lengths zero through three; and
- exact results only for the listed longer ground arrays.

They do **not** establish the HumanEval contract for arbitrary finite
non-negative arrays. Differential testing cannot fill this formal gap.

`example-ordered` and `example-permutation` also concern only one ground model
evaluation, not the arbitrary output of the entry point. Moreover,
`sameMultiplicity(SUPPORT,INPUT,OUTPUT)` checks counts only for values appearing
in `SUPPORT`; by itself it does not exclude fresh values in `OUTPUT`. It is true
for the fixed submitted use, but its informal “permutation” name/comment is
stronger than the predicate's general mathematical meaning.

## 5. Rule-by-rule static soundness review

The complete line-numbered `semantic.k`, `verification.k`, `spec.k`, and
`solution.mpy`, plus inventory counts, are preserved in
[`evidence/stage5-rule-inventory.log`](evidence/stage5-rule-inventory.log).
There are 57 semantic rules, 19 verification rules, 32 local function
declarations, and 22 claims. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, `[owise]`, priority, `anywhere`, or opaque
declarations. The only special local declarations are two macros.

### Local syntax and construct coverage

Every local syntax declaration is inventoried here:

| Source | Local declaration(s) | Review |
|---|---|---|
| `semantic.k:8-36` | `Pgm=Module(Stmts)`; list sorts `Stmts`, `Strings`, `Exprs`, `CmpOps`; `Stmt=FuncDef/If/Return`; `Params`; `Index=Expr/Slice`; `Expr=Int/Bool/Name/UnaryOp/BinOp/BoolOp/Compare/Call/Attribute/ListExpr/Subscript`; `CmpOp`; `Slice`; `Bound=Expr/NoBound` | Recognizable MPY AST syntax. It includes several unused forms, but no used source form is missing. |
| `semantic.k:48-61` | `Ints=.Ints/Int::Ints`; `Val=intV/boolV/listV`; `Vals=.Vals/Val;Vals`; `Def=def/lookupDef`; `Outcome=normal/returned` | Sufficient pure runtime domains for integer-list programs; no heap or mutation is needed by this source. |
| `semantic.k:63-85` | `#run` and the 24 functions listed below | Function equations are reviewed rule-by-rule below. None is declared total. |
| `verification.k:9-10` | macro terminals `solutionProgram`, `solutionDefs` | Exact expanded term matches trusted-regenerated program. |
| `verification.k:59-66` | eight functions: `popcount`, `beforeEq`, `ordered`, `allNonnegative`, `sameMultiplicity`, `insertModel`, `sortModel`, `occurrences` | Mathematical/model layer; equations reviewed below. |

The submitted MPY constructors map as follows:

| Used submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, statement juxtaposition | `semantic.k:8-16`; `#run`, lookup, invocation at `89-104` |
| `If`, `Return` | syntax `11-13`; statement/outcome rules `106-119` |
| `Name` | syntax `24`; lookup rules `123-124` |
| `Call(Name(...))`, `Call(Attribute(...,"bit_count"))` | syntax `29-30`; rules `133-139`, argument rules `147-149` |
| `BoolOp("or"/"and")` | syntax `27`; rules `129-130`, `173-174` |
| `Compare` with `==`, `<`, `<=` and one `CmpOp` | syntax `28,34`; rules `131-132`, `166-171` |
| `ListExpr` and expression lists | syntax `18,31`; rules `140-141`, `151-153` |
| `Subscript(...,Int(0))` | syntax `32`; rules `142-143`, `186` |
| `Subscript(...,Slice(Int(1),NoBound,NoBound))` | syntax `32,35-36`; rules `144-145`, `187` |
| list `BinOp("+",...)` | syntax `26`; rules `127-128`, `160`, `189-190` |
| integer literals `0` and `1` | syntax `22`; rule `121` |

Unused syntax such as general unary expressions, `len`, `%`, `//`, Boolean
literals, and general slices is not needed for the submitted program. Its
partial coverage is therefore not a missing-used-construct defect in generated
semantics mode.

### All 24 semantic function declarations

| Function declarations | Coverage decision |
|---|---|
| `#run`, `evalCall`, `invoke`, `outcomeValue` | Covered for the submitted top-level module, one/two-argument functions, and returning paths. |
| `lookupDef`, `lookupEnv` | Deterministic on the submitted unique definitions and one/two-variable environments. |
| `evalStmts`, `evalAfterIf`, `continueWith` | Complete for submitted `If`/`Return` control paths. |
| `evalExpr`, `evalUnary`, `evalBin`, `evalCompare`, `evalBoolBin`, `evalBitCount`, `evalLen`, `evalIndex`, `evalTail` | Every submitted expression shape and every reachable operand type/operator has an equation. Unused advertised shapes may remain stuck. |
| `evalArgs`, `evalListItems`, `appendInts`, `intOf`, `lengthInts` | Structural recursion on finite lists; complete on reachable values. |
| `bitCount` | Negative, zero, and positive guards are disjoint and exhaustive on `Int`; positive recursion decreases by division by two. |

No declared function introduces a fresh or opaque value. All result-bearing
values are fixed by equations on the reachable domain.

### All 57 `semantic.k` rules

Each row below decides every ordinary semantic rule. “Sound here” means sound
for the submitted source and intended well-typed integer-list inputs, which is
the permitted minimal generated-semantics scope.

| Line | Rule | Decision |
|---|---|---|
| 89 | `#run(Module(DEFS),INPUT)` calls `"sort_array"` | Sound here; selects the real submitted entry name. |
| 91 | matching `lookupDef` | Sound here; returns the matching submitted body/parameters. |
| 92-94 | nonmatching `lookupDef` recursion | Sound; guard is disjoint from line 91 and structurally descends. |
| 96-97 | `evalCall` to `invoke(lookupDef(...))` | Sound here; no execution body is skipped. |
| 99-100 | one-parameter invocation | Sound for `count_ones` and `sort_array`; binds the sole argument. |
| 101-102 | two-parameter invocation | Sound for comparator and insertion helpers; binds both arguments. |
| 104 | returned outcome to value | Sound for completed function calls. |
| 106 | empty statement list to `normal` | Sound. |
| 107-108 | `Return(E)` evaluates `E` and discards following statements | Sound Python return control for this pure subset. |
| 109-110 | `If` evaluates condition then delegates | Sound here. |
| 112-114 | true `If` branch | Sound; guard is Boolean true. |
| 115-117 | false `If` branch | Sound; disjoint/exhaustive with the prior branch. |
| 118 | returned branch propagates return | Sound; preserves abrupt function return. |
| 119 | normal branch continues with rest | Sound. |
| 121 | integer literal | Sound. |
| 122 | Boolean literal | Sound but unused by the submitted AST. |
| 123 | name expression delegates to environment | Sound here. |
| 124 | map lookup | Sound for the submitted unique local bindings. |
| 125-126 | unary expression dispatch | Sound dispatcher; submitted source does not use it. |
| 127-128 | binary expression dispatch | Sound here; submitted operands are pure. |
| 129-130 | two-operand Boolean dispatch | Value-correct for the submitted pure total comparisons. It is eager rather than Python-short-circuiting in general; see limitations below. |
| 131-132 | singleton comparison dispatch | Sound for every submitted comparison, all of which have one operator. |
| 133-134 | `len` call | Sound for modeled list values but unused. |
| 135-136 | `int.bit_count()` call | Sound on modeled mathematical integers. |
| 137-139 | named function call except `"len"` | Sound here; all submitted bindings are unique top-level functions. |
| 140-141 | list literal evaluation | Sound for submitted integer-only list literals. |
| 142-143 | expression index dispatch | Sound here; only nonempty index zero is reachable. |
| 144-145 | exact tail-slice dispatch | Sound for the only submitted slice `[1:]`. |
| 147 | empty argument list | Sound. |
| 148-149 | nonempty argument list recursion | Sound here; structurally descends and arguments are pure. |
| 151 | empty list-literal items | Sound. |
| 152-153 | nonempty integer list-literal items | Sound for the submitted integer-list value domain. |
| 155 | unwrap `intV` | Sound. |
| 157 | unary minus | Sound on arbitrary integers, unused by source AST. |
| 159 | integer addition | Sound, unused as a source operation. |
| 160 | list concatenation | Sound and used by insertion. |
| 161-162 | integer remainder, nonzero divisor | Sound, unused as a source operation. |
| 163-164 | integer division, nonzero divisor | Sound on the positive operands relevant to popcount; unused as a source operation. |
| 166 | integer equality | Sound. |
| 167 | empty-list equality | Sound and used on base cases. |
| 168 | nonempty equals empty | Sound and used on recursive cases. |
| 169 | empty equals nonempty | Sound but unreachable in this source. |
| 170 | integer `<` | Sound. |
| 171 | integer `<=` | Sound. |
| 173 | Boolean `and` | Truth-table sound on Boolean values. |
| 174 | Boolean `or` | Truth-table sound on Boolean values. |
| 176 | `bit_count` wrapper | Sound if `bitCount` equations below represent population count; they do. |
| 177 | negative `bitCount` uses magnitude | Sound for Python `int.bit_count`; guard disjoint from zero/positive. |
| 178 | zero population count | Sound. |
| 179-180 | positive parity recursion | Sound ordinary population-count recurrence; `N/2` decreases for `N>0`. |
| 182 | length wrapper | Sound but unused. |
| 183 | empty length | Sound. |
| 184 | cons length | Sound and structurally decreasing. |
| 186 | zero index of nonempty list | Sound; exactly the only reachable index. |
| 187 | tail of nonempty list | Sound for `[1:]`. |
| 189 | append empty left list | Sound. |
| 190 | append cons recursion | Sound and structurally decreasing. |

### All 19 `verification.k` rules

| Line | Rule | Class and decision |
|---|---|---|
| 11 | `solutionProgram => Module(solutionDefs)` | Macro expansion; exact KORE pinning establishes identity. |
| 12-55 | `solutionDefs =>` the four submitted definitions | Macro expansion; exact KORE pinning establishes identity. It supplies syntax, not an execution result. |
| 68 | `popcount(N) => bitCount(N)` | Definitional alias. It reuses the audited semantic recurrence and is not an independent theorem about bit count. |
| 70-72 | `beforeEq(I,J)` | Truthful lexicographic key-order definition. |
| 74 | insert into empty model list | Truthful. |
| 75-76 | insert at front when `beforeEq` | Truthful; guard and result agree. |
| 77-78 | recurse when not `beforeEq` | Truthful, disjoint/exhaustive with prior nonempty rule, structurally decreasing. |
| 80 | sort empty model list | Truthful. |
| 81 | sort cons by tail sort then insertion | Truthful insertion-sort definition, structurally decreasing. |
| 83 | empty list is ordered | Truthful. |
| 84 | singleton is ordered | Truthful. |
| 85 | longer list ordered iff head pair and tail are ordered | Truthful adjacency definition, structurally decreasing. |
| 87 | empty list is all-nonnegative | Truthful but unused by all submitted claims. |
| 88 | cons non-negativity recursion | Truthful and structurally decreasing; unused. |
| 90 | zero occurrences in empty | Truthful. |
| 91 | matching head adds one | Truthful. |
| 92-93 | nonmatching head skipped | Truthful; guard disjoint from matching rule. |
| 98 | empty support makes multiplicity check true | Truthful for the predicate as defined, but shows why it is not full multiset equality by itself. |
| 99-101 | compare one support value then recurse | Truthful for the predicate as defined; structurally decreasing. |

The model rules do not preempt or replace `evalCall`, `evalExpr`, function
bodies, returns, or recursion. They appear on claim right-hand sides or in
model-only claims. There is consequently no operational bridge requiring an
execution-context equivalence theorem and no result-bearing oracle shared
circularly between program execution and the postcondition.

### Control, state, overlaps, and generated-semantics limitations

- Configuration: a single `<k>` cell is adequate because the submitted
  program is pure. Environments are explicit `Map` arguments to evaluator
  functions. There is no heap allocation, mutation, I/O, or exception state in
  the submitted well-typed paths.
- Calls/returns: submitted definitions execute through lookup, parameter
  binding, statement evaluation, and returned outcomes. Recursive calls do not
  use a summary shortcut.
- Branches: all reachable Boolean guards have disjoint true/false rules.
- Lists: recursion and slicing decrease structurally; index zero occurs only
  after a nonempty check.
- Equation overlaps: same-symbol rules are disjoint by constructors, operator
  strings, types, or complementary guards. No overlapping pair has differing
  right-hand sides on a reachable overlap.
- Totality: no local symbol asserts `[total]`. Several interpreter functions
  intentionally remain undefined on unsupported or ill-typed inputs, which is
  acceptable for minimal generated semantics when those terms cannot arise.

The definition is not a general Python semantics. In particular, `and`/`or`
are eager rather than short-circuiting; argument evaluation is modeled only
for pure expressions; duplicate/rebound function names, exceptions, arbitrary
list equality, general indexing/slicing, heterogeneous lists, and resource
limits are not modeled. No such divergence yields a false conclusion for this
submitted program on the intended non-negative integer-list domain: all
Boolean operands are pure total comparisons, all function arguments are pure,
definitions are unique, and every index/slice is guarded and fixed. Therefore
I record these as a narrow language-model boundary, not as unsound rules. No
claimed rule was labeled unsound without an intended-domain false-conclusion
witness.

## 6. Fresh non-vacuity test

The reviewer mutation
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) changes the
result-constraining `example-one` destination from the true
`[1,2,4,3,5]` to the false `[0,2,4,3,5]`. Its fixed input is a satisfying
entry state, and both Python implementations return the true result.

First, `kprove --dry-run` parsed and built the mutated spec successfully with
exit 0; see
[`evidence/stage6-mutation-build.log`](evidence/stage6-mutation-build.log).
Then the real proof command exited 1 with `WarnStuckClaimState`. The residual
configuration explicitly contains:

```text
listV ( 1 :: 2 :: 4 :: 3 :: 5 :: .Ints ) ~> .K
```

which cannot unify with the mutated destination. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. The exact proof command and residual are in
[`evidence/stage6-mutation-proof.log`](evidence/stage6-mutation-proof.log).

## 7. Proven versus assumed accounting

### Precisely what the successful K proofs establish

Conditional on the fresh K definition:

1. Submitted `count_ones` agrees with the model alias `popcount` for every K
   integer.
2. Submitted `comes_before` agrees with `beforeEq` for every non-negative pair.
3. Submitted insertion agrees with `insertModel` for the empty and
   insert-at-front cases only.
4. Submitted `sort_array` agrees with `sortModel` for every K integer list of
   length at most three, split across exhaustive path preconditions.
5. Submitted `sort_array` returns the exact asserted result for six fixed
   inputs.
6. For one fixed model-sorted example, the model adjacency predicate and the
   limited support-based multiplicity predicate both reduce to true.

It does not establish arbitrary-list entry-point correctness, universal
ordering, universal permutation preservation, or the prompt's inconsistent
displayed outputs.

### Trust ledger

| Boundary | What is assumed or informally checked | Influence | Assessment/evidence |
|---|---|---|---|
| K toolchain and Haskell backend | Compiler, parser, built-in rewriting, and prover implement K correctly | All proofs | Ordinary unavoidable trusted computing base; fresh v7.1.293 commands recorded. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, and list machinery | Mathematical integers, Boolean operations, strings/maps, and generated list syntax have their standard K meanings | Values, guards, environments | Acceptable low-level primitive boundary; no task answer is encoded in it. |
| Trusted translator | `/reference/py2mpy.py` faithfully represents the Python AST in the MPY constructors | Real-program identity | User-designated trusted input; byte identity and KORE macro identity independently checked. |
| Generated semantics-to-Python bridge | The 57 local rules model this pure source on integer-list inputs | Execution and result | Exhaustively reviewed above and concretely checked on 13 branch/boundary cases. This remains an informal language-semantics argument, not a machine-checked CPython refinement theorem. |
| `bitCount` recurrence | Magnitude, parity, and halving equations equal Python `int.bit_count` | Comparator and all results | Ordinary mathematics; guards are exhaustive/disjoint and recursion decreases. Differential and concrete evidence support the bridge. |
| Unbounded resources | K mathematical recursion ignores CPython recursion depth, memory exhaustion, and implementation resource limits | Termination/exception behavior on very long lists | Acceptable for abstract partial correctness only if resource failures are excluded; concerning as a literal CPython execution model. |
| Prose/canonical bridge | Nested stable sorts in canonical equal lexicographic `(popcount,value)` order on non-negative integers | Natural-language intent | Mathematically direct and supported by 7,696 independent cases. Displayed prompt examples conflict and are explicitly excluded. |
| Opaque symbols/oracles | None | None | No opaque or unconstrained result-bearing boundary exists. |
| Operational proof bridges | None | None | Program-defined bodies execute under the generated interpreter. |

### Validation gates

- **Gate A — real-program soundness: PASS for the submitted claims.** Fresh
  reconstruction closes every claim; KORE pins the real AST; no program body
  is replaced; results are concrete/model-constrained; equations are sound on
  reachable inputs; and the false result mutation is rejected.
- **Gate B — intent adequacy: FAIL / SOUND-BUT-LIMITED.** The intended contract
  ranges over arbitrary non-negative arrays, but symbolic proof coverage ends
  at length three. Fixed longer tests and finite differential evidence do not
  supply the missing universal theorem. The prompt's displayed examples are
  also inconsistent with its prose and canonical implementation.
- **Gate C — trust and evidence auditability: PASS.** Reviewer scripts,
  inputs/scopes, exact commands, exit statuses, bounded outputs, fresh build
  products, per-claim logs, and mutation residual are preserved. The finite
  evidence is not presented as proof.

The appropriate decision is therefore `CONCERNS / LEGIT`: the reconstructed
claims are honest, sound partial-correctness theorems about the actual program,
but they fall materially short of universal HumanEval-task correctness.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
