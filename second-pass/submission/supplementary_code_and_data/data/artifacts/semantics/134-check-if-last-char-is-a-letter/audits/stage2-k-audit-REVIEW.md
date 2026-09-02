# Independent adversarial review

Problem: `134-check-if-last-char-is-a-letter`  
Condition: `semantics`  
Rendered semantics mode: `SUPPLIED_SEMANTICS`

The candidate's six K claims reconstruct successfully and are non-vacuous, but
they are not a legitimate proof of the real generated Python program over the
HumanEval source-contract domain. The generated Python calls Unicode-aware
`str.isalpha()`. The supplied semantics models that call with the ASCII-only
predicate `isAlphaC`, and the trusted canonical implementation likewise admits
only ASCII `a` through `z`. A concrete false-conclusion witness is `"é"`:

- `/candidate/solution.py` returns `True`;
- `/reference/canonical.py` returns `False`; and
- the reconstructed K proof closes with `#Top` for code point `233` returning
  `false`.

Thus the proof establishes a theorem about the supplied ASCII code-sequence
model, not partial correctness of the real submitted Python program. This is a
material language/domain gap and maps to `FAIL / NOT_LEGIT` under the benchmark
decision boundary.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, and maps all
launcher mounts through `container_paths`. I treated the host provenance paths
as metadata and inspected only the mounted container paths.

Integrity findings:

- `/audit-campaign-lock.json` is a regular readable file. Its parsed object is
  structurally identical to `audit_input["audit_campaign"]`, and its SHA-256 is
  the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are present, readable, and
  nonsymlinked: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, the structured JSONL trace, and the present `usage.json`.
  Historical `runtime-metrics.json` is not required for this legacy layout.
- Recorded file hashes for the campaign lock, run/task/result manifests,
  invocation, metrics, usage, prompt, Codex output/last message, trace file,
  canonical, trusted prompt, and translator all match independent SHA-256
  calculations.
- All 181 structured-trace lines parse as JSON. The 10,318-line Codex log and
  all other required generation records were read and summarized. Their
  `KPROVE_PASSED` marker is only an untrusted generation claim.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The required trusted `/reference/reference-semantics` mount is present.
  `diff -qr --no-dereference` finds no missing, additional, changed, or
  mistyped entry in `/candidate/reference-semantics`. No symlink exists
  anywhere in the candidate, reference, or generation-evidence trees.
- Every candidate file was independently hashed. No launcher-owned mount or
  required provenance record is absent or unreadable, so there is no audit
  infrastructure breach.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log` — command exit 0,
  `STAGE1_INTEGRITY_OK`
- `evidence/generation_record_summary.py`
- `evidence/generation_record_summary.log` — command exit 0

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires a function on a Python string that returns true
exactly when the final character is alphabetic and is not part of a
space-delimited word. The trusted canonical makes the intended predicate
precise:

1. split on the literal space;
2. take the last piece;
3. require that piece to have length one; and
4. require its lowercased character code to be in ASCII `97..122`.

Equivalently, the canonical returns true precisely when the string is one ASCII
letter, or when it ends in an ASCII letter whose immediately preceding
character is a space. Empty strings, trailing spaces, nonletters, and
non-ASCII letters return false.

### Translation identity

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py
```

created `solution.regenerated.mpy`. It is byte-identical to the submitted
`solution.mpy`; both have SHA-256
`9e03fdeff3da93d08bca16e915284912d738d1557badd000f682a8c690d61395`.
The translator and comparison both exited 0. See
`evidence/translator_regeneration.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical and
the generated candidate. It exercises:

- all four documented examples;
- empty, one-character, two-character, spacing, letter, digit, and punctuation
  branch boundaries;
- every string through length four over the branch-focused alphabet
  `' aA0!?éβ'`; and
- 1,000 fixed-seed generated strings up to length 24.

Exact command: `python3 /audit-output/evidence/differential_test.py`.
It tested 5,577 unique inputs, found 163 mismatches, and exited 1 as designed
when mismatches exist. Representative counterexamples are:

```text
input='é'  canonical=False  candidate=True
input='β'  canonical=False  candidate=True
input=' é' canonical=False  candidate=True
input='a β' canonical=False candidate=True
```

All documented and ASCII branch cases agree; the divergence is specifically
the generated use of Unicode-aware `str.isalpha()` versus the canonical ASCII
test. Complete bounded output is in `evidence/differential_test.log`.

This is a material divergence on the unrestricted Python `str` domain. The
prompt contains no ASCII-only precondition.

Stage 2 result: **FAIL (material program/canonical divergence)**.

## 3. Clean proof reconstruction

I copied candidate source artifacts to `/tmp/audit-work/candidate` and created
new output definitions named `audit-runtime-kompiled` and
`audit-verification-kompiled`. No candidate-built definition or cache was
reused. The available toolchain is K `v7.1.293`; see
`evidence/tool_versions.log`.

Fresh build and execution commands:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun concrete_tests.mpy --definition audit-runtime-kompiled --output pretty

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

All three exited 0. The concrete run ended with `.K`, `NoExc`, and exit code
zero. Logs are `evidence/llvm_kompile.log`,
`evidence/concrete_krun.log`, and `evidence/haskell_kompile.log`.

To avoid trusting a single aggregate proof run, I copied each submitted claim
unchanged into a separate module in `evidence/positive-claims.k` and ran:

```text
kprove positive-claims.k --definition audit-verification-kompiled \
  --spec-module <MODULE>
```

| Claim module | Result | Evidence |
|---|---:|---|
| `SPEC-EMPTY` | exit 0, `#Top` | `evidence/kprove_spec_empty.log` |
| `SPEC-ONE-ALPHA` | exit 0, `#Top` | `evidence/kprove_spec_one_alpha.log` |
| `SPEC-ONE-NONALPHA` | exit 0, `#Top` | `evidence/kprove_spec_one_nonalpha.log` |
| `SPEC-LONG-TRUE` | exit 0, `#Top` | `evidence/kprove_spec_long_true.log` |
| `SPEC-LONG-LAST-NONALPHA` | exit 0, `#Top` | `evidence/kprove_spec_long_last_nonalpha.log` |
| `SPEC-LONG-PREV-NOT-SPACE` | exit 0, `#Top` | `evidence/kprove_spec_long_prev_not_space.log` |

The positive target-proof gate therefore reconstructs successfully. This says
only that the claims close under the supplied theory and proof-local rules; it
does not repair the real-program mismatch found in Stage 2.

Stage 3 result: **PASS (formal closure reconstructed)**.

## 4. Adequacy and real-program pinning

### Plain-language claims

The six formal claims partition constructor-form `IntSeq` strings as follows:

1. empty returns `false`;
2. length one with `isAlphaC(C)` returns `true`;
3. length one with `notBool isAlphaC(C)` returns `false`;
4. length at least two, ASCII-alpha last code, and penultimate code `32`
   returns `true`;
5. length at least two with non-ASCII-alpha/nonalpha last code returns `false`;
6. length at least two with ASCII-alpha last code and penultimate code not
   `32` returns `false`.

For long strings,
`seqConcat(PREFIX, iCons(PREV, iCons(LAST, .IntSeq)))` represents an arbitrary
prefix followed by its last two codes. `isLen(PREFIX) >=Int 0` holds for every
finite constructor sequence, so it does not bound the source length. The
alpha/nonalpha and space/nonspace cases are disjoint and exhaustive under the
supplied `isAlphaC`.

Each RHS is a concrete boolean. No result variable is free, no implication
weakens equivalence, and the complete initial/final cells constrain normal
return with an empty heap and stack, restored environment, `NoExc`, and exit
code zero.

### Satisfiability

`evidence/witness_comparison.py` exhibits one ground witness for every entry
precondition:

| Claim | Witness | Claimed/canonical/candidate |
|---|---|---|
| empty | `""` | `False` |
| one alpha | `"a"` | `True` |
| one nonalpha | `"7"` | `False` |
| long true | `" a"` | `True` |
| long last nonalpha | `" !"` | `False` |
| long previous not space | `"aa"` | `False` |

The script exited 0; see `evidence/witness_comparison.log`.

### Constructor-level program identity

The entry rule does not return a summary oracle. It constructs a
`closureVal` and sends it through the fixed call, frame, branch, subscript,
method, and return rules.

`evidence/constructor_pinning.py` parses balanced constructors from the trusted
regeneration and the proof adapter. It verifies:

- function name `check_if_last_char_is_a_letter`;
- translated parameter `Params("txt")` versus closure parameter `"txt"`;
- lexical scope `0`; and
- exact body-constructor identity, allowing only whitespace and the parser's
  equivalent explicit `.Exprs`/`.Stmts` spelling of empty lists.

The comparison exited 0 with `constructor_body_identity=true`; see
`evidence/constructor_pinning.log`.

The adapter omits execution of the module-level `FuncDef`, so it does not leave
the function-name binding in module scope. The supplied `FuncDef` rule would
bind exactly the compared capture-free closure at scope `0`. The body is
nonrecursive and never reads its own function name, making that omitted binding
inert for the return value proved here. It is nevertheless an observable-state
and artifact-maintenance limitation, not evidence that the module itself was
executed.

### Body sensitivity

As a separate operational-sensitivity test, I changed the embedded body's
final comparison from `" "` to `"x"` in
`evidence/verification-body-mut.k`. The mutated definition compiled with exit
0. Re-running the original long-true obligation failed with
`WarnStuckClaimState`, residual `<k> false`, and exit 1. The ground witness is
`PREFIX=.IntSeq, PREV=32, LAST=97`, i.e. `" a"`. See
`evidence/body_sensitivity_kompile.log` and
`evidence/body_sensitivity_kprove.log`.

The claim is therefore sensitive to the program body actually embedded in the
entry term.

### Adequacy failure

Mechanical body identity also exposes the fatal mismatch: the exact body calls
real Python's Unicode-aware `isalpha`, while K interprets the same constructor
with ASCII-only `isAlphaC`. The proof pins the submitted syntax but not its real
Python behavior on the source domain.

Stage 4 result: **FAIL (pinned syntax, inadequate Python operation model)**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` scans `reference-semantics/semantics.k`, all 23
supplied helper K files, and `verification.k`. The line-addressed inventory is
`evidence/k_rule_inventory.tsv`; generation exited 0. It contains 933
declarations:

- 695 supplied ordinary semantic rules;
- 1 supplied configuration;
- 5 supplied contexts;
- 82 other supplied syntax declarations;
- 120 supplied function declarations;
- 25 supplied opaque/external function declarations, including every
  `symbol(...)`/`no-evaluators` declaration;
- 1 proof-local entry syntax declaration;
- 1 proof-local entry rule; and
- 3 proof-local simplification rules.

The inventory records complete collapsed statements and attributes, including
every `total`, `functional` if present, `priority`, `owise`, `concrete`,
`simplification`, `symbol`, and `no-evaluators` occurrence. It therefore also
enumerates priority and overlap candidates rather than relying on candidate
prose.

All supplied entries are launcher-trusted fixed-semantics entries, not
candidate-authored proof extensions. Unused baseline rules do not contribute
to these claims; their meaning remains part of the named supplied-semantics
trust boundary. The 25 opaque symbols occur in float, sort, and MD5 support and
are unreachable from this program's constructor/rule slice. None can influence
the tested branch, returned boolean, state, exception, or postcondition.

`evidence/used_construct_map.md` maps every constructor used by
`solution.mpy` to declarations and rules for module/function binding, lexical
lookup, left-to-right call evaluation, frame allocation and cleanup, `If`,
early `Return`, literals, unary negation/minus, negative indexing, attribute
and method dispatch, `len`, `isalpha`, and comparisons. Relevant state cells
and control effects are preserved; out-of-bounds indexing is unreachable after
the preceding length branches.

### Proof-local rules K0929-K0933

**K0929-K0930 — `#checkIfLastChar`.** This is an entry adapter, not a
result-bearing abstraction. Its complete RHS is a real `Call` of the exact
closure body with argument `V`. It does not fabricate a boolean, skip any
body operation, introduce abrupt return, or use an opaque value. Fixed call
semantics allocates a temporary frame, binds `txt`, executes the body, and pops
the frame while restoring `<env>`, `<scopeLoc>`, `<stack>`, and `<ret>`.
Constructor comparison and body sensitivity are recorded in Stage 4.

**K0931 — suffix length.**

```text
isLen(seqConcat(P,[A,B])) => isLen(P) + 2
```

For every finite constructor `IntSeq`, this follows by induction from
`seqConcat(.IntSeq,T) => T`,
`seqConcat(iCons(I,S),T) => iCons(I,seqConcat(S,T))`, and the two `isLen`
equations. Ground overlaps reduce to identical integers, and recursion strictly
descends through `P`.

**K0932-K0933 — suffix indexing.** For every finite constructor `IntSeq`, the
same induction plus `intSeqAt([C,...],0) => C` and positive-index decrement
proves that indices `isLen(P)` and `isLen(P)+1` select `A` and `B`.
Ground overlaps with fixed rules agree, the two rules target different valid
indices, and neither changes control or state.

I also attempted bridge-free universal K connection claims using only
`BASELINE-VERIFICATION`; see
`evidence/baseline-verification.k` and
`evidence/lemma-connection-specs.k`. The baseline definition compiled, but all
three claims exited 1 because the backend left abstract `P:IntSeq` unsplit and
reported an implication/definedness residual. Logs:

- `evidence/lemma_len_connection.log`;
- `evidence/lemma_at_first_connection.log`;
- `evidence/lemma_at_second_connection.log`.

That is not a false-rule witness: the equations are valid on the finite
constructor sequences denoting program strings. It is a narrower universal
machine-check evidence gap, so I do **not** label these three rules unsound.
They are an informal-induction trust boundary.

No proof-local function, `total` or `functional` declaration, opaque symbol,
priority rule, task-answer oracle, unconstrained fresh value, or operational
return shortcut exists.

### Material fixed-semantics mismatch and false witness

The relevant supplied rules are:

```text
applyMethod(str(CS), "isalpha", .Vals)
  => notBool (CS ==K .IntSeq) andBool allAlpha(CS)

isAlphaC(C) => (65 <= C <= 90) or (97 <= C <= 122)
allAlpha(iCons(C,S)) => isAlphaC(C) andBool allAlpha(S)
```

These rules are coherent as an ASCII sequence model, but they do not follow
real Python `str.isalpha()` on the intended unrestricted string domain.
Concrete false-conclusion witness:

```text
input value: str(iCons(233, .IntSeq))  // Python "é"
K conclusion: false
real generated Python conclusion: True
```

`evidence/unicode-witness-spec.k` independently proves the K conclusion with
exit 0 and `#Top`; see `evidence/unicode_witness_kprove.log`.
`evidence/unicode_witness_python.log` records the actual submitted Python
result `'é' True`, exit 0. The trusted canonical result is `False`, also shown
in the differential evidence.

This is the required concrete false-conclusion witness. It is not an unused or
exception-only difference: the one-character nonalpha claim directly proves
the wrong result for the real submitted program.

Stage 5 result: **FAIL (material used-operation semantics mismatch)**.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was
trusted.

I created `evidence/spec-vacuity-fresh.k`, changing the empty-string result
obligation from `false` to `true`. Its precondition is concretely satisfied by
`""`, for which both Python implementations return `False`.

Commands and outcomes:

```text
kprove spec-vacuity-fresh.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-FRESH --dry-run
# exit 0

kprove spec-vacuity-fresh.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-FRESH
# exit 1, WarnStuckClaimState, residual <k> false
```

The first command establishes that the mutation parses/builds. The second
fails for the expected unmet result, not a parser error, missing import,
timeout, or unrelated crash. See `evidence/fresh_mutation_dry_run.log` and
`evidence/fresh_mutation_kprove.log`.

Stage 6 result: **PASS (proof is result-constraining and non-vacuous)**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied K definition and the four proof-local rules, the
six claims establish partial correctness of the directly constructed closure
over finite constructor code sequences:

- empty returns false;
- a one-code string returns the ASCII `isAlphaC` classification; and
- a longer string returns true exactly when its final code is an ASCII letter
  and its penultimate code is `32`.

The proof executes the submitted constructor body and constrains a concrete
boolean result. It is universal in prefix length; it is not finite unrolling or
example-only proof.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted `py2mpy.py` transliteration | Program-term identity | Acceptable launcher trust boundary; byte regeneration was independently checked. It does not validate Python/K semantic equivalence. |
| Supplied K core, cells, call/frame, branches, returns, integer/string indexing, and builtins | Control, state, returned value | Required named fixed-semantics boundary. The used slice is operationally complete for the submitted constructors. |
| Supplied `isalpha`/`isAlphaC` equations | Branch and final result | **Illegitimate for the real submitted Python program on Unicode inputs.** The U+00E9 witness demonstrates the wrong result. |
| Direct-closure entry adapter | Binding, body, lexical environment | Mechanically pins name/parameter/body and scope; safe for this nonrecursive return property. It omits the persistent module function binding, so it is not a theorem about complete module poststate. |
| Three proof-local suffix simplifications | Symbolic length and final-two indexing | Mathematically valid by induction on finite constructor sequences; no false witness or conflicting overlap found. Universal bridge-free `kprove` evidence is absent, so this remains an informal-induction limitation. |
| 25 supplied opaque/external symbols | Potential values in unrelated language features | Unreachable from this program and all six claims; no dependency on a float, sort, or MD5 oracle. |
| K builtin mathematics and SMT reasoning | Integer inequalities and boolean partitions | Ordinary low-level proof trust boundary. |
| Termination | Whether a result is reached | The theorem is partial correctness. Concrete runs terminate, but differential/concrete tests are finite evidence, not a termination theorem. |
| Differential and witness tests | Python/canonical adequacy bridge | Reproducible finite evidence only. Here they expose a counterexample; they are not used as a substitute for K proof. |

### Gate and verdict accounting

- Fresh formal reconstruction: pass.
- Result constraint/non-vacuity: pass.
- Proof-local body execution and constructor pinning: pass for the return
  property, with a module-binding observation.
- Proof-local simplification validation: mathematically supported, but lacks
  bridge-free universal machine closure; evidence limitation only.
- Real-program/source-contract adequacy: fail. The generated Python diverges
  from the canonical, and the K model proves a result that is false of that
  Python program on `"é"`.

The formal artifact is therefore at best sound-but-limited to an ASCII
interpretation. The benchmark explicitly maps material narrowing or
mis-modeling of the HumanEval source-contract domain to `FAIL / NOT_LEGIT`,
not to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
