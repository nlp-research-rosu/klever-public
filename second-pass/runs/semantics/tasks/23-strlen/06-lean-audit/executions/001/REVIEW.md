# Independent audit: HumanEval `23-strlen`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. I treated every
mounted candidate/provenance file and prior review as untrusted evidence. I did
not use the selected Stage 2 verdict as authority.

The protected Stage 3 classification is correct. The true `DOMAIN_LEMMA` set
is empty. The selected deterministic Stage 4 result is therefore correctly
`KLEAN_NO_OBLIGATIONS`: its obligation map is genuinely empty, it generates no
target proposition, and there is no Stage 5 candidate or result.

## Producer and immutable-input integrity

I applied the required producer-source gate before judging Stage 4:

| Producer input | Recomputed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | same in source and generator manifests | match |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | same in source and generator manifests | match |

The source manifest and `generator-manifest.json` both bind the immutable
generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
That ID also equals the terminal component of the producer-source path recorded
in `/audit-input.json`. The complete mounted producer bundle recomputes to
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
exactly the audit-input digest. Producer provenance therefore passes; there is
no producer-source infrastructure error.

The signed resolution digest, every Stage 1 per-file hash, the Stage 1 artifact
and export-tree hashes, the discovery-manifest hash, selected Stage 2 and Stage
4 tree hashes, producer-bundle hash, generated-tree hash, obligation-map hash,
trust-inventory hash, selection hashes, and null Lean hashes all recomputed
exactly. The comprehensive result is `all_match: true` in
[20-verify-hashes.txt](evidence/20-verify-hashes.txt).

Key bindings include:

- frozen Stage 1 export:
  `4158b34c9c045c172cf84f2a47fb1a8bae3161d27db736f401c35b55087b7515`;
- protected Stage 3 manifest:
  `d213582596c3126bb308cf663d3ed1f35091ee6d4c3b831c5a9a83b654aad6a0`;
- complete selected Stage 4 artifact:
  `c80a0a7f84e8094368dbb7d2b103b0140f4b74d41312a3197679ca9bd2cc14f9`;
- generated project:
  `f4d38bde7a86668e3f75196e46449385ca7490083d2327483ca1a95c9d88b5b4`.

## Canonical rule-inventory reconstruction

I reconstructed the local closure of the main module selected by the frozen
`prove.sh` using the trusted `tools.k_rule_inventory.inventory_verification`
implementation. The selected module is `VERIFICATION`; its local module closure
is exactly `["VERIFICATION"]`.

The frozen `verification.k` hash is
`37917325874ac23f2318e7e0c2d207cefa3014e131581b2f7f839c0fe61d5da0`.
The canonical whole-inventory hash independently recomputes to
`5fb2cd8fbac239a2c3b33e986d119eee9233d58f66404e269a981b9627f2ad37`.

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Attributes | Independent class |
|---|---|---|---|---|
| 1 | lines 8–15 | `b71ea096f6e92dea97adefa58c521bb4aab0f25d49e84fa784b5a0cb3ceee82d` / `rule-b71ea096f6e92dea97adefa58c521bb4aab0f25d49e84fa784b5a0cb3ceee82d` | none | `DEFINITION` |
| 2 | lines 19–20 | `b40bd3d53d30e1797dff4bda42d1500c65a0af4579226f8b93f6d759be42af3f` / `rule-b40bd3d53d30e1797dff4bda42d1500c65a0af4579226f8b93f6d759be42af3f` | none | `OPERATIONAL_RULE` |

For both rules, the reconstructed physical span equals the extracted rule text,
the normalized text independently hashes to the recorded normalized hash, and
the `source_rule_id` is exactly `rule-<normalized_sha256>`.

The protected Stage 3 manifest contains those two identities exactly once and
in that exact order. There are no omitted, duplicated, extra, or reordered
identities, no changed hashes, and no unclassified inventory entries. The
trusted Stage 3 structural validator also accepts the same reconstruction.
Full reconstructed records and checks are in
[21-reconstruct-inventory.txt](evidence/21-reconstruct-inventory.txt).

## Independent classification judgment

### Rule 1: `DEFINITION`

`strlenModule` is declared as a named `Module` macro. Its rule expands that
name to:

`Module(FuncDef("strlen", Params("string"), Return(Call(Name("len"), Name("string")))))`.

After removing layout only, this is exactly the frozen `solution.mpy`
constructor tree translated from `def strlen(string): return len(string)`.
The rule therefore defines a named macro/proof term and adds no mathematical
fact. `DEFINITION` is the required class.

### Rule 2: `OPERATIONAL_RULE`

The second rule is a normal `<k>`-cell harness transition:

`#invokeStrlen(V)` becomes
`#loadAll(strlenModule) ~> Call(Name("strlen"), V)`.

It does not rewrite to `isLen(V)`, assume the postcondition, summarize the
return value, or skip the program body. Under the supplied semantics:

1. `#loadAll(Module(SS))` exposes the actual module statements;
2. `FuncDef` installs the exact body as a closure;
3. ordinary call routing evaluates the named callee and argument;
4. closure dispatch binds `V` and executes the body;
5. normal name lookup resolves `len` in `builtinsScope`; and
6. builtin `len` maps `str(IS)` to `seqLen(str(IS))`, then to `isLen(IS)`.

The spec starts from this exact harness operation and asks for
`isLen(S)`, whose base and recursive equations are already part of the supplied
operational semantics. Thus this verification-local rule is an ordinary,
source-relevant execution rule, not a domain lemma or execution-bypassing
bridge.

Neither inventory rule has `simplification`, so the simplification-class
restriction is satisfied. There are no locally claimed
`PROVED_DERIVED_LEMMA` entries, so the required “prove first without the rule,
use later” protocol is not claimed or needed. There are no mathematical
proof-local rules to classify as `DOMAIN_LEMMA`.

The source/semantics facts supporting this judgment are in
[37-classification-checks.txt](evidence/37-classification-checks.txt), with raw
source and operational-semantics excerpts in evidence files 17–25.

Independent true domain set:

`[]`

## Deterministic Stage 4 generation

I reran exactly
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and:

- frozen input `/reference/k-proof`;
- discovery manifest `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`; and
- lock `/reference/klean-toolchain.lock.json`.

The audit sandbox initially denied the Lean/Lake launchers access to
`/proc/self/exe`, causing installation-discovery failures before project
evaluation. I documented those failed attempts. A narrow preload shim answered
only `/proc/*/exe` from the same process's kernel-provided `AT_EXECFN`; it did
not modify Lean, Lake, the generated tree, imports, declarations, or build
behavior. The shim source, compiler version, and source/binary hashes are
preserved in evidence.

With the pinned Lean 4.22.0 toolchain activated, the trusted preflight returned:

- `lake clean`: exit `0`, empty output,
  SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit `0`, “Build completed successfully,” output SHA-256
  `61bee7477aa44cefef9532b890613629531883ee8376ee99ad608954bf726daf`;
- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`; and
- trust-declaration count `47`.

Those results and output hashes exactly reproduce the recorded preflight. The
complete commands, full build output, exit codes, and returned JSON are in
[31-preflight-rerun-success.txt](evidence/31-preflight-rerun-success.txt).

## Obligation bijection and fixed target

The independent classification partitions the ordered inventory as:

- definitions: `[rule-b71e…e82d]`;
- operational rules: `[rule-b40b…af3f]`;
- proved derived lemmas: `[]`;
- domain lemmas: `[]`.

`input-manifest.json` contains exactly that partition. The generated
`obligation-map.json` contains:

```json
{
  "source_rules": [],
  "obligations": [],
  "trust_parameters": []
}
```

Therefore source rules and obligations are bijective over the true empty domain
set. There are no omissions, duplicates, irrelevant obligations, weakened
equations, or vacuous `True` conjuncts.

The expected generated target for an empty obligation map is no target.
Independently:

- the generator manifest, export result, recorded/rerun preflight, and audit
  input all bind the target to `null`;
- the trusted target parser returns `None`;
- a direct scan finds zero `def targetStatement` declarations;
- the generated `Lemmas.lean` namespace contains no proposition; and
- no generated file references `Proof.final`.

All independent bijection and target checks pass in
[36-verify-bijection-and-target.txt](evidence/36-verify-bijection-and-target.txt).
The generic generated project contains 47 allowlisted executable Klean boundary
axioms, but preflight finds no proposition-valued trust declaration and there
is no target theorem for them to prove in this mode.

## Stage 5

Stage 5 is correctly absent. `AUDIT_MODE` and the signed resolution both say
`CLASSIFICATION_ONLY`; Lean workspace/invocation hashes and `stage5_result` are
null; the generated target is absent; and `/candidate` contains no files.
Consequently no candidate clean build, `#print axioms Proof.final`, proof
identity, or operational-parameter bridge audit applies.

## Evidence index

Exact audit commands are recorded in
[COMMANDS.md](evidence/COMMANDS.md). The most relevant raw results are:

- producer and manifest evidence: files 06–12;
- complete immutable-hash recomputation: files 15 and 20;
- inventory reconstruction: files 17 and 21;
- operational-semantics classification evidence: files 18–25 and 37;
- preflight attempts and successful rerun: files 27–31 and 39;
- obligation map, target scan, trust inventory, and independent bijection:
  files 32–36.

VERDICT: PASS
LEGITIMACY: LEGIT
