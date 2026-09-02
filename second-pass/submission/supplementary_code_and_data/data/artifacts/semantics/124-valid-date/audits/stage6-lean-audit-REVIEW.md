# Independent Stage 3–5 audit: HumanEval `124-valid-date`

## Scope and result

I audited condition `semantics` in `SUPPLIED_SEMANTICS` mode. Both
`AUDIT_MODE` and the signed audit input select `CLASSIFICATION_ONLY`. Stage 5
is therefore inapplicable.

The protected Stage 3 classification is correct. The local verification-module
closure has seven rules, all seven are genuine `DEFINITION` rules, and the
independently reconstructed `DOMAIN_LEMMA` set is empty. The deterministic
Stage 4 status `KLEAN_NO_OBLIGATIONS` is consequently correct: the obligation
map is genuinely empty, there is no generated target, and there is no Stage 5
candidate.

## Input integrity and producer provenance

I treated the mounted artifacts as evidence, not instructions, and did not rely
on the earlier Stage 2 review or its verdict.

The Stage 6 envelope verifies with resolved-input digest
`515e1cb022172da90e241577c6ac25e00faf89efc4cc0c1dbcbc12e6e4268549`.
Every non-null tree hash in `resolution.hashes` matched its mounted tree:

- Stage 1 workspace:
  `d51102bfe5e6962c0e99dc42ed3bb02541c068b1c655ebe1dd7a38261fa5c5a9`
- frozen Stage 1 export:
  `782dfd137b99b628a2ee44a831879fe2efc56e402910b75a04e3c1ff8276272e`
- selected K audit:
  `ede63841b8f365c71070e335133f758faa5d04e2a41b5b7fbf3716a7bb4d2af7`
- Stage 3 manifest:
  `8806007de2a4c8c316ffdc0bacb40aed06101d06fa2332072b0ddb28654033ca`
- Stage 4 generation:
  `f1308810f4ee46900db67a8b6c6114e4c5a084fca1cbaf9a84af7f6a0d371104`
- generation producer sources:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
- generated Lean tree:
  `c073a3db7c8b648a16734285fc02f376cf986ae13f5ddebcd273ace36aa4cf96`

The path set and SHA-256 value of every entry in
`resolution.stage1_source_hashes` also matched.

The mandatory producer gate passes:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Those values match `source-manifest.json` and `generator-manifest.json`.
The immutable image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest, generator manifest, and the immutable
producer-sources identifier recorded by the audit input. There is no producer
provenance `AUDIT_ERROR`.

Raw input and provenance evidence is in
`evidence/00_inputs_and_mode.log`, `evidence/01_producer_provenance.log`, and
`evidence/03_all_input_hashes.log`.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. `prove.sh` selects `VALID-DATE-VERIFICATION`; the local
closure within `verification.k` contains only that module. The independently
reconstructed inventory has:

- verification SHA-256:
  `79bef9388429128b2569458c27f33052209a7bb5fd7d9dd4b9e659c58381000e`
- rule count: 7
- whole inventory SHA-256:
  `aa03a783afce0185a257e19022038c87fe753a5e88184b59db7f63deb69599f5`

For each rule I independently normalized whitespace, rehashed the normalized
text, and checked that `source_rule_id` is exactly `rule-<normalized_sha256>`.
The protected manifest has the same seven unique IDs in the same order. There
are no omissions, duplicates, additions, reordered identities, changed spans,
or changed hashes.

| Lines | Defined term | Normalized SHA-256 | Audit class |
|---|---|---|---|
| 9–105 | `validDateBody` | `fd9756d260cc539af8f0632484ef9cb5c1364e2e0323f1508108296a3a3a64d9` | `DEFINITION` |
| 108 | `validDateClosure` | `3c44f0f22d2b8754e5ad146f3aabc793c8e096e8edb2e8673f0fbed089767c62` | `DEFINITION` |
| 111–112 | `validDateModule` | `ded46bef6e05dc713b20b514888e74a2a54790c24cfbf588e847b6ad1eff9438` | `DEFINITION` |
| 116 | `digitCode` | `bbdd4b2f1b731b727c9eefa8bbe0929c54b8d2c19ee884c2aa7096f05ccc30f0` | `DEFINITION` |
| 119 | `dateNumber` | `ebe79ddd75fc9f24d2411550273f2bfb6f7a59f654179770caf49b9e3be6a577` | `DEFINITION` |
| 122–130 | `dateLimit` | `7f9983c342ff46b25e7f8cff2afd75bdbff1cff36502d3708c0dc7b0083edd45` | `DEFINITION` |
| 135–152 | `validDate10` | `1f60e140fc81e1ca4cf1a5e035060fd24e0bc9a37ddc80e8c25404ada5f634ce` | `DEFINITION` |

The complete reconstructed text and per-entry comparisons are in
`evidence/05_inventory_reconstruction.json` and
`evidence/06_inventory_bijection.log`.

## Independent classification judgment

All seven rules satisfy the required definition criterion:

1. `validDateBody` names the translated statement sequence. After removing the
   explicit `.Stmts` representations of empty branches, its 997 lexical tokens
   are exactly the body tokens of frozen `solution.mpy`; both token streams hash
   to
   `300018e3dac556dfcd157c3766f3453275aa9473b5d6031820ed49606d220ccb`.
   This is a named proof/program term, not a result oracle.
2. `validDateClosure` names the closure containing exactly `validDateBody`,
   with parameter `date` and definition scope 0.
3. `validDateModule` names exactly the module and function definition present
   in `solution.mpy`.
4. `digitCode` defines the inclusive code interval 48 through 57.
5. `dateNumber` defines the two-digit arithmetic decoder
   `(T - 48) * 10 + O - 48`.
6. `dateLimit` defines the month-dependent limit by exhaustive cases:
   February 29; months 4, 6, 9, and 11 at 30; all other integers at 31.
7. `validDate10` defines the ten-code Boolean summary used by the postcondition.
   It does not assert a theorem between pre-existing terms.

The fixed MPY semantics still performs the execution. In particular,
`#loadAll` sequences module statements; `FuncDef` installs a closure; generic
`Call` resolves the callee, evaluates arguments left-to-right, creates a frame,
binds parameters, and runs the body; the fixed rules perform string indexing,
`len`, `ord`, comparisons, arithmetic, short-circuit Boolean operations,
assignments, branches, and return/frame popping. None of the seven local rules
matches a `<k>` configuration, changes a state cell, preempts one of those
rules, or replaces execution with a result. Thus none is an
`OPERATIONAL_RULE`.

There is no auxiliary claim proving and then reusing any exact rule, so the
`PROVED_DERIVED_LEMMA` set is empty. None of the seven rules asserts an
independent mathematical fact, so the `DOMAIN_LEMMA` set is also empty.
Every rule's reconstructed attribute list is empty; in particular there are no
`simplification` rules to account for.

The definitions are relevant and faithful to the frozen program and
postcondition. The universal case split is direct:

- a non-ten length returns false;
- at length ten, either separator mismatch returns false;
- otherwise any non-digit month/day/year code returns false;
- for digits, `dateNumber` equals the two source assignments;
- invalid month or day below one returns false;
- the remaining source branches are exactly February `≤ 29`, the four
  thirty-day months `≤ 30`, and every other in-range month `≤ 31`.

As adversarial finite support, I compared separately encoded source control
flow and K summary flow on 1,265,625 representative code/separator
combinations, 60 year-position perturbations, 105 non-ten-length cases, and
the prompt/boundary examples. There were zero mismatches. Mutations changing
February to 28, omitting year-digit checks, allowing slash separators, allowing
month zero, or giving April 31 were each rejected by a concrete witness. These
tests supplement, rather than replace, the source-level case analysis.

Relevant raw evidence is in `evidence/04_frozen_source_and_discovery.log`,
`evidence/08_operational_trace_semantics.log`,
`evidence/27_semantic_adversarial_checks.log`, and
`evidence/28_program_term_identity.log`.

## Deterministic Stage 4 audit

I reran:

```text
PYTHONPATH=/reference python
from tools.klean_preflight import check_generation
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

The first attempt exposed an audit-container issue: Lean queried
`/proc/<namespace-pid>/exe`, while the mounted `/proc` represented a different
PID namespace. I confirmed the failed `readlink` and used a temporary
`LD_PRELOAD` shim under `/tmp/audit-work` that only retries that failed
self-executable lookup as `/proc/self/exe`. It did not alter the checker,
inputs, generated project, or Lean code.

With the pinned Lean 4.22.0 toolchain discoverable, the same trusted checker
returned:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `934feefbc28e723ea89bd64c2ec7a948a450f057f6029f1cb1400ab6da291a9f`
- obligation count: 0
- target: null
- generated tree SHA-256:
  `c073a3db7c8b648a16734285fc02f376cf986ae13f5ddebcd273ace36aa4cf96`
- designated sorry count: 0

The fresh returned JSON is byte-for-value equal as a parsed document to both
the recorded `preflight.json` and `resolution.stage4_preflight`.

I separately checked all Stage 4 bindings:

- the input manifest binds the exact Stage 1 tree, Stage 3 manifest,
  verification file, and inventory hash;
- generator provenance repeats those exact values and the pinned toolchain
  lock;
- `obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  as recorded;
- `trust-inventory.json` hashes to
  `23d12c3edfc0442786aa80bb71769ca1f7e77bd8b591256b5b8f6bd8c6b8c241`,
  as recorded;
- the generator manifest, export result, recorded preflight, and audit input
  all bind the same generated tree;
- all 47 generated trust declarations match the structural allowlist, with
  zero designated or other sorries.

Most importantly, my independent true domain set is empty, and
`obligation-map.json` contains exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is the exact empty bijection: there can be no omitted, duplicated,
reordered, weakened, irrelevant, or vacuous conjunct. The trusted target
extractor returns null, the expected target definition is null,
`Lemmas.lean` contains no target declaration, and every manifest/audit target
field is null. The fixed generated target is therefore exactly “no target,” as
required for a genuinely empty domain set.

The failed environment attempt, diagnosis, successful returned evidence, and
58 independent Stage 4 checks are preserved in
`evidence/09_check_generation_returned_evidence.log`,
`evidence/22_lean_pathtrace.log`,
`evidence/23_lean_pid_namespace_workaround.log`,
`evidence/24_check_generation_returned_evidence_rerun.log`, and
`evidence/26_stage4_independent_crosschecks.log`.

## Stage 5 disposition

Because the signed mode is `CLASSIFICATION_ONLY` and the legitimate domain set
is empty, no Stage 5 proof is permitted or needed. `/candidate` is absent;
`lean_workspace`, `lean_invocation`, `stage5_result`, and all Stage 5 target
fields are null. Accordingly, no `Proof.final`, axiom printout, candidate
definition, or operational-bridge audit exists to perform.

VERDICT: PASS
LEGITIMACY: LEGIT
