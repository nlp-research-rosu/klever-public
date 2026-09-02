# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is the canonical inventory. It contains nine
rules, all from `SORT-ARRAY-VERIFICATION`, and no rule has the
`simplification` attribute. The classifications preserve the inventory order
and assign each `source_rule_id` exactly once.

The Stage 1 source confirms that every inventoried symbol is declared
`[function, total]` in `verification.k`. The rules fall into three
definition-only groups:

- `sortArrayLambda`, `sortArrayBody`, `sortArrayClosure`, and
  `sortArrayModule` reconstruct the translated program as named AST, closure,
  and module terms.
- `popcountKeyClosure` defines the expected runtime closure term, while
  `sortArraySpec` defines the result summary using the supplied `sortVS` and
  `sortKeyVS` summaries.
- The three `allNonNegativeInts` equations are the base, recursive, and
  catch-all cases of a structural domain predicate. The `owise` attribute on
  the catch-all case only completes that definition; it does not turn the
  equation into an operational observation rule.

Accordingly, all nine rules are classified as `DEFINITION`. There are no
inventoried `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as
`SORT-ARRAY-VERIFICATION`, with all nine inventoried rules already present,
and then invokes `kprove` once on `spec.k` against that compiled definition.
It never proves an inventoried rule against a module omitting that rule and
then reintroduces the exact statement. Thus no inventory entry satisfies the
required proof-order criterion for `PROVED_DERIVED_LEMMA`.

The four reachability claims in `spec.k` establish module loading,
end-to-end execution, the non-negative popcount key behavior, and the negative
extension. Those claims are proof goals, not reusable rules in the canonical
inventory, so they do not change any rule classification.

## Domain lemmas

The domain-lemma set is empty.

No inventoried rule asserts an additional trusted mathematical fact. In
particular, `sortArraySpec` is a definitional abbreviation even though it
refers to the supplied reference semantics' trusted sorting primitives. The
Stage 1 notes explicitly identify that inherited sorting trust, but no local
inventory rule adds a sorting theorem or other domain lemma.
