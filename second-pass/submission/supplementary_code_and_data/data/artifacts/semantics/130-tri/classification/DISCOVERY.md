# K proof trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256` equal to
`22d7ad4bc3ed7a5278b63b8aded18b021a7eb89701c1bb6f41c416fa399e49fa`.
It contains 16 rules, all in `TRI-VERIFICATION`. The classification counts
are:

- `DEFINITION`: 14
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 2

## Definitions

The `triAt` base cases and primary even/odd contract equations define the
mathematical value summary. The `triPrefix` base and append equations define
the mathematical prefix summary. The `prefixIndex` equations define the
observer used by the loop invariant and final postcondition. Finally,
`TriLoopCond`, `TriLoopBody`, and `TriFunctionBody` are macro expansions
defining named proof terms for exact translated AST fragments.

These are definitions even where their K orientation compresses a concrete
expression into a named summary. All simplification rules not identified
below as domain lemmas are definitional equations or structural helpers.

No inventory rule is an `OPERATIONAL_RULE`: the ordinary Python execution
rules come from the supplied `MPY` semantics and are outside this canonical
local-verification inventory. The three local AST rules are macro
definitions, not additional execution semantics.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

1. `rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac`
   identifies the backend-canonical even expression
   `I /Int 2 +Int 1` with `triAt(I)` under the even-index constraints.
2. `rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019`
   identifies the Haskell-backend odd expression after `pyMod` unfolding
   with `triAt(I)` under the odd-index constraints.

Both are reusable arithmetic-normalization facts beyond the primary
`triAt` defining equations. They carry `simplification`, are already present
in `verification.k` when the proof definition is compiled, and have no
separate exact-statement proof in Stage 1. They are therefore trusted
`DOMAIN_LEMMA` rules, not proved derived lemmas.

## Separately proved derived lemmas and Stage 1 evidence

No canonical inventory rule qualifies as `PROVED_DERIVED_LEMMA`.

Stage 1 `prove.sh` performs the relevant operations in this order:

1. It compiles `verification.k` as `TRI-VERIFICATION`; this compilation
   already contains every one of the 16 inventoried rules.
2. It runs `kprove` for `TRI-LOOP-SPEC`.
3. It runs a separate `kprove` invocation for `TRI-CORRECT-SPEC`.

There is no compilation or injection of a newly proved rule between steps 2
and 3, and no inventoried rule is first proved against a module that omits
that same rule. The loop reachability claim in `spec.k` is separately targeted
by the first `kprove` command, and `TRI-CORRECT-SPEC` imports
`TRI-LOOP-SPEC`, but that claim is not a canonical `source_rule_id` in the
local verification-module inventory. Moreover, the second command is an
independent prover invocation rather than consumption of a generated proof
rule or certificate from the first command. Thus it supplies no basis for
classifying any inventoried rule as `PROVED_DERIVED_LEMMA`.
