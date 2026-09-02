# Independent adversarial review: 72-will-it-fly

## Outcome

The candidate contains a legitimate partial-correctness proof for the intended
HumanEval integer domain: arbitrary finite lists of unbounded integers and an
unbounded integer weight. The proof was reconstructed from source, all three
entry claims independently closed, the claims execute the exact submitted MPY
function, and meaningful result and body mutations were rejected.

The status is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
auditability limitations:

1. `verification.k` accelerates the fixed reverse-slice and integer-sum folds.
   Both rules are mathematically correct and no false witness was found, but
   the candidate supplies no bridge-free universal K connection theorem.
   Fresh universal attempts did not close: reverse slicing left the expected
   structural-induction lemma, while the sum attempt made the Haskell backend
   explore an inconsistent Float branch and fail at an unavailable Float hook.
   Ground fixed-semantics checks, opposite-interpretation checks, complete
   fixed-versus-extended executions, and direct rule analysis all support the
   bridges, but finite evidence does not replace a universal K theorem.
2. `sumIntVS` is declared `[total]` over all `ValSeq`, while its equations cover
   only empty sequences and Int-headed sequences. Every theorem use is guarded
   by `allInts`, and a non-Int probe remained stuck instead of fabricating a
   result, so this is not a false conclusion on an entry domain. It is still an
   unnecessarily broad declaration.

No candidate rule is labeled unsound in this review. Consequently there is no
claimed false-conclusion witness to report. The deliberately false witnesses
used during the audit were all rejected.

## 1. Input and provenance integrity

The launcher record declares:

- problem `72-will-it-fly`;
- condition `semantics`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `SUPPLIED_SEMANTICS`;
- complete input provenance.

The mounted inputs agree with that declaration. `/reference/reference-semantics`
is present, so there is no rendered-mode contradiction.

The following checks were performed independently by
`evidence/integrity_check.py`:

- `/audit-input.json` and `/audit-campaign-lock.json` are regular readable
  files.
- The `audit_campaign` object in `/audit-input.json` is exactly equal to the
  complete campaign-lock document.
- The campaign lock hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the launcher-recorded hash.
- All records required by `legacy-selected-stage1` are regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`. `usage.json` is
  present and was also inspected. Historical runtime metrics were not
  recorded and are not required for this legacy layout.
- Every recorded individual-file hash checked by the script matches, including
  the run/task/result manifests, invocation, metrics, usage, prompt, output
  log, last message, canonical program, trusted prompt, and translator.
- The independently reimplemented pipeline tree hash of `/candidate` is
  `389211a1d4a6baa628456bb5b35f6dfabd4bd99de35961a085e64a21f1f0b464`,
  equal to the retained workspace hash in `/generation-result.json`.
- The structured trace consists of one JSONL file and all 163 JSON records
  parse. The trace inventory accounts for 31 tool calls and every outer and
  payload event type. Its pipeline tree hash is
  `3a2c87c494d0684e833b8cca2aa6ccbdc561a7741b3f1ef2b37b431f37868423`,
  equal to `usage.json`'s source-trace hash.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Candidate `reference-semantics/` and trusted
  `/reference/reference-semantics/` have exactly the same 25-entry recursive
  manifest. Every entry has the same kind and bytes; neither tree contains a
  symlink or unsupported node. Both independently hash to
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
  under the pipeline tree algorithm.

The generation transcript, prior `#Top`, and final `KPROVE_PASSED` marker were
read only as historical claims. The trace shows that the generator added two
summary rules and eventually obtained `#Top`; none of that was used as proof
of legitimacy.

Evidence:

- `evidence/integrity.log`
- `evidence/trace-inventory.log`
- `evidence/trace_inventory.py`
- `evidence/integrity_check.py`

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks for `will_it_fly(q, w)` to return true exactly when:

1. `q` is balanced, meaning that it is a palindromic list; and
2. the sum of its elements is at most `w`.

The trusted canonical implementation first rejects `sum(q) > w`, then compares
elements from the two ends. The candidate implementation is:

```python
def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w
```

The algorithms differ but are equivalent on finite integer lists. The
candidate's Boolean `and` short-circuits the sum when the list is not
palindromic, which changes no result on ordinary integer inputs.

The natural and formal intended domain used for the verdict is arbitrary
finite integer lists and integer weights. It is unbounded in list length,
element magnitude, sign, total sum, and weight. The original Python signature
has no annotations, so the same Python code incidentally handles some Float and
Bool mixtures. Seven such cases were tested and agreed, but they are not
covered by the K entry claims. If the unannotated prompt is interpreted as
requiring every CPython-summable numeric mixture, the formal theorem is
narrower; this review treats the all-integer domain evidenced by every prompt
example and by the HumanEval arithmetic task as the material contract.

### Trusted regeneration

In scratch, the trusted translator regenerated `solution.mpy`. Submitted and
regenerated files both hash to
`7c0e0763451ba64ad5a942a7e0cf477e9755446d733bd21ae8221636efd7efa0`;
`cmp` exited 0. The same check succeeded for the candidate concrete harness.

### Independent differential test

`evidence/differential_test.py` imports only the trusted canonical Python entry
point and the submitted Python entry point. It does not import proof equations.
It checks:

- all four documented examples;
- empty, singleton, even/odd palindrome, and non-palindrome cases;
- `sum == w`, one below, and one above the branch boundary;
- negative values and weights;
- arbitrary-size Python integers;
- every list through length five over `[-2,2]`, with weights `[-8,8]`;
- 5,000 deterministic generated lists through length 30, each with thresholds
  around its sum and an additional random threshold;
- seven separately reported Float/Bool numeric cases.

Result: 86,423 integer cases, seven extended numeric cases, and zero
mismatches.

Evidence:

- `evidence/differential_test.py`
- `evidence/differential.log`
- `evidence/fidelity.log`

Differential testing is finite evidence of implementation equivalence, not a
replacement for the K proof.

## 3. Clean proof reconstruction

All candidate source artifacts needed for execution were copied into
`/tmp/audit-work/reconstruction`. No candidate-provided compiled definition or
cache was copied. The initial scratch check printed no `*kompiled*` directory.

The available tools are K v7.1.293. The fresh proof build command was:

```sh
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. The only Haskell build diagnostics were unused variables in two
trusted `str.k` rules.

The aggregate candidate command:

```sh
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`.

To ensure that one successful aggregate invocation did not conceal a claim,
each source claim was copied unchanged into a single-claim module and proved
separately:

| Claim module | Exit | Output |
|---|---:|---|
| `SPEC-BALANCED-WITHIN` | 0 | `#Top` |
| `SPEC-UNBALANCED` | 0 | `#Top` |
| `SPEC-OVERWEIGHT` | 0 | `#Top` |

The concrete definition was also freshly built from trusted supplied source:

```sh
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun regenerated-concrete-tests.mpy --definition audit-runtime-kompiled
```

Both commands exited 0. The final configuration had `.K`, an empty stack,
`noRet`, `NoExc`, and exit code 0. LLVM reported non-exhaustive fixed-semantics
functions in unused language areas; none is reached by this program.

As an operational comparison, the complete eight-case harness was also run
with a bridge-free Haskell definition and the candidate bridge-enabled Haskell
definition. The full final configurations were byte-identical, both hashing to
`f07face38f3b97ada5a1a83f5bdf9f7a4b36e492f8c7eb44872377b152e5a55f`.

Evidence:

- `evidence/reconstruction.log`
- `evidence/k/spec-balanced-within.k`
- `evidence/k/spec-unbalanced.k`
- `evidence/k/spec-overweight.k`

The clean reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

All three claims require `VS` to contain only K `Int` values and require
`W:Int`.

1. Balanced and within limit: if `VS == reverseVS(VS)` and
   `sumIntVS(VS) <= W`, the call returns `true`.
2. Unbalanced: if `VS != reverseVS(VS)`, the call returns `false`, for every
   integer `W`.
3. Balanced and overweight: if `VS == reverseVS(VS)` and
   `sumIntVS(VS) > W`, the call returns `false`.

These cases exhaust the integer domain: a finite sequence is either equal or
not equal to its reverse, and integer order partitions the balanced case into
`<=` and `>`. There is no length, magnitude, or non-negativity restriction.

### Actual body and binding

Every claim begins with:

```k
#loadAll(willItFlyModule)
~> Call(Name("will_it_fly"), list(VS), W)
```

It therefore executes module loading, function definition, name lookup,
left-to-right argument handling, parameter binding, the submitted return
expression, return state, frame pop, and cleanup.

`evidence/program_term_check.py` mechanically extracts and expands
`willItFlyModule`, `willItFlyResult`, and `willItFlyClosure` from the actual
candidate `verification.k`. Whitespace-normalized constructor terms show:

- the expanded module is exactly submitted `solution.mpy`;
- the prebound closure has exactly parameters `("q","w")`, the same return
  body, and defining scope 0.

The initial module-scope closure is overwritten by `#loadAll` with the same
closure; it does not substitute another implementation. The bare `list(VS)`
argument is the supplied semantics' documented representation for read-only
claim inputs. The function does not mutate `q`. Its reverse slice allocates one
fresh list, which is reflected by the claims' heap transition from empty to
location 0 containing `list(reverseVS(VS))`.

### Satisfiable states and ground substitutions

The independent witness script exhibits:

| Claim | `q` | `w` | Canonical | Candidate | Claimed |
|---|---|---:|---:|---:|---:|
| balanced/within | `[3,2,3]` | 9 | true | true | true |
| unbalanced | `[1,2]` | 5 | false | false | false |
| balanced/overweight | `[3,2,3]` | 1 | false | false | false |

Thus no entry precondition is contradictory.

### Body sensitivity

A fresh definition changed the actual executed body from `sum(q) <= w` to
`sum(q) < w`, while leaving an original `<=` obligation. The mutated definition
compiled successfully. Its proof exited 1 with `WarnStuckClaimState`; the
residual retained `mutantSumIntVS(VS) <Int W` under the assumption
`mutantSumIntVS(VS) <=Int W`. The theorem is therefore sensitive to the actual
body at the equality boundary.

Evidence:

- `evidence/program-pinning.log`
- `evidence/claim-witnesses.log`
- `evidence/program_term_check.py`
- `evidence/claim_witnesses.py`
- `evidence/body-sensitivity.log`
- `evidence/k/verification-body-mutant.k`
- `evidence/k/spec-body-mutant.k`

The claims are result-constraining and pin the real submitted MPY program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` lexically inventories every local source sentence in
trusted `reference-semantics/` and candidate `verification.k`, including its
complete collapsed text and attributes. It records:

- 1 configuration;
- 5 contexts;
- 234 syntax declarations;
- 709 rules.

The attribute inventory includes 47 priority rules, 35 `[concrete]` rules, 26
`[owise]` rules, 22 `[function,total,symbol,no-evaluators]` declarations, and
three additional `[function,total,symbol]` declarations. There are no
`[simplification]` rules and no `functional` declarations.

`evidence/rule-review.tsv` appends a disposition to every one of the 949
inventoried non-summary rows. Fixed-semantics rows are classified as reachable,
unreachable, or opaque fixed baseline; every candidate row is individually
classified. This grouping is legitimate in `SUPPLIED_SEMANTICS` mode because
the recursively identical trusted tree is the selected fixed semantics.
Unreachable fixed rules cannot contribute to claim closure. The reachable path
was additionally reviewed construct by construct below.

### Program construct map

| Submitted construct | Declaration/rule path |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | `syntax.k`; `core.k` module sequencing; `functions.k` definition/return/pop; `call.k` closure call |
| `Name("q")`, `Name("w")`, `Name("sum")` | `core.k` scoped lookup and `builtinsScope` |
| `BoolOp("and",...)` | `bool.k` head-only context and truthful short-circuit rules |
| list `==` | `operators.k` comparison evaluation/deref; `list.k` structural equality |
| `Subscript(..., Slice(...,-1))` | `subscript.k` object/bound evaluation, list allocation, `doSlice`, and slice-index helpers |
| unary `-1` | `operators.k` unary dispatch; `int.k` integer negation |
| `Call(sum,q)` | `call.k` callee and argument evaluation, builtin binding/dispatch |
| integer sum fold | `builtins.k` `#sumAcc/#sumCont`; `iter.k`; `list.k` iterator rules |
| integer `<=` | `operators.k` comparison dispatch; `int.k` comparison |

Evaluation order is preserved. The palindrome comparison always runs first.
The sum call runs only on the truthy palindrome branch. Slice construction
allocates before list comparison. Calls bind the closure selected by ordinary
name lookup; no proof rule intercepts source-level `Call`, lookup, binding,
return, or frame pop.

### Candidate-local declarations and rules

1. `allInts` (one declaration, three equations) is a structurally recursive
   predicate. Empty, Int-head, and guarded non-Int-head cases cover its uses.
   The latter two are disjoint because of `notBool isInt(V)`. It terminates on
   the sequence tail.
2. `sumIntVS` (one declaration, two equations) is the ordinary mathematical
   sum on Int sequences and descends on the tail. The equations are truthful
   for every entry use. The `[total]` attribute is globally over-broad because
   no non-Int-head equation exists. A direct non-Int probe did not rewrite to
   the proposed value. This is recorded as a coverage concern, not an unsound
   entry-domain conclusion.
3. `snocVS` and `reverseVS` (two declarations, four equations) are exhaustive
   structural functions. Guards are unnecessary, rules do not overlap
   inconsistently, and recursion descends on a finite sequence.
4. The `doSlice` priority rule is an operational bridge over exactly
   `list(VS)[::-1]`. Under fixed semantics this evaluates to
   `buildVS(VS, len(VS)-1, -1, -1)`, which visits indices from the last through
   zero. Structural induction gives exactly `reverseVS(VS)`. It is correct for
   arbitrary `Val` elements, including references, because a slice copies
   element values without inspecting them. The rule reads or writes no cell;
   the surrounding fixed slice rule still performs the fresh allocation.
   Priority 40 only chooses the equivalent function equation sooner.
5. The `#sumAcc(list(VS),0)` priority rule is an operational bridge guarded by
   `allInts(VS)`. Fixed execution repeatedly invokes the list iterator, adds
   each Int to the accumulator, and returns zero for empty input. That is
   exactly `sumIntVS(VS)`. Neither fixed nor accelerated execution reads or
   changes any non-`k` cell, and neither has an exception path for Int
   elements. The candidate rule accepts an arbitrary continuation through
   `...`; fixed execution also returns the same value into that continuation,
   with no abrupt control effect.
6. `willItFlyResult`, `willItFlyModule`, and `willItFlyClosure` are fresh,
   terminating definitional aliases. Mechanical expansion proves that they
   contain the submitted term. They do not summarize the requested answer and
   do not introduce an oracle.

There are no proof-local opaque symbols, simplification rules, claims, or
answer-encoding rules.

### Bridge validation

A fresh bridge-free definition imports `MPY` and only independent structural
math functions. Its evidence establishes:

- fixed semantics closes ground reverse-slice claims for empty, singleton,
  three-element, and mixed-Val sequences, plus ground sum claims (`#Top`);
- the opposite reverse interpretation `[1,2] -> [1,2]` fails, leaving
  `[2,1]`;
- the opposite sum interpretation `sum([1,2]) -> 4` fails, leaving `3`;
- a full eight-case fixed Haskell execution is byte-identical to the
  bridge-enabled execution.

The attempted universal bridge-free slice claim failed only on the symbolic
equality between fixed `buildVS` and structural reverse. The universal sum
attempt encountered a missing Haskell Float hook after exploring a Float branch
inconsistent with the all-Int intent. Neither is a false conclusion witness,
so neither rule is called unsound. They expose the absence of candidate-supplied
machine connection theorems and justify the `CONCERNS` status.

Evidence:

- `evidence/rule-inventory.tsv`
- `evidence/rule-review.tsv`
- `evidence/k_inventory.py`
- `evidence/classify_rule_inventory.py`
- `evidence/bridge-validation.log`
- `evidence/k/bridge-base.k`
- `evidence/k/bridge-connection-spec.k`
- `evidence/k/bridge-ground-spec.k`
- `evidence/k/bridge-ground-false-spec.k`
- `evidence/k/sum-ground-false-spec.k`
- `evidence/k/totality-gap-probe.k`

## 6. Fresh non-vacuity test

The audit-created `SPEC-VACUITY` changes the balanced-and-within result from
`true` to `false`. It is demonstrably false for the satisfying witness
`q=[3,2,3], w=9`, for which both Python implementations return true.

First:

```sh
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0 and printed the exact `kore-exec` invocation, establishing that the
mutation parses and builds against the definition.

The actual proof command exited 1 with `WarnStuckClaimState`. Its terminal
configuration has `<k> true </k>`, while the destination requires `false`,
under the retained satisfiable symbolic assumptions:

- `allInts(VS) == true`;
- `VS == reverseVS(VS)`;
- `sumIntVS(VS) <= W`.

This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

Evidence:

- `evidence/k/spec-vacuity.k`
- `evidence/nonvacuity.log`

The proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied `MPY` semantics plus the reviewed proof-local equations,
for every finite `VS` containing only K integers and every K integer `W`, the
exact submitted function satisfies:

```text
return == (VS is a palindrome and sum(VS) <= W)
```

The three claims establish that characterization by exhaustive cases. They
also preserve the specified environment, restore the empty call stack and
`noRet` state, leave `NoExc` and exit code 0, and account for the reverse
slice's fresh heap allocation.

This is partial correctness. It does not independently prove CPython
termination or all behavior outside the selected MPY subset, although the
finite-list operations used here are structurally terminating under the
reviewed equations.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover and builtin Int/Bool/Map/List/String equality theories | All symbolic execution and arithmetic | Standard unavoidable checker trust |
| Trusted mounted `py2mpy.py` | Source-to-MPY bridge | Acceptable; regenerated bytes equal the submitted MPY term |
| Trusted supplied `MPY` semantics | Calls, lookup, control, lists, allocation, slicing, sum | Required fixed baseline; candidate copy is exact; reachable path reviewed and freshly executed |
| `doSlice(...,-1) => reverseVS` bridge | Palindrome value and slice heap content | Mathematically correct; ground and complete-execution evidence pass; universal bridge-free K theorem absent |
| `#sumAcc(list(VS),0) => sumIntVS(VS)` bridge | Weight comparison on the palindrome branch | Mathematically correct on guarded all-Int domain; ground and complete-execution evidence pass; universal bridge-free K theorem absent |
| Bare `list(VS)` claim input | Representation of the function argument | Supplied semantics explicitly permits this for read-only claim inputs; this function performs no mutation |
| Trusted canonical Python | Differential oracle only | 86,430 finite cases support implementation/intent alignment; not part of the K proof |
| Integer-domain interpretation | Theorem scope | Covers arbitrary finite integer lists and weights; incidental Float/Bool generality of unannotated Python is tested but not formally claimed |

The supplied fixed definition contains these opaque proof-backend symbols:

- sorting: `sortVS`, `sortKeyVS`;
- float/conversion: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, `sqrtF`;
- digest: `md5hexCodes`.

None is reachable from the submitted integer program or its proof claims.
They therefore cannot affect a branch, result, state, exception, or
postcondition in this theorem. Candidate `verification.k` introduces no opaque
symbol.

### Final decision

The reconstructed theorem is non-vacuous, unrestricted over the intended
integer domain, result-constraining, body-sensitive, and mechanically pinned to
the real generated MPY program. The low-level bridge equations do not smuggle
the task answer and are true consequences of ordinary structural list
mathematics. Their missing universal machine connection proofs, together with
the over-broad `sumIntVS [total]` declaration, are genuine but non-fatal
auditability concerns. They do not make a false conclusion provable on the
entry domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
