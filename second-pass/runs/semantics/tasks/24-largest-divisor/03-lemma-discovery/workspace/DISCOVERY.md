# Trust-boundary discovery

The canonical inventory contains five rules in the local `VERIFICATION` closure. `trust-boundary.json` reproduces their identifiers in exactly that order.

## Classifications

1. `rule-4dc883be7558c48413570e94ef894be86bb7f2defba4701dddd8ecbdfc6fdf61` is a `DEFINITION`. It expands `largestDivisorBody()` into the exact translated Python statement sequence used by the reachability specifications.
2. `rule-7e08785f2fa3d9871eb727a17489e6ad09a58d3acdd6b1aa0576bb1cf35e0069` is a `DEFINITION`. It initializes the mathematical largest-proper-divisor scan at `N - 1`.
3. `rule-ff250606498fa2b0f63ef3d95275fc5bcf246520b20e477dc18297ba8710f027` is a `DEFINITION`. It is the scan’s terminating equation when the current positive candidate divides `N`.
4. `rule-864338f2577bfe3d8f78663dcfd53efcfbb9747d6d849326441f6cbd4b554fb8` is a `DEFINITION`. It is the recursive scan equation for a nondividing candidate above `1`.
5. `rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630` is a `DOMAIN_LEMMA`. Its `deleteFreshFrame` simplification supplies the extensional Map fact that deleting the newly added fresh frame binding restores the original map.

No inventory rule is an `OPERATIONAL_RULE`: the first four rules define named proof terms or the mathematical reference recurrence, and the fifth adds a mathematical Map simplification.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence in `prove.sh` compiles `verification.k` as `VERIFICATION` before invoking any proof. That compiled module already contains all five inventory rules. The subsequent `kprove` commands prove the `PREFIX-SPEC`, `INIT-SPEC`, and `LOOP-SPEC` reachability claims against that same definition; none of those claims is then installed as a reusable inventory rule. In particular, `deleteFreshFrame` is present during every proof rather than first being proved against a module that omits it.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly `rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630`, the unproved `deleteFreshFrame` Map simplification.
