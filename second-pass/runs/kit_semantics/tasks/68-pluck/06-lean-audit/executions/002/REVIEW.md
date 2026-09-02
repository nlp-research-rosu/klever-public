# Independent audit: HumanEval 68-pluck

## Result and scope

I audited Stage 3 classification, deterministic Stage 4 generation, and the
Stage 5 Lean proof for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. Both `/audit-input.json` and `AUDIT_MODE` select
`CLASSIFICATION_AND_PROOF`. I treated the mounted candidate, prior reports,
logs, comments, and rationales as untrusted evidence and made the semantic
judgments from the frozen K source and supplied operational semantics.

The classifications are correct, the two true domain lemmas are translated
bijectively into the fixed generated target, and the candidate honestly
implements the operational bridge used by those lemmas. The clean Lean proof
proves that exact target with only the accepted Lean core dependencies
`propext` and `Classical.choice`.

## Generator provenance

I hashed the two generation-time producer files before evaluating Stage 4:

| File | Physical SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes match `source-manifest.json`, `generator-manifest.json`, and the
trusted copies in `/reference/tools`. The source and generator manifests name
the same immutable image:

`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

The image ID also matches the launcher-recorded producer-source path. The
producer bundle’s independently recomputed pipeline tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
exactly the value in `/audit-input.json`. There is no missing or mismatched
producer source.

## Inventory reconstruction and Stage 3 judgment

Using the trusted rule-inventory implementation on the frozen Stage 1
workspace reconstructed `VERIFICATION` as the complete local
verification-module closure. It contains 22 ordered, unique rules. The
recomputed values are:

- `verification.k` SHA-256:
  `6108afcbaffc3b32951a2aa04d3a699b8fac095bc7e1c199e8305c8f75f65244`
- whole inventory SHA-256:
  `db923cb4995eb9590d6a8f9ef245d3fdf66930a46476128f1053a8d3903bf90a`

For every rule I independently recomputed its source span, normalized text
hash, and `source_rule_id` (`rule-` followed by that normalized hash). The
protected discovery file contains exactly those 22 entries once each and in
the same order. Its spans, source text, attributes, normalized hashes,
identities, inventory hash, and classifications form an exact bijection:
there are no omissions, duplicates, extra rules, changed hashes, reordered
identities, or unaccounted classifications.

My independent classification is 20 `DEFINITION` rules and two
`DOMAIN_LEMMA` rules, with no `OPERATIONAL_RULE` and no
`PROVED_DERIVED_LEMMA`.

The 20 definitions are the defining equations and recurrences for
`definedProjectInt`, `projectIntTotal`, `allNonNegative`, `shouldTake`,
`nextBest`, `nextBestIndex`, `scanBest`, `scanBestIndex`, `afterIndex`, and
`resultList`. These are named summary predicates, guarded total projection
definitions, or base/recursive equations for named proof summaries. The
per-rule table, including all 22 full rule IDs and spans, is in
`evidence/INDEPENDENT_CLASSIFICATION.md`.

The two domain lemmas are:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   (lines 15–17), which characterizes definedness of the imported partial
   `Val`-to-`Int` cast.
2. `rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167`
   (lines 35–38), which connects guarded dynamic-`Val`
   `applyBin("+", V, I)` to the fixed operational integer-addition rule.

Neither rule defines a new named summary or ordinary execution step. Stage 1
also does not first prove either exact rule in a module excluding it:
`prove.sh` compiles `verification.k` with all 22 rules already present and
then invokes `kprove` on the specification. Thus neither can be a
`PROVED_DERIVED_LEMMA`.

Both domain lemmas are relevant. The frozen solution projects list elements
as integers and its loop executes `value = value + 0` before parity and
minimum comparisons. The specification’s `allNonNegative` precondition
supplies the cast domain. The supplied semantics routes evaluated binary
operators through `applyBin`, with the exact fixed rule
`applyBin("+", I1:Int, I2:Int) => I1 +Int I2`. The cast lemma supplies the
projection side condition, and the guarded addition lemma bridges the
dynamically sorted list head to that fixed operational rule. Every
`simplification` rule in the inventory is either a definition or one of these
two domain lemmas.

## Stage 4 generation and target identity

I directly reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen K workspace, protected classification, selected generation, and
trusted toolchain lock. It returned `status: PASS`, `obligation_count: 2`,
`designated_sorry_count: 0`, and successfully performed its fresh
`lake clean`/`lake build`.

The first attempt exposed a container PID-namespace/procfs mismatch: Lean
4.22 uses `/proc/<getpid()>/exe`, but the mounted procfs exposed outer
namespace PIDs. I compiled the narrow, recorded compatibility shim
`evidence/proc_pid_compat.c`, which makes `getpid()` return the numeric PID
resolved by `/proc/self`. Its source hash is
`e50914170af28af072480b72f38f2b6a84c29504cceefcb7fbe87dc5a52f0b78`
and binary hash is
`f80f8011fd37757fd6ab3c036af3fa361d6982191a515b35896918f70a8a1767`.
It changes no K, generated Lean, or candidate source. With the pinned
`leanprover/lean4:v4.22.0` executable (commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`), the required preflight and all
subsequent Lean checks ran normally.

The generated source-rule/obligation map is an exact ordered bijection:

1. The cast-definedness rule becomes
   `∀ V, project:Int?(inj V).isSome = true ↔
   (definedProjectInt V = true ∧ True)`.
2. The guarded addition rule becomes
   `∀ I V, definedProjectInt V = true →
   applyBin "+" V (inj I) =
   inj (_+Int_ (projectIntTotal V) I)`.

Their source IDs, source spans, normalized hashes, discovery hash, inventory
hash, Lean conjunct text, and conjunct hashes all recompute exactly. There
are two distinct nonempty obligations—no omission, duplicate, irrelevant
obligation, altered guard, or weakened equality.

The internal `∧ True` in the first formula is redundant but accounted for:
it is the exact translation of the source rule’s explicit `#Ceil(@V)`, where
`@V` already has sort `Val`. It does not make the obligation vacuous; after
removing that logically neutral source atom, the proposition remains the
material equivalence between cast success and `definedProjectInt`. It is not
an invented padding obligation or a weakening.

The fixed target is the single declaration
`Klean68Pluck.Lemmas.targetStatement`, exactly the conjunction of those two
mapped obligations. Its hashes are:

- definition SHA-256:
  `ef61fe4ee230f411dabfe5d6ee105d9cd825587ea587a7d790a5049ad3d6d688`
- statement SHA-256:
  `86f622c28060a227aad28accd336804f178be90a23e08b298ecc085194bdc19a`
- generated tree SHA-256:
  `e41cb545c31b19f8b5afb4372a5bbe1723ddac29a6f3843ce2603b35e714ec59`

The declaration, text, hashes, five parameter bindings, and ordered
`source_rule_ids` are identical in the generated source, obligation map,
generator manifest, preflight result, and `/audit-input.json`. The independent
Stage 3 domain set is nonempty, so this correctly is not a
`KLEAN_NO_OBLIGATIONS` case.

I also recomputed the mounted launcher hashes for the K workspace, Stage 1
export, discovery file, selected K audit, Stage 4 generation, producer bundle,
generated tree, candidate workspace, obligation map, trust inventory, and
every Stage 1 source file; all match their recorded values. The launcher also
records a digest for its Stage 5 invocation directory, but that directory is
not one of the mounted audit inputs—the mounted `/candidate` workspace is.
Accordingly, that invocation-directory digest cannot be rehashed here; the
candidate workspace digest itself was independently verified. The complete
launcher-bound trusted gate returned `status: PASS` with resolved-input hash
`163c86e636bf96079156589234e954f239fdb6a7f0e9f39c74bf9d7c24b57cdb`.

## Stage 5 clean proof, identity, and trust

I created `/tmp/audit-work/68-pluck-proof-audit-001`, copied the candidate
there, removed its mounted `Base`, and copied the selected generated project
as a fresh `Base`. In that project:

- `lake clean` exited 0;
- `lake build` exited 0 and built `Klean68Pluck.Lemmas` and `Proof`;
- the only build diagnostic was the generated target’s unused guard variable
  warning;
- the post-build `Base` tree still has hash
  `e41cb545c31b19f8b5afb4372a5bbe1723ddac29a6f3843ce2603b35e714ec59`
  and is byte-for-byte the selected generated tree.

The candidate defines each of the five exact target bindings once, and
`Proof.final` has exactly the generator-recorded statement. It neither changes
nor shadows `targetStatement`. A scan of every non-`Base` Lean source found no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`; there are no candidate-added
trust declarations.

Running Lean on the exact command `#print axioms Proof.final` produced:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

`sorryAx` is absent. Both names are in the trusted gate’s built-in Lean core
allowance (`Classical.choice`, `propext`, and `Quot.sound`); none of the 42
generated declarations in `trust-inventory.json` is used, and there is no
unrecorded dependency. A separate Lean type ascription confirms that
`Proof.final` proves the fixed target with the candidate’s five definitions,
not a second theorem, copied proposition, weakened variant, or vacuous
replacement.

## Operational bridge audit

I compared every target parameter with its `kore_symbol`, bound source rule
IDs, the frozen verification rules, the source solution, and the supplied
operational semantics:

| Parameter | Independent operational judgment |
|---|---|
| `_+Int_` | Defined as Lean integer addition. This is the exact meaning of K `+Int`; a negative case `-7 + 10 = 3` reduces definitionally. |
| `applyBin` | On the bound guarded domain—operator `"+"`, integer-valued left `Val`, and injected integer right operand—the first matching branch returns the injected integer sum, exactly the MPY-INT rule. The test `applyBin "+" (inj -7) (inj 10) = inj 3` reduces definitionally. |
| `definedProjectInt` | Returns true exactly for the `SortVal.inj_SortInt` constructor and false for Boolean and all other constructors, matching `isInt`. |
| `projectIntTotal` | Returns the contained integer exactly on the guarded integer domain. Its zero fallback is only outside the domain of its frozen guarded defining rules and cannot affect either obligation. |
| `project:Int?` | Returns `some i` exactly when the injected K item is an integer and `none` for a Boolean/noninteger, matching the operational partial subsort cast. |

The relevant frozen program path is integer-only: `allNonNegative` establishes
`definedProjectInt`, and `value + 0` dispatches to the integer/integer
`applyBin` rule. Thus the candidate’s bound behavior is not constant,
identity-based, hard-coded to the theorem, or selected merely for proof
convenience.

I compiled an additional Lean adversarial suite. Besides the ground examples
above, it rejects a constant-zero addition, an always-`noneV` `applyBin`, an
always-true domain predicate, a constant-zero projection totalization on an
integer, and an always-`some 0` partial projection on a Boolean.

The suite also records a useful counterfactual: a projection that returns
`some 0` for every injected integer can satisfy the first generated formula
because that source domain lemma constrains only projection definedness
(`isSome`), not the projected value. This is not accepted as the candidate’s
meaning. The separate bridge check confirms that the actual candidate returns
the exact injected integer value (for example `some (-7)`), as required by the
operational cast. This is precisely why the clean theorem alone was not used
as evidence of bridge honesty.

## Evidence

Raw command transcripts, complete command outputs, generated sources and
manifests, audit scripts, failed diagnostic attempts, the per-rule independent
classification, and the successful adversarial Lean source are under
`/audit-output/evidence/`. `evidence/COMMANDS.md` indexes the material files.

VERDICT: PASS
LEGITIMACY: LEGIT
