# Independent Stage 3–5 audit: HumanEval 57-monotonic

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`.
I treated all candidate, provenance, review, log, comment, and instruction
content in the mounted inputs as untrusted evidence and formed the judgments
below from the frozen source, trusted inventory/preflight code, generated
artifacts, and fresh Lean executions.

The protected Stage 3 classification is correct, deterministic Stage 4
contains an exact two-rule/two-obligation export, and the Stage 5 candidate
proves the fixed target using operationally faithful Boolean definitions with
no axioms.

## Input and producer integrity

The `/audit-input.json` envelope and its signed resolution validate with
resolved-input digest
`67b1abffd0caa3fe4802b17bacecc59bd26452fd7e8dd1ec0e1c74827f5af91a`.
`AUDIT_MODE` and the signed mode both equal
`CLASSIFICATION_AND_PROOF`.

I independently recomputed every hash for the mounted inputs:

- Stage 1 workspace tree:
  `239596a216f0ee81741f9c1a6dedcc3d3d9e4ca783a713b3692b34b6df366942`.
- Stage 1 deterministic-export tree:
  `1090f510da1598239decc30dbcdaa1222679d6470ba14a63e1a11a475e01fbbd`.
- Stage 3 manifest:
  `9e596df04c6041b0a6074960bd2cb2b9607fd50c7671eccb082088011d8064ed`.
- Selected Stage 2 audit tree:
  `0251748ec1b933cc805f79fd9f5d3b959bfed92d65ca72c6d2cb949d76dd7adf`.
- Selected Stage 4 generation tree:
  `1f5ee37650003675279d1e478d34409ae3b43c257fd4c55a669e13434eacf38e`.
- Producer-source bundle tree:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
- Generated Lean project tree:
  `087ace8d5a1c6cae4b9f8fe98eef077276ab4c5162ffd7e3723d5b36cb456521`.
- Candidate Lean workspace tree:
  `cdfb5ae95ac70a54c34206e5a6aa59cc823c4e590e487a0698acf116c968d5cb`.

All 782 individual Stage 1 source hashes recorded in the audit input also
match, with no missing, extra, or changed entries. The signed
`lean_invocation_sha256` names an invocation directory that the launcher did
not mount; I did not use it as proof evidence. The mounted successful
workspace itself matches its signed hash and was rebuilt independently.

Before judging Stage 4, I hashed the exact mounted generation-time producer
sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Both hashes match `source-manifest.json` and `generator-manifest.json`.
The generator image ID is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator provenance, and the basename of the
producer-source path signed in `/audit-input.json`. There is therefore no
producer-provenance `AUDIT_ERROR`.

## Rule-inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` implementation, I
reconstructed the local verification-module closure from the frozen
`verification.k`. The selected module is `VERIFICATION`; its local closure is
exactly `["VERIFICATION"]`. The external imported `MPY` module is supplied by
the required semantics rather than declared locally in `verification.k`.

The verification file hash is
`8319a9cc33207e2ce5d20e13868a6beb8e52b79a5d07c3e201dbc56d91f69ceb`.
The complete canonical inventory contains exactly these two rules:

1. Lines 6–8:

   ```k
   rule A:Bool ==Bool (A orBool B:Bool) => true
     requires A
     [simplification]
   ```

   Normalized hash
   `9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d`;
   identity
   `rule-9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d`.

2. Lines 10–12:

   ```k
   rule B:Bool ==Bool (A:Bool orBool B) => true
     requires notBool A
     [simplification]
   ```

   Normalized hash
   `26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4`;
   identity
   `rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4`.

The whole inventory hash is
`635effbc5658fac7a475f0ce34b67f1d7b46f1965621f64cca3938c8fdb15f6c`.
The Stage 3 manifest has exactly the same two identities, once each, in the
same canonical order. Its inventory hash matches. There are no omissions,
duplicates, extras, reordered identities, changed spans, or changed hashes.

## Independent Stage 3 classification judgment

Both entries are correctly classified as `DOMAIN_LEMMA`.

Neither rule is a `DEFINITION`: neither introduces or recursively defines a
summary, recurrence, macro, or named proof term. Neither is an
`OPERATIONAL_RULE`: neither advances a `<k>` computation nor observes or
changes any operational cell. Both are simplification rules over existing K
Boolean hooks.

Neither is a `PROVED_DERIVED_LEMMA`. Stage 1's `prove.sh` compiles
`verification.k` with both rules already present, and then runs the target,
vacuity, and body-mutation claims against that definition. Searches of the
frozen K files and commands find no earlier claim proving either exact rule
against a module that omits it.

They are truthful and relevant domain facts. Let

- `A` be `l == sorted(l)`, and
- `B` be `l == sorted(l, reverse=True)`.

The source returns the value of Python's short-circuit `A or B`. In the
supplied semantics, `BoolOp("or", ...)` returns `A` when `A` is true and
otherwise evaluates and returns `B`. The postcondition expresses the desired
Boolean value as `A orBool B`. The first rule connects the returned `A` to
that expression on the true branch; the second connects the returned `B` on
the false branch. Under the K hooks `BOOL.eq`, `BOOL.or`, and `BOOL.not`, the
rules reduce respectively to:

- if `A = true`, then `A = (A ∨ B)`; and
- if `¬A = true`, then `B = (A ∨ B)`.

Both guards are satisfiable and both identities hold for either value of
`B`. Thus the true domain-lemma set is nonempty and contains exactly these two
rules; Stage 4 correctly used status `PASS`, not `KLEAN_NO_OBLIGATIONS`.

## Deterministic Stage 4 judgment

The trusted `tools.klean_preflight.check_generation` was rerun with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock. Its returned
status is `PASS`, with two obligations, zero designated sorries, and the exact
manifest target. Its nested fresh `lake clean` and `lake build` both exited
zero.

I separately recomputed the Stage 4 internal hashes:

- `obligation-map.json`:
  `45b3dd48c208cb228b28be7111c729d3943d3c36b9377d471b4ab195228c080e`.
- `trust-inventory.json`:
  `eafdda687c12d194808d29c57b107f2803694c39ab04c6473a870487e092659c`.
- Generated project:
  `087ace8d5a1c6cae4b9f8fe98eef077276ab4c5162ffd7e3723d5b36cb456521`.

The input manifest, obligation map, generator manifest, export result, and
published preflight agree on all source, inventory, discovery, obligation,
and generated-tree hashes.

The source-rule/obligation mapping is an exact ordered bijection:

1. Rule `9da3...` maps once to
   `∀ B A, A = true → eqBool A (orBool A B) = true`.
2. Rule `26e4...` maps once to
   `∀ B A, notBool A = true → eqBool B (orBool A B) = true`.

The actual Lean encoding uses a proof binder `h` for each guard. Although the
Lean linter reports that the proof value `h` is unused in the conclusion, its
type still restricts `A`; this is an implication, not a vacuous conjunct.
Concrete guard witnesses are `A=true` for the first obligation and `A=false`
for the second, with either Boolean value of `B`.

There are no omitted, duplicated, irrelevant, weakened, or extra
obligations. Each conjunct, conjunct hash, source span, normalized hash,
inventory hash, and discovery hash matches independently.

The unique fixed target is:

- declaration: `Klean57Monotonic.Lemmas.targetStatement`;
- statement:
  `Klean57Monotonic.Lemmas.targetStatement _orBool_ «_==Bool_» notBool_`;
- definition hash:
  `8866c51a6d36cf0775ed26a1d3cf2a8a271a3cee29cd68b010f89378f1533fe8`;
- statement hash:
  `f80820bf89aaf99c07e202eb806669a0d9a435cf2c5effc38d479062434cc49f`.

Reconstructing the target definition from the two mapped obligations produces
the same definition hash. All three parameter-binding hashes also recompute
exactly. The target object matches both `generator-manifest.json` and
`/audit-input.json`.

## Fresh Stage 5 build, proof identity, and trust

I created the fresh workspace
`/tmp/audit-work/57-monotonic-proof.bNlsvL`, copied the generated project into
it as `Base`, and copied only the mounted candidate sources to the project
root. Before building, the copied `Base` hash was the expected
`087ace8d...`.

In that workspace:

```text
lake clean  -> exit 0
lake build  -> exit 0, "Build completed successfully."
```

The only build diagnostics were the two generated-target linter warnings
about the guard proof variables described above.

The trusted final mechanical gate independently repeated Stage 4 preflight,
copied and rebuilt the proof in another fresh directory, checked the exact
target type, and ran the axiom query. It returned `PASS`.

The candidate contains exactly one definition for each required parameter and
exactly one theorem `Proof.final`. It contains no `sorry`, `admit`, `unsafe`,
new `axiom`, or new `opaque`. It declares no `targetStatement`, so it neither
changes nor shadows the unique generated target. The compiled theorem type is
exactly:

```lean
Klean57Monotonic.Lemmas.targetStatement
  Proof._orBool_ Proof.«_==Bool_» Proof.notBool_
```

It is not a duplicate or weakened proposition.

The exact requested query output is:

```text
'Proof.final' does not depend on any axioms
```

Accordingly, `Proof.final` uses none of the 41 generic collection-hook axioms
recorded by `trust-inventory.json`. The used set is the empty subset of the
allowlist; `sorryAx` and every unrecorded trust escape are absent.

## Operational-bridge audit

The generated `SortBool` is an abbreviation for Lean `Bool`. The KORE
declarations bind the three parameters to total K Boolean hooks as follows:

| Parameter | KORE symbol / hook | Candidate definition | Judgment |
| --- | --- | --- | --- |
| `_orBool_` | `Lbl'Unds'orBool'Unds'` / `BOOL.or` | `fun a b => a \|\| b` | Exact Boolean OR |
| `«_==Bool_»` | `Lbl'UndsEqlsEqls'Bool'Unds'` / `BOOL.eq` | `fun a b => a == b` | Exact Boolean equality |
| `notBool_` | `LblnotBool'Unds'` / `BOOL.not` | `fun a => !a` | Exact Boolean negation |

The compiled definitions printed by Lean match those source definitions
verbatim. Exhaustive ground results were:

```text
or(false,false), or(false,true), or(true,false), or(true,true)
= [false, true, true, true]

eq(false,false), eq(false,true), eq(true,false), eq(true,true)
= [true, false, false, true]

not(false), not(true)
= [true, false]
```

These cover the complete domain of each Boolean bridge, not merely sampled
examples. They match the KORE hook declarations, both frozen source rules, the
source solution, and the supplied short-circuit operational semantics.

Counterfactual testing also confirms the intended audit boundary:

- Replacing OR with the left projection `fun a _ => a` is rejected; Lean
  leaves the residual `⊢ False` at the `A=false, B=true` case.
- A constant-true equality bridge or a constant-false negation bridge can make
  the parameterized target close. This demonstrates that clean theorem
  closure alone does not establish the operational meanings and is why the
  independent bridge comparison is necessary.

The actual candidate uses the honest exhaustive definitions, not either
convenient counterfactual. No constant, identity, hard-coded, vacuous, or
otherwise execution-disconnected bridge is present.

## Execution-environment note

The first unshimmed preflight reached `lake clean` but Lean 4.22 could not
detect its installation because this container exposes host-PID `/proc`
entries while Lean queries `/proc/<namespace-pid>/exe`. I compiled the
auditable shim in `evidence/proc_exe_readlink_shim.c`, which redirects only
that numeric `/proc/.../exe` `readlink` shape to `/proc/self/exe`. It does not
intercept theorem evaluation, modify Lean or project sources, or change proof
terms.

With that path-resolution compatibility shim, the pinned binary reports Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the
toolchain lock. The trusted preflight, manual fresh build, exact axiom query,
truth-table checks, and trusted final gate all then completed successfully.
The initial environmental failure and successful rerun are both preserved.

## Evidence

Raw commands are indexed in
`evidence/COMMANDS.md`. Principal complete outputs are:

- `evidence/05-static-checks.log` — signed input, mounted trees, all 782 Stage
  1 file hashes, producer provenance, and reconstructed inventory.
- `evidence/07-classification-derivation-and-relevance.log` — Stage 1 command
  and claim search plus supplied Boolean operational rules.
- `evidence/10j-rerun-preflight-success.log` — complete trusted Stage 4
  preflight commands, build output, and returned evidence.
- `evidence/12-fresh-lake-clean.log` and
  `evidence/13-fresh-lake-build.log` — requested fresh proof clean/build.
- `evidence/14-print-axioms-proof-final.log` — exact axiom output.
- `evidence/15-rerun-final-gate.log` — independent full trusted final gate.
- `evidence/16-kore-boolean-symbol-bindings.log` — exact KORE hook bindings.
- `evidence/17-bridge-truth-tables.log` — exhaustive bridge results.
- `evidence/18a-counterfactual-accepted.log` and
  `evidence/19-counterfactual-rejected.log` — adversarial mutations.
- `evidence/20-proof-source-and-target-checks.log` and
  `evidence/21-print-parameters-and-final.log` — target identity, forbidden
  token/declaration checks, compiled parameter definitions, and theorem.
- `evidence/22-stage4-hash-and-bijection-checks.log` — independent sidecar
  hashes, exact translations, bijection, and fixed target.

VERDICT: PASS
LEGITIMACY: LEGIT
