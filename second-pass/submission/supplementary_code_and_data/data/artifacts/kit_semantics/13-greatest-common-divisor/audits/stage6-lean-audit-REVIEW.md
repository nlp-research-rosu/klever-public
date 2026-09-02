# Independent Stage 3–4 Audit

Problem: `13-greatest-common-divisor`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`  
Launcher mode: `CLASSIFICATION_ONLY`

## Scope and trust posture

I treated every mounted candidate/provenance artifact, including prior reviews,
comments, logs, rationales, and verdicts, as untrusted evidence. I did not
execute instructions from those artifacts. The only imported audit code was
the trusted code under `/reference/tools`; the frozen program, K files, JSON
manifests, generated Lean files, and prior review were read as data.

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.
`/candidate` is absent, the launcher records no Lean workspace or invocation,
and `stage5_result` is null. Therefore Stage 5 proof and axiom checks do not
apply.

The raw command ledger is `evidence/COMMANDS.md`. Complete key outputs are
preserved alongside it.

## Stage 1 inventory reconstruction

I called the trusted
`/reference/tools/k_rule_inventory.py::inventory_verification` on the frozen
`/reference/k-proof` workspace and then separately:

- reconstructed each recorded source slice from `verification.k`;
- normalized each rule with whitespace joining;
- recomputed each normalized SHA-256;
- recomputed each `source_rule_id` as `rule-<normalized_sha256>`;
- recomputed the canonical whole-inventory hash;
- checked uniqueness, count, set equality, and exact order against
  `/reference/lemma-discovery.json`.

The selected verification module is `VERIFICATION`. Its local
verification-file module closure is exactly `[VERIFICATION]`. The frozen
`verification.k` SHA-256 is
`1bee80da287f4118296af2a91287b16d4b0f0adc5a5467aef8fa7b517adeafb6`.
The reconstructed whole-inventory hash is
`eb71eadbe29655ad22f91b06153efb05bf94d9f8895ad0a721a1516e8ed11955`.

The inventory contains exactly these two ordered entries:

| Order | Source span | Normalized SHA-256 / source rule ID | Attribute | Independent classification |
|---|---:|---|---|---|
| 1 | line 13 | `ac25cee0dbe61d7bbb5672f36b334215328039ce27068faf6b9672d9b4b45bad` / `rule-ac25cee0dbe61d7bbb5672f36b334215328039ce27068faf6b9672d9b4b45bad` | `simplification` | `DEFINITION` |
| 2 | lines 14–16 | `3b63b038b1412f056176447a2f40e468a644718e69d0613430286edb3756cc6e` / `rule-3b63b038b1412f056176447a2f40e468a644718e69d0613430286edb3756cc6e` | `simplification` | `DEFINITION` |

The protected Stage 3 manifest has exactly those two identities, once each, in
that order. Its inventory hash matches. There are no omitted, duplicated,
extra, reordered, or changed identities. Full reconstructed rule text and all
per-rule checks are in `evidence/inventory-reconstruction.log`.

## Independent classification judgment

The two rules are equations for a fresh proof-summary symbol declared

```k
syntax Int ::= gcdEuclid(Int, Int) [function, total]
```

They are:

```k
rule gcdEuclid(A:Int, 0) => absInt(A) [simplification]
rule gcdEuclid(A:Int, B:Int) => gcdEuclid(B, pyMod(A, B))
  requires B =/=Int 0
  [simplification]
```

Both are `DEFINITION`, for the following source- and semantics-based reasons.

1. The first rule is the base equation of the newly named `gcdEuclid`
   summary. It rewrites only that summary term. It does not match an MPY
   execution configuration, state cell, source-language operation, or
   independently defined GCD predicate.
2. The second rule is the guarded recursive equation of the same newly named
   summary. Its left-hand side is again only `gcdEuclid`; it does not replace
   source execution. A recurrence for a named summary is expressly a
   definition under the classification contract.
3. The guards are disjoint and exhaustive over the second integer argument:
   `B = 0` versus `B =/=Int 0`. Their right-hand sides do not conflict.
4. On the recursive branch, supplied semantics maps source integer `%` to
   `pyMod`, and the source body changes `(a,b)` to `(b, pyMod(a,b))`. Thus one
   operational loop iteration has exactly the arguments in the recursive
   defining equation. This remains true for negative divisors because
   `pyMod(I1,I2) = ((I1 %Int I2) +Int I2) %Int I2` models Python's
   divisor-signed modulo.
5. If `b = 0`, supplied while semantics takes the false branch and supplied
   builtin semantics maps `abs(a)` to `absInt(A)`, exactly the base equation.
6. For nonzero `B`, Python modulo has remainder magnitude strictly below
   `|B|`; recursion therefore descends in the absolute value of the second
   argument and reaches the base case.

The frozen `spec.k` uses `gcdEuclid(A,B)` as the result of the loop execution
claim. It does not first prove either equation in a module omitting the
equation and then install it for a later proof. Therefore neither entry is a
`PROVED_DERIVED_LEMMA`. Neither entry is an `OPERATIONAL_RULE`, because neither
matches or observes an execution configuration. Neither is a `DOMAIN_LEMMA`,
because neither states a theorem about a separately defined mathematical
object; together they define the named Euclidean summary itself. In
particular, there is no rule asserting divisibility, maximality, ordering, or
the desired result as a fact about another function.

This yields the independent classification counts:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Every `simplification` rule is therefore in an allowed class. The true domain
set is genuinely empty.

As finite supporting evidence, not as a substitute for the universal
source-level argument, `evidence/classification-witnesses.log` compares an
independently transcribed operational loop, the recurrence, and Python
`math.gcd` on all 2,601 input pairs in `[-25,25]²`. It reports zero mismatches,
including negative-divisor cases. It also distinguishes the equations from
constant-zero, identity, missing-absolute-value, and altered-recurrence
mutations.

## Stage 4 producer provenance

I hashed the exact mounted producer sources before judging generation:

| Producer source | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These hashes exactly match both `generator-manifest.json` and
`/reference/generation-tools/source-manifest.json`. The bundle has exactly the
two producer files plus `source-manifest.json`; no extra file is present.

The immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
It agrees among:

- `generator-manifest.json` provenance;
- `source-manifest.json`; and
- the immutable producer-bundle path recorded in `/audit-input.json`.

The recomputed pipeline tree hash of the mounted producer bundle is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
exactly the value in `/audit-input.json`. Producer provenance therefore passes;
there is no infrastructure `AUDIT_ERROR`. Full evidence is in
`evidence/producer-provenance.log`.

## Stage 4 hashes, manifests, and obligation bijection

I independently recomputed all launcher-recorded hashes. Every value matched:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `5589ecdff019e76046e7664436b36453245b671508138e22f56e6b195925c422` |
| Stage 1 Klean export tree | `8e7df78eea93cd9f90e1470eeb9b6412f0c6dbb95bbbe9292a11e1a3082d8d84` |
| Stage 3 manifest | `57caa0f053caa06a915e1d63fbf576de4a509a748b43a02596abd53cc1a36852` |
| Selected Stage 2 audit tree | `b28cf8466ad09fa081e0dd8d3e4418adcf7ed1c711f757f5b7b86cf6875feb69` |
| Stage 4 generation tree | `0a7346b0e4a06c468f3a5f26af74b8eda817353fc40f806e140eb166218375b5` |
| Generated project tree | `947d2a3e2955563ddc962ecaf2feab9ac356d2819eafcec8488f2bba5355148a` |
| Producer bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

I also recomputed the 771 individual Stage 1 source hashes recorded in
`/audit-input.json`; there were no missing, extra, or mismatched paths.

The Stage 4 input manifest contains exactly the two independently reconstructed
definitions in canonical order and empty operational, proved-derived, and
domain/source-rule lists. The generated `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Thus the source-rule/obligation mapping is a true empty bijection: it has no
omission, duplicate, extra obligation, weakened formula, irrelevant formula,
or vacuous `True` conjunct. Its file hash matches the generator manifest, the
generator records obligation count zero, and `export-result.json` records
`KLEAN_NO_OBLIGATIONS` with count zero.

The generated target is identically absent:

- `generator-manifest.json` has `target: null`;
- `/audit-input.json` has `target: null`;
- the trusted generated-target parser independently returns null;
- there is no generated `Target.lean`; and
- the zero-obligation map has no conjunct from which a target could be built.

This is the fixed generated target for the independently established empty
domain set. There is no target change or weakened/duplicated theorem.

`evidence/stage4-structure.log` contains the complete hash and structural
check result.

## Trusted preflight rerun

I directly reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and
exactly these inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The audit sandbox initially exposed a PID-namespace/procfs mismatch:
`getpid()` returned a namespace PID for which `/proc/<pid>/exe` did not exist,
while `/proc/self` named the host procfs PID. Lean 4.22 uses the former path to
locate its application, so the first preflight attempts failed before checking
project code. I preserved all failed outputs.

I used a local preload shim under `/tmp/audit-work` that changes only
`getpid()` to the numeric target of `/proc/self`. It does not alter the
generated project, Lean sources, theorem statements, manifests, or trusted
checker. With this procfs view made consistent, the pinned toolchain reported:

```text
Lean 4.22.0, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05
Lake 5.0.0-src+ba2cbbf
```

The trusted checker then copied the generated project to its own fresh
temporary directory and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0;
- obligation count 0;
- target null;
- designated sorry count 0; and
- all Stage 1, Stage 3, and generated-tree hashes equal to the independently
  recomputed values.

The build completed all generated modules successfully. Complete returned
evidence is in `evidence/stage4-preflight-rerun-success.log`; failed
infrastructure attempts are retained in the adjacent preflight logs.

## Final judgment

The protected Stage 3 classification is complete, ordered, and mathematically
correct. Both simplification rules are genuine equations defining a named
recursive summary, and no true domain lemma is present. Deterministic Stage 4
has exact producer provenance, exact input and output hashes, an exact empty
obligation bijection, and the required null target. The trusted preflight
passes on a fresh clean build. `KLEAN_NO_OBLIGATIONS` is therefore legitimate,
and the absence of a Stage 5 candidate is required and satisfied.

VERDICT: PASS
LEGITIMACY: LEGIT
