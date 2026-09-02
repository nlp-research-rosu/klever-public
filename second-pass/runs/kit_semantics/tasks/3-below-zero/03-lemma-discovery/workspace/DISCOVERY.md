# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256` `cbd01d2180727a31e50a6a9a84bb19a5f64ee02043eacf45565f265a3fdfb237`.
It contains 14 rules in the local `VERIFICATION`/`VERIFICATION-BASE` closure.
`trust-boundary.json` preserves that order and classifies every canonical
`source_rule_id` exactly once.

## Classification results

The single `OPERATIONAL_RULE` is
`rule-f051c58eece2d330fa7d7511f482d75b7b22e8f9096905625aa42d3b04258e75`.
It is the complete-state `Call(Name("below_zero"), ...)` bridge in
`verification.k`: it changes the execution configuration directly and is part
of the verification model rather than an equation defining a fresh summary.

The eight `DEFINITION` rules are:

- `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08`
  and
  `rule-fa394f9b181c0d7a89141e7d4e865895db0443da2d399ebaeb0492e3a9b63ed4`,
  the base and structural recurrence for the fresh `allInts` predicate;
- `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5`,
  the defining equation for the fresh `definedProjectInt` predicate;
- `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0`
  and
  `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442`,
  the guarded general equation and the `Int` input equation for the fresh
  `projectIntTotal` proof term; and
- `rule-b5021b367bc326b94f3621c82c076c3f031ff1e9001210a5910356c24525191c`,
  `rule-a3084bec5f81759651e4dac35dbf83e4cff2fdbeb62e517c4aca8967bb2eeaa2`,
  and
  `rule-01915b20cb506fa25a513601a18f3a077b78452906dab952ad5311d1c4da08cb`,
  the empty, integer-head recursive, and non-integer totalization equations
  for the fresh `belowFrom` summary.

These rules have a freshly introduced verification symbol at the head of a
genuine input case, base case, or structural recurrence. The
`projectIntTotal(projectIntTotal(V))` simplification is deliberately excluded:
it states idempotence of an already-defined helper rather than defining a new
input case.

The five `DOMAIN_LEMMA` rules are:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`,
  a definedness equation for `#Ceil` of K's generated `Val :> Int` projection;
- `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`,
  a symbolic rewrite from that generated projection to `projectIntTotal`;
- `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`,
  the idempotence fact for `projectIntTotal`;
- `rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc`,
  a guarded addition fact about `applyBin`, an operation already defined in
  the reference semantics; and
- `rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b`,
  a finite-map/scope-deletion identity about externally supplied collection
  and update operations.

Accordingly, the domain-lemma set is **not empty**. Every inventory rule with a
`simplification` attribute is classified as either `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas and Stage 1 evidence

There are **no `PROVED_DERIVED_LEMMA` rules** in the canonical inventory.

Stage 1 does contain relevant pre-install evidence, but it does not satisfy the
required exact-statement correspondence. In `prove.sh` lines 13--19,
`verification-base.k` is compiled first and `connection-spec.k` is proved
against that definition. `verification-base.k` does not contain the call
bridge, and `kprove-connection.out` records `#Top`. The three claims proved in
that run are:

1. `call-prefix-connection` (`connection-spec.k` lines 8--60), which rewrites
   the call only to the evaluated `For` body and establishes the new frame;
2. `for-to-loop-connection` (lines 63--76), which lowers that `For` term to
   `#loop`; and
3. `loop-connection` (lines 80--109), which rewrites the loop and frame-pop
   state to `belowFrom(BALANCE, VS)`.

Only after those claims does `prove.sh` compile `verification.k` at lines
21--24. Their composition supports the operational bridge, but no one of the
three claims is identical to the installed complete-configuration rule in
`verification.k` lines 11--37. Compositional implication is insufficient under
the exact-statement rule, so the bridge remains `OPERATIONAL_RULE`, not
`PROVED_DERIVED_LEMMA`.

The later target and context proofs use the definition that already contains
the bridge. None of the five domain lemmas is first stated and proved exactly
against a module omitting that rule. Consequently, comments such as “derived
lemma,” successful use inside the connection proof, and the `#Top` target result
do not change their classifications.
