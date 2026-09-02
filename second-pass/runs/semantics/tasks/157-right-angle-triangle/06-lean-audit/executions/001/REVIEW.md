# Independent audit: HumanEval 157-right-angle-triangle

## Scope and outcome

I independently audited Stage 3 classification and deterministic Stage 4
generation for condition `semantics` under `SUPPLIED_SEMANTICS`. Both
`AUDIT_MODE` and the signed launcher record select `CLASSIFICATION_ONLY`.
`/candidate` is absent, the launcher records no Lean workspace or invocation,
and Stage 4 defines no target. Stage 5 proof checks are therefore not
applicable.

I treated the mounted workspaces, manifests, logs, comments, rationales, and
prior verdicts only as untrusted evidence. The conclusions below come from a
fresh trusted inventory reconstruction, direct source and operational-semantics
review, independent hash/bijection checks, and a fresh trusted Stage 4
preflight.

## Generation producer identity

Before judging Stage 4, I hashed the two mounted generation-time producer
sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Each hash exactly matches both the protected producer-source manifest and
`generator-manifest.json`. The immutable image identity is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in those manifests, and the image digest encoded in the launcher-recorded
producer-source path is the same. The full mounted producer-source tree hash,
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
also matches `/audit-input.json`. There is no producer-source infrastructure
error.

## Independent rule inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` implementation, I
reconstructed the complete local verification-module closure of the frozen
`verification.k`. The closure contains only module `VERIFICATION` and exactly
these three rules, in source order:

| Order | Frozen span | `source_rule_id` / normalized SHA-256 | Independent classification |
|---:|---:|---|---|
| 1 | 10–41 | `rule-772ba268f1a7b7e7a2809c0fff0eb1708b462640adeb23380c1b0a26bec9aac8` | `DEFINITION` |
| 2 | 44–45 | `rule-dc3194c482c9cf0dd5964c66ef7d6b69a6990a004fe770631b2bc9319d9e96c9` | `DEFINITION` |
| 3 | 49–50 | `rule-897fe19e8f6cd251ddc38df1351b19993ef9ad82b91c59f12bfd525e18172ca7` | `OPERATIONAL_RULE` |

For each entry, the trusted reconstruction's module, start/end span, empty
attribute list, normalized source text, normalized source hash, and derived
`source_rule_id` exactly match the protected Stage 3 record. The frozen
`verification.k` hash is
`de1299aaa98dfbd94a3962585cf2ae1def8ec318d33d3b11973237ce29443504`.
The canonical whole-inventory hash independently recomputes to
`e78aedc88cdec6af90737209a923a8cabf29e903dd23ecaf91dff2b12a19fe27`.

The comparison is bijective and order-sensitive: there are three reconstructed
rules and three distinct Stage 3 identities, with no omission, extra entry,
duplicate, reordered identity, changed span, or changed hash.

## Independent classification judgment

The first rule expands the nullary named proof term
`#rightAngleTriangleBody` into the exact statement AST translated from
`solution.py`: reject a non-positive `a`, `b`, or `c`; test the three possible
Pythagorean equalities; otherwise return false. It states no independent
algebraic fact and is an exact named-term definition, so `DEFINITION` is
correct.

The second rule defines `#rightAngleTriangleClosure` as
`closureVal(("a", "b", "c"), #rightAngleTriangleBody, 0)`. Its parameter
order, exact body term, and module environment agree with the supplied
function semantics, where a `FuncDef` installs precisely such a closure.
This is a named proof-term definition, not a fact about right triangles, so
`DEFINITION` is correct.

The third rule rewrites
`#runRightAngleTriangle(A, B, C)` to the ordinary semantic
`Call(#rightAngleTriangleClosure, A, B, C)`. The supplied semantics then
evaluates the callee and arguments, dispatches `closureVal`, binds all three
parameters, evaluates `If`, comparison, multiplication, addition, and return
normally. The rule neither asserts an output nor bypasses execution. It is an
ordinary execution/observation harness, so `OPERATIONAL_RULE` is correct.

There are no `simplification` attributes, no `DOMAIN_LEMMA` entries, and no
`PROVED_DERIVED_LEMMA` entries. In particular, none of the three rules is a
Pythagorean identity or other mathematical shortcut disguised as a definition
or operational rule. Stage 1's script invokes its claims with these rules
already present and contains no prove-first/use-later derived-lemma sequence;
the protected classification also claims no such sequence. The independently
classified true domain-lemma set is genuinely empty.

## Deterministic Stage 4 integrity

I independently recomputed every launcher-recorded mounted artifact hash:

- full Stage 1 tree:
  `35a4c543203ed2278ad61ba5188a1776717fae9a29ffa3634320e3c17a67363a`;
- deterministic Stage 1 export:
  `240503df89cd9f70b00d5e55cab5b9941cd82a2f99da57df9beec61f2c5fa3cd`;
- selected Stage 2 tree:
  `a5adeb6f4416c157b9010cbf0dc2442f4e9100a2efcac5409bfcd24fd929190b`;
- protected Stage 3 file:
  `4b620b4ec6cc62134da527fc28faa698a4b2bc6a50e21315a0c84e7f6dcde3d1`;
- selected Stage 4 tree:
  `4a6b8981c83264c0a74df61841600334e15d9869460a236a36838205a60c6f97`;
- generated Lean project tree:
  `4c8bef5c94c84b9c7bbd7551af9b31fa78c555ef4e565f54d9d95ad8dcb73656`.

The complete per-file Stage 1 source-hash map also matches the launcher record.
The generator manifest binds the same Stage 1 export, Stage 3 file, inventory,
producer image, and locked K/Lean toolchain.

Stage 4's classification partitions exactly reproduce the three independently
audited entries. Its domain-rule sequence is `[]`; its obligation sequence is
`[]`; `trust_parameters` is `[]`; the obligation count is zero; and the
obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
Thus the ordered source-rule/obligation bijection is exactly the empty
bijection, with no omission or duplicate. Because the mathematically correct
domain set is empty, this is not a weakened export. There are no obligations
or conjuncts that could be irrelevant or vacuous.

The generator manifest target, generated obligation-map target, fresh
preflight target, and launcher-recorded target are all exactly `null`. Direct
inspection confirms that the generated `Lemmas` namespace is empty and no
generated target theorem exists. The fixed target has therefore not been
changed or replaced; the correct zero-obligation result has no target at all.

## Fresh trusted preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
classification, selected Stage 4 generation, and the trusted toolchain lock.
It made its fresh project copy and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- designated sorry count `0`;
- target `null`;
- `lake clean` exit code `0`;
- `lake build` exit code `0`, ending with “Build completed successfully.”

The entire returned object is exactly equal to both the selected
`preflight.json` and `/audit-input.json`'s recorded Stage 4 preflight,
including command-output hashes.

The first attempt exposed an audit-container compatibility issue: Lean 4.22
requests `/proc/<getpid()>/exe`, but this PID namespace exposes only
`/proc/self/exe`. I diagnosed this with a standalone libuv probe and preserved
all failed output. The successful rerun used a source-recorded, narrowly scoped
`readlink` interposer that redirects only that exact same-process executable
lookup to `/proc/self/exe`; it leaves mounted evidence, producer sources,
trusted Python tooling, and Lean binaries unchanged. A separate clean/build
validation succeeded before the required rerun. This is an audit-runtime
compatibility measure, not a modification of any audited artifact, and the
fresh result's exact equality to the generation-time record provides an
additional consistency check.

## Stage 5

Stage 5 is not selected. There is no generated target, no candidate,
no `Proof.final`, no target parameter, and no Lean invocation or result in
the launcher record. Consequently the proof-mode candidate copy/build,
`#print axioms Proof.final`, candidate trust-escape scan, proof-identity check,
and operational-bridge parameter audit do not apply. This also satisfies the
zero-domain requirement that `KLEAN_NO_OBLIGATIONS` have neither a generated
target nor a Stage 5 proof candidate.

## Evidence

Raw command results and exact checker output are under `evidence/`. The main
index is `evidence/COMMANDS.md`; the decisive records are:

- `01-producer-hashes-and-manifests.txt`;
- `04-reconstructed-rule-inventory.json.txt`;
- `05-stage1-source-and-stage3.txt`;
- `07-independent-integrity-checks.txt` and its checker source;
- `09-focused-operational-crosswalk.txt`;
- `26b-fresh-check-generation-pass.txt`;
- `27-generated-source-absence-checks.txt`;
- `28-preflight-reconciliation.txt`.

No mismatch, unaccounted rule, misclassification, weakened obligation set,
target substitution, or proof/trust escape was found.

VERDICT: PASS
LEGITIMACY: LEGIT
