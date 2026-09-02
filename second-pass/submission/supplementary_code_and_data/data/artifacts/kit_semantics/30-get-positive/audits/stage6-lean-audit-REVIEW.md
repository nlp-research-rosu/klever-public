# Independent audit: HumanEval 30-get-positive

## Scope and conclusion

The launcher-bound mode is `CLASSIFICATION_AND_PROOF` for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. I independently
audited the frozen Stage 1 verification-module closure, the protected Stage 3
classification, deterministic Stage 4 generation, and the Stage 5 Lean proof.
I did not rely on the selected Stage 2 verdict, prior review prose, or any
earlier PASS.

The audit passes. The canonical closure has ten rules: nine genuine defining
equations or structural recurrence clauses and one relevant `DOMAIN_LEMMA`.
Stage 4 maps that one domain lemma bijectively to one faithful Lean obligation.
The isolated Stage 5 project clean-builds, proves exactly the immutable target,
has an accounted axiom closure, and supplies operationally faithful
definitions on the complete source-rule domain.

## Producer-source and launcher binding

The mandatory producer gate passed before Stage 4 was judged:

- `klean_export.py` SHA-256 is
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `klean.py` SHA-256 is
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- The trusted pipeline tree hash of the three-file producer bundle is
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
- The source manifest and generator manifest record those exact file hashes
  and generator image
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
  The launcher path is keyed by that image digest and records the same bundle
  tree hash.

The trusted audit-input contract recomputed
`25a18c0e57f0e404eeb7e59ff00f5962bec3b824c2e808c06cd848a659b5340e`,
exactly the recorded resolved-input hash. Recomputed mounted-tree and file
hashes match for the Stage 1 workspace, Stage 1 export, Stage 2 audit,
discovery manifest, Stage 4 generation, producer bundle, generated project,
and candidate workspace. All 788 Stage 1 regular-file paths and hashes match
the launcher's per-file map exactly.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`, not against the discovery manifest. `prove.sh` selects
`VERIFICATION` for the final proof. Its local closure, retained in source
order, is `VERIFICATION-BASE`, then `VERIFICATION`.

The reconstructed values are:

- `verification.k` SHA-256:
  `b8451601fa2aaa078d50afaba6a9deea095b64e08feb21fc1ceda6e3bdc6c386`
- inventory SHA-256:
  `22a541b7d4934594e95b3772f125d9c1872b0d6b37d91b7d26eb5f7bcb7908fa`
- inventory count: 10

The protected manifest also contains ten unique identities. Its identity
sequence is exactly the canonical sequence, not merely the same set. There
are no omissions, extras, duplicates, reorderings, span changes, normalized
hash changes, or unclassified rules.

| # | Frozen span | Source rule ID | Independent class |
|---:|---|---|---|
| 1 | `VERIFICATION-BASE:9` | `rule-b241ce9f2bd7347fcfdf85ef6584e8b5bd3d4cbf1d60172dbccd972353a6263b` | `DEFINITION` |
| 2 | `VERIFICATION-BASE:12` | `rule-66cf82d7237685a06ca264938d829ef692b6502a47052bc8b2f6955fe66a6b93` | `DEFINITION` |
| 3 | `VERIFICATION-BASE:13-14` | `rule-17c621b67d0aacf118bb323f41413fea744bb561265d52ff628c37ad78cc2cd9` | `DEFINITION` |
| 4 | `VERIFICATION-BASE:19` | `rule-6617447b31c170258fdc23f4b1ca0dc4b3f7c945e50c08d4e290381d3e24508f` | `DEFINITION` |
| 5 | `VERIFICATION-BASE:20` | `rule-b7d6ce82ec2a2ac7221e232a8762ec40e0c5f8a33688ec923438f1197c35a783` | `DEFINITION` |
| 6 | `VERIFICATION-BASE:21-22` | `rule-569442f388c8214bce6f506695671575b195c7d000bcc61c81f57507abc8eeae` | `DEFINITION` |
| 7 | `VERIFICATION-BASE:27` | `rule-f59962ae3cbf101799667bef7e71cd44e7fc5067b67f94493ee34bff8c007791` | `DEFINITION` |
| 8 | `VERIFICATION-BASE:28-31` | `rule-88784a48ac7e5083100f357cdc7fcd5856f28ba2c5b93d4a5efd4a85eb3dfae2` | `DEFINITION` |
| 9 | `VERIFICATION-BASE:32-35` | `rule-6f46b6b7356839cbf0b867220b1e1216ff7a93fb8ba127ad7cd2a420f744ecf2` | `DEFINITION` |
| 10 | `VERIFICATION:43-45` | `rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0` | `DOMAIN_LEMMA` |

## Independent classification judgment

Rules 1-3 define the `numericVal` and `numericVals` domain summaries. Rules
4-6 are the sort-disjoint and guarded totalizing clauses of
`positiveNumeric`. Rules 7-9 are the empty, positive-head, and nonpositive-head
clauses of the structurally decreasing `filterPositive` recurrence. These are
all definitions; the two recursive guards are complementary. The three
`filterPositive` clauses are simplifications, so their `DEFINITION`
classification is also valid under the simplification restriction.

Rule 10 is not a definition of the pre-existing `applyCmp` symbol and is not
an ordinary execution rule. It equates the supplied operational comparison
with the proof-local `positiveNumeric` summary:

```k
rule applyCmp(">", V:Val, 0.0) => positiveNumeric(V)
  requires numericVal(V)
  [simplification]
```

Stage 1 proves Int- and Float-specialized connection claims using
`VERIFICATION-BASE`, but it does not first prove this exact generic rule with
this exact guard and then use it later. It is therefore not a
`PROVED_DERIVED_LEMMA`; `DOMAIN_LEMMA` is the correct classification.

The lemma is materially relevant. The source function branches on
`x > 0.0`, appends exactly the values satisfying that comparison, and the
postcondition summarizes the returned list with `filterPositive`. There are
no operational or proved-derived entries, and every simplification is either
a definition or this domain lemma.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required frozen inputs. The first invocation exposed an audit-runner
PID-namespace issue: Lean 4.22 could not resolve
`/proc/<getpid()>/exe` because `/proc` reflects the outer namespace. A local
`LD_PRELOAD` shim under `/tmp/audit-work` made `getpid()` return the numeric
target of `/proc/self`; it did not alter any candidate or provenance input.
With the pinned Lean 4.22 installation then visible, the same trusted
preflight returned `PASS`.

The successful preflight independently clean-built the generated project and
returned:

- Stage 1/export hash:
  `1370f4a6a448f634004586bba96baba6ee2c98695deb577b26d99d6954c06298`
- discovery hash:
  `1fc4eb578da6ef7d8d9b65c49bb3b729c4ad3836d11defe7509f7c1772f31b86`
- generated tree hash:
  `54ebe798b47f29722e34e69f1fd1ce6345bfb3ada26c7b348a99381682c86fb8`
- obligation count: 1
- generated trust declarations: 44
- generated proof holes: 0

The independently classified domain set has one entry. The input manifest,
obligation map, and generator manifest each have that same one source rule in
the same position. Its source span, normalized hash, inventory hash,
discovery hash, and conjunct hash all recompute exactly. The obligation-map
file hash is
`89a985bbfe92a8a44362b2badba982012004d4b8313a7448d141c4f667f91e10`.
Thus the source-rule/obligation relation is a true bijection.

The target is not weakened or relocated. Its definition hash is
`6f5dec2aeadbe159d708d06c09f69bb5f6033586eba4cf48bb2147fb482125f6`,
and its instantiated statement hash is
`6913cb334bc6fd0eb3e161a87802f537b0fc922641b50842392b6025f39ba226`.
Both equal the generator manifest and audit input. The proposition preserves
the exact operator, Val input, Float-zero injection, guard, and RHS:

```lean
∀ (V : SortVal)
  (h : numericVal V = true),
  applyCmp ">" V (SortVal.inj_SortFloat (0.0 : Float))
    = positiveNumeric V
```

The guard is satisfiable for both Int and Float constructors under the frozen
definition, so this is not a vacuous obligation.

## Stage 5 clean proof and target identity

I created
`/tmp/audit-work/lean-proof-audit.tMzybb/project`, copied only the candidate
proof project metadata and source into it, and copied the immutable generated
project as `Base`. Its Base tree initially and after the build remained
exactly
`54ebe798b47f29722e34e69f1fd1ce6345bfb3ada26c7b348a99381682c86fb8`.
The target hashes remained unchanged.

`lake clean` exited 0, after which neither the root build directory nor the
Base package's absolute build directory existed. `lake build` then rebuilt
the project from scratch and exited 0. The warnings were only unused-variable
linters in generated code.

Outside immutable Base, the candidate contains no `sorry`, `admit`, `unsafe`,
new `axiom`, or new `opaque`. Each of the three target parameter bindings is
defined exactly once. The candidate does not declare or shadow
`targetStatement`; the only target declaration remains the generated one.
`Proof.final` states the generator's exact instantiated statement, rather
than a copy or weakened theorem.

The exact Lean axiom output was:

```text
'Proof.final' depends on axioms: [«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»,
 «_>Float__FLOAT_Bool_Float_Float»,
 propext,
 Classical.choice]
```

The two named Klean axioms are exact `trust-inventory.json` entries for the
supplied opaque Int-to-Float and Float-greater-than primitives. `propext` and
`Classical.choice` are the standard Lean axioms expressly accepted by the
trusted final gate. `sorryAx` is absent, and there is no unrecorded generated
trust escape. The trusted end-to-end mechanical gate also returned `PASS`;
as designed, it marked semantic classification `NOT_EVALUATED`, which is why
the following independent bridge audit is necessary.

## Operational-bridge audit

The target bindings all cite
`rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0`.
I compared their elaborated Lean definitions with that rule's complete match
domain, the frozen program, and the supplied operational rules.

`numericVal` returns true exactly for `SortVal.inj_SortInt` and
`SortVal.inj_SortFloat`, and false for every other constructor. This is the
exact operational meaning of `isInt(V) orBool isFloat(V)`. Ground checks for
an Int, Float, Bool, and `noneV` all reduced to the expected result.

`positiveNumeric` maps an Int to
`gtF(intToF(I), 0.0)`, a Float to `gtF(F, 0.0)`, and a nonnumeric value to
false. Its Lean helpers select total interpretations of the two recorded
opaque supplied primitives; they do not assert any concrete floating-point
fact.

For the bound `applyCmp` rule, the complete relevant domain is operator `">"`,
numeric left operand, and Float right operand `0.0`. Supplied `float.k` maps
the Int/Float case to `gtF(intToF(I), F)` and the Float/Float case to
`gtF(F1, F2)`. The candidate's corresponding branches reduce to those exact
terms. It also implements the two other numeric `>` combinations consistently
with `int.k` and `float.k`. Its total default for unrelated operators lies
outside the bound source rule and the source program's use; it is not used to
prove this obligation.

Adversarial Lean witnesses established the Int and Float bridge equations
for arbitrary operands on the target's Float-zero boundary. They also checked
positive and negative ground integer comparisons. A deliberately dishonest
counterfactual in which `numericVal` was constant false still built, proving
that build success alone would admit a vacuous bridge; the submitted
definition is not that mutation and has satisfiable numeric guards. A second
counterfactual changed only the operational Int/Float `applyCmp` branch to
false. Its clean build failed with the residual:

```text
⊢ totalFloatGreater (totalIntToFloat x✝) 0.0 = false
```

This demonstrates sensitivity to the frozen operational comparison rather
than closure through a constant, identity, hard-coded result, or vacuous
guard.

## Evidence

Raw commands, outputs, hashes, target text, clean-build logs, exact axiom
output, and adversarial results are under `/audit-output/evidence/`:

- `00-context-and-producer-gate.txt`
- `01-rule-inventory-and-classification.txt`
- `02-stage4-preflight.txt`
- `03-stage4-integrity-and-target.txt`
- `04-fresh-lean-build.txt`
- `05-lean-axioms-and-mechanical-gate.txt`
- `06-operational-bridge-audit.txt`
- `07-final-mechanical-gate.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
