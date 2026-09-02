# Rule classification discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256:

```text
97f503f0101ebe78977b771b6b95ffc103d3457cd3f5c7ce08ae6874023a1512
```

It contains seven rules in the local `VERIFICATION` module closure. Each
canonical `source_rule_id` appears exactly once in `trust-boundary.json`, in
the same order as the inventory. The inventory contains no rule carrying the
`simplification` attribute.

## Definitions

Six rules are `DEFINITION`:

- `rule-02349ceffec1049d372ce10bf9984d2a928dca91bcce4f527ff08aaa50e88e5a`
  expands the `[macro]` term `sortEvenLoopBody` to the exact translated loop
  assignment AST.
- `rule-61a087dbf540316c7ffe409d318ed1abd81afdc67636986d622fbbcabe7ea30a`
  expands the `[macro]` term `sortEvenBody` to the complete translated function
  body AST.
- `rule-86d3fae28ae4ec7cefa52ecbaea1a03c0f94bfc931a350e0c2beb28c6cd7123e`
  defines `evenCount`.
- `rule-84057d0c37cb0c2e1e806eb747f7016bbc4854bd23ecaad20e6fc13cfcac8ccf`
  is the guarded base equation of `fillEven`.
- `rule-da9594733502733c5baea5c07345e60cff4228109cd5931016f3801b06910350`
  is the guarded recursive equation of `fillEven`.
- `rule-6d751676da4edbf999ca6d4c967d22060cd612334941e4e2f1dd1c404926d54e`
  defines `sortEvenResult`.

The two `fillEven` guards, `I >=Int STOP` and `I <Int STOP`, are disjoint and
exhaustive. These rules are equations, recurrences, or macro expansions; none
asserts an additional mathematical property beyond the named term it defines.

## Separately proved derived lemma

Exactly one inventory rule is `PROVED_DERIVED_LEMMA`:

```text
rule-4cee3e3fae5dc24dccfe7ee0495478a590993ee6d2488173adbb104fb8345a92
```

The rule has operational effect when reused—it accelerates the exact loop,
return, and frame-pop configuration—but the benchmark classification is
`PROVED_DERIVED_LEMMA` because the mounted Stage 1 artifacts demonstrate all
parts of the required proof-before-use discipline:

1. `/reference/k-proof/spec-connection.k` states
   `SPEC-CONNECTION.loop-connection`. After removing only the declaration
   keyword/label and the reusable rule's `priority(40)` deployment attribute,
   its statement token-matches the inventory rule: the same `#loop` term,
   `(Return(...) .Stmts)` continuation, `#endcall`, cell rewrites, maps, heap,
   frame, result, and `I >=Int 0` guard.
2. The connection spec imports `VERIFICATION-NO-BRIDGE`.
   `/reference/k-proof/verification.k` shows that this module imports only
   `VERIFICATION-BASE`; the reusable priority-40 rule is declared later and
   only in the separate `VERIFICATION` module. Thus the proving module does not
   contain the rule.
3. `/reference/k-proof/prove.sh` first compiles
   `VERIFICATION-NO-BRIDGE` and runs:

   ```bash
   kprove spec-connection.k \
     --definition verification-no-bridge-kompiled \
     --spec-module SPEC-CONNECTION
   ```

   Only after that command does it compile the `VERIFICATION` module containing
   the reusable rule and prove `spec.k`.
4. `/reference/k-proof/proof-run.log` records `#Top` for the connection proof
   before the later `#Top` for the target proof.

No other inventory rule has separate proof-before-use evidence, and none needs
it because the other six rules are definitions.

## Operational and domain-lemma sets

The `OPERATIONAL_RULE` set is empty. The only rule with operational shape is
classified by the more specific proved-derived category because its exact
statement was established before reuse.

The `DOMAIN_LEMMA` set is explicitly empty. No additional unproved
mathematical fact occurs in the canonical local verification-module rule
closure.
