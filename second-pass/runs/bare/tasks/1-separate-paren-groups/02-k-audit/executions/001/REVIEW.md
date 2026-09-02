# Independent adversarial review: `1-separate-paren-groups`

## Executive decision

The candidate contains a reconstructed, result-constraining K reachability proof
of the exact submitted constructor program for the prompt's intended domain:
balanced groups made from `(`, `)`, and ASCII spaces. The source-to-IR check is
byte exact, both positive claims close from fresh source builds, the exact
program term is pinned in the entry claim, and a fresh false-result mutation is
rejected at the expected final obligation.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
related scope reasons:

1. The language is an individually generated, task-sized semantics, not a
   trusted Python semantics. Its correspondence to Python on balanced inputs
   relies on the static audit, an informal nonnegative-depth argument, and
   finite concrete evidence.
2. `program-correct` formally quantifies over *all* `Chars` sequences, while
   the Peano decrement model saturates at zero. On the malformed input `")"`,
   which is in that formal K precondition but outside the prompt's
   balanced-input precondition, fresh K execution returns `[")"]` whereas both
   Python implementations return `[]`. Thus the comment describing the claim
   as a sound “strict superset” of the prompt domain is not a faithful bridge
   to the real Python program over the whole formal precondition.

No rule was found that enables a false result on the intended balanced
parenthesis/space domain. In accordance with the required witness standard, the
malformed-input discrepancy is recorded as a formal-scope/fidelity limitation,
not labeled an intended-domain unsoundness.

## 1. Input and provenance integrity

### Trusted boundary and rendered mode

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist and is not a symlink, so the trusted mounts do not contradict
that mode. No hidden or inferred reference semantics was used.

The trusted inputs are:

- `/reference/prompt.py`, SHA-256
  `ba4d0641a184fb3cdd632060a25d6408a7e91fe9d79b5c341407e74b80536327`
- `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
- `/reference/canonical.py`, SHA-256
  `b74f3a3f40b1416f878efb45645d27f822b9d06b04bcd6191329a2229357b82d`

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted counterparts. All required deliverables—`solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`—are
nonempty regular files and not symlinks. No required source artifact is missing
or mistyped. There are no helper K files beyond those three K sources.

The candidate also contains additional generated evidence and cache material:
`verification-kompiled/`, `__pycache__/`, four `krun-*.out` files,
`kprove.out`, and `kore-exec.tar.gz`. These are not source-integrity failures,
but none was reused. Only explicit source files were copied to
`/tmp/audit-work/candidate`; trusted inputs were copied separately to
`/tmp/audit-work/trusted`.

### Untrusted generation records

`run-input.json` identifies problem `1-separate-paren-groups`, condition
`bare`, and the same trusted prompt/translator hashes. `metrics.json` reports a
zero generation exit and no timeout. `codex-last.txt`, `codex-output.log`, and
the JSONL trace claim that all proofs closed. The trace also shows the
candidate's evolution from an integer model to the final Peano model. These
records were read only as claims; none supplies audit authority.

Evidence:

- [integrity commands and results](evidence/stage1_integrity.log)
- [bounded structured-trace extraction](evidence/generation_trace_extract.log)
- [trace extractor](evidence/trace_extract.py)

Stage 1 result: **PASS**. There is no infrastructure breach and no provenance
mismatch.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt asks `separate_paren_groups(paren_string)` to split a string
containing separate balanced parenthesis groups into one output string per
top-level group, preserving nesting while ignoring ASCII spaces. For example,
`"( ) (( )) (( )( ))"` must produce `["()", "(())", "(()())"]`.

The trusted canonical implementation keeps a list for the current group and an
integer nesting depth. It appends the current group when processing a `)` makes
the depth zero.

The submitted implementation uses the same state in a different
representation: `current` is a string, `depth` is an integer, and each
non-space character is appended. `(` increments depth; every other non-space
character decrements it, and `)`-domain inputs are emitted when the result is
zero. On the documented parenthesis/space domain this is extensionally the
same algorithm. Its “every other character is a close parenthesis” behavior
would not be faithful for arbitrary text, but arbitrary text is not part of
the stated input language.

### Trusted regeneration

The command

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy
```

exited 0. The regenerated and submitted files are byte-identical, both with
SHA-256
`1a0f6c1f65d3abac6f021e0a791a9f33236254b0f377f9b2cb3a8168e85c51ef`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and submitted
entry points under distinct module names. It covers:

- nine named cases, including the documented example, empty input, spaces
  only, a single group, adjacent groups, deep nesting, the nonzero-close
  branch, and spaces at boundaries;
- every Dyck word through five pairs with every optional single-space gap
  placement: 93,898 inputs;
- every string over `(`, `)`, and space through length nine, matching the
  proof's broader `Chars` alphabet: 29,524 inputs;
- 250 deterministic larger balanced samples, up to 40 pairs.

There were 123,681 comparisons and zero mismatches. This finite evidence does
not prove universal equivalence, but it strongly supports the
candidate-versus-canonical bridge on the tested scope.

Evidence:

- [differential source](evidence/differential_test.py)
- [regeneration and differential log](evidence/stage2_program_fidelity.log)
- [exact commands](evidence/stage2_program_fidelity.sh)

Stage 2 result: **PASS on the intended domain**.

## 3. Clean proof reconstruction

### Fresh builds

K version 7.1.293 was used. Candidate-provided definitions and caches were not
copied or referenced. Two definitions were built from the scratch source:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled

kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled
```

Both exited 0.

### Positive proof targets

The helper claim was selected alone:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant --output pretty
```

It exited 0 and printed `#Top`.

The end-to-end target needs the loop claim available as its circularity.
Selecting only `program-correct` removes that helper from the spec and causes
unbounded loop unrolling; that diagnostic was interrupted and is not a
candidate failure. The proper target invocation retained both labels:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant,SPEC.program-correct --output pretty
```

It exited 0 and printed `#Top`. A final unfiltered run over every claim also
exited 0 and printed `#Top`.

Evidence:

- [fresh build and positive-proof log](evidence/stage3_build_prove.log)
- [reconstruction script](evidence/stage3_build_prove.sh)
- [program-only selector diagnostic](evidence/stage3_program_only_diagnostic.log)

### Fresh generated-semantics execution

The LLVM definition was executed on the documented example, empty input,
spaces only, `"()"`, deep nesting, adjacent groups, and a spaced boundary
case. Each `krun` exited 0, and its parsed `<result>` was equal to both the
trusted canonical and submitted Python results. There were seven intended
comparisons and zero mismatches.

The same run records the important out-of-domain diagnostic:

```text
input:                 ")"
fresh K result:        [")"]
trusted canonical:     []
submitted Python:      []
```

This discrepancy follows from the saturating zero-decrement rule and is
discussed in Stages 5 and 7.

Evidence:

- [K/Python comparison source](evidence/k_python_compare.py)
- [fresh concrete-execution log](evidence/stage3_concrete_execution.log)

Stage 3 result: **PASS for clean reconstruction and intended-domain concrete
execution**, with a recorded formal-scope limitation.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each entry claim

`loop-invariant` (`spec.k:9-37`) has no explicit `requires` clause. Its
sort-constrained precondition is:

- the `<k>` cell is the exact submitted `for`-loop body at a loop head,
  followed by the exact final `Return(result)` continuation;
- `CS` is any remaining structural character sequence;
- the environment contains the exact five relevant bindings:
  `ch = LAST`, `current = CURRENT`, `depth = D`,
  `paren_string = ALL`, and `result = OUT`;
- `D` is a Peano natural, while the input, function map, and initial result are
  otherwise framed/arbitrary.

Its postcondition says execution reaches `.K` and the `<result>` cell is
exactly the completed-output projection of
`runSpec(CS,D,CURRENT,OUT,LAST)`. The final local environment is existential,
but the returned value is not.

`program-correct` (`spec.k:42-72`) also has no explicit `requires`. Its
precondition is the exact `#boot(Module(...))` constructor tree, an empty
environment and function map, `none` as result, and `Encoded(CS)` for any
sequence over `LP`, `RP`, and `SP`. Its postcondition reaches `.K` and fixes
the result to `OutList(separateSpec(CS))`; only the final environment and
function map are existential.

### Exact real-program pinning

The trusted translator regenerated the IR byte-for-byte. Independently,
`evidence/pinning_check.py` extracted the argument of `#boot` from
`program-correct` and compared its constructor tokens with both submitted and
regenerated IR. The spec uses two explicit `.Stmts` tokens where the concrete
surface file leaves an empty list syntactically blank. After normalizing this
standard empty-list spelling:

- all three terms contain the same 226 constructor tokens;
- the normalized spec and submitted term have SHA-256
  `97ec7f8863a32d49306ed9f0a24c8034f9adab2c14f6c9e4dc2f7fc9b2510a16`.

Thus the entry claim does not substitute another program or call an oracle in
place of the body.

### Satisfiable witnesses and concrete substitution

For `loop-invariant`, a concrete satisfying loop-head state uses:

```text
CS = LP RP .Chars
D = zero
CURRENT = .Chars
OUT = .Outputs
LAST = .Chars
ALL = LP RP .Chars
IN = Encoded(LP RP .Chars)
FS = .Map
initial result = none
```

For `program-correct`, use the exact entry configuration with
`CS = LP RP .Chars`. These are reachable/satisfiable states for the input
`"()"`. Fresh ground claims for both configurations independently returned
`#Top`. Substituting the same value into the claimed result gives
`out(LP RP)`, i.e. `["()"]`; both Python implementations returned `["()"]`.

Evidence:

- [ground K witnesses](evidence/ground-witnesses.k)
- [pinning checker](evidence/pinning_check.py)
- [ground proof and Python log](evidence/stage4_adequacy.log)
- [exact adequacy commands](evidence/stage4_adequacy.sh)

### Adequacy assessment

The result is genuinely constrained. `?FINALENV`, `?TOPENV`, and `?TOPFUNS`
cannot choose or weaken `<result>`, and there is no one-way Boolean implication
standing in for output equality.

The scope caveat is that `Encoded(CS)` is formally broader than the natural
precondition. On balanced input, every close parenthesis occurs at positive
depth, so the Peano model tracks the Python integer exactly. On malformed
inputs, that connection need not hold, as the `")"` witness shows.

Stage 4 result: **PASS for the real submitted program on the intended domain;
CONCERN for the formally overbroad precondition**.

## 5. Rule-by-rule static soundness review

The complete numbered sources and declaration searches are preserved in
[the static inventory log](evidence/stage5_static_inventory.log). The inventory
contains 67 rules in `semantic.k`, 11 rules in `verification.k`, and two
claims in `spec.k`.

### Local syntax inventory

| Location | Complete local declaration inventory |
|---|---|
| `semantic.k:8-9` | `Ids` as comma-separated `String`; `Params(Ids)` |
| `semantic.k:11-12` | `Program = Module(Stmts)`; `Stmts` as a statement list |
| `semantic.k:14-21` | `Stmt`: `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`, `For`, `If`, `Return`, `Expr` |
| `semantic.k:23-30` | `Expr`: `Name`, `Str`, `Int`, `ListExpr`, `Compare`, `Attribute`, `Call`; and `CmpOp` |
| `semantic.k:35-39` | `Char`: `LP`, `RP`, `SP`; `Chars` list; `Output = out(Chars)`; `Outputs` list |
| `semantic.k:41-46` | `PInt`: `zero`, `succ(PInt)`; `Value`: `PInt`, `Bool`, `SVal`, `OutList`, `none` |
| `semantic.k:48-51` | `Input`: `Raw`, `Encoded`; `Function = fun(String,Stmts)` |
| `semantic.k:53-59` | Function symbols: `#chars`, `#concat`, `#char`, `#snocOut`, `#inputValue`, `#eqChars`, `#eqChar` |
| `semantic.k:61-75` | `KItem`: `#boot`, `#load`, `#invoke`, `#exec`, `#assign`, `#augAssign`, `#cmpLeft`, `#cmpRight`, `#if`, `#for`, `#loop`, `#set`, `#append`, `#discard`, `#return` |
| `verification.k:9-15` | `ScanState = scanState(...)`; functions `runSpec`, `stateDepth`, `stateCurrent`, `stateLast`, `stateOutput`, `separateSpec` |

There are no local `[total]`, `[functional]`, priority, simplification,
`owise`, `anywhere`, macro, or alias declarations. There are no opaque or
uninterpreted local symbols. Every local function has equations below; `#char`
is deliberately partial outside the three-character modeled alphabet.

The configuration (`semantic.k:86-93`) has exactly the required cells:
`<k>`, `<input>`, local `<env>`, `<functions>`, and `<result>`. There is no
heap, output stream, exception cell, or call stack. Those omissions are
adequate for this one top-level, alias-free, exception-free program on its
intended inputs.

### Equational/function rules in `semantic.k` — all 24

| Rules | Count | Static decision |
|---|---:|---|
| `#chars("") -> .Chars`; nonempty `#chars` takes the first K string character and recurses (`95-98`) | 2 | Guards are disjoint by string length and recursion decreases. Combined with `#char`, this is correct for ASCII `(`, `)`, and space. |
| `#char("(")`, `#char(")")`, `#char(" ")` (`100-102`) | 3 | Pairwise disjoint and correct. Other characters visibly remain stuck; this is appropriate minimal coverage, not silent fabrication. |
| `#concat(.Chars,CS)` and `#concat(C CS1,CS2)` (`104-105`) | 2 | Total on `Chars`, disjoint, structurally decreasing, and implements ordered concatenation. |
| `#snocOut(.Outputs,CS)` and the `out(OLD) OS` recursive case (`107-108`) | 2 | Total on `Outputs`, disjoint, decreasing, and appends without reordering. |
| `#inputValue(Raw(S))` and `#inputValue(Encoded(CS))` (`110-111`) | 2 | Total on `Input`; correctly separates the concrete decoder boundary from structural proof input. |
| Four `#eqChars` shape cases: empty/empty, empty/nonempty, nonempty/empty, cons/cons (`113-116`) | 4 | Exhaustive and nonoverlapping; recursion decreases. This function is unused by the submitted path but mathematically sound. |
| Nine `#eqChar` cases for the full `LP/RP/SP × LP/RP/SP` product (`118-126`) | 9 | Exhaustive, pairwise constructor-disjoint, and truthful. It is also unused by the submitted path. |

### Operational rules in `semantic.k` — all 43

| Rules | Count | Static decision |
|---|---:|---|
| `#boot(Module(SS)) -> #load(SS)` (`128`) | 1 | Correct entry transition for the exact submitted module. |
| `#load(.Stmts)` invokes the named entry; `ImportFrom` is skipped; `FuncDef` stores `fun(P,BODY)` (`130-133`) | 3 | Correct for the exact module. Ignoring `typing.List` has no runtime effect. The hard-coded entry name is narrow but pinned to the requested entry point. |
| `#invoke(F)` looks up the stored body, converts input, and resets locals to the single parameter (`135-138`) | 1 | Correct for this top-level one-argument call. No program-defined call is bypassed. |
| `#exec(.Stmts)` and `#exec(S SS)` (`140-141`) | 2 | Standard left-to-right statement sequencing. |
| `Assign` evaluates its RHS; a resulting `Value` updates the named map key (`143-145`) | 2 | Preserves RHS-before-write order and exact local state. |
| `AugAssign` evaluates its RHS; string `+` concatenates; Peano `+ 1` takes successor; `zero - 1` stays zero; `succ(N) - 1` yields `N` (`147-155`) | 5 | String addition and positive-depth arithmetic are correct on all reachable intended states. The two decrement environment patterns are disjoint. The zero-decrement case is not Python integer subtraction on malformed-prefix states; witness `")"` gives K `[")"]` versus Python `[]`. Because such a prefix violates the balanced-input precondition, this is recorded as a scope gap rather than intended-domain unsoundness. |
| `If` evaluates its test; `true` selects then and `false` selects else (`157-159`) | 3 | Correct and constructor-disjoint. |
| `For` evaluates the iterable; `SVal(CS)` starts `#loop`; empty loop stops; nonempty loop sets the target, executes the body, and recurs on the tail (`161-164`) | 4 | Correct left-to-right string iteration on the structural character sequence. The recurring configuration exactly matches the invariant. |
| `#set` updates the loop variable (`166-167`) | 1 | Exact local-state effect. |
| `Return` evaluates its expression; the value rule sets `<result>` and discards the remaining function continuation (`169-171`) | 2 | Correct abrupt return for this function. It accepts a broad suffix, but the submitted return is last and reaches the exact `#exec(.Stmts)` suffix; no intended-domain control witness differs. No caller frame exists in this model. |
| `Expr` evaluates and `#discard` drops the value (`173-174`) | 2 | Correct for the ignored return from `list.append`. |
| The specialized `Call(Attribute(Name(X),"append"),E)` evaluates `E`; `#append` appends to `OutList` and yields `none` (`176-178`) | 2 | Correct mutation and return value for the only used method call. No alias observes a distinct list object. |
| `Compare` evaluates left then right; `#cmpLeft` preserves the left value; zero equals zero and differs from successor; six specialized literal/character results cover `ch != " "` and `ch == "("` (`180-192`) | 10 | Evaluation order is correct. All used combinations are covered and constructor-disjoint. Operand orientation was checked against the continuation rules. |
| Bound-name lookup, string literal decoding, integer literals `0` and `1`, and empty-list construction (`194-199`) | 5 | Each matches a used source construct. Larger integers and other expressions are deliberately unmodeled and unused. |

The only evaluation-order approximation worth noting is that simple-name
augmented assignment reads the old binding in its commit rule, after evaluating
the RHS, whereas full Python specifies target read before RHS evaluation. Every
submitted RHS is a side-effect-free `Name` or integer literal, so this broader
rule creates no behavioral difference for the submitted program.

### Verification-function rules — all 11

| Rules | Count | Static decision |
|---|---:|---|
| `runSpec` base case (`verification.k:17`) | 1 | Returns exactly the accumulated state when input is exhausted. |
| `runSpec` on `SP`, `LP`, `RP` at `zero`, `RP` at `succ(zero)`, and `RP` at `succ(succ(D))` (`18-22`) | 5 | Exhaustive over `Chars × PInt`, constructor-disjoint, and recursively decreasing in `CS`. Each case mirrors the generated operational semantics, including its zero-saturating malformed-input behavior. |
| `stateDepth`, `stateCurrent`, `stateOutput`, `stateLast` projections (`24-27`) | 4 | Truthful constructor projections. Only `stateOutput` affects the final theorem; the other three are inert. |
| `separateSpec(CS)` initializes `runSpec` and takes its output (`28`) | 1 | A fully defined mathematical specification, not an operational shortcut. |

`runSpec` and `separateSpec` encode the requested result *as a postcondition*;
they do not rewrite or bypass any program construct. The loop claim is the
machine-checked connection between actual execution and this summary. There is
no fresh result-bearing oracle and no circular use of an opaque value.

### Claims and construct-to-rule map

`spec.k` contains exactly `loop-invariant` and `program-correct`, described in
Stage 4. No claim is installed in `verification.k` as an ordinary semantic
rewrite.

Every constructor in `solution.mpy` is covered:

| Submitted construct | Declaration and execution path |
|---|---|
| `Module`, `ImportFrom`, `FuncDef`, `Params` | syntax `8-15`; boot/load/invoke `128-138` |
| statement list | syntax `12`; execution `140-141` |
| `Assign(Name,...)` | syntax `16`, `23`; rules `143-145`, `194-199` |
| `AugAssign` with string or depth | syntax `17`; rules `147-155` |
| `For(Name,Name,body)` | syntax `18`; rules `161-167` |
| `If` | syntax `19`; rules `157-159` |
| `Return` | syntax `20`; rules `169-171` |
| expression statement | syntax `21`; rules `173-174` |
| `Str`, `Int(0)`, `Int(1)`, `ListExpr` | syntax `24-26`; rules `196-199` |
| `Compare`/`CmpOp` | syntax `27`, `30`; rules `180-192` |
| `Attribute` and `Call` for `result.append` | syntax `28-29`; specialized rules `176-178` |

State changes are limited to the local map and result cell. Output order and
iteration order are preserved. There is no allocation identity, exception, or
external state relevant to this source. Rule guards and constructor patterns
are disjoint on every overlapping family reviewed above.

Stage 5 result: **PASS on the intended domain, with the explicit malformed-input
scope limitation**. No smuggled correctness rule or unconstrained oracle was
found.

## 6. Fresh non-vacuity test

No candidate-provided vacuity artifact was trusted. The fresh
`spec-vacuity-audit.k` uses the exact submitted boot term and satisfiable input
`Encoded(LP RP .Chars)`, but mutates the correct one-group postcondition to
require `OutList(.Outputs)`.

First,

```text
kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0, establishing that the mutation parses and builds.

The actual proof exited 1 with `WarnStuckClaimState`. Its residual is the
reachable final configuration:

```text
<k> .K </k>
<input> Encoded ( LP RP .Chars ) </input>
<result> OutList ( out ( LP RP .Chars ) .Outputs ) </result>
```

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash.

Evidence:

- [fresh mutation](evidence/spec-vacuity-audit.k)
- [mutation build/proof log](evidence/stage6_nonvacuity.log)
- [exact mutation commands](evidence/stage6_nonvacuity.sh)

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the generated `MPY` transition system, K's imported domains, and the
fully defined verification functions:

1. From every configuration matching `loop-invariant`, execution of the exact
   submitted loop and final return reaches a state whose returned list is
   exactly the output component of `runSpec` for the remaining characters and
   supplied scanner state.
2. From the exact submitted `#boot(Module(...))` term, empty local/function
   maps, `none` result, and any structural `Encoded(CS)`, execution reaches
   `.K` with result exactly `OutList(separateSpec(CS))`.

This is a partial-correctness reachability result. The returned value is proved;
the final local and function maps are intentionally existential because they
are not observable in the function contract.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, LLVM/Haskell backends, and reachability prover | All machine-checked results | Standard unavoidable toolchain trust; acceptable. |
| Imported `domains.md` definitions for strings, Booleans, maps, integers, and generated lists | Decoding, maps, guards, syntax lists | Standard low-level trust boundary; acceptable. |
| Trusted CPython-AST translator correctly represents Python syntax | Identity of `solution.mpy` | Its output was byte-reproduced, but semantic correctness of the translator remains trusted. The translator is a designated trusted input; acceptable. |
| Generated `MPY` rules correspond to Python for the used subset | Bridge from K theorem to `solution.py` | Audited line by line and concretely tested. Still an informal/empirical bridge rather than a theorem against CPython; concerning but legitimate for generated-semantics mode. |
| `LP/RP/SP` encoding matches ASCII parenthesis/space iteration | All inputs | Straightforward and concretely exercised. Other characters visibly fail decoding; acceptable because unused by the prompt domain. |
| Peano `PInt` corresponds to Python's integer depth while prefixes remain nonnegative | Depth comparisons and result emission | Informally justified by balance-prefix induction and supported by tests. It fails for malformed negative-depth prefixes, producing the documented `")"` divergence; this is the principal concern. |
| `runSpec`/`separateSpec` express the natural-language grouping property | Human-facing intent | These are fully defined, total structural functions and are connected to K execution by the proof. Their interpretation as the English contract is an informal mathematical bridge, supported by 123,681 canonical differential cases; finite evidence is not a universal theorem. |
| `?FINALENV`, `?TOPENV`, `?TOPFUNS` | Only unobserved final maps | Existential proof variables, not opaque primitives. They cannot influence the constrained result; acceptable. |

There are no opaque symbols, trusted result oracles, empirical operational
bridges, proof-local priority rewrites, or proof rules that replace the
program-defined body. `#char` is a partial boundary rather than an oracle:
unsupported raw input remains visibly stuck.

### Gates

- **Gate A — real-program soundness:** PASS on the prompt's balanced
  parenthesis/space domain. Program execution is not bypassed, the result is
  fixed, and non-vacuity passes. The theorem's broader malformed-input wording
  is not a faithful real-Python claim and prevents an unqualified pass.
- **Gate B — intent adequacy:** PASS with concerns. The algorithm and scanner
  postcondition match the prompt on its stated domain, but the
  summary-to-English and generated-semantics-to-Python connections are
  informal rather than separately machine-checked.
- **Gate C — trust/evidence auditability:** PASS. Reviewer-authored scripts,
  inputs, exact commands, statuses, and bounded outputs are preserved under
  `evidence/`.

### Final rationale

The proof is neither missing nor vacuous, does not prove a substituted program,
and does not rely on a result-bearing oracle. The exact program is symbolically
executed, its loop is summarized by a separately closing circularity, and a
false returned value is rejected.

The generated semantics is adequate for every construct and state reachable on
the intended balanced input domain. Because its formal claim overstates that
bridge to all `Chars`, and because Python correspondence remains an audited
assumption rather than a theorem, the appropriate decision is legitimate with
documented concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
