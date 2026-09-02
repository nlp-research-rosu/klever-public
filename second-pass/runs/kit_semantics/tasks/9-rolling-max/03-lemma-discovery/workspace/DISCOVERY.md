# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`:

```text
1c12e41bbca4ec629cf3f596be0392c2a4657a8a834a0360dc4a6ad77b50e57d
```

It contains 19 rules in the local verification-module closure. Every
`source_rule_id` is classified exactly once and remains in canonical inventory
order in `trust-boundary.json`.

## Classification summary

| Classification | Count | Rules |
|---|---:|---|
| `DEFINITION` | 16 | The equations for `allInts`, `stepMax`, `rollAcc`, `rollingMax`, `foldMax`, and `lastOr`, including their base, recursive, and `owise` totalization cases |
| `PROVED_DERIVED_LEMMA` | 2 | The integer `#bindTgt` specialization and the exact rolling-loop summary rule |
| `DOMAIN_LEMMA` | 1 | The `isInt` existential simplification rule |
| `OPERATIONAL_RULE` | 0 | None remain in this category because both ordinary execution rules in the local closure have qualifying earlier connection proofs |

The summary equations are `DEFINITION` rules because they define named
mathematical predicates or recurrences and do not themselves rewrite the MPY
program configuration. The `owise` cases are also definitions: they totalize
the corresponding summary outside the `allInts` theorem domain.

## Separately proved derived lemmas

### Integer target-binding specialization

Canonical rule:

```text
rule-31a6bac2bd8050884a7695b95e2da949d3afd1ffa512f6f540b7e70fa7be7fd8
```

Stage 1 evidence:

- `verification.k` places the rule in `VERIFICATION-CORE`.
- `bind-base.k` imports only `VERIFICATION-SUMMARIES`; its compiled closure
  therefore does not contain the `VERIFICATION-CORE` target-binding rule.
- `bind-spec.k` states `BIND-SPEC.bind-int-name` with the same
  `#bindTgt(Name(X), I)` transition, arbitrary continuation, environment,
  framed surrounding scopes, map update, parent, and no-closure-cell guard.
  The rule's `<k> ... </k>` ellipsis and the claim's explicit `CONT:K` are the
  corresponding arbitrary-continuation forms of the same statement.
- `prove.sh` compiles `BIND-BASE` and runs the connection proof before it
  compiles the final `VERIFICATION` definition.
- `proof-run.log` line 163 records `#Top` for that first positive connection
  proof.

This ordering and matching statement justify `PROVED_DERIVED_LEMMA`.

### Exact rolling-loop summary

Canonical rule:

```text
rule-59ce8f7a5a66c78d9a389f0872a48ebbc7e48b3ebf905673b33bee12077a79e5
```

Stage 1 evidence:

- `verification.k` places the rule in module `VERIFICATION`.
- `loop-base.k` imports `VERIFICATION-CORE`, not `VERIFICATION`, so its
  compiled closure excludes the loop rule. It does include the target-binding
  specialization, which `prove.sh` has already proved in the preceding stage.
- `loop-spec.k` states `LOOP-SPEC.rolling-loop-connection`. Its loop body,
  `.Stmts ~> Return(...) .Stmts ~> #endcall` continuation, `allInts` guard,
  scope bindings, heap update, allocation cells, stack frame, return cell,
  exception cell, and exit-code cell match the reusable rule.
- `prove.sh` compiles `LOOP-BASE` and runs this connection proof after the
  binding proof and before compiling the final `VERIFICATION` definition.
- `proof-run.log` line 232 records `#Top` for the loop connection. The final
  target proof appears later at line 337.

This is therefore a separately proved reusable rule, classified
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-8722c58a66500d998b33e9332efe3c98d027270e2a8119c0d9554459c8d55f9c
```

That rule has the `simplification` attribute and rewrites truth of the existing
`isInt(V)` predicate into existence of an injected `Int`. It does not define a
new named summary, and Stage 1 `prove.sh` does not first prove its exact
statement against a module without the rule. It is consequently an additional
trusted mathematical fact and is classified `DOMAIN_LEMMA`, regardless of the
informal “lemma” terminology in Stage 1 documentation.
