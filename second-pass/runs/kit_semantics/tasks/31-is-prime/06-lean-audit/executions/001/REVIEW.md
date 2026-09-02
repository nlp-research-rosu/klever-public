# Independent audit: `31-is-prime`, `kit-semantics`

## Scope and result

The launcher selected `AUDIT_MODE=CLASSIFICATION_ONLY` and
`semantics_mode=SUPPLIED_SEMANTICS`. Stage 4 is recorded as
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, and the Stage 5 paths and hashes
in `/audit-input.json` are null. I therefore audited Stage 3 classification and
Stage 4 generation. Stage 5 proof checks are correctly inapplicable.

I treated the mounted source, comments, old logs, and old review as untrusted
evidence. The decisions below come from a fresh rule reconstruction, direct
source/semantics inspection, fresh hash checks, and a rerun of the trusted
preflight. Commands, helper sources, and raw results are in `evidence/`; the
exact command index is `evidence/COMMANDS.md`.

## Producer-source infrastructure gate

I hashed the mounted generation-time sources before accepting any Stage 4
result:

- `klean_export.py`:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

Both hashes match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The image ID in both manifests is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`,
which is also the immutable producer-bundle identity encoded in the path in
`/audit-input.json`. The complete three-file producer bundle hashes to
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
exactly the audit-input value. There are no extra bundle entries. This gate
passes; there is no producer-source `AUDIT_ERROR`.

Evidence: `evidence/02_producer_provenance.log`.

## Fresh verification-module inventory

Using the trusted `tools.k_rule_inventory.inventory_verification` code, I
reconstructed the local closure selected by the final `kompile verification.k
--main-module VERIFICATION` command. The closure contains the one locally
defined module `VERIFICATION`; `MPY` is supplied by the required semantics
files rather than another module declared in `verification.k`.

The reconstruction found exactly six rules, in source order:

| Span | Normalized SHA-256 / `source_rule_id` suffix | Fresh class |
|---|---|---|
| 12–13 | `56a2e70b2b9a6897534484145ed3c22f2e76bcf2e474dc68eef9f37172a8d12a` | `DEFINITION` |
| 15–16 | `c9098f115d5ab2018046eb5b7aa8258fc144eaf87ed620450558b6738876fc2a` | `DEFINITION` |
| 18–20 | `f25721ae7af46a0d407f68b99044bcc092e0886933e95e182b7f354dd372cc6f` | `DEFINITION` |
| 22–24 | `9dfa4d77d4e72a22bb3e22d40e29debbf97d343991879dc70b5d3d14769f44b6` | `DEFINITION` |
| 26–27 | `2feaa748adba85dc4184b9bd769705f17045eecdf978f110190f1bf45f6d0c6d` | `DEFINITION` |
| 29–30 | `85efba1c2354ec176471d3fd15fe706012a5e3145f8eedc205b93748cdddfdff` | `DEFINITION` |

For every entry I separately sliced the recorded physical source span, checked
it exactly equals the inventory text, normalized whitespace, recomputed the
rule hash, and checked that `source_rule_id` is exactly `rule-` followed by that
hash. The ordered whole-inventory hash recomputes to
`c0628bc9c6a3e07fd361ebae705579a2a3cf61c51cc51b40398ddd545b5fe37b`.

The protected Stage 3 file has exactly those six unique identities in exactly
that order and the same whole-inventory hash. There are no omissions, extras,
duplicates, reordered identities, span changes, or hash changes.

Evidence: `evidence/01_inventory_reconstruction.log`.

## Independent classification judgment

All six rules are genuine definitions, not disguised domain lemmas:

1. `primeScan(_N,D) => false` for `D < 2` is an explicit totalization case for
   the named summary outside the proof-relevant `D >= 2` domain.
2. `primeScan(N,D) => true` for `D >= 2` and `D >= N` is the empty-interval base
   equation.
3. The `pyMod(N,D) == 0` case is the divisor-found defining branch.
4. The `pyMod(N,D) =/= 0` case is the recurrence at `D + 1`.
5. `primeResult(N) => false` for `N < 2` is the first result-summary case.
6. `primeResult(N) => primeScan(N,2)` for `N >= 2` is definitional composition.

These rules rewrite only the declared function symbols `primeScan` and
`primeResult`; none matches a `<k>` cell, execution configuration, or program
observation. Thus none is an `OPERATIONAL_RULE`. None is presented as a
`PROVED_DERIVED_LEMMA`, so no unsupported prior-proof claim is being credited.
They do not assert a separate theorem such as primality, membership, or an
arithmetic shortcut; they give exhaustive equations for the named summaries.

The guards are exhaustive and pairwise disjoint over their declared integer
arguments: `D < 2` versus `D >= 2`; then `D >= N` versus `D < N`; then remainder
zero versus nonzero. On the recursive branch, `D < N` and replacement by
`D + 1` strictly decrease the natural measure `N-D`. The two `primeResult`
guards similarly partition all integers. In the supplied operational
semantics, integer `BinOp("%",...)` dispatches to the same `pyMod` symbol used
by the definition, and integer comparisons dispatch to the same K integer
predicates. The recurrence consequently mirrors the source loop from divisor
2 through `N-1`, while `primeResult` mirrors the source's `N < 2` branch.

As a finite operational sanity witness—not as a substitute for the above
classification argument—I freshly ran the source body with the supplied K
runtime for inputs `[-7,0,1,2,3,4,5,9,25,49,97]`. It terminated with results
`[false,false,false,true,true,false,true,false,false,false,true]` and clean
control/exception cells. Evidence:
`evidence/06_operational_witnesses.log`.

No reconstructed rule has a `simplification` attribute. The simplification
policy is therefore satisfied without exception. The independent true
`DOMAIN_LEMMA` set is genuinely empty. The detailed fresh rationales are in
`evidence/independent_classification.json` and agree with the protected
classifications by identity and order.

## Stage 4 preflight and recorded hashes

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the required Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and trusted toolchain lock.

The first invocation could not start `lake clean`: this sandbox hides
`/proc/<pid>/exe`, which Lean uses to locate its installation, although it
exposes the equivalent `/proc/self/exe`. A diagnostic readlink trace showed the
failing numeric proc path. I compiled the evidence-local narrow shim in
`evidence/proc_self_exe_shim.c`, which changes only numeric
`/proc/<digits>/exe` reads to `/proc/self/exe`, and reran the exact trusted
checker with that shim preloaded. This restored the pinned Lean 4.22.0 commit
`ba2cbbf...`; it does not change any source, generated file, build command, or
checker decision. Both the failed attempt and the diagnosis are preserved in
`evidence/03_preflight_rerun.log` and
`evidence/07_lean_environment_diagnosis.log`.

The successful rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, successful build of all generated modules;
- obligation count 0;
- target null;
- designated sorry count 0;
- 43 generated executable trust declarations, exactly accounted for by the
  generation trust inventory and with no proposition trust.

The build-output hash is
`5175f8078437554fd1083c0ec997bd6c47e29b07d6d5adcab8ab611674f48b57`,
matching the selected preflight's recorded build output. Evidence:
`evidence/04_preflight_rerun_with_proc_shim.log`.

I also independently recomputed and matched these audit-input/manifests values:

- Stage 1 pipeline tree:
  `367802fc2eab2dfb3a657c257765a7646b799d0a403f9d8db2f71b9e45a5a229`;
- Stage 1 export tree:
  `f906d821a76985757fb69cbdb407beb98da0389ab139262c41f043eeb9e242f8`;
- all 783 individual Stage 1 source-file hashes;
- selected Stage 2 tree:
  `04eb511cd466095881af87e45e45b5df0203a02a3c46e0bfaacfe29384ec37e8`;
- Stage 3 file:
  `61e27bb736e271b8d017590aeb07725171e6774212051002dead045d41e7f5d5`;
- selected Stage 4 tree:
  `002e342eafeee67c076f9562ce42cfb058a5f6729852f153508f1d6742929d29`;
- generated project tree:
  `54e8656ba2a8ad41f20c92b3a8e5a9e5dc2245cc2aaefc1644fec20a472d9802`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `38a0688456f75d4eadc6e5fd2172d6e9e1559cc8f1944bc6f232ce3cc1e3c6b9`.

Evidence: `evidence/05_stage4_integrity.log`.

## Obligation bijection and fixed target

The independently classified domain set is `[]`. It matches, exactly and in
order, all of the following:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`.

The generator manifest, export result, selected preflight, and fresh preflight
all record obligation count zero. This is an empty conjunction represented by
the absence of a target, not a generated `True` or another vacuous conjunct.
The trusted target extractor returns null, the expected target definition is
null, and the generator manifest, preflight, and audit input all bind the fixed
target to null. There are therefore no weakened, irrelevant, duplicated, or
omitted obligations and no target statement that could have changed.

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the correct
Stage 4 status. `/candidate` does not exist, so there is no forbidden Stage 5
proof candidate. Lean proof identity, candidate shadowing, `#print axioms
Proof.final`, and parameter operational-bridge checks are not applicable in
this launcher mode.

## Final judgment

The protected Stage 3 classification is complete and mathematically correct;
producer provenance is intact; Stage 4 deterministically preserves the empty
domain set, generates no target, and passes the trusted clean-build preflight;
all provenance and tree bindings recompute exactly. The sandbox proc-path issue
was diagnosed and corrected without modifying audited inputs and is not an
artifact concern.

VERDICT: PASS
LEGITIMACY: LEGIT
