# Independent Stage 3–5 audit: `73-smallest-change`

## Scope and result

The launcher envelope and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for
condition `kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. There is no
`/candidate`, the audit input records no Lean workspace or invocation, and the
selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`. Stage 5 is therefore not
applicable unless the no-obligation decision is mathematically valid.

It is not valid. The protected Stage 3 manifest classifies the sole local
verification rule as `PROVED_DERIVED_LEMMA`, but Stage 1 first proves a
strictly more general claim rather than the exact installed rule. The audit
contract permits `PROVED_DERIVED_LEMMA` only when Stage 1 first proves the
exact same rule. The installed whole-loop summary is consequently a relevant
`DOMAIN_LEMMA`. Stage 4 omits its required obligation and generated target, so
the selected `KLEAN_NO_OBLIGATIONS` status is not legitimate.

## Input and producer integrity

The signed audit-input contract validates with resolved-input digest
`a387b0e2bc1eeca78d5b447f041d27698285f295807f02a708fb9797cf42deac`.
I recomputed every mounted tree hash named by the launcher:

- Stage 1 pipeline tree:
  `d5dd3b76ea2255833efcfb3265c6c5b12e251d1f07c1cb101926cd6d7ed56c63`;
- Stage 1 export tree:
  `e2de8d3edaef3a6a49692aba22ae534680c0215f7f66aed7c30bda3f7d3848bf`;
- Stage 2 audit tree:
  `14f59daea439b1e52fa5fa012e846dd6640a402f51d0c4aea2a869aad02472e1`;
- Stage 3 manifest:
  `78234092b2f8d90141d9c020d9f99d137bd8b91881262054a368bae8a0aa1e8c`;
- Stage 4 generation tree:
  `7f75a095e5d91b04f1a3d1b8b9289f08dcd8d44d8a6447524e852e45df8bdeeb`;
- generated project tree:
  `1351e71bfb566250b9bcb34d0ff8082436842a06feb3cd14093650d0673543b9`;
  and
- generation-producer bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

The machine-readable evidence reports exact equality for all seven recorded
hashes. All 836
individually recorded Stage 1 source paths are present with no extra path and
no hash mismatch.

Before judging Stage 4, I hashed the mounted generation-time sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Both match `generator-manifest.json` and `source-manifest.json`. The producer
bundle contains exactly those two files plus `source-manifest.json`. Its
source manifest and generator manifest both record image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`,
which also matches the immutable image-key path recorded in
`/audit-input.json`. Producer provenance therefore passes; there is no
producer-source `AUDIT_ERROR`.

Raw recomputation is in `evidence/01-producer-authentication.txt` and
`evidence/05-hash-audit.txt`; the reviewer-authored checker is
`evidence/hash_audit.py`.

## Canonical rule inventory and manifest bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` against
the frozen `/reference/k-proof` workspace. `prove.sh` selects module
`VERIFICATION`, and the trusted local module closure is the singleton
`["VERIFICATION"]`. Its reconstructed inventory contains exactly one rule:

- source span: `verification.k:9–56`;
- attributes: `[priority(40)]`;
- normalized source hash:
  `80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791`;
- source identity:
  `rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791`;
- whole inventory hash:
  `8450bb5b555270770633926bc7feda46564197408e95091bf486e6803dd78ca9`.

I independently re-sliced lines 9–56, normalized their whitespace, recomputed
the hash, rebuilt `source_rule_id` as `rule-<hash>`, and recomputed the
canonical inventory hash. Every value agrees with the trusted inventory.

Comparison with `/reference/lemma-discovery.json` is bijective: one canonical
identity and one manifest identity, in the same order, with no duplicate,
unknown, omitted, or extra identity. The manifest inventory hash also agrees.
The structural Stage 3 trust-boundary validator passes. The defect is solely
the semantic classification, not identity or provenance.

The complete reconstructed rule text is in
`evidence/02-reconstructed-rule-inventory.txt`; the frozen sources and
protected manifest are in `evidence/03-source-and-stage3-manifest.txt`; the
independent comparison is in
`evidence/15-classification-and-stage4-audit.txt`.

## Independent classification

The rule recognizes the exact function-frame state at the start of the
submitted `while i < len(arr) // 2` loop, with `changes = 0`, `i = 0`, the
exact `Return(changes) ~> #endcall` continuation, and all remaining
configuration cells pinned. It replaces the entire remaining loop and return
execution with `mismatchCount(VS, 0, halfLen(VS))`, while popping the callee
scope and stack frame.

That operational meaning follows directly from the source and supplied
semantics: `#while` repeatedly evaluates the condition and body; integer
comparison, indexing, unequal comparison, and `AugAssign` implement one
mirrored-pair test per iteration; `Return` records the value; and `#pop`
restores the caller and removes the frame. The relevant frozen semantics are
preserved in `evidence/16-operational-semantics-bridge-context.txt`.

The rule is not a `DEFINITION`: it does not define a summary, recurrence,
macro, or named proof term; it rewrites a live program configuration and
changes control/state cells. It is not an `OPERATIONAL_RULE`: it is a
proof-specific whole-loop shortcut, not an ordinary execution or observation
step of the supplied semantics. It is relevant to both the source program and
the postcondition because its right-hand side is the exact summary returned by
the whole-program target.

The protected rationale calls it `PROVED_DERIVED_LEMMA`, but it also concedes
that the earlier claim **strictly generalizes** the installed rule. The source
diff is material:

- the installed rule fixes `changes = 0` and `i = 0` and returns
  `mismatchCount(VS, 0, halfLen(VS))` under `allInts(VS)`;
- the earlier claim quantifies `C` and `I`, returns
  `C +Int mismatchCount(VS, I, halfLen(VS))`, and adds `0 <=Int I`.

Stage 1 does establish useful independent evidence: `LOOP-CONNECTION`
requires `verification-base.k`, imports `VERIFICATION-BASE`, and neither
contains nor imports the later `VERIFICATION` rule. A fresh compilation of
that bridge-free definition succeeded, and a fresh run of the generalized
claim exited zero with `#Top`. `prove.sh` records that generalized proof before
compiling `verification.k` and using the installed specialization in the
target proof.

This establishes the general mathematical connection but does not satisfy the
audit's stricter classification prerequisite that Stage 1 first prove the
**exact same rule**. Substituting `C = 0` and `I = 0` and then invoking integer
simplification is a corollary argument, not the exact prior claim. The true
classification of the inventory entry is therefore `DOMAIN_LEMMA`. The rule
has no `simplification` attribute, so the separate simplification-class
restriction is not implicated.

The proof order and prior logs are recorded in
`evidence/04-stage1-derived-proof-order.txt`. Fresh compilation and proof
outputs are in `evidence/06-exact-loop-kompile.txt` and
`evidence/08-general-loop-proof.txt`. The exact source-level differences and
import search are in `evidence/17-exact-versus-generalized-rule.txt`. A
reviewer-authored exact specialized claim was also attempted without the
generalized invariant; it timed out after 30 seconds
(`evidence/07-exact-loop-proof.txt`). That attempt is supplemental evidence
only—the classification decision rests on the required exact-statement
comparison, not on a timeout.

## Deterministic Stage 4 generation

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, using
the frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and pinned toolchain lock.

The first invocation exposed an audit-container PID-namespace issue: Lean
4.22 constructs `/proc/<getpid()>/exe`, but this sandbox exposes host `/proc`
while returning a namespace PID, so Lake could not locate its installation.
I diagnosed this independently and compiled a reviewer-authored preload shim
that makes `getpid()` return the host PID visible through `/proc/self`. With
only `LD_PRELOAD` added, pinned Lean reports version 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted
preflight succeeds. This resolved infrastructure condition does not affect
any mounted input or generated hash.

The successful preflight returned:

- status `KLEAN_NO_OBLIGATIONS`;
- zero obligations and no target;
- the exact Stage 1, Stage 3, and generated-project hashes listed above;
- `lake clean` exit 0 with empty output; and
- `lake build` exit 0, output hash
  `3a1ae0b6e2b551a7cfe08c66007047eee025037aa6108dbd9962f0679facecee`,
  ending in `Build completed successfully.`

The initial environment failure is preserved in
`evidence/09-required-klean-preflight.txt`; diagnostics are in
`evidence/10-lake-diagnostic.txt` through
`evidence/12-lake-home-diagnostic.txt`; the successful required result is
`evidence/13-required-klean-preflight-repaired-env.txt`. The shim source and
version check are `evidence/hostpid_shim.c` and
`evidence/18-lean-lake-environment-repair.txt`.

Mechanically, Stage 4 is self-consistent under the protected classification:

- `input-manifest.json` records no `source_rules` and one
  `proved_derived_lemmas` entry;
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters` arrays;
- the obligation-map hash
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
  matches the generator manifest;
- both generator and export manifests record obligation count zero;
- the generated tree contains no `targetStatement` declaration;
- the authenticated producer computes no expected target from that empty
  recorded map;
- `generator-manifest.json`, `export-result.json`, and `/audit-input.json`
  all bind the target to `null`; and
- there are no duplicate obligations, weakened conjuncts, vacuous conjuncts,
  or target substitutions because there are no conjuncts or target at all.

The independent mathematical bijection fails. The true domain set is the
singleton
`rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791`,
whereas the generated obligation identity list is empty. Stage 4 therefore
omits one required obligation and its fixed generated target. Its empty target
is structurally faithful to the incorrect protected manifest but is not a
faithful generated target for the frozen program after independent
classification.

Raw sidecars and generated sources are in
`evidence/14-stage4-manifests-and-generated-tree.txt`. The independent
recorded-versus-true bijection, target count, hashes, and status decision are
in `evidence/15-classification-and-stage4-audit.txt`; its source is
`evidence/classification_stage4_audit.py`.

## Stage 5

Because the recorded and environment modes are `CLASSIFICATION_ONLY`, there
must be no Stage 5 candidate; `/candidate` is absent and the audit input has
null Stage 5 paths and result. No clean candidate build, `Proof.final`, axiom
print, candidate target-shadowing check, or operational-parameter bridge audit
is applicable.

That absence is structurally correct for the selected Stage 4 record, but it
cannot rescue the result: the independently classified domain set is nonempty,
and the audit instructions explicitly make `KLEAN_NO_OBLIGATIONS` illegitimate
in that case.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
