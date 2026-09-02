# Trust-boundary discovery

The canonical inventory contains three rules, all from
`FIBFIB-VERIFICATION`.

| Source rule | Classification | Reason |
| --- | --- | --- |
| `rule-b44371020fcd21e0007e7bee08ec628a112e7fcc8a28189045b1aa649eaab409` | `DEFINITION` | Base equation for the named mathematical summary `fibFrom`; a nonpositive remaining shift count returns the current first component. |
| `rule-b6e2aed5571df740aad1436d238bffe16db53ff99d0f83547591a7173792f4c5` | `DEFINITION` | Positive recurrence for `fibFrom`; it shifts `(A, B, C)` to `(B, C, A + B + C)` and decreases the remaining count. |
| `rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477` | `DOMAIN_LEMMA` | Integer-arithmetic normalization equating `N - (I + 1)` with `(N - I) + (-1)`. It is an added mathematical fact and carries the `simplification` attribute. |

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
inventory's local rules define the proof summary or supply arithmetic
normalization; ordinary Python execution remains in the imported reference
semantics.

## Separately proved derived lemmas

The separately proved derived-lemma set is empty. In particular, the
arithmetic simplification rule is not a `PROVED_DERIVED_LEMMA`. Stage 1
`prove.sh` first compiles `verification.k` as module
`FIBFIB-VERIFICATION`, which already contains that rule, and then invokes
`kprove spec.k` against the resulting definition. There is no preceding
command, separate specification claim, or module without the rule that proves
the rule's exact statement before reuse.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477`

This classification records the arithmetic identity as part of the trusted
mathematical boundary rather than treating the Stage 1 program proof—which
used the rule—as a proof of the rule itself.
