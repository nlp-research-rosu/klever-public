# Independent adversarial audit: HumanEval 121

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I reconstructed every definition from source, independently
proved every positive claim, confirmed exact program pinning, and obtained the
expected failure from a fresh false-result mutation.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
bridge from this bespoke, program-focused semantics to CPython is necessarily
reviewer-validated rather than machine-proved. In addition, one generic helper
rule is broader than the submitted program needs: it models `%` using
Euclidean `modInt` for every divisor, which differs from Python for negative
divisors. The submitted AST fixes the divisor at positive `2`, so that
overbreadth cannot affect a task-domain execution or the theorem.

## 1. Input and provenance integrity

### Trusted-mount boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted `/reference` tree
contains exactly the three regular files expected at this boundary:
`canonical.py`, `prompt.py`, and `py2mpy.py`. In particular,
`/reference/reference-semantics` does not exist. There is therefore no
infrastructure contradiction and no hidden/supplied semantics was sought or
used. The tree, types, hashes, comparisons, and JSON checks are recorded in
[01_integrity.log](/audit-output/evidence/01_integrity.log).

The candidate's `prompt.py` is byte-identical to
`/reference/prompt.py` (SHA-256
`f5c091f79c729b97c5ed96f86e84d4d3ebee2ccae5b5ab192e98f6e265df18d5`).
Its `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

### Candidate artifacts and untrusted provenance claims

The following required/used artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The structured generation trace is
also a regular JSONL file and parses without error. No symlink exists anywhere
in the candidate tree. There is no missing, changed, mistyped, or symlinked
required artifact.

The candidate also contains `__pycache__` and three prebuilt `*-kompiled`
directories. Those are extra generated caches, not source inputs; I did not copy
or use them. There is no candidate `spec-vacuity.k` to credit.

I read `run-input.json`, `metrics.json`, both Codex text logs, and every JSONL
trace event only as untrusted generation claims. Their bounded hashes, event
counts, claimed commands, and claimed status are in
[00_provenance_untrusted.log](/audit-output/evidence/00_provenance_untrusted.log).
The untrusted material claims a bare run and prior `#Top`; neither claim was
used as proof evidence.

All source execution occurred from source-only copies under
`/tmp/audit-work/candidate-src`; trusted Python inputs were separately copied to
`/tmp/audit-work/trusted`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `solution(lst)` for a non-empty list of integers.
It must sum the odd-valued elements at zero-based even positions: indices
`0, 2, 4, ...`. The zero-based interpretation is fixed both by the examples
and by the trusted canonical implementation, which filters
`enumerate(lst)` using `idx % 2 == 0` and `x % 2 == 1`.

The candidate implements:

```python
def solution(lst):
    return sum([x for x in lst[::2] if x % 2 != 0])
```

For integer elements this is equivalent: `lst[::2]` selects exactly the
zero-based even positions, and `x % 2 != 0` selects exactly odd integers,
including negative odd integers. Handling the empty list by returning zero is a
sound extension beyond the stated non-empty domain.

### Trusted translation identity

I regenerated `solution.mpy` from the scratch copy of `solution.py` with the
trusted translator. The regenerated and submitted files are byte-identical,
both with SHA-256
`a55f820888905adcf823d46ef45309212d34c6901f266d3e4acd991cd5ff3507`.
The exact command, hashes, comparison, and exit 0 are in
[02_translate_identity.log](/audit-output/evidence/02_translate_identity.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and candidate functions from distinct explicit paths. Its
inputs are preserved in
[differential_inputs.json](/audit-output/evidence/differential_inputs.json):

- the three documented examples;
- empty, singleton, parity, sign, length, skipped-position, and very-large-int
  boundaries;
- every list of length 0 through 6 over `[-3,-2,-1,0,1,2,3]`;
- 1,000 deterministic random lists of lengths 0 through 30 with values in
  `[-1,000,000,1,000,000]`.

All 138,272 cases matched, including all documented expected values. The run
had exit 0 and mismatch count zero:
[03_differential.log](/audit-output/evidence/03_differential.log). This is
finite implementation-to-canonical evidence, not a replacement for the K
proof.

## 3. Clean proof reconstruction

K v7.1.293 was independently located and version-checked; see
[04_toolchain.log](/audit-output/evidence/04_toolchain.log).

### Concrete definition and generated-semantics execution

From source only, I ran:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/semantic-llvm-kompiled
```

It exited 0:
[05_kompile_semantic_llvm.log](/audit-output/evidence/05_kompile_semantic_llvm.log).
The fresh definition path is outside `/candidate`.

The reviewer-authored
[semantic_concrete_test.py](/audit-output/evidence/semantic_concrete_test.py)
then executed the submitted `solution.mpy` with that fresh definition on 15
normal and boundary lists. These exercise empty, singleton included/excluded,
two-or-more included/excluded, skipped odd positions, negative integers, and
arbitrary-size integers. Each `krun` command exited 0; every K result equaled
both independent Python results. Failure count was zero:
[06_semantic_concrete.log](/audit-output/evidence/06_semantic_concrete.log).

### Proof definition and every positive claim

From source only, I ran:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-haskell-kompiled
```

It exited 0:
[07_kompile_verification_haskell.log](/audit-output/evidence/07_kompile_verification_haskell.log).

The aggregate proof independently printed `#Top` and exited 0:
[08_kprove_all.log](/audit-output/evidence/08_kprove_all.log). I also selected
every target claim separately. Each printed `#Top` and exited 0:

| Claim | Evidence |
|---|---|
| `SPEC.example-one` | [09_kprove_example-one.log](/audit-output/evidence/09_kprove_example-one.log) |
| `SPEC.example-two` | [10_kprove_example-two.log](/audit-output/evidence/10_kprove_example-two.log) |
| `SPEC.example-three` | [11_kprove_example-three.log](/audit-output/evidence/11_kprove_example-three.log) |
| `SPEC.all-integer-lists` | [12_kprove_all-integer-lists.log](/audit-output/evidence/12_kprove_all-integer-lists.log) |

No candidate-built definition, cache, prior trace, or prior `#Top` contributed
to these results.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All claims have no separate `requires` clause. Their typed source
configurations are satisfiable.

| Claim | Precondition/source state | Required postcondition |
|---|---|---|
| `example-one` | Exact submitted program, cursor/original `[5,8,7,1]`, accumulator 0 | `result(12)`, preserving the surrounding computation frame |
| `example-two` | Exact program, cursor/original `[3,3,3,3,3]`, accumulator 0 | `result(9)`, same frame |
| `example-three` | Exact program, cursor/original `[30,13,24,321]`, accumulator 0 | `result(0)`, same frame |
| `all-integer-lists` | Exact program, any constructor integer-list cursor `INPUT`, any original integer list, and any integer `ACC` | `result(expected(INPUT,ACC))`, same frame |

The universal claim is stronger than the external entry contract because it
covers empty lists and arbitrary internal accumulators/original-list values.
The real initial configuration is the included special case
`ORIGINAL = INPUT` and `ACC = 0`. Allowing arbitrary `ORIGINAL` is sound here
because the submitted body and guard depend only on the bound element `x`, not
on `lst`.

### Exact real-program pinning

The `<k>` terms use the `solutionProgram` nullary function. Its sole equation is
the full translated AST. The reviewer check normalizes only whitespace and
finds that RHS exactly identical to submitted `solution.mpy`, with matching
normalized SHA-256
`aac42fb33fd6cb7f7cb7d32a9d56a15671c39454cc181035c3b8c3134dd17c19`;
see [pinning_check.py](/audit-output/evidence/pinning_check.py) and
[13_pinning.log](/audit-output/evidence/13_pinning.log). Coupled with the
trusted byte-identical regeneration in Stage 2, the proof term pins the real
generated program rather than a substitute.

The operational rules retain that program term while consuming two cursor
cells per recursive step. They evaluate the captured comprehension `BODY` and
`COND`; neither value is replaced by an oracle. Reviewer mutations changing
the body to zero and the condition to false changed the concrete result from
12 to 0, as required:
[14_operational_sensitivity.log](/audit-output/evidence/14_operational_sensitivity.log).
A separate reachability witness shows an immediate `result(999)` continuation
is preserved rather than discarded:
[audit-witness.k](/audit-output/evidence/audit-witness.k) and
[15_audit_witness.log](/audit-output/evidence/15_audit_witness.log).

### Satisfying witnesses and result constraint

The three concrete claim LHS configurations are direct satisfying states. For
the universal claim, I used:

```text
INPUT = ORIGINAL = [-5, 2, -3], ACC = 10
```

Both Python implementations return `-8` on that list, so the instantiated
claim requires `-8 + 10 = 2`. The ground K witness reached exactly `result(2)`
and printed `#Top` in
[15_audit_witness.log](/audit-output/evidence/15_audit_witness.log).

Every postcondition fixes a concrete integer or the fully defined recursive
function `expected(INPUT,ACC)`. There is no RHS-only free result, existential
oracle, tautology, or implication that can avoid equality of the returned
integer.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule/claim inventory is
[rule_inventory.md](/audit-output/evidence/rule_inventory.md). It enumerates
all 35 local syntax/function declarations, the configuration, all 20 semantic
rules, all 6 verification equations, and all 4 claims. There are no submitted
helper K files.

There are no local `total`, `functional`, `simplification`, `concrete`,
priority, `owise`, freshness, or opacity declarations. There are no
proof-local ordinary rewrites, auxiliary claims, or uninterpreted
result-bearing symbols.

### Construct and control-flow coverage

Every constructor in `solution.mpy` is mapped in the inventory:
`Module`, `FuncDef`, `Params`, `Return`, `Call`, `Name`, `ListComp`,
`CompFor`, `Subscript`, `Slice`, `NoBound`, `Int`, `Compare`, `BinOp`, and
`CmpOp`. Runtime integer lists use only `nil` and `cons`.

The sole `<k>` cell is adequate for this pure function: there is no
program-visible mutation, heap, output, allocation identity, exception, or
call stack to preserve on the intended integer-list domain. The fused run
rules omit temporary slice/comprehension list allocation, but that allocation
is unobservable because the body and condition are pure and the sole consumer
is integer `sum`.

The run cases are disjoint and exhaustive over constructor lists:

- empty cursor returns the accumulator;
- singleton true/false cases optionally add the body value;
- length-at-least-two true/false cases optionally add the current value, skip
  the next list element, and recurse on the tail.

The guard pairs are complementary after `testAt` produces a `Bool`. Program,
original input, accumulator, and continuation are preserved or updated exactly
as listed. Cursor length decreases by two. Environment construction binds the
comprehension variable over the parameter, matching Python shadowing. All
actual lookups are bound; the body is `x`; the condition computes
`x mod 2 != 0`.

The `expected` equations use the same mathematically correct structural split,
with mutually exclusive parity guards and decreasing recursion. The universal
reachability claim itself is the circularity applied when a transition reaches
the same `run(solutionProgram, REST, ORIGINAL, updatedACC)` shape. No helper
claim bypasses real execution.

### Generated-semantics limitation

Rule `semantic.k:59-60` declares a generic
`eval(BinOp("%",LEFT,RIGHT),ENV)` and implements it with K's Euclidean
`modInt`. For positive divisor `2`, this agrees with CPython for every integer
dividend, including negative list values, so it is sound on every reachable
submitted-program execution.

It is over-broad as a reusable Python rule. CPython gives `1 % -2 == -1`,
while this rule proves `intVal(1)` for that alternate expression. The concrete
off-program witness and successful K claim are in
[semantic-overbreadth.k](/audit-output/evidence/semantic-overbreadth.k) and
[16_semantic_overbreadth.log](/audit-output/evidence/16_semantic_overbreadth.log).
No intended list input can put `-2` in the divisor position: exact pinning
fixes `RIGHT` to `Int(2)`. I therefore classify this as a narrower generated
language-model limitation, not a false conclusion witness for the real program
on its intended domain. It is nevertheless a reason for `CONCERNS`; the rule
should have been narrowed to the supported positive-divisor case.

No inventoried rule can enable a false result for the exact submitted AST and
an integer-list input. The fused operational rules are low-level,
body-sensitive execution rules, not a smuggled task answer: they neither refer
to `expected` nor return an unconstrained/new summary value.

## 6. Fresh non-vacuity test

I created a fresh mutation,
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), that keeps
the realizable first-example source state but changes the required result from
12 to 13.

First, `kprove --dry-run` parsed and translated the mutation successfully with
exit 0:
[17_vacuity_dry_run.log](/audit-output/evidence/17_vacuity_dry_run.log). The
actual proof then exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet result obligation:

```text
<k>
  result ( 12 ) ~> _DotVar1 ~> .K
</k>
```

The complete bounded failure is
[18_vacuity_failure.log](/audit-output/evidence/18_vacuity_failure.log). This is
not a parser error, missing import, timeout, unrelated crash, or unreachable
mutation. The documented input satisfies the source state, both Python
implementations return 12, and the K semantics reaches 12.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the audited submitted K definition, the proof establishes partial
correctness of the exact translated program:

- each documented configuration reaches its documented integer result; and
- for every finite constructor integer-list cursor and integer accumulator,
  `run(solutionProgram, INPUT, ORIGINAL, ACC)` reaches
  `result(expected(INPUT,ACC))`.

For the real initial state (`ORIGINAL = INPUT`, `ACC = 0`), `expected` is the
recursive sum of the values at positions `0,2,4,...` whose remainder modulo 2
is nonzero. Thus, if the modeled execution terminates, its returned integer
meets the prompt contract. The claim is result-constraining and body-sensitive.

This is a partial-correctness theorem, not a proof of all CPython behavior or a
separate total-correctness theorem. It excludes non-list inputs, non-integer
elements, Python subclasses/overloaded operators, mutation/concurrency, and
unmodeled exceptions. Those behaviors are outside the prompt's intended
domain.

### Trust ledger

| Boundary | What is assumed; dependents | Assessment/evidence |
|---|---|---|
| K compiler, Haskell/LLVM backends, and reachability kernel | Correct parsing, compilation, execution, and proof checking; all claims depend on this | Standard acceptable proof-kernel/toolchain boundary; version and exact runs are preserved. |
| Imported `INT`, `BOOL`, and `STRING` primitives | Arbitrary mathematical integers, `+Int`, positive-divisor `modInt`, integer/string equality, and Boolean negation | Acceptable low-level primitives. Positive-divisor modulo is the only reachable `%` case. |
| Trusted CPython-AST translator | `solution.py` is represented by submitted `solution.mpy` | Accepted mounted input and independently rerun; byte identity established. |
| `solutionProgram` alias | The spec's program term is the submitted translation | Not merely assumed: exact normalized identity is recorded in Stage 4. |
| Generated semantics-to-CPython bridge | R01–R20 faithfully model this exact pure expression over integer lists | Audited rule by rule and supported by 15 K/Python boundary executions plus body/guard/continuation sensitivity. It is not a machine-checked theorem against official Python semantics; this is the principal concern. |
| `expected`-to-natural-language bridge | Recursive step-two parity sum means “odd elements at even positions” | Direct structural mathematical argument, documented examples, and the 138,272-case independent canonical differential. The finite differential is supporting evidence only. |
| Off-program `%` behavior | Generic negative-divisor expressions would be modeled incorrectly | Concerning but non-dependent: exact submitted AST fixes divisor `2`; no target claim can reach the counterexample. |

There is no opaque symbol, unconstrained oracle, empirical value injected into
the proof, or informal helper lemma on which claim closure depends.
`PROOF.md`, prior logs, traces, differential tests, and concrete runs were not
substituted for the K proof. They support only provenance, the finite
implementation/semantics bridges, non-vacuity, and adequacy.

The remaining limitations are documented and non-material to the theorem about
the exact generated program. The clean proof is sound and pins the real
program; the bespoke semantics bridge warrants concerns but not rejection.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
