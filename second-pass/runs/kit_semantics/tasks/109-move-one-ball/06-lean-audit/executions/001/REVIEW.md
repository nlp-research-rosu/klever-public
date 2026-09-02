# Independent audit: 109-move-one-ball

## Conclusion

I independently audited Stage 3, deterministic Stage 4, and the Stage 5 Lean
proof for `109-move-one-ball`, condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. `/audit-input.json` and `AUDIT_MODE` both select
`CLASSIFICATION_AND_PROOF`.

The protected classification is complete and mathematically correct: the local
verification-module closure contains ten definitions and two relevant domain
lemmas. Stage 4 generates exactly one obligation for each of those two domain
lemmas and fixes their conjunction as the immutable target. The candidate
clean-builds, proves exactly that target, has no forbidden trust escape, and
supplies operationally faithful implementations on the complete domains used
by the obligations. I found no omitted rule, false classification, weakened
obligation, target substitution, or convenient operational stub.

## Input and producer authentication

The signed audit envelope recomputes to
`1025a14d54554d1ad0d9559e466bf842f99aea0d2e4e167e8032a0bc155b302f`.
I recomputed every hash for the mounted Stage 1, Stage 2, Stage 3, Stage 4,
producer-source, and Stage 5 inputs. This included all 791 individually
recorded Stage 1 files. All mounted pipeline-tree hashes, both export-tree
hashes, and the Stage 3 file hash match `/audit-input.json`.

Before judging Stage 4, I hashed the two generation-time producers:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match `source-manifest.json` and `generator-manifest.json`. The
source manifest and generator manifest also agree on immutable image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the image digest is the exact basename of the launcher-recorded producer-source
path. The producer-source tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also matching the launcher. Producer authentication therefore passes; there is
no infrastructure `AUDIT_ERROR`.

## Inventory reconstruction

I invoked the trusted local rule-inventory implementation directly on
`/reference/k-proof`. The selected verification module is `VERIFICATION`, and
its local closure is exactly `["VERIFICATION"]`. The frozen `verification.k`
hash is
`29c13d56bb1a0389e75163a4716014d73960a7f4948324dd782562b04e588524`.

For every rule I independently extracted the recorded line span, normalized
the exact source with whitespace joining, recomputed its normalized SHA-256,
and reconstructed `source_rule_id` as `rule-<normalized SHA-256>`. All 12
checks pass. Canonical hashing of the ordered reconstructed records gives
inventory hash
`e7581c4cdd2c4847747f0d1386bc17857b25c08874b12a090a6be0c32116955b`.

The protected Stage 3 manifest has exactly the same 12 unique identities in
the same order and records the same inventory hash. Thus there are no omitted,
extra, duplicated, reordered, or hash-changed rules.

## Independent classification

My classifications, based on the frozen source and its operational role, are:

| Span | Source rule ID | Classification | Independent reason |
|---|---|---|---|
| 11–15 | `rule-2113f0fdc2009228980618182d1e8b1e9cbb2b4e997089fa8e3b9265644d811b` | `DEFINITION` | `[macro]` expansion naming the exact loop-body AST |
| 18–30 | `rule-a954c7fce79d3cc622c51dd0a87db8553231b26de3aaa807968ebbf55e3e4381` | `DEFINITION` | `[macro]` expansion naming the exact function-body AST |
| 34 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | `allInts` base equation |
| 35 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | `allInts` constructor recurrence |
| 39–42 | `rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d` | `DOMAIN_LEMMA` | guarded sort-refinement fact for operational `applyCmp`, marked `[simplification]` |
| 47 | `rule-4e59619ad0d5e4c817fce319f536d37391f7c43783f89757495c9ed16530e409` | `DEFINITION` | `scanDrops` base equation |
| 48–53 | `rule-bd22b95ff27fa507ace8a55b23e07960d0ba7af1765c6c5a6c75faeb33a2aeee` | `DEFINITION` | guarded `scanDrops` recurrence defining the loop fold |
| 57 | `rule-2fcb91a07fe018ada596c62b5c013251f64fc0c3817612c4f480cbc51f49374f` | `DEFINITION` | `lastAfter` base equation |
| 58 | `rule-f7986d4c0e6a22445baeea69ebcde91b805f9c0d364d6d60d917b74a2ab2005f` | `DEFINITION` | `lastAfter` constructor recurrence |
| 60–63 | `rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1` | `DOMAIN_LEMMA` | guarded sort-refinement fact for comparison with `lastAfter`, marked `[simplification]` |
| 68–69 | `rule-5c07cca7fdc014be55b52c0e209519d4b57df23c2b7d0323cd179fcd59f76d32` | `DEFINITION` | empty-input equation for the named `moveSpec` summary |
| 70–76 | `rule-5277cf06d6a112559474beb63e50a1eced34870a71610af9bc1b31a081414e17` | `DEFINITION` | nonempty all-integer equation for the named `moveSpec` summary |

The macro rules name exact source proof terms. The remaining definition rules
are base equations or recurrences for named predicates and summaries. They are
not ordinary execution rules and do not assert free-standing mathematical
facts about an already defined operational symbol.

The two `applyCmp` rules are different. They do not define `applyCmp`; the
supplied semantics already dispatches a source comparison to that function and
defines integer `<` as K integer order. These rules add guarded mathematical
sort-refinement facts to the proof theory, so `DOMAIN_LEMMA` is the correct
class. Both are relevant: line 39 supports each `current < previous` loop
comparison, while line 60 supports the final circular `first < previous`
comparison after `previous` is summarized by `lastAfter`. These are exactly
the comparisons used by the frozen program and postcondition.

Neither rule qualifies as `PROVED_DERIVED_LEMMA`. `prove.sh` first compiles
`verification.k`, including both rules, into `verification-kompiled`; every
subsequent `kprove` uses that already extended module. There is no prior proof
of either exact rule against a module that omits it. No inventory entry is an
`OPERATIONAL_RULE`. Both and only both `[simplification]` rules are
`DOMAIN_LEMMA`, satisfying the simplification restriction.

This independently yields the same Stage 3 counts: 10 `DEFINITION`, 2
`DOMAIN_LEMMA`, 0 `OPERATIONAL_RULE`, and 0 `PROVED_DERIVED_LEMMA`.

## Deterministic Stage 4 audit

With `PYTHONPATH=/reference`, I reran
`tools.klean_preflight.check_generation` on the frozen Stage 1 workspace,
protected discovery manifest, and selected Stage 4 generation. It returned
`status: PASS`, `obligation_count: 2`, and `trust_declaration_count: 42`.
Its clean/build commands both exited 0. The rerun build-output hash
`10ca7252253b5cc1b0e625ddd64b1c9251d8707b7fcaf00a5d19a51235f5a935`
is identical to the generation-time recorded output hash.

The normal pinned Lean executable could not recover `IO.appPath` in this
audit sandbox because the sandbox blocks its `/proc/.../exe` lookup. I
preserved those failures. For the successful rerun I used a temporary view of
the pinned Lean 4.22 toolchain in which only the two same-length self-path
string literals were redirected to auditor-owned symlinks; the Lean libraries,
kernel logic, project sources, and every generated input remained the pinned
ones. The output-identical Stage 4 rebuild, independent target hashing, fresh
proof rebuild, and separate final gate all agree. Evidence 10–32 records the
diagnosis and the narrow compatibility shim; evidence 33 is the successful
required preflight result.

The independently reconstructed true domain set is nonempty and has exactly
the two rule IDs above. Stage 4 correctly has status `OK`, not
`KLEAN_NO_OBLIGATIONS`.

The source-rule list and obligation list form an ordered, duplicate-free
bijection:

1. For arbitrary `A` and `B`, if both are integer values, operational
   `applyCmp("<", A, B)` equals integer order on their projections.
2. For arbitrary `A`, `P`, and `VS`, if `A` and `P` are integer values and
   every element of `VS` is an integer, operational
   `applyCmp("<", A, lastAfter(P, VS))` equals integer order on the corresponding
   projections.

Those are exact encodings of source spans 39–42 and 60–63. The nested Boolean
guard in the second obligation preserves K's parsed association. Each
obligation's source ID, span, normalized hash, inventory hash, discovery hash,
and Lean-conjunct hash recomputes. Their guards are satisfiable—for example,
injected integers satisfy the first, and an integer seed with `[4, -2]`
satisfies the second—so neither conjunct is vacuous.

All seven target-parameter binding hashes recompute, every binding refers only
to the two exact source obligations, and their union covers both obligations.
The obligation-map raw hash is
`9e5a8d3f598cc362dc7d310b59781b73bb02768970d7b444aa561742d2471f76`.
The generated export-tree hash is
`159d35045ec9fd551774ca169ba660a0f57639022cdd975f6de8bf09c9993256`.

The single fixed target is
`Klean109MoveOneBall.Lemmas.targetStatement`, and it is the exact conjunction
of those two mapped obligations. Its hashes are:

- statement:
  `f92275cba75daf6423a698d8599a2df3b3aceff0bfae9bc0b7fa6d6f7566b11a`
- definition:
  `c5d254fb9807d6d0b71d4442b0eeb72d8bd72fefa7ea01457c7dd5cbce99f190`

The target recomputed from `Lemmas.lean` is structurally identical in the
generator manifest, recorded Stage 4 preflight, `/audit-input.json`, and the
fresh Stage 5 `Base`. There is no omission, extra obligation, target change,
weakening, duplication, or irrelevant conjunct.

## Stage 5 proof and target identity

I made a fresh project at `/tmp/audit-work/fresh-proof-2`, copied the selected
generated project into it as `Base`, and copied the candidate proof project
around it. The candidate `Proof.lean`, `lakefile.lean`, and `lean-toolchain`
hashes were unchanged. The copied `Base` retained export-tree hash
`159d35045ec9fd551774ca169ba660a0f57639022cdd975f6de8bf09c9993256`.

`lake clean` exited 0. `lake build` exited 0 and built the generated Prelude,
Sorts, Inj, Lemmas, and `Proof`. An earlier discarded setup attempt copied the
generated directory one level too deep (`Base/generated`) and consequently
could not resolve the Base package; evidence 38 preserves that auditor setup
mistake, while evidence 39 contains the correctly shaped, successful clean
build required for the verdict.

The candidate does not declare or shadow `targetStatement`, and it declares
exactly one `Proof.final`. Its type is the fixed generated target applied to
the seven candidate definitions. Recomputed target identity in fresh `Base`
matches the manifest and audit input exactly. The proof constructs the exact
two-conjunct target: it first proves the guarded integer `applyCmp` equation,
then proves by recursion that `lastAfter` preserves the integer property on an
`allInts` sequence, and uses those facts for the second conjunct. It does not
prove a copied, weakened, or vacuous variant.

A case-insensitive scan of the candidate project found no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`.

## Axiom accounting

Running Lean on:

```lean
import Proof
#print axioms Proof.final
```

produced exactly:

```text
'Proof.final' depends on axioms: [propext]
```

The generated trust inventory contains 42 named Klean trust-boundary axioms;
none is in `Proof.final`'s dependency closure. `propext` is one of the
mechanical gate's fixed Lean foundational allowances
(`Classical.choice`, `propext`, and `Quot.sound`), rather than a candidate or
generated declaration. The dependency is therefore explicitly accounted for.
There is no `sorryAx` and no unexpected or unrecorded proof escape. The trusted
final candidate gate independently repeated the clean build and type/axiom
check and returned `status: PASS` with `used_axioms: ["propext"]`.

## Operational-bridge audit

I compared every target parameter to its `kore_symbol`, bound source-rule IDs,
frozen verification rules, source program, and supplied K semantics:

| Candidate definition | Operational judgment |
|---|---|
| `_andBool_` (`Proof.lean:6`) | Lean `left && right` is exact K Boolean conjunction. |
| `«_<Int_»` (`Proof.lean:8`) | `decide (left < right)` is exact mathematical/K integer strict order, including negative and equal cases. |
| `isInt` (`Proof.lean:10–12`) | Returns true exactly for the singleton K sequence containing an injected `SortInt`; other represented K terms return false. This matches the sort guard used by both rules. |
| `«allInts(_)_VERIFICATION_Bool_ValSeq»` (`Proof.lean:14–18`) | Empty is true; a constructor checks the head with `isInt` and recurses on the tail, exactly matching lines 34–35. |
| `«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»` (`Proof.lean:20–34`) | All six integer comparison cases agree with `int.k` lines 22–27. In particular, the complete matched domain of both bound obligations fixes operator `<` and integer operands, where the definition is exact. Its fallback only totalizes cases outside those guarded obligations; it is neither used nor claimed as semantics for other source domains. |
| `«lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq»` (`Proof.lean:36–40`) | Empty returns the seed; a constructor advances the seed to the head and recurses, exactly matching lines 57–58. |
| `«project:Int»` (`Proof.lean:42–44`) | Returns the integer from exactly the guarded singleton integer injection. The `0` fallback totalizes the Lean function outside K projection's defined/guarded domain and is unreachable in both obligations. |

The source program accepts lists of integers, counts each strict adjacent
descent, adds the circular comparison between the first and final elements,
and tests whether the count is at most one. The Stage 1 claim has the matching
`allInts(VS)` domain. Thus the bridge domain is aligned with the source
contract; no float, string, collection, malformed K term, or non-integer
projection is silently admitted by the generated theorem.

I added independent Lean witnesses for true and false Boolean conjunction,
negative/equal integer order, integer and non-integer `isInt`, empty/all-int/
mixed `allInts`, true and false integer `applyCmp`, empty/nonempty `lastAfter`,
and defined-domain projection. I also defined adversarial counterfactuals:
constant implementations for all Boolean/integer/predicate/comparison/
projection parameters and an identity implementation of `lastAfter`. Lean
proved concrete inequalities separating every counterfactual from the
candidate implementation. The audit file typechecked with exit code 0; its
evaluated witnesses include `allInts [4,-2] = true`,
`allInts [4,true] = false`, `applyCmp("<",-2,9) = true`,
`lastAfter(99,[4,-2]) = -2`, and `project:Int(7) = 7`.

These checks rule out a constant, identity, hard-coded-result, vacuous, or
otherwise convenient operational bridge on the complete obligation domains.

## Evidence index

Raw commands, source excerpts, results, and audit scripts are under
`/audit-output/evidence/`. The principal records are:

- `02-producer-authentication.txt`: producer source and image authentication
- `04-reconstructed-inventory.json.txt`: trusted reconstructed inventory
- `05-stage1-source-and-stage3-manifest.txt`: frozen source, claims,
  classifications, and Stage 1 proof order
- `10`–`32`: pinned Lean `IO.appPath` sandbox diagnosis and compatibility shim
- `33-rerun-check-generation-success.txt`: required Stage 4 preflight result
- `34-generated-obligations-and-manifests.txt`: exact obligations, target, and
  trust inventory
- `35-candidate-source-inspection.txt`: candidate definitions and forbidden
  token inspection
- `37-exact-operational-bridge-semantics.txt`: supplied K operational rules
- `39-fresh-proof-clean-build-success.txt`: correct fresh clean build
- `40-print-axioms-proof-final.txt`: exact direct axiom output
- `41-operational-bridge-adversarial-lean.txt`: semantic and counterfactual
  Lean tests
- `42-independent-integrity-checks.py` and
  `43-independent-integrity-checks-output.txt`: 59 independent integrity
  checks, all passing
- `44-trusted-final-candidate-gate.txt`: repeated final mechanical gate
- `45-axiom-reconciliation.txt`: explicit dependency reconciliation

VERDICT: PASS
LEGITIMACY: LEGIT
