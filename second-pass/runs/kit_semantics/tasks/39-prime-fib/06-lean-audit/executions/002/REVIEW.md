# Independent Stage 3–5 audit: `39-prime-fib`

The Stage 3 classification is complete and mathematically appropriate, and
the deterministic Stage 4 generation is provenance-clean, bijective, and
target-preserving. The Stage 5 project also clean-builds and proves the exact
generated target without an unrecorded axiom. It nevertheless fails the
required operational-bridge audit: the candidate's exact total Lean definition
of `primeFibSearch` violates one of the frozen definitional recurrence rules on
that rule's complete guard. This is the decisive failure.

## Audit scope and infrastructure

`/audit-input.json` records `CLASSIFICATION_AND_PROOF`, problem
`39-prime-fib`, condition `kit-semantics`, and
`SUPPLIED_SEMANTICS`. The trusted audit-input verifier recomputed resolved
input digest
`783eb5a621ad2d6c251160a45bf215fda02b2b3761524b33648666be40b25133`;
see [12_audit_input_binding.log](/audit-output/evidence/12_audit_input_binding.log).

Before evaluating Stage 4, I hashed the two mounted producer sources:

- `klean_export.py`:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`;
- `klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.

They exactly match `source-manifest.json` and the exporter/Klean hashes in
`generator-manifest.json`. The producer tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching `/audit-input.json`. The immutable image identity is consistently
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in the source manifest, generator provenance, and the image-derived producer
path in the audit input. Thus there is no producer-provenance `AUDIT_ERROR`.

The recorded Stage 1, selected Stage 2, Stage 4, candidate, Stage 1 export,
and generated-project tree hashes all recomputed exactly. All 771 Stage 1
per-file source hashes also match. Full results and the canonical inventory are
in [01_integrity_inventory.log](/audit-output/evidence/01_integrity_inventory.log).

The audit container exposes `/proc` from a different PID namespace, while Lean
4.22's `IO.appPath` reads `/proc/<namespace-pid>/exe`. The first two preserved
preflight attempts consequently failed before source compilation. The
successful attempts interposed `readlink` only to map that missing path to
`/proc/self/exe`; the source is
[lean_app_path_fix.c](/audit-output/evidence/lean_app_path_fix.c). This did not
modify Lean, Lake, generated source, candidate source, or build output. Exact
commands are collected in [COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## Inventory reconstruction and Stage 3 classification

Using the trusted `tools.k_rule_inventory.inventory_verification`, I
independently reconstructed the local verification-module closure as
`[VERIFICATION-SYNTAX, VERIFICATION]`. The frozen `verification.k` hash is
`1153c81e4368133084f64b522d4d019de25055dfa9acbaac2915890ae15d5453`.
There are exactly 12 rules, and the canonical inventory hash is
`d277ae12725aaa26772d37930e9cbe9a7b2e0699b8289d37fe7be0befeac524a`.

For each entry I recomputed its physical span, whitespace-normalized source,
SHA-256, and `source_rule_id = "rule-" + normalized_sha256`. The ordered IDs
in `/reference/lemma-discovery.json` are exactly equal to the ordered canonical
IDs; there are no omissions, extras, duplicates, reordered identities, or hash
changes. The trusted Stage 3 boundary validator also passes. The full normalized
source of every rule is in
[01_integrity_inventory.log](/audit-output/evidence/01_integrity_inventory.log).

My independent rule-by-rule classification is:

1. Lines 25–40,
   `rule-b140a59a2c7ac129f59c3ea9479e74b1afb69f96d459aeab91625b0a325f62e1`:
   **DEFINITION**. Exact macro body for the source inner `While`.
2. Lines 42–57,
   `rule-ae138cf631c852c6689037278cdef752c08dc868bb22082ac057c01d37dfb043`:
   **DEFINITION**. Exact named proof term for the corresponding internal
   `#while` head.
3. Lines 59–75,
   `rule-2eeee8218fa0f1ab3abdeb706b12f9b9c5caa3732a3901edbab9195bf216b5c7`:
   **DEFINITION**. Exact macro body for the outer Fibonacci-search `While`.
4. Lines 77–93,
   `rule-557c59673423be46fad688ff932860ebe8ffbf6a93b9b76798d9917cbf431255`:
   **DEFINITION**. Exact named proof term for the outer internal `#while` head.
5. Lines 95–104,
   `rule-42b12587f50eda8ad9a9526c55e96494f2ebf4b50034495a0c8bc4fd6fd8abc4`:
   **DEFINITION**. Exact named initialization, outer loop, and return body.
6. Lines 108–110,
   `rule-ed39697ae845fca5c3929cc19f202f89ba72c9d726de3189a7db0165f7d66247`:
   **DEFINITION**. `primeScan` exit/base equation.
7. Lines 111–115,
   `rule-3b0d654a52c07f36a2c8e03ab9a42adb2fbab342d609dc7963241a2fd2dd5c7f`:
   **DEFINITION**. `primeScan` divisor equation.
8. Lines 116–120,
   `rule-d1b2c3dd591d8a0aa4abb1a73970f1bbc7d8c61befd06b9e7e07e0ec88ca15a3`:
   **DEFINITION**. Backward-folding `primeScan` recurrence.
9. Lines 123–125,
   `rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2`:
   **DOMAIN_LEMMA**. False-flag absorption is a mathematical consequence of
   the scan, not a defining branch or ordinary execution rule. Stage 1 never
   first proves this exact rule in a module omitting it. It is relevant because
   the source inner loop can clear but never restore `is_prime`.
10. Lines 129–131,
    `rule-7add6c868057fde760e298599f3f04aca6b58a8f251dc5a65f962e218851c151`:
    **DEFINITION**. Reached-count base equation for `primeFibSearch`.
11. Lines 132–139,
    `rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f`:
    **DOMAIN_LEMMA**. The one-step exit-boundary equality is additional
    mathematics, not separately proved before use. It is directly relevant to
    the outer loop's final prime-bit update and return.
12. Lines 140–150,
    `rule-88229ce3ed2cdd6dfe0c0cedf0411c4b335071c8bc4cd37ed184c0b6a9feaa02`:
    **DEFINITION**. Backward-folding one-step `primeFibSearch` recurrence.

Thus the protected classification of ten definitions and two domain lemmas is
correct. There are no local `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA`
entries. Every rule carrying `simplification` is classified as either
`DEFINITION` or `DOMAIN_LEMMA`, as required.

The two domain lemmas are true and non-vacuous. False absorption follows because
the trial-division body never writes `true`. For the boundary lemma, the guard
has `C < N` and not `(C + bit < N)`, where `bit` is 0 or 1; integer arithmetic
therefore forces `bit = 1` and `C + 1 = N`, after which one exact outer step and
the reached-count base return `B`. Concrete guard witnesses are `D=2,A=4` for
the first and `N=1,C=0,A=0,B=2` for the second.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected discovery
manifest, selected generation, and pinned toolchain lock. The successful result
is [02_generation_preflight_success.log](/audit-output/evidence/02_generation_preflight_success.log):
status `PASS`, two obligations, zero designated sorries, generated tree hash
`3cfac9ef368319eb3c21306428cb0c26a03c235396ac4c5f6b4c9fb52e4654eb`,
and successful clean/build diagnostics.

The independently reconstructed domain-rule order is exactly:

1. `rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2`;
2. `rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f`.

The obligation map contains exactly those two IDs, once each, in the same
order, with exact source spans, normalized hashes, inventory hash, discovery
hash, conjunct text, and conjunct hash. Its hash is
`869bdee3d8a807bdc6f6cca51a54da2eab7ae53e4432f8e8e869ccadac373623`.
The generated proposition is exactly their conjunction; neither guard is
unsatisfiable under the honest primitive bindings. See
[03_stage4_bijection.log](/audit-output/evidence/03_stage4_bijection.log).

The fixed target is `Klean39PrimeFib.Lemmas.targetStatement` in
`Klean39PrimeFib/Lemmas.lean`, with definition hash
`2d48f8c99a053921560123488abafe8016e08223dec09b883b2b36c13406e1c9`
and application-statement hash
`d1ac059479a94936bc9c9d49c554ae2ded44a051b8c0895dc7b6a0fc54caa49c`.
The target object is byte-for-byte consistent among the generated source,
generator manifest, preflight result, and `/audit-input.json`. Stage 4 is not
`KLEAN_NO_OBLIGATIONS`; the independently confirmed domain set has size two.

## Stage 5 mechanical proof and trust accounting

I created `/tmp/audit-work/39-prime-fib-independent-audit` fresh, copied the
generated project verbatim as `Base`, and copied only the candidate source and
Lake metadata—not its prior `.lake` artifacts. The copied Base tree retained
the exact generated hash above. I then ran both required commands:

- `lake clean`: exit 0, complete output in
  [04_lake_clean.log](/audit-output/evidence/04_lake_clean.log);
- `lake build`: exit 0, `Build completed successfully`, complete output in
  [05_lake_build.log](/audit-output/evidence/05_lake_build.log).

The candidate tree hash matches the audit input. The trusted candidate gate
finds exactly one definition for each of the seven target parameters and one
exact `Proof.final`; candidate-authored files contain no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`. They neither define nor shadow
`targetStatement`. The fresh Base target remains exact. See
[11_candidate_static.log](/audit-output/evidence/11_candidate_static.log).

`#print Proof.final` confirms that it has exactly the fixed target applied to
the seven candidate definitions; see
[07_proof_identity.log](/audit-output/evidence/07_proof_identity.log). The
required exact axiom command produced:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The complete output is [06_print_axioms.log](/audit-output/evidence/06_print_axioms.log).
Those are precisely the three Lean core axioms explicitly admitted by the
trusted mechanical gate in addition to the generated trust inventory. None of
the 43 generated allowlisted collection/summary axioms is a dependency of
`Proof.final`; there is no `sorryAx` and no other dependency. The independent
trusted Stage 5 mechanical gate returns `PASS` and the same three-item set in
[08_stage5_mechanical_gate.log](/audit-output/evidence/08_stage5_mechanical_gate.log).

These facts establish mechanical integrity only. They do not cure the bridge
failure below.

## Operational-bridge audit

The first five primitive bindings are faithful: Boolean conjunction and
negation use Lean `Bool`; integer comparison and addition use Lean `Int`, which
are exactly the generated `SortBool` and `SortInt` representations. Their
printed definitions are in
[07_proof_identity.log](/audit-output/evidence/07_proof_identity.log).

The candidate `primeScan` binding runs the source trial-division recurrence. On
the relevant domain, divisors start at or above two, its fuel exceeds the
number of possible divisor steps, positive-divisor Lean remainder agrees with
the supplied `pyMod`, and a false input flag returns false. Adversarial negative,
small, composite, prime, false-flag, and suffix-start cases match an independent
oracle exactly; see [09_adversarial_success.log](/audit-output/evidence/09_adversarial_success.log)
and [09_operational_oracle.log](/audit-output/evidence/09_operational_oracle.log).

The generated target alone is not enough to validate `primeFibSearch`. A
counterfactual hard-coded definition `fun _target _count _a b => b` proves the
entire target without axioms; see
[10_counterfactual.log](/audit-output/evidence/10_counterfactual.log). Therefore
the actual candidate definition must independently preserve the frozen search
meaning and every applicable defining rule.

It does not. The frozen recurrence at lines 140–150 requires, for its complete
guard:

```text
primeFibSearch(N, C + bit(B), B, A + B)
  = primeFibSearch(N, C, A, B)
```

Instantiate `N=1`, `C=0`, `A=4`, `B=4`. The guard is satisfiable and true:
`1>=1`, `0<1`, `4>=0`, and `4>=1`. The frozen `primeScan(4,2,true)` divisor
equation yields false, so `bit(B)=0`. The frozen definition therefore demands:

```text
primeFibSearch(1, 0, 4, 8) = primeFibSearch(1, 0, 4, 4).
```

The candidate instead gives 8 on the left and 4 on the right. Starting from
either state, every subsequent pair remains a positive multiple of four, every
prime bit remains zero, and count never reaches one. The candidate's
`completeFibonacciSearch` then takes its no-reach branch and returns the
*current input state's* `a`; that state-dependent convenience makes the two
successive recurrence states unequal.

This counterexample is machine-checked in
[Probe.lean](/audit-output/evidence/Probe.lean), with exact output in
[13_recurrence_counterexample.log](/audit-output/evidence/13_recurrence_counterexample.log).
The probe was made by copying `Proof.lean`, changing only its namespace, and
adding the counterexample lemmas. Candidate lines 4–104, containing every
parameter definition and helper, are byte-identical in the probe, with slice
hash `20186d8b8a7a5b7c03f46537ba05cd9e3074f4a32b5c126c47fba2fec70d4980`;
see [14_probe_identity.log](/audit-output/evidence/14_probe_identity.log).

Although the corresponding source loop diverges on this artificial state, the
frozen `primeFibSearch` rule is an explicit universal definition whose guard
includes this state. The candidate was required to implement that frozen K
symbol and compare against the complete frozen rule domain, not merely choose
different convenient values for different divergent states. A fixed
totalization could preserve the recurrence; this state-dependent one does not.
This is the operational-bridge failure mandated by the audit instructions, so
the otherwise clean Lean theorem is not a legitimate proof of the fixed K
obligations under honest parameter meanings.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
