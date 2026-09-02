# Independent Stage 3–5 audit: `141-file-name-check`

## Scope and conclusion

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF` for condition `kit-semantics`, with
`SUPPLIED_SEMANTICS`. I treated the frozen workspaces, manifests, candidate
source, logs, and earlier review as untrusted evidence. The trusted inventory,
preflight, frozen-toolchain gate, clean Lean builds, and final mechanical gate
were rerun; the semantic classification and operational bindings were judged
independently.

The protected Stage 3 classification is correct, Stage 4 has exactly one
relevant and faithful obligation, and the Stage 5 candidate proves the exact
fixed target with honest definitions for both K integer comparison parameters.

## Producer provenance gate

This gate passed before Stage 4 was judged.

- Observed `klean_export.py` SHA-256:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- Observed `klean.py` SHA-256:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Those values exactly match both `source-manifest.json` and
  `generator-manifest.json`.
- The producer bundle contains exactly those two regular, non-symlink source
  files plus `source-manifest.json`.
- Its trusted tree hash is
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
  matching `/audit-input.json`.
- The source manifest and generator manifest both record immutable image
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
  the same digest is the final component of the producer-source path recorded
  by `/audit-input.json`.

Evidence: `evidence/00-producer-sha256.txt` and
`evidence/01-producer-provenance.json`.

## Rule inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen `/reference/k-proof`. It selected module `VERIFICATION`; its local
verification-file import closure contains no second local module. The
reconstructed inventory has five rules in source order:

| Span | Normalized SHA-256 / `source_rule_id` suffix | Independent class | Reason |
|---|---|---|---|
| 9–99 | `3af6834c5d265aaa932ee4a8d6e9c27217a407ae8d47026f5f3bded39d1d39bc` | `DEFINITION` | Expands the `[macro]` proof term `fileNameCheckBody` to the exact translated function body. It defines syntax and does not observe or shortcut runtime state. |
| 103–113 | `090cffa7fcdc5ffc47356048225b8e0752c4c5eb3eee496ad6a1f6c758c90243` | `DEFINITION` | Exhaustively defines `decimalDigitCount` as the sum of ten fixed `cntSub` summaries. |
| 116–120 | `bbf7cf0b4fb369fbc48c61958bcbe40df6c243afe391fe598d557324862e89c4` | `DEFINITION` | Defines `fileExtensionIs` by fixed slicing and equality operations. |
| 123–126 | `359a1379ae7cf0fd25d119b9d40416cdee51f7a8b2a512b81c012bdf386f8523` | `DEFINITION` | Defines `allowedFileExtension` as the disjunction of the three named extension summaries. |
| 128–130 | `62d1bbd5b25d2b70152e85917d8c17ce8f2ed86c82cce542d4527216437bc22c` | `DOMAIN_LEMMA` | The guarded simplification `N >Int 3 => false requires N <=Int 3` is a mathematical fact about hooked integer order, not a definition or operational rule. |

Every `source_rule_id` is `rule-` followed by the listed normalized hash. The
whole canonical inventory hash is
`0ebb6d2902488cbd08d9a03c06d8a8d5707b37278af455cb56c373e3c0899f2b`.
The protected manifest contains the same five unique IDs in the same order and
the same whole-inventory hash. Trusted contract validation found no omission,
duplicate, extra rule, reordered identity, changed source span, or changed
hash.

There are four definitions, no ordinary operational rules, no
`PROVED_DERIVED_LEMMA`, and one domain lemma. Although the arithmetic rule is
independently provable, its role in `verification.k` is still a material
`[simplification]` fact about the problem domain, so `DOMAIN_LEMMA` is the
required classification.

The domain lemma is relevant. The source program branches on total decimal
digit count `> 3`; the valid-name claims assume that same summary is `<= 3`.
The rule connects that precondition to execution of the program's final
comparison. A fresh Haskell definition compiled only from the supplied MPY
semantics—not from `verification.k`—proved the exact claim in `lemma-spec.k`
with `#Top` and exit 0. The supplied K declarations bind `<=Int` to
`hook(INT.le)` and `>Int` to `hook(INT.gt)`.

Evidence: `evidence/02-rule-inventory.json`,
`evidence/14-fresh-semantics-kompile.log`,
`evidence/15-domain-lemma-kprove.log`, and
`evidence/16-semantic-bridge-source-excerpts.txt`.

## Recorded hashes

Independent recomputation matched the audit input for:

- Stage 1 workspace tree:
  `13be97e90ef91ef0219be39088a8c9ce009faa6d1cd48c0b1e6948370ce18105`;
- Stage 1 deterministic-export tree:
  `92f922bf6bf82d07a661f72e3412925b79d0a44fef51953ac62879021cc5e10b`;
- discovery manifest:
  `52c6ae86789acd6064c2bb6669ba17e3362a7af89b98ce2efb52200de550d8f3`;
- selected K audit tree:
  `31e86c8b5baabfd72beb55cd27964ad0290a128cc32dac41d5e349c44ed99061`;
- Stage 4 generation tree:
  `c023875863741aa6fd45aa3c5654f4ec2fba7d7cf0cc8db96ebf55c6dd663a90`;
- producer-source tree:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`;
- generated Lean tree:
  `253baec828b67e5af662ba61acb16997e706dd2094dc92c0acaa452caad7c43b`;
  and
- candidate Lean workspace tree:
  `9e446c4b555a54eb4a0a49377bebcac5e756afce507c1dd2942196561745f23a`.

The exact 783-entry Stage 1 source-file hash map also matches. The launcher
records a Stage 5 invocation hash, but that invocation directory is not among
the mounted audit inputs; the mounted candidate workspace, its source, and its
fresh rebuild were all checked directly.

Evidence: `evidence/05-all-recorded-hashes-pass.json` and
`evidence/18-key-file-hashes.txt`.

## Stage 4 structural and mathematical judgment

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen K workspace, protected discovery manifest, selected generation, and
pinned toolchain lock. It returned `PASS`, obligation count 1, zero designated
sorries, and successful clean/build diagnostics.

The audit sandbox initially prevented Lean's `/proc/<pid>/exe` application-path
lookup, causing Lake to report that it could not detect its installation.
The pinned binaries themselves were present. I used the preserved
`evidence/app_path_shim.c`, which intercepts only `readlink`/`readlinkat` for
the current process executable and returns the kernel `AT_EXECFN` value. With
that narrow environment accommodation, the frozen-toolchain gate reported:
K 7.1.293, pyk/Klean 7.1.293, Lean 4.22.0, and Codex 0.144.6. The shim does not
change project files, Lean declarations, elaboration rules, or proof terms.

The independent Stage 4 check established all of the following:

- The sole `DOMAIN_LEMMA` is the sole `source_rules` entry in both the input
  manifest and obligation map.
- The one obligation carries the same unique source ID, lines 128–130,
  normalized hash, inventory hash, and discovery hash.
- Its conjunct is exactly
  `∀ (N : SortInt) (h : («_<=Int_» N 3) = true), («_>Int_» N 3 : SortBool) = false`.
- Its conjunct SHA-256 is
  `77067df640631be73782a5a17d411d3d0152a3808ea255b0fb94e941c2661a21`.
- The obligation-map file SHA-256 is
  `e7f35007e9d6abc9d81aa11f19ff6a3948727188cb792e1ec7797ec5bfd52c85`,
  matching the generator manifest.
- The generated definition is exactly the conjunction constructed from that
  map, with definition hash
  `eaafc3e2b8799bcf920f8b720a7575692463f6d909bb0a8ddbe6267015dc529c`.
- The applied target statement hash is
  `8615a7d37765570e8f83dff4eba28cb41f4cdeb69475f956b01aed98474d6d18`.
- The observed target object exactly matches the generator manifest, Stage 4
  preflight recorded in the audit input, and audit-input target.

The obligation is neither weakened nor irrelevant: it preserves the exact
guard, left-hand comparison, constant 3, and Boolean result of the K rule. It
is nonvacuous—for example, `N = 3` satisfies the guard—and it is needed to
relate the valid-name claim partition to the source program's `> 3` branch.
There are no omitted, duplicate, extra, or vacuous conjuncts and no target
change. Because the true domain set has one entry, `KLEAN_NO_OBLIGATIONS` would
have been invalid; the selected status is correctly `PASS`.

Evidence: `evidence/03-preflight-sandbox-failure.log`,
`evidence/03-toolchain-shim-gate.txt`,
`evidence/04-generation-preflight.json`, and
`evidence/06-stage4-integrity-pass.json`.

## Stage 5 clean build, target identity, and source policy

I created `/tmp/audit-work/lean-audit.Bncwtt`, copied only the candidate's
root proof/project files into it, and copied the immutable generated project
from Stage 4 as `Base`. That fresh Base has generated-tree hash
`253baec8...ad7c43b`. From the fresh project:

- `lake clean` exited 0;
- `lake build` exited 0 and built `Proof`;
- the only warning was the generated target's unused hypothesis linter;
- candidate `Proof.lean` contains no `sorry`, `admit`, `unsafe`, `axiom`, or
  `opaque`;
- there are no candidate trust declarations and no shadowing
  `targetStatement`;
- each required parameter has exactly one candidate `def`; and
- `Proof.final` is declared exactly once with the fixed generated target, not
  a copied, weakened, or independently restated proposition.

`#check` printed:

```text
Proof.final : Klean141FileNameCheck.Lemmas.targetStatement Proof.«_>Int_» Proof.«_<=Int_»
```

The trusted full final gate independently repeated the Stage 4 preflight,
replaced the candidate Base with the selected generated tree, clean-built the
proof, checked its type, parsed its axiom set, verified all bound input hashes,
and returned `PASS` in `CLASSIFICATION_AND_PROOF` mode.

Evidence: `evidence/07-fresh-project-files.txt`,
`evidence/08-lake-clean.log`, `evidence/09-lake-build.log`,
`evidence/10-candidate-source-check.json`, and
`evidence/13-trusted-final-gate.json`.

## Axiom accounting

The exact Lean output is:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. The generated trust inventory has 58 declarations, but
none is a dependency of `Proof.final`. `propext` is one of the three explicit
Lean core allowances in the trusted final gate (`propext`,
`Classical.choice`, and `Quot.sound`); the other two are not used. There is no
candidate axiom/opaque declaration and no unrecorded dependency.

Evidence: `evidence/11-print-axioms-and-final.log` and
`evidence/17-axiom-reconciliation.json`.

## Operational-bridge audit

Both target parameters are bound to the sole source rule
`rule-62d1...bc22c`.

| Parameter | Manifest KORE symbol | Candidate definition | Frozen operational meaning | Judgment |
|---|---|---|---|---|
| `«_>Int_»` | `Lbl'Unds-GT-'Int'Unds'` | `def «_>Int_» (x0 x1 : SortInt) : SortBool := x0 > x1` | K symbol `_>Int_`, total `hook(INT.gt)`; MPY dispatches source `">"` comparisons to it. | Exact |
| `«_<=Int_»` | `Lbl'Unds-LT-Eqls'Int'Unds'` | `def «_<=Int_» (x0 x1 : SortInt) : SortBool := x0 <= x1` | K symbol `_<=Int_`, total `hook(INT.le)`; this is the source rule's guard. | Exact |

The generated types make `SortInt` Lean `Int` and `SortBool` Lean `Bool`, so
Lean and K both use unbounded mathematical integers here. The generated
Prelude independently represents the same hooks as `some (x0 > x1)` and
`some (x0 <= x1)`; the target parameters intentionally expose their total
Boolean values without the generated `Option` wrapper.

Adversarial checks passed for greater-than and less-or-equal at `(4,3)`,
`(3,3)`, `(-100,3)`, and `(9223372036854775808,3)`, covering true, false,
equality, negative, and beyond-machine-word cases.

Counterfactuals were material:

- a constant-false greater-than definition still proves the generated
  conditional equation, but differs from the frozen hook at `(4,3)`;
- a reversed less-or-equal definition differs at `(4,3)` and `(-100,3)`.

Thus clean theorem closure alone would not have established the operational
bridge. The submitted definitions are not constant, identity, hard-coded, or
vacuous: both use both arguments and are exactly the two bound K hooks. The
candidate proof then correctly derives that `N <= 3` rules out `N > 3`.

Evidence: `evidence/12-operational-bridge-checks.log` and
`evidence/16-semantic-bridge-source-excerpts.txt`.

## Final judgment

All classification, deterministic-generation, target-identity, proof,
trust-boundary, and operational-bridge obligations pass. The transparent
application-path shim was needed only because of audit-sandbox process-path
visibility and did not alter the theorem or proof environment.

VERDICT: PASS
LEGITIMACY: LEGIT
