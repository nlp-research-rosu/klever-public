# Independent Stage 3 classification

Canonical inventory hash:
`ffdd03dae916c92bbeabedc0a48396bb3bec96dd06d1b7dedba0533f4cd5d4ae`.

| Ordered rule | Span | Normalized SHA-256 | Independent class | Reason |
|---|---:|---|---|---|
| `filterLoopBody => If(...)` | 17–27 | `7a8aefa8550c8a06b16a409b5174a955c92023c5c954b847bc146b10750b669d` | `DEFINITION` | Expands the fresh `filterLoopBody` macro to the exact source loop-body AST. It neither observes nor replaces runtime state. |
| `filterBody => (...)` | 29–35 | `8e8f01b5e0fd33ceb875a3d4d5eaaabb18bf343c33360eb7a965dd98e22a8685` | `DEFINITION` | Expands the fresh `filterBody` macro to the exact source function-body AST. |
| `isIntV(V) => isInt(V) orBool isBool(V) [simplification]` | 39 | `55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350` | `DOMAIN_LEMMA` | Adds an unconditional symbolic characterization of the pre-existing `isIntV`. Stage 1 compiles it before every proof and never first proves the exact rule in a module omitting it, so it is neither definitional nor a proved derived lemma. It is directly relevant: the source calls `isinstance(value, int)`, fixed semantics routes that call to `isIntV`, and the result summary branches on it. |
| `filterAcc(.ValSeq, ACC) => ACC` | 42 | `577aa383be88832d9bea1ce3fa32e88bef61a50c8c009c29dd02cc4ee6b8dec4` | `DEFINITION` | Base equation for the fresh result-summary function. |
| `filterAcc(vCons(V, REST), ACC) => ...` | 43–49 | `f78e3bc6b47e926e3c06b48a1fe9acb3eb68fda26c3b17ee0c8eb4ad23dfcd03` | `DEFINITION` | Structurally descending recurrence for the fresh result-summary function; together with the base case it covers both `ValSeq` constructors. |

There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. The sole
`simplification` rule is the `DOMAIN_LEMMA`, satisfying the classification
restriction.
