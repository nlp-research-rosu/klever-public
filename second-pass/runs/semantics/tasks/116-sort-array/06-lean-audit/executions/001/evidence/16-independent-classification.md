# Independent Stage 3 classification

The canonical local closure selected by `prove.sh` is exactly
`SORT-ARRAY-VERIFICATION`. It contains nine rules. The imported `MPY` module is
defined in the supplied semantics, not in `verification.k`, so it is outside
the verification-file-local inventory required by the trusted inventory tool.

The classification below is based on each left-hand side's behavior, not its
name or the protected manifest's rationale.

| Canonical index | Source rule ID | Span | Independent class | Judgment |
|---:|---|---:|---|---|
| 0 | `rule-91969a44ebe81e8440544191d47e4d0c77497a01622cf2780ccd6a32cc927b0f` | 9–19 | `DEFINITION` | The fresh nullary function `sortArrayLambda` expands to the exact annotated lambda AST in `solution.mpy`. It is a named syntax/proof term. It does not match a `<k>` cell or preempt execution of `Lambda`. |
| 1 | `rule-3394773e65cd3c685efe7b67a2e0712e9b8385d9cc4918b3d923519206a36953` | 22–27 | `DEFINITION` | The fresh nullary function `sortArrayBody` expands to the exact nested `sorted(sorted(arr), key=...)` return AST. It is a named program-body term. |
| 2 | `rule-1b6b20077ea79be1ae3b91368bba7358d1c81ca17220a6b219ea9a3d990854f0` | 30–31 | `DEFINITION` | `sortArrayClosure` names the closure value formed from the exact parameter, named body, and module environment `0`. Its left-hand side is a fresh proof term, not the operational call form. |
| 3 | `rule-8c3d1fd428ed4fd5551785b792097861c53d170392cd4e0e6e035ef41fdaffca` | 34–35 | `DEFINITION` | `sortArrayModule` names the exact module AST containing `FuncDef("sort_array", Params("arr"), sortArrayBody)`. |
| 4 | `rule-0d67eed4009d8768a79d1e4380a4bfda4237eea93a5b37e43a19e4a8fcea24a4` | 41–52 | `DEFINITION` | `popcountKeyClosure` names the exact closure value for the annotated lambda. Under `functions.k` lines 50–60, the same lambda with empty cell/free-variable lists steps through `#mkLambda` to this `closureValC` value. This rule only defines the fresh name; it does not replace that operational transition. |
| 5 | `rule-a3f1073813f699e9d521caadc3d9c55f9986dec43437ca84e8c209de8bea4a7b` | 55–56 | `DEFINITION` | `sortArraySpec` defines the output summary as the keyed sort of the ordinary pre-sort, with the named key closure. It is an unfolding equation for a fresh summary symbol, not an equality or ordering fact about existing symbols. The underlying `sortVS`/`sortKeyVS` trust belongs to the supplied semantics, not to this local rule. |
| 6 | `rule-e0a2c939ef190cae703a15286afeaedd08d0a4bb51e417bb7225c258617c3b93` | 59 | `DEFINITION` | Base equation of the structural domain predicate `allNonNegativeInts`. |
| 7 | `rule-d9e43013916651d6e2605735e1ab4130026a357ac29da8a57141d13b82a5f557` | 60–61 | `DEFINITION` | Integer-head recurrence of the same predicate, descending on the sequence tail. |
| 8 | `rule-f8d3af040db5b70e848575e68e26451a99858586005b55415778a6bcdeb17e3c` | 62 | `DEFINITION` | The `[owise]` non-integer-head equation completes the predicate definition and returns `false`. It states no mathematical property of another function. |

Independent totals:

- `DEFINITION`: 9
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

No inventory rule has the `simplification` attribute. Therefore there is no
simplification rule requiring a `DEFINITION`/`DOMAIN_LEMMA` correction.

Operational cross-check:

- The annotated lambda reduction in `functions.k` produces the named
  `popcountKeyClosure`; the local definition does not intercept that reduction.
- The inner ordinary `sorted` call allocates `list(sortVS(VS))`
  (`sort.k` lines 34–37).
- The outer keyed `sorted` call dereferences that list through ordinary call
  routing and allocates `list(sortKeyVS(sortVS(VS), KV))`
  (`sort.k` lines 45–62). Thus `sortArraySpec` is the relevant summary shape.
- For non-negative `N`, `bin` yields `"0b" ++ binCodes(N)` and string `count`
  evaluates to `cntSub`; these are supplied-semantics operational rules, not
  hidden local domain lemmas.

Counterfactual classification checks:

- Replacing the right-hand side of `sortArraySpec` with `VS`, a constant, or
  only `sortVS(VS)` would remain syntactically a definition but would cease to
  summarize the frozen program; the actual equation has the two operationally
  required sorts and the exact key closure.
- Replacing `popcountKeyClosure` with an identity/constant closure would no
  longer be the value produced by the source lambda; the actual closure body
  exactly matches `solution.mpy`.
- Reclassifying any of the nine equations as a domain lemma would be wrong:
  none proves a property about an already defined source operation. Each
  introduces or completes a fresh named term, summary, or recurrence.

Conclusion: the protected Stage 3 manifest's nine `DEFINITION`
classifications are independently confirmed, and the true domain-lemma set is
genuinely empty.
