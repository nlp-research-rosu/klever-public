# Independent audit: 156-int-to-mini-roman

## Scope and result

This audit covers HumanEval problem `156-int-to-mini-roman`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both the live
`AUDIT_MODE` and `/audit-input.json` select `CLASSIFICATION_ONLY`.
The launcher records `stage5_result: null`, `target: null`, and no
`/candidate` is mounted. Stage 5 proof, axiom, theorem-identity, and
operational-bridge checks are therefore inapplicable. Their absence is also
required by the selected Stage 4 status.

I did not rely on the selected Stage 2 PASS, the protected Stage 3
classification, or prior logs as verdicts. I reconstructed the rule inventory
and classifications from the frozen source and supplied semantics, then checked
Stage 4 independently.

## Producer provenance gate

Before judging Stage 4, I hashed the exact mounted producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable generator image is consistently
bound as
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator manifest, and the final component of the
launcher-recorded producer-source path in `/audit-input.json`. The recomputed
producer-source tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly matching the audit input. There is no producer-source
infrastructure error.

Evidence: `evidence/01-producer-provenance.txt`,
`evidence/02-inventory-tool-and-image-binding.txt`, and
`evidence/38-stage4-independent-check.txt`.

## Rule inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof`. The selected verification module is
`VERIFICATION`; its local verification-file closure contains only that local
module. `MPY` is supplied by the required external semantics rather than
defined as another local module in `verification.k`.

Reconstruction produced:

- `verification.k` SHA-256:
  `dc061fe1bcdad413b2394a2cc475337e70a180cce415e68fb7f257ea05867978`
- inventory SHA-256:
  `da15137333fc4ba0e27fa6e78b326e34c147bb1051cc398ad15e8b90fba881b1`
- exactly three rules, in source order.

| Span | Source rule ID | Attributes | Independent class |
|---|---|---|---|
| 12–41 | `rule-73432c3a885f4063bc8df0e53921bf98bff4057d4844018e2315176d083cc1ac` | none | `DEFINITION` |
| 43–46 | `rule-9c027b657c924d9bded261a2258c44e3b4f2a5adc4d1fa50a891947006f320c6` | none | `DEFINITION` |
| 48–53 | `rule-0ea1d474a57944cbe1723cb797da19fe9cb40b152784827f7fc8e7cf966f2e93` | none | `DEFINITION` |

For each rule, an independent normalization of its exact source span reproduced
the recorded normalized hash and `source_rule_id`. The ordered ID lists in
the reconstruction and `lemma-discovery.json` are identical and unique.
There are no omissions, extras, duplicates, reordered identities, changed
hashes, or unaccounted classifications. The discovery inventory hash also
matches the fresh whole-inventory hash.

Evidence: `evidence/04-reconstructed-inventory.json` and
`evidence/06-inventory-bijection.txt`.

## Independent classification judgment

All three rules are honest definitions, not domain lemmas or operational
bridges.

1. `intToMiniRomanBody` is a named macro expansion of the program body. It
   expands to the three assignments, tuple subscripts, integer `%` and
   `//`, the `number == 1000` branch, returns, and string concatenations.
   It states no result property and supplies no mathematical shortcut.

2. `solutionModule` is a named macro that wraps that body in the
   `int_to_mini_roman(number)` function definition. With macro expansion
   enabled, `kast` produced byte-identical KORE for `solutionModule` and
   the frozen `solution.mpy`: both outputs were 9,659 bytes with SHA-256
   `7a013b9edaa963989944c1d67cdb5172269a233a6ce09132da398501f877976d`,
   and `cmp` exited 0.

3. `solutionCall(N)` is the verification harness macro. It expands to the
   same function module followed by assignment of `__result` to an ordinary
   call of `int_to_mini_roman(N)`. It does not replace that call with an
   answer or summary.

The relevant syntax productions are marked `[macro]`, and the compiled
sentences are tagged `macro`. After expansion, the supplied semantics
performs module loading and statement sequencing, constructs the closure,
looks up and calls it, binds the argument, executes the body, evaluates
assignments, tuple indexing and integer/string operations, branches, and
returns through the ordinary operational rules. Thus none of these rules
preempts program execution or assumes the Roman-numeral postcondition.

There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or
`DOMAIN_LEMMA` entries. No rule has a `simplification` attribute, so the
requirement that every simplification rule be a definition or domain lemma is
satisfied. The true domain-lemma set is genuinely empty; no relevant
source-program or postcondition fact was hidden under another classification.

Evidence: `evidence/08-classification-operational-evidence.txt`,
`evidence/09-fixed-semantics-execution-path.txt`, and
`evidence/39-macro-solution-ast-identity.txt`.

## Recorded hash audit

The independent checker recomputed every launcher-level mounted artifact hash,
the Stage 1 export hash, generated tree hash, discovery hash, producer tree
hash, verification hash, producer file hashes, obligation-map hash, and
trust-inventory hash. All match their bindings in the audit input and Stage 4
sidecars. It also checked all 800 per-file hashes in
`resolution.stage1_source_hashes`: there are zero missing files and zero
mismatches. The canonical hash of the complete `resolution` object matches
`resolved_input_sha256`.

Key recomputed values include:

- Stage 1 export:
  `894b08d9302c8f9e36b4e8fca96ee620a136f724e22c5a9b086325abf538a7e0`
- generated tree:
  `5d629dc61d9517c3f076d878ce4ab7d4005f5371e6fe7351408b1555d78bf6fa`
- Stage 3 discovery:
  `2c05a1ffbc7170a69c4bf5b4e23dc8f2440e3f8d9d629fe414611b6490fa9352`
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- trust inventory:
  `3656f36378c28ff36cf296720a7085b34fa1854439f5d59e35a1ce2009a219d2`.

Evidence: `evidence/07-recorded-hash-recomputation.txt` and
`evidence/38-stage4-independent-check.txt`.

## Stage 4 preflight and manifest bijection

I reran `tools.klean_preflight.check_generation` with exactly:

```text
PYTHONPATH=/reference
input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
```

The audit sandbox initially prevented Lean from locating itself: this Lean
runtime reads `/proc/<getpid()>/exe`, while the sandbox exposes
`/proc/self/exe` but not the numeric PID entry. The first failure is preserved
in `evidence/12-preflight-rerun.txt`. Disassembly of the installed,
hash-bound Lean runtime confirmed the exact failing `readlink`. I used a
narrow preload shim under `/tmp/audit-work` that redirects only numeric
`/proc/*/exe` reads to `/proc/self/exe`; it does not alter the frozen input,
generated project, manifests, producer sources, Lean declarations, or build
outputs. With the pinned toolchain directory first in `PATH`, the unchanged
preflight then completed.

The rerun returned:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: `null`
- designated sorry count: 0
- trust declaration count: 41
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, all generated modules built successfully.

The complete command output and returned JSON are in
`evidence/35-preflight-rerun-fixed.txt`; the shim diagnosis and validation
are in `evidence/29-proc-app-path-test.txt`,
`evidence/33-lean-app-path-disassembly.txt`, and
`evidence/34-procself-shim-test.txt`.

The independently checked identity chain is:

```text
independent DOMAIN_LEMMA IDs
= Stage 3 DOMAIN_LEMMA IDs
= input-manifest source_rules
= obligation-map source_rules
= obligation source_rule_ids
= []
```

All five lists are empty, ordered identically, and duplicate-free.
`trust_parameters` is also empty. Consequently there is no omitted,
duplicated, irrelevant, weakened, or vacuous conjunct. The generator manifest,
export result, recorded preflight, and selected status all record zero
obligations and `KLEAN_NO_OBLIGATIONS`.

## Fixed target identity and Stage 5 absence

The expected target definition derived from the obligation map is absent.
Independent parsing finds no generated target. The generator manifest,
launcher audit input, and both preflight records all bind `target: null`.
`Lemmas.lean` contains no theorem or lemma declaration. Therefore the fixed
generated target is correctly “no target”; it has not been changed or weakened.

The generated prelude contains 41 allowlisted executable collection-hook
axioms, which the preflight reconciled with the trust inventory and checked as
non-propositional. They cannot prove a target here because no target or
obligation exists.

In classification-only mode, a Stage 5 candidate must not exist. `/candidate`
is absent, the launcher records no Lean workspace or invocation hashes, and
`stage5_result` is null. It would be incorrect to manufacture a `Base`
copy, run `#print axioms Proof.final`, or assess target parameters when there
is no target or proof candidate.

Evidence: `evidence/36-stage4-sidecars-and-target-scan.txt` and
`evidence/38-stage4-independent-check.txt`.

## Conclusion

Stage 3 is complete and correctly classifies all three local verification
rules as definitions. The genuinely empty domain-lemma set justifies Stage 4's
`KLEAN_NO_OBLIGATIONS` result. Producer provenance, all recorded hashes,
the empty source-rule/obligation bijection, the null target, and the required
absence of Stage 5 artifacts are internally and independently consistent.

VERDICT: PASS
LEGITIMACY: LEGIT
