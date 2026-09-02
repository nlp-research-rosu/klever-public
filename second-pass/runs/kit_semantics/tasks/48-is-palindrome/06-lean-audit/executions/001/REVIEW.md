# Independent Stage 3–5 audit: HumanEval 48-is-palindrome

## Scope and result

I independently audited problem `48-is-palindrome`, condition
`kit-semantics`, with `SUPPLIED_SEMANTICS`.  `/audit-input.json` and the
`AUDIT_MODE` environment variable both record `CLASSIFICATION_ONLY`.
`/candidate` is absent; the recorded Stage 5 workspace, invocation, and hashes
are all null.  That is the required shape for a legitimate
`KLEAN_NO_OBLIGATIONS` result.

The conclusion is PASS/LEGIT.  The decisive fact is not merely that the
manifests say there are no obligations: reconstruction of the frozen local
verification-module closure produces no rules at all, and inspection of the
source program, exact reachability post-state, and supplied operational rules
confirms that no proof-local domain lemma is hidden or needed.

## Trusted-tool and producer provenance

Before judging the generation, I hashed the exact producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both equal the values in `generator-manifest.json` and
`source-manifest.json`.  The source bundle contains exactly those two files
plus `source-manifest.json`.  Its pipeline tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`.

The immutable generator image ID is a three-way match:
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
It appears in the generator manifest, the producer source manifest, and as
the basename bound by the producer-source path in `/audit-input.json`.

The mechanical-checker lock hashes to
`1cca0c10fa61c806f07242ba46c7aa84149c9e547741914e702cd1bbcc4d6eb8`,
matching the launcher record.  Every one of the nine trusted checker source
files under `/reference/tools` matches the per-file hash in that lock.
Therefore there is no producer or checker provenance error.

## Inventory reconstruction and bijection

I ran the trusted `inventory_verification` implementation directly against
`/reference/k-proof`, rather than accepting the protected classification or a
prior review.  The selected module is `VERIFICATION`, as fixed by `prove.sh`.
Its local closure inside `verification.k` is exactly `["VERIFICATION"]`:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

`MPY` is supplied by the required frozen semantics, not by another local
module in `verification.k`.  The local closure therefore has zero `rule`
sentences.  There are no source spans or per-rule normalized hashes to list.
The reconstructed inventory is:

- `verification_sha256`:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`
- `verification_module`: `VERIFICATION`
- `verification_modules`: `["VERIFICATION"]`
- `rules`: `[]`
- independently recomputed canonical inventory hash:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

The protected Stage 3 document has exactly schema version 2, that inventory
hash, and `rules: []`.  Trusted boundary validation reports zero definitions,
zero operational rules, zero proved derived lemmas, and zero domain lemmas.
The comparison is bijective and order-preserving because both ordered sets
are empty.  There are no omitted, duplicated, extra, reordered, or
hash-changed identities.

## Independent classification judgment

There are no inventory entries to label.  In particular, the frozen local
closure contains no definition, operational bridge, simplification rule,
purported derived lemma, or asserted domain fact.  Consequently:

- no `DOMAIN_LEMMA` can be hidden under `DEFINITION`, `OPERATIONAL_RULE`, or
  `PROVED_DERIVED_LEMMA`;
- there is no unproved rule claimed to have been established earlier and used
  later; and
- the condition that every `simplification` rule be a `DEFINITION` or
  `DOMAIN_LEMMA` is satisfied because there are no such rules.

I also checked that the empty domain set is mathematically appropriate rather
than merely structurally self-consistent.  The source is exactly:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

The reachability claim binds the returned result to
`S ==K buildIS(S, isLen(S) -Int 1, -1, -1)`.  Under the frozen supplied
semantics, a no-bound slice with step `-1` has start `isLen(S) -Int 1` and
stop `-1`; `buildIS` recursively selects decreasing indices until that stop;
and string equality reduces to structural equality of the two `IntSeq`
values.  Thus the claim's result is the ordinary operational normal form of
`text == text[::-1]`.  It is not a proof-local palindrome characterization,
oracle, shortcut, or domain theorem.  No source-relevant domain lemma remains
to export.

## Recorded hash audit

The independent hash script checked all 773 regular files in the frozen
Stage 1 export bijectively against `stage1_source_hashes`; there were no
missing, extra, or changed files.  It also recomputed both hash schemes used
by the manifests:

- Stage 1 pipeline tree:
  `87a20a0a5decc244eafb85225e463a9ec1011a029520ebee2548f1bd13e5d101`
- Stage 1 export tree:
  `ab0c59fd7c1803191261f32d2a0b6d1a01fd6cc23aa5955281364ffd76afbb1b`
- selected Stage 2 audit tree:
  `f3cedb5c5b550df2db0d7be1a3f3dbf61a5aea54bece5609cd68c64e54cab7be`
- protected discovery file:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`
- selected Stage 4 generation tree:
  `d4e1b3b9b9bd2b9dda7b42311ebd38192b3a0a4fff423232d0d074a360057434`
- generated project export tree:
  `cc8d96574ff360f36df8ef43e02612aaabbedb1854433eecb122fba0bd8a96c4`

All match `/audit-input.json`, the selections, and the applicable generation
sidecars.  The pinned toolchain document also equals the toolchain object in
the generator manifest.

## Deterministic Stage 4 judgment

The generated `obligation-map.json` has exact schema version 3 and contains:

```json
{
  "source_rules": [],
  "obligations": [],
  "trust_parameters": []
}
```

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`.  The independently classified domain set,
the mapped source-rule list, and the obligation-ID list are the same empty
ordered set.  There are no omissions, duplicates, irrelevant or weakened
equations, or vacuous conjuncts.

The generator manifest, export result, selected Stage 4 status, and trusted
preflight all agree on `obligation_count: 0` and
`KLEAN_NO_OBLIGATIONS`.  The generator manifest and preflight both record a
null target.  The trusted target parser returns null, and an independent scan
of every generated `.lean` file finds zero `def targetStatement`
declarations.  Therefore the fixed target identity is exact absence; it was
not changed, weakened, duplicated, or replaced.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three inputs.  Its own fresh-copy
`lake clean` returned 0 with empty output, and `lake build` returned 0 with
the expected nine-target build completing successfully.  The returned
evidence status is `KLEAN_NO_OBLIGATIONS`, target null, zero obligations, zero
sorries, and 41 generated trust declarations.

The first preflight invocation exposed an audit-sandbox defect: Lean 4.22
could not locate `/proc/<getpid>/exe` in the sandbox's PID view.  I preserved
that failure, then used the recorded audit-only `LD_PRELOAD` shim that rewrites
only numeric `/proc/<pid>/exe` reads to the working `/proc/self/exe`.  The
pinned Lean binary, generated project, and all input hashes remained
unchanged.  With that narrowly scoped environment repair, the trusted
preflight passed and reproduced the recorded clean-build output hash
`8658968a7dba2a7bc1bd3b85c183083ecc66235b98778d90ba39a991c593d9cc`.

The generated prelude's 41 generic collection-hook axioms are exactly the
allowlisted declarations in `trust-inventory.json`; the inventory records no
designated or other sorries.  Because there is no generated proposition and
no Stage 5 theorem, these declarations are not dependencies of a purported
proof and do not convert the no-obligation result into a proof claim.

## Stage 5 applicability

Stage 5 is correctly absent.  There is no `/candidate`, no generated target,
no `Proof.final`, and no Stage 5 path or hash in the audit input.  Accordingly,
a candidate copy, candidate `lake clean`/`lake build`, `#print axioms
Proof.final`, operational-bridge parameter testing, and proof-identity audit
are neither required nor possible in this `CLASSIFICATION_ONLY` audit.  Their
absence is a required consistency condition, not missing evidence.

## Evidence index

- [Mode and candidate presence](/audit-output/evidence/00-mode-and-presence.txt)
- [Producer provenance](/audit-output/evidence/01-producer-provenance.txt)
- [Trusted inventory reconstruction](/audit-output/evidence/02-inventory-reconstruction.txt)
- [Source and operational meaning](/audit-output/evidence/03-source-and-operational-meaning.txt)
- [Initial sandbox preflight failure](/audit-output/evidence/04-preflight-unshimmed.txt)
- [Narrow sandbox shim check](/audit-output/evidence/05-sandbox-shim-check.txt)
- [Successful trusted preflight](/audit-output/evidence/06-preflight-success.txt)
- [Complete hash and structure audit](/audit-output/evidence/07-hash-and-structure-audit.txt)
- [Reproducible hash audit script](/audit-output/evidence/hash_and_structure_audit.py)
- [Reproducible preflight driver](/audit-output/evidence/run_preflight.py)
- [Recorded sandbox shim source](/audit-output/evidence/lean-proc-self-shim.c)

VERDICT: PASS
LEGITIMACY: LEGIT
