# Independent adversarial audit: 57-monotonic

## Outcome

The candidate contains a legitimate partial-correctness proof of the exact
submitted translated program over finite lists of mathematical integers. Fresh
LLVM and Haskell definitions built from copied source, the original four claims
closed, each claim also closed independently, and a fresh false-result mutation
was rejected for the expected semantic reason.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
formal theorem states monotonicity through equality with an insertion-sort
result, while the equivalence of that predicate to the prompt's English
adjacent-order property remains an ordinary-mathematics argument rather than a
separate K theorem. The generated semantics also intentionally models only the
integer-list fragment exercised by this program. These are scope and bridge
limitations; neither permits a false conclusion about the submitted program on
the formal input domain.

All candidate prose, logs, traces, and compiled trees were treated as untrusted.
All executable audit work used source copied to
`/tmp/audit-work/review-57`; candidate-provided compiled definitions and caches
were not reused.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required condition holds:
`/reference/reference-semantics` does not exist and is not a symlink. No hidden
or inferred reference semantics was sought or used. This is recorded in
[stage1_integrity.log](evidence/stage1_integrity.log).

There is therefore no infrastructure contradiction and a candidate verdict is
appropriate.

### Required artifacts and symlinks

The following required candidate artifacts are present, nonempty regular files,
and not symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`, `prove.sh`
- the structured generation trace at
  `/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-14-42-019f8952-09f1-7763-a225-2b722207253e.jsonl`

No symlink occurs anywhere under `/candidate`. There are no additional helper K
source files to audit. The extra `build/`, `__pycache__/`, and trace/log trees
are generated outputs or provenance records, not source-integrity failures;
they were excluded from reconstruction.

The candidate prompt is byte-identical to `/reference/prompt.py` (SHA-256
`5656ff21e3b01209978415c290235784e32350405706cebc0045defa6271dd99`).
The candidate translator is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
Those hashes also agree with the untrusted `run-input.json` claims.

### Untrusted generation claims

`metrics.json` claims a 501-second successful generation run.
`codex-last.txt` and `codex-output.log` claim that the examples ran and the
combined proof printed `#Top`; the 186-record JSONL trace contains the same
claim and shows intermediate failed compilation attempts followed by a claimed
successful final run. These records were read as provenance only. No verdict
depends on their reported success or on any `/candidate/build` content.

No required source artifact is missing, changed relative to its trusted
counterpart, mistyped, or symlinked. Full commands, hashes, file types, and exit
statuses are in [stage1_integrity.log](evidence/stage1_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt asks for `monotonic(l: list)` to return `True` when the list
is monotonically increasing or monotonically decreasing. Repeated adjacent
values are allowed: the trusted canonical implementation returns

```python
l == sorted(l) or l == sorted(l, reverse=True)
```

Thus the intended predicate is nondecreasing-or-nonincreasing, including empty,
singleton, and constant lists.

The trusted canonical at `/reference/canonical.py:7` uses an `if` around that
predicate. The candidate at `/candidate/solution.py:1` returns the same
predicate directly. Since both equality operations produce booleans, these are
extensionally identical. The signature and entry-point name are preserved.

The formal K input domain is narrower and explicit: finite `IntList` values
whose elements are mathematical `Int`s. That covers the integer examples and
the usual HumanEval domain, but does not claim Python behavior for floats,
strings, mixed types, custom comparison objects, or exceptional comparisons.
The prompt's annotation says only `list`, so this narrowing is one documented
reason for `CONCERNS`.

### Translator fidelity

The submitted `solution.mpy` was regenerated with the trusted translator:

```text
python3 /tmp/audit-work/review-57/trusted/py2mpy.py \
  /tmp/audit-work/review-57/src/solution.py \
  > /tmp/audit-work/review-57/build/solution.trusted-regenerated.mpy
```

`cmp -s` exited 0. Both files have SHA-256
`defbbe28aa5bde39b5092455096db10e76684b1ab0401e4e6a08151ef2de27b7`.
See [stage2_translate.sh](evidence/stage2_translate.sh) and
[stage2_translate.log](evidence/stage2_translate.log).

### Independent differential test

[stage2_differential.py](evidence/stage2_differential.py) independently imports
the trusted canonical and the scratch-copied candidate. It checks:

- all three documented examples;
- empty, singleton, constant, duplicate, two-element, peak, and valley cases;
- large positive and negative Python integers;
- every list of lengths 0 through 7 over `(-2, -1, 0, 1, 2)`;
- a separately implemented adjacent-pair characterization.

The exact generated scope comprises 97,656 lists. Results were 1,548 `True`,
96,108 `False`, and zero mismatches. The command exited 0; complete explicit
cases and counts are in
[stage2_differential.log](evidence/stage2_differential.log).

This finite test supports program/canonical fidelity. It is not substituted for
the K proof or for a universal semantics correspondence theorem.

## 3. Clean proof reconstruction

### Clean source and toolchain

Only these source files were copied from the candidate:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. Trusted inputs were separately copied from `/reference`.
No candidate `*-kompiled` directory, cache, bytecode, trace, or proof output was
copied into a build path.

The live tools are K version `v7.1.293`.

### Concrete semantics build and execution

The generated semantics was freshly compiled with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/review-57/build/semantic-llvm-kompiled
```

It exited 0. See
[stage3_build_concrete.log](evidence/stage3_build_concrete.log).

[stage3_concrete_compare.py](evidence/stage3_concrete_compare.py) then invoked
that fresh definition on ten inputs: empty, singleton, duplicates, increasing,
decreasing, nonmonotonic peak/valley, negative/duplicate boundaries, and
arbitrarily large integers. For every input, the K boolean equaled both the
candidate Python result and the trusted canonical result. There were zero
mismatches and the script exited 0. Exact `krun` commands and outputs are in
[stage3_concrete_compare.log](evidence/stage3_concrete_compare.log).

### Proof definition and positive claims

The proof definition was freshly compiled with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition \
  /tmp/audit-work/review-57/build/verification-haskell-kompiled
```

It exited 0. See [stage3_build_proof.log](evidence/stage3_build_proof.log).

The untouched copied `spec.k` was first proved as a whole:

```text
kprove spec.k \
  --definition /tmp/audit-work/review-57/build/verification-haskell-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`; see
[stage3_prove_original_all.log](evidence/stage3_prove_original_all.log).

Because the candidate claims are unlabeled, the reviewer also created
[spec-audit.k](evidence/spec-audit.k), changing only formatting and adding
labels so each semantically identical claim could be selected independently.
Each command exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| Universal finite-integer-list claim | [stage3_prove_universal.log](evidence/stage3_prove_universal.log) |
| Increasing example | [stage3_prove_example-increasing.log](evidence/stage3_prove_example-increasing.log) |
| Nonmonotonic example | [stage3_prove_example-nonmonotonic.log](evidence/stage3_prove_example-nonmonotonic.log) |
| Decreasing example | [stage3_prove_example-decreasing.log](evidence/stage3_prove_example-decreasing.log) |

The dynamic reconstruction gate passes. The following stages determine whether
the freshly reconstructed `#Top` is meaningful.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

1. **Universal claim, `/candidate/spec.k:7`.** There is no explicit `requires`.
   K infers `L : IntList` from `listVal(L)`. Starting with the exact embedded
   program and argument `listVal(L)`, the sole `<k>` cell must become
   `#monotonicSpec(L)`. Expanding that function fixes the result to:

   ```text
   boolVal(
     eqIntLists(L, sortInts(L))
     or
     eqIntLists(L, reverseInts(sortInts(L))))
   ```

2. **Increasing example, `/candidate/spec.k:13`.** With
   `[1, 2, 4, 20]`, the required result is exactly `boolVal(true)`.
3. **Nonmonotonic example, `/candidate/spec.k:20`.** With
   `[1, 20, 4, 10]`, the required result is exactly `boolVal(false)`.
4. **Decreasing example, `/candidate/spec.k:27`.** With
   `[4, 1, 0, -10]`, the required result is exactly `boolVal(true)`.

There are no omitted state cells, helper claims, loop claims, invariants,
existential result variables, implications, or unconstrained output variables.
The language configuration has only the `<k>` cell because the submitted
computation is pure; the environment is an explicit evaluator argument.

Every precondition is satisfiable. For the universal claim, `L = nil` is a
witness. Each example's displayed constructor list is its own witness. Concrete
substitution gives: `nil -> true`, the prompt's mixed-order list -> false, and
the prompt's descending list -> true. The fresh K executions and both Python
implementations agree on all three substitutions and additional cases in
[stage3_concrete_compare.log](evidence/stage3_concrete_compare.log).

### Exact program identity

The pinning chain is:

```text
solution.py
  --trusted py2mpy.py-->
solution.mpy
  --token identity-->
verification.k's solutionProgram AST
  --SEMANTIC evaluator-->
claimed result
```

[stage4_program_identity.py](evidence/stage4_program_identity.py) independently
extracts the balanced `Module(...)` right-hand side of the
`solutionProgram` equation and compares K tokens outside strings. The submitted,
trusted-regenerated, and embedded terms each contain 213 normalized token
characters and are identical. See
[stage4_program_identity.log](evidence/stage4_program_identity.log).

The actual execution path is:

```text
#run -> #apply -> #findFunction -> #applyFunction -> #exec(Return)
     -> #eval(BoolOp)
     -> #eval(Compare/Call) -> sort/reverse/equality -> #boolOr
```

It therefore executes the exact translated return expression. No proof rule
replaces that expression with an oracle or precomputed task answer.

### Result strength

The result is constrained to a concrete boolean predicate of the original
input. `#monotonicSpec` is not opaque: its sole equation exposes the complete
predicate, and every result-bearing helper on the exercised path has executable
equations. Although the specification deliberately uses the same
sorted-list characterization as the trusted canonical, that is an independently
validated task specification, not a free variable or a circular opaque symbol.

The remaining limitation is that the K file does not separately formalize an
adjacent-pair `<=`/`>=` predicate and prove it equivalent to the sorted-list
characterization. That bridge is mathematically standard and was tested
independently, but it remains outside the reachability theorem.

## 5. Rule-by-rule static soundness review

The complete line-numbered source and attribute search are preserved in
[stage5_inventory.log](evidence/stage5_inventory.log). There are 30 local rules:
28 in `semantic.k` and 2 in `verification.k`.

### Syntax and configuration inventory

| Location | Local declaration(s) | Role and assessment |
|---|---|---|
| `semantic.k:6` | `Pgm ::= Module(Stmts)` | Exact translator module node; used. |
| `semantic.k:8` | juxtaposed `Stmts` list | Represents the translator's statement sequence; used by the one function and one return. |
| `semantic.k:9-10` | `FuncDef`, `Return` | Exact used statement constructors. |
| `semantic.k:12-16` | `Strings`, `Params`, `Exprs`, `CmpOps` lists | Exact constructor-list payloads used by parameters, calls, boolean operations, and comparisons. |
| `semantic.k:18-23` | `Name`, `Bool`, `BoolOp`, `Compare`, `Call`, `KwArg` | Every expression constructor in `solution.mpy`; no used expression constructor is missing. |
| `semantic.k:25` | `CmpOp` | Carries the translated `==`; used twice. |
| `semantic.k:28-31` | `nil`, `cons`, `boolVal`, `listVal` | Finite mathematical-integer lists and the only observable values. |
| `semantic.k:40` | `<k> #run($PGM,$ARG) </k>` | One-cell pure configuration. No heap, output, allocation identity, or mutable state is observable in this program. |
| `semantic.k:44-45` | internal `function(Params,Stmts)`, `env(String,Val)` | Function-body and one-parameter binding representations. |
| `semantic.k:47` | `#findFunction` `[function]` | Defined on every function-search case reachable here. |
| `semantic.k:54` | operational `#run(Pgm,Val) : KItem` | Ensures the entry transition is an actual semantic rewrite. |
| `semantic.k:56-61` | `[function]` symbols `#apply`, `#applyFunction`, `#exec`, `#eval`, `#equals`, `#boolOr` | Pure evaluator layers; all exercised applications are covered. |
| `semantic.k:98` | `#asIntList` `[function]` | Checked conversion for the only input value form. |
| `semantic.k:103-104` | `#sortInts`, `#insertInt` `[function]` | Executable insertion sort over mathematical integers. |
| `semantic.k:114-115` | `#reverseInts`, `#appendInts` `[function]` | Executable finite-list reverse and append. |
| `semantic.k:123` | `#eqIntLists` `[function]` | Structural integer-list equality. |
| `verification.k:9` | `solutionProgram` `[function]` | Definitional AST constant, independently token-pinned to `solution.mpy`. |
| `verification.k:30` | `#monotonicSpec` `[function]` | Fully exposed result predicate; not an execution shortcut. |

No local declaration has `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, `[macro]`, `[owise]`, `priority`, `anywhere`, `fresh`, or
`opaque`. The `[function]` attribute is present on 15 symbols; it controls
equational evaluation and is not itself treated as a truth proof.

### Exhaustive rule inventory and decisions

| Rule | Domain/effect | Decision |
|---|---|---|
| `semantic.k:48-49`, matching `#findFunction` head | Returns that head's parameters/body; ignores only later definitions. | Sound for lexical module search and the submitted first/only function. |
| `semantic.k:50-52`, mismatching `#findFunction` head | Recurses only when names differ. | Sound; guard is disjoint from the preceding equation and recursion descends. |
| `semantic.k:63-64`, `#run(Module(FUNS),ARG)` | Selects entry point `"monotonic"` and preserves argument/functions. | Sound task runner; entry name matches the trusted signature. |
| `semantic.k:66-67`, `#apply` | Finds the named body, then applies it. | Sound on the present binding; no result is fabricated. |
| `semantic.k:68-69`, `#applyFunction` | Binds the sole parameter to the already supplied value and enters the body. | Sound for the actual one-parameter function; no argument side effects exist at this runner boundary. |
| `semantic.k:71-72`, `#exec(Return(E) REST,...)` | Evaluates `E` and discards later statements. | Correct Python return control for this pure function. |
| `semantic.k:74`, name evaluation | Looks up exactly the sole `env(N,V)` binding. | Sound for `Name("l")`; an unbound/different name visibly remains unmodeled. |
| `semantic.k:75`, boolean literal | Produces `boolVal(B)`. | Sound. |
| `semantic.k:79-80`, two-operand `"or"` | Evaluates both expressions and combines them. | Sound on the submitted context because both operands are pure, boolean, total comparisons. It is not a complete model of Python short-circuiting outside this context. |
| `semantic.k:81-82`, `#boolOr` | Uses K `orBool` on two boolean values. | Sound and complete on exercised calls. |
| `semantic.k:84-85`, one-link `==` comparison | Evaluates both sides and calls value equality. | Sound for the two exact list comparisons. |
| `semantic.k:86-87`, list equality | Returns structural `#eqIntLists`. | Sound for integer lists. |
| `semantic.k:90-91`, one-argument `sorted` | Evaluates the list and applies ascending insertion sort. | Sound for the unshadowed Python builtin in the submitted module. |
| `semantic.k:92-96`, `sorted(..., reverse=True)` | Evaluates the list, sorts ascending, reverses. | Sound for the exact pure literal-keyword call. |
| `semantic.k:99`, `#asIntList(listVal(L))` | Extracts the represented list. | Sound; wrong value kinds remain visibly unmodeled. |
| `semantic.k:105`, sorting `nil` | Returns `nil`. | Correct base case. |
| `semantic.k:106`, sorting `cons` | Sorts the tail, then inserts the head. | Correct insertion-sort recursion; structural descent is on the finite tail. |
| `semantic.k:108`, insertion into `nil` | Produces a singleton. | Correct base case. |
| `semantic.k:109-110`, insertion when `I <= J` | Places `I` before the sorted list. | Correct. Guard is disjoint from the next rule. |
| `semantic.k:111-112`, insertion when `I > J` | Keeps `J` and recurses into its tail. | Correct; together with `<=` it exhausts mathematical integer order and structurally descends. |
| `semantic.k:116`, reversing `nil` | Returns `nil`. | Correct base case. |
| `semantic.k:117-118`, reversing `cons` | Reverses tail and appends the head singleton. | Correct finite-list reverse; recursion descends. |
| `semantic.k:119`, appending to `nil` | Returns second list. | Correct base case. |
| `semantic.k:120-121`, appending `cons` | Preserves head and appends the tail. | Correct; recursion descends. |
| `semantic.k:124`, equality `nil,nil` | Returns true. | Correct. |
| `semantic.k:125`, equality `nil,cons` | Returns false. | Correct. |
| `semantic.k:126`, equality `cons,nil` | Returns false. | Correct. |
| `semantic.k:127-128`, equality `cons,cons` | Conjoins head equality with tail equality. | Correct; the four shape cases are pairwise disjoint and exhaustive for constructor lists. |
| `verification.k:10-26`, `solutionProgram` | Expands to the complete submitted AST. | Sound definitional alias; exact token identity was independently checked. |
| `verification.k:31-35`, `#monotonicSpec` | Names equality with ascending sort or descending sort. | Truthful definitional specification; complete one-equation coverage over `IntList`. It does not preempt program execution. |

### Used-construct coverage and control/state analysis

Every constructor in `solution.mpy` maps to the declarations above and to an
applicable evaluator rule. Every internal value/function reached from those
rules also has an applicable equation. On finite constructor `IntList`s,
recursive calls strictly decrease list length. The two guarded insertion rules
are disjoint and exhaustive; function-search rules are disjoint by string
equality; expression rules are constructor/arity-disjoint; equality rules are
shape-disjoint.

The semantics preserves the only observable result. Python `sorted` allocates a
fresh list, but object identity is never tested and neither input nor output
state is mutated, so omitting heap/allocation cells cannot affect this boolean.
There is no exception on finite lists of mathematical integers. Return control
correctly discards the unused suffix.

Two language-wide limitations were checked narrowly:

- Eager `or` can get stuck on an unmodeled second operand even when Python
  would short-circuit after `True`; for example, a synthetic
  `BoolOp("or", Bool(true), Name("unbound"))`. This is an incompleteness witness,
  not a false-result witness, and that term is not reachable in the submitted
  program.
- The `sorted` rules recognize the textual builtin name directly and do not
  model arbitrary rebinding. The submitted module contains no `sorted`
  definition or binding, so builtin selection is fixed on every intended run.

Neither limitation enables a false conclusion for any finite-integer-list
execution of the submitted program. Accordingly, no rule is labeled unsound
and there is no missing required false-conclusion witness. They remain
documented reasons not to treat this as a reusable full Python semantics.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or relied upon. The reviewer created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) with the satisfiable input
`L = nil` and the deliberately false postcondition:

```text
#run(solutionProgram, listVal(nil)) => boolVal(false)
```

The mutation first passed a `kprove --dry-run` compilation with exit 0; see
[stage6_mutation_dry_run.log](evidence/stage6_mutation_dry_run.log).

The actual proof command then exited 1. It produced
`WarnStuckClaimState` with the terminal residual:

```text
<k>
  boolVal ( true ) ~> .K
</k>
```

This is exactly the unmet result obligation: the semantics computed `true`,
which cannot unify with required `false`. There was no parser error, missing
import, timeout, or unrelated crash. See
[stage6_mutation_proof.log](evidence/stage6_mutation_proof.log).

The positive proof is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly compiled generated K theory, for every K `IntList` term `L`
in the exercised constructor domain, evaluation of the exact submitted
`solution.mpy` AST with argument `listVal(L)` reaches the boolean saying that
`L` equals its ascending insertion-sort result or the reverse of that result.
The three displayed prompt instances reach their stated booleans.

This is a partial-correctness result. It is not a general theorem about all
Python values or the whole Python language. Structural descent makes
termination on finite constructor lists evident from the audited equations,
but termination is not promoted into a separate theorem claim.

### Proof-local extensions

| Extension | Class | Value/control influence | Justification and dependents |
|---|---|---|---|
| `solutionProgram` | Definitional summary of syntax | Selects the complete body evaluated by all four claims. | Exact token identity with trusted-regenerated `solution.mpy`; it skips no execution. |
| `#monotonicSpec` | Definitional result summary | Fixes the universal claim's returned boolean. | One exhaustive equation over `IntList`; uses only the audited sort/reverse/equality functions. |

There are no proof-local operational bridges, derived lemmas, helper
reachability claims, circularities, fresh values, unconstrained oracles, opaque
result symbols, priorities, or simplification axioms.

### Trust ledger and limitations

| Boundary | Status | Dependents/evidence |
|---|---|---|
| K parser, compiler, Haskell/LLVM backends, and imported `BOOL`, `INT`, `STRING` builtins | Trusted primitive/tool boundary | All executions and proofs. Fresh builds and cross-backend concrete/proof runs reduce stale-cache risk. |
| K mathematical `Int` order and equality correspond to Python arbitrary-precision integer order/equality | Acceptable semantic bridge | Sort, equality, and final result. Direct static correspondence plus negative and very large integer concrete tests. |
| The local insertion-sort equations implement Python `sorted` on integer lists | Acceptable, not separately machine-proved | Both sorted calls and `#monotonicSpec`. Exhaustive rule review and ten fresh K-versus-two-Python concrete comparisons; finite testing is not claimed universal. |
| Trusted translator maps `solution.py` AST to `solution.mpy` | Trusted supplied component | Real-program identity. Candidate/trusted translator byte identity and fresh output byte identity. |
| Embedded `solutionProgram` is the submitted translated program | Deterministically checked bridge | All claims. Token-level equality artifact and byte-identical trusted regeneration. |
| Equality with ascending sort or descending sort means nondecreasing or nonincreasing | Ordinary-mathematics/intent bridge | Interpretation of `#monotonicSpec` as the English contract. It follows from finite total-order sorting, is exactly the trusted canonical criterion, and is independently tested against an adjacent-pair oracle, but is not a separate K theorem. |
| Input scope | Explicit limitation | Proof covers finite mathematical-integer lists, not every object accepted by a Python `list` annotation. |
| Concrete differential evidence | Finite empirical evidence only | 97,656 candidate/canonical/relation-oracle tests; ten K/candidate/canonical tests. It supports but does not replace the universal reachability proof or semantic reasoning. |

### Validation gates

- **Gate A — real-program soundness: PASS.** Exact program pinning, full used
  evaluator coverage, no unsound proof extension, constrained result, and a
  meaningful rejected false mutation.
- **Gate B — intent adequacy: PASS with limitation.** The theorem matches the
  trusted canonical on finite integer lists. The sorted-predicate/English
  equivalence and broader Python-list types are not separately formalized.
- **Gate C — trust and auditability: PASS with limitation.** Commands, scripts,
  source mutations, outputs, and exit statuses are preserved. The generated
  semantics bridge has strong static support and bounded concrete evidence, not
  a universal CPython correspondence theorem.

Those limitations do not create a material soundness or real-program-pinning
gap, so the proof remains legitimate. They do warrant the `CONCERNS` qualifier.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
