# Independent Stage 3–4 audit: 79-decimal-to-binary

Audit mode is `CLASSIFICATION_ONLY`, matching both `AUDIT_MODE` and the signed
`/audit-input.json`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, as required. I did not rely on
the earlier Stage 2 verdict, Stage 1 review narrative, generated comments, or
any prior classification as authority.

## Provenance and frozen-input integrity

The mandatory Stage 4 producer-source gate passes.

- `/reference/generation-tools/klean_export.py` hashes to
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`.
- `/reference/generation-tools/klean.py` hashes to
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
- Those values agree exactly with `generator-manifest.json` and
  `source-manifest.json`.
- The immutable image ID is
  `sha256:2db35f33b29b4ada4f78dd04470349652b5f62e1ff63355111720eee4e3cc162`
  in both manifests, and its digest component is the final path component of
  the audit-input producer bundle.
- The producer bundle's trusted pipeline tree hash is
  `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb`,
  exactly the value in the audit input.

The signed audit-input envelope validates with resolved-input digest
`c5cc9ec086649a9ec54881c294f16f13fe1e288e8e4b978c17dbad7c2d29e219`.
Every recorded top-level hash was independently recomputed and matched:

- Stage 1 pipeline tree: `178c3afda295cbdf3074cb0a38f0283e8eac8423d58546005baf8c7168b3742a`;
- Stage 1 Klean tree: `186319a5ffcce15e46718dc2272d7f7bbddb8eea470eb15b59751773c9a9a7ec`;
- Stage 2 tree: `e4bfedf66f2374428da589b25449a35d0043aa1ebf8089bb890ec5f6a0423a42`;
- Stage 3 manifest: `5b4045b605dada489c3d3f20673e2a5b50bdef4d1b075286e10bffb0ba3178e0`;
- Stage 4 tree: `d0d9b02ea8708c4723ae5b762daeb3f8d2ede7503ac544b503e2851c8abf4f1c`;
  and
- generated project tree: `c76244799316389967f6cfec67e38e87cc8735d65d3a64326bf78eab33cf0457`.

All 788 individually recorded Stage 1 file paths and hashes also matched, with
no missing, extra, or changed file. Raw results are in
[producer-integrity-contract.log](/audit-output/evidence/producer-integrity-contract.log),
[hash-reconciliation.log](/audit-output/evidence/hash-reconciliation.log), and
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## Canonical rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The local verification-module closure contains
only `VERIFICATION`, and its `verification.k` hash is
`d019861f570f855722bb54971461cbe467b7e369e9240c150647a0a8c1b1c0c1`.
The reconstructed inventory hash is
`2ed8f1e00a992ffb3f759fe8c7c61e8766ab82bbf0e80ff4f6562940c03a1e93`.

For every row below, `source_rule_id` is exactly `rule-` followed by the full
normalized SHA-256 shown. These are in frozen source order.

| Span | Normalized SHA-256 | Attributes | Independent class |
|---|---|---|---|
| 11–12 | `0a82089db438d6896e57def6a6d687fd829e250b2e3a57f86e1114728cabfd3d` | none | `DEFINITION` |
| 14–19 | `311c7818aa61ab48edceaaf524aa96cdc5343c25e35edeb7b7895c50438f7e39` | none | `DEFINITION` |
| 21–22 | `73d9b9e52c4141a668b87a1bda99e477853f9ac07bdde4e178dff6db56018487` | none | `DEFINITION` |
| 28–30 | `bb0dd8b44a02de305b300de162887fd197bafc6ab3bffe93bdff08e62e6f569e` | none | `DEFINITION` |
| 32–34 | `288f1d1aa76e8c443e284a26c6a3ffaa6dc11746b856850011993c220b27b228` | none | `DEFINITION` |
| 36–37 | `b28ffaf5f18a64587bbe6d9f806d4536c273d62a4236f1341522cafaef664d27` | none | `DEFINITION` |
| 41–42 | `7c2e6fd20be28dd4a2b6f16a4389ef39d505f39f3f321b7eab857f76d1bf7526` | none | `DEFINITION` |
| 44–44 | `c6ae0b2b0ab8b9dfc28262926c22380fb803f9275d4e040bba7d777a9d8c61d9` | `owise` | `DEFINITION` |

The protected Stage 3 manifest has exactly these eight unique identities in
this order and the same whole-inventory hash. There are no omissions,
duplicates, extras, reordered identities, or changed hashes. Full reconstructed
texts, spans, IDs, and hashes are in
[inventory-reconstruction.log](/audit-output/evidence/inventory-reconstruction.log).

## Independent classification judgment

All eight rules genuinely define named summaries or their recurrence; none is
a disguised domain lemma.

The first three equations define `binRel` over a disjoint and exhaustive
integer sign partition. At zero it equates the accumulated and output code
sequences. At positive `N` it recurses after prepending one digit code and
replacing `N` by the quotient. The negative equation is the totalizing false
case. This is a recurrence definition, not an independent claim about an
already defined operation.

The next three equations similarly define `decimalTailRel`: the zero case is
the exact code sequence `0db`, the positive case invokes `binRel` with `db` as
the suffix accumulator, and the negative case totalizes the summary. The last
two equations define `decimalResultRel` by removing the required leading `db`
codes and delegating to `decimalTailRel`, with an `owise` false complement.

This classification agrees with the frozen operational semantics, not merely
with the rule names. The source loop performs:

1. `decimal % 2`, which supplied `int.k` reduces to `pyMod(decimal, 2)`;
2. `chr(48 + remainder)`, which supplied `builtins.k` converts to the one-code
   string `iCons(48 + remainder, .IntSeq)`;
3. string prefix concatenation, whose supplied `seqConcat` rules prepend that
   code to the accumulator; and
4. `decimal // 2`, which supplied `int.k` reduces to
   `(decimal - pyMod(decimal, 2)) /Int 2`.

That is exactly the positive `binRel` recurrence. For the boundary witness
`N = 0`, `decimalTailRel` requires `0db` and `decimalResultRel` supplies the
leading wrapper, yielding `db0db`. For the counterfactual-sensitive witness
`N = 2`, the recurrence prepends `0` then `1` to the trailing `db`, yielding
`db10db`; changing the digit offset, quotient, or accumulator direction would
disagree with the frozen loop. These checks rule out a constant, identity, or
hard-coded summary interpretation.

No inventory rule matches a `<k>` cell, continuation, environment, binding,
or other operational state, so none is an `OPERATIONAL_RULE`. No rule is
claimed as `PROVED_DERIVED_LEMMA`, and there is consequently no proof-order
claim to validate. There are no `simplification` attributes; the sole `owise`
rule is a definitional complement. Every rule is relevant to the loop summary
or final postcondition. The independently reclassified `DOMAIN_LEMMA` set is
therefore genuinely empty. The frozen source and load-bearing semantics
excerpts are preserved in
[semantic-source.log](/audit-output/evidence/semantic-source.log).

## Deterministic Stage 4 generation

I reran the required trusted
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three mandated inputs. The first attempt failed before project elaboration
because this audit runtime did not expose an executable path usable by
Lean/Lake (`failed to locate application` / `could not detect the
configuration of the Lake installation`). I recorded that failure rather than
treating it as a candidate result.

I then used the pinned direct Lean 4.22.0 binary plus a narrow temporary
`LD_PRELOAD` shim that changes only `readlink`/`readlinkat` for the current
process's `/proc/.../exe` link. The shim reports the pinned toolchain path; it
does not alter the generated tree, imports, source reads, elaboration, or proof
kernel. With it, Lean reported the exact locked version and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the same trusted
`check_generation` returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0 with “Build completed successfully”;
- obligation count 0;
- designated sorry count 0;
- target `null`; and
- the expected Stage 1, Stage 3, and generated-tree hashes.

The initial failure, shim source and hashes, exact rerun command, and returned
evidence are in [check-generation.log](/audit-output/evidence/check-generation.log),
[lean-toolchain-recovery.log](/audit-output/evidence/lean-toolchain-recovery.log),
[lean_app_path_shim.c](/audit-output/evidence/lean_app_path_shim.c), and
[check-generation-rerun.log](/audit-output/evidence/check-generation-rerun.log).

Independent of preflight, all cross-manifest hashes matched. The Stage 3
domain set, Stage 4 `input-manifest.json` source rules,
`obligation-map.json` source rules, and obligation list are all exactly `[]`.
The trust-parameter list is also empty, counts are zero in both generator and
export results, and there can be no duplicate, weakened, irrelevant, or
vacuous conjunct in an empty list. `generator-manifest.json`, the audit input,
independent target extraction, and preflight all record `target: null`.
`Lemmas.lean` contains only an empty namespace, and a source search found no
theorem, lemma, example, or generated-target declaration. The generated trust
inventory's 43 declarations are executable non-propositional boundary symbols;
the trusted preflight independently rejected proposition trust and found no
proof holes.

The exact empty bijection and target inspection are in
[manifest-bijection.log](/audit-output/evidence/manifest-bijection.log) and
[generated-target-inspection.log](/audit-output/evidence/generated-target-inspection.log).

## Stage 5 disposition

Stage 5 is correctly absent. The launcher selected `CLASSIFICATION_ONLY`, the
true domain-lemma set is empty, no generated target exists, the audit input has
null Lean workspace/invocation hashes, and `/candidate` does not exist.
Therefore a clean candidate build, `#print axioms Proof.final`, target-shadow
audit, and operational-parameter bridge audit are not applicable.

## Conclusion

The protected Stage 3 classification is complete and mathematically correct.
The deterministic Stage 4 artifacts are provenance-bound and structurally
sound, and `KLEAN_NO_OBLIGATIONS` accurately reflects the independently empty
domain-lemma set. No Stage 5 project should exist, and none does.

VERDICT: PASS
LEGITIMACY: LEGIT
