# bf-probe — cracking HumanEval/148 `bf` (symbolic string membership, 8-way case-split)

## The blocker

`bf(planet1, planet2)` maps each of two symbolic strings to an orbit index via an 8-way
if/elif chain (`idxOf`, else `-1`), then slices the fixed planet tuple between them. The proof
case-splits on the input string equalities (`planet ==K "Mercury"` …). The **valid** branches
closed; the **invalid** branch (a planet equal to none of the eight) did not — `idxOf(P) ⇒ -1`
would not discharge. Documented as a `krun`-green blocker.

## The probe (2 literals "A"/"B"; mechanism identical to the 8 planets)

Two `idxOf` failure modes were conflated. The probe separated them.

### Round 1 — `idxOf` in isolation (`verif.k`, `spec-*.k`): the `=/=K` bug

| formulation | invalid-case precond | result |
|---|---|---|
| `#if` cascade over `==K` | `=/=K` conj | **#Top** |
| `#if` cascade over `==K` | `notBool(==K)` conj | **#Top** |
| **original: positive `requires` + `=/=K` conj fallback** | `=/=K` conj | **STUCK** |
| positive `requires` + **`notBool(==K)`** conj fallback | `notBool(==K)` conj | **#Top** |
| positive sanity (`==K`) | — | **#Top** |

**Finding 1.** The solver does **not** normalize `P =/=K X` to `notBool(P ==K X)`. The program's
branch puts `P ==K "Mercury" = false` in the path condition; a `=/=K` fallback asks the solver to
discharge a *different* atom it can't connect. Stating the fallback with `notBool(P ==K name)`
fixes it. This was the original blocker's proximate cause.

### Round 2 — faithful context (`verif2.k`/`verif3.k`): RHS + `#branch`, and scale

`dispatch(P)` branches on the `==K` atoms via `#branch` (the real path-condition shape) and pins
`idxOf(P)` in the **postcondition** (`ensures`), not on the `<k>` cell. Both `#if` and
`notBool`-rule forms → **#Top**; the 8-planet version → **#Top**. So neither the RHS/implication
context nor scale is the blocker.

### Round 3 — `idxOf` buried in a guard (`verif4.k`): the real one

`bfRes` uses `idxOf` inside a guard `#if (idxOf(P1) <Int 0 orBool …) …`. Reproducing that:

| `idxOf` form buried in `#if (idxOf(P) <Int 0) …` | result |
|---|---|
| `#if` cascade (`idx`) | **STUCK** |
| binding an intermediate `?I ==Int idx(P)` in `ensures`, then `combWith(?I)` | **STUCK** |
| **rule-based (`idxCNB`: positive `requires` + `notBool` fallback)** | **#Top** |

**Finding 2 (the crux).** A `#if`-cascade `idxOf` *always* rewrites to a `#if` term; when that term
is buried inside another `#if`'s **condition** (`bfRes`'s guard), kprove does not push the path
condition deep enough to collapse it, so it stays symbolic and the guard never decides. A
**rule-based** `idxOf` instead fires one rule per path-conditioned branch and reduces to a **bare
`Int`** (0..7 / −1); a bare Int survives being buried in a guard, so the guard decides and `bfRes`
reduces. Introducing an intermediate existential (`?I ==Int idx(P)`) does **not** help — kprove
won't propagate `?I` into the downstream function.

## The fix (applied to `questions/148-bf/verification.k`)

`idxOf` = 8 positive `requires P ==K name` rules **plus** a fallback
`idxOf(P) => -1 requires notBool(P ==K "Mercury") andBool … andBool notBool(P ==K "Neptune")`.
Rule-based (bare-Int result) **and** `notBool(==K)` (not `=/=K`). Both findings are load-bearing.

## Reproduce

```sh
D=verification/humaneval/reference/notes/bf-probe
for v in verif verif2 verif3 verif4; do
  kompile "$D/$v.k" --backend haskell --main-module ${v^^} --syntax-module ${v^^} \
    --output-definition "$D/$v-kompiled"   # module names: BF-PROBE / BF-PROBE2 / BF-PROBE3 / BF-PROBE4
done
# then kprove each $D/spec*.k against the matching *-kompiled (see the tables above)
```
