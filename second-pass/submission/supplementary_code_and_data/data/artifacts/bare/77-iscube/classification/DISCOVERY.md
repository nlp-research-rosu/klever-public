# K proof trust-boundary discovery

The canonical inventory has SHA-256
`768c6d425e02156c7113c418107467c11510230db45758138d0307d7efd017c9`
and contains four rules. This report classifies those four rules only, in the
inventory's order.

| Source rule ID | Classification | Reason |
|---|---|---|
| `rule-de3f9727c1b2c9f19559bcf49d9facf57997eb3c9d4715f670ff6644a77098f9` | `DEFINITION` | Expands the named `iscubeProgram` proof term into the exact MPY program constructor tree. |
| `rule-b88003e929c70fa00f8441eaf77e74ba66845261dacd5efbb19e5da9b5a59865` | `DEFINITION` | Defines `cube(I)` as `I *Int I *Int I`. |
| `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027` | `DOMAIN_LEMMA` | Adds an open-cube-gap implication as a `[simplification]` fact used by the nonlinear loop proof. |
| `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f` | `DOMAIN_LEMMA` | Adds the corresponding `[simplification]` fact identifying the terminal index as `N +Int 1`. |

## Stage 1 proof ordering

Stage 1 `prove.sh` lines 32–39 compile `VERIFICATION` and prove
`CUBE-SPEC`. That module contains the program-tree and `cube` definitions, but
not the two rules declared later in `GAP-VERIFICATION`.

Lines 42–49 then compile `GAP-VERIFICATION`, with both simplification rules
already included, and run `kprove` on `GAP-SPEC`. Therefore the successful
`GAP-SPEC` proof uses those rules as available facts; it is not prior evidence
proving either exact rule against a module in which that rule is absent.

No canonical inventory rule is a `PROVED_DERIVED_LEMMA`. The `cube-loop` item
in `CUBE-SPEC` is a separately checked reachability claim, but it is not one of
the canonical inventoried rules and does not exactly correspond to either
later simplification rule. Consequently it cannot establish the required
rule-before-use ordering for either domain lemma.

No canonical inventory rule is an `OPERATIONAL_RULE`. The ordinary MPY
execution rules are in `semantic.k`, but they are not present in the
launcher-generated canonical inventory and are therefore outside this
classification list.

The domain-lemma set is **not empty**. It consists exactly of:

- `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027`
- `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f`
