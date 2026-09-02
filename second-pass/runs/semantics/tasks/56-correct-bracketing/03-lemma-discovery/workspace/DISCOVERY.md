# K proof trust-boundary discovery

The canonical inventory digest is
`e3f58226e37acb7e0c5b36cb997d22117d54afe906492f0de33c894ec694a1e6`.
All 17 inventory rules are classified exactly once and remain in canonical
inventory order in `trust-boundary.json`.

## Classification summary

- **DEFINITION (8):** the eight `bracketResult` rules define the mathematical
  summary used by the specification. They are its base cases, totality cases,
  and structural recurrences over the remaining character sequence and current
  depth. All six inventory rules carrying `simplification` are in this group.
- **OPERATIONAL_RULE (9):** the remaining rules are program-specific execution
  or observation macro-steps in the verification model. They execute the two
  return forms, decide the two bracket-test branches, perform the increment and
  decrement assignments, decide the two negative-depth-test branches, and
  normalize function-frame popping.
- **PROVED_DERIVED_LEMMA (0):** none.
- **DOMAIN_LEMMA (0):** none. The domain-lemma set is explicitly empty.

## Derived-lemma evidence audit

There are no separately proved derived lemmas to identify. In particular, the
comments at `verification.k` lines 37–40 call two return rules “proof-only
derived macro steps,” and lines 155–158 describe the normalized `#pop` rule,
but comments are not proof evidence.

The Stage 1 ordering rules out `PROVED_DERIVED_LEMMA` for every inventory rule:

1. `prove.sh` lines 21–25 compile `verification.k` as module `VERIFICATION`.
   At that point all 17 inventoried rules, including every macro-step, are
   already in the proof definition.
2. Only afterward, at `prove.sh` lines 26–30, `kprove` proves
   `SPEC.loop-zero`, `SPEC.loop-positive`, and `SPEC.correct-bracketing`.
3. Those three claims are loop/correctness reachability claims from `spec.k`;
   none is the exact statement of an inventoried macro-step.
4. Stage 1 contains no earlier proof command against a module from which any
   candidate rule is absent, and no later installation of an exactly
   corresponding proved rule.

Therefore the nine unproved macro-steps are classified by what they do in the
verification model—`OPERATIONAL_RULE`—not by the “derived” wording in their
comments. This classification does not claim that Stage 1 separately proved
their equivalence to the reference semantics.

## Rule groups

The definition group comprises:

- `rule-207b388af4da8e91770cc2e5dfa3334f2c7cb3abab9f4ce3ee0b5556a80d988a`
- `rule-02e7c7d055ee0a9b46b120434c0999517027766a94bbf811a73bad382ff0ca58`
- `rule-562a5b96195210cb93cbe3fd185fb657274985b684d96ae0718c761abc0ae361`
- `rule-c009ca485d92588a2425c7b27ed84d622e0f2a640f43a7fc76576877015e77de`
- `rule-b826036260c387d86c2951c072674f12cd04aa0945d253970449696f289c19a2`
- `rule-5a43aa76ec7c743c09441d94ad4523a0820678ebee2e892b6ae2e0dbea71aafd`
- `rule-d150d34c73b5e7e7df44e0f78637fa08aaea6c0d9b58db2c15bd4de334f75297`
- `rule-c378c485f3ef516beba9ed406d4caefde1b0cc0da12f4770a828cff3410c8f89`

The operational group comprises:

- `rule-1f72614e32dd1a414ca75a0ec691e2b60b8258f18ac8f306bbe1b2a1be8a270b`
- `rule-57ced75c342800317f50e844312847ad8f928210115d5cde67cef55cb640e47a`
- `rule-058845677e89393f24d41dc88e38dda0a47b8b4d7f69b22c1e73b602ee00c856`
- `rule-ac66c3eb9c3f2b06aa9af9b0e89799ad173312c93fc4073c6c0dd8883e693942`
- `rule-ddc41f55ce472ec0464fd6efd6564c320da6eeea40bdf0d4dd924964511ab52a`
- `rule-662848af7bdff96a83b6327aefd9a0a0b9e8543d842dda55ab98579ec53e391b`
- `rule-a15b42e38626ae6fdada659b2b7c77dfd5b56f138e83e83da5f1e5c161a32a9f`
- `rule-d1a6400b306febacfd80cd4002d9b4cb274ff8b92b96779ec73040249b7dfb2e`
- `rule-d0af1511799ccfa9f05017e139cba9803361b235a61051630269ea5149706430`
