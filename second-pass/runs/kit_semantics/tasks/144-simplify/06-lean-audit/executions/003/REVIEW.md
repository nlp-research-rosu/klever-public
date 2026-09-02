# Independent audit: HumanEval 144-simplify

This audit covers `kit-semantics`, `SUPPLIED_SEMANTICS`, in launcher-recorded
`CLASSIFICATION_AND_PROOF` mode. I treated the candidate, manifests, prior
reviews, comments, logs, and all mounted provenance as untrusted evidence. I
used the trusted inventory, preflight, tree-hash, target-extraction, candidate,
and axiom-parsing code under `/reference/tools` and independently judged the K
rules, generated obligations, Lean definitions, and proof.

The result is a pass. Stage 3 classifies all 21 frozen rules correctly; Stage
4 deterministically exports the two genuine domain lemmas without weakening or
changing them; and the fresh Stage 5 build proves that fixed target with honest
operational interpretations and no unrecorded trust escape.

## Producer-source provenance

I hashed the required producer files before judging Stage 4. The results match
the generation-time source manifest, `generator-manifest.json`, and the image
identity encoded by `/audit-input.json`:

| Producer | Actual and recorded SHA-256 |
|---|---|
| `klean_export.py` | `f1a7004c0ec7b8be2646f9fdedbc9a9975903f9797e34cdf8b3e4ecb1df3ed59` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` |

The trusted pipeline tree hash is
`3141041ba4f4427b633483489102d026b053f5f382041e7ae1d1041689619478` on
both the mounted producer tree and the launcher record. The source manifest,
generator manifest, and audit-input path all identify immutable image
`sha256:853cc3153c8c3a393e12a3bbc09f51f7f1384695616f4490f55b252c156a3d0e`.
There is no producer-source infrastructure error.

## Frozen rule inventory and Stage 3 classification

The trusted inventory code selected module `VERIFICATION` and reconstructed
its local verification-module closure in source order as
`VERIFICATION-SYNTAX`, `VERIFICATION-BASE`, and `VERIFICATION`. It found 21
rules. The frozen `verification.k` hash is
`43a690d36d510243677f01691f374e97d6e6fd7cce6a848de7a41bfb6ce43e34`;
the whole reconstructed inventory hash is
`377ee46b909ba5c403e738ed5881c00cd31e73905dce6f16656b3a11ce90bc86`.

The reconstructed list and `lemma-discovery.json` agree bijectively on every
source span, normalized source text hash, `source_rule_id`, and order. Both
lists have 21 unique IDs. There are no missing, extra, duplicate, reordered,
or hash-changed entries. The complete per-rule table is preserved in
`evidence/02-rule-inventory.txt`.

My independent classifications are:

| Frozen lines | Rules | Judgment and reason |
|---|---:|---|
| 20–112 | 4 | `DEFINITION`: exact named AST terms `simplifyLoopBody`, `simplifyReturn`, `simplifyBody`, and the named scope constructor `simplifyScope`. |
| 114–143 | 9 | `DEFINITION`: the base, slash/digit recurrence, accepting, and `owise` equations that completely define `validScan`. |
| 145–163 | 6 | `DEFINITION`: the terminal modulo case and slash/digit recurrences that define `scanResult`. |
| 169–200 | 1 | `DOMAIN_LEMMA`: generic digit-loop execution summary, ID `rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543`. |
| 202–232 | 1 | `DOMAIN_LEMMA`: generic slash-loop execution summary, ID `rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650`. |

The first 19 rules introduce named proof terms or recursive summary functions;
they do not assert extra executions. The final two priority-40 rules replace a
complete running `#loop` configuration with a `scanResult` summary. They are
neither definitions nor ordinary small-step operational/observation rules.

They are also not `PROVED_DERIVED_LEMMA`s. Stage 1's `loop-spec.k` imports only
`VERIFICATION-BASE`, then proves four digit claims specialized to phases 0,
1, 2, and 3 and three slash claims specialized to phases 0, 1, and 2. It never
first proves either later installed rule with the exact symbolic `P`, arbitrary
guarded `LOOPBODY`/`RETSTMTS`/scope terms, and exact generic premise. Thus the
required exact-same-rule criterion is not met.

Both domain lemmas are relevant. The frozen solution scans the character codes
of `x + "/" + n` into four decimal accumulators and returns whether
`(a*c) % (b*d) == 0`; the two rules summarize precisely the digit and slash
loop steps used to reach that postcondition. No inventory rule has a
`simplification` attribute, so there is no simplification rule assigned an
impermissible class.

## Stage 4 deterministic generation

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three specified inputs plus the pinned toolchain lock. It returned `PASS`, two
obligations, 76 generated trust declarations, zero designated sorries, and
successful internal `lake clean` and `lake build` diagnostics. The complete
returned data is `evidence/03-stage4-preflight.json`.

The sandbox lacks `/proc/<reported-pid>/exe`, which Lean 4.22 uses to locate
its installation. I used the narrow, recorded compatibility shim in
`evidence/pid-namespace-shim.c`; it redirects only that readlink to
`/proc/self/exe`. It does not alter project or proof content. The commands then
used the exact pinned Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

Independent hash checks agree across the actual files, manifests, and audit
input:

| Object | SHA-256 |
|---|---|
| Stage 1 frozen export | `894f4717a6146c47ed7d13c5226da45c47fa4e4cb7ddf672a124c57a12dbfcdd` |
| Stage 3 discovery manifest | `0503bb95aa88062aeaa5203b43361df0cc78df321014349cb6029fcbf5f2ecda` |
| Generated project tree | `4dc43c025d4e3fe487736af960165f2ff73ddbf513ab721164e8050d076febd6` |
| Obligation map | `3a303ddc682d1b4b6203b02334d41bfebc251fa46fcf72b4ab2780b4614b7673` |

The independently classified domain-ID list, generated `source_rules` list,
and generated obligation list are the same unique ordered pair. The digit
conjunct hash is
`17adea475b0cd17d87b3d13b5c62c7382be27eef7d15765e4c902ede5923b481`;
the slash conjunct hash is
`af558ba8e6c4704a48da36f09e2fa5cb38cf0a99ee66a6920ece41d0eeac3206`.
Their source IDs, spans, normalized hashes, inventory hashes, and discovery
hashes all agree with the frozen reconstruction.

Mathematically, the two Lean obligations preserve every source cell and
transition: `k`, `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`,
`ret`, `exc`, `exitCode`, and `generatedCounter`. They retain the exact AST,
scope, builtins, phase, digit, and `validScan` guards. The digit case has
`0 <= P <= 3` and `isDigitC CODE`; the slash case fixes code 47 and has
`0 <= P < 3`. Each destination is the exact `scanResult` state. Neither
conjunct is irrelevant, duplicated, weakened, vacuous, or syntactically equal
on both sides.

The generated fixed target is:

- declaration: `Klean144Simplify.Lemmas.targetStatement`;
- file: `Klean144Simplify/Lemmas.lean`;
- definition hash:
  `ea7b23c1b410bb9cc367f92d8595e8e3f4859489b700fa283bc8201e8ef3875a`;
- statement hash:
  `b398cace569cf85fa9ab7950f60d946ce73b95578a19121167fb53139cca5040`.

The extracted target object equals both `generator-manifest.json` and
`/audit-input.json`. Because the true domain set has two entries, the selected
`OK`/two-obligation result is correct; `KLEAN_NO_OBLIGATIONS` would not have
been legitimate.

## Stage 5 proof, identity, and trust

I created `/tmp/audit-work/lean-project`, copied the candidate source project,
and copied the immutable generated project into it as `Base`. The copied Base
tree retained hash
`4dc43c025d4e3fe487736af960165f2ff73ddbf513ab721164e8050d076febd6`.
The candidate's independently computed tree hash is
`2203f6c06d3d1975c4628b4a1093b6e3d10bbbeed883ecfb67b2a75982cec6f6`,
matching `/audit-input.json`.

In that fresh project, `lake clean` exited 0 with empty output and `lake build`
exited 0 with only unused-variable linter warnings. The full output is in
`evidence/06-fresh-lake-clean-build.txt`. The candidate gate found exactly one
definition for each of the 16 required parameters and exactly one theorem
`Proof.final`. Candidate sources contain zero instances of `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`.

`Proof.final` has exactly the manifest target statement and applies the
qualified generated declaration; there is no local target shadow or duplicate
weaker theorem. It unfolds the two fixed conjuncts, recovers the exact AST and
scope equalities from their guards, and applies `candidateLoopSound` to digit
and slash starts. `candidateLoopSound` is an induction over the remaining
codes that uses concrete generated operational `Rewrites` constructors for
loop unconsing, slash branching, decimal assignments, scope/map operations,
return evaluation, and final-state cleanup. The generated `Rewrites.lean`
contains no constructor with a `#loop` source and protected `scanResult`
destination and no occurrence of either domain-rule ID, so the proof cannot
invoke the obligations circularly.

Running Lean on `#print axioms Proof.final` reported 30 dependencies. Twenty-
seven are generated executable-semantics boundary declarations, and each is an
exact recorded trust-inventory entry:
`Float2Int`, `Int2Float`, `Int2String`, float multiplication/addition/
subtraction/division/comparisons/equality/power/root/min/max/abs/ceil/floor,
Boolean equality, string equality, integer power/abs, `binAcc`, `buildVS`,
`cntSub`, `md5hexCodes`, and `sortKeyVS` (with their full generated names shown
in `evidence/07-proof-axioms.txt`). The remaining three are the trusted Lean
core primitives `propext`, `Classical.choice`, and `Quot.sound`, explicitly
included by the trusted final gate. The generated declaration set contains
exactly the 76 entries in the manifest allowlist. There is no unrecorded
dependency and no `sorryAx`.

## Operational bridge audit

I located and compared all 16 exact candidate definitions with their bound
KORE symbols, source-rule IDs, the two frozen domain rules, the frozen source
program, and the supplied operational semantics:

| Target parameter(s) | Independent operational judgment |
|---|---|
| `«.List»`, `«.Map»`, `ListItem` | Exact empty-list, empty-map, and singleton-list constructors. |
| `_Map_`, `«_|->_»` | Exact generated K map concatenation and singleton operations on the target's defined, pairwise-distinct keys 0, 1, and -1. `getD` only totalizes undefined cases, which the target and proof never use. |
| `_andBool_`, `«_<Int_»`, `«_<=Int_»`, `«_==K_»` | Exact Boolean conjunction, integer comparisons, and structural K equality. |
| `«builtinsScope_MPY-CORE_Scope»` | Exact set of 23 name/value bindings from `semantics/core.k`, with root parent. |
| `«isDigitC(_)_MPY-METHODS_Bool_Int»` | Exact `48 <= code <= 57` rule from `semantics/methods.k`. |
| `«validScan(...)»` | Exact nine-rule `verification.k` base/recurrence/`owise` definition, including three slashes, four positive accumulators, and decimal Horner updates. |
| `«scanResult(...)»` | Exact six-rule slash/digit recurrence and terminal `(a*c) pyMod (b*d) == 0`. Its total fallback is outside the `validScan` domain; on the target domain `b*d` is positive and the Lean modulo formula equals Python/K modulo. |
| `«simplifyLoopBody...»`, `«simplifyReturn...»` | Exact generated values of the frozen named AST equations. Their Option fallback is unreachable for these generated constants. |
| `«simplifyScope(...)»` | Exact bindings for `x`, `n`, `part`, `a`, `b`, `c`, `d`, and `ch`, with `parent(0)`. |

I also ran executable adversarial tests. Codes 47, 48, 57, and 58 produced
`false, true, true, false` for `isDigitC`. The valid scan `1/2/3/4` was
accepted and produced false, while `1/5/5/1` was accepted and produced true.
Replacing a slash with a digit, inserting a non-digit, omitting the first or
last component, adding a trailing slash, or starting at phase 4 was rejected.
Lean additionally proved that constant-true digit/valid/result definitions and
a constant-false result definition disagree with these witnesses. Thus a
constant, identity, hard-coded, or vacuous bridge cannot explain the theorem.

## Final judgment

The protected classification is independently correct, deterministic
generation is source- and target-faithful, the two real domain obligations are
neither omitted nor weakened, and the candidate cleanly proves precisely that
fixed target against the generated operational relation. All operational
bindings implement the frozen meaning on the theorem's domain, and every proof
dependency is accounted for.

VERDICT: PASS
LEGITIMACY: LEGIT
