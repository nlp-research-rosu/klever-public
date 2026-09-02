# Independent adversarial audit: 80-is-happy

## Headline

The candidate's K theory rebuilds cleanly, all original claims close with
`#Top`, the claims constrain the result, and a fresh false-result mutation is
rejected. The submitted `solution.mpy` is also byte-faithful to `solution.py`,
and `verification.k` contains the same constructor tree.

That is not sufficient for the requested verdict. The submitted Python program
replaces the canonical loop with one Python call per character, while the
generated K semantics models user calls with an unbounded pure recursive
function. On the valid input `"abc" * 400` (length 1200), the fresh K
definition returns `pyBool(true)` and the trusted canonical Python returns
`True`, but the actual submitted `solution.py` raises `RecursionError` under
the available CPython 3.10.12 runtime. The prompt has no length restriction.
Thus the semantics makes a false normal-return conclusion provable for a
satisfying intended-domain input. This is a material real-program adequacy
failure, not a timeout or infrastructure uncertainty.

## 1. Input and provenance integrity

The rendered mode and mounts agree. `/reference/reference-semantics` does not
exist, so there is no supplied or hidden semantics baseline to use. The audit
therefore assesses the candidate's `semantic.k` on its own merits.

All required candidate deliverables are regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. The required audit inputs `run-input.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.py`, and `py2mpy.py` are also
regular files. The complete candidate-tree scan found zero symlinks. There are
no candidate helper K files.

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`f6df53687ee0d5e99ab8d7b0e23ccaa81bf7bb578c1789277336f0016d402ac0`).
Its `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
Those hashes also match the untrusted `run-input.json` claims.

The provenance JSON is syntactically valid. The structured trace has one JSONL
file, 225 valid records, and zero parse errors. `metrics.json`,
`codex-last.txt`, `codex-output.log`, and the trace claim a successful
generation and `#Top`; none was trusted as proof evidence. Their full-file
hashes, record counts, and bounded summaries are in
[provenance-summary.log](evidence/provenance/provenance-summary.log).

The top-level `semantic-kompiled/` and `verification-kompiled/` directories are
additional generated build products, not source deliverables. They were
deliberately excluded from the scratch copy and never used. The runner metadata
and traces are additional provenance artifacts required by this audit. No
required artifact is missing, changed, mistyped, or symlinked.

Evidence:

- [provenance_summary.py](evidence/provenance/provenance_summary.py)
- [provenance-summary.log](evidence/provenance/provenance-summary.log)
- [toolchain.log](evidence/provenance/toolchain.log)

The independently used toolchain was K v7.1.293. `kup` was unavailable, but
the installed `kompile`, `krun`, and `kprove` binaries ran successfully; this
is not an infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is:

> For a Python string `s`, return `True` exactly when `len(s) >= 3` and, for
> every index `i` from 0 through `len(s)-3`, the three characters
> `s[i]`, `s[i+1]`, and `s[i+2]` are pairwise distinct. Return `False`
> otherwise.

The trusted canonical implementation checks this with a loop. The candidate
checks the first triple, returns `False` on any equality, and recursively calls
the helper on `s[1:]`; abstracting away resource limits, this is the same
algorithm.

The trusted translator regenerated a file byte-identical to the submitted
`solution.mpy`; both have SHA-256
`fd871e9b9fe673932b6f77f16595ee6a0fea1ae8d74e89c8fca2e0b11a1e604c`.
See
[translator-byte-identity.log](evidence/program-fidelity/translator-byte-identity.log).

The independent differential script covered:

- all six documented examples;
- empty, lengths 1, 2, 3, and equality at each of the three pair positions;
- later-window failures, embedded NUL, and Unicode;
- all strings over `{a, b, 🙂}` of lengths 0 through 7;
- 600 seeded strings over a seven-character mixed alphabet, lengths 0 through
  79; and
- one valid length-1200 string whose every triple is distinct.

There were 3,899 cases and exactly one mismatch:

```text
input = "abc" * 400
canonical = True
candidate = RecursionError: maximum recursion depth exceeded ...
```

This input is in the stated domain, and the prompt supplies no upper bound.
The differential command intentionally exited 1 to retain the mismatch as
visible evidence. See
[differential_test.py](evidence/program-fidelity/differential_test.py) and
[differential-test.log](evidence/program-fidelity/differential-test.log).

This is a material implementation-versus-contract divergence. It is not merely
an untested corner or a different but equivalent algorithm.

## 3. Clean proof reconstruction

Only these source files were copied to `/tmp/audit-work/fresh`:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`py2mpy.py`. No candidate definition, cache, scanner, interpreter, KORE file,
or serialized backend state was copied.

Fresh concrete definition:

```text
kompile semantic.k --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX --backend llvm \
  --output-definition semantic-audit-kompiled
exit 0
```

See [semantic-kompile.log](evidence/build/semantic-kompile.log).

The fresh concrete definition was run on 12 normal and boundary cases,
including all equality branches, a later recursive failure, Unicode, the
zero-length case, and a longer valid string. Every run exited 0 and agreed
with both Python implementations on those bounded inputs. See
[semantic_differential.py](evidence/concrete/semantic_differential.py) and
[semantic-differential.log](evidence/concrete/semantic-differential.log).

The length-1200 witness was then run against that same fresh LLVM definition:

```text
K result:          pyBool(true), exit 0
trusted canonical: True
submitted Python:  RecursionError
```

The exact input generator, digest, generated PString-term length, command
shape, exit status, and output are in
[long_recursion_witness.py](evidence/concrete/long_recursion_witness.py) and
[long-recursion-witness.log](evidence/concrete/long-recursion-witness.log).

Fresh proof definition:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module VERIFICATION --backend haskell \
  --output-definition verification-audit-kompiled
exit 0
```

See [verification-kompile.log](evidence/build/verification-kompile.log).

The untouched submitted spec then closed:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
exit 0
#Top
```

See [all-claims.log](evidence/proofs/all-claims.log).

For claim-specific reconstruction, the reviewer added labels without changing
any claim body in
[spec-labeled.k](evidence/proofs/spec-labeled.k). The recursive helper closes
alone. The universal entry claim and each of the six ground examples close
when selected together with that proved helper circularity. Every such command
exited 0 and printed `#Top`; the logs are:

- [claim-helper.log](evidence/proofs/claim-helper.log)
- [claim-entry-with-helper.log](evidence/proofs/claim-entry-with-helper.log)
- [claim-example-a-with-helper.log](evidence/proofs/claim-example-a-with-helper.log)
- [claim-example-aa-with-helper.log](evidence/proofs/claim-example-aa-with-helper.log)
- [claim-example-abcd-with-helper.log](evidence/proofs/claim-example-abcd-with-helper.log)
- [claim-example-aabb-with-helper.log](evidence/proofs/claim-example-aabb-with-helper.log)
- [claim-example-adb-with-helper.log](evidence/proofs/claim-example-adb-with-helper.log)
- [claim-example-xyy-with-helper.log](evidence/proofs/claim-example-xyy-with-helper.log)

As a diagnostic only, filtering the universal entry while removing its helper
circularity forces unbounded symbolic recursive unrolling and was stopped by a
30-second reviewer timeout. That is recorded in
[diagnostic-entry-without-helper.log](evidence/proofs/diagnostic-entry-without-helper.log);
it is not used as a candidate failure. The original collective proof and all
dependency-correct target runs closed.

## 4. Adequacy and real-program pinning

### Claims in plain language

The helper claim has no explicit `requires`. Its sort is its precondition:
for every finite `PString S`, calling the actual
`check_happy_triples` body with `pyStr(S)` must finish at exactly
`pyBool(#allTriples(S))`.

The entry claim also has no explicit `requires`: for every finite `PString S`,
calling `is_happy` must finish at exactly `pyBool(#happy(S))`.
`#happy` is false for lengths 0, 1, and 2, and otherwise equals
`#allTriples`. The six remaining claims are ground instances for the prompt
examples.

No right-hand result variable is free or existential. The `<k>` cell has no
ellipsis, and the one-cell configuration has no omitted observable state.
The result is an exact `pyBool(...)`, not an implication or tautology.

### Program identity

The proof uses `#solution`, whose sole equation expands to the submitted
constructor tree. A mechanical token comparison found 277 tokens on both
sides and exact identity after normalizing the two equivalent spellings of the
empty `Stmts` list. See
[pinning_check.py](evidence/static/pinning_check.py) and
[pinning-check.log](evidence/static/pinning-check.log). Together with trusted
translator byte identity, this rules out a substituted AST.

Concrete `krun` consumed the actual scratch copy of `solution.mpy`. Symbolic
`kprove` consumed the mechanically identical `#solution` tree. The proof file
does not dynamically import `solution.mpy`; the pin is therefore a checked
static identity rather than a K theorem about file bytes.

### Control-flow match and satisfying witnesses

The helper claim matches the real helper entry. Its base branch covers strings
shorter than three; the three equality branches match indices `(0,1)`,
`(0,2)`, and `(1,2)`; its recursive branch calls the same function on the
one-character suffix. This is the actual submitted control flow. The
circularity is reached only after `#drop(S,1)`, so there is structural
progress.

Every universal precondition is satisfiable. Examples include:

- `S = eps`: entry result `false`;
- `S = ch(97,ch(98,ch(99,eps)))` (`"abc"`): helper and entry result `true`;
- `S = ch(97,ch(98,ch(97,eps)))` (`"aba"`): helper and entry result `false`.

These substitutions agree with both Python implementations and fresh K
execution; the concrete evidence is in
[semantic-differential.log](evidence/concrete/semantic-differential.log).

The formal result is adequate for an idealized, unbounded-stack string
language. It is not adequate for the submitted Python implementation on the
full prompt domain because of the witnessed recursion exception.

## 5. Rule-by-rule static soundness review

The complete numbered sources are preserved in
[source-numbered.log](evidence/static/source-numbered.log), and a declaration
index is in
[declaration-index.log](evidence/static/declaration-index.log).

### Local syntax, configuration, and attributes

| File:lines | Declaration | Review |
|---|---|---|
| `semantic.k:9-10` | `PString ::= eps \| ch(Int,PString)` | Finite inductive character sequence. Broader than Unicode because `Int` is unrestricted, but the proved equality property remains meaningful on every such sequence. |
| `semantic.k:12-15` | `PValue ::= pyInt \| pyBool \| pyStr \| pyTest` | Tagged values sufficient for every used expression and internal test. |
| `semantic.k:17-19` | `Test ::= yes \| no \| #short3 \| #same` | Explicit symbolic branch terms; all four forms have rules on every reachable use. |
| `semantic.k:21` | `Program ::= Module(Stmts)` | Exact top-level constructor used by `solution.mpy`. |
| `semantic.k:23` | `Stmts ::= List{Stmt,""}` | Exact juxtaposed statement-list representation, with generated `.Stmts` unit. |
| `semantic.k:25-27` | `Stmt ::= FuncDef \| Return \| If` | Exactly the statement forms used by the submission. |
| `semantic.k:29` | `Params(String)` | Covers the single-parameter functions. |
| `semantic.k:31-37` | `Expr ::= Bool \| Int \| Name \| Call \| Compare \| Subscript \| Slice` | Exactly all expression constructors used. |
| `semantic.k:39` | `CmpOp(String,Expr)` | Covers the submitted `<` and `==` comparison nodes. |
| `semantic.k:40` | `Bound ::= NoBound \| Expr` | Covers the submitted `Slice(Int(1),NoBound,NoBound)`. |
| `semantic.k:49-50` | One `<k>` cell starting `#call($PGM,"is_happy",pyStr($INPUT))` | Sufficient for this immutable, single-argument, no-I/O program; it has no stack/depth or exception cell, which causes the material recursion gap below. |
| `semantic.k:54` | `#len(PString) [function,total]` | Totality is true by the two PString constructors. |
| `semantic.k:58` | `#at(PString,Int) [function]` | Intentionally partial; every reachable use has index 0, 1, or 2 after a length-at-least-3 branch. |
| `semantic.k:62` | `#drop(PString,Int) [function]` | Intentionally partial; the only reachable use drops 1 from a length-at-least-3 string. |
| `semantic.k:76-79` | `#asInt`, `#asBool`, `#asStr`, `#asTest` `[function]` | Partial typed projections. Reachable calls have the declared tag. `#asBool` is unused. |
| `semantic.k:85` | `#valueEq(PValue,PValue) [function]` | Partial and unused; its sole integer equation is true. |
| `semantic.k:91-92` | `#call`, `#findCall` `[function]` | Pure function-call interpreter retaining the module for recursion. It has no dynamic call-depth/exception state. |
| `semantic.k:100-102` | `#exec [function]`, `#choose` ordinary term, `#branch [function]` | Implements statement sequencing, conditional selection, and return. |
| `semantic.k:135` | `#append(Stmts,Stmts) [function,total]` | Total by empty/nonempty list split. |
| `semantic.k:139` | `#eval(Expr,...) [function]` | Deliberately partial to the used AST subset. Every submitted expression form has a matching rule. |
| `verification.k:8` | `#distinct3(Int,Int,Int) [function,total]` | One unconditional, mathematically total equation. |
| `verification.k:14` | `#allTriples(PString) [function,total]` | Four disjoint constructor cases cover every PString. |
| `verification.k:22` | `#happy(PString) [function,total]` | Four disjoint constructor cases cover every PString. |
| `verification.k:32` | `#solution [function]` | Closed constant with one exact equation; no result abstraction. |

There are no local `[simplification]`, `[concrete]`, priority, `owise`,
macro, anywhere, or opaque declarations. No rule carries a priority. The only
local `[total]` symbols are `#len`, `#append`, `#distinct3`,
`#allTriples`, and `#happy`; each has complete, disjoint coverage.
Candidate-local partial functions are undefined only outside the used
well-typed paths. Imported K `INT`, `BOOL`, `STRING`, list syntax, and their
builtins are part of the named trust boundary in stage 7.

### Every local rule

| File:lines | Rule | Decision |
|---|---|---|
| `semantic.k:55` | `#len(eps) => 0` | True base equation. |
| `semantic.k:56` | `#len(ch(_,S)) => 1 + #len(S)` | True, structurally descending. |
| `semantic.k:59` | `#at(ch(C,_),0) => C` | True zero-index lookup. |
| `semantic.k:60` | Positive-index `#at` recursion | True under `I > 0`, decreases the index; partial at invalid indices, none reachable. |
| `semantic.k:63` | `#drop(S,0) => S` | True. |
| `semantic.k:64` | Positive `#drop` recursion | True under `I > 0`, decreases the index; reachable use is safe. |
| `semantic.k:68` | `#short3(eps) => yes` | Exactly `len < 3`. |
| `semantic.k:69` | One-character `#short3 => yes` | Exactly `len < 3`. |
| `semantic.k:70` | Two-character `#short3 => yes` | Exactly `len < 3`. |
| `semantic.k:71` | Three-or-more `#short3 => no` | Exactly negates `len < 3`. |
| `semantic.k:73` | `#same(I,I) => yes` | True equality branch. |
| `semantic.k:74` | `#same(I,J) => no requires I =/= J` | True and disjoint from line 73. |
| `semantic.k:80` | `#asInt(pyInt(I)) => I` | True projection. |
| `semantic.k:81` | `#asBool(pyBool(B)) => B` | True projection; unused. |
| `semantic.k:82` | `#asStr(pyStr(S)) => S` | True projection. |
| `semantic.k:83` | `#asTest(pyTest(T)) => T` | True projection. |
| `semantic.k:86` | Integer `#valueEq` | True integer equality; unused. |
| `semantic.k:93` | `#call(Module(DEFS),F,V) => #findCall(...)` | Correct module-preserving lookup in the abstract interpreter. Participates in the unbounded-call gap. |
| `semantic.k:94-95` | Matching `FuncDef` invokes `#exec` | Correct binding of the single parameter for the actual unique function definitions. |
| `semantic.k:96-98` | Nonmatching `FuncDef` skips to the rest | Guard is disjoint from the matching rule. First-definition lookup differs from Python only for duplicate definitions; the submitted program has none. |
| `semantic.k:104` | `#exec(Return(E) _) => #eval(E)` | Correctly discards the remaining function body after return. |
| `semantic.k:105-106` | `#exec(If...) => #choose(...)` | Correct conditional setup; the actual condition expressions are pure. |
| `semantic.k:108-109` | `#choose(yes,...)` | Correct true branch. |
| `semantic.k:110-111` | `#choose(no,...)` | Correct false branch. |
| `semantic.k:115-116` | Direct empty-string `#short3` context | Same result and continuation as reducing `#short3` to `yes`; sound bridge. |
| `semantic.k:117-118` | Direct one-character `#short3` context | Same result and continuation as `yes`; sound bridge. |
| `semantic.k:119-120` | Direct two-character `#short3` context | Same result and continuation as `yes`; sound bridge. |
| `semantic.k:121-122` | Direct three-or-more `#short3` context | Same result and continuation as `no`; sound bridge. |
| `semantic.k:123-124` | Direct equal `#same` context | Same branch and full continuation as reducing to `yes`. |
| `semantic.k:125-127` | Direct unequal `#same` context | Guarded disjointly; same branch and continuation as reducing to `no`. |
| `semantic.k:129` | Empty selected branch continues with `REST` | Correct statement sequencing. |
| `semantic.k:130` | Return in selected branch evaluates and discards all rests | Correct abrupt function return for the modeled normal-return language. |
| `semantic.k:131-133` | Nested `If` appends its remainder to outer rest | Correct fallthrough order; `#append(MORE,REST)` preserves sequencing. |
| `semantic.k:136` | Empty-list append | True list identity. |
| `semantic.k:137` | Nonempty-list append recursion | True, structurally descending. |
| `semantic.k:140` | Boolean literal evaluation | True. |
| `semantic.k:141` | Integer literal evaluation | True. |
| `semantic.k:142` | Parameter-name lookup | Correct for the only actual local name `s`; other names deliberately remain unsupported. |
| `semantic.k:144-145` | Builtin `len` call | Correct value on PString; this general rule is bypassed by the exact line-150 comparison shortcut in the submitted paths. |
| `semantic.k:146-148` | User call evaluates its argument and invokes `#call` | Value/binding behavior is correct with pure actual arguments, but this used rule recursively invokes with no depth increment, stack cell, or `RecursionError`; collectively with lines 49-50 and 91-104 it is not a sound complete model of the submitted Python calls on the full domain. Concrete false-conclusion witness below. |
| `semantic.k:150-151` | Exact `len(E) < 3` comparison to `#short3` | Truthful for every PString and does not encode the task answer; it is a sound low-level builtin shortcut. |
| `semantic.k:152-154` | Integer equality comparison to `#same` | Truthful for the character-index results used. |
| `semantic.k:156-157` | Integer string subscript via `#at` | Correct on all reachable in-range indices. |
| `semantic.k:158-159` | Suffix slice via `#drop` | Correct value for the only used `[1:]` slice; ignored allocation identity is unobservable in this immutable program. |
| `verification.k:9-12` | `#distinct3` is conjunction of three inequalities | Ordinary mathematics; exactly pairwise distinction. |
| `verification.k:15` | `#allTriples(eps) => true` | Vacuous-window base case. |
| `verification.k:16` | One-character `#allTriples => true` | Vacuous-window base case. |
| `verification.k:17` | Two-character `#allTriples => true` | Vacuous-window base case. |
| `verification.k:18-20` | Head distinctness and one-character recursive shift | Exactly enumerates every consecutive triple; structurally descending. |
| `verification.k:23` | `#happy(eps) => false` | Matches minimum-length contract. |
| `verification.k:24` | One-character `#happy => false` | Matches minimum-length contract. |
| `verification.k:25` | Two-character `#happy => false` | Matches minimum-length contract. |
| `verification.k:26-27` | Three-or-more `#happy => #allTriples` | Exact contract, not a program-execution shortcut. |
| `verification.k:33-58` | `#solution => Module(...)` | Exact program alias, confirmed mechanically; it neither predicts nor fabricates a result. |

### Used-construct map

| `solution.mpy` construct | Declaration and operational coverage |
|---|---|
| `Module` | `semantic.k:21`, call dispatch at 93 |
| `FuncDef`, `Params` | 25, 29; lookup/binding at 94-98 |
| statement lists and empty else lists | 23; `#exec`, `#branch`, and `#append` at 100-137 |
| `If` | 27; 105-133 |
| `Return` | 26; 104 and 130 |
| `Bool`, `Int`, `Name` | 31-33; 140-142 |
| builtin and user `Call` | 34; 144-148 |
| `Compare`, `CmpOp("<",...)`, `CmpOp("==",...)` | 35, 39; 150-154 |
| integer `Subscript` | 36; 156-157 and `#at` |
| suffix `Slice`/`NoBound` | 37, 40; 158-159 and `#drop` |

Every submitted construct is covered. No silently fabricated rule is used for
an unmodeled AST node.

### Concrete false-conclusion witness for the semantic gap

The problematic conclusion is enabled by the user-call rule
`semantic.k:146-148` together with the call/exec cycle and the absence of any
stack-depth/exception component in the configuration.

Take the satisfying intended-domain input `S = "abc" * 400`. Every consecutive
triple is pairwise distinct. The fresh K semantics makes 1,198 idealized helper
calls and concludes `pyBool(true)`, exit 0. The trusted canonical returns
`True`. The real submitted Python call crosses CPython's recursion limit 1000
and raises `RecursionError`. This exact witness, including the SHA-256 of the
input and the fresh `krun` output, is in
[long-recursion-witness.log](evidence/concrete/long-recursion-witness.log).

The individual call rewrite is internally coherent as an unbounded-stack
abstract language rule; the unsoundness is its use as the complete semantics
of the real submitted Python program without a domain bound or an explicit
conditional theorem. The witness shows the narrower issue directly, so no
other rule is labeled unsound merely because its general language coverage is
thin.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation was
trusted or reused. The reviewer created
[spec-vacuity.k](evidence/non-vacuity/spec-vacuity.k), which changes a
result-constraining obligation for the satisfying input `"abc"` from its true
result to `pyBool(false)`.

The mutation parsed and built successfully under `kprove --dry-run`, exit 0:
[mutation-dry-run.log](evidence/non-vacuity/mutation-dry-run.log).

The actual mutation proof exited 1 with `WarnStuckClaimState`. Its residual
front was:

```text
<k>
  pyBool ( true ) ~> .K
</k>
```

It failed because that term cannot unify with the false destination, exactly
the intended unmet result obligation. See
[mutation-proof.log](evidence/non-vacuity/mutation-proof.log). This is valid
non-vacuity evidence: it is not a parser error, missing import, timeout, or
unreachable mutation.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's generated, unbounded-stack semantics and K's imported
builtins:

1. For every finite inductive `PString S`, normal execution of the exact
   `check_happy_triples` AST reaches `pyBool(#allTriples(S))`.
2. For every finite inductive `PString S`, normal execution of the exact
   `is_happy` AST reaches `pyBool(#happy(S))`.
3. The six prompt examples reach their stated Boolean results.

The proof-local `#allTriples` and `#happy` functions are exhaustive
mathematical definitions. They do not replace program execution. The universal
helper claim is the connection theorem; it executes the helper body and uses
itself circularly only after consuming one character. The entry claim then
executes the entry body and calls that proved helper.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, parser, and reachability implementation | All build, execution, and proof results | Necessary low-level trust boundary; fresh builds reduce cache/provenance risk. |
| Imported `INT`, `BOOL`, `STRING`, generated list syntax, and integer/string/Boolean builtins | Length arithmetic, equality, guards, conjunction, statement-list representation | Ordinary fixed K primitives; acceptable. |
| Trusted `/reference/py2mpy.py` | Bridge from `solution.py` AST to `solution.mpy` | Explicit trusted input; byte-identity regeneration was checked. Translator semantic correctness is not reproved. |
| `#solution` static constructor alias | Which program the symbolic claims execute | Mechanically token-identical to submitted MPY modulo empty-list spelling; acceptable static pin, though not a theorem over file bytes. |
| PString as an immutable sequence of unrestricted mathematical integers | Python string length, indexing, slicing, and character equality | Broader than valid Unicode but property-preserving for the used operations. No false intended-domain conclusion found from this broadening. |
| Exact-specialized `len(E) < 3` and integer equality semantic rules | Branch control | Universally truthful on PString/Int; acceptable minimal generated semantics, not answer encoding. |
| Unbounded pure user-call recursion with no depth/exception cell | Control, exceptional termination, and final result | Illegitimate as an unconditional bridge to the submitted Python program over the unrestricted prompt domain. The length-1200 witness gives a concrete false normal-result conclusion. |
| Trusted canonical implementation and independent differential scripts | Empirical source-intent bridge | Finite evidence only. It supports short-input agreement and exposes the long-input counterexample; it is not a substitute for K proof. |
| Prompt-to-`#happy` reading | Human-language intent | Direct mathematical equivalence for all abstract strings: minimum length plus pairwise distinction of every length-three window. |

There are no candidate-local opaque result symbols, empirical oracles inside
the proof theory, task-answer semantic rewrites, proof-local simplifications,
or unproved operational bridges from the helper body to its result. The
decisive excluded behavior is CPython exceptional call termination, which is
not harmless here because the actual submitted implementation reaches it on a
valid input.

### Decision

Fresh verification and non-vacuity pass, but the requested theorem is about
the real generated program over the stated string domain. The candidate proves
an idealized unbounded-stack substitute and demonstrably proves a normal
Boolean result where the submitted Python execution raises. Because this is a
material false-conclusion witness rather than a merely informal or thin intent
bridge, it does not qualify for `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
