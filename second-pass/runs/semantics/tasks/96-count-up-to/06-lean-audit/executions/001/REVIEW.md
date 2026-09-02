# Independent audit: HumanEval 96-count-up-to

## Result

I independently audited condition `semantics` in semantics mode
`SUPPLIED_SEMANTICS`. The launcher and environment both selected
`CLASSIFICATION_AND_PROOF`.

The protected Stage 3 classification is complete and mathematically correct.
Stage 4 deterministically generated exactly the two genuine loop-summary
obligations without weakening or changing the target. The Stage 5 project
clean-builds, proves that fixed target without a candidate-added trust escape,
and supplies operationally faithful definitions for every target parameter.

## Producer provenance and frozen inputs

I performed the producer-source gate before judging Stage 4. The observed
producer hashes are:

- `klean_export.py`:
  `6d620b92d4de6a051dea0ef5ed4670a77d76199648a7b64808b91286b3dd20c0`
- `klean.py`:
  `1ba065b19feb2fb0a48abe80bc2cf0d0afd3d72289374303745e0d5a59f0bccc`
- canonical producer bundle:
  `83415436ab900e1a996037f6c97d291e693e705c9de30342d3e142bd264dfbfb`
- immutable generator image:
  `sha256:9552b3eb7f21ae17e7ade215d2115ed1f2232426ba7ebc2af7c8784215780274`

The two source hashes agree across `source-manifest.json`,
`generator-manifest.json`, and `/audit-input.json`. The bundle has exactly the
three recorded files, its canonical tree hash matches `/audit-input.json`, and
the image ID agrees in the source manifest, generator manifest, and the
launcher-recorded producer path. The infrastructure gate therefore passes.

Using the launcher/generator canonical hash functions, I also recomputed every
mounted top-level hash for which the launcher supplied a mounted object:

| Object | Recomputed hash | Result |
| --- | --- | --- |
| Stage 1 K workspace | `118cd172a9c352af15f3a2198ead2e31a429a5cc1b023b99661a0be14da7298b` | match |
| Stage 1 frozen export | `0d69bef5ee3eb5fa647e7e8aeae630c3d9780236cdcc1c47757d5a461de3b33e` | match |
| Stage 3 discovery file | `dc4482e6beb53430c8640b901dae31bf53af2b2871e2ca964764c613fb6e9a06` | match |
| Selected K audit | `bc27f22d0256471571378468ea62aaa55bb98c306abb44b75c9ec8ca32d7363d` | match |
| Stage 4 generation bundle | `b84b4173d760ba9856b955ecf6c306d8f5bc576a5ab4c8c222fa5d6d34f18d7e` | match |
| Producer bundle | `83415436ab900e1a996037f6c97d291e693e705c9de30342d3e142bd264dfbfb` | match |
| Generated project | `4b7864e4e762819dab8a825f9b2cafbcacbff903547e8007c8446a092f0b68ac` | match |
| Candidate Lean workspace | `3e28a79538898d93eda1b82c6765169e76a3cbe0dfc8cd3fead58dab83d55313` | match |

All individual Stage 1 source hashes also match. The launcher records a Lean
invocation hash, but no separate invocation artifact is mounted from which to
recompute it; I did not treat the launcher record alone as an independent
check.

## Stage 3 inventory reconstruction

I ran the trusted local rule inventory on `/reference/k-proof`, independently
of the protected classification. It selected verification module
`COUNT-UP-TO-WITH-OUTER` and reconstructed this ordered local closure:

1. `COUNT-UP-TO-BASE`
2. `COUNT-UP-TO-WITH-INNER`
3. `COUNT-UP-TO-WITH-OUTER`

The frozen `verification.k` hash is
`7b982f2674041fa71d15dbcb6d5f9f680f57ff4059b9cd072684a072dde1439f`.
The reconstructed canonical inventory has nine unique entries and hash
`248228e8fdfc6e33e8b384cf6ee6d6599339e96ceb0bed8b684817fefeffc574`.

For each entry I recomputed the source span, normalized source, normalized
SHA-256, and `source_rule_id`. The protected manifest is a bijection with the
reconstruction: same nine unique IDs, same order, same modules, same spans,
same normalized hashes, and the same whole-inventory hash. There are no
omissions, duplicates, extras, reordered identities, or unaccounted
classifications.

### Independent classification

| Index | Module and span | Recomputed identity | Classification | Judgment |
| --- | --- | --- | --- | --- |
| 0 | base, 11–12 | `rule-3fd8fd1461c846ce04fb9836fb4027e1f766622bc9007f6df9436864c68df78c` | `DEFINITION` | `noDivisor` stopping case |
| 1 | base, 13–14 | `rule-2ddb2c047b23e8c62bd5f396488db85f22bdeb90e9cd3f012b55c4a8afdf044f` | `DEFINITION` | divisor-found case |
| 2 | base, 15–17 | `rule-a5dd03d74f2397ad15d952b0f1061edc2250d99cff9166dce37b08b892342316` | `DEFINITION` | `noDivisor` recurrence |
| 3 | base, 22 | `rule-21d36a84375658a572f41d1591520a1c2d9b6006b7b384021af3b07d880e290c` | `DEFINITION` | false `appendIfPrime` case |
| 4 | base, 23–24 | `rule-165d98d2cdf2e1e8fc6bb2cb8c7a4690fdf535c966e889a7fd578bb38293f334` | `DEFINITION` | true append case |
| 5 | base, 31–32 | `rule-e3f610fa6210b74d8634f7c0ea1fba43078d455966137ef34884cac9b79169a2` | `DEFINITION` | `primesAcc` stopping case |
| 6 | base, 33–38 | `rule-c693e9dfdde9b8d6790e2a6e90151e9c3705ea0219e6f32fa07265391856459b` | `DEFINITION` | `primesAcc` recurrence |
| 7 | inner, 46–73 | `rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e` | `DOMAIN_LEMMA` | summarizes the entire divisor loop |
| 8 | outer, 82–122 | `rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5` | `DOMAIN_LEMMA` | summarizes the entire candidate loop |

The first seven rules define named mathematical summaries and their
recurrences, so `DEFINITION` is exact. The two priority-40 rules replace whole
`#while` computations with summarized state changes. Under the supplied MPY
semantics, ordinary execution instead expands `While` to `#while`, evaluates
the guard and body, updates locals through assignment/augmented assignment,
uses Python-style `pyMod`, and mutates the result list through `append`.
Consequently the two whole-loop rules are not ordinary execution or
observation rules.

Stage 1 does prove related claims before importing the summaries, but it does
not prove the *exact same rules*. Among other differences, the claims fix
`builtinsScope` and explicitly bind machine cells that the reusable rules
frame or omit, while the rules generalize the builtins map as `BI`. They
therefore do not satisfy the exact-identity requirement for
`PROVED_DERIVED_LEMMA`; `DOMAIN_LEMMA` is the correct category.

Both domain lemmas are relevant. The source program contains exactly the
nested divisor and candidate loops. The inner summary determines primality
through `noDivisor`; the outer summary determines the returned list through
`primesAcc`. No inventory rule has the `simplification` attribute, so no
simplification rule falls outside `DEFINITION` or `DOMAIN_LEMMA`.

## Stage 4 deterministic generation

I reran:

```text
PYTHONPATH=/reference tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation
)
```

with the trusted toolchain lock. The returned evidence reports `PASS`, two
obligations, zero designated sorries, 82 recorded trust declarations, and
successful generated-project `lake clean` and `lake build` commands. Its
frozen input, discovery, generated tree, target, and trust counts agree with
the recorded preflight.

The managed sandbox exposes `/proc/self/exe` but not Lean's equivalent
`/proc/<inner-pid>/exe`, so unmodified Lean initially could not detect its
installation. To execute the required checks, I used a narrow audit-only
`LD_PRELOAD` shim that redirects only `readlink("/proc/<digits>/exe")` to
`/proc/self/exe`. Its full source and hashes are in
`evidence/lean-proc-shim.txt`; it does not intercept files, compilation, proof
checking, or command results. With it, the pinned executable reports Lean
4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

### Obligation and target judgment

The independently classified domain set, obligation IDs, and obligation-map
source IDs are the same ordered pair:

1. `rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e`
2. `rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5`

Both IDs and both conjunct hashes are unique. Each obligation records the
exact reconstructed span, normalized hash, inventory hash, and discovery
hash. The obligation-map hash
`18ac5fdffd14f95f1eb842dd903a1ea80ad23163ce6af802a0fb71953c4c50fb`
matches its manifest.

The first conjunct contains the exact inner `#while`, guard, modulo test,
assignment, and divisor increment. Its destination changes the divisor to
`C`, changes `is_prime` to `B andBool noDivisor(C,D,C)`, and preserves the
heap. The second contains the exact nested outer body, including the append
and the three end-of-iteration updates. Its destination changes candidate
`I` to `N` and the heap list to `primesAcc(VS,I,N)`.

Neither conjunct is literal `True` or `False`; both are universal reachability
claims with meaningful guard hypotheses. The guards are satisfiable, for
example with inner `D = C = 2` and outer `I = N = 2`. The destination effects
are not identities on general inputs. I found no irrelevant, weakened,
duplicated, omitted, or vacuous obligation.

The generated target is exactly the trusted deterministic conjunction:

- declaration: `Klean96CountUpTo.Lemmas.targetStatement`
- file: `Klean96CountUpTo/Lemmas.lean`
- definition hash:
  `0ba11a839a95d2a82056b046e9c4583d97913207fd0a36cc67fdd67362264d0e`
- instantiated statement:
  `Klean96CountUpTo.Lemmas.targetStatement _Map_ _andBool_ «_<=Int_» «_|->_» noDivisor primesAcc`
- statement hash:
  `9b37fb26753cfc20232895f77fd878287460d4f1ce5ceb0254b7afcc64955000`

Those values independently match the obligation map, generator manifest,
audit input, successful preflight, and recomputation with the trusted target
builder. Stage 4 status is `PASS`, not `KLEAN_NO_OBLIGATIONS`; the true domain
set is nonempty and correctly generated as two obligations.

## Stage 5 Lean proof

I created a fresh project at the path recorded in
`evidence/stage5-fresh-copy-path.txt`, copied the generated project into it as
`Base`, and ran both `lake clean` and `lake build`. Both exited 0. The complete
build output is preserved in `evidence/stage5-lake-build.log`; it contains
only linter warnings and ends with `Built Proof` and
`Build completed successfully`.

After the rebuild:

- the fresh `Base` tree still hashes to
  `4b7864e4e762819dab8a825f9b2cafbcacbff903547e8007c8446a092f0b68ac`;
- the target declaration, statement, definition hash, and statement hash are
  exactly the fixed values above;
- no candidate source declares or shadows `targetStatement`;
- no candidate source contains `sorry`, `admit`, `unsafe`, a new `axiom`, or
  a new `opaque`; and
- `Proof.final` has exactly the fixed generated statement as its type, with
  the six candidate definitions supplied as the target parameters.

The proof unfolds that target and proves both original conjuncts. It does not
prove a duplicate, a weakened theorem, or an independent vacuous variant.

### Circularity and axiom accounting

I inventoried all 48 distinct `Rewrites.*` names referenced by the candidate.
Forty-five are generated ordinary semantic/transitivity constructors and
three are candidate helper theorems proved from such constructors. The only
generated constructors mentioning the generated `noDivisor` or `primesAcc`
axioms are the separate `kxExport0` and `kxExport2` sentinel constructors.
The candidate uses neither. In particular, it does not invoke a generated
inner- or outer-loop summary to prove that same summary; it explicitly
composes guard evaluation, branches, local lookup/update, modulo, increment,
append, loop-back, and loop-exit steps.

An exact Lean run of `#print axioms Proof.final` reports 34 dependencies:
31 generated names plus Lean's ordinary `propext`, `Classical.choice`, and
`Quot.sound`. All 31 generated names occur in both the 82-entry
`trust-inventory.json` axiom inventory and its allowlist, with the recorded
source, line, and reason. There is no `sorryAx` and no unrecorded generated
dependency.

The trace includes the generated root names `noDivisor` and `primesAcc`
because Lean's `Rewrites` inductive declaration contains the separate export
constructors, so every theorem whose type uses `Rewrites` inherits the
inductive declaration's dependencies. `#print axioms Rewrites` and
`#print axioms Rewrites.tran` produce the same list. The constructor-use audit
above establishes that the proof does not use those exports as shortcuts.

### Operational bridge audit

I located each exact candidate `def` named by `target.parameters` and compared
it with its bound KORE symbol, source-rule IDs, frozen rules, source program,
and the supplied operational semantics.

| Parameter | Independent judgment |
| --- | --- |
| `_Map_` / `Lbl'Unds'Map'Unds'` | Forms the union of both association lists. The concrete list is concatenated in reverse syntactic order, which is observationally equivalent on the disjoint maps admitted by K's associative/commutative map union. On overlapping keys the K hook is undefined, so its totalization is irrelevant. Tests show both distinct bindings remain independently retrievable; it is neither constant nor an identity projection. |
| `_andBool_` / `Lbl'Unds'andBool'Unds'` | Lean Boolean conjunction; the complete four-case truth table is correct. |
| `«_<=Int_»` / `Lbl'Unds-LT-Eqls'Int'Unds'` | `decide (left ≤ right)`; negative, equality, and false-order cases agree with the K integer comparison. |
| `«_|->_»` / `Lbl'UndsPipe'-'-GT-Unds'` | Constructs exactly one key/value binding; key lookup and cardinality tests distinguish it from empty, constant, and identity implementations. |
| `noDivisor` / `LblnoDivisor` | Uses the supplied Python modulo formula `((a % b) + b) % b` via `Int.tmod`, then scans exactly `[divisor, upper)`. Independently checked Lean theorems establish the frozen base, divisor-found, and recursive cases. Examples distinguish primes and composites: 4, 9, and 15 return false, while 2, 5, and 11 return true. |
| `primesAcc` / `LblprimesAcc` | Iterates exactly `[start, upper)`, calls `noDivisor(i,2,i)`, appends `i` only when prime, and preserves the supplied prefix. Independently checked Lean theorems establish the frozen stop and recurrence equations, and the existing append theorem connects its append helper to the MPY `valSeqConcat` hook. |

Adversarial evaluations produced:

- Python modulo witnesses `pyMod(-5,3) = 1`, `pyMod(5,-3) = -1`, and
  `pyMod(9,3) = 0`;
- `primesAcc([],2,10) = [2,3,5,7]`;
- `primesAcc([99],2,6) = [99,2,3,5]`;
- changing the start from 3 to 4 over the same upper bound changes
  `[3,5,7]` to `[5,7]`; and
- the two-entry map returns the separate values at both keys and no value at
  an absent key.

These examples and recurrence theorems rule out constant, identity,
hard-coded, and seed-discarding counterfeits. More importantly, the candidate
proof itself uses these definitions while replaying the frozen MPY operational
steps, including the exact inner and outer loop measures. I find no
operational-bridge failure.

## Evidence index

Raw commands and results are under `evidence/`. The principal files are:

- `audit-context.txt`
- `producer-provenance-authoritative.txt`
- `mounted-hash-reconciliation.txt`
- `stage3-inventory.json` and `stage3-bijection.txt`
- `stage4-preflight-command.txt` and `stage4-preflight-rerun-success.json`
- `stage4-obligation-target-audit.txt`
- `lean-proc-shim.txt`
- `stage5-lake-clean.log` and `stage5-lake-build.log`
- `stage5-forbidden-shadow-scan.log`
- `stage5-target-identity.txt`
- `stage5-print-axioms.log`
- `stage5-axiom-reconciliation.txt` and `stage5-axiom-origin.log`
- `stage5-constructor-audit.txt`
- `stage5-operational-bridge-tests.log`

VERDICT: PASS
LEGITIMACY: LEGIT
