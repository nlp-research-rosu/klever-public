# Independent adversarial audit: 142-sum-squares

## Overall determination

The candidate contains an honest, result-constraining partial-correctness proof
for the exact submitted MPY abstract syntax under its generated, idealized
integer-list semantics. The proof was rebuilt without candidate caches, both
claims closed together with `#Top`, the recursive-call claim also closed when
selected alone, concrete execution agrees with the mathematical contract, and a
fresh false result mutation was rejected for the expected unmet equality.

The qualification is material but does not make the partial-correctness proof
vacuous: the generated call semantics has an unbounded continuation stack,
whereas real CPython raises `RecursionError` for this recursively implemented
candidate on sufficiently long valid lists. For `[1] * 1000`, the fresh K
semantics and the trusted iterative canonical implementation both produce
`1000`, while `/candidate/solution.py` raises `RecursionError`. Thus the proof
does not establish the prompt's apparent total "shall return" behavior over all
finite Python lists, and its bridge to real CPython is limited to normal
executions within available recursion resources. This is why the verdict is
`CONCERNS / LEGIT`, not `PASS`.

All candidate prose, logs, traces, and prebuilt definitions were treated as
untrusted. The executable evidence below was reconstructed in
`/tmp/audit-work`; reviewer scripts, mutations, and bounded logs are in
`/audit-output/evidence`.

## 1. Input and provenance integrity

### Rendered semantics boundary

This is `GENERATED_SEMANTICS`. The required absence check succeeded:

```text
$ test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
EXIT_STATUS: 0
```

There is therefore no supplied or hidden reference semantics to compare or use.
There is no infrastructure contradiction. See
`evidence/toolchain-and-boundary.log`.

### Trusted input comparisons

The candidate prompt and translator are regular files, not symlinks, and are
byte-identical to the trusted mounts:

| Artifact | SHA-256 | `cmp` |
|---|---|---:|
| `/reference/prompt.py`, `/candidate/prompt.py` | `3705edce076dd10a274c837a15bf688a69bd9c342a0576cabb0cb02ab7c53446` | 0 |
| `/reference/py2mpy.py`, `/candidate/py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | 0 |

Both corresponding `diff -u` commands exited 0. See
`evidence/provenance-comparison.log`.

The required source and proof artifacts are present as regular files:

- `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
  `prove.sh`;
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`;
- one regular JSONL structured trace below `codex-trace/`.

No required artifact is missing, mistyped, or symlinked. The complete
two-level file-type inventory is in `evidence/candidate-inventory.log`.
An explicit `stat` check of every required source/metadata file and the deep
JSONL trace path is in `evidence/required-artifact-types.log`.
Candidate-provided `semantic-kompiled`, `semantic-llvm-kompiled`, and
`verification-kompiled` directories and `__pycache__` are extra generated
caches, not trusted inputs. None was copied into the reconstruction.

### Untrusted generation claims

`run-input.json` claims problem `142-sum-squares`, condition `bare`, and no
supplied semantics; this agrees with the rendered generated-semantics mode.
`metrics.json` claims a successful, non-timeout generation. `codex-last.txt`
and `codex-output.log` claim `#Top`. These were not accepted as proof evidence.
Their relevant contents and hashes are recorded in
`evidence/untrusted-metadata.log` and
`evidence/untrusted-generation-claims.log`.

The structured trace was read independently: all 198 JSONL records parsed, with
event-type counts and bounded summaries recorded in
`evidence/structured-trace-summary.log`. It records the generator's failed
intermediate parses and eventual proof claim, but neither those events nor the
candidate's compiled outputs were used to determine success.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and trusted canonical behavior

For a list of integers, use each element's zero-based index:

- square the value when the index is divisible by 3;
- otherwise cube it when the index is divisible by 4;
- otherwise leave it unchanged;
- return the sum of those contributions.

The divisible-by-3 case takes precedence at indices divisible by both 3 and 4,
such as index 12. The documented examples are:

```text
[1, 2, 3]             -> 6
[]                    -> 0
[-1, -5, 2, -1, -5]  -> -126
```

The trusted `/reference/canonical.py` iterates over
`range(len(lst))`, appending precisely those three contributions and returning
their sum.

The candidate is a mathematically equivalent right-to-left recursion: for a
nonempty list it computes the last index as `len(lst) - 1`, chooses that
element's contribution with the same precedence, recursively computes the
prefix `lst[:-1]`, and adds the contribution. The base case is the empty list.
This preserves all original indices in the prefix. It does not mutate the
input.

### Translator identity

In scratch, the trusted translator was run exactly as follows:

```text
$ cd /tmp/audit-work/translation
$ python3 py2mpy.py solution.py > regenerated-solution.mpy
translator_exit: 0
$ cmp -s regenerated-solution.mpy submitted-solution.mpy
byte_identity_exit: 0
```

Both submitted and regenerated MPY files have SHA-256
`2987f9f674b68d7e552479ad5eb5d84eb854953ff699a97526f4662733e93417`.
See `evidence/translation-identity.log`. Thus there is no source/translation
substitution.

### Independent differential reconstruction

`evidence/differential_test.py` loads scratch copies of the trusted canonical
entry point and candidate entry point using separate modules. It covers:

- all three documented examples;
- empty, zero, negative, and very large integer values;
- final-index representatives 0, 1, 2, 3, 4, 6, 8, and the shared
  3/4 boundary 12;
- every list length from 0 through 16;
- 500 deterministic generated lists, seed 142, lengths 0 through 60, values
  -20 through 20;
- nine recursion-boundary lengths from 900 through 1100.

The exact run was:

```text
$ python3 /audit-output/evidence/differential_test.py
total_cases=538
mismatches=4
...
EXIT_STATUS: 1
```

All 534 non-mismatching cases returned equal results. The four mismatches were
lengths 1000, 1001, 1050, and 1100: the canonical returned the list length for
all-one lists, while the candidate raised `RecursionError: maximum recursion
depth exceeded in comparison`. See `evidence/differential-test.log`.

This is not an audit-infrastructure failure and is not hidden. It is a real
implementation-to-intent limitation on valid lists of integers. Because the
requested theorem class is partial correctness, it does not falsify the
candidate's result on any observed normal return, but it prevents an
unqualified claim that the implementation fulfills the prompt for every finite
CPython list.

## 3. Clean proof reconstruction

### Fresh sources and toolchain

K was independently available at `/usr/bin/{kompile,kprove,krun}`, version
`v7.1.293`. `kup` was not present, but no installation was needed. Only
`semantic.k`, `verification.k`, `spec.k`, and the trusted-regenerated MPY file
were placed in `/tmp/audit-work/reconstruction`. Candidate compiled
definitions and caches were not copied.

Scratch-source hashes equal their candidate source counterparts, as recorded
in `evidence/static-inventory.log`; the definitions below were nevertheless
fresh builds.

### Fresh concrete and proof definitions

The generated semantics built with LLVM:

```text
$ kompile semantic.k --main-module MPY-SEMANTICS \
    --syntax-module MPY-SYNTAX --backend llvm \
    --output-definition semantic-llvm-kompiled
EXIT_STATUS: 0
```

The proof definition built with Haskell:

```text
$ kompile verification.k --main-module MPY-VERIFICATION \
    --syntax-module MPY-SYNTAX --backend haskell \
    --output-definition verification-kompiled
EXIT_STATUS: 0
```

See `evidence/fresh-concrete-build.log` and
`evidence/fresh-proof-build.log`.

### Fresh generated-semantics executions

`evidence/concrete_semantics_test.py` invoked `krun` on the
trusted-regenerated MPY file and parsed the final `<k>` result. All K runs
exited 0:

| Input | K | trusted canonical | candidate CPython |
|---|---:|---:|---|
| `[]` | 0 | 0 | 0 |
| `[1,2,3]` | 6 | 6 | 6 |
| `[-1,-5,2,-1,-5]` | -126 | -126 | -126 |
| `[-4]` | 16 | 16 | 16 |
| `[0,0,0,0,-3]` | -27 | -27 | -27 |
| `[0]*12 + [-3]` | 9 | 9 | 9 |
| large signed integers | exact arbitrary-precision result | same | same |
| `[1]*1000` | 1000 | 1000 | `RecursionError` |

The last row is direct evidence of the unbounded-stack semantics boundary.
Commands, statuses, and results are in
`evidence/concrete-semantics-test.log`.

### Positive target claims

The authoritative fresh run of every claim in the candidate's spec succeeded:

```text
$ kprove spec.k --definition verification-kompiled \
    --spec-module MPY-SPEC
#Top
EXIT_STATUS: 0
```

See `evidence/kprove-all-claims.log`. This command proves both
`sum-squares-call` and `sum-squares-program`; `#Top` is emitted only after the
whole selected spec closes.

The recursive-call claim also closes when selected independently:

```text
$ kprove spec.k --definition verification-kompiled \
    --spec-module MPY-SPEC \
    --claims MPY-SPEC.sum-squares-call
#Top
EXIT_STATUS: 0
```

See `evidence/kprove-sum-squares-call.log`.

A diagnostic filter selecting only `sum-squares-program` removes the
recursive-call claim that serves as its separately proved induction lemma. It
then unrolls and was interrupted after 60 seconds (exit 130); this is recorded
in `evidence/kprove-sum-squares-program.log` and is not substituted for the
successful unfiltered target run. The dependency is legitimate: the complete
run proves the auxiliary and end-to-end claims in the same proof set, while
the auxiliary itself has an independent `#Top`.

Finally, reviewer-authored concrete claims for an empty direct call and the
`[1,2,3]` end-to-end program state both closed with `#Top`, exit 0. See
`evidence/spec-ground-witness.k` and
`evidence/ground-witness-proof.log`.

## 4. Adequacy and real-program pinning

### Plain-language claim contracts

`sum-squares-call` has no hidden Boolean precondition. Its typed and cell
pattern says:

- begin exactly at `invoke1("sum_squares", ListVal(IS))`;
- use the exact single-entry function table `solutionFunctions`;
- permit any caller environment `ENV` and any continuation `KREST`;
- finish the call as `VInt(sumSquaresSpec(IS))` immediately before the same
  `KREST`;
- leave the exact function table unchanged and restore `ENV`.

This is an exact function-call summary, including binding, caller-local state,
and continuation, rather than a value-only rule that discards control.

`sum-squares-program` also has no hidden Boolean precondition. It says:

- start with the exact `solutionProgram`, followed by
  `run(ListVal(IS))`;
- start with empty functions and empty environment;
- load the submitted function, execute it, and end with the exact value
  `VInt(sumSquaresSpec(IS))`;
- end with exactly `solutionFunctions` and an empty restored environment.

The result is not an unconstrained variable, existential, implication, or
tautology. The entire `<k>` cell is consumed to the specified `VInt`.
Reachability is the appropriate one-way partial-correctness property; reverse
reachability is not required by the function contract.

### Satisfying states and substitutions

Each entry precondition is plainly satisfiable:

- call claim: `IS = .Ints`, `KREST = .K`, `ENV = .Map`, and
  `<functions> solutionFunctions </functions>`; the required result is
  `VInt(0)`;
- program claim: `IS = 1, 2, 3`, empty function/environment cells; the
  required result is `VInt(6)`.

Both are machine-checked by `spec-ground-witness.k`. Substitution
`IS = 0,0,0,0,-3` gives `-27`, and substitution with 13 elements ending in
`-3` gives `9` because divisibility by 3 takes precedence at index 12. The
fresh K runs, candidate Python normal runs, and trusted canonical runs agree
on these values.

### Exact program identity

The proof does not replace the function call with `sumSquaresSpec`.
`solutionProgram` is a definitional alias for:

```text
Module(FuncDef("sum_squares", Params("lst"), sumSquaresBody))
```

and `sumSquaresBody` is the exact constructor tree in the regenerated
`solution.mpy`: outer empty-list test; `index` and `value` assignments; nested
modulo tests; square/cube/identity assignment; recursive prefix call; and
addition. `solutionFunctions` is exactly the map produced by the module-load
rule for the same parameter and body. These definitions occur at
`verification.k:29-67`; the submitted constructor tree is
`solution.mpy:1-31`.

The independent translator check pins `solution.mpy` to `solution.py`, and
the fresh concrete runs execute that actual regenerated file. The end-to-end
claim first rewrites only the two aliases and then uses the ordinary
`Module`, load, invoke, statement, expression, recursive-call, and return
rules. No task-specific operational rule rewrites the submitted program to
its expected answer.

The recursive claim matches real control flow at the precise
`invoke1` configuration produced by the recursive `Call`. Its arbitrary
`KREST` is justified by exact preservation: fixed execution puts the returned
value before that same continuation and restores the caller environment
before continuing.

### Adequacy limitation

The syntax and control rules pin the submitted algorithm, but they model an
unbounded mathematical call stack and no exceptions. Consequently they do
not pin CPython's resource-exhaustion behavior. The concrete false bridge
witness is `[1] * 1000`: K reaches `VInt(1000)` while real candidate CPython
raises `RecursionError`. This is reported as a language-model and
total-behavior limitation, not as a fabricated K result on a normal execution.

## 5. Rule-by-rule static soundness review

The only candidate K sources are `semantic.k`, `verification.k`, and
`spec.k`. `evidence/static-inventory.log` records every declaration, rule,
claim, and searched attribute. There are no helper K files.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares:

| Lines | Declaration and audit |
|---|---|
| 6 | `Pgm ::= Module(Stmts)`, exactly the translated module root. |
| 8 | whitespace-separated `Stmts`, matching translator juxtaposition. |
| 9-12 | `FuncDef`, `Return`, `Assign`, `If`; all and only submitted statement forms are covered. |
| 14-15 | `Params` and comma-separated strings; the one `"lst"` parameter parses. |
| 17 | comma-separated `Exprs`; both empty and one-argument forms in the program parse. |
| 18-25 | `Int`, `Name`, `ListExpr`, `BinOp`, `UnaryOp`, `Compare`, `Call`, `Subscript`; every submitted expression constructor is included. |
| 26-27 | comparison-list and `CmpOp`; submitted comparisons contain exactly one operator. |
| 28-30 | expression index, `Slice`, expression/no bound; covers `[-1]` and `[:-1]`. |
| 37-39 | empty, singleton, and snoc integer sequences; surface order equals Python list order. |
| 40-43 | integer, Boolean, integer-list, and `None` runtime values. |

`MPY-SEMANTICS` has one configuration (`semantic.k:54-57`):
`<k> $PGM ~> run($ARGS) </k>`, a function table, and a local environment.
No heap, allocation, output, or exception cell is present. That is sufficient
for the submitted program's immutable integer values and non-mutating slices,
but it is also the source of the documented exception/resource limitation.

Runtime syntax is exhaustively:

- `function1(String, Stmts)` (`:59`);
- `normal` and `returned(Value)` (`:61`);
- continuations `load`, `run`, `exec`, `eval`, `invoke1`, `finishCall`,
  `restoreEnv`, `assignTo`, `choose`, `afterBranch`, `binLeft`, `binRight`,
  `compareLeft`, `compareRight`, `callOne`, `lengthResult`, `lastResult`, and
  `initResult` (`:63-80`);
- `makeReturned` (`:119`) and `negateResult` (`:136`);
- function symbols `binResult`, `compareResult`, `lengthInts`, `lastInt`, and
  `initInts` (`:161,167,172,177,181`).

`MPY-VERIFICATION` adds exactly five function symbols:
`elementContribution`, `sumSquaresSpec`, `sumSquaresBody`,
`solutionProgram`, and `solutionFunctions`.

There are no local `[total]`, explicit `[functional]`, priority, `owise`,
`anywhere`, macro, or opaque declarations. K's `[function]` attribute is used
on the ten symbols listed above; it is not treated as proof of their equations.
Only the three `elementContribution` equations carry `[simplification]`.

### Operational rule inventory

Every one of the 50 semantic rules was reviewed:

| Lines | Rules | Decision |
|---|---|---|
| 84-88 | `Module -> load`, empty load, and function-definition load | Sound. Bodies are not executed at definition time; the exact parameter/body pair is stored. The actual module contains one definition, so map update is unambiguous. |
| 90 | `run(ARG) -> invoke1("sum_squares", ARG)` | Sound task entry dispatch for the required entry point. It does not determine the result. |
| 94-100 | invoke, normal/returned call finish, caller-environment restoration | Sound for idealized unbounded normal execution. A fresh callee map contains only its parameter; exact function binding supplies `BODY`; returned values and caller maps are preserved. No stack/resource cell means this subsystem does not model `RecursionError`, with witness `[1]*1000`. |
| 104-109 | empty statement list, return, assignment scheduling and update | Sound. `Return` discards the unexecuted tail; assignment evaluates before updating a name and then resumes the exact tail. |
| 110-117 | `If`, true/false choice, normal branch continuation, returned branch propagation | Sound and disjoint on Boolean values. The exact remaining statements are resumed only after normal branch completion; a returned branch bypasses them. |
| 120 | `makeReturned` | Sound conversion of the evaluated return expression to explicit return control. |
| 123-126 | integer literal, name lookup, empty list literal | Sound for used terms. Lookup requires the real binding; it does not invent a value. Only the used empty list literal is modeled. |
| 128-133 | binary-expression, left, and right continuations | Sound left-to-right Python operand order. This is especially important for restoring the caller environment before looking up `contribution` after the recursive call. |
| 135-137 | unary minus scheduling/result | Sound integer negation; used only for literal `-1`. |
| 139-144 | single comparison scheduling/result continuation | Sound left-to-right evaluation for the one-comparison form used by the program. Chained comparisons are syntactically admitted but deliberately unmodeled; none occurs. |
| 146-150 | `len`, non-`len` named call, and call continuation | Sound on the actual bindings. The guards for built-in `len` and other names are disjoint. The only other call is the loaded, unshadowed global `sum_squares`. |
| 154-159 | last-element index and all-but-last slice scheduling/results | Sound for nonempty integer lists. The program reaches these forms only on the nonempty branch. Surface snoc representation preserves Python order. |
| 162-165 | `+`, `-`, `*`, `%` integer result equations | True and pairwise disjoint by operator. K and Python modulo agree for the only modulo operands used: nonnegative indices and positive divisors 3 or 4. Other operator/value combinations remain visibly stuck. |
| 168-170 | integer equality and integer-list equality to empty | True and constructor-disjoint. List equality is defined only in the exact empty-list comparison used by the program. |
| 173-175 | empty/singleton/snoc length | True, disjoint by constructor, structurally descending. Covers every runtime integer list. |
| 178-179 | singleton/snoc last element | True and disjoint for every nonempty runtime list. Empty is intentionally undefined and unreachable at its used call site. |
| 182-183 | singleton/snoc initial prefix | True and disjoint for every nonempty runtime list. Empty is intentionally undefined and unreachable at its used call site. |

The generated semantics therefore fails visibly for admitted but unused
constructs rather than fabricating their outcomes. No rule has a task-answer
right-hand side, no program body is skipped, and no fresh/unconstrained result
symbol affects control or the postcondition.

### Verification-function and simplification inventory

Every one of the eight verification equations was reviewed:

| Lines | Equation(s) | Decision |
|---|---|---|
| 10-17 | three `elementContribution(N,I)` equations | True. Guards partition all integer indices into divisible by 3; not by 3 but divisible by 4; and neither. They are pairwise disjoint and exhaustive. The three simplification attributes expose true arithmetic equalities, not operational shortcuts. |
| 20-25 | empty and nonempty `sumSquaresSpec` | True structural definition. Guards are complements. The recursive case removes exactly the final element and uses prefix length as its original zero-based index. It descends on every ground nonempty list. |
| 30-59 | `sumSquaresBody` | Exact definitional alias for the submitted body; no computation is summarized. |
| 62-63 | `solutionProgram` | Exact module/function wrapper around that body; no answer is encoded. |
| 66-67 | `solutionFunctions` | Exact map created by the module-load rule; fixes binding, parameter, and body. |

No `[total]` claim overstates the intentionally partial helper functions.
`binResult` and `compareResult` have disjoint literal/operator equations;
`lastInt` and `initInts` cover their complete used nonempty domain.
`elementContribution` and `sumSquaresSpec` cover the full formal constructor
domain relevant to their uses. There are no conflicting equations or priority
interactions.

`sumSquaresSpec` is result-bearing, but it is a definitional mathematical
postcondition, not an opaque oracle or operational bridge. Fixed semantics
computes the function body; the recursive reachability claim connects that
execution to the definition. The same symbol is not used to replace a program
expression.

### Claim inventory and control/state containment

`spec.k` contains exactly two claims:

1. `sum-squares-call` (`:8-12`) is an auxiliary execution theorem over the
   exact invocation, function table, arbitrary continuation, and arbitrary
   caller environment. It preserves every cell in the three-cell semantics.
   Recursive use is a standard progressed circularity: fixed execution first
   evaluates the nonempty test, index/value/contribution, and prefix before
   returning to a strictly shorter matching invocation.
2. `sum-squares-program` (`:16-20`) loads the exact module from empty state and
   reaches the exact result. It depends on the first, independently closing
   claim.

There is no operational bridge rule in `verification.k`. The auxiliary claim
is proved against the fixed generated semantics and its complete accepted
context; it is not compiled as a shortcut into concrete execution. The body,
binding, evaluation order, return unwinding, and environment restoration all
remain sensitive.

### Construct-to-rule coverage

Every constructor in `solution.mpy` is pinned as follows:

| Submitted construct | Declaration | Executing rules |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `:6,8-15` | `:84-90` |
| `If` and nested branch lists | `:12` | `:110-117` |
| `Return` | `:10` | `:105,120,97-100` |
| `Assign(Name, ...)` | `:11,19` | `:106-109,124-125` |
| `Int`, empty `ListExpr`, `Name` | `:18-20` | `:123-126` |
| `Compare(..., CmpOp("==",...))` | `:23,26-27` | `:139-144,168-170` |
| `BinOp` for `+,-,*,%` | `:21` | `:128-133,162-165` |
| `UnaryOp("-",Int(1))` | `:22` | `:135-137` |
| `Call(Name("len"),...)` | `:24` | `:146-147` |
| recursive `Call(Name("sum_squares"),...)` | `:24` | `:148-150,94-100` |
| last `Subscript` | `:25,28` | `:154-156,178-179` |
| prefix `Subscript(...Slice...)` | `:25,29-30` | `:157-159,182-183` |

The concrete test set exercises each used construct and all three contribution
branches, including the shared 3/4 boundary.

### Static soundness conclusion

Within the chosen idealized semantics level, every local rule is supported by
the actual program behavior or ordinary integer/list mathematics. I found no
locally false proof equation, overlap, priority exploit, unconstrained oracle,
state loss, or execution bypass. Accordingly, I do not label a local rule
unsound.

The narrower evidence gap is that no stack/exception model or universal
connection theorem relates unbounded `invoke1` execution to all CPython
executions. The concrete boundary witness is preserved rather than being used
to allege a different, unwitnessed rule defect.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; none was trusted or reused.
The reviewer-authored `evidence/spec-vacuity.k` preserves the legitimate
recursive-call lemma and changes the end-to-end destination from:

```text
VInt(sumSquaresSpec(IS))
```

to the deliberately false:

```text
VInt(sumSquaresSpec(IS) +Int 1)
```

`IS = .Ints` is a concrete satisfying witness: fixed execution returns 0,
while the mutation requires 1.

The mutation parsed and compiled to KORE:

```text
$ kprove spec-vacuity.k --definition verification-kompiled \
    --spec-module MPY-SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

See `evidence/vacuity-dry-run.log`.

The actual proof then reached the correct result and failed on precisely the
false equality:

```text
#Not ({ sumSquaresSpec ( IS ) +Int 1
        #Equals sumSquaresSpec ( IS ) })
...
<k> VInt ( sumSquaresSpec ( IS ) ) ~> .K </k>
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
EXIT_STATUS: 1
```

The output includes `WarnStuckClaimState` at the mutated claim. This is an
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. Full bounded output is in
`evidence/vacuity-proof.log`. The proof is therefore non-vacuous and
discriminates an off-by-one result.

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly built `MPY-SEMANTICS` and the reviewed mathematical
definitions in `MPY-VERIFICATION`, K proves partial correctness for every
defined runtime integer sequence `IS`:

- an exact call to the loaded submitted body, in any caller environment and
  before any continuation, can only return
  `VInt(sumSquaresSpec(IS))` at that continuation, with the caller environment
  restored; and
- loading the exact submitted module from empty state and running it on
  `ListVal(IS)` reaches exactly that result and the exact loaded function map.

The definition of `sumSquaresSpec` is the prompt's right-to-left sum:
empty is zero; each nonempty list is its prefix sum plus the final element's
square/cube/identity contribution according to the final index.

This is partial correctness. The cyclic reachability proof does not establish
a CPython recursion-resource bound, absence of exceptions, or total
termination of the actual Python implementation.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| K 7.1.293 compiler, LLVM/Haskell backends, and `kprove` | All concrete and symbolic results | Standard unavoidable toolchain trust; fresh builds and both concrete/symbolic backends were used. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, `K-EQUAL`, and generated collection machinery | Arithmetic, guards, bindings, structural equality, lists | Acceptable low-level K trust boundary. Only ordinary mathematical integer operations and finite maps are used. |
| Trusted `/reference/py2mpy.py` | Source-to-MPY identity | Mounted trusted input; regeneration is byte-identical. The proof itself begins at MPY syntax and does not prove translator correctness. |
| `solutionProgram`, `sumSquaresBody`, `solutionFunctions` aliases | Pin the proof claim to the submitted AST and binding | Audited exact definitions, byte-identity translation, actual MPY concrete execution. No operational result shortcut. |
| Candidate-generated Python subset semantics | Connects MPY execution to idealized Python normal execution | Exhaustively statically audited for every used construct and concretely checked. There is no formal connection theorem to CPython. |
| Runtime `ListVal(Ints)` representation | Connects Python integer lists to K values | Surface order preserved; empty/singleton/snoc equations audited; examples, boundaries, random inputs, and large integers tested. |
| `elementContribution` and `sumSquaresSpec` | Give the postcondition its task meaning | Transparent, exhaustive mathematical equations. No opacity. Their prompt/canonical bridge is direct by index cases and finitely supported by differential tests. |
| Unbounded call continuation; absent exception/resource cells | Affects whether deep recursive executions return normally | Concerning limitation. `[1]*1000` gives K/canonical 1000 but candidate CPython `RecursionError`. The proof must not be read as total correctness or exception freedom. |

There are no custom opaque symbols, fresh result oracles, empirical rewrite
bridges, proof-local priority rules, or assumed program summaries. The only
result-bearing abstraction is the transparently defined postcondition, and
program execution is independently connected to it by the proved call claim.

### Evidence scope

The 538-case differential run is finite evidence about the implementation and
intent bridge, not a replacement for the K proof. It supports equality on all
534 observed normal-return cases and exposes four recursion-limit exceptions.
The eight fresh K concrete cases are likewise finite semantics checks. The
universal result under the selected semantics comes only from the reconstructed
`kprove #Top`.

### Gate and decision summary

- Real-program proof soundness under the selected idealized semantics: pass.
  The exact body executes; all result equations are true; state/control are
  preserved; the false mutation fails.
- Formal intent adequacy: limited. The mathematical value matches the prompt,
  but the recursive implementation and unbounded semantics do not establish
  the prompt's apparent total return behavior for all finite CPython lists.
- Trust/evidence auditability: pass with the above explicit boundary. All
  commands, statuses, finite test scopes, source hashes, and mutation residuals
  are preserved.

The limitation warrants `CONCERNS`, but the proof remains `LEGIT`: it is a
sound, non-vacuous partial-correctness proof of the exact submitted algorithm
for normal executions in the generated semantics, not a substituted program or
answer-encoding theory.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
