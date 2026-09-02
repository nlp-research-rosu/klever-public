# Independent audit: HumanEval 152-compare

## Result

The Stage 3 classification is complete and mathematically appropriate, and the
selected Stage 4 status `KLEAN_NO_OBLIGATIONS` is legitimate. The independently
reconstructed local rule inventory contains four rules, all four genuinely
define named terms or recurrences, and the true `DOMAIN_LEMMA` set is empty.
Stage 4 consequently has an empty source-rule/obligation bijection, no target
declaration, and no Stage 5 candidate.

The launcher mode is `CLASSIFICATION_ONLY`, matching both `AUDIT_MODE` and the
signed resolution in `/audit-input.json`. No prior verdict or classification
was accepted as authoritative. The mounted `prove.sh`, previous review scripts,
and previous review conclusions were not executed or relied on.

## Frozen input and producer identity

Before judging Stage 4, I hashed the two exact generation-time producer
sources:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

These values match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
sources plus `source-manifest.json`; its independently recomputed tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`. The generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator manifest, and the signed producer-bundle
path in `/audit-input.json` is keyed by that same image digest. There is no
producer-source mismatch or infrastructure `AUDIT_ERROR`.

The audit mechanical-checker lock itself hashes to
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`,
matching the launcher record. Every file named by that lock independently
matches its recorded hash.

The signed Stage 6 resolution digest also recomputes exactly as
`8cf7f6c8050a5b619303bc1cc87b16fc75aaf6ec47e0f07320b96a0778aa079b`.
All resolution hashes and all Stage 1 per-file hashes were independently
checked. Important tree hashes are:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `8b1cddac534c1c5ba7a542ff772a6af369ec50294aebaf0ac260341ee8014994` |
| Stage 1 exporter tree | `1627288e85a21557443477740e3ac9ea9acde56e1d4e14478f12aab470ba73fe` |
| Stage 2 selected audit tree | `ee21ba6428bbd0063ccd9db2b6762c32d694e0e10745a2ced3927e11d956891e` |
| Stage 3 manifest | `c62b55198d0b1f5b855488cbc808d35a769d1ad2b076ea170833ac73e4df72d2` |
| Stage 4 generation tree | `425a5bae743ad7606b5b688aa09fc6acb24d76e6fb3e7557628919502b732f97` |
| Generated Lean project | `b0a1138b86b359bb93dca5a20c88377d37b9eee1d8d75011176e4228a9af7478` |

The generator toolchain object equals
`/reference/klean-toolchain.lock.json`, including Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and K/pyk 7.1.293.

## Independent inventory reconstruction

I ran the locked `tools.k_rule_inventory.inventory_verification` on the frozen
Stage 1 workspace, then independently rechecked every returned physical span,
the whitespace-normalized source text hash, the derived
`rule-<normalized_sha256>` identity, and the canonical JSON inventory hash.

The selected verification module is `VERIFICATION`. Its local module closure
inside `verification.k` is exactly `[VERIFICATION]`; `SEMANTIC` is imported
from the separate frozen `semantic.k`, not another locally defined
verification module. The reconstructed inventory is:

| Span | `source_rule_id` / normalized SHA-256 | Attributes | Independent class |
|---|---|---|---|
| `verification.k:9-28` | `rule-1a31d186612bdc6749d37d6c3da77977158f53c4e73aacb83ebba762c6f45847` | none | `DEFINITION` |
| `verification.k:34-35` | `rule-ae62c27ad3424040225a1c94838f791abd610e6519a372c5656fbe1ebabf000e` | none | `DEFINITION` |
| `verification.k:36-43` | `rule-a4545b542cd0f8ff08024b166bf6bd722fa870b2dc67958768c7594c623b6919` | none | `DEFINITION` |
| `verification.k:44-51` | `rule-0b6e8a0b23d3e6470229df58b00bdcac1c3030a0cc6c9fca317f8aae915af200` | none | `DEFINITION` |

The recomputed whole-inventory hash is
`420faefde3ec2d8bbe14ddc4b8e7750c06010ddc67a860e683a4c930fdcc1036`.
The protected Stage 3 manifest has exactly four entries. Its identities are
unique and occur in exactly the canonical order above. There are no omissions,
duplicates, extras, reordered identities, changed source hashes, or
unaccounted classifications. The locked Stage 3 trust-boundary validator also
accepts the manifest.

## Classification judgment

The classifications follow rule behavior, not comments or names:

1. `solutionProgram` is declared as a total K function of sort `Pgm`, and its
   sole equation expands the name into the exact AST for the frozen source
   function. The AST performs the empty-list return, head subtraction,
   conditional negation, list construction, tail slicing, and recursive call
   found in `solution.py`/`solution.mpy`. This is a named proof term and
   macro-style program definition. It does not rewrite an `execute`, `invokeK`,
   `execK`, `evalK`, continuation, environment, or result configuration.

2. The first `expected` rule defines the empty-`GS` base case as `VNil`.

3. The second `expected` rule defines the negative-difference recurrence:
   prepend the negated head difference and recurse on both tails.

4. The third `expected` rule defines the complementary nonnegative recurrence:
   prepend the direct head difference and recurse on both tails.

The two recursive guards are disjoint and exhaustive once `GS` is nonempty,
and both recursive calls descend through `tailValues(GS)`. Together with the
base case they define the total summary used by the postcondition. On the
prompt domain this is exactly elementwise absolute difference. The totalized
behavior outside the equal-length integer-list domain remains a definition,
not a mathematical assertion.

None of these rules is an ordinary operational execution/observation rule.
None states an independent algebraic or domain fact, and none is a
`PROVED_DERIVED_LEMMA`: there is no earlier proof of the same rule against a
module omitting it followed by later use. The `DOMAIN_LEMMA` set is therefore
genuinely empty. All four rules have no explicit `simplification` attribute, so
the special simplification-class policy is satisfied vacuously.

The frozen operational semantics executes the AST through
`execute -> invokeK -> execK`, evaluates subtraction and the less-than branch,
and recursively invokes `compare` on the two slices. The proof-local
`expected` symbol appears in the destination summary, not in an operational
bridge that replaces source execution. Thus the classification does not hide
a program-derived oracle or execution shortcut.

As an additional independent sensitivity check, I manually compiled the frozen
K sources in a fresh directory and ran `kprove` without executing the mounted
`prove.sh`; the original claim returned `#Top`. A false `ensures 0 ==Int 1`
mutation exited nonzero with `WarnStuckClaimState` and a failed implication.
Separately, changing the source AST's negative branch from negation to identity
made the original property fail. The residual explicitly requires a negative
head difference to equal its negation. This confirms that the proof is
sensitive to the actual source body and that `solutionProgram` is not bypassing
execution.

## Stage 4 obligation and target audit

The Stage 4 input manifest reproduces the four classified definitions exactly
and records empty `operational_rules`, `proved_derived_lemmas`, and
`source_rules`. Independently recomputing the Stage 3 domain set produces the
same empty `source_rules` list.

`generated/obligation-map.json` contains exactly:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

Its file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. Because both sides are empty, the
source-rule/obligation mapping is bijective with no omission, duplicate,
irrelevant obligation, weakened conjunct, or vacuous conjunct.

The generator manifest, signed audit input, stored preflight, and trusted
`target_statement` reconstruction all report `target: null`. An independent
source search finds no `def targetStatement`; `Lemmas.lean` contains only the
empty namespace. Thus the fixed generated target is correctly absent, not
changed or weakened.

The generated project contains 44 allowlisted executable trust-boundary
declarations and no generated proof hole. The trusted preflight independently
matched those declarations to `trust-inventory.json` and rejected proposition
trust. Since there is no obligation and no theorem target, these declarations
do not establish or weaken a Lean proposition.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen K workspace, protected Stage 3 manifest,
selected Stage 4 generation, and pinned toolchain lock.

The first attempt reached the fresh build but exposed a sandbox-specific PID
namespace defect: Lean asks for `/proc/<getpid()>/exe`, while this container's
`/proc` exposes outer rather than inner numeric PIDs. The exact failure is
preserved. I then used a narrow preload shim that changes only a self-executable
`readlink` request to `/proc/self/exe`; its complete C source is preserved in
the evidence directory. It does not alter any K, Lean, manifest, or generated
project file.

With that compatibility fix, the same trusted preflight returned:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- designated sorry count `0`
- trust declaration count `44`
- fresh `lake clean` exit `0`
- fresh `lake build` exit `0`

The clean output hash was the empty SHA-256, and the build output hash was
`24e474f313d51cbca1333dd0ab2e5d1c98f6c3412e90d38b2bbacdf618987602`.
Both exactly match the immutable stored preflight. The trusted checker also
confirmed unchanged snapshots before and after the build.

## Stage 5

Stage 5 is correctly inapplicable. The signed resolution has null Lean
workspace, invocation, result, and target fields; `/candidate` is absent.
Therefore no `Proof.final`, candidate clean build, axiom printout, or
operational-bridge parameter audit is required or possible in this
classification-only case.

## Evidence

Exact commands are recorded in `evidence/COMMANDS.md`. Principal raw results
are:

- `evidence/reconstructed_rule_inventory.log`
- `evidence/verify_inventory_bijection.log`
- `evidence/stage3_manifest_and_trusted_validation.log`
- `evidence/frozen_stage1_sources.log`
- `evidence/verify_all_recorded_hashes_complete.log`
- `evidence/rerun_klean_preflight.log`
- `evidence/lean_toolchain_diagnostics.log`
- `evidence/lean_proc_self_shim.c`
- `evidence/rerun_klean_preflight_with_pid_shim.log`
- `evidence/no_obligations_no_target_no_candidate.log`
- `evidence/independent_kprove_spec.log`
- `evidence/independent_kprove_false_postcondition_ensures.log`
- `evidence/body_mutation_kprove.log`

The mathematical classification, rather than manifest self-consistency alone,
is what makes the zero-obligation result legitimate: every local rule defines a
named term or recurrence, and no true domain lemma is present.

VERDICT: PASS
LEGITIMACY: LEGIT
