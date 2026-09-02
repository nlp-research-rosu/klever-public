# Trust-boundary discovery

## Canonical scope

The sole classification source is `/reference/rule-inventory.json`. Its
canonical `inventory_sha256` is
`d86e2617188d6ba4a76b8b0d18613904c9a2b3607d2af2956cac4ffc88f494f9`.
It contains 10 rules, in modules `VERIFICATION-SYNTAX` and `VERIFICATION`.
`trust-boundary.json` preserves that order and includes each canonical
`source_rule_id` exactly once.

The inventory reports no rule with the `simplification` attribute.

## Classification

All 10 canonical rules are `DEFINITION`.

The first four rules define named proof syntax:

- `rule-3016862...433e` expands `triLoopCondition` to the exact comparison AST.
- `rule-9f977117...98c` expands `triLoopBody` to the exact branch/append/increment
  AST.
- `rule-f6885500...009` expands `triFunctionBody` to initialization, loop, and
  return syntax.
- `rule-9a61ae48...715` expands `triDefinition` to the required function AST.

These are macro expansions attached to `[macro]` syntax declarations. They name
constructor terms and do not supply runtime Python behavior; execution remains
in the imported fixed MPY semantics.

The remaining six rules define mathematical summaries:

- `rule-c4c4c3e5...588`, `rule-5a5bbd97...53f`, and
  `rule-ffc8510a...d90` are the negative, nonnegative-odd, and
  nonnegative-even defining cases of total function `triValue`.
- `rule-c64282d3...de2` and `rule-503acfd8...37f` are the base and recursive
  defining cases of `triComplete`.
- `rule-a3d3f0c...f54` defines `triResult` as a call to `triComplete` from the
  empty prefix.

The `triValue` guards partition the intended cases, while the `triComplete`
guards `I > N` and `I <= N` are complementary. These equations define the
summaries used in the claims; they are not separately asserted mathematical
facts beyond those definitions.

No canonical rule is an `OPERATIONAL_RULE`. None matches `<k>` or another
configuration cell, performs an observation, or adds an execution step to the
verification model.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

Stage 1 `prove.sh` first kompiles the complete `verification.k`, containing all
10 canonical rules, and only then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The resulting `#Top` in `proof-all.out` and `prove-run.out` proves the claims
under that already-complete theory. The focused `#Top` results in
`proof-loop.out` and `proof-math.out` likewise do not show any canonical rule's
exact statement being proved against a module from which that rule was absent.
No Stage 1 command builds such a rule-free predecessor module and then admits
an exactly corresponding rule.

The `SPEC.tri-loop` circularity and the four arithmetic properties in `spec.k`
are claims, not rules in the canonical inventory. Their successful proofs
therefore do not turn any inventory rule into a separately proved derived
lemma.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule is an extra trusted mathematical fact used only to make the
proof close. In particular, there are no local simplification axioms, algebraic
rewrite lemmas, or comments labeled as lemmas that lack prior proof evidence.
