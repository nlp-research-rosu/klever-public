# Independent Stage 3–5 audit: HumanEval 72-will-it-fly

Audit mode was `CLASSIFICATION_AND_PROOF`, condition `kit-semantics`, with
`SUPPLIED_SEMANTICS`. I treated all candidate text, prior reviews, comments,
logs, and recorded verdicts as untrusted evidence. The judgment below comes
from the frozen source, trusted inventory/checker code, fresh K theorem runs,
and a fresh Lean build.

## Result

The protected Stage 3 classification is complete and mathematically correct.
The deterministic Stage 4 project is provenance-bound to the immutable
producer, exports exactly the seven genuine domain lemmas, and preserves the
fixed target. The Stage 5 project clean-builds, proves exactly that target,
has no forbidden declaration or proof hole, uses only the permitted Lean
foundational axioms, and supplies operationally faithful definitions for all
18 target parameters.

## Producer and input provenance

I performed the required producer-source gate before judging Stage 4.

- `/reference/generation-tools/klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `/reference/generation-tools/klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- Generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

Both file hashes agree with `source-manifest.json` and
`generator-manifest.json`. The image ID agrees between those manifests and
the image-keyed producer path recorded in `/audit-input.json`. The producer
tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
exactly the audit-input value. The trusted `/reference/tools` copies are
byte-identical to the generation-time files. See
`evidence/01-producer-hashes.txt` and
`evidence/23-producer-provenance-verification.txt`.

Every launcher-bound hash for a mounted artifact matched independently:
the two Stage 1 tree encodings, all 827 Stage 1 file hashes, Stage 2 tree,
Stage 3 manifest, Stage 4 tree, generated tree, producer tree, Stage 5
workspace, and the resolved audit-input digest. The audit input also records
the Stage 5 invocation-tree hash, but that invocation directory is not among
the mounted audit inputs; it is non-load-bearing here because the mounted
candidate workspace matched its own recorded hash and was independently
rebuilt. Full results are in `evidence/06-recorded-hash-verification.txt`.

## Inventory reconstruction and classification

Using `/reference/tools/k_rule_inventory.py` directly on the frozen
`verification.k`, I reconstructed the local closure:

`VERIFICATION-SYNTAX`, `VERIFICATION-BASE`, `VERIFICATION`.

The frozen file hash is
`6940ce57128f334f266566af6feb86ce91ac165076da490066d7b5a75d4e1310`.
The inventory contains 38 unique rules in source order, with inventory hash
`11c89cc35585dc358ff90ecb064dc19d96b1288ea183620d0fdeb33f28bdc46d`.
For every rule I recomputed its module, start/end lines, normalized source
hash, and `source_rule_id`. The protected manifest has exactly the same 38
identities in exactly the same order. There are no omissions, extras,
duplicates, span changes, or hash changes. The full reconstructed rules are
in `evidence/02-reconstructed-inventory.json`; the ordered bijection is in
`evidence/03-inventory-bijection.txt`.

My independent classification is:

- 28 `DEFINITION` rules: the `integralV`/`floatV` classifiers; structural and
  accumulator equations for `allIntegral`, `allNumeric`, `hasFloat`,
  `sumInts`, `sumFloatRest`, and `sumToFloat`; the `reverseSlice` summary;
  guarded totalizer equations; and the exact `willItFlyClosure` macro.
- 7 `DOMAIN_LEMMA` rules: the three reverse projection equalities, the three
  projection-definedness (`#Ceil`) characterizations, and the guarded
  `intOf = intLikeTotal` equality.
- 3 `PROVED_DERIVED_LEMMA` rules: the reverse-slice continuation, integral
  sum fold, and mixed-float sum fold.
- 0 `OPERATIONAL_RULE` rules in this proof-local closure.

The seven domain lemmas are not definitions of the pre-existing K projection
or `intOf` symbols, and Stage 1 did not first prove them in a rule-free module.
They are relevant: the source computes `q == q[::-1] and sum(q) <= w`; the
projection and `intOf` facts support the Int/Bool and mixed-Float supplied
`sum` semantics.

The three operational-looking transitions qualify as derived lemmas. The
`SUMMARY-DEFINITION` closure excludes `VERIFICATION`; it first proves the
reverse-slice and integral-fold transitions. The integral-fold connection
claim has the same LHS, RHS, arbitrary suffix, and state footprint on the
broader `allIntegral` domain, so the later rule with the additional
`not hasFloat` guard is an immediate specialization. The float-rest
transition is first proved in the same bridge-free closure; then
`FLOAT-REST-VERIFICATION`, which still excludes `VERIFICATION`, proves the
mixed-float transition on the broader `allNumeric and hasFloat` domain. The
later rule adds `not allIntegral`, again a direct specialization. Stage 1's
connection builds precede the target build.

I reran all four connection claims separately. Each returned `#Top` with exit
code 0:

- `SUM-CONNECTION.reverse-slice`
- `SUM-CONNECTION.sum-fold`
- `SUM-CONNECTION.float-rest-fold`
- `FLOAT-SUM-CONNECTION.float-sum-fold`

The isolated output is in `evidence/05-connection-proofs.txt`, and the parsed
module closures are in `evidence/29-derived-proof-isolation.txt`. All 31 rules
carrying `simplification` or `simplification(...)` are classified only as
`DEFINITION` or `DOMAIN_LEMMA`; see
`evidence/28-simplification-policy.txt`. The complete 38-row independent
classification is `evidence/24-independent-classification.tsv` and agrees
exactly with Stage 3.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
over `/reference/k-proof`, `/reference/lemma-discovery.json`, and
`/reference/klean-generation`, using the pinned lock file. It returned
`status: PASS`, seven obligations, zero designated sorries, 54 recorded trust
declarations, and the expected hashes. The returned evidence is
`evidence/10-preflight-rerun.json`.

The audit sandbox initially exposed a PID-namespace defect: Lean calls
`/proc/<getpid()>/exe`, while this environment provides only
`/proc/self/exe`. A minimal `LD_PRELOAD` shim remapped only that failed
readlink. Its source and binary hashes are recorded in
`evidence/09-lean-shim-build-and-test.txt`; with it, Lean reports the pinned
4.22.0 commit and the unmodified checker reproduces the original successful
diagnostics. This workaround changes no project, theorem, compiler input, or
proof behavior.

The independent source-rule/obligation audit found an exact ordered
bijection:

1. guarded Int projection equality;
2. Int projection definedness;
3. guarded Bool projection equality;
4. Bool projection definedness;
5. guarded Float projection equality;
6. Float projection definedness;
7. guarded `intOf = intLikeTotal`.

Every span, normalized source hash, inventory hash, discovery hash, conjunct
hash, and binding hash matches. The `#Ceil` translations contain `∧ True`
because `#Ceil(V)` is true for a Lean constructor `V : SortVal`; this is a
faithful subterm, not a standalone padded obligation. Each surrounding
projection-definedness equivalence remains nontrivial. There are no duplicate,
irrelevant, weakened, or `True`-only obligations.

The generated target is unchanged and equals both the generator manifest and
audit input:

- declaration: `Klean72WillItFly.Lemmas.targetStatement`
- file: `Klean72WillItFly/Lemmas.lean`
- definition SHA-256:
  `94a9a9e0c3d745a5f03389b5c127916afd5a819af43b99213ee2b44e081e0b5a`
- application-statement SHA-256:
  `4a391d999651e6a5453216d82996a49970dc5345a811f2b131b4a124f8b0b254`

The complete structural recomputation is in
`evidence/22-stage4-independent-integrity.txt`, and the mathematical mapping
is in `evidence/26-obligation-mathematical-judgment.md`.

## Stage 5 proof identity and trust

I created the final fresh project at the path recorded in
`evidence/13-stage5-audit-path-final.txt`, copied only the candidate's four
root project files, and copied the immutable generated project directly as
`Base`. `Base` retained generated-tree hash
`454c5c339d4ebad1aba9684a8bf12183a28ea175512bc07110eed65e27d629b4`.

In that fresh project:

- `lake clean` exited 0;
- `lake build` exited 0 and built `Proof`;
- the candidate contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`;
- it defines every one of the 18 target parameters exactly once;
- it does not declare or enter the generated target namespace;
- it declares exactly one `Proof.final`; and
- Lean checks `Proof.final` at the exact generated target application.

Complete build output is in `evidence/14-stage5-clean-build-final.log`.
Target and source-integrity results are in
`evidence/15-target-and-candidate-integrity.txt`. The trusted independent
proof gate also returned `PASS`; see
`evidence/17-trusted-proof-gate.json`.

The exact Lean dependency line is:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

There is no `sorryAx`. `propext` and `Classical.choice` are the standard Lean
foundational axioms explicitly permitted by the trusted proof gate. None of
the 54 generated allowlisted axioms is a dependency, and there is no
unrecorded or unpermitted dependency. The full `#check`, `#print`, and
`#print axioms` output is `evidence/16-print-axioms.txt`; reconciliation is
`evidence/30-axiom-accounting.txt`.

## Operational bridge for all target parameters

I located and reviewed every exact candidate `def`; the 18-row audit is in
`evidence/27-target-parameter-audit.tsv`.

- `_andBool_` and `notBool_` implement the supplied Boolean truth tables.
- `isInt`, `isBool`, and `isFloat` are exactly the definedness observations
  of singleton K sort projections.
- `integralV` and `floatV` reproduce the frozen mutually exclusive
  classifiers.
- `project:Int?`, `project:Bool?`, and `project:Float?` extract exactly the
  corresponding singleton injection and return `none` otherwise.
- The three value projections and three `project*Total` definitions return
  the exact injected payload wherever the frozen rules apply.
- `intLikeTotal` and `intOf` both implement Int identity and Bool-to-0/1 on
  their complete guarded operational domain.

The total Lean types require completion outside the defined K projection and
`intOf` domains. The candidate's defaults occur only there: all exported rules
guard those uses, and the optional projections independently preserve
definedness. No default is reachable as a substitute for a frozen operational
value.

Adversarial Lean checks covered all four Boolean combinations, negative and
positive Ints, both Bool values, a Float, a nonnumeric `SortVal`, and a
non-value continuation. Results agree with the supplied semantics; the final
run is `evidence/21-operational-bridge-tests-with-mutations.txt`.

Counterfactual checks were discriminating:

- a constant-zero `intOf` fails at integral value 42;
- a constant-false `isInt` fails the projection-definedness fact; and
- coordinated constant `project:Int`/`projectIntTotal` definitions can satisfy
  their relational equality while returning the wrong value at 42.

The last mutation confirms why the clean theorem alone is insufficient. The
actual candidate is not that convenient model: its ground extraction returns
the frozen values (`-7`, `42`, Bool `0/1`, and Float `1.5`) and rejects
non-value continuations.

## Evidence summary

Raw commands, exact outputs, reconstructed JSON, source-level tables, shim
source, and Lean adversarial artifacts are under `/audit-output/evidence/`.
The initial preflight and first incorrectly nested fresh-copy attempts are
retained as failed setup evidence; the final successful runs are clearly
identified by `10-`, `14-`, `17-`, and `21-`.

VERDICT: PASS
LEGITIMACY: LEGIT
