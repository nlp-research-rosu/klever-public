# Trust-boundary discovery

## Canonical scope

The sole classification source is `/reference/rule-inventory.json`, whose
`inventory_sha256` is
`a2523def47030dccad31ef8683dd617cfc620e1f05b3fe7f963639ba8eee7c2f`.
It contains 55 rules from the local `VERIFICATION` closure. The output preserves
their canonical order and classifies each `source_rule_id` once.

The mounted Stage 1 workspace under `/reference/k-proof` was inspected
read-only. No Stage 1 artifact was edited or copied.

## Classification method

- `DEFINITION` is used for new-symbol equations and structural recurrences:
  the total projection terms when the new projection is the defined head,
  domain predicates, sequence predicates, `codesOf`, `numericView`,
  the complete `numericGt` table, the concrete definition of `maxFOpaque`,
  and the four recursive maximum summaries.
- `DOMAIN_LEMMA` is used for unproved additional facts about existing K or MPY
  symbols: the four `#Ceil` characterizations, the four reverse cast
  orientations, the three `applyCmp` dispatch simplifications, the symbolic
  `maxFloat`/`maxFOpaque` equality, and the three sort-disjointness
  simplifications.
- `OPERATIONAL_RULE` is unused. The canonical local inventory contains pure
  equations and simplifications, not a rule over an execution configuration or
  an observation cell.
- `PROVED_DERIVED_LEMMA` is unused for the evidence reason below.

All rules carrying `simplification` are classified only as `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `/reference/k-proof/prove.sh` first kompiles `verification.k` as the
`VERIFICATION` module and then runs:

- `kprove spec.k ... --spec-module SPEC`;
- `kprove spec.k ... --spec-module SPEC-STR`; and
- three expected-failure mutation probes.

Every one of those spec files requires `verification.k`; no command proves an
inventory rule's exact statement against a module from which that rule has
first been removed. The positive `#Top` results therefore prove the target and
circularity claims under the complete rule set, not any inventory rule in the
ordering required for `PROVED_DERIVED_LEMMA`. Comments such as “dispatch twin”
or “restates” are not treated as proof evidence.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains 15 rules:

- Int cast facts:
  `rule-83a120e7a0765b750dbc0ef3eb515f2d8b64c7b50538b3bebbd1cc4789cf8d3e`,
  `rule-0c81e675943b09f77b3c9bcde8bf866227b1fb965fcb1d308e097cea0abff848`;
- Int comparison dispatch:
  `rule-15d2159bad2a7aea7a496c3fcc1a2424c1e94a787eca67f2288469b2dd32820e`;
- Float cast and primitive facts:
  `rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e`,
  `rule-0efb958402771e00f0c87dc7fc8ee7185fb8aee4c9d4eb3d4fe5a2200a1a9fac`,
  `rule-d3c655f03d0599014d0675fb90b301045c507f274904692d149e1aa3aa5fcc6e`;
- Bool cast facts:
  `rule-94291474df49f0025fadd1e009e9c1267cf9fc22cb9d891f2604783277c3365c`,
  `rule-da035816c11ad6dff67d5301ca6654c3f3a6aa6e611daf47d9809952ebb70c73`;
- Str cast facts:
  `rule-eba3d8bb8496c9c5885aaf564d4bb58cbf5f171260b498cb2ecf9199e4de2bb6`,
  `rule-3802c35df0656a078865fc6fd93f989eff8400fa623325e53283e267b01869a2`;
- dynamic numeric and string dispatch:
  `rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e`,
  `rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d`;
- sort disjointness:
  `rule-217c86e6ea02fd8a4d522673cccf435e5bd87a23e18f17f498dfd31b0197c5d2`,
  `rule-fd5dc7e25c9b6aa2d8b03dc179dba72357ad91d531372a1f977f6d6f5ddf44ba`,
  `rule-add4293d1db932d0d69adaa4f5856603221b0a4520153f408fd85c3d29640f08`.

These rules may be mathematically plausible or mirror fixed semantics, but the
mounted evidence does not establish them in the separate, prior, rule-free
fashion required by this discovery schema.

## Counts

- `DEFINITION`: 40
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 15
- Total: 55
