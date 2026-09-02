# Independent Stage 3–5 audit: `65-circular-shift`

## Scope and result

The launcher records:

- condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`;
- audit mode: `CLASSIFICATION_AND_PROOF`; and
- problem: `65-circular-shift`.

I treated all candidate, provenance, prior-review, comment, and log content as
untrusted evidence. I used the trusted rule inventory and preflight code from
`/reference/tools`, read the frozen K source directly, rebuilt the Lean proof
in a fresh directory, and independently checked the target-parameter
implementations against the supplied K semantics.

The Stage 3 classification is complete and mathematically correct. Stage 4
authenticates to the recorded immutable producer, generates exactly the one
true domain obligation, and preserves the fixed target. The Stage 5 proof
clean-builds, proves exactly that target without a candidate trust escape, and
uses operationally faithful target-parameter implementations.

## Producer authentication

This gate passed before Stage 4 was judged.

| Producer artifact | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |
| producer bundle tree | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` |

The two file hashes equal both `generator-manifest.json` and
`source-manifest.json`. The bundle contains exactly those two producer files
plus `source-manifest.json`.

The immutable image identity is
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
It is identical in:

1. `generator-manifest.json`;
2. `source-manifest.json`; and
3. the image-keyed producer bundle path recorded in `/audit-input.json`.

There is therefore no producer-source infrastructure error. Raw hashes and
the three-way image check are in
`evidence/01-producer-authentication.txt`,
`evidence/04-tree-hash-recomputation.txt`, and
`evidence/41-generator-image-id-reconciliation.txt`.

## Canonical rule-inventory reconstruction

Running `tools.k_rule_inventory.inventory_verification` against the frozen
`/reference/k-proof` workspace selected module `VERIFICATION`. Its local
verification-file closure is exactly `["VERIFICATION"]`. The reconstructed
`verification.k` SHA-256 is
`7ad0dc3cfc0df7db1370bb38fc5bf87e5c3433d6eeb96d5445d19dc381ddd76d`;
the canonical inventory SHA-256 is
`6518a0e5335bdd735f7d1fc208888cbaffb3c4f9c920f296fc3a5283f2485322`.

The five reconstructed rules, in canonical source order, are:

| Lines | `source_rule_id` | Attributes | Independent class |
|---:|---|---|---|
| 9–9 | `rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf` | `simplification` | `DOMAIN_LEMMA` |
| 15–46 | `rule-d103b0bf43c5480134ff24998aab7d8de1dcb6a242ebb94857dc35a60557cae1` | none | `DEFINITION` |
| 52–58 | `rule-402746ae5fd5896de06add571676987d516921b32b5a67c3dd97ac0a15e6a04b` | none | `DEFINITION` |
| 60–64 | `rule-0f914aff35fd352e2deb2adcd224d21f53f0ebfd8aa096d3c5c9f09a6967abf6` | none | `DEFINITION` |
| 66–86 | `rule-f54a87e944876d0f1f30b0a06541d47de0fc4d7c746b66c465a942f688c8058b` | none | `DEFINITION` |

For every row, the trusted reconstruction recomputed the exact source span,
normalized source text hash, and `source_rule_id`. The protected Stage 3
manifest has exactly five unique identities in exactly this order. Its ID set,
inventory hash, and per-entry identity all match. There are no omissions,
duplicates, extras, reordered identities, changed hashes, or unaccounted
classifications. See
`evidence/06-reconstructed-rule-inventory.json` and
`evidence/09-inventory-bijection-and-classification-check.txt`.

## Independent Stage 3 classification

### Domain lemma

The line-9 rule is:

```k
rule #Ceil(strToCodes(Int2String(X:Int))) => #Top [simplification]
```

It is not a definition: it does not define a summary, recurrence, macro, or
named proof term. It is not an ordinary execution/observation rule. It is not
a proved derived lemma: Stage 1 compiles `verification.k`, already containing
this exact rule, before every `kprove` call. There is no earlier proof of the
same statement against a module omitting it.

It is a genuine and relevant `DOMAIN_LEMMA`. In the supplied semantics,
`strToCodes` is partial:

```k
rule strToCodes("") => .IntSeq
rule strToCodes(S:String)
  => iCons(ordChar(substrString(S, 0, 1)),
           strToCodes(substrString(S, 1, lengthString(S))))
  requires S =/=String ""
    andBool ordChar(substrString(S, 0, 1)) <Int 128
```

`Int2String` emits the optional minus sign and decimal digits, all ASCII, so
the composition is defined for every K integer. The fact is material to this
program: `solution.py` executes `s = str(x)`, and both the frozen postcondition
summary and its guards use `strToCodes(Int2String(X))`. It is neither
irrelevant nor a restatement of the requested circular-shift result.

This is also the only `simplification` rule, so every simplification is
classified as the permitted `DOMAIN_LEMMA`.

### Definitions

The lines 15–46 rule expands the named total term
`circularShiftClosure` into the exact `closureVal` constructor tree for
`solution.mpy`. It names the program binding; it does not intercept a call or
replace execution. The supplied lookup, argument, frame, body, return, and
state-restoration rules remain active.

The other three rules define the named total summary
`circularShiftResult(X, SHIFT)`. Their guards are:

1. `SHIFT > length`;
2. not the first guard and `SHIFT < 0`; and
3. not the first guard and not `SHIFT < 0`.

They are pairwise disjoint and exhaustive. Their right-hand sides respectively
name reverse, unchanged decimal string, and the normalized rotation slice.
They occur as a proof summary, not as program-execution shortcuts. They are
therefore `DEFINITION`, not domain lemmas or operational bridges.

There are zero `OPERATIONAL_RULE` and zero
`PROVED_DERIVED_LEMMA` entries. The Stage 3 classifications agree with this
independent judgment.

## Stage 4 deterministic generation

### Trusted preflight

I reran:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

with `PYTHONPATH=/reference`. The successful returned result is:

- status: `PASS`;
- frozen Stage 1 export hash:
  `72505765ba82bb822a1fb2f7e6bec5b45623210f0bf15b18ade1dfdf7157764d`;
- Stage 3 manifest hash:
  `cc535ebd4290e1eed0a2d9fa18781e4c3ca7b5b1871db801c9f47fd466d96d06`;
- generated tree hash:
  `938bcc6b5f106c6110d6bb591324c505c20fcfe9d099b924848c7b0407826498`;
- obligation count: `1`;
- trust declaration count: `48`;
- designated sorry count: `0`; and
- clean/build exit codes: `0`/`0`.

The complete returned document is
`evidence/19-rerun-check-generation-success.json`.

The first preflight attempts exposed an audit-sandbox defect before project
loading: namespace `getpid()` returns `2`, but `/proc/2/exe` is absent, while
Lean 4.22 locates its executable through `/proc/<getpid>/exe`. Those failures
are preserved in evidence. I reran with a recorded preload shim that changes
only a `readlink("/proc/<digits>/exe", ...)` request to
`readlink("/proc/self/exe", ...)`. Its source and binary hashes are preserved
in `evidence/18-lean-proc-shim-validation.txt`. It changes no project file,
Lean source, target, proof term, or compiler behavior. With this path-only
correction, the build output hash exactly matches the recorded generation-time
preflight output hash.

### Independent hash reconciliation

All mounted launcher hashes recompute exactly:

- Stage 1 pipeline tree;
- Stage 1 export tree;
- every one of the 771 recorded Stage 1 file hashes, with no missing,
  mismatched, or unrecorded file;
- Stage 2 audit tree;
- Stage 3 manifest;
- Stage 4 generation tree;
- producer-source tree;
- generated project tree; and
- Stage 5 candidate tree.

The detailed comparison is
`evidence/24-independent-hash-reconciliation.txt`.

### Source-rule/obligation bijection and mathematical adequacy

Independent classification yields one domain-rule ID. The Stage 4 source map
contains that same one ID, and the obligation map contains that same one ID,
in exact order and without duplication:

```text
rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf
```

Its mapped conjunct is exactly:

```lean
∀ (X : SortInt),
  ((«strToCodes(_)_MPY-STR_IntSeq_String?»
      («Int2String(_)_STRING-COMMON_String_Int» X)).isSome = true) ↔ True
```

This is the faithful option-valued lowering of
`#Ceil(strToCodes(Int2String(X))) => #Top`: it quantifies the source integer,
applies both bound KORE symbols, and asserts that the partial result is
present. It is not bare `True`; the `↔ True` is the exact translation of the
K rule's right-hand side and leaves the definedness proposition fully
constrained. There is no irrelevant, weakened, omitted, duplicate, or vacuous
conjunct. Evidence is in
`evidence/21-obligation-map.json` and
`evidence/44-stage4-bijection-and-nonvacuity.txt`.

Because the true domain set is nonempty, `KLEAN_NO_OBLIGATIONS` would have been
invalid. The selected Stage 4 status is correctly `OK`/`PASS` with one target.

### Fixed target identity

The generated target is exactly:

- declaration:
  `Klean65CircularShift.Lemmas.targetStatement`;
- file: `Klean65CircularShift/Lemmas.lean`;
- definition hash:
  `83aa086aa5daf74bf3e4c3ece12d26e9fda8f99f8ef4919e857c55ce59b6020d`;
- applied statement hash:
  `2684d31225fce96f004b389e9eba44195f731c346a6257e6083ba2554dfdaa21`;
- obligation-map hash:
  `c624092628541729e21e97b48f27b45e313d3cdf471cb9c35a32a20e24713126`.

The target parsed from the generated source equals both the generator manifest
and `/audit-input.json`. Recomputing the target from the obligation map gives
the same definition hash. Both target-parameter binding hashes also recompute
from their KORE symbol, Lean name/type, and source-rule link. See
`evidence/22-generated-target-source.txt`,
`evidence/24-independent-hash-reconciliation.txt`, and
`evidence/42-target-parameter-binding-hashes.txt`.

## Stage 5 Lean proof

### Fresh clean build and source integrity

The candidate tree hash is
`6205392a0960e0246652e4f3b373a82018e5856bdba8ba430959b18c98e5b052`,
exactly as recorded in `/audit-input.json`.

I created `/tmp/audit-work/lean-proof-audit.6hDcA5`, copied only the candidate
source/metadata files to its root, and copied the immutable generated project
to `Base`. Before adding audit-only query files, the copied `Base` tree hash
was exactly
`938bcc6b5f106c6110d6bb591324c505c20fcfe9d099b924848c7b0407826498`.

Both required commands succeeded:

```text
lake clean   -> exit 0
lake build   -> exit 0
```

The complete output is
`evidence/27-fresh-lake-clean-build-complete.txt`.

The candidate root defines only its two target parameters, supporting private
definitions/theorems, and `Proof.final`, all inside namespace `Proof`. It does
not define or shadow `Klean65CircularShift.Lemmas.targetStatement`. It contains
no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The immutable `Base`
target and its hash remain unchanged. See
`evidence/28-candidate-integrity-and-forbidden-scan.txt`.

### Proof identity

Lean reports the exact type:

```lean
Proof.final :
  Klean65CircularShift.Lemmas.targetStatement
    Proof.«Int2String(_)_STRING-COMMON_String_Int»
    Proof.«strToCodes(_)_MPY-STR_IntSeq_String?»
```

An audit-only `example` requiring exactly that fixed application accepts
`Proof.final` directly. The theorem is not a weakened, duplicated, or separate
vacuous proposition. Exact Lean output is
`evidence/32-proof-identity.txt`.

### Axiom accounting

Running Lean on a file containing exactly:

```lean
import Proof
#print axioms Proof.final
```

produces:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

The command exits 0; its exact output is
`evidence/29-print-axioms-Proof-final.txt`.

`propext` and `Quot.sound` are Lean core logical axioms, not candidate or
generated declarations. None of the 48 generated declarations recorded in
`trust-inventory.json` is a dependency of `Proof.final`. The inventory records
zero designated and zero other sorries. `sorryAx` is absent, and there is no
unrecorded candidate proof trust escape. The reconciliation is in
`evidence/30-axiom-trust-reconciliation.txt` and
`evidence/45-trust-inventory-summary.txt`.

## Operational bridge audit

The counterfactual tests are important: a constant `Int2String` or a
`strToCodes` that always returns `some []` can prove the bare definedness
target. Both counterfactual target proofs compile in the audit file. Their
outputs are observably wrong (`""` for `-120`, empty codes for `"A0-"`, and a
defined result for non-ASCII `"é"`). Thus the clean theorem alone is not being
used as bridge evidence.

The actual candidate definitions pass the independent operational check.

### `Int2String`

Binding:

- Lean parameter:
  `Proof.«Int2String(_)_STRING-COMMON_String_Int»`;
- type: `SortInt → SortString`, where generated sorts reduce to
  `Int → String`;
- KORE symbol:
  `LblInt2String'LParUndsRParUnds'STRING-COMMON'Unds'String'Unds'Int`;
- source rule:
  `rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf`.

The exact candidate definition is:

```lean
def «Int2String(_)_STRING-COMMON_String_Int»
    (value : SortInt) : SortString :=
  value.repr
```

Lean `Int.repr` emits `"0"` for zero, ordinary decimal digits for positive
integers, and a minus sign followed by decimal digits for negative integers.
This is the total operational meaning of K's `Int2String` hook. The candidate
also proves universally that every character in this representation is ASCII.

Independent witnesses agree on both sides:

| Input | Candidate | Supplied K execution |
|---:|---|---|
| `0` | `"0"` | completed assertion for `"0"` |
| `507` | `"507"` | completed assertion for `"507"` |
| `-120` | `"-120"` | completed assertion for `"-120"` |

The K run reaches `.K`, `NoExc`, and exit code `0`; see
`evidence/36-fixed-k-semantics-int2string-adversarial.txt`.
This is neither constant, identity, hard-coded to the theorem, nor otherwise a
convenient definedness-only implementation.

### `strToCodes`

Binding:

- Lean parameter:
  `Proof.«strToCodes(_)_MPY-STR_IntSeq_String?»`;
- type: `SortString → Option SortIntSeq`;
- KORE symbol:
  `LblstrToCodes'LParUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'String`;
- same exact source-rule link as above.

The candidate recursively processes `String.toList`:

1. empty input becomes `some .IntSeq`;
2. an ASCII head becomes `iCons(Int.ofNat head.toNat, recursiveTail)`; and
3. a head with code point at least 128 becomes `none`.

This matches the two frozen `strToCodes` rules constructor-for-constructor,
including the `< 128` guard and partiality. Candidate outputs include:

| Input | Candidate |
|---|---|
| `""` | `some []` |
| `"A0-"` | `some [65, 48, 45]` |
| code point `127` | `some [127]` |
| code point `128` | `none` |
| `"é"` | `none` |
| `"Aé"` | `none` |

The supplied K semantics completes independent ASCII assertions for the empty
string and `"A0-"`, including length and the three character codes. It rejects
non-ASCII and mixed ASCII/non-ASCII inputs at the residual
`strToCodes("\xe9")`, exit `113`, exactly corresponding to the candidate's
`none`. See
`evidence/37-fixed-k-semantics-strtocodes-adversarial.txt`,
`evidence/38-fixed-k-semantics-strtocodes-mixed-nonascii.txt`, and
`evidence/40-operational-bridge-ascii-boundary.txt`.

The exact candidate declarations and types are also printed by Lean in
`evidence/43-candidate-parameter-definitions.txt`.

The operational bridge therefore passes despite the target's ability to admit
convenient counterfactual implementations: the definitions actually supplied
implement the frozen operational meanings over their complete domains.

## Final judgment

The protected Stage 3 manifest is bijective with the independently
reconstructed inventory and classifies every rule correctly. The authenticated
Stage 4 producer deterministically emits exactly the required domain
obligation and fixed target. The fresh Stage 5 project clean-builds; its final
theorem has the exact target type, has clean axiom accounting, and uses honest
operational parameter definitions. No infrastructure mismatch, classification
defect, generation weakness, proof trust escape, or operational-bridge failure
was found.

VERDICT: PASS
LEGITIMACY: LEGIT
