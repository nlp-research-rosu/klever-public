# Independent Stage 3–5 audit: `38-decode-cyclic`

## Result

The protected Stage 3 classification is complete and mathematically correct,
the selected Stage 4 generation is provenance-valid and preserves a bijection
between all true domain lemmas and the fixed Lean target, and the Stage 5
candidate cleanly proves that exact target with operationally faithful
definitions. I found no omitted rule or obligation, classification escape,
target change, proof hole, unrecorded project axiom, or operational-bridge
shortcut.

The launcher and `AUDIT_MODE` both select
`CLASSIFICATION_AND_PROOF`; the condition is `bare` and the semantics mode is
`GENERATED_SEMANTICS`.

## Immutable inputs and producer provenance

I treated all mounted candidate and historical review material as evidence
only. The signed audit-input envelope recomputes to
`8976e918cf6d6a7ccb51ada231bd67b301c75fddb42c830ac73a6e86aeeee472`.
The mounted trees reproduce the launcher records:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `f600725fab73470246ba886f9bf3af31bb1d72edca63918399cd60d871f1bc73` |
| Stage 1 deterministic export tree | `2db69dd3a57605c6a212cedbe401470040ad29a65b7c00f27b9d286bb5ff3dff` |
| selected Stage 2 audit tree | `a257592abdcfea9cecf9efce51a1e29a1d4b0b62342fc318f65a57761a25e6b2` |
| Stage 3 manifest file | `b5ecfd0e5ad951679b77e881ccf86470d4328205da3f2ef238dd9e8061ae5fb8` |
| selected Stage 4 generation tree | `b2d2ee67e50006a244f35eb09575bb7d232056e23540da53b9692b35bbb93ae3` |
| generated Lean project export tree | `9a729bf9e6da030fc7c4fe7790160f24365d0a04642cc6ab149786aecce5bd8d` |
| producer-source bundle tree | `5e674104ca65fed1c0a0004d3011762dcd335fa0f6620bac310ec19f1f143cbc` |
| Stage 5 candidate tree | `a929657b8239498ed485be3c9e954f9a039afb0ed52126cda7d71f68f6c0038e` |

Every mounted Stage 1 per-file source hash also matches. The historical
Stage 5 invocation directory is intentionally not mounted, so its historical
tree hash cannot be independently re-hashed and was not used as proof
evidence; the candidate workspace itself is mounted and matches.

Before judging generation I directly hashed the two immutable producer files:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `b8bcddc01151a647e69b336435af38cd8dd94239a3ac96da0d45c2aa60bbb6f0` |

Those hashes agree exactly with `source-manifest.json` and
`generator-manifest.json`. Both manifests also agree on generator image
`sha256:686134aa922debe485b0e3bb0a6476ca48e04c580ceb66d0f01003c97cdcab65`;
the same immutable image identity is encoded in the producer-source path
recorded by `/audit-input.json`. The source bundle contains exactly those two
producers plus its source manifest. The generator toolchain object equals
`/reference/klean-toolchain.lock.json`.

Full commands and results are in
`evidence/00-provenance-and-hashes.log`; the independent checker is
`evidence/verify_hashes.py`.

## Canonical inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen Stage 1 workspace reconstructed local verification module
`VERIFICATION`. Its local closure inside `verification.k` contains only that
module; `MPY` is imported from the separate `semantic.k` and was examined for
operational relevance but is outside this lexical inventory.

The frozen file hash is
`330223b03ce586a4acf9294a57c3244ba7421059c3d508794b9c40d8a5aaca4f`.
The complete ordered inventory is:

| Span | `source_rule_id` / normalized source SHA-256 | Attributes |
|---|---|---|
| 9–11 | `rule-ef7d5d777b33ed834768f6d5eae1abcfc5bb3ea8e0391ad21da31281612828ec` | `simplification` |
| 13 | `rule-aa08fc7ab00f7ed5932bfabaec47fbf527e50b83d0b239787af7e592a9c05a9d` | `simplification` |
| 14 | `rule-6a69a83530cb8d2469f0452d5b6878c9d18dc4dbc80234500bed171c1b093548` | `simplification` |

The whole ordered inventory hash is
`d2db99b7bfbb6f10173dc29736d6dd1020fae34b484b232cc0ed4a77b679becb`.
The protected Stage 3 manifest contains exactly these three identities in this
order, once each, with no extra key or rule. The trusted boundary validator
accepts the exact source spans, normalized hashes, IDs, ordering, and inventory
hash. There are no omissions, duplicates, extras, reordered identities, or
unclassified entries. Raw reconstruction is in `evidence/01-inventory.log`
and the reproducible driver is `evidence/reconstruct_inventory.py`.

## Independent Stage 3 classification

All three rules are `DOMAIN_LEMMA`:

1. The map-update cancellation rule says that updating the same finite map at
   the same key with `V` and `V'` yields equal maps exactly when `V = V'`.
   This is a true map-domain fact. It is not a named definition and does not
   execute or observe a `<k>` configuration. It is relevant to the exact map
   update used by assignment in `semantic.k` lines 73–75 and to symbolic
   matching of the loop environment.
2. `0 <=Int lengthString(S) => true` is the nonnegativity theorem for the K
   string-length hook. It does not define length and is not an operational
   transition. It is directly relevant to the initial loop invariant
   `0 <= I <= length(S)` and the tail-slice guards.
3. `substrString(S, 0, lengthString(S)) => S` is the full half-open substring
   identity. It does not define substring and is not an operational
   transition. It is relevant to the source return `result + s[i:]`, including
   the no-loop `i = 0` case.

All are present during the only Stage 1 `kprove` command. `prove.sh` contains
no earlier proof of any exact rule against a module that omits it, so none
qualifies as `PROVED_DERIVED_LEMMA`. None defines a summary, recurrence, macro,
or named proof term, so none is a `DEFINITION`. None is an ordinary execution
or observation rule, so none is an `OPERATIONAL_RULE`. Their
`simplification` attributes are therefore consistent only with the selected
`DOMAIN_LEMMA` classification.

As an additional relevance diagnostic, the unmodified proof returned `#Top`.
Removing the length rule made the end-to-end claim stick on
`0 <=Int lengthString(S)`. Removing the local map or substring rule still
returned `#Top` because the imported K builtin/symbolic theory also simplifies
those facts. That redundancy does not make the facts unrelated to the
operations executed by the source. Exact outputs are in
`evidence/02-classification-relevance.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock. It returned
`PASS`, rebuilt the generated project, and reproduced:

- Stage 1 export hash
  `2db69dd3a57605c6a212cedbe401470040ad29a65b7c00f27b9d286bb5ff3dff`;
- Stage 3 hash
  `b5ecfd0e5ad951679b77e881ccf86470d4328205da3f2ef238dd9e8061ae5fb8`;
- generated tree hash
  `9a729bf9e6da030fc7c4fe7790160f24365d0a04642cc6ab149786aecce5bd8d`;
- three obligations, 44 generated trust declarations, and zero designated
  sorries.

This sandbox exposes `/proc/self/exe` but not Lean 4.22's
`/proc/<getpid()>/exe` lookup. The first preflight attempt therefore failed at
Lake configuration detection. I used the narrow interposition recorded in
`evidence/proc-self-readlink.c` solely to redirect that lookup; it does not
change Lean, the generated source, or any proof term. The rerun used the
pinned Lean commit and reproduced the generation-time build output hash
exactly. The complete result and environment diagnosis are in
`evidence/03-preflight.log`.

Independent of preflight, the source-rule, obligation, and trust-parameter
lists are exact ordered bijections. The generated conjuncts are:

1. map update at one key is injective in the replacement value;
2. K string length is nonnegative; and
3. substring over `[0, length)` is the original string.

Their conjunct hashes are respectively
`605288df3595458e146108030d6f873ddc581fd08747d3d33cb3bbdc28ab80e3`,
`e5e0b5d1e73d78a312a269ffdb0bd3de1ec94b20bdcf21e52a8c95cb55edb701`,
and
`b4f0e8779fd822284e322a0807dc5d7726dde4fecb42b8be23884a2f16af4a02`.
Each is nonempty and universally quantified over inhabited generated sorts.
There is no implication with a false antecedent, unconstrained result,
duplicate conjunct, omitted direction, irrelevant fact, or changed target.
`evidence/check_obligation_bijection.py` and
`evidence/04-obligation-bijection.log` record the mechanical comparison.

The fixed target remains:

```text
Klean38DecodeCyclic.Lemmas.targetStatement
  «_<=Int_» «Map:update»
  «lengthString(_)_STRING-COMMON_Int_String»
  «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
```

Its declaration is
`Klean38DecodeCyclic.Lemmas.targetStatement`, its definition hash is
`7bba40a4a2892d50612192343a8e7d8226c3ab93278ca4a4d062e68a5dc1b835`,
and its applied-statement hash is
`32a2ae8e9350f6d65d01c27776f3613cdd40397f360a1a8e886b85a2cf20fd80`.
The computed target, generator manifest, recorded Stage 4 preflight, and
`/audit-input.json` agree exactly.

## Fresh Stage 5 proof and target identity

I copied the candidate to `/tmp/audit-work/stage5-fresh`, copied the immutable
generated project into it as `Base`, rejected symlinks, and ran:

```text
lake clean
lake build
```

Both exited zero. The complete build output ends with `Built Proof` and
`Build completed successfully`; see
`evidence/05-stage5-clean-build.log`. After the build, `Base` still has the
exact generated tree hash above.

The candidate Lean sources contain no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`. Its trust-declaration inventory is empty. It defines the four target
arguments inside namespace `Proof` and one theorem, `Proof.final`; it neither
opens the generated target namespace for declarations nor defines or shadows
`targetStatement`. Source and target scans are in
`evidence/06-target-and-source-scan.log`.

`#check` and `#print Proof.final` show that its type is exactly the fully
qualified immutable target applied to those same four candidate definitions.
It is not a duplicate proposition, implication, existential, or separately
restated equation. The exact printed type and proof term are in
`evidence/08-proof-identity.log`.

The required command:

```text
#print axioms Proof.final
```

produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`sorryAx` is absent. None of the 44 project-local declarations in
`trust-inventory.json` is a dependency, and the candidate adds no declaration
to that inventory. The three printed names are fixed Lean core foundations:
proposition extensionality, classical choice, and quotient soundness. They are
not unrecorded project proof escapes. Exact output and reconciliation are in
`evidence/07-axioms.log`.

## Operational bridge audit

The generated proposition alone is structurally insufficient to certify the
four parameter implementations: I machine-checked a counterfactual theorem
using constant-true integer comparison, a map update that discards the old
map, constant-zero length, and identity substring. Those deliberately wrong
definitions still satisfy the three target conjuncts. I therefore did not
infer operational faithfulness from `Proof.final`.

I compared each actual candidate definition with its `kore_symbol`, bound
source rule IDs, the frozen source program, and the executable K rules:

| Parameter | Independent judgment |
|---|---|
| `«_<=Int_»` | `decide (x ≤ y)` is exactly K integer less-than-or-equal. Boundary evaluations `-1 ≤ 0`, `0 ≤ 0`, and `1 ≤ 0` returned `true`, `true`, and `false`, rejecting a constant-true implementation. |
| `«Map:update»` | It prepends the new `(key,value)` binding and removes every old binding at that key. On valid K maps this overwrites exactly one key and preserves every other binding, matching `ENV [ X <- V ]`. Existing-key and fresh-key adversarial examples both checked. It differs from the counterfactual singleton update because it preserves unrelated state. |
| `«lengthString»` | `Int.ofNat s.length` matches the K character-count hook. Independently compiled K literals and Lean evaluations agree on empty, ASCII, BMP `é`, astral `🙂`, and combining `é` inputs: `0,3,1,1,2`. This rejects constant, byte-length, and UTF-16-length substitutions. |
| `«substrString»` | Converting to the character list, dropping `start`, and taking `end-start` implements K's valid half-open substring. K and Lean agree on full, interior, Unicode, and empty ranges, including `"a🙂éz"[1:3] = "🙂é"`. All calls reachable through frozen `semantic.k` satisfy `0 <= start <= end <= length`; K rejects a negative constant index, so the candidate's total extension outside that unreachable hook domain is not used as evidence. It differs from identity substring on `"abcdef"[1:4]`. |

The map representation test also checks preservation of an unrelated
environment binding, so equality of the returned value alone is not the
oracle. String probes use compiled K literals rather than the known
configuration-variable serialization path. The counterfactual theorem,
adversarial examples, K probe, commands, and complete results are in
`evidence/OperationalAudit.lean`, `evidence/string-probe.k`, and
`evidence/09-operational-bridge.log`.

These checks establish operational fidelity on the complete domain reachable
from the frozen program and on every domain used by the source rules. The
candidate is not constant, identity, hard-coded to the displayed equations,
or state-discarding.

## Final judgment

Stage 3 has exactly three genuine, relevant domain lemmas. Stage 4 exports all
three and only those three without changing their meaning or target. Stage 5
proves the immutable conjunction from honest implementations, with a clean
build, exact proof identity, and no project-local trust escape.

VERDICT: PASS
LEGITIMACY: LEGIT
