# Independent Stage 3–4 audit: HumanEval 13, `bare`

## Result

This audit fails. The frozen verification-module inventory contains one rule.
Stage 3 classified it as `PROVED_DERIVED_LEMMA`, but frozen Stage 1 did not
first prove the exact same rule: the proved loop claim has an empty
continuation, while the later priority-40 rule admits and preserves an
arbitrary `K` continuation. Under the required classification contract, this
program-specific loop theorem is a relevant `DOMAIN_LEMMA`. The independently
classified domain set therefore has one member, not zero. Stage 4 omitted its
obligation and incorrectly selected `KLEAN_NO_OBLIGATIONS`.

The producer sources, immutable generator identity, manifests, hashes, build,
and recorded empty-to-empty mapping are internally consistent. This is not an
infrastructure `AUDIT_ERROR`; it is a substantive classification and
obligation-omission failure.

## Scope and audit mode

- Problem: `13-greatest-common-divisor`
- Condition: `bare`
- Semantics mode: `GENERATED_SEMANTICS`
- Launcher mode in both `AUDIT_MODE` and `/audit-input.json`:
  `CLASSIFICATION_ONLY`
- Selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`
- Candidate: absent, as required for the recorded classification-only mode

All mounted Stage 1–5 files, logs, comments, rationales, and earlier reviews
were treated as untrusted evidence. No candidate or provenance script was
executed. Trusted code under `/reference/tools` was used for inventory and
preflight operations.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof` workspace. It selected `VERIFICATION`, the module
selected by the final `kompile verification.k` command in `prove.sh`. The local
verification-module closure within `verification.k` is exactly:

```text
VERIFICATION
```

`MPY` and `GCD-SPEC` are required from other frozen files and were inspected
for operational meaning, but they are not additional local modules inside
`verification.k`.

The reconstructed inventory is:

| Field | Reconstructed value |
|---|---|
| `verification.k` SHA-256 | `4b9cdac9c0e4687858a578f6712f4f53750bcb7fe03321364094a85e8ce64381` |
| Rule count | 1 |
| Module | `VERIFICATION` |
| Source span | lines 10–25 |
| Attributes | `priority(40)` |
| Normalized SHA-256 | `73f9484c2d5d4a2650340be4aa44fdeb23887916e674aa08b16de37c95cfb1fe` |
| `source_rule_id` | `rule-73f9484c2d5d4a2650340be4aa44fdeb23887916e674aa08b16de37c95cfb1fe` |
| Whole inventory SHA-256 | `50008efcfd19cf576b27005e04202364acfe9d3f1878d22d030b895e9a37b9ec` |

I also recomputed the normalized source hash directly from the trusted
inventory's extracted text and reconstructed `source_rule_id` as
`"rule-" + normalized_sha256`.

The protected Stage 3 manifest has exactly one entry with that identity in the
same position. There are no omissions, duplicates, extra identities, ordering
changes, source-span changes, or inventory-hash changes. Thus the Stage 3
manifest is structurally bijective with the frozen inventory. The failure is
the semantic classification, not its structural binding.

Evidence:

- `evidence/03-inventory-reconstruction.json.txt`
- `evidence/04-stage3-structural-validation.json.txt`
- `evidence/28-explicit-inventory-bijection.txt`

## Independent classification

### Operational meaning of the only rule

The rule matches the exact Euclidean loop from `solution.py` and
`solution.mpy`:

```text
while b != 0:
    r = a % b
    a = b
    b = r
```

For nonnegative `A` and `B`, it consumes that loop and rewrites the environment
to:

```text
a = gcdSpec(A, B)
b = 0
r = finalR(B, R0)
```

The LHS is an operational `execStmt(While(...))` term, and the RHS uses the
program-specific mathematical summary needed by the whole-program
postcondition. It is not a definition of a summary symbol, recurrence, macro,
or named proof term. It is also not an ordinary small-step execution or
observation rule from the language semantics; it is a proof-specific
whole-loop theorem/acceleration. It is directly relevant to both the source
program and the `gcdSpec(normInt(A), normInt(B))` postcondition.

The appropriate independent classification is therefore:

```text
DOMAIN_LEMMA
```

The rule has no `simplification` attribute, so the separate simplification-rule
restriction is not implicated.

### Why `PROVED_DERIVED_LEMMA` is invalid

Frozen Stage 1 does have the required ordering in part:

1. `loop-verification.k` imports `MPY` and `GCD-SPEC` and contains no summary
   rule.
2. `loop-spec.k` is proved against that rule-free module.
3. Only afterward does `prove.sh` compile `verification.k` with the
   priority-40 rule for the whole-program proof.

I independently rebuilt the rule-free loop definition and reran the frozen
loop claim. `kompile` exited 0 and `kprove` exited 0 with `#Top`.

However, the theorem statement is not the exact later rule. The compiled K
ASTs expose the material difference:

- Frozen `loop-spec.k` claim:
  `KRewrite(execStmt(loop), .K)` in the `<k>` cell. It starts and ends with an
  otherwise empty continuation.
- Later `verification.k` rule:
  `KSequence(KRewrite(execStmt(loop), .K), _DotVar2:K)`. The source
  `.K ...` admits and preserves an arbitrary continuation.

The later rule thus has a strictly broader match/context domain than the
frozen theorem that Stage 1 first proved. Its added `priority(40)` attribute is
also absent from the claim, although the continuation-domain difference alone
is decisive.

As a counterfactual check, I created a fresh audit-only claim explicitly
quantified over `REST:K` and proved
`execStmt(loop) ~> REST => REST` against the rule-free definition. It also
closed with `#Top`. This supports the mathematical plausibility of the framed
generalization, but it was not part of frozen Stage 1 and cannot retroactively
satisfy the required “first proves the exact same rule” provenance condition.

Evidence:

- `evidence/02-frozen-and-manifest-inputs.txt`
- `evidence/21-independent-loop-proof.txt`
- `evidence/23-compiled-claim-rule-scope.txt`
- `evidence/24-counterfactual-framed-loop-proof.txt`
- `evidence/26-three-way-k-cell-scope.txt`

## Generator producer provenance

Before judging Stage 4, I hashed the mounted generation-time sources:

| Producer | Actual SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable generator image ID is consistently:

```text
sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda
```

It matches the source manifest, generator manifest, and the image-key basename
recorded by `/audit-input.json` in `generation_producer_sources`. The mounted
producer-bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching `/audit-input.json`. Producer provenance passes; there
is no infrastructure `AUDIT_ERROR`.

Evidence:

- `evidence/06-producer-provenance.txt`
- `evidence/07-audit-input-tree-hashes.txt`
- `evidence/27-independent-hash-and-bijection-check.txt`

## Stage 4 preflight and hash verification

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required frozen Stage 1 workspace, protected
Stage 3 manifest, selected Stage 4 generation, and pinned toolchain lock.

The first invocation failed before project loading because this audit sandbox
does not expose `/proc/<reported-pid>/exe`, which Lean 4.22 uses to locate its
installation. `/proc/self/exe` is available. I recorded the failure and used a
narrow, audit-local `LD_PRELOAD` shim that redirects only
`/proc/<digits>/exe` reads to `/proc/self/exe`. The shim restored the pinned
Lean identity:

```text
Lean 4.22.0
commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05
```

With that environment-only workaround, the trusted preflight ran unchanged
and returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean: exit 0
lake build: exit 0
```

The returned build-output hash and tail exactly reproduce the recorded
preflight.

I separately recomputed both pipeline-style and exporter-style tree hashes,
every Stage 1 source-file hash, the Stage 3 file hash, producer hashes,
generator sidecar hashes, obligation-map hash, trust-inventory hash,
verification source hash, generated-project hash, toolchain binding, and
manifest provenance fields. All recorded values match the mounted bytes. The
launcher `resolved_input_sha256` also matches a fresh canonical hash of its
`resolution` object.

Evidence:

- `evidence/08-rerun-check-generation.txt` (initial sandbox failure)
- `evidence/19-proc-shim-test.txt`
- `evidence/20-rerun-check-generation-with-proc-shim.txt`
- `evidence/27-independent-hash-and-bijection-check.txt`

## Obligation bijection and target identity

Relative to the incorrect protected classification, Stage 4 is mechanically
self-consistent:

- `input-manifest.json` records zero `source_rules`;
- `obligation-map.json` records zero source rules and zero obligations;
- all obligation counts are zero;
- the generator manifest, recorded preflight, and audit input all record a
  null target;
- the generated Lean sources contain zero `def targetStatement`
  declarations; and
- no Stage 5 candidate, workspace, invocation, or result exists.

That is an empty-to-empty manifest-relative bijection, and there are no
generated conjuncts to duplicate, weaken, or make vacuous.

It is not the required mathematical bijection. Independent classification
yields this nonempty true domain set:

```text
rule-73f9484c2d5d4a2650340be4aa44fdeb23887916e674aa08b16de37c95cfb1fe
```

The Stage 4 source-rule list and obligation list both omit that identity.
Consequently the generated target is also missing: a true one-obligation
domain set cannot legitimately generate no target. Structural integrity
relative to a wrong classification does not cure this omission.

Evidence:

- `evidence/20-rerun-check-generation-with-proc-shim.txt`
- `evidence/27-independent-hash-and-bijection-check.txt`

## Stage 5

Stage 5 is not applicable because the launcher-selected mode is
`CLASSIFICATION_ONLY`. `/candidate` is absent and all Stage 5 paths/results in
the audit input are null. Therefore no candidate clean build, `Proof.final`,
axiom print, or operational-bridge parameter audit was performed.

## Final judgment

The inventory and provenance bindings are intact, and deterministic Stage 4
faithfully implements the protected manifest it received. The protected
manifest is nevertheless semantically wrong under the audit's exact-derived-
lemma criterion. Reclassifying the sole rule as the relevant `DOMAIN_LEMMA`
makes the domain set nonempty, invalidates `KLEAN_NO_OBLIGATIONS`, and exposes
one omitted Lean obligation and its missing fixed target.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
