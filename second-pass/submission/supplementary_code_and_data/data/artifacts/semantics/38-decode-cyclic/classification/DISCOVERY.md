# Trust-boundary discovery

The canonical inventory contains 12 rules from `VERIFICATION`, and every one is classified exactly once in `trust-boundary.json`.

## Definitions

Six rules are definitions:

- `decodeBody` expands the named proof term to the translated body of `decode_cyclic`.
- `decodeClosure` defines the closure value used by the claims.
- The two `decodeCodes` equations define the base and recursive cases of the mathematical decoding summary.
- The two `keysBelow` equations structurally define the scope-map invariant on an empty map and on an integer-keyed map entry plus its remainder.

These rules introduce or recursively define named summaries and proof terms. They do not add independent facts about an already-defined operation.

## Operational rules

The local verification-module inventory has no `OPERATIONAL_RULE` entries. None of its rules is an ordinary `<k>` execution or observation rule added to the Python model; operational execution comes from the imported reference semantics. The local `decodeBody` and `decodeClosure` rules are macro/summary definitions, not new execution behavior.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 ordering is decisive:

1. `prove.sh` lines 17–21 compile `verification.k` as the Haskell definition.
2. That compilation already contains every rule in the canonical inventory, including all six simplification rules.
3. Only afterward, lines 23–25 run `kprove spec.k` against that compiled definition.
4. `spec.k` proves an active-frame induction claim and the top-level function-call claim. It does not state and first prove any inventory rule exactly against a module from which that rule is absent.

Thus the comment calling the slice-length rule a “lemma” is not proof evidence for the stricter `PROVED_DERIVED_LEMMA` classification.

## Domain lemmas

The domain-lemma set is **not empty**. It contains six rules:

- `rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d`: length of the symbolic `s[3:]` slice.
- `rule-e4afafd317ff2760b1290163a9583c9ff2cefc541daf634480a32a004199a9f2`: clamping index 3 when the sequence length is at least 3.
- `rule-12b6390dc702f6660b47ee0c0a9b53b2797cbb240846a822a143c2125bd020b7`: monotonicity of `keysBelow`.
- `rule-75fa33282a96ce93976534a56a3cbca68ee1b3b3369c99ec1a39f0690d886745`: `keysBelow` implies the boundary key is absent.
- `rule-f0db16212bf58f7561bc29b239623e9a2ac5f7372a7228b99c3baf953e83b63c`: normalization of insertion at a fresh scope key.
- `rule-d7d11f1fc9fe34f62521436622edf9d5bea2ea8bfb4c788542b09eb6d23ffab9`: normalization of deleting the maximal allocated scope key.

All six carry the `simplification` attribute. They state additional mathematical facts about imported sequence/map operations or consequences of the already-defined `keysBelow` predicate, and Stage 1 trusts them while closing the proof.
