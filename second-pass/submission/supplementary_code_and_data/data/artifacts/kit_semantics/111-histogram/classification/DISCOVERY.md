# Trust-boundary discovery

## Canonical inventory

The canonical `/reference/rule-inventory.json` has inventory SHA-256
`8355762f852bbf96edc58dc881c1320a840f84700bf8f961adeefc1e834f1d0d`
and contains nine rules, in two local modules: `COUNT-SUMMARY` and
`VERIFICATION`. The recorded Stage 1 verification SHA-256 is
`5c7548ae1a4b8a6f5e2386578f0950e62baed1b2b00a8a40d94e0ddaf54b6157`,
which matches the mounted `/reference/k-proof/verification.k`.

Every inventory rule is classified exactly once, in canonical order, in
`trust-boundary.json`. None of the nine inventory entries carries the
`simplification` attribute.

## Classification

All nine rules are `DEFINITION`. They are pure equations for symbols declared
as total functions, match only their explicit arguments, and do not match or
rewrite MPY configuration cells:

| Inventory position | Source rule | Defined case |
| ---: | --- | --- |
| 0 | `rule-0e257a4ad15e0e26ec2d40a2bdb7104348f30fb607cec9c8268016c2df32ff5c` | `countHistogramCode` empty-sequence base equation |
| 1 | `rule-e835c344071adb5cf8f06eb17d251a967ac9d5ae2edaa67d3f42ef596bfd8015` | `countHistogramCode` cons-sequence recurrence |
| 2 | `rule-d32dc5006d7e4ee002713099c087fb613bfad82730d2c2e21c54afd56d0a067b` | `validHistogramInput` empty-sequence base equation |
| 3 | `rule-9ef0332db5a72b4f18503c215dfb40222289c5651ddbef6e2e7fad578292005c` | `validHistogramInput` cons-sequence recurrence |
| 4 | `rule-bcb3143ad88bf081cf786ab5158df364f6725bdc3a35484a2d7d5de476120b2f` | `maxHistogramCount` empty-sequence base equation |
| 5 | `rule-16a917fc8d42da5cc2fc1a4a7bba75e65b7999838dbe9a9daa88ba945f4a6076` | `maxHistogramCount` cons-sequence recurrence |
| 6 | `rule-0547ef9d878306e0708cee9245a6b3126d85c893b76a24cf3d2ccc4522c9ba63` | `buildHistogram` empty-sequence base equation |
| 7 | `rule-873fc726e8c4c1db886845f8ff0875b9c7bb782452d1d8f3d3e5667015b23e6b` | `buildHistogram` cons-sequence recurrence |
| 8 | `rule-385829d23edb7fb14f9b963a8ed360edd5ebb107deade4c540203c41b439e4a4` | `histogramResult` composition equation |

The first eight rules are exhaustive base/structural equations for four
mathematical summaries or the input-domain predicate. The last rule is the
macro-like expansion of the named final proof term into the two folds. These
rules name mathematical results used by the reachability claims; they are not
ordinary execution or observation rules, so the `OPERATIONAL_RULE` set is
empty.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1 supplies no evidence with the ordering required for that
classification. `/reference/k-proof/prove.sh` first compiles
`verification.k` (lines 16–20), so all nine canonical rules are already
present in `verification-kompiled` before any proof command runs. It then runs
focused proofs for the reachability claims `SPEC.first-count-loop` (lines
21–24) and `SPEC.second-count-loop` (lines 25–28), followed by a proof of all
claims in `SPEC` (lines 29–32). Stage 1 records `#Top` with exit status 0 for
these commands in `/reference/k-proof/PROOF.md`.

The two focused items are claims from `/reference/k-proof/spec.k`, not rules
in the canonical verification-module inventory. Their statements do not
exactly correspond to any of the nine inventory rules, and `prove.sh` never
recompiles a module after proving either claim in order to add it as a reusable
rule. The other loop claims are covered by the all-claims command, likewise
without being added to the verification module. Consequently, Stage 1's
successful loop proofs do not make any canonical inventory entry a
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical rule asserts an extra
mathematical fact used to close the proof: every rule is instead an equation,
structural recurrence, or named-term expansion defining one of the proof's
total summaries. Thus the complete trust-boundary classification has no
domain lemmas.
