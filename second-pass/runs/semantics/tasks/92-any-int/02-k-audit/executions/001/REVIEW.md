# Independent adversarial audit: 92-any-int

The candidate is **not a legitimate partial-correctness proof of the real
generated Python program**. The K claims reconstruct and are non-vacuous, but
two independent real-program gates fail:

1. The formal model proves the false result `False` for the satisfying formal
   input `(true, 1, 2)`, while both `/reference/canonical.py` and the submitted
   `/candidate/solution.py` return `True`.
2. The entry claims start from a proof-only `#anyInt` symbol that constructs a
   hand-embedded closure. They never load or invoke `/candidate/solution.mpy`,
   and there is no bridge-free connection theorem from the real module-load and
   name-lookup path to this shortcut.

All execution was performed from source-only copies below
`/tmp/audit-work`. Candidate-built caches and definitions were not used. The
reviewer scripts, exact commands, statuses, bounded logs, mutations, and test
corpus are under [`evidence/`](evidence/).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no rendered-mode
infrastructure contradiction and a candidate verdict is appropriate.

I compared entry types and symlink targets for the entire candidate semantics
tree, then ran:

```text
diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
```

Both the type inventory and recursive content comparison exited 0. There are no
symlinks, missing entries, added entries, mistyped entries, or changed bytes in
`/candidate/reference-semantics`. The candidate prompt and translator also
compare byte-for-byte equal to `/reference/prompt.py` and
`/reference/py2mpy.py`. Commands, statuses, and SHA-256 values are in
[`01_integrity.log`](evidence/01_integrity.log).

### Missing generation records

The following requested untrusted records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. These absences prevent review of the
generation history, but do not create infrastructure uncertainty because the
proof was independently reconstructed. `/candidate/spec-vacuity.k` and
`/candidate/PROOF.md` are also absent; the former was replaced by a fresh
reviewer mutation in stage 6. The environment, K version, source hashes, and
artifact manifest are recorded in
[`07_environment_manifest.log`](evidence/07_environment_manifest.log).

Stage result: the supplied-semantics and trusted-input integrity checks pass;
generation provenance is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`, `any_int(x, y, z)`
returns true exactly when all three values satisfy Python
`isinstance(value, int)` and at least one of these equalities holds:

```text
x + y == z
x + z == y
y + z == x
```

It returns false otherwise. The examples include positive, negative, false, and
non-integral-float cases. Under real Python, `bool` is a subclass of `int`; this
fact becomes material in stages 4 and 5.

The submitted `solution.py` replaces the reference's nested `if` statements
with the same short-circuit Boolean expression. It preserves the ordering of
the three type tests and evaluates addition only after all three succeed.

### Trusted retranslating

The exact command

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

exited 0. `cmp -s` against the submitted `solution.mpy` exited 0; both files
have SHA-256
`f637e45fc0c6da706b0a5481b60953133849f72bc16bdd1f01c3c9e5d384c26c`.

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the solution from the clean scratch copy.
It covers:

- all four documented examples;
- a witness for each equality orientation;
- none-equal, zero, negative, and large-arbitrary-precision cases;
- a non-integer in each argument position;
- `NaN`, infinity, and Python `bool`;
- the full Cartesian product of 16 boundary values, giving 4,096 cases;
- 2,000 deterministic generated cases, including each true branch,
  off-by-one false cases, broad random integers, and 100 very large integers.

The exact 6,113-input corpus is
[`differential_inputs.json`](evidence/differential_inputs.json). The test exited
0 with `mismatch_count=0`; see
[`02_fidelity.log`](evidence/02_fidelity.log). This is finite evidence that the
two Python implementations agree. It is not a K connection theorem.

Stage result: program and translation fidelity pass at the Python/MPY artifact
level.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`; no
`*-kompiled` directory, `__pycache__`, `.pyc`, or candidate cache was copied.
The installed toolchain was K `v7.1.337`.

The following fresh commands all succeeded:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun audit-concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module ANY-INT-VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module ANY-INT-SPEC
```

The LLVM build exited 0. The trusted-retranslated concrete program ended with
`.K`, `NoExc`, and exit code 0. The Haskell build exited 0. The combined
`kprove` invocation exited 0 and printed `#Top`. Complete bounded output is in
[`03_reconstruct.log`](evidence/03_reconstruct.log).

Because the four candidate claims are unlabeled, I placed exact copies of each
claim in a separate reviewer module and ran each independently:

| Claim | Reviewer module | Exit | Output |
|---|---|---:|---|
| all K `Int` values | `SPEC-CLAIM-INTEGERS` | 0 | `#Top` |
| non-`Int` `X` | `SPEC-CLAIM-X-NONINT` | 0 | `#Top` |
| `Int X`, non-`Int Y` | `SPEC-CLAIM-Y-NONINT` | 0 | `#Top` |
| `Int X,Y`, non-`Int Z` | `SPEC-CLAIM-Z-NONINT` | 0 | `#Top` |

The exact split claims are in
[`evidence/claim-specs/`](evidence/claim-specs/), and all four commands and
outputs are in [`03_claims.log`](evidence/03_claims.log).

The builds report non-exhaustive-totality warnings in unrelated helpers such as
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`, plus unused
variables in `strLt`. None of those terms is reachable from this program. They
are retained in the evidence rather than suppressed.

Stage result: verification closure passes. This establishes closure only under
the supplied K theory plus `verification.k`; it does not resolve the soundness
and pinning failures below.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Every claim fixes the same initial configuration: environment 0; an empty
module scope whose parent is the builtins scope; fresh scope location 1; empty
heap and stack; `noRet`; `NoExc`; and exit code 0.

1. For all K-sort `Int` values `X`, `Y`, and `Z`, `#anyInt` must return the
   Boolean disjunction of the three integer-sum equalities.
2. For arbitrary K `Val` values `X`, `Y`, and `Z`, if `isIntV(X)` is false,
   `#anyInt` must return `false`.
3. If `X` is a K `Int` and `isIntV(Y)` is false, it must return `false`.
4. If `X` and `Y` are K `Int` values and `isIntV(Z)` is false, it must return
   `false`.

The destinations are result-constraining. They contain either the explicit
Boolean `false` or the exact `sumCondition(X,Y,Z)` formula; there is no free
result variable, implication-only postcondition, omitted result cell, or
tautological destination.

### Satisfiable preconditions and substitutions

Each precondition has a concrete witness:

| Claim | Witness | Claimed result | Canonical | Solution |
|---|---|---:|---:|---:|
| 1 | `(5, 2, 7)` | `True` | `True` | `True` |
| 2 | `(1.5, 2, 3)` | `False` | `False` | `False` |
| 3 | `(1, 2.5, 3)` | `False` | `False` | `False` |
| 4 | `(1, 2, 3.5)` | `False` | `False` | `False` |

These substitutions and both Python results are reproduced in
[`04_adequacy.log`](evidence/04_adequacy.log).

### The `<k>` cell does not execute the submitted module

The actual submitted MPY program begins with:

```text
Module(FuncDef("any_int", Params("x", "y", "z"), Return(...)))
```

Fixed semantics would enter through `#loadAll(Module(...))`, execute the
`FuncDef` rule to bind `any_int`, resolve that binding through `Name` lookup,
and then call the resulting closure. None of the candidate entry claims has
that term.

Instead, `/candidate/verification.k:27-32` declares a fresh `#anyInt` symbol and
rewrites it directly to:

```text
#applyK(
  toCall(closureVal(("x", "y", "z"), anyIntBody, 0)),
  (X, Y, Z, .Vals))
```

`anyIntBody` is a hand-embedded copy of the submitted function body. Static
comparison confirms that the copied AST is currently exact, and the fixed
closure-call rules then perform real parameter binding, body execution, return,
and frame restoration. But no auxiliary claim proves, without importing this
bridge, that loading and invoking `solution.mpy` universally reaches this
synthetic invocation. The fixed module-load, function-definition, and
name-binding path is bypassed.

The body-sensitivity test makes the missing dependency observable. I changed a
scratch source body to `return False`, translated it with the trusted
translator, and confirmed that its Python result for `(5,2,7)` is `False`.
Without changing `verification.k`, the original candidate proof still exited 0
and printed `#Top`. The mutation and generated MPY are
[`body_sensitivity_solution.py`](evidence/body_sensitivity_solution.py) and
[`body_sensitivity_solution.mpy`](evidence/body_sensitivity_solution.mpy);
commands and results are in
[`04_adequacy.log`](evidence/04_adequacy.log). The concrete false-conclusion
witness for the missing bridge is therefore `(5,2,7)`: the mutated real body
returns false while the still-closing synthetic theorem requires
`sumCondition(5,2,7) = true`.

This does not show that the current copied body differs textually—it does not.
It shows that source identity is an unproved manual premise, not a dependency
of the reachability proof. Under the required real-program pinning gate, that
is a substituted-program proof.

### Concrete false conclusion on the candidate's own formal domain

There is also a direct false result, with no source mutation:

```text
X = true, Y = 1, Z = 2
```

K `Bool` is included in `Val`, and
`/candidate/reference-semantics/semantics/builtins.k:294-295` defines:

```text
isIntV(_:Int) => true
isIntV(_:Val) => false [owise]
```

Thus `notBool isIntV(true)` is true and this state satisfies entry claim 2.
The K model reduces `#anyInt(true,1,2)` to `false`. A ground claim for that
result exited 0 with `#Top`. A ground claim for the real result `true` exited 1
with `WarnStuckClaimState` and residual `<k> false ~> .K </k>`.

Both Python implementations return `True`, because
`isinstance(True, int)` is true and `True + 1 == 2`. The exact same source
containing `assert not any_int(True, 1, 2)` exits 1 with `AssertionError` under
Python but completes with `.K`, `NoExc`, and exit code 0 under the freshly built
LLVM K semantics. The sources, ground claims, and outputs are in
[`concrete_bool_model.py`](evidence/concrete_bool_model.py),
[`evidence/claim-specs/`](evidence/claim-specs/), and
[`04_adequacy.log`](evidence/04_adequacy.log).

This is the required false-conclusion witness for the `isIntV` fallback rule as
a model of real Python `isinstance(_, int)`. Even if human-facing “numbers” were
read as excluding booleans, the candidate's formal claim explicitly includes
K `Bool` through `X:Val` and asserts a result for it.

There are no loop or helper reachability claims to check.

Stage result: **fail**. The proof neither machine-pins the submitted module nor
states the real program's result over its own claimed K domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`05_rule_inventory.md`](evidence/05_rule_inventory.md) inventories every
top-level local `syntax`, `configuration`, `context`, `rule`, and `claim` in the
assembled semantics, all helper K files, `verification.k`, and `spec.k`.
It contains 938 statements:

- 230 syntax declarations;
- 1 configuration;
- 5 evaluation contexts;
- 698 rules;
- 4 claims;
- 237 bracketed function/total/symbol/concrete/priority-related attribute
  occurrences.

There are no `[simplification]` or `[functional]` declarations. The inventory
also lists all function and total declarations, all 45 priority annotations,
all concrete rules, and all 25 `symbol(...)` opaque boundaries. Each statement
has one of these audit decisions:

- reachable and aligned with the declared MPY subset;
- reachable Bool/Python model-gap path;
- real module-load path bypassed by the proof;
- candidate definition accepted;
- candidate operational bridge lacking a connection theorem;
- result-constraining claim;
- fixed and statically unreachable from this AST.

For unreachable supplied rules, the inventory makes the narrower finding that
they cannot contribute to these claims; it does not assert that an unused
partial Python model is universally sound. This is sufficient to isolate the
theory actually used by this proof while still enumerating every declaration
and rule.

### Used syntax and operational rules

| Submitted construct | Declaration and operational path | Assessment |
|---|---|---|
| `Module`, `FuncDef` | `syntax.k`; `core.k` `#loadAll`; `functions.k` `FuncDef` | Sound for the subset, but bypassed by `#anyInt` |
| `Params`, `Stmts`, `Return` | `syntax.k`; `functions.k` bind/return/pop | Binding and LIFO frame restoration are correct on the claimed configuration |
| `Name` | `core.k` `#look` and parent-chain lookup | Correct lookup path; program arguments and builtins resolve in order |
| `Call` | `call.k` callee evaluation, `#evalArgs`, `#applyK` | Callee then arguments, left-to-right; correct for used calls |
| `isinstance(_, int)` | `builtinsScope`, `applyBuiltin`, `isIntV` | `Int` case correct; `Bool` fallback is false relative to Python, witnessed above |
| `BoolOp("and"/"or")` | `bool.k` head-only context and truthy short circuit | Correct evaluation order and value-return behavior on the used Boolean results |
| `BinOp("+",...)` | seqstrict syntax, `operators.k`, `int.k` | Unbounded K integer addition agrees with Python integer addition |
| `Compare(...,"==",...)` | comparison contexts, `operators.k`, `int.k` | Left then right evaluation and integer equality are correct |

The function allocates no heap objects, mutates no persistent state, emits no
output, and has no exceptional path after the three type tests succeed on K
`Int` arguments. Closure invocation temporarily changes `env`, `scopes`,
`scopeLoc`, `stack`, and `ret`; the fixed call/return rules restore the claimed
initial cells. The candidate bridge itself frames all those cells and has no
guard tying them to a loaded `any_int` binding.

### Candidate-local extension inventory

| Extension | Class and complete domain | Static decision |
|---|---|---|
| `anyIntBody` and its equation | Definitional constant of sort `Stmts`, `[function,total]`; one unconditional equation | The equation is terminating, non-overlapping, and currently equals the translated function body. It does not itself connect to the source file. |
| `#anyInt(Val,Val,Val)` rule | Operational bridge; any three K `Val` arguments, arbitrary framed continuation and omitted cells | Illegitimate for real-program pinning. It constructs a hard-coded closure at defining scope 0 and skips module load, binding selection, and name lookup. There is no bridge-free universal connection theorem. The body-sensitivity witness is `(5,2,7)`. |
| `sumCondition(Int,Int,Int)` equation | Definitional mathematical summary, `[function,total]`; all K integers | Sound, terminating, complete, and non-overlapping. Its three disjuncts exactly match the source expression. |
| Four entry claims | Reachability claims | Result-constraining and satisfiable, but dependent on the unconnected bridge and the false Bool type relation. |

There are no candidate priority rules, ordinary semantic shortcuts besides
`#anyInt`, simplification rules, opaque symbols, lemmas, or loop circularities.

### Functions, overlaps, priorities, and opaque boundaries

On the used path, `anyIntBody` and `sumCondition` each have one exhaustive
equation. `isIntV` has an `Int` equation and an `owise` equation, so its K guards
are operationally disjoint and covering; the defect is the meaning assigned to
K `Bool`, not rule overlap. The relevant integer addition/equality cases are
sort-disjoint from the other operator cases. No priority rule is needed on the
ordinary Int/Bool path; ref/cell priority rules cannot match the exact empty
heap and plain parameter bindings used here.

The supplied proof theory contains these 25 named symbol boundaries:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. None can occur on this submitted body:
non-Int values short-circuit before arithmetic, while all arithmetic in the
success branch is K `Int`. They are therefore inert trust boundaries for these
claims, not hidden result oracles.

Stage result: **fail**, based on the witnessed `isIntV` false conclusion and the
unconnected `#anyInt` operational bridge. No other inventoried rule is labeled
unsound without a witness.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k), containing only the
integer entry claim with its result changed from:

```text
sumCondition(X,Y,Z)
```

to:

```text
notBool sumCondition(X,Y,Z)
```

This is a meaningful result mutation. `(5,2,7)` satisfies the precondition, the
original result is true, and the mutated result is false.

The dry-run command parsed and built the mutation successfully:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
```

It exited 0. The live proof command exited 1 with `WarnStuckClaimState`,
`WarnUnexploredBranches`, and an unmet branch condition including
`Z #Equals X +Int Y`. This is an obligation failure, not a parse error,
missing import, timeout, or unrelated crash. Exact commands, statuses, and
bounded output are in
[`06_nonvacuity.log`](evidence/06_nonvacuity.log), with the raw dry-run and
proof outputs in
[`06_nonvacuity_dry_run.log`](evidence/06_nonvacuity_dry_run.log) and
[`06_nonvacuity_proof.log`](evidence/06_nonvacuity_proof.log).

Stage result: non-vacuity passes. It shows that the synthetic K theorem
constrains its result; it does not connect that theorem to the real program.

## 7. Proven-versus-assumed accounting and decision

### What the successful K proof establishes

Under the exact supplied K definition plus `verification.k`, and starting from
the exact cells in `spec.k`, symbolic execution of the proof-only
`#anyInt(X,Y,Z)` term has these partial-correctness results:

- for three K `Int` values, termination yields the Boolean disjunction of the
  three sum equalities;
- when the first non-K-`Int` occurs at `X`, `Y`, or `Z`, termination yields
  `false`.

That is what the fresh `#Top` proves. It does not prove termination. It does not
start with the `Module` in `solution.mpy`. It does not prove that the
hand-embedded closure is universally equivalent to loading and calling the
submitted program. It also does not establish real Python behavior for K
`Bool`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.337`, Haskell/LLVM backends, K Int/Bool/Map/List/String hooks | All build, concrete, and proof results | Necessary low-level trust boundary; commands and versions are recorded |
| Supplied semantics tree | All operational execution | Integrity verified exactly; acceptable as the selected fixed theory, but its `isIntV(Bool)` interpretation is not a faithful bridge to real Python |
| Trusted `/reference/py2mpy.py` | Python-to-MPY artifact relation | Trusted input; byte identity of regenerated and submitted MPY is proved empirically |
| Manual equality of `anyIntBody` and current MPY function body | Every entry claim | Static fact for this candidate, but not machine-connected to the entry theorem |
| `#anyInt` equals real module load, binding, lookup, and call | Every entry claim | Unproved and illegitimate; body-sensitivity test confirms proof independence from `solution.mpy` |
| `isIntV` models Python `isinstance(_, int)` | All non-Int claims and branch reachability | False for K Bool; `(true,1,2)` is the concrete false-conclusion witness |
| `sumCondition` equations | Integer result claim | Acceptable ordinary mathematics, fully defined over K Int |
| 25 supplied opaque symbols | None of these claims | Acceptable here only because static reachability shows they cannot affect control, state, or result |
| Python differential test | Candidate-versus-canonical intent bridge | 6,113-case finite support only; not a universal proof and not a K connection theorem |
| Termination | None proved | Explicitly outside partial correctness |
| Python values not representable as MPY `Val` | Natural-language coverage | Excluded by the formal model; secondary limitation for a prompt phrased as “numbers” |

### Decision

Fresh construction and non-vacuity are necessary but not sufficient. The
candidate proves a discriminating theorem about a synthetic invocation under
the supplied K theory. It fails the real-program pinning requirement and, more
decisively, proves a concrete result that is false for both real Python
implementations on a satisfying formal input. Either defect independently
precludes `LEGIT`; together they require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
