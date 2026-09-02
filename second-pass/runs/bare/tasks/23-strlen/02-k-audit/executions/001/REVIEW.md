# Independent adversarial audit: 23-strlen

## Audit conclusion

The candidate has a fresh-reproducible, syntactically pinned, non-vacuous K
reachability proof, but it is **not a legitimate proof of the real Python
program**. Its result-bearing `len` bridge uses K's `lengthString`, which
concretely disagrees with Python `len(str)` on intended Unicode-string inputs.
For the satisfying input `"😀"`, both trusted and candidate Python return `1`;
fresh LLVM and Haskell executions of the submitted generated semantics return
`Int(4)`. The successfully proved postcondition repeats that same K primitive,
so `#Top` proves the wrong semantic model rather than connecting the real
program to the requested result.

This is a material Gate A failure with a concrete false-conclusion witness, not
an infrastructure uncertainty. The required decision is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is absent, as required. I did not search for or
use a hidden semantics. The candidate's `semantic.k` was audited on its own
merits. See [stage1-integrity.log](evidence/stage1-integrity.log).

### Required artifacts

All requested candidate artifacts are present as regular files, with no
required symlink or mistyped entry:

| Artifact | Status |
|---|---|
| `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log` | Present, regular files; read only as untrusted generation claims |
| structured trace | One regular JSONL file under `codex-trace/` |
| `prompt.py`, `py2mpy.py` | Present, regular files |
| `solution.py`, `solution.mpy` | Present, regular files |
| `semantic.k`, `verification.k`, `spec.k`, `prove.sh` | Present, regular files |

The candidate also contains `__pycache__/` and
`verification-kompiled/`. These are additional generated cache/build artifacts,
not source integrity substitutions. They were inventoried and then ignored;
none was copied into or used by the clean reconstruction. No generated helper K
file exists. `PROOF.md` and a candidate vacuity spec are absent, but neither was
a required deliverable for the generation condition.

The candidate prompt is byte-identical to `/reference/prompt.py`
(`18b94c...65a9`), and the candidate translator is byte-identical to
`/reference/py2mpy.py` (`406485...db16`), with `cmp` exit 0 for both. The hashes
claimed by `run-input.json` agree with these observed hashes.

`metrics.json`, `codex-last.txt`, the 1,237,834-byte generation log, and the
251,744-byte structured trace claim an exit-0 successful run and final `#Top`.
The generation log also records numerous intermediate errors. None of those
claims was trusted as proof evidence; all relevant commands were reconstructed.

Exact hashes show that each source used in scratch matches its candidate or
trusted source counterpart. See
[scratch-source-hashes.log](evidence/scratch-source-hashes.log).

**Stage result:** integrity passed; no infrastructure breach and no missing,
changed, mistyped, or symlinked required artifact.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`, the entry
point is `strlen(string: str) -> int`. For every intended Python `str`, it must
return the string's Python length. The documented examples are `strlen("") == 0`
and `strlen("abc") == 3`. The canonical implementation is `return len(string)`,
so the intended Unicode behavior is Python's `len(str)`, not a byte or encoding
length.

Candidate `solution.py` is:

```python
def strlen(string: str) -> int:
    return len(string)
```

It preserves the signature and uses the same result expression as the trusted
canonical implementation. Omitting the docstring has no behavioral effect.

### Trusted retranslation

In scratch, the trusted copied translator was run over the copied
`solution.py`. The regenerated output, scratch submitted output, and original
candidate output all have SHA-256
`508c92dec7b8810291f0fa18ef567c25d5e8f398d62952cff2bd359697d6aebf`;
byte comparison exited 0. See
[stage2_translation_check.sh](evidence/stage2_translation_check.sh) and
[stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

The reviewer-authored [differential_test.py](evidence/differential_test.py)
loads the scratch copies of the trusted canonical module and candidate solution
under distinct module names. It covers:

- both documented examples;
- empty/nonempty and lengths 0, 1, 2, and adjacent larger size boundaries;
- spaces, NUL, newline, quote, and backslash;
- Latin, combining marks, emoji, and the maximum Unicode scalar used in the
  sample alphabet;
- deterministic generated strings at lengths through 127, plus fixed
  255/256-length cases.

There is no control-flow branch in the one-expression algorithm, so there are
no additional algorithmic branch thresholds. All 87 cases matched, including
their independently computed Python lengths (`MISMATCHES=0`, exit 0). See
[stage2-differential.log](evidence/stage2-differential.log).

**Stage result:** the candidate Python program is faithful to the canonical
program on the intended domain, and the submitted MPY artifact is exactly the
trusted translation.

## 3. Clean proof reconstruction

All needed source was copied to `/tmp/audit-work/reconstruction`. Candidate
compiled definitions and caches were neither copied nor referenced. K
v7.1.293 was available independently.

### Fresh builds

| Purpose | Exact command | Exit | Evidence |
|---|---|---:|---|
| Concrete generated semantics | `kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled` | 0 | [stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log) |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-haskell-kompiled` | 0 | [stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log) |

Both definitions were created afresh below scratch.

### Concrete generated-semantics execution

Boundary and ordinary ASCII executions terminated with `.K` and the expected
results:

| Input | Fresh K result | Both Python results | Exact log |
|---|---:|---:|---|
| `""` | 0 | 0 | [stage3-krun-empty.log](evidence/stage3-krun-empty.log) |
| `"a"` | 1 | 1 | [stage3-krun-a.log](evidence/stage3-krun-a.log) |
| `"abc"` | 3 | 3 | [stage3-krun-abc.log](evidence/stage3-krun-abc.log) |

The required generated-semantics comparison fails on Unicode:

| Input | Python/candidate | Fresh K | Mismatch |
|---|---:|---:|---|
| `"é"` | 1 | 1 | no |
| `"😀"` | 1 | 4 | yes |
| `"a😀é"` | 3 | 6 | yes |
| `"e\u0301"` | 2 | 3 | yes |

The seven-case reconstruction script itself exited 0 because every requested
experiment executed; it reports `K_VS_PYTHON_MISMATCHES=3`. See
[stage3_concrete_oracle.py](evidence/stage3_concrete_oracle.py) and
[stage3-concrete-oracle.log](evidence/stage3-concrete-oracle.log). The LLVM
full configuration for `"a😀é"` is in
[stage3-krun-unicode.log](evidence/stage3-krun-unicode.log). Fresh Haskell
concrete executions independently return `4` for `"😀"` and `3` for the
two-code-point combining string; see
[stage3-krun-haskell-unicode.log](evidence/stage3-krun-haskell-unicode.log)
and
[stage3-krun-haskell-combining.log](evidence/stage3-krun-haskell-combining.log).
Passing the emoji through an explicit K `\U0001F600` string escape produces the
same internal string and result `Int(4)`; see
[stage3-krun-unicode-escaped.log](evidence/stage3-krun-unicode-escaped.log).

The observations show that the imported K string representation/length
operation used here is not Python Unicode `str` length. No assumption about the
exact underlying encoding is needed for the counterexample.

### Positive proof target

`spec.k` contains exactly one claim. Independently running

```text
kprove spec.k --definition verification-haskell-kompiled --spec-module SPEC
```

exited 0 and printed exactly `#Top`; see
[stage3-kprove-spec.log](evidence/stage3-kprove-spec.log). Thus proof closure
under the submitted theory is reproducible. It does not cure the concrete
semantic mismatch.

**Stage result:** clean reconstruction and the positive proof command succeed,
but the mandatory real-semantics concrete comparison exposes a material
candidate defect rather than an audit-infrastructure failure.

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry claim has no `requires` side condition. Its structural precondition is
the exact submitted module term followed by
`invoke("strlen", Str(S))`, with empty function and local maps and
`noResult`. Therefore its value domain is every K `String` that can instantiate
`S`; the prompt does not restrict the intended Python input to ASCII.

Its postcondition requires:

- the entire `<k>` computation to be consumed;
- the `strlen` definition to be present in `<functions>`;
- the input to remain bound to `"string"` in `<locals>`;
- `<result>` to be exactly `Int(lengthString(S))`.

The result is not free, existential, tautological, or guarded by a one-way
implication. It is strongly constrained—just to the wrong semantic quantity.

### Real-program identity and helper claims

The normalized MPY term embedded on the claim's left-hand side is byte-for-term
identical to the submitted MPY constructors:

```text
Module(FuncDef("strlen",Params("string"),Return(Call(Name("len"),Name("string")))))
```

[stage4_program_pinning.py](evidence/stage4_program_pinning.py) records this
comparison, one entry claim, and no claim precondition; its run is in
[stage4-program-pinning.log](evidence/stage4-program-pinning.log). There are no
loop or auxiliary claims. The real translated body executes through the
ordinary semantic rules; it is not replaced by a different submitted program.
`strlenPost` in `verification.k` is not referenced by the claim.

### Satisfiable instances and result substitution

Concrete states with `S=""`, `S="abc"`, and `S="😀"` all satisfy the formal
entry shape and execute to completion. Substitution gives:

| S | Claimed/fresh K result | Trusted canonical | Candidate Python |
|---|---:|---:|---:|
| `""` | 0 | 0 | 0 |
| `"abc"` | 3 | 3 | 3 |
| `"😀"` | 4 | 1 | 1 |
| `"e\u0301"` | 3 | 2 | 2 |

The `"😀"` row is a concrete false conclusion about the real generated program:
the claim specialized to that satisfying input fixes result `4`, while the
actual program fixes result `1`.

**Stage result:** syntactic program pinning and non-vacuous result constraint
pass, but semantic/result adequacy fails materially.

## 5. Rule-by-rule static soundness review

The complete reviewer inventory is preserved in
[rule-inventory.md](evidence/rule-inventory.md). No generated helper K files
exist.

### Local syntax, functions, attributes, and opaque symbols

Every local production is inventoried:

| Sort | Productions |
|---|---|
| `Pgm` | `Module(Stmt)` |
| `Stmt` | `FuncDef(String,Params,Stmt)`; `Return(Expr)` |
| `Params` | `Params(String)` |
| `Expr` | `Value`; `Name(String)`; `Call(Expr,Expr)` |
| `Value` | `Str(String)`; `Int(Int)` |
| `KItem` | `invoke(String,Value)`; `callLen`; `finishReturn` |
| `Function` | `function(String,Stmt)` |
| `Result` | `noResult`; `Value` |
| `Bool` in verification | `strlenPost(Value,Value) [function,total]` |

The `<py>` configuration has `<k>`, `<functions>`, `<locals>`, and `<result>`;
every cell participates in execution or the postcondition. There are no local
priorities, `owise` rules, simplification rules, `concrete` rules,
`[functional]` declarations, or fresh/opaque result symbols. The internal
`callLen` and `finishReturn` constructors are control markers, not value
oracles.

The submitted constructors are all modeled:
`Module` by R1, `FuncDef`/`Params` by R2, `Return` by R7/R8, `Call` by R5/R6,
`Name("string")` by R4, and the `Str` input/`Int` output by the harness and R6.
The used defect is therefore wrong semantics, not an unmodeled used construct
silently receiving a fabricated result.

### Ordinary rules

| ID | Rule and state/control effect | Static decision |
|---|---|---|
| R1 | `Module(S) => S`, preserving the `<k>` suffix and all cells | Sound for the used one-statement module. |
| R2 | Consume `FuncDef` and update `<functions>` with its formal/body | Sound for the exact initial empty map and submitted definition. |
| R3 | Look up `invoke(F,V)`, replace it by `BODY`, and replace locals with `P |-> V` | Sound in the claim's fresh top-level single-call state. It is over-broad for nested calls because it has no call stack/restoration; no real submitted execution reaches that context, so this is recorded as a narrower reuse/model gap rather than a separate witnessed false conclusion. |
| R4 | Resolve `Name(X)` by local-map lookup | Sound for reachable `Name("string")`. |
| R5 | Rewrite `Call(Name("len"),E)` to `E ~> callLen` | Evaluation order is correct for the used single argument. It bypasses general binding lookup, but the exact grammar/program cannot shadow or assign `len`, so the selected builtin binding is justified only for this program. Its value correctness depends entirely on R6. |
| R6 | Rewrite `Str(S) ~> callLen` to `Int(lengthString(S))` | **Unsound as a semantics of the used real Python operation over its intended domain.** It is a result-bearing operational bridge, affects the final postcondition, has no universal Python-connection theorem, and admits the concrete `"😀"` false result `4` instead of `1`. |
| R7 | Rewrite `Return(E)` to `E ~> finishReturn` | Correct evaluation order for the submitted single-return body. |
| R8 | Consume `V ~> finishReturn` and write `<result> V` | Correct in the exact top-level context. General return-frame unwinding is outside this minimal grammar; no broader-context soundness is claimed. |

R6 is not merely under-documented. It replaces the real property-bearing
computation, and the exact submitted control path exercises it for every input.
The rule reads no state, writes no state other than the resulting term, and
preserves the continuation; its binding/control footprint is not the problem.
Its value is wrong. The imported `lengthString` appears both in R6 and directly
in the entry postcondition. That repetition is circular as an intent bridge: it
makes the K claim easy to close but does not establish that Python `len` has the
same value. The opposite value is concretely observed on a satisfying intended
input.

### Verification-local function

The only equation is:

```k
rule strlenPost(Str(S), Int(N)) => N ==Int lengthString(S)
```

There is no overlap. As a definition relative to K's primitive, its covered
equation is deterministic. However, the syntax declares the function
`[total]` over `Value × Value`, while the rule covers only `Str × Int`.
`Str × Str`, `Int × Str`, and `Int × Int` are uncovered.

The reviewer ground probe
`strlenPost(Str("x"),Str("y"))` parsed and reached the prover but remained
stuck; `kprove` exited 1 with the unresolved function in the residual. See
[stage5-totality-probe.k](evidence/stage5-totality-probe.k) and
[stage5-totality-probe.log](evidence/stage5-totality-probe.log). This is a
concrete totality-coverage gap. Because `strlenPost` is unused by the entry
claim, it did not cause that claim's false closure; its advertised
Python-postcondition meaning nevertheless inherits R6's Unicode defect.

### Evaluation, state, allocation, calls, guards, and overlaps

The exact submitted path is deterministic:
module load → function-map installation → function lookup/parameter binding →
local lookup → `len` continuation → result construction → return transfer.
Rules preserve ordering via explicit `~>` continuations. Maps are the only
mutable state; there is no heap, allocation, I/O, exception, loop, branch, or
recursion construct in the submitted term. All ordinary rules are unguarded,
and no same-head rule overlaps on the reachable path. The minimal semantics
does not model exceptions or Python's resource bounds, but those omissions are
not used to fabricate an otherwise unavailable path here; R6 directly assigns
the wrong value to a used ordinary case.

**Stage result:** material static soundness failure at R6, with the required
real-input false-conclusion witness. The under-covered unused `[total]` helper is
an additional, narrower theory-quality defect.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. In scratch I created the independent
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), changing only the final
result obligation from:

```text
Int(lengthString(S))
```

to the demonstrably false:

```text
Int(lengthString(S) +Int 1)
```

The original structural precondition remains satisfiable; at `S=""`, execution
returns 0 while the mutated target demands 1.

The dry run:

```text
kprove spec-vacuity-audit.k --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0, proving that the mutation parsed and built successfully. See
[stage6-mutation-dry-run.log](evidence/stage6-mutation-dry-run.log).

The actual proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its relevant residual is exactly:

```text
lengthString(S) +Int 1 #Equals lengthString(S)
```

and its final configuration contains the actually executed
`Int(lengthString(S))`. See
[stage6-mutation-proof.log](evidence/stage6-mutation-proof.log).

**Stage result:** non-vacuity passes. This establishes result sensitivity under
the candidate theory; it does not validate the theory's interpretation of
string length.

## 7. Proven versus assumed accounting

### What is machine-proved

Precisely, under the submitted generated K theory, the exact submitted MPY term
followed by the supplied invocation harness reaches a final configuration, for
symbolic K string `S`, with:

- empty `<k>`;
- the expected stored function definition;
- local binding `"string" |-> Str(S)`;
- result `Int(lengthString(S))`.

The single claim closes with a fresh `#Top`, and the false-result mutation is
rejected. This is a genuine result-constraining K reachability proof of that
K-level statement.

It does **not** prove that `lengthString(S)` equals the real program's
`len(S)` for Python Unicode strings. The only operational connection is R6,
which assumes that conclusion directly and is false on intended inputs.

### Trust and assumption ledger

| Boundary | Dependents | Judgment |
|---|---|---|
| K v7.1.293 prover/compiler and reachability implementation | All build, execution, and proof results | Ordinary accepted machine-checking boundary. |
| Built-in K sequencing, cells, maps, integers, and equality | Control, bindings, helper predicate | Acceptable low-level primitives for this program. |
| K `String` representation/parser | Input representation and `lengthString` | Concerning intent bridge; its observable length differs from CPython Unicode on witnessed inputs. |
| Imported `lengthString` | R6, final result, and `strlenPost` | Acceptable as a primitive describing K strings, but **illegitimate as the unproved replacement for Python `len(str)`** in this theorem. |
| Direct selection of builtin `"len"` rather than general name resolution | R5 and all results | Informally acceptable only for the exact pinned source, which has no shadowing/rebinding construct. |
| Initial invocation harness after module loading | Entry claim | Acceptable explicit modeling of the HumanEval caller; it invokes the exact pinned function. |
| CPython execution of trusted canonical and candidate files | Program-fidelity oracle and false witness | Trusted executable intent evidence; candidate and canonical agree. |
| Trusted `py2mpy.py` | Python-to-MPY identity | Byte identity is established for this artifact; translator semantics beyond transliteration is not treated as a proof of Python behavior. |
| `[total] strlenPost` | No entry-claim dependent | Unjustified/incomplete declaration; ground coverage probe is stuck. |

There are no proof-local lemmas, simplification rules, priority rules, fresh
symbols, or opaque result oracles beyond the imported result-bearing primitive
already identified.

### Empirical evidence and limits

- The 87-case differential test supports candidate-Python equivalence to the
  trusted canonical over those cases only. The source bodies being the same
  gives a direct additional fidelity argument, but the differential test is
  not substituted for the K proof.
- The seven K-versus-Python executions are finite evidence, but a single
  mismatch is enough to refute the universal semantics bridge. Three mismatches
  were observed.
- Fresh `#Top` proves closure only under the submitted theory.
- The mutation establishes proof discrimination only; it cannot repair R6.
- Candidate prose, traces, prior compiled output, and prior `#Top` were not used
  as proof substitutes.

### Gate and decision accounting

| Gate | Result | Reason |
|---|---|---|
| A — real-program soundness | **FAIL** | R6 replaces real Python `len(str)` with a different result-bearing primitive; `"😀"` yields the false result 4 rather than 1. |
| B — intent adequacy | **FAIL** | The formal postcondition states K `lengthString`, not Python Unicode string length over the prompt's unrestricted `str` domain. |
| C — trust/evidence auditability | PASS as evidence accounting | Commands, statuses, artifacts, finite scopes, and assumptions are preserved; auditability cannot rescue Gate A. |

The proof is pinned and non-vacuous but proves a materially incorrect semantics
of a used operation. Under the required decision boundary, that is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
