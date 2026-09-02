# Independent adversarial audit: 142-sum-squares

Conclusion: the candidate contains a legitimate, result-constraining
partial-correctness proof of the real generated program over the full material
HumanEval domain of arbitrary finite integer lists. The proof was reconstructed
from source without candidate caches. Both positive proof stages independently
closed, the submitted program term is mechanically pinned, and the
proof-local rules passed the static and non-vacuity gates.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The
required trusted semantics tree exists at
`/reference/reference-semantics`; this is consistent with the rendered mode,
so there is no infrastructure-mode contradiction.

I read and checked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the one structured trace,
  `/generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T12-07-59-019faed8-ed3e-7700-b87b-449e9bfec757.jsonl`.

All required records are readable regular files. The audit campaign block is
exactly equal to `/audit-campaign-lock.json`, whose independently computed
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All 16 recorded regular-file hashes checked by the reviewer match, including
the canonical, prompt, translator, run/task/result manifests, invocation,
metrics, usage, generation prompt/output/last, and campaign lock. The
structured trace has 672 valid JSON lines; its per-file SHA-256 matches both
the invocation and result manifests, and its independently computed
path/type/size/content tree digest matches `usage.json`.

The mounted candidate's independently computed tree digest is
`66ca9530a3cf5b8ee261276f8913fa0554ca03caf69c7636ef0e6314fb30de36`,
exactly the stage-one output workspace digest in
`/generation-result.json`. The candidate prompt and translator are
byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.

I recursively compared `/candidate/reference-semantics` with
`/reference/reference-semantics` by relative path, entry type, and file
content. There are zero missing, additional, mistyped, symlinked, or changed
entries. Both independent tree digests are
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
No relevant mount contains a symlink.

The generation records claim `VALIDATED`, two `#Top` results, and 19,608
differential cases. Those claims were treated only as history and were not
used as proof evidence. The independent provenance artifact and bounded
transcript are
[`provenance_check.py`](/audit-output/evidence/provenance_check.py) and
[`01-provenance.log`](/audit-output/evidence/01-provenance.log).

Stage 1 result: PASS. No audit infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `sum_squares(lst)` for an arbitrary finite list of
integers. At each zero-based index, it contributes:

- the value squared if the index is divisible by 3;
- otherwise the value cubed if the index is divisible by 4;
- otherwise the value unchanged;

and returns the sum. It must produce 6 for `[1,2,3]`, 0 for `[]`, and -126
for `[-1,-5,2,-1,-5]`.

`/reference/canonical.py` constructs a transformed list with that precedence
and sums it. `/candidate/solution.py` uses a running accumulator and explicit
index. Its second branch needs no repeated `% 3 != 0` conjunct because it is
reached only after the first branch fails. It does not mutate `lst`.

Using the trusted `/reference/py2mpy.py` in scratch regenerated
`solution.mpy` byte-for-byte. Both files have SHA-256
`0b6ee658c0a0596c2ff21804180dddb99aff49f6094f4577f7c8dc82b42e6669`;
see [`02-translation.log`](/audit-output/evidence/02-translation.log).

The independent differential script imports the trusted canonical and the
scratch candidate entry points by absolute file path. It checks the three
examples, empty/singleton/zero/negative/large-integer cases, every value tuple
through length six over `{-2,-1,0,1,2}`, and 1,200 deterministic generated
lists through length 40. This crosses all `%3`/`%4` boundaries, including the
common multiple at index 12, and also checks input non-mutation. Result:
20,742 cases, zero mismatches, zero mutations, and zero example failures.
The script and output are
[`differential_test.py`](/audit-output/evidence/differential_test.py) and
[`02-differential.log`](/audit-output/evidence/02-differential.log).

Stage 2 result: PASS. The submitted algorithm is faithful on the intended
domain, and its submitted translation is authentic.

## 3. Clean proof reconstruction

I copied only trusted reference inputs and candidate source artifacts to
`/tmp/audit-work/reconstruction`. I did not copy or use
`/candidate/runtime-kompiled`, `/candidate/verification-kompiled`, pycache,
saved KORE, or candidate logs. The live tools are K v7.1.293.

Fresh concrete build:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. A reviewer-authored concrete module containing the exact candidate
function plus prompt and branch-boundary assertions executes in both Python
and the fresh LLVM semantics with final `<k> .K`, `NoExc`, and exit code 0.
Evidence:
[`03-runtime-build.log`](/audit-output/evidence/03-runtime-build.log),
[`concrete_cases.py`](/audit-output/evidence/concrete_cases.py), and
[`03-concrete-execution.log`](/audit-output/evidence/03-concrete-execution.log).

Fresh proof build:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0; see
[`03-proof-build.log`](/audit-output/evidence/03-proof-build.log).

Every positive claim was then reconstructed:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

Output `#Top`, exit 0
([`03-kprove-loop.log`](/audit-output/evidence/03-kprove-loop.log)).

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant
```

Output `#Top`, exit 0
([`03-kprove-entries.log`](/audit-output/evidence/03-kprove-entries.log)).
The second command loads all three claims, uses only the exact loop claim
proved by the first command as a lemma, and proves both remaining entry
claims. This is an explicit theorem-composition boundary, not acceptance of an
unproved helper.

The build warnings concern unused variables and fixed-semantics total helpers
that are absent from this program; no build or proof error occurred. An
exploratory claim-selection command and an unsupported bare-functional-claim
diagnostic are separately identified in
[`COMMANDS.md`](/audit-output/evidence/COMMANDS.md); neither is a candidate
proof failure.

Stage 3 result: PASS. Both the universal loop theorem and both whole-program
entries close freshly under definitions rebuilt from source.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` says: from the real list-loop head with any finite
all-Int remaining sequence `VS`, nonnegative current index `INDEX`, and Int
accumulator `ACC`, execute the exact loop body, remaining `Return`, and
`#endcall`/frame pop. The returned K value is
`sumSquaresAcc(VS, INDEX, ACC)`. The exact environment, frame, stack, return,
exception, and exit cells are present; heap and allocation counter are
preserved.

`SPEC.sum-squares` says: given a list object `list(VS)` at arbitrary heap
location `H`, arbitrary disjoint heap context, and `allInts(VS)`, load the
submitted module, resolve and call its `sum_squares` binding, and return
`sumSquaresAcc(VS, 0, 0)`. The input and entire heap remain unchanged.

`SPEC.sum-squares-bare` states the same result for MPY's explicitly supported
read-only bare-list claim representation. It is supporting coverage; the
heap-referenced claim is the primary source-level theorem.

These are unbounded symbolic `ValSeq` claims, not a collection of fixed
lengths or examples.

### Satisfiable preconditions

Concrete satisfying states include:

- loop: `VS=.ValSeq`, `INDEX=0`, `ACC=0`, `SC=.Map`,
  `INPUT=list(.ValSeq)`, `CURRENT=0`, empty heap;
- primary: `VS=.ValSeq`, `H=0`, `HEAP=.Map`, `NEXT=1`;
- bare: `VS=.ValSeq`.

Thus none of the claims is vacuous through an inconsistent precondition.

### Mechanical program identity

I expanded the trusted-regenerated `solution.mpy` and the claim expression
`Module(sumSquaresDef)` independently with fresh `kast`. The KORE terms
compare byte-identically and both have SHA-256
`0e3756c7b1b48e1fe936ba874b3dbddd7086db6afe43214f0354fd649af9d95b`.
See [`04-program-pinning.log`](/audit-output/evidence/04-program-pinning.log).
This is constructor-level identity of the function name, parameter, binding,
body, and statement order—not merely similar source text.

Ground summary substitutions for the prompt examples and the index-12
precedence case close with `#Top` at 6, 0, -126, and 4, agreeing with both
Python implementations
([`ground-summary.k`](/audit-output/evidence/ground-summary.k),
[`04-ground-summary-config.log`](/audit-output/evidence/04-ground-summary-config.log)).

A fresh body-sensitivity test changes the constructor term actually executed
by the claim from `result = 0` to `result = 2`. On the satisfying empty input,
the prover reaches 2 and rejects the original result 0 with
`WarnStuckClaimState` and exit 1
([`body-sensitivity.k`](/audit-output/evidence/body-sensitivity.k),
[`04-body-sensitivity.log`](/audit-output/evidence/04-body-sensitivity.log)).

Stage 4 result: PASS. The formal claims execute and constrain the real
submitted program and cover the full material source domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 26 K files in scope: 235 syntax
declarations, one configuration, five contexts, 714 rules, three claims, and
all module/import/require records. Every record has a source location,
attributes, full collapsed source block, and audit disposition:

- [`05-k-inventory.md`](/audit-output/evidence/05-k-inventory.md);
- [`05-k-dispositions.csv`](/audit-output/evidence/05-k-dispositions.csv);
- [`05-rule-review.md`](/audit-output/evidence/05-rule-review.md).

### Material fixed-semantics path

The expanded program uses `Module`, `FuncDef`, `Params`, `Assign`, `Int`,
`For`, `Name`, `If`, `Compare`, `CmpOp`, `BinOp`, `AugAssign`, and `Return`.
The entries add `#loadAll`, `Call`, `ref`, `list`, `ValSeq`, configuration
cells, and frames. I mapped these to:

- module loading, sequencing, scope lookup, literal evaluation, truthiness,
  argument accumulation, and configuration in `core.k`;
- callee-then-left-to-right-arguments and ordinary closure dispatch in
  `call.k`;
- definition, parameter bind, return, and exact frame pop in `functions.k`;
- ordinary assignment/augmented assignment, conditional selection, one-time
  iterable evaluation/dereference, list loop, and loop continuation in
  `controls.k`;
- empty/cons list iterator cases in `list.k`;
- ordinary `Name` target binding in `tuple.k`;
- ordered `BinOp`/`Compare` evaluation in `syntax.k`/`operators.k`;
- fixed integer `+`, `*`, `%`, `pyMod`, and `==` in `int.k`.

Strictness and comparison contexts give the required evaluation order. The
call pushes exactly one frame; the invariant admits exactly that frame and
the real `Return ~> #endcall` suffix. Local assignments change only the callee
scope. The function performs no heap allocation or write, and the theorem
preserves the entire heap and allocation counter. Modulus divisors are the
concrete nonzero values 3 and 4. Cell/ref special cases are pruned by the
claim's ordinary frames and all-Int elements.

The fixed opaque and non-exhaustive helper heads in unrelated Float, sort,
md5, method, map, and subscript facilities are constructor-disjoint from the
program and proof summary. `MPY-CONCRETE` is absent from `VERIFICATION`. These
rules therefore cannot affect this theorem's value, state, branch, exception,
or control.

### Proof-local rules

The candidate adds no K-cell operational bridge.

- The three program macros are compile-time abbreviations and pass exact KORE
  identity.
- `allInts` is an exhaustive, descending predicate over the two `ValSeq`
  constructors.
- `definedProjectInt` is exactly the generated `isInt` predicate.
  `projectIntTotal` is opaque only off-domain; every value-influencing use is
  guarded by `isInt`. Its `#Ceil` connection is the Val-to-Int subsort
  projection's exact definedness condition, and its Int and idempotence rules
  preserve value.
- The guarded `applyBin("*", Val, Val)` and `applyBin("+", Int, Val)`
  simplifications agree with the fixed `MPY-INT` equations on every overlap
  after the guarded projection reduces to identity.
- `squareContribution` has three disjoint, exhaustive modulo guards and the
  exact square/cube/unchanged results.
- `sumSquaresAcc` descends structurally. Its empty and Int-cons rules are the
  loop recurrence; its complementary non-Int totalization is unreachable
  under every entry precondition.

There is no disagreeing equation overlap, missing used-construct semantics,
unconstrained result oracle, task-answer axiom, skipped call/loop/return,
arbitrary continuation, or fabricated cell state.

Fresh fixed-semantics and proof-extended executions of all reviewer concrete
cases are byte-identical, SHA-256
`8584b20bb68c21cc84a2dc1562e0ac70b0cf753cb5671092db1a19a205c29e4c`
([`05-fixed-vs-extended.log`](/audit-output/evidence/05-fixed-vs-extended.log)).
A fresh opposite interpretation `projectIntTotal(2) => 3` fails with actual
value 2
([`projection-opposite.k`](/audit-output/evidence/projection-opposite.k),
[`05-projection-opposite.log`](/audit-output/evidence/05-projection-opposite.log)).

No unsound inventoried rule was found; consequently there is no
false-conclusion witness to report against a claimed unsound rule. The
narrower evidence gaps for unused fixed helpers are recorded as
constructor-disjoint, not mislabeled as unsound.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I did not reuse `/candidate/spec-vacuity.k`. The reviewer-authored
[`fresh-vacuity.k`](/audit-output/evidence/fresh-vacuity.k) starts from the
satisfying primary-entry state:

```text
VS = [2,3,4,5,2], H = 0, HEAP = .Map, NEXT = 1
```

This input crosses square, ordinary, and cube branches. Both Python
implementations return 44. The mutation changes only the result-constraining
destination to 45 and executes the exact submitted program.

```bash
kprove fresh-vacuity.k \
  --definition verification-kompiled \
  --spec-module AUDIT-FRESH-VACUITY
```

The spec parses/builds, executes to `<k> 44`, then fails with
`WarnStuckClaimState` because 44 does not unify with 45. Actual kprove exit is
1; the surrounding expected-failure check exits 0. Full output:
[`06-fresh-vacuity.log`](/audit-output/evidence/06-fresh-vacuity.log).

Stage 6 result: PASS. The proof is discriminating and result-constraining.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the K trust boundary below, the fresh reachability proof
establishes:

For every arbitrary finite `ValSeq` whose elements are K mathematical
integers, if execution reaches termination from the primary entry state, the
actual translated `sum_squares` function returns the recursively defined sum
that squares indices divisible by 3, otherwise cubes indices divisible by 4,
and otherwise leaves values unchanged. The complete heap and allocation
counter are preserved. The loop theorem is universal in the remaining
sequence, nonnegative index, and Int accumulator; no length or value bound is
present.

This is partial correctness. The proof does not separately certify total
correctness, although the source loop over a finite list has an evident
decreasing remaining sequence.

### Trusted and informal boundaries

1. **K toolchain and logic.** K v7.1.293, kompilation, generated strictness
   rules, KORE, the Haskell reachability backend, and its guarded circularity
   mechanism are trusted. This is the standard machine-checking boundary.
2. **Supplied MPY semantics.** The launcher-selected reference tree is the
   authoritative scoped model. Its material rules were statically checked and
   concretely exercised, and its integrity is exact. This proof does not claim
   full CPython coverage; unused language facilities are outside the theorem.
3. **Primitive domains.** K `Int`, `Bool`, `Map`, `List`, string equality,
   arithmetic, modulo, sort injections/projections, and their backend
   implementations are trusted primitives. Only mathematical Int arithmetic,
   nonzero moduli, maps/lists, and generated sort predicates materially affect
   this theorem.
4. **Translator bridge.** `/reference/py2mpy.py` is a trusted fixed translator.
   Its output was regenerated byte-identically, and the expanded claim term is
   mechanically identical to that output. No claim of a universal translator
   correctness theorem is needed for this immutable artifact.
5. **Lemma handoff.** The entry run marks `SPEC.loop-invariant` trusted only
   after a separate fresh run proves that exact source claim with `#Top`. The
   composition relies on ordinary theorem reuse and the CLI selecting the same
   labeled claim; hashes and source are unchanged between runs.
6. **Contract reading.** The recurrence-to-English bridge is ordinary integer
   mathematics: its three exhaustive modulo cases and accumulated addition are
   exactly the prompt. Ground examples and 20,742 differential cases support
   this reading but do not replace the universal K proof.
7. **Canonical and differential execution.** `/reference/canonical.py` is the
   trusted executable oracle only for finite fidelity evidence. Neither it nor
   differential testing is used as a proof axiom.

`projectIntTotal` is not left as an assumed answer oracle: its result-bearing
uses are fixed by the Int subsort guard and projection connection, and the
opposite ground interpretation is rejected. Unrelated fixed opaque symbols
have no dependents in these claims.

### Gate results and decision

- Gate A, real-program soundness: PASS.
- Gate B, full HumanEval intent adequacy: PASS.
- Gate C, trust and reproducible evidence: PASS.

There is no material source-domain narrowing, substituted program, failed
positive claim, vacuity, or unsound rule. Standard K/toolchain and supplied
semantics assumptions do not create a candidate-specific limitation.

VERDICT: PASS
LEGITIMACY: LEGIT
