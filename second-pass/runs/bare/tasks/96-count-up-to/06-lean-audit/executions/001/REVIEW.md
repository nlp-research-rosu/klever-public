# Independent Stage 3–5 audit: `96-count-up-to`

## Scope and outcome

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `bare`, and
semantics mode `GENERATED_SEMANTICS`. Stage 4 is selected as
`KLEAN_NO_OBLIGATIONS`. I independently reconstructed and classified the
Stage 3 inventory, authenticated the generation-time Stage 4 producer,
reran the trusted mechanical preflight, and checked every recorded hash,
mapping, and target field.

The selected status is legitimate. The frozen `verification.k` contains eight
proof-side defining equations and no domain lemma. Consequently, the correct
domain-obligation set is empty, Stage 4 correctly emits no theorem target, and
there must be no Stage 5 proof candidate. `/candidate`, the resolved Lean
workspace, the resolved Lean invocation, and the Stage 5 result are all absent
or null.

I treated every mounted candidate/provenance file as untrusted evidence. I did
not rely on the earlier Stage 2 review, its verdict, the Stage 3 rationales, or
the stored Stage 4 PASS-like status for the judgments below.

## Frozen input and inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. Its local module-closure result is exactly
`["VERIFICATION"]`. `VERIFICATION` imports `MPY`, but `MPY` is defined in
`semantic.k`, not as another module inside the frozen `verification.k`; thus it
does not add local verification-file rules to this inventory.

The reconstructed values are:

- `verification.k` SHA-256:
  `1618277d676d68b08fc89c7f3a4ba8563d1496dc94db67b69cd5c36c5460636d`
- inventory SHA-256:
  `2588e4ba3c30ca3e8b04ddc4d7e095dcf7647748a626faf4a4eef016fd3e5145`
- rule count: 8
- duplicate reconstructed IDs: 0
- omitted Stage 3 IDs: 0
- extra Stage 3 IDs: 0
- duplicate Stage 3 IDs: 0
- ordered identity sequence equal: yes

For every rule, I independently normalized its captured source as
single-space-separated text, recomputed the SHA-256, confirmed
`source_rule_id = "rule-" + normalized_sha256`, and checked its physical source
span. The exact reconstructed sequence is:

| Span | Normalized SHA-256 / source identity | Classification |
|---|---|---|
| 11–12 | `4c9c7cd0ecff4b21cb2a0220c1266d98e432dae12759c131c91d6693489f0993` | `DEFINITION` |
| 14–17 | `955cda9f3354ba04534cae8c06c05905914e9d2d6daf0bc6bc5ded052d940be2` | `DEFINITION` |
| 19–22 | `577db1aaf2625dbeb758307db9641573f59928437d750b64a81d788c69b0e08d` | `DEFINITION` |
| 27 | `e47ad287a5faffc436895fc5017ba26a9df44510cd197aba879225609e7c4c40` | `DEFINITION` |
| 28 | `dc7cdce70c542df1714b2772a5d2476a13e792688f8d9cd7a872d34c5d06c842` | `DEFINITION` |
| 33–34 | `403f46dd6096062e1aeedc2696c1ce761f7414c3e91f819ddcabea36164a8662` | `DEFINITION` |
| 36–39 | `2ff40da2add1eb80cc1ec89686f3a022e3631a8b2dcf0d901316d114807529a9` | `DEFINITION` |
| 41 | `7cc9f28ac165f611ede21e85e873ac0356fd4511c1ba99151ed097b72984ab3c` | `DEFINITION` |

The protected Stage 3 document has exactly these eight IDs in this order and
the same whole-inventory hash. No rule has a `simplification` attribute, so the
special simplification-class constraint is satisfied vacuously.

## Independent semantic classification

All eight entries are genuinely `DEFINITION`, not disguised domain lemmas:

1. The three `noFactor(C,D)` equations are the base, divisor, and recursive
   branches of a newly declared proof-side summary. On the used domain
   `C >= 2, D >= 2`, their guards are exhaustive and disjoint, and the recursive
   branch strictly advances `D`.
2. The two `isPrime(C)` equations define a newly declared predicate. Below 2 it
   is false; from 2 upward it invokes the divisor-search summary at divisor 2.
3. The two `primesFrom(C,N)` equations define a newly declared half-open list
   recurrence. On the used domain `C >= 2`, the base and recursive guards
   partition `C >= N` versus `C < N`, and recursion advances `C`.
4. `primesBelow(N) => primesFrom(2,N)` is an unconditional alias defining the
   result summary used by the postcondition.

None is an `OPERATIONAL_RULE`: their left-hand sides are fresh functional
summary symbols and contain no `<k>` execution configuration. None is a
`PROVED_DERIVED_LEMMA`: Stage 1 does not first prove an identical rule in a
module excluding it and later import it. None is a `DOMAIN_LEMMA`: no rule
asserts an independent fact over pre-existing mathematics; each fixes a branch
of a newly introduced named summary.

The definitions are materially relevant. The source program initializes the
candidate at 2, scans candidates below `n`, tests divisors while
`divisor * divisor <= candidate`, conditionally appends the candidate, and
increments it. The frozen operational K semantics lowers the exact source AST
to `scan(2,N)` and models the divisor loop with `trial`. The summaries mirror
those operational boundaries, and the exact result postcondition is
`primesBelow(N)`. Removing or counterfactually changing the divisor outcome,
candidate increment, conditional cons, or initial candidate changes the
corresponding summary connection; these equations are not irrelevant facts.

The independently classified `DOMAIN_LEMMA` set is therefore genuinely empty.

## Stage 4 producer authentication

I hashed the mounted generation-time producer sources before accepting any
Stage 4 result:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same |

Those hashes match both `generator-manifest.json` and
`generation-tools/source-manifest.json`. The immutable image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the generator manifest, source manifest, and the basename bound by the
launcher’s producer-source path. The producer bundle contains exactly the two
producers plus `source-manifest.json`.

Using the same `tools.pipeline_contract.sha256_tree` framing used by the Stage 6
resolver, the producer bundle recomputes to
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
exactly the launcher-recorded value. A separate evidence log also records a
different digest from the unrelated `tools.audit_contract.sha256_tree`
framing; that is not the resolver algorithm. The correct resolver-algorithm
comparison passes.

There is no missing or mismatched producer source and therefore no
infrastructure `AUDIT_ERROR`.

## Trusted preflight rerun

I invoked `tools.klean_preflight.check_generation` with:

```text
frozen_input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
PYTHONPATH=/reference
```

The first invocation reached the clean-build step but the audit container’s
process namespace caused Lean to read `/proc/<its namespace PID>/exe`, which
returned `ENOENT`; `lake clean` consequently reported that it could not detect
its installation. I traced that exact failed `readlink`. `/proc/self/exe`
remained available.

I compiled the recorded minimal `LD_PRELOAD` interposer that changes only a
failed `/proc/*/exe` read to `/proc/self/exe` and logs every such call. I then
reran the same trusted `check_generation` function with that interposer
inherited by its real subprocesses. I did not replace its `run_command`,
simulate a build, edit the immutable generated project, or bypass any
structural check. The function made its own fresh temporary copy and actually
ran both commands.

The completed rerun returned:

```text
status=KLEAN_NO_OBLIGATIONS
obligation_count=0
target=None
designated_sorry_count=0
trust_declaration_count=41
lake clean exit_code=0
lake build exit_code=0
Build completed successfully.
```

The check’s pre/post immutable snapshot remained unchanged. The diagnostic
output hashes differ from the stored preflight only because the interposer’s
readlink trace is included in stdout/stderr; the structural hashes, status,
target, counts, and actual build result agree.

## Hash and manifest reconciliation

The launcher envelope validates with resolved-input digest
`af1e22f5097dd1f252c610fc29c75792be0ede8e43a50c98578c1c1e110eeda0`.
All launcher-recorded artifact hashes recompute:

| Artifact/hash convention | Recomputed value |
|---|---|
| Stage 1 workspace, pipeline tree | `7666da4ff6c5e604ecac333bb785b4922c13131976bbd556b40518e5330d2869` |
| Stage 1 frozen export, Klean tree | `e173af5c2b07b756856f7774397100e71dc378a6df50fad350f5e90855eff1a9` |
| Stage 3 discovery file | `98e469db221c9f7189c5e317f69162a7116e1ea6edf4e3c4546f1fc7a7937d72` |
| Selected Stage 2 audit tree | `944ef1e00dab2615bf20193d627d346c303b09f766ba6f6ab32b3072aa5925cd` |
| Selected Stage 4 generation tree | `b872a0c3226552c44119ba602e15426b568adbb5f79956725aeba0977ffa4a34` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project, Klean tree | `6ed054b2016baf30155ed9c87e69b7166db12b64fa2ba030b5c5884f661596cb` |
| Trust inventory file | `ac74ecc6b77cf45bc4734b728e165751336e23ae76610c19ee6f9293003fab36` |
| Obligation map file | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |

Every individually recorded Stage 1 source hash also matches. The generator
toolchain block equals the pinned toolchain lock. The input manifest’s
`definitions` list is exactly the reconstructed eight-rule inventory enriched
with the Stage 3 classification/rationale fields. Its `operational_rules`,
`proved_derived_lemmas`, and domain `source_rules` lists are all empty, as the
independent classification requires.

## Obligation bijection and fixed target

The complete generated `obligation-map.json` is:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Thus the independently required domain-rule sequence, input-manifest
`source_rules`, obligation-map `source_rules`, and generated obligation
sequence are the exact empty-to-empty bijection. There can be no omission,
duplicate, irrelevant conjunct, weakened conjunct, vacuous conjunct, or
unbound trust parameter inside an empty obligation set. All four recorded
obligation counts—the generator manifest, export result, stored preflight, and
launcher preflight—are zero.

The trusted `klean_export.target_statement` parser returns `None`, and
`expected_target_definition(obligation_map)` also returns `None`. The generator
manifest, stored preflight, and launcher all record `target: null`.
`Lemmas.lean` contains only imports, comments, and an empty namespace; a search
finds no theorem, lemma, `sorry`, `admit`, `unsafe`, target, or `Proof.final` in
the generated project.

This is the required fixed target state for a genuinely empty domain set:
there is no generated target at all.

## Stage 5 disposition

Proof-mode checks are not applicable because the authenticated and
mathematically justified Stage 4 status is `KLEAN_NO_OBLIGATIONS` and the
launcher selected `CLASSIFICATION_ONLY`. Consistently:

- `/candidate` is absent;
- `lean_workspace`, `lean_invocation`, `stage5_result`, and launcher `target`
  are null;
- there is no `Proof.final`;
- there are no `target.parameters` requiring an operational-bridge audit.

Running a Stage 5 proof or inventing a target here would contradict the
required no-obligation protocol.

## Evidence

Key raw and derived evidence is preserved under
[`/audit-output/evidence/`](/audit-output/evidence/):

- [launcher metadata](/audit-output/evidence/00-launcher-metadata.txt)
- [canonical reconstructed inventory](/audit-output/evidence/02-reconstructed-inventory.json)
- [inventory command output](/audit-output/evidence/02-inventory-command.log)
- [strict Stage 3 bijection](/audit-output/evidence/03-stage3-bijection.log)
- [frozen source, semantics, and specification](/audit-output/evidence/04-frozen-program-semantics-spec.txt)
- [Stage 4 manifests and producer hashes](/audit-output/evidence/05-stage4-manifests-and-producer-hashes.txt)
- [producer authentication](/audit-output/evidence/06-producer-authentication.log)
- [correct resolver-framed producer tree check](/audit-output/evidence/06b-producer-tree-hash-correct-algorithm.log)
- [initial preflight environment failure](/audit-output/evidence/07-preflight-command.log)
- [Lean/Lake namespace diagnosis](/audit-output/evidence/08-lean-toolchain-diagnosis.txt)
- [recorded namespace interposer source](/audit-output/evidence/08-readlink-namespace-shim.c)
- [interposer reproducibility](/audit-output/evidence/08f-shim-reproducibility.txt)
- [successful trusted preflight rerun](/audit-output/evidence/09-preflight-command.log)
- [returned preflight JSON](/audit-output/evidence/09-preflight-result.json)
- [independent hash, bijection, and target audit](/audit-output/evidence/10-independent-hash-bijection-target-audit.log)
- [no-obligation/no-target/no-candidate evidence](/audit-output/evidence/11-no-obligations-no-target-no-candidate.txt)
- [full independent classification judgment](/audit-output/evidence/12-classification-judgment.md)

VERDICT: PASS
LEGITIMACY: LEGIT
