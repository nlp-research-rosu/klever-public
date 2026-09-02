# Independent Stage 3–5 audit

## Scope and outcome

I audited HumanEval `136-largest-smallest-integers`, condition `bare`, with
`GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the signed launcher input record
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, all Stage 5 paths/hashes/results
are null, and no Stage 5 proof audit is applicable.

I treated the mounted workspaces, earlier audit, manifests, logs, and comments
as evidence only. I did not execute any instruction, script, or test supplied
by those artifacts. Audit-owned scripts and the explicitly trusted
`/reference/tools` modules performed the mechanical checks.

The classification and zero-obligation generation are legitimate. There is no
generated theorem, vacuous `True` substitute, Stage 5 candidate, or Lean proof
whose identity or axioms require reconciliation.

## Frozen-input and hash accounting

The launcher envelope's canonical resolution hash recomputes to
`c97c86ee64e3122898004af97d48cb6c087a1ac55b2cf45dd3b49eedbbc9de9a`.
The launcher and `/audit-output/audit-input.json` copies are byte-identical.

I independently reimplemented both tree-hash encodings, rather than merely
copying manifest values. The recomputed mounted hashes are:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 selected-artifact tree | `8043e15c6c6f41ca2165223e60059ec04572da90f59a8eed081c559383bc0bd9` |
| Stage 1 exporter tree | `00b6795e09cda2a090e4e7dab47413920e59489e3e5968bcb50769f4ec1a0c90` |
| Stage 2 selected-audit tree | `ac009aa1396e95724a308b6a533ab3d7045703dcc519547b9a942a855ec1e0f6` |
| Stage 3 discovery file | `2b94ff2eebda3d21f8ba4c4f46bf2b58e912c271402b841985b7240e46ec02a3` |
| Stage 4 selected-generation tree | `ed651f3ea12aac3b8acb79a1381adce6391b9c3e0dbe52d2497524930111c72a` |
| Generated project tree | `d3a3a5f900992e805887806c558b10a13b9fb56d388836e69c00172fb1f74765` |
| Frozen `verification.k` | `a54766e74afa56d501e8880c29aacebec2884555ba27c801af7a1bbb614859db` |
| Canonical rule inventory | `577e90b3e2ba59231529bb8ba7f67b95a7969f86d0f9e22e335605619797a3f9` |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `22cfa7b965c7fa5bfadf5bc9eef6eb502fea4368ccfdb37622364c6738ef330e` |

Every per-file Stage 1 digest was independently recomputed and the resulting
path-to-hash map exactly equals `stage1_source_hashes`. Both selected-artifact
hashes equal their selection records. All Stage 1, Stage 3, generated-tree,
obligation-map, trust-inventory, and toolchain bindings in the Stage 4
sidecars also match their mounted referents.

The generation manifest's `exporter_sha256` and `klean_py_sha256` identify
source in its separately recorded historical generator image; those source
preimages are not mounted. They are not hashes of the distinct audit-time
checker files in `/reference/tools`, and the trusted preflight correctly does
not conflate those scopes. Both historical values and the current audit-tool
hashes are preserved in `independent_checks.log`. Structural output is
independently revalidated below.

## Inventory reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. `prove.sh` selects module `VERIFICATION`. The trusted
local closure procedure finds exactly that module among the modules physically
defined in `verification.k`; imported operational module `MPY` is defined in
`semantic.k`, not as another local module in this file.

The canonical reconstruction contains 11 rules in source order. For every
entry I separately:

- sliced the frozen source at the reported inclusive line span and obtained
  byte-for-byte the inventory text;
- normalized whitespace and recomputed its SHA-256;
- recomputed `source_rule_id` as `rule-<normalized_sha256>`;
- checked uniqueness; and
- recomputed the canonical JSON inventory hash.

The protected Stage 3 manifest has exactly 11 unique identities in exactly the
same order. There are no omitted, duplicated, additional, unknown, or reordered
rules. Its inventory hash is the reconstructed
`577e90b3e2ba59231529bb8ba7f67b95a7969f86d0f9e22e335605619797a3f9`.

Since each `source_rule_id` is `rule-` followed by the listed normalized hash,
the complete reconstructed inventory is:

| # | Frozen span | Normalized SHA-256 | Independent class |
|---:|---:|---|---|
| 1 | 15 | `f399d8c5d55f049f32bfc0bd71b072990832b797cd2cb42f6179b783046534cf` | `DEFINITION` |
| 2 | 16–17 | `9b3b29557dda868e08cfdf72056753b24c58ed6d469ddf14e2186b89b0e3ea1c` | `DEFINITION` |
| 3 | 18 | `19cf10e725a5d97d562b52cd3a5fe1591b678d5bcc7a6d1940b2a8f004377ed6` | `DEFINITION` |
| 4 | 19–20 | `24cf846bf9c77cc8a105ef4f25e62da61cd8bd53da78040bc17fd0123d8e08dd` | `DEFINITION` |
| 5 | 22–26 | `d7ba05b7723c98a5a29344e98acb2fad66722b3cf5375329b30adb9afdaab7ef` | `DEFINITION` |
| 6 | 27 | `8edcdf9ff6c7e0e0546a377adca014bf2f167b722725bd5f18085acfd42a4a2e` | `DEFINITION` |
| 7 | 28–32 | `1a4cc923c3fb70c9d37d91d1cffd19876a7de71476fc86a021051ea28b8131c3` | `DEFINITION` |
| 8 | 34–38 | `3ae79becbba60cc8588c454974ca8d38e698a8209a85ee19fa8148db09158b0a` | `DEFINITION` |
| 9 | 39 | `6092bce027b3d36ec09884b15ec16c4c4e794c506d5b662bf468880fd537e36a` | `DEFINITION` |
| 10 | 40–44 | `d1456be43b700a0307264d0eecf8cf5db5851c6cbc6d8a3e55395d73aa60db76` | `DEFINITION` |
| 11 | 47–67 | `1eea429ae87f08a6a57848039abc4bbe4591ac006ff0969311d6da7d48604f0b` | `DEFINITION` |

All reconstructed rule-attribute lists are empty. In particular, there is no
`simplification` rule to which the stricter classification restriction must be
applied.

## Independent classification judgment

Rules 1–4 are the empty and nonempty recurrence equations for the named
`#negFold` and `#posFold` summaries. Rules 5–10 are the defining step and
candidate equations called by those recurrences. Their left-hand sides are
fresh summary/helper symbols declared as total K functions; they do not match
or replace an executing `<k>` configuration. They are definitions, not
ordinary operational rules or standalone mathematical facts.

Coverage and overlap are sound:

- each fold covers the disjoint `nil` and `icon` constructors and recurses on
  the strict tail;
- each candidate helper covers the disjoint `pyNone` and `pyInt` constructors;
- each step uses a total Boolean conditional;
- negative values choose the larger negative integer, positive values choose
  the smaller positive integer, and zero changes neither accumulator.

Rule 11 expands `solutionProgram`, whose syntax declaration is a macro, into
the exact translated program AST. It is a macro/named proof term and does not
skip execution of the function body. The AST initializes both sentinels,
iterates over `lst`, performs the two sign tests and extremum updates, and
returns the tuple in the same order as frozen `solution.py`.

The operational semantics confirms the definitions' relevance and meaning:
`iterateIntSeq` binds heads in order, executes both `If` statements, then
recurses on the tail. The comparison rules preserve operand order for `<` and
`>`, `is None` distinguishes the sentinel, assignments update the environment,
and the final return evaluates the tuple. The Stage 1 loop claim connects that
exact execution to `#negFold` and `#posFold`; it does not turn their defining
equations into domain lemmas.

As an independent sensitivity check, an audit-owned oracle compared the direct
operational algorithm with the fold equations on all 3,906 sequences of
length 0–5 over `{-2,-1,0,1,2}`, including empty, zero-only, duplicate,
order-sensitive, sign-boundary, and mixed cases. There were zero mismatches.
Counterfactually changing negative selection from maximum to minimum produced
1,540 mismatches (first witness `[-2,-1]`); changing positive selection from
minimum to maximum also produced 1,540 mismatches (first witness `[1,2]`).
This finite check is sensitivity evidence; the source/semantic analysis above
is the classification basis.

There is no `OPERATIONAL_RULE` in the local verification-file closure; the
ordinary execution rules live in frozen `semantic.k`. There is no
`PROVED_DERIVED_LEMMA`: none of the 11 entries has a proof-first,
module-without-rule, later-use history. There is no `DOMAIN_LEMMA`: every entry
introduces/fixes a summary, recurrence, helper, macro, or named proof term.
Thus the protected partition—11 definitions and empty operational,
proved-derived, and domain sets—is correct.

## Deterministic Stage 4 generation

I directly reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1 workspace, Stage 3 manifest, selected generation, and trusted
toolchain lock. The first launcher attempt exposed an audit-sandbox
PID-namespace incompatibility in Lean's executable-path lookup. Its complete
failure is retained. I used the audit-owned `proc_exe_compat.c`, which changes
only `/proc/<digits>/exe` readlink requests to `/proc/self/exe`; it neither
changes the project nor bypasses Lean elaboration. The same trusted function
then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- Stage 1 hash
  `00b6795e09cda2a090e4e7dab47413920e59489e3e5968bcb50769f4ec1a0c90`;
- Stage 3 hash
  `2b94ff2eebda3d21f8ba4c4f46bf2b58e912c271402b841985b7240e46ec02a3`;
- generated-tree hash
  `d3a3a5f900992e805887806c558b10a13b9fb56d388836e69c00172fb1f74765`;
- 47 allowlisted non-propositional generated trust declarations;
- `lake clean` exit 0 with empty output; and
- `lake build` exit 0 with output hash
  `830e27a137e8df217daf93ff10a991550ab4383fe6af8473b11dcc81c0846668`.

The fresh returned JSON equals both
`/reference/klean-generation/preflight.json` and the signed
`stage4_preflight` object exactly, including diagnostics.

The Stage 4 input manifest reproduces all 11 definitions and has empty
`operational_rules`, `proved_derived_lemmas`, and domain `source_rules`. The
generated `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Consequently the source-rule/obligation map is an exact empty bijection. There
are no omissions, duplicates, irrelevant obligations, weakened formulas, or
vacuous conjuncts. The expected target definition is absent, trusted
`target_statement` returns null, and the generator manifest and signed audit
input also bind target null. Generating no target—rather than a theorem of
`True`—is the correct fixed result for a genuinely empty independently
classified domain set.

## Stage 5 disposition

This audit is not in proof mode. The selected no-obligation generation
correctly has no generated target and no `/candidate`. No `Proof.final`,
candidate definitions, target parameters, or candidate axioms exist to build
or reconcile. Running a Stage 5 proof workflow would contradict the signed
classification-only mode.

## Evidence

Raw commands, outputs, the full reconstructed inventory, all per-rule checks,
hash checks, preflight return value, preflight comparison, runtime compatibility
shim, and operational sensitivity results are under `/audit-output/evidence/`.
`evidence/COMMANDS.md` is the command index.

VERDICT: PASS
LEGITIMACY: LEGIT
