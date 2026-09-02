# Independent adversarial review: 113-odd-count

## Decision summary

The source-only reconstruction succeeds mechanically, and I found no false
local semantics or verification equation on the modeled ASCII-digit domain.
The submitted `solution.mpy` is pinned exactly to the program term used in the
entry claims. All ten submitted claims individually close with a fresh Haskell
definition, and a fresh false-result mutation is rejected for the expected
result mismatch.

Those facts do **not** amount to a proof of the requested program contract. The
only end-to-end claims cover the empty list and the two prompt examples. There
is no entry claim quantified over an arbitrary input list (or even an arbitrary
single digit string), no inner-loop invariant connecting the accumulated count
to `oddCount`, and no outer-loop inductive claim connecting all input elements
to `expected`. The remaining claims are local one-step equations and formatting
facts. Thus the reconstructed proof establishes several true finite and local
facts about the real program but omits the material universal theorem.

This is a missing-proof/adequacy failure, not a claim that a particular local K
rule is unsound. In accordance with the decision boundary, the candidate is not
a legitimate partial-correctness proof of the problem.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, as required. I did not search for or use a hidden semantics.
There is no trusted-mount contradiction and therefore no infrastructure breach.
The check and trusted/candidate hashes are recorded in
`evidence/stage1/integrity.log`.

### Trusted-file comparison

The candidate copies of the prompt and translator are regular files and are
byte-identical to the trusted mounts:

| Artifact | SHA-256 | Comparison |
|---|---|---|
| `/candidate/prompt.py` and `/reference/prompt.py` | `2e684f86c7166a064ce81c06ad2a26b4d974f41c507e6e65e4dccd32f2345bcd` | identical |
| `/candidate/py2mpy.py` and `/reference/py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

Exact `cmp`, hash commands, outputs, and statuses are in
`evidence/stage1/provenance-comparison.log`.

The required core source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`.
The requested generation evidence is also present: `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, and one structured JSONL
trace. `prove.sh` and `mutation.k` are present as additional source/evidence
artifacts. No symlink exists anywhere under `/candidate`; no required source
artifact is missing, changed relative to a trusted counterpart, mistyped, or
symlinked.

There are extra candidate-built products: `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, and `kore-exec.tar.gz`. They are not
integrity failures in generated-semantics mode, but they were excluded from all
reconstruction and execution. No `PROOF.md` or `spec-vacuity.k` is present; the
former is not needed to reconstruct the submitted claims, and the latter was
replaced by a reviewer-authored mutation as required.

### Untrusted generation claims

`run-input.json` identifies the bare condition and hashes that agree with the
trusted prompt and translator. `metrics.json` claims generation exit 0.
`codex-last.txt`, the raw output log, and the structured trace claim that the
candidate harness compiled, rejected its mutation, and printed `#Top`. These
were treated only as claims. The raw log also contains many failed intermediate
build and proof attempts, reinforcing why the final candidate cache cannot be
trusted.

Bounded projections are preserved in
`evidence/stage1/untrusted-generation-log-summary.txt` and
`evidence/stage1/untrusted-trace-projection.txt`; the reviewer script is
`evidence/stage1/summarize_trace.py`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a list of digit strings, return a list of the same length. For each input
string, count its odd digits. Insert that decimal count at each of the four
places represented by `i` in:

`the number of odd elements in the string i of the input.`

The intended executable domain used by the prompt, canonical implementation,
candidate, and formal input representation is lists of strings over ASCII
digits `0` through `9`; empty lists and empty strings are included. Behavior for
non-digit or non-ASCII characters is outside the formal model.

`/reference/canonical.py` computes
`sum(int(d) % 2 == 1 for d in arr)` and builds the sentence. The candidate
computes the same count on this domain using `c in "13579"` and constructs the
same sentence. It uses immutable list concatenation instead of `append`; that
algorithmic difference is not observable here.

### Trusted translation

The trusted translator was run on the scratch copy of `solution.py`. The
regenerated file and submitted `solution.mpy` are byte-identical with SHA-256
`aa1e67044660add960f3ecfdfa3921e3a9eb37af61126cd27df92cb8ff5357ae`.
The translator and `cmp` commands both exited 0. See
`evidence/stage2/translator-identity.log`.

### Independent differential test

`evidence/stage2/differential_test.py` independently loads the trusted
`canonical.py` and the scratch candidate `solution.py`. It does not import any
candidate proof equation. It exercised:

- both documented examples;
- the empty list and empty string;
- every individual digit and all-even/all-odd cases;
- count transitions including multi-digit counts;
- every digit string of length zero through three (1,111 strings);
- 250 deterministic generated list inputs containing strings up to length 64.

There were 1,375 total input lists and zero mismatches. The command exited 0.
The exact command/status is in `evidence/stage2/differential-command.log`; all
inputs and both results are in
`evidence/stage2/differential-results.json`.

This is strong finite evidence that the generated Python implementation matches
the canonical implementation on the documented domain. It is not a universal K
proof.

## 3. Clean proof reconstruction

### Isolation and toolchain

Only these source files were copied into `/tmp/audit-work/source`:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`.
Trusted files were copied separately into `/tmp/audit-work/trusted`. No
candidate-compiled directory, cache, KORE definition, interpreter, or trace was
copied into the build path.

The installed toolchain is K `v7.1.293` (build date 2025-10-03). Paths and
version commands are in `evidence/stage3/toolchain.log`.

### Fresh builds

Both definitions were built from source:

| Purpose | Command summary | Exit |
|---|---|---:|
| Concrete semantics | `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/build/semantic-kompiled` | 0 |
| Proof definition | `kompile verification.k --main-module ODD-COUNT-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/build/verification-kompiled` | 0 |

Exact commands and output are in
`evidence/stage3/kompile-semantic-llvm.log` and
`evidence/stage3/kompile-verification-haskell.log`.

### Fresh concrete execution of the generated semantics

`evidence/stage3/run_concrete_cases.sh` ran the submitted translated program
against the fresh LLVM definition. Every run exited 0 and ended with `.K`:

| Case | K result, interpreting `concat`/`number` as their stated denotations | Independent Python result |
|---|---|---|
| `[]` | `pyList(noValues)` | `[]` |
| `[""]` | one `message(0)` value | sentence with four `0` insertions |
| `["1234567"]` | one `message(4)` value | sentence with four `4` insertions |
| `["24680", "13579"]` | `message(0)`, `message(5)` | sentences with `0`, `5` |

Full K configurations are in `evidence/stage3/krun-*.log`. Both Python
implementations were run on the same cases in
`evidence/stage3/python-concrete-results.log`; all comparisons match.

The K results are structural `Text` trees rather than host `String` tokens. The
bridge from `literal`/`concat`/`number` trees to concrete Python strings is
therefore an interpretation boundary, accounted for in Stage 7.

### Fresh positive proofs

Every claim in `spec.k` was selected and run independently with
`--claims ODD-COUNT-SPEC.<label>`. A claim was counted as closed only if the
process exited 0 and the log contained a standalone `#Top`.

| Claim | Exit | `#Top` |
|---|---:|---:|
| `empty-list` | 0 | 1 |
| `prompt-example-one` | 0 | 1 |
| `prompt-example-two` | 0 | 1 |
| `format-all-counts` | 0 | 1 |
| `character-loop-base` | 0 | 1 |
| `even-character-step` | 0 | 1 |
| `odd-character-step` | 0 | 1 |
| `list-loop-base` | 0 | 1 |
| `append-base` | 0 | 1 |
| `append-step` | 0 | 1 |

The runner and summary are
`evidence/stage3/run_positive_claims.sh` and
`evidence/stage3/kprove-positive-summary.log`; each exact command and output is
in its corresponding `evidence/stage3/kprove-<label>.log`.

Seven local claims produce `WarnTrivialClaim`, meaning normalization establishes
them without reachability rewriting. That warning does not invalidate those
true local equations, but it emphasizes that they are not loop invariants or a
universal end-to-end proof.

## 4. Adequacy and real-program pinning

### Entry-claim preconditions and postconditions

There are exactly three program-entry claims. None has an explicit `requires`;
instead, each fixes the entire initial input and fixes `<output>` to `noValue`.

| Claim | Precondition in plain language | Postcondition in plain language |
|---|---|---|
| `empty-list` | Run the submitted `odd_count` program with the empty abstract list. | Computation is consumed and output is the empty list. |
| `prompt-example-one` | Run it on the parity abstraction of `["1234567"]`. | Output is the one-element `expected` list, which normalizes to the sentence using count 4. |
| `prompt-example-two` | Run it on the parity abstraction of `["3", "11111111"]`. | Output is the two-element `expected` list, which normalizes to counts 1 and 8. |

These outputs are result-constraining: none is a fresh variable, tautology, or
one-way implication. Concrete satisfying states and results from both Python
entries are recorded in
`evidence/stage4/entry_witnesses.py` and
`evidence/stage4/entry-witness-results.log`. For example,
`["1234567"]` satisfies the second entry configuration, and both Python
implementations return the exact count-4 sentence.

### Program identity

The entry claims use the `solutionProgram` macro. With the fresh Haskell
definition, I separately expanded:

1. the submitted `/tmp/audit-work/source/solution.mpy`; and
2. `solutionProgram` parsed in `ODD-COUNT-VERIFICATION`.

Their expanded KORE files are byte-identical, both with SHA-256
`4787be8a7794b8e40b20c9994be6b257e2810197052a6ceef3fabaad5ff0931a`.
Commands, statuses, and hashes are in
`evidence/stage4/program-pinning.log`; the two expanded terms are preserved as
`evidence/stage4/submitted-program.expanded.kore` and
`evidence/stage4/proof-program.expanded.kore`.

The semantic entry rule binds the actual `BODY` from that `FuncDef` and passes
it to `execute`. It does not replace the body with `expected`, `oddCount`, or
another oracle. The body-sensitivity experiment in Stage 5 further confirms
this.

### Helper-claim meanings and satisfiability

All helper claims also have satisfiable domains:

- `format-all-counts` says the actual formatting expression, with `count=N`,
  evaluates to structural `message(N)` for every K integer. A ground witness is
  `N=4`.
- `character-loop-base` says an empty character iterator proceeds to its
  continuation. A witness is `REST=.Stmts`, `ENV=emptyEnv`.
- `even-character-step` executes one real loop iteration on an even abstract
  digit and leaves `count` unchanged. A witness is `DS=noDigits`,
  `REST=.Stmts`, and an environment binding `count` to 0.
- `odd-character-step` executes one real odd-digit iteration and adds one to
  the looked-up count. The same ground environment is a witness.
- `list-loop-base` proceeds to the continuation for an empty outer iterator.
- `append-base` and `append-step` state the two ordinary structural-list append
  equations; ground empty-list terms witness both.

The helper transitions match the real `executeFor`/`execute` control flow and
do not introduce abrupt control or discard an admitted continuation.

### Decisive adequacy gap

No claim has a symbolic input list at program entry. In particular, there is no
claim of the form:

`solutionProgram(input-list) => pyList(expected(input-list))`

for all well-formed digit-string lists. The intended input `["2"]`, for
example, is valid and is exercised successfully by differential testing, but it
satisfies none of the three entry claims. The formal theorem set says nothing
end-to-end about that input.

The local claims do not fill this gap:

- the even/odd claims are only one-character operational steps;
- there is no invariant saying a completed inner loop changes `count` by
  `oddCount(DS)`;
- there is no nonempty outer-list step or invariant relating accumulated
  `result` to `expected`;
- `list-loop-base` covers only zero outer iterations;
- `append-*` merely restate list append normalization.

Consequently, the returned value is constrained correctly for three fixed
entries, but the intended result is not constrained for the intended domain.
This is material and cannot be downgraded to thin evidence for an otherwise
universal theorem: the universal theorem is absent.

## 5. Rule-by-rule static soundness review

Numbered source and declaration evidence is preserved in
`evidence/stage5/numbered-sources.log`,
`evidence/stage5/declaration-inventory.log`, and
`evidence/stage5/attribute-and-count-inventory.log`.

### Local syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

| Sort | Local constructors | Use |
|---|---|---|
| `Module`, `Stmts` | `Module(Stmts)`, separator-free statement list | submitted module and all statement sequences |
| `Params` | one `String` parameter | submitted `Params("lst")` |
| `Stmt` | `FuncDef`, `Assign`, `For`, `If`, `Return` | every statement constructor appearing in `solution.mpy` |
| `Expr` | `Name`, `Int`, `Str`, empty/singleton `ListExpr`, `BinOp`, `Compare`, `Call` | every expression constructor in `solution.mpy` |
| `CmpOp` | string operator and right expression | submitted membership comparison |
| `Digit`, `Digits` | even/odd parity and a recursive sequence | abstract valid input characters |
| `Text` | `literal`, `inputDigits`, `oneDigit`, `number`, `concat` | abstract input/output strings |
| `Values`, `Value` | recursive values; no-value, integer, Boolean, string, list | runtime values used by the program |
| `Env` | empty or newest-first `store` | variable state |
| `ExecResult` | `normal`, `returned` | ordinary and return control |

The configuration has exactly the used cells: `<k>` for the module,
`<input>` for the call argument, and `<output>` for the result. Local statement
execution state is passed explicitly as `Env`; no local rule reads or writes a
heap, output stream, allocation counter, or exception cell. That is adequate
for this alias-free program: input strings are immutable and `result + [x]`
creates a fresh abstract list value.

Construct mapping for the submitted program is complete:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| module/function | `Module`, `FuncDef`, `Params` | semantic entry rule executes the bound body |
| assignment/name lookup | `Assign`, `Name`, `Env` | `execute` assignment; `evaluate`/`lookup` |
| empty/singleton list | `ListExpr` | two `evaluate` equations |
| nested `for` | `For` | `execute`, `executeFor`, `afterIteration` |
| conditional membership | `If`, `Compare`, `CmpOp("in",...)` | `executeIf`, `containsValue` |
| integer/string literals | `Int`, `Str` | literal evaluation rules |
| overloaded `+` | `BinOp("+",...)` | integer, string, and list `addValue` cases |
| `str(count)` | `Call(Name("str"),...)` | `builtinStr` |
| return | `Return` | `returned` and `resultValue` |

Missing behavior for unused Python constructs is not a defect in this generated,
minimal semantics.

### Attributes, opaque boundaries, priorities, and overlaps

`semantic.k` declares fourteen `[function]` symbols:
`evaluate`, `lookup`, `addValue`, `containsValue`, `builtinStr`,
`appendValues`, `iterableValues`, `digitValues`, `execute`, `afterBlock`,
`executeFor`, `afterIteration`, `executeIf`, and `resultValue`.
`verification.k` declares four more: `oddCount`, `message`, `expected`, and
`runProgram`.

There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
`[anywhere]`, `[owise]`, `[opaque]`, `strict`, or `seqstrict` attributes, and no
local priority declarations. Therefore no unproved totality, simplifier, or
priority assumption is hidden in the local source. Functions are intentionally
partial outside the actual well-typed construct set and visibly become stuck
there.

The data constructors `inputDigits`, `oneDigit`, `literal`, `number`, and
`concat` have no reduction equations. They form an abstract text denotation,
not an unconstrained fresh result: constructor arguments uniquely retain the
input parity, literal, integer, and concatenation structure. Nevertheless,
interpreting `number(I)` as Python decimal `str(I)` and `concat(A,B)` as Python
string concatenation is a result-bearing external semantic boundary, not a K
connection theorem. It is accounted for as a concern in Stage 7.

All local equation heads are constructor-disjoint except `lookup`. Its
same-name rule and different-name rule are separated by
`X =/=String Y`, so their guards do not overlap. Recursions on `Digits`,
`Values`, and environments structurally descend. No pair of applicable local
rules was found to yield conflicting results.

### Exhaustive `semantic.k` rule decisions

There are 37 local rules. “Sound” below means sound for the submitted program
and the modeled well-typed ASCII-digit input domain; it does not claim a full
Python semantics.

| ID / lines | Rule | Decision |
|---|---|---|
| S1 / 84 | `evaluate(Name(X),ENV) => lookup(X,ENV)` | Sound name-evaluation delegation. |
| S2 / 85 | lookup matching newest binding | Sound shadowing lookup. |
| S3 / 86-87 | lookup skips a different name under `=/=String` | Sound, disjoint from S2, and structurally descending. |
| S4 / 88 | integer literal to `pyInt` | Sound. |
| S5 / 89 | string literal to `pyString(literal(S))` | Sound abstract literal embedding. |
| S6 / 90 | empty list literal | Sound. |
| S7 / 91 | singleton list literal | Sound for the only nonempty list-literal shape used. |
| S8 / 92-93 | `BinOp("+",...)` evaluates operands then calls `addValue` | Sound for pure used expressions; all used overload cases are covered. |
| S9 / 94-95 | membership comparison delegates to `containsValue` | Sound for the single used comparison. |
| S10 / 96-97 | `Call(Name("str"),ARG)` delegates to `builtinStr` | Sound for this program, where `str` is not rebound and arguments are pure. |
| S11 / 99 | integer `addValue` uses `+Int` | Sound ordinary integer addition. |
| S12 / 100 | string `addValue` constructs `concat` | Sound under the stated text denotation. |
| S13 / 101 | list `addValue` calls structural append | Sound for Python list concatenation without observable aliases. |
| S14 / 103 | append empty-left base | Sound list mathematics. |
| S15 / 104 | append recursive step | Sound and structurally descending. |
| S16 / 106 | `builtinStr(pyInt(I)) => pyString(number(I))` | Sound conditional on the explicit decimal-rendering interpretation; not itself a K proof of that primitive. |
| S17 / 108-109 | odd abstract digit is in `"13579"` | Sound for the odd ASCII equivalence class. |
| S18 / 110-111 | even abstract digit is not in `"13579"` | Sound for the even ASCII equivalence class. |
| S19 / 113 | list iteration exposes its values | Sound. |
| S20 / 114 | abstract string iteration calls `digitValues` | Sound for input digit strings under the parity abstraction. |
| S21 / 115 | empty digit sequence to empty values | Sound. |
| S22 / 116-117 | digit sequence to one-character string values | Sound, preserves order, and descends. |
| S23 / 124 | empty statement sequence returns `normal(ENV)` | Sound. |
| S24 / 126-127 | assignment evaluates in old environment and stores newest binding | Sound state and evaluation behavior for used targets. |
| S25 / 129-130 | `If` evaluates condition and delegates with both branches/rest | Sound; continuation is preserved. |
| S26 / 133-134 | true branch executes then continues through `afterBlock` | Sound. |
| S27 / 135-136 | false branch executes then continues through `afterBlock` | Sound and disjoint from S26. |
| S28 / 138 | normal block result resumes `REST` with new environment | Sound state/control propagation. |
| S29 / 139 | returned block result propagates and discards rest | Sound Python return control. |
| S30 / 141-142 | `For` evaluates iterator once and calls `executeFor` | Sound evaluation order for the used immutable iterables. |
| S31 / 144 | empty iterator resumes rest | Sound loop base. |
| S32 / 145-146 | nonempty iterator binds loop variable and executes body | Sound per-iteration binding and order. |
| S33 / 148-149 | normal iteration continues with remaining values and updated environment | Sound state/control propagation. |
| S34 / 150 | return from loop body propagates | Sound abrupt control. |
| S35 / 152 | `Return(E)` evaluates in current environment and discards remaining statements | Sound for the used pure return expression. |
| S36 / 155 | extract value from `returned(V)` | Sound on the terminating function path. |
| S37 / 157-160 | exact `odd_count(lst)` module entry executes bound `BODY` with input and writes result | Sound for the submitted single function; it reads actual `BODY` and does not use a proof oracle. |

No S-rule was labeled unsound, so no false-conclusion witness is asserted for
one. The narrower evidence limitations are the abstract digit/text
interpretation and intentional partiality outside used constructs.

Evaluation order is faithfully observable for this program: assignment and
return evaluate under the pre-update/current environment, iterable evaluation
occurs before looping, iterations preserve order, and statement continuations
are passed explicitly. The K function evaluator may normalize pure subterms
without modeling all Python sequencing, but all submitted expression subterms
are side-effect free, so no differing observable order witness exists here.
Valid inputs avoid type errors and conversion exceptions.

### Exhaustive `verification.k` rule decisions

There are 11 local rules:

| ID / lines | Rule | Class and decision |
|---|---|---|
| V1 / 14-17 | `innerBody` macro | Exact syntactic abbreviation; sound. |
| V2 / 19-51 | `outerBody` macro | Exact syntactic abbreviation; sound. |
| V3 / 53-56 | `functionBody` macro | Exact syntactic abbreviation; sound. |
| V4 / 58-59 | `solutionProgram` macro | Exact module abbreviation; sound and KORE-pinned to `solution.mpy`. |
| V5 / 62 | `oddCount(noDigits)=0` | Truthful recursive-summary base. |
| V6 / 63 | even head contributes zero | Truthful and descending. |
| V7 / 64 | odd head contributes one | Truthful and descending. |
| V8 / 67-82 | `message(N)` structural text tree | Truthful factorization of the submitted formatting AST. |
| V9 / 85 | `expected(noValues)=noValues` | Truthful map base. |
| V10 / 86-87 | `expected` maps a digit string to `message(oddCount(DS))` | Truthful intended mathematical summary and descending on `REST`; partial but not marked total. |
| V11 / 90-91 | `runProgram` invokes `execute` on the bound body | Exact definitional wrapper, not an execution bypass; it is unused by the submitted claims. |

The four macros are syntax expansion, not operational bridges. The expanded
program equality is machine-checked in Stage 4. `oddCount`, `message`, and
`expected` are result-bearing definitional summaries. Their equations are
disjoint, descending, and mathematically truthful under the abstract
interpretation. Crucially, no rule rewrites real `execute` computation to
`expected` or `oddCount`; the program body executes. The problem is that no
universal reachability claim connects the completed execution to those truthful
summaries.

### Body sensitivity

To check that S37 and the proof program are not body-insensitive, I changed the
real body update from `count + 1` to `count + 2`, regenerated its `.mpy` with
the trusted translator, and executed it under the fresh semantics. On
`"1234567"`, both mutated Python and K returned the count-8 structure rather
than count 4. Artifacts and exact output are
`evidence/stage5/body-sensitivity.py`,
`evidence/stage5/body-sensitivity.mpy`, and
`evidence/stage5/body-sensitivity.log`.

This supports real-body execution and rules out a fixed answer shortcut in the
semantic entry rule. It does not supply the absent universal proof.

## 6. Fresh non-vacuity test

I inspected the candidate `mutation.k` only as untrusted evidence and wrote a
fresh mutation, preserved at `evidence/stage6/audit-vacuity.k`.

The fresh claim uses the satisfiable entry input `["1234567"]` but changes the
result-constraining postcondition from count 4 to `message(5)`. This is
demonstrably false: both trusted canonical and generated Python return the
count-4 sentence for that input.

Two separate checks were run:

| Check | Result |
|---|---|
| `kprove ... --dry-run` | exit 0; the mutation parses and builds against the fresh definition |
| actual `kprove ... --output pretty` | exit 1 with `WarnStuckClaimState` |

The residual final configuration explicitly contains four occurrences of
`number(4)`, while the destination requires `message(5)`. The failure is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. Exact commands and outputs are in
`evidence/stage6/mutation-dry-run.log` and
`evidence/stage6/mutation-proof.log`.

The non-vacuity gate therefore passes for the fixed entry harness. It shows
that false outputs for a covered entry are rejected; it cannot extend the
claim's input domain.

## 7. Proven versus assumed accounting

### What the successful reachability proofs actually establish

Under the submitted generated K semantics, the reconstructed `#Top` results
establish exactly:

1. The real translated program returns the empty abstract list on empty input.
2. It returns the specified structural messages for the two prompt examples.
3. The submitted formatting AST evaluates to `message(N)` for every K integer
   `N`.
4. Empty character and outer-list iterators proceed to their continuations.
5. One even-character loop iteration preserves count, and one odd-character
   iteration adds one, with the stated environment/control transitions.
6. The two structural append equations hold.

They do not establish:

1. full-program correctness for an arbitrary list of digit strings;
2. an inner-loop invariant or completed-loop theorem equating count with
   `oddCount`;
3. an outer-loop invariant or step theorem equating the result prefix with
   `expected`;
4. a formal encoder/bisimulation theorem from concrete Python digit strings to
   `Digits`;
5. a formal decoder theorem from structural `Text` to concrete Python strings;
6. total correctness or termination (the requested proof notion is partial
   correctness);
7. behavior on non-digit, non-ASCII, ill-typed, exceptional, or unmodeled
   Python inputs.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, reachability logic | all build, run, and proof results | Acceptable standard toolchain trust boundary; rebuilt independently. |
| K built-in `INT`, `BOOL`, and `STRING` operations, especially `+Int` and string inequality | arithmetic, lookup guards, branching | Acceptable primitive mathematical/runtime boundary. |
| Trusted `/reference/py2mpy.py` | identity of Python source and submitted `.mpy` | Acceptable trusted input; byte identity was checked. |
| Parity abstraction `Digit/Digits` and the informal encoder from ASCII characters | membership, inner iteration, all abstract input claims | Concerning but not shown false on the stated ASCII domain. Concrete/differential evidence supports it; no K connection theorem proves it. |
| `literal`, `concat`, and `number` as exact text/decimal denotations | every formatted result and postcondition | Result-bearing trusted Python-primitive boundary. Plausible and empirically supported, but the same constructors appear in execution and the formal message, so K does not independently prove the concrete-string denotation. |
| Proof-local `oddCount`, `message`, `expected` equations | helper postconditions and fixed example outputs | Audited truthful definitional summaries; no execution-bypassing rule uses them. |
| `runProgram` | none of the ten claims | Unused definitional wrapper; no contribution to closure. |
| Trusted canonical CPython implementation and differential corpus | implementation-to-intent and abstract/concrete confidence | Finite empirical evidence only, never substituted for a K theorem. |
| Informal observation that expressions are pure and the program is alias-insensitive | adequacy of simplified evaluation/immutable lists | Acceptable for this narrow program, but not a reusable Python-semantics theorem. |

No fresh or unconstrained proof oracle controls a branch or result. No local
rule was found that fabricates a false result on the stated domain, and
therefore this review does not manufacture an unsoundness witness. The
candidate instead fails at the more basic theorem-scope boundary.

### Gate accounting and final rationale

| Audit gate | Result | Reason |
|---|---|---|
| Input/provenance integrity | pass | Trusted prompt/translator match; generated-semantics mount boundary is correct. |
| Program fidelity | pass on documented ASCII-digit domain | Byte-identical trusted translation and zero mismatches in 1,375 cases. |
| Clean reconstruction | pass | Fresh builds succeed; all ten actual claims independently print `#Top`. |
| Real-program pinning for those claims | pass | Expanded KORE identity and body-sensitivity evidence. |
| Local-rule soundness on used constructs | pass with explicit abstraction boundaries | Exhaustive inventory found no false local equation on the modeled domain. |
| Fresh non-vacuity | pass | A buildable false count-5 postcondition is rejected with actual count 4. |
| Intended theorem adequacy | fail | No universally quantified end-to-end entry claim or loop invariant proves the contract for arbitrary inputs. |

The abstraction boundaries would merit concern even if a universal theorem
were present, because their concrete Python interpretation is not
machine-connected. They are not the decisive verdict here. The decisive issue
is that the candidate never states or proves the required universal
partial-correctness property. Finite examples, true one-step rules, and
differential testing cannot substitute for that missing claim.

Evidence hashes are recorded in `evidence/stage7/SHA256SUMS`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
