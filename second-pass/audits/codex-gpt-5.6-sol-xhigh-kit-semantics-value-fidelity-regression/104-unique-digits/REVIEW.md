# Independent adversarial review: 104-unique-digits

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied MPY semantics. I reconstructed the
definitions from trusted source, obtained fresh `#Top` results for the target
claims with their actual circularity dependencies, proved the proof-local
operational bridge from the bridge-free semantics, checked concrete ground
witnesses, and observed the expected stuck state for a fresh false result.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
machine-checked entry postcondition is expressed as
`sortVS(filterOddDigits(VS))`. The connection from the recursively defined
`oddDigits` summary to the English decimal-digit property is an ordinary but
informal induction, and `sortVS` is explicitly an opaque symbolic primitive of
the supplied semantics. These are transparent intent/trust boundaries,
supported by static review and fresh finite tests; they do not permit a false
program result or make the proof illegitimate.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it:

- `/reference/reference-semantics` exists as an ordinary directory.
- `/candidate/reference-semantics` contains no symlinks.
- A relative-path/type manifest comparison and a recursive
  `diff -qr --no-dereference` both returned 0. There were no missing,
  additional, mistyped, changed, or symlinked entries in the candidate
  semantics tree.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `bebe5af48f3614d96f23c19fa6134409f0b3bfe2f759662569f0987e15e0507c`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `solution.py`, `solution.mpy`, `verification.k`, and `spec.k` are ordinary
  files. One structured JSONL trace is present under
  `/candidate/codex-trace/2026/07/23/`.

The complete check and hashes are in
[`01-integrity.log`](evidence/logs/01-integrity.log). The candidate's
`metrics.json` says generation exited 0, and its final report claims validation,
but I treated those as untrusted provenance claims. I did not use any
candidate-provided `*-kompiled` directory, `.pyc`, prior `#Top`, prior mutation
output, or `PROOF.md` conclusion.

The live independently installed toolchain is K v7.1.293; exact paths and
versions are in [`01-toolchain.log`](evidence/logs/01-toolchain.log). There is
no trusted-mount contradiction and therefore no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of positive integers, retain every occurrence of each
integer whose decimal representation contains no even digit, and return the
retained values sorted in increasing order. Empty input is allowed; duplicates
are retained. The two documented examples are:

- `[15, 33, 1422, 1]` → `[1, 15, 33]`
- `[152, 323, 1422, 10]` → `[]`

This restatement follows `/reference/prompt.py` and
`/reference/canonical.py`. The canonical implementation converts each positive
integer to decimal text, tests all characters, filters, and sorts.

The candidate uses a different but equivalent arithmetic algorithm on the
intended domain. For each positive `n`, it repeatedly examines `y % 2` and
sets a sticky flag false when the current last decimal digit is even, then
replaces `y` by `y // 10`. An integer and its last decimal digit have the same
parity, and division by 10 removes that digit. The flag is reset for each list
element, never changes back to true within the inner loop, and the final
in-place sort retains duplicates.

The positive-input restriction matters. For example, the candidate would
accept `0` because its inner loop does not run, whereas the canonical decimal
test rejects digit `0`. Zero and negative integers are outside both the prompt
domain and the K entry precondition, so this is not a contract divergence.

### Translator identity

In a clean scratch directory I ran the trusted translator over the submitted
`solution.py`. `cmp` returned 0 and both submitted and regenerated `.mpy` files
have SHA-256
`4858c38d8c5f1ff63a30b30d85980a8d4f6e6bb2912f9cc88aea77fec2129a04`.
See [`02-translation-identity.log`](evidence/logs/02-translation-identity.log)
and the preserved
[`regenerated-solution.mpy`](evidence/artifacts/regenerated-solution.mpy).

### Independent differential test

The reviewer-authored
[`differential_test.py`](evidence/scripts/differential_test.py) independently
loads `/reference/canonical.py` and the scratch copy of the submitted
`solution.py`. Its 4,278 intended-domain cases comprise:

- both documented examples;
- 21 explicit empty, decimal-transition, parity, duplicate, and huge-integer
  boundary cases;
- all lists of length 0 through 3 over 14 branch-sensitive values (2,955
  cases);
- every singleton from 1 through 300;
- 1,000 deterministic generated lists of positive integers.

The exact serialized inputs are
[`differential-inputs.json`](evidence/artifacts/differential-inputs.json),
SHA-256
`265c8d1e703d8f9911050fb95bb0ee684f2363fb8b147347611f55b1359ec3ea`.
The run exited 0 with zero result mismatches and zero input mutations; see
[`02-differential.log`](evidence/logs/02-differential.log). This is finite
evidence for program-to-canonical fidelity, not a substitute for the K proof.

## 3. Clean proof reconstruction

I copied only candidate source artifacts needed for proof and trusted source
artifacts into `/tmp/audit-work/104-unique-digits`. The imported
`reference-semantics` came from `/reference`, not from a candidate build.
There were no compiled definitions in the scratch directory before the fresh
builds.

### Fresh proof definition and target claims

The exact fresh Haskell build was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exited 0; see
[`03-kompile-verification.log`](evidence/logs/03-kompile-verification.log).

The claims form a dependency chain: `filter-loop` uses the `digit-loop`
circularity, and `unique-digits` uses both loop circularities. I tested the
smallest dependency-respecting prefix for each target:

| Target checked | Selection | Exit | Result |
|---|---|---:|---|
| `SPEC.digit-loop` | `--claims SPEC.digit-loop` | 0 | `#Top` |
| `SPEC.filter-loop` plus its already separately checked digit helper | `--exclude SPEC.unique-digits` | 0 | `#Top` |
| `SPEC.unique-digits` plus both required loop helpers | complete `SPEC` | 0 | `#Top` |

The bounded logs are
[`03-kprove-digit-loop.log`](evidence/logs/03-kprove-digit-loop.log),
[`03-kprove-filter-with-digit-dependency.log`](evidence/logs/03-kprove-filter-with-digit-dependency.log),
and [`03-kprove-all-claims.log`](evidence/logs/03-kprove-all-claims.log).

For transparency, I also diagnostically selected `filter-loop` while removing
its `digit-loop` circularity. That dependency-stripped run was still actively
rewriting when the reviewer-imposed 900-second limit terminated it with status
143 and no proof result; see
[`03-kprove-filter-loop.log`](evidence/logs/03-kprove-filter-loop.log). It is
neither positive evidence nor a candidate failure. Retaining the actual helper
claim makes the same filter target close in about 14 seconds.

### Bridge-free connection definition

I separately compiled `VERIFICATION-BASE`, which omits the priority-40
operational normalization:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition fresh-connection-kompiled
```

The build exited 0
([`03-kompile-connection.log`](evidence/logs/03-kompile-connection.log)).
The `CONNECTION-SPEC.loop-yield-int` theorem then exited 0 and printed `#Top`
against that bridge-free definition
([`03-kprove-connection.log`](evidence/logs/03-kprove-connection.log)).

### Fresh concrete reconstruction

Although concrete reconstruction is mandatory only for generated semantics, I
also built the trusted supplied semantics afresh with the LLVM backend and
`MPY-KRUN`; see
[`04-kompile-runtime.log`](evidence/logs/04-kompile-runtime.log). The function
prefix in reviewer concrete tests was byte-identical to `solution.py`.
The initial seven branch/boundary assertions completed with `.K`, `NoExc`, an
empty stack, and exit code 0
([`04-krun-concrete.log`](evidence/logs/04-krun-concrete.log)).

I then generated 64 additional deterministic K assertions from the trusted
canonical Python oracle. The cases and expected results are in
[`k-differential-cases.json`](evidence/artifacts/k-differential-cases.json).
Their trusted translation and fresh `krun` completed with `.K`, `NoExc`, empty
stack, and exit code 0; see
[`07-generate-k-differential.log`](evidence/logs/07-generate-k-differential.log),
[`07-translate-k-differential.log`](evidence/logs/07-translate-k-differential.log),
and [`07-krun-k-differential.log`](evidence/logs/07-krun-k-differential.log).

## 4. Adequacy and real-program pinning

### Plain-language meaning of each positive claim

1. `digit-loop` (`spec.k:6-19`): if the current `y` is a non-negative
   integer `Y` and the incoming flag is `O`, executing the real internal while
   loop consumes the loop computation, sets `y` to 0, and sets `odd` to
   `O andBool oddDigits(Y)`. The rest of the function state and any following
   continuation are framed.

2. `filter-loop` (`spec.k:21-39`): if the remaining iterable is a list `VS`
   of positive integers and the result object initially contains `ACC`,
   executing the real outer loop consumes it and changes that object to
   `filterOddAcc(ACC, VS)`. The final scratch locals `n`, `odd`, and `y` are
   existential because they do not affect the returned list.

3. `unique-digits` (`spec.k:41-63`): from the standard empty module
   configuration, load the submitted function body and call it on an unboxed
   list `VS` of positive integers. The call returns exactly `ref(0)`, and heap
   location 0 contains exactly
   `list(sortVS(filterOddDigits(VS)))`; the frame stack is empty, no exception
   is present, and exit code remains 0.

4. `loop-yield-int` (`connection-spec.k:8-17`): under the fixed supplied
   semantics, yielding an integer to a `for` loop binds that same integer,
   executes the same body, and installs the same loop continuation as the
   proof-local normalization, for an arbitrary trailing computation.

### Pinning to the submitted program

The entry claim does not call a replacement summary. Its `<k>` cell loads a
`Module(FuncDef("unique_digits", Params("x"), #uniqueDigitsBody))`, then invokes
that closure. The four nullary aliases expand as follows:

- `#digitCondition` is exactly `solution.mpy:10`;
- `#digitBody` is exactly `solution.mpy:11-14`;
- `#outerBody` is exactly `solution.mpy:8-17`;
- `#uniqueDigitsBody` is exactly the function body at `solution.mpy:3-19`.

Empty translator productions such as `ListExpr()` and an omitted `else` parse
as the explicit `.Exprs` and `.Stmts` used in the aliases. Initializations,
loop target, loop iterand, statement order, append call, in-place sort, and
return all match. The submitted `.mpy` was independently regenerated
byte-for-byte in stage 2. The concrete-test function prefix was also
byte-identical to the submitted `solution.py`, and the fresh final
configurations print the same full closure body.

This is structural pinning to the current submitted AST, even though the spec
spells out that AST through readable aliases rather than reading
`solution.mpy` by path. A later source edit would require this audit to repeat
the comparison; no such mismatch exists here.

### Result constraint and satisfiable states

The return is not a free variable. The entry destination fixes both the returned
reference (`ref(0)`) and its heap value. The existential `?SC` relaxes only the
unobserved final scope map; it cannot choose or change the return or heap
result. The auxiliary claims similarly constrain their property-bearing state
changes; only irrelevant final scratch locals are existential.

Each precondition is satisfiable:

- `digit-loop`: take `Y = 0`, `O = true`, any integer `L`, and a scope
  containing the five displayed bindings.
- `filter-loop`: take `VS = vCons(1, vCons(2, .ValSeq))`, an empty `ACC`, and
  an allocated result-list heap cell.
- `unique-digits`: take `VS = vCons(1, .ValSeq)`, or the documented example
  sequence. `positiveInts` reduces to true in both cases.

Reviewer-authored ground claims execute the exact body under
`VERIFICATION-BASE`, with the operational bridge absent. Both `[1] → [1]` and
the example `[15,33,1422,1] → [1,15,33]` exited 0 with `#Top`; see
[`audit-witness-spec.k`](evidence/artifacts/audit-witness-spec.k) and
[`04-kprove-ground-witnesses.log`](evidence/logs/04-kprove-ground-witnesses.log).
Those outputs agree with both Python implementations and with the symbolic
postcondition after ground substitution.

## 5. Rule-by-rule static soundness review

### Scope of the inventory

There is no candidate-generated `semantic.k` in this supplied-semantics
condition, and there are no proof-local K helpers imported by the positive
definition other than `verification.k`. The trusted semantics manifest contains
227 `syntax` declaration starts, 695 rule starts, five explicit contexts, and
one configuration across its modules. A complete line-start inventory and a
solution execution-slice map are preserved in
[`05-k-inventory-success.log`](evidence/logs/05-k-inventory-success.log).

The supplied tree is the trusted selected semantics level. I reviewed all
proof-local declarations and rules below, and traced every construct used by
`solution.mpy` through the relevant supplied declarations and rules. Candidate
mutation files are not imported by `VERIFICATION` and contribute nothing to
positive closure. An earlier reviewer inventory command had a malformed final
search regex and exited 2 after producing a partial listing
([`05-k-inventory.log`](evidence/logs/05-k-inventory.log)); the corrected
inventory exited 0 and supersedes it.

### Exhaustive proof-local declaration inventory

All nine local symbols are `[function, total]`:

| Symbol | Result / arguments | Additional attributes | Role |
|---|---|---|---|
| `oddDigits(Int)` | `Bool` | `no-evaluators` | mathematical digit predicate |
| `positiveInts(ValSeq)` | `Bool` | none | formal input-domain predicate |
| `filterOddDigits(ValSeq)` | `ValSeq` | none | initializes the stable filter |
| `filterOddAcc(ValSeq,ValSeq)` | `ValSeq` | `no-evaluators` | filter accumulator |
| `#digitCondition` | `Expr` | none | exact AST alias |
| `#digitBody` | `Stmts` | none | exact AST alias |
| `#outerBody` | `Stmts` | none | exact AST alias |
| `#uniqueDigitsBody` | `Stmts` | none | exact AST alias |
| `projectIntTotal(Val)` | `Int` | none | total sort projection |

There are no local `[functional]` declarations, no local `symbol(...)`
declarations, and no opaque local value oracle. `no-evaluators` controls
backend evaluation but does not leave these functions unconstrained because
each has explicit exhaustive equations over its use domain.

### Exhaustive proof-local rule inventory and decisions

| Location | Rule | Static decision |
|---|---|---|
| `verification.k:27-29` | `oddDigits(0) => true` | Correct base case after all digits are consumed. |
| `:30-32` | positive, even parity → false | Correct: a positive integer's parity is its last decimal digit's parity. |
| `:33-36` | positive, odd parity → recurse on quotient by 10 | Correct and descending: for positive `N`, the new value is `N // 10 < N`. |
| `:37-39` | negative → false | Completes totality; entry claims exclude negatives. |
| `:43` | `projectIntTotal(I:Int) => I` | Exact identity on the bridge/use domain. |
| `:44` | other `Val` → 0 `[owise]` | Disjoint totalization. It is not used to replace a non-integer program value because the bridge requires `isInt(V)` and entry/filter preconditions require integers. |
| `:46` | `positiveInts(.ValSeq) => true` | Correct empty-list case. |
| `:47-50` | cons is integer, positive, and recursive rest | Correct exact formalization of a finite list of positive integers. |
| `:52` | initialize `filterOddAcc(.ValSeq, VS)` | A definitional wrapper, not an execution shortcut. |
| `:54-55` | empty filter remainder returns accumulator | Correct base case. |
| `:56-61` | odd-digit head appends projected integer | Correct stable inclusion; projection is identity under `positiveInts`. |
| `:62-65` | non-odd head skips it | Complementary and disjoint with the preceding rule. |
| `:68-69` | `#digitCondition` expansion | Exact AST from `solution.mpy`. |
| `:71-75` | `#digitBody` expansion | Exact AST and statement order. |
| `:77-83` | `#outerBody` expansion | Exact reset, copy, while, and conditional append. |
| `:85-92` | `#uniqueDigitsBody` expansion | Exact initialization, outer loop, in-place sort, and return. |
| `:102-112` | integer loop-yield normalization, priority 40 | Sound operational bridge; detailed below. |

The four `oddDigits` guards partition all integers. The positive even/odd
guards do not overlap, and the recursive rule descends. The three
`filterOddAcc` cases cover empty and cons sequences; on a cons,
`oddDigits(...)` and its Boolean negation are disjoint and exhaustive, and
recursion removes one element. Thus the `[total]` declarations are justified
on their declared algebraic domains. All seven `[simplification]` rules are
ordinary true equations, not task-answer axioms.

The total non-integer projection may look broad, but it defines a new helper
rather than asserting a false fact about a pre-existing operation. Its
property-bearing uses are guarded by integer preconditions. In particular,
the operational bridge cannot turn a non-integer yield into zero.

### Operational bridge audit

The bridge matches:

```text
#iterYield(V, REST) ~> #loopStep(Name(X), B) ~> CONT
```

under `isInt(V)`. It rewrites this to:

```text
#bindTgt(Name(X), projectIntTotal(V))
~> B
~> #loopLbl(#loop(REST, Name(X), B))
~> CONT
```

The fixed supplied rule at `semantics/controls.k:73-74` has exactly the same
matched continuation, binding, body, loop continuation, and framed suffix,
except it passes `V` directly. On the bridge guard,
`projectIntTotal(V) = V`. Neither rule reads or changes a non-`k` cell at this
step; the subsequent target binding performs the same scope update in both.
The priority changes which identical transition fires but does not broaden it
to a different target, value sort, body, or control context.

The bridge-free `loop-yield-int` connection theorem is quantified over
`N:Int`, `REST`, `X`, `B`, and the arbitrary trailing computation and closes
under fixed semantics. A fresh immediate-continuation witness additionally
binds `n = 1`, completes the remaining empty loop, and then performs the
observable assignment `marker = 7`; it closes under the bridge-free definition
([`audit-bridge-context.k`](evidence/artifacts/audit-bridge-context.k),
[`04-kprove-bridge-continuation.log`](evidence/logs/04-kprove-bridge-continuation.log)).
The opposite interpretation, yield 1 but bind `n = 2`, exits 1 with a genuine
stuck final scope containing `n = 1`
([`05-kprove-wrong-yield-value.log`](evidence/logs/05-kprove-wrong-yield-value.log)).

This bridge is an exact normalization, not a result-bearing oracle or a
program-body bypass.

### Supplied-semantics execution slice

Every submitted construct has both syntax and an execution route:

| Submitted construct | Supplied source and behavior |
|---|---|
| `Module`, statement sequence | `syntax.k:56-61`; `core.k:124-127` loads and sequences |
| literals and names | `syntax.k:9-13`; `core.k:131-154,193-196` |
| `FuncDef`, call, return | `functions.k:14-16,63-90`; `call.k:19-21,69-74` |
| `Assign` | strict RHS in `syntax.k:41`; state update in `controls.k:9-18` |
| empty `ListExpr` and allocation | `list.k:13-15`; `core.k:117-121` |
| `For` over input list | strict iterable in `syntax.k:45`; dereference and loop in `controls.k:69-74,106-108`; list iteration in `list.k:9-10`; target binding in `tuple.k:31-41` |
| `While` | `controls.k:77-82`, with truthiness from `core.k:198-205` |
| `%`, `//`, `>`, `==` | ordered evaluation in `syntax.k:15` and `operators.k:14-17`; integer cases in `int.k:15-27` |
| `If` | strict condition in `syntax.k:49`; branch rules in `controls.k:51-54` |
| `Attribute` and `Call` | receiver/callee/arguments evaluated in order by `syntax.k:29`, `call.k:16-24`, and `core.k:183-191` |
| `result.append(n)` | priority-40 in-place heap update in `list.k:53-55` |
| `result.sort()` | priority-40 in-place heap update in `sort.k:39-42` |

The standard configuration contains the `k`, environment, scopes, allocation
counters, heap, call stack, return, exception, and exit-code cells. The entry
claim starts from the standard module scopes and empty heap. The empty result
list allocates at heap location 0; append and sort mutate that same object;
the function call pushes and then pops one scope frame; returned list objects
remain allocated; the final stack/return/exception/exit cells are fixed.

There is no binding ambiguity: `#loadAll` puts the exact `unique_digits`
closure in module scope 0, the call resolves that binding, and the method
dispatch rules select the fixed `append` and `sort` operations on the result
reference. Evaluation is left-to-right where the program needs it. On the
positive-integer domain there is no division by zero, failing lookup,
exceptional control flow, or unmodeled used construct.

### Opaque primitive and warnings

`sortVS` is declared in the trusted semantics as
`[function,total,symbol(sortVS),no-evaluators]`. Ground integer sequences have
concrete insertion-sort equations (`sort.k:20-24`), while a symbolic sequence
remains opaque in the Haskell proof. This is an acceptable external primitive
boundary because sorting is a fixed supplied built-in, not program-defined
code, and the source visibly calls `.sort()`. It is nevertheless
result-bearing: the entry postcondition depends on the stated contract that
`sortVS` is ascending sort. The target K proof does not prove independent
sortedness and permutation predicates.

The fresh LLVM build reports non-exhaustive-match warnings for several
supplied-semantics total helpers such as `mapStrVS`, `floorFI`, and
`valSeqAt`. None is reached by this submitted program or used by the proof
summaries. I do not label those globally unsound: no concrete or symbolic
false conclusion witness was found, and the narrower fact is only that their
unused out-of-slice totality was not independently established in this audit.

No proof-local rule was found unsound, so there is no unsoundness allegation
requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh reviewer mutation
[`audit-vacuity.k`](evidence/artifacts/audit-vacuity.k) uses the first prompt
example but changes the result-bearing heap obligation from the true
`[1,15,33]` to `[1,15]`, deliberately dropping 33.

The precondition is demonstrably satisfiable: all four inputs are positive
integers. The independent witness script reports:

```text
mutated_result=[1, 15]
canonical_result=[1, 15, 33]
candidate_result=[1, 15, 33]
mutation_is_false=True
```

See [`06-mutation-witness.log`](evidence/logs/06-mutation-witness.log).
`kprove --dry-run` exited 0, establishing that the mutation parses and builds
against the fresh definition
([`06-mutation-dry-run.log`](evidence/logs/06-mutation-dry-run.log)).

The actual proof exited 1 with `WarnStuckClaimState`. Its residual is a fully
executed final configuration with `ref(0)` returned and heap 0 containing
exactly `vCons(1, vCons(15, vCons(33, .ValSeq)))`, which cannot unify with the
mutated two-element list. This is the expected unmet result obligation, not a
parser error, missing import, timeout, unrelated crash, or unreachable
mutation. See
[`06-mutation-kprove.log`](evidence/logs/06-mutation-kprove.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every finite MPY `ValSeq` whose elements are all integers greater than
zero, if execution terminates under the supplied MPY semantics, the exact
submitted `unique_digits` body, called from the standard initial
configuration on `list(VS)`, returns reference 0 to a heap list equal to:

```text
sortVS(filterOddDigits(VS))
```

Here `filterOddDigits` is the explicitly defined stable filter that retains
exactly the values accepted by `oddDigits`. The proof also fixes successful
control state: empty call stack, `noRet`, `NoExc`, and exit code 0. The loop
claims machine-check the inner digit scan and outer filtering execution; the
bridge-free theorem connects the only operational normalization to the fixed
semantics.

This is a partial-correctness statement. Termination for finite lists of
positive integers is straightforward informally—the outer remainder shrinks,
and positive `y` decreases to zero by division by 10—but termination is not
being reported as a separately formalized total-correctness theorem.

### Trust ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| Trusted supplied MPY semantics and K built-ins for unbounded integers, Booleans, maps, lists, rewriting, and proof execution | All modeled execution and proof checking | Required selected semantics level; candidate tree is byte-identical to trusted mount; rebuilt with K v7.1.293. |
| Proof-local `oddDigits`, `positiveInts`, `filterOddDigits`, `filterOddAcc`, and `projectIntTotal` equations | Preconditions and final filtered sequence | Not opaque assumptions. Exhaustive, disjoint, descending equations were statically checked; loop claims connect them to exact execution. |
| Integer loop-yield normalization | Loop binding and control | Machine-checked bridge-free connection theorem plus continuation and opposite-value witnesses. |
| `sortVS` contract | Final result ordering | Fixed external primitive of supplied semantics. Ground int equations and 64 fresh K oracle assertions support it; symbolic sortedness/permutation is not proved by the target claim. |
| `oddDigits` means “all decimal digits are odd” | Human-facing filtering intent | Informal arithmetic induction: parity classifies the last decimal digit and quotient-by-10 removes it. Supported, not replaced, by 4,278 fresh Python differential cases and ground K witnesses. |
| Trusted translator | Python-to-MPY program identity | Candidate translator is trusted-byte-identical; submitted `.mpy` regenerates byte-for-byte. |
| Canonical Python implementation | Executable intent oracle | Trusted input used only for finite differential evidence, not as a K axiom or proof substitute. |

The broad Python differential tests establish candidate/canonical agreement on
their recorded finite input set. The 64 K assertions separately exercise the
actual translated body and the concrete supplied semantics, including sort.
Neither finite result supplies a universal connection theorem for the English
contract or for symbolic `sortVS`; the universal execution statement comes
from the K reachability proof and remains conditional on the trusted supplied
primitive's contract.

### Gate and decision summary

- **Real-program soundness:** pass. The exact body executes; all
  property-bearing summaries are connected through loop claims; the sole
  operational bridge is exact; the result is fixed; concrete preconditions are
  realizable; and the fresh false result is rejected for the expected reason.
- **Intent adequacy:** pass with a documented limitation. The positive-integer
  formal domain exactly matches the prompt, and the recursive filter matches
  the requested behavior, but the decimal-property explanation and opaque
  sort contract are not separately stated as machine-checked high-level
  predicates.
- **Trust and auditability:** pass. Every command used for the judgment,
  including non-zero diagnostics and expected failures, has an exact bounded
  log; test scripts and inputs are preserved. Finite evidence is not described
  as proof.

There is no material adequacy gap, substituted program, vacuity, failed clean
reconstruction, or materially unsound rule. The remaining limitations are
precisely the kind of sound-but-informally-bridged evidence boundary assigned
`CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
