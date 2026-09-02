# Independent Stage 3 classification

The trusted inventory reconstructed the local verification-module closure as
`VERIFICATION-SYNTAX`, then `VERIFICATION`. The syntax module contains no
rules. The verification module contains exactly these three rules, in source
order:

| Source rule ID | Span | Normalized SHA-256 | Independent class |
|---|---:|---|---|
| `rule-0151c94749b8017ab1ca7d238620beed0c8ae98bf6d0591e136a99bf3f95d944` | 18–19 | `0151c94749b8017ab1ca7d238620beed0c8ae98bf6d0591e136a99bf3f95d944` | `DEFINITION` |
| `rule-c122a6c58de509694010cd1eeb7f5ecbec714b80ca196cf36fe97c8480fb570a` | 21–22 | `c122a6c58de509694010cd1eeb7f5ecbec714b80ca196cf36fe97c8480fb570a` | `DEFINITION` |
| `rule-3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193` | 24 | `3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193` | `DOMAIN_LEMMA` |

The whole inventory hash is
`7a8023c3b8bec86f0b00d2cce4a8ab35baa1a6a7b47c608ce8f154d9f2d1d923`.

The first two rules are the guarded base and recursive equations of the named
summary function `fibFrom`. Their guards, `N <=Int 0` and `N >Int 0`, are
disjoint and exhaustive over K integers. The positive branch decreases `N` by
one. The symbol occurs in the proof specification, not in the frozen program
body, so these equations name a terminating mathematical summary rather than
preempting program execution.

The third rule states the universal integer identity
`(A +Int B) -Int A = B`. It does not define a new symbol and is not an ordinary
execution/observation rule. Stage 1 compiles it into `verification-kompiled`
before the first `kprove`; there is no earlier proof of this exact rule against a
module that excludes it. It is therefore not a `PROVED_DERIVED_LEMMA`. It is a
`DOMAIN_LEMMA`.

The domain lemma is materially relevant. The frozen source loop executes
`b = a + b` followed by `a = b - a`; under the supplied operational rules,
integer `BinOp` dispatches to K's hooked `INT.add` and `INT.sub`. Establishing
that the new `a` equals the old `b` is exactly the identity in the lemma and is
the transition needed by the `fibFrom` recurrence in the loop invariant.

The only rule carrying `[simplification]` is the domain lemma, satisfying the
classification restriction on simplification rules.
