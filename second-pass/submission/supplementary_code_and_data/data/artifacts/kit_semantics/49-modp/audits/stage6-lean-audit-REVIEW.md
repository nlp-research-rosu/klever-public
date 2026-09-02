# Independent Stage 3–5 audit: HumanEval `49-modp`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. The selected
Stage 4 status is `KLEAN_NO_OBLIGATIONS`; consequently, Stage 5 is absent and
no Lean proof candidate is in scope.

The no-obligation result is legitimate. The frozen `verification.k` contributes
no rules at all to its local verification-module closure, so its true set of
domain lemmas is empty. The protected Stage 3 classification exactly records
that empty inventory. Stage 4 maps the empty domain set bijectively to an empty
obligation set and generates no target theorem. No candidate directory or
Stage 5 result exists.

## Input and producer integrity

The signed `/audit-input.json` envelope validates with resolved-input digest
`7942f72086e4bb416b83fa0d3e38b8ec0e8a615849a41021e32717abce3a3e27`.
I recomputed every launcher-recorded tree/file digest with the trusted hashing
implementations. All recorded values matched, including:

- Stage 1 pipeline tree:
  `76bcaa09aede4b10e7bbced2697a6c16fe6901259bb42bbf92a99938cc31d5e2`;
- Stage 1 Klean tree:
  `4058cd7591e8bcc0849d7ca7bd5c0006a55ee6a34befc73562e827639b191472`;
- protected discovery manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`;
- selected Stage 4 generation:
  `9756480ede55863f5a44f15b736c54d8471013a034dd33fbbfc58c5b01cfee57`;
- generated project:
  `011f41791d8cd13268a3a2cb243458b4e57fd187cfd40410893417ca37172b1d`;
  and
- producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

The audit input lists 771 Stage 1 regular files. The mounted workspace also has
771 regular files; there are no missing, extra, or hash-mismatched entries.

The mandatory producer-source gate passes. The actual files hash to:

| Producer | Actual SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Those values exactly match both `source-manifest.json` and
`generator-manifest.json`. The immutable image ID
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
is identical in the source manifest, generator provenance, and the basename of
the launcher-recorded producer-source path. The bundle has exactly the two
producer files plus its source manifest. There is therefore no producer-source
infrastructure error.

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. It selected module `VERIFICATION`; its local closure in
the frozen `verification.k` is just `VERIFICATION`. The file is five lines:
it requires the supplied semantics, declares `VERIFICATION`, imports fixed
module `MPY`, and ends the module. It contains no `rule` sentence and no
`simplification` attribute.

The reconstructed canonical inventory is:

- verification SHA-256:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- ordered rules: `[]`; and
- canonical inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The protected `/reference/lemma-discovery.json` has the same inventory hash and
the same empty ordered rule list. Thus the bijection has no omissions,
duplicates, extras, reordering, changed identities, changed normalized hashes,
changed source spans, or unaccounted classifications. Because there are no
entries, the independently reconstructed sets of `DEFINITION`,
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, and `DOMAIN_LEMMA` entries are all
empty. The simplification constraint also holds vacuously because there are no
simplification rules.

This is not an empty classification hiding a mathematical shortcut. The source
body is exactly `return 2 ** n % p`, translated as nested `BinOp("**", ...)`
and `BinOp("%", ...)`. The K claim starts from the actual bound closure and
returns `pyMod(2 ^Int N, P)` under `N >=Int 0` and `P =/=Int 0`. The supplied
semantics executes this through ordinary name lookup, callee and argument
evaluation, parameter binding, strict binary-operator dispatch, the guarded
integer exponentiation rule, the integer modulo rule, return, and frame pop.
The guards make exponentiation and modulo defined. No rule in
`verification.k` preempts, summarizes, bridges, or adds a mathematical fact to
that execution. Therefore no source-relevant domain lemma exists to export.

## Deterministic Stage 4 judgment

I independently reconciled every Stage 4 sidecar:

- `input-manifest.json` has no definitions, operational rules, proved-derived
  lemmas, summary functions, or source rules;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- the generator manifest, export result, stored preflight, and obligation map
  all report obligation count zero;
- the obligation-map file hash and trust-inventory file hash match their
  manifests;
- the generator toolchain object exactly matches
  `/reference/klean-toolchain.lock.json`; and
- the audit input, generator manifest, stored preflight, generated source, and
  independent target parser all agree that the target is `null`.

The exact source-rule/obligation identity lists are therefore:

| Set | Ordered IDs |
|---|---|
| reconstructed inventory | `[]` |
| independently classified domain lemmas | `[]` |
| Stage 4 input source rules | `[]` |
| obligation-map source rules | `[]` |
| generated obligations | `[]` |

This is an exact empty-to-empty bijection. There are no obligations that could
be irrelevant, weakened, duplicated, omitted, or vacuous, and there is no
generated target whose statement could have changed. `Lemmas.lean` contains
only an import, a comment, and an empty namespace. The generated generic
prelude's 41 non-propositional collection-hook trust declarations are recorded
in `trust-inventory.json`; with no proposition, obligation, or target, they do
not establish or weaken any theorem in this audit.

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three mandated inputs. The sandbox hides `/proc/<current-pid>/exe`, which made
the pinned Lean runtime initially fail to locate itself. I recorded the two
failed environment attempts and used a narrow preload shim that redirects only
that hidden proc path to the available `/proc/self/exe`. The shim is preserved
in the evidence directory. It does not modify any frozen input, generated
source, manifest, theorem, or trusted checker.

With the pinned Lake/Lean environment restored, `check_generation` exited zero.
Its returned evidence reports `KLEAN_NO_OBLIGATIONS`, obligation count zero,
`target: null`, matching Stage 1, discovery, and generated-tree hashes, no
designated sorry, and successful `lake clean` and `lake build`. The build-output
SHA-256 is
`4dfaf2f757c816d50fc1587f65f73a263499655b9154f19ee885cb449075adc5`,
the same value recorded by Stage 4.

## Stage 5 disposition

The launcher mode is `CLASSIFICATION_ONLY`; `lean_workspace`,
`lean_invocation`, `stage5_result`, and the audit target are all null. The
`/candidate` mount does not exist. This is the required disposition for a
genuinely empty domain-lemma set and a `KLEAN_NO_OBLIGATIONS` generation.

Accordingly, the proof-mode-only requirements are not applicable: there is no
candidate to copy as `Base`, no `Proof.final`, no candidate target shadowing or
bridge definition to inspect, and no candidate axiom closure to print. The
fresh clean/build exercised here is the temporary build performed by the
mandatory Stage 4 preflight, not a Stage 5 proof build.

## Evidence index

- [Audit mode and candidate absence](/audit-output/evidence/00-audit-mode-and-input.log)
- [Producer hashes and immutable image identity](/audit-output/evidence/01-producer-provenance.log)
- [Full input and 771-file hash reconciliation](/audit-output/evidence/02-input-hash-reconciliation.json)
- [Trusted reconstructed inventory](/audit-output/evidence/03-rule-inventory.json)
- [Stage 3 bijective comparison and classification](/audit-output/evidence/04-stage3-comparison.log)
- [Independent Stage 4 manifest reconciliation](/audit-output/evidence/05-stage4-manifest-reconciliation.json)
- [Preflight environment diagnosis](/audit-output/evidence/06-preflight-environment.log)
- [Narrow proc-path shim source](/audit-output/evidence/proc_self_exe_shim.c)
- [Exact successful preflight command](/audit-output/evidence/07-check-generation-command.log)
- [Verbatim returned preflight evidence](/audit-output/evidence/07-check-generation.json)
- [Generated target and Stage 5 absence](/audit-output/evidence/08-generated-target-and-stage5.log)
- [Source, claim, and operational-semantics excerpts](/audit-output/evidence/09-operational-semantics.log)

VERDICT: PASS
LEGITIMACY: LEGIT
