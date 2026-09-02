# Independent audit: `38-decode-cyclic`

Audit mode was `CLASSIFICATION_AND_PROOF`; condition was `bare`; semantics mode
was `GENERATED_SEMANTICS`. I treated every mounted candidate, prior review, log,
comment, and manifest as evidence rather than authority.

## Outcome

The protected Stage 3 classification is complete and correct, the selected
Stage 4 generation is structurally and mathematically faithful to the three
true domain lemmas, and the Stage 5 candidate clean-builds and proves exactly
the immutable generated target. Its four parameter definitions implement the
reachable K operations rather than merely exploiting the target equations.

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` over
`/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`; its imported `MPY` and `MAP-SYMBOLIC` modules are external to
`verification.k`, so there are no additional local modules in this closure.
The reconstructed `verification.k` SHA-256 is
`330223b03ce586a4acf9294a57c3244ba7421059c3d508794b9c40d8a5aaca4f`,
and the canonical ordered inventory hash is
`d2db99b7bfbb6f10173dc29736d6dd1020fae34b484b232cc0ed4a77b679becb`.

| Span | `source_rule_id` / normalized hash | Independent classification | Judgment |
|---|---|---|---|
| 9–11 | `rule-ef7d5d777b33ed834768f6d5eae1abcfc5bb3ea8e0391ad21da31281612828ec` | `DOMAIN_LEMMA` | This is injectivity of K's total `MAP.update` at a fixed key. It simplifies a proof equality; it neither defines a term nor performs program execution. It is relevant because assignment updates the `<env>` map and the loop claim matches updated environments. |
| 13 | `rule-aa08fc7ab00f7ed5932bfabaec47fbf527e50b83d0b239787af7e592a9c05a9d` | `DOMAIN_LEMMA` | Nonnegativity of code-point string length is a general string-domain fact. It is used by the loop invariant's `0 <=Int I <=Int lengthString(S)` domain and the guarded string operations. |
| 14 | `rule-6a69a83530cb8d2469f0452d5b6878c9d18dc4dbc80234500bed171c1b093548` | `DOMAIN_LEMMA` | Full valid-range substring identity is a general string-domain fact. It is directly relevant to the decoder's indexed blocks, tail slice, return, and `decodeFrom` postcondition. |

All three rules have the `simplification` attribute and are correctly placed in
an allowed class. None names a summary, recurrence, macro, or proof term, so
none is a `DEFINITION`. None is an ordinary execution/observation rule, so none
is an `OPERATIONAL_RULE`. Stage 1's `prove.sh` performs one `kprove` with all
three rules already reachable through `spec.k`; there is no earlier proof of
any exact rule against a module that omits it. Thus none qualifies as
`PROVED_DERIVED_LEMMA`.

For every entry, I independently re-extracted the source lines, normalized
whitespace, recomputed SHA-256 and `source_rule_id`, and recomputed the
canonical inventory hash. The Stage 3 manifest contains the same three IDs
once each and in the same order, with no omission, duplicate, extra entry, or
hash change. The full reconstruction is in
[inventory-reconstruction.log](/audit-output/evidence/inventory-reconstruction.log)
and the independent assertions are in
[independent-checks.log](/audit-output/evidence/independent-checks.log).

## Hash and provenance checks

The signed audit-input digest and every hash whose referent is mounted were
recomputed successfully. In particular:

- Stage 1 pipeline tree:
  `f600725fab73470246ba886f9bf3af31bb1d72edca63918399cd60d871f1bc73`
- Stage 1 deterministic export tree:
  `2db69dd3a57605c6a212cedbe401470040ad29a65b7c00f27b9d286bb5ff3dff`
- selected Stage 2 audit tree:
  `a257592abdcfea9cecf9efce51a1e29a1d4b0b62342fc318f65a57761a25e6b2`
- Stage 3 manifest:
  `b5ecfd0e5ad951679b77e881ccf86470d4328205da3f2ef238dd9e8061ae5fb8`
- selected Stage 4 generation tree:
  `b2d2ee67e50006a244f35eb09575bb7d232056e23540da53b9692b35bbb93ae3`
- generated Lean tree:
  `9a729bf9e6da030fc7c4fe7790160f24365d0a04642cc6ab149786aecce5bd8d`
- Stage 5 candidate tree:
  `a929657b8239498ed485be3c9e954f9a039afb0ed52126cda7d71f68f6c0038e`

The complete Stage 1 source-file set and all ten source hashes also match the
audit input. Input-manifest, generator-provenance, obligation-map, conjunct,
binding, generated-tree, trust-inventory, export-result, target-definition,
and target-statement hash relations all match their mounted referents.

The audit input also records the original Stage 5 invocation-tree digest, but
that invocation directory is not one of the mounted inputs. Likewise, the
generation manifest records generation-time exporter source digests without
mounting those exact source blobs. I did not use those unavailable artifacts
as evidence; no mounted hash mismatched.

## Stage 4 generation

I reran the required function:

```text
PYTHONPATH=/reference python -c '... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json) ...'
```

The first attempt exposed a sandbox-specific Lean runtime failure:
`/proc/<getpid()>/exe` is absent although `/proc/self/exe` is available.
Lean 4.22 therefore reported `failed to locate application`. I preserved that
failure, then used a narrowly scoped `LD_PRELOAD` compatibility shim that
redirects only numeric `/proc/<pid>/exe` reads to `/proc/self/exe`. It does not
alter Lean sources, libraries, terms, elaboration, or kernel checking. With
that environment repair, the same trusted function returned `PASS`,
`obligation_count: 3`, zero sorries, and successful clean/build diagnostics.
See [check-generation.log](/audit-output/evidence/check-generation.log),
[proc-exe-compatibility-shim.log](/audit-output/evidence/proc-exe-compatibility-shim.log),
and [check-generation-rerun.log](/audit-output/evidence/check-generation-rerun.log).

The source-rule and obligation lists are an ordered bijection over the three
inventory IDs. Each obligation repeats the exact source span, normalized hash,
inventory hash, and discovery-manifest hash, and each Lean-conjunct hash
recomputes correctly.

Mathematically, the three conjuncts state exactly:

1. equality of two updates of the same map/key is equivalent to equality of
   the inserted values;
2. `0 <= lengthString(S)` evaluates to `true`; and
3. `substrString(S, 0, lengthString(S)) = S`.

The reverse direction in the first `↔` is the trivial congruence direction of
the same K equality simplification, not an unrelated obligation. Every
conjunct mentions its bound operation and quantified data; none is empty,
vacuous, weakened, duplicated, or unrelated to the decoder.

There is exactly one generated target:
`Klean38DecodeCyclic.Lemmas.targetStatement` in
`Klean38DecodeCyclic/Lemmas.lean`. Its definition hash is
`7bba40a4a2892d50612192343a8e7d8226c3ab93278ca4a4d062e68a5dc1b835`,
and its instantiated-statement hash is
`32a2ae8e9350f6d65d01c27776f3613cdd40397f360a1a8e886b85a2cf20fd80`.
Those values and the four parameter bindings agree exactly among the generated
file, obligation map, generator manifest, preflight result, and audit input.

## Stage 5 clean build, target identity, and trust

I copied `/candidate` to `/tmp/audit-work/stage5-fresh`, copied the immutable
generated project into it as `Base`, and ran:

```text
LD_PRELOAD=/tmp/audit-work/libfix_proc_exe.so lake clean
LD_PRELOAD=/tmp/audit-work/libfix_proc_exe.so lake build
```

Both exited 0. The full build output is in
[stage5-clean-build.log](/audit-output/evidence/stage5-clean-build.log).
The copied `Base` tree retained the exact generated-tree hash, and the copied
`Proof.lean` is byte-identical to `/candidate/Proof.lean`; see
[fresh-copy-identity.log](/audit-output/evidence/fresh-copy-identity.log).

The candidate has exactly one definition for each target parameter and one
`Proof.final`. It neither defines nor shadows `targetStatement`, and its Lean
sources contain no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.
`Proof.final`'s elaborated type is exactly the fixed target applied to those
four definitions; a separately compiled exact-type check is recorded in
[proof-identity.log](/audit-output/evidence/proof-identity.log). There is no
weakened copy or vacuous replacement theorem.

Running Lean on `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are Lean's standard logical/quotient dependencies. The generated trust
inventory contains 44 named Klean hook axioms; none occurs in the dependency
list. There is no `sorryAx`, no candidate-created trust declaration, and no
unreconciled dependency. Exact output and reconciliation are in
[print-axioms.log](/audit-output/evidence/print-axioms.log) and
[axiom-accounting.log](/audit-output/evidence/axiom-accounting.log).

## Operational-bridge audit

The generated equation alone is not sufficient to validate the parameter
implementations. I compiled a counterfactual Lean file in which:

- integer comparison is constantly `true`;
- length is constantly `0`;
- substring ignores its indices and returns the whole input; and
- map update discards the entire old map and returns only the new pair.

That deliberately bad collection still proves the immutable target. This
confirms that the independent bridge audit is material rather than redundant.
The compiled counterfactual and actual bridge tests are recorded in
[lean-bridge-tests.log](/audit-output/evidence/lean-bridge-tests.log).

The selected candidate passes the bridge audit:

| Parameter | Frozen operational meaning | Candidate and adversarial judgment |
|---|---|---|
| `«_<=Int_»` | K integer `<=`, bound to `Lbl'Unds-LT-Eqls'Int'Unds'` | `decide (x <= y)` is exact for all integers. Negative true/false cases agree with `krun`. |
| `«Map:update»` | Total K `MAP.update`; environment assignment uses `ENV [X <- V]` | The candidate removes the prior binding for the key, prepends the new binding, and preserves every other pair. K maps forbid duplicate keys and are order-insensitive, so this is the standard list representation of exact update on the valid map domain. Empty insertion and overwrite-with-unrelated-binding witnesses pass. |
| `«lengthString…»` | K `STRING.length`, measured in Unicode code points; used by loop/index/slice guards | `Int.ofNat s.length` is nonconstant and agrees on ASCII and mixed `A😀éZ` (`4`). |
| `«substrString…»` | K code-point half-open slice `[start,end)`; all frozen operational calls are guarded to valid indices | `s.toList.drop start.toNat |>.take (end-start).toNat` is the same code-point slice throughout that reachable domain. Mixed Unicode, nonempty, empty, and full-range cases agree. Its arbitrary totalization outside the K-valid index domain cannot affect any frozen execution rule. |

I independently compiled a small K probe against the installed pinned K
domains and compared it with Lean. Both sides returned `false`, `true`, `4`,
the Unicode slice `😀é`, and the empty slice for the integer/string cases.
K map overwrite and insertion produced exactly the expected extensional
bindings; the Lean witnesses proved overwrite preservation and empty-map
insertion. Commands and full results are in
[k-bridge-kompile.log](/audit-output/evidence/k-bridge-kompile.log) and
[k-bridge-results.log](/audit-output/evidence/k-bridge-results.log).

## Evidence summary

Raw commands and outputs are under `/audit-output/evidence/`. The principal
records are the inventory reconstruction, numbered frozen/generated/candidate
sources, Stage 4 manifests, trusted preflight rerun, independent hash and
bijection assertions, clean Stage 5 build, exact proof type, axiom accounting,
and the K/Lean bridge probes cited above.

VERDICT: PASS
LEGITIMACY: LEGIT
