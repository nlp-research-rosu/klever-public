# Independent audit: HumanEval `94-skjkasdkd`

Audit mode was `CLASSIFICATION_AND_PROOF`; condition was `kit-semantics`; the
semantics mode was `SUPPLIED_SEMANTICS`.

## Executive judgment

Stage 3 classification is correct, and Stage 4 is a deterministic, structurally
and mathematically faithful generation of the 13 true domain-lemma
obligations. The Stage 5 Lean project also clean-builds, states exactly the
fixed generated theorem, and has an acceptable axiom report.

The combined audit nevertheless fails because the candidate's operational
interpretations do not faithfully implement every bound KORE symbol. Most
decisively, generated target parameter `«_%Int_»` denotes K's truncating
remainder hook `INT.tmod`, but the candidate defines it as Lean `%`
(`Int.emod`). A live ground witness gives frozen K result `-2` and candidate
result `1` for `(-5, 3)`. This is the operational-bridge failure that determines
the final pair.

## Producer and immutable-input authentication

Before judging Stage 4, I hashed both mounted producer sources:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`

Each equals its entry in `source-manifest.json` and its corresponding field in
`generator-manifest.json`. The producer tree's pipeline digest is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
equal to `/audit-input.json`. The source manifest, generator manifest, and the
image-identified audit-input source path all bind the same immutable image:
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
There is no producer-provenance `AUDIT_ERROR`.

All 810 per-file Stage 1 source hashes in `/audit-input.json` were recomputed
and matched. The mounted Stage 1, Stage 2, Stage 4 generation, generated
project, producer-source, Stage 3 manifest, and candidate tree digests also
matched their launcher records under the appropriate pipeline/export digest
algorithms. The launcher records a Lean-invocation digest but does not mount
that invocation among the declared audit inputs; the mounted candidate itself
does match `lean_workspace_sha256`.

## Rule inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code on the
frozen Stage 1 workspace produced:

- verification main module: `VERIFICATION`;
- local verification-module closure: `VERIFICATION` only;
- rule count: 33;
- canonical inventory hash:
  `1858c992ef1e9a6b842e6b7d36b1e30b8abe0e686374e68b1766d4f9cb1e3824`.

For every rule I independently re-extracted the recorded line span, normalized
the exact rule text, recomputed its SHA-256, and reconstructed
`source_rule_id = "rule-" + normalized_sha256`. All 33 spans, normalized
hashes, and identities matched. The ordered identity list equals the protected
Stage 3 list exactly; there are no omissions, duplicates, extras, reorderings,
or altered hashes.

## Independent Stage 3 classification

The source program scans an integer list for its largest prime, then sums that
prime's decimal digits. The Stage 1 target executes the translated function
body and summarizes the scan with `largestPrime`, primality with `primeTail`,
and the final loop with `digitSum`.

My independent classification is 20 `DEFINITION` rules and 13
`DOMAIN_LEMMA` rules, exactly matching Stage 3. There are no local
`OPERATIONAL_RULE` entries and no `PROVED_DERIVED_LEMMA` entries.

The 20 definitions are:

- exact named statement macros at lines 9–16, 19–35, 38–43, and 46–56;
- `allInts` base/recurrence at 61 and 62–63;
- `definedProjectInt` at 69;
- the primary guarded `projectIntTotal` equation at 78–80 and its Int collapse
  at 86;
- `primeTail` totalization/base/primary recurrence at 120–121, 122–123, and
  124–128;
- `isPrime` at 145–146;
- both guarded `selectPrime` branches at 150–151 and 152–153;
- all three structural `largestPrime` equations at 157, 158–160, and 161–163;
  and
- the `digitSum` base and primary recurrence at 167–168 and 169–173.

Each of these introduces or recursively defines a named macro, summary, or
proof term. None rewrites an ordinary machine configuration as an execution
rule.

The 13 domain lemmas are:

| Frozen span | Independent reason and program relevance |
|---|---|
| 74–76 | Unproved definedness characterization of the pre-existing Val-to-Int cast; required for integer projection. |
| 82–84 | Unproved reverse symbolic cast/projection orientation; required for dynamic list elements. |
| 87–89 | Unproved projection-idempotence simplification. |
| 93–96 | Guarded dynamic-Val `>` dispatch used by the scan/digit loops. |
| 98–101 | Guarded dynamic-Val `>=` dispatch used for `value >= 2`. |
| 103–106 | Guarded `<` dispatch used by `divisor < value`. |
| 108–111 | Guarded `%` dispatch used in primality testing. |
| 113–116 | Guarded `+` dispatch used by `largest = value + 0`. |
| 133–137 | Unproved zero-remainder shortcut for the primality summary. |
| 138–142 | Unproved backward `primeTail` fold for the incremented divisor invariant. |
| 174–178 | Unproved reverse fold of the positive `digitSum` recurrence. |
| 179–184 | The same fold after supplied-semantics remainder normalization. |
| 185–191 | Unproved accumulator-lifted digit-sum fold and reassociation. |

All 13 are materially connected to the frozen integer projection, primality
loop, or digit-sum postcondition. Every inventory rule carrying a
`simplification` or `simplification(...)` attribute is classified as either
`DEFINITION` or `DOMAIN_LEMMA`.

No rule qualifies as a proved derived lemma: `prove.sh` compiles
`verification.k` once with every rule already installed, then runs all claims
against that same definition. It never first proves an exact inventory rule
against a module that omits it and then uses it later.

## Stage 4 deterministic generation

I directly reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
`/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock. It returned
`PASS`, with `lake clean` and `lake build` both exiting 0.

The returned identities match the audit input and manifests:

- Stage 1 export:
  `a479ffc26d0888a54bafb361e930785a3b05365b6aba1bdcd36c5437b2e6b324`;
- Stage 3 manifest:
  `96e36beab2d7540a7fb8eb90be52dc480a387490a00e35df62c753a106123002`;
- generated tree:
  `d39652423da4b22eeaa43a473205673f746e535ba4d94082c472acd874151e0e`;
- obligation-map file:
  `bb2491e2df0794d7ec4cfaa25fb3c67baae828339a3e6d3ae26ce9119422fc91`.

The independently found 13-domain-rule ordered identity list equals both
`obligation-map.json.source_rules` and the 13 obligation identities. Every
source span, normalized rule hash, inventory hash, discovery-manifest hash, Lean
conjunct hash, and obligation count matches. Each obligation retains the exact
K variables, guard, sides, and operation. There are no omitted, duplicated,
irrelevant, weakened, or top-level-vacuous obligations. The first obligation's
nested `True` is the exact lowering of `#Ceil(V)` for an already typed variable;
the enclosing cast-definedness equivalence is not vacuous.

The fixed target is:

- declaration: `Klean94Skjkasdkd.Lemmas.targetStatement`;
- file: `Klean94Skjkasdkd/Lemmas.lean`;
- definition hash:
  `59d9bcf3f62a054d1f933d400dbfa78e5797720737511640b2dd0f953d4837db`;
- applied statement hash:
  `697b0dbcd4c7e94800f6ee2a3079030a59743d59cf5c3b936fb9d8135ddf80b9`.

The source-derived target, generator manifest, and `/audit-input.json` agree
exactly. Because the independently confirmed domain set has 13 entries, this is
correctly a normal `PASS` generation, not `KLEAN_NO_OBLIGATIONS`.

## Stage 5 build, proof identity, and trust

I copied the candidate to the fresh directory
`/tmp/audit-work/stage5-audit.fQnODm`, copied the immutable generated project
into it as `Base`, and ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, “Build completed successfully.”

The trusted candidate gate found exactly one `def` for every target parameter,
no candidate definition of or namespace shadow for `targetStatement`, and
exactly one `Proof.final`. Its normalized theorem type is the manifest's fixed
applied statement exactly, so it is neither a duplicate nor a weakened or
vacuous variant. The candidate contains no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque`.

Running Lean with `#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

The trusted mechanical gate explicitly includes this Lean-core trio in its base
allowance and then adds the 42 declarations recorded by
`trust-inventory.json`. No generated allowlist axiom is actually a dependency
of `Proof.final`; there is no `sorryAx` and no candidate-introduced or
unrecorded proof trust escape. Thus the build, theorem identity, and axiom
accounting all pass.

The audit sandbox initially prevented Lean/libuv from resolving
`/proc/<pid>/exe`. Evidence includes the first failure and a narrowly scoped
preload shim that answers only that process-image lookup with the immutable
pinned toolchain path. With it, Lean identified itself as version 4.22.0,
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.
The shim does not alter Lean sources, project files, elaboration, or kernel
checking.

## Operational-bridge audit

The exact 21-definition accounting is in
[`evidence/09-parameter-audit.md`](/audit-output/evidence/09-parameter-audit.md).
Subtraction, Boolean conjunction, integer comparisons, addition, truncating
division, the guarded projections, `digitSum`, `primeTail`, and normalized
`pyMod` agree with their frozen meanings on their defined domains.

Three bound whole-symbol interpretations fail the stricter required bridge
check:

1. `Proof.«_%Int_»` is defined as Lean `x % y`. Frozen
   `verification-kompiled/definition.kore` binds the parameter's exact KORE
   symbol to `INT.tmod`. Live evaluation records:

   - frozen K: `-5 %Int 3 = -2`;
   - candidate: `Proof.«_%Int_» (-5) 3 = 1`;
   - Lean reference: `Int.tmod (-5) 3 = -2`,
     `Int.emod (-5) 3 = 1`.

   Both implementations return 7 on `(17, 10)`, which explains why the
   positive decimal obligations can be proved despite the wrong complete
   operation.

2. The candidate's bound `applyBin` implements only an integer/Boolean subset
   and returns `noneV` elsewhere. Supplied `float.k:32` operationally rewrites
   integer true division `applyBin("/", 1, 2)` to `divII(1, 2)`, while the
   candidate adversarial probe returns `noneV`.

3. The bound `applyCmp` similarly returns `false` outside integer/Boolean
   projections even though the supplied semantics defines Float, String, list,
   tuple, set, dictionary, and `noneV` comparison cases.

As a counterfactual sensitivity check, I changed the unmodeled integer
true-division branch of `applyBin` to the hard-coded result `999` in an
isolated copy. Both `lake clean` and `lake build` still passed, and a probe
confirmed that result. This demonstrates that the exact target theorem checks
the source-linked branches but cannot certify the whole KORE-symbol
implementation. Under the explicit audit instruction that every target
parameter must implement the frozen operational meaning, the live `%Int`
counterexample alone is sufficient for `FAIL`/`NOT_LEGIT`; the dispatch
counterexamples independently reinforce it.

## Evidence index

- Producer source/image authentication:
  [`01-producer-authentication.out`](/audit-output/evidence/01-producer-authentication.out)
- Full reconstructed inventory and bijection:
  [`02-rule-inventory.json`](/audit-output/evidence/02-rule-inventory.json)
- Independent per-rule classifications:
  [`03-independent-classification.json`](/audit-output/evidence/03-independent-classification.json)
- Required preflight result:
  [`04-klean-preflight.out`](/audit-output/evidence/04-klean-preflight.out)
- Independent hashes, obligations, and target:
  [`05-stage4-integrity.json`](/audit-output/evidence/05-stage4-integrity.json)
- Fresh clean build and exact axiom output:
  [`06-stage5-build-and-axioms.out`](/audit-output/evidence/06-stage5-build-and-axioms.out)
- Trusted Stage 5 mechanical gate:
  [`07-stage5-mechanical-gate.out`](/audit-output/evidence/07-stage5-mechanical-gate.out)
- Live adversarial and counterfactual runs:
  [`08-operational-bridge-probes.out`](/audit-output/evidence/08-operational-bridge-probes.out)
- Candidate forbidden-token and target-shadow scan:
  [`10-candidate-source-scan.out`](/audit-output/evidence/10-candidate-source-scan.out)

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
