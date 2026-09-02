# Independent rule classification and operational bridge audit

## Frozen local inventory

The trusted inventory selected `VERIFICATION`, and its local import closure
within `verification.k` is exactly `["VERIFICATION"]`. It reconstructed five
ordered rules. The canonical inventory hash is
`7233706d0dbd7e2e45da849c5e062cddaa080936fac4c6aafcc0fe447030d1c2`.
Exact spans and texts are in `rule-inventory.json`.

| Rule suffix | Span | Independent class | Reason |
|---|---:|---|---|
| `a2a0…f1ff` | 9 | `DEFINITION` | Base equation for the new named `decimalDigit` summary. It names `pyMod(N,10)` and does not replace source execution. |
| `23f8…d85` | 10–12 | `DEFINITION` | Guarded higher-place equation for the same summary. Every source use has `N≥0` and `P∈{10,100,1000,10000}`, inside the guard. |
| `979a…87b` | 16–22 | `DEFINITION` | Bounded five-place recurrence/summary. The five terms are exactly the source expression and cover `0..10000`, including the fifth place at `10000`. |
| `0ff7…61e` | 26 | `DEFINITION` | Names the prefix-free `binCodes` string used in the postcondition. |
| `a850…370` | 31–38 | `DOMAIN_LEMMA` | Added universal prefix-slice identity. It is not an ordinary rule from the supplied semantics, and Stage 1 did not first prove it in a module omitting it. It is directly relevant to `bin(digit_sum)[2:]`. |

There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. None of the
five rules has a `simplification` attribute, so the simplification restriction
is satisfied. `priority(40)` on the domain lemma is not `simplification`.

The Stage 3 manifest has those five identities once each and in that exact
order, with four definitions and the one domain lemma above. There are no
omissions, duplicates, additions, reordered identities, or altered hashes.

## Mathematical relevance and truth of the domain lemma

The frozen source returns `bin(digit_sum)[2:]`. The supplied semantics rule in
`builtins.k` maps nonnegative `bin(N)` to the IntSeq prefix
`iCons(48,iCons(98,binCodes(N)))`. The source digit sum is nonnegative on the
claimed `0≤N≤10000` domain. The supplied `subscript.k` semantics evaluates a
slice through `#evalB`, `slStart`, `slStop`, `slStep`, `doSlice`, and `buildIS`.
With start `2`, no upper bound, no step, and a finite two-element prefix:

- `slStart=2`;
- `slStop=isLen(prefix++REST)`;
- `slStep=1`; and
- `buildIS` visits exactly the indices occupied by `REST`.

Thus the result is `str(REST)` for every finite `REST`. The rule preserves the
arbitrary continuation and all other configuration cells.

The fixed target is not reflexive or vacuous: its LHS and RHS differ, and the
generated `Rewrites` relation has transitivity but no reflexivity constructor.
The generated `Rewrite.lean` does not contain the domain lemma as a constructor.
The candidate proof uses only the ordinary supplied-semantics constructors:

1. `_1a401d8` starts slice evaluation;
2. `_1fe7f3b`, `_665cd53`, `_a1c192d` evaluate `Int(2)` to `someB(2)`;
3. `_c094fe7`, `_bb17cff`, `_04d5465`, `_bb17cff` evaluate the absent bounds;
4. `_7e6f52e` applies the supplied `doSlice` rule after proving its exact value.

The final value proof structurally inducts over every `REST`. The generated
private model used by the candidate matches the frozen `isLen`, `intSeqAt`,
positive/negative continuation guard, recursive `buildIS`, `slStart`,
`slStop`, and `slStep` rules on this complete target domain. Fuel is
`isLen(input)+1`; for the target's positive unit step every recursive lookup is
in-bounds and recursion terminates exactly at the stop index.

The candidate does not supply a convenient bridge definition. The generated
target has `parameters: []`, so the requested per-parameter `def`/`kore_symbol`
audit has an empty domain. The only candidate `def` used in the value argument
is a normal structurally recursive `append`; the candidate otherwise refers
to the immutable generated models and proves the connection.

Adversarial evidence:

- the universal proof instantiates successfully with tail `[-7,100000]`,
  showing that it does not hard-code character-like tails;
- replacing the result with the empty sequence is rejected for arbitrary
  `REST`; and
- mutating the slice start from `2` to `1` is rejected.

The all-input finite-domain cross-check compares the frozen source formula
with independently implemented decimal-sum and binary conversion oracles for
all 10,001 inputs. It has zero mismatches. Omitting the `10000` place fails at
`N=10000`, and slicing from `1` fails at `N=147`.
