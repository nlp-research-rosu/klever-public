# Independent Stage 3–4 audit: `61-correct-bracketing`

## Result

The audit mode is `CLASSIFICATION_ONLY`, matching both `AUDIT_MODE` and the
signed resolution in `/audit-input.json`. The Stage 3 classification is
complete and mathematically correct: the local verification-module closure
contains five rules, all five are genuine definitions, and the true
`DOMAIN_LEMMA` set is empty. The selected Stage 4 result
`KLEAN_NO_OBLIGATIONS` is therefore legitimate. It has no generated target,
and there is no Stage 5 candidate.

I treated the mounted workspaces, manifests, comments, logs, and prior review
as untrusted evidence. Hashes, rule identities, classifications, obligation
mapping, and target status were reconstructed independently using the trusted
code in `/reference/tools`.

## 1. Input and producer provenance

The signed audit-input digest recomputes to
`c15d7c58e11ef5836a9bc9e5f9df97444aa49734d07ab27d5f65ecddad84a414`.
The audit-input envelope, condition `bare`, problem ID, semantics mode
`GENERATED_SEMANTICS`, and `CLASSIFICATION_ONLY` mode are internally
consistent.

All mounted-tree and source hashes recompute exactly:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `d129cacc023263c10008eae34ae4ad3bf4b8e3c08c5d54b1ed927562559ffadf` |
| Stage 1 export tree | `182975adc6dcee9e395b19c30534d93291567e13e8a3b69c4acdb8fff0092f8e` |
| Stage 3 manifest | `6e83e1a5f2c175b07b2b50940548c9cc190e9e33dbc629b1e3c7813c4552e252` |
| Selected Stage 2 tree | `7a94017c0e9751b72d8a4d67e5a68e55a2fc68c48ad325684bc4c09d2b46aca4` |
| Selected Stage 4 tree | `85056547c273074d4187adca8dfd68b6b0c6fa7ae904a91093e1c9eb8a102bc5` |
| Generated Lean tree | `088885dbf15ded3cdcd28afcdd928ef986059f3e67a22d7c36a60614325596d7` |
| Producer-source bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

Every individual Stage 1 source hash also matches the audit input, including
`verification.k` at
`114aa53602dba52635d1065d51299e14b6b3206481865b7f39cc71fb0bc9cd4b`.
The selection hashes match their mounted Stage 2 and Stage 4 trees.

### Mandatory producer-source gate

The immutable generator image identity is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
It agrees in all three required places:

- `generator-manifest.json` provenance;
- `/reference/generation-tools/source-manifest.json`; and
- the image-key basename of the producer-source path signed in
  `/audit-input.json`.

The bundle contains exactly `klean_export.py`, `klean.py`, and
`source-manifest.json`, all regular files. The producer hashes are:

| Producer | Generator manifest | Source manifest | Recomputed |
|---|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same | same |

Thus the infrastructure producer-source prerequisite passes.

The complete hash record is in
[01_provenance_check.log](/audit-output/evidence/01_provenance_check.log);
the exact executable check is
[01_provenance_check.py](/audit-output/evidence/01_provenance_check.py).

## 2. Rule-inventory reconstruction

The trusted rule inventory selects `MPY-VERIFICATION`, as fixed by the final
`kompile verification.k --main-module MPY-VERIFICATION` command in
`prove.sh`. Its local closure within `verification.k` is exactly
`["MPY-VERIFICATION"]`. `MPY-SEMANTIC` and `K-EQUAL` are imports defined
outside this file, so they do not add local `verification.k` rules.

The reconstructed inventory is:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Attributes | Independent class |
|---:|---:|---|---|---|
| 1 | 10–23 | `ff38bf4352a9d5177710fc8cdb52e149480f3430cbb3889ae520f039fdd1caaf` / `rule-ff38bf4352a9d5177710fc8cdb52e149480f3430cbb3889ae520f039fdd1caaf` | none | `DEFINITION` |
| 2 | 32–32 | `52c678867274bfbe50cfd8894cb300d08fb5f3a018c416a200e725d66ad1ffb7` / `rule-52c678867274bfbe50cfd8894cb300d08fb5f3a018c416a200e725d66ad1ffb7` | `simplification` | `DEFINITION` |
| 3 | 33–36 | `0b80080b9a7dd4f80716f34190b5a512ffa576526b020733d3a661e68720cea9` / `rule-0b80080b9a7dd4f80716f34190b5a512ffa576526b020733d3a661e68720cea9` | `simplification` | `DEFINITION` |
| 4 | 37–39 | `dab3458a72db386dbad39915bdb52a22d7ee1cccd37c33aa1b8b984a02af13f4` / `rule-dab3458a72db386dbad39915bdb52a22d7ee1cccd37c33aa1b8b984a02af13f4` | `simplification` | `DEFINITION` |
| 5 | 40–44 | `2877c405b261ca01cd0ba4ed8be5aa27101f1fbd6c09d33fb7d78416ef4c6968` / `rule-2877c405b261ca01cd0ba4ed8be5aa27101f1fbd6c09d33fb7d78416ef4c6968` | `simplification` | `DEFINITION` |

The canonical whole-inventory hash is
`6aeee3fa40855aacaad8dc3198ea22558fcbad8dad852967b36973aa988321fb`.
It exactly matches Stage 3. The Stage 3 rule-ID list equals the canonical list
position-for-position. There are no omitted, extra, duplicated, reordered, or
hash-changed rules, and the trusted Stage 3 boundary validator accepts the
manifest's exact schema and key sets.

The full reconstructed rule text and all comparisons are in
[02_inventory_check.log](/audit-output/evidence/02_inventory_check.log), with
the executable check in
[02_inventory_check.py](/audit-output/evidence/02_inventory_check.py).

## 3. Independent classification judgment

### `solutionProgram`

The rule at lines 10–23 expands a zero-argument function symbol into the full
constructor AST for `correct_bracketing`. Inspection against `solution.py`,
`solution.mpy`, and the operational constructors in `semantic.k` confirms the
same parameter, initial `count = 0`, string loop, opening increment,
zero-depth early false return, positive-depth decrement, and final
`count == 0` return. It names an immutable proof term; it does not assert a
mathematical law or shortcut program execution. `DEFINITION` is the required
class.

### The four `bracketSpec` rules

These are the defining equations of a result-bearing execution summary:

1. empty suffix returns whether the current depth is zero;
2. a leading `(` consumes one character and increments depth;
3. a non-`(` at depth zero rejects;
4. a non-`(` at positive depth consumes one character and decrements depth.

The guards are disjoint over nonnegative depths, the recursive cases strictly
shorten the string, and together they cover every use reachable from the loop
claim's `N >=Int 0` precondition. The source program makes exactly the same
branch distinction and state transition. `SPEC.loop` and `SPEC.main` use this
summary directly in their postconditions, so the equations are relevant to
both the frozen program and property. They are recurrences, not independent
domain facts; all four are `DEFINITION`.

The declaration marks `bracketSpec` as total although its equations do not
cover a negative depth followed by a non-opening character. That case is
outside every classified use: the loop claim begins nonnegative, the
zero-depth close rule returns rather than recursing, and the other transitions
preserve nonnegativity. This unused declaration-domain gap does not turn any
equation into a `DOMAIN_LEMMA` and does not create a Stage 4 obligation.

As finite adversarial support, I compared the defining recurrence with an
independent operational loop model for 88,569 combinations of depths 0–8 and
strings over `(`, `)`, and a non-opening character through length 8. There
were zero mismatches. Separate counterfactual mutations of the base, opening,
zero-close, and positive-close clauses were each distinguished by a concrete
witness. This testing supports, but does not replace, the universal
source-level branch and descent argument above. See
[05_semantic_sensitivity.log](/audit-output/evidence/05_semantic_sensitivity.log)
and
[05_semantic_sensitivity.py](/audit-output/evidence/05_semantic_sensitivity.py).

### Classification totals

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Every `simplification` rule is therefore a `DEFINITION`. No rule purports to
be a separately proved derived lemma, so the two-phase exact-rule proof
criterion is not invoked. Most importantly, no domain law has been hidden
under another category.

## 4. Deterministic Stage 4 generation

The Stage 4 input manifest's five definitions are byte-for-byte the validated
classified entries reconstructed above. Its operational and proved-derived
lists are empty. Independent classification also makes the true domain set
empty, and the input manifest, obligation map, and trusted exporter all agree
on that exact set:

```text
source_rules = []
obligations = []
trust_parameters = []
```

Consequently the source-rule/obligation bijection is the genuine empty
bijection—not an omission. There are zero extra obligations, duplicates,
weakened or irrelevant conjuncts, vacuous conjuncts, or unmapped rule IDs.

The obligation-map hash recomputes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
The input, generator, export-result, preflight, toolchain, inventory,
discovery, verification, generated-tree, obligation-map, and trust-inventory
hash bindings all recompute and agree. The generator toolchain object exactly
equals `/reference/klean-toolchain.lock.json`.

The trusted expected-target calculation returns `None`; independent target
extraction from the generated tree also returns `None`. This agrees with the
generator manifest, recorded preflight, and audit input. The generated root
module only imports `Rewrite` and the empty `Lemmas` namespace; it contains no
target declaration. Thus there is no changed, weakened, duplicated, or
vacuous target.

The generated Lean trust declarations number 44 and exactly equal the
`trust-inventory.json` allowlist. The generated tree has zero designated or
other sorries. These declarations do not prove a target because no target was
generated.

All independent Stage 4 checks and hashes are in
[03_stage4_independent_check.log](/audit-output/evidence/03_stage4_independent_check.log),
with executable source in
[03_stage4_independent_check.py](/audit-output/evidence/03_stage4_independent_check.py).

## 5. Required preflight rerun

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these three inputs:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
```

The audit sandbox exposes `/proc/self/exe` but not Lean 4.22's requested
`/proc/<numeric-pid>/exe`. I used the audit-local
[proc_self_compat.c](/audit-output/evidence/proc_self_compat.c) shim, which
rewrites only that one `readlink` path, and put the pinned v4.22.0 toolchain
binary directory first in the subprocess `PATH`. It does not alter the
generated project, Lean terms, compiler, kernel, or libraries. Its build,
hash, and exact pinned Lean/Lake versions are recorded in
[04_toolchain_compat.log](/audit-output/evidence/04_toolchain_compat.log).

The trusted preflight made its own fresh temporary copy and returned:

```text
lake clean: exit 0, output SHA-256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

lake build: exit 0, output SHA-256
cde5df963058fa72971b93e86c7b8bd53eaa6685c20290b06cbbe2a17cde89bc

status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
```

The complete build output is saved in
[04_preflight_rerun.log](/audit-output/evidence/04_preflight_rerun.log), and
the exact invocation wrapper is
[04_preflight_rerun.py](/audit-output/evidence/04_preflight_rerun.py). The
entire returned evidence object exactly equals both the recorded
`preflight.json` and the preflight object signed into `/audit-input.json`.

## 6. Stage 5 applicability

Stage 5 is not applicable in `CLASSIFICATION_ONLY` mode. `/candidate` does not
exist; the signed Lean workspace and invocation paths and hashes are null; and
`stage5_result` is null. Because the true domain set is empty and Stage 4
generated no target, this absence is required. There is no `Proof.final`,
candidate definition, axiom printout, or operational bridge to audit.

VERDICT: PASS
LEGITIMACY: LEGIT
