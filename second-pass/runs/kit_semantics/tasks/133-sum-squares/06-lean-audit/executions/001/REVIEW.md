# Independent audit: HumanEval 133-sum-squares

## Scope and result

I audited Stage 3 classification and deterministic Stage 4 generation for
`133-sum-squares`, condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` select
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate`, a Stage 5 result, a Lean workspace hash,
and a Lean invocation hash are all absent. I treated all mounted candidate and
provenance content as untrusted evidence and did not rely on an earlier PASS or
classification.

The substantive conclusion is that the only two rules in the local
verification-module closure are exactly the base and recursive equations of a
named mathematical summary. Both are genuine `DEFINITION` rules. There are no
domain lemmas, so zero Lean obligations, no generated target, and no Stage 5
project are the correct results.

## Producer provenance

I hashed the mounted generation-time sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These values exactly match both `generator-manifest.json` and the producer
`source-manifest.json`. Both manifests record immutable generator image ID
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The image-keyed producer path in `/audit-input.json` has that same digest, and
the independently recomputed producer-bundle tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`. Producer source and image provenance are
therefore authenticated; there is no producer-source infrastructure error.

Raw evidence is in `evidence/01-producer-provenance.txt`,
`evidence/09-trusted-hash-and-producer-binding.txt`, and the independent
cross-check in `evidence/19-independent-structural-checks-passing.txt`.

## Canonical rule-inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` implementation, I
reconstructed the local closure selected by the frozen `prove.sh`. The closure
contains only local module `VERIFICATION`; imported semantics and program
modules are external to `verification.k`. The frozen file hash is
`d395088b7fce12221e4304c3a0e37d78b11dc84160dc104da281f657a284868b`.
The canonical inventory contains exactly these rules, in this order:

| Span | Rule | Normalized SHA-256 / `source_rule_id` |
|---|---|---|
| 12 | `rule sumCeilSquares(.ValSeq) => 0` | `5ea09376a68c388fa472315e5a536792a41ff43051dca71cb26ead91d202a76d` / `rule-5ea09376a68c388fa472315e5a536792a41ff43051dca71cb26ead91d202a76d` |
| 13–14 | `rule sumCeilSquares(vCons(V, VS)) => (ceilF(V) *Int ceilF(V)) +Int sumCeilSquares(VS)` | `681871636bed54428193956727088b21b492bc6c75570d01a289f5f5e087030a` / `rule-681871636bed54428193956727088b21b492bc6c75570d01a289f5f5e087030a` |

The recomputed whole-inventory hash is
`c7d4c5b3a7bc27a03f386a579a0214d8e3d8c738efff051f731036e5290aa152`.
The comparison with `/reference/lemma-discovery.json` is bijective and
order-preserving: two canonical entries and two unique classified entries,
with the same spans, normalized hashes, IDs, and inventory hash. There are no
omissions, duplicates, extras, reordered identities, or unaccounted entries.
The complete reconstruction is in `evidence/05-reconstructed-inventory.txt`.

## Independent Stage 3 classification

The syntax declaration immediately above the rules is
`syntax Int ::= sumCeilSquares(ValSeq) [function, total]`. The two rules cover
the empty and `vCons` constructors and recurse structurally on the tail:

- The empty equation defines the fold's base value as zero.
- The cons equation defines the recurrence by applying the supplied semantic
  `ceilF` operation to the head, squaring that integer, and adding the summary
  of the tail.

Neither rule contains or observes a `<k>` configuration, a store, a scope, or
another execution cell. They are not ordinary execution/observation rules.
They also state no independent arithmetic or domain fact: together they are
the definition of the named postcondition summary. They were present in the
compiled `VERIFICATION` module before the Stage 1 claims were proved and were
not first proved against a module omitting them, so they are not
`PROVED_DERIVED_LEMMA` rules. Neither has a `simplification` attribute.

This classification agrees with the frozen program and operational semantics.
The Python program initializes `total` to zero, iterates over every list
element, evaluates `math.ceil(number)`, adds the square, and returns `total`.
The supplied K semantics turns list `vCons` into one yielded head plus the tail,
implements the loop step and augmented assignment operationally, routes
`math.ceil` to `ceilF`, maps integer inputs to themselves and float inputs to
`Float2Int(ceilFloat(F))`, and uses K integer multiplication and addition. Thus
the recurrence is exactly the mathematical summary used by the loop invariant
and final postcondition.

Counterfactuals expose why this is a relevant definition rather than a
convenient lemma: changing the empty result from `0` contradicts the source
program on `[]`; omitting the recursive tail contradicts any two-element list;
and a constant or identity summary disagrees with simple lists such as `[2]`
and `[2, 3]`. No extra theorem is needed to state this fold. I therefore
independently classify both entries as `DEFINITION` and the true domain-lemma
set as empty. Source and operational traces are preserved in
`evidence/06-source-spec-operational-context.txt` and
`evidence/07-operational-rule-trace.txt`.

## Deterministic Stage 4 generation

I independently recomputed and matched the launcher and sidecar hashes,
including all 782 entries in the Stage 1 source-hash map. Important bindings
include:

- pipeline K-workspace tree:
  `f2727d5c16cc63407eb081ac917e5655c0d851ae5ce01c5004f665804a310705`;
- Stage 1 export/workspace digest:
  `50cce1588ecdd631511af92cffdba0e417179a8eb8b2a3637ee2695c9969c718`;
- Stage 3 manifest:
  `aa4f0079bb60c10f4cd0dbb24984a88a293f5c6e442f93df8066a849d860b099`;
- selected Stage 2 audit tree:
  `ac38f42fef1151e5c65c342957e903100b11ecabd061afbec2ae761fa369fcde`;
- complete Stage 4 generation tree:
  `14ae272e25804a1d34367c82739d048ad5b5b34d2681481af555028a263ea1f7`;
- generated-project tree:
  `cfe554ab900fb94214e89f40176ee2ebbe139b83974a119fa13f23db4b08a390`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

The exact obligation map is
`{"obligations":[],"schema_version":3,"source_rules":[],"trust_parameters":[]}`.
After the independent classification, the eligible domain-rule sequence is
also exactly `[]`; hence the source-rule/obligation mapping is an exact
empty-to-empty bijection. There are no omitted, duplicated, irrelevant,
weakened, or vacuous conjuncts. In particular, the generator did not replace
an empty conjunction with a theorem of `True`: the expected target definition,
the observed generated target, the generator-manifest target, the recorded
preflight target, and the audit-input target are all `null`.

The two definition rules are retained as definitions rather than obligations.
The generated function has an empty case returning `some 0` and a cons case
that evaluates `ceilF` twice, multiplies the results, recursively evaluates the
tail, and adds the values. This is the direct generated counterpart of the
frozen equations; the generated rewrite exports that summary result without
changing its meaning. The generated `Lemmas` namespace is empty.

An independent Lean-source gate found seven immutable Lean files, no `sorry`,
`admit`, or `unsafe`, and exactly 43 `axiom`/`opaque` trust declarations, all
and only the entries in `trust-inventory.json`. The trusted independent policy
also confirmed that none of those declarations assumes a proposition and that
all imports are local/safe. There is no target declaration to change or
shadow. See `evidence/19-independent-structural-checks-passing.txt`,
`evidence/72-stage4-source-trust-gate.txt`, and
`evidence/73-generated-definition-and-declaration-audit.txt`.

## Trusted preflight rerun

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly the required frozen workspace, discovery manifest, selected
generation, and pinned toolchain lock. The first invocation reached the fresh
temporary-copy build but exposed a sandbox/toolchain compatibility issue:
Lean 4.22 requests `/proc/<current-pid>/exe`, while this sandbox exposes only
the equivalent `/proc/self/exe`; an ordinary shell and Python process reproduce
the missing numeric-PID path. That raw failure is retained in
`evidence/20-rerun-check-generation.txt`.

I resolved only that path-lookup incompatibility with a preserved shim that
redirects `readlink`/`readlinkat` for the exact
`/proc/<its-own-pid>/exe` string to `/proc/self/exe` and passes every other path
unchanged. Its source is `evidence/lean-proc-self-shim.c`, source SHA-256 is
`9e5d43275cba69fb226fae8c74f302642dbddbcca32f2d5f1a2c5692be19198a`,
and compiled-object SHA-256 is
`02aefabe70005a4dfec7c26d002dd53941e07e5bc6ce85aa58ee492513fb6d65`.
This shim neither changes an audited input nor bypasses a checker or build
command. I did not supply a replacement `run_command`; the trusted preflight's
default runner executed the real pinned Lake and Lean tools.

With that equivalent application-path lookup available, the required trusted
rerun returned `KLEAN_NO_OBLIGATIONS`. Its fresh-copy `lake clean` exited 0 and
its `lake build` exited 0 after building Prelude, Sorts, Inj, Lemmas, Func,
Rewrite, and the root module. The returned evidence reports zero obligations,
no target, zero designated sorries, 43 reconciled trust declarations, and the
same frozen-input, discovery, and generated-tree hashes listed above. The
complete returned object and build output are in
`evidence/77-rerun-check-generation-passing.txt`; shim probes and hashes are in
`evidence/76-lean-proc-self-shim-probe.txt` and
`evidence/78-preserved-shim-hashes.txt`.

## Stage 5 applicability and legitimacy

This is not `CLASSIFICATION_AND_PROOF`. Because the independently determined
domain set is genuinely empty, the absence of a generated target and Stage 5
candidate is required, not an omission. There is no `Proof.final`, target
parameter, candidate definition, proof-axiom output, or operational bridge to
audit. Running proof-mode checks or `#print axioms Proof.final` would therefore
invent a target that the authenticated generation correctly did not produce.

The Stage 3 classification is mathematically correct, the Stage 4 generation
is fully bound to the frozen inputs and authenticated producer, and the
selected `KLEAN_NO_OBLIGATIONS` status accurately reflects the empty true
domain-lemma set.

VERDICT: PASS
LEGITIMACY: LEGIT
