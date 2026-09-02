# Independent Stage 3–5 audit: HumanEval 131-digits

## Scope and result

The launcher and environment both select `CLASSIFICATION_AND_PROOF`; the
condition is `semantics` and the semantics mode is `SUPPLIED_SEMANTICS`. I
independently reconstructed and classified the frozen K verification rules,
audited the deterministic Stage 4 generation, and clean-built and validated the
Stage 5 Lean proof. I did not rely on an earlier PASS, review rationale, or
candidate comment as authority.

All required integrity, classification, target-identity, proof, trust, and
operational-bridge checks pass. The proof candidate is legitimate.

## Evidence handling and producer-source gate

The mounted candidate and provenance trees were treated as evidence. Trusted
code was limited to `/reference/tools` and the pinned toolchain inventory.

Before interpreting Stage 4, I hashed the exact generation-time producer
sources:

| File | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These equal the individual hashes in both `generator-manifest.json` and
`source-manifest.json`. Both manifests name immutable generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`,
and `/audit-input.json` binds the producer bundle to a path whose final
component is that image digest. Recomputing the bundle with the launcher's
canonical pipeline tree hash produced
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
exactly the audit-input hash. The producer gate therefore passes; there is no
infrastructure `AUDIT_ERROR`.

The other launcher-bound hashes also recomputed exactly:

| Artifact | Hash |
|---|---|
| Stage 1 pipeline tree | `dfadcf70102456ceed8a476f3c9e470237f95e3d86cab60d3279cdaf823417bc` |
| Stage 1 export tree | `9e18c83d672e90ac987a116cd94058ae3b513d4b9c27bc679eb550bd8dc3a686` |
| Stage 2 audit tree | `c0ecb83d41518ec24d572d9f3b1712f6f1fc6d5f94ba4ea19cbe299e936c69e8` |
| Stage 3 manifest file | `2a00407680a3395423482e655efbf8f90a6525107c72153df942265f88a8f003` |
| Stage 4 generation tree | `b8a817784a53c5dd88485640d256b63abea92f456f570af55a47a1ee9340da45` |
| Generated Lean export tree | `9da9dffdd2d83ac1c9de6b2b579cf49eddc2aec3136cb03ac804d935329698e7` |
| Stage 5 candidate tree | `01f15103abedcaa824601f32b7eba0abf65250c1c47518437f0a385912ea89b6` |

## Stage 3 inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` directly against
`/reference/k-proof`. The selected module is `DIGITS-VERIFICATION`, and its
local verification-file closure contains only that module. The canonical
inventory has eight rules and hash
`997f9d867d49fb42b1d83ee8bdd60f1713a245267682473af0e3d6032a48e174`.

For every rule, the trusted lexer independently reconstructed the exact source
span, normalized text hash, and `source_rule_id`:

| Span | `source_rule_id` | Attribute | Independent class |
|---|---|---|---|
| 11 | `rule-707d2fff65d29fc33df78fa7df36a27570c6ead38e034ac0561a47af26b8cadd` | none | `DEFINITION` |
| 13–19 | `rule-72752e93fc84beda2568dfffa077ef72955a8f0f706517d875412fca8af59242` | none | `DEFINITION` |
| 21–23 | `rule-5b347c8a08e5a3787eb910773a322c40a260bd764f177d0ba72804d83ff940b9` | none | `DEFINITION` |
| 25–27 | `rule-47bf10a3ae4840b8cea3e2bfa5c81034547e374f6a91f99094dc6e0291b4fcbd` | none | `DEFINITION` |
| 29–31 | `rule-108d879768555f310cc51819054b5d497269e3d4cf23cab9d938e93438b5bcc3` | none | `DEFINITION` |
| 37–46 | `rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2` | `simplification` | `DOMAIN_LEMMA` |
| 48–57 | `rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2` | `simplification` | `DOMAIN_LEMMA` |
| 59–69 | `rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd` | `simplification` | `DOMAIN_LEMMA` |

The Stage 3 manifest contains these eight identities exactly once and in this
exact order. There are no omitted, duplicated, extra, or reordered identities.
The manifest inventory hash, every recomputed identity, and all generated
source-rule copies agree.

### Independent classification judgment

The first five rules are genuine definitions:

- line 11 is the zero/base equation of the named summary
  `oddDigitProduct`;
- lines 13–19 are its guarded positive recurrence;
- lines 21–31 are the exhaustive false, first-odd-digit, and later-odd-digit
  equations of the named helper `oddDigitStep`.

They name and define a mathematical execution summary; they do not rewrite a
program invocation or skip K control/state. They are not ordinary operational
rules.

The last three rules assert equality facts about that summary. They were
present in the compiled Stage 1 verification module before the proof ran.
There is no earlier Stage 1 proof of these exact rules against a module that
omits them, followed by a later use. Thus none qualifies as
`PROVED_DERIVED_LEMMA`. They are not definitions because they do not define a
new summary symbol or an equation selected by the summary's arguments; they
assert the loop-step recurrence as proof facts. `DOMAIN_LEMMA` is the correct
classification, and it is also the only permitted non-definition class for
these `simplification` rules.

The three domain lemmas are relevant and true. Let

`d = ((N %Int 10 +Int 10) %Int 10)` and
`q = (N -Int d) /Int 10`.

For `N > 0`, the supplied `pyMod` rule makes `d = pyMod(N,10)`, and the five
definition equations give exactly:

1. if `pyMod(N,2) ≠ 1`, `oddDigitProduct(q,A) =
   oddDigitProduct(N,A)`;
2. if `pyMod(N,2) = 1`, `oddDigitProduct(q,d) =
   oddDigitProduct(N,0)`;
3. if additionally `A ≠ 0`, `oddDigitProduct(q,A*d) =
   oddDigitProduct(N,A)`.

These are precisely the non-odd, first-odd, and later-odd branches of the
source loop and its postcondition summary. No true domain lemma was omitted or
misclassified.

## Stage 4 deterministic generation

I reran:

```sh
PYTHONPATH=/reference python3 -c \
  'from tools.klean_preflight import check_generation; ...'
```

using exactly `/reference/k-proof`,
`/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the pinned lock. The audit sandbox initially
prevented Lean from resolving its executable because its PID namespace and
mounted `/proc` disagree. A narrow local `LD_PRELOAD` shim changed only
`readlink("/proc/<pid>/exe")` to `readlink("/proc/self/exe")`. With that
namespace correction, the trusted preflight returned `PASS`. Its returned JSON
is exactly equal to the recorded `preflight.json` and the
`resolution.stage4_preflight` object in `/audit-input.json`, including the
clean/build output hashes.

The rerun established:

- frozen input hash:
  `9e18c83d672e90ac987a116cd94058ae3b513d4b9c27bc679eb550bd8dc3a686`;
- Stage 3 manifest hash:
  `2a00407680a3395423482e655efbf8f90a6525107c72153df942265f88a8f003`;
- generated tree hash:
  `9da9dffdd2d83ac1c9de6b2b579cf49eddc2aec3136cb03ac804d935329698e7`;
- three obligations, zero designated sorries, and 54 generated trust
  declarations;
- successful fresh `lake clean` and `lake build`.

An additional independent checker performed 34 cross-manifest checks. The
three obligation IDs are a unique ordered bijection with the three independently
classified domain rules. Each obligation retains the exact source span,
normalized hash, inventory hash, discovery hash, and Lean-conjunct hash:

| Rule | Lean conjunct SHA-256 |
|---|---|
| `rule-4d5167…` | `55e695a1cc85d159ce82810d98cfddf476bd0f7444736d8c07476f9af945281c` |
| `rule-3978fc…` | `5aa617a72737794207c02f39ac8abc03186678d83dcb00a182d93a2e795128ff` |
| `rule-373920…` | `b02cd911e325a3e1939fdd5ae1a959a90c2409eac5821ec23b0515db7054320e` |

The generated guards and equality sides exactly preserve the frozen K rules.
The guards are satisfiable (witnesses `N=14,A=7`, `N=135,A=0`, and
`N=135,A=2` were exercised), and none of the conjuncts is `True`, false-guarded,
duplicated, irrelevant, or weakened.

### Fixed target identity

The only target is
`Klean131Digits.Lemmas.targetStatement` in
`Klean131Digits/Lemmas.lean`. It is exactly the conjunction of the three mapped
obligations with the eleven recorded parameters.

| Target property | Hash |
|---|---|
| Definition | `b3fc24329d96c19e4e635c5b04f2d1b0736e7b31d6ade3d65ad87da8c126a8b1` |
| Applied statement | `fab279c6806102ae4b4037972d1edd523c16da2a86663c123b7ac1076ce1ec00` |

The extracted target object is identical in the generator manifest, recorded
preflight, rerun preflight, and audit input. The generated target file itself
has SHA-256
`0988ed832d56a46352991c16915b7dc1d19d4cdf49a7d8e178c3b40a519f6f50`.

## Stage 5 clean build, theorem identity, and trust

I made a fresh project at
`/tmp/audit-work/131-digits-proof-audit`, copied the candidate into it, and
copied the immutable generated project contents into `Base/`. The candidate
`Proof.lean` copied byte-for-byte with SHA-256
`17f5a59b81624dee687534fd0b7831259ffac3f3004d98a8c71da23fa45af9fe`.
The fresh `Base` export tree remained
`9da9dffdd2d83ac1c9de6b2b579cf49eddc2aec3136cb03ac804d935329698e7`
after the build, and its target file remained byte-identical to the reference.

Both required commands succeeded:

- `lake clean`: exit 0, no output;
- `lake build`: exit 0, `Build completed successfully.`

The only build diagnostics are three unused-`h` linter warnings in the
immutable generated target. The trusted final mechanical gate independently
repeated the copy, clean build, exact-binding check, exact theorem-statement
check, and axiom check and returned `PASS`.

The candidate contains exactly one definition for every target binding and
exactly one `theorem final`. It contains no `sorry`, `admit`, `unsafe`,
`axiom`, or `opaque`; the trusted declaration scanner returns an empty list.
It imports rather than redefines the generated namespace, so it neither changes
nor shadows `Klean131Digits.Lemmas.targetStatement`.

`Proof.final` has exactly the manifest's applied target statement. The direct
Lean output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. `trust-inventory.json` records zero designated and zero
other sorries. Its 54-entry allowlist accounts for generated executable
boundary declarations; none of those declarations occurs in the actual axiom
set of `Proof.final`. The trusted final gate explicitly permits the three Lean
core logical axioms `propext`, `Classical.choice`, and `Quot.sound`; every
reported dependency is therefore accounted for, with no unrecorded proof trust
escape.

## Operational-bridge audit of all target parameters

`SortInt` is generated as Lean `Int` and `SortBool` as Lean `Bool`. Each exact
candidate definition was compared with its bound KORE symbol, linked source
rules, K built-in hook, supplied `int.k`, the five summary definition rules,
and the source loop:

| Target parameter | Candidate definition | Frozen operational meaning | Judgment |
|---|---|---|---|
| `_-Int_` | `Int.sub` | `INT.sub` / `-Int` | Exact |
| `_andBool_` | `Bool.and` | `BOOL.and` truth table | Exact on evaluated Bool arguments |
| `_>Int_` | `decide (a > b)` | `INT.gt` / `>Int` | Exact |
| `_==Int_` | `decide (a = b)` | `INT.eq` / `==Int` | Exact |
| `_=/=Int_` | `decide (a ≠ b)` | `INT.ne` / `=/=Int` | Exact |
| `_%Int_` | `Int.tmod` | K `%Int`, hook `INT.tmod` | Exact |
| `_+Int_` | `Int.add` | `INT.add` / `+Int` | Exact |
| `_/Int_` | `Int.tdiv` | K `/Int`, hook `INT.tdiv` | Exact |
| `_*Int_` | `Int.mul` | `INT.mul` / `*Int` | Exact |
| `pyMod(_,_)…` | `(a.tmod b + b).tmod b` | exact frozen `pyMod` equation | Exact for every defined divisor |
| `oddDigitProduct(_,_)…` | `oddDigitProductCore N.toNat A` | zero base plus the guarded positive recurrence and three `oddDigitStep` branches | Exact on the full source/obligation domain |

K documents `%Int` and `/Int` as truncating remainder and division. Adversarial
sign witnesses distinguish the honest definitions from convenient Euclidean
ones:

- `(-13) %Int 10` / Lean `tmod` is `-3`, while `emod` is `7`;
- `(-13) /Int 10` / Lean `tdiv` is `-1`, while `ediv` is `-2`;
- frozen `pyMod(-13,10)` and the candidate both produce `7`.

The recursive summary is not a constant, identity, hard-coded table, or opaque
oracle. It inlines the frozen recurrence: calculate Python modulus for parity
and the last digit, calculate the decimal quotient with truncating division,
preserve the accumulator on the non-odd branch, replace the zero sentinel on
the first odd digit, and multiply on later odd digits. The termination proof
shows that the positive quotient is `n / 10` and strictly decreases.

The source contract and all linked rules require positive `N`, and recursion
reaches the explicit `N=0` base. The Lean total extension maps negative `N`
through `Int.toNat` to the base behavior; no frozen rule, generated obligation,
source input, or recursive call assigns operational meaning to negative `N`.
Similarly, K division/remainder by zero is undefined, while every linked use has
the fixed nonzero divisor 2 or 10. These totalizations are outside the theorem's
active domain and do not create a convenient proof path within it.

### Adversarial, differential, and counterfactual checks

Lean evaluation exercised the base and every recurrence branch:

- `oddDigitProductCore 0 11 = 11`;
- `oddDigitProductCore 1 0 = 1`;
- `oddDigitProductCore 24680 0 = 0`;
- `oddDigitProductCore 135 0 = 15`;
- `oddDigitProductCore 10305 0 = 15`;
- `oddDigitProductCore 123456789 0 = 945`;
- `oddDigitProductCore 123 2 = 6`.

An independently written Lean source-loop oracle, using only Nat decimal
division/remainder and the source accumulator algorithm, agreed with the
candidate for every input from 0 through 4,999 and for larger adversarial
values including `90909`, `987654321`, and `999999999`. The last value
correctly produced `387420489`.

Counterfactual tests were deliberately discriminating:

- a constant summary can satisfy the bare recurrence equations, confirming
  why the operational bridge cannot be inferred from the Lean theorem alone;
  it disagrees with the source at `N=135`;
- an identity summary also disagrees at `N=135`;
- Euclidean remainder/division disagree with the K hooks on negative witnesses;
- direct truncating remainder disagrees with frozen Python `pyMod` on
  `(-13,10)`;
- a source-body mutation that multiplies even digits disagrees at `N=2468`.

The actual candidate avoids all of these counterexamples and implements the
frozen operational meaning. The fact that a constant model can satisfy the
equations does not make a conjunct vacuous: all three antecedents have concrete
satisfying witnesses and their equations are the exact requested K domain
lemmas. It does show why the separately required operational-bridge audit is
essential; that audit passes for this candidate.

Finally, I compiled the supplied semantics independently with the LLVM backend.
A hand-written MPY harness containing the exact source body and 13 boundary and
representative assertions ran with exit 0. Mutating the expected result of
`digits(1)` from 1 to 0 caused `krun` to exit 1, confirming that the operational
test is result-sensitive.

## Evidence index

Raw commands are indexed in `evidence/COMMANDS.md`. Principal result files are:

- `evidence/inventory-reconstruction.json`
- `evidence/discovery-structural-validation.json`
- `evidence/preflight-rerun.json`
- `evidence/independent-manifest-check.json`
- `evidence/final-mechanical-gate.json`
- `evidence/lake-build.log`
- `evidence/print-axioms.log`
- `evidence/operational-bridge-lean.log`
- `evidence/operational-differential-lean.log`
- `evidence/k-adversarial-krun.log`
- `evidence/k-false-assert-krun.log`

VERDICT: PASS
LEGITIMACY: LEGIT
