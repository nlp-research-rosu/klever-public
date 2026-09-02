# Independent audit: HumanEval 24-largest-divisor

## Scope and outcome

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. I treated the
Stage 1 workspace, Stage 2 review, Stage 3 discovery, Stage 4 generation, and
their comments and logs as untrusted evidence. I did not use the earlier Stage
2 PASS or Stage 3 rationales to decide the classification.

The Stage 3 classification is complete and correct. Both local verification
rules are genuine definitions of a descending-search summary. The independently
determined domain-lemma set is empty. The selected Stage 4
`KLEAN_NO_OBLIGATIONS` result therefore has the required empty
source-rule/obligation bijection, no generated target, and no Stage 5 candidate.

## Launcher and mounted-input integrity

`AUDIT_MODE` and `/audit-input.json` both select `CLASSIFICATION_ONLY`.
The canonical launcher resolution hash recomputes to
`feadf9f136728a1d49f8be0b9e0bae73da2fd74c914df5f1fd2dc987e812df3a`.
The trusted tree/file hash routines reproduced every recorded mounted-input
hash:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `553cb747ae25e84a0f158de85a6460c20dac1dca647d7b44346e3a9d61f94573` |
| Stage 1 deterministic export tree | `6fc6003a7a51374958037bfa910ea119dacceff71c6381b44ed33abf3bf7d6aa` |
| Stage 2 selected audit tree | `f6a47fa0368a8564f074a27cd5ddfa1c35f82a2a5b54ec6636105325ce01e985` |
| Stage 3 discovery file | `c603f16847f3c8a10baa75615fb064a4cc76f5246884040ef7fe387a62743b0b` |
| Stage 4 selected generation tree | `71ce1e1dab2dd289a6a357b04557c85f6877d0150c908d2d883fd6502a6cba69` |
| Generation producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Generated Lean project | `4b0d09093c734ee5dc8d4fd0108880d27e226610404729b6954390f45be44015` |

I also recomputed the complete 769-entry Stage 1 per-file hash map; its file
set and every digest equal `resolution.stage1_source_hashes`. Evidence:
`evidence/00-launcher-environment.log`,
`evidence/03-mounted-tree-hashes.log`, and
`evidence/28-independent-stage4-verification.log`.

## Mandatory Stage 4 producer provenance gate

This gate passed before I judged the generated result.

| Producer | Recomputed hash | Recorded hash |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same in the source manifest and generator manifest |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same in the source manifest and generator manifest |

The source manifest and generator manifest both record immutable generator
image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
That digest is also the basename of the launcher-resolved producer bundle in
`/audit-input.json`. The producer bundle contains exactly the two producers and
its source manifest. Evidence: `evidence/01-producer-provenance.log` and
`evidence/02-producer-cross-check.log`.

## Independent rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`. The selected local verification module is `VERIFICATION`;
its local closure contains only `VERIFICATION`. The frozen
`verification.k` hash is
`0ec338251b272f778a945639d5bface7cbc4a1ae3bfd36870721895d8cf0c18b`.

The canonical inventory is:

| Order | Source span | Normalized SHA-256 / source rule ID | Attributes |
|---|---|---|---|
| 1 | `VERIFICATION:10-12` | `0f02393212bfcf7e7c8810a806f9829aa2bbf9b5bd9795c9a7b5db26160d7995` / `rule-0f02393212bfcf7e7c8810a806f9829aa2bbf9b5bd9795c9a7b5db26160d7995` | none |
| 2 | `VERIFICATION:14-17` | `99644c7600e08ea07b0c26314084adf2ab5eb468a6b1eb4aadd857b2f427b14a` / `rule-99644c7600e08ea07b0c26314084adf2ab5eb468a6b1eb4aadd857b2f427b14a` | none |

The whole inventory hash is
`993975976aee2a5aec1109c062dbe6168d9391fcdc989e7a2667ebe9d68d6bb1`.
The protected Stage 3 file has exactly these two IDs once each, in this order,
and the same whole-inventory hash. There are no omitted, duplicated, extra, or
reordered identities. Because `source_rule_id` is `rule-` followed by the
recomputed normalized hash for each entry, changed rule text or a changed
identity would also have been detected.

Evidence: `evidence/05-stage3-discovery-full.log`,
`evidence/06-reconstructed-rule-inventory.log`, and
`evidence/08-stage3-inventory-bijection.log`.

## Independent classification and mathematical judgment

The source program initializes `divisor` to `N - 1`, tests
`N % divisor != 0`, decrements by one while that test is true, and returns the
first divisor found. The frozen K semantics implements the relevant behavior
without a proof-local operational bridge:

- calls resolve the closure, evaluate the integer argument, bind `n`, and
  execute the source body;
- assignment writes the current scope;
- `While` evaluates the comparison and repeats its body exactly when the
  Boolean is truthy;
- integer `%` dispatches to `pyMod`, and integer `!=` dispatches to
  `=/=Int`;
- `Return` records the returned value and pops the exact call frame.

The two inventory entries do not match a `<k>` cell, a source call, or another
operational configuration. They only give equations for the new
`[function]` symbol `largestDivisorAtOrBelow`.

1. Rule 1 says that the summary at `(N,D)` is `D` when `D >= 1` and
   `pyMod(N,D) = 0`. This is the base/value equation for the first divisor
   encountered.
2. Rule 2 says that the summary at `(N,D)` equals the same summary at
   `(N,D-1)` when `D > 1` and `D` is not a divisor. This is the defining
   recurrence for the downward search.

I therefore independently classify both rules as `DEFINITION`. This is based
on their behavior, not their names or the Stage 3 rationales. They are neither
ordinary execution/observation rules nor derived lemmas. They also are not
domain lemmas disguised as definitions: each rule directly defines the value
or recurrence of a newly named summary, as allowed by the classification
contract, rather than asserting an auxiliary property of an already-defined
program result.

On the proof use-domain `N >= 2` and `D >= 1`, the guards are mutually
exclusive where both could syntactically be considered; they cover every
reachable case; the recursive branch strictly decreases the positive `D`; and
the search must reach `D = 1`, where `pyMod(N,1) = 0`. Beginning at
`D = N - 1`, the returned first divisor is exactly the largest divisor smaller
than `N`, matching the HumanEval postcondition. The equations are relevant to
the source program and postcondition.

There are no `simplification` attributes in this inventory, so the
simplification-category restriction is satisfied vacuously. There are no
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA` entries. In
particular, no derived-lemma claim needed a prior bridge-free Stage 1 proof.

As adversarial finite support, an independent implementation agreed with
brute-force largest-proper-divisor enumeration for every `N` from 2 through
1000, including prime, square, composite, and boundary witnesses; the guard
overlap and coverage-gap sets were empty. Counterfactual one-step and
constant-one summaries disagreed on many cases. An independent `krun` of the
frozen operational semantics completed all four supplied assertions
(`15 -> 5`, `7 -> 1`, `100 -> 50`, and `2 -> 1`) with empty computation and
exit code 0. These tests support, but do not replace, the preceding
source-and-semantics argument.

Evidence: `evidence/07-frozen-source-and-spec.log`,
`evidence/10-exact-operational-rules.log`,
`evidence/11-definition-adversarial-checks.log`,
`evidence/29-independent-krun-operational-witnesses.log`, and
`evidence/30-source-contract.log`.

## Stage 4 structural and mathematical audit

The Stage 4 input manifest accounts for both inventory rules as exact
definitions, with their spans, text hashes, IDs, classifications, and
rationales. Its operational-rule and proved-derived-lemma lists are empty. Its
domain `source_rules` list is empty.

The generated `obligation-map.json` contains:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

This is the exact bijection required by the independently empty domain-lemma
set. There is no omitted or duplicated source rule, no weakened or irrelevant
obligation, no conjunct (vacuous or otherwise), and no trust parameter to
bridge. The generator manifest, stored preflight, launcher input, and an
independent call to `klean_export.target_statement` all record `target: null`.
A source scan confirms that the generated `Lemmas.lean` namespace is empty and
there is no generated target theorem.

All Stage 4 sidecar bindings recompute correctly:

- the input manifest binds the frozen Stage 1 tree, Stage 3 file,
  `verification.k`, inventory, and complete classification records;
- the generator manifest binds the producer hashes, generator image, pinned
  toolchain, generated project, obligation map, inventory, Stage 1, and Stage
  3;
- the export result binds the generated project and trust inventory; and
- the selected status, stored preflight, and launcher status all agree on
  `KLEAN_NO_OBLIGATIONS`.

The generated library contains 43 recorded non-propositional trust
declarations and zero proof holes. The preflight independently matched all 43
declarations against `trust-inventory.json`, rejected proposition trust, and
found no `sorry`, `admit`, or `unsafe`. Because there is no target theorem,
none of these declarations is being presented as a proof of a generated
obligation.

Evidence: `evidence/23-stage4-sidecars-full.log`,
`evidence/24-generated-target-and-forbidden-scan.log`, and
`evidence/28-independent-stage4-verification.log`.

## Required preflight rerun and deterministic regeneration

I called `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these three mounted inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`; and
- `/reference/klean-generation`;

using `/reference/klean-toolchain.lock.json`.

The audit sandbox initially exposed a tool-launcher defect: Lean attempted
`readlink("/proc/<namespace-pid>/exe")`, but only `/proc/self/exe` identifies
the process in this environment. The trace records `ENOENT` for that numeric
path. I preserved the failure, the diagnostic source, and a narrow
compatibility shim that changes only those `/proc/.../exe` reads to
`/proc/self/exe`. The shim does not alter the Lean binary, generated project,
candidate data, hash routines, or any mounted input. With it, the pinned
binary reports Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The required preflight then succeeded and returned exactly the stored and
launcher-recorded evidence:

| Check | Result |
|---|---|
| `lake clean` in a fresh temporary project | exit 0, empty output |
| `lake build` in that fresh project | exit 0 |
| Build output | Prelude, Sorts, Inj, Func, Lemmas, Rewrite, and root module built; “Build completed successfully.” |
| Status | `KLEAN_NO_OBLIGATIONS` |
| Obligation count | 0 |
| Target | null |
| Designated sorry count | 0 |
| Trust declaration count | 43 |

The exact successful returned JSON is in
`evidence/22-rerun-check-generation-success.log`. The initial failure and
sandbox diagnosis are in `evidence/12-rerun-check-generation.log`,
`evidence/31-lean-proc-namespace-diagnosis.log`, and
`evidence/32-lean-shim-source-and-smoke.log`; the shim source is
`evidence/lean_proc_self.c`.

As an additional determinism check, I placed the hash-verified generation-time
producer files in a scratch `tools/` layout and reran the exact exporter with
the same frozen input, discovery, problem ID, generator image ID, and toolchain
lock. It reproduced:

- the generated project byte-for-byte, including generated-tree hash
  `4b0d09093c734ee5dc8d4fd0108880d27e226610404729b6954390f45be44015`;
- `generator-manifest.json` byte-for-byte;
- `trust-inventory.json` byte-for-byte; and
- `export-result.json` byte-for-byte.

The rerun input manifest has identical semantic fields and the identical
required-file closure. Its only byte difference is the expected absolute
workspace prefix: `/frozen-k` in the generation image versus
`/reference/k-proof` in this audit mount. No generated Lean source, target,
obligation, trust declaration, or hash-bearing semantic field changed.
Evidence: `evidence/26-exact-stage4-regeneration.log`,
`evidence/27-stage4-regeneration-identity.log`, and
`evidence/28-independent-stage4-verification.log`.

## Stage 5 applicability

Stage 5 is correctly absent. `/candidate` does not exist; the launcher records
no Lean workspace, no Lean invocation, no Stage 5 result, and no target. Under
the required no-obligation policy, creating a candidate or a `Proof.final`
would itself be inconsistent. Therefore a Base copy, candidate `lake clean`
and `lake build`, `#print axioms Proof.final`, candidate target-shadowing
checks, and parameter operational-bridge checks are not applicable in this
`CLASSIFICATION_ONLY` audit.

## Final judgment

The protected Stage 3 document is a complete, ordered, hash-identical
classification of the frozen local rule inventory, and both classifications
survive independent semantic review. The genuine domain-lemma set is empty.
Stage 4 faithfully preserves that empty set as an empty obligation map and no
target, with verified producer provenance, exact manifest bindings, successful
fresh preflight build, and deterministic regenerated output. The required
absence of Stage 5 is satisfied.

VERDICT: PASS
LEGITIMACY: LEGIT
