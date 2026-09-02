# Independent Stage 3/4 Audit: HumanEval `80-is-happy`

## Scope and result

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for condition
`bare` and semantics mode `GENERATED_SEMANTICS`. Stage 4 is recorded as
`KLEAN_NO_OBLIGATIONS`. There is no Stage 5 workspace, invocation, result, or
`/candidate`.

I treated the mounted Stage 1/2/3/4 artifacts, their logs, comments, and prior
reviews only as untrusted evidence. I did not execute any script from those
artifacts. I executed only the trusted modules under `/reference/tools`, the
pinned Lean/Lake binaries through the trusted preflight, and two independently
written audit scripts under `/audit-output/evidence`.

The result is a pass. The ten rules in the local verification-module closure
are all genuine definitions. The independently reconstructed `DOMAIN_LEMMA`
set is empty, so the deterministic Stage 4 empty obligation set and absent
target are mathematically appropriate rather than an omission.

## Generation-producer provenance gate

I hashed the two mounted generation-time producer sources before judging Stage
4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image ID is identically
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, generator manifest provenance, and the immutable
producer-source path recorded by `/audit-input.json`. The complete producer
bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching the audit input. The bundle contains only the two
producers and its source manifest. There is therefore no producer-provenance
`AUDIT_ERROR`.

The generator's toolchain object also exactly matches
`/reference/klean-toolchain.lock.json`, including Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

## Inventory reconstruction and manifest bijection

I called the trusted `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on `/reference/k-proof`. It selected module
`VERIFICATION`; its local module closure is exactly `["VERIFICATION"]`. The
frozen `verification.k` hash is
`bdc20e814982237e00dfd33e022c8b590e2ed7c304180ace4f87e88f42e3a62d`.

The reconstruction found exactly ten rules. For each rule I independently
checked that:

- the reported line span slices the exact source text;
- normalizing whitespace and hashing the text reproduces
  `normalized_sha256`;
- `source_rule_id` is exactly `rule-` followed by that hash; and
- the canonical JSON hash of the ordered rule records reproduces the whole
  inventory hash.

The whole inventory hash is
`e04c1af4b26723a5714f4f85dc6110990a90f9cef9e8a9a8821d48c8f3ac92f9`.
The inventory is:

| Lines | Normalized SHA-256 | Rule head | Independent class |
|---:|---|---|---|
| 9–12 | `69601beb0343036e854813d9040d0e7be89139b3e0cd50ce596794209dca4f61` | `#distinct3(A,B,C)` | `DEFINITION` |
| 15 | `478cd4b6502eecc48e84415ded3bd64091a052e8a8199bb6d03d3e1d7312f9d5` | `#allTriples(eps)` | `DEFINITION` |
| 16 | `a700fc43e7c1a3f9ded4078cffd324126d78a8eec4c13f1f47553e95618b5af6` | one-character `#allTriples` | `DEFINITION` |
| 17 | `5d2499db9648ae526689de44b92045f3c86424b21d0436b59aa258f6f90179f7` | two-character `#allTriples` | `DEFINITION` |
| 18–20 | `0b0dfd5e96ef2a2d5ad5724d4fdf3772ecb74fcc9bc3529173452c8ce4c5e525` | recursive `#allTriples` | `DEFINITION` |
| 23 | `b18edf589ca2fa028207e23f3bdcab82f0c96369e0a227b35688bf81a9cd55e1` | `#happy(eps)` | `DEFINITION` |
| 24 | `2298e96555ab8f5332d8e1231a4f428ed5d45e88d963c77663edc2cd3eebc944` | one-character `#happy` | `DEFINITION` |
| 25 | `6a146cc6de613319d0d1b7bba22a7c30cbf871a2df749c76588ac44cebfe1bfe` | two-character `#happy` | `DEFINITION` |
| 26–27 | `101f770cf9ecaed7611d946159a4da00a907686825770c0aaa6a4a712cee3092` | long-string `#happy` | `DEFINITION` |
| 33–58 | `d84b4a2297a281eb3055e9a3fdf6ffda1c4f8b4c58c4d048a96230da446fa94c` | `#solution` | `DEFINITION` |

The protected Stage 3 manifest has SHA-256
`31b81ea634f26c28d1d082bb46ffe44b6a784cc1ae3c44cd3f1f11a780765b1c`.
Its ten identities occur once each and in exactly the canonical order above.
There are no omissions, duplicates, extra identities, reordered identities,
changed rule hashes, changed spans, or unaccounted classifications. The trusted
`lemma_discovery_contract.validate_trust_boundary` also accepts the bijection.

## Independent classification judgment

All ten classifications are substantively correct, not merely
manifest-consistent:

- Lines 9–12 are the defining equation for the named Boolean summary
  `#distinct3`. Its right side is exactly the conjunction of the three pairwise
  integer inequalities.
- Lines 15–20 are exhaustive defining equations for `#allTriples`. The three
  base cases say that a sequence shorter than three has no bad window. The
  recursive equation checks the leading window and recurs after removing
  exactly one leading element. It is a structurally decreasing recurrence.
- Lines 23–27 are exhaustive defining equations for `#happy`: lengths zero,
  one, and two are false, while every longer value delegates to the
  `#allTriples` summary. This is exactly the prompt's minimum-length condition.
- Lines 33–58 define the named proof term `#solution` by expanding it to the
  exact constructor tree for the two frozen functions. This is a macro/named
  proof term, a category explicitly allowed as `DEFINITION`.

None of these rules is an ordinary execution or observation rule. In
particular, they do not match an active configuration or bypass the program's
call, branch, equality, indexing, slicing, or recursion semantics. The
operational K rules in `semantic.k` still perform:

- function lookup and body execution through `#call`, `#findCall`, and
  `#exec`;
- the length split through `#len` and `#short3`;
- character equality through `#at` and `#same`; and
- the recursive suffix call through `#drop` and the ordinary call rules.

`#solution` merely supplies the exact program AST to those operational rules.
`#happy` and `#allTriples` occur as mathematical result summaries in the
claims; their definitions do not themselves assert or shortcut the connection
between execution and the postcondition.

There is no rule that Stage 1 first proves in a module omitting that rule and
then reuses, so the `PROVED_DERIVED_LEMMA` set is empty. There is no
independent algebraic/domain fact beyond the defining equations, so the
`DOMAIN_LEMMA` set is empty. No inventory rule carries the `simplification`
attribute. The final independent class counts are therefore:

| Class | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The definitions are relevant and mathematically faithful to both the source
program and the postcondition. As finite adversarial support for that
source-level judgment, an independently transcribed program, the recursive
definitions, and a direct sliding-window oracle agreed on all 9,841 strings
over a three-element alphabet of lengths 0 through 8, plus boundary values.
Counterfactual mutations were distinguished by concrete witnesses:

| Mutation | Witness | Incorrect mutation result | Required result |
|---|---|---:|---:|
| accept short strings | `()` | true | false |
| inspect only the first window | `(0,1,2,1)` | true | false |
| require global distinctness | `(0,1,2,0)` | false | true |
| omit the positions 1/2 equality check | `(0,1,1)` | true | false |
| reject length exactly three | `(0,1,2)` | false | true |

These tests are supporting evidence; the classification rests on the exact
equation forms and the operational reading above.

## Recorded hash reconciliation

The signed resolution digest recomputes to
`490c8b85fef60f45180090d2b082953f9d2558961991d6c17a57bf58c01ed567`.
Using the pipeline's trusted tree algorithms, every signed artifact hash
recomputed exactly:

| Artifact/hash kind | SHA-256 |
|---|---|
| Stage 1 workspace tree | `e0695ff94065e513581874b71a3f647dcb9dbae0f7baf92e499d8e6c4ff375a2` |
| Stage 1 deterministic export tree | `6c193a097c19a20c2334e2c36a1800c383acf8c72ddc55c284d33d090dce83a9` |
| Stage 3 manifest | `31b81ea634f26c28d1d082bb46ffe44b6a784cc1ae3c44cd3f1f11a780765b1c` |
| Selected Stage 2 audit tree | `fca4651124b35169df1a7335037e6e78b711b429ac89e107370ebe73d5ec2278` |
| Selected Stage 4 generation tree | `e01f9566034fcd48dd05c844629c61c10b2c2f07310756da47a6dd30b93ce4b6` |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `fd5801b9e10edc11b190f92e3d291c6a6ec5888ed808c74b9551c461dd3b33f5` |

All eight individual Stage 1 source hashes also match the audit input. The
selected artifact hashes, input manifest, generator provenance, export result,
recorded preflight, and embedded preflight record all agree with these values.
The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
the trust-inventory hash is
`5a12ea96ea71cc234663cf7c8d97227fe410cd118dd12fb11b4e36fcb66054ca`.
The recorded complete `lake clean` and `lake build` output strings reproduce
their recorded diagnostic hashes.

## Stage 4 obligation bijection and target identity

Because the independently classified domain set is empty, the exact
source-rule/obligation bijection is the empty bijection:

```text
input-manifest.source_rules       = []
obligation-map.source_rules       = []
obligation-map.obligations        = []
obligation-map.trust_parameters   = []
```

The generator manifest, export result, recorded preflight, and audit input all
record obligation count zero. The trusted expected-target reconstruction
returns `None`; the trusted target parser finds no generated target; and the
generator manifest and audit input both have `target: null`.
`Klean80IsHappy/Lemmas.lean` contains only its imports and an empty namespace.
Thus there is no omitted obligation, duplicate, irrelevant/weak conjunct,
vacuous conjunct, altered theorem, or target to weaken. `KLEAN_NO_OBLIGATIONS`
is the correct Stage 4 status.

## Fresh trusted preflight

The first exact invocation of
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` reached
its temporary-copy build phase but the managed sandbox's Lean launcher could
not detect its installation. A direct trace showed Lean requesting
`/proc/<namespace-pid>/exe`, which this sandbox denied or omitted even though
`/proc/self/exe` resolved to the same pinned executable.

I used a recorded, narrowly scoped `LD_PRELOAD` workaround that passes every
`readlink` through unchanged and only retries a failed
`/proc/<digits>/exe` lookup as `/proc/self/exe`. Its complete C source and hash
are in the evidence directory. With that path-resolution workaround, the same
trusted `check_generation` call returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean exit_code: 0
lake build exit_code: 0
designated_sorry_count: 0
trust_declaration_count: 41
```

The build compiled all generated modules successfully. The workaround changes
only how the pinned executable discovers its own path; its trace confirms that
each fallback resolves to the pinned Lean/Lake installation. The trusted
preflight also re-snapshotted all immutable inputs after the build and found no
change.

## Stage 5 and proof-mode checks

Proof-mode checks are not applicable. The launcher mode is
`CLASSIFICATION_ONLY`, the genuine domain set is empty, Stage 4 has no target,
the audit input has no Lean workspace or invocation, there is no Stage 5
result, and `/candidate` is absent. Accordingly there is no `Proof.final`,
axiom printout, target parameter, or candidate operational bridge to audit.
Creating or accepting a Stage 5 proof in this state would have violated the
required no-obligation contract.

## Evidence index

Raw commands and outputs are under `/audit-output/evidence/`. The principal
records are:

- `01_manifests_and_producer_hashes.txt`: producer hashes and all Stage 4
  manifests, captured before Stage 4 judgment;
- `02_inventory_manifest_and_frozen_sources.txt`: canonical inventory,
  protected manifest, and line-numbered frozen sources;
- `03_independent_recorded_hashes.txt`: trusted tree and source hashes;
- `04_fresh_check_generation.txt`: initial exact preflight and environment
  failure;
- `05_toolchain_diagnosis.txt` through
  `08_fresh_check_generation_success.txt`: diagnosis, auditable workaround,
  and successful fresh preflight;
- `09_prompt_generated_target_and_candidate_absence.txt`: prompt, empty target
  module, and candidate absence;
- `10_independent_checks_and_math_witnesses.txt`: exact rule/span/hash checks
  and counterfactual witnesses;
- `11_expanded_independent_hash_checks.txt`: final complete manifest/hash and
  empty-bijection reconciliation;
- `independent_checks.py` and `classification_witness.py`: independently
  written audit code; and
- `lean_proc_self_workaround.c`: exact transparent executable-path workaround.

VERDICT: PASS
LEGITIMACY: LEGIT
