# K rule trust-boundary discovery

## Canonical scope

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory. Its copied inventory identifier is:

`3635b55c581bb693bf9d1f691d4d109988a8b38ca64b5d50a3dfdfb99c6eb22e`

The inventory contains six rules, in one local verification module,
`VERIFICATION`. All six have an empty attribute list. In particular, there are
no canonical rules carrying `simplification`.

## Classifications

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-c66555fbc7562dc499a559e86f61f18f4641f27b060cdaac63d026c4a6228f4a` | `DEFINITION` | Empty-input base equation for `prefixesAcc`. |
| 2 | `rule-ddc7841337c859b509a00b74a2e0a5b7e6bd9580e358dace34a9474cf5433539` | `DEFINITION` | Constructor recurrence defining `prefixesAcc` while consuming the strict `IntSeq` tail. |
| 3 | `rule-86be445e1c689d1c6ed735a9a647f68ed43460e098ac79c711756a84ec51506c` | `DEFINITION` | Empty-input base equation for `finishPrefix`. |
| 4 | `rule-8cbc95a23d5256ceff710bd39a970d4af1d331ffa290596fe0b2a2bf11fe5e63` | `DEFINITION` | Constructor recurrence defining `finishPrefix` while consuming the strict `IntSeq` tail. |
| 5 | `rule-68569d14375a530cd3bc32752b84149ccbaa54ed7ded6be435ffa66ae49a6808` | `DEFINITION` | Empty-input base equation for `finishChar`. |
| 6 | `rule-77a2c1942531821ff4fcd1cb2a8c9e380517c3e7efcf1f6ae4048acf2974e2e8` | `DEFINITION` | Constructor recurrence defining `finishChar` while consuming the strict `IntSeq` tail. |

The three symbols are declared `[function, total]` in mounted
`verification.k`. For each symbol, the two rules split on the disjoint and
exhaustive `IntSeq` constructors `.IntSeq` and `iCons`. Each recursive rule
recurs on the strict tail. The rules name mathematical summaries used by the
loop and target claims; none matches a `<k>` cell, reads or writes an
operational cell, or intercepts fixed-semantics execution. Therefore all six
are definitions, not operational rules or additional mathematical facts.

## Separately proved derived lemmas

There are no separately proved derived rules.

Mounted Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, with all six canonical rules already present. It then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The corresponding mounted `kprove-loop.out` and `kprove.out` both contain
`#Top`. This proves the reachability claims under the compiled definition, but
it does not establish the required ordering for
`PROVED_DERIVED_LEMMA`: no Stage 1 command first proves the exact statement of
one of the six ordinary rules against a module that omits that rule. The
`SPEC.loop-invariant` reachability claim is not a rule in the canonical
inventory and is therefore not an entry in `trust-boundary.json`.

## Other classification sets

- `OPERATIONAL_RULE`: empty. No canonical rule is an execution or observation
  rule.
- `PROVED_DERIVED_LEMMA`: empty. No canonical rule has the required separate,
  prior proof evidence.
- `DOMAIN_LEMMA`: empty. **The domain-lemma set is empty.**

The mounted supplied Python semantics and the K toolchain remain broader Stage
1 trust assumptions, but their rules are not entries in the launcher-generated
canonical local verification-rule inventory and are not added to this JSON.
