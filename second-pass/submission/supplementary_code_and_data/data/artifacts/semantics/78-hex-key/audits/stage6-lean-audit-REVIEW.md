# Independent Stage 3/4 Audit: HumanEval `78-hex-key`

## Scope and conclusion

The launcher-signed input and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY` for condition `semantics` in
`SUPPLIED_SEMANTICS` mode. I therefore audited the frozen Stage 1 K
workspace, the protected Stage 3 classification, and the deterministic
Stage 4 generation. Stage 5 proof checks are not applicable. `/candidate`
is absent, as required.

The protected classification is complete and mathematically appropriate:
all eight local verification-module rules are definitions, and none is a
domain lemma. Consequently the selected `KLEAN_NO_OBLIGATIONS` generation
has the correct empty obligation set and no generated theorem target.

All mounted candidate and provenance material was treated as untrusted
evidence. The reconstruction and checks used the trusted code under
`/reference/tools`; earlier verdicts and logs were not used as authority.

## Producer provenance gate

I hashed both mounted generation-time producer files before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Each hash exactly matches both `source-manifest.json` and
`generator-manifest.json`. The producer-source tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`. The immutable image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest and generator manifest; the same digest is the
basename of the producer-source path signed in `/audit-input.json`.
There is no producer-source infrastructure error.

The signed audit-input envelope also validates under the trusted resolution
contract, including resolved-input digest
`0d54ae98c9ef06efd3418df4b4b642cdeac507d9bb72d312e4f45f01e5dd47e4`.

## Inventory reconstruction and bijection

Using `tools.k_rule_inventory.inventory_verification` on the frozen
workspace, I reconstructed the local closure selected by `prove.sh`. It
contains only `HEX-KEY-VERIFICATION`; the imported `MPY` module is external
to the local `verification.k` module set. The frozen `verification.k` byte
hash is
`b1555a5f26720a92c97e2f0e4a6be1f8c79b7fe2dd01048e3a821f8f73a2d1ec`.

For every rule I independently checked that the reconstructed text is the
exact physical source slice, normalized it with whitespace joining,
recomputed SHA-256, and confirmed that `source_rule_id` is `rule-` followed
by that hash:

| Order | Lines | Defined term | Normalized SHA-256 |
|---:|---:|---|---|
| 1 | 9–12 | `hexKeyLoopBody` | `a21c4e1376187971c7643f3e565cabcbfd4adf8fb326ad1b1ed66d8ccf2ee5dc` |
| 2 | 15–19 | `hexKeyBody` | `997f1164935d81cf0a177321cded75d4547861c8641b38c27297eb3d9a029072` |
| 3 | 23–26 | `isPrimeHexCode` | `05b5f69701a4c26d96e9102f57d9aa376b71ec50124579bbae35e8fbfd93bf81` |
| 4 | 29–30 | `primeHexBit` | `3532524624ac91c8c5bef2d87f5c2bf88f8419752a22a63b80e9c9fca7ff5702` |
| 5 | 33 | `hexCount` base | `1f493419665e264916f30ab5358e05eef39549f5227088474c1ff240d5e27abe` |
| 6 | 34–35 | `hexCount` step | `690663e02cb1ae6cd79a33453a4d2c75dbd0a76973cc10dc57fcdd89a7cf8993` |
| 7 | 40 | `finalDigit` base | `2c5863a720c0bb1e81a39efe6316267a1af396797c22acd873b152227333ade3` |
| 8 | 41–42 | `finalDigit` step | `f95b3740442b75f1ff5a75424586af712960c05b37858b16c5f6802d8b9b2d38` |

The canonical whole-inventory hash is
`bc46fe896b90ee97006a88310d20365bdecd25a1fd99b06a42a35b7c0bca0217`.
It matches the Stage 3 manifest and all Stage 4 provenance fields.

The Stage 3 rule list has exactly the eight identities above in that exact
order. There are no omissions, extra entries, duplicate identities,
reordered identities, changed hashes, or unclassified rules. The trusted
Stage 3 contract independently accepts the same bijection.

## Independent classification judgment

I reclassified each rule from its frozen source and the supplied operational
semantics:

1. `hexKeyLoopBody` is a `DEFINITION`. Its syntax production is a named
   `[macro]`, and its equation expands that proof term to the exact loop-body
   statement tree.
2. `hexKeyBody` is a `DEFINITION`. It similarly expands a named `[macro]` to
   the translated function body: initialize `count`, initialize `digit`,
   iterate over `num`, and return `count`.
3. `isPrimeHexCode` is a `DEFINITION`. It defines a named Boolean summary as
   one-character containment in the code sequence
   `[50, 51, 53, 55, 66, 68]`, exactly the characters `2`, `3`, `5`, `7`,
   `B`, and `D`.
4. `primeHexBit` is a `DEFINITION`. It defines the named numeric indicator
   of `isPrimeHexCode`, returning one or zero.
5. The empty `hexCount` equation is the base case of a named recursive
   summary, so it is a `DEFINITION`.
6. The constructor `hexCount` equation is the recurrence for that same
   summary, so it is a `DEFINITION`.
7. The empty `finalDigit` equation is the base case of the named loop-state
   summary, so it is a `DEFINITION`.
8. The constructor `finalDigit` equation is its recurrence, so it is a
   `DEFINITION`.

The operational bridge behind those judgments is direct. The supplied
string iterator yields a one-character string for each head code. String
`in` dispatches to `strContains`; the loop binds the yielded character,
executes the body, and continues on the remainder. The body increments
`count` exactly when that character occurs in `"2357BD"`. Thus `primeHexBit`
is the exact per-character increment and `hexCount` is the exact fold over
the input. `finalDigit` preserves the old value for empty input and otherwise
returns the final one-character string, exactly matching the loop claim's
non-return observable. Both named AST macros match `solution.mpy` and
`solution.py`, and the entry claim returns `hexCount(CS)`.

None of the eight equations asserts a free-standing domain fact. In
particular, the recurrences define their left-hand symbols rather than
claiming algebraic properties about pre-existing operations. None is an
ordinary execution/observation rule, and none satisfies the required
two-stage history for `PROVED_DERIVED_LEMMA`; all are present in the module
used by the Stage 1 claims. No rule has a `simplification` attribute, so
there is also no simplification rule misclassified as operational or
proved-derived.

The independent classification is therefore:

- `DEFINITION`: 8
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The domain set is genuinely empty, not merely recorded as empty.

## Recorded hashes and deterministic Stage 4 structure

The trusted hashing implementations reproduce every signed tree binding:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `8f836f571d09156d18504ec31d539ccdd85610d0ceb389cb7e0bb2e18ba0fab9` |
| Stage 1 deterministic-export tree | `d5b755ed0aa090f8d2d4c9daf81edea832cab03696cd4d00be5e304816afad45` |
| Selected Stage 2 audit tree | `65fd58562d82db019dfc191596129cc261d2603f2339333716c160e88e7e2d9a` |
| Stage 3 discovery file | `8121ea1b1497e4b9bf1fd08e05aeffdf7c28832eecc09ba19c2bea579fc31b71` |
| Selected Stage 4 generation tree | `d7f825fc9279a32d2517531af5b1d009f570586b60dd28d722b299d821349511` |
| Generated Lean project tree | `7bb95897800851c671c8ccafca4035edaa243e556e1a889068848a3903e1111f` |

I also recomputed every individual Stage 1 source hash and checked the exact
file-path set against `stage1_source_hashes`; all match. The input,
generator, export, trust-inventory, obligation-map, selection, provenance,
and pinned-toolchain bindings all match their recomputed values.

The Stage 4 input manifest preserves all eight validated definitions in
canonical order and records no operational rules, proved-derived lemmas, or
domain source rules. Its four summary-function signatures match the frozen
K productions.

The independently classified domain set, `input-manifest.source_rules`,
`obligation-map.source_rules`, `obligation-map.obligations`, and
`obligation-map.trust_parameters` are all exactly `[]`. This is the exact
source-rule/obligation bijection `[] ↔ []`. With no conjuncts, there can be
no omitted, duplicate, irrelevant, weakened, or vacuous conjunct.

The generation-time producer's `target_statement` and
`expected_target_definition` both return `None`; the current trusted checker
independently returns the same. A raw scan finds no `def targetStatement` in
any generated Lean file. `generator-manifest.target`,
`/audit-input.json`'s target, and the fresh preflight target are all `null`.
The generator and export obligation counts are zero, the export status is
`KLEAN_NO_OBLIGATIONS`, and no Stage 5 candidate is mounted.

## Trusted preflight rerun

I directly called `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and these exact arguments:

- frozen input: `/reference/k-proof`
- discovery manifest: `/reference/lemma-discovery.json`
- generation: `/reference/klean-generation`
- toolchain lock: `/reference/klean-toolchain.lock.json`

The checker copied the generated project to a fresh temporary directory,
then ran:

| Command | Exit | Complete result |
|---|---:|---|
| `lake clean` | 0 | no output |
| `lake build` | 0 | all seven generated modules and the root library built; `Build completed successfully.` |

The returned evidence is:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: `null`
- generated tree:
  `7bb95897800851c671c8ccafca4035edaa243e556e1a889068848a3903e1111f`
- Stage 1 tree:
  `d5b755ed0aa090f8d2d4c9daf81edea832cab03696cd4d00be5e304816afad45`
- Stage 3 manifest:
  `8121ea1b1497e4b9bf1fd08e05aeffdf7c28832eecc09ba19c2bea579fc31b71`
- designated sorries: `0`
- trust declarations: `47`, exactly reconciled by preflight with the
  generated allowlist and rejected as proposition trust if proposition-like

The returned document exactly equals the recorded Stage 4 preflight,
including command-output hashes.

The audit container initially exposed a PID namespace without a matching
`/proc` PID view, causing Lean 4.22 to be unable to locate its installed
executable before any project processing. I preserved that raw failure, then
used a small audit-only `LD_PRELOAD` shim that makes `getpid()` return the
parent-visible `Pid` from `/proc/self/status`. This allowed the pinned,
unchanged Lean `4.22.0` commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` to run. The shim was applied
only to audit subprocesses under `/tmp/audit-work`; it did not alter any
mounted input or generated source. Preflight's before/after snapshots
confirmed all immutable inputs stayed unchanged.

## Evidence index

- `evidence/00_context.sh` and `.log`: launcher mode, tool versions, and
  candidate absence.
- `evidence/01_verify_hashes.py` and `.log`: producer, source, tree,
  sidecar, selection, and signed-resolution hashes.
- `evidence/02_verify_inventory.py` and `.log`: complete canonical inventory,
  physical spans, normalized hashes, IDs, order, and Stage 3 bijection.
- `evidence/03_semantics_extract.sh` and `.log`: frozen program, claims, and
  operational K rules used for the classification judgment.
- `evidence/04_preflight_initial_failure.log`: preserved audit-environment
  failure.
- `evidence/04a_hostpid_preload.c`,
  `04a_build_and_test_hostpid_preload.sh`, and `.log`: isolated audit
  environment repair and pinned-toolchain check.
- `evidence/04_run_preflight.py`, `04_run_preflight.sh`,
  `04_preflight.log`, and `04_preflight_return.json`: required trusted
  preflight call, complete subprocess output, and returned evidence.
- `evidence/05_verify_stage4.py` and `.log`: independent classification,
  empty bijection, no-vacuity result, and fixed-null-target checks using both
  the exact generation-time producer and trusted checker.

VERDICT: PASS
LEGITIMACY: LEGIT
