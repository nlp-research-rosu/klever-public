# Independent audit: HumanEval 144-simplify

Audit scope: condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`,
launcher mode `CLASSIFICATION_AND_PROOF`. I treated all mounted candidate,
provenance, comments, logs, and prior judgments as untrusted evidence. The Stage
3 classification and Stage 5 proof were judged anew from the frozen Stage 1
source and supplied operational semantics.

## Conclusion

Stage 3 is correctly classified and Stage 4 is a structurally and
mathematically faithful deterministic generation of two real domain
obligations. Stage 5 is not a legitimate proof. `Proof.final` obtains an
inhabitant of `Empty` from the generated polymorphic axiom
`SetHookDef.choiceAx Empty []`, then eliminates it to prove the target. The same
term proves `False`, proves `0 = 1`, and proves the exact target for arbitrary
mutations of all sixteen operational parameters. It therefore proves neither
loop lemma and fails the proof-identity, non-vacuity, trust, and operational
bridge gates.

## Input and producer integrity

The audit mode from both `AUDIT_MODE` and `/audit-input.json` was
`CLASSIFICATION_AND_PROOF`. Hashing used the trusted pipeline/tree routines,
not filesystem metadata. The recorded and actual mounted tree hashes agree:

| Input | SHA-256 |
|---|---|
| `/reference/k-proof` pipeline tree | `a64b814d718a79a5b94e33f0778e26f3a0dcc2f6da7854ebbebd7640f9be88ee` |
| `/reference/k-audit` pipeline tree | `72b4d0db52f4488a28e094adaf992e578dccb37979759105a6a78d572ae650c1` |
| `/reference/klean-generation` pipeline tree | `9fd07ebdd84c34f3bdd1c883f0b9ad5686e43e500829e56084efc591969c44ac` |
| `/reference/generation-tools` pipeline tree | `e2997e276bc28e190348cbf865548aaeda9c5a355767876bf0a1e21fec2aada8` |
| `/candidate` pipeline tree | `4dc271423f979165e75ae57f615b9393f3032a091ade2f46818412be2863b2c7` |

The Stage 1 content digest is
`894f4717a6146c47ed7d13c5226da45c47fa4e4cb7ddf672a124c57a12dbfcdd`,
the Stage 3 file digest is
`0503bb95aa88062aeaa5203b43361df0cc78df321014349cb6029fcbf5f2ecda`,
and the generated-project content digest is
`e4d7593675f2d206403c684c17e5fd1147663b85349556f9158021ff0820206f`.
All agree with the manifests and audit input.

Before reviewing Stage 4, I independently hashed the two immutable producer
files:

| Producer | Actual and recorded SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `ba1148c5df311b510d03f95887839e72b878bbe302c54fd0d981cf568ea8eaa1` |

These match `generator-manifest.json`, the producer source manifest, and the
producer-source tree in `/audit-input.json`. Both manifests record immutable
generator image
`sha256:a12daa6dccbac0cead0f384a86899561d3ceb2d478ef3f182ec36ec52ba2cb77`,
and the audit-input source path is bound to that same image ID. The producer
gate passed; there is no producer-source infrastructure error.

## Stage 3: independent rule reconstruction and classification

I ran the trusted local rule-inventory implementation on the frozen
`verification.k`. Its verification-module closure, in source order, is
`VERIFICATION-SYNTAX`, `VERIFICATION-BASE`, `VERIFICATION`. It reconstructed 21
unique rules. For every entry it independently recovered the module, source
span, normalized text/hash, attributes, and
`source_rule_id = "rule-" + normalized_source_sha256`.

The recomputed whole-inventory hash is
`377ee46b909ba5c403e738ed5881c00cd31e73905dce6f16656b3a11ce90bc86`.
It equals the protected Stage 3 value. The 21 IDs match bijectively and in the
same order: no duplicate, omission, extra rule, reordered identity, changed
span, changed normalized hash, or unaccounted classification exists.

My classification from the source and operational semantics is:

| Frozen rules | Classification | Reason |
|---|---|---|
| 1-4, spans 20-112 | `DEFINITION` | Exact named AST/scope terms: `simplifyLoopBody`, `simplifyReturn`, `simplifyBody`, and `simplifyScope`. |
| 5-13, spans 114-143 | `DEFINITION` | The exhaustive base, recursive, and owise equations defining `validScan`. |
| 14-19, spans 145-163 | `DEFINITION` | The six guarded recurrence equations defining `scanResult`. |
| 20, span 169-200, `rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543` | `DOMAIN_LEMMA` | A digit-loop execution summary that collapses an entire loop plus function-frame teardown. |
| 21, span 202-232, `rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650` | `DOMAIN_LEMMA` | The corresponding slash-loop execution summary. |

Rules 20 and 21 are not ordinary operational rules: they summarize many
language steps and are introduced at priority 40 specifically to accelerate
the later proof. They also are not proved-derived lemmas under the required
exact-identity test. `prove.sh` first builds `VERIFICATION-BASE` and proves four
phase-specialized digit claims and three phase-specialized slash claims from
`loop-spec.k`; it only then builds `VERIFICATION`, which contains the broader
symbolic-`P` rules, and uses those rules in `spec.k`. Stage 1 never first proves
either exact generic rule in a module that omits it.

Both domain lemmas are relevant. The frozen source scans `x + "/" + n`, treats
code 47 as a phase separator, accumulates four positive decimal integers, and
returns whether `(a*c) % (b*d) == 0`. The two summaries consume precisely a
digit or slash under `validScan` and return `scanResult`, while restoring the
caller environment, scope location, stack, return, and exception cells. No
rule in the reconstructed inventory has a `simplification` attribute, so the
special simplification-category constraint is satisfied vacuously. The
protected Stage 3 labels agree with this independent classification.

## Stage 4: preflight, bijection, target, and mathematical content

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly `/reference/k-proof`,
`/reference/lemma-discovery.json`, and `/reference/klean-generation`. It
returned `status: PASS`, `obligation_count: 2`, zero designated sorries, and a
successful clean generated-project build. Its Stage 1, Stage 3, generated-tree,
target, and trust-declaration values match the independent hashes above.

The first invocation stopped before checking inputs because this sandbox
blocks Lean/Lake's numeric `/proc/<pid>/exe` lookup. I diagnosed that
`/proc/self/exe` remains readable, then used an audit-only `LD_PRELOAD` shim
under `/tmp/audit-work` that changes only such numeric readlink requests to
`/proc/self/exe`. Its source and binary hashes and pinned Lean 4.22.0 version
are in evidence 15-16. It did not modify or shadow any mounted input or Lean
project. The successful exact preflight output is evidence 17.

The independently classified domain set is exactly the ordered source-rule set
in both the input manifest and obligation map:

1. digit bridge `rule-ab9ad07a...d1543`, generated conjunct SHA-256
   `17adea475b0cd17d87b3d13b5c62c7382be27eef7d15765e4c902ede5923b481`;
2. slash bridge `rule-c37d3f4e...cb650`, generated conjunct SHA-256
   `af558ba8e6c4704a48da36f09e2fa5cb38cf0a99ee66a6920ece41d0eeac3206`.

Each obligation carries the correct source span, normalized source hash,
inventory hash, discovery hash, parameter bindings, and complete generated
configuration. The obligation-map SHA-256 is
`3a303ddc682d1b4b6203b02334d41bfebc251fa46fcf72b4ab2780b4614b7673`,
matching the generator manifest. There are no extra, omitted, duplicated, or
reordered source rules or obligations.

Mathematically, the digit conjunct retains exact equality guards for the loop
body, return, callee scope, and builtins scope; `0 <= P <= 3`; the digit test;
and `validScan`. The slash conjunct retains the same structural guards,
`0 <= P < 3`, and the slash-headed `validScan`. Both retain the full pre/post
configuration, including the loop/continuation, caller and callee scopes,
environment and scope counters, empty heap, one-frame-to-empty stack,
return/exception state, exit code, and generated counter. Their conclusions
are the corresponding `scanResult` value. Neither is `True`, a dropped guard,
an irrelevant property, or a vacuous conjunct.

The generated target is exactly the conjunction of those two obligations with
the recorded sixteen operational parameters. Its immutable identity is:

- declaration: `Klean144Simplify.Lemmas.targetStatement`;
- definition SHA-256:
  `ea7b23c1b410bb9cc367f92d8595e8e3f4859489b700fa283bc8201e8ef3875a`;
- statement SHA-256:
  `b398cace569cf85fa9ab7950f60d946ce73b95578a19121167fb53139cca5040`.

The generated source, generator manifest, audit input, and independent
reconstruction all agree. This is not a `KLEAN_NO_OBLIGATIONS` case: the true
domain set has exactly two members, a target exists, and proof mode is
applicable.

## Stage 5: clean build and target identity

I made the fresh project `/tmp/audit-work/stage5-audit-001`, copied the
candidate into it, and copied the immutable generated project as `Base`.
`Base/Klean144Simplify/Lemmas.lean` has SHA-256
`a774a369d05fbaa685d8a70085edcffc62ceffde19b31ced420c036cc1396b70`
and is byte-identical to the selected generated target. I ran both required
commands from the fresh copy:

- `lake clean`: exit 0;
- `lake build`: exit 0, `Build completed successfully.`

The complete outputs are evidence 22-23. The candidate neither changes nor
shadows `targetStatement`; `Proof.final` states exactly the fixed generated
target, not a copy or weakened variant. Searches found no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque` in the candidate.

These structural checks do not validate the proof body. Its complete proof is:

```lean
theorem final : Klean144Simplify.Lemmas.targetStatement ... := by
  exact Empty.elim (SetHookDef.choiceAx Empty [])
```

The generated prelude declares the recorded trust item
`SetHookDef.choiceAx : List T -> T`. Instantiating `T := Empty` and passing the
empty list produces an impossible `Empty`; `Empty.elim` then proves any
proposition. This is an inconsistent use of a collection-hook placeholder,
not evidence for either operational rewrite.

## Axiom accounting and adversarial proof checks

Running Lean with `#print axioms Proof.final` produced 32 dependencies. Exact
output is evidence 25. Independent parsing against `trust-inventory.json`
accounts for all of them:

- 29 are recorded generated declarations, including
  `SetHookDef.choiceAx`;
- three are Lean core axioms: `propext`, `Classical.choice`, and `Quot.sound`;
- no name is unrecorded;
- `sorryAx` is absent.

Thus the mechanical ledger reconciliation passes, but the semantic trust
audit fails. Merely listing an inconsistent axiom in the inventory cannot make
ex-falso a proof of the frozen program. The candidate directly exploits that
inconsistency. Evidence 28 compiles the exact countertests:

```lean
theorem contradiction : False :=
  Empty.elim (SetHookDef.choiceAx Empty [])

theorem zero_eq_one : (0 : Nat) = 1 :=
  Empty.elim (SetHookDef.choiceAx Empty [])
```

It also proves the immutable `targetStatement` with all sixteen parameters as
arbitrary binders using the same term. Therefore the candidate proof remains
valid under constant, identity, hard-coded, or otherwise adversarial mutations
of every operational bridge. No parameter definition and no rewrite theorem is
used.

## Operational-parameter review

I located and compared every one of the sixteen candidate definitions with its
manifest `kore_symbol`, recorded source-rule IDs, frozen definitions, source
solution, and operational semantics. Evidence 31 contains the full per-entry
table and evidence 30 contains executable boundary/source probes.

The empty list/map, Boolean and integer operations, K equality on generated
syntax, map/list items, exact 23-entry builtins scope, digit predicate,
`scanResult`, exact loop/return ASTs, eight-binding callee scope, and
`validScan` all agree on the guarded frozen states. The probes check digit
boundaries, both source examples, the accepting scan, and the scope size. The
candidate's `_Map_` is raw list append: it constructs the fixed distinct-key
maps in the required order, but it is not an unrestricted total model of the
hooked map abstraction because order is observable and duplicate-key validity
is unchecked. The source-specific recurrence totalizes K-undefined states,
but those states are excluded by the generated guards.

Most importantly, these definitions cannot establish an operational bridge
when the theorem proof ignores all sixteen of them and derives the target from
`Empty`. The arbitrary-parameter countertheorem is a direct non-vacuity test:
every counterfactual mutation still compiles. The claimed `Proof.final` is
therefore not a proof of the fixed generated obligations or the frozen
operational meaning.

## Evidence index

Raw commands, complete outputs, manifests, and audit analyses are under
`/audit-output/evidence/`. Key files are:

- `04`, `11`, `12`: reconstructed inventory, bijection/classification, and
  Stage 1 proof ordering;
- `13`: producer hash/image gate;
- `17`: successful trusted Stage 4 preflight;
- `18`, `19`: complete manifests/obligations/trust data and independent
  obligation/target bijection;
- `21`-`24`: fresh copy, clean/build outputs, and target/forbidden-token checks;
- `25`, `27`: exact axiom output and corrected ledger reconciliation;
- `28`, `30`, `31`: proof-escape counterexamples and full operational-parameter
  audit.

Files explicitly named `superseded` preserve failed diagnostic/parser/probe
attempts and are not relied upon. The first preflight infrastructure failure is
preserved separately in evidence 14 and resolved by evidence 15-17.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
