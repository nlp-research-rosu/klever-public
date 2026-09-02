# Independent adversarial review: HumanEval 120 `maximum`

## Executive finding

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program.  A fresh Haskell proof build closes the only
positive claim with exit 0 and `#Top`; the trusted translator regenerates the
submitted `solution.mpy` byte-for-byte; the claim's executed module is
constructor-identical to that term; a mutation of the executed body and a
separate false-postcondition mutation are both rejected for the expected result
obligation.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
formal postcondition names the requested result by transparently reusing the
same `sortInts` and `dropInts` helpers that give meaning to `sorted` and slicing
in the generated semantics.  The fact that these equations implement ascending
sorting and select exactly the largest `K` elements is readily justified by
structural induction and is strongly supported by independent tests, but it is
not stated and machine-checked as a separate sortedness/multiset/top-`K`
theorem.  This is a non-fatal informal intent bridge, not an oracle or an
execution bypass: all defining equations are visible, terminating on the
intended domain, and sound.

Exact commands and their evidence-log mapping are in
`/audit-output/evidence/COMMANDS.md`.

## 1. Input and provenance integrity

### Layout and mode

`/audit-input.json` declares:

- problem `120-maximum`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- complete input provenance; and
- container paths for every mounted input.

I used only those container paths.  `/reference/reference-semantics` does not
exist, as required in generated-semantics mode.  I did not seek or use a hidden
reference semantics.

The required launcher records are all readable real files/directories:
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured `codex-trace/` tree.  I also inspected the
present legacy records `legacy-metrics.json` and `legacy-run-input.json`.
Historical `runtime-metrics.json` is absent, which is permitted for this
declared legacy-selected layout.

The structured trace contains 133 JSON records and parses with zero errors.
The generation output, trace, prior `#Top`, and final report were treated only
as untrusted historical claims.  See
`evidence/generation_trace_summary.{py,log}`.

### Campaign and hash checks

The JSON campaign block in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`.  The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher record.

Independent hashes equal the launcher-recorded hashes for the run manifest,
task manifest, stage-one result and invocation, metrics, usage, generation
prompt/output/last message, trusted canonical, trusted prompt, trusted
translator, candidate prompt, and candidate translator.  In particular:

- candidate and trusted prompt:
  `360323c0b48ab9ab91ecd91655e881eb66140b4822d73cc5e6e40c9e2ae6ab82`;
- candidate and trusted translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- canonical:
  `e67c0c10b177f85c33e5546557ee3afdf9127a58a56af8663c2ee1b7e183af1f`;
- trace JSONL:
  `406735740478d07046c5a5f05c48bc43fc9ed0157bc41cfbf5f7057bc403441a`.

I recursively enumerated type, mode, relative path, and per-file hash for the
candidate, references, and generation evidence.  There are no symlinks or
unsupported entries.  The independent legacy pipeline tree algorithm also
reproduces the retained candidate workspace digest
`683865c9387bc7544dd63407ce88c13f33d5ee8d0b192bbcd77794155fef0db8`
and trace digest
`8cc117c9299fcdb57ac492fb09df62588404cf8167533f6d6d8d36e3525fe44e`.
See `evidence/stage1_integrity.{py,log}` and
`evidence/pipeline_tree_hash.{py,log}`.

All required proof artifacts are present as regular candidate files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`.  The candidate contains a Python bytecode cache, but no
candidate-built K definition was copied or reused.  Only source artifacts were
copied to `/tmp/audit-work/120-maximum`; the copy and hashes are recorded in
`evidence/scratch_copy.log`.

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From the trusted prompt and canonical implementation, the intended domain is:

- `arr` is a list of length 1 through 1000;
- every element is an integer from -1000 through 1000; and
- `k` is an integer satisfying `0 <= k <= len(arr)`.

The requested return value is an ascending list of length `k` containing the
`k` largest values of `arr`, preserving multiplicities.  Although the prose
once calls `k` positive, the explicit bound and canonical `k == 0` branch make
zero part of the contract.

The generated implementation is:

```python
def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]
```

For `k` in range, sorting all values and taking the suffix beginning at
`len(arr)-k` returns exactly the requested values.  Unlike the canonical
implementation, it does not mutate `arr`; the contract constrains only the
returned list.

### Trusted regeneration

Running the trusted `/reference/py2mpy.py` against the scratch `solution.py`
produces SHA-256
`9940ac33863a39ff689beea3a0e5b38b93312bac216254cb9a2dbd667385b021`,
identical to the submitted `solution.mpy`; `cmp` exits 0.  See
`evidence/translator_regeneration.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical and
generated entry points.  It checks:

- all three documented examples;
- minimum and maximum length, element bounds, duplicates, `k=0`, `k=1`, and
  `k=len(arr)`;
- the empty-list/zero-`k` extension outside the documented length bound;
- every array of lengths 1 through 5 over
  `{-1000,-1,0,1,1000}`, for every permitted `k` (22,460 cases); and
- 500 deterministic generated cases of lengths 1 through 1000.

There are 22,972 total calls and zero return-value mismatches.  The complete
deterministic input description hashes to
`4ebc2bb65502f83511a7681565b1d5f4e291dd04f7fe5383ef904ec7f69fdda7`.
There are 18,008 post-call input-state differences because the canonical sorts
its argument in place while the generated implementation uses `sorted`; this
is recorded, not hidden, and is outside the specified return-value behavior.
See `evidence/differential_test.log`.

## 3. Clean proof reconstruction

The installed independently available K tools report version 7.1.293, matching
the campaign lock.  `kup` is absent, but `kompile`, `krun`, and `kprove` are
available and operational; see `evidence/tool_versions.log`.

From the source-only scratch copy I built:

1. an LLVM concrete definition from `semantic.k` as
   `concrete-kompiled`; and
2. a Haskell proof definition from `verification.k` as
   `verification-kompiled`.

Both builds exit 0 (`evidence/kompile_concrete.log` and
`evidence/kompile_proof.log`).  No candidate definition or cache was reused.

`spec.k` contains exactly one positive target claim.  Independently running

```text
kprove spec.k --definition verification-kompiled --spec-module MAXIMUM-SPEC
```

exits 0 and prints exactly `#Top`; see `evidence/kprove_positive.log`.

### Generated-semantics execution

The rebuilt LLVM semantics was run on the three examples, `k=0`,
`k=len(arr)`, a singleton, both element bounds and duplicates, and a
100-element case.  Every final K `<out>` value equals both generated Python
execution and an independently written `sorted`/suffix oracle.  The exact
commands, output hashes, parsed results, and zero mismatch count are in
`evidence/semantic_differential.{py,log}`.

A direct `-cARGS` parse of a varied 1,000-element literal was killed with exit
137 in K's argument parser before semantic execution.  This is preserved in
`evidence/semantic_differential_attempt1.{py,log}` and is not treated as a
candidate defect.  To exercise the actual candidate body at the length
boundary without that parser expansion, I compiled the reviewer-authored
`evidence/length_boundary_harness.k`.  Its only setup function constructs
1,000 zeros, then places the exact candidate body and `k=3` into the ordinary
candidate configuration.  The run exits 0, retains an array of length 1,000,
and returns `[0,0,0]`, equal to Python.  See
`evidence/kompile_length_boundary.log` and
`evidence/run_length_boundary.log`.  An initial harness syntax-module mistake
is also preserved in the `*_attempt1.log` files.

## 4. Adequacy and real-program pinning

### Plain-language entry claim

The sole claim starts with:

- the exact module containing a function named `maximum`;
- formal parameters named `arr` and `k`;
- the submitted return-expression body;
- concrete entry arguments `listVal(L)` and `intVal(K)`;
- an empty environment; and
- no prior result.

Its precondition is `0 <= K <= size(L)`.

Its destination consumes the computation, binds `arr` and `k` in the
environment, and sets the output to:

```text
listVal(maximumSpec(L,K))
```

where the transparent definition is:

```text
maximumSpec(L,K) = dropInts(size(L)-K, sortInts(L))
```

Thus the result is not a fresh variable, opaque oracle, implication-only
condition, or unconstrained value.  On intended integer lists it is exactly the
ascending suffix of length `K`.

The formal precondition is broader than the source contract: it does not impose
the source length/value bounds and admits the empty list.  It therefore does
not materially narrow the source domain.  Non-integer K-list elements are also
syntactically admitted, although helper reduction is partial on them; every
source-contract input consists of integers and is fully covered.

### Mechanical program identity

After trusted regeneration, `evidence/program_pinning.py` tokenizes the
submitted module and the program term before `~> boot` in the claim.  Both have
63 constructor tokens and the identical digest
`56eab54aaec8218b744722c81c2af61eac70335b126f0540c54a2f14c7eb8f9b`.
The constructor-token sequences are equal.  There is no omitted helper,
typing-only import, or normalization bridge.

The `boot` rule matches the exact function binding and parameters, installs
the two supplied entry arguments, and executes `BODY`.  The body then evaluates
the actual `sorted`, `len`, subtraction, and slice constructors before the
return is installed in `<out>`.  There are no source loops or helper calls and
therefore no helper/loop claims to pin.

### Satisfying states and substitution

`evidence/claim_witness.py` records three satisfying states.  For example,
`L=[-3,-4,5]`, `K=2` satisfies the precondition and substitutes into the formal
result as `[-3,5]`; both Python implementations return `[-3,5]`.  The witnesses
`L=[5], K=1` and `L=[7,-1], K=0` similarly agree.

### Body sensitivity

`evidence/spec-body-mutation.k` changes the program term actually executed by
the claim: the slice start becomes `len(arr)-len(arr)`, while the original
postcondition is retained.  Its dry run exits 0, so the mutation builds.  Its
proof exits 1 with `WarnStuckClaimState`; the residual compares
`dropInts(size(L)-size(L),sortInts(L))` with
`dropInts(size(L)-K,sortInts(L))`.  This demonstrates sensitivity to the
submitted body rather than to an external source filename.

## 5. Rule-by-rule static soundness review

There are no generated helper K files besides `semantic.k`, `verification.k`,
and the claim module.  The line-numbered source and mechanical declaration
search are preserved in `evidence/source_inventory.log`.

### Complete local declaration inventory

`semantic.k` declares these syntax productions:

- `Module`: `Module(Stmt)`;
- `Params`: exactly two string parameters;
- `Stmt`: `FuncDef(String,Params,Stmt)` and `Return(Expr)`;
- `Expr`: `Name(String)`, `Call(Expr,Expr)`,
  `BinOp(String,Expr,Expr)`, `Subscript(Expr,Expr)`, and
  `Slice(Bound,Bound,Bound)`;
- `Bound`: injection from `Expr` and `NoBound`;
- `Val`: `intVal(Int)`, `listVal(List)`, and `noResult`;
- `KItem`: `boot` and `finish(Val)`;
- function `eval(Expr,Map)`;
- functions `sortedVal(Val)`, `lengthVal(Val)`,
  `subtractVal(Val,Val)`, and `suffixVal(Val,Val)`; and
- list functions `sortInts(List)`, `insertInt(Int,List)`, and
  `dropInts(Int,List)`.

`verification.k` adds the one function `maximumSpec(List,Int)`.
`Module`, `Params`, the AST constructors, value constructors, and control
markers are ordinary data/control symbols.  There are no fresh result symbols
or uninterpreted result-bearing oracles.

There are no local `[total]` declarations, `[functional]` declarations,
simplification rules, concrete rules, priority rules, `owise` rules, or opaque
proof symbols.  The listed helpers have `[function]`; their coverage,
overlap, and descent are assessed below rather than inferred from that
attribute.

The configuration has exactly the needed cells:

- `<k>` for the translated module and computation;
- `<args>` for the two entry values;
- `<env>` for local bindings; and
- `<out>` for the returned value.

No rule needs heap, I/O, exception, or call-stack state for this capture-free,
single-return, pure expression.  Python object identity/allocation is not
represented, but it is not observable in the requested returned integer-list
value.

### Construct coverage

Every constructor in `solution.mpy` is declared and modeled:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` / `FuncDef` / `Params` | Exact entry `boot` rule |
| `Return` | Return rule followed by `finish` |
| `Name("arr")`, `Name("k")` | Map lookup |
| `Name("sorted")`, `Name("len")` in calls | Exact built-in call equations |
| `Call` | The two call equations used by the body |
| `BinOp("-")` | Integer subtraction equation |
| `Subscript` + lower-only `Slice` + `NoBound` | Suffix equation |

No submitted construct is silently unmodeled or replaced by a fabricated
value.

### Complete rule inventory and judgments

| Rule | Role and static judgment |
|---|---|
| S1, `semantic.k:45` | Exact entry rule.  It matches only `maximum(arr,k)` with the submitted two-parameter binding, reads exactly two value arguments, preserves any K frame, installs distinct map bindings, and executes `BODY`.  It is a sound entry-call harness for this capture-free function. |
| S2, `semantic.k:50` | Evaluates the return expression under the current environment and transfers the value to `finish`.  The actual expression is pure and exception-free on intended inputs, so collapsing expression evaluation into `eval` preserves order-observable behavior. |
| S3, `semantic.k:53` | Consumes `finish(V)` only when `<out>` is `noResult`, writing exactly `V`.  No control suffix is discarded. |
| S4, `semantic.k:57` | Name lookup selects the unique map item with key `X`.  Actual environments contain distinct `"arr"` and `"k"` keys. |
| S5, `semantic.k:58` | `sorted(E)` first obtains `eval(E,RHO)` and then applies `sortedVal`.  The actual module does not shadow or rebind Python's `sorted`; binding selection is exact for this program. |
| S6, `semantic.k:60` | Same analysis for the standard `len` binding. |
| S7, `semantic.k:62` | `BinOp("-")` evaluates both operands and applies integer subtraction.  Python and K integers are unbounded here; both operands are pure, so the absence of an observable sequencing cell is harmless. |
| S8, `semantic.k:64` | Models exactly a lower-bound-only slice.  It evaluates the base and start and calls `suffixVal`; this is the only submitted subscript shape. |
| S9, `semantic.k:71` | `sortedVal(listVal(L))` returns `listVal(sortInts(L))`.  For integer lists, S13–S17 are ordinary insertion sort; a new list value is produced and the environment's `arr` term is unchanged. |
| S10, `semantic.k:72` | `lengthVal` returns K List `size`, equal to Python list length on represented lists. |
| S11, `semantic.k:73` | Exact unbounded integer subtraction. |
| S12, `semantic.k:74` | `suffixVal` delegates to `dropInts(N,L)`.  The entry precondition makes the actual start `N=size(L)-K` satisfy `0<=N<=size(L)`, exactly the Python slice regime modeled by S18–S19.  Negative or too-large starts are partial/stuck rather than assigned a false terminal value; those regimes cannot arise on the intended entry domain. |
| S13, `semantic.k:79` | Empty-list insertion-sort base case. |
| S14, `semantic.k:80` | Recurses on the strict tail and inserts the head.  Together with S15–S17, structural induction gives an ascending permutation. |
| S15, `semantic.k:83` | Inserts into the empty list. |
| S16, `semantic.k:84` | If `I<=J`, places `I` before the sorted list headed by `J`. |
| S17, `semantic.k:87` | If `I>J`, preserves `J` and recursively inserts into the strict tail.  The guards of S16/S17 are disjoint and exhaustive for K integers; recursion descends. |
| S18, `semantic.k:91` | Dropping zero elements returns the list unchanged. |
| S19, `semantic.k:92` | For positive `N`, removes one integer head and recurses with `N-1`.  It terminates and is complete whenever `0<N<=size(L)`, exactly the actual use.  Its guard does not overlap S18. |
| V1, `verification.k:9` | Transparent definitional summary: `maximumSpec(L,K)` rewrites to `dropInts(size(L)-K,sortInts(L))`.  It has one unguarded, nonrecursive, nonoverlapping equation and no opaque value.  It does not rewrite a program term or bypass execution. |
| C1, `spec.k:6` | The only reachability claim.  It executes the exact submitted module and constrains all relevant destination cells and the returned value as described in Stage 4. |

Function-equation overlaps are constructor-disjoint except for the deliberately
paired insertion guards, which are disjoint and exhaustive.  Map lookup is
unique on well-formed K Maps.  All recursive calls descend on a list tail or a
positive counter.  There is no rule priority that preempts another behavior.

The direct-style `eval` function does not model general Python effects,
exceptions, arbitrary callable bindings, negative/out-of-range slicing, or
non-integer ordering.  Those are language-coverage limits, not false rules on
this program's stated input domain.  The body has no effects between operand
evaluations, the built-ins are not rebound, and `0<=K<=size(L)` keeps slicing
inside the modeled range.

No rule was found that yields a false conclusion on an intended input, encodes
an unconstrained task-answer oracle, or skips a material operation.  Therefore
there is no unsound-rule witness to report.  The narrower evidence limitation
is V1's summary-to-natural-language bridge: its equation visibly denotes the
correct sorted suffix, but the candidate has no separate K predicates/theorem
for sortedness, multiplicity preservation, and maximality.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact.  The fresh
`evidence/spec-vacuity-fresh.k` keeps the original program and precondition but
changes the result-constraining destination to `listVal(.List)`.  This is false
for the satisfying witness `L=[5], K=1`, for which both Python implementations
and the original formal result are `[5]`.

The mutation dry run exits 0, establishing that it parses and builds against
the fresh proof definition.  The proof exits 1 with `WarnStuckClaimState`.
The residual explicitly contains the unmet equality:

```text
.List #Equals dropInts(size(L) -Int K, sortInts(L))
```

This is the expected reachable result obligation, not a parser failure,
missing import, timeout, or unrelated crash.  Evidence:
`evidence/vacuity_dry_run.log`, `evidence/vacuity_proof.log`, and the mutation
source itself.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the rebuilt definition, for every K `List` term `L` and K integer `K`
with `0<=K<=size(L)`, starting the exact submitted module with entry arguments
`listVal(L)` and `intVal(K)`, an empty environment, and `noResult` reaches a
consumed computation with:

- `arr` bound to `listVal(L)`;
- `k` bound to `intVal(K)`; and
- output
  `listVal(dropInts(size(L)-K,sortInts(L)))`.

For every finite source-contract integer list, the audited helper equations
terminate.  By the ordinary insertion-sort and prefix-drop argument, that
value is an ascending list containing exactly the largest `K` input values,
with duplicates.  The result is a partial-correctness theorem under the
generated model; it is not a proof of arbitrary Python behavior outside the
modeled subset.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and reachability logic | Build, execution, and `#Top` | Standard proof-tool trust boundary; version recorded, fresh builds used. |
| `domains.md` Int, Bool, String, List, Map, `size`, comparison, subtraction, and collection matching | Every semantic/helper rule | Standard K primitive boundary; operations are used in their ordinary typed domains. |
| Trusted `py2mpy.py` translation of the small source AST | Program identity | Launcher-trusted input; regenerated bytes and constructor comparison independently checked. |
| `boot` as entry-point invocation rather than general Python module/function-call machinery | Binding and control | Acceptable minimal generated semantics for this exact capture-free two-argument entry; exact binding/body/arguments are matched. |
| Generated equations for `sorted`, `len`, subtraction, and lower-only slicing | Program value | Audited rule by rule; independently compared with Python on normal and boundary cases.  No opaque value or operational shortcut remains. |
| Structural fact that S13–S17 are insertion sort and S18–S19 drop a prefix | Natural-language sorted/top-`K` meaning | Mathematically straightforward and empirically supported, but not separately machine-checked as sortedness/permutation/maximality predicates.  This is the principal non-fatal concern. |
| Trusted canonical Python implementation | Differential oracle only | Not used in the K proof.  Its return values agree in 22,972 cases; its in-place mutation is outside the return contract. |
| Finite concrete/differential evidence | Semantic and intent bridge support | Reproducible and broad but not a universal theorem; it does not substitute for the reconstructed K proof. |

Excluded behavior includes non-integer list elements, rebound built-ins,
exceptions, alias/object-identity observations, arbitrary slice bounds, and
out-of-contract calls.  None is material to the stated HumanEval domain.

### Gate and decision summary

- Real-program soundness: pass.  The program body executes under the audited
  generated semantics, the only proof extension is transparent and
  result-fixing, satisfying witnesses exist, and both body and postcondition
  mutations are rejected.
- Intent adequacy: the entire HumanEval domain is covered; there is no finite
  bound, fixed-size restriction, or substituted program.  The
  summary-to-top-`K` connection is an informal but sound mathematical bridge.
- Trust/evidence auditability: all assumptions and finite evidence are
  explicit and reproducible.  Candidate logs and prior `#Top` were not relied
  upon.

The informal summary-to-property theorem and necessarily finite
generated-semantics differential evidence warrant `CONCERNS`, but neither can
make a false result provable and neither narrows the required domain.  The proof
is therefore legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
