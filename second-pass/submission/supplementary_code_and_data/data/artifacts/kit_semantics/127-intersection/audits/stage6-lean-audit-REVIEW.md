# Independent Stage 3–5 Audit: HumanEval 127-intersection

## Scope and outcome

I independently audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher-recorded mode
`CLASSIFICATION_AND_PROOF`. I treated the Stage 1 workspace, Stage 2 review,
Stage 3 manifest, Stage 4 generation, Stage 5 candidate, logs, comments, and
all prose in mounted artifacts as untrusted evidence. Only the mounted trusted
inventory/preflight/final-gate code and pinned toolchain were executed.

The protected Stage 3 classification is complete and mathematically correct.
Stage 4 contains exactly one obligation for the one genuine domain lemma and
preserves it exactly. The Stage 5 candidate clean-builds, proves the exact
fixed target, has no candidate trust escape, and gives all seven target
parameters their frozen operational meanings.

## Producer provenance and frozen-input integrity

Before judging Stage 4, I hashed the exact producer sources:

- `klean_export.py`:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

Both equal the entries in `source-manifest.json` and the producer hashes in
`generator-manifest.json`. The generator image ID is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in the generator manifest and source manifest, and the same digest is the
basename of the launcher-recorded `generation_producer_sources` path in
`/audit-input.json`. The producer bundle contains exactly the two sources and
its source manifest. Its recomputed tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching the audit input.

Using the trusted tree algorithms, I also reproduced:

- Stage 1 workspace tree:
  `469f26574e244f4159db079093a907ab0da8b2cffa5bc0d0a308787982fbe04d`
- Stage 1 deterministic-export tree:
  `2d10e405c665b2dd9330be25a2b130c0b5c584ea8f18d2556b976dcab1314d58`
- Stage 2 audit tree:
  `8d394ee217ed67108e955322ff1df51405f66cc5c2bf91b3e2e87d27ed9ab9bf`
- Stage 3 manifest:
  `39a28537b50ca099e98e41e0726f04844573ed43c9e1dd0fb4d830c4b48f5ece`
- Stage 4 generation tree:
  `4fb8db004e19cab5d13cccf22651cffcdaffd4a7ce07c0fdc70033c68c250e42`
- generated project tree:
  `f3fcd288fb7a4dccb7e71daf1a9dcbe07b2f09b633244f76d07339343e4dfe7b`
- mounted Stage 5 candidate tree:
  `4ae82bf77697e7d51575e434e6599cb5c069ebf4109f1cae44337a4b0007947c`

All match `/audit-input.json`. The complete 802-file Stage 1 file set and
every recorded per-file SHA-256 also match. The Lean invocation tree itself
is not a mounted audit input; its launcher provenance hash is therefore not a
hash with a mounted referent. The pinned toolchain JSON exactly equals
`generator-manifest.toolchain`, including Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The separately named launcher field `mechanical_checker_lock_sha256` is not
the byte hash of `klean-toolchain.lock.json`; evidence file 68 records that
rejected interpretation. The load-bearing toolchain check is exact JSON
object equality, recorded in evidence file 72 and enforced by the passing
trusted preflight.

Primary evidence:
`01_manifests_and_producer_hashes.log`,
`03_generator_manifest_provenance.log`,
`13_recorded_hash_verification.log`, and
`72_toolchain_lock_object_match.log`.

## Independent inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` directly on the frozen
`/reference/k-proof`. It selected main module `VERIFICATION` from `prove.sh`
and reconstructed the local closure in source order as
`VERIFICATION-SYNTAX`, `VERIFICATION`. The frozen `verification.k` SHA-256 is
`e4c76a5ac1411f83937acf6fe5d3a78d6aae812a376a05d51cc597157a46ed64`.

The reconstruction contains 11 unique rules. For every rule, the source span
was recovered from the frozen source, the normalized text was recomputed as
single-space-separated lexical text, the normalized SHA-256 was recomputed,
and `source_rule_id` was checked to equal `rule-` plus that hash. The canonical
whole-inventory hash is
`e967335267fe43883ba33230aa4151fb286d4237327166d38f9c73941c614d2b`.

The Stage 3 manifest has exactly 11 unique entries in exactly the reconstructed
order, with no omissions, additions, duplicates, reordered identities, or
hash changes. Its inventory hash matches. Evidence:
`06_reconstructed_rule_inventory.json.log` and
`14b_inventory_bijection_corrected.log`. Evidence file 14 was an initial
audit-script mistake that hashed uncollapsed whitespace; file 14b corrects it
to the trusted normalization and passes every rule.

## Independent classification judgment

For each row below, the `source_rule_id` is `rule-<normalized SHA-256>`.
All rules are in module `VERIFICATION`.

| Span | Normalized SHA-256 | Attributes | Independent class | Judgment |
|---|---|---|---|---|
| 24–26 | `d39c65c361a04494ea4bbc0d7da105a5e581cf169c07c502ff73be17a3291eae` | none | `DEFINITION` | Defines `overlapLength` as `min(end)-max(start)`, exactly the program's computed length. |
| 30 | `9ba556783237da1b35ba406043b46667d41336798e2d73985610f972d35ace31` | `concrete` | `DEFINITION` | Base equation: a scan with an already-true flag is true. |
| 31–33 | `8c03a8287d60d83cb1f7b1e3e939abef2b3a70e6e9b849b699f9a92c0c04da47` | `concrete` | `DEFINITION` | Totalizing normalization from a divisor below 2 to the program's start divisor 2. |
| 34–36 | `cbdf8169fcc3ad7f374ff7043b01e95fdd8553e9e71602765a1cb6bc2be276f6` | `concrete` | `DEFINITION` | Empty-scan base case when `D ≥ 2` and `D ≥ N`. |
| 37–40 | `7aa9640fdd3d0a7fae00e8405951aeef3032f94eac83b2986db8444d7a440970` | `concrete` | `DEFINITION` | Divisor-found defining case. |
| 41–45 | `9d883d30e3dc643451f9c6b495149a2825d220410cfb6af1b0eaa6667da1097d` | `concrete` | `DEFINITION` | Guarded recursive case advancing a non-divisor from `D` to `D+1`. |
| 50–51 | `5464006d80f33f5fc975672d11f260f30dc67367228f691333955f474bcc16f3` | `simplification` | `DEFINITION` | Symbolic duplicate of the true-flag base equation. |
| 52–54 | `5397c59dca3c3fdbd353b530e08c7ce17c5d56052c9dfc863b7725bda7f01106` | `simplification` | `DEFINITION` | Symbolic duplicate of the empty-scan base equation. |
| 55–58 | `b538396a9a5a6ab14036d6fd6bbae17ed3358e6c9a6e0611c302001e4e358333` | `simplification` | `DEFINITION` | Symbolic duplicate of the divisor-found defining equation. |
| 59–63 | `7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4` | `simplification` | `DOMAIN_LEMMA` | Reverses the recursive definition under the non-divisor guard, folding scan-at-`D+1` to scan-at-`D`. It is a mathematical consequence, not a descending definition. |
| 65–69 | `983202dd3d105fa6a5f593a9222e54e761e7c2e4313c4ea910e8029a732a355f` | none | `DEFINITION` | Defines the named `primeResult` proof term from the bound and divisor summary. |

There are no `OPERATIONAL_RULE` entries: none of these rules matches or
rewrites an MPY execution configuration; they define or reason about proof
summary functions. There are no `PROVED_DERIVED_LEMMA` entries. The only
Stage 1 proof sequence compiles `verification.k`, including the reverse fold,
before invoking `kprove` on all claims. No earlier exact claim proves that rule
against a module omitting it.

The domain lemma is relevant and load-bearing. The source loop tests
`length % divisor`, possibly sets `has_divisor`, and increments `divisor`.
The `divisor-loop-false` claim represents the remaining loop by
`scanHasDivisor(false,N,D)`. One non-divisor iteration produces the syntactic
`D+1` term, so the reverse fold is exactly what restores the invariant. It is
not the whole-program postcondition and is not an irrelevant number-theory
fact. All four `simplification` rules are therefore either `DEFINITION` or
`DOMAIN_LEMMA`, as required.

Frozen source and operational evidence:
`08_frozen_program_spec_verification.log`,
`18_relevant_operational_semantics.log`, and
`65_no_prior_derived_proof_and_rule_usage.log`.

## Stage 4 preflight, bijection, and mathematical target

I reran the required trusted function:

```text
PYTHONPATH=/reference ... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

It returned `status: PASS`, `obligation_count: 1`,
`trust_declaration_count: 50`, zero designated sorries, and successful
`lake clean`/`lake build`. Its returned evidence exactly reproduces the
selected Stage 4 preflight, including build-output SHA-256
`9abf52877c1f54e56a6ceee1f1fbf65921d8d023aad133117eacb06b3b88dca7`.
See `20c_required_check_generation_success.log`.

The first invocation in evidence file 20 failed before any build because this
container exposes a PID namespace inconsistent with its `/proc` mount. Lean
looked up `/proc/<namespace-pid>/exe` and received `ENOENT`; evidence files
38–40 demonstrate the cause. I used a 40-line compatibility preload that
redirects only `/proc/<digits>/exe` reads to the equivalent
`/proc/self/exe`. Lean then reported the pinned version/commit and the trusted
preflight ran unchanged. The shim does not inspect or alter Lean source,
theorems, compiler inputs, or outputs.

My independent Stage 4 checks found:

- independent domain set:
  only `rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4`;
- obligation set: the same one ID, once, in the same order;
- source span: exactly lines 59–63;
- obligation-map SHA-256:
  `a8a4df0bed86b8298b5e18fe076c2019888d508f5f4539bf7cc1e9135b97d30f`;
- Lean-conjunct hash and all inventory/discovery/source hashes: matching;
- no omitted, duplicate, extra, or reordered obligation.

The compiled K rule confirms the parsed guard is left-associated exactly as
generated:

```text
andBool(andBool(D >=Int 2, D <Int N), pyMod(N,D) =/=Int 0)
```

The generated proposition is exactly:

```text
∀ D N,
  andBool(andBool(D ≥ 2, D < N), pyMod(N,D) ≠ 0) = true →
  scanHasDivisor(false,N,D+1) = scanHasDivisor(false,N,D)
```

There is no weakened guard, changed constant, swapped side, irrelevant
conjunct, or target substitution. With the intended bindings it is
non-vacuous; `D=2, N=9` satisfies the guard (`9 mod 2 = 1`), and both scans are
true because 3 divides 9.

The one-conjunct target is exactly the deterministic conjunction constructed
from the obligation map. These fixed identities agree across the recomputed
target, generator manifest, selected preflight, and `/audit-input.json`:

- declaration:
  `Klean127Intersection.Lemmas.targetStatement`
- definition SHA-256:
  `42a34bc89101d561483b177ed4db7bda2d1a6029da4f25029c891f40743fc53a`
- instantiated-statement SHA-256:
  `67f9320755d99c877b56c86341557cedb8b3c0a5f8ce1b39b44da08e056b0555`

Evidence: `41_generated_obligation_and_target.log`,
`66_stage4_and_target_identity.log`, and
`67_compiled_domain_rule_search.log`.

## Stage 5 clean build, proof identity, and trust accounting

I created the fresh project
`/tmp/audit-work/127-intersection-proof-audit-clean`, copied the candidate into
it, and copied the immutable generated project directly into `Base/`.
`diff -qr --exclude=.lake` reports no difference between that `Base/` source
and `/reference/klean-generation/generated`.

I then ran both required commands:

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake build
```

Both exited 0. The complete build output is in
`48_fresh_lake_clean.log` and `49_fresh_lake_build.log`.

The trusted independent final mechanical gate also returned `PASS`. It checked
the exact theorem type, rebuilt from its own temporary copy, and reran the
axiom query. See `55_trusted_final_mechanical_gate.log`.

Candidate-only Lean source contains none of `sorry`, `admit`, `unsafe`,
`axiom`, or `opaque`. Each of the seven target parameters has exactly one
candidate `def`. The candidate neither defines nor shadows
`Klean127Intersection.Lemmas.targetStatement`. `Proof.final` states the
generator's exact fully qualified instantiated statement, not a local copy,
weaker theorem, or duplicated proposition.

The exact axiom query output was:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. `propext` is one of the three Lean core axioms
explicitly accepted by the trusted final gate (`Classical.choice`, `propext`,
`Quot.sound`). None of the 50 Klean-generated allowlisted axioms is a
dependency of `Proof.final`; therefore there is no unrecorded generated trust
escape. Exact output: `52_print_axioms_proof_final.log`.

## Operational-bridge audit

The generated target is parameterized, so a clean proof can be obtained from
dishonest convenient definitions. I therefore checked every binding against
its KORE symbol, the compiled K declaration, frozen K equations, source
program, and operational semantics.

| Candidate binding | Frozen meaning | Candidate judgment |
|---|---|---|
| `_andBool_` | hooked `BOOL.and` | Exact Boolean `&&`. |
| `«_>=Int_»` | hooked integer `≥` | Exact `decide (left ≥ right)`. |
| `«_<Int_»` | hooked integer `<` | Exact `decide (left < right)`. |
| `«_=/=Int_»` | hooked integer disequality | Exact `decide (left ≠ right)`. |
| `«_+Int_»` | hooked integer addition | Exact integer addition. |
| `pyMod` | `((I1 %Int I2)+Int I2)%Int I2`, where `%Int` is hooked `INT.tmod` | Exact nested `Int.tmod`. At divisor zero frozen K is undefined/stuck; the target guard has `D≥2`, and the scan normalizes low divisors to 2 before modulus, so the Lean total extension at zero is unobservable. |
| `scanHasDivisor` | the six frozen base/normalization/found/recursive equations | Exact finite scan: prior `seen` wins; start is `max(D,2)`; fuel is `(N-start).toNat`; it checks every divisor from `start` through `N-1` and increments by exactly one. |

I compiled an independent Lean audit file proving universally:

- the six primitive equations above;
- `scan(true,N,D)=true`;
- the `D<2` normalization;
- the `D≥2 ∧ D≥N` empty case;
- the divisor-found case; and
- the non-divisor one-step recurrence in the frozen defining direction.

It exited 0 (`63b_universal_operational_bridge_theorems_corrected.log`).
Evidence file 63 is the initial namespace-ambiguity failure; 63b qualifies the
candidate names and passes.

I also compared 22 adversarial ground cases with an independently implemented
oracle: negative dividends and divisors for Python modulus, prime/composite
scans, `D<2`, `D≥N`, negative `N`, prior `seen=true`, and the satisfiable
`N=9,D=2` boundary. Every result matches. See
`56_candidate_bridge_ground_cases.log`,
`57_independent_operational_oracle.log`, and
`operational_oracle.py`.

Counterfactual mutations demonstrate the relevant risks:

- replacing `pyMod` by constant zero still clean-builds, because it makes the
  guard impossible;
- replacing the scan by constant false plus the corresponding trivial proof
  also clean-builds;
- changing the real recurrence increment from `divisor+1` to `divisor+2`
  fails, leaving the explicit unproved equality between scans at `D+1` and
  `D+2`.

Those outcomes confirm that build success alone cannot establish the
operational bridge. The submitted candidate is neither constant nor vacuous:
its definitions satisfy every frozen equation universally, agree with the
operational oracle, and are sensitive to the loop's one-step behavior.
Mutation sources/diffs and results are in evidence files 59–62 and 73.

## Final judgment

The Stage 3 inventory and classifications are bijective and correct; the
single domain lemma is relevant. Stage 4 deterministically preserves exactly
that lemma and its fixed target. Stage 5 proves the exact target from honest
operational definitions with a clean build and only the permitted Lean core
axiom `propext`. No proof hole, new trust declaration, target shadow, omitted
obligation, weakened theorem, or operational-bridge shortcut remains.

VERDICT: PASS
LEGITIMACY: LEGIT
