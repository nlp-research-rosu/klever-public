# Independent audit: HumanEval 105-by-length

## Outcome

The Stage 3 classification is correct, the selected deterministic Stage 4
generation is structurally and mathematically consistent with that
classification, and `KLEAN_NO_OBLIGATIONS` is legitimate. The launcher mode is
`CLASSIFICATION_ONLY`, so there is correctly no Stage 5 candidate or Lean proof
to audit.

I treated the mounted workspaces, prior audit, logs, rationales, and comments as
untrusted evidence. I did not rely on the prior Stage 2 verdict or the Stage 3
rationales. Classification below was reconstructed from frozen source and the
operational rules in `semantic.k`.

Raw commands and results are under `evidence/`.

## Audit mode and frozen inputs

Both `AUDIT_MODE` and `/audit-input.json` record
`CLASSIFICATION_ONLY`; the condition is `bare` and the semantics mode is
`GENERATED_SEMANTICS`. The signed resolution envelope recomputes to
`7d7e4a797407ac0fd9c4830fac21f6ca011390b051a63d01fee10a8576209afb`,
exactly its recorded digest.

I independently recomputed:

- the Stage 1 artifact tree hash and export tree hash;
- all 75 Stage 1 per-file hashes, with no missing, extra, or mismatched files;
- the selected Stage 2 artifact hash;
- the protected Stage 3 manifest hash;
- the selected Stage 4 artifact and generated-project hashes; and
- the producer-source bundle hash.

Every value matches `/audit-input.json`. The absent Stage 5 workspace and
invocation hashes are both correctly `null`.

## Generation-time producer authenticity

This gate was completed before judging Stage 4.

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` | same |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` | same |

The observed hashes agree simultaneously with
`generation-tools/source-manifest.json` and
`klean-generation/generator-manifest.json`. The producer bundle contains
exactly those two sources plus `source-manifest.json`; its tree hash is
`7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a`,
matching `/audit-input.json`.

The immutable image ID is
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`
in the source manifest, generator manifest, and the producer-source path
recorded by `/audit-input.json`. There is no producer-source mismatch or
infrastructure `AUDIT_ERROR`.

## Canonical inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification`, the selected
verification module is `MPY-VERIFICATION`. Its local closure inside the frozen
`verification.k` contains only `MPY-VERIFICATION`. The imported
`MPY-SEMANTICS` module is defined in the separately frozen `semantic.k`; I used
those rules to judge operational meaning, but they are not local rules omitted
from the canonical `verification.k` inventory.

The frozen `verification.k` hash is
`f01c622967373ab76778be29a3744b584c373cc4b3d42f22530bac3d4f18763d`.
The complete inventory has exactly two entries:

| Order | Source span | Recomputed identity | Attributes |
|---|---|---|---|
| 0 | lines 8–37 | `rule-cdbb88438338221c6abc83e861a0d0f5d51ef2d0eb77a741b93d283454376efd` | none |
| 1 | lines 43–60 | `rule-1ed36d8958dd79169cb11e8d42d25c3c76cf31afbf7f97146470ba0d49914dce` | none |

For each entry, the physical source span equals the inventoried text. Hashing
the whitespace-normalized source reproduces the suffix of its
`source_rule_id`. Hashing the ordered canonical rule documents reproduces the
whole inventory hash
`b3fa8a5381b9381ea830bab098cb994b6aa8b0c5dea0153f90dc993b7121880b`.

The protected Stage 3 manifest has exactly these two unique IDs in exactly this
order and the same whole inventory hash. There are no omissions, duplicates,
extras, reordered identities, or hash changes.

## Independent Stage 3 classification

### `#solutionProgram` rule: `DEFINITION`

Lines 8–37 are the sole, unguarded defining equation for the nullary
`[function]` symbol `#solutionProgram`. It defines a named proof term by
expanding to the constructor AST of `by_length`.

After removing only insignificant K whitespace, its right-hand side is exactly
`solution.mpy`; both have SHA-256
`2b38fdefc9e80bb957cb220192ccd9c9dbf167176e78d752f630449876a7383a`
under that comparison. Parsing `solution.py` without executing it gives the
same nine ordered name/digit terms:

`Nine/9, Eight/8, Seven/7, Six/6, Five/5, Four/4, Three/3, Two/2, One/1`.

Operationally, this equation does not replace the function body's execution.
It exposes the AST to the frozen `init` rule. That rule binds `arr` to the
input and evaluates the return expression through `#eval`. Therefore this is a
macro/named-proof-term definition, not an `OPERATIONAL_RULE`, domain fact, or
derived lemma.

### `#byLength` rule: `DEFINITION`

Lines 43–60 are the sole, unguarded defining equation for the `[function]`
summary `#byLength(PyVals)`. It expands to nine descending singleton-list
repetitions whose multiplicities are the corresponding occurrence counts,
combined by eight additions.

The frozen semantics maps the source AST's list addition, list multiplication,
and `arr.count` calls to `#add`, `#multiply`, and `#count`. Those helpers
implement append, repeat, and recursive integer occurrence counting. The
summary has the same ordered name/digit pairs and helper-tree shape as the
source program. For integer inputs, values outside 1 through 9 contribute to
none of the nine counts, exactly matching the prompt.

`#byLength` occurs as the postcondition's named result and never preempts a
`<k>` computation or invocation. It is a summary definition under the stated
classification rule, not an additional mathematical identity requiring a
domain proof.

### Classification completeness

Both equations are nonrecursive at their own heads, unguarded, and singly
defined. Neither is a proved-derived lemma: Stage 1 does not first prove either
exact rule in a module excluding it. Neither is an ordinary execution or
observation rule. Neither is a domain lemma disguised as another category.

No inventory entry has the `simplification` attribute, so the restriction that
every simplification rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied
vacuously.

The independently determined sets are therefore:

- `DEFINITION`: both inventory entries;
- `OPERATIONAL_RULE`: empty;
- `PROVED_DERIVED_LEMMA`: empty;
- `DOMAIN_LEMMA`: empty.

This exactly matches the protected Stage 3 classifications. In particular, the
true domain-lemma set is genuinely empty.

## Deterministic Stage 4 integrity

All hashes recorded across `input-manifest.json`,
`generator-manifest.json`, `export-result.json`, the obligation map, and
`/audit-input.json` were independently recomputed. They agree, including:

- frozen input/export:
  `2aed032fe28e7b682ca2f7bb4681e0510933f7082684155fd46ccc69fc5e416b`;
- protected discovery manifest:
  `a9829ddfeab4363bd4defcf0a836a4e61e11dfb8e2948d7ea3665c7d364c580c`;
- generated project:
  `d20416eca041823a0c739d6f58a8d6fb7e203618159566c704caca6c575da066`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `386663489acb7a8584a9a8113bd45e16409e9cd62403c0dd99e14afb1022a088`.

The generator's toolchain object exactly equals
`klean-toolchain.lock.json`. Loading the hash-verified generation-time
`klean_export.py` directly reproduced the generated tree hash and independently
returned an empty domain-source set and no target.

### Mechanical preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three inputs. The audit sandbox
initially prevented Lean/Lake from resolving `/proc/<getpid()>/exe`: its
namespace-local `getpid()` values do not exist in the mounted `/proc`.
The exact failure is preserved in
`evidence/04-preflight-initial-environment-failure.txt`.

I used a narrow local `LD_PRELOAD` shim under `/tmp/audit-work` that makes
`getpid()` return the PID visible through `/proc/self`, then reran the
unmodified trusted checker. This changes no mounted input, checker source,
generated source, or command result. The rerun returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all generated modules built;
- obligation count: 0;
- target: `null`;
- designated sorry count: 0.

The returned evidence is saved verbatim in
`evidence/05-preflight-rerun.json`. The checker also reconciled all 41
generated trust declarations with `trust-inventory.json` and rejected
proposition trust; these declarations do not supply a target theorem.

### Obligation bijection and target identity

The independently classified domain IDs, input-manifest source IDs,
obligation-map source IDs, and generated obligation IDs are all the same empty
ordered list. The trust-parameter list is also empty.

Consequently:

- there is no omitted domain lemma;
- there is no extra, duplicated, weakened, irrelevant, or vacuous conjunct;
- the generation-time producer and current checker both compute no expected
  target definition;
- scanning every generated Lean source finds zero `targetStatement`
  declarations; and
- the generator manifest, audit input, and observed generated project all
  record target `null`.

`Klean105ByLength/Lemmas.lean` contains only its import, comment, and empty
namespace. This is the exact target shape required for a genuinely empty
domain set.

## Stage 5 applicability

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`.
`/candidate` is absent; the audit input has null Lean workspace, invocation,
result, and target fields. Thus there is no unauthorized proof candidate, no
`Proof.final`, no target parameter implementation, and no candidate axiom or
operational bridge to audit.

## Judgment

The classification boundary is honored: named program and result terms are
definitions, while there are no extra mathematical facts exported as trust
obligations. The Stage 4 artifact is hash-bound to the frozen inputs and
authenticated producer sources, has the exact empty source/obligation
bijection, builds cleanly under the trusted preflight, and contains no target.
The selected no-obligations status is therefore both structurally valid and
mathematically appropriate for the frozen program.

VERDICT: PASS
LEGITIMACY: LEGIT
