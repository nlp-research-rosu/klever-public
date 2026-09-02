# Independent Stage 3–5 audit: HumanEval `77-iscube`

## Result and scope

This audit covered condition `bare`, semantics mode
`GENERATED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`.
Candidate and provenance text was treated as untrusted evidence. The only
provenance-side code invoked was the trusted code under `/reference/tools`,
plus the pinned Lean toolchain for the expressly required clean build.

The audit independently finds two genuine domain lemmas, an exact two-rule
Stage 4 obligation export, and an honest Stage 5 proof of the fixed target.

## Frozen-input identity and inventory reconstruction

I called
`tools.k_rule_inventory.inventory_verification(Path("/reference/k-proof"))`
with `PYTHONPATH=/reference`. The selected verification module is
`GAP-VERIFICATION`; its local closure inside `verification.k`, in source
order, is `VERIFICATION`, `GAP-VERIFICATION`.

Recomputed hashes:

- `verification.k` SHA-256:
  `c941d95f59a2ddb57298abbb42ad637dfc84c7753c2907462ce4ebc3cd966659`
- Canonical inventory SHA-256:
  `768c6d425e02156c7113c418107467c11510230db45758138d0307d7efd017c9`

The reconstructed entries are:

| Source span | Recomputed normalized hash / source-rule ID | Attributes | Independent classification |
|---|---|---|---|
| `VERIFICATION` 11–24 | `de3f9727c1b2c9f19559bcf49d9facf57997eb3c9d4715f670ff6644a77098f9` / `rule-de3f9727c1b2c9f19559bcf49d9facf57997eb3c9d4715f670ff6644a77098f9` | none | `DEFINITION` |
| `VERIFICATION` 27–27 | `b88003e929c70fa00f8441eaf77e74ba66845261dacd5efbb19e5da9b5a59865` / `rule-b88003e929c70fa00f8441eaf77e74ba66845261dacd5efbb19e5da9b5a59865` | none | `DEFINITION` |
| `GAP-VERIFICATION` 36–44 | `71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027` / `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027` | `simplification` | `DOMAIN_LEMMA` |
| `GAP-VERIFICATION` 46–54 | `5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f` / `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f` | `simplification` | `DOMAIN_LEMMA` |

For every entry, I separately re-sliced the recorded physical source lines,
re-normalized the exact rule text with whitespace joining, recomputed the
normalized SHA-256, and regenerated `source_rule_id`. Every line span, text,
hash, and identity matched.

The Stage 3 manifest has exactly these four IDs exactly once and in the same
order. It has no omitted, duplicated, unknown, extra, or reordered entry.
Its inventory hash matches the independently reconstructed inventory. This is
a bijection, not merely a set-membership comparison.

Evidence:

- `evidence/inventory-reconstruction.log`
- `evidence/reconstruct_inventory.py`
- `evidence/recomputed-hashes-final.log`

## Independent classification judgment

### The two definitions

`iscubeProgram => Module(...)` is a named proof-term/program-tree
abbreviation. Its constructor tree agrees with the frozen `solution.mpy` and
the control structure of `solution.py`: normalize a negative input, initialize
`n` to zero, increment while `n*n*n < a`, and return `n*n*n == a`. It does not
skip or replace the MPY execution rules. It therefore satisfies the requested
`DEFINITION` category.

`cube(I) => I *Int I *Int I` defines the named mathematical summary used in
the claims. It is also a `DEFINITION`.

Neither rule is an ordinary execution/observation rule, a derived theorem, or
a domain fact.

### The two domain lemmas

The first simplification rule assumes, over mathematical integers:

`0 ≤ I`, `I ≤ N+1`, `0 ≤ N`, `0 < D`,
`D < (N+1)^3-N^3`, and `I^3 < N^3+D`.

If `I` were not below `N+1`, the upper bound would force `I=N+1`.
Then the last two strict inequalities would yield both
`(N+1)^3 < N^3+D` and `N^3+D < (N+1)^3`, a contradiction. Thus
`I < N+1`. This is a valid, nontrivial open-cube-gap arithmetic lemma.

The second rule has the same bounds but assumes `I^3 ≥ N^3+D`. If
`I ≠ N+1`, integrality and `I ≤ N+1` imply `I ≤ N`. Since `I` and `N`
are nonnegative, monotonicity gives `I^3 ≤ N^3`; positivity of `D` gives
`N^3 < N^3+D`, contradicting the guard. Thus `I=N+1`.

These facts are directly relevant to the loop in the frozen program: they
establish whether the incrementing loop index is still below `N+1` or has
reached it for an input strictly between consecutive cubes. They are used by
the `GAP-SPEC` loop invariant and its positive/negative non-cube
postconditions.

They are not `PROVED_DERIVED_LEMMA`s. `prove.sh` first builds
`GAP-VERIFICATION` with both rules already present and then proves
`GAP-SPEC`. There is no earlier proof of either exact rule against a module
that omits it. They are not definitions and do not perform ordinary program
execution. `DOMAIN_LEMMA` is therefore the only valid category. Both
`simplification` rules consequently satisfy the policy that a simplification
must be a `DEFINITION` or `DOMAIN_LEMMA`.

Finite adversarial support over thousands of satisfiable ground instances
found no counterexample. This testing is supplementary to the arithmetic
argument. The run found 19,164 first-rule and 1,113 second-rule antecedent
instances in the selected range, including concrete witnesses, and rejected
deliberate off-by-one conclusion mutations.

Evidence: `evidence/domain-lemma-adversarial-checks.log`.

## Recorded hashes and provenance bindings

The proper trusted digest was used for each recorded field:
`pipeline_contract.sha256_tree` for selected stage/workspace artifacts and
`klean_export.tree_digest` for frozen/exported Klean trees.

All mounted resolution bindings matched:

| Bound artifact | Recomputed hash |
|---|---|
| Stage 1 selected workspace | `3b1f3d508fbac7cf3d76dab301ea969394befd37ed5e6e8a9c94b974c231873f` |
| Stage 1 frozen export | `bb5a6d7c5a368cef32fdefa06f1fefce90aab1a7240b995eb522702fc03a9e2d` |
| Stage 2 selected audit tree | `78bdd2de264287aea9b48e4430b0cb15401288bf79db1012b2bf1b9c1b80386f` |
| Stage 3 manifest file | `15dc8f8202c2f2bba0a6043e762654a6ecbc4ebdd979765a531e7635eb0888b3` |
| Stage 4 selected generation tree | `6d7a41fd0b762964edeb22582ee13fa74302e94f6c631f92442d0628618e2721` |
| Stage 4 generated project | `01021315ed43f873b7dfd83015184249e65b44416a4e3a4d94bf6e27301f68d1` |
| Stage 5 mounted workspace | `c1993c0d3323bbb956a8f0de9664263c1ae083804a7a05df52073eb1bf70b19d` |

All nine frozen Stage 1 per-file hashes in `stage1_source_hashes`, including
`verification.k`, `semantic.k`, `spec.k`, `solution.py`, and `solution.mpy`,
also matched byte-for-byte.

The launcher separately records a Stage 5 invocation-tree hash and hashes of
invocation logs. That invocation directory is not one of the mounted audit
inputs and was not used as proof evidence. The mounted Stage 5 workspace—the
candidate actually audited—does match its recorded tree hash exactly.

Evidence: `evidence/recomputed-hashes-final.log`.

## Deterministic Stage 4 generation

I reran:

```text
PYTHONPATH=/reference python /audit-output/evidence/run_preflight.py
```

using `/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and
`/reference/klean-toolchain.lock.json`.

The sandbox initially denied Lean's own
`readlink("/proc/<pid>/exe")`, so the first preflight attempts failed before
compilation. I retained those failures. For the successful rerun, I used an
audit-owned preload shim that preserves the real `readlink` syscall and, only
when that exact self-executable lookup fails, returns the current invocation
path. The shim does not modify the toolchain, generated sources, candidate,
target, or proof. With the pinned Lean 4.22.0 sysroot made explicit, the same
trusted `check_generation` returned `PASS`.

Successful returned evidence:

- frozen input:
  `bb5a6d7c5a368cef32fdefa06f1fefce90aab1a7240b995eb522702fc03a9e2d`
- discovery manifest:
  `15dc8f8202c2f2bba0a6043e762654a6ecbc4ebdd979765a531e7635eb0888b3`
- generated tree:
  `01021315ed43f873b7dfd83015184249e65b44416a4e3a4d94bf6e27301f68d1`
- obligation count: 2
- generated trust declaration count: 44
- designated `sorry` count: 0
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `1ffacd40cb932a86bbc033055728944c6526acef93d57b2658b95d94b4f41dc2`

Evidence:

- successful result: `evidence/preflight-rerun-success.log`
- initial failures: `evidence/preflight-rerun.log`,
  `evidence/preflight-rerun-with-toolchain.log`,
  `evidence/preflight-rerun-pinned-env.log`
- shim source/build: `evidence/readlink_self_shim.c`,
  `evidence/readlink-shim-rebuild.log`

### Source-rule/obligation bijection and mathematical adequacy

The independently classified domain set has exactly the two rules at lines
36–44 and 46–54. `input-manifest.json`,
`generator-manifest.json`, and `generated/obligation-map.json` preserve their
IDs, source order, source spans, normalized hashes, inventory hash, and
discovery-manifest hash. The obligation list contains each exactly once and
contains no other rule.

The first Lean conjunct is exactly the first K rule: the complete six-part
Boolean `requires` guard implies `I < N+1 = true`. The second conjunct is
exactly the second K rule: its complete guard implies `I == N+1 = true`.
Integer subtraction, addition, multiplication, comparisons, equality, and
Boolean conjunction all remain explicit target parameters bound to their KORE
symbols. No guard was dropped, strengthened to remove cases, or replaced with
`True`; no result was weakened; and no unrelated fact was added.

The antecedents are genuinely satisfiable under the correct operational
meanings. For example, `(N,I,D)=(1,1,1)` satisfies the first antecedent and
`(1,2,1)` satisfies the second. The Lean bridge audit checks both witnesses.
Thus neither conjunct is vacuous under the frozen semantics.

The selected status is ordinary `OK`/preflight `PASS`, not
`KLEAN_NO_OBLIGATIONS`, which is correct for the nonempty true domain set.

## Fixed generated target

The generated target is uniquely located at
`Klean77Iscube/Lemmas.lean` and declared as
`Klean77Iscube.Lemmas.targetStatement`.

- definition SHA-256:
  `c3c8b0cf83982c67b43958d67a0d411a787722dfb126effabceb89bbd25d9fd6`
- applied statement SHA-256:
  `62d5c1728b668edca6cedca0e3d7d020894b66bc4a1c9be50e791dbca195cebb`
- applied statement:
  `Klean77Iscube.Lemmas.targetStatement «_-Int_» _andBool_ «_>=Int_» «_<Int_» «_<=Int_» «_==Int_» «_+Int_» «_*Int_»`

I independently regenerated the expected target definition from the two
obligation-map conjuncts. Its hash equals the actual definition hash. The full
target object, including all eight parameter names, KORE symbols, types,
source-rule links, and binding hashes, is identical in the generated tree,
generator manifest, recorded Stage 4 preflight, and audit input.

Evidence: `evidence/recomputed-hashes-final.log`.

## Stage 5 fresh build and candidate integrity

I created `/tmp/audit-work/77-iscube-proof-audit`, copied only the candidate
project sources/metadata into it, and copied the immutable generated project
to `Base`. Before and after building, the fresh `Base` tree digest remained
`01021315ed43f873b7dfd83015184249e65b44416a4e3a4d94bf6e27301f68d1`,
and its target object remained exactly equal to the selected generated target.
The copied `Proof.lean`, `lakefile.lean`, `lake-manifest.json`, and
`lean-toolchain` were byte-identical to `/candidate`.

I then ran both required commands:

```text
lake clean
lake build
```

Both exited 0. The complete build output ends with
`Build completed successfully.` The only warnings are generated
`Lemmas.lean` unused-binder lints; they do not alter the theorem.

Evidence:

- `evidence/fresh-copy-identity.log`
- `evidence/proof-lake-clean.log`
- `evidence/proof-lake-build.log`

The trusted static candidate gate also passed. The candidate:

- has exactly one `def` for each of the eight required target parameters;
- has exactly one theorem `Proof.final`;
- gives `Proof.final` exactly the fixed applied target, confirmed both
  lexically and with a separate Lean `#check`;
- stays in namespace `Proof`, so it neither changes nor shadows
  `Klean77Iscube.Lemmas.targetStatement`;
- contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

Evidence:

- `evidence/candidate-static-gate.log`
- `evidence/proof-identity-check.log`

## Operational-bridge audit

`SortInt` is generated as Lean `Int` and `SortBool` as Lean `Bool`. Each
candidate definition implements the frozen K hook meaning rather than a
convenient theorem-specific interpretation:

| Target parameter / KORE symbol | Source-rule links | Candidate definition | Operational judgment |
|---|---|---|---|
| `«_-Int_»` / `Lbl'Unds'-Int'Unds'` | both domain rules | `x - y` | exact unbounded integer subtraction |
| `_andBool_` / `Lbl'Unds'andBool'Unds'` | both | `x && y` | exact Boolean conjunction; agrees with generated `true,B ↦ B` and `false,_ ↦ false` equations |
| `«_>=Int_»` / `Lbl'Unds-GT-Eqls'Int'Unds'` | second rule | `decide (x >= y)` | exact integer greater-than-or-equal Boolean |
| `«_<Int_»` / `Lbl'Unds-LT-'Int'Unds'` | both | `decide (x < y)` | exact integer strict-less-than Boolean |
| `«_<=Int_»` / `Lbl'Unds-LT-Eqls'Int'Unds'` | both | `decide (x <= y)` | exact integer less-than-or-equal Boolean |
| `«_==Int_»` / `Lbl'UndsEqlsEqls'Int'Unds'` | second rule | `decide (x = y)` | exact integer equality Boolean |
| `«_+Int_»` / `Lbl'UndsPlus'Int'Unds'` | both | `x + y` | exact unbounded integer addition |
| `«_*Int_»` / `Lbl'UndsStar'Int'Unds'` | both | `x * y` | exact unbounded integer multiplication |

These meanings agree with the generated Prelude hook definitions and with the
operators used in the two frozen K rules. They also agree with the frozen MPY
semantics and source program where those operators occur.

Independent Lean checks covered negative operands, reversed inequalities,
equality boundaries, unequal equality, Boolean truth-table branches, zero and
sign-sensitive arithmetic. Representative outputs include `5-9=-4`,
`-3 < -2 = true`, `-3 ≥ -2 = false`, `5+(-9)=-4`, and
`(-3)*4=-12`.

For every parameter I also defined a constant, identity, or otherwise wrong
counterfactual and proved a concrete witness separates it from the candidate
definition. As a sensitivity check, a constantly-false `andBool` can make the
parameterized target provable vacuously. That demonstrates why a clean target
proof alone is insufficient. The candidate does not use that escape: it uses
the exact Boolean conjunction, and both real antecedents have checked
satisfying witnesses.

Evidence: `evidence/operational-bridge-and-mutation-checks.log`.

## Proof identity, mathematical proof, and axiom accounting

`Proof.final` proves the exact fixed target, not a restatement or duplicate.
For the first conjunct it splits on `I < N+1`; in the other branch the upper
bound gives `I=N+1`, after which the cube-gap and loop-guard inequalities are
contradictory. For the second conjunct it splits on `I=N+1`; otherwise
`I≤N`, nonnegative multiplication yields `I^3≤N^3`, and `D>0` plus the guard
yields `N^3<I^3`, again a contradiction. This matches the independent
arithmetic classification argument.

I ran Lean with the exact command `#print axioms Proof.final`. Its exact result
was:

```text
'Proof.final' depends on axioms: [propext]
```

The trusted final-gate policy explicitly includes the Lean core axioms
`Classical.choice`, `propext`, and `Quot.sound` in addition to names recorded
by `trust-inventory.json`. Reconciliation found:

- used axioms: only `propext`;
- `sorryAx`: absent;
- unexpected/unrecorded proof-trust escapes: none;
- used generated trust declarations: none of the 44 recorded declarations.

Thus the candidate proof does not depend on any generated Map/List/Set or
other Klean boundary axiom.

Evidence:

- `evidence/proof-print-axioms-success.log`
- `evidence/axiom-reconciliation.log`

## Evidence summary

The raw results and audit-owned reproducer sources are under
`/audit-output/evidence/`. Failed environmental startup attempts were retained
alongside the successful pinned-toolchain runs. No prior review or purported
PASS was used as a premise for this verdict. Exact commands and their
corresponding log names are indexed in `evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
