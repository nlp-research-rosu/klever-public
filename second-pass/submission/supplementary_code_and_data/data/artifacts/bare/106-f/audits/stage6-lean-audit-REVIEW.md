# Independent Stage 3–4 audit: HumanEval 106-f, bare, GENERATED_SEMANTICS

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, and the verified
`/audit-input.json` resolution also records `CLASSIFICATION_ONLY`. The selected
Stage 4 status is `KLEAN_NO_OBLIGATIONS`; the resolved target, Stage 5 result,
Lean workspace, and Lean invocation are all null. `/candidate` is absent.
Accordingly, this audit covers the independent Stage 3 rule classification and
deterministic Stage 4 generation. Candidate clean-build, `Proof.final`, axiom,
and operational-bridge checks are not applicable.

I treated the prior Stage 2 review and all mounted prose/logs as untrusted
evidence. The findings below come from the frozen source, the trusted inventory
and preflight code, direct hashing, and independent semantic inspection.

Raw commands, executable audit scripts, and returned results are under
`evidence/`; see `evidence/COMMANDS.md`.

## Frozen-input and producer authentication

The launcher audit document validates under
`tools.klean_audit_contract.verify_stage6_audit_input`. Its recomputed resolved
hash is
`ed7e8a4e873caa1344198806580b85664fde9c17f697bd3642ffe2427c7dc0fb`,
exactly the recorded value. The mounted and `/audit-output` copies of the
document are byte-identical.

All Stage 1 per-file hashes match `stage1_source_hashes`. The two relevant tree
hash schemes were applied as recorded:

- Stage 1 artifact:
  `9446aa8469c786d57b74e526869d9e7b4b8607f32285e9da67fce8789b068cb3`
- Stage 1 deterministic export:
  `0f5bd8572d3e64c809b341eb6ecd8c2e25e811d7f3cb7273e1c8ca38bec2fb83`
- Stage 3 manifest:
  `48bea5f3575a5437c31a8576bb4c4d1b555005701670bd9f2faedb04240c7ce8`
- selected Stage 4 artifact:
  `002ef1dc433ba178ecfbbfa648e3cf73442f206a796081c22a935847de50e168`
- generated project:
  `43764944be0e7c50fb4e0149b29d8b769262a3ea8c06df7c5a01bc2f0c217867`

Before judging Stage 4, I directly hashed the generation-time producers:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

Both values match `source-manifest.json` and the corresponding fields in
`generator-manifest.json`. The producer bundle's launcher artifact hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also an exact match. The immutable image ID
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
matches the source manifest, generator provenance, and the image-addressed
producer path in the audit input. The producer authentication gate therefore
passes; there is no infrastructure `AUDIT_ERROR`.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. `prove.sh` selects
`VERIFICATION`; the local closure inside `verification.k` is exactly that
module. The imported `SEMANTIC` module is in frozen `semantic.k`, not a local
module in `verification.k`, so its ordinary language-execution rules are not
inventoried as proof-local extensions.

The frozen `verification.k` hash is
`d98bd4d84086a32ac784bb6ba74dda698dd88675bb7540813af080c191bf47d9`.
The reconstruction found exactly 12 rules, in this order:

| Lines | Named term | Normalized SHA-256 / `source_rule_id` suffix | Independent class |
|---:|---|---|---|
| 12 | `mathFactorial` base | `4693d6ca6703bc51dbce107317481f1d5637de3e02d06be32aac9c2206cdbfab` | `DEFINITION` |
| 13–14 | `mathFactorial` recurrence | `04a0ebb0b1e8cc00795d597fb0aa1244a955aa3e41bb57b132e9bdc64898f8f3` | `DEFINITION` |
| 16 | `mathTriangle` base | `f2d0f185a32e99da59643bc1a42f6a6a4d5919af3442ced79a75392a1f157496` | `DEFINITION` |
| 17–18 | `mathTriangle` recurrence | `784cb109f6bcbdd3194134950639a08722fc9f59f51803eb9148156ec8d8245a` | `DEFINITION` |
| 20–21 | `expectedAt`, even branch | `762d559f800081a629d17fdbddfe8e5c4c5b12a3bfaa70e9266e72627068f1ed` | `DEFINITION` |
| 22–23 | `expectedAt`, odd branch | `9fb06979b21d6172c5b78afc66f98fbe0f8c1d18da0a4e2c238bd38ec341eaa7` | `DEFINITION` |
| 28–29 | `expected` initializer | `9527523183f2b29e742ddd1e173f06c8cb0750d2bbb348255a0a0f2d5881b80b` | `DEFINITION` |
| 31–32 | `expectedCompletion` terminal | `d081096f2795120e7568a1e22fff9bf169faa3935d72f5851ae0c7fc8455ede9` | `DEFINITION` |
| 33–37 | `expectedCompletion`, even step | `dba23e89996b4981ec78def8af8501dac37d6590ae83120d9b2315510b48cbdd` | `DEFINITION` |
| 38–42 | `expectedCompletion`, odd step | `51d5ac90598636dfe1b73b72ccb56d69c3a0829028e66cc398ded33dc29eacf8` | `DEFINITION` |
| 47–60 | `solutionLoop` macro term | `3881924a92eb8019a4666e9158673a5639a0de87a4efb5709666701e7c192dff` | `DEFINITION` |
| 62–70 | `solution` macro term | `76b2f4322bb9dc303ee170b2c2dab5e8672c46e60d2456d89969331e5f2d5b68` | `DEFINITION` |

For every row, `source_rule_id` is exactly `rule-` followed by the reconstructed
normalized hash. The whole canonical inventory hash is
`dd2b2a30dbe254268b8c8164d328afa35d11a8baab4cb1187bcd9ade25c58863`.
It matches the protected Stage 3 manifest.

The comparison is bijective and order-sensitive: both sides have 12 unique
identities; the ordered identity lists and sets match; no rule is omitted,
duplicated, added, reordered, or assigned an unaccounted identity. Full rule
text, spans, hashes, and comparison results are in
`evidence/reconstruct_inventory.out`.

## Independent classification and semantic judgment

The independent counts are:

- `DEFINITION`: 12
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The first ten rules define named mathematical summaries by base equations,
guarded recurrences, or branch equations. The last two define named macro/proof
terms for the exact loop AST and whole program AST. They therefore satisfy the
required `DEFINITION` category. They are not ordinary execution/observation
rules, and none claims to be a separately proved derived rule. No inventory
entry has a `simplification` attribute, so there is no simplification
classification violation.

The definitions also match the frozen source and operational semantics. At the
head of iteration `I`, the relevant state is a product accumulator `F`, a sum
accumulator `T`, and output prefix `L`. The sequential assignment rules in
`semantic.k` evaluate and store `F * I`, then `T + I`; the parity comparison
then appends the updated product on even `I` or the updated sum on odd `I`, and
finally increments `I`. The two `expectedCompletion` step equations perform
exactly those state updates and append exactly the same branch value. Its
terminal equation returns `L` exactly when `I > N`, and `expected(N)` supplies
the program's initial state `(I,F,T,L) = (1,1,0,.List)`.

Thus the recurrence is a genuine execution summary, not a freestanding
mathematical assertion disguised as a definition. `mathFactorial`,
`mathTriangle`, and the parity branches of `expectedAt` correctly define the
factorial/triangular values stated by the HumanEval postcondition. Although
`expectedAt` is not needed by the final K claim, irrelevance does not turn a
named defining equation into a domain lemma. The `solutionLoop` and `solution`
expansions preserve the statement order and expressions in `solution.mpy` and
the source solution.

The protected Stage 3 manifest records the same class for every canonical
identity. There is no mislabeled or omitted relevant domain lemma. In
particular, the genuine domain-lemma set is empty.

## Deterministic Stage 4 generation

I reran the required
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation, ...)` with
`PYTHONPATH=/reference` and the pinned toolchain lock. The direct first attempt
exposed a sandbox PID-namespace mismatch: Lean 4.22 requests
`/proc/<getpid>/exe`, while this shell reports namespace PID 2 against a
different visible `/proc`. I used the recorded narrow `readlink` shim in
`evidence/lean-proc-self-shim.c`, which changes only that exact lookup to
`/proc/self/exe`; it does not change any mounted source, generator, generated
file, or Lean proof behavior.

The rerun returned:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: null
- designated sorry count: 0
- generated trust declaration count: 47
- isolated `lake clean`: exit 0
- isolated `lake build`: exit 0, all 9 build steps successful

The complete returned JSON and command output hashes/tails are in
`evidence/run_preflight.out`; the initial environment failure and adaptation
are in `evidence/preflight-environment.txt`.

I separately recomputed and compared the Stage 4 bindings rather than relying
on preflight's verdict. `input-manifest.json` exactly contains all 12
reconstructed definitions and empty operational, proved-derived, and domain
lists. Its inventory, verification, Stage 1, and Stage 3 hashes all match.
Generator provenance and the pinned toolchain lock match. The obligation-map
hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
the map has exactly:

```json
{
  "obligations": [],
  "source_rules": [],
  "trust_parameters": []
}
```

The independently determined domain set and the generated source-rule set are
therefore the same empty set. Their ordered source-rule/obligation mapping is
an exact empty bijection: there can be no omitted, duplicated, irrelevant,
weakened, or vacuous conjunct. The independently computed expected target is
null, `target_statement` returns null, and the generator manifest, recorded
preflight, export result, and audit input all bind null as the fixed target.
`Klean106F/Lemmas.lean` contains no proposition declaration, and a direct
target scan finds none. No Stage 5 candidate exists. This is precisely the
required shape for a genuinely empty domain set.

## Final judgment

Stage 3 is complete, bijective, correctly ordered, and semantically classified.
Stage 4 is authenticated to the immutable producer image, hash-consistent,
clean-building, and exactly reflects the independently empty domain-lemma set.
Its no-obligations status, lack of target, and lack of Stage 5 proof are
legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
