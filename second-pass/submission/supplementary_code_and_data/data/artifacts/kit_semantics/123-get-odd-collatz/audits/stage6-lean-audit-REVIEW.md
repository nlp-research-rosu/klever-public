# Independent audit: `123-get-odd-collatz`

Audit mode was `CLASSIFICATION_AND_PROOF`; condition was `kit-semantics`;
semantics mode was `SUPPLIED_SEMANTICS`. I treated every mounted candidate,
manifest narrative, prior review, and log as untrusted evidence. Conclusions
below come from the frozen sources, the trusted inventory/preflight/final-gate
code, fresh Lean runs, and independent mathematical inspection.

## Input and producer integrity

All hashes that can be recomputed from the mounted inputs match
`/audit-input.json`:

| Input | Recomputed hash |
|---|---|
| Stage 1 workspace, launcher tree hash | `9d9e1af69cc2b0fbd1db65326e55c9797a948c45a74650e6ca7ffab9ec0cbdc8` |
| Stage 1 deterministic-export tree hash | `b2c8dda938b3e858f612f9ba9ef4323859eed6282b8cf0c39e54ff4f308ca237` |
| Stage 2 audit tree | `ae5aaeb37af4fea842b3d6dacf6fc5e27723045fa7534c5734ab20314471f2cd` |
| Stage 3 manifest | `e1cfb92edc33d899058fc3c32a336805a845b91638759cbfdc3ca90e008a7550` |
| Stage 4 generation tree | `4a563a364adcd01063112685b7725670587ab8899041a0139e75a694820c6a80` |
| Generated Lean project | `34702f91d66c1bd4f5a657b71a5a1377d10f2d43794d32ed93157441a02c4fd7` |
| Stage 5 candidate tree | `2f109bdbce303afba652292a5629d369a84386e1fae940cd82ae86a0f633657f` |
| Generation producer-source bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |

The complete 771-file Stage 1 per-file hash map is also an exact match. The
recorded Stage 5 invocation tree is not mounted by the launcher, so its
launcher hash cannot be independently recomputed; the mounted successful
workspace itself does match exactly.

The required producer gate passes before any Stage 4 judgment:

- `klean_export.py` is
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`.
- `klean.py` is
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
- Those hashes agree with `generator-manifest.json` and
  `source-manifest.json`.
- The source bundle contains exactly those two producers plus the source
  manifest.
- The generator image ID is consistently
  `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
  in the generator manifest, source manifest, and the bundle path recorded by
  `/audit-input.json`.

The audit sandbox exposes `/proc/self/exe` but not `/proc/<getpid>/exe`, which
caused the pinned Lean 4.22 binary initially to report that it could not locate
its application. I used the recorded 46-line compatibility shim in
`evidence/00_proc_exe_compat.c`; it redirects only `readlink` calls of the
numeric `/proc/<pid>/exe` form to `/proc/self/exe`. With it, the unmodified
pinned binaries report Lean 4.22.0, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and Lake 5.0.0. It has no access
to or transformation of Lean source, elaborated terms, or candidate files.

## Inventory reconstruction and Stage 3 classification

Trusted `tools.k_rule_inventory.inventory_verification` selected
`VERIFICATION` from `prove.sh`. Its local source closure is exactly
`VERIFICATION-SYNTAX` and `VERIFICATION`. The frozen `verification.k` hash is
`bf42852fda488e22958cfbbc44f6082ad90448259e0d3bcc43d6a120d827612a`.
The reconstruction found 27 rules and produced inventory hash
`8ec67278b8911dae25f163d88afd1b55cccd504bb96573d1b111cdc4193d5663`.

The reconstructed ordered `source_rule_id` list is byte-for-byte identical to
the Stage 3 list. There are no duplicate IDs, omitted rules, extra rules,
reordered identities, span changes, normalized-hash changes, or unclassified
rules. Full source text, span, attributes, normalized hash, and ID for every
entry are preserved in `evidence/01_inventory_reconstruction.json`.

I independently reclassified all entries:

| Frozen lines | Rules | Classification and reason |
|---|---:|---|
| 20–21, 22–23 | 2 | `DEFINITION`: exhaustive even/odd equations defining the named `collatzNext` summary. |
| 28, 29, 30–32, 33 | 4 | `DEFINITION`: empty, singleton, adjacent-step recurrence, and `owise` completion for `validCollatzTrace`. |
| 35, 36 | 2 | `DEFINITION`: integer-head and default equations for `traceFirstInt`. |
| 38, 39, 40–41, 42 | 4 | `DEFINITION`: empty, integer singleton, structural tail recurrence, and default equations for `traceLastInt`. |
| 44–45, 46–47 | 2 | `DEFINITION`: even-empty and odd-singleton equations for `maybeOdd`. |
| 50, 51, 52–54, 55–57, 58–60 | 5 | `DEFINITION`: structural base, even, odd, and non-integer-head equations for `oddWithoutLast`. |
| 64–103 | 8 | `DOMAIN_LEMMA`, individually detailed below. |

The 19 definitions define named summaries and structurally decreasing
recurrences. They do not match a `<k>` cell, heap, environment, continuation,
or any other operational configuration and do not replace source-program
execution. Their cases are disjoint or use `owise`, and the parity pairs are
exhaustive because `pyMod(N, 2)` is 0 or 1. Thus none is an
`OPERATIONAL_RULE`.

The eight simplification rules are correctly `DOMAIN_LEMMA`, not definitions
or proved-derived lemmas:

| Lines / rule ID prefix | Independent judgment |
|---|---|
| 64–65 / `rule-1bc30ace…` | Right identity of the pre-existing, left-recursive `valSeqConcat`; true by induction and needed to normalize list append. |
| 67–69 / `rule-9345c98e…` | Associativity of `valSeqConcat`; true by induction and needed for repeated appends. |
| 71–73 / `rule-bf51f8af…` | Appending a constructor-valued right operand cannot yield empty; true by the list constructors. |
| 75–77 / `rule-57fc2eb6…` | Symmetric form of the same non-emptiness fact. |
| 81–84 / `rule-89c097c3…` | Appending a singleton preserves the first observation when the old sequence is nonempty. |
| 86–88 / `rule-f6103b1a…` | The last observation of a singleton append is the appended integer. |
| 90–95 / `rule-18e026ac…` | A nonempty trace extended by `J` is valid exactly when the old trace is valid and `J` is the Collatz successor of its last element. |
| 97–103 / `rule-8b95aa8c…` | For a valid trace, extending it moves the former last element into `oddWithoutLast` exactly when that former last element is odd. |

These laws are relevant to the frozen source and postcondition: list
`.append` is modeled by `valSeqConcat`; the loop invariant tracks the first
and last trace elements, validity of adjacent Collatz steps, and the odd
elements before the terminal trace position. They are not generic,
irrelevant mathematical assertions.

No entry qualifies as `PROVED_DERIVED_LEMMA`. `prove.sh` compiles
`verification.k` with all eight simplifications already installed and only
then runs the loop and target claims. There is no earlier proof of any exact
rule against a module that omits it. Every `simplification` entry is therefore
in the allowed `DOMAIN_LEMMA` class.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
pinned lock. The returned result in
`evidence/03_preflight_rerun.json` is `PASS` with 8 obligations, zero sorries,
43 generated trust declarations, and successful `lake clean` and `lake build`.

The independently reconstructed domain-rule ID list, the obligation map's
`source_rules`, and its `obligations` are the same eight unique IDs in the same
order. Each source span, normalized source hash, inventory hash, discovery
hash, and conjunct hash matches. The exact translations are:

1. right identity;
2. associativity;
3. right-nonempty `==K` false;
4. its symmetric form;
5. `traceFirstInt` after singleton append under the exact nonempty guard;
6. `traceLastInt` after singleton append;
7. the exact guarded `validCollatzTrace` append equation; and
8. the exact guarded `oddWithoutLast` append equation.

No conjunct is `True`, `False`, a proof hole, or unrelated to its source rule.
The Lean linter calls some proof binders `h` unused in the proposition body,
but those binders are the translated K guards: a dependent function from a
proof of `guard = true` is an implication, not a vacuous dropped premise.

The generated target is the exact conjunction of those eight obligations:

- declaration:
  `Klean123GetOddCollatz.Lemmas.targetStatement`;
- statement hash:
  `6501d738080cdd0a6846e9cb37a71f6aefcf92c1836ba73d50a0ca0edf264a72`;
- definition hash:
  `d0c784cc774c98dab7ea4f5fc6f755f309d7f1c1472ecca006ebc9163c8a2f89`.

The declaration, complete parameter bindings, statement, definition, and
hashes agree across the generated source, obligation map, generator manifest,
preflight, and audit input. Because the independently classified domain set
contains eight genuine lemmas, Stage 4 correctly has status `OK`; a
`KLEAN_NO_OBLIGATIONS` result would have been invalid here.

## Stage 5 Lean proof

I copied the candidate to the fresh directory
`/tmp/audit-work/lean-audit.XONbiz`, copied the immutable generated project
contents into `Base`, then ran `lake clean` and `lake build`. Both exited 0;
the complete non-ANSI build output is in
`evidence/04_lake_build.raw.log` and ends with `Build completed
successfully.`

The trusted final gate independently repeated the copy, clean build, exact
type check, and axiom check and returned `PASS`. It found exactly one
definition for every target parameter and exactly one `Proof.final`, whose
type is the generator's fixed statement. Candidate sources outside `Base`
contain no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`; they neither
redeclare nor shadow `Klean123GetOddCollatz.Lemmas.targetStatement`.

The exact `#print axioms Proof.final` output is:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

There is no `sorryAx` and no dependency on any of the 43 project-level axioms
recorded by `trust-inventory.json`. The three reported names are Lean's
standard core trust base and are explicitly allowed by the trusted final
gate. `Classical.choice` is used to obtain decidable structural equality for
`SortK`; it does not assume a proposition about an obligation. Thus every
actual dependency is accounted for and there is no unrecorded candidate
escape.

### Operational-bridge judgment

I located each exact candidate `def` named by `target.parameters` and compared
it with its bound KORE symbol, cited source-rule IDs, frozen summary equations,
and the supplied semantics:

| Parameter group | Judgment |
|---|---|
| `_andBool_`, `«_==Int_»`, `notBool_` | Exact Boolean conjunction, integer equality, and negation. |
| `«_==K_»` | Exact structural equality on generated `SortK`; equal and distinct wrapped sequences were checked. |
| `collatzNext` | Computes the supplied `pyMod(_,2)` parity for every `Int`, exact halving for even inputs, and `3*n+1` for odd inputs. Negative and zero cases were checked, not only the positive source precondition. |
| `maybeOdd` | Returns empty for even integers and an injected integer singleton for odd integers, including negative witnesses. |
| `valSeqConcat` | Exact left-recursive implementation of the two frozen `MPY-LIST` equations. |
| `traceFirstInt` | Returns the injected integer head and 0 for every other shape, matching the specific and `owise` K rules. |
| `traceLastInt` | Structurally drops heads until the singleton; integer singleton gives its integer and all default shapes give 0. |
| `oddWithoutLast` | Structurally excludes the last position, skips even and non-integer heads, and preserves odd integer heads. |
| `validCollatzTrace` | Empty is false, integer singleton is true, integer adjacency follows `collatzNext`, and all other shapes are false. |

`evidence/06_AuditBridge.lean` checks parity boundaries `-4`, `-3`, `0`, `5`,
and `6`; even/odd `maybeOdd`; concatenation; non-integer head/tail behavior;
the valid trace `[5,16,8,4,2,1]`; invalid `[5,15]`; empty and non-integer
traces; and structural K equality. It also introduces hard-coded
`collatzNext`, always-empty `maybeOdd`, constant concatenation, identity
`oddWithoutLast`, and constant-true validity mutations and proves each differs
on a concrete witness. Lean accepts all these adversarial checks. The
candidate definitions are therefore operationally sensitive, not convenient
constants, identities, or encodings chosen merely to close the conjunction.

The proof itself establishes each fixed conjunct by structural induction and
then constructs the conjunction in the generated order. It does not prove a
duplicate theorem or weaken the target. As intended by this pipeline, this
Lean theorem discharges the eight Stage 3 domain lemmas; it does not purport
to be a separate proof of Collatz termination or replace the frozen Stage 1
program reachability theorem.

## Evidence index

- `evidence/00_preflight_without_proc_compat.log` and
  `evidence/00_proc_exe_compat.c`: sandbox toolchain diagnosis and narrow
  compatibility shim.
- `evidence/01_inventory_reconstruction.json`: full reconstructed inventory
  and exact ordered comparison.
- `evidence/02_producer_provenance.json`: producer hashes, bundle hash, and
  image-ID checks.
- `evidence/03_preflight_rerun.json`: required Stage 4 preflight result.
- `evidence/09_obligation_bijection.json`: all eight source texts paired with
  their generated conjuncts.
- `evidence/07_integrity_and_target.json`: mounted input hashes, all Stage 1
  file hashes, sidecar hashes, and target identity checks.
- `evidence/04_lake_clean.raw.log` and
  `evidence/04_lake_build.raw.log`: fresh proof clean build.
- `evidence/05_print_axioms.log`: exact axiom output.
- `evidence/08_final_gate.json`: independent exact-type, forbidden-token,
  clean-build, and axiom gate.
- `evidence/06_AuditBridge.lean` and
  `evidence/06_bridge_adversarial.log`: operational and counterfactual checks.

VERDICT: PASS
LEGITIMACY: LEGIT
