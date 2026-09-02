# Independent Stage 3/4 Audit: `83-starts-one-ends`

## Result

The selected Stage 3 classification and deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` result are correct. The audit mode is
`CLASSIFICATION_ONLY`, so no Stage 5 candidate or Lean proof target is
permitted or present.

This review was made from the frozen sources and trusted mechanical tooling.
The prior Stage 2 review, prior PASS/CONCERNS labels, logs, comments, and
rationales were not treated as authoritative.

## Scope and launcher binding

- Problem: `83-starts-one-ends`
- Condition: `bare`
- Semantics mode: `GENERATED_SEMANTICS`
- Launcher environment: `AUDIT_MODE=CLASSIFICATION_ONLY`
- Signed resolution mode: `CLASSIFICATION_ONLY`
- Signed resolution digest:
  `ccebb7138738146916f6910be862e15646cd16d2bf48f7fe703670bbc551c314`
- `/candidate`: absent
- Recorded Stage 5 result, workspace, and invocation: all null

The signed resolution envelope was independently verified with
`tools.stage6_resolution_contract.verify_audit_input`.

## Generation-producer authentication

The generation-time producer sources were authenticated before judging Stage
4:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`
- Producer bundle tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`
- Immutable generator image:
  `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`

The two file hashes agree exactly with both `source-manifest.json` and
`generator-manifest.json`. The source manifest and generator manifest record
the same image ID. The terminal image key in the producer-source path recorded
by `/audit-input.json` is the same digest, and the independently computed
three-file bundle tree equals the signed launcher hash. There are no extra
producer-bundle files. Thus the producer-source infrastructure gate passes;
there is no producer-related `AUDIT_ERROR`.

Evidence:
[producer hash record](evidence/02-producer-authentication-raw.txt) and
[independent producer check](evidence/06-producer-provenance-check.txt).

## Canonical K rule inventory

The trusted `tools.k_rule_inventory.inventory_verification` reconstruction
selected `VERIFICATION` as the verification module. Its local
verification-file closure is exactly `["VERIFICATION"]`; imported module
`MPY` is in the separately required `semantic.k`, not another local module in
`verification.k`.

- Frozen `verification.k` SHA-256:
  `8f3781f713f22cf18052e8ecab4ae8690904d0ed940bb1c011f6cc26d4ea6f3a`
- Rule count: 6
- Canonical inventory SHA-256:
  `ad364a4d596bee36c7fdfb3e6ff9e70973845dfddfbc96db3a679fa4e8d04b71`

For every rule, I independently sliced the recorded line span from the frozen
file, normalized it with whitespace joining, recomputed SHA-256, reconstructed
`rule-<normalized_sha256>`, and compared the result with the protected Stage 3
entry. The exact ordered inventory is:

1. Line 16,
   `rule-6bfa896627657f1a7db8b47ce47b179a54d8fd758509fe97bf7a3ce73c03de68`,
   `decimalMiddles`.
2. Lines 17–18,
   `rule-900178d8e3d641d23088309b6f97b2e1ba72acc705ca5cef173a811620073c2e`,
   `startsWithOne`.
3. Lines 19–20,
   `rule-5dc8417368bc588fc6a024fbf8fcd66df9d65abff8a26efb5914cc28f7b3afdf`,
   `endsWithOne`.
4. Lines 21–22,
   `rule-e1973b68bd55ec1aee34975f8190d8904f9801ea819c77bc8458834d86548d92`,
   `startsAndEndsWithOne`.
5. Line 24,
   `rule-64e2ba1944740284efdfe861cce87ab814bafe93ef385139684238c5d2c0c9dd`,
   the `qualifyingCount(1)` base case.
6. Lines 25–27,
   `rule-0f5f78a079edc8e1768e03a4620c5a4efb5ed7021a834b19876e366334085298`,
   the guarded `qualifyingCount(N)` equation.

The Stage 3 list has the same six identities in the same order. There are no
missing, duplicate, extra, reordered, or hash-altered rules. Each exact source
span matches the canonical inventory text. All six attribute lists are empty.
The trusted Stage 3 boundary validator also accepts the bijection.

Evidence:
[frozen sources](evidence/07-frozen-sources.txt),
[raw reconstruction and manifest](evidence/08-inventory-and-discovery.txt),
and [span/hash/order check](evidence/10-rule-inventory-bijection.txt).

## Independent semantic classification

I classify all six rules as `DEFINITION`, agreeing with Stage 3.

The five symbols are freshly declared `[function]` summary symbols in
`verification.k` lines 10–14. Each rule supplies a value equation for the
fresh symbol at its head:

- `decimalMiddles(K)` names `10^K` on the nonnegative exponent domain.
- `startsWithOne(N)`, `endsWithOne(N)`, and
  `startsAndEndsWithOne(N)` name the three guarded counting summaries.
- The two `qualifyingCount` rules are the positive-domain base case and
  guarded inclusion–exclusion summary.

These equations do not rewrite a `<k>` computation or any operational cell, so
they are not `OPERATIONAL_RULE`s. They were compiled into the Stage 1
verification module before the claims were proved; there is no earlier,
bridge-free proof of the exact rules followed by later use, so none is a
`PROVED_DERIVED_LEMMA`. They define fresh named summaries rather than assert a
new theorem between already defined operations, so none is a `DOMAIN_LEMMA`.
No rule has a `simplification` attribute, and therefore the simplification
classification restriction is satisfied trivially.

The guards cover every use in the frozen positive-integer specification:
`N = 1` uses the base case; `N > 1` makes `N - 2 >= 0`, which is exactly the
domain required by `decimalMiddles`. Every summary is relevant:
`startsWithOne`, `endsWithOne`, and `startsAndEndsWithOne` feed
`qualifyingCount`, which occurs directly in both result postconditions.

The mathematical meaning also matches the source and operational semantics.
For `N > 1`, the three cardinalities are respectively
`10 * 10^(N-2)`, `9 * 10^(N-2)`, and `10^(N-2)`. Inclusion–exclusion gives
`18 * 10^(N-2)`, exactly the source program's else branch; `N = 1` gives one.
The frozen K semantics evaluates the equality branch, environment lookup,
subtraction, exponentiation, multiplication, and return value directly.

A fresh LLVM `kompile` and independent `krun` calls on a copy under
`/tmp/audit-work` produced results `1`, `18`, `180`, and `18000` for
`N = 1, 2, 3, 5`. Independent brute-force enumeration through six digits
matched both the definitions and source formula. Mutating either count
coefficient, omitting overlap subtraction, or changing the source coefficient
to 17 is rejected already at `N = 2`.

Therefore the independently determined domain-lemma set is genuinely empty:
`{}`.

Evidence:
[fresh operational K run](evidence/44-fresh-operational-k-run.txt) and
[count/counterfactual checks](evidence/42-count-semantics-and-counterfactuals.txt).

## Recorded hashes and immutable sidecars

All hashes in the signed resolution were independently recomputed with the
appropriate trusted hash contract:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, framed pipeline tree | `4cf9af2b4cdea83d5b9a9f604765245f229cf11af575ad7ceb29359eaf42025b` |
| Stage 1 frozen export, Klean tree digest | `6b564879da565a876bb0bfd7bbfc91109fccb3f52ec6900e95ac6caa143faff8` |
| Stage 3 discovery manifest | `40fda1efb9bc1c629d235444e31fcd4eb73676b9ff374fde60278ab11116f376` |
| Selected Stage 2 audit tree | `ba030cc2f2b4cceea8250dd6cf7026ad202288f63bf095d4c73866a175a2aad8` |
| Selected Stage 4 generation tree | `fd978aaf9214da6e8d60dea214fc90333b62b69ebf57059db756d23a97dcd2ba` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `0edb412714cbc2e5ddfe5f9c15a2e9cd62c31d88a8f47d1f003cf6f04b9a7ccb` |

The two recorded Lean Stage 5 tree hashes are null, as required. All ten
per-file Stage 1 source hashes match. The generated obligation map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
the trust inventory hash is
`5a089006c23b3dc30ba35b91b4567f61b0e7dceec472fcca5fdc6d5989cd67b1`.
The generator toolchain object exactly equals the trusted frozen toolchain
lock, including Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

Evidence:
[comprehensive hash and Stage 4 check](evidence/40-all-hashes-stage4-check.txt).

## Trusted Stage 4 preflight

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage
4 generation, and trusted toolchain lock.

The first invocation reached its clean-build phase but the installed Lean
launcher could not locate itself. This was an audit-container PID-namespace
issue: the process reported PID 2 while the mounted `/proc` had no
`/proc/2/exe`; Lean 4.22 resolves its executable specifically through
`/proc/<getpid>/exe`. This initial failure is preserved in
[the first preflight log](evidence/14-check-generation.txt).

I used a narrowly scoped `LD_PRELOAD` shim that changes only
`readlink("/proc/<digits>/exe", ...)` to
`readlink("/proc/self/exe", ...)`. Its source and compiler command are in the
evidence directory. It did not modify any frozen source, manifest, generated
file, or checker. Lean then reported the pinned version and commit, and the
unmodified trusted checker passed. The checker's before/after snapshots also
confirmed all immutable inputs remained unchanged.

The returned evidence is:

- Status: `KLEAN_NO_OBLIGATIONS`
- Obligation count: 0
- Target: null
- Designated sorry count: 0
- Recorded trust declarations: 45
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, all generated modules built successfully

Evidence:
[namespace diagnosis](evidence/36-proc-pid-diagnostic.txt),
[shim build and version test](evidence/37-proc-shim-build-and-test.txt), and
[successful returned preflight evidence](evidence/38-check-generation-rerun.txt).

## Obligation bijection and target identity

The independently classified domain set is empty. The generated
`obligation-map.json` has:

- `source_rules = []`
- `obligations = []`
- `trust_parameters = []`

The input manifest likewise has no source/domain rules, operational rules, or
proved-derived lemmas, while retaining all six definitions. Thus the
source-rule/obligation mapping is an exact empty-to-empty bijection: there is
no omission or duplicate.

The generator manifest, stored preflight result, signed audit input, and direct
`klean_export.target_statement` reconstruction all report target null. A
separate lexical scan found no generated theorem declaration. Obligation counts
are zero in the generator manifest, export result, preflight result, and
obligation map. Consequently there is no obligation that could be irrelevant,
weakened, duplicated, or padded with a vacuous conjunct, and there is no target
whose statement or hash could have changed. `KLEAN_NO_OBLIGATIONS` is a sentinel
result here, not a vacuous proof theorem.

Because this is `CLASSIFICATION_ONLY`, the Stage 5 clean-copy build,
`Proof.final`, axiom printing, candidate target-shadowing checks, and
operational-bridge parameter checks do not apply. Their required absence is
confirmed instead: no target parameters exist and `/candidate` is absent.

## Conclusion

Stage 3 accounts for the entire canonical inventory in exact source order and
classifies every rule according to its real semantic role. The true
domain-lemma set is empty. Stage 4 faithfully maps that empty set to no Lean
obligations and no target, with authenticated generation-time producers,
matching immutable hashes, a passing trusted preflight, and no illicit Stage 5
artifact.

VERDICT: PASS
LEGITIMACY: LEGIT
