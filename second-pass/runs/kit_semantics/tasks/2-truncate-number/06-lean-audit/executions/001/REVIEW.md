# Independent Stage 3–5 Audit: `2-truncate-number`

## Scope and conclusion

I audited HumanEval problem `2-truncate-number`, condition `kit-semantics`,
semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
`/audit-input.json` record `CLASSIFICATION_ONLY`. The selected Stage 4 status
is `KLEAN_NO_OBLIGATIONS`; `/candidate`, the Stage 5 workspace, and the Stage 5
invocation are all absent.

The protected Stage 3 classification is correct. The local verification-module
closure contains no rules, so the independently classified domain-lemma set is
genuinely empty. The deterministic Stage 4 artifacts are an exact empty
source-rule/obligation bijection, contain no generated target, and pass a fresh
trusted preflight. Stage 5 proof checks are inapplicable in this audit mode.

## Evidence handling

I treated every mounted candidate/provenance file, earlier verdict, log,
comment, and instruction as untrusted evidence. I did not rely on the earlier
Stage 2 PASS or the earlier Stage 3 classification. Rule reconstruction used
`tools.k_rule_inventory.inventory_verification` from the trusted
`/reference/tools` mount. Stage 4 checking used
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`.

Raw commands and outputs are under `/audit-output/evidence/`. The main records
are:

- `04_inventory_reconstruction_and_bijection.txt`
- `06_recomputed_recorded_hashes.txt`
- `11_rerun_check_generation_with_proc_fix.txt`
- `14_independent_zero_obligation_audit.txt`
- `15_independent_k_operational_sanity.txt`

## Inventory reconstruction and Stage 3 bijection

Frozen `verification.k` is only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The trusted inventory code selected `VERIFICATION` from the final `kompile`
command in `prove.sh`, reconstructed its local import closure as exactly
`["VERIFICATION"]`, and found no `rule` sentences. Its canonical result is:

- `verification_sha256`:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`
- `inventory_sha256`:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- ordered rule inventory: `[]`

`/reference/lemma-discovery.json` has schema version 2, the same inventory hash,
and `rules: []`. Trusted boundary validation reconstructed the same empty
ordered lists for `definitions`, `operational_rules`,
`proved_derived_lemmas`, and `domain_lemmas`. Therefore there are no omitted,
duplicated, extra, reordered, span-changed, or hash-changed rule identities.
There are also no simplification rules to misclassify.

## Independent classification and mathematical judgment

There are no local rule entries to assign to `DEFINITION`,
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. This is not a
manifest-created empty set: it follows directly from the frozen five-line
`verification.k`.

The empty domain set is also semantically appropriate for this proof. The
claim evaluates:

```k
Call(Name("truncate_number"), (F:Float, .Exprs))
```

to:

```k
floatMod(F, 1.0)
```

using only the supplied operational semantics:

1. `call.k` evaluates the callee and arguments and dispatches the stored
   `closureVal`.
2. `core.k` performs name lookup and left-to-right argument evaluation.
3. `functions.k` allocates the call frame, binds `number` to `F`, evaluates
   `Return`, and restores the caller frame.
4. `operators.k` dispatches `BinOp("%", F, 1.0)` to `applyBin`.
5. `float.k` evaluates the float literal and rewrites
   `applyBin("%", F1, F2)` to the supplied opaque operational symbol
   `floatMod(F1, F2)`.

The postcondition observes exactly that operational result. It does not assert
an additional arithmetic fact such as bounds, a floor identity, or a
human-facing fractional-part characterization. No domain theorem is being
assumed under another label, and no domain theorem is required to reach the
stated operational postcondition.

As an independent operational sanity check, K 7.1.293 produced `#Top` with
exit 0 for the frozen claim. Replacing the expected result by
`floatMod(F, 2.0)` failed with a stuck implication and exit 1. Changing the
function body to `% 2.0` while retaining the `% 1.0` target also failed with a
stuck implication and exit 1. The residuals distinguish
`floatMod(F, 1.0)` from `floatMod(F, 2.0)`, confirming both result constraint
and body sensitivity without any local verification rule.

## Producer provenance and recorded hashes

I hashed the generation-time producer files before judging Stage 4:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both match `source-manifest.json` and `generator-manifest.json`. The immutable
generator image ID is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest and generator manifest, and its digest component is the
producer-source path component recorded in `/audit-input.json`. The producer
bundle has the recorded pipeline tree hash
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
There is no producer-source infrastructure error.

All 770 per-file `stage1_source_hashes` were recomputed: there were no missing,
extra, or mismatched paths. All launcher tree/file hashes also matched:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `1b31767c919517cef3cc8a6d91b4498a74c6ebb40c7ff35e73fe765094818945` |
| Stage 1 export tree | `4883ebbfc3d8e3f284a2bcbf639440b5deda684dff9661746b1aa016d67a4c32` |
| Stage 2 audit tree | `cdf090312727ff2ecc2e762091b278faef9ab27ac553e0e851bc95059e0c266e` |
| Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 generation tree | `ee944b786f2111f06ec64aff0a88be3666b50f7a6369b8d5e77ce1b6ae275e8e` |
| Generated Lean tree | `62e40be3b85c7745b8c787df1afda71f132ec1321f2cc6db138427e9ab277f5b` |

The generator toolchain object exactly matches
`/reference/klean-toolchain.lock.json`, including Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The obligation-map hash,
trust-inventory hash, Stage 1/3 provenance hashes, generated-tree hash, and
recorded preflight object were independently reconciled across the input
manifest, generator manifest, export result, and audit input.

## Deterministic Stage 4 generation

The hash-bound generation-time producer source constructs Stage 4 source rules
only from the validated `domain_lemmas` list, preserves its order, and rejects
any mismatch between expected source IDs and emitted proposition IDs. It emits
`targetStatement` only when the proposition list is nonempty and selects
`KLEAN_NO_OBLIGATIONS` only when the obligation list is empty.

For this artifact:

- Stage 3 domain rules: `[]`
- `input-manifest.json` source rules: `[]`
- `obligation-map.json` source rules: `[]`
- generated obligations: `[]`
- trust parameters: `[]`
- generator obligation count: `0`
- export obligation count: `0`
- expected generated target: `null`
- observed generated target: `null`
- generator-manifest target: `null`
- audit-input target: `null`

The ordered source-rule/obligation identity lists are exactly equal and contain
no duplicates. With no conjuncts, there can be no irrelevant, weakened,
omitted, duplicated, or vacuous generated conjunct. Trusted target extraction
independently returned `None`, and a direct source search found no
`targetStatement` declaration. The generic generated project has 41 recorded
non-propositional collection-hook trust declarations, but no proposition trust
and no target that can depend on them.

`/candidate` does not exist, both Stage 5 paths and hashes in the audit input
are null, and no Stage 5 result is selected. This satisfies the
`KLEAN_NO_OBLIGATIONS` requirement that there be no generated target and no
proof candidate.

## Fresh Stage 4 preflight

The first preflight attempt exposed an audit-sandbox issue: Lean queried
`/proc/2/exe`, which is absent in the sandbox's proc view, and reported
`failed to locate application`. A diagnostic preload trace recorded that exact
failed readlink. I used a small, recorded shim that changes only numbered
`/proc/<pid>/exe` readlinks to `/proc/self/exe`; it does not alter Lean source,
the generated project, theorem content, or checker logic. With the shim, the
pinned binary independently reported Lean 4.22.0 and the exact locked commit.

I then reran the unchanged
`tools.klean_preflight.check_generation` call with:

- frozen input `/reference/k-proof`
- discovery manifest `/reference/lemma-discovery.json`
- generation `/reference/klean-generation`
- lock `/reference/klean-toolchain.lock.json`
- `PYTHONPATH=/reference`

The trusted checker copied the generated project to a fresh temporary
directory and returned:

- `lake clean`: exit 0
- `lake build`: exit 0, `Build completed successfully.`
- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: `null`
- designated sorry count: `0`
- trust declaration count: `41`

It also rechecked unchanged Stage 1, Stage 3, generated-tree, and sidecar
snapshots after the build. The resolved sandbox path issue is not a proof or
classification concern.

## Stage 5

Stage 5 is not present because the recorded and independently confirmed mode is
`CLASSIFICATION_ONLY`. Consequently there is no `Proof.final`, candidate
definition, target shadowing, axiom printout, or operational bridge to audit.
Running proof-mode checks or inventing a proof candidate would contradict the
selected zero-obligation status.

VERDICT: PASS
LEGITIMACY: LEGIT
