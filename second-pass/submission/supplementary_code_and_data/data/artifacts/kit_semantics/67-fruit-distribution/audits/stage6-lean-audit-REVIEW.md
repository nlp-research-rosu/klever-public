# Independent Stage 3–5 audit: `67-fruit-distribution`

## Scope and audit mode

This audit covers HumanEval problem `67-fruit-distribution`, condition
`kit-semantics`, with `SUPPLIED_SEMANTICS`. The signed launcher envelope has
canonical resolution hash
`05ed201fb4314694b74395b8d1d9d90ff8665328ece4cac3100f7e6f5349a578`.
Both the envelope and `AUDIT_MODE` select `CLASSIFICATION_ONLY`. The signed
Lean workspace and invocation paths are null, the signed target is null, and
`/candidate` is absent. Consequently Stage 5 proof checks—including a Base
copy, `Proof.final`, `#print axioms`, and parameter bridge checks—are neither
applicable nor permitted for this run.

All mounted candidate and provenance material was treated as untrusted
evidence. In particular, the generation-time producer files were hashed but
not executed. Executed pipeline code came only from the trusted
`/reference/tools` package. Exact commands, audit scripts, and raw transcripts
are indexed in [evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## Generation-producer integrity

The producer check passed before any Stage 4 judgment:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

The bundle contains exactly those two files and `source-manifest.json`, all
regular files. Its independently recomputed pipeline tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching the signed audit input. The source manifest and generator manifest
both bind the same producer hashes and immutable image ID
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the signed producer-bundle path has that image digest as its basename. There
is no producer-source infrastructure error. Full evidence is in
[00-context-and-producer-integrity.log](/audit-output/evidence/00-context-and-producer-integrity.log).

## Inventory reconstruction and Stage 3 classification

The trusted inventory implementation independently selected main module
`VERIFICATION`, as fixed by `prove.sh`, and reconstructed its local module
closure as exactly `["VERIFICATION"]`. The frozen `verification.k` is:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

Its direct and recorded SHA-256 is
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.
It contains no proof-local `rule` sentence. The supplied `MPY` operational
semantics is external to this local proof-extension inventory; importing it
does not create a proof-local lemma.

The reconstructed ordered rule list is therefore `[]`. Its canonical whole-
inventory hash is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
which is also the Stage 3 value. The Stage 3 file hash is
`e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`,
matching the signed audit input. The manifest's ordered identity list is also
`[]`: there are no omissions, duplicates, extras, reordered identities,
changed spans, changed normalized hashes, or unaccounted classifications.

Independent reclassification yields zero `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`
entries. There are also no `simplification` rules. Thus none can be a hidden
or mislabeled domain lemma, and the true domain-lemma set is genuinely empty,
not merely declared empty. See
[01-inventory-reconstruction.log](/audit-output/evidence/01-inventory-reconstruction.log).

## Mathematical and operational judgment

The empty classification agrees with the frozen program rather than evading
its postcondition. The source body is exactly:

```python
return n - int(s.split()[0]) - int(s.split()[3])
```

The K claim embeds the same two-argument closure, the same left-associated
subtractions, split indices `0` and `3`, and the exact result
`N -Int APPLES -Int ORANGES`. Its precondition binds `splitWS` to the five
expected tokens and binds both `int` applications to `APPLES` and `ORANGES`.
The supplied operational semantics executes no-argument whitespace splitting,
list indexing, single- and multi-digit integer conversion, `BinOp` dispatch,
and integer subtraction. No summary, recurrence, macro, named proof term,
execution bridge, or mathematical result fact was added in `verification.k`.
Accordingly there is no source-relevant domain fact for Stage 4 to export.
The checked source and rule excerpts are in
[06-program-semantics-alignment.log](/audit-output/evidence/06-program-semantics-alignment.log).

## Stage 4 preflight and provenance hashes

I invoked the required trusted entry point
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
exact frozen paths `/reference/k-proof`, `/reference/lemma-discovery.json`, and
`/reference/klean-generation`, plus the trusted toolchain lock.

The first invocation exposed a container-only launcher fault: Lean 4.22 reads
`/proc/<getpid()>/exe`, but this managed environment reports namespace-local
PIDs while mounting a host-PID `/proc`, producing `ENOENT`. This failed before
`lake clean` and is retained in
[02-preflight-rerun.log](/audit-output/evidence/02-preflight-rerun.log). A
narrow preload shim was compiled under `/tmp/audit-work`; it redirects only
numeric `/proc/<pid>/exe` reads to the equivalent `/proc/self/exe`. With this
environment correction, `lean --version` reported the pinned Lean 4.22.0
commit and the unchanged trusted preflight was rerun.

The rerun returned:

- `lake clean`: exit 0;
- `lake build`: exit 0, all seven generated modules built;
- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- generated tree hash
  `554f0f16aa139947c0e475b5578afcd34428607c2e7ced13afe1f32bce63bfdd`;
- frozen Stage 1 export hash
  `d11c8e7a3ed873e17c5a1347d00c9f6f621cc64a09c176c47329d8f21effcf95`;
- Stage 3 file hash
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`;
- no generated `sorry` and 41 non-propositional generated trust declarations
  matching the trust inventory.

The successful returned evidence is in
[04-preflight-rerun-with-proc-shim.log](/audit-output/evidence/04-preflight-rerun-with-proc-shim.log).
The independent build's output hash differs from the generation-time diagnostic
only because independent Lean jobs reported `Func` and `Lemmas` completion in
a different order; both complete builds exit 0. The original diagnostic hashes
were separately recomputed from their complete retained outputs and match.

Beyond preflight, I recomputed every signed top-level artifact hash and all 776
signed Stage 1 per-file hashes. The observed and recorded file sets and values
are identical; their canonical map digest is
`02890de2d792204bc0aaa9e1f388c5592cfc3686509ee635fb7c17ddfa9d615b`.
The input-manifest, generator-manifest, export-result, preflight, obligation-map,
trust-inventory, toolchain, source, discovery, inventory, and producer hash
bindings all agree. Details are in
[05-stage4-hashes-bijection-target.log](/audit-output/evidence/05-stage4-hashes-bijection-target.log).

## Obligation bijection and fixed target

The independently reconstructed domain source-rule list, input-manifest
`source_rules`, obligation-map `source_rules`, obligation list, and ordered
obligation-ID list are all exactly `[]`. The trust-parameter list is also
`[]`. This is an exact bijection with no omission or duplicate. Because there
are no conjuncts, none can be irrelevant, weakened, or vacuous.

The generated Lean sources contain no `targetStatement` declaration. The
trusted target parser returns null, and the expected target definition for the
empty obligation set is null. This agrees with the generator manifest,
preflight, export result, signed audit input, and selected
`KLEAN_NO_OBLIGATIONS` status. No Stage 5 candidate exists. The generated
collection-hook trust declarations therefore support generated semantic
infrastructure only; there is no proposition or proof target whose legitimacy
could depend on them in this classification-only case.

## Conclusion

The protected Stage 3 classification is bijectively correct, the true domain-
lemma set is empty, the deterministic Stage 4 artifacts and provenance are
intact, and `KLEAN_NO_OBLIGATIONS` is the mathematically correct outcome. The
required absence of both a generated target and a Stage 5 proof candidate is
satisfied. No concern affects legitimacy.

VERDICT: PASS
LEGITIMACY: LEGIT
