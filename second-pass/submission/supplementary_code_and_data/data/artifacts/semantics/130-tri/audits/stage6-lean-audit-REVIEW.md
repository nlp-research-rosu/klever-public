# Independent Stage 3–5 audit: HumanEval 130-tri

## Scope and outcome

The launcher and environment both select `CLASSIFICATION_AND_PROOF`; the
condition is `semantics` and the semantics mode is `SUPPLIED_SEMANTICS`. I
independently audited the frozen Stage 1 `verification.k`, protected Stage 3
classification, authenticated Stage 4 producer and generated project, and the
Stage 5 Lean candidate. I did not rely on the selected Stage 2 verdict, prior
Stage 4 preflight, or prior Stage 5 success.

The evidence is under `evidence/`. `evidence/00_commands.txt` records the
commands; subsequent files contain their results and the independent audit
sources.

## Input and producer integrity

All mounted input hashes that can be recomputed from the supplied mounts match
`/audit-input.json`:

- Stage 1 pipeline tree:
  `2a684e17d61dbed61a8420c6fe0b93172b2fa7450ed845461374f0d7f894d816`.
- Stage 1 export tree:
  `07d8327c2606aeb4c4160768d9a425c996690be0647fae02ff5cd2a4f4cc65c4`.
- Stage 3 manifest:
  `f00c11a53001f56e840b98bd4d98c67e2854b806cc3e3a7ed2ea0902877d745d`.
- Selected Stage 2 tree:
  `3bdaf25fa4cfaa326afd79febb88e3755ff627c8c312937eda170e61c0621afd`.
- Stage 4 generation tree:
  `cf929a87f3432eebfd5b4014f2a77b64f801b1445715622c2024e56d5d570fc3`.
- Generated project:
  `eac179e2962be6518d3e040f4ec559c46844cf087444847073a57f723ca96acf`.
- Stage 5 workspace:
  `9de84124b9f7dadc7b861550cc4348b9a5d1623b5c960e785690a588dd377568`.
- Producer source bundle:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

All 32 individually recorded Stage 1 source hashes also match. The launcher
input at `/audit-input.json` and its mounted copy in `/audit-output` have the
same SHA-256.

I authenticated Stage 4 before judging it. The producer bundle contains
exactly `klean.py`, `klean_export.py`, and `source-manifest.json`. The observed
producer hashes are:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`.
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`.

They match both `source-manifest.json` and `generator-manifest.json`. The image
ID in both manifests is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
the same digest is the final component of the launcher-recorded immutable
producer path. There is no producer-provenance infrastructure error.

## Stage 3 inventory reconstruction

I invoked the trusted
`tools.k_rule_inventory.inventory_verification` on the frozen Stage 1
workspace. `prove.sh` selects `TRI-VERIFICATION`, and the local
verification-module closure contains exactly that module. The reconstruction
found 16 rules, with:

- frozen `verification.k` SHA-256
  `40204e637c95c116d96e031fba8896cffe4170018369184a89384d9648936b3c`;
- inventory SHA-256
  `22d7ad4bc3ed7a5278b63b8aded18b021a7eb89701c1bb6f41c416fa399e49fa`;
- 16 unique reconstructed identities and 16 unique Stage 3 identities;
- exact ordered identity equality; and
- no omitted, extra, duplicated, or reordered rule.

For every entry I recomputed its source span, whitespace-normalized source
hash, and `source_rule_id`. Every value matches the protected manifest.
`evidence/03_rule_inventory.tsv` gives all 16 full identities, hashes, spans,
attributes, and classifications; `evidence/03_rule_text.txt` gives all
reconstructed rule bodies.

## Independent classification judgment

My classification is 14 `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and two `DOMAIN_LEMMA`. It agrees entry-for-entry with
Stage 3.

The definitions are:

- Lines 12 and 13: the two base equations for the named mathematical summary
  `triAt`.
- Lines 15–18: the even-index defining equation for `triAt`.
- Lines 27–31: the odd-index recurrence defining `triAt`.
- Lines 48 and 49: base representations of `triPrefix`.
- Lines 50–52: base and structural projection equations for the named
  `prefixIndex` summary.
- Lines 53–58: the inductive observation equation for advancing
  `prefixIndex`.
- Lines 59–62: the inductive `triPrefix` append recurrence.
- Lines 67–68, 71–86, and 89–100: exact macro expansions of the named
  `TriLoopCond`, `TriLoopBody`, and `TriFunctionBody` proof terms.

These rules name summaries, recurrences, projections, or macro proof terms.
They do not replace an ordinary fixed-semantics execution transition. The
three macros exactly reproduce the translated loop condition, loop body, and
function body in `solution.mpy`.

The two true domain lemmas are:

1. Lines 22–25,
   `rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac`,
   which equates the backend-canonical even expression `I /Int 2 +Int 1`
   with the already defined even `triAt(I)` under the even guard.
2. Lines 34–40,
   `rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019`,
   which equates the Haskell-backend form obtained after `pyMod` unfolds with
   the already defined odd recurrence under the odd guard.

Neither is a definition: each is an additional arithmetic normalization of a
previous defining rule. Neither is an operational rule or a derived lemma
first proved without itself; there are no entries in those categories. Both
are directly relevant. The even source branch computes `1 + i // 2`; the odd
source branch computes the two preceding values plus the following-even
contribution. These are exactly the two expressions normalized by the
lemmas, and the Stage 1 postcondition observes the resulting `triAt` prefix.
All 12 rules bearing `simplification` are classified as either a definition
or one of these domain lemmas.

## Deterministic Stage 4 generation

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
specified frozen Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
trusted toolchain lock. The pinned toolchain is K 7.1.293, pyk/Klean 7.1.293,
Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and Codex 0.144.6.

The sandbox initially blocked Lean's `/proc/<pid>/exe` installation lookup. I
used the narrow local readlink compatibility shim recorded in
`evidence/lean_proc_readlink_shim.c`; the frozen-toolchain assertion then
passed. This changes no audited input or toolchain binary. The exact rerun
returned `PASS`, two obligations, zero designated sorries, 49 generated trust
declarations, and successful temporary `lake clean` and `lake build`.
`evidence/preflight-check-generation.json` is the returned evidence.

The independently reconstructed domain IDs, Stage 4 `source_rules`, and
generated obligation IDs are the same two-element list in the same order.
Each obligation has the exact source span, normalized hash, inventory hash,
discovery hash, and conjunct hash. There are no duplicates.

Mathematically, the generated conjuncts are exactly:

1. For every `I`, if `I >= 2` and `pyMod(I,2) = 0`, then
   `I /Int 2 +Int 1 = triAt(I)`.
2. Write `r(x) = ((x %Int 2) +Int 2) %Int 2`. For every `I`, if
   `I >= 3` and `r(I) = 1`, then
   `triAt(I-1) +Int triAt(I-2) +Int 1 +Int
   ((I+1 -Int r(I+1)) /Int 2) = triAt(I)`.

These preserve the complete guards and arithmetic terms from lines 22–25 and
34–40. They are not weakened, duplicated, irrelevant, or vacuous. With the
honest operational bindings, `I=2` inhabits the first guard and `I=3`
inhabits the second.

The target is the exact conjunction of those two obligations. Independently
recomputing it gives:

- declaration `Klean130Tri.Lemmas.targetStatement`;
- file `Klean130Tri/Lemmas.lean`;
- definition hash
  `92a96f09666026a01308bf93e75fdbcc19f3fcac3b897328c115cef7a76041b8`;
- instantiated-statement hash
  `c4dd23f0a31621f4a02e486b02d1032e12aa5a10575a3933cbe01c6df042340c`.

The complete target object is identical in the generated project,
`generator-manifest.json`, the rerun preflight, and `/audit-input.json`. The
obligation-map SHA-256 is
`3476a69da9c3bd2836fa2d5ffa10d6b42530f885e7ded123d2889227a2c505ea`,
matching the generator manifest. All nine parameter-binding hashes recompute
from their KORE symbol, Lean name, type, and source-rule IDs. Both conjunct
hashes recompute, and the trust-inventory SHA-256
`f91fde9c0fc243fe504e8838edfd7124f9addd062095c9cc5d6596c69b417113`
matches `export-result.json`. The generator's toolchain object exactly equals
the trusted lock. `evidence/05_recorded_hashes.txt` records these comparisons.

## Stage 5 project and theorem identity

I created `/tmp/audit-work/lean-audit.EcpzYz/Project`, copied the four candidate
project files into it, and copied the immutable generated project into
`Project/Base`. The Base copy has the same generated-tree hash
`eac179e2962be6518d3e040f4ec559c46844cf087444847073a57f723ca96acf`.

From that fresh project:

- `lake clean` exited 0 with no output.
- `lake build` exited 0 and built `Proof`; its only diagnostics were the two
  generated unused-hypothesis linter warnings in `Lemmas.lean`.

The complete output is in `evidence/06_fresh_clean_build.txt`. The trusted
`stage5_mechanical_check.py` independently repeated the fresh-copy build and
returned `PASS`.

The candidate has only `Proof.lean` and `lakefile.lean` as Lean sources. It
contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. Each of the nine
required parameter definitions occurs exactly once. The candidate contains no
`targetStatement`; Base contains exactly one, so the candidate neither changes
nor shadows the generated target. It contains exactly one `theorem final`.
The trusted static gate confirms its type annotation is the exact generated
statement, not a duplicate or weakened variant.

An explicit kernel check printed:

```text
Proof.final : Klean130Tri.Lemmas.targetStatement Proof.«_-Int_» Proof._andBool_ Proof.«_>=Int_» Proof.«_==Int_»
  Proof.«_%Int_» Proof.«_+Int_» Proof.«_/Int_» Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» Proof.triAt
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Thus `Proof.final` proves exactly the fixed target. The used axiom set contains
only the three standard Lean trust-base axioms explicitly permitted by the
trusted mechanical gate. It uses none of the 49 generated allowlisted axioms.
The trust inventory records zero designated and other sorries and no automatic
axiomatization. There is no `sorryAx` and no unrecorded proof escape.

## Operational-bridge audit

The candidate bindings agree with the frozen KORE symbols, source rules, and
operational semantics:

| Parameter | Candidate definition | Frozen meaning | Judgment |
|---|---|---|---|
| `«_-Int_»` | `a - b` | `INT.sub` | Exact |
| `_andBool_` | `a && b` | total `BOOL.and` | Exact truth table |
| `«_>=Int_»` | `decide (a ≥ b)` | `INT.ge` | Exact |
| `«_==Int_»` | `decide (a = b)` | `INT.eq` | Exact |
| `«_%Int_»` | `Int.tmod a b` | `INT.tmod` | Exact wherever K defines it |
| `«_+Int_»` | `a + b` | `INT.add` | Exact |
| `«_/Int_»` | `Int.tdiv a b` | `INT.tdiv` | Exact wherever K defines it |
| `pyMod` | `tmod (tmod a b + b) b` | frozen `((a %Int b)+Int b)%Int b` | Exact wherever K defines it |
| `triAt` | even closed form; odd `k*(k+2)` | frozen bases/even equation/odd recurrence | Exact on the full nonnegative source domain |

K's `/Int` and `%Int` hooks are undefined at divisor zero, while the generated
target requests total Lean parameters. The candidate's total extensions at
zero therefore do not replace any defined K result; every generated occurrence
uses divisor 2. The frozen `triAt` equations cover nonnegative indices, and
both obligations use only that domain (`I >= 2`, with recursive arguments at
least 1). Its arbitrary total extension outside the frozen rule coverage is
irrelevant and non-conflicting.

I compiled a fresh minimal K definition importing `INT` and `BOOL`. Ground
execution confirmed truncating `-8 %Int 3 = -2`, truncating
`-8 /Int 3 = -2`, `true andBool false = false`, and the combined negative
comparison/equality witness. Lean ground tests exercised both operand signs,
the full Boolean truth table, comparisons, equality, `pyMod`, and `triAt`.
The resulting prefix was:

```text
[1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6, 48, 7]
```

An independently implemented recurrence oracle compared the frozen source
recurrence with the candidate closed form for every `n` from 0 through 10,000
and found zero mismatches. In addition, `evidence/SourceRulesAudit.lean`
machine-checks both frozen `triAt` bases and universally proves the exact
guarded even defining equation (lines 15–18) and guarded odd defining
recurrence (lines 27–31) for the candidate bindings.

Counterfactual tests were discriminating:

- A constant-false `_andBool_` makes both generated implications vacuous; the
  audit file proves this mutation can satisfy the target. This demonstrates
  that a clean theorem alone is insufficient.
- The actual candidate uses the exact Boolean conjunction, and the ground
  truth-table test confirms it is not that vacuous binding.
- A constant-zero `triAt` is refuted by the first obligation at `I=2`
  (`2 ≠ 0`).
- An identity `triAt` is refuted by the second obligation at `I=3`
  (the source value is `8`, not `3`).
- Negative division and remainder witnesses distinguish truncating K hooks
  from convenient Euclidean replacements.

The operational bindings are therefore body- and value-sensitive rather than
constant, identity, hard-coded, or vacuous shortcuts.

## Final judgment

The Stage 3 classification is complete and correct, the authenticated Stage 4
generation is deterministic and exactly bijective with the two genuine domain
lemmas, the target is fixed and unweakened, and `Proof.final` cleanly proves
that exact target with honest operational bindings and no unaccounted trust.

VERDICT: PASS
LEGITIMACY: LEGIT
