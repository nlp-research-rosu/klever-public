# Independent adversarial review: 67-fruit-distribution

## Outcome

The candidate contains a legitimate partial-correctness proof of its real
generated program. I independently rebuilt the supplied semantics and proof
definition, reran the only positive candidate claim, obtained exit 0 with
`#Top`, mechanically pinned the claim's closure to the regenerated
`solution.mpy`, exhibited a satisfying ground state, and made fresh body and
result mutations fail at the expected reachable results.

I record `CONCERNS / LEGIT`, rather than an unqualified pass, for three
non-fatal boundaries: the exact five-token ASCII phrase domain is inferred
from the examples rather than completely spelled out in the prose; the fixed
MPY semantics intentionally models only a subset of CPython whitespace/string
behavior; and the source/translator/MPY-to-CPython bridge has finite
differential evidence rather than a universal equivalence theorem. These
limitations do not enable a false result for any state satisfying the entry
claim, and they do not materially bound fruit counts, string length, or total
size.

## 1. Input and provenance integrity

Infrastructure gate: **PASS**. The rendered mode is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is present as
required. No launcher-owned input or required pipeline-v3 record is missing,
unreadable, mistyped, or symlinked, so this is a candidate audit rather than
an `AUDIT_ERROR`.

I first read `/audit-input.json`. It declares `record_layout` `pipeline-v3`,
problem `67-fruit-distribution`, condition `kit-semantics`, and the container
paths used in this audit. I then read:

- `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 212 JSONL records in the single structured trace below
  `/generation-evidence/codex-trace/`.

The generation reports and candidate prose were treated only as claims. The
trace inventory records 43 tool calls and all event/payload classes, including
the generation-time K commands and mutations, but none of those reported
outcomes was reused as proof evidence.

The campaign lock JSON object is exactly equal to the `audit_campaign` block in
`/audit-input.json`, and its independently computed SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every directly declared file hash also matches, including:

- canonical:
  `5cc8f3ee9f26d78e5a6a511de09e1121ffff19365398abb8c0a77c32cbfdccde`;
- trusted/candidate prompt:
  `287ace00706dbc14460387cbd37396f40de3816fb26bd13182cec8a85fd6dddb`;
- trusted/candidate translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- run, task, and generation-result manifests:
  `3b99df...`, `26d593...`, and `702bd4...`;
- invocation, generation metrics, runtime metrics, and usage:
  `542430...`, `31ed38...`, `028513...`, and `2d2e61...`;
- generation prompt, last message, and output log:
  `c5f7af...`, `f1a395...`, and `bb7583...`.

I reimplemented the pipeline-v3 length-delimited tree digest rather than
trusting the declared integrity booleans. The mounted candidate tree hashes to
`da5bfe81a9872a8dfd9278d266705aa2075dc16da2f17efc21418ee6356f933e`,
matching both the invocation and stage result. The trusted and candidate
semantics trees independently hash to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task manifest. The structured trace tree hashes to
`aeea3b1d4e12d6b8a826098032631e8e6076a662e4cd8cfcf152182f2a07a842`,
matching `usage.json`; its only JSONL file separately matches the recorded
`d110a3...` hash.

The recursive supplied-semantics comparison covers 25 entries. Candidate and
trusted paths, entry types, and bytes are identical; there are no missing,
additional, changed, or symlinked entries. The candidate tree as a whole has
782 real file/directory entries and no symlink or special entry. Its required
proof artifacts are regular files. The prompt and translator are byte
identical to their trusted versions.

Reproducible evidence:
`evidence/stage1_integrity.py`, `stage1_integrity.log`,
`trace_inventory.py`, and `trace_inventory.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract asks for the number of mangoes in a basket when `s`
describes the apple and orange counts and `n` is the total fruit count. All
four prompt examples have the form:

```text
<nonnegative number> apples and <nonnegative number> oranges
```

and the intended result is:

```text
n - apples - oranges
```

The trusted canonical scans every whitespace-separated token, converts every
token for which CPython `str.isdigit()` is true, and subtracts their sum from
`n`. The submitted implementation instead parses positions 0 and 3:

```python
def fruit_distribution(s, n):
    return n - int(s.split()[0]) - int(s.split()[3])
```

That is a different algorithm but agrees with the canonical on the prompt's
well-formed phrase grammar.

Using the trusted `/reference/py2mpy.py` from the scratch workspace regenerated
`solution.mpy` with SHA-256
`280a1b9812a03c3679da3bf6dd8dc7be48f2c78769ec1a5ce6ff7b1ba73a5902`.
It is byte-for-byte identical to `/candidate/solution.mpy`.

The independent differential script imports the trusted canonical and
submitted entry points through separate module loaders. It covers all four
examples; zero counts; `n = apples + oranges`; large integers; leading,
trailing, repeated, tab, and newline whitespace; Unicode decimal digits; and
a 147-case generated valid grid. Across 157 format-valid cases it reports zero
mismatches.

Six deliberately excluded probes were also recorded. Five expose real
canonical/submitted divergences: empty input, a missing number, free prose
before the counts, a signed count, and an extra unrelated numeric token. The
sixth, a total smaller than the two stated counts, returns the same negative
value in both implementations. The five divergent strings are not instances
of the demonstrated five-token basket phrase; nevertheless, because the prose
does not give a formal grammar and the canonical is more permissive, this is a
non-fatal intent-boundary concern. It would become a material defect if the
contract were interpreted to require arbitrary prose or malformed-input
behavior. Under the examples' conventional HumanEval domain, it is not a
material narrowing.

Evidence:
`evidence/differential_test.py`, `differential_test.log`, and
`translation_regeneration.log`.

## 3. Clean proof reconstruction

Dynamic reconstruction gate: **PASS**.

I copied only source artifacts into `/tmp/audit-work/fruit67`: candidate
`solution.py`, `solution.mpy`, `spec.k`, and `verification.k`, plus the trusted
translator, prompt, canonical, and trusted reference-semantics tree. I did not
copy or use `/candidate/runtime-kompiled`,
`/candidate/verification-kompiled`, `__pycache__`, or any candidate cache/log.

The independently observed tools are K `v7.1.293`. Fresh definitions were
built with:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exit statuses are 0. Compiler warnings concern unused variables and
known non-exhaustive `total` symbols; no build error occurred.

The reviewer-authored concrete MPY program exercises all examples plus
zero/equality, whitespace, and large-count boundaries. Fresh LLVM execution:

```bash
krun concrete_audit.mpy --definition concrete-kompiled
```

exits 0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0.

Lexical candidate-claim inventory finds exactly one positive target,
`SPEC.fruit-distribution`. Fresh proof:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

prints exactly one `#Top` and exits 0. That is the required positive proof
closure; no candidate trace or prior compiled result was used.

Evidence:
`evidence/tool_versions.log`, `kompile_llvm.log`, `krun_concrete.log`,
`kompile_haskell.log`, `positive_claim_inventory.log`, and
`kprove_positive.log`.

## 4. Adequacy and real-program pinning

Pinning and result-constraint gate: **PASS**.

### Plain-language claim

The initial state calls a closure with parameters `s,n`, the submitted nested
subtraction body, defining environment 0, string value `str(CS)`, and integer
`N`. The caller has the standard empty module scope, fixed builtin parent,
empty heap/stack, no pending return or exception, and exit code 0.

The precondition says:

1. fixed MPY whitespace splitting of `CS` is exactly five tokens:
   `APPLECODES`, `"apples"`, `"and"`, `ORANGECODES`, `"oranges"`;
2. both count tokens are nonempty sequences of ASCII digits;
3. fixed MPY `int` conversion maps them to `APPLES` and `ORANGES`;
4. both counts are nonnegative; and
5. `N >= APPLES + ORANGES`.

The postcondition requires the returned `<k>` value to be exactly
`N - APPLES - ORANGES`. It also restores environment 0, the original two
scopes, scope location 1, empty stack, `noRet`, `NoExc`, and exit code 0. The
two temporary lists allocated by the two `split()` calls make final heap and
heap location existential. That abstraction does not weaken the result or any
HumanEval-observable state.

### Mechanical identity

The claim does not execute the module wrapper or look up
`fruit_distribution` by name. This is permitted only if it invokes the exact
closure that loading the regenerated module would bind. The fixed rule at
`semantics/functions.k:14` maps
`FuncDef(F, Params(PNS), BODY)` in environment `L` to
`F <- closureVal(PNS, BODY, L)`.

`evidence/program_term_compare.py` parses the regenerated constructor text and
the entry-claim closure independently. After normalizing only K list
terminators (`.Exprs`, `.Stmts`) and the `Params`/`ParamNames` representation,
the parameter trees and complete `Return` expression trees are identical. The
normalized closure digest is
`6142704e68bf78ac39de50b9369ce271a0d9fcf8d1aeeb3a6710c33f7b37b4b6`.
The compared body includes both actual `split()` calls, both indices, both
`int` calls, and both subtractions.

### Satisfying state and concrete substitution

The state:

```text
s = "5 apples and 6 oranges"
N = 19
APPLECODES = (53)
ORANGECODES = (54)
APPLES = 5
ORANGES = 6
```

satisfies every entry guard. The claimed result is `19 - 5 - 6 = 8`; both
trusted canonical Python and submitted Python return 8.

A separate ground K claim starts from the exact closure/state and proves the
result 8 with exit 0 and `#Top`. This validates satisfiability inside the fixed
K model rather than only in Python.

Finally, a reviewer-authored body-sensitivity claim changes the executed
outer operation from subtraction to addition while retaining target 8. It
parses, reaches actual `<k> 20 ~> .K`, emits `WarnStuckClaimState`, and exits
1. Thus body sensitivity changes the term actually executed by the claim; it
is not a mutation of an ignored external `solution.py`.

Evidence:
`evidence/program_term_compare.py`, `program_term_compare.log`,
`precondition_witness.py`, `precondition_witness.log`, `ground-witness.k`,
`kprove_ground_witness.log`, `body-sensitivity.k`, and
`kprove_body_sensitivity.log`.

## 5. Rule-by-rule static soundness review

Static rule gate: **PASS on the claimed domain**, with the documented fixed
semantics limitations below.

`evidence/rule_inventory.tsv` exhaustively inventories and hashes every local
sentence in `semantics.k`, all 23 helper K files, `verification.k`, and
`spec.k`. Each row has a source span, kind, role, attributes, normalized hash,
assessment, and rationale. Totals are:

- 1 configuration;
- 227 local syntax statements;
- 5 contexts;
- 695 ordinary semantic/equational rules;
- 1 target claim;
- 145 function-bearing declarations;
- 107 `total` declarations;
- 25 `symbol` declarations and 22 `no-evaluators` declarations;
- 35 concrete sentences, 45 priority-bearing sentences, and 26 `owise`
  sentences;
- no `functional`, `simplification`, alias, candidate-local opaque, or
  proof-local rule.

The module-by-module disposition is in `evidence/static_review.md`, and the
complete mapping from every constructor in `solution.mpy` to declarations and
rules is in `evidence/used_construct_map.md`.

### Candidate-local proof theory

`verification.k` only imports `MPY`. It defines no syntax, function, totality
claim, opaque symbol, priority, simplification, concrete rule, ordinary
rewrite, lemma, auxiliary claim, or operational bridge. Therefore there is no
candidate-added rule that can encode the fruit answer, bypass the program, or
smuggle an unconstrained result.

### Reachable rule path

The fixed path executes:

1. closure application and a new call frame;
2. parameter binding;
3. strict/left-to-right nested subtraction;
4. `Name` lookup for `n`, `s`, and fixed builtin `int`;
5. receiver evaluation and bound-method creation for each `split`;
6. fixed recursive `splitWS` and real heap allocation;
7. heap dereference and in-bounds indexing at 0 and 3;
8. fixed single/multi-digit decimal conversion;
9. fixed integer subtraction;
10. return, frame pop, and restoration of caller control cells.

The configuration, binding, evaluation order, priorities, allocation, stack,
return, exception, and exit-code effects are preserved. No rule in an
unrelated module becomes reachable by symbolic narrowing on this fully typed
path.

### Fixed-semantics limitations and witnesses

The static review found no false conclusion enabled for a state satisfying the
entry claim. It did find these explicit trust/domain boundaries:

- `applyBuiltin("int", str(CS), .Vals)` for length at least two does not carry
  its own digit guard. On the excluded value `"AA"`, fixed MPY computes 187,
  whereas CPython raises `ValueError`. This is a concrete false-behavior
  witness for the globally over-broad fixed rule, not a false theorem witness:
  `"AA"` cannot satisfy the claim's nonempty `allDigit` guards.
- `valSeqAt` is `[total]` but intentionally underspecified out of bounds.
  Exact five-token splitting makes positions 0 and 3 constructor-provably in
  bounds, so no opposite value is admitted on the claim domain.
- `isWSC` models space, tab, LF, and CR rather than the entire CPython Unicode
  whitespace class. This narrows edge strings but does not fabricate a result
  for any string admitted by the formal split predicate.
- float operations, symbolic sort, keyed sort, and MD5 include fixed opaque
  proof-domain symbols. None is reachable from this program, so none can
  influence a branch, state cell, result, or postcondition here.
- `MPY-CONCRETE` contains 16 LLVM-only rules and is imported by `MPY-KRUN`,
  not by `VERIFICATION`; those rules cannot contribute to `#Top`.

The used recursive equations have structural descent. Used overlaps are
guard/sort disjoint or have agreeing right-hand sides. Repeated mixed-float
rules elsewhere have identical conclusions and are unreachable. The relevant
priority rules only distinguish heap references and exact call forms. No
unsound rule on the intended entry domain was found, so there is no required
false-conclusion witness against the target.

## 6. Fresh non-vacuity test

Non-vacuity gate: **PASS**.

I did not reuse candidate `spec-vacuity.k`. The fresh
`evidence/false-result.k` fixes the satisfying ground input
`"5 apples and 6 oranges", 19`, executes the correct submitted closure, and
changes only the required result from 8 to 9.

First:

```bash
kprove false-result.k \
  --definition verification-kompiled \
  --spec-module FALSE-RESULT \
  --dry-run
```

exits 0, establishing successful parsing/spec construction. Then the real
proof command without `--dry-run` exits 1. Its residual is reachable and
specific:

```text
WarnStuckClaimState
<k>
  8 ~> .K
</k>
...
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
```

This is the expected unmet result obligation, not a parser error, timeout,
missing import, unrelated crash, or unreachable mutation. It independently
demonstrates that the positive claim constrains the returned value.

Evidence:
`evidence/false-result.k`, `false_result_dry_run.log`, and
`kprove_false_result.log`.

## 7. Proven versus assumed accounting

### Precisely proven

Under the fixed supplied MPY semantics, for every finite `CS`, integer `N`,
and logical values satisfying the entry precondition, if execution of the
exact regenerated `fruit_distribution` closure terminates, it reaches the
exact integer value:

```text
N - APPLES - ORANGES
```

with the caller environment/scopes/control state restored, no exception, and
exit code 0. The theorem is unbounded in digit-string length and integer
magnitude. It is partial correctness: no liveness/termination theorem is
claimed.

### Trust and assumption ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K 7.1.293 parser/compiler, Haskell reachability backend, SMT/builtin integer/string/map theories | Establishes the reported symbolic reachability result | Ordinary proof checker trust. Fresh compile, positive `#Top`, ground `#Top`, and two expected stuck mutations were recorded. |
| Supplied MPY semantics | Defines calls, frames, strings, split, allocation, indexing, parsing, arithmetic, and return | Required fixed semantics and recursively identical to the trusted mount. All 695 rules were inventoried. Used limitations are guarded; unused opaque symbols do not influence the theorem. |
| Trusted `py2mpy.py` | Connects CPython AST syntax to `solution.mpy` | Byte-exact regeneration plus constructor-level body/parameter comparison. It is trusted translation code, not a proof rule. |
| Direct-closure entry normalization | Connects omitted module load/name lookup to the actual binding | Fixed `FuncDef` mapping plus mechanical normalized-tree equality. A body mutation changing that closure changes the result to 20 and fails. |
| Exact phrase-domain interpretation | Connects the formal guards to the natural-language source contract | All examples have the exact grammar and arbitrary nonnegative counts; zero/large/whitespace cases were tested. More permissive canonical behavior on malformed/free-prose strings is excluded and is the main non-fatal concern. |
| CPython/MPY behavioral bridge | Supports intended-runtime adequacy | 163 finite Python differential cases, fresh LLVM execution, and a ground K witness. This is empirical support, not universal CPython equivalence. |
| Temporary final heap | Two split-list allocations are not postconstrained | Acceptable because the HumanEval observation is the returned integer; environment, stack, return, exception, and exit cells are constrained. |
| Termination | Reachability is partial correctness | Explicitly not proved. The fixed execution path is finite for finite admitted strings, but that observation is not promoted to a K liveness theorem. |

Candidate `PROOF.md`, prior logs, generation traces, and differential claims
were not used as substitutes for the reachability proof. The independent
differential supports only the finite Python fidelity/intent bridge.

### Decision

Gate A passes: the proof is sound under the fixed semantics, executes the real
body, constrains the result, and rejects meaningful body/result mutations.
The material Gate B domain passes: it covers arbitrary-size well-formed basket
phrases of the form demonstrated by every prompt example, not a finite set of
sizes or bounded unrolling. Gate C evidence is reproducible and its trust
boundaries are explicit.

The edge-domain ambiguity, ASCII/whitespace subset, and finite CPython bridge
justify `CONCERNS`, but not `FAIL`: none admits a false conclusion on the
formal/intended phrase domain, and none materially restricts fruit counts,
string length, or arithmetic magnitude. The proof is therefore legitimate.

Exact commands and observed statuses are consolidated in
`evidence/COMMANDS.md`; `evidence/final_checks.log` confirms all required
positive and negative markers.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
