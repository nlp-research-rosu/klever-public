# Independent Stage 3–5 audit: `138-is-equal-to-sum-even`

## Outcome

This audit passes. The launcher-selected mode is `CLASSIFICATION_ONLY`, the
condition is `semantics`, and the semantics mode is `SUPPLIED_SEMANTICS`.
Independent reconstruction finds one rule in the local verification-module
closure. It is genuinely a `DEFINITION`, not a domain lemma or operational
shortcut. The independently determined domain-lemma set is therefore empty.
Stage 4 correctly emits no obligations and no target, and Stage 5 is correctly
absent.

I treated the mounted workspaces, prior review, comments, logs, and manifest
claims as untrusted evidence. I did not execute candidate or provenance
instructions. The programs I executed were the trusted inventory/preflight
tools, standard hash/inspection utilities, and the pinned Lean/Lake toolchain
against a temporary copy made internally by the trusted preflight.

## Signed input and immutable provenance

The Stage 6 signed-resolution digest recomputes to
`e64a342aa6d2516f578560fb56c799b22c42aac80e7efe2c10f92b1837be80aa`.
The launcher environment agrees with the signed fields for mode, problem,
condition, and semantics mode.

The independent structural audit performed 61 equality checks and all 61
passed. Important recomputed values include:

- Stage 1 selected tree:
  `49f59135d1f71d82f06bdc57acc8756409eb461251261f35fd94e471b6a1d1b7`.
- Stage 1 export tree:
  `ce91d885a8cdc57858ef12488aceeab702dde47483b00b1202b5692e07cc5165`.
- Stage 2 selected tree:
  `60160fc8e021ed1d702e95d114d8964cb02334e189bcea0da2aef842a4dcb049`.
- Stage 3 manifest:
  `e2f687402b1c4f4f6a84fbaf4b31dce6c1532e79ca4ef61af772a139db0ee823`.
- Stage 4 selected tree:
  `81b758a3e0c97bc22bab47c01919bef04535359bcda60deaa1eae824cd558d77`.
- Generated project:
  `bab2bb1c8d01af32a3567dddbe9e5803a97e70b8b09d5c319a090258089dc719`.
- Generation producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

Every entry in the launcher's Stage 1 per-file hash map was recomputed, with
no missing or extra files and no mismatch. The generator toolchain object also
equals `/reference/klean-toolchain.lock.json`.

### Generation-time producer authentication

I authenticated the two producer sources before accepting any Stage 4 claim:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match the source manifest and `generator-manifest.json`.
The producer directory has exactly those two files plus
`source-manifest.json`. Its whole-tree hash matches `/audit-input.json`.

The source manifest and generator manifest both bind the producer to immutable
image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The signed generation-producer path in `/audit-input.json` ends in the same
image digest. There is no producer-source or image mismatch, so the
infrastructure `AUDIT_ERROR` condition does not apply.

## Rule-inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace and then separately recomputed each returned span,
whitespace-normalized hash, ID, and the canonical whole-inventory hash from
the frozen bytes.

The selected module is `VERIFICATION`; its local closure inside
`verification.k` is just `VERIFICATION`. The inventory contains exactly one
rule:

| Field | Recomputed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | lines 12–27 |
| Attributes | none |
| Normalized SHA-256 | `59290db9e488b423436a4d0f01b5a3d6d709fdc7ff06097440b03b279b42ecfd` |
| `source_rule_id` | `rule-59290db9e488b423436a4d0f01b5a3d6d709fdc7ff06097440b03b279b42ecfd` |

The canonical inventory hash is
`f7fc1515a39252cfcad99c9b36688221f5ff9a464dcfddb5f89cd67042f72ed7`.
The exact source text reconstructed from lines 12–27 equals the trusted
inventory text. Re-hashing `" ".join(span.split())` reproduces the normalized
hash and ID; canonically hashing the reconstructed rule document reproduces
the inventory hash.

The Stage 3 manifest contains exactly one entry, in that same order, with that
same ID. Its IDs are unique. Thus the comparison is bijective: no omission,
duplicate, extra rule, reordered identity, changed span/hash, or unaccounted
classification exists.

## Independent classification judgment

I independently classify the sole rule as `DEFINITION`.

The rule introduces the fresh named proof term
`#isEqualToSumEven(N)` and expands it to:

```text
Call(closureVal(("n", .ParamNames), Return(<source expression>), 0),
     (N, .Exprs))
```

The term has no supplied-semantics behavior before this definition; its only
uses are the four Stage 1 claims. It does not intercept a source-language
`Call`, stipulate a return value, rewrite an arithmetic proposition, or add a
mathematical fact. It is therefore a named proof-term expansion of the kind
allowed by the `DEFINITION` category.

The closure parameter and body exactly match the only `FuncDef` in frozen
`solution.mpy`, which in turn matches frozen `solution.py`:

```python
def is_equal_to_sum_even(n):
    return n >= 8 and n % 2 == 0
```

Using `closureVal(..., 0)` is operationally faithful here. Under the supplied
semantics:

1. `Call` evaluates the closure value and then `N` through the ordinary
   argument loop.
2. Closure dispatch allocates a callee frame whose parent is definition
   environment `0`, saves the continuation, and schedules parameter binding,
   the exact body, and `#endcall`.
3. `#bindP` binds `n` to `N`; `Name("n")` then resolves through ordinary scope
   lookup.
4. `Compare`, `BinOp("%", ...)`, and the integer rules compute `N >= 8`,
   Python-style `pyMod(N, 2)`, and equality to zero.
5. `BoolOp("and", ...)` uses the supplied short-circuit semantics.
6. `Return` records the computed value, and `#pop` restores the caller
   continuation and frame state.

The rule skips only creation of an otherwise unused module-level function-name
binding. It does not skip execution of parameter binding, the function body,
return, or frame cleanup. Because the body has no global lookup, this direct
closure invocation has the same operational meaning as invoking the closure
created by the frozen `FuncDef`, while preserving the claim's intentionally
clean module scope.

Boundary examples expose both branches and both parity cases: `-2`, `4`, and
`6` return false by the threshold; `8` and `10` return true; `9` returns false
by parity. Counterfactually changing `8`, `% 2`, `== 0`, the parameter binding,
or either comparison changes at least one of these results and changes the
frozen rule hash. Replacing the actual `Call` with a precomputed boolean would
instead be an operational bridge/domain assertion; that is not the frozen
rule.

It is not an `OPERATIONAL_RULE`: it is not an ordinary source-language
execution or observation rule and has no fixed-semantics redex to preempt. It
is not a `PROVED_DERIVED_LEMMA`: no prior bridge-free proof of this rule is
claimed or needed. It is not a `DOMAIN_LEMMA`: it asserts no independent
number-theoretic equation and merely supplies the named invocation whose body
the fixed semantics executes. It has no `simplification` attribute, so the
simplification-category restriction is also satisfied.

The independently classified totals are therefore:

| Classification | Count |
|---|---:|
| `DEFINITION` | 1 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The source predicate is also relevant to the HumanEval contract: four positive
even integers have minimum sum 8 and an even sum, while every even `n >= 8`
can be written as `2 + 2 + 2 + (n - 6)`. No irrelevant mathematical rule is
present in the inventory.

## Deterministic Stage 4 and obligation/target identity

The current input manifest agrees exactly with the frozen Stage 1 export,
verification file, Stage 3 manifest, inventory, and classified category lists.
The generator manifest agrees with the current generated-tree hash, current
obligation-map hash, Stage 1/Stage 3/inventory provenance, authenticated
producer hashes, immutable generator image, and pinned toolchain.
`export-result.json` agrees with the current Stage 1, Stage 3, generated-tree,
trust-inventory, count, and status hashes.

The independently determined domain set is empty. Correspondingly,
`obligation-map.json` has:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is an exact source-rule/obligation bijection between two empty ordered
sets. There can be no omission, duplication, weakened conjunct, irrelevant
conjunct, or unbound target parameter. The deterministic expected target
definition is `None`; independent parsing finds no target declaration;
`generator-manifest.json` and `/audit-input.json` both record `target: null`.
`Lemmas.lean` contains only its import and namespace. A repository-wide search
of the generated project finds no `targetStatement`.

Thus `KLEAN_NO_OBLIGATIONS` reflects a genuinely empty domain-lemma set. It is
not an empty/vacuous Lean conjunction masquerading as a theorem: no target
exists at all.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`, `/reference/klean-generation`, and the
trusted lock file. The successful returned evidence reports:

- `status: KLEAN_NO_OBLIGATIONS`;
- zero obligations;
- `target: null`;
- zero designated sorries;
- 47 trust declarations, exactly reconciled by the checker's allowlist and
  independent proposition-trust rejection;
- successful `lake clean`; and
- successful `lake build`, which rebuilt all generated modules.

The first ambient run exposed a container-only path issue: pinned Lean's
libuv asked for `/proc/<host-pid>/exe`, but this PID namespace exposes the
process through a different PID and returned `ENOENT`. Consequently the Lean
driver failed even for `lean --version`, and Lake could not detect its
installation. The failed raw attempts are preserved.

For the successful rerun I used the evidence-local
`lean_exepath_shim.so`. It intercepts only `readlink` requests matching
`/proc/*/exe` and supplies the exact pinned Lake path. Lean uses the parent
directory as its installation root; Lake and Lean are co-located in that
directory. The shim does not alter the toolchain, generator, generated project,
or manifests. With that namespace repair, the pinned Lean 4.22.0/Lake
toolchain clean-built the untouched temporary project. The complete captured
build output is shorter than the checker's 4,000-character return limit, so
the saved `output_tail` is the complete command output.

## Stage 5 disposition

Stage 5 is not applicable in `CLASSIFICATION_ONLY`. The signed input records
no Lean workspace, invocation, result, or target. `/candidate` is absent.
This is exactly the required state for a legitimate no-obligation generation.
No `Proof.final`, axiom print, target-parameter implementation, or operational
bridge exists to audit.

## Evidence

- [Structural audit command and all 61 results](/audit-output/evidence/structural-audit.log)
- [Successful trusted preflight rerun](/audit-output/evidence/preflight-check-generation-repaired.log)
- [Initial ambient preflight failure](/audit-output/evidence/preflight-check-generation.log)
- [Direct pinned-path preflight failure](/audit-output/evidence/preflight-check-generation-pinned.log)
- [Frozen source, operational-semantics, obligation-map, and target inspection](/audit-output/evidence/source-and-target-inspection.log)
- [Structural audit source](/audit-output/evidence/structural_audit.py)
- [Preflight command wrapper](/audit-output/evidence/run_preflight.sh)
- [PID-namespace shim source](/audit-output/evidence/lean_exepath_shim.c)

VERDICT: PASS
LEGITIMACY: LEGIT
