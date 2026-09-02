# Independent Stage 3–5 audit: `95-check-dict-case`

## Scope and result

The launcher mode is `CLASSIFICATION_AND_PROOF`; the condition is
`kit-semantics`, and the semantics mode is `SUPPLIED_SEMANTICS`.

The Stage 3 classification is correct, and the Stage 4 files are structurally
self-consistent and provenance-bound. The audit nevertheless fails
mathematically and operationally:

1. The generated Lean carrier omits the frozen K `Str` sort and its
   `str(IntSeq) → Iterable → Val` constructor path. Therefore, under an honest
   interpretation of the frozen symbols, no generated `SortVal` satisfies
   `isStringKey`. Both fixed target conjuncts have an empty honest guard domain.
2. The candidate works around the missing constructor by treating
   `boundMethodV(setV(codes), "$KLEAN::MPY::RESERVED::STR$")` as a string.
   That term is an existing non-string frozen K value, not an encoding of
   `str(codes)`. Frozen K proves it is not a string and leaves its `islower`
   method application stuck, while the candidate says it is a string and
   returns a Boolean result.

Thus the clean Lean proof proves the fixed syntactic target only under
operationally false parameter definitions. It does not discharge the two real
K domain lemmas.

## Producer provenance and infrastructure

The producer provenance is intact; there is no producer-source `AUDIT_ERROR`.

- `klean_export.py` observed SHA-256:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py` observed SHA-256:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- Both values exactly match `generator-manifest.json` and
  `source-manifest.json`.
- Generator image ID in the generator manifest, source manifest, and the
  `/audit-input.json` producer-bundle path is exactly
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
- The trusted pipeline tree hash of `/reference/generation-tools` is
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
  exactly the audit-input value.
- The mounted producer files are byte-identical to the trusted mounted tool
  copies.

The first preflight attempt exposed a container PID/procfs mismatch: Lean used
a namespace PID to resolve `/proc/<pid>/exe`, while `/proc` exposed host PIDs.
The narrow documented `LD_PRELOAD` shim used for the rerun changes only
`getpid()` to return `/proc/self/status`'s host `Pid`. It restored the pinned
Lean 4.22.0 executable without changing any input, generated source, target, or
candidate file. The required preflight then completed successfully.

Raw evidence:
[producer provenance](/audit-output/evidence/00-mode-producer-provenance.txt),
[runtime and clean build](/audit-output/evidence/05-lean-runtime-and-clean-build.txt).

## Stage 3 inventory reconstruction

The trusted inventory code reconstructed only the local closure of the selected
`VERIFICATION` module in `verification.k`, as required:

- verification SHA-256:
  `cd3a6bdc6c1985b56fdff715b06106a6a7dddcaf3e5f7725de86b1e9f517c152`
- closure: `["VERIFICATION"]`
- inventory SHA-256:
  `da6d570ca5aad66979a01df14308854813e040e7b91e7662cc90b7713d10cb67`
- rule count: 6

The protected manifest has exactly the same six IDs in the same order. All IDs
are unique; there are no omissions, extras, duplicates, reordered identities,
span changes, normalized-hash changes, or whole-inventory-hash changes.

| Span | Source rule ID suffix | Independent classification | Judgment |
|---|---|---|---|
| 9–30 | `81fe…2549` | `DEFINITION` | Exact expansion of the named `checkDictLoopBody()` AST helper. It names syntax and does not replace execution. |
| 33–37 | `1162…98b5` | `DEFINITION` | Exact expansion of the named `checkDictReturn()` AST helper. |
| 40–50 | `08f1…44f7` | `DEFINITION` | Exact expansion of the complete named function-body AST helper. |
| 54–57 | `abdb…8b5c` | `DOMAIN_LEMMA` | Guarded symbolic `applyMethod(V,"islower",.Vals)` simplification. It is not the exact constructor rule and was not first proved as this rule. It is directly relevant to the program and postcondition. |
| 58–61 | `fd44…0b8c` | `DOMAIN_LEMMA` | The analogous guarded `isupper` simplification. It is relevant, unproved in this exact form, and load-bearing. |
| 66–71 | `3c57…c962` | `PROVED_DERIVED_LEMMA` | Exact `isinstance(_,str)` bridge with the same guard and arbitrary continuation. It was independently proved first against bridge-free `CONNECTION`, then used in the later loop/target theory. |

Both rules carrying `[simplification]` are classified as either `DEFINITION`
or `DOMAIN_LEMMA`—here both are correctly `DOMAIN_LEMMA`. There are no
`OPERATIONAL_RULE` entries in this local closure.

For the derived rule, I rebuilt `CONNECTION` from frozen source in a fresh
workspace. `CONNECTION` imports `PROOF-THEORY` but neither requires nor imports
`verification.k`/`VERIFICATION`. The exact `CONNECTION-SPEC.isinstance` claim
proved `#Top`. I then independently built `VERIFICATION`; the loop proved
`#Top`, followed by the loop-plus-target proof with the loop trusted, also
`#Top`. This reproduces the required prove-first/use-later order rather than
trusting an earlier log.

Raw evidence:
[inventory](/audit-output/evidence/01-rule-inventory.txt),
[independent K checks](/audit-output/evidence/02-stage3-independent-k-checks.txt).

## Stage 4 structural integrity

The required trusted call to `tools.klean_preflight.check_generation` returned:

- status: `PASS`
- Stage 1 export hash:
  `600a94330d6d54e848d21beeacd868bf25b75406953ee7a68c18f1637275532c`
- discovery manifest hash:
  `2fad431056250f140d0f7f2fe3849e2cc431486a7325e0aa20dc1eeb070d55c7`
- generated tree hash:
  `421f3b002c1d56266949d340367f5657d5e54d77e0a70cd81246f9773da9e916`
- obligation count: 2
- generated trust declarations: 41
- clean/build diagnostics: both exit 0

Independent hashing also matched the audit input for the Stage 1 pipeline tree,
Stage 1 export, discovery manifest, selected generation tree, producer tree,
and generated project tree.

The independently classified domain set contains exactly:

1. `rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c`
2. `rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c`

Those two IDs occur exactly once and in that order in `source_rules` and
`obligations`. Their spans, normalized hashes, inventory hash, discovery hash,
and Lean conjunct hashes all match. The first conjunct expresses the guarded
`islower` equality; the second expresses the guarded `isupper` equality.
There is no missing or duplicate source obligation. Because the genuine domain
set has two entries, `KLEAN_NO_OBLIGATIONS` would not have been valid.

The generated target is byte-for-byte the producer-expected conjunction:

- declaration: `Klean95CheckDictCase.Lemmas.targetStatement`
- definition SHA-256:
  `d09d5b0be50ff5667570dd7a99f5d11e8e0638300ca0b6ac88bb1499108646b0`
- statement SHA-256:
  `2e9b768e4bd8906c2431172b343da5b25d23f0885a1a59d702414c218ded046b`

The extracted target equals both `generator-manifest.json` and
`/audit-input.json`.

Raw evidence:
[preflight result](/audit-output/evidence/03-preflight.json),
[Stage 4 integrity](/audit-output/evidence/04-stage4-integrity-and-carrier.txt).

## Stage 4 mathematical failure: lost string carrier

Mechanical bijection is not mathematical adequacy. The frozen semantics has:

```k
syntax Str ::= str(IntSeq)
syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | ...
syntax Val ::= ... | Iterable | ...
```

The frozen proof theory makes the domain precise:

```k
rule isStringKey(str(_:IntSeq)) => true
rule isStringKey(_:Val) => false [owise]
rule stringCodes(str(CS:IntSeq)) => CS [simplification]
```

The compiled frozen KORE likewise contains `SortStr` and the
`Lblstr... : SortIntSeq → SortStr` constructor.

In contrast, generated `Sorts.lean` has no `SortStr`. Its `SortIterable`
constructors are list, range, tuple, zip, and zipS only. Its `SortVal` has no
string constructor either. Therefore:

- there is no generated value corresponding to frozen `str(CS)`;
- an honest `isStringKey : SortVal → Bool` is false on every generated value;
- an honest `stringCodes` has no source-relevant string input on which to
  implement its constructor equation; and
- the guard in each generated conjunct has an empty honest domain.

This is a vacuous weakening of both nonempty, source-relevant domain lemmas.
The target file and hash were not changed by the candidate; the fixed generated
target itself lost a required frozen constructor.

## Stage 5 mechanical checks

A fresh project was created at
`/tmp/audit-work/stage5-proof.Ib1FOg`, with the immutable generated project
copied as `Base`. Under the documented PID shim:

- `lake clean`: exit 0, no output
- `lake build`: exit 0, “Build completed successfully.”

After the build:

- `Base` still hashes to
  `421f3b002c1d56266949d340367f5657d5e54d77e0a70cd81246f9773da9e916`;
- the target still equals the manifest and audit input;
- the candidate defines no `targetStatement`, so it does not shadow it;
- the candidate has no `sorry`, `admit`, `unsafe`, new `axiom`, or new
  `opaque`; and
- every target parameter has exactly one candidate `def`.

`#print Proof.final` confirms that its type is exactly the fixed target applied
to the eight candidate definitions in manifest order. It is not a duplicate or
textually weakened theorem. Its proof term is two `Eq.refl` terms; the guard
argument `h` is unused.

`#print axioms Proof.final` printed exactly:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

The generated trust inventory records 41 List/Map/Set hook declarations.
`Proof.final` depends on none of them. `propext` and `Quot.sound` are standard
Lean core axioms explicitly allowed by the trusted final-gate code. There is no
`sorryAx`, no candidate trust declaration, and no unrecorded proof escape. The
trusted `check_proof_candidate` gate independently returned `PASS` with the
same two used axioms.

These are necessary mechanical successes, but they do not repair the
operational failure.

Raw evidence:
[clean build](/audit-output/evidence/05-lean-runtime-and-clean-build.txt),
[identity and axioms](/audit-output/evidence/06-proof-identity-and-axioms.txt).

## Stage 5 operational-bridge audit

| Target parameter | Candidate definition vs. frozen meaning | Result |
|---|---|---|
| `_andBool_` | Boolean `&&`; truth-table probes match K `andBool`. | Pass |
| `applyMethod` | Hard-codes `islower`/`isupper` for every receiver with no arguments via `totalStringCodes`. For the invented receiver, frozen K has no matching `applyMethod` rule and is stuck. | **Fail** |
| `isRefV` | True only on `ref(_)`; false on `cellRef(_)` and other constructors, matching frozen `core.k`. | Pass |
| `isStringKey` | True on the invented `boundMethodV(setV(CS),tag)` carrier. Frozen `isStringKey` is true only on `str(CS)` and false on this term. | **Fail** |
| `lowerKeyCodes` | Recursive ASCII `hasLower && !hasUpper`, matching frozen proof theory and method rules on `IntSeq`. | Pass |
| `notBool_` | Boolean negation, matching frozen semantics. | Pass |
| `stringCodes` | Extracts codes from the invented carrier and returns empty codes otherwise. The alleged carrier is not a frozen string, while the actual frozen `str(CS)` carrier is absent from Lean. | **Fail** |
| `upperKeyCodes` | Recursive ASCII `hasUpper && !hasLower`, matching frozen proof theory and method rules on `IntSeq`. | Pass |

The encoding is not a harmless representation isomorphism. It reuses existing
constructors for a distinct frozen value:

```text
boundMethodV(setV(CS), "$KLEAN::MPY::RESERVED::STR$")
```

`boundMethodV` and `setV` both already have their own frozen operational
meanings. Thus the representation collides with a legitimate non-string value
and cannot preserve the frozen constructor algebra.

For `CS = [97]` (`"a"` in the frozen ASCII code model), Lean evaluated:

- candidate `isStringKey(inventedCarrier) = true`;
- candidate guard = `true`;
- candidate `lowerKeyCodes(CS) = true`; and
- candidate `applyMethod(inventedCarrier,"islower",.Vals) = true`.

Against the independently rebuilt frozen K definition:

- the exact claim
  `isStringKey(boundMethodV(setV([97]),tag)) => false` proved `#Top`; and
- the claim that
  `applyMethod(boundMethodV(setV([97]),tag),"islower",.Vals) => true`
  exited 1 with `WarnStuckClaimState`, leaving that exact `applyMethod` term
  unreduced.

This directly exhibits value and execution disagreement, not merely a missing
comment or incomplete test.

A counterfactual Lean theorem then instantiated the same generated target with
constant-false Boolean operations and predicates, a constant `noneV` method
result, and constant empty codes. It still proved because the guard was made
false. This confirms that the generated proposition alone does not bind the
parameters to their KORE meanings; the operational audit is load-bearing.

Raw evidence:
[operational adversarial checks](/audit-output/evidence/07-operational-bridge-adversarial.txt).

## Final judgment

Stage 3 is classified correctly and both mechanical Lean gates are clean.
However, Stage 4 loses the only constructor that makes the two domain
obligations nonvacuous, and Stage 5 replaces it with a constructor-colliding
non-string surrogate. The adversarial K/Lean comparison proves a concrete
semantic disagreement. A successful build, exact target type, and clean axiom
list cannot legitimize that operational bridge.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
