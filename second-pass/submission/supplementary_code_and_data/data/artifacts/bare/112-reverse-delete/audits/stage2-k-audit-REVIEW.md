# Independent adversarial review: 112-reverse-delete

The candidate is **not a legitimate partial-correctness proof of the HumanEval
program**. Freshly reconstructed K proofs do close, the submitted Python
implementation is correct, and the proof term is mechanically pinned to the
submitted translation. Those facts do not rescue the proof: the generated
semantics uses a task-specific rule that replaces the entire loop by the same
`deleteChars` summary used in the postcondition, without a bridge-free
connection theorem, and that rule is false over its admitted context. The
generated string semantics also operates on encoded bytes where Python operates
on Unicode code points. Fresh concrete execution gives wrong results for the
actual submitted program on unrestricted, in-contract Python strings.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `112-reverse-delete`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- container paths for all mounted inputs.

All launcher-required records for this layout are readable regular files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the one structured JSONL
trace. The trace has 155 valid JSON records, 24 paired custom tool calls and
outputs, one paired function call and output, and no unmatched call IDs.
Historical `runtime-metrics.json` is not required by this legacy-selected
layout.

The campaign block in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`; the independently computed lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded hash. Every recorded direct-file SHA-256 checked in
`audit-input.json` matches, including the run, task, result, invocation,
metrics, usage, generation prompt/output/last-response, canonical, prompt, and
translator files.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. There are no symlinks under
the candidate, generation-evidence, or reference mounts. An independent
pipeline tree digest of `/candidate` is
`f2b6b617e1144cf484f18c102dd3718b38682f600807b602f5e5716df5b4042c`,
matching the retained-workspace digest in the invocation record. The
independently computed trace-tree digest is
`03517b41ad8aa004530f465a911e4714141a40ef9f5a4ac2056bc14b72a3f077`,
matching `usage.json`.

The generated-semantics boundary is correct:
`/reference/reference-semantics` does not exist. I did not search for or use a
hidden semantics. There is no infrastructure breach.

Evidence:

- `evidence/01-provenance.log`
- `evidence/check_provenance.py`
- `evidence/01-generation-trace-summary.log`
- `evidence/summarize_generation_trace.py`

The generation records claim prior `#Top` executions and tests. I treated those
only as untrusted historical claims; none is used as proof evidence below.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For arbitrary Python strings `s` and `c`, delete from `s`, without reordering
the remaining characters, every character that occurs anywhere in `c`. Return
the pair `(filtered, is_palindrome)`, where `is_palindrome` is true exactly when
`filtered == filtered[::-1]`. The trusted prompt states no ASCII, byte, length,
or finite-alphabet restriction.

`/candidate/solution.py` implements exactly that contract with a left-to-right
loop. Its behavior agrees with `/reference/canonical.py`, which expresses the
same filter as a comprehension. This is a different implementation style but
not a fidelity defect.

The trusted translator was run on the scratch copy:

```text
python3 /tmp/audit-work/112-reverse-delete/trusted-py2mpy.py \
  /tmp/audit-work/112-reverse-delete/solution.py \
  > /tmp/audit-work/112-reverse-delete/regenerated-solution.mpy
```

The regenerated and submitted `solution.mpy` files are byte-identical. Both
have SHA-256
`f000e03ceb98957592a0d397f7e51aad729823b556ab7fdfb749b5fb8defc28e`.
See `evidence/02-translation-fidelity.log`.

The independent differential test imports the trusted canonical and candidate
entry points under distinct module names. It covers all three examples, empty
strings, both outcomes of the membership branch, all/none removed, duplicate
deletion characters, palindrome/non-palindrome outcomes, whitespace, NUL,
newlines, combining characters, non-BMP characters, all 1,905 combinations
over `s ∈ {a,b}^{0..6}` and `c ∈ {a,b}^{0..3}`, and 1,000 deterministic
generated Unicode-containing cases. All 2,924 cases agree.

Evidence:

- `evidence/differential_test.py`
- `evidence/02-differential.log` (exit 0, zero mismatches)

Thus the Python implementation is faithful. The failure is in the generated K
semantics and proof theory, not in `solution.py`.

## 3. Clean proof reconstruction

Only source files were copied to
`/tmp/audit-work/112-reverse-delete`. No candidate kompiled definition or cache
was reused. The installed tools report K version 7.1.293.

Fresh builds:

| Purpose | Command | Status |
|---|---|---:|
| Concrete definition | `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition audit-semantic-llvm-kompiled` | 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 |

Build logs are `evidence/03-kompile-llvm.log` and
`evidence/03-kompile-haskell.log`.

I copied each of the four positive claims into a distinct reviewer spec module
and ran it independently. Each command exited 0 and printed exactly `#Top`:

| Claim | Evidence |
|---|---|
| Arbitrary `S:String, C:String` | `evidence/03-kprove-universal.log` |
| Prompt example 1 | `evidence/03-kprove-example-1.log` |
| Prompt example 2 | `evidence/03-kprove-example-2.log` |
| Prompt example 3 | `evidence/03-kprove-example-3.log` |

The corresponding reviewer specs are
`evidence/audit-spec-universal.k` and
`evidence/audit-spec-example-1.k`,
`evidence/audit-spec-example-2.k`, and
`evidence/audit-spec-example-3.k`.

### Fresh generated-semantics execution

Fresh LLVM execution agrees with Python for the ASCII prompt and boundary
cases, but fails on unrestricted Python strings:

| `s`, `c` | Python result | Fresh `krun` result |
|---|---|---|
| `"abcde"`, `"ae"` | `("bcd", False)` | `("bcd", false)` |
| `""`, `""` | `("", True)` | `("", true)` |
| `"abac"`, `"a"` | `("bc", False)` | `("bc", false)` |
| `"😀a😀"`, `"a"` | `("😀😀", True)` | encoded `"\xf0\x9f\x98\x80\xf0\x9f\x98\x80"`, `false` |
| `"😀"`, `"ð"` | `("😀", True)` | corrupted `"\x9f\x98\x80"`, `false` |

The first Unicode witness shows that `reverseString` reverses encoded bytes,
not Python code points. The second shows that the loop summary deletes one byte
of a non-BMP character merely because that byte is also the K representation
of a different Python character. Both inputs satisfy the unrestricted source
contract, and both Python implementations return the result shown in
`evidence/02-differential.log`.

Exact K commands, exit statuses, and outputs are in
`evidence/03-concrete-semantics-expanded.log`; the executable test is
`evidence/concrete_semantics_test.sh`. The nonzero test status counts the two
observed semantic mismatches, not an infrastructure failure.

Stage 3 conclusion: positive K closure reconstructs, but fresh concrete
reconstruction disproves the required generated-semantics-to-Python bridge.

## 4. Adequacy and real-program pinning

### Claims in plain language

`/candidate/spec.k` has no `requires` clause on any claim.

1. The universal claim starts from a `<k>` cell containing
   `execute(solutionPgm, S, C)` for arbitrary K strings. It requires the final
   cell to be exactly `returned(expectedResult(S,C))`.
2. The next three claims fix the inputs to the prompt examples and require the
   exact ground tuples `("bcd", false)`, `("acdef", false)`, and
   `("cdedc", true)`.

These are result-constraining postconditions, not free right-hand variables or
one-way implications. Realizable starting states include:

- `<k> execute(solutionPgm, "", "") </k>` for the universal claim;
- each of the three exact example left-hand configurations for its example
  claim.

The one-cell configuration in `semantic.k` has no hidden precondition cell that
could make these states inconsistent.

### Mechanical program identity

The reviewer script extracts the ground `Module(...)` right-hand side of
`solutionPgm`, parses it and submitted `solution.mpy` with the freshly built K
parser, normalizes only K's explicit `.Stmts` unit to the empty
`List{Stmt,""}` program spelling, and compares the complete JSON KASTs. Both
KASTs have SHA-256
`fdb2462a0b61634dd7eebf0b11d0f1b4c5e37e397d555f99cd168e6ada725bc0`.
The comparison is true.

Evidence:

- `evidence/compare_program_terms.py`
- `evidence/04-program-term-pinning.log`

Thus the theorem names the same function binding and body as the trusted
translation. The defect is not a stale or substituted `solutionPgm`.

A separate body-sensitivity experiment changes the initial result literal in
the term actually executed by the claim from `""` to `"X"`. The mutated
definition builds, but the universal proof exits 1 with a stuck residual
requiring `"X" +String deleteChars(S,C)` to equal `deleteChars(S,C)`.
Evidence is in `evidence/verification-body-mutated.k`,
`evidence/audit-spec-body-mutated.k`,
`evidence/04-body-mutation-kompile.log`, and
`evidence/04-body-mutation-kprove.log`.

### Concrete substitution

For `S="abcde", C="ae"`, the claimed K result, candidate Python result, and
canonical result all agree. For `S="😀a😀", C="a"`, the universal K claim
specializes to a false palindrome flag while both Python implementations return
true. For `S="😀", C="ð"`, K specializes to a corrupted byte sequence while
both Python implementations retain the emoji. Therefore the formal claim does
not cover the real source-contract domain.

Although the constructor term is pinned, not every material operation in that
term executes: the entire `For` node, its `If`, membership comparison, and
concatenating assignment are consumed by one summary rule at
`semantic.k:115-127`. This is an execution-pinning failure, analyzed next.

## 5. Rule-by-rule static soundness review

The exact numbered sources and declaration index are preserved in
`evidence/05-k-sources-numbered.log` and
`evidence/05-declaration-index.log`. There are no generated helper K files.

### Complete local declaration inventory

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: the empty-separated list of `Stmt`;
- `Stmt`: `FuncDef`, `Assign`, `For`, `If`, and `Return`;
- `Strings`: comma-separated `String`; `Params(Strings)`;
- `Expr`: `Name`, `Str`, `Int`, `UnaryOp`, `BinOp`, `Compare`,
  `TupleExpr`, and `Subscript`;
- `CmpOp`; comma-separated `CmpOps`; comma-separated `Exprs`;
- `Index`: `Expr` or `Slice(Bound,Bound,Bound)`;
- `Bound`: `Expr` or `NoBound`.

`SEMANTIC` declares:

- values `strVal`, `boolVal`, and binary `tupleVal`;
- execution results `normal(Map)` and `returned(Val)`;
- the sole configuration `<k> execute($PGM,$S,$C) </k>`;
- `execute(Pgm,String,String)`;
- seven `[function]` symbols: `exec`, `eval`, `getVal`, `asString`,
  `asBool`, `deleteChars`, and `reverseString`.

`VERIFICATION` adds two `[function]` symbols, `solutionPgm` and
`expectedResult`.

There are no local `[total]` or `[functional]` declarations, no opaque local
symbols, no priority rules, and exactly one `[simplification]` rule. Imported
hooked primitives are accounted for in Stage 7.

### Complete rule inventory and judgment

| Location / rule | Classification and judgment |
|---|---|
| `semantic.k:62 getVal` | Partial map lookup. Unique maps make matching values agree. Sound for present keys; missing keys remain visibly stuck. |
| `:63 asString` | Partial projection from `strVal`; sound. |
| `:64 asBool` | Partial projection from `boolVal`; sound. |
| `:68 "" +String S => S` | The sole simplification. True for K string concatenation and non-overlapping. |
| `:70 deleteChars("",_)` | Byte-filter base case; true in the K byte model. |
| `:71-74 deleteChars`, found branch | Drops the leading K string unit when `findString` reports it in `C`. Guard is disjoint from the next rule and recursion decreases `lengthString`. True as byte filtering, not by itself a Python-code-point theorem. |
| `:75-79 deleteChars`, absent branch | Retains the leading unit. Together with the preceding rule covers nonempty K strings. Same byte-model limitation. |
| `:81 reverseString("")` | Byte-reversal base case; sound in that model. |
| `:82-85 reverseString`, nonempty | Moves the first K byte to the end and decreases length. Sound as byte reversal, not as Python Unicode reversal. |
| `:87 eval(Name)` | Delegates to the partial map lookup; sound for actual bound names. |
| `:88 eval(Str)` | Wraps the K token; sound for the submitted empty literal. It supplies no theorem relating arbitrary K bytes to Python Unicode. |
| `:89-90 eval(BinOp("+"))` | String concatenation of recursively evaluated operands. Pure actual operands avoid evaluation-order concerns. |
| `:91-93 eval("not in")` | K byte-substring membership. It is not exercised by the submitted program because the `For` bridge consumes its enclosing syntax. It would not be an adequate Unicode-character rule. |
| `:94-95 eval("==")` | K byte-string equality; mathematically sound for its operands. |
| `:96-97 eval(TupleExpr)` | Pair construction; sound for the binary tuple used here. |
| `:98-99 eval(Subscript(...[::-1]))` | **Unsound Python bridge.** It identifies Python code-point reversal with `reverseString`'s byte reversal. False-conclusion witness: the actual submitted program on `s="😀a😀", c="a"` returns palindrome `false` in K but `True` in Python. See `evidence/03-concrete-semantics-expanded.log`. |
| `:101 exec(.Stmts)` | Correct normal termination of an empty statement list. |
| `:102-103 exec(Assign)` | Evaluates in the old environment and then updates a name; sound for used pure assignments. |
| `:104-106 exec(If true)` | Executes the then list before the suffix. |
| `:107-109 exec(If false)` | Complementary false guard executes else before suffix. The two Boolean guards are disjoint and covering when condition evaluation yields a Boolean. |
| `:110 exec(Return)` | Returns the evaluated value and discards the local suffix, matching abrupt function return for this fragment. |
| `:115-127 exec(For...)` | **Unsound, answer-bearing operational bridge.** It matches the complete task loop plus arbitrary `REST` and any environment, skips iteration, branch evaluation, concatenation, and loop-variable writes, and installs `deleteChars` directly. No bridge-free universal connection theorem exists. Its result is circularly reused by `expectedResult`. Concrete false-conclusion witnesses are below. |
| `:129-136 execute` | Tailored entry bridge matching exactly the function name and parameters and executing its `BODY` with `s,c` bound. Acceptable for the single submitted module; no source `Call` node or other module action is present. |
| `verification.k:14-31 solutionPgm` | Ground definitional constant. Mechanically equal to submitted `solution.mpy`; sound. |
| `verification.k:34-38 expectedResult` | Definitional summary of the K byte-level result. The equation is non-overlapping, but it is not a proof that this summary has Python's Unicode meaning. Its use of the same `deleteChars` term introduced by the loop bridge makes the positive proof circular as a real-program correctness argument. |

### Concrete false-conclusion witness for the `For` rule

The `For` rule admits arbitrary `REST` and preserves the environment except for
`RVAR`. Python assigns the loop target `CH` on every nonempty iteration; the K
rule never does. The reviewer witness uses the same loop shape, first binds
`ch = "OLD"`, runs it with `s="a", c=""`, and returns `ch`.

- Python returns `"a"`.
- Fresh K execution returns `"OLD"`.

The K execution exits normally, so this is a wrong observable result rather
than a parser error, timeout, or merely stuck term. Artifacts:

- `evidence/for_bridge_context_witness.mpy`
- `evidence/for_bridge_context_oracle.py`
- `evidence/run_for_bridge_context_witness.sh`
- `evidence/05-for-bridge-context-witness.log`

On the actual submitted program, the same `For` bridge is false on
`s="😀", c="ð"`: Python keeps the emoji, while K deletes its leading encoded
byte and returns `"\x9f\x98\x80"`. This second witness is on the exact program
term and exact source-contract input domain.

### Construct coverage and control/state review

Every constructor in `solution.mpy` has syntax. `Module`, `FuncDef`, and
`Params` are consumed by the entry rule. Initial `Assign`, final `Return`,
`TupleExpr`, `Name`, equality, `Subscript`, `Slice`, `NoBound`, `UnaryOp`, and
`Int` are consumed by their listed rules or the exact slice pattern. `Int` and
`UnaryOp` have no general evaluation rule, but the only submitted occurrences
are syntactically consumed by the exact `[::-1]` rule; unused general coverage
is not required in generated-semantics mode.

The submitted `For`, inner `If`, `"not in"` comparison, and `BinOp("+")`
have syntax and apparent component rules, but those component rules do not run.
The task-specific `For` rule preempts all of them. The actual execution path is:

```text
execute
→ exec(initial Assign)
→ exec(whole-For bridge installing deleteChars)
→ exec(Return)
→ eval tuple/equality/slice using reverseString
```

State is an explicit `Map` argument to `exec`; there is no heap, allocation,
I/O, exception, or call stack cell. Those omissions are acceptable for the
well-typed pure source fragment, but omission of the used loop binding is not.
The `If` guards and `deleteChars` guards are disjoint; no rule priority is
declared. Recursive byte helpers descend by one K string unit. Partial
functions visibly stop on unsupported inputs rather than fabricate a value.

Stage 5 conclusion: both identified unsound rules have concrete false-result
witnesses on satisfiable string inputs. The loop bridge also directly encodes
the task answer and lacks the required independent connection theorem.

## 6. Fresh non-vacuity test

`evidence/audit-spec-vacuity.k` is reviewer-authored. It changes the returned
string obligation from `deleteChars(S,C)` to
`"X" +String deleteChars(S,C)` while retaining the Boolean obligation. The
claim has no precondition; `S=""` and `C=""` are a concrete satisfying witness
for which the mutation is false.

The dry run:

```text
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exits 0 and emits the backend command, establishing successful parsing and
claim construction. The real proof command exits 1 with
`WarnStuckClaimState`; its residual explicitly contains the unmet equality
`"X" +String deleteChars(S,C) #Equals deleteChars(S,C)`.

Evidence:

- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-kprove.log`

The positive theorem is therefore internally result-constraining and
non-vacuous. This does not repair the false semantics used to prove it.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's own `semantic.k`, for all K `String` values `S` and `C`,
the ground constructor program named by `solutionPgm` rewrites to:

```text
returned(
  tupleVal(
    strVal(deleteChars(S,C)),
    boolVal(deleteChars(S,C)
            ==String reverseString(deleteChars(S,C)))))
```

The three ASCII example instances follow under the same theory. This is a
theorem about the tailored K byte-level rewrite theory. It is not a theorem
that Python's loop computes that summary or that Python `[::-1]` has the
candidate's byte-reversal meaning.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 hooked `Map`, `String`, `Int`, and `Bool` primitives: map lookup/update, `+String`, `lengthString`, `substrString`, `findString`, `==String`, integer comparisons, `andBool`, `notBool` | All semantic and proof rules | Acceptable low-level trust boundary for K byte mathematics; it does not supply a Python Unicode bridge. |
| Trusted `py2mpy.py` transliteration | Program identity | Acceptable and checked: trusted regeneration is byte-identical. |
| `solutionPgm` constructor copy | All four claims | Acceptable and mechanically checked at parsed-constructor level. |
| `exec(For...) => ... deleteChars ...` | Universal claim and examples | Illegitimate program-derived abstraction. It replaces used program execution, affects the returned value and environment, has no bridge-free connection theorem, shares its result symbol with the postcondition, and has concrete wrong-result witnesses. |
| `eval([::-1]) => reverseString(...)` | Palindrome component | Illegitimate Python bridge on the unrestricted domain; concrete non-BMP witness disproves it. |
| `expectedResult` means the natural-language contract | Universal claim's human-facing interpretation | Assumed, not proved, and false for non-BMP strings under this semantics. |
| Python differential tests | Candidate implementation versus canonical | Finite but strong support for the source implementation only: 2,924 cases, zero mismatches. It does not validate the K semantics; fresh K differential cases refute that bridge. |
| Generation logs and prior `#Top` | None in this review | Untrusted historical evidence only. |

There are no fresh local opaque symbols beyond the imported hooked primitives,
and no local totality axioms. The decisive assumptions are not benign
abstraction boundaries: they concern used, program-defined operations and the
final observable result.

### Gate and benchmark decision

- Real-program soundness (Kit Gate A): **FAIL**. The task-specific operational
  bridge is false over its matched context and lacks an independent connection
  theorem; Unicode rules give false results for the submitted program.
- Intent adequacy (Kit Gate B): **FAIL**. The proof materially narrows Python's
  unrestricted string contract to a byte-oriented model without stating a
  precondition. Under the benchmark instruction, this is `FAIL / NOT_LEGIT`,
  not a non-fatal concern.
- Evidence auditability (Kit Gate C): the audit artifacts are reproducible, but
  finite evidence cannot repair Gates A or B.

The clean `#Top`, exact program-term pinning, correct Python implementation, and
successful non-vacuity mutation establish that this is not a trivial missing
artifact or tautological claim. They also make the failure precise: the proof
closes only in a materially false, answer-encoding generated semantics rather
than proving partial correctness of the real generated Python program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
