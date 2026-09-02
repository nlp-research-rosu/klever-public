# Independent audit: HumanEval `64-vowels-count`

Audit mode: `CLASSIFICATION_ONLY`  
Condition: `bare`  
Semantics mode: `GENERATED_SEMANTICS`

## Conclusion

The protected Stage 3 classification is correct. The frozen local
verification-module closure contains exactly four rules, and each is a
`DEFINITION` of the recursive mathematical summary `#vowels`. There are no
`DOMAIN_LEMMA` rules. Consequently the deterministic Stage 4 result
`KLEAN_NO_OBLIGATIONS` is mathematically and structurally correct: its source
set, obligation set, and trust-parameter set are all empty, it generates no
target proposition, and Stage 5 is absent.

I did not rely on the selected Stage 2 opinion or any earlier `PASS` or
classification. I read candidate and provenance material only as untrusted
evidence and ran only the trusted `/reference/tools` checkers plus audit-local
checking code.

## Input and producer authentication

The launcher envelope has schema version 4 and its canonical resolution digest
recomputes to
`d37be862b90b4efdf6641e5bdf0cef001a35ee8d75c1df0d2b08c4a3b2dec23e`.
`AUDIT_MODE` and the signed resolution both say `CLASSIFICATION_ONLY`.
`/candidate` is absent, and all Lean workspace, invocation, and Stage 5 result
fields are null.

Before judging Stage 4, I directly hashed the two mounted generation-time
producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both hashes exactly match `generator-manifest.json` and
`source-manifest.json`. The generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the generator manifest and source manifest; the same digest is the
launcher-recorded producer-bundle path component. The bundle contains exactly
the two producer files and its source manifest. Its recomputed tree hash
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`
matches `/audit-input.json`.

All other signed hashes also recompute exactly:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 3 discovery manifest | `f4ed30c257600440c7129e04af73650162ed2d1a2e7e491f9e5db4489821ce13` |
| Generated project tree | `7aa32de8fde92d3c9c93a442f6895193cdc6f11b60e4339247ed0ddecab64f4e` |
| Selected Stage 2 audit tree | `3a6dc796eb35fbfbe47510b268ca071ff9b8d580355af8bfa00769ce27ede41d` |
| Stage 1 pipeline tree | `0dc797314c51f77dc9e58b6ca2caf814da52cd09fd680abe9e032fde3cd722c0` |
| Selected Stage 4 generation tree | `adb851ba3493dedef3709728383c3b4daa1f9100f0079012e9f5b02c430dc9ea` |
| Stage 1 deterministic-export tree | `ec6c124d6422a5d9b579e570a2fa37c7348c40bfc37b066f14c7788d10b4d991` |

The complete Stage 1 per-file key set and every per-file hash match the signed
launcher map with no missing or extra files. Selection hashes, generator
provenance hashes, the generated-tree hash, the frozen toolchain lock, the
recorded preflight object, and the null target all match as well. See
`evidence/04_hashes_and_producer_authentication.txt`.

## Rule-inventory reconstruction

I reconstructed the inventory from the frozen
`/reference/k-proof/verification.k` with the trusted
`tools.k_rule_inventory.inventory_verification` implementation. The selected
module is `VERIFICATION`; its local in-file closure is exactly
`["VERIFICATION"]`. `SEMANTIC` is an imported frozen module in `semantic.k`,
not a proof-local module defined in `verification.k`, so its operational rules
are not incorrectly added to this local classification inventory.

The source file hash is
`16f06c240f03447c209f0b63398b17ce859e2a97e8776bffe09bf10c39be98de`.
For every reconstructed rule I independently sliced the recorded physical
source span, normalized whitespace, recomputed SHA-256, rebuilt
`source_rule_id` as `rule-<normalized-sha256>`, and recomputed the canonical
whole-inventory hash.

| Span | Source rule ID / normalized SHA-256 | Independent class |
|---|---|---|
| 11–11 | `rule-446e7a734fabed5a2e572668cda7855a61d25da12a442b82a62f647c84f77bd3` | `DEFINITION` |
| 13–16 | `rule-978c7862f1563f18c6de2c29b31592e2015d58e41236161ec41227b34122fc54` | `DEFINITION` |
| 18–22 | `rule-fff7ec9596c3f8bfea2b8032980d90cb281da9e279b32474488f5f03c5c489f7` | `DEFINITION` |
| 24–29 | `rule-b63a26b5a4b87f3f77a92f06b896b36655a9114c01cfdee89d791439a893db9e` | `DEFINITION` |

The whole-inventory hash is
`890e46f90e901fe9209ae52b57475bbf1dac09c368d55d42f5bb95ad17f0cf57`.
All spans, normalized hashes, rule IDs, and that inventory hash match the
protected manifest. The manifest contains exactly four unique identities in
the exact canonical order. Thus there is no omission, duplicate, extra rule,
reordering, changed hash, or unaccounted classification. The detailed
reconstruction is in `evidence/03_inventory_reconstruction.txt`.

## Independent classification judgment

`verification.k` declares `#vowels(String)` as a total function immediately
before these four equations. The equations define:

1. the empty-string base value;
2. the recurrence adding one when the head is one of
   `a/e/i/o/u/A/E/I/O/U`;
3. the terminal `y/Y` value when the sole remaining character is `y` or `Y`;
4. the recurrence dropping a non-contributing head in every remaining case.

These are definitions of a named recursive summary, not ordinary execution
rules, derived facts, or domain lemmas. Their guards partition the string
domain: empty versus nonempty; on nonempty strings, ordinary vowel versus
non-vowel; and within the latter, terminal `y/Y` versus the complementary
fallback. The recursive branches call `#vowels` on the one-character-shorter
suffix. The branches are disjoint, cover every string, and descend.

This recurrence is relevant and exact for both the source program and the
postcondition. The operational semantics defines `#isVowelChar` for exactly
the ten ordinary-vowel characters and `#isYChar` for exactly `y/Y`; its
substring rules implement `s[0]` and `s[1:]`. The frozen program tests the
same four cases and the Stage 1 claim relates its return to `#vowels(S)`.
Thus these rules name the mathematical result the operational proof uses;
they do not preempt execution.

No rule claims `PROVED_DERIVED_LEMMA`, so there is no absent earlier derivation
to excuse. None of the four has a `simplification` attribute; in any event,
every entry is in the allowed `DEFINITION` class. The independently classified
domain-lemma set is genuinely empty.

As finite adversarial support, an independent direct contract oracle and the
frozen recurrence agreed on all 299,593 strings of lengths 0 through 6 over
`aAeEyYbz`. Counterfactuals that count `y` everywhere or omit terminal `y`
were separated by witnesses such as `yy`, `yby`, `rhythm`, `y`, and `ay`.
This testing supports, but does not replace, the source-and-semantics analysis.
See `evidence/12_semantic_relevance_and_mutations.txt`.

## Stage 4 generation, bijection, and target identity

I reran the required trusted call:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The first run exposed a sandbox/toolchain issue before any project code ran:
Lean uses `readlink("/proc/<namespace-pid>/exe", ...)`, while this audit
sandbox exposes the executable through `/proc/self/exe`. I preserved that
failure and the diagnosis. I then compiled a narrow audit-local preload shim
which changes only such `/proc/<pid>/exe` reads to `/proc/self/exe`.
With that compatibility shim, the same trusted checker returned
`KLEAN_NO_OBLIGATIONS`; `lake clean` and `lake build` both exited 0. The build
output hash
`6938fcec97a02999b2814878a352c40d09e6d15c8337eeb4a47bf943c6458a99`
and complete returned diagnostic object exactly match the recorded preflight.
The shim source, its hash, failed attempts, and successful output are preserved
under `evidence/05_*` through `evidence/10_*`.

Independent of the checker, `generated/obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Its SHA-256 matches
`generator-manifest.json.obligation_map_sha256`. The independently classified
domain ID sequence is also empty, so the source-rule/obligation comparison is
an exact bijection `[] ↔ []`, not an omission. Every manifest and preflight
obligation count is zero, every relevant status is
`KLEAN_NO_OBLIGATIONS`, and no vacuous conjunct exists because no conjunct or
proposition was emitted.

The trusted target extractor returns null; the expected target definition is
null; the generator manifest, recorded preflight, and audit input all record a
null target. `Lemmas.lean` contains only an empty namespace, and a scan of all
generated Lean sources finds no target, obligation, domain-lemma, or final
declaration. Therefore there is no changed, weakened, duplicated, or vacuous
target. The fixed generated target for this valid zero-domain case is precisely
the absence of a target.

## Stage 5

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. This is the
required mode for a genuine `KLEAN_NO_OBLIGATIONS` result. There is no generated
target to prove, `/candidate` is absent, and the launcher records no Lean
workspace, Lean invocation, or Stage 5 result. Therefore no clean candidate
copy, `Proof.final`, axiom printout, target parameter, or operational-bridge
definition exists to audit.

## Evidence index

`evidence/COMMANDS.md` records the commands and points to their complete
results. The key artifacts are:

- `03_inventory_reconstruction.txt`
- `04_hashes_and_producer_authentication.txt`
- `10_successful_rerun_check_generation.txt`
- `11_obligation_map_and_target_absence.txt`
- `12_semantic_relevance_and_mutations.txt`
- `13_trusted_stage3_boundary_validation.txt`
- `14_independent_stage4_zero_obligation_check.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
