# Independent audit: `156-int-to-mini-roman`

## Result and scope

This audit independently evaluated the protected Stage 3 classification and
the selected deterministic Stage 4 generation for condition `bare` and
semantics mode `GENERATED_SEMANTICS`.

`AUDIT_MODE` and `/audit-input.json` both record `CLASSIFICATION_ONLY`. The
selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent.
Consequently, the Stage 5 proof, `Proof.final`, axiom accounting, and
`target.parameters` operational-bridge checks do not exist and are not
applicable.

I treated the prior Stage 2 review, all mounted logs, rationales, and prior
verdicts as untrusted evidence. In particular, the prior Stage 2 PASS was not
used to select this result.

## Input and tool authentication

The Stage 6 audit-input envelope recomputes to its recorded digest:

`1f5e9c7d41a3a494f7b088bb946aaade4644bdc67b1d10bbc376693b41f8157d`.

The recorded mechanical-checker lock hashes to
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`.
Every one of its eight `/reference/tools` file hashes matches, including the
trusted rule inventory, Klean preflight, final gate, and resolution contract.

All launcher-bound hashes recomputed exactly:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace artifact tree | `88d32ed87cae8c8a0b2c01040bf93bb7b49ff1e25839af5d8687197ef49d1e43` |
| Frozen Stage 1 export tree | `43fc3caea839135ebaefe591f8cc08c1d74feb534a5c2b017d8cffb7dcf51c12` |
| Stage 3 discovery manifest | `1421f4dba177bb737ae7058513abbe96a7d5a15272d699d9cb5edfbace94137c` |
| Selected Stage 2 audit tree | `2d278628e6bf90546c38ffed3f73f7d0752acc7cb9a5b534e5f9ae8bcaa234a2` |
| Selected Stage 4 generation tree | `14aa04fa8b5f27a4cfec6fbc3f7a3f06e16a1eba78615aeef32138d7e4d53cad` |
| Generation-time producer bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project | `250a264ecd375328b3a24526d7b9b690700f157bf4884f4f1de1f72f199dc3b1` |

The complete set of 232 Stage 1 regular-file hashes also matches
`audit-input.json` bijectively.

### Generation-time producer authentication

I hashed the required producers before judging Stage 4:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

These values match both `source-manifest.json` and
`generator-manifest.json`. The immutable generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator provenance, and its digest is the
generation-producer bundle key recorded in `/audit-input.json`. The bundle
contains exactly the two producers and `source-manifest.json`. There is no
producer-source mismatch or missing source, so no infrastructure
`AUDIT_ERROR` applies.

## Stage 3 inventory reconstruction

I called the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`, then independently recomputed every returned source
span and normalized hash from the frozen bytes.

The selected main module is `ROMAN-VERIFICATION`; its local module closure in
`verification.k` is exactly that module. The reconstructed inventory contains
two rules, in source order:

1. Lines 7–42:
   `rule-00b13407b775d8f7c54a7237162b4d7ce28eaf42ee68f04dbd2bceab22d62733`.
   The recomputed normalized source hash is
   `00b13407b775d8f7c54a7237162b4d7ce28eaf42ee68f04dbd2bceab22d62733`.

2. Lines 45–61:
   `rule-54c74217ad8efd4f90535b99e49caf9d7c1180c37fabc1b60442f6ab239a9b13`.
   The recomputed normalized source hash is
   `54c74217ad8efd4f90535b99e49caf9d7c1180c37fabc1b60442f6ab239a9b13`.

For both entries, the exact extracted span matches the frozen source, the
normalized hash matches, and `source_rule_id` is exactly `rule-` followed by
that hash. The whole reconstructed inventory hash is
`15b0fdae4ecec18050cdc11d01d501b659713a2e964097a347e97dce027fe12e`.

The protected Stage 3 manifest has exactly the same two unique identities in
the same order and the same inventory hash. There are no omissions,
duplicates, extra entries, reordered identities, changed hashes, or
unaccounted classifications.

## Independent classification and operational judgment

### `romanProgram` rule: `DEFINITION`

The production declares the named ground term `romanProgram` as a program
macro. Its sole rule expands that name to the complete translated Mini-Python
AST. I compared the AST with both the frozen source solution and
`solution.mpy`: it contains the same function, parameter, four tuple
assignments, four indices, nested string concatenations, and return.

This rule has no operational cells, state transition, guard, or mathematical
proposition. It names a fixed proof/program term. Under `semantic.k`, ordinary
execution starts after expansion: the module rule binds `number` to the input,
the assignment rules populate the environment, and the return/evaluation
rules compute the result. The macro neither bypasses nor summarizes that
execution.

It is therefore a `DEFINITION`, not an `OPERATIONAL_RULE`, `DOMAIN_LEMMA`, or
`PROVED_DERIVED_LEMMA`.

### `miniRoman(N)` rule: `DEFINITION`

The production declares `miniRoman : Int -> String` as a K function. Its rule
defines that named summary as four decimal-place `tupleAt` lookups joined by
`+String`: thousands, hundreds, tens, then ones.

The operational program does not invoke `miniRoman`. It evaluates the four
corresponding tuple subscripts through the fixed rules for name lookup,
integer division/remainder, tuple indexing, and left-to-right string
concatenation. Only the postcondition mentions `miniRoman`, so this equation
names the mathematical result to which ordinary execution is compared; it
does not preempt source execution or create an operational bridge.

The definition is relevant and faithful to the source program. On the formal
domain `1 <= N <= 1000`, the thousands index is 0 or 1, and the hundreds,
tens, and ones indices are each 0 through 9. Thus every lookup is within its
corresponding tuple, including the `N = 1000` boundary. The equation is
non-recursive and expands directly to the same digit decomposition used by
the source.

It is therefore a `DEFINITION`, not a domain fact, ordinary operational rule,
or separately proved derived lemma.

Neither inventory entry has a `simplification` attribute. The `tupleAt`
equations in the frozen generated semantics are outside the local
`verification.k` inventory; operationally, they are definitional base and
recurrence equations for tuple lookup in any event. No simplification rule is
misclassified as operational or derived.

There are no `PROVED_DERIVED_LEMMA` claims, so no rule incorrectly relies on a
purported prove-first/use-later history. There are no true domain lemmas:
both inventory entries are definitions, and no mathematical fact about the
program or postcondition remains to be exported as a Lean obligation.

## Stage 4 deterministic generation and obligation bijection

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required mounted inputs plus the pinned toolchain lock. The returned
result is:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: `null`
- generated tree:
  `250a264ecd375328b3a24526d7b9b690700f157bf4884f4f1de1f72f199dc3b1`
- `lake clean`: exit 0
- `lake build`: exit 0, all nine generated-project steps completed
- designated `sorry` count: 0

The audit launcher has a PID-namespace defect affecting Lean's application
path discovery: Lean initially attempted `readlink("/proc/3/exe")`, which is
absent in the outer `/proc` mount. I preserved the failed default run and the
exact trace. For the rerun I used a narrow `LD_PRELOAD` shim that only maps
`/proc/<decimal-pid>/exe` to `/proc/self/exe`; it does not alter Lean inputs,
generated sources, statements, or checking. Lean then reported the pinned
4.22.0 commit and the required preflight passed. The trusted final mechanical
gate also passed under the same namespace-only workaround.

The rerun build-output hash differs from the stored preflight's diagnostic
hash only because independent Lean modules finished in a different parallel
order. The stored diagnostic's decoded output itself recomputes exactly to
its recorded hash. All content/tree hashes are identical before and after
the reruns.

The independent mathematical domain set is empty. It matches each generation
layer exactly:

- `input-manifest.json` `source_rules`: empty
- `obligation-map.json` `source_rules`: empty
- `obligation-map.json` `obligations`: empty
- generator and export obligation counts: zero
- obligation-map file hash:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`

The two reconstructed rule IDs instead appear exactly once, in order, in the
generated input manifest's `definitions` array. Hence the source-rule /
obligation mapping is an exact empty bijection over the independently
classified domain set. There are no omitted, duplicated, irrelevant,
weakened, or vacuous obligations.

Target identity is also exact: `generator-manifest.json`, the stored
preflight, `/audit-input.json`, and an independent
`klean_export.target_statement` parse all return `null`. An independent scan
found no generated `theorem` or `lemma` declaration. There is therefore no
target statement that could have been changed, weakened, duplicated, or made
vacuous.

## Stage 5 applicability and trust

Stage 5 must not exist for a genuinely empty domain set. It does not:
`/candidate` is absent, both Lean workspace/invocation hashes are null, and
the selected mode is `CLASSIFICATION_ONLY`.

There is no `Proof.final`, generated target, target parameter, or proof axiom
dependency to inspect. Running `#print axioms Proof.final` or candidate
operational-bridge tests would fabricate a proof artifact contrary to the
recorded mode. The generated Base project's 46 trust declarations were
structurally reconciled with `trust-inventory.json` by preflight; it contains
zero proof holes and no proposition-level target proof.

## Evidence

Raw commands and complete results are under `evidence/`. The principal files
are:

- `03-generation-producer-hashes.txt`
- `04-reconstructed-rule-inventory.txt`
- `05-verification-and-spec-source.txt`
- `06-program-and-generated-semantics.txt`
- `07-rerun-check-generation.txt` (the initial launcher-environment failure)
- `10-lean-pid-namespace-shim-test.txt`
- `11-rerun-check-generation-with-pid-shim.txt`
- `12-independent-stage4-bindings.txt`
- `13-trusted-final-mechanical-gate.txt`
- `14-lean-app-path-failure-trace.txt`
- `lean-proc-self-shim.c`

The independent classification is mathematically correct, the true domain
set is genuinely empty, deterministic Stage 4 provenance and structure are
intact, the null target is fixed, and the absence of Stage 5 is required.

VERDICT: PASS
LEGITIMACY: LEGIT
