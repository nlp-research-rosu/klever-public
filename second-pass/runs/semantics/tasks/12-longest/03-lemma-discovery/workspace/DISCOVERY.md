# Trust-boundary discovery

The canonical inventory contains nine rules, all in the Stage 1 `VERIFICATION`
module. Each is classified exactly once in `trust-boundary.json`, in canonical
inventory order.

## Definitions

Seven rules are definitions:

- `rule-61a7e85b99e1fd517b3f029cca636566b11a786aa2f24d053db8e5dea4317820`
  and
  `rule-06cf824ccd2247d57e4141172b5e6494e4acc57dc1a88a94144097b09d59b0c1`
  are the base and recursive equations for `stringVals`, the structural
  embedding from the proof-domain `StringSeq` into MPY `ValSeq`.
- `rule-f40c65506711d9264ce5e002c00c58e14bffb284ba0a0ef1e062022c850058fa`,
  `rule-4344ff90b2feb479d11bd8ad23e5a852fa65b2184ee2ab2a22a60b8b24b7a9ba`,
  `rule-0f388914c90471f2074c0ae8359e3fa11b9f73200e404e8cded4c53936bcd932`,
  and
  `rule-370c2d5a71b42f964c5e0bc4fde658a3d2f206ee26b68793283aebc5d57f27f9`
  define the `longestAcc` mathematical fold. Its strict-update and
  shorter-or-tied branches encode first-on-tie behavior.
- `rule-1b6d53d96f4b4a82eb6b7f9bafc5577f204500d0110e04dbb065f0e26a91bc18`
  expands the `longestSolution` macro to the exact closure used by the
  verification claims.

These rules introduce or recursively define named proof-domain terms; they do
not assert independent mathematical facts about already-defined terms.

## Operational rules

Two rules are operational:

- `rule-285b45564f2d7dce460b69dbde1ea9178bdc2bd530970d2320373eaba6467c80`
  implements the `#iterDone` observation for an embedded empty sequence.
- `rule-55d56cc27c981347c574d1ce91485262c24edb072a6b353a25dac39dfaa97e32`
  implements the `#iterYield` observation for an embedded nonempty sequence.

Both rewrite the `<k>` cell and participate directly in the MPY iterator
protocol. Although the Stage 1 comment describes them as compositions of the
`stringVals` equations and MPY list iteration, they are present in
`verification.k` before proof compilation and are not separately proved
rules.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 `prove.sh` first compiles `verification.k`, with all nine inventory
rules already present, and then runs `kprove` over claims in `spec.k`. The
first proof command covers `loop-init-empty`, `loop-init-cons`, `loop-empty`,
`loop-longer`, and `loop-retain`; the second covers `load-solution`,
`call-empty`, and `call-cons-dispatch`. Those are reachability claims, not
inventory rules, and no inventory rule's exact statement is first proved
against a module that omits it. Consequently, Stage 1 supplies no ordering or
exact-correspondence evidence that would justify classifying any rule as a
proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact used to close the proof, and the inventory contains no rule
with the `simplification` attribute.
