# Independent Stage 3–5 audit: `147-get-max-triples`

## Scope and outcome

This audit covers condition `bare` under `GENERATED_SEMANTICS`. Both
`AUDIT_MODE` and the signed resolution in `/audit-input.json` say
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; the signed Stage 5 result and paths are null, and
`/candidate` is absent.

I treated the mounted K workspaces, manifests, generated files, earlier audit,
logs, and comments only as untrusted evidence. The conclusions below come from
fresh reconstruction with the locked tools, direct source inspection, fresh
hashing, independent mathematical analysis, and a rerun of the trusted
generation preflight.

## Producer and checker provenance

The required producer gate passes:

| Producer | Observed SHA-256 | Recorded result |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | Matches `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | Matches `source-manifest.json` and `generator-manifest.json` |

The producer bundle contains exactly those two sources plus
`source-manifest.json`. Its tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching the signed audit input. The image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in both manifests, and the same digest is the immutable producer-bundle key in
the signed audit path. There is therefore no producer-source infrastructure
error.

The launcher’s mechanical-checker lock hashes to
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`,
exactly the value in `/audit-input.json`. Every one of its eight locked
`/reference/tools` file hashes also matches. The Klean toolchain lock is
identical to the toolchain object in `generator-manifest.json`.

## Inventory reconstruction and Stage 3 bijection

Using the locked `tools.k_rule_inventory.inventory_verification`, I
reconstructed the local module closure rooted at the selected `VERIFICATION`
module. The closure contains the locally declared module `VERIFICATION`; `MPY`
is supplied by the required semantics file rather than declared as another
local module in `verification.k`.

The frozen `verification.k` hash is
`4a366e9e0d63d8e26123e0ff6c326cdd9ba588f2da3c00ed81cbd4f350dc15a3`.
The complete reconstructed inventory, in source order, is:

| Span | Normalized SHA-256 / `source_rule_id` | Attributes |
|---|---|---|
| line 9 | `5594fc18d5a757bd7bc014744a8a19e50e1ec19fb7038acbd49648528470fc16` / `rule-5594fc18d5a757bd7bc014744a8a19e50e1ec19fb7038acbd49648528470fc16` | none |
| lines 16–18 | `6d32eb21bafe6c64f6064ecdd1a030bcb2fbcfbd60c40dcdbe25253ac5f1150b` / `rule-6d32eb21bafe6c64f6064ecdd1a030bcb2fbcfbd60c40dcdbe25253ac5f1150b` | none |

The canonical whole-inventory hash is
`82eac2a78f10c8fe4e60ce086d678804728d8b0fda041bf90ab10a4089b39d19`.
It matches the Stage 3 manifest, Stage 4 input manifest, and generator
provenance.

The two Stage 3 entries have exactly the reconstructed IDs in exactly the same
order. The IDs are unique, and every ID’s span, source text, normalized hash,
and module are reproduced by the trusted inventory. There are no omitted,
duplicated, extra, reordered, or changed rule identities.

## Independent classification judgment

Both entries are correctly classified as `DEFINITION`.

1. `choose3`

   The rule at line 9 is the defining equation for the freshly declared total
   function `choose3(Int)`. Its left-hand side names a mathematical summary,
   and its right-hand side gives that summary’s arithmetic expansion. It does
   not match an execution cell, observe operational state, or replace an MPY
   program term. It is not a claim proved without itself.

2. `validTripleCount`

   The rule at lines 16–18 is the defining equation for the freshly declared
   total summary `validTripleCount(Int)`. This is the only definition of that
   symbol, and the Stage 1 postcondition explicitly returns
   `validTripleCount(N)`. The equation names the two residue-class combination
   counts; it is not an equation about a pre-existing operational function.
   Consequently it is a definition, not a concealed domain lemma.

Neither rule can be a `PROVED_DERIVED_LEMMA`: `prove.sh` has one positive
`kprove` command, and it runs only after compiling `verification.k` with both
rules already present. Neither is an `OPERATIONAL_RULE`: the ordinary MPY
execution rules are in `semantic.k` and evaluate module loading, lookup,
arithmetic, floor division, and return. The two inventory rules only reduce
new summary symbols. Neither inventory entry has a `simplification` attribute.

The independent true `DOMAIN_LEMMA` set is therefore empty.

The definitions are materially relevant, rather than arbitrary names. For an
index `i`, `i*i-i+1` has residue 0 modulo 3 exactly when `i` is 2 modulo 3 and
otherwise has residue 1. A three-term sum from residues `{0,1}` is divisible
by 3 exactly for residue multisets `{0,0,0}` and `{1,1,1}`. The class sizes in
`1..N` are `(N+1)//3` and `N-(N+1)//3`, so their two `choose3` values are the
source program’s formula and the postcondition’s summary.

As finite independent support, a direct enumeration of the HumanEval triples
matched the frozen summary for every `N` from 1 through 80, including the
prompt’s `N=5` result of 1. Counterfactual sensitivity was also present:
omitting the second class first fails at `N=4`, and replacing `(N+1)//3` by
`N//3` first fails at `N=5`. These tests support relevance and sensitivity;
the classification itself follows from the rules’ definitional role.

## Immutable hashes

Fresh hashing reproduced the signed inputs:

| Artifact | Observed SHA-256 |
|---|---|
| Signed resolution | `dc6f1c5bb0b8e2b8101d780af19b22c3c846d01f208e71252498da3210e924c0` |
| Stage 1 workspace, pipeline tree hash | `bc9e219af0d5c41f16de070cfc336c56298f6b4d3878fee3950176add79e79c5` |
| Stage 1 workspace, exporter tree hash | `da89912d586b776cbb2196fa74ee5582bee20e5284cf7480e3d45ff92470c64b` |
| Selected Stage 2 audit | `1a6649911bb674941f93bced6a32403a6d514c2c8dbd357bec2b3f8f8f3ed34d` |
| Stage 3 manifest | `2d93d25d0a99001009348be48a9d1990693dfa42d79947c8d537b353814c96ce` |
| Selected Stage 4 generation | `a116e6739aa048076c83569833bd0e3a34ac731a1e6b82df9a91c4716080518b` |
| Generated project | `ad81bd030c8de81d06b70eba0b9be63fc4f0dda6f5aeb96fe33ac062c7e7710a` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `37709b65f1949970cd2161162159b77068efd052e966c0ffdd25d2f08878691e` |

The selected Stage 2 and Stage 4 artifact hashes also equal their selection
records. All nine per-file Stage 1 source hashes equal the signed source map.
The input manifest, generator provenance, export result, recorded preflight,
and audit input all bind to the same Stage 1, Stage 3, and generated-project
hashes.

## Deterministic Stage 4 and target identity

The independently classified domain set is empty, and every deterministic
artifact agrees:

- `input-manifest.json` has `source_rules: []`.
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`.
- The generator and export result both record obligation count zero.
- No source rule is omitted from the obligation map because there is no true
  domain rule. Conversely, there is no extra, duplicate, irrelevant, weakened,
  or vacuous generated conjunct.

The fixed generated target is absence of a target. The generator manifest,
recorded preflight, signed audit input, and independent
`klean_export.target_statement` result are all null. A direct generated-source
scan finds no target declaration or `Proof.final`; the generated root module
only imports the rewrite and empty lemma modules. Thus Stage 4 did not silently
change, duplicate, or weaken a theorem.

I called `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the three required frozen inputs. The first attempt exposed an audit-sandbox
PID/proc mismatch: Lean asked for `/proc/<getpid>/exe`, which returned `ENOENT`
although `/proc/self/exe` was available. A narrow audit-local `LD_PRELOAD`
compatibility shim retries only that failed numeric `/proc/.../exe` read as
`/proc/self/exe`. It does not edit the checker, generated project, producer
sources, manifests, or any frozen input.

With the pinned Lean paths and this sandbox compatibility in place, the same
trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0 and target null;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0 with output hash
  `bdfa3e1e14d23b9d186351af2c99f1a4ba83a83c582686cc0c9c0633f38d13d7`;
- generated tree hash
  `ad81bd030c8de81d06b70eba0b9be63fc4f0dda6f5aeb96fe33ac062c7e7710a`;
- 44 generated executable trust declarations and zero designated sorries.

The fresh return document is exactly equal to both the selected
`preflight.json` and the preflight object in `/audit-input.json`. The complete
build output is shorter than the checker’s retained output limit and is
preserved in the evidence log.

The trusted final mechanical gate also returns `PASS` in
`CLASSIFICATION_ONLY` mode, with null candidate, null target, no diagnostics,
and `used_axioms: []`. Its `semantic_classification: NOT_EVALUATED` is
expected: the mechanical gate checks structure, while the independent
classification judgment is supplied above.

## Stage 5 disposition

Stage 5 proof auditing is not applicable. This is not a proof-bearing
generation: the mode is `CLASSIFICATION_ONLY`, the true domain set and target
parameter list are empty, the generated target is absent, and there is no
candidate or Stage 5 result. Accordingly there is no `Proof.final`, no
candidate definition to operationally bridge, and no final theorem whose axiom
dependencies could be printed. Running candidate `lake clean`, candidate
`lake build`, or `#print axioms Proof.final` would contradict the selected
no-obligation mode. The successful build above is the Stage 4 preflight’s
fresh generated-project build, not a Stage 5 proof build.

## Evidence

Raw commands and results are under `/audit-output/evidence/`, principally:

- [commands.txt](/audit-output/evidence/commands.txt)
- [reconstruct_and_hash_with_tool_lock.log](/audit-output/evidence/reconstruct_and_hash_with_tool_lock.log)
- [producer_hashes.log](/audit-output/evidence/producer_hashes.log)
- [mechanical_checker_hashes.log](/audit-output/evidence/mechanical_checker_hashes.log)
- [preflight_check_generation_compare.log](/audit-output/evidence/preflight_check_generation_compare.log)
- [final_mechanical_gate.log](/audit-output/evidence/final_mechanical_gate.log)
- [preflight_check_generation.log](/audit-output/evidence/preflight_check_generation.log)
- [lean_proc_diagnosis.log](/audit-output/evidence/lean_proc_diagnosis.log)
- [semantic_relevance_check.log](/audit-output/evidence/semantic_relevance_check.log)
- [target_and_candidate_absence.log](/audit-output/evidence/target_and_candidate_absence.log)

The Stage 3 classifications are complete and mathematically appropriate, the
empty domain set is genuine, Stage 4 is hash-bound and deterministic, the null
target is exact, and Stage 5 is correctly absent.

VERDICT: PASS
LEGITIMACY: LEGIT
