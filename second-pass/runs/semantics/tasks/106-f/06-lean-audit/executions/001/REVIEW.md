# Independent audit: HumanEval 106-f

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Determination

The Stage 3 classification is complete and behaviorally correct, the Stage 4
generation is deterministic and preserves all four genuine domain obligations,
and the Stage 5 Lean candidate proves the exact fixed target with the honest
operational meaning of `valSeqConcat`. The proof builds from a fresh copy and
`Proof.final` has no axiom dependencies.

I treated the prior Stage 2 review, all candidate comments and logs, and all
recorded earlier verdicts as untrusted evidence. No conclusion below depends on
their asserted result.

## Producer and input integrity

The producer-source gate passed before judging Stage 4:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`
- immutable generator image:
  `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
- producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`

The two file hashes match `source-manifest.json` and
`generator-manifest.json`. The image ID matches both manifests and the final
component of the launcher-selected producer-source path in `audit-input.json`.
The producer-source tree matches the launcher digest. There is therefore no
producer provenance `AUDIT_ERROR`.

Every hash for a mounted audit object was independently recomputed. This
included both Stage 1 tree encodings, every launcher-recorded Stage 1 source
file, the discovery manifest, selected Stage 2 audit, selected Stage 4
generation, generated project, producer sources, candidate workspace, all
selection bindings, and the signed-resolution digest. The final structural run
passed 105/105 checks. The historical Stage 5 invocation directory itself is
not mounted; its launcher-only tree digest was not used as proof evidence. The
mounted candidate workspace digest and the Stage 5 result's workspace digest
both match.

Key identities are:

- selected Stage 1 tree:
  `1369b7138cef1abb312f9a4df2385ddac78e42c82509a9c3cd81a12a5979d840`
- frozen Stage 1 export:
  `2bb2321a2e7bb6acc4c81a8a8070cca7b0a46768f9dcb06168b813e999c9e34d`
- discovery manifest:
  `cd5a215d73f441e91cef5b00ac023703e39d736318f40555997847e520f4aeb1`
- selected Stage 4 generation:
  `694051201f468aa7f0e050e79e85a2f3808e4913100f60225298febda91ed3a9`
- generated project:
  `28a0a77725572cb855f104669609c845fb88e7d3772f018d1ca3c7be0b007932`
- candidate workspace:
  `d37cbd73afc07238e57bc32f23d7cafd24eeeebd71213f49a08a3f3880f44c86`

Evidence:
[producer identity](/audit-output/evidence/01b_producer_identity.log),
[final structural checks](/audit-output/evidence/06c_independent_structural_checks_final.log).

## Inventory reconstruction

Using the trusted rule-inventory implementation on the frozen
`verification.k`, the local verification-module closure is exactly
`VERIFICATION`. It contains seven rules, in source order. For each rule I
recomputed its exact source span, whitespace-normalized SHA-256,
`source_rule_id`, and the canonical whole-inventory hash.

The inventory hash is
`a51d8b2c346e72b06c592a426e9e98ee5acf2554dd48cf0c23e835041070ae4e`.
The protected discovery manifest has exactly the same seven identities in the
same order, with no omission, duplicate, extra identity, hash change, or
unaccounted classification.

| Lines | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 10–11 | `rule-55fa05d4b7990a68e203e8b15296e11489577bd53e5c352747785f464ae79cf1` | `DEFINITION` | Base equation of the named `outputOK` summary. |
| 12–16 | `rule-db034c4631f6721f201f955ef113ee2a18fe8458a2e631d046dc5323df2d45ce` | `DEFINITION` | Even-index recurrence of `outputOK`. |
| 17–21 | `rule-7f063b6288ed1ca9af618a843891c9fb41fc39c7ea5c85c2cba58238be877bf7` | `DEFINITION` | Odd-index recurrence of `outputOK`. |
| 25–27 | `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97` | `DOMAIN_LEMMA` | Associativity of pre-existing `valSeqConcat`. |
| 28–29 | `rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa` | `DOMAIN_LEMMA` | Right identity of pre-existing `valSeqConcat`. |
| 32–35 | `rule-4bb6de9678be64ad9a5dbb1d96a9acd747002bd379e02e9adb311bd159bf6396` | `DOMAIN_LEMMA` | Left cancellation of a common sequence prefix. |
| 36–38 | `rule-6b49fce56fe800f0a53b8ec7f41fec54b9db95c08b9bd8d56dde0b6720d71d84` | `DOMAIN_LEMMA` | A finite sequence cannot equal itself followed by a nonempty suffix. |

There are no local `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.
Stage 1 first proves a loop claim and later trusts that claim, but it never
first proves any of these four exact algebraic rules against a module that
omits the rule. Calling them proved-derived would therefore be invalid.

All four `[simplification]` rules are classified as `DOMAIN_LEMMA`; none is
mislabeled as a definition or operational rule. They are relevant. The source
program appends one computed integer on every loop iteration, supplied
semantics updates the heap list from `VS` to
`valSeqConcat(VS, vCons(V, .ValSeq))`, and the invariant frames the produced
suffix as `valSeqConcat(PREFIX, OUTPUT)`. Associativity and right identity
normalize successive appends, while cancellation exposes the invariant's
existential suffix. The three `outputOK` equations directly describe the
factorial/triangular values in the postcondition.

Evidence:
[inventory and protected classification](/audit-output/evidence/02_inventory_and_discovery.log),
[frozen program and specification](/audit-output/evidence/03_frozen_sources_and_semantic_refs.log),
[relevant operational semantics](/audit-output/evidence/03b_relevant_operational_semantics.log).

## Stage 4 generation and obligation judgment

The required fresh call to
`tools.klean_preflight.check_generation`, with `PYTHONPATH=/reference`, passed
after `lake clean` and `lake build` both exited 0. It returned:

- status `PASS`;
- four obligations;
- zero designated sorries;
- 48 generated trust declarations; and
- the exact recorded target.

This environment hides `/proc/<current-pid>/exe`, which Lean 4.22 uses to find
its installation. The initial preflight consequently failed before running
Lean. I compiled and inspected a narrow compatibility shim that redirects only
that current-process `readlink` to `/proc/self/exe`. With it, the unchanged
pinned binaries report Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and the preflight succeeds. The
failed attempts and shim hashes remain in evidence.

The domain-rule/obligation mapping is a strict ordered bijection:

1. associativity becomes the universally quantified append-associativity
   equality;
2. right identity becomes the universally quantified empty-suffix equality;
3. left cancellation becomes an `↔` between prefixed equality and suffix
   equality; and
4. the self-plus-suffix rule becomes an `↔` between the fixed-point equality
   and an empty suffix.

The `↔` obligations are not weakenings. A K simplification of an equality
predicate must preserve its truth value, and the reverse directions follow
from congruence/right identity. Each conjunct contains the bound function,
quantifies its complete source variables, has the recorded source span and
hash, and is nontrivial. None is `True`, `False`, empty, duplicated, irrelevant,
or vacuous.

Mathematically, supplied semantics defines finite `ValSeq` by empty/cons and
defines concatenation by recursion on the first sequence:

```text
valSeqConcat(.ValSeq, T) = T
valSeqConcat(vCons(V, S), T) = vCons(V, valSeqConcat(S, T))
```

Induction on the first sequence proves associativity and right identity.
Induction on the common prefix plus constructor injectivity proves
cancellation. Right identity and cancellation prove that
`P = valSeqConcat(P, A)` exactly when `A` is empty. Thus all four obligations
are true of the frozen operation and are material to the source proof.

The generated project contains exactly one target:
`Klean106F.Lemmas.targetStatement`. Its fixed identities are:

- definition:
  `0390e24478899b88cadacc90777465afa48d9ac8df1cdcc7903528e960565d1a`
- statement:
  `2bd5f406d518d7c48d4195088c4c56bbe905e81d03a219b8de6896a6161ff0d7`
- parameter binding:
  `5c0262f8a39f0d0f20822ba0afc9f2f3fe040fb2cb183895666e53d3d5f881de`

The declaration, statement, four source-rule IDs, KORE symbol, binding hash,
and definition hash match the obligation map, generator manifest, preflight
result, and `audit-input.json`.

Evidence:
[successful required preflight](/audit-output/evidence/04l_check_generation_success.log),
[generated target and candidate layout](/audit-output/evidence/05b_target_and_candidate_layout.log).

## Stage 5 proof, target identity, and trust

I created
`/tmp/audit-work/humaneval-106-f-proof-audit`, copied only the candidate source
and project metadata into it, and copied the immutable generated project into
`Base`. Candidate build caches were not reused. In that fresh project:

```text
lake clean  -> exit 0
lake build  -> exit 0, "Build completed successfully."
```

The fresh `Base` tree still has the exact generated-project hash. The candidate
does not define or shadow `targetStatement`, and its theorem type is exactly:

```text
Proof.final :
  Klean106F.Lemmas.targetStatement
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
```

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`. It introduces exactly the required target-parameter definition.

The parameter's bound KORE symbol is the MPY-LIST `valSeqConcat` production.
The candidate definition has exactly the two constructor equations shown
above: empty returns the suffix, and cons preserves the head while recursively
concatenating the tail. This matches the supplied semantics and the
`SortValSeq` empty/cons constructors exactly. It is neither constant,
identity/projection, hard-coded, nor vacuous.

The adversarial Lean file independently checked both universal defining
equations and concrete empty/singleton/doubleton results. It also machine
checked that the fixed target rejects:

- constant-empty concatenation;
- right projection;
- left projection/identity; and
- a recursive mutation that drops every left-hand head.

This is finite sensitivity evidence in addition to the direct definition
comparison; the operational bridge passes because the candidate is
definitionally the frozen recursive operation.

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' does not depend on any axioms
```

The dependency set is empty. It therefore contains neither `sorryAx` nor any
unrecorded trust escape. The generated `trust-inventory.json` allowlist has 48
entries, but none is exercised by `Proof.final`; its proof-hole counts are both
zero. The trusted Stage 5 mechanical checker independently returned `PASS`,
the same fixed target, `used_axioms: []`, and successful clean/build/axiom
diagnostics.

Evidence:
[fresh project copy](/audit-output/evidence/07_fresh_proof_project.log),
[complete clean build](/audit-output/evidence/08_clean_build.log),
[#print axioms](/audit-output/evidence/09_print_axioms.log),
[operational adversarial checks](/audit-output/evidence/10b_operational_bridge_adversarial_final.log),
[candidate and trust scan](/audit-output/evidence/11b_proof_integrity_and_trust_success.log),
[proof identity](/audit-output/evidence/12_proof_identity.log),
[trusted Stage 5 mechanical gate](/audit-output/evidence/13_trusted_stage5_mechanical_check.log).
The exact primary commands are indexed in
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
