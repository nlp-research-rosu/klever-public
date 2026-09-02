# Independent audit: HumanEval 100-make-a-pile

This is an independent audit of Stage 3 lemma classification, deterministic
Stage 4 generation, and the Stage 5 Lean proof for condition `semantics` under
`SUPPLIED_SEMANTICS`.

The launcher environment and the cryptographically bound audit input both
select `CLASSIFICATION_AND_PROOF`. The recomputed audit-input binding is
`252bc21c3f31d78780aa6d21bdc4b13c9035e18106c4fb954e9f5c8e45df7c5a`,
identical to the recorded value. I did not rely on the prior Stage 2 review,
the prior Stage 3 rationales, or earlier PASS results as proof of correctness.

The complete command index is `evidence/COMMANDS.md`. All commands and results
referenced below are under `evidence/`.

## 1. Frozen inputs and hash binding

Using the launcher's trusted digest implementations, I independently
recomputed every hash backed by a mounted input. All matched:

- Stage 1 artifact tree:
  `fd22b659736c079572c882690db5a6de1a60c2cdd2c6780b9375cea86c5e5e75`
- Stage 1 export tree:
  `8cb310c27b58c4cf4a1177bca23d5c552188aec707cbc5889ff11034e0121394`
- Stage 2 audit tree:
  `547086d0780d793584fc2ec31777ddaf8af268475ac2037c18730492e20c81bc`
- Stage 3 manifest file:
  `106516d0c062739603068e16583badc80e70377748c53d324b8333954b018206`
- Stage 4 generation tree:
  `4eb4d5539a8d89803b3b22b8da12ce597359f1170c5db9629689e104e03ef3a0`
- Generated Lean project:
  `4a4f68cf160e9e1c5d78708fa9997b11bfbecfe93a4523c7c01ed207ee94c014`
- Producer-source bundle:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
- Stage 5 candidate workspace:
  `d78850d0e81c3a5e4477ae89c765e81c658138cad535ce6a661e7ec61efb2d39`

All 35 recorded Stage 1 per-file source hashes also matched. The Stage 5
invocation directory and the audit checker lock are not mounted as standalone
files in this audit interface, so their standalone recorded digests cannot be
recomputed from local bytes. The trusted final gate nevertheless verified the
signed audit-input binding and every mounted input hash before and after its
checks. See `00-audit-mode-and-binding.txt`,
`25-recorded-hash-verification.json`, and
`59-trusted-final-mechanical-gate.json`.

## 2. Independent rule-inventory reconstruction

I first ran `tools.k_rule_inventory.inventory_verification` directly on the
frozen `/reference/k-proof`. The selected main module is
`PILE-VERIFICATION`; its local verification-file closure contains only that
module. The frozen `verification.k` hash is
`9afbe6b62b2759b73907eae6e058d6abbe29558e50b90ecfa44fd373c152f0f9`.

The canonical inventory contains these nine rules. Each
`source_rule_id` suffix is the independently recomputed normalized source
SHA-256.

1. Lines 7–8,
   `rule-22751b6f0ce256a241dc19f1640dcb5480b4efc2a26bbfa044ba4629c8bb9c35`:
   `DEFINITION` (`pileCondition` macro).
2. Lines 11–16,
   `rule-4fb38cd43bd4ca35e7dae0edae393d11b590c0f523ccfc1dd9bed6969c629464`:
   `DEFINITION` (`pileLoopBody` macro).
3. Lines 19–23,
   `rule-f23f2f7e0eba99112c099245082f9d758a2c0c6c59eddffb11a02898914989bf`:
   `DEFINITION` (`pileBody` macro).
4. Line 26,
   `rule-6010dc93df234a84e52b82001b1f5013df8aa366d7a3250587f36b7863f45a53`:
   `DEFINITION` (`pileClosure` macro).
5. Lines 29–30,
   `rule-49c485cbb59af517bd2978b8d663cb5072f818f9d7ceb9f26cf6e545770689f4`:
   `DEFINITION` (`pileModule` macro).
6. Lines 35–36,
   `rule-c7bc3f6e9e3d053f0d1a231faec47b72f24e3a9d1bf5bd7dcc951f8cea4f6fa4`:
   `DEFINITION` (base equation of the `pile` summary).
7. Lines 37–39,
   `rule-facdd655b24df1d5b12ab16ecd73c39d00a41e6f338a787a0ccad6551c07e234`:
   `DEFINITION` (recursive equation of the `pile` summary).
8. Line 43,
   `rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb`:
   `DOMAIN_LEMMA` (right identity of `valSeqConcat`).
9. Lines 44–46,
   `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97`:
   `DOMAIN_LEMMA` (associativity of `valSeqConcat`).

The whole reconstructed inventory hash is
`bd714f82b827e599055d7113fac38d50c8870fa758db37a34b198a8c45698cf4`.
It matches the protected Stage 3 manifest. The manifest has exactly nine
entries in the same order, with no duplicate, missing, extra, unknown, or
reordered identity. See `01-reconstructed-inventory.json` and
`02-inventory-manifest-comparison.json`.

## 3. Independent classification judgment

The first five rules expand syntax explicitly declared `[macro]`; they name
the exact translated comparison, loop body, function body, closure, and
module terms. They are definitions, not execution shortcuts. The two `pile`
rules define a named mathematical summary. Their guards `I >=Int N` and
`I <Int N` are disjoint and exhaustive over integers, and the recursive
branch advances `I` by one toward the base branch. These are also
definitions.

The supplied list semantics already declares and defines `valSeqConcat`:

```text
valSeqConcat(.ValSeq, T) = T
valSeqConcat(vCons(V, S), T) = vCons(V, valSeqConcat(S, T))
```

Consequently, the two simplification rules in `verification.k` neither
introduce that function nor define a named summary. They are universally
valid algebraic consequences of the existing recursive definition, proved by
structural induction on the first sequence. They are not ordinary operational
rules because they do not rewrite a program configuration or observation.
They are not `PROVED_DERIVED_LEMMA`: both were compiled into the verification
module before either Stage 1 `kprove` invocation, and Stage 1 contains no
earlier bridge-free proof of either exact rule. `DOMAIN_LEMMA` is therefore
the only valid classification for both.

Both domain lemmas are materially relevant to this program and postcondition.
The source loop appends with `valSeqConcat`, while the loop claim expresses
the remaining suffix as `valSeqConcat(VS, pile(N,I))`.

- Removing only right identity makes the loop proof fail at termination on
  the residual `VS = valSeqConcat(VS, .ValSeq)`.
- Removing only associativity makes the induction step fail on the equality
  between
  `valSeqConcat(valSeqConcat(VS, singleton), pile(N,I+1))` and
  `valSeqConcat(VS, vCons(current, pile(N,I+1)))`.

These are exact nonzero `kprove` failures in
`28-right-identity-removed-kprove.log` and
`30-associativity-removed-kprove.log`. With the frozen rules restored, the
prefix and loop claims independently return `#Top`
(`32-original-prefix-kprove.log` and `33-original-loop-kprove.log`).

Thus the Stage 3 classification is complete and correct. There are seven
definitions, no operational rules, no proved-derived lemmas, and exactly two
genuine, relevant domain lemmas. Every simplification rule is a domain lemma,
as required.

## 4. Stage 4 producer identity and deterministic generation

Before accepting any Stage 4 result, I hashed the mounted generation-time
producer sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

These values exactly match both `generator-manifest.json` and
`source-manifest.json`. The source manifest contains exactly those two
producer files, and its immutable image ID
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
matches the generator manifest and the image-derived producer-bundle path in
`/audit-input.json`. The producer bundle's launcher-style tree hash also
matches the audit input. There is no producer-source infrastructure error.
See `12-generation-producer-final-attestation.json`.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock. It returned
`PASS`, rebuilt an isolated generated project successfully, found zero
designated sorries, found 49 generated trust declarations, and reported
exactly two obligations. Its generated build-output hash
`899832167ed3ce2a20d1d23723b2043eaa20b1a2d4391674c1cf33cf0be17317`
also matches the recorded preflight. See
`44-independent-stage4-preflight-success.json`.

The exact source-rule/obligation mapping is:

1. Rule `656b…c5cb`, source line 43, maps to
   `∀ VS, valSeqConcat VS .ValSeq = VS`.
2. Rule `9345…09b97`, source lines 44–46, maps to
   `∀ C B A, valSeqConcat (valSeqConcat A B) C =
   valSeqConcat A (valSeqConcat B C)`.

The ordered ID lists are equal and duplicate-free. Every source span,
normalized hash, inventory hash, discovery-manifest hash, and Lean-conjunct
hash matches. The obligation-map hash is
`f35f3cc1a4d6ed0adbf5ff7ba0178438531f46dce057d409e5466c4b4a68b591`,
equal to the generator manifest. There are no guards to lose, and all source
variables and both equations are retained exactly.

The generated project contains exactly one target:

```text
Klean100MakeAPile.Lemmas.targetStatement
  «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
```

Its statement hash is
`f67a6958cbe0cbf94c6a69277149fb909d495cdb02f17bc427b5a6c645de3214`;
its exact definition hash is
`791b790c52c69aa4fc975872dc22c252555973f3fd2b9931098a1096de0ca587`.
The declaration, file, parameter binding, statement, and both hashes match
the obligation map, generator manifest, recorded preflight, and audit input.
The target definition is exactly the conjunction of the two mapped
obligations. See `26-obligation-target-bijection.json`.

Neither conjunct is vacuous. The Lean adversarial checks exhibit a right
projection that violates the first conjunct and a right-identity operation
that violates associativity, hence the second conjunct. The selected Stage 4
status is correctly `PASS`, not `KLEAN_NO_OBLIGATIONS`.

## 5. Fresh Stage 5 build, target identity, and source scan

I copied the candidate into
`/tmp/audit-work/stage5-fresh-audit-2` and copied the generated project
contents into its existing empty `Base` directory. Before the build, `Base`
had the exact generated-project tree hash
`4a4f68cf160e9c5d78708fa9997b11bfbecfe93a4523c7c01ed207ee94c014`.

The audit container mounts `/proc` from a different PID namespace. Lean
4.22's lookup of `/proc/<getpid>/exe` therefore initially failed before
reading any project file, although `/proc/self/exe` worked. I used the
recorded, narrowly scoped preload shim in `evidence/lean_proc_self_shim.c`, which
rewrites only that current-process executable lookup. It does not alter Lean
sources, imports, declarations, elaboration, kernel checking, or output.
With the pinned Lean binary and this environment-only correction:

```text
lake clean exit_code=0
lake build exit_code=0
```

The fresh build compiled `Klean100MakeAPile.Prelude`, `Sorts`, `Inj`,
`Lemmas`, and `Proof` and completed successfully. See
`45-stage5-lake-clean-final.log`, `46-stage5-lake-build-final.log`, and
`47-stage5-build-final-exit-codes.txt`.

After the build, `Base` still had the exact reference tree hash and exact
target metadata, and `Proof.lean` still had candidate hash
`f61dda2e2ab96a5485a56397f53c25ce384a5634e880ee9e52cd411fd26d9981`.
The candidate's original `Base` directory was empty, so it did not replace or
shadow generated source. It declares no `targetStatement`.

An independent scan of the two candidate Lean sources found:

- no `sorry`, `admit`, or `unsafe`;
- no new `axiom` or `opaque`;
- no trust declarations;
- exactly one definition of the required parameter; and
- exactly one theorem named `final`.

See `51-candidate-integrity-scan.json` and
`52-postbuild-target-identity.json`.

## 6. Proof identity and axiom accounting

Lean prints the theorem type as:

```text
Proof.final :
  Klean100MakeAPile.Lemmas.targetStatement
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
```

This is the fixed generated theorem instantiated with the candidate's unique
required definition. It is not a duplicate, weakened theorem, or alternate
target. `#print Proof.final` shows precisely the conjunction constructor with
the candidate's right-identity and associativity proofs. See
`49-print-proof-final-and-target.log`.

The exact required axiom query output is:

```text
'Proof.final' does not depend on any axioms
```

Thus the actual dependency set is empty. It contains neither `sorryAx` nor
any unrecorded trust escape. The generated trust inventory has 49 allowlisted
declarations, but none is reachable from `Proof.final`; the empty dependency
set is fully reconciled with that ledger. See
`48-print-axioms-proof-final.log` and
`50-axiom-reconciliation.json`.

The trusted final mechanical gate independently repeated preflight, clean
build, exact target typing, and axiom parsing. It returned `PASS` in
`CLASSIFICATION_AND_PROOF` mode with `used_axioms: []`. See
`59-trusted-final-mechanical-gate.json`.

## 7. Operational-bridge audit

The single target parameter is bound to KORE symbol
`LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq`
and to both domain-rule IDs. The generated `SortValSeq` is the same free
datatype shape as frozen K `ValSeq`: empty or `vCons(head, rest)`.

The candidate defines the parameter by structural recursion on its first
argument:

```text
concat(empty, tail) = tail
concat(cons(head, rest), tail) =
  cons(head, concat(rest, tail))
```

Those are exactly the two frozen operational equations in
`reference-semantics/semantics/list.k`, including argument order, base value,
constructor placement, preservation of element order, and recursive descent.
The Lean audit proves both universal candidate-to-K defining equations by
definitional equality (`rfl`).

The operational comparison is essential because the generated algebraic
target alone does not uniquely characterize concatenation. I checked two
adversarial counterfactuals in `CounterfactualAudit.lean`:

- A left projection proves both generated obligations without axioms but
  violates the frozen K base equation on an empty left sequence and a
  nonempty tail.
- A "first nonempty" operation implements the correct base equation and also
  proves both generated obligations without axioms, but violates the frozen
  recursive step on nonempty left and right sequences.

Both wrong definitions are therefore convenient target-only models and would
be rejected. The actual candidate is neither constant, identity,
hard-coded, vacuous, nor merely chosen to satisfy the equations: it matches
both complete frozen defining cases for every `SortValSeq`. The expanded
counterfactual and connection checks compile successfully with no output in
`57-operational-bridge-and-nonvacuity-success.log`.

The candidate consequently passes the independent operational bridge, proof
identity, and trust-boundary judgments. The Stage 3 classifications are
correct and relevant, Stage 4 is deterministic and bijective, and Stage 5
proves exactly the fixed target with an honest implementation of the bound K
operation.

VERDICT: PASS
LEGITIMACY: LEGIT
