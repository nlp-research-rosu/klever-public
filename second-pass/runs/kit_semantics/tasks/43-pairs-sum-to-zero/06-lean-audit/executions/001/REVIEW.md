# Independent Stage 3–5 audit: `43-pairs-sum-to-zero`

Audit mode was `CLASSIFICATION_AND_PROOF`; the condition was `kit-semantics`
with `SUPPLIED_SEMANTICS`. I treated the mounted workspaces, prior reviews,
comments, and logs as evidence only. The conclusions below come from the
frozen sources, trusted reconstruction/checking code, fresh builds, and
independent bridge tests. Raw transcripts and retained helper programs are
indexed in `evidence/README.md`.

## Result

The protected Stage 3 classification is complete and correct. Stage 4
deterministically generated exactly the two genuine domain-lemma obligations,
without omission, duplication, weakening, or target substitution. The Stage 5
candidate freshly builds, proves the exact fixed target, has no candidate-added
trust escape, and supplies operationally faithful definitions on the complete
match domains of both source rules. The proof is legitimate.

## Producer-source and input integrity

The required producer gate passed before the Stage 4 judgment:

| Artifact | Recomputed SHA-256 |
|---|---|
| `generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |
| producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The two file hashes match `source-manifest.json` and
`generator-manifest.json`. The producer-tree hash matches `/audit-input.json`.
All three available image bindings—the source manifest, generator-manifest
provenance, and image digest encoded by the signed producer-source path—equal
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
There is no producer-provenance `AUDIT_ERROR`.

The signed-resolution digest was independently recomputed as
`fe1482d83d5cd09a3bbcf920f20e9cb1df749ec4e60b909c34ad814a659aed1c`.
The mounted Stage 1 workspace/export, Stage 2 audit, Stage 3 manifest, Stage 4
generation/generated project/producer tree, and Stage 5 workspace all match
their recorded hashes. All 795 recorded per-file Stage 1 hashes also match.
The K/Lean toolchain-lock byte hash is
`a3dc0270ff7cab64550e91f605d8f2b5f6076b75f4ec49629a0e13894455fa9f`;
it matches the Stage 2 binding, and its contents exactly match the Stage 4
generator toolchain record.

`lean_invocation_sha256` refers to the historical Stage 5 invocation tree.
That tree is not among the specified mounts (neither its host path nor a
`/reference/lean-invocation` path exists), so that launcher-only historical
hash cannot be recomputed here. No conclusion relies on it: the mounted
candidate workspace hash was verified, and the proof was independently rebuilt
and axiom-checked from a fresh copy.

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. The selected local verification module and its local
closure are both exactly `VERIFICATION`. The reconstruction found seven rules
in source order. `verification.k` hashes to
`26bbbcd5b08d624d98e111aab6804e75e86defa7f6d4a349481ee6f89a032bc9`;
the canonical whole-inventory hash is
`d0fdf03a9d036db3e9b0732707b1c26876c4455cf0bffb60046d153ec2797da8`.

Comparison with `lemma-discovery.json` is bijective and order-preserving:
seven unique inventory IDs, seven unique discovery IDs, no omitted or extra
rules, no changed span/hash/identity, and no reordering.

| Frozen span and ID | Independent classification | Reason |
|---|---|---|
| 8–12, `rule-8348557acb9f13893399c872ddae569bc70937b7abc79fbe39494743b080aa93` | `DEFINITION` | Defines the total `hasInverse` occurrence-count summary, including the distinct-position two-zero case. |
| 18, `rule-2ebe172a962d634da4247333469c7c769941308cbaa1ffb0733ad2c17efc3b87` | `DEFINITION` | Empty-sequence base equation for `anyInverse`. |
| 19–21, `rule-f0f2741daac7483fe012897d489038765088adda53a780fb059bfe91cd605192` | `DEFINITION` | Structural `anyInverse` recurrence. |
| 24, `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty-sequence base equation for `allInts`. |
| 25, `rule-d25e64ac0656cbce08dd6ef3cd864d49a4614f3e415d6533ea1c726c4a025b1a` | `DEFINITION` | Structural `allInts` recurrence. |
| 30–32, `rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def` | `DOMAIN_LEMMA` | Guarded `Val`-to-`Int` sort-recovery equation for `applyCmp("==", …)`. |
| 34–36, `rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5` | `DOMAIN_LEMMA` | Guarded `Val`-to-`Int` sort-recovery equation for `applyUn("-", …)`. |

The first five equations name summaries, recurrences, or a domain predicate;
they are definitions rather than execution rules or asserted human-facing
facts. The last two rules carry `[simplification]`, are not definitions, and
therefore must be domain lemmas. They are relevant: integer equality selects
the source program's `x == 0` branch, and unary minus forms the `l.count(-x)`
argument. Both feed the loop summary and final postcondition.

Neither simplification is a `PROVED_DERIVED_LEMMA`. Stage 1's bridge-free
connection claims prove the narrower, already-`Int` operational equations:
`applyCmp("==", I:Int, J:Int)` and `applyUn("-", I:Int)`. They do not first
prove the exact guarded `V:Val` rules later installed in `VERIFICATION`.
A fresh bridge-free `kprove` rerun closed those narrower claims with `#Top`;
that validates the fixed integer operations but does not change the
classification. There are no `OPERATIONAL_RULE` or
`PROVED_DERIVED_LEMMA` inventory entries.

## Deterministic Stage 4 generation

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 JSON, selected Stage 4 generation,
and pinned toolchain lock. It returned `PASS`, two obligations, zero designated
sorries, 42 recorded generated trust declarations, and the fixed target below.
Its fresh generated-project `lake clean` and `lake build` both exited 0.

The two independently identified domain-rule IDs equal, in the same order:

1. the `input-manifest.json` source-rule list;
2. the `obligation-map.json` source-rule list; and
3. the `obligation-map.json` obligation list.

Each obligation's source span, normalized hash, inventory hash, discovery hash,
and Lean-conjunct hash recompute correctly. The first conjunct is exactly the
guarded integer-equality rule; the second is exactly the guarded integer
unary-minus rule. The K `Int` argument/result injections, `isInt` guard, and
`intProj` uses are preserved. There are no extra conjuncts, duplicates, missing
domain rules, changed operators, strengthened guards, or weakened conclusions.
Concrete integer values make both guards satisfiable, so the conjuncts are not
inherently vacuous.

The generated source contains one target declaration and exactly two
conjuncts:

- declaration:
  `Klean43PairsSumToZero.Lemmas.targetStatement`;
- definition SHA-256:
  `158437a46ea70eaad307e390e94e8435007eff0b495eb49559054cde5134cd84`;
- instantiated-statement SHA-256:
  `d1d7285363d3a4fbc8d327aa9eae1f5bdf71de225b507f20c3497cfbc588946c`.

The trusted parser's reconstructed target equals the expected target generated
from `obligation-map.json`, `generator-manifest.json`, the recorded preflight,
and `/audit-input.json`. The generated tree hash is
`1f43e94e5498e827724eb04996e1fac89a6db4cd36b10962118253115f0f86c9`.
This is correctly a nonempty `PASS` generation, not
`KLEAN_NO_OBLIGATIONS`.

## Fresh Stage 5 build, proof identity, and trust

I created `/tmp/audit-work/stage5-fresh`, copied the candidate into it, and
copied the immutable generated project into `Base`. Before building, `Base`
recomputed to the exact generated-tree hash above. I then ran, separately:

```text
lake clean   # exit 0
lake build   # exit 0
```

The audit container's PID namespace exposes `/proc/self/exe` but not
`/proc/<getpid()>/exe`; Lean 4.22 uses the latter while locating its
application. A retained, narrowly scoped `LD_PRELOAD` shim redirects only the
exact `/proc/<digits>/exe` read to `/proc/self/exe`. The shim source and
diagnostics are in evidence. It changes neither candidate/generated source nor
Lean elaboration, kernel checking, declarations, or axiom accounting. The
reported toolchain is the pinned Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

Post-build, the target file is byte-identical to Stage 4 (file SHA-256
`e506781245e3d8522864a163ed54618455db3a666cc6df468aaec5bd04c698f1`),
and its definition/statement hashes are unchanged. Candidate code defines each
of the six target parameters exactly once, defines exactly one `Proof.final`,
does not define or shadow `targetStatement`, and states the exact fixed
instantiation. Candidate-only Lean sources contain no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`.

The exact axiom output is:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. `propext` is one of the three Lean foundational
dependencies explicitly recognized by the trusted final gate
(`Classical.choice`, `propext`, and `Quot.sound`), not a candidate declaration
or hidden generated escape. The generated trust inventory records 42 axioms;
none is in `Proof.final`'s dependency list. Both recorded sorry counts are
zero. Thus every reported dependency is accounted for and no unrecorded proof
escape is used.

## Operational-bridge audit

The relevant scope is the complete match domain of the two bound source rules,
not unrelated `applyCmp`/`applyUn` cases that the theorem never states. The
source program's `allInts` precondition and each rule's `isInt` guard restrict
these paths to integer values.

| Target parameter | Independent operational comparison |
|---|---|
| `«_-Int_»` | Candidate is Lean integer subtraction, exactly K's `_-Int_`; tested across positive and negative operands. |
| `«_==Int_»` | Candidate is decidable integer equality, exactly K's `_==Int_`; equal and unequal negative/positive witnesses discriminate it. |
| `«applyCmp(_,_,_)…»` | On the bound rule domain (`"=="`, integer-injected operands), pattern matching selects the integer branch and calls the honest equality primitive, matching `int.k` and the source `x == 0`. |
| `«applyUn(_,_)…»` | On the bound rule domain (`"-"`, integer-injected value), it returns the injected result of `0 -Int x`, matching `int.k` and the source `-x`. |
| `«intProj(_)…»` | Returns the integer payload and returns `0` for non-integers, exactly the two frozen `projection.k` equations. |
| `isInt` | True exactly for the singleton K sequence whose item is an integer injection; false for Boolean injections and for a nonempty continuation. This is the exact target encoding of K's sort guard. |

Independent Lean ground checks covered equal/unequal integers, positive and
negative unary minus, integer and Boolean projections, positive/negative
`isInt` witnesses, and a continuation-boundary counterexample. All elaborated
successfully. These checks agree with the frozen `verification.k`, `int.k`,
`projection.k`, the source solution, and the KORE symbol bindings.

Three counterfactual builds tested sensitivity:

- making `applyCmp` constant `false` and `applyUn` constant `noneV` failed with
  unsolved integer-domain goals;
- making `isInt` constantly `false` still built, demonstrating that the
  parameterized equation alone permits a vacuous guard; and
- changing subtraction to addition while changing equality to constant false
  still built because the same mutated primitives occur on both sides.

The two surviving mutations are why a clean Lean proof is not sufficient.
They do not describe the submitted definitions. The submitted `isInt` has
explicit satisfying integer witnesses, and the submitted primitive and
dispatch definitions independently implement the fixed operational meaning on
every accepted source-rule match. Therefore the candidate does not exploit the
vacuity or shared-symbol circularity exposed by the mutations.

## Final judgment

Stage 3 correctly identifies a nonempty two-rule domain-lemma set. Stage 4
preserves that set and the frozen rules exactly. Stage 5 proves the unique fixed
target with an accounted foundational axiom only, and its operational
definitions pass the independent bridge audit. No material concern or
legitimacy failure remains.

VERDICT: PASS
LEGITIMACY: LEGIT
