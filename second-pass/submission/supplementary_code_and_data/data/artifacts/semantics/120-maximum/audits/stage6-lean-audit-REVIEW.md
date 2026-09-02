# Independent Audit: HumanEval `120-maximum`

This audit covers condition `semantics` in `SUPPLIED_SEMANTICS` mode. The launcher selected `CLASSIFICATION_AND_PROOF`, so I audited the Stage 3 classifications, deterministic Stage 4 output, and the Stage 5 Lean proof. Candidate and provenance content was treated solely as untrusted evidence.

## Result

The protected Stage 3 file accounts for the complete local verification-module rule inventory in source order and classifies both rules correctly. The only true domain lemma is relevant to the program and postcondition, and Stage 4 generates exactly one corresponding obligation without weakening or duplication. The authenticated producer sources reproduce a single fixed target. In a fresh workspace, the Stage 5 candidate builds cleanly, proves exactly that target, uses only Lean's core `propext` axiom, and supplies operational definitions matching the frozen K behavior on the integer-list domain of the source problem.

## Audit mode and immutable inputs

`AUDIT_MODE` and `/audit-input.json` both select `CLASSIFICATION_AND_PROOF`. The audit-input envelope hash recomputed to:

`6889c5fe91cb47483e24128de91e8a5f93ff23ed266e3c818528b7796566bd5d`

All recorded hashes for the mounted Stage 1, Stage 2, Stage 3, Stage 4, producer, and Stage 5 trees or files matched their mounted content. In particular:

- Stage 1 pipeline tree: `24fc88ce2d1cdac9f9de36ec9ab111a24f90986fc8f7185b48a5ecb28ef7efca`
- Stage 1 export tree: `a15636d712029939901892bc3e495fd0a79dfde75ccfb550cf6b3447e2264b53`
- Stage 2 pipeline tree: `b59de17fe4254ec44290066648fb9ba87f2e88ec0d93026341eaaed1052f2162`
- Stage 3 discovery file: `4c7c3ee30d03d858619bb5c476033904a1619b7e3a403f8fb50e4f808431b263`
- Stage 4 pipeline tree: `2b722d17b1332635fa5b8df3bbd2b75e37227cf2f7027f4b43cd7b15a755bf2`
- Stage 4 generated export tree: `2774bd9d4a4261e63add40eca6e6f9dcc7e06bd18feeb66299855ff44ad6da4e`
- Stage 5 candidate pipeline tree: `a2478734a2bc8c20359bec16fe4a2f7318f6963fb70dd7b1150503553872e935`

The launcher records a hash for a non-mounted Lean-invocation artifact. Because that artifact is not among the read-only inputs provided to this audit, it could not be rehashed and was not used as proof evidence. The mounted candidate itself was hashed and rebuilt independently.

The complete hash reconciliations are in [21-stage1-source-hashes.log](evidence/21-stage1-source-hashes.log), [22-mounted-artifact-hash-reconciliation.log](evidence/22-mounted-artifact-hash-reconciliation.log), and [38-stage4-recorded-hash-reconciliation.log](evidence/38-stage4-recorded-hash-reconciliation.log).

## Producer-source authentication

Before judging generated content, I hashed the two producer files:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes match `generator-manifest.json` and the source manifest. The producer bundle tree hash is `55e6319d291d467020c36da688ffcb40e56d4303774227fbd070d3d6b4a4cf19`, matching `/audit-input.json`. The immutable generator image ID is consistently:

`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`

It agrees across the generator manifest, source manifest, and launcher-recorded producer path. Producer source is therefore present and authenticated; no infrastructure `AUDIT_ERROR` applies. Raw comparison evidence is in [03-producer-authentication.log](evidence/03-producer-authentication.log).

## Stage 3 inventory reconstruction

I ran the trusted local rule-inventory implementation against the frozen Stage 1 `verification.k` and independently checked its source extraction. The local verification-module closure contains only `MAXIMUM-VERIFICATION` and exactly two rules. The reconstructed inventory hash is:

`2ba3d5ba59fa3fb610b17cf7244ed413c75697e95761761650e2fbf35d7b4e9f`

The frozen verification source hash is:

`21f4e09e6ef0e828e13192f82307453115d994c054511552b418549b4d68a60a`

| Order | Source span | Reconstructed identity | Attributes | Independent classification |
|---:|---:|---|---|---|
| 1 | lines 9–17 | `rule-8e525ad3c9ded20f8b26e2c2398d95661f926cd77cc2c322f7c541606c0988ad` | none | `DEFINITION` |
| 2 | line 22 | `rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907` | `simplification` | `DOMAIN_LEMMA` |

For both rules, the normalized-source hash is the digest embedded in its `source_rule_id`. The protected classification has the same two identities, spans, normalized hashes, order, and whole-inventory hash. There are no missing, duplicated, extra, reordered, changed, or unclassified rules.

The first rule expands the named `maximumBody` syntax term to the exact source-program body. It is a genuine macro/summary definition, not an operational rule or mathematical domain fact.

The second rule states:

`vsLen(sortVS(VS)) => vsLen(VS)`

This does not define `sortVS` or `vsLen`; those functions are already operationally defined in the imported semantics. It states the mathematical preservation fact that sorting does not change sequence length. Stage 1 does not first prove this exact rule in a module omitting it and then import it for a later proof, so it cannot be a `PROVED_DERIVED_LEMMA`. Nor is it an ordinary execution/observation rule. Its correct category is `DOMAIN_LEMMA`.

The lemma is directly relevant. The frozen solution returns `sorted(arr)[-k:]` for positive `k`; the K semantics implements `sorted` through `sortVS`, slicing computes indices using `vsLen`, and the postcondition constructs the expected suffix using the original sequence length. Relating the sorted and original lengths is therefore material to the proof. The only `simplification` rule is this valid domain lemma, satisfying the classification restriction.

The reconstructed inventory and bijection are recorded in [04-rule-inventory-and-bijection.log](evidence/04-rule-inventory-and-bijection.log). Source proof order and semantic relevance are documented in [33-stage1-proof-order-and-rule-use.log](evidence/33-stage1-proof-order-and-rule-use.log), [35-domain-lemma-relevance-and-operational-semantics.log](evidence/35-domain-lemma-relevance-and-operational-semantics.log), and [36-source-contract.log](evidence/36-source-contract.log).

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1, Stage 3, and Stage 4 paths. The first run exposed a container `/proc` PID-namespace mismatch: Lean's application-path lookup could not resolve its own executable because the child PID was not visible in the host-mounted `/proc`. This was an execution-environment issue, not a source or proof result.

I used a narrowly scoped read-only compatibility shim that changes only `readlink` results for `/proc/self/exe`, `/proc/thread-self/exe`, and `/proc/<digits>/exe`, returning the already pinned Lean executable. The shim source and binary hashes, Lean version, and toolchain identity are captured in [13-proc-shim-toolchain-validation.log](evidence/13-proc-shim-toolchain-validation.log). It did not alter any candidate or provenance input.

With that environment repair, the required trusted preflight returned `PASS`, with one obligation, zero designated sorries, 47 recorded trust declarations, successful `lake clean`, and successful `lake build`. The full result is in [14-rerun-check-generation-with-proc-shim.log](evidence/14-rerun-check-generation-with-proc-shim.log).

My independent obligation check found an exact one-to-one mapping:

- Domain set: exactly source rule `rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907`
- Generated obligation: `∀ VS, vsLen (sortVS VS) = vsLen VS`
- Conjunct hash: `dfeaedb665c23249055633885767fb11b65e28b63f313f7438350405c3896a4d`

The obligation preserves both quantified input and both sides of the frozen K equation. It has no vacuous `True`/`False` conjunct, no irrelevant condition, and no weakening. There are no omissions or duplicates. Because the independently classified domain set is nonempty, `KLEAN_NO_OBLIGATIONS` would have been invalid; the selected Stage 4 correctly generated one obligation.

The fixed generated target is:

- Declaration: `Klean120Maximum.Lemmas.targetStatement`
- File: `Klean120Maximum/Lemmas.lean`
- Definition SHA-256: `65d23f54ec53cde158f5d27bc7f019ec18ea9202bbf94b08d47b4c49fb88c108`
- Instantiated statement: `Klean120Maximum.Lemmas.targetStatement sortVS «vsLen(_)_MPY-CORE_Int_ValSeq»`
- Statement SHA-256: `fed84c3fc843add569ca14825b7e2cb9d6d536bcba84aa0384c8c0d20954025b`

These values agree exactly among the authenticated producer output, generator manifest, obligation map, audit input, trusted preflight, and mounted generated source. The binding hashes for the two parameters also match their recorded KORE symbols and source-rule provenance. Evidence is in [24-fixed-target-identity-success.log](evidence/24-fixed-target-identity-success.log) and [25-obligation-bijection-and-mathematical-translation.log](evidence/25-obligation-bijection-and-mathematical-translation.log).

## Stage 5 fresh build and proof identity

I created a fresh workspace at `/tmp/audit-work/lean-audit.zDcMtK`, copied the generated project into it as `Base`, and copied the candidate proof project around that fixed base. The copied candidate and generated-base hashes matched their source trees before building. See [18-fresh-proof-copy-corrected.log](evidence/18-fresh-proof-copy-corrected.log).

Both required commands succeeded:

- `lake clean`: exit 0, [19-proof-lake-clean.log](evidence/19-proof-lake-clean.log)
- `lake build`: exit 0 with `Build completed successfully`, [20-proof-lake-build.log](evidence/20-proof-lake-build.log)

The generated `Base` tree and target remained byte-identical after the build. The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It does not redeclare, modify, or shadow `targetStatement`; it only refers to the generated declaration as the type of `Proof.final`. The scan is in [26-candidate-forbidden-scan-and-target-shadow-check.log](evidence/26-candidate-forbidden-scan-and-target-shadow-check.log).

Lean reports:

`Proof.final : Klean120Maximum.Lemmas.targetStatement Proof.sortVS Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»`

Thus `Proof.final` proves the exact fixed generated statement instantiated with the candidate's two bound implementations. It is not a copied, weakened, renamed, or vacuous theorem. The declarations and proof type are printed in [29-print-proof-identity.log](evidence/29-print-proof-identity.log).

Running Lean with `#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext]`

There is no `sorryAx`. `propext` is a Lean core logical axiom accepted by the trusted final gate, not a new candidate axiom or an unrecorded generated executable declaration. None of the 47 executable declarations recorded in `trust-inventory.json` occurs in the dependency list, and the inventory records zero designated or other sorries. The exact output and reconciliation are in [27-print-axioms-Proof-final.log](evidence/27-print-axioms-Proof-final.log) and [28-trust-inventory-reconciliation.log](evidence/28-trust-inventory-reconciliation.log).

As an additional mechanical cross-check, the trusted Stage 5 final gate returned `PASS`, confirmed the exact target, repeated both clean build steps successfully, and reported only `propext`. See [34-trusted-stage5-mechanical-gate.log](evidence/34-trusted-stage5-mechanical-gate.log).

## Operational bridge for target parameters

The theorem alone is underdetermined: an identity sorter paired with the real length, or a constant sorter paired with a constant-zero length, can satisfy length preservation. I therefore evaluated the implementations independently rather than treating theorem provability as evidence of operational fidelity.

### `vsLen`

The candidate definition is structurally recursive:

- empty sequence maps to `0`;
- a cons maps to `1 + vsLen(tail)`.

This is exactly the frozen `vsLen` operational recurrence on `ValSeq`, and it is neither constant nor input-ignoring.

### `sortVS`

The source contract restricts arrays to integers. On every representable integer sequence, the candidate:

- maps empty to empty;
- recursively sorts the tail;
- inserts the integer head before the first element greater than or equal to it using the decided integer relation `a ≤ b`;
- otherwise recurses past the current element.

This matches the frozen K insertion-sort equations: the `X ≤ Y` branch inserts before `Y`, while the complementary integer branch corresponds to K's `X > Y` rule. It preserves duplicates and negative values and is not identity, constant, hard-coded, or input-ignoring.

The generated Lean `SortVal` does not expose a string constructor corresponding to K's separate string-comparison branches. Its remaining non-integer cases are outside the HumanEval source domain and lack a matching concrete K `sortVS` equation. The candidate's stable total fallback for those cases is therefore an out-of-domain extension, not a contradiction of the frozen operational meaning used by this problem.

Adversarial evaluations covered descending values, negative values, duplicates, mixed order, and already sorted inputs. Representative results include:

- `[-3, -4, 5]` → `[-4, -3, 5]`
- `[4, -4, 4]` → `[-4, 4, 4]`
- `[3, 2, 1, 0, -1]` → `[-1, 0, 1, 2, 3]`
- `[-7, -7, 0, 2, 2]` remains `[-7, -7, 0, 2, 2]`

The same test file demonstrates the underdetermination counterexamples noted above, making clear that the bridge conclusion rests on definition inspection and behavior, not merely the generated equation. An identity-sort mutation fails the concrete `[2,1] → [1,2]` counterfactual. Results are in [30-operational-bridge-tests.log](evidence/30-operational-bridge-tests.log) and [31-counterfactual-identity-failure.log](evidence/31-counterfactual-identity-failure.log).

## Conclusion

The Stage 3 inventory is complete and correctly classified. The one true domain lemma is relevant and is translated bijectively into the sole Stage 4 obligation. Producer sources, image identity, manifests, hashes, parameter bindings, and fixed target all agree. The Stage 5 candidate preserves the target, rebuilds from clean state, contains no prohibited trust escapes, proves exactly the generated theorem, accounts for its sole core axiom, and implements the bound K operations faithfully on the frozen program's integer-list domain.

The raw-command index is [evidence/COMMANDS.md](evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
