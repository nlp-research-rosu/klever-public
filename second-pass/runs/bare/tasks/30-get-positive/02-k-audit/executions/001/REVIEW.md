# Independent adversarial review: 30-get-positive

## Executive conclusion

The reconstructed K proof is legitimate for its stated formal domain: finite
`PyList` values containing mathematical integers.  It executes the exact
constructor AST submitted in `solution.mpy`, reaches a fully defined stable
filter function, closes all eight positive claims, rejects a false result, and
is sensitive to a material body change.  I found no unsound local rule and no
unconstrained result-bearing symbol.

The qualification is an intent-domain limitation.  The prompt annotates only
`list` and says “numbers”; the Python implementation and canonical solution
also work on floats and other values for which comparison with zero succeeds.
The K theorem models only mathematical integers.  That does not make a false
statement provable on the modeled domain, but it prevents an unqualified proof
over the entire Python-level domain suggested by the prompt.  The appropriate
decision is therefore legitimate with concerns.

All candidate prose, traces, caches, and prior proof output were treated only
as untrusted claims.  The commands below used K v7.1.293, recorded in
[`evidence/00_toolchain.log`](evidence/00_toolchain.log).

## 1. Input and provenance integrity

### Trusted-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent (including as a symlink), exactly as
this mode requires.  There is no trusted hidden semantics and no infrastructure
contradiction.  I therefore audited the candidate's own `semantic.k`.

### Artifact checks

All required artifacts are present as regular files: `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
`prove.sh`, `run-input.json`, `metrics.json`, `codex-last.txt`, and
`codex-output.log`.  One regular JSONL structured trace is present.  There are
no symlinks anywhere under `/candidate`, and no required artifact is missing,
mistyped, or replaced by another file type.  There are no generated helper K
files beyond the three submitted K sources.

The candidate also contains non-source extras: `semantic-kompiled/`,
`__pycache__/`, and `codex-trace/`.  The first two are generated caches and were
not copied into scratch or used.  The trace was read only as an untrusted
generation record.  These extras are not required source artifacts and do not
alter the generated-semantics integrity boundary.

The trusted/candidate prompt pair is byte-identical with SHA-256
`278875ddc3e598e47227263e6384f3c169b8526e9ab6475e52e939d6a151f00b`.
The trusted/candidate translator pair is byte-identical with SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The complete manifest, types, sizes, hashes, symlink scan, and top-level extras
are in [`evidence/01_integrity.log`](evidence/01_integrity.log); the check
exited 0.

`run-input.json` identifies problem `30-get-positive`, condition `bare`, and no
supplied semantics.  `metrics.json` claims a successful, non-timed-out
generation.  `codex-last.txt` and `codex-output.log` claim `#Top` and 1,000
random checks.  The structured trace has 120 valid JSON records and no invalid
line.  These claims were not relied on.  Their complete-input hashes, parsed
metadata, bounded claim extraction, and record-type counts are preserved in
[`evidence/02_generation_claims.log`](evidence/02_generation_claims.log);
the reader script is
[`evidence/trace_summary.py`](evidence/trace_summary.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From the trusted prompt and canonical implementation, the task is:

> Given a list of numbers, return a new list containing exactly the elements
> strictly greater than zero, preserving their original order and duplicates.

The canonical body is `[e for e in l if e > 0]`; the candidate body is
`[x for x in l if x > 0]`.  They are the same algorithm up to the bound
comprehension variable's name.  Negative values and zero are dropped; positive
values are retained; the empty list produces the empty list.

### Trusted regeneration

In scratch, the command embodied by
[`evidence/regenerate_check.sh`](evidence/regenerate_check.sh) ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/30-get-positive/solution.py
cmp submitted regenerated
```

The trusted translator exited 0.  The regenerated and submitted `solution.mpy`
are byte-identical, both with SHA-256
`92acaeeccce1f8907e2664861a7e9d8bf55ff096565d6f05e1aff1a8fbdfa2ee`.
See [`evidence/03_regenerate_mpy.log`](evidence/03_regenerate_mpy.log).

### Independent differential

The reviewer-authored
[`evidence/differential.py`](evidence/differential.py) imports
`/reference/canonical.py` and the scratch copy of `solution.py` independently.
It checks:

- both documented examples;
- empty, zero-only, negative-only, and positive-only lists;
- the branch boundary `[-1, 0, 1]`;
- duplicates and order;
- arbitrarily large integers;
- float boundaries, including infinities and signed zero;
- Python booleans as numeric subclasses; and
- 120 deterministic generated lists, seed `20260723`, lengths 0 through 35,
  with integers in `[-1000,1000]` and selected fractional boundary values.

All 130 cases matched.  The log records every named boundary result, generator
scope, seed, input-scope digest, zero mismatches, and exit 0:
[`evidence/04_differential.log`](evidence/04_differential.log).  This is finite
evidence for Python implementation fidelity, not a replacement for the K
reachability proof.

## 3. Clean proof reconstruction

Only the source artifacts needed to execute the program and proof were copied
to `/tmp/audit-work/30-get-positive`.  No candidate `*-kompiled` directory,
cache, binary definition, or prior result was reused.

### Fresh definitions

The concrete definition was built from `semantic.k` with:

```text
/usr/bin/kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

It exited 0; see
[`evidence/05_kompile_llvm.log`](evidence/05_kompile_llvm.log).
The independent proof definition was built from the same source with:

```text
/usr/bin/kompile --backend haskell semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

It exited 0; see
[`evidence/06_kompile_haskell.log`](evidence/06_kompile_haskell.log).
`verification.k` contains claims rather than executable proof rules, so it and
`spec.k` were loaded as specification sources by `kprove`, rather than being
smuggled into a candidate-provided compiled definition.

### Fresh generated-semantics execution

The reviewer-authored
[`evidence/concrete_compare.py`](evidence/concrete_compare.py) invoked the
fresh LLVM definition separately for seven integer-list inputs: empty, zero,
the `-1/0/1` boundary, both prompt examples, duplicates/order, and
100-digit-magnitude integers.  It decoded the JSON KAST result and compared it
with both Python implementations.  Every `krun` exited 0 and all seven
three-way comparisons matched.  Exact `krun` commands, inputs, K results,
Python results, and statuses are in
[`evidence/07_concrete_compare.log`](evidence/07_concrete_compare.log).

### Fresh positive proofs

The original modules were proved independently:

```text
/usr/bin/kprove spec.k --definition proof-kompiled \
  --spec-module VERIFICATION
#Top
EXIT_STATUS: 0

/usr/bin/kprove spec.k --definition proof-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

The complete bounded outputs are
[`evidence/08_kprove_verification.log`](evidence/08_kprove_verification.log)
and [`evidence/09_kprove_spec.log`](evidence/09_kprove_spec.log).

For an additional one-target-at-a-time check, I made a label-only duplicate of
the exact three helper claims and exact five spec claims:
[`evidence/spec-audit-labeled.k`](evidence/spec-audit-labeled.k).  Each of the
eight labels was selected in a separate `kprove` invocation.  Every invocation
printed `#Top` and exited 0.  The harness, commands, and results are
[`evidence/run_individual_proofs.sh`](evidence/run_individual_proofs.sh) and
[`evidence/10_individual_positive_claims.log`](evidence/10_individual_positive_claims.log).

Thus every positive target is present and closes under a freshly compiled
definition.

## 4. Adequacy and real-program pinning

### Plain-language claims

The three `VERIFICATION` claims say:

1. On a nonempty integer list whose head `I` is positive, executing the exact
   submitted program returns `I` followed by the stable filtered tail.
2. On a nonempty integer list whose head is zero or negative, executing the
   exact submitted program returns the stable filtered tail.
3. On the empty integer list, executing the exact submitted program returns
   the empty list.

Their preconditions are respectively `I > 0`, `I <= 0`, and an exact empty
input.  Positive witnesses are `cons(1,nil)`, `cons(0,nil)`, and `nil`.

The five `SPEC` claims say:

1. Universally for `INPUT:PyList`, the exact program reaches
   `filterGt(INPUT,0)`.
2. Each of the two prompt examples reaches its displayed expected result.
3. Empty input reaches `nil`.
4. The exact all-nonpositive input `[0,-1,-2]` reaches `nil`.

The universal precondition is inhabited by `INPUT=nil`; the four concrete
preconditions are their displayed configurations.  Substitution of all these
witnesses is covered by the concrete execution log: `nil`, `[1]`, `[0]`, both
examples, and the all-nonpositive/mixed boundary cases all agree with both
Python implementations.  Ground mutation witnesses are also explicit in
[`evidence/14_mutation_witness.log`](evidence/14_mutation_witness.log).

### Program and result pinning

Every claim's starting `<k>` term is structurally the complete submitted
`solution.mpy`:

```text
Module(FuncDef("get_positive", Params("l"),
  Return(ListComp(Name("x"),
    CompFor(Name("x"), Name("l"),
      Compare(Name("x"), CmpOp(">", Int(0))))))))
```

This is the sole program term regenerated by the trusted translator.  It is
not a substituted helper call.  The entry rule decomposes that module and
function body; the evaluation rule then matches the actual list-comprehension
AST, including iterable name, bound-name relationship, comparison operator,
and zero threshold.

The universal result is not a free or existential variable:
`filterGt(INPUT,0)` is a recursively defined function with disjoint,
constructor-covering equations.  The result is an equality-bearing destination
term, not a one-way implication or tautology.  The concrete claims further pin
ground results.

There is no loop claim because the source uses a comprehension, not an
explicit submitted loop.  The three helper claims match real constructor cases
after the program's actual entry and evaluation rules; each is independently
derivable from those rules.

As a body-sensitivity check, I changed only the inlined source threshold from
`0` to `1` while retaining the original summary.  The changed artifact parsed
and built, then `kprove` exited 1 with `WarnStuckClaimState` at the unmet
equality `filterGt(INPUT,1) = filterGt(INPUT,0)`.  Input `[1]` is the ground
witness.  See
[`evidence/spec-body-sensitivity.k`](evidence/spec-body-sensitivity.k),
[`evidence/15_body_mutation_dry_run.log`](evidence/15_body_mutation_dry_run.log),
and
[`evidence/16_body_mutation_expected_failure.log`](evidence/16_body_mutation_expected_failure.log).
This establishes that the theorem is sensitive to a material program-body
change.

## 5. Rule-by-rule static soundness review

The numbered source and declaration/attribute scan are preserved in
[`evidence/11_static_inventory.log`](evidence/11_static_inventory.log).  The
inventory below covers every local declaration and rule.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` defines twelve data/AST productions:

1. `Pgm`: `Module(Function)`;
2. `Function`: `FuncDef(String,Params,Stmt)`;
3. `Params`: `Params(String)`;
4. `Stmt`: `Return(Expr)`;
5. through 8. `Expr`: `Name(String)`, `Int(Int)`,
   `ListComp(Expr,CompFor)`, and `Compare(Expr,CmpOp)`;
9. `CompFor`: `CompFor(Expr,Expr,Expr)`;
10. `CmpOp`: `CmpOp(String,Expr)`;
11. and 12. `PyList`: constructor `nil` and constructor
    `cons(Int,PyList)`.

`SEMANTIC` adds three evaluator/helper productions:
`eval(Expr,Map):KItem`, `asList(KItem):PyList`, and
`filterGt(PyList,Int):PyList`.  `asList` and `filterGt` carry `[function]`;
neither carries `[total]`.

There is one configuration:

```text
<py>
  <k> $PGM:Pgm </k>
  <input> $INPUT:PyList </input>
</py>
```

No heap, call stack, allocation counter, output, or exception cell exists.
That is adequate for the submitted pure, single-function, integer-list value
computation.  The external initial configuration represents invocation of the
sole `get_positive` definition with `<input>` as its argument.

Every submitted construct is covered:

- `Module`, `FuncDef`, `Params`, and `Return` are declared and consumed by the
  entry rule.
- `ListComp`, `CompFor`, the three occurrences of `Name`, `Compare`, `CmpOp`,
  and `Int(0)` are declared and consumed by the comprehension rule.
- The formal argument is represented by a singleton K `Map`; input and result
  lists are represented by free `nil`/`cons` constructors.

No used source construct is silently unmodeled.  Missing semantics for other
Python constructs is acceptable in generated-semantics mode and causes a
visible stuck term rather than a fabricated result.

There are exactly two local function declarations, six semantic rules, three
helper claims, and five spec claims.  There are no local `total`,
`functional`, opaque, priority, simplification, `concrete`, `owise`,
`anywhere`, macro, alias, or trusted declarations.

### The six semantic rules

1. **Function entry (lines 37–39).**  It matches only a module containing
   `get_positive` with one parameter and a `Return(E)` body, reads the `PyList`
   input, and rewrites to `eval(E,P |-> L)`.  It preserves the input cell and
   any `<k>` suffix.  Under the explicitly chosen external-call convention,
   singleton binding and immediate evaluation of the return expression are
   faithful.  The actual claim fixes `P="l"` and the exact body, so the rule
   cannot select another submitted binding.

2. **`asList` projection (line 43).**  `asList(L:PyList) => L` is true on its
   guard-by-sort.  It has no equation for a non-list `KItem` and is not declared
   total, so ill-typed lookup values get stuck rather than being invented.  In
   every actual entry execution the lookup is the `PyList` just stored under
   the formal name.

3. **Comprehension evaluation (lines 47–52).**  This is a high-level
   operational semantic bridge for precisely the used comprehension shape.
   Reusing `X` in the produced element, generator target, and predicate enforces
   the binding relation; matching `P` in `Name(P)` and looking up `RHO[P]`
   evaluates the iterable binding; matching the literal operator `">"` and
   integer `N` fixes the comparison.  It rewrites to
   `filterGt(asList(RHO[P]),N)`.  The expression is pure on the modeled
   integer-list domain, the arbitrary active suffix is syntactically preserved,
   and the only observable state cell is unchanged.  Hence the broad suffix
   does not hide return, exception, output, or state effects.  The bridge is
   task-specialized but not an oracle: its result-bearing helper is completely
   defined by the next three equations.

4. **Empty filter (line 57).**  `filterGt(nil,N) => nil` is the correct stable
   filter base case.

5. **Positive-head filter (lines 58–59).**  If `I > N`, the equation retains
   `I` and recursively filters `IS`.  It preserves order and duplicates.

6. **Nonpositive-head filter (lines 60–61).**  If `I <= N`, the equation drops
   `I` and recursively filters `IS`.

For mathematical integers, the guards in rules 5 and 6 are disjoint and
exhaustive.  Both recurse on the strict constructor tail, so they descend.
Together with the `nil` rule, `filterGt` is fixed on every finite constructor
`PyList`, despite not relying on a `[total]` assertion.  The `asList` and
`filterGt` equations do not overlap inconsistently.

### Proof-local inventory

`verification.k` declares no syntax, function, ordinary rule,
simplification, priority, opaque symbol, or trusted axiom.  Its only extensions
are the three reachability claims inventoried in Stage 4.  They are derived
lemmas: entry plus comprehension evaluation plus the applicable one-step
`filterGt` equation yields the displayed destination.  The positive and
nonpositive guards are disjoint and cover integer heads; the empty claim covers
the remaining list constructor.

`spec.k` likewise adds no semantic rule or symbol.  Its five reachability
claims are proof targets.  The universal claim follows directly from entry,
lookup/projection, and comprehension evaluation; the concrete claims also
normalize `filterGt`.

Imported K `INT`, `MAP`, and string syntax are the only lower-level primitives.
No local rule encodes a ground expected answer, bypasses the actual AST,
introduces an unconstrained value, changes control abruptly, or fabricates
behavior for a missing used construct.

I found no false conclusion witness for any local rule, and therefore do not
label any rule unsound.  The narrower issue is adequacy: the bridge models
integer-list value semantics, not all Python values or allocation identity.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was
needed or trusted.

I created
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k), which changes
the universal result from `filterGt(INPUT,0)` to the deliberately false
`cons(1,filterGt(INPUT,0))`.  The precondition remains satisfiable.  At
`INPUT=nil`, both Python implementations and fresh K execution return `nil`,
whereas the mutated destination is `cons(1,nil)`; the witness is recorded in
[`evidence/14_mutation_witness.log`](evidence/14_mutation_witness.log).

The dry run built the mutation successfully and exited 0:
[`evidence/12_mutation_dry_run.log`](evidence/12_mutation_dry_run.log).
The actual proof then exited 1, emitted `WarnStuckClaimState`, and displayed the
unmet equality between `cons(1,filterGt(INPUT,0))` and
`filterGt(INPUT,0)`: see
[`evidence/13_mutation_expected_failure.log`](evidence/13_mutation_expected_failure.log).
This is the expected result-bearing failure, not a parser, import, timeout, or
unrelated backend error.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the submitted generated K definition and K's reachability logic:

- for every formal `INPUT:PyList`, executing the exact submitted constructor
  program from the configured external entry reaches
  `filterGt(INPUT,0)` and leaves `<input>` unchanged;
- the three constructor-boundary helper claims hold;
- both prompt examples, empty input, and the displayed all-nonpositive input
  reach their exact expected lists; and
- the result is discriminating and body-sensitive.

This is a partial-correctness result.  For finite ground constructor lists,
the structurally descending `filterGt` equations also give concrete
termination, but the audit does not elevate that observation into a separate
total-correctness theorem.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, and reachability engine | All builds, execution, and `#Top` results | Ordinary unavoidable toolchain trust; fresh outputs and statuses are preserved. |
| Imported K `INT`, `MAP`, and string syntax | Mathematical comparison, singleton environment, lookup, and AST tokens | Acceptable low-level trusted primitives.  Their use does not encode the task answer. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | The translator is an authority supplied by the audit.  Fresh regeneration is byte-identical, so the proof term pins its output for this source. |
| External-entry configuration convention | Treats the module's sole `get_positive` definition as invoked with `<input>` | Informal harness bridge, explicit and appropriate for this single-function task; it affects call setup but does not supply the returned value. |
| `PyList` versus Python list values | Interprets `nil`/`cons` as finite immutable list values | Sound for value-level finite integer lists.  Python allocation identity and mutation are outside the theorem and immaterial to the stated return-value examples. |
| High-level comprehension rule | Replaces the exact pure used AST with `filterGt` | Program-derived and result-bearing, but not opaque or circular: the rule fixes binding/operator/threshold, and `filterGt` has truthful exhaustive recursive equations.  Static reasoning supplies the universal connection on integer lists; seven K/Python executions provide finite corroboration. |
| Stable-filter intent bridge | Reads the recursive equations as “preserve order/duplicates and keep exactly values greater than zero” | Ordinary induction on finite lists and integer order justifies it.  It is not separately stated as a K theorem, so its adequacy was audited rule-by-rule. |
| Python implementation versus canonical | Connects the candidate source to HumanEval intent | The bodies are alpha-equivalent comprehensions; 130 independent differential cases are supporting finite evidence, not the K proof. |
| Element domain | K uses mathematical `Int`; Python prompt says unparameterized `list` of “numbers” | Documented limitation.  Floats and other successfully comparable values are outside the K theorem even though both Python functions handle them. |

There are no fresh opaque symbols, unconstrained oracles, empirical rewrite
rules, proof-local ordinary rules, or unstated trusted claims.  Differential
testing supports only the tested Python and K/intent bridges; it is not used as
a substitute for `kprove`.

### Validation gates and decision

- **Gate A — real-program soundness: PASS.**  The exact translated body
  executes, all result-bearing helpers are defined, all positive claims close
  freshly, and both result and body mutations are rejected meaningfully.
- **Gate B — intent adequacy: FAIL with a bounded scope limitation.**  The
  theorem faithfully covers finite integer lists but does not formalize the
  broader numeric Python domain suggested by the prompt.  This is
  sound-but-limited, not an unsound proof.
- **Gate C — trust and auditability: PASS.**  Commands, statuses, bounded
  outputs, sources, witnesses, finite test scopes, and trust assumptions are
  preserved under `/audit-output/evidence/`.

The Gate B limitation warrants `CONCERNS`, while Gate A establishes that the
candidate nevertheless contains a legitimate partial-correctness proof for the
formal integer-list domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
