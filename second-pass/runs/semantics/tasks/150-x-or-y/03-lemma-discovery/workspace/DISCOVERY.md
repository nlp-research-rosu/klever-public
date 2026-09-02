# Trust-boundary discovery

The canonical inventory has SHA-256
`702eb4a32ed254d180b4a3daaa572ca6ea99647abaa08d1d125856029ecfd0ef`
and contains 11 rules. Every inventory entry is classified exactly once and
in canonical order in `trust-boundary.json`.

## Classification summary

- `DEFINITION`: 10 rules
- `OPERATIONAL_RULE`: 0 rules
- `PROVED_DERIVED_LEMMA`: 1 rule
- `DOMAIN_LEMMA`: 0 rules

The first three definitions expand the named program and call-harness macros:
`xOrYLoopBody`, `xOrYBody`, and `#xOrY`. The four `primeSelect` rules define
the mathematical trial-division summary by disjoint base, success, divisor,
and recursive cases. The three `scanLast` rules define the structural helper
that tracks the final value of the mutable `divisor` local. These are
equations, recurrences, or macro expansions, so they are definitions rather
than extra facts or operational extensions.

## Separately proved derived lemma

The sole proved derived lemma is:

`rule-9a422e1a1ab7385500d096a89793812db519cc1b6c12a2343c21aecc82c89c8d`

The Stage 1 evidence establishes the required ordering and correspondence:

1. `spec.k` labels the exact same loop-summary configuration transition and
   precondition as `loop_correct` in `X-OR-Y-LOOP-SPEC`.
2. The first symbolic definition built by `prove.sh` has main module
   `X-OR-Y-VERIFICATION`. That base module does not import
   `X-OR-Y-SUMMARY`, so the reusable summary rule is absent from the module
   against which `loop_correct` is proved.
3. `prove.sh` then runs `kprove` for `loop_correct`.
4. Only after that proof does `prove.sh` compile `X-OR-Y-SUMMARY`, where the
   corresponding rule appears, and use it for the separate `main_correct`
   proof.

The rule's `priority(40)` attribute controls reuse ordering in the summary
module; the configuration transition, state updates, and precondition match
the previously proved claim.

## Domain lemmas and simplification rules

The domain-lemma set is empty. No canonical inventory rule supplies an
additional trusted mathematical fact, and no inventory rule carries the
`simplification` attribute.
