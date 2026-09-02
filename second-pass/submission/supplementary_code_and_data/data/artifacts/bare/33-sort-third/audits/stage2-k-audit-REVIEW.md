# Independent adversarial review: 33-sort-third

The candidate reconstructs to a sound, non-vacuous reachability theorem about
the exact submitted program on finite lists of mathematical integers. It is not
a proof of the full source contract: the prompt annotates only `list` and does
not restrict element values to integers, while the formal syntax and all entry
claims admit only `VList(Ints)`. Ordinary string and float lists are terminating
source-contract inputs handled by both Python implementations but are not
expressible by the K theorem. The benchmark directs that this material
source-domain narrowing be classified as `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `legacy-selected-stage1` and
`GENERATED_SEMANTICS`. All records required for that layout are present as
regular readable files: `/run.json`, `/task.json`, `/generation-result.json`,
the invocation and metrics records, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, `usage.json`, and the structured trace. Historical
`runtime-metrics.json` was not recorded; the benchmark expressly says it is not
required for this legacy layout.

The parsed `/audit-campaign-lock.json` equals the `audit_campaign` block in
`/audit-input.json`, and its independent SHA-256 is the recorded
`ad5dfcc0...78d745`. The mounted run, task, result, invocation, metrics, usage,
prompt, output, last-message, canonical, trusted-prompt, and translator bytes
all match their recorded hashes. The sole trace file matches the hash recorded
by `/generation-result.json`; all 142 JSONL records parse. Independent pipeline
tree hashes also match the retained generation workspace digest and
`usage.json` trace digest. There are no symlinks below `/candidate` or
`/reference`.

The candidate `prompt.py` and `py2mpy.py` match their trusted mounted versions
byte-for-byte. `/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`; no hidden or inferred reference semantics was used.
Required candidate proof artifacts `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are present. The generation logs and
their prior `KPROVE_PASSED` assertion were inspected only as untrusted history.

Reproducible checks and hashes are in
`/audit-output/evidence/provenance_check.py` and
`/audit-output/evidence/01-provenance.log`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract says to return a list in which indices not divisible by
three retain their original values, while the subsequence at indices
`0, 3, 6, ...` is sorted and written back at those indices. The trusted
canonical implementation copies with `list(l)`, sorts `l[::3]`, assigns that
slice, and returns the copy.

The submitted implementation copies with `l[:]`, performs the same
stride-three sorted slice assignment, and returns the copy. Those two copy
forms are extensionally equivalent for the declared list input. Regeneration
with the trusted translator,

```text
python3 trusted_py2mpy.py solution.py | cmp - solution.mpy
```

exited 0, establishing byte identity with submitted `solution.mpy`.

The independent differential script exercised the two prompt examples, empty
and length-boundary lists, every length from 0 through 7 exhaustively over
`[-2,-1,0,1,2]`, equality/ordering branches, negative and large integers, and
500 seeded lists up to length 50. All 98,168 comparisons matched and neither
implementation mutated its input. This is finite fidelity evidence, not a
proof.

The source-domain probe additionally used:

- `["z", "kept-1", "kept-2", "a"]`, for which both implementations return
  `["a", "kept-1", "kept-2", "z"]`;
- `[3.5, 20.25, 10.75, -1.5, 8.0, 9.0, 2.25]`, for which both return
  `[-1.5, 20.25, 10.75, 2.25, 8.0, 9.0, 3.5]`.

These are ordinary comparable lists satisfying the stated source contract, not
exceptional or nonterminating inputs. Neither is representable by the formal
`VList(Ints)` input sort. Scripts and complete bounded results are in
`differential_test.py`, `domain_scope_witness.py`, and `02-fidelity.log`.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/33-sort-third`; no
candidate definition or cache was copied or reused. With K 7.1.293, the
following fresh builds both exited 0:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantics-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The unmodified positive spec then passed:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
#Top
EXIT: 0
```

Because the three candidate claims were unlabeled, the audit made a separate
copy differing only by inert claim labels and selected each one. The universal
claim and both example claims each independently printed `#Top` and exited 0.

Fresh LLVM execution covered empty, singleton, prompt, reverse-order,
equality, negative, and length-modulo-three cases. A separate 24-case K/Python
bridge run over lengths 0 through 11 reported no `krun` failure and no mismatch
against either Python implementation. Representative exact output includes:

```text
INPUT:  VList(5, 6, 3, 4, 8, 9, 2)
RESULT: VList(2, 6, 3, 4, 8, 9, 5)

INPUT:  VList(9, 0, -1, 8, 7, 6, 2, 5, 4, 1)
RESULT: VList(1, 0, -1, 2, 7, 6, 8, 5, 4, 9)
```

Exact commands, exits, bounded outputs, and the labeled audit spec are in
`03-reconstruction.log`, `k_semantics_differential.py`, and
`spec-audit-labeled.k`.

## 4. Adequacy and real-program pinning

The three entry claims state:

1. For every finite K sequence `IS:Ints`, execute the submitted function body
   on `VList(IS)` and return `contractResult(IS)`.
2. On `[5,6,3,4,8,9,2]`, return `[2,6,3,4,8,9,5]`.
3. On `[1,2,3]`, return `[1,2,3]`.

Each precondition is satisfiable. The first is witnessed by either ground
example (and by `.Ints` for the empty list); the latter two claims specify
their satisfying initial configurations directly. The initial result is `.K`,
as in the generated configuration.

`program_term_check.py` extracted every balanced `Module(...)` entry term,
removed only layout outside string literals, and compared it with regenerated
`solution.mpy`. All three constructor comparisons are true. Thus the claims
pin the exact function name, sole parameter, binding, three-statement body,
slice bound, builtin-call syntax, and return. They do not merely reference an
external source filename.

The universal destination constrains `<result>` to
`contractResult(IS)`, whose equation expands to:

```text
VList(replaceThirdInts(0 ; IS ; sortInts(thirds(IS))))
```

It is neither a free variable, implication, nor tautology. Ground substitution
with the second example gives exactly the K and Python result shown in stage 3.

A separate body-sensitivity claim removed the stride-three assignment from the
`Module(...)` term actually executed, retaining the original expected result.
It exited 1 with `WarnStuckClaimState`, exposing the unchanged input list in
`<result>`. This demonstrates dependence on the proved body rather than on an
external file. See `program_term_check.py`, `body-sensitivity-spec.k`, and
`04-pinning-and-sensitivity.log`.

The material adequacy failure is the entry sort itself: `IS:Ints` covers only
integer elements. The trusted prompt says `l: list`, gives no integer
precondition, and its sorting contract applies to the comparable string and
float witnesses from stage 2. Restricting all elements to mathematical
integers therefore excludes whole ordinary classes of source-contract inputs,
not merely implementation-specific edge behavior.

## 5. Rule-by-rule static soundness review

`/audit-output/evidence/rule_inventory.md` is the exhaustive inventory. It
enumerates every local source/runtime syntax declaration, configuration cell,
function attribute, semantic equation, and claim. In summary:

- `semantic.k` declares the exact AST fragment used by `solution.mpy`, integer
  sequences and values, ten `[function]` symbols, three state cells, and 26
  rules/equations.
- `verification.k` adds one `[function]`, `contractResult`, and one defining
  equation. `spec.k` has three claims.
- There are no local `total`, `functional`, `simplification`, `concrete`,
  `owise`, priority, opaque, or syntax-macro declarations.

Every constructor used by the regenerated program maps to both syntax and
behavior: module/function loading and parameter binding; name lookup; full and
stride-three slices; one-argument builtin sorting; name and slice assignment;
statement sequencing; return; integer extraction; insertion sort; and
stride-three replacement. The map is the only local-variable state; input is
preserved; result is written once. For the exact program, expressions are pure,
so the big-step equations preserve the material evaluation and control effects.

The helper cases are disjoint on their relevant domain. Empty/nonempty list
heads are disjoint; counter zero and `N >Int 0` are disjoint; and integer
`I <=Int J` versus `I >Int J` is disjoint and exhaustive. Each recursive list
equation descends on a finite list. `thirds` selects precisely indices
`0,3,6,...`; `sortInts` is ascending insertion sort; and
`replaceThirdInts` changes only those selected positions when supplied the
equal-length sorted selected subsequence. `contractResult` names that
mathematical construction and does not rewrite or bypass the program term.

The semantics is target-local rather than reusable Python semantics. In
particular, `Name("sorted")` selects the builtin syntactically rather than
modeling arbitrary shadowing, and the full slice erases allocation identity.
The exact submitted module does not shadow `sorted`; on integer elements its
subsequent whole-value map update preserves `l` and `<input>`, so omitted list
identity is unobservable. Unsupported syntax has no total/otherwise rule and
stays stuck. These are bounded modeling choices, not false-result witnesses for
an execution of the submitted program on the proved integer domain.

No local rule was found that enables a false conclusion for the exact submitted
program on an admitted `VList(Ints)` input. Accordingly, this review makes no
unsupported unsound-rule allegation. The failure is instead the separate,
concrete exclusion of valid non-integer source inputs.

## 6. Fresh non-vacuity test

`spec-vacuity-review.k` retains the exact submitted program term and the
satisfying input `VList(5,6,3,4,8,9,2)`, but deliberately changes the returned
list obligation to the false unsorted input. `kprove --dry-run` exited 0 and
emitted a valid `kore-exec` command, showing that the mutation built.

The actual proof exited 1 with `WarnStuckClaimState`. Its residual is the
meaningful unmet result obligation:

```text
<result>
  VList ( 2 , 6 , 3 , 4 , 8 , 9 , 5 , .Ints ) ~> .K
</result>
```

That is the correct computed result and does not unify with the mutated
destination `[5,6,3,4,8,9,2]`. This is proof discrimination, not a parser error,
timeout, or unrelated crash. The mutation and exact build/proof logs are in
`spec-vacuity-review.k` and `06-non-vacuity.log`.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following precise,
restricted statement:

> Under the candidate-generated K semantics, for every finite sequence of
> mathematical integers, executing the exact regenerated `sort_third` body from
> the initial three-cell configuration consumes its computation and places
> `replaceThirdInts(0; IS; sortInts(thirds(IS)))` in the result cell.

The trust and evidence ledger is:

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, LLVM/Haskell backends, reachability engine | All dynamic reconstruction | Ordinary toolchain trust; both fresh builds and independent claim runs succeeded. |
| K builtin mathematical `Int`, integer comparison/arithmetic, `Map`, and generated list infrastructure | Lookup, counters, insertion ordering, all claims | Acceptable low-level primitives. The integer arithmetic matches Python arbitrary-precision integers on the admitted domain. |
| Trusted CPython-AST translator | Real-program constructor identity | Byte identity was independently re-established; no candidate translator change is assumed. |
| Generated module/call/slice/assignment/return equations as a model of this source body | Connection from K execution to Python | Manually audited rule by rule and empirically bridged on boundary/representative integer inputs. There is no separately machine-checked CPython-to-K refinement theorem, so the Python connection remains a reviewed modeling boundary. |
| `thirds`, `sortInts`, and `replaceThirdInts` equations | Natural-language meaning of `contractResult` | Their index, ordering, preservation, disjointness, and descent properties follow by ordinary finite-list mathematics. The K entry proof executes these equations; the natural-language interpretation is an informal adequacy bridge supported by differential evidence, not replaced by it. |
| Builtin `sorted` binding and erased list-copy identity | Call result and non-mutation | Acceptable only for this exact unshadowed function over immutable integer elements; both input cells and Python inputs remain unchanged in tests. |
| Element domain `Ints` | Every K claim | Illegitimate as completion of the stated source contract. Comparable strings and floats are valid, terminating witnesses handled by both Python implementations but excluded from syntax and preconditions. |

Gate A (real-program soundness for the admitted integer model) passes: the body
is pinned and executed, the result is constrained, and both body sensitivity
and false-result mutations fail meaningfully. Gate C evidence is reproducible
and adequate for the limits claimed. Gate B fails because the formal input
domain materially narrows the source contract. Per the benchmark-specific
decision boundary, a sound-but-limited theorem caused by this narrowing is
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
