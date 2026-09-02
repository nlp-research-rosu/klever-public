# K proof trust-boundary discovery

The canonical inventory identifies three rules in the local `VERIFICATION`
module closure.

## Classifications

- `rule-772ba268f1a7b7e7a2809c0fff0eb1708b462640adeb23380c1b0a26bec9aac8`
  is a **DEFINITION**. It expands the function-backed
  `#rightAngleTriangleBody` proof term to the exact statement sequence mirrored
  from `solution.mpy`.
- `rule-dc3194c482c9cf0dd5964c66ef7d6b69a6990a004fe770631b2bc9319d9e96c9`
  is a **DEFINITION**. It defines the function-backed
  `#rightAngleTriangleClosure` term from the submitted function's parameters,
  body, and defining environment.
- `rule-897fe19e8f6cd251ddc38df1351b19993ef9ad82b91c59f12bfd525e18172ca7`
  is an **OPERATIONAL_RULE**. It is the verification entry-point rewrite that
  turns the symbolic runner into the ordinary Python-call term executed by the
  supplied semantics.

None of the inventoried rules carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` first
compiles `verification.k` as module `VERIFICATION`; that file already contains
all three inventoried rules. It then runs the sole `kprove` command against
that compiled definition. Therefore Stage 1 has no proof against a module
omitting any one of these rules, and no claim provides the required
proof-before-install evidence or exact rule correspondence for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule asserts an additional
mathematical fact used to close the proof.
