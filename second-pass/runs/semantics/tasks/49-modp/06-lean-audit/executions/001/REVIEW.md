# Independent Stage 3–5 Audit: HumanEval `49-modp`

## Scope and result

I audited problem `49-modp`, condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed resolution in
`/audit-input.json` select `CLASSIFICATION_ONLY`. The selected Stage 4 status
is `KLEAN_NO_OBLIGATIONS`; there is no Stage 5 candidate.

The classification is correct. The local verification-module closure contains
three rules, all of which are definitions. There is no true domain lemma, so
the empty Stage 4 obligation set and absent target are legitimate.

I treated the mounted reviews, logs, rationales, and prior verdicts only as
evidence. The conclusion below comes from the frozen sources, trusted
inventory/preflight code, independently recomputed hashes, and fresh tool runs.

## Producer and input integrity

The generation-time producer bundle has exactly the expected three files:
`klean_export.py`, `klean.py`, and `source-manifest.json`. There are no extra
or linked entries.

The producer bindings agree across the mounted sources, source manifest,
generator manifest, and signed audit resolution:

| Item | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |
| Producer bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| Immutable generator image | `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000` |

The image ID is identical in `generator-manifest.json` and
`source-manifest.json`; the signed producer-source path in `/audit-input.json`
ends in the same digest. This clears the mandatory producer-source
infrastructure gate.

The signed resolution digest recomputes to
`962e6f10bed2c40cc78c970e48381fd25a4632072532b736b9cf188800de231f`.
Every listed Stage 1 source hash also recomputes exactly, including
`verification.k` at
`9ee9a4a9d20147a93a986331429546e8c2009d15b5ea29b39577bd0d226ccc4c`.
The two deliberately different Stage 1 tree encodings both match their
recorded fields:

- pipeline tree:
  `c8b221ea53d6854e900194f1b571f12caf5970156888da0d519629b7b07cc007`;
- frozen Klean export tree:
  `ca1d4ac7178b89cc6a687e6d727262f1bf29e096d52e2ac93bda7b7c0b565784`.

## Canonical inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace. I also independently sliced the reported source
lines, normalized whitespace, recomputed each rule hash and `source_rule_id`,
and recomputed the canonical JSON inventory hash.

The selected local closure is exactly module `MODP-VERIFICATION`. It contains
these three rules in source order:

| Span | Rule | Normalized SHA-256 / identity | Independent class |
|---|---|---|---|
| 10–12 | `modpBody => ...` | `71d349ffafcb30fd76f8fe497ddc3bd83e9c8f32d2e73927d650e4dc1e713860` | `DEFINITION` |
| 15–17 | `modpProgram => ...` | `642fa0e1d269068ee1ff23a4190cc20e8dd97d36c91e0e7fdd0f6fc2160ca730` | `DEFINITION` |
| 23–24 | `specModp(N,P) => pyMod(2 ^Int N,P)` | `979f0d2fa1ec906f8e5bf589b74d8f25cd25fe0ce31c6c16227b18246e343ea5` | `DEFINITION` |

Each `source_rule_id` is `rule-` followed by the displayed hash. The whole
inventory hash is
`8e151024b7f0e14bad413ae3030acd7ac6d27d749bcc138a8712ed54ada3e191`.

The protected Stage 3 manifest has exactly those three identities in the same
order. There are no omissions, extras, duplicates, reordered identities,
changed spans, or changed hashes. Trusted
`lemma_discovery_contract.validate_trust_boundary` also accepted the exact
bijection. All three inventory attribute lists are empty, so there is no
misclassified `simplification` rule.

## Independent classification judgment

### `modpBody`

This rule gives a name to the exact translated statement sequence:

`Expr(Str(...))` followed by
`Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))`.

The sequence matches `solution.mpy` exactly. It is a structural, macro-like
definition. It has no configuration cells and neither intercepts nor replaces
the supplied operational rules.

### `modpProgram`

This rule gives a name to the exact
`Module(FuncDef("modp", Params("n", "p"), modpBody))` term. It is likewise a
structural definition. Loading the module, installing the closure, evaluating
the callee and arguments, binding both parameters, executing the body,
returning, popping the frame, and restoring state are still performed by the
supplied semantics.

### `specModp`

This is a named postcondition summary:

```text
specModp(N, P) = pyMod(2 ^Int N, P)
when N >= 0 and P > 0
```

It is a `DEFINITION`, not a domain lemma. The classification contract
explicitly admits named summaries and proof terms as definitions, and this
rule asserts no independent arithmetic fact. Its right-hand side is exactly
the operational result:

- `BinOp("**", I1, I2)` dispatches to `I1 ^Int I2` under `I2 >= 0`;
- `BinOp("%", I1, I2)` dispatches to `pyMod(I1, I2)`;
- `pyMod(I1, I2)` is the supplied floored-remainder equation.

The claim uses the same `N >= 0` guard needed by exponentiation and strengthens
the modulus side to `P > 0`, matching the source contract and excluding
division by zero. Thus `specModp` faithfully names the value produced by the
source expression `return (2 ** n) % p`.

None of the three rules is an ordinary execution/observation rule, so no
`OPERATIONAL_RULE` is present. Stage 1 does not first prove and later import
any one of them from a module lacking it, so no
`PROVED_DERIVED_LEMMA` is present. None states a separate arithmetic theorem,
so no `DOMAIN_LEMMA` is present.

## Operational and non-vacuity evidence

I built the supplied semantics with K 7.1.293 in a fresh directory rather than
running the mounted `prove.sh`. The original concrete examples and additional
boundary/adversarial cases `(0,1)`, `(1,1)`, `(4,3)`, `(5,7)`, and `(10,17)`
all terminated with empty computation, no exception, and semantic exit code
zero. A deliberately false assertion that `modp(5,7) = 5` produced
`AssertionError` and semantic exit code one.

I separately compiled the frozen verification definition and ran `kprove` on
the frozen claim; it exited zero with `#Top`. To test result sensitivity, I
changed only the postcondition to `specModp(N,P) + 1`. That proof exited one
with `WarnStuckClaimState`. Its residual explicitly contained the impossible
equality between the computed remainder and that same remainder plus one.
This demonstrates a satisfiable, result-constraining claim rather than a
vacuous closure.

These runs supplement the source-level classification; finite examples do not
replace the exact operational correspondence above.

## Deterministic Stage 4 audit

The verified generation-time source selects only validated
`domain_lemmas` for `source_rules` and generated obligations. It returns no
target when the obligation list is empty and rejects any stray
`targetStatement` in that case. Since the independently reconstructed domain
set is empty, the correct generated mapping is:

```json
{
  "source_rules": [],
  "obligations": [],
  "trust_parameters": []
}
```

That is exactly the mounted `obligation-map.json`. The source-rule/obligation
bijection is therefore the unique empty bijection: no omissions, extras,
duplicates, weakened obligations, irrelevant obligations, or vacuous
conjuncts exist.

Independently recomputed Stage 4 bindings are:

| Item | SHA-256 |
|---|---|
| Stage 3 manifest | `553885232b2b557bd618ac8719cefbf0e04f616ed3d270323b469acee2ca5c17` |
| Generated project tree | `69711b36fbf78c6186252f0365829929258bba625b2df132bb2728a40409ce27` |
| Selected generation tree | `48c7ae1d6b8d095c4a3208deb3fea1dd3ce369f0acb16ba82641fbe8a22b7175` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `d91909d734e1fdd5ad6b4fb04bb70e6269c95a06d41bda5804f084646da7fcac` |
| Selected Stage 2 audit tree | `3fb14b35fdefe178ef6020b0512208b24cde2f77457d1abc689c4a9ff24a3f1e` |

These values agree across `/audit-input.json`, the input manifest, generator
manifest, export result, preflight record, selection records, and the mounted
trees. The generator toolchain object is identical to
`klean-toolchain.lock.json`.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three inputs. Its fresh `lake clean`
and `lake build` both exited zero, and the returned preflight evidence matches
the recorded preflight, including:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count zero;
- target `null`;
- generated-tree and provenance hashes;
- zero designated sorries;
- 49 structurally inventoried generated trust declarations.

The build completed all generated modules successfully. The generated trust
declarations are executable Klean boundary constants, not a proposition or
proof of a target; with no target they cannot conceal a Stage 5 theorem.

The audit container exposes PIDs from one namespace but mounts `/proc` from
another. Lean 4.22 queries `/proc/<getpid()>/exe`, which is absent here even
though `/proc/self/exe` works. I recorded this failure and used a narrow
`LD_PRELOAD` compatibility shim that redirects only numeric
`/proc/<pid>/exe` reads to `/proc/self/exe`. With that environment repair,
Lean reports commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, Lake reports
Lean 4.22.0, and the unmodified trusted preflight and generated project build
successfully. The shim does not alter files, project inputs, Lean terms, or
build outputs.

## Target identity and Stage 5

The independently parsed target is `null`. It is also `null` in the generator
manifest, preflight record, and signed audit input. There is no generated
target module or `targetStatement` declaration. `/candidate` is absent, and
the signed Lean workspace, invocation, hashes, and Stage 5 result are all
`null`.

Therefore Stage 5 clean-build, `Proof.final`, axiom accounting, and
operational-bridge parameter checks are not merely skipped for convenience:
they are inapplicable and forbidden by the legitimate
`KLEAN_NO_OBLIGATIONS`/`CLASSIFICATION_ONLY` branch.

## Evidence

Raw commands, complete outputs, authored mutations, and integrity checks are
under `/audit-output/evidence/`:

- `01_integrity.log`: producer files, image identity, and aggregate trees;
- `02_inventory.log`: numbered source, canonical inventory, manual
  span/hash reconstruction, ordered bijection, and all Stage 1 source hashes;
- `03_semantic.log`: fresh K builds, concrete/adversarial execution, and
  successful frozen `kprove`;
- `04_preflight.log`: complete required preflight build output, returned
  evidence, all manifest/tree/hash bindings, empty bijection, and null target;
- `05_vacuity.log`: rejected `+1` symbolic postcondition mutation and residual;
- `06_classification.log`: source, relevant operational rules,
  generation-time selection logic, and per-rule independent judgments;
- `07_toolchain_compat.log`: PID-namespace failure and exact repaired
  Lean/Lake identities.

VERDICT: PASS
LEGITIMACY: LEGIT
