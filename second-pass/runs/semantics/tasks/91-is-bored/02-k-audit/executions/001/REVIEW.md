# Independent adversarial audit: 91-is-bored

The candidate is **not a legitimate proof of the requested program contract**.
Its submitted K claims reconstruct cleanly, are non-vacuous, and appear sound for
the narrow statements they actually make. However, those statements include
only three internal loop-continuation claims and two concrete examples. There is
no symbolic full-function entry claim for arbitrary input. Independently, the
generated Python program materially disagrees with the trusted canonical
implementation on the intended string domain.

All candidate material was treated as untrusted. Candidate-built caches, the
submitted `kore-exec.tar.gz`, and the old `prove.log` were not reused. Builds and
experiments used fresh sources below `/tmp/audit-work`; reviewer artifacts and
bounded logs are in `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. There is therefore no
infrastructure-mode contradiction.

`diff --no-dereference -r` between the trusted and candidate semantics trees
returned exit 0. Type/mode manifests also match: both trees contain the same two
directories and 24 regular `.k` files with modes 755/644 as appropriate. The
candidate semantics tree contains no symlink, missing entry, additional entry,
mistyped entry, or changed entry. See
[`evidence/01_integrity.sh`](evidence/01_integrity.sh) and
[`evidence/01_integrity.log`](evidence/01_integrity.log).

The candidate prompt and translator are byte-identical to their trusted
versions:

- `prompt.py`:
  `9445e82177f062459a801e24909bc856435701d82f1d67a9dad1f9d6fd0f6362`
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

### Missing provenance artifacts

The following requested generation artifacts are absent from `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace is present. Because these files do not exist,
their claims could not be inspected. Their absence is a provenance/auditability
gap, not an infrastructure contradiction. The candidate's `prove.log`,
`prove.sh`, concrete tests, archive, and bytecode cache were inspected or listed
only as untrusted evidence and were not used as proof results.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for the count of sentences that start with the word
`"I"`, where `.`, `?`, and `!` delimit sentences. The trusted canonical
implementation gives the executable interpretation:

1. split with `[.?!]\s*`, consuming any Python-regex whitespace after each
   delimiter; and
2. count split pieces whose first two characters are exactly `"I "`.

Thus initial whitespace at the start of the entire input is not stripped, while
Unicode whitespace immediately after a delimiter is stripped.

### Translation fidelity

The trusted translator regenerated `solution.mpy` from `solution.py`; `cmp -s`
returned 0 and both files had SHA-256
`c67074e139048d0e105db65f2c5b19123923087e625626990091a610233ea841`.
The submitted `.mpy` is therefore the real translation of the submitted Python.

### Differential result

The independent differential imports `/reference/canonical.py` and the scratch
copy of the submitted `solution.py`. It covers the documented examples, empty
input, all scanner branches and numeric boundaries, fixed whitespace/Unicode
cases, every string of lengths 0 through 5 over an eight-character boundary
alphabet, and 2,000 deterministic random strings.

Results:

- 37 fixed cases, 6 mismatches;
- 37,449 exhaustive generated cases, 256 mismatches; and
- 2,000 random cases, 0 mismatches (the relevant short patterns are rare in
  that random distribution).

Concrete counterexamples are:

- `" I x"`: canonical `0`, generated `1`. The candidate incorrectly treats
  whitespace at the very start of the whole input as ignorable sentence-leading
  whitespace.
- `"A.\u00a0I x"`: canonical `1`, generated `0`. The canonical regex consumes
  the non-breaking space after `.`, while the candidate recognizes only code
  points 9–13 and 32 as whitespace.

These are material result divergences on the intended Python-string domain.
See [`evidence/differential_test.py`](evidence/differential_test.py),
[`evidence/02_fidelity.sh`](evidence/02_fidelity.sh), and
[`evidence/02_fidelity.log`](evidence/02_fidelity.log). Stage 2 fails.

## 3. Clean proof reconstruction

K v7.1.337 was used. Fresh copies contained the trusted supplied semantics and
only the candidate's source-level `solution.py`, `solution.mpy`, `verification.k`,
and `spec.k`.

The following definitions were built from source:

- LLVM `MPY-KRUN` definition: exit 0.
- Haskell `VERIFICATION` definition: exit 0.

The exact regenerated submitted module was run under the fresh LLVM definition:
it terminated with `.K`, exit code 0, and a module-scope `is_bored` closure whose
body is the submitted translated AST. See
[`evidence/03_build.log`](evidence/03_build.log) and
[`evidence/05_concrete_program.log`](evidence/05_concrete_program.log).

The three mutually recursive loop claims were selected together as their
minimal circularity unit:

```text
kprove ... --claims loop-state-0,loop-state-1,loop-state-2
#Top
[exit 0]
```

Each concrete entry claim was also selected independently; both printed
`#Top` and exited 0. Finally, the complete unfiltered five-claim spec printed
`#Top` and exited 0. Evidence:

- [`evidence/04d_loop_claim_unit.log`](evidence/04d_loop_claim_unit.log)
- [`evidence/04c_example_claims.log`](evidence/04c_example_claims.log)
- [`evidence/04b_full_proof.log`](evidence/04b_full_proof.log)

An earlier attempt to select `loop-state-0` alone timed out after 300 seconds
because that filtering removes the companion state circularities. It is
inconclusive and is not used against the candidate; the observation is recorded
in
[`evidence/04a_isolated_claim_observation.txt`](evidence/04a_isolated_claim_observation.txt).

The fresh reconstruction gate therefore passes for the candidate's actual five
claims. This does not establish that the five claims are adequate for the task.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

The three loop claims in `/candidate/spec.k:8`, `:45`, and `:81` state:

- **state 0:** executing the remaining loop over symbolic code sequence `CS`,
  then the real `Return(count)` and call cleanup, returns `bored0(CS, N)`;
- **state 1:** the same continuation from state 1 returns `bored1(CS, N)`; and
- **state 2:** the same continuation from state 2 returns `bored2(CS, N)`.

Each assumes an exact function-frame configuration, empty heap, matching
control stack, no exception, and that the global scope does not shadow builtin
`ord`. Each postcondition fixes the returned value and frame cleanup; it is not
a free variable, tautology, or one-way implication.

The only full-call claims, at `/candidate/spec.k:117` and `:144`, state exactly:

- `is_bored("Hello world") == 0`; and
- `is_bored("The sky is blue. The sun is shining. I love this weather") == 1`.

They have completely concrete entry configurations and exact integer
postconditions.

### Real control flow and satisfying witnesses

`boredFunctionBody` expands to the exact function body in `solution.mpy`, and
`boredLoopBody` expands to the exact body of its `For`. The empty statement
branches in the translated program are `.Stmts` after K parsing. The fresh
`krun` closure and the residual closure printed by the false mutation show the
same expanded body. There is no substituted algorithm or operational shortcut
inside these claims.

Every precondition is satisfiable. Ground witnesses include:

| Claim | Satisfying values | Claimed result | Realizing full input; both Python results |
|---|---|---:|---|
| `loop-state-0` | `GLOBAL=.Map`, `CS=(73,32)`, `N=0`, state `0` | `1` | `"I "`; `1` |
| `loop-state-1` | `GLOBAL=.Map`, `CS=(32)`, `N=0`, state `1` | `1` | `"I "` after consuming `I`; `1` |
| `loop-state-2` | `GLOBAL=.Map`, `CS=(46,73,32)`, `N=0`, state `2` | `1` | `"A.I "` after consuming `A`; `1` |
| `prompt-example-0` | concrete claim configuration | `0` | `"Hello world"`; `0` |
| `prompt-example-1` | concrete claim configuration | `1` | prompt example; `1` |

The full values and computations are preserved in
[`evidence/claim_witnesses.py`](evidence/claim_witnesses.py) and
[`evidence/08_claim_witnesses.log`](evidence/08_claim_witnesses.log).

### Fatal adequacy gap

There is no claim of the form

```text
Call(Name("is_bored"), str(CS)) => bored0(CS, 0)
```

under a symbolic entry configuration, nor an equivalent claim that loads and
executes the submitted `Module` for arbitrary `S`. The loop claims would be
useful circularities inside such a theorem, but the missing connection from
function entry, initialization, and `For` setup to `loop-state-0` is not itself
proved. The two literal examples cannot substitute for that theorem.

Consequently, the K artifact does not establish partial correctness of
`is_bored` over the requested input domain. Stage 4 fails even though the
restricted claims are result-constraining and pinned to the submitted body.

## 5. Rule-by-rule static soundness review

The exhaustive textual inventory is
[`evidence/rule_inventory.tsv`](evidence/rule_inventory.tsv), generated by
[`evidence/rule_inventory.py`](evidence/rule_inventory.py). It enumerates:

- 705 rules;
- 230 syntax declarations;
- 5 contexts;
- 1 configuration; and
- 5 claims.

It also tags every `function`, `total`, `symbol`, `no-evaluators`,
`simplification`, `priority`, `owise`, `concrete`, `macro`, `strict`, and
`seqstrict` occurrence. There are no `[functional]` or `[anywhere]`
declarations. Every inventory row has a review disposition.

### Supplied semantics

All declarations and rules below `reference-semantics/` are byte-identical to
the selected trusted semantics level, so they are not candidate proof
extensions. The relevant execution path is:

| Submitted construct | Declaration and semantic route |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53-61`; `core.k:124-127`; `functions.k:14-16` |
| `Name`, `Int`, `Str` | `syntax.k:9-13`; `core.k:130-154,194`; `str.k:13-17` |
| `Assign`, `AugAssign` | `syntax.k:41,44`; `controls.k:9-31`; integer `+` at `int.k:9` |
| `Call(...ord...)` | `syntax.k:28`; `call.k:20-32`; builtin lookup in `core.k:156-181`; `builtins.k:143` |
| `Compare`, `CmpOp` | `syntax.k:30-32`; contexts/dispatch in `operators.k:15-17`; integer cases in `int.k:22-27` |
| `BoolOp("and"/"or")` | `syntax.k:16`; left-to-right short-circuit context/rules in `bool.k:16-25` |
| `If` | `syntax.k:49`; truthiness and branches in `controls.k:51-54` |
| `For` over `str` | `syntax.k:45`; loop protocol in `controls.k:65-74`; string yields in `str.k:8-10`; name target binding in `tuple.k:31-40` |
| `Return` and call cleanup | `syntax.k:50`; `functions.k:78-90`; closure entry in `call.k:69-74` |

The claims include every active configuration cell: `<k>`, `<env>`,
`<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`,
and `<exit-code>`. Evaluation is left-to-right where relevant; `BoolOp`
short-circuits; `For` evaluates the iterable once, yields one-character
strings, binds `ch`, executes the exact body, and resumes the exact loop
continuation. `Return` pops precisely the frame shown in each loop claim.

The LLVM build warned about several non-exhaustive trusted-baseline helpers
(`mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`). None is reachable
from this submitted AST or any postcondition. They remain part of the supplied
semantics trust boundary, not a candidate-local correctness shortcut.

### Candidate extensions

The candidate adds the following and nothing else:

1. Nullary total `Stmts` functions `boredLoopBody` and
   `boredFunctionBody`, each with one exact AST-expansion rule. These are
   definitional abbreviations, not operational bridges.
2. Total Boolean functions `isBoredDelimiter` and `isBoredWhitespace`.
   Their unconditional integer equations truthfully encode the submitted
   scanner's tests.
3. Total `Val` functions `bored0`, `bored1`, and `bored2`, with six
   simplification rules. Empty/cons patterns are disjoint and exhaustive over
   `IntSeq`; recursive calls strictly consume the tail; branch conditions are
   exhaustive; overlapping right-hand sides do not occur.
4. The five reachability claims already described.

`[no-evaluators]` on `bored0/1/2` does not create an oracle: every constructor
case has a truthful equation. No candidate rule has priority, no program
execution is intercepted, no result-bearing fresh symbol is introduced, and no
rule fabricates an answer for an unmodeled used construct.

I found no materially unsound candidate rule, so there is no unsound-rule
allegation requiring a false-conclusion witness. The narrower defect is that a
sound internal summary is never used in a universal entry theorem. Static Gate
A passes for the restricted theorem; intent adequacy does not.

## 6. Fresh non-vacuity test

The reviewer-created
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k) changes the first concrete
entry result from `0` to `1` and gives it a fresh label. `"Hello world"` is a
satisfying concrete input, and both Python implementations demonstrably return
`0`.

The selected mutation was first passed through `kprove --dry-run`; it built and
parsed successfully with exit 0 and emitted KORE. The real proof then exited 1
with `WarnStuckClaimState`. Its residual configuration has `<k> 0 ~> .K </k>`
while the destination requires `1`. This is the expected unmet result
obligation, not a parser error, timeout, missing import, or unrelated crash.

See [`evidence/07_vacuity.sh`](evidence/07_vacuity.sh) and
[`evidence/07_vacuity.log`](evidence/07_vacuity.log). Stage 6 passes. This shows
that the ground claim constrains its result; it cannot supply the missing
universal theorem.

## 7. Proven versus assumed accounting

### What the successful K run establishes

Conditional on the supplied MPY semantics and K backend, the successful
reachability proof establishes:

1. from each of the three exact internal scanner-state configurations,
   processing any finite symbolic remaining `IntSeq` with the submitted loop
   body and then returning produces the corresponding structurally defined
   `bored0/1/2` value while cleaning up the stated frame; and
2. the exact submitted function body returns `0` and `1` for the two literal
   prompt examples.

It does **not** establish:

- any full-function result for arbitrary `S`;
- equivalence of `bored0(CS,0)` with the canonical regex algorithm;
- equivalence of submitted `solution.py` with `/reference/canonical.py`;
- correctness for the natural-language input domain; or
- Python/K equivalence outside the constructs and values used by the restricted
  claims.

### Trust ledger

- **Supplied semantics:** all 705 fixed rules, its configuration, and K's
  imported integer, Boolean, string, map, list, and equality hooks are trusted
  by the rendered problem boundary. The proof depends specifically on the
  execution path listed in Stage 5.
- **String-literal hooks:** `ordChar`, `substrString`, and `lengthString` are
  trusted for the two ASCII ground examples. The universal loop claims start
  directly from symbolic `str(IntSeq)` and do not use literal conversion.
- **Builtin `ord`:** the fixed rule mapping a one-code string to that code is
  trusted. The loop claims explicitly exclude a global shadow binding; the
  submitted module has no such shadow.
- **Imported opaque but unused symbols:** the supplied definition declares
  `md5hexCodes`; `sortVS`, `sortKeyVS`; and the float-family symbols
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
  `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
  `sqrtF`. None is reachable from the solution or its claims, so none
  contributes to closure.
- **Proof-local summaries:** `bored0/1/2` have `no-evaluators` but are not
  opaque; their exhaustive equations fix every result. No external oracle or
  empirical value bridge is used by the K proof.
- **Real-program structural bridge:** byte-identical trusted translation plus
  direct comparison of the loaded closure and expanded proof closure supports
  that the restricted calls execute the submitted body. This bridge is exact
  for the inspected AST, not a claim that the body meets the task.
- **Intent bridge:** the trusted canonical implementation is the independent
  executable oracle. Differential evidence does not merely fail to prove this
  bridge; it falsifies it with concrete intended-domain witnesses.
- **Partial correctness:** `kprove` establishes reachability under the supplied
  theory; it is not an independent proof of CPython, regex semantics, or the
  natural-language interpretation.

### Decision

The candidate earns credit for a clean, sound, non-vacuous proof of three
internal loop summaries and two examples. The decision boundary nevertheless
requires `FAIL / NOT_LEGIT`: it lacks a universal full-program theorem, and the
actual generated program demonstrably disagrees with the trusted canonical
function on valid string inputs. Missing generation metadata is an additional
auditability gap but is not the basis for converting an infrastructure issue
into the candidate verdict.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
