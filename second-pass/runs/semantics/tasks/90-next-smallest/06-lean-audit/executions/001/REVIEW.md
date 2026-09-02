# Independent audit: HumanEval 90-next-smallest

## Scope and result

I audited condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`, in
`CLASSIFICATION_AND_PROOF` mode. Both `/audit-input.json` and `AUDIT_MODE`
record that mode.

The frozen Stage 3 classification is complete and mathematically correct. The
deterministic Stage 4 artifact contains exactly one obligation for the one
genuine domain lemma, and its fixed target is an exact translation of that
rule. The Stage 5 project builds from a fresh clean copy, `Proof.final` has the
exact fixed type, all of its axioms are accounted for, and all eight candidate
bridge definitions implement their frozen operational meanings. I found no
omission, weakening, target substitution, trust escape, or convenient
definition.

## Producer-source and provenance integrity

Before assessing Stage 4 I hashed the mounted producer sources:

| Source | SHA-256 |
|---|---|
| `klean_export.py` | `6d620b92d4de6a051dea0ef5ed4670a77d76199648a7b64808b91286b3dd20c0` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These are exact matches for both the source manifest and
`generator-manifest.json`. The immutable generator image ID in the source
manifest, generator manifest, and audit-input-bound producer path is uniformly
`sha256:cf7f2501e6059bf1f49cbb078023e544b7884d51ee6bb298cbfe8bc42ec9097e`.
The producer pipeline artifact tree hash, computed with the trusted pipeline
tree-hash algorithm, is
`1823e0fd1f4044c938deff6d834503b56bff528c74b01bd6f27a472d0a337e39`,
exactly as recorded in `/audit-input.json`.

The preserved `00-producer-integrity.log` was an initial algorithm-selection
probe that incorrectly applied the Klean generated-export `tree_digest`
algorithm to the whole producer artifact. It therefore reported an apparent
aggregate mismatch. The producer artifact is bound by the pipeline tree-hash
algorithm, not `tree_digest`; the corrected check in
`01-producer-integrity-correct-algorithm.log` passes every source, image, and
aggregate check. This is not a missing or mismatched producer source.

I also recomputed every recorded Stage 1 per-file hash and the mounted Stage 1,
Stage 2, Stage 3, Stage 4, generated-export, and Stage 5 tree/file hashes. All
match `/audit-input.json`.

## Independent rule-inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` code on
the frozen `/reference/k-proof` before loading the protected Stage 3
classification. The selected local verification module is
`NEXT-SMALLEST-WITH-LOOP-LEMMA`; its local `verification.k` closure is:

1. `NEXT-SMALLEST-VERIFICATION`
2. `NEXT-SMALLEST-WITH-LOOP-LEMMA`

The frozen `verification.k` SHA-256 is
`08e2a66428c4b9adfe95239bc96c364e2f62d3419794fe698e7e7ea1bd53c59c`.
The reconstruction contains 19 rules and has canonical inventory SHA-256
`fa23b9c4607ef517134979f874e704c9629ea9852e1eeb73ba5642663a693ab5`.

For each rule I independently sliced the recorded source lines, normalized
whitespace, recomputed the normalized source hash, reconstructed
`source_rule_id = "rule-" + normalized_sha256`, and recomputed the whole
canonical inventory hash. Comparison with `/reference/lemma-discovery.json`
is an exact ordered bijection: 19 versus 19, with no omission, duplicate,
extra rule, reordered identity, changed span, or changed hash.

## Independent classification

The following is my classification from the frozen text and the supplied
operational K semantics, not an adoption of the protected labels.

| Frozen span | Source rule identity | Classification | Independent reason |
|---|---|---|---|
| 9–25 | `rule-5d2d5767e4dddebd9a7a6d22be189c7642a9ba811be0c7a4d8f63f020f9cd858` | `DEFINITION` | Macro defining the named loop-body statement term. |
| 28–32 | `rule-e4a29a4e353dba077b430b87e1e395934a29a851148c33cf4846ec4de15e093f` | `DEFINITION` | Macro defining the post-loop return sequence. |
| 35–41 | `rule-fcde16193af01e4771b1d9ea9ec9fa57b62264bf88836347b998118e7e786418` | `DEFINITION` | Macro composing initialization, loop, and return into the function body. |
| 44–45 | `rule-f357bb3cd9996bbab4f6dcb8768e2e648eb6cc49c48da5d9a4155d6138183771` | `DEFINITION` | Macro defining the module containing `next_smallest`. |
| 54 | `rule-067871e46d1874d93e1cf2b77305ec506b9df5cc4c6dfd3124f5a21c14a1871a` | `DEFINITION` | Base equation for the `intsEmpty` observer. |
| 55 | `rule-774b2bfe520129add55f4d7ecf8c398615344202df34a624da01108283cffde2` | `DEFINITION` | Constructor equation for the `intsEmpty` observer. |
| 56 | `rule-823d37f3fd0fb7a719825948b6beb6786c49c6d71d75bf3c095948bd5ddca77b` | `DEFINITION` | Head projection equation. |
| 57 | `rule-f31b7c50d1df1e9b8e13dc3a760fe3c5a815e023a1d40304b64dd975c7022b6a` | `DEFINITION` | Tail projection equation. |
| 58–59 | `rule-c3bbc4578420bfc77e185d7e8b40307b970e61d08375688dd7255b2c6842cdd7` | `OPERATIONAL_RULE` | Ordinary iterator execution rule: an empty integer carrier produces `#iterDone`. |
| 60–62 | `rule-214b64e9f98d1b28da26cee68c41aac638fd294904b41f43c6e129de8fe23d4d` | `OPERATIONAL_RULE` | Ordinary iterator execution rule: yield the head and advance to the tail. |
| 67–68 | `rule-b66aa045ce6d34606acc56ebd67dba56587d63db4906a7da23de20b161d4f7e4` | `DEFINITION` | Terminal `nsScan` equation returning the second value when `count = 2`. |
| 69–70 | `rule-fb666e47c86303d94e9f9cf453ebad197a98d92c9c2fb00f8ba95c8301d06eb1` | `DEFINITION` | Terminal `nsScan` equation returning `noneV` otherwise. |
| 71–73 | `rule-50de226a7d637d91ff05c7856d5ed23d004e981405416dcb662ba6a8861c22f1` | `DEFINITION` | Recursive initialization equation. |
| 74–77 | `rule-efbe01e60fe5fcfaf647ad5a84d03d3ee7130712a9528f77d88a7e0df347551b` | `DEFINITION` | Recursive new-minimum/old-minimum-shift equation. |
| 78–81 | `rule-bfa35b1c80fb01a4594475eac3f77d47d76556fec21a06853075dba8509a0403` | `DEFINITION` | Recursive duplicate-minimum equation. |
| 82–85 | `rule-6986b2203560a617e3de370ce1151594398170c4b52dce18cd4f451e2fae22a8` | `DEFINITION` | Recursive first-distinct-above-minimum equation. |
| 86–90 | `rule-9924c381571bc232102ba71dd2bb52d1a4f95615a7273b08819452fae32eea15` | `DEFINITION` | Recursive replacement of the second candidate. |
| 91–95 | `rule-37cd9f38f1fd5fee88469c885e3fa549cc9750530a7e2e58f1d004900a5c69d4` | `DEFINITION` | Recursive preservation of the existing second candidate. |
| 104–145 | `rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba` | `DOMAIN_LEMMA` | Priority-40 loop summary, including return, frame deletion, and stack pop. |

Totals are therefore 16 `DEFINITION`, 2 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`.

The eight guarded `nsScan` equations are a genuine total recurrence: the two
terminal guards partition empty inputs, the six nonempty branches partition
the accumulator/value cases, and every recursive call consumes the tail.
They directly summarize the frozen source program's maintenance of its
smallest and second distinct values. The two iterator rules instead change
the `<k>` cell according to the supplied iterator protocol and are ordinary
execution rules.

The priority-40 rule is not a `PROVED_DERIVED_LEMMA`. Stage 1 first proves the
loop claim against `NEXT-SMALLEST-VERIFICATION`, but that claim leaves the
final scopes cell existential as `?FINAL_SCOPES`. The later installed rule
asserts the stronger, specific map-deletion result
`((SC 1 |-> scope(...))[1 <- undef])`. Thus Stage 1 did not first prove the
exact same rule against a module that omitted it. The correct class is
`DOMAIN_LEMMA`.

That domain lemma is relevant and nontrivial. It summarizes the exact
`#loop(list(intVals(INPUT)), Name("value"), nextSmallestLoopBody)` followed by
`nextSmallestReturn` and `#endcall`; returns the `nsScan` result to `CONT`;
restores environment and scope location; deletes the function frame; pops the
saved stack frame; and preserves heap, heap location, exception, exit code,
and generated counter. This is precisely the bridge needed by the public
entry proof and the program's second-distinct-minimum postcondition.

No rule in the reconstructed closure has a `simplification` attribute, so the
requirement that every simplification rule be a definition or domain lemma is
satisfied vacuously.

## Stage 4 generation and obligation judgment

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` on exactly `/reference/k-proof`,
`/reference/lemma-discovery.json`, and `/reference/klean-generation`.
The trusted checker performed `lake clean` and `lake build` and returned:

- status `PASS`;
- one obligation;
- no designated sorry;
- frozen Stage 1 export hash
  `544d4f2fe968326bdcef3d229eff8a87f864516a6321613909f6a824619f749e`;
- discovery hash
  `13e65f52ec7b2cbe7ae68004aa6708264be4721f681108151d765e00fecde8ee`;
- generated tree hash
  `0f18c75c715f2d3f48706fe3f023557f4976b77fc0edf1eaa8f014f92a973d53`.

The sandbox does not expose Lake's process executable through `/proc/*/exe`,
so the first two preserved preflight attempts fail at Lake toolchain
detection. I did not run the candidate-provided shim. I independently wrote
and compiled the small recorded `lean_proc_exe_shim.c`, which only supplies
the pinned lockfile Lean/Lake executable paths for those `readlink` calls.
The pinned tools report Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0. With that
environment-only adaptation, the trusted preflight ran unchanged and
completed successfully.

Independently of preflight, I verified this exact ordered bijection:

`one independently classified domain rule`
→ `one input-manifest source rule`
→ `one obligation-map source rule`
→ `one generated obligation`.

All source spans, normalized hashes, inventory hashes, discovery hashes,
conjunct hashes, obligation-map hash, and eight parameter binding hashes are
exact. There are no omitted, duplicated, extra, or reordered obligations.
The conjunct is a universal `Rewrites` proposition, not literal `True` or
`False`. Its freshness premise is the source rule's nontrivial K map
definedness condition `notBool (1 in_keys(SC)) = true`; although the generated
file's linter notes that the proof object named `h` does not occur in the
conclusion, the dependent function domain still requires that proposition,
and the Stage 5 proof materially uses it.

Mathematically, the generated start and destination configurations retain all
parts of the domain rule: loop body, return continuation, environment change,
function-frame map, exact frame deletion, scope-location restoration, stack
pop, returned `nsScan` value, heap, heap location, return state, exception,
exit code, and generated counter. I found no weakened cell, irrelevant
obligation, missing side condition, vacuous conjunct, or target change.

The fixed target is:

- declaration: `Klean90NextSmallest.Lemmas.targetStatement`;
- definition SHA-256:
  `4435753cc367d7fce4884d8fa89681ab379c3a0b8fc1978a6498ba1fe9166a49`;
- instantiated-statement SHA-256:
  `47fdb9521e07ecb90449987529383f9c0e1bf2ac5919d77e15dfb5923af3078e`.

It matches `generator-manifest.json`, `/audit-input.json`, the trusted
preflight result, and an independent reconstruction of the conjunction.

## Stage 5 clean build, identity, and source gate

I created `/tmp/audit-work/stage5-clean-project`, copied the immutable
generated project into it as `Base`, and copied only candidate project/source
files around that base. I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, complete fresh build.

The fresh `Base` remains byte-for-byte at generated tree hash
`0f18c75c715f2d3f48706fe3f023557f4976b77fc0edf1eaa8f014f92a973d53`.
The trusted model-free candidate source gate passes. Each of the eight target
parameters has exactly one candidate definition. Candidate Lean sources
contain no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.
They neither define nor shadow `targetStatement`.

There is exactly one `Proof.final`, and its type is textually the exact fixed
instantiation:

`Klean90NextSmallest.Lemmas.targetStatement _List_ _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» ListItem notBool_ «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»`

Thus `Proof.final` is not a duplicated, weakened, or alternate theorem.

## Axiom accounting

Running Lean on `#print axioms Proof.final` in the fresh project reports 33
dependencies. Three are recorded Lean-standard trust:
`Classical.choice`, `propext`, and `Quot.sound`.

The other 30 all have exact entries in `trust-inventory.json`:

`Float2Int`, `Int2Float`, `Int2String`, float multiplication, float addition,
float subtraction, float division, float less-than, boolean equality, float
equality, K equality, string equality, float greater-or-equal, float
greater-than, float exponentiation, integer exponentiation, `absFloat`,
`absInt`, `binAcc`, `buildVS`, `ceilFloat`, `cntSub`, `floorFloat`,
`maxFloat`, `md5hexCodes`, `minFloat`, the generated root `nsScan`,
`rootFloat`, `sortKeyVS`, and `strToCodes`.

The reconciliation log records the exact encoded Lean declaration name,
source file, line, type, kind, and inventory reason for every one. The root
`nsScan` dependency is the recorded deterministic Klean definition repair in
generated rewrite infrastructure; it is distinct from the candidate's
`Proof.nsScan` target parameter, whose operational definition is audited
below. There is no `sorryAx` and no unrecorded axiom or proof trust escape.

## Operational-bridge audit

Every target parameter is bound by its exact manifest `kore_symbol` and by
`source_rule_ids = [rule-24e0...52cba]`. I compared each candidate definition
with that domain rule, the relevant K hook/constructor meaning in the supplied
semantics and generated model, the eight frozen `nsScan` definition rules,
and `solution.py`.

| Candidate parameter | Independent operational judgment |
|---|---|
| `_List_` | Calls the generated list-concatenation model and totalizes it with the same `left.coll ++ right.coll` result. It is ordered concatenation, not identity or a constant. |
| `_Map_` | Calls the partial disjoint K map union and uses the same union as fallback. The wrapper's list order is reversed, but K `Map` union is associative/commutative and the target's merges are disjoint: the internal frame keys are distinct and the freshness premise excludes location 1 from `SC`. It is extensionally the frozen K map meaning on the entire target domain. |
| `«_in_keys(_)_MAP_Bool_KItem_Map»` | Directly uses the generated finite-map membership model with `false` only as the impossible missing-option fallback. |
| `«_[_<-undef]»` | Directly uses generated finite-map key deletion, with the original map only as the impossible missing-option fallback. |
| `«_|->_»` | Directly constructs the singleton finite map `(key,value)`. |
| `ListItem` | Directly constructs a singleton K list. |
| `notBool_` | Directly uses the supplied K boolean-negation model and falls back to Lean boolean negation. |
| `nsScan` | A structural recursion exactly matching all eight frozen equations: the two terminal cases, initialization, new minimum, duplicate minimum, first second value, smaller second replacement, and preservation branch. Every recursive call consumes the tail. |

The independently retained Lean examples check list order; map singleton,
membership-present, membership-absent, deletion, and disjoint merge; singleton
list construction; both Boolean negations; terminal `nsScan` states; ascending
and unsorted inputs; duplicates; negative integers; and adversarial
noncanonical accumulator states that exercise new-minimum, new-second, and
preservation behavior. All examples compile.

I also rebuilt three isolated counterfactual projects:

1. Replacing `nsScan` by constant `noneV` fails the fixed proof at the returned
   value/`#pop` trace and later branch proofs.
2. Replacing `_Map_` by left identity fails singleton concatenation,
   function-frame construction, deletion, and the final trace.
3. Replacing map membership by constant `true`—the standard attack that would
   make the freshness premise impossible under honest `notBool_`—fails the
   candidate's semantic membership/deletion arguments.

These mutations are recorded exactly and all three builds exit 1. Together
with the source-level comparison, they show that the successful proof depends
on the actual operational bridges; it is not accepted through a constant,
identity, hard-coded, or vacuous implementation.

## Evidence index

The principal raw evidence is:

- `evidence/COMMANDS.md` and `evidence/00a-audit-context.log`;
- `evidence/01-producer-integrity-correct-algorithm.log` and
  `evidence/check_producer_integrity.py`;
- `evidence/02-inventory-reconstruction.log` and
  `evidence/reconstruct_inventory.py`;
- `evidence/06-stage4-preflight-rerun-success.log` and
  `evidence/run_stage4_preflight.py`;
- `evidence/07-stage4-integrity.log` and
  `evidence/check_stage4_integrity.py`;
- `evidence/08-stage5-fresh-copy.log`,
  `evidence/09-stage5-lake-clean.log`, and
  `evidence/10-stage5-lake-build.log`;
- `evidence/11-proof-final-axioms.log`,
  `evidence/12-axiom-reconciliation.log`,
  `evidence/AxiomAudit.lean`, and `evidence/reconcile_axioms.py`;
- `evidence/13-candidate-static-and-target.log` and
  `evidence/check_candidate_static.py`;
- `evidence/BridgeAudit.lean` and
  `evidence/14b-bridge-adversarial-examples-passing.log`;
- `evidence/15b-counterfactual-nsscan-diff.log`,
  `evidence/16-counterfactual-nsscan-constant.log`,
  `evidence/15c-counterfactual-map-diff.log`,
  `evidence/17-counterfactual-map-identity.log`,
  `evidence/18b-counterfactual-membership-diff.log`, and
  `evidence/19-counterfactual-membership-vacuity.log`;
- `evidence/20-final-consistency.log` and
  `evidence/final_consistency.py`.

The diagnostic failed attempts are also preserved:
`00-producer-integrity.log` (wrong aggregate-hash algorithm),
`03-stage4-preflight-rerun.log` and
`04-stage4-preflight-rerun-pinned-env.log` (sandbox `/proc` issue), and
`14-bridge-adversarial-examples.log` (first test-harness expectations). None
represents a candidate, provenance, or proof failure; the corrected checks and
their exact outputs are identified above.

VERDICT: PASS
LEGITIMACY: LEGIT
