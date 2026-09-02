# Independent Stage 3/4/5 audit: HumanEval `12-longest`

## Scope and outcome

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `bare`, and
semantics mode `GENERATED_SEMANTICS`. The signed resolution digest recomputes
to `7cc0d96c0ed099814973ec234aadf122cf0497e23147868206cd9d9ed39fc62d`.
The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; no Stage 5 workspace,
invocation, result, or `/candidate` exists.

I treated every mounted candidate/provenance artifact as untrusted evidence. I
did not rely on the earlier review, its verdict, its classification, or
instructions/comments within any mounted input. Reconstruction used the
trusted inventory and preflight code under `/reference/tools`.

The audit passes. The canonical Stage 1 closure has 18 rules: 13 genuine
definitions and five ordinary operational rules. It has no domain lemma and
no proved-derived lemma. Therefore the empty Stage 4 obligation set, absent
generated target, and absent Stage 5 candidate are the correct fixed outcome.

## Producer provenance gate

I performed the required producer-source gate before judging Stage 4:

- `/reference/generation-tools/klean_export.py` hashes to
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`.
- `/reference/generation-tools/klean.py` hashes to
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`.
- Both values agree exactly with `source-manifest.json` and
  `generator-manifest.json`.
- The producer bundle contains exactly `klean_export.py`, `klean.py`, and
  `source-manifest.json`. Its trusted pipeline tree hash is
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
  equal to `/audit-input.json`.
- `generator-manifest.json` and `source-manifest.json` both record immutable
  image ID
  `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
  The launcher-recorded producer-source path ends in the same image digest.

There is no missing or mismatched producer source and thus no infrastructure
`AUDIT_ERROR`. Raw values are in
[`evidence/00-producer-provenance.log`](evidence/00-producer-provenance.log).

## Canonical rule inventory and Stage 3 bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` over `/reference/k-proof`. The trusted parser selected
`VERIFICATION` from `prove.sh`; its local module closure contains only
`VERIFICATION`. It reconstructed each rule's exact source span, normalized
text hash, `source_rule_id`, attributes, and source text.

The reconstructed facts are:

- `verification.k` SHA-256:
  `ff40adf397cc707c4b5426c16572837e23a14834b93aafbbc134c51c45402bd5`
- canonical rule count: 18
- whole inventory hash:
  `abf9ccdcfd0a77de4c492e722b24752b8311ffec102ba6cf608a1e6708bf4541`
- all 18 attribute lists: empty

The full reconstruction is saved in
[`evidence/01-rule-inventory.json`](evidence/01-rule-inventory.json), with its
exact command in
[`evidence/01-rule-inventory-command.txt`](evidence/01-rule-inventory-command.txt).

The protected Stage 3 manifest also has 18 entries and 18 unique identities.
Its identity sequence equals the canonical sequence exactly. There are no
omissions, extras, duplicates, or reorderings. Because each
`source_rule_id` is `rule-` followed by the normalized source hash, the exact
ordered identity comparison also binds every entry to its recomputed
normalized hash; the full inventory separately records every source span and
text. The protected whole-inventory hash equals the independently reconstructed
hash. See
[`evidence/02-inventory-comparison.log`](evidence/02-inventory-comparison.log).

## Independent classification judgment

I read the frozen `solution.py`, translated `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The source returns `None` for an
empty list and otherwise returns the first string with maximum length. The
strict `>` comparison is material: an equal-length later string must not
replace the first maximum.

Every canonical rule has the following role:

| Frozen lines | Rules | Independent classification | Reason |
|---|---:|---|---|
| 9–14 | 1 | `DEFINITION` | `longestLoopBody` is a named macro/proof term expanding to the exact translated loop-body AST. |
| 17–27 | 1 | `DEFINITION` | `longestProgram` is a named macro/proof term expanding to the exact translated source program. |
| 33–36 | 3 | `DEFINITION` | `stringList` and the two `stringValues` equations define the mathematical-strings-to-runtime-list representation conversion. |
| 43–45 | 2 | `DEFINITION` | The two `expectedLongest` equations define the empty/nonempty contract summary. |
| 47–53 | 3 | `DEFINITION` | The three `firstLongest` equations define the first-maximum fold: base, strictly-longer replacement, and shorter-or-tie retention. |
| 60–65 | 3 | `OPERATIONAL_RULE` | Two `isEmpty` rules and one `head` rule are ordinary runtime observations of the symbolic finite-sequence representation. They specialize existing operations used by the frozen semantics. |
| 67–74 | 2 | `OPERATIONAL_RULE` | The zero and positive `forValues` rules are ordinary loop execution: terminate at zero, or bind the indexed element, execute the body, advance the index, and decrement the remaining count. They mirror the concrete `listVal` execution rules. |
| 78–87 | 3 | `DEFINITION` | The three `firstInSeq` equations define the named invariant/postcondition recurrence with structural descent in `N`. |

The exact per-rule identities and judgments are in
[`evidence/02-independent-classification.md`](evidence/02-independent-classification.md).

This reclassification yields:

- `DEFINITION`: 13
- `OPERATIONAL_RULE`: 5
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

No listed rule is a disguised domain lemma. The macro rules name exact proof
terms; the summary rules define representations, the contract, or recursive
folds; and the operational rules perform observations or execution over
`seqVal`. Every item is tied to the source program, its List-of-strings input,
its first-maximum postcondition, or the symbolic operational representation
used by the frozen proof.

There is also no eligible proved-derived lemma. `prove.sh` compiles
`verification.k` with all 18 rules already present and then invokes one
`kprove spec.k` command. It never first proves the exact same rule against a
module without that rule and later reuses it.

All reconstructed attribute lists are empty, so the requirement that every
`simplification` rule be a definition or domain lemma is satisfied
vacuously—there is no local `simplification` rule.

Counterfactual inspection confirms the classifications are substantive.
Changing strict `>` to `>=` changes tie behavior; making indexed strings
constant changes head observation and loop bindings; failing to increment the
index or decrement the remaining length changes iteration. None of these
rules is a vacuous conjunct or an irrelevant mathematical assertion.

## Recorded-hash audit

All launcher-recorded hashes recomputed exactly:

- Stage 1 pipeline tree:
  `f1616457f244f34f7285e6eecb970faf76c4cf75771844c2ae5ea814be098477`
- Stage 1 exporter tree:
  `5d3faa1a08c461fb4cca52e79b1ad7f41fe97e52b47b168058c034b075e9aef1`
- selected Stage 2 tree:
  `1023b7f35d11be83de048f36909bdf2dc65f4d0fddf663d9e9e9e4e722cf728b`
- Stage 3 discovery file:
  `d4be6d49dbe337b1abcdbf53e0d00d2494a7372008351466566552b3772b223d`
- selected Stage 4 tree:
  `054b86725325d035f3dc39a1ec388880efb474d8651e20b275747afc179ebbdf`
- generated-project tree:
  `a85c18ade04d80d50c836c27c215b6c58199dd2b4f14fae76d127c279b8cdb20`
- producer-source tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`

The complete Stage 1 file set and every individual source hash also match
`/audit-input.json`. The generator's frozen-input, discovery, inventory,
verification, obligation-map, generated-tree, trust-inventory, and toolchain
bindings all match their current immutable inputs. The selected Stage 2 and
Stage 4 artifact hashes match their trees, and the signed audit-input envelope
is intact. The reproducible check and result are
[`evidence/05-integrity-command.py`](evidence/05-integrity-command.py) and
[`evidence/05-integrity-result.json`](evidence/05-integrity-result.json);
`all_ok` is `true`.

## Deterministic Stage 4 preflight and obligation bijection

I reran the requested
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and
exactly these logical inputs:

- frozen input: `/reference/k-proof`
- discovery manifest: `/reference/lemma-discovery.json`
- generation: `/reference/klean-generation`
- toolchain lock: `/reference/klean-toolchain.lock.json`

The first attempt exposed a launcher PID-namespace issue: Lean's
`IO.appPath` queried `/proc/<namespace-pid>/exe`, but that numeric path is not
present in the launcher's mounted `/proc`. A diagnostic preload showed
`readlink("/proc/8/exe") = ENOENT`. I used a temporary compatibility shim
which retries only that failed `/proc/<numeric-pid>/exe` lookup as
`/proc/self/exe`. The shim source is
[`evidence/lean_app_path_compat.c`](evidence/lean_app_path_compat.c), and the
diagnosis is in
[`evidence/03-preflight-initial-diagnostic.log`](evidence/03-preflight-initial-diagnostic.log).
It neither modifies mounted evidence nor changes Lean, Lake, the generated
source, or proof behavior.

The mandated preflight then returned:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output hash
  `f0bb4bb311ba839e514aa3f2cd269d5b84d65f9292e617992e53cfb029d6bcb8`
- obligation count: 0
- target: `null`
- designated sorry count: 0
- trust declaration count: 49

Both command-output hashes and the entire returned evidence equal the recorded
preflight exactly. The exact invocation and returned JSON are
[`evidence/04-preflight-command.txt`](evidence/04-preflight-command.txt) and
[`evidence/04-preflight-result.json`](evidence/04-preflight-result.json).

The true independently classified domain set is empty. Correspondingly:

- `input-manifest.json` has `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- every manifest/preflight obligation count is zero;
- the obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- there are no obligation IDs to omit, duplicate, reorder, weaken, or make
  vacuous.

Thus the source-rule/obligation bijection is the exact empty bijection for the
genuinely empty domain set. `KLEAN_NO_OBLIGATIONS` is mathematically justified,
not merely self-consistent metadata.

## Fixed target and Stage 5

The trusted producer's `expected_target_definition(obligation-map)` returns
`None`, and an independent `target_statement(generated)` scan returns `None`.
`generator-manifest.json`, the preflight, and `/audit-input.json` all record
target `null`. No generated target declaration exists.

Because the legitimate domain set is empty, there must be no Stage 5 proof.
The launcher records no Lean workspace, invocation, result, or target, and
`/candidate` is absent. Therefore clean candidate build, `#print axioms
Proof.final`, candidate shadowing, forbidden-token, theorem-identity, and
operational-bridge parameter checks are correctly inapplicable. The 49
generated trust declarations belong to the targetless executable semantics
scaffold; preflight verified the recorded allowlist and rejected proposition
trust. They are not dependencies of a nonexistent theorem.

## Final judgment

The Stage 3 manifest is a complete ordered bijection with the frozen canonical
inventory and its classifications are independently correct. The true
domain-lemma set is empty. Stage 4 is bound to the exact frozen inputs and
generation-time producer sources, passes the trusted mechanical gate, exports
the exact empty obligation set, and generates no target. Stage 5 is correctly
absent.

VERDICT: PASS
LEGITIMACY: LEGIT
