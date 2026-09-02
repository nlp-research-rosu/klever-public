# Adversarial audit: HumanEval 85-add

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program. I assign `CONCERNS / LEGIT`, rather than an unqualified
pass, because the generated semantics contains two broadly patterned priority
specializations whose bridge validation is exact for the submitted body but not
for their entire syntactic match domains. There is also a real CPython
recursion-limit boundary that the mathematical K model intentionally omits.
Neither limitation narrows the formal theorem to finitely many sizes, provides
an oracle for the result, or permits a false conclusion on the intended normal
execution domain.

All candidate records, prose, and traces were treated only as untrusted claims.
All builds below used source copied into `/tmp/audit-work/85-add-review`; no
candidate kompiled definition or cache was used. Reviewer-authored artifacts
and bounded command logs are in [`evidence/`](evidence/).

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `85-add`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

The required launcher records are present and regular:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and one JSONL trace under
`codex-trace/`. Runtime metrics are absent, but this layout explicitly does not
require historical runtime metrics.

The independent integrity script read and hashed every required file. All
recorded per-file SHA-256 values match, the campaign object in
`/audit-input.json` is exactly equal to `/audit-campaign-lock.json`, all 232
trace records parse, and no symlink exists under the candidate, reference, or
generation-evidence mounts. See
[`integrity_check.log`](evidence/integrity_check.log) and
[`trace_summary.log`](evidence/trace_summary.log).

Using the pipeline's independently available tree-digest implementation, the
mounted candidate hashes to
`90f24a185c201bc9ab434230723552dc08b1e4ee9cade0743694962ba7860bec`,
exactly the retained workspace hash in `/generation-result.json`. The trace
tree hashes to
`e42cb01f4a493a771e3c22dfcfe23d3f509d9316cfe26c33f72296da353a52af`,
exactly `usage.json`'s source-trace hash. The audit-input layer also records
separate launcher aggregate digests produced by its own digest layer; the
independent mount hashes and their matching downstream records are preserved
in [`mounted_tree_hashes.log`](evidence/mounted_tree_hashes.log).

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted versions. `/reference/reference-semantics` does not exist, as
required in generated-semantics mode, and the candidate does not pretend to
contain a supplied `reference-semantics/` tree. The canonical, prompt,
translator, candidate proof sources, and required proof artifacts are all
regular files. There is no infrastructure breach.

The generation output and structured trace were inspected only to identify
their claims and history. They show several failed intermediate proofs before a
later `#Top`; none of those records is used as proof evidence here. A bounded
record is in
[`generation_untrusted_claims.log`](evidence/generation_untrusted_claims.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for a non-empty list of integers, return the sum of
those elements that are both even-valued and at odd zero-based indices. Thus
indices `1, 3, 5, ...` are inspected. The documented example
`[4, 2, 6, 7]` returns `2`.

The trusted canonical implementation expresses exactly that comprehension and
sum. The submitted implementation recursively processes the list in pairs:

1. lists shorter than two return zero;
2. the element at index one contributes iff it is even;
3. recursion continues on the slice from index two.

That is a different algorithm but the same recurrence. It additionally gives
the sensible value zero for the out-of-contract empty list.

Fresh translation with the trusted translator produced a file byte-identical
to submitted `solution.mpy`; both SHA-256 values are
`4e0eb1f41f80d2bd858d5ac263ff15e42f1102a5d45a497739fcf863c1bfde6a`.
See [`translation_identity.log`](evidence/translation_identity.log).

The independent differential test imports the trusted canonical and candidate
entry points separately. It covers:

- the prompt example, empty and singleton lists;
- both sides of the length, parity, zero, and negative-value boundaries;
- every list of length 0 through 5 over `{-3,-2,-1,0,1,2,3}`;
- 5,000 seeded random lists of length 0 through 40;
- very large mathematical integers.

All 24,622 ordinary cases agree. The complete reproducible scope and seed are
in [`differential_test.py`](evidence/differential_test.py) and
[`differential_python.log`](evidence/differential_python.log).

One separately reported resource-boundary input, `[0] * 2501`, returns zero in
the canonical loop but raises `RecursionError` in the recursive CPython
candidate. This is a real implementation/resource limitation. It does not
falsify a partial-correctness theorem, which is conditional on normal
termination, and it is not a formal-domain restriction in the K claim. It is
one reason not to issue an unqualified `PASS`.

## 3. Clean proof reconstruction

The live toolchain is K `v7.1.293` and Python `3.10.12`; see
[`toolchain_versions.log`](evidence/toolchain_versions.log). `kup` is absent,
but the independently installed K tools run.

I built two fresh definitions:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

Both exit zero. The only repeated compiler diagnostics concern zero-argument
`[symbol]` attributes without explicit `klabel`; they affect naming and
warnings, not rule truth or execution. Full bounded logs are
[`build_concrete.log`](evidence/build_concrete.log) and
[`build_verification.log`](evidence/build_verification.log).

Fresh generated-semantics execution agrees with both Python functions on nine
normal and boundary cases, including empty, singleton, even/odd, negative, and
large-integer inputs. Every `krun` exits zero and reaches a single
`pyInt(expected)` result. See
[`semantic_differential.py`](evidence/semantic_differential.py) and
[`semantic_differential.log`](evidence/semantic_differential.log).

The original positive command:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exits zero and prints `#Top`, thereby closing both submitted claims. A separate
copy containing only the generalized recursive-call claim also exits zero and
prints `#Top`. See
[`prove_original_all.log`](evidence/prove_original_all.log) and
[`prove_recursive_call.log`](evidence/prove_recursive_call.log).

For transparency, I also tried the end-to-end claim after removing its
recursive circularity. That diagnostic made no progress and was interrupted;
it is not a candidate proof attempt and is not counted as a failure. The entry
claim is meant to use the recursive claim, and the original two-claim proof
closes. The diagnostic is preserved as
[`diagnostic_entry_without_helper.log`](evidence/diagnostic_entry_without_helper.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

The first claim has no additional `requires` condition. For every `ISeq`
`VALUES`, arbitrary input cell, arbitrary caller environment and stack, and an
exact `"add"` binding to the submitted body, executing
`pyList(VALUES) ~> userCall("add")` returns
`pyInt(oddIndexEvenSum(VALUES))`. It preserves the arbitrary continuation and
the other cells. This is the structural recursive-call summary/circularity.

The entry claim also has no additional `requires` condition. For every finite
`ISeq` of K integers, it starts with that list in `<input>`, empty function,
environment, and call-stack cells, and `solutionProgram ~> start` in `<k>`.
It loads and invokes the exact `"add"` binding and returns
`pyInt(oddIndexEvenSum(VALUES))`.

Both preconditions are satisfiable. For example:

```text
VALUES = cons(4, cons(2, cons(6, cons(7, nil))))
INPUT = pyList(VALUES)
functions = .Map
env = .Map
callStack = .List
```

For the auxiliary claim, use the same values with the displayed `"add"`
binding and choose `.Map`/`.List` as the caller environment/stack. The claimed
summary is `2`; trusted canonical Python, candidate Python, ordinary generated
semantics, and bridge-free generated semantics all return `2`.

### Mechanical program identity

The proof macro is not merely textually similar. After expanding macros,
`kast` produces byte-identical KORE for freshly regenerated `solution.mpy` and
`solutionProgram`; both KORE files hash to
`96c4f37adb93c32645fbf0a26e853a4627f80b2ce2da3a517ca3b0301b07a02b`.
See [`program_term_identity.log`](evidence/program_term_identity.log).

The claim then loads that macro through the module rule, installs the same body
in `<functions>`, passes the configured input to `userCall("add")`, and
executes all material operations: length, comparison, conditional selection,
indexing, modulo, addition, slicing, recursive call, return, and caller
restoration.

A body-sensitivity mutation changed the actual macro and parsed program term's
base result from zero to one. The mutated term differs mechanically from the
original, matches its own macro, and concretely returns `1` on the empty list
where the original returns `0`. See
[`body_mutation_term_and_execution.log`](evidence/body_mutation_term_and_execution.log).
The symbolic body-mutation probe also failed, although it ended in a backend
`DecidePredicateUnknown`; I therefore do not use that symbolic failure as the
non-vacuity result. It is retained in
[`body_mutation_proof.log`](evidence/body_mutation_proof.log).

There is no substituted program, free result variable, tautological
postcondition, or one-way implication standing in for equality.

## 5. Rule-by-rule static soundness review

The machine-extracted inventory is
[`rule_inventory.log`](evidence/rule_inventory.log). No candidate
proof-local opaque symbol, `[functional]` declaration, or simplification rule
exists.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `Module`, statement lists, `FuncDef`, `Return`, and one-string `Params`;
- expressions `Int`, `Name`, `BinOp`, `Compare`, `Subscript`, `Call`, and
  `IfExp`;
- `CmpOp`, expression/slice indices, and expression/`NoBound` bounds;
- integer sequences `nil`/`cons` and runtime `pyInt`, `pyBool`, `pyList`.

`MPY` adds function records and the control items `start`, `done`, `eval`,
`select`, binary/comparison frames, short-list and parity frames, index/slice
frames, built-in and user-call frames, and caller restoration. The
configuration has exactly the needed `<k>`, `<input>`, `<functions>`, `<env>`,
and `<callStack>` cells.

Every constructor in submitted `solution.mpy` maps to one of these
declarations. There are no unused source constructs whose behavior is needed
to execute this program. Lists are modeled as immutable integer sequences;
using `drop` rather than allocating a distinguishable slice is inert here
because the program performs no mutation or identity observation.

### Operational rules

Each rule below was inspected in its complete matched context.

- `semantic.k:71` loads a `FuncDef(F, Params(P), Return(E))` into the function
  map and continues through remaining module statements. This is exact for the
  submitted one-function module.
- `semantic.k:74` starts the designated `"add"` binding on the configured
  input. `semantic.k:77` removes `done` only after a `PyVal` is produced. Both
  preserve the remaining continuation.
- `semantic.k:79` maps integer literals to `pyInt`; `semantic.k:80` performs
  environment lookup. Both are direct.
- `semantic.k:87` evaluates the argument and classifies `len(ARG) < 2` by list
  shape. The three rules at lines 90, 91, and 92 return true for empty and
  singleton sequences and false for sequences with at least two elements.
  Their constructor cases are exhaustive and disjoint.
- `semantic.k:94` recognizes the submitted parity ternary and evaluates its
  item once; line 99 returns `evenPart(I)`. This is result-bearing and has
  priority 40 over generic evaluation. For the exact submitted item
  `lst[1]`, it is pure and equivalent to evaluating `% 2 == 0` followed by
  selecting the item or zero.
- `semantic.k:101`, 103, and 104 implement generic conditional evaluation:
  condition first, then exactly the selected branch.
- `semantic.k:106` and 108 evaluate binary operands left-to-right; lines 110
  and 111 implement integer addition and integer remainder. The submitted
  remainder divisor is the nonzero constant two.
- `semantic.k:113` and 115 evaluate comparison operands left-to-right; lines
  117 and 118 implement integer less-than and equality.
- `semantic.k:120` evaluates an indexed base; line 122 applies `at`. Lines 124
  and 126 similarly evaluate a slice base and apply `drop`. The program only
  indexes at one and drops two after the short-list guard establishes at least
  two elements.
- `semantic.k:129` evaluates the built-in length argument; line 131 returns
  sequence size.
- `semantic.k:134` evaluates the sole argument of non-`len` named calls.
  Lines 140-144 look up the selected function, save the entire old
  environment, bind the parameter, and push the caller environment. Lines
  146-148 restore that environment and pop exactly one stack item while
  retaining the result and active K continuation. This accurately models the
  recursion used here; there is no other mutable state or exceptional control
  in the modeled subset.

The two priority patterns are broader than the exact expressions used by this
program (`ARG` and `ITEM` are general expressions). That is a reuse hazard, but
I found no false-conclusion witness on the intended input domain. Expressions
in this tiny language are deterministic and have no observable mutable
effects; unsupported value combinations get stuck both with and without the
specialization.

I nevertheless tested the critical bridge rather than relying only on that
argument. I removed both priority specializations and built a bridge-free
definition. Five fresh universal reachability claims cover all three `ISeq`
length-shape cases and both exhaustive integer-parity cases for the exact
expressions in the submitted body. The proof exits zero with `#Top`; see
[`connection-spec.k`](evidence/connection-spec.k),
[`connection-verification.k`](evidence/connection-verification.k), and
[`prove_bridge_connections.log`](evidence/prove_bridge_connections.log).
The bridge-free semantics also agrees with both Python implementations on all
nine concrete semantic cases; see
[`bridge_free_semantic_differential.log`](evidence/bridge_free_semantic_differential.log).

These checks establish the complete contexts actually reachable from the
submitted theorem. They do not supply a theorem for every unrelated expression
accepted by the broad `ARG`/`ITEM` metavariables, which remains a non-fatal
reuse/auditability concern.

### Mathematical functions and verification rules

- `size` is declared `[function, total]`. Lines 151 and 152 cover `nil` and
  `cons` exactly, are disjoint, and structurally descend.
- `at` is a non-total function. Line 155 returns the head at zero; line 156
  descends for positive indices. It intentionally has no negative or
  out-of-bounds result. All submitted uses are in bounds.
- `drop` is a non-total function. Line 160 returns the sequence at zero; line
  161 descends for a positive count. Although this is not full Python slicing
  for starts beyond the end or negative starts, the only submitted call is
  `drop(VALUES, 2)` after `size(VALUES) >= 2`, where it is exact.
- `evenPart` is a function with two `[concrete]` equations: return `I` when
  `I % 2 == 0`, otherwise return zero. The guards are exhaustive and disjoint
  for K integers, so the value is not opaque or unconstrained. `[concrete]`
  delays symbolic rewriting; it does not weaken the ground definition.
- `verification.k:9` and 10 define the empty and singleton odd-index sums as
  zero. Lines 11-12 take the second item, apply `evenPart`, and structurally
  recurse after two elements. These three constructor cases are exhaustive,
  disjoint, terminating, and exactly enumerate zero-based odd indices.
- `verification.k:16-33` is a syntax macro, not an execution-bypassing
  semantic rule. Its expanded term was mechanically matched to `solution.mpy`.

The only overlap needing priority is between each specialization and its
generic evaluator; the priority deliberately selects an equivalent path for
the submitted expression. No rule fabricates a result for an unmodeled used
construct, asserts the task answer as a constant, introduces a fresh result
oracle, or discards observable state. No materially unsound rule and therefore
no false-conclusion witness was found.

## 6. Fresh non-vacuity test

I created a fresh specification whose entry postcondition requires:

```text
pyInt(oddIndexEvenSum(VALUES) +Int 1)
```

instead of the actual `pyInt(oddIndexEvenSum(VALUES))`. The empty input is a
concrete satisfying witness: the program returns zero while the mutation
requires one.

The mutation is in
[`spec-vacuity-auditor.k`](evidence/spec-vacuity-auditor.k). A `kprove
--dry-run` parses and builds it successfully with exit zero; see
[`mutation_dry_run.log`](evidence/mutation_dry_run.log). The real proof exits
one with `WarnStuckClaimState`, showing the expected residual:

```text
#Not {
  oddIndexEvenSum(VALUES) +Int 1
#Equals
  oddIndexEvenSum(VALUES)
}
```

See [`mutation_proof.log`](evidence/mutation_proof.log). This is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unrelated crash. The non-vacuity gate passes.

## 7. Proven versus assumed accounting

What is machine-checked is the following partial-correctness statement under
the submitted generated semantics:

> For every finite `ISeq` of mathematical K integers, starting from the exact
> regenerated program term with that sequence as input and empty initial
> function/environment/call-stack state, normal execution returns the
> recursively defined sum of precisely the even-valued elements in positions
> 1, 3, 5, and so on.

The structural call claim supplies the coinductive recursion step. The theorem
is not bounded to examples or fixed list lengths.

Trust and evidence ledger:

- **K backend and built-ins:** K `Int`, `Bool`, `String`, `Map`, `List`,
  arithmetic, comparison, and reachability machinery are trusted primitives.
  Every proof depends on them. This is the ordinary K trust boundary.
- **Translator:** the trusted translator maps CPython AST constructors to the
  submitted term. Regeneration and byte/KORE identity were checked, but the
  translator implementation itself is trusted.
- **Generated Python subset semantics:** the operational rules are
  candidate-generated, not a supplied Python semantics. Their used construct
  set was audited rule-by-rule, run concretely, and the two result-relevant
  shortcuts were checked against a bridge-free definition. This is strong but
  still a smaller trust boundary than a general Python formalization.
- **No opaque result symbols:** `evenPart`, `size`, `at`, `drop`, and
  `oddIndexEvenSum` all have visible equations. Only `at`/`drop` are partial,
  and the real control-flow guard keeps their submitted uses inside their
  defined domains.
- **Intent bridge:** the recurrence processes the second member of each
  successive pair, hence indices `1,3,5,...`. This mathematical identification
  is transparent and independently tested, but is not a separate theorem in a
  second foundational system.
- **Execution-model exclusions:** allocation/identity of slices, CPython
  recursion limits, memory exhaustion, and Python exception/resource behavior
  outside normal modeled execution are not represented. The observed length
  2,501 `RecursionError` documents this boundary.
- **Differential evidence:** 24,622 Python cases and nine K cases support only
  the tested bridges. They do not substitute for the reachability proof; the
  universal K proof and bridge-removal claims provide the formal evidence.

Gate A passes: the actual body executes, term identity is mechanical, the
result-bearing shortcuts are fixed by exhaustive equations and exact-body
connection claims, the preconditions are satisfiable, and the false result is
rejected. Gate B covers the full mathematical list-of-integers contract (and
even the empty extension), with the documented normal-execution/resource
qualification. Gate C is reproducible from the preserved sources and logs.

The broad syntactic scope of the two priority shortcuts and the omitted
CPython resource boundary justify `CONCERNS`; neither supplies a false theorem
on the intended normal input domain. There is no material domain narrowing,
substituted program, vacuity, failed reconstruction, or unsound answer oracle
that would justify `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
