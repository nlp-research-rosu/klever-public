# Independent audit: HumanEval 59-largest-prime-factor

Audit mode was `CLASSIFICATION_AND_PROOF`; condition was `semantics`; semantics
mode was `SUPPLIED_SEMANTICS`.

The Stage 3 classification and Stage 4 provenance/structural mapping are
internally consistent. The result is nevertheless not legitimate because the
only generated Lean obligation is vacuous: the frozen K `Scope` sort is
inhabited by `scope(Map, Parent)`, but generated `SortScope` has no constructors.
In addition, the candidate definition of K Map concatenation is ordered list
append and violates K Map commutativity on disjoint maps.

## Frozen-input and producer provenance

I recomputed every hash whose input is mounted. All matched
`/audit-input.json`:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 tree (`pipeline_contract.sha256_tree`) | `5a386674aaf35f450ecafeb7f348fbf2003de9c1ab5c1b7fe7428b9d08971171` |
| Stage 1 export tree (`klean_export.tree_digest`) | `90be5ee41912354e693ab7a94400da755b0c4f00f44d7268bee82fafbce81af4` |
| Stage 2 selected audit tree | `8766796efbd7d9b7e75385d76ee3943e5d2d9c87a2b199fb9e8b204c57464d82` |
| Stage 3 manifest | `e3efd90d780e830a4280a1280a1da90fbf7b4b88a55f34ad75166669a8498613` |
| Stage 4 selected generation tree | `e7afd20c400ab054435d9c96f65c1dbdd98690d8fd712ff0f21956572507d625` |
| Generated project tree | `33c00e5142086d7df53c6e58268ea1bd12282d19ac4ed79be6d1bfe53160033f` |
| Producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| Stage 5 candidate tree | `b96a93b9ae6fefa63f843be7a23e5c207b5324a30b967fc3050e892527cd2de3` |

The complete per-file Stage 1 source map also matched exactly. The
launcher-recorded Stage 5 invocation tree itself is not mounted; it was not
used as evidence. The mounted candidate workspace hash above was independently
verified.

Before judging Stage 4, I directly hashed the immutable producer sources:

| Producer | Actual and recorded SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Those values agree with `generator-manifest.json` and
`source-manifest.json`. Both manifests and the final path component recorded
in `/audit-input.json` identify the same immutable generator image:
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
There is no producer-source infrastructure error.

Full recomputation is in
[`provenance-verification.json`](evidence/provenance-verification.json).

## Rule inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof`, rather than using the protected classification as
an inventory source. The local verification-module closure is exactly the
single module `VERIFICATION`.

The reconstruction found 12 unique rules in source order. It recomputed:

- `verification.k` SHA-256:
  `a2d250bccf8d792ff241ae2c74ee0c40b93f6a991b038a3a99da4cd0a574ca64`;
- inventory SHA-256:
  `25b938408e3059398c920d927e696e9f95b8d23ac41685644a7a5cd11105f257`;
- exact spans: `9–11`, `16–27`, `31–32`, `35–40`, `45–46`,
  `47–49`, `50–51`, `58–70`, `72–86`, `88–102`, `104–117`,
  and `119–128`; and
- each normalized source hash and `source_rule_id`.

The protected Stage 3 manifest has exactly the same 12 ordered IDs. Both lists
are duplicate-free; there are no missing or extra IDs; every ID is
`rule-` followed by the reconstructed normalized hash; and the whole inventory
hash matches. Because the inventory hash commits to the complete rule
documents, it also binds the reconstructed spans and texts even though the
compact Stage 3 file lists only IDs, classifications, and rationales.

Raw reconstruction and the explicit comparison are in
[`inventory-reconstruction.json`](evidence/inventory-reconstruction.json) and
[`inventory-bijection.txt`](evidence/inventory-bijection.txt).

## Independent Stage 3 classification

My ordered classification is:

| Frozen span | Classification | Judgment |
|---:|---|---|
| 9–11 | `DOMAIN_LEMMA` | Fresh-key Map removal equality. It defines no symbol and was available during the only proof run. It is relevant because MPY `#pop` changes the scope map to `SC [ L <- undef ]`, while the loop claim must restore `SC`. |
| 16–27 | `DEFINITION` | Defines the named `solutionModule` macro as the source AST. |
| 31–32 | `DEFINITION` | Defines `lpfCondition`. |
| 35–40 | `DEFINITION` | Defines `lpfStep`. |
| 45–46 | `DEFINITION` | Base equation of the named `lpfSpec` recurrence. |
| 47–49 | `DEFINITION` | Divisible branch of `lpfSpec`. |
| 50–51 | `DEFINITION` | Nondivisible branch of `lpfSpec`. |
| 58–70 | `OPERATIONAL_RULE` | Observes the active scope and executes the integer loop comparison. |
| 72–86 | `OPERATIONAL_RULE` | Observes the active scope and executes the remainder-equality test. |
| 88–102 | `OPERATIONAL_RULE` | Executes the floor-division assignment to `n`. |
| 104–117 | `OPERATIONAL_RULE` | Executes `factor += 1`. |
| 119–128 | `OPERATIONAL_RULE` | Executes return observation/control and proceeds to `#pop`. |

There is no `PROVED_DERIVED_LEMMA`. `prove.sh` compiles the complete
`VERIFICATION` module once and then invokes `kprove` once; no inventory rule is
first proved in a module that omits it and only later imported.

The only `[simplification]` entry is the line 9–11 Map equality, and it is
classified `DOMAIN_LEMMA`. The protected Stage 3 sequence exactly matches this
independent sequence. A fuller per-rule explanation is in
[`independent-classification.md`](evidence/independent-classification.md).

## Deterministic Stage 4 structural check

I reran the required trusted call:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The audit sandbox exposes host `/proc` inside a separate PID namespace. Lean
therefore initially failed to locate `/proc/<namespace-pid>/exe`; this occurred
before any project check. I preserved that output, then used a narrow
`LD_PRELOAD` shim which changes only `/proc/<digits>/exe` reads to
`/proc/self/exe`. It does not modify Lean, the candidate, generated sources, or
proof behavior. With that environment repair, the trusted check returned
`PASS`, performed successful fresh `lake clean` and `lake build` commands, and
reported:

- one domain obligation;
- one unique mapped source ID,
  `rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84`;
- zero designated sorries;
- 51 generated trust declarations; and
- generated tree hash
  `33c00e5142086d7df53c6e58268ea1bd12282d19ac4ed79be6d1bfe53160033f`.

The domain-rule list, `obligation-map.json` source list, and obligation list are
an exact ordered one-to-one mapping with no duplicate, omission, or extra
entry. The generated conjunct is the direct syntactic translation of the
fresh-key Map removal rule, and it is relevant to scope deallocation.

The fixed target also matches `generator-manifest.json` and
`/audit-input.json` byte-for-byte under the trusted target parser:

- declaration:
  `Klean59LargestPrimeFactor.Lemmas.targetStatement`;
- definition SHA-256:
  `a32b56fd44e16d539b6a1a3ec2306f5be78902cd6aa9cb6e8303ca764dc22430`;
- instantiated statement SHA-256:
  `ef927764ebb1f8f6cdabfad95f717d04b5b6c3952caba94ba1994a7295684f4c`;
- five parameters bound to the same source rule: `_Map_`, map membership,
  map deletion, map element, and Boolean negation.

The returned preflight document is
[`check-generation-rerun.json`](evidence/check-generation-rerun.json).

### Mathematical failure in the generated target

The structural pass is insufficient. Frozen
`reference-semantics/semantics/core.k` declares:

```text
syntax Scope ::= scope(Map, Parent)
```

so `Scope` has ordinary values, and the source rule quantifies `_V:Scope`.
Generated `Sorts.lean`, however, declares:

```lean
inductive SortScope : Type
```

with no constructor anywhere in the generated project. The only target
conjunct quantifies `_V : SortScope`. Consequently it has no ground instance
and proves nothing about removal of a real scope value.

[`BridgeAudit.lean`](evidence/BridgeAudit.lean) machine-checks the
counterfactual: `_Map_`, membership, deletion, element, and negation can all be
unrelated constant functions, yet the exact fixed target follows by
`nomatch scope`. The test exits 0. This is a vacuous conjunct and a weakened
generated obligation, which requires rejection even though all manifests and
hashes are self-consistent.

The selected status is not `KLEAN_NO_OBLIGATIONS`, and the independent domain
set is genuinely nonempty. The failure is instead that the sole generated
obligation erased its inhabited source domain.

## Stage 5 build, theorem identity, and trust

I created `/tmp/audit-work/stage5-fresh-001`, copied the candidate into it, and
copied the immutable generated project into `Base`. The copied Base retained
the exact generated tree hash
`33c00e5142086d7df53c6e58268ea1bd12282d19ac4ed79be6d1bfe53160033f`;
`Proof.lean` retained SHA-256
`55aa4db724f6f61b5006f1230b0367baf6630ae8d19bb336a052792b53003004`.

Both required commands succeeded:

```text
lake clean  -> exit 0
lake build  -> exit 0
```

The candidate:

- does not modify or shadow `targetStatement`;
- defines each of the five target parameters exactly once;
- contains exactly one `theorem final`;
- states the exact fixed generated theorem;
- contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`; and
- cleanly passes the trusted mechanical final gate.

Exact outputs are in
[`stage5-lake-clean.log`](evidence/stage5-lake-clean.log),
[`stage5-lake-build.log`](evidence/stage5-lake-build.log), and
[`stage5-integrity.txt`](evidence/stage5-integrity.txt).

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are the three standard Lean axioms explicitly admitted by the trusted
mechanical gate. None of the 51 generated declarations in
`trust-inventory.json` is a dependency. There is no `sorryAx` and no
unrecorded dependency. See
[`print-axioms.log`](evidence/print-axioms.log) and
[`axiom-accounting.txt`](evidence/axiom-accounting.txt).

These mechanical facts do not repair the vacuous target.

## Operational-bridge audit of the five definitions

The K 7.1.293 Map definition states that `_Map_` is partial on overlapping
keys and is `assoc`, `comm`, and unitary on defined inputs. It forbids multiple
bindings for one key. The candidate definitions compare as follows:

| Parameter | Candidate meaning | Operational judgment |
|---|---|---|
| `_Map_` | `left.coll ++ right.coll` | **Fails.** Ordered list append is not commutative even for disjoint valid singleton maps, while K Map concatenation is commutative. It also returns duplicate-key lists instead of respecting partial definedness, although the disjoint counterexample alone is decisive. |
| map `in_keys` | Recursive syntactic key membership | Matches key membership on valid finite-map lists. |
| map deletion | Removes every pair with the selected key | Matches removal on valid maps, which have at most one such key. |
| `_|->_` | One-pair list | Matches a singleton map element. |
| `notBool_` | Lean Boolean negation | Matches K Boolean negation. |

[`BridgeAudit.lean`](evidence/BridgeAudit.lean) also proves that the candidate
`_Map_` gives different Lean values for the two orders of two distinct,
disjoint singleton maps. That adversarial theorem elaborates successfully,
while K equates those orders through `_Map_`'s `comm` attribute. Thus the
candidate has an operational-bridge failure independently of target vacuity.

## Conclusion

The Stage 3 labels are correct, and deterministic provenance plus all
mechanical Stage 4/5 gates are intact. The mathematical audit nevertheless
finds two decisive failures: Stage 4 makes its only obligation vacuous by
translating an inhabited K sort to an empty Lean type, and Stage 5 supplies a
noncommutative implementation for K's commutative Map concatenation. The clean
build and clean axiom list therefore do not establish the frozen domain lemma.

Raw commands, test sources, and complete captured outputs are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
