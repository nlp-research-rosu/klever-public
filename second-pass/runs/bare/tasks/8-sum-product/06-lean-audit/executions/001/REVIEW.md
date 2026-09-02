# Independent Stage 3–4 Audit: `8-sum-product`, `bare`, `GENERATED_SEMANTICS`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, and
`/audit-input.json` independently records the same mode. `/candidate` is
absent. Stage 5 proof, axiom, and operational-parameter checks therefore do not
apply.

I independently reconstructed the Stage 1 rule inventory, reclassified its
only rule from the frozen K source and semantics, reran the required trusted
preflight, checked the signed input bindings, and audited the zero-obligation
Stage 4 output. The Stage 3 classification and the mathematical
`KLEAN_NO_OBLIGATIONS` decision are legitimate.

I do not issue a clean PASS because two generator-code hashes recorded in
`generator-manifest.json` cannot be reconciled with the trusted mounted tool
sources. This is a provenance concern, not a mathematical or
operational-bridge failure in this classification-only case.

## Evidence handling

All mounted candidate and provenance content was treated as untrusted evidence.
No mounted script such as `prove.sh`, no Python solution, and no instruction
from a mounted review or log was executed. Trusted code under
`/reference/tools` was used only for the specified inventory, preflight, and
mechanical gates.

Raw commands and outputs are under `/audit-output/evidence/`. Principal files
are:

- `07-frozen-stage1-sources.txt`: frozen K semantics, specification, source
  solution, prompt, and hashes;
- `08-inventory-and-stage3-bijection.txt`,
  `reconstructed-inventory.json`, and `validated-stage3.json`: trusted
  inventory reconstruction and exact Stage 3 boundary validation;
- `25-preflight-rerun-success.txt` and `preflight-returned.json`: exact returned
  evidence from `tools.klean_preflight.check_generation`;
- `26-stage4-manifests-and-generated-source.txt` and
  `27-zero-obligation-and-target-inspection.txt`: manifests, obligation map,
  generated source, and target search;
- `independent_hash_check.py`, `28-independent-hash-check.txt`, and
  `independent-hash-results.json`: separately implemented source, tree,
  canonical-JSON, inventory, bijection, and target checks;
- `29-generator-code-hash-provenance.txt` and
  `30-generator-code-hash-resolution.txt`: generator-source hash discrepancy;
- `31-trusted-final-gate.txt` and `final-gate-returned.json`: signed-input
  mechanical gate.

The initial preflight attempts are also retained. Lean failed before project
elaboration because the container exposes host PIDs in `/proc` while processes
observe namespace PIDs. Evidence `19-proc-access-diagnosis.txt` through
`24-proc-exe-shim-validation.txt` isolates that issue. I used a narrow
`LD_PRELOAD` shim whose source is preserved as
`/tmp/audit-work/proc_exe_shim.c`: only an `ENOENT` result for a numeric
`/proc/<pid>/exe` readlink is retried as `/proc/self/exe`. It does not modify
the generated project or Lean inputs. With the pinned Lean root and this
identity-path correction, the unchanged trusted preflight succeeded.

## Inventory reconstruction and bijection

The trusted inventory selected module `VERIFICATION` from `prove.sh`. Its local
closure inside the frozen `verification.k` contains only `VERIFICATION`;
`MPY` is imported from the required external `semantic.k` and is not a local
module in `verification.k`.

Exactly one rule occurs in that closure:

```k
  rule expectedSumProduct(IS)
       => PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))
```

Independent reconstruction produced:

| Field | Recomputed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | lines 9–10 |
| Attributes | empty |
| Normalized SHA-256 | `08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1` |
| `source_rule_id` | `rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1` |
| Whole inventory SHA-256 | `e8b2af5d56d43143bcb41185878698b73f7fef8d96887a96fd2fbafe09431f9e` |
| `verification.k` SHA-256 | `f862f6f645a2bf62a530087f0ced39b85a998b8be1be82566b5e86cc73e95d44` |

I recomputed the normalized rule hash and canonical whole-inventory hash
separately from the trusted inventory result. Both agree.

`/reference/lemma-discovery.json` has one and only one entry, in the same
order, with exactly that identity. Its inventory hash also agrees. There are
no omissions, duplicates, extra entries, reordered identities, altered spans,
or altered hashes. The manifest file hash is
`d529a4c1e08a7455591481e774b5eda00b9e800038dd70d1d0d204f98fac84ed`,
matching the audit input and all Stage 4 bindings.

## Independent classification judgment

The sole rule is correctly classified as `DEFINITION`.

`expectedSumProduct` is introduced immediately above the rule as a total
function from `Ints` to `PyVal`. The rule gives that new symbol its complete
meaning: a tuple containing the mathematical integer-list sum and product.
The symbol has no prior operational or mathematical interpretation that the
rule could be proving.

The fixed semantics defines the referenced recurrences:

- `sumInts(.Ints) => 0`;
- `sumInts(I , IS) => I +Int sumInts(IS)`;
- `productInts(.Ints) => 1`;
- `productInts(I , IS) => I *Int productInts(IS)`.

The program semantics maps source calls to `sum` and `prod` through
`sumValue` and `productValue`, and the final reachability claim requires
`expectedSumProduct(IS)`. Thus the definition is directly relevant to both
the source program and the postcondition.

It is not an `OPERATIONAL_RULE`: it matches no cell, invocation, expression,
continuation, binding, or state transition and does not preempt execution of
the program. It is not a `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove
this same rule against a module without it. It is not a `DOMAIN_LEMMA`: it
introduces the named postcondition summary rather than asserting a separate
fact about already-defined objects.

The rule has no `simplification` attribute. Consequently the additional
simplification-class restriction is satisfied vacuously.

The independently determined class counts are:

- `DEFINITION`: 1;
- `OPERATIONAL_RULE`: 0;
- `PROVED_DERIVED_LEMMA`: 0;
- `DOMAIN_LEMMA`: 0.

The true domain-lemma set is therefore genuinely empty.

## Stage 4 generation, bijection, and target identity

The required call to
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation, ...)` returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- generated-tree hash
  `1599353254d79bd4c6a13fe8063d91d5ba1e6900df86e943671f14dcb4377a29`;
- fresh `lake clean` exit 0 with empty output;
- fresh `lake build` exit 0 with output SHA-256
  `91173c4611c2c6d1f4c648f6763ec5f6f18ea21a8449a3c5403786e93c1a0c79`.

The complete returned build output is preserved and reports all generated
modules built successfully.

Independent inspection confirms an exact empty-to-empty mapping:

- `input-manifest.json.source_rules` is `[]`;
- `obligation-map.json.source_rules` is `[]`;
- `obligation-map.json.obligations` is `[]`;
- `obligation-map.json.trust_parameters` is `[]`;
- `generator-manifest.json.obligation_count` is 0;
- the generator, export result, stored preflight, and audit input all record a
  null target;
- no Lean source contains a `targetStatement` declaration;
- `/candidate` does not exist.

There is no weakened, irrelevant, duplicated, omitted, or vacuous conjunct:
no conjunct or generated proposition exists. This is the correct Stage 4
result because the independently classified domain set is empty. The generated
Lean definition of `expectedSumProduct` also expands to the generated sum and
product functions, consistent with the frozen K definition, but it is not
presented as a proof obligation.

The trusted final mechanical gate separately returned `status: PASS`,
`mode: CLASSIFICATION_ONLY`, `target: null`, and no used axioms. Its
`semantic_classification` field is explicitly `NOT_EVALUATED`; the semantic
classification above is my independent judgment, not an inference from that
gate.

## Hash accounting

The independent checker reproduced all signed input and artifact-bound hashes:

| Binding | Recomputed SHA-256 |
|---|---|
| Signed resolution | `478e7742032676322457923247ec3fb68d24d061165593b4f2e484dca77c366a` |
| Stage 1 pipeline tree | `65461e9d38e144f5c6fb7e3d5b64c3b53d169b09bcbe625f8113e743f31b72a3` |
| Stage 1 export tree | `371cde27d62c71b300d9febf459275aa9d3e14e3013635e53cc44e7753a4e219` |
| Stage 2 selected tree | `a0b84a7941d5fa39430955d457d3c29e895e6d0bea63c220360a8de21b03cec2` |
| Stage 3 manifest | `d529a4c1e08a7455591481e774b5eda00b9e800038dd70d1d0d204f98fac84ed` |
| Stage 4 generation tree | `9ae1580e8db0457cb6fe5250bd7c5f1aaa55a2a8a2df44332623e31566269bc7` |
| Generated project tree | `1599353254d79bd4c6a13fe8063d91d5ba1e6900df86e943671f14dcb4377a29` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `f418820b0f4fa6b06b49fd9ca7eeaa41c8116dafef489eec13e9ee502c7b4865` |

The complete Stage 1 file set exactly equals the keys in
`stage1_source_hashes`, and every individual file hash matches. The generator
manifest's toolchain object exactly equals the trusted lock.

Two generator-source provenance fields do not reconcile:

| Manifest field | Recorded | Trusted `/reference/tools` file |
|---|---|---|
| `exporter_sha256` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean_py_sha256` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | `92e9515ae1e4c5275b0cd366e5ff5c16ad35af1afdaf070ef1ae7c0980998964` |

The untrusted manifest is the only mounted occurrence of the recorded exporter
hash. An environment copy at `/opt/humaneval/tools/klean.py` happens to match
the recorded Klean hash, but it is not the trusted mounted tool copy specified
for this audit; neither environment nor trusted copy matches the recorded
exporter hash. The trusted preflight and final gate do not check these two
fields.

This leaves the exact generation-time source versions unpreserved or
unaccounted. It prevents a PASS on the request to verify every recorded hash.
It does not make the selected classification or zero-obligation result
illegitimate: the frozen rule identity, independent semantic classification,
empty obligation bijection, null target, absence of a candidate, complete
artifact bindings, and clean generated build were all re-established without
trusting those self-reported generator-source hashes.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
