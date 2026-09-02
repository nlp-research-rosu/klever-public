# Independent Stage 3–4 Audit: `48-is-palindrome`

## Result

The selected Stage 3 classification and deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` generation are legitimate. The launcher-recorded mode is
`CLASSIFICATION_ONLY`, so there is correctly no Stage 5 candidate or Lean proof
to audit.

I treated the mounted candidate/provenance material as untrusted evidence. I did
not rely on the earlier Stage 2 verdict or Stage 3 rationale as authority. The
classification below was reconstructed from frozen `verification.k`, the source
program, the K claim, and the supplied operational semantics.

## Signed inputs and producer authentication

`/audit-input.json` passes the trusted signed-resolution contract. Its canonical
resolution digest is
`7cf3d94b3865236563a64977dedc06e6abba3075c3d8b5611db3cc8e1df3a1a2`.
It records:

- problem `48-is-palindrome`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- audit mode `CLASSIFICATION_ONLY`;
- selected Stage 4 status `KLEAN_NO_OBLIGATIONS`;
- null Stage 4 target, Stage 5 result, Lean workspace, and Lean invocation.

Before judging Stage 4, I hashed the exact mounted producer sources:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Each value exactly matches both `source-manifest.json` and
`generator-manifest.json`. The immutable generator image is consistently
identified as
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
by the generator manifest, source manifest, and the image-keyed producer path
recorded in `/audit-input.json`. The producer bundle contains exactly the two
sources and its source manifest. Its independently recomputed tree hash
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
also matches the audit input. There is no producer-provenance infrastructure
error.

All other signed hashes were recomputed with the trusted hash algorithms. The
Stage 1 artifact tree, Stage 1 export tree, Stage 2 audit tree, discovery
manifest, complete Stage 4 generation tree, generated-project tree, and all 34
individual Stage 1 source hashes match exactly. The absent Stage 5 hashes are
both correctly null. Full per-file results are in
`evidence/05-recorded-hashes.txt`.

## Inventory reconstruction and bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. The local
verification-module closure contains only the local `VERIFICATION` module; its
imported `MPY` module is defined in the separately required supplied-semantics
files, not as another local module in `verification.k`.

The canonical inventory has exactly one entry:

| Field | Reconstructed value |
|---|---|
| Source span | `verification.k:9-10` |
| Module | `VERIFICATION` |
| Attributes | none |
| Normalized text | `rule palindrome(IS:IntSeq) => IS ==K buildIS(IS, isLen(IS) -Int 1, -1, -1)` |
| Normalized SHA-256 | `f5ed2b78f37cc7987423ef2f718f88456d091c4c95e893898cf03b437c6f3d3e` |
| `source_rule_id` | `rule-f5ed2b78f37cc7987423ef2f718f88456d091c4c95e893898cf03b437c6f3d3e` |

I separately normalized and hashed the physical source span without calling the
inventory helper. Canonical JSON hashing of the reconstructed singleton
inventory yields
`e73364f37cbe12afed7be35ee630275fbec7d6eb06ca1c28f719a2bf2cb9f87b`,
the same inventory hash returned by the trusted tool.

`/reference/lemma-discovery.json` has exactly that one identity in exactly that
order and exactly once. Its inventory hash is identical. There are no omissions,
duplicates, extras, reordered identities, changed spans, or changed hashes. The
trusted `validate_trust_boundary` check also passes.

## Independent classification judgment

The only rule is correctly classified `DEFINITION`.

Immediately before the rule, frozen `verification.k` introduces the fresh
function production:

```k
syntax Bool ::= palindrome(IntSeq) [function]
```

The rule is its sole defining equation. The symbol occurs in the frozen
workspace only in that production/equation and as the destination proof term in
`spec.k`. It does not match a `<k>` cell, call, continuation, environment,
heap, or any other operational state. It therefore does not replace or
accelerate execution and is not an `OPERATIONAL_RULE`. It asserts no pre-existing
mathematical fact and is not a `DOMAIN_LEMMA`. It was not presented as, nor used
as, a separately proved theorem, so it is not a
`PROVED_DERIVED_LEMMA`. It exactly meets the required `DEFINITION` category as a
named Boolean proof term.

The entry has no `simplification` attribute, so the special simplification
classification restriction is vacuously satisfied.

### Operational correspondence

The source implementation is:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

The supplied K semantics executes this body rather than intercepting the
program:

1. The ordinary function-call rules resolve and invoke the loaded
   `is_palindrome` closure, bind `text`, and execute its `Return`.
2. `text[::-1]` evaluates through the ordinary `Subscript`/`Slice` rules.
3. For a string with code sequence `IS`, `NoBound`, `NoBound`, and step `-1`
   reduce to slice start `isLen(IS) -Int 1`, stop `-1`, and step `-1`.
4. The string slice reduces to
   `str(buildIS(IS, isLen(IS) -Int 1, -1, -1))`.
5. String equality reduces through
   `applyCmp("==", str(A), str(B)) => A ==K B`.

Thus the program result is exactly the term used to define `palindrome(IS)`.
The definition summarizes the expected value after operational execution; it
does not bypass that execution.

Ground checks cover empty, singleton, even and odd non-palindromes, odd
palindromes, and boundary code values. An exhaustive finite check over alphabet
`{0,1,2}` through length five found the frozen `buildIS` recurrence identical
to sequence reversal. Counterfactual identity, constant-true, and positive-step
mutations are distinguished by `[97,98]`: the real definition is false, while
identity/constant-true would be true and positive step produces the wrong empty
sequence. These are finite sensitivity checks supporting the direct semantic
derivation, not substitutes for it.

The independent classification therefore contains:

- definitions: one;
- operational rules: zero;
- proved derived lemmas: zero;
- domain lemmas: zero.

The true domain-lemma set is genuinely empty.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` using:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`; and
- `/reference/klean-toolchain.lock.json`;

with `PYTHONPATH=/reference`.

The first attempt exposed an audit-container path-discovery problem: Lake could
not detect its installation, and direct `lean --version` failed to locate its
application even though the complete pinned toolchain was present under
`/opt/elan`. I preserved that failure. I then used the narrow source-preserved
shim in `evidence/app_path_shim.c`, which only supplies `/proc/<pid>/exe` for
processes named `lean` or `lake`; every other `readlink`/`readlinkat` call is
forwarded to libc. This changes no source, project, Lean expression, compiler
behavior, or checker logic.

With path discovery restored, the pinned tools report Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake
`5.0.0-src+ba2cbbf`, matching the lock. The trusted preflight exits 0 and
returns:

- status `KLEAN_NO_OBLIGATIONS`;
- zero obligations;
- null target;
- zero designated sorries;
- 50 generated trust declarations;
- successful `lake clean`;
- successful `lake build`.

The complete build output is seven short build lines plus
`Build completed successfully.` Its SHA-256 is
`d7a240983e021e4a054b8e4ff539320903c1a518aca6933d1b4e87964ee069b3`,
byte-for-byte identical to the generation-time diagnostic recorded in the
preflight and audit input. The successful returned preflight document otherwise
matches the recorded document field for field.

### Obligation and target identity

Only independently classified `DOMAIN_LEMMA` rules are eligible Stage 4 source
rules. That ordered eligible set is empty. Independently inspected Stage 4
artifacts contain:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`.

Both the source-rule and obligation identities are exact ordered bijections with
the empty eligible set. There can be no omitted, duplicated, irrelevant,
weakened, or vacuous conjunct because no conjunct exists. The obligation-map
hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`, and the generator obligation count is zero.

For a zero-obligation generation, the fixed target is absence of a target.
`generator-manifest.json`, `/audit-input.json`, the authenticated generator's
computed expected target, and independent target extraction all return null.
There is no target module and no `Target` declaration in any generated Lean
source. This is the exact required fixed generated target for
`KLEAN_NO_OBLIGATIONS`.

The 50 generated trust declarations are executable Klean boundary functions,
not a proposition target or proof. The trusted preflight independently matched
them to `trust-inventory.json`, rejected proposition trust, found no generated
`sorry`, `admit`, or `unsafe`, and clean-built the immutable generated tree.
Because there is no theorem target, these declarations cannot discharge a
missing obligation.

## Stage 5

Stage 5 proof checks are inapplicable. `AUDIT_MODE` and the signed resolution
are `CLASSIFICATION_ONLY`; `/candidate` does not exist; the Stage 5 result,
workspace, invocation, and hashes are null. This is exactly the required state
for a legitimate `KLEAN_NO_OBLIGATIONS` generation. No `Proof.final`,
candidate target shadowing, candidate trust escape, target parameter, or axiom
dependency exists to inspect.

## Evidence

Raw commands and decisive results are preserved under `evidence/`; the
preflight and hash-check outputs are complete:

- `00-mode-and-signed-input.txt`
- `01-producer-authentication.txt`
- `02-rule-inventory.txt`
- `03-classification-and-semantics.txt`
- `04-preflight.txt`
- `app_path_shim.c`
- `05-recorded-hashes.txt`
- `06-stage4-bijection-and-target.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
