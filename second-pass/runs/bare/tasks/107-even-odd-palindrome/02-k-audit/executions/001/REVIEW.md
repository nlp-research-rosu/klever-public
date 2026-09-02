# Independent adversarial audit: 107-even-odd-palindrome

## Headline

The candidate contains a legitimate, result-constraining proof for the complete
stated input domain `1 <= n <= 1000`. The proof is an exhaustive finite K
execution: it runs the actual submitted MPY program once for every domain value
and permits the final `verified` marker only after each returned tuple has
matched a separate digit-reversal specification.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because two
unguarded arithmetic equations in the generated language definition are not a
faithful model of Python on negative operands. A concrete out-of-scope probe
shows the difference. No negative arithmetic operand or divisor is reachable
from the submitted program on the theorem's positive input domain, so this
over-breadth cannot enable a false conclusion for any admitted input and does
not invalidate the reconstructed proof.

All candidate prose, traces, caches, and earlier outputs were treated only as
untrusted claims. All executable checks used source copies in
`/tmp/audit-work/case107`; no candidate-provided compiled definition was used.
The exact commands, outputs, and exit statuses are in
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` neither exists nor is a symlink. This is the
required mount state, so there is no infrastructure breach and no basis for an
`AUDIT_ERROR`. See `evidence/stage1-integrity.log`.

### Required artifacts

The following required candidate artifacts are present as ordinary files and
are not symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the JSONL generation trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.

No required source artifact is missing, mistyped, or symlinked. There are no
additional helper K source files. The candidate also contains
`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/`; these are
additional generated caches, not trusted source. They were deliberately not
copied into scratch and were never used.

The candidate prompt and translator compare byte-for-byte with their trusted
mounts:

| Artifact | SHA-256 | `cmp` |
|---|---|---|
| trusted and candidate `prompt.py` | `0635c205473d52d0dcb6681641abe4b97606c0f5dbd6b2881179bd386b9f0d64` | exit 0 |
| trusted and candidate `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

`run-input.json` names the correct problem and records the same prompt and
translator hashes. Its `bare`/no-supplied-semantics claim is consistent with
the rendered mode. The instruction-prompt hash cannot be compared because no
trusted `bare.md` is mounted; it is provenance metadata, not a proof input.

The 227-line structured trace parses as JSON on every line. The large text log,
trace, `metrics.json`, `codex-last.txt`, and their claimed earlier `#Top` were
inspected but not relied upon. The final successful integrity run is
`evidence/stage1-integrity.log`; earlier reviewer attempts that encountered the
absence of `jq` are preserved as
`evidence/stage1-integrity-initial.log` and
`evidence/stage1-integrity-rerun1.log` and are not treated as successful
evidence.

**Stage 1 result: pass.**

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt and canonical implementation establish this contract:
given an integer `n` with `1 <= n <= 1000`, return
`(even_count, odd_count)`, where the counts classify by parity all positive
decimal integer palindromes from 1 through `n`, inclusive. Although the prompt
uses the awkward phrase “range(1, n), inclusive,” both examples and the trusted
canonical loop include `n`; that is the interpretation audited here.

Examples are:

- `n = 3` gives `(1, 2)`;
- `n = 12` gives `(4, 6)`.

There is no meaningful “empty” valid input because the input is one positive
integer. The lower and upper boundary cases are `1` and `1000`.

### Candidate algorithm

`/candidate/solution.py` counts:

1. one-digit palindromes directly;
2. two-digit palindromes as `11 * k`, capped at `k = 9`, with parity equal to
   the parity of `k`;
3. three-digit palindromes as `101 * lead + 10 * middle`, ten per completed
   leading digit and a bounded partial count for the current leading digit.

For `n = 1000`, it caps the three-digit leading digit at 9, correctly excluding
1000.

### Trusted regeneration

In scratch, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp -l submitted-solution.mpy regenerated-solution.mpy` also exited
0 with no output. See `evidence/translation-regenerate.log` and
`evidence/translation-identity.log`. The submitted MPY is therefore byte
identical to output from the trusted translator.

### Independent differential test

`evidence/differential_test.py` imports the copied trusted canonical entry point
and candidate entry point independently. It checks the two documented examples,
explicit branch boundaries, 40 seeded generated inputs, and then every integer
in `1..1000`. It also records both outcomes of every candidate branch:
`n < 10`, `pairs > 9`, `n >= 101`, `lead > 9`, `candidate <= n`, and even/odd
`lead`.

Command:

```text
python3 differential_test.py
```

Result: exit 0, 1,000 intended-domain inputs, zero mismatches. Boundary results
include `1 -> (0,1)`, `100 -> (8,10)`, `101 -> (8,11)`,
`999 -> (48,60)`, and `1000 -> (48,60)`. Complete output is in
`evidence/differential-test.log`.

**Stage 2 result: pass.**

## 3. Clean proof reconstruction

The scratch tree was populated only with the trusted prompt, translator, and
canonical source plus the candidate's source artifacts. Candidate
`*-kompiled` directories and caches were excluded. The independently installed
toolchain is K `v7.1.293`; see `evidence/tool-versions.log`.

### Generated semantics build and concrete execution

The fresh concrete build command was:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
```

It exited 0. The compiler emitted deprecation and zero-argument `symbol`
warnings, but no parse, coverage, or backend error. See
`evidence/semantic-kompile.log`.

`evidence/concrete_semantics_test.sh` then ran the submitted MPY with the fresh
definition at inputs
`1, 3, 9, 10, 12, 99, 100, 101, 109, 110, 111, 999, 1000`.
Every K tuple equaled both Python implementations. The script exited 0; its
commands and full configurations are in
`evidence/concrete-semantics-test.log`.

### Proof build and positive claim

The fresh proof build command was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0 (`evidence/verification-kompile.log`). Static enumeration found one
and only one positive target claim in `spec.k`. It was run independently:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

The command exited 0 and printed `#Top`; see
`evidence/positive-proof.log`. This run took approximately two minutes on the
audit toolchain and completed without a timeout.

**Stage 3 result: pass.**

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim has no symbolic `requires` clause. Its precondition is the exact,
concrete configuration:

- `<k>` contains
  `verifyRange(solutionProgram, 1, 1000, 0, 0)`;
- `<env>` is the empty map;
- `<return>` is `noReturn`.

That literal configuration is an immediate satisfying witness, so the
precondition is realizable.

The postcondition requires `<k>` to be exactly `verified`, with the environment
again empty and the return state `noReturn`. This is not a free result variable.
`verified` can be reached only after the harness has:

1. invoked `run(solutionProgram, N)` for the current concrete `N`;
2. received a tuple `VTuple(VInt(E), VInt(O))`;
3. matched it syntactically against the exact accumulated digit-oracle counts;
4. advanced to `N + 1`;
5. repeated through `N = 1000`.

A wrong result leaves `VTuple(...) ~> expect(...)` stuck; no alternative rule
can skip the check. The base rule produces `verified` only when `N > MAX`, after
all 1,000 checks.

### Program identity

The proof uses the function constant `solutionProgram`. Its equation is a
manual K term rather than a file include, so identity was checked separately.
`evidence/program_identity_check.sh`:

1. parses the actual submitted MPY into KORE;
2. extracts the full `solutionProgram` right-hand side from `verification.k`;
3. converts K's internal `.Stmts` empty-list spelling to the equivalent empty
   concrete-list spelling;
4. parses that term into KORE;
5. compares the two KORE files byte-for-byte.

Both normalized KORE terms have SHA-256
`d2dbe7ed69624df16726fe8aaa493b5ece363ba5f171e26b3f999a80e9e82b20`;
the comparison exited 0 (`evidence/program-identity-check.log`). Thus the
`<k>` harness executes the exact structural program submitted in
`solution.mpy`.

An earlier auxiliary reachability identity claim was simplified completely by
the K frontend and caused the backend to report an empty claim set
(`evidence/program-identity-proof.log`). It is not counted as proof evidence;
the successful parser/KORE identity check is the operative check.

### Concrete substitution and body sensitivity

Representative satisfying executions give:

| Input | trusted canonical | candidate Python | fresh K |
|---:|---:|---:|---:|
| 1 | `(0,1)` | `(0,1)` | `(0,1)` |
| 3 | `(1,2)` | `(1,2)` | `(1,2)` |
| 12 | `(4,6)` | `(4,6)` | `(4,6)` |
| 1000 | `(48,60)` | `(48,60)` | `(48,60)` |

There are no helper or loop claims to pin: the finite harness concretely
unrolls all calls. As an additional sensitivity check, the auditor changed the
program's initial even count from 4 to 5 while leaving the oracle unchanged.
The mutated definition built, but its proof exited 1 with
`WarnStuckClaimState` at `n = 10`, showing actual `(5,5)` against expected
`(4,5)`. See `evidence/verification-body-mutation.k`,
`evidence/body-mutation-kompile.log`, and
`evidence/body-mutation-proof.log`.

**Stage 4 result: pass.**

## 5. Rule-by-rule static soundness review

The complete source and declaration extraction is preserved in
`evidence/static-inventory.log`. It counts 24 rules in `semantic.k`, 12 rules
in `verification.k`, and one claim in `spec.k`.

### Complete local syntax and attribute inventory

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`;
- `Params`: `Params(String)`;
- `Expr`: `Int(Int)`, `Name(String)`, `BinOp(String,Expr,Expr)`,
  `Compare(Expr,CmpOp)`, and `TupleExpr(Expr,Expr)`;
- `CmpOp`: `CmpOp(String,Expr)`;
- `Stmt`: `FuncDef(String,Params,Stmts)`, `Assign(Expr,Expr)`,
  `If(Expr,Stmts,Stmts)`, and `Return(Expr)`;
- `Stmts`: the juxtaposed `List{Stmt,""}` representation.

`MPY` additionally declares:

- values `VInt`, `VBool`, and `VTuple`;
- return states `noReturn` and `returned(Value)`;
- execution items `run`, `exec`, and `finish`;
- partial functions `eval`, `lookupValue`, `getInt`, and `getBool`;
- one configuration with `<k>`, `<env>`, and `<return>` cells.

`VERIFICATION` declares:

- function constant `solutionProgram`;
- functions `reverseDigits`, `evenPalindrome`, and `oddPalindrome`;
- harness items `verifyRange`, `expect`, and `verified`.

All constructor and execution-item productions carrying `[symbol]` are listed
above. They introduce names, not axioms about results. There are no local
`[total]`, `[functional]`, `[simplification]`, `[concrete]`, `[owise]`, or
priority declarations; there are no fresh variables, opaque result oracles,
auxiliary claims, or local lemmas. The imported K `INT`, `BOOL`, `MAP`, list,
and sequencing facilities are accounted for in Stage 7.

Every syntax form used by `solution.mpy` is covered: module/function/parameter,
statement lists, assignment-to-name, conditional, return, integer/name/binary
expressions, all five used binary operators, all five used comparisons,
comparison operators, and tuple construction. No unmodeled used construct is
silently fabricated.

### `semantic.k`: all 24 rules

| ID and location | Rule | Judgment |
|---|---|---|
| S1, line 54 | `getInt(VInt(I)) => I` | True typed projection; other values remain stuck. |
| S2, line 55 | `getBool(VBool(B)) => B` | True typed projection; other values remain stuck. |
| S3, line 57 | `eval(Int(I),_) => VInt(I)` | Faithful integer literal evaluation. |
| S4, line 58 | map `lookupValue` | Faithful lookup of the unique matching map key; absence remains stuck. |
| S5, line 59 | `eval(Name(X),ENV)` | Delegates to S4; all reachable reads are initialized. |
| S6, line 61 | binary `+` | K unbounded addition equals Python integer addition. |
| S7, line 63 | binary `-` | K unbounded subtraction equals Python integer subtraction. |
| S8, line 65 | binary `*` | K unbounded multiplication equals Python integer multiplication. |
| S9, line 67 | binary `//` via `/Int` | Correct for every reachable nonnegative dividend and positive divisor; over-broad for negative dividends, discussed below. |
| S10, line 69 | binary `%` via `%Int` | Correct for every reachable nonnegative dividend and positive divisor; over-broad for negative divisors, discussed below. |
| S11, line 72 | comparison `<` | Faithful integer comparison. |
| S12, line 74 | comparison `<=` | Faithful integer comparison. |
| S13, line 76 | comparison `>` | Faithful integer comparison. |
| S14, line 78 | comparison `>=` | Faithful integer comparison. |
| S15, line 80 | comparison `==` | Faithful integer equality for the used integer subset. |
| S16, line 83 | tuple evaluation | Builds the pair of recursively evaluated pure expressions; no modeled subexpression has side effects, so order is immaterial here. |
| S17, lines 85–88 | `run` target function | Matches the exact target binding and parameter, replaces the whole environment with `n`, clears return, executes the body, then finishes. This is the standalone invocation represented by the configuration. |
| S18, line 90 | empty `exec` | Consumes an empty statement list. |
| S19, lines 91–92 | skip `exec` after return | Correctly discards pending statement chunks after return; it requires `returned(_)`. |
| S20, lines 94–96 | assignment | Evaluates against the pre-update environment and updates the named local binding. |
| S21, lines 98–102 | true `if` branch | Executes then-statements followed by the enclosing rest when the pure condition is true. |
| S22, lines 103–107 | false `if` branch | Complement of S21 via `notBool`; executes else-statements then the rest. |
| S23, lines 109–111 | return | Evaluates the return expression, records it, and discards the current statement-list remainder. S19 handles enclosing continuations. |
| S24, lines 113–114 | finish | Emits the recorded value and restores `noReturn`. |

S21 and S22 are disjoint and exhaustive whenever the condition evaluates to a
`VBool`. Operator/constructor equations are pairwise disjoint. The partial
functions intentionally remain stuck for missing names, wrong value kinds,
unknown operators, or unused syntax rather than inventing a result.

Control and state are adequate for this program: expressions are pure, there is
one local environment, no heap or allocation, no I/O, and no exception is
reachable. Return propagation preserves the result and intentionally suppresses
remaining local statements. Concrete execution exercises zero/nonzero branches
and both early and final returns.

#### Arithmetic over-breadth

K's `/Int` truncates negative division toward zero, whereas Python `//` floors.
K's `%Int` also differs from Python when the divisor is negative. The unguarded
S9 and S10 equations therefore describe more syntax than they faithfully model.
The preserved probe `evidence/division-semantics-probe.mpy` compares:

```text
Python: (-3 // 2, 3 % -2) = (-2, -1)
K:                              (-1,  1)
```

See `evidence/division-semantics-probe.log`.

This is not a false-conclusion witness on the intended input domain. For every
`1 <= n <= 1000`, all divisions and remainders in the actual program have
nonnegative dividends and fixed positive divisors (`2`, `10`, `11`, or `100`).
`lead >= 1` before `previous = lead - 1`, so even `previous` remains
nonnegative. Thus no reachable intended-domain state activates the discrepant
cases. In accordance with the decision boundary, this is recorded as an
over-broad-but-sound-on-domain concern, not as material unsoundness or a reason
for `NOT_LEGIT`.

### `verification.k`: all 12 rules

| ID and location | Rule | Judgment |
|---|---|---|
| V1, lines 8–67 | `solutionProgram` equation | Definitional program constant. Its RHS is structurally identical to submitted MPY by the KORE comparison. It does not replace execution. |
| V2, lines 75–76 | `reverseDigits`, 0–9 | Exact one-digit reversal. |
| V3, lines 77–78 | `reverseDigits`, 10–99 | Exact two-digit decimal reversal, including leading zero in the reversed numeral as ordinary integer arithmetic. |
| V4, lines 79–82 | `reverseDigits`, 100–999 | Exact three-digit decimal reversal. |
| V5, line 83 | `reverseDigits(1000)` | Correctly yields 1. |
| V6, lines 85–86 | even-palindrome true case | Returns 1 exactly when reversal equals the input and parity is even. |
| V7, lines 87–88 | even-palindrome false case | Boolean complement of V6; returns 0. |
| V8, lines 89–90 | odd-palindrome true case | Returns 1 exactly when reversal equals the input and parity is odd. |
| V9, lines 91–92 | odd-palindrome false case | Boolean complement of V8; returns 0. |
| V10, lines 98–104 | recursive `verifyRange` | Runs the actual program before `expect`; updates both accumulators with the independently defined indicators; increases `N` by one. |
| V11, lines 106–107 | base `verifyRange` | Produces `verified` only after `N > MAX`; counts can be discarded because every prior result was already checked. |
| V12, lines 109–110 | `expect` | Consumes only an exactly equal pair and clears the local environment for the next standalone run. A mismatch has no rewrite. |

V2–V5 have disjoint guards and cover exactly `0..1000`, which is more than the
used `1..1000`. No `[total]` assertion claims behavior outside that range.
V6/V7 and V8/V9 have complementary guards wherever `reverseDigits` is defined.
The decimal equations and parity classification are ordinary mathematics.
`evidence/oracle_equations_test.py` independently compares their cumulative
meaning with the trusted canonical implementation for every input `1..1000`;
it exits 0 with zero mismatches (`evidence/oracle-equations-test.log`).

V10–V12 form a proof harness, not an operational bridge over program code. V10
places `run(P,N)` before the expectation, so the program body executes under
S17–S24. No task result is supplied to execution by the oracle. V12 merely
checks the observed result. The same opaque symbol is not shared between
execution and postcondition, and there is no unconstrained result-bearing
abstraction.

### Claim

`spec.k` contains exactly the one concrete reachability claim described in
Stage 4. It has no omitted symbolic input cell, implication-only result, or
existential result variable. Its finite enumeration exactly covers the source
contract domain.

**Stage 5 result: pass with the documented negative-arithmetic concern.**

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The auditor copied the proof definition to
`evidence/verification-vacuity.k`, gave it a distinct module, and changed the
result-constraining obligation from

```text
expect(EVENS + evenPalindrome(N), ODDS + oddPalindrome(N))
```

to demand one extra even palindrome. The literal entry state remains a
satisfying precondition. At the first input, `n = 1`, the real program returns
`(0,1)` while the mutation demands `(1,1)`.

The mutated definition command:

```text
kompile verification-vacuity.k --backend haskell \
  --main-module VERIFICATION-VACUITY --syntax-module MPY-SYNTAX \
  --output-definition audit-vacuity-kompiled
```

exited 0 (`evidence/vacuity-kompile.log`). The proof command:

```text
kprove spec-vacuity.k --definition audit-vacuity-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its residual begins with
`VTuple(VInt(0),VInt(1)) ~> expect(1,1)`, exactly the intended unmet result
obligation. See `evidence/spec-vacuity.k` and
`evidence/vacuity-proof.log`. This is not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation.

**Stage 6 result: pass.**

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted `semantic.k`, `verification.k`, and the K built-ins used by
those files, the exact MPY translation of `solution.py`, when invoked
independently with each integer from 1 through 1000, terminates with a pair
whose components equal the cumulative counts defined by decimal digit reversal
and integer parity. The check is result-sensitive, body-sensitive, and exhaustive
over the formal input domain.

The K theorem itself does not execute `canonical.py` or Python strings. It proves
the K program against the K digit equations. The following ledger separates the
remaining boundaries.

| Boundary | Influence and dependents | Evidence and assessment |
|---|---|---|
| K `INT`, `BOOL`, `MAP`, list, and K-sequencing built-ins | Arithmetic, guards, environments, statement lists, and control for every claim | Standard trusted K primitives. Acceptable low-level proof-engine boundary. |
| K compiler, LLVM backend, and Haskell prover v7.1.293 | All parsing, execution, and proof closure | Fresh independent builds; exact versions and outputs recorded. Necessary trusted toolchain boundary. |
| Trusted `py2mpy.py` | Connects Python AST syntax to submitted MPY | Candidate copy is byte-identical to trusted mount; regenerated MPY is byte-identical; structural program constant also KORE-identical. Acceptable trusted frontend boundary. |
| Generated MPY operational semantics | Connects used MPY constructors to Python behavior | Exhaustive static review plus normal/boundary K/Python comparisons. Sound for every reachable state in the stated domain. Negative arithmetic outside that reachable subset is a documented concern. |
| `reverseDigits`, `evenPalindrome`, `oddPalindrome` | Defines the formal postcondition consumed by `expect` | Truthful finite-domain equations, statically checked and independently compared on all 1,000 domain values. These specify the property; they do not provide the program result. |
| Decimal-reversal characterization of “integer palindrome” | Bridges the formal postcondition to natural-language intent | Ordinary mathematical equivalence for positive decimal integers; consistent with examples and trusted canonical implementation. No string semantics is formalized in K. Acceptable but informal intent bridge. |
| Trusted `canonical.py` and CPython execution | Supports implementation-to-intent and finite differential evidence | Independent oracle over every admitted input; zero mismatches. This is supporting evidence, not a substitute for `kprove`. |

There are no proof-local opaque values, fresh result symbols, empirical
operational bridges, simplification axioms, priorities, totality assumptions,
or auxiliary circularity claims. The digit equations are not opaque and have
complete, disjoint equations over their entire used domain.

Excluded behavior includes `n <= 0`, `n > 1000`, non-integer inputs, arbitrary
programs using the declared MPY syntax, negative-operand Python floor/modulo
behavior, division by zero, exceptions, side-effecting expressions, heap
objects, I/O, and multiple-function binding. None is part of the trusted prompt
contract or reachable submitted execution.

### Final gate assessment

- Real-program soundness: **pass**. The body executes, the program term is
  pinned, results are checked exactly, and both false-result and body mutations
  are rejected.
- Intent adequacy: **pass for `1..1000`**. The formal finite domain, inclusive
  range, ordering of tuple components, palindrome predicate, and parity match
  the prompt and canonical behavior.
- Trust/evidence auditability: **pass**. Commands, sources, mutations, bounded
  logs, witnesses, and finite test scopes are preserved.
- Documented limitation: the generated semantics overstates Python fidelity
  for negative operands even though those cases are unreachable in the theorem.
  This warrants `CONCERNS` but does not make any false intended-domain claim
  provable.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
