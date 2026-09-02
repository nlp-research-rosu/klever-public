# Independent Stage 3/4 audit: HumanEval 88-sort-array

## Result and scope

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition
`kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. The selected Stage 4
status is `KLEAN_NO_OBLIGATIONS`; `/candidate` does not exist, and the launcher
records null Stage 5 paths and hashes. Accordingly, the Stage 5 clean-copy,
`Proof.final`, axiom-reconciliation, and operational-bridge-parameter checks do
not apply.

I treated all mounted Stage 1--5 artifacts, prior reviews, comments, and logs as
untrusted evidence. I used the mounted trusted inventory and preflight code for
mechanical reconstruction, then made the classification and obligation-scope
judgments directly from the frozen source and supplied operational semantics.

## Producer-source and provenance gate

I hashed the generation-time producer sources before judging Stage 4:

| Source | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

These values agree with both `generator-manifest.json` and
`generation-tools/source-manifest.json`. The generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests, and the basename of the producer-source path recorded in
`/audit-input.json` is the same digest. Using the launcher's trusted tree-hash
routine, `/reference/generation-tools` hashes to
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
exactly the audit-input value. There is no producer-source infrastructure error.

## Frozen program and operational meaning

The frozen source returns a new sorted copy. The empty branch returns
`sorted(array)`. The nonempty branch selects descending order exactly when
`(array[0] + array[-1]) % 2 == 0`; otherwise it selects ascending order. The
prompt restricts inputs to non-negative integers.

The supplied semantics represents integer sequences by `.IntSeq`/`iCons` and
value sequences by `.ValSeq`/`vCons`. It evaluates list truthiness, normalizes
negative indices (so `-1` selects the last element), implements integer addition
and Python-style modulo, and routes `sorted(..., reverse=RB)` to a fresh list
containing `condRev(sortVS(VS), RB)`. The nonempty K claim mirrors that behavior:
it leaves the input heap object unchanged and allocates a result containing
`condRev(sortVS(intVals(...)), pyMod(F +Int L, 2) ==Int 0)`.

`sortVS` is a primitive of the frozen supplied semantics, not a proof-local rule
in `verification.k`; it is therefore outside this Stage 3 local-rule inventory.
No proof-local rule preempts a source call, control step, heap effect, index
operation, parity calculation, or sort operation.

## Independent inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` over the frozen
`/reference/k-proof`. It selected module `VERIFICATION`, with local closure
`VERIFICATION-SYNTAX` and `VERIFICATION`, and reconstructed:

- `verification.k` SHA-256:
  `4887dbdeb7f4eccb4377a96946b1d2d20783961229af26682301e5feef32bec7`;
- four rules, in source order; and
- inventory SHA-256:
  `79bcb25ad216ecb707ec3f1dc4591a1afb03ed9a778f0fa2d7bd947b49333a50`.

The protected Stage 3 file has the same inventory hash and exactly the same four
ordered, unique rule IDs. There are no missing, extra, duplicated, or reordered
rules. Each reconstructed line span, normalized source hash, source text, and
`source_rule_id` agrees with the corresponding Stage 4 definition record.

## Independent classification

| Span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 15 | `rule-61708f547727d7aa918ad6bf8a016e92b25d1ccd0e36098b415347016593af3e` | `DEFINITION` | Base equation `intVals(.IntSeq) => .ValSeq` for the freshly declared proof-side embedding. |
| 16 | `rule-cfcac90169b6a7cd2244c88675990844903b2aaec267489c942ae4ccd2156521` | `DEFINITION` | Constructor equation preserving the integer head and recursively embedding the strictly smaller tail. |
| 18 | `rule-a9f37c1eb33efeb535d72a822b8dfc6ea4e900fe284743e255793a6456e2a7e8` | `DEFINITION` | Base equation for the proof-side `nonNegative` predicate; `true` is the empty conjunction. |
| 19--20 | `rule-758572a581b5030cc9404c6609e8681bf8bd5aa4744ae6307a1a2074351c15c9` | `DEFINITION` | Recursive predicate equation checking the head and recurring on the strictly smaller tail. |

The two constructor pairs are exhaustive and non-overlapping because `IntSeq`
has exactly the empty and `iCons` constructors. Both recurrences structurally
descend. `intVals` merely represents the K claim's symbolic list; for example it
retains a negative head rather than filtering or sorting it. `nonNegative`
computes the source precondition: it is true on `[]` and `[0, 2]`, and false on
`[-1]`. It does not assume that an arbitrary input is non-negative and does not
state a result property.

Thus all four rules genuinely define summaries/named proof terms. None is an
ordinary operational rule, a proved-derived lemma, or a domain lemma. No rule
has a `simplification` attribute, so the special simplification constraint is
satisfied. There is no claimed `PROVED_DERIVED_LEMMA` whose earlier proof would
need reconstruction, and no result-characterizing or irrelevant domain lemma is
hidden under another label.

The independently determined true domain-lemma set is therefore empty.

## Hash and manifest integrity

Independent recomputation matched every launcher resolution hash:

| Artifact | SHA-256 |
|---|---|
| Stage 1 selected workspace tree | `b98aefcb26a64daa334e6b44b95fa62afaad9ba6357bcf4058624d5b957ad4bc` |
| Stage 1 deterministic export tree | `43eac14c36be37fc866a669c67b150c1517da01c7ac93c9d464fcd41d41216d9` |
| Stage 2 selected audit tree | `287e053a6e423a8f404f0d8ae67f4900ea4093cb4485a52b378029ce15c21b2d` |
| Stage 3 discovery manifest | `821c90e5d8690eed3b7af8c3553b49a252d50add20afcc8dc613dbcb476d465f` |
| Stage 4 selected generation tree | `15b6111505ecc896edde5ee98ba83cdcc2b6d053b1e820e3e207989799764e49` |
| Generated Lean project tree | `ba0ca84fc18187f1c326d4a2ada7c121547288ae27add1be3e2c155eaf2c5d24` |
| Generation producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

I also recomputed the per-file Stage 1 source map: all 771 expected files are
present, no extra file is present, and no file hash differs. The generated
`obligation-map.json` file hashes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and `trust-inventory.json` hashes to
`78b2a7ec91bb6d65123199e89ced3eef15ff3a24614b2dc1fb2f031ca1c1c1b0`,
matching their manifest bindings.

## Stage 4 bijection, obligations, and target

The Stage 4 `definitions` array is an exact field-for-field join of the
reconstructed inventory and protected classification, in source order. Its
operational-rule, proved-derived-lemma, and source-rule arrays are empty. The
obligation map has empty `source_rules`, `obligations`, and `trust_parameters`
arrays. Consequently there are no omitted or duplicated obligations, no
weakened or irrelevant conjuncts, and no vacuous conjunct to exploit.

The generator manifest records obligation count zero and target null. An
independent `klean_export.target_statement` scan also returns null, and
`/audit-input.json` records target null. There is no hidden or changed generated
target declaration. This is the required fixed output for the genuinely empty
domain set.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned
toolchain lock.

The first invocation exposed a sandbox-only Lean runtime issue: this container
provides `/proc/self/exe` but not Lean 4.22's `/proc/<own-pid>/exe` lookup. I
recorded that failure, the diagnosis, and the source of a narrow local preload
shim that changes only that self-executable lookup to `/proc/self/exe`. With the
pinned Lean toolchain first on `PATH` and that compatibility shim, the exact
preflight completed successfully. The shim cannot alter file reads, hashes,
classification, generated source, theorem text, or Lean elaboration.

The returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 hash `43eac14c...16d9`;
- Stage 3 hash `821c90e5...465f`;
- generated tree hash `ba0ca84f...d24`;
- obligation count 0;
- target null;
- designated sorry count 0;
- trust declaration count 41, exactly reconciled by preflight with the generated
  trust allowlist;
- `lake clean` exit 0; and
- `lake build` exit 0 with output hash
  `54172f8c62c8e496c2db96a5cd40b197358836307654e34c49c14f167d10324f`.

The successful preflight also rechecked the immutable snapshots after the
build. Because this is classification-only mode with no target, there is no
`Proof.final` and no proof axiom dependency set to audit.

## Evidence index

Raw commands and outputs are under `/audit-output/evidence/`. The principal
records are listed with their exact invocations in `evidence/COMMANDS.md` and
include:

- `01-producer-hashes.txt`, `03-generator-manifest.txt`,
  `04-source-manifest.txt`, `05-audit-input-producer-fields.txt`, and
  `07-producer-tree-hash-pipeline.txt`;
- `08-reconstructed-inventory.json.txt`, `09-lemma-discovery.txt`,
  `10-verification-k.txt`, `11-spec-k.txt`, `12-solution-py.txt`, and
  `23-relevant-operational-semantics.txt`;
- `14-rerun-preflight.txt` (initial environment failure),
  `15-rerun-preflight-with-sandbox-shim.txt` (successful returned evidence),
  `26-lean-sandbox-shim-diagnosis.txt`, and `lean-proc-self-shim.c`;
- `16-independent-high-level-hashes.txt`,
  `17-stage1-source-hash-bijection-and-mode.txt`,
  `19-generation-sidecar-file-hashes.txt`, and
  `22-inventory-discovery-bijection.txt`; and
- `18-generation-maps-and-result.txt`, `20-generated-tree-target-and-candidate-absence.txt`,
  `21-fixed-target-identity.txt`, `24-candidate-absence.txt`, and
  `25-independent-manifest-bijection.txt`.

VERDICT: PASS
LEGITIMACY: LEGIT
