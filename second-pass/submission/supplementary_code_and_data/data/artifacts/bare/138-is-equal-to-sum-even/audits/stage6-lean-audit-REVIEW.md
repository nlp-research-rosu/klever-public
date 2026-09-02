# Independent Stage 3–4 audit

Problem: `138-is-equal-to-sum-even`  
Condition: `bare`  
Semantics mode: `GENERATED_SEMANTICS`  
Signed audit mode: `CLASSIFICATION_ONLY`

## Outcome

The protected Stage 3 classification is complete and mathematically sound.
The true domain-lemma set is empty. The selected deterministic Stage 4 result,
`KLEAN_NO_OBLIGATIONS`, is therefore the correct result: its source-rule and
obligation lists are both empty, it generated no target proposition, and there
is no Stage 5 candidate. Producer provenance, all launcher-recorded hashes,
sidecar bindings, the generated tree, and a fresh trusted preflight rerun all
check out.

I treated the mounted K/Lean artifacts, prior audit, logs, manifests, and
comments as untrusted evidence. I did not rely on the prior Stage 2 verdict or
execute its scripts. The reconstruction used the trusted
`tools.k_rule_inventory` and contract code under `/reference/tools`; Stage 4
was checked with the required trusted `tools.klean_preflight.check_generation`.

## Input and producer integrity

The signed `/audit-input.json` envelope recomputes to
`1d244dc73fd3b989fc79f2b6d64da5458908f82884d4c14837c1f73299196c22`.
The launcher copy at `/audit-output/audit-input.json` is byte-identical.
Every recorded resolution hash was independently recomputed:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree hash | `fd6a4ab61c74ce3e776a94b44475898037ecba786c9b70ce0f5d017d1b554ae7` |
| Stage 1 export tree hash | `5a476623288743406a523bb18a9d55afaa9dff058293bd031044984c9a502705` |
| Stage 3 manifest | `2ed8abb6453b92734a8d436b64dcb1511329ebdc180005554d202faf9d572b83` |
| Selected Stage 2 audit tree | `1ce9b5e9c827b7c493a78d93bfe202ad8e6aea2d71f6a7fc0ad2ccb29a448fa8` |
| Selected Stage 4 generation tree | `e86d02130e48981a42029ff98ce37f93bfb9df01350dda87e3dcb47d9d5d92df` |
| Generation producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `2ada4f7650042aa106dba2d114ac1968f6ebf6c56570c6ecce60176b6964a6a7` |

All nine per-file Stage 1 hashes also match the signed
`stage1_source_hashes`. The selected Stage 2 and Stage 4 artifact hashes match
their selection records. The Stage 4 input manifest, export result, generator
manifest, embedded preflight record, obligation-map hash, trust-inventory hash,
and toolchain lock agree with the recomputed inputs.

I hashed the two generation-time producer sources before evaluating Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Those values match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus the source manifest. The immutable generator image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in both manifests, and its digest is also the producer-source directory
component recorded by `/audit-input.json`. There is no producer mismatch and
therefore no infrastructure `AUDIT_ERROR`.

Complete values and comparisons are in
`evidence/independent-checks.log`.

## Inventory reconstruction

The trusted inventory selected the sole locally declared verification module,
`VERIFICATION`; its local module closure is exactly `["VERIFICATION"]`.
`MPY` is imported from the separately required `semantic.k` and supplies the
fixed operational context, but it is not another module locally declared in
`verification.k`.

The frozen `verification.k` hash is
`ad8dd1b917ef0ec5bcc9d1f42acce2545b5420c57776fa239fb015540c3225a5`.
Independent extraction and normalization produced:

| Order | Span | Normalized SHA-256 / `source_rule_id` | Attributes |
|---|---|---|---|
| 1 | 10–11 | `df444b1d030ac9ca78919bfd775a5a03296a11547d9d28a09eb36785f9397593` / `rule-df444b1d030ac9ca78919bfd775a5a03296a11547d9d28a09eb36785f9397593` | none |
| 2 | 14–18 | `88b901aa7847ffb653815da50fc9ef8c784736ae52b2ae8c3a22a1e9022d78fe` / `rule-88b901aa7847ffb653815da50fc9ef8c784736ae52b2ae8c3a22a1e9022d78fe` | none |
| 3 | 21–22 | `5eddae4fc1a0fc36142764ad3da36cec90ecf05b5f586e6b0278165849bba1ee` / `rule-5eddae4fc1a0fc36142764ad3da36cec90ecf05b5f586e6b0278165849bba1ee` | none |

The canonical JSON hash of those ordered rule records is
`63b8c9228272c8278f7555435e02f61090a2224613424222e96a5ccd394152a4`.
It matches Stage 3 and the Stage 4 provenance.

The Stage 3 rule-ID list is exactly the same ordered three-element list. It has
no duplicate, omitted, extra, or reordered identity. For each entry I
independently sliced the recorded source lines, renormalized the text,
recomputed the normalized hash, and rebuilt `source_rule_id`; every value
matches.

## Independent classification judgment

1. `sumFourPositiveEvens(N) => N >=Int 8 andBool N %Int 2 ==Int 0` is a
   `DEFINITION`. It defines the fresh named Boolean summary on its complete
   integer domain; it does not rewrite a pre-existing mathematical fact.

2. `canonicalWitnessesAreValid(N) => ...` is a `DEFINITION`. It defines a
   fresh named proof term by expanding the positivity, parity, and sum checks
   for witnesses `N-6, 2, 2, 2`.

3. The `<k>/<result>` transition for `checkCanonicalWitnesses(N)` is an
   `OPERATIONAL_RULE`. It consumes an executable verification command and
   records its Boolean observation in the result cell. It is not a standalone
   mathematical implication.

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 compiles all three rules
before its single `kprove spec.k` call; no exact rule is first proved against a
module lacking it and then used in a later proof.

There are no rule-level `simplification` attributes. The `[function, total]`
annotations belong to syntax declarations, not to these rule records, so the
simplification classification constraint is satisfied.

The classification also agrees with the source and operational semantics. The
source returns `n >= 8 and n % 2 == 0`; its generated MPY AST has the same
structure. The semantics loads input `N`, evaluates the comparisons and
remainder by literal nonzero divisor 2, then applies Boolean conjunction.
Evaluating both operands rather than modeling Python short circuit is
observationally harmless here because the second operand is total and
side-effect free.

The summary is the exact intended arithmetic characterization. Four positive
even addends imply an even sum at least 8. Conversely, an even `N >= 8` has
the four positive even witnesses `N-6, 2, 2, 2`. The witness-check definition
expands precisely that construction, and the operational rule makes the check
observable for the sufficiency claim. Thus none of the three entries is an
irrelevant domain fact or a `DOMAIN_LEMMA` disguised as another category.
Counterfactual mutations of the parity summary, `N-6`, or the result-cell
update respectively change the summary, invalidate the witness sum, or change
execution, confirming the distinctions.

The resulting independent class counts are:

```text
DEFINITION:             2
OPERATIONAL_RULE:       1
PROVED_DERIVED_LEMMA:   0
DOMAIN_LEMMA:           0
```

The more detailed source-to-semantics analysis is in
`evidence/classification-analysis.md`.

## Deterministic Stage 4 generation

Because the independently determined domain set is empty, the expected
eligible `source_rules` list is empty. The following are exactly and
bijectively empty:

- Stage 4 input-manifest `source_rules`;
- generated obligation-map `source_rules`;
- generated obligation-map `obligations`;
- generated obligation-map `trust_parameters`.

The generator manifest, export result, recorded preflight, and rerun preflight
all report obligation count `0`. There are consequently no omissions,
duplicates, irrelevant/weakened obligations, or vacuous conjuncts. In
particular, the generator did not substitute a vacuous `True` theorem for an
empty conjunction.

Target identity is consistently null:

- generator manifest target: `null`;
- signed audit-input target: `null`;
- recorded Stage 4 preflight target: `null`;
- independent `klean_export.target_statement(generated)`: `None`.

The generated Lean sources contain no `targetStatement` declaration. This is
the exact fixed output required for a genuine zero-domain case.

I reran:

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

with the pinned Lean 4.22 toolchain on `PATH` and the sandbox-only proc shim
documented below. The wrapper calls
`tools.klean_preflight.check_generation` with:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
toolchain lock: /reference/klean-toolchain.lock.json
```

It copied the generated project to a fresh temporary directory, ran
`lake clean` and `lake build`, and returned:

```text
status:                  KLEAN_NO_OBLIGATIONS
obligation_count:        0
target:                  null
trust_declaration_count: 42
designated_sorry_count:  0
```

Both commands exited `0`; all nine build tasks completed. The 42 declarations
are the mechanically inventoried non-propositional Klean hook boundary, match
`trust-inventory.json`, and do not supply a proposition or proof. The trusted
preflight also verified no generated `sorry`, forbidden token, unlisted trust
declaration, unsafe import, or mutated input/sidecar/tree.

The audit sandbox exposes `/proc/self/exe` but not
`/proc/<getpid()>/exe`, while this Lean build uses the latter to find its
installation. Initial attempts therefore failed during tool startup. I used a
narrow `LD_PRELOAD` shim that redirects only `/proc/<number>/exe` readlink
requests to the semantically identical `/proc/self/exe`. It does not alter
candidate or provenance files. The pinned compiler then identified itself as
Lean `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the required preflight
completed. Preflight’s immutable snapshots before and after the build remained
identical. The diagnosis, shim source, exact commands, failed setup attempts,
complete successful build output, and returned evidence are under `evidence/`.

## Stage 5

Stage 5 is correctly inapplicable. `AUDIT_MODE` and the signed resolution both
say `CLASSIFICATION_ONLY`; the generated target is null, `stage5_result` is
null, both Lean workspace/invocation hashes are null, and `/candidate` is
absent. Running `#print axioms Proof.final`, checking candidate definitions, or
performing an operational-bridge audit on target parameters would invent a
proof stage forbidden by the genuine `KLEAN_NO_OBLIGATIONS` outcome.

## Evidence index

- `evidence/COMMANDS.md`: exact commands and log mapping.
- `evidence/independent_checks.py` and
  `evidence/independent-checks.log`: hash reconstruction, canonical inventory,
  ordered Stage 3 bijection, sidecar bindings, zero-obligation map, and target
  absence.
- `evidence/classification-analysis.md`: independent semantic classification
  and counterfactual analysis.
- `evidence/run_preflight.py` and
  `evidence/preflight-rerun-success.log`: complete trusted preflight command
  output and returned evidence.
- `evidence/lean-runtime-workaround.sh`,
  `evidence/proc-self-readlink-shim.c`, and
  `evidence/lean-runtime-workaround.log`: reproducible sandbox diagnosis and
  narrow workaround.
- `evidence/preflight-rerun.log`,
  `evidence/preflight-rerun-pinned.log`, and
  `evidence/preflight-rerun-configured.log`: retained failed setup attempts.

VERDICT: PASS
LEGITIMACY: LEGIT
