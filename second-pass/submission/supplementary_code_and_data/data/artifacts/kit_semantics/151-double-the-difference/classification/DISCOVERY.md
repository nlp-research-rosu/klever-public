# Trust-boundary discovery

## Method

`/reference/rule-inventory.json` is treated as the exhaustive canonical
inventory.  It contains 23 rules from the local `VERIFICATION` module closure,
and its inventory SHA-256 is:

```text
7b6228289923d63c0b89687fc42470bbb802c30a6c0f491ffdaf55af87a0ef72
```

Every canonical `source_rule_id` appears once in `trust-boundary.json`, in the
same order.  Classification is based on the rule text and attributes in the
canonical inventory, checked against the mounted `verification.k`, `spec.k`,
`prove.sh`, and `prove-run.log`.  Stage 1's prose labels were not treated as
proof evidence.

## Classification summary

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 15 | Exhaustive equations and recurrences for proof summaries, guarded definitional orientations for the named total projection, and exact macro expansions. |
| `OPERATIONAL_RULE` | 0 | No inventoried rule is an ordinary `<k>` execution or observation rule; program execution remains in the supplied semantics. |
| `PROVED_DERIVED_LEMMA` | 0 | No exact rule statement is proved first against a module that omits that rule. |
| `DOMAIN_LEMMA` | 8 | Unproved simplification facts used to bridge dynamic sorts, characterize cast definedness, normalize projection, or extend fixed static dispatch equations. |

## Definitions

The following are definitions rather than additional facts:

- `numericVals` base and cons rules define the formal numeric-list domain.
- The primary `dtd` base, Int, Float, and `[owise]` recurrences define the
  mathematical result on all value sequences.
- `oddIntSquare` defines an element's contribution.
- `lastNumber` base and recurrence define the final local loop-target value.
- `definedProjectInt` defines the guard for the named total projection.
- The two guarded cast orientations and the Int-collapse rule define
  `projectIntTotal` as the fixed partial Int cast on its defined domain.
- `dtdLoopBody` and `dtdBody` are macro expansions defining named proof terms
  for the exact source body.

The projection orientations carry `simplification`, but they are classified as
`DEFINITION` because they introduce and define the named proof term
`projectIntTotal`; they are not claimed as previously proved facts.

## Domain lemmas

The domain-lemma set is **not empty**.  It contains exactly these eight rules:

1. `rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18`
   — guarded dynamic-`Val` Int equation for `dtd`.
2. `rule-663dfaf9b65e6ba3e1928de01c21ec78aeceec06ef94896d881e0da14372c17c`
   — guarded dynamic-`Val` Float equation for `dtd`.
3. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   — `#Ceil` characterization of the partial Val-to-Int cast.
4. `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`
   — idempotence of `projectIntTotal`.
5. `rule-e0cb703bc5de627528842cad9c26edce5c5ccfba97a015cd76b3ffa227523e1e`
   — equality of `isIntV` and the K `isInt` sort predicate.
6. `rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388`
   — guarded dynamic dispatch for integer `>`.
7. `rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a`
   — guarded dynamic dispatch for integer `%`.
8. `rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc`
   — guarded dynamic dispatch for integer `*`.

Each is a reusable mathematical/sort fact with a `simplification` attribute.
None has the required prior, exact, rule-free Stage 1 proof, so none is labeled
`PROVED_DERIVED_LEMMA` even where Stage 1 comments or prose call it a
"derived lemma" or "exact twin."

## Separately proved derived lemmas

There are **no separately proved derived lemmas** in the canonical inventory.

The Stage 1 evidence is decisive:

- `prove.sh` first kompiles `verification.k` into
  `verification-kompiled`; that file already contains all 23 canonical rules.
- Both positive commands then run `kprove` against that compiled definition.
  Their `#Top` results in `prove-run.log` therefore establish the claims under
  all inventoried rules, not any inventoried rule itself in isolation.
- `spec-vacuity.k` and `spec-body-mutation.k` both require the same
  `verification.k`, so the negative probes do not provide a proof of an exact
  rule against a module omitting it.
- No alternate verification module, rule-free connection spec, or earlier
  `kprove` command proving one of the exact inventoried statements appears in
  the mounted Stage 1 evidence.

Consequently the `PROVED_DERIVED_LEMMA` classification is unused.

## Operational rules

The `OPERATIONAL_RULE` set is empty.  None of the 23 rules matches a program
configuration or adds ordinary execution/observation behavior.  The two body
rules are compile-time macros, while all remaining rules are pure equations or
simplifications.  Ordinary call, loop, binding, comparison, arithmetic,
return, and state-cell execution comes from the supplied reference semantics,
which is outside this local canonical inventory.
