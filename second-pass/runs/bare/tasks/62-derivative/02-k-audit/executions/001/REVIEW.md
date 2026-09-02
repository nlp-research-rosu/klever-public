# Independent adversarial review: 62-derivative

## Decision

The proof reconstructs and is result-constraining under the submitted generated K semantics. The exact translated program tree is pinned, the helper theorem is obtained by executing the real recursive body, and a fresh false-result mutation is rejected for the expected semantic reason.

The result is not a clean PASS because the K language is an idealized, principally integer-valued subset of CPython. In particular, on the valid finite input `list(range(998))`, the K program and trusted canonical implementation return the 997-element derivative, while the submitted `solution.py` raises `RecursionError`. The prompt gives no length bound. The K model also cannot represent floats and does not implement Python's boolean multiplication even though the Python implementation and canonical function accept those cases.

I classify these as limitations of the normal-termination and intent bridge, rather than a proof-local false equation: no tested normally returned Python value disagreed with the canonical value, and the requested theorem is partial correctness rather than total correctness or absence of exceptions. The proof is therefore legitimate for the exact program under the stated idealized K execution model, with material concerns about its bridge to unrestricted CPython behavior.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree: `/reference/reference-semantics` is absent, as required for `GENERATED_SEMANTICS`. There is no infrastructure breach.

All required candidate inputs are regular files, not symlinks: `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the JSONL generation trace, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. The structured trace parses completely. No required artifact is missing or mistyped.

The submitted [prompt.py](/candidate/prompt.py) is byte-identical to `/reference/prompt.py` (SHA-256 `2ed91e...33331`), and the submitted [py2mpy.py](/candidate/py2mpy.py) is byte-identical to `/reference/py2mpy.py` (SHA-256 `406485...db16`). Exact comparisons, hashes, artifact types, parsed untrusted metadata, bounded claim-bearing log lines, and trace record counts are in [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log).

The candidate also contains generated `semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, and a `.pyc`. These are extra build/cache artifacts, not trusted source artifacts. They were identified and excluded from reconstruction. I read `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the trace only as untrusted claims. Their claims included a prior `#Top`, four concrete runs, an AST comparison, and 500 random tests; none was reused as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says `xs[i]` is the coefficient of \(x^i\), and the result must contain the derivative coefficients in the same representation. Thus, for `xs = [c0, c1, ..., cn]`, the required value is `[1*c1, 2*c2, ..., n*cn]`. The trusted canonical implementation is exactly `[(i * x) for i, x in enumerate(xs)][1:]`.

The submitted implementation drops `xs[0]`, starts `degree` at one, and recursively emits `degree * xs[0]` while advancing through the tail. For every normally completing plain-list call, this is extensionally the same computation as the canonical implementation.

### Translation identity

I regenerated `solution.mpy` in scratch with the trusted translator:

`python3 /tmp/audit-work/audit-62/trusted-py2mpy.py /tmp/audit-work/audit-62/solution.py > /tmp/audit-work/audit-62/regenerated-solution.mpy`

The command exited 0, and `cmp` against the submitted `solution.mpy` exited 0. See [translator_regeneration.log](/audit-output/evidence/translator_regeneration.log) and [translator_byte_identity.log](/audit-output/evidence/translator_byte_identity.log).

### Independent differential test

The reviewer-authored [differential_test.py](/audit-output/evidence/differential_test.py) independently imports `/reference/canonical.py:derivative` and the scratch copy of the submitted entry point. It covers:

- both documented examples;
- empty, singleton, two-element, zero, negative, huge-integer, float, and boolean cases;
- every empty/nonempty branch boundary;
- 680 seeded generated integer lists of lengths 0 through 16;
- 108 seeded generated float lists of lengths 0 through 8;
- recursion-boundary lists of lengths 998 and 1100.

The exact scope and all inputs/outcomes are preserved in [differential_inputs_results.json](/audit-output/evidence/differential_inputs_results.json). The run found 799 matching outcomes and two mismatches:

| Input | Trusted canonical | Submitted Python |
|---|---|---|
| `list(range(998))` | returns 997 values | raises `RecursionError` |
| `list(range(1100))` | returns 1099 values | raises `RecursionError` |

The command exited 1 because mismatches are deliberately fatal; see [differential_test.log](/audit-output/evidence/differential_test.log). This invalidates any universal CPython-equivalence claim. It does not exhibit an incorrect *returned* value, so for partial correctness it is a termination/exception limitation. For the natural-language task as an unrestricted executable function, it is nevertheless material.

The separate [ground_witnesses.log](/audit-output/evidence/ground_witnesses.log) records exact agreement for `[]`, `[7]`, both examples, a two-element negative case, and a three-element negative case.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/audit-62`; no candidate definition, cache, compiled KORE, interpreter, or `.pyc` was copied or referenced. The installed tools are K `v7.1.293`; see [toolchain_versions.log](/audit-output/evidence/toolchain_versions.log).

### Fresh concrete definition

The LLVM definition was built from `semantic.k`:

`kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm -o semantic-audit-kompiled`

It exited 0 ([kompile_semantic_llvm.log](/audit-output/evidence/kompile_semantic_llvm.log)). Fresh `krun` executions returned:

| Input | Fresh K result | Evidence |
|---|---|---|
| `[3,1,2,4,5]` | `[1,4,12,20]` | [krun_doc1.log](/audit-output/evidence/krun_doc1.log) |
| `[1,2,3]` | `[2,6]` | [krun_doc2.log](/audit-output/evidence/krun_doc2.log) |
| `[]` | `[]` | [krun_empty.log](/audit-output/evidence/krun_empty.log) |
| `[7]` | `[]` | [krun_singleton.log](/audit-output/evidence/krun_singleton.log) |
| `[5,-3]` | `[-3]` | [krun_two.log](/audit-output/evidence/krun_two.log) |
| `[-2,4,-6]` | `[4,-12]` | [krun_negative.log](/audit-output/evidence/krun_negative.log) |

The long-input witness is especially informative. For `list(range(998))`, fresh K execution exits 0 at a normal `ListV(...) ~> .K`, contains 997 values, and exactly equals `[i*i for i in 1..997]`; canonical Python returns the same list, while submitted Python raises `RecursionError`. See the reviewer script [long_input_k_witness.py](/audit-output/evidence/long_input_k_witness.py) and successful [long_input_k_witness_fixed.log](/audit-output/evidence/long_input_k_witness_fixed.log). The earlier [long_input_k_witness.log](/audit-output/evidence/long_input_k_witness.log) is preserved transparently: its inner K run exited 0, but the first reviewer regex failed to parse whitespace in the output; this was a harness error corrected in the fixed run.

### Fresh proof definition and positive claims

The Haskell proof definition was built from source:

`kompile verification.k --main-module VERIFICATION --syntax-module VERIFICATION --backend haskell -o verification-audit-kompiled`

It exited 0 ([kompile_verification_haskell.log](/audit-output/evidence/kompile_verification_haskell.log)). The parsed, macro-expanded submitted `solution.mpy` and `solutionProgram` terms compare byte-for-byte equal ([program_ast_identity.log](/audit-output/evidence/program_ast_identity.log)).

Every claim closes in an appropriate fresh positive run:

| Selection | Exit | Output | Evidence |
|---|---:|---|---|
| `helper-correct` | 0 | `#Top` | [kprove_helper_correct.log](/audit-output/evidence/kprove_helper_correct.log) |
| `derivative-empty` | 0 | `#Top` | [kprove_derivative_empty.log](/audit-output/evidence/kprove_derivative_empty.log) |
| `helper-correct,derivative-nonempty` | 0 | `#Top` | [kprove_nonempty_with_dependency.log](/audit-output/evidence/kprove_nonempty_with_dependency.log) |
| complete `SPEC` | 0 | `#Top` | [kprove_all_claims.log](/audit-output/evidence/kprove_all_claims.log) |

An audit diagnostic selecting only `derivative-nonempty` omitted its helper circularity from the selected set and recursively unrolled until the auditor interrupted it with status 130. This is preserved in [kprove_derivative_nonempty.log](/audit-output/evidence/kprove_derivative_nonempty.log); it is not the valid positive target. Selecting the nonempty claim together with its declared dependency closes immediately.

Clean proof reconstruction therefore passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

There are no textual `requires` clauses. The sort constraints are the preconditions.

1. `helper-correct`: for every finite K sequence `CS`, every mathematical integer `N`, and every continuation `K`, calling the exact `derivative_helper` closure on `(ListV(CS), IntV(N))` reaches `ListV(#differentiate(N, CS))` and preserves the same continuation.
2. `derivative-empty`: running the exact program on `ListV([])` reaches `ListV([])`.
3. `derivative-nonempty`: for every first value `C0` and finite tail `CS`, running the exact program on `ListV(C0, CS...)` reaches `ListV(#differentiate(1, CS))`.

For an integer tail `[c1,...,cn]`, the two exhaustive equations for `#differentiate` reduce the third result to `[IntV(1*c1), ..., IntV(n*cn)]`. The result is not a free variable, tautology, implication, or oracle. For non-integer `Value` elements, the summary can contain an unreduced `#bin`; consequently, the claim is a useful returned-value theorem only on the supported integer fragment.

Satisfying states are immediate: `#run(solutionProgram,ListV(.Values))` witnesses the empty claim; `ListV(IntV(7))` witnesses the nonempty shape with empty `CS`; and `ListV(IntV(3),IntV(1),IntV(2),IntV(4),IntV(5))` witnesses a nonempty result-bearing case. The fresh K and both Python implementations agree on the corresponding expected values, as shown in the concrete and ground logs above.

### Exact program pin

The `<k>` claims execute `solutionProgram`, a macro whose full constructor tree is the submitted two-function program. The independent expanded-KORE comparison proves this tree is exactly the parsed submitted `solution.mpy`. As a sensitivity check, changing only the initial helper degree from `Int(1)` to `Int(2)` makes that comparison fail at byte 1477; see [solution-program-mutation.mpy](/audit-output/evidence/solution-program-mutation.mpy) and [program_ast_mutation_rejected.log](/audit-output/evidence/program_ast_mutation_rejected.log).

The pin is therefore real but external to `kprove`: `kprove` executes the exact embedded macro tree, and the separately audited `kast` comparison connects that tree to the file. The trusted-translator regeneration then connects the file to `solution.py`.

### Adequacy limitation

The entry preconditions include every finite K list, but the generated semantics has an unbounded abstract call mechanism and no stack or exception state. The concrete length-998 witness satisfies the K precondition and returns in K, while actual CPython raises. Because the property under review is partial correctness, this does not demonstrate a wrong normal return. It does show that the proof cannot establish termination, exception freedom, or unrestricted CPython equivalence.

## 5. Rule-by-rule static soundness review

The complete numbered source and mechanical declaration scan are preserved in [static_inventory.log](/audit-output/evidence/static_inventory.log).

### Syntax, configuration, and attributes

Local syntax is exhaustive as follows:

- `Pgm`: `Module(Stmts)`.
- Sequence and statement sorts: `Stmts` list; `Stmt` has `FuncDef`, `Return`, and `If`.
- Parameters and argument syntax: `Params`, `Strs`, and `Exprs` lists.
- `Expr`: `Int`, `Bool`, `Str`, `Name`, `ListExpr`, `BinOp`, `Compare`, `Call`, and `Subscript`.
- Comparison/index syntax: `CmpOps`, `CmpOp`, an expression or `Slice` index, and expression/`NoBound` slice bounds.
- Runtime data: `IntV`, `BoolV`, `StrV`, `ListV`, `NoneV`, finite `Values`, and `closure`.
- Runtime/control terms: `#prepend`, `#run`, `#call`, `#exec`, `#choose`, `#eval`, `#bin`, `#equal`, `#head`, `#tail`, `#evalArgs`, `#concat`, `#collect`, and `#bind`.
- Verification syntax: `solutionProgram`, `solutionFunctions`, and `solutionFuns` macros; `#differentiate`.

The only configuration is `<mpy><k>...</k></mpy>`. Environments and the function table are explicit term arguments, so there is no omitted mutable state cell. The modeled fragment has no heap, I/O, exceptions, or resource/stack counter.

There are 12 local `[function]` declarations: `#run`, `#choose`, `#eval`, `#bin`, `#equal`, `#head`, `#tail`, `#evalArgs`, `#concat`, `#collect`, `#bind`, and `#differentiate`. None is declared `total`. There are three `[macro]` declarations. There are no local `total`, `functional`, `simplification`, `concrete`, priority, `owise`, `anywhere`, or opaque declarations. `#call` and `#exec` are ordinary semantic terms. Partial functions visibly stick outside their equations rather than fabricating values.

Every constructor used by `solution.mpy` is covered: module/function collection, parameter binding, function calls, both return shapes, empty/nonempty `if`, integer/name/list/binop evaluation, equality with `[]`, named calls, index zero, slice `[1:]`, argument sequencing, integer addition/multiplication, list concatenation, head, and tail.

### Ordinary semantic rules

The following inventory assigns a disposition to all 41 rules in `semantic.k`.

| IDs and rules | Disposition |
|---|---|
| S1 `#run(Module...)`; S2-S3 `#collect` empty/cons | Sound for the target: load the exact module and collect its two uniquely named closures. Duplicate-name behavior is partial but unreachable here. |
| S4-S5 `#bind` empty/cons | Sound pointwise binding for the exact matching arities. Mismatched arity visibly sticks. |
| S6 `#call` | Sound for the target's unique function map: selects the named closure and executes its body with a fresh immutable environment. It idealizes an unbounded call stack; the length-998 CPython witness is the documented model-level exception gap. |
| S7 return-list; S8 return-call | Sound for the exact return forms and correctly discard unreachable remaining statements after `Return`. |
| S9 specialized list-plus-call return; S10 `#prepend` | Extensionally sound for this program's pure integer computation and makes the recursive call explicit. S9 actually evaluates the recursive right operand before evaluating `LEFT`, contrary to its comment and CPython's left-before-right order. Here `LEFT` is the pure, total-on-`IntV` expression `degree * xs[0]`, environments are immutable, and there is no observable state, so no false result witness exists on the intended integer domain. This is an over-broad/order-fidelity concern, not a witnessed unsound conclusion for this program. |
| S11-S12 empty/nonempty `xs == []`; S13 empty statement sequence | The two list shapes are disjoint and exhaustive and select the correct branch. S13 returns `NoneV` only for a genuinely empty body. |
| S14-S15 `#choose` true/false | Truthful and disjoint, but unused by the submitted control flow. |
| S16-S18 integer/boolean/string literals; S19 name lookup; S20 list expression | Constructor-correct. Name lookup is guarded by an actual binding; list evaluation uses the explicit finite argument sequence. Bool/string literal rules are unused. |
| S21 binary expression; S22 single `==`; S23 named call | Truthfully delegate to the corresponding helpers for the used shapes. Evaluation ordering is not separately state-observable in this pure fragment. Other operators, chained comparisons, and non-name calls visibly stick. |
| S24 index zero; S25 slice `[1:]` | Correct for the only two submitted subscript forms. Empty head has no equation, but the real branch calls it only after proving nonempty. |
| S26-S27 argument evaluation empty/cons | Structurally exhaustive and terminating on finite `Exprs`. It preserves source order at the sequence level; any backend interleaving is immaterial because expressions have no modeled state. |
| S28 integer `+`; S29 integer `*`; S30 list `+` | Exact unbounded-integer arithmetic and finite list concatenation for used operands. Float and Python bool arithmetic are absent rather than assigned false values. |
| S31-S32 concatenation empty/cons | Disjoint, exhaustive, structurally decreasing, and mathematically correct. |
| S33-S35 same-constructor int/bool/string equality | Correct for those same-type values. Only list-versus-empty equality is used by the program. |
| S36 empty-list equality; S37 nonempty-vs-empty; S38 empty-vs-nonempty | Disjoint and correct. Nonempty-vs-nonempty and cross-type equality are unmodeled, not falsely modeled. |
| S39 list head; S40-S41 tail empty/nonempty | Correct finite-list destructors. The head rule is deliberately partial on empty. |

No ordinary rule encodes the derivative answer, bypasses the submitted body, introduces a free oracle, or alters an unmodeled observable cell.

### Verification-local rules and claims

| IDs and rules | Disposition |
|---|---|
| V1 `solutionProgram`; V2 `solutionFuns`; V3 `solutionFunctions` | Macro definitions, not execution shortcuts. V3 is exactly the submitted AST; the independent identity and mutation checks validate the pin. V2 invokes the ordinary `#collect`. |
| V4 `#differentiate(N,.Values)` | True base equation; disjoint from V5. |
| V5 `#differentiate(N,(C,CS))` | True mathematical recurrence. It decreases the finite sequence, has no overlap with V4, and fixes every integer result through S29. For unsupported values it preserves a visible partial `#bin` rather than choosing an answer. |
| C1 `helper-correct` | A derived circularity over the exact closure body. The empty/nonempty semantic split decreases `CS`; the recursive call returns to the exact claim shape with `N+1` and a framed `#prepend` continuation. The sole configuration cell is preserved. |
| C2 `derivative-empty`; C3 `derivative-nonempty` | Exact entry summaries using C1. Empty and nonempty finite lists are exhaustive, and the nonempty result is fixed by V4-V5. |

There are no proof-local operational bridge rules that replace the helper body. `#differentiate` is a definitional summary on the destination side, connected to execution by C1; it is not an opaque result-bearing primitive.

I do not label any individual equation as unsound on the intended integer-list domain. The concrete length-998 witness instead demonstrates the narrower, explicitly recorded mismatch between the idealized unbounded-call language and CPython's resource exception.

## 6. Fresh non-vacuity test

The reviewer-created [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) changes the empty-input destination from the true `ListV([])` to the false `ListV([IntV(1)])`. Its precondition is satisfied by the concrete input `[]`.

The mutation parses/builds successfully: `kprove ... --dry-run` exits 0 ([vacuity_dry_run.log](/audit-output/evidence/vacuity_dry_run.log)). The actual proof exits 1 with `WarnStuckClaimState`; the residual is the actual normal final configuration `ListV(.Values) ~> .K`, which cannot unify with the false destination. See [vacuity_proof.log](/audit-output/evidence/vacuity_proof.log).

This is the expected unmet result obligation, not a parser error, missing import, timeout, unrelated crash, or unreachable mutation. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the freshly compiled K definition and its imported K libraries:

- the exact embedded `solution.mpy` AST maps empty input to `[]`;
- on nonempty finite K lists it discards the constant coefficient and invokes the exact submitted helper body at degree one;
- the exact helper body on finite `CS` realizes the structural `#differentiate(N,CS)` recurrence while preserving any continuation;
- on `IntV` coefficients, this recurrence is exactly `[N*c0,(N+1)*c1,...]`;
- all three reachability claims close with `#Top`;
- the result is discriminating, as the false empty result does not prove.

### Trust and limitation ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, reachability/circularity implementation | All execution and proof closure | Ordinary low-level trusted computing base; acceptable and version-recorded. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, and K list machinery | Arithmetic, equality, environments, finite sequences | Standard K primitives; acceptable. Unbounded `Int` matches CPython integers absent resource exhaustion. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor bridge | Byte identity and fresh regeneration are checked; semantic correctness of the trusted translator is assumed by the task boundary. |
| `solutionProgram` macro | File-to-proof program identity | Exact expanded-KORE identity and a rejected one-token program mutation provide strong reproducible evidence; acceptable. |
| Generated semantics | Meaning of the parsed AST | Statically audited and concretely exercised for every used construct on normal/boundary integer inputs. It is intentionally small but omits CPython floats, bool multiplication, exceptions, and stack/resource limits. The omission is concerning because the prompt does not state those restrictions. |
| `#differentiate` | Final result | Not opaque and not assumed: two disjoint structural equations fix it, and the helper claim connects actual body execution to it. |
| Recursion/termination bridge | Long finite inputs | K uses an unbounded abstract stack; CPython raises at documented long inputs. Acceptable only as a partial-correctness/normal-return limitation, not as evidence of total correctness or universal equivalence. |
| Mathematical intent bridge | “Derivative” meaning | Informal but direct: coefficient `c_i` becomes `i*c_i`; documented examples and finite tests support it. No separate K theorem names polynomial evaluation. |
| Differential testing | Python implementation versus canonical | Finite evidence only. It supports 799 cases and explicitly refutes universal behavioral equivalence with two recursion exceptions. It is not substituted for the K proof. |

Gate A (sound proof under the fixed submitted theory) passes: the body executes, the exact AST is pinned, no oracle or false proof extension was found, and the mutation is rejected. Gate B is limited by the broader prompt domain and CPython exception/type behavior. Gate C records reproducible evidence honestly, including the two mismatches, so it cannot support a universal implementation-equivalence claim.

If the requested property were total correctness, exception freedom, or exact CPython behavior for all finite numeric lists, this candidate would not establish it. For the requested partial-correctness reading—correct value whenever the modeled/normal execution returns—the reconstructed proof is legitimate but carries material concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
