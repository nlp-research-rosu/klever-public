# Independent audit: HumanEval 108-count-nums

## Result

The protected Stage 3 classification is complete and mathematically correct,
and the selected Stage 4 generation is authenticated, deterministic, and
bijective with the five true domain lemmas. The generated Lean target is
unchanged, and the Stage 5 candidate cleanly builds and proves that exact
target with only Lean's foundational `propext` axiom.

The overall result nevertheless fails. Three Stage 5 public definitions claim
the total meaning of a full KORE dispatcher symbol but implement only the
single dispatcher case needed by the generated equations. Concrete
counterexamples from the frozen supplied semantics show that the definitions
of `applyCmp`, `applyUn`, and `applyBuiltin` return the wrong value on other
specified cases of those same symbols. This is the operational-bridge failure
the audit instructions require me to reject; a clean theorem about the narrow
generated equations does not repair it.

The audit mode was `CLASSIFICATION_AND_PROOF` in both `AUDIT_MODE` and
`/audit-input.json`.

## Frozen inputs and producer authentication

I treated all mounted candidate and provenance content as untrusted evidence.
The trusted hashing and inventory implementations came from `/reference/tools`.

The mounted Stage 1 tree contained exactly the 815 files recorded in the audit
input: no missing, extra, or mismatched file was found. Its pipeline tree hash
was
`4817cd494240566a67a8dec838fbc5ad4ae18ab19af49eb5fbde283cd71510d6`;
`verification.k` was
`a6a57397f1b7f6b856df6012dcde84159e0506d8875f11edbc0f76579f1f57c0`.
The independently recomputed Stage 4 frozen-input hash was
`0b9500be5f09a202d093efad9f8c820dad7639990a3e7d69afd52dff5c55e346`.

Before considering Stage 4, I hashed the mounted generation-time producers:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes agree with `generator-manifest.json`, the mounted source manifest,
and the producer snapshot identified by `/audit-input.json`. The producer tree
hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`.
The generator image ID in the source manifest and generator manifest is
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`,
which is also the digest encoded by the audit-input producer path. Producer
authentication therefore passes; this is not a producer-source
`AUDIT_ERROR`.

Raw results are in
[`producer-authentication.json`](evidence/producer-authentication.json),
[`stage1-source-hash-check.json`](evidence/stage1-source-hash-check.json), and
[`01-integrity-command.log`](evidence/01-integrity-command.log).

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
local verification-module closure rooted at the frozen `verification.k`. It
reconstructed 29 rules in source order. For every rule it recomputed the
source span, normalized source hash, and `source_rule_id`. The whole inventory
hash is
`86637211d8eb42b498d51f829d1bcd21ab5987f93b26ba91a4a35193e5b3824b`.

The reconstructed sequence and `/reference/lemma-discovery.json` form an exact
ordered bijection:

- 29 reconstructed entries and 29 protected entries;
- all IDs unique on both sides;
- identical ordered IDs, spans, normalized hashes, and inventory hash;
- no omission, duplicate, extra entry, reorder, or changed identity.

The complete reconstruction is
[`inventory-reconstruction.json`](evidence/inventory-reconstruction.json);
the explicit comparison is
[`inventory-comparison.json`](evidence/inventory-comparison.json).

### Independent classification

My independent classification is 24 `DEFINITION` and 5 `DOMAIN_LEMMA`, with
zero `OPERATIONAL_RULE` and zero `PROVED_DERIVED_LEMMA`.

The 24 definitions are precisely the base/recursive/guarded equations for the
new proof summaries and named terms: `allInts`, `definedProjectInt`,
`projectIntTotal`, `magnitude`, the `decimalCodes` naming equation,
`allDigitCodes`, `codeDigitSum`, `chooseFirst`, `lastCode`,
`signedDigitSum`, and `countNumsSpec`. They define summaries, recurrences,
macros, or named proof terms; they are not pre-existing domain facts.

The five independently identified domain lemmas are:

| Frozen span | `source_rule_id` | Judgment and relevance |
|---|---|---|
| 24–26 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | Unproved definedness equivalence for the partial `Val`-to-`Int` cast; needed by guarded projection. |
| 41–44 | `rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69` | Unproved dynamic-`Val` comparison bridge; needed by source `num < 0`. |
| 45–48 | `rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2` | Unproved dynamic-`Val` unary-minus bridge; needed by source `n = -num`. |
| 63–67 | `rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da` | Unproved bridge from the `str` builtin to the named decimal-code result; needed by `for char in str(n)`. |
| 76–78 | `rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344` | Unproved contract that nonnegative decimal conversion produces digit codes; needed to justify each `int(char)`. |

Stage 1 does not first prove any of these exact rules against a module that
omits it. `prove.sh` compiles `verification.k` with all five already present
before every successful `kprove` command. Thus none qualifies as a
`PROVED_DERIVED_LEMMA`.

Every rule carrying `simplification` or `simplification(10)` is classified as
either `DEFINITION` or `DOMAIN_LEMMA`. All five domain lemmas are directly
relevant to the frozen source or postcondition; none is an irrelevant
mathematical convenience.

The 29 individual decisions, texts, spans, attributes, hashes, and rationales
are in
[`classification-and-obligation-judgment.json`](evidence/classification-and-obligation-judgment.json).

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`;
- `/reference/klean-toolchain.lock.json`.

The returned status is `PASS`, with five obligations, no designated sorry, the
expected frozen/discovery hashes, and generated tree hash
`d07328eaa869c701a22c42ff7e8ae010ea0e3563e97ad614857c607e1c9b90e8`.
The selected status is not `KLEAN_NO_OBLIGATIONS`, appropriately, because the
independent domain set is nonempty.

The ordered domain-rule IDs, generated `source_rules`, and generated
`obligations` are identical and unique. Each obligation repeats the exact
source span and normalized hash, and each `lean_conjunct_sha256` recomputes.
Mathematically:

1. Cast definedness is lowered to `project:Int?.isSome ↔
   definedProjectInt = true ∧ True`.
2. Guarded dynamic integer `<` is lowered to projected integer `<`.
3. Guarded dynamic integer unary minus is lowered to `0 - projectIntTotal`.
4. Guarded `str` on a dynamic nonnegative integer is lowered to the
   `decimalCodes` string result.
5. The nonnegative decimal-code digit contract is lowered unchanged.

The `True` inside the first formula is the exact static lowering of
`#Ceil(V)` where `V : SortVal`; it is not a separate top-level obligation and
does not make the surrounding equivalence vacuous. All five whole obligations
remain discriminating, relevant, and neither duplicated nor weakened.

The fixed generated target is:

- declaration: `Klean108CountNums.Lemmas.targetStatement`;
- definition SHA-256:
  `70f1d88809dcc5ae4f0d283099e5dae878c4385dad1fa0e44959bce6562ed6b4`;
- statement SHA-256:
  `f41037e06fc1909c2283b8fa272875c5f8f536e51ff4b915280347c2c4a38188`;
- 13 bound parameters and exactly the five conjunctions above.

The extracted target from the reference generation, fresh `Base`, generator
manifest, and audit input is identical in all four places. Full preflight
evidence is in
[`preflight-returned-evidence.json`](evidence/preflight-returned-evidence.json),
[`preflight-01-lake-clean.log`](evidence/preflight-01-lake-clean.log), and
[`preflight-02-lake-build.log`](evidence/preflight-02-lake-build.log).

### Audit-image Lean launcher

The first preflight attempt failed before compilation because the mounted Lean
installation lacked the application metadata needed by its generic launcher.
I preserved that failure. The locked Lean 4.22 compiler library was present,
so I used a minimal audit-local launcher that calls the `Lean.Shell` frontend
from that exact `libleanshared` (commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`) and reran all required commands.
The compiler and kernel remained the locked Lean implementation; the launcher
does not transform source or proofs. Its source, compile command, artifact
hashes, and version output are in
[`14-toolchain-recovery.log`](evidence/14-toolchain-recovery.log) and
[`lean_shell_wrapper.c`](evidence/lean_shell_wrapper.c). The initial failure is
in
[`preflight-initial-failed-lake-clean.log`](evidence/preflight-initial-failed-lake-clean.log).

## Stage 5 clean proof and identity

I copied `/candidate` to the fresh workspace recorded in
[`fresh-proof-workspace.txt`](evidence/fresh-proof-workspace.txt) and copied
the generated project into it as `Base`. I cleaned `Base`, ran `lake clean` in
the proof root, and then ran `lake build`. All returned exit code 0. The build
compiled the generated prelude, sorts, injections, immutable lemma module, and
candidate `Proof`.

The candidate pipeline tree hash is exactly the audit-input value
`513b54c4434d082b36a295903360faa7014d207484d493c31e60663a9aaefce9`.
The fresh `Base/Klean108CountNums/Lemmas.lean` byte hash equals the reference
file hash
`c751be51fef61a7c45babdc62e7e4a65ede947e371aa960ab5c40c6a99be80a3`.

The independent source scan found:

- no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`;
- exactly one `def` for each of the 13 fixed parameters;
- exactly one theorem `Proof.final`;
- no candidate declaration or shadow of
  `Klean108CountNums.Lemmas.targetStatement`;
- an exact normalized `Proof.final` statement equal to the fixed generated
  target application.

The trusted mechanical final gate also returned `PASS`. The clean-build logs
are
[`04-base-lake-clean.log`](evidence/04-base-lake-clean.log),
[`05-proof-lake-clean.log`](evidence/05-proof-lake-clean.log), and
[`06-proof-lake-build.log`](evidence/06-proof-lake-build.log). Target and
source-scan results are in
[`proof-integrity.json`](evidence/proof-integrity.json); the trusted gate result
is
[`final-gate-returned-evidence.json`](evidence/final-gate-returned-evidence.json).

### Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. `propext` is one of the three foundational Lean axioms
explicitly allowed by the trusted final-gate implementation, alongside
`Classical.choice` and `Quot.sound`; it is not an unrecorded
generator-specific trust escape. None of the 43 custom K trust declarations
recorded by `trust-inventory.json` occurs in the transitive axiom list. The
exact output is
[`07-print-axioms-Proof.final.log`](evidence/07-print-axioms-Proof.final.log).

## Stage 5 operational-bridge failure

I located and assessed every one of the 13 public parameter definitions. The
arithmetic, Boolean, digit-code predicate, decimal conversion, integer
predicate/projections, and partial-cast definitions agree with the frozen
rules on adversarial inputs. In particular, the decimal implementation
computes `105` as `[49,48,53]` and `-42` as `[45,52,50]`, rather than using a
constant digit sequence.

Three full-symbol definitions fail:

| Bound KORE symbol | Candidate behavior | Frozen operational behavior |
|---|---|---|
| `LblapplyCmp...` | `applyCmp("<", str([97]), str([98])) = false` through the wildcard branch | `str.k` rules 52–56 give `"a" < "b" = true` |
| `LblapplyUn...` | `applyUn("not", true) = noneV` through the wildcard branch | `bool.k` rule 8 gives Boolean `false` |
| `LblapplyBuiltin...` | `applyBuiltin("int", 3, .Vals) = noneV` through the wildcard branch | `builtins.k` rule 140 gives integer `3` |

These are not hypothetical source edits. The auxiliary Lean audit compiles
proofs of the candidate reductions and of their inequality with the expected
frozen results. See
[`OperationalAudit.lean`](evidence/OperationalAudit.lean) and
[`09-operational-adversarial-tests.log`](evidence/09-operational-adversarial-tests.log).

The candidate agrees on the narrow cases used by `solution.py`:
integer `<`, integer unary `-`, and builtin `str`. That is why
`Proof.final` builds. But the public `def`s are bound respectively to the
entire `applyCmp`, `applyUn`, and `applyBuiltin` KORE symbols and are presented
as their honest total meanings. Returning a convenient default for other
operationally specified cases does not implement those frozen symbols. The
generated target does not exercise the counterexamples, so the clean theorem
cannot establish the required operational bridge.

The complete 13-row binding/source-rule/KORE comparison is
[`operational-bridge-judgment.json`](evidence/operational-bridge-judgment.json).
The raw command index for the full audit is
[`COMMANDS.md`](evidence/COMMANDS.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
