# Independent audit: HumanEval `8-sum-product`

## Scope and result

The launcher and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF` for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. I independently audited the frozen Stage 1 rule
inventory, Stage 3 classifications, deterministic Stage 4 generation, and the
Stage 5 Lean proof. I treated all mounted candidate and provenance content as
untrusted evidence.

The audit found:

- an exact 14-rule Stage 3 inventory, with no omission, duplicate, extra,
  reordered, or changed rule;
- exactly four genuine, source-relevant `DOMAIN_LEMMA` entries;
- an exact four-rule/four-obligation Stage 4 bijection and unchanged generated
  target;
- a successful fresh `lake clean` and `lake build`;
- exact identity between `Proof.final` and the fixed target instantiated with
  the candidate definitions;
- no candidate trust declaration or forbidden proof escape;
- only `propext`, `Classical.choice`, and `Quot.sound` in
  `#print axioms Proof.final`; and
- operationally faithful candidate definitions on every domain bound by the
  target's source-rule metadata and exercised by the frozen program.

## Producer provenance and artifact integrity

I hashed the two mounted producer sources before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes equal the entries in the producer `source-manifest.json` and
`generator-manifest.json`. Both manifests identify generator image
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
That digest also equals the basename of the immutable producer-source bundle
recorded in `/audit-input.json`. The independently recomputed producer bundle
tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
again exactly the audit-input value. There is therefore no producer-source
infrastructure mismatch.

Other independently recomputed recorded hashes were:

| Artifact | SHA-256 | Result |
|---|---|---|
| Stage 3 discovery manifest | `0a6b05f6531d41a15084b923da2a5df0b26a2a9f50a5496216fb018fba5be0f8` | match |
| generated source tree | `26a316608b521f9fdbf7592b96684cb2ac26e1f8d5f0945f0ee25773777da304` | match |
| complete Stage 4 directory | `0979a3a232946865c485b1bf9e36e55a758ecb42dc51567ec299e436dff128c3` | match |
| Stage 1 exported tree | `f0935a04d815a28216bb9b8b02cf19fa5613ed81d93a1cca886fcadd147fd484` | match |
| Stage 1 pipeline workspace | `1ba212743136486053546c8c441c2f88479626048a6b1de123247f265c0647a4` | match |
| selected Stage 2 tree | `360140f659dc276a33120af1fe7363b2910dfd6cd3da9513c2a6cbe4b9f30a1b` | match |
| mounted candidate tree | `95b8ef4c9da0f087ddee2f7e9d3dca533b07cbe3db8bdb4079bfdd028f070878` | match |

Every Stage 1 path and per-file hash recorded by the launcher also matched.
The full comparisons are in
[`02-independent-structural-checks.txt`](/audit-output/evidence/02-independent-structural-checks.txt).
The historical Stage 5 invocation directory itself is not one of the mounted
inputs, so its recorded `lean_invocation_sha256` (and the invocation's
individual log hashes) cannot be recomputed from this audit container. I did
not use those unmounted logs as evidence; I independently hashed the mounted
candidate and reran all proof checks in the fresh workspace.

## Inventory reconstruction

I invoked the trusted `k_rule_inventory.inventory_verification` implementation
with `PYTHONPATH=/reference` against `/reference/k-proof`. The local
verification-module closure is exactly `VERIFICATION`. Its frozen
`verification.k` hash is
`b411022ccf9bdbf21a93b4ae25660119eea041b74493fd9a008ed1dc87b0d843`;
the reconstructed inventory contains 14 ordered rules and has inventory hash
`11a97077795acdba4d3bb7290d390b37e211fd8696e566f66fe2af8c1f6b3c68`.

For each row below, the full `source_rule_id` is `rule-` followed by the shown
normalized SHA-256.

| # | Source span | Normalized SHA-256 | Independent class | Judgment |
|---:|---:|---|---|---|
| 1 | 11 | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | `allInts` empty case |
| 2 | 12–13 | `d1d219f3427f5536073a572ec05d566def4e43ec32fddd6fbff02d536113eb4e` | `DEFINITION` | `allInts` recurrence |
| 3 | 19 | `9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | `DEFINITION` | names cast definedness as `isInt` |
| 4 | 24–26 | `0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` | cast definedness equivalence |
| 5 | 28–30 | `ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | `DEFINITION` | guarded `projectIntTotal` equation |
| 6 | 32–34 | `22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | `DEFINITION` | reverse macro orientation for the named projection |
| 7 | 36 | `7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | `DEFINITION` | projection on an `Int` |
| 8 | 37–39 | `9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | `DOMAIN_LEMMA` | projection coherence/idempotence |
| 9 | 43–46 | `3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0` | `DOMAIN_LEMMA` | guarded dynamic-to-static integer `+` dispatch |
| 10 | 48–51 | `85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4` | `DOMAIN_LEMMA` | guarded dynamic-to-static integer `*` dispatch |
| 11 | 56 | `72e5eac672dc42c33a08defca9cae94adfeb15589c8e4181a9bc48cdc32e7a63` | `DEFINITION` | `sumFrom` empty case |
| 12 | 57–58 | `7f9611f1ad40bdd1fce4065a2139931095c8d3af173a8dbcb75b95576da67c98` | `DEFINITION` | `sumFrom` recurrence |
| 13 | 61 | `421bf17a6cbeb7277fb51e605cd8c239397335231755fe2e0b862ab38281bbc8` | `DEFINITION` | `productFrom` empty case |
| 14 | 62–63 | `1e836dcf2b1df7f6322a01e54db668a6f35bbb7b27c89af9bd65f887168bade0` | `DEFINITION` | `productFrom` recurrence |

The reconstructed source spans, attributes, normalized hashes,
`source_rule_id` values, texts, and ordering match the protected discovery
manifest bijectively. Both inventories have no duplicate identity.

There are no `OPERATIONAL_RULE` entries in this local proof-module inventory:
the rules either define proof summaries/named projection machinery or assert
facts about imported operational symbols. There are no
`PROVED_DERIVED_LEMMA` entries. In particular, `prove.sh` compiles
`verification.k`, including all 14 rules, before its only positive `kprove`
invocation; it never first proves one of these exact rules against a module
that omits it.

All rules carrying a `simplification` or `simplification(10)` attribute are
classified as either `DEFINITION` or `DOMAIN_LEMMA`. None is mislabeled as an
ordinary operational rule or as a proved-derived lemma.

## Independent classification judgment

The independently selected domain set is exactly rules 4, 8, 9, and 10 above.
These are mathematical facts rather than definitions:

1. The partial `Val`-to-`Int` projection is defined exactly on integer values.
2. Reinjecting a totalized projection and projecting again is coherent.
3. On two integer values, dynamic `applyBin("+", ...)` agrees with integer
   addition after projection.
4. On two integer values, dynamic `applyBin("*", ...)` agrees with integer
   multiplication after projection.

All four are relevant. The source function consumes `List[int]`, initializes
`total` to `0` and `product` to `1`, then performs `+=` and `*=` in its loop.
The Stage 1 postcondition is expressed with the `sumFrom` and `productFrom`
recurrences, and the claim requires `allInts(VS)`. The cast facts and exact
integer operator dispatch are therefore used at the loop boundary; none is
unrelated domain mathematics.

The remaining ten rules meet the requested `DEFINITION` criterion: they
introduce the input-domain predicate, the named total projection/macro
equations, or the two recursive summaries. The Stage 3 protected
classifications consequently agree with the independent classification.

## Stage 4 generation and mathematical adequacy

I reran the requested trusted call:

```python
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

with `PYTHONPATH=/reference`. The final run returned `status: PASS`,
`obligation_count: 4`, `designated_sorry_count: 0`,
`trust_declaration_count: 42`, and successful internal `lake clean` and
`lake build` diagnostics. Its complete returned evidence is
[`06-preflight-rerun-success.txt`](/audit-output/evidence/06-preflight-rerun-success.txt).

The four independently identified domain IDs are, in the same order, exactly:

- the protected discovery domain IDs;
- `obligation-map.json`'s `source_rules`;
- `obligation-map.json`'s `obligations`; and
- the union covered by `target.parameters[*].source_rule_ids`.

There are no duplicates. Each obligation's source span and normalized source
hash equals the frozen inventory entry, and each recorded Lean-conjunct hash
equals the independently hashed conjunct. The obligations state exactly:

1. integer projection definedness iff named definedness is true;
2. `projectIntTotal` reinjection/projection coherence;
3. guarded integer `applyBin("+", V, W)` agreement; and
4. guarded integer `applyBin("*", V, W)` agreement.

The `∧ True` inside the first lowering is the exact image of the source
`#Ceil(@V)` for an already typed `@V : Val`; it does not replace the
substantive projection/definedness equivalence, and it does not create a
top-level empty obligation. The arithmetic hypotheses are also not vacuous for
the submitted bridge: explicit injected integer witnesses make both `isInt`
tests and `_andBool_` true.

No obligation is irrelevant, weakened, omitted, duplicated, or replaced by a
free `True`. This is not a `KLEAN_NO_OBLIGATIONS` case.

The fixed target is:

| Field | Verified value |
|---|---|
| declaration | `Klean8SumProduct.Lemmas.targetStatement` |
| file | `Klean8SumProduct/Lemmas.lean` |
| definition SHA-256 | `55b08aa8a5b59441f5a76fe44add2c5df625679fa17315679d177dbeebdd5c35` |
| statement SHA-256 | `831b5e69c5ed784822b0d89bc921a3becaf9e70c01077639ac2d87bca8555119` |
| obligation-map SHA-256 | `cd9a558084519075d03967923886f41e3c48e8f10353ea87618911a06b6e10f4` |

The independently extracted target equals both `generator-manifest.json` and
`/audit-input.json`, including every parameter binding and source-rule list.

## Fresh Stage 5 build and target identity

I created `/tmp/audit-work/stage5-fresh-002`, copied only the candidate's source
project files into it, and copied the exact generated project contents into
`Base`. This deliberately excluded the mounted candidate's stale `.lake`
directory and empty `Base` placeholder. Before building, the candidate
`Proof.lean` SHA-256 matched the mounted file, and the copied
`Base/Klean8SumProduct/Lemmas.lean` matched the generated source.

Using Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0:

- `lake clean` exited 0;
- `lake build` exited 0 with “Build completed successfully”; and
- the only reported issues were two unused-variable linter warnings in the
  immutable generated target.

After the build, `diff -qr --exclude=.lake` found no difference between
fresh `Base` and `/reference/klean-generation/generated`. The target source
file hash on both sides is
`f8b4008aac8baae81d868e656580d37b556bf3952c971a6cd516f20503f94f31`.

The candidate declares eight bridge definitions and `theorem final`. It does
not declare or shadow `targetStatement`. A scan of candidate-controlled Lean
sources found no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`; the trusted
generation parser likewise found no candidate trust declaration.

`Proof.final` has exactly the normalized fixed statement:

```text
Klean8SumProduct.Lemmas.targetStatement _andBool_ «_+Int_» «_*Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» isInt projectIntTotal «project:Int?»
```

The successful direct `#check`/`#print` output in
[`19-proof-identity-lean-success.txt`](/audit-output/evidence/19-proof-identity-lean-success.txt)
shows the same declaration and its full proof term. Thus `Proof.final` proves
the fixed generated theorem itself, not a duplicate or altered theorem.

## Axiom accounting

The exact requested Lean output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

It exited 0 and is preserved in
[`12-print-axioms.txt`](/audit-output/evidence/12-print-axioms.txt).
There is no `sorryAx`.

The generated project's 42 explicit trust declarations exactly equal the 42
entries, including kinds and types, in `trust-inventory.json`. None of those
42 declarations occurs in `Proof.final`'s dependency list. The three reported
dependencies are Lean's core propositional extensionality, classical choice,
and quotient soundness. The candidate introduces no axiom or opaque
declaration, and both designated and other generated sorry counts are zero.
The reconciled set of unrecorded proof trust escapes is empty; see
[`16-axiom-reconciliation.txt`](/audit-output/evidence/16-axiom-reconciliation.txt).

## Operational-bridge audit

I located the exact candidate `def` for every generated target parameter and
compared it with its KORE binding, bound source-rule IDs, frozen rules, source
function, and supplied semantics:

| Parameter | Candidate definition | Independent bridge judgment |
|---|---|---|
| `_andBool_` | Lean Boolean `a && b` | Exact `BOOL.and` truth table; crucially `true && true = true`, so integer guards are not disabled. |
| `«_+Int_»` | Lean `Int` addition | Exact unbounded K `+Int`; negative and very large witnesses agree. |
| `«_*Int_»` | Lean `Int` multiplication | Exact unbounded K `*Int`; negative and zero witnesses agree. |
| `applyBin` | Pattern match with exact integer `+` and `*` branches | On the complete match domains of bound rules `3eff…` and `85c5…`, returns precisely injected K integer addition/multiplication in the correct operand order. |
| `definedProjectInt` | `isInt` of the injected `Val` | Exact named definition in frozen rule `9e2e…` and exact cast-definedness domain of rule `0312…`. |
| `isInt` | `.isSome` of `project:Int?` | True exactly for the relevant singleton-K injection of an integer and false for Boolean and non-singleton adversarial values. |
| `projectIntTotal` | integer projection with `getD 0` | Returns the exact integer on every defined K cast domain. The default only totalizes cases where the K cast has no value; it is never used to falsify the integer guards. |
| `project:Int?` | singleton injected integer maps to `some i`, all else to `none` | Exact generated injection/projection shape and correct on positive, negative, Boolean, and malformed-sequence witnesses. |

The bound `applyBin` source-rule domains and the source program are integer
`+` and integer `*`. The candidate also defines additional numeric cases, but
the audit does not claim those unrelated branches are proved by this target.
Conversely, K's string-concatenation branch is outside both bound
`source_rule_ids` and every execution admitted by the frozen `List[int]`
precondition, so the candidate's fallback outside the bound match domains
cannot affect this theorem. On the full relevant match domains, the two
branches are exact rather than observational shortcuts.

Machine-checked adversarial examples cover the Boolean truth table, negative
and very large integers, exact `applyBin` results, integer/non-integer
projection, a malformed multi-item K sequence, and totalized non-integer
projection. They also distinguish the submitted definitions from constant
false, identity addition, addition-as-multiplication, constant `applyBin`,
constant definedness/type tests, constant projection, and always-failing
projection. The test file and output are
[`BridgeTests.lean`](/audit-output/evidence/BridgeTests.lean) and
[`13-operational-bridge-tests.txt`](/audit-output/evidence/13-operational-bridge-tests.txt).

As a stronger counterfactual, I compiled two deliberately dishonest
instantiations of the bare target:

- constant-false `_andBool_`, which makes both arithmetic hypotheses false;
  and
- coordinated constant-zero `+Int`, `*Int`, and `applyBin`.

Both can inhabit the parameterized target, demonstrating that a clean proof of
the equation alone would be insufficient. The source and successful compile
are preserved in
[`CounterfactualGuard.lean`](/audit-output/evidence/CounterfactualGuard.lean)
and
[`22-counterfactual-vacuous-and-hardcoded-bridges.txt`](/audit-output/evidence/22-counterfactual-vacuous-and-hardcoded-bridges.txt).
The submitted candidate is not either model: its concrete definitions and
compiled distinguishing witnesses implement the frozen source-relevant
meaning. This closes the operational-bridge check rather than relying on the
target's formal inhabitance alone.

## Evidence and runner diagnostics

Raw commands are collected in
[`00-command-log.md`](/audit-output/evidence/00-command-log.md), and complete
outputs and audit scripts are under `/audit-output/evidence/`.

Several preliminary setup failures are intentionally retained:

- `01-producer-provenance.txt` printed the producer hashes, then exited 127
  because `jq` is absent; the successful Python comparisons supersede it.
- `03-preflight-rerun.txt` and `04-preflight-rerun-configured.txt` exposed a
  runner-specific Lean failure: this sandbox permits `/proc/self/exe` but not
  Lean's `/proc/<pid>/exe` lookup.
- `08-fresh-workspace-copy.txt` detected that a first copy layout had nested
  the generated project under `Base/generated`; that workspace was discarded
  before any proof judgment.
- `18-proof-identity-lean.txt` records a mistaken nonexistent toolchain path;
  `19-proof-identity-lean-success.txt` is the corrected successful run.

For the successful Lean runs I used the source-retained
`proc_exe_compat.c`, which redirects only numeric
`/proc/<pid>/exe` `readlink`/`readlinkat` requests to `/proc/self/exe`. It does
not modify candidate/generated sources, declarations, proofs, or Lean
semantics. The trusted preflight, fresh clean/build, axiom print, proof print,
bridge witnesses, and counterfactuals all then ran to completion.

VERDICT: PASS
LEGITIMACY: LEGIT
