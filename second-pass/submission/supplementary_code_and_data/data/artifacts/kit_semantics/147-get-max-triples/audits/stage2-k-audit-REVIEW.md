# Independent adversarial audit: 147-get-max-triples

This review treats every candidate artifact and every generation record as
untrusted evidence. All executable checks were performed from reviewer-created
scratch copies under `/tmp/audit-work`; no candidate-compiled definition or
cache was used. The audit followed `using-kit` and the Gate A/B/C procedures in
`validating-proof`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`
- problem: `147-get-max-triples`
- condition: `kit-semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- candidate mount: `/candidate`
- trusted inputs: `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`

The supplied-semantics mount is present, as required for this mode. There is no
mode/mount contradiction.

I read `/audit-campaign-lock.json` and compared its parsed JSON object with the
`audit_campaign` block in `/audit-input.json`. They are exactly equal. Its
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All records required for `pipeline-v3` are present, readable, non-symlinked
regular files or directories of the required kind:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

I independently reproduced every launcher-recorded file hash. The structured
trace contains one 500,627-byte JSONL file with 215 valid JSON records and no
parse failure. Its SHA-256,
`61a3baf27d9e707c673337a266e8df9a331001454dbb0bae259bbfb8642a6e4b`,
matches `generation-result.json`. I read and summarized all declared generation
records. They report one successful 837-second generation invocation, but none
of those success claims is used as proof evidence here.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate `reference-semantics/` and trusted
`/reference/reference-semantics/` have identical recursive path sets, entry
types, and file bytes. Neither tree contains a symlink. There are no missing,
additional, changed, or mistyped entries in the candidate semantics tree. The
candidate's required proof artifacts are present as regular files. Candidate
compiled directories were regarded as untrusted and ignored.

The exact hashes, type checks, independent reviewer tree digests, and commands
are in:

- `/audit-output/evidence/integrity_check.py`
- `/audit-output/evidence/stage1-integrity.log`

Stage 1 result: **PASS**. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a positive integer `n`, form the length-`n` array whose element at
one-based index `i` is `i*i - i + 1`. Return the number of index triples
`i < j < k` whose three array values sum to a multiple of three. The documented
example requires `get_max_triples(5) == 1`.

The trusted canonical implementation directly constructs the array and
enumerates all index triples. The candidate uses the closed form

```text
z = (n + 1) // 3
o = n - z
C(z, 3) + C(o, 3)
```

with each `C(x,3)` expanded as `x*(x-1)*(x-2)//6`.

This is correct on the entire positive-integer domain. Modulo three,
`i*i-i+1` has residue zero exactly when `i` has residue two; otherwise it has
residue one. Thus a triple sum has residue zero exactly when the triple contains
zero or three residue-one elements. There are
`z = floor((n+1)/3)` residue-zero elements and `o = n-z` residue-one elements,
giving exactly `C(z,3)+C(o,3)`. Both populations are nonnegative, and the
product of three consecutive integers is divisible by six.

### Trusted regeneration

From the scratch copy I ran:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited zero. The submitted and regenerated MPY files have the
same SHA-256:
`657ff2583f44dc96442f742ea8e9ff4ae32cdfa589f25c6aacef3e19d99914ce`.
This establishes byte identity with output from the trusted translator.

### Independent differential test

`/audit-output/evidence/differential.py` independently imports the trusted
canonical entry point and the generated entry point. It tested:

- the documented input `5`;
- the empty/domain boundary `0` as an explicitly excluded probe;
- every positive integer from 1 through 18, crossing all `n mod 3` boundaries
  and every `C(x,3)` population threshold;
- 120 deterministic random draws from 1 through 120 using seed 147.

There were 82 unique intended-domain inputs and zero mismatches. Both
implementations returned 1 at `n=5` and 92,040 at the largest sampled input,
`n=120`. At the excluded negative probe `n=-1`, the implementations diverge
(canonical 0, candidate -1); this is not a defect because the prompt and formal
claim both require a positive integer.

The complete input set, commands, statuses, and representative results are in
`/audit-output/evidence/stage2-fidelity-and-differential.log`.

Stage 2 result: **PASS**. The alternative algorithm preserves the source
contract over its full stated domain.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/147-clean-rebuild` from source artifacts only. It
contained no candidate-built definition or cache. K v7.1.293 was available as
`/usr/bin/kompile`, `/usr/bin/krun`, and `/usr/bin/kprove`.

### Fresh concrete definition

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited zero. The compiler reported non-exhaustiveness warnings only for
unused supplied helpers and unused-variable warnings in `str.k`.

Fresh execution:

```bash
krun smoke.mpy --definition audit-runtime-kompiled
```

exited zero with `.K`, exit code zero, clean heap/stack/return/exception cells,
and results `0`, `1`, and `36` for inputs 1, 5, and 10.

### Fresh proof definition and every positive claim

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

The build exited zero. `spec.k` contains exactly one positive claim,
`SPEC.get-max-triples`. Its fresh `kprove` run exited zero and printed `#Top`.
Six non-fatal `DecidePredicateUnknown` diagnostics appeared while builtin
integer equations were considered; they did not leave a residual claim.

Bounded actual output and exact commands are preserved in
`/audit-output/evidence/stage3-clean-reconstruction.log`.

Stage 3 result: **PASS**. Every positive target claim closes in a clean
reconstruction.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `N` is any unbounded K integer with `N > 0`.
- scope 0 binds `get_max_triples` to a closure with one parameter, `n`, and the
  submitted straight-line body;
- that closure's defining scope is 0, whose parent is the fixed builtins scope;
- environment, allocator, heap, stack, return, exception, and exit-code cells
  are the concrete normal caller state shown in `spec.k`.

Postcondition:

- executing `Call(Name("get_max_triples"), Int(N))` returns
  `expectedTriples(N)`;
- the caller environment and every other configuration cell is restored to the
  exact stated value.

There are no helper or loop claims.

### Constructor-level identity

The claim does not begin with the module-loading wrapper. This is acceptable
only if its explicit closure is exactly the binding produced by the submitted
module. I checked that connection independently.

`/audit-output/evidence/pinning_check.py` lexes K constructors, extracts the
`FuncDef("get_max_triples", Params("n"), BODY)` body from regenerated
`solution.mpy`, extracts the `closureVal("n", BODY, 0)` body from `spec.k`, and
compares their token sequences. It also checks that the entry call is exactly
`Call(Name("get_max_triples"), Int(N))`.

The result was:

```text
function_body_tokens=195
entry_call=Call(Name("get_max_triples"), Int(N))
parameter_list=("n") and closure_parent_scope=0
PINNING CHECK PASS exact constructor-token body identity
```

This, combined with trusted byte-identical regeneration, mechanically pins the
claim to the real submitted function binding and body.

### Satisfiable state and ground substitution

`N=4` satisfies the entry precondition. Substitution gives
`zeroResidueCount(4)=1`, so the claimed result is
`C(1,3)+C(3,3)=1`.

A reviewer-authored concrete module containing the identical function body was
translated by the trusted translator and run under the fresh LLVM definition.
For inputs 1, 4, 5, 10, and 120, K returned respectively
`0, 1, 1, 36, 92040`. The trusted canonical and generated Python
implementations returned the same values.

I also created the reviewer body-sensitivity claim
`/audit-output/evidence/audit-spec-body-mutation.k`. It changes the closure term
actually executed by the theorem to `Return(Int(0))`, keeps `N=4`, and leaves
the correct postcondition unchanged. Its dry run exited zero; its proof exited
1 with `WarnStuckClaimState` and residual `<k> 0 ~> .K </k>`. Thus a material
change to the executed program term changes the result and invalidates the
theorem. This does not rely on changing an external source file while leaving
the claimed closure untouched.

Artifacts and results are in:

- `/audit-output/evidence/pinning_check.py`
- `/audit-output/evidence/ground_probe.py`
- `/audit-output/evidence/audit-spec-body-mutation.k`
- `/audit-output/evidence/stage4-pinning-and-ground.log`

Stage 4 result: **PASS**. The theorem executes the real body, has a realizable
precondition, and constrains the returned value rather than a free variable,
tautology, or implication.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/k_inventory.py` enumerates every multiline syntax
declaration, configuration, context, ordinary rule, and claim with source
locations. Its non-summary inventory has 928 records (128,108 bytes). The
supplied tree contains:

- 227 local syntax records;
- one configuration;
- five evaluation contexts;
- 695 ordinary rules;
- 107 records with `total`, 145 with `function`, 45 with priority, 26 with
  `owise`, 35 with `concrete`, and 25 explicit `symbol` declarations.

There are no local `simplification` rules and no `functional` declarations.
The per-file inventory, attribute counts, opaque-symbol list, command, and exit
status are in `/audit-output/evidence/stage5-rule-inventory.log`.

The proof-local inventory is small and exhaustive:

1. `zeroResidueCount(Int) [function, total]` with one unguarded equation.
2. `chooseThree(Int) [function, total]` with one unguarded equation.
3. `expectedTriples(Int) [function, total]` with one unguarded equation.

There are no proof-local operational rewrites, priorities, simplifications,
opaque symbols, concrete rules, or auxiliary claims.

### Construct and execution map

Every constructor used by `solution.mpy` has a declaration and a real
fixed-semantics execution route:

| Program construct | Declaration/behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; the claim uses the exact closure that `functions.k` would bind |
| `Call` | generic callee evaluation and argument evaluation in `call.k` |
| `Name` | scope-chain lookup in `core.k` |
| `Int` | integer literal rule in `core.k` |
| `Assign` | strict RHS followed by current-frame map update in `controls.k` |
| `BinOp` | left-to-right `seqstrict` evaluation, dispatch in `operators.k` |
| integer `+`, `-`, `*`, `//` | `int.k`; `//` uses `pyMod` and exact integer division |
| statement sequence | `core.k` statement sequencing |
| parameter binding/frame | `call.k` and `functions.k` |
| `Return`/frame pop | `functions.k`, restoring caller state |

The generated heat/cool rules from `strict` and `seqstrict` evaluate each
assignment RHS before mutation, both binary operands left-to-right, and the
return expression before frame pop. The claim's exact local map makes ordinary
lookup deterministic. The closure call allocates frame 1, binds `n`, executes
all four assignments and the return, removes the frame, restores environment 0
and scope location 1, and leaves heap, stack, return, exception, and exit code
unchanged.

Potential overlaps were checked:

- cell lookup, cell assignment, and cell-parameter priority rules require a
  `$cells` marker and matching heap cell; the exact plain frame has neither;
- ref-dereference operator priorities require `ref` operands; every operand on
  this path is an `Int`;
- list, string, bool, float, dict, set, and tuple operator equations are
  sort-disjoint from the integer path;
- special `math.*` and `hashlib.md5` call rules require different callee ASTs;
- generic `Call` therefore selects the explicit `get_max_triples` closure;
- division denominators are the nonzero constants 3 and 6, so no modeled
  division-by-zero behavior is invoked.

The remaining inventoried supplied rules are outside the submitted program's
dynamic cone: their head constructors, callee forms, control tokens, iterable
forms, or operand sorts never arise in this claim. `MPY-CONCRETE` is not
imported by the Haskell proof module. The 25 supplied opaque symbols (the float
helpers, sort helpers, and MD5 helper listed in the evidence log) likewise
cannot influence a branch, state cell, return value, or postcondition here.
Thus no conclusion depends on an oracle or an unmodeled used construct.

The LLVM compiler's non-exhaustiveness warnings concern unused helper domains.
There is no satisfying positive-`N` state in which those helper heads arise, so
they supply no false-conclusion witness for this theorem and are not labeled
unsound.

### Proof-local equation validity

- `zeroResidueCount(N)` exactly expands Python `(N+1)//3` for the positive
  divisor 3.
- `chooseThree(X)` exactly expands Python
  `X*(X-1)*(X-2)//6`. Its rule is defined for every integer. On every use in
  the postcondition, `X` is a nonnegative population count.
- `expectedTriples(N)` is the acyclic sum of the two definitions.

Each symbol has one exhaustive equation, so there are no guard gaps or
pairwise overlaps. The definitions are acyclic and terminating. They occur
only on the postcondition side and do not replace or accelerate program
execution. Their mathematical meaning is established by the residue/counting
argument in Stage 2.

Stage 5 result: **PASS**. No local rule encodes an unproved program result,
bypasses execution, fabricates a value, or permits a false conclusion on the
intended domain.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. I created the distinct
reviewer artifact `/audit-output/evidence/audit-spec-false.k`, preserving the
exact entry state and exact function body, fixing the satisfiable witness
`N == 4`, and changing only the result obligation to
`expectedTriples(N) -Int 1`.

The dry run:

```bash
kprove audit-spec-false.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE \
  --dry-run
```

exited zero, proving that the mutation parses and builds.

The actual mutation proof exited 1 with `WarnStuckClaimState`. Its residual had
`<k> 1 ~> .K </k>` and the correct restored state, while the false destination
at `N=4` was 0. The backend failed because the result did not unify with that
destination, not because of parsing, imports, timeout, crash, or an unrelated
stuck computation.

The mutation, exact commands, statuses, and bounded residual are in:

- `/audit-output/evidence/audit-spec-false.k`
- `/audit-output/evidence/stage6-fresh-nonvacuity.log`

Stage 6 result: **PASS**. The proof is meaningfully result-discriminating.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics and K's integer theory, for every unbounded
integer `N > 0`, executing the exact submitted `get_max_triples` body from the
claim's concrete caller state reaches a normal state whose returned K integer is

```text
chooseThree(zeroResidueCount(N))
+ chooseThree(N - zeroResidueCount(N))
```

and restores all modeled caller cells to the exact stated values. This is a
reachability/partial-correctness result. The straight-line program is also
concretely terminating, but termination is not a separate theorem claimed by
`spec.k`.

### Trust and assumption ledger

1. **Supplied MPY semantics.** The proof trusts the fixed supplied semantics as
   the language model. The candidate copy is exactly the trusted tree. The
   complete imported tree was inventoried, and the smaller execution cone used
   here was checked rule by rule. This boundary is acceptable.

2. **K implementation and mathematical hooks.** K v7.1.293, its parser,
   kompiler, Haskell prover, LLVM interpreter, solver, maps/lists, and unbounded
   integer hooks are trusted infrastructure. This is the ordinary
   machine-checked-proof trust base and is acceptable.

3. **Translator.** The trusted `py2mpy.py` is assumed to faithfully
   transliterate the used CPython AST nodes. For this program those nodes are
   only a function definition, assignments, names, integer literals, binary
   arithmetic, and return. Regeneration was byte-identical, and the claim body
   was independently compared at constructor level. This boundary is
   acceptable.

4. **Python/K integer alignment.** Python integers and K `Int` are unbounded;
   the used operations are exact `+`, `-`, `*`, and floor division by positive
   constants. No overflow, floating point, collection, text, exception, or
   implementation-defined behavior is involved. This bridge is acceptable.

5. **Formula-to-contract mathematics.** The residue classification and
   `C(z,3)+C(o,3)` count are reviewed explicitly in Stage 2. This is elementary
   ordinary mathematics, not an opaque result primitive or a circular symbol.
   It is acceptable.

6. **Finite empirical evidence.** Differential and ground tests support source
   fidelity and the formula bridge on their documented finite inputs. They are
   not used in place of the universal K reachability proof or the mathematical
   derivation.

No program-derived value is assumed, no external oracle appears in the proof
theory, and none of the supplied opaque symbols is a dependent of the claim.

### Overall decision

Gate A passes: the real body executes, the proof-local equations are sound,
the result is constrained, and the fresh false obligation is rejected. Gate B
passes: `N > 0` is exactly the source-contract domain and the result formula is
the requested triple count for all such `N`. Gate C passes: all material trust
boundaries and finite evidence are explicit and reproducible.

The reconstructed candidate is therefore a legitimate partial-correctness
proof of the real generated program, with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
