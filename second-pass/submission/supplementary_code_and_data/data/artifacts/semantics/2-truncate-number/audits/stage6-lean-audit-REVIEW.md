# Independent Stage 3/4 audit: `2-truncate-number`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the verified launcher resolution
select `CLASSIFICATION_ONLY`. The absence of `/candidate`, a Lean invocation,
and a Lean workspace is therefore required and was confirmed. Stage 5 proof,
`Proof.final`, axiom accounting, and operational-bridge parameter checks are
not applicable because Stage 4 legitimately generated no target.

I treated the mounted candidate and provenance material as untrusted evidence.
The conclusions below come from fresh hashes, the trusted rule-inventory and
preflight implementations, and independent source/semantics inspection. Raw
commands and their result-file mapping are in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## Producer-source authentication

I hashed the two mounted generation-time producer files before evaluating the
Stage 4 result:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

These values exactly match both `source-manifest.json` and the corresponding
fields in `generator-manifest.json`. The immutable generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest, generator manifest, and the basename of the producer
bundle path bound by `/audit-input.json`. The producer bundle's independently
recomputed pipeline-tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
also exactly the audit-input value. Producer provenance therefore passes; no
infrastructure `AUDIT_ERROR` applies. The raw hash output is
[`evidence/00-launcher-mode-and-producer-sha256.txt`](evidence/00-launcher-mode-and-producer-sha256.txt),
and the three-layer comparison is
[`evidence/22-producer-provenance-comparison.json`](evidence/22-producer-provenance-comparison.json).

## Inventory reconstruction and bijection

Using `/reference/tools/k_rule_inventory.py` through
`inventory_verification(Path("/reference/k-proof"))`, I independently rebuilt
the local verification-module closure of the frozen `verification.k`.

The selected main module is `VERIFICATION`. The local closure contains only
that module; `MPY` is supplied by the required external semantics files and is
not another module declared locally in `verification.k`. The reconstructed
inventory contains exactly one rule:

| Field | Reconstructed value |
|---|---|
| source span | lines 9–12 |
| module | `VERIFICATION` |
| normalized SHA-256 | `9f2dfdab6d05b03a483926083949b77353f4d59ab6455390118d3ed077036f67` |
| source rule ID | `rule-9f2dfdab6d05b03a483926083949b77353f4d59ab6455390118d3ed077036f67` |
| attributes | empty |

The whole ordered inventory hash is
`bbad9df4e70598a94f0400994f8887fa6499ad74a9bcf8b430d656fa4f69683a`.
The `verification.k` file hash is
`475d864095943d4a4025b1229c7eec986c50175458f41514ae14bbffc71eedad`.
The complete reconstruction is saved in
[`evidence/03-reconstructed-rule-inventory.json`](evidence/03-reconstructed-rule-inventory.json).

The protected Stage 3 manifest has the same sole identity in the same order
and the same inventory hash. Revalidating the trust-boundary manifest against
the frozen workspace recovered the same span, text, normalized hash, and
classification record. There are no omitted, duplicated, extra, or reordered
rules and no unaccounted classification. See
[`evidence/23-validated-stage3-trust-boundary.json`](evidence/23-validated-stage3-trust-boundary.json).

## Independent classification judgment

The sole rule is:

```k
rule solutionProgram
  => Module(
       FuncDef("truncate_number", Params("number"),
         Return(BinOp("%", Name("number"), Float(1.0)))))
```

`solutionProgram` is declared immediately above as
`syntax Module ::= "solutionProgram" [macro]`. Its right-hand side matches the
normalized frozen `solution.mpy` AST exactly; that AST in turn directly
represents the source body `return number % 1.0`. The exact comparison is
recorded in
[`evidence/86-definition-source-ast-comparison.json`](evidence/86-definition-source-ast-comparison.json).

The correct classification is `DEFINITION`. It expands a named macro/proof
term into the frozen program AST. It does not match a `<k>` configuration,
change any operational cell, observe execution, or state an independent
mathematical fact. It is consequently neither an `OPERATIONAL_RULE` nor a
`DOMAIN_LEMMA`. It is not a `PROVED_DERIVED_LEMMA`: there is no earlier proof
of it against a module omitting the rule and no later lemma use. The rule has
no `simplification` attribute, so the simplification-category constraint is
also satisfied.

The operational semantics confirms this distinction. After macro expansion,
the supplied rules:

1. unwrap `#loadAll(Module(...))` into the module statements;
2. execute `FuncDef` to bind a `closureVal`;
3. route the call through normal callee lookup, argument evaluation, frame
   allocation, and parameter binding;
4. evaluate `Return(BinOp("%", Name("number"), Float(1.0)))`;
5. dispatch the cooled `BinOp` to `applyBin`; and
6. apply the supplied float operational rule
   `applyBin("%", F1, F2) => floatMod(F1, F2)`.

Those rules are frozen operational semantics, not local proof extensions. The
Stage 1 postcondition returns that same operational `floatMod(N, 1.0)` term.
No local algebraic or domain fact is introduced or needed to close this
execution-summary claim. Thus the independently classified
`DOMAIN_LEMMA` set is genuinely empty. The relevant source extracts are
[`evidence/11-float-semantics-core.txt`](evidence/11-float-semantics-core.txt),
[`evidence/12-operator-dispatch.txt`](evidence/12-operator-dispatch.txt),
[`evidence/13-call-semantics.txt`](evidence/13-call-semantics.txt), and
[`evidence/14-function-semantics.txt`](evidence/14-function-semantics.txt).

## Hash and manifest integrity

I verified the signed audit-input envelope; its canonical resolution digest is
`9e245192f1799ec603525c816da42d58494a8c9bb9fbc514d2de7e71ab27b298`.
All 33 recorded Stage 1 source hashes match, and the mounted workspace has no
unrecorded file. Both hash schemes used by the pipeline were recomputed:

- Stage 1 selected artifact:
  `77be51676234c67d619a6047faa66792615d40a4cff940225acb3818fbabbcff`
- Stage 1 deterministic export:
  `1ad8d725b09173c1329c0bc5024bac76cff3a56baa26ede3f98e59d92a0c1c6c`
- selected Stage 2 artifact:
  `a3956bfef90d2d97058cdbc8cab3b7ad27118d8d47bc4e8a91d96e66beb47c97`
- selected Stage 4 artifact:
  `f582b9a805e4e2c6524ec4b6d57916cab4c028c4335f69ddd045fe3870b05d04`
- generated project tree:
  `f58f07b440b3339214ce2c1dffe74820d004fddb387eb061f55467d689ad6638`
- Stage 3 manifest:
  `af5132d2e92043ff3bddfd71ddbafba1ea8ccb50d780d4e040e2d403e32dcc2d`

These values match the audit input, selections, input manifest, generator
manifest, export result, and recorded preflight wherever each is bound. The
generator toolchain object exactly matches
`/reference/klean-toolchain.lock.json`. The comprehensive field-by-field
report is
[`evidence/84-independent-stage3-stage4-verification.json`](evidence/84-independent-stage3-stage4-verification.json);
all listed checks are `true` and the script exited 0.

## Required preflight rerun

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and
toolchain-lock paths.

The first invocation exposed a sandbox-specific Lean startup issue:
Lean 4.22 constructs `/proc/<getpid()>/exe`, while this audit sandbox exposes
the process executable only through `/proc/self/exe`. This produced
“could not detect the configuration of the Lake installation” before any
project source was compiled. I retained the exact failure in
[`evidence/24-check-generation-output.txt`](evidence/24-check-generation-output.txt).

I then built a narrow compatibility shim
([`evidence/proc_exe_compat.c`](evidence/proc_exe_compat.c)) that changes only
the exact `readlink("/proc/<this namespace PID>/exe", ...)` call to
`/proc/self/exe`. It does not modify the generated project, manifests,
generator code, theorem content, or Lean trust environment. With that shim,
the pinned toolchain reports Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The unchanged trusted checker then exited 0 and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- unchanged Stage 1, Stage 3, and generated-tree hashes;
- `lake clean` exit 0; and
- `lake build` exit 0 with “Build completed successfully.”

The complete returned evidence is
[`evidence/73-check-generation-rerun-output.txt`](evidence/73-check-generation-rerun-output.txt)
and its recorded exit code is
[`evidence/73-check-generation-rerun-exit-code.txt`](evidence/73-check-generation-rerun-exit-code.txt).
The rerun's build-output hash differs from the historical preflight only
because independent modules were printed in a different successful build
order; the generated project hash is unchanged.

## Obligation bijection and fixed target

The generated `obligation-map.json` contains exactly:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

This is the exact source-rule/obligation bijection for the independently empty
domain set. There are no omitted, duplicated, irrelevant, weakened, or
vacuous conjuncts. The obligation-map file hash
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
matches `generator-manifest.json`.

The trusted target parser independently returns `None`, the expected target
definition is `None`, `Lemmas.lean` contains no `targetStatement`, and the
generator manifest, recorded preflight, and audit input all bind the target as
`null`. Therefore Stage 4 made no target change: for a genuinely empty domain
set, no generated target exists. The generated trust inventory reports zero
designated and other sorries. Its 47 generated executable-data axioms have no
proposition target to prove in this mode, and the preflight independently
rejects proposition trust.

The absence of `/candidate`, Lean workspace/invocation hashes, Stage 5 result,
and target parameters is consistent with and required by
`KLEAN_NO_OBLIGATIONS`. No `Proof.final` or operational bridge exists to audit.

## Final judgment

Stage 3 completely and correctly classifies the one local rule as a
definition. The true domain-lemma set is empty. Stage 4 authentically derives
the exact empty obligation set, generates no target, and passes the trusted
structural/build preflight. There is no Stage 5 proof in this
classification-only audit.

VERDICT: PASS
LEGITIMACY: LEGIT
