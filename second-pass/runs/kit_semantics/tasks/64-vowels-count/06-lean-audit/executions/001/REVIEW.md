# Independent audit: HumanEval 64-vowels-count

## Scope and outcome

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition
`kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. Accordingly, this
audit covers the independent Stage 3 classification and deterministic Stage 4
generation. Stage 5 proof checks are not applicable: `/candidate` is absent,
the generated target is null, and the audit input records no Lean workspace or
invocation.

The Stage 3 classification is complete and mathematically appropriate. Its
true `DOMAIN_LEMMA` set is empty. Stage 4 therefore correctly reports
`KLEAN_NO_OBLIGATIONS`, emits no target theorem, and has no Stage 5 candidate.

## Producer provenance gate

I hashed the mounted generation-time producer sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The complete producer-source tree recomputes to
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`. The immutable generator image ID is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator manifest, and the image-keyed producer path
recorded by the audit input. The producer provenance gate passes; there is no
infrastructure `AUDIT_ERROR`.

## Inventory reconstruction and Stage 3 bijection

I ran the trusted canonical inventory code against the frozen
`/reference/k-proof`, without using the protected classification as input. The
local verification-module closure is exactly `VERIFICATION`; the selected
source is `verification.k` with SHA-256
`6bc684e38c7c1dfc4d991fa29f3d68c911d06824d5715b4a8a599cdd25c408c9`.
The reconstructed whole-inventory hash is
`016f23d6c21435b58eea72f72774ef91166fc2d422c670009b869717cfea0da7`.

The canonical ordered inventory is:

| Span | Normalized SHA-256 / source rule ID | Independent class |
|---|---|---|
| lines 11–13 | `ad7d69a43b55c7d713eb912ef35d6d9c5b48ec3b76133d9058d939e165530edf` / `rule-ad7d69a43b55c7d713eb912ef35d6d9c5b48ec3b76133d9058d939e165530edf` | `DEFINITION` |
| lines 15–28 | `5ef4c64339248ffdcfe1ebbeb14f7c7490e1d2b6b56b81a6718dfd908e382af8` / `rule-5ef4c64339248ffdcfe1ebbeb14f7c7490e1d2b6b56b81a6718dfd908e382af8` | `DEFINITION` |

The protected Stage 3 manifest contains those two identities exactly once, in
that exact order. Its inventory hash matches. There are no omitted,
duplicated, extra, reordered, or unknown identities. Because the manifest
binds classification to the canonical `source_rule_id`, its recorded source
spans, normalized texts, normalized hashes, and IDs are the independently
reconstructed ones above. The trusted Stage 3 structural validator also
returns two definitions and empty operational-rule, proved-derived-lemma, and
domain-lemma lists.

## Independent classification judgment

The first rule is the constructor base equation for the named total summary
`vowelsTail(IntSeq, IntSeq)`. When no characters remain, it converts the two
terminal comparisons (`last == "y"` and `last == "Y"`) to integer
contributions. This defines the base value; it does not match a `<k>` cell or
replace program execution.

The second rule is the constructor step equation. It adds one exactly-one-code
membership test against `aeiouAEIOU`, then structurally recurses on `REST`
with the current character as `LAST`. It is a genuine descending recurrence
over `IntSeq`, not an asserted aggregate property.

This agrees with the supplied operational semantics:

- string iteration yields the head as a one-character string and continues
  with the tail;
- `For` advances through `#iterNext`, binds the yielded character, executes
  the body, and resumes the remaining iterable;
- the body adds the result of string membership and assigns that character to
  `last`;
- string `in` dispatches to `strContains`, whose prefix/recursive equations
  make a one-character pattern true exactly when that code occurs in the fixed
  literal; and
- `intOf(Bool)` maps true to 1 and false to 0.

A structural induction on the remaining `IntSeq` therefore connects the
summary to the frozen program: the empty case is exactly the two post-loop
terminal tests, while the constructor case is exactly one loop iteration plus
the induction hypothesis on the tail. The equations are definitions of that
summary, not domain lemmas disguised as definitions. They are relevant to the
source program and its postcondition. Neither rule has a `simplification`
attribute, so the special simplification-class restriction is also satisfied.
There is no claimed `PROVED_DERIVED_LEMMA` requiring a prior bridge-free proof.

As finite adversarial support, an independent recurrence and source-level
oracle agreed on all 19,531 strings of lengths 0 through 6 over `aAyYb`.
Counterfactuals that count nonfinal `y/Y`, double-count final `y/Y`, ignore
uppercase vowels, or return a constant were rejected by concrete witnesses
`"yA"`, `"y"`, `"ACEDY"`, and `"a"`, respectively. These checks support,
but do not replace, the structural argument above.

The independently determined class partition is therefore:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

## Recorded hashes and deterministic Stage 4 generation

The independent hash checker verified the audit-input envelope digest and all
recorded mounted artifact hashes: Stage 1 workspace, Stage 1 export, Stage 2
audit, protected Stage 3 manifest, selected Stage 4 generation, generated
project, producer sources, and the null Stage 5 hashes. It also recomputed all
787 frozen Stage 1 regular-file hashes and found an exact key/value match.
Selection artifact hashes agree with their mounted trees.

The same check verified every Stage 4 hash binding across the input manifest,
generator manifest, export result, obligation map, trust inventory, and audit
input. In particular:

- generated tree:
  `2abb22058bbb385be6a404ed68d90ef26848eb5e6ad420276ed715e8438082e7`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `6829918ad3d5ad192db192e20eca05be69028fcbd15aadbaffe8a4bcb4a776ed`;
  and
- protected Stage 3 manifest:
  `fe7a0ab17af344ae447845e71ed8ee6e49ea4f3055ff2ee9308e53f046d42a04`.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1, Stage 3, Stage 4, and pinned toolchain paths. The
first call exposed a container-only PID namespace mismatch: Lean attempted to
resolve `/proc/<namespace-pid>/exe`, while this container exposes the process
through `/proc/self/exe`. A narrow audit-local `LD_PRELOAD` compatibility shim
redirected only that path form to `/proc/self/exe`; it did not alter any input,
generated source, theorem data, or Lean logic. With the pinned Lean 4.22.0
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, the exact preflight rerun
returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output SHA-256
  `f943c023c30cd1855ade3d282b34977f5a4004fd9e9f80f3622349d3eaed551a`;
- obligation count 0; and
- target null.

These diagnostic hashes exactly reproduce the selected Stage 4 preflight.

## Obligation bijection and target identity

The independent mathematical classification has an empty domain-lemma set.
The Stage 4 input manifest has no `source_rules`; `obligation-map.json` has no
source rules, obligations, or trust parameters; the generator and export
manifests both record obligation count 0; and the generator status is
`KLEAN_NO_OBLIGATIONS`. Thus the source-rule/obligation mapping is the exact
empty bijection. There is no omission, duplicate, weakened obligation,
irrelevant obligation, or vacuous conjunct.

The trusted target parser independently finds no generated target declaration.
The generator manifest, selected preflight, and `/audit-input.json` all bind
the target to null. `/candidate` does not exist. This is exactly the required
fixed output for a genuinely empty domain-lemma set, so there is no Stage 5
proof identity, axiom-accounting, or operational-bridge parameter check to
perform in this classification-only audit.

## Evidence

Raw command outputs, preserved scripts, frozen-source excerpts, the failed and
successful preflight runs, hash/bijection checks, and adversarial recurrence
checks are under `/audit-output/evidence/`. `evidence/COMMANDS.md` maps the
principal commands to their result logs.

VERDICT: PASS
LEGITIMACY: LEGIT
