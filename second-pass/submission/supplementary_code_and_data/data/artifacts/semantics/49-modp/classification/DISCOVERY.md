# Trust-boundary discovery

The canonical inventory contains three rules, in the order reported by
`/reference/rule-inventory.json`. All three are classified as `DEFINITION`.

- `rule-71d349ffafcb30fd76f8fe497ddc3bd83e9c8f32d2e73927d650e4dc1e713860`
  expands `modpBody` into the exact translated statement sequence from
  `solution.mpy`. It is a structural abbreviation for program syntax.
- `rule-642fa0e1d269068ee1ff23a4190cc20e8dd97d36c91e0e7fdd0f6fc2160ca730`
  expands `modpProgram` into the module-level function definition. It is also
  a structural abbreviation for program syntax.
- `rule-979f0d2fa1ec906f8e5bf589b74d8f25cd25fe0ce31c6c16227b18246e343ea5`
  defines the named mathematical summary `specModp(N, P)` as
  `pyMod(2 ^Int N, P)` when `N >=Int 0` and `P >Int 0`. This merely names the
  contract expression in terms of operations supplied by the reference
  semantics; it does not state an extra property of exponentiation or modulo.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as
`MODP-VERIFICATION`, which already contains all three inventory rules, and
then runs `kprove spec.k` against that compiled definition. It has no earlier
proof command against a module omitting any inventory rule, and therefore
provides no ordering or exact-correspondence evidence that would justify a
`PROVED_DERIVED_LEMMA` classification.

## Domain lemmas

The domain-lemma set is empty. None of the inventory rules supplies an
additional mathematical fact trusted to close the proof.

There are also no `OPERATIONAL_RULE` entries in the local verification-module
closure: execution behavior comes from the imported reference semantics,
while the canonical inventory is limited to the three local definitions
above. No inventory rule carries the `simplification` attribute.
