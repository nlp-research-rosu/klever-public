# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is treated as the exhaustive canonical rule
inventory. Its copied inventory digest is:

```text
11a97077795acdba4d3bb7290d390b37e211fd8696e566f66fe2af8c1f6b3c68
```

The inventory contains 14 rules, all from the Stage 1 `VERIFICATION` module.
Each appears exactly once and in canonical order in `trust-boundary.json`.
Reachability claims from `spec.k` are not canonical rule entries and therefore
are not added to the JSON.

The classification counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 4 |

No canonical rule is an ordinary `<k>`-cell execution or observation rule.
The inventory consists of named predicates/folds/projection equations and
proof-time simplifications, so the `OPERATIONAL_RULE` set is empty.

## Definitions

The following rules are equations or structural recurrences defining named
proof terms:

- `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08`
  and
  `rule-d1d219f3427f5536073a572ec05d566def4e43ec32fddd6fbff02d536113eb4e`
  are the empty and constructor equations for `allInts`.
- `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5`
  defines `definedProjectInt` as the existing `isInt` predicate.
- `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0`,
  `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`,
  and
  `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442`
  define the guarded `projectIntTotal` proof term, its symbolic reverse
  orientation, and its static `Int` case.
- `rule-72e5eac672dc42c33a08defca9cae94adfeb15589c8e4181a9bc48cdc32e7a63`
  and
  `rule-7f9611f1ad40bdd1fce4065a2139931095c8d3af173a8dbcb75b95576da67c98`
  are the base and recurrence equations for `sumFrom`.
- `rule-421bf17a6cbeb7277fb51e605cd8c239397335231755fe2e0b862ab38281bbc8`
  and
  `rule-1e836dcf2b1df7f6322a01e54db668a6f35bbb7b27c89af9bd65f887168bade0`
  are the base and recurrence equations for `productFrom`.

The projection orientation rules carry `simplification`, but they remain
definitions: together they orient the guarded defining equality between the
new named term and K's partial cast. This satisfies the requirement that every
rule carrying `simplification` be classified as either `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 evidence is decisive:

1. `/reference/k-proof/prove.sh` first compiles
   `/reference/k-proof/verification.k` as the Haskell
   `verification-kompiled` definition.
2. That source already contains every one of the 14 canonical rules.
3. Every positive or negative `kprove` command then uses that same compiled
   definition.
4. There is no command that compiles a module omitting a candidate rule and
   first proves the candidate's exact statement.

The `#Top` in `/reference/k-proof/prove.log` proves the reachability claims
under the already extended theory. The mutation probes test discrimination but
do not establish any canonical rule as a prior theorem. Consequently, comments
and `PROOF.md` descriptions that call the cast-definedness or widened
`applyBin` rules “derived” are not evidence for the stricter
`PROVED_DERIVED_LEMMA` classification required here.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly four rules:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
  trusts the `#Ceil` characterization of the existing partial `Val`-to-`Int`
  cast.
- `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`
  trusts idempotence of `projectIntTotal`.
- `rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0`
  trusts the widened dynamic-sort addition equation under `isInt` guards.
- `rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4`
  trusts the corresponding multiplication equation.

All four carry `simplification`, are available while the target proof runs,
and lack the required earlier exact proof against a module that omits them.
They are therefore explicit trusted mathematical facts in the finalized proof
boundary, not proved derived lemmas.
