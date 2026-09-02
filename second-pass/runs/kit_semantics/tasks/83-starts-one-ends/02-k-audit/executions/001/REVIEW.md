# Independent adversarial audit — 83-starts-one-ends

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full positive-integer contract domain. I independently rebuilt
the supplied semantics and proof definition from source, proved each target
claim separately and together, mechanically pinned the claims to the regenerated
program body, reviewed every K declaration and rule, and rejected both a fresh
body mutation and a fresh false-result mutation.

I did not rely on the candidate's `#Top` logs, compiled directories,
`PROOF.md`, generation trace, or final report.

## 1. Input and provenance integrity

### Record layout and required mounts

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`
- `problem_id`: `83-starts-one-ends`
- `condition`: `kit-semantics`
- `semantics_mode`: `SUPPLIED_SEMANTICS`
- `mount_reference_semantics`: `true`

This mode agrees with the mounts: `/reference/reference-semantics` exists. All
launcher-required pipeline-v3 records are readable regular files/directories:
`/run.json`, `/task.json`, `/generation-result.json`, all seven required
generation-evidence files, and the structured trace. The trace contains one
JSONL file with 254 parseable rows and zero malformed rows. See
`evidence/01_integrity_checks.log` and
`evidence/01_generation_record_summary.log`.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded lock hash.

Every launcher-declared single-file hash checked by
`evidence/01_integrity_checks.sh` matches its mount, including the canonical
implementation, prompt, translator, run/task/result manifests, invocation,
metrics, runtime metrics, usage, generation prompt, output log, and last
message. The generation-result per-file trace hash also matches.

The independently reproduced pipeline-v3 tree digests establish:

- candidate workspace:
  `6af3781781c45f2f6b47c63668ad8e31ffa5263efffde8d993911bb1dfb667f7`,
  matching the generation result;
- candidate and trusted semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  both matching the task input;
- trace tree:
  `3b5431f01509fb89b7ff6995a1c23eef09fd5222a830e9fc1f0b7ff79c263131`,
  matching `usage.json`.

The launcher also records distinct snapshot-digest fields. I did not use those
as truth: `evidence/integrity-manifests/` contains independent per-file
manifests, and direct type/content checks were applied to mounted inputs.

### Prompt, translator, and supplied-semantics integrity

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The candidate and trusted `reference-semantics/` trees each contain the same 24
regular files. `diff -qr --no-dereference` reports no difference. Neither tree
contains a symlink, extra entry, missing entry, mistyped entry, or changed
file. No candidate, generation-evidence, or trusted-reference symlink was
found.

All required proof artifacts are regular files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-built `runtime-kompiled/` and
`verification-kompiled/` trees were treated only as untrusted artifacts and
were never copied into scratch.

### Generation records

The generation records claim success, but were used only for provenance
inspection. The complete output log has 17,911 lines; the structured trace's
record/tool-type counts and hashes are in
`evidence/01_generation_record_summary.log`. All records required for
`pipeline-v3` are present. There is no audit-infrastructure breach.

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires, for every positive integer `n`, the number of
positive `n`-digit integers that start with `1` or end with `1`.

The trusted canonical implementation is:

```python
if n == 1:
    return 1
return 18 * (10 ** (n - 2))
```

The candidate is the expression-form equivalent:

```python
return 1 if n == 1 else 18 * 10 ** (n - 2)
```

For `n >= 2`, inclusion-exclusion gives the contract result:

- starting with `1`: `10^(n-1)`;
- ending with `1`: `9 * 10^(n-2)`;
- both: `10^(n-2)`;
- union: `10^(n-1) + 8 * 10^(n-2) = 18 * 10^(n-2)`.

For `n = 1`, the only qualifying one-digit number is `1`.

### Trusted regeneration

In fresh scratch, this exact command used the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

It exited 0. The regenerated and submitted files are byte-identical, both with
SHA-256
`d4630613fc4eed942749e77a1d3bddf32bd75802a6424bce22be92dcbe9843a2`.
See `evidence/02_program_fidelity.log`.

### Independent differential testing

`evidence/02_differential.py` independently imports the trusted canonical
entry point and candidate entry point. It checks:

- the minimum/branch boundary `n = 1`;
- the first else-branch input `n = 2`;
- ordinary and large fixed values through `n = 1000`;
- 250 deterministic generated inputs in `[1, 1000]` (232 unique total cases);
- direct decimal enumeration of the natural-language property for `n = 1..5`.

Command:

```text
python3 evidence/02_differential.py \
  /tmp/audit-work/83-audit.N7f3FW/trusted-canonical.py \
  /tmp/audit-work/83-audit.N7f3FW/solution.py
```

It exited 0 with zero differential mismatches and zero enumerated-property
mismatches. The prompt supplies no examples. An “empty” case is inapplicable
to a positive-integer scalar domain.

The implementation therefore preserves the signature, covers every intended
branch, agrees with the canonical implementation, and does not narrow the
source-contract domain.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

Fresh scratch was created at the path recorded in
`evidence/scratch-path.txt`. It initially contained only source copies,
`__pycache__`, and the trusted semantics tree—no kompiled definition. All K
builds below used K `v7.1.293`.

### Concrete definition

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

Exit: 0.

The reviewer-authored concrete program in
`evidence/03_concrete_review.py` checks `n = 1, 2, 3, 10`. It was translated
with the trusted translator, then run:

```text
krun reviewer-concrete.mpy \
  --definition reviewer-runtime-kompiled \
  --output none
```

Exit: 0.

### Proof definition and all positive claims

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

Exit: 0.

The two target claims were then run independently, preventing mutual target
claims from hiding a failure, and were also run together:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.starts-one-ends-one-digit
# exit 0; #Top

kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.starts-one-ends-multi-digit
# exit 0; #Top

kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC
# exit 0; #Top
```

Each output has exactly one line equal to `#Top`. Full bounded build/proof logs
and exact commands are in `evidence/03_reconstruction.log`.

Compiler warnings concern unused variables in `semantics/str.k` and
non-exhaustive functions in unused list/float/string/indexing fragments. No
warning concerns a target computation, stuck claim, or missing target rule.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.starts-one-ends-one-digit` starts in the standard module state with:

- argument `N : Int`;
- precondition `N ==Int 1`;
- `starts_one_ends` bound at module scope `0` to the submitted closure body;
- builtins at scope `-1`;
- empty heap and stack, `scopeLoc = 1`, `heapLoc = 0`, `noRet`, `NoExc`,
  and exit code `0`.

It requires the call to finish with `<k> 1 </k>` and the same stated cells.

`SPEC.starts-one-ends-multi-digit` has the same state and exact binding, with
precondition `N >Int 1`, and requires:

```text
18 *Int (10 ^Int (N -Int 2))
```

The preconditions are satisfiable (`N = 1` and `N = 2`) and partition every
positive K integer. They are unbounded; this is not an examples-only or
fixed-size theorem.

### Mechanical program identity

`evidence/04_constructor_pinning.py` tokenizes constructor syntax rather than
using textual line equality. It establishes:

- exact `Module(FuncDef("starts_one_ends", Params("n"), ...))` wrapper;
- exact 63-token `Return(IfExp(...))` body;
- exactly two occurrences of that body in `spec.k`;
- exactly two occurrences of the exact `closureVal("n", BODY, 0)` binding;
- exactly two symbolic calls to `starts_one_ends`.

All checks exited 0. Trusted regeneration had already established that the
submitted `solution.mpy` is the translator output.

The claims begin after module loading, which is permissible because the fixed
rules mechanically connect the real module to that state:

- `#loadAll(Module(SS)) => SS`;
- statement sequencing;
- `FuncDef(F, Params(PNS), BODY)` stores
  `closureVal(PNS, BODY, L)` in the current scope.

As a concrete cross-check, running the submitted `solution.mpy` through the
fresh LLVM definition ended with exactly the `starts_one_ends` closure in scope
`0`, parent `-1`, and every other claimed initial cell. The output is in
`evidence/04_pinning.log`.

There is no helper or loop claim. The actual call performs name lookup,
left-to-right argument evaluation, frame creation, parameter binding,
conditional selection, integer operations, return, frame deletion, and state
restoration under the supplied rules.

### Result constraint and ground substitution

Ground substitution produced:

| `n` | Formal claim | Trusted canonical | Candidate |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 18 | 18 | 18 |
| 7 | 1,800,000 | 1,800,000 | 1,800,000 |

The returned value is an equality target in `<k>`, not a free variable,
tautology, or one-way implication.

### Body sensitivity

`evidence/04_reviewer_body_mutation.k` changes coefficient `18` to `19` in the
closure body actually executed by the claim, while keeping the correct `n=3`
postcondition `180`. It does not merely edit an external source file.

The mutation dry-run exited 0. Its proof exited 1 with
`WarnStuckClaimState`; the final `<k>` value is `190`. See
`evidence/04_body_sensitivity.log`.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.md` lists the complete whitespace-collapsed source,
attributes, classification, and decision for every top-level K statement in:

- `reference-semantics/semantics.k`;
- all 23 helper files under `reference-semantics/semantics/`;
- `verification.k`;
- `spec.k`.

Inventory totals:

| Kind | Count |
|---|---:|
| syntax declarations | 227 |
| ordinary/equational rules | 695 |
| contexts | 5 |
| configurations | 1 |
| target claims | 2 |

There are no proof-local syntax declarations, functions, `total` or
`functional` declarations, opaque symbols, priorities, simplifications,
ordinary rules, or auxiliary claims in `verification.k`; it only imports the
fixed `MPY` module. No `[simplification]`, `[simp]`, or `functional`
declaration occurs in either the supplied semantics or verification file.

The reference semantics contain 22 `no-evaluators` opaque declarations and 35
concrete-only rules. None is reachable from this integer-only program.
`MPY-CONCRETE` is imported by the LLVM `MPY-KRUN` module, not by the Haskell
proof module `MPY`.

### Constructor-to-rule mapping

| Submitted construct | Declaration/behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` load/sequencing; `functions.k` exact closure binding |
| `Call(Name(...), N)` | `call.k` callee-first route; `core.k` lookup and left-to-right argument loop |
| function frame | `call.k` closure dispatch; `functions.k` parameter bind and pop |
| `Return` | strict expression evaluation; `functions.k` records result and restores caller |
| `IfExp` | condition strictness; complementary `truthy`/`notBool truthy` rules |
| `Compare(..., "==", ...)` | explicit left/right contexts; `operators.k` dispatch; `int.k` equality |
| `Int` and `Name` | `core.k` literal and scope-lookup rules |
| `BinOp("-", ...)` | sequential strictness; `operators.k`; `int.k` subtraction |
| `BinOp("**", ...)` | sequential strictness; guarded `int.k` exponentiation |
| `BinOp("*", ...)` | sequential strictness; `int.k` multiplication |

For the multi-digit claim, `N > 1` implies `N - 2 >= 0`, satisfying the
exponent rule's guard. K integers and CPython integers are unbounded for these
operations.

### Used-path soundness

The inventory marks 30 explicit rules, two contexts, 26 syntax declarations,
and the configuration as target-path items. Their effects are consistent:

1. Name lookup selects the pinned module binding.
2. The call rule evaluates the callee and the already-valued integer argument.
3. The closure rule creates scope `1`, pushes the exact continuation, and
   increments `scopeLoc`.
4. Parameter binding writes `n -> N` in that scope.
5. Equality selects exactly one `IfExp` branch.
6. The else branch executes subtraction, nonnegative exponentiation, and
   multiplication in source order.
7. Return discards the remaining function continuation, records the value, and
   `#pop` restores environment, stack, `scopeLoc`, and `noRet` while removing
   the callee scope.
8. No heap allocation, exception, or exit-code rule is reached.

The generic `Call` rule is `[owise]`, but all higher-priority call rules in the
fixed semantics require specific `math`/`hashlib`/builtin/method syntax and do
not match `Call(Name("starts_one_ends"), N)`. Reference-dereference priorities
do not match the integer values or plain scopes on this path. Guard overlaps
on the used conditional and integer rules are disjoint. The duplicate mixed
float equations elsewhere have equal right-hand sides and are unreachable.

### Remaining fixed rules and boundaries

The other 630 fixed ordinary rules, three contexts, and 179 non-opaque syntax
declarations concern constructors absent from `solution.mpy`: assertions,
booleans operations, floats, strings, sets, lists, tuples, dictionaries,
iteration, ranges, subscripts, comprehensions, methods, imports, sorting, and
builtins. Their LHS/function heads cannot replace a reachable target term.

The supplied semantics intentionally has limited or opaque behavior outside
the target fragment (notably floating-point operations, sorting, MD5, and
some totalized out-of-bounds/container functions). I classify this as an
explicit, unused language-model boundary, not a target-rule unsoundness. It
does not influence a branch, result, state, exception, or postcondition here.
Compiler non-exhaustiveness warnings are for those unused functions.

No rule mentions `starts_one_ends`, the task label, or the target formula. No
rule encodes the answer, inserts an oracle on the target path, skips the
program-defined body, or fabricates the result. There is therefore no claimed
unsound rule requiring a false-conclusion witness.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

I inspected but did not rely on the candidate's mutation files. The independent
artifact `evidence/06_reviewer_false_result.k` uses the exact original body and
the satisfying multi-digit input `n = 3`, but changes the required result from
`180` to `181`.

The independent Python witness reports:

```text
n = 3
multi_digit_precondition_n_gt_1 = True
trusted_value = 180
candidate_value = 180
false_mutated_target = 181
mutation_demonstrably_false = True
```

The mutation first built successfully:

```text
kprove reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT \
  --dry-run
# exit 0
```

Then the actual proof:

```text
kprove reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT
# exit 1
```

The failure is `WarnStuckClaimState`, not a parser/import/timeout/backend
error. The final configuration is otherwise complete and has
`<k> 180 ~> .K </k>`, which cannot unify with target `181`. Exact source,
commands, statuses, and bounded output are in
`evidence/06_nonvacuity.log`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied `MPY` semantics and the exact initial cells in `spec.k`:

- for every K integer `N` with `N == 1`, the submitted function call reaches
  result `1`;
- for every K integer `N > 1`, it reaches
  `18 * (10 ^ (N - 2))`;
- the environment, module/builtin scopes, allocation counters, empty heap,
  empty stack, return state, exception state, and exit code reach the stated
  destination values.

This is partial correctness. It does not establish a separate termination or
resource bound.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| trusted prompt and canonical implementation | intended domain/result | Acceptable benchmark authority; hashes checked |
| trusted `py2mpy.py` and CPython AST parsing | Python-to-constructor bridge | Acceptable; regeneration is byte-identical |
| supplied 24-file semantics | execution, values, control, cells | Acceptable selected semantics; exact tree integrity checked and used fragment reviewed |
| K `v7.1.293`, Haskell/LLVM backends, builtin integer theory | compilation, rewriting, proof closure | Standard unavoidable machine-checking trust |
| manual constructor comparison from module body to claim binding | real-program pinning | Mechanically checked by reviewer script and concrete module loading |
| inclusion-exclusion argument | formula-to-natural-language count | Ordinary mathematics outside K; canonical agrees and finite enumeration supports it |
| differential/enumeration tests | finite bridge evidence only | 232 canonical comparisons and `n=1..5` enumeration; not used as universal proof |
| float/sort/MD5/totalized container primitives | none on this target | Unused; explicitly excluded from the theorem's dependency set |

The simple inclusion-exclusion bridge is not encoded as a separate K theorem,
but it introduces no material adequacy gap: the K result is universally
constrained on the full input domain, is identical to the trusted canonical
result, and the bridge is a direct counting identity.

### Gate and decision mapping

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS.
- Gate C, trust/evidence auditability: PASS.

The proof is unbounded over all positive integers, result-constraining,
non-vacuous, and tied to the actual translated body. No material source-domain
restriction, substituted program, operational bridge, proof-local oracle, or
unsound target rule was found.

VERDICT: PASS
LEGITIMACY: LEGIT
