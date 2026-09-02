# Independent Stage 3–5 Audit

## Scope and audit mode

This audit covers HumanEval `16-count-distinct-characters`, condition
`kit-semantics`, with `SUPPLIED_SEMANTICS`.

The live environment and `/audit-input.json` independently report
`CLASSIFICATION_ONLY`. `/candidate` is absent. The launcher-recorded Lean
invocation and Lean workspace hashes are both `null`, consistent with this
mode. Consequently, the Stage 5 `Base` copy, candidate clean build,
`#print axioms Proof.final`, proof-identity checks, and parameter operational
bridges are not applicable.

I treated the Stage 1 workspace, selected Stage 2 review, Stage 3 manifest,
Stage 4 generation, prior logs, and comments as untrusted evidence. I did not
adopt any prior classification or verdict. Reconstruction and mechanical
checks used the trusted code under `/reference/tools` with
`PYTHONPATH=/reference`.

## Producer-source infrastructure gate

I checked the generation-time producer sources before judging Stage 4.

| Binding | Recomputed value | Recorded value(s) | Result |
|---|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in `source-manifest.json` and `generator-manifest.json` | match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in `source-manifest.json` and `generator-manifest.json` | match |
| producer tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | same in `/audit-input.json` | match |
| generator image | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` | same in `source-manifest.json`, `generator-manifest.json`, and the audit-input producer-path binding | match |

There is no producer-source mismatch and therefore no infrastructure
`AUDIT_ERROR`.

## Frozen-input and provenance hashes

All non-null resolution hashes recomputed to their launcher-recorded values:

| Artifact | Recomputed and expected SHA-256 |
|---|---|
| protected Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 1 workspace, pipeline tree hash | `349f2b23a3e3e16a757f53cc73dfed7f2b0914ad2d803b9381b03b4f33eab46a` |
| Stage 1 frozen export, Klean tree hash | `f0d01b4844acc04f59f408c7bb9de48af59bbbd1ac0c52b85ac23b40e10ca168` |
| selected Stage 2 audit tree | `bc314fd9fa694edc6afabceb28f49bdb1a616aa2fa1a655252ec945e4b6f8116` |
| selected Stage 4 generation tree | `ba581ef0c7c14b3c40a4e328536ba018b11bf26b2b9c096a530367dc83ae3128` |
| generated Lean project | `ad6a569222e70857c263c7b783d907d27acaf223c8fe04150b4e9d36320e1994` |

I also recomputed the launcher’s complete Stage 1 per-file source map:
all 778 paths were present, there were no extra paths, and all 778 hashes
matched. The input manifest, generator manifest, export result, obligation-map
hash, trust-inventory hash, verification hash, and pinned toolchain object all
agree with the independently recomputed inputs.

## Inventory reconstruction and Stage 3 bijection

The frozen `verification.k` has SHA-256
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.
It contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The trusted lexical inventory selected `VERIFICATION`; its local module
closure is exactly `["VERIFICATION"]`. There are no `rule` sentences in that
closure. The independently reconstructed record is therefore:

- rule count: `0`;
- ordered source-rule ID list: `[]`;
- canonical inventory hash:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

`/reference/lemma-discovery.json` has schema version 2, the same inventory
hash, and `rules: []`. The trusted trust-boundary validator also accepted the
reconstruction. The comparison is bijective and order-preserving: there are
no omitted rules, duplicate IDs, extra IDs, reordered identities, changed
normalized hashes, or unaccounted classifications. Because the source
inventory is empty, there are no source spans, normalized hashes, or
`source_rule_id` values that could differ entry-by-entry.

## Independent classification judgment

The independent counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

This is not merely a structurally empty manifest. The true domain-lemma set is
genuinely empty for the frozen proof extension:

1. The source body is exactly
   `return len(set(string.lower()))`.
2. The supplied call semantics evaluates the user closure body and routes a
   bound method to `applyMethod` and builtins to `applyBuiltin`.
3. Supplied `lower` semantics rewrites
   `applyMethod(str(CS), "lower", .Vals)` to `str(mapLower(CS))`, where
   `mapLower` is the recursive operational definition using `lowerC`.
4. Supplied `set(str(CS))` semantics yields
   `setV(dedupCodes(CS))`, with `dedupCodes` and `dedupFrom` implementing the
   insert-if-absent fold.
5. Supplied `len(setV(DS))` semantics yields `isLen(DS)`, and `isLen` is the
   ordinary recursive sequence-length definition.
6. The frozen postcondition is exactly
   `isLen(dedupCodes(mapLower(CS)))`.

Thus the program executes through the supplied operational definitions
directly to the stated result. No proof-local simplification, semantic
shortcut, result-characterizing property, or human-facing domain fact is
assumed. There is also no candidate `PROVED_DERIVED_LEMMA` whose earlier
bridge-free proof would need validation and no simplification rule requiring
reclassification.

This judgment is relative to the explicitly selected supplied K semantics;
it does not silently replace those semantics with a different Unicode or
Python model.

## Deterministic Stage 4 generation

The independently checked Stage 4 bindings are:

- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`;
- manifest obligation count: `0`;
- obligation-map SHA-256:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- selected/export status: `KLEAN_NO_OBLIGATIONS`;
- expected target definition: `null`;
- parsed generated target: `null`;
- generator-manifest target: `null`.

The source-rule/obligation mapping is an exact ordered bijection. There is no
omission, duplicate, weakened obligation, irrelevant conjunct, or vacuous
generated target. In particular, the generator did not turn the empty
obligation set into an empty-conjunction theorem: `Lemmas.lean` contains only
its import and namespace.

The generated project contains 41 generic collection-hook executable axioms.
The trusted preflight independently found exactly the same declarations in
`trust-inventory.json`, rejected proposition trust, found zero designated
sorries, and found no generated target. Since there is no target or Stage 5
proof, these declarations cannot discharge a nonexistent obligation.

No `/candidate` exists, as required for a legitimate
`KLEAN_NO_OBLIGATIONS` result in classification-only mode.

## Required preflight rerun

I invoked `tools.klean_preflight.check_generation` with:

- frozen input: `/reference/k-proof`;
- discovery manifest: `/reference/lemma-discovery.json`;
- generation: `/reference/klean-generation`;
- toolchain lock: `/reference/klean-toolchain.lock.json`;
- `PYTHONPATH=/reference`.

The final returned evidence reports:

- status: `KLEAN_NO_OBLIGATIONS`;
- target: `null`;
- obligation count: `0`;
- designated sorry count: `0`;
- trust declaration count: `41`;
- Stage 1 hash:
  `f0d01b4844acc04f59f408c7bb9de48af59bbbd1ac0c52b85ac23b40e10ca168`;
- Stage 3 hash:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`;
- generated tree hash:
  `ad6a569222e70857c263c7b783d907d27acaf223c8fe04150b4e9d36320e1994`.

Its isolated `lake clean` exited 0. Its isolated `lake build` exited 0 and
built all generated modules. The complete build output is saved, and its hash
`5511683eb4f8c201cbd1a322726d655700a52c65c244f5999f574957ab4190c3`
also reproduces the selected Stage 4 preflight record.

The first attempt exposed an audit-container issue: processes received a
numeric PID for which `/proc/<pid>/exe` was absent, while `/proc/self/exe`
worked. Lean consequently could not locate its application. I preserved that
failure. I then used the saved, 39-line compatibility shim that changes only
`readlink("/proc/<digits>/exe", ...)` to
`readlink("/proc/self/exe", ...)`. It does not alter the generated project,
the frozen K input, producer source, manifests, Lean declarations, or build
commands. With that audit-environment compatibility in place, the exact
trusted preflight completed successfully.

## Evidence

- [Inventory, producer, provenance, and hash reconstruction](/audit-output/evidence/01-reconstruction-and-hashes.txt)
- [Frozen source, claim, and supplied operational rules](/audit-output/evidence/02-frozen-source-and-operational-rules.txt)
- [Preserved initial preflight failure](/audit-output/evidence/03-check-generation-preflight.txt)
- [Lean toolchain diagnostics](/audit-output/evidence/04-lean-toolchain-diagnostics.txt)
- [Preserved direct Lake failure before the compatibility diagnosis](/audit-output/evidence/05-direct-stage4-lake-diagnostics.txt)
- [Successful intermediate preflight rerun](/audit-output/evidence/06-check-generation-preflight-success.txt)
- [Generated-tree, obligation-map, target, trust, and candidate inspection](/audit-output/evidence/07-stage4-manual-inspection.txt)
- [Numeric `/proc` diagnosis and saved compatibility source validation](/audit-output/evidence/08-lean-proc-compatibility-diagnostic.txt)
- [Final trusted preflight return and complete clean-build output](/audit-output/evidence/09-final-check-generation-preflight.txt)
- [Preflight wrapper used to preserve complete subprocess output](/audit-output/evidence/run_preflight_audit.py)
- [Narrow `/proc/self/exe` compatibility source](/audit-output/evidence/proc_exe_compat.c)

## Final judgment

Stage 3 is a complete and correct empty classification, Stage 4 is bound to the
verified producer and frozen inputs and correctly emits no obligations and no
target, and Stage 5 is correctly absent in classification-only mode. No
legitimacy defect was found.

VERDICT: PASS
LEGITIMACY: LEGIT
