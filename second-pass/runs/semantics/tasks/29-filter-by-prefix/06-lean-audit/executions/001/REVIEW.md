# Independent Stage 3–5 audit: `29-filter-by-prefix`

Scope: condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`, launcher mode
`CLASSIFICATION_AND_PROOF`.

## Result

The protected Stage 3 classification is complete and mathematically correct.
The deterministic Stage 4 generation has intact producer provenance and maps
the two genuine domain lemmas bijectively to the fixed Lean target. The Stage 5
candidate clean-builds, proves exactly that target without axioms, and gives
the target parameter the exact recursive operational meaning of the frozen K
`valSeqConcat` symbol.

## Frozen-input and producer provenance

I recomputed the launcher binding and every mounted hash recorded in
`/audit-input.json`. The canonical audit-input digest is
`c9daeb05d432f1ac7467b935a160d0aa94d7805c0e8bfca39424b445ca1f3871`.
The following all matched:

- Stage 1 full tree:
  `cfcfe8ca15c9e62a1eacc40fddc87a5700a97c9ee4cb8f9d32d2062d84761fa8`.
- Stage 1 export tree:
  `c94a779ff431973be373191d47ba26cb5cd8f3663fae32dd76fd270d72544920`.
- Stage 2 audit tree:
  `d7e9f487bf1d28c624697a48642720e40e563fa200e7b698631db7533eed7ab3`.
- Stage 3 manifest:
  `a0d7580e1b7927f9bc8dbdae0915f4284f379b6896af7c45ad1fd750ffdaedd5`.
- Stage 4 generation tree:
  `bb96f5901d34942ad08ef77be0533805293cf42abaa50e2f133178dae9d71c3c`.
- Generated project tree:
  `1d3c833efda1f0d9c8d67e0548f189fd6be6cbe55eb6b262e6a3233d92e7dbbe`.
- Producer bundle tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.
- Candidate tree:
  `e51191e1d295510fb2fcc12a47d0e026195fa843a93cc75fabe26213b2d4c9ef`.
- Every individual Stage 1 source hash listed by the launcher.

The launcher records a Stage 5 invocation hash, but that invocation directory
is not one of the mounted audit inputs. I did not use it or any prior Stage 5
log as evidence.

Before evaluating generation, I hashed the exact mounted producer sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`.
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`.

Both hashes equal the generator manifest and source manifest. Both manifests,
and the basename of the producer path recorded in the audit input, identify
the immutable generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The producer bundle contains exactly those two sources plus
`source-manifest.json`. There is no producer-provenance error.

## Inventory reconstruction

Using the trusted rule-inventory implementation on the frozen
`verification.k`, I reconstructed the local closure selected by `prove.sh`.
The closure contains the single local module `VERIFICATION`; its import
`MPY` is supplied from the required semantics files rather than another local
module in `verification.k`.

The reconstructed inventory contains nine rules and has whole-inventory hash
`bae4d241cf5d1f87e3688240b9e5231b0c9e60229ef325038b2b5ec659e1c117`.
For each row below, the `source_rule_id` is `rule-` followed by the shown
normalized SHA-256.

| Lines | Normalized SHA-256 | Independent classification | Rule role |
|---|---|---|---|
| 8–21 | `61ad22e91cf1d14a56c700f11857dd29831578a6b40d0572a243f6d516c9c52d` | `DEFINITION` | `filterByPrefixDef` macro expands to the translated source function AST. |
| 28 | `599e41d4a9d9ad6575d0c83c9adfb5897b57da250aa3fcd4b6b3948d5d38cfc8` | `OPERATIONAL_RULE` | Empty `stringList` iterator step. |
| 29–30 | `a3ddd233cb42bb15fccbe05d5ffd00bf4b460fcd7fc482613d9afea1b394c43a` | `OPERATIONAL_RULE` | Nonempty `stringList` iterator step. |
| 34–35 | `30f5db2b3a8fd9b20dc7a47b44c33129a183aca23513f2f4c9625795c94333f4` | `DEFINITION` | Base equation of the named `prefixFilter` summary. |
| 36–39 | `13aa965c78704fb137f385111497f865604cbdac678b96ff482033a5a5ce8bb7` | `DEFINITION` | Retaining recursive equation of `prefixFilter`. |
| 40–43 | `280dd2b182ad4aa8740abfb49cf0d4b811a2905793dcbf7164ed1ef1181d0c2c` | `DEFINITION` | Dropping recursive equation of `prefixFilter`. |
| 46 | `656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb` | `DOMAIN_LEMMA` | Symbolic right identity of `valSeqConcat`. |
| 48–50 | `9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97` | `DOMAIN_LEMMA` | Associativity of `valSeqConcat`. |
| 54–56 | `1d5d8612675bca2b2d6063306a951720465c08e01ed82c31035b38c7829e56a6` | `OPERATIONAL_RULE` | Returned-list heap observation by `#checkFilter`. |

The Stage 3 manifest contains these same nine identities in the same order.
There are no omissions, duplicates, extras, changed identities, or
unclassified rules. Its inventory hash matches. All five rules bearing
`simplification` are classified as either `DEFINITION` (the three
`prefixFilter` equations) or `DOMAIN_LEMMA` (the two list-algebra equations).

### Classification judgment

The three `prefixFilter` equations are a genuine base/recursive definition of
a named mathematical summary. Their two recursive guards cover the Boolean
outcomes of the total `startsWith` function. The macro rule similarly defines
a named proof term. The iterator rules and `#checkFilter` change or observe an
execution configuration and are ordinary operational/observation rules.

There is no `PROVED_DERIVED_LEMMA`. In particular, Stage 1 installs right
identity and associativity as simplification rules before either claim in
`spec.k`; there is no earlier proof of either exact rule against a module from
which it is absent.

Those two rules are genuine, relevant domain lemmas. Frozen `MPY-LIST` defines
`valSeqConcat` only by recursion on its first operand:

```text
valSeqConcat(.ValSeq, T) = T
valSeqConcat(vCons(V, S), T) = vCons(V, valSeqConcat(S, T))
```

Right identity for a symbolic first operand and associativity are algebraic
consequences, not additional defining clauses. They are needed to normalize
the symbolic accumulator in the loop invariant. This directly corresponds to
the source operation `result.append(string)`, whose frozen heap rule updates
the list with `valSeqConcat(VS, vCons(V, .ValSeq))`. Neither lemma is
irrelevant to the program or postcondition.

## Deterministic Stage 4 generation

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required mounted inputs. The first attempt exposed an audit-sandbox
issue: Lean 4.22 reads `/proc/<getpid()>/exe`, but this sandbox exposes outer
PIDs in `/proc`. A local preload shim redirected only such reads to the
equivalent `/proc/self/exe`; it did not modify any frozen or generated input.
The unchanged trusted checker then returned `PASS`, with two obligations,
zero sorries, 48 generated trust declarations, and successful `lake clean`
and `lake build`.

The independent structural and mathematical checks found:

- The domain-rule sequence and obligation sequence are exactly the same two
  IDs, in order, with no duplicate.
- Each obligation has the exact reconstructed source span, normalized hash,
  inventory hash, discovery-manifest hash, and conjunct hash.
- The first conjunct is exactly universal right identity.
- The second conjunct is exactly universal associativity. Its quantified
  variable order is `C`, `B`, `A`, but the body uses `A`, `B`, `C` in the
  source-rule positions; universal binder ordering does not weaken it.
- Every quantified variable occurs materially, neither conjunct contains
  `True` or `False`, and neither equality is textually reflexive.
- The obligation-map hash is
  `a5121420140f2c07534dadf8decd0296b756f0e0084b8dbe30ac3d4a749b3d48`.
- The target is the exact conjunction produced from those obligations. There
  is exactly one target declaration.

The independently reconstructed fixed target is:

- Declaration:
  `Klean29FilterByPrefix.Lemmas.targetStatement`.
- File: `Klean29FilterByPrefix/Lemmas.lean`.
- Definition hash:
  `791b790c52c69aa4fc975872dc22c252555973f3fd2b9931098a1096de0ca587`.
- Applied statement:
  `Klean29FilterByPrefix.Lemmas.targetStatement «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»`.
- Statement hash:
  `5c1a27a58891e05308b0db4fe5206dd96f61eff0a5c81e96a698a7392a60ce7c`.

This target and its parameter binding equal the generator manifest, the audit
input, and the rerun preflight result byte-for-byte/hash-for-hash. The single
parameter binds the expected `valSeqConcat` KORE symbol to both and only the
two domain-rule IDs.

## Stage 5 Lean proof

I created the fresh project
`/tmp/audit-work/human29-proof.S56dOa`, copied the mounted candidate into it,
and copied the immutable generated project contents into its empty `Base`
directory. After the build, `Base` still had the generated tree hash
`1d3c833efda1f0d9c8d67e0548f189fd6be6cbe55eb6b262e6a3233d92e7dbbe`.
Thus the candidate did not alter the target or any generated source.

Both required commands succeeded:

- `lake clean`: exit 0, no output.
- `lake build`: exit 0, ending with `Build completed successfully.`

The candidate-authored Lean sources are only `Proof.lean` and
`lakefile.lean`. After masking comments and strings, they contain no `sorry`,
`admit`, or `unsafe`, no `axiom` or `opaque` declaration, and no declaration
that shadows `targetStatement`.

`#print Proof.final` gives exactly:

```text
theorem Proof.final : Klean29FilterByPrefix.Lemmas.targetStatement
  Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := ...
```

An explicit type check against the fixed generated application also succeeds.
There is no duplicated or weakened theorem.

`#print axioms Proof.final` reports exactly:

```text
'Proof.final' does not depend on any axioms
```

Therefore the proof uses none of the 48 declarations in the generated,
hash-bound trust inventory. It uses no `sorryAx` and has no unrecorded trust
dependency.

### Operational bridge

The target alone does not uniquely characterize concatenation: the
counterfactual function `leftProjection a b := a` satisfies both right identity
and associativity. I machine-checked that fact as an adversarial test. Thus a
clean proof of the target would not by itself establish the bridge.

The candidate passes the stronger operational check. Frozen `SortValSeq` has
exactly the empty and `vCons` constructors corresponding to K `.ValSeq` and
`vCons`. The candidate definition has exactly the two frozen `MPY-LIST`
branches:

- empty first operand returns the suffix;
- nonempty first operand preserves the head and recursively concatenates its
  tail with the suffix.

I transcribed the two frozen K equations into an independent Lean model and
proved universally, by structural recursion, that the candidate equals that
model for every pair of `SortValSeq` values. Ground checks also covered empty
left, empty right, one-plus-one, and two-plus-one lists with distinct values,
preserving element order. A mutation that drops left-hand elements is
distinguished by a one-element witness, and the candidate is distinguished
from the target-satisfying left projection by an empty-plus-nonempty witness.

This is the operational meaning used by the frozen source's `append` heap
update and by both source-rule obligations. The definition is neither
constant, identity, hard-coded, vacuous, nor merely convenient.

## Evidence

Commands are recorded in `evidence/COMMANDS.md`. Decisive raw results are:

- `01-producer-provenance.log`
- `02-recorded-hashes.log`
- `03-inventory-reconstruction.log`
- `04-classification-source.log`
- `05b-stage4-preflight-retry.log`
- `06b-stage4-obligation-audit.log`
- `07-stage5-lake-clean.log`
- `08-stage5-lake-build.log`
- `09-print-axioms.log`
- `10-proof-identity.log`
- `11c-operational-bridge-tests.log`
- `12-stage5-source-and-trust-audit.log`
- `13-stage5-source-excerpts-and-scan.log`

The associated audit scripts and Lean test sources are preserved beside the
logs. `05-stage4-preflight.log` records the initial PID-namespace failure.
`11-operational-bridge-tests.log` records an invalid pattern in the first
audit-authored test draft; it was corrected before the successful `11b` and
final strengthened `11c` runs. Neither superseded diagnostic is a candidate
failure.

VERDICT: PASS
LEGITIMACY: LEGIT
