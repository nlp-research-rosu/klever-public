# Independent adversarial review: 20-find-closest-elements

The submitted K claims reconstruct cleanly and are honest, result-constraining
claims about the exact submitted constructor program. They do **not** prove the
HumanEval contract: their only symbolic input family has length exactly two,
while the remaining claims are three fixed examples. This materially narrows
the contract's unrestricted length-at-least-two domain. Under the benchmark's
explicit decision boundary, the otherwise sound limited theorem is
`FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and `semantics_mode =
GENERATED_SEMANTICS`. I used its `container_paths`, not its host provenance
paths.

All records required by that layout are present, readable, regular, and
unlinked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the trace tree;
- the present optional `/generation-evidence/usage.json`; and
- the additional legacy records `legacy-metrics.json` and
  `legacy-run-input.json`.

`runtime-metrics.json` is absent, as permitted for this legacy-selected layout.
The one structured trace file has 165 valid JSONL events and no invalid record.
The full 487,555-character generation log, last message, prompts, manifests,
metrics, usage, and trace were read as untrusted generation history. No prior
claim in them was used as proof evidence.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` field-for-field. Its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded lock hash. Every launcher-recorded regular-file hash
checked against the mounted byte stream, including all generation records,
canonical source, prompt, and translator. The invocation's per-file trace
digest also matches.

An independent pipeline tree digest of `/candidate` is
`adc52633e57d70e47975c9d0b1ca8f81cecb6bd68fc8f1c041463fb7a4ff0f06`,
matching the retained/output workspace hash in both
`generation-result.json` and `invocation.json`. The corresponding independent
trace-tree digest is
`c76b406b66475ce0c65e2e6cba46037ee7bd4aa0e9bbd89ef3fb9658c90f8994`,
matching `usage.json`'s `source_trace_sha256`. All candidate, reference, and
generation entries are regular files/directories; no symlinks were found.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to
`/reference/py2mpy.py`. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist and
`mount_reference_semantics` is false. There is no semantics-mode
infrastructure contradiction or missing launcher record.

Evidence: [bounded command log](evidence/command-log.md), especially Stage 1.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py:4-10` is:

> For any supplied list of numbers of length at least two, select two elements
> whose distance is minimum and return the pair in nondecreasing order.

The contract does not bound the list length and does not require a particular
pair when several pairs tie at the same minimum distance.

The trusted canonical implementation at `/reference/canonical.py:16-31`
enumerates distinct index pairs, compares absolute gaps, and retains the first
strict improvement. The candidate implementation at
`/candidate/solution.py:5-29` initializes from the first pair, enumerates every
unordered index pair with nested while loops, normalizes each pair, and retains
strict improvements. It is a different but contract-compatible algorithm.

In scratch, the trusted translator regenerated the submitted source:

```text
submitted solution.mpy   b55ed6ed23309810651d2a11ca145e61a0fcffac8d85a3150ccc20345c9f43ab
regenerated solution.mpy b55ed6ed23309810651d2a11ca145e61a0fcffac8d85a3150ccc20345c9f43ab
cmp exit                 0
```

The independent differential test exercised both prompt examples; minimum
legal size in ascending, descending, and equal forms; initial-swap and
inner-swap paths; improvement/no-improvement paths; an equal-gap tie;
duplicates; negatives; signed zero; large finite magnitudes; 3,900 exhaustive
ordered lists of lengths 2–5 over a five-value pool; and 2,500 seeded generated
lists of lengths 2–30. There were zero in-domain mismatches.

Empty and singleton lists were also tested. The canonical returns `None` while
the candidate raises `IndexError`; those two cases violate the explicit
length-at-least-two precondition and are not fidelity defects.

Evidence: [differential_test.py](evidence/differential_test.py),
[regenerated-solution.mpy](evidence/regenerated-solution.mpy), and Stage 2 of
the [command log](evidence/command-log.md).

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the trusted translator/canonical
source to `/tmp/audit-work/closest-audit`. I did not copy or use candidate
kompiled definitions, `kore-exec.tar.gz`, bytecode caches, prior output, or
traces.

Fresh K 7.1.293 builds succeeded:

```text
LLVM semantic.k build       exit 0
LLVM verification.k build   exit 0
Haskell verification.k build exit 0
```

The generated semantics was concretely executed through the exact entry
harness:

| Input | Fresh K result | Python candidate | Status |
|---|---|---|---|
| `[1,2,3,4,5,11/5]` | `(2,11/5)` | `(2.0,2.2)` | agree under the stated rational representation |
| `[2,1]` | `(1,2)` | `(1.0,2.0)` | agree; minimum-size and initial-swap boundary |
| `[-10,-3,-7/2,9]` | `(-7/2,-3)` | `(-3.5,-3.0)` | agree; later update |
| `[]` | `valueAt(vnil,0)`, exit 113 | `IndexError` | both fail; outside contract |

Loading `solution.mpy` itself under the semantics consumes the module and
installs the exact `find_closest_elements` function binding.

The fresh positive proof command was:

```sh
kprove spec.k --definition fresh-verification-proof-kompiled \
  --spec-module SPEC
```

It selected all six unlabeled claims, printed `#Top`, and exited 0. Thus the
submitted formal claims close under the freshly built candidate semantics.
This dynamic result is not treated as adequacy or semantics validation.

Evidence: the run inputs
[example](evidence/run-example-1.mpy),
[length-two descending](evidence/run-length2-descending.mpy),
[negative update](evidence/run-negative-update.mpy), and
[out-of-domain empty](evidence/run-out-of-domain-empty.mpy), plus Stage 3 of
the [command log](evidence/command-log.md).

## 4. Adequacy and real-program pinning

### Plain-language claims

The six entry claims in `/candidate/spec.k:7-62` say:

1. one fixed length-six prompt input returns `(2, 11/5)`;
2. one fixed duplicate-valued length-six prompt input returns `(2,2)`;
3. every exact-rational two-element list `[A,B]` with `A < B` returns `(A,B)`;
4. every exact-rational two-element list `[A,B]` with `B < A` returns `(B,A)`;
5. every exact-rational two-element list `[A,B]` with `A = B` returns `(A,B)`;
6. the fixed length-four input `[-10,-3,-7/2,9]` returns `(-7/2,-3)`.

Each claim starts with empty modeled environment/function maps and `noResult`;
each requires the computation to be consumed, the internal maps to be empty,
and the result to be the explicit tuple. The result is neither free nor
guarded only by a one-way implication.

Satisfying witnesses exist for every precondition: the three ground claims are
their own witnesses; claims 3–5 use respectively `(A,B)=(1,2)`, `(2,1)`, and
`(2,2)`. All six formal results equal both Python implementations on those
witnesses. Evidence:
[claim_witnesses.py](evidence/claim_witnesses.py).

### Program identity and sensitivity

`verification.k:9-43` defines `solution` as a constructor tree. An independent
extractor obtained that exact rule RHS, normalized only the three explicit
`.Stmts` empty-list units to the concrete parser's empty spelling, and parsed
both it and the trusted regenerated `solution.mpy`. The two 12,835-byte KORE
terms are byte-identical:

```text
49688d9f3ee1f5d0191129959613193e441b4c09fddf4b0e0a6d3db493f8d5dd
```

Evidence: [extract_solution_rhs.py](evidence/extract_solution_rhs.py),
[regenerated KORE](evidence/regenerated-solution.kore), and
[embedded KORE](evidence/proof-embedded-solution.kore).

The claims execute `run(solution, ...)`; the semantics expands that exact
module, registers its exact body, looks the function up by the required name,
binds its parameter, and executes the body. There is no summary that skips a
loop or replaces its value.

A fresh body-sensitivity test changed the second initialization subscript in
the **embedded executed term** from index 1 to index 0. The mutated definition
built, but the documented example claim failed with
`WarnStuckClaimState` at actual result `(1,1)`. This is genuine body
sensitivity, not a change to an unused external Python file. Evidence:
[mutated verification](evidence/verification-body-mutated.k) and
[mutated spec](evidence/spec-body-mutated.k).

### Material adequacy failure

There is no arbitrary-list claim, no list variable ranging over lengths at
least two, and no loop invariant/helper claim. The only symbolic execution has
fixed length two; all longer executions have fully fixed values and lengths.
The loops are therefore unrolled only for finitely fixed executions.

The theorem says nothing about:

- any list of length 3, 5, or greater than 6;
- arbitrary contents at lengths 4 or 6; or
- arbitrary contents at any length other than 2.

This is a material narrowing of the unrestricted HumanEval source-contract
domain, not an artifact-maintenance limitation. It is Gate B failure and,
under this benchmark's explicit mapping, requires `FAIL / NOT_LEGIT` even
though the limited claims themselves are sound.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved in
[rule-inventory.md](evidence/rule-inventory.md). It enumerates:

- every local syntax production and the four-cell configuration;
- all 51 rules in `semantic.k`;
- the exact-program rule and three `nums` rules in `verification.k`;
- all six claims; and
- every local attribute.

The submitted source's complete construct set—module/import/function,
parameters, assignments, names, integer literals, subscripts, arithmetic,
comparisons, conditionals, nested loops, `len`, return, and tuple
construction—has declarations and executable rules. Concrete tests collectively
exercise every used construct and both material branches.

Static findings:

- `valueLength` and positive-index `valueAt` structurally descend; used
  accesses are in range. Invalid or malformed inputs stop rather than receive
  fabricated values.
- Integer/rational addition, subtraction, and comparison cases are
  constructor-disjoint and use K's exact arithmetic. No helper is marked
  `[total]`.
- statement/expression contexts enforce left-to-right evaluation;
  true/false rules are disjoint; a true while executes its body then restores
  the same loop head.
- function registration, lookup, argument binding, local assignment, and
  return all execute on the real body. There are no loop summaries,
  simplification axioms, priorities, task-answer rules, unconstrained oracles,
  opaque result symbols, or proof-local operational bridges.
- `solution` is a truthful definitional constant, mechanically connected to
  the regenerated program. The `nums` rules are truthful finite-list
  constructors.

Four rules are intentionally minimal rather than reusable full-Python
semantics: all imports are ignored (the actual import is typing-only);
function entry replaces the local environment (the body uses no globals);
top-level return clears the harness's internal maps; and `len` is recognized
syntactically (the exact program does not shadow it). Their exact submitted
matches preserve the task result and control. I found no intended-domain false
conclusion witness, so I do not label these rules unsound. Their broader
reusability is limited.

The largest semantics adequacy gap is numeric: `vnum(Rat)` and K exact-rational
arithmetic are not an IEEE-754 Python `float` model. They exclude NaN and
infinities and treat `11/5` as exact. The ground claims and finite concrete
bridges tested here agree with Python, but there is no universal
machine-checked float-to-rational connection. This is an additional trust/domain
limitation for any purported full Python theorem; it is not a false equation
inside the declared `Rat` rules.

The only imported nonlocal theory is the installed K 7.1.293
`BOOL`/`INT`/`RAT`/`MAP`/`STRING` theory (including `rat.md`). That is an
ordinary low-level toolchain trust boundary, not a task-answer axiom.

No candidate-local rule is rejected as materially unsound; consequently there
is no unsupported unsoundness label lacking the required false-conclusion
witness. The decisive failure is theorem scope.

## 6. Fresh non-vacuity test

I created a fresh claim for the satisfiable first prompt input but changed its
required result from the true `(2,11/5)` to the false `(2,5)`.

The mutation's `kprove --dry-run` exited 0 and emitted a valid backend proof
command, establishing that it parses/builds. The real proof exited 1 with
`WarnStuckClaimState`; its terminal configuration was:

```text
<k> .K </k>
<env> .Map </env>
<functions> .Map </functions>
<result> vtuple(vnum(2), vnum(11 /Rat 5)) </result>
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. It shows the entry
claim discriminates the returned value.

Evidence: [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) and Stage 6 of
the [command log](evidence/command-log.md).

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the freshly built candidate semantics and K's imported
theories, executing the exact submitted constructor program from the six
listed entry configurations reaches the six explicit result tuples and final
modeled state. The three length-two claims quantify over exact rationals under
their exhaustive order/equality cases. The other three claims are ground
executions. The proof is body-dependent and result-constraining.

It does **not** machine-check that the algorithm returns a closest pair for
arbitrary lists of length at least two. It does not even state such a claim.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 prover/backend and builtin BOOL, INT, RAT, MAP, STRING rules | Every build, execution, and claim | Acceptable standard proof-tool trust boundary. |
| Trusted `/reference/py2mpy.py` transliteration | Source-to-constructor identity | Launcher-trusted; byte regeneration and KORE identity independently checked. |
| Candidate-generated `semantic.k` | Meaning of all six reachability claims | Exhaustively audited and concretely tested for the used subset. Sound for the limited claims, but not independently proved equivalent to CPython. |
| Exact rational values/arithmetic as a stand-in for Python floats | All numeric K results | Ground/finite agreement only. No IEEE special values or universal rounding bridge; unacceptable as an unqualified full-float proof boundary. |
| Ignored typing import, local-only environment, top-level run/return harness | Control and modeled final maps | Exact submitted body has no dependency that exposes the abstraction; acceptable for the limited returned-value claims, limited for reusable semantics. |
| Python candidate versus trusted canonical equivalence | Informal source-level rewrite bridge | 6,400 exhaustive/generated in-domain tests plus named cases, zero mismatches. Finite evidence only, not a universal theorem. |
| Partial-correctness interpretation | Claim meaning | Termination is not generally established by this proof discipline. Here the fixed-length executions close; no general input theorem exists. |

There are no candidate-local opaque symbols, empirical result oracles,
unproved loop summaries, proof-local lemmas, or simplification rules to add to
the ledger.

Gate accounting for the theorem actually submitted:

- Gate A (real-program soundness and non-vacuity): **PASS**.
- Gate B (source-contract intent adequacy): **FAIL** due to finite/fixed list
  coverage, with an additional unproved exact-rational/float bridge.
- Gate C (auditability of the limited theorem): **PASS**, with all finite
  evidence explicitly bounded.

Kit terminology for this combination is `SOUND-BUT-LIMITED`. The benchmark
prompt explicitly maps material HumanEval domain narrowing to
`FAIL / NOT_LEGIT`, not to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
