# Independent adversarial audit: 119-match-parens

The candidate reconstructs mechanically and its submitted claims print `#Top`,
but it does **not** contain a legitimate proof of the generated program. The
proof definition adds priority rules that replace both program-defined
functions with their desired mathematical summaries. There is no
fixed-semantics connection theorem, and fresh witnesses show that both rules
produce results different from fixed execution over configurations admitted by
their own match domains. There is also a real-Python boundary divergence:
`solution.py` raises `RecursionError` on an in-domain input for which both the
canonical program and the generated K semantics return `Yes`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. I did not search for,
infer, request, or use any hidden reference semantics. There is no
infrastructure-mode contradiction, so a candidate verdict is appropriate.

The live tools are `/usr/bin/kompile`, `/usr/bin/krun`, `/usr/bin/kprove`, and
`/usr/bin/kast`, all from K v7.1.293. See
`/audit-output/evidence/00-toolchain.log`.

### Required artifacts and provenance claims

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are all regular files, not
symlinks. No required artifact is missing or mistyped. There are no additional
helper K source files. The extra top-level trees are untrusted generated
material: `semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, and
`codex-trace/`. They were inventoried but none of their compiled products or
caches was copied into the initial scratch tree or used as proof evidence.

The candidate prompt and translator are byte-identical to their trusted mounts:

- `prompt.py`: SHA-256
  `7d057f437949f329d47d033084ee94a506621185f9063e13a91bbb741dca6216`.
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

These hashes agree with `run-input.json`. Full types, hashes, top-level extras,
and the generated-semantics mount check are in
`/audit-output/evidence/01-provenance.log`.

I treated all generation records only as claims. `metrics.json` claims exit 0
without timeout. `codex-last.txt` and the final log claim that the examples,
one aggregate `kprove`, and 3,969 Python input pairs passed. The one structured
JSONL trace contains 234 parseable records and repeats those claims. See
`01-trace-summary.log` and `01-generation-log-summary.log`. The trace and logs
do not substitute for any reconstruction below.

All source execution occurred in
`/tmp/audit-work/119-match-parens-audit`. Reviewer-authored artifacts and
bounded logs are under `/audit-output/evidence/`.

**Stage result:** provenance integrity passes. There are no missing, changed,
mistyped, or symlinked required artifacts. Candidate-provided compiled trees
are extra untrusted outputs and were ignored.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt supplies a list containing exactly two strings over
`(` and `)`. The function must return `"Yes"` iff either concatenation is a
balanced-parenthesis string; otherwise it must return `"No"`. “Balanced” means
that every prefix has at least as many opens as closes and the final counts are
equal.

The trusted canonical function forms both concatenations. Its local iterative
checker rejects a negative prefix and accepts only final balance zero.

The candidate uses a recursive `is_balanced(s, depth)`. For a normally
completing call, it rejects negative depth, accepts an empty suffix exactly at
depth zero, increments on `(`, and decrements on `)`. `match_parens` tries the
two concatenation orders in sequence. This is the same mathematical algorithm
on the promised alphabet, subject to Python recursion behavior discussed
below.

### Trusted translation

The exact command recorded in `02-regenerate-mpy.log` is:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

It exited 0. Both files have SHA-256
`8dbd9d8ccd21ca1bc99a1eb0aad2aa0eb7873eedc7d449b423bb12a5d8548e5b`.
The submitted constructor program is therefore exactly the trusted
translation of submitted `solution.py`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports
`/reference/canonical.py` (copied unchanged as `reference_canonical.py`) and
the staged `solution.py`. Its scope includes:

- both documented examples;
- both strings empty;
- the negative-depth, empty/depth-zero, empty/depth-nonzero, leading-`(`, and
  leading-`)` helper branches;
- first concatenation succeeds, second concatenation succeeds, and neither
  succeeds;
- all 127 parenthesis strings of lengths zero through six, hence all 16,129
  ordered pairs;
- 1,000 deterministic generated pairs with lengths up to 80;
- a CPython recursion-boundary input with lengths 600 and 600.

The first 17,139 checks agree. The final in-domain check does not:

```text
input lengths: [600, 600]
input: ["(" * 600, ")" * 600]
trusted canonical: ("return", "Yes")
candidate:         ("exception", "RecursionError")
CPython recursion limit: 1000
MISMATCH_COUNT: 1
EXIT_STATUS: 1
```

See `02-differential.log`. This is a material implementation-to-contract
divergence because the prompt contains no input-length restriction and asks the
function to return `Yes` or `No`.

The unchanged K semantics has no recursion-depth or exception state. A fresh
LLVM build executes that same 1,200-character input to `strVal(yesString)`; see
`03-build-semantic-llvm.log` and `03-krun-recursion-boundary-llvm.log`. A first
attempt with the Haskell concrete backend was killed with exit 137 after about
one minute (`03-krun-recursion-boundary-haskell-resource.log`). That backend
resource failure is recorded only as an infrastructure limitation; it is not
used as a candidate failure.

**Stage result:** translation fidelity passes, and ordinary finite test cases
strongly support the candidate's mathematical algorithm. Real-Python fidelity
does not fully pass: the unbounded K recursion model omits an observable
`RecursionError` on an intended-domain input.

## 3. Clean proof reconstruction

The scratch tree initially contained only candidate source artifacts and the
trusted canonical copy. No candidate `*-kompiled` directory or cache was
copied.

### Fresh semantic builds and concrete execution

Both fresh builds succeeded:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled-fresh
EXIT_STATUS: 0

kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled-llvm-fresh
EXIT_STATUS: 0
```

The Haskell definition concretely reaches:

- `["()(", ")"]` -> `strVal(yesString)`;
- `[")", ")"]` -> `strVal(noString)`;
- `["", ""]` -> `strVal(yesString)`;
- `["(", ")"]` -> `strVal(yesString)` (first order);
- `[")", "("]` -> `strVal(yesString)` (second order);
- `["(", "("]` -> `strVal(noString)`;
- `[ "))", "((" ]` -> `strVal(yesString)` (reverse order).

The exact commands, complete final configurations, and zero exits are in the
seven `03-krun-*.log` files. These cover normal execution, the zero-length
boundary, every source branch, and both entry branches. The LLVM stress run
described in Stage 2 establishes the generated-semantics result on the
recursion boundary.

### Fresh proof build and every positive claim

The proof definition was built solely from staged source:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition verification-kompiled-fresh
EXIT_STATUS: 0
```

The submitted aggregate command exited 0 and printed `#Top`:

```text
kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC
#Top
EXIT_STATUS: 0
```

See `03-build-verification.log` and `03-kprove-all-submitted.log`. A direct
fresh execution of submitted `prove.sh` also printed the two expected concrete
results and `#Top`, exit 0 (`03-prove-sh-fresh.log`).

Because the submitted claims are unlabeled, I made
`evidence/spec-audit-labeled.k`, which is the same three claims with labels
only. Each was then selected independently:

```text
SPEC-AUDIT-LABELED.universal   -> #Top, exit 0
SPEC-AUDIT-LABELED.prompt-yes  -> #Top, exit 0
SPEC-AUDIT-LABELED.prompt-no   -> #Top, exit 0
```

See `03-kprove-universal.log`, `03-kprove-prompt-yes.log`, and
`03-kprove-prompt-no.log`.

**Stage result:** mechanical clean reconstruction passes. This establishes
closure under the candidate's proof theory only; Stage 5 shows that theory is
not a sound proof theory for fixed program execution.

## 4. Adequacy and real-program pinning

### Plain-language reading of the claims

The universal claim has no separate `requires` clause. Its initial cells are:

- `<k>` contains `solutionProgram`;
- `<input>` is a two-element list expression containing arbitrary inductive
  parenthesis strings `A` and `B`;
- `<env>` and `<functions>` are empty maps;
- `<result>` is `noResult`.

It requires termination with empty `<k>`, an arbitrary final function map,
and result `strVal(contractAnswer(A,B))`. `contractAnswer` is `yesString` iff
`balanced(pconcat(A,B),0)` or `balanced(pconcat(B,A),0)`, and `noString`
otherwise. Thus the postcondition is result-constraining and expresses
equivalence, not a free result or one-way implication.

The two closed claims have the same empty initial state and require,
respectively, `yesString` for `["()(", ")"]` and `noString` for
`[")", ")"]`.

### Program identity

`solutionProgram` does not name a substitute algorithm. Its rule expands to
the complete constructor tree duplicated from `solution.mpy`.
`evidence/solution-program-expanded.mpy` is a source-parser spelling of that
RHS. Fresh `kast` normalization produced byte-identical KORE for it and the
submitted `solution.mpy`, SHA-256
`b33609af7503062ceb3121612ea66b20ac52cfcbc762e9c45db8f97511c79a9d`.
See `04-program-pinning.log`. Together with trusted translation identity, this
is adequate static pinning of the initial program term.

However, pinning the initial term does not make the proof execution-sensitive.
After the real module-loading and input-evaluation rules reach the
`match_parens` invocation, `verification.k:48-65` replaces that exact entire
invocation with `strVal(contractAnswer(A,B))`. Its priority 40 makes it preempt
the ordinary invocation/body rules. All conditionals, calls to `is_balanced`,
recursive computation, name resolution, returns, and caller-map restoration
inside `match_parens` are bypassed. There is no auxiliary reachability claim
from the fixed invocation state to this summary. There is likewise no helper
or recursive claim proving `verification.k:25-43`.

### Satisfiable preconditions and concrete substitution

A concrete universal pre-state is:

```text
<k> solutionProgram </k>
<input> ListExpr(PStr(.PString), PStr(.PString)) </input>
<env> .Map </env>
<functions> .Map </functions>
<result> noResult </result>
```

It is syntactically and semantically realizable. With `A=B=.PString`,
`contractAnswer(A,B)=yesString`; both Python implementations and fresh
concrete K execution return `Yes`. With `A=B=rp .PString`,
`contractAnswer(A,B)=noString`; both Python implementations return `No` on
that small input, and fresh concrete K execution agrees. The prompt examples
supply two further satisfying substitutions.

The 600+600 substitution also satisfies the universal precondition and reduces
the claimed K result to `yesString`, while real `solution.py` raises
`RecursionError`. This is a language-model adequacy failure even apart from the
proof-rule failure.

**Stage result:** the initial K term is exactly pinned and the result is
nontrivially constrained, but the successful proof does not execute the
property-bearing program body or connect a derived theorem to it. Real-program
adequacy fails.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule inventory is preserved in
`/audit-output/evidence/rule-inventory.md`; extraction counts and every source
rule line are in `05-static-inventory-extract.log`. It inventories:

- every local grammar production and all 22 runtime control constructors;
- the five-cell configuration and `Result`;
- all eleven `[function]` declarations;
- the absence of `[total]`, `[functional]`, `[simplification]`, and
  `[concrete]` declarations;
- the one unused opaque function (`ptail`);
- both priority rules and the one `[owise]` rule;
- all 76 ordinary rules in `semantic.k`;
- all nine rules in `verification.k`;
- all three reachability claims.

### Construct-to-semantics coverage

| Used construct | Declaration | Operational coverage |
|---|---|---|
| `Module`, `FuncDef` | `semantic.k:6,12` | load/launch rules 114-119 |
| `If`, `Return` | `semantic.k:13-14` | rules 121-129 |
| `Name` | `semantic.k:22` | environment/function lookup 136-137 |
| `Int`, `Bool`, `Str`, proof `PStr` | `semantic.k:23-25,61` | literal rules 132-135 and 202-241 |
| `BinOp("+"/"-")` | `semantic.k:27` | left-to-right rules 139-144 |
| `Compare("=="/"<")` | `semantic.k:28` | rules 147-154 and equality functions |
| integer `Subscript` and `[1:]` slice | `semantic.k:29-30` | rules 156-165 |
| two-element external `ListExpr` | `semantic.k:26` | rules 167-170 |
| one- and two-argument `Call` | `semantic.k:31` | rules 172-193 |
| entry/result control | runtime syntax 63-84 | rules 195-198 |

Every syntactic constructor in submitted `solution.mpy` therefore has a
visible operational route. Unsupported constructs fail by getting stuck rather
than by fabricated fallback rules.

### Generated semantics

The complete per-rule judgments are in `rule-inventory.md`. In summary:

- Rules 114-135 faithfully load the two top-level functions, sequence
  statements, implement conditional control and return unwinding, and evaluate
  literals for this program.
- Rules 136-137 are correct on this program's disjoint local and function
  names. They overlap globally if the same name occurs in both maps, so this
  reusable semantics does not model Python's local-first shadowing outside the
  exercised subset. I record that as a narrower unused-domain gap, not as a
  false conclusion about this submitted control path.
- Rules 139-181 implement left-to-right operand/callee/argument order for the
  exact binary, comparison, subscript, slice, list, and call forms used.
- Rules 185-198 install fresh local maps, restore caller maps, resolve the entry
  binding, and store the final result. They match the actual arities and
  control flow.
- Rules 202-241 truthfully implement the two result literals, conversion of
  parenthesis literals, concatenation, head/tail, and equality. Their recursive
  equations descend structurally. Partial cases—invalid alphabet characters,
  empty-string head/tail, unsupported equality types, bad indices, and other
  arities—are not reached by the promised input/program.
- The `[function]` symbol `ptail` has no equations but no uses, so it is an
  inert opaque symbol. The other semantic functions are covered on every
  reached domain. No function is falsely marked total.

The finite concrete evidence supports these judgments on the exercised
subset. It does not eliminate the CPython recursion/exception mismatch from
Stages 2 and 4.

### Mathematical proof helpers

`balanced`'s four guarded equations (`verification.k:12-15`) are disjoint,
cover every `PString × Int`, decrease the string when needed, and correctly
implement prefix failure and final depth zero.

`contractAnswer` (`verification.k:17-20`) is mathematically correct: its
positive rule is exactly the two concatenation disjunction, and `[owise]`
selects the complementary `noString` case. Neither helper is an unconstrained
oracle.

### Fatal operational bridges

The mathematical truth of the summaries does not justify replacing
program-defined execution with them.

#### `is_balanced` bridge (`verification.k:25-43`)

Classification: result-bearing operational bridge, priority 40.

Its LHS pins the helper closure body and arguments, but `...` admits arbitrary
continuations and the rule omits every state cell. Fixed invocation:

1. saves the caller environment;
2. binds `s` and `depth`;
3. executes all conditionals;
4. resolves a recursive `Name("is_balanced")` through `<functions>`;
5. executes the selected recursive binding;
6. restores the caller environment.

The bridge performs none of those steps and directly emits
`boolVal(balanced(S,D))`. No claim proves equality to fixed execution over the
bridge's complete match domain.

A concrete false-conclusion witness uses the valid parenthesis string `")"`,
depth 0, and a satisfiable `<functions>` map whose `"is_balanced"` binding
returns `true`. The bridge does not constrain that map:

- fixed semantics: `boolVal(true)`, `#Top`, exit 0
  (`05-bridge-base-helper.log`);
- bridge-enabled semantics: `boolVal(false)`, `#Top`, exit 0
  (`05-bridge-extended-helper.log`);
- asking fixed semantics for `false` fails with a `true` residual, exit 1
  (`05-helper-base-rejects-false.log`);
- asking bridge-enabled semantics for `true` fails with a `false` residual,
  exit 1 (`05-helper-extended-rejects-true.log`).

Thus the rule is false over its declared match domain and can enable a false
result on an intended-alphabet input.

#### `match_parens` bridge (`verification.k:48-65`)

Classification: result-bearing operational bridge, priority 40, and a direct
encoding of the target answer.

Its LHS pins the entry closure syntax and a two-parenthesis-string value, but
also omits `<functions>`. Fixed execution resolves both source-level
`Name("is_balanced")` calls from that cell. The bridge instead returns
`strVal(contractAnswer(A,B))` immediately. No connection claim derives this
from the fixed body.

For the in-domain inputs `[")", ")"]` and the same satisfiable true-returning
`"is_balanced"` binding:

- fixed semantics executes the source body and returns `yesString`, `#Top`,
  exit 0 (`05-bridge-base-match.log`);
- bridge-enabled semantics returns `noString`, `#Top`, exit 0
  (`05-bridge-extended-match.log`);
- the opposite fixed-semantics claim fails with a `yesString` residual, exit 1
  (`05-bridge-base-rejects-no.log`);
- the opposite bridge-enabled claim fails with a `noString` residual, exit 1
  (`05-bridge-extended-rejects-yes.log`).

The altered function binding is not reachable from the submitted empty-map
module-loading claim, but it is admitted by the unguarded bridge. A globally
false proof rule is not made true by an unstated reachability argument. More
fundamentally, even on the normal loaded binding the bridge assumes the exact
universal result requested in `spec.k` and bypasses every property-bearing
source operation. The candidate supplies neither an exact auxiliary execution
theorem nor an independently proved universal connection theorem.

`solutionProgram` (`verification.k:69-109`) is the one acceptable proof-side
rewrite: it is an exact, machine-compared alias for the submitted constructor
program and does not summarize a result.

**Stage result:** the core generated semantics is a plausible minimal model of
the constructs used, with documented unused-domain limitations. Both
proof-local operational bridges are materially unsound over their stated
domains and, on the actual proof path, the entry bridge smuggles the
correctness conclusion in place of execution. This independently requires
`FAIL / NOT_LEGIT`.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation artifact. The fresh
`evidence/spec-vacuity-audit.k` keeps the real prompt input `["()(", ")"]` but
changes the result obligation from the demonstrably correct `yesString` to
`noString`.

The mutation parses and builds against the fresh proof definition:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled-fresh \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
EXIT_STATUS: 0
```

The actual proof then fails for the expected unmet result:

```text
WarnStuckClaimState
<k> .K </k>
<result> strVal(yesString) </result>
EXIT_STATUS: 1
```

See `06-vacuity-dry-run.log` and `06-vacuity-proof.log`. The input is a
satisfying pre-state, and both trusted Python executions return `Yes`.

**Stage result:** the submitted result cell is non-vacuously constrained under
the candidate theory. This successful negative test does not repair the
unsound theory that produced the result.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the theory consisting of `semantic.k` **plus** all rules in
`verification.k`, the three initial configurations reach the stated result
cells. In particular, for arbitrary inductive `A,B`, the theory rewrites the
exact program alias through module loading and input evaluation, then applies
the priority axiom:

```text
invoke(exact match_parens closure, [A,B])
  => strVal(contractAnswer(A,B))
```

The remaining mathematical equations reduce that summary. This is a theorem
of the extended theory. It is not a reachability proof that fixed
`MPY-SEMANTICS` execution of the program-defined body has that result.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K Int, Bool, String, Map, List operations and Haskell/LLVM backends | all execution/proofs | Standard low-level toolchain trust; acceptable. |
| `/reference/py2mpy.py` | program identity | Trusted input; regenerated bytes and normalized term identity verified. |
| Generated `semantic.k` operational model | all K executions | Candidate-authored. The used small-input subset is supported by rule review and concrete tests; CPython recursion depth/exceptions are omitted and observably matter at length 1,200. |
| Proof-only `PStr(S) => parens(S)` | universal input representation | Transparent constructor bridge for the promised alphabet; acceptable as an ideal string representation, but does not model recursion limits. |
| `balanced`, `pconcat`, `contractAnswer` equations | formal postcondition | Truthful, exhaustive on their use domains, and structurally decreasing; acceptable mathematics. |
| `ptail` | none | Opaque due to no equations, but unused and result-irrelevant. |
| `solutionProgram` alias | all three claims | Exact normalized match to submitted `solution.mpy`; acceptable. |
| `is_balanced` priority bridge | any helper invocation in proof theory | Illegitimate and false over its match domain; no connection theorem; concrete opposite-result witness. |
| `match_parens` priority bridge | all three positive claims | Illegitimate, false over its match domain, and directly asserts the requested result instead of proving source execution. |
| Reviewer differential/concrete tests | Python/K intent bridge | Finite empirical evidence only. They support small-input behavior and expose the recursion mismatch; they do not prove universal equivalence. |
| Candidate's claimed 3,969-pair test | candidate narrative only | No candidate-authored test script was delivered. The trace/log claim is not proof evidence. |

### Gate accounting and decision

- **Real-program soundness:** fails. Both result-bearing operational bridges
  lack connection theorems; each has a machine-checked fixed-versus-extended
  opposite-result witness. The universal proof closes by the entry bridge.
- **Intent adequacy:** fails independently at the CPython recursion boundary.
  The prompt has no length restriction, while the candidate raises instead of
  returning and the generated semantics proves an idealized unbounded
  execution.
- **Non-vacuity:** passes. A concrete false result mutation builds and is
  rejected for the intended reason.
- **Evidence auditability:** the reviewer evidence is reproducible. Candidate
  generation prose and traces were not used as proof.

Mechanical `#Top`, exact initial program identity, correct small-input behavior,
and a discriminating result cell cannot legitimize a theory that assumes the
program's result in a priority rewrite. The appropriate completed-audit
decision is therefore `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
