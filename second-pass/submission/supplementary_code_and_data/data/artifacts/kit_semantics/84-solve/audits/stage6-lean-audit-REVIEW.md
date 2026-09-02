# Independent audit: HumanEval `84-solve`

## Scope and result

The launcher and environment both record:

- mode: `CLASSIFICATION_AND_PROOF`
- condition: `kit-semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- problem: `84-solve`

I treated the mounted candidate, manifests, prior audit, logs, and comments as
untrusted evidence. I did not adopt the prior Stage 2 verdict or the protected
Stage 3 classifications. The trusted mechanical final gate reports
`semantic_classification: NOT_EVALUATED`; the semantic classification and
operational-bridge judgments below are my independent judgments.

The Stage 3 classification is correct, Stage 4 is a deterministic and exact
two-obligation export, and `Proof.final` proves the fixed target with honest
implementations of every target parameter on the complete source-rule match
domain.

## Input and producer integrity

Before evaluating Stage 4, I hashed the exact mounted producer sources:

| Producer input | Recomputed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same in the source manifest and generator manifest |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same in the source manifest and generator manifest |
| producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` | same in `/audit-input.json` |

The source manifest and generator manifest both name immutable generator image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
That digest is also the basename of the generation-producer source path
recorded by the launcher. Producer provenance therefore passes; there is no
producer-source infrastructure error.

I also recomputed the mounted tree/file hashes with the trusted digest
implementations:

| Object | Recomputed hash | Result |
|---|---|---|
| complete Stage 1 workspace | `4327c645ee227e6b4318cf51f00f495bde2d78ff108346974de9af124951dfc9` | matches audit input |
| frozen Stage 1 export | `05f4cd352f7808cf382474c311a0a2b5d3f9be3dd8c46e73708beedf975f99ac` | matches all Stage 4 records |
| Stage 2 audit tree | `e27f4bf52c7d6f3955082c7a1d5f5d7513623f6d915378a2d3883c26e8665904` | matches audit input; its verdict was not trusted |
| Stage 3 manifest | `08c8de9b2956fc1015b2d3f8951562cc0bf741644ff225073a8c1460cebef18c` | matches all records |
| Stage 4 generation tree | `8abb2e745df592e2c4573a0627e3f3517aba89fcd8a3d753c3548cfd5f2ac989` | matches audit input |
| generated Lean tree | `648a8799520af2511f3d8d694d1e92d6cf9a539a329e3e15a503d73669e2292d` | matches generator, export result, preflight, and audit input |
| Stage 5 candidate tree | `4d31faa5a9e2348540e5bc88e683322d92107b5a68117c0a0f6b7c7524a32bc8` | matches audit input |

All 816 regular Stage 1 files were present, there were no extras, and every
per-file hash in `stage1_source_hashes` matched. The launcher-only Stage 5
invocation directory is not mounted independently, so its invocation-tree hash
could not be recomputed; it is not used as proof evidence. The mounted Stage 5
workspace itself was independently hashed as shown above.

## Stage 3 inventory reconstruction

I called
`tools.k_rule_inventory.inventory_verification(/reference/k-proof)` with
`PYTHONPATH=/reference`. The trusted parser selected module `VERIFICATION`;
its local module closure is exactly `["VERIFICATION"]`. It reconstructed 11
rules from `verification.k` with:

- `verification_sha256`:
  `4af5ad7c9891e293399b7c756155ffdc871d165436935dee72a9ad89a6a9fb4d`
- `inventory_sha256`:
  `0d280d2436eed6d6d7b88857c60dfbe7ccf942ecf8cc442fa068cb3e4b47e6c2`

For every entry, the `source_rule_id` suffix equals the independently
recomputed normalized source hash. The protected manifest has the same 11
identities in the same order, with no omitted, extra, or duplicated identity.
The source spans, attributes, normalized hashes, and source text also match
bijectively.

My independent classification is:

| Order | Source rule ID | Span | Classification | Semantic judgment |
|---:|---|---:|---|---|
| 1 | `rule-dabe5596b9af337f8a3164e47c3cfc9c95ac77a7f0264e301a20c92506acca00` | 10–95 | `DEFINITION` | `solutionModule` names the exact program AST; expansion supplies a named proof term and does not bypass execution of that AST. |
| 2 | `rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a` | 100–102 | `DOMAIN_LEMMA` | Guarded arithmetic fact for the expanded Python remainder operation; it rewrites built-in arithmetic and is not a named summary. |
| 3 | `rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d` | 103–105 | `DOMAIN_LEMMA` | Guarded arithmetic fact for the expanded Python floor-division operation; it rewrites built-in arithmetic and is not a named summary. |
| 4 | `rule-4919db5997cb25213b3ce98a76a6388b59df5563a22cfed932df4735a6ada343` | 109 | `DEFINITION` | Base equation for `decodeBin`. |
| 5 | `rule-029a575b73486388e10fb475acdaa1c76ca37368761dae92ed2d68bb1867892f` | 110–111 | `DEFINITION` | Structurally recursive `decodeBin` equation. |
| 6 | `rule-f2aba656d92faee38fea90204e6da2354ebcd914af1f55350da58939351da8e7` | 114 | `DEFINITION` | Base equation for `allBinDigits`. |
| 7 | `rule-41b4ad77e7eb08d36e9936dfae668eb2aaabf4d1b688374fb8aa3dc01a172ded` | 115–116 | `DEFINITION` | Structurally recursive `allBinDigits` equation. |
| 8 | `rule-aa7e0002a3407b5d4b867e2d6bc75311639f1ebc558615aef42627e335282198` | 120 | `DEFINITION` | Canonical binary zero case. |
| 9 | `rule-5545f7cabeaaacdd260458c643ec6a2bf61709a3bd4df73bd5c83a82a0344b84` | 121 | `DEFINITION` | Canonical nonzero binary recurrence through `allBinDigits`. |
| 10 | `rule-7475c26cae009c85998c0c5a72c4d4421a9a2f44657a413aca401a947f1e1b24` | 122 | `DEFINITION` | Exhaustive `owise` fallback completing `canonicalBin`. |
| 11 | `rule-983c37ae659da6b7c7eb71a96580a3332dd4fa37b9eb2a0a0e5f23e7c4c2b339` | 126–139 | `DEFINITION` | Named predicate defining the exact decimal-digit parameterization of `0..10000`. |

There are nine definitions, two domain lemmas, no ordinary operational rules,
and no proved-derived-lemma classification. Both rules carrying
`[simplification]` are domain lemmas, satisfying the mandatory constraint that
a simplification be either `DEFINITION` or `DOMAIN_LEMMA`. Although Stage 1
contains separate bridge-free arithmetic claims, these two installed
simplifications must remain `DOMAIN_LEMMA`; they cannot be relabeled
`PROVED_DERIVED_LEMMA`.

The domain lemmas are true and relevant. The frozen operational semantics maps
source `%` to `pyMod(I1,I2) = ((I1 %Int I2) +Int I2) %Int I2` and source `//`
to `(I1 -Int pyMod(I1,I2)) /Int I2`. The source program repeatedly evaluates
`N % 10` and `N // 10`. For `N = D + 10Q` and `0 <= D < 10`, the first lemma
extracts `D`, and the second reduces the remaining quotient to `Q`. Neither
lemma is an irrelevant human-facing theorem smuggled into the proof.

## Deterministic Stage 4 generation

I reran the required trusted function:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

It returned `status: PASS`, `obligation_count: 2`,
`trust_declaration_count: 42`, and zero designated sorries. Its clean and build
subcommands both exited 0. The returned JSON is saved verbatim as
`evidence/preflight-returned-evidence.json`.

The first invocation exposed a container PID-namespace defect: Lean asks for
`/proc/<getpid()>/exe`, while only `/proc/self/exe` exists in this audit
namespace. The initial failure is preserved. I compiled the narrow
`proc_exe_compat.c` preload shim, which redirects only that path lookup to
`/proc/self/exe`; it does not alter Lean input, elaboration, terms, project
files, or proof checking. With the shim, `lean --version` reported the pinned
Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, the frozen toolchain gate passed,
and both the preflight and final mechanical gate completed.

The independently classified domain set is exactly:

1. `rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a`
2. `rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d`

`obligation-map.json` contains exactly those two source rules and exactly one
obligation for each, in that order. There are no duplicate or extra
obligations. Its raw hash
`1d62be15b7bc340479aac8c4bf0891e821e00a3088c798f7a2c76910fa86796d`
matches the generator manifest. Each obligation repeats the correct source
span, normalized hash, inventory hash, and discovery-manifest hash; each
`lean_conjunct_sha256` recomputes correctly.

Mathematically, the generated target is exactly:

- for every integer `Q` and digit `D`, under `0 <= D < 10`,
  `tmod(tmod(D + 10*Q, 10) + 10, 10) = D`; and
- for every integer `D,Q`, under the same digit guard,
  `tdiv((D + 10*Q) - D, 10) = Q`.

These are exact translations of lines 100–105, including the guard and
truncating K integer operators. The guard is satisfiable (for example `D = 0`
or `D = 9`). The second equality is valid even without its guard, which
explains the generated unused-variable warning, but retaining the frozen
guard is exact rather than a weakening. Neither conjunct is vacuous.

The fixed target recomputed from the mounted generation is:

- declaration: `Klean84Solve.Lemmas.targetStatement`
- file: `Klean84Solve/Lemmas.lean`
- statement hash:
  `879f69bb72fb8360edda9e28b94f2006e262af4917bb6ab5a9bd818d529c5214`
- definition hash:
  `9053009b1d9ce443e5d1f56d52cceda9531c9f50a8f3e27f927ed16db241eb95`

The declaration, statement, definition, hashes, eight parameter bindings, and
their source-rule ID lists match the generator manifest, audit input, recorded
preflight, rerun preflight, and fresh Base copy. This generation is not
`KLEAN_NO_OBLIGATIONS`; the true domain set is nonempty and the two obligations
are present.

## Stage 5 proof and target identity

I made the fresh workspace
`/tmp/audit-work/84-solve-proof-audit-2`, copied the immutable generated project
into it as `Base`, and ran both `lake clean` and `lake build`. Both exited 0;
the only diagnostics were two unused-guard linter warnings in the immutable
generated target. The trusted Stage 5 mechanical check and the full
`klean_final_gate.py` also returned `status: PASS`.

The fresh Base has the same 12 non-build files as the immutable generated
project, with no missing, extra, or changed source file. The candidate source
copy matches the mounted candidate. Outside Base there is no
`targetStatement` declaration or `Klean84Solve.Lemmas` namespace, and exactly
one `theorem final` exists. The candidate has no `sorry`, `admit`, `unsafe`,
new `axiom`, or new `opaque`.

`#print Proof.final` reports precisely:

```text
theorem Proof.final :
  Klean84Solve.Lemmas.targetStatement
    Proof.«_-Int_» Proof._andBool_ Proof.«_<Int_» Proof.«_<=Int_»
    Proof.«_%Int_» Proof.«_+Int_» Proof.«_/Int_» Proof.«_*Int_»
```

Thus `Proof.final` proves the one fixed generated theorem applied to the eight
candidate bindings; it does not prove a duplicate, shadow, weakened, or
candidate-authored target.

## Axiom accounting

The exact independent output of `#print axioms Proof.final` is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are the three ambient Lean core axioms explicitly permitted by the
trusted final-gate policy. The generated `trust-inventory.json` contains 42
named generated declarations; none appears in the dependency list.
`sorryAx` is absent, there is no unexpected axiom, and the candidate introduced
no trust declaration. Every reported dependency is therefore accounted for:
three standard Lean kernel/library trust primitives and zero generated Klean
trust axioms.

## Operational-bridge audit

The frozen compiled KORE binds the eight target symbols to these hooks, and the
candidate definitions are:

| KORE symbol / hook | Candidate definition | Judgment |
|---|---|---|
| `Lbl'Unds'-Int'Unds'` / `INT.sub` | `x - y` | exact integer subtraction |
| `Lbl'Unds'andBool'Unds'` / `BOOL.and` | `x && y` | exact Boolean conjunction |
| `Lbl'Unds-LT-'Int'Unds'` / `INT.lt` | `decide (x < y)` | exact Boolean-valued strict comparison |
| `Lbl'Unds-LT-Eqls'Int'Unds'` / `INT.le` | `decide (x ≤ y)` | exact Boolean-valued non-strict comparison |
| `Lbl'UndsPerc'Int'Unds'` / `INT.tmod` | `Int.tmod x y` | exact truncating remainder |
| `Lbl'UndsPlus'Int'Unds'` / `INT.add` | `x + y` | exact integer addition |
| `Lbl'UndsSlsh'Int'Unds'` / `INT.tdiv` | `Int.tdiv x y` | exact truncating division |
| `Lbl'UndsStar'Int'Unds'` / `INT.mul` | `x * y` | exact integer multiplication |

Generated `SortInt` and `SortBool` are respectively Lean `Int` and `Bool`, so
there is no representation bridge hidden in this table. K's `tmod` and `tdiv`
hooks are partial at a zero divisor, whereas the target asks for total Lean
parameters. Every occurrence bound by the two source-rule IDs has literal
divisor `10`; the candidate agrees with K over that complete match domain.
Values assigned by Lean outside that unreachable zero-divisor domain cannot
affect either obligation.

I compiled an independent K integer oracle and compared it with the candidate
on boundary and adversarial values. Both sides produced:

- `7 - 12 = -5`, `7 + (-12) = -5`, and `(-7) * (-3) = 21`;
- the full tested Boolean conjunction and comparison boundaries;
- `tmod(-7,10) = -7`, `tmod(-13,10) = -3`,
  `tmod(13,10) = 3`; and
- `tdiv(-7,10) = 0`, `tdiv(-13,10) = -1`,
  `tdiv(13,10) = 1`.

The negative cases are load-bearing: counterfactual Euclidean definitions
produce `(-7) % 10 = 3` and `(-7) / 10 = -1`, unlike the frozen K hooks. This
also demonstrates why the clean Lean theorem alone is insufficient: the fixed
equations do not distinguish every convenient interpretation, but the
operational bridge audit does.

For obligation-level adversarial checks, both conjuncts evaluated true at
`Q ∈ {-100,-1,0,100}` and digit boundaries `D ∈ {0,9}`. A
constant-false conjunction would make the premise vacuous, and an identity
subtraction fails at `D = 9,Q = -1`; the actual definitions are neither.
Finally, changing the first result at the satisfiable witness `D = 0,Q = 0`
from `0` to `1` was rejected by Lean with exit code 1. The proof is therefore
result-constraining and non-vacuous.

## Evidence

The command record is in `evidence/COMMANDS.md`. Principal raw results are:

- `evidence/reconstructed-inventory.json` and
  `evidence/01_inventory_audit.log`
- `evidence/02_run_preflight.log`,
  `evidence/02_run_preflight_rerun.log`, and
  `evidence/preflight-returned-evidence.json`
- `evidence/03_integrity_audit.log`
- `evidence/04_fresh_lake_clean_build_final.log`
- `evidence/05_stage5_mechanical_check.log` and
  `evidence/12_klean_final_gate.log`
- `evidence/06_print_axioms.log`,
  `evidence/07_print_final.log`, and
  `evidence/15_axiom_reconcile.log`
- `evidence/09_operational_bridge_k.log`,
  `evidence/10_operational_bridge_lean.log`,
  `evidence/11_kore_hooks.log`, and
  `evidence/14_obligation_adversarial.log`
- `evidence/13_candidate_source_audit.log` and
  `evidence/16_false_mutation.log`

VERDICT: PASS
LEGITIMACY: LEGIT
