# Independent Stage 3–5 audit: `92-any-int`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition
`semantics`, and semantics mode `SUPPLIED_SEMANTICS`. The environment variable
agrees. There is no `/candidate`, and the Stage 5 paths, hashes, result, and
target in `/audit-input.json` are null. I therefore audited Stage 3
classification and deterministic Stage 4 generation; Stage 5 proof checking is
correctly inapplicable.

The protected classification is correct. The genuine `DOMAIN_LEMMA` set is
empty, so Stage 4's `KLEAN_NO_OBLIGATIONS` status, empty obligation map, absent
generated target, and absent Stage 5 candidate are legitimate.

## Input integrity and producer-source gate

I treated every mounted candidate/provenance statement as untrusted evidence
and recomputed the bindings with the trusted hash and contract code.

The signed resolution digest recomputes to
`d378b0acf52a08b3bfdc875164059d48749e0825d143d04a188c555a8731a7fd`.
Every recorded resolution hash matches its mounted input:

- Stage 1 pipeline tree:
  `815934451a46397aa88e314c37b993a13716e32b540a9219476fe6121589ba15`
- Stage 1 deterministic-export tree:
  `dac9331fd382feb0e6f4199afc55b97192dfe8ba80936d3789406224dc473506`
- Stage 2 audit tree:
  `b606b42274aa0d4f512feb482e3dd1ae307e7200182d17a8aaad947663c3ef3a`
- Stage 3 manifest:
  `c45bd4645a5be9ee9b6c9b83b552b9273b8fb052831e48ad651223c3ab61debc`
- Stage 4 generation tree:
  `d9926ee093dd5d97351c97320eb700cc0aa2f193533a55dc93440fb1b611c718`
- Generated project tree:
  `da50a94b3a3a119684d1aba8d07a826f41a3fb84c20538de48ebff15ddede290`
- Generation-producer bundle:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`

All 35 individually recorded Stage 1 source hashes also match.

The mandatory producer-source gate passed:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Those hashes agree independently with
`generation-tools/source-manifest.json` and `generator-manifest.json`. The
immutable generator image ID in both manifests is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
it also agrees with the content-addressed producer path recorded in
`/audit-input.json`. The producer-bundle tree hash binds that source manifest
and both producer files. The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

Raw evidence: `evidence/00-integrity-and-producer-gate.log`.

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof` workspace. `prove.sh` selects
`ANY-INT-VERIFICATION`; its local closure inside `verification.k` is exactly
that one module. Imported `MPY` is supplied from the required semantics files,
not another local module in `verification.k`.

The frozen `verification.k` SHA-256 is
`bf222a6d72916e7963da8511a0318933ba3dd66e36f6566290679031132f9eba`.
The reconstructed whole-inventory hash is
`92116bfe9b8801cd04e25e56823e9371e4bac9c4c08d05bc44852ac69f5d27ab`.

The canonical inventory, in source order, is:

| Span | Normalized hash / `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| 7–25 | `2448470f8e791bc970ea500cb0eab8f2f171b687e742dc9dd620c3fe599983ae` / `rule-2448470f8e791bc970ea500cb0eab8f2f171b687e742dc9dd620c3fe599983ae` | none | `DEFINITION` |
| 28–32 | `20a4c6b1a1a6ebf18f4619214bf9a06e19c1ded1a4237df4613d473cbbd128eb` / `rule-20a4c6b1a1a6ebf18f4619214bf9a06e19c1ded1a4237df4613d473cbbd128eb` | none | `OPERATIONAL_RULE` |
| 35–38 | `da3bd6ef60a4c93d6ad5fcaf71497b30730636aeefceca70e5216a0ee566f547` / `rule-da3bd6ef60a4c93d6ad5fcaf71497b30730636aeefceca70e5216a0ee566f547` | none | `DEFINITION` |

For each rule, I independently sliced the reported source lines, normalized
whitespace, recomputed the normalized SHA-256, and rebuilt
`source_rule_id = "rule-" + hash`. Every text slice, line span, normalized hash,
and ID matches. The canonical and Stage 3 ID lists are exactly equal in order,
not merely equal as sets. Both lists contain three unique IDs. Thus there are
no omissions, duplicates, extras, reordered identities, changed hashes, or
unaccounted rules.

Raw evidence: `evidence/01-rule-inventory-and-manifest-bijection.log`.

## Independent classification judgment

### `anyIntBody`, lines 7–25 — `DEFINITION`

The immediately preceding syntax declares the fresh named proof term
`anyIntBody : Stmts` with `[function, total]`. Its sole unconditional equation
expands that name to the translated `Return(BoolOp(...)) .Stmts` function body.
The parameters, three `isinstance(_, int)` checks, and three addition/equality
disjuncts exactly match the frozen `solution.py` and `solution.mpy`.

This rule names and expands the source body. It does not state an extra fact
about existing mathematical operations and does not replace execution with a
result oracle. It satisfies the requested definition/macro/named-proof-term
criterion.

### `#anyInt`, lines 28–32 — `OPERATIONAL_RULE`

This is a `<k>`-cell transition from the problem-local invocation form to
`#applyK(toCall(closureVal(...)), (X,Y,Z,.Vals))`. Under the supplied
semantics, closure dispatch creates a call frame, binds `"x"`, `"y"`, and
`"z"` to those values, executes `anyIntBody`, and returns through the ordinary
`Return`/`#pop` rules. Name lookup, left-to-right call argument evaluation,
`isinstance`, short-circuit `BoolOp`, integer addition, and integer equality
all continue through the frozen operational semantics.

The rule does not jump to `sumCondition` or a convenient constant. It is the
ordinary operational entry rule for the exact source body and parameter order,
not a domain fact or an unproved derived lemma.

### `sumCondition`, lines 35–38 — `DEFINITION`

The immediately preceding syntax declares the fresh named summary
`sumCondition : Int × Int × Int → Bool` with `[function, total]`. The equation
defines it as exactly the three source-level sum equalities joined by
disjunction. The main claim uses this named summary as its postcondition.

It is a direct named summary definition, not an independent arithmetic theorem.
Changing or deleting a disjunct would change the defined postcondition rather
than prove a hidden fact about the source program.

### Partition and relevance

The independent partition is therefore two `DEFINITION` rules, one
`OPERATIONAL_RULE`, no `PROVED_DERIVED_LEMMA`, and no `DOMAIN_LEMMA`. No rule
claims the special two-stage derivation required for
`PROVED_DERIVED_LEMMA`. All three rule inventories have empty rule-attribute
lists, so there is no `simplification` rule to police.

All three entries are relevant: `#anyInt` is the claim's source configuration,
`anyIntBody` is the body it operationally executes, and `sumCondition` is the
main claim's destination value. There is no irrelevant alleged domain lemma.
The conclusion is against the frozen supplied K semantics; no unstated
mathematical shortcut is being treated as part of those semantics.

The exact frozen source and relevant name lookup, call, binding, return,
short-circuit, `isinstance`, integer-addition, and equality rules are preserved
in `evidence/02-operational-semantics-excerpts.log`.

## Deterministic Stage 4 audit

After the producer gate and classification audit, I invoked exactly
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and:

- frozen input `/reference/k-proof`
- discovery manifest `/reference/lemma-discovery.json`
- generation `/reference/klean-generation`
- lock `/reference/klean-toolchain.lock.json`

The default launcher initially failed before compilation because this audit
sandbox hides `/proc/<pid>/exe`, while Lean 4.22 asks for its own executable
using that path. `/proc/self/exe` is available. I documented and compiled a
narrow preload shim that redirects only a process's exact own-PID `readlink`
request to the equivalent `/proc/self/exe`; every other `readlink` passes
through unchanged. With `LEAN_SYSROOT` and `LAKE_HOME` fixed to the pinned
4.22.0 toolchain, Lean reported commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and an isolated `lake clean` /
`lake build` succeeded. This workaround affects executable-path discovery
only; it does not alter Lean sources, elaboration, definitions, axioms, or
generated inputs.

The required preflight rerun then returned:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- designated-sorry count `0`
- trust declaration count `47`
- `lake clean` exit `0`
- `lake build` exit `0`
- build-output SHA-256
  `ae596713922bfa5564d6f77826f3a550d03dd9d515f23353f632d087287b4b1d`

Its complete returned evidence exactly matches both
`klean-generation/preflight.json` and the preflight object bound in
`/audit-input.json`.

The initial failure, its cause/workaround, the successful diagnostic build, and
the successful required preflight are in
`evidence/03c-initial-preflight-failure-reproduced.log`,
`evidence/03a-lake-environment-diagnostic.log`,
`evidence/03b-lean-sandbox-readlink-workaround.log`, and
`evidence/04-klean-preflight-check-generation.log`.

## Obligation bijection and fixed target

I separately audited the generated sidecars and project rather than relying on
the preflight verdict.

The independently classified domain set is `[]`.
`input-manifest.json.source_rules`,
`generated/obligation-map.json.source_rules`, and the obligation list are all
exactly `[]`. The trust-parameter list is also `[]`. Hence the exact
source-rule/obligation bijection is the unique empty-to-empty bijection: no
omission, duplicate, extra, irrelevant, weakened, or vacuous conjunct exists.

The obligation-map file SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`. Counts are zero in the obligation map,
generator manifest, export result, generated preflight, and audit input. All
statuses are consistently `KLEAN_NO_OBLIGATIONS`.

The trusted target parser returns null, the independently reconstructed expected
target definition is null, and no Lean source contains a
`def targetStatement` declaration. Target fields are null in the generator
manifest, generated preflight, and audit input. Thus the fixed generated target
is genuinely absent and has not been changed. The generated project contains no
`sorry`, `admit`, or `unsafe`; its recorded 47 executable-boundary trust
declarations exactly match the generated trust inventory. With no generated
proposition or Stage 5 proof, none can be used to establish a hidden theorem.

Raw evidence:
`evidence/05-manifest-obligation-target-audit.log`.

## Stage 5

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. There is no
candidate project to copy, no `Proof.final`, no target parameters to bridge,
and no axiom dependency list to reconcile. This is the required shape for a
legitimate `KLEAN_NO_OBLIGATIONS` generation.

## Final judgment

The inventory is complete and identity-preserving; every rule's protected class
agrees with its actual syntactic and operational role; the true domain-lemma
set is empty; producer provenance is intact; deterministic generation is bound
to the frozen inputs; the empty obligation map is exact; and no generated
target or Stage 5 candidate exists. There are no audit concerns within the
requested Stage 3–5 scope.

VERDICT: PASS
LEGITIMACY: LEGIT
