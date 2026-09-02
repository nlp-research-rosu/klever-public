# Independent Stage 3–5 audit: `36-fizz-buzz`

## Scope and result

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_AND_PROOF` for
condition `bare` and semantics mode `GENERATED_SEMANTICS`. I treated all
candidate, prior-review, log, comment, and manifest prose as untrusted
evidence. I used the trusted rule inventory, preflight, resolution contract,
and final mechanical gate, and made the semantic classification and
operational-bridge judgments independently.

The audit found a complete 13-rule Stage 1 inventory, a correct Stage 3
classification with one genuinely relevant domain lemma, an exact one-rule /
one-obligation Stage 4 mapping, and a Stage 5 proof whose only target parameter
implements the frozen K operation exactly. The final result is PASS/LEGIT.

## Producer provenance gate

This gate was completed before judging Stage 4.

The mounted generation-time sources hash as follows:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`
- complete producer bundle:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`

The two file hashes equal both `generator-manifest.json` and
`source-manifest.json`. The bundle hash equals `/audit-input.json`. The
generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the generator manifest, source manifest, and the basename of the
launcher-recorded producer-source path. The bundle has exactly the two
producer files and its source manifest. There is no producer-provenance
infrastructure error. Raw evidence is in
`evidence/01-producer-provenance.txt`.

The signed resolution digest independently recomputes to
`5f71ce9075e61d27eed79fae1f8373c812fb20c2ea8a80c71789bd76de5eb491`.
Every available launcher-recorded tree hash matches: the Stage 1 workspace,
Stage 1 export, selected Stage 2 audit, selected Stage 4 generation, producer
bundle, generated project, and Stage 5 workspace. Every individual Stage 1
source hash also matches. The launcher records a Stage 5 invocation-tree hash,
but no invocation tree is among the mounted inputs; it was not used as proof
evidence. The complete reconciliation is in
`evidence/16-hash-reconciliation.json`.

## Inventory reconstruction and Stage 3 bijection

I ran `tools.k_rule_inventory.inventory_verification` directly against the
read-only `/reference/k-proof`. The local verification-module closure of
`verification.k` is exactly `VERIFICATION`, containing 13 rules. The
reconstructed results are:

- `verification.k` SHA-256:
  `24034a2584fae5d039c164a46ecdba6763c893b5f9675d8b543d0c41897bae86`
- canonical inventory SHA-256:
  `736568ab7f1701fa76e06519c913488b7fd319b62eb88baa3958a177a3882787`
- 13 distinct normalized hashes and `source_rule_id` values.

For every rule, the trusted inventory recomputed its exact module, start and
end line, normalized source hash, ID, attributes, and source text. The full
records are preserved in `evidence/02-reconstructed-inventory.json`.

The protected Stage 3 manifest has exactly 13 distinct IDs. Its ID list is
identical to the reconstructed source order. There are no omissions, extras,
duplicates, reordered identities, or inventory-hash differences. The trusted
Stage 3 boundary validator also passes. See
`evidence/03-stage3-bijection.json`.

## Independent classification judgment

The independent classification is 12 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`:

| Frozen span | Rule family | Independent classification | Judgment |
|---:|---|---|---|
| 13–14 | `fizzEnd`, negative branch | `DEFINITION` | Defines the named final-index summary as zero when the outer loop does not start. |
| 15–16 | `fizzEnd`, nonnegative branch | `DEFINITION` | Defines the final index as `N`, matching repeated `i := i + 1`. |
| 18–19 | `digitSevens`, base | `DEFINITION` | Defines zero remaining digits once the nonnegative digit scan is exhausted. |
| 20–21 | `digitSevens`, last digit seven | `DEFINITION` | Adds one and recurses on positive division by ten, matching the inner loop. |
| 22–23 | `digitSevens`, other last digit | `DEFINITION` | Recurses without incrementing. |
| 25–26 | `fizzContribution`, divisible by 11 | `DEFINITION` | Defines the digit-count contribution on the first eligible branch. |
| 27–28 | `fizzContribution`, only divisible by 13 | `DEFINITION` | Defines the second disjoint eligible branch. |
| 29–30 | `fizzContribution`, neither divisor | `DEFINITION` | Defines the ineligible contribution as zero. |
| 32–33 | `fizzFrom`, empty interval | `DEFINITION` | Defines the empty interval summary as zero. |
| 34–35 | `fizzFrom`, nonempty interval | `DEFINITION` | Adds the current contribution and advances the interval index. |
| 38 | integer-addition reassociation | `DOMAIN_LEMMA` | A globally true algebraic fact needed to align symbolic invariant sums. |
| 43–48 | `INNER-LOOP` | `DEFINITION` | A macro defining a named proof term as the exact translated inner-loop AST. |
| 51–59 | `OUTER-LOOP` | `DEFINITION` | A macro defining the exact translated outer-loop AST. |

The guarded function branches are pairwise disjoint and exhaustive.
`digitSevens` strictly descends for positive inputs, and `fizzFrom` advances
toward `N`. The two macro equations expand to the constructors in
`solution.mpy`; after expansion, ordinary rules in `semantic.k` execute the
program. They therefore define named proof terms rather than replacing
operational execution.

The line-38 simplification is not a definition or an ordinary execution rule.
It is integer associativity:

`(A +Int B) +Int C = A +Int (B +Int C)`.

It is relevant to the source program and postcondition because loop execution
produces a left-nested update while the summaries and invariant use a
right-associated sum. An exact mutation deleting only this rule compiles, but
the original `kprove spec.k` then exits 1. Its residual is the expected failed
implication between
`C +Int 1 +Int digitSevens(X /Int 10)` and
`C +Int (digitSevens(X /Int 10) +Int 1)`. The unmodified fresh proof exits 0
with `#Top`. See `evidence/27-kprove.stdout.txt`,
`evidence/31-no-assoc-kprove.stdout.txt`, and
`evidence/37-no-assoc-mutation.diff`.

The lemma is not a `PROVED_DERIVED_LEMMA`: the frozen `prove.sh` compiles
`verification.k` once with this rule already present and only afterward calls
`kprove`. There is no earlier module or proof of the exact rule with the rule
absent. It is correctly classified as the sole `DOMAIN_LEMMA`, and it is the
only `[simplification]` rule. Detailed per-entry reasoning is also recorded in
`evidence/05-independent-classification.md`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected discovery
manifest, selected generation, and pinned toolchain lock. It returns:

- status `PASS`;
- one obligation;
- generated tree
  `7796a58da3724bfe844e4ccc3ad5df12b23c95f7db60fbda59688db408db6904`;
- zero designated sorries;
- 50 generated trust declarations; and
- successful clean and build diagnostics.

The audit sandbox initially denied Lean 4.22's
`readlink("/proc/<current-pid>/exe")` even though it allows the equivalent
`/proc/self/exe`. That caused an environment-only first preflight failure. I
confirmed the exact permission asymmetry and used the preserved
`evidence/lean-app-path-shim.c`, which redirects only that exact self-PID
readlink. It does not modify a project, declaration, term, elaboration, or
kernel check. With this narrow runtime correction, the mandated preflight
passes and reproduces the recorded Stage 4 build output hash
`8250decced98e3a463305169b7c4dce4053180dc193c47c8ee91fd3a8198a412`.
The failure diagnosis and successful returned evidence are in
`evidence/06-preflight-result.json`,
`evidence/13-proc-app-path-root-cause.txt`, and
`evidence/15-preflight-rerun-result.json`.

The independent source-rule/obligation mapping is exact:

- independently classified domain set: one rule,
  `rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7`;
- generated source-rule set: that same one rule;
- generated obligation set: that same one rule;
- source span: line 38;
- normalized hash:
  `115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7`;
- inventory and discovery hashes: exact matches;
- no duplicate or omitted IDs.

The obligation is the unguarded and non-vacuous proposition

`∀ A B C : SortInt, add (add A B) C = add A (add B C)`.

It neither adds a premise nor drops variables or cases from the frozen K rule.
It is mathematically relevant for the reason demonstrated by the deletion
mutation. There is one conjunct, so there are no duplicate or vacuous
conjuncts.

The generated target occurs exactly once at
`Klean36FizzBuzz/Lemmas.lean:9`. It is the exact expected conjunction. Its
identity matches the generator manifest, recorded preflight, trusted
recomputation, and `/audit-input.json`:

- declaration: `Klean36FizzBuzz.Lemmas.targetStatement`;
- definition SHA-256:
  `f5de4b2237c7af5067d9f684fd0ceeb08bc2caf891532eba3722805ed96c620e`;
- statement:
  `Klean36FizzBuzz.Lemmas.targetStatement «_+Int_»`;
- statement SHA-256:
  `83aeddd5dbd588726a15128801c81b7cd2d02c4ecef9f957e43beb4742104de6`.

The obligation-map hash, target-definition hash, conjunct hash,
trust-inventory hash, discovery hash, verification hash, generated tree hash,
and all Stage 1/Stage 3 cross-bindings independently match their recorded
values. See `evidence/16-hash-reconciliation.json`.

The domain set is nonempty, so `PASS` with a target is the correct Stage 4
shape; `KLEAN_NO_OBLIGATIONS` would have been invalid here.

## Fresh Stage 5 build and target identity

I created `/tmp/audit-work/36-fizz-buzz-stage5-audit`, copied the immutable
generated project into it as `Base`, and copied only the candidate
`Proof.lean`, `lakefile.lean`, and `lean-toolchain` to the project root. The
scratch `Base` digest before and after the build is exactly the frozen
generated-tree digest. Each copied candidate source is byte-identical to its
mounted counterpart.

I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, ending with `Built Proof` and
  `Build completed successfully`.

Complete stdout, stderr, and exit records are in
`evidence/19-lake-clean.*` and `evidence/20-lake-build.*`.

The candidate-local sources contain no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`. They do not define or shadow `targetStatement`; the only target
definition remains the immutable one in `Base`. The candidate contains
exactly one `theorem final`, and trusted mechanical parsing confirms its type
is exactly the generator's fixed statement. Lean prints:

`theorem Proof.final :
Klean36FizzBuzz.Lemmas.targetStatement Proof.«_+Int_»`.

There is no duplicated, weakened, or vacuous replacement theorem. See
`evidence/21-candidate-integrity-and-target.txt` and
`evidence/24-proof-identity.stdout.txt`.

## Operational parameter bridge

The target has one parameter:

- name: `«_+Int_»`;
- type: `SortInt → SortInt → SortInt`;
- KORE symbol: `Lbl'UndsPlus'Int'Unds'`;
- bound source rule: the line-38 associativity rule.

The candidate's exact definition is:

`def «_+Int_» (x0 x1 : SortInt) : SortInt := x0 + x1`.

This is operationally correct:

1. Generated `Prelude.lean` defines `SortInt` as Lean `Int`.
2. A fresh compilation of the frozen K sources declares the recorded KORE
   symbol as a total hooked symbol with `hook("INT.add")` and SMT hook `+`.
3. Frozen `semantic.k:70` executes source `BinOp("+", ...)` as K
   `A +Int B`.
4. The frozen source and translated program use that operation for both
   `count := count + 1` and `i := i + 1`.
5. The bound source lemma uses the same `+Int` symbol on both sides.
6. Lean accepts a universal, definitional bridge theorem
   `Proof.«_+Int_» x y = x + y` by `rfl`, with no axioms.

Fresh adversarial evaluations include negative, zero, ordinary, and very large
integers:

- `(-5) + 2 = -3`;
- `0 + 7 = 7`;
- `11 + 13 = 24`;
- `100000000000000000000 + 99999999999999999999 =
  199999999999999999999`.

The KORE/source linkage is preserved in
`evidence/28-operational-bridge-source-and-kore.txt`; the Lean bridge and
evaluations are in `evidence/24-proof-identity.stdout.txt`.

I also tried two counterfactual replacements. A constant-zero operation and a
left-projection operation both prove the generated associativity target by
reflexivity, with outputs `0` and `11` respectively on inputs `(11, 13)`.
Thus the target equation alone cannot establish the operational bridge. Both
counterfactuals are rejected semantically because K's total `INT.add` result
is `24`; the actual candidate is not one of these convenient definitions and
implements addition exactly. Probe sources and results are in
`evidence/38-lean-probe-sources.txt` and
`evidence/25-counterfactual-results.txt`.

## Proof identity and axiom accounting

Lean elaborates the candidate proof as:

`fun A B C => Int.add_assoc A B C`.

The mandated exact query
`#print axioms Proof.final` exits 0 and prints:

`'Proof.final' depends on axioms: [propext]`

This exact output is saved in `evidence/22-print-axioms.stdout.txt`.

The dependency reconciliation is complete:

- `Proof.«_+Int_»` has no axiom dependencies;
- the fixed generated `targetStatement` has no axiom dependencies;
- `Int.add_assoc` depends on `[propext]`;
- `Proof.final` has exactly the same `[propext]` dependency;
- no generated trust-inventory declaration is in the closure;
- `sorryAx` is absent.

`propext` is Lean's fixed core proposition-extensionality axiom, printed by
Lean as `axiom propext : ∀ {a b : Prop}, (a ↔ b) → a = b`. It is not a
candidate-created or generated project declaration. The trusted final gate
explicitly recognizes the fixed Lean core axioms `propext`,
`Classical.choice`, and `Quot.sound` in addition to the generated inventory;
only `propext` is used here. Therefore this is reconciled core logic, not an
unrecorded candidate proof escape. The 50 generated declarations exactly
match `trust-inventory.json`, but none is used by `Proof.final`.

The origin queries are in `evidence/32-axiom-origins.stdout.txt` and
`evidence/33-core-propext.stdout.txt`. The trusted
`klean_final_gate.py` reruns preflight, clean build, exact target checking, and
axiom parsing and returns `status: PASS`, `used_axioms: ["propext"]`; its full
result is `evidence/34-final-mechanical-gate-result.json`.

## Final judgment

The Stage 3 manifest is bijective and semantically correct. The nonempty domain
set is exactly the relevant integer-associativity lemma. Stage 4 preserves
that rule without weakening or vacuity and fixes one exact target. Stage 5
clean-builds, proves exactly that target, introduces no forbidden trust
declaration, and binds the target parameter to the frozen total K integer
addition operation rather than to a convenient associative substitute. No
material concern remains.

VERDICT: PASS
LEGITIMACY: LEGIT
