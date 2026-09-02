# Independent adversarial review: 43-pairs-sum-to-zero

The candidate is **not a legitimate partial-correctness proof of the real
generated Python program**. Fresh reconstruction does produce `#Top`, the claim
is result-constraining, and the claim's constructor term is identical to
`solution.mpy`. The fatal issue is the generated call rule: it silently turns
Python recursion into unbounded tail-call re-entry. On the intended input
`[1] * 997`, the actual submitted Python raises `RecursionError`, while the
freshly rebuilt K semantics returns `false` and the universal claim covers that
K result. This is a concrete false behavioral conclusion on the unrestricted
source-contract domain, not a timeout or infrastructure uncertainty.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `43-pairs-sum-to-zero`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- no mounted reference semantics.

The mode boundary is consistent: `/reference/reference-semantics` is absent.
No hidden or inferred reference semantics was used.

I independently checked all launcher-required records for this layout:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
present and was also checked; historical `runtime-metrics.json` is absent and
is not required for this legacy layout. The trace contains one JSONL file with
202 valid structured records. Its tool calls and final generation claim were
treated only as untrusted history.

The campaign lock is byte-hashed as
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object exactly equals the embedded
`audit_campaign` block. Every directly recorded file hash matches. Independent
pipeline tree hashes also match the retained generation records:

- candidate tree:
  `fec1efcb6250c5867446b668b19124e3562b96b2f0b7da4e6a5abf04f0c615bc`;
- structured trace tree:
  `e7546f2b5e251105aa7fc31d9bab372e965a3827616c6cdb829d2f0383e98ae5`.

All entries below `/candidate`, `/generation-evidence`, and `/reference` are
regular files or real directories; there are no symlinks or unsupported nodes.
The candidate's `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. All generation-prompt deliverables are present:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. `PROOF.md` was not a generation-prompt deliverable, so its absence
is not charged as a candidate defect.

Evidence:
[integrity script](evidence/01_integrity.py),
[integrity log](evidence/01-integrity.log),
[trace parser](evidence/01_trace_summary.py), and
[trace summary](evidence/01-trace-summary.log).

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`: for an
unrestricted finite list of integers, return `True` exactly when two elements
at distinct indices sum to zero, and return `False` otherwise. The prompt states
no maximum length.

The candidate implements a mathematically equivalent recursive algorithm:

1. return `False` on the empty list;
2. return `True` when the inverse of the head occurs in the tail; otherwise
3. recurse on the tail.

### Trusted regeneration

The exact command is recorded in
[02-regenerate.log](evidence/02-regenerate.log). Running the trusted translator
on the scratch copy exited 0, and `cmp` exited 0. Both regenerated and submitted
`solution.mpy` have SHA-256
`7620bbe22dae64260e7de1666540d5f6f1e198346d814eb3dc6664832b6e63c6`.

### Independent differential test

[02_differential.py](evidence/02_differential.py) imports the trusted canonical
entry point and submitted entry point independently. It exercises:

- all five documented examples;
- empty, singleton, duplicate-zero, positive/negative, recursive, duplicate,
  and large-integer branch boundaries;
- every one of the 19,608 lists of length 0 through 5 over `[-3, 3]`;
- 2,000 deterministic generated lists of length 0 through 80; and
- four recursion-boundary lists of length 997 or 1,200.

The deterministic 21,629-case corpus has SHA-256
`8605a45149cb8d357f136298c46c033cf9d34108b7ba542a700e1da276e7dffb`.
There were three mismatches, all preserved in
[02-differential.log](evidence/02-differential.log). With Python 3.10.12's
recorded recursion limit of 1,000:

- the canonical returns `False` on a 997-element positive list;
- the candidate raises `RecursionError`;
- the same divergence occurs on two 1,200-element no-pair lists; and
- a 997-element list with `[1, -1]` at the front returns `True` immediately,
  confirming that the divergence is caused by reachable recursive control
  rather than list size alone.

This is a material source-contract divergence on a documented `list[int]`
domain. The differential script intentionally exits 1 when it finds it.

## 3. Clean proof reconstruction

All source artifacts were copied to
`/tmp/audit-work/43-pairs-sum-to-zero`; no candidate kompiled definition or
cache was present or reused. The observed tools are K v7.1.293.

Fresh commands and results:

| Purpose | Result | Evidence |
|---|---:|---|
| LLVM concrete definition from `semantic.k` | exit 0 | [03-kompile-concrete.log](evidence/03-kompile-concrete.log) |
| Haskell definition from `semantic.k` | exit 0 | [03-kompile-fresh-semantic-haskell.log](evidence/03-kompile-fresh-semantic-haskell.log) |
| Haskell proof definition from `verification.k` | exit 0 | [03-kompile-proof-haskell.log](evidence/03-kompile-proof-haskell.log) |
| Candidate's positive command against fresh semantic definition | `#Top`, exit 0 | [03-positive-kprove-candidate-command.log](evidence/03-positive-kprove-candidate-command.log) |
| Same sole claim against the independently built proof definition | `#Top`, exit 0 | [03-positive-kprove-proof-definition.log](evidence/03-positive-kprove-proof-definition.log) |

The complete build procedure is
[03_build.sh](evidence/03_build.sh). There is one positive claim in `spec.k`,
so every positive target claim was run.

The LLVM compiler warned that `hasZeroPair`, `first(.ISeq)`, and
`rest(.ISeq)` are declared total but have non-exhaustive executable equations
in `semantic.k`. `hasZeroPair` receives its equations only when
`verification.k` is imported; the empty `first` and `rest` cases remain
unmodeled.

Fresh concrete execution covered empty, singleton, duplicate-zero, recursive
true/false, arbitrary-precision integers, and recursion-boundary inputs. Every
`krun` command itself exited 0 and agreed with the mathematical/canonical
answer. The critical comparison is:

| Input | Canonical Python | Candidate Python | Fresh K |
|---|---|---|---|
| `[1] * 997` | returns `False` | raises `RecursionError` | returns `pyBool(false)` |
| `[1, -1] + [1] * 995` | returns `True` | returns `True` | returns `pyBool(true)` |

The exact deterministic construction, input-term hashes, K exits, and result
hashes are in
[03_concrete_compare.py](evidence/03_concrete_compare.py) and
[03-concrete-compare.log](evidence/03-concrete-compare.log). Thus reconstruction
passes as a theorem under the candidate theory, but generated-semantics
fidelity fails.

## 4. Adequacy and real-program pinning

### Formal entry claim in plain language

The claim has no `requires` clause. Its precondition is:

- `L` is any `ISeq`;
- `<env>` is empty;
- `<k>` begins with `run` of the literal submitted function binding and body;
  and
- `<program>` contains the same literal binding and body.

Its postcondition is exact, not one-way or free: if execution terminates under
the candidate K theory, `<k>` is `pyBool(hasZeroPair(L))`, while the framed
program cell remains that function and the environment is empty.
`hasZeroPair` recursively means “the head's additive inverse occurs later, or
the tail has such a pair,” with `false` at the empty list.

The precondition is satisfiable. Three mechanical ground instances all prove
with `#Top`:

- `.ISeq` gives `false`;
- `0 :: 0 :: .ISeq` gives `true`;
- `1 :: 2 :: .ISeq` gives `false`.

Their source and logs are
[04-ground-empty.k](evidence/04-ground-empty.k),
[04-ground-two-zeroes.k](evidence/04-ground-two-zeroes.k),
[04-ground-no-pair.k](evidence/04-ground-no-pair.k), and the corresponding
`04-ground-*.log` files. These results agree with both Python implementations
on those inputs.

### Mechanical program identity

[04_pinning.py](evidence/04_pinning.py) extracts both literal `Module(...)`
terms from the claim, removes only the internal `.Stmts` empty-list spelling
that the standalone program scanner represents by omission, and parses all
three programs with `kast` to KORE. The submitted `solution.mpy`, the `<k>`
program, and the `<program>`-cell program all produce the same 4,225-byte KORE
term with SHA-256
`e10b6d40559e54579b177eefb86d4a6e7f607bc84668be863a530202e0c97379`.
See [04-pinning.log](evidence/04-pinning.log).

There are no helper claims. The universal entry claim itself is used
circularly after the recursive call reaches the same `run` configuration for
`rest(L)`.

### Body sensitivity

The fresh mutation changes `Return(Bool(false))` to
`Return(Bool(true))` in both the actually executed `<k>` program and the
matching `<program>` cell. It builds with `--dry-run` exit 0, then fails proof
with exit 1 on the reachable empty-list branch, leaving
`pyBool(true)` where `hasZeroPair(L)` requires false. See
[04-body-mutation.k](evidence/04-body-mutation.k),
[dry-run log](evidence/04-body-mutation-dry-run.log), and
[proof log](evidence/04-body-mutation-proof.log).

### Adequacy decision

Constructor identity is not enough: the meaning assigned to that constructor
term must match the real program. `semantic.k:91-95` replaces Python's
recursive call/return with direct `run(...)` re-entry, clears the environment,
and keeps no call stack or recursion exception. The `[1] * 997` witness lies in
the entry claim's unrestricted `ISeq` domain and in the source contract's
unrestricted `list[int]` domain. K produces a normal Boolean result where the
actual submitted Python takes an exceptional control path. The claim therefore
pins the submitted syntax but not the real generated program's material
control behavior.

This is not merely failure to prove termination. The K model positively
executes to a normal `false` result for an input on which the real program
terminates abnormally with `RecursionError`.

## 5. Rule-by-rule static soundness review

The complete numbered sources and declaration index are preserved in
[05-source-inventory.log](evidence/05-source-inventory.log). There are no helper
K files beyond `semantic.k`, `verification.k`, and `spec.k`.

### Syntax, configuration, functions, and attributes

Local syntax inventory:

- `Program`: `Module(Stmts)`;
- `Stmts`: juxtaposed `Stmt` list;
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`;
- `Params` and comma-separated `StringList`;
- `Expr`: `Bool`, `Int`, `Name`, `UnaryOp`, `Compare`, `Subscript`, `Call`;
- `Exprs`, `CmpOps`, `CmpOp`;
- `Index`: expression or `Slice`;
- `Bound`: expression or `NoBound`;
- semantic list `ISeq`: `.ISeq` or `Int :: ISeq`;
- values `pyInt`, `pyBool`, `pyList`, `pyNone`; and
- K items `run`, `functionEnd`, `ifStmt`.

The configuration has exactly the state used here: `<k>`, immutable
`<program>`, and `<env>`. There is no call-stack or exception cell.

Function symbols are `eval`, `negVal`, `atZero`, `tailVal`, `containsVal`,
`truth`, `asList`, `isEmpty`, `member`, `hasZeroPair`, `first`, and `rest`.
`isEmpty`, `member`, `hasZeroPair`, `first`, and `rest` are declared
`[total]`. Only the two `ISeq` constructors carry local `[symbol(...)]`
attributes. There are no local `[functional]`, priority, `owise`, macro,
opaque-hook, or priority rules. The only simplification rules are the three in
`verification.k`.

Every submitted constructor is covered: module/function/parameter entry,
statement sequencing, both `If` branches, both returns, recursive `Call`,
names, Booleans and integers, unary `not` and minus, index zero, tail slice,
membership comparison, list truthiness, head/tail, and integer membership.

### All 32 semantic rules

| Location | Rule and decision |
|---|---|
| `semantic.k:74-76` | One-argument function entry binds the exact parameter in an empty environment. Faithful for the submitted module. |
| `:79` | Splits the first statement from a statement list. Correct left-to-right control. |
| `:80` | Empty statement list becomes empty K. Correct. |
| `:82-83` | Name assignment evaluates the pure RHS and updates the map. Unused by this program; sound for the represented case. |
| `:85-86` | Evaluates the `If` expression and creates `ifStmt`. The submitted expressions are pure, so the atomic function evaluation does not alter observable order. |
| `:87` | True guard selects the then-list. Correct. |
| `:88` | False guard selects the else-list. Complementary and disjoint with `:87`. |
| `:91-95` | Tail-return call re-enters `run` with no call stack. Binding is pinned by the repeated `F`, and discarding the local `_REST` is correct for a return, but omission of recursive stack/exception behavior is materially false. Witness: `[1] * 997` gives K `false` and Python `RecursionError`. **Fatal.** |
| `:97-98` | Returning a Boolean literal discards the local suffix and clears the environment. Correct on both submitted return sites. |
| `:99` | Falling off a function returns `pyNone`. Correct but unreachable for this function. |
| `:101` | Boolean literal evaluation. Correct. |
| `:102` | Integer literal evaluation. Correct; K's unbounded integer arithmetic matches Python integers absent resource exhaustion. |
| `:103` | Map lookup by the exact name. Correct for unique K maps and the bound parameter. |
| `:104` | Unary `not` applies modeled truthiness. Correct for used list values. |
| `:105` | Unary minus delegates to integer negation. Correct. |
| `:106` | Index-zero evaluation delegates to `atZero`. Correct only when the list is nonempty; Python's empty-list error is not represented. The actual body guards this path. |
| `:107-108` | `[1:]` delegates to `tailVal`. Correct on the reachable nonempty path; the empty-slice behavior is not executable because `rest(.ISeq)` has no equation. |
| `:109-110` | Single `in` comparison delegates to modeled containment. Correct for used integer/list values. |
| `:112` | Integer negation `0 -Int I`. Correct. |
| `:113` | `atZero(pyList(L))` returns `first(L)` without a nonempty guard or `IndexError`. Globally false on `L=.ISeq`, though unreachable in the submitted body because the preceding empty test returns. |
| `:114` | `tailVal` returns `rest(L)`; faithful on nonempty lists, incomplete on empty. |
| `:115` | Integer/list containment returns `member`. Correct. |
| `:117` | Boolean truthiness. Correct. |
| `:118` | Integer truthiness is nonzero. Correct. |
| `:119` | List truthiness is nonempty. Correct. |
| `:120` | Extracts the modeled list from `pyList`. Correct. |
| `:122` | Empty-list test returns true. Correct. |
| `:123` | Cons-list test returns false. Correct and disjoint with `:122`. |
| `:124` | `first` of a cons is its head. Correct. |
| `:125` | `rest` of a cons is its tail. Correct. |
| `:126` | Membership in empty is false. Correct. |
| `:127` | Membership in cons is head equality or recursive membership. Correct, exhaustive with `:126`, and structurally descending. |

The false empty-index conclusion is machine-demonstrable, rather than inferred:
[05-totality-witness.k](evidence/05-totality-witness.k) asks whether evaluating
`l[0]` with `l=.ISeq` reaches some `pyInt`. It builds and proves `#Top`, while
real Python raises `IndexError`; see
[05-totality-witness-proof.log](evidence/05-totality-witness-proof.log).
A diagnostic removal of `[total]` from `first` alone did not repair this
existential conclusion, confirming that the missing exception/guard in the
operational subscript path is the underlying model gap, not merely the
attribute. This rule is off the submitted program's reachable empty branch, so
the verdict does not rely on it; the reachable recursive-call witness already
establishes the fatal failure.

### All three verification rules

| Location | Rule and decision |
|---|---|
| `verification.k:6` | `notBool notBool B => B` is ordinary Boolean involution and is valid for all `Bool`. |
| `:12-13` | `hasZeroPair(L) => false` when `isEmpty(L)` is a truthful base equation. |
| `:14-16` | On nonempty `L`, head-inverse membership or `hasZeroPair(rest(L))` is exactly the distinct-index decomposition. The recursion structurally descends. |

The two `hasZeroPair` guards are disjoint and exhaustive over constructor
`ISeq` values. `member` is likewise exhaustive. `hasZeroPair` is a definitional
summary used only in the postcondition; it does not rewrite or bypass program
execution. It is therefore not a smuggled operational oracle.

`first` and `rest` are over-broadly declared total even though their empty cases
have no equations, as the LLVM compiler warns. Reachable uses in the submitted
body and recursive summary are guarded by nonemptiness, but the global
declarations and missing exception semantics prevent full language-level
validation.

There are no overlapping priority rules, hidden state cells, allocation
effects, I/O, or mutations in the submitted program. Omitting physical slice
allocation is inert here because lists are never mutated. Omitting recursive
stack state is not inert because it changes the witnessed exception and normal
result.

## 6. Fresh non-vacuity test

The fresh mutation keeps the exact submitted program and changes only the
result-constraining postcondition from:

`pyBool(hasZeroPair(L))`

to:

`pyBool(notBool hasZeroPair(L))`.

`L=.ISeq` satisfies the original precondition and is a concrete false witness:
the program returns false and `hasZeroPair(.ISeq)=false`, while the mutation
demands true.

The preserved mutation is
[06-spec-vacuity.k](evidence/06-spec-vacuity.k). It builds successfully with
`--dry-run` exit 0
([06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log)). The real proof run
exits 1 with `WarnStuckClaimState` on the reachable `pyBool(false)` empty branch
([06-vacuity-proof.log](evidence/06-vacuity-proof.log)). This is the expected
unmet obligation, not a parser error, timeout, or unrelated crash.

The formal K claim is therefore non-vacuous and result-constraining under the
candidate theory.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under `MPY-VERIFICATION`, for every modeled `ISeq L`, every terminating modeled
execution of the exact submitted constructor term from the empty environment
reaches `pyBool(hasZeroPair(L))`. The recursive predicate is defined by the
three reviewed simplification rules, and the recursive program body is
genuinely executed until circularity matches its next `run(..., rest(L))`
configuration.

It does **not** establish the same statement for real Python execution because
the connection between modeled `run` and Python call/return behavior is false
on a reachable intended-domain input.

### Trust and assumption ledger

| Boundary | Dependents and assessment |
|---|---|
| Trusted `py2mpy.py` transliteration | Acceptable provenance boundary. Byte-identical regeneration and constructor comparison pin the syntax. It supplies no semantics. |
| K v7.1.293 parser, LLVM/Haskell backends, reachability logic, and circularity | Ordinary toolchain trust. Fresh independent builds and mutation behavior are reproducible. |
| Imported K `INT`, `BOOL`, and `MAP` | Acceptable low-level primitives for arbitrary-precision arithmetic, Booleans, and immutable bindings used here. |
| `ISeq` as finite Python `list[int]` | Informal representation bridge. Sound for element/order observations used here; allocation identity is unobservable because there is no mutation. |
| Manually generated truthiness, negation, membership, and slicing rules | Reviewed rule-by-rule and empirically supported on the recorded finite corpus. Finite tests do not universally prove the bridge. |
| Tail-call `run` rule with no Python stack/exception | Illegitimate result/control-bearing abstraction. It changes a reachable `RecursionError` into a normal Boolean result. All universal target conclusions depend on it for recursive no-pair inputs. |
| Empty indexing and `[total] first/rest` boundary | Globally unsound/incomplete relative to Python errors; concrete false semantic witness preserved. Guarded off the submitted empty path, so secondary to the reachable call-stack failure. |
| `hasZeroPair` equations | Truthful definitional summary, not an operational bridge. The ordinary induction connecting it to “two distinct indices sum to zero” is transparent but not a separate machine-checked theorem. |
| Differential and concrete tests | Finite evidence only. They expose the decisive mismatch; they do not substitute for the K proof. |
| Termination and absence of resource errors | Not proved by partial-correctness reachability. More importantly here, the semantics masks a real terminating exceptional path rather than merely declining to prove termination. |

Gate accounting:

- Clean verification under the supplied theory: **PASS** (`#Top`, exit 0).
- Result constraint/non-vacuity and body sensitivity: **PASS**.
- Real-program semantic soundness: **FAIL** because of the reachable
  call-stack/`RecursionError` witness.
- Source-contract adequacy: **FAIL** because the unrestricted prompt domain
  includes the witnessed long integer list.
- Reproducibility/evidence auditability: **PASS**, but it cannot repair the
  failed soundness and adequacy gates.

The successful K run is a theorem about an idealized, tail-call-optimized
language, not a legitimate proof of the real generated Python program. The
material source-domain and semantics mismatch requires `FAIL / NOT_LEGIT`
under the benchmark decision boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
