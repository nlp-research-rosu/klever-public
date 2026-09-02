# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` has SHA-256
`6518a0e5335bdd735f7d1fc208888cbaffb3c4f9c920f296fc3a5283f2485322`
and contains five rules, all from module `VERIFICATION`. The classifications
below follow that inventory order.

## Classifications

1. `rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf`
   is `DOMAIN_LEMMA`. It is the only rule carrying `simplification`. It trusts
   definedness of the supplied partial ASCII conversion when applied to the
   fixed integer-to-string hook. It is an additional mathematical fact used by
   symbolic proof, not an equation defining a new summary.
2. `rule-d103b0bf43c5480134ff24998aab7d8de1dcb6a242ebb94857dc35a60557cae1`
   is `DEFINITION`. It expands `circularShiftClosure` into the exact
   `closureVal` constructor representation of the translated function.
3. `rule-402746ae5fd5896de06add571676987d516921b32b5a67c3dd97ac0a15e6a04b`
   is `DEFINITION`. It defines the oversized-shift branch of
   `circularShiftResult`.
4. `rule-0f914aff35fd352e2deb2adcd224d21f53f0ebfd8aa096d3c5c9f09a6967abf6`
   is `DEFINITION`. It defines the negative-shift branch of
   `circularShiftResult`.
5. `rule-f54a87e944876d0f1f30b0a06541d47de0fc4d7c746b66c465a942f688c8058b`
   is `DEFINITION`. It defines the ordinary doubled-string rotation branch of
   `circularShiftResult`.

The closure equation and three result equations are equations for total named
proof terms. They do not intercept a `<k>` computation, mutate a configuration
cell, or add an observation step, so none is an `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 script `/reference/k-proof/prove.sh` compiles
`/reference/k-proof/verification.k` at lines 17–20 before running any positive
or negative `kprove` command at lines 22–58. That compilation includes every
canonical rule. No Stage 1 command first proves the exact statement of any
inventory rule against a module from which that rule is absent. The positive
target claims and negative mutation probes therefore do not establish the
ordering required for `PROVED_DERIVED_LEMMA`.

This agrees with the Stage 1 audit in `/reference/k-proof/PROOF.md`: lines
76–93 describe the definedness rule as a trusted fact, while lines 40–74
describe `circularShiftClosure` and `circularShiftResult` as definitional
summaries.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly
`rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf`.
The other four canonical rules are definitions.
