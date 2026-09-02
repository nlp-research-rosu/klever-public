# Independent audit: `24-largest-divisor` / `semantics`

Audit mode was `CLASSIFICATION_AND_PROOF`; the launcher input and
`AUDIT_MODE` agreed. The frozen semantics mode was `SUPPLIED_SEMANTICS`.

## Result

Stage 3 classification is correct and Stage 4 is structurally self-consistent,
but the generated Lean obligation is mathematically vacuous. The frozen K sort
`Scope` is inhabited by `scope(Map, Parent)`, whereas Stage 4 generated an
empty Lean inductive `SortScope`. The only target conjunct quantifies over
`_S : SortScope`, so it has no instances.

Independently, the Stage 5 `_Map_` definition is list append and therefore
does not implement K's associative-commutative `MAP.concat` symbol even for
two disjoint integer-keyed singleton maps. These are proof-legitimacy failures,
not hash, producer-provenance, or build failures.

## Producer and mounted-input authentication

The generation-time producer sources are present and authenticated:

| Artifact | Recomputed SHA-256 |
|---|---|
| `generation-tools/klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `generation-tools/klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |
| Producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

Both file hashes agree with `source-manifest.json` and
`generator-manifest.json`. The immutable image identifier
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
agrees between those manifests and the basename of the producer-source path
recorded in `/audit-input.json`.

All 37 launcher-recorded Stage 1 source hashes match. The mounted Stage 1,
Stage 2 audit, Stage 3 manifest, Stage 4 generation, generated project,
producer-source tree, and Stage 5 candidate tree hashes also match their
launcher records. The launcher records a `lean_invocation_sha256`, but no
Stage 5 invocation artifact is mounted; I did not rely on that unmaterialized
hash. See `evidence/01-producer-authentication.txt`,
`evidence/05-mounted-tree-hashes.txt`, and
`evidence/24-independent-recorded-hash-audit.txt`.

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`. The reconstructed `verification.k` hash is
`79c0b9b931a43d5259d1836266130985241b15c21fae4e16c480bd902b358eb0`,
and the canonical whole-inventory hash is
`1d8f722885d42ef29665976d7d341a53686993fa57703f73b3f2423f7b4e7b90`.

The reconstructed ordered inventory is:

| Lines | `source_rule_id` / normalized SHA-256 | Independent classification |
|---|---|---|
| 9–17 | `rule-4dc883be7558c48413570e94ef894be86bb7f2defba4701dddd8ecbdfc6fdf61` | `DEFINITION` |
| 25–26 | `rule-7e08785f2fa3d9871eb727a17489e6ad09a58d3acdd6b1aa0576bb1cf35e0069` | `DEFINITION` |
| 28–29 | `rule-ff250606498fa2b0f63ef3d95275fc5bcf246520b20e477dc18297ba8710f027` | `DEFINITION` |
| 31–33 | `rule-864338f2577bfe3d8f78663dcfd53efcfbb9747d6d849326441f6cbd4b554fb8` | `DEFINITION` |
| 38–41 | `rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630` | `DOMAIN_LEMMA` |

The five protected entries are a unique, ordered bijection with this
inventory. There are no omissions, extras, duplicate identities, changed
spans, reordered rules, or changed hashes.

The classifications are substantively correct:

- `largestDivisorBody()` is a named proof term expanding to the exact
  translated source body.
- `largestProperDivisor` initializes a mathematical descending scan.
- The two `firstDivisorAtOrBelow` equations are the base and recursive
  equations of that scan. The proof uses them only with candidates at least
  one, where the cases cover the scan and recursion descends.
- `deleteFreshFrame` is not a definition, ordinary program-execution rule, or
  separately proved derived lemma. It is the Map-domain law that removing a
  fresh integer-keyed frame from a disjoint map restores the remainder.

The only `[simplification]` rule is therefore correctly a `DOMAIN_LEMMA`.
It is relevant: returning from `largest_divisor` reaches the frozen `#pop`
rule, which updates `<scopes>` from `SC` to `SC [ L <- undef ]`. Stage 1
compiled the local rule into `VERIFICATION` before all three proof commands
and never first proved the exact rule in a module without it, so
`PROVED_DERIVED_LEMMA` would be invalid. Evidence is in
`evidence/03-rule-inventory-and-discovery.txt`,
`evidence/04-frozen-stage1-sources.txt`,
`evidence/06-inventory-bijection.txt`, and
`evidence/07-relevant-operational-semantics.txt`.

## Stage 4 structural and target audit

The required fresh call to
`tools.klean_preflight.check_generation`, with `PYTHONPATH=/reference` and
the frozen Stage 1, Stage 3, and Stage 4 paths, returned `PASS`. It found:

- one domain obligation;
- generated tree
  `23b1b1d57a90a7f3361dcea43ebd08171ea43f5eb9a5e05e0b96bbb308a41e13`;
- zero designated sorries;
- 50 generated trust declarations; and
- successful clean and build commands.

The first invocation exposed a container PID-namespace issue: Lean 4.22
looked up `/proc/<namespace-pid>/exe` while this container's `/proc` exposes
host PIDs. A narrow `LD_PRELOAD` shim made `getpid()` return the numeric target
of `/proc/self`; it did not modify Lean, Lake, any input, or any proof source.
The failed attempt, diagnosis, shim source/hash, and successful rerun are all
preserved in `evidence/10-fresh-stage4-preflight.txt` through
`evidence/16-fresh-stage4-preflight-success.txt`.

The protected domain set contains exactly
`rule-feff944e...f630`, and `obligation-map.json` contains exactly one
obligation with that same identity, span 38–41, normalized hash, inventory
hash, and discovery hash. Its conjunct is the direct syntactic translation
of the local Map-removal rule. There are no structural omissions, duplicates,
extra obligations, target changes, or changed provenance bindings.

The extracted target agrees byte-for-normalized-byte with the obligation map,
generator manifest, Stage 4 preflight record, and audit input:

- declaration: `Klean24LargestDivisor.Lemmas.targetStatement`;
- definition SHA-256:
  `eef252e691d588778e3187ede990e62988b76155e914444802f104e7b9efb4e4`;
- instantiated statement SHA-256:
  `ef40fed572bed032138fe5b45bc11354d1d5982a4f0c4957b641b061846a0cfb`.

See `evidence/16-fresh-stage4-preflight-success.txt` and
`evidence/20-target-identity-bijection-forbidden-scan.txt`.

### Fatal mathematical defect: empty `SortScope`

Structural integrity is not mathematical adequacy. Frozen
`reference-semantics/semantics/core.k` declares:

```k
syntax Parent ::= "root" | parent(Int)
syntax Scope  ::= scope(Map, Parent)
```

The initial configuration contains
`0 |-> scope(.Map, parent(-1))`, so `Scope` is operationally inhabited.
The generated `Sorts.lean` instead contains only:

```lean
inductive SortScope : Type
```

with no constructors anywhere in the generated project. The generated target's
only conjunct begins:

```lean
∀ (SC : SortMap) (_S : SortScope) ...
```

It is therefore true for every choice of the five target parameters simply
because `_S` cannot exist. This weakens the nonempty K-domain lemma to an empty
Lean domain.

`evidence/22-vacuity-and-operational-adversarial-lean.txt` machine-checks a
counterfactual theorem using deliberately nonsensical parameters: right
projection for map concatenation, constant membership, identity deletion,
an empty element map, and constant Boolean negation. The exact generated
target still closes solely by `nomatch impossibleScope`. This is a vacuous
conjunct and makes Stage 4 mathematically unacceptable despite all matching
hashes.

## Stage 5 proof and trust audit

I created a fresh project at
`/tmp/audit-work/lean-audit-wsL1bE`, copied the candidate into it, and copied
the immutable generated project contents into its existing `Base/` directory.
Both required commands then succeeded:

- `lake clean`: exit 0;
- `lake build`: exit 0.

An earlier fresh-copy attempt nested the generated directory below the
candidate's pre-existing empty `Base/` placeholder; Lake rejected that layout
before compilation. It is retained as
`evidence/17-fresh-candidate-clean-build.txt`; the correctly constructed clean
build is `evidence/18-fresh-candidate-clean-build-success.txt`.

Post-build comparison confirms that `Base` still matches the generated source
project and that `Proof.lean` still matches the mounted candidate. The
candidate contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`, and it
does not declare or shadow `targetStatement`. `Proof.final` states the exact
fixed target. See `evidence/20-target-identity-bijection-forbidden-scan.txt`,
`evidence/21-trusted-proof-candidate-gate.txt`, and
`evidence/27-post-build-source-identity.txt`.

The exact independent axiom output was:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

There is no `sorryAx`. Neither of the 50 generated trust declarations is used.
`propext` and `Quot.sound` are the explicitly recognized Lean core/kernel
allowances in the trusted final gate; there are no unrecorded dependencies.
See `evidence/19-print-axioms-proof-final.txt` and
`evidence/25-axiom-reconciliation.txt`.

### Operational-bridge audit

All five parameter bindings name the one source domain rule, but their
definitions must still implement the corresponding KORE symbols:

| Parameter | Candidate definition | Judgment |
|---|---|---|
| `_Map_` / `MAP.concat` | concatenates the two association lists with `++` | **Fail** |
| `_in_keys...` / `MAP.in_keys` | list `any` using `sameMapKey` | **Fail on general `KItem` keys** |
| `_[_<-undef]` / `MAP.remove` | list filter using `sameMapKey` | **Fail on general `KItem` keys** |
| `_|->_` / `MAP.element` | singleton association list | Consistent with an association-list representation |
| `notBool_` / `BOOL.not` | Lean Boolean negation | Correct |

K declares `_Map_` associative and commutative and defines it on maps with
disjoint keys. The adversarial Lean check uses two disjoint singleton maps
with integer keys 1 and 2, well inside the program's operational key domain.
The candidate yields distinguishable orders:

```text
first key is 1 in `_Map_ m1 m2`: true
first key is 1 in `_Map_ m2 m1`: false
```

and Lean proves the two results unequal. Thus list append does not interpret
the bound commutative K map symbol even on its defined domain.

Moreover, `sameMapKey` handles only injected integers and strings and returns
false for every other pair. On a map whose key is `inj_SortBool true`, the
candidate reports membership `false` and deletion leaves one entry, whereas
K's `Map` is from arbitrary `KItem` keys and its hooks must report membership
and remove that key. These executable observations are in
`evidence/22-vacuity-and-operational-adversarial-lean.txt`; the exact K hook
declarations and candidate definitions are collected in
`evidence/26-operational-bridge-source-comparison.txt`.

Even if the membership/delete comparison were narrowed to the integer/string
keys reachable in this particular MPY program, `_Map_` still fails on disjoint
integer-keyed maps. The candidate proof succeeds because the target is empty
and does not exercise any operational implementation.

## Final judgment

Stage 3 has a complete and correct classification. Stage 4 passes deterministic
provenance, hash, bijection, and build checks but generates a vacuous theorem
that is not the frozen nonempty-domain Map law. Stage 5 cleanly proves exactly
that vacuous theorem with an acceptable axiom list, but its `_Map_` bridge also
fails the frozen operational semantics. A clean build and exact theorem
identity cannot repair either defect.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
