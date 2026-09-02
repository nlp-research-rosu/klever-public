# Independent Stage 3–5 audit: HumanEval `53-add`

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`.
Both `AUDIT_MODE` and `/audit-input.json` record
`CLASSIFICATION_ONLY`.  This is the correct mode for the selected Stage 4
status only if the independently reconstructed domain-lemma set is empty.

I treated the mounted workspaces, manifests, logs, comments, and earlier
reviews only as untrusted evidence.  I did not adopt the selected Stage 2
verdict or the protected Stage 3 classification.  The conclusions below come
from the frozen sources, the trusted inventory/preflight implementations, and
fresh hash and build checks.

Result: the Stage 3 empty classification is correct, Stage 4 is a structurally
and mathematically legitimate `KLEAN_NO_OBLIGATIONS` generation, and Stage 5
must not run.  No concern changes that result.

## Audit mode and immutable inputs

The environment and launcher resolution both say `CLASSIFICATION_ONLY`.
`/candidate` does not exist.  The launcher records null Stage 5 workspace,
invocation, result, and hashes.  The mounted copy
`/audit-output/audit-input.json` is byte-identical to `/audit-input.json`.

Fresh trusted hashing reproduced every launcher-recorded resolution hash:

| Input | Recomputed SHA-256 | Judgment |
|---|---|---|
| Stage 1 workspace tree | `9941be0c0148107fb6e87969b13e54e390fea33d7b88ed2a7190917050db522f` | match |
| Stage 1 export tree | `83352aaa33d3f483a98c364b050b18881df5ed48589880b777ad82658502ac92` | match |
| Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` | match |
| selected Stage 2 tree | `9ea744831b6d9c778b2342e4d7fcd3fc6ba86f51f645948235df45bb1a537c9b` | match |
| selected Stage 4 tree | `008dd96416052c93badddaef2f61079a961397376b6dcaec84003928fc838535` | match |
| producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | match |
| generated project tree | `8ef454ff00df5d090556c003ff9480e6a5e10c127905a759c7e5bcea0904dd5a` | match |
| Stage 5 workspace/invocation | null / null | match |

All 772 individual Stage 1 file hashes recorded by the launcher were also
recomputed: there were no missing, extra, or changed files.  The Stage 2 and
Stage 4 selection artifact hashes match their mounted trees.  Cross-file
bindings among the input manifest, generator manifest, export result,
published preflight, and launcher record all match.  See
`evidence/12-integrity-check.log`.

## Generation-time producer provenance

I checked this before judging the Stage 4 content.  The mounted producer files
have these hashes:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Those hashes exactly equal both the generator-manifest fields and the file map
in `source-manifest.json`.  The immutable generator image identifier is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest and source manifest.  The launcher-recorded producer
directory has the same digest as its final path component.  The producer
bundle contains the expected source manifest and its whole-tree hash also
matches the launcher.  There is therefore no producer-provenance
`AUDIT_ERROR`.  Raw evidence is in `evidence/01-producer-provenance.log`.

## Independent rule-inventory reconstruction

The frozen `verification.k` is only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

Using `/reference/tools/k_rule_inventory.py`, the selected verification module
is `VERIFICATION` and the local module closure inside `verification.k` is the
single module `["VERIFICATION"]`.  `MPY` is supplied semantics defined in the
required semantics files; it is not a proof-local module defined by
`verification.k`.

The reconstructed inventory is:

- `verification_sha256`:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- rules: `[]`;
- canonical inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

Thus there are no rule spans, normalized rule hashes, or `source_rule_id`
values to omit or alter.  The protected Stage 3 manifest also has exactly the
ordered list `[]` and exactly the same canonical inventory hash.  Counts and
sets establish an ordered bijection: zero canonical IDs, zero manifest IDs,
and no duplicates, extras, omissions, changed hashes, or reordered identities.
The trusted Stage 3 contract validation also returns zero definitions, zero
operational rules, zero proved-derived lemmas, and zero domain lemmas.  See
`evidence/02-rule-inventory.log`.

## Independent classification and mathematical judgment

Every inventory entry was reclassified independently; because the canonical
inventory is empty, each classification category is genuinely empty.  In
particular, there are no local `[simplification]` rules and no opportunity to
mislabel a simplification as an operational or proved-derived rule.  There is
also no Stage 1 sequence that could purport to prove and later import a derived
rule.

The empty domain-lemma set agrees with the actual program and claim, rather
than merely with the manifests.  The frozen source is:

```python
def add(x: int, y: int):
    return x + y
```

The K claim loads that exact translated function, calls its module binding on
arbitrary K integers `X` and `Y`, and requires the returned value to be
`X +Int Y`.  No precondition narrows the inputs.

The supplied operational semantics already provides the entire computation:
module loading installs the closure; name lookup selects that closure;
ordinary call evaluation creates a frame and binds `x` and `y`; sequentially
strict `BinOp` evaluation dispatches to `applyBin`; and the fixed integer rule

```k
rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2
```

produces exactly the claimed value before the ordinary return/pop rules restore
the caller state.  No summary, recurrence, mathematical property, execution
bridge, or postcondition lemma is needed.  Consequently there is no relevant
domain fact that Stage 3 failed to expose.  The exact source, claim, and fixed
semantic rules are recorded in `evidence/13-source-semantics-trace.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`, `/reference/klean-generation`, and the
pinned `/reference/klean-toolchain.lock.json`.

The sandbox initially exposed an infrastructure quirk: `getpid()` and the
mounted `/proc/<pid>` namespace disagree, while Lean 4.22 discovers its binary
through `/proc/<getpid()>/exe`.  The failed attempts were preserved in
`evidence/03-check-generation.log` through
`evidence/09-check-generation-configured.log`.  A direct C probe shows the
numbered proc path fails with `ENOENT` while `/proc/self/exe` succeeds.  I used
a narrow preload shim that changes only numbered `/proc/<digits>/exe`
`readlink` requests to `/proc/self/exe`; its source, build hashes, probe, and
the resulting Lean version/commit are in
`evidence/10-proc-compat-probe.log`.  It does not alter the generated sources,
compiler, theorem statements, or proof logic.

With that procfs compatibility fix, the exact trusted preflight completed:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all nine build steps completed;
- returned status: `KLEAN_NO_OBLIGATIONS`;
- frozen input hash:
  `83352aaa33d3f483a98c364b050b18881df5ed48589880b777ad82658502ac92`;
- discovery hash:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`;
- generated tree hash:
  `8ef454ff00df5d090556c003ff9480e6a5e10c127905a759c7e5bcea0904dd5a`;
- obligation count: 0;
- target: null;
- designated sorries: 0;
- generated trust declarations: 41, exactly reconciled with the generated
  trust inventory.

Complete successful command output and the returned JSON are in
`evidence/11-check-generation-pass.log`.

## Source-rule/obligation bijection and fixed target

The independently classified domain IDs, Stage 4 input-manifest source IDs,
obligation-map source IDs, and obligation IDs are all the same ordered set:
`[]`.  Each list is duplicate-free.  Obligation count zero agrees across the
generator manifest, export result, published preflight, fresh preflight, and
launcher record.  The obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest.

The generation-time target parser returns null, the deterministic expected
target definition is null, and the generator manifest, published preflight,
and launcher all record null.  An independent scan found no target-like Lean
declaration.  There are therefore no omitted, duplicated, weakened,
irrelevant, or vacuous conjuncts and no target change: there are no conjuncts
and no generated theorem at all.

Because the true domain-lemma set is independently empty, this is precisely
the case in which `KLEAN_NO_OBLIGATIONS` is legitimate.

## Stage 5 and trust boundary

Stage 5 is not applicable in `CLASSIFICATION_ONLY`.  There is no candidate,
no generated target theorem, no `Proof.final`, and no target parameters.
Accordingly a clean candidate copy, candidate token scan, `#print axioms
Proof.final`, proof-identity comparison, and operational-bridge parameter
audit would be category errors rather than omitted checks.  The required
absence of all Stage 5 artifacts was verified.

The generated project contains 41 allowlisted collection-hook axioms, exactly
as recorded by `trust-inventory.json`, but with no generated proposition and
no Stage 5 proof they cannot discharge or weaken an obligation.  The trusted
preflight independently rejects proposition trust and reconciled all 41
declarations.  This does not create a proof trust escape because there is no
Lean proof target in this run.

## Evidence index

- `evidence/00-context.log`: audit mode and mounted-input summary.
- `evidence/01-producer-provenance.log`: producer file, bundle, and image-ID
  checks.
- `evidence/02-rule-inventory.log`: full reconstructed inventory and Stage 3
  bijection.
- `evidence/03-check-generation.log`–`evidence/10-proc-compat-probe.log`:
  preserved preflight diagnostics and procfs root-cause evidence.
- `evidence/11-check-generation-pass.log`: complete successful trusted
  preflight rerun and returned evidence.
- `evidence/12-integrity-check.log`: all launcher hashes, 772 per-file hashes,
  manifest bindings, obligation bijection, and target identity.
- `evidence/13-source-semantics-trace.log`: frozen source, formal claim, and
  load/call/bind/add/return operational rules.
- `evidence/run_logged.sh`, `evidence/run_preflight.py`,
  `evidence/integrity_check.py`, `evidence/app_path_probe.c`, and
  `evidence/proc_exe_compat.c`: exact evidence-producing helpers.

VERDICT: PASS
LEGITIMACY: LEGIT
