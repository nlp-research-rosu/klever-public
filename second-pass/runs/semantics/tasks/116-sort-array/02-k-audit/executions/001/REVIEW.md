# Independent adversarial review: 116-sort-array

This audit used the required `using-kit` and `validating-proof` procedures. It
treated every candidate artifact as untrusted, kept `/candidate` read-only,
rebuilt from source under `/tmp/audit-work/rebuild`, and preserved reviewer
scripts and bounded logs under `/audit-output/evidence`.

Decision: the proof is legitimate but has documented limitations. It
machine-checks exact execution of the submitted translated program to a
result-bearing term built from the supplied semantics' fixed opaque sorting
primitives. The candidate adds no execution shortcut or unconstrained oracle.
The meaning of those supplied primitives as stable Python sorting is,
nevertheless, a named external trust boundary supported by concrete execution
and finite differential tests rather than a universal K connection theorem.
The prompt examples and required provenance records also have auditability
problems. These limitations warrant `CONCERNS / LEGIT`, not failure.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. The trusted mount does
not contradict the rendered mode, so there is no infrastructure breach.

The recursive, no-dereference comparison found the candidate
`reference-semantics/` byte- and entry-identical to the trusted tree. There are
no candidate semantics symlinks, no missing entries, no additional entries,
and no type mismatches. This result only authenticates the supplied semantics;
it does not bless `verification.k`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` (both
SHA-256
`dc8d425f9133ada84c2a380d6cab8321aba622d443cee4d54bcc98c4859a2289`).
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` (both
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
All candidate source/proof artifacts used by this audit are regular files.

The required provenance records `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are missing. No structured generation
trace is present. They therefore supplied no evidence. `PROOF.md` is also
absent. The available `NOTES.md`, `prove.sh`, candidate tests, and Python bytecode
were read only as untrusted claims and were not used in place of reconstruction.
The extra `__pycache__/` directory was ignored.

Evidence:

- `evidence/integrity_audit.sh`
- `evidence/01-integrity.log` — command and exit 0, including every missing
  provenance record, hashes, types, symlink check, and recursive semantics diff

Scratch provenance: the audit copied candidate `solution.py`, `solution.mpy`,
`spec.k`, and `verification.k` plus trusted `prompt.py`, `canonical.py`,
`py2mpy.py`, and the trusted semantics tree to
`/tmp/audit-work/rebuild`. Candidate caches and compiled definitions were not
copied or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

The prose contract accepts a finite array of non-negative integers and orders
it by:

1. ascending number of `1` digits in each integer's binary representation; and
2. ascending decimal value when popcounts tie.

The trusted canonical implementation first applies ordinary ascending
`sorted(arr)` and then a stable keyed sort using
`bin(x)[2:].count("1")`. For non-negative integers, stripping the `"0b"` prefix
does not change the count. A stable second sort therefore implements the
lexicographic key `(popcount(x), x)`.

The displayed prompt examples are inconsistent with that prose and with the
canonical implementation. In particular:

- `[1,5,2,3,4]` is displayed as `[1,2,3,4,5]`, but the prose/canonical result
  is `[1,2,4,3,5]`.
- `[1,0,2,3,4]` is displayed as `[0,1,2,3,4]`, but the prose/canonical result
  is `[0,1,2,4,3]`.
- The negative example is outside the stated non-negative domain.

The submitted `solution.py` performs the same two sorts, with key
`bin(value).count("1")` for non-negative values. It assigns every negative key
0. Thus it agrees with the prose and canonical implementation throughout the
intended domain. Its negative branch intentionally matches the out-of-domain
negative example but differs materially from the canonical implementation on
some negative arrays. That divergence does not affect the explicitly stated
domain and remains recorded rather than hidden.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
python3 /reference/py2mpy.py /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`9f5d29667fdd1adb62505f439ed2d11bf8db7408b3adeb35eeea3123b760f362`;
the command exited 0. See `evidence/02-translation.log`.

### Independent differential execution

`evidence/differential_audit.py` imports the trusted canonical entry point and
the scratch candidate entry point independently. Its intended-domain suite
contains:

- ten named empty, singleton, zero/one boundary, duplicate, prompt,
  bit-boundary, tie, and large-integer cases;
- every list of length 0 through 4 over values 0 through 8 (7,381 cases); and
- 1,000 deterministic generated lists of length 0 through 29, including powers
  of two and random values through 80 bits.

All 8,391 intended-domain cases matched and neither implementation mutated its
input. The complete input set is
`evidence/differential-inputs.json` (SHA-256 recorded by the test as
`33dd9927adba2e1662e50e6f4740ade9b21dc90df83c4fdf63c9522aa6b1f934`).
The contradictory prompt results and four negative-domain observations are in
`evidence/differential-results.json`. Exact command, output, and exit 0 are in
`evidence/03-differential.log`.

This is finite evidence for implementation/canonical fidelity. It is not a
substitute for the K proof.

## 3. Clean proof reconstruction

The installed tools are K v7.1.337. Both definitions were rebuilt from clean
source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0; see `evidence/04-kompile-llvm.log`. The compiler reported
non-exhaustiveness warnings for several fixed, unused semantic functions
(`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`). None is reachable from
this submitted program. They are fixed supplied-semantics limitations, not
candidate rules.

```text
kompile verification.k --backend haskell \
  --main-module SORT-ARRAY-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0; see `evidence/05-kompile-haskell.log`. Its only warnings are unused
pattern variables in the fixed `strLt` rules.

The candidate's complete four-claim spec then closed:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SORT-ARRAY-SPEC
```

Output `#Top`, exit 0; see `evidence/06-kprove-all.log`.

Because the source claims are unlabeled, the reviewer also placed verbatim
copies in one-claim spec modules and ran each independently:

| Claim | Evidence | Result |
|---|---|---|
| exact module load | `spec-load-only.k`, `07b-kprove-load.log` | `#Top`, exit 0 |
| universal entry execution | `spec-entry-only.k`, `08-kprove-entry.log` | `#Top`, exit 0 |
| non-negative key execution | `spec-key-nonnegative-only.k`, `09-kprove-key-nonnegative.log` | `#Top`, exit 0 |
| negative key branch | `spec-key-negative-only.k`, `10-kprove-key-negative.log` | `#Top`, exit 0 |

`evidence/07-kprove-load.log` transparently records an initial reviewer harness
failure: the isolated spec searched for `verification.k` relative to the
evidence directory and exited 113. The corrected artifact names the scratch
source explicitly and closes in `07b-kprove-load.log`. This was a spec include
path mistake after the aggregate candidate proof had already closed, not a
candidate proof failure.

For a concrete cross-check, the reviewer translated
`evidence/concrete_audit.py` with the trusted translator and ran the result
against the fresh LLVM definition:

```text
krun /audit-output/evidence/concrete_audit.mpy \
  --definition runtime-kompiled
```

The final configuration has `.K`, `NoExc`, and exit code 0. Its heap visibly
contains the decimal pre-sorts and keyed results for empty, zero/one boundary,
prompt, binary-boundary, duplicate, and negative cases. The same assertions
exit 0 under CPython. See `11-concrete-translation.log`,
`12-krun-concrete.log`, and `13-python-concrete.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Loading claim (`spec.k:7`)**: starting from the fully pinned empty module
   state, loading the exact named module terminates with the binding
   `sort_array -> sortArrayClosure` in scope 0 and leaves the other cells
   unchanged.
2. **Entry claim (`spec.k:27`)**: for every finite `ValSeq` consisting only of
   non-negative K integers, calling the exact `sort_array` closure on that list
   returns `ref(1)`. It allocates at heap location 0 the decimal-sort summary
   `list(sortVS(VS))`, then at location 1 the keyed-sort summary
   `list(sortArraySpec(VS))`, and advances `heapLoc` to 2. Environment, scopes,
   stack, return state, exception state, and exit code are fully constrained.
3. **Non-negative key claim (`spec.k:54`)**: for every `N >= 0`, calling the
   exact key closure returns the count of ASCII `"1"` in the supplied binary
   representation `"0b" ++ binCodes(N)`, with every state cell restored.
4. **Negative key claim (`spec.k:79`)**: for every `N < 0`, the same exact key
   closure returns 0. This helper theorem is outside the main claim's input
   domain.

There is no loop or circularity claim.

### Pinning the submitted program

After expansion, `sortArrayModule`, `sortArrayBody`, `sortArrayLambda`,
`sortArrayClosure`, and `popcountKeyClosure` are the exact AST, function body,
lambda, closure, and module in the byte-verified submitted `solution.mpy`.
`sortArrayModule` is checked through real `#loadAll`; the entry claim calls the
exact resulting closure body directly. It does not replace the body with a
result summary. Ordinary supplied rules execute name lookup, argument
evaluation, nested calls, lambda construction, frame changes, return, and both
allocations.

The direct entry claim does not literally parse a filesystem path at proof
time, but its definitional module and closure terms are exact expansions of the
trusted-translator output, and the separate loading claim establishes the
installed binding. This is sufficient source pinning; a body change would
break the checked term equality or change the execution proof.

### Satisfiable witnesses and concrete substitution

Every precondition is satisfiable:

- the loading claim's displayed initial state is ground and has no side
  condition;
- `VS = .ValSeq` and, nontrivially,
  `VS = vCons(1,vCons(5,vCons(2,vCons(3,vCons(4,.ValSeq)))))` satisfy
  `allNonNegativeInts(VS)`;
- `N = 5` satisfies the non-negative key claim; and
- `N = -1` satisfies the negative key claim.

For `[1,5,2,3,4]`, substitution yields returned `ref(1)`, heap 0 equal to
`list(sortVS(VS))`, and heap 1 equal to
`list(sortKeyVS(sortVS(VS),popcountKeyClosure))`. Under the supplied sort
contract that list is `[1,2,4,3,5]`; both trusted canonical Python and candidate
Python return exactly that value, and the fresh LLVM execution displays that
same inner/outer allocation pair. For `N=5`, the key RHS evaluates to 2, equal
to `bin(5).count("1")`.

The full ground states and substituted terms are in
`evidence/adequacy_witness.py` and `16-adequacy-witness.log`.

The result is not a free variable, tautology, or one-way implication:
`ref(1)`, both heap objects, heap locations, and all control/state cells are
fixed. The fresh false-return mutation in stage 6 confirms that constraint.
The contents of heap 1 do retain the explicitly named supplied
`sortKeyVS` abstraction discussed below.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventories every K declaration from all 24
supplied K files (including the root `semantics.k`) plus `verification.k` and
`spec.k`.
`evidence/k-inventory.tsv` is lossless and line-addressed; it contains full
declaration text. The summary (`k-inventory-summary.json`,
`14-k-inventory.log`) records 1,231 structural entries from 26 files:

- 1 configuration;
- 234 syntax declarations;
- 704 ordinary rules;
- 5 contexts;
- 4 claims;
- plus every module, import, require, and endmodule entry.

`evidence/k-special-declarations.tsv` enumerates every declaration or rule with
`function`, `total`, `functional`, `symbol`, `no-evaluators`, `priority`,
`owise`, `concrete`, `macro`, `macro-rec`, `simplification`, or `anywhere`.
There are 152 function declarations, 114 total declarations, 25 symbol
declarations, 22 `no-evaluators` declarations, 45 priority-bearing entries, 27
`owise` entries, 35 concrete entries, three macros, and one recursive macro.
There are no `functional`, `simplification`, or `anywhere` entries.

`evidence/k-rule-assessments.tsv` gives an explicit disposition and basis for
all 948 configuration/syntax/context/rule/claim entries. The 1,200 structural
entries in `reference-semantics` are accepted as the selected fixed semantics
only after byte identity with the trusted mount; unused rules do not contribute
to this theorem. This does not infer Python correctness from those rules. Every
fixed rule reachable from this program received the focused binding,
evaluation, control, state, overlap, and result review in
`evidence/used-rule-map.md`.

### Candidate-local extensions

`verification.k` contains seven `[function,total]` declarations and nine
rules. It contains no semantic call interception, priority rule,
simplification, opaque symbol, loop rule, or claim.

- `sortArrayLambda`, `sortArrayBody`, `sortArrayClosure`, and
  `sortArrayModule` are total zero-argument names whose RHS terms exactly
  expand the submitted translated program.
- `popcountKeyClosure` is exactly the value produced by evaluating the exact
  annotated lambda with empty cell/free-variable sets. The universal helper
  claims execute its program-defined body under fixed semantics.
- `sortArraySpec(VS)` merely names
  `sortKeyVS(sortVS(VS),popcountKeyClosure)` in the postcondition. It does not
  rewrite or bypass a program call.
- `allNonNegativeInts` has exhaustive empty, integer-cons, and `owise`
  non-integer-head cases. The cases are disjoint; recursion strictly descends
  on the tail.

All local `total` declarations are covered, equations do not conflict on an
overlap, and recursion descends. These are sound definitional summaries, not
operational bridges.

### Used fixed semantics

The exact mapping is in `evidence/used-rule-map.md`. The important findings are:

- The configuration pins every relevant cell. Calls resolve their binding,
  evaluate callee and arguments in order, allocate a fresh frame, bind
  parameters, and restore control through `#pop`.
- The input `arr` binding flows to the first `sorted` call. Its result allocates
  heap 0. The outer call dereferences that object, evaluates the exact key
  lambda, and allocates heap 1. Heap allocations survive frame teardown.
- `KwArg` tags only after its expression evaluates. `IfExp` evaluates the
  condition first and chooses exactly one branch. `Compare("<",...)`, `bin`,
  `Attribute`, and string `count` dispatch to the intended supplied integer,
  binary, method-binding, and count rules.
- Exact `sorted` rules preempt the generic `[owise]` builtin dispatch.
  Reference dereference priorities preserve all other cells. The LLVM-only
  keyed-sort rule has priority 40 and executes real key calls; it is absent from
  the Haskell proof, which retains the opaque symbol.

### Opaque and priority review

The supplied tree declares 25 K `symbol(...)` functions. The complete ledger is
`evidence/opaque-symbols.tsv` and `19-opaque-symbols.log`:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

Only `sortVS` and `sortKeyVS` are reached by this theorem. All float and MD5
symbols are inert here. The used sorting symbols are pre-existing,
result-bearing trusted primitives in supplied `sort.k`, not proof-local
oracles. Their terms are fixed by the input and exact key closure, so the
candidate cannot choose an arbitrary result. But their asserted meanings as
ascending and stable keyed sorting are not universally derived in K.

The concrete LLVM module independently computes ordinary integer sort and
stable keyed insertion with real closure calls, and the differential suite
observed zero mismatches. This supports the intended interpretation on tested
inputs but does not turn the opaque proof term into a universal sorting
theorem. That is the principal concern and trust boundary.

No candidate-local false rule or materially unsound fixed-rule use was found.
Accordingly, this review makes no unsoundness claim and no false-conclusion
witness is applicable. The narrower evidence gap is the unproved intended
interpretation of the supplied opaque sort primitives.

## 6. Fresh non-vacuity test

The reviewer did not rely on a candidate mutation. The fresh artifact
`evidence/spec-vacuity-review.k` keeps the entry precondition and all heap/state
obligations unchanged but falsely changes the returned object from `ref(1)` to
`ref(0)`. `VS=.ValSeq` is a satisfying ground witness: even the empty input
performs two distinct allocations and returns the outer object.

First, the mutation built successfully:

```text
kprove /audit-output/evidence/spec-vacuity-review.k \
  --definition verification-kompiled \
  --spec-module REVIEW-SPEC-VACUITY --dry-run
```

Exit 0; the generated `kore-exec` command appears in
`evidence/17-vacuity-dry-run.log`.

The actual mutation proof then failed for the intended unmet result:

```text
kprove /audit-output/evidence/spec-vacuity-review.k \
  --definition verification-kompiled \
  --spec-module REVIEW-SPEC-VACUITY
```

Exit 1 with `WarnStuckClaimState`; see
`evidence/18-vacuity-kprove.log`. The residual final configuration explicitly
contains `<k> ref(1) ~> .K </k>`, heap 0 with `sortVS(VS)`, heap 1 with
`sortKeyVS(sortVS(VS), exact-closure)`, and `heapLoc` 2. It cannot unify with
the false `ref(0)` destination. This is meaningful non-vacuity evidence, not a
parse error, missing import, timeout, or unrelated crash.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the exact supplied semantics and its primitive interpretations, for every
finite `ValSeq` of non-negative mathematical integers, partial-correctness
execution of the exact submitted `sort_array` body:

1. performs the inner ordinary `sorted`;
2. constructs the exact submitted key closure;
3. performs the outer keyed `sorted`;
4. returns the newly allocated outer object at `ref(1)`; and
5. leaves all displayed heap, environment, scope, stack, return, exception, and
   exit-code cells exactly as the entry postcondition states.

It also establishes exact module loading and exact key-body execution on both
integer-sign branches. The main result is the constrained term
`sortKeyVS(sortVS(VS),popcountKeyClosure)`, not an existential result.

### Trust and assumption ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K v7.1.337 parser/compiler/Haskell prover and builtin `Int`, `Bool`, `Map`, `List`, string operations | All formal execution and proof closure | Necessary framework trust. Fresh builds, individual proofs, and mutation behavior are logged. |
| Trusted `py2mpy.py` | Source-to-`solution.mpy` identity | Acceptable trusted input; regenerated output is byte-identical. The translator itself is not proved correct in K. |
| Byte-identical supplied MPY semantics | Language execution, cells, calls, allocation, operators | Required selected semantics. Candidate made no change. Used paths were reviewed; unused fixed rules and warnings do not affect this theorem. |
| `sortVS` | Inner ascending sort and tie-order setup | Result-bearing supplied opaque primitive. Concrete insertion rules and differential tests support it; no universal K connection theorem establishes its human-facing contract. |
| `sortKeyVS` | Final value, stability, and application of the key closure | Result-bearing supplied opaque primitive. The LLVM-only leg performs real closure calls and stable insertion; finite concrete/differential evidence supports it. The Haskell proof remains conditional on its supplied contract. |
| Other 23 `symbol(...)` declarations | None | Explicitly inventoried and unreachable from this program/claims. |
| `binCodes`/`cntSub` to mathematical popcount | Key meaning | The key claim formally executes to these defined recursions. Identifying the binary-digit count with ordinary popcount is a straightforward but informal mathematical bridge, supported by concrete and differential tests. |
| Stable double sort to lexicographic `(popcount,value)` order | Natural-language result | Ordinary mathematical/stability argument, conditional on the sort contracts. The prompt examples contradict this prose interpretation; the trusted canonical agrees on the stated non-negative domain. |
| CPython canonical and 8,391-case differential suite | Candidate-to-canonical adequacy and primitive interpretation on tested inputs | Independent finite evidence only, with zero intended-domain mismatches. Negative divergences are preserved and excluded by the formal precondition. |
| Missing generation logs/metrics/trace | Provenance auditability | Concerning but not theorem-changing. Reconstruction does not depend on them. |
| Termination outside the terminating executions represented by partial correctness | Total correctness | Not proved. The formal result is partial correctness. |

Gate A (real-program soundness) passes: exact program-defined bodies execute,
local equations are true and complete, state/control are preserved, entry
states are satisfiable, and the false-result mutation is rejected. The supplied
sorting builtin is an explicit external primitive, not a candidate bridge.

Gate B (intent adequacy) is legitimate but limited: on the stated non-negative
domain the candidate, canonical implementation, formal precondition, and
ordinary `(popcount,value)` contract align. The prompt examples are
contradictory, and the final sorting meaning is conditional on the supplied
opaque primitive contracts.

Gate C (trust/evidence auditability) has concerns: reconstruction is fully
reproducible, but the universal sort-meaning connection theorem and generation
provenance records are absent. Finite tests support, but do not prove, the
opaque semantic bridge.

Therefore the reconstructed proof is sound, result-constraining, and pins the
real generated program. Its explicitly conditional bridge from supplied opaque
sorting terms to the natural-language sorting property prevents an
unqualified `PASS` but does not make the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
