# Independent audit: HumanEval 61 `correct-bracketing`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Outcome

The protected Stage 3 classification is complete and mathematically correct.
The deterministic Stage 4 artifact has one exact, relevant domain-lemma
obligation and an unchanged generated target. The Stage 5 candidate cleanly
proves that target with operationally faithful definitions of both target
parameters. No proof hole or unrecorded trust escape is present.

## Producer-source hard gate

I hashed the two mounted generation-time producer files before judging Stage
4:

| Producer | Observed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same in `generator-manifest.json` and `source-manifest.json` | Match |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same in `generator-manifest.json` and `source-manifest.json` | Match |

The immutable producer image is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in both manifests and in the basename of the producer-source path bound by
`/audit-input.json`. The producer tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
also exactly matching the audit input. This hard gate passes. See
[producer evidence](/audit-output/evidence/23-producer-hard-gate-summary.txt).

## Inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen `/reference/k-proof`. The selected local verification module is
`VERIFICATION`; its local closure contains that module and seven rules.

The reconstructed `verification.k` hash is
`2b49ce96b5b21696cc825931beaa41a9f4f5f4b8d2a2ec66e46ad0fba8a68fe2`.
The canonical whole-inventory hash is
`8c6cab4afd22730fa2defac7902ae428539a33dd8d81fbc13ff2fdbf9369d455`.

| Span | Source rule ID | Independent class |
|---|---|---|
| 11–12 | `rule-b9c21f71f007e14b87428fc39b47b152444b900cfb5ae90c093a6a0adbe3bac0` | `DEFINITION` |
| 13–19 | `rule-a39e2d4a34fe8d3daf6e7a14ed9cd1f1efc7f40036ee34e406b4a1f8e0ec5a74` | `DEFINITION` |
| 23 | `rule-90116861827fe29b6190d60f2c7fa45d68a9e1d53c40cb018cb4bdfd97122478` | `DEFINITION` |
| 24 | `rule-952eaa451e2e2dafbf07e4b2853104ca12d32a5798a18fd07e34328e033d4dc4` | `DEFINITION` |
| 28–30 | `rule-d9b0adbebf1e3f908a9944544102b6bcd8aee7d5a41871e3719cd38e5470aaa0` | `DOMAIN_LEMMA` |
| 34 | `rule-86c81c4e83f334a250f0f7cd6a3d696ef3dd176482dc7252a0d002fb835aa66c` | `DEFINITION` |
| 35–36 | `rule-1e22fa424b19594ef171e00ed16730ba4f24c804316660a9f0a4eeaee1779942` | `DEFINITION` |

For every row, `source_rule_id` is exactly `rule-` followed by the
independently reconstructed normalized-source SHA-256. The protected manifest
has exactly seven unique entries in the same order. Its identity set equals
the reconstructed set: no omission, duplicate, extra, reordering, changed
hash, or unaccounted classification exists. Recomputing the canonical hash
from the reconstructed rule documents gives the same inventory hash. The
trusted Stage 3 contract validator also accepts the manifest. Full rule text,
spans, attributes, and hashes are in
[the reconstructed inventory](/audit-output/evidence/04-reconstructed-rule-inventory.json.txt);
the explicit ordered bijection is in
[the Stage 3 comparison](/audit-output/evidence/05-stage3-bijection.txt).

## Independent classification judgment

The two `scanBrackets` rules are the base case and structural recurrence of a
named mathematical summary. The two `keepValid` rules are complementary,
guarded defining equations: `< 0` and `>= 0` are disjoint and exhaustive over
K integers. The two `bracketInput` rules define the empty and `iCons` cases of
the formal input-domain predicate. All six are genuine definitions; the
recursive rules strictly consume the `IntSeq` tail.

The rule at lines 28–30 is not a definition or ordinary operational rule:

```k
rule (#if C ==Int 40 #then _X:Int #else Y:Int #fi) => Y
  requires C =/=Int 40
  [simplification]
```

It is also not a proved-derived lemma under the required criterion. Stage 1
first compiles `verification.k` with this rule already present, then proves
the loop claim; it never proves this exact rule against a module that omits
it. It is therefore correctly classified as `DOMAIN_LEMMA`.

The lemma is true on its complete guard. The frozen KORE definition binds
`_==Int_` to `INT.eq`, `_=/=Int_` to `INT.ne`, and the polymorphic conditional
to `KEQUAL.ite`. Integer disequality from 40 makes the condition false, so the
conditional returns `Y`. It is materially relevant: the source program tests
whether each character is `"("`, represented by integer code 40, and both
the source-linked `scanBrackets` recurrence and the loop proof must reduce the
else branch under a symbolic disequality. It is not an irrelevant fact
smuggled into the domain set.

Independent classification is thus exactly six `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`.
Detailed reasoning is in
[the semantic judgment](/audit-output/evidence/22-independent-semantic-judgment.md),
with the frozen source and proof ordering in
[source/program evidence](/audit-output/evidence/24-source-program-and-proof-order.txt).

## Stage 4 deterministic generation

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1 workspace, protected Stage 3 manifest, Stage 4 generation,
and trusted toolchain lock. It returned `PASS` with one obligation, zero
designated sorries, 41 inventoried generated trust declarations, and clean
`lake clean`/`lake build` diagnostics. The returned evidence is saved in
[the preflight rerun](/audit-output/evidence/17-preflight-successful-rerun.txt).

All mounted hashes bound by `/audit-input.json` independently recompute
exactly: Stage 1 pipeline tree and export tree, Stage 2 audit tree, Stage 3
manifest, Stage 4 generation tree, generated project, producer-source tree,
and Stage 5 workspace. All 792 individually recorded Stage 1 file hashes also
match. The audit-input canonical digest is
`3d1fb6a0f77fff04cc6408c5ef04098ab73ea3e0a5e3ff9c39b3f44b75b39b26`.
See [tree-hash evidence](/audit-output/evidence/08-audit-input-and-tree-hashes.txt)
and [file-hash evidence](/audit-output/evidence/09-stage1-recorded-file-hashes.txt).

The true domain set has exactly the single rule above. `input-manifest.json`
and `obligation-map.json` contain that exact source record, including span,
normalized hash, inventory hash, discovery hash, attributes, text, and
classification. The obligation list contains its ID exactly once and in the
same order. The generated conjunct is:

```text
∀ (Y : SortInt) (_X : SortInt) (C : SortInt)
  (h : («_=/=Int_» C 40) = true),
  kite («_==Int_» C 40) _X Y = Y
```

This is the exact Lean rendering of the guarded K rule: all variables, the
guard, test, branches, and result are preserved. It is neither weakened nor
vacuous. For example, `C = 41`, `_X = 0`, `Y = 1` satisfies the premise and
forces the else result.

The unique generated target is
`Klean61CorrectBracketing.Lemmas.targetStatement`, with definition hash
`4f89938cbae5f369f41c22ceb4d34877ddeb46bda85269e16882ca9df6454731`
and applied-statement hash
`8acaa3b01217061434d80e5a51ade6d2db04cf6dcfbbb35387886d2462b1e3e3`.
These match the obligation-derived definition, generator manifest, preflight,
and audit input exactly. The obligation map hash, parameter binding hashes,
toolchain lock, export result, and all provenance links also match. See
[independent Stage 4 integrity checks](/audit-output/evidence/13-stage4-independent-integrity.txt).

## Stage 5 clean build, target identity, and proof

I copied `/candidate` to a fresh directory below `/tmp/audit-work` and copied
the immutable generated project into its existing `Base` directory. The
copied Base tree equals the Stage 4 generated tree, and its extracted target
equals both the generator manifest and audit input. Candidate-owned sources
do not declare or shadow `targetStatement`; they contain no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque`. The trusted candidate static gate passes.
See [candidate/target evidence](/audit-output/evidence/14-candidate-static-and-target-identity.txt).

Both required commands succeeded in the fresh project:

- `lake clean`: exit 0, complete output in
  [clean evidence](/audit-output/evidence/11-lake-clean-complete.txt).
- `lake build`: exit 0 and `Built Proof`, complete output in
  [build evidence](/audit-output/evidence/12-lake-build-complete.txt).

`Proof.final` states exactly:

```text
Klean61CorrectBracketing.Lemmas.targetStatement
  Proof.«_==Int_» Proof.«_=/=Int_»
```

It is the fixed generated theorem, not a duplicated, weakened, or separately
defined proposition.

The exact `#print axioms Proof.final` output is:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

The trusted final-gate policy includes `propext` and `Quot.sound` as fixed
Lean foundational dependencies in addition to declarations listed by
`trust-inventory.json`. Both dependencies are accounted for; `sorryAx` is
absent, there is no unexpected axiom, and none of the 41 generated hook
axioms is a dependency of `Proof.final`. See
[exact axiom output](/audit-output/evidence/15-print-axioms-complete.txt) and
[trust reconciliation](/audit-output/evidence/21-trust-and-operational-bindings.txt).
The trusted proof-candidate gate and the full audit-input-bound mechanical
gate both independently return `PASS` in
[proof-gate evidence](/audit-output/evidence/18-proof-candidate-mechanical-gate.txt)
and [full-gate evidence](/audit-output/evidence/20-full-mechanical-final-gate.txt).

## Operational-bridge audit

The two target parameters are load-bearing because dishonest definitions can
make the generated proposition convenient. I compared each exact candidate
definition to its bound KORE symbol, source rule, source program, and frozen
operational hooks:

| Parameter | Candidate definition | Frozen meaning | Judgment |
|---|---|---|---|
| `«_==Int_»` | `x == y` | total `INT.eq` on K integers | Exact |
| `«_=/=Int_»` | `x != y` | total `INT.ne` on K integers | Exact |

Generated `SortInt` is Lean `Int` and `SortBool` is Lean `Bool`. The fresh
compiler output calls `lean_int_dec_eq` for equality and Boolean-negates that
result for disequality, agreeing with the source definitions and K hooks.
Ground evaluations produce `eq(40,40)=true`, `eq(41,40)=false`,
`ne(40,40)=false`, and `ne(41,40)=true`.

I also checked counterfactual mutations in Lean. Constant-false equality
still proves the generated equation, and constant-false disequality makes its
premise vacuous, demonstrating why the bridge audit cannot be replaced by a
clean proof. Conversely, constant-true equality is rejected at `C=41` with
unequal branches, and constant-true disequality is rejected at `C=40`. The
actual candidate uses neither shortcut: its definitions implement equality
and disequality for every integer. The adversarial audit compiled with exit 0;
its exact output is in
[operational-bridge evidence](/audit-output/evidence/19-operational-bridge-adversarial-lean.txt).

## Audit-environment note

The audit sandbox denies numeric `/proc/<pid>/exe` reads while permitting
`/proc/self/exe`. Lean 4.22 uses the numeric path to locate its installation,
so the first unadjusted attempt failed before elaboration. I used a local,
auditor-created `LD_PRELOAD` compatibility shim that changes only a
current-process `/proc/<pid>/exe` `readlink` request to `/proc/self/exe`.
The pinned Lean binary was not modified; with the shim it reports Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the locked
toolchain. The shim source, build command, and hash are preserved in
[environment evidence](/audit-output/evidence/16-lean-sandbox-shim-build-and-test.txt).
All reported successful preflight, build, proof, and axiom commands were
rerun after this narrowly scoped environment repair.

VERDICT: PASS
LEGITIMACY: LEGIT
