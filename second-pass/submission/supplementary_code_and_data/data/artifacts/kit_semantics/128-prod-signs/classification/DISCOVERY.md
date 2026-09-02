# Trust-boundary discovery

## Canonical basis

The sole enumeration source was the launcher-generated, read-only
`/reference/rule-inventory.json`. Its copied inventory digest is:

```text
67bc388005597d52da2f13062beca1be1a2b96c5b6ea5e137605db48107d5a61
```

The canonical inventory contains one rule. `trust-boundary.json` preserves that
inventory order and contains its `source_rule_id` exactly once.

| Inventory rule | Attributes | Classification |
|---|---|---|
| `rule-c908455e78e8ae97070a45812683ccd10a81620c7713a89c5777cc7a2fde98a8` | `priority(30)` | `PROVED_DERIVED_LEMMA` |

No canonical rule carries the `simplification` attribute.

## Separately proved derived lemmas

There is exactly one separately proved derived lemma in the canonical
inventory: the exact `prod_signs` loop transition later installed as the rule
in `verification.k`.

The Stage 1 evidence is:

1. `loop-connection-spec.k` states claim `[prod-signs-loop]`. Its complete
   transition matches the inventory rule: the exact translated loop body and
   combined post-loop `Stmts` continuation reduce to
   `foldResult(REST,TOTAL,SIGN)`; `env` changes from 1 to 0; the exact builtin
   and module scopes are retained while the local scope is removed;
   `scopeLoc` changes from 2 to 1; arbitrary heap and heap location are
   preserved; the single call frame is removed; and `noRet`, `NoExc`, and exit
   code 0 are preserved. There is no guard in either statement.
2. The proof module is independent of the reusable rule:
   `loop-connection-spec.k` imports `LOOP-CONNECTION`, and
   `loop-connection.k` imports `VERIFICATION-BASE`. That import chain does not
   import module `VERIFICATION` or `verification.k`, so it does not contain the
   inventory rule.
3. `prove.sh` first compiles `loop-connection.k` as `LOOP-CONNECTION`, then
   runs:

   ```bash
   kprove loop-connection-spec.k \
     --definition loop-connection-kompiled \
     --spec-module LOOP-CONNECTION-SPEC
   ```

   Only after that proof does the script compile `verification.k` as
   `VERIFICATION`.
4. Stage 1 `PROOF.md` records that this connection command printed `#Top` and
   exited 0. It also records a body-sensitivity probe in which changing
   `seen = 1` to `seen = 0` caused the connection proof to fail.
5. The reusable rule adds `priority(30)`. Priority controls selection when the
   already-proved transition is used as a rule; it does not alter the proved
   reachability statement.

Although the installed rule accelerates operational execution, the requested
classifications are mutually exclusive and its exact transition was proved
before installation against a module that omitted it. It therefore satisfies
the supplied definition of `PROVED_DERIVED_LEMMA`, rather than being classified
as an unproved `OPERATIONAL_RULE`.

## Other classification sets

- `DEFINITION`: empty in the canonical inventory.
- `OPERATIONAL_RULE`: empty after recognizing the sole rule as separately
  proved.
- `DOMAIN_LEMMA`: empty.

The domain-lemma set is explicitly empty: no additional trusted mathematical
fact from the canonical rule inventory is assumed to close the K proof.

No theorem statement, Lean artifact, replacement rule, or alternative
formulation was added to `trust-boundary.json`.
