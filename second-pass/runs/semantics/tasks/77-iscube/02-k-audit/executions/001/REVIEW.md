# Independent adversarial audit: 77-iscube

This audit used the supplied-semantics path mandated for
`SUPPLIED_SEMANTICS`. All candidate content was treated as untrusted. Fresh
work was performed in `/tmp/audit-work/77-iscube.RDpOYi`; no candidate-built
definition or cache was present or reused. Reviewer-authored artifacts and
bounded command logs are under `/audit-output/evidence/`.

The reconstructed K claims all print `#Top`, but they are not a legitimate
proof of the submitted program. The proof replaces the program-derived
floating-point cube-root computation with an opaque integer oracle and then
adds a simplification rule that directly supplies the ideal cube conclusion.
That rule has a concrete false-conclusion witness on the formal input domain.
The claims also call a manually injected closure rather than loading and
executing `solution.mpy`.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required in
`SUPPLIED_SEMANTICS` mode. There is no rendered-mode/mount contradiction, so
this is not an infrastructure error.

The independent recursive manifest comparison found the candidate
`reference-semantics/` byte-identical to the trusted tree. It found no missing,
additional, changed, mistyped, or symlinked entry in that tree. The candidate
`prompt.py` and `py2mpy.py` are also regular files and byte-identical to their
trusted versions:

- `prompt.py`: SHA-256
  `7396a97deb6df81d38aac289d2d195791695d2a8e14ab21f2e58366b8842b0de`
  on both sides.
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
  on both sides.

The checker and complete result are
`evidence/integrity_check.py` and `evidence/01-integrity.log`.

### Missing generation records

The following requested untrusted generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace, `PROOF.md`, or `spec-vacuity.k` is present.
The complete candidate inventory, including file types and top-level hashes,
is in `evidence/02-candidate-inventory.log`. All submitted proof/source
artifacts that are present are regular files, not symlinks. The four missing
generation records are provenance failures, but they do not prevent an
independent reconstruction from the trusted inputs.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical implementation

The contract in `/reference/prompt.py` is: for a valid integer `a`, return
`True` exactly when `a` is the cube of an integer. Cubes of negative integers
and zero count. The examples are `1 -> True`, `2 -> False`, `-1 -> True`,
`64 -> True`, `0 -> True`, and `180 -> False`.

The trusted canonical implementation takes `abs(a)`, computes a binary-float
approximation to its cube root, rounds it, cubes the resulting integer, and
compares it to the magnitude:

```python
int(round(abs(a) ** (1. / 3))) ** 3 == abs(a)
```

The submitted `solution.py` uses `1 / 3` in place of `1. / 3`. Under Python 3
both expressions produce the same binary float, so this is not a behavioral
difference.

### Trusted translation

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` regenerated a file byte-identical to submitted `solution.mpy`.
Both hashes are
`b56ee22cbe66948fa1ea4e9dbaaf9922cfda1f8f1ddc2e5512c071fe1d8398d7`.
The exact command, hashes, `cmp`, and exit 0 are in
`evidence/04-translation-byte-identity.log`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the generated entry point. Its deterministic
796-input corpus includes:

- all documented examples;
- zero (there is no “empty” value in the integer-only API);
- positive and negative cases at `n^3-1`, `n^3`, and `n^3+1`;
- both return branches and both signs;
- seeded random integers, exact cubes, and near-cubes;
- large integer precision and float-conversion boundaries.

The exact input corpus is preserved in
`evidence/differential-inputs.json`. The run exited 0 with zero
canonical-versus-generated mismatches
(`evidence/05-differential.log`).

That same run used an independent integer-only binary-search oracle for the
natural contract. It found 210 generated-versus-contract mismatches. In
particular, with

```text
N = 1000000000000000
A = N^3
  = 1000000000000000000000000000000000000000000000
```

both Python implementations return `False`, even though `A` is exactly a cube.
Python computes the floating cube root as `999999999999998.0`, two below `N`.
The focused calculation is in `evidence/16-claim-witnesses.log`.
Still larger valid integers can raise `OverflowError` instead of returning a
Boolean; those outcomes are also in the preserved differential evidence.

Thus the generated program is faithful to the canonical implementation over
the tested inputs, but neither implements the stated exact-cube contract over
all Python integers. This matters directly because the K cube claims quantify
over unbounded K `Int`.

## 3. Clean proof reconstruction

K v7.1.337 was independently available; tool versions are recorded in
`evidence/00-toolchain.log`.

### Fresh builds and concrete execution

The trusted supplied semantics and candidate sources were copied to the fresh
scratch directory. No `*-kompiled` directory or cache came from `/candidate`.

| Action | Exit | Relevant result | Evidence |
|---|---:|---|---|
| LLVM `kompile` of supplied semantics | 0 | fresh `runtime-kompiled` | `evidence/06-kompile-concrete.log` |
| `krun solution.mpy --output none` | 0 | concrete module executes | `evidence/07-krun-solution.log` |
| `krun concrete_tests.mpy --output none` | 0 | submitted small assertions execute | `evidence/08-krun-candidate-tests.log` |
| Haskell `kompile verification.k` | 0 | fresh `verification-kompiled` | `evidence/09-kompile-proof.log` |

The LLVM compiler reported non-exhaustive-match warnings in supplied, unused
general-purpose helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`). None is reached by this program. The proof build had only
unused-variable warnings from trusted `str.k`.

The fresh concrete supplied semantics also reproduced the decisive large-cube
behavior:

- an assertion that the generated program returns `False` on `10^45` exits 0
  (`evidence/large_cube_actual_false.py`,
  `evidence/12-krun-large-cube-actual.log`);
- an assertion that it returns the contract-required `True` exits 1 with
  `<exc> AssertionError </exc>` and `<exit-code> 1 </exit-code>`
  (`evidence/large_cube_false_contract.py`,
  `evidence/13-krun-large-cube-contract.log`).

### Every positive target claim

Each target was run separately. Every command exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| `ISCube-SPEC.implementation` | `evidence/10-kprove-implementation.log` |
| `ISCube-SPEC.positive-cubes` | `evidence/10-kprove-positive-cubes.log` |
| `ISCube-SPEC.negative-cubes` | `evidence/10-kprove-negative-cubes.log` |
| `ISCube-SPEC.positive-noncubes` | `evidence/10-kprove-positive-noncubes.log` |
| `ISCube-SPEC.negative-noncubes` | `evidence/10-kprove-negative-noncubes.log` |

These are genuine closure results under the extended candidate theory, but
closure is not a soundness certificate for that theory.

To test dependence on the result-supplying extension, the audit removed only
the ideal-cube simplification from a scratch copy. The modified definition
built successfully (`evidence/17-kompile-without-ideal-rule.log`), but the
positive-cubes proof then exited 1 with `WarnStuckClaimState` at the unresolved
condition
`roundedCubeRoot(N^3)^3 == N^3`
(`evidence/verification-without-ideal-cube-rule.k`,
`evidence/18-kprove-without-ideal-rule.log`). This identifies the offending
rule as necessary for closure.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All claims begin in the same explicit state: environment 0; module scope 0
mapping `"iscube"` to `iscubeClosure`; builtins at scope -1; empty heap and
stack; no return, no exception, and exit code 0.

| Claim | Preconditions | Claimed terminating result |
|---|---|---|
| `implementation` | arbitrary K integer `A` | the Boolean `roundedCubeRoot(abs(A))^3 == abs(A)` |
| `positive-cubes` | `N >= 0`; input `N^3` | `true` |
| `negative-cubes` | `N > 0`; input `-N^3` | `true` |
| `positive-noncubes` | `N >= 0`, `0 < D < (N+1)^3-N^3`; input `N^3+D` | `false` |
| `negative-noncubes` | same `N,D`; input `-(N^3+D)` | `false` |

Every precondition is satisfiable. Concrete witnesses in the shared initial
state are:

- `implementation`: `A=8`;
- positive cube: `N=2`;
- negative cube: `N=2`;
- positive noncube: `N=2,D=1`;
- negative noncube: `N=2,D=1`.

Both Python implementations produce the claimed results for those small
witnesses. The exact substitutions and outcomes are in
`evidence/16-claim-witnesses.log`.

The same log exhibits satisfying witnesses that falsify the universal cube
claims: `N=10^15` satisfies both cube preconditions, but both Python
implementations return `False` on `N^3` and `-N^3`, while the claims require
`true`.

### The actual submitted program is not executed by the claims

The claim `<k>` cells start with
`Call(Name("iscube"), ...)`. Their scope is manually populated with the
proof-local nullary function `iscubeClosure` from `verification.k:59-77`.
They do not start with submitted `Module(...)`, do not invoke `#loadAll`, and
do not execute submitted `FuncDef(...)` to install the closure.

The closure literal currently matches the parameter and body rendered in
`solution.mpy`, and the external trusted-translation comparison supports that
manual correspondence. Nevertheless, the K theorem contains no connection
claim from the actual `solution.mpy` module to `iscubeClosure`. Editing
`solution.mpy` without editing `verification.k` would leave every proof claim
unchanged. This is a substituted-program/body-sensitivity failure, not
real-program pinning.

The `implementation` postcondition is also only a structural restatement in
terms of the proof-local opaque `roundedCubeRoot`; it does not constrain that
symbol to Python’s floating computation or to the mathematical cube root.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` lexically inventoried every local `syntax`,
`configuration`, `context`, `rule`, and `claim` declaration in the supplied
semantics helper tree and `verification.k`. The full normalized source record
for every entry is in `evidence/K-INVENTORY.md`; machine-readable records and
per-file summaries are in `evidence/k-inventory.json`. A disposition for every
one of the 941 records is in `evidence/K-RULE-DECISIONS.md`, generated by
`evidence/k_rule_decisions.py` with its run recorded in
`evidence/19-k-rule-decisions.log`. There are 941 records:

- trusted supplied semantics: 227 syntax declarations, 695 rules, one
  configuration, and five contexts;
- candidate `verification.k`: three syntax declarations and ten rules.

Across the complete inventory there are 148 function-bearing declarations,
109 `total` declarations, 26 `symbol` declarations, 23 `no-evaluators`
declarations, 46 priority rules, 35 concrete rules, 26 `owise` rules, and six
simplification rules. There are no local `[functional]` declarations. All six
simplifications are candidate proof extensions.

Per-file declaration/rule coverage is:

| File | Syntax | Rules | Other |
|---|---:|---:|---|
| supplied `semantics.k` | 0 | 0 | requires/import assembly only |
| `assert.k` | 0 | 3 | |
| `bool.k` | 0 | 13 | 1 context |
| `builtins.k` | 38 | 137 | |
| `call.k` | 3 | 21 | |
| `comprehension.k` | 3 | 7 | |
| `concrete.k` | 5 | 16 | |
| `controls.k` | 3 | 34 | |
| `core.k` | 37 | 46 | 1 configuration |
| `dict.k` | 12 | 28 | |
| `float.k` | 34 | 121 | |
| `functions.k` | 4 | 15 | |
| `int.k` | 1 | 16 | |
| `iter.k` | 1 | 0 | |
| `list.k` | 5 | 27 | |
| `methods.k` | 27 | 75 | |
| `operators.k` | 0 | 10 | 2 contexts |
| `range.k` | 2 | 6 | |
| `set.k` | 6 | 12 | |
| `sort.k` | 6 | 19 | |
| `str.k` | 5 | 28 | |
| `subscript.k` | 15 | 40 | 2 contexts |
| `syntax.k` | 16 | 0 | |
| `tuple.k` | 4 | 21 | |
| candidate `verification.k` | 3 | 10 | |

The 24 supplied K source files (the assembly file plus 23 helper files) are
byte-identical to the trusted supplied semantics and therefore constitute the
fixed semantics selected by the rendered mode, not candidate proof extensions.
Every trusted declaration/rule has been accounted for in the inventory. The
modules unrelated to this program are unreachable from its syntax and add no
proof-local conclusion. The used fixed path was reviewed in detail below. The
low-level concrete IEEE-float hooks are a supplied trust boundary; they are
independently exercised by the LLVM witness, but are not part of the Haskell
proof’s symbolic evaluation.

### Mapping every submitted construct to fixed semantics

| Submitted construct | Declaration | Operational treatment |
|---|---|---|
| `Module` | `syntax.k:61` | `core.k:124-127` loads and sequences it; bypassed by the formal claims |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` installs a closure; bypassed by the formal claims |
| `Assign` | `syntax.k:41` with strict RHS | `controls.k:9-18` updates the current scope |
| `Name` | `syntax.k:12` | `core.k:130-154` performs lexical/builtin lookup |
| `Call` | `syntax.k:28` | `call.k:18-32`, `core.k:183-191` evaluate callee then arguments; `call.k:69-85` enters a closure frame |
| `Return` | `syntax.k:50`, strict | `functions.k:77-90` records the value, pops the frame, restores environment/scope |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:14-17` evaluates both operands; `int.k:26` supplies integer equality |
| `BinOp` | `syntax.k:15`, left-to-right `seqstrict` | `operators.k:12` dispatches; `int.k:17` handles final integer cubing; proof-local rules intercept `/` and cube-root `**` |
| `Int` | `syntax.k:9` | `core.k:193-196` yields the K integer |
| `abs` | builtin scope in `core.k:156-181` | call routing reaches `builtins.k:43-44`, producing `absInt` |
| `int` | builtin type in `core.k:179` | `builtins.k:139-140` is identity on the rounded integer |
| `round` | builtin scope in `core.k:174` | fixed `float.k:216-228` handles a real Float; candidate rule intercepts a proof-local token instead |

The fixed semantics’ call frame, scope update, evaluation order, and return
rules are consistent on the used path. The program performs no heap allocation
or output. The candidate bridge rules frame all cells, so they do not directly
mutate state, but they replace result-bearing evaluation and erase possible
float conversion/operation failures. The formal `<exc> NoExc </exc>` therefore
does not cover Python’s `OverflowError` behavior on large integers.

### Candidate extension inventory and decisions

| Location | Extension/class | Static decision |
|---|---|---|
| `verification.k:10` | `oneThirdV`, `cubeRootV(Int)` syntax | Fresh proof-local result tokens. They become result-bearing through later rules. |
| `verification.k:11-12` | opaque `roundedCubeRoot(Int)` `[function,total,symbol,no-evaluators]` | Program-derived opaque integer with no defining equations and no bridge-free connection theorem. `[total]` does not fix its value. Illegitimate as a basis for value-level cube claims. |
| `verification.k:14` | priority-40 `applyBin("/",1,3) => oneThirdV`; operational bridge | Overlaps and preempts fixed `float.k:32`, which would produce `divII(1,3)`. The match has no continuation/cell guard and no universal equivalence theorem. Exact dataflow prose is not a value/control proof. This is an unjustified bridge; the combined false-result witness is below. |
| `verification.k:15` | `applyBin("**",I,oneThirdV) => cubeRootV(I)`; operational bridge | Replaces fixed mixed Int/Float power after the prior interception. Its fresh operand makes it non-overlapping with fixed Float cases, but only because the preceding bridge changed the value. No connection theorem fixes `cubeRootV(I)` to `powF(intToF(I),divII(1,3))`. |
| `verification.k:16-17` | `round(cubeRootV(I)) => roundedCubeRoot(I)`; operational bridge/result abstraction | Replaces actual rounding with the opaque integer. It affects the final cube and return branch. No universal connection theorem, opposite-interpretation rejection, exception proof, or binding/control theorem exists. |
| `verification.k:22-36` | four `absInt` simplifications | Sound under their guards: cubes/noncube magnitudes are nonnegative and the negative forms have positive magnitudes. Their overlaps agree on the same absolute value. |
| `verification.k:41-46` | cube-result simplification to `true` | **Materially unsound.** It encodes the desired cube answer for the opaque program-derived oracle. Concrete false-conclusion witness: `N=10^15` satisfies `N>=0`; actual Python and the fresh fixed concrete K semantics compute a rounded root unequal to `N` and return `False`, while this rule rewrites the corresponding equality to `true`. Evidence: `evidence/16-claim-witnesses.log` and `evidence/12-krun-large-cube-actual.log`. Removing only this rule makes the cube proof stick at precisely the otherwise unproved equality (`evidence/18-kprove-without-ideal-rule.log`). |
| `verification.k:48-55` | noncube-result simplification to `false` | Sound ordinary integer mathematics on its guard: `N^3+D` is strictly between consecutive nonnegative cubes, so no integer value of `roundedCubeRoot(...)` can cube to it. Its guard is disjoint from the perfect-cube case at the interval endpoints. |
| `verification.k:59-77` | total nullary `iscubeClosure` and defining rule | The equation faithfully copies the current submitted body, so it is sound as a definition. It is not a connection theorem and substitutes a proof-local closure for loading the submitted module. |

There are no auxiliary claims in `verification.k`, and no bridge-free module
proves any of the three operational bridges. The only five claims are the
entry claims in `spec.k`, all proved while importing the bridges themselves;
they cannot serve as independent bridge justification.

The critical false conclusion is not merely an untested or unreachable corner:
the formal cube claim explicitly admits `N=10^15`. This satisfies the required
intended-domain witness for the unsound rule. The finite differential evidence
does not replace the missing universal connection theorem; here it actively
refutes the claimed connection.

## 6. Fresh non-vacuity test

No candidate vacuity spec was available. The audit created
`evidence/spec-vacuity-audit.k`, changing the result-constraining obligation at
the satisfying input `1` from `true` to deliberately false `false`.

The mutation:

1. parsed and built successfully under `kprove --dry-run`, exit 0
   (`evidence/14-vacuity-dry-run.log`);
2. then failed under actual proof, exit 1, with `WarnStuckClaimState`
   (`evidence/15-vacuity-proof.log`).

The residual shows the executed `<k>` result `true` and the failed implication
to the target `false`; this is the expected unmet obligation, not a parser,
import, timeout, or unrelated backend error. Both Python implementations return
`True` on witness input 1.

Non-vacuity therefore passes: the result is constrained and a false result is
rejected. This does not make the candidate legitimate, because the successful
positive cube result depends on the materially false rule identified in stage
5.

## 7. Proven versus assumed accounting

### What the successful reachability runs actually establish

Under the candidate’s extended K theory and from the explicitly supplied
manual-closure state:

- the proof-local closure executes through assignment, calls, integer cubing,
  comparison, return, and frame restoration;
- its float-derived subcomputation is summarized as the opaque term
  `roundedCubeRoot(abs(A))`;
- with the added simplifications, ideal mathematical cubes reduce to `true`
  and integers strictly between consecutive cubes reduce to `false`.

This is partial correctness of a manually installed abstract closure under the
candidate’s added axioms. It is not partial correctness of actual
`solution.mpy` under the supplied floating semantics, and it is not the
natural exact-cube theorem.

### Trust and assumption ledger

| Boundary/assumption | Influence | Assessment |
|---|---|---|
| Trusted supplied syntax, configuration, calls, scopes, integers, maps/lists, and builtin routing | control, state, return | Acceptable fixed semantics boundary selected by `SUPPLIED_SEMANTICS`; source tree matches exactly and the used path was freshly built/executed. |
| Supplied concrete Float hooks (`divII`, `intToF`, `powF`, `roundF`, `truncF`) | computed root, exceptions/results | Acceptable low-level supplied boundary for concrete evidence. They reproduce the large-cube `False` witness. They are opaque in Haskell proof mode. |
| `oneThirdV` and `cubeRootV` | evaluation path and eventual return | Concerning/unjustified program-derived operational abstractions; no bridge-free connection or complete-context theorem. |
| `roundedCubeRoot(Int)` | final branch and every postcondition | Illegitimate result-bearing oracle. It is not externally defined, interpretation-parametric, or connected to fixed execution. |
| Ideal-cube simplification | forces cube claims to `true` | Illegitimate and concretely false for the real program at `N=10^15`. |
| Noncube simplification and four abs lemmas | postconditions | Acceptable guarded integer mathematics. |
| `iscubeClosure` literal equals current translated body | program identity | Only an informal/external bridge. Byte translation and inspection support it, but K does not load or pin `solution.mpy`; body mutation would not affect the claims. |
| Canonical-versus-generated differential testing | Python rewrite fidelity | Finite empirical support only: zero mismatches on 796 preserved inputs. It proves no universal equivalence. |
| Generated-versus-integer-oracle testing | intent adequacy | Finite but decisive counterevidence: 210 mismatches, including a concrete satisfying counterexample to the universal formal claim. |
| Fresh false-result mutation | non-vacuity | Valid evidence that the postcondition constrains the result; it does not validate proof extensions. |

### Decision

The dynamic reconstruction succeeds only under a materially unsound
proof-specific rule, and the formal claims use a substituted closure rather
than the submitted program artifact. A satisfying formal input produces the
opposite Boolean in both real Python implementations and in the fresh concrete
supplied K semantics. These are direct `FAIL / NOT_LEGIT` conditions, not a
mere limitation in empirical coverage or an infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
