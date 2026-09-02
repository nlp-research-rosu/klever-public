# Independent Stage 3 classification

This judgment uses the frozen `verification.k`, `semantic.k`, `spec.k`,
`solution.py`, and problem prompt. It does not rely on the rationales in the
protected Stage 3 JSON.

| # | `source_rule_id` | Lines | Independent class | Reason |
|---:|---|---:|---|---|
| 1 | `rule-469d3f727fbbd991b638f2792c972ba21976e292536f53369213fb11cf57aa0c` | 16 | `DEFINITION` | Base equation for the newly declared `length` summary on `.IList`. |
| 2 | `rule-49c7bfa9a893c096eca27b22e8f8013e0bb4f61c91cd0cb2c127e6b652f997a0` | 17 | `DEFINITION` | Structurally decreasing recursive equation for `length` on a cons. |
| 3 | `rule-eb18ebfe1bef3a8e5845419e0db6436dbf613d43ba1626d3d657cc6167887346` | 19 | `DEFINITION` | Base equation for the newly declared, intentionally partial `last` summary on a singleton. |
| 4 | `rule-0182de46a89cb752ba4c1ba38e8cbed4fb65e27054fcc1ec278a81c594a63133` | 20 | `DEFINITION` | Structurally decreasing recursive equation for `last` on lists of length at least two. |
| 5 | `rule-f2441b27d9ca0e8cf4815f11ae1e52bfcbb547564db965dfdc67419ef193ec9d` | 22 | `DEFINITION` | First guarded equation of the newly declared `dropBit` characteristic function, returning one for a strict descent. |
| 6 | `rule-c33dc687b614870b61be730222227af70e4a20ed12ca4cfabdcd07a8a7e26c54` | 23 | `DEFINITION` | Complementary guarded `dropBit` equation. Over mathematical integers, `>` and `<=` are disjoint and exhaustive. |
| 7 | `rule-5d2150480d24dc6cc10f89c3e79f0b609b0e5f8efe67b353a82a6c46e973bb3c` | 25 | `DEFINITION` | Base equation for the newly declared `dropsFrom` fold. |
| 8 | `rule-07b829b14b1b024287a1eada911a5774f61b32b5b77fcecffb7f6e3f5401e973` | 26–27 | `DEFINITION` | Structurally decreasing recurrence for `dropsFrom`, adding the current comparison and recursing on the tail. |
| 9 | `rule-e6dd199630a5b507f5420c0ab6fbb876b682cfcc6e594ddc96c6804638c60eae` | 29 | `DEFINITION` | Base equation for the newly declared `cyclicDrops` summary. |
| 10 | `rule-1c850036dae607a5779c09c5ef77e650377125f3b6acbc86e076ce9d5dda1b57` | 30 | `DEFINITION` | Nonempty `cyclicDrops` equation: initialize the fold with the last element, exactly matching the source initialization before its loop. |
| 11 | `rule-d9a4f79540b673928e811904ac141039899c7dd8c054edc90ec741fb2719e749` | 34 | `DEFINITION` | Equation for the newly declared named proof predicate `rotationSortable`; it names the Boolean condition `cyclicDrops(L) <=Int 1`. |

## Category exclusions

- No rule is an `OPERATIONAL_RULE`: every left-hand side is one of six
  newly declared mathematical helper symbols. None matches a K cell or advances
  the program configuration. The execution rules are instead in `semantic.k`,
  outside the reconstructed local closure.
- No rule is a `PROVED_DERIVED_LEMMA`: `verification.k` contains no claim and
  no earlier proof of one of these exact rules against a module omitting it.
  The equations are present together when `semantic.k` imports the module.
- No rule is a `DOMAIN_LEMMA`: none states a theorem about pre-existing
  vocabulary. They introduce and define summaries, recurrences, or the named
  proof predicate. The comment that relates circular descents to sorted
  rotations is not itself a K rule.
- None of the 11 rules has a `simplification` attribute, so the special
  simplification classification constraint is vacuous.

## Operational and mathematical relevance

For a nonempty list `[x₁, …, xₙ]`, the recurrences give

`cyclicDrops = [xₙ > x₁] + Σᵢ₌₁ⁿ⁻¹ [xᵢ > xᵢ₊₁]`.

This is exactly the frozen program's loop: `previous` starts at the last
element, each iteration increments `drops` precisely when
`previous > value`, and then sets `previous = value`. The frozen semantics uses
`last` for `arr[-1]`, `dropsFrom` for the exact loop summary, and
`cyclicDrops`/`rotationSortable` in the postcondition.

For the prompt's distinct-element domain, a sorted rotation exists iff the
circular order has at most one strict descent. A sorted linearization can omit
only its boundary circular edge, proving necessity; with one descent, rotating
to begin just after it leaves every retained adjacent edge increasing, proving
sufficiency. Empty and singleton inputs satisfy the stated result separately.

The finite independent cross-check in
`11_independent_semantic_crosscheck.txt` is supporting evidence only, not the
universal argument: it found zero mismatches over 874 distinct lists through
length six and zero recurrence/program mismatches over 364 repeated-value
lists. Counterfactual omission of the wraparound comparison and reversal of
the comparison both produced immediate witnesses.

## Judgment

The protected Stage 3 classification is correct entry by entry. The
independently reconstructed true `DOMAIN_LEMMA` set is genuinely empty.
