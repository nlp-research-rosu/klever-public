# Independent adversarial audit: 23-strlen

Decision: **CONCERNS / LEGIT**. I independently rebuilt the supplied semantics and
the proof from source, proved the sole positive claim with `#Top`, checked that
the claim executes the exact translated program, and obtained the expected
failures from both a false postcondition and a changed function body. The
remaining concerns are provenance/evidence limitations, not a soundness defect:
four requested generation-record files are absent, and the bridge from Python
Unicode strings to the proof's over-broad `IntSeq` representation is not itself
a universal machine-checked theorem.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is a real directory.
There is therefore no infrastructure breach requiring `AUDIT_ERROR`.

I recursively compared entry names, entry types, and SHA-256 contents between
the trusted and candidate semantics trees without following symlinks. Both
trees contain the same two directories and 24 regular files. There are no
missing, additional, mistyped, changed, or symlinked entries in
`/candidate/reference-semantics`; every file hash matches. The candidate
`prompt.py` and `py2mpy.py` are also regular files and byte-identical to the
trusted versions. The complete comparison and candidate inventory are in
[01-integrity.log](evidence/01-integrity.log), produced by
[integrity_check.py](evidence/integrity_check.py).

The proof sources `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are present as regular files. Candidate `prove.sh` was read
only as an untrusted claim and was not used as the audit driver. The candidate
also contains `__pycache__/solution.cpython-310.pyc`; I treated it as an
untrusted extra, did not execute it, and did not copy it to scratch.

The following requested generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace, `PROOF.md`, or candidate `spec-vacuity.k` is
present. Their absence limits provenance and prior-run auditability, but none is
used as a premise of the reconstructed proof.

All source needed for execution was copied to
`/tmp/audit-work/23-strlen`; no candidate-built definition or cache was copied.
The exact copy command and resulting tree are in
[02-scratch-copy.log](evidence/02-scratch-copy.log). The environment record is
[00-environment.log](evidence/00-environment.log); the live tools were K
v7.1.337 and Python 3.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a Python `str`, return its length. Its documented
examples are `strlen("") == 0` and `strlen("abc") == 3`. The trusted canonical
implementation returns Python's `len(string)`.

The submitted `solution.py` is:

```python
def strlen(string: str) -> int:
    return len(string)
```

Thus its implementation is the same expression as the canonical entry point
over the intended domain of Python strings. It has no conditionals, loops, or
other branch boundaries.

I ran the trusted translator from scratch on the submitted Python source. The
regenerated and submitted `solution.mpy` files are byte-identical and have the
same SHA-256 hash,
`508c92dec7b8810291f0fa18ef567c25d5e8f398d62952cff2bd359697d6aebf`.
See [03-translation-fidelity.log](evidence/03-translation-fidelity.log).

The independent differential test
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and submitted Python entry points separately. It checked 510
deterministic string inputs: the two documented examples; lengths zero, one,
and two; whitespace; embedded NUL; BMP, astral, and combining Unicode;
a 4096-character string; and 500 seed-230023 generated strings of lengths
0 through 256. Both implementations also matched Python's direct structural
length on every case. There were zero mismatches and exit status was zero:
[04-differential.log](evidence/04-differential.log). The complete generated
inputs and per-case results are preserved in
[03-differential-cases.json](evidence/03-differential-cases.json).

This differential run is finite evidence. Universal source-level alignment is
stronger here because the submitted and canonical function bodies are the same
`return len(string)` expression.

## 3. Clean proof reconstruction

I did not reuse a candidate definition or cache.

First, I compiled the copied supplied semantics with the LLVM backend:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited zero. The compiler reported non-exhaustiveness warnings for several
unused, declared-total helpers; those warnings are accounted for in Stages 5
and 7. The exact command and bounded output are in
[05-kompile-runtime.log](evidence/05-kompile-runtime.log).

Concrete execution of the submitted `solution.mpy` exited zero and reached
`.K`, with the exact `strlen` closure installed, no exception, and exit code
zero: [06-krun-submitted-module.log](evidence/06-krun-submitted-module.log).
The independent concrete program
[concrete-tests.mpy](evidence/concrete-tests.mpy) loaded the same body and
asserted lengths for `""`, `"x"`, `"abc"`, and `"a\nb"`. It also reached `.K`
with `NoExc` and exit code zero:
[07-krun-concrete-tests.log](evidence/07-krun-concrete-tests.log).

Next, I compiled the proof definition with the Haskell backend:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The build exited zero; see
[08-kompile-verification.log](evidence/08-kompile-verification.log).
The target inventory contains exactly one positive claim and no helper claims:
[09-positive-claim-inventory.log](evidence/09-positive-claim-inventory.log).
I independently ran:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited zero and printed `#Top`:
[10-kprove-spec.log](evidence/10-kprove-spec.log).

Stage 3 therefore passes. The success is treated only as closure under the
freshly built theory; the separate soundness and non-vacuity gates follow.

## 4. Adequacy and real-program pinning

### Entry precondition and postcondition

The entry claim has no side `requires` clause. Its precondition says:

- `S` is any finite K term of sort `IntSeq`;
- `<k>` contains `#invokeStrlen(str(S))`;
- execution starts in module environment 0;
- module scope 0 is empty with the builtins frame at scope `-1`;
- the next scope location is 1;
- heap and stack are empty;
- return state is `noRet`, exception state is `NoExc`, and exit code is 0.

This is satisfiable. In particular, both `S = .IntSeq` and
`S = iCons(97, iCons(98, iCons(99, .IntSeq)))` satisfy it.

The postcondition says `<k>` is exactly `isLen(S)`, not an existential or free
result. The same input variable `S` occurs on both sides, and `isLen` has the
exhaustive recursive equations
`isLen(.IntSeq) = 0` and
`isLen(iCons(_, R)) = 1 +Int isLen(R)`. The postcondition also requires the
loaded `strlen` closure to remain in module scope and requires all temporary
call state to be restored: scope location 1, empty heap and stack, `noRet`,
`NoExc`, and exit code 0.

The ground claims in [adequacy-ground.k](evidence/adequacy-ground.k) substitute
the two satisfying inputs above and require results 0 and 3. Both claims close
with `#Top` and exit zero:
[12-ground-adequacy.log](evidence/12-ground-adequacy.log). The corresponding
Python inputs are the documented empty and `abc` cases; both the trusted and
submitted implementations return the same 0 and 3 values in
[03-differential-cases.json](evidence/03-differential-cases.json).

### Pinning and control flow

The proof does not read `solution.mpy` dynamically. Instead,
`verification.k:7-15` defines a macro whose constructor tree is:

```text
Module(
  FuncDef("strlen", Params("string"),
    Return(Call(Name("len"), Name("string")))))
```

That is exactly the byte-verified submitted `solution.mpy`. This explicit
identity check is essential: without it, an embedded AST could prove a
substituted program.

`#invokeStrlen` is a fresh harness constructor. Its sole rule expands it to
`#loadAll(strlenModule) ~> Call(Name("strlen"), V)` while preserving any
surrounding continuation. It does not rewrite or summarize an existing
MiniPython construct. Fixed semantics then:

1. opens the exact module and executes its `FuncDef`;
2. looks up the resulting `strlen` closure;
3. enters a real call frame and binds `string` to `str(S)`;
4. executes the actual `Return(Call(Name("len"), Name("string")))`;
5. resolves `len` through the exact builtin frame;
6. dispatches `len(str(S))` to `seqLen(str(S))` and then `isLen(S)`;
7. returns through the real frame-pop rule and restores every constrained cell.

There are no loop claims or helper summaries to mismatch with control flow.
The function body, builtin lookup, argument binding, call, return, and state
updates all execute. The proof-local rules introduce no result oracle.

The formal input domain is slightly over-broad: an `IntSeq` may contain
integers that are not valid Python Unicode scalar values. This cannot falsify
the intended result because the only observation is the number of sequence
constructors, but it is an informal representation bridge and contributes to
the `CONCERNS` rather than `PASS` verdict.

## 5. Rule-by-rule static soundness review

The exhaustive line-addressed inventory is
[11-rule-inventory.md](evidence/11-rule-inventory.md), generated by
[rule_inventory.py](evidence/rule_inventory.py) with the command and totals in
[11-rule-inventory-generation.log](evidence/11-rule-inventory-generation.log).
It covers `semantics.k`, every helper K file, `verification.k`, and `spec.k`:
26 sources and 933 local constructs in total.

The inventory contains:

- 229 syntax declarations, including 146 `[function]`, 107 `[total]`,
  25 `[symbol]`, 22 `[no-evaluators]`, five `[macro]`, one `[macro-rec]`,
  two `[strict]`, and one `[seqstrict]` occurrence;
- one configuration and five explicit contexts;
- 697 rules, including 45 priority, 26 `owise`, and 35 `concrete`
  occurrences;
- one reachability claim;
- no explicit `[functional]` declaration and no simplification rule.

The inventory records the full text, attributes, file, and line of every item.
Each rule is classified as either an exact used-path rule or a fixed,
non-matching rule. The semantic files contain 695 rules; 23 are on the unique
`strlen` path and 672 cannot be reached by this program. `verification.k` adds
two rules.

### Used syntax and rules

| Program construct | Declaration and execution rules | Static decision |
|---|---|---|
| `Module` and statement list | `syntax.k:61`; `core.k:125-127` | Opens and sequences exactly the submitted single definition. |
| `FuncDef`, `Params` | `syntax.k:53,57,60`; `functions.k:14` | Installs the real closure and exact body in scope 0. |
| `Return` | `syntax.k:50` `[strict]`; `functions.k:78,85` | Evaluates the body expression, returns its value, restores caller state, and discards only the callee-local tail. |
| `Call` | `syntax.k:28`; `call.k:20-21,31,69`; `core.k:189-191` | Preserves callee-before-argument and left-to-right argument evaluation, enters the real closure, and dispatches the resolved builtin. |
| `Name` | `syntax.k:12`; `core.k:131-132,152,158` | Resolves `strlen`, `string`, and `len` through the exact scope chain; no binding is pinned by name alone. |
| `str(S)` and length | `core.k:15,227-229`; `builtins.k:21,24` | Transparently computes structural length; equations are exhaustive, disjoint, and descend on the tail. |
| Proof harness | `verification.k:7-20` | Exact AST macro plus a fresh driver expansion; no execution is bypassed. |

The applicable rules have disjoint or agreeing overlaps:

- The cell-aware lookup and parameter rules require a `"$cells"` marker, absent
  from both the ordinary call frame and module/builtin frames here.
- Heap-dereference call routes require `ref(_)`; the input is the bare value
  `str(S)`.
- Special call intercepts require syntactic `math`/`hashlib` attributes, not
  either `Name("strlen")` or `Name("len")`.
- Fold builtins require names `sum`, `all`, `any`, `max`, or `min`; only the
  generic `len` dispatch applies.
- The `seqLen(str(IS))` equation is constructor-disjoint from its list, tuple,
  set, and range equations.
- `isLen` covers both and only the two `IntSeq` constructors, and recursion
  strictly descends.

The proof-local macro is compile-time syntax expansion. The `#invokeStrlen`
rule matches only the newly declared harness symbol, preserves the arbitrary
continuation denoted by `...`, and produces fixed-semantics terms. It reads or
writes no cell itself. It is therefore a definitional harness, not an
operational bridge over a program-defined operation. There is no proof-local
function, totality assertion, opaque symbol, priority rule, simplification,
lemma, or helper claim.

### Unused rules, priorities, totals, and opaque symbols

I inspected every remaining inventory entry for a syntactic or guarded overlap
with the path above. The modules for assertions, booleans, comprehensions,
control statements, dictionaries, floats, integer operators, iterators,
lists, methods, comparisons, ranges, sets, sorting, string literals/methods,
subscripts, tuples, and LLVM-only concrete support require constructors,
callee names, operators, receivers, or control markers that this AST never
creates. Within the otherwise-used core/call/function/builtin modules, the
unused rules are separated by those same constructor, name, heap-reference, or
cell-frame tests. Consequently none can affect control, result, scopes, heap,
stack, return state, exception state, or exit code for an intended input.

The supplied semantics declares these 25 symbolic/opaque primitives:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. None occurs in the submitted AST, reachable
state, target result, or postcondition. They have no dependent claim here.

LLVM compilation warned that the declared-total `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt` equations are not exhaustive over their
declared sorts. This is a real limitation of the larger supplied MiniPython
subset. Totality leaves unmatched cases defined but opaque; it does not assert
a contradictory value. None of these symbols is reachable in this theorem.
Other fixed rules intentionally model only a valid-program subset (for
example, ASCII string literals and omitted Python exception cases). I do not
promote those comments into general Python-correctness claims.

I found no rule that enables a false conclusion for `strlen` on the intended
string domain, so I do not label any rule unsound. Accordingly, no unsoundness
witness is asserted. For the unrelated partial/opaque portions, the narrower
finding is an evidence and coverage gap outside this theorem, not an
intended-domain false conclusion.

Finally, the body-sensitivity experiment changed the embedded function body to
`return 0` while retaining the structural-length obligation. The mutant
definition and spec are
[verification-body-mutant.k](evidence/verification-body-mutant.k) and
[spec-body-mutant.k](evidence/spec-body-mutant.k). They compiled and dry-ran
successfully ([15-body-mutant-build.log](evidence/15-body-mutant-build.log)),
but proof exited 1 with a meaningful `WarnStuckClaimState` residual
`0 = isLen(S)` ([16-body-mutant-proof.log](evidence/16-body-mutant-proof.log)).
This confirms that the successful theorem is sensitive to the actual body.

## 6. Fresh non-vacuity test

I did not rely on candidate non-vacuity evidence. The fresh mutation
[spec-vacuity.k](evidence/spec-vacuity.k) changes the result-constraining
postcondition from `isLen(S)` to `isLen(S) +Int 1`, leaving the same program,
precondition, and state obligations.

This mutation is demonstrably false in the satisfiable empty-string state:
the real and formal results are 0, while the mutation demands 1.

`kprove --dry-run` parsed and compiled the mutation successfully with exit
status 0: [13-vacuity-dry-run.log](evidence/13-vacuity-dry-run.log). The actual
proof then exited 1, reported `WarnStuckClaimState`, and displayed the expected
failed implication between `isLen(S)` and `isLen(S) +Int 1`:
[14-vacuity-proof.log](evidence/14-vacuity-proof.log). This was an unmet,
reachable result obligation—not a parser error, missing import, timeout, or
unrelated crash.

Stage 6 passes.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly compiled supplied K semantics, for every finite `S:IntSeq`,
starting from the exact clean state in `spec.k`, loading the exact submitted
translated module and invoking its `strlen` closure on `str(S)` reaches a
terminal result `isLen(S)`. The loaded module binding persists, the temporary
call scope and frame are removed, heap and allocation counters are unchanged,
and return, exception, and exit-code cells are restored to the claimed values.
This is a partial-correctness reachability theorem. It is not replaced by the
Python differential tests.

### Trust ledger

| Boundary | Dependents and evidence | Judgment |
|---|---|---|
| K v7.1.337 compiler, LLVM/Haskell backends, and K builtin theories for maps, lists, integers, strings, and equality | All machine-checking; fresh build/proof logs 05-10 and mutation logs 13-16 | Necessary low-level toolchain trust; acceptable. |
| Supplied MiniPython semantics | The formal theorem; candidate tree is recursively identical to the trusted mounted tree | Required fixed semantics for this mode; acceptable. Proof-local rules were audited separately. |
| Transparent `len(str(S)) = isLen(S)` and recursive `isLen` equations | The final result directly depends on these ordinary fixed rules | Fully explicit and exhaustive over `IntSeq`; acceptable, not an oracle. |
| Trusted `py2mpy.py` and the embedded-AST identity check | Pins Python source, submitted `.mpy`, and the proof macro | Trusted translator was used independently; submitted and regenerated `.mpy` are byte-identical. Acceptable for real-program pinning. |
| Python `str` to K `str(IntSeq)` representation | Bridge from the formal theorem to the natural-language Unicode contract | Structural length is representation-independent and source matches canonical; 510 finite Python tests support it. No universal machine-checked encoding theorem is supplied, so this is a documented concern. |
| Trusted canonical implementation and prompt | Establish natural-language intent | Submitted implementation uses the identical `return len(string)` body. Acceptable. |
| The 25 fixed opaque symbols listed in Stage 5 | No dependency: none reaches this program, result, or claim | Inert here. They neither support nor weaken this theorem. |
| Differential and ground tests | Support source/intent and concrete bridge only | Finite empirical evidence, not a substitute for the K proof. |
| Missing generation records | No formal dependency | Provenance limitation and a reason for `CONCERNS`, not a false theorem. |

The proof does not establish behavior for non-string Python arguments,
monkey-patched builtin environments, resource exhaustion, or the full Python
exception model. It also does not prove universal semantic correctness of the
translator or validate every arbitrary integer in `IntSeq` as a Unicode scalar.
Those exclusions do not alter `strlen` on the intended clean, string-valued
domain.

The reconstructed proof is sound, discriminating, result-constraining, and
pinned to the actual generated program. The over-broad but harmless string
representation and incomplete generation provenance warrant concerns, but
neither permits a false intended result or makes the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
