# Trust-boundary discovery

## Canonical scope

The sole rule source for this classification is
`/reference/rule-inventory.json`. Its embedded `inventory_sha256` is
`3958f6820b90d65233bc4d4a3ec51b55238409e271c26efe964ec46a14f39f5f`.
The inventory identifies module `VERIFICATION`, verification-source hash
`39ef1863ae8c319165119661dba9507a3e58f9d177eba0f59b3d9df4420a3f3f`,
and 32 rules. `trust-boundary.json` preserves those 32 source IDs exactly once
and in canonical order.

## Classification method and result

I classified by the rule's left-hand operation and role, not by comments or by
whether the equation appears mathematically plausible:

- A rule is `DEFINITION` only where its left-hand head is a fresh symbol
  introduced by `VERIFICATION` and the rule supplies an expansion, equation,
  recurrence, accessor case, or totalization case for that symbol.
- A simplification whose left-hand operation is K's cast/definedness machinery
  or the reference semantics' `applyBin`/`applyCmp` is a `DOMAIN_LEMMA`.
- An `OPERATIONAL_RULE` would be a local execution/observation transition, not
  merely a function that expands to program syntax.
- `PROVED_DERIVED_LEMMA` requires Stage 1 to prove the identical installed rule
  first against a module that omits it.

The resulting counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 27 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 5 |
| Total | 32 |

All rules with a `simplification` attribute are classified as either
`DEFINITION` or `DOMAIN_LEMMA`, as required.

## Definitions

The 27 definitions fall into these fresh-symbol families:

- Program-term expansions: `nextSmallestLoopBody`, `nextSmallestBody`, and
  `solutionProgram`.
- Domain and projection helpers: `allInts`, `definedProjectInt`, and the rules
  whose left-hand head is the fresh `projectIntTotal` symbol.
- Result summaries: every defining case for `scanStep`, `scanAfter`, `scanVS`,
  the four `scanState` accessors, `lastInt`, and `nextSmallestSpec`.

The non-integer `scanVS` and `lastInt` cases remain definitions: they are
explicit totalization equations for fresh functions, irrespective of whether
the target claim reaches those cases.

## Operational rules

There are no `OPERATIONAL_RULE` entries. None of the 32 canonical rules has a
configuration-cell transition or supplies a new execution/observation step.
The three program-syntax helpers expand fresh named proof terms to MPY
constructors; the reference semantics performs the actual execution.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence does not establish the ordering required for
`PROVED_DERIVED_LEMMA`:

1. `/reference/k-proof/prove.sh` compiles `verification.k` into
   `verification-kompiled` before its positive `kprove spec.k` command.
   Consequently, every canonical rule is already installed in the module used
   to produce `/reference/k-proof/proof.out` (`#Top`).
2. The vacuity probe reuses that same `verification-kompiled` definition and
   rejects a false result. It does not prove any canonical rule's exact
   statement in a rule-free module.
3. The body-sensitivity probe compiles `verification-mutation.k`, which imports
   `VERIFICATION`, and then rejects the mutated body's claimed result. It also
   does not prove an identical canonical rule before installation.

Stage 1's prose calls some projection/dispatch equations “derived lemmas,” but
comments and the successful target proof do not meet the stricter exact-prior-
proof criterion in this stage.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these five canonical
rules:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   — a `#Ceil` characterization of K's existing partial Val-to-Int cast.
2. `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`
   — an orientation from that existing cast to `projectIntTotal`.
3. `rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0`
   — guarded integer behavior for reference-semantics `applyBin("+")`.
4. `rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0`
   — guarded integer behavior for reference-semantics `applyCmp("<")`.
5. `rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5`
   — guarded integer behavior for reference-semantics `applyCmp("!=")`.

Each is a simplification fact about an operation defined outside the fresh
verification-symbol layer. None has an exact prior rule-free proof in the
mounted Stage 1 evidence, so all five remain in the trusted mathematical
boundary rather than being erased as definitions or promoted to proved derived
lemmas.
