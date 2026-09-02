# Independent adversarial audit: 29-filter-by-prefix

The candidate contains a sound, result-constraining partial-correctness proof
of the submitted function over an unbounded, list-isomorphic representation of
all finite `List[str]` values. The submitted Python, translated constructor
term, macro-expanded function body, and term executed by the entry claim all
agree. Fresh builds and proofs succeeded, while independent body and
postcondition mutations failed for the expected semantic reasons.

I assign `CONCERNS / LEGIT`, rather than `PASS`, for one limited auditability
gap: the candidate states its universal theorem over the proof-only
`stringList(StrList)` representation rather than the supplied semantics'
ordinary `list(ValSeq)`/heap-reference representation. Its two iterator rules
are visibly exhaustive and constructor-for-constructor identical to the fixed
list iterator, so this neither bounds nor narrows the HumanEval value domain.
However, the candidate contains no separately machine-checked universal
connection theorem for that representation bridge. Finite fixed-list K runs
and extensive Python differential tests support the bridge but cannot make it
part of the submitted theorem.

## 1. Input and provenance integrity

The launcher declares `record_layout: legacy-selected-stage1` and
`semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as required.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required generation records,
`usage.json`, the complete 393-record structured trace, and the complete
generation output through a bounded summarizer. These records were treated
only as untrusted historical claims.

Independent checks found:

- The campaign-lock JSON equals the `audit_campaign` object exactly. Its
  SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`.
- Every required record is a readable regular file. Every recorded per-file
  digest, including the trace, output log, prompt, metrics, usage, invocation,
  run, task, and result records, matches.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
  their trusted `/reference` counterparts.
- Recursive entry-name, entry-type, and file-digest comparison of
  `/candidate/reference-semantics` against the trusted tree reports exact
  equality: no missing, additional, changed, mistyped, special, or symlinked
  entries.
- The candidate tree contains no symlinks. All required proof artifacts
  (`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`)
  are present.
- The generation record's `KPROVE_PASSED` marker was not relied on.

The primary evidence is
`evidence/inspect_provenance.py`, `evidence/01-provenance.log`,
`evidence/summarize_generation.py`, and
`evidence/01-generation-summary.log`. The provenance command exited 0. There
is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: given a finite list of Python strings and a string
prefix, return, in original order and with duplicates preserved, exactly those
elements for which `str.startswith(prefix)` is true. The contract has no size
bound. An empty list returns an empty list, and an empty prefix matches every
element.

The canonical implementation is a list comprehension. The candidate uses a
loop, an initially empty result list, `string.startswith(prefix)`, and
`result.append(string)`. The extra initialization `string = ""` does not affect
the returned result.

Using the trusted translator:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.2.mpy
cmp -s solution.regenerated.2.mpy solution.mpy
sha256sum solution.regenerated.2.mpy solution.mpy
```

exited 0. Both files have SHA-256
`1c4b746359e3db4ea54a2e3c9dd703b9a4bc4f1b75b0b6c0af45d832931f9502`;
see `evidence/02-translation-replay.log`.

The independent differential test imports `/reference/canonical.py` and
`/candidate/solution.py` under separate module names. It covers the documented
examples, empty arguments, empty prefix, exact/short/long/mismatching
prefixes, duplicates, order, Unicode, combining characters, astral characters,
NUL, and newline. It then exhausts all lists through length 3 over all strings
through length 2 from `{"a","b","é"}`, with every such string as a prefix, and
runs 10,000 seeded broader generated cases. The exact command was:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 with `TOTAL_CASES=40950` and `MISMATCHES=0`. The generator, seed,
directed inputs, oracle construction, and results are preserved in
`evidence/differential_test.py` and `evidence/02-differential.log`.

## 3. Clean proof reconstruction

I copied source artifacts into `/tmp/audit-work/reconstruction`, copied the
semantics from the trusted `/reference` mount, and did not copy or use any
candidate-built definition or cache.

`kup` is absent, but the independently installed tools run and report K
v7.1.293, matching the campaign lock. The fresh commands and outcomes were:

| Purpose | Exact substantive command | Exit / result |
|---|---|---|
| LLVM build | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-fresh` | 0 |
| Concrete suite | `krun concrete-tests.mpy --definition runtime-kompiled-fresh --output pretty` | 0; final `.K`, `NoExc`, exit code 0 |
| Haskell build | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled-fresh` | 0 |
| Original claims | `kprove spec.k --definition verification-kompiled-fresh --spec-module FILTER-BY-PREFIX-SPEC` | 0; `#Top` |

The corresponding bounded logs are `evidence/03-kompile-llvm.log`,
`evidence/03-krun-concrete.log`, `evidence/03-kompile-haskell.log`, and
`evidence/03-kprove-all-claims.log`. Compiler warnings concern unused
variables and non-exhaustive total functions in unrelated supplied-semantics
features; none is on the target execution path.

To check the two positive claims separately, I added labels only in
`evidence/03-spec-labeled.k`. Parsed KAST comparison confirms that both labeled
claim bodies, requirements, and ensures are exactly equal to the originals
(`evidence/compare_labeled_claims.py`,
`evidence/03-labeled-claim-comparison.log`).

- The loop invariant alone exited 0 with `#Top`
  (`evidence/03-kprove-loop-claim.log`).
- The entry theorem exited 0 with `#Top` when the already independently proved
  loop invariant was marked trusted for that second run
  (`evidence/03-kprove-entry-with-verified-loop.log`).
- As an expected dependency diagnostic, selecting the entry theorem while
  removing its loop lemma merely kept unrolling; it was interrupted after
  about 27 seconds. This is not a failed required proof. The unmodified
  multi-claim proof and both dependency-ordered proof runs close.

Thus every positive target claim was reconstructed from source, with the only
trusted claim in the entry-only run already proved by the preceding independent
run.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

The loop claim says: for any finite remaining `StrList`, prefix, arbitrary
already accumulated `ValSeq`, and the exact loop body from the submitted
function, executing the loop terminates the loop computation and changes the
result heap object from `ACC` to
`valSeqConcat(ACC, prefixFilter(PREFIX, REST))`. It preserves the arbitrary
continuation and all framed cells, preserves the prefix/result/strings
bindings, and permits only the loop target variable `string` to change.

The entry claim says: from the supplied semantics' clean module state, load a
module containing the typing import and the exact submitted function, call it
on an arbitrary finite `StrList` and arbitrary finite prefix code sequence,
then inspect the returned heap object. The computation reaches Boolean `true`,
with the returned list exactly `prefixFilter(PREFIX, INPUT)`, no exception,
empty call stack, restored return state, and precisely one result allocation.

Both preconditions are satisfiable. One loop witness is `L=1`, `H=0`,
`SC = 0 |-> scope(.Map,parent(-1))`, empty `REST`, empty `ORIGINAL`, empty
prefix, empty accumulator, and any current string value, with heap
`0 |-> list(.ValSeq)`. An entry witness is the exact declared initial
configuration with `INPUT=["a","b"]` and `PREFIX="a"`.

`evidence/spec-ground-correct.k` substitutes that entry witness and the
claimed result `["a"]`; its proof exits 0 with `#Top` in
`evidence/04-ground-correct-kprove.log`. The independent concrete
interpretation of `prefixFilter` agrees with both Python implementations for
this and an empty-prefix witness; see `evidence/claim_witness.py` and
`evidence/04-claim-witness.log`.

### Mechanical program identity

The entry claim's `filterByPrefixDef` macro expands to the translated
`FuncDef`. I parsed both the trustedly regenerated `solution.mpy` module and an
explicit macro-expanded module through the fresh definition:

```text
kast solution.mpy --definition verification-kompiled-fresh --module VERIFICATION --sort Module --output json ...
kast executed-module.mpy --definition verification-kompiled-fresh --module VERIFICATION --sort Module --output json ...
cmp -s solution.kast.replay.json executed-module.kast.replay.json
```

The command exited 0, and both KAST files have SHA-256
`e2c6cbcae2c9e2b01e17f5cc1ad17cfa022e230bf387ffd1384e6ca06fa48943`;
see `evidence/04-constructor-replay.log`,
`evidence/executed-module.mpy`, `evidence/solution.kast.json`, and
`evidence/executed-module.kast.json`. Differences such as omitted textual
`.Exprs`/`.Stmts` are parser-normalized unit syntax, not body differences.

The fixed semantics executes every material operation: module load and
function binding, left-to-right call argument evaluation, parameter binding,
list allocation, local assignment, loop iteration and target binding, name
lookup, method binding, `startswith`, conditional branch, in-place `append`,
return, frame pop, and heap observation. There is no rewrite replacing the
function call or body by `prefixFilter`.

### Body sensitivity

I changed the actual macro-expanded `If` condition from the submitted
`startswith` call to `Bool(false)`, rebuilt the altered proof definition, and
reran the unchanged claim bodies. The build exited 0; proof exited 1 with
`WarnStuckClaimState` on the nonempty-input branch, requiring an empty actual
list to equal the nonempty `prefixFilter`. The concrete witness
`strings=["a"]`, `prefix="a"` makes the conclusion false. Files and logs are
`evidence/verification-body-mut.k`, `evidence/spec-body-mut.k`,
`evidence/04-body-mutation-kompile.log`, and
`evidence/04-body-mutation-kprove.log`. This mutation changes the term actually
loaded by the claim, not merely an external source file.

### Input-representation limitation

The universal candidate claim passes `stringList(INPUT)` rather than an
ordinary fixed-semantics `list(ValSeq)` or heap reference. `StrList` is
inductive and unbounded; every finite Python `List[str]` has exactly one such
value. Its empty/nonempty `#iterNext` rules have the same control shape and
yield the same strings in the same order as fixed `list` iteration, and no
other operation on the input is used.

A ground theorem using a real fixed-semantics bare `list(ValSeq)`, for which no
`stringList` rule can match, exits 0 with `#Top`
(`evidence/spec-real-list-ground.k`,
`evidence/05-real-list-ground-kprove.log`). The fresh LLVM suite additionally
uses heap-allocated list literals.

I also attempted a reviewer-authored universal fixed-list theorem using a
transparent `strValues(StrList)` embedding. It built, but the proof exited 1
because K could not invert symbolic equations such as
`strValues(REST) == .ValSeq`; the residual is an embedding-injectivity
obligation, not a behavioral counterexample. This experiment is preserved in
`evidence/verification-real-list.k`, `evidence/spec-real-list.k`,
`evidence/05-real-list-kompile.log`, and
`evidence/05-real-list-kprove.log`. Because the candidate itself lacks such a
universal connection theorem, I retain this as the reason for `CONCERNS`.
There is no size restriction or excluded `List[str]` value, so it is not a
material HumanEval-domain narrowing and does not justify `FAIL`.

## 5. Rule-by-rule static soundness review

`evidence/build_rule_inventory.py` generated the exhaustive
`evidence/05-rule-inventory-v4.tsv`. It inventories 944 items:

- 704 rules,
- 232 syntax declarations,
- 5 contexts,
- 1 configuration, and
- 2 reachability claims.

Every entry records file/line, full normalized text, attributes (including
`function`, `total`, `simplification`, `macro`, `priority`, `owise`,
`concrete`, `symbol`, and `no-evaluators`; no local `functional` attribute was
found), target-path classification, and a review disposition. The aggregate
dispositions are 712 accepted fixed unused items, 28 documented
fixed-semantics subset approximations, 22 explicitly `no-evaluators` opaque
fixed declarations, 166 sound target-path items, and 16 proof-local
declarations/rules/claims.

### Used-constructor map

| Submitted construct | Declaration and material rules |
|---|---|
| `Module`, `ImportFrom` | `syntax.k`; core `#loadAll`/statement sequencing; `controls.k` typing-import no-op |
| `FuncDef`, `Params` | `syntax.k`; simple closure binding in `functions.k` |
| `Call`, `Attribute`, `Name` | `syntax.k`; core scope lookup and left-to-right `#evalArgs`; `call.k` callee/method/closure dispatch |
| `ListExpr()` | `list.k` evaluation, `vals2valSeq`, fresh `#alloc` |
| `Assign(Name, ...)` | strict RHS and current-scope update in `controls.k` |
| `Str("")` | `str.k` literal conversion; only the exhaustively handled empty literal is used |
| `For` | strict iterable evaluation; `#loop`, iterator protocol, `#loopStep`, and `#loopLbl` in `controls.k` |
| loop target `Name("string")` | `tuple.k`'s simple `#bindTgt(Name,Val)` rule |
| `If` | strict condition, `truthy(Bool)`, and disjoint `#branch` rules |
| `startswith` | generic method binding/call plus `methods.k`'s `startsWith` equations |
| `result.append(string)` | the priority-40 heap-ref mutator in `list.k`; it beats generic receiver dereference |
| `Return` | return-state update, frame restoration, scope removal, and continuation restoration in `functions.k` |

Evaluation order is fixed by strictness/contexts and the `#evalArgs` accumulator.
The append rule reads and writes only the selected heap object. The call rules
allocate one scope, save the continuation and caller environment, and restore
them on return. The plain-frame cell rules are excluded by their `$cells`
guards. Relevant priority overlaps select the append mutator and ordinary
assignment/target-binding paths as intended.

### Proof-local extensions

- `filterByPrefixDef` is a syntax macro, not an execution shortcut. Mechanical
  KAST comparison establishes exact body identity.
- `StrList` has only empty and nonempty constructors.
- The two `stringList` iterator rules are exhaustive, have no overlap with
  fixed constructors, preserve the continuation and all cells, and yield
  precisely the encoded strings. They are a proof-domain representation, not
  an oracle for the result.
- `prefixFilter` has an empty rule and two nonempty rules guarded by the same
  total Boolean `startsWith`. The `true` and `false` guards are disjoint and
  exhaustive. Each rule structurally decreases the `StrList`; the result is
  exactly stable prefix filtering.
- `valSeqConcat(VS,.ValSeq) => VS` and right-association are valid for the
  free-list equations in `list.k`. Their overlaps with the defining equations
  agree, and the orientations terminate.
- `#checkFilter` reads the actual returned heap list and rewrites to
  `ACTUAL ==K EXPECTED`. It does not fabricate or constrain `ACTUAL`; the
  equality must reduce to `true`.
- The loop claim matches the exact real loop body and a continuation-polymorphic
  suffix. The body has no abrupt control, exceptions, output, or input mutation,
  so eliminating only the completed loop computation preserves the suffix.

No proof-local opaque symbol, priority rule, unconstrained oracle, assumed
program helper, task-answer rewrite, or inconsistent equation exists.

### Supplied-semantics boundaries

The Haskell target does not reach any of the imported opaque primitives:
`md5hexCodes`; `sortVS`/`sortKeyVS`; or the float-family
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. Their dependents are unrelated fixed-semantics operations, not either
target claim.

The supplied MPY language deliberately contains unused approximations. They
do not overlap a reachable target term, but the following concrete witnesses
prevent overstating the semantics as full Python:

- `isIntV(_:Val) => false [owise]`: Python
  `isinstance(True, int)` is `True`, while this MPY case is `false`.
- Generic `ImportFrom`/`Import` no-op rules: `from math import sqrt; sqrt(4)`
  or `import os; os` binds a name in Python but not under those generic MPY
  rules. The used `from typing import List` binding is never read and is
  inert after annotations are erased.
- `For(...,ref(H),...)` snapshots the list. A Python loop that appends to the
  same list observes appended elements; MPY's snapshot does not. The submitted
  loop never mutates `strings`.
- Eager `map(str, ...)` makes a reusable list. In Python, iterating the same
  `map` object twice exhausts it after the first pass. It is unreachable here.
- `str.encode` returns the code-sequence model unchanged. For example,
  `"é".encode("ascii")` raises in Python, but that MPY rule would return a
  string-model value. It is unreachable here.
- Haskell-side shallow list equality can distinguish two separate references
  to structurally equal nested lists: Python `[[]] == [[]]` is true, while
  direct `==K` on distinct inner refs is false. No comparison occurs here.

These are fixed, unused language-subset limitations, not proof-local rules and
not routes by which this target closes. No unsoundness is alleged without the
explicit witnesses above. Other unmodeled exceptional cases merely get stuck;
I treat those as coverage limitations, not false conclusions.

## 6. Fresh non-vacuity test

I authored `evidence/spec-vacuity.k`, which loads the actual function and calls
it on the satisfiable input `strings=["a"]`, `prefix="a"`, but changes the
result obligation to require `[]`. Both the trusted canonical and candidate
Python functions return `["a"]`, so the mutation is demonstrably false.

Exact command:

```text
kprove spec-vacuity.k --definition verification-kompiled-fresh --spec-module FILTER-BY-PREFIX-SPEC-VACUITY
```

It parsed and executed normally, then exited 1 with
`WarnStuckClaimState`. The residual contains `<k> false ~> .K </k>` and the
actual heap contains
`list(vCons(str(iCons(97,.IntSeq)),.ValSeq))`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. See `evidence/06-false-result-kprove.log`. The matching true ground
claim had already exited 0 with `#Top`.

## 7. Proven versus assumed accounting

Formally, under the supplied MPY semantics plus the transparent candidate
extensions, the successful reachability proof establishes:

1. the exact submitted function body executes from the stated initial state;
2. for every finite `StrList` and every finite prefix `IntSeq`, the loop
   appends exactly those original strings satisfying the fixed
   `startsWith` predicate, in order and with duplicates;
3. the returned heap object contains exactly that sequence;
4. the observer evaluates to `true`, with no exception and a restored call
   stack/return state.

The proof is partial-correctness in the Kit sense. Its inductive constructor
domain is unbounded; it is not a finite-size proof or bounded unrolling.

The trust ledger is:

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell backend, and built-in Int/Bool/String/Map/K-equality theories | All builds and proofs | Standard low-level trusted computing base |
| Trusted supplied MPY rules on the mapped target path | Binding, control, heap allocation/write, call/return, strings, and loops | Audited rule-by-rule; sound for this program |
| Trusted translator | Source-to-constructor bridge | Byte identity plus constructor-level KAST identity |
| `stringList(StrList)` representation | Universal formal input and loop iteration | Sound and exhaustive by its equations; universal fixed-list connection is informal rather than candidate-proved, causing `CONCERNS` |
| `prefixFilter` | Postcondition and loop summary | Fully defined by exhaustive, guarded, descending equations; not opaque |
| `#checkFilter` | Final result observation | Reads the actual heap list and demands equality; mutation proves it discriminates |
| Fixed opaque sort/float/hash symbols | None | Imported but unreachable; no target dependency |
| Python differential suite | Source/canonical behavioral bridge on 40,950 inputs | Strong finite evidence only, not a universal proof |
| LLVM and fixed-list ground K runs | Concrete supplied-semantics/representation bridge | Finite evidence only |

Kit gates: Gate A passes (real body, state/control fidelity, valid proof-local
equations, body sensitivity, and non-vacuity); Gate B passes (the unbounded
finite-string-list value domain and requested filtering property are covered);
Gate C has the narrow representation-connection limitation described above.
Under the benchmark's decision boundary, that is a legitimate proof with a
non-fatal trust/evidence concern, not a substituted program, vacuous theorem,
bounded domain, or materially unsound proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
