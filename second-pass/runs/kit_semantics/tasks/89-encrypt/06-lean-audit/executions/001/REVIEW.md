# Independent Stage 3/4 audit: HumanEval 89-encrypt

## Outcome and scope

The launcher-selected mode is `CLASSIFICATION_ONLY`, matching both
`AUDIT_MODE` and `/audit-input.json`. The condition is `kit-semantics`, the
semantics mode is `SUPPLIED_SEMANTICS`, Stage 4 is selected as
`KLEAN_NO_OBLIGATIONS`, and no `/candidate` or Stage 5 workspace/invocation is
present. Accordingly, this review audits the frozen K inventory, every Stage 3
classification, deterministic Stage 4 provenance and generation, and the
required Stage 4 preflight. Stage 5 proof identity, axiom printing, and
operational-bridge parameter checks are not applicable.

All mounted candidate/provenance material was treated as untrusted evidence.
No prior verdict, review, rationale, log, or comment was accepted as authority.

## Producer-source provenance gate

I hashed the two mounted generation-time producer files before judging the
Stage 4 result:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes exactly match `generator-manifest.json` and
`source-manifest.json`. The source manifest contains exactly those two files,
binds them to generator image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`,
and that image ID matches the immutable image-key component of the producer
path recorded in `/audit-input.json`. The producer bundle tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
also exactly matching the audit input. Thus the infrastructure producer-source
gate passes; there is no `AUDIT_ERROR` condition.

Raw evidence: `evidence/01-producer-sha256.txt`,
`evidence/02-producer-tree-sha256.txt`, and
`evidence/04-independent-integrity-checks.txt`.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` implementation
on the frozen `/reference/k-proof`, I reconstructed the local verification
module closure as exactly one module: `VERIFICATION`. Its frozen
`verification.k` SHA-256 is
`49b3cd3442e5a9f3d74f9942ca9e3bb5fd636f472a3f9426dc55ed81b88beaba`.

The reconstruction found exactly nine rules. For every entry I independently
checked that the recorded source slice equals the indicated physical lines,
normalized it by whitespace, recomputed the normalized SHA-256, and confirmed
that `source_rule_id` is exactly `rule-` followed by that digest.

| Order | Source span | Normalized SHA-256 | Rule head | Independent class |
|---:|---:|---|---|---|
| 1 | 8–9 | `a2cf8a164cbf94a5a3d7e444fbdaf3102628d2d0fecf228f37fd79d4dece6873` | `rot4Code` | `DEFINITION` |
| 2 | 13–14 | `d0417986ed3df602be0bfac4ca4cca3508a931dd5e1f044c0f0c1403dda203c7` | `encryptedChar`, below range | `DEFINITION` |
| 3 | 15–16 | `235635117bf711de90184aa7ad59620fe6b55936d3bbd90d5bb3b6a779d23518` | `encryptedChar`, lowercase | `DEFINITION` |
| 4 | 17–18 | `7fd0c0a9b39e8cb02242fc4650209b4e029307a059efc848cc10aeb01bec0b3e` | `encryptedChar`, above range | `DEFINITION` |
| 5 | 22 | `5a9a473afba1abcdb4a753006cdb3325c9531614b72a97d3ae145928cb54c00e` | `encryptFold`, base | `DEFINITION` |
| 6 | 23–26 | `6d8f5b2a6f2c94349997e8605406de5e3a62f684322db20582a216c99de16051` | `encryptFold`, recurrence | `DEFINITION` |
| 7 | 29 | `85d0bc26ae10c2b14fd916a400f96b49f796f68ed4a275143ca218d6795865b0` | `encryptResult` | `DEFINITION` |
| 8 | 33 | `5e6f27b3aa1140b7b8710b50f99a56ad029c2c48b9706918c0973fff130113a2` | `finalLoopChar`, base | `DEFINITION` |
| 9 | 34–35 | `f55a8da87fb92ce9e96ebbc4ea82ce71e9cee705e034c1c7003d546479f625c2` | `finalLoopChar`, recurrence | `DEFINITION` |

The canonical JSON hash of that ordered rule list is
`21e3419f1942121a9fa0035fd52d04a450b0359c12014aa2545fe788fed4d6d8`.
It matches the protected discovery manifest, Stage 4 input manifest, and
generator provenance. The protected manifest contains these same nine IDs in
exactly this order, with no omission, duplicate, extra identity, changed hash,
or unclassified entry. This order check is stricter than merely comparing the
sets of IDs.

Raw inventory and the executable comparison are in
`evidence/03-reconstructed-rule-inventory.txt` and
`evidence/04-independent-integrity-checks.txt`.

## Independent classification judgment

All nine entries are genuine definitions, and the true domain-lemma set is
empty.

The operational path in the supplied semantics is explicit: string iteration
yields a one-character `str(iCons(C, .IntSeq))`; the loop binds that value to
`c`; `ord` returns `C`; integer comparisons implement the two source guards;
integer `%` dispatches to `pyMod`; `chr` turns the in-range integer back into a
one-character string; `AugAssign` updates `out` through string `+`; and string
`+` is `seqConcat`. The `encrypt-loop` claim relates that actual loop body to
the summaries, while `encrypt-entry` executes the frozen function body and
concludes `result = str(encryptResult(S))`.

The individual judgments are:

- `rot4Code` names exactly the source arithmetic
  `((C - 97 + 4) % 26) + 97`. Its divisor is the fixed nonzero value 26, and
  the supplied `%` semantics is exactly `pyMod`.
- The three guarded `encryptedChar` equations jointly define one total
  one-character summary. Their guards `C < 97`, `97 <= C <= 122`, and
  `C > 122` are pairwise disjoint and exhaustive over `Int`. They preserve
  non-lowercase codes and rotate exactly the lowercase interval, matching the
  source branch.
- The two `encryptFold` equations are a base case and a structurally decreasing
  recurrence over the remaining `IntSeq`. The step appends the current
  `encryptedChar` to the accumulator before recurring, exactly matching the
  source's left-to-right `out += ...` update.
- `encryptResult` is a macro initializing that fold with `.IntSeq`, exactly
  matching `out = ""`.
- The two `finalLoopChar` equations are a structurally decreasing proof-term
  recurrence for the loop-target binding. Empty input preserves the prior
  value; nonempty input finishes with the last yielded one-character string.
  This is relevant to the source state and the loop claim's `c` binding even
  though `c` is not returned.

Every LHS is a named function term, not an operational configuration; none of
the nine rules contains a `<k>` or other cell pattern or replaces program
execution. None states a human-facing output property separate from the named
summary. Therefore none is an `OPERATIONAL_RULE` or `DOMAIN_LEMMA` disguised as
a definition. There are no entries labeled `PROVED_DERIVED_LEMMA`, so the
proof-before-use condition has no candidate to assess. None of the nine rules
has a `simplification` attribute, so the simplification-class restriction is
satisfied trivially.

Boundary checks agree with this reading: codes 96 and 123 are preserved; 97
maps to 101; 118 maps to 122; 119 wraps to 97; and 122 maps to 100. For the
sequence `(97, 33, 122)`, the fold returns `(101, 33, 100)` in the original
order and the final loop target is code 122. Identity, constant, no-wrap,
reversed-fold, widened-guard, and constant-loop-target counterfactuals all have
explicit rejecting witnesses. The recorded finite check covers 17,521 cases
with zero mismatches; it is supporting evidence only, not the basis of the
universal judgment, which follows from the equations and operational rules.

The relevant frozen excerpts and finite probes are preserved in
`evidence/07-operational-semantics-excerpts.txt` and
`evidence/09-classification-boundary-checks.txt`.

## Deterministic Stage 4 generation

The independently classified `DOMAIN_LEMMA` list is genuinely empty. Stage 4
therefore must not turn an unproved mathematical proposition into a Lean goal,
and `KLEAN_NO_OBLIGATIONS` is the correct status.

The Stage 4 bindings are exact:

- `input-manifest.json` contains all nine reconstructed definitions and empty
  operational, proved-derived, and source-rule lists.
- `generated/obligation-map.json` is exactly schema 3 with
  `source_rules: []`, `obligations: []`, and `trust_parameters: []`.
- Its raw SHA-256 is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching `generator-manifest.json`.
- The source-rule/obligation mapping is thus an exact empty-to-empty
  bijection: no omission, duplicate, irrelevant conjunct, weakened conjunct,
  or vacuous `True` conjunct exists.
- `obligation_count` is 0 in the generator manifest, export result, preflight,
  and fresh preflight result.
- The generator manifest target, launcher-recorded target, recorded preflight
  target, and freshly recomputed target are all `null`. An independent scan of
  every generated Lean source found zero `def targetStatement` declarations.
  Zero obligations therefore produced no target rather than a vacuous theorem.
- `/candidate`, the Stage 5 result, Lean workspace, and Lean invocation are all
  absent/null as required.

The generated tree digest is
`f70a3ff7937391dfd18892dd3252d316ad128487eba99a1ed018bcd6e896f824`,
and the complete selected Stage 4 tree digest is
`4e7d3f6cd7f982c28ffa3aac1883efc064fb62764a7a86cc037a5fcf53a84d5a`.
Both match `/audit-input.json`. The generated project contains 41 recorded
non-propositional Klean trust declarations, but no generated proposition or
proof target depends on them in this classification-only case; the trusted
preflight independently reconciled them with `trust-inventory.json` and
rejected proposition-shaped trust.

## Fresh mechanical preflight

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these three inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`

The first attempt was preserved because Lake could not locate its installation
inside the command sandbox. The diagnosed cause was specific and
reproducible: the sandbox creates a PID namespace whose numeric process IDs do
not exist in its read-only host `/proc`, while Lean 4.22 locates its executable
with `/proc/<getpid()>/exe`. I compiled a narrow local `LD_PRELOAD` shim under
`/tmp/audit-work` that only corrects Lean/Lake self-executable `readlink` calls
to the pinned v4.22.0 toolchain paths. It does not alter the trusted preflight
code, frozen inputs, generated sources, or compiler output. Its source and hash
are retained with the evidence.

With that environment compatibility repair, the exact preflight returned
`KLEAN_NO_OBLIGATIONS`. Its fresh temporary copy had `lake clean` exit 0 and
`lake build` exit 0. The build output hash is
`6fca8c6c27045add0c20ad965ffad6defaf6f7340c5c92bb2c106cadf738e60f`,
identical to the recorded Stage 4 preflight, and it built all seven Lean
modules successfully. The returned Stage 1 export hash, Stage 3 manifest hash,
generated tree hash, target, obligation count, trust-declaration count, and
sorry count all exactly match the recorded values.

The failed and successful transcripts are
`evidence/05-klean-preflight-rerun.txt` and
`evidence/06-klean-preflight-rerun-success.txt`; the compatibility evidence is
`evidence/08-lean-sandbox-workaround.txt`.

## Independent hash accounting

The signed resolution digest recomputes to
`72b160ecdd967d790d86c9b8bbefa7d24d2f751055f497cbb9a4d1fc05024cbd`.
In addition to the producer and Stage 4 hashes above, I independently verified:

| Artifact | Recomputed hash/result |
|---|---|
| Stage 1 selected tree, pipeline framing | `c8c910a33b3736a15d24b6b60c87653aa2415e061f651c1e6be219a376e65788` |
| Stage 1 export tree, generator framing | `34429e7bfc8bcb6b60cfe12874ee6be56c8b21034a8335307e0ddfd47d17c6ba` |
| Stage 1 per-file source map | all 807 entries exactly match |
| Selected Stage 2 audit tree | `865f8a7590cde371a50973bc084bcef6879e9cceeddac0b81e230d0ba18cf277` |
| Protected Stage 3 manifest | `de185039610d20c1987d79af0462093496a579daffad7b10c22d84c95d362c86` |
| Canonical rule inventory | `21e3419f1942121a9fa0035fd52d04a450b0359c12014aa2545fe788fed4d6d8` |
| Selected Stage 4 generation tree | `4e7d3f6cd7f982c28ffa3aac1883efc064fb62764a7a86cc037a5fcf53a84d5a` |
| Generated Lean project | `f70a3ff7937391dfd18892dd3252d316ad128487eba99a1ed018bcd6e896f824` |

The independent checker also compared the selected artifact hashes, embedded
preflight document, generator toolchain lock, raw trust-inventory hash, and all
manifest provenance bindings. Every assertion passed. Exact verdict-bearing
commands are listed in `evidence/COMMANDS.md`; their raw results and exit codes
are retained in the numbered transcripts.

## Judgment

The protected Stage 3 classification is mathematically correct: all nine local
rules define named summaries, recurrences, or a macro that exactly track the
frozen source under the supplied operational semantics. There is no true
domain lemma. The deterministic Stage 4 generation faithfully maps that empty
domain set to zero obligations and no target, with complete producer and
manifest provenance. The mandatory fresh preflight passes. Since the selected
mode is classification-only and no Stage 5 candidate exists, no proof-mode
condition remains to audit.

VERDICT: PASS
LEGITIMACY: LEGIT
