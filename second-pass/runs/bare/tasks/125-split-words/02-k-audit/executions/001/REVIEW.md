# Independent adversarial audit: 125-split-words

## Outcome

The reconstructed K proof is legitimate for the exact submitted program under
the submitted generated semantics. It is result-constraining, executes the
translated body through the semantics, survives an exact AST-pinning check, and
rejects a reachable false result mutation.

The result is `CONCERNS / LEGIT`, not `PASS`, because the submitted Python
program and its proved postcondition materially diverge from the trusted
canonical implementation on the unrestricted string domain. In particular,
they disagree on non-space whitespace, leading/trailing/repeated commas, and
non-ASCII lowercase letters. The natural-language prompt partly supports the
candidate's choices, so this is an intent/canonical-bridge limitation rather
than evidence that the K reachability proof itself is unsound.

No infrastructure breach was found. The rendered mode is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` is absent as
required.

## 1. Input and provenance integrity

### Semantics boundary

- `/reference/reference-semantics` does not exist. This is consistent with
  `GENERATED_SEMANTICS`; no hidden or inferred reference semantics was used.
- `/reference` contains exactly the three trusted files relevant to this mode:
  `canonical.py`, `prompt.py`, and `py2mpy.py`.
- The candidate's compiled `verification-kompiled/` and
  `__pycache__/solution.cpython-310.pyc` are untrusted extra build/cache
  artifacts. They were inventoried but were neither copied nor used.
- No symlink was found anywhere under `/candidate`. Every required candidate
  path inspected was a regular file.

Evidence: [mount and complete candidate inventory](evidence/stage1_mount_inventory.log).

### Trusted-file comparisons and required source artifacts

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` with SHA-256
`c9ac5a400f5388b93fcc2acc0fa2adf0237e9f1802cebec7f375644658bd9aa0`.
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` with SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The following candidate artifacts all exist as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. No required source artifact is
missing, mistyped, changed relative to its applicable trusted counterpart, or
symlinked.

Evidence: [byte comparisons, hashes, types, and sizes](evidence/stage1_provenance_comparison.log).

### Untrusted generation records

The records claim a successful generation run and a prior `#Top`; those claims
were not used as proof evidence. The complete 15,423-line `codex-output.log`
and the complete 208-record JSONL trace were parsed, and the smaller metadata
files were read. `run-input.json` identifies problem `125-split-words`,
condition `bare`, and no supplied semantics. `metrics.json` claims exit 0
without timeout. These are provenance claims only.

Evidence:

- [bounded metadata and trace excerpt](evidence/stage1_untrusted_metadata.log)
- [full-record parse counts and bounded signal summary](evidence/stage1_untrusted_record_full_parse.log)
- [record sizes and hashes](evidence/stage1_generation_record_summary.log)
- [source-artifact snapshot](evidence/stage1_source_artifacts.log)

All executable work used the explicit source-only copy recorded in
[scratch_source_copy.log](evidence/scratch_source_copy.log). No candidate
definition, cache, binary, or generated backend artifact entered the scratch
copy.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract restatement

The prompt says, for a string `txt`:

1. if whitespace exists, return words split on whitespace;
2. otherwise, if commas exist, return words split on commas;
3. otherwise, return the count of lowercase letters having odd zero-based
   alphabet positions, where `a` is 0 through `z` at 25.

For ASCII letters, the third branch counts
`b,d,f,h,j,l,n,p,r,t,v,x,z`.

The trusted canonical implementation is more specific, and differs from a
literal reading of parts of the prose:

1. it selects the first branch only when the literal ASCII space `" "` occurs,
   then calls `txt.split()`;
2. otherwise, when a comma occurs, it evaluates
   `txt.replace(",", " ").split()`, which discards empty fields and also splits
   any other Python whitespace present;
3. otherwise, it counts every character satisfying `islower()` whose Unicode
   code point is even.

The candidate preserves the required signature `split_words(txt)`. It computes
`words = txt.split()`, detects any Python whitespace by testing
`"".join(words) != txt`, uses `txt.split(",")` in the comma branch, and sums
the 13 fixed ASCII one-character counts in the final branch.

### Translator fidelity

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced a 2,124-byte file that is byte-identical to the
submitted `solution.mpy`, with common SHA-256
`df19e38bff0c6bbb1f301ab129ef175ef193e54f38b70a28dbf152a2b6d02ec0`.

Evidence: [translation command and byte comparison](evidence/stage2_translation_identity.log);
preserved [regenerated constructor program](evidence/solution.regenerated.mpy).

### Independent Python differential

The reviewer-authored test imports the trusted canonical and candidate entry
points independently. Its scope is:

- 28 fixed cases covering all prompt examples, empty input, each branch,
  branch precedence, leading/trailing/repeated separators, ASCII and Unicode
  whitespace, and ASCII/Unicode count boundaries; and
- every string of length 0 through 4 over
  `["a","b","c",","," ","\t","A","1","ä"]`.

After deduplication, 7,393 inputs were checked. There were 3,438 mismatches:
1,413 in the canonical comma branch and 2,025 in its count branch. Important
ground witnesses are:

| Input | Trusted canonical | Candidate |
|---|---|---|
| `"\t"` | `0` | `[]` |
| `"left\u2003right"` | `6` | `["left", "right"]` |
| `","` | `[]` | `["", ""]` |
| `"a,,b,"` | `["a", "b"]` | `["a", "", "b", ""]` |
| `"ä"` | `1` | `0` |

All three documented examples agree. The mismatch count is not used as a
statistical proof; the listed witnesses directly establish real divergence on
the unrestricted Python `str` domain.

Evidence:

- [differential script](evidence/differential_test.py)
- [fixed input corpus](evidence/differential_inputs.json)
- [command, complete scope, results, and mismatch witnesses](evidence/stage2_python_differential.log)

### Fidelity judgment

The candidate is a faithful implementation of a plausible literal reading of
"whitespace", "split on commas", and the explicitly bounded `a` through `z`
alphabet. It is not extensionally equal to the trusted canonical over all
strings, and the prompt contains no ASCII-only or normalized-separator
precondition that removes the witnesses above. This is a material adequacy
limitation and is the reason a clean proof cannot receive `PASS`.

## 3. Clean proof reconstruction

### Toolchain and fresh builds

The independent toolchain was K `v7.1.293` and Python `3.10.12`; see
[toolchain_versions.log](evidence/toolchain_versions.log).

Two separate definitions were built from copied source:

| Purpose | Command result | Evidence |
|---|---|---|
| Concrete LLVM definition | `kompile verification.k --backend llvm --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition concrete-kompiled`; exit 0 | [build log](evidence/stage3_build_concrete_llvm.log) |
| Proof Haskell definition | `kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled`; exit 0 | [build log](evidence/stage3_build_proof_haskell.log) |

Both output directories were newly produced below `/tmp/audit-work/fresh`.

### Fresh generated-semantics execution

The actual regenerated `solution.mpy` was run with the LLVM definition on 22
normal and boundary strings. The inputs cover all three branches, all selected
and unselected ASCII count letters as groups, empty input, separator placement,
ASCII and Unicode whitespace, and representative non-ASCII lowercase letters.
Each K value was structurally compared with an independently imported candidate
Python result. All 22 `krun` calls exited 0, with zero mismatches.

Evidence:

- [comparison script](evidence/concrete_semantics_compare.py)
- [input corpus](evidence/k_concrete_inputs.json)
- [all commands, statuses, and results](evidence/stage3_concrete_semantics_differential.log)
- [single direct smoke run](evidence/stage3_krun_smoke.log)

### Fresh positive proofs

The unchanged candidate `spec.k` was first proved as one target command. It
exited 0 and printed `#Top`, covering all eight claims:
[stage3_kprove_all_candidate_claims.log](evidence/stage3_kprove_all_candidate_claims.log).

The claims were then copied without changing their formulas into distinct
reviewer modules and run independently:

| Claim | Exit / result | Evidence |
|---|---|---|
| Universal symbolic claim | 0 / `#Top` | [log](evidence/stage3_kprove_universal.log) |
| `"Hello world!"` | 0 / `#Top` | [log](evidence/stage3_kprove_example_space.log) |
| `"Hello,world!"` | 0 / `#Top` | [log](evidence/stage3_kprove_example_comma.log) |
| `"abcdef"` | 0 / `#Top` | [log](evidence/stage3_kprove_example_count.log) |
| `""` | 0 / `#Top` | [log](evidence/stage3_kprove_empty.log) |
| `"a,b c"` | 0 / `#Top` | [log](evidence/stage3_kprove_whitespace_precedence.log) |
| `"left\u2003right"` | 0 / `#Top` | [log](evidence/stage3_kprove_unicode_whitespace.log) |
| `"a,,b,"` | 0 / `#Top` | [sequential retry log](evidence/stage3_kprove_empty_comma_fields_retry.log) |

The preserved per-claim source is
[spec-individual.k](evidence/spec-individual.k). One parallel attempt at the
last claim encountered a transient Java-detection error
([log](evidence/stage3_kprove_empty_comma_fields.log)); the exact same claim
then succeeded sequentially. This was tooling noise, not treated as candidate
evidence in either direction.

Every successful run emitted `WarnTrivialClaim`: the K frontend normalized the
`[function]` equations on the source and destination until the claims were
identical before backend rewriting. That warning does not by itself make the
claims vacuous. It makes the truth of every normalizing equation, exact program
pinning, and the false-result mutation decisive. Those checks are addressed in
Stages 4 through 6.

## 4. Adequacy and real-program pinning

### Preconditions and postconditions

There are no `requires` clauses and no auxiliary or loop claims.

- The universal claim accepts every K `String` `S`. It requires the exact
  result:
  - `VList(pySplitWhitespace(S))` when
    `joinValues("", pySplitWhitespace(S)) =/=String S`;
  - otherwise `VList(pySplitOn(S, ","))` when a comma is found;
  - otherwise `VInt(oddLetterCount(S))`.
- The seven concrete claims fix their inputs and exact `VList` or `VInt`
  results. No right-hand-side output is free or existential.
- The `...` in the `<k>` cell frames and preserves an arbitrary continuation;
  it does not weaken the exact value placed at the front of that continuation.

The sole configuration cell is `<k>`. Function-local state is an explicit
`Map` argument to `exec`, so there are no omitted heap, output, exception, or
allocation cells in this submitted subset.

### Satisfying states and substitution

Each initial `<k>` term itself supplies a satisfying state because no additional
precondition exists:

| Entry claim | Satisfying input | Claimed / K / candidate Python | Trusted canonical |
|---|---|---|---|
| Universal | `"abcdef"` | `3` | `3` |
| Example 1 | `"Hello world!"` | `["Hello","world!"]` | same |
| Example 2 | `"Hello,world!"` | `["Hello","world!"]` | same |
| Example 3 | `"abcdef"` | `3` | `3` |
| Empty | `""` | `0` | `0` |
| Precedence | `"a,b c"` | `["a,b","c"]` | same |
| Unicode whitespace | `"left\u2003right"` | `["left","right"]` | `6` |
| Empty comma fields | `"a,,b,"` | `["a","","b",""]` | `["a","b"]` |

The K/candidate comparisons are in
[stage3_concrete_semantics_differential.log](evidence/stage3_concrete_semantics_differential.log);
both Python implementations are compared in
[stage2_python_differential.log](evidence/stage2_python_differential.log).

### Exact program identity

The formal claims use `solutionAST`, so the duplicated constructor tree was
checked rather than trusted:

1. the submitted `.mpy` is byte-identical to trusted regeneration;
2. after accounting only for K source syntax's explicit `.Exprs` and `.Stmts`
   spellings of the three empty generated lists, all 414 constructor tokens in
   `solutionAST` are identical to the regenerated `.mpy`;
3. a configuration-form K pinning claim from `solutionAST` to that normalized
   constructor tree exits 0 with `#Top`.

Evidence:

- [mechanical 414-token comparison](evidence/stage4_ast_token_identity.log)
- [comparison script](evidence/ast_pinning_compare.py)
- [pinning claim](evidence/pinning-spec.k)
- [successful pinning proof](evidence/stage4_solution_ast_pinning_configuration.log)

The first two reviewer attempts used an invalid empty-list spelling and then a
backend-unsupported functional-claim shape; those parser/backend diagnostics
are preserved in
[stage4_solution_ast_pinning.log](evidence/stage4_solution_ast_pinning.log) and
[stage4_solution_ast_pinning_retry.log](evidence/stage4_solution_ast_pinning_retry.log).
They are not candidate proof failures.

### Body sensitivity

A separate scratch mutation changed only the final counted letter from `"z"`
to `"a"`. Trusted translation changed the `.mpy` hash; the program/pinning
comparison detected the exact changed token at normalized index 407. Python
results changed for `"a"`, `"z"`, and `"abcdef"`, and the unchanged fresh K
semantics executed the mutated `.mpy` to `1`, `0`, and `4`, respectively.
Thus execution and the identity check are sensitive to the body rather than to
the function name alone.

Evidence:

- [mutated source](evidence/body_mutated_solution.py) and
  [translated program](evidence/body_mutated_solution.mpy)
- [generation and differing hashes](evidence/stage4_body_mutation_generation_retry.log)
- [behavior and AST sensitivity](evidence/stage4_body_mutation_sensitivity.log)
- K executions for [`"a"`](evidence/stage4_mutated_krun_a.log),
  [`"z"`](evidence/stage4_mutated_krun_z.log), and
  [`"abcdef"`](evidence/stage4_mutated_krun_abcdef.log)

### Control-flow pinning

`runProgram` finds `split_words` in the actual module, `invoke` binds its one
parameter, and `exec` consumes its actual statement list. Assignment updates
the environment map; `execRest` propagates returns; both `If` terms distribute
the remaining statements only to normal outcomes. There is no helper call or
loop to summarize. The final value is derived from the body and is not supplied
by an unconstrained oracle.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

The machine-extracted declaration locations are preserved in
[stage5_declaration_inventory.log](evidence/stage5_declaration_inventory.log).

Local syntax is:

| File/module | Declarations |
|---|---|
| `semantic.k` / `MPY-SYNTAX` | `Module`; list sorts `Stmts`, `Strings`, `Exprs`, `CmpOps`; `Params`; statement constructors `FuncDef`, `Assign`, `If`, `Return`; expression constructors `Name`, `Str`, `Int`, `Attribute`, `Call`, `Compare`, `BinOp`; `CmpOp` |
| `semantic.k` / `MPY-SEMANTIC` | value constructors `VStr`, `VInt`, `VBool`, `VList`, `VAttr`, `iteValue`; evaluator symbols `eval`, `call`, `add`, `compare`, `asBool`; outcome constructors `normal`, `returned`, `iteOutcome`; `exec`, `execStmt`, `execRest`; `isWhitespace`; `pySplitWhitespace`, `splitWhitespaceAt`; `joinValues`, `joinValuesTail`; `pySplitOn` |
| `verification.k` / `MPY-VERIFICATION` | `closure`, `findFunction`; `invoke`, `outcomeValue`, `runProgram`; `solutionAST`; `oddLetterCount`; `containsWhitespace`; configuration `<k> runProgram($PGM,$INPUT) </k>` |

There are 22 local `[function]` declarations:
`iteValue`, `eval`, `call`, `add`, `compare`, `asBool`, `exec`, `execStmt`,
`execRest`, `isWhitespace`, `pySplitWhitespace`, `splitWhitespaceAt`,
`joinValues`, `joinValuesTail`, `pySplitOn`, `findFunction`, `invoke`,
`outcomeValue`, `runProgram`, `solutionAST`, `oddLetterCount`, and
`containsWhitespace`.

Exactly three are also `[total]`: `isWhitespace`, `oddLetterCount`, and
`containsWhitespace`. There are no local `[functional]` declarations, opaque
result symbols, priorities, `[simplification]` rules, `[concrete]` rules,
`[owise]` rules, or user claims imported as proof lemmas. All local rules below
are equations for the declared functions; there are no separate cell-rewriting
operational bridges.

### Used-constructor coverage

Every constructor in `solution.mpy` is covered:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | program lookup and one-argument invocation in V01–V06 |
| `Assign(Name(...), ...)` | expression evaluation plus map update in S24 |
| `If` | condition evaluation and branch outcomes in S26, S23, V05 |
| `Return` | returned outcome and propagation in S25, S22, V04 |
| `Name`, `Str`, `Attribute` | S01, S02, S04 |
| zero/one-argument `Call` | S05–S06 and method equations S09–S12 |
| one-operator `Compare` / `CmpOp` | S08, S14–S16 |
| `BinOp("+",...)` | S07, S13 |

`Int`, multiargument calls, comparison chains, other operators, other
assignment targets, exceptions, globals, and arbitrary Python features are
not used by the program. Their absence or partial handling is acceptable for
generated minimal semantics.

### Exhaustive semantic rule decisions

| ID / location | Rule | Decision |
|---|---|---|
| S01 / `semantic.k:50` | `eval(Name)` map lookup | Sound for the unique-key K map; `txt` and `words` are bound before use. |
| S02 / `:51` | string literal to `VStr` | Direct and sound. |
| S03 / `:52` | integer literal to `VInt` | Direct; declared but unused by this AST. |
| S04 / `:53` | attribute evaluation to `VAttr` | Sound delayed method selection for this pure string subset. |
| S05 / `:54` | zero-argument call | Preserves receiver evaluation and exact empty argument list. |
| S06 / `:55` | one-argument call | Preserves receiver and argument values; every submitted nonzero-arity call has exactly one argument. |
| S07 / `:56` | `BinOp("+")` | Delegates evaluated operands to S13; used only for integers. |
| S08 / `:57` | single comparison | Preserves the submitted one-operator shape; chains are intentionally unmodeled. |
| S09 / `:60` | `str.split()` | Maps the external string primitive to the defined `pySplitWhitespace`; no program-defined body is skipped. |
| S10 / `:61` | `str.split(SEP)` | Correct through S38–S39 for nonempty separators; the submitted separator is always `","`. Empty-separator exception behavior is outside the used subset. |
| S11 / `:63` | `str.join(VList)` | Correct through S34–S37 for lists of strings; the submitted `words` value has exactly that form. |
| S12 / `:65` | `str.count(NEEDLE)` | K's nonoverlapping `countAllOccurrences` matches Python for every used one-character needle. The equation is broader than needed; empty-needle behavior is not modeled faithfully but is unreachable from this program. |
| S13 / `:68` | integer addition | Direct K integer arithmetic. |
| S14 / `:69` | string `!=` | Direct K string inequality. |
| S15 / `:70` | string containment | `findString >= 0` is the ordinary substring predicate; used for comma containment. |
| S16 / `:72` | `VBool` truth extraction | Direct. |
| S17 / `:73` | true conditional value | Selects the then value. |
| S18 / `:74` | false conditional value | Selects the else value; S17 and S18 are disjoint and exhaustive. |
| S19 / `:84` | empty statement list | Returns the unchanged environment. |
| S20 / `:85` | statement-list head/tail | Executes the head then passes its outcome and exact tail to S21–S23; structurally decreases. |
| S21 / `:87` | normal outcome continuation | Executes the remaining statements in the updated environment. |
| S22 / `:88` | returned outcome continuation | Discards later statements exactly as Python return does. |
| S23 / `:89` | conditional outcome continuation | Applies the remainder only within each branch outcome; return branches are still stopped by S22. |
| S24 / `:92` | assignment to `Name` | Evaluates in the old environment, then updates the named local. This matches the only assignment form used. |
| S25 / `:93` | return expression | Evaluates the expression and creates a returned value. |
| S26 / `:94` | `If` | Computes both pure outcome terms and defers selection. This would not model exceptions or side effects in an unchosen branch generally, but every submitted branch is total and state-pure except for the explicitly threaded local map, so it is extensionally faithful here. |
| S27 / `:101` | whitespace table membership | On the only reachable call domain—a one-code-point substring—it exactly matches all 29 Python `isspace()` code points. The declaration is over-broad: for example `isWhitespace("")` evaluates true because the empty needle is found, although Python `"".isspace()` is false. No submitted-program input can cause that call because S31–S33 invoke it only under `I < lengthString(S)` on `[I,I+1)`. This is an off-path width gap, not a task-domain false-conclusion witness. |
| S28 / `:108` | initialize whitespace split | Starts at index 0 with empty word and output. |
| S29 / `:109` | terminate with empty word | Correctly omits an empty trailing word. |
| S30 / `:111` | terminate with nonempty word | Correctly appends the last word; guard is disjoint from S29. |
| S31 / `:113` | whitespace with empty current word | Skips leading/repeated whitespace and advances one code point. |
| S32 / `:117` | whitespace with nonempty word | Appends the word, clears it, and advances. |
| S33 / `:122` | nonwhitespace | Appends exactly one code point and advances. Its guard complements S31/S32 on reachable indices. |
| S34 / `:131` | join empty list | Returns the empty string, as Python join does. |
| S35 / `:132` | join nonempty list head | Emits the first string without a leading separator and delegates the tail. |
| S36 / `:134` | join empty tail | Returns empty suffix. |
| S37 / `:135` | join nonempty tail | Emits one separator and consumes one list item; S34–S37 are disjoint by list shape. |
| S38 / `:141` | separator absent | Returns the entire remaining string as one field. |
| S39 / `:143` | separator present | Emits the prefix and recurses after a nonempty separator. For the submitted comma, the remaining string strictly shortens and the rule preserves leading, trailing, and repeated empty fields exactly like `str.split(",")`. S38 and S39 are disjoint. |
| V01 / `verification.k:13` | matching function lookup | Returns the exact parameters/body of the matching `FuncDef`; the real module matches at its first and only definition. |
| V02 / `:15` | nonmatching function lookup | Consumes one `FuncDef` only under unequal names; disjoint from V01. Other statement heads are off the actual module-lookup path. |
| V03 / `:19` | invoke one-parameter closure | Creates the exact fresh local map binding used by the submitted function. |
| V04 / `:21` | returned outcome value | Direct. A `normal` function fallthrough is unmodeled, but every path in this function returns. |
| V05 / `:22` | conditional outcome value | Selects corresponding result values without losing either branch's return behavior. |
| V06 / `:24` | run module entry | Looks up and invokes the required `split_words` entry point with `VStr(S)`. |
| V07 / `:31` | `solutionAST` | Definitional constructor constant; mechanically identical to trusted regeneration. It supplies code, not a result. |
| V08 / `:84` | `oddLetterCount` | Total definitional sum of the same 13 `countAllOccurrences` terms executed by the final body expression. It does not replace execution and has no overlapping equations. |
| V09 / `:100` | `containsWhitespace` | Total definition of the exact join/split inequality computed by the first `If`; it does not preempt that execution and has no overlap. |

### Evaluation, state, overlap, termination, and trust observations

- Expression evaluation order is represented recursively. The submitted
  operands and method calls have no side effects or exceptions for string
  inputs, so any equational normalization order cannot change observable
  behavior.
- The environment map carries the only mutation. No heap, I/O, allocation,
  exception, or global state is used or silently fabricated.
- All local rule families are constructor-disjoint or guard-disjoint on their
  used domains. No priority is needed to resolve an overlap.
- `exec`, the join functions, `findFunction`, and the two split functions
  structurally consume a list, advance a bounded index, or shorten a string.
  The only problematic generic cases—empty split separator, empty count
  needle, invalid substring index, and non-string list contents—cannot be
  produced by the submitted AST on a string input.
- The 29-character whitespace literal was checked against Python
  `isspace()` for every Unicode code point: exact set equality, no omissions,
  additions, or duplicates. Evidence:
  [script](evidence/whitespace_inventory_check.py) and
  [result](evidence/stage5_whitespace_table_exhaustive.log).
- The imported K `lengthString`, `substrString`, `findString`,
  `countAllOccurrences`, string equality, integer, Boolean, list, and map
  operations are the low-level fixed-library trust boundary. Relevant installed
  declarations/equations are preserved in
  [stage5_trusted_k_string_primitives.log](evidence/stage5_trusted_k_string_primitives.log).

No inventoried rule encodes an unconstrained answer, bypasses the function
body, or enables a false result for a submitted-program input. The named
postcondition functions are definitional summaries: expanding them yields the
same independently executed operations, and they are not used as operational
shortcuts on the left-hand side.

## 6. Fresh non-vacuity test

The candidate did not provide a `spec-vacuity.k`; no candidate mutation was
trusted.

The fresh reviewer mutation changes the submitted reachable claim
`split_words("abcdef") == 3` to the false result `VInt(4)`. The initial state
has no unsatisfied precondition, and independent Python plus concrete K
execution both establish the actual result `3`.

The mutation:

- parsed and built successfully under `kprove --dry-run`, exit 0;
- then failed under actual proof with exit 1 and
  `WarnStuckClaimState`;
- reached the expected residual `<k> VInt ( 3 ) ~> ... </k>`, which could not
  unify with destination `VInt(4)`.

This is a reached, result-bearing failure, not a parser error, missing import,
timeout, or unrelated backend crash.

Evidence:

- [fresh mutation source](evidence/spec-vacuity-audit.k)
- [successful dry run](evidence/stage6_false_mutation_dry_run.log)
- [expected proof failure and residual](evidence/stage6_false_mutation_proof.log)

## 7. Proven versus assumed accounting

### What the proof establishes

Under the submitted `MPY-SEMANTIC`/`MPY-VERIFICATION` theory, for every finite K
`String S`, evaluation of the exact constructor translation of the submitted
`split_words` body reaches the exact piecewise result stated by the universal
claim:

- whitespace-split list when the body's join/split inequality is true;
- otherwise comma-split list, including empty fields, when a comma occurs;
- otherwise the sum of occurrences of the 13 fixed ASCII letters.

It also establishes the seven exact concrete results in `spec.k`. This is a
partial-correctness result. The structural recursion gives a persuasive
termination argument for the used subset, but termination is not promoted into
a separate K theorem here.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` correctly preserves the supported CPython AST | Identity of the `.mpy` program being proved | Acceptable trusted input; byte regeneration and exact AST-token identity were checked. |
| K compiler, LLVM/Haskell backends, and K logical implementation | Every `krun` and `kprove` result | Necessary foundational tool trust; versions and fresh commands are recorded. |
| Installed K `DOMAINS` integer, Boolean, string, list, and map primitives | All semantic equations | Acceptable low-level semantics boundary. Relevant declarations were inspected; no task result is hidden in them. |
| Candidate equations for `split`, comma split, join, count, environment, and returns model the used Python subset | Universal theorem's bridge to actual Python behavior | Supported by exhaustive static review and 22 fresh K/Python cases. This is not a machine-checked theorem about CPython itself, so the universal cross-language bridge remains partly informal. |
| The whitespace literal represents Python single-character whitespace | First branch | Exhaustively supported over all Unicode code points by Python `isspace()` set comparison; recursive split correctness remains a mathematical review of the equations. |
| `solutionAST` is the submitted program | Every formal claim | Strongly supported: trusted byte regeneration, exact 414-token comparison, K pinning claim, and body-sensitivity mutation. |
| `containsWhitespace` and `oddLetterCount` mean the human-facing predicates suggested by their names | Intent interpretation of the postcondition | Their equations are transparent and mathematically appropriate to a literal prompt reading. They are not opaque assumptions. |
| Candidate behavior equals the trusted canonical on the intended domain | Natural-language task adequacy | Not true over unrestricted strings; concrete counterexamples are recorded. Accepting the candidate requires choosing the prompt's literal whitespace/ASCII interpretation over canonical edge behavior. This is the material concern. |

There is no fresh or opaque local symbol whose arbitrary interpretation can
select a branch or returned value. Finite differential tests are used only as
bridge evidence and counterexamples; they are not substituted for the K proof.
The proof itself is the fresh `#Top` reconstruction plus the audited theory.

### Gate summary

- Real-program soundness: **pass**. Exact body pinned; no unsound reachable
  extension; all claims freshly close; false mutation is rejected.
- Intent adequacy: **concern**. The theorem accurately describes the candidate,
  but the candidate is not extensionally equal to the trusted canonical on the
  unrestricted stated string domain.
- Evidence and auditability: **pass with an explicit cross-language trust
  boundary**. Commands, statuses, inputs, mutations, and bounded outputs are
  preserved under `/audit-output/evidence/`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
