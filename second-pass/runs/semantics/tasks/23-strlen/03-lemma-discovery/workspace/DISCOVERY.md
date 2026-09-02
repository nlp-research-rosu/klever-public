# Trust-boundary discovery

The canonical inventory hash is
`5fb2cd8fbac239a2c3b33e986d119eee9233d58f66404e269a981b9627f2ad37`.
Its two rules are classified in canonical inventory order.

## Classifications

- `rule-b71ea096f6e92dea97adefa58c521bb4aab0f25d49e84fa784b5a0cb3ceee82d`
  is a `DEFINITION`. In `verification.k` lines 7–15, the syntax declares
  `strlenModule` as a macro and the rule expands that name to the constructor
  tree generated in `solution.mpy`. It is a named abbreviation for program
  syntax, not an additional fact used to reason about string length.

- `rule-b40bd3d53d30e1797dff4bda42d1500c65a0af4579226f8b93f6d759be42af3f`
  is an `OPERATIONAL_RULE`. In `verification.k` lines 18–20, it changes the
  active computation from the harness command `#invokeStrlen(V)` to loading
  the translated module and calling its public function. This is ordinary
  execution setup in the verification model.

Neither inventory rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 `prove.sh` lines 42–46
compile `verification.k` with both inventory rules already present, and line
48 runs `kprove` only on the final claim in `spec.k` lines 8–34. There is no
earlier proof against a module omitting either rule, and no separately proved
claim whose exact statement corresponds to an inventory rule.

## Domain lemmas

The domain-lemma set is empty. Neither rule asserts an additional mathematical
fact: one is a macro definition and the other is an operational transition.
