# Independent audit: `39-prime-fib`

Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`  
Audit mode: `CLASSIFICATION_AND_PROOF`

## Result

The Stage 3 classification is complete and correct, and the deterministic
Stage 4 generation is structurally and mathematically faithful to the two
true domain lemmas. The Stage 5 project also passes the mechanical checks:
it builds from a fresh immutable `Base`, proves exactly the fixed target, has
no forbidden candidate declarations or proof holes, and uses only the
standard Lean axioms `propext`, `Classical.choice`, and `Quot.sound`.

The proof is nevertheless not legitimate. The candidate definition of the
`primeFibSearch` KORE symbol violates the frozen `primeFibSearch` recurrence
on a concrete state satisfying that recurrence's guard. Its no-reach branch
is a state-dependent convenient totalization, not an implementation of the
frozen summary equations. This is an operational-bridge failure even though
the generated boundary lemma never exercises that branch.

## Frozen inputs and producer identity

`AUDIT_MODE` and `/audit-input.json` both record
`CLASSIFICATION_AND_PROOF`. The audit-input copy mounted at
`/audit-output/audit-input.json` is byte-identical to `/audit-input.json`.
The trusted `pipeline_contract.sha256_tree` implementation reproduced every
recorded mounted tree hash:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 K workspace | `a0bd2a6606735c8bd4df4a4e0f4c9736b4fc09e4f69d2bb267e33eb9408672c6` |
| Stage 2 K audit | `b302fd3fd16ae78792560bb88d38f5207dea562f49b384ecbeb0ea469c8485b8` |
| Stage 4 generation | `d13cdff330258bbcb89d40e5ff601ea92e0aa78e73057a1ead056cf004b56676` |
| Generation producer bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Stage 5 candidate | `29512dfc08a099c7a1afa8f327f5615497a5d943c66da8ef2c3372114894e9b5` |

All 771 Stage 1 per-file source hashes also match the audit input. The Klean
content-tree digest of Stage 1 is
`8de9f776d8d35168a3748992152f88289862525cd002b406840c0dd92381e1d9`,
and the generated-tree digest is
`3cfac9ef368319eb3c21306428cb0c26a03c235396ac4c5f6b4c9fb52e4654eb`;
both match their manifests and the audit input.

The required producer check passed before Stage 4 was judged:

| Producer | Observed and recorded SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

The source manifest and generator manifest both identify the immutable
generator image as
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
The basename of the producer-source path recorded in `/audit-input.json` is
the same image digest. There is no producer-source infrastructure error.

## Inventory reconstruction

I ran the trusted local rule-inventory code directly against
`/reference/k-proof`. It selected `VERIFICATION` from `prove.sh` and found the
local module closure, in source order, to be:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION`

It reconstructed 12 rules. The frozen `verification.k` hash is
`1153c81e4368133084f64b522d4d019de25055dfa9acbaac2915890ae15d5453`;
the canonical inventory hash is
`d277ae12725aaa26772d37930e9cbe9a7b2e0699b8289d37fe7be0befeac524a`.
The Stage 3 manifest has exactly the same 12 ordered IDs and the same
inventory hash. There are no omissions, extras, duplicate IDs, reordered
identities, changed spans, or changed normalized hashes.

| Lines | Normalized hash / source-rule identity | Independent class |
|---|---|---|
| 25–40 | `b140a59a2c7ac129f59c3ea9479e74b1afb69f96d459aeab91625b0a325f62e1` | `DEFINITION` |
| 42–57 | `ae138cf631c852c6689037278cdef752c08dc868bb22082ac057c01d37dfb043` | `DEFINITION` |
| 59–75 | `2eeee8218fa0f1ab3abdeb706b12f9b9c5caa3732a3901edbab9195bf216b5c7` | `DEFINITION` |
| 77–93 | `557c59673423be46fad688ff932860ebe8ffbf6a93b9b76798d9917cbf431255` | `DEFINITION` |
| 95–104 | `42b12587f50eda8ad9a9526c55e96494f2ebf4b50034495a0c8bc4fd6fd8abc4` | `DEFINITION` |
| 108–110 | `ed39697ae845fca5c3929cc19f202f89ba72c9d726de3189a7db0165f7d66247` | `DEFINITION` |
| 111–115 | `3b0d654a52c07f36a2c8e03ab9a42adb2fbab342d609dc7963241a2fd2dd5c7f` | `DEFINITION` |
| 116–120 | `d1b2c3dd591d8a0aa4abb1a73970f1bbc7d8c61befd06b9e7e07e0ec88ca15a3` | `DEFINITION` |
| 123–125 | `577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2` | `DOMAIN_LEMMA` |
| 129–131 | `7add6c868057fde760e298599f3f04aca6b58a8f251dc5a65f962e218851c151` | `DEFINITION` |
| 132–139 | `a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f` | `DOMAIN_LEMMA` |
| 140–150 | `88229ce3ed2cdd6dfe0c0cedf0411c4b335071c8bc4cd37ed184c0b6a9feaa02` | `DEFINITION` |

Each `source_rule_id` is `rule-` followed by the displayed full normalized
hash. The first five rules expand named macro/proof terms. Rules 6–8 define
the base, divisor, and non-divisor cases of `primeScan`. Rule 10 is the
reached-target base equation of `primeFibSearch`, and rule 12 is its
state-transition recurrence. Those are genuine definitions rather than
ordinary execution rules or unproved domain facts.

The two domain classifications are also correct:

- `rule-5779…` is false-flag absorption for `primeScan`. The operational
  inner loop can preserve false or assign false but never restore true, so
  the lemma is true and relevant to the inner-loop invariant. It is an
  additional invariant, not a core recurrence clause.
- `rule-a100…` is the one-step outer-loop exit fact. The increment is exactly
  zero or one; `C < N` together with `not (C + bit < N)` means the next
  iteration reaches the target and moves `a` to `B`. It directly supports
  the program result.

`prove.sh` proves loop reachability claims in stages, but it never first
proves either exact inventory rule in a module from which that rule is
absent. Therefore neither is a `PROVED_DERIVED_LEMMA`. There are no
`OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. All seven
`[simplification]` rules are classified as either `DEFINITION` or
`DOMAIN_LEMMA`. My independent ordered classification exactly matches Stage
3.

## Deterministic Stage 4 generation

With `PYTHONPATH=/reference`, I called
`tools.klean_preflight.check_generation` on the frozen Stage 1 workspace,
Stage 3 manifest, Stage 4 generation, and trusted toolchain lock. After the
Lean PID-namespace compatibility described below, it returned `PASS`,
reported two obligations, rebuilt the generated project successfully, and
returned the exact recorded target.

An independent standard-library-only check reproduced:

- obligation-map hash:
  `869bdee3d8a807bdc6f6cca51a54da2eab7ae53e4432f8e8e869ccadac373623`;
- generated-tree hash:
  `3cfac9ef368319eb3c21306428cb0c26a03c235396ac4c5f6b4c9fb52e4654eb`;
- trust-inventory hash:
  `60d166080ab46da40648a255d23711c2430f5765f4b7b4f22dba31e0f7d8f43a`;
- both obligation conjunct hashes;
- all seven KORE/name/type/source-rule binding hashes; and
- the exact ordered bijection between the two independently classified
  domain rules and the two generated obligations.

The obligations are exact translations:

1. For `rule-5779…`, for every `D` and `A`, if `D >= 2`, then
   `primeScan A D false = false`.
2. For `rule-a100…`, for every `B, A, C, N`, the exact nested conjunction of
   `N >= 1`, `C < N`, `not (C + primeBit(B) < N)`, and `B >= 1` implies
   `primeFibSearch N C A B = B`.

Neither conclusion is `True`, an omitted equation, or a changed target.
There are no duplicated obligations and no missing domain rule. The true
domain set is nonempty, so this is correctly an ordinary two-obligation
generation, not `KLEAN_NO_OBLIGATIONS`.

The generated project contains one and only one `targetStatement`. Its
definition is the exact conjunction reconstructed from `obligation-map.json`.
The following values agree in the generated source, generator manifest,
preflight record, and `/audit-input.json`:

| Target field | Value |
|---|---|
| Declaration | `Klean39PrimeFib.Lemmas.targetStatement` |
| Definition SHA-256 | `2d48f8c99a053921560123488abafe8016e08223dec09b883b2b36c13406e1c9` |
| Applied statement SHA-256 | `d1ac059479a94936bc9c9d49c554ae2ded44a051b8c0895dc7b6a0fc54caa49c` |

## Lean environment note

The first preflight attempt reached `lake clean` but failed because this
container reports a process ID that is absent from its mounted `/proc`, while
Lean 4.22 obtains its executable path through `/proc/<pid>/exe`. This is an
audit-container issue, not candidate evidence. I recorded the failure and
diagnosis, then compiled a 35-line compatibility shim that redirects only a
`readlink("/proc/<digits>/exe", …)` request to `/proc/self/exe`. Its source
hash is
`075747322b1759df5180a1aba60ba96b24587d2a2acd80460e042ea61fecd666`.
With that narrow shim, the pinned binary reports Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the trusted preflight and
all subsequent fresh builds run normally. The shim does not alter Lean
source, proof terms, generated files, or command output.

## Stage 5 mechanical proof audit

I created
`/tmp/audit-work/39-prime-fib-proof-audit-001`, copied only the candidate
top-level proof project into it, and copied
`/reference/klean-generation/generated` into that project as `Base`.
`diff -ruN` confirmed that the fresh `Base` was exact before building.

The required commands both succeeded:

```text
lake clean
exit 0

lake build
exit 0
Build completed successfully.
```

The candidate `Proof.lean` copy has SHA-256
`9b9b0971a4f69da9c009a1e16bf281061d8e12c938f3f5523d65897fc7388d79`.
It contains exactly one definition for every target parameter. It contains no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`, and introduces no trust
declaration. The only `targetStatement` declaration in the fresh project is
the immutable generated one. Its file remained byte-identical to the Stage 4
source after the build.

`#check` and `#print Proof.final` show that `Proof.final` has exactly this
type:

```text
Klean39PrimeFib.Lemmas.targetStatement
  Proof._andBool_ Proof.«_>=Int_» Proof.«_<Int_» Proof.«_+Int_»
  Proof.notBool_
  Proof.«primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
  Proof.«primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
```

It is not a duplicate or weakened theorem. Running Lean with the required
command produced this exact output:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. The three names are the standard Lean trust base
accepted by the trusted final-gate policy. None of the 43 generated,
recorded trust declarations is used by `Proof.final`; all 43 generated
declarations do exactly match `trust-inventory.json`. The inventory records
zero designated sorries, zero other sorries, and no automatic
axiomatization. The trusted Stage 5 mechanical checker independently returned
`PASS` with the same target and axiom set.

## Operational-bridge audit

The simple bindings are faithful:

| Target parameter | Candidate definition | Judgment |
|---|---|---|
| `_andBool_` | Boolean `&&` | Matches K `andBool` |
| `«_>=Int_»` | `decide (x ≥ y)` | Matches unbounded K integer comparison |
| `«_<Int_»` | `decide (x < y)` | Matches unbounded K integer comparison |
| `«_+Int_»` | Lean `Int` addition | Matches K `+Int` |
| `notBool_` | Boolean negation | Matches K `notBool` |
| `primeScan` | Fuel-bounded divisor scan | Faithful on the frozen `D >= 2` domain |
| `primeFibSearch` | Reachability search plus no-reach totalization | **Fails the frozen recurrence** |

`SortBool` and `SortInt` are generated abbreviations for Lean `Bool` and
`Int`. The `primeScan` implementation checks exactly the source loop's
`d*d > a`, positive-divisor remainder, false absorption, and `d+1`
transition. K's `pyMod` and Lean's remainder agree for the positive divisors
in the rule domain. For nonnegative `a`, `a.toNat + 1` fuel exceeds the
number of possible `d >= 2` iterations; for negative `a`, the square-bound
base case is immediate. Stopping as soon as the flag becomes false preserves
the only represented observation because the source loop cannot restore it.
There were zero mismatches over 51,058 adversarial scan cases, including
negative values, primes, composites, perfect squares, false initial flags,
and divisors already beyond the square bound.

On terminating searches, `advance` also matches the source assignment order:
it tests old `b`, increments the count by zero or one, then maps
`(a,b)` to `(b,a+b)`. There were zero mismatches over 2,216 terminating
search states, zero mismatches under different valid existential witnesses,
and the observed entry results were exactly `2, 3, 5, 13, 89`.

Those successes do not cover the candidate's no-reach branch. The frozen
defining recurrence, `rule-88229…`, is:

```text
primeFibSearch(N, C + primeBit(B), B, A + B)
  = primeFibSearch(N, C, A, B)
```

under `N >= 1`, `C < N`, `A >= 0`, and `B >= 1`. It is a Stage 3
`DEFINITION`, and its guard does not assume eventual termination.

The candidate's `semanticSearch` returns its input state's `a` when no state
ever reaches the target. The public function advances once before invoking
that branch. Consider:

```text
N = 1, C = 0, A = 4, B = 4.
```

All recurrence guards hold. `primeBit(4) = 0`. Starting from `(4,4)`, every
later pair remains a pair of positive multiples of four, so each tested `b`
is composite, the count remains zero forever, and the no-reach existential
is false.

- The right side, `primeFibSearch(1,0,4,4)`, advances to `(a,b)=(4,8)`;
  its no-reach branch returns `4`.
- The recurrence's left side is
  `primeFibSearch(1,0,4,8)`. It advances to `(a,b)=(8,12)`; its no-reach
  branch returns `8`.

Thus the candidate interprets the frozen defining equation as `8 = 4`.
The evidence script records the states, the first 20 constant-zero counts,
the multiple-of-four invariant witnesses, and the unequal candidate values.
This is not merely an arbitrary value outside the frozen domain: it is inside
the explicit guard of a frozen `primeFibSearch` defining rule. A faithful
totalization could use one common value along a divergent transition class;
this state-dependent `initial.a` fallback does not.

As an additional sensitivity check, an audit-only Lean file instantiated the
same fixed target with `badAnd := false`, `badScan := false`, and
`badSearch := fun _ _ _ b => b`; Lean still proved the exact target because
the second guard became vacuous and the first equation became reflexive.
Separate examples and differential tests reject those definitions against
the operational semantics. This confirms why the clean target proof is
insufficient and why the actual bridge definitions must satisfy the frozen
rules.

## Evidence index

- `evidence/00-launcher-producer-and-tree-hashes.txt` and
  `01-recorded-tree-hash-recalculation.txt`: launcher, producer, tree, and
  per-source integrity.
- `02-inventory-reconstruction.txt`, `independent-classification.json`, and
  `16-independent-classification-check.txt`: complete inventory and
  classification comparison.
- `03-frozen-source-and-proof-structure.txt` and
  `04-operational-semantics-excerpts.txt`: numbered frozen source and
  operational semantics.
- `05-stage4-preflight-rerun.txt`: successful required trusted preflight.
- `05a-stage4-preflight-initial-env-failure.txt`,
  `06-lean-toolchain-diagnosis.txt`, and
  `07-lean-proc-compatibility-shim.txt`: complete environment diagnosis and
  narrow compatibility evidence.
- `08-independent-stage4-identity-check.txt`,
  `independent_stage4_check.py`, and
  `17-generated-obligation-and-target-sources.txt`: independent hashes,
  bijection, target reconstruction, and raw numbered Stage 4/candidate
  sources.
- `09-fresh-proof-build.txt`: exact fresh copy, `Base` comparison, clean, and
  build output.
- `10-proof-axioms-and-identity.txt`,
  `11-candidate-integrity-and-forbidden-scan.txt`,
  `12-trusted-stage5-mechanical-check.txt`, and
  `15-axiom-reconciliation.txt`: theorem identity, trust, and forbidden-token
  evidence.
- `13-lean-operational-and-counterfactual-tests.txt`,
  `14-operational-bridge-differential-tests.txt`, and
  `operational_bridge_tests.py`: operational examples, vacuity
  counterfactual, finite differential checks, and the decisive divergent
  recurrence witness.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
