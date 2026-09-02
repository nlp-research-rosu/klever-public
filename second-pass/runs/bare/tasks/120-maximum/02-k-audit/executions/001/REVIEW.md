# Independent adversarial audit: HumanEval 120 `maximum`

The candidate contains a legitimate, freshly reconstructible
partial-correctness proof of the submitted generated program under its generated
K semantics. The proof is exact-program-pinned and result-constraining, the
semantics is sound for the intended finite integer-list domain, and a fresh
false result mutation is rejected for the expected logical reason.

The status is `CONCERNS / LEGIT`, rather than an unqualified pass, because the K
claim proves equality with a definitional sort-and-drop expression but does not
separately machine-check the theorem that this expression is the English
“maximum K” operation. That bridge is mathematically straightforward, supported
by a rule-by-rule audit and finite differential evidence, and does not enable a
false conclusion on the intended domain. A maximum-length K command-line test
also hit an external parser kill before semantic execution; this is recorded as
an infrastructure-limited test, not as a candidate failure.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` does not exist, as required for
`GENERATED_SEMANTICS`. There is therefore no hidden/supplied semantics baseline
to infer or compare. The candidate's generated `semantic.k` was audited on its
own merits.

All required candidate artifacts are regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, `prove.sh`, and the structured JSONL trace. The
trace parses as 133 JSON records. The source tree contains no candidate helper
K file beyond the three named K files.

The candidate prompt and translator are byte-identical to the trusted mounts:

| Artifact | Trusted/candidate SHA-256 | Result |
|---|---|---|
| `prompt.py` | `360323c0b48ab9ab91ecd91655e881eb66140b4822d73cc5e6e40c9e2ae6ab82` | identical |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

`run-input.json` identifies problem `120-maximum`, condition `bare`, and no
supplied semantics; its recorded prompt/translator hashes match the trusted
files. `metrics.json`, the prose report, generation log, and trace claim a
successful generation and `#Top`, but those claims were not trusted.

The additional candidate `semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/` trees are derived extras. They were catalogued and deliberately
excluded from scratch. No missing, changed, mistyped, or symlinked required
source artifact was found.

Evidence:

- [`01_integrity.sh`](evidence/01_integrity.sh) and
  [`01_integrity.log`](evidence/01_integrity.log) contain the exact checks,
  hashes, JSON validation, untrusted-claim extract, and exit statuses.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a list `arr` of length 1 through 1000 containing integers in
`[-1000,1000]`, and integer `k` satisfying `0 <= k <= len(arr)`, return a
nondecreasing list of length `k` containing the `k` largest input values with
multiplicity. In particular, `k=0` returns `[]`.

The trusted canonical implementation returns early for `k=0`; otherwise it
sorts `arr` in place and returns its last `k` entries. The candidate is:

```python
def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]
```

For the stated domain, the candidate computes the same return value: after
ascending sorting, `len(arr)-k` is in `[0,len(arr)]`, and the suffix from that
index consists of exactly the largest `k` values in ascending order. The
candidate does not mutate the caller's list, whereas the canonical function
sorts it for `k>0`. The prompt specifies the return value, not input mutation,
so this is a non-material algorithm/side-effect difference.

Regeneration used the trusted translator directly:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/120-maximum-audit/src/solution.py \
  > /tmp/audit-work/120-maximum-audit/src/regenerated-solution.mpy
cmp -s /tmp/audit-work/120-maximum-audit/src/regenerated-solution.mpy \
  /candidate/solution.mpy
```

Both commands exited 0. The regenerated and submitted `.mpy` files have the
same SHA-256:
`9940ac33863a39ff689beea3a0e5b38b93312bac216254cb9a2dbd667385b021`.

The independent differential harness imports `/reference/canonical.py` and the
scratch-copy `solution.py` under distinct module names. It exercised:

- all three documented examples;
- the requested empty case (`[]`, `k=0`, explicitly outside the prompt's
  `len>=1` domain);
- `k=0`, `k=1`, `k=n-1`, and `k=n` branch/slice boundaries;
- one-element lists, duplicates, `-1000`/`1000`, and length 1000;
- 500 deterministic generated cases (seed 120).

There were zero return mismatches over 519 cases: 518 intended-domain cases
plus the empty case. It recorded 442 argument-side-effect differences, all from
the canonical in-place sort and none affecting the specified return.

Evidence:

- [`02_differential_test.py`](evidence/02_differential_test.py)
- [`02_fidelity_and_differential.log`](evidence/02_fidelity_and_differential.log)
- [`02_differential_results.json`](evidence/02_differential_results.json), which
  preserves every input and both outputs

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/120-maximum-audit/src`. No candidate definition, compiled
cache, or generated backend artifact was copied or referenced. K version
`v7.1.293` was independently reported by `kompile`, `kprove`, and `krun`.

Fresh builds used distinct scratch output directories:

```text
kompile semantic.k --backend llvm \
  --main-module MAXIMUM --syntax-module MAXIMUM-SYNTAX \
  --output-definition concrete-kompiled

kompile verification.k --backend haskell \
  --main-module MAXIMUM-VERIFICATION --syntax-module MAXIMUM-SYNTAX \
  --output-definition proof-kompiled
```

Both builds exited 0. `spec.k` contains exactly one positive target claim. It
was independently run as:

```text
kprove spec.k \
  --definition proof-kompiled \
  --spec-module MAXIMUM-SPEC
```

The command exited 0 and printed exactly the required success signal `#Top`.

The freshly built LLVM semantics then executed the actual regenerated
`solution.mpy`. Eleven bounded concrete cases covered all examples, empty input,
`k=0`, `k=1`, `k=n`, duplicates, integer extrema, and representative
length-100 inputs at both `k` endpoints. Every `krun` exited 0, the harness
parsed the final `<out>` cell, and all eleven results equaled both the trusted
canonical and generated Python results.

Two additional length-1000 `-cARGS` attempts exited 137 because the Java-based
K argument parser was killed before it produced a parsed configuration. The
diagnostic identifies `kparse`, not a stuck or incorrect semantic execution.
The failed attempt is preserved separately and is not used as evidence against
the candidate. Length-1000 return behavior remains covered by the independent
Python differential suite; this finite evidence does not replace the proof.

Evidence:

- [`03_rebuild.sh`](evidence/03_rebuild.sh) and
  [`03_rebuild.log`](evidence/03_rebuild.log)
- [`03_k_concrete_compare.py`](evidence/03_k_concrete_compare.py),
  [`03_k_concrete_compare.log`](evidence/03_k_concrete_compare.log), and
  [`03_k_concrete_results.json`](evidence/03_k_concrete_results.json)
- Infrastructure-limited attempt:
  [`03_k_concrete_compare_max_length_attempt.log`](evidence/03_k_concrete_compare_max_length_attempt.log)
  and
  [`03_k_concrete_results_max_length_attempt.json`](evidence/03_k_concrete_results_max_length_attempt.json)

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The sole claim starts with:

- `<k>` containing the exact submitted `Module(FuncDef(...Return(...)))`
  followed by `boot`;
- `<args>` containing exactly `listVal(L)` and `intVal(K)`;
- an empty `<env>` and `noResult` in `<out>`;
- the numeric condition `0 <= K <= size(L)`.

The formal precondition omits the prompt's length 1..1000 and element
`[-1000,1000]` bounds, and it has no explicit predicate that every K `ListItem`
is an `Int`. For represented finite integer lists this is a broader theorem,
not a strengthened precondition that excludes intended inputs. The bridge from
Python `list[int]` to K `List` of `Int` is stated in Stage 7.

### Postcondition in plain language

The program must consume `<k>` to `.K`, bind `arr` and `k` in `<env>`, preserve
the arguments, and change `<out>` from `noResult` to:

```text
listVal(maximumSpec(L,K))
```

`maximumSpec` is not fresh or opaque. Its only equation expands it to:

```text
dropInts(size(L) -Int K, sortInts(L))
```

Thus the returned value is an equality-constrained function of the actual
inputs; it is not a free variable, tautology, existential oracle, or one-way
implication.

After whitespace normalization, the complete regenerated `solution.mpy` term
occurs verbatim in the entry claim. The trusted regeneration is byte-identical
to the submitted `.mpy`, so the claim pins the real generated program rather
than a replacement. The boot rule extracts and executes the matched `BODY`;
there is no helper/loop claim and no proof rule that skips it.

A concrete satisfying state is
`L = [-3,-4,5]`, `K = 3`: `0 <= 3 <= size(L)=3`.
Substitution gives:

```text
sortInts(L)                 = [-4,-3,5]
size(L)-K                   = 0
dropInts(0,[-4,-3,5])       = [-4,-3,5]
maximumSpec(L,K)            = [-4,-3,5]
canonical.maximum(L,K)      = [-4,-3,5]
generated.maximum(L,K)      = [-4,-3,5]
```

Four additional satisfying substitutions, including `K=0`, duplicates, and
integer extrema, also agree.

Evidence:

- [`04_pinning_and_ground.py`](evidence/04_pinning_and_ground.py)
- [`04_pinning_and_ground.log`](evidence/04_pinning_and_ground.log)

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved in
[`05_rule_inventory.md`](evidence/05_rule_inventory.md), with the source
declaration extract in
[`05_source_inventory_extract.log`](evidence/05_source_inventory_extract.log).
The complete inventory comprises:

- 12 grouped local declarations covering every alternative for `Module`,
  `Params`, `Stmt`, `Expr`, `Bound`, `Val`, the configuration, continuations,
  eight semantic function symbols, and `maximumSpec`;
- 19 semantic rules in `semantic.k`;
- one definitional proof rule in `verification.k`;
- one reachability claim in `spec.k`.

There are ten `[symbol(...)]` constructor alternatives and nine `[function]`
symbols. There are no local `total`, `functional`, opaque, priority,
simplification, concrete, strictness, macro, or anywhere declarations/rules.
There is no generated helper K file.

### Exhaustive rule decisions

| Rules | Decision |
|---|---|
| `semantic.k:45-48` entry/boot | Matches the exact function name, parameter names, body, and two typed arguments; binds the empty environment and executes `BODY`. Sound direct-entry model, not a body bypass. |
| `semantic.k:50-54` return/finish | Evaluates the actual expression, consumes control, and writes only `<out>` while preserving args/env. Sound for the single pure return. |
| `semantic.k:57` name lookup | Retrieves the unique K-map binding; sound. |
| `semantic.k:58-65` `sorted`, `len`, subtraction, suffix slice | Constructor/name patterns are disjoint. They model exactly the used unshadowed built-ins/operators. All operands are pure; the claim makes the slice start in range. Sound on intended integer lists. |
| `semantic.k:71-74` typed wrappers | Directly and truthfully connect list/int values to sort, size, subtraction, and prefix-drop helpers. |
| `semantic.k:79-81` `sortInts` | Empty base plus structural recursion. With insertion rules, ordinary induction gives an ascending permutation. |
| `semantic.k:83-89` `insertInt` | Empty base; guarded cases `I<=J` and `I>J` are disjoint and exhaustive over mathematical K integers. Both preserve order and multiplicity. |
| `semantic.k:91-94` `dropInts` | Zero base and positive structural step truthfully remove a prefix. It is deliberately partial for negative/out-of-range/non-integer-list cases; no `[total]` claim exists and intended entry states do not reach those cases. |
| `verification.k:9-10` `maximumSpec` | Definitional summary, not an operational bridge. Sorting ascending and dropping `n-K` leaves a sorted length-`K` suffix; by sorted order, every removed value is no greater than every retained value. Truthful for `0<=K<=n`. |
| `spec.k:6-23` entry claim | Exact-program-pinned, satisfiable, consumes `<k>`, and equality-constrains the result. |

Construct coverage is complete:
`Module/FuncDef/Params` use boot; `Return` uses return/finish;
`Subscript/Slice/NoBound` use suffix/drop; `Call/Name("sorted")` uses
sort/insertion; `Call/Name("len")` uses list size; and `BinOp("-")/Name("k")`
uses integer subtraction and environment lookup. No used construct falls
through to a catch-all or fabricated result.

Configuration and control are adequate for this submitted program:

- The environment contains only `arr` and `k`; the source has no rebinding of
  `sorted` or `len`.
- The generated Python uses `sorted`, not `arr.sort`, and slicing returns a new
  list. Preserving the K environment's original `arr` is therefore faithful for
  the observable result. Allocation identity is not part of the contract.
- Valid integer-list inputs cannot raise from the modeled operations; omitted
  general Python exceptions and arbitrary rebinding are unused constructs.
- Recursive helpers descend on finite lists. No overlap, guard hole on a
  reachable intended case, priority interaction, or unjustified totalization
  was found.

No rule is labeled unsound, so this review makes no unsupported unsoundness
claim and needs no false-conclusion witness for Stage 5. The narrower evidence
gaps are explicit: the representation predicate and prompt bounds are not
formalized; the English maximum characterization is not a separate K lemma;
and one maximum-length concrete K encoding could not pass the external parser.
None permits a false conclusion on the intended domain.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or trusted. A fresh scratch mutation
changed the result-bearing postcondition from:

```text
listVal(maximumSpec(L,K))
```

to the deliberately false:

```text
listVal(maximumSpec(L,K) ListItem(0))
```

The satisfying witness `L=[1]`, `K=1` has actual/claimed result `[1]` and
mutated result `[1,0]`.

The mutation first built successfully:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module MAXIMUM-SPEC-VACUITY --dry-run
```

Dry-run exit status: 0.

The actual negative proof command was:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module MAXIMUM-SPEC-VACUITY
```

It exited 1 and produced `WarnStuckClaimState`. The residual says the
destination unifies but the implication check fails, and explicitly exposes
the unmet equality between the real
`dropInts(size(L)-K,sortInts(L))` and that same list with `ListItem(0)`
appended. This is the expected result-obligation failure, not a parser error,
missing import, timeout, unreachable mutation, or unrelated crash.

Evidence:

- [`06_spec-vacuity.k`](evidence/06_spec-vacuity.k)
- [`06_non_vacuity.log`](evidence/06_non_vacuity.log)

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the source-defined `MAXIMUM` semantics, for every initial K configuration
matching the exact regenerated submitted module, exact two-argument entry
shape, empty environment/output, and `0 <= K <= size(L)`, execution reaches
`.K` with:

```text
out = listVal(dropInts(size(L)-K, sortInts(L)))
```

and with `arr`/`k` bound to the initial values. For intended finite lists of K
integers, the audited recursive equations terminate, `sortInts` is ascending
insertion sort, and `dropInts(size(L)-K,...)` is the sorted maximum-`K` suffix.
This is a partial-correctness result under the generated semantics; the fresh
mutation demonstrates that its result equality is discriminating.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler/prover/backends and reachability kernel | All build, execution, and proof results | Necessary low-level tool trust; rebuilt from source with both LLVM and Haskell paths. |
| Standard K `INT`, `BOOL`, `STRING`, `LIST`, and `MAP` domains, including mathematical integer order/subtraction, list `size`, and map matching | Guards, length, sorting, dropping, environment | Acceptable standard primitive boundary. There is no candidate-defined opaque primitive. |
| Trusted `/reference/py2mpy.py` transliteration | Python-to-`.mpy` identity | Authorized trusted input; candidate copy matches it and regeneration is byte-identical. |
| Python `list[int]` represented as K `ListItem(Int)...`, with two args represented by `listVal`/`intVal` | Intent interpretation of the K theorem | Simple informal representation bridge. The spec omits an explicit element-type predicate, but every intended input has this representation. |
| `sorted`, `len`, subtraction, and suffix slicing equations in generated semantics | Actual program result | Not blindly assumed: exhaustively audited for the used pure, valid-input cases and concretely compared. General Python shadowing, exceptions, and object identity are excluded. |
| Inductive fact that R13-R17 sort ascending and R18-R19 drop a prefix | Meaning of `maximumSpec` | Ordinary mathematical audit, not a separate machine-checked K theorem. This is the principal reason for `CONCERNS`. |
| Finite Python differential suite (519 cases) and K concrete suite (11 completed cases) | Empirical support for program/semantics/intent bridges | Reproducible supporting evidence only; not treated as a universal proof. |
| Canonical input mutation versus candidate non-mutation | Comparison with reference | Excluded from the theorem because the prompt requests only a returned list. The generated K state matches the candidate's non-mutating expression. |
| Maximum-length K CLI parser kill | Concrete evidence breadth only | Infrastructure limitation before semantic execution. It neither establishes nor refutes candidate correctness and does not affect the fresh symbolic proof. |

There are no loop invariants, auxiliary reachability claims, proof-local
operational bridges, opaque symbols, unconstrained fresh values, priorities,
totality assertions, or simplification lemmas. `maximumSpec` is the sole
proof-local function, has one explicit truthful equation, and influences only
the equality-constrained final output.

### Decision

- Real-program soundness: pass. The actual generated body executes under
  audited semantics, the claim is pinned and constraining, fresh `#Top` is
  reproduced, and the false result mutation is rejected.
- Intent adequacy: legitimate with a documented limitation. Sort-then-drop is
  the requested maximum-`K` result on the intended domain, but that English
  characterization and the input representation are audited informally rather
  than encoded as separate K theorems/predicates.
- Trust/evidence auditability: pass with the maximum-length parser limitation
  disclosed. Exact scripts, commands, statuses, inputs, results, mutation, and
  bounded logs are preserved under `evidence/`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
