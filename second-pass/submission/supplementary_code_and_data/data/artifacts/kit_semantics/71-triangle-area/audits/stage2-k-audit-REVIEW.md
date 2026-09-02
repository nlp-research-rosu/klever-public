# Independent adversarial review: 71-triangle-area

## Outcome

The candidate contains a real, result-constraining K reachability proof of the
submitted translated program. I rebuilt both definitions from source, proved all
27 target claims separately, mechanically matched the quoted program to a
trusted fresh translation, and obtained clean rejection of both a false result
and a changed executed body.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
fixed supplied MPY model has documented numerical representation gaps. In
particular, its float `<=` encoding gives the wrong CPython answer on NaN, and
its concrete Int-to-Float hook aborts on sufficiently large K integers. Neither
gap was introduced by the candidate, neither narrows the K claims, and the
submitted Python behaves like CPython at both boundaries. Concrete divergence
witnesses are recorded below. This is the supplied-model exception described in
campaign amendment v2, not a candidate-caused restriction.

## 1. Input and provenance integrity

I treated every generation record and everything in `/candidate` as untrusted.
The launcher record declares `pipeline-v3`, problem `71-triangle-area`,
condition `kit-semantics`, and `SUPPLIED_SEMANTICS`.

All required records were present, regular files or real directories, readable,
and not symlinks:

- `/audit-input.json`, `/audit-campaign-lock.json`
- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the structured trace below `/generation-evidence/codex-trace/`

The mounted campaign lock is byte-for-byte equal to the campaign block embedded
in `/audit-input.json`; its SHA-256 is the recorded
`053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`.
The recorded hashes of the required individual generation files match the
mounted files. The sole trace file contains 352 valid JSONL events and no
malformed line. I read the full 58,237-line generation output and parsed the
full structured trace; their success reports and prior `#Top` are merely
generation claims and were not used as proof results.

The candidate prompt and translator are byte-identical to the trusted mounts:

- prompt SHA-256:
  `08897376ea63666a837e51f16608bd0abb6d1633e025ccacde662a7844e19626`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

`diff -qr --no-dereference` found no difference between
`/candidate/reference-semantics` and
`/reference/reference-semantics`, and recursive symlink inspection found none.
Both semantics trees have launcher tree hash
`4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`.
The full candidate tree hash is
`5d067b9d5d521fe0e3661ce44cdbd9366941413a65897e3226ad3e39a4a78b85`,
matching `/generation-result.json`.

Evidence:

- `evidence/inspect_provenance.py`
- `evidence/01-provenance-inspection.log`
- `evidence/01b-integrity.log`
- `evidence/01c-tree-hashes.log`
- `evidence/02-scratch-setup.log`

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted docstring says that the input is three side lengths. A triangle is
invalid if any pair sums to no more than the remaining side, in which case the
function returns `-1`; otherwise it returns Heron's-formula area rounded to two
decimal places. The determined examples are `(3, 4, 5) -> 6.00` and
`(1, 2, 10) -> -1`. The canonical implementation is one witness of precisely
that reading.

`solution.py` performs the three invalidity comparisons, then computes
`s = (a + b + c) / 2`,
`sqrt(s * (s-a) * (s-b) * (s-c))`, and `round(area, 2)`. This directly
implements the determined behavior. Its handling of numeric subtypes and
exceptional numeric representations is not contradicted by the docstring.

I regenerated MPY using the trusted command

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

and obtained byte identity with submitted `solution.mpy`. Both have SHA-256
`d997081a8921698c9358a0a4ecdc8ec25207211a91b0382701334219854e09fa`.
See `evidence/03-translator-identity.log`.

### Independent differential

`evidence/differential.py` imports the candidate and trusted canonical entry
points independently. It exercises both examples; equality and both sides of
all three branch boundaries; zero, negative, Boolean, float, subnormal, large,
NaN and infinity cases; Fraction, Decimal and empty-container cases; and 800
seeded generated integer/float triples. It also compares every positive integer
triple in `[1,30]^3` (27,000 cases) with an independent high-precision Decimal
Heron oracle.

Results:

- 828 candidate/canonical cases
- zero failures of a documented example
- zero material docstring-contract mismatches
- 27,000/27,000 agreement with the independent oracle
- one canonical divergence: Decimal `(3,4,5)` returns `6.0` in the candidate
  but raises `TypeError` in canonical

The Decimal difference is an underdetermined representation/error-handling
case. Returning the described triangle area is defensible and is not a program
defect under campaign v3. The finalized script exits zero and records that
classification in `evidence/04b-differential-final.log`. The earlier
`evidence/04-differential.log` is retained for transparency but used a stricter
intermediate assertion before the v3 classification was applied.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/proof`; candidate-built
definitions and caches were neither copied nor reused.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

This exited 0. A reviewer-authored smoke module ran the examples, all three
degenerate equality boundaries, valid integer and float cases, and a Boolean
case through that definition. Python and `krun` both exited zero; `krun` ended
with `.K`, `NoExc`, and exit code 0. See
`evidence/05-kompile-llvm.log`, `evidence/concrete_smoke.py`,
`evidence/concrete_smoke.mpy`, and `evidence/06-concrete-smoke.log`.

Fresh proof build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

This exited 0; see `evidence/07-kompile-haskell.log`.

I enumerated all 27 labels from `spec.k` and invoked `kprove` once per label
against the fresh definition. Every invocation exited zero and printed exactly
one `#Top`. The claims are the full Cartesian product `{Int, Float, Bool}^3`,
not a bounded set of examples. The aggregate result is
`TOTAL_CLAIMS=27`, `FAILED_CLAIMS=0` in
`evidence/08-positive-claims-summary.log`; complete bounded output for every
individual claim is retained as `evidence/08-claim-*.log`, and the command
driver is `evidence/run_positive_claims.sh`.

## 4. Adequacy and real-program pinning

All 27 entry claims have the same shape. Their only precondition is that
`A`, `B`, and `C` inhabit the indicated combination of K `Int`, `Float`, and
`Bool` sorts. There is no hidden size, positivity, validity, or finiteness
guard. Each initial state has the normal empty MPY heap, stack, and user scope
plus the fixed builtins scope.

In plain language, the postcondition says:

- return `-1` if any of `A+B<=C`, `A+C<=B`, or `B+C<=A` holds under the fixed
  MPY numeric operations;
- otherwise return fixed MPY `round(sqrt(HeronProduct), 2)`;
- leave normal return/exception/stack/allocator cells in their prescribed
  completed state.

The destination scope is existential because module execution installs the
function closure. It does not leave the returned value free: the `<k>` result
is exactly `triangleAreaSpec(A,B,C)`. The postcondition is an equality-shaped
reachability target, not a one-way implication or unconstrained oracle.

The initial `<k>` cell executes
`#loadAll(triangleProgram())` and then performs ordinary lookup and a call to
`triangle_area`. To check that `triangleProgram()` is not a substituted body, I
parsed the trusted fresh `solution.regenerated.mpy` with `kast` and proved its
constructor term equal to the quotation. The only normalization is the parser's
semantically inert collapse of trailing empty `.Stmts`. The mechanical check
exits zero with `#Top`; its source and complete output are
`evidence/program-pinning.k` and
`evidence/09c-program-pinning-config-final.log`.

`evidence/ground_witnesses.py` supplies one satisfying ground input for each of
the 27 sort combinations. All 27 formal ground results agree with both Python
implementations; hence every entry precondition is satisfiable. For example,
the all-integer claim contains `(3,4,5)` and produces `6.0`, while the Boolean
claim contains `(true,true,true)` and produces `0.43`. See
`evidence/10-ground-witnesses.log`.

Finally, the body-sensitivity mutation changes the constructor actually
executed by the claim, replacing invalid `return -1` with `return 7` while
leaving the postcondition unchanged. It builds, reaches `7`, and fails with one
expected stuck claim rather than `#Top`. This is direct evidence that the
theorem depends on the submitted body; see
`evidence/auditor-body-sensitivity.k` and
`evidence/13-body-sensitivity.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried every source line declaring syntax, functions, totality,
priorities, contexts, ordinary rules, concrete rules, simplifications,
no-evaluator symbols, and claims. The inventory contains 250 syntax declaration
lines, 770 rule lines, five contexts, and 27 claims across all source modules.
The complete line-numbered inventory, attributes, and source hashes are in
`evidence/11-rule-inventory.log`; its reproducible driver is
`evidence/build_rule_inventory.sh`.

Every inventory group received the following disposition:

| Files | Static disposition |
| --- | --- |
| `semantics.k`, `syntax.k` | Pure module assembly, AST/value syntax and configuration declarations; no task result is encoded. |
| `core.k`, `controls.k`, `functions.k`, `call.k`, `operators.k` | Relevant module loading, sequencing, lookup, expression order, short-circuiting, frames, argument binding, call/return and operator dispatch. Guards and priorities are constructor/sort specific; the submitted term follows ordinary MPY control flow. |
| `int.k`, `bool.k` | Relevant exact integer arithmetic/comparisons, Boolean-as-integer promotion, truthiness and `or` short-circuit rules. Their guards are disjoint on the used sorts and their conclusions match Python for the covered operations. |
| `float.k` | Relevant fixed-model float arithmetic/comparisons, promotion, `math.sqrt`, and `round`. Proof-side values are deliberately opaque/total; concrete equations use K float hooks. The NaN and extreme-integer gaps below are the material limitations. No rule directly returns this task's answer. |
| `builtins.k` | Builtin map plus generic builtin definitions; only `round` is reached here. The used `roundFN` path is a fixed numerical primitive, not a proof-local summary. Other rules are sort/constructor guarded and unreachable from this program. |
| `concrete.k` | LLVM-only concrete bridges and assertion behavior. It is used for fresh concrete tests, not imported by the proof module. |
| `assert.k`, `comprehension.k`, `dict.k`, `iter.k`, `list.k`, `methods.k`, `range.k`, `set.k`, `sort.k`, `str.k`, `subscript.k`, `tuple.k` | Reviewed declarations and rules are constructor/sort guarded and unreachable from `solution.mpy`; they cannot enable a task-specific false conclusion in these claims. No answer-encoding or unconstrained operational bypass was found. |
| `verification.k` | Six declarations and six equations reviewed individually below. |
| `spec.k` | Exactly 27 entry claims, one per represented numeric sort triple; no helper/loop claim or bounded unrolling exists. |

### Used-construct mapping

`solution.mpy` uses `Module`, `Import`, `FuncDef`, `Params`, `If`, `BoolOp`,
`Compare`, `CmpOp`, `BinOp`, `UnaryOp`, `Assign`, `Return`, `Call`,
`Attribute`, `Name`, `Int`, and numeric `Val` arguments. These map to:

- AST declarations in `syntax.k`;
- `#loadAll`, statement sequencing, names, assignment and evaluation contexts
  in `core.k`;
- function closure creation in `functions.k`;
- lookup, argument evaluation, frame creation/binding, return and frame popping
  in `call.k` and `functions.k`;
- `If`, `Return`, and control propagation in `controls.k`;
- ordered evaluation in `operators.k`, with Boolean `or` short-circuit rules in
  `bool.k`;
- integer/Boolean dispatch in `int.k` and `bool.k`;
- float and mixed-type operations in `float.k`;
- the fixed priority-40 `math.sqrt` interception in `float.k`;
- normal builtin lookup and `roundFN` in `builtins.k`/`float.k`.

There is no loop, mutation of a user heap object, or allocation relevant to the
algorithm. The normal final stack, return, exception, allocator, environment
and heap cells are constrained.

### Candidate proof extension

Each of the six candidate equations is terminating and nonoverlapping:

1. `intToF(I) => proofIntToF(I) [simplification]` reifies the supplied
   no-evaluator `intToF` primitive because Haskell lacks its concrete hook.
   `proofIntToF` is a fresh, argument-retaining opaque symbol. It changes no
   cells or control and cannot choose a branch or fabricate an independent
   expected result. Its equality to actual numeric conversion remains an
   explicit assumption, discussed in the ledger.
2. `triangleProgram()` is the exact program quotation mechanically checked in
   stage 4. It is data consumed by operational semantics, not a call rewrite.
3. `invalidTriangle` is exactly the disjunction of the three contract
   comparisons.
4. `semiPerimeter` is exactly left-associated `((A+B)+C)/2`.
5. `heronProduct` is exactly the source's left-associated Heron product.
6. `triangleAreaSpec` selects `-1` or fixed `round(sqrt(...),2)` from those
   terms.

The summary dependency graph is acyclic. None of these equations rewrites a
user call, assignment, comparison, branch, continuation, frame, or return. The
source computes the same operations independently, and the negative probes show
that the summaries do not make arbitrary values provable.

### Concrete fixed-model gaps and witnesses

The supplied float rule

```text
applyCmp("<=", F1, F2) => notBool gtF(F1, F2)
```

assumes a total order. False-conclusion witness: with `F1 = NaN`,
`gtF(NaN,F2)` is false, so the rule concludes `NaN <= F2` is true, whereas
CPython concludes false. In this program the submitted Python returns NaN for
`triangle_area(NaN,3.0,4.0)`, but the untouched freshly built MPY definition
takes an invalid branch and returns `-1`. Both sides of the witness execute
successfully in `evidence/nan_boundary.py`,
`evidence/nan_boundary.mpy`, and
`evidence/14-nan-model-boundary.log`.

A second supplied boundary arises from treating Int-to-Float operations as
total over unbounded K integers. For three sides equal to `10**309`, submitted
Python raises `OverflowError` during true division, while the untouched LLVM
model aborts in its `FLOAT.float2int`/non-finite bridge rather than representing
that Python exception. The translated witness and exact statuses are in
`evidence/huge_integer_boundary.py`,
`evidence/huge_integer_boundary.mpy`, and
`evidence/14b-huge-integer-boundary.log`.

These witnesses do not make the submitted Python violate the docstring: NaN,
non-finite behavior, enormous integer-to-float conversion, and exception policy
are numeric-representation details the docstring leaves open. They also do not
come from a candidate rule or restriction. The candidate claims quantify over
all three fixed MPY numeric sorts; the gaps are behaviors the supplied model
cannot faithfully represent. They are therefore recorded as non-fatal supplied
model boundaries under amendment v2, but they prevent `PASS`.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`.

The accepted reviewer mutation keeps the real program and restricts the
all-integer entry to `A+B<=C`, but demands result `0` rather than `-1`.
`(1,2,3)` is a concrete satisfying witness and both Python implementations
return `-1`. The mutation passes K dry-run/build, then proof execution exits 1
with exactly one `WarnStuckClaimState`; the residual contains `<k>-1</k>`
against the demanded zero. There is no missing-hook diagnostic and no `#Top`.
See `evidence/auditor-false-result-v2.k` and
`evidence/12b-non-vacuity-final.log`.

For transparency, `evidence/auditor-false-result.k` and
`evidence/12-non-vacuity.log` retain a preliminary ground-float probe that hit
the unrelated Haskell `FLOAT.int2float` hook. I rejected that probe as
non-vacuity evidence and used only the clean symbolic invalid-branch mutation.

Together with the independently clean body mutation from stage 4, this
establishes both postcondition sensitivity and executed-program sensitivity.

## 7. Proven-versus-assumed accounting

### What the K proof establishes

Under the exact supplied MPY proof semantics plus the one explicit
`proofIntToF` reification, loading the freshly translated submitted module and
calling `triangle_area` on any of the 27 represented numeric sort combinations
reaches the result term:

```text
if A+B<=C or A+C<=B or B+C<=A
then -1
else round(sqrt(s*(s-A)*(s-B)*(s-C)), 2)
```

with `s=((A+B)+C)/2`, using the fixed MPY operations, ordinary source control
flow, and normal completed operational cells. It is a partial-correctness
statement relative to that model; it is not a bit-level theorem about K's
opaque float primitives and is not a separate CPython termination theorem.

### Trust ledger

| Boundary | Status and justification |
| --- | --- |
| Trusted prompt, translator, canonical witness | Launcher-trusted mounts; prompt/translator integrity checked independently. Canonical is used only as a helper witness. |
| Supplied MPY semantics | Read-only trusted model and recursively identical candidate copy. It supplies operational Python modeling; candidate did not alter it. |
| K builtin Int/Bool/Map/List machinery and compiler/prover | Ordinary toolchain trust boundary. Fresh LLVM and Haskell builds were used. |
| `divII`, `addF`, `subF`, `mulF`, `sqrtF`, `roundFN`, `gtF`, `floatLt`, `ltIF`, `ltFI`, `eqIF` | Fixed opaque numerical primitives in symbolic proof. Structurally appropriate low-level boundaries, but the theorem is conditional on their intended numerical meanings. Concrete/differential tests are finite bridge evidence only. |
| `proofIntToF(I)` | Candidate proof-local reification of fixed opaque `intToF(I)`, retaining `I` and carrying no task result or state. Acceptable as an explicit conditional primitive bridge; the extreme-integer witness shows it cannot be interpreted as an unrestricted CPython conversion theorem. |
| Quoted `triangleProgram()` | Mechanically equal to trusted regenerated MPY modulo parser-normalized empty statement tails. Body mutation rejection confirms dependence on it. |
| Contract summaries | Direct, acyclic definitions of the prompt predicate and Heron expression. They constrain the result and do not bypass execution. |
| Decimal/Fraction/custom values | Classes absent from the supplied model. The proof adds no narrower guard within represented numeric sorts. Candidate's Decimal result is docstring-defensible; differential evidence records the canonical difference. |
| NaN ordering | Documented fixed-model divergence with concrete witness: model `-1`, submitted CPython program NaN. Supplied-model concern, not candidate unsoundness. |
| Extreme integer conversion | Documented fixed-model divergence with concrete witness: CPython `OverflowError`, concrete MPY abort. Supplied-model representation/exception gap, not candidate narrowing. |
| Differential and concrete testing | Supports only translation, concrete execution, examples, branch coverage and boundary observations. It is not substituted for the K proof. |

No proof-local rule encodes the desired answer, no oracle replaces a
property-bearing source operation, the result is not existential, and the
theorem does not prove a substituted program. The two numerical limitations are
real but satisfy the supplied-model representation-gap exception: they
originate in the fixed semantics, the claims cover every numeric value/sort the
symbolic model offers without an added candidate guard, this ledger gives
concrete divergence witnesses, and the submitted Python itself is faithful to
CPython rather than to the flawed model behavior.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
