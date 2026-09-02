# Trust-boundary discovery

The canonical inventory has SHA-256 `a884f8ef58b1e8a15f0626a1551c3d76fe8c2d4cbcb350700cbc4602131edab0` and contains two rules, both from `VERIFICATION`. Each inventory rule is classified exactly once and in canonical order in `trust-boundary.json`.

## Classifications

| Source rule | Classification | Reason |
| --- | --- | --- |
| `rule-d1a23396f61dd26b11833b39066cbd64b498e0dfb07eaea1e6c090daaa0b0893` | `DEFINITION` | The rule is the defining equation for the total function `rightTriangle`. It unfolds the named contract predicate into positive-side checks and the disjunction of the three possible squared-side equalities. It introduces the mathematical summary used by the proof; it does not assert an extra fact about independently defined terms. |
| `rule-4fee0a7dc4c0172c3b675bff411434ca46c778b577d492797129b2328534b07a` | `DEFINITION` | The rule expands the nullary function `solutionProgram` into the translated `Module`/`FuncDef` AST. This is a structural named-proof-term expansion, not operational execution and not an additional mathematical fact. |

Neither canonical rule has a `simplification` attribute. Their classifications are nevertheless `DEFINITION` because both are function unfoldings. There are no `OPERATIONAL_RULE` entries in this inventory; the execution rules in the imported `MPY` semantics are not canonical inventory entries and therefore are not classified here.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first runs `kompile verification.k --main-module VERIFICATION`, which compiles both inventoried rules into `verification-kompiled`, and only afterward runs `kprove spec.k --definition verification-kompiled --spec-module SPEC`. Thus Stage 1 does not prove either inventoried rule against a module from which that same rule is absent. The four items in `spec.k` are reachability claims, not inventoried reusable rules, so they provide no ordering evidence for a `PROVED_DERIVED_LEMMA` classification.

## Domain lemmas

The domain-lemma set is empty. The inventory contains no additional trusted mathematical fact used to close the K proof; `rightTriangle` is the explicit definition of the contract, while `solutionProgram` is an AST expansion.
