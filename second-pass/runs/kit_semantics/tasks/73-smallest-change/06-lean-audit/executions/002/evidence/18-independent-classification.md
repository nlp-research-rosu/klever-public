# Independent Stage 3 classification judgment

This is the auditor's classification from the frozen K text and the supplied
MPY operational semantics. It was made independently of the rationales in
`lemma-discovery.json`; that file was compared only after the classifications
below were fixed.

The trusted inventory reconstruction found the verification-module closure in
this order: `VERIFICATION` in `verification.k`, followed by its local import
`VERIFICATION-BASE` in `verification-base.k`. The reconstructed inventory has
14 unique rules and hash
`3f2d6f96e2fde04bddd98fb0e5cc6357e5f39a29c219ed0264215d821bec45b9`.

| # | source rule (short id) | span | independent class | reason |
|---:|---|---|---|---|
| 1 | `80907d17` | `verification.k:9-56` | `DOMAIN_LEMMA` | Replaces the complete initialized operational loop/return configuration with the mathematical mismatch summary. It is program-specific and material. The earlier bridge-free claim is generalized over `C,I`, has an additional guard, and concludes `C +Int mismatchCount(...)`; it is not the exact installed rule. |
| 2 | `360163ba` | `verification-base.k:10-24` | `DEFINITION` | Macro defining the named `smallestLoopBody` AST. |
| 3 | `43ea95f7` | `verification-base.k:27-40` | `DEFINITION` | Macro defining the named `smallestBody` AST. |
| 4 | `e08ccd59` | `verification-base.k:43-44` | `DEFINITION` | Macro defining the named `smallestDef` AST. |
| 5 | `80a92228` | `verification-base.k:49-73` | `DEFINITION` | Macro/named proof term expanding `fixedBuiltins`. |
| 6 | `8277b118` | `verification-base.k:78` | `DEFINITION` | Empty-case equation defining the fresh structural summary `allInts`. |
| 7 | `bb65aed9` | `verification-base.k:79` | `DEFINITION` | Recursive constructor equation defining `allInts`. |
| 8 | `7f56b17c` | `verification-base.k:83-87` | `DEFINITION` | Equation defining the fresh summary `halfLen`; its `simplification` attribute is therefore permitted. |
| 9 | `0a4fd72c` | `verification-base.k:94-103` | `DOMAIN_LEMMA` | Asserts definedness of pre-existing `applyCmp`/`valSeqAt` operations under integer-list and in-bounds guards. It is needed at the exact mirrored comparison in the source loop and no earlier exact proof is run. Its `simplification` attribute is permitted for a domain lemma. |
| 10 | `7d0900f7` | `verification-base.k:108-127` | `OPERATIONAL_RULE` | Ordinary execution/observation step for the selected branch plus its fixed `AugAssign`; it preserves the continuation and residual scope map. Earlier true/false branch claims are separately guarded and are not this unguarded conditional rule. |
| 11 | `68e408c2` | `verification-base.k:132-139` | `DEFINITION` | Defines the fresh pair contribution summary using the supplied comparison. |
| 12 | `d9a3ffca` | `verification-base.k:143-144` | `DEFINITION` | Guarded base equation for fresh recursive `mismatchCount`. |
| 13 | `b924d8f7` | `verification-base.k:145-147` | `DEFINITION` | Guarded recurrence for fresh recursive `mismatchCount`. |
| 14 | `53698f5d` | `verification-base.k:149-151` | `DOMAIN_LEMMA` | Associativity of the pre-existing hooked integer addition, material to reassociating the accumulator and recursive summary. No earlier command proves this exact equation without it. Its `simplification` attribute is permitted for a domain lemma. |

Counts are 10 `DEFINITION`, 1 `OPERATIONAL_RULE`, 3 `DOMAIN_LEMMA`, and
0 `PROVED_DERIVED_LEMMA`. The domain set is nonempty and all three facts are
relevant to the frozen source loop or its result. Every `simplification` rule
is either a `DEFINITION` or `DOMAIN_LEMMA`.

The protected classification has exactly these 14 identities, in this order,
with the same category for every identity. There are no missing, extra,
duplicated, reordered, rehashed, or unaccounted rules.
