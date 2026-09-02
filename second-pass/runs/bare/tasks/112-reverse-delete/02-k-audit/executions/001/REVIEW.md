# Adversarial proof audit: 112-reverse-delete

## Executive decision

The candidate's submitted K claims do rebuild and close, and the claims constrain
the returned tuple.  They do not constitute a legitimate proof of the real
Python program.  The generated semantics uses K's byte-indexed string operations
as if they were Python's Unicode-code-point operations, and the discrepancy is
observable on the actual submitted program:

- `reverse_delete("🙂a🙂", "")` returns `("🙂a🙂", True)` in both trusted
  canonical Python and candidate Python, while fresh `krun` returns the same
  string with `false`.
- `reverse_delete("🙃", "🙂")` returns `("🙃", True)` in Python, while fresh
  `krun` filters the shared UTF-8 prefix bytes and returns the invalid byte
  string `"\x83"` with `true`.

In addition, the only `For` rule is a task-specific operational bridge that
rewrites the entire loop directly to `deleteChars`.  There is no iterative
`For` execution or auxiliary connection theorem.  The rule is false on its
declared match domain, as demonstrated by the preserved ASCII aliasing witness.
The postcondition then uses the same `deleteChars` and `reverseString` symbols,
so `#Top` follows inside the candidate's theory without proving that those
symbols have the real program's meaning.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`.  `/reference/reference-semantics`
does not exist, including as a dangling symlink, so the trusted mounts do not
contradict the mode.  There is no infrastructure breach.

The required root artifacts `run-input.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh` are
all regular files.  `prove.sh` is executable.  There are no symlinks anywhere
under `/candidate`.  The only root K sources are the required three K files;
there are no additional helper K files.  The candidate-supplied
`*-kompiled/` directories and `__pycache__/` were classified as generated
material and were never copied or used.

The prompt is byte-identical to `/reference/prompt.py`:
`1a0e5435912522547470d17b91604c47dbff24e81d145a7f2b79c281eef6b033`.
The translator is byte-identical to `/reference/py2mpy.py`:
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
No required artifact is missing, changed, mistyped, unexpectedly added, or
symlinked.

The structured generation trace is present as one regular JSONL file.  I read
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
trace only as untrusted provenance.  They claim a successful generation,
1,000 differential tests, and an all-claims `#Top`; none of those claims was
used in place of reconstruction.

Evidence:

- [01-integrity.log](/audit-output/evidence/01-integrity.log)
- [integrity_check.py](/audit-output/evidence/integrity_check.py)
- [02-untrusted-provenance-claims.log](/audit-output/evidence/02-untrusted-provenance-claims.log)
- [provenance_claims.py](/audit-output/evidence/provenance_claims.py)

## 2. Program fidelity and candidate-versus-canonical checks

The natural-language contract is: for Python strings `s` and `c`, retain in
order every character of `s` that is not a character of `c`; return the
filtered string together with whether that filtered string reads the same
forward and backward.  The trusted canonical implements this with a
comprehension/join followed by `s[::-1] == s`.

The candidate Python uses a left-to-right loop, appending `ch` exactly when
`ch not in c`, then compares the result with `result[::-1]`.  It is a different
implementation of the same algorithm for Python-string inputs.

I ran the trusted translator from the scratch copy:

```text
python3 py2mpy.py solution.py
```

The result was byte-identical to submitted `solution.mpy` (both SHA-256
`f000e03ceb98957592a0d397f7e51aad729823b556ab7fdfb749b5fb8defc28e`).

An independent differential script imported the trusted canonical entry point
from `/reference/canonical.py` and the scratch candidate entry point.  Its
2,424 preserved inputs comprise the three examples, 16 explicit boundary and
branch cases, all 1,905 pairs with `s` over `"ab"` through length 6 and `c`
through length 3, and 500 seed-112 generated ASCII/Unicode cases.  It found
zero mismatches.  This supports Python implementation fidelity, including
Unicode behavior, but is finite evidence rather than a proof.

Evidence:

- [03-regenerate-solution-mpy.log](/audit-output/evidence/03-regenerate-solution-mpy.log)
- [04-mpy-byte-identity.log](/audit-output/evidence/04-mpy-byte-identity.log)
- [05-mpy-hashes.log](/audit-output/evidence/05-mpy-hashes.log)
- [differential_test.py](/audit-output/evidence/differential_test.py)
- [differential-inputs.json](/audit-output/evidence/differential-inputs.json)
- [06-python-differential.log](/audit-output/evidence/06-python-differential.log)

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/112-reverse-delete`.  No candidate-compiled definition or
cache was copied.  The live tools were K `v7.1.293` and Python `3.10.12`
([33-tool-versions.log](/audit-output/evidence/33-tool-versions.log)).

Fresh concrete build:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled
```

This exited 0.  The exact log is
[07-kompile-semantic-llvm.log](/audit-output/evidence/07-kompile-semantic-llvm.log).

The corrected concrete comparison executed the actual regenerated
`solution.mpy` on 12 normal and boundary inputs.  Ten ASCII/combining-mark
cases matched both Python implementations.  Two valid Unicode cases materially
diverged, and the comparison exited 1 because of those mismatches:

```text
S="🙂a🙂", C=""  : K ("🙂a🙂", false), Python ("🙂a🙂", True)
S="🙃", C="🙂"   : K (b"\x83", true), Python ("🙃", True)
```

The full commands, inputs, parsed outputs, exit statuses, and mismatch count
are in
[10-concrete-semantics-compare-final.log](/audit-output/evidence/10-concrete-semantics-compare-final.log),
with inputs in
[concrete-semantics-inputs.json](/audit-output/evidence/concrete-semantics-inputs.json).
The two raw `krun`/Python pairs are
[19](/audit-output/evidence/19-krun-unicode-palindrome-witness.log),
[20](/audit-output/evidence/20-python-unicode-palindrome-witness.log),
[21](/audit-output/evidence/21-krun-unicode-membership-witness.log), and
[22](/audit-output/evidence/22-python-unicode-membership-witness.log).
Logs 08 and 09 preserve two superseded reviewer-harness parser failures; they
were diagnosed before any candidate conclusion, fixed in the preserved script,
and replaced by log 10.

Fresh proof build:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

This exited 0
([11-kompile-verification-haskell.log](/audit-output/evidence/11-kompile-verification-haskell.log)).
The submitted all-claims command then exited 0 and printed exactly `#Top`
([12-kprove-original-all-claims.log](/audit-output/evidence/12-kprove-original-all-claims.log)).

I added labels without changing the claims and independently selected all four:

- universal: exit 0, `#Top`
  ([13-kprove-universal.log](/audit-output/evidence/13-kprove-universal.log));
- example 1: exit 0, `#Top`
  ([14-kprove-example-1.log](/audit-output/evidence/14-kprove-example-1.log));
- example 2: exit 0, `#Top` on the serial run
  ([17-kprove-example-2-serial.log](/audit-output/evidence/17-kprove-example-2-serial.log));
- example 3: exit 0, `#Top`
  ([16-kprove-example-3.log](/audit-output/evidence/16-kprove-example-3.log)).

An initial parallel example-2 launch hit a transient Java detection error; it
is preserved in log 15 and is not treated as candidate evidence because the
serial rerun closed normally.  The labeled audit spec is
[spec-audit.k](/audit-output/evidence/spec-audit.k).

Thus the positive reconstruction gate itself passes: all positive claims close
under the freshly built candidate theory.  The generated-semantics concrete
gate fails because that theory does not execute the real Python behavior on
the intended string domain.

## 4. Adequacy and real-program pinning

There are no `requires` clauses.  Each precondition is therefore `true` for
well-sorted K `String` inputs.

- The universal claim says: for arbitrary K strings `S` and `C`, executing
  `solutionPgm` reaches exactly `returned(expectedResult(S,C))`.
- Each example claim starts from one prompt input and reaches an exact concrete
  `tupleVal(strVal(...), boolVal(...))`.

Every claim is satisfiable.  For example,
`<k> execute(solutionPgm, "abcde", "ae") </k>` is a concrete starting state.
It reaches `returned(tupleVal(strVal("bcd"), boolVal(false)))`, which agrees
with both Python implementations.  The equally satisfying state with
`S="🙂a🙂"` and `C=""` reaches the wrong boolean under K, and the state with
`S="🙃"` and `C="🙂"` reaches the wrong filtered value.

The submitted spec names a hard-coded copy as `solutionPgm` rather than parsing
`solution.mpy` during `kprove`.  For this submission the copy is pinned:
trusted regeneration is byte-identical, its constructor tree is identical to
the definition, and a fresh claim embedding that exact tree directly also
exited 0 with `#Top`
([spec-direct.k](/audit-output/evidence/spec-direct.k),
[18-kprove-direct-regenerated-program.log](/audit-output/evidence/18-kprove-direct-regenerated-program.log)).
Fresh concrete runs also parse the actual file.  Therefore substitution of a
different program is not the defect here.

The destinations constrain the complete returned tuple; there is no fresh
right-hand-side result variable, tautology, or implication-only escape.  There
are no helper or loop claims to check against control flow.  Instead, the loop
is replaced inside the semantics by one ordinary rule.  The false mutation in
stage 6 confirms result constraint, but result constraint cannot repair an
unsound execution model.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory and construct mapping

`semantic.k` declares:

| Sort/declaration | Every local production | Use by submitted `solution.mpy` |
|---|---|---|
| `Pgm` | `Module(Stmts)` | outer program |
| `Stmts` | separator-free `List{Stmt,""}` | function body, branches, sequencing |
| `Stmt` | `FuncDef`, `Assign`, `For`, `If`, `Return` | all five occur |
| `Strings`, `Params` | comma list of `String`; `Params(Strings)` | `"s","c"` |
| `Expr` | `Name`, `Str`, `Int`, `UnaryOp`, `BinOp`, `Compare`, `TupleExpr`, `Subscript` | all occur, with `Int`/`UnaryOp` inside the slice step |
| `CmpOp`, `CmpOps` | `CmpOp(String,Expr)` and comma list | `"not in"` and `"=="` |
| `Exprs` | comma list of `Expr` | returned tuple |
| `Index` | `Expr` or `Slice(Bound,Bound,Bound)` | slice form |
| `Bound` | `Expr` or `NoBound` | `[::-1]` |
| `Val` | `strVal`, `boolVal`, `tupleVal` | all result components |
| `ExecResult` | `normal(Map)`, `returned(Val)` | `returned` on the target; `normal` is the empty-body result |
| configuration / `KItem` | one `<k>` cell initialized with `execute(Pgm,String,String)` | entry execution |

It additionally declares nine local `[function]` symbols across the two K
files: `exec`, `eval`, `getVal`, `asString`, `asBool`, `deleteChars`,
`reverseString`, `solutionPgm`, and `expectedResult`.  There is one local
`[simplification]` rule, for empty-string concatenation.  There are no
`[total]` declarations, no `functional` attributes, no priority rules, no
`owise` rules, and no proof-local opaque result symbols.  AST/value/result
productions are free constructors.  Partial functions have no equations for
unsupported syntax or wrong value types, so such uses stop visibly.
`verification.k` adds only `solutionPgm` and `expectedResult`; `spec.k` adds
four claims and no rules.  There are no generated helper K files.

The actual construct path is:

```text
Module/FuncDef/Params
  -> execute initializes the map
  -> Assign initializes result
  -> specialized For/If/Compare/BinOp pattern is consumed as one summary
  -> Return evaluates TupleExpr
  -> Name plus Compare("==") plus exact [::-1] Subscript
  -> returned(tupleVal(...))
```

Thus syntax coverage exists, but the `For` and its body do not execute through
the ordinary `If`, `Compare`, `Assign`, and sequencing rules.

### Exhaustive rule assessment

The numbered source is preserved in
[27-semantic-source-numbered.log](/audit-output/evidence/27-semantic-source-numbered.log),
[28-verification-source-numbered.log](/audit-output/evidence/28-verification-source-numbered.log),
and [29-spec-source-numbered.log](/audit-output/evidence/29-spec-source-numbered.log).

| Rule | Assessment |
|---|---|
| `getVal`, line 62 | Correct lookup for a present unique Map key; intentionally partial for an unbound name. |
| `asString`, line 63 | Correct projection from `strVal`; partial on other values. |
| `asBool`, line 64 | Correct projection from `boolVal`; partial on other values. |
| `"" +String S => S`, line 68 | True string identity.  Its simplification attribute does not introduce a false equation. |
| `deleteChars("",_)`, line 70 | Correct byte-string base case. |
| `deleteChars` delete branch, lines 71–74 | The guard is disjoint from the keep branch and recursion decreases hooked string length, but “one unit” is one byte in these concrete hooks, not one Python character.  As part of the loop bridge it enables the exact false target conclusion `S="🙃", C="🙂"`: K returns byte `83`, Python retains `🙃`. |
| `deleteChars` keep branch, lines 75–79 | Internally complementary and decreasing over K bytes, but has the same invalid Python-character bridge.  The two recursive branches are exhaustive for nonempty hooked strings because `findString` returns either a negative or nonnegative integer. |
| `reverseString("")`, line 81 | Correct base case. |
| `reverseString` recursive branch, lines 82–85 | Internally reverses byte units.  It is not Python `[::-1]`.  False-conclusion witness on the submitted program: `🙂a🙂` is a Python palindrome but K reports `false`. |
| `eval(Name)`, line 87 | Correct for a bound name. |
| `eval(Str)`, line 88 | Correct literal wrapping. |
| `eval(BinOp("+"))`, lines 89–90 | Correct string concatenation for this pure, well-typed target expression.  The model omits Python type errors, excluded by K `String` inputs. |
| `eval(Compare "not in")`, lines 91–93 | Implements hooked string-substring non-membership.  It is not reached for loop iterations because the whole loop is summarized.  It is internally consistent for valid byte encodings but is not a proof of character iteration. |
| `eval(Compare "==")`, lines 94–95 | Correct equality of represented strings/bytes. |
| `eval(TupleExpr)`, lines 96–97 | Correct pair construction.  Evaluation-order omissions are immaterial for the target's pure subexpressions. |
| `eval(Subscript(...[::-1]))`, lines 98–99 | Materially unsound as Python slicing: it calls byte `reverseString`.  The concrete `🙂a🙂` witness above is on the actual target path. |
| `exec(.Stmts)`, line 101 | Correct normal completion of an empty statement list. |
| `exec(Assign)`, lines 102–103 | Evaluates in the old environment then updates the target name; correct for target pure expressions. |
| true `exec(If)`, lines 104–106 | Correct branch/continuation concatenation when the evaluated condition is true. |
| false `exec(If)`, lines 107–109 | Complement of the preceding guard; correct when the evaluated condition is false. |
| `exec(Return)`, line 110 | Produces the evaluated return value and discards the remaining function-body statements, matching return control for this stack-free entry model. |
| specialized `exec(For...)`, lines 115–127 | Illegitimate operational bridge.  It recognizes the task's entire filtering idiom and directly writes `oldResult + deleteChars(oldSource,oldC)` for arbitrary identifier aliases and arbitrary `REST`.  There is no iteration semantics or connection theorem.  It also does not bind `CH`.  Exact target Unicode witnesses are already false.  Independently, the valid matched ASCII alias program `if ch not in result: result += ch` on `s="aba"` returns `("ab",False)` in Python but this rule returns `("aba",true)`; see logs 23–24.  With the original loop followed by `return ch`, Python returns `"b"` but K stops at unbound `ch`; see logs 25–26.  These are concrete witnesses, not merely evidence gaps. |
| entry `execute`, lines 129–136 | Correctly selects the named two-parameter entry and initializes `s` and `c` for this narrow task.  General Python calls, frames, defaults, and module effects are unmodeled but unused. |
| `solutionPgm`, `verification.k` lines 14–31 | A truthful definitional name for the submitted constructor tree, independently pinned in stage 4. |
| `expectedResult`, `verification.k` lines 34–38 | A consistent definition of a K-byte result, but not the Python contract on Unicode.  It uses the same `deleteChars` and `reverseString` that drive execution, so it supplies no independent connection theorem for those program-derived summaries. |

The specialized loop's ASCII false conclusion is preserved in
[loop-rule-alias-witness.mpy](/audit-output/evidence/loop-rule-alias-witness.mpy),
[loop_rule_alias_witness.py](/audit-output/evidence/loop_rule_alias_witness.py),
[23-krun-loop-alias-false-conclusion.log](/audit-output/evidence/23-krun-loop-alias-false-conclusion.log),
and [24-python-loop-alias-expected.log](/audit-output/evidence/24-python-loop-alias-expected.log).
The arbitrary-continuation/control-state witness is preserved in
[loop-rule-context-witness.mpy](/audit-output/evidence/loop-rule-context-witness.mpy),
[loop_rule_context_witness.py](/audit-output/evidence/loop_rule_context_witness.py),
[25-krun-loop-context-residual.log](/audit-output/evidence/25-krun-loop-context-residual.log),
and [26-python-loop-context-expected.log](/audit-output/evidence/26-python-loop-context-expected.log).

The configuration has only `<k>`; the environment Map is an argument of
`exec`.  That is sufficient for this pure target's local bindings and immutable
strings.  There is no heap, allocation, output, exception, or call-stack state.
The lack of exception semantics is acceptable only under the formal K-String
input restriction.  It does not excuse the Unicode mismatch because both
counterexamples are ordinary, well-typed Python strings.

## 6. Fresh non-vacuity test

I created a new concrete claim for the satisfying input
`S="abcde", C="ae"` and changed only the result string from the true `"bcd"`
to false `"bcdx"`, leaving the boolean `false`.  The mutation is
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k).

Its dry run:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims SPEC-VACUITY-AUDIT.false-result --dry-run
```

exited 0, demonstrating successful parsing/build
([31-vacuity-mutation-dry-run.log](/audit-output/evidence/31-vacuity-mutation-dry-run.log)).
The actual proof command exited 1.  Its residual was the reached
`returned(tupleVal(strVal("bcd"),boolVal(false)))`, followed by
`WarnStuckClaimState` because that term does not unify with the mutated
destination.  This is the expected unmet result obligation, not a parser error,
timeout, or unrelated crash
([32-vacuity-mutation-proof-fails.log](/audit-output/evidence/32-vacuity-mutation-proof-fails.log)).

The claim is therefore non-vacuous and result-discriminating.  This gate passes
but does not validate the semantics.

## 7. Proven-versus-assumed accounting

What successful `kprove` precisely establishes is:

> Under the candidate K theory, for every K `String` pair `S,C`, the hard-coded
> submitted AST rewrites to the tuple made from the candidate's byte-recursive
> `deleteChars(S,C)` and its equality with the candidate's byte-recursive
> `reverseString`.

It does not establish that byte-recursive summary as the result of real Python
character iteration or slicing.

| Boundary | Dependents | Status |
|---|---|---|
| Trusted translator and byte identity | program syntax pinning | Acceptable syntactic bridge; independently reconstructed. |
| Imported K Map/Bool/Int/String hooks | all local semantics | Acceptable primitives for a theorem about K's own domains.  The String hooks are not an acceptable unqualified model of Python `str` here because exact valid-Unicode witnesses diverge. |
| `solutionPgm` duplicate | every spec claim | Acceptable for this artifact after byte/constructor identity and the direct-program proof. |
| `deleteChars` as whole-loop result | universal claim and all examples | Illegitimate program-derived operational bridge.  No iterative execution or universal connection theorem; exact and alias false witnesses exist. |
| `reverseString` as Python `[::-1]` | returned palindrome flag and postcondition | Illegitimate semantic bridge on Unicode; exact target false witness exists. |
| `expectedResult` | universal postcondition | Definitional only.  It repeats the same summary symbols used by execution, which is circular rather than independent correctness evidence. |
| Python differential run | Python candidate-to-canonical bridge | Strong finite support over 2,424 documented inputs, but not a K proof and not a repair for the K divergences. |
| Concrete K/Python comparison | generated-semantics adequacy | Decisive negative evidence: two mismatches among 12 selected cases. |
| Termination | theorem interpretation | The task asks partial correctness.  Concrete recursive helper calls decrease byte length, but no separate theorem connects or proves Python termination; no total-correctness conclusion is claimed. |

There are no local opaque result symbols beyond imported hooked primitives.
No candidate `PROOF.md`, trace, differential claim, or candidate-built
definition was treated as formal evidence.

Gate accounting:

- Gate A, real-program soundness: **FAIL**.  The `For` operational bridge has
  no connection theorem and has concrete false conclusions; the exact target
  also diverges on valid Unicode.
- Gate A5, result constraint/non-vacuity: **PASS**.
- Gate B, intent adequacy: **FAIL**.  The formal K-byte theorem does not cover
  the stated Python-string contract.
- Gate C, evidence auditability: **PASS for this audit record**.  Exact
  commands, statuses, inputs, raw witnesses, and bounded logs are preserved,
  but good evidence cannot make the unsound theorem legitimate.

The reconstructed `#Top` is real but proves the wrong semantic model.  Under
the required decision boundary, materially unsound generated semantics and an
answer-encoding, unconnected operational bridge require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
