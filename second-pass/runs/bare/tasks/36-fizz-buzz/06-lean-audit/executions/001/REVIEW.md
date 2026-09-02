# Independent Stage 3–5 audit: `36-fizz-buzz`, `bare`

## Scope and conclusion

The launcher mode and signed resolution both say
`CLASSIFICATION_AND_PROOF`; the semantics mode is
`GENERATED_SEMANTICS`. I treated the mounted Stage 1–5 artifacts and earlier
reviews as evidence only. Classification and operational adequacy were
reassessed from the frozen K source, source program, generated Lean statement,
and candidate definition.

The audit passes. The local Stage 1 rule inventory is complete and matches the
Stage 3 manifest bijectively and in order. The independent classification is
12 definitions/macros and one relevant domain lemma: integer-addition
associativity. Stage 4 generates exactly that one obligation. The Stage 5
candidate implements the bound K symbol as Lean integer addition, proves the
unchanged target after a clean build, and uses no disallowed axiom or proof
escape.

## Launcher and hash binding

`/audit-input.json` has a valid schema-3 signed envelope. Its canonical
resolution digest recomputes to
`4994c603954d41b3ad4acdb27bc5ab331624254f9301b46891d42b028ecd673f`.
`AUDIT_MODE`, the signed mode, and the presence of `/candidate` agree.

Every recorded hash whose object is a mounted audit input was independently
recomputed with the trusted hash implementation:

| Object | Recomputed hash | Result |
|---|---|---|
| Stage 1 pipeline tree | `21ed0d0c7c006fb5f568f4efcc73e8db7a5bfbd68b03086d798c6c88f80f5f44` | matches |
| Stage 1 exported tree | `b991023a78aa688227026b58ef3bbd7b5a46ae68901df9dec6d114506499e99d` | matches |
| Stage 2 selected audit tree | `e43167e6b0259bde0888b0f1587634089cce5d6bb6dbf865844e1b0f2989ea11` | matches |
| Stage 3 manifest file | `73d00a9c43ca6be80e8c33b3a78b35c2f30b12231a3dd2f45b6973b1e7ed5020` | matches |
| Stage 4 generation tree | `07e986bbf490737cdac4f123108ac1abf112fa56fd8401fee557692cd4335095` | matches |
| Stage 4 generated project | `7796a58da3724bfe844e4ccc3ad5df12b23c95f7db60fbda59688db408db6904` | matches |
| Stage 5 candidate tree | `e9ae0217f1381aadfe979c8f7d947bf327a8272b9de358cf5d3d384d0092a221` | matches |

The complete key set and all nine per-file Stage 1 source hashes also match.
The signed resolution contains a `lean_invocation_sha256`, but no Stage 5
invocation tree is mounted; that field was not used as proof evidence. The
mounted candidate tree itself was recomputed as shown above.

## Inventory reconstruction and Stage 3 bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on `/reference/k-proof`. `prove.sh` selects
`VERIFICATION`, and the local module closure in `verification.k` is exactly
`["VERIFICATION"]`. The reconstructed values are:

- `verification.k` SHA-256:
  `24034a2584fae5d039c164a46ecdba6763c893b5f9675d8b543d0c41897bae86`
- inventory SHA-256:
  `736568ab7f1701fa76e06519c913488b7fd319b62eb88baa3958a177a3882787`
- rule count: 13

For each entry I independently normalized its captured text by whitespace,
hashed that normalized text, rebuilt `source_rule_id` as `rule-<hash>`, and
checked its physical source span. All 13 hashes and IDs match. The Stage 3
manifest has 13 unique IDs in the identical order; there are no missing,
extra, duplicated, or reordered identities.

## Independent rule classification

| Source rule ID | Span | Independent class | Reason |
|---|---:|---|---|
| `rule-e763c3f3ce388151393e428198722a36cf283185f5d31d700c07a4fea32b597b` | 13–14 | `DEFINITION` | Negative branch of the named `fizzEnd` summary. |
| `rule-1904e693aaf0033ea4c764af47f3256dcc77b731523dc22f4cfd10611f765237` | 15–16 | `DEFINITION` | Nonnegative branch of `fizzEnd`. |
| `rule-30079623688f5b570b38f8a2896ee5b74b79a4367acc2ab3e054817b7e0cb7a7` | 18–19 | `DEFINITION` | Base equation of `digitSevens`. |
| `rule-729ad4a68b3299ff18b3488c12489276a4edfa8a890e236b5bcf981e6e3c6f89` | 20–21 | `DEFINITION` | Decreasing recurrence for a final digit equal to seven. |
| `rule-5d535d5211f655f272b25f28b219933239017014bc24e0eaa6e81b5985089d20` | 22–23 | `DEFINITION` | Decreasing recurrence for a final digit unequal to seven. |
| `rule-6f6d25b627a7de6753b30c8b1db33b14717b8740662705d84581dd0ddde88d72` | 25–26 | `DEFINITION` | First branch of the named `fizzContribution` summary. |
| `rule-e81d3927655b90d37b43ae533110b18c623a05009b9e1e9a3e154a6f97ffeb44` | 27–28 | `DEFINITION` | Second branch of `fizzContribution`. |
| `rule-ebf295199abbea4dc9a90303c80ad6f55809586ff7eeb17f56389907d94e7c15` | 29–30 | `DEFINITION` | Final branch of `fizzContribution`. |
| `rule-dde8b8487c0ea1e1e4fe6cb86253708342138e3bf3d5d148b5fe526cf90da8fe` | 32–33 | `DEFINITION` | Base equation of the interval summary `fizzFrom`. |
| `rule-7ba888d5c7f8ca80108339cec76a10640fa99b1108c9249858ebad2a85ebb7ef` | 34–35 | `DEFINITION` | Advancing recurrence for `fizzFrom`. |
| `rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7` | 38 | `DOMAIN_LEMMA` | General associativity of K mathematical integer addition. |
| `rule-948f699a84e5f8aba9d6d2c7879d7807ab825a002416eb1275a55c26ada875ab` | 43–48 | `DEFINITION` | Macro expansion of the named `INNER-LOOP` proof term to the exact AST. |
| `rule-55f4df2bb36ada94a0fbce4dfb208de6119596fecc5a3da9f9260be5f4f2b937` | 51–59 | `DEFINITION` | Macro expansion of `OUTER-LOOP` to the exact translated AST. |

This yields 12 `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`, exactly as Stage 3 records.
The operational execution rules live in frozen `semantic.k`, not in this local
verification-module inventory. No rule is claimed as proved-derived, and
`prove.sh` contains no earlier proof of rule 38 against a module omitting it:
the rule is compiled into the definition before `kprove`, so treating it as a
derived lemma would have been invalid.

The only `[simplification]` rule is rule 38, and its `DOMAIN_LEMMA`
classification is mandatory and correct. It is true because frozen
`semantic.k` imports K's `INT` module, where `_+Int_` is a total function with
hook `INT.add`. It is also directly relevant. One outer-loop step yields an
accumulator shaped as
`(C +Int fizzContribution(I)) +Int fizzFrom(I+1,N)`, while the invariant and
`fizzFrom` recurrence require
`C +Int (fizzContribution(I) +Int fizzFrom(I+1,N))`. The same reassociation
arises in the inner-loop count. Thus it is neither an operational rule nor an
irrelevant algebraic fact.

The prompt asks for the number of digit sevens in eligible integers below
`n`; `solution.py`, the loop macros, the summary definitions, and `spec.k`
align with that program and postcondition.

## Deterministic Stage 4 generation

I reran
`tools.klean_preflight.check_generation(Path("/reference/k-proof"),
Path("/reference/lemma-discovery.json"),
Path("/reference/klean-generation"), ...)` with
`PYTHONPATH=/reference`.

The first attempt exposed a sandbox-specific tool-discovery problem: the audit
sandbox has a PID namespace but a host `/proc` mount, so Lean could not find
`/proc/<namespace-pid>/exe`. The evidence includes this failure and a small
local `LD_PRELOAD` compatibility shim that returns the host-visible `Tgid`
from `/proc/thread-self/status`. The shim changes only executable discovery;
it does not modify Lean, the generated project, or any audited input. With it,
Lean identifies itself as version 4.22.0 at pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The rerun returned the same recorded evidence:

- status `PASS`;
- obligation count 1;
- designated sorry count 0;
- trust declaration count 50;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0 with output hash
  `8250decced98e3a463305169b7c4dce4053180dc193c47c8ee91fd3a8198a412`;
- all Stage 1, Stage 3, and generated-tree hashes identical to the signed
  resolution.

This is not a `KLEAN_NO_OBLIGATIONS` case: the independently classified domain
set genuinely contains rule 38.

### Source-rule/obligation bijection

The generated source-rule list and the independently reconstructed domain set
are identical and ordered. There is one unique obligation for the one domain
rule:

```text
∀ (A : SortInt) (B : SortInt) (C : SortInt),
  «_+Int_» («_+Int_» A B) C =
    «_+Int_» A («_+Int_» B C)
```

It preserves all three variables, has no guard to weaken, has no vacuous
conjunct, and is the exact equality represented by the K rule. Its provenance
span is 38–38, its source-rule ID and normalized hash are the rule-38 values
above, and its Lean-conjunct hash recomputes to
`4da5ad235ac8b67affb5ea695f933229df3e67a3ad328056cea4e88103e88b35`.
The obligation-map file hash recomputes to
`e0cf3d506c5e7d01153267bc285593189b3e1a65bb1eb6283a6c9437ad74299c`.

### Fixed target

The exact generated declaration is:

```lean
def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (A : SortInt) (B : SortInt) (C : SortInt),
      «_+Int_» («_+Int_» A B) C =
        «_+Int_» A («_+Int_» B C))
```

Independent extraction equals both `generator-manifest.json` and
`/audit-input.json`:

- declaration: `Klean36FizzBuzz.Lemmas.targetStatement`;
- statement:
  `Klean36FizzBuzz.Lemmas.targetStatement «_+Int_»`;
- definition hash:
  `f5de4b2237c7af5067d9f684fd0ceeb08bc2caf891532eba3722805ed96c620e`;
- statement hash:
  `83aeddd5dbd588726a15128801c81b7cd2d02c4ecef9f957e43beb4742104de6`.

The sole parameter binds KORE symbol
`Lbl'UndsPlus'Int'Unds'` and rule 38 to Lean name `«_+Int_»` of type
`SortInt → SortInt → SortInt`. Its canonical binding hash recomputes to
`c33da7c1697bfe5cd56f5a1028b13979a3aea7a57e3473723b2916b6004903a8`.
No obligation, parameter, or target change was found.

## Stage 5 clean proof audit

I copied `/candidate` to
`/tmp/audit-work/36-fizz-buzz-proof-audit`, copied the generated project into
that fresh workspace as `Base`, and verified `Base` has generated-tree hash
`7796a58da3724bfe844e4ccc3ad5df12b23c95f7db60fbda59688db408db6904`.
I then ran both required commands:

```text
lake clean
lake build
```

Both exited 0. The complete build output records fresh builds of
`Klean36FizzBuzz.Prelude`, `Sorts`, `Inj`, `Lemmas`, and `Proof`, followed by
`Build completed successfully.`

Outside the immutable `Base` dependency, the candidate has no `sorry`,
`admit`, `unsafe`, `axiom`, or `opaque`; it introduces no target declaration
and therefore does not change or shadow the generated target. `Proof.lean`
contains exactly one required parameter definition and one `final` theorem:

```lean
def «_+Int_» (x0 x1 : SortInt) : SortInt := x0 + x1

theorem final :
    Klean36FizzBuzz.Lemmas.targetStatement «_+Int_» := by
  intro A B C
  exact Int.add_assoc A B C
```

The theorem statement normalizes exactly to the fixed manifest statement.
An independent Lean type check prints:

```text
Proof.final : Klean36FizzBuzz.Lemmas.targetStatement Proof.«_+Int_»
```

### Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx` and no generated trust declaration is used.
`trust-inventory.json` has 50 generated allowlist entries and zero designated
or other sorries; its file hash is
`84b86d179662c5656a269b49af9d3f2c472eb0d8e751604475622f9f3bb3f4c9`.
The trusted final-gate policy explicitly permits Lean's core
`Classical.choice`, `propext`, and `Quot.sound` in addition to that generated
allowlist. A separate `#print axioms Int.add_assoc` also reports only
`[propext]`, accounting for the dependency. The reproduced trusted final gate
returns `PASS` with `used_axioms: ["propext"]`.

## Operational-bridge judgment

The generated equation is intentionally parametric, so a proof of it alone
does not determine the operational meaning of `«_+Int_»`. I checked the
candidate definition separately:

1. Frozen `semantic.k` imports `INT`.
2. The pinned K 7.1.293 `domains.md` declares
   `Int "+Int" Int [function, total, symbol(_+Int_), ..., hook(INT.add)]`.
3. The generated binding names the matching KORE symbol
   `Lbl'UndsPlus'Int'Unds'`.
4. `SortInt` is Lean `Int`, and the candidate definition is definitionally
   `fun x0 x1 => x0 + x1`.
5. The frozen source uses this operation for `count + 1`, `i + 1`, and the
   count summaries; no partiality, overflow, state, evaluation-order, or
   exceptional behavior is omitted. Both K integers and Lean integers here
   are arbitrary-precision mathematical integers.

An independent K harness using the pinned `INT.add` hook and a Lean audit of
the candidate gave identical results:

| Inputs | K `+Int` | candidate Lean definition |
|---|---:|---:|
| `-7, 3` | `-4` | `-4` |
| `0, 999999` | `999999` | `999999` |
| `7, -7` | `0` | `0` |
| `10000000000000000000000000000000000000000, 1` | `10000000000000000000000000000000000000001` | same |

The Lean audit also proves by `rfl` the universal connection
`∀ x0 x1, Proof.«_+Int_» x0 x1 = x0 + x1`; the ground tests are adversarial
evidence, not the basis of the universal correspondence.

Counterfactual checks confirm why this bridge review matters. A constant-zero
operator, left projection, and right projection each prove the generated
associativity statement by reflexivity, despite failing K addition. The
candidate is none of these: for example its values at `(-7,3)` and `(0,999999)`
exclude constant, projection, identity, and common hard-coded
implementations. Mutating the operational meaning to subtraction makes the
two sides at `(10,3,2)` evaluate to `5` and `9`, so that mutation is rejected.
The exact native-addition body and universal definitional equality close the
otherwise underconstrained operational bridge.

## Evidence

Raw commands and complete outputs are under `/audit-output/evidence/`.
The principal records are:

- `04-reconstructed-inventory.json.txt` and
  `06-stage3-bijection-and-hashes.txt`;
- `25-klean-check-generation-success.txt`,
  `27-stage4-obligation-and-target-exact.txt`, and
  `44-independent-hash-target-and-candidate-checks.txt`;
- `35-fresh-proof-copy.txt`, `36-proof-lake-clean.txt`, and
  `37-proof-lake-build.txt`;
- `40-proof-print-axioms.txt`, `41-axiom-reconciliation.txt`,
  `42-trusted-final-gate.txt`, and `50-core-axiom-origin.txt`;
- `43-operational-bridge-adversarial.txt`,
  `47-k-domains-int-add-definition.txt`, and
  `49-k-int-add-ground-results.txt`;
- the failed preflight/tool diagnosis and compatibility-shim construction are
  preserved in records `07` through `24`.

VERDICT: PASS
LEGITIMACY: LEGIT
