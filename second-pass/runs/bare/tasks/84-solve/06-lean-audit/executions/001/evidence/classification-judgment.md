# Independent rule-by-rule classification

The canonical local closure is only module `VERIFICATION`. Its 13 rules are
classified below from the frozen rule text, the declarations at
`verification.k:7-17`, the execution definitions in `semantic.k:23-89`, and
the Stage 1 claims in `spec.k`. No prior classification rationale was used as
the basis of the judgment.

| Lines | `source_rule_id` | Judgment | Independent reason |
|---:|---|---|---|
| 18-67 | `rule-53df571852c7260b5405e3f430a1e197cea8bc915573926401bb413440ff9dbd` | `DEFINITION` | This is the sole equation for the declared `solutionProgram` macro. It names the source program's constructor tree. Fresh `kast` outputs for `solution.mpy` and expanded `solutionProgram` were byte-identical. |
| 69-70 | `rule-611eff644e7463953f9e3303994ad536c6d7af8ffc37dbee9f4547f5b2ee3f78` | `DEFINITION` | Base equation for the declared digit-sum summary `oracleDigitSum` on `0 <= N < 10`. It defines the summary rather than asserting a fact about a separately defined symbol. |
| 71-72 | `rule-6218849d083de77765852fa3fe298f64fdf2bfd9311e3d0062c42d730007fd1d` | `DEFINITION` | Descending recurrence for the same summary on `N >= 10`; division by 10 decreases nonnegative inputs in this guard. |
| 74 | `rule-ebae8e4ed50af4d120453d2fe890f9016636d08ca01623aea8e7d1b4abc35258` | `DEFINITION` | Zero base equation for the declared binary-string summary. |
| 75-76 | `rule-dc16181ae61d3a6d0e550918248fc54a1063df4d3cef4f78b5bc3441607af695` | `DEFINITION` | Positive-case dispatch equation defining `oracleBinary` in terms of its positive recurrence. |
| 77 | `rule-210e1de7ac4c4d3ce648ab492751173244b1780ff5a6079d020c6f08a3caa079` | `DEFINITION` | Base equation defining the positive binary recurrence at one. |
| 78-80 | `rule-8a06509279c320d36822dfc724d403f7420b3e96b713ab6bc415d5f382c868e8` | `DEFINITION` | Descending quotient-by-two recurrence defining `oracleBinaryPositive`; the remainder is in the domain of the two `appendOracleBit` equations. |
| 81 | `rule-fd6e492c3ce6cccc19a388a48110eada54f8ec3873eefcbee35ad3749408e406` | `DEFINITION` | Constructor/helper equation defining how a zero bit is appended. |
| 82 | `rule-a96d6b217cafcd09542501da8bb099ff5354be745cece943378f2234c10481f0` | `DEFINITION` | Constructor/helper equation defining how a one bit is appended. |
| 84 | `rule-35401f91dcb79fd77f091e4a9ceebbbdd8a933c147da98e3d56a7ca84fb8bf65` | `DEFINITION` | Equation for the declared proof helper `sameValue`; it defines the Boolean observation on the `VStr` constructor. It is not a rule of the source-language execution relation. |
| 85-86 | `rule-4be79ef929afae60de4bcb6a9f2350cb51af72c71637cec8e25e20ce6220a110` | `DEFINITION` | Equation defining the named per-input proof term. Its RHS invokes `runProgram`; it does not replace or shortcut `runProgram` or any source execution rule. |
| 87 | `rule-14c68d306becb13e6832dc81bbef1f0d797be29f9de2a8958be6a76e6b91b25b` | `DEFINITION` | Base equation for the named half-open range proof term. |
| 88-89 | `rule-8dbb48e717faaf83c06d57955b3cfbf6ad8a0559ad53f25651556f98ea091014` | `DEFINITION` | Recurrence defining that proof term as the current check conjoined with the remainder of the range. |

Consequences:

- `DEFINITION`: 13.
- `OPERATIONAL_RULE`: 0. None of the rules has an execution-configuration
  LHS, defines `evalExpr`/`runProgram`, or preempts source-language execution.
- `PROVED_DERIVED_LEMMA`: 0. No rule is introduced through an earlier proof
  against a module omitting that rule and then consumed later.
- `DOMAIN_LEMMA`: 0. Each rule defines its LHS head symbol; none states an
  independent arithmetic/string theorem.
- Textual `simplification` attributes: 0, as reconstructed by the canonical
  inventory. The simplification-class restriction is therefore vacuous.

This is a genuinely empty domain-lemma set. The Stage 1 reachability claims in
`spec.k` are proof goals, not rules in the local `verification.k` inventory.
