# Independent audit: `155-even-odd-count`

## Result

Stage 3 classification and Stage 4 deterministic generation are sound. The
Stage 5 project also clean-builds, proves the exact generated target, and has
an acceptable axiom list. Nevertheless, Stage 5 is not legitimate because one
of its eleven required operational bindings does not implement the frozen K
symbol to which it is bound:

```lean
def «_%Int_» : SortInt → SortInt → SortInt := Int.emod
```

The bound KORE symbol is `Lbl'UndsPerc'Int'Unds'`, whose frozen declaration is
hooked to `INT.tmod`, not Euclidean modulo. On the adversarial input
`(-11, 10)`, frozen K returns `-1`, while the candidate returns `9`. The
generated obligations only use this operation under positive guards, where
the two operations agree, so the clean proof does not expose the mismatch.
The requested audit policy explicitly makes such a total operational-bridge
mismatch a `FAIL`/`NOT_LEGIT`.

## Audit binding and producer identity

The launcher document and environment both select
`CLASSIFICATION_AND_PROOF`. The signed resolution hash recomputes to
`b9c59e47d193276c81b5a6b34dc22756c64259564932be235f7880e38bfa395f`.

Before judging generation, I hashed the preserved producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match the source manifest and generator manifest. The immutable
generator image ID
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
also matches the source manifest, generator manifest, and the image-derived
producer-source path recorded by the launcher. The complete producer tree
hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
There is no producer-source infrastructure error.

The mounted Stage 1, Stage 2, Stage 4, and Stage 5 tree hashes, the Stage 1
export digest, all 803 frozen Stage 1 file hashes, the discovery file hash,
and the generated project digest all match their mounted records. The
launcher records a hash for the original Stage 5 invocation directory, but
that invocation directory is not part of the mounted audit interface; the
mounted selected Stage 5 workspace itself was independently verified.

Relevant raw evidence:

- `evidence/07-producer-identity-verdict.txt`
- `evidence/54-independent-recorded-hash-verification.txt`
- `evidence/75-post-build-source-immutability-corrected.txt`
- `evidence/76-audit-input-resolution-hash.txt`

## Stage 3: inventory reconstruction and classification

I ran the trusted local rule-inventory implementation over the frozen
`/reference/k-proof/verification.k`. Its local verification-module closure is
exactly `VERIFICATION`; no imported operational semantics modules are
mistakenly counted as local verification rules.

The independent reconstruction produced:

- frozen `verification.k` SHA-256:
  `972347fb2f5c1ac10251f295a40ccf9464fea383405626cd87346aff804e6516`;
- 24 rules;
- inventory SHA-256:
  `b2fb8d2f080192ac639ab57ac9b211ee836bb2e63f89b4d157059d4ffc931fe2`.

For every rule I recomputed the source span, normalized source hash, and
`source_rule_id`. The reconstructed and protected inventories have the same
24 ordered identities. Both sides have unique identities, and there are no
omissions, extras, duplicated rules, reordered identities, changed spans, or
changed hashes.

My independent classification is:

- rules 0–13: 14 `DEFINITION` entries;
- rules 14–23: 10 `DOMAIN_LEMMA` entries;
- no `OPERATIONAL_RULE`;
- no `PROVED_DERIVED_LEMMA`.

The definitions consist of the named translated body and closure, the base
and totalizing equations for `evenPos`/`oddPos`, and the public summary
equations for `decEven`/`decOdd`. The ten domain lemmas are proposition-to-
`#Top` proof simplifiers: two public zero facts, four absolute-value/public-
summary normalization equalities, and four one-step decimal recurrences in
both equality orientations.

Stage 1 does not first prove any of those ten exact rules against a module
that omits them. Its proofs import `VERIFICATION`, which already contains the
rules, so none qualifies as a proved derived lemma. The separately proved
loop bridge is outside the frozen local inventory and does not change that
classification.

All rules carrying `[simplification]` are either definitions or domain
lemmas. Every domain lemma is relevant: the zero and absolute-value facts
connect the public postcondition to the totalized summaries, and the decimal
recurrences close the loop step corresponding to the source updates and
division by ten.

The protected Stage 3 classifications agree entry-for-entry with this
independent result.

Relevant raw evidence:

- `evidence/09-reconstructed-rule-inventory.json.log`
- `evidence/12-inventory-bijection.txt`
- `evidence/13-operational-semantics-and-stage1-use.txt`
- `evidence/70-independent-classification-table.txt`

## Stage 4: deterministic generation and mathematical adequacy

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the three required mounted inputs. It returned `PASS` with ten
obligations, no designated sorries, and a successful generated-project clean
build.

The rerun required a narrow environmental workaround. This audit sandbox
hides `/proc/<pid>/exe` from the PID-isolated Lean process, while pinned Lean
4.22 uses that path to locate itself. I compiled an auditable `readlink`
shim that redirects only `/proc/<digits>/exe` to `/proc/self/exe`. Its source,
binary hashes, and behavior are recorded in
`evidence/46-proc-exe-shim-test.txt`. It changes neither audited source nor
theorem content.

The independently checked Stage 4 bijection is exact:

- independent true-domain set: 10 unique ordered rule IDs;
- `source_rules`: the same 10 unique ordered IDs;
- `obligations`: the same 10 unique ordered IDs;
- generated target: exactly 10 textually unique conjuncts;
- every conjunct hash, rule span, normalized hash, and source text matches;
- the obligation-map hash and generated tree hash match the manifests.

The reverse-orientation equalities are not accidental duplicates: they have
different source-rule IDs, different conjunct hashes, and preserve the two
separately frozen K rules.

The fixed target is:

- declaration:
  `Klean155EvenOddCount.Lemmas.targetStatement`;
- definition hash:
  `1b3125aa6574304838e19004df800355d6a96a1f8ad1262817dcc3614b591446`;
- applied-statement hash:
  `64f32e5bf396b4786df83e6b17fe3992fc262c5abfd98180547f2a1b7cd488eb`;
- generated-project digest:
  `dbbc2d3db666269bdecc295225b44133e1f219d873e1cac19df1673ee79c0f7d`.

Those values match the generator manifest, copied generated project, and both
target records in `/audit-input.json`. The obligations preserve the exact
zero guards, absolute-value links, recurrence guards, arithmetic expressions,
and equality orientations from the ten frozen domain lemmas. None is
irrelevant, weakened, omitted, duplicated, or itself vacuous under the honest
operational meanings.

`evidence/55-independent-obligation-bijection.txt` contains an initial local
parser mistake involving an outer parenthesis. The corrected independent
check is `evidence/56-independent-obligation-bijection-corrected.txt`, where
all bijection assertions pass. Similarly, a manually transcribed expected
digest in evidence 59 had a typo; `evidence/60-fresh-project-integrity-correction.txt`
compares the copied tree directly with both authoritative records and passes.

Relevant raw evidence:

- `evidence/47-check-generation-rerun-success.txt`
- `evidence/48-generated-obligations-and-bindings.txt`
- `evidence/56-independent-obligation-bijection-corrected.txt`
- `evidence/72-candidate-integrity-and-target-identity.txt`

## Stage 5: clean build, target identity, and axioms

I created the fresh project
`/tmp/audit-work/lean-stage5.lgIu0B`, copied only the candidate source and
project configuration into it, and copied the generated project contents into
`Base`. The copied `Base` digest exactly matches the fixed generated-project
digest.

In that project:

- `lake clean` exited 0;
- `lake build` exited 0;
- `Proof.lean` remained byte-identical to `/candidate/Proof.lean`;
- copied generated sources remained byte-identical to the mounted generated
  project after the build.

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`; it does not declare or shadow `targetStatement`. It has exactly one
`theorem final`, and its statement is exactly the fixed generated target with
the eleven candidate bindings. The trusted final mechanical gate also
returned `PASS`.

The exact Lean output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are the three Lean core logical axioms explicitly accepted by the
trusted final gate. `Proof.final` uses none of the 45 Klean-generated
trust-inventory axioms. There is no `sorryAx` and no unrecorded axiom.

Relevant raw evidence:

- `evidence/61-fresh-lake-clean.txt`
- `evidence/62-fresh-lake-build.txt`
- `evidence/63-proof-final-axioms-and-type.txt`
- `evidence/64-trusted-final-gate.txt`
- `evidence/73-proof-axiom-reconciliation.txt`

## Stage 5: operational bridge

I located exactly one candidate `def` for every `target.parameters` entry and
recomputed all eleven binding hashes. Ten definitions implement their frozen
meanings:

| Binding | Candidate implementation | Frozen meaning | Judgment |
|---|---|---|---|
| `_-Int_` | `Int.sub` | `INT.sub` | pass |
| `_>Int_` | `decide (a > b)` | `INT.gt` | pass |
| `_==Int_` | `a == b` | `INT.eq` | pass |
| `_%Int_` | `Int.emod` | `INT.tmod` | **fail** |
| `_+Int_` | `Int.add` | `INT.add` | pass |
| `_/Int_` | `Int.tdiv` | `INT.tdiv` | pass |
| `absInt` | `Int.ofNat n.natAbs` | `INT.abs` | pass |
| `decEven` | zero special case plus magnitude count | frozen lines 48–50 | pass |
| `decOdd` | zero special case plus magnitude count | frozen lines 52–54 | pass |
| `evenPos` | recursive even-digit magnitude count | frozen summary and recurrence | pass |
| `oddPos` | recursive odd-digit magnitude count | frozen summary and recurrence | pass |

The `%Int` discrepancy is not a naming ambiguity:

1. The target parameter is bound to the exact KORE symbol
   `Lbl'UndsPerc'Int'Unds'`.
2. Frozen `verification-kompiled/definition.kore` declares that symbol with
   `hook{}("INT.tmod")`.
3. Frozen `semantics/int.k` implements Python `%` separately as
   `pyMod(I1,I2) => ((I1 %Int I2) +Int I2) %Int I2`. Thus raw `%Int` is
   intentionally the truncating primitive used to construct Python modulo;
   it is not itself `pyMod`.
4. A direct K evaluation using the same `INT.tmod` hook gives:

   ```text
   <k>
     -1 ~> .K
   </k>
   ```

   for `-11 %Int 10`.
5. Evaluating the candidate binding gives:

   ```text
   ("emod(-11,10)", 9)
   ```

The candidate proof succeeds because the generated recurrence assumes
`N > 0`, and the relevant remainders have positive divisors; `Int.emod` and
`Int.tmod` coincide there. That makes the target unable to distinguish this
incorrect total binding. An additional counterfactual test proves the whole
target with dishonest always-false guard functions, confirming mechanically
that theorem construction alone cannot establish the operational bridge.

The digit-summary definitions themselves survived zero, positive, negative,
mixed-digit, and large decimal examples. Constant, identity, wrong-modulo,
and wrong-division mutations were rejected by concrete witnesses. Those
successful checks do not cure the `%Int` failure.

Relevant raw evidence:

- `evidence/65-operational-bridge-examples.txt`
- `evidence/66-operational-bridge-counterfactuals.txt`
- `evidence/69-direct-k-tmod-evaluation.txt`
- `evidence/71-target-parameter-operational-bridge-table.txt`

## Final judgment

The Stage 3 classification and Stage 4 generation are legitimate, and the
Stage 5 Lean theorem is structurally and logically clean. However, the
candidate's `Int.emod` definition changes the total operational meaning of
the exact frozen `%Int` KORE symbol. Under the required operational-bridge
rule, that single mismatch is dispositive.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
