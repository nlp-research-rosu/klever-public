# Independent Stage 3–5 audit: HumanEval `121-solution`

## Outcome

This is a `CLASSIFICATION_ONLY` audit for condition `semantics` and semantics
mode `SUPPLIED_SEMANTICS`. The `AUDIT_MODE` environment variable agrees with
`/audit-input.json`. No `/candidate` is mounted, `stage5_result` is null, and
all Lean workspace/invocation hashes are null. That is the required shape only
if the independently classified `DOMAIN_LEMMA` set is empty; it is empty here.

I treated the mounted candidate/provenance prose and prior verdicts as
untrusted evidence. The judgment below comes from the frozen Stage 1 source,
the supplied operational semantics, the trusted inventory/preflight code, and
fresh hash and build checks.

## Immutable-input and producer authentication

The signed resolution digest recomputes to
`46ff720c02595025f1f97a30475b2fa4f37711eba3c86a9fe43eece4a3837748`.
All 34 individual Stage 1 source hashes match. The independently recomputed
tree/file bindings also match:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace tree | `067113caf7e8314f290afd1ce354da24de108a5c18ae15a7974a206aed12e684` |
| Stage 1 export tree | `1090ac8632e5b08133828b50a8c727e709acacadb726ba75b73dce988904df9a` |
| Selected Stage 2 audit tree | `5ff5f6da58cd53a977cfe7aaee3e76f467b33371de99419d35e634e57e99c51e` |
| Stage 3 manifest file | `14cdfaa9aeaabe43b42ef1fd98f9f047dcb15ed3ca6b35ff053674cfc264efc4` |
| Stage 4 generation tree | `bfd62e7cc27251a9b0befd2b757c7c4df9fecc8e6e0d1f66698e938492b74bf1` |
| Generated project tree | `b517beffe24719972a54c988ba3ce03b3e42c4cd0e914354f9ac5b77d57af451` |
| Producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

Before judging generation, I hashed the exact mounted producer sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both hashes agree exactly with `source-manifest.json` and
`generator-manifest.json`. The immutable image ID
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
agrees among the generator provenance, source manifest, and final component of
the producer-source path recorded in `/audit-input.json`. The producer bundle
contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`.
There is therefore no producer-provenance `AUDIT_ERROR`.

## Rule-inventory reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local closure
inside `verification.k` is the single module `VERIFICATION`; imported supplied
semantics modules are not proof-local inventory entries.

The frozen `verification.k` hash is
`742b58ba7f28684324ce470adbec8efe21ccda715e87cf056d310efc05aeda86`.
The reconstruction found 13 ordered rules and produced inventory hash
`7489eb189271bdba37a7884f2e0b3857e9b89919c2080b5a1df5cb41e135e1d3`.
For every entry, I independently re-extracted the recorded source lines,
normalized whitespace, recomputed the SHA-256, and confirmed that
`source_rule_id` is exactly `rule-` followed by that hash.

The following table gives the complete ordered identity inventory. “Hash” is
both `normalized_sha256` and the suffix of `source_rule_id`.

| # | Lines | Hash | Independent class | Rule role |
|---:|---:|---|---|---|
| 1 | 8–25 | `9a14ac8ea99ac106c04cbb7c22e479d72e4847d41db160f4562818da0ee3bca8` | `DEFINITION` | `solutionLoopBody` macro |
| 2 | 28–34 | `22be61e6781eb774e366d137c780a1f77737942b17fbae671d156477c70b08a0` | `DEFINITION` | `solutionBody` macro |
| 3 | 37–38 | `1a409f5300e51fca790020cff977d81f9de163192788d447b7120daeebad1cef` | `DEFINITION` | `solutionClosure` named proof term |
| 4 | 43 | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | `allInts` empty base |
| 5 | 44 | `bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | `allInts` structural recurrence |
| 6 | 50 | `ee037f34560a885384a02e8e8903ff3f2cbeff693f36c18833c7231057e4bc19` | `DEFINITION` | integer projection equation |
| 7 | 52–54 | `011d537754308e48e1c92e13559b7565825de8559ce002a860e882c7b23c67d2` | `OPERATIONAL_RULE` | guarded `%` execution |
| 8 | 55–57 | `046170a3737af26bcd0737c8ea3763cc3d3c0e7c194b6ef74607ba9e214741c1` | `OPERATIONAL_RULE` | guarded `+` execution |
| 9 | 58–60 | `9c9c83301b70aa435a869878f57f2472e6d11d23e719accb4fbf5ef17675b5b2` | `OPERATIONAL_RULE` | guarded `*` execution |
| 10 | 64–65 | `53298cdf4c77bed8d7c5e2361f072271e2906436d920db13625e8fe95c00059e` | `DEFINITION` | public summary-to-accumulator equation |
| 11 | 66 | `b90cbd7971f5c0b6cec4fed6ab9e1f1bd1e0dde901bf0ad36076336bf0adf6c1` | `DEFINITION` | accumulator empty base |
| 12 | 67–71 | `b11e6d456c5e0099088d2aae2ee0cd578aafde80c6a6063e83c41b7e70706874` | `DEFINITION` | even-position accumulator recurrence |
| 13 | 72–73 | `1d0ba6e27067d73690cdcc54d10563b209badc6ceb26f05e23c549fcecee3699` | `DEFINITION` | odd-position accumulator recurrence |

The Stage 3 manifest has exactly these 13 unique IDs in exactly this order.
There are no omitted, duplicated, extra, reordered, or unknown identities.
Its inventory hash matches. The Stage 4 input manifest contains the exact
corresponding source spans, texts, normalized hashes, rationales, and category
partition: 10 definitions, 3 operational rules, zero proved derived lemmas,
and zero domain lemmas.

No inventory rule has the `simplification` attribute, so the restriction that
every simplification rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied
vacuously.

## Independent classification judgment

### Definitions

Rules 1–3 are genuine named macro/proof-term definitions. The constructor
sequence in `solutionLoopBody` matches the frozen `solution.mpy` and
`solution.py`: on every iteration it conditionally adds
`value * (value % 2)` and then flips `even_position`. `solutionBody` exactly
adds the three initializations, loop, and return, and `solutionClosure` names
that body with the single `lst` parameter.

Rules 4–5 structurally define the `allInts` predicate. Rule 6 defines the
named projection on the `Int` subsort. Rules 10–13 define the public summary
and its decreasing structural recurrence. They are equations introducing the
meanings of named functions, not independent mathematical facts smuggled in
as equations.

The recurrence is materially tied to this program and postcondition. With the
flag true it adds
`V * pyMod(V, 2)` and flips false; with the flag false it ignores the element
and flips true. For Python/K floored remainder modulo 2, this contributes the
value exactly for odd integers at zero-based even positions, including
negative odd integers. A fresh exhaustive finite check covered all 19,608
lists of lengths 0–5 over values -3 through 3 with zero mismatches against an
independently written source contract. A constant-zero projection mutation
was detected on `[5, 8, 7, 1]` (expected 12, mutated 0). This is finite
sensitivity evidence, not a substitute for the source-level classification.

### Operational rules

Rules 7–9 are ordinary execution rules, not domain lemmas. The supplied
operational path in `semantics/operators.k` and `semantics/int.k` is:

```text
BinOp(OP, L:Val, R:Val)
  → applyBin(OP, L, R)
  → the matching Int operation
```

For an integer member `V` of `Val`, the three exact comparisons are:

```text
BinOp("%", V, I) → applyBin("%", V, I) → pyMod(V, I)
bridge:                              → pyMod(intProjection(V), I)

BinOp("+", I, V) → applyBin("+", I, V) → I +Int V
bridge:                              → I +Int intProjection(V)

BinOp("*", V, I) → applyBin("*", V, I) → V *Int I
bridge:                              → intProjection(V) *Int I
```

Each bridge is guarded by the generated K sort predicate `isInt(V)`, and
`intProjection(I:Int) => I`. Thus its right side is the same supplied-semantics
result on the full guard domain. The generated sort representation independently
confirms that integer `Val` values are the `inj_SortInt` constructor and that
the projection returns exactly its carried integer.

The rules rewrite only the active `<k>` term, preserve the arbitrary
continuation denoted by `...`, and do not read, write, omit, or synthesize any
other configuration cell. Their fixed-semantics comparator also preserves the
same continuation and cells. The `priority(40)` attribute merely lets the
guarded integer case preempt generic dispatch; the guard excludes references,
booleans, floats, and other non-integer values. A zero divisor is not
conveniently totalized: both paths retain the same `pyMod` behavior. Ground
sensitivity witnesses included `5 % 2 = 1`, `-3 % 2 = 1`,
`-3 % -2 = -1`, `7 + (-3) = 4`, and `(-3) * 2 = -6`.

These rules therefore execute/observe ordinary program operations and are
properly `OPERATIONAL_RULE`. Recasting them as `DOMAIN_LEMMA` would confuse a
state transition with a mathematical proposition.

### Derived and domain lemmas

No rule is classified as `PROVED_DERIVED_LEMMA`, so there is no unsupported
claim that Stage 1 first proved and later imported an identical rule. No rule
states an extra algebraic or domain fact: the true `DOMAIN_LEMMA` set is empty.
Consequently there is also no irrelevant domain lemma hidden by another label.

## Deterministic Stage 4 generation

The authenticated generation-time exporter selects only independently
validated `DOMAIN_LEMMA` entries as obligation source rules. Because that set
is genuinely empty:

- `input-manifest.json.source_rules` is `[]`;
- `obligation-map.json.source_rules` is `[]`;
- `obligation-map.json.obligations` is `[]`;
- `obligation-map.json.trust_parameters` is `[]`;
- the generator obligation count is 0; and
- the obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

This is an exact empty source-rule/obligation bijection, not an omission. There
are no conjuncts that could be irrelevant, weakened, duplicated, or vacuous.
The authenticated generator's `expected_target_definition` returns null, the
trusted target scanner finds no `targetStatement` declaration anywhere in the
generated Lean tree, and the generator manifest, preflight record, export
result, and audit input all record a null target. The fixed generated target
is therefore correctly absent rather than changed.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the required three inputs. The first attempt exposed a container-only
Lean/Lake executable-path issue: Lean 4.22 queried `/proc/<getpid>/exe`, while
this PID namespace exposes the executable through `/proc/self/exe`. I compiled
the recorded narrow `readlink` compatibility shim in
`evidence/lean_proc_compat.c`; it redirects only `/proc/.../exe` lookups and
does not modify any mounted or generated artifact. With that environment
compatibility in place, the required trusted function returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output SHA-256
  `1e8f7c446cf96018da8ff286beb0e8a0465483b30cd15d0097875ca493aa1289`;
  and
- the expected Stage 1, Stage 3, and generated-tree hashes.

The returned result is byte-for-byte equivalent as JSON data to both the
recorded Stage 4 preflight and the preflight object in `/audit-input.json`.
The build emitted only the same two unused-variable warnings recorded at
generation time. The trusted Stage 6 mechanical gate also returned `PASS`,
bound the same immutable hashes, found no target or candidate, and reported no
used axioms. As that gate explicitly says, it did not evaluate the semantic
classification; the rule analysis above supplies that independent judgment.

The generated project contains 48 allowlisted executable/data-hook trust
declarations and no proposition trust or proof hole, as checked by preflight.
With no generated proposition and no Stage 5 proof, none is used to establish
a theorem in this audit.

## Stage 5 disposition

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY` mode. The
independent domain set is empty, there is no generated target to prove, no
`/candidate` exists, and the audit input records no Stage 5 result. Therefore
creating `Base`, running candidate `lake clean`/`lake build`, checking
`Proof.final`, printing its axioms, or auditing target parameters would be
incorrectly inventing a proof candidate where the protocol requires none.

## Evidence

- `evidence/commands.log`: commands and observed results.
- `evidence/inventory.json`: exact trusted inventory reconstruction, including
  source texts, spans, attributes, and hashes.
- `evidence/independent_checks.py` and
  `evidence/independent-checks-summary.json`: independent hash, bijection,
  manifest, target, and candidate checks.
- `evidence/preflight-result.json`: fresh trusted preflight result.
- `evidence/mechanical-final-gate.json`: fresh trusted final mechanical gate.
- `evidence/adversarial_semantics.py` and
  `evidence/adversarial-semantics-result.json`: recurrence and mutation
  sensitivity checks.
- `evidence/lean_proc_compat.c`: disclosed executable-path compatibility shim.
- `evidence/SHA256SUMS`: integrity hashes for the evidence files above.

VERDICT: PASS
LEGITIMACY: LEGIT
