# Independent audit: HumanEval `148-bf`, `bare`, `GENERATED_SEMANTICS`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, and
`/audit-input.json` independently records the same mode. The Stage 5 fields
are null and `/candidate` is absent. Accordingly, this review audits the
Stage 3 classification and deterministic Stage 4 generation. The proof-mode
candidate copy, `Proof.final` axiom print, candidate target identity, and
candidate operational-bridge checks are not applicable.

I treated the mounted K audit, prior reviews, logs, comments, classifications,
and generated files only as untrusted evidence. I did not adopt the earlier
Stage 2 verdict or the Stage 3 classification as an authority.

## Generator-source authentication

Authentication was completed before judging the Stage 4 output:

| Item | Recomputed SHA-256 | Recorded agreement |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | Source manifest and generator manifest |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | Source manifest and generator manifest |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` | Audit input |

The source manifest and generator manifest both identify generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The digest component is also the final path component of the immutable
producer-source path recorded in the audit input. Producer authentication
therefore passes; there is no infrastructure `AUDIT_ERROR`.

## Frozen-input and inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. It selected `VERIFICATION` as the verification module,
with local closure `["VERIFICATION"]`, and reconstructed exactly one rule:

- Source span: `verification.k:10-12`
- Normalized text:
  `rule <k> verifyBF(P1, P2) => solutionProgram ~> invokeBF(P1, P2) ... </k>`
- Normalized SHA-256:
  `6f56e984cb3d0fc19ad90190688aabe5b4fa9cd665cd8ddc4bb1e7b98d9eb69f`
- Source rule ID:
  `rule-6f56e984cb3d0fc19ad90190688aabe5b4fa9cd665cd8ddc4bb1e7b98d9eb69f`
- Attributes: none
- Whole ordered inventory SHA-256:
  `e89b4739e9431ec1455126fb59fc7694602405f61bd657e423bf442297b68129`

The frozen `verification.k` file hash is
`7a008f7d521b5ba471dfdd8236529e06d411b9248b1662ed62f478a190a4cca3`.
The discovery manifest contains exactly the same one ordered identity. Both
identity lists are duplicate-free; there are no omissions, extras,
reorderings, changed normalized hashes, or unaccounted classifications. The
discovery inventory hash exactly matches the reconstruction.

## Independent Stage 3 classification

The sole rule is an `OPERATIONAL_RULE`.

It is the ordinary entry transition for the verification harness. It replaces
`verifyBF(P1, P2)` in the computation cell with the frozen source-program term
followed by `invokeBF(P1, P2)`. The separate frozen `solution-program.k`
expands `solutionProgram` to the exact program AST. In `semantic.k`, the
module/invocation rule consumes that AST and invocation, binds `P1` and `P2`
to the two planet cells, and then ordinary statement, conditional, and return
rules execute the program and update the result cell.

The inventory rule does not define a summary, recurrence, macro, or named
proof term. It does not assert a mathematical fact about the planet ordering,
and it is not a separately proved rule later imported into another proof. It
therefore is neither `DEFINITION`, `DOMAIN_LEMMA`, nor
`PROVED_DERIVED_LEMMA`. Counterfactually replacing its right-hand side with a
constant result, omitting the frozen program, or changing either argument
would alter or bypass execution rather than express a valid mathematical
lemma. This confirms its operational role.

Consequently, the independently classified domain-lemma set is genuinely
empty:

| Classification | Count |
|---|---:|
| `OPERATIONAL_RULE` | 1 |
| `DEFINITION` | 0 |
| `DOMAIN_LEMMA` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |

There are no `simplification` attributes, so the requirement that every
simplification rule be a definition or domain lemma is satisfied vacuously.
There is no mislabeled, irrelevant, or concealed domain lemma.

## Hash and provenance verification

Independent checks recomputed and matched:

- Stage 1 selected workspace tree:
  `f56ef397f1473aca5beedbfee0b2c596f98ccd604eb958f0892b48851602106b`
- Stage 1 deterministic-export tree:
  `e64e45d01443272b6fbf375799f1e31189b687d833207af9a33617899a1a8ea3`
- Stage 2 selected audit tree:
  `b384433ce47601d41a5fde4c40acac68c881f013628e2944e64490f3c694a0b5`
- Stage 3 discovery file:
  `86e745f28d64916edbf7926d36c7287d0ea3000ac72b958ed93ebd672058caa2`
- Stage 4 selected generation tree:
  `b2f8d2456481bb9525480c79667f8a7e4f551da960fcf1ed5c0339239782ea53`
- Generated Lean project tree:
  `605f5ee1c7ad3c139280be423c1059d67782f2a3bf926ebe93a876b3bacb6771`
- Generated obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- Trust inventory:
  `e6b94af33ad4a938e05929eed9d8df3068aa40c5199c976dee54aab5afe66be3`
- Canonical resolved audit input:
  `55636a2e734ea8adeb7fe9d362f206b4e76ac1d48552d070f2f5467038773001`

The complete audit-input Stage 1 file map also matches bijectively: all 255
recorded relative files exist, no additional files occur, and every file hash
matches. The generator toolchain object exactly equals the trusted lock file.
All corresponding hashes agree across the audit input, input manifest,
generator manifest, export result, recorded preflight, and mounted content.

## Stage 4 obligation and target judgment

The deterministic input manifest accounts for the reconstructed rule exactly
once in `operational_rules`. Its definition, proved-derived-lemma,
domain-source-rule, and summary-function lists are empty.

The generated obligation map contains:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

Thus the independently empty domain set maps bijectively and in order to the
empty obligation set. There can be no omission, duplicate, irrelevant or
weakened obligation, vacuous conjunct, or unbound target parameter. All
manifests record obligation count zero and status
`KLEAN_NO_OBLIGATIONS`.

An independent scan of every generated Lean source found zero
`targetStatement` declarations. The generator manifest, recorded preflight,
audit-input preflight, and audit-input top-level target all record `null`.
This is the exact required fixed generated target for a genuinely empty domain
set: no target exists. No Stage 5 proof candidate exists.

The generated base contains 41 generic Klean hook axioms recorded by
`trust-inventory.json`, but it contains no generated proposition or proof
target and has zero proof holes. These generic executable hook declarations do
not turn the empty Stage 3 domain set into a proof obligation.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three inputs plus the trusted
toolchain lock.

The first invocation exposed a container PID-namespace/procfs mismatch: Lean
used `/proc/<namespace-pid>/exe`, while this environment exposed the current
process through `/proc/self/exe`. I recorded that failed invocation. I then
used the audit-local shim in `evidence/procfs-readlink-shim.c`, which rewrites
only numeric `/proc/<pid>/exe` `readlink` requests to `/proc/self/exe`; it does
not alter any frozen or generated input. With that environment correction,
the same trusted function returned:

- `lake clean`: exit 0, empty output
- `lake build`: exit 0, successful nine-target build
- Stage 1 export hash:
  `e64e45d01443272b6fbf375799f1e31189b687d833207af9a33617899a1a8ea3`
- Discovery hash:
  `86e745f28d64916edbf7926d36c7287d0ea3000ac72b958ed93ebd672058caa2`
- Generated tree hash:
  `605f5ee1c7ad3c139280be423c1059d67782f2a3bf926ebe93a876b3bacb6771`
- Obligation count: 0
- Target: null
- Designated sorry count: 0
- Status: `KLEAN_NO_OBLIGATIONS`

The generated input snapshots remained unchanged through the rerun.

## Evidence

Raw commands, outputs, reconstructed inventory, independent checker, and
environment-shim source are under `/audit-output/evidence/`. The decisive
records are:

- `03b-inventory-bijection-complete.log`
- `04b-pipeline-tree-hash-verification.log`
- `08-rerun-klean-preflight-with-procfs-shim.log`
- `09-generation-sidecars-map-and-target-scan.log`
- `10-independent-stage4-checks.log`
- `reconstructed-inventory.json`
- `independent_stage4_checks.py`
- `procfs-readlink-shim.c`

The independent checker reports 38 checks, zero failures.

VERDICT: PASS
LEGITIMACY: LEGIT
