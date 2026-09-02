# Independent adversarial audit: 126-is-sorted

This review treats every candidate artifact as an untrusted claim. All dynamic
work used source copies under `/tmp/audit-work/reconstruction`; neither
`/candidate/runtime-kompiled` nor `/candidate/verification-kompiled`, candidate
caches, bytecode, logs, traces, or prior `#Top` output was reused.

The reconstructed K proof is legitimate for its explicitly bounded theorem:
lists of length 0 through 7 containing arbitrary nonnegative mathematical
integers. It does **not** prove the prompt's unbounded finite-list domain. That
material scope limitation determines `CONCERNS / LEGIT`, rather than `PASS` or
`FAIL`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists. The candidate's
`reference-semantics/` also exists.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 651-record JSONL trace only as untrusted generation
claims. They claim a kit-semantics run, exit 0, eight closing claims, concrete
tests, differential tests, expected negative probes, and a
`SOUND-BUT-LIMITED` result. None of those claims was used as authority.
`evidence/01_trace_summary.log` records the bounded trace inspection, including
all tool-call commands and assistant reports found by
`evidence/trace_summary.py`.

The independent provenance checks established:

- The required trusted `prompt.py`, `canonical.py`, `py2mpy.py`, and reference
  semantics are present as the expected filesystem types.
- The candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- The candidate `py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- `diff -qr --no-dereference` reports no missing, additional, changed, or
  mistyped entry between the trusted and candidate semantics trees.
- No symlink occurs in either compared semantics tree, and the required
  candidate raw artifacts are regular, non-symlink files.
- All required deliverables are present. Candidate-provided compiled
  definitions and caches were identified but deliberately excluded.

There is no infrastructure-mode contradiction and no provenance integrity
failure. Exact commands, statuses, hashes, and both semantics manifests are in
`evidence/01_provenance_checks.sh` and
`evidence/01_provenance_checks.log`. In particular, the prompt and translator
hashes are respectively
`050a2b9defc209aa64d0777939ff3387ee7db918434d818789eab7b36578b7ca`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `is_sorted(lst)` to return whether a finite list of
nonnegative integers is nondecreasing, except that any value occurring more
than twice makes the result false. The trusted canonical implementation first
counts all values, rejects any count above two, and then checks every adjacent
pair with `<=`.

The generated implementation uses a different but appropriate one-pass
algorithm. It initializes `previous = -1`, which is safe only because the
prompt excludes negative inputs. It rejects a decrease, tracks repetitions
within an equal run, rejects the third occurrence, resets the repetition
counter when the value changes, and otherwise returns true. In a
nondecreasing list, all equal values are contiguous, so run length and global
multiplicity coincide.

### Translation identity

The trusted translator was run afresh:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

It exited 0, and `cmp -s solution.regenerated.mpy solution.mpy` exited 0.
Both translated files have SHA-256
`a837c6a383eb4cf6bd4a635de85cbac09240ad6740d4638c12324035eb73c35e`.
See `evidence/02_program_fidelity.sh` and
`evidence/02_program_fidelity.log`.

### Independent differential test

`evidence/02_differential.py` independently imports
`/reference/canonical.py:is_sorted` and the scratch copy of
`solution.py:is_sorted`. It also uses a third, direct contract oracle:
adjacent nondecrease plus `Counter` multiplicities at most two. The test
covered:

- all eight documented examples;
- empty, zero/sentinel, first decrease, allowed pair, third duplicate, reset,
  large-integer, and length-above-seven boundaries;
- every list of length 0 through 7 over values `{0,1,2,3,4}`; and
- 6,000 deterministic generated lists of lengths 0 through 40.

After duplicate inputs were removed, all three implementations agreed on
103,427 unique inputs with zero mismatches. The exact input stream is
`evidence/02_differential_inputs.jsonl`; the command, seed, group sizes, status,
and result are in `evidence/02_program_fidelity.log`. This is strong finite
evidence of program-to-intent fidelity, not a universal proof.

## 3. Clean proof reconstruction

K v7.1.293 and Python 3.10.12 were available. The reviewer copied only raw
sources to scratch and built new definitions with distinct names.

The fresh concrete definition was built with:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

The build exited 0. An independently authored driver was translated with the
trusted translator and run with:

```text
krun 03_concrete_driver.mpy --definition runtime-audit-kompiled
```

It exited 0 after testing empty input, zero boundaries, decreases, allowed and
third duplicates, and inputs above the proof's length bound. Its final
configuration has `.K`, `NoExc`, and exit code 0. Sources and logs are
`evidence/03_concrete_driver.py`, `evidence/03_translate_concrete.log`,
`evidence/03_build_runtime.log`, and
`evidence/03_concrete_run.log`.

The fresh proof definition was built with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

The build exited 0. The aggregate proof command

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

printed exactly one `#Top` and exited 0. I then independently selected every
positive claim with `--claims SPEC.len-N` for each `N=0,...,7`. Every one
printed `#Top` and exited 0. The driver and status index are
`evidence/03_reconstruct.sh` and
`evidence/03_reconstruction_summary.log`; the complete bounded logs are
`evidence/03_positive_all.log` and
`evidence/03_positive_len_0.log` through
`evidence/03_positive_len_7.log`.

Thus the candidate's positive claims close in a clean reconstruction. No
candidate-built definition contributed to this result.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.len-0` starts with the exact top-level call state and an empty input list.
`SPEC.len-N`, for each `N=1,...,7`, starts with exactly `N` independently
symbolic `Int` elements and requires every element to be nonnegative. All
claims start with environment 0, module scope containing only `input`, the
trusted builtins scope at `-1`, next scope location 1, empty heap, heap
location 0, empty stack, `noRet`, `NoExc`, and exit code 0.

Every destination requires:

- the `<k>` result to be an existential Boolean `?RESULT`;
- `?RESULT ==Bool sortedAtMostTwice(the exact input sequence)`;
- the original input to be preserved;
- the exact `is_sorted` closure to have been installed in module scope;
- call scope/frame removal and restoration of scope location, heap, stack,
  return, exception, and exit-code cells.

The postcondition is an equality, not a one-way implication, free result, or
tautology.

### Exact program execution

`IS-SORTED-LOOP-BODY` and `IS-SORTED-BODY` are compile-time macros, not
operational bridges. A fresh `kast --expand-macros` of
`IS-SORTED-BODY` exited 0 and printed the same constructor sequence and
statement order as the freshly parsed submitted `solution.mpy`. The entry
macro expands to that exact `FuncDef` followed by lookup and
`Call(Name("is_sorted"), Name("input"))`; the closure macro records the exact
parameter, body, and defining environment 0. Source and expansion evidence is
in `verification.k:9-37` and `evidence/04_macro_expansion.log`.

An optional pretty-expansion attempt for the whole sort-`K` entry macro hit a K
`NoSuchElementException` concerning `#EmptyK`; it was not used as proof
evidence. The body expansion and submitted program parse both succeeded, the
macro source is directly inspectable, and the fresh definition and all claims
compiled and proved. This isolated diagnostic therefore creates no unresolved
program-identity uncertainty.

There are no helper or loop claims. Each bounded loop is executed and unrolled
through the supplied fixed semantics. The mathematical `sortedFrom` function
appears only in the destination constraint; no rule rewrites a program term to
that summary.

### Satisfying witnesses

For each claim `SPEC.len-N`, the concrete state binding `input` to a list of
`N` zeros and using the stated initial cells satisfies its precondition.
Substitution into `sortedAtMostTwice` yields true for `N=0,1,2` and false for
`N=3,...,7`. The trusted canonical and generated Python functions give the
same values for every witness. Exact states and results are in
`evidence/04_claim_witnesses.py` and
`evidence/04_claim_witnesses.log`.

### Adequacy limitation

The prompt permits arbitrary finite lengths. No claim covers length 8 or
greater, and there is no loop invariant or other theorem from which those
cases follow. Differential examples above the bound do not enlarge the K
theorem. This is a material intent-scope limitation, but not a substitution,
vacuity, or soundness defect in the bounded claims.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_inventory.py` parsed every K source declaration in the supplied
semantics tree, `verification.k`, and `spec.k`. Its exhaustive row-level output
is `evidence/05_rule_inventory.tsv`; each row records file, module, exact
line span, kind, full normalized declaration, attributes, relevance, and a
review decision. `evidence/05_rule_inventory_summary.log` records counts and
lists every opaque declaration and priority rule.

The inventory contains 1,123 entries:

- 232 syntax declarations;
- 695 supplied semantic rules and 8 proof-local rules;
- 1 configuration and 5 contexts;
- 45 priority-rule declarations;
- 35 `[concrete]` rule declarations;
- 146 declaration rows containing `[function]`;
- 108 declaration rows containing `[total]`;
- 25 opaque/symbol declarations;
- no `[functional]` declaration;
- no `[simplification]` rule; and
- all eight reachability claims.

The candidate's supplied semantics is byte-identical to the trusted selected
semantics. The 608 fixed rules outside the submitted program's execution
slice were inspected and classified as having no target-path effect; they are
accepted only as part of the user-supplied semantics level, not asserted here
as a complete theorem about Python. The 25 opaque symbols are `md5hexCodes`,
22 float/conversion helpers, `sortVS`, and `sortKeyVS`; none is reachable from
this integer/list program or appears in a target postcondition.

The LLVM compiler reports non-exhaustive total-function warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are
narrow evidence gaps in unused fixed-semantics features. None occurs in the
submitted syntax, executed target path, summary, or claim result. The Haskell
proof build reports only unused-variable warnings in string comparison rules,
also outside the target path. No claim of unsoundness is made from these
warnings because they enable no false target conclusion witness.

### Used syntax and rules

`evidence/05_used_construct_map.md` maps every submitted construct to its
declaration and operative rules. The used slice comprises:

- `FuncDef`, closure creation, callee-before-argument evaluation, name lookup,
  fresh frame creation, parameter binding, return, and frame pop;
- strict RHS/condition/iterable evaluation for `Assign`, `AugAssign`, `If`,
  `For`, and `Return`;
- statement sequencing and mathematical `Int`/`Bool` literals;
- integer unary minus, addition, and `<`, `==`, `>` comparisons;
- list-head/tail iteration and loop-target binding; and
- Boolean truth and branch selection.

The call starts from a module binding for `input`, defines the exact closure,
looks up that closure and input, creates a plain local scope, binds `lst`,
executes both initialization assignments and the real `For`, performs each
comparison and update, and returns through the ordinary frame machinery.
Early `Return(V) ~> _ => #pop` correctly discards the remainder of the
function computation while resuming the captured caller continuation.

All competing used-slice priority rules concern heap `ref` values or annotated
closure cells. Here the input is the supplied semantics' legal unboxed,
read-only `list(ValSeq)`, each element is constrained `Int`, and the ordinary
call creates a plain frame without `"$cells"`. Those competitors' match or
guard conditions are false. Integer operator cases are sort-disjoint from
Boolean, float, string, collection, and dictionary cases. The input is never
mutated or allocated.

### Proof-local extensions

`verification.k` adds only:

1. Four exact syntax macros and their four expansion rules.
2. One syntax declaration containing the total functions `sortedFrom` and
   `sortedAtMostTwice`.
3. Four pure defining equations for those functions.

There is no proof-local priority, simplification, concrete, opaque,
call-interception, loop-interception, return, state, or allocation rule.

For `sortedFrom`, empty and `vCons` are disjoint. On a `vCons`, the `Int` head
rule and the guarded non-`Int` rule are disjoint and exhaustive over `Val`.
The integer rule's nested conditionals exhaust decrease, equal with a third
occurrence, equal without a third occurrence, and increase. Every recursive
call consumes the strict sequence tail. `sortedAtMostTwice` has one
unconditional equation and uses sentinel `-1`; all entry claims guarantee
nonnegative elements. The equations therefore have truthful coverage and
structural descent on their full declared domain.

These functions constrain the destination but never replace real execution.
They legitimately state the expected result; they do not smuggle it into an
operational rule. Independently selected per-length proofs also rule out
cross-claim assistance.

No rule encodes a false target conclusion, supplies an unconstrained
result-bearing oracle, bypasses execution, or fabricates a used construct.
Accordingly this review makes no unsound-rule allegation and has no false-rule
witness to report.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not reused. I authored
`evidence/06_false_result_spec.k`, copied it to scratch, and used the satisfying
input `[0,1,2,3]`. Both trusted canonical and generated Python executions
return true, while the mutated K claim requires `?RESULT ==Bool false`.

The parsing/build check

```text
kprove 06_false_result_spec.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run
```

exited 0. The actual proof command without `--dry-run` exited 1, printed one
`WarnStuckClaimState`, printed no `#Top`, and reported that the term unified
with the destination but the condition implication failed. Its residual
contains `<k> true ~> .K </k>`, the complete expected final state, and the
unmet false result obligation. This is a reachable semantic rejection, not a
parse error, missing import, timeout, or unrelated crash.

The exact artifact, commands, statuses, witness oracle results, and bounded
output are in `evidence/06_nonvacuity.sh`,
`evidence/06_nonvacuity_summary.log`,
`evidence/06_false_result_dry_run.log`, and
`evidence/06_false_result_proof.log`.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied `MPY` semantics and ordinary K mathematical domains, for
each fixed length 0 through 7 and all nonnegative symbolic integer elements,
any terminating execution of the exact submitted translated function from the
specified clean top-level state returns the Boolean computed by
`sortedAtMostTwice`, while restoring/preserving the cells constrained by the
claim. This is a partial-correctness theorem over eight bounded symbolic input
shapes.

### Trust ledger

| Boundary | Effect on this theorem | Assessment |
|---|---|---|
| Byte-identical supplied `reference-semantics/` | Defines syntax, evaluation, values, lookup, calls, frames, loops, state, and exceptions | Authorized fixed theorem base. The exact used slice was statically reviewed and concretely exercised. |
| K v7.1.293 frontend, Haskell backend, SMT stack, and runtime | Parses/compiles rules and establishes `#Top` | Necessary toolchain trust. Fresh positive and negative runs discriminate the result. |
| LLVM backend | Supports concrete smoke execution only | Empirical support; not a substitute for the Haskell reachability proof. |
| K `Int`, `Bool`, `String`, `Map`, `List`, equality, and arithmetic hooks | Supplies ordinary mathematical primitives used by semantics and summary | Acceptable low-level trust boundary; no task answer is embedded in it. |
| Trusted translator `/reference/py2mpy.py` | Bridges `solution.py` to the exact submitted MPY AST | Authorized input; fresh byte identity pins the translated program. |
| `sortedFrom` to the English property | Interprets rejection of decreases and third equal run as nondecreasing with global multiplicity at most two | Structurally justified informally and supported by zero-mismatch differential evidence; not a separate K theorem about the English sentence. |
| Trusted canonical Python implementation | Differential oracle only | Supports program/intent alignment on tested inputs; contributes nothing to `#Top`. |
| 25 supplied opaque symbols | Float, sorting, and MD5 behavior elsewhere in the selected semantics | None is reached or result-bearing for these claims, so no target conclusion depends on an interpretation. |

There is no proof-local trusted primitive, empirical operational bridge, or
opaque result on which the bounded theorem depends.

### Excluded and concerning scope

The K proof does not cover:

- lists of length 8 or greater;
- negative or non-integer elements;
- heap-ref/aliased inputs, mutation, or exceptional inputs; or
- total correctness/termination as a separately stated theorem.

Negative and non-integer inputs are excluded by the prompt itself. The
length-at-most-seven restriction is not in the prompt and is the decisive
adequacy concern. Concrete and differential success for longer inputs does not
repair that formal gap.

The proof is therefore sound, result-constraining, non-vacuous, and pinned to
the real generated program on its formal domain, but it is not a complete proof
of the prompt's intended arbitrary-length domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
