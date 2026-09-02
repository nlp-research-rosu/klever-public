# Independent audit: HumanEval 17-parse-music

## Scope and audit mode

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and the Stage 3 classification plus deterministic Stage 4
generation. Both `AUDIT_MODE` and `/audit-input.json` record
`CLASSIFICATION_ONLY`. The launcher records no Stage 5 workspace or invocation,
and `/candidate` is absent, as required for this mode.

I treated the mounted workspaces, manifests, prior reports, logs, comments, and
classifications as untrusted evidence. I did not adopt an earlier PASS or
classification. Executed verification code was limited to trusted tooling
below `/reference/tools`; candidate/provenance source was inspected as data.

## Producer authentication

Stage 4 was not judged until the generation-time producer sources were
authenticated.

| Binding | Recomputed value | Recorded value | Result |
|---|---|---|---|
| `klean_export.py` SHA-256 | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| `klean.py` SHA-256 | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| Producer bundle tree SHA-256 | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Same in `/audit-input.json` | Match |
| Generator image ID | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` | Same in generator provenance, source manifest, and the terminal component of the producer path recorded by `/audit-input.json` | Match |

The producer bundle contains exactly `klean_export.py`, `klean.py`, and
`source-manifest.json`. Evidence is in
`evidence/producer-authentication.json` and
`evidence/producer-provenance.txt`. There is no producer-source infrastructure
error.

## Recorded-input hash reconciliation

I recomputed the launcher bindings using their trusted, format-specific hash
algorithms. All recorded values match:

- signed resolution digest:
  `c02a9b6e9fd302ae83a0723a5e351e5fc123e903259caa13c50192d25cbc84a8`;
- Stage 1 pipeline tree:
  `b894ae2f2d27466ee2c63bf82eb833ca09fc2d04c43e1fe9993968246adad88d`;
- Stage 1 deterministic-export tree:
  `c69673ed3571bb40346a0b808238b0fc8760833901a85a61089879aa5ac21749`;
- selected Stage 2 K-audit tree:
  `161662de0d25c2a4a4c882d47c1739b453e3b167d4f924a3c1982a27ec4998b5`;
- Stage 3 manifest:
  `e2e1273ab20946476de5cc4adf25022e2ac70e4de10da6d8d9858c27d9fa04f3`;
- Stage 4 generation tree:
  `d7986af58954168231aa7d069cc023ca51e49a9c2998f8be897de269f1f4301f`;
- generated project tree:
  `69343ad83e227dc7dbe4439a21bd5825bc87f04945b76cffc66333d2fe78b94c`;
- producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

The launcher’s complete map of 770 Stage 1 file hashes is also an exact
bijection with the mounted workspace: no missing, extra, or changed file.
The two Lean hashes are consistently null in classification-only mode. See
`evidence/hash-reconciliation.json`.

## Canonical rule-inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against the frozen `/reference/k-proof` workspace. The
trusted parser selected `VERIFICATION` from `prove.sh` and reconstructed its
local module closure in source order:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION`

The frozen `verification.k` SHA-256 is
`c2216fe4ac0ed219a5fc6cc7a122a8476f63aa0bb3920533801703a8fd03f6a4`.
The reconstruction contains 17 rules. For each rule, the trusted inventory
recomputed the physical start/end span, whitespace-normalized source SHA-256,
`rule-<normalized-sha256>` identity, attributes, and exact source text. The
canonical JSON hash of the ordered 17-rule array is
`932e796013ca30c337145920f57c5b5c304c9fb7d35633917a2a159a409a7759`.

Comparison with `/reference/lemma-discovery.json` is bijective and
order-sensitive:

- 17 canonical identities and 17 manifest identities;
- exact ordered-list equality;
- all identities unique;
- no omission, duplicate, extra rule, changed identity, or reordering;
- manifest inventory hash equals the independently reconstructed inventory
  hash;
- the trusted Stage 3 contract validator also passes.

The complete reconstructed entries are in
`evidence/canonical-inventory.json`; the explicit ordered comparison is in
`evidence/inventory-comparison.json`.

## Independent Stage 3 classification

I classified all 17 entries from their frozen source and their role under the
supplied operational semantics.

| Rules | Independent classification | Reason |
|---|---|---|
| Lines 28–35 and 37–51 | `DEFINITION` | `parseMusicBody` and `parseMusicCharBody` are nullary `[function, total]` terms of sort `Stmts`. Their equations expand named proof terms to the exact source AST. They have no configuration cells and do not replace the supplied execution rules. |
| Lines 54–61 and 63–77 | `DEFINITION` | The two mutation-only body terms likewise name statement ASTs. The changed `o := 5` body is not referenced by the positive claim. |
| Lines 79–84 | `DEFINITION` | Three disjoint, exhaustive guarded equations define the one-character `nextCurrent` state transition for `o`, `.`, and every other code. |
| Lines 86–98 | `DEFINITION` | Four disjoint, exhaustive guarded equations define how one character changes the accumulated result: pipe/current-4, pipe/other-current, ordinary separator/current-4, and the complementary no-append cases. |
| Lines 100–106 | `DEFINITION` | Base and strict-tail recursive equations define `scanCurrent` and `scanResult`. They consume one `IntSeq` element on every recursive step. |
| Lines 108–112 | `DEFINITION` | Two complementary guarded equations define the terminal `musicResult` flush. |

Independent totals are therefore:

- `DEFINITION`: 17
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Every reconstructed rule has an empty attribute list. In particular, there is
no `simplification` rule that could have been mislabeled as operational or
derived.

This classification does not confuse summary definitions with facts about the
summary. The transition and recurrence rules define named mathematical
functions; they do not assert an additional ordering, membership, arithmetic,
or postcondition property. The connection from supplied execution to those
functions is stated in the `scan-loop` and `parse-music` K claims, not installed
as one of the inventory rules. No inventory rule qualifies as an ordinary
execution/observation rule, and no rule is claimed as a separately proved
derived lemma.

The operational reading was checked against the relevant supplied rules:
string iteration yields one-code strings; equality compares their `IntSeq`
representations; `For` repeatedly binds and executes the body; `If` follows
truthiness; assignment updates the active scope; and `list.append` mutates the
heap by `valSeqConcat`. These rules give exactly the transition encoded by
`nextCurrent` and `nextResult`, including unusual inputs:

- a bare pipe appends the current value, hence input `|` yields `[0]`;
- repeated `o` characters leave one pending whole note, hence `oo` yields
  `[4]`;
- a non-note separator flushes a pending 4 and resets current;
- arbitrary represented integer character codes take the complementary
  branch.

As adversarial evidence, I compared a direct statement-level execution model
against the independent transition/fold model for all 55,987 strings of
length 0–6 over codes `111`, `46`, `124`, `32`, `-1`, and `128`. There were
zero mismatches. I also tested 1,224 representative guard points and found no
guard overlap or gap. Counterfactually changing the executing body’s `o`
assignment from 4 to 5 disagrees with the frozen summary on `o`, `o|`, and
`o `, demonstrating body sensitivity rather than a convenient constant or
vacuous summary. Detailed entry-by-entry classification is in
`evidence/stage3-reclassification.md`; the check output is in
`evidence/semantic-crosscheck.txt`.

The protected Stage 3 classifications agree with this independent result. The
true domain-lemma set is genuinely empty.

## Deterministic Stage 4 preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, exactly the frozen Stage 1 workspace, protected Stage
3 manifest, selected Stage 4 generation, and trusted toolchain lock.

The first call reached the checker’s temporary `lake clean` but failed before
compilation because this audit process’s namespace PID is not represented in
the mounted read-only `/proc`; Lean’s application-path lookup therefore could
not detect its installation. That infrastructure-only attempt is preserved in
`evidence/check-generation-output.txt`.

I used the narrow compatibility shim recorded in
`evidence/proc-self-fix.c`: it redirects only
`readlink`/`readlinkat("/proc/<numeric-pid>/exe", ...)` to
`/proc/self/exe`. It does not alter any project, manifest, source, command
result, or compiler option. With that environment correction, the unchanged
trusted preflight completed:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0;
- build output SHA-256:
  `41b779fcc6c3f64d540197fe3008da14f7933e33c61cd19960439f1838334573`,
  exactly equal to the previously recorded Stage 4 preflight output hash;
- checker status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- generated target: null;
- designated sorry count: 0;
- generated-project trust declarations: 41.

The 41 declarations are the checker-allowlisted executable collection-hook
parameters in the targetless generated library; the preflight independently
rejects proposition trust. Because there is no generated proposition or proof,
they do not discharge an obligation.

The complete returned checker evidence is in
`evidence/check-generation-output-rerun.txt`.

## Obligation bijection and fixed target

I separately reconciled the mathematical domain set and every recorded Stage 4
list:

| Source of rule IDs | Ordered IDs |
|---|---|
| Independent reclassification | `[]` |
| Stage 3 `DOMAIN_LEMMA` entries | `[]` |
| `input-manifest.json` source rules | `[]` |
| `obligation-map.json` source rules | `[]` |
| `obligation-map.json` obligations | `[]` |

All five lists are identical and duplicate-free. The obligation-map SHA-256
recomputes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The obligation count is zero in the map,
generator manifest, and export result. The trust-parameter list is empty.

The generator’s expected-target function returns null for this map. Independent
source inspection finds no `generatedTarget` definition or theorem. The
recomputed target, generator-manifest target, launcher target, and recorded
preflight target are all null. Thus Stage 4 did not replace an empty conjunction
with a vacuous `True` theorem; it generated no target at all. There are no
obligations that could be irrelevant, weakened, duplicated, omitted, or made
vacuous.

The generated tree hash matches the generator manifest and launcher. The
selected status, export status, recorded preflight status, and fresh checker
status all agree on `KLEAN_NO_OBLIGATIONS`. `/candidate` is absent, so no Stage
5 proof was smuggled into classification-only mode. Structured evidence is in
`evidence/stage4-bijection-and-target.json` and
`evidence/candidate-presence.txt`.

## Judgment

The protected Stage 3 manifest is a complete, ordered, hash-exact
classification of the canonical local verification-rule closure. Its
classification is mathematically correct: every entry is a genuine definition
of a named statement term, state transition, recurrence, or final summary, and
there are no domain lemmas. Consequently the deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` result is the required result, not an omission. Producer
provenance, all launcher hashes, the empty obligation bijection, generated-tree
identity, target absence, fresh build, and Stage 5 absence all reconcile.

VERDICT: PASS
LEGITIMACY: LEGIT
