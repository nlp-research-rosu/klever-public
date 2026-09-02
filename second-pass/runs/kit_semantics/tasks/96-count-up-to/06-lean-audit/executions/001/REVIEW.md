# Independent Stage 3–5 audit: `96-count-up-to`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The protected Stage 3 classification is complete and correct. The true domain
set contains exactly two rules: associativity and right identity of the
pre-existing `valSeqConcat` function. Deterministic Stage 4 generated exactly
those two obligations and one fixed conjunctive target. The Stage 5 candidate
defines `valSeqConcat` by the exact two frozen K equations, proves the fixed
target, clean-builds from source, and has no axiom dependencies.

## Producer-source infrastructure gate

I authenticated the producer bundle before judging Stage 4:

| Item | Observed SHA-256 | Required source |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | source manifest and generator manifest |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | source manifest and generator manifest |
| three-file producer tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` | `/audit-input.json` |
| generator image | `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` | source manifest, generator manifest, and audit-input producer path |

The bundle contains exactly `klean_export.py`, `klean.py`, and
`source-manifest.json`. There is no producer-source mismatch and therefore no
infrastructure `AUDIT_ERROR`.

Evidence: `evidence/01_producer_authentication.log`,
`evidence/01b_producer_manifests.log`, and
`evidence/01c_producer_tree_hash.log`.

## Inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` afresh on
`/reference/k-proof`. Its local verification-module closure is, in source
order:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION`

The frozen `verification.k` hash is
`6387393d36d954beb348701b00afefd04d2edff04d8b97c220588d963284b91c`.
The canonical inventory contains 16 rules and has hash
`9eaebbd4fb6dd63f68a3e126ff644a5f975c58ce19f8951223c1ce18c21c72c8`.

For every rule, I recomputed the source span, whitespace-normalized source,
normalized SHA-256, and `source_rule_id`. The protected Stage 3 document has
exactly 16 unique entries in the same order. There are no missing, duplicated,
extra, reordered, or hash-divergent identities. The independent comparison
also verified that each ID is exactly `rule-<normalized_sha256>` and that every
classification is accounted for.

Evidence: `evidence/reconstructed-rule-inventory.json`,
`evidence/compare_inventory.py`, and
`evidence/02_inventory_and_discovery.log`.

## Independent classification of every rule

| Span | `source_rule_id` | Classification | Independent basis |
|---|---|---|---|
| 24–30 | `rule-8f1a14b0902a879bc6ead4dfee122e5e1265e10b0cbb88132187719ffbc45e74` | `DEFINITION` | `innerBody` is a macro naming the exact inner-loop AST. |
| 32–42 | `rule-bdfc23acf9cf70adc41bad986933ed7277937929904f1669b00568437b1c3459` | `DEFINITION` | `outerBody` is a macro naming the exact outer-loop AST. |
| 44–54 | `rule-83bcb3b74f0192957018f8be60acc9a6942a2a28da5d31b585070f5c00c88a41` | `DEFINITION` | `countBody` names the exact source-function AST used by the entry claim. |
| 57–67 | `rule-e9dfcbb6e535df394027c53af10293b33882b5f5e9ba1c1f3ac059558bf60073` | `DEFINITION` | `countBodyStart3` names the validation mutation AST; it is still a named proof term. |
| 76–77 | `rule-6c150dee4919f33b527576715d69f373b0c71d0bcdb234e310a360df2fec8cdb` | `DEFINITION` | Totalizing equation for the fresh `noDivisors` summary below divisor 2. |
| 78–79 | `rule-98cb7ce294f915ee8d7bd2cd06fc8ff072483b0e31e80bffd97c5cc1666119e2` | `DEFINITION` | Empty-search base equation of `noDivisors`. |
| 80–82 | `rule-74f701962b96b34421e1e61caa390bd6effa656a436d73db49594f470a395d73` | `DEFINITION` | Dividing-current-candidate equation of `noDivisors`. |
| 83–85 | `rule-5ab72e98282a264da379bdd15a4b73e006eafa86706e62409af11679a1b2fc90` | `DEFINITION` | Recursive non-dividing equation of `noDivisors`; the divisor increases. |
| 87–88 | `rule-7500a60cba5226d47db935faa305d04b568de603e6bcbbe4fb50cdb3e6fe5a5e` | `DEFINITION` | Empty-range base equation of the fresh `primesBetween` summary. |
| 89–91 | `rule-7753d3ae7b9815bc5b6c497d902a9ef19ee9b4bcbef0e6265b813d6323a65fc4` | `DEFINITION` | Recursive equation skipping candidates below 2. |
| 92–95 | `rule-b48ae093ba4642f6355f72e334eb9498d3e367e9de1b7fe145c19823245aab0d` | `DEFINITION` | Recursive equation including a candidate satisfying `noDivisors`. |
| 96–99 | `rule-5b03c31debf612c50d63a30dc6f22a243c0a65d1667904ed96c9ddf73fe77841` | `DEFINITION` | Recursive equation skipping a non-prime candidate. |
| 101–102 | `rule-d54ce4e171447b38c5db2843b98b90e45c2f0a13e8fa12a42a40543b9884e338` | `DEFINITION` | Base equation of the fresh `primesBelow` summary. |
| 103–104 | `rule-1b022e4a8f2e4e270dcaafb81be7e8e8817e2b746fa792867025fdcc7280935f` | `DEFINITION` | Equation defining `primesBelow` through `primesBetween(2,N)`. |
| 109–111 | `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97` | `DOMAIN_LEMMA` | Associativity is a fact about pre-existing `valSeqConcat`, not one of its defining equations. |
| 112–113 | `rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa` | `DOMAIN_LEMMA` | Right identity is a fact about pre-existing `valSeqConcat`, not one of its defining equations. |

There are no `OPERATIONAL_RULE` entries: none of these 16 rules is an ordinary
execution/observation rewrite over the operational configuration. There are no
`PROVED_DERIVED_LEMMA` entries. Searches across the Stage 1 K claims show that
the two `valSeqConcat` facts are compiled into `VERIFICATION` before the proof;
Stage 1 does not first prove either exact statement against a module omitting
it.

The four `noDivisors` equations are exhaustive on the proof's integer use
domain and recurse by increasing the divisor. The four `primesBetween`
equations are exhaustive and recurse by increasing the candidate. Together
with the two `primesBelow` equations they define the ascending primes below
`N`, matching the source loop and its `N >= 0` entry precondition.

The two domain lemmas are relevant, not decorative. Supplied semantics defines
`valSeqConcat` structurally and implements `primes.append(candidate)` by the
heap update
`valSeqConcat(VS, vCons(candidate, .ValSeq))`. The outer-loop claim summarizes
the accumulated list as `valSeqConcat(P, primesBetween(C,N))`; associativity
and right identity are precisely the normalization facts needed to relate
successive appends to that accumulator.

Both rules bearing `[simplification]` are therefore correctly classified as
`DOMAIN_LEMMA`. No simplification is mislabeled.

Evidence: `evidence/03_classification_sources.log` and
`evidence/04_derived_and_relevance_check.log`.

## Stage 4 preflight, bijection, and fixed target

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required Stage 1 workspace, Stage 3 document, Stage 4 generation,
and pinned toolchain lock. The successful returned evidence reports:

- status `PASS`;
- two obligations;
- Stage 1 export hash
  `e6a0bf4a8787a0883489c1747f181ef02b1e64f529f5e1f1862253ab4f3364b8`;
- Stage 3 hash
  `5322af01ad010f5dbe1a0242bd625f1aa1a7dd0e278d72f37cd85ca259e57fbd`;
- generated tree hash
  `60a4cd1cadb6c090828bf8e06cfb3756fbe438a495fa1e4ec4101e8c292018bb`;
- successful internal `lake clean` and `lake build`; and
- zero designated sorries.

I separately ran 830 hash, identity, and mapping checks with zero failures.
They include every launcher-recorded Stage 1 regular-file hash, all available
mounted tree hashes, every Stage 4 sidecar binding, the obligation-map hash
`89da51a6e4cf3cf17eeebf082650e34888d95161a372a05373a9f37705a68a4a`,
and the exact source-rule/obligation order and uniqueness.

The obligation bijection is:

1. `rule-9345…09b97` ↔
   `∀ A B C, concat (concat A B) C = concat A (concat B C)`.
2. `rule-1bc3…384fa` ↔
   `∀ A, concat A .ValSeq = A`.

These are the exact unguarded K rules. Neither obligation loses a guard,
restricts the sort, changes a side, or inserts `True`, `False`, an unused
premise, or another vacuous conjunct. `SortValSeq` is visibly inhabited by its
empty constructor and has a `vCons` constructor, so the universal equations
are not vacuous.

The generated target is uniquely:

```text
Klean96CountUpTo.Lemmas.targetStatement
  «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
```

Its recorded and recomputed identities are:

- declaration: `Klean96CountUpTo.Lemmas.targetStatement`;
- definition hash:
  `511346591a0e18a4b78267913de54b28109049d3c9204acaca784489d52b97e8`;
- statement hash:
  `c5bf172a92c57628f90b2ffe69684ecd76c896f39379501e114963a3d6b56a55`;
- sole parameter binding hash:
  `c01b877d208f854dc476d9277680d7b0fe3bbd01053a2f18c1b59316203d6538`;
- bound KORE symbol:
  `LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq`.

The obligation map supplies the exact parameter and conjunct material from
which that target is generated. The resulting target object is byte-for-byte
identical in the generator manifest, preflight result, and
`/audit-input.json`. Because the independently classified domain set has two
members, `KLEAN_NO_OBLIGATIONS` would not have been legitimate; the selected
status is correctly `OK`/`PASS` with a generated target.

Evidence: `evidence/05i_check_generation_pass.log`,
`evidence/audit_hashes_and_stage4.py`,
`evidence/06_stage4_obligations_and_target.log`, and
`evidence/07_stage4_independent_checks.log`.

## Lean environment note

The first preflight attempt exposed a sandbox-specific `/proc` mismatch:
`getpid()` returned a namespace PID for which `/proc/<pid>/exe` was absent.
Lean 4.22 uses that path to locate its own installation, so Lake initially
reported that it could not detect its installation. A compiled minimal probe
reproduced `ENOENT`.

For the successful runs I used the recorded
`evidence/proc-self-readlink.c` shim, which redirects only
`/proc/<pid>/exe` self-lookups to the equivalent `/proc/self/exe`. Its source
hash is
`a6a483c6f14d4ca82d4e8a0dff5e6982cb174ec87b51304515685bdb7cd6dc40`.
It does not intercept proof files, source reads, hashing, or theorem
elaboration. With the shim, Lean identified itself as version `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.
The trusted frozen-toolchain gate also passed.

Evidence: `evidence/05b_toolchain_diagnosis.log`,
`evidence/05g_proc_self_shim.log`, and
`evidence/proc-pid-probe.c`.

## Stage 5 clean build and target identity

I created a source-only fresh project at
`/tmp/audit-work/proof-audit-source-only.k206OF`, copied the generated Stage 4
project into it as `Base`, and excluded all candidate `.lake` cache artifacts.
In that directory:

- `lake clean` exited 0;
- `lake build` exited 0; and
- the build compiled `Prelude`, `Sorts`, `Inj`, `Lemmas`, and `Proof` and
  ended with `Build completed successfully.`

The copied `Base/Klean96CountUpTo/Lemmas.lean` remains byte-identical to Stage
4 (file hash
`d59b0e703ed275cd91ec79665307f3066fd04371c0e83af5cb364b7dfb288876`).
The copied `Proof.lean` remains byte-identical to the candidate (file hash
`8d3e17ecf087c050f52365a23d04861d03a729f3ccdea1b06170c2567dec1a59`).

Candidate source contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`. It neither defines `targetStatement` nor enters namespace
`Klean96CountUpTo.Lemmas`; therefore it does not change or shadow the fixed
target. There is exactly one `Proof.final`, and its type is exactly the fixed
generated statement, not a duplicate or weakened proposition.

The trusted Stage 5 mechanical gate independently removed candidate `.lake`
and `Base`, reconstructed `Base` from Stage 4, ran clean/build/type checks, and
returned `status: PASS` with `toolchain_gate: PASS`.

Evidence: `evidence/08c_candidate_source_only_clean_build.log`,
`evidence/11_stage5_static_and_identity.log`, and
`evidence/13_stage5_mechanical_gate.log`.

## Axiom accounting

The exact Lean output for `#print axioms Proof.final` is:

```text
'Proof.final' does not depend on any axioms
```

Thus the used-axiom set is empty. It contains neither `sorryAx` nor an
unrecorded dependency. The generated trust inventory contains 48 unique
function-valued infrastructure declarations, but none is in the dependency
closure of `Proof.final`; no allowlist entry is needed to justify this proof.
The trusted mechanical gate independently returned `"used_axioms": []`.

Evidence: `evidence/AxiomAudit.lean`,
`evidence/09b_source_only_print_axioms.log`, and
`evidence/13_stage5_mechanical_gate.log`.

## Operational bridge for the target parameter

There is one `target.parameters` entry. The candidate defines its exact name
once:

```text
SortValSeq → SortValSeq → SortValSeq
```

The frozen supplied semantics defines the bound KORE operation by:

```text
valSeqConcat(.ValSeq, T) = T
valSeqConcat(vCons(V,S), T) = vCons(V, valSeqConcat(S,T))
```

The candidate definition has exactly those two pattern-matching equations:
empty left sequence returns the right sequence; a left `vCons` preserves its
head and recursively concatenates its tail. This is a structural recursive
definition on the complete `SortValSeq` domain, not a constant, identity,
hard-coded table, or opaque choice.

Independent Lean checks established both universal equations by definitional
equality and exercised:

- empty concatenated with a nonempty sequence;
- `[1,2]` concatenated with `[3]`, yielding `[1,2,3]`.

The counterfactual checks are discriminating:

- a left-projection `fakeLeft(A,B) = A` can prove the generated associativity
  and right-identity target, demonstrating that the target alone does not fix
  operational meaning;
- that same `fakeLeft` is proved unequal to the candidate on
  `empty ++ [3]`, where frozen K semantics returns `[3]`; and
- a constant-empty operation is proved unable to satisfy the target.

Accordingly, the separate operational bridge check is load-bearing and passes:
the actual candidate is the exact frozen recursive operation, not the
convenient left projection that the equations alone would admit. The source
solution's `primes.append(candidate)` and the supplied heap-update rule use
this same `valSeqConcat` operation with a singleton right sequence.

Evidence: `evidence/OperationalBridgeAudit.lean`,
`evidence/10b_operational_bridge_tests_pass.log`, and
`evidence/audit_stage5_static.py`.

## Evidence index

`evidence/COMMANDS.md` records the principal exact commands and maps them to
their raw transcripts. Failed environment-diagnosis attempts are retained
rather than hidden; the successful preflight, source-only clean build, axiom
check, operational checks, static checks, and trusted mechanical gate are all
separately recorded.

VERDICT: PASS
LEGITIMACY: LEGIT
