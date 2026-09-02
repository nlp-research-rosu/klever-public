# Independent audit: 136-largest-smallest-integers

## Scope and result

The launcher selected:

- problem: `136-largest-smallest-integers`
- condition: `bare`
- semantics: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

`AUDIT_MODE` and the signed audit-input resolution both say
`CLASSIFICATION_ONLY`. `/candidate` is absent, and the Stage 5 result,
workspace path, invocation path, and hashes are all null. Stage 5 build,
`Proof.final`, axiom accounting, and operational-parameter checks therefore do
not apply.

The mathematical classification and the selected no-obligation result are
legitimate. The only concern is byte-level Stage 4 reproducibility: the
historical generator source hashes do not identify the current mounted trusted
generator sources, and current-source regenerations vary with Python's hash
seed unless that unrecorded environment variable is pinned. This does not
change the empty obligation set or null target.

## Frozen rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`; imported `MPY` and `K-EQUAL` are external to the local
`verification.k` module set.

The reconstruction produced:

- `verification.k` SHA-256:
  `a54766e74afa56d501e8880c29aacebec2884555ba27c801af7a1bbb614859db`
- rule count: 11
- inventory SHA-256:
  `577e90b3e2ba59231529bb8ba7f67b95a7969f86d0f9e22e335605619797a3f9`

For every rule I independently sliced the recorded physical source span,
normalized it with single whitespace between tokens, recomputed SHA-256, and
checked that `source_rule_id` is `rule-` followed by that digest.

| # | Source span | Recomputed `source_rule_id` | Independent class and role |
|---:|---:|---|---|
| 1 | 15 | `rule-f399d8c5d55f049f32bfc0bd71b072990832b797cd2cb42f6179b783046534cf` | `DEFINITION`: `#negFold` base equation |
| 2 | 16–17 | `rule-9b3b29557dda868e08cfdf72056753b24c58ed6d469ddf14e2186b89b0e3ea1c` | `DEFINITION`: `#negFold` recurrence |
| 3 | 18 | `rule-19cf10e725a5d97d562b52cd3a5fe1591b678d5bcc7a6d1940b2a8f004377ed6` | `DEFINITION`: `#posFold` base equation |
| 4 | 19–20 | `rule-24cf846bf9c77cc8a105ef4f25e62da61cd8bd53da78040bc17fd0123d8e08dd` | `DEFINITION`: `#posFold` recurrence |
| 5 | 22–26 | `rule-d7ba05b7723c98a5a29344e98acb2fad66722b3cf5375329b30adb9afdaab7ef` | `DEFINITION`: negative-fold step |
| 6 | 27 | `rule-8edcdf9ff6c7e0e0546a377adca014bf2f167b722725bd5f18085acfd42a4a2e` | `DEFINITION`: first negative candidate |
| 7 | 28–32 | `rule-1a4cc923c3fb70c9d37d91d1cffd19876a7de71476fc86a021051ea28b8131c3` | `DEFINITION`: maximum negative candidate |
| 8 | 34–38 | `rule-3ae79becbba60cc8588c454974ca8d38e698a8209a85ee19fa8148db09158b0a` | `DEFINITION`: positive-fold step |
| 9 | 39 | `rule-6092bce027b3d36ec09884b15ec16c4c4e794c506d5b662bf468880fd537e36a` | `DEFINITION`: first positive candidate |
| 10 | 40–44 | `rule-d1456be43b700a0307264d0eecf8cf5db5851c6cbc6d8a3e55395d73aa60db76` | `DEFINITION`: minimum positive candidate |
| 11 | 47–67 | `rule-1eea429ae87f08a6a57848039abc4bbe4591ac006ff0969311d6da7d48604f0b` | `DEFINITION`: `solutionProgram` macro term |

The protected Stage 3 manifest has exactly these 11 IDs in exactly this order.
It has no duplicate, omitted, extra, or reordered identity, and its inventory
hash matches the reconstructed inventory. The Stage 4 input manifest also
preserves every rule's ID, module, span, normalized hash, attributes, text, and
classification.

Raw inventory and the 167 automated comparison checks are in
[10-reconstructed-rule-inventory.json](/audit-output/evidence/10-reconstructed-rule-inventory.json)
and
[65-independent-structural-checks-success.txt](/audit-output/evidence/65-independent-structural-checks-success.txt).

## Independent classification judgment

All 11 rules are definitions, not domain lemmas:

- `#negFold`, `#posFold`, `#negStep`, `#posStep`,
  `#negCandidate`, and `#posCandidate` are newly declared
  `[function, total]` symbols. Their equations supply the symbols' meanings.
- The fold equations cover the two `IntSeq` constructors (`nil` and `icon`)
  and recurse on the strict tail.
- The candidate equations cover the two `OptInt` constructors (`pyNone` and
  `pyInt`). Their cases are disjoint.
- The step functions have one unconditional defining equation each and select
  the appropriate candidate function only at the strict sign boundary.
- `solutionProgram` is declared `[macro]`; its rule expands that named proof
  term to the translated source-program AST.

These are not ordinary execution/observation rules: none is a `<k>`-cell
transition from `semantic.k`. They are not already meaningful mathematical
facts about pre-existing symbols, so none is a `DOMAIN_LEMMA`. None is a
`PROVED_DERIVED_LEMMA`: the entries are equations rather than separately
proved claims, and `prove.sh` performs one compilation followed by one
`kprove`; it has no earlier module that proves one of these exact rules without
the rule and then imports it into a later proof.

There are no `simplification` attributes in the reconstructed inventory, so
the special simplification-category restriction is satisfied vacuously.

Mathematically, starting from `pyNone`, `#negFold` ignores nonnegative values
and accumulates the maximum among negative values; `#posFold` ignores
nonpositive values and accumulates the minimum among positive values. Induction
on `IntSeq` gives exactly the prompt's pair. The source macro has the same two
`None` initializations, one traversal, strict `< 0`/`> 0` tests, maximum/minimum
updates, and final tuple as `solution.py`. The operational K rules evaluate
those comparisons and assignments, bind each `iterateIntSeq` element, and
evaluate the returned tuple.

As finite adversarial support for that direct inductive reading, I compared the
recurrences with an independently implemented max-negative/min-positive oracle
on all 3,906 lists of length 0 through 5 over
`{-3,-1,0,1,3}`. There were zero mismatches. Constant-`None`, first-element,
and zero-inclusive counterfactuals fail on explicit witnesses. See
[71-fold-semantics-tests.txt](/audit-output/evidence/71-fold-semantics-tests.txt).

Therefore the independently classified `DOMAIN_LEMMA` set is genuinely empty.

## Hash and manifest audit

The signed audit-input digest recomputes to
`c97c86ee64e3122898004af97d48cb6c087a1ac55b2cf45dd3b49eedbbc9de9a`.
The exact 41-entry Stage 1 source-hash map matches every mounted regular file,
with neither omissions nor extras.

All hashes bound to mounted artifacts recompute exactly:

| Object | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `8043e15c6c6f41ca2165223e60059ec04572da90f59a8eed081c559383bc0bd9` |
| Stage 1 exported tree | `00b6795e09cda2a090e4e7dab47413920e59489e3e5968bcb50769f4ec1a0c90` |
| Stage 2 selected audit tree | `ac009aa1396e95724a308b6a533ab3d7045703dcc519547b9a942a855ec1e0f6` |
| Stage 3 manifest | `2b94ff2eebda3d21f8ba4c4f46bf2b58e912c271402b841985b7240e46ec02a3` |
| Stage 4 selected generation tree | `ed651f3ea12aac3b8acb79a1381adce6391b9c3e0dbe52d2497524930111c72a` |
| Generated Lean-project tree | `d3a3a5f900992e805887806c558b10a13b9fb56d388836e69c00172fb1f74765` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `22cfa7b965c7fa5bfadf5bc9eef6eb502fea4368ccfdb37622364c6738ef330e` |

These values agree across the audit input, selections, input manifest,
generator manifest, export result, preflight result, and generated files. The
generator's toolchain object exactly equals the mounted lock.

## Stage 4 obligation and target identity

Because the independently classified domain set is empty, the exact expected
Stage 4 source-rule set is empty. The selected artifacts have:

- `input-manifest.json.source_rules = []`
- `obligation-map.json.source_rules = []`
- `obligation-map.json.obligations = []`
- `obligation-map.json.trust_parameters = []`
- generator/export/preflight obligation count `0`

Thus the source-rule/obligation relation is an exact empty bijection: there is
no omission, duplicate, irrelevant obligation, weakened obligation, vacuous
conjunct, or parameter bridge.

The generator manifest, preflight, audit input, and an independent
`target_statement` parse all report target `null`. `Lemmas.lean` contains only
an empty namespace and no proposition declaration. Stage 5 is absent. This is
the required fixed target for a genuinely empty domain set.

The generated project has 47 allowlisted non-propositional infrastructure
axioms and zero `sorry`/`admit`/`unsafe` occurrences. They do not discharge a
target because there is no target. Target inspection is in
[62-generated-target-inspection.txt](/audit-output/evidence/62-generated-target-inspection.txt).

## Required preflight rerun

The first literal rerun reached `lake clean` but exposed a container PID
namespace defect: Lean 4.22 calls `readlink("/proc/<getpid()>/exe")`, while this
container does not expose the namespace PID at that path. A standalone C test
reproduced `ENOENT`. I compiled an audit-local preload shim that changes only
those `/proc/<pid>/exe` readlinks to `/proc/self/exe`; it does not alter any K,
Lean, manifest, or candidate file.

With the pinned Lean sysroot and that environment repair,
`tools.klean_preflight.check_generation` returned:

- status `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `830e27a137e8df217daf93ff10a991550ab4383fe6af8473b11dcc81c0846668`
- obligation count 0
- target null
- trust declaration count 47
- designated sorry count 0

Those diagnostics exactly match the recorded preflight. The full returned
evidence is
[44-rerun-check-generation-success.txt](/audit-output/evidence/44-rerun-check-generation-success.txt);
the failed environmental attempts and repair are retained alongside it.

## Concern: Stage 4 byte reproducibility

The selected generator manifest records:

- exporter source:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- Klean wrapper source:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`
- separate generator image:
  `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`

The current trusted `/reference/tools` sources hash instead to
`0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
and
`92e9515ae1e4c5275b0cd366e5ff5c16ad35af1afdaf070ef1ae7c0980998964`.
The exact historical exporter source object is not mounted in the trusted
inputs, so those two historical source-hash claims cannot both be replayed
against `/reference/tools`.

More importantly, two regenerations with the same current trusted sources and
the same semantic inputs but randomized/default Python hash seeds produced
different generated-tree hashes:

- `3251853cecbe36a181a2d12f59cac62fdcb8a50ad0e524055c37399c8187cd7f`
- `af0e02e98f9ee65b8693313e217630c7a520c3a0f4b498538761a8558dc7084c`

The differences are ordering of generated `Func.lean` axioms and `Inj.lean`
instances (plus an expected current-exporter `lakefile.toml` setting compared
with the historical selected tree). Two runs with `PYTHONHASHSEED=0` were
byte-identical at
`5e4b2e53f5f7e532781bff80617c6ab6fe6155834b190e70fa81514c9238b53b`.
Neither the manifest nor toolchain lock records a Python hash seed.

This is a reproducibility/provenance concern for the word “deterministic.” It
does not undermine legitimacy here: every regeneration retained the identical
empty obligation-map hash, identical empty `Lemmas.lean`, zero parameters, and
null target. Details are in
[59-stage4-regeneration-diff.txt](/audit-output/evidence/59-stage4-regeneration-diff.txt),
[60-second-stage4-regeneration.txt](/audit-output/evidence/60-second-stage4-regeneration.txt),
and
[72-fixed-seed-stage4-regeneration.txt](/audit-output/evidence/72-fixed-seed-stage4-regeneration.txt).

The exact command ledger is
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

VERDICT: CONCERNS
LEGITIMACY: LEGIT
