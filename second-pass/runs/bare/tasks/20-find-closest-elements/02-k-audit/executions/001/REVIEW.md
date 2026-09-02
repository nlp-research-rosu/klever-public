# Independent adversarial audit: 20-find-closest-elements

## Outcome

The candidate's six submitted reachability claims rebuild cleanly, independently
print `#Top`, constrain their returned tuples, execute an exact K copy of the
submitted constructor program, and reject a fresh false-result mutation. Those
facts make the six narrow claims genuine.

They do **not** constitute a proof of the requested program contract. The only
symbolic claims cover lists of exactly two elements. Lists of length three or
more are covered only by three fixed examples, and no claim states or proves
that the returned pair minimizes distance over an arbitrary input list of
length at least two. Thus the target correctness theorem is missing. The
exact-rational input model also has no universal bridge to Python's annotated
IEEE `float` domain.

This is a candidate adequacy failure, not an infrastructure failure and not a
failure to reproduce the candidate's reported `#Top`.

## 1. Input and provenance integrity

### Rendered semantics boundary

The mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics` is absent;
there is therefore no supplied or hidden semantics baseline to compare or use.
The trusted mount contains exactly the relevant regular files
`canonical.py`, `prompt.py`, and `py2mpy.py`. This satisfies the rendered-mode
boundary. See [01-key-artifacts.log](evidence/01-key-artifacts.log) and
[01-provenance-comparison.log](evidence/01-provenance-comparison.log).

### Required artifacts and hashes

All of the following are regular files, not symlinks:

- `/candidate/run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`;
- the one structured JSONL trace below `/candidate/codex-trace`;
- `/candidate/prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
  `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

There are no candidate symlinks at depth two. The candidate prompt and
translator are byte-identical to their trusted counterparts (`cmp` status 0).
Their trusted hashes are respectively
`881d52f394307cce02e432bc6342c93bfe0f6652b203f0bf1a0fc365ed87c594`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`,
which also match `run-input.json`.

The candidate contains extra generated/build products: several
`*-kompiled/` directories, `__pycache__/`, `example.run`,
`kore-exec.tar.gz`, and generation logs/traces. They are not source integrity
failures, but none was trusted or reused. The complete top-level list is in
[01-candidate-top-level.log](evidence/01-candidate-top-level.log).
There is no candidate `PROOF.md` and no candidate `spec-vacuity.k`; neither was
treated as evidence of validity or non-vacuity.

### Untrusted generation claims

`metrics.json` claims exit 0 and no timeout. `codex-last.txt`,
`codex-output.log`, and the structured trace claim that all six claims reached
`#Top`; the generation log also records earlier parser, hook, and stuck-proof
failures before its final successful run. These were read only as claims. The
structured trace inventory is preserved in
[01-structured-trace-inventory.log](evidence/01-structured-trace-inventory.log);
fresh reconstruction is reported in Stage 3.

No missing, changed, mistyped, or symlinked required source artifact was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

The trusted prompt requires
`find_closest_elements(numbers: List[float]) -> Tuple[float, float]`.
For a supplied list of length at least two, it must return two elements having
minimum pairwise distance, ordered as `(smaller, larger)`. The trusted canonical
implementation examines every pair of distinct indices, initializes from the
first such pair, replaces the result only on a strictly smaller absolute
distance, and sorts the selected pair.

`/candidate/solution.py` uses a behaviorally equivalent quadratic traversal on
the intended domain. It initializes from indices 0 and 1, normalizes each
examined pair, visits each unordered pair once with `i < j`, and replaces the
best pair only for a strictly smaller gap. Visiting the reverse ordered pair,
as the canonical implementation does, cannot change a strict-minimum update or
tie choice.

The implementation assumes the documented length-at-least-two precondition.
For empty and singleton lists the canonical implementation returns `None`,
whereas the submitted implementation raises `IndexError`. These are recorded
differences outside the intended domain, not candidate failures on the stated
domain.

### Trusted translation

The reviewer regenerated the constructor program with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/generated-solution.mpy
```

Translation exited 0. `cmp` against the submitted scratch copy of
`solution.mpy` exited 0, and both files have SHA-256
`b55ed6ed23309810651d2a11ca145e61a0fcffac8d85a3150ccc20345c9f43ab`.
See [02-regenerate-mpy.log](evidence/02-regenerate-mpy.log).

### Independent differential execution

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical file and the scratch copy of the submitted Python file through
independent module loaders. It exercises:

- both documented examples;
- empty and singleton out-of-domain boundaries;
- length-two ordered, reversed, and equal cases;
- true and false pair-normalization branches;
- true, false, and tied best-gap updates;
- negatives, signed zero, very small/large magnitudes, infinities, and NaNs;
- 200 seeded generated inputs of lengths 2 through 10.

The run covered 215 intended-domain cases with zero mismatches. The two
out-of-domain cases produced the expected two mismatches described above.
The exact inputs, per-case results, totals, command, and exit 0 are in
[02-python-differential.log](evidence/02-python-differential.log). This is
finite program-fidelity evidence, not a proof of the algorithm or semantics.

## 3. Clean proof reconstruction

### Isolation and builds

Only `semantic.k`, `verification.k`, `spec.k`, `solution.py`, and
`solution.mpy` were copied from the candidate into `/tmp/audit-work/source`.
Trusted Python inputs were copied separately. No candidate-built definition or
cache was copied. Fresh build directories were created only below
`/tmp/audit-work/build`; the isolation record is
[03-scratch-isolation.log](evidence/03-scratch-isolation.log).

The live tools are K version `v7.1.293`. Fresh builds were:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-llvm-kompiled

kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition /tmp/audit-work/build/verification-haskell-kompiled
```

Both exited 0. See
[03-build-semantics-llvm.log](evidence/03-build-semantics-llvm.log) and
[03-build-verification-haskell.log](evidence/03-build-verification-haskell.log).

### Fresh generated-semantics execution

Reviewer-generated raw `run(Module(...), Value)` inputs are preserved in
[evidence/runtime-inputs](evidence/runtime-inputs), with their construction
script and hashes in
[make_semantic_inputs.sh](evidence/make_semantic_inputs.sh) and
[03-make-runtime-inputs.log](evidence/03-make-runtime-inputs.log).

Fresh LLVM execution produced:

| Input | Fresh K result | Python comparison |
|---|---|---|
| `[1,2,3,4,5,11/5]` | `(2,11/5)`, exit 0 | both Python bodies return `(2.0,2.2)` |
| `[1,2,3,4,5,2]` | `(2,2)`, exit 0 | both return `(2.0,2.0)` |
| `[1,2]` | `(1,2)`, exit 0 | both return `(1.0,2.0)` |
| `[2,1]` | `(1,2)`, exit 0 | both return `(1.0,2.0)` |
| `[2,2]` | `(2,2)`, exit 0 | both return `(2.0,2.0)` |
| `[-10,-3,-7/2,9]` | `(-7/2,-3)`, exit 0 | both return `(-3.5,-3.0)` |

The K logs are
[03-krun-example-six.log](evidence/03-krun-example-six.log),
[03-krun-boundary-reversed-two.log](evidence/03-krun-boundary-reversed-two.log),
[03-krun-boundary-duplicate-two.log](evidence/03-krun-boundary-duplicate-two.log),
and the Stage 4 claim logs. The independent Python comparison is
[04-claim-python-witnesses.log](evidence/04-claim-python-witnesses.log).

Loading the submitted `solution.mpy` itself also exits 0, reaches `.K`, and
registers its function body; see
[03-krun-module-load.log](evidence/03-krun-module-load.log).

The deliberately out-of-contract empty input stops at
`valueAt(vnil, 0)` with exit 113
([03-krun-boundary-empty.log](evidence/03-krun-boundary-empty.log)).
That is the generated semantics visibly stopping on an unsupported exceptional
case; it is not a parser/build failure and does not affect the stated
length-at-least-two domain.

### Fresh positive proofs

The original aggregate command:

```text
kprove spec.k \
  --definition /tmp/audit-work/build/verification-haskell-kompiled \
  --spec-module SPEC
```

exited 0 and printed `#Top`
([03-kprove-original-all.log](evidence/03-kprove-original-all.log)).

Because the claims have no source labels, the reviewer copied each exact claim
unchanged into a separate module in
[spec-independent.k](evidence/spec-independent.k). Each module was then run
separately. All six commands exited 0 and printed `#Top`:

- [claim 1](evidence/03-kprove-claim-1.log)
- [claim 2](evidence/03-kprove-claim-2.log)
- [claim 3](evidence/03-kprove-claim-3.log)
- [claim 4](evidence/03-kprove-claim-4.log)
- [claim 5](evidence/03-kprove-claim-5.log)
- [claim 6](evidence/03-kprove-claim-6.log)

Thus clean reconstruction of every submitted positive claim succeeds.

## 4. Adequacy and real-program pinning

### Plain-language meaning and witnesses of the six entry claims

All claims start from `.Map` environment/functions and `noResult`, execute
`run(solution, ...)`, require termination at `.K`, restore the two maps to
`.Map`, and constrain the result to one exact tuple.

| Claim | Preconditions and postcondition | Satisfying witness |
|---|---|---|
| 1 | No side condition; on the fixed six-element example return `(2,11/5)` | the fixed input itself |
| 2 | No side condition; on the fixed duplicate example return `(2,2)` | the fixed input itself |
| 3 | Two rationals `A < B` and not `B < A`; return `(A,B)` | `A=1, B=2` |
| 4 | Two rationals `B < A` and not `A < B`; return `(B,A)` | `A=2, B=1` |
| 5 | Two equal rationals, with neither less relation; return `(A,B)` | `A=B=2` |
| 6 | No side condition; on `[-10,-3,-7/2,9]` return `(-7/2,-3)` | the fixed input itself |

All witnesses satisfy their side conditions. Substitution gives the claimed
tuple in fresh K execution and in both Python implementations. Exact per-claim
values are in
[04-claim-python-witnesses.log](evidence/04-claim-python-witnesses.log),
[04-krun-claim2.log](evidence/04-krun-claim2.log),
[04-krun-claim3.log](evidence/04-krun-claim3.log), and
[04-krun-claim6.log](evidence/04-krun-claim6.log), together with the Stage 3
K runs for the remaining cases.

### Program identity

The `<k>` cell uses the local function symbol `solution`. Its sole equation in
`/candidate/verification.k:9` expands to a manually copied constructor tree.
Static comparison shows that tree is the submitted `solution.mpy` tree, using
`.Stmts` where the pretty-printed empty blocks are blank. This link was also
tested dynamically:

1. a fresh LLVM verification definition loaded the submitted
   `solution.mpy`;
2. the same definition loaded a file containing only `solution`;
3. the two final KORE configurations were byte-identical (same SHA-256
   `901430aba5d092aaa3053f9b1af26f1bdd55ab90b14b82792d68e4729214c8cd`).

Both executions and `cmp` exited 0; see
[04-program-pinning.log](evidence/04-program-pinning.log). Together with
trusted translator byte identity, this pins the current submitted program.
It remains a manual source-to-spec duplication rather than an automatic file
inclusion, but the current trees agree.

There are no helper or loop claims and no operational shortcut in
`verification.k`; fixed semantics executes the program body. The concrete
longer-list proofs simply unroll their fixed loops. The length-two symbolic
claims also have statically bounded execution and require no invariant.

### Material theorem-scope failure

The natural-language domain is every input list of length at least two. No
entry claim has a symbolic list, a symbolic length above two, a minimum-gap
postcondition, or a quantified condition comparing the returned pair with
every other distinct-index pair.

In particular, any ordinary three-element input—such as the tested
`[0.0, 10.0, 1.0]`, whose correct result is `(0.0,1.0)`—satisfies the prompt
but matches no symbolic claim. Claim 1, claim 2, and claim 6 prove only their
single literal inputs. Claims 3 through 5 prove only lists of exactly two
elements, where there is only one possible index pair. The spec therefore does
not exercise or prove the algorithm's essential minimum-maintenance property
for arbitrary loop iterations.

The returned values in the claims are constrained and non-vacuous, but the
requested general result is absent. Differential tests and an informal
algorithm argument cannot substitute for that missing K theorem.

## 5. Rule-by-rule static soundness review

The source hashes and machine-extracted declaration/rule inventory are in
[05-static-source-inventory.log](evidence/05-static-source-inventory.log).
There are 51 rules in `semantic.k`, four definitional rules in
`verification.k`, and six claims. There are nine `[function]` productions and
no `[total]`, `[functional]`, simplification, `owise`, or priority attributes.
There are no opaque result-bearing symbols.

### Local syntax inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: a juxtaposed list of `Stmt`;
- one-name `Params` and comma-separated `Strings`;
- `Stmt`: `ImportFrom`, `FuncDef`, `Assign`, `If`, `While`, and `Return`;
- `Expr`: `Name`, `Int`, `Subscript`, `BinOp`, `Call`, `Compare`, and
  two-element `TupleExpr`;
- `CmpOp`;
- `Value`: `vint`, `vnum`, `vbool`, `vnil`, `vlist`, and `vtuple`;
- `Input`: a program or `run(Program, Value)`.

`MPY-SEMANTIC` adds `Result` (`noResult` or a value), `Function`, the four-cell
configuration, 17 control-item productions, and the five helper function
productions `valueLength`, `valueAt`, `valuePlus`, `valueMinus`, and
`valueLess`.

`MPY-VERIFICATION` adds the defined `solution` program symbol and three defined
`nums` constructors of arities 2, 4, and 6.

### Used-construct coverage

| `solution.mpy` construct | Declaration and behavior |
|---|---|
| module and statement sequence | `semantic.k:10-11`, rules 109-112 |
| `ImportFrom` | line 15, rule 114 |
| `FuncDef` and one parameter | lines 12 and 16, rules 115-121 |
| name assignment and lookup | lines 17 and 22, rules 124-126 and 144-145 |
| `If` | line 18, rules 128-130 |
| `While` | line 19, rules 132-135 |
| `Return` | line 20, rules 137-141 |
| integer literals | line 23, rule 146 |
| subscripting | line 24, rules 86-89 and 153-155 |
| binary `+` and `-` | line 25, rules 91-100 and 148-151 |
| `len` call | line 26, rules 82-84 and 166-167 |
| comparison `<` | lines 27 and 29, rules 102-106 and 157-162 |
| two-element tuple | line 28, rules 169-171 |

Every constructor in the submitted program has a declaration and an exercised
rule path. Unused Python constructs are intentionally absent, which is
acceptable in this mode.

### Exhaustive semantic rule assessment

The following inventory covers every rule in `semantic.k`.

| Rule lines | Role and decision |
|---|---|
| 83 | `valueLength(vnil)=0`: true list-length base case. |
| 84 | Cons length is one plus tail length: true and structurally descending. |
| 87 | Index zero returns the head: true for a nonempty list. |
| 88-89 | Positive index decrements and recurses on the tail: true on its guard and structurally descending. It intentionally has no negative/out-of-range case. |
| 93 | `vint(I)+vint(J)`: exact integer addition; true. |
| 94 | `vnum(R)+vnum(S)`: exact rational addition; true in the selected model. |
| 95 | `vint(I)+vnum(R)`: exact mixed rational addition; true. |
| 96 | `vnum(R)+vint(I)`: exact mixed rational addition; true. |
| 97 | integer subtraction: true. |
| 98 | rational subtraction: true in the selected model. |
| 99 | integer-minus-rational: true. |
| 100 | rational-minus-integer: true. |
| 103 | integer less-than: true. |
| 104 | rational less-than: true in the selected model. |
| 105 | integer/rational less-than: true. |
| 106 | rational/integer less-than: true. |
| 109 | Loading a module begins statement execution: faithful for the submitted module. |
| 110 | `run` loads the exact module and then invokes the named entry point: faithful for the one submitted entry point and already-evaluated input value. |
| 111 | Empty statement execution terminates: true. |
| 112 | Nonempty statements execute head before tail: correct sequential order. |
| 114 | The `typing` import is ignored: safe for this translated program because annotations are absent from the constructor tree and the import has no result-relevant effect. |
| 115-116 | Function definition stores its parameter/body in the function map: faithful for the single top-level definition. |
| 118-119 | Invocation looks up that exact stored binding: no name oracle or substituted body. |
| 120-121 | Binding installs the sole parameter in a fresh local map, then executes the body: faithful for the one-shot, one-argument call. |
| 124 | Assignment evaluates the right side before storage: correct. |
| 125-126 | Name assignment updates the local map: correct for all submitted targets. |
| 128 | `If` evaluates its condition before branch choice: correct. |
| 129 | True selects the yes statements: correct. |
| 130 | False selects the no statements: correct. |
| 132 | `While` evaluates its condition: correct. |
| 133-134 | True executes the body and returns to the same loop head: correct recurring control state. |
| 135 | False exits the loop: correct. |
| 137 | Return evaluates its expression first: correct. |
| 138-141 | Return records the value and clears the one-shot continuation/maps: correct for the only reachable top-level invocation context in this program. It is not a general Python call-stack rule; nested calls or later invocations are outside this semantics. |
| 144-145 | Name lookup reads the current map binding: correct. |
| 146 | Integer literal becomes `vint`: correct. |
| 148 | Binary expression starts with the left operand: correct Python order. |
| 149 | After the left value, evaluate the right and retain the left: correct. |
| 150 | `+` applies left plus right: operand order is correct. |
| 151 | `-` applies left minus right: operand order is correct. |
| 153 | Subscript evaluates the collection first: correct. |
| 154 | Then it evaluates the index and retains the collection: correct. |
| 155 | Integer indexing uses `valueAt`: correct for the nonnegative, in-range indices maintained by this program's loops. |
| 157-158 | Comparison evaluates the left expression first: correct. |
| 159-160 | Then it evaluates the right and retains the left: correct. |
| 161-162 | `<` computes left less-than right: operand order is correct. |
| 166 | The unshadowed `len` call evaluates its argument: correct for this program, which never binds `len`. |
| 167 | List length returns an integer value: correct. |
| 169 | Tuple evaluates its first element first: correct. |
| 170 | Then it evaluates its second element: correct. |
| 171 | The two evaluated values form the returned tuple in order: correct. |

The helper equation guards are disjoint or agree: `valueAt`'s zero and
positive cases do not overlap; the four numeric wrapper combinations are
pairwise disjoint; true/false branch rules are disjoint. Recursive helpers
descend. Partial functions remain partial rather than being falsely marked
total. There are no local rule priorities or simplifications whose interaction
could preempt execution.

The environment is the only mutable program state. There is no heap, output,
exception, or allocation cell; lists and tuples are immutable values. That is
sufficient for the result behavior of this source on supported inputs, but not
a complete Python execution model. The one-shot return cleanup would be
inadequate for nested calls or a second invocation, neither of which is
reachable from the submitted program/input grammar.

### Exhaustive verification-rule assessment

| Rule | Class and decision |
|---|---|
| `verification.k:9-43`, `solution` | Definitional program constant, not an operational answer summary. It is exactly the submitted constructor tree, as checked statically and dynamically. |
| `verification.k:49`, two-argument `nums` | Truthful constructor for a two-element rational list. |
| `verification.k:50-51`, four-argument `nums` | Truthful constructor for a four-element rational list. |
| `verification.k:52-54`, six-argument `nums` | Truthful constructor for a six-element rational list. |

These functions encode syntax/input data, not the closest-pair answer. There
is no result oracle, operational bridge, priority rewrite, proof-local lemma,
loop summary, or unconstrained fresh value.

### Semantics limitations, without an unsupported unsoundness allegation

The local rules are sound on the exercised exact-rational, one-shot
configurations. This review does not label a local rule unsound, so there is no
purported false-rule witness to supply. The narrower evidence gaps are:

- Python `float` values and operations are represented by exact K rationals;
  NaN, infinities, signed zero, and IEEE rounding have no K representation or
  connection theorem.
- Out-of-range indexing stops rather than modeling `IndexError`, as witnessed
  by the empty-input run. That input violates the prompt precondition.
- The call/return model is only sufficient for this single top-level
  invocation.

These are explicit language-model boundaries. Most importantly, even within
the exact-rational subset the spec still lacks the arbitrary-list correctness
claim.

## 6. Fresh non-vacuity test

The reviewer created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), which retains claim 1's
satisfiable input but mutates the required second result element from `11/5`
to `12/5`.

First,

```text
kprove spec-vacuity-audit.k \
  --definition /tmp/audit-work/build/verification-haskell-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exited 0, demonstrating successful parsing/spec construction
([06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log)).

The real proof command then exited 1 with `WarnStuckClaimState`. Its residual
terminal configuration explicitly contains
`vtuple(vnum(2), vnum(11 /Rat 5))`, which cannot unify with the mutated target
`vtuple(vnum(2), vnum(12 /Rat 5))`. See
[06-vacuity-proof.log](evidence/06-vacuity-proof.log). This is failure for the
expected unmet result obligation, not a parser error, timeout, unrelated crash,
or unreachable mutation.

This passes non-vacuity for the concrete result claim. It does not create the
missing universal closest-pair theorem.

## 7. Proven versus assumed accounting

### What the reachability proof actually establishes

Under `semantic.k` and K's built-in exact arithmetic/maps, the proof
establishes only:

1. the two fixed prompt examples return the stated tuples;
2. every exact-rational list of exactly two strictly ascending elements is
   returned in that order;
3. every exact-rational list of exactly two strictly descending elements is
   returned in ascending order;
4. every exact-rational list of exactly two equal elements returns that equal
   pair;
5. one fixed four-element negative-valued input returns the stated tuple.

All are terminating reachability results from the exact initial cells to
`.K`; they are not tautologies or implications with a free result.

The proof does not establish a closest-pair property for arbitrary list
length, does not establish an invariant over examined pairs, and does not
quantify that no other pair has a smaller gap.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and reachability implementation | all builds, executions, and proofs | Necessary low-level tool trust; acceptable. |
| Built-in `Bool`, `Int`, `Rat`, and `Map` operations from K | every semantic computation | Ordinary mathematical/runtime primitives; acceptable for the exact-rational theorem. |
| Handwritten `semantic.k` as a model of the used Python subset | all claims | Audited rule-by-rule and concretely tested; acceptable for the narrow rational, one-shot theorem, but not machine-proved equivalent to Python. |
| Trusted `py2mpy.py` and byte equality of regenerated `solution.mpy` | source-to-constructor identity | Trusted input plus exact reproducible comparison; acceptable. |
| Manual `solution` constructor equation | every claim | Fully defined and dynamically equal to the submitted constructor program; acceptable for the current artifact, though manually duplicated. |
| Exact rational as a bridge for Python `float` | intent interpretation of every numeric claim | No universal connection theorem; excludes IEEE special values and rounding. Concerning and inadequate for an unrestricted `List[float]` theorem. |
| Independent Python differential testing | candidate-versus-canonical fidelity only | 215 intended cases with no mismatch; useful finite evidence, not a universal proof or a K-semantics connection theorem. |
| Informal loop/algorithm reasoning | belief that the implementation is generally correct | Plausible, but wholly outside the submitted K claims and cannot fill the missing theorem. |

There are no opaque symbols or empirical oracles inside claim closure.

### Gate and verdict reasoning

- **Real-program soundness of the six literal claims:** passes. The current
  program is pinned, fixed semantics executes it, results are constrained,
  all claims reconstruct independently, and the false result is rejected.
- **Intent adequacy for 20-find-closest-elements:** fails materially. The
  formal theorem omits virtually the whole length-at-least-two domain and
  never states the minimum-distance property for arbitrary lists.
- **Evidence auditability:** the reviewer evidence is reproducible and finite
  evidence is labeled as such. The float bridge remains assumed rather than
  proven.

Under the requested decision boundary, a missing target correctness proof is
`FAIL / NOT_LEGIT`, even when narrower example claims legitimately reach
`#Top`. No timeout, container problem, malformed mount, or other audit
infrastructure uncertainty contributed to this decision.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
