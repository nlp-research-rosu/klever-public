# Independent Stage 3–5 audit: HumanEval `150-x-or-y`

## Result

The selected Stage 3 classification is correct. The independently reconstructed
local verification closure has ten definitions, one genuinely proved derived
lemma, no ordinary operational rules, and no domain lemmas. Consequently, the
selected deterministic Stage 4 status `KLEAN_NO_OBLIGATIONS` is correct: the
source-rule/obligation bijection is the empty bijection, the fixed generated
target is absent, and Stage 5 is correctly absent.

This was a `CLASSIFICATION_ONLY` audit under `SUPPLIED_SEMANTICS`.
`AUDIT_MODE` and `/audit-input.json` agree. I treated the mounted candidate,
prior audit, logs, comments, and rationales as untrusted evidence. No prior
verdict or prior classification was used as authority.

## Producer and mounted-input provenance

I hashed the generation-time producer sources before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These are exactly the hashes in both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus `source-manifest.json`. Its independently recomputed tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`. The audit-input producer path basename, the
source manifest, and generator provenance all bind the same immutable image:

`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.

The trusted Stage 6 audit-input contract verified successfully, including the
resolved-input digest
`69925557596f269a48ed3bb4a5a0c4055eba47980ddee198df6057ebcd1aa3b5`.
Every Stage 1 per-file hash matches the launcher record. Independently
recomputed principal hashes are:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree algorithm | `31b4566c19b2805f8b5ca6552daf9c2be7fc18f8fafcbe9eaeae88dd7828c749` |
| Stage 1 frozen export tree | `a78619cc1fdea5492f1e55607b3b8b56d511fd637009ca6681c7eaa03dad3b6e` |
| `verification.k` | `61021f343cccad572e0b471545a1cdf92fbc4087db010449fd5b96a3f0f7c0f2` |
| Stage 3 discovery manifest | `f57f1a88bebde0cfeff3674115202ad22ad3d000b8421e82314777f0f26cbf90` |
| selected Stage 2 audit tree | `734c42cca9391cb1cb7e00dfb6bcc08e5d5d33f2fc3bd57f0093ad1e80644361` |
| selected Stage 4 generation tree | `c365071eda892931f34ac20815fbcd304d63fdc6fd96b12dd32261f66d6d77f7` |
| generated project tree | `14f7941045b75b33d98695b5a0f3fdb3a26a602a29b1020269fd8f3b5330449c` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `fbb763df0f7d0de64c0361e3a02b5e38f3ef73e6937c8bf39a9d763ea9a2242b` |

All corresponding audit-input, input-manifest, generator-manifest,
export-result, preflight, selection, and toolchain-lock bindings match.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` code, I
reconstructed the local module closure selected by the final Stage 1
`kompile verification.k`: `X-OR-Y-VERIFICATION` followed by
`X-OR-Y-SUMMARY`. The reconstruction found exactly eleven rules. The canonical
whole-inventory hash is:

`702eb4a32ed254d180b4a3daaa572ca6ea99647abaa08d1d125856029ecfd0ef`.

For every row below, the exact `source_rule_id` is `rule-` followed by the
listed normalized SHA-256:

| Module / role | Source span | Normalized SHA-256 | Independent class |
|---|---:|---|---|
| `xOrYLoopBody` macro | 9–14 | `d8c0396d99cdaa6578f74d682dccdbe17f2a6c5c06920ff3ddc77c9703b53af4` | `DEFINITION` |
| `xOrYBody` macro | 17–23 | `c3590d006a48f7fb580323c09a84fb8d8b67e624d7743626829c8f229f5f3639` | `DEFINITION` |
| `#xOrY` invocation macro | 27–28 | `aab9969fc8e0d7f8d032ebc1fde57e0ac25f8c6542ee28021b38bbd8ddcdc410` | `DEFINITION` |
| `primeSelect`, `N < 2` | 35–36 | `233b9b155a5aad308207746f3e5fbb78e61a7ff6b481e6eadbe88f55ceaa72f2` | `DEFINITION` |
| `primeSelect`, terminal scan | 38–39 | `2d55b06d448d5cab5f3516d052549c646374f54f17718505f1abf76453a0e21e` | `DEFINITION` |
| `primeSelect`, divisor found | 41–43 | `095b4c9ff1307f814a13007c732477ec0a292f12a3a0e99fdd8835a3338d0f7f` | `DEFINITION` |
| `primeSelect`, recursive scan | 45–48 | `28e6dd4cbd572ccafa686bcd18b8c77cfffd1347486d1b31521b77f6724786f3` | `DEFINITION` |
| `scanLast`, terminal scan | 54–55 | `d9b8d42be816da166a1e0659584737197dc92eacc5f23c3a9681683e688b184b` | `DEFINITION` |
| `scanLast`, divisor found | 57–59 | `8844023decfe2108f1e2edf0942eda092335fa19dad7e651c41e367309f4c163` | `DEFINITION` |
| `scanLast`, recursive scan | 61–64 | `53ceb72bcf5cb4bf1d5acfbcc53327afe8dce7b4bf97c1fa640c3c3b50dd6e35` | `DEFINITION` |
| exact loop-summary transition | 73–100 | `9a422e1a1ab7385500d096a89793812db519cc1b6c12a2343c21aecc82c89c8d` | `PROVED_DERIVED_LEMMA` |

The Stage 3 manifest has these same eleven identities exactly once and in this
exact order. Its inventory hash matches. The trusted manifest contract also
rejects unexpected fields, malformed categories, and omissions. There are no
extra, missing, duplicated, reordered, or changed identities.

No inventory rule has a `simplification` attribute. The only rule attribute is
`priority(40)` on the loop summary. Thus the requirement that every
`simplification` rule be a definition or domain lemma is satisfied vacuously.

## Independent classification judgment

The first three rules expand named K syntax macros. They define the exact
translated loop body, function body, and harness call; they do not assert
mathematical facts or bypass an operational construct.

The four `primeSelect` equations define a recursive result summary. For
`D >= 2`, their guards exhaustively and disjointly partition:

1. `N < 2`;
2. `N >= 2` and `D >= N`;
3. `N >= 2`, `D < N`, and `pyMod(N,D) == 0`; and
4. the same scan domain with nonzero remainder.

The only recursive branch increments `D`, so it reaches the terminal branch.
Under the supplied semantics, `%` on integers is `pyMod`, `range(2,n)` becomes
`rangeObj(2,n,1)`, and the iterator yields precisely `2, …, n-1`. Therefore
`primeSelect(N,D,X,Y)` names the source loop's suffix result: `Y` if `N < 2`
or a divisor is found in `[D,N)`, otherwise `X`. This is a recurrence
definition, not a hidden domain lemma.

The three `scanLast` equations similarly define the final value of the mutable
`divisor` binding needed by the exact loop-state invariant. Their guards
partition `N >= 2, D >= 2`; the recursive branch increments `D` and updates the
remembered value. They are state-summary definitions, not facts assumed about
integers.

As supporting counterexample-oriented evidence, an independent source-loop
oracle matched `primeSelect` on 7,298 `(N,D)` cases and `scanLast` on 25,912
`(N,D,OLD)` cases. Mutations of the below-2, divisor, terminal, and tracked-old
branches were each separated by concrete witnesses. These finite checks
support—but do not replace—the exhaustive guard and descent reasoning above.

The last rule is a genuine proved derived lemma:

- The `loop_correct` claim and reused summary rewrite have the exact same
  configuration transition, cells, continuation, bindings, result summaries,
  and guard. After removing the proof-only `label(loop_correct)` and reuse-only
  `priority(40)` attributes, their normalized core is identical, with SHA-256
  `a1c28ea6540c660388552fe029a849c17aa3b3a256bb14d03ef6a0c08ff26b9f`.
  The differing attributes name the claim and schedule later application;
  they do not alter the proved reachability relation.
- `X-OR-Y-LOOP-SPEC` imports only `X-OR-Y-VERIFICATION`. That base module does
  not import or contain `X-OR-Y-SUMMARY`.
- In a fresh copy under `/tmp/audit-work`, the base module compiled with K
  7.1.293 and `kprove ... --claims loop_correct` exited 0 with `#Top`.
- Only afterward was `X-OR-Y-SUMMARY` compiled and imported by
  `X-OR-Y-MAIN-SPEC`; the main claim also exited 0 with `#Top`.
- The compiled summary rule has backend unique ID
  `ad2530f085eb20cb8a7faed8a7f49f7c300a4203bb31a69174dc2642975de222`.
  A complete later-main-proof rewrite trace records an actual application of
  that exact ID.

It is thus neither an unproved operational shortcut nor a domain lemma. It is
first proved from the frozen operational semantics and definitions, then reused
in the later proof exactly as required.

The local inventory contains no `OPERATIONAL_RULE`: ordinary `If`, `For`,
range iteration, comparison, modulo, call-frame, return, and pop behavior is
provided by the frozen supplied semantics, outside the local
`verification.k` inventory. It contains no `DOMAIN_LEMMA`: all mathematical
content in the local closure is either a named recurrence/state definition or
the separately proved operational loop transition. Hence the independently
determined domain-lemma set is genuinely empty.

## Deterministic Stage 4 generation

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
three specified inputs, and the trusted toolchain lock. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- frozen Stage 1 hash
  `a78619cc1fdea5492f1e55607b3b8b56d511fd637009ca6681c7eaa03dad3b6e`;
- Stage 3 hash
  `f57f1a88bebde0cfeff3674115202ad22ad3d000b8421e82314777f0f26cbf90`;
- generated tree hash
  `14f7941045b75b33d98695b5a0f3fdb3a26a602a29b1020269fd8f3b5330449c`;
  and
- successful `lake clean` and `lake build` diagnostics.

The literal first preflight attempt exposed a sandbox-specific Lean startup
problem: this environment's virtual numeric PID is absent from its read-only
`/proc` mount, although `/proc/self/exe` works. Lean therefore reported that it
could not locate its application before project checking. I preserved that
failed attempt. A narrowly scoped `LD_PRELOAD` shim redirected only
`readlink("/proc/<pid>/exe", ...)` to `/proc/self/exe`; Lean then reported the
pinned version/commit, and the unchanged trusted checker completed
successfully. The shim did not change the generated project, checker, manifests,
or toolchain.

The generation-time recorded `lake clean` output hash reproduces exactly. The
recorded 823-byte `lake build` output tail itself hashes exactly to its recorded
digest
`4d0e0f1f67bd7ede90233b95f5bb5158ff333d3d2289ddbca1ff53b8084ea522`.
The independent rerun's build log hash is
`4039309372b83f3ab72d2bbb481e21cf58952601a04508fdb369b0e54ecdf958`
because parallel Lake scheduling swapped the numbered `Func` and `Lemmas`
success lines. After normalizing those step numbers, the line multiset is
identical; all exit codes and artifact hashes match.

The independently reconstructed domain set, `input-manifest.json`
`source_rules`, obligation-map `source_rules`, and obligation list are all
empty. Thus the exact source-rule/obligation bijection is `∅ ↔ ∅`. There are no
conjuncts that could be irrelevant, weakened, duplicated, omitted, or vacuous.
The generator's expected-target calculation returns no definition;
independent target scanning returns none; and `generator-manifest.json` and
`/audit-input.json` both record `target: null`. No generated target declaration
exists in the Lean sources.

The preflight reconciled all 52 generated non-propositional trust declarations
with `trust-inventory.json` and rejected proposition trust. With no target,
none can serve as a proof escape for a Stage 5 theorem.

## Stage 5

Stage 5 is correctly inapplicable. `/candidate` is absent, while
`stage5_result`, `lean_workspace`, `lean_invocation`, and `target` are all null
in the launcher record. This is exactly what a legitimate
`KLEAN_NO_OBLIGATIONS` result requires. A `Proof.final` build, axiom print, and
parameter operational-bridge audit would be required only in
`CLASSIFICATION_AND_PROOF`; performing them here would invent a target and
candidate that must not exist.

## Evidence

Exact commands and output locations are indexed in
`evidence/COMMANDS.md`. Principal evidence is:

- `evidence/reconstruction.json`: canonical inventory, all hash and manifest
  bindings, ordered Stage 3 bijection, empty obligation map, target identity,
  and Stage 5 absence;
- `evidence/classification-checks.json`: exact claim/rule comparison, module
  graph and proof order, recurrence checks, and counterfactual witnesses;
- `evidence/preflight-attempt-1.txt` and
  `evidence/preflight-return.json`: preserved initial infrastructure failure
  and successful required preflight return;
- `evidence/derived-kprove.log` and
  `evidence/summary-main-kprove.log`: fresh `#Top` results;
- `evidence/main-rewrites.yml` and `evidence/summary-rule-use.txt`: complete
  later-proof trace and exact derived-rule application;
- `evidence/producer-and-target-check.txt`: raw producer hashes, manifests,
  generated file list, target scan, and candidate absence; and
- `evidence/tool-versions.txt`: K 7.1.293 and Lean 4.22.0 tool identities.

VERDICT: PASS
LEGITIMACY: LEGIT
