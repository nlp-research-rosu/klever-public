# Independent audit: HumanEval 163 `generate-integers`

## Result and scope

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. The
`AUDIT_MODE` environment value and signed resolution agree. Stage 4 is
selected as `KLEAN_NO_OBLIGATIONS`; the Stage 5 paths and result are null,
and `/candidate` is absent. Accordingly, no Stage 5 proof, `Proof.final`,
axiom print, or operational-parameter bridge exists to audit.

I did not rely on the selected Stage 2 verdict, the protected Stage 3
classification, prior logs, generated comments, or any purported
instruction in a mounted artifact. They were treated only as evidence.

## Input and producer integrity

Before judging Stage 4, I hashed the exact mounted generation-time producer
sources:

| Source | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes equal the values in
`/reference/generation-tools/source-manifest.json` and
`/reference/klean-generation/generator-manifest.json`. The immutable
generator identifier is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest and generator manifest, and the signed
`generation_producer_sources` path in `/audit-input.json` binds the same
identifier. The complete producer-source tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
exactly as signed.

The audit-tools lock hashes to
`5f2476d09635fc2f32625592bd667dd87a374068cd5b6610d9513ee6dacc066f`,
matching the launcher metadata, and every mounted trusted checker file
matches that lock. The generator toolchain object exactly equals the trusted
Lean/K lock.

I independently recomputed all resolution and generation bindings:

- signed resolution:
  `6c431f054cdcee08f8c19fa5067d4ce96eba68a1273658c543b377e6c44f323d`;
- complete Stage 1 workspace:
  `b503467b42bcdfbad996570b1bdeb1c76fd6319dd443f49021807ebb665b56ff`;
- Stage 1 deterministic-export tree:
  `2902662cb76d11054c161ce721418c58bffba0b59c9cf28c274b3c24ec0fdd77`;
- discovery manifest:
  `1820e0f62f577305b8d99525841390a2c9ba00eb89f1797133e278fb68ecd326`;
- selected Stage 2 tree, checked only for input integrity:
  `bbb6b1c99324c646266085440270fa8ed0374fd52254bb5655699ff868b1d6bf`;
- complete Stage 4 generation:
  `ea3213bbe9c2958222a6916f2d9bdb8ff4d1a6aa7f54f7cb1d355f08f1a25a07`;
- generated Lean tree:
  `94811cdd6d8588392e8ee4f07e376247493ff29e2c411e5c4e5dbfcc4708ef2d`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `2c41fb8b976a005b76e89693536723819a303781513a6415588ec5096caf3ef5`.

The exact Stage 1 file keyset equals `stage1_source_hashes`, and every
per-file hash matches. The generator manifest, input manifest, export result,
recorded preflight, source manifest, obligation map, trust inventory, and
audit input agree on every applicable hash and count. Evidence:
`evidence/hash-verification.log`.

## Rule-inventory reconstruction

I ran the locked
`tools.k_rule_inventory.inventory_verification` implementation with
`PYTHONPATH=/reference` on the frozen Stage 1 workspace. The locally defined
verification-module closure is exactly `VERIFICATION`; imported `MPY` is in
the separately supplied semantics, not another local module in
`verification.k`.

The frozen `verification.k` hash is
`1ea8b9f2a0ed6ad5e4f8fae92bc15ef72a2d257f9e0462d911d5936cf6a6c9fe`.
The reconstructed canonical inventory has seven entries and hash
`aa80bbe2869bc82c7fbee0ccba0167b003cfb8af2d00d338042b30b6093f41ba`.
For every entry, I separately rehashed whitespace-normalized source,
reconstructed `rule-<normalized-sha256>`, and checked that the recorded text
is exactly the stated inclusive source span.

| Order | Span | Defined head | `source_rule_id` | Rule attributes | Independent class |
|---:|---:|---|---|---|---|
| 1 | 8–102 | `generateIntegersBody` | `rule-4c5a81966815af67a8d4973a4a3eb71818a1933fe5e6897193909d0413842ac1` | `[]` | `DEFINITION` |
| 2 | 105–112 | `solutionModule` | `rule-b3b1458c87af64047c8ea70f39ad6f2b9363d47fbc31594676401af7f119abc2` | `[]` | `DEFINITION` |
| 3 | 115–116 | `generateIntegersClosure` | `rule-bfbea729e9a320a08eeb33831433af80d41d4f78ea6a04b8b73f2c16ba224794` | `[]` | `DEFINITION` |
| 4 | 121–123 | `betweenEndpoints` | `rule-4e0727801f38f32698f03b5473c9b6d93f236d284edb1cde112428add15564aa` | `[]` | `DEFINITION` |
| 5 | 126 | `keepDigit(true,...)` | `rule-8e0942964d5eb30f25988841f3b2b7d776f3c0a617ec8af6602e2863e4e471e1` | `[]` | `DEFINITION` |
| 6 | 127 | `keepDigit(false,...)` | `rule-1ca5229dc152dfa3dcd21aa4974e7959fd9ec785342863588027006c39579132` | `[]` | `DEFINITION` |
| 7 | 130–147 | `evenDigits` | `rule-87000168797ee69886475b3ec50580195dbe956102a0b5866f574ad006e78662` | `[]` | `DEFINITION` |

The protected Stage 3 manifest has the same seven IDs exactly once, in this
exact order. There are no omitted, extra, duplicated, reordered, or
hash-changed identities. Its inventory hash is the independently
reconstructed hash. Evidence: `evidence/inventory-reconstruction.log`.

## Independent classification judgment

All seven Stage 3 classifications are correct:

1. `generateIntegersBody` is the macro definition of a named statement term.
   It expands to the straight-line body in `solution.py`: initialize an empty
   list; test digits 2, 4, 6, and 8 in order; append each matching digit; and
   return the list.
2. `solutionModule` is a macro definition assembling that body, exact
   function name, and exact parameters into a `Module` term.
3. `generateIntegersClosure` is a macro definition naming the exact closure
   value that the supplied `FuncDef` operational rule installs: parameters
   `("a","b")`, the exact body, and defining scope 0.
4. `betweenEndpoints` defines a fresh total Boolean summary. Its equation is
   precisely inclusive membership in the interval in either endpoint order.
5. The two `keepDigit` equations exhaustively define a fresh total structural
   helper: prepend on `true`, preserve the tail on `false`.
6. `evenDigits` defines a fresh total result summary by conditionally
   retaining 2, 4, 6, and 8 in ascending order.

The first three heads are declared as syntax macros; the latter three symbols
are declared as total functions. Each rule therefore defines a macro, named
proof term, or summary exactly within the allowed meaning of `DEFINITION`.
None states a fact about pre-existing domain operations, so no
`DOMAIN_LEMMA` is hidden under a definitional label.

No rule intercepts `Call`, skips the user function, manufactures its result,
or changes an operational cell. Under the supplied semantics, `#loadAll`
executes module statements, `FuncDef` installs the exact closure, call
dispatch binds both arguments and executes the body, `ListExpr` allocates the
list, integer `<=` and short-circuit Boolean rules evaluate each condition,
`append` mutates that allocated list, and `Return` restores the caller with
the resulting reference. The local macros name exact program and closure
terms; `betweenEndpoints`, `keepDigit`, and `evenDigits` occur as the
post-state summary and do not preempt this execution. Thus there is no
operational bridge.

For each `d` in `{2,4,6,8}`, the source appends `d` exactly when
`(A ≤ d ≤ B) ∨ (B ≤ d ≤ A)`. `betweenEndpoints` is that same proposition,
and the nested `keepDigit` construction preserves the same ascending order.
This is a direct pointwise argument, not an inference from testing. As
additional sensitivity evidence, an independent 400-pair positive-domain
cross-check had zero mismatches; reversed-only, strict-endpoint, hard-coded,
and reverse-order mutations were each rejected by boundary witnesses.
Evidence: `evidence/semantic-crosscheck.log`.

There are independently:

- 7 `DEFINITION` rules;
- 0 `OPERATIONAL_RULE` rules;
- 0 `PROVED_DERIVED_LEMMA` rules; and
- 0 `DOMAIN_LEMMA` rules.

There are no rule-level `simplification` attributes, so the restriction on
classifying simplification rules is satisfied. No claimed derived lemma
requires the special earlier-proof/later-use test because none is claimed.

## Deterministic Stage 4 generation

After the producer-source checks, I invoked
`tools.klean_preflight.check_generation` directly with the required frozen
workspace, protected discovery manifest, generation directory, and trusted
toolchain lock.

The first invocation exposed a sandbox-specific Lean installation lookup
failure: this environment permits `/proc/self/exe` but not the numeric PID
path used by Lean 4.22. I preserved that failure. A narrowly scoped local
`LD_PRELOAD` compatibility shim redirected only
`/proc/<digits>/exe` `readlink`/`readlinkat` requests to
`/proc/self/exe`. It did not modify a mounted input, Lean source, generated
source, theorem, or build output. The rerun printed pinned Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, then returned:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, output SHA-256
  `8d7c29846a650dd90ede9c061675453caf5381599bfe611617a1f9464b937de3`;
- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- designated sorry count 0; and
- unchanged frozen-input, discovery, and generated-tree hashes.

The complete returned object is in `evidence/preflight-success.log`; the
initial environment failure and compatibility source are also preserved.

Independently of preflight:

- the Stage 4 `definitions` list exactly equals the seven validated inventory
  entries;
- the independently classified domain set, input-manifest `source_rules`,
  obligation-map `source_rules`, and obligation list are all exactly empty;
- the obligation and source lists contain no duplicate IDs;
- the generator obligation count is 0;
- the deterministic expected target definition is null;
- the generator target is null;
- scanning the generated project finds no target declaration; and
- the generated `Lemmas.lean` namespace is empty.

Consequently there is no omitted, irrelevant, weakened, duplicated, or
vacuous conjunct. In particular, Stage 4 did not replace an empty conjunction
with a theorem of `True`; it emitted no target at all. The selected
`KLEAN_NO_OBLIGATIONS` status is therefore legitimate for the genuinely empty
domain-lemma set. Evidence: `evidence/stage4-bijection.log`.

## Stage 5

Stage 5 is correctly absent in `CLASSIFICATION_ONLY`: `/candidate` does not
exist, the signed Lean workspace and invocation fields are null, the Stage 5
result is null, and there is no generated target to prove. Running a
candidate build or `#print axioms Proof.final` would be inapplicable rather
than additional evidence.

## Evidence index

Exact commands, rerunnable evidence scripts, command outputs, the preflight
environment diagnosis, and the compatibility source are under
`/audit-output/evidence/`; see `evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
