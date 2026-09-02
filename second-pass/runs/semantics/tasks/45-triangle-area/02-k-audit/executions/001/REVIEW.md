# Independent adversarial audit — 45-triangle-area

The candidate reconstructs to `#Top` and its claim is non-vacuous, but it is
not a legitimate proof of the real generated program over its stated domain.
There is a concrete positive-integer witness admitted by the entry claim on
which:

1. `solution.py` materially diverges from the trusted canonical program; and
2. the supplied K `divII` model materially diverges from `solution.py`.

The witness is

```text
A = (2**53 - 1) * 2**972
H = 1
```

The generated program (`... / 2`, integer/integer true division) returns the
largest finite binary64 value. The canonical program (`... / 2.0`) raises
`OverflowError`, while the supplied K concrete division fails an assertion
requiring the generated program's finite result. This is not a timeout or
infrastructure inference; it is reproduced by completed Python and LLVM runs.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- Mode is `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` exists as a real directory.
- `diff -qr --no-dereference` between the trusted and candidate semantics
  trees exited 0. Both trees contain the same 24 regular K files; there are no
  missing, additional, changed, mistyped, or symlinked entries.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`sha256 2ffd4f475e7fbe32b636a57d40751aedd393c3a1096cd6a1edaef3981d7c8564`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`sha256 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

The following requested provenance artifacts are missing from `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace is present. `PROOF.md` and candidate vacuity
evidence are also absent, though neither is needed to reproduce the submitted
claim. The candidate contains an untrusted `prove.sh`, smoke files, and Python
bytecode. I did not rely on its script or bytecode. The exact copied
`__pycache__` was deleted before rerunning imports, and no candidate-provided K
compiled definition existed or was reused.

Evidence:

- [stage1-integrity.log](evidence/stage1-integrity.log)
- [artifact-manifest.log](evidence/artifact-manifest.log)
- [cache-discard.log](evidence/cache-discard.log)

Stage 1 result: semantics provenance integrity passes; generation provenance
is materially incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the area of a triangle from a side length and
height, with documented example `triangle_area(5, 3) == 7.5`. The trusted
canonical implementation returns:

```python
a * h / 2.0
```

The generated implementation returns:

```python
a * h / 2
```

For ordinary built-in integers and floats these usually agree, but they are not
equivalent for all Python integers. The candidate's own formal comment says
the claim covers every pair of Python integers, and its K variables have no
size bound.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
dfeb6ac63836b0ff5014334a279dd1e5f625a17de4a5aba7e45e034ccab07b8a
```

Thus the submitted constructor program faithfully represents `solution.py`.

The independent differential harness imports the trusted canonical entry point
and generated entry point directly. It covers the documented example, zero
and sign boundaries, odd products, binary64 boundaries, invalid empty/short/
extra arity, an empty invalid value, NaN/infinity, 400 seeded integer pairs,
and 80 seeded float pairs. There are no conditional branches in either
implementation. Across 500 cases it found one mismatch:

```text
A = 359538626972463141629054847463408713596141135051689993197834953606314521560057077521179117265533756343080917907028764928468642653778928365536935093407075033972099821153102564152490980180778657888151737016910267884609166473806445896331617118664246696549595652408289446337476354361838599762500808052368249716736
H = 1
canonical: OverflowError
generated: 0x1.fffffffffffffp+1023
```

This is a material result divergence on the candidate's stated integer domain,
not merely a type-presentation difference. The generated program performs
integer/integer true division, for which CPython scales the unbounded integers
before the binary64 result is formed. The canonical program's float divisor
forces conversion of the oversized numerator and raises.

Evidence:

- [program-fidelity.log](evidence/program-fidelity.log)
- [translation-regeneration.log](evidence/translation-regeneration.log)
- [differential_triangle_area.py](evidence/differential_triangle_area.py)
- [differential.log](evidence/differential.log)

Stage 2 result: **fail**. The generated program is not equivalent to the
trusted canonical program over the formal all-integer domain.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/review-45-triangle-area-20260724`. Builds were made from that
source snapshot. Candidate caches and compiled definitions were not used.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
EXIT_STATUS: 0
```

The candidate smoke source was regenerated with the trusted translator and was
byte-identical. Its four assertions executed to `NoExc`, exit code 0. A
reviewer-authored five-case concrete program, including zero, negative, odd,
and large exactly representable values, also executed to `NoExc`, exit code 0.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module TRIANGLE-AREA-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
EXIT_STATUS: 0
```

`spec.k` contains one positive claim. Its independent proof run was:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module TRIANGLE-AREA-SPEC
#Top
EXIT_STATUS: 0
```

An optional ground-specialized K claim encountered the known Haskell backend
absence of the `FLOAT.int2float` hook when the `[concrete]` `divII` equation
became ground. I do not use that backend error as a candidate verdict. The
required symbolic positive claim completed successfully, and LLVM supplied
the independent ground execution evidence.

Evidence:

- [kompile-runtime.log](evidence/kompile-runtime.log)
- [smoke-translation.log](evidence/smoke-translation.log)
- [krun-smoke.log](evidence/krun-smoke.log)
- [concrete_cases.py](evidence/concrete_cases.py)
- [krun-reviewer-cases.log](evidence/krun-reviewer-cases.log)
- [kompile-verification.log](evidence/kompile-verification.log)
- [kprove-positive.log](evidence/kprove-positive.log)
- [kprove-ground-witness.log](evidence/kprove-ground-witness.log)

Stage 3 result: **pass** for clean reconstruction of every required positive
claim.

## 4. Adequacy and real-program pinning

### Entry precondition

In plain language, the sole entry claim admits arbitrary K integers `A` and
`H`, with no nonnegativity or magnitude bound. It starts in module environment
0 with an empty user scope whose parent is the builtins scope, next scope
location 1, empty heap and stack, `noRet`, `NoExc`, and exit code 0.

This precondition is satisfiable. For `A=5`, `H=3`, substitution gives the
claimed result `divII(15,2)`. Independent arithmetic, trusted canonical Python,
and generated Python all give `7.5`; the fresh LLVM concrete assertions also
pass.

### Entry postcondition

The claim requires execution of module loading followed by a call to
`triangle_area`. It requires the returned `<k>` value to be exactly
`divII(A *Int H, 2)`, retains the installed function closure in module scope,
restores scope location 1, leaves heap and heap location unchanged, empties the
stack, restores `noRet`, and requires `NoExc` and exit code 0.

There are no helper or loop claims. `triangleAreaProgram` is the exact
constructor tree from submitted `solution.mpy`; trusted regeneration and
manual constructor comparison both confirm the identity. The encoded function
body therefore executes rather than being replaced by a result summary.

The return is result-constraining: it is not a free variable, tautology, or
one-way implication. The fresh false-result mutation in Stage 6 confirms this.

### Concrete adequacy failures

The finite-result witness from Stage 2 also falsifies the semantics bridge for
the real generated program:

- Generated Python executes normally and returns
  `1.7976931348623157e308`.
- The same reviewer-authored assertion under the fresh supplied LLVM semantics
  ends in `AssertionError`, exit code 1.

This occurs because the supplied concrete equation

```k
divII(I1, I2) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11)
```

converts the oversized numerator before division, unlike CPython's
integer/integer true-division path.

A second satisfying witness, `A=10**400`, `H=1`, shows exception mismatch:
generated and canonical Python both raise `OverflowError`, while the supplied
K execution completes with `NoExc`, exit code 0.

Evidence:

- [ground_witness_compare.py](evidence/ground_witness_compare.py)
- [ground-witness-compare.log](evidence/ground-witness-compare.log)
- [concrete_division_scaling_boundary.py](evidence/concrete_division_scaling_boundary.py)
- [python-division-scaling-boundary.log](evidence/python-division-scaling-boundary.log)
- [krun-division-scaling-boundary.log](evidence/krun-division-scaling-boundary.log)
- [concrete_huge_boundary.py](evidence/concrete_huge_boundary.py)
- [python-huge-boundary.log](evidence/python-huge-boundary.log)
- [krun-huge-boundary.log](evidence/krun-huge-boundary.log)

Stage 4 result: **fail**. Exact syntax is pinned, but real generated-program
behavior is not pinned for inputs admitted by the entry precondition.

## 5. Rule-by-rule static soundness review

The reviewer-authored inventory exhaustively enumerates every K file in the
supplied tree plus `verification.k` and `spec.k`:

- 26 files total: 24 supplied-semantics files, `verification.k`, and `spec.k`
- 1,102 top-level inventory entries
- 228 syntax declarations
- 696 rules
- 147 declarations marked `function`
- 108 declarations marked `total`
- 45 priority-bearing rules
- 26 `owise` rules
- 36 concrete-only rules
- 22 `no-evaluators` opaque declarations
- five evaluation contexts
- one configuration and one reachability claim
- no `functional` declarations and no `simplification` rules

Every entry, exact source range, attributes, and compact source text is in
[k-rule-inventory.md](evidence/k-rule-inventory.md). The rule-by-rule
reachable-path classification is in
[static-path-analysis.md](evidence/static-path-analysis.md).

### Reachable constructs and control flow

The submitted program uses only `Module`, `FuncDef`, `Params`, `Return`,
`BinOp`, `Name`, and `Int`; the entry adds `Call`. The static path maps each to
its syntax and rules:

- `#loadAll` and statement sequencing execute the module.
- `FuncDef` installs the exact closure in scope 0.
- the generic call route resolves the actual binding, evaluates arguments
  left-to-right, and dispatches to that closure;
- a fresh call frame binds `a` and `h`;
- `seqstrict` evaluates multiplication before division;
- integer multiplication reduces to `A *Int H`;
- integer division reduces to `divII(A *Int H,2)`;
- `Return` and `#pop` restore the caller continuation, environment, scopes,
  stack, and return state.

The higher-priority closure-cell lookup/binding competitors have false guards
because this is a plain frame without `$cells`. No builtin, method, math,
reference-dereference, collection, or other priority rule matches the
reachable heads. Configuration, evaluation order, binding, call/return
control, and state footprints align on the reachable ordinary cases.

All out-of-path rules were inventoried. Their constructor heads, sorts, call
targets, guards, or continuation shapes do not unify with a state reachable
from this program. I found no false-rule witness connecting any such rule to
this theorem and therefore do not label unreachable baseline rules unsound.

### Candidate-local extension

`verification.k` adds exactly:

```k
syntax Module ::= "triangleAreaProgram" [function, total]
rule triangleAreaProgram => Module(FuncDef(...submitted exact body...))
```

This is a terminating, covering, non-overlapping definitional constant. It
does not replace program execution and does not encode the task answer. The
candidate adds no operational bridge, priority rule, simplification rule,
opaque symbol, or auxiliary claim.

### Result-bearing opaque primitive and false witness

Of 22 supplied opaque primitives, only `divII(Int,Int)` is reachable. It
controls the entire returned value and postcondition. Structurally, the proof
is interpretation-parametric: it proves that execution returns the same
`divII` term named by the postcondition. It does not independently prove what
that term means numerically.

Treating primitive integer true division as a low-level external boundary
would be acceptable only with a correct named contract. Here the supplied
concrete equation and the candidate comment claim Python integer true
division, but the finite-result witness above disproves that contract over the
complete formal domain. The same witness makes the false conclusion observable:
the real generated program returns the largest finite float, while the K model
does not. The `10**400` witness separately shows a false normal-completion
conclusion.

This is a materially unsound semantics-to-real-program bridge, not merely an
evidence gap or an unreachable bad case.

Stage 5 result: **fail** on the reachable result-bearing `divII` bridge. The
candidate-local rule itself is sound.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was used. I created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), changing the demanded
result from:

```k
divII(A *Int H, 2)
```

to:

```k
divII((A *Int H) +Int 1, 2)
```

For the satisfying witness `A=5`, `H=3`, real execution produces
`divII(15,2)` while the mutation demands `divII(16,2)`.

The mutated spec dry-built successfully (`EXIT_STATUS: 0`). The proof then
exited 1 with `WarnStuckClaimState`; its residual explicitly reports the unmet
equality:

```text
divII(A *Int H +Int 1, 2) #Equals divII(A *Int H, 2)
```

This is the expected reachable unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash.

Evidence:

- [vacuity-build.log](evidence/vacuity-build.log)
- [vacuity-proof.log](evidence/vacuity-proof.log)

Stage 6 result: **pass**. The claim is discriminating and result-constraining.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied K theory, from the exact formal configuration and for
arbitrary K integers `A,H`, the exact constructor encoding of `solution.mpy`
loads and its real function body executes. It computes K integer multiplication
and returns the opaque term `divII(A *Int H,2)`, with the module closure
installed and all temporary call state restored as specified. This structural
reachability theorem is machine-checked and non-vacuous.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K frontend, Haskell prover, LLVM backend, hooked integer/map/list primitives | Parsing, rewriting, symbolic closure, concrete evidence | Ordinary toolchain trust. Fresh builds and bounded logs exist. |
| Trusted `py2mpy.py` | Python-source to constructor-tree bridge | Byte-identical candidate copy; independent regeneration exactly matches `solution.mpy`. Acceptable. |
| `triangleAreaProgram` equation | Selects the program executed by the claim | Exact constructor identity; no result summary. Acceptable. |
| Supplied operational call/scope/operator rules | Binding, evaluation order, state, call/return | Fixed trusted-source tree and statically faithful on the reachable structural path. |
| Opaque `divII` | Entire returned value and numerical meaning | The proof only establishes the term structurally. Its claimed Python meaning is false on two satisfying integer witnesses. Illegitimate as a universal real-program bridge. |
| Canonical-versus-generated equivalence | Connection to the requested implementation | Finite differential evidence finds a concrete mismatch on the claimed integer domain. Failed. |
| Formal input type | Theorem scope | Only K/Python integers are formalized. Float inputs accepted by both Python implementations are tested but not proved. This is an additional scope limitation. |
| Differential and smoke tests | Empirical fidelity evidence | Finite evidence only, never substituted for the K proof. One differential mismatch is preserved rather than hidden. |
| Candidate provenance records | Reproducibility of generation | Four requested records are missing. The independent reconstruction remains reproducible, but candidate-side auditability is incomplete. |

The positive `#Top` therefore cannot be promoted to a proof of the requested
real program. The failure does not rest on the optional Haskell ground-hook
error, a timeout, malformed mount, or other infrastructure uncertainty. It
rests on completed, reproducible counterexamples within the entry claim's
formal integer domain.

Overall decision: the proof is structurally genuine under its K theory and
non-vacuous, but it proves a generated implementation that is not
canonical-equivalent on the claimed domain and relies on a result-bearing
semantics bridge that is concretely false for that same real implementation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
