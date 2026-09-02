# Independent adversarial audit: 146-specialFilter

This review treats every candidate artifact, prior log, trace, and `#Top` as
untrusted evidence. All execution used fresh source copies below
`/tmp/audit-work/146-specialFilter`; no candidate-built definition or cache was
copied or reused.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts are
consistent with the rendered mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all records required by the
declared layout:

- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL trace below `/generation-evidence/codex-trace`

I also inspected the present `usage.json`, `legacy-metrics.json`, and
`legacy-run-input.json`. The structured trace contains 502 valid JSON records,
111 tool calls, and 111 corresponding outputs. The generation record says the
candidate passed, but that statement was not used as proof evidence.

The independent integrity script and exact command/exit record are
[stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1-integrity.log](evidence/stage1-integrity.log). It established:

- the campaign-lock JSON object is exactly equal to the campaign block in
  `audit-input.json`;
- the campaign-lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly as recorded;
- every directly recorded hash for the canonical source, prompts, translator,
  run/task/result manifests, invocation, metrics, usage, generation prompt,
  final text, output log, and trace file matches the mounted bytes;
- every evidence-entry hash listed by both `generation-result.json` and
  `invocation.json` matches;
- candidate `prompt.py` is byte-identical to `/reference/prompt.py`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- the candidate and trusted supplied-semantics inventories are identical:
  one directory and 24 regular K files, with identical SHA-256 for every file;
- neither semantics tree contains a symlink, special entry, missing entry, or
  extra entry. No candidate or generation-evidence entry is a symlink or
  special file.

The generation trace was parsed in full by
[generation_trace_inventory.py](evidence/generation_trace_inventory.py); its
bounded action inventory and exit status are in
[generation-trace-inventory.log](evidence/generation-trace-inventory.log).

Stage 1 result: **PASS**. There is no audit-infrastructure breach, so a
candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of integers, return the number of elements that are greater
than 10 and whose first and last decimal digits are both members of
`{1, 3, 5, 7, 9}`. The two documented examples return 1 and 2.

The trusted canonical function converts each qualifying positive integer to
decimal text, converts its first and last characters back to integers, and
tests membership in the odd-digit tuple. The candidate uses the equivalent
character test `digits[0] in "13579" and digits[-1] in "13579"`. Because the
test is reached only when `num > 10`, the representation is positive and has
at least two characters.

Running the trusted translator on the scratch copy produced a byte-identical
`solution.mpy`. Both files have SHA-256
`d3d8c79a12490216fd14e7573efbd7abb0031ed6ae1ae9e4bd8a269df68ff113`.
The exact command, `cmp`, hashes, and exit 0 are in
[translation-identity.log](evidence/translation-identity.log).

The independent differential test
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and candidate functions independently. It covered:

- both documented examples;
- empty input and the `10`/`11` threshold;
- leading- and trailing-digit branch boundaries;
- negatives, zero, one- and multi-digit integers;
- every singleton integer from -250 through 5000;
- 2,000 seeded random lists of length 0 through 64 with integers drawn from
  `[-10^30, 10^30)`.

It reported `total_cases=7274 mismatches=0`; command and exit 0 are in
[differential-test.log](evidence/differential-test.log).

Stage 2 result: **PASS** for implementation fidelity on the intended finite
integer-list domain. The candidate algorithm itself agrees with the canonical
implementation.

## 3. Clean proof reconstruction

The installed tools are independently reported as K v7.1.293 in
[k-toolchain.log](evidence/k-toolchain.log).

### Concrete definition and execution

I built the trusted supplied semantics from source:

```sh
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0; see [llvm-build.log](evidence/llvm-build.log). The warnings are
the supplied semantics' known non-exhaustive total-function warnings and do
not involve the operations exercised here.

The reviewer-authored concrete program
[concrete_audit.py](evidence/concrete_audit.py) contains the exact candidate
function body followed by empty, threshold, odd/even endpoint, mixed, and
prompt-example assertions. Translation followed by

```sh
krun concrete_audit.mpy --definition audit-runtime-kompiled --output pretty
```

exited 0 with `<exc> NoExc </exc>` and `<exit-code> 0 </exit-code>`; see
[concrete-krun.log](evidence/concrete-krun.log).

Two earlier reviewer test oracles incorrectly expected 5 where the correct
answer was 4 and then 2 where the correct answer was 1. The semantics rejected
both with `AssertionError`. Those mistakes are transparently preserved in
[concrete-krun-initial-reviewer-oracle-error.log](evidence/concrete-krun-initial-reviewer-oracle-error.log)
and
[concrete-krun-second-reviewer-oracle-error.log](evidence/concrete-krun-second-reviewer-oracle-error.log);
they are reviewer errors, not candidate defects.

### Positive proof targets

The universal loop definition was freshly built with:

```sh
kompile verification.k --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-loop-kompiled
```

The build exited 0
([loop-build.log](evidence/loop-build.log)). Then:

```sh
kprove spec.k --definition audit-loop-kompiled \
  --spec-module SPECIALFILTER-LOOP-SPEC
```

exited 0 and printed `#Top`
([loop-proof.log](evidence/loop-proof.log)).

The derived-summary/entry definition was independently built with:

```sh
kompile verification.k --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The build exited 0
([entry-build.log](evidence/entry-build.log)). Then:

```sh
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPECIALFILTER-SPEC
```

exited 0 and printed `#Top`
([entry-proof.log](evidence/entry-proof.log)).

Stage 3 result: **PASS**. Every submitted positive claim reconstructs from
source and closes. This proves closure under the submitted theory; it does not
by itself establish that the theory states the required end-to-end theorem.

## 4. Adequacy and real-program pinning

### Plain-language claim restatement

`specialfilter-loop-correct` starts at an internal `#loop` over a
proof-specific `list(intVals(NS))`. The current environment is local scope 1.
That scope contains an original `nums` value `list(intVals(ALL))`, arbitrary
integer `count = C`, prior integer `num = OLDNUM`, and prior string
`digits = OLDDIGITS`. The module scope must not shadow `str`; the builtin scope
must bind `str` to `typeV("str")`. The postcondition removes the loop from
`<k>`, adds `specialCount(NS)` to `count`, assigns the final iterated element
to `num` when one exists, and assigns the decimal text of the last element
greater than 10 to `digits` when one exists.

`specialfilter-empty-call-correct` starts at a direct application of a closure
whose parameter and complete function body are the candidate macros, but the
argument is fixed to `list(intVals(.IntSeq))`. It requires a fresh call-frame
state and a valid builtin `str` binding. Its postcondition is the concrete
return value 0 with the caller frame restored. It is an empty-input call
claim, not an arbitrary-input call claim.

Both preconditions are satisfiable. For the loop claim, choose
`NS = ALL = .IntSeq`, `C = OLDNUM = 0`, an empty string for `OLDDIGITS`, an
empty global map, and a root builtin map containing
`"str" |-> typeV("str")`. For the call claim, use its written empty maps,
fresh locations, empty stack/heap, `NoExc`, and the same builtin binding.

Concrete substitution is consistent where the formal result can be checked:

- empty input gives 0 in the claim, candidate Python, canonical Python, and
  concrete K;
- `specialCount(iCons(11, .IntSeq)) => 1` closes under the proof definition
  ([ground-result-spec.k](evidence/ground-result-spec.k),
  [ground-result-proof.log](evidence/ground-result-proof.log)), agreeing with
  both Python functions and concrete K;
- both prompt examples agree in the differential and concrete runs.

An initial bare functional version of that ground probe was rejected because
this Haskell backend does not support bare functional claims. It is preserved
as
[ground-result-proof-initial-unsupported-functional-claim.log](evidence/ground-result-proof-initial-unsupported-functional-claim.log)
and was replaced by the valid `<k>`-cell claim above.

### Constructor identity and body sensitivity

Using the freshly compiled definition, I parsed both regenerated
`solution.mpy` and `#specialModule` as sort `Module`, expanded macros, emitted
JSON KAST, and compared the results. They are byte-identical, with SHA-256
`47455fe5689e076d31bc68e88cc5777227d421dce986ece7625b950f8f76b462`.
The exact commands and exit 0 are in
[constructor-identity.log](evidence/constructor-identity.log). Thus the three
body macros are not a substituted function body.

I also changed the threshold in the term actually executed by the loop claim
from 10 to 100. The mutant
[verification-body-mutant.k](evidence/verification-body-mutant.k) built
successfully ([body-mutant-build.log](evidence/body-mutant-build.log)), but
the original loop specification failed with `WarnStuckClaimState` and a
residual contrasting `N > 10` with `N > 100`
([body-mutant-proof.log](evidence/body-mutant-proof.log)). The loop theorem is
sensitive to the submitted body.

### Material adequacy failure

Despite exact body identity, no positive claim proves an arbitrary call of
that body:

- the only full closure/call/parameter-binding/return claim fixes the argument
  to the empty list;
- the arbitrary-length claim starts after call entry, parameter binding, the
  three initial assignments, and `For` lowering, at an internal `#loop`;
- that loop ranges over the fresh proof constructor `intVals(IntSeq)`, not the
  supplied semantics' actual `.ValSeq`/`vCons` representation;
- there is no bridge-free reachability theorem connecting an arbitrary real
  `list(vCons(...))` argument and full function entry to the internal
  `list(intVals(NS))` loop state, nor a submitted arbitrary-entry claim that
  composes the loop result with return/frame restoration.

The loop theorem is useful, arbitrary-length proof progress, and the missing
prefix/suffix are intuitively simple. But the benchmark requires a
machine-checked partial-correctness proof whose entry precondition covers the
source-contract domain. An empty-call smoke theorem plus an internal theorem
over a disjoint proof-only list constructor does not establish that end-to-end
claim. This is not the harmless absence of automatic source-to-proof
regeneration: regeneration and body identity succeeded. It is a material
theorem-domain and real-input-connection gap.

Stage 4 result: **FAIL** for end-to-end adequacy and real-program pinning over
the unrestricted finite integer-list domain.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated inventory is
[rule_inventory.py](evidence/rule_inventory.py) with complete output and exit
0 in [rule-inventory.log](evidence/rule-inventory.log). It enumerates every
module/import, configuration, syntax declaration, context, rule, attribute,
and claim with source line and full multiline text:

- supplied semantics: 1 configuration, 5 contexts, 227 syntax declarations,
  and 695 rules;
- candidate files: 14 syntax declarations, 20 rules, and 2 claims.

### Supplied semantics entries 0001-1064

These entries are byte-identical to the selected trusted supplied semantics.
They are classified as the fixed semantic level rather than candidate proof
extensions. I reviewed their root patterns and guards against all constructors
used by `solution.mpy`. Unused rules have disjoint root labels or guarded
operation names and cannot replace a used redex.

The used-construct map is:

| Program construct | Declaration and fixed execution |
|---|---|
| `Module`, statement sequence | `MPY-SYNTAX`; `#loadAll` and sequencing in `core.k` |
| `FuncDef`, closure application, parameter binding, return | `functions.k` and `call.k`; local scope allocation, stack push, `#bindP`, `#pop` |
| `Assign`, `AugAssign` | `controls.k`; current-scope map updates and integer `applyBin("+",...)` |
| `For` | `controls.k`; evaluates iterable once and lowers to `#loop/#iterNext/#loopStep` |
| `If` | `controls.k`; strict guard followed by `truthy` and `#branch` |
| `Name` | `core.k`; lexical parent lookup with local/global/builtin shadowing |
| integer/string literals and unary `-` | `core.k`, `str.k`, `operators.k`, `int.k` |
| integer `>` and `+` | operator dispatch in `operators.k`, cases in `int.k` |
| `str(num)` | callee and argument evaluation in `call.k`; builtin type binding and `applyBuiltin("str",...)` in `builtins.k` |
| string indexes `0` and `-1` | `subscript.k`; `normIdx`, `isLen`, and `intSeqAt` |
| character `in "13579"` | comparison routing plus `strContains` in `str.k` |
| short-circuit `and` | left-to-right `BoolOp` context/rules in `bool.k` |

The fixed rules preserve the relevant evaluation order. The call rule creates
and removes a local scope and stack frame. The program mutates only local
bindings. Decimal strings and one-character subscripts are values, so the
program has no heap allocation, output, or modeled exception effect on the
proved `num > 10` path. The `str`-binding guards exclude local/global
shadowing and require the builtin type object.

The concrete compiler warns that several unrelated supplied total functions
are not exhaustive. None is reached by this program. The used `intSeqAt` is
safe in fixed concrete execution because `num > 10` ensures a nonempty
multi-digit decimal string. I found no supplied-rule overlap that gives a
false conclusion for this program.

### Candidate entries 1065-1115

Every candidate extension is classified below.

1. **Three syntax macros and three macro rules** (`#specialElementBody`,
   `#specialFunctionBody`, `#specialModule`): constructor aliases only.
   Macro expansion is exactly the regenerated module, as shown by the KAST
   identity check. They neither replace an operation nor add an answer.

2. **Three opaque decimal symbols** (`decimalCodes`, `decimalLength`,
   `decimalCodeAt`): fresh `[function, total, symbol, no-evaluators]`
   declarations. Their values affect both string-index branches and ultimately
   `specialCount`.

3. **Three simplification rules**:
   `strToCodes(Int2String(N)) => decimalCodes(N)`,
   `isLen(decimalCodes(N)) => decimalLength(N)`, and
   `intSeqAt(decimalCodes(N), I) => decimalCodeAt(N, I)`. These are symbolic
   aliases for fixed terms that the Haskell backend cannot reduce on symbolic
   integers. They have no pairwise right-hand-side disagreement, and the last
   two match only the fresh `decimalCodes` term. The first bypasses fixed
   symbolic `Int2String` evaluation and is result-bearing.

   No bridge-free universal connection theorem is submitted. That is a
   validation limitation. I did not label the rules unsound because I found no
   false-conclusion witness. In particular, I supplied the opposite ground
   interpretation `decimalCodes(_) = .IntSeq`,
   `decimalLength(_) = 0`, and `decimalCodeAt(_,_) = 48`. It built, but the
   false full-call claim `specialFilter([11]) => 0` was rejected; the residual
   concrete result was 1. See
   [wrong-oracle-verification.k](evidence/wrong-oracle-verification.k),
   [wrong-oracle-spec.k](evidence/wrong-oracle-spec.k),
   [wrong-oracle-build.log](evidence/wrong-oracle-build.log), and
   [wrong-oracle-proof.log](evidence/wrong-oracle-proof.log). Ground hook
   evaluation fixes that case. The narrower finding is absence of the required
   universal connection evidence, not demonstrated logical falsity.

4. **Transparent mathematical summaries**:
   `decimalString`, `hasOddEndDigits`, `boolAsInt`, `specialBit`,
   `specialCount`, `finalNum`, and `finalDigits`. Their 11 equations are
   structurally recursive or exhaustive on their stated constructors.
   `boolAsInt` covers both booleans; the three `IntSeq` folds have disjoint
   empty/cons cases and descend on the tail. `specialBit` exactly applies the
   threshold before the endpoint predicate. These functions describe the
   postcondition; they do not rewrite the program control term.

5. **`intVals` and its two iterator rules**: `intVals(IntSeq)` is a fresh
   proof-only `ValSeq` representation. Its empty and cons iterator rules are
   disjoint and faithfully implement base/step iteration if `intVals` is
   assumed to represent integer-valued Python lists. But fixed semantics would
   otherwise be stuck on this fresh constructor, and the candidate supplies no
   theorem connecting it to `.ValSeq`/`vCons`. This is an operational
   representation bridge and the principal real-input pinning gap. I found no
   false per-step conclusion under the intended representation; the defect is
   missing universal connection and exclusion of actual list constructors
   from the theorem's precondition.

6. **Loop-state summaries**: `specialCount`, `finalNum`, and `finalDigits`
   match the three local writes performed by the exact loop body. The
   `ALL`/`NS` split is sound: `ALL` preserves the original `nums` binding while
   `NS` denotes the remaining iterator.

7. **Derived loop rewrite at priority 40**: its LHS, RHS, guards, environment,
   exact empty continuation, and scope footprint are the same as the
   independently successful loop claim. It cannot match an arbitrary
   continuation because the `<k>` cell is exactly the loop term, not
   `loop ~> CONT`. It reads/writes only the cells stated by its proving claim;
   other configuration cells are framed identically. Priority makes the
   proved summary preempt fixed unrolling but does not broaden its match
   domain. As an operational bridge, it is justified within the
   `intVals`/decimal-extension theory by
   [loop-proof.log](evidence/loop-proof.log). Its submitted dependent is only
   the empty-call claim.

8. **Two reachability claims**: both are result-constraining and satisfiable.
   The loop claim is arbitrary in `IntSeq`; the call claim is fixed to empty.
   Their scope mismatch with the requested arbitrary entry theorem is
   addressed in Stage 4.

I found no candidate rule for which a concrete or symbolic false conclusion
witness was established. Therefore this review does not use an unsupported
"unsound rule" allegation. The fatal finding is theorem adequacy and missing
real-input/entry connection, with an additional universal-evidence limitation
around the symbolic aliases.

Stage 5 result: **no witnessed rule inconsistency**, but **FAIL** at the
real-program connection obligation.

## 6. Fresh non-vacuity test

The fresh mutation
[spec-vacuity.k](evidence/spec-vacuity.k) changes the loop postcondition from
`C + specialCount(NS)` to the deliberately false
`C + specialCount(NS) + 1`. It imports the original source-built loop
definition and has a concrete satisfying witness at `NS = .IntSeq`, `C = 0`
with the scope/builtin choices given in Stage 4.

The exact command was:

```sh
kprove spec-vacuity.k --definition audit-loop-kompiled \
  --spec-module SPECIALFILTER-FRESH-VACUITY-SPEC
```

The mutated specification parsed and built, then exited 1 with
`WarnStuckClaimState`. The residual is the expected unmet implication
`C = C +Int 1` on the empty branch, not a parser error, missing import,
timeout, or unrelated crash. Full bounded output and exit status are in
[non-vacuity-proof.log](evidence/non-vacuity-proof.log).

Stage 6 result: **PASS**. The loop claim is non-vacuous and constrains its
summarized result.

## 7. Proven versus assumed accounting

### What the successful K proofs establish

Under the trusted supplied MPY semantics plus the candidate's proof-local
decimal aliases and `intVals` iterator rules:

1. an internal loop already positioned at
   `#loop(list(intVals(NS)), Name("num"), #specialElementBody)` transforms
   `count`, `num`, and `digits` according to `specialCount`, `finalNum`, and
   `finalDigits` for arbitrary finite `NS`; and
2. a direct closure call of the exact candidate function body returns 0 for
   the single argument `list(intVals(.IntSeq))`, restoring the modeled call
   frame.

The proofs do **not** state or close the required theorem that an arbitrary
finite real Python integer-list argument passed to the exact function returns
the contract count.

### Trust and assumption ledger

| Boundary | Influence | Evidence and judgment |
|---|---|---|
| Supplied MPY semantics | All execution, state, calls, and results | Trusted selected semantic level; candidate tree is byte-identical. Concrete and symbolic definitions rebuilt. |
| K integer/string hooks, especially `Int2String`, `ordChar`, substring and length hooks | Decimal rendering and endpoint characters | Low-level implementation trust inherited from supplied K/builtin semantics. Ground `[11]`, boundaries, examples, and broader Python differential agree. |
| `decimalCodes`, `decimalLength`, `decimalCodeAt` and three simplification aliases | Symbolic branch choice and `specialCount` | No bridge-free universal theorem. Opposite ground interpretation did not admit the false `[11] => 0` result. Concerning evidence limitation, not a witnessed false rule. |
| `intVals` and its two iterator rules | Entire arbitrary-list loop domain | Informal representation map only; no machine-checked connection to fixed `.ValSeq`/`vCons` list inputs. Material pinning limitation. |
| Derived priority-40 loop rule | Skips loop execution in its exact empty-continuation context | Exact duplicate of the independently proved loop reachability claim, with matching cells and guards. Acceptable only within the proof-local representation theory. |
| Macro/source identity | Whether the theorem uses the submitted body | Mechanical expanded-KAST equality and body-sensitivity mutation. Strong evidence. |
| Python differential and LLVM assertions | Implementation/canonical and concrete-semantics bridges on tested inputs | Reproducible finite evidence only; not a universal K connection theorem. |
| Composition from arbitrary source call to internal loop and back to return | Required end-to-end theorem | Not submitted or machine-checked. Only empty input is composed. Fatal scope gap. |

Gate summary:

- **Real-program soundness/pinning (Gate A): FAIL.** Body identity,
  result sensitivity, and the exact loop summary pass, but the proof has no
  arbitrary real-list entry theorem or universal `vCons`/`intVals` connection.
- **Intent adequacy (Gate B): FAIL.** The only full call theorem fixes one
  list size (empty), materially narrowing the unrestricted finite-list source
  contract.
- **Evidence auditability (Gate C): partial.** All claimed builds, proofs,
  mutations, hashes, and differential checks in this audit are reproducible,
  but the symbolic decimal and list-representation bridges lack universal
  connection theorems.

The reconstructed `#Top` results are genuine for the two submitted claims, and
the loop claim is meaningful proof progress. Nevertheless, the candidate does
not contain the required end-to-end partial-correctness theorem over the real
source-contract domain. Under the benchmark's explicit mapping, a
sound-but-limited theorem that materially narrows the HumanEval domain is
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
