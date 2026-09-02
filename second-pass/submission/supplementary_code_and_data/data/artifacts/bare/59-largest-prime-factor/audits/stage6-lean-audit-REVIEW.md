# Independent audit: `59-largest-prime-factor`

## Result

The Stage 3 classification is complete and correct, and the selected Stage 4
`KLEAN_NO_OBLIGATIONS` result is legitimate. The launcher selected
`CLASSIFICATION_ONLY`; there is no fixed Lean theorem and no Stage 5 candidate,
so proof, axiom-dependency, and operational-bridge checks on `Proof.final` are
not applicable.

I treated the mounted Stage 1/2/3/4 artifacts, their comments and logs, and the
absence of a candidate only as evidence. I did not rely on the prior Stage 2
review or any earlier verdict.

## Audit mode and immutable inputs

`AUDIT_MODE` and `/audit-input.json` both report
`CLASSIFICATION_ONLY`, condition `bare`, and semantics mode
`GENERATED_SEMANTICS`. The signed resolution verifies with resolved-input hash
`ebeb6057b58ef4f6cd55f8935a27d2d8ad8dfacae4fc94720de0add01aecf8f1`.

Independent hashes matched the launcher:

| Input | Observed and expected SHA-256 |
|---|---|
| Stage 1 pipeline tree | `ba4c8447536b3f27b64485e5aa5c2f7d6faa5413937c936e76ba53320540478e` |
| Stage 1 export tree | `4e6ded552d0150015b52fa2b9783da8d11a2dafcc40de307dcd5c3390fe7d18c` |
| Stage 2 selected audit tree | `eb3d96394dc7320406864ba44d744c0c6ad33c8759469c09dc29d4300f6657bb` |
| Stage 3 manifest file | `85b00c3eb73f3322643b70a38b7b92659b14996f93159775b9f80fcf417960fc` |
| Stage 4 selected generation tree | `723b17fa325e390073aded0417d9506f122c7e59dd453fdbf8acf072c72f9043` |
| Generated Lean project | `2b4e298409c1902084118ac3ca60ab22b677d5d6add358b5402acb092b5ff753` |
| Producer-source bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

Every individual Stage 1 source-file hash also matched
`audit-input.json`. Raw calculations are in
`evidence/01-input-integrity.txt` and
`evidence/16-stage4-independent-checks.txt`.

## Producer-source integrity

I checked the required producer sources before judging Stage 4:

| File | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, generator manifest, and the producer-bundle path
recorded in `/audit-input.json`. The bundle contains exactly the two producer
files and its source manifest. There is no producer-provenance infrastructure
error. See `evidence/00-producer-provenance.txt`.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` implementation
on `/reference/k-proof`, I reconstructed the local verification-module closure
as the single module `VERIFICATION`. `SEMANTIC` is imported from a different
file and is not part of the module closure local to `verification.k`.

The reconstructed `verification.k` hash is
`2d91a75545319527f17616b6820bbf9c9d9420d3824e6fc10b6baae08dae3bf1`.
The canonical whole-inventory hash is
`f715fe7d9395ed053677b2631fd590296b3a715799e4a8c563f12c76b2fed95c`.
Both match Stage 3 and Stage 4 provenance.

The ordered inventory is:

| Pos. | Lines | Normalized SHA-256 / `source_rule_id` | Independent class |
|---:|---:|---|---|
| 1 | 10–11 | `b489aea63970d411594bff613776dd4bfb15b7ac7fe48b33b080c25e1c15104e` / `rule-b489aea63970d411594bff613776dd4bfb15b7ac7fe48b33b080c25e1c15104e` | `DEFINITION` |
| 2 | 12–13 | `9f466ec05d3a0f3d8752ddb1fee638ad7b8dde8cbbbbad9fb7a1ee11ff00da54` / `rule-9f466ec05d3a0f3d8752ddb1fee638ad7b8dde8cbbbbad9fb7a1ee11ff00da54` | `DEFINITION` |
| 3 | 14–15 | `6bcfd228f976749c4488d33cabe64a1899dd5afdd53b74669fbdb7e39f26004b` / `rule-6bcfd228f976749c4488d33cabe64a1899dd5afdd53b74669fbdb7e39f26004b` | `DEFINITION` |
| 4 | 20–27 | `714829c2a43113532931e52647ec59e899cbe92207d6c68dda64aca3e7e4a2d7` / `rule-714829c2a43113532931e52647ec59e899cbe92207d6c68dda64aca3e7e4a2d7` | `DEFINITION` |
| 5 | 30–35 | `1cd257a656a378c8604c9e23fa722fe9b878c2f65050396e8713e5991b93b63f` / `rule-1cd257a656a378c8604c9e23fa722fe9b878c2f65050396e8713e5991b93b63f` | `DEFINITION` |

For every entry I independently recomputed the physical span, normalized text
hash, and `rule-<hash>` identity. The Stage 3 list has exactly the same five
unique identities in the same order. There are no omitted, duplicated, extra,
reordered, or hash-changed rules. See
`evidence/reconstructed-inventory.json`,
`evidence/02-inventory-reconstruction.txt`, and
`evidence/04-inventory-bijection.txt`.

## Independent classification judgment

The first three rules are the guarded base, divisible, and nondivisible
recurrence equations for the explicitly named summary function `lpfSpec`.
They define a recurrence; they do not rewrite a program configuration or assert
a separate number-theory proposition.

The last two rules are macro equations. `factorLoop` expands to the exact
translated `While`/`If` AST, and `solutionModule` expands to the complete
function AST containing initialization, that loop, and `Return`. They are named
proof terms. After macro expansion, the ordinary rules in `semantic.k` execute
the AST through the `<k>`, `<env>`, and `<result>` cells.

The recurrence mirrors the frozen source program: stop when `F*F > N`; while
`F*F <= N`, divide `N` by `F` when `N % F == 0`, otherwise increment `F`.
The macro AST likewise matches `solution.py` and `solution.mpy`. None of these
five rules preempts or replaces ordinary execution. The comment claiming that
the recurrence represents the greatest prime factor is not itself a rule or
lemma.

Therefore:

- all five entries are genuinely `DEFINITION`;
- there are no `OPERATIONAL_RULE` entries;
- there are no `PROVED_DERIVED_LEMMA` entries;
- there are no `DOMAIN_LEMMA` entries; and
- no inventory rule has a `simplification` attribute.

No domain lemma is hidden under another class, and the independently determined
domain set is genuinely empty. The detailed per-rule reasoning is in
`evidence/05-independent-classification.md`.

## Deterministic Stage 4 generation

I reran the required function with the specified inputs:

```text
PYTHONPATH=/reference
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

Lean 4.22 initially could not locate itself because this audit sandbox exposes
an outer PID in `/proc` while `getpid()` returns an inner PID. I diagnosed this
independently and used a narrow preload shim from `/tmp/audit-work` that returns
the numeric PID visible through `/proc/self`; it changes no mounted input or
Lean artifact. The failed environment-only attempts remain in
`evidence/06-preflight-run.txt`, `evidence/08-preflight-rerun.txt`, and
`evidence/11-preflight-success.txt`; the diagnosis and shim hashes are in
`evidence/09-toolchain-probes.txt` through `evidence/13-pid-shim.txt`.

With executable discovery repaired, the trusted check returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean: exit 0, empty output
lake build: exit 0
lake build output SHA-256:
  53b8851de54c855616b864bb5724feecfafb96d2fa28ff07c70d50b267d4179f
```

The complete successful command output and returned evidence are in
`evidence/14-preflight-final.txt`,
`evidence/preflight-return.json`, and
`evidence/preflight-complete-command-results.json`. The rerun result is
byte-for-byte equal as a JSON value to both the recorded Stage 4 preflight and
the launcher-carried preflight result.

I also checked the source/obligation mapping independently:

```text
independent DOMAIN_LEMMA ids = []
validated Stage 3 domain ids = []
input-manifest source ids     = []
obligation-map source ids     = []
generated obligation ids     = []
trust parameters              = []
```

This is an exact ordered empty bijection. Counts are zero in the obligation
map, generator manifest, export result, recorded preflight, and rerun preflight.
The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. There are no conjuncts that could be
irrelevant, weakened, duplicated, or vacuous.

The trusted target extractor returns `null`, and the expected target definition
for the empty map is also `null`. `generator-manifest.json`, both preflight
results, and `/audit-input.json` all record a null target. The generated
`Lemmas.lean` has an empty namespace and no target declaration. Thus no target
statement or target hash exists to change. See
`evidence/15-stage4-artifacts.txt` and
`evidence/16-stage4-independent-checks.txt`.

The generated base contains 48 allowlisted, non-propositional K vocabulary
trust declarations. The preflight matched them exactly to
`trust-inventory.json`, rejected proposition trust and proof holes, and cleanly
built the project. With no target theorem, none forms a proof of an empty or
vacuous proposition.

Finally, the trusted Stage 6 mechanical gate returned `PASS`,
`CLASSIFICATION_ONLY`, `target: null`, `candidate_sha256: null`, and no used
axioms. Its exact result is in `evidence/17-final-mechanical-gate.txt`.

## Stage 5

Stage 5 is correctly absent: `/candidate` does not exist,
`stage5_result`, `lean_workspace`, and `lean_invocation` are null, and there is
no generated target to prove. Consequently there is no `Proof.final`,
candidate clean build, candidate axiom printout, or `target.parameters`
operational bridge to audit. Supplying any Stage 5 proof in this mode would
have contradicted the empty domain set and the launcher mode.

VERDICT: PASS
LEGITIMACY: LEGIT
