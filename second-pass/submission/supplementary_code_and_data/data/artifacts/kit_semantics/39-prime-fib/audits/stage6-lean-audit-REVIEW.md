# Independent audit: `39-prime-fib`

## Result

I independently audited Stage 3 classification, deterministic Stage 4 generation, and the Stage 5 Lean proof for condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. The launcher and environment both select `CLASSIFICATION_AND_PROOF`. I did not accept the selected Stage 2 judgment, Stage 3 rationales, generated comments, candidate comments, or earlier PASS records as authoritative.

The reconstructed Stage 3 inventory is complete and correctly classified; the two genuine domain lemmas map bijectively to two exact, non-vacuous Stage 4 obligations; and the candidate builds from source, proves the fixed target with an allowed axiom set, and supplies operationally faithful definitions for all seven target parameters. The result is therefore PASS/LEGIT.

Raw commands and results are in `evidence/`. The most relevant records are `04_inventory_reconstruction.json`, `07_stage3_bijection.txt`, `16_check_generation_rerun.txt`, `20_hash_reconciliation.txt`, `22_obligation_target_reconciliation.txt`, `36_stage5_source_only_clean_build.txt`, `37_source_only_print_axioms.txt`, `38_candidate_target_static_reconciliation.txt`, `42_operational_oracle_results_rerun.txt`, `43_final_gate.txt`, and the fully captured copy/build replay `44_final_source_only_replay.txt`.

## Scope, mode, and provenance

`AUDIT_MODE` and `/audit-input.json` both report `CLASSIFICATION_AND_PROOF`; the problem, condition, and semantics mode are `39-prime-fib`, `kit-semantics`, and `SUPPLIED_SEMANTICS`.

Before judging generation, I directly hashed the two mounted producer files:

- `klean_export.py`: `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

Each hash exactly matches the producer source manifest and `generator-manifest.json`. The producer tree hash is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, matching `/audit-input.json`. The producer directory identity, source manifest, and generator manifest all bind the same immutable generator image ID, `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`. Thus there is no producer-source infrastructure error.

I independently recomputed all hashes for mounted objects recorded by the launcher: the discovery manifest, producer tree, K workspace artifact, frozen Stage 1 export, selected K audit, Stage 4 artifact, generated project, and Stage 5 workspace. All matched. I also checked all 771 individual Stage 1 source-hash entries: none was missing or mismatched. `lean_invocation_sha256` identifies a launcher-side execution directory that is not one of the mounted inputs, so that directory itself is not independently addressable here; its mounted Stage 5 workspace and sources were checked instead. Full values and algorithms are recorded in `evidence/20_hash_reconciliation.txt`.

## Stage 3 inventory reconstruction

I invoked the trusted local rule-inventory implementation against the frozen `/reference/k-proof`, not the protected classification. It reconstructed the local verification-module closure as `VERIFICATION-SYNTAX` plus `VERIFICATION`, with exactly 12 rules and whole-inventory hash:

`d277ae12725aaa26772d37930e9cbe9a7b2e0699b8289d37fe7be0befeac524a`

For every rule, I recomputed its module, line span, normalized text hash, and `source_rule_id`. Direct ordered comparison with `/reference/lemma-discovery.json` found equal counts, unique identities on both sides, equal order, no missing or extra identities, exact span text, and exact per-rule hashes. The comparison is bijective, not merely set inclusion.

My independent classifications are:

| Frozen span and identity | Classification | Independent reason |
|---|---|---|
| `25-40`, `rule-b140a59a2c7ac129f59c3ea9479e74b1afb69f96d459aeab91625b0a325f62e1` | `DEFINITION` | Expands the named source-level inner `while` macro. |
| `42-57`, `rule-ae138cf631c852c6689037278cdef752c08dc868bb22082ac057c01d37dfb043` | `DEFINITION` | Defines the corresponding internal `#while` proof term. |
| `59-75`, `rule-2eeee8218fa0f1ab3abdeb706b12f9b9c5caa3732a3901edbab9195bf216b5c7` | `DEFINITION` | Expands the named outer Fibonacci-search loop. |
| `77-93`, `rule-557c59673423be46fad688ff932860ebe8ffbf6a93b9b76798d9917cbf431255` | `DEFINITION` | Defines the corresponding outer `#while` proof term. |
| `95-104`, `rule-42b12587f50eda8ad9a9526c55e96494f2ebf4b50034495a0c8bc4fd6fd8abc4` | `DEFINITION` | Defines the exact initialization, outer loop, and return body. |
| `108-110`, `rule-ed39697ae845fca5c3929cc19f202f89ba72c9d726de3189a7db0165f7d66247` | `DEFINITION` | Base equation for the named `primeScan` summary. |
| `111-115`, `rule-3b0d654a52c07f36a2c8e03ab9a42adb2fbab342d609dc7963241a2fd2dd5c7f` | `DEFINITION` | Divisor case of the scan recurrence. |
| `116-120`, `rule-d1b2c3dd591d8a0aa4abb1a73970f1bbc7d8c61befd06b9e7e07e0ec88ca15a3` | `DEFINITION` | Non-divisor recurrence for the named scan summary. |
| `123-125`, `rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2` | `DOMAIN_LEMMA` | False-flag absorption is a mathematical consequence of the scan equations, not a defining case required to compute the scan. It is used by the source-relevant inner invariant because the loop never restores a cleared primality flag. |
| `129-131`, `rule-7add6c868057fde760e298599f3f04aca6b58a8f251dc5a65f962e218851c151` | `DEFINITION` | Base equation for the named remaining-search summary. |
| `132-139`, `rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f` | `DOMAIN_LEMMA` | The guarded one-step exit fact follows from the source loop update and is needed at the outer-loop boundary: once the next count reaches `N`, the updated `a` is `B`, which is returned. |
| `140-150`, `rule-88229ce3ed2cdd6dfe0c0cedf0411c4b335071c8bc4cd37ed184c0b6a9feaa02` | `DEFINITION` | Recursive equation for the remaining-search summary over one exact Fibonacci/primality step. |

Consequently the correct totals are 10 `DEFINITION`, zero `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and two `DOMAIN_LEMMA`. The local rules are named macros and summary equations rather than ordinary language-execution/observation rules. The Stage 1 proof script stages the inner and outer *claims*, but it never first proves any exact inventory rule against a module omitting that rule; therefore no inventory entry qualifies as `PROVED_DERIVED_LEMMA`. Both domain lemmas are materially tied to the frozen program and postcondition. Every `[simplification]` rule is either a definition or one of these two domain lemmas.

## Stage 4 generation and target

I reran the required trusted call `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the frozen Stage 1 workspace, protected discovery manifest, selected generation, and locked toolchain. It returned `status: PASS`, `obligation_count: 2`, the expected frozen input and generated-tree hashes, zero designated sorries, and successful clean/build diagnostics.

The container initially prevented Lean/Lake from resolving numeric `/proc/<pid>/exe` despite `/proc/self/exe` being available. I recorded that failed environmental attempt, then used an audit-only `readlink` shim limited to translating numeric `/proc/<pid>/exe` lookups to `/proc/self/exe`. Its source and behavior are in `evidence/15_lean_environment_fix.txt`; it does not alter candidate or generated files or Lean semantics. The rerun used the locked Lean 4.22.0 commit and passed.

Independent manifest reconciliation established:

- The independently classified domain IDs, obligation-map source IDs, and generated obligation IDs are the same two-element ordered list, with no duplicate.
- Both obligation conjunct hashes, frozen spans, normalized hashes, inventory hash, and discovery hash match.
- All seven parameter binding hashes recompute exactly and every bound `source_rule_id` exists.
- The obligation-map hash is `869bdee3d8a807bdc6f6cca51a54da2eab7ae53e4432f8e8e869ccadac373623`.
- The generated target is exactly `Klean39PrimeFib.Lemmas.targetStatement`; its definition hash is `2d48f8c99a053921560123488abafe8016e08223dec09b883b2b36c13406e1c9` and its instantiated-statement hash is `d1ac059479a94936bc9c9d49c554ae2ded44a051b8c0895dc7b6a0fc54caa49c` everywhere it is recorded.

The first conjunct is the exact guarded equation `D >= 2 -> primeScan(A,D,false) = false`. The second is the exact guarded one-step exit equation `primeFibSearch(N,C,A,B) = B`, preserving the frozen nested Boolean guard and the exact `#if primeScan(B,2,B>=2) #then 1 #else 0` count increment. Neither equality is reflexive or weakened. Both guards are satisfiable: for example, the first at `D=2,A=5`, and the second at `N=1,C=0,B=2` (with arbitrary `A`). The linter's “unused variable h” warnings merely reflect the normal implication encoding as `forall h : guard = true`; they do not make the guarded domains empty. Since the true domain set has size two, `KLEAN_NO_OBLIGATIONS` would have been illegitimate, but that status was not selected.

## Stage 5 clean build, target identity, and trust

I made a fresh source-only project at `/tmp/audit-work/stage5-source-only.9Aq6g7`, copied only the candidate source/configuration into it, and copied the immutable generated project as `Base`. I then repeated that construction at `/tmp/audit-work/stage5-final.vUvFvA` while capturing every copy and build command. No candidate `.lake` cache was reused. In both projects:

- `lake clean` exited 0.
- `lake build` exited 0 and rebuilt `Klean39PrimeFib.Lemmas` and `Proof`.
- The candidate source hashes match the mounted candidate.
- The `Base` target file is byte-identical to the selected generated target.

The candidate has no symlink/special-file trick, does not declare or shadow `targetStatement`, imports the exact generated Lemmas module, and contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. The independently extracted target in the fresh project exactly equals both the generator manifest and audit input.

`#check`, `#print Proof.final`, and a separate exact-type elaboration show that `Proof.final` proves the single fixed instantiated target, not a duplicate or alternate proposition. Its expanded term uses the supplied guard in each conjunct and the second proof takes the exact one-step branch.

The exact required output is:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

There is no `sorryAx`. The candidate adds no trust declaration. None of the 43 generated K collection/map allowlist axioms in `trust-inventory.json` is used by `Proof.final`. The three reported dependencies were independently printed at their Lean core declarations: `propext`, `Classical.choice`, and `Quot.sound`. They are precisely the standard core axioms explicitly allowed by the trusted final-gate implementation in addition to the generated inventory; there is no unrecorded dependency. The trusted `check_proof_candidate` cross-check also returned PASS with exactly these three dependencies.

## Operational bridge audit

The generated theorem alone is not enough to validate the seven parameter implementations. I demonstrated that sensitivity explicitly: deliberately dishonest `constantScan := false` and `projectionSearch ... B := B` definitions can satisfy the two structural conjuncts. This counterfactual Lean project builds, so the following independent comparison of the *actual* definitions is load-bearing.

For the five primitive parameters, the candidate definitions are exact: Boolean conjunction is `&&`; negation is `!`; integer `>=` and `<` are `decide` over Lean `Int`; and integer addition is Lean `Int` addition. These match their bound KORE symbols and the supplied operational K hooks over arbitrary-precision integers and booleans.

For `primeScan`, the candidate implements Python/K modulo as `tmod(tmod x y + y, y)`, exactly the frozen `pyMod` rule. Starting from `D >= 2`, it tests `d*d > a`, then divisibility, then increments `d`, preserving false absorption. Its fuel `a.toNat + 1` cannot expire on the guarded domain: negative `a` exits immediately at `d*d > a`, while nonnegative `a` needs fewer than `a+1` increments to exceed the square bound. The below-domain totalization is not reachable from the frozen summary guards.

For `primeFibSearch`, the state step is exactly the source outer body: `count` increases by 1 iff the updated Fibonacci value `B` passes the same scan, `a` becomes `b`, and `b` becomes `a+b`. The base branch returns `A` when `C >= N`; the one-step boundary returns `B`; and the remaining branch scans successor states until the first state whose count reaches the target. Although an arbitrary reachability witness supplies fuel, `firstReachedFibonacciValue` checks states in order, so the selected witness cannot change the first returned value. The fixed `0` cases only totalize invalid or genuinely divergent states, where the partial-correctness K summary has no terminating operational result; they do not replace behavior on the frozen source invariant `N>=1, C<N, A>=0, B>=1`.

I tested adversarial boundary values in Lean and also used an independently written Python operational oracle rather than reusing the proof term. Results were:

- 12,238 guarded scan cases, zero candidate/oracle mismatches and zero frozen-equation failures.
- 656 terminating search states, zero candidate/source mismatches and zero recurrence failures.
- 168 exact exit-boundary states, zero failures.
- The first ten returned prime Fibonacci values agree through `433494437`.
- Counterfactual constant scan, projection search, and reversed-divisibility mutations all disagree on concrete witnesses (`5` or target `2`).

Those finite checks support, but do not replace, the source-level semantic argument above. The actual definitions are neither constant, identity, hard-coded, vacuous, nor merely convenient witnesses for the generated equations.

## Final judgment

The Stage 3 classification is complete and mathematically correct; Stage 4 is producer-authentic, deterministic, bijective, and exact; and Stage 5 proves the unchanged generated theorem from clean sources with fully accounted trust and faithful operational bridges. I found no legitimacy defect.

VERDICT: PASS
LEGITIMACY: LEGIT
