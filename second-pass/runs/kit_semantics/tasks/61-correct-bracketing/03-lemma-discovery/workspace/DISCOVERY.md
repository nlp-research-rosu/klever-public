# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the canonical inventory.  Its
`inventory_sha256` is
`8c6cab4afd22730fa2defac7902ae428539a33dd8d81fbc13ff2fdbf9369d455`,
and it lists seven rules in module `VERIFICATION`.  `trust-boundary.json`
preserves that order and contains each listed `source_rule_id` exactly once.
No rule absent from the canonical inventory was added to the JSON.

## Classifications

| Inventory rule | Classification | Reason |
|---|---|---|
| `rule-b9c21f71f007e14b87428fc39b47b152444b900cfb5ae90c093a6a0adbe3bac0` | `DEFINITION` | Empty-sequence base equation for `scanBrackets`. |
| `rule-a39e2d4a34fe8d3daf6e7a14ed9cd1f1efc7f40036ee34e406b4a1f8e0ec5a74` | `DEFINITION` | Nonempty-sequence recurrence for `scanBrackets`. |
| `rule-90116861827fe29b6190d60f2c7fa45d68a9e1d53c40cb018cb4bdfd97122478` | `DEFINITION` | Negative-balance case of the `keepValid` definition. |
| `rule-952eaa451e2e2dafbf07e4b2853104ca12d32a5798a18fd07e34328e033d4dc4` | `DEFINITION` | Nonnegative-balance case of the `keepValid` definition. |
| `rule-d9b0adbebf1e3f908a9944544102b6bcd8aee7d5a41871e3719cd38e5470aaa0` | `DOMAIN_LEMMA` | A guarded simplification fact about K's existing conditional, not an equation defining a new proof-local symbol.  It is present during both positive proofs and is not separately proved first. |
| `rule-86c81c4e83f334a250f0f7cd6a3d696ef3dd176482dc7252a0d002fb835aa66c` | `DEFINITION` | Empty-sequence base equation for `bracketInput`. |
| `rule-1e22fa424b19594ef171e00ed16730ba4f24c804316660a9f0a4eeaee1779942` | `DEFINITION` | Nonempty-sequence recurrence for `bracketInput`. |

The six `DEFINITION` rules are equations or recurrences for the three named
proof-local mathematical terms `scanBrackets`, `keepValid`, and
`bracketInput`.  They do not execute or observe an MPY configuration.

There are no `OPERATIONAL_RULE` entries in the canonical inventory.

## Separately proved derived lemmas

No canonical inventory rule qualifies as `PROVED_DERIVED_LEMMA`.

The mounted Stage 1 workspace does contain one separately proved rule outside
the canonical `VERIFICATION` inventory:
`VERIFICATION-WITH-LOOP.loop-lemma` in
`/reference/k-proof/verification-with-loop.k`.  It is not added to
`trust-boundary.json`, because the launcher inventory includes only the
`VERIFICATION` module closure and is authoritative for JSON membership.

Stage 1 establishes the rule in this order:

1. `/reference/k-proof/prove.sh` compiles `verification.k` as module
   `VERIFICATION`, which does not contain `loop-lemma`.
2. It runs
   `kprove spec.k --definition verification-kompiled --spec-module SPEC
   --claims SPEC.loop`; `/reference/k-proof/PROOF.md` records `#Top` and exit
   0.
3. Only afterward does the script compile `verification-with-loop.k`.
4. The configuration rewrite and `requires bracketInput(CS)` in
   `SPEC.loop` (lines 6–50 of `spec.k`) correspond exactly to the installed
   `loop-lemma` statement (lines 8–52 of `verification-with-loop.k`); the
   installed rule additionally carries `priority(40)`.

Thus Stage 1 provides bridge-free proof evidence for that out-of-inventory
rule, while providing no such independent proof for the canonical
`simplification` rule.

## Domain lemmas

The domain-lemma set is **not empty**.  It contains exactly:

- `rule-d9b0adbebf1e3f908a9944544102b6bcd8aee7d5a41871e3719cd38e5470aaa0`,
  the guarded simplification from
  `#if C ==Int 40 #then _X #else Y #fi` to `Y` when `C =/=Int 40`.

This rule is mathematically straightforward, but within the requested evidence
taxonomy it remains trusted because Stage 1 does not first prove its exact
statement against a module from which the rule is absent.
