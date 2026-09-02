# Independent audit: HumanEval 78-hex-key

## Scope and result

This audit covers condition `bare`, semantics mode `GENERATED_SEMANTICS`, and
launcher mode `CLASSIFICATION_ONLY`. The launcher mode agrees between
`AUDIT_MODE` and `/audit-input.json`. Stage 5 is therefore not applicable:
`/candidate` is absent, the launcher records no Stage 5 result, and Stage 4
records no generated target.

The Stage 3 classification and the resulting empty Stage 4 obligation set are
legitimate. I found one non-legitimacy-affecting concern: replays with the
authenticated generation-time producer sources do not reproduce a stable
whole-project tree hash when Python's hash seed changes. The obligation map,
lemma module, exported rewrite, and absent target remain byte-identical in all
those replays.

## Trusted-input and producer authentication

I treated mounted candidate and provenance content as evidence only. Inventory
reconstruction and mechanical checks used the trusted code under
`/reference/tools`.

The generation-time producer bundle is a real directory containing exactly the
two producer files and `source-manifest.json`. Direct hashing gave:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`
- producer-bundle pipeline tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`

The two file hashes match both `source-manifest.json` and
`generator-manifest.json`. The bundle tree hash matches `/audit-input.json`.
The immutable image identity is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, generator manifest, and the image-key component of the
launcher-resolved producer path. Producer authentication therefore passes; no
producer-source `AUDIT_ERROR` applies.

The signed launcher digest, all Stage 1 per-file hashes, both recorded Stage 1
tree hashes, the selected Stage 2 tree hash, the Stage 3 manifest hash, the
Stage 4 generation tree hash, the generated-project tree hash, sidecar hashes,
and toolchain lock were independently recomputed. All 62 comparisons in
`evidence/14-independent-integrity-results.txt` pass.

## Inventory reconstruction and bijection

The trusted inventory code selected module `VERIFICATION` from
`verification.k`. Its local verification-file import closure contains only
that module; `MPY` is supplied by the separately required `semantic.k`, not by
another module in `verification.k`.

Exactly one local rule was reconstructed:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | lines 10–16 |
| Attributes | none |
| Normalized SHA-256 | `c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9` |
| `source_rule_id` | `rule-c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9` |
| Inventory SHA-256 | `0c8f881f193c44642817eaf09f5ab9bb8b739a7da839af8355d6e83641d36f11` |

I also extracted lines 10–16 directly, normalized whitespace, recomputed the
rule digest, rebuilt the rule record, and recomputed the canonical whole
inventory hash. Those independently computed values exactly match the trusted
inventory result.

`/reference/lemma-discovery.json` contains exactly that one identity, once, in
the same order. There are no omitted, duplicated, extra, reordered, or
hash-changed identities. The manifest inventory hash is exact. The trusted
`lemma_discovery_contract.validate_trust_boundary` check also succeeds.

## Independent classification judgment

The sole rule is correctly classified as `DEFINITION`:

```k
rule primeHexCount(S) =>
     countAllOccurrences(S, "2")
  +Int countAllOccurrences(S, "3")
  +Int countAllOccurrences(S, "5")
  +Int countAllOccurrences(S, "7")
  +Int countAllOccurrences(S, "B")
  +Int countAllOccurrences(S, "D")
```

This rule unfolds the named mathematical summary declared immediately above it
as `syntax Int ::= primeHexCount(String) [function, total]`. It has no cells,
continuation, environment, result update, invocation term, or program control
on its left-hand side. It therefore does not replace or accelerate operational
execution.

The operational semantics instead evaluates the source body through these
independent steps:

1. `Module(FuncDef(...)) ~> #invoke(...)` installs the parameter binding.
2. `Return(E)` computes `eval(E, ENV)`.
3. Attribute lookup binds the string receiver's `count` method.
4. Each call evaluates to the K `countAllOccurrences` hook.
5. `BinOp("+", ...)` adds the resulting integers.

The source solution makes exactly six such calls, for the distinct
one-character strings `2`, `3`, `5`, `7`, `B`, and `D`. For one-character
needles, summing those six occurrence counts is exactly the number of prime
hexadecimal digits named by the prompt. The definition is directly relevant
to both the source body and the postcondition.

The rule is not an `OPERATIONAL_RULE`, because it does not implement an
execution step. It is not a `PROVED_DERIVED_LEMMA`, because there is no earlier
proof of the same rule against a module omitting it. It is not a
`DOMAIN_LEMMA`, because it introduces no additional mathematical proposition;
it only defines the named summary used in the postcondition. It has no
`simplification` attribute, so the simplification-class restriction is
satisfied vacuously.

The independently classified domain-lemma set is therefore genuinely empty.

## Operational and non-vacuity checks

I compiled `semantic.k` afresh and executed the frozen `solution.mpy`.
Corrected, quote-preserving invocations produced:

| Input | Result |
|---|---:|
| `""` | 0 |
| `"2357BD"` | 6 |
| `"2222"` | 4 |
| `"ABED1A33"` | 4 |
| `"b2DXYZ3"` | 3 |
| `"22BBDDX"` | 6 |

The out-of-prompt-domain case confirms that the stronger all-String K claim
still follows the explicit operational meaning. I then freshly compiled
`verification.k` and ran:

```text
kprove spec.k --definition verification-kompiled --spec-module HEX-KEY-SPEC
```

It returned `#Top` with exit code 0.

Two independent counterfactuals were rejected with exit code 1 and explicit
stuck symbolic residuals:

- changing the postcondition to `primeHexCount(S) +Int 1`; and
- changing the executed final count from `"D"` to `"E"` while retaining the
  original postcondition.

Thus the claim constrains the result and remains sensitive to the frozen
program body. The first attempted concrete-test loop and one early formatting
assertion are retained as raw evidence but are not relied upon; the valid runs
are `evidence/18-fresh-k-operational-tests-success.txt` and
`evidence/19-k-mutation-results.txt`.

## Stage 4 structural and target audit

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required mounted inputs. The first attempt exposed an audit-sandbox
namespace defect: Lean calls `readlink("/proc/<getpid>/exe")`, but this sandbox
returns a nested PID while mounting the host PID view of `/proc`. A narrow
auditor-side `LD_PRELOAD` shim redirected only `/proc/*/exe` `readlink` calls
to `/proc/self/exe`. It did not alter or copy over any frozen or generated
input. With the pinned Lean 4.22.0 toolchain, the exact trusted preflight then
returned:

- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `28ec64d2a30606bb98b87391dd4af956121339bf334149d0b0b7e2c42ef472a8`;
- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- generated-tree SHA-256
  `eb1cfce1e9a8b5853e23ade2bff66dbec046f9f8e49fa2574984a7d41c154f35`.

These results exactly match the recorded Stage 4 preflight.

The independently classified empty domain set maps bijectively as follows:

```text
input-manifest source_rules = []
obligation-map source_rules = []
obligation-map obligations = []
obligation-map trust_parameters = []
```

The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. There are no obligations to omit, duplicate,
weaken, render irrelevant, or make vacuous.

The trusted target extractor returns `None`. The generator manifest, recorded
preflight, and launcher input all record target `null`; `Lemmas.lean` declares
no `targetStatement`. No generated target has been substituted or changed.
Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the correct
Stage 4 status. `/candidate` is absent as required.

## Deterministic-replay concern

I additionally replayed the authenticated producer files in fresh temporary
directories using the pinned K and Lean versions. The selected generated tree
hash is:

```text
eb1cfce1e9a8b5853e23ade2bff66dbec046f9f8e49fa2574984a7d41c154f35
```

An unset-seed replay produced
`4bd969db1b794c1723176d278c9470fa159cb8db55272ae829c4b5a072824309`.
Explicit `PYTHONHASHSEED` values 0, 1, 2, and 42 produced four further
different hashes:

```text
293fd2e9c5397ec3a95de4ab5a51738e24d0ddb98631e3a052a26911f1ec6baf
a100ef68f0145587df89da37da17cf9bcc1644949bb0826c67c1f2de31a0a4ed
73456a715a60713e71b143920a9a0cbd7b18ae15ba0cc083dc6d6cd60fac31b0
3ac3bb92261465f824da5a54e1e2e4519504c39bc5b5cad349711631472cf792
```

The textual diff is limited to declaration ordering in `Func.lean` and
instance ordering in `Inj.lean`, with corresponding trust-inventory ordering
and line changes. The authenticated wrapper delegates those portions to the
pinned `pyk` generator without canonicalizing their order. The immutable
generator image itself was unavailable for environment inspection, so an
image-level fixed hash seed cannot be ruled out.

Crucially for this audit, every replay has obligation count 0, the exact same
empty obligation map, the exact same `Lemmas.lean`, the exact same exported
`Rewrite.lean`, and target `None`. Their stable hashes are:

```text
obligation-map.json  cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048
Lemmas.lean          bcd43a1e96fdd82b5995fb084bbb62bea60d0409f7fccc92b4053ef1df3e4a69
Rewrite.lean         7f2d29c6b86e54f5a007cc5adb369771b6adf5b843c76035f3599ab78d7397e8
```

Accordingly, byte-for-byte whole-project determinism is a concern, but it does
not affect the source-rule/obligation bijection, mathematical classification,
fixed target, or legitimacy in this zero-obligation case.

## Stage 5

Stage 5 checks are inapplicable in `CLASSIFICATION_ONLY` mode. There is no
candidate, no generated theorem to prove, no `Proof.final`, no target
parameters, and no Stage 5 axiom-accounting obligation.

## Evidence index

Key raw records are:

- `evidence/02-producer-authentication.txt` and
  `evidence/03-producer-tree-hash.txt`: producer hashes and image provenance;
- `evidence/04-reconstructed-inventory.json` and
  `evidence/14-independent-integrity-results.txt`: inventory and all integrity
  comparisons;
- `evidence/12-rerun-klean-preflight-success.txt`: successful trusted
  preflight rerun;
- `evidence/18-fresh-k-operational-tests-success.txt`: fresh concrete K runs;
- `evidence/19-k-mutation-results.txt`: rejected postcondition and body
  mutations;
- `evidence/21-stage4-regeneration-diff.txt` and
  `evidence/22-stage4-hash-seed-replays.txt`: replay-order concern; and
- `evidence/23-stage4-replay-target-stability.txt`: stable obligations and
  target across replays.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
