# Independent adversarial review: HumanEval/104 `unique_digits`

The candidate's K commands are reproducible and its theorem is
result-constraining, but it is not a legitimate proof of the submitted Python
program. The generated semantics recognizes the exact translated program and
then replaces the entire execution with the task's mathematical answer. It
contains no semantics for the program's function definitions, branches,
returns, name lookup, calls, recursion, comprehension, or `sorted`. There is no
bridge-free connection theorem. An intended-domain witness also makes the
substitution observably false: on a positive 995-digit all-odd integer, K
returns normally while the submitted CPython program raises `RecursionError`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1` and `semantics_mode = GENERATED_SEMANTICS`. I followed
the declared `container_paths`, not the host provenance paths.

- `/audit-campaign-lock.json` is a regular file. Its JSON object equals the
  `audit_campaign` block exactly, and its independently computed SHA-256 is the
  recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The required `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, structured trace, and present `usage.json` are readable,
  regular, nonsymlink files/trees. Every recorded file hash checked by
  [the provenance checker](evidence/provenance_check.py) matches. The trace's
  sole JSONL file has the hash recorded in `generation-result.json`; all 163
  records parse, with their event and payload types inventoried in
  [stage1-provenance.log](evidence/stage1-provenance.log).
- The legacy records consistently identify problem `104-unique-digits`,
  condition `bare`, the selected invocation, and the untrusted
  `KPROVE_PASSED` generation marker. I inspected the full structured trace and
  the generation log's program, semantics, compile, execution, proof, and
  final-report events. These are only generation-history claims.
- The mounted candidate consists of eight regular source artifacts and no
  symlinks. The provenance log records an independent relative-path,
  size, and SHA-256 manifest for every file.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`. Their hashes match the
  launcher records.
- `/reference/canonical.py` has the recorded trusted hash.
- `/reference/reference-semantics` is absent, as `GENERATED_SEMANTICS`
  requires. I did not infer or use any hidden semantics.
- Historical runtime metrics not required by this legacy-selected layout were
  not reconstructed. Present legacy auxiliary records were inspected and
  their hashes match `generation-result.json`.

There is no audit-infrastructure breach. I copied only the eight candidate
source artifacts to
`/tmp/audit-work/104-unique-digits-audit-002/source`, made that scratch copy
writable, and built all definitions there. The candidate contained no mounted
compiled definition or cache, and none was reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For a list of positive integers, `unique_digits` must return, in increasing
numeric order, every occurrence of every input integer whose decimal digits
are all odd. Inputs with any even decimal digit are omitted. The empty list is
allowed, duplicates must be preserved, and the prompt gives no bound on list
length, integer value, or decimal digit count.

The trusted canonical converts each positive integer to decimal text, tests
every digit for odd parity, retains qualifying occurrences, and sorts them.
The candidate instead defines a recursive `no_even_digit`: zero is the
recursion base, an even current integer is rejected, and an odd current
integer recurses on floor division by ten. `unique_digits` filters through
that helper and calls `sorted`.

### Translation identity

Fresh translation with the trusted translator exits 0 and produces SHA-256
`d8d3826e35a2ff49382daa10d55e5efc95ef660c0c28438bc242abd69a136940`,
byte-identical to the submitted `solution.mpy`. See
[stage2-translation.log](evidence/stage2-translation.log).

### Independent differential testing

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and submitted entry point independently. It tests both prompt
examples, empty and one-element boundaries, all digit-predicate branches and
digit positions, duplicates, mixed lengths, 300 deterministic random lists,
all singleton values from 1 through 2000, and all-odd integers around
CPython's recursion boundary. The complete bounded output and exit status are
in [stage2-differential.log](evidence/stage2-differential.log).

- Both implementations agree on 2,300 deterministic generated cases and the
  ordinary named cases, including all-odd integers through 990 digits.
- They disagree on five positive, in-contract all-odd inputs of 995, 999,
  1000, 1001, and 1100 digits. The canonical returns the integer; the
  candidate raises `RecursionError`.
- A compact exact witness is
  `H = (10 ** 995 - 1) // 9`, the positive 995-digit repunit. `[H]` satisfies
  the source domain without any unstated extension.

The differential script therefore exits 1 with five mismatches. This is a
material implementation/source-contract discrepancy, not an out-of-domain
stress test: the prompt says positive integers without a digit bound.

## 3. Clean proof reconstruction

The installed live toolchain is K v7.1.293; `kompile`, `krun`, and `kprove`
are independently available. See
[stage3-toolchain.log](evidence/stage3-toolchain.log).

From the clean scratch sources I built:

- `semantic.k` with the Haskell backend, main module `MPY-SEMANTIC`, syntax
  module `MPY-SYNTAX`, into a fresh `concrete-kompiled`; exit 0
  ([log](evidence/stage3-kompile-concrete.log)).
- `verification.k` with the Haskell backend, main module `VERIFICATION`,
  syntax module `MPY-SYNTAX`, into a separate fresh `proof-kompiled`; exit 0
  ([log](evidence/stage3-kompile-proof.log)).

The candidate `spec.k` run exits 0 and prints `#Top`. K warns that the two
ground digit-summary claims are trivial claims, but that is not a command
failure. See [stage3-kprove-all.log](evidence/stage3-kprove-all.log).

I also copied each of the five positive claims exactly into separate reviewer
modules in [individual-claims.k](evidence/individual-claims.k) and ran each
module independently. Every command exits 0 and prints `#Top`; outputs are in
[stage3-kprove-individual.log](evidence/stage3-kprove-individual.log).

Fresh concrete execution was compared with both Python implementations by
[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py):

- K, canonical Python, and candidate Python agree on empty, example,
  predicate-branch, and duplicate cases.
- For `[H]`, fresh K returns `[H]`, matching the canonical mathematical
  answer, while the submitted Python raises `RecursionError`.

The successful K reconstruction confirms closure under the candidate's theory.
The last comparison proves that this theory is not an execution semantics for
the real submitted program over the claimed domain. Full results and bounded
hash-based summaries are in
[stage3-concrete-compare.log](evidence/stage3-concrete-compare.log).

## 4. Adequacy and real-program pinning

The five claims mean:

| Claim | Precondition | Postcondition |
|---|---|---|
| Universal entry | `NS` is any finite `IntSeq` whose elements are all strictly positive; empty is admitted | final `<k>` is exactly `pyList(uniqueDigitsSpec(NS))` |
| Digit true | none | the proof-local summary says 97531 has all odd digits |
| Digit false | none | the proof-local summary says 1422 does not |
| Example one | ground input `[15,33,1422,1]` | exact result `[1,15,33]` |
| Example two | ground input `[152,323,1422,10]` | exact empty result |

The entry result is not free or merely implication-constrained:
`uniqueDigitsSpec(NS)` reduces to
`sortInts(filterOddDigits(NS))`.

The entry precondition is satisfiable. The concrete witness
`NS = cons(15, cons(2, .Ints))` reduces to `true`, and both Python
implementations return `[15]`. A reviewer K entry claim reaches exactly
`pyList(cons(15, .Ints))`. These checks are in
[stage4-pinning.k](evidence/stage4-pinning.k),
[stage4-pinning.log](evidence/stage4-pinning.log), and the named
`entry-precondition-witness` in the differential log.

There is real constructor-level identity but no execution identity:

- Trusted regeneration is byte-identical to `solution.mpy`.
- `solutionProgram` expands to the complete submitted constructor tree,
  allowing only K's explicit empty-list normalization. The reviewer pinning
  claim closes.
- Concrete `krun` on the submitted `solution.mpy` satisfies the exact-tree
  recognizer.
- A body-sensitivity mutation changes the base-case `Return(Bool(true))` in
  the actual term expanded by `solutionProgram` to `Return(Bool(false))`,
  without changing the recognizer. The mutated definition builds, and the
  entry proof fails with `WarnStuckClaimState` at the changed constructor
  tree. The exact diff, preserved semantic, spec, compile log, and proof log
  are
  [stage4-body-mutation.diff](evidence/stage4-body-mutation.diff),
  [stage4-body-mutated-semantic.k](evidence/stage4-body-mutated-semantic.k),
  [stage4-body-mutation-entry.k](evidence/stage4-body-mutation-entry.k),
  [stage4-body-mutation-kompile.log](evidence/stage4-body-mutation-kompile.log),
  and
  [stage4-body-mutation-kprove.log](evidence/stage4-body-mutation-kprove.log).

This sensitivity establishes only a syntactic admission check. Once the tree
is recognized, no node in either function body executes. There is no helper,
loop, recursion, call, or sorting execution claim matching the source control
flow. The two `allDecimalDigitsOdd` claims execute a proof-local mathematical
function, not `no_even_digit`.

## 5. Rule-by-rule static soundness review

The exhaustive declaration scan is preserved in
[stage5-declaration-scan.log](evidence/stage5-declaration-scan.log), and the
complete production-by-production and rule-by-rule assessment is in
[rule-inventory.md](evidence/rule-inventory.md). There are no candidate helper
K files.

### Syntax, configuration, and used-construct coverage

`semantic.k` declares:

- `Program`: `Module` and functional/total `solutionProgram`;
- AST statements: `FuncDef`, `If`, `Return`;
- AST expressions: `Name`, `Int`, `Bool`, `BinOp`, `Compare`, `Call`,
  `ListComp`;
- `Params`, `CmpOp`, `CompFor`, and generated list sorts for statements,
  strings, expressions, comparison operators, and comprehensions;
- proof/runtime representations `.Ints`, `cons`, `pyList`, and `pyBool`;
- `invoke(String, PyVal)`.

The configuration has only a `<k>` cell. There is no environment, locals,
heap, call stack, iterator/comprehension state, list allocation, exception,
return frame, output, or builtin binding.

Every constructor in `solution.mpy` parses, but none has an operational
meaning. There are no rules for:

- module execution or binding the two functions;
- variable lookup or argument binding;
- evaluating `If`, `Return`, AST integer/Boolean wrappers, `%`, `//`, or
  `==`;
- call evaluation order, recursive calls, return propagation, or exceptions;
- comprehension iteration/binding/allocation;
- resolving or applying `sorted`.

Thus minimal generated-semantics coverage is not met: all of these constructs
are materially used by the submitted program and are merely declared.

### Exhaustive local rule inventory

`semantic.k` has 16 rules:

1. one truthful `solutionProgram` exact-tree equation;
2. one partial `isUniqueDigitsProgram` exact-tree recognizer equation;
3. four disjoint/exhaustive `oddDigits` equations;
4. three structural `filterOddDigits` equations;
5. three disjoint/exhaustive `insertSorted` equations;
6. two structural `sortInts` equations;
7. one `uniqueDigitsMeaning =
   sortInts(filterOddDigits(...))` equation;
8. one whole-program operational bridge.

`verification.k` has six rules:

1. two structural `positiveInts` equations;
2. one `allDecimalDigitsOdd = oddDigits` alias;
3. one `retainAllOddDigitItems = filterOddDigits` alias;
4. one `inIncreasingOrder = sortInts` alias;
5. one `uniqueDigitsSpec =
   inIncreasingOrder(retainAllOddDigitItems(...))` alias.

This accounts for all 22 local rules. The five reachability claims are
inventoried in Stage 4. There are no local priority, `owise`,
`simplification`, macro, context, alias-rule, opaque, or explicit
`functional` declarations. The declarations marked `[function]` are
equational functions; all except the exact-tree recognizer are marked
`[total]`.

The arithmetic/filter/insertion-sort equations are mathematically coherent on
positive inputs. Their guards are disjoint and cover their declared domains,
and recursive arguments descend. `positiveInts` is also structurally sound.
The negative and direct-zero conventions of `oddDigits` are outside the source
input contract; I do not use them as an intended-domain unsoundness witness.

The verification aliases terminate, but `inIncreasingOrder` does not state an
independent sortedness relation: it simply calls `sortInts`. More importantly,
`uniqueDigitsSpec` reduces to the same filter/sort expression placed on the
operational rule's right-hand side. This is a mathematical restatement of the
desired answer, not an execution connection.

### Decisive unsound operational bridge

At `semantic.k:119–121`:

```k
rule <k> P:Program ~> invoke("unique_digits", pyList(NS))
      => pyList(uniqueDigitsMeaning(NS)) ... </k>
  requires isUniqueDigitsProgram(P)
```

This reads the exact program and input, rewrites the only state cell, and
frames any continuation. It is an operational bridge because it replaces all
source execution with a result-bearing summary. Its value directly determines
the entry postcondition and both example results.

The required bridge checks fail:

- There is no bridge-free universal connection theorem. None can be stated
  using the candidate's fixed semantics because no source evaluator exists.
- Binding, argument evaluation, evaluation order, allocation, recursion,
  return control, builtin behavior, and exceptions are not represented.
- The bridge's arbitrary suffix is broader than any justification. The
  reviewer continuation probe appends `pyBool(false)` after the call and
  closes, confirming the match domain; see
  [stage5-bridge-context.k](evidence/stage5-bridge-context.k) and
  [stage5-bridge-context.log](evidence/stage5-bridge-context.log).
- There is no exact helper/body execution claim. The same proof-local
  filter/sort functions occur in the bridge result and reduce the
  postcondition, so their agreement is circular evidence about source
  execution.

The concrete false conclusion enabled on the intended domain is:

```text
P  = the exact submitted solution.mpy constructor tree
NS = cons(H, .Ints), H = (10 ** 995 - 1) // 9
K bridge conclusion = normal result pyList(cons(H, .Ints))
real submitted program = RecursionError, no normal list result
```

This witness is recorded by fresh K and Python execution in
`stage3-concrete-compare.log`. It is not merely a missing proof or broad but
sound abstraction: the rule establishes a false normal-return conclusion
about the actual submitted program. It also encodes the task's answer in the
semantics instead of executing the property-bearing computation.

Imported K integer, Boolean, string, sequence, matching, configuration, and
generated-list machinery are ordinary low-level trusted infrastructure. They
do not supply the missing connection or CPython behavior.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created
[spec-vacuity.k](evidence/spec-vacuity.k) with the satisfiable positive input
`[15, 2]`, changing only the result obligation from the correct `[15]` to the
false `[16]`.

- `kprove ... --dry-run` exits 0, proving that the mutation parses and builds
  against the fresh proof definition
  ([stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log)).
- Actual `kprove` exits 1 with `WarnStuckClaimState`. The residual is the
  reached `pyList(cons(15, .Ints))`, which does not unify with demanded
  `[16]`
  ([stage6-vacuity-kprove.log](evidence/stage6-vacuity-kprove.log)).

The proof is therefore discriminating and result-constraining. This positive
non-vacuity result does not repair the unsound program-to-summary bridge.

## 7. Proven versus assumed accounting

What the reconstructed reachability proof actually establishes is:

> In the candidate theory, an exact admitted constructor tree followed by
> `invoke("unique_digits", pyList(NS))` rewrites through the whole-program
> bridge to `pyList(sortInts(filterOddDigits(NS)))`; the proof-local
> `uniqueDigitsSpec(NS)` reduces to the same term. This holds symbolically for
> every finite `IntSeq` satisfying `positiveInts`, and the four ground summary
> or example claims also close.

That is a theorem about the candidate's summary theory. It is not a theorem
that the submitted Python bodies execute to that result.

| Boundary or assumption | Dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | contract, differential oracle, constructor regeneration | Acceptable launcher trust; hashes and byte identity checked |
| K `INT`/`BOOL`, matching, sequences, and generated lists | every equation and claim | Acceptable low-level K trust |
| Exact `solutionProgram` constructor alias and recognizer | entry and example claims | Constructor identity established; acceptable only as pinning |
| Mathematical `oddDigits`, filter, insertion sort | summary and postcondition | Equations are coherent on positive inputs, but their human-facing meaning is reviewed informally rather than proved by an independent property |
| Whole-program bridge to `uniqueDigitsMeaning` | universal entry and both examples | Illegitimate; program-derived, result-bearing, no bridge-free theorem, and false on `[H]` |
| Omitted CPython frames, recursion limit, and exceptions | claimed unbounded positive-input execution | Illegitimate material model gap; directly exposed by `[H]` |
| Finite differential evidence | implementation-to-contract bridge | Reproducible but not universal; moreover it contains five intended-domain mismatches |
| Opaque/fresh symbols | none | No local opaque or unconstrained result symbol exists |

Gate accounting:

- **Gate A — real-program soundness: FAIL.** The exact term is admitted but
  its bodies never execute; the operational bridge lacks a connection theorem
  and has the explicit intended-domain false-conclusion witness above.
- **Gate B — intent adequacy: FAIL.** The source domain is unbounded positive
  integers, while the submitted recursive Python implementation raises on
  valid sufficiently long all-odd integers. The formal `positiveInts`
  precondition does not exclude them.
- **Gate C — trust/evidence auditability: completed but unable to rescue the
  proof.** Fresh builds, individual claims, concrete runs, body mutation,
  continuation probe, and false-result mutation are reproducible. They expose
  rather than justify the decisive bridge.

The fresh `#Top` results and successful non-vacuity check show that this is not
a missing or merely malformed proof. It is a cleanly closing proof under a
materially unsound, task-answer-encoding generated semantics. Under the
benchmark decision boundary, that is `FAIL / NOT_LEGIT`, not a nonfatal trust
limitation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
