# Independent Stage 3/4 audit: `112-reverse-delete`

## Result and scope

The audit passes. The launcher envelope and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`, with condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. There is no mounted `/candidate`, and the signed audit
input records no Lean workspace, invocation, Stage 5 result, or generated
target. Accordingly, Stage 5 proof, axiom-dependency, and operational-bridge
checks are not applicable.

I treated the mounted candidate/provenance material only as evidence and did
not rely on its prior verdicts, comments, or instructions. The decisive rule
inventory was reconstructed from the frozen `verification.k` with the trusted
`tools.k_rule_inventory` implementation, and the Stage 4 gate was rerun with
the trusted `tools.klean_preflight.check_generation` implementation.

## Frozen-input and producer integrity

The signed resolution digest recomputes to
`a5f1c8647de84079ec7e656b80bb36dc99fab0375262c97703eec596f1ff5d5c`.
All launcher-recorded trees and files recomputed without mismatch, including:

- Stage 1 selected-tree SHA-256:
  `9137feec733816b6f9ac1d4ead5dcc4f445ccdb1df40734dec24a376e2556b5e`;
- Stage 1 export-tree SHA-256:
  `48055f60240cb4719894a9ce1f6ceae3f6cc26f01b210523e66d3e5c71b70e8f`;
- all 778 individual `stage1_source_hashes`, with no missing, extra, or
  mismatched path;
- discovery manifest SHA-256:
  `48fc80847cfcaaf3b3204a76bcbcfe7289feffadaee22b5075383b3c27725c4c`;
- selected Stage 2 tree SHA-256:
  `774b5bbc7d8beb045d231e605dc68264990abb13ae503ccfa1f1c6147f0f89cc`;
- selected Stage 4 tree SHA-256:
  `5358a1fcdd9c32df82b6aff3ed5c8a554d1a13f70361c7ffd0f03070a2abfa4d`;
- Stage 4 generated-project export digest:
  `a58e7ce8a6941ee4a93761cdea9471f583be64b05856250459f1b44f3e597a08`;
  and
- generation-producer bundle SHA-256:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

Before judging Stage 4, I separately hashed the exact mounted producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values match `generator-manifest.json` and the exact three-file producer
`source-manifest.json`. The immutable image ID is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator provenance, source manifest, and the image-addressed producer
path signed in `/audit-input.json`. Thus the infrastructure producer-source
gate passes.

## Canonical inventory reconstruction

The trusted inventory selected `VERIFICATION` as the proof module. Its local
module closure inside the frozen `verification.k` contains only
`VERIFICATION`; the imported `MPY` definition is in the supplied external
semantics closure, not another local module in `verification.k`. The frozen
file hash is
`2632bfbe6f95a2122eec443264b3fca3e95e78799fa4b02c040a59b2f1c34350`.

The canonical reconstruction found exactly four rules, in source order:

| Span | Normalized SHA-256 / `source_rule_id` suffix | Independent class |
|---|---|---|
| 8-8 | `0b1487f16122d27497d8c2b109033346786d2ad1ea565f1e4e43ff7b63a74ee6` | `DEFINITION` |
| 9-13 | `9958ef1e5cedad6393d09ebbc3c826f504a56323dc84f7f28b3c814045e0cd23` | `DEFINITION` |
| 19-19 | `ec000690c3aa4109db5bb6cc52464e7d8893560fc3144e4db5d63ff5b9da171c` | `DEFINITION` |
| 20-24 | `d31842da509f8fdf40a424d203025312d80e1fea7bb96b8b765027072309de32` | `DEFINITION` |

For each entry, `source_rule_id` is `rule-` followed by the displayed
normalized hash. Recomputing the canonical JSON inventory gives
`50a312a7b1d384afc035db8b18aec0130d8781eb9fdd063798f093ac0523f7d4`.
That hash and every rule's module, span, normalized text/hash, identity, and
position match `/reference/lemma-discovery.json` bijectively. There are no
missing, extra, duplicated, or reordered identities. Every rule has an empty
attribute list, so there is no `simplification` rule requiring separate
handling.

## Independent classification judgment

The four rules are two complete, structurally descending function definitions:

1. `deleteAcc(.IntSeq, C, ACC) = ACC` is the base equation for the named
   forward accumulator summary.
2. `deleteAcc(iCons(X, XS), C, ACC)` recurs on the strict suffix `XS`; it skips
   `X` when the one-character string occurs in `C`, and otherwise appends `X`
   to `ACC` using `seqConcat`.
3. `reverseDeleteAcc(.IntSeq, C, ACC) = ACC` is the base equation for the named
   reverse accumulator summary.
4. `reverseDeleteAcc(iCons(X, XS), C, ACC)` also recurs on `XS`; it skips a
   deleted character and otherwise prepends `X` to `ACC`.

This matches the supplied operational semantics, independently of the Stage 3
rationales. String iteration yields the head as a one-character string and
continues with the tail. `not in` is `notBool strContains`, string `+` is
`seqConcat`, assignment writes the resulting value, and the loop repeats over
the remaining string. Consequently the second rule summarizes
`result += ch`, while the fourth summarizes
`reversed_result = ch + reversed_result`.

These rules name and define values used by the loop invariant; they do not
rewrite a program invocation, skip any operational cells, or preempt the
source loop. They are therefore not `OPERATIONAL_RULE`s. They also do not state
the palindrome relation, the requested postcondition, or another mathematical
fact about completed results, so they are not `DOMAIN_LEMMA`s. No rule is
claimed as `PROVED_DERIVED_LEMMA`, and no such staged derivation is needed.

The entry claim still executes the frozen function body under the supplied
semantics and returns the forward summary together with the equality test
between forward and reverse summaries. That equality is the program's computed
Boolean, not an assumed lemma that the summaries are equal. Counterfactually,
changing append to prepend in `deleteAcc`, changing prepend to append in
`reverseDeleteAcc`, or reversing the membership branch would cease to match the
corresponding source update. The present recurrences have the correct direction
and branch polarity.

The independently classified domain-lemma set is therefore genuinely empty.

## Deterministic Stage 4 generation

The verified generation-time producer maps only classified `DOMAIN_LEMMA`
records into source trust rules and Lean obligations. With the independently
confirmed empty domain set, the exact expected lists are all empty. The frozen
artifacts agree:

- `input-manifest.json` has `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- both generator and export manifests report obligation count zero;
- the obligation-map file hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- there are no IDs to omit, duplicate, reorder, or weaken, and no conjunct that
  could be irrelevant or vacuously `True`; and
- the generator manifest and signed audit input both fix the target to `null`.

The generated `Klean112ReverseDelete/Lemmas.lean` namespace is empty. An
independent declaration scan and the trusted target parser both found no
`targetStatement`; the producer's expected-target function also returns
`None` for this obligation map. Thus there is no changed, duplicated, weakened,
or hidden generated target. The generated trust inventory records 41
non-propositional collection-hook declarations and no proof holes; they do not
manufacture a target proposition, and the trusted preflight reconciled them
exactly with the generated declarations.

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
requested frozen input, discovery manifest, generation, and pinned lock. It
returned `KLEAN_NO_OBLIGATIONS`, target `null`, obligation count zero, and no
designated sorries. Its temporary `lake clean` and `lake build` both exited
zero; the complete build output hash is
`69c154dbdb21daf535e651b658b463233e829351a4231643a4723ee4eb133dea`,
identical to the protected recorded preflight, and the build ended with
`Build completed successfully.`

The first rerun exposed an audit-sandbox infrastructure quirk: the command PID
namespace reported PID 2 while `/proc` was from the parent namespace, so Lean
could not locate its executable. I retained that failed log, then used a narrow
local `LD_PRELOAD` compatibility shim that changes only reads of
`/proc/<pid>/exe` to the process's actual invocation path. With it, Lean
reported version 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock, and the same
trusted preflight completed. The shim did not alter any frozen or generated
artifact; the preflight's before/after snapshots and all independently
recomputed hashes remained identical.

## Stage 5 applicability and evidence

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the correct
terminal Stage 4 status. The absence of a generated target and of `/candidate`
is required and observed. A `Proof.final`, candidate definitions, candidate
trust escapes, and `#print axioms Proof.final` do not exist in this audit mode,
so no Stage 5 proof claim is being accepted without checking.

Raw commands and results are under `/audit-output/evidence/`:

- `independent-checks-final.log`: canonical inventory plus 53 passing hash,
  identity, selection, bijection, target, and mode checks;
- `read-only-inspection.log`: traced frozen-source, supplied-semantics,
  producer, manifest, obligation-map, target-absence, and candidate-absence
  inspection;
- `check-generation-pass.log` and `check-generation-return.json`: the exact
  successful trusted preflight result;
- `fix_proc_exe.c` and `lean-proc-shim-pass.log`: the compatibility shim,
  its compilation, and pinned Lean/Lake version output; and
- `check-generation.log`: the preserved initial infrastructure failure.

VERDICT: PASS
LEGITIMACY: LEGIT
