# Independent Stage 3/4 Audit: HumanEval `14-all-prefixes`

## Scope and result

The launcher and environment both record:

- problem: `14-all-prefixes`;
- condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`; and
- audit mode: `CLASSIFICATION_ONLY`.

I treated the Stage 1 workspace, prior Stage 2 review, protected Stage 3
classification, Stage 4 artifacts, and all embedded prose as untrusted
evidence. I did not rely on the prior PASS or its conclusions.

The independent result is PASS. The local verification-module closure has
exactly six rules. All six are genuine recursive definitions of newly declared
summary functions. There are no operational rules, proved-derived lemmas, or
domain lemmas in that inventory. Consequently, Stage 4's
`KLEAN_NO_OBLIGATIONS` status, empty obligation map, absent generated target,
and absent Stage 5 candidate are legitimate.

## Trusted tooling and producer provenance

The launcher-recorded mechanical-checker lock
`/opt/humaneval/data/klean-audit-tools.lock.json` hashes to:

```text
b264b3e71509703dee83f852b9e5c084220c7d8310f0d97350c4f82efde1d34b
```

This exactly matches `/audit-input.json`. Every one of the nine trusted tool
files named by that lock also matches its locked SHA-256. This includes the
rule inventory, lemma-discovery contract, Klean exporter, preflight, final
gate, pipeline tree hash, and Stage 6 resolution contract.

Before judging Stage 4, I hashed the exact mounted generation-time producers:

```text
bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07  klean_export.py
42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d  klean.py
```

These hashes match both `generator-manifest.json` and
`generation-tools/source-manifest.json`. The source bundle contains exactly
those two producers plus the source manifest. Its canonical tree hash is:

```text
388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e
```

That hash matches `/audit-input.json`. The immutable generator image ID agrees
across the generator manifest, source manifest, and launcher-recorded producer
path:

```text
sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7
```

There is therefore no producer-source infrastructure error.

## Signed input and tree integrity

I independently recomputed the launcher envelope digest and every mounted
input hash relevant to this audit. The canonical signed-resolution digest is
`f7e9acfbf66eb071d46e9becfefad032117a11b5616d0252033a5659a8a102f4`.

The following values all match `/audit-input.json`:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 mounted tree | `bf434670efd547c62098305600d4c19b0c6d8400b2db93e6f731389bdb6bd6d5` |
| Stage 1 frozen export digest | `ccfe7240acdf2b61069b5c0a11db4a0e022f600d4ba0b02848e79a2b8c180e88` |
| Stage 2 mounted tree | `14f1180b672753373e646296b19d52fdcd58fa6eab093d5b82a8e3fd8cd82fb9` |
| Stage 3 manifest file | `93a3088524226fc522459641b6c47f0eff23cc15a05c7a288bd8ea48f15f0ee8` |
| Stage 4 mounted tree | `04c3fb0047e964c0f3110cc3091066d2c0e715e3b7de7da9e8e7e4a149e6f694` |
| Generated project digest | `4ea306c273b4bc55c0c51704e0220ee67093cff71d3bfcdf9d6b219efe96b237` |
| Producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

I also reconstructed the complete Stage 1 regular-file map. Its exact set of
778 relative paths and all 778 per-file SHA-256 values match
`resolution.stage1_source_hashes`; there are no omitted or extra paths.

The distinction between the Stage 1 mounted-tree hash and frozen-export digest
is intentional: they use the pipeline tree framing and Klean frozen-input
digest respectively. Both were recomputed with the locked trusted
implementations and both match their recorded fields.

## Inventory reconstruction and Stage 3 bijection

Using the locked `tools.k_rule_inventory.inventory_verification` on the frozen
`/reference/k-proof`, I reconstructed:

```text
verification module: VERIFICATION
local module closure: [VERIFICATION]
verification.k SHA-256:
  a5de4cf739bfe0c9bded2008df3a264e90781761b76df2ac0c2ba3b1e218ba86
rule count: 6
inventory SHA-256:
  3635b55c581bb693bf9d1f691d4d109988a8b38ca64b5d50a3dfdfb99c6eb22e
```

For every rule, I separately sliced the recorded physical source span from
`verification.k`, compared it byte-for-byte with the reconstructed rule text,
normalized it by whitespace, recomputed its SHA-256, and checked that
`source_rule_id` is exactly `rule-<normalized_sha256>`.

| Lines | `source_rule_id` | Role after independent classification |
|---|---|---|
| 9 | `rule-c66555fbc7562dc499a559e86f61f18f4641f27b060cdaac63d026c4a6228f4a` | `DEFINITION` |
| 10–16 | `rule-ddc7841337c859b509a00b74a2e0a5b7e6bd9580e358dace34a9474cf5433539` | `DEFINITION` |
| 21 | `rule-86be445e1c689d1c6ed735a9a647f68ed43460e098ac79c711756a84ec51506c` | `DEFINITION` |
| 22–23 | `rule-8cbc95a23d5256ceff710bd39a970d4af1d331ffa290596fe0b2a2bf11fe5e63` | `DEFINITION` |
| 26 | `rule-68569d14375a530cd3bc32752b84149ccbaa54ed7ded6be435ffa66ae49a6808` | `DEFINITION` |
| 27–28 | `rule-77a2c1942531821ff4fcd1cb2a8c9e380517c3e7efcf1f6ae4048acf2974e2e8` | `DEFINITION` |

The protected Stage 3 manifest contains exactly these six identities, exactly
once each, in this order. Its inventory hash matches the reconstruction.
There are no missing, extra, duplicated, or reordered identities. Since the
manifest carries identities rather than duplicating source text, the
identity's embedded normalized hash plus the matching whole-inventory hash
bind each entry to the independently reconstructed source span. The Stage 4
input manifest additionally copies the six full classified records, including
spans and normalized hashes, exactly.

## Independent classification judgment

### `prefixesAcc` rules, lines 9–16

`prefixesAcc` is newly declared as a total function
`IntSeq × IntSeq × ValSeq → ValSeq`. The first rule is its empty-remaining-input
base equation. The second is its constructor recurrence: it consumes the head
character, extends the current prefix, appends that new prefix to the
accumulator, and recurses on the strict tail.

These rules name a recursively defined mathematical summary. They do not
rewrite a `<k>` configuration, skip an operational computation, or assert a
property of an already defined result. They are therefore `DEFINITION`, not
`OPERATIONAL_RULE` or `DOMAIN_LEMMA`.

### `finishPrefix` rules, lines 21–23

`finishPrefix` is newly declared as a total function
`IntSeq × IntSeq → IntSeq`. Its equations define the final accumulated prefix:
the empty case returns the current prefix, while the constructor case appends
one character and recurses on the strict tail. This is a constructor-complete,
descending definition of a named loop-variable summary.

It does not claim an unproved equality about an existing K operation and does
not replace execution. It is `DEFINITION`.

### `finishChar` rules, lines 26–28

`finishChar` is newly declared as a total function
`Val × IntSeq → Val`. With no remaining characters it returns the current
loop-target value. With a nonempty remainder it records the current singleton
string and recurses on the strict tail. This exactly defines the final loop
target: the prior value is retained for an empty remainder and otherwise the
last yielded character wins.

Again, this is a named, constructor-complete recurrence, so it is
`DEFINITION`.

### Operational-semantics comparison

The fixed supplied semantics supports the same one-step recurrence:

- string iteration maps `str(iCons(C,R))` to the yielded singleton
  `str(iCons(C,.IntSeq))` and remaining iterator `str(R)`;
- the for-loop binds the yielded value, executes the body, and continues with
  the remaining iterator;
- string `+` maps to `seqConcat`;
- list `append` updates the heap from `VS` to
  `valSeqConcat(VS,vCons(V,.ValSeq))`; and
- the source loop performs exactly the prefix concatenation followed by that
  append.

The loop-invariant claim connects those operational effects to
`prefixesAcc`, `finishPrefix`, and `finishChar`; the definitions themselves do
not preempt the program's execution.

Boundary examples discriminate the recurrences:

- empty input leaves the output empty, prefix empty, and initialized `char`
  unchanged;
- one character `a` yields output `[a]`, prefix `a`, and final `char = a`;
- two characters `a,b` yield `[a,ab]`, final prefix `ab`, and final
  `char = b`.

Counterfactual recurrences that prepend instead of append, reuse the old
accumulator, retain the initial `char` on a nonempty input, or fail to recurse
on the tail disagree with these fixed operational steps. The actual equations
do not have those defects.

None of the six rules has a `simplification` attribute. No rule is claimed as
`PROVED_DERIVED_LEMMA`, so the special prior-proof requirement is not invoked.
No rule states a domain fact or desired postcondition over preexisting
operations. My independent domain-lemma set is therefore genuinely empty.

All three defined summaries are relevant: `prefixesAcc` occurs in the final
heap postcondition, and all three occur in the loop invariant that connects
execution to that postcondition. There is no irrelevant claimed domain lemma.

## Deterministic Stage 4 generation

The generator manifest's pinned toolchain exactly matches
`/reference/klean-toolchain.lock.json`, including Lean `v4.22.0` at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

I reran the required call:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The audit sandbox initially prevented Lean's `IO.appPath` from resolving
`/proc/<pid>/exe`, so the mounted Elan proxy could print Lake's version but
could not locate the Lean/Lake installation for a build. I diagnosed that
environment issue and used a narrow local `LD_PRELOAD` shim under
`/tmp/audit-work` that supplies only the missing self-executable path for the
pinned `lean`, `lake`, and `leanc` binaries. It does not alter any source,
manifest, generated project, theorem, or compiler result. With the shim,
`lean --version` reports the exact locked version and commit.

The unchanged trusted preflight then returned:

```text
status: KLEAN_NO_OBLIGATIONS
lake clean exit: 0
lake build exit: 0
obligation count: 0
target: null
designated sorry count: 0
trust declaration count: 41
```

The fresh `lake clean` output hash is the empty-output SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The fresh build output hash is
`07123ee4dd17259c5af19a5baba33b5de61399f850e49b6eca721321cbb34093`.
Both hashes and the full returned preflight document are exactly identical to
the signed launcher record.

The independent manifest and obligation audit found:

```json
{
  "source_rules": [],
  "obligations": [],
  "trust_parameters": []
}
```

The raw obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trust-inventory hash is
`1cce5bef07a74ceecd7d931df9669aed74ab01d30505eaadaab1e181e0da572f`,
matching the export result. All Stage 1, Stage 3, inventory, generated-tree,
producer, toolchain, obligation-map, and trust-inventory bindings agree across
the input manifest, generator manifest, export result, signed launcher input,
and freshly recomputed values.

The generated Lean project contains translations of the three definition
functions and the generated rewrite driver. Those are not domain-lemma
obligations. The 41 allowlisted collection-hook trust declarations are
structural declarations in the generated base project; no proposition target
depends on them because there is no target.

The zero-domain-set/source-rule/obligation correspondence is an exact
bijection. There can be no omitted, duplicated, irrelevant, weakened, or
vacuous conjunct: the generated conjunction does not exist. A manual scan of
all generated Lean sources finds zero `def targetStatement` declarations.
`generator-manifest.json`, `/audit-input.json`, and the fresh preflight all
record `target: null`. `Klean14AllPrefixes/Lemmas.lean` has an empty namespace
and no generated target.

Thus `KLEAN_NO_OBLIGATIONS` is confirmed for a genuinely empty independently
classified domain set.

## Stage 5

Stage 5 proof checks are inapplicable. The launcher mode is
`CLASSIFICATION_ONLY`; `lean_workspace`, `lean_invocation`, their hashes,
`stage5_result`, and the fixed target are all null. `/candidate` is absent, as
required. I did not fabricate or perform proof-mode-only candidate checks.

## Evidence

The complete raw command record is in `evidence/COMMANDS.md`. Key artifacts
include:

- `18-reconstructed-rule-inventory.json`;
- `25-verification-k-numbered.txt`;
- `33-stage3-bijection-summary.txt`;
- `142-str-operational-rules.txt` through
  `147-controls-for-loop-rules.txt`;
- `122-rerun-check-generation-shimmed.json`;
- `124-obligation-map.json`;
- `148-independent-integrity-audit.py`; and
- `159-independent-integrity-audit-final.json`, containing 106 passing
  independent assertions, with exit code 0 in
  `160-independent-integrity-audit-final-exit.txt`.

VERDICT: PASS
LEGITIMACY: LEGIT
