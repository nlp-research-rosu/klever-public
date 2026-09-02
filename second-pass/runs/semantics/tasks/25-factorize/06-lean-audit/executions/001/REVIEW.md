# Independent Stage 3/4/5 Audit: HumanEval `25-factorize`

## Result

This audit passes the Stage 3 classification and the deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` generation. The launcher mode is
`CLASSIFICATION_ONLY` under `SUPPLIED_SEMANTICS`; Stage 5 is therefore correctly
absent.

I treated the mounted workspaces, manifests, logs, comments, and prior review as
untrusted evidence. I did not execute the Stage 1 `prove.sh`, prior-audit
scripts, or the generation-time producer sources. I used the trusted
`/reference/tools` inventory/preflight code and issued the K commands directly
against a fresh copy.

## Producer provenance gate

The mandatory producer-source gate passes:

| Binding | Recomputed value | Recorded values | Result |
|---|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | identical in `source-manifest.json` and `generator-manifest.json` | Match |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | identical in `source-manifest.json` and `generator-manifest.json` | Match |
| Generator image | `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000` | identical in the source manifest, generator manifest, and the producer-source path recorded by `/audit-input.json` | Match |
| Producer bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` | `/audit-input.json` | Match |

The bundle has exactly `klean.py`, `klean_export.py`, and
`source-manifest.json`. There is no producer-source infrastructure error.

## Recorded input and artifact hashes

All applicable recorded hashes were independently recomputed:

| Artifact | Recomputed hash | Result |
|---|---|---|
| Signed resolution JSON | `30068b0427ad3d79027fbcb0db04eb1dfcd195ee650679667a8175c6633f32bf` | Match |
| Stage 1 selected workspace tree | `f5c65bf898929655249d72de88d332bc3e1eaf5f1f33b27f0af3d523c92242c5` | Match |
| Frozen Stage 1 export | `4053db583b1d4c7220fb73349994cbff5625981bbe97bb2ab775a6571bb05cea` | Match |
| `verification.k` | `9f42fd722f59c575b9f684b6f4807263d94e9696c5ba336e97c45b2d24872fbf` | Match |
| Stage 3 manifest | `df6e518d644589682fc7b20376db22c9d8bc0d54c67a14ceff6d7cacf6045c84` | Match |
| Selected Stage 2 audit tree | `ea2b168199bb1cb651e45181de3b2706f0ea40dd2077380cd0b006e429eb41c2` | Match |
| Selected Stage 4 generation tree | `a66b7cf1beb69e91250efad37f187a50fcc2c450eace088b27fbfb4e805cd6b7` | Match |
| Generated project tree | `40da47d20e9ed83074f48716e2563406b1401d0002b22821404e5265e60384b2` | Match |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | Match |
| Trust inventory | `7168ec836f412e9478aec9912955f1c7570a0f6d4d4a72eeb348a5ea95b0dc15` | Match |

All 34 individual `stage1_source_hashes` entries match with no missing or
extra files. The pinned toolchain document exactly equals the generator
manifest's toolchain object: K/pyk `7.1.293` and Lean commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

## Inventory reconstruction

The trusted inventory selected
`FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA`, the last verification main module
named by the frozen proof procedure. Its local `verification.k` import closure
is exactly:

1. `FACTORIZE-VERIFICATION`
2. `FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA`

The reconstruction contains 11 rules. Each source span was re-extracted, each
normalized source hash was recomputed from `" ".join(text.split())`, and each
`source_rule_id` was reconstructed as `rule-<normalized_sha256>`. All 11 are
unique and self-consistent. The canonical whole-inventory hash is:

`2f8b212c17f86ce405005dc29a58c94ce010a10384580bdedeaa3c8b15778416`

That hash matches `lemma-discovery.json`, `input-manifest.json`, and
`generator-manifest.json`. The Stage 3 rule list has exactly the same 11 IDs in
the same order: no omission, duplicate, extra rule, reordered identity, changed
hash, or unaccounted classification exists.

## Independent classification

| Frozen span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 8–14 | `rule-7f8c42332f0b798eee0b216c19d5d737994c30bca58bf60acf82eff2cb615db0` | `DEFINITION` | Defines the named `factorizeStep` AST macro. |
| 17–21 | `rule-ff36487c2202b88e3202d1e6622812de6a27d82188e3b7999b6c7c7be54797e8` | `DEFINITION` | Defines the named `factorizeBody` AST macro. |
| 24–25 | `rule-7520d00b18cd44c15c8c66ee59da1729e0aff44a38220cce83690aca9918b78e` | `DEFINITION` | Defines the named `factorizeDef` AST macro. |
| 31–32 | `rule-974193eeb99c10573f8dab5154f95bf8f6117f8608a552dbe51b0d6bac94b0f2` | `DEFINITION` | Base equation of the `factorLoop` recurrence. |
| 33–37 | `rule-97414a2f1326ed4caaabdb270b8d32a516ce5379a17fe29c67b89403da76d3e2` | `DEFINITION` | Divisible branch of `factorLoop`. |
| 38–41 | `rule-fa4a22ace5a93a7480acd4a580108ddb030954fd16f84400b2af42a8ef019e7c` | `DEFINITION` | Nondivisible branch of `factorLoop`. |
| 44 | `rule-7abb5eb657f4bef944df578672058961f94b444760fa902d543029900e2f1d89` | `DEFINITION` | Names the recurrence initialized at divisor 2 and an empty accumulator. |
| 48–49 | `rule-00ba33f1d00d89a1287b827ed0e4d61a72208d9481e855799dfa084cc130eb8a` | `DEFINITION` | Base equation of the final-divisor recurrence. |
| 50–53 | `rule-8d7f72419f6087f2e87e0319302781f3a30793025cdfa8d56ddfd4880321eb43` | `DEFINITION` | Divisible branch of the final-divisor recurrence. |
| 54–57 | `rule-fb3e8c9a0714f588bbdcc8ba9d5615b6a66551f899d90d882938e80c7e105b1c` | `DEFINITION` | Nondivisible branch of the final-divisor recurrence. |
| 67–94 | `rule-7a0b234f2c7d2f2e9f5ca663b20c6f7b0d9cfa7eb71ea38b3a1681cb48235035` | `PROVED_DERIVED_LEMMA` | Exact separately proved loop-summary reachability claim, promoted only for the later entry proof. |

Thus the independent partition is:

- 10 `DEFINITION`
- 0 `OPERATIONAL_RULE`
- 1 `PROVED_DERIVED_LEMMA`
- 0 `DOMAIN_LEMMA`

There are no `simplification` attributes in the inventory, so the
simplification-class restriction is satisfied vacuously.

### Definitions and operational meaning

The first three rules name syntax already present verbatim in `solution.mpy`;
they do not skip execution. The remaining definition rules give two guarded
recurrences:

- `factorLoop` records the heap sequence and current `n`.
- `factorDivisor` records the final divisor needed by the complete loop-frame
  claim.

The guards are aligned with the supplied semantics. For `N > 1` and `D > 0`,
the divisible and nondivisible guards split on `pyMod(N,D) == 0`. The divisible
branch appends `D` and uses
`(N - pyMod(N,D)) /Int D`, exactly the supplied `//` rule. The other branch
increments `D`, exactly the source `AugAssign`. The `N <= 1` equations match
the supplied while-exit rule. Supplied list allocation/append, name lookup,
function-call framing, and return rules preserve the heap/result represented
by the recurrences.

As finite adversarial support, an independent source-algorithm implementation
and an independent recurrence implementation agreed for every integer
`1 <= N <= 500`, including `1`, repeated factors, odd squares, mixed factors,
and large primes. There were zero factor-sequence/final-divisor mismatches and
zero failures of sortedness, primality, or product reconstruction. The
machine-checked loop claim below is the universal evidence; this finite test is
not used as a substitute for it.

### Derived-lemma chronology and identity

After erasing only the sentence keyword and the promoted rule's
`priority(40), label(...)` metadata, the normalized configuration rewrite and
guard are byte-for-byte identical to `FACTORIZE-LOOP-SPEC.factorize-loop`.
The base `FACTORIZE-VERIFICATION` module does not import or contain the
promoted rule, and the loop spec imports only that base module.

The frozen procedure orders the base compile/loop proof before the
with-lemma compile/entry proof. I independently repeated those commands in a
fresh `/tmp/audit-work` copy:

```text
kompile verification.k --backend haskell \
  --main-module FACTORIZE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# exit 0

kprove spec.k --definition verification-kompiled \
  --spec-module FACTORIZE-LOOP-SPEC --output pretty
# #Top, exit 0

kompile verification.k --backend haskell \
  --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-lemma-kompiled
# exit 0

kprove spec.k --definition verification-with-lemma-kompiled \
  --spec-module FACTORIZE-SPEC --output pretty
# #Top, exit 0
```

This satisfies the special requirement for `PROVED_DERIVED_LEMMA`: the exact
semantic rule is first proved against a module that lacks it and is only then
used by the later proof.

## Deterministic Stage 4 generation

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and these
immutable inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The audit container initially exposed a PID-namespace incompatibility in Lean's
numeric `/proc/<pid>/exe` lookup, causing Lake to fail before checking the
project. I retained that raw failure. A narrowly scoped compatibility shim
translated only numeric `/proc/<pid>/exe` `readlink` requests to
`/proc/self/exe`; it changed no project or provenance file. Lean then reported
the exact pinned 4.22.0 commit, and the unmodified trusted preflight returned:

```text
lake clean
# exit 0

lake build
# Built Prelude, Sorts, Inj, Lemmas, Func, Rewrite, and Klean25Factorize
# Build completed successfully.
# exit 0
```

The returned evidence exactly equals both `preflight.json` and the preflight
record in `/audit-input.json`, including the empty clean output hash and the
build output hash
`e1f281f8580dcfb8d56d6e12cd47626784f6e863248a029b08a262ea28e48339`.

### Source-rule/obligation bijection

The independently established domain set is genuinely empty. The following
ordered lists are all exactly `[]`:

- independently classified `DOMAIN_LEMMA` IDs;
- `input-manifest.json` source rules;
- `generated/obligation-map.json` source rules;
- generated obligations; and
- trust parameters.

There are consequently no omitted, duplicated, irrelevant, weakened, or
vacuous conjuncts. The obligation-map hash matches the generator manifest, and
the generated-tree hash matches the generator manifest and audit input.

### Fixed target

The trusted target parser returns `null`. The generator manifest, stored
preflight, rerun preflight, and audit input all record a null target. An
independent scan finds no `targetStatement` or `Proof.final` declaration in any
generated Lean source.

This is the required fixed result for a genuinely empty domain set:
`KLEAN_NO_OBLIGATIONS`, no generated target, and no Stage 5 proof.

## Stage 5

Stage 5 checks are not applicable in `CLASSIFICATION_ONLY` mode.
`lean_workspace`, `lean_invocation`, and `stage5_result` are null;
`/candidate` is absent; and the generated project contains no `Proof.lean`.
Therefore no clean candidate build, `#print axioms Proof.final`, candidate
shadowing check, or operational-bridge parameter audit is required or possible.

## Evidence index

Raw commands, outputs, and exit codes are under `/audit-output/evidence/`:

- `01_inspect_inputs.*` — mounted inputs, manifests, frozen sources, and mode.
- `02_provenance_and_inventory.*` — producer gate, tree/file hashes, canonical
  inventory, spans, normalized hashes, IDs, and Stage 3 bijection.
- `03_hash_and_lemma_identity.*` — all Stage 1 source hashes, signed resolution,
  toolchain, exact claim/rule identity, module exclusion, and command order.
- `04_stage1_derived_lemma_recheck.*` — fresh direct K compiles and both `#Top`
  proofs.
- `05_stage4_preflight*` and `proc_self_exe_compat.c` — initial infrastructure
  failure, environment diagnosis/fix, complete Lake output, and returned
  trusted preflight evidence.
- `06_semantic_classification.*` — supplied operational rules, independent
  classification ledger, and adversarial correspondence checks.
- `07_stage4_independent_gate.*` — partition equality, empty bijection, hash
  bindings, target identity, status consistency, and Stage 5 absence.

VERDICT: PASS
LEGITIMACY: LEGIT
