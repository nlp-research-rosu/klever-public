# Adversarial audit: 111-histogram

## Executive decision

The submitted commands can be reconstructed: every one of the 15 positive
claims exits zero and prints `#Top`, the program translation is exact, and the
generated semantics agrees with Python on the exercised intended-domain cases.
The proof is nevertheless not legitimate. The two rules in
`/candidate/lemmas.k` replace the two arbitrary-length, result-bearing program
loops by denotational summaries. The candidate machine-checks empty and
single-item cases, but it does not machine-check either universal connection
between the fixed loop semantics and the summary. Instead, it compiles the
universal connections as ordinary rules and then uses those rules to close the
entry claims.

Fresh universal connection claims against the unextended semantics both stop on
exactly the missing equality
(`execFor(..., WORDS, ..., ENV) == normal(countLoop/selectLoop(WORDS, ENV))`).
This is a core Gate A connection failure, not a timeout or infrastructure
failure. I found no false intended-domain instance of the two equations and
therefore do **not** label the equations themselves false or unsound. The defect
is that the K proof assumes the property-bearing induction step it needs to
prove. Ground checks and an informal structural-induction argument do not turn
that assumed rule into the required machine-checked universal connection
theorem.

Evidence files and their recorded exit statuses are indexed in
`evidence/38_evidence_index.log`. Tool versions are in
`evidence/00_environment.log`.

## 1. Input and provenance integrity

### Rendered semantics boundary

This is `GENERATED_SEMANTICS` mode. `/reference/reference-semantics` is absent,
as required; there is no contradictory trusted semantics mount. This is
recorded in `evidence/02_provenance_integrity.log`. Therefore the audit proceeds
against the candidate's own `semantic.k`; no hidden or inferred reference
semantics was used.

### Required artifacts

The following candidate source artifacts are regular, non-symlinked files:

- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `lemmas.k`, `spec.k`
- `prove.sh`
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the JSONL structured trace

There is no candidate `PROOF.md` or `spec-vacuity.k`; neither was a required
generation deliverable here. The candidate also contains `__pycache__` and
three compiled-definition directories. They are extra generated outputs, not
trusted sources. They were not copied or used. The exact scratch-copy command
and copied file list are in `evidence/01_scratch_source_copy.log`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
trusted/candidate SHA-256 pairs and successful `cmp` statuses are in
`evidence/02_provenance_integrity.log`. No required artifact is missing,
mistyped, symlinked, or changed.

### Untrusted generation claims

The untrusted metadata claims a successful, non-timeout generation and says
that four module-level proof commands printed `#Top`. The 2.1 MB textual log
and the 395-record JSONL trace make the same claim. I treated those only as
claims. Bounded extracts are in `evidence/03_untrusted_claims.log`; a streaming
summary that reads the complete JSONL trace is in
`evidence/04_trace_summary.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a string representing lowercase letters separated by spaces, count every
letter and return a dictionary containing every letter tied for the greatest
count, mapped to that count. Return `{}` for the empty input. The five prompt
examples instantiate empty input, all-tied input, a two-way tie, and a unique
winner.

The trusted canonical implementation uses `test.split(" ")`, scans for the
maximum nonempty token count, then inserts every list element whose count is
that maximum. The candidate uses `test.split()`, builds a count dictionary and
running maximum in one loop, then selects maximum-count keys in a second loop.
On a strict domain of lowercase-letter tokens joined by exactly one ASCII
space, these are different algorithms for the same result.

### Translation identity

I regenerated the MPY program in scratch with the trusted translator:

```text
python3 trusted/py2mpy.py solution.py > solution.regenerated.mpy
```

The regenerated and submitted files are byte-identical, both with SHA-256
`27dbd7021b90510745698e63226b6c6b358013e4a2aa7f54712922df5e3e4662`.
See `evidence/05_translation_identity.log`.

### Independent differential test

`evidence/differential.py` independently imports
`/reference/canonical.py:histogram` and the scratch candidate entry point. It
checks the documented examples and explicit branch boundaries, then exhausts
all 9,841 `a`/`b`/`c` token lists of length zero through eight joined by one
ASCII space. There are zero mismatches. The command, complete deterministic
input construction, and result are preserved in
`evidence/06_python_differential.log`.

The script records ambiguous separator cases separately. Six disagree with the
canonical implementation: `" a"`, `"a "`, `"a  b"`, `"a   a"`, `"a\tb"`,
and `"a\nb"`. The candidate omits empty fields and splits tab/newline
whitespace; the canonical implementation can retain an empty-string winner or
treat tab/newline as part of one token. Leading/trailing/repeated separators
are outside the strict single-separator lowercase-letter domain used for the
zero-mismatch result. This remains an intent-boundary limitation because the
prompt does not explicitly spell out separator normalization.

## 3. Clean proof reconstruction

All work occurred under `/tmp/audit-work/111-histogram`. Only source files were
copied; candidate compiled definitions and caches were excluded.

K v7.1.293, Python 3.10.12, and Java 17 were available
(`evidence/00_environment.log`). Fresh builds were:

- LLVM concrete semantics:
  `kompile semantic.k --backend llvm --main-module SEMANTIC
  --syntax-module MPY-SYNTAX --output-definition
  semantic-audit-kompiled` — exit 0
  (`evidence/07_build_concrete_semantics.log`).
- Haskell base proof definition:
  `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  verification-audit-kompiled` — exit 0
  (`evidence/10_build_verification.log`).
- Haskell loop-rule proof definition:
  `kompile lemmas.k --backend haskell --main-module
  VERIFIED-LOOP-LEMMAS --syntax-module MPY-SYNTAX
  --output-definition lemmas-audit-kompiled` — exit 0
  (`evidence/11_build_lemmas.log`).

The LLVM build reports two non-exhaustive `[total]` functions:
`envGet(Map,String)` and `execFor(Expr,List,Stmts,Map)`. Their uncovered
inputs are discussed in stages 5 and 7.

### Concrete generated-semantics reconstruction

The fresh LLVM definition executed the submitted `solution.mpy` on empty,
singleton, all-tied, two-way-tied, unique-winner, repeated-space, and
leading-space inputs. Every `krun` exited zero. The K `pyDict` results agree
with independently executed candidate Python on every listed input; full
commands and outputs are in `evidence/09_concrete_semantics_comparison.log`
(with the standalone empty run also in `evidence/08_krun_empty.log`).

### Every positive claim, independently

Each claim was selected and run separately. Every command exited zero and
printed `#Top`:

- Count-loop claims: `count-empty`, `count-existing-raises-step`,
  `count-fresh-step`, `count-existing-keeps-step`,
  `count-fresh-keeps-step` — `evidence/12_...` through
  `evidence/16_...`.
- Selection-loop claims: `select-empty`, `select-equal-step`,
  `select-unequal-step` — `evidence/17_...` through
  `evidence/19_...`.
- Five prompt-example claims — `evidence/20_...` through
  `evidence/24_...`.
- `all-token-lists` and `all-space-separated-strings`, using the freshly
  compiled loop-rule definition — `evidence/25_prove_all_token_lists.log`
  and `evidence/26_prove_all_strings.log`.

The count and selection base/one-item claims are reported by `kprove` as
`WarnTrivialClaim`: function simplification normalizes the two sides to the
same term before reachability rewriting. That is still a zero/`#Top` closure,
but it is not a proof by induction over an arbitrary list.

## 4. Adequacy and real-program pinning

### Claim meanings and preconditions

There are 15 claims:

| Claims | Plain-language precondition and postcondition |
|---|---|
| `count-empty` | For any environment, the exact count-loop `execFor` on `.List` returns `normal(ENV)`. No guard. |
| Four count singleton claims | For a one-item list, an integer count is either existing/fresh and the updated count is either greater than or no greater than integer maximum `M`. Under the corresponding guard, executing the exact two-statement body equals `normal(countIteration(...))`. |
| `select-empty` | For any environment, the exact selection loop on `.List` returns the environment unchanged. |
| `select-equal-step` | When the selected count value equals `maximum`, a one-item exact body execution equals `selectIteration`, including the result insertion. |
| `select-unequal-step` | When the values are unequal, a one-item exact body execution equals `selectIteration`, which updates only `letter`. |
| Five example claims | The closed program on each prompt string returns the exact ordered `pyDict` shown in the postcondition. No guard. |
| `all-token-lists` | For every K `List` (no element-type invariant), `executeWords(histogramProgram(), WORDS)` reaches `histogramSpec(WORDS)`. |
| `all-space-separated-strings` | For every K `String`, `execute(histogramProgram(), INPUT)` reaches `histogramSpecString(INPUT)`. |

The two entry claims have no `requires`; their preconditions are therefore
satisfiable. Examples include `WORDS = .List`, `INPUT = ""`, and
`INPUT = "a b b a"`. `evidence/37_entry_ground_substitution.log` records
empty, tied, and unique-winner witnesses and equal results from both Python
implementations. The corresponding K results are in
`evidence/09_concrete_semantics_comparison.log`.

### Program identity

The `<k>` entry claims execute `histogramProgram()` rather than mentioning a
file. The single equation defining that constructor is a closed transcription
of the translated program. I parsed `solution.mpy` and an explicit
transcription of `verification.k` lines 9–31 to KORE with the fresh definition;
the two 8,390-byte terms are byte-identical and have the same SHA-256. See
`evidence/28_program_ast_pinning.log`. Thus this is the submitted program AST,
not a substituted algorithm.

### Result constraint and the core adequacy defect

For intended inputs, `histogramSpecString` is reducible: it uses
`splitWords`, recursive `countLoop`, recursive `selectLoop`, and `envGet`.
It is not a free result variable or an unconstrained opaque oracle. The exact
examples and the fresh false-result mutation also show that the postcondition
discriminates values.

However, the entry proof does not obtain this result by symbolically executing
arbitrary-length `execFor`. The two ordinary rules in `lemmas.k` preempt those
loops and replace them with `normal(countLoop(...))` and
`normal(selectLoop(...))`. Those values directly determine the final result.
No independently proven arbitrary-list claim connects either summary to the
fixed semantics.

I restated both connections as claims in
`evidence/connection-spec.k` and ran them against
`verification-audit-kompiled`, where the bridge rules are absent. Both parse
and begin proof normally, then exit 1 with `WarnStuckClaimState` on the exact
unmet equality. See `evidence/29_missing_count_connection_probe.log` and
`evidence/30_missing_select_connection_probe.log`. This establishes the
evidence gap; it does not establish that the equations are mathematically
false.

## 5. Rule-by-rule static soundness review

`evidence/27_static_declaration_inventory.log` is the line-addressed exhaustive
declaration/attribute inventory. The following groups enumerate every local
declaration and rule.

### `semantic.k`: syntax, configuration, and all 60 rules

Surface syntax declarations are:

- `Program = Module(Stmts)`;
- list sorts `Stmts`, `Exprs`, and `Entries`;
- statements `FuncDef`, `Assign`, `For`, `If`, and `Return`;
- `Params`, `Entry`, and `CmpOp`;
- expressions `Name`, `Int`, `Str`, `DictExpr`, `Attribute`, `Call`,
  `Subscript`, `BinOp`, and `Compare`.

Runtime declarations are `pyInt`, `pyString`, `pyWords`, `pyList`, `pyDict`,
and `pyBool`; `normal` and `returning`; and entry items `execute` and
`executeWords`. The only cell is `<k>`. State is an explicit `Map` argument;
there is no heap, call-stack, output, or exception cell. That small
configuration is adequate for this target's single pure function, local
bindings, lists, dictionaries, loops, and return.

Every `[function,total]` declaration is:
`resultOf`, `splitWords`, `splitValue`, `eval`, `envGet`, `dictGet`,
`addValues`, `compareValues`, `truth`, `assign`, `dictSet`, `iterable`,
`exec`, `execNext`, `execStmt`, `execIf`, `execFor`, and `execForNext`.
There is no locally declared opaque or explicitly `[functional]` symbol and no
explicit priority rule.

All rule groups, with every case, are:

| Lines | Complete rule inventory | Static decision |
|---|---|---|
| 58–66 | `execute` string, `executeWords` token-list harness; `resultOf(returning)` and `resultOf(normal)` | Exact function-name/parameter binding and body execution. `normal -> false` is unreachable for the real body because it ends in `Return`. |
| 71–84 | `splitWords`: empty, leading ASCII space, no-space remainder, positive first-space index; `splitValue`: string, token-list harness, `owise` | Sound for empty and ASCII-space-separated strings. It intentionally does **not** model Python no-argument `split()` on tab/newline/other Unicode whitespace. |
| 88–100 | `eval`: integer, string, name, empty dict, no-argument `.split`, subscript, integer `+`, comparison, `owise` | Covers every expression in `solution.mpy`; source evaluation is pure, so no omitted effect changes order. The fallback fabricates `false` for unused malformed expressions but cannot preempt a used case. |
| 103–106 | Three `envGet` equations; the update-hit and update-miss equations are `[simplification]` | The equations are valid map lookup facts. Missing-key maps are uncovered despite `[total]`; all real-program lookups are initialized/reachably present. |
| 109–114 | Four `dictGet` equations; update-hit/update-miss are `[simplification]`, then map-entry hit and `owise false` | Valid on reachable dictionaries. The missing/wrong-value fallback differs from Python `KeyError`, but every real lookup is membership-guarded or iterates an existing key. |
| 117–129 | `addValues`: int and `owise`; `compareValues`: membership, integer `>`, K equality, `owise`; `truth`: bool, int, `owise` | Correct on the reachable integer/bool types. Wrong-type fallbacks replace Python exceptions, but no intended execution reaches them. |
| 134–151 | `assign`: local name, named-dict subscript, `owise`; `dictSet`: existing key, fresh key with insertion-order append, `owise`; `iterable`: list, ordered dict keys, `owise` | Correct state changes and dictionary insertion/iteration order for the target. Unsupported assignment/iteration fallbacks are unreachable. |
| 162–189 | `exec`: empty/cons; `execNext`: normal/returning; `execStmt`: assign/if/for/return/`owise`; `execIf`: true/false; `execFor`: empty/cons; `execForNext`: normal/returning | Deterministic big-step sequencing, one-time iterable evaluation, state threading, early return, and loop order match the used control flow. `execFor` is non-exhaustive for a generic K `List` containing non-`PyVal` elements, but `splitWords` produces only `pyString` elements. |

There are ten semantic `owise` fallback rules: `splitValue`, `eval`,
`dictGet`, `addValues`, `compareValues`, `truth`, `assign`, `dictSet`,
`iterable`, and `execStmt`. They are the only implicit fallback priorities in
this file. The four simplification rules are precisely the two `envGet` update
rules and two `dictGet` update rules. I found no overlap with disagreeing
right-hand sides on reachable inputs.

Construct coverage is complete for `solution.mpy`: `Module`/`FuncDef` is
handled by `execute`; statement sequencing, both `For` loops, both kinds of
`If`, assignments, and return are handled by `exec*`; every used `Name`,
`Int`, empty `DictExpr`, `Attribute`/`Call` to `split`, `Subscript`, `+`, and
`in`/`>`/`==` comparison is handled by `eval` and its primitives. `Str`,
`Entry`, nonempty literal dictionaries, and general calls are unused and need
not be modeled in generated-semantics mode.

### `verification.k`: all 18 total functions and 23 rules

All local declarations are `[function,total]`:
`histogramProgram`, `nextCount`, `putCount`, `raiseMaximum`,
`countIteration`, `countLoop`, `selectIteration`, `selectLoop`, `dictKeys`,
`initialEnvWith`, `initialEnv`, `afterCountWith`, `afterCount`,
`beforeSelectWith`, `beforeSelect`, `histogramSpecWith`, `histogramSpec`, and
`histogramSpecString`.

The complete equations are:

- one exact closed equation for `histogramProgram` (lines 9–31);
- three `nextCount` equations: present, absent, and `owise`;
- one `putCount`;
- two disjoint `raiseMaximum` guards (true/false);
- one `countIteration`;
- base and cons equations for `countLoop`;
- two disjoint `selectIteration` guards (equal/not equal);
- base and cons equations for `selectLoop`;
- `dictKeys(pyDict)` and `dictKeys(owise)`;
- one equation each for `initialEnvWith`, `initialEnv`,
  `afterCountWith`, `afterCount`, `beforeSelectWith`, `beforeSelect`,
  `histogramSpecWith`, `histogramSpec`, and `histogramSpecString`.

`nextCount` and `dictKeys` contain the only two `owise` priorities in this
file. There are no simplification, concrete, explicit priority, or opaque
rules. The recursive list functions descend on the tail. On reachable maps,
the guarded equation pairs cover all Boolean outcomes without overlap, and
the equations truthfully implement one count or selection iteration.

These functions are definitional summaries until an operational rule replaces
execution by them. They do not independently prove that the selected keys are
exactly all maximum-frequency input letters; that human-facing interpretation
is a straightforward but informal induction over `countLoop` followed by
`selectLoop`.

### `lemmas.k`: both ordinary operational rules

There are exactly two rules and no new syntax:

1. Lines 10–20 replace the exact count-loop `execFor` over arbitrary
   `WORDS:List` and arbitrary `ENV:Map` with
   `normal(countLoop(WORDS, ENV))`.
2. Lines 22–29 replace the exact selection-loop `execFor` over arbitrary
   `WORDS:List` and arbitrary `ENV:Map` with
   `normal(selectLoop(WORDS, ENV))`.

Classification: both are result-bearing operational bridges. They match an
exact loop target and exact body. Because `execFor` and the summaries are pure
functions over the explicit map, there is no hidden continuation, stack,
allocation, output, or exception cell for the bridge to discard. The count
bridge changes `letter`, `counts`, and possibly `maximum`; the selection bridge
changes `letter` and possibly `result`. Their values control the returned
dictionary and both universal entry postconditions.

Finite fixed-semantics connections for a three-item count loop and for a
winner/loser selection loop both close with `#Top` without importing
`lemmas.k`; see `evidence/connection-ground-spec.k` and logs 33–34. A
deliberately wrong bridge that discards all count iterations builds but is
rejected with the empty dictionary rather than the required tie result; see
`evidence/lemmas-wrong-count.k` and logs 35–36. These are useful sensitivity
checks.

They do not supply the required universal connection theorem. The submitted
five count claims cover empty and singleton reachable integer-count branches;
the three selection claims cover empty and singleton equal/unequal branches.
None has a symbolic tail plus an induction hypothesis, circularity, invariant,
or another machine-checked derivation that entails either arbitrary-`WORDS`
rule. The fresh exact universal claims fail against the fixed semantics
(logs 29–30).

The rules are also wider than their supporting claims: they accept arbitrary
maps and arbitrary K lists, while the count claims assume integer count and
maximum shapes and `execFor` itself is not exhaustive for non-`PyVal` list
elements. I did not obtain a concrete false conclusion for an intended,
reachable state. Accordingly this review records a missing complete-domain
connection and proof assumption—not a claim that either bridge equation is
false. That narrower gap is still material: compiling the core arbitrary-loop
equations as axioms bypasses the real loop execution in the entry proof.

### `spec.k`: all claims and no hidden extensions

The file contains exactly the 15 claims listed in stage 4. It introduces no
functions, simplifications, priorities, opaque symbols, or ordinary rules.
The example claims use the base definition; only the two main claims import
the compiled operational bridges.

## 6. Fresh non-vacuity test

`evidence/spec-vacuity.k` imports the same freshly compiled loop-rule layer and
changes the concrete result for satisfying input `"a b b a"` from
`a -> 2, b -> 2` to the demonstrably false `a -> 3, b -> 2`.

The dry run builds the mutation successfully and exits zero
(`evidence/31_vacuity_mutation_build.log`). The actual proof exits 1 with
`WarnStuckClaimState`; the residual final configuration visibly contains
`a -> 2, b -> 2` and cannot unify with the mutated destination
(`evidence/32_vacuity_mutation_rejected.log`). This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. The candidate proof is therefore non-vacuous and result-sensitive even
though its loop connection is assumed.

## 7. Proven versus assumed accounting

### What the successful reachability run establishes

Under the combined theory consisting of the generated big-step semantics,
all verification equations, and the two compiled arbitrary-loop bridge rules,
K establishes:

- the five exact prompt results;
- the eight base/single-item loop obligations;
- for every K list, the token-list harness equals `histogramSpec`;
- for every K string, the closed translated program under this generated
  semantics equals `histogramSpecString`.

The theorem constrains a concrete result on intended ground inputs and pins the
submitted AST. It is a theorem of the extended K theory. It is not an
independent proof that the extended loop rules follow from the fixed semantics.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K hooked `Int`, `String`, `Bool`, `Map`, `List`, string substring/length/find, map membership/update, and K equality | All semantics and proof functions | Acceptable low-level mathematical/runtime trust boundary. |
| Trusted `/reference/py2mpy.py` | Program-to-AST identity | Acceptable trusted input; byte regeneration succeeds. |
| Generated big-step model of the used Python subset | Every K execution claim | Empirically supported on normal/boundary cases and statically adequate for used constructs. It remains an informal bridge to CPython, especially for exceptions and no-argument whitespace splitting. |
| `envGet` and `execFor` marked `[total]` despite compiler-reported uncovered cases | Malformed symbolic states and the overbroad list harness | Concerning but not shown to affect the intended split-string execution. No false intended-domain conclusion witness was found. |
| Count and selection arbitrary-list rules in `lemmas.k` | Both universal entry claims; returned dictionary | Illegitimate as proof premises here. They replace program-defined result-bearing loops and lack an independent universal connection theorem. Ground tests and singleton obligations are not substitutes. |
| Informal interpretation of `histogramSpecString` as “all and only maximum-frequency letters” | Natural-language task adequacy | Plausible and supported by code inspection/differential testing, but not stated or proved as a K invariant/property theorem. This would be an adequacy concern even if the loop connection were repaired. |
| Canonical differential testing | Candidate-to-reference behavioral bridge | Finite empirical support only: zero mismatches on 9,841 strict-domain inputs, with six documented separator-edge divergences. It is not part of the K proof. |

No local opaque symbol or unconstrained oracle supplies the expected result.
The decisive issue is instead an assumed operational summary of
program-derived loops. The validating-proof Gate A requirement is not met:
result-bearing program execution is replaced without a universal connection
theorem over the bridge's matched domain. Gate B also retains a documented
split-semantics and summary-to-natural-contract limitation. Gate C evidence is
reproducible, but it honestly supports only finite ground bridges and cannot
repair Gate A.

Therefore the reconstructed `#Top` is real but conditional on a central proof
assumption. It is not a legitimate partial-correctness proof of the real
generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
