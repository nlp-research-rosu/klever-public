# Trust-boundary classification

The canonical inventory has schema version 2, inventory hash
`3d01d1f5125fc451e01e2c1d535329fec6ae9582a016e32d5fc1455e7812226c`,
and nine rules. All nine rules are classified as `DEFINITION`.

## Definitions

The rules form six named mathematical summaries and predicates:

- `decodeCode` defines the inverse Caesar shift for one lowercase character
  code.
- The base and recursive `decodeSpec` rules lift `decodeCode` to an inductive
  character sequence.
- `encodeCode` defines the prompt's forward Caesar shift for one lowercase
  character code.
- The base and recursive `encodeSpec` rules lift `encodeCode` to an inductive
  character sequence.
- `isLowerCode` defines the lowercase ASCII-code range.
- The base and recursive `allLower` rules define the lowercase-domain predicate
  over an inductive character sequence.

These are equations and structural recurrences defining the verification
model's named summaries. None states an additional fact beyond those
definitions.

## Other classifications

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
execution rules in `semantic.k` are outside the inventory's local
verification-module closure and therefore were not added or classified.

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` runs one
aggregate `kprove` command over `spec.k`, whose labeled claims are
`code-inverse`, `loop-correct`, and `program-correct`. Those claims are not
rules in the canonical inventory, and the mounted evidence does not show any
inventory rule first proved against a module that omitted it and then reused
with exact correspondence. Thus there are no separately proved derived lemmas
to identify.

The `DOMAIN_LEMMA` set is explicitly empty: none of the nine inventoried rules
is an additional trusted mathematical fact used to close the proof.
