# Independent audit: HumanEval 110-exchange

## Outcome

The Stage 3 classification is complete and semantically correct, the selected
Stage 4 generation is deterministic and binds exactly the five genuine domain
lemmas, and the Stage 5 candidate proves the immutable target with honest
operational definitions and no unaccounted proof trust. The audit mode was
`CLASSIFICATION_AND_PROOF` in both `AUDIT_MODE` and `/audit-input.json`;
the semantics mode was `SUPPLIED_SEMANTICS`.

I treated all mounted candidate, provenance, review, comment, and log content
as untrusted evidence. I did not rely on the previous Stage 2 verdict or any
earlier PASS marker. Commands and complete results are indexed in
`evidence/COMMANDS.md`.

## Producer provenance gate

This gate passed before I judged Stage 4:

- observed `klean_export.py` SHA-256:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`;
- observed `klean.py` SHA-256:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`;
- immutable generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`;
- producer-bundle tree SHA-256:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`.

The two file hashes match `generator-manifest.json` and
`source-manifest.json`. The source manifest contains exactly those two producer
files, its own manifest, and no extra files. Its image ID matches the generator
manifest and the image-key component of the producer path recorded in
`/audit-input.json`. The bundle tree hash matches the audit input. Thus there
is no producer-source infrastructure error. Raw results are in
`evidence/producer-file-hashes.txt`, `evidence/hash-values.txt`, and
`evidence/structural-hash-checks.json`.

## Frozen-input and inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`, rather than copying the protected discovery inventory.
It selected verification module `VERIFICATION` and reconstructed the local
closure in source order as:

1. `VERIFICATION-BASE`
2. `VERIFICATION`

The reconstruction contains 37 rules. For every rule, the reconstructed module,
start/end source span, normalized source SHA-256, `source_rule_id`, attributes,
and exact source text match the corresponding frozen source. The reconstructed
`verification.k` byte hash is
`382e4280ca967bb2f61ae9ab29a6e6c8f6c99378c875bf85d1817871f6fcc23d`;
the canonical whole-inventory hash is
`28f7d11cd40b6c85cf800f361b0188ccab45c2024b37a26f522ded53d34dd534`.

The 37 protected discovery identities are in the exact same order as the
canonical inventory and are unique. There are no missing, extra, duplicated,
or reordered identities. The protected inventory hash and the inventory hash
recorded by Stage 4 both equal the reconstruction. The complete independent
inventory is `evidence/reconstructed-inventory.json`; the per-rule comparison
is `evidence/classification-audit.txt`.

I also independently rehashed all mounted artifacts bound by the launcher:

- Stage 1 pipeline tree:
  `94260d2db16cf846f8a36e8dc5504a95ccd82fed5d3c3d3a9c6485d022bc7659`;
- Stage 1 exporter tree:
  `7171a3f1e6c7e09092d2c8e8bb377f61f3009ee901e8e881ec8a23afdc0d1aad`;
- Stage 3 discovery bytes:
  `cc1e1db833330f9d4c5ba1be8887b0fc8af00b367d0ac32f61bac9f2cd43685c`;
- selected Stage 2 audit tree:
  `ac95401d6ce5df57b1365e5b85c92ae3ea69502c0213d51bd761b0bb2a9d34bb`;
- selected Stage 4 generation tree:
  `a2297a9b3498f971cb0c52af875b527636ade653656982a14b33735e6a247af5`;
- generated project tree:
  `5ed9171d90541d603cdb4419005e3a212f2a5dc6ba8d60464ec66650a0d53bee`;
- Stage 5 candidate tree:
  `cf9ef421df3f685001f4eb5fd31eac2f2548fa5a0733128a9c742c66ecdf426b`.

Every Stage 1 per-file source hash in `/audit-input.json` also matches, with no
unaccounted regular file. The launcher-recorded Stage 5 invocation directory
itself is not a mounted audit input; I did not rely on it or claim to rehash it.

## Independent Stage 3 classification

My independent counts are:

| Class | Count | Frozen rules |
|---|---:|---|
| `DEFINITION` | 29 | Lines 9–35, 41, 50–58, 61, 70–78, 81, 90–98, 103–104, 111–152 |
| `OPERATIONAL_RULE` | 3 | Lines 106–108 |
| `PROVED_DERIVED_LEMMA` | 0 | None |
| `DOMAIN_LEMMA` | 5 | Lines 46–48, 66–68, 86–88, 161–166 |

The 29 definitions are all genuinely definitional:

- three macros name the exact loop body, function body, and program module;
- the Int, Bool, and Float families define their projection-domain predicates
  and named total projection terms;
- `boolToInt` is exhaustively defined on both Boolean constructors;
- `isNumberVal` and `allNumbers` define the represented numeric domain;
- `numberEven`, `evenCount`, and `exchangeResult` define the parity summary,
  its recurrence, and the final result summary.

The projection orientation and idempotence rules remain definitions because
they define the named total proof terms and their structural normal forms; they
do not assert the program's human-facing result.

The three operational rules are ordinary dispatch/observation rules, not domain
facts:

- Bool `% 2` uses Python's integer interpretation of Bool;
- Float `% 2` promotes the literal divisor to `2.0` and invokes the supplied
  floor-based `floatMod`;
- Float `== 0` observes the supplied mixed Float/Int equality at the concrete
  promoted zero.

They are sort- and literal-specific execution cases. They do not carry a
`simplification` attribute and do not state the desired postcondition.

The five domain lemmas are exactly the unproved logical facts:

- definedness of the partial Int, Bool, and Float projections;
- equivalence of the source expression `V % 2 == 0` with `numberEven(V)` over
  the represented numeric union;
- definedness of `% 2` over that union.

The three per-sort claims in `connection-spec.k` are related evidence, but Stage
1 never first proves the exact guarded `Val`-sorted rule at lines 161–163
against a module omitting it and then uses that exact rule later. It therefore
cannot be labeled `PROVED_DERIVED_LEMMA`; `DOMAIN_LEMMA` is correct. The
definedness rule at lines 164–166 is likewise not separately proved.

All five domain lemmas are relevant. The source loop evaluates `% 2 == 0` on
each dynamic list head, and the postcondition counts exactly those even heads.
The projection lemmas are load-bearing for the three represented numeric
branches of `numberEven`; the last two rules directly characterize and establish
definedness of the source condition. There is no irrelevant domain fact.

Every rule with `simplification` or `simplification(10)` is classified as
either `DEFINITION` or `DOMAIN_LEMMA`; none is classified operational or
derived.

## Stage 4 deterministic generation

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required frozen paths. It returned `PASS`, rebuilt the generated project
after `lake clean`, and reported:

- obligation count: 5;
- generated trust declarations: 55;
- designated sorry count: 0;
- generated-project hash:
  `5ed9171d90541d603cdb4419005e3a212f2a5dc6ba8d60464ec66650a0d53bee`.

The returned evidence is `evidence/stage4-check-generation.json`.

The source-rule/obligation mapping is an exact ordered bijection:

| Source rule | Generated mathematical obligation |
|---|---|
| `rule-0312858…` | Int projection is defined iff `definedProjectInt(V) = true` |
| `rule-e1f0f7d…` | Bool projection is defined iff `definedProjectBool(V) = true` |
| `rule-57727b2…` | Float projection is defined iff `definedProjectFloat(V) = true` |
| `rule-f297fbc…` | `% 2` followed by `== 0` equals `numberEven(V)` under `isNumberVal(V) = true` |
| `rule-4ec80ff…` | `% 2` returns `some` under `isNumberVal(V) = true` |

The ordered source IDs in the protected discovery, Stage 4 input manifest,
`obligation-map.json` source rules, and generated obligations are identical.
There are five distinct IDs and five obligations. Each obligation's source
span, normalized hash, inventory hash, discovery hash, conjunct text, and
conjunct hash recompute exactly. The obligation-map byte hash is
`f67b4905e17dcea19e3b7716c541f05647128648346ed1d1eec683b95cda2ee5`.

The `True` in each projection obligation is the faithful translation of
`#Ceil(V)` for an already sorted `V : SortVal`; it does not replace the
load-bearing projection predicate. Similarly, the final obligation translates
the K right side `#Top` to `True` while preserving both the definedness query
and the satisfiable numeric guard. The guard is not vacuous under the candidate:
Int, Bool, and Float constructors all satisfy it, as checked below. No
obligation is irrelevant, duplicated, weakened, or replaced with a vacuous
proposition.

This is not a `KLEAN_NO_OBLIGATIONS` case: the independently reconstructed
domain set has five entries, a generated target exists, and proof mode is
required.

## Fixed target identity

The generated target is exactly:

- declaration: `Klean110Exchange.Lemmas.targetStatement`;
- file: `Klean110Exchange/Lemmas.lean`;
- 11 ordered trust parameters;
- statement SHA-256:
  `e655b15313d029f205543a48d89b78a7835fbfc530bef57835eb0935bb3713da`;
- definition SHA-256:
  `16c191f938c9dba6a3320977a8a7815e1f3ea971f811b5ece516cde3cdc9f7e2`.

The trusted exporter recomputed every parameter binding hash from its KORE
symbol, Lean name/type, and exact source-rule ID list. The parsed target equals
the generator manifest and `/audit-input.json` byte-for-byte at the structured
target level. Reconstructing the expected target definition from the five
mapped conjuncts produces the same definition hash.

The fresh `Base/Klean110Exchange/Lemmas.lean` is byte-identical to the selected
generated file; both have SHA-256
`3ccde69aa85de7bf995f130bd3842d25dd1608fbadc6fc62fcff00dbff68e5a1`.
The candidate defines no `targetStatement` and does not shadow or modify the
target. See `evidence/candidate-integrity.txt`.

## Stage 5 clean build and proof identity

I made a fresh project at `/tmp/audit-work/lean-proof-audit-final`, copied the
candidate into it, and copied the selected generated project into it as
`Base`. I then ran both required commands:

- `lake clean`: exit 0, complete output in `evidence/lean-clean.log`;
- `lake build`: exit 0, complete output in `evidence/lean-build.log`.

The build compiled `Klean110Exchange.Lemmas`, `Proof.Dispatch`, and `Proof`, and
ended with `Build completed successfully.` The only warnings are the immutable
target's two unused guard variables.

The candidate has exactly one definition for each of the 11 ordered target
parameters and exactly one theorem `Proof.final`. Its theorem type is the exact
manifest statement, using those definitions in the exact target order; it is
not a duplicate, reformulation, weakened theorem, or vacuous variant. The
trusted independent Stage 5 checker also returned `PASS` in
`evidence/stage5-mechanical-check.json`.

An explicit scan of every candidate Lean source found no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque`. There are no candidate-created proof
assumptions.

## Axiom accounting

I ran Lean on an audit source containing the literal command
`#print axioms Proof.final`. Its exact output is in
`evidence/lean-axioms.log`:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. None of the 55 Klean-generated executable trust
declarations in `trust-inventory.json` occurs in the dependency list. The three
reported names are the standard Lean baseline explicitly admitted by the
trusted final-gate checker (`propext`, `Classical.choice`, and `Quot.sound`);
they are not candidate declarations or hidden K propositions. Thus the used
dependency set is fully reconciled: generated allowlist dependencies used by
the proof are empty, standard checker-baseline dependencies are exactly those
three, and there is no unrecorded candidate proof escape.

## Operational-bridge audit of all target parameters

I located and checked every exact candidate definition:

| Target parameter | Candidate implementation | Frozen meaning and judgment |
|---|---|---|
| `applyBin` | `ProofModel.applyBin` over `applyBin?` | Exact total wrapper around the frozen dispatch table; on the target domain it executes Int, Bool, or Float `% 2` and never takes the default |
| `applyCmp` | `ProofModel.applyCmp` over `applyCmp?` | Exact target path uses Int `== 0` or the specialized Float/Int-zero observation |
| `definedProjectBool` | Bool-constructor recognizer | Matches `definedProjectBool(V) => isBool(V)` |
| `definedProjectFloat` | Float-constructor recognizer | Matches `definedProjectFloat(V) => isFloat(V)` |
| `definedProjectInt` | Int-constructor recognizer | Matches `definedProjectInt(V) => isInt(V)` |
| `isNumberVal` | Int/Bool/Float constructor union | Matches the three-way K definition; nonnumeric constructors are false |
| `numberEven` | Constructor split using Int parity, Bool-to-Int parity, and Float parity | Matches the complete K definition at lines 126–134 |
| `applyBin?` | Option-valued frozen dispatch table | Returns `some` for all three numeric `% 2` cases and records undefined cases as `none` |
| `project:Bool?` | K-sequence projection of injected Bool | Accepts exactly Bool injection and rejects other K terms |
| `project:Float?` | K-sequence projection of injected Float | Accepts exactly Float injection and rejects other K terms |
| `project:Int?` | K-sequence projection of injected Int | Accepts exactly Int injection and rejects other K terms |

The arithmetic bridge is substantive, not convenient:

- `pyMod(x,m)` is exactly `((x %Int m) +Int m) %Int m`, using truncated
  remainders as in the frozen K rule;
- Bool maps exhaustively to `0` or `1`;
- Float modulo is exactly
  `x - floor(x / modulus) * modulus`, with divisor `2.0`;
- Float equality uses the generated `SortFloat`/Lean `Float` equality, and the
  specialized mixed-zero case uses `0.0`;
- the Option-valued table carries the K partiality/definedness boundary; the
  total wrapper's `noneV`/`false` defaults occur only where no frozen dispatch
  rule applies and are not used by either guarded target obligation.

The definitions therefore implement the frozen operation on the complete
match domain of the five obligations. They are not constant, identity,
hard-coded to the theorem result, or made vacuous by a false domain predicate.

I checked adversarial witnesses in three independent ways:

- Lean evaluated negative Ints, both Bools, negative integral and non-integral
  Floats, a nonnumeric value, and successful/failed projections; the output is
  `evidence/lean-operational-audit.log`.
- An independently written Python oracle produced the same parities and full
  `exchange` results; see `evidence/python-operational-oracle.log`.
- A fresh LLVM compilation of the frozen K definition executed five mixed,
  negative, Bool, and Float program cases to `.K`, `NoExc`, and exit code 0;
  see `evidence/k-adversarial-run.log`.

The Lean audit source also proves that identity `applyBin`, constant-false
parity, a hard-coded-zero result, and a constant-false numeric-domain predicate
disagree with the honest bridge on satisfiable witnesses. Separately, mutating
both source conditions from `% 2 == 0` to `% 2 == 1` makes the fixed expected
result fail under fresh K execution with `AssertionError` and exit code 1
(`evidence/k-counterfactual-odd-mutation.log`). These checks confirm both result
sensitivity and program-body sensitivity.

## Final judgment

All structural, classification, mathematical-obligation, target-identity,
build, axiom, and operational-bridge gates pass. The one environment wrinkle
was Lean 4.22's use of `/proc/<getpid>/exe` in a PID namespace whose numeric PID
is not mounted in `/proc`; a narrow audit-only preload redirected that lookup
to `/proc/self/exe`. The shim was validated against the pinned Lean commit and
did not alter candidate or generated sources. It is documented in
`evidence/COMMANDS.md` and `evidence/proc_self_exe_shim.c`.

VERDICT: PASS
LEGITIMACY: LEGIT
