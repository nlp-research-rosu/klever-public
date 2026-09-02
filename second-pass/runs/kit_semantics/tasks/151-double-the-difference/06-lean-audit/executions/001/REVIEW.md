# Independent audit: HumanEval 151 `double_the_difference`

## Result

I independently audited the frozen Stage 1 verification closure, the protected
Stage 3 classification, deterministic Stage 4 generation, and the Stage 5
Lean proof for:

- problem: `151-double-the-difference`
- condition: `kit-semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- audit mode: `CLASSIFICATION_AND_PROOF`

The audit mode in `/audit-input.json` agrees with `AUDIT_MODE`. I did not rely
on any prior verdict or classification. The reconstructed inventory, the
independent classifications, all producer and artifact hashes, the generated
obligations, the fixed target, the clean proof build, the proof's axiom
dependencies, and all 15 operational bridge definitions pass review.

One important negative test is that the abstract generated target can be
proved with deliberately degenerate constant parameters. That fact makes the
mechanical proof insufficient on its own, but it does not invalidate this
candidate: the actual candidate definitions were separately checked against
the supplied K semantics and are non-degenerate. They distinguish positive,
negative, even, odd, Int, Float, Bool, and non-Int cases and compute the mixed
source example correctly.

## Frozen-input and producer integrity

Before assessing Stage 4, I hashed the producer sources directly:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes agree with the producer source manifest and
`generator-manifest.json`. The producer-bundle tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
which agrees with `/audit-input.json`. The immutable generator image ID is
identically recorded in all three provenance locations as:

`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

The bundle contains exactly `klean.py`, `klean_export.py`, and
`source-manifest.json`; there is no missing or mismatched producer source.
The detailed comparison is in `evidence/03-producer-provenance.txt`.

I also independently checked the recorded trees for the Stage 1 workspace,
Stage 1 export, Stage 2 audit, Stage 3 discovery file, Stage 4 generation,
generated Lean project, producer source bundle, and Stage 5 candidate. Every
tree agrees with `/audit-input.json`. All 774 individually recorded Stage 1
paths are present with the recorded hashes; there are no path or content
mismatches. See `evidence/05-hash-and-target-integrity.txt`.

## Rule-inventory reconstruction

I used the trusted `/reference/tools/k_rule_inventory.py` implementation to
reconstruct the local verification-module closure rooted at the frozen
`verification.k`. The closure is:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION`

The imported MPY semantics is not part of the *local* verification-module
inventory. Reconstruction found 23 local rules. The frozen
`verification.k` hash is:

`22eaf262a318adda58bcaf4cfb73cd5aae26d5bf7ec95390d0f817df83f3566b`

For every rule, I recomputed the source span, normalized source, normalized
source hash, and `source_rule_id`. I then recomputed the canonical whole
inventory hash:

`7b6228289923d63c0b89687fc42470bbb802c30a6c0f491ffdaf55af87a0ef72`

That hash agrees with the protected Stage 3 file and the generator inputs.
The protected classification contains exactly the same 23 unique identities
in the same order. There are no omitted, extra, duplicated, reordered, or
changed rules. The full reconstructed canonical inventory is
`evidence/01-reconstructed-inventory.json`; the bijective comparison is
`evidence/02-inventory-bijection.txt`.

## Independent Stage 3 classification

My independent result is 15 `DEFINITION`, 8 `DOMAIN_LEMMA`, 0
`OPERATIONAL_RULE`, and 0 `PROVED_DERIVED_LEMMA`. It agrees entry-for-entry
with the protected Stage 3 classification:

| Frozen lines | Term or rule role | Classification | Reason |
|---|---|---|---|
| 25 | `numericVals(.ValSeq)` | `DEFINITION` | Base equation for the named domain summary |
| 26–27 | `numericVals(vCons(...))` | `DEFINITION` | Structural recurrence for that summary |
| 30 | `dtd(.ValSeq)` | `DEFINITION` | Base equation for the result summary |
| 31–32 | static-Int `dtd` | `DEFINITION` | Structural Int recurrence |
| 33 | static-Float `dtd` | `DEFINITION` | Structural Float recurrence |
| 34 | `dtd` `[owise]` | `DEFINITION` | Completes the summary on other heads |
| 35–38 | guarded dynamic-Int `dtd` | `DOMAIN_LEMMA` | Extra symbolic simplification derived from sort/project facts |
| 39–41 | guarded dynamic-Float `dtd` | `DOMAIN_LEMMA` | Extra symbolic simplification derived from the Float guard |
| 43–47 | `oddIntSquare` | `DEFINITION` | Defines the named postcondition summary |
| 51 | `lastNumber` base | `DEFINITION` | Base equation for a named proof summary |
| 52–53 | `lastNumber` recurrence | `DEFINITION` | Structural recurrence for that summary |
| 57 | `definedProjectInt` | `DEFINITION` | Defines the named projection guard |
| 58–60 | `#Ceil`/projection characterization | `DOMAIN_LEMMA` | Additional definedness equivalence |
| 61–63 | `projectIntTotal(V) => {V}:>Int` | `DEFINITION` | Guarded defining orientation of the named total projection |
| 64–66 | `{V}:>Int => projectIntTotal(V)` | `DEFINITION` | Reverse guarded orientation of the same alias |
| 67 | `projectIntTotal(I) => I` | `DEFINITION` | Int-domain defining equation |
| 68–70 | projection idempotence | `DOMAIN_LEMMA` | Additional simplification property |
| 71 | `isIntV(V) => isInt(V)` | `DOMAIN_LEMMA` | Relates a builtin observation to the K sort observation |
| 72–75 | guarded `applyCmp(">")` | `DOMAIN_LEMMA` | Source-relevant dispatch simplification |
| 76–79 | guarded `applyBin("%")` | `DOMAIN_LEMMA` | Source-relevant dispatch simplification |
| 80–83 | guarded `applyBin("*")` | `DOMAIN_LEMMA` | Source-relevant dispatch simplification |
| 85–95 | `dtdLoopBody` | `DEFINITION` | Exact compile-time macro for the nested source loop |
| 97–101 | `dtdBody` | `DEFINITION` | Exact compile-time macro for the source function body |

All rules marked `[simplification]` are either definitions or domain lemmas.
The ordinary execution rules live in the imported MPY semantics; none of
these 23 local verification helpers is an ordinary operational rule.

No rule qualifies as `PROVED_DERIVED_LEMMA`. Stage 1 does not first prove any
of these exact rules against a module that excludes it and then add it for a
later proof. In particular, the eight extra symbolic/definedness/dispatch
facts cannot be relabeled as definitions, operational rules, or previously
proved derived lemmas.

The eight domain lemmas are all relevant. They connect the `dtd` summary to
dynamic Int/Float values, justify the Int projection used by the summary, and
model the exact source operations `isinstance(..., int)`, `> 0`, `% 2`, and
`number * number`. No unrelated mathematical fact was admitted. The complete
entry-level judgment, including full `source_rule_id` values, is in
`evidence/06-independent-classification.tsv`.

## Deterministic Stage 4 generation

I reran the required trusted call:

`tools.klean_preflight.check_generation(/reference/k-proof, /reference/lemma-discovery.json, /reference/klean-generation)`

with `PYTHONPATH=/reference` and the pinned toolchain lock. It returned
`status: PASS`, rebuilt the generated project successfully after `lake clean`,
reported zero designated `sorry`s, and found exactly eight obligations. The
complete returned value is `evidence/04-preflight-return.json`.

The audit container's PID namespace required a narrow `readlink` compatibility
shim for Lean to resolve its executable through `/proc/<pid>/exe`. The shim
only maps that lookup to `/proc/self/exe`; it does not alter source, generated
artifacts, proof terms, or Lean's checking behavior. The exact command is
recorded in `evidence/00-command-ledger.md`.

The independent domain-set/obligation comparison is an ordered bijection:

| Frozen rule | Generated conjunct | Mathematical judgment |
|---|---|---|
| lines 35–38, dynamic Int `dtd` | guarded Int-head recurrence | Exact |
| lines 39–41, dynamic Float `dtd` | guarded Float-head recurrence | Exact |
| lines 58–60, projection `#Ceil` | projection `isSome` iff guard and `True` | Exact |
| lines 68–70, idempotence | total projection after Int reinjection | Exact |
| line 71, `isIntV` | equality with the K Int-sort observation | Exact |
| lines 72–75, `applyCmp(">")` | guarded Int comparison dispatch | Exact |
| lines 76–79, `applyBin("%")` | guarded Int modulo dispatch | Exact |
| lines 80–83, `applyBin("*")` | guarded two-Int multiplication dispatch | Exact |

For each row, source span, normalized hash, `source_rule_id`, generated
conjunct hash, discovery entry, and obligation-map entry all agree. There is
one generated conjunct per domain lemma in inventory order, and no additional
conjunct.

The `∧ True` in the third conjunct is not a vacuous replacement for a
substantive condition. Its source is `#Ceil(@V)` where `@V` is already a
universally bound value of generated type `SortVal`; such a bound value is
defined. The other part of the equivalence preserves the nontrivial
projection-definedness test. The guards are also not vacuous: injected Int
and Float constructors directly witness satisfiable guarded domains.

The generated target is fixed as follows:

| Property | Verified value |
|---|---|
| Declaration | `Klean151DoubleTheDifference.Lemmas.targetStatement` |
| File | `Klean151DoubleTheDifference/Lemmas.lean` |
| Definition SHA-256 | `8692c46b758ca44e52c56b8ad68fb9d56804e805f53943138a1c490b7316d3eb` |
| Statement SHA-256 | `fb24fbe66177d0d1ac09b8bbd69f1df410d8b802a45dbdd6121e7974b82fea35` |
| Generated tree SHA-256 | `1938592f3efda3f6923d91a767e4b4e69bba33a4f8c1893767d0a1daf4cc32e4` |

I reconstructed the expected target from the obligation map and verified
byte-for-byte definition identity, statement identity, all 15 parameter
binding hashes, the obligation-map hash, and agreement among the generator
manifest, audit input, and preflight result. There are no weakened,
irrelevant, duplicated, omitted, or reordered obligations and no target
change. The generation is therefore correctly nonempty; this is not a
`KLEAN_NO_OBLIGATIONS` case.

## Stage 5 clean build and target identity

I created a fresh workspace at `/tmp/audit-work/lean-proof.GZJvxI`, copied the
candidate into it, and copied the immutable generated project into `Base`.
I then ran both required commands:

1. `lake clean` — exit 0
2. `lake build` — exit 0

The full outputs are `evidence/08-lake-clean.log` and
`evidence/09-lake-build.log`. The only messages are unused-variable warnings
from immutable generated files.

After the build, the fresh `Base` tree still has the exact generated-tree hash
shown above. The copied `Proof.lean` hash is
`309f089d254ea9fcf3df358b51303c974cdcc624b465c22b5510ba047037e85d`,
identical to the mounted candidate source.

The candidate:

- does not define or shadow `targetStatement`;
- has exactly one `Proof.final`;
- applies `targetStatement` to exactly the 15 manifest parameters in manifest
  order;
- has a whitespace-normalized final statement identical to the fixed manifest
  statement;
- contains no `sorry`, `admit`, or `unsafe`;
- declares no new `axiom` or `opaque`;
- proves the fixed generated theorem directly, rather than a duplicated,
  weakened, or vacuous variant.

The detailed scan is `evidence/12-candidate-integrity.txt`. The trusted Stage 5
mechanical gate independently returns `PASS` in
`evidence/17-stage5-mechanical-gate.json`.

## Proof axioms and trust accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

That exact output is saved in `evidence/10-print-axioms.log`. There is no
`sorryAx`.

`trust-inventory.json` records 42 generated Klean boundary axioms. None is a
dependency of `Proof.final`. The three reported dependencies are precisely
the standard Lean core dependencies admitted by the trusted final gate
(`propext`, `Classical.choice`, and `Quot.sound`) under the pinned Lean
v4.22.0 toolchain. Thus every reported dependency is accounted for, no
unrecorded generated trust escape is used, and the proof does not depend on
any of the generated hook axioms.

## Operational bridge audit

I located and inspected the exact candidate `def` for every manifest
parameter. I compared each one with its `kore_symbol`, full
`source_rule_ids`, corresponding frozen `verification.k` rules, the source
program, and the operational rules in the supplied MPY semantics. The detailed
15-row mapping is `evidence/18-operational-bridge.tsv`; the conclusions are:

- Boolean conjunction, integer `>`, `+`, and `*` are the corresponding Lean
  Boolean/integer operations.
- The source-relevant `applyCmp` branch dispatches `">"` on two injected Int
  values to integer greater-than.
- The source-relevant `applyBin` branches dispatch `"%"` to supplied
  Python-style modulo and `"*"` to integer multiplication, reinjecting the
  result as a value.
- `definedProjectInt`, `isInt`, `isFloat`, and the partial projection
  discriminate the exact generated K constructors.
- `isIntV` matches the frozen supplied-semantics rule: Int is true and Bool,
  Float, and other values are false.
- `projectIntTotal` is identity on the guarded Int domain and uses a fixed
  default only outside that domain, where the frozen equations and source
  execution do not observe the value.
- `pyMod` implements `((i₁ % i₂) + i₂) % i₂`, with a total fallback only for
  the zero divisor. The source divisor is the constant 2.
- `oddIntSquare` returns `i*i` exactly when `i > 0` and `pyMod(i,2) = 1`.
- `dtd` is the exact empty/Int/Float/other structural recurrence from the
  frozen verification module.

The generated value datatype does not contain the supplied semantics'
string-value constructor; unrelated string dispatch cannot be represented by
these target parameter types. Within the generated closure, every case bound
by the source rules and every source-reachable case is implemented
operationally, not chosen merely to solve the equations.

I ran adversarial checks in both the frozen K runtime and Lean. They cover:

- empty and representative positive/even/negative values;
- `-3 % 2 = 1`;
- `5 * -4 = -20`;
- Int, Float, and Bool sort discrimination;
- partial and total Int projections;
- the mixed sequence `[1.5, 5, 4.0, -3, 7]`, whose result is `74`.

The frozen K run exited 0 (`evidence/13-k-operational-checks.log`), and the
Lean definitions returned the expected distinguishing values
(`evidence/15-lean-operational-checks.log`).

Under ordinary Python, `bool` is a subclass of `int`; under this frozen
`SUPPLIED_SEMANTICS`, `isIntV(Bool)` is false. That is a semantics-model
boundary, not a candidate shortcut: the frozen K rule says exactly that only
the Int constructor satisfies `isIntV`, the Stage 1 `numericVals` domain is
Int/Float, and the candidate matches that supplied semantics. I tested the
Bool case explicitly.

Finally, I replaced all 15 target parameters with constant/false/default
counterfactuals and confirmed that the abstract target alone can still close
(`evidence/16-counterfactual-target.log`). This demonstrates why clean build
and target identity are only structural evidence. The actual candidate is
not constant, identity-only, hard-coded to the final answer, or vacuous: the
definition audit and adversarial results above establish the missing
operational bridge.

## Evidence index

- `evidence/00-command-ledger.md` — raw command ledger and result locations
- `evidence/01-reconstructed-inventory.json` — canonical trusted reconstruction
- `evidence/02-inventory-bijection.txt` — spans, IDs, hashes, order, uniqueness
- `evidence/03-producer-provenance.txt` — producer hashes and image identity
- `evidence/04-preflight-return.json` — required Stage 4 preflight return value
- `evidence/05-hash-and-target-integrity.txt` — trees, 774 sources, obligations,
  bindings, and target identity
- `evidence/06-independent-classification.tsv` — all 23 independent judgments
- `evidence/08-lake-clean.log` — successful fresh clean
- `evidence/09-lake-build.log` — successful fresh build
- `evidence/10-print-axioms.log` — exact `#print axioms Proof.final` output
- `evidence/11-candidate-source.txt` — complete line-numbered candidate source
- `evidence/12-candidate-integrity.txt` — target/shadow/forbidden-token checks
- `evidence/13-k-operational-checks.log` — frozen-runtime adversarial results
- `evidence/15-lean-operational-checks.log` — Lean bridge results
- `evidence/16-counterfactual-target.log` — degenerate-model negative test
- `evidence/17-stage5-mechanical-gate.json` — trusted final mechanical gate
- `evidence/18-operational-bridge.tsv` — all 15 parameter judgments

The discarded audit-harness setup diagnostics are preserved separately as
`evidence/07-lake-clean-setup-failure.log` and
`evidence/14-lean-operational-checks-harness-failure.log`; neither is a
candidate failure and neither contributes to the verdict.

VERDICT: PASS
LEGITIMACY: LEGIT
