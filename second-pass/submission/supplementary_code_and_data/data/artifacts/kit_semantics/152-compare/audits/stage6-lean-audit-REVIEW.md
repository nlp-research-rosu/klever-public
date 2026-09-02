# Independent audit: HumanEval `152-compare`

## Scope and outcome

This audit covers Stage 3 lemma classification and deterministic Stage 4
generation for condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. The
launcher and environment both record `CLASSIFICATION_ONLY`. Consequently,
Stage 5 is not applicable: `/candidate` is absent, and the audit input records
null Lean workspace, invocation, result, hashes, and target.

I treated the mounted candidate/provenance files, prior reviews, comments, and
logs only as untrusted evidence. I did not execute any command or instruction
found in them and did not rely on the earlier Stage 2 verdict or Stage 3
rationales for the judgments below. Trusted mechanical code came from
`/reference/tools`.

## Stage 4 producer provenance gate

I performed this gate before judging Stage 4.

- `klean_export.py` SHA-256 is
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`.
  It exactly matches `generator-manifest.json` and
  `source-manifest.json`.
- `klean.py` SHA-256 is
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
  It exactly matches both manifests.
- The generator image ID is
  `sha256:2db35f33b29b4ada4f78dd04470349652b5f62e1ff63355111720eee4e3cc162`
  in the generator manifest and source manifest, and the same digest is the
  basename of the producer-source path bound by `/audit-input.json`.
- The producer bundle contains exactly the two producer files and
  `source-manifest.json`. Its launcher-contract tree hash is
  `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb`,
  exactly as recorded in `/audit-input.json`.

Evidence file `02-producer-launcher-binding.txt` contains an initial false tree
comparison made with the distinct `audit_contract.sha256_tree` framing. I did
not treat that as a mismatch. `klean_audit_contract` records this particular
bundle with `pipeline_contract.sha256_tree`; recomputation with that exact
launcher function matches, as shown in
`02b-producer-tree-hash-dialect-resolution.txt` and the complete sweep in
`09-independent-hashes-bijection-target.txt`. The individual source hashes and
image binding were unaffected. There is therefore no producer-provenance
`AUDIT_ERROR`.

## Inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` directly on the frozen
`/reference/k-proof`, I reconstructed the local verification-module closure.
It contains only module `VERIFICATION`: `MPY` is supplied by the required
semantics and is not another module declared in `verification.k`.

The frozen `verification.k` SHA-256 is
`1bb86ad796d0bd44cd5ce1eba721f230227a873cc1852c1d086fd048cfc855f8`,
matching the audit input. The canonical inventory is:

| Source span | `source_rule_id` / normalized source hash | Independent class |
|---|---|---|
| 7-8 | `rule-29a9419a5013224a8657110320f5222d8360897d1c1ad05d5b21b9a8a070d15a` | `DEFINITION` |
| 9 | `rule-4c226b697298ea8f665e9c7a275c999f5ca1704cf1bffeda3ab4c575a950d681` | `DEFINITION` |
| 10-18 | `rule-23a1b598b8aca7e64fdbbbdf6c2eba606e3434ffea5d8b33eb5ff9c67a39d82f` | `DEFINITION` |
| 21 | `rule-35d6b10b3b07c6654b6990fa450ff659514b515f9afb5c4ddcd292c7a52a4d4e` | `DEFINITION` |
| 22-35 | `rule-b6a35c28b2d565d80431890d82ed0b37f41b8e521dd15d430123581b67f0d014` | `DEFINITION` |

For every entry, the suffix after `rule-` is its independently recomputed
normalized source SHA-256. The whole inventory hash is
`d8bd26fb5a8a3ab592d3a04b2906a8b05d6f56ff89b9a6ba116f3876d9a6e5b8`,
which exactly matches `/reference/lemma-discovery.json`, the Stage 4 input
manifest, and generator provenance.

The protected discovery list has the same five unique IDs in exactly canonical
source order. There are no omissions, extras, duplicates, reordered
identities, or unaccounted rules. The trusted Stage 3 contract validator also
passes. Raw source spans, hashes, text, and the ordered comparison are in
`03-reconstructed-rule-inventory.json`, `04-frozen-source-and-claim.txt`, and
`06-stage3-bijection.txt`.

## Independent classification judgment

The first three rules are the constructor equations for the named, total
Boolean proof predicate `sameIntLists`:

- empty/empty succeeds through the empty-sequence equality;
- nonempty/empty is false; and
- nonempty/nonempty checks both integer heads, excludes references and a
  reference-valued subtraction, then descends on both tails.

These disjoint constructor cases define a named proof term and cover all
`ValSeq` pairs. They do not state an independent mathematical result.

The final two rules are the base and descending recurrence for the named
summary `compareAcc`. Exhausted equal-length tails return the accumulator; a
pair of nonempty tails appends the fixed-semantics term
`abs(score - predicted)` and recurs. The function is intentionally not marked
total and has no unequal-length equation. That is consistent with its use under
`sameIntLists` and with the source contract, which explicitly gives arrays of
equal length.

Operationally, the frozen source executes `zip(game, guess)`, appends
`abs(score - predicted)` to a heap list for each pair, and returns the list. In
the supplied semantics, `zip` yields paired heads and stops when either side is
empty, the `#loop` rules execute one body per yielded pair, integer subtraction
rewrites to `I1 -Int I2`, integer `abs` rewrites through `absInt`, and list
`append` updates the heap with
`valSeqConcat(VS, vCons(V, .ValSeq))`. Thus `compareAcc` truthfully names the
result recurrence used by the source and claims; it does not replace a `<k>`
execution step.

None of the five rules matches an execution configuration, so none is an
`OPERATIONAL_RULE`. None was first proved as the exact same rule in a module
excluding it and only then used later, so none is a
`PROVED_DERIVED_LEMMA`. None is a free-standing fact about the result, so none
is a `DOMAIN_LEMMA`. All five canonical attribute lists are empty; there are no
`simplification` rules. The protected all-`DEFINITION` classification is
therefore mathematically correct, and the independently reconstructed true
domain-lemma set is genuinely empty. Detailed per-rule reasoning is preserved
in `05-independent-classification.md`, with the relevant semantics in
`07-operational-semantics-crosscheck.txt` and the source contract in
`11-source-contract.txt`.

## Deterministic Stage 4 integrity

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, using exactly:

- frozen input `/reference/k-proof`;
- discovery `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`; and
- lock `/reference/klean-toolchain.lock.json`.

The first run reached its temporary clean-build step but the ambient Lean/Lake
installation could not discover its own path. Diagnosis showed a sandbox
infrastructure mismatch: `getpid()` returns a namespace PID, while `/proc`
exposes host PIDs, and Lean 4.22 resolves its executable via
`/proc/<getpid>/exe`. I preserved that exact failure in
`08-rerun-klean-preflight.txt`. A narrowly scoped preload shim made `getpid()`
return the host PID read from `/proc/self`; it did not modify any mounted input
or generator output. With that audit-environment repair, the same pinned
toolchain reports Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the mandated preflight
returns:

- status `KLEAN_NO_OBLIGATIONS`;
- frozen/Stage 1 export hash
  `c26f390cd5345408c3d47b8fb0db968f7403b41f68855ccdd9b65223b557812d`;
- discovery hash
  `497c8496354ff1b8533a396dfe78bf41982207e3107006c8ff82861f30038490`;
- generated tree hash
  `d7a42ab1605007d505d72ef8d4233978a721fc37d6d5f29413b6ac60fb2d410d`;
- obligation count 0 and target null;
- `lake clean` exit 0; and
- `lake build` exit 0, with only two unused-variable warnings.

The successful returned evidence is saved verbatim in
`08b-rerun-klean-preflight-with-pid-shim.txt`; the environment diagnosis,
shim hashes, and pinned version output are in
`10-toolchain-environment-repair.txt`.

I also independently recomputed every launcher-recorded hash. Both tree-hash
dialects used by the launcher match their respective fields: K workspace
`24621bd693304af52dd16dc103e053bd56a33b6306eeb9194c41125747a1d73b`,
Stage 1 export `c26f...12d`, selected K audit
`1cdc387615815638d17a07609cb501cb1f7c596c4edac710245142fa9bdbb8e7`,
Stage 4 generation
`87faf79e68edceac0c9d7cace6955122ef0aff3c1e76c4bf8951a8ebd756eb27`,
producer bundle `61e1...e5fb`, discovery `497c...490`, and generated tree
`d7a4...410`. All 772 Stage 1 source-file paths and hashes match with no
missing, extra, or changed entry. The canonical resolved-input hash also
matches. The generator toolchain object equals the lock exactly; the
obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and the trust-inventory hash is
`455485ba0a3837194c48b3f962c319b8f7e1fa58a5f84ad51461ae07fa672a1c`,
both matching their manifests.

## Obligation bijection and fixed target

The independently correct domain set is empty. Correspondingly:

- `input-manifest.json` has `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- generator, export-result, and preflight obligation counts are all zero;
- export-result and preflight statuses are both `KLEAN_NO_OBLIGATIONS`; and
- independent target extraction, generator manifest, preflight, and audit
  input all report target null.

The exact source-rule/obligation identity lists are therefore bijective and
empty. There are no omitted, duplicated, irrelevant, weakened, or vacuous
conjuncts, and no generated theorem whose statement could have changed. This
is a legitimate no-obligation generation because the mathematical domain set,
not merely the manifests, is genuinely empty.

The generated structural project contains 64 inventoried executable trust
declarations, all exactly reconciled by preflight, with no generated `sorry`,
`admit`, or `unsafe` token and no proposition-level trust declaration. Since
there is no generated proposition and the launcher is classification-only,
there must be and is no Stage 5 proof candidate; proof identity, operational
parameter bridges, and `#print axioms Proof.final` are not applicable.

The full independent hash, bijection, target, and Stage 5-absence output is in
`09-independent-hashes-bijection-target.txt`.

VERDICT: PASS
LEGITIMACY: LEGIT
