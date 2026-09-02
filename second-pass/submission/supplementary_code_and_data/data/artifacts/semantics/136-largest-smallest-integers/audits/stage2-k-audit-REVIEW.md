# Independent adversarial audit: 136-largest-smallest-integers

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program for every finite MPY list of mathematical
integers. I reconstructed both definitions from source, obtained fresh `#Top`
results, mechanically pinned the theorem's function body to the regenerated
`solution.mpy`, audited every proof-local extension, and made a reachable false
loop-result mutation fail with the expected arithmetic residual.

I assign `CONCERNS / LEGIT`, not `PASS`, for two non-fatal validation
limitations:

1. The candidate's one operational bridge is sound on its complete ground
   domain, and a bridge-free universally quantified theorem closes for every
   `Int`. However, the extensionally equivalent theorem phrased exactly as
   `V:Val requires isInt(V)` does not close because this backend does not
   reverse a generated sort predicate into a subsort injection. The compiler's
   generated `isInt` equations and the typed theorem complete the semantic
   argument, but this is less direct than a single exact-domain connection
   proof.
2. The K postcondition returns recursively defined folds. Their equations
   transparently compute the greatest negative and least positive, and the
   guard/equation audit supports that reading, but no separate quantified K
   theorem relates those folds to a set-theoretic extrema definition. That last
   intent bridge remains ordinary mathematical reasoning.

Neither limitation admits a false result on the intended integer-list domain.
The proof is unrestricted in list length and integer magnitude; it is not a
finite unrolling or examples-only argument.

Audit evidence is indexed in `evidence/README.md`. Exploratory logs explicitly
marked `initial` or `interrupted` are retained but are not used as successful
evidence.

## 1. Input and provenance integrity

I first read `/audit-input.json` and used its `container_paths`, not its
host-only paths. It declares:

- `record_layout = pipeline-v3`
- `condition = semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `problem_id = 136-largest-smallest-integers`

The trusted `/reference/reference-semantics` tree is present, so the mount
agrees with the rendered semantics mode.

I read all required pipeline-v3 records:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/runtime-metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the JSONL trace beneath
`/generation-evidence/codex-trace/`. These were treated only as generation
claims. The trace contains one regular JSONL file with 299 valid records.

The independent command was:

```text
bash /audit-output/evidence/01_integrity.sh
```

It exited 0. Its bounded record is `evidence/01_integrity.log`. The checks
established:

- every launcher-required mount and pipeline-v3 record is regular, readable,
  and present;
- `/audit-campaign-lock.json` exactly equals the campaign block in
  `/audit-input.json`;
- the independently computed campaign-lock hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  equal to the recorded value;
- all launcher-recorded hashes checked by the script match the mounted bytes,
  including run/task/result/invocation/metrics/runtime/usage/prompt/log/trace
  records and trusted source inputs;
- no candidate, trusted-semantics, or structured-trace entry is symlinked or a
  special file;
- `diff -qr --no-dereference` between candidate and trusted
  `reference-semantics/` exits 0;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.

The candidate supplied compiled directories, but they were explicitly
excluded. No infrastructure breach or supplied-semantics integrity failure was
found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of integers, return `(a, b)` where `a` is the greatest member less
than zero and `b` is the least member greater than zero. Return `None` in a
component when the corresponding subset is empty. Zero belongs to neither
subset. The trusted examples include a positive-only list, the empty list, and
`[0]`.

The canonical implementation filters negative and positive values, then uses
`max` and `min`. The candidate implementation maintains zero sentinels while
scanning once, replaces each remaining sentinel with `None`, and returns the
pair. All four update boundaries are correct: first negative, greater negative,
first positive, and lesser positive.

### Regeneration and differential evidence

The command:

```text
bash /audit-output/evidence/02_fidelity.sh
```

exited 0; see `evidence/02_fidelity.log` and
`evidence/differential_test.py`.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
9663d933ac0d1f0b8d407139edd1f376fd156f3f10f79b79882ce8136df957b7
```

The independent differential driver imports
`/reference/canonical.py:largest_smallest_integers` and the candidate entry
point. It ran:

- 17 documented and boundary cases, including empty, zero-only,
  negative-only, positive-only, duplicate, ordering, arbitrary-precision, and a
  Python-`bool` edge case;
- all 19,531 lists of lengths 0 through 6 over
  `[-5, -1, 0, 1, 5]`;
- 2,000 deterministic random lists of lengths 0 through 50 with values up to
  approximately `10^30` in magnitude.

There were 21,548 total cases and zero mismatches. The exact serialized input
set hash is
`4b6910afa202dc74b06695b5c1a4ac65e20a67f1790c406081275de1360889d8`.
This is finite program-fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reconstruction`; candidate-built `runtime-kompiled`,
`verification-kompiled`, and Python caches were not copied. K reported version
7.1.293.

The exact reconstruction record is
`evidence/03_reconstruction.sh` / `evidence/03_reconstruction.log`. It exited
0. In sequence, it:

1. checked by Python AST comparison that the function embedded in the
   reviewer concrete driver equals the submitted `solution.py` function;
2. translated the driver with the trusted translator;
3. built a fresh LLVM definition from trusted
   `reference-semantics/semantics.k`, main module `MPY-KRUN`;
4. ran ten K assertions covering the examples, empty/list boundaries, repeated
   zeroes, mixed signs, ordering, and arbitrary-precision integers;
5. built a fresh Haskell definition from the scratch `verification.k`, main
   module `VERIFICATION`, importing the trusted supplied semantics;
6. proved `SPEC.scan-loop` independently; `kprove` exited 0 and printed
   `#Top`;
7. ran the complete `SPEC` module containing `scan-loop` and
   `entry-point-correct`; `kprove` exited 0 and printed `#Top`.

The entry theorem uses `scan-loop` as its circularity, so selecting only the
entry label would remove a proof dependency rather than test the actual target
proof. The unfiltered run checks both target claims together; the loop claim
was additionally checked alone.

The concrete execution ended with `NoExc` and exit code 0. The compiler emitted
non-exhaustiveness and unused-variable warnings in unrelated supplied-semantics
helpers, but neither fresh build failed and no candidate cache contributed to
either result.

## 4. Adequacy and real-program pinning

### Claims in plain language

`scan-loop` assumes a finite `VS` whose members satisfy `allInts`, a negative
accumulator `A <= 0`, and a positive accumulator `B >= 0`. Starting at the real
MPY `#loop` over `list(VS)` and the submitted loop body, it states that:

- `largest_negative` becomes `negFold(VS, A)`;
- `smallest_positive` becomes `posFold(VS, B)`;
- the loop target `value` becomes the final list value, or remains `OLD` on an
  empty list;
- the loop computation is consumed while the surrounding cells and scope
  context remain framed.

`entry-point-correct` assumes only `allInts(VS)`. From the exact initial MPY
configuration, it loads the module, looks up and calls
`largest_smallest_integers` with the bare list value, and reaches:

```text
tuple(
  optionalNeg(negFold(VS, 0)),
  optionalPos(posFold(VS, 0))
)
```

It also pins environment, scopes, allocation counters, heap, stack, return
state, exception state, and exit code. The result is not a free variable, a
tautology, or a one-way implication.

### Satisfying states and ground substitutions

`evidence/claim_witness.py`, run from
`evidence/05_adequacy_extensions.sh`, exhibited:

- entry witness `VS=[-5,-2,0,7,3]`, with K model, trusted canonical, and
  candidate Python all returning `(-2,3)`;
- loop witness with that `VS`, `A=-9`, `B=10`, and `OLD=42`, producing
  bindings `(-2,3,3)`;
- empty entry witness producing `(None,None)` in all three interpretations.

Thus both preconditions are satisfiable.

### Mechanical body pinning

The auditor parsed the submitted `solution.mpy` as sort `Module`, separately
parsed `largestSmallestModule`, and evaluated both with the fresh Haskell
definition. The final JSON constructor configurations are byte-identical:

```text
f0b82f73d607b313ea5b19ef17c72b6affe2c53a9d458c2f95205d4245643e74
```

They are preserved as `evidence/pinning-submitted-final.json` and
`evidence/pinning-proof-final.json`. This mechanically demonstrates that the
claim loads the same binding and body, allowing only K evaluation of the
candidate's naming macros.

A separate body-sensitivity mutation changed the actual executed constructor
from initializing `smallest_positive` to 0 into initializing it to 1. The
mutated definition built, but the original theorem exited 1 with
`WarnStuckClaimState`, exposing `posFold(VS,1)` against the required
`posFold(VS,0)`. See `evidence/body-mutation-verification.k`,
`evidence/body-mutation-spec.k`, and
`evidence/05_adequacy_extensions.log`.

The formal domain is every finite algebraic `ValSeq` whose elements are K
`Int`s, with no bound on length or integer magnitude. MPY has a distinct
`Bool` value sort, while CPython makes `bool` a subclass of `int`. The prompt's
material domain is lists of integers, so I do not treat K's exclusion of Bool
as a material contract narrowing; it remains a language-model edge ambiguity.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` normalized and enumerated every top-level
declaration from all 24 supplied-semantics source files plus
`verification.k` and `spec.k`. The complete 1,129-record inventory, including
source path, line, declaration kind, attributes, and full normalized block, is
in `evidence/04_inventory.log`. Its script exited 0.

Overall counts are:

```text
claims=2  configuration=1  contexts=5  rules=721  syntax=233
function=151  functional=0  total=111  simplification=0
priority=46  owise=26  concrete=35  no-evaluators=22
symbol=25  macro=4  macro-rec=1  strict=2  seqstrict=1
```

Per-file rule dispositions are below. `reachable` means the listed program
uses at least one rule in that fixed module. `fixed/unreached` means every rule
was still inspected and inventoried but cannot occur along this program's
constructor/control path. All are byte-identical members of the trusted
supplied baseline; that status does not bless any rule in `verification.k`.

| File | Syntax | Rules | Disposition for this proof |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | fixed aggregator |
| `syntax.k` | 16 | 0 | declarations reachable |
| `core.k` | 37 | 46 | fixed/reachable |
| `iter.k` | 1 | 0 | protocol declaration reachable |
| `controls.k` | 3 | 34 | fixed/reachable |
| `functions.k` | 4 | 15 | fixed/reachable |
| `call.k` | 3 | 21 | fixed/reachable |
| `operators.k` | 0 | 10 | fixed/reachable |
| `int.k` | 1 | 16 | fixed/reachable |
| `bool.k` | 0 | 13 | fixed/reachable |
| `list.k` | 5 | 27 | fixed/reachable |
| `tuple.k` | 4 | 21 | fixed/reachable |
| `assert.k` | 0 | 3 | fixed/unreached |
| `builtins.k` | 38 | 137 | fixed/unreached operations |
| `comprehension.k` | 3 | 7 | fixed/unreached |
| `concrete.k` | 5 | 16 | excluded from proof definition |
| `dict.k` | 12 | 28 | fixed/unreached |
| `float.k` | 34 | 121 | fixed/unreached |
| `methods.k` | 27 | 75 | fixed/unreached operations |
| `range.k` | 2 | 6 | fixed/unreached |
| `set.k` | 6 | 12 | fixed/unreached |
| `sort.k` | 6 | 19 | fixed/unreached |
| `str.k` | 5 | 28 | fixed/unreached |
| `subscript.k` | 15 | 40 | fixed/unreached |
| `verification.k` | 6 | 26 | proof-local; audited below |
| `spec.k` | 0 | 0 | two obligations, not assumed rules |

The fresh proof definition contains zero rules sourced from `concrete.k`;
`evidence/06_static_checks.log` records that mechanical check. Thus the 35
`[concrete]` declarations and the fixed baseline's 22 `[no-evaluators]`
declarations cannot serve as proof-local oracles here.

### Used-construct coverage and fixed execution

Every constructor in `solution.mpy` is declared in `syntax.k`: `Module`,
`FuncDef`, `Params`, `Assign`, `Name`, `Int`, `For`, `If`, `Compare`, `CmpOp`,
`BoolOp`, `NoneVal`, `Return`, and `TupleExpr`.

The reachable fixed rules provide:

- `core.k`: the full configuration, module loading, statement sequencing, name
  lookup, integer/None literals, and operator dispatch;
- `functions.k` and `call.k`: function binding, left-to-right argument
  evaluation, parameter binding, frame allocation, return, and frame pop;
- `controls.k`: right-hand-side-before-assignment strictness, branch selection,
  iterable evaluation once, loop step, target binding, and loop continuation;
- `list.k` and `iter.k`: empty-list completion and head/tail yield;
- `operators.k`, `int.k`, and `bool.k`: left/right comparison evaluation,
  integer `<`, `>`, `==`, and value-returning short-circuit `or`;
- `tuple.k`: loop target binding and left-to-right tuple construction.

No material source operation is missing or fabricated. The relevant path does
not allocate a list, mutate a heap object, perform I/O, invoke a builtin, or
raise an exception. Its only state changes are function-frame/scoping actions
and the three local assignments represented in the claims.

### Proof-local extension inventory and decisions

The 26 rules in `verification.k` are records 1092–1122 of the complete
inventory:

1. `intValue(I:Int) => I` is a guarded sort projection. For integers it is the
   identity. On non-integer `Val`s the total function is uninterpreted, not
   equated to a false value; every result-bearing use is guarded by `isInt`.
2. The priority-40 `#iterNext` rule is the only operational bridge. It has the
   same list head/tail binding, arbitrary continuation, and complete framed
   state as the fixed `list.k` rule. It changes only the yielded term from `V`
   to `intValue(V)`, under `isInt(V)`.
3. `scanBody`, `finishBody`, `solutionBody`, and
   `largestSmallestModule` are four definitional naming equations. Constructor
   comparison proves they expand to the submitted translated program. They do
   not skip execution.
4. The four `negStep` equations are pairwise disjoint and exhaustive for
   integer `I` and the claim invariant `A <= 0`; they implement the source's
   negative update.
5. The four `posStep` equations are pairwise disjoint and exhaustive for
   integer `I` and `B >= 0`; they implement the source's positive update.
6. Base/recursive pairs for `negFold`, `posFold`, and `finalValue` consume one
   `vCons` at each recursive step. Their guarded recursive cases are exhaustive
   on the `allInts` domain. They may remain uninterpreted on non-integer lists,
   which the entry precondition excludes.
7. The two `allInts` equations structurally cover every finite `ValSeq`.
8. Each pair of `optionalNeg` and `optionalPos` equations is disjoint and
   exhaustive over integers: zero maps to `noneV`, nonzero maps to itself.

There are no proof-local simplification rules, concrete rules,
`[no-evaluators]` symbols, or functional declarations. The sole proof-local
priority is the iterator bridge. `evidence/extension_equation_checks.py`
checked 1,681 accumulator/value pairs for exactly one applicable negative and
positive step rule, and 3,906 small sequences for equation agreement, extremum
meaning, and invariant preservation. It exited 0. These finite checks support
the exhaustive symbolic guard analysis; they do not replace it.

### Iterator bridge connection audit

The bridge-free definition in `evidence/bridge-base.k` imports only trusted
`MPY` plus the independently justified `intValue(I:Int) => I` equation; it does
not import `verification.k` or the candidate bridge.

The claim in `evidence/bridge-spec.k` universally quantifies over every
`I:Int`, arbitrary tail, arbitrary continuation, and all framed cells. Under
the fixed list iterator it proves:

```text
#iterNext(list(vCons(I,REST)))
  => #iterYield(intValue(I),list(REST))
```

The bridge-free build and proof both exited 0 and the proof printed `#Top`.
Compiled KORE independently shows exactly:

```text
isInt(inj{Int,KItem}(Int)) => true
isInt(K) => false [owise]
```

Therefore every ground `Val` satisfying the bridge guard is an integer
injection and lies in the typed universal theorem. All continuations and
non-`k` cells are preserved. The fixed/extended behavior agrees on value,
control, state, allocation, exception, and return effects.

As an adversarial containment check, the fixed semantics rejected a claim that
would yield `-6` instead of `-7` while retaining a distinct `Int(999)`
continuation. This confirms that neither the tail nor the continuation can be
silently discarded.

The exact `V:Val requires isInt(V)` formulation was also attempted and exited
1 with residual `V = intValue(V)`. This is the non-fatal evidence limitation
reported in the outcome: the backend does not derive a subsort substitution
from its generated sort predicate. There is no ground or symbolic false
conclusion witness for the candidate rule; the generated predicate equations
and typed universal proof instead establish its intended ground domain. I
therefore do not label the rule unsound.

No rule encodes the task's answer as an oracle, replaces the function call,
bypasses control, fabricates results for a used construct, or permits an
incorrect result on the intended domain.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. The final fresh mutation is
`evidence/spec-vacuity.k`; the command record is
`evidence/07_nonvacuity.sh` / `evidence/07_nonvacuity.log`.

The mutation changes the result-bearing loop obligation:

```text
largest_negative => negFold(VS,A) +Int 1
```

The state `VS=.ValSeq`, `A=0`, `B=0`, `OLD=0` satisfies all preconditions. A
real empty loop leaves `largest_negative=0`, while the mutation requires 1.

The dry-run command built the spec successfully and exited 0. The actual
command:

```text
timeout 180 kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1, did not time out, and emitted `WarnStuckClaimState` with the expected
unmet implication:

```text
#Not ( { A #Equals A +Int 1 } )
VS #Equals .ValSeq
```

No parser, missing-import, missing-hook, or unrelated build failure occurred.
This is valid non-vacuity evidence.

For completeness, `spec-vacuity-initial.k` and
`07_nonvacuity_initial.log` preserve an earlier entry-result mutation that
wandered into an unrelated unsupported float hook. I rejected it and do not
use it to support this stage.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied MPY semantics and K's proof engine, for every
finite `VS` consisting of K integers, execution of the exact translated
`largest_smallest_integers` function from the claim's initial configuration
reaches a returned tuple whose components are:

- `noneV` if no negative was accumulated, otherwise the value computed by
  `negFold(VS,0)`;
- `noneV` if no positive was accumulated, otherwise the value computed by
  `posFold(VS,0)`.

The auxiliary reachability claim establishes the loop's state transformation
for arbitrary finite tails and invariant-compatible accumulators. The proof
executes the real assignments, comparisons, branches, loop binding,
continuations, function call, and return. This is a partial-correctness result;
it is not a theorem about inputs outside the stated list-of-integers domain.

By inspection of disjoint equations and ordinary integer order, `negFold` is
the greatest negative input (or zero sentinel) and `posFold` is the least
positive input (or zero sentinel). Hence the returned K tuple implements the
natural-language contract.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied `reference-semantics` tree | Both claims and all execution | Acceptable by `SUPPLIED_SEMANTICS`; recursive byte identity was independently verified. |
| K 7.1.293 compiler, Haskell/LLVM backends, reachability prover, and built-in `Int`/`Bool`/`Map`/`List` theories | Builds, execution, and `#Top` | Standard unavoidable toolchain trust boundary. |
| Trusted `py2mpy.py` translation contract | Link from Python source to `solution.mpy` | Acceptable benchmark input; byte regeneration and AST/body checks support the link. |
| `intValue` projection and priority iterator bridge | Loop and entry claim closure | Sound on the complete ground integer domain; typed universal connection is machine-checked. Exact `Val+isInt` proof-form limitation is the primary concern. |
| `negStep`/`posStep`/fold/optional equations | Meaning of the returned symbolic postcondition | Truthful, terminating, and guard-complete on the claim domain. Set-theoretic extrema correspondence is an informal ordinary-mathematics bridge, recorded as a concern. |
| Mapping “list of integers” to finite MPY `list(ValSeq)` with `allInts` | Formal-domain adequacy | Materially aligned and unbounded. CPython Bool-versus-MPY Bool is a nonmaterial edge ambiguity. |
| Trusted canonical Python oracle and differential sample | Program-to-intent empirical support only | Zero mismatches on the recorded 21,548 inputs; finite and not treated as proof. |

There is no reachable proof-local opaque result, external call oracle, assumed
program helper, hidden compiled definition, or empirical premise standing in
for execution.

### Validation gates and decision

- Gate A, real-program soundness: **PASS**. The real constructor body executes;
  state/control are preserved; the only bridge has complete ground-domain
  justification; equations are sound; witnesses exist; body and postcondition
  mutations are discriminating.
- Gate B, intent adequacy: **PASS** for unrestricted finite integer lists. The
  fold-to-extrema correspondence is simple but not separately proved in K.
- Gate C, trust and evidence auditability: **PASS**, with the exact-form bridge
  theorem/backend limitation and missing standalone fold-extrema theorem
  explicitly exposed.

The non-fatal limitations warrant the benchmark's `CONCERNS / LEGIT`
classification. They do not materially narrow the HumanEval domain, substitute
another program, make the theorem vacuous, or enable a false conclusion.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
