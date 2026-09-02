# Independent adversarial audit: 51-remove-vowels

The candidate contains a legitimate, result-constraining partial-correctness
proof of its real translated program under its generated semantics. The proof
was rebuilt from source, its only positive claim freshly closed with `#Top`, the
claim is byte-level pinned to the trusted translation, and meaningful body and
postcondition mutations were rejected.

The result has concerns rather than a clean pass. Symbolic execution leaves the
external string-deletion primitive opaque and defines the postcondition using
that same primitive, so the proof is parametric in the primitive and does not
separately prove a character-level “contains no vowels” theorem. Ground
behavior is fixed through K's imported `replaceAll` hook and is strongly,
reproducibly consistent with both Python implementations. Also, the generated
semantics is executable on the Haskell backend used for the proof but its
`[concrete,simplification]` helper does not execute under the freshly built LLVM
backend, and an unused empty-needle generalization diverges. Neither limitation
enables a false result for the submitted program.

## 1. Input and provenance integrity

The rendered `GENERATED_SEMANTICS` boundary is internally consistent:
`/reference/reference-semantics` does not exist. I did not search for or infer
any hidden reference semantics. The candidate also has no
`reference-semantics/` tree. There is therefore no infrastructure breach.

All required candidate artifacts exist with the expected type:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`codex-trace/`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, and `spec.k` are regular files except the trace
directory. No candidate symlink exists. `prove.sh` also exists as a regular
file. There are no missing, changed, mistyped, or symlinked required
artifacts.

The candidate prompt and translator are byte-identical to their trusted
mounts:

- `prompt.py`: SHA-256
  `94f4ed2b675b10bfe15e0adb2ea620b19790cfb4df26b9362df57d6daa6c9b8b`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The full type/tree check, comparisons, metadata, and bounded log excerpts are in
`/audit-output/evidence/stage1_integrity.log`. The candidate contains extra
generated caches (`semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/`). They are not source-integrity failures, but I did not use
them. Only source artifacts were copied to
`/tmp/audit-work/candidate-src`; trusted files were separately copied to
`/tmp/audit-work/trusted`.

I read all 237 JSONL records in the structured trace (zero parse errors) and all
11,111 lines of `codex-output.log`, solely as untrusted provenance claims.
Their bounded summaries are
`/audit-output/evidence/stage1_trace_summary.log` and
`/audit-output/evidence/stage1_log_summary.log`. The untrusted reports claim a
successful `#Top`, but that claim played no role in the verdict.
`run-input.json` claims problem `51-remove-vowels`, condition `bare`, and no
supplied semantics; `metrics.json` claims a clean generation exit. These claims
are consistent with, but do not establish, the independently observed files.

Fresh tooling was K `v7.1.293`; see
`/audit-output/evidence/tool_versions.log`.

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `remove_vowels(text)` to return the input string
with vowels removed. The examples and trusted canonical implementation clarify
that this means deleting each character whose lowercase form is one of
`a,e,i,o,u`, while preserving every other character and its order.

`/candidate/solution.py` performs ten sequential `str.replace(vowel, "")`
calls, once for each lower- and upper-case ASCII vowel. This is a different but
equivalent algorithm for the intended string domain.

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` regenerated a file byte-identical to the submitted
`solution.mpy`. Both have SHA-256
`1b0f4951b9dbf084dcb7a3542bf3259efff37c566a6322023be96a16d7de0d14`.
The exact command and exit status 0 are in
`/audit-output/evidence/stage2_translator.log`.

The independent differential harness is
`/audit-output/evidence/differential_test.py`. It loads the trusted canonical
entry point and submitted entry point from separate paths and tests:

- all six documented examples;
- 19 explicit empty, single-vowel, case, newline, long, NUL, punctuation, and
  Unicode boundaries;
- all 2,955 strings of lengths 0 through 3 over
  `aeiouAEIOUbc0\n`;
- 2,000 deterministic generated strings of lengths 0 through 64 over the full
  Python code-point range; and
- every one of the 1,114,112 Python code points as a singleton.

There were zero mismatches. The seed, input construction, examples, outputs,
command, and exit status are preserved in
`/audit-output/evidence/stage2_differential.log`. This is strong finite evidence
and exhaustive singleton evidence, not a replacement for the K proof.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

No candidate definition or cache was reused. I created distinct fresh
definitions from the copied sources:

1. `kompile semantic.k --backend llvm --main-module MPY --syntax-module
   MPY-SYNTAX --output-definition
   /tmp/audit-work/semantic-llvm-kompiled` — exit 0
   (`stage3_build_llvm.log`).
2. `kompile semantic.k --backend haskell --main-module MPY --syntax-module
   MPY-SYNTAX --output-definition
   /tmp/audit-work/semantic-haskell-kompiled` — exit 0
   (`stage3_build_semantic_haskell.log`).
3. `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module MPY-SYNTAX --output-definition
   /tmp/audit-work/verification-haskell-kompiled` — exit 0
   (`stage3_build_haskell.log`).

`spec.k` contains exactly one, unlabeled positive claim. Therefore the
unfiltered command ran every target:

```text
kprove spec.k --definition /tmp/audit-work/verification-haskell-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

The bounded log is
`/audit-output/evidence/stage3_positive_claim.log`.

The independently built Haskell semantics concretely executed normal and
boundary inputs. The observed K results were:

| Input | K result |
|---|---|
| `""` | `""` |
| `"abcdef\nghijklm"` | `"bcdf\nghjklm"` |
| `"aeiouAEIOU"` | `""` |
| `"zbcdf_123"` | `"zbcdf_123"` |
| `"aBecIdOfuU"` | `"Bcdf"` |
| `"éAßuİ🙂"` | `"éßİ🙂"` |

Each `krun` exited 0; see the six `stage3_krun_*_haskell.log` or
`stage3_krun_*.log` files. Independent Python results for the same cases are in
`stage3_python_oracle.log` and agree exactly.

One backend limitation is visible. The LLVM definition compiled, but even the
empty-input submitted program stopped at `deleteAll("", "a")` and `krun`
exited 113 (`stage3_krun_empty.log`). This is not an audit-infrastructure
failure: the independently built Haskell semantic definition executes all
cases, and the Haskell proof definition closes. It is a portability/executable-
semantics concern caused by how this K version handles the local
`[concrete,simplification]` rule.

Stage 3 result: PASS with a backend concern.

## 4. Adequacy and real-program pinning

The entry claim has no `requires` clause. In plain language, its precondition is:

- `<k>` contains the exact constructor term printed in `solution.mpy`;
- `<input>` is any K `String`; and
- `<result>` is `noResult`.

Its postcondition is:

- `<k>` is `done`;
- the input cell is unchanged; and
- the result cell is exactly
  `result(removeVowelsSpec(INPUT))`.

There are no framed/omitted state cells in the configuration and no helper or
loop claims.

`/audit-output/evidence/stage4_pinning.py` extracts the balanced `Module(...)`
terms from `solution.mpy` and `spec.k`, removes only whitespace, and compares
them. The normalized 508-character terms are exactly equal
(`stage4_pinning.log`). Combined with the trusted-translator byte check, this
pins the claim to the actual generated program rather than a substituted
program.

The precondition is satisfiable. For example:

```text
<k> exact submitted Module(...) </k>
<input> "aB" </input>
<result> noResult </result>
```

The reviewer-authored ground instance in
`/audit-output/evidence/spec-instance.k` requires the result `"B"` and closes
with `#Top`, exit 0 (`stage4_instance_claim.log`). The trusted canonical and
submitted Python functions both return `"B"` for this input.

Body sensitivity was checked separately. I removed only the final
`.replace("U","")`, regenerated its MPY term with the trusted translator, and
ran input `"U"`. K returned `"U"` rather than `""`
(`stage4_body_mutation_krun.log`). A claim demanding the original specification
then got a genuine stuck final configuration and exited 1
(`stage4_body_mutation_proof.log`). Thus the proof does depend on the real
body.

The result is neither free nor tautological: the fresh postcondition mutation
in Stage 6 is rejected.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule/claim inventory, including domains, matched
contexts, state footprints, value influence, and reviewer decisions, is
`/audit-output/evidence/stage5_rule_inventory.md`. The source-oriented extraction
is `stage5_source_inventory.log`.

### Local declaration inventory

`semantic.k` declares:

- `Program ::= Module(Stmt)`;
- `Stmt ::= FuncDef(String,Params,Stmt) | Return(Expr)`;
- `Params ::= Params(String)`;
- `Expr ::= Name(String) | Str(String) | Attribute(Expr,String) |
  Call(Expr,Expr,Expr)`;
- the `[function]` symbol `deleteAll(String,String)`;
- `Value ::= strVal(String)`;
- partial `[function]` symbols `eval(Expr,String,String)` and
  `replaceValue(Value,String,String)`;
- `Result ::= noResult | result(String)`; and
- `KItem ::= done`.

`verification.k` declares exactly three `[function,total]` symbols:
`removeLowerVowels`, `removeUpperVowels`, and `removeVowelsSpec`. Each has one
unconditional, nonrecursive equation, so coverage is complete and termination
is immediate.

There are no local `[functional]` declarations, priorities, `owise` rules,
macros, fresh generators, or helper K files. The only simplification rule is
the concrete `deleteAll` equation. The only claim is the entry claim in
`spec.k`.

The configuration has only `<k>`, read-only `<input>`, and single-write
`<result>` cells. No state required by this expression-only program is omitted.

### Complete local rule decisions

| Rule | Decision |
|---|---|
| `deleteAll(S,N) => replaceAll(S,N,"")` for concrete arguments | An external string-primitive equation. Correct and executable on the proof backend for all ten nonempty literal needles actually used. It stays opaque symbolically. |
| `eval(Name(X),P,I) => strVal(I)` when `X ==String P` | Correct lookup for the sole formal parameter. |
| `eval(Str(S),_,_) => strVal(S)` | Correct literal evaluation. |
| `eval(Call(Attribute(E,"replace"),Str(OLD),Str(NEW)),P,I) => replaceValue(eval(E,P,I),OLD,NEW)` | Correct receiver-first evaluation for the submitted calls; arguments are literals with no effects. Other call shapes remain visibly unmodeled. |
| `replaceValue(strVal(S),OLD,"") => strVal(deleteAll(S,OLD))` | Correct bridge to the fixed external `str.replace` primitive for the submitted empty-replacement calls. |
| module/function-entry rule | Correctly invokes the exact sole function body with its sole parameter and reads the input cell. It changes no other state. |
| final `strVal` rule | Correctly writes the result and reaches `done`; it requires exact `<k>` contents and does not discard a continuation. |
| `removeLowerVowels` equation | Truthful definitional summary of the five lowercase operations; unconditional, total, no overlap. |
| `removeUpperVowels` equation | Truthful definitional summary of the five uppercase operations; unconditional, total, no overlap. |
| `removeVowelsSpec` equation | Truthful composition of the preceding two summaries; unconditional, total, no overlap. |

Every constructor in `solution.mpy` maps to these declarations and rules:
`Module`/`FuncDef`/`Params`/`Return` use the entry rule; `Name` and `Str` use
their evaluator rules; each nested `Attribute`/`Call` uses the call and
replacement rules; and finalization writes the returned string. Concrete runs
exercise every local semantic rule.

No program-defined operation is replaced by an unconstrained oracle. The real
ten-call body is symbolically traversed. `deleteAll` is result-bearing and
opaque for symbolic input, but its origin is the fixed external `str.replace`
operation rather than program-defined code. The theorem is
interpretation-parametric in that primitive: execution and the postcondition
apply it in the same order, while its ground behavior is fixed by the imported
K string hook. This is a legitimate trust boundary, not a universal proof that
the primitive has the natural-language meaning.

The generalized R1 domain is broader than needed. A reviewer program using an
empty search string timed out after 10 seconds and the backend was terminated
(`stage5_deleteAll_empty_old.log`), whereas Python
`"abc".replace("", "")` returns `"abc"`. A nonempty overlapping probe
`"aaa".replace("aa","")` returned `"a"` in both K and Python
(`stage5_deleteAll_overlap.log`, `stage5_deleteAll_python.log`). The empty-
needle observation is a termination/coverage gap for an unused program shape,
not a false-conclusion witness. Consistent with the generated-semantics
boundary, the submitted body only uses nonempty one-character needles. I
therefore do not label R1 materially unsound; no false result was witnessed or
derivable for the intended program domain.

No local rule was found to enable a false conclusion for a satisfying submitted
input. Accordingly, there is no unsupported “unsound rule” label requiring a
false-conclusion witness.

Stage 5 result: PASS with documented external-primitive and over-broad-domain
concerns.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created the distinct reviewer
artifact `/audit-output/evidence/spec-vacuity-audit.k`. It keeps the original
exact program and unrestricted `INPUT:String`, but changes the required result
from:

```text
result(removeVowelsSpec(INPUT))
```

to the deliberately false:

```text
result(removeVowelsSpec(INPUT) +String "!")
```

Input `"aB"` satisfies the unchanged precondition and demonstrably returns
`"B"`, not `"B!"`.

The mutation parsed and built successfully: `kprove --dry-run` exited 0
(`stage6_mutation_dry_run.log`). The real proof attempt exited 1 with
`WarnStuckClaimState`; its residual explicitly contains the unmet equality
between the original nested deletion term and that term with `"!"` appended
(`stage6_mutation_proof.log`). This is the expected result-bearing failure, not
a parser error, timeout, unrelated crash, or unreachable mutation.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the freshly compiled `MPY`/`VERIFICATION` definition, for every K
`String` `INPUT`, starting from the exact trusted translation of the submitted
`remove_vowels` body with `noResult`, evaluation reaches `done`, preserves the
input cell, and writes the tenfold nested deletion term named by
`removeVowelsSpec(INPUT)`. This is a partial-correctness reachability theorem
under the selected semantics. It is body-sensitive and result-constraining.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.293`, its Haskell backend, reachability logic, and imported `STRING`/`replaceAll` implementation | Compilation, concrete string evaluation, and `#Top` | Ordinary low-level K trust boundary. Fresh builds and negative controls reduce, but cannot eliminate, toolchain trust. |
| Trusted `py2mpy.py` maps CPython AST to the submitted constructor term | Real-program pinning | Acceptable: byte identity was independently regenerated. Translator correctness itself is a mounted trusted input, not proved here. |
| Candidate-generated evaluator rules R2-R7 model the used MPY subset | Meaning of the K execution | Acceptable for this exact program after exhaustive static mapping, normal/boundary execution, a ground claim, and body sensitivity. Unused language forms are intentionally absent. |
| Symbolic `deleteAll` and its concrete equation to imported `replaceAll` | Every replacement result and the formal postcondition | Legitimate external primitive, but a concern: no universal K theorem relates this symbol to CPython `str.replace`. Ground K runs and Python comparisons support only the cases exercised. |
| `removeVowelsSpec` denotes the natural-language “remove vowels” result | Intent adequacy | Informal/executable bridge, not a separately proved character theorem. Its ten operations match the canonical behavior on all recorded evidence, including every Unicode singleton and generated multi-character strings. |
| K `String` represents the intended Python string observations | Domain alignment | Adequate for tested empty, ASCII, newline, NUL, and Unicode cases. A full formal isomorphism with every CPython string representation is not established. |
| Termination of the real Python implementation | Scope beyond partial correctness | The finite chain of ten built-in calls plainly terminates for ordinary Python strings, but the Kit theorem is reported only as partial correctness. |

Differential testing, candidate prose, and generation traces are not used as
substitutes for the K proof. They support only program/canonical alignment and
the external intent bridge.

Gate A (real-program soundness): PASS. Gate B (material intent adequacy): PASS,
with the unformalized character-level bridge recorded as a limitation. Gate C
(trust and reproducibility): PASS, with finite evidence described honestly.
The limitations are enough to withhold an unqualified PASS but do not make a
false theorem provable or disconnect the claim from the real program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
