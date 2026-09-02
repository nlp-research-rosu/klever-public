# Independent Stage 3–5 audit: HumanEval `12-longest`

## Result

The selected Stage 3 classification, deterministic Stage 4 generation, and
Stage 5 Lean proof are legitimate. The audit mode is
`CLASSIFICATION_AND_PROOF`, the condition is `kit-semantics`, and the semantics
mode is `SUPPLIED_SEMANTICS`.

The launcher contract verified with audit-input digest
`0026373c85729ef8f8d390b1ecee152569e26e4547dc0c0b0ae1e2e48b7c0b81`.
Every hash for a mounted input matched, including all 788 individual Stage 1
file hashes. The launcher also records a `lean_invocation_sha256`, but no
Stage 5 invocation directory is part of the mounted audit input set; the
mounted `/candidate` workspace hash itself matched exactly.

Key evidence:

- launcher and mounted-tree hashes: [03-independent-hash-recomputation.log](evidence/03-independent-hash-recomputation.log) and [28-launcher-recorded-source-and-tree-hash-audit.log](evidence/28-launcher-recorded-source-and-tree-hash-audit.log);
- canonical rule reconstruction: [04-rule-inventory-and-manifest-bijection.log](evidence/04-rule-inventory-and-manifest-bijection.log);
- required preflight result: [15-required-klean-preflight-returned-evidence.log](evidence/15-required-klean-preflight-returned-evidence.log);
- independent Stage 4 bijection and target checks: [23-independent-stage4-bijection-and-target-hashes.log](evidence/23-independent-stage4-bijection-and-target-hashes.log);
- fresh clean/build: [19-fresh-stage5-lake-clean.log](evidence/19-fresh-stage5-lake-clean.log) and [20-fresh-stage5-lake-build.log](evidence/20-fresh-stage5-lake-build.log);
- exact axiom output: [21-proof-final-axioms-exact.log](evidence/21-proof-final-axioms-exact.log);
- operational witnesses and mutations: [24-operational-bridge-witnesses.log](evidence/24-operational-bridge-witnesses.log), [25-coordinated-wrong-bridge-control.log](evidence/25-coordinated-wrong-bridge-control.log), and [26-bad-seqlen-counterfactual-expected-failure.log](evidence/26-bad-seqlen-counterfactual-expected-failure.log).

## Producer and immutable-input integrity

The producer-source prerequisite passes:

- `/reference/generation-tools/klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`;
- `/reference/generation-tools/klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`;
- immutable generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`;
- producer bundle tree:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`.

The two file hashes match both `generator-manifest.json` and
`source-manifest.json`; the image ID matches both manifests and the
launcher-recorded producer bundle path; and the producer-tree hash matches
`/audit-input.json`. There is therefore no producer-provenance `AUDIT_ERROR`.

The independently recomputed major hashes are:

| Artifact | Observed hash |
|---|---|
| Stage 1 pipeline tree | `616879fa4fac0e0efd8499dbe2f4ff825c06468cdf0ed0d58cccf91ae600c27c` |
| Stage 1 Klean export tree | `08cef3f0ee823df2acdd572e8ba6729d4736aec5c38e389fc8f19a3d6ae204ff` |
| Stage 3 manifest file | `ff90de51ae9ffca23cbd2772793216f321aae0a664795c83cb40986958f39dcc` |
| Stage 4 selected artifact tree | `acc96a73f2be45d0b828205d4369cf13600b837f16f5b4a1d9522dd0cd0b45de` |
| Generated project tree | `129390716ae727db4051405e71fd0a8f2790a16c1b4b3155fb499a0a05d7a22d` |
| Candidate workspace tree | `fe3e9be2f3b9d53f2d386146b3720710c80112601c7d2284bf91b9330529646f` |

## Inventory reconstruction and Stage 3 classification

The trusted inventory code selected `VERIFICATION` from the final
`verification.k` kompile command and reconstructed its local source closure as
`VERIFICATION-BASE`, then `VERIFICATION`. It found exactly 16 rules in source
order.

- `verification.k` SHA-256:
  `9ddecb3cbc29344c765df7c22e58740e647007a383d525361549b6f35237461c`;
- canonical inventory SHA-256:
  `11838d318c7fc07f68702a780c2b4e461084d9eeb535b76cad4d65a4128c7631`.

For every rule, I independently recomputed the physical source span,
whitespace-normalized SHA-256, and `rule-<normalized SHA-256>` identity. The
inventory and protected manifest have equal counts, unique IDs, equal ID sets,
and exactly equal ordered ID lists. No rule is omitted, duplicated, inserted,
or reordered.

The independent classifications are:

| Source span | Rule role | Judgment |
|---|---|---|
| `VERIFICATION-BASE:9` | `isStringValue(_:Str) => true` | `DEFINITION` |
| `VERIFICATION-BASE:10` | `isStringValue(_:Val) => false [owise]` | `DEFINITION` |
| `VERIFICATION-BASE:13` | empty `allStrings` case | `DEFINITION` |
| `VERIFICATION-BASE:14–15` | recursive `allStrings` case | `DEFINITION` |
| `VERIFICATION-BASE:23–25` | definedness of the partial `Str` projection | `DOMAIN_LEMMA` |
| `VERIFICATION-BASE:27–29` | guarded `projectString` equation | `DEFINITION` |
| `VERIFICATION-BASE:30–32` | reverse projection/alias normalization | `DEFINITION` |
| `VERIFICATION-BASE:33` | typed `projectString` collapse | `DEFINITION` |
| `VERIFICATION-BASE:34–35` | `projectString` idempotence | `DEFINITION` |
| `VERIFICATION-BASE:41` | `seqLenString(str(CS)) = isLen(CS)` | `DEFINITION` |
| `VERIFICATION-BASE:47` | empty `scanLongest` case | `DEFINITION` |
| `VERIFICATION-BASE:48–58` | recursive strict-update fold | `DEFINITION` |
| `VERIFICATION-BASE:63` | empty `longestValue` case | `DEFINITION` |
| `VERIFICATION-BASE:64–66` | guarded nonempty `longestValue` case | `DEFINITION` |
| `VERIFICATION-BASE:67–68` | off-domain totalization | `DEFINITION` |
| `VERIFICATION:76–78` | guarded dynamic `seqLen` observation | `DOMAIN_LEMMA` |

The 14 definitions introduce or define named predicates, projections,
recurrences, or summaries. None is an ordinary state-changing execution rule.
The two domain lemmas are:

1. `rule-ddffe23dc5c6ffd5ffac0d16bb982569a790626473fe51f3053dbbcfd160d303`,
   which characterizes when the pre-existing partial `Val`-to-`Str`
   projection is defined; and
2. `rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122`,
   which equates fixed-semantics `seqLen(V)` with the typed string-length
   summary under the string guard.

Both are material to this source program: its loop compares
`len(string)` with `len(result)`, while the symbolic loop invariant stores
those values as `Val`. Neither exact rule was first proved by Stage 1 against
a module omitting it. The bridge-free connection claims prove only canonical
`str(CS)` instances, not either exact universally guarded inventory rule.
Thus neither can be promoted to `PROVED_DERIVED_LEMMA`. There are no
`OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. Every rule carrying
`simplification` or `simplification(10)` is classified as either
`DEFINITION` or `DOMAIN_LEMMA`.

The full reconstructed source, relevant fixed semantics, and source program
are recorded in [05-frozen-program-proof-and-relevant-semantics.log](evidence/05-frozen-program-proof-and-relevant-semantics.log) and [06-operational-semantics-core-and-len.log](evidence/06-operational-semantics-core-and-len.log).

## Deterministic Stage 4 generation

The required call to `tools.klean_preflight.check_generation`, with
`PYTHONPATH=/reference` and the three prescribed inputs, returned `PASS`:

- obligation count: `2`;
- trust declaration count: `43`;
- designated sorry count: `0`;
- internal `lake clean`: exit `0`;
- internal `lake build`: exit `0`.

The sandbox initially exposed a PID-namespace `/proc` mismatch: Lean asked for
`/proc/<getpid>/exe`, but that numeric path was absent even though
`/proc/self/exe` was valid. The included
[lean_proc_compat.c](evidence/lean_proc_compat.c) retries only that failed
executable-path lookup. With the pinned toolchain copied under
`/tmp/audit-work`, Lean reported version `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly as locked. The final
preflight and all proof checks then ran successfully. This resolved
environmental lookup failure does not alter Lean parsing, elaboration, kernel
checking, or the generated sources.

The independently classified domain-rule list and generated obligation list
are an exact ordered bijection. Each obligation carries the matching source
span, normalized rule hash, inventory hash, discovery-manifest hash, and
conjunct hash. The obligation-map file hash is
`713dd86a5018b31beb9aee55867c29b5dcbd4b56486ee46f9cff95a7c6afbeac`.

Mathematically, the two conjuncts preserve the frozen rules:

1. for every `V : SortVal`, successful `Str` projection is equivalent to
   `isStringValue V = true` and definedness of `V`; the latter becomes `True`
   because a Lean `SortVal` inhabitant is already a defined carrier value;
2. for every string-guarded `V`, fixed `seqLen V` equals
   `seqLenString (projectString V)`.

The `True` term is therefore the faithful lowering of source `#Ceil(V)`, not
an inserted replacement for a material condition. The string guard is
non-vacuous for the candidate, as witnessed by a two-character string.

The generated target is the exact conjunction of those two obligations:

- declaration: `Klean12Longest.Lemmas.targetStatement`;
- definition hash:
  `dadb1055c526593b5be24a69c6be17a00e9e20427c808c3eb57e1f7236502d47`;
- applied statement hash:
  `41e81d92cc08b7c494f9e98fbfa05b7171c1fb03197b1df2338d85615e69552a`.

The parsed target equals the generator manifest and `/audit-input.json`
exactly. Its copy in the fresh Stage 5 `Base` is unchanged. The candidate
does not declare or shadow `targetStatement`.

## Stage 5 proof, target identity, and trust

I created `/tmp/audit-work/stage5-proof-fresh`, copied only the candidate
project sources into it, and copied the immutable generated project into
`Base`. Candidate-source hashes match `/candidate`. I then ran:

```text
lake clean  # exit 0
lake build  # exit 0; Build completed successfully.
```

The candidate contains exactly one definition for each of the five target
parameters and exactly one `Proof.final`. Outside immutable `Base`, it
contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The trusted
final gate also independently clean-built the candidate and confirmed that
the normalized `Proof.final` type is exactly the generator target.

The exact kernel query returned:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. `propext` is one of the three standard Lean
foundational dependencies explicitly admitted by the trusted final gate
(`propext`, `Classical.choice`, and `Quot.sound`); it is not a
candidate-added or generated declaration. None of the 43 generated
trust-inventory axioms appears in the dependency set. Thus every actual
dependency is accounted for, and there is no unrecorded proof escape.

## Operational-bridge audit

Each target parameter was checked against its manifest `kore_symbol`, bound
source-rule IDs, the frozen K equations, and the supplied operational
semantics:

| Candidate definition | Operational judgment |
|---|---|
| `isStringValue` | `true` exactly on canonical `SortVal.inj_SortStr`; all other `Val` constructors are `false`, matching the constructor and `owise` K rules. |
| `projectString` | returns the enclosed `SortStr` on the guarded string case. Its empty-string result elsewhere is only a total completion outside the K rule's guard. |
| `seqLen` | structurally counts string, list, tuple, and set sequences and implements the two guarded `rangeLen` formulas. It returns `0` only where fixed `seqLen` has no applicable rule. |
| `seqLenString` | structurally computes `isLen` on the string's `IntSeq`, exactly matching line 41 of `verification.k`. |
| `project:Str?` | returns `some value` exactly for a singleton K sequence containing a canonical `Str`; otherwise it returns `none`, matching the K sort projection used by the first domain lemma. |

The two-character witness produced `true`, length `2`, typed length `2`, and
a successful projection. The official `Inj SortIterable SortVal` instance
canonically flattens an iterable string to the same direct string
representation (`rfl`), and that path produced the same results. A manually
constructed, noncanonical nested Lean constructor produced
`false/0/none`; it is not the image of the generated `inj` operation and is
not a translated K value. Defined list, tuple, set, positive-range, and
negative-range examples produced `2, 2, 2, 3, 3`, respectively.

As an adversarial control, coordinated constant-false/constant-zero
definitions can satisfy the bare parameterized proposition. This demonstrates
why the required operational-bridge audit is necessary; those definitions do
not implement their manifest-bound KORE symbols and would be rejected. The
actual candidate is not such a model. Holding its honest definitions fixed
while mutating only `seqLen` to zero caused Lean to fail with the concrete
residual:

```text
case right.inj_SortStr
x✝ : SortStr
⊢ 0 = Proof.intSeqLength✝ x✝.1
```

The actual bridge is therefore source-sensitive, nonconstant, and
non-vacuous on the source program's string domain.

VERDICT: PASS
LEGITIMACY: LEGIT
