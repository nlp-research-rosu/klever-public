# Independent adversarial review: 70-strange-sort-list

This audit used the rendered `SUPPLIED_SEMANTICS` boundary. I treated every
candidate artifact and prior output as untrusted, copied source inputs into
`/tmp/audit-work/recon`, and rebuilt all definitions there. The final assessment
is `CONCERNS / LEGIT`: the candidate gives a non-vacuous, result-constraining
partial-correctness proof of the exact translated function body under the
supplied K theory. It has two material auditability limitations: the final
human-facing meaning depends on the supplied opaque `sortVS`/`valSeqAt` boundary,
and the proof-local loop summary matches a broader environment and continuation
domain than its independently proved loop claim. I found no false conclusion
for a state satisfying the actual entry claim.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required for
`SUPPLIED_SEMANTICS`. A recursive, no-symlink comparison found:

- the candidate and trusted semantics trees have the same directory and file
  entries;
- every entry is a regular file or directory of the expected type;
- there are no symlinks anywhere under `/candidate`;
- `diff --no-dereference -r` exits 0, so there are no missing, additional, or
  changed entries in `/candidate/reference-semantics`.

The trusted mount therefore does not contradict the rendered mode. This is a
candidate audit, not an infrastructure error.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`; both `cmp` commands exit 0.
Their matching SHA-256 digests are recorded in
`evidence/stage1_integrity.log`.

### Missing and untrusted provenance

The following requested candidate provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No top-level structured generation trace is present. This prevents checking
generation-history claims and is an auditability concern, but it does not
replace or invalidate the fresh source reconstruction below. Candidate
`*.out`, `parsed-spec.json`, `prove.sh`, and `__pycache__` were treated only as
untrusted claims and were not reused.

Evidence: `evidence/stage1_integrity.sh` and
`evidence/stage1_integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a list of integers, return a new list obtained by repeatedly choosing the
minimum remaining integer, then the maximum remaining integer, alternating
until no values remain. Duplicates are retained. The documented examples are:

- `[1, 2, 3, 4] -> [1, 4, 2, 3]`
- `[5, 5, 5, 5] -> [5, 5, 5, 5]`
- `[] -> []`

The trusted canonical implementation performs those choices directly and
mutates its private input copy by removal. The generated implementation first
computes `ordered = sorted(lst)`, then returns indices
`0, n-1, 1, n-2, ...`. That is a different but equivalent result algorithm on
integer lists. The prompt constrains the returned list, not mutation of the
caller-provided object.

### Trusted translation

Running

```text
python3 /reference/py2mpy.py /tmp/audit-work/recon/solution.py > /tmp/audit-work/recon/solution.regenerated.mpy
```

exits 0. `cmp` against `/candidate/solution.mpy` exits 0; both files have digest
`e3821adc6c256d846d6fd09bdfcc56196e564a2aac16acfe791dfb352b1535ee`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the generated entry point. Each receives a separate list copy.
The run covers:

- all three documented examples;
- eight explicit boundaries covering empty/singleton input, both parity
  branches, even and odd lengths, duplicates, negative values, ordering
  patterns, and arbitrary-size Python integers;
- every list of lengths 0 through 6 over values `-2..2` (19,531 cases);
- 2,000 deterministic random lists of lengths 0 through 30 and values
  `-1,000,000..1,000,000`.

All 21,542 comparisons agree; mismatch count is zero. This is finite adequacy
evidence, not a universal proof.

Evidence: `evidence/stage2_fidelity.sh` and
`evidence/stage2_fidelity.log`.

## 3. Clean proof reconstruction

The scratch directory contained no `runtime-kompiled`,
`verification-base-kompiled`, or `verification-kompiled` directory before the
build. K version `v7.1.337` was used.

### Concrete definition

The trusted copied semantics was built from source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The command exits 0. A reviewer-authored program containing the exact generated
function and seven assertions was translated with the trusted translator and
executed with:

```text
krun audit_concrete.mpy --definition runtime-kompiled
```

It exits 0 with `.K`, `NoExc`, and `<exit-code> 0`. The cases include empty,
singleton, both loop parity branches, even/odd lengths, duplicates, and
negative values.

### Positive target claims

The loop definition was independently built with no candidate loop-summary
rule:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC --claims LOOP-SPEC.loop-invariant
```

Both commands exit 0 and the proof prints `#Top`.

The whole-function definition was independently built and proved:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.function-correct
```

Both commands exit 0 and the proof prints `#Top`. These are the two positive
target claims in `spec.k`; both were run separately.

Compiler warnings concern unused variables in the fixed supplied string
semantics and non-exhaustive total functions in the concrete build. None is a
failed claim, and the relevant opaque total functions are accounted for in
Stage 7.

Evidence: `evidence/stage3_reconstruction.sh` and
`evidence/stage3_reconstruction.log`.

## 4. Adequacy and real-program pinning

### Plain-language claims

The `loop-invariant` claim assumes:

- the current function environment is scope 1 with `lst`, `ordered`, `result`,
  and integer `i`;
- `ordered` points to sequence `S`, `result` points to
  `strangePrefix(S,I,N)`, `N = vsLen(S)`, and `0 <= I <= N`;
- the builtins scope is exactly `builtinsScope`, heap/scope allocation counters
  are 2, and no return or exception is active.

It claims that fixed execution of the actual while condition and body reaches
loop exit with `i = N`, preserves `ordered`, and changes `result` to
`strangePrefix(S,N,N)`.

The `function-correct` claim assumes the normal initial module configuration:
empty heap, module scope plus `builtinsScope`, empty call stack, no return or
exception, and a direct call of a one-parameter closure over the submitted
body with argument `list(INPUT)`. It claims the call returns `ref(1)`, allocates
the sorted list at heap address 0 and the result at address 1, restores the
caller scope/stack, and leaves:

```text
heap[0] = list(sortVS(INPUT))
heap[1] = list(strangeResult(sortVS(INPUT)))
```

where `strangeResult(S)` is
`strangePrefix(S,vsLen(S),vsLen(S))`.

### Exact program body

The entry claim does not load the top-level `Module(FuncDef(...))`; it directly
calls the closure that loading that sole definition creates. This is not a
substituted function:

1. the trusted translator reproduces `solution.mpy` byte-for-byte;
2. independent `kast` parses show the module contains exactly one function
   named `"strange_sort_list"` with parameter `"lst"` and no trailing
   statements;
3. after macro expansion, the JSON KAST of `strangeBody()` is exactly equal to
   the translated `FuncDef` body. Both normalized bodies have SHA-256
   `867a5db8e466d71175623d989185957998a07969b84d101e021be171cb354c3e`.

Thus the direct closure call pins the real entry body, parameter binding, and
definition environment 0. Evidence:
`evidence/compare_kast_body.py` and `evidence/stage4_adequacy.log`.

### Satisfiable preconditions and concrete substitution

`INPUT = .ValSeq` (the empty integer list) satisfies the entry precondition.
A loop-head witness is `S=[1,2,3]`, `N=3`, `I=0`, `result=[]`, the actual
builtins scope, and the exact scope/heap counters in the claim.

Reviewer ground claims for `[]`, `[2,1,3]`, and `[4,1,3,2]` execute fixed
semantics without the summary and prove the explicit output lists with
`#Top`. The corresponding Python pairs are:

- `[]`: both return `[]`;
- `[2,1,3]`: both return `[1,3,2]`;
- `[4,1,3,2]`: both return `[1,4,2,3]`.

When the summary-enabled definition is asked to prove those stronger explicit
lists, it exits 1 at the equality between the explicit list and the opaque
`strangePrefix(...)` normal form. This is not a counterexample—the fixed
execution and both Python programs agree—but it shows that the K theory does
not itself normalize the proof summary to concrete output syntax. The
human-facing interpretation of the summary remains a named bridge.

### Operational bridge scope

The independently proved loop claim has exact empty `<k>` continuation and
requires `-1 |-> builtinsScope`. The summary rule in `VERIFICATION` instead:

- accepts an arbitrary trailing continuation through `<k> ... </k>`;
- replaces the exact builtin scope with arbitrary `BS:Scope`;
- is installed at priority 30, preempting normal while execution.

A reviewer continuation witness places
`Assign(Name("marker"),Int(99))` after the loop. Fixed execution proves the
explicit result and marker with `#Top`. Summary-enabled execution reaches
`marker = 99`, so the immediate continuation is preserved, but stops at the
opaque result equality. Static inspection also shows the real loop body has no
return, break, exception, allocation, or cleanup effect that can inspect or
discard its suffix. This supports lifting the loop theorem to the actual
`Return(Name("result"))` suffix, but the candidate supplies no bridge-free
universal theorem for all suffixes accepted by its rule.

There is a concrete over-breadth witness: keep an intended integer list `[7]`
but replace the builtin scope with an empty scope. With fixed semantics and
depth 30, proof exits 1 at `#look("len",-1)`. With the candidate summary, the
same claim exits 0 with `#Top`, fabricating loop completion relative to the
fixed semantics. This witness does **not** satisfy the entry claim, which fixes
`builtinsScope`, so it is not a false conclusion on the submitted program's
initial-state domain. I therefore classify it as an over-broad proof rule and
a validation concern, not a material entry-proof unsoundness. The initially
unbounded diagnostic was interrupted and replaced by the completed bounded
run; see `evidence/exploratory_interrupt.txt`.

Full evidence: `evidence/stage4_adequacy.sh`,
`evidence/stage4_adequacy.log`, and `evidence/ground-spec.k`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.tsv` contains every source-level configuration,
context, syntax declaration, rule, and claim, with file, line span, module,
attributes, origin, reachability classification, and normalized complete
sentence. Its independent source-start count agrees at 947 sentences across 26
K files:

- fixed supplied semantics: 1 configuration, 5 contexts, 227 syntax
  declarations, and 695 rules;
- candidate `verification.k`: 6 syntax declarations and 11 rules;
- candidate `spec.k`: 2 claims.

Across the whole theory, counting each attribute-bearing sentence once, the
inventory records 150 `function`, 110 `total`, zero `functional`, 23
`no-evaluators`, 26 `symbol`, 46 `priority`, 35 `concrete`, 26 `owise`, 3
`simplification`, 7 `macro`, 2 `strict`, and 1 `seqstrict` sentence.

Every fixed-semantics row is marked either
`MODULE_AUDITED_FOR_REACHABILITY_AND_OVERLAP` (600 sentences in modules that
can participate in this execution) or `INERT_FOR_SUBMITTED_PROGRAM` (328
sentences whose constructor, callable name, value type, or unimported concrete
module cannot match this program). The latter include unused language features;
they cannot contribute to either target claim. This disposition is per
inventory row, not a claim that unused semantics was tested as a separate
language.

### Used construct-to-rule map

- `Module`/`FuncDef` syntax is in `semantics/syntax.k`; the claim directly uses
  the closure value whose body was KAST-checked against that definition.
- Calls, callee-first and left-to-right argument evaluation, heap-reference
  dereference for `len`, closure-frame creation, and parameter binding are in
  `core.k`, `call.k`, and `functions.k`.
- `sorted(lst)` resolves through the real builtin scope and allocates
  `list(sortVS(INPUT))`; proof-side `sortVS` is the supplied opaque primitive,
  while concrete ground inputs use insertion-sort rules in `sort.k`.
- `result=[]` allocates the second object through `ListExpr`, `#evalArgs`, and
  `#alloc`; `append` mutates that same heap cell through the priority-40 list
  method rule. No loop iteration allocates.
- `while`, condition truthiness, `if`, expression discard, assignment, and
  integer `AugAssign` follow `controls.k`.
- comparison, `%`, `//`, `+`, and `-` follow `operators.k` and `int.k`;
  for nonnegative `i`, the candidate even/odd index formulas agree with Python
  floor arithmetic.
- list dereference and indexing follow `subscript.k`; under `0 <= i < N`, both
  selected indices are within `0..N-1`.
- `Return` pops the frame, restores environment 0, deletes the local scope, and
  preserves heap allocations, exactly matching the entry postcondition.

Priority rules that can overlap this execution were checked: reference
deref/mutator priorities select the concrete heap behavior; the only
proof-local priority is the loop summary discussed above. No exception or
allocation cell is silently changed by that summary on its intended match.

### Candidate-local declarations and rules

All 17 local sentences are individually listed in the exhaustive inventory.
Their decisions are:

1. `strangeCondition`, `strangeLoopBody`, and `strangeBody` plus their three
   macro rules are exact definitional aliases. KAST equality validates the
   whole body; the condition/body text also matches the translated while node.
2. `strangePick` is a total definitional helper with two disjoint guards
   (`pyMod(I,2)==0` versus nonzero). The formulas are the even low index and odd
   high index. It is not used by either target claim, so it contributes no
   closure shortcut.
3. `strangePrefix` is a result-bearing, total, symbolic `no-evaluators`
   function. Its base rule fixes index 0 to `.ValSeq`. Its two simplification
   rules have disjoint parity guards, require `I>=0`, append exactly the
   program-selected value, and rewrite to index `I+1`. On the loop domain
   `0<=I<N`, these are truthful induction equations and uniquely characterize
   each finite natural prefix from the base. They are syntactically descending
   as simplifications because the outer concatenation is removed. Cases outside
   the loop domain remain underspecified but do not enter either claim.
4. `strangeResult` is a transparent alias for the completed prefix.
5. `0 <=Int vsLen(S) => true [simplification]` is ordinary sequence-length
   mathematics on the intended `ValSeq` interpretation. Because `vsLen` on an
   opaque `sortVS` term is not derived by fixed equations, this is an assumed
   mathematical lemma rather than a proved bridge; it only establishes a
   nonnegative loop bound and does not encode output values.
6. The priority-30 loop rule is an operational bridge. The bridge-free
   `loop-invariant` proof justifies its value/state transition for exact
   `builtinsScope` and empty continuation. It reads the local bindings and two
   heap cells, updates only `i` and the result cell, and preserves ordered data,
   counters, return/exception status, and framed cells. Its broader `BS` and
   continuation match is not universally justified; the concrete
   missing-builtin witness above demonstrates the excess domain. Actual-entry
   static control inspection and ground continuation evidence support the
   intended use, but narrowing the rule would have made the proof cleaner.

The two claims have satisfiable preconditions, execute the exact body/loop, and
constrain the returned reference, heap allocation, and result sequence. No
free result variable, tautological postcondition, answer-encoding rule, or
program-body replacement was found.

Evidence: `evidence/inventory_k_sentences.py`,
`evidence/rule_inventory.tsv`, and `evidence/stage5_inventory.log`.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact. The fresh mutation is
`evidence/spec-vacuity-audit.k`. It keeps the real call and return reference but
changes the result heap cell from:

```text
strangeResult(sortVS(INPUT))
```

to:

```text
vCons(0, strangeResult(sortVS(INPUT)))
```

For the satisfying input `INPUT=.ValSeq`, the real result is `[]` and the
mutation requires `[0]`.

The mutation dry-run exits 0, proving it parses/builds against the fresh
definition. The real proof exits 1 with `WarnStuckClaimState`; its residual is
the expected failed implication:

```text
strangePrefix(...) #Equals vCons(0, strangePrefix(...))
```

This is an unmet result-content obligation, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation. It establishes that the
positive claim is discriminating and result-constraining.

Evidence: `evidence/stage6_nonvacuity.sh`,
`evidence/stage6_nonvacuity.log`, and
`evidence/spec-vacuity-audit.k`.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY semantics plus the candidate's reviewed prefix equations
and intended-use loop summary, for every `INPUT:ValSeq`: if the exact submitted
one-argument function call terminates from the claimed normal initial
configuration, it returns heap reference 1; heap reference 0 contains
`sortVS(INPUT)`; heap reference 1 contains the alternating low/high prefix
summary of that sequence; the function frame is removed; allocation counters
and all explicitly constrained control cells have the stated final values; and
no exception is active.

This is partial correctness. It is not a K proof that the opaque supplied
`sortVS` has Python's ascending-sort meaning, nor a separately mechanized proof
that the prefix equations express the English phrase “minimum, maximum,
minimum, ...”. Those bridges are accounted for below.

### Trust ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| K `v7.1.337`, Haskell/LLVM backends, SMT and builtin Int/Map/List theories | All parsing, execution, and proof closure | Standard toolchain trust; fresh source builds and independent positive/negative runs reduce cache risk. |
| Byte-identical supplied MPY semantics | Binding, evaluation order, heap, calls, control, arithmetic | Authorized fixed semantics for this mode. The exact used slice was statically reviewed and concretely exercised. |
| Supplied `sortVS` (`function,total,symbol,no-evaluators`) | The ordered sequence and therefore every selected output value | Explicit external trusted primitive in the supplied semantics. Ground LLVM rules implement insertion sort for integer lists; 21,542 Python differential cases give finite support. Universal ascending/permutation correctness is not proved in this candidate, so this is the main intent-bridge concern. |
| Supplied total `valSeqAt` on an opaque sequence | Each selected element | Conditional on `sortVS` denoting a real finite sequence and on the proved in-bounds indices. Concrete and Python witnesses support it; out-of-bounds behavior remains intentionally unspecified and is unreachable under the loop invariant. |
| Proof-local `strangePrefix` equations | Final result sequence | Program-derived definitional summary, not a free oracle: base plus disjoint even/odd append equations characterize all natural indices used by the loop. The bridge-free loop claim proves fixed execution maintains it. Its opaque normal form prevents direct ground normalization, so the English interpretation is partly an informal induction bridge. |
| Proof-local `vsLen` nonnegativity simplification | Establishes the initial loop bound condition | Ordinary sequence mathematics, but assumed for opaque `ValSeq` terms rather than derived from fixed rules. It does not determine result elements. |
| Priority-30 loop summary | Whole-function proof termination and result/state summary | Exact loop claim proves the intended state transition without this rule. The installed rule is broader in builtin scope and suffix; a false out-of-entry-domain witness exists. Actual entry pins builtins, and static/ground evidence supports the real suffix. Acceptable only as a documented concern, not as a reusable universally sound semantic rule. |
| Trusted translator and canonical Python entry point | Program identity and natural-intent bridge | Translator identity is byte-exact. Differential testing is broad but finite and cannot replace the K proof. |
| Missing generation provenance files | Audit trail only | Prevents validating generation-history claims; does not affect the fresh reconstruction. |

### Decision

The candidate is not vacuous, does not substitute another program, and
reconstructs cleanly. The exact real body is pinned, explicit fixed-semantics
ground outputs agree with both Python implementations, and the false
result-content mutation is rejected. I found no material false conclusion for
any integer-list input satisfying the actual entry configuration.

`PASS` would overstate the evidence because the natural-language result depends
on the supplied opaque sort/index bridge, the prefix's concrete meaning is not
normalized or separately proved in K, the loop summary is broader than its
connection claim, and generation provenance is missing. These are documented
limitations rather than a vacuous or materially false intended-domain proof,
so the appropriate pairing is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
