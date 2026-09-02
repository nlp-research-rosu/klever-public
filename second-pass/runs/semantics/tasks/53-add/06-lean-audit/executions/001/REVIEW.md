# Independent Stage 3–4 Audit: HumanEval `53-add`

## Scope and audit mode

This review independently audits the Stage 3 lemma classification and selected
deterministic Stage 4 generation for condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`.

The launcher and environment both record `CLASSIFICATION_ONLY`. The signed
resolution has no Lean workspace, no Lean invocation, no Stage 5 result, and no
target. `/candidate` is absent. Therefore the conditional Stage 5 build,
`#print axioms Proof.final`, proof-identity audit, and parameter operational
bridge audit do not apply.

All mounted candidate/provenance prose, prior verdicts, logs, and comments were
treated only as untrusted evidence. The prior Stage 2 conclusion was not used
as authority.

## Inventory reconstruction and manifest bijection

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation over
the frozen `/reference/k-proof`. The selected main module is
`ADD-VERIFICATION`; its local verification-module closure contains only that
module.

The reconstruction found exactly one local rule:

- module: `ADD-VERIFICATION`
- source span: `verification.k` lines 9–16
- attributes: none
- normalized source SHA-256:
  `421e63465e293edfd877e4482b1842e53422f4b5589c6d1a5f54e9d264066aa8`
- source rule ID:
  `rule-421e63465e293edfd877e4482b1842e53422f4b5589c6d1a5f54e9d264066aa8`

The frozen `verification.k` SHA-256 is
`912fefa77063687e87e6018d770c7e2d04b76f3c18ceda3ca14385b3be927a9d`.
Recomputing the normalized hash directly from the recovered text reproduced
both the rule hash and `source_rule_id`. Recomputing the canonical inventory
hash produced
`7f6dfa07ad90e336bc3ed6929c273b3f264e3f0cce73bda711e0b3dba9d13b06`.

The protected discovery manifest contains exactly that one ID, in that order,
and the same inventory hash. Both inventories have unique IDs. Thus there are
no omissions, duplicates, extras, reordered identities, changed hashes, or
unclassified entries. The trusted
`lemma_discovery_contract.validate_trust_boundary` check independently
accepted the same inventory binding.

Evidence:

- `evidence/02_reconstructed_inventory_and_discovery.txt`
- `evidence/24_inventory_bijection_verification.txt`
- `evidence/verify_inventory_bijection.py`

## Independent classification judgment

The sole rule introduces the proof-harness term `#callAdd(X, Y)` and expands it
to:

1. `#loadAll` of the exact translated module containing
   `def add(x, y): return x + y`; then
2. an ordinary `Call(Name("add"), Int(X), Int(Y))`; then
3. the pre-existing continuation, preserved by the `<k> ... </k>` frame.

The normalized `solution.mpy` module occurs exactly once in the rule, and the
parsed Python source independently confirms the same two-parameter function
and `x + y` body.

Under the supplied operational semantics, the expansion does not compute or
assume the result. `#loadAll` exposes the statements; `FuncDef` installs a
closure; `Call` performs ordinary callee lookup and left-to-right argument
evaluation; the closure rule creates a frame; `#bindP` binds `x` and `y`; the
body evaluates `Name("x")` and `Name("y")`; generic `BinOp` dispatch reaches
the integer rule `applyBin("+", I1, I2) => I1 +Int I2`; and `Return`/`#pop`
restores the caller frame. The rule therefore adds a name for an exact proof
entry configuration and leaves the source body to execute.

This is a `DEFINITION`: specifically, a macro/named proof-term expansion. It is
not an `OPERATIONAL_RULE`, because it does not model an ordinary source
operation or observation and does not replace a supplied-semantics execution
step. It is not a `DOMAIN_LEMMA`, because it states no mathematical fact such
as the result of addition. It is not a `PROVED_DERIVED_LEMMA`, and Stage 3 does
not claim it as one.

There are no `[simplification]` rules in the reconstructed local closure, so
the requirement that every simplification be a `DEFINITION` or
`DOMAIN_LEMMA` is satisfied. The independently classified domain-lemma set is
genuinely empty.

A counterfactual rule rewriting `#callAdd(X,Y)` directly to `X +Int Y`, or
replacing the `Call` with a precomputed value, would change this judgment by
skipping the frozen function execution. The actual rule does neither.

Evidence:

- `evidence/03_frozen_sources_and_relevant_semantics_index.txt`
- `evidence/04_operational_semantics_sources.txt`
- `evidence/25_problem_contract_and_tests.txt`
- `evidence/27_source_to_harness_identity.txt`
- `evidence/28_harness_usage_and_rule_attributes.txt`

## Stage 4 producer provenance

The generation-time producer-source gate passes:

- mounted `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- mounted `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Those hashes equal the values in both `generator-manifest.json` and
`source-manifest.json`. The complete mounted producer-source tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
equal to `/audit-input.json`.

The generator image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest and source manifest; the launcher binds the same
identity in the basename of its immutable producer-source path. There is no
producer-source infrastructure error.

Evidence:

- `evidence/05_producer_provenance.txt`
- `evidence/26_producer_provenance_recheck.txt`
- `evidence/verify_producer_provenance.py`

## Stage 4 hashes, obligations, and fixed target

I verified the signed-resolution digest and every launcher-recorded mounted
hash. The observed values exactly equal the recorded values for:

- Stage 1 workspace tree:
  `03f83b5037276ec8e5f69eee6416e0fab73f8fb3a3d6501e62f3aa2d1cedcb60`
- Stage 1 deterministic-export tree:
  `bac90f6443f9d14a888b99f0eb504010d905c2f2e38fb135c1c2462e4d8e4d31`
- discovery manifest:
  `7000dba0b468cc6c84428619f7e2d9b6dde1684d49fca99f909b2f7910158315`
- selected Stage 2 tree:
  `b9374c0b3eaf14e399583daeacff4135350c7615c13c1df37ebf7f28bd0667e0`
- selected Stage 4 generation tree:
  `d4a58d874e4b34b8e78118d3bc7064fc47f61feb210e38fd821b4c66d277caeb`
- generated project tree:
  `3238cfc5cef04c46c7b69c40aa12ba213ce036450e79f1686232f7512d87c958`
- producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`

All 33 individually recorded Stage 1 source paths and hashes match exactly,
with no missing or extra files. Both selected-artifact hashes match their
mounted trees. The obligation-map hash and trust-inventory hash match their
manifests. The audit input's stored Stage 4 preflight document exactly equals
the selected generation's `preflight.json`; because both stored command
outputs are shorter than the 4000-character tail limit, independently hashing
their stored output reproduces both diagnostic hashes.

The independently classified domain set, the input-manifest `source_rules`,
the obligation-map `source_rules`, and the obligation `source_rule_id` list are
all exactly `[]`. The obligation IDs are unique, and the generator manifest,
export result, and actual map all record count zero. Hence the
source-rule/obligation bijection is exact and empty—not the result of an
omission or reclassification mismatch.

`klean_export.expected_target_definition` returns `null`, and
`klean_export.target_statement` finds no target declaration. The generator
manifest, Stage 4 preflight record, and signed audit input also all bind
`target: null`. `Klean53Add/Lemmas.lean` contains only its namespace and no
theorem. With no domain obligations, there is no conjunct to weaken, duplicate,
make vacuous, or replace.

The generated base project contains 47 allowlisted non-propositional Klean
trust declarations and no `sorry`; the fresh preflight independently matches
all 47 declarations to the trust inventory and rejects proposition trust.
Because there is no generated proposition or Stage 5 proof in this mode, these
declarations are not dependencies of a claimed final theorem.

Evidence:

- `evidence/21_obligation_target_and_trust_artifacts.txt`
- `evidence/23_hashes_and_bijection_verification.txt`
- `evidence/verify_hashes_and_bijection.py`

## Fresh mechanical preflight

I directly invoked
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected discovery manifest, selected Stage 4
generation, and pinned toolchain lock.

The first invocation reached `lake clean` but exposed a sandbox infrastructure
quirk: Lean resolves its executable through `/proc/<pid>/exe`, while this audit
PID namespace exposes the process executable only through `/proc/self/exe`.
This made unmodified Lean report that it could not locate its application and
made Lake report that it could not detect its installation. `unshare
--mount-proc` is disallowed.

I used a recorded, narrowly scoped `LD_PRELOAD` compatibility shim that changes
only numeric `/proc/<pid>/exe` `readlink` requests to `/proc/self/exe`.
Its source SHA-256 is
`3ab5249e161724488ef389050a8542852e67e54236a243588853c74e1bf7704a`.
With that sandbox-path correction, Lean reports version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the pinned
toolchain.

The rerun returned:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, all generated modules built
- frozen input:
  `bac90f6443f9d14a888b99f0eb504010d905c2f2e38fb135c1c2462e4d8e4d31`
- discovery:
  `7000dba0b468cc6c84428619f7e2d9b6dde1684d49fca99f909b2f7910158315`
- generated tree:
  `3238cfc5cef04c46c7b69c40aa12ba213ce036450e79f1686232f7512d87c958`
- obligations: 0
- target: `null`
- designated sorries: 0
- trust declarations: 47

The fresh parallel build listed `Func` and `Lemmas` in the opposite completion
order from the stored generation-time build, so its log hash differs. This is
only scheduling order in command output: the immutable generated tree hash and
all semantic/structural results are identical. The trusted preflight also
resnapshotted the immutable inputs after the build and accepted them unchanged.

Evidence:

- `evidence/08_fresh_klean_preflight.txt`
- `evidence/09_toolchain_diagnosis.txt`
- `evidence/14_proc_exe_probe.txt`
- `evidence/18_pid_namespace_probe.txt`
- `evidence/19_lean_proc_shim_build_and_probe.txt`
- `evidence/20_fresh_klean_preflight_with_pid_shim.txt`
- `evidence/lean_proc_exe_shim.c`

## Judgment

The protected Stage 3 classification is mathematically and operationally
correct. The only rule is an exact named proof-term definition, not a hidden
domain lemma or execution shortcut. Consequently the true domain-lemma set is
empty.

The selected Stage 4 `KLEAN_NO_OBLIGATIONS` status faithfully represents that
empty set. Producer provenance, all input and artifact hashes, the empty
source-rule/obligation bijection, and the absence of a generated target all
check out. No Stage 5 candidate is permitted or present in the recorded audit
mode.

VERDICT: PASS
LEGITIMACY: LEGIT
