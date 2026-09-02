# Independent audit: HumanEval `103-rounded-avg`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The Stage 3 inventory and classifications are complete and mathematically
correct. Stage 4 authenticates to the immutable producer image, generates an
ordered bijection of three genuine domain lemmas, and fixes the exact
conjunction it records. The Stage 5 candidate clean-builds from a fresh copy of
that generated project, proves exactly the fixed target without forbidden
declarations or proof holes, and implements every target parameter with its
frozen K operational meaning.

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`. It selected module `VERIFICATION`; its local same-file
import closure contains only that module. The reconstruction produced:

- `verification.k` SHA-256:
  `8f7949ecf93ad43cc6bcb134e77929ab9060503bdd67d4229a658a0e1148bf52`
- inventory SHA-256:
  `c56fede9da88c87be21505bdccb01640677a3e69700202e3ff3859734027c180`
- exactly four ordered rules:

| Order | Source span | `source_rule_id` / normalized SHA-256 | Attributes | Independent classification |
|---|---:|---|---|---|
| 0 | 8–38 | `rule-856b350eb7e5e0b8b4439c4c371b7848357d072149e50a9a7359680b877be187` | `priority(40)` | `OPERATIONAL_RULE` |
| 1 | 41–44 | `rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804` | `simplification` | `DOMAIN_LEMMA` |
| 2 | 45–48 | `rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52` | `simplification` | `DOMAIN_LEMMA` |
| 3 | 50–52 | `rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f` | `simplification` | `DOMAIN_LEMMA` |

For every rule, I independently re-extracted the source lines, normalized the
text with whitespace joining, recomputed SHA-256, and derived
`source_rule_id = "rule-" + normalized_sha256`. The protected manifest has the
same inventory hash, count, unique IDs, set, and order. There are no omissions,
duplicates, extras, reordered identities, or unaccounted classifications. The
trusted Stage 3 contract validator independently returned the same partition:
zero definitions, one operational rule, zero proved-derived lemmas, and three
domain lemmas.

The classifications are correct for these reasons:

1. Rule `856b…` matches the live translated `while value > 1` computation in
   `<k>`, consumes it, sets `value` to `1`, and changes `digits` to
   `loopDigits(V,A)` in `<scopes>`. It is therefore an execution transition,
   not a defining equation or mathematical domain fact. I reran the
   bridge-free `LOOP-CONNECTION.binary-loop-exact` claim from
   `connection-spec.k`, which imports `VERIFICATION-BASE` rather than
   `VERIFICATION`; `kprove` returned `#Top`, exit 0. The claim matches the
   bridge's loop, continuation generality, bindings, and state update.
2. Rule `8310…` states the guarded binary-value invariant
   `weight(loopDigits(V,A)) + value(loopDigits(V,A))
   = V*weight(A) + value(A)`. It defines no symbol. For `V=1` it is immediate;
   for `V>1`, the `loopDigits` recurrence prepends the remainder bit and
   recurses on the quotient, so the equality follows from
   `V = 2*(V div 2) + (V mod 2)`. It is a domain lemma.
3. Rule `6e9…` is the same guarded invariant in the syntactic form with
   `1 * weight(...)`. It is not a new definition and is not the exact statement
   of a separately proved K claim. It is a domain lemma.
4. Rule `555…` states that `loopDigits` preserves `allBits` when the accumulator
   already contains only `48` and `49`. Each positive recursion step prepends
   `48 + (V mod 2)`, hence another `48` or `49`. It is a domain lemma.

All three simplifications are therefore classified as `DOMAIN_LEMMA`, as
required. They are relevant: the valid-program postcondition requires the
returned binary digit sequence to have the rounded value and satisfy
`allBits`; the first two carry the value invariant through the source loop and
prefix, and the third supplies the bit predicate. None is a disguised,
irrelevant domain assumption.

Primary evidence:
`evidence/02-reconstructed-inventory.json`,
`evidence/04-stage1-relevant-source.txt`,
`evidence/29-inventory-bijection-check.txt`,
`evidence/30-trusted-stage3-contract-validation.json`, and
`evidence/31-fresh-k-connection-proof.txt`.

## Producer authentication and recorded hashes

Before judging Stage 4, I hashed the mounted generation-time sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image identity is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator manifest, and the identity component of the
generation-producer path recorded in `/audit-input.json`. The producer-source
tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly matching the audit input.

I recomputed every one of the 807 per-file
`resolution.stage1_source_hashes`; all exist, all are regular files, all
hashes match, and there are no unrecorded regular files. Independent tree/file
checks also matched:

| Object | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `51a4dc5ddafccf70941442bac319702a7b31d8d6b241615061bc3f35a7a32aca` |
| Stage 1 export tree | `a8f3fa978c512ede39c6161f2a6fe25f2fc8a82df07b2462dded4c013b50f08c` |
| selected Stage 2 audit tree | `9d7200da4f029f17f12e4424e98d4fd65423491782c8503d05be894ebac33641` |
| protected Stage 3 file | `d3f1da65e92b49e5b38d0845417ebdd0e7e8dfd99ae8fab43366dc8bae82bc15` |
| selected Stage 4 tree | `5735b51f507f7b6238e7c85a89b28bb763e7aa3a0f93eacb4f8fb991b7b70ac5` |
| generated project export tree | `1d7365d2be9fdec05643fd23d577a3baf2430628cc29f60b9242c0dae4a51979` |
| mounted candidate workspace | `368bb5275251ab1b88e4de5ec24e8d14d72f967ecaac96ebd963aa5d06e6f839` |

The obligation-map, trust-inventory, every conjunct, every parameter binding,
target statement, target definition, and all associated sidecar hashes also
recompute exactly. The trusted complete gate verified the canonical signed
resolution digest
`826c199c1810c596b100d0b9b0f991f31e4a0c38074b34d10c5551141a84293f`.
The launcher-recorded Lean invocation tree itself is not mounted, so its
standalone tree hash cannot be re-enumerated; it is not used as proof evidence.
Every recorded hash whose object is supplied to this audit was independently
recomputed.

Primary evidence:
`evidence/05-producer-authentication-inputs.txt`,
`evidence/10-producer-authentication-result.txt`,
`evidence/28-stage1-recorded-file-hashes.txt`,
`evidence/41-independent-stage4-target-bijection-hashes.txt`, and
`evidence/49-trusted-complete-mechanical-gate.json`.

## Stage 4 obligation bijection and target identity

The independent classification has a nonempty domain set of exactly three
rules, so `KLEAN_NO_OBLIGATIONS` would have been invalid. The selected export
correctly has status `OK` and obligation count 3.

The ordered domain IDs, `obligation-map.json.source_rules`, and
`obligation-map.json.obligations` are identical and unique. Each obligation
retains the exact source span, normalized hash, inventory hash, discovery
manifest hash, and guarded K meaning:

- conjunct 1 is exactly the `8310…` value invariant;
- conjunct 2 is exactly the `6e9…` normalized value invariant; and
- conjunct 3 is exactly the `555…` `allBits` preservation fact.

The K guard `V >Int 0 andBool allBits(A)` is retained as a proof parameter
whose type asserts that the translated conjunction equals `true`. No
conjunct is empty, literal, duplicated, omitted, or replaced by a weaker
result. With the honest bindings, the guard is satisfiable—for example
`V = 2` and `A = .IntSeq`—and the first equation distinguishes `1` from `2`.

The generated `targetStatement` is exactly the conjunction reconstructed from
those three mapped conjunct strings. It occurs exactly once, at
`Klean103RoundedAvg/Lemmas.lean`, with:

- definition SHA-256:
  `23fcbae960b68803474e73e3bf6865d974c45cb8f57c97f4f1e2857fa6d1f7bb`
- applied-statement SHA-256:
  `48ae69b88a036536fb4aa0b68d8559938cc61832f47c942a9617e24d8c8049e0`

The declaration, file, statement, both hashes, parameter order, KORE symbols,
source-rule links, and binding hashes are exactly equal in the generator
manifest, fresh preflight result, and audit input. There is no generated target
change.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three paths. The sandbox initially
exposed a PID-namespace `/proc` mismatch that prevented Lean from locating its
own executable. Evidence shows `NSpid` differed from the mounted `/proc` PID.
I used a documented temporary `LD_PRELOAD` shim which only retries a failed
`readlink("/proc/<pid>/exe")` as `/proc/self/exe`; it does not alter source,
generated files, Lean elaboration, or the kernel. With that environment repair,
fresh preflight returned `PASS`, obligation count 3, unchanged hashes and
target, zero sorries, 41 inventoried generated trust declarations, and
successful clean/build diagnostics.

Primary evidence:
`evidence/24-pid-shim-source-and-validation.txt`,
`evidence/26-final-pid-shim.txt`,
`evidence/27-fresh-check-generation.json`,
`evidence/32-generated-obligations-target-trust.txt`, and
`evidence/41-independent-stage4-target-bijection-hashes.txt`.

## Stage 5 clean build, proof identity, and trust

I created the fresh project
`/tmp/audit-work/rounded-avg-proof-audit`, copied the authenticated generated
project into it as `Base`, and copied only the candidate's top-level proof
project files. Before building, `Base` had the exact generated export-tree hash
`1d7365…`. I then ran from that fresh project root:

1. `lake clean` — exit 0;
2. `lake build` — exit 0, “Build completed successfully.”

The full command output is preserved. An earlier invocation accidentally used
`/audit-output` as its working directory and was correctly rejected for lack of
a Lake configuration; that failed attempt is also preserved, followed by the
required successful clean and build from the exact fresh directory.

After the build, `Base` still has the fixed generated hash. Across the complete
fresh project there is exactly one `targetStatement`, in the authenticated
generated file. The candidate defines each of the eight exact target parameter
names once and does not define or shadow `targetStatement`. `Proof.final`
occurs exactly once and its normalized theorem type is exactly the generator
manifest's fixed applied statement. Candidate source contains no `sorry`,
`admit`, `unsafe`, `axiom`, or `opaque`.

Running Lean with exactly `#print axioms Proof.final` produced:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. The trusted final-gate policy records these three as
Lean's permitted baseline and adds the generated trust-inventory allowlist.
No one of the 41 generated hook axioms is a dependency of `Proof.final`, and
there is no unrecorded dependency. The complete trusted mechanical gate also
returned `PASS`.

Primary evidence:
`evidence/34-fresh-proof-project-construction.txt`,
`evidence/37-proof-lake-clean-complete.log`,
`evidence/38-proof-lake-build-complete.log`,
`evidence/39-proof-final-axioms-complete.log`,
`evidence/40-trusted-final-proof-gate.json`,
`evidence/41-independent-stage4-target-bijection-hashes.txt`, and
`evidence/53-exact-candidate-parameter-definitions.txt`.

## Operational meaning of every target parameter

`SortBool` is Lean `Bool` and `SortInt` is Lean `Int`. The compiled KORE
declarations bind the four builtin parameters to hooks `BOOL.and`, `INT.gt`,
`INT.add`, and `INT.mul`. The candidate definitions are respectively `x && y`,
`decide (x > y)`, `x + y`, and `x * y`; these are exact, total meanings of the
bound hooks, not proof conveniences.

The other four definitions reproduce `verification-base.k`:

| Parameter | Frozen K meaning | Candidate judgment |
|---|---|---|
| `allBits` | empty is true; a cons is `(c=48 or c=49) and allBits(rest)` | Exact structural recursion |
| `bitWeight` | empty is 1; a cons doubles the tail weight | Exact structural recursion |
| `bitValue` | empty is 0; a cons contributes `(c-48)*weight(rest)` plus tail value | Exact structural recursion, including non-bit integers |
| `loopDigits` | for `V≤1`, return the accumulator; for `V>1`, recurse on the quotient and prepend `48 + V mod 2`; the symbolic inverse rule folds an existing bit back into `V` | Exact recurrence |

For `loopDigits`, converting `v` to `Nat` is faithful on the whole relevant
integer behavior: every negative integer and zero maps to `0`, and both the K
and Lean definitions immediately return the accumulator; `1` is also a base
case. For positive `v>1`, natural division/remainder agrees with the frozen K
quotient and `pyMod(_,2)`, and the accumulator is preserved and extended in the
same order. The implementation also satisfies the frozen symbolic inverse
rule, as checked at a boundary example.

I checked the same adversarial cases independently in Lean and K:

- Boolean/arithmetic results: `false`, `true`, `3`, `-12`;
- `loopDigits` at `-3`, `0`, and `1` preserves accumulator `[49,48]`;
- values `2`, `3`, and `4` produce `[48]`, `[49]`, and `[48,48]`;
- value `5` with accumulator `[49,48]` produces `[48,49,49,48]`;
- the symbolic case `loopDigits(2, 49 :: [49,48])` equals
  `loopDigits(5,[49,48])`;
- accumulator `[49,48]` has weight `4`, value `2`, and `allBits = true`;
- the non-bit head `50` has the frozen arithmetic value `2` and
  `allBits = false`.

Lean completed all evaluations and checked propositions with exit 0. The
corresponding K ground claims returned `#Top`, exit 0.

As counterfactual sensitivity checks, I instantiated the target with an
identity `loopDigits`; Lean proved that this counterfeit target is false using
the satisfiable witness `V=2`, empty accumulator. I also showed that an
intentionally dishonest constant-false `allBits` makes the abstract target
vacuously provable. This second mutation confirms that structural integrity and
a clean proof are insufficient by themselves. The actual candidate does not
use that escape: its `allBits` is the exact frozen recursion, its guard is
inhabited, and all remaining definitions are operationally faithful.

Primary evidence:
`evidence/48-target-parameter-kore-bindings.txt`,
`evidence/50-final-lean-operational-and-mutation-audit.log`,
`evidence/51-final-k-operational-examples.log`,
`evidence/52-final-adversarial-sources.txt`, and
`evidence/53-exact-candidate-parameter-definitions.txt`.

## Conclusion

The protected Stage 3 classification is independently correct, the
deterministic Stage 4 artifact is authentic and mathematically faithful to all
and only the genuine domain lemmas, and the Stage 5 theorem proves exactly the
fixed target using honest operational bindings and only the accepted Lean
baseline axioms. No legitimacy defect or residual concern remains.

VERDICT: PASS
LEGITIMACY: LEGIT
