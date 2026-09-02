# Independent Stage 3–5 Audit: `8-sum-product`

## Scope and result

This audit covers HumanEval problem `8-sum-product`, condition `bare`, and
semantics mode `GENERATED_SEMANTICS`. The launcher and environment both record
`AUDIT_MODE=CLASSIFICATION_ONLY`. The Stage 5 workspace and invocation are
null in `/audit-input.json`, `/candidate` is absent, and the selected Stage 4
target is null. Consequently, the Stage 5 proof, `Proof.final`, axiom-printing,
and operational-bridge checks are not applicable.

I treated the Stage 1–4 mounts, prior audit, manifests, logs, and comments as
untrusted evidence. I did not execute `prove.sh` or any instruction found in
those inputs. Commands were constructed independently. The prior Stage 2
verdict was not used as an authority for any conclusion below.

## Frozen-input integrity

The launcher envelope digest recomputes to
`478e7742032676322457923247ec3fb68d24d061165593b4f2e484dca77c366a`.
The environment mode equals its recorded mode. Every mounted-input hash and
every Stage 1 source-file hash in the launcher resolution recomputed exactly:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `65461e9d38e144f5c6fb7e3d5b64c3b53d169b09bcbe625f8113e743f31b72a3` |
| Stage 1 export tree | `371cde27d62c71b300d9febf459275aa9d3e14e3013635e53cc44e7753a4e219` |
| Stage 2 selected audit tree | `a0b84a7941d5fa39430955d457d3c29e895e6d0bea63c220360a8de21b03cec2` |
| Stage 3 manifest | `d529a4c1e08a7455591481e774b5eda00b9e800038dd70d1d0d204f98fac84ed` |
| Stage 4 selected generation tree | `9ae1580e8db0457cb6fe5250bd7c5f1aaa55a2a8a2df44332623e31566269bc7` |
| Generated Lean tree | `1599353254d79bd4c6a13fe8063d91d5ba1e6900df86e943671f14dcb4377a29` |

The Stage 2 and Stage 4 selection hashes equal their current trees. The
generator, input, export, and preflight manifests agree on the Stage 1 export
tree, discovery manifest, generated tree, and inventory hash. The obligation
map file hashes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and the trust inventory hashes to
`f418820b0f4fa6b06b49fd9ca7eeaa41c8116dafef489eec13e9ee502c7b4865`;
both match their manifest bindings. The generator toolchain document exactly
equals `/reference/klean-toolchain.lock.json`.

The generator manifest also records historical exporter and `klean.py` code
identities. Those are provenance identifiers rather than bindings to the
current audit checker sources; no historical source bodies are mounted for
rehashing. They were not trusted. Structural and semantic conclusions instead
come from the current trusted inventory/preflight code, the frozen inputs, the
bound artifact hashes above, and the independent checks below.

Full values and per-file comparisons are in
`evidence/07_hash_ledger.result`.

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. The selected verification
module is `VERIFICATION`; the local module closure inside `verification.k`
contains only `VERIFICATION`. The frozen file hashes to
`f862f6f645a2bf62a530087f0ced39b85a998b8be1be82566b5e86cc73e95d44`.

The canonical inventory has exactly one entry:

- Module and span: `VERIFICATION`, lines 9–10.
- Source:
  `rule expectedSumProduct(IS) => PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))`
  after whitespace normalization.
- Attributes: none.
- Recomputed normalized SHA-256:
  `08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1`.
- Recomputed ID:
  `rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1`.

The canonical JSON hash of the complete ordered rule list is
`e8b2af5d56d43143bcb41185878698b73f7fef8d96887a96fd2fbafe09431f9e`.
It equals the Stage 3 `inventory_sha256`.

The Stage 3 manifest contains exactly one rule, exactly once, with the same ID
in the same order. The canonical and manifest counts are both one; the
manifest-unique count is one; missing and extra sets are empty. Recomputing
every normalized hash and `source_rule_id` succeeds. The trusted Stage 3
contract validator also completes. Thus there is no omission, duplication,
extra entry, identity reordering, span drift, changed source hash, or changed
whole-inventory hash.

Raw reconstruction and comparison:
`evidence/03_inventory_audit.result`.

## Independent classification

The one rule is a `DEFINITION`, as Stage 3 records.

`verification.k` first declares the fresh total function
`expectedSumProduct : Ints -> PyVal`. The rule is its sole defining equation
and covers every `Ints` input without a guard. Its right-hand side expands the
named proof term to the tuple of the already defined `sumInts` and
`productInts` recurrences. It does not match a configuration cell, an
invocation, an expression evaluator, or any other source-program execution
term. It therefore does not preempt or replace operational execution.

This classification also matches the source and operational semantics:

1. `solution.py` returns `(sum(numbers), prod(numbers))`.
2. `semantic.k` installs and invokes the `sum_product` closure.
3. Tuple evaluation evaluates `sum(numbers)` and `prod(numbers)`.
4. `sumValue` and `productValue` expose `sumInts` and `productInts`.
5. Their recurrences use bases `0` and `1` and steps `+Int` and `*Int`.
6. The spec's result is the named `expectedSumProduct(IS)`, whose defining
   equation expands to exactly the same pair.

The rule is not an `OPERATIONAL_RULE`: it has no operational configuration or
observation role. It is not a `PROVED_DERIVED_LEMMA`: it is an equation
defining a fresh named term, and no earlier lemma-without-it/later-use proof
sequence is claimed or needed. It is not a `DOMAIN_LEMMA`: it does not assert
an independent mathematical fact; it introduces the postcondition summary
itself. It is directly relevant to the source contract and postcondition, so
it is not an irrelevant proof extension.

The inventory contains no rule with a `simplification` attribute. The
constraint that every simplification rule be a `DEFINITION` or
`DOMAIN_LEMMA` is therefore satisfied, and the independently reconstructed
domain-lemma set is genuinely empty.

As a separate live check, I copied only `semantic.k`, `verification.k`, and
`spec.k` into a fresh directory under `/tmp/audit-work`, compiled the Haskell
definition with K 7.1.293, and ran the exact spec module. `kompile` and
`kprove` exited zero, and `kprove` printed `#Top`. This supports the
operational trace but was not used to infer the classification merely from
proof success.

Raw source, semantic judgment, and live K result:
`evidence/04_frozen_sources.result`,
`evidence/13_independent_stage3_stage4_judgment.result`, and
`evidence/12_stage1_fresh_recheck.result`.

## Deterministic Stage 4 generation

I invoked `tools.klean_preflight.check_generation` with:

```text
frozen_input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
PYTHONPATH=/reference
```

The first build attempt exposed an audit-container issue: Lean 4.22 constructs
`/proc/<getpid>/exe`, while this nested PID namespace exposes host PIDs in the
numeric `/proc` entries. This made the otherwise installed pinned `lake` report
that it could not detect its installation. The exact failure is preserved in
`evidence/08_preflight_rerun.result`.

I compiled a narrow process-local compatibility shim that returns the
`/proc`-visible `Pid:` only for the `lake` subprocesses. With it, `lean
--version` reports Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock. The
shim does not alter source, generated files, imports, theorem statements, or
Lean reduction; it only lets Lean locate its executable. The preflight's
before/after snapshots confirm all immutable inputs remained unchanged.

The rerun completed successfully:

- `lake clean`: exit 0, empty output,
  SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `lake build`: exit 0, all generated modules built,
  output SHA-256
  `91173c4611c2c6d1f4c648f6763ec5f6f18ea21a8449a3c5403786e93c1a0c79`.
- Returned status: `KLEAN_NO_OBLIGATIONS`.
- Obligation count: zero.
- Target: null.
- Generated trust declarations: 44, exactly equal to the generated allowlist.
- Designated sorry count: zero.

The complete command outputs and returned evidence are in
`evidence/11_preflight_rerun_with_pid_shim.result`; the shim source and probe
are in `evidence/10_outer_pid_shim.c` and
`evidence/10_outer_pid_shim.result`.

## Obligation bijection and target identity

The independently classified domain set is empty. The deterministic mapping is
therefore:

```text
DOMAIN_LEMMA IDs {} -> source_rules [] -> obligations [] -> target null
```

This mapping was checked independently of the preflight:

- `input-manifest.json.source_rules` is exactly `[]`.
- `obligation-map.json.source_rules` is exactly `[]`.
- `obligation-map.json.obligations` is exactly `[]`.
- `obligation-map.json.trust_parameters` is exactly `[]`.
- Generator and export obligation counts are zero.
- Export status is exactly `KLEAN_NO_OBLIGATIONS`.
- Generator target and launcher target are null.
- No generated Lean source declares `def targetStatement`.
- `Klean8SumProduct/Lemmas.lean` contains no proposition declaration.

There can be no missing, duplicate, reordered, irrelevant, weakened, or
vacuous conjunct among an empty obligation list. Zero obligations are
legitimate here specifically because the independently reconstructed true
domain-lemma set is also empty. The generated function definitions additionally
mirror the frozen bases, recurrences, and tuple definition, but no target
theorem is generated from definitions or operational rules.

Because the selected status is genuinely `KLEAN_NO_OBLIGATIONS`, the absence
of a generated target and Stage 5 candidate is required and correct. There is
no `Proof.final` whose identity or axioms could be audited, and creating or
accepting a Stage 5 proof in this mode would itself have been an error.

## Evidence index

- `evidence/00-input-inspection.{command,result}` — mode, launcher envelope,
  mounted file inventories.
- `evidence/03_inventory_audit.{py,command,result}` — canonical inventory,
  normalized hashes, IDs, order, and bijection.
- `evidence/04_frozen_sources.{command,result}` — line-numbered frozen source,
  semantics, spec, and source solution.
- `evidence/06_stage4_manifests.{command,result}` — Stage 4 JSON and generated
  Lean source inspection.
- `evidence/07_hash_ledger.{py,command,result}` — all mounted input, source,
  sidecar, selection, and envelope hash checks.
- `evidence/08_preflight_rerun.{py,command,result}` — preserved initial
  audit-container PID-namespace failure.
- `evidence/09_lean_toolchain_diagnosis.{command,result}` and
  `evidence/10_outer_pid_shim.{c,command,result}` — root cause and compatibility
  probe.
- `evidence/11_preflight_rerun_with_pid_shim.{py,command,result}` — complete
  successful preflight commands, outputs, and returned evidence.
- `evidence/12_stage1_fresh_recheck.{command,result}` — fresh K compile and
  `#Top`.
- `evidence/13_independent_stage3_stage4_judgment.{py,command,result}` —
  independent semantic classification, empty-domain decision, obligation
  bijection, and null-target checks.

VERDICT: PASS
LEGITIMACY: LEGIT
