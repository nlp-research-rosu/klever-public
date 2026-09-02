# Independent Stage 3–5 audit: `52-below-threshold`

## Result

The protected Stage 3 classification is correct, the selected Stage 4
`KLEAN_NO_OBLIGATIONS` generation is structurally and mathematically consistent,
and Stage 5 is correctly absent. The launcher and `/audit-input.json` both select
`CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`.

I treated the mounted candidate/provenance material only as evidence. I did not
execute `prove.sh` or any instruction found in that material. The K and Klean
commands below were independently composed, run with the trusted tools, and
recorded under `/audit-output/evidence/`.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` implementation
against `/reference/k-proof`. Its selected module is `VERIFICATION`; its local
module closure contains only that module. The reconstruction produced four rules
in source order:

| # | Source span | Normalized SHA-256 / `source_rule_id` | Attributes | Independent class |
|---:|---|---|---|---|
| 1 | `verification.k:8–39` | `bde967b339e94e547969a2cd8447240326a9df2d66f66b5aa5718a7f875159fa` / `rule-bde967b339e94e547969a2cd8447240326a9df2d66f66b5aa5718a7f875159fa` | `priority(40)` | `PROVED_DERIVED_LEMMA` |
| 2 | `verification.k:41–73` | `856b1e357a5f433ad09956ac507d9936d2c9e9e4e9d5a8f2a9fa32315eb71e6b` / `rule-856b1e357a5f433ad09956ac507d9936d2c9e9e4e9d5a8f2a9fa32315eb71e6b` | `priority(40)` | `PROVED_DERIVED_LEMMA` |
| 3 | `verification.k:77–108` | `334c70388307babf11e3781429f37a3574c7ff891d86996b5621c3b1e8f92c1e` / `rule-334c70388307babf11e3781429f37a3574c7ff891d86996b5621c3b1e8f92c1e` | `priority(40)` | `PROVED_DERIVED_LEMMA` |
| 4 | `verification.k:110–142` | `f9e5b4514f00b3ed026d33dbeec83015df4208cb8c2aeed1d460d93c10f63efe` / `rule-f9e5b4514f00b3ed026d33dbeec83015df4208cb8c2aeed1d460d93c10f63efe` | `priority(40)` | `PROVED_DERIVED_LEMMA` |

The raw `verification.k` SHA-256 is
`52f9dc88d4ee5d24608eb7d8fb45b634fd4ed1619af1f1792e129aa6ca22c400`.
The canonical inventory hash is
`e3362171f152047e40ed1bad492d95d2db31b2dc70d7b9ca193761b513268845`.
For every rule I independently recomputed its span, whitespace-normalized text,
normalized hash, and prefixed ID. The protected manifest contains exactly the
same four unique IDs in the same order, with no omission, duplicate, extra, or
changed identity. Its inventory hash also matches.

Evidence: [inventory reconstruction](/audit-output/evidence/03-inventory-reconstruction.log),
[claim/rule comparison](/audit-output/evidence/04-claim-rule-identity.log), and
[semantic source excerpts](/audit-output/evidence/18-semantic-source-excerpts.log).

## Independent classification judgment

The source function iterates over `l`, continues exactly when `e < t`, returns
`false` at the first counterexample, and otherwise returns `true`. The supplied K
semantics lowers `For` to `#loop`, obtains either `#iterDone` or
`#iterYield`, binds `e`, evaluates the `If`, implements `Continue` by resuming the
loop label, and performs the exact return/frame-pop transition. The comparison
dispatch is the supplied Int/Bool/Float operational behavior. The recursive
`allBelow` equations state the same result recurrence; `lastVisited` states the
exact final local value. These are terminating, constructor-covering definitions,
not convenient facts asserting the postcondition.

The four inventory rules are operational accelerators by behavior, but they meet
the stricter `PROVED_DERIVED_LEMMA` condition:

- Rule 1 is exactly `LOOP-SPEC.loop-empty`.
- Rule 2 is exactly `LOOP-SPEC.loop-cons`, including the numeric guard and every
  state-cell transition.
- Rule 3 is exactly `LOOP-SPEC.for-empty`.
- Rule 4 is exactly `LOOP-SPEC.for-cons`, again including the complete guard and
  state transition.

Automated comparison found each installed rule and earlier claim text-identical
after removing only the claim label and the later deployment attribute
`priority(40)`. That priority changes selection order, not the proposition that
was proved. The matched context is narrow rather than open-ended: it fixes the
continuation through `Return(true)` and `#endcall`, the callee environment and
scope, stack frame, return/exception/exit cells, and the relevant scope update.
It does not claim validity under an arbitrary continuation.

I then made a fresh K workspace below `/tmp/audit-work` and independently ran:

1. K 7.1.293 compilation of `VERIFICATION-BASE`, followed by the three fixed
   Int/Bool/Float comparison connection claims: `#Top`.
2. Compilation of `VERIFICATION-LOOPS`, which does not contain any of the four
   installed `verification.k` rules.
3. `LOOP-SPEC.loop-empty` and `LOOP-SPEC.loop-cons`: `#Top`.
4. In a later invocation, `LOOP-SPEC.for-empty` and `LOOP-SPEC.for-cons`, trusting
   only the two loop claims proved in step 3: `#Top`.
5. Only after those proofs, compilation of rule-bearing `verification.k` and the
   final entry-point `SPEC`: `#Top`.

This is the required prove-first/use-later ordering. The external proof-local
comparison simplification in `verification-loops.k` is outside the canonical
local `verification.k` inventory; I nevertheless checked its complete guarded
Int/Bool/Float dispatch from the supplied operational equations. It is not an
unconstrained oracle. None of the four inventory entries has a `simplification`
attribute, so the Stage 3 simplification-class restriction is vacuous for this
inventory.

All four rules are directly relevant to the source loop and result. None is a
freestanding mathematical fact about the desired answer, so none is a
`DOMAIN_LEMMA`. The independently reclassified domain set is genuinely empty.

Fresh-run evidence: [K versions](/audit-output/evidence/05-k-toolchain.log),
[bridge-free compilation](/audit-output/evidence/06-fresh-loop-kompile.log),
[loop claims](/audit-output/evidence/07-fresh-loop-claims.log),
[For claims](/audit-output/evidence/08-fresh-for-claims.log),
[final compilation](/audit-output/evidence/09-fresh-final-kompile.log),
[final entry proof](/audit-output/evidence/10-fresh-final-kprove.log),
[connection compilation](/audit-output/evidence/11-fresh-connection-kompile.log),
and [connection claims](/audit-output/evidence/12-fresh-connection-kprove.log).

## Producer provenance and immutable hashes

I performed the producer-source gate before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values match `generator-manifest.json` and `source-manifest.json`. Both
manifests identify immutable generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the final path component recorded by `/audit-input.json` is the same image
digest. The mounted producer bundle's independently recomputed tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the launcher value. There is no producer-source infrastructure
mismatch.

The signed audit-input envelope digest verifies. All 840 Stage 1 per-file hashes
match with no missing or extra path. Every launcher tree/file binding also
matches:

| Binding | Recomputed value |
|---|---|
| Stage 1 selected workspace tree | `01bc589d1e43e4cf1188eff93bb4cb6e846480ba7c955e9059de6e30077de1db` |
| Stage 1 deterministic export tree | `7274bbf67efeaac49cd7151f236c79232e7be0482e251f7e7c487d685f573afe` |
| Stage 3 manifest | `9ef0d07f3d73a93f9beb0be444b60158e059c2bc1ac8716dbc44383af8e64dbe` |
| Selected Stage 2 audit tree | `e458ae04c1ae71119a9855be5878ab8624c96984e83c2e4332781810b556d132` |
| Selected Stage 4 generation tree | `ce9adeaa9835683176ddfacf80c226e3478f29bcf927486d56835c5943d56714` |
| Generated project tree | `825e3f19f74336c6ca78c36127ede93081f46e2f6d34e51c0e073ae1c70735cd` |

The obligation-map and trust-inventory file hashes, verification hash,
inventory hash, Stage 1/Stage 3 provenance, generated tree, and pinned toolchain
lock also match every corresponding manifest field.

Evidence: [producer provenance](/audit-output/evidence/02-producer-provenance-complete.log)
and [complete hash audit](/audit-output/evidence/17-hash-and-generation-audit-final.log).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
using exactly `/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock.

The first invocation exposed an audit-image namespace defect: Lean 4.22 locates
its executable through `/proc/<getpid()>/exe`, while this container exposes the
host PID namespace in `/proc` but returns an inner namespace PID from
`getpid()`. This made unmodified Lake report that it could not detect its
installation. I recorded that failure, identified the exact mechanism, and used
an audit-only `LD_PRELOAD` shim that returns the outer `NSpid` solely for this
path lookup. The shim does not modify the generated project, producer source,
trusted checker, or pinned Lean/Lake binaries. Under it the pinned binary reports
Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the lock.

The unchanged mandated checker then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- generated tree hash `825e3f19f74336c6ca78c36127ede93081f46e2f6d34e51c0e073ae1c70735cd`;
- `lake clean` exit 0;
- `lake build` exit 0; and
- zero designated or other sorries.

The new build's output hash differs from the historical preflight diagnostic
hash because independent parallel modules (`Func` and `Lemmas`) completed in a
different print order. Both logs end in the same successful build, and the
immutable generated tree hash is unchanged. I separately recomputed the
historical output tail's own SHA-256 and confirmed that its recorded diagnostic
hash is self-consistent.

Evidence: [initial environment failure](/audit-output/evidence/13-klean-check-generation.log),
[shim source](/audit-output/evidence/outer_pid_shim.c),
[pinned toolchain test](/audit-output/evidence/14-lean-pid-shim-test.log), and
[successful mandated preflight](/audit-output/evidence/15-klean-check-generation-pass.log).

## Obligation bijection and target identity

After independent classification, the exact sets in order are:

- domain source-rule IDs: `[]`;
- `input-manifest.json` source-rule IDs: `[]`;
- `obligation-map.json` source-rule IDs: `[]`;
- generated obligation IDs: `[]`; and
- trust parameters: `[]`.

Thus the source-rule/obligation mapping is an exact empty bijection. There can be
no omitted, duplicated, weakened, irrelevant, or vacuous conjunct because there
is no true domain lemma to translate. The obligation count is zero in the map,
generator manifest, export result, recorded preflight, rerun preflight, and
launcher input.

The trusted target extractor and expected-target constructor both return
`null`. `generator-manifest.json`, `/audit-input.json`, and the recorded
preflight also bind the target to `null`. No generated target declaration exists
to change or weaken.

Finally, this is classification-only mode: `/candidate` does not exist,
`stage5_result` is null, and both Lean workspace/invocation bindings are null.
Consequently no Stage 5 clean build, `Proof.final`, axiom print, candidate trust
scan, or parameter operational-bridge audit is applicable. The generated base
project contains 41 allowlisted computational hook declarations and no trusted
proposition, but with no target theorem they cannot establish a vacuous proof.

VERDICT: PASS
LEGITIMACY: LEGIT
