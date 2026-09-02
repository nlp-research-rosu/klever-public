# Independent Stage 3 classification

The trusted inventory selects `MPY-VERIFICATION` as the main module and finds
only that module in the local module closure inside `verification.k`. Its
`imports MPY` target is supplied by `semantic.k`, not defined as another local
module in `verification.k`.

The operational K rules are visibly separate: `semantic.k` lines 128–199
rewrite the `<k>`, `<env>`, `<functions>`, `<input>`, and `<result>` cells to
execute the translated Python AST. None of the 11 inventoried rules rewrites a
configuration cell or a program operation. All inventoried heads are symbols
declared with `[function]` in `verification.k` lines 10–15.

| Source rule ID | Span | Independent class | Reason |
|---|---:|---|---|
| `rule-b29a7b1f61d027c75f5d54e6f778c4ffafe703f461096a1d08700bae9b5849da` | 17 | `DEFINITION` | Base equation for the named recursive scanner summary `runSpec`. |
| `rule-03d30c437cb7bd8a90fd37a82631921d6c5bd459ea8924300ffafa088b28240e` | 18 | `DEFINITION` | Space recurrence for `runSpec`; consumes one `Chars` constructor. |
| `rule-ee28b1b89c45af68725d2c53c17fec71114155badb89a86ba1370ef263893c24` | 19 | `DEFINITION` | Opening-parenthesis recurrence for `runSpec`; consumes one constructor and updates summary accumulators. |
| `rule-ee734da296fe2d2d4070e9117fa1dc33181b3c52f7e9629c362ebe25fa07a852` | 20 | `DEFINITION` | Totalized zero-depth closing-parenthesis recurrence for `runSpec`. |
| `rule-a1305acd847b564566d980520b2960809147091b2fc541ba1b00bc3534001edd` | 21 | `DEFINITION` | Depth-one closing-parenthesis recurrence for `runSpec`, completing a group. |
| `rule-23aee5f25569cab008c78f770e7a68f475ee096ae14e72789cb7a87d5c7b6e26` | 22 | `DEFINITION` | Nested closing-parenthesis recurrence for `runSpec`; structurally reduces the remaining input. |
| `rule-6e9d63e72f1d96b8d7ba85bd3016f00960ddff320ccba1bd43d74b23295b5f90` | 24 | `DEFINITION` | Constructor projection defining `stateDepth`. |
| `rule-5b065840a104280bdea14bf8cbfb96a45454e5d3f68448977ab8119c3521b55a` | 25 | `DEFINITION` | Constructor projection defining `stateCurrent`. |
| `rule-4c968b2b2cfa45f88ae0c5dcf90432112081bb44e8a2471c9a987aa90bd17bfe` | 26 | `DEFINITION` | Constructor projection defining `stateOutput`. |
| `rule-109874df159aa48ad8e1b3715b0ea513f28bc7bb9b410bf89eb790601fd826a4` | 27 | `DEFINITION` | Constructor projection defining `stateLast`. |
| `rule-83fdf9d2c3bc8712363c660c4deb46f4e4be4ae1056e9f139ccca451b876e6df` | 28 | `DEFINITION` | Entry definition for the named `separateSpec` summary. |

No entry qualifies as `PROVED_DERIVED_LEMMA`: the file contains rules, not
claims, and Stage 1 does not first prove an exact inventoried rule in a module
without it and later reuse it. The two claims are instead in `spec.k`, compiled
after all 11 definitions are already present.

No entry is a `DOMAIN_LEMMA`: every entry is an equation that defines a named
summary, recurrence, or projection rather than an independent mathematical
fact needed by the source program/postcondition. No inventoried rule has a
`simplification` attribute.

Independent counts:

- `DEFINITION`: 11
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
