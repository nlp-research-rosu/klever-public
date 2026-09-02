# Independent Stage 3–5 audit: `19-sort-numbers`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition
`semantics`, and semantics mode `SUPPLIED_SEMANTICS`. Stage 5 is therefore not
in scope: `/candidate` is absent, the audit input has no Stage 5 result, and
the generated target is null.

The artifact chain is cryptographically and mechanically self-consistent, but
the protected Stage 3 classification is mathematically wrong. One
problem-specific split connection rule is a `DOMAIN_LEMMA`, not an
`OPERATIONAL_RULE`. Consequently, the true domain set is nonempty while Stage
4 records `KLEAN_NO_OBLIGATIONS`, emits no obligation, and emits no target.
That is a proof-critical omission and requires `FAIL` / `NOT_LEGIT`.

Raw commands and results are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## Input and producer authentication

`/audit-input.json` passed the trusted schema-v4 envelope and canonical digest
check. Its resolved-input digest is
`7862e977293d3e0b58ca096fae3abf3b8fea4a950b66fd8e2893527c66030aca`.

All recomputable launcher hashes matched:

- selected Stage 1 workspace, pipeline tree hash:
  `9d2b6fa4d4e944e80022cc73bb2363bf7607a807913af8c871e13ef7d010b115`;
- canonical Stage 1 export, Klean tree hash:
  `2cd64a3906424e1895006b315271ec6e31aa29d74464caae4029500160129d55`;
- every listed Stage 1 source-file hash, including all supplied semantics
  files, `verification.k`, `spec.k`, and the solution;
- protected discovery manifest:
  `ba96f9400173d23831e63b4ec5b87920f46abbe48654c2562463fa73fa245dbf`;
- selected Stage 2 audit tree:
  `79e4325cecf2d4b4fff707d632a8d874a3f9b7351a8421e50ee4fddd65c6555d`;
- selected Stage 4 tree:
  `648c1252908510bdf761d9a0b5da67e7dfaa9979bd7f199fe6180b7d504d274e`;
- generated project tree:
  `2452fbcea27b8da2d4ff0dadfab28fe3d1869155558b56734c3d8ae657c26215`;
  and
- producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

Before evaluating generation, I independently hashed the two mounted producer
files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These values match both `source-manifest.json` and
`generator-manifest.json`. Both manifests name generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The final component of the launcher-recorded
`generation_producer_sources` path is the same image digest. There is no
producer-source infrastructure error. Full results are in
[`05-recorded-hash-check.txt`](evidence/05-recorded-hash-check.txt).

## Inventory reconstruction and protected-manifest bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen Stage 1 workspace. The local verification-module closure contains only
`SORT-NUMBERS-VERIFICATION`; `MPY` is supplied by the required external
semantics rather than by another local module in `verification.k`.

The reconstruction contains 31 rules and has inventory hash
`bbc103c45933fff14c2d2ca4db25fe227558633eacf355687354aabcd8c83563`.
For every rule I independently checked:

- the exact `start_line`/`end_line` slice against `verification.k`;
- SHA-256 of whitespace-normalized source;
- `source_rule_id = "rule-" + normalized_sha256`; and
- its ordinal in the reconstructed closure.

The protected manifest also contains exactly 31 unique entries. Its ordered ID
sequence is identical to the reconstruction, its ID set is identical, and its
whole-inventory hash matches. There are no omissions, duplicates, extra rules,
reordered identities, changed hashes, or unaccounted entries. See
[`03-reconstructed-rule-inventory.json`](evidence/03-reconstructed-rule-inventory.json)
and
[`06-inventory-bijection-check.txt`](evidence/06-inventory-bijection-check.txt).

This is a structural pass only; an ordered list of correctly hashed rule IDs
does not validate their semantic labels.

## Independent classification of all 31 rules

The full per-rule record, including text, span, normalized hash, protected
label, independent label, and rationale, is
[`12-independent-reclassification.json`](evidence/12-independent-reclassification.json).
Every ordinal is accounted for as follows:

| Inventory ordinals | Source lines | Count | Independent class | Reason |
|---|---:|---:|---|---|
| 0–3 | 9–49 | 4 | `DEFINITION` | `numberBody`, `sortBody`, `solutionModule`, and `numberKey` name translated syntax or a proof term. |
| 4–13 | 58–67 | 10 | `DEFINITION` | Exhaustive constructor equations define `wordVal`. |
| 14–15 | 70–71 | 2 | `DEFINITION` | Base and recursive equations define `wordsVS`. |
| 16–25 | 74–83 | 10 | `DEFINITION` | Exhaustive constructor equations define `wordCodes`. |
| 26–28 | 89–93 | 3 | `DEFINITION` | Base, singleton, and recursive equations define `encodedWords`. |
| 29 | 95–99 | 1 | `DOMAIN_LEMMA` | Problem-specific connection from splitting `encodedWords(WORDS)` to `wordsVS(WORDS)`. |
| 30 | 104–106 | 1 | `DEFINITION` | `numericOutput` names the expected joined/sorted summary. |

Thus the independent totals are 30 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`.
No inventory rule has a `simplification` attribute, so the special
simplification-label constraint is satisfied vacuously.

### Why rule 29 is a domain lemma

The supplied operational semantics already defines no-argument string split
in `semantics/methods.k:72-86`. Its ordinary execution rule allocates

```text
list(splitWS(CS, .IntSeq, .ValSeq))
```

and `splitWS` recursively scans character codes, flushing tokens on whitespace.
The local rule at `verification.k:95-99` instead recognizes the
problem-specific term `str(encodedWords(WORDS))` and directly allocates
`list(wordsVS(WORDS))` at higher precedence. It therefore preempts an existing
supplied-semantics execution, and its correctness requires the mathematical
connection

```text
splitWS(encodedWords(WORDS), .IntSeq, .ValSeq) = wordsVS(WORDS).
```

That connection is true and relevant:

- for `.NumWords`, both sides are empty;
- for a singleton, `wordCodes` contains only non-whitespace numeral letters,
  so `splitWS` flushes exactly `wordVal(W)`;
- for a sequence of at least two words, `encodedWords` inserts character code
  32, which `isWSC` recognizes as whitespace, so `splitWS` flushes the head
  and the induction hypothesis handles the tail; and
- `wordVal(W) = str(wordCodes(W))` follows by the ten constructor cases.

It is directly relevant to the source and postcondition: the source calls
`numbers.split()`, the symbolic input is `str(encodedWords(WORDS))`, and the
postcondition's `numericOutput` sorts and joins `wordsVS(WORDS)`.

It is not an ordinary operational/observation rule because the generic
operation is already modeled; this special rule asserts the connection
between two proof-local summaries across that operation. It is not a
`PROVED_DERIVED_LEMMA`: Stage 1 contains no earlier claim proving this exact
rule against a module without it. `prove.sh` compiles `verification.k` with
the rule present and then runs one `kprove` invocation.

The proof-sensitivity experiment confirms the role. In two fresh Stage 1
copies:

- with the frozen rule present, the isolated `sort-numbers-symbolic` claim
  returns `#Top`, exit 0; and
- after removing only lines 95–99, compilation still succeeds, but the same
  claim exits 1 with `WarnStuckClaimState`.

The residual explicitly compares the result through
`sortKeyVS(splitWS(encodedWords(WORDS), ...), numberKey)` with the claimed
result through `sortKeyVS(wordsVS(WORDS), numberKey)`. See
[`09-no-split-only-mutation.diff`](evidence/09-no-split-only-mutation.diff),
[`09-no-split-kprove-symbolic.txt`](evidence/09-no-split-kprove-symbolic.txt),
and
[`09-with-split-kprove-symbolic.txt`](evidence/09-with-split-kprove-symbolic.txt).

The protected label `OPERATIONAL_RULE` for
`rule-b25203fce8fc32addea6c7671ce933b1a9ee841e26d4b5263e1113d6ed4ffaed`
is therefore rejected.

## Stage 4 preflight and deterministic structure

I reran `tools.klean_preflight.check_generation` with the required frozen
workspace, protected discovery manifest, selected generation, pinned
toolchain lock, and `PYTHONPATH=/reference`.

The first direct run exposed an audit-sandbox issue: Lean's implementation of
`IO.appPath` calls `readlink("/proc/<pid>/exe")`, which this sandbox denies,
causing `lake clean` to report that it could not detect its installation.
The exact failure is
[`10-rerun-check-generation.txt`](evidence/10-rerun-check-generation.txt).
I then used a documented, narrow compatibility shim only for the temporary
build callback. It substitutes `program_invocation_name` only for
`/proc/*/exe` reads and delegates every other `readlink` call to libc. A
direct `lean --version` test under the shim reports the pinned Lean 4.22.0
commit. This workaround does not read, edit, or relax any generated Lean
source or any preflight structural check.

With that environment repair, the trusted function returned:

- status `KLEAN_NO_OBLIGATIONS`;
- frozen input
  `2cd64a3906424e1895006b315271ec6e31aa29d74464caae4029500160129d55`;
- discovery manifest
  `ba96f9400173d23831e63b4ec5b87920f46abbe48654c2562463fa73fa245dbf`;
- generated tree
  `2452fbcea27b8da2d4ff0dadfab28fe3d1869155558b56734c3d8ae657c26215`;
- zero recorded obligations;
- null target;
- 54 allowlisted trust declarations;
- zero designated sorries;
- `lake clean` exit 0; and
- `lake build` exit 0 with output hash
  `959fd3c0903bc7923bf9a8be6ece2baebed63851d5e7cf88e27fff5753bb6f81`.

The returned document exactly matches the launcher-recorded preflight. See
[`10-rerun-check-generation-compatible.txt`](evidence/10-rerun-check-generation-compatible.txt).

I also independently checked the generated sidecars and target:

- `obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching `generator-manifest.json`;
- its `source_rules`, `obligations`, and `trust_parameters` arrays are all
  empty;
- the input manifest's recorded domain-source list is also empty;
- the recorded source IDs and obligation IDs form an exact ordered empty
  bijection, with no duplicates;
- `Lemmas.lean` has no `targetStatement`;
- trusted target extraction returns null;
- expected-target construction from the empty obligation map returns null;
  and
- that null target matches the generator manifest, export result, recorded
  preflight, and audit input.

Accordingly, deterministic Stage 4 is structurally exact relative to the
incorrect protected classification. There are no generated irrelevant,
weakened, duplicated, or vacuous conjuncts because there are no conjuncts at
all.

The mathematical completeness check fails: the independently reconstructed
domain-source sequence is

```text
[rule-b25203fce8fc32addea6c7671ce933b1a9ee841e26d4b5263e1113d6ed4ffaed]
```

while the generated sequence is `[]`. The exact source-rule/obligation
bijection that should contain this rule is therefore missing one entry and
its corresponding target conjunct. Evidence is in
[`13-stage4-bijection-and-target-check.txt`](evidence/13-stage4-bijection-and-target-check.txt).

`KLEAN_NO_OBLIGATIONS` is not legitimate because the true domain set is not
empty. Manifest self-consistency cannot cure that omission.

## Stage 5

This is `CLASSIFICATION_ONLY`. There is no generated target, no Stage 5 result,
and no `/candidate` mount. That is structurally consistent with the selected
but invalid zero-obligation Stage 4 result. Candidate clean-build,
`Proof.final`, axiom reconciliation, and operational-bridge parameter checks
are not applicable in this mode.

## Final judgment

The hashes, inventory identity, producer provenance, deterministic generated
tree, recorded empty bijection, null target, and generated-project build all
check out. The semantic classification does not. A relevant, proof-critical
domain lemma was labeled `OPERATIONAL_RULE`, suppressing the only required
Stage 4 obligation and all possibility of a fixed theorem target. Under the
required rule for a nonempty true domain set paired with
`KLEAN_NO_OBLIGATIONS`, this is a failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
