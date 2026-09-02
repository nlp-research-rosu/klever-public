# Independent Stage 3–5 Audit: HumanEval 124-valid-date

## Scope and result

This audit covers condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. Both
`AUDIT_MODE` and the signed `/audit-input.json` resolution say
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; the audit input binds no Lean workspace or invocation,
`stage5_result` is null, and `/candidate` is absent. Consequently the Stage 5
proof, axiom, final-theorem, and operational-parameter checks are not applicable
and were not performed.

I treated every candidate/provenance narrative, old log, comment, and prior
verdict as untrusted evidence. The findings below come from the frozen source,
the trusted inventory/preflight implementations, fresh hashing, direct semantic
inspection, and a fresh preflight run.

## Producer provenance gate

The required generation-time sources are present as exactly three regular
files: `klean_export.py`, `klean.py`, and `source-manifest.json`. Fresh SHA-256
values are:

| Producer file | Observed SHA-256 | Generator/source manifests |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | match |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | match |

`source-manifest.json` and `generator-manifest.json` both bind generator image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
The basename of the launcher-recorded `generation_producer_sources` path is the
same image digest. The producer bundle's fresh pipeline tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching `/audit-input.json`. The producer provenance gate therefore passes;
there is no infrastructure `AUDIT_ERROR`.

## Frozen-input integrity

The signed audit envelope verifies with recomputed canonical digest
`6e6812672a87c81ba021eb34cdb7742839f51054ad3b352ab3ed365e0564f8a3`.
Fresh hashes agree with every non-Lean artifact/source binding in the signed
resolution:

| Binding | Observed and recorded SHA-256 |
|---|---|
| Stage 1 K workspace artifact | `881d79411ad7ab81a95e6fcfa47a4ebe04295354a139b9c787909c3b308f0180` |
| Stage 1 deterministic export | `b39714014c6857a733694c0cae5cffd66485b768998fb8b0432bfc875e0c95b8` |
| Stage 2 audit artifact | `bc593422e47d09f211ae3e2da4bb0ae969ef12d055ef906db9c58bb0a628d31f` |
| Stage 3 discovery manifest | `32d52cfdbb4ece2bcc1496d4e59c4b26bc93fc385fb13b2ccbe6d9d55f5e9507` |
| Stage 4 generation artifact | `b5e18ed7bf36112a72d40a98ead741c196d0ac1edfdaff7e3e28d907cb655210` |
| Generated project tree | `fca67d8c880040a1a2d653bcfbd2d7b52edeedac6ee618842ce89566fef07a17` |
| Producer-source bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |

All 787 launcher-recorded Stage 1 regular-file source hashes were independently
recomputed: the path sets and counts agree and there are no missing, extra, or
mismatched files. The Lean workspace/invocation hashes are correctly null in
classification-only mode.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference` tree against `/reference/k-proof`. The selected local verification
module is `VERIFICATION`; its local-module closure contains only
`VERIFICATION`. Imports such as `MPY`, `INT`, and `BOOL` are supplied by the
separately frozen semantics and are not locally defined modules in
`verification.k`.

The reconstruction contains exactly five rules in source order:

| # | Source span | `source_rule_id` / normalized SHA-256 | Attributes | Independent class |
|---:|---|---|---|---|
| 1 | 12–166 | `rule-415033600c05a74b967858910de7e6f137b7072cad657a6ac7aa4017632c1851` | none | `DEFINITION` |
| 2 | 171–171 | `rule-95075d83a0bfc357491c9ebdd73471597f5d3d7efa19b7eed607a527de6e57c6` | none | `DEFINITION` |
| 3 | 174–184 | `rule-213d2e3601b35f7d452f718a58bb49a80abbaf99a4343a8c4ba60f3309dc0cbd` | none | `DEFINITION` |
| 4 | 187–188 | `rule-d8a4e28b9a30919ceb03d02944cfc337efe8eb8e81474a454172b2d68b6bf2aa` | none | `DEFINITION` |
| 5 | 190–206 | `rule-000f1433c33376dfa1807ad42ebb0d8821bd71fb57e744c08fcbe1308f5d50cf` | none | `DEFINITION` |

For every entry, the exact physical source span equals the inventory text. A
fresh normalization (`" ".join(text.split())`) and SHA-256 recomputation equals
the recorded normalized hash, and prefixing it with `rule-` reproduces the
identity. The IDs are unique. The canonical ordered inventory hash is
`1e1e11bd9e60b6563190fbf01074626066c574d662f30b073201e87b2c31a316`.

The Stage 3 manifest contains exactly the same five unique identities in the
same order, all classified as `DEFINITION`, and commits the same canonical
inventory hash. That hash commits the complete reconstructed documents,
including spans, text, normalized hashes, and attributes. Thus a changed span,
text, normalized hash, or order would fail either the inventory hash or ordered
identity comparison. There are no omitted, duplicated, extra, reordered, or
unaccounted rules. The deterministic Stage 4 input manifest also contains the
same full five definition records.

## Independent classification judgment

1. `validDateProgram` is a `DEFINITION`. Its locally declared nullary
   `[function, total]` symbol expands to a `Module(...)` source AST. Removing
   whitespace from the independently translated `solution.mpy` and from the
   extracted rule RHS produces identical token streams. The rule does not
   match a `<k>` cell, call, continuation, state cell, or any other operational
   configuration. It names the exact source proof term; fixed MPY semantics
   still performs module loading, lookup, argument evaluation, call/frame
   control, body execution, and return.

2. `asciiDigit(C)` is a `DEFINITION`. It names the Boolean predicate
   `48 <= C <= 57`, exactly the range tested after `ord(character) - 48` in the
   source program.

3. `validMonthDay(M,D)` is a `DEFINITION`. It names the three disjoint calendar
   cases: February through day 29; months 4/6/9/11 through day 30; and months
   1/3/5/7/8/10/12 through day 31. It asserts no equality about an executed
   program result.

4. The guarded `validDateResult(CS) => false` rule is the non-length-10 clause
   of a summary definition. Its guard is `isLen(CS) =/=Int 10`.

5. The length-10 `validDateResult` rule is the complementary summary clause.
   It defines the expected result using the two hyphen positions, ASCII-digit
   checks for all eight digit positions (including all four year positions),
   decimal month/day construction, and `validMonthDay`. Its guard is
   `isLen(CS) ==Int 10`. The two guards are exhaustive and non-overlapping.

The summary symbols occur only in their local declarations/definitions and in
the Stage 1 specification; they do not occur in the supplied MPY operational
semantics. No inventory LHS is an ordinary execution/observation rule, no rule
is a derived theorem, and no rule has a `simplification` attribute. Therefore
there is no disguised operational bridge, unproved derived lemma, or
simplification rule requiring `DOMAIN_LEMMA` classification.

Direct branch-by-branch inspection shows that `validDateResult` is relevant and
matches both the frozen source solution and the HumanEval postcondition. As
finite corroboration only, an independent source-branch evaluator and formula
evaluator agreed on 11,251 boundary/adversarial strings. Counterfactuals were
sensitive as expected: changing February's bound to 28 disagrees on
`02-29-2000`; omitting the year-digit check changes `03-11-20a0`; omitting the
separator check changes `03/11/2000`. These tests support, but do not replace,
the direct semantic classification.

The independently determined true domain-lemma set is therefore genuinely
empty. This agrees with Stage 3.

## Deterministic Stage 4 judgment

I reran the required function
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and trusted toolchain lock.

The default first attempt was preserved because it exposed an audit-sandbox
issue: Lake could not discover its installation. This sandbox unshares the PID
namespace while its `/proc` mount lacks `/proc/<getpid()>/exe`; Lean 4.22 uses
that path for `IO.appPath`, although `/proc/self/exe` is available. The final
rerun used a recorded compatibility library that redirects only a
`/proc/*/exe` `readlink` to `/proc/self/exe`, plus the frozen Lean sysroot. It
does not rewrite generated input, alter Lean declarations, or change proof
logic. Its source and binary hashes are recorded in the evidence.

The checker then ran both internal commands successfully:

```text
lake clean: exit 0, empty output
lake build: exit 0
✔ [2/9] Built Klean124ValidDate.Prelude
✔ [3/9] Built Klean124ValidDate.Sorts
✔ [4/9] Built Klean124ValidDate.Inj
✔ [5/9] Built Klean124ValidDate.Lemmas
✔ [6/9] Built Klean124ValidDate.Func
✔ [7/9] Built Klean124ValidDate.Rewrite
✔ [8/9] Built Klean124ValidDate
Build completed successfully.
```

The returned evidence is `KLEAN_NO_OBLIGATIONS`, with zero obligations, zero
designated sorries, 41 generated executable trust declarations, and target
null. Its clean/build output hashes exactly equal those in the launcher-recorded
preflight.

Independent manifest checks also pass:

- `verification.k` hash is
  `1da0585e487943e4d702e5199d11b41c8f4c6ea7d510963e2fede6e50fa7ce4c`.
- `obligation-map.json` hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching the generator manifest.
- `trust-inventory.json` hash is
  `68f7ec1b2865683b1d722d2eed2c67ae77673066c4d7eb79d474f512a824497d`,
  matching the export result.
- The independently empty domain-ID list, Stage 3 domain-ID list, input
  manifest `source_rules`, obligation-map `source_rules`, and obligation IDs
  are all exactly the same empty ordered list. There are no omissions,
  duplicates, irrelevant/weak obligations, or vacuous conjuncts.
- Obligation counts are zero in the generator manifest, export result,
  recorded preflight, fresh preflight, and actual obligation map.
- The generated target is null in the generator manifest, recorded preflight,
  audit resolution, and audit-input preflight snapshot. The generated
  `Lemmas.lean` contains only an empty namespace, not a target theorem.

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is mathematically
appropriate rather than merely self-consistent. There must be no Stage 5 proof,
and the signed null Stage 5 bindings plus absent `/candidate` satisfy that
requirement.

## Evidence index

- `evidence/01_provenance_commands.sh` and
  `evidence/01_provenance_results.txt`: producer identity, all signed artifact
  and Stage 1 source hashes, and signed-envelope verification.
- `evidence/02_inventory_commands.sh` and
  `evidence/02_inventory_results.txt`: canonical reconstruction, per-rule span
  and hash recomputation, ordered bijection, and source-AST comparison.
- `evidence/03_preflight_initial_failure.txt`: preserved initial environment
  failure.
- `evidence/03a_compat_diagnosis.sh`,
  `evidence/03a_compat_diagnosis_results.txt`, and
  `evidence/lean_app_path_compat.c`: PID-namespace diagnosis and the narrowly
  scoped compatibility mechanism.
- `evidence/03_preflight_commands.sh` and
  `evidence/03_preflight_results.txt`: exact required checker invocation,
  complete clean/build output, and returned evidence.
- `evidence/04_stage4_integrity_commands.sh` and
  `evidence/04_stage4_integrity_results.txt`: independent sidecar hashes,
  source/obligation bijection, counts, target nullity, and Stage 5 absence.
- `evidence/05_classification_commands.sh` and
  `evidence/05_classification_results.txt`: frozen source/spec/rules, symbol-use
  search, boundary examples, and counterfactual mutations.

VERDICT: PASS
LEGITIMACY: LEGIT
