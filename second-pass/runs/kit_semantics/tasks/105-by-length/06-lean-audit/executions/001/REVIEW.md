# Independent Stage 3–5 audit: `105-by-length`

## Scope and outcome

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_AND_PROOF`; the
semantics mode is `SUPPLIED_SEMANTICS`. I did not rely on the prior K audit,
prior classifications, prior build logs, or candidate comments as authority.

Stage 3 and Stage 4 are sound and structurally intact. The Lean project also
clean-builds, proves the exact generated target, and is axiom-free. The overall
submission nevertheless fails the required Stage 5 operational-bridge check:
the candidate definition bound to the global KORE `applyCmp` symbol implements
only six integer comparisons and returns `false` for every other input. The
frozen supplied semantics defines many of those discarded cases with different
results. Concrete boolean, string, and `None` equality witnesses all expose the
mismatch.

## Input and producer provenance

I first hashed the two exact generation-time producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

These values match all three applicable bindings: `generator-manifest.json`,
`generation-tools/source-manifest.json`, and the files themselves. The source
manifest and generator manifest both name immutable image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the same image digest is the basename of the producer-source path recorded in
`/audit-input.json`. The producer bundle contains exactly the two source files
and `source-manifest.json`. Its independently recomputed pipeline tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching the audit input.

The trusted audit-input contract validated with resolved-input digest
`2b33c65db7c2dcf18328053736e0789fee89a6536aa142cc313668e448f307a2`.
All mounted hashes recorded by the launcher matched:

- Stage 1 pipeline tree:
  `14e1f68e49e379a8cc0b7d20c097a2d26bd08ae55fa7d35bc7f0ec3ef7991aea`
- Stage 1 export tree:
  `5cab8bdf04771b50412d561b8edcfaa3ebf1f7550a6acf8f386fb274dcf92db4`
- selected Stage 2 tree:
  `9067024337babc3410b97a0a958dd849d026ea75a4bcc7802ec24d3709c28ef8`
- Stage 3 manifest:
  `ea297e7947d65f3f8dfbf31581af286687b0c08ef32a7e225f271c65124ec7bb`
- selected Stage 4 generation tree:
  `a4b7d6b297bbb66acfedfce2f7e9880a6eb32e7e5efe6fbacf7381832f1e1fb9`
- generated project:
  `bcbd88215a42455adad5d49c22a5ebe24958d2fdad0016e2c718c96379e89da8`
- Stage 5 candidate pipeline tree:
  `24b751d8b1b02a81c018c8d4defd05d2d051f2e939f615622ac5a768013324e5`

All 780 individually recorded Stage 1 source-file hashes were present and
matched. The audit input also records a Stage 5 invocation digest, but the
invocation directory is not a mounted audit input; the mounted candidate
workspace is independently bound by `lean_workspace_sha256`, and the trusted
final gate accepted the complete launcher binding.

Raw and structured provenance evidence is in
`evidence/01-provenance-and-hashes.log` and
`evidence/01-provenance-and-hashes.json`.

## Inventory reconstruction and Stage 3 classification

Using the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen Stage 1 workspace, the selected main module is `VERIFICATION` and its
local verification-file closure is exactly `["VERIFICATION"]`.
`verification.k` hashes to
`9696cfcae2e2436114cda643ad130cf607767bf60afd368c0a63ddbe9a1c863b`.
The canonical ten-rule inventory hashes to
`aae99af3f9847ce2ab92c4c7c79358ecfcde2abeaa10a418c3fd084758889f0e`.

The reconstructed rules, in canonical order, are:

| Span | Rule head | Normalized SHA-256 | Independent class |
|---|---|---|---|
| 8–14 | `collectLoopBody` | `747dafbcb7dbc93d4b10f99002817e64857a8e4f4d9f3f604bb3d90fb4181465` | `DEFINITION` |
| 17–22 | `collectDigitBody` | `b1c919f173ebaeae5a0a9dcc7a927d0995652e12f3c7a1e4686c6f0162042ead` | `DEFINITION` |
| 25–53 | `byLengthBody` | `ee637e6a46f75586aa270feb662c49c0a1bd3155822a7ffcd090506423e50c76` | `DEFINITION` |
| 56–66 | `solutionModule` | `d4e50b0b16832b7d70466127d7bea606a9302a86e815d82c3ae539a6dcc7ef4d` | `DEFINITION` |
| 70 | `allInts(.ValSeq)` | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` |
| 71–72 | `allInts(vCons(...))` | `fa394f9b181c0d7a89141e7d4e865895db0443da2d399ebaeb0492e3a9b63ed4` | `DEFINITION` |
| 75–78 | `applyCmp("==", V, I)` | `4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430` | `DOMAIN_LEMMA` |
| 84 | `collectAcc(.ValSeq, ...)` | `71bf531cb528d1347e0a5832ea7e03bbac0c3023754ea73e59f68348ed0f3bae` | `DEFINITION` |
| 85–97 | `collectAcc(vCons(...), ...)` | `d0c98c20c0cd5ca4e7da32399bf306e24d37834742a0c41c2baec6f58fd809e7` | `DEFINITION` |
| 101–118 | `byLengthVS` | `a37220915a776fe106be230a864954901967f8c85ed0fbb76b60e2233efefb0a` | `DEFINITION` |

Each `source_rule_id` is exactly `rule-` followed by the corresponding
normalized hash. The protected manifest has the same ten identities in the
same order, with no omission, extra identity, duplicate, reordered identity,
or inventory-hash difference.

The first four rules name exact source ASTs/macros. The two `allInts` rules and
two `collectAcc` rules are base/recursive defining equations. `byLengthVS`
defines the final summary as nine concatenated collections. They are therefore
definitions, not execution rules or assumed mathematical facts.

The only simplification rule is:

```k
rule applyCmp("==", V:Val, I:Int)
  => {V}:>Int ==Int I
  requires isInt(V)
  [simplification]
```

It is not an ordinary execution rule: the supplied `MPY-INT` semantics already
has the concrete `applyCmp("==", I1:Int, I2:Int)` execution equation. It is not
a proved-derived lemma either: Stage 1 compiles it into `VERIFICATION` before
both K claims and contains no earlier proof of the exact rule in a module that
omits it. It is therefore correctly classified as `DOMAIN_LEMMA`.

The lemma is relevant. The frozen source helper compares every symbolic array
element with a digit; the loop claim summarizes matching elements with
`collectAcc`, whose recurrence tests the projected integer equality, and the
final postcondition is built from those summaries. It is neither detached from
the program nor unrelated to the postcondition.

Full reconstructed rule text and the bijective comparison are in
`evidence/02-reconstructed-rule-inventory.json` and
`evidence/02-inventory-manifest-comparison.json`.

## Deterministic Stage 4 generation

I reran:

```text
PYTHONPATH=/reference python3 evidence/03_run_preflight.py
```

through `tools.klean_preflight.check_generation` with the required Stage 1,
Stage 3, Stage 4, and toolchain-lock paths. The trusted preflight returned
`PASS`, one obligation, generated tree hash
`bcbd88215a42455adad5d49c22a5ebe24958d2fdad0016e2c718c96379e89da8`,
47 inventoried generated trust declarations, zero designated sorries, and
successful `lake clean`/`lake build`.

The first attempt exposed a container PID-namespace issue: Lean queried
`/proc/<getpid()>/exe`, while this container exposes the executable as
`/proc/self/exe`. The failed attempt is preserved. The rerun used the small
audited `evidence/fix_proc_exe.c` preload that redirects only the current
process's executable lookup; it does not alter source, proof terms, imports, or
Lean behavior. Lean reported the pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The successful preflight output
hash is identical to the recorded Stage 4 preflight output.

I also independently checked the Stage 4 sidecars and exact producer output:

- the independently classified domain set has exactly the one rule
  `rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430`;
- `input-manifest.json`, `obligation-map.json` source rules, and the generated
  obligation are bijective and in that same order;
- all source span, normalized hash, inventory hash, discovery hash, conjunct
  hash, and obligation-map hash fields match;
- there are no duplicate or omitted obligations;
- the target produced by the exact generation-time `klean_export.py` equals
  both the generator manifest and audit input.

The generated conjunct is a faithful translation of the guarded K rule:

```lean
∀ (I : SortInt) (V : SortVal)
  (h : isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = true),
  applyCmp "==" V (SortVal.inj_SortInt I) =
    _==Int_ (projectInt
      (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) I
```

It is not a `True` conjunct, is not duplicated, and has satisfiable instances,
for example `V = SortVal.inj_SortInt 7` and `I = 7` under the intended
`isInt`. It exactly captures the source rule's equality, guard, projection,
and integer injection. There is no target change and this is not a
`KLEAN_NO_OBLIGATIONS` case.

The fixed target is
`Klean105ByLength.Lemmas.targetStatement` in
`Klean105ByLength/Lemmas.lean`, with definition hash
`9fd05dd81aa754ff39920cd21046a722ee57d943d1719895762e09924adde7dc`
and instantiated-statement hash
`22910f52851033b1a5112d6ff0b674228069a23696a80017135079b1a6daafc5`.

Evidence is in `evidence/03-klean-preflight.log`,
`evidence/03-klean-preflight-result.json`, and
`evidence/04-stage4-independent-checks.json`.

## Clean Lean build, proof identity, and axioms

I created `/tmp/audit-work/lean-proof-audit` from the candidate source files,
copied the immutable generated project into it as `Base`, and ran both required
commands:

```text
lake clean
lake build
```

The fresh build exited 0. The copied `Base` tree remained byte-identical to the
generated Stage 4 tree. The candidate has exactly one definition for each of
the four target parameters, does not define or shadow `targetStatement`, and
contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. `Proof.final`
occurs exactly once and its type is the exact manifest statement, not a copy,
weakened theorem, or vacuous variant.

Running Lean on `AxiomAudit.lean` produced:

```text
final : Klean105ByLength.Lemmas.targetStatement «_==Int_»
  «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» isInt «project:Int»
'Proof.final' does not depend on any axioms
```

Thus the used-axiom set is empty. It contains neither `sorryAx` nor any
unrecorded dependency; it is trivially a subset of the 47 generated
declarations in `trust-inventory.json`. The trusted final mechanical gate also
returned `PASS`, with `semantic_classification: NOT_EVALUATED`, as expected for
a structural gate.

The complete fresh build is in `evidence/05-fresh-clean-build.log`; exact axiom
output and adversarial Lean evaluations are in
`evidence/06-lean-axiom-and-bridge-audits.log`; the trusted final-gate result is
in `evidence/07-final-mechanical-gate.json`.

## Operational-bridge audit

Three parameter definitions agree with their frozen meaning:

- `«_==Int_»` uses Lean integer equality, matching K `_==Int_`.
- `isInt` is true exactly on the singleton K sequence containing an injected
  integer and false otherwise, matching the generated forms of the supplied
  sort predicate.
- `«project:Int»` returns the injected integer on the `isInt` domain. Its
  fallback `0` only totalizes a region where the K projection is undefined,
  so it does not conflict with a defined frozen case used by the obligation.

The fourth definition is not an honest implementation of its bound symbol:

```lean
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  match operator, left, right with
  | "==", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt == rightInt
  -- five other integer comparison cases
  | _, _, _ => false
```

Its KORE binding is the global
`LblapplyCmp...MPY-CORE...String_Val_Val`, not a newly scoped integer-only
helper. The supplied semantics says comparison dispatch is owned jointly by
`bool.k`, `int.k`, `float.k`, `str.k`, `list.k`, `tuple.k`, `set.k`,
`dict.k`, and `operators.k`. Unlike the undefined off-domain part of
`project:Int`, the wildcard cases above contain many inputs for which K has
explicit operational rules.

Three direct witnesses are decisive:

| Input | Frozen K rule/result | Candidate Lean result |
|---|---|---|
| `applyCmp("==", true, true)` | `bool.k:10`, `true ==Bool true = true` | `false` |
| equality of two empty K strings | `str.k:25`, identical code sequences compare `true` | `false` |
| `applyCmp("==", noneV, noneV)` | `float.k:154`, `noneV ==K noneV = true` | `false` |

`evidence/08-k-operational-examples.log` shows the supplied K runtime
successfully executing assertions for all three cases to `.K`, `NoExc`, and
exit code 0. `evidence/06-lean-axiom-and-bridge-audits.log` shows the candidate
evaluating all three to `false`. Requiring the three frozen-semantics results
in Lean fails with three explicit `false = true` goals and nonzero status 1;
see `evidence/10-expected-operational-semantics.log`.

The counterfactual mutation is also discriminating. In
`evidence/CounterfactualAudit.lean`, replacing both integer equality and
`applyCmp` with constant-`false` functions still proves the fixed generated
target with the honest `isInt` and projection definitions. Lean accepts that
file. This confirms that the equation alone cannot establish the meanings of
its parameters; the required independent operational audit is load-bearing.

The candidate happens to agree with the one target conjunct on its guarded
integer-equality slice. That is insufficient under the requested bridge
criterion: it binds a full operational KORE symbol and uses a convenient
wildcard value on other inputs where the frozen semantics is defined. The
adversarial witnesses are not speculative or merely unreachable totalizations;
they are ordinary observations accepted by the same supplied semantics. This
is an operational-bridge failure, which the audit instructions require to be
`FAIL`/`NOT_LEGIT` even though the build, exact theorem check, and axiom check
all pass.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
