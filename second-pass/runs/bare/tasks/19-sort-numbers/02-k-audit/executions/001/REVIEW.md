# Independent adversarial review: 19-sort-numbers

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under its generated semantics. The
proof was rebuilt from source, all five positive claims closed independently,
the exact submitted AST was pinned to the proof abbreviation, and a fresh false
postcondition was rejected for the expected semantic reason.

The decision is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two scoped
limitations:

1. `trimTrailingSpace` is intentionally narrower than Python's general
   `str.strip` but its K rule is syntactically broader than that justification.
   The submitted program only reaches the sound subset (`""`, or an ASCII
   numeral rendering with exactly one final space), so there is no false-result
   witness on the intended program/input domain. An off-path witness is recorded.
2. K proves that execution returns the explicit counting summary `sortSpec`.
   The bridge from that summary to the human phrase "numbers sorted from
   smallest to largest" is a straightforward mathematical argument supported by
   broad differential evidence, but it is not a separate K theorem about token
   lists and numeric ordering.

Everything below treats candidate logs, traces, compiled definitions, and prose
as untrusted claims. Only fresh reviewer runs and source inspection are used for
the decision.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, as required. There is therefore no supplied or inferred hidden
semantics baseline. This is not an infrastructure breach.

The live tools used were `kompile`, `krun`, and `kprove` from K
v7.1.293. Candidate-provided `semantic-kompiled/` and
`verification-kompiled/` were never copied into scratch and never used.

### Required artifacts and types

The following candidate source artifacts were present as regular files:

- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `solution-program.k`, `verification.k`, `spec.k`
- executable `prove.sh`
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the structured JSONL generation trace

No required source artifact was missing, mistyped, or symlinked. No candidate
entry anywhere in the inspected tree was a symlink. The additional
`semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, logs, and trace
are extra generated/evidentiary artifacts, not source-integrity failures; they
were ignored for reconstruction.

`PROOF.md` and `spec-vacuity.k` were absent, but neither was a required
generation deliverable. A reviewer-authored vacuity spec was created in stage
6.

The candidate prompt and translator are byte-identical to the trusted mounts:

- prompt SHA-256:
  `61b0d963a0d3797bc5ef83253bf35a531d7e31eedbd18181ff117b0e07e5c940`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The direct `cmp` checks exited 0. See
[candidate hashes](/audit-output/evidence/03_candidate_hashes.log),
[prompt comparison](/audit-output/evidence/04_prompt_cmp.log), and
[translator comparison](/audit-output/evidence/05_translator_cmp.log).

The candidate's small metadata/prose claims were read and recorded in
[02_candidate_claims_small.log](/audit-output/evidence/02_candidate_claims_small.log).
The generation log and structured trace were inspected only as untrusted
claims; see
[07_codex_log_structure.log](/audit-output/evidence/07_codex_log_structure.log)
and the corrected bounded trace review
[08b_trace_review.log](/audit-output/evidence/08b_trace_review.log).
The earlier `08_trace_structure.log` is a superseded reviewer command with a
mistyped secondary path and unavailable `jq`; it contributed no audit
conclusion.

The final source hashes under `/candidate` match the initially recorded hashes,
confirming that the candidate was not changed during review:
[45_candidate_unchanged_hashes.log](/audit-output/evidence/45_candidate_unchanged_hashes.log).

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

The trusted prompt requires:

- input: a space-delimited string whose numeral tokens are among `zero` through
  `nine`;
- output: the same numeral tokens sorted by numeric value from zero through
  nine;
- documented example: `"three one five"` becomes `"one three five"`.

The trusted canonical implementation splits on the literal space, discards
empty fields, ranks the ten words by a dictionary, sorts, and rejoins with one
space. Thus the canonical implementation also admits the empty string and
leading, trailing, or repeated literal spaces around otherwise valid tokens.
Invalid non-numeral tokens are outside the stated domain and may raise in the
canonical implementation.

The candidate uses a different counting algorithm. It concatenates, in numeric
order, `"word " * numbers.count(word)` for each of the ten numeral words and
then strips the constructed result. On the intended domain this is equivalent:
spaces separate tokens and no one of the ten numeral words is a substring of
another, so each substring count is exactly the token multiplicity.

### Trusted translation

The reviewer regenerated the translation with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/generated/solution.mpy
```

The submitted and regenerated files are byte-identical, both with SHA-256
`936f59152d7ef3e68b894293b4ab1f129faac965d0530a2b20d3f31290029495`.
See [regeneration](/audit-output/evidence/09_regenerate_mpy.log),
[byte comparison](/audit-output/evidence/10_regenerated_cmp.log), and
[hashes](/audit-output/evidence/11_regenerated_hashes.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted `/reference/canonical.py` and the clean scratch copy of the candidate
entry point independently. It exercised:

- the prompt example, empty input, sorted and reverse order, and multiplicity;
- all ten singleton and all ten double-token cases, covering every candidate
  count at zero, one, and greater than one;
- all `10^n` canonical token sequences for lengths 0 through 5: 111,111 cases;
- 300 leading/trailing/repeated-space boundary cases;
- 3,000 deterministic representative sequences of lengths 6, 10, and 25
  using seed 19019.

The complete run covered 114,439 inputs with 0 mismatches and exit status 0:
[12_differential.log](/audit-output/evidence/12_differential.log). The script
itself preserves the exact fixed inputs and generator scope; the log preserves
the fixed-case results and aggregate counts. This is finite evidence, not a
universal proof.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/candidate-src`. Candidate compiled directories and caches were
not copied. Fresh output definitions were created at
`/tmp/audit-work/concrete-kompiled`,
`/tmp/audit-work/verification-kompiled`, and, for the reviewer AST-pinning
claim, `/tmp/audit-work/audit-verification-kompiled`.

### Fresh builds

The concrete semantics build was:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
```

It exited 0:
[13_build_concrete.log](/audit-output/evidence/13_build_concrete.log).

The candidate proof definition build was:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-kompiled
```

It exited 0:
[14_build_proof.log](/audit-output/evidence/14_build_proof.log).

### Concrete generated-semantics executions

`krun` executed the actual submitted `solution.mpy`, not `solutionProgram`.
Fresh concrete results were:

- `"three one five"` -> `VStr("one three five")`
- `""` -> `VStr("")`
- `"two two one zero two"` -> `VStr("zero one two two two")`
- reverse all ten -> `VStr("zero one two three four five six seven eight nine")`
- `"nine   zero  five"` -> `VStr("zero five nine")`

See logs
[15](/audit-output/evidence/15_krun_example.log),
[16b](/audit-output/evidence/16b_krun_empty_retry.log),
[17](/audit-output/evidence/17_krun_duplicates.log),
[18](/audit-output/evidence/18_krun_reverse_all.log), and
[19](/audit-output/evidence/19_krun_spacing.log). These agree with both Python
implementations in stage 2.

One parallel empty-input invocation transiently failed while detecting Java
([16_krun_empty.log](/audit-output/evidence/16_krun_empty.log), exit 2).
The same command, definition, and input immediately succeeded sequentially in
`16b`; all other concurrent invocations succeeded. The resolved transient is
not treated as candidate evidence.

### Positive claims

The untouched aggregate `spec.k` invocation:

```text
kprove spec.k --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited 0:
[20_kprove_all_original.log](/audit-output/evidence/20_kprove_all_original.log).

Because the five candidate claims are unlabeled, the reviewer also copied each
claim verbatim into a distinct one-claim module and ran it independently.
Every invocation printed `#Top` and exited 0:

- universal claim:
  [spec-entry-1.k](/audit-output/evidence/spec-entry-1.k),
  [run](/audit-output/evidence/21_kprove_entry_1.log)
- prompt example:
  [spec-entry-2.k](/audit-output/evidence/spec-entry-2.k),
  [run](/audit-output/evidence/22_kprove_entry_2.log)
- duplicate case:
  [spec-entry-3.k](/audit-output/evidence/spec-entry-3.k),
  [run](/audit-output/evidence/23_kprove_entry_3.log)
- all-ten case:
  [spec-entry-4.k](/audit-output/evidence/spec-entry-4.k),
  [run](/audit-output/evidence/24_kprove_entry_4.log)
- empty case:
  [spec-entry-5.k](/audit-output/evidence/spec-entry-5.k),
  [run](/audit-output/evidence/25_kprove_entry_5.log)

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

None of the five claims has a `requires` clause.

1. For every K `String` `S`, start with `solutionProgram` followed by
   `invoke(S)`. Termination must leave the exact result
   `VStr(sortSpec(S))`.
2. For the fixed prompt input `"three one five"`, the exact final result must be
   `VStr("one three five")`.
3. For `"two two one zero two"`, the exact final result must be
   `VStr("zero one two two two")`.
4. For the reverse ordering of all ten words, the exact final result must be
   the zero-through-nine ordering.
5. For the empty string, the exact final result must be `VStr("")`.

The claims rewrite the complete `<k>` cell to a concrete `VStr` term. The
universal result is a deterministic function of the same input variable `S`;
there is no right-only existential, free result variable, implication-only
postcondition, or tautological `ensures`.

Every precondition is satisfiable. Examples include the initial configurations
with `S = ""`, `S = "three one five"`, and each fixed ground input. These are
instances of the semantics configuration
`$PGM:Program ~> invoke($ARG:String)`. The fixed substitutions and outputs agree
with both Python implementations in
[12_differential.log](/audit-output/evidence/12_differential.log).

### Exact submitted-program pinning

The candidate claims use `solutionProgram`, a three-function K abbreviation
(`block`, `solutionBody`, and `solutionProgram`) rather than including the
81-line translated AST inline. The reviewer independently pinned it as follows:

1. Embedded the submitted `solution.mpy` constructor tree in
   [audit-actual-program.k](/audit-output/evidence/audit-actual-program.k).
   The only surface normalization is spelling the zero-length `Exprs` list as
   `.Exprs`, which K requires inside a rule RHS but permits to be omitted in the
   top-level `.mpy` input.
2. Compared the submitted and embedded terms with a string-literal-aware
   normalizer. Both normalized hashes are
   `923f0838603e3e50d982cd43e69ee1d411cf5627b1c7abf29b75a9a863de6780`;
   identity is `True`:
   [compare_embedded_ast.py](/audit-output/evidence/compare_embedded_ast.py),
   [26d log](/audit-output/evidence/26d_actual_ast_identity_unit_normalized.log).
3. Freshly compiled the reviewer extension
   ([27d](/audit-output/evidence/27d_build_actual_ast_proof_retry.log)).
4. Proved the same universal result starting from the embedded exact AST:
   [spec-actual.k](/audit-output/evidence/spec-actual.k),
   [28_kprove_actual_ast.log](/audit-output/evidence/28_kprove_actual_ast.log),
   `#Top`, exit 0.
5. Proved that the candidate `solutionProgram` and the reviewer exact-AST
   symbol simplify to the same program term:
   [spec-alias-identity.k](/audit-output/evidence/spec-alias-identity.k),
   [29_kprove_alias_ast_identity.log](/audit-output/evidence/29_kprove_alias_ast_identity.log),
   `#Top`, exit 0. The prover reports the equality as trivial after function
   simplification, which is the expected structural-identity result.

Earlier reviewer attempts to put the top-level omitted-list syntax directly
inside a claim failed to parse (logs `27`, `27b`, and `27c`). They were
superseded by the explicit `.Exprs` unit representation above and are not
candidate build/proof failures.

### Body sensitivity

Separately from the stage-6 postcondition mutation, the reviewer changed the
zero block in a scratch copy from `"zero "` to `"bogus "`. The mutated
definition built successfully:
[body mutation source](/audit-output/evidence/body-mutation-solution-program.k),
[build](/audit-output/evidence/39_build_body_mutation.log). The original
universal target then failed with `WarnStuckClaimState`; its residual explicitly
compares the `"bogus "` and `"zero "` summaries:
[40_body_mutation_proof_expected_fail.log](/audit-output/evidence/40_body_mutation_proof_expected_fail.log).
Thus the connection is sensitive to a result-affecting body change.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

The raw declaration/rule inventory is preserved in
[30_rule_inventory_raw.log](/audit-output/evidence/30_rule_inventory_raw.log).
Compiled local-rule source locations were also checked in
[32_compiled_local_rules.log](/audit-output/evidence/32_compiled_local_rules.log).

### Complete local declaration inventory

`semantic.k`, module `MPY-SYNTAX`, declares:

- list sorts `Ids`, `Exprs`, and `Stmts`;
- `Params(Ids)`;
- expression constructors `Name`, `Str`, `Int`, `Attribute`, `Call`, and
  `BinOp`;
- statement constructors `Return` and `FuncDef`;
- program constructor `Module`;
- result constructors `VStr` and `VInt`;
- control item `invoke(String)`.

`semantic.k`, module `MPY`, declares the sole configuration:

```text
<k> $PGM:Program ~> invoke($ARG:String) </k>
```

It declares eight local functions: `evalProgram`, `eval`, `addVals`,
`multiplyVals`, `countVal`, `stripVal`, `repeatString`, and
`trimTrailingSpace`.

`solution-program.k` declares three function-valued abbreviations:
`block`, `solutionBody`, and `solutionProgram`.

`verification.k` declares:

- `sortSpec(String)` as a function;
- `isNumeral(String)` as `[function, total]`;
- `validNumerals(String)` as a function.

There are no local `[functional]` declarations, opaque symbols, priority
rules, fresh values, axioms, or uninterpreted result oracles. The only local
`[total]` declaration is `isNumeral`. The only `[owise]` rule is its fallback.
The simplification rules are the two guarded `repeatString` rules and the
nonempty `trimTrailingSpace` rule; all three also carry `[concrete(...)]`.

### Construct-to-rule coverage

Every construct in the submitted `solution.mpy` is covered:

| Submitted construct | Declaration and semantics |
|---|---|
| `Module(FuncDef(...))` | `Program`, `Stmt`, `Params`, and `Stmts`; exact-shape `evalProgram` rule |
| `Return(E)` | consumed by the exact-shape `evalProgram` rule, which evaluates `E` |
| `Name("numbers")` | `eval(Name("numbers"), S) => VStr(S)` |
| numeral string literals | `eval(Str(X), _) => VStr(X)` |
| `BinOp("+", E1, E2)` | recursive `eval`, then `addVals` and K `+String` |
| `BinOp("*", E1, E2)` | recursive `eval`, then `multiplyVals`/`repeatString` |
| `numbers.count(word)` | exact `Call(Attribute(E,"count"), Str(Needle))` rule, then `countVal` |
| final `.strip()` | exact zero-argument `Call(Attribute(E,"strip"), .Exprs)` rule, then `stripVal` |
| one-element and empty expression lists | `Exprs` list syntax; visible in the regenerated AST |
| invocation and final result | the sole `<k>` operational rule and `VStr` |

`Int`/`VInt` is reached as the result of a count. Source-level `Int(I)` is
declared and has a faithful evaluation rule but is not present in this program.
Unmodeled names, operators, methods, functions, statements, and effects stop
because no rule matches. Missing semantics for those unused forms is permitted
in generated-semantics mode.

### Exhaustive rule decisions

The 17 `semantic.k` rules are:

1. `evalProgram` for exactly one `sort_numbers(numbers)` function containing
   one `Return(E)`: faithful to the submitted module and binding.
2. `eval(Name("numbers"), S)`: faithful parameter lookup for this exact
   environment.
3. `eval(Str(S), _)`: faithful string literal evaluation.
4. `eval(Int(I), _)`: faithful and unused at source level.
5. `eval(BinOp("+",...))`: faithful on the actual string operands.
6. `eval(BinOp("*",...))`: faithful on the actual string/integer operands.
7. count-method call recognition: faithful to each actual built-in `str`
   receiver and one nonempty string argument.
8. zero-argument strip-method call recognition: reaches `stripVal`.
9. `addVals(VStr,VStr)`: faithful string concatenation.
10. `multiplyVals(VStr,VInt)`: delegates to the fully guarded repetition
    function.
11. `countVal`: delegates to K's non-overlapping occurrence count.
12. `stripVal`: delegates to the scoped trailing-space helper.
13. `repeatString(_,N) => ""` for `N <= 0`: agrees with Python string
    multiplication.
14. positive `repeatString`: one-copy recursion, with strict descent in `N`.
15. `trimTrailingSpace("") => ""`: exact on the reachable empty intermediate.
16. nonempty `trimTrailingSpace`: removes exactly one final code point; exact on
    every reachable nonempty intermediate, but deliberately not general
    `str.strip` semantics.
17. `<k> P ~> invoke(S) => evalProgram(P,S) ...</k>`: a big-step operational
    entry rule. It preserves any continuation after `invoke`; it does not pop a
    stack, discard a suffix, fabricate a return, or change another cell.

The guards for rules 13/14 are disjoint and cover all integers; the recursive
argument decreases. Rules 15/16 are disjoint. The `[concrete]` attributes
restrict when the simplifier evaluates ground helpers but do not add an
equation or leave their mathematical cases overlapping.

The three `solution-program.k` rules are purely definitional:

1. `block(Word,Printed)` constructs exactly the string-multiplication/count AST
   block.
2. `solutionBody` constructs the nine left-nested additions of ten blocks and
   the final zero-argument strip call.
3. `solutionProgram` constructs the exact module/function/return wrapper.

They do replace the abbreviation before program evaluation, but the exact AST
identity proof in stage 4 supplies their complete justification. They read or
write no state and introduce no result-bearing opaque value.

The 16 `verification.k` rules are:

1. the single unconditional `sortSpec` equation, which names the exact
   zero-through-nine counting rendering without replacing program execution;
2. ten exact `isNumeral` true cases plus one `[owise]` false case. The cases are
   complete and non-overlapping under `owise`, validating `[total]`;
3. four `validNumerals` cases: empty, nonempty/no-space, a proper first
   delimiter with recursion on a strictly shorter suffix, and a trailing-space
   false case. Their `findString` guards are disjoint for the relevant string
   positions and recursion descends.

`validNumerals` is not referenced by `sortSpec`, any semantic rule, or any of
the five claims. Its comment describes a stricter single-space grammar than the
trusted canonical implementation, which tolerates empty split fields. That
comment/domain mismatch has no proof dependency and cannot make a target claim
close.

The five `spec.k` declarations are reachability claims, inventoried and
independently executed in stage 3. There are no auxiliary loop claims,
invariants, or circularities.

### State, evaluation, calls, returns, and exceptions

The only state is `<k>`. The actual function is pure: no heap, mutable
bindings, I/O, allocation, or user-defined calls are required. The semantics
passes the input `String` directly as the sole parameter binding. Both
subexpressions of each binary operation are pure and exception-free on the
intended typed input, so the absence of an explicit small-step left-to-right
evaluation context does not change an observable result.

Method binding is pinned by the exact `Attribute` names and by `numbers` and all
intermediates being K strings. No rebinding or dynamic object dispatch is
possible in the submitted program. Python exceptions for wrong receiver types,
invalid operators, or unsupported programs are outside this intended,
well-typed path and are not silently converted to a value; such terms become
stuck.

### Built-ins and scoped semantic limitation

The local theory depends on K `DOMAINS` primitives for string concatenation,
length, substring, search, non-overlapping occurrence count, integer arithmetic
and comparison, and Boolean operations. The installed source declares
`countAllOccurrences` with hook `STRING.countAllOccurrences` and also gives the
expected two recursive rules: return zero when `findString` fails, otherwise
remove the matched prefix plus the nonempty needle and add one. The inspected
declarations/rules are recorded in
[31_builtin_string_hooks.log](/audit-output/evidence/31_builtin_string_hooks.log).
All ten program needles are fixed, nonempty ASCII words.

`trimTrailingSpace` is not a sound general semantics for arbitrary Python
`str.strip`. The reviewer exhibited an off-path program for `" x ".strip()`:
K returns `" x"` while Python returns `"x"`:
[strip-offpath.mpy](/audit-output/evidence/strip-offpath.mpy),
[K result](/audit-output/evidence/34_strip_offpath_k.log),
[Python result](/audit-output/evidence/35_strip_offpath_python.log).

This is not classified as an intended-domain unsoundness witness. In the
submitted AST, the argument to strip is a concatenation of zero or more blocks
`"word " * N`, with `N >= 0`. By induction over the ten blocks, that
intermediate is either empty or is made only of numeral words separated by one
space and ending in exactly one space. Removing its last code point is therefore
exactly Python `strip` on every submitted-program state, including every
intended input. No rule enables a false target conclusion for such a state.
The narrower finding is that the rule's syntactic match is broader than its
documented/path justification; this is a concern for reuse of the generated
semantics.

No candidate rule encodes an unconstrained answer, replaces the submitted body
with an oracle, bypasses the real execution, or fabricates a value for a used
unmodeled construct. `sortSpec` is a fully defined postcondition summary. Its
similarity to the implementation makes the K execution theorem simple, but the
AST still executes compositionally and both body and postcondition mutations
are discriminating.

**Stage 5 result: PASS for the submitted program and intended domain, with the
documented reuse/adequacy concerns.**

## 6. Fresh non-vacuity test

The reviewer created
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), which keeps the
satisfiable prompt-example start state but changes the exact result from the
true `"one three five"` to the false `"one three four"`.

The mutation first built successfully with:

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit status was 0 and the backend command was produced:
[42_vacuity_dry_run.log](/audit-output/evidence/42_vacuity_dry_run.log).

The real mutation run used the same command without `--dry-run`. It exited 1
with `WarnStuckClaimState`. The reachable residual is exactly
`VStr("one three five")`, which fails to unify with the false destination:
[43_vacuity_proof_expected_fail.log](/audit-output/evidence/43_vacuity_proof_expected_fail.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the freshly compiled candidate K theory:

- for every finite K `String` `S`, evaluating the exact submitted translated
  AST returns the exact K string
  `trimTrailingSpace(repeat("zero ",count(S,"zero")) + ... +
  repeat("nine ",count(S,"nine")))`;
- the four ground results in `spec.k` are exact instances of that theorem;
- the result is constrained and body-sensitive;
- for the intended valid numeral-token inputs, the returned rendering has all
  zero tokens first, then ones, through nines, preserving each multiplicity.

This is partial correctness in the Kit sense. It does not claim behavior for
arbitrary Python objects, invalid non-numeral tokens under the canonical
implementation, resource exhaustion, or programs outside the modeled AST
subset.

### Trust ledger

| Boundary | Dependents | Status and evidence |
|---|---|---|
| Trusted `py2mpy.py` translation algorithm | source-to-`solution.mpy` identity | Accepted trusted input; candidate copy matches, regeneration is byte-identical |
| K parser, compiler, Haskell backend, and reachability prover | all machine-checked results | Standard tool trust boundary; version and exact commands are recorded |
| K `DOMAINS` string/int/bool primitives and hooks | concatenation, count, repeat guards, trim indices, validity helper | Accepted low-level primitive boundary; installed declarations and recursive count equations were inspected |
| Candidate-generated big-step Python subset semantics | connection from AST to K result | Audited rule by rule and tested concretely; adequate for every construct in this pure submitted program |
| `solutionProgram` abbreviation | all original claims | Exact AST identity and exact-AST universal execution were machine-checked; body mutation is rejected |
| `repeatString` and `trimTrailingSpace` | multiplication, strip, and `sortSpec` | `repeatString` is exhaustively guarded and descending. `trimTrailingSpace` is accepted only on the proved-by-inspection reachable shape; broader reuse is concerning |
| K `countAllOccurrences` versus CPython `str.count` | token multiplicities | Recursive non-overlap definitions agree for fixed nonempty needles; the five concrete K/Python comparisons support this bridge. The 114,439-case differential run tests candidate Python versus canonical Python separately and is not evidence for the K hook |
| Counting summary versus natural-language sorting | intent adequacy | Informal mathematical bridge: fixed zero-to-nine output order plus exact token multiplicities; 114,439 canonical differential cases give finite support, not a universal K theorem |
| Trusted canonical Python implementation | differential oracle | Trusted problem input; used only as finite adequacy evidence, never as a substitute for `kprove` |

There are no opaque candidate symbols, fresh result values, empirical
operational bridges, assumed loop invariants, or proof-local axioms.
`validNumerals` is unused and has no dependent claim.

### Gate accounting

- Real-program soundness: **PASS** on the complete intended input domain. The
  actual AST is pinned, all used computation is defined, the result is exact,
  body sensitivity holds, and the false result is rejected.
- Intent adequacy: **PASS with concerns**. The counting summary has the required
  meaning on valid numeral-token strings, but that final meaning is justified
  mathematically and empirically rather than by a separate K token-order theorem.
- Trust/evidence auditability: **PASS**. Exact commands, statuses, sources, and
  bounded outputs are preserved under `/audit-output/evidence/`.

The proof is therefore legitimate. The limitations are non-material for this
submitted program but significant enough to preclude an unqualified `PASS`,
especially if `semantic.k` were reused as general Python string semantics.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
