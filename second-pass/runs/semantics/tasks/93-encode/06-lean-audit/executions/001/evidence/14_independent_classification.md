# Independent Stage 3 classification

Frozen source: `/reference/k-proof/verification.k`

Selected local verification module: `ENCODE-VERIFICATION`

Local module closure reconstructed by the trusted inventory code:
`["ENCODE-VERIFICATION"]`. The imported `MPY` module is supplied from the
required external semantics and is not a module declared locally in
`verification.k`.

The canonical inventory contains eight rules, in source order. Its canonical
JSON SHA-256 is
`e3cb1460d02952d9116b4f977842c33b5a5399e664b221ce7f280b6e21020025`.
No rule has a `simplification` attribute.

| Source span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 9–45 | `rule-4f1c1b8a406c0f6cf8b5d127a3dc79e4ddbab158f74aa40cbbd60e54aa68f543` | `DEFINITION` | Expands the named `encodeLoopBody` AST term. It is a macro/named proof term, not a proposition about pre-existing functions and not a configuration rewrite. The expansion matches `solution.mpy` lines 7–25, including call arguments, vowel order, both assignments, and both branches. |
| 48–55 | `rule-fe7cc44ef102427686a96c04572b5ba2207f321d0a51c6a392c8df26f885f857` | `DEFINITION` | Expands the named `encodeFunctionBody` AST term to the initialization, exact named loop body, and return. It matches `solution.mpy` lines 3–26. |
| 60–64 | `rule-c967809d7c1f7190c8ad73e7c196724ba72b22ff8161f4b280ffeb5eec91a81e` | `DEFINITION` | Defines the Boolean summary `isVowelCode` as membership in exactly the ten ASCII vowel code points. It is used by the `encodeCode` case definition. |
| 67–68 | `rule-cff78f2fb920faa6ccb5cd7dc82e6fc6fef2f2b8add70a8501a76838d75b7bff` | `DEFINITION` | First guarded case of the mathematical summary `encodeCode`: swap the input code and add two exactly when the swapped code is a vowel. |
| 69–70 | `rule-e36d9423613e355c95d43fc7e640d283a0f29febbbaf355149ebefac14af8c37` | `DEFINITION` | Complementary guarded case of `encodeCode`: return the swapped code when it is not a vowel. The two Boolean guards are exhaustive and disjoint. |
| 75 | `rule-6f211f83fd1f1b067ef8044b1b3525bab51c6d295ab7ac66fe5024ea27fb9d59` | `DEFINITION` | Empty-input base equation of the `encodeAcc` recurrence. |
| 76–79 | `rule-1a15858c13e575c194c98f523a18428daa99bf08a7d7f9756b8ffe6ea2e12371` | `DEFINITION` | Nonempty-input recurrence for `encodeAcc`; it appends the encoded head to the accumulator and structurally descends to `REST`. It is disjoint from the empty case. |
| 82 | `rule-34c2691cb0a6fbd3e7ddcc90c14b933007085cabf3ad29d27766ad1f2943c4cf` | `DEFINITION` | Wrapper definition `encodeCodes(INPUT) = encodeAcc(INPUT, .IntSeq)`. |

## Operational-semantics cross-check

The supplied semantics makes the source/summary connection transparent:

- String iteration yields singleton strings from left to right
  (`str.k` lines 8–10), and `For` binds each yielded value, executes the body,
  and recurs on the remaining iterator (`controls.k` lines 69–74).
- `swapcase` maps `swapC` over string codes (`methods.k` lines 21 and
  162–164). `swapC` adds 32 to ASCII uppercase, subtracts 32 from ASCII
  lowercase, and leaves other integers unchanged (`methods.k` lines 149–152).
- `ord` returns the code of a singleton string, while `chr` creates a singleton
  string for an ASCII code (`builtins.k` lines 143–145). The only path using
  `chr` is a post-swap ASCII vowel plus two, so the result remains in its
  `0 <= I < 128` guard.
- String concatenation is left-to-right `seqConcat` (`str.k` lines 20–24).
  Thus the accumulator recurrence mirrors the operational `result += ...`.

Boundary examples distinguish the summary from convenient mutations:

- `97` (`a`) swaps to `65` (`A`) and advances to `67` (`C`).
- `65` (`A`) swaps to `97` (`a`) and advances to `99` (`c`).
- `121` (`y`) swaps to `89` (`Y`) without advancing.
- `89` (`Y`) swaps to `121` (`y`) without advancing.
- A non-letter code remains unchanged.
- On a two-element input, replacing append by prepend would reverse output
  order and disagree with the operational loop.

These rules are all relevant: the two macros are the exact function/loop terms
used by the claims, and the four summary symbols form the dependency chain
from the loop result to the postcondition. None is an ordinary operational
execution/observation rule, none states a derived proposition about existing
symbols, and none is a standalone domain lemma. Therefore the independently
determined true `DOMAIN_LEMMA` set is genuinely empty.

Independent counts:

- `DEFINITION`: 8
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
