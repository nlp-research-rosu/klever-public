# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, schema version 2,
with inventory SHA-256
`da6d570ca5aad66979a01df14308854813e040e7b91e7662cc90b7713d10cb67`.
It contains six rules, all from `VERIFICATION`. This report follows that
inventory exactly; imported Stage 1 files are used as evidence but do not add
rules beyond the launcher's canonical list.

## Classification

| Inventory order | Source rule | Classification | Basis |
|---:|---|---|---|
| 1 | `rule-81fe4f69cf7ab212987021b7d8c879f9934d9377d4b91bbf98dca24bbbb92549` | `DEFINITION` | Exact expansion of the named translated loop-body AST. |
| 2 | `rule-11625be1d29d6741955954718f3701fe5f097e745430f303e047b26b60e798b5` | `DEFINITION` | Exact expansion of the named return-expression AST. |
| 3 | `rule-08f10d82d1d9cf5aaa12a66a72897eea21304575f4314ef709a86b80776a44f7` | `DEFINITION` | Exact expansion of the complete named function-body AST. |
| 4 | `rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c` | `DOMAIN_LEMMA` | Guarded `islower` simplification for existing `applyMethod`; no exact prior proof of this rule. |
| 5 | `rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c` | `DOMAIN_LEMMA` | Guarded `isupper` simplification for existing `applyMethod`; no exact prior proof of this rule. |
| 6 | `rule-3c5715f409e07a5b606d19b237104b7c169175fa863d23d9c2f35cd45be9c962` | `PROVED_DERIVED_LEMMA` | Exact bridge-free connection claim over the rule's full guard and arbitrary continuation. |

The first three rules introduce named proof terms and only expand those names;
they are definitions rather than execution-model rules or additional facts.

The fourth and fifth rules carry the `simplification` attribute and extend the
pre-existing MPY `applyMethod` operation for a symbolic `Val`. They therefore
cannot be classified as ordinary operational rules under the requested
constraint. They also do not meet the exact-prior-proof requirement:
`CONNECTION-SPEC.islower` and `CONNECTION-SPEC.isupper` start from
`#applyK(toCall(boundMethodV(str(CS), ...)), .Vals)` and prove the frozen
constructor results. Those claims support the intended equations, but they are
not the exact guarded rules over `V:Val` with `isStringKey(V)` and
`notBool isRefV(V)`. Both simplifications are consequently `DOMAIN_LEMMA`.

## Separately proved derived lemma

Exactly one inventory rule is a separately proved derived lemma:

`rule-3c5715f409e07a5b606d19b237104b7c169175fa863d23d9c2f35cd45be9c962`.

Its Stage 1 evidence is:

- `/reference/k-proof/connection-spec.k`, claim
  `CONNECTION-SPEC.isinstance`, proves the same
  `#applyK(toCall(builtinV("isinstance")),
  (V,typeV("str"),.Vals))` transition to `isStringKey(V)`.
- The claim has the same `notBool isRefV(V)` domain as the rule and explicitly
  quantifies over `CONT:K`, corresponding to the rule's `<k> ... </k>` suffix.
- `/reference/k-proof/connection.k` imports `PROOF-THEORY` and does not import
  `VERIFICATION`, so the module used for the connection proof does not contain
  the priority rule being justified.
- `/reference/k-proof/prove.sh` compiles `CONNECTION`, runs
  `kprove connection-spec.k --definition connection-kompiled --spec-module
  CONNECTION-SPEC`, and only afterward runs the positive `SPEC.loop` and
  `SPEC.target` proof commands.
- `/reference/k-proof/PROOF.md` records `#Top`, exit 0 for that connection
  proof.

The rule is therefore classified as `PROVED_DERIVED_LEMMA`, even though its
shape is an operational bridge: the exact reusable transition was established
against a bridge-free module before the positive target proofs used it.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c`;
- `rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c`.

There are no rules classified as `OPERATIONAL_RULE`: the only non-simplification
execution-shaped rule satisfies the stricter proved-derived criterion.
