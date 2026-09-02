# Independent Stage 3–4 Audit: `101-words-string`

## Scope and result

The launcher and environment both record:

- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

I treated the mounted candidates, prior reviews, manifests, comments, and logs
as untrusted evidence. I reconstructed the rule inventory with the trusted
inventory code, classified the rules from the frozen source and K semantics,
authenticated the generation-time producer, reran the trusted Stage 4
preflight, and independently checked the hash, obligation, and target
bindings. The selected no-obligation result is legitimate.

## Producer authentication

Before judging Stage 4, I hashed the mounted generation-time producer files.
The observed values are:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |

Both hashes exactly match the per-file records in
`source-manifest.json` and `generator-manifest.json`. The immutable generator
image ID is consistently
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`
in the source manifest, generator provenance, and the producer-bundle path
recorded by `/audit-input.json`. Using the launcher's
`pipeline_contract.sha256_tree` algorithm, the mounted producer bundle hashes
to `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a`,
exactly the audit-input value.

An initial diagnostic used the generated-project `tree_digest` algorithm on
this bundle and therefore produced a different directory digest. Evidence
`06-producer-authentication-launcher-hash.txt` records the corrected,
launcher-equivalent check; the required individual source hashes and image ID
never differed.

## Inventory reconstruction and manifest bijection

The trusted `tools.k_rule_inventory.inventory_verification` reconstruction
selected `VERIFICATION` as the verification module. Its local-module closure
contains only `VERIFICATION`; imports `STRING`, `LIST`, `INT`, and `BOOL` are
external modules, not additional modules defined in frozen
`verification.k`.

The reconstructed `verification.k` SHA-256 is
`82ee1f94a4d495cae06a684ea151f27c5c0e42fafd3f6a0080fa42e852953d4e`.
The canonical whole-inventory SHA-256 is
`086bf69ce233b71b39bec7b995b58e03fdb91b9abb938717d25130a09d35f43a`.
Both match the Stage 3 records.

For every rule, I separately sliced the recorded physical source lines,
normalized whitespace, hashed the normalized text, and rebuilt
`source_rule_id` as `rule-<normalized SHA-256>`. Every span text, normalized
hash, and ID matched:

| Lines | Normalized SHA-256 / source-rule suffix | Independent class |
|---|---|---|
| 11 | `0f2b3c0338c308c6e540e36730e5ce4e0f8f0ce7c8eed855c5c9e34f9a98c000` | `DEFINITION` |
| 12–14 | `e491c1fb0e8e00626c57da7bdf738586273f4a383040729fc31c9d3d5ddad722` | `DEFINITION` |
| 15–17 | `a19d226dc5883e21f248c0a3e052522d97865bf258b9f04af3c7413224ce82b9` | `DEFINITION` |
| 18–22 | `11ff21fab5c88224bb89c0f5615f702abcdd7f3511f2cfdc579a426b8eadba59` | `DEFINITION` |
| 27 | `72df39d002c7268a5910d129469e892464cbf0bd4498cc96570a2b633e890396` | `DEFINITION` |

The Stage 3 manifest has exactly these five IDs, once each and in this exact
order. There are no omitted, duplicated, extra, reordered, or hash-changed
entries. The trusted `validate_trust_boundary` check also passed and produced
counts of five definitions and zero entries in each other category.

## Independent classification judgment

All five classifications are mathematically appropriate:

1. Line 11 is the base equation for the named `splitSpaces : String -> List`
   summary.
2. Lines 12–14 are its leading-space recurrence. On a nonempty string whose
   first character is a space, it removes that character and recurs on a
   strictly shorter suffix.
3. Lines 15–17 are its nonempty, no-space terminal equation, producing one
   list item.
4. Lines 18–22 are its word-producing recurrence. It emits the nonempty
   prefix before the first space, removes that space, and recurs on a strictly
   shorter suffix.
5. Line 27 is the defining macro for the named
   `wordsContract : String -> List` summary: replace commas by spaces, then
   apply `splitSpaces`.

These are equations defining named summaries and their recursion. They do not
rewrite an execution configuration, observe program state, assert a separate
mathematical fact, or claim a result derived in an earlier proof. Thus none is
an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`.

This agrees with the frozen operational K semantics. The source solution
evaluates `s.replace(",", " ").split()`. `semantic.k` evaluates the replace
call with `replaceAll`, evaluates the zero-argument split call with
`splitSpaces`, and the postcondition names that same result with
`wordsContract`. The four `splitSpaces` cases cover empty input and, for
nonempty input, first-space positions zero, absent, or positive. The recursive
cases decrease string length.

I also compiled a fresh temporary copy of the frozen semantics and ran
operational cases for empty input, separator-only input, repeated and edge
separators, a singleton word, and alternating comma/space runs. They produced,
respectively, the empty list, empty list, `["alpha", "beta", "gamma"]`,
`["alpha"]`, and `["a", "b", "c"]`. These executions are finite supporting
evidence; the classification itself follows from the rule forms and semantic
roles.

No inventory rule has a `simplification` attribute, so the special
simplification restriction is vacuously satisfied. More importantly, the
independent true domain-lemma set is genuinely empty rather than hidden by a
misclassification.

## Stage 4 structural and mathematical audit

I invoked
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required frozen Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
trusted toolchain lock.

The container initially lacked `/proc/<getpid()>/exe`, although
`/proc/self/exe` was available. Lean 4.22 uses the former spelling to locate
its installation, so the first preflight stopped at `lake clean` before any
project check or compilation. I used the recorded minimal compatibility shim
that redirects only the current process's exact
`/proc/<getpid()>/exe` `readlink` to the equivalent `/proc/self/exe`.
It does not alter the pinned Lean/Lake binaries or any mounted input. With
that environment repair, the exact trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `9a65182771b5fb46f74d46f07c22548113b5e1611707d0304da572ab49171926`;
- obligation count 0;
- target `null`;
- designated sorry count 0.

The final build-output hash is also exactly the value recorded in
`/audit-input.json`. Complete failed and successful outputs and the shim source
are retained under `evidence/`.

Independent cross-record checks produced these observed values:

| Artifact | Observed SHA-256 |
|---|---|
| Stage 1 workspace, launcher tree algorithm | `54977efe684cc985090d33eef37f1439ad11b6ffe9db9390222a33907286bc0d` |
| Stage 1 frozen export, generator tree algorithm | `44cbb605ddf09ceedcd8f64e929c741938bab26c6385693a718c2b80dfb817d8` |
| Stage 2 selected K audit tree | `8a44beb46a559401511a3da19731d8f97f769b6d2625f4db65cbcb960e7443f0` |
| Stage 3 discovery manifest | `13a569446dc756ad2453b007958db7d8d47c79d2171374b0d4049c849ed5c162` |
| Selected Stage 4 generation tree | `2ccea9c1229c00d0567326353b483c004525152e1582f757744c349e4a7d7025` |
| Generated project tree | `75171b4dcb523034e694c74f5911cc44f932e14e04dc27f6fde7e4750914d1e2` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `0ef049965580c79fd2ef1a19a7445d4ff02a3ed3076ec4b197d866dcbd9ffaf7` |
| Resolved audit input | `5408482764f4d37804da3a2c13b4d625c1d39466d37491ca542833c3deff1583` |

Every value matches its applicable audit input and manifest records. Every
individual Stage 1 source hash also matches. The generator toolchain object is
identical to the trusted toolchain lock.

The exact source-rule/obligation relation is:

- independently classified domain source rules: `[]`;
- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- generated trust parameters: `[]`.

All obligation counts are zero. This is an exact empty-set bijection, not an
omission, duplicate, weakened obligation, vacuous `True` conjunct, or
irrelevant theorem. `target_statement(generated)` is `null`, and the generator
manifest, recorded preflight, export result, and audit input all likewise have
no target. `Lemmas.lean` contains only an empty namespace, so no target was
hidden under another declaration.

## Stage 5 applicability

Stage 5 proof auditing is not applicable. Both `AUDIT_MODE` and
`/audit-input.json` say `CLASSIFICATION_ONLY`; Lean workspace, Lean invocation,
Stage 5 result, and target are all null, and `/candidate` is absent. This is
the required state for a legitimate `KLEAN_NO_OBLIGATIONS` result. Therefore
there is no `Proof.final`, target parameter, candidate bridge, or candidate
axiom list to audit.

## Evidence index

The exact commands are in `evidence/COMMANDS.txt`. Principal machine-readable
or raw outputs are:

- `06-producer-authentication-launcher-hash.txt`
- `05-inventory-reconstruction.txt`
- `03-frozen-sources-and-classification.txt`
- `15-check-generation-final.txt`
- `16-independent-stage4-checks-final.txt`
- `14-operational-k-adversarial-cases.txt`
- `13-generated-project-and-trust.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
