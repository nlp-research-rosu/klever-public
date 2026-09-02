# Trust-boundary discovery

The canonical inventory has one rule, in `VERIFICATION`, and that rule is
classified exactly once.

## Classification

`rule-6f56e984cb3d0fc19ad90190688aabe5b4fa9cd665cd8ddc4bb1e7b98d9eb69f`
is an `OPERATIONAL_RULE`. It is a transition on the `<k>` cell that turns the
`verifyBF` harness invocation into execution of `solutionProgram`, followed by
`invokeBF` with the same two inputs. It therefore initiates an ordinary run of
the verification model. It does not define a mathematical summary and does
not supply an independent mathematical fact.

The inventory gives this rule no attributes, so there are no
`simplification`-attribute rules requiring classification as `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` into
`verification-kompiled` and only then runs `kprove spec.k` against that
definition. The sole inventory rule is already present in the compiled module
during the positive proof. The later mutation probe uses the same compiled
definition and is expected to fail. Stage 1 contains no earlier proof of the
rule's exact statement against a module from which that rule is absent, so
there is no evidence satisfying the required proof-before-installation
ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No canonical inventory rule adds a mathematical
fact trusted to close the K proof.
