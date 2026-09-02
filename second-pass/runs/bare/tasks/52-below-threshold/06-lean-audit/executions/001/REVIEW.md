# Independent Stage 3/4 Audit: `52-below-threshold`, `bare`

## Result

The protected Stage 3 classification is complete and mathematically correct.
The frozen local verification-module closure contains exactly three rules. Each
is a genuine definition: two equations define the recursive summary
`allBelow`, and one macro equation defines the named proof term
`solutionProgram`. There is no `DOMAIN_LEMMA`, so Stage 4's
`KLEAN_NO_OBLIGATIONS` result, empty obligation map, and absence of a generated
target are the correct deterministic outputs.

The launcher and environment both select `CLASSIFICATION_ONLY`. No `/candidate`
exists, and all Stage 5 paths, hashes, results, and target fields in the audit
input are null. Stage 5 proof, axiom, and operational-bridge checks therefore do
not apply.

I did not rely on the selected Stage 2 review or any prior PASS statement. I
treated mounted source, manifests, logs, and comments only as evidence and used
the locked trusted tools plus independent source/semantic analysis.

## Audit-input and trusted-tool authentication

`AUDIT_MODE` and `/audit-input.json` both state `CLASSIFICATION_ONLY`. The
trusted `stage6_resolution_contract.verify_audit_input` check recomputed the
signed resolution digest as
`2ea25aed27f61fe9afd664af26f56213ffb4d55152a649c091716fb4f37f9e8d`,
exactly the recorded value.

The audit metadata records mechanical-checker lock hash
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`.
That is the actual SHA-256 of
`/opt/humaneval/data/klean-audit-tools.lock.json`. Every one of the eight
locked tool files under `/reference/tools` independently matched its per-file
hash, including `k_rule_inventory.py`, `lemma_discovery_contract.py`,
`klean_preflight.py`, `klean_export.py`, and `stage6_resolution_contract.py`.

The launcher-recorded hashes were independently recomputed:

- Stage 1 full tree:
  `08cd07c4989c2c1d70ef03650a7f884cfc26a5488e8da37c8c1528ac309d1d6a`.
- Stage 1 deterministic export tree:
  `60fa7f174596971e65b98b83670c66aac94d5f45a95c3a8ed5c7737df29e894a`.
- Stage 2 selected audit tree:
  `092f285f26ccea3d8c9ab912b9c89029ec0079027f999bda6079cfe7f32711fe`.
  This authenticates the mount but was not used as a judgment.
- Stage 3 manifest:
  `b4e729dfb54d2a7b6a92c4ff5cdee1745631ba70bb77c1f8ac2de8ac542c6838`.
- Stage 4 full generation tree:
  `6d7c5004903dc112ec3c778a35547051087a4bfe60d4acac0f911b6e58728d91`.
- Generated Lean project tree:
  `a173e6ae9c76310f17386904e774c2b05be2a70f89e48122822d834612bf8701`.
- Generation producer-source tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`.

The complete Stage 1 per-file hash map also exactly matches the audit input.

## Stage 4 producer authentication

This check was performed before judging Stage 4. The mounted producer bundle
has exactly three regular files: `klean_export.py`, `klean.py`, and
`source-manifest.json`.

The observed producer hashes are:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`.
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`.

Both values exactly match the source manifest and `generator-manifest.json`.
The immutable image identity is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in all three bindings: generator provenance, the producer source manifest, and
the image-key component of the producer path recorded in `/audit-input.json`.
There is therefore no producer-source infrastructure error.

## Inventory reconstruction and bijection

Using the locked `tools.k_rule_inventory.inventory_verification` implementation,
I reconstructed the local closure rooted at the frozen `verification.k` main
module. The closure is exactly `["VERIFICATION"]`. `MPY` is imported from
`semantic.k`, not defined in the local `verification.k` module closure, so its
ordinary execution rules are correctly outside this Stage 3 inventory.

The frozen `verification.k` SHA-256 is
`b7c1fa3dd85aa9ae2f86be343439b418add64496fe3b1477818c95addcbac005`.
For every reconstructed rule, I separately extracted the recorded source lines,
normalized them by whitespace, recomputed SHA-256, and checked that
`source_rule_id` is exactly `rule-<normalized_sha256>`.

| Order | Source span | Recomputed normalized SHA-256 / identity | Attributes | Independent class |
|---|---:|---|---|---|
| 1 | 8–8 | `a8176184e1ba57504866732ee5f4ad5ab8fcf8101c60b1b27722cc122c120ec4` | none | `DEFINITION` |
| 2 | 9–10 | `0208a16b17f61f199b8fd1d9c5435b9b71da6c6ce49cbbca4ffed14d285fb668` | none | `DEFINITION` |
| 3 | 14–21 | `50c5600cfb11ade9a3062a0751132a38f4a48d7f51e504490c6e5b59f0180ffb` | none | `DEFINITION` |

The recomputed canonical whole-inventory hash is
`b61d51764fcfdac4ac6068281265d2facfb383d36204fe8701f301f324d367bb`.
It matches the trusted reconstruction, Stage 3 manifest, Stage 4 input
manifest, and generator provenance.

The Stage 3 manifest contains exactly three entries and exactly the ordered
identity sequence above. There are no missing, extra, duplicated, or reordered
identities. The trusted
`lemma_discovery_contract.validate_trust_boundary` check also passes. Because
all three rule attribute lists are empty, there is no `simplification` rule
whose classification needs an additional restriction.

## Independent classification and semantic judgment

The rule at line 8 is the base equation
`allBelow(nil, _T) => true`. It defines the empty-input case of the fresh
`[function, total]` summary. It does not assert a fact about a pre-existing
symbol. It is a `DEFINITION`.

The rule at lines 9–10 is the recurrence
`allBelow(cons(I, XS), T) => (I <Int T) andBool allBelow(XS, T)`. It defines
the nonempty case, recursively descends to the strict tail, and is disjoint
from the `nil` case. Together, the two equations cover the `IntSeq` constructors
without overlap. It is a `DEFINITION`, not a domain lemma.

The rule at lines 14–21 expands the zero-argument `[macro]` symbol
`solutionProgram` to the translated `below_threshold` module AST. Its function
name, parameter order, loop target and iterable, `x >= t` comparison, early
`false` return, empty else branch, and final `true` return agree exactly with
the frozen source and `solution.mpy`. It is a macro/named proof-term
`DEFINITION`.

Operationally, `semantic.k` boots by binding the input `IntSeq` and threshold,
evaluates the iterable, consumes it left-to-right, and binds each head to `x`.
For each head it evaluates `x >= t`. A true comparison executes
`Return(false)`, which discards the remaining computation and records false; a
false comparison executes the empty branch and continues. Exhausting the list
executes `Return(true)`. Thus the operational result is true exactly when each
integer satisfies `x < t`, which is precisely the recursive `allBelow`
definition.

Boundary and counterfactual checks discriminate the intended strict relation:

- `nil` gives true for every threshold.
- `cons(T - 1, nil)` gives true.
- `cons(T, nil)` gives false.
- `cons(T + 1, nil)` gives false.
- A below-threshold prefix followed by `T` gives false rather than ignoring the
  later element.

Replacing `<Int` with `<=Int`, making the summary constant, or dropping the
recursive tail changes at least one of these cases and disagrees with the
frozen operational execution. The two summary equations are relevant to the
postcondition, and the macro is the exact program term used by both claims.
There is no irrelevant rule and no hidden `DOMAIN_LEMMA`.

The resulting independent partition is:

- `DEFINITION`: 3.
- `OPERATIONAL_RULE`: 0.
- `PROVED_DERIVED_LEMMA`: 0.
- `DOMAIN_LEMMA`: 0.

No rule is being accepted as a proved-derived lemma, so no two-phase
prove-without-then-use claim is involved.

## Deterministic Stage 4 generation

The independently established true domain set is genuinely empty. The Stage 4
input manifest therefore correctly has `source_rules: []`. The generated
`obligation-map.json` has:

- `source_rules: []`;
- `obligations: []`;
- `trust_parameters: []`.

Its observed SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
exactly the generator-manifest value. All generator, export, preflight, and
audit-input obligation counts are zero. There are no omissions, duplicates,
weakened obligations, irrelevant conjuncts, or vacuous conjuncts: no conjunct
exists because no domain rule exists.

The trusted target parser independently returns `None`. The generator manifest,
recorded preflight, and audit input all also record `target: null`. Hence there
is no generated target declaration, statement, or hash that could have been
changed. This null target is the required fixed output for the empty domain
set, not a weakened theorem.

## Mandated preflight rerun

I ran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the frozen Stage 1 workspace, protected Stage 3 manifest, Stage 4 generation,
and pinned `/reference/klean-toolchain.lock.json`.

The first invocation exposed an audit-container toolchain issue: Lean's runtime
looked up `/proc/<namespace-pid>/exe`, but this container exposes the executable
only through `/proc/self/exe`. Consequently Lake could not identify its
installation before building. I recorded that failure rather than treating it
as a proof result.

For the rerun I compiled a narrow `LD_PRELOAD` shim under `/tmp/audit-work`
which changes only `readlink` requests shaped as `/proc/*/exe` to
`/proc/self/exe`. With `ELAN_HOME=/opt/elan`, `lean --version` reported Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the pinned
toolchain. A separate copied-project smoke test clean-built successfully.
Neither the shim nor the preflight mutated a frozen input; preflight itself
copies the generated project to a fresh temporary directory.

The mandated rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0;
- build-output SHA-256
  `22d7724241c716545b65ac7fcd0ff7fa27724aeb368eeb4fb0f4c59b35076db1`;
- obligation count 0;
- target null;
- designated-sorry count 0;
- 41 generated computational trust declarations, exactly reconciled with the
  Stage 4 trust inventory and rejected by the checker if proposition-like.

The entire rerun result is byte-for-value equal as a JSON object to the
recorded `preflight.json`. The trust-inventory SHA-256 is
`3875aad025caed8a9200006cc2492390329a56c23c3bfec7e9b9a2c5ea684694`,
matching `export-result.json`. The authenticated generated-tree hash before and
after the rerun remained unchanged.

## Stage 5 applicability

This is not proof mode. `/candidate` is absent, as required for
`KLEAN_NO_OBLIGATIONS`. The launcher records no Lean workspace, invocation,
Stage 5 result, target, or candidate hashes. There is therefore no
`Proof.final`, candidate definition, target shadowing, or axiom dependency to
audit. Running a Stage 5 `#print axioms Proof.final` command would be
inapplicable because no target or proof project exists.

## Evidence

Exact commands are listed in
[COMMANDS.txt](/audit-output/evidence/COMMANDS.txt). Principal raw results are:

- [Launcher input and mode](/audit-output/evidence/00-launcher-audit-input.txt)
- [Producer authentication](/audit-output/evidence/01-producer-authentication.txt)
- [Generation manifests](/audit-output/evidence/02-generation-manifests.txt)
- [Canonical inventory reconstruction](/audit-output/evidence/03-inventory-reconstruction.txt)
- [Independent integrity and bijection checks](/audit-output/evidence/04-independent-integrity-checks.txt)
- [Initial preflight environment failure](/audit-output/evidence/05-rerun-klean-preflight.txt)
- [Toolchain diagnosis](/audit-output/evidence/06-toolchain-diagnosis.txt)
- [Shim and copied-project clean-build test](/audit-output/evidence/07-toolchain-shim-smoke-test.txt)
- [Successful mandated preflight rerun](/audit-output/evidence/08-rerun-klean-preflight-success.txt)
- [Frozen source, K semantics, spec, and empty map](/audit-output/evidence/09-frozen-source-semantics-and-empty-target.txt)
- [Audit envelope and trusted-tool lock verification](/audit-output/evidence/10-audit-envelope-and-tool-lock.txt)
- [Exact preflight-result and trust-hash reconciliation](/audit-output/evidence/11-preflight-exact-match-and-trust-hash.txt)
- [Independent checker source](/audit-output/evidence/independent_checks.py)
- [PID/procfs shim source](/audit-output/evidence/proc-self-shim.c)

VERDICT: PASS
LEGITIMACY: LEGIT
