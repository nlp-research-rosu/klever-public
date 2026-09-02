# Trust-boundary discovery

The canonical inventory hash is
`bdc76b589c31174ad35d4f87c6970c4c9e6aa6b9be392e0dfd015630536ba6e2`.
Its seven rules occur in `MPY-VERIFICATION`, and all seven are classified
exactly once as `DEFINITION`.

## Classification basis

The first three rules are the mutually exclusive defining branches of
`primeFrom(N, D)`: stop with true after the square-root search bound, stop with
false upon finding a divisor, or recur at `D + 1`. The next two rules define
`isPrime(N)`: values below 2 are false, while values at least 2 expand to
`primeFrom(N, 2)`. The last two rules define the true and false branches of the
structural result helper `chooseVal`.

These are equations and a recurrence that introduce the mathematical summary
and named proof term used on claim right-hand sides. They are therefore
definitions, rather than ordinary program-execution rules or additional
mathematical facts. No inventory rule carries the `simplification` attribute.

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
ordinary execution rules are in Stage 1's `MPY` semantics, while the canonical
inventory supplied for this stage contains only the seven local
`MPY-VERIFICATION` rules above.

## Separately proved derived lemma and evidence

Stage 1 separately proves one reusable derived claim: the generalized loop
invariant in module `LOOP-SPEC` of `/reference/k-proof/spec.k`. It starts at an
arbitrary divisor `D` subject to `2 <=Int D` and proves that the loop returns
`chooseVal(primeFrom(N, D), X, Y)`.

The ordering evidence is explicit in `/reference/k-proof/prove.sh`:

1. `verification.k` is compiled as module `MPY-VERIFICATION`.
2. `kprove spec.k --definition verification-kompiled --spec-module LOOP-SPEC`
   proves the generalized loop claim.
3. Only afterward,
   `kprove spec.k --definition verification-kompiled --spec-module SPEC`
   proves the importing entry-point specification and examples.

That derived lemma is a `claim` in `spec.k`, not a `rule` represented by any
canonical `source_rule_id`. Consequently, it is identified here as Stage 1
proof evidence but does not create a `PROVED_DERIVED_LEMMA` entry in
`trust-boundary.json`. None of the seven inventoried rules qualifies for that
classification: every one is already present in the verification module
compiled before either `kprove` command, so Stage 1 does not first prove its
exact rule statement against a module lacking the rule.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional trusted
mathematical fact used to close the proof; the mathematical-summary rules are
classified as definitions.
