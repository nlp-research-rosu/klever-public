# Independent audit: HumanEval 114-minSubArraySum

## Scope and outcome

The launcher selected `CLASSIFICATION_AND_PROOF` for condition `semantics`
with `SUPPLIED_SEMANTICS`. I independently audited the frozen Stage 1 rule
closure, every Stage 3 classification, deterministic Stage 4 provenance and
generation, and the Stage 5 Lean proof. Candidate files, comments, prior
reviews, and prior PASS results were treated only as untrusted evidence.

The protected classification is correct, the true domain-lemma set contains
exactly one relevant rule, Stage 4 generates exactly that obligation, and the
candidate gives the bound K symbol an operationally faithful definition before
proving the exact immutable target.

## Producer provenance and frozen hashes

I hashed the mounted generation-time producers before judging Stage 4:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

These are identical in the observed files, `source-manifest.json`, and
`generator-manifest.json`. The immutable image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
it agrees between both manifests and the image-key basename recorded by
`/audit-input.json`. The producer bundle contains exactly the two producers and
its source manifest. Its recomputed pipeline tree hash,
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
also matches the audit input.

Every recorded hash with a mounted referent was recomputed. The Stage 1
pipeline tree, Stage 1 export tree, Stage 2 audit, Stage 3 manifest, complete
Stage 4 generation, generated project, producer bundle, and candidate Lean
workspace all match. Every individual entry in `stage1_source_hashes` also
matches exactly. The historical `lean_invocation_sha256` has no invocation
directory among the launcher-provided mounts and was not used as proof
evidence.

Evidence:
`evidence/01_environment_and_producer_hashes.txt`,
`evidence/02_manifests_and_audit_input.txt`, and
`evidence/03b_inventory_and_hash_reconstruction_corrected.txt`.

## Canonical inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` implementation, I
reconstructed the local closure selected by the last Stage 1 `kompile`
command. Its modules, in source order, are:

1. `VERIFICATION-BASE`
2. `VERIFICATION`

The reconstruction found 20 rules. For every rule I independently rechecked
the source span against the frozen source text, normalized the source by
whitespace, recomputed its SHA-256, reconstructed `source_rule_id` as
`rule-<normalized_sha256>`, and checked uniqueness. All checks pass.

- `verification.k` SHA-256:
  `dba7e68aec636257a66d3f4c1deede5a35af7c35a2d3a968eecf75d887c1e4c4`
- inventory SHA-256:
  `1fc51704b30efce23cfec3f8c1b390f5524a51919d6e82869f21eb471d67d6e4`

The protected Stage 3 list has the same 20 identities in the same order, with
no omission, duplicate, extra identity, changed span, or changed hash. The
Stage 4 input-manifest partitions also match the independently reconstructed
classification groups exactly.

## Independent classification of all 20 rules

| Frozen span | Source rule ID | Classification | Independent judgment |
|---|---|---|---|
| 10 | `rule-61708f547727d7aa918ad6bf8a016e92b25d1ccd0e36098b415347016593af3e` | `DEFINITION` | Empty case defining the `intVals` sequence embedding. |
| 11 | `rule-7e02eb37b7bdf1eab6f0857a5ba0eea03ae8d443148932837b9044d248811a1f` | `DEFINITION` | Recursive case defining the `intVals` embedding. |
| 16–17 | `rule-751f9db6408b37cdf73430964e3ffdf6029449e99f7d80a269006bc2640726e0` | `OPERATIONAL_RULE` | Empty-list iterator observation; it is the frozen MPY-LIST rule after the empty `intVals` reduction. |
| 18–20 | `rule-7c8aa5b4df16b8b39906d270756c36f651b19dbc8a1531df6aad58cd52b2c0ae` | `OPERATIONAL_RULE` | Nonempty iterator step; it preserves the MPY-LIST yield and remainder after one `intVals` reduction. |
| 24–25 | `rule-7a7edac73364fddfa1ef4bac81d105b3bf56b8eb38bcf5f58c3e0870f8a6ae55` | `DOMAIN_LEMMA` | An added simplification equation for imported `valSeqAt`; it is true but was not first proved separately. |
| 35–36 | `rule-ddb2a9a17afa83ccead9953239de6b8640bfdcb07b5d919d5f3fef6fd450df5a` | `DEFINITION` | First guarded equation of `chooseSmaller`. |
| 37–38 | `rule-e414c2c690c54d3aff26ea489493eeb2b52b5e37c1f5fe9ea0723203661776d9` | `DEFINITION` | Complementary guarded equation of `chooseSmaller`. |
| 41 | `rule-2e35ac88a7868a7de836211c573b73eb3fec197a29c6fc4b545dc0c1d4025164` | `DEFINITION` | Defines the next Kadane current value. |
| 44 | `rule-382008e7c331639bdf2122fb1e8e697a018e1932c7ffbb663b07a0d9ed4dab54` | `DEFINITION` | Base case of `kadaneCurrent`. |
| 45–46 | `rule-538263806e08f896295a8e43dccd79d3b2682d49dd3a83d0bf7be98bc05ce9ef` | `DEFINITION` | Recursive `kadaneCurrent` equation. |
| 49 | `rule-b77bb29211065f926011aeb07474c28374b27afe8225fbad12ea669ccda27918` | `DEFINITION` | Base case of `kadaneSmallest`. |
| 50–54 | `rule-b918679df7be71188a57e3b7f86189ff84457d4193215ebb54ca1eff52430469` | `DEFINITION` | Recursive `kadaneSmallest` equation. |
| 60–61 | `rule-6623a3796cfdcb66d4f69856565b76423d6a28be7027c5a7bdb641c2450f01f5` | `DEFINITION` | Defines the nonempty-input proof summary `minSubArraySumSpec`. |
| 64 | `rule-f6b2c49e4162bd80ca3acc1433e3738c91a600c1a77eeef3a64db19df4a925ab` | `DEFINITION` | Base case of the `lastFrom` recurrence. |
| 65–66 | `rule-0d184e0a169fc24d4d6b137dc9e8f1718d2e55996d8b9d719a063d075f6bad59` | `DEFINITION` | Recursive `lastFrom` equation. |
| 70–82 | `rule-bef95a832d9aafada0edddcd170407e7be2078dd45cfe2b96bc391a5c8445c58` | `DEFINITION` | Macro naming the exact translated loop body. |
| 87–96 | `rule-e17eaf3f5efc7de2b66d4005c595c668ad0317ec2b3235aa09c7c273a461e5e9` | `DEFINITION` | Macro naming the exact translated function body. |
| 99–103 | `rule-c9903e98ccf11645c2d85472b1e9045c58837512be5d1a0aa13530f3df954d4b` | `DEFINITION` | Macro naming the translated function definition. |
| 106–110 | `rule-ab94eb4e17ea649d7db0e05e93af0a499c8404ccaeeb0cd94c18f140105fb6db` | `DEFINITION` | Macro naming the translated closure value. |
| 119–145 | `rule-ebdc46c197940f4814a9d88d03be7d1724ee648b5ba27ec4399dcd5e0a3104a8` | `PROVED_DERIVED_LEMMA` | Exact loop reachability statement first proved by `LOOP-SPEC` against `VERIFICATION-BASE`, then used after compiling `VERIFICATION`. |

The sole `[simplification]` rule is therefore correctly a `DOMAIN_LEMMA`.
The two iterator rules are ordinary operational observations, not mathematical
domain facts. All remaining equations define summaries, recurrences, macros,
or named proof terms except the final loop theorem.

The loop rule and `LOOP-SPEC` have identical LHS, RHS, cells, variables, and
framing. Their raw normalized texts differ only because the reusable rule has
the rule-use attribute `[priority(30)]`; removing that attribute leaves
identical reachability statements. `LOOP-SPEC` imports only
`VERIFICATION-BASE`, where the rule is absent. `prove.sh` proves that claim
before compiling `VERIFICATION` and proving `FUNCTION-SPEC`.

The domain lemma is mathematically true: `intVals(iCons(I,R))` reduces to
`vCons(I,intVals(R))`, after which the supplied MPY-SUBSCRIPT equation
`valSeqAt(vCons(V,_),0) => V` applies. It is also relevant rather than
incidental: the frozen program initializes `smallest = nums[0]`, the translated
body contains that exact subscript, and the arbitrary nonempty symbolic input
is represented through `intVals(iCons(H,T))`.

Evidence:
`evidence/03b_inventory_and_hash_reconstruction_corrected.txt`,
`evidence/13_frozen_sources_and_semantic_comparison.txt`, and
`evidence/13b_exact_derived_lemma_comparison_corrected.txt`.

## Deterministic Stage 4 generation

I reran exactly `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the pinned toolchain lock.

The first attempt exposed an audit-container Elan process-path discovery issue:
`lake clean` could not detect its installation configuration. I did not load
the candidate's shim. I compiled a small audit-authored preload shim under
`/tmp/audit-work` that changes only `/proc/<pid>/exe` discovery, confirmed Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and reran the same trusted
check. The rerun returned `PASS`, and reproduced the stored clean/build output
hashes exactly.

The preflight and independent checks establish:

- one true domain source rule and one obligation;
- exact source-rule/obligation identity, order, source span, normalized hash,
  inventory hash, and discovery-manifest hash;
- obligation-map SHA-256
  `cbc23612a72e59d687baf4215cab047306406fd63e06b89971b0cfb317029369`;
- generated tree SHA-256
  `6e38574ff75db1815b3364face966f82834843ae54ebf9cb8ba537d84f236b9f`;
- no omission, duplicate, extra obligation, target change, or vacuous conjunct.

The generated conjunct is exactly:

```lean
∀ (_R : SortIntSeq) (I : SortInt),
  valSeqAt (intVals (iCons I _R)) 0 = SortVal.inj_SortInt I
```

This is a direct typed translation of frozen rule 24–25. It quantifies both
source variables, preserves index zero and the right-hand integer injection,
and neither weakens nor adds hypotheses.

The fixed target is:

- declaration:
  `Klean114Minsubarraysum.Lemmas.targetStatement`
- definition SHA-256:
  `6114caf7dfa5e63ce33d9edc594db631826b9dc04070eb895355d71e7e505316`
- statement SHA-256:
  `fe29b08b34a617cf692630f1f3b4055291980d4d6aa8972c5ed218eb9f664cba`
- parameter binding SHA-256:
  `5a83a7b72c6ddc251eb250a219c54f432e7c9e26024130fd50b1f89fda65d1b0`

The target reconstructed from the generated source is identical to the target
in the generator manifest, stored preflight, and audit input.

Evidence:
`evidence/04_rerun_klean_preflight.txt` records the initial environment failure,
`evidence/04b_rerun_klean_preflight_with_toolchain_shim.txt` is the successful
mandated rerun, and `evidence/14_toolchain_environment.txt` records the pinned
tool versions and audit-side shim hashes.

## Fresh Lean build, proof identity, and trust

I created `/tmp/audit-work/proof-audit`, copied the candidate project there,
and populated `Base` from the immutable generated project. Before and after
the build, `Base` had the exact generated-tree hash
`6e38574ff75db1815b3364face966f82834843ae54ebf9cb8ba537d84f236b9f`.

Both required commands succeeded:

- `lake clean`: exit 0
- `lake build`: exit 0, ending with `Build completed successfully.`

The only candidate Lean sources outside immutable `Base` are `Proof.lean` and
`lakefile.lean`. They contain no `sorry`, `admit`, or `unsafe`, introduce no
`axiom` or `opaque`, and do not declare or shadow `targetStatement`. The
generated project has exactly 47 trust declarations and they match
`trust-inventory.json` bijectively.

Lean prints the exact final type as:

```lean
theorem Proof.final :
  Klean114Minsubarraysum.Lemmas.targetStatement
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
```

Thus `Proof.final` is not a copied, weakened, or vacuous theorem. Running
`#print axioms Proof.final` produced exactly:

```text
'Proof.final' does not depend on any axioms
```

The dependency set is empty, so none of the 47 recorded generated axioms is in
the proof's kernel dependency closure. There is no `sorryAx` and no unrecorded
trust dependency.

Evidence:
`evidence/05_fresh_proof_workspace.txt`,
`evidence/06_lake_clean.txt`, `evidence/07_lake_build.txt`,
`evidence/08_print_axioms.txt`, `evidence/09_proof_identity.txt`, and
`evidence/12b_proof_static_and_target_checks_corrected.txt`.

## Operational bridge audit

There is one target parameter:

- Lean name:
  `«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»`
- type: `SortValSeq → SortInt → SortVal`
- KORE symbol:
  `LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int`
- source rule:
  `rule-7a7edac73364fddfa1ef4bac81d105b3bf56b8eb38bcf5f58c3e0870f8a6ae55`

The candidate has exactly one matching `def`, at `Proof.lean:17`. It is neither
constant nor hard-coded to the target case:

- on `vCons`, index zero returns the head;
- on positive indices it recurses on the tail with `index - 1`;
- on promoted `intVals`, it recursively implements the two frozen embedding
  equations;
- empty, negative, and out-of-bounds cases return `noneV`.

The last choice completes Lean's total function only where the supplied K
semantics intentionally leaves the `[total]` function abstract. It does not
contradict any K equation, and the source program's obligation is the valid
in-bounds head access.

I compiled independent universal checks showing:

1. the candidate satisfies both supplied `valSeqAt` equations for every value,
   remainder, and positive index;
2. for every `SortIntSeq` and every index, applying the candidate directly to
   promoted `intVals` is equal to applying it after fully expanding `intVals`
   with the two frozen K equations;
3. concrete witnesses `[7, -3, 42]` return `7`, `-3`, and `42` at indices
   0, 1, and 2, while negative/out-of-bounds cases take only the chosen total
   completion;
4. direct `vCons` witnesses preserve both head and recursive-tail behavior.

As a counterfactual, I defined a shortcut bridge that only recognizes the one
generated target pattern. It can prove the generated target by reflexivity but
fails the supplied `vCons` operational rule. The actual candidate passes that
same witness and the universal checks. A second mutation replacing the
function by a constant `noneV` is rejected by Lean on the generated target.
These results confirm that the clean theorem alone would be insufficient, but
the candidate's actual parameter definition implements the frozen operational
meaning.

Evidence:
`evidence/10c_bridge_validation_final.txt` records the successful universal and
adversarial Lean checks, while
`evidence/11_bridge_mutation_expected_failure.txt` records the expected
constant-mutation rejection.

## Final judgment

The true domain set is nonempty and contains exactly the selected
`valSeqAt` lemma, so Stage 4's `PASS` status and one fixed target are correct.
The Stage 3 classification is complete and mathematically sound, deterministic
generation is provenance-clean and bijective, and the Stage 5 proof establishes
the exact target with an honest operational parameter and no axiom dependency.

VERDICT: PASS
LEGITIMACY: LEGIT
