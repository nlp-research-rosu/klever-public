# Independent Stage 3–5 audit: HumanEval 77-iscube

## Scope and conclusion

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. `/candidate` is absent, as a classification-only run
requires.

The selected artifacts are byte-for-byte and structurally self-consistent, but
the classification is not mathematically complete. The lexical inventory used
by Stage 3 sees only the wrapper module physically declared in
`verification.k`. Operational K also loads the proof-local modules declared in
`connection-rule.k` and `verification-base.k`. That cross-file import closure
contains two relevant, load-bearing `DOMAIN_LEMMA` simplifications. Stage 3
omits both, Stage 4 generates zero obligations and no target, and therefore the
selected `KLEAN_NO_OBLIGATIONS` status is not legitimate.

This is a proof/classification failure, not an infrastructure `AUDIT_ERROR`:
the required Stage 4 producer sources and immutable generator identity all
match.

## Provenance and producer-source gate

I hashed the mounted producer files before judging Stage 4:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Those values equal both `source-manifest.json` and the `exporter_sha256` /
`klean_py_sha256` fields of `generator-manifest.json`. The source manifest and
generator manifest both name image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`,
which is also the image-key component of the producer bundle path signed in
`/audit-input.json`. The trusted launcher tree-hash algorithm gives
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`
for the bundle, matching the audit input.

All other recorded bindings also match independently:

- the signed audit-input digest is valid;
- every one of the nine launcher resolution hash fields matches its mounted
  input, including both Stage 1 tree-hash schemes, Stage 2, Stage 4, generated
  project, discovery manifest, and the two expected null Stage 5 hashes;
- both selected artifact hashes match;
- all 814 Stage 1 per-file hashes match with no missing, extra, or changed
  regular file;
- generator, input, export, obligation-map, trust-inventory, generated-tree,
  `verification.k`, and discovery sidecar hashes all agree.

Raw results are in `evidence/producer_hash_gate.log` and
`evidence/hash_verification.log`.

## Inventory reconstruction

### Exact trusted lexical inventory

Running the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace returns:

- `verification_sha256`:
  `712698ff263887adafb3ee2c12978495a4f97efbff3aae23d000d16fb4409e9d`;
- selected module: `VERIFICATION`;
- reported local modules: `["VERIFICATION"]`;
- rules: `[]`;
- whole inventory hash:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

`/reference/lemma-discovery.json` has the same inventory hash and an empty
ordered rule list. Against this narrow lexical result, the comparison is
bijective: no duplicate, extra, reordered, or changed identity exists, and the
trusted Stage 3 contract validates it.

That mechanical result is insufficient for the requested mathematical audit.
`verification.k` contains `requires "connection-rule.k"`, and its
`VERIFICATION` module imports `CONNECTION-RULE`. That module in turn requires
`verification-base.k` and imports `VERIFICATION-BASE`. The trusted inventory
implementation builds its module index only from text physically present in
`verification.k`; an imported module declared in a required file is therefore
silently outside that index even though K loads and executes it.

### Operational proof-local closure

I applied the same trusted lexical module, rule-span, normalization, and hash
routines across the proof-local files reached by K imports, stopping at the
supplied `MPY` semantics boundary. The reached proof-local modules are
`VERIFICATION`, `CONNECTION-RULE`, `VERIFICATION-BASE`, and
`VERIFICATION-SYNTAX`. They contain ten rules. The canonical JSON audit hash of
the ten records, with `source_file` added to disambiguate cross-file spans, is
`42b7bcdbe0652a11625501123bc985104cd9241994abf88349bee4bdc578a514`.

The independently reconstructed entries and classifications are:

| Source span | `source_rule_id` | Classification | Reason |
|---|---|---|---|
| `connection-rule.k:8-47` | `rule-7053976245560ebde1f9c329f37f168cf403550b3226be6fd87bc25c9c187bda` | `PROVED_DERIVED_LEMMA` | Exact full-state loop transition first proved bridge-free, then imported as a rule. |
| `verification-base.k:17` | `rule-a125d094d70188da5ff77c740e52261fd69a2a3784be6928238fb15df19a7a19` | `DEFINITION` | Defines the named summary `cubeOf`. |
| `verification-base.k:21-22` | `rule-19e8781342762c8c476b4eea71d343b12d1e66bc89b2d271905518e733ed4682` | `DEFINITION` | Equality branch of the named `cubeSearch` recurrence. |
| `verification-base.k:23-24` | `rule-fb3d10bf0eb9e4f62aad18017f1ab7c5f7a7a5f5c590593e8b83ec2d9834028b` | `DEFINITION` | Greater-than branch of the recurrence. |
| `verification-base.k:25-26` | `rule-bf30e24b24687c20941ecb863886dc67a9049d65bf68ca325559188ec68de3ae` | `DEFINITION` | Recursive less-than branch. |
| `verification-base.k:30-32` | `rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d` | `DOMAIN_LEMMA` | `[simplification]` equating the executed exit comparison with `cubeSearch`; it does not define its built-in equality LHS. |
| `verification-base.k:37-39` | `rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2` | `DOMAIN_LEMMA` | `[simplification]` asserting a guarded finite-map deletion identity; it does not define a named summary. |
| `verification-base.k:42-43` | `rule-79867a7dea47e4e5f98e59d1cdcebad2e7a31d021c387d2ab8c5714ceac988b0` | `DEFINITION` | Negative branch defining `isCubeInt`. |
| `verification-base.k:44-45` | `rule-9371ae3bb178a5f2d69f2338883aa1878c94170ae90c5b52f939214871d333d5` | `DEFINITION` | Nonnegative branch defining `isCubeInt`. |
| `verification-base.k:49-72` | `rule-e0a6a1010506cb6e1e4dcfbfaacc8a9fcb910826e3cf03e90b3a2d2fd022089d` | `DEFINITION` | Names the exact source closure proof term. |

Thus the actual classification is seven `DEFINITION` rules, one
`PROVED_DERIVED_LEMMA`, two `DOMAIN_LEMMA` rules, and no ordinary
`OPERATIONAL_RULE` rule. Full normalized source text, spans, attributes,
hashes, and IDs are in `evidence/proof_local_closure_inventory.log`.

## Classification judgment and operational relevance

The fixed supplied semantics evaluates integer `*`, `<`, and `==` to the K
integer operations; expands `While` to `#while`; updates `candidate` for
`AugAssign`; and implements function return by `#pop`, whose `<scopes>` update
deletes the callee environment key. Those are exactly the operations mentioned
by the two simplifications.

The exit-comparison rule is mathematically true on its guard: if `I³` is not
less than `A`, integer trichotomy leaves equality or greater-than. In the first
case both the built-in comparison and `cubeSearch(A,I)` are true; in the second
both are false. It directly connects the source program's returned equality to
the postcondition summary, so it is not irrelevant.

The map rule is the guarded identity obtained by deleting key `1` from
`(1 |-> S) REST` when `REST` does not contain key `1`. It is needed to express
the fixed semantics' frame-pop scopes state as the target remainder. It is
also relevant to the complete reachability postcondition.

Neither rule qualifies as `PROVED_DERIVED_LEMMA`: both are already present in
`VERIFICATION-BASE`, the module against which the bridge-free connection claim
is proved. Stage 1 does not first prove either exact simplification against a
module that excludes it.

By contrast, the `CONNECTION-RULE` transition does meet the derived-lemma
criterion. The transition bodies in `connection-spec.k:10-47` and
`connection-rule.k:9-46` are byte-identical. I made a fresh Haskell build from
`verification-base.k`, which excludes `CONNECTION-RULE`, and independently ran
the claim; it exited 0 with `#Top`. The Stage 1 sequence then compiles the rule
module and imports it into the final verification module. Evidence is in
`evidence/connection_transition_and_order.log`,
`evidence/kompile_bridge_free_base.log`, and
`evidence/kprove_bridge_free_connection.log`.

The two domain lemmas are demonstrably load-bearing. In separate scratch
copies I removed exactly one simplification at a time, freshly compiled the
unchanged bridge-free base, and reran the unchanged connection claim:

- without the exit lemma, `kprove` exits 1 at the residual
  `C*C*C == A = cubeSearch(A,C)`;
- without the map lemma, `kprove` exits 1 at the residual equating `SC` with
  the post-pop map update.

Both are `WarnStuckClaimState`, not tool failures. The exact mutations and raw
outputs are in `evidence/domain_lemma_removals.diff`,
`evidence/kprove_without_exit_domain_lemma.log`, and
`evidence/kprove_without_map_domain_lemma.log`.

## Stage 4 generation and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
trusted toolchain lock.

The first invocation exposed an audit-sandbox issue: Lean's runtime tried to
read `/proc/<namespace-pid>/exe`, while this sandbox exposes only the equivalent
`/proc/self/exe`, so Lake could not detect its installation. I diagnosed the
exact failed `readlink` and used the recorded minimal compatibility shim that
redirects only `/proc/<digits>/exe` to `/proc/self/exe`. With the trusted
preflight code and all audited inputs otherwise unchanged, the rerun exits 0.
`lake clean` exits 0 and `lake build` exits 0. The build-output SHA-256
`3da7d1e834a84e269f4eb376b285aaa12a0c1a230fe7b2e99abe05f2e790bd5c`
equals the launcher-recorded preflight result. The exact failure, diagnosis,
shim, and successful returned evidence are under `evidence/`.

Mechanically, Stage 4 is internally exact:

- canonical Stage 3 source rules: empty;
- obligation map source rules: empty;
- obligations: empty, ordered, unique, with no conjunct to weaken or make
  vacuous;
- manifest obligation count: `0`;
- expected generated target: `null`;
- actual target found by the trusted parser: `null`;
- generator-manifest target and signed audit-input target: both `null`;
- no candidate project exists.

Those empty sets form a structural bijection only because Stage 3 omitted the
cross-file rules. Under the independent classification, the true domain set
contains the two rule IDs above. Stage 4 therefore omits two required
source-rule obligations and the fixed generated theorem that should contain
them. Internal equality of three `null` target records cannot cure that
semantic omission. Per the audit contract, `KLEAN_NO_OBLIGATIONS` is valid only
for a genuinely empty domain set; this one is nonempty.

The structural results are in `evidence/structural_bijection.log`, and the full
command index is `evidence/COMMANDS.md`.

## Stage 5

Stage 5 is inapplicable because the signed mode is `CLASSIFICATION_ONLY` and no
candidate exists. Accordingly I did not perform proof-target, `Proof.final`,
axiom, or operational-parameter checks. The absence of Stage 5 is structurally
consistent with the selected zero-obligation status, but that status itself is
rejected for the nonempty true domain-lemma set.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
