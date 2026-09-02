# Independent adversarial review: 91-is-bored

The candidate is **not a legitimate proof of the HumanEval task**. A clean
reconstruction does produce `#Top` for all eight submitted claims, and a fresh
false-result mutation is rejected. Those facts establish only eight concrete
executions under the candidate's own semantics. They do not overcome three
material failures:

1. `solution.py` disagrees with the trusted canonical implementation on ordinary
   ASCII inputs.
2. `spec.k` contains only eight ground-input claims and no theorem for arbitrary
   strings.
3. The generated `strip` semantics disagrees with the submitted Python on
   non-ASCII Python whitespace, with concrete false-result witnesses.

All candidate prose, traces, prior builds, and reported `#Top` results were
treated only as untrusted claims. All executable work used fresh definitions
under `/tmp/audit-work/reconstruction`. Reviewer scripts, mutations, and bounded
logs are under `/audit-output/evidence`.

## 1. Input and provenance integrity

### Generated-semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` neither exists nor is a symlink. The only
trusted reference files are regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

Thus there is no infrastructure contradiction and this review may issue a
candidate verdict. The exact checks and exits are in
[`01_integrity.log`](evidence/01_integrity.log).

### Candidate artifacts and untrusted generation claims

The following required candidate artifacts are present as regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
One structured generation JSONL trace is present. No symlinks were found
anywhere under `/candidate`.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. These are additional generated
build/cache artifacts, not source-integrity failures; they were deliberately
ignored and never copied into the fresh reconstruction.

The candidate prompt and translator are byte-identical to the trusted mounts:

| Artifact | SHA-256 | `cmp` |
|---|---|---|
| prompt, candidate and trusted | `9445e82177f062459a801e24909bc856435701d82f1d67a9dad1f9d6fd0f6362` | exit 0 |
| translator, candidate and trusted | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

There are no missing, changed, mistyped, or symlinked required source
artifacts. In particular, the absence of a candidate `PROOF.md` or
`spec-vacuity.k` is not a provenance defect because neither was a deliverable
of the original bare generation prompt.

The untrusted final report claims eight proved claims and 10,000 passing
differential cases. The structured trace confirms that the 10,000-case oracle
was:

```python
sum(part.strip().startswith('I ') for part in re.split(r'[.?!]\s*', s))
```

That oracle repeats the submitted implementation's extra `strip()` behavior;
it is not the trusted canonical implementation. The trace also records an
attempted symbolic-string claim that failed and was then deleted. These are
generation-history facts, not proof evidence. A bounded extraction is preserved
in [`trace_summary.py`](evidence/trace_summary.py) and
[`01_integrity.log`](evidence/01_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended behavior

The prompt says that `is_bored(S)` receives a string, splits it into sentences
at `.`, `?`, or `!`, and counts sentences that start with the word `"I"`.
The trusted canonical implementation uses:

```python
sentences = re.split(r'[.?!]\s*', S)
return sum(sentence[0:2] == 'I ' for sentence in sentences)
```

Accordingly, whitespace immediately after a delimiter is consumed, but
whitespace at the beginning of the whole input is not silently removed.
Likewise, the canonical test examines the original first two characters; it
does not remove trailing whitespace before testing the prefix.

The submitted implementation instead normalizes punctuation, splits on `.`,
then applies `sentence.strip().startswith("I ")`. This changes both leading and
trailing boundary behavior.

### Translator fidelity

The trusted translator was rerun on the scratch copy:

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated.mpy
```

The command exited 0. `cmp` against the submitted scratch
`solution.mpy` exited 0, and both files have SHA-256
`f1425ef9768862e9616ade04b4745aa99d678335a15a4bd8b3070ee499cc9fa6`.
Thus the submitted constructor term faithfully translates the submitted
Python. See [`02_fidelity.log`](evidence/02_fidelity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical entry point and the scratch copy of the submitted entry point. Its
9,709 deterministic cases comprise:

- 28 directed examples and branch/boundary cases;
- all 4,681 strings of length 0 through 4 over
  `('I', 'i', ' ', 'a', '.', '?', '!', '\t')`;
- 5,000 seeded random strings of length 0 through 80, including punctuation,
  ASCII controls, and all Python whitespace classes.

The script exited 1 after reporting **119 mismatches**. Minimal witnesses
include:

| Input | Trusted canonical | Submitted Python | Cause |
|---|---:|---:|---|
| `"I "` | 1 | 0 | `strip()` removes the space required by `"I "` |
| `"\tI agree"` | 0 | 1 | leading input whitespace is removed |
| `" I am here?You are there!  I agree"` | 1 | 2 | the first sentence is incorrectly trimmed |
| `"\tI tabbed.\nI newline?\rNot me!"` | 1 | 2 | the initial tab is incorrectly ignored |

These are valid strings and no prompt precondition excludes them. The
implementation therefore materially diverges from the trusted task on the
intended domain. Full scope, commands, exits, and the first 25 mismatches are in
[`02_fidelity.log`](evidence/02_fidelity.log).

**Stage 2 result: fail.**

## 3. Clean proof reconstruction

### Fresh builds

Only these source files were copied from `/candidate`:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. Trusted `canonical.py`, `prompt.py`, and `py2mpy.py` were copied
separately from `/reference`. No candidate definition or cache was copied.

The live toolchain was:

```text
K v7.1.293 (build 2025-10-03)
Python 3.10.12
```

Fresh builds used explicit new output directories:

```text
kompile semantic.k --backend llvm \
  --syntax-module MPY-SYNTAX --main-module MPY \
  --output-definition semantic-fresh-kompiled

kompile semantic.k --backend haskell \
  --syntax-module MPY-SYNTAX --main-module MPY \
  --output-definition semantic-haskell-fresh-kompiled

kompile verification.k --backend haskell \
  --syntax-module MPY-SYNTAX --main-module VERIFICATION \
  --output-definition verification-fresh-kompiled
```

All three builds exited 0. Logs:
[`03_build.log`](evidence/03_build.log) and
[`03_build_haskell_semantics.log`](evidence/03_build_haskell_semantics.log).

### Positive claims

The original claims have no labels. The audit made a scratch-only
`spec-labelled.k` whose diff adds only labels `audit-1` through `audit-8`;
no term, cell, precondition, or postcondition changed. Each claim was then run
individually:

```text
kprove spec-labelled.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims SPEC.audit-N
```

For every `N` from 1 through 8, `kprove` printed `#Top` and exited 0.
The label-only diff and all eight outputs are in
[`03_proofs.log`](evidence/03_proofs.log).

### Fresh concrete generated-semantics execution

[`k_python_concrete.py`](evidence/k_python_concrete.py) ran the actual
`solution.mpy` through the fresh Haskell semantics on 13 normal and boundary
inputs. K had zero mismatches against the submitted Python on this ASCII-focused
suite, while it had three mismatches against the trusted canonical, including
`"I "`, `" I agree"`, and the candidate's tab/newline example. Exact commands
and results are in
[`03_concrete_haskell.log`](evidence/03_concrete_haskell.log).

The fresh LLVM build crashed on the empty-string boundary in its
`substrString` implementation (exit 113). That crash is preserved in
[`03_concrete.log`](evidence/03_concrete.log). It is not treated as proof of
candidate failure by itself: the unchanged source rebuilt and executed on the
Haskell backend. It is, however, consistent with the reachable partial-slice
problem identified statically in Stage 5.

A later generated-semantics test exposed actual Haskell-versus-Python
divergences for non-ASCII whitespace; those witnessed semantic failures are
analyzed in Stage 5.

**Stage 3 result:** the submitted positive ground claims reconstruct
successfully, but this is not a task-level correctness result.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

None of the eight claims has a `requires` clause or a symbolic input. Each
precondition is the exact ground configuration
`<k> start </k>`, `<program> solutionModule </program>`, the listed input, and
`<result> 0 </result>`. Each such state is realizable. The postcondition requires
`<k> done </k>` and the listed final result:

| Claim | Exact input | Required result | Submitted Python | Canonical Python |
|---:|---|---:|---:|---:|
| 1 | `"Hello world"` | 0 | 0 | 0 |
| 2 | prompt's sky/weather example | 1 | 1 | 1 |
| 3 | `"I am bored. I am still bored! Are you? I think so."` | 3 | 3 | 3 |
| 4 | `" I am here?You are there!  I agree"` | 2 | 2 | **1** |
| 5 | `"It is cold. Island life! In time? I agree"` | 1 | 1 | 1 |
| 6 | `"... ! ?  . I count!"` | 1 | 1 | 1 |
| 7 | `"\tI tabbed.\nI newline?\rNot me!"` | 2 | 2 | **1** |
| 8 | `"I first! No. I second?"` | `boredSpec(...)`, reducing to 2 | 2 | 2 |

The concrete satisfying states and substitutions are printed by
[`claim_accounting.py`](evidence/claim_accounting.py) in
[`04_adequacy.log`](evidence/04_adequacy.log).

All eight results are genuinely constrained. Claim 1's unchanged
`<result> 0 </result>` constrains both sides to zero; claims 2–7 rewrite zero to
a numeral; claim 8 rewrites zero to a closed function term that reduces to 2.
There is no right-only existential, free result variable, implication, or
tautological postcondition.

### Program identity

The proof does not parse `solution.mpy` at proof time. Instead,
`verification.k` defines nullary function `solutionModule` to a constructor
tree. Static comparison shows that tree is exactly the translated file:
`Module`, the single `FuncDef("is_bored", Params("S"), ...)`, assignment,
normalized/split loop, conditional, increment, and return all agree, including
empty statement lists. Translator regeneration independently established byte
identity of the submitted `.mpy`.

The semantics' `start` rule then matches that exact module and executes its
`BODY` through `evalStmts`; no proof rule substitutes a different body. There
are no helper or loop claims—the ground proofs simply evaluate finite concrete
strings.

Thus real-program pinning is adequate **for the eight ground configurations**.
It does not expand their scope.

### Scope failure

There is no claim with `<input> S:String </input>`, no input variable, and no
universal postcondition. The only `boredSpec` comparison is for one fixed
string, and `boredSpec` itself uses the same `splitDots`, `strip`, and
`startsWith` helpers as execution. It is neither an independent canonical model
nor a universal connection theorem.

The successful proof therefore says nothing about `"I "`, `"\tI agree"`, most
other strings, or the entire intended input domain. Concrete examples cannot
serve as a partial-correctness theorem for arbitrary valid inputs.

**Stage 4 result: fail.** Ground program pinning and result constraint pass, but
the theorem is materially under-scoped and two submitted ground expectations
already contradict the canonical implementation.

## 5. Rule-by-rule static soundness review

The complete numbered sources and mechanical counts are in
[`05_static_inventory.log`](evidence/05_static_inventory.log).

### Syntax, configuration, attributes, and construct coverage

Local syntax declarations enumerate:

- AST/container syntax: `Module`, `Params`, `Stmts`, and `Exprs`;
- every statement constructor used: `FuncDef`, `Assign`, `AugAssign`, `For`,
  `If`, and `Return`;
- every expression constructor used: `Name`, `Int`, `Str`, `Attribute`, and
  `Call`;
- semantic data: `vStr`, `vInt`, `vBool`, `vList`, `nil`, `cons`, `state`,
  `normal`, and `returned`;
- control tokens `start` and `done`;
- the 27 semantic function symbols listed below and four verification function
  symbols (`solutionModule`, `boredSpec`, `countBored`, `boolInt`).

The configuration has exactly the state needed by this subset: `<k>`,
`<program>`, `<input>`, and `<result>` (plus K's compiler-generated counter).
There is no modeled heap, allocation, I/O, exception, or mutable object state.
The target program requires none.

There are 31 `[function]` productions across the two files. There are no local
`[total]`, `[functional]`, `[simplification]`, or `[concrete]` attributes, no
opaque symbols, and no explicit priority rules. The sole special priority is
`[owise]` on `whiteSpace(_) => false`.

Construct-to-rule mapping is complete for the submitted `.mpy`:

| Used construct | Declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k` 6–16; entry rule 51–54 |
| statement list and assignment | 8, 64–77 |
| `For` | 14, 78–79, 88–94 |
| `If` | 15, 80–86 |
| `Return` | 16, 71, 82, 93 |
| `Name`, `Int`, `Str` | 18–20, 97–108, 116–118 |
| `Attribute`/`Call` for four string methods | 21–22, 119–132 |
| `.replace`, `.split`, `.strip`, `.startswith` | 128–201 |

Declarations not given standalone evaluators are still covered in their actual
context: top-level `FuncDef` is consumed by `start`, and `Attribute` is consumed
inside the exact method-call patterns. Minimal omission of unused Python forms
is acceptable in generated-semantics mode.

### Exhaustive semantic rule inventory (79 rules)

| Source | Rules (count) | Classification and decision |
|---|---|---|
| 51–54 | entry `start` (1) | Ordinary semantic rule. Reads exact function name, parameter, body, and input; preserves program/input; writes control/result. For the isolated pure entry point, this is a faithful invocation harness, not an oracle. |
| 57–61 | `runFunction`, `resultOf` (2) | Definitional big-step entry/return rules. Correct on the used domain, where the body returns `vInt`. |
| 68–72 | `evalStmts`, `evalRest` (4) | Empty/nonempty sequencing and early-return propagation. Patterns are disjoint and faithfully preserve control. |
| 74–82 | five `evalStmt` forms (5) | Correct for the exact count assignment, integer increment, string iteration, Boolean conditional, and return forms. Unsupported statement shapes remain visibly stuck. |
| 85–86 | `evalBranch` (2) | True/false guards are disjoint and exhaustive for `Bool`. |
| 90–94 | `evalFor`, `evalForRest` (4) | Empty/nonempty value-list iteration and return propagation. Each iteration updates `sentence`, executes the body, then recurs on a shorter list. |
| 98–108 | lookup, setters, getter (6) | Exact rules for `S`, `count`, and `sentence`; setters preserve the other state components. No overlap among lookup names. |
| 116–139 | expression rules (7), method adapters (4), coercions (3), total 14 | Method names/arities are disjoint. All actual subexpressions are pure, so nested functional evaluation does not change observable Python evaluation order. Adapters preserve the fixed string/int/bool/list values. |
| 144–149 | `splitDots`/`splitDotsAt` (3) | `-1` and `I >= 0` branches are disjoint; recursion removes the first dot and matches Python `split(".")` on tested boundaries. Reachable empty slices rely on backend behavior outside the documented `substrString` index precondition, so portability/definedness is a concern, but no false split result was observed. |
| 152–181 | 29 true `whiteSpace` equations plus one `owise` false equation (30) | The 29 literals exactly equal CPython 3.10's `str.isspace()` set; guards are disjoint under `owise`. The equations on whole strings are mathematically sound. [`05_whitespace.log`](evidence/05_whitespace.log) records the exhaustive set comparison. Their composition with byte slicing is unsound, as described next. |
| 186–196 | `strip`, three `stripLeft`, three `stripRight` rules (7) | **Materially unsound as Python `str.strip` semantics.** The rules assume indices `0..1` remove one Python character, but K's active string backend indexes UTF-8 bytes. Concrete false-result witnesses are below. Base and generic guarded rules also overlap syntactically at `""` and evaluate partial substring terms; this produced the fresh LLVM crash. |
| 199–201 | `startsWith` (1) | Correct for the program's fixed ASCII prefix on observed Haskell executions, but uses non-short-circuiting `andBool` with a potentially invalid substring when `S` is shorter than the prefix. This is a definedness gap, not a separate unsoundness allegation because no false result witness was found for this rule. |

The 27 semantic function symbols accounted for above are:
`runFunction`, `resultOf`, `evalStmts`, `evalStmt`, `evalRest`, `evalBranch`,
`evalFor`, `evalForRest`, `lookup`, `setCount`, `setSentence`, `getCount`,
`eval`, `replaceValue`, `splitValue`, `stripValue`, `startswithValue`, `asInt`,
`asBool`, `asValues`, `splitDots`, `splitDotsAt`, `whiteSpace`, `strip`,
`stripLeft`, `stripRight`, and `startsWith`.

### Concrete false-conclusion witnesses for the strip rules

The installed K documentation says only `andThenBool` is reliably
short-circuiting and documents `substrString` only for valid `start < end`
ranges. More importantly, the reviewer-built
[`string-probe.k`](evidence/string-probe.k) establishes the active
representation:

```text
Probe("AI"):       length 2, first "A",    rest "I"
Probe("\u00a0I"): length 3, first "\xc2", rest "\xa0I"
Probe("\u2003I"): length 4, first "\xe2", rest "\x80\x83I"
```

See [`05_string_probe_corrected.log`](evidence/05_string_probe_corrected.log).
Thus line 190's non-whitespace branch can return a string beginning with a
Python whitespace character because it tests only the first UTF-8 byte; line
195 has the analogous trailing-byte problem.

[`unicode_semantics_witness.py`](evidence/unicode_semantics_witness.py) supplies
observable program-level witnesses:

| Input | Fresh K | Submitted Python | Canonical Python | False semantic effect |
|---|---:|---:|---:|---|
| `"No.\u00a0I agree"` | 0 | 1 | 1 | `stripLeft` fails to remove U+00A0 |
| `"No.\u2003I agree"` | 0 | 1 | 1 | `stripLeft` fails to remove U+2003 |
| `"I \u00a0"` | 1 | 0 | 1 | `stripRight` fails to remove U+00A0 and the preceding ASCII space |

The same leading failure was reproduced for U+0085, U+1680, and U+3000; ASCII
tab is a passing control. The latest run reports six K-versus-submitted
mismatches in seven cases:
[`05_unicode_witness_v2.log`](evidence/05_unicode_witness_v2.log).
An aggregate test separately produced K result 10 versus submitted-Python
result 29 across all 29 whitespace characters.

These are concrete false conclusions on the intended string domain, not merely
missing evidence. They make the generated semantics materially unsound as a
model of the real submitted Python.

### Exhaustive verification-rule inventory (6 rules)

| Source | Rule | Classification and decision |
|---|---|---|
| `verification.k` 10–32 | `solutionModule` | Definitional nullary summary of the exact submitted AST. It does not replace body execution. Sound and result-sensitive for this artifact. |
| 39–40 | `boredSpec` | Definitional summary using the same string helpers as execution. It terminates on concrete finite strings but is not an independent contract model and inherits the Unicode-strip defect. |
| 41–43 | two `countBored` rules | Disjoint empty/`vStr`-cons recursion; descends on the list. Sound on lists produced by `splitDots`; deliberately partial on lists containing other `Value` variants. |
| 44–45 | two `boolInt` rules | Disjoint and exhaustive over `Bool`; mathematically sound. |

There are no operational proof bridges, simplification lemmas, loop claims,
priority claims, or opaque result symbols in `verification.k`. The key issue is
not a hidden oracle: it is that the only purported contract model shares the
execution helpers, is ground-used once, and the underlying generated strip
semantics has witnessed false behavior.

**Stage 5 result: fail.** Most rules faithfully cover the small submitted
subset, but `stripLeft`/`stripRight` are materially unsound for reachable valid
inputs, with the required false-result witnesses.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate negative test was
trusted. The audit created
[`spec-vacuity.k`](evidence/spec-vacuity.k), changing the result-constraining
obligation for the satisfiable input `"Hello world"` from 0 to 1. Both trusted
canonical and submitted Python return 0 on that input.

The mutation was validated in two separate steps:

```text
kprove spec-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY --dry-run
# exit 0

kprove spec-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY
# exit 1, WarnStuckClaimState
```

The residual is the fully executed `<k> done </k>` configuration with
`<result> 0 </result>`, which cannot unify with the mutated destination result
1. This is the expected unmet result obligation, not a parse error, timeout,
missing import, or unrelated crash. Full output is in
[`06_nonvacuity.log`](evidence/06_nonvacuity.log).

**Stage 6 result: pass for non-vacuity.** The ground claims discriminate a false
result. This does not enlarge their scope or validate the semantics.

## 7. Proven versus assumed accounting

### Precisely what the successful reachability proof establishes

Conditional on the candidate's K theory and the fresh K toolchain, each of the
eight exact initial ground configurations in `spec.k` reaches `done` with
results:

```text
0, 1, 3, 2, 1, 1, 2, 2
```

The eighth `2` is expressed through the closed term
`boredSpec("I first! No. I second?")`. The proof executes the exact submitted
constructor body. The false-result mutation shows these ground results are not
vacuous.

The proof does **not** establish:

- correctness for arbitrary `S:String`;
- equivalence of the submitted Python to `/reference/canonical.py`;
- equivalence of the generated K semantics to Python on all valid strings;
- that `boredSpec` expresses the natural-language/canonical contract;
- any universal connection theorem for `splitDots`, `strip`, or `startsWith`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted CPython translator `/reference/py2mpy.py` | identity of `solution.mpy` | Acceptable trusted input; byte identity was independently re-established. |
| Manual `solutionModule` constructor alias | all eight K claims | Acceptable for these ground claims after exact static comparison, but it is a syntactic pin, not a theorem about Python behavior. |
| K v7.1.293 compiler, parser, Haskell prover/backend | all reconstructed builds and proofs | Ordinary machine-checking trust boundary. Fresh builds avoid candidate caches. |
| K `Int`/`Bool` arithmetic and equality | counter, guards, results | Acceptable low-level primitives for unbounded Python integer behavior used here. |
| K string primitives `replaceAll`, `findString`, `substrString`, `lengthString`, `==String` | all string execution and `boredSpec` | Materially concerning. Finite ASCII tests support part of the bridge, but byte indexing plus invalid slice boundaries cause witnessed Python divergence and an LLVM crash. |
| Candidate `whiteSpace`, `strip`, `splitDots`, `startsWith` helpers | execution and `boredSpec` | Program-derived, not external primitives. `whiteSpace`'s table is exact, but `strip` composition is refuted by concrete witnesses. No universal connection theorem exists. |
| `boredSpec` as “contract-level model” | claim 8 only | Illegitimate as evidence for the task contract: it shares semantic helpers, is used only on one ground string, and does not model the trusted canonical boundary behavior. |
| Candidate's 10,000 random comparison | generation report only | Finite and self-referential: its oracle repeats `strip().startswith`. It cannot bridge to the trusted canonical or prove any K theorem. |
| Reviewer canonical differential | source-to-intent bridge | Reproducible finite evidence that refutes, rather than proves, equivalence: 119 mismatches in 9,709 cases. |
| Reviewer K/Python concrete suites | semantics bridge | Finite evidence only. The 13-case ASCII suite passes against submitted Python; Unicode witnesses refute the universal bridge. |

There are no opaque or fresh result-bearing symbols to account for. There are
also no proof-local operational bridges or simplification rules. The informal
arguments that remain—AST-alias identity and rule correspondence—cannot repair
the absent universal claim, the canonical counterexamples, or the witnessed
semantic false conclusions.

### Decision

Fresh `#Top` reconstruction and a passing non-vacuity mutation are real but
narrow facts. Under the required decision boundary, the candidate must fail
because it proves only eight ground instances rather than the task-wide
property, the submitted program materially diverges from the trusted canonical
implementation, and the generated semantics is materially unsound on reachable
valid string inputs.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
