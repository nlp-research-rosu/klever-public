# Independent Stage 3/4 Audit: HumanEval 115-max-fill

## Scope and audit mode

This audit independently examined the frozen Stage 1 K workspace, the protected
Stage 3 classification, and the selected deterministic Stage 4 generation for
condition `bare` and semantics mode `GENERATED_SEMANTICS`. I treated all mounted
candidate, provenance, log, comment, and earlier-review content as untrusted
evidence and did not rely on any earlier verdict.

Both `AUDIT_MODE` and the signed resolution in `/audit-input.json` are
`CLASSIFICATION_ONLY`. The signed resolution digest recomputes to
`a3daaf2b5c429b6ecace62fef468a6275603fe473fd59033b8533f97e2f3119b`.
The Stage 4 selection is `KLEAN_NO_OBLIGATIONS`; the audit input has a null
target, null Stage 5 result, null Lean workspace/invocation hashes, and
`/candidate` is absent. Stage 5 proof, axiom, and operational-bridge checks are
therefore not applicable.

## Producer identity and immutable provenance

I hashed the generation-time producer sources before making any Stage 4
judgment:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The producer bundle tree hash recomputes to
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`. The immutable generator image identity is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator manifest, and the audit input binds the
producer bundle path to the same image digest. There is no producer-source
infrastructure error.

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`; it contains six rules from `verification.k`. The reconstructed
verification hash is
`2f481182873f49f499b5285d7e22341937cd46f01938baf881c6b5141ca83278`,
and the canonical ordered inventory hash is
`7217a3a829699787866d2a6ba1990d5b95ddb742b434e782a79e118db3952ae0`.

The reconstructed entries, in source order, are:

| # | Span | Canonical identity | Attributes | Independent class |
|---:|---:|---|---|---|
| 1 | 11–11 | `rule-6ca28ceef2b848336d992ba2b268dc7c328f91eb4ed13f0068d5df2beef1d338` | none | `DEFINITION` |
| 2 | 12–12 | `rule-98dd266f5d08677ee67ace7455996a9ff6126e987b4677512995573403be6538` | none | `DEFINITION` |
| 3 | 15–15 | `rule-6383d0e05f23e001a089bd57bd449f97db8e1e39df694102b320098d6caec6a4` | none | `DEFINITION` |
| 4 | 16–19 | `rule-fc18bc8ceb43f9a96a719e63e4390ea4cff17cc757b6a60b12c863eb947baba8` | none | `DEFINITION` |
| 5 | 23–23 | `rule-e7562bd9fdea75cbcbc580858d07fc3ff155128dc9eacb02888d4c80c2c39f6a` | none | `DEFINITION` |
| 6 | 24–24 | `rule-94c086eef5eb1ff63da7d10fd63bf998a9a0b17ad46fcdb30b800b81beadfac0` | none | `DEFINITION` |

For every entry, the normalized source SHA-256 is the digest embedded in its
`source_rule_id`. The protected Stage 3 manifest contains exactly these six
unique identities in this exact order. It has no omitted, duplicated, extra,
reordered, or changed identity, and its inventory hash matches the
reconstruction. Trusted `validate_trust_boundary` also succeeds.

## Independent classification judgment

The frozen Python solution defines `_water_in` as a structural row sum,
`_buckets_for` as a structural grid recurrence adding
`(rowWater + capacity - 1) // capacity`, and `max_fill` as a call to that grid
recurrence. The K operational semantics evaluates the translated AST through
ordinary configuration rewrites for calls, environments, conditionals,
subscripts, arithmetic, and returns. The three claims in `spec.k` connect those
executions to the `water` and `requiredBuckets` summaries under positive
capacity.

Against that source and operational semantics:

1. `water(.Ints) => 0` is the base defining equation for the newly introduced
   row-sum summary.
2. `water(I, REST) => I +Int water(REST)` is its structurally descending
   recurrence.
3. `requiredBuckets(.Rows, C) => 0` is the base defining equation for the newly
   introduced bucket-count summary.
4. The guarded `requiredBuckets(rowVal(ROW), ROWS, C)` rule is its structurally
   descending recurrence for the exact per-row ceiling expression used by the
   source solution and postcondition. Its `C >Int 0` guard covers every use in
   the frozen claims.
5. `functionsOf(Module(SS)) => collectFunctions(SS)` defines a fresh structural
   wrapper/macro for the function map already computed by the operational
   semantics. It does not rewrite a runtime configuration or bypass execution.
6. `solutionFunctions => functionsOf(solutionProgram)` defines a fresh named
   proof term for the frozen program's function map.

Thus all six rules genuinely introduce and define a summary, recurrence, macro,
or named proof term. None is an ordinary execution/observation rule. None is a
theorem over pre-existing symbols, and none has the required prove-first,
use-later history of a `PROVED_DERIVED_LEMMA`. None is a `DOMAIN_LEMMA`.
There are no `simplification` attributes, so the simplification-classification
constraint is satisfied vacuously.

The independently reconstructed category counts are therefore:

- `DEFINITION`: 6
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The true domain-lemma set is genuinely empty. There is consequently no
irrelevant purported domain lemma and no relevant domain lemma hidden in a
non-domain category.

## Stage 4 integrity, bijection, and target identity

All signed-resolution tree/file hashes recompute exactly:

- Stage 1 pipeline tree:
  `7794c14ebac8697cc228dd85e23df7ee7791094f6849777f5730c3e31b14c969`
- Stage 1 export tree:
  `e6f2d8f7830a473f20927827e1b3e5d65707b154ab6bd6cf9f302e4cdc6521db`
- selected Stage 2 tree:
  `26043a0638a22b129dc285638f61005350cf78ca84f030fafac441c79b4d5fa5`
- protected Stage 3 manifest:
  `9ccf764057fc63e1793dffa67952eaa988c7b2d298e540aacf3ff565fdcb8e53`
- generated project export tree:
  `58da1c6ced88da2879090625798f781d7929ded7fcc4c927e57a56ac402f2b6d`
- selected Stage 4 generation tree:
  `f854d8651e1e3daf9f79685c778c423bc7533322988763e381e8293ff9501ab8`

The per-file Stage 1 hashes and every applicable hash binding in the input,
generator, export, obligation, trust, selection, and preflight manifests also
match. In particular, the obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and the trust-inventory hash is
`a9d6b6d91b831e85b9ab0da3f777c49cb38607b6bba7e91426d66cabf1d9f2e4`.
The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
over the three required inputs and the trusted toolchain lock. The first
attempt exposed an audit-sandbox PID/proc mismatch: Lean 4.22 asks for
`/proc/<getpid()>/exe`, but the namespace PID returned inside this sandbox has
no corresponding proc entry. That failed attempt is preserved. I then used the
recorded, narrow compatibility shim in
`evidence/proc_self_readlink_shim.c`, which redirects only
`/proc/<digits>/exe` reads to the semantically equivalent `/proc/self/exe`.
It changes no mounted input, producer, checker, generated source, or theorem.
With that environment correction, the unchanged trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `44`;
- `lake clean` exit `0`; and
- `lake build` exit `0`, with output hash
  `ee5606bb67f5ae11fabefb458d1af63a74faae62ee46b7836c5e742348ca7883`.

The returned object exactly matches the recorded Stage 4 preflight object.

The independently accepted domain-rule ID sequence is empty. It matches,
bijectively and in order, each of:

- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`; and
- generated trust parameters: `[]`.

The generator and export obligation counts are both zero. Therefore there are
no omitted, duplicated, irrelevant, weakened, or vacuous conjuncts. Trusted
target extraction and expected-target reconstruction both return `null`; an
independent scan finds zero `def targetStatement` declarations. The generator
manifest, preflight, and audit input all bind the target to `null`. This is the
exact fixed target for a genuinely empty domain set, not a changed or weakened
theorem.

## Stage 5

Stage 5 is correctly absent in `CLASSIFICATION_ONLY`: no generated target
exists, no Stage 5 result or workspace is recorded, and no `/candidate` is
mounted. A fresh `Base` proof workspace, `Proof.final`, `#print axioms`, and
parameter operational-bridge audit would be inappropriate because there is no
theorem to prove.

## Evidence

Raw commands, complete source snapshots, hashes, checker returns, and results
are under `/audit-output/evidence/`. The main records are:

- `00_environment_and_inputs.log`
- `01_producer_identity.log`
- `02_reconstruct_inventory.log`
- `03_frozen_sources.log`
- `04_rerun_preflight.log` (initial environment failure)
- `04a_lean_environment_fix.log`
- `04_rerun_preflight_with_shim.log`
- `04_preflight_return.json`
- `05_independent_generation_gate.log`

The protected Stage 3 classification is mathematically correct, the selected
Stage 4 no-obligation result is structurally and semantically appropriate, and
the absence of Stage 5 is required by the empty domain-lemma set.

VERDICT: PASS
LEGITIMACY: LEGIT
