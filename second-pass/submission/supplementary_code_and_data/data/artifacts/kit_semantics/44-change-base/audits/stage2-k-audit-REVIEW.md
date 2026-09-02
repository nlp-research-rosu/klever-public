# Independent audit: 44-change-base

## Executive decision

The candidate contains a genuine, non-vacuous K reachability proof of the exact
submitted `solution.mpy` under the supplied MPY semantics. The proof was rebuilt
from source, both claims close together with `#Top`, the loop claim also closes
independently, the parsed constructor tree in each claim is identical to the
trusted regeneration of the program, and two fresh false mutations fail at the
expected result obligation.

The result is **LEGIT with CONCERNS**, rather than an unqualified pass, for two
non-fatal boundary issues:

1. The prompt does not state `x > 0`, although the trusted canonical only
   implements a meaningful base conversion for positive `x`. The candidate
   agrees with the canonical on every tested positive input, but returns `"0"`
   at zero and signed representations for negatives where the canonical returns
   `""`. The proof covers these inputs and proves the candidate's actual
   behavior; it does not narrow its theorem to examples or fixed sizes. I treat
   positive `x` and bases 2 through 9 as the material HumanEval domain implied
   by the canonical loop and examples, but the missing written precondition is a
   real contract ambiguity.
2. `changeBaseCodes` is a sound recursive digit-sequence specification, but the
   final identification of that sequence with the natural-language phrase
   “string representation after the conversion” is an informal mathematical
   intent bridge. The K theorem proves the algorithmic sequence exactly; it
   does not separately prove a positional-value equation.

These limitations do not allow a false result about the exact submitted program
to be proved and do not materially narrow the positive-input source-contract
domain.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `44-change-base`, and condition
`kit-semantics`. The supplied-semantics mount is present, so the rendered mode
and trusted mounts are consistent. There is no infrastructure breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required
`/generation-evidence` top-level records, the full output and final text, and
the complete structured trace. The campaign-lock JSON equals the
`audit_campaign` block and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly as recorded.

The independent provenance checker found:

- every required pipeline-v3 file and directory present, readable, and of the
  expected node type;
- all recorded individual file hashes equal to newly computed SHA-256 values;
- the pipeline-v3 length-delimited hashes of the complete candidate tree,
  candidate reference semantics, trusted reference semantics, and trace tree
  equal their values in the generation records;
- no symlink or unsupported node in the candidate, either semantics tree, or
  trace tree;
- candidate `prompt.py` and `py2mpy.py` byte-identical to their trusted mounts;
  and
- all 24 files plus the directory layout in
  `/candidate/reference-semantics` recursively identical to
  `/reference/reference-semantics`, with no missing or additional entry.

`/audit-input.json` also contains an audit-launcher-specific family of tree
digests whose serialization is not declared in the record. I recorded those
values and separately computed two content-addressed tree serializations. I did
not infer integrity from an unknown serialization: the independently
recomputed, specified pipeline-v3 tree hashes, per-file hashes, node-type scan,
and recursive byte comparison provide the integrity check.

The trace contains one 750,442-byte JSONL file with 462 valid events, 103 tool
calls and 103 matching tool outputs, no orphaned call, and no malformed record.
The complete generation output is valid UTF-8 (1,244,652 bytes and 37,018
lines), not a sampled excerpt. These generation records were treated only as
untrusted historical claims.

Evidence:

- `evidence/provenance_check.py` and
  `evidence/stage1-provenance.log` (exit 0)
- `evidence/trace_inspect.py` and
  `evidence/stage1-trace-inspection.log` (exit 0)
- `evidence/generation_log_inspect.py` and
  `evidence/stage1-generation-log-inspection.log` (exit 0)

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for a string representation of integer `x` in a base
whose digits are below 10, with examples `8` in base 3 producing `"22"`, `8` in
base 2 producing `"1000"`, and `7` in base 2 producing `"111"`. The trusted
canonical repeatedly prepends `str(x % base)` while `x > 0`, then returns the
accumulator. Operationally, that canonical supplies the conventional contract
for positive `x` and bases 2 through 9. It returns `""` for `x <= 0`; bases
below 2 are not a viable unrestricted domain (division by zero or
non-termination).

The generated program uses the same repeated-division algorithm, spelling a
digit as `chr(48 + x % base)`. It additionally handles zero as `"0"` and
negative integers with a leading `"-"`.

### Trusted translation

I ran the trusted `/reference/py2mpy.py` against the copied `solution.py`.
The regeneration and submitted `solution.mpy` are byte-identical, both with
SHA-256
`a334193f7f2cb458295d0c62874904cfc9f9e44eaa0265d0f061afd890e1b57c`.
See `evidence/stage2-translation.log` (exit 0).

### Differential execution

The independent script imports the two real Python entry points. It covers all
prompt examples, zero, negatives, branch boundaries, very large integers, the
complete grid `x = -64..512` for bases `2..9`, and 1,000 deterministic random
cases, for 5,618 unique cases.

There were no exceptions and **zero mismatches for `x > 0`**. There were 1,015
mismatches confined to `x <= 0`: eight at zero and 1,007 for negatives. For
example, `(0,2)` is canonical `""` versus generated `"0"`, and `(-8,3)` is
canonical `""` versus generated `"-22"`. This is the contract ambiguity
reported above, not a hidden restriction in the theorem.

Evidence:

- `evidence/differential_test.py` and
  `evidence/stage2-differential.log` (exit 1 solely because the script makes
  discovered divergences fail the check)
- `evidence/targeted_program_cases.py` and
  `evidence/stage2-targeted-cases.log` (exit 0)

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/44-change-base` and did not copy
or use either candidate-provided `*-kompiled` directory, Python cache, proof
log, or candidate test as a proof result. The observed toolchain was K
7.1.293 and Python 3.10.12.

Fresh builds:

- `kompile reference-semantics/semantics.k --backend llvm --main-module
  MPY-KRUN --syntax-module MPY-SYNTAX --output-definition
  runtime-fresh-kompiled` — exit 0.
- `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  verification-fresh-kompiled` — exit 0.

The Haskell build emits only unused-variable warnings. The LLVM build also
warns that several supplied total functions are not exhaustive on exotic
injected values. None is reached by this program except ordinary integer and
string operations; a missing equation would make such an alien term stuck, not
derive the desired result.

Fresh positive proofs:

- the `SPEC.loop-invariant` claim exits 0 and prints `#Top`;
- selecting both `SPEC.loop-invariant,SPEC.change-base` exits 0 and prints
  `#Top`; and
- the unfiltered spec, containing exactly those two claims, exits 0 and prints
  `#Top`.

The entry claim needs the loop claim as its supporting circular invariant; the
joint invocation is therefore the relevant independent entry proof. Exact
commands and bounded output are in:

- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-loop.log`
- `evidence/stage3-kprove-entry.log`
- `evidence/stage3-kprove-all.log`

For concrete reconstruction, `evidence/concrete_actual.py` contains the exact
candidate function AST followed by assertions for the three prompt examples,
zero, a negative input, and base 9. The AST comparison and translation succeed,
and `krun` with the fresh LLVM definition ends in `.K`, `NoExc`, and exit code
0. See `evidence/stage3-concrete-harness-build.log` and
`evidence/stage3-krun-concrete.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-invariant` starts at the exact internal `#while` for the submitted loop.
For arbitrary accumulated result codes `ACC`, nonnegative current `X`, and
`2 <= B < 10`, it says execution reaches the real return continuation with
local `x = 0` and result codes `baseAcc(X,B,ACC)`. The exact call frame, closure,
scopes, heap, stack, return, exception, and exit-code cells are present.

`change-base` starts with the real call
`Call(Name("change_base"), (X,B,.Exprs))` for every integer `X` and
`2 <= B < 10`. It says execution returns
`str(changeBaseCodes(X,B))`, where that function is:

- code `[48]`, i.e. `"0"`, when `X = 0`;
- repeated base-`B` remainder digits for positive `X`; and
- code 45 (`"-"`) followed by those digits for negative `X`.

This is a result-constraining equality, not a free variable, existential oracle,
tautology, or one-way implication.

### Mechanical pinning

I parsed regenerated `solution.mpy` with the fresh definition and emitted the
spec claims as JSON KAST. The closure in each claim has the same parameter-tree
SHA-256 and body-tree SHA-256 as the regenerated function. Both equality tests
are exact constructor-level comparisons, both defining environments are zero,
and the entry claim contains exactly one `change_base` call and one
`changeBaseCodes` result term. See
`evidence/constructor_compare.py`,
`evidence/stage4-parse-artifacts.log`, and
`evidence/stage4-constructor-comparison.log` (zero failures).

The preconditions are satisfiable. A loop state with
`X=8, B=3, ACC=[]` has final accumulator `[50,50]`. Entry witnesses include:

- `(8,3)` gives claimed/generated/canonical `"22"`;
- `(9,9)` gives all three `"10"`;
- `(0,2)` gives claimed/generated `"0"` versus canonical `""`; and
- `(-8,3)` gives claimed/generated `"-22"` versus canonical `""`.

See `evidence/stage4_witnesses.py` and
`evidence/stage4-satisfying-witnesses.log`.

For body sensitivity I changed the actual constructor in the claim closure from
`Int(48)` to `Int(49)` while retaining the original `"22"` obligation at
`(8,3)`. Mechanical comparison reports exactly that one token difference.
The mutation builds, then the proof exits 1 with the concrete residual result
codes `[51,51]` (`"33"`) unable to unify with `[50,50]` (`"22"`). This directly
shows that the theorem executes and depends on the embedded submitted body.
See `evidence/fresh-body-mutation-spec.k`,
`evidence/body_mutation_compare.py`,
`evidence/stage4-body-mutation-build.log`,
`evidence/stage4-body-mutation-constructor-check.log`, and
`evidence/stage4-body-mutation-proof.log`.

A separate exploratory attempt to prove standalone functional equalities was
rejected by this backend because functional claims are not reachability claims;
`evidence/stage4-ground-summary.log` is retained as a discarded diagnostic and
is not used as proof or non-vacuity evidence.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` inventories every declaration in the trusted
`semantics.k`, all 23 required helper files, `verification.k`, and `spec.k`.
The resulting `evidence/stage5-rule-inventory.log` contains all 938 items with
source line, normalized text, and attributes:

| Kind | Count |
|---|---:|
| Syntax declarations | 229 |
| Ordinary semantic rules | 594 |
| Priority rules | 47 |
| Concrete-only rules | 54 |
| Simplification rules | 6 |
| Contexts | 5 |
| Configuration | 1 |
| Claims | 2 |

The inventory gives per-file counts for `assert`, `bool`, `builtins`, `call`,
`comprehension`, `concrete`, `controls`, `core`, `dict`, `float`, `functions`,
`int`, `iter`, `list`, `methods`, `operators`, `range`, `set`, `sort`, `str`,
`subscript`, `syntax`, and `tuple`, then enumerates every row. Thus unused
modules were not silently omitted from the review.

### Used-construct coverage and control/data flow

The parsed program uses 21 unique K labels, enumerated in
`evidence/used_constructs.py` and
`evidence/stage5-used-constructs.log`: `Module`, `FuncDef`, `Params`, `If`,
`Assign`, `While`, `Return`, `Int`, `Str`, `Name`, `UnaryOp`, `BinOp`,
`Compare`, `CmpOp`, `Call`, and their sequence constructors.

I mapped that set to the following reachable rule slice:

- `syntax.k`: all listed AST declarations and sequence constructors;
- `core.k`: the configuration, module/statement sequencing, scope lookup,
  built-in root, value forms, string/int literal plumbing, and cell updates;
- `functions.k` and `call.k`: closure binding, two-argument evaluation,
  parameter binding, call-frame creation, return, and `#pop`;
- `controls.k`: condition evaluation, truth selection, `#while`,
  `#whileCond`, loop label/continue structure, assignment, and sequencing;
- `operators.k` plus `int.k`: left-to-right operand evaluation, dispatch,
  unary minus, `+`, `%`, `//`, `<`, `==`, `>`, and `pyMod`;
- `str.k`: ASCII literal conversion and left-to-right sequence concatenation;
  and
- `builtins.k`: ordinary built-in lookup and
  `applyBuiltin("chr", I, .Vals) => str(iCons(I,.IntSeq))`.

On `2 <= B < 10`, each remainder is in `0..8`, so `chr(48 + remainder)` stays
in the supplied ASCII model. Integer floor division is defined as
`(I1 - pyMod(I1,I2))/I2`, which matches Python for the positive divisor used
here. The evaluation contexts and call/return cell changes preserve Python's
order, and the while rule executes the actual body before rechecking the guard.
No allocation, exception, alias, or mutation behavior omitted by the claim is
material to this function.

Every inventory row outside this closure is disposed of as an imported,
constructor-disjoint feature: assertions, comprehensions, dicts, floats,
iteration protocols not used by `chr`, lists, methods, ranges, sets, sorting,
subscripts, and tuples cannot introduce their AST constructors into this
closed call. Concrete-only twins do not participate in the Haskell proof.
Their presence therefore cannot help establish the result. The supplied
semantics' intentionally opaque symbols—`sortVS`, `sortKeyVS`,
`md5hexCodes`, and the float family `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `floorFI`, `toF`, `ceilF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`—are all unreachable. Symbolic string ordering
is likewise unused.

### Candidate proof extension

The only proof-local declarations are two total functions and six
simplification equations:

- `baseAcc`: its guards `N <= 0`, `N > 0 and B < 2`, and
  `N > 0 and B >= 2` are pairwise disjoint and exhaustive. On the theorem
  domain, the recursive equation prepends exactly `48 + N mod B` and recurs on
  the quotient. For `N > 0, B >= 2`, that quotient is a nonnegative integer
  strictly below `N`, so the equation is well-founded.
- `changeBaseCodes`: its zero, positive, and negative guards are disjoint and
  exhaustive. It adds exactly the candidate's zero code or negative sign and
  delegates the magnitude to `baseAcc`.

These equations neither rewrite the `<k>` cell nor bypass calls, loops, state,
or exceptions. They contain no proof-local opaque symbol, no unconstrained
oracle, and no task-answer rule for a fixed input. They are a mathematical
summary of the exact computation, and the operational proof must establish
that summary.

I found no rule capable of enabling a false conclusion on the theorem domain,
so there is no claimed-unsound rule requiring a false-conclusion witness. The
compiler's non-exhaustiveness warnings are narrower completeness gaps on
unreachable injected terms, not evidence that an incorrect value can be
derived.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation in
`evidence/fresh-false-spec.k` retains the exact original closure and the
satisfying input `(8,3)`, but changes the result obligation from true `"22"`
(codes `[50,50]`) to false `"23"` (codes `[50,51]`).

The mutation builds successfully in
`evidence/stage6-false-mutation-build.log` (exit 0). Its proof then exits 1 with
`WarnStuckClaimState`: the fully evaluated actual result is
`str(iCons(50,iCons(50,.IntSeq)))`, which cannot unify with the false
destination. This is an expected, reachable unmet result obligation—not a
parse error, timeout, missing import, or unrelated crash. See
`evidence/stage6-false-mutation-proof.log`.

Together with the independent body mutation in stage 4, this establishes both
result sensitivity and program-body sensitivity.

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied MPY K definition and K's reachability logic, from the exact
configuration in `SPEC.change-base`, for every mathematical integer `X` and
every integer base `B` satisfying `2 <= B < 10`, the exact submitted function
returns:

- `"0"` when `X = 0`;
- the sequence of ASCII digit codes obtained by repeated quotient/remainder
  decomposition when `X > 0`; or
- `"-"` followed by that sequence for `-X` when `X < 0`.

The loop invariant covers symbolic, unbounded magnitudes; this is not a bounded
unrolling, finite-size theorem, or proof of examples. It also restores the
specified heap, stack, exception, return, scope-location, and exit-code cells.
As requested, the conclusion is treated as a partial-correctness result; no
separate source-language termination theorem is claimed.

### Trust and assumption boundary

The proof assumes:

- the integrity-checked supplied MPY semantics and trusted translator;
- the K 7.1.293 parser, compiler, Haskell backend, reachability/circularity
  implementation, SMT reasoning, and K's built-in `Int`, `Bool`, `String`,
  `Map`, `List`, equality, and arithmetic primitives;
- the reachable MPY rules for scopes, calls, control flow, integer operations,
  strings, and `chr`; these were statically reviewed and concretely exercised;
  and
- the ordinary mathematical bridge that recursive quotient/remainder digit
  codes denote the requested base representation.

There is no proof-local opaque symbol, empirical semantic replacement, or
trusted rewrite. Differential testing supports only the Python-to-contract
bridge on tested inputs; it is not used in place of the K proof. The fixed
semantics contains the unreachable opaque symbols listed in stage 5, but none
occurs in the initial term, postcondition, or any reachable rule path.

The remaining uncertainty is therefore about informal source intent at
`x <= 0` and the absence of a separate positional-value theorem, not about
whether the K proof executes or constrains the submitted program. That matches
the benchmark's `CONCERNS / LEGIT` boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
