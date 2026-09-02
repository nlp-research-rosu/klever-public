# Independent Stage 3 / Stage 4 Audit

Problem: `102-choose-num`  
Condition: `semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`  
Launcher mode: `CLASSIFICATION_ONLY`

## Scope and trust posture

I treated the Stage 1 workspace, Stage 2 audit, protected Stage 3
classification, Stage 4 generation, generation-time producer sources, logs,
comments, and manifests as untrusted evidence. I did not rely on the selected
Stage 2 verdict or any prior classification. The checks below use the trusted
code in `/reference/tools` and independent inspection of the frozen K source,
source solution, postcondition, and supplied operational semantics.

`AUDIT_MODE` is `CLASSIFICATION_ONLY`, exactly matching
`/audit-input.json`. The signed resolution has no Lean workspace, Lean
invocation, target, or Stage 5 result, and `/candidate` is absent. Stage 5 proof
identity, `#print axioms Proof.final`, and operational-bridge parameter checks
are therefore not applicable.

## Immutable inputs and generator provenance

I recomputed the signed resolution digest, every available resolution tree/file
hash, the complete per-file Stage 1 source-hash map, and the selected artifact
hashes. All comparisons passed:

- signed resolution: `df566e18596b86686e8a73576847fbf89a7bf93c918f5cae81e1a132dc63844a`;
- Stage 1 pipeline tree:
  `7d836d922fe828aa6f193f1f9bd5ce05d809f5d6e1066df3656222e873043569`;
- Stage 1 deterministic-export tree:
  `f16552e370a67cfb3c649eecdf7e3ca5746ec9374edc8c6a9ba3db02f8985a64`;
- Stage 3 manifest:
  `365fd0e41168d4ff417a9e80e2432bdc1a8ceed714140f62fd265b4abcdacb35`;
- selected Stage 2 tree:
  `e87dbfc2a301bd94e363b9f2f66e59914d2dbc222e5738f54c5f072b335d0bf7`;
- selected Stage 4 generation tree:
  `425f39d4380f90c5cd8c59e8b58e4ccac2f44c83f979d63190fb5ef31f1f75b4`;
- generated Lean project tree:
  `b7baf821e1ee0ca496d34024e5ebea428e94c5d0925fe2848bccccc2658ae006`;
  and
- producer-source bundle tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

Before judging Stage 4, I hashed the two mounted generation-time producers:

| Producer | Observed and required SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes equal `generator-manifest.json` and
`source-manifest.json`. The source manifest, generator manifest, and producer
bundle path recorded in `/audit-input.json` all bind the same immutable image:

`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.

The producer bundle contains exactly `klean_export.py`, `klean.py`, and
`source-manifest.json`; there is no missing or extra producer file. The
generator toolchain object also exactly equals
`/reference/klean-toolchain.lock.json`. There is no producer-provenance
`AUDIT_ERROR`.

## Canonical Stage 1 rule inventory

Using `tools.k_rule_inventory.inventory_verification` on the frozen Stage 1
workspace, I reconstructed the local closure selected by `prove.sh`. The
selected module is `CHOOSE-NUM-VERIFICATION`; its local `verification.k`
closure contains only that module. Imports from the supplied MPY semantics are
external to the local verification-file rule inventory.

The frozen `verification.k` SHA-256 is
`75326a4ee966fbd0a381571838bb8dd97c307aa193ab21f0f6120e23f413c956`.
The canonical inventory contains exactly these two rules, in this order:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Attributes |
|---:|---|---|---|
| 1 | `verification.k:13-17` | `c03e276aa838c9ccf89f1a02a5355f619fd9394ba2274696d4c6c3b5f6c8c047` / `rule-c03e276aa838c9ccf89f1a02a5355f619fd9394ba2274696d4c6c3b5f6c8c047` | none |
| 2 | `verification.k:19-40` | `322c7434385e18d731b0a8f9faaae283673f25cd14302a2d02662c6bb69252e0` / `rule-322c7434385e18d731b0a8f9faaae283673f25cd14302a2d02662c6bb69252e0` | none |

For each rule I independently sliced the recorded source lines, checked exact
text equality, normalized whitespace, recomputed the normalized hash, and
re-derived `source_rule_id`. I then recomputed the canonical JSON inventory
hash:

`7404ea53de69b0b6e2830923e167cbfa6ba2cdebf210b3f3c87ebd119d70c3ee`.

That hash equals the protected Stage 3 manifest and the Stage 4 input and
generator provenance. The protected manifest contains the same two identities
once each and in canonical order. There are no omissions, duplicates, extras,
reordered identities, changed hashes, or unaccounted rules. Neither rule has a
`simplification` attribute, so the simplification-class policy is satisfied
vacuously.

## Independent classification judgment

### `largestEvenInRange`: `DEFINITION`

The first rule is the sole, unguarded defining equation for the declared
`[function, total]` symbol `largestEvenInRange(Int, Int)`. It names the
mathematical result summary used on the right side of the
`all-positive-inputs` postcondition; it does not rewrite a source-program term
or replace operational execution.

For positive `Y`, the supplied `pyMod(Y, 2)` is `0` for even `Y` and `1` for
odd `Y`. Thus `Y - pyMod(Y, 2)` is the greatest even integer at or below `Y`,
and the `X <=` test returns it exactly when it lies in `[X,Y]`; otherwise the
definition returns `-1`. This is a relevant, complete named summary, not a
domain theorem disguised as a definition.

### `#chooseNum` entry rule: `OPERATIONAL_RULE`

The second rule expands the proof-harness redex `#chooseNum(X,Y)` into a
`Call` of `closureVal(("x","y"), BODY, 0)` with arguments `X,Y`. The closure
body is the exact statement sequence in frozen `solution.mpy`, which in turn
matches the frozen `solution.py` AST:

1. test `y % 2 == 0`;
2. on the even branch, return `y` iff `y >= x`, otherwise `-1`;
3. on the odd branch, return `y - 1` iff `y - 1 >= x`, otherwise `-1`.

The supplied operational semantics then evaluates the call rather than
replacing it with an oracle: `call.k` evaluates the callee and arguments,
allocates a fresh frame, binds `x` and `y`, and executes `BODY`;
`syntax.k` enforces expression/statement strictness; `core.k` performs name
lookup and argument sequencing; `controls.k` selects the `If` branch;
`operators.k` dispatches arithmetic and comparisons; `int.k` supplies Python
modulo, subtraction, equality, and ordering; and `functions.k` performs
`Return` and restores the caller frame. The rule neither states nor assumes the
answer. It is therefore an ordinary execution-entry rule, not a definition of
the mathematical result, a derived lemma, or a domain lemma.

As supporting adversarial evidence, I statically compared the frozen source AST
to the locally audited operational model, exercised twelve parity and boundary
cases, and obtained agreement with the mathematical summary in every case. A
parity-flipped counterfactual implementation differed on nine of the cases,
including even/odd singleton ranges and both endpoint parities. These examples
support body sensitivity; the classification itself follows from the exact
source and operational rules, not from finite tests.

### Resulting partition

- `DEFINITION`: one rule, `largestEvenInRange`;
- `OPERATIONAL_RULE`: one rule, the `#chooseNum` execution entry;
- `PROVED_DERIVED_LEMMA`: none; and
- `DOMAIN_LEMMA`: none.

There is consequently no claimed derived lemma whose proof chronology must be
validated, no mislabeled or irrelevant domain lemma, and no simplification rule
that needs a domain obligation. My partition exactly matches Stage 3, but the
judgment above was made independently.

## Deterministic Stage 4 generation

I reran the required trusted call
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and:

- frozen input `/reference/k-proof`;
- discovery manifest `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`; and
- toolchain lock `/reference/klean-toolchain.lock.json`.

The returned status is `KLEAN_NO_OBLIGATIONS`. The copied generated project
passed `lake clean` and `lake build`; both exited 0. The returned evidence
reconfirms the Stage 1 export hash, Stage 3 manifest hash, generated tree hash,
zero designated sorries, zero obligations, `target: null`, and 48 generated
trust declarations. The trusted preflight independently rejects proposition
trust, unexpected proof holes, forbidden imports/tokens, and deviation from
the trust allowlist.

The audit sandbox initially exposed a PID-namespace `/proc` mismatch that
prevented Lean 4.22 from locating its executable before elaboration. The
recorded compatibility shim only makes `getpid()` agree with the PID visible
through `/proc/self`; it does not alter the copied project, Lean source,
manifests, declarations, or target. The initial failure and successful rerun
are both retained in evidence.

I also checked Stage 4 independently of the preflight result:

- my true domain-lemma set is empty;
- the Stage 4 input manifest `source_rules` list is empty;
- the obligation map has empty `source_rules`, `obligations`, and
  `trust_parameters` lists;
- the generator and export result both record obligation count zero;
- `expected_target_definition` and the generated target scan both return
  `null`;
- no generated `GeneratedTarget` declaration exists;
- the generator manifest, prior preflight, export result, selected status, and
  audit input consistently record `KLEAN_NO_OBLIGATIONS` and no target;
- no empty or `True` conjunct exists (there are no conjuncts at all); and
- there is no Stage 5 candidate.

Thus the source-rule/obligation mapping is the exact empty bijection induced by
the independently empty domain set. Nothing was omitted, duplicated, weakened,
made vacuous, or redirected to another target. `KLEAN_NO_OBLIGATIONS` is
substantively correct, not merely self-consistent.

## Evidence index

Raw commands and results are under `/audit-output/evidence/`:

- `audit-checks.log`: successful hash, inventory, classification-case,
  Stage 4 structure, and trusted preflight commands/results;
- `audit-checks-initial-failed.log`: retained initial Lake environment failure;
- `hash_and_provenance_check.py`: complete hash/provenance recomputation;
- `inventory_check.py`: canonical reconstruction and bijective comparison;
- `independent-classification.json`: independent per-rule judgments;
- `classification_cases.py`: static AST, boundary, and counterfactual checks;
- `stage4_structure_check.py`: empty bijection and fixed-null-target checks;
- `preflight_check.py`: exact trusted `check_generation` invocation;
- `source-excerpts.log`: numbered frozen source, postcondition, and relevant
  operational-semantics rules; and
- `LEAN_ENVIRONMENT_NOTE.md` plus `proc_pid_shim.c`: documented, reproducible
  audit-container compatibility handling.

VERDICT: PASS
LEGITIMACY: LEGIT
