# Independent audit: 82-prime-length / kit-semantics

## Scope and result

I independently audited the frozen Stage 1 K workspace, protected Stage 3
classification, and selected deterministic Stage 4 generation for HumanEval
problem `82-prime-length` under `SUPPLIED_SEMANTICS`. I did not rely on the
prior Stage 2 verdict, prior reviews, logs, comments, or candidate-authored
claims.

The environment variable `AUDIT_MODE` and `/audit-input.json` both say
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, both recorded Lean workspace
hashes are null, and no Stage 5 proof audit is applicable.

## Mandatory producer-integrity gate

I hashed the two generation-time producer sources before judging Stage 4:

| File | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same |

Those hashes agree with `/reference/generation-tools/source-manifest.json`
and `/reference/klean-generation/generator-manifest.json`. The generator image
ID in both manifests is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`,
which is also the image ID encoded in the launcher-recorded producer-source
path. The exact three-file producer bundle hashes to
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching `/audit-input.json`. The infrastructure `AUDIT_ERROR` condition is
therefore absent. Raw evidence is in `evidence/01-producer-integrity.txt`.

## Canonical rule-inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code with
`/reference/k-proof`, I reconstructed the local module closure selected by the
frozen `verification.k` build. The closure, in canonical order, is
`VERIFICATION-SYNTAX`, `VERIFICATION`. The frozen file SHA-256 is
`13fab2c1c0831dfe83960aea67ea45932516ff618349ac9d3e94e50158e32a8a`.

The canonical inventory contains exactly these four rules:

| Span | Normalized SHA-256 / source rule ID | Independent class |
|---|---|---|
| `verification.k:20-21` | `0d84adc0fbe6fe3c0ad834b7cabaec34b6f1a14a37b1d97e6309a591d770d73e` / `rule-0d84adc0fbe6fe3c0ad834b7cabaec34b6f1a14a37b1d97e6309a591d770d73e` | `DEFINITION` |
| `verification.k:23-25` | `f7636d5013012b53a727f7a69e19eee33049f6844171d011930dcbc50544e7b5` / `rule-f7636d5013012b53a727f7a69e19eee33049f6844171d011930dcbc50544e7b5` | `DEFINITION` |
| `verification.k:27-29` | `c788496123caab512e57df64b2dd0261154d3d075835223008964c8feddfab13` / `rule-c788496123caab512e57df64b2dd0261154d3d075835223008964c8feddfab13` | `DEFINITION` |
| `verification.k:31` | `835478f853e5b3aed5797027e0534f3648fdf19cc84cf0cc5b7ef40a0675b715` / `rule-835478f853e5b3aed5797027e0534f3648fdf19cc84cf0cc5b7ef40a0675b715` | `DEFINITION` |

The recomputed whole-inventory hash is
`769426b2163a87c782102e56a3bed0a12ffc57f4f5045ad2ec51f22e842de036`.
It matches Stage 3. The Stage 3 ID sequence is identical to the canonical
source sequence, both lists are unique, and their sets are equal. Thus there
are no omissions, duplicates, extras, reordered identities, changed spans, or
changed normalized hashes. The trusted Stage 3 contract validator also
accepted the bijection. Full reconstructed rule text and IDs are in
`evidence/02-rule-inventory.txt`.

## Independent classification judgment

All four entries are definitions in the sense required by this audit, not
mislabelled domain facts:

1. Lines 20-21 are the guarded base equation for the named `trialPrime`
   summary: once `D >= N` on its declared `D >= 2` domain, the accumulated
   Boolean `P` is the result.
2. Lines 23-25 are the divisible-case recurrence. While `D < N`, a divisor
   advances the summary state to `D + 1` with accumulated result `false`.
3. Lines 27-29 are the complementary nondivisible recurrence. They advance to
   `D + 1` while preserving `P`.
4. Line 31 is a wrapper definition initializing the recurrence at divisor 2
   with `P = (N >= 2)`.

This classification agrees with the supplied operational semantics. `len` of
a modeled string reduces to `isLen`; integer `%` reduces through `pyMod`;
comparison dispatch supplies `<`, `>=`, and `==`; assignment updates the
current scope; and the while rules execute the body exactly while `D < N`.
Consequently the source loop and `trialPrime` make the same state transition:
test `N % D`, optionally set `P` false, increment `D`, and return `P` at loop
exit. These rules name and recursively compute that summary; they neither
rewrite a `<k>` execution configuration nor state an independent mathematical
theorem.

The three `trialPrime` guards are pairwise disjoint and exhaustive for every
`D >= 2`. Each recursive equation increases `D` by one, strictly decreasing
the remaining `N-D` measure while `D < N`. No inventory rule has the
`simplification` attribute. There is no claimed `PROVED_DERIVED_LEMMA`, so no
unproved rule is being passed off as a previously derived theorem.

As finite sensitivity evidence, I compared the source transition system with
the recurrence for every length 0 through 30; all outputs agreed. Mutating the
divisible branch fails at length 4, mutating the nondivisible branch fails at
length 3, mutating the base equation fails for state `(N,D,P)=(4,4,false)`,
and mutating the wrapper initialization fails at length 0. These tests support
the structural reasoning and show that none of the four definitions is
irrelevant or vacuous. Commands and complete output are in
`evidence/03-classification-operational-check.txt`.

The independently reconstructed classification is therefore:

- `DEFINITION`: 4
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The true domain-lemma set is genuinely empty.

## Stage 4 structural preflight

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required frozen workspace, Stage 3 manifest, Stage 4 generation, and
pinned toolchain lock. The first attempt exposed a sandbox-specific Lean
runtime issue: this environment exposes `/proc/self/exe` but not
`/proc/<getpid>/exe`, while the pinned Lean 4.22 runtime uses the latter in
`lean_io_app_path`. I used a recorded local compatibility shim that redirects
only that exact `readlink` request to `/proc/self/exe`; every other `readlink`
is forwarded unchanged. The shim source and binary hashes and the successful
pinned Lean version check are recorded in
`evidence/04-lean-sandbox-compatibility.txt`.

With that environment-only compatibility fix, the unchanged trusted preflight
returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- frozen/Stage 1 digest:
  `b20ae20bcb603d10b86dcb9787fa672d7ef71d338f044d132eaf2217432b5949`;
- Stage 3 manifest digest:
  `34bdea4f70053dcc60a6d72610cd6d89f82454bdef8fbdbe48d5c8e81348e05e`;
- generated-tree digest:
  `e0c59505c3464b8bda84b1e8a90313397264005647f44abaaafe8045e90f7fa5`;
- obligation count: 0;
- target: null;
- designated sorry count: 0; and
- `lake clean` exit 0 followed by `lake build` exit 0.

The exact returned JSON and build tail are in
`evidence/05-check-generation.txt`.

## Independent manifest, obligation, and target checks

I separately recomputed and matched all launcher-recorded digests: the signed
resolution digest, pipeline Stage 1 tree, Stage 1 export tree, Stage 3 file,
selected Stage 2 tree, selected Stage 4 tree, producer-source bundle, and
generated project tree. All 778 launcher-recorded Stage 1 per-file hashes have
the same names and bytes; there are no missing, extra, or mismatched entries.
The Stage 4 sidecar and obligation-map hashes also agree, including:

- obligation-map SHA-256:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust-inventory SHA-256:
  `52b4bc7ea97cd96ba3d9318a18c2262116332a5f686fdfa935a63ad0d1f549b5`.

The Stage 4 input manifest's four definitions equal the independently
validated Stage 3 definition records exactly. Its operational-rule and
proved-derived-lemma lists are exactly empty, and its domain source-rule list
is exactly the independently reconstructed empty domain set. Across all four
classification buckets, every canonical inventory ID occurs exactly once in
canonical order. Its 25 required K files are exactly the recursively resolved
`requires` closure of `verification.k`, with no spec-mutation artifacts. Its
summary-function signatures, verification module, syntax module,
`verification.k` hash, modeled hooks, and pinned toolchain all agree with the
frozen inputs and generator manifest.

The exact source/obligation sequences are all empty and equal:

```text
independent DOMAIN_LEMMA IDs = []
input-manifest source IDs    = []
obligation-map source IDs    = []
obligation IDs               = []
trust parameters             = []
```

Thus the source-rule/obligation map is bijective. There are no obligations to
weaken, duplicate, omit, make vacuous, or replace with an irrelevant
conjunct. Generator manifest, export result, recorded preflight, and actual map
all report obligation count zero.

Target identity is also exact for this no-obligation case. The generator
manifest, audit input, and recorded preflight all bind the target to null. An
independent scan found no `def targetStatement` in any generated Lean source,
and the trusted producer-side target parser returned null. There is therefore
no changed, duplicated, weakened, or vacuous target. Raw hash, bijection, and
target evidence is in `evidence/06-independent-hash-and-bijection-check.txt`;
classification-bucket and required-closure evidence is in
`evidence/07-manifest-classification-buckets.txt`.

## Stage 5 applicability and final judgment

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the legitimate
Stage 4 result. The required consequences hold: there is no generated target
and no Stage 5 candidate. Accordingly, proof-mode-only checks such as a fresh
candidate copy, candidate shadowing review, `Proof.final`, `#print axioms`, and
candidate operational-bridge parameter validation are not applicable. The 44
preflight-counted generic generated trust declarations cannot support a proof
here because no target theorem or Stage 5 proof exists.

The Stage 3 classification is complete and mathematically appropriate, Stage
4 is structurally and semantically faithful to the genuinely empty domain set,
and the selected no-obligation status is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
