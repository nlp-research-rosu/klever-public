# Independent Stage 3–5 audit: `75-is-multiply-prime`

## Scope and result

The launcher, `/audit-input.json`, and the environment all identify:

- problem: `75-is-multiply-prime`;
- condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`; and
- audit mode: `CLASSIFICATION_ONLY`.

I treated the mounted workspaces, manifests, comments, logs, and earlier review
as untrusted evidence. I did not use the selected Stage 2 verdict as a premise.
The decisive results below come from the frozen source, trusted inventory and
preflight code, independent hash reconstruction, and an independent check of
the source program's mathematics.

The selected `KLEAN_NO_OBLIGATIONS` status is correct. The local verification
module closure contains no rules, hence the true domain-lemma set is empty.
Stage 4 maps that empty set bijectively to zero obligations, generates no target,
and correctly has no Stage 5 candidate.

## Producer-source authentication

I authenticated the generation-time producers before making any substantive
Stage 4 judgment.

| Item | Recomputed SHA-256 | Recorded result |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Exact match in `generator-manifest.json` and `source-manifest.json` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Exact match in `generator-manifest.json` and `source-manifest.json` |
| producer bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Exact match in `/audit-input.json` |

The producer bundle contains exactly those two source files and
`source-manifest.json`. Its image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator provenance and source manifest. The basename of the immutable
producer path signed in `/audit-input.json` is the same digest. There is no
producer-source infrastructure error.

Raw evidence: `evidence/00_environment_and_producer_auth.txt`,
`evidence/01_manifest_contents.txt`, and
`evidence/14_recorded_hash_reconciliation.txt`.

## Inventory reconstruction and Stage 3 classification

The frozen `verification.k` has SHA-256
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.
It contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference`. The trusted lexical reconstruction selected main
module `VERIFICATION`; its local closure is exactly `["VERIFICATION"]`. `MPY`
is supplied by the required semantics file and is not a locally declared module
inside `verification.k`. The local closure therefore contains zero rule
sentences.

Consequently there are no source spans, normalized rule hashes, or
`source_rule_id` values to classify. The complete ordered rule document is
`[]`, whose independently recomputed canonical SHA-256 is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
The protected Stage 3 manifest contains the same hash and exactly the same empty
ordered rule list. The trust-boundary validator also returned:

- definitions: 0;
- operational rules: 0;
- proved derived lemmas: 0; and
- domain lemmas: 0.

This is a bijection, not an omission: there is no local rule that could be
duplicated, reordered, hidden under a changed hash, or assigned an unaccounted
classification. In particular, there is no local `simplification` rule and no
purported `PROVED_DERIVED_LEMMA` whose prior proof would need checking.

I also inspected the operational path used by the frozen claim. The supplied
semantics ordinarily loads and binds the function, evaluates the call and
argument, looks up `a`, evaluates integer literals and integer equality, applies
short-circuit `BoolOp("or", ...)`, returns the value, and restores the frame.
These are fixed execution/observation rules in `core.k`, `functions.k`,
`call.k`, `operators.k`, `int.k`, and `bool.k`; none is a proof-local extension
subject to Stage 3 classification. The frozen program is a finite disjunction
of equality tests, and the K postcondition is the identical disjunction. Thus
ordinary symbolic execution needs no mathematical domain lemma.

As an independent intent and adversarial check, I enumerated products of three
positive primes below 100 without importing or executing `solution.py`. The
result was exactly:

`[8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50, 52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99]`.

That list exactly matches both the source disjunction and the K postcondition.
Witnesses including negative inputs, `7`, `8`, `30`, `64`, `97`, `98`, and
`99` all behaved as expected. This extra check confirms that the absence of a
domain lemma is not concealing an unrelated or false finite list.

Raw evidence: `evidence/02_frozen_sources_and_stage3.txt`,
`evidence/03_inventory_reconstruction.txt`,
`evidence/16_relevant_operational_semantics.txt`, and
`evidence/18_frozen_program_math.txt`.

## Signed-input and manifest hash reconciliation

The signed resolution digest recomputed to
`4339e7e2843d0d1539ccbe9a2b6305ce340ffb59123db264025bf0976da215be`,
exactly the value in `/audit-input.json`. The mounted audit-input copies are
byte-identical. All resolution hashes recomputed exactly:

| Bound artifact | Recomputed SHA-256 |
|---|---|
| full Stage 1 workspace tree | `ba8fb8d5cc17025b344751f4b40ae21d3f5efa6c5a32483ee9ad8124115574e2` |
| deterministic Stage 1 export tree | `52a4e49e9cc13fc2822727642c8efec9d1a5b9be5130bc4bb6bddf3e6f75263f` |
| Stage 3 discovery manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| selected Stage 2 audit tree | `ed0c4c66776137389f45045b13e08ff468e0f9fd4dd7b2a02836cf5414695e07` |
| selected Stage 4 generation tree | `9011e5cf7aa5f765f0613d07f042c8a1ce3aa9ece809e00fa3022d19fb07d69a` |
| generated Lean project tree | `b1ee60840de6dc12e40ab7829400e41baac5c8e58dfb0c240dc77cd2f579e314` |

I recomputed the signed per-file Stage 1 source map as well: all 775 expected
paths were present, there were no extra paths, and every file hash matched.
The input manifest, generator provenance, export result, selected-artifact
records, trust-inventory hash, and pinned toolchain object all reconcile with
these recomputed values.

Raw evidence: `evidence/14_recorded_hash_reconciliation.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` using:

- frozen input `/reference/k-proof`;
- discovery manifest `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`;
- toolchain lock `/reference/klean-toolchain.lock.json`; and
- `PYTHONPATH=/reference`.

The audit runner exposes a procfs PID namespace in which Lean 4.22's
`/proc/<getpid()>/exe` lookup returns `ENOENT`. The unmodified default invocation
therefore failed before artifact-dependent compilation. I traced that exact
failure, then used the function's public `run_command` callback to invoke the
pinned Lake binary with a narrow compatibility library that only retries a
failed `/proc/*/exe` `readlink` as `/proc/self/exe`. The complete 24-line source,
its hashes, original failure, and restored Lean version are preserved. This did
not alter the generated project, manifests, proof logic, or compiler inputs.

The trusted preflight then completed all structural checks and ran, in a fresh
temporary copy, both:

```text
lake clean  -> exit 0
lake build  -> exit 0
```

The complete build produced the seven expected generated-module build lines and
`Build completed successfully.` Its output hash is
`148ccf06bdda5108cbe4c99fc2a91566248f8d99ce3a207c181efb3da841db88`,
which is also the generation-time recorded hash. `check_generation` returned
`KLEAN_NO_OBLIGATIONS`, obligation count 0, target `null`, no designated sorry,
and the expected generated tree and source hashes. Its policy check accounted
for 41 generated executable trust declarations and rejected proposition trust;
these declarations are not target parameters because there is no target.

Raw evidence: `evidence/04_check_generation.txt`,
`evidence/13_check_generation_completed.txt`,
`evidence/19_procfs_compatibility_evidence.txt`, and
`evidence/proc_exe_compat.c`.

## Obligation bijection and fixed target identity

The independently reconstructed domain source-rule list is empty. The Stage 4
input manifest records `source_rules: []`. The generated obligation map records:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

The obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
exactly the generator-manifest value. Both sides of the source-rule/obligation
mapping have the same order and cardinality zero, and there are no duplicated
IDs. No irrelevant, weakened, omitted, duplicated, or vacuous conjunct exists.

The deterministic expected target definition is `None`, and the trusted target
scanner observed `None`. The generator manifest, export result, preflight,
and signed audit input all record target `null`. The generated `Lemmas.lean`
namespace is empty, and there is no target-related theorem or definition.
Accordingly the fixed generated target has not changed: it is intentionally
absent for a genuine empty domain set.

Raw evidence: `evidence/15_obligation_target_and_candidate.txt` and
`evidence/17_exact_bijection_and_target.txt`.

## Stage 5 applicability

This is `CLASSIFICATION_ONLY`, not `CLASSIFICATION_AND_PROOF`. The signed input
has no Lean workspace or Stage 5 invocation, `/candidate` is absent, and Stage 4
has no generated target. That is the required configuration for
`KLEAN_NO_OBLIGATIONS`. Candidate isolation, `Proof.final`, `#print axioms`,
target-parameter implementation checks, and operational-bridge adversarial
mutations are therefore not applicable.

## Evidence index

`evidence/COMMANDS.md` records the reproducible commands. Numbered text files
contain raw combined command results, including unsuccessful environment
diagnostics rather than hiding them. The helper programs used for independent
hash, target, and mathematical checks are also preserved in `evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
