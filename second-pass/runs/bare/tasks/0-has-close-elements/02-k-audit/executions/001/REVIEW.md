# Independent adversarial audit: 0-has-close-elements

## Executive decision

The candidate's nine submitted reachability claims do reconstruct and are
non-vacuous, but they are not a legitimate proof of the real generated
program. The decisive failures are:

1. `spec.k` never executes or even references `solution.mpy`. It starts from
   `verify(...)`, whose rule executes a separately embedded
   `solutionProgram` AST. A body-sensitivity experiment changed the executable
   file so the empty-list case returned `true`; fresh concrete execution
   changed to `true`, while a fresh proof build still proved the embedded
   empty-list result was `false`.
2. The generated semantics models inputs as exact rationals, not Python
   binary floats. On the intended input `[0.1, 0.3]` with threshold `0.2`,
   both trusted and submitted Python return `True`, while concrete execution
   of `solution.mpy` under the submitted decimal-rational encoding returns
   `false`.
3. The formal claims do not cover the natural contract's arbitrary lists of
   floats. Apart from two fixed examples, they cover only empty and singleton
   integer lists, symbolic integer lists of lengths two through four, and two
   fixed rational boundary cases.

The clean `#Top` results therefore establish finite theorems about an embedded
AST under an exact-rational model, not partial correctness of the submitted
program over the requested domain.

## 1. Input and provenance integrity

I treated every file below `/candidate` as an untrusted claim. The detailed
type, path, hash, mount, prompt, and translator checks are in
`evidence/stage1-integrity.log`; the reviewer script is
`evidence/stage1_integrity.sh`.

- All required artifacts were present as regular files:
  `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
  `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`.
  None was a symlink or a mistyped directory/device.
- The candidate also contains `prove.sh`, a structured JSONL trace, and
  candidate-built `semantic-kompiled/` and `verification-kompiled/` trees.
  Those extra built trees were inventoried but never copied into or used by
  this audit.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a`).
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The rendered mode is `GENERATED_SEMANTICS`, and
  `/reference/reference-semantics` does not exist. The trusted reference
  mount contains exactly the three expected regular files
  `canonical.py`, `prompt.py`, and `py2mpy.py`. There is no semantics-mode
  contradiction and hence no infrastructure breach.
- The untrusted run metadata says this was the bare/no-supplied-semantics
  condition, exited 0, and was not timed out. `codex-last.txt`,
  `codex-output.log`, and the structured trace claim that `kprove` returned
  `#Top`. I did not rely on those claims. Their bounded inspection is recorded
  in `evidence/stage1-small-claims.log` and
  `evidence/stage1-untrusted-log-summary.log`.

One non-substantive diagnostic in `evidence/stage1-claims-sizes.log` exits 127
because the container lacks the optional `file` utility; its preceding byte
and line counts completed. All integrity decisions come from the independent
exit-0 integrity script and standard `stat`/`find`/`cmp` checks, not that
diagnostic.

Stage 1 result: **PASS**. No input-integrity or rendered-mode failure was
found.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`, the required entry
point is:

```python
has_close_elements(numbers: List[float], threshold: float) -> bool
```

It must return `True` exactly when there are two distinct indices `i != j`
such that `abs(numbers[i] - numbers[j]) < threshold`; equality with the
threshold is false. Empty and singleton lists return false.

The trusted canonical implementation checks every ordered pair of distinct
indices. The submitted `solution.py` instead recursively checks each head
against its tail and then recurses over the tail. Subject to normal return,
that is the same existential-pair algorithm.

### Trusted translation

I regenerated the MPY file from the scratch copy of `solution.py` using
`/reference/py2mpy.py`. `cmp` exited 0, and both submitted and regenerated
files have SHA-256
`72ab5b828433279d72f5d206ad80275be823630222794f4eb041ff7b8057178d`.
The exact command and result are in `evidence/stage2-regenerate.log`.

### Independent differential test

The reviewer-authored `evidence/differential.py` independently imports
`/reference/canonical.py` and the scratch copy of the submitted
`solution.py`. It checks:

- both documented examples;
- empty, singleton, strict equality/just-above/just-below, duplicates,
  negative/zero thresholds, negative values, an end-only close pair, NaN,
  infinity, and infinite threshold;
- all lists of lengths 0 through 5 over
  `{-2, -1, 0, 0.5, 1, 2}` with five threshold values;
- 2,000 deterministic generated cases; and
- a length-1100 recursion-depth boundary.

The run in `evidence/stage2-differential.log` reports 48,672 cases, zero
normal-return mismatches, and one exceptional-outcome mismatch. For the
length-1100 list `[0.0, ..., 1099.0]` with threshold `-1.0`, the canonical
loop returns `False` while the submitted recursive Python implementation
raises `RecursionError`. That is a total-behavior limitation of the rewrite;
partial correctness alone does not assert termination, but it is part of the
implementation-to-intent ledger.

Stage 2 result: **PASS for normal-return functional fidelity and byte
translation**, with the documented CPython recursion-depth limitation.

## 3. Clean proof reconstruction

All source files needed for execution were copied as regular files to
`/tmp/audit-work/source`. No candidate-built definition, cache, or compiled
artifact was copied. K was independently available as version v7.1.293.

### Fresh builds

The concrete definition was rebuilt with:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-kompiled
```

It exited 0 (`evidence/stage3-kompile-semantic.log`).

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

It exited 0 (`evidence/stage3-kompile-verification.log`).

The aggregate submitted spec exited 0 and printed `#Top`
(`evidence/stage3-kprove-all.log`).

### Every positive claim independently

Because the submitted claims are unlabeled, I copied each claim verbatim into
a distinct module in `evidence/audit-positive-claims.k`. The driver
`evidence/run_positive_claims.sh` invoked nine separate `kprove` processes.
Every process exited 0 and printed an exact `#Top`; see
`evidence/stage3-kprove-claim-1.log` through
`evidence/stage3-kprove-claim-9.log`.

### Fresh generated-semantics execution

The actual scratch `solution.mpy` was run with the fresh concrete definition
on ten cases: both examples, empty, singleton, exact and just-above strict
boundaries, negative threshold, two negative-rational boundaries, and a
four-element list whose only close pair is at the end. Each K result matched
both Python implementations. The independent Python oracle is
`evidence/concrete_oracle.py`, its output is
`evidence/stage3-concrete-python-oracle.log`, and the exact K commands and
results are the `evidence/stage3-krun-*.log` files.

This positive concrete sample does not repair the later decimal-rational
counterexample.

Stage 3 result: **PASS**. The candidate's finite positive claims genuinely
reconstruct and close.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

None of the nine claims has an explicit `requires`; each left-hand structural
pattern is its precondition.

| Claim | Precondition | Postcondition |
|---|---|---|
| 1 | Exact rational list `[1,2,3]`, threshold `1/2` | Returns false |
| 2 | Exact rational prompt list `[1,2.8,3,4,5,2]`, threshold `3/10` | Returns true |
| 3 | Empty list, any integer threshold | Returns false |
| 4 | One arbitrary integer, any integer threshold | Returns false |
| 5 | Two arbitrary integers and integer threshold | Returns exactly `abs(X-Y) < T` |
| 6 | Three arbitrary integers and integer threshold | Returns the submitted recursive pair predicate |
| 7 | Four arbitrary integers and integer threshold | Returns the submitted recursive pair predicate |
| 8 | Exact rational list `[1,1.5]`, threshold `1/2` | Returns false |
| 9 | Exact rational list `[1,1.5]`, threshold `5000001/10000000` | Returns true |

`evidence/claim_witnesses.py` supplies one realizable ground state for every
precondition. In `evidence/stage4-claim-witnesses.log`, the claimed ground
result agrees with both trusted and submitted Python for all nine witnesses.
Thus the claims are not made vacuous by impossible preconditions.

There is no general list claim, induction/circularity, or recursive helper
claim. Claims 6 and 7 simply unroll the interpreter at fixed lengths. Claim 2
is a fixed six-element example, not a symbolic length-six theorem.

### Failure to pin `solution.mpy`

The concrete initial configuration in `semantic.k` is:

```k
configuration <k> runProgram($PGM:Pgm, $ARGS:PValues) </k>
```

and its rule executes the parsed `$PGM`. No submitted proof claim starts from
that configuration. Every claim starts from `verify(ARGS)`, and
`verification.k` contains:

```k
rule <k> verify(ARGS)
  => call("has_close_elements", ARGS, solutionFunctions) ... </k>
```

`solutionFunctions` is collected from a separately typed
`solutionProgram` literal embedded in `verification.k`. Neither `spec.k` nor
`verification.k` references, imports, hashes, parses, or otherwise consumes
`solution.mpy`. The embedded literal visually agrees with the original
submitted AST, but that is an informal duplication, not a proof-local
connection to the file.

The required body-sensitivity witness is decisive:

1. In scratch, I changed only the executable `solution.mpy` base case for
   `len(numbers) < 2` from `Return(Bool(false))` to
   `Return(Bool(true))`. The exact diff is
   `evidence/stage4-body-mutation-diff.log`.
2. Fresh concrete execution of that mutated file on an empty list exited 0
   with `<k> VBool ( true ) </k>`
   (`evidence/stage4-mutant-krun-empty.log`).
3. I freshly rebuilt `verification.k` in the mutant workspace; the build
   exited 0 (`evidence/stage4-mutant-kompile-verification.log`).
4. The empty-list proof still exited 0 with `#Top`, proving
   `VBool(false)` (`evidence/stage4-mutant-kprove-claim3.log`).

This witness shows that the purported program connection is insensitive to a
material body change. If the `verify` claims are interpreted as claims about
the executable file, the bridge admits the concrete false conclusion
"the mutated empty-list program returns false" even though its real concrete
execution returns true. Under the validation contract this is a Gate A1
real-program pinning failure and falls squarely under "proves a substituted
program."

Stage 4 result: **FAIL**.

## 5. Rule-by-rule static soundness review

The complete machine-extracted inventory is
`evidence/stage5-rule-inventory.log`; the full line-numbered sources are in
`evidence/source-k-files.log`. There are no generated helper K files beyond
`semantic.k`, `verification.k`, and `spec.k`.

### Local syntax and declaration inventory

`semantic.k` contains these local syntax families:

- Program/statement grammar: `Pgm = Module(Stmts)`; list sorts `Stmts`,
  `Strings`, `Exprs`, and `CmpOps`; statements `ImportFrom`, `FuncDef`, `If`,
  and `Return`; `Params`; `CmpOp`; `Index`; `Bound`; and `Slice`.
- Expression grammar: `Name`, `Int`, `Float`, `Bool`, `BinOp`, `Compare`,
  `Call`, and `Subscript`.
- Runtime values and functions: `VInt`, `VRat`, `VBool`, `VList`, `VNone`,
  `PValues`, and `function(Params,Stmts)`.
- Computation/helper symbols: `runProgram`; functional `call`, `exec`,
  `branch`, `eval`, `subValue`, `absValue`, `compareValue`,
  `subscriptValue`, `sliceOne`, `lengthValue`, `evalExprs`, `concatStmts`,
  `collect`, `bind`, and `lengthValues`; plus the `verify` K item.

`verification.k` adds functional `solutionProgram`, `solutionFunctions`,
`functionsOf`, `closePair`, `closeFirstRef`, `hasCloseRef`, and `boolOf`.

There are 21 `syntax` declaration statements in `semantic.k` and three
declaration statements in `verification.k` (with alternatives as enumerated
above). There are no `[total]`, `[functional]`, `[concrete]`, `[owise]`,
priority, trusted, or opaque declarations. The only local simplification rule
is the symbolic-`#if` distribution rule at `semantic.k:98`. All other local
rules are ordinary semantic/function rules.

`Float` expressions and `VNone` are declared but have no evaluator rule. They
are unused by `solution.mpy`, so this is acceptable minimal generated
coverage rather than fabricated behavior.

### Mapping every used MPY construct

| Construct in `solution.mpy` | Declaration and operational coverage |
|---|---|
| `Module`, `ImportFrom`, `FuncDef` | Program/statement syntax; `runProgram` and the three `collect` rules discard the import and build the two-function map |
| `Params`, statement/expression lists | List syntax; the two `bind`, two `concatStmts`, and two `evalExprs` rules |
| `If`, `Return` | The two `exec` rules and two `branch` rules |
| `Name`, `Int`, `Bool` | The three atomic `eval` rules |
| `BinOp("-")` | `eval(BinOp)` and four constructor-specific `subValue` rules |
| `Compare`, `CmpOp("=="/"<")` | `eval(Compare)` and five relevant `compareValue` rules |
| `Call(len)`, `Call(abs)`, user calls | Three disjoint call-evaluation rules, `lengthValue`, `absValue`, and `call` |
| `Subscript(..., Int(0))` | Expression-index `eval(Subscript)` plus `subscriptValue` |
| `Subscript(..., Slice(Int(1),NoBound,NoBound))` | Slice-specific `eval(Subscript)` plus `sliceOne` |

Every construct actually present in `solution.mpy` therefore has a rule
path. No catch-all oracle or fabricated result is used for an unmodeled used
construct.

### All 41 `semantic.k` rules

Each semicolon-separated item below names a distinct rule; the judgment
applies to every named rule.

| Lines/rules | Static decision |
|---|---|
| 74 `runProgram` | Correctly collects the parsed module and invokes the requested entry point. This is the path used by `krun`, but not by the submitted claims. |
| 77 empty `collect`; 78 import `collect`; 79 function `collect` | Correct for the target module: imports have no runtime effect and unique function definitions become map bindings. Duplicate definitions are outside this target. |
| 82 empty `bind`; 83 recursive `bind` | Correct positional binding for equal-length parameter/argument lists. Every target call has matching arity; mismatches visibly stick rather than invent values. |
| 86 `call` | Correctly selects the named function map binding and evaluates its real stored body with a fresh parameter environment. |
| 89 return `exec`; 90 if `exec` | Return discards following statements, and if evaluates its condition before concatenating only the selected body with the continuation. This matches the pure target program's control flow. |
| 93 Boolean `branch`; 98 symbolic-`#if` branch simplification | The concrete rule selects exactly one branch. The simplification distributes the same branch operation over a symbolic Boolean conditional; its overlap with a later-concrete Boolean agrees. It changes no cell or continuation. |
| 105 empty `concatStmts`; 106 recursive `concatStmts` | Standard list concatenation, terminating on the first list. |
| 109 name `eval`; 110 integer `eval`; 111 Boolean `eval` | Correct environment lookup and value injection. |
| 113 subtraction `eval`; 115 comparison `eval` | Correctly delegates the only used binary and comparison forms. Subexpressions are pure here, so symbolic normalization order cannot change state or control. |
| 118 `len` call; 120 `abs` call; 122 user call | The built-ins have specific rules; the general call is guarded to exclude `"len"` and `"abs"`, so there is no conflicting overlap. Argument evaluation and source-function lookup are preserved. |
| 126 empty `evalExprs`; 127 recursive `evalExprs` | Correct positional argument-list evaluation. The target expressions have no side effects. |
| 130 index `eval(Subscript)`; 132 slice `eval(Subscript)` | Sort-disjoint and exactly cover the target's `[0]` and `[1:]` uses. Earlier length checks guarantee nonempty accesses on real paths. |
| 135 `lengthValue`; 137 empty `lengthValues`; 138 recursive `lengthValues` | Correct list length over arbitrary-precision K integers. |
| 140 `subscriptValue`; 141 `sliceOne` | Correct head and tail operations for a nonempty list. |
| 143 int-int `subValue`; 144 rat-rat; 146 rat-int; 147 int-rat | Ordinary exact-rational subtraction. These preserve a positive denominator when inputs have positive denominators. |
| 149 integer `absValue`; 150 rational `absValue` | Correct for integers and positive-denominator rationals. The rational rule lacks an explicit `B > 0` guard; negative/zero denominators are not excluded syntactically. Subsequent rational comparison guards prevent a negative-denominator Boolean result in the mixed-sign cases, usually leaving a stuck term. This is an over-broad/unformalized representation boundary, not the basis of a false submitted closed claim. |
| 152 integer equality; 153 integer less-than; 154 rat-rat less-than; 157 rat-int; 160 int-rat | Correct integer and positive-denominator cross-multiplication equations. Their guards are disjoint by constructors/operator or agree. Unsupported comparisons stick. |

The semantics has only the `<k>` cell. That is sufficient for this pure,
side-effect-free program: environments and function maps are explicit
arguments to functional terms, and the source has no heap mutation, I/O,
allocation, exceptions intentionally modeled, or observable state beyond the
return value. Recursive calls and returns execute the stored source bodies;
there is no call-result oracle.

### All 11 `verification.k` rules

| Lines/rules | Static decision |
|---|---|
| 9 `solutionProgram` | A closed definitional AST constant. It visually duplicates the original translated AST, but has no machine-checked identity connection to `solution.mpy`. |
| 48 `solutionFunctions`; 49 `functionsOf` | Truthful collection of that closed AST's function map. |
| 50 `verify` | Executes the embedded program bodies and preserves an arbitrary `<k>` continuation, so it is value/control faithful to the embedded literal. It is nevertheless an illegitimate harness for claims presented as proofs of the file, as the body-mutation witness demonstrates. |
| 59 `boolOf`; 60 `closePair` | Truthful extraction of a Boolean comparison and exact-rational/int closeness predicate wherever the underlying operations reduce. |
| 63 empty `closeFirstRef`; 64 nonempty `closeFirstRef` | Disjoint, terminating list recursion expressing whether the head is close to a tail element. |
| 67 empty `hasCloseRef`; 68 singleton `hasCloseRef`; 69 two-or-more `hasCloseRef` | Disjoint, terminating list recursion expressing existence of a close unordered pair. |

The reference functions are not opaque and do not replace execution of the
source bodies. For claims 6 and 7, the prover executes the embedded source
and independently normalizes these equations at fixed list lengths. There is
no universal connection theorem for arbitrary lengths, because no such
program claim was submitted.

### Overlaps, priorities, coverage, and numeric witness

- The user-call guard excludes the two built-in call rules.
- Expression index and slice rules are sort-disjoint.
- Constructor/operator-specific arithmetic rules are disjoint.
- Empty, singleton, and recursive reference-list equations are disjoint.
- The symbolic branch simplification agrees with concrete selection on its
  overlap.
- There are no priorities, totality assertions, opaque values, or
  result-bearing fresh symbols.
- Functions are intentionally partial outside the used subset. Missing
  semantics produces a visible stuck term rather than a guessed result.

The arithmetic equations themselves are sound exact-rational mathematics on
the positive-denominator domain. The bridge from that domain to the requested
Python-float behavior is not sound. The candidate's own examples encode
decimal values as `VRat(decimal numerator, decimal denominator)`. Using the
same encoding:

```text
Python input: [0.1, 0.3], threshold 0.2
Python distance: 0.19999999999999998
trusted canonical: True
submitted Python: True
K input: VList(VRat(1,10),VRat(3,10)), VRat(2,10)
fresh krun result: VBool(false)
```

The Python witness is
`evidence/stage5-float-rounding-python.log`; the exact concrete K command and
false result are `evidence/stage5-float-rounding-krun.log`. This is a
concrete false-conclusion witness on the intended `List[float]` domain for
the generated semantics bridge. NaN and infinities are also not represented.

Stage 5 result: **FAIL for real-Python numeric adequacy and proof-file
connection**, although the individual exact-rational operational equations
used by the finite claims are otherwise sound.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was used. I created the fresh mutation
`evidence/spec-vacuity.k`, changing submitted claim 3's result-bearing
obligation on the realizable input `numbers=[]`, `threshold=0` from false to
true:

```k
claim <k> verify(VList(.PValues), VInt(0)) => VBool(true) </k>
```

Both Python implementations and fresh concrete K execution return false for
this witness.

- `kprove ... --dry-run` exited 0, proving the mutation imports and builds
  correctly (`evidence/stage6-vacuity-dry-run.log`).
- The real proof exited 1 with `WarnStuckClaimState`. Its residual is exactly
  `<k> VBool ( false ) ~> .K </k>`, so failure is caused by the intended unmet
  result obligation, not parsing, import failure, timeout, or an unrelated
  crash (`evidence/stage6-vacuity-kprove.log`).

Stage 6 result: **PASS**. The finite submitted claims constrain their results
and are not vacuous.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the freshly compiled submitted exact-rational semantics and the
separately embedded `solutionProgram` constant, the nine configurations
listed in Stage 4 rewrite to their stated Boolean results. This includes
symbolic integer theorems for list lengths zero through four, two prompt
examples, and two fixed rational boundaries. The proof executes the embedded
function bodies; it does not use an unconstrained oracle.

It does **not** establish:

- any theorem about the bytes or parsed term of `solution.mpy`;
- correctness for arbitrary list length;
- correctness for arbitrary Python floats;
- CPython termination or absence of `RecursionError`;
- Python binary-float, NaN, or infinity behavior; or
- a universal equivalence between the program and `hasCloseRef`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, Haskell backend, and imported `BOOL`, `INT`, `MAP`, `STRING`, and `K-EQUAL` domains | All builds and proofs | Acceptable low-level tool and mathematical primitive boundary |
| Trusted `/reference/py2mpy.py` plus byte identity | Link from submitted Python AST translation to original `solution.mpy` | Acceptable and independently checked, but it does not link the MPY file to the proof's duplicate AST |
| `solutionProgram` is the same program as `solution.mpy` | Every submitted claim | Illegitimate as a proof boundary: no file is consumed, and the fresh body-sensitivity witness shows the proof is unchanged when file behavior changes |
| Positive-denominator exact rationals stand for Python `float` | Rational concrete executions and intent bridge | Materially false as a general bridge; `[0.1,0.3], 0.2` is a concrete opposite-result witness |
| Recursive `closeFirstRef`/`hasCloseRef` equations express pair existence | Claims 6 and 7 | Acceptable ordinary mathematics for their fixed integer list lengths; no arbitrary-length program theorem was submitted |
| Trusted canonical Python implementation | Intent oracle for differential and witness tests | Acceptable independent oracle evidence, not part of the K proof |
| 48,672 Python differential cases and ten initially matching K concrete cases | Empirical source and semantic support | Finite evidence only; it neither proves universal equivalence nor overrides the discovered K float counterexample |
| Partial-correctness termination assumption | Recursive source calls | Legitimate for a partial-correctness theorem, but the length-1100 CPython `RecursionError` remains an excluded behavior |

### Final reasoning

Clean reconstruction and non-vacuity are positive evidence: the candidate did
not fake the reported `#Top`, and the submitted finite postconditions are
discriminating. They cannot substitute for Gate A real-program soundness.
The proof is body-insensitive to `solution.mpy`, so it proves a substituted
closed AST. Even that theorem is materially narrower than the requested
all-list contract, and the generated numeric model has a concrete
intended-domain mismatch with both Python implementations.

Accordingly, the candidate meets the decision boundary for
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
