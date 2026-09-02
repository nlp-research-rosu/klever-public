# Independent Stage 3/4 audit: HumanEval 119-match-parens

## Scope and result

The launcher-selected mode is `CLASSIFICATION_ONLY`; `/audit-input.json` and
`AUDIT_MODE` agree. The condition is `kit-semantics`, the semantics mode is
`SUPPLIED_SEMANTICS`, the selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`, all Lean-workspace and Stage 5 fields in the signed
resolution are null, and `/candidate` is absent. Stage 5 proof, axiom, and
operational-bridge checks therefore do not apply.

I treated all mounted prior prose, logs, and classifications as untrusted
evidence. I did not execute any script from the candidate or provenance trees.
The only imported code was the trusted tooling below `/reference/tools`; the
only compiled audit helper was the narrowly scoped `/proc` compatibility shim
described below.

## Producer authentication and frozen inputs

Producer authentication passed before Stage 4 was judged:

| Item | Recomputed SHA-256 | Required value | Result |
|---|---|---|---|
| `generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| `generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| Producer bundle, pipeline tree algorithm | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | `/audit-input.json` | Match |
| Generator image | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` | Source manifest, generator provenance, and launcher bundle basename | Match |

The source bundle contains exactly `klean.py`, `klean_export.py`, and
`source-manifest.json`. The signed audit envelope digest is
`d3508b9a9e025499e32b336ea41379a7c0d2399f7cff14181bf8ed3ed11d8105`.
Using the launcher's trusted pipeline tree algorithm, all four recorded mounted
tree hashes matched: Stage 1 K workspace `5823e593…`, selected Stage 2 audit
`5eb0b522…`, Stage 4 generation `8dbf863c…`, and producer bundle `388cac39…`.
All 777 recorded Stage 1 file paths and per-file hashes were present and equal.
The separate deterministic-export workspace digest is
`97d6dc8f3dc2cf4265d6e9663e9a1efb41674e22b2c8c11ab347e57a3b9f6182`,
also matching the input manifest, generator provenance, export result, fresh
preflight, and audit input.

Full evidence: [producer authentication](evidence/01-producer-auth.json) and
[commands](evidence/COMMANDS.md).

## Canonical rule inventory reconstruction

I invoked `tools.k_rule_inventory.inventory_verification` directly on the
frozen `/reference/k-proof`. `prove.sh` selects main module `VERIFICATION`.
The trusted local-module closure contains only `VERIFICATION`: its import
`MPY` is supplied semantics from another required file, not a local module in
`verification.k`. The reconstruction found 16 rules, all unique and in source
order.

- `verification.k` SHA-256:
  `8ca11d31d5616b1c7cbe0af0ece1296b7baca3c3bf164f5adacd69413634030b`.
- Canonical inventory SHA-256:
  `f0ac74e960f507aef4fa9453b392fd9c8075bd1ed5b645532becd82a9e24645f`.
- Discovery manifest SHA-256:
  `107dcd43143fe5ee254e2ae2f31e3a217b71240604165dce75fb952359aabd02`.

For every entry I recomputed the exact start/end source span, normalized source
hash, and `source_rule_id`. The 16 discovery IDs equal the 16 canonical IDs in
the same order. Both sides contain 16 unique IDs; there are no missing, extra,
duplicated, or reordered identities. The discovery inventory hash equals the
recomputed inventory hash. The complete per-rule source, span, attributes,
normalized hash, and full ID are preserved in the
[reconstructed inventory](evidence/02-rule-inventory.json).

## Independent Stage 3 classification

I reclassified the rules from the frozen source, source solution, formal
postcondition, and supplied operational semantics. The result independently
agrees with Stage 3: every entry is `DEFINITION`; the other three sets are
empty.

| Entries | Lines | Defined symbol | Independent class | Reason |
|---|---:|---|---|---|
| 0–1 | 8–10 | `parenCodes` | `DEFINITION` | Empty/cons constructor equations define the parenthesis-only input predicate. |
| 2–3 | 15–20 | `nextBalance` | `DEFINITION` | Complementary guarded equations define the source loop's `+1`/`-1` update. These are the only `simplification` rules. |
| 4–5 | 23–25 | `scanBalance` | `DEFINITION` | Empty/cons structural recurrence defines final balance from a starting balance. |
| 6–7 | 28–31 | `nextMinimum` | `DEFINITION` | Disjoint/exhaustive `<` and `>=` cases define `min(newBalance, oldMinimum)`. |
| 8–9 | 34–39 | `scanMinimum` | `DEFINITION` | Empty/cons recurrence defines the minimum reached while scanning, using the post-update balance. |
| 10–11 | 42–44 | `scanLast` | `DEFINITION` | Empty/cons recurrence names the `for` target's final value, including the empty-loop prior value. |
| 12 | 49–51 | `goodParens` | `DEFINITION` | Transparent named predicate for zero final balance and nonnegative minimum prefix balance. |
| 13 | 54–55 | `possibleMatch` | `DEFINITION` | Transparent named disjunction over the two concatenation orders. |
| 14–15 | 58–63 | `matchAnswer` | `DEFINITION` | Complementary guarded cases define the exact `Yes`/`No` code sequences. |

This is a classification by behavior, not by naming. Every left-hand side is
headed by the fresh function declared immediately above it, and every rule is
a base equation, structural recurrence, transparent macro-like equation, or
guarded defining case. No rule matches a `<k>` configuration or any other
execution cell, so none is an ordinary execution/observation rule. No rule
states a property solely about pre-existing symbols, so none is a domain
lemma. No rule was first proved in a module omitting it and later installed;
therefore none qualifies as `PROVED_DERIVED_LEMMA`. The two simplification
rules are genuine guarded defining cases, satisfying the special
simplification restriction.

The potentially load-bearing `goodParens`, `possibleMatch`, and `matchAnswer`
rules remain definitions rather than disguised domain lemmas. They introduce
and transparently reduce named symbols. The frozen source itself tests final
balance and minimum, then tries the reverse concatenation, then returns the
same two strings. These equations do not assume that a pre-existing result has
the requested property.

### Operational-semantic and mathematical check

The supplied semantics represents strings as `str(IntSeq)`, iterates them one
one-character `str(iCons(C,.IntSeq))` at a time, implements string `+` by the
structural `seqConcat`, lowers `For` through `#loop`, and implements integer
augmented assignment and comparison with the expected `+Int`, `-Int`, and
integer relations. Its ASCII literal rule gives code 40 for `(` and code 41
for `)`. The theorem's `parenCodes` precondition restricts characters to those
two codes, while the frozen source's `else` branch decrements for every
non-`(` character; thus `nextBalance` exactly matches the operational branch
on the entire formal input domain.

Induction on the `IntSeq` constructor shows that `scanBalance` is the source
loop's balance after all characters; a simultaneous induction shows that
`scanMinimum` is the minimum of the starting minimum and all post-update
balances. `scanLast` follows the iterator's one-character yields. Therefore
`goodParens` is exactly the pair of tests in each source block,
`possibleMatch` exactly covers `A+B` and `B+A`, and `matchAnswer` names the
source's exact returned string.

As finite corroboration, independent implementations of the frozen control
flow and these recurrences agreed on all 16,129 pairs whose component lengths
are 0 through 6. Counterfactuals were discriminating: `")"` rejects an
incrementing else branch and a pre-update minimum; `(")", "(")` requires the
second order; and `(")", ")")` rejects a constant-`Yes` result. This finite
check supports but does not replace the inductive argument. See
[semantic probes](evidence/06-semantic-probes.txt).

The independently determined true domain-lemma set is therefore genuinely
empty.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation,
and pinned toolchain lock. Its temporary fresh copy passed both `lake clean`
and `lake build`:

| Command | Exit | Complete output SHA-256 |
|---|---:|---|
| `lake clean` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `lake build` | 0 | `c20f22ca7a4272866393d788edf5b8bd013b45b8798c70db9d70506fa82caadb` |

The returned result is `KLEAN_NO_OBLIGATIONS`, with obligation count 0,
target null, generated tree
`2c034fdfe4cbadcd2a7ebf2f47db1274b66946bda9e065da93c29e5c39889abc`,
no designated sorries, and 42 generated executable trust declarations. The
build output is exactly the same complete output and hash recorded by the
immutable generation. The preflight separately rejects proposition trust;
there is no generated proposition or proof depending on those executable
declarations in this no-obligation case.

The audit container initially prevented Lean and Lake from finding their
installation because `getpid()` returned a nested namespace PID while numeric
`/proc/<pid>/exe` exposed only the host PID. Lean 4.22 uses that numeric path.
I preserved all failed outputs, then used an audit-only `LD_PRELOAD` shim that
first performs the original `readlink` and retries only an `ENOENT` for the
exact `/proc/<digits>/exe` shape as `/proc/self/exe`. With it, the pinned
binaries reported Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`,
and the unmodified trusted preflight passed. The shim did not alter mounted
inputs or compiler output. Source, hashes, failures, and final result are in
[preflight diagnostics](evidence/03-preflight.txt),
[shim source](evidence/proc-self-readlink.c), and
[returned preflight evidence](evidence/04-preflight-result.json).

### Manifest bijection and target identity

Independent of the preflight result, I loaded and cross-checked every sidecar:

- Input-manifest definitions exactly equal the canonical validated 16-rule
  definition sequence, including order and provenance. Its operational and
  proved-derived lists are empty.
- The independently determined `DOMAIN_LEMMA` list is empty. Accordingly,
  `input-manifest.json` has `source_rules: []` and `obligation-map.json` has
  `source_rules: []`, `obligations: []`, and `trust_parameters: []`.
- The obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly the generator-manifest value. The source-rule/obligation map is the
  unique empty-to-empty bijection: there can be no omission, duplication,
  weakening, irrelevant obligation, or vacuous conjunct.
- The generator and export obligation counts are zero, and the export status
  is `KLEAN_NO_OBLIGATIONS`.
- Trusted `target_statement` independently returned null. The generator
  manifest, audit input, and launcher-recorded Stage 4 preflight also record
  target null. There is no generated target declaration, statement, or hash
  to change, and `/candidate` is absent.
- Generated tree, workspace, discovery, inventory, verification, obligation
  map, trust-inventory, and export linkage hashes all recomputed and matched.
  The pinned toolchain object exactly equals `klean-toolchain.lock.json`.

The full check matrix and sidecar hashes are in
[manifest and bijection evidence](evidence/05-manifest-bijection.json).

Because the mathematical reclassification—not merely the manifests—finds no
domain lemma, the selected no-obligation status is legitimate. Stage 4 did not
drop a true domain obligation, generate a substitute theorem, or permit a
Stage 5 proof for a null target.

VERDICT: PASS
LEGITIMACY: LEGIT
