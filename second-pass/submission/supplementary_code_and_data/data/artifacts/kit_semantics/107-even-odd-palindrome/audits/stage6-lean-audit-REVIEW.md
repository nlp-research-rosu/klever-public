# Independent Stage 3–5 audit: 107-even-odd-palindrome

## Scope and result

This audit covers HumanEval `107-even-odd-palindrome`, condition
`kit-semantics`, with `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
`/audit-input.json` select `CLASSIFICATION_ONLY`. `/candidate` is absent and
the recorded Lean workspace/invocation hashes are null, so Stage 5 proof
checking is not applicable.

I treated the Stage 1/2/3/4 artifacts and their prior reports as untrusted
evidence. I did not execute any script from those inputs. Trusted code was
limited to `/reference/tools`, with independent read-only inspection and
audit scripts stored under `/audit-output/evidence`.

## Producer-source prerequisite

The Stage 4 producer prerequisite passes before any generation judgment:

- `klean_export.py` SHA-256:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`.
- `klean.py` SHA-256:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
- Producer bundle SHA-256, using the trusted Stage 6 resolver's
  `tools.pipeline_contract.sha256_tree`:
  `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`.
- Immutable generator image ID:
  `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.

The two file hashes agree exactly among the mounted files,
`source-manifest.json`, and `generator-manifest.json`. The image ID agrees
between both manifests and the image-key suffix of the producer path recorded
in `/audit-input.json`. The bundle contains exactly the two producer files and
the source manifest. There is no producer-source mismatch and therefore no
infrastructure `AUDIT_ERROR`.

The preliminary diagnostic in
`evidence/00-diagnostic-wrong-tree-algorithm.log` intentionally remains in the
record: it used Klean's generated-project `tree_digest`, which is not the
aggregate algorithm used for producer bundles. Tracing the trusted resolver to
the correct `pipeline_contract.sha256_tree` yields the exact launcher hash in
`evidence/01b-producer-integrity-contract-hash.log`.

## Inventory reconstruction and bijection

I ran the trusted rule inventory over the frozen `/reference/k-proof` workspace
and independently recomputed each source slice and canonical JSON hash. The
local verification-module closure is exactly `VERIFICATION`; imported supplied
semantics modules are external to the local `verification.k` module closure.

The frozen `verification.k` SHA-256 is
`466c7679d2f2c6cd7a3d3b9a04c583d518d0920cc9d070b4e41226adb9d26748`.
The reconstruction contains exactly one rule:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | lines 10–228 |
| Attributes | empty list |
| Normalized SHA-256 | `85e70a4588ebd4cc7fa9900b762e8c8d4075fa1ebbdfda530c9ea390b0a2029a` |
| `source_rule_id` | `rule-85e70a4588ebd4cc7fa9900b762e8c8d4075fa1ebbdfda530c9ea390b0a2029a` |
| Protected classification | `DEFINITION` |

The exact line slice equals the inventory rule text. Re-normalizing that slice
reproduces the digest, and prefixing the digest with `rule-` reproduces the
identity. Re-hashing the ordered rule documents gives whole-inventory hash
`bd6baa11540644d109e6d3516ace2adf5c7c318407fb921dfed4acc5a6ffaf79`,
which matches the trusted reconstruction, Stage 3 manifest, Stage 4 input
manifest, and generator provenance.

The protected manifest has exactly the same one identity in the same order,
with one accounted classification and no duplicate. There are no omitted,
extra, reordered, duplicated, or changed rules.

## Independent classification judgment

The sole rule is the exhaustive nullary equation
`solutionClosure() => closureVal(("n", .ParamNames), BODY, 0)`. It is a
`DEFINITION` because it names an exact proof term: the source function's
parameter list, body syntax tree, and defining environment. It does not state
a mathematical proposition about palindromes, characterize a result apart
from the source body, or rewrite an operational configuration.

I compared the rule without executing the untrusted source. A small independent
parser compared its body with both the frozen `solution.mpy` term and the
Python AST of `solution.py`. All three have function name
`even_odd_palindrome`, parameter `n`, the same 107 decision nodes and 108
return leaves, and defining environment 0. Their canonical decision-tree hash
is `8cd8d74355c52f1c11734c722a7498a48260b4f261a828ec06e420c45afab3a0`.

The supplied operational semantics supports that classification:

- `functions.k` lines 14–16 translate an actual `FuncDef` into a
  `closureVal(PNS, BODY, L)` in the current environment.
- `call.k` lines 69–74 do not summarize the result. They allocate the callee
  frame, bind `PNS` to the evaluated arguments, and execute `BODY` before
  `#endcall`.
- `functions.k` lines 63–90 bind the parameter and preserve the ordinary
  return/frame lifecycle.

Thus `solutionClosure()` does not replace or accelerate execution of the
program body. It merely supplies the exact closure value that the source
definition denotes. It is not an `OPERATIONAL_RULE`, not a
`PROVED_DERIVED_LEMMA`, and not a `DOMAIN_LEMMA`. The rule has no
`simplification` attribute; even viewed as a function equation, its exhaustive
nullary definition satisfies the required definition category.

There are no other local rules from which a relevant domain theorem could be
hidden. The independently classified domain-lemma set is genuinely empty.

## Deterministic Stage 4 generation

All resolution and manifest hashes were independently recomputed. In
particular:

- Stage 1 contract tree: `f82c9d533b5d5132abe30319663dfc27eeefa1e6dbeaf363e22f55c97b62a601`.
- Stage 1 Klean export tree: `0962452562fbe64aa7550a510fd7dc45a10a9f09818f275c3f0301d03988e961`.
- Stage 3 manifest: `85547ddce7c7a1e0263a0ca0dd16979ea4a0f74176fc1c70ec08ae5befc13ed8`.
- Stage 4 selected generation tree:
  `c0f65f36b3489a66112ebddcea8e67249b1b9d5451015cc288e2153360ec1bd3`.
- Generated project tree:
  `b3c6d888f4246bc765b28a7c060eeae01b1597977e12bce40c84e11d66c929ff`.
- Obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
- Trust inventory:
  `daca9efbfc46885059bca85b8c0f6da0c409e65f557dcf50203d496ef6b7cef6`.

The complete 791-file Stage 1 source-hash map also matches bijectively, with no
missing, extra, or changed path. The Stage 2 and Stage 4 selected artifact
hashes match their launcher selections. The generator toolchain object equals
the trusted lock, including Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The Stage 4 input manifest's sole `definitions` entry is exactly the
reconstructed rule enriched with its Stage 3 classification and rationale.
The independently determined domain set, input-manifest `source_rules`,
obligation-map `source_rules`, and obligation IDs are all the same empty
ordered list. The obligation map also has empty `obligations` and
`trust_parameters`; all sidecars record obligation count 0.

This is not a weakened or vacuous theorem: the trusted producer computes no
expected target for an empty obligation set, trusted target discovery finds no
generated target, and the generator manifest, audit input, shipped preflight,
and rerun preflight all record `target: null`. No empty conjunction or `True`
target was emitted. Therefore `KLEAN_NO_OBLIGATIONS` is the correct Stage 4
status for the independently classified empty domain set.

## Required preflight and build evidence

The first unmodified invocation of
`tools.klean_preflight.check_generation` reached its fresh build and exposed an
audit-sandbox defect: the shell reported a namespace PID for which
`/proc/<pid>/exe` was absent. Lean's `IO.appPath` consequently could not detect
its installed Lake configuration. This failure and exit are preserved in
`evidence/05-preflight-check-generation.log`.

I used the minimal audited shim in `evidence/proc-self-shim.c`, which redirects
only `readlink("/proc/<digits>/exe")` to `/proc/self/exe`. It does not modify
the pinned Lean/Lake binaries, generated sources, imports, build options, or
proof terms. With that sandbox-only path repair, I reran the exact trusted
`check_generation` function with `PYTHONPATH=/reference` and the required
three inputs plus the trusted toolchain lock.

The returned evidence is saved verbatim in
`evidence/07-preflight-returned.json` and the full command transcript is
`evidence/06-preflight-check-generation-shimmed.log`. It reports:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0 and target null;
- `lake clean` exit 0;
- `lake build` exit 0 with all generated modules built;
- zero designated sorries; and
- the same Stage 1, Stage 3, and generated-project hashes independently found
  above.

The rerun object exactly equals the mounted preflight JSON, although that prior
result was not assumed. A separate fresh-copy clean/build transcript, including
the unshimmed failure, shim source/library hashes, pinned Lean version and
complete interactive build output, is in
`evidence/12-lean-sandbox-workaround.log`.

## Stage 5 and trust accounting

Stage 5 is correctly absent. Both launcher mode sources say
`CLASSIFICATION_ONLY`, `/candidate` does not exist, and the Lean workspace and
invocation fields/hashes are null. Since Stage 4 generated no target theorem,
there can be no `Proof.final` proving it and no target-parameter bridge to
audit. Running `#print axioms Proof.final`, candidate shadowing checks, or
candidate operational-parameter tests would fabricate a proof-mode artifact
outside the selected mode, so those checks are not applicable.

The generated base project contains 41 preflight-accounted collection-hook
trust declarations, but no proposition target or Stage 5 proof depends on
them in this no-obligation mode. Preflight independently confirmed that the
generated target module contains no proposition trust escape.

## Evidence index

- `evidence/COMMANDS.md`: exact command index and artifact mapping.
- `evidence/01b-producer-integrity-contract-hash.log`: producer files, bundle,
  manifests, and image binding.
- `evidence/02-inventory-reconstruction-full.log`: full trusted inventory.
- `evidence/03-closure-identity.log`: independent non-executing source/closure
  comparison.
- `evidence/08-independent-manifest-check.log`: 14 independent hash,
  sidecar, bijection, target, and mode checks; all pass.
- `evidence/09-inventory-reconstruction-summary.log`: independent span,
  normalized hash, source ID, whole hash, and ordered-bijection reconstruction.
- `evidence/10-functions-semantics.log` and
  `evidence/11-call-semantics.log`: frozen operational rules used in the
  classification judgment.
- `evidence/05-preflight-check-generation.log`,
  `evidence/06-preflight-check-generation-shimmed.log`, and
  `evidence/07-preflight-returned.json`: required preflight failure diagnosis
  and successful returned evidence.
- `evidence/12-lean-sandbox-workaround.log`: full independent clean-build
  environment transcript.

VERDICT: PASS
LEGITIMACY: LEGIT
