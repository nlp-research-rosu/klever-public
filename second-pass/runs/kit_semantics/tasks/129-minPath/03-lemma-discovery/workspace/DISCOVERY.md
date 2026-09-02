# Trust-boundary discovery

## Canonical source

This classification uses `/reference/rule-inventory.json` as the exhaustive
inventory for the local verification-module closure.  Its canonical inventory
SHA-256 is
`2f34de6086439b274fa066f73caa7594f022eb8812c6d5ff00eb4b9566898f3e`.
The mounted Stage 1 workspace was inspected read-only and was not copied or
modified.

All 71 canonical rules are classified exactly once, in inventory order:

| Classification | Count |
|---|---:|
| `DEFINITION` | 64 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 7 |

Every rule carrying `simplification` is classified as either `DEFINITION` or
`DOMAIN_LEMMA`.

## Definitions

The definitions are equations whose root symbol is freshly introduced by the
`VERIFICATION` module, plus macro expansions for fresh syntax abbreviations.
They comprise:

- the structural `IntSeq` predicates and `validPerm`;
- row-major construction, total indexing, and unique-`1` coordinate summaries;
- `chooseMin` and the fresh neighbor-minimum helper chain, including the
  guarded defining expansion of `neighborMin`;
- structural and specialized defining equations for `snocVS`;
- the base and recursive equations for `pairDone`, `oddDone`, `finishRel`, and
  `pathRel`, except for the separate `oddDone`/`pairDone` bridge listed below;
  and
- the exact AST and continuation macros from `innerLoop` through
  `minPathBody`.

The specialized `snocVS` equations remain definitions because they directly
define the fresh `snocVS` symbol on constructor patterns.  They do not state a
fact about an imported function.

## Domain lemmas

The domain-lemma set is **not empty**.  It contains exactly these seven rules:

- `rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70`:
  guarded length fact for imported `vsLen` on `gridRows`;
- `rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149`:
  guarded imported `valSeqAt` fact selecting a row;
- `rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b`:
  guarded imported `valSeqAt` fact selecting a cell;
- `rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1`:
  guarded imported integer-equality fact connecting `gridAt` with the unique
  `oneRow`/`oneCol` position;
- `rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987`:
  guarded imported integer-order range fact for a valid `gridAt` value;
- `rule-79cc3308597d2aedf94188a46aa45b9302edb4bd5dc309fcd4bc218ec8dc5894`:
  singleton-append fact about imported `valSeqConcat`; and
- `rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348`:
  the additional bridge identity from a specialized `oddDone` term to
  `pairDone`.

The first six are facts about imported operations or hooks rather than
definitions of fresh verification symbols.  The seventh is an extra identity
between result relations already defined by their own base and recursive
equations; it is not itself a defining base or recurrence.  Stage 1 records no
exact rule-absent proof for any of these rules, so each remains in the trusted
domain-lemma set.

## Separately proved derived lemmas

There are **no** canonical inventory rules classified as
`PROVED_DERIVED_LEMMA`.

Stage 1 `prove.sh` separately invokes `kprove` for these reachability claims:

- `inner-one-ahead`, `inner-no-one`, `outer-one-ahead`, `outer-one-past`, and
  `scan-finish` together at depth 240;
- `neighbor-finish` at depth 400; and
- `result-loop-tail` at depth 110.

`PROOF.md` records `#Top` and exit 0 for those commands.  These claims are not
rules in the canonical rule inventory, however, and none is the identical
compiled statement of an installed rule proved against a module from which
that rule was absent.  In particular, the reachability claims include program
configurations and cells, whereas the domain lemmas above are functional
equations or predicate identities.  Thus the Stage 1 claim evidence cannot be
used to classify any inventory rule as a proved derived lemma, including under
the compiled-cell exactness requirement.

The final `minpath-full-contract` command is recorded as exiting nonzero, so it
also supplies no prior exact-rule proof evidence.

## Operational rules

No canonical rule is classified as `OPERATIONAL_RULE`.  The inventory contains
fresh mathematical definitions, proof-domain facts, and macro expansions, but
no ordinary configuration rewrite that adds execution or observation behavior
to the verification model.
