# Independent audit: `7-filter-by-substring`

## Result

The Stage 3 classification, deterministic Stage 4 generation, and Stage 5
Lean proof are legitimate. I reconstructed and reclassified the frozen rule
inventory without relying on the prior classification or review conclusions.
The one genuine domain lemma is present exactly once in the generated
obligation, the generated target is unchanged, and the candidate supplies
operationally honest definitions for both target parameters.

Audit mode was `CLASSIFICATION_AND_PROOF`; the condition was `kit-semantics`
and the semantics mode was `SUPPLIED_SEMANTICS`.

## Producer and input authentication

I hashed the mounted generation-time sources before judging Stage 4:

| Source | Actual SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in `source-manifest.json` and `generator-manifest.json` | match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in `source-manifest.json` and `generator-manifest.json` | match |

The generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
It agrees between the source manifest and generator manifest, and the same
digest is the basename of the generation-producer-source path recorded by
`/audit-input.json`. The mounted producer-source tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly as recorded by the launcher.

I independently recomputed the launcher-bound tree and file hashes. These
include the K workspace
`4247d334d98f7c24b67dd9ce59ba8c0be544897429b8b4e5e3a84e800e3bfcb6`,
the Stage 1 export
`ab03184a1dc4cf9d039f2d1577fe299a98e7857f923621d370f5eb14e4c4c0dc`,
the Stage 2 audit
`4dc3da0f27fcbc9c8a13385605b20046775c1400ba42efc39b237b1a9bf7cb72`,
the discovery manifest
`ff7d79db18ea952e08f0933f163c8000e246bdfcc6aeb93c986e752582840959`,
the Stage 4 generation
`5c1891356052f0af3e2435c84c71022f033f594ec5e5da31333ef65b67d6a4f0`,
the generated tree
`3f21302f11b2328e6d3f9a1abb941e89512a4fdb7b523e96cec2334e5e7f0381`,
and the candidate tree
`855081126d8b3024cf2869dee257f2106fe442064bbfbd76123bda4b218fc956`.
Every individual frozen Stage 1 file path and hash also matched the launcher
record.

Evidence: `evidence/01b-mode-and-producer-authentication.log` and
`evidence/03-integrity-bijection-and-hashes.log`.

## Stage 3 inventory reconstruction

Using the trusted rule-inventory implementation with `/reference/k-proof`, I
resolved the local verification-module closure to exactly `VERIFICATION`.
The frozen `verification.k` SHA-256 is
`2ba333ffd5abb64f71cfbe58089640f1a0d2b6d1102ddfbceada13c1c9f73323`.
The reconstructed ordered inventory contains eight rules and has whole
inventory hash
`2f18e093bb2959170b6ba00673e017fa9cb2ff9e0454b57a271bf5cbda4bf7ce`.

For every rule I independently sliced the recorded source span, normalized it
as whitespace-separated source text, hashed it, and reconstructed
`source_rule_id` as `rule-` plus that hash:

| Span | Reconstructed identity / normalized SHA-256 | Independent class | Reason |
|---|---|---|---|
| 12 | `rule-d4676ce65d5aa71d896650582ea7fd95efd3f817b5b09d834d0ee937362738f4` | `DEFINITION` | `strCodes(str(S)) => S` defines the string projection case. |
| 13 | `rule-847ade70763e1124464b657827fa409b360b4ee6da4959b08c37af4bfcc6ea05` | `DEFINITION` | The `owise` rule completes the total `strCodes` projection on non-strings. |
| 16 | `rule-8f5f9af1fe8efa4c83c0197e4a31cd8150af4cd53c7d3fc694a6fa2796bc0d5a` | `DEFINITION` | Base equation for the proof-domain predicate `allStrVS`. |
| 17–18 | `rule-865c4b24763637b23fa93793d11806aae069dc118aea556597904b6aae56a5ad` | `DEFINITION` | Structural recurrence for `allStrVS` on the sequence tail. |
| 23–26 | `rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503` | `DOMAIN_LEMMA` | Guarded normalization of the pre-existing operational symbol `applyCmp`; it does not define a summary or operation. |
| 31 | `rule-c7e3f2f45bbfd43ef6b8731a4e0c5ffee7b1efe6805f88d96b74e539a66d2e71` | `DEFINITION` | Base equation for the accumulator summary `filterAcc`. |
| 32–39 | `rule-e766fccb4416695974e50ef3cf530b303db323532b6a6987b87d7a5a123c4193` | `DEFINITION` | Include-head recurrence for `filterAcc`, decreasing on the remaining tail. |
| 40–44 | `rule-ad345f4ab95b42abade2e1e581a480d6a8f282ec27387d0fc23704a7aa59979b` | `DEFINITION` | Exclude-head recurrence for `filterAcc`, also decreasing on the tail. |

The independently reconstructed identities, spans, hashes, order, and classes
match `/reference/lemma-discovery.json` bijectively. There are no omissions,
duplicates, extra entries, reordered identities, operational rules, or
proved-derived lemmas.

The rule at lines 23–26 is not a `DEFINITION`: `applyCmp` already belongs to
the supplied language semantics. It is not an `OPERATIONAL_RULE`: ordinary
execution is the frozen MPY-STR rule
`applyCmp("in", str(P), str(X)) => strContains(P, X)`. It is not a
`PROVED_DERIVED_LEMMA`: Stage 1 compiles it into `VERIFICATION` before its
claims and contains no earlier exact proof of that rule against a module from
which it is absent. It is therefore correctly a `DOMAIN_LEMMA`.

That lemma is relevant, not decorative. The source program tests
`substring in string`; the final and loop claims use `filterAcc`, and its
recurrences decide inclusion through `strContains(P, strCodes(V))`. The
lemma connects the operational `applyCmp` term to that projected string
representation under the explicit string-domain guard. Its guard is
satisfiable for every semantic string. The three rules carrying the
`simplification` attribute are this domain lemma and the two defining
`filterAcc` recurrences, so every simplification rule is either a
`DOMAIN_LEMMA` or a `DEFINITION`.

Evidence: `evidence/02-trusted-rule-inventory.log`,
`evidence/03-integrity-bijection-and-hashes.log`, and the independent checker
source `evidence/check_integrity.py`.

## Stage 4 generation and obligation judgment

The genuine domain set is nonempty and contains exactly the line 23–26 rule.
Accordingly the selected status is correctly a normal successful generation
with one obligation, not `KLEAN_NO_OBLIGATIONS`.

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
three required paths, and the trusted toolchain lock. It returned `PASS`,
one obligation, zero designated sorries, and 42 recorded trust declarations.
The rerun rebuilt the generated project successfully.

The source-rule/obligation mapping is exactly one-to-one:

- source:
  `rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503`,
  span 23–26, normalized hash
  `ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503`;
- generated conjunct hash:
  `7b060dcdc8e6fd11130afc59519b58d4ac2c75d77000611a0149c94ecaa96e64`;
- obligation-map hash:
  `7c3cf138a9b4a9a7078a5f42a0421155323947814de8cc8b21ceaf47d7394c0b`.

Mathematically, the conjunct preserves all of the frozen K rule: arbitrary
`V : SortVal` and pattern `P : SortIntSeq`, the exact guard that injected
`V` equals the injected string `str(strCodes(V))`, and equality between the
two exact `applyCmp("in", str(P), ...)` terms. It introduces no additional
premise, discards no premise or operand, and changes neither operator nor
result. There is one source rule, one conjunct, and no duplicate or extra
conjunct. The premise is satisfiable, so this is not a vacuous implication.

The fixed target is:

- declaration: `Klean7FilterBySubstring.Lemmas.targetStatement`;
- definition hash:
  `115c77a0eb3b90c59d66743add4adc358edc5886941deb7d2973a884089843f0`;
- statement hash:
  `2b56a8d0bddfa74273e8470c55d381f2f45f830b040712bf851cec09044cca77`;
- generated tree hash:
  `3f21302f11b2328e6d3f9a1abb941e89512a4fdb7b523e96cec2334e5e7f0381`.

These values agree among the freshly extracted generated declaration,
generator manifest, obligation map, rerun preflight result, and
`/audit-input.json`.

Evidence: `evidence/12-rerun-check-generation-with-sandbox-shim.log`,
`evidence/03-integrity-bijection-and-hashes.log`, and
`evidence/16-candidate-target-and-source-integrity.log`.

## Stage 5 proof identity and trust accounting

I created `/tmp/audit-work/stage5-fresh-001`, copied the candidate proof
workspace there, replaced its `Base` with an exact copy of
`/reference/klean-generation/generated`, and ran both `lake clean` and
`lake build`. Both commands exited 0. After the build, the fresh `Base` hash
was still exactly
`3f21302f11b2328e6d3f9a1abb941e89512a4fdb7b523e96cec2334e5e7f0381`.
The copied `Proof.lean` hash
`fa6682a0c0ba9b78c559db75de4c8ddc94ae21c6bd0da51aec2565d43c4c5185`
equals the mounted candidate source hash.

An independent source scan and the trusted final candidate gate found:

- exactly one definition for each required target binding;
- exactly one theorem `Proof.final`;
- no candidate declaration or namespace that changes or shadows
  `targetStatement`;
- no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`;
- an exact theorem type equal to the fixed generated target, rather than a
  copied, weakened, or alternative proposition.

Lean's exact `#print axioms Proof.final` result was:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

The trust inventory records 42 generated trust-boundary axioms. None occurs
in the dependency result. The trusted final-gate policy explicitly adds the
three standard Lean foundational dependencies shown above to that inventory
allowlist. Thus every printed dependency is accounted for, while `sorryAx`
and every unrecorded or generated proof escape are absent. The trusted
mechanical final gate independently returned `PASS`.

Evidence: `evidence/13-stage5-fresh-lake-clean-build.log`,
`evidence/14-axioms-and-bridge-adversarial.log`,
`evidence/15-trusted-final-gate.log`, and
`evidence/16-candidate-target-and-source-integrity.log`.

## Operational bridge audit

The generated equation is a guarded congruence and cannot by itself force
honest implementations: as a counterfactual check, I defined both target
parameters as constants and Lean still proved the fixed equation. I then
showed that constant `applyCmp` disagrees with the required positive
substring case and constant `strCodes` disagrees with a nonempty string.
This confirms that the following independent parameter audit is necessary;
it is not inferred from the successful theorem.

### `strCodes`

The candidate's exact definition returns the stored `IntSeq` for
`SortVal.inj_SortStr (str codes)` and `.IntSeq` for every other `SortVal`
constructor. This is precisely the pair of frozen definition rules at
verification lines 12–13, including the `owise` non-string behavior. It is
neither constant nor identity-like. Lean checks on a nonempty string and an
integer value reduced to the required results.

### `applyCmp`

The bound KORE symbol is the supplied MPY-CORE `applyCmp` function. On the
domain used by the source rule and target—operator `"in"`, string left
operand, and a right operand made a string by the guard—the candidate matches
the exact string branch and calls `intSeqContains pattern text`.

The frozen K semantics defines `strPrefix` by empty/nonempty constructor
cases and pointwise head equality, then defines `strContains` as success on a
prefix or recursion on the text tail. Candidate `intSeqPrefix` is the same
constructor recurrence. Candidate `intSeqContains` tests that prefix at the
current suffix and otherwise recurses on the tail, which is extensionally the
same operational meaning. This also matches the source program's Python
condition `substring in string`.

I compiled kernel-reduced Lean checks for:

- empty pattern in empty text: true;
- empty pattern in nonempty text: true;
- a one-code suffix match: true;
- a pattern longer than the text: false;
- a middle contiguous match: true;
- a same-prefix mismatch: false;
- `strCodes` round-trip on a nonempty string;
- `strCodes` fallback on a non-string;
- explicit disagreement between the honest definitions and the deliberately
  constant counterfactuals.

All checks passed. The candidate bridge definitions implement the frozen
operational meaning on the entire domain relevant to the fixed rule; there
is no constant, hard-coded, vacuous, or convenient bridge substitution.

Evidence: `evidence/14b-bridge-adversarial-rerun.log` and
`evidence/17-operational-bridge-source-and-tests.log`.

## Toolchain note

The audit sandbox exposes a host-PID `/proc` mount while Lean 4.22 asks for
`/proc/<namespace-pid>/exe`; the initial direct invocation therefore could
not locate its own installation. I used a minimal local compatibility shim
that redirects only numeric `/proc/.../exe` `readlink` calls to
`/proc/self/exe`. It does not alter candidate or generated source, Lean
elaboration, kernel checking, or proof dependencies. With it, the pinned
toolchain identified itself as Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0, exactly matching
the lock and manifest. Full shim source, hashes, diagnosis, and smoke output
are in `evidence/18-sandbox-toolchain-compatibility.log`.

## Conclusion

All authenticated structural checks and independent mathematical checks
agree. Stage 3 has seven definitions and one relevant domain lemma. Stage 4
generates exactly that lemma with an unchanged target. Stage 5 proves exactly
the target with fully accounted trust dependencies and honest operational
bindings.

VERDICT: PASS
LEGITIMACY: LEGIT
