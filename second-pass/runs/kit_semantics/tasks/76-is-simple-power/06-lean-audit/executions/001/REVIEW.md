# Independent Stage 3–5 Audit: `76-is-simple-power`

## Outcome

This was a `CLASSIFICATION_AND_PROOF` audit for condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The Stage 3
classification, deterministic Stage 4 generation, and Stage 5 Lean proof all
pass independent review.

The audit methodology followed the proof-validation contract: successful K
and Lean runs were treated as structural evidence only. The proof-local K
rules, generated obligations, fixed target, Lean trust dependencies, and every
operational parameter were checked independently.

## Input and producer integrity

The launcher state in `/audit-input.json` and `AUDIT_MODE` agree on
`CLASSIFICATION_AND_PROOF`.

Before judging Stage 4, I hashed the mounted generation-time producers:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image ID is consistently
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`;
the same digest is encoded in the immutable producer-source path recorded by
`/audit-input.json`. The mounted producer-source tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
also exactly as recorded.

Independent hash recomputation also established:

| Input | Recomputed hash | Recorded match |
|---|---|---|
| Stage 1 workspace, campaign tree hash | `399a442a3f278b7b0453de046416fc8daeec3b5ff4f37118cd0fc3b1747983c9` | Yes |
| Stage 1 export digest | `b37ed1671273ef2069cd75b21a4494d24a3a0daaf9f8894219fa96aa384ebd12` | Yes |
| Selected Stage 2 audit tree | `ca4f6b4d9250375426d6bfb3f1219bd4a417c288673d06e34bd6503dce24f24f` | Yes |
| Stage 3 manifest | `7b5a119f83d1e14255b83dc94aa212db060ad43525375615d529eaafc6b4890c` | Yes |
| Stage 4 generation tree | `56240d1af7558b133675020ddc0df7058d5a6f4a1ada262c262dfe1d4ffed707` | Yes |
| Generated Lean tree | `b1345c28d09c462aaa160aea2ae56f7c0e8b5cbc71949b0c2da40253530d1b77` | Yes |
| Mounted Stage 5 workspace | `13cc84ba587cd46bec51bc93e992e62f122a6efb74a7483187afb0c6de7476a9` | Yes |

All 771 per-file Stage 1 hashes recorded in the audit input also match. The
canonical hash of the complete `resolution` object matches
`resolved_input_sha256`.

Evidence:

- `evidence/00-launcher-and-inputs.txt`
- `evidence/01-producer-identity.txt`
- `evidence/05-recorded-hash-recomputation.txt`
- `evidence/16b-independent-structural-audit-success.txt`

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The local verification-module closure contains
only `VERIFICATION`; imported supplied-semantics modules are outside the local
`verification.k` module closure.

- `verification.k` SHA-256:
  `3ecbd3d511a9a62b04cdd41a9ef6239124ae8eab1f2147e447d7e1bf98689512`
- Inventory SHA-256:
  `d2933cd1014ec18a12e3f519fc18739b2c3d87ab2b3a6ac648eeaf11c68ae48d`
- Inventory size: 9 rules

The reconstructed entries, in canonical source order, are:

| Lines | `source_rule_id` / normalized source SHA-256 | Independent class |
|---|---|---|
| 13–13 | `rule-146fed052167b079e1650450e1ce639924212da85a65b3aba6d9be3d6e53c7e3` | `DEFINITION` |
| 15–16 | `rule-60585bbb6d312b6f4f8499ebbf464f74ddf2e2181ec92b0e8af660b2838bc868` | `DEFINITION` |
| 18–19 | `rule-896a8a4fcf1778edbc32f433cc5724feec0edb677d9dea32a3e484bb2aecf746` | `DEFINITION` |
| 21–22 | `rule-3ecd89403379532a7e0ba4d1d0747278594ded6e9d59f9925bdee477f6b5ddc3` | `DEFINITION` |
| 24–25 | `rule-e5a3d5202919810bbe675a2a77fceecdb470e4b5c07f803b5b3ecbed8f59041b` | `DEFINITION` |
| 27–31 | `rule-d19d1bda5d0346f529812d8ff45415af253ed73e3bc020870bf8b1750eb773b9` | `DEFINITION` |
| 33–36 | `rule-775415705833fb882b7bb2633fea60ea3123195b617f4a19ad0450c43e3dd4ae` | `DEFINITION` |
| 40–43 | `rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee` | `DOMAIN_LEMMA` |
| 47–51 | `rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b` | `DOMAIN_LEMMA` |

For every entry, the `source_rule_id` is exactly `rule-` followed by its
recomputed normalized source hash. The Stage 3 manifest contains these same
nine identities exactly once and in the same order. Its inventory hash is the
recomputed whole-inventory hash. There are no omissions, duplicates, extra
rules, reordered identities, or unaccounted classifications.

Evidence:

- `evidence/02-reconstructed-rule-inventory.json.txt`
- `evidence/03-stage3-bijection-and-classifications.txt`
- `evidence/16b-independent-structural-audit-success.txt`

## Independent Stage 3 classification

The first seven rules are the exhaustive equations for the named
`simplePower(Int, Int)` summary:

1. `simplePower(1, N) = true`;
2. the `N = 0` case;
3. the `N = 1` case;
4. the `N = -1` case;
5. the `X = 0`, `|N| ≥ 2` case;
6. the exact-factor recursive case; and
7. the nondivisible terminal case.

They define a named mathematical summary and do not rewrite an operational
configuration or bypass source-program execution. `DEFINITION` is therefore
the correct class for all seven. There are no local ordinary
execution/observation rules, so the `OPERATIONAL_RULE` set is empty.

The two `[simplification]` rules are not definitions:

- Lines 40–43 establish the loop-exit fact
  `(X == 1) == simplePower(X,N)` when `|N| ≥ 2` and `pyMod(X,N) ≠ 0`.
  This is directly relevant to the source function's final `return x == 1`
  and the loop invariant postcondition.
- Lines 47–51 establish summary preservation under `X := X /Int N` on the
  nonzero divisible loop-body domain. This is directly relevant to the
  source loop assignment and invariant preservation.

Both are mathematically relevant domain facts. Neither qualifies as
`PROVED_DERIVED_LEMMA`: `prove.sh` compiles `verification.k` with both rules
already present before any `kprove` command, and there is no earlier exact
proof against a module omitting the rule. They are therefore correctly
classified `DOMAIN_LEMMA`. Every simplification is thus classified as either
`DEFINITION` or `DOMAIN_LEMMA` as required.

The supplied integer semantics confirms that source `%` is `pyMod`, source
`//` is `(X - pyMod(X,N)) /Int N`, and `pyMod` is
`((X %Int N) +Int N) %Int N`. This makes both domain lemmas faithful to the
actual loop rather than unrelated arithmetic claims.

Evidence:

- `evidence/04-frozen-source-spec-verification.txt`
- `evidence/17-operational-bridge-source-comparison.txt`

## Deterministic Stage 4 generation

I reran the required trusted function with:

```text
PYTHONPATH=/reference
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The successful rerun returned:

- status `PASS`;
- obligation count `2`;
- generated tree
  `b1345c28d09c462aaa160aea2ae56f7c0e8b5cbc71949b0c2da40253530d1b77`;
- Stage 1 digest
  `b37ed1671273ef2069cd75b21a4494d24a3a0daaf9f8894219fa96aa384ebd12`;
- Stage 3 hash
  `7b5a119f83d1e14255b83dc94aa212db060ad43525375615d529eaafc6b4890c`;
- zero generated sorries; and
- successful fresh `lake clean` and `lake build`.

The first attempted rerun exposed a sandbox PID-namespace issue rather than an
artifact error: Lean 4.22 uses `/proc/<getpid>/exe`, while the sandbox reported
PID `2` without mounting `/proc/2`; `/proc/self/exe` remained valid. I recorded
the failure, diagnosed it, and used a 34-line preload shim that redirects only
that equivalent self-executable `readlink` call. Its source and binary hashes
are recorded. With that environment-only correction, the unchanged pinned
Lean 4.22 binaries reported commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and the unchanged trusted
preflight passed.

The ordered domain-rule IDs, Stage 4 `source_rules`, and obligation IDs are the
same two-element unique list. Each obligation preserves its source span,
normalized hash, inventory hash, discovery hash, and full generated conjunct.
The generated obligations are exactly:

1. Under `|N| ≥ 2` and `pyMod(X,N) ≠ 0`,
   `((X ==Int 1) ==Bool simplePower(X,N)) = true`.
2. Under `X ≠ 0`, `|N| ≥ 2`, and `pyMod(X,N) = 0`,
   `simplePower(X,N) = simplePower(X /Int N,N)`.

These are faithful universal implications for the two K rules. The variable
order is immaterial because both variables are universally quantified. No
guard, result term, or equality was dropped or weakened. The premises are
satisfiable—for example `(X,N) = (2,3)` for the first and `(8,2)` for the
second—so neither conjunct is vacuous under the fixed operational
interpretation.

The generated target is the exact conjunction of those two obligations:

- declaration:
  `Klean76IsSimplePower.Lemmas.targetStatement`;
- definition SHA-256:
  `78af6612ecb0b47b8abe54c5a8b84d6a3be6e9fd09a776f1ac24b2ad19dc190d`;
- application SHA-256:
  `3a38f4193dccfec193be3de8f58532bdb100145b03f3d84fce18b08b613e4d6e`.

The declaration, parameter list, parameter binding hashes, statement, and both
target hashes agree exactly across the generated source, obligation map,
generator manifest, Stage 4 preflight record, and audit input.

Evidence:

- `evidence/06-klean-preflight-rerun.txt`
- `evidence/07-lean-toolchain-diagnostic.txt`
- `evidence/09-lean-pid-namespace-shim.txt`
- `evidence/10-klean-preflight-rerun-success.txt`
- `evidence/11-stage4-obligations-target-trust.txt`
- `evidence/16b-independent-structural-audit-success.txt`

## Stage 5 clean build and theorem identity

The mounted candidate contains the proof overlay and cached build outputs; its
mounted `Base` directory is empty. I did not trust that cache. I created
`/tmp/audit-work/lean-proof-audit`, copied the candidate's outer project
sources and metadata, and copied the immutable Stage 4 generated project into
it as `Base`. The resulting `Base` digest exactly matches
`b1345c28d09c462aaa160aea2ae56f7c0e8b5cbc71949b0c2da40253530d1b77`.

In that fresh project:

```text
lake clean
LAKE_CLEAN_EXIT: 0

lake build
Build completed successfully.
LAKE_BUILD_EXIT: 0
```

The candidate `Proof.lean` has no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`, and introduces no declaration named `targetStatement`. There is
exactly one `Proof.final`.

Kernel printing and an explicit type-ascription check show that `Proof.final`
has exactly this type:

```text
Klean76IsSimplePower.Lemmas.targetStatement
  Proof._andBool_
  Proof._orBool_
  Proof.«_>=Int_»
  Proof.«_<=Int_»
  Proof.«_==Bool_»
  Proof.«_==Int_»
  Proof.«_=/=Int_»
  Proof.«_/Int_»
  Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int»
  Proof.«simplePower(_,_)_VERIFICATION_Bool_Int_Int»
```

It therefore proves the fixed generated theorem rather than a duplicate,
weakened, or separately stated variant.

Evidence:

- `evidence/12-candidate-inventory-and-base-diff.txt`
- `evidence/13-fresh-lake-clean-build.txt`
- `evidence/15-proof-and-target-identity.txt`
- `evidence/16b-independent-structural-audit-success.txt`

## Axiom accounting

The exact output of `#print axioms Proof.final` is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are Lean's standard foundational axioms. There is no `sorryAx`.
`trust-inventory.json` records 43 generated project trust declarations, but
none appears in the dependency list of `Proof.final`; in particular, the
generated axiomatized `simplePower` symbol is not used by the proof. The
candidate itself introduces no axiom or opaque declaration. Thus there is no
unrecorded project-level proof escape.

Evidence:

- `evidence/14-print-axioms-proof-final.txt`
- `evidence/23-axiom-reconciliation.txt`

## Operational-bridge audit

`SortBool` is Lean `Bool` and `SortInt` is Lean `Int`. Every target parameter
has one exact candidate definition:

| Target parameter | Candidate definition | Frozen operational meaning | Judgment |
|---|---|---|---|
| `_andBool_` | `a && b` | K Boolean conjunction | Exact |
| `_orBool_` | `a \|\| b` | K Boolean disjunction | Exact |
| `«_>=Int_»` | `decide (a ≥ b)` | K `>=Int` | Exact |
| `«_<=Int_»` | `decide (a ≤ b)` | K `<=Int` | Exact |
| `«_==Bool_»` | `a == b` | K `==Bool` | Exact |
| `«_==Int_»` | `a == b` | K `==Int` | Exact |
| `«_=/=Int_»` | `a != b` | K `=/=Int` | Exact |
| `«_/Int_»` | `Int.tdiv a b` | K truncating `/Int` | Exact on the nonzero rule domain |
| `pyMod` | `Int.tmod (Int.tmod a b + b) b` | `((a %Int b) +Int b) %Int b` | Exact on the nonzero rule domain |
| `simplePower` | exhaustive recursive Boolean definition | The seven frozen summary equations | Exact |

The two arithmetic parameters are used only under `|N| ≥ 2`, so the K
undefined divisor-zero case is outside both bound source-rule domains. The
Lean totalization at divisor zero is not used to prove either obligation.

The candidate `simplePower` definition follows the same case order and guards
as the frozen rules. In its divisible recursive branch, `pyMod = 0`, so its
`Int.tdiv x n` argument is exactly the frozen
`(x - pyMod(x,n)) /Int n` argument. The definition also matches the source
solution's special handling of `x = 1`, `n = 0`, `n = 1`, `n = -1`, and
`x = 0`.

Adversarial tests covered Boolean truth-table boundaries, signed comparison,
equality/inequality, signed truncating division, signed Python modulo, zero
and degenerate bases, positive powers, negative bases, and nonpowers. A
broader 171-case grid over 19 values of `X` and 9 values of `N` was compared
against an independently implemented oracle for K truncating division, the
frozen `pyMod` equation, and the seven `simplePower` equations:

```text
records=171
mismatches=0
```

This finite test is corroborative, not a substitute for the direct definition
comparison above.

Counterfactual Lean checks showed that the abstract target alone can accept
several dishonest interpretations—constant-false conjunction/disjunction,
constant-true Boolean equality, constant-false inequality, and identity
division. This confirms that a clean theorem proof alone would be
insufficient. The actual candidate does not use any of those definitions and
pointwise adversarial witnesses distinguish every actual parameter from its
constant or identity mutation. Additional concrete counterfactuals show that
bad integer equality, constant-zero `pyMod`, and constant-false
`simplePower` are rejected. The candidate therefore passes the required
operational bridge audit.

Evidence:

- `evidence/17-operational-bridge-source-comparison.txt`
- `evidence/18b-operational-bridge-adversarial-tests-success.txt`
- `evidence/19-target-counterfactual-mutations.txt`
- `evidence/20d-rejected-counterfactual-mutations-success.txt`
- `evidence/21-operational-bridge-grid-lean.txt`
- `evidence/22-check-operational-grid.txt`

## Final judgment

The independently reconstructed Stage 3 inventory and classification are
correct. The Stage 4 producer provenance is intact, the deterministic
generation is structurally and mathematically faithful to the two genuine
domain lemmas, and the target is fixed and unchanged. The fresh Stage 5 proof
builds, proves exactly that target, has no forbidden trust escape, and binds
all ten operational parameters to honest implementations of the frozen K
meaning.

VERDICT: PASS
LEGITIMACY: LEGIT
