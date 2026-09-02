# Independent Stage 3/4/5 Audit: `59-largest-prime-factor`

## Scope and mode

This audit covers condition `kit-semantics` with semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` record
`CLASSIFICATION_ONLY`. `/candidate` is absent, and the audit input has null
Stage 5 invocation, workspace, result, and hashes. Therefore the Stage 5 Lean
proof, candidate clean build, `#print axioms Proof.final`, and operational-
parameter bridge checks are not applicable.

All mounted Stage 1 through Stage 4 artifacts, including the earlier Stage 2
review, were treated only as untrusted evidence. Classification and structural
judgments below were reconstructed from the frozen source and trusted tools.

## Producer and input provenance

The generation-time producer files were hashed before judging Stage 4:

| Producer | Actual SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same in `source-manifest.json` and `generator-manifest.json` | Match |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same in `source-manifest.json` and `generator-manifest.json` | Match |

The source manifest contains exactly those two producer entries. Its generator
image ID and the generator manifest provenance both equal
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
The basename of the immutable producer-source path recorded in
`/audit-input.json` is the same digest. Thus there is no producer-source or
image-provenance infrastructure error.

All launcher-recorded hashes recomputed successfully using their designated
digest schemes:

| Input | Recomputed hash |
|---|---|
| Stage 1 workspace, pipeline tree | `53c58232fc1d47f0a4a1797cdb5fbe999cc36cd9ea47bd08850a17277fe2116e` |
| Stage 1 immutable export tree | `ec790395db866a37d15b915cd7971dbf63ee912a7004aa8b8bf958b9b315d1f3` |
| Stage 3 discovery manifest | `7a65832816deafca903240d6e73f17de3f4b20572c1908a9f7c072d3562d2578` |
| Generated project tree | `6d73c4aca521a689f39792e32fb908568e827aa6bae610958b9791849beaf29b` |
| Stage 4 generation artifact | `4df298acebccc12b4f6ccf8ea4cf9aafdd10c04d1b1996fab6f3cf75d7bb5f09` |
| Producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Selected Stage 2 artifact | `427d7e223a8ba4f61689e546a2246bcab8a2945e2396ccfc37788d5827ff98ec` |

The 768-entry Stage 1 per-file hash map is also exact: 768 regular files,
zero missing files, zero extra files, zero mismatched hashes, and zero
non-regular entries.

## Canonical local rule inventory

`tools.k_rule_inventory.inventory_verification` selected main module
`VERIFICATION` from `prove.sh` and reconstructed the local closure
`[VERIFICATION-SYNTAX, VERIFICATION]`. The frozen `verification.k` hash is
`5cd97d6db221c6a1ebf5e3e958892094b2dd9bdca1cbeee66edc58a6dc1b88a6`.

The canonical inventory contains exactly three rules, in source order:

| Span | `source_rule_id` / normalized SHA-256 | Attributes |
|---|---|---|
| 14–15 | `rule-c09d86f09f196dc6bfd7245139d77da63a26829d9dcf6ed5b3c1e876b4204f34` / `c09d86f09f196dc6bfd7245139d77da63a26829d9dcf6ed5b3c1e876b4204f34` | none |
| 17–19 | `rule-4c37787b8b69deb1e9173a83d853af7a8fe0ee7441fddb5263a9d691cadc23ac` / `4c37787b8b69deb1e9173a83d853af7a8fe0ee7441fddb5263a9d691cadc23ac` | none |
| 21–22 | `rule-de3529b439b11f78acab7501799690277d17c9e760bf812468bba7d69d04efd4` / `de3529b439b11f78acab7501799690277d17c9e760bf812468bba7d69d04efd4` | none |

The canonical whole-inventory hash is
`7b0c3a5cec95c8717ad8bdb6dce5cf1d85abf737e1ec48c0586929bb5e49d810`.
It matches the Stage 3 manifest, Stage 4 input manifest, and generator
provenance.

The Stage 3 ID sequence is byte-for-byte identical in order to the canonical
ID sequence. Both sequences are unique. Consequently there are no omitted,
duplicated, extra, reordered, or changed rule identities. The trusted Stage 3
contract validation also succeeds.

## Independent classification judgment

`lpfFrom(Int, Int)` is introduced in `VERIFICATION-SYNTAX` as a fresh K
function. Each inventory rule rewrites that summary symbol only; none matches
`<k>` or any program configuration.

1. Lines 14–15 are a `DEFINITION`. The equation defines the base value of the
   summary as `N` when `F >= 2` and `N <= F`, exactly the state in which the
   source loop exits and returns `n`.
2. Lines 17–19 are a `DEFINITION`. The recurrence covers `N > F` and
   `pyMod(N,F) == 0`, preserves `F`, and updates `N` to
   `(N - pyMod(N,F)) / F`. Supplied `int.k` defines Python `//` by that exact
   expression and Python `%` as `pyMod`, so this is the source loop's divisible
   branch expressed as a mathematical summary recurrence.
3. Lines 21–22 are a `DEFINITION`. The recurrence covers `N > F` and nonzero
   `pyMod`, preserves `N`, and advances `F` by one, exactly the source loop's
   else branch.

The guards are mutually exclusive and exhaustive on the proved `F >= 2`
domain: `N <= F`, or `N > F` split by zero versus nonzero remainder. Division
by zero is excluded. In the divisible branch positive `N` decreases; in the
nondivisible branch `F` advances toward `N`. The equations therefore form a
truthful, guarded recurrence for the loop summary.

These rules do not assert primality, factor membership, maximality, or another
independent mathematical fact. Relabeling any one as a `DOMAIN_LEMMA` would
misclassify a defining equation. They are not ordinary execution or
observation rules because their left sides are the fresh summary function, and
no rule is claimed as a proved derived lemma. No inventory rule has a
`simplification` attribute, so the simplification-class restriction is
vacuously satisfied.

The English HumanEval contract names the returned value as a largest prime
factor, while the frozen K postcondition is equality with the recursively
defined `lpfFrom`. This audit does not invent a missing rule or turn the
definition into a domain lemma: the Stage 3 task is a bijective classification
of the actual local rule inventory. The actual inventory contains no separate
primality or maximality proposition. Its genuine domain-lemma set is therefore
empty. Finite independent execution checks over inputs 2 through 5000, plus
the examples 13195 and 2048, found zero disagreement between the source loop
and the recurrence; direct rule/semantics comparison, rather than those finite
checks, is the classification basis.

## Deterministic Stage 4 generation

The independently determined domain set, the Stage 3 `DOMAIN_LEMMA` set, the
Stage 4 input `source_rules`, the obligation-map `source_rules`, and the
obligation list are all exactly `[]`. The obligation IDs are unique and the
recorded count is zero. This is an exact empty-to-empty source-rule/obligation
bijection, not an omission.

The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trust-inventory hash is
`51aafb2842cd913c116d510024aaad67e821a55df76e510c351be0fec277e07e`,
matching the export result.

For zero obligations, the trusted `expected_target_definition` and
`target_statement` functions both return null. The generator manifest,
launcher audit input, launcher-recorded Stage 4 preflight, and current export
all record a null target. No generated Lean target/final theorem declaration
exists. Hence there is no weakened, duplicated, vacuous, or changed target and
no target hash to reconcile. `KLEAN_NO_OBLIGATIONS` is the correct Stage 4
status.

The generated project retains 44 allowlisted executable-value trust
declarations, including an opaque executable interpretation of `lpfFrom`, but
contains no proposition trust and no theorem target. The trusted preflight
confirms zero generated `sorry` locations. With no target proposition and no
Stage 5 proof, these executable declarations cannot constitute a proof of a
weakened target.

## Mechanical preflight rerun

The required call to `tools.klean_preflight.check_generation` was made with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`, `/reference/klean-generation`, and the
pinned `/reference/klean-toolchain.lock.json`.

The first invocation exposed an audit-image issue: Lean 4.22 resolves its
executable using `/proc/<getpid()>/exe`, while this sandbox exposes host-
namespace `/proc` and a nested `getpid()`. The resulting path did not exist.
The evidence records both failed attempts and the diagnosis. A narrow
audit-local `LD_PRELOAD` shim redirected only `/proc/<digits>/exe` `readlink`
calls to `/proc/self/exe`; it did not modify any K, manifest, generated Lean,
or target file.

With that environment repair, the required checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `44`;
- `lake clean` exit `0`; and
- `lake build` exit `0`, ending with `Build completed successfully.`

Its frozen-input, discovery-manifest, and generated-tree hashes equal the
independently recomputed values. Its immutable-input snapshot check also passed,
so the direct build and preflight did not alter mounted provenance inputs.

## Stage 5 disposition

Stage 5 is correctly absent. `CLASSIFICATION_ONLY` has no generated target,
`/candidate` is absent, and all Stage 5 launcher fields are null. Running a
candidate proof, `Proof.final`, target-parameter bridge, or axiom audit would
fabricate a proof stage that this mode explicitly does not contain.

## Final judgment

The Stage 3 classification and the deterministic Stage 4 no-obligation export
are legitimate. The concern is narrower and does not change the empty-domain
classification: the frozen machine-checked theorem connects execution to the
recursively defined `lpfFrom`, but no frozen K rule, generated Lean obligation,
or Stage 5 theorem formalizes the separate number-theoretic statement that
`lpfFrom(N,2)` is the largest prime factor of `N`. That human-facing intent
bridge is mathematically plausible and finitely corroborated, but remains
outside the machine-checked chain. This warrants `CONCERNS`, not `FAIL`: no
domain rule was mislabeled, no true inventory domain lemma was omitted, and no
untrusted proof escape or weakened target was accepted.

## Evidence

Raw commands, exact outputs, executable check scripts, producer hashes,
inventory reconstruction, source/semantics excerpts, preflight failures and
repair, successful returned preflight evidence, structural target audit, and
finite branch witnesses are under `/audit-output/evidence/`. The reproduction
entry point is `/audit-output/evidence/COMMANDS.md`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
