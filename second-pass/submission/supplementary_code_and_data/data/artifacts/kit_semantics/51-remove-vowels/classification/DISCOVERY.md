# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, whose embedded
`inventory_sha256` is
`66a4d5e793d791fbdda316eb554e724dae0c3c9a8c8e7a0b4c19a947953aa0c4`.
It lists three rules, all in the local `VERIFICATION` module. Each canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order.

## Classifications

All three rules are `DEFINITION`:

1. `rule-57b0cde04709c6e7a00dfe8653eab54893af58910849881dee897171eda75743`
   is the empty-sequence base equation for `removeVowelsFrom`.
2. `rule-4a0f30aa2efa0ab7a661101ca8c4d5b92435f1906adced2f965cb6025ae9176f`
   is the guarded constructor recurrence that drops a vowel code.
3. `rule-b4fa0061a0832f9024dfe53cedb6eccc549392fe39607aaacbe4eb2194cb1686`
   is the complementary guarded constructor recurrence that appends a
   non-vowel code.

Together these are the base and exhaustive recursive cases of the named
mathematical summary. They match `removeVowelsFrom` terms, not `<k>` or another
runtime configuration, so none is an `OPERATIONAL_RULE`. The latter two carry
the `simplification` attribute, but their statements are still the defining
recurrence itself; the attribute does not turn either equation into an
additional trusted fact.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1's `prove.sh` kompiles `verification.k` with all three rules already in
`VERIFICATION`, then runs `kprove spec.k`. It does not first prove any reusable
rule's exact statement against a module that omits that rule, nor does it
install an exactly corresponding rule only after such a proof. The
`SPEC.loop-invariant` reachability claim is proof evidence for the program, but
it is a claim rather than a rule in the canonical inventory and therefore is
not an inventory entry to classify.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical rule adds an independent
mathematical fact beyond the equations defining `removeVowelsFrom`.
