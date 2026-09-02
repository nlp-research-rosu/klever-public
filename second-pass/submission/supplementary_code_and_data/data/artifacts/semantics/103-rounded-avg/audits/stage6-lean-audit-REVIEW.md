# Independent audit: `103-rounded-avg`

## Scope and conclusion

This audit covers Stage 3 lemma classification and deterministic Stage 4
generation for condition `semantics` in `SUPPLIED_SEMANTICS` mode. The launcher
records `AUDIT_MODE=CLASSIFICATION_ONLY`; `/audit-input.json` agrees. Stage 4
is selected as `KLEAN_NO_OBLIGATIONS`, so there is no Stage 5 Lean candidate
and no proof-bearing theorem to audit.

I treated the mounted Stage 1/2/3/4 artifacts, logs, prior review, comments, and
classifications as untrusted evidence. I did not rely on the selected Stage 2
verdict or the prior Stage 3 classification. I used the trusted inventory and
preflight implementations under `/reference/tools` to reconstruct mechanical
facts, and made the classification and relevance judgments directly from the
frozen K source, source solution, postcondition, and supplied operational
semantics.

The result is legitimate. The local verification closure contains exactly two
rules. Both are structural definitions of named proof terms, neither is a
domain lemma, and therefore the true domain-lemma set is empty. Stage 4
preserves that empty set bijectively, generates no conjunct and no target, and
correctly has no Stage 5 candidate.

## Launcher and provenance

The signed Stage 6 envelope validates with resolved-input digest
`7819050157227845ecea5785b4e22055974ac5ff599534d35cf4564403eabb10`.
The launcher mode, condition, problem, and semantics mode are:

- mode: `CLASSIFICATION_ONLY`
- condition: `semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- problem: `103-rounded-avg`

Every hash recorded by `/audit-input.json` was independently recomputed with
the corresponding trusted hash algorithm:

| Binding | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 artifact tree | `44d6c4faa59f45ac201313c4d4f2a3960743ef4c7e1d2b728cce33ccbbd7f40c` |
| Stage 1 deterministic-export tree | `422f7ab6327cf88116acf053266a76807ce8037c1d555c7942348900519da584` |
| selected Stage 2 audit tree | `121ccbb6c3658e8139b63e34875709679fc967422705821e6c758cab3d9b3627` |
| Stage 3 manifest file | `b93f3c896f4e81985d78090036a74d53bc1ebe00eab58a0ee448238ccec8cda6` |
| selected Stage 4 generation tree | `abd4879944040cf0d236fbddf7b7099688c38bbbe7981182f34c38c8b7d71165` |
| Stage 4 producer bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| generated Lean project tree | `9213cc27af9ed382d56bbb56e7a13ea1c70e93cfd5bf94c3b79c896cd32c0861` |

The complete Stage 1 regular-file set and every per-file source hash also match
the launcher record. The selected Stage 2 and Stage 4 artifact hashes match
their selection manifests. Both Stage 5 hashes are correctly `null`.

## Generation-producer authentication

I hashed the two mounted producer files before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Those values match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus `source-manifest.json`; its tree hash matches `/audit-input.json`.
The generator image binding is identical in all available locations:

`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`

Specifically, it matches `generator-manifest.json`, `source-manifest.json`, and
the image-key suffix of the immutable producer path recorded in
`/audit-input.json`. There is no missing or mismatched producer source, so no
infrastructure `AUDIT_ERROR` applies.

## Inventory reconstruction

I invoked `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. The selected main module
is `ROUNDED-AVG-VERIFICATION`. Its local verification-module closure contains
only that module; `MPY` is supplied by the required external semantics rather
than another local module in `verification.k`.

The frozen `verification.k` hash is
`f592076475187c76e15fdfa9db22d4ec6c44cbf40611a0f4322dfc9c8d9dac34`.
The canonical inventory hash is
`54046ca4266a466afc0472ebf70f3a40dd5ae3971a2d8e6491d0797e40632601`.

The complete reconstructed inventory is:

| Order | Span | Normalized SHA-256 / source rule ID | Attributes | Independent class |
|---:|---|---|---|---|
| 1 | lines 10–25 | `07b2e76171363735048d516894c0106df978020141671339aaa271a5d5e0d8e7` / `rule-07b2e76171363735048d516894c0106df978020141671339aaa271a5d5e0d8e7` | none | `DEFINITION` |
| 2 | lines 30–32 | `5e130f83335a10b2992b3283bceb5cbf4e9d208c0b150ab3918d09173e3f7ad7` / `rule-5e130f83335a10b2992b3283bceb5cbf4e9d208c0b150ab3918d09173e3f7ad7` | none | `DEFINITION` |

For each entry I independently extracted the recorded source span from
`verification.k`, normalized whitespace, recomputed its SHA-256, and confirmed
that `source_rule_id` is `rule-` followed by that digest. I also recomputed the
canonical whole-inventory digest.

The Stage 3 manifest has exactly two entries. Its ordered identity list equals
the canonical ordered list. Counts, uniqueness, identity set, classifications,
and inventory hash all match. Thus there are no omissions, duplicates, extra
rules, reordered identities, changed hashes, or unaccounted classifications.

## Independent classification judgment

### `roundedAvgBody` — `DEFINITION`

The declaration is `syntax Stmts ::= "roundedAvgBody" [function, total]`. Its
only rule expands that ground name to the translated statement sequence:

1. compare `n > m` and return `-1` on the inverted interval;
2. assign `total = n + m`;
3. assign `average = total // 2`;
4. implement the odd-total/odd-lower-neighbor tie-to-even adjustment; and
5. call `bin(average)` and return it.

That sequence agrees statement-for-statement with `solution.mpy` and
`solution.py`. The rule has no result theorem, arithmetic conclusion,
precondition, or postcondition. It is a ground structural macro naming the
source body for later reachability claims. This is exactly a named proof-term
definition, not a domain lemma and not an ordinary execution rule.

### `roundedAvgCall(N, M)` — `DEFINITION`

The declaration is
`syntax Expr ::= roundedAvgCall(Int, Int) [function, total]`. Its rule expands
the named entry-point expression to:

`Call(closureVal(("n", "m", .ParamNames), roundedAvgBody, 0), (N, M, .Exprs))`

The two arguments are carried unchanged, the parameter order matches the
source function, the body is the exact structural term above, and parent scope
`0` matches the module scope in the initial claim configuration. It is a
parameterized proof-harness constructor.

Crucially, it does not replace the function result with an oracle or summary.
After this definitional expansion, the supplied operational semantics still
performs the ordinary call route: callee and argument evaluation, closure
dispatch, frame allocation, parameter binding, body execution, builtin `bin`,
return, and frame pop. Counterfactually changing the body or either argument
changes the constructed invocation and therefore the subsequent execution; the
definition does not hard-code a convenient result. It is not an operational
bridge and asserts no mathematical fact.

### Exhaustiveness and policy

There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`
entries. Nothing claims the stricter derived-lemma status, so no Stage 1
prove-then-use history is required. Neither rule has a `simplification`
attribute; the rule-policy condition is satisfied. No parity, averaging,
rounding, binary-conversion, or postcondition fact is embedded in
`verification.k`. The independently established domain set is therefore
genuinely empty, not merely irrelevant or mislabeled.

## Deterministic Stage 4 audit

The authenticated generation-time producer selects only
`validated["domain_lemmas"]`, preserves their order and provenance, requires
generated obligation IDs to equal the expected ordered IDs, and returns no
target definition when the obligation list is empty. That behavior agrees with
the mounted artifacts and the trusted current preflight.

The exact Stage 3/Stage 4 mapping is:

| Set | Ordered source rule IDs |
|---|---|
| independently classified domain lemmas | `[]` |
| validated Stage 3 domain lemmas | `[]` |
| `input-manifest.json` source rules | `[]` |
| `obligation-map.json` source rules | `[]` |
| `obligation-map.json` obligations | `[]` |
| `obligation-map.json` trust parameters | `[]` |

All recorded obligation counts are zero, and the empty obligation list is
unique and bijective with the empty true domain set. There are no omitted,
duplicated, irrelevant, weakened, or vacuous conjuncts. In particular, the
generator did not turn the empty conjunction into a theorem of `True`.

The fixed generated target is absence of a target:

- expected target definition from `obligation-map.json`: `null`
- mechanically located generated target: `null`
- generator manifest target: `null`
- preflight target: `null`
- audit-input target: `null`

`Klean103RoundedAvg/Lemmas.lean` contains only its namespace and comments; it
has no `targetStatement`. No candidate exists at `/candidate`. This is the
required shape for a legitimate `KLEAN_NO_OBLIGATIONS` generation.

## Independent preflight rerun

I reran `tools.klean_preflight.check_generation` with the required three
inputs and `PYTHONPATH=/reference`. The sandbox initially exposed a toolchain
infrastructure defect: Lean 4.22 obtains its application path with
`readlink("/proc/<getpid()>/exe")`, while this PID namespace exposes
`/proc/self/exe` but not `/proc/<namespace-pid>/exe`. The first unchanged
preflight therefore reached `lake clean` and failed with:

`error: could not detect the configuration of the Lake installation`

I diagnosed that behavior directly and used the recorded
`proc-self-readlink-shim.c`, which rewrites only the exact
`/proc/<digits>/exe` readlink shape to `/proc/self/exe`. It does not modify the
generated project, Lean source, build arguments, declarations, or proof terms.
With that namespace compatibility shim preloaded, the unchanged trusted
preflight command completed.

Returned evidence:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0
- `lake build`: exit 0
- generated tree:
  `9213cc27af9ed382d56bbb56e7a13ea1c70e93cfd5bf94c3b79c896cd32c0861`
- Stage 1 export:
  `422f7ab6327cf88116acf053266a76807ce8037c1d555c7942348900519da584`
- Stage 3 manifest:
  `b93f3c896f4e81985d78090036a74d53bc1ebe00eab58a0ee448238ccec8cda6`
- obligations: 0
- target: `null`
- generated trust declarations: 47
- designated sorries: 0

The generated trust declarations are non-propositional Klean boundary
constants admitted by the mechanical policy. Because there is no generated
target and no Stage 5 proof, they support no theorem under review and cannot
hide a missing domain obligation.

## Stage 5 disposition

Stage 5 is not applicable. The signed launcher mode is
`CLASSIFICATION_ONLY`, the true domain set is empty, the generated target is
absent, all Stage 5 fields and hashes are `null`, and `/candidate` is absent.
Accordingly there is no `Proof.final`, axiom printout, target parameter,
candidate definition, or operational bridge to inspect. Running proof-mode
checks would contradict the required no-obligation workflow rather than add
assurance.

## Evidence index

Key reproducible artifacts under `/audit-output/evidence/` are:

- `01-producer-authentication-inputs.typescript`: producer hashes and manifests
- `03-frozen-source-and-stage3.typescript`: numbered K source, spec, solution, and Stage 3 manifest
- `inventory-reconstruction.json`: trusted canonical inventory
- `stage3-contract-validation.json`: trusted Stage 3 boundary reconstruction
- `inventory-bijection-reconciliation.json`: explicit order, span, hash, identity, and class checks
- `06-operational-semantics-excerpts.typescript`: relevant call, binding, control, arithmetic, and builtin semantics
- `provenance-reconciliation.json`: all launcher, tree, file, manifest, selection, and image bindings
- `20-authenticated-producer-logic.typescript`: authenticated generation-time mapping and target logic
- `proc-self-readlink-shim.c`: narrow PID-namespace compatibility shim
- `15-proc-shim-toolchain-test.typescript`: pinned Lean version plus clean/build validation
- `16-rerun-klean-preflight-with-proc-shim.typescript`: exact successful preflight rerun
- `preflight-returned-evidence.json`: returned preflight evidence
- `no-obligations-reconciliation.json`: exact empty-set bijection and target-absence checks

VERDICT: PASS
LEGITIMACY: LEGIT
