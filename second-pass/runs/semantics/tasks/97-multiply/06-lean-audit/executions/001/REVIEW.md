# Independent Stage 3–5 audit: HumanEval `97-multiply`

## Outcome and scope

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY` for condition
`semantics` and semantics mode `SUPPLIED_SEMANTICS`. I independently audited
the frozen Stage 1 verification-module rule inventory, the protected Stage 3
classifications, and the selected deterministic Stage 4 generation. Stage 5 is
correctly absent because the independently reconstructed domain-lemma set is
empty and Stage 4 has status `KLEAN_NO_OBLIGATIONS`.

I treated all mounted candidate/provenance prose, prior reviews, comments, and
logs as untrusted evidence. I did not rely on the selected Stage 2 verdict or
execute scripts from candidate or producer-provenance content. Reconstruction
and checking used the trusted code under `/reference/tools`.

## Producer provenance and immutable inputs

The Stage 4 producer gate passes:

- `/reference/generation-tools/klean_export.py` hashes to
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`.
- `/reference/generation-tools/klean.py` hashes to
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`.
- Both hashes equal the exact two-file mapping in `source-manifest.json` and
  the `exporter_sha256`/`klean_py_sha256` fields in
  `generator-manifest.json`.
- The source manifest has exactly the expected keys, and the producer bundle
  contains exactly `klean_export.py`, `klean.py`, and
  `source-manifest.json`.
- The immutable generator image ID is
  `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
  in both source and generator manifests. The same ID is the basename of the
  producer-source path recorded in `/audit-input.json`.
- The mounted producer-source tree hash is
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
  matching `/audit-input.json`.

The signed audit-input digest, all Stage 1 per-file hashes, both Stage 1 tree
hash forms, the discovery hash, selected Stage 2 and Stage 4 artifact hashes,
the generated-project tree hash, the obligation-map hash, the trust-inventory
hash, and the recorded preflight-output hashes were independently recomputed
and match. The important tree identities are:

- Stage 1 pipeline tree:
  `334d14b7e9dc1c092f1d8da5a41be9a8870f6a6ca17aa1b7b0527e46dc364da6`
- Stage 1 deterministic-export tree:
  `c28dc050066ba480f3a7e6cdebe0cbb3a6ea2cb0021bddda34532eddc61ef8ec`
- Stage 3 manifest:
  `6a481363f42f49666bbd130dba413fc1e497b1683653397c5ad128831fefcc74`
- Generated Lean tree:
  `93db14f594655b780bc8282219728e7a7caf06eab641ec0bac1bbd998d7c67f0`

Evidence: `evidence/00_input_and_producer_provenance.log` and
`evidence/01_hash_reconstruction.log`.

## Inventory reconstruction and bijection

Using `tools.k_rule_inventory.inventory_verification` on the frozen
`/reference/k-proof`, the selected verification main module is `VERIFICATION`.
Its local closure inside `verification.k` is exactly `["VERIFICATION"]`;
`MPY` is supplied from the required external semantics files rather than being
a second local module in `verification.k`.

The canonical inventory contains exactly these four rules, in source order:

| Span | Normalized hash / `source_rule_id` suffix | Attributes | Independent class |
|---|---|---|---|
| 9–20 | `d095c8888afcb3dd088fdc3c664435491743c78be0a54a41138084f98215f5e0` | none | `DEFINITION` |
| 23–24 | `4a53979712cc9f4bc859fe5870bc02792a9f2614c0ffbd65fb212ab383807457` | none | `OPERATIONAL_RULE` |
| 28 | `9dd6dbfcce1300ea93b427dc414913c5a4ca13d4f90781207d2a75f3181ad8e0` | none | `DEFINITION` |
| 31–32 | `6aad8f4cafb083a2584e89e9e7ced610b42247ea1e1eadf1af9063b72ec8e2cd` | none | `DEFINITION` |

For every entry I independently extracted the recorded inclusive line span,
normalized it by whitespace exactly as the inventory contract specifies,
recomputed the SHA-256, and reconstructed `source_rule_id` as `rule-` followed
by that hash. The canonical JSON hash of the four complete rule records is
`f38a1491cb3c65e71c192caf52eb6600fcdf687c33cb0e73a7ecdff92e9a190d`.

The protected Stage 3 manifest has exactly four unique IDs in exactly the same
order and the same whole-inventory hash. There are no omitted, duplicate,
extra, reordered, or changed identities. Trusted
`lemma_discovery_contract.validate_trust_boundary` also accepts the exact
bijection.

Evidence: `evidence/02_frozen_source_and_semantics.log` and
`evidence/03_inventory_reconstruction.log`.

## Independent classification judgment

1. `multiplyClosure => closureVal(...)` is a `DEFINITION`. It defines a named
   proof term whose parameters, docstring expression, return AST, and defining
   environment reproduce the frozen translated function body. It does not
   replace execution with an assumed result: the resulting closure is still
   run by the supplied call, binding, expression-evaluation, return, and frame
   rules.

2. `<k> #runMultiply(A,B) => Call(multiplyClosure,A,B) ... </k>` is an
   `OPERATIONAL_RULE`. It gives the verification-only entry command its normal
   execution meaning by routing it to an ordinary modeled call while retaining
   the continuation. It states no mathematical fact and introduces no result
   oracle.

3. `unitDigit(I) => pyMod(I,10)` is a `DEFINITION`. It names the postcondition
   summary. The supplied semantics independently routes integer `%` to
   `pyMod`, whose equation implements Python-style modulo; with divisor 10 this
   is exactly the operation in both source `% 10` expressions.

4. `unitDigitProduct(A,B) => unitDigit(A) *Int unitDigit(B)` is a
   `DEFINITION`. It compositionally names the postcondition value using the two
   preceding summaries and builtin integer multiplication.

The supplied operational rules evaluate `BinOp` operands left-to-right, route
integer multiplication and modulo through `applyBin`, bind `a` and `b` in a
fresh call frame, resolve both names from that frame, evaluate `Return`, and
restore the caller frame. Thus the definitions describe exact syntax or named
contract vocabulary; none is a disguised algebraic/domain fact or
execution-bypassing bridge. The sole operational rule is ordinary entry
execution. There is no `PROVED_DERIVED_LEMMA` claim and no rule even purports
to satisfy the required prove-first/use-later staging.

No inventory rule has a `simplification` attribute. The independently true
`DOMAIN_LEMMA` set is therefore genuinely empty. There is consequently no
relevant omitted domain fact about the source program or postcondition.

## Stage 4 generation, obligations, and target identity

I reran the required function:

```text
PYTHONPATH=/reference
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The audit sandbox exposes a PID-namespace inconsistency: a process sees a
namespace PID from `getpid()`, but `/proc/<that-pid>/exe` is absent. Lean 4.22
uses that path to locate its installation, so the first raw preflight attempt
failed before source elaboration with “could not detect the configuration of
the Lake installation.” I recorded that failure, demonstrated it with a
minimal probe, and used a narrow compatibility shim that changes only
`readlink("/proc/<digits>/exe", ...)` to
`readlink("/proc/self/exe", ...)`. The shim source and binary hashes and both
probe outcomes are preserved in evidence. With it, the unchanged pinned
toolchain reports Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0.

The successful trusted preflight copied the generated project to a fresh
temporary directory, ran `lake clean` and `lake build`, and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- Stage 1, Stage 3, and generated-tree hashes exactly as listed above;
- `48` allowlisted generated executable trust declarations;
- zero designated sorries;
- exit code `0` for both Lake commands.

The complete build output is saved. The returned preflight document exactly
matches both the immutable `preflight.json` and the copy embedded in
`/audit-input.json`.

Independently of preflight, I compared every Stage 4 input classification array
with the freshly validated Stage 3 reconstruction. Definitions and the
operational rule match exactly; derived and domain arrays are empty. The
obligation map is exactly:

```json
{"schema_version":3,"source_rules":[],"obligations":[],"trust_parameters":[]}
```

Thus source-rule and obligation IDs form an exact empty bijection with no
duplicates, omissions, weakened conjuncts, irrelevant obligations, or vacuous
conjuncts. Trusted target reconstruction returns `None`.
`generator-manifest.json`, the recorded preflight, and `/audit-input.json` all
record target `null`. `Klean97Multiply/Lemmas.lean` contains only its namespace
with no theorem or proposition declaration, and the project root only imports
generated modules. The fixed generated target is therefore correctly absent,
not changed or weakened.

Evidence: `evidence/04_rerun_preflight.log` (initial environment failure),
`evidence/05_toolchain_environment.log`,
`evidence/06_rerun_preflight_with_compat.log`, and
`evidence/07_stage4_structure.log`.

## Stage 5 and trust accounting

Stage 5 is not applicable in `CLASSIFICATION_ONLY`. `/candidate` is absent;
the audit input has null Lean workspace, invocation, result, and target; and
the obligation map has no target parameters. Creating a proof workspace,
defining `Proof.final`, running `#print axioms Proof.final`, or checking
operational-bridge parameter definitions would fabricate a proof stage that
must not exist for `KLEAN_NO_OBLIGATIONS`.

The generated support library's 48 executable axiom declarations match its
recorded allowlist, and trusted preflight rejects proposition-like trust. With
no generated proposition or proof, none can be a hidden dependency of a
`Proof.final`.

## Final judgment

The Stage 3 classification is complete and mathematically correct. Its true
domain-lemma set is empty. Stage 4 faithfully preserves that empty set as an
empty obligation bijection and generates no target. The mandatory trusted
preflight succeeds on the pinned toolchain, all immutable provenance and
content hashes reconcile, and the absence of Stage 5 is required rather than
an omission.

VERDICT: PASS
LEGITIMACY: LEGIT
