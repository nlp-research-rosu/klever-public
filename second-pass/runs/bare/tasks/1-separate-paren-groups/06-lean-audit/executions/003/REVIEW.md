# Independent Stage 3–4 audit

## Scope and result

This audit covers HumanEval `1-separate-paren-groups`, condition `bare`,
semantics mode `GENERATED_SEMANTICS`. Both `AUDIT_MODE` and
`/audit-input.json` record `CLASSIFICATION_ONLY`. The resolution records no
Lean workspace, no Lean invocation, no Stage 5 result, and no target; the
`/candidate` mount is absent. Stage 5 proof checks therefore do not apply and
were not run.

I treated every mounted candidate/provenance artifact as untrusted evidence.
Only the trusted code in `/reference/tools` was invoked for inventory,
contract, hash, and preflight checks. No provenance shell script or prior
review was executed or trusted.

The protected Stage 3 classification is correct. The independently classified
domain-lemma set is genuinely empty, so Stage 4's
`KLEAN_NO_OBLIGATIONS` result, absent generated target, and absent Stage 5
candidate are legitimate.

## Producer and immutable-input authentication

Before judging Stage 4, I directly hashed the exact producer sources:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same |

`source-manifest.json` has exactly those two file records and no extra producer
source. Its generator image ID,
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`,
equals `generator-manifest.json` and the final path component recorded by
`resolution.generation_producer_sources` in `/audit-input.json`. The complete
producer-bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching the audit input. Producer provenance therefore passes;
there is no infrastructure `AUDIT_ERROR`.

The trusted audit-input verifier recomputed
`resolved_input_sha256 =
805154090e44d8c2b299be4ce0a6b121fd504fa8391a3fb5e60a8af4d4a8ea23`.
All recorded immutable hashes were recomputed:

| Artifact/hash convention | Observed and recorded SHA-256 |
|---|---|
| Stage 1 workspace artifact tree | `2912ea3c0e4486e103d25d57ade56084b7f5534d35b8782cb3fc9a08c479138b` |
| Stage 1 export tree | `f7198173f419636cacf3c009694d458c1c8113750de230e115a8bdfd24289f83` |
| Selected Stage 2 audit tree | `3ab68ecc6de59b23c1b683246120c2713b070f395f90187f23b8b0039828af9c` |
| Stage 3 manifest file | `1d658f9f3f836cd96386a95bf89aa4d0ae7883a6c174f3fd3bb21487b68e0357` |
| Selected Stage 4 generation tree | `ed3e571d636bf69faabef69f98765174f72b54325fc602c91e65a752f466f35a` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `ec2cabdd88613df091a482f8974a0b9be67d75d3d97827da8ff6ac78ae163e7a` |

Every per-file Stage 1 source hash in the audit input also matches, including
`verification.k =
cf1dced488cadea0d91cd8c13684c691c2bbd9c891e0b717d0905146938e0f53`.
The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

## Rule-inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` independently on the
frozen Stage 1 workspace. `prove.sh` selects `MPY-VERIFICATION`; its local
verification-file closure contains only `MPY-VERIFICATION`. The imported
`MPY` module is in `semantic.k`, not another local module in
`verification.k`.

The reconstruction found 11 rules, all unique, in this exact source order.
Every span was checked against the physical frozen source; every normalized
hash was recomputed from `" ".join(source_text.split())`; every
`source_rule_id` is exactly `rule-<normalized_sha256>`.

| Line | Normalized SHA-256 / `source_rule_id` suffix | Independent class | Role |
|---:|---|---|---|
| 17 | `b29a7b1f61d027c75f5d54e6f778c4ffafe703f461096a1d08700bae9b5849da` | `DEFINITION` | `runSpec` empty-input base equation |
| 18 | `03d30c437cb7bd8a90fd37a82631921d6c5bd459ea8924300ffafa088b28240e` | `DEFINITION` | `runSpec` space recurrence |
| 19 | `ee28b1b89c45af68725d2c53c17fec71114155badb89a86ba1370ef263893c24` | `DEFINITION` | `runSpec` opening-parenthesis recurrence |
| 20 | `ee734da296fe2d2d4070e9117fa1dc33181b3c52f7e9629c362ebe25fa07a852` | `DEFINITION` | `runSpec` closing parenthesis at depth zero |
| 21 | `a1305acd847b564566d980520b2960809147091b2fc541ba1b00bc3534001edd` | `DEFINITION` | `runSpec` closing parenthesis at depth one |
| 22 | `23aee5f25569cab008c78f770e7a68f475ee096ae14e72789cb7a87d5c7b6e26` | `DEFINITION` | `runSpec` closing parenthesis above depth one |
| 24 | `6e9d63e72f1d96b8d7ba85bd3016f00960ddff320ccba1bd43d74b23295b5f90` | `DEFINITION` | `stateDepth` structural projection |
| 25 | `5b065840a104280bdea14bf8cbfb96a45454e5d3f68448977ab8119c3521b55a` | `DEFINITION` | `stateCurrent` structural projection |
| 26 | `4c968b2b2cfa45f88ae0c5dcf90432112081bb44e8a2471c9a987aa90bd17bfe` | `DEFINITION` | `stateOutput` structural projection |
| 27 | `109874df159aa48ad8e1b3715b0ea513f28bc7bb9b410bf89eb790601fd826a4` | `DEFINITION` | `stateLast` structural projection |
| 28 | `83fdf9d2c3bc8712363c660c4deb46f4e4be4ae1056e9f139ccca451b876e6df` | `DEFINITION` | `separateSpec` initialized summary/output projection |

The resulting whole-inventory hash is
`7110b556e2e2e5f7641769542e6db909889827d1e68749a448bdf5f51d38d241`.
It equals `/reference/lemma-discovery.json`. The manifest contains exactly 11
unique IDs in exactly canonical order; there are no omissions, duplicates,
extras, reordered identities, changed hashes, or unclassified entries. Trusted
`validate_trust_boundary` also passes.

All reconstructed `attributes` lists are empty, so there is no explicit
`simplification` rule to account for. In any event, every function equation is
classified `DEFINITION`, one of the two permitted classes for simplification.

## Independent classification judgment

The six `runSpec` rules are a constructor-complete, tail-recursive definition
of a named scanner summary. The empty case packages the state. The nonempty
cases consume one `Chars` constructor, so recursion strictly descends. For
`RP`, `PInt` is exhaustively and disjointly split into `zero`, `succ(zero)`,
and `succ(succ(D))`. The four `state*` rules define constructor projections,
and `separateSpec` defines the initialized named output term. These rules
define newly introduced proof vocabulary; they do not rewrite a program AST,
the `<k>` cell, an environment cell, or another fixed-semantics operation.
They are definitions rather than operational bridges or mathematical
consequences asserted about pre-existing symbols.

The recurrences match the frozen program and operational K semantics:

- `SP` is ignored by the source conditional; depth/current/output remain
  unchanged and the loop binding makes the last character `SP`.
- `LP` is concatenated to `current` and increments `PInt` depth.
- `RP` is first concatenated to `current`. At `zero`, K's subtraction is
  saturating, so depth remains zero and the program appends/resets. At
  `succ(zero)`, subtraction reaches zero and likewise appends/resets. At
  `succ(succ(D))`, subtraction leaves `succ(D)`, so no append occurs and the
  extended current group is retained.
- `stateOutput` projects exactly the result list used by the loop invariant,
  while `separateSpec` supplies the source initial state.

I compiled a fresh copy of `semantic.k` plus `verification.k` using K
7.1.293. Controlled `krun` checks included balanced, spaced, unfinished, and
unbalanced counterexamples:

| Input | Frozen operational result |
|---|---|
| `""` | `[]` |
| `")"` | `[")"]` |
| `"(()"` | `[]`, with unfinished current group and depth one |
| `"())"` | `["()", ")"]` |
| `"( ) (( )) (( )( ))"` | `["()", "(())", "(()())"]` |
| `" (()) () "` | `["(())", "()"]` |

The adversarial `")"` and `"())"` cases specifically confirm the otherwise
easy-to-miss totalized depth-zero recurrence. A fresh `kprove` of both frozen
claims returned `#Top`. As a non-vacuity check, a separate temporary spec
changed only the end-to-end result to `OutList(.Outputs)`; `kprove` exited 1
with `WarnStuckClaimState` and the residual disequality between `.Outputs` and
`stateOutput(runSpec(...))`.

There is no rule claimed as `PROVED_DERIVED_LEMMA`, so no two-phase derivation
claim needs validation. There is also no rule that asserts a source-relevant
mathematical fact beyond defining the named summary. The independent true
`DOMAIN_LEMMA` set is therefore empty. No domain lemma has been mislabeled or
excluded from Stage 4.

## Deterministic Stage 4 and fixed target

I reran the mandated
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen K workspace, protected discovery manifest, selected generation, and
pinned toolchain lock.

The first call exposed a launcher-only PID namespace issue: Lean 4.22 obtains
its executable as `/proc/<getpid()>/exe`, but the managed sandbox exposes that
process only through `/proc/self`. This made `lake clean` report that it could
not detect the Lake installation. I recorded the failed call and diagnostic.
A minimal preload shim changes only `getpid()` to the procfs-visible PID read
from `/proc/self`; it does not edit or wrap any audit input, generator output,
Lean source, theorem, or toolchain file. With that process-identity workaround,
the unchanged trusted `check_generation` call succeeded. Its immutable
before/after snapshots also passed.

The fresh returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 export hash
  `f7198173f419636cacf3c009694d458c1c8113750de230e115a8bdfd24289f83`;
- Stage 3 manifest hash
  `1d658f9f3f836cd96386a95bf89aa4d0ae7883a6c174f3fd3bb21487b68e0357`;
- generated tree hash
  `ec2cabdd88613df091a482f8974a0b9be67d75d3d97827da8ff6ac78ae163e7a`;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0 with output hash
  `669037f0d20098cd4e0488a046a50dee67e38e9994f982b51afd0bd6f01a0ee7`,
  exactly equal to the recorded preflight;
- zero designated sorries; and
- 44 generated executable-hook trust declarations, exactly matching
  `trust-inventory.json`. The preflight independently rejects proposition
  trust; no target proposition exists.

The mathematical and structural obligation audit agrees:

- independently true domain rules: `[]`;
- `input-manifest.json.source_rules`: `[]`;
- `obligation-map.json.source_rules`: `[]`;
- `obligation-map.json.obligations`: `[]`;
- `obligation-map.json.trust_parameters`: `[]`;
- obligation-map SHA-256:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- generator and export obligation counts: zero;
- no omitted, duplicated, irrelevant, weakened, or vacuous conjunct exists;
- the trusted expected-target function returns `None`;
- the trusted generated-target scan returns `None`;
- `generator-manifest.json.target`, `preflight.json.target`, and the audit-input
  target are all `null`; and
- `Lemmas.lean` contains no `targetStatement` declaration.

Thus the source-rule/obligation relation is the exact empty bijection, and the
fixed generated target is correctly absent rather than changed or weakened.

## Stage 5 and evidence

Because this is `CLASSIFICATION_ONLY` and the legitimate domain set is empty,
there must be no Stage 5 proof. There is no candidate to copy or build, no
`Proof.final`, no target parameters, and no axiom printout to reconcile.
Attempting proof-mode checks here would contradict the recorded mode.

Raw commands and complete material outputs are under
[`evidence/`](/audit-output/evidence), with exact commands indexed in
[`COMMANDS.md`](/audit-output/evidence/COMMANDS.md). The key machine-readable
audits are
[`stage3_inventory_audit.py`](/audit-output/evidence/stage3_inventory_audit.py),
[`provenance_hash_audit.py`](/audit-output/evidence/provenance_hash_audit.py),
and
[`stage4_manifest_audit.py`](/audit-output/evidence/stage4_manifest_audit.py);
all exit successfully. The fresh preflight result is
[`22_fresh_check_generation.log`](/audit-output/evidence/22_fresh_check_generation.log).

VERDICT: PASS
LEGITIMACY: LEGIT
