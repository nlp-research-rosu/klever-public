# Independent adversarial audit: 34-unique

## Outcome

The candidate contains a legitimate, freshly reconstructible partial-correctness
proof of the submitted program under the supplied MPY semantics. The proof is
not vacuous, its recursive summaries are connected to fixed execution, and its
entry postcondition constrains the returned heap object.

I assign concerns rather than an unqualified pass for two limitations:

1. the natural-language meaning of the final `sorted` call is conditional on
   the supplied semantics' result-bearing opaque primitive `sortVS`; the K proof
   establishes `sortVS(uniqueAcc(INPUT, .ValSeq))`, not independent ordering and
   permutation predicates; and
2. four required candidate provenance files are absent, although direct trusted
   comparisons and clean reconstruction were still possible.

Neither limitation lets the candidate prove a false result or bypass the
submitted body. All builds and experiments were performed in
`/tmp/audit-work/34-unique`; `/candidate` was read only. Evidence is indexed in
`/audit-output/evidence/README.md`.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
infrastructure-mode contradiction and a candidate verdict is appropriate.

A recursive, no-symlink-following diff between the candidate and trusted
semantics trees returned zero. Their entry sets and file types also match, and
the candidate tree contains no symlinks. Thus there are no missing, additional,
changed, mistyped, or symlinked entries inside
`/candidate/reference-semantics`. See
`evidence/01-provenance-integrity.log`.

The candidate copies of the prompt and translator are byte-identical to their
trusted mounts:

- `prompt.py`: SHA-256
  `c48cad1505632ee1c7534d4b5dc430767155942186f1f0eb2c3e46074c1111a6`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Missing and untrusted artifacts

The following required provenance artifacts are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

No structured generation trace is present. No `PROOF.md` or candidate
`spec-vacuity.k` is present either. The latter two are not needed to reconstruct
the proof, but their absence means there was no candidate-authored validation
record to audit.

I read the available `prove.sh`, `prove.log`, `concrete_tests.py`, and
`concrete-tests.mpy` only as untrusted claims. In particular, the `#Top` in
`prove.log` was not accepted. The candidate's `__pycache__` and `.pyc` were
ignored. The scratch-source identity and ignored-cache inventory are in
`evidence/23-scratch-source-manifest.log`.

The missing provenance files are an auditability/integrity concern, but they do
not create uncertainty about the actual prompt, translator, semantics, program,
or proof sources because those were compared directly to the trusted mounts and
rebuilt independently.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and algorithms

From `/reference/prompt.py`, the contract is: `unique(l)` returns the sorted
unique elements of `l`; the documented example maps
`[5, 3, 5, 2, 3, 3, 9, 0, 123]` to
`[0, 2, 3, 5, 9, 123]`.

The trusted canonical implementation in `/reference/canonical.py` computes
`sorted(list(set(l)))`. The submitted `/candidate/solution.py` instead scans
left to right, appends an element only if it is not already in `result`, and
then calls `sorted(result)`. On ordinary finite lists of mutually comparable,
hashable values—and in particular the integer domain evidenced by the prompt
and supplied sort semantics—the latter computes the same value. It is a
different but valid algorithm. Inputs containing custom or unhashable objects
are outside the canonical implementation's reliable domain and are not claimed
by this audit.

### Translator fidelity

Running the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to submitted `solution.mpy`; both hashes are
`f127bbe2851b4c49afff06bb7e96bd30c6d76455c05617f66d0d687c73242411`.
The exact command, hashes, `cmp` result, and exit status are in
`evidence/02-translator-regeneration.log`.

The translated AST is faithful:

- initialize `result` with `ListExpr`;
- iterate `item` over `l`;
- execute `result.append(item)` only under `item not in result`;
- return `sorted(result)`.

### Independent differential

`evidence/differential_unique.py` independently imports
`/reference/canonical.py:unique` and the scratch copy of the submitted
`solution.py:unique`. It does not reuse proof equations. Its exact input corpus
is preserved in `evidence/differential-inputs.json`.

The run covered:

- 15 documented and boundary cases, including empty, singleton, duplicate,
  both membership branches, sorting reversal, negative and unbounded integers,
  strings, and tuples;
- every integer list of lengths 0 through 5 over
  `[-2, -1, 0, 1, 2]` (3,906 cases);
- 250 deterministic random integer lists of lengths 0 through 40, seed
  `340034`.

All 4,171 cases matched. The log also records both Python results for `[]`,
`[1]`, `[2, 1, 2]`, and the documented example. See
`evidence/03-python-differential.log` (`mismatch_count=0`, exit 0).
This is finite implementation-to-canonical evidence, not a universal proof.

## 3. Clean proof reconstruction

### Fresh definitions

K v7.1.337 was available independently at `/usr/bin`; versions are recorded in
`evidence/00-tool-versions.log`. Only source files were copied into scratch.
Candidate-provided caches and prior output were not reused.

The following fresh builds succeeded:

| Purpose | Fresh command | Evidence |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled` | `evidence/05-kompile-concrete.log`, exit 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module UNIQUE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled` | `evidence/07-kompile-proof.log`, exit 0 |

The reviewer-authored concrete program
`evidence/k_concrete_tests.py` was translated with the trusted translator. It
asserts the correct result on empty, singleton, duplicate-only, reversed,
negative/duplicate, and documented inputs. `krun` reached a normal final
configuration with `.K`, `NoExc`, exit code 0, and process exit 0. See
`evidence/04-k-test-translation.log` and
`evidence/06-krun-concrete.log`.

### Positive claims

The claims have a genuine dependency order: `unique-loop` uses the independently
proved membership summary, and `unique-correct` uses both helper claims. I
therefore ran dependency-preserving tiers, in addition to the aggregate proof:

| Target tier | Claim selection | Result |
|---|---|---|
| Membership | `UNIQUE-SPEC.member-summary` | `#Top`, exit 0 (`evidence/08-kprove-member-summary.log`) |
| Loop with proved dependency | `UNIQUE-SPEC.member-summary,UNIQUE-SPEC.unique-loop` | `#Top`, exit 0 (`evidence/11-kprove-loop-with-dependency.log`) |
| Entry with both dependencies | all three labels | `#Top`, exit 0 (`evidence/12-kprove-entry-with-dependencies.log`) |
| Candidate target module as submitted | no label filter | `#Top`, exit 0 (`evidence/13-kprove-all-claims.log`) |

An additional loop-only diagnostic selected only `unique-loop`. Inspection of
its generated `spec.kore` showed that `--claims` had removed
`member-summary`, so the prover was left recursively exploring membership over
an abstract accumulator. I interrupted that dependency-stripped diagnostic; it
is preserved and explicitly excluded in
`evidence/09-kprove-unique-loop.log`. This is neither a failed submitted claim
nor verdict evidence.

The compiler emitted fixed-semantics warnings about non-exhaustive total
functions such as `mapStrVS`, several float conversions, `joinCodes`, and
`valSeqAt`, plus unused pattern variables in `strLt`. None of those
non-exhaustive functions is on this program's proof path. They remain narrower
fixed-semantics coverage limitations, not candidate unsoundness or proof
failure.

## 4. Adequacy and real-program pinning

### Claim meanings

`member-summary` (`spec.k:6-10`)

- Precondition: the current computation is the fixed-semantics membership fold
  `#memberAcc(V, list(VS))`, followed by an arbitrary continuation.
- Postcondition: that fold is replaced by the fully defined Boolean
  `memberVS(V, VS)`, with the same continuation and all state framed.
- It is a universal connection claim for the fixed membership computation, not
  an assumed rule.

`unique-loop` (`spec.k:12-28`)

- Precondition: execution is at the real `#loop` over `list(INPUT)`, with target
  `item`, the exact submitted loop body abbreviation, a current frame containing
  `l`, `result -> ref(H)`, and an old `item`, and heap object `H` containing
  accumulator `ACC`.
- Postcondition: the loop is consumed, `result` contains
  `uniqueAcc(INPUT, ACC)`, `item` is the final visited item (or stays old on
  empty input), and the arbitrary continuation resumes.
- Other scopes, heap entries, and omitted cells are framed. The body has no
  return, break, exception, or other abrupt control, so an arbitrary
  continuation is safe here.

`unique-correct` (`spec.k:29-62`)

- Precondition: the standard module/builtins initial configuration loads a
  module defining `unique` and then executes
  `answer = unique(list(INPUT))`; `INPUT` is an arbitrary MPY `ValSeq`.
- Postcondition: module binding `unique` is the expected closure, `answer` is
  `ref(1)`, heap object 0 contains the first-seen deduplicated accumulator, heap
  object 1 contains `sortVS` of that accumulator, allocations advance from 0 to
  2, and stack, return, exception, and exit cells are normal.

The result is not a free variable, implication-only placeholder, or tautology:
the observable `answer` reference and its exact heap value are fixed.

### Actual submitted program

The entry claim uses proof-local `uniqueBody` and the loop claim uses
`uniqueLoopBody`. These are transparent, total syntactic abbreviations:

- `uniqueLoopBody` expands exactly to the submitted `If(item not in result,
  result.append(item), empty-else)` AST;
- `uniqueBody` expands exactly to the submitted initialization, `For`, and
  `Return(sorted(result))` AST.

They introduce no operational rewrite that can preempt the actual AST.
Translator regeneration established the submitted AST, and the rule equations
in `verification.k:33-44` are textually the same AST with explicit empty list
tails.

As an additional pinning check,
`evidence/spec-ground-witnesses.k` contains an entry claim with the literal
submitted body, not `uniqueBody`. On input `[2, 1, 2]`, it proves the exact final
heap objects `[2, 1]` and `[1, 2]`. It returned `#Top`, exit 0, in
`evidence/20-ground-literal-entry.log`.

### Satisfying states and substitutions

Every claim precondition has a concrete witness:

- membership: `V=2`, `VS=[1,2,1]`;
- loop: environment 1, result heap 0 initially `[9]`, old item 99, and loop
  input `[2,1,2]`;
- entry: the exact standard initial module configuration and input `[2,1,2]`.

The first two ground claims also returned `#Top`, exit 0
(`evidence/18-ground-member.log` and `evidence/19-ground-loop.log`). The loop
ground result is accumulator `[9,2,1]` and final `item=2`, exactly matching the
formal summary.

Substituting `[2,1,2]` into the entry result yields:

1. `uniqueAcc([2,1,2], []) = [2,1]`;
2. the supplied sort operation yields `[1,2]`;
3. both trusted canonical Python and submitted Python return `[1,2]`;
4. the literal K entry witness returns `[1,2]`.

The same comparison is recorded for empty, singleton, and documented inputs in
`evidence/03-python-differential.log` and the concrete K run.

The formal `INPUT:ValSeq` is broader than the well-evidenced ordinary integer
domain. This does not create a false K theorem—the postcondition remains in
terms of the fixed semantics' equality and `sortVS`—but conclusions about full
Python behavior for exotic values are outside the evidence.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` extracted complete, line-bounded statements from every
`.k` file in the supplied semantics tree, `verification.k`, and `spec.k`.
`evidence/10-k-rule-inventory.md` preserves each statement verbatim and
classifies it. Totals are:

- 233 syntax declarations;
- 152 declarations with `function`, 113 with `total`, and none with
  `functional`;
- 25 declarations with explicit `symbol(...)`;
- one configuration and five evaluation contexts;
- 706 rules: 703 ordinary and three simplification rules;
- 49 rules carrying explicit `priority(...)`;
- three reachability claims.

The three simplification rules are exactly the candidate's `memberVS`
equations. The candidate adds no priority rule and no opaque symbol.

### Per-file disposition

The exhaustive artifact gives every rule and source line. The following table
records the static decision for every file-level inventory; “inactive” is not
used to excuse a known false rule—no concrete or symbolic false-conclusion
witness was found in the scan.

| File | Inventory | Role and decision |
|---|---:|---|
| `semantics/syntax.k` | 16 syntax | Declares every submitted AST constructor. No equations. |
| `semantics/core.k` | 37 syntax, 46 rules, 1 configuration | Active loading, sequencing, allocation, lookup, builtins scope, argument order, and shared sequence helpers. Constructor cases and guarded priorities are disjoint; state changes match the used subset. |
| `semantics/iter.k` | 1 syntax | Iterator protocol declaration only. |
| `semantics/list.k` | 5 syntax, 27 rules | Active list construction, iteration, membership, concatenation, and append. Membership uses the same `==K` test as `memberVS`; append updates only the referenced heap list. |
| `semantics/tuple.k` | 4 syntax, 21 rules | Only name-target binding is active. It updates the current scope exactly as the loop claim records; other tuple rules do not match. |
| `semantics/operators.k` | 10 rules, 2 contexts | Active left-then-right compare evaluation and list-membership dispatch. Ref priorities do not change the submitted bare-list harness. |
| `semantics/controls.k` | 3 syntax, 34 rules | Active `Assign`, `Expr`, `If`, and `For` cases preserve evaluation order and loop control. The submitted body contains no abrupt control. Other control constructs are disjoint. |
| `semantics/functions.k` | 4 syntax, 15 rules | Active ordinary definition, parameter binding, return, frame pop, and default return. Frame allocation/deallocation and return reference preservation match the entry postcondition. Annotated-closure cases do not match. |
| `semantics/call.k` | 3 syntax, 21 rules | Active callee-first then left-to-right argument evaluation, ordinary closure call, bound append, and builtin `sorted` dispatch. Priority rules dereference exactly the receiver/argument positions documented by the fixed semantics. |
| `semantics/sort.k` | 6 syntax, 19 rules | Active unkeyed `sorted` allocation. Ground int/string insertion equations are truthful; symbolic `sortVS` is intentionally opaque and is accounted for as trust, not as a candidate lemma. Keyed/reverse cases do not match. |
| `semantics/int.k` | 1 syntax, 16 rules | Standard integer operations; the program has no arithmetic. Ground sorting uses K integer comparison directly. No overlap affecting the proof. |
| `semantics/str.k` | 5 syntax, 28 rules | Ground string ordering supports concrete string tests; otherwise inactive. Recursive lexicographic guards are disjoint. |
| `semantics/builtins.k` | 38 syntax, 137 rules | Registry implementations are fixed semantics. The generic builtin rule is `owise` to the active `sorted` rule. Other builtins, including opaque MD5, do not match the program. |
| `semantics/methods.k` | 27 syntax, 75 rules | Method function namespace is imported; list append itself is in `list.k`. Other method equations do not match. Guarded recursive helpers were scanned without a false witness. |
| `semantics/bool.k` | 13 rules, 1 context | Standard truth and Boolean operator cases; only Boolean `If` consumption is indirectly relevant. |
| `semantics/assert.k` | 3 rules | Concrete smoke-test assertions only; excluded from the Haskell proof path and used normally by reviewer concrete tests. |
| `semantics/concrete.k` | 5 syntax, 16 rules | Imported only by `MPY-KRUN`; used for concrete-only deep equality/keyed sorting, neither of which affects the symbolic proof. |
| `semantics/comprehension.k` | 3 syntax, 7 rules | No matching submitted syntax. |
| `semantics/dict.k` | 12 syntax, 28 rules | No matching submitted syntax. |
| `semantics/float.k` | 34 syntax, 121 rules | No float input operation is used by the proof. Its opaque symbols and compiler totality warnings are inactive trust/coverage boundaries. |
| `semantics/range.k` | 2 syntax, 6 rules | No matching submitted syntax. |
| `semantics/set.k` | 6 syntax, 12 rules | The submitted implementation deliberately does not execute `set`; no matching syntax. |
| `semantics/subscript.k` | 15 syntax, 40 rules, 2 contexts | No subscript occurs; the warned empty-sequence `valSeqAt` coverage gap is not result-bearing here. |
| `semantics.k` | imports/modules only | Assembles the exact trusted tree. The Haskell proof imports `MPY`, not concrete-only `MPY-CONCRETE`; LLVM imports `MPY-KRUN`. |
| `verification.k` | 6 syntax, 11 rules | All candidate-local extensions are reviewed below; no opaque or operational rule. |
| `spec.k` | 3 claims | All three close under fresh reconstruction and are adequate as described above. |

The fixed tree contains many generic rules because it models more programs than
this one. I checked constructor separation, guarded overlap, recursive descent,
and priority interactions for the active path. The compiler's non-exhaustive
totality warnings identify genuine but inactive coverage gaps; without a false
conclusion witness on this intended input path, I do not label them unsound.

### Submitted construct-to-rule map

| Submitted construct | Declaration and controlling rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, `Params`, `Name` | `syntax.k:9-13,53-60`; `functions.k:14-16`; `core.k:130-154` |
| `Assign` | `syntax.k:41`; `controls.k:9-18` |
| `ListExpr` | `syntax.k:17`; `list.k:13-15`; allocation at `core.k:117-121` |
| `For` and target `item` | `syntax.k:45`; `controls.k:62-74`; list iteration at `list.k:9-10`; name binding at `tuple.k:30-41` |
| `If` | `syntax.k:49`; `controls.k:50-54` |
| `Compare(..., "not in", ...)` | `syntax.k:30-32`; evaluation contexts at `operators.k:14-17`; list fold at `list.k:57-67` |
| `Attribute(..., "append")`, `Call`, `Expr` | `syntax.k:28-29,52`; `call.k:15-24,52-67`; `list.k:52-55`; discard at `controls.k:46-48` |
| `Return(sorted(...))` | `syntax.k:50`; builtins binding at `core.k:156-181`; call order at `core.k:183-191` and `call.k:18-32`; sort allocation at `sort.k:34-37`; return/pop at `functions.k:77-90` |

This mapping covers every constructor in submitted `solution.mpy`; there is no
fabricated rule for an unmodeled used construct.

### Candidate-local extension decisions

All 11 local equations are definitional:

1. `memberVS(_, .ValSeq) = false`;
2. equal head gives `true`;
3. unequal head recurses on the tail;
4. `addUnique` returns the accumulator when membership is true;
5. otherwise it appends one value;
6. `uniqueAcc` on empty input returns the accumulator;
7. on a cons it recurses on the strict tail using `addUnique`;
8. `lastItem` on empty input returns the old value;
9. on a cons it recurses on the strict tail with the head as new old value;
10. `uniqueLoopBody` expands to the exact submitted `If`;
11. `uniqueBody` expands to the exact submitted body.

For each constructor-recursive function, base and recursive cases are disjoint
and recursive calls decrease the algebraic sequence. The two guarded
`addUnique` equations are exhaustive and disjoint because `memberVS` is total.
The equal-head and unequal-head membership equations agree with fixed
membership's `==K`. No pair has conflicting right-hand sides on an overlap.
`[total]` does not hide an uncovered reachable case.

The two body abbreviations name syntax; they do not replace execution. The
result-bearing `uniqueAcc` is fixed by exhaustive equations rather than an
oracle. It is connected to real loop execution by the independently closing
`unique-loop` claim.

### Auxiliary claims as connection theorems

`member-summary` is bridge-free: it starts at the fixed `#memberAcc` redex,
unfolds fixed iterator/equality rules, and its structural circularity consumes
a list head before recurring. The fold reads no observable cell, so its
arbitrary continuation is contained in its justification scope.

`unique-loop` also starts at the fixed `#loop` redex. Its matched context pins
the active continuation, environment, exact local frame bindings, parent, and
result heap object. Its state footprint is:

- read: loop sequence, current frame, accumulator heap object;
- write: `item` and that accumulator heap object;
- preserve: environment identity, frame parent and other scope/heap entries,
  allocation counters, call stack, return/exception/exit state, and
  continuation.

It executes fixed target binding, membership, condition, and append before
using a structurally smaller circularity. There is no return/frame pop,
exception, break, cleanup, allocation, or continuation discard in the body.
Thus its arbitrary `CONT` is not broader than the connection theorem.

The independent operational-sensitivity test changes the real loop body to
append every item while retaining the original unique result obligation. On
input `[1,1]`, fixed execution reaches heap `[1,1]`; `kprove` rejects the
original `[1]` summary with a meaningful stuck residual. The mutated spec builds
successfully (`evidence/21-operational-sensitivity-dry-run.log`, exit 0) and the
proof fails as expected (`evidence/22-operational-sensitivity-proof.log`, exit
1). This is separate from the false-postcondition test.

No rule in `verification.k` is an operational bridge, no program-defined
operation is replaced by an unconstrained oracle, and no task answer is encoded
as an axiom. I found no unsound candidate rule; consequently there is no
unsoundness allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on candidate evidence. The fresh mutation is preserved as
`evidence/spec-vacuity.k`.

It fixes the satisfying input to `[1]`, leaves the submitted body and all normal
final-state obligations unchanged, and changes only the result-bearing heap
object from `[1]` to `[]`.

- Parsing/proof preparation succeeded with `--dry-run`, exit 0:
  `evidence/14-vacuity-dry-run.log`.
- The real proof returned exit 1 with `WarnStuckClaimState`:
  `evidence/15-vacuity-proof.log`.
- The residual is fully executed (`<k> .K </k>`) and shows
  `1 |-> list(vCons(1, .ValSeq))`, directly contradicting the mutated
  `1 |-> list(.ValSeq)` destination.

This is a reachable unmet result obligation, not a parser error, missing import,
timeout, unrelated crash, or dead mutation. It demonstrates that the successful
entry proof discriminates the returned value.

An initial reviewer draft of the separate ground-witness file had an explicit
empty-list parse spelling error; it is transparently preserved in
`evidence/16-ground-witnesses-dry-run.log`. The corrected artifact built
(`evidence/17-ground-witnesses-dry-run.log`) before any ground result was used.
That reviewer drafting error is unrelated to the non-vacuity mutation.

## 7. Proven versus assumed accounting

### What the proof establishes

Under the exact supplied MPY theory, for every finite symbolic
`INPUT:ValSeq`, executing the submitted `unique` body from the entry
configuration reaches a normal final configuration in which:

- the first allocated list is
  `uniqueAcc(INPUT, .ValSeq)`;
- `answer` points to the second allocated list;
- that second list is
  `sortVS(uniqueAcc(INPUT, .ValSeq))`;
- scope/heap counters, call stack, return, exception, and exit state have the
  exact values in `unique-correct`.

The membership and loop summaries used to establish that result are themselves
machine-checked reachability claims over fixed execution. This is a
partial-correctness statement in the Kit sense; the report does not promote
candidate logs, traces, or differential tests into proof rules.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.337 compiler and Haskell/LLVM backends | Parses, compiles, executes, and proves all K artifacts | Necessary low-level tool trust; fresh builds and exact statuses reduce, but cannot eliminate, implementation trust. |
| Exact supplied MPY semantics | Defines the execution model used by every claim | Authoritative for `SUPPLIED_SEMANTICS`; recursive tree identity was established. Its Python subset and inactive totality warnings are explicit limitations. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable mounted translator boundary; byte-identity regeneration pins the submitted AST. |
| K builtins (`==K`, maps, integer/Boolean/string operations) | Equality, guards, maps, and ground arithmetic throughout semantics | Ordinary foundational semantics trust. No candidate redefinition or conflicting local equation was found. |
| `sortVS(ValSeq)` | Determines the final returned value and the natural-language “sorted” meaning | Fixed external builtin boundary, not program-defined code. Ground int/string equations and concrete execution support it, but the symbolic proof treats it as opaque. Any claim that the output is ascending and a permutation is conditional on the supplied `sortVS` contract. This is the principal concern. |
| `uniqueAcc`/`addUnique` meaning “first-seen unique elements” | Connects the execution summary to “unique” | Not opaque: exhaustive recursive equations plus the proved loop connection fix its value. The set/no-duplicates interpretation is an ordinary structural induction, not a separately stated K predicate. Acceptable, but part of the informal intent bridge. |
| Trusted canonical Python entry point | Oracle for implementation-to-reference comparisons | Finite empirical support only. It is independent of K equations and reported as 4,171 tests, not as a universal theorem. |
| Intended input-domain bridge | Relates MPY `ValSeq` and the broad `list` annotation to ordinary Python inputs | Strongly evidenced for finite integer lists and sampled homogeneous strings/tuples. Exotic Python equality, hashing, comparison, exceptions, and custom objects are excluded. |

The supplied tree has 25 explicit opaque symbols:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. The exhaustive declarations are in
`evidence/10-k-rule-inventory.md`. Only `sortVS` is reachable from the submitted
program and appears in the target postcondition. The other 24 cannot affect
control, state, exceptions, or result for this AST.

### Final decision

Real-program soundness passes: fresh proof closure, exact body expansion,
literal-AST ground execution, connection claims, operational sensitivity, and
false-result rejection all agree. The candidate neither substitutes another
program nor smuggles the answer through an unsound rule.

Intent adequacy is legitimate but conditional: transparent `uniqueAcc`
equations and broad differential evidence support “unique,” while “sorted” is
carried by the fixed opaque `sortVS` contract rather than independently proved
ordering/permutation predicates. Candidate-side provenance is also incomplete.
Those are documented limitations, not grounds for `NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
