# Independent audit: 28-concatenate, bare, GENERATED_SEMANTICS

## Scope and result

The launcher and `/audit-input.json` both select `CLASSIFICATION_ONLY`. I
therefore audited the protected Stage 3 classification and selected
deterministic Stage 4 generation. Stage 5 proof checks are inapplicable: the
audit input has `stage5_result: null`, every Lean workspace/invocation binding
is null, and `/candidate` is absent.

I treated the mounted Stage 1, prior Stage 2 review, Stage 3 manifest, Stage 4
artifacts, logs, and comments only as evidence. No conclusion or instruction
from those artifacts was trusted.

## Producer-source provenance gate

I hashed the two mounted generation-time producer files before judging Stage 4:

- `klean_export.py`:
  `2f04f1bc0f49f9f8c6f009875e730866a61c76ac029663d2ed2ffaffeab4e773`
- `klean.py`:
  `308fb4d213034fc0c00cd37e9617f6b05f10bda7bc7e383994786911f8a04bcc`

Both equal the file map in
`/reference/generation-tools/source-manifest.json` and the
`exporter_sha256`/`klean_py_sha256` fields in
`generator-manifest.json`. The manifest image ID is
`sha256:9b919795ce70e46b5f58b36984cd9be4f84d1b056135e41498da6390ff4c5fa2`;
it equals the source-manifest image ID and the image key embedded in the
launcher-resolved producer-source path.

Using the launcher's trusted `pipeline_contract.sha256_tree`, the complete
three-file producer bundle hashes to
`305f865953323958cc46250998c0ae761309c7bc7c60d6a2206b72df280f8354`,
exactly the aggregate recorded in `/audit-input.json`. The producer source set
is complete and has no unexpected file. This gate passes; there is no
producer-source `AUDIT_ERROR`.

Raw provenance evidence is in `evidence/06`, `07`, and `09`.

## Independent inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, independently of the protected classification.
The selected local verification-module closure is exactly `VERIFICATION`.
`MPY-SYNTAX` is imported but defined outside `verification.k`, so it does not
add a local rule. The reconstructed `verification.k` hash is
`e93633b8a7730d721595849914379018046e25c0b0e6843968c3011a70a0b029`;
the canonical inventory hash is
`ff1489ee82454cec9e85142c89c5bdd29be7bb93f1356d4116e0a41c3a0c1843`.

The complete ordered inventory is:

| Order | Source span | Normalized hash / source rule ID | Attributes | Independent class |
|---|---:|---|---|---|
| 1 | `verification.k:6` | `df6c6246e36176afc3c709b2cac7210c00527c8cbdd63317e19954afb58e6d9b` / `rule-df6c6246e36176afc3c709b2cac7210c00527c8cbdd63317e19954afb58e6d9b` | none | `DEFINITION` |
| 2 | `verification.k:7` | `4785cdfafa15c19b300ac57d1f3eefe6562fc8e321341a00841e9a26112e2f64` / `rule-4785cdfafa15c19b300ac57d1f3eefe6562fc8e321341a00841e9a26112e2f64` | none | `DEFINITION` |

For each entry, `source_rule_id` is exactly `rule-` plus the independently
recomputed normalized-source SHA-256. The protected manifest has the same
inventory hash and exactly the same ordered ID sequence. The sequence is
unique, with no omissions, extras, duplicates, reordered identities, or
changed hashes. Evidence is in `evidence/03` and `10`; numbered frozen sources
are in `evidence/04`.

## Classification judgment

The two rules are:

```k
rule concatAcc(ACC, .StrList) => ACC
rule concatAcc(ACC, S :: REST) => concatAcc(ACC +String S, REST)
```

`concatAcc` is declared as a named `[function]` and these are its base and
recursive equations. The empty and cons patterns are disjoint and cover the
entire locally declared `StrList` grammar. The recursive call consumes
`REST`, so the definition descends structurally. The equations therefore
define a total mathematical left fold, rather than assert a separate property.

The frozen operational semantics initializes the program accumulator to the
empty string, consumes the input list from left to right, evaluates
`result + string` with K's `+String`, and returns the accumulator. The
definition uses the same accumulator order and the same `+String` operation.
It is relevant to both the source program and postcondition: the loop claim
and end-to-end claim use `concatAcc` to state the returned string.

Neither rule matches a `<k>` item, source AST constructor, configuration cell,
continuation, binding, or operational state. It does not replace program
execution. Neither is a separately asserted domain theorem, and neither is
presented as a derived lemma. Accordingly both are genuinely `DEFINITION`,
not `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`.

There are no `simplification` attributes in the reconstructed inventory, so
the simplification-class restriction is satisfied vacuously. The induction
claim in `spec.k` is a claim rather than a rule in the local
`verification.k` inventory; it is therefore not an omitted Stage 3 rule.

The independently classified true domain-lemma set is empty.

## Hash and manifest reconciliation

I independently recomputed every launcher resolution content hash with its
trusted producer:

- Stage 3 manifest:
  `e76b701b6245aa8c507b785da32418d896fcbdfe1cccc318c5c1fcce841a17c1`
- generated tree:
  `6893259c092152261697d2dfad63dd8036f3b2b19181f835d0345b2e8fa127bb`
- producer bundle:
  `305f865953323958cc46250998c0ae761309c7bc7c60d6a2206b72df280f8354`
- selected Stage 2 tree:
  `5fcfc811659d4b5e3546ecd28fdafa21484c7e3f465b7345a4594e5ec0ac1b15`
- Stage 1 source tree:
  `ed27e8d459b7d9d8b8c73325ef522dc9ba74a54451e4f32cd37e06410244c1e3`
- selected Stage 4 tree:
  `c5f8cd99115e43bfef20d592318cab271e82c5a9f03fc6cb87441572a347fd81`
- Stage 1 deterministic-export digest:
  `b26619d486f37f86e50464db61d29fa90a1d7b38be626022e8a9e8397f1bbc7d`

All match `/audit-input.json`. The complete per-file Stage 1 hash map also
matches exactly. Re-hashing the canonical `resolution` object gives
`5d729574c2296250c27269ba88dc182d8cf003836c5e00e80a1d32eb8f8a5d39`,
the recorded `resolved_input_sha256`. Evidence is in `evidence/24`.

The obligation-map file hashes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
and the trust inventory to
`0397f02690ededa8aa065cb839c492ae0b534ec1204422f20e43929d28815fb5`;
both match their sidecar bindings. The generator toolchain object equals
`/reference/klean-toolchain.lock.json`.

## Stage 4 bijection and fixed target

I directly loaded the already hash-verified generation-time
`klean_export.py`. It independently recomputed:

- Stage 1 export digest:
  `b26619d486f37f86e50464db61d29fa90a1d7b38be626022e8a9e8397f1bbc7d`;
- generated tree digest:
  `6893259c092152261697d2dfad63dd8036f3b2b19181f835d0345b2e8fa127bb`;
- eligible domain source rules: `[]`;
- expected target definition: none; and
- actual generated target statement: none.

`input-manifest.json.source_rules`,
`obligation-map.json.source_rules`, and
`obligation-map.json.obligations` are all exactly empty.
`trust_parameters` is also empty. Thus the exact ordered
source-rule/obligation bijection holds, with no omission, duplicate, extra
rule, irrelevant obligation, weakened obligation, or conjunct to make
vacuous.

The generator manifest target, generated target, audit-input target, and
recorded Stage 4 preflight target are all null. `Lemmas.lean` contains only an
empty namespace; there is no generated theorem to change. This is not an
improper empty conjunction: the domain set was found empty independently from
the frozen K source before inspecting the Stage 4 mapping.

Evidence is in `evidence/23`, `25`, and `27`.

## Fresh trusted preflight

The first literal `check_generation` invocation reached its temporary-build
phase but Lake failed with `could not detect the configuration of the Lake
installation`. Diagnostics showed an audit-container PID namespace mismatch:
processes received namespace PIDs while `/proc/<pid>/exe` exposed host PIDs.
Lean/Lake 4.22.0 uses that path to locate its installation.

I preserved the failure and diagnostics, then compiled the narrow source in
`evidence/lean_pid_namespace_fix.c`. It changes `getpid()` only for processes
named `lean` or `lake`, returning the host PID reported by
`/proc/self/status`; all other processes use the real syscall. It does not
modify the generated project, K inputs, manifests, checker, or theorem
environment. With that infrastructure repair, `lean --version` reports the
pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

I then reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required mounted paths. Its immutable-input snapshots remained
unchanged. Fresh results:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all generated modules built;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligations: 0;
- target: null;
- designated sorries: 0; and
- recorded executable trust declarations: 42, exactly reconciled by the
  trusted checker.

The exact returned JSON is
`evidence/28_check_generation_returned_evidence.json`; the initial failure,
repair, and successful raw run are in `evidence/11` through `22`.

## Stage 5 applicability and final judgment

Because the independently determined domain set is genuinely empty,
`KLEAN_NO_OBLIGATIONS` is the correct deterministic Stage 4 status. There must
be no generated target and no Stage 5 candidate; both conditions hold.
Consequently no `Proof.final`, target parameter, operational bridge
definition, clean candidate build, or `#print axioms Proof.final` exists to
audit in this classification-only mode.

Stage 3 is complete and correctly classified. Stage 4 is provenance-bound,
hash-consistent, bijective, and mathematically faithful to the empty domain
set. The fixed no-target result is unchanged, and Stage 5 is correctly absent.

VERDICT: PASS
LEGITIMACY: LEGIT
