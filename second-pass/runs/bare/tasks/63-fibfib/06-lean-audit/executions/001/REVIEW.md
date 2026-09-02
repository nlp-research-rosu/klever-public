# Independent Stage 3–4 audit: `63-fibfib`

## Result

This audit passes. The signed launcher mode is `CLASSIFICATION_ONLY` for
condition `bare` and semantics mode `GENERATED_SEMANTICS`. I treated all
mounted candidate and provenance prose, logs, and earlier verdicts as
untrusted evidence and based the decision on the frozen source, trusted
inventory/checker code, freshly recomputed hashes, a fresh preflight run, and
independent semantic analysis.

The independent classification has no `DOMAIN_LEMMA` entries. Consequently,
Stage 4's `KLEAN_NO_OBLIGATIONS` result is mathematically appropriate: the
source-rule set, obligation set, and trust-parameter set are all empty, there
is no generated target, and there is no Stage 5 candidate.

## Launcher binding and producer provenance

`AUDIT_MODE` and `/audit-input.json` both select `CLASSIFICATION_ONLY`.
The signed resolution canonical hash recomputes to
`c46c5470e513c58a9c959078adac98a00185805041457c5adf213a9b2ad64d80`.

The required producer check passed before Stage 4 was judged:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable image identity is
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`
in both manifests and in the basename bound by the
`generation_producer_sources` path in `/audit-input.json`. The producer bundle
tree hash also recomputes to the signed
`7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a`.
There is no producer-source infrastructure error.

## Inventory reconstruction and bijection

Using `/reference/tools/k_rule_inventory.py` with `PYTHONPATH=/reference`, I
reconstructed the local verification-module closure from the frozen
`verification.k`. The selected module is `FIBFIB-VERIFICATION`; its local
closure contains that module and exactly six rules. The frozen
`verification.k` hash is
`43829c5c7945ee6b0c67bca30e73826958e9d2997c09074475e357b68c8d399d`,
and the canonical inventory hash is
`919caef0f333c4387764b07f1f21020fea2ff0c7fdabb6cba717c130722b5aa6`.

| Order | Frozen span | `source_rule_id` / normalized SHA-256 | Independent class |
|---:|---:|---|---|
| 1 | 10–11 | `rule-92253dd9ab88ae194b1d2638b0a0c17e26b902df20bedbcb09621a2f930802c0` | `DEFINITION` |
| 2 | 13–18 | `rule-87907b49a1e48ff956e0b742627a7148aa518a33bba7eac1d04c80d8631b6e85` | `DEFINITION` |
| 3 | 20–28 | `rule-f5d94980a5f4b4791f14aeda0846ffd914363c9b3b8405b4721279a5fe06a214` | `DEFINITION` |
| 4 | 30–30 | `rule-3425aac728465535886194b960352ad925ad62239dda06d66ce4902426355044` | `DEFINITION` |
| 5 | 31–31 | `rule-774b9e1a2aa5194a3d6935d644711d4f1e7e7918cbeef155d600ccb27a1847e8` | `DEFINITION` |
| 6 | 32–35 | `rule-db0cf8be568ec2479314d5f70faeadcdc6500cbd89de5c8b6425b724d6a7fd04` | `DEFINITION` |

For each entry, `source_rule_id` is `rule-` followed by its recomputed
normalized source hash. The explicit comparison checked the ordered identity
list, both sides' uniqueness, rule count, spans, and whole-inventory hash. It
found no omission, duplicate, extra entry, reordered identity, or changed hash.
The trusted Stage 3 boundary validator also passed. Full reconstructed source
text and hashes are in `evidence/05-inventory-reconstruction-and-bijection.txt`
and `evidence/25-explicit-inventory-bijection.txt`.

## Independent classification judgment

The first three rules are definitions of named syntax:

- `loopCondition` expands to the exact translated comparison
  `i < n`.
- `loopBody` expands to the exact translated simultaneous tuple assignment
  `(a,b,c) := (b,c,a+b+c)` followed by `i := i+1`.
- `fibfibProgram` expands to the exact translated function body with initial
  state `(a,b,c,i) = (0,0,1,0)`, the named loop, and `return a`.

These are macros/named proof terms. They do not bypass an operational K rule.
The frozen semantics evaluates tuple right-hand sides through
`tupleSecond`, `tupleThird`, and `tupleStore` before one map update, so the
macro preserves simultaneous assignment rather than introducing a convenient
sequential interpretation.

The final three rules are the definition of the newly introduced summary
function `fibfibMath : Int -> Int`:

- `fibfibMath(N) = 0` for `N <= 1`;
- `fibfibMath(2) = 1`;
- `fibfibMath(N) = fibfibMath(N-1) + fibfibMath(N-2) + fibfibMath(N-3)`
  for `N >= 3`.

Their guards are mutually exclusive and exhaustive over integers. The
recursive branch strictly decreases until a base branch. These rules define a
summary and recurrence; they do not state an independent fact about an
existing symbol and do not replace execution. `fibfibMath` appears in the
postcondition and loop invariant, not in an execution bridge.

The mathematical connection to the frozen program is direct. Let `F` be the
defined summary. Initially `(a,b,c) = (F(0),F(1),F(2))`. If the loop invariant
has `(a,b,c) = (F(i),F(i+1),F(i+2))`, the operational tuple update produces
`(F(i+1),F(i+2),F(i)+F(i+1)+F(i+2)) =
(F(i+1),F(i+2),F(i+3))`, and then increments `i`. For the specification's
`0 <= N`, loop exit therefore returns `a = F(N)`. This also shows that the
summary is relevant to the source program and requested postcondition.

An independently written transition model agreed with the recurrence and
three-component invariant for sampled boundary and representative values.
Changing initial `c` from 1 to 0 or interpreting the tuple update
sequentially produced counterexamples, so the check is body- and
evaluation-order-sensitive. This finite check is supporting evidence; the
classification rests on the symbolic transition argument above.

There are no ordinary operational rules in this verification-module
inventory, no claimed `PROVED_DERIVED_LEMMA`, and no `DOMAIN_LEMMA`.
Inspection of the Stage 1 structure shows no separate proof of any inventory
rule against a module omitting it followed by later reuse. All six inventory
entries have an empty attribute list, so there is no `simplification` rule to
misclassify.

## Hash and manifest integrity

The independent integrity program performed 65 comparisons with zero
failures. Among the recomputed bindings:

- Stage 1 pipeline tree:
  `88fe6f2159111185510bb69a53df1be53714742c15550e135a7944127d23c4d8`;
- Stage 1 export tree:
  `434c438e2c3b51fcd5813edaedd88e305009d1433a312cf94128f4900b37987d`;
- selected Stage 2 tree:
  `36deb71b78091a20120a24a75510313f7602550e7c74fd2eae0c1c432f542eff`;
- selected Stage 4 tree:
  `d729552d099d89360fd7f9407ff9abf01265df6b5083c6f001f72c8d18fc30c5`;
- generated project tree:
  `a1f2df6af129db69420666d0a42c9d872bb6bbd67e0da16e74f5ec03cd8e83ed`;
- Stage 3 manifest:
  `f109d45e119bf13ffb3b9e972c8a62235f3af8d3b966e0e97c98793e9bc3dd59`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `24bcc1ea4dfd31edc47619510dba41b9825bcaea9ee6a5a0e22b4176d510b372`.

Every individual Stage 1 source hash in `/audit-input.json` matched. The
generator toolchain object exactly matched
`/reference/klean-toolchain.lock.json`. The selected artifact hashes, input
manifest, generator provenance, export result, saved preflight, and signed
audit preflight all agreed with freshly observed values.

## Stage 4 obligations and target identity

My independent domain set is empty. This exactly matches:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`;
- every recorded obligation count, which is zero.

Thus the source-rule/obligation mapping is an exact empty bijection. There can
be no omitted, duplicated, weakened, irrelevant, or vacuous conjunct because
there is no true domain lemma and no conjunct.

A scan of every generated Lean source found zero `targetStatement`
declarations. `generator-manifest.json`, the saved preflight, and
`/audit-input.json` all bind the target to `null`. The export status and
selected Stage 4 status are both `KLEAN_NO_OBLIGATIONS`. `/candidate` is
absent, the Stage 5 result is null, and both signed Lean workspace hashes are
null. This is exactly the required fixed generated target state for an empty
domain set.

## Fresh preflight and mechanical gate

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the three required mounted inputs. The first run
exposed an audit-container PID-namespace issue: Lean looked up
`/proc/<getpid()>/exe`, while this sandbox exposes only `/proc/self/exe`.
The failure occurred at `lake clean` before any candidate-dependent judgment.
I recorded it and used a narrowly scoped local `LD_PRELOAD` compatibility shim
that changes only that exact procfs lookup to `/proc/self/exe`; no mounted
input or generated source was modified.

With that environment repair, the same trusted check returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `obligation_count = 0`;
- `target = null`;
- `designated_sorry_count = 0`;
- 43 generated, inventoried trust declarations;
- `lake clean` exit 0;
- `lake build` exit 0 with output hash
  `581fe703d594b747d4c448d87ee05e2460908da667fb1fba19e08511172c0895`.

That build-output hash exactly matches the immutable saved preflight. A final
run of the trusted `klean_final_gate.py` also exited 0 and returned `PASS` in
`CLASSIFICATION_ONLY` mode with a null target and null candidate hash. Its
`semantic_classification` field is intentionally `NOT_EVALUATED`; the
independent semantic classification is the analysis documented above.

Stage 5 proof identity, axiom accounting for `Proof.final`, and operational
bridge parameter definitions are not applicable in this signed mode because
there is no target theorem and no proof candidate. The generated project's
inventoried executable trust declarations do not support any candidate proof
here: there is no generated proposition to prove.

Complete command lines and their corresponding evidence files are indexed in
`evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
