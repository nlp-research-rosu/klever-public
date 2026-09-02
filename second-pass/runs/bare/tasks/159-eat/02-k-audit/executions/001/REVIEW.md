# Independent adversarial audit — 159-eat

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program. The proof rebuilds and closes from source,
the formal result is exact, and the program term in the claim is structurally
identical to the trusted translation of `solution.py`.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, for two bounded reasons:
several helper declarations claim `[total]` beyond the syntax/type cases covered
by their equations, and the bridge between this individually generated minimal
semantics and CPython is a rule-by-rule informal argument supported by finite
testing rather than a machine-checked Python-semantics theorem. Neither issue
creates a false task result on the submitted program. In particular, the whole
spec still proves after every local `total` attribute is removed.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` does not exist. No
hidden or inferred reference semantics was used. The boundary check is recorded
in [stage1_integrity.log](evidence/stage1_integrity.log).

The following required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. There are no symlinks anywhere
under `/candidate`. There are no missing, mistyped, or wrong-type required
artifacts.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values agree with the values claimed in `run-input.json`. Exact hashes
and type checks are in [stage1_integrity.log](evidence/stage1_integrity.log).

The additional top-level directories `semantic-kompiled/` and
`verification-kompiled/` are untrusted generated caches, not source
deliverables. They were not copied or used. `codex-trace/` is additional
provenance evidence, not proof evidence. The JSONL trace contains 367 valid
records; the generation log and final message claim successful concrete and
proof runs. Those claims were read but were not relied on. A bounded extraction
is in [trace_summary.log](evidence/trace_summary.log), produced by
[trace_summary.py](evidence/trace_summary.py). The untrusted `metrics.json`
claims exit 0 and no timeout; this likewise played no part in the verdict.

All executable source needed for reconstruction was copied to
`/tmp/audit-work/159-eat/candidate-src`, and trusted inputs were copied to
`/tmp/audit-work/159-eat/trusted`. No candidate-built definition or cache was
reused.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted natural-language contract has integer inputs
`number`, `need`, and `remaining`, each in `0..1000`. The result is a two-element
list:

- if `need <= remaining`, return
  `[number + need, remaining - need]`;
- otherwise, return `[number + remaining, 0]`.

This is exactly the behavior of `/reference/canonical.py`.
`/candidate/solution.py` implements the same two branches, preserves the
required `eat(number, need, remaining)` signature, and uses no unsupported
construct.

Running the trusted translator on the copied `solution.py` produced a byte
stream identical to the submitted `solution.mpy`; both have SHA-256
`49f9697d0fa8809c3144fc5b812d49e68db0cdbb56b74617e8c089e0a8c6e78a`.
The exact check is in [translator_identity.log](evidence/translator_identity.log).

The independent differential test
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and candidate entry point by separate file paths. It
also compares both to the independently written formula using
`min(need, remaining)`. Its scope was:

- all four documented examples;
- eleven zero, equality, adjacent-branch, and `0`/`1000` boundary cases;
- every pair `(need, remaining)` in `0..1000 × 0..1000` for
  `number` in `[0, 1, 500, 999, 1000]`;
- 20,000 deterministic generated triples over the full documented cube,
  using seed `1592026`.

All 5,030,020 comparisons agreed, including exact Python list/int types.
[differential_test.log](evidence/differential_test.log) records exit 0 and zero
mismatches. This is strong finite fidelity evidence, not a substitute for the
K proof.

## 3. Clean proof reconstruction

The available tools are K `v7.1.293` (build date 2025-10-03); see
[toolchain.log](evidence/toolchain.log).

The concrete definition was rebuilt from the copied source, with no candidate
cache:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/159-eat/semantic-audit-kompiled
```

It exited 0 with no diagnostic output
([build_semantic.log](evidence/build_semantic.log)). Fresh `krun` executions of
the actual copied `solution.mpy` were compared with both Python implementations
on all four examples and eight additional normal/boundary inputs. All twelve
K executions exited 0 and matched, including `need = remaining` and
`need = remaining + 1`; see
[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) and
[concrete_semantics_compare.log](evidence/concrete_semantics_compare.log).

The proof definition was independently rebuilt:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/159-eat/verification-audit-kompiled
```

It exited 0 with no diagnostic output
([build_verification.log](evidence/build_verification.log)). The original
candidate spec then produced `#Top` and exit 0:

```text
kprove spec.k \
  --definition /tmp/audit-work/159-eat/verification-audit-kompiled \
  --spec-module SPEC
```

See [kprove_all_claims.log](evidence/kprove_all_claims.log).

Every positive target claim was also copied verbatim into a separate module in
[spec-isolated.k](evidence/spec-isolated.k) and run independently:

| Claim | Scope | Exit | Output |
|---|---|---:|---|
| 1 | symbolic `need <= remaining` branch | 0 | `#Top` |
| 2 | symbolic `remaining < need` branch | 0 | `#Top` |
| 3 | example `(5,6,10)` | 0 | `#Top` |
| 4 | example `(4,8,9)` | 0 | `#Top` |
| 5 | example `(1,10,10)` | 0 | `#Top` |
| 6 | example `(2,11,5)` | 0 | `#Top` |

The bounded exact logs are
[claim 1](evidence/kprove_claim_1.log),
[claim 2](evidence/kprove_claim_2.log),
[claim 3](evidence/kprove_claim_3.log),
[claim 4](evidence/kprove_claim_4.log),
[claim 5](evidence/kprove_claim_5.log), and
[claim 6](evidence/kprove_claim_6.log).

There was no timeout, container failure, or other infrastructure uncertainty
in the reconstruction.

## 4. Adequacy and real-program pinning

The first symbolic claim says: for bounded inputs with
`need <= remaining`, executing the submitted program reaches the two-component
contract result `(number + need, remaining - need)`. The second says: for
bounded inputs with `remaining < need`, it reaches
`(number + remaining, 0)`. These guards are disjoint and exhaustive for integer
`need` and `remaining`. The four remaining claims state the four documented
ground results without extra preconditions.

The result is not free or tautological. `carrotContract` has two guarded
equations in `verification.k`; each rewrites to a fully determined `result`,
and the claim requires the executed `<k>` computation to reach that exact
destination. The contract symbol appears only on the destination side and does
not rewrite any program operation.

The real-program identity chain is:

1. the trusted translator output is byte-identical to submitted
   `solution.mpy`;
2. [program_term_identity.py](evidence/program_term_identity.py) extracts the
   RHS of the `solutionProgram` rule, normalizes only the rule-syntax spelling
   `.Stmts` to the corresponding concrete empty-list field, parses both terms
   with `kast`, and obtains byte-identical KORE
   ([program_term_identity.log](evidence/program_term_identity.log));
3. the `<k>` cell begins with `run(solutionProgram, args(...))`;
4. `solutionProgram` expands to that exact parsed tree, and the ordinary
   `run`/evaluator rules execute its real body.

[krun_actual_depth0.log](evidence/krun_actual_depth0.log) independently shows
the initial parsed `$PGM` constructor tree for the submitted file. An
exploratory attempt to parse the proof-only literal `solutionProgram` through
the concrete main syntax module failed, as expected; that parser diagnostic in
`krun_solutionProgram_depth0.log` was not used as evidence. The successful
KORE comparison above performs the relevant identity check.

Concrete satisfying states and substitutions include:

| Entry claim | Satisfying input | Claimed result | Canonical / candidate Python / fresh K |
|---|---|---|---|
| symbolic branch 1 | `(5,6,10)` | `result(11,4)` | all `(11,4)` |
| symbolic branch 2 | `(2,11,5)` | `result(7,0)` | all `(7,0)` |
| ground example 1 | `(5,6,10)` | `result(11,4)` | all `(11,4)` |
| ground example 2 | `(4,8,9)` | `result(12,1)` | all `(12,1)` |
| ground example 3 | `(1,10,10)` | `result(11,0)` | all `(11,0)` |
| ground example 4 | `(2,11,5)` | `result(7,0)` | all `(7,0)` |

The implementation has no loop and the spec has no helper, loop, circularity,
or lemma claims. Every claim starts at the actual entry computation.

As a separate body-sensitivity probe, the reviewer changed the true-branch
first component to `number + need + 1`. Trusted translation then failed the
program-identity check, fresh `krun` on `(5,6,10)` produced `result(12,4)`, and
a well-formed reachability claim demanding the old `result(11,4)` failed with a
stuck state containing `result(12,4)`. Evidence:
[mutation source](evidence/solution-body-mutated.py),
[identity log](evidence/body_mutation_identity.log),
[concrete log](evidence/body_mutation_krun.log),
[dry run](evidence/body_mutation_dry_run.log), and
[failed proof](evidence/body_mutation_kprove.log).

## 5. Rule-by-rule static soundness review

[rule-inventory.md](evidence/rule-inventory.md) is the exhaustive inventory.
It enumerates every local syntax alternative, configuration cell, function and
`total` attribute, all 21 rules in `semantic.k`, all four rules in
`verification.k`, and all six claims. There are no other candidate helper K
sources. There are no local `[functional]`, `[simplification]`, priority,
`owise`, macro, alias, hook, freshness, or explicit opaque-symbol declarations.

Every construct in `solution.mpy` is covered:

| Used construct | Declaration | Executing rules |
|---|---|---|
| `Module` / exact `FuncDef` / `Params` | `semantic.k` 6, 9, 13 | entry rule S21 |
| statement list / fall-through / early return | lines 8, 39-40 | S12-S15 |
| `If` | line 11 | S17-S19 |
| `Compare` with singleton `CmpOp("<=")` | lines 19, 22-23 | S6, S10-S11 |
| `Name` and parameter bindings | line 17 | S1, S3, S21 |
| `Return` | line 10 | S16, S15 |
| two-element `ListExpr` | lines 20, 24 | S7, S20 |
| `BinOp("+")` and `BinOp("-")` | line 18 | S4-S5, S8-S9 |
| `Int(0)` | line 16 | S2 |

The configuration has only `<mpy><k>...</k></mpy>`. An explicit immutable `Map`
argument contains the three bindings. The program has no assignment, mutable
collection operation, call expression, exception-producing operation, I/O,
heap observation, or other state that would require an omitted cell.

The arithmetic rules use unbounded K integers, matching Python integers for
this domain. The two comparison guards are disjoint and exhaustive. Statement
sequencing correctly evaluates the first statement, falls through after the
empty `else`, and propagates `returned(V)` without executing the later return.
Nested expression evaluation has no explicit Python evaluation context, but
all actual subexpressions are pure map reads and integer operations, so order
cannot affect value, control, state, or exceptions here. `resultOf` projects
exactly a returned two-integer list to the observable two-component result; it
does not choose either component.

The entry `run` rule is the language-harness bridge. It matches exactly one
module-level `eat` definition with the required parameter names, binds the
three integer arguments, and executes the captured body. It neither contains
the carrot formula nor bypasses the `If`, expression, or return rules. For this
pure content-only task, omission of Python function-object allocation and list
identity is observationally irrelevant.

The proof-layer rules are soundly classified:

- V1/V2 are definitional postcondition equations. They state the expected
  property but do not participate in program execution; their guards are
  disjoint and exhaustive.
- V3 is an exact transcription of the three prompt bounds.
- V4 names the exact submitted program term, as independently checked in
  Stage 4.

No rule replaces a property-bearing program computation with an oracle, no
fresh/opaque value influences a branch or result, and no rule silently
fabricates behavior for an unmodeled construct used by the program.

The evidence gap is the breadth of several `[total]` declarations. Their
equations do not document arbitrary absent-key lookups, unsupported expression
operator/cardinality shapes, non-integer arithmetic operands, nested
`FuncDef` statements, non-Boolean conditions, or non-two-integer returns. None
of those cases is reachable from this exact program and integer input domain.
I do **not** label these declarations materially unsound: I found no concrete
or symbolic false task-result conclusion witness enabled by them. More
importantly, the reviewer mechanically removed every local `total` attribute,
rebuilt the definition successfully, and the entire original spec still
produced `#Top`:
[attribute diff](evidence/no_total_variant_diff.log),
[build](evidence/build_no_total.log), and
[proof](evidence/kprove_no_total.log). Thus successful closure does not depend
on the over-broad coverage claims.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted or reused. The
reviewer created [spec-vacuity.k](evidence/spec-vacuity.k), a fresh mutation of
the first symbolic branch. It changes the required first result component from
`NUMBER + NEED` to the false `NUMBER + NEED + 1` while retaining the original
bounded/equality-side precondition. The concrete state `(5,6,10)` satisfies
that precondition and reaches `result(11,4)`, whereas the mutation demands
`result(12,4)`.

The mutation first built successfully with `kprove --dry-run` and exit 0
([vacuity_dry_run.log](evidence/vacuity_dry_run.log)). The real proof command
then exited 1 with `WarnStuckClaimState`. Its residual contains the correctly
reached symbolic state
`result(NUMBER +Int NEED, REMAINING -Int NEED)` and the failed implication
requiring:

```text
NUMBER +Int NEED +Int 1 #Equals NUMBER +Int NEED
```

See [vacuity_kprove.log](evidence/vacuity_kprove.log). This is an expected
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation. The original proof is discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the submitted K semantics, for every integer triple in the documented
`0..1000` domain:

- when `need <= remaining`, execution of the exact translated program reaches
  `result(number + need, remaining - need)`;
- when `remaining < need`, it reaches
  `result(number + remaining, 0)`.

The four examples are also independently proved as ground instances. The
symbolic claims partition the complete intended input domain. This is a
partial-correctness reachability result under the supplied semantic theory; it
is not a theorem about arbitrary Python syntax or inputs outside the prompt
domain.

### Trust and assumption ledger

| Boundary | Influence | Support | Assessment |
|---|---|---|---|
| K `INT`, `BOOL`, `STRING`, `MAP`, parser, Haskell backend, and `kprove` | arithmetic, maps, symbolic execution, proof result | standard installed K v7.1.293; fresh rebuild | acceptable low-level tool/builtin trust |
| Trusted `py2mpy.py` | connects `solution.py` text to `solution.mpy` AST | byte-identity regeneration | acceptable trusted input; it does not supply semantics or the task result |
| `solutionProgram` identity | selects the body proved | parsed KORE identity with submitted `.mpy`; mutation sensitivity | acceptable and exact |
| `run` entry harness | invocation, argument binding, start of body | exact rule review; fresh concrete tests; body mutation | acceptable for this pure exact signature |
| Generated expression/statement semantics | control and returned values | exhaustive used-construct review plus twelve fresh K/Python comparisons | sound for every construct/path used; connection to CPython is informal rather than a universal Python theorem |
| K integer arithmetic versus Python integers | all numeric results and branch guard | both are unbounded for these operations; 5,030,020 differential cases | acceptable |
| `resultOf` list-content projection | final observable result | direct two-int constructor equation; task observes list content only | acceptable; list allocation/identity is outside the property |
| Broad `[total]` annotations | possible definedness reasoning outside used subset | proof still closes after all are removed | concerning documentation/coverage gap, but not a dependency or material soundness defect |
| Canonical/differential execution | implementation-to-intent bridge on tested values | trusted canonical plus independent formula, zero mismatches | finite empirical support only; not used as the K proof |

There are no remaining opaque symbols, program-derived oracles, trusted
proof-local lemmas, operational shortcut rules, loop invariants, or
unmachine-checked claims contributing to proof closure. `carrotContract`,
`validInput`, and `solutionProgram` all have inspected equations; every
reachable semantic helper has an applicable inspected equation.

The generated-semantics-to-CPython bridge is the principal limitation:
rule-by-rule reasoning makes it compelling for this tiny pure program, and the
large differential campaign supports it, but the K proof itself proves
execution under `semantic.k`, not a universal refinement theorem against a
full formal CPython semantics. Together with the over-broad but nonessential
`total` annotations, this warrants `CONCERNS` under the stated decision
boundary. It does not amount to a material adequacy gap, execution bypass,
vacuity, substituted program, or false-result witness, so the proof remains
legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
