# Independent adversarial review: 160-do-algebra

This audit treats every candidate artifact and generation record as untrusted
evidence. I rebuilt both K definitions from mounted source, independently
regenerated the translated program, reran the positive claims, reconstructed
the rule inventory, and created a new false-result mutation. The proof is
legitimate and unbounded over the stated structural input domain. I assign
`CONCERNS / LEGIT`, rather than an unqualified pass, because the supplied
semantics does not model CPython's division-by-zero exception path: concrete
LLVM execution aborts in the integer hook for a valid structural input
containing `// 0`. This does not enable a false normal-result conclusion in
the partial-correctness claim, and it is not a candidate-local rule defect, but
it is a real language-model/trust-boundary limitation.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `160-do-algebra`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the mounted paths used by this review, rather than the host-only provenance
  paths.

The semantics-mode boundary is internally consistent.
`/reference/reference-semantics` is present as a real directory. The candidate
`reference-semantics/` recursively has the same 25 directory/file entries,
entry types, and file bytes as the trusted tree. Neither tree contains a
symlink, and there are no missing or additional candidate semantics entries.
The independently computed pipeline tree digest of each tree is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task manifest.

The campaign lock is a regular file, its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and its parsed object is exactly equal to the `audit_campaign` block in
`/audit-input.json`.

All pipeline-v3 records required by the prompt are present, regular,
non-symlinked, readable, and were inspected:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
  and
- the JSONL trace under `/generation-evidence/codex-trace/`.

Every directly recorded file hash matches the mounted file. The only trace
file matches the per-file digest in `generation-result.json`; all 437 JSONL
records parse. Its independently computed pipeline tree digest is
`32f7f92c984cf412be68c0cd42fa6756647a0c2e5d6c7bae24a0438486cf7764`,
matching `usage.json`. The candidate's independently computed pipeline tree
digest is
`5aac635870b237a41c75dbbadbf8ce8bea9d71f98ddd44e5fa65b4d8d3f21f45`,
matching the generation result's recorded workspace digest. The larger text
log was inspected by command/event and proof-result searches in addition to
the complete structured trace parse. These records were used only to identify
claims to check, not as proof authority.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Their hashes are,
respectively,
`edeaa3bb46a2a49ef15270a996f764af73cfe463c3480bc5bcae8f04332c3620`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The six required proof deliverables are present as regular, nonempty,
non-symlinked candidate files. Candidate-built `runtime-kompiled/` and
`verification-kompiled/` were not used.

Reproducible evidence: `evidence/01_integrity.py` and
`evidence/01_integrity.log` (exit 0).

Stage 1 result: PASS. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `do_algebra(operator, operand)` to form and
evaluate the infix expression whose operands and operators alternate. The
operator list:

- contains at least one element;
- contains only `+`, `-`, `*`, `//`, or `**`;
- has length exactly one less than the operand list.

The operand list contains at least two non-negative integers. There is no
finite length or integer bound in the contract.

The trusted canonical function starts with `str(operand[0])`, then appends
each `operator[i] + str(operand[i + 1])`, and calls `eval`.

The candidate uses a different but equivalent construction on this domain. It
zips all operands with `operator + [""]` and appends
`str(operand[i]) + extended_operator[i]`. Exact length equality makes the
constructed strings identical:

```text
operand[0] operator[0] operand[1] ... operator[n-1] operand[n]
```

The candidate does not mutate either input.

### Trusted translation

In scratch, the exact command

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. `cmp -s solution.regenerated.mpy solution.mpy` exited 0. Both files
have SHA-256
`2394c9fcede9e1ab3623fe3d6cbdf0f2a016de104ef41d8cca67f451fe71d5e3`.
Thus the submitted `solution.mpy` is exactly the trusted translation of the
submitted Python.

### Independent differential execution

`evidence/02_differential.py` imports the trusted canonical and scratch
candidate as separate modules. It compares either returned values or exception
types. Coverage includes:

- the documented example;
- the minimum legal size for every operator;
- zero operands and `// 0`;
- precedence boundaries and right-associative exponentiation;
- a large non-negative integer case;
- all 125 one-operator cases over operands `0..4`; and
- 1,200 seeded generated legal inputs of one to four operators.

Adjacent randomly generated exponent towers were excluded only to keep the
review harness resource-bounded; a dedicated right-associative `**` case was
included. Across 1,337 intended-domain cases there were zero mismatches.
Both Python implementations raised `ZeroDivisionError` on the checked
division-by-zero cases.

Empty and malformed length cases were also recorded. Some differ, such as
`([], [])` producing `IndexError` in the canonical function and `SyntaxError`
in the candidate. Those cases violate the explicit at-least-one-operator and
length requirements, so they do not narrow the intended domain.

Reproducible evidence: `evidence/02_program_fidelity.sh`,
`evidence/02_program_fidelity.log`, and
`evidence/02_differential.py` (exit 0).

Stage 2 result: PASS.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were excluded. Source artifacts
were copied explicitly to `/tmp/audit-work/160-do-algebra`, while the supplied
semantics was copied from the trusted `/reference` mount. The installed K
version is 7.1.293.

### Fresh concrete definition

The reviewer command in `evidence/03a_kompile_llvm.log` built
`audit-runtime-kompiled` from the trusted scratch semantics with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Compiler exhaustiveness and unused-variable warnings are in the
log; none prevented the build.

The independently authored concrete fixture was translated with the trusted
translator and run with the fresh definition. `krun` exited 0 with empty
`<k>`, empty stack, `noRet`, `NoExc`, and exit code 0. Its module scope
contained:

- documented example: `9`;
- minimum `+`: `0`;
- minimum `-`: `-7`;
- minimum `*`: `0`;
- minimum `//`: `2`;
- minimum `**`: `1`;
- precedence case: `14`; and
- right-associated power case: `512`.

See `evidence/fixtures/k_concrete_cases.py` and
`evidence/03b_krun_concrete.log`.

### Fresh proof definition and positive claims

The reviewer command in `evidence/03c_kompile_haskell.log` built
`audit-verification-kompiled` from scratch:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0.

The auxiliary circularity was run individually:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.algebra-loop
```

It exited 0 and printed `#Top`
(`evidence/03d_kprove_algebra_loop.log`).

The entry claim relies on that circularity. Therefore the actual positive
target command loads the complete `SPEC`:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`
(`evidence/03f_kprove_all.log` and `evidence/03_resume_target.log`).
This proves both claims with the loop circularity available to the entry
proof.

For completeness, I also tried
`--claims SPEC.do-algebra` alone. That selector excludes the required
`SPEC.algebra-loop` circularity, so it was interrupted after more than 180
seconds without a result. The same behavior is visible in the generation
trace. This is a diagnostic command, not the target proof command and not a
failed positive claim; the complete `SPEC` is the proper proof unit.
`evidence/03e_kprove_do_algebra.log` records the interruption explicitly.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.algebra-loop` begins exactly at the fixed semantics' loop head:

```text
#loop(zipObj(NUMBERS, OPERATIONS), tuple target, augmentation body)
```

Its precondition says the remaining values are a valid operand/extended-
operator sequence. It claims that loop completion:

- appends exactly the code sequence summarized by
  `runPairCodes(ACC, NUMBERS, OPERATIONS)` to `expression`;
- leaves `oprn` equal to the final paired operand;
- leaves `oprt` equal to the appended empty string; and
- returns to `.K`.

The claim's `For` target and body match the translated function. Fixed rules
perform `#iterNext`, yield a tuple, bind that tuple target, execute the
augmentation, and return through `#loopLbl` to the next loop head. The loop
summary changes only the three loop locals. Its omitted heap, stack, return,
exception, and allocation cells are not touched by this body for valid
integer/string pairs.

`SPEC.do-algebra` starts in the default module configuration, loads the
function, invokes it on arbitrary symbolic list values satisfying the
contract, and executes to an empty computation. Its precondition:

```text
validAlgebraLists(
  OPERANDS,
  OPERATORS ++ [empty-string])
and OPERATORS != empty
```

means, by the audited equations:

- every operand is an integer at least zero;
- every non-final extended operator is one of the five allowed strings;
- the final extended operator is exactly the empty string;
- the two extended sequences have equal nonzero length; and
- the original operator list is nonempty.

This is exactly the prompt domain and has no finite bound.

The postcondition is not a free result. It requires the module binding
`answer` to equal:

```text
evalArith(
  runPairCodes(
    empty-codes,
    OPERANDS,
    OPERATORS ++ [empty-string]))
```

It also constrains the function call to have returned and popped its frame,
with empty stack, `noRet`, `NoExc`, exit code 0, the two expected list
allocations, and heap location 2. The existential function value in the final
module scope is harmless: fixed execution has already loaded and called the
exact closure, and `answer` remains fully constrained.

### Mechanical program identity

`evidence/04_pinning.py` extracts the balanced `FuncDef("do_algebra", ...)`
constructor from trusted-regenerated `solution.mpy` and the entry claim,
normalizes layout outside string literals, and compares the constructor terms.
The 395 normalized bytes are identical. This is a constructor-level
comparison, not reliance on candidate prose.

The spec therefore executes the actual submitted function binding and body.
The claim adds a caller assignment, which is necessary to observe a return
value, but does not substitute the function.

### Satisfying witness and concrete substitution

The documented input

```text
operators = ["+", "*", "-"]
operands  = [2, 3, 4, 5]
```

satisfies every entry precondition. Reviewer-authored reachability checks in
`evidence/04_witness.k` simplify:

- the full `validAlgebraLists` predicate to true;
- the nonempty predicate to true;
- `runPairCodes` to the ASCII codes for `2+3*4-5`; and
- `evalArith` of those codes to 9.

`kprove` printed `#Top` and exited 0. Both trusted canonical Python and
candidate Python also returned 9. See `evidence/04_adequacy.log`.

### Body sensitivity

The candidate-provided body mutation was not trusted as a report; it was run
independently against the fresh reviewer definition. Its actual claim term
changes `Assign(Name("expression"), Str(""))` to `Str("1")` while continuing
to demand the original answer 9. The proof exited 1 with
`WarnStuckClaimState`, and the reachable final scope contains `answer |-> 19`
and the mutated closure body. Thus the check changes the term executed by the
claim, not merely an external source file. See
`evidence/04_body_sensitivity.log`.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_inventory.txt` is a source-located, flattened inventory of every
module/import, configuration, context, syntax declaration, rule, and claim in
the 24 supplied-semantics K files, `verification.k`, and `spec.k`. It includes
source SHA-256 values, attributes such as `function`, `total`, `symbol`,
`no-evaluators`, `priority`, `simplification`, `concrete`, `symbolic`,
`owise`, strictness, and a rule assessment.

Inventory totals are:

| Kind | Count |
|---|---:|
| configuration | 1 |
| syntax declarations | 232 |
| contexts | 5 |
| rules | 721 |
| positive claims | 2 |

The inventory's automated relevance tags are routing aids. I separately read
all source files and manually reviewed the dependency closure of the
submitted program, including helper predicates such as `isRefV` that may not
name a surface construct. Rules for unrelated floats, dicts, sets, sorting,
methods, comprehensions, assertions, and slices cannot be reached from this
program and do not contribute to either claim.

### Construct-to-semantics map

| Submitted construct | Declaration/evaluation | Material rules |
|---|---|---|
| `Module`, statement sequence | `syntax.k`, `core.k` | `#loadAll`, statement sequencing |
| `FuncDef`, `Call`, parameters, return | `syntax.k`, `functions.k`, `call.k` | closure binding, callee/argument evaluation, frame push, `#bindP`, `Return`, `#pop` |
| `Name`, assignments | `syntax.k`, `core.k`, `controls.k` | scope-chain lookup, `Assign`, `AugAssign` |
| integer/string literals | `syntax.k`, `core.k`, `str.k` | `Int`, ASCII `Str`, `strToCodes` |
| list literal and list `+` | `syntax.k`, `list.k`, `operators.k`, `core.k` | left-to-right elements, allocation, ref dereference, `valSeqConcat`, second allocation |
| tuple loop target | `syntax.k`, `tuple.k` | `TupleExpr`, `#bindTgt`, `#unpackSeq` |
| `for` | `syntax.k`, `controls.k`, `iter.k` | strict iterable evaluation, `#loop`, `#iterNext`, `#loopStep`, `#loopLbl` |
| `zip` | `builtins.k`, `call.k` | builtin resolution, `zipObj`, yield/done rules |
| `str(int)` | `builtins.k`, `call.k` | fixed integer conversion plus the exact guarded proof twin |
| string `+` | `str.k`, `operators.k` | `seqConcat` plus the exact guarded proof twin |
| `eval` | `builtins.k`, `call.k` | `evalArith`, tokenizer, power/multiply/add precedence passes |

Strict and sequential-strict attributes plus the shared `#evalArgs` machine
give the needed order: callee before arguments, list elements left-to-right,
and binary operands left-to-right. The call rules preserve the continuation,
push a frame, bind the exact parameters, and pop back to the caller. The two
list constructions are the only heap allocations. The loop evaluates `zip`
once and follows the real iterator path. No candidate-local rule changes a
cell or introduces abrupt control.

### Every proof-local declaration and rule

`verification.k` adds five syntax declaration groups and 26 rules. They fall
into these exhaustive groups:

1. `definedProjectInt` and `definedProjectStr` (2 rules) are exact names for
   fixed sort predicates.
2. The two `#Ceil` rules characterize the fixed partial casts. Their right
   sides require exactly the corresponding sort predicate and the input's
   own definedness.
3. Integer and string total-projection rules (3 each) orient the same guarded
   cast for concrete and symbolic simplification and collapse actual `Int` or
   `Str` constructors. Overlaps have identical values.
4. `codesOf` and `codesProject` (2 rules) expose the sole `Str` constructor's
   code sequence through the guarded projection.
5. The two guarded dispatch twins restate the fixed
   `str(Int)` and `str + str` equations. Their exact builtin/operator names,
   arities, and sort guards are no broader than the fixed rules. They match
   no `<k>` context and read or write no cell.
6. `allowedOperator` (1 rule) is exactly the five prompt strings.
7. `validAlgebraLists`/`validAlgebraRest` (5 rules) are constructor-recursive
   domain predicates with `owise` false cases.
8. `runPairCodes` (3 rules) is the exact zip-truncating recurrence; its two
   base cases and cons/cons case are exhaustive and mutually disjoint.
9. `lastPairValue` (3 rules) returns the last paired operand on valid
   sequences. The singleton and recursive patterns only overlap when the
   recursive guard is false; the `owise` case covers invalid shapes.

All recursive equations consume at least one sequence constructor. There are
no proof-local priority rules, K-cell operational bridges, return shortcuts,
call interceptions, loop interceptions, state or exception rewrites, answer
axioms, or unconstrained result-producing oracles.

`projectIntTotal` and `projectStrTotal` are declared total symbols and may have
an arbitrary off-sort interpretation. That interpretation cannot affect these
claims: every value-bearing use is dominated by
`validAlgebraLists`, which establishes the corresponding sort guard. On the
guarded domain, the fixed partial casts uniquely determine their values. This
is a low-level symbolic projection idiom, not a program-result oracle.

### Relevant fixed evaluator

The supplied `evalArith` is not opaque. Its rules tokenize non-negative decimal
operands and the five operator strings, then:

- fold `**` from the right;
- fold `*` and `//` from the left; and
- fold `+` and `-` from the left.

On the formal domain, each power/multiplicative subexpression starts from
non-negative operands. Therefore all normally evaluated division operands are
non-negative, so the evaluator's integer division agrees with Python floor
division. A zero divisor has no normal integer result.

Reviewer-authored K execution compared the full candidate function and fixed
evaluator with independently computed Python values on 44 additional bounded
normal cases. All 44 final scope bindings matched. See
`evidence/05_make_eval_cases.py`, `evidence/05_eval_inputs.json`,
`evidence/05_eval_bridge_krun.out`, and
`evidence/05_eval_bridge.log`.

### Division-by-zero limitation

The fixed rule at `semantics/builtins.k:234` rewrites
`applyOpE("//", A, B)` to the K integer division hook without a nonzero guard.
For the valid structural input `operators=["//"]`, `operands=[5,0]`,
both Python functions raise `ZeroDivisionError`. Fresh LLVM execution instead
aborted in `[hook_INT_ediv]` and `krun` exited 255; it did not produce a final
K exception configuration. See `evidence/fixtures/k_zero_divisor.py` and
`evidence/05_zero_divisor_krun.log`.

I do not label this rule materially unsound for the proved normal-result
property: there is no witness where it enables a false returned integer, and
the reachability theorem is partial correctness. The zero-divisor execution
has no normal result on either side. Nevertheless, the concrete backend abort
is not a faithful model of CPython's observable exception state. It is the
specific nonfatal semantics/evidence limitation behind the `CONCERNS`
verdict.

Stage 5 result: PASS for proof soundness, with the documented fixed-semantics
exception-model concern.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was inspected only as untrusted evidence and
was not reused as the required mutation.

`evidence/06_false_mutation.k` is reviewer-authored. It executes the exact
submitted body on the satisfying documented input, but changes the
result-constraining postcondition from the true answer 9 to the false answer
8. It changes no import and retains the real function load/call path.

The command:

```text
kprove 06_false_mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-MUTATION
```

successfully parsed and built the mutation, then exited 1 with
`WarnStuckClaimState`. The residual has empty `<k>`, normal control cells, the
exact loaded closure, and `answer |-> 9`; it fails only because the
destination demands 8. The wrapper verified both the warning and residual
and exited 0 to indicate the expected rejection.

Reproducible evidence: `evidence/06_nonvacuity.sh`,
`evidence/06_false_mutation_kprove.log`, and
`evidence/06_nonvacuity.log`.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY theory and the entry precondition, the exact submitted
function body has this partial-correctness property for arbitrary finite
contract-valid sequences:

1. It loads and calls the actual `do_algebra` closure.
2. Fixed list, lookup, call, zip, loop, tuple-binding, conversion,
   concatenation, return, and frame-pop rules execute the material operations.
3. If execution reaches a normal result, the module variable `answer` equals
   `evalArith` of the exact alternating operand/operator code sequence.
4. The final stack, return state, exception cell, exit code, allocations, and
   heap counter have the stated values.

The auxiliary circularity universally summarizes an arbitrary finite
remaining loop sequence; this is not a bounded unrolling. The precondition
does not restrict list length or integer magnitude.

### Trusted primitives and assumptions

- The supplied reference semantics is the fixed semantic trust base. Its
  candidate copy passed recursive integrity checking.
- K integer and string hooks, including `Int2String`, integer arithmetic, and
  the parser's primitive operations, are trusted. The used evaluator itself is
  defined by equations rather than an opaque answer symbol.
- The K frontend, Haskell backend, LLVM backend, and reachability
  implementation are trusted tooling.
- The trusted `py2mpy.py` translator is assumed to represent its supported
  CPython AST faithfully. Byte regeneration and constructor comparison remove
  candidate control over this bridge.
- Mapping K unbounded integers and ASCII operator code sequences to the
  corresponding Python values is an ordinary representation bridge.
- The simple algebraic fact that
  `zip(operand, operator + [""])` constructs the same token order as the
  canonical initial-operand/remaining-pairs loop follows from the exact length
  precondition. Differential execution supplies finite independent support;
  it does not replace the K proof.
- Termination and abnormal-exception behavior are not proved. In particular,
  the supplied semantics does not construct Python's `ZeroDivisionError`
  state.

### Opaque symbols

- Proof-local `projectIntTotal` and `projectStrTotal` are no-evaluator symbols
  only off their sort guards. Their result-bearing uses in both claims are
  guard-fixed by exact casts; no opposite interpretation is admitted on the
  formal domain.
- Supplied semantics contains unrelated opaque symbols for floats, sorting,
  and MD5. The submitted syntax and all reachable rules avoid them.
- No opaque symbol stands for `do_algebra`, the loop, its expression string,
  or the final answer.

### Empirical evidence

- 1,337 independent Python canonical-versus-candidate cases had zero
  intended-domain mismatches, including compared exception types.
- Fresh K concrete execution covered normal branches and precedence.
- A further 44 K-versus-Python normal evaluator cases had zero mismatches.
- The body mutation and fresh false-result mutation both reached a different
  concrete result and were rejected.

These tests support fidelity and trust-boundary assessment only. The
unbounded theorem comes from the reconstructed K reachability proof.

### Decision

Gate A passes: the proof is sound, body-sensitive, result-constraining, and
has no execution bypass. Gate B passes for the requested unbounded
partial-correctness property and does not narrow the HumanEval structural
domain. The fixed semantics' division-by-zero path is a nonfatal language-
model limitation: it aborts rather than representing the observable Python
exception, but it does not make a false normal-result conclusion provable.
That limitation prevents an unqualified `PASS` while leaving the proof
legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
