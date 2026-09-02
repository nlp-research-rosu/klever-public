# pow-probe — intercepting a symbolic `**` to an opaque power

## Finding

kprove HANGS on `10 ** (n-2)` for a symbolic `n`: the reference reduces `**` to `I1 ^Int I2`, and
`^Int` with a symbolic exponent is nonlinear — the Haskell backend / Z3 never converges. Modelling
the power as an **opaque** primitive `ipow(B, E)` (`[function, total, symbol(ipow), no-evaluators]`,
plus a `[concrete]` rule for krun) fixes it — but only if the COMPUTED side actually produces `ipow`
instead of `^Int`. Two ways to make it do so were probed:

- **Function-rule override** (`rule applyBin("**", B, E) => ipow(B, E) [priority(40)]`): **does NOT
  work.** `applyBin` is a `[function]` defined in an imported module (MPY-OPERATORS); adding a
  higher-priority rule for it in a downstream module does not override the imported rule — `^Int`
  still fires and kprove hangs (`ps.k` with this variant of `pv.k` ran > 2 min, no result).
- **K-cell rewrite interception** (`rule <k> RV:Int ~> #binR("**", LV:Int) => ipow(LV, RV) ... </k>
  requires RV >=Int 0 [priority(40)]`): **works** — `ps.k` proves `#Top` in ~10 s. Catching `**` at
  the `#binR` continuation (BEFORE it becomes `applyBin`) is a k-cell rewrite, and k-cell rewrites
  ARE ordered by `[priority]` (same mechanism as the is_prime / memberVS / count7 interceptions).

## Takeaway

To intercept a shared OPERATOR problem-locally, rewrite its k-cell continuation
(`#binR(OP, LV)` / `#cmpR(OP, LV)`), not the `applyBin` / `applyCmp` function. Used in
`questions/83-starts-one-ends`.

## Files

- `pv.k` — probe module: opaque `ipow` + the k-cell `#binR("**")` interception.
- `ps.k` — claim `result == ipow(10, N-2)` for N>=2 (proves `#Top` fast with the k-cell version).
