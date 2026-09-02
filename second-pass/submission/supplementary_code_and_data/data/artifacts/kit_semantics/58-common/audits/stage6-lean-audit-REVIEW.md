# Independent audit: HumanEval 58-common

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the candidate, prior reviews, logs, manifests, comments, and classifications
as untrusted evidence. I did not rely on the prior Stage 2 concern or any
earlier PASS/classification judgment.

The independently reconstructed Stage 3 classification is correct. Stage 4
contains exactly one faithful obligation for the one true domain lemma, and
the fixed target is unchanged. The Stage 5 project builds cleanly from a fresh
copy, proves exactly that target, has no forbidden declaration or proof hole,
uses only the three expected Lean foundational axioms, and supplies honest
operational meanings for all three target parameters.

## Launcher and producer integrity

`/audit-input.json` verifies to resolved-input SHA-256
`04f8a979af706a0f0102582769e13e5dc255f99113094edc08b5e7de83d771bc`.
Every mounted hash checked by the launcher contract matched, including:

- Stage 1 workspace:
  `017d00ed7d9e6bf64014550a6acb496d3318f95fa43cf33eb50f6d0778a4cb9e`;
- Stage 1 export:
  `1d8be9aa06c1f4e4befc27f7d068cf1426c878553e4591c62ad16917529b138e`;
- Stage 3 manifest:
  `e9c55ad1cd4ee9b1197b4b5d7ed2bc3cf47561719b89bf22bcdf008eddc41974`;
- selected Stage 2 audit:
  `ca59a75665559dd05972378a27f9c9836cc51edd64a693c72065413b61d6e152`;
- Stage 4 generation:
  `2ef1347913ef7d1fb34e093502fd75b426d90c6e5a4c10dc29948f52239aac01`;
- generated project:
  `392c68da1f6ac9f2277bbdcc3979fbc456af0fea00a89e45cd41f4e136ccebce`;
- producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`;
  and
- Stage 5 workspace:
  `f7429573cb47036ad77879a278bcbc4b1bed891db6e59a50fe297a1ef2b09e64`.

All 770 Stage 1 regular-file hashes matched `/audit-input.json` exactly, with
no missing, extra, or changed file.

Before evaluating Stage 4, I directly hashed the immutable producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

These are exactly the hashes in `generator-manifest.json` and
`source-manifest.json`. Both manifests identify generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the image key is also the final component of the producer path bound by
`/audit-input.json`. The pinned toolchain object exactly matches
`/reference/klean-toolchain.lock.json`. There is no producer-provenance
infrastructure error.

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen Stage 1 workspace. The selected local verification module and its local
closure are both exactly `VERIFICATION`. The frozen `verification.k` hash is
`2e830c8b68b6e20f91c87c36cbd9a2752b9bd16efa9ee8a07eab6a1d439ba9a6`.

The reconstruction found seven rules. For each rule I independently
recomputed the source span, whitespace-normalized text hash, and
`source_rule_id`. The canonical whole-inventory hash is
`87f56ae659ac675f0785aa4bb001dad4a3f0f76ab2231c11d8dd28eaf505e6f6`.
It matches the protected Stage 3 manifest. The Stage 3 IDs are unique and
bijective with the reconstruction in the same order: there are no omissions,
duplicates, extras, reordered identities, changed spans, or changed hashes.

| Frozen span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 8 | `rule-b851270341fa427d7c6b86536424da72948b62f5f47bf7a5debfcf72c73e19af` | `DEFINITION` | Empty-sequence base equation for the named total `commonMember` summary. |
| 9–10 | `rule-2bbf2fca970e20e1ac591ef3fdfe348b299c5160141f4fefbc8f4d1e683815b0` | `DEFINITION` | Strict-tail recurrence for `commonMember`. |
| 14–16 | `rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0` | `DOMAIN_LEMMA` | Guarded Boolean fact over existing K hooks; not a definition, operational rule, or previously proved lemma. |
| 20 | `rule-10e71d2ccb6e618e545b5c344fbd49a07fb245480c0dc10b2f8ce274d73e655c` | `DEFINITION` | Empty-input base equation for the named total `commonAcc` summary. |
| 21–28 | `rule-b1d407f48ea5db85651bab85e4931a62e916cc0c29c463d62deb4e093d66c5cf` | `DEFINITION` | Strict-tail accumulator recurrence corresponding to the loop update. |
| 32–41 | `rule-24fa2be80e9ed0bfffd6b7a91d6b534370f30c8d0074bdfc6680eda1e7b5f16c` | `DEFINITION` | Macro expansion naming the exact translated loop body. |
| 44–48 | `rule-345d1c0eced89af20c67c30dcca439dc5c455af03b30199f56c132eeb1dc141f` | `DEFINITION` | Macro expansion naming the exact translated function body. |

The only `[simplification]` rule is the third entry, classified
`DOMAIN_LEMMA`, so the simplification-category restriction is satisfied.

## Independent classification judgment

The six `DEFINITION` entries genuinely define named summaries, recurrences,
or macro proof terms:

- `commonMember` folds exact K equality over a `ValSeq`;
- `commonAcc` folds the encounter-order, duplicate-free intersection over the
  unprocessed suffix and accumulator; and
- `commonLoopBody()` and `commonBody()` expand to the exact syntax in the
  translated source solution.

None is an ordinary execution/observation rule, and none states an
independent human-facing property.

The third rule states:

```k
rule ((E:Val ==K V:Val) orBool B:Bool) => B
  requires notBool (E ==K V)
  [simplification]
```

Operational K binds its symbols to `KEQUAL.eq`, `BOOL.or`, and `BOOL.not`.
The guard is enabled exactly when `E ==K V` is false; the left side then is
`false orBool B`, which the frozen Boolean rules reduce to `B`. Thus the rule
is mathematically valid over its whole guard.

It is also materially relevant. The frozen list semantics takes its unequal
membership path under `notBool (E ==K V)`, while the `commonMember`
recurrence produces `(E ==K V) orBool commonMember(V,R)`. Membership and
non-membership are the two conditions controlling whether the source loop
appends an element, and the Stage 1 loop/program claims summarize the result
through `commonAcc`.

It is not a `PROVED_DERIVED_LEMMA`: `prove.sh` first compiles
`verification.k` with this rule already present, then proves `spec.k`. There
is no earlier proof of the exact rule against a module that excludes it.
It does not define a symbol and it is not an ordinary operational transition.
`DOMAIN_LEMMA` is therefore the only admissible class.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
over the required Stage 1 workspace, protected Stage 3 manifest, selected
Stage 4 generation, and pinned toolchain. It returned `PASS`, one obligation,
42 generated trust declarations, zero designated sorries, and the exact
generated tree hash. Both its clean and build commands exited zero; the build
output hash exactly reproduced the recorded
`b0e127169b3a32caa1bbebde218767a9a149fe5e4f3a3e58bbf38bfb1ab51dbf`.
The complete returned document is saved in
[04-preflight-result.json](/audit-output/evidence/04-preflight-result.json).

Independent of preflight, the true domain set contains exactly the single
Stage 3 rule at lines 14–16. The obligation map has:

- one source-rule record with that ID;
- one obligation with that ID;
- no duplicate ID;
- the exact source span, normalized hash, inventory hash, and discovery hash;
  and
- Lean-conjunct hash
  `103473fe86dcdb7ca9fe3c74b8879f74a116d402d652918c991751958f340c7d`.

The map is therefore an exact source-rule/obligation bijection.

The generated conjunct universally quantifies `B`, `V`, and `E`, assumes
`notBool(E ==K V) = true`, and concludes `(E ==K V) orBool B = B`, with the
required `Val → KItem → K` injections. This is the exact guarded K rule. It
does not restrict `B`, `V`, or `E`, delete the guard, replace the conclusion,
add an irrelevant disjunct, or introduce a vacuous conjunct. The guard is
satisfiable: the operational audit machine-checks distinct Boolean `SortVal`
values injected into `SortK`. The fact that the equal case does not satisfy
the guard mirrors the K rule rather than weakening it.

The immutable generated project contains exactly one target:

- declaration: `Klean58Common.Lemmas.targetStatement`;
- file: `Klean58Common/Lemmas.lean`;
- definition hash:
  `98d0672b78b4f4c15e8b7bffa3425b18e7bca1bb75cb035b56f43ed504068fbe`;
- fixed applied statement:
  `Klean58Common.Lemmas.targetStatement _orBool_ «_==K_» notBool_`; and
- statement hash:
  `2fda1f81ed5497da53237f8d752e5636cd9ae4baacd1950d50dc5f8fe50af609`.

The target object reconstructed from the generated source is byte-for-byte
equal as structured data to both `generator-manifest.json` and
`/audit-input.json`. The obligation-map hash
`4257c6507e42ecb243223cde96bdabf2d4fab7fc0331367b9faf29c8238accea`
also matches its manifest. This is not a `KLEAN_NO_OBLIGATIONS` case.

## Stage 5 candidate and proof identity

I created a fresh project at
`/tmp/audit-work/manual-proof-audit-58-common-final`, copied the candidate
there, and copied the immutable generated project into `Base/`. I then ran
both `lake clean` and `lake build`. Both exited zero. The only diagnostic is
the generated target's harmless unused-variable linter warning. Complete
output is in
[05-manual-clean-build.txt](/audit-output/evidence/05-manual-clean-build.txt).

The trusted launcher-bound final gate independently repeated Stage 4
preflight, copied and rebuilt the proof, checked the exact theorem statement,
ran the axiom audit, and returned `PASS`.

Static inspection of every candidate Lean source found:

- zero `sorry`, `admit`, `unsafe`, `axiom`, or `opaque` tokens;
- no candidate definition of `targetStatement`;
- exactly one `theorem final`; and
- exactly one candidate `def` for each required target parameter.

The candidate therefore neither changes nor shadows the generated target.
Lean's printed declaration is exactly:

```lean
theorem Proof.final :
  Klean58Common.Lemmas.targetStatement
    Proof._orBool_ Proof.«_==K_» Proof.notBool_
```

This is the fixed theorem applied to the candidate definitions, not a copy,
weakened theorem, or vacuous replacement.

## Axiom accounting

In the fresh project I ran Lean on a file containing the exact command
`#print axioms Proof.final`. The output was:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. `trust-inventory.json` records all 42 generated
axiom/opaque declarations. None of those generated declarations occurs in
the dependency set of `Proof.final`; in particular, the generated global
`«_==K_»` axiom is not used in place of the candidate's namespaced
definition. The three printed dependencies are the standard Lean
foundational axioms allowed by the trusted final gate: `Classical.choice`
supports the candidate's noncomputable structural decision procedure, while
`propext` and `Quot.sound` arise from the simplifier. There is no unrecorded
generated proof-trust escape.

The exact source and output are in
[05-axiom-audit.txt](/audit-output/evidence/05-axiom-audit.txt).

## Operational-bridge audit

All three target parameters are bound to
`rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0`.
The compiled frozen KORE identifies their operational hooks exactly.

| Target parameter | Candidate definition | Frozen K meaning | Independent judgment |
|---|---|---|---|
| `_orBool_` / `Lbl'Unds'orBool'Unds'` | `fun left right => left \|\| right` | Total `BOOL.or`; truth table `false,false,false`, `false,true,true`, `true,false,true`, `true,true,true`. | Exact. The observed candidate table is `[false, true, true, true]`. |
| `«_==K_»` / `Lbl'UndsEqlsEqls'K'Unds'` | `fun left right => decide (left = right)` | Total `KEQUAL.eq`, equality of K terms. | Exact. `SortK` is the generated inductive encoding of `.K`/`kseq`; Lean equality is structural equality of that encoding. Equal empty terms, equal one-item terms, unequal empty/one-item terms, and different embedded Boolean terms were checked. |
| `notBool_` / `LblnotBool'Unds'` | `fun value => !value` | Total `BOOL.not`; `false ↦ true`, `true ↦ false`. | Exact. The observed candidate table is `[true, false]`. |

These definitions are total over the declared parameter types. They are not
constant, identity, hard-coded to the theorem, or dependent on the proof
hypothesis. Boolean short-circuit implementation is immaterial here because
the target parameter receives already evaluated `SortBool` values and has no
state or control effects. Structural equality is also appropriate for every
canonical `SortK` term and, in particular, the one-item injected values used
by the frozen rule.

I also tested counterfactual mutations in Lean. A right-projection
`_orBool_`, a constant-true equality, and a constant-false negation can each
make this equation provable—the first by making the conclusion definitional,
the others by making the guard false. Those counterfactual theorems
machine-check. This confirms that clean build and theorem identity alone are
not sufficient and that the operational bridge comparison is load-bearing.
The actual candidate passes that comparison. The adversarial and
counterfactual artifact is
[06-operational-bridge-adversarial.lean](/audit-output/evidence/06-operational-bridge-adversarial.lean).

## Evidence index

- Environment and Lean PID-namespace adapter:
  [00-environment.txt](/audit-output/evidence/00-environment.txt) and
  [00-lean-proc-pid-shim.c](/audit-output/evidence/00-lean-proc-pid-shim.c).
  The adapter only repairs Lean's `/proc/<pid>/exe` prefix lookup; it does not
  alter source, elaboration, kernel checking, or theorem dependencies.
- Producer hashes:
  [00-producer-provenance.txt](/audit-output/evidence/00-producer-provenance.txt).
- Trusted inventory reconstruction and exact result:
  [01-reconstruct-inventory.py](/audit-output/evidence/01-reconstruct-inventory.py)
  and
  [01-reconstruct-inventory.txt](/audit-output/evidence/01-reconstruct-inventory.txt).
- Launcher hashes, source hashes, target identity, and forbidden-token scan:
  [02-integrity-and-target.py](/audit-output/evidence/02-integrity-and-target.py)
  and
  [02-integrity-and-target.txt](/audit-output/evidence/02-integrity-and-target.txt).
- Frozen operational hook bindings:
  [03-operational-k-bindings.txt](/audit-output/evidence/03-operational-k-bindings.txt).
- Stage 4 preflight command and complete returned evidence:
  [04-preflight-command.txt](/audit-output/evidence/04-preflight-command.txt)
  and
  [04-preflight-result.json](/audit-output/evidence/04-preflight-result.json).
- Trusted final gate and manual clean build:
  [05-trusted-final-gate.txt](/audit-output/evidence/05-trusted-final-gate.txt)
  and
  [05-manual-clean-build.txt](/audit-output/evidence/05-manual-clean-build.txt).
- Exact axiom output:
  [05-axiom-audit.txt](/audit-output/evidence/05-axiom-audit.txt).
- Operational examples and counterfactuals:
  [06-operational-bridge-output.txt](/audit-output/evidence/06-operational-bridge-output.txt).
- Printed candidate declarations and proof term:
  [07-print-candidate-declarations.lean](/audit-output/evidence/07-print-candidate-declarations.lean)
  and
  [07-print-candidate-output.txt](/audit-output/evidence/07-print-candidate-output.txt).

VERDICT: PASS
LEGITIMACY: LEGIT
