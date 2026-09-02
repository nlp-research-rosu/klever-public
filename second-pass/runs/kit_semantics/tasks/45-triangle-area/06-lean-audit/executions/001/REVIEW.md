# Independent Stage 3/4 audit: `45-triangle-area`

## Scope and result

This audit covers HumanEval problem `45-triangle-area`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
`/audit-input.json` select `CLASSIFICATION_ONLY`. Accordingly, Stage 5 proof
checks are not applicable. `/candidate` is absent, and both Lean-candidate
hashes in the audit input are null.

I did not rely on the prior Stage 2 verdict, Stage 3 classification, prior
preflight result, comments, or logs as authority. I used them only as values to
compare against independently reconstructed or recomputed evidence.

## Generator producer provenance

I hashed the two mounted generation-time producer sources before judging Stage
4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These values exactly equal the per-file values in
`generation-tools/source-manifest.json` and the `exporter_sha256` and
`klean_py_sha256` values in `generator-manifest.json`. The source manifest and
generator manifest both identify generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The same digest is the terminal component of the producer-source path recorded
in `/audit-input.json`. The producer-source tree independently hashes to
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly matching the audit input. There is no producer-provenance
infrastructure error.

Evidence: `evidence/01-producer-provenance.log`,
`evidence/02-manifests.log`, and `evidence/07-hash-and-bijection.log`.

## Inventory reconstruction and Stage 3 classification

The frozen `verification.k` has SHA-256
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.
The trusted `tools.k_rule_inventory.inventory_verification` selected module
`VERIFICATION` from the final `kompile verification.k --main-module
VERIFICATION` command in `prove.sh`. Its local module closure is exactly
`["VERIFICATION"]`.

That module occupies lines 3–5 of `verification.k` and contains only `imports
MPY`; it contains no rule, local imported module, syntax declaration, summary
definition, recurrence, macro, named proof term, operational bridge, or derived
lemma. The independently reconstructed ordered rule list is therefore exactly
`[]`. Its canonical inventory hash is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The protected `/reference/lemma-discovery.json` is the exact ordered projection
of that reconstruction: schema version 2, the same inventory hash, and the same
empty rule list. The comparison is bijective. There are no source spans,
normalized hashes, or source-rule identities that could be omitted,
duplicated, added, changed, or reordered. The trusted inventory code also
recomputed the verification file hash and module closure rather than accepting
them from Stage 3.

The independent semantic classification is consequently vacuous but genuine:

- There are zero `DEFINITION` entries.
- There are zero `OPERATIONAL_RULE` entries.
- There are zero `PROVED_DERIVED_LEMMA` entries.
- There are zero `DOMAIN_LEMMA` entries.
- There are zero local `simplification` rules.

This is mathematically appropriate for the frozen program, not an empty-set
loophole. The source body is exactly `return a * h / 2.0`. The supplied
semantics executes module loading, name lookup, closure application, parameter
binding, return/pop control, and binary-operator evaluation. Its ordinary
operator rules map integer multiplication to `*Int`, mixed multiplication to
`mulF` with `intToF`, integer/float division to `intFloatDiv`, and float/float
division to `divF`. The four Stage 1 claims state precisely those operational
results for Int/Int, Int/Float, Float/Int, and Float/Float inputs. None of those
rules is a proof-local addition in `verification.k`, and no human-facing area
identity or other domain fact is asserted as a simplifier. Thus there is no
relevant domain lemma to export.

Evidence: `evidence/03-frozen-sources-and-classification.log`,
`evidence/04-inventory-reconstruction.log`,
`evidence/inventory_check.py`, `evidence/06-operational-semantics.log`, and
`evidence/15-integer-operational-semantics.log`.

## Independent hash and manifest checks

I recomputed the audit-input path bindings with the trusted tree-hash
implementations. Every value matched:

| Binding | Recomputed value |
|---|---|
| Stage 1 artifact tree | `87b624a4f0ee2ccc7739d5fd57a2f4f2a1a896d85c60c9bdce7def39e02b3d07` |
| Stage 1 deterministic-export tree | `d98da7e202aadb71803162fa6a1bd2b9a93b95114e9cd0d8eeeb4e49ec812692` |
| Stage 2 artifact tree | `084e2998d769525519d48f6360ec75f0394e34582582ac161d44c1c4c3b95720` |
| Stage 3 manifest file | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 artifact tree | `314bbf018ffbe2d0d4bc7d2c082fe1370c008d858fa0154fff380b746ed10216` |
| Generated project tree | `156534a709df8cda51ca7912e710ccf993cf18c35062ea1e2440ae5a539b9021` |

I also checked all 769 individual Stage 1 file hashes recorded in the audit
input, including exact file-set equality; there were no missing, extra, or
mismatched files. The selected Stage 2 and Stage 4 artifact hashes match their
selection records. Cross-checks among `input-manifest.json`,
`generator-manifest.json`, `export-result.json`, `trust-inventory.json`, the
toolchain lock, `verification.k`, and `obligation-map.json` all passed. In
particular:

- `obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- `trust-inventory.json` hashes to
  `193c8f7bca1b19ef6a5ae5bfc8fd6556ed4612ce8f96907cb9831761c8ab51f4`;
- the toolchain object is exactly the pinned toolchain lock; and
- the Stage 1, Stage 3, inventory, generated-tree, obligation-map, and trust
  hashes agree across every sidecar that records them.

Evidence: `evidence/05-stage4-sidecars.log`,
`evidence/07-hash-and-bijection.log`, and
`evidence/hash_and_bijection_check.py`.

## Stage 4 bijection and fixed target

The independently established Stage 3 domain-rule sequence is empty. The Stage
4 input manifest has `source_rules: []`; the obligation map has
`source_rules: []`, `obligations: []`, and `trust_parameters: []`; the generator
and export manifests both record obligation count zero. This is an exact
source-rule/obligation bijection, `0 <-> 0`. There can be no omitted, duplicate,
irrelevant, weakened, or vacuous conjunct in an empty obligation list.

The trusted target constructor returns no expected target definition, and the
trusted generated-project target parser returns `null`. This exactly equals the
generator manifest's `target: null`. `Klean45TriangleArea/Lemmas.lean` contains
only its import, namespace opening, and namespace closing; an independent scan
found no theorem, lemma, example, `Proof.final`, or target-like declaration in
the generated project. Therefore Stage 4 did not change or weaken a target: it
correctly generated no target at all.

The selected status `KLEAN_NO_OBLIGATIONS` is legitimate because the true
independently classified domain set is genuinely empty. The required companion
conditions also hold: there is no generated target and no Stage 5 candidate.

Evidence: `evidence/07-hash-and-bijection.log` and
`evidence/14-target-and-candidate-absence.log`.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly the requested Stage 1 workspace, Stage 3 manifest, Stage 4
generation, and pinned toolchain lock.

The first invocation reached its fresh-copy `lake clean` but exposed an audit
container PID-namespace issue: Lean queried `/proc/<namespace-pid>/exe`, while
the mounted procfs did not expose that numeric PID. A trace demonstrated the
failed lookup, and unmodified Lean consequently reported `failed to locate
application`. I used a narrowly scoped compatibility library that changes only
numeric `/proc/<pid>/exe` `readlink` calls to `/proc/self/exe`; its complete
source is preserved in `evidence/proc_exe_compat.c`. With that environment fix,
the pinned tools identify themselves as Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0.

The rerun then completed successfully. Its returned evidence records:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit code 0;
- `lake build` exit code 0 and “Build completed successfully”;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- all Stage 1, Stage 3, and generated-tree snapshot hashes unchanged.

The compatibility adjustment addresses executable-path discovery only; it does
not rewrite generated source, alter Lean declarations, modify the immutable
inputs, or bypass any preflight gate.

Finally, I ran the trusted Stage 6 mechanical gate against the same mounted
inputs and audit binding. It returned `status: PASS`, mode
`CLASSIFICATION_ONLY`, target null, candidate hash null, and the same successful
preflight result. As designed, it marks semantic classification
`NOT_EVALUATED`; the independent classification judgment above supplies that
non-mechanical part of this review.

Evidence: the original environmental failure is in
`evidence/08-rerun-check-generation.log`; diagnosis and tool versions are in
`evidence/09-lean-toolchain-diagnostic.log` through
`evidence/12-proc-exe-compatibility.log`; the successful returned evidence is
in `evidence/13-rerun-check-generation.log`. Exact commands are collected in
`evidence/COMMANDS.md`. The final mechanical result and its raw output are
`evidence/16-mechanical-final-gate.json` and
`evidence/16-mechanical-final-gate.log`.

## Stage 5 disposition

Stage 5 was not run because the launcher selected `CLASSIFICATION_ONLY`, the
generated target is null, and `/candidate` is absent. Running candidate build,
`#print axioms Proof.final`, proof-identity, or operational-bridge checks would
be inapplicable: there is no fixed proposition or proof candidate to inspect.

## Conclusion

The protected Stage 3 classification exactly matches an independently
reconstructed empty local rule inventory. The empty domain-lemma judgment is
correct for this frozen operational proof. All producer, source, artifact,
sidecar, and target bindings checked above are consistent. Deterministic Stage
4 correctly selected `KLEAN_NO_OBLIGATIONS`, emitted no target, and has no Stage
5 candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
