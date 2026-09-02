# Independent Stage 3–5 Audit: `122-add-elements`

## Scope and audit mode

I audited HumanEval problem `122-add-elements`, condition `kit-semantics`, with supplied K semantics. The authenticated launcher input verifies as schema 4 and records:

- `mode = CLASSIFICATION_ONLY`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `target = null`
- `stage5_result = null`

The canonical resolution digest returned by the trusted audit-input verifier is `268a456e0fe3c1d0fdaca5718ea9554e3c23d0f0f94ac8be03f2d671589d5800`. I treated the selected Stage 2 review, saved logs, comments, manifests, and mounted source text as evidence rather than authority. No earlier verdict or classification was adopted.

## Producer-source gate

I hashed the two mounted generation-time producer files before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These values match both `generator-manifest.json` and `generation-tools/source-manifest.json`. Both manifests name generator image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`, and that digest is also the terminal component of the producer-source path authenticated by `/audit-input.json`. The launcher-style observed producer-bundle hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly the audit-input value. The source bundle contains precisely the source manifest and the two named producer files. The generator's toolchain object also equals `/reference/klean-toolchain.lock.json`.

This gate passes; there is no missing or mismatched producer-source infrastructure error. Raw results are in `evidence/18-producer-provenance-bijection.txt`.

## Frozen-input and inventory reconstruction

All 823 launcher-recorded Stage 1 file hashes match the 823 regular files mounted at `/reference/k-proof`; there are no missing, extra, or mismatched files. The launcher-style tree hashes also match for the Stage 1 workspace, selected Stage 2 audit, selected Stage 4 generation, and producer bundle. The export-style Stage 1 and generated-project tree hashes match their separately recorded fields.

Using `tools.k_rule_inventory.inventory_verification` with `PYTHONPATH=/reference`, I reconstructed the local verification-module closure from the frozen `verification.k`. The trusted algorithm selected module `VERIFICATION`; its local closure contains that one module. `VERIFICATION-BASE` is in an externally required frozen file and is not a locally declared module in `verification.k`, so it is not an additional entry under this inventory definition.

The reconstruction is:

| Field | Reconstructed value |
|---|---|
| `verification_sha256` | `a55217898161b9ae2701457a7a17e1b695095f74a70e6fc26664b6fa458de5f8` |
| rule count | 1 |
| module | `VERIFICATION` |
| source span | lines 10–64 |
| attributes | `priority(30)` |
| normalized SHA-256 | `af419f60f77e409fe9d74f8499c04f5bc5e7c6463972156d45ed7a152331ad03` |
| `source_rule_id` | `rule-af419f60f77e409fe9d74f8499c04f5bc5e7c6463972156d45ed7a152331ad03` |
| whole inventory SHA-256 | `3eb2050e8c9cec58287e26ab1c6d749f2c97c11af0a4174a42cc5e77f4f8421a` |

The protected Stage 3 document has exactly that one identity, exactly once and in the same order, and the same whole-inventory hash. There are no omitted, duplicated, extra, reordered, or changed rule identities. The full reconstructed source span and metadata are in `evidence/02-reconstructed-rule-inventory.txt`; the frozen source is in `evidence/03-frozen-program-and-proof-sources.txt`.

## Independent classification judgment

The sole rule is correctly classified `PROVED_DERIVED_LEMMA`.

It is not a definition: its left side is the exact operational `#loop` configuration followed by `Return(Name("total"))` and `#endcall`, and its right side is the resulting integer summary. It is not an ordinary supplied-semantics operational rule: it is a proof-local acceleration of a complete loop/call return. It is not an assumed domain lemma: Stage 1 states and proves the same reachability relation against `VERIFICATION-BASE`, which does not contain the reusable rule, before compiling the rule into `VERIFICATION` and using it in the final proof.

The reusable rule's entire configuration, rewrite, guards, and state updates are byte-identical to `LOOP-SPEC.loop-connection` after excluding only the K sentence header/claim label and the reusable rule's scheduling attribute; the body comparison exits 0 with an empty diff. The reusable rule has no `simplification` attribute, so the restriction that simplification rules be definitions or domain lemmas is satisfied vacuously for this inventory.

I independently reran the proof sequence from frozen source with fresh Haskell definitions under `/tmp/audit-work`:

1. Compile `verification-base.k` as `VERIFICATION-BASE`.
2. Prove `loop-spec.k` against that base-only definition: `#Top`.
3. Compile `verification.k` as `VERIFICATION`.
4. Prove `spec.k` against the extended definition: `#Top`.

The combined command exited 0 and contains two `#Top` results (`evidence/05-fresh-stage1-derived-and-downstream-proof.txt`). Thus the connection is established without importing the later rule, and the later theorem genuinely reuses the proven summary.

The classification also agrees with the supplied operational semantics and source program:

- `For` lowers to `#loop`; list iteration consumes one `vCons` at a time in order.
- Each iteration binds `element`, first tests `remaining == 0`, and propagates `Break` through the exact loop label.
- Integer comparison dispatch implements `>= -99` and `<= 99`; guarded augmentation updates `total`; `remaining` is then decremented.
- `Return` sets the return value, pops precisely the framed call, restores the caller environment, and removes the callee scope.
- `qualifyingPrefix` is a terminating recurrence: it returns zero at nonpositive length or sequence exhaustion and otherwise adds exactly the head when it lies in `[-99, 99]`, then recurs with `N - 1`.

These facts match the frozen source contract: sum the values with at most two decimal digits among the first `k` integer elements. The rule's `allInts(VS)`, `0 <= N`, and `N <= vsLen(VS)` guards are relevant and cover the loop states reached under the entry theorem. Its continuation, frame, bindings, heap, return, exception, exit-code, environment, scope, and allocation cells match the bridge-free claim; it does not generalize over an unjustified trailing continuation.

As adversarial checks, the fixed-semantics and summary-enabled boundary witness `[99, -100, 7]`, `N = 2`, initial sum `5` both prove result `104`. Changing the program upper bound from 99 to 98 while retaining the summary is rejected with a stuck residual exposing the boundary discrepancy. Changing the final result to `qualifyingPrefix(INPUT, K) + 1` is also rejected. Both mutations exit 1 (`evidence/21-semantic-witnesses-and-counterfactuals.txt`).

Therefore the independently classified true `DOMAIN_LEMMA` set is empty. The sole rule is source-relevant and operationally derived, not an irrelevant or disguised mathematical assumption.

## Stage 4 hash, bijection, and target audit

The following independently observed values match every corresponding Stage 4 sidecar and audit-input resolution field:

| Artifact | SHA-256 |
|---|---|
| Stage 1 export tree | `5818822dd76233b839cc6ccfb2c40e744ae84769acedaf3a5da5864318a4170f` |
| protected Stage 3 manifest | `43a220c69f6ce584cc600d4e24fc15c116f759fdba406371e9536fab35d870ec` |
| generated project tree | `bbddd84540fc6c2414677d8fe43951b0e61cc0328cf8d701e864b0b87352388d` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `6b7f2b23b0620aa595e7f7fab3946aafc66e8299dcc9048b64a187a695bf6df0` |

The independent source/obligation reconciliation is exact and ordered:

- independently classified domain-rule IDs: `[]`
- input-manifest `source_rules`: `[]`
- obligation-map `source_rules`: `[]`
- obligation-map `obligations`: `[]`
- obligation-map `trust_parameters`: `[]`
- generator and export obligation counts: `0`

There are no omitted, duplicated, extra, weakened, irrelevant, or vacuous conjuncts because there are no legitimate domain obligations to generate. The fixed generated target is `null` in the generator manifest and audit input, the trusted target parser returns `None`, and no generated Lean file contains `targetStatement` or `Proof.final`. The complete independent reconciliation reports every comparison true in `evidence/20-independent-stage4-reconciliation.txt`.

I reran `tools.klean_preflight.check_generation` with the required frozen workspace, protected Stage 3 manifest, selected Stage 4 generation, `PYTHONPATH=/reference`, and the pinned toolchain lock. Its successful returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- unchanged Stage 1, Stage 3, and generated-project hashes
- `lake clean` exit 0
- `lake build` exit 0 with `Build completed successfully.`
- designated sorry count `0`

The first invocation exposed a sandbox-only Lean launcher failure: Lean 4.22 reads `/proc/<getpid>/exe`, while this PID namespace exposes only `/proc/self/exe`. I diagnosed this before assigning any verdict and used the narrow audit-local preload shim in `evidence/lean_app_path_shim.c`, which redirects only those executable-path readlinks. It changes no mounted input or Lean semantics. With the shim, the same pinned Lean commit reports correctly, a separate recovery build succeeds, and the required unchanged trusted checker returns the same build-output hash as the recorded Stage 4 preflight. The failed invocation, diagnosis, shim source/hash, recovery build, and successful checker output are preserved in `evidence/10-fresh-check-generation.txt` through `evidence/16-fresh-check-generation-success.txt`.

Finally, the trusted `klean_final_gate.py` returned `PASS` in `CLASSIFICATION_ONLY` mode, with the authenticated resolution digest, all bound input hashes, `KLEAN_NO_OBLIGATIONS`, target `null`, candidate hash `null`, and no used axioms. That gate intentionally reports semantic classification as `NOT_EVALUATED`; the independent semantic classification supporting the verdict is the analysis above. Its full result is in `evidence/22-trusted-final-gate.txt`.

## Stage 5 disposition and conclusion

Because the authenticated mode is `CLASSIFICATION_ONLY` and the independently classified domain set is genuinely empty, `KLEAN_NO_OBLIGATIONS` is the correct Stage 4 result. `/candidate` is absent, there is no Stage 5 result, and there is no generated target theorem. A clean-build copy, `#print axioms Proof.final`, candidate target-shadowing audit, and operational-bridge audit of target parameters are therefore inapplicable: no `Proof.final`, target, parameter, or proof candidate exists to inspect. This is exactly the required no-obligation shape, not a missing proof for a nonempty domain set.

The Stage 3 classification is complete and mathematically sound; the deterministic Stage 4 generation is provenance-correct, hash-correct, bijective, and target-preserving; and the absence of Stage 5 is required by the valid empty-domain classification.

VERDICT: PASS
LEGITIMACY: LEGIT
