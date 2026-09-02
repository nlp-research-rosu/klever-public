# Independent Stage 3–5 audit: `63-fibfib`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_AND_PROOF`, condition
`kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. I independently
audited the frozen Stage 1 K workspace, the protected Stage 3 classification,
the deterministic Stage 4 generation, and the Stage 5 Lean proof. Candidate
comments, prior reviews, and prior PASS results were not used as authority.

The classification is complete and correct, Stage 4 is reproducible and
bijective, and the candidate proves the fixed target with operationally honest
bindings. The complete command ledger and raw results are under `evidence/`.

## Producer and input provenance

Before judging Stage 4, I hashed the exact mounted producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These hashes match both `source-manifest.json` and
`generator-manifest.json`. The producer tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`. The immutable generator image identity is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator manifest, and the basename of the
launcher-recorded producer-source path.

I also verified the signed audit-input digest and recomputed every hash having a
mounted object: the Stage 1 pipeline and export trees, all 773 Stage 1
source-file hashes, the Stage 2 audit tree, discovery manifest, full Stage 4
generation tree, generated project tree, producer tree, trust inventory, and
candidate workspace tree. All match. The launcher records a Stage 5 invocation
tree hash, but no invocation tree is mounted; that launcher-only value remains
covered by the valid signed-resolution digest and is not used as proof
evidence. See `evidence/01-provenance-and-hashes.log`.

## Stage 3 inventory reconstruction and classification

Using the trusted `tools.k_rule_inventory.inventory_verification`, I
reconstructed the local closure of the selected `VERIFICATION` module. The
closure is `VERIFICATION-SYNTAX`, then `VERIFICATION`; it contains six rules.
The frozen `verification.k` hash is
`0ba6e76046e41525071a3b16fa409cd680b26b165b60bb78452d51a8128fe2e4`,
and the canonical whole-inventory hash is
`080f92c29f904570f666abf93dd802a1044388939b36ecd9797a9376820299d0`.

For every entry I independently recomputed its exact source span, whitespace-
normalized SHA-256, and hash-derived `source_rule_id`. The six identities are
unique and occur in exactly the same order in `lemma-discovery.json`; there are
no omitted, duplicate, extra, reordered, or unclassified rules.

| Lines | Rule hash suffix | Independent classification | Judgment |
|---:|---|---|---|
| 17 | `06e1ae240693…` | `DEFINITION` | Defines `fibfibSpec(0) = 0`. |
| 18 | `f91d06a62055…` | `DEFINITION` | Defines `fibfibSpec(1) = 0`. |
| 19 | `007e98cae0e9…` | `DEFINITION` | Defines `fibfibSpec(2) = 1`. |
| 20–23 | `333596937108…` | `DEFINITION` | Guarded recurrence for indices at least three. |
| 24–26 | `abff69f2453c…` | `DEFINITION` | Totalizes the named summary to zero on negative integers. |
| 30–34 | `2c1e06471f40…` | `DOMAIN_LEMMA` | Shifted recurrence used to close the loop invariant. |

The first five rules are equations defining the named mathematical summary,
including its negative-integer totalization. They do not replace program
execution and are not ordinary operational observations.

The simplification rule is not a definition: it states
`F(I)+F(I+1)+F(I+2)=F(I+3)` for `I >= 0`. It is mathematically valid by
instantiating the defining recurrence at `N=I+3` and using integer addition's
associativity and commutativity. It is materially relevant because the source
loop updates the consecutive triple `(a,b,c)` by `a+b+c`, and the Stage 1 loop
claim tracks `(F(I),F(I+1),F(I+2))`.

It is not a `PROVED_DERIVED_LEMMA`: `prove.sh` compiles it into
`verification.k` before the only `kprove` invocation, with no earlier proof of
the exact rule against a module excluding it. Therefore `DOMAIN_LEMMA` is the
only valid classification. There are no operational or proved-derived entries,
and the sole simplification is classified in an allowed category. Detailed
reconstruction is in `evidence/02-reconstructed-inventory.json`,
`03-stage3-contract.json`, and `04-independent-bijection.log`.

## Stage 4 deterministic generation and mathematical adequacy

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1, Stage 3, Stage 4, and pinned-toolchain paths. The
ambient sandbox initially prevented Lean from resolving `/proc/<pid>/exe`;
that raw failure is preserved in
`evidence/05a-preflight-initial-failure.log`. The sandbox PID namespace does
not expose its numeric PIDs through the mounted `/proc`. I reran with the
pinned Lean 4.22.0 binaries and the source-visible
`evidence/proc-exe-readlink-shim.c`, which only supplies the pinned executable
path for that readlink. It does not intercept source access, compilation, proof
checking, or output.

The mandated preflight then returned `PASS`, with clean/build exit codes zero,
one obligation, zero designated sorries, 43 recorded generated trust
declarations, and the expected immutable hashes. Its returned evidence is
`evidence/05b-preflight-rerun.json`.

The independently reconstructed true domain set has exactly one member, and
the obligation map has exactly one source rule and one obligation with that
same ordered identity:

`rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8`.

The source text, span 30–34, normalized hash, inventory hash, and discovery hash
are exact. The generated conjunct preserves the universal `I`, the
`I >= 0` guard, all three left-hand summary applications, hooked integer
addition, and the `F(I+3)` result. It contains no added `True`, disjunction,
duplicate, omission, or weakened equality. Although Lean reports the proof
variable `h` as unused in the equality body, the guard remains the premise of
the universally quantified implication; it is not removed.

The generated target is exactly one definition:

- declaration: `Klean63Fibfib.Lemmas.targetStatement`
- file: `Klean63Fibfib/Lemmas.lean`
- definition hash:
  `faafa8610390835b211eaf3bc454bfd1a111cb78a1f6602809373c567ace656a`
- fixed statement hash:
  `6d04586ce45b3ed6e6dea92e113b1b14408ee13f0098108255ec21a58fbc56b1`

The declaration, definition, applied statement, three parameter bindings,
binding hashes, and target hashes match the obligation map, generator manifest,
preflight result, and `/audit-input.json`. See
`evidence/06-stage4-independent-audit.log`.

## Stage 5 clean build, target identity, and source hygiene

I created the fresh workspace
`/tmp/audit-work/63-fibfib-proof.zz70ap`, copied the candidate into it, and
copied the immutable generated project into `Base`. I then ran both
`lake clean` and `lake build`. Both exited zero; the complete transcripts are
`evidence/07a-lake-clean.log` and `07b-lake-build.log`.

The trusted full mechanical gate independently repeated Stage 4 preflight,
copied and rebuilt the candidate, checked the final theorem type, ran the axiom
audit, and returned `PASS`; see `evidence/08-trusted-final-gate.json`.

An independent source scan found exactly one definition of each required target
parameter, exactly one `Proof.final`, no candidate declaration named
`targetStatement`, and no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`
token in candidate-owned Lean sources. The copied Base target is byte-for-byte
the generated target. `Proof.final` has exactly the fixed applied target as its
type, not a duplicate or restatement:

`Klean63Fibfib.Lemmas.targetStatement «_>=Int_» «_+Int_» «fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»`.

See `evidence/12-candidate-static-audit.log`.

## Axiom accounting and proof identity

I ran the exact audit source `evidence/AxiomAudit.lean`, including
`#print axioms Proof.final`. The exact output in
`evidence/09-print-axioms.log` is:

```text
Proof.final : Klean63Fibfib.Lemmas.targetStatement Proof.«_>=Int_» Proof.«_+Int_»
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»
'Proof.final' depends on axioms: [propext, Quot.sound]
```

`sorryAx` is absent. Neither dependency is a candidate or generated axiom:
`propext` and `Quot.sound` are Lean's core logical baseline, explicitly
accepted by the trusted final-gate policy alongside `Classical.choice`. None of
the 43 declarations in the generated `trust-inventory.json` is used by
`Proof.final`, and there is no unrecorded proof trust escape. The mechanical
reconciliation is in `evidence/14-axiom-accounting.log`.

## Operational bridge audit

The three fixed target parameters were checked against their `kore_symbol`,
source-rule binding, frozen K, generated sorts, source solution, and candidate
definition:

1. `Lbl'Unds-GT-Eqls'Int'Unds'` is a total hooked symbol with
   `hook("INT.ge")`. `SortInt` and `SortBool` lower to Lean `Int` and `Bool`.
   The candidate defines it as `decide (x0 ≥ x1)`, exactly preserving K
   integer comparison.
2. `Lbl'UndsPlus'Int'Unds'` is a total hooked symbol with `hook("INT.add")`.
   The candidate defines it as `x0 + x1`, exactly preserving unbounded K
   integer addition.
3. The summary parameter is defined as `fibfibInt`, backed by a recursive
   `fibfibNat` with bases `0,0,1`, the shifted ternary recurrence, and
   `Int.toNat` negative totalization. For nonnegative indices this is the
   frozen recurrence; for negative integers `toNat` is zero and hence gives
   the frozen value zero.

The independent Lean source `evidence/BridgeDefinitionProof.lean` proves all
three frozen base equations, the negative rule for every negative integer, the
original frozen recurrence for every `n >= 3`, and exact equality of the two
hook implementations. It checks with exit zero in
`evidence/11b-bridge-definition-proof.log`.

Adversarial values include negative indices, all recurrence boundaries, source
examples, mixed-sign addition, and comparison boundaries. The candidate
produced:

```text
ge:      [false, true, true, false]
add:     [3, 0, 7]
summary: [0, 0, 0, 0, 1, 1, 2, 4, 24, 274]
```

These correspond to indices `[-5,-1,0,1,2,3,4,5,8,12]` and match an
independent recurrence/source-loop oracle. The source three-register loop and
frozen summary also agree for every input from 0 through 100. Evidence is in
`10d-bridge-adversarial.log` and `13-operational-bridge-audit.log`.

The counterfactual audit is deliberately discriminating. A constant-zero
summary satisfies the generated recurrence, and a constant-false comparison
makes its guard vacuous; `evidence/BridgeAudit.lean` machine-checks both facts.
They are nevertheless operationally false: constant zero disagrees with the
frozen base at index 2 (`0` versus `1`), and false comparison disagrees at
`0 >= 0`. A left-projection addition disagrees on `2+3` (`2` versus `5`).
The submitted candidate is none of these convenient bridges and matches the
frozen operations at each witness and universally by its definitions and the
independent Lean equations. Thus the fact that structural proof alone would
accept bad parameter interpretations does not create a candidate failure; the
required operational-bridge gate rules them out.

## Final judgment

The frozen rule inventory and Stage 3 classification are exact; the sole true
domain lemma is relevant and correctly exported; Stage 4 producer provenance,
obligation bijection, and target identity are intact; and the Stage 5 proof
cleanly proves the exact fixed target with fully reconciled trust and honest
operational bindings.

VERDICT: PASS
LEGITIMACY: LEGIT
