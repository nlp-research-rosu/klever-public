# Independent adversarial audit: 95-check-dict-case

## Executive finding

The candidate rebuilds and both submitted positive claims print `#Top`, but the
proof is not legitimate.  A proof-local priority rule changes the supplied
semantics on a state admitted by the submitted loop claim.  With the same
ground loop state, a bridge-free definition proves that the real execution
returns `true`, while the candidate definition proves that it returns `false`.
This is a concrete false-conclusion witness, not merely a missing explanation.

The fresh false-result mutation was rejected correctly, so the proof is
result-constraining rather than vacuous.  That does not cure the materially
unsound operational bridge.

All candidate files were treated as untrusted and read-only.  Sources used for
execution were copied to `/tmp/audit-work`; no candidate-built definition or
cache was reused.  The line-addressable rule inventory, reviewer test sources,
exact commands, exit statuses, and bounded outputs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Required inputs

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode.

The following candidate records required by the audit request are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present.  These are provenance defects.
They do not prevent an independent rebuild because the proof, program,
translator, prompt, and supplied semantics sources are present.

The candidate also contains `.build/` outputs and `__pycache__/` bytecode.
They were inventoried as untrusted extras and were neither copied into the
scratch source tree nor used.

### Trusted comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The candidate `reference-semantics/` tree recursively matches the trusted
`/reference/reference-semantics/` tree.  `diff -qr --no-dereference` returned
0.  There are no symlinks in the candidate semantics tree, no missing or extra
entries, and no type or content differences.  The supplied-semantics integrity
gate therefore passes.  This identity does not bless the rules added in
`verification.k`.

Evidence:

- `evidence/01-provenance-integrity.log`: inventory, missing records, hashes,
  symlink checks, byte comparisons, and recursive semantics comparison.
- `evidence/05-scratch-source-hashes.log`: hashes of all scratch source inputs.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a dictionary, return `false` when it is empty.  Otherwise return `true`
exactly when every key is a string and either every key satisfies
`str.islower()` or every key satisfies `str.isupper()`.  Values are irrelevant.
Mixed lower/upper keys, non-string keys, mixed-case or uncased-only strings
make the result `false`.

The generated `solution.py` implements this predicate with three Boolean
accumulators:

- `has_key` records non-emptiness;
- `all_lower` remains true exactly while every visited key is a lower-case
  string;
- `all_upper` remains true exactly while every visited key is an upper-case
  string.

It visits every key and returns
`has_key and (all_lower or all_upper)`.

### Translator fidelity

I regenerated `solution.mpy` from the scratch copy of `solution.py` with the
trusted translator.  The regenerated and submitted files both have SHA-256
`02c470fff3f9967c3a4af5071971b6d09d8a48fd940ecb3a4e0888c7390fef04`;
`cmp` returned 0.

Evidence: `evidence/02-translator-byte-identity.log`.

### Independent differential testing

`evidence/differential_check.py` independently loads the trusted canonical
entry point and the generated entry point and also evaluates a direct
implementation of the prompt predicate.  Its 2,599 cases comprise:

- all five documented examples;
- 13 explicit empty/type/case/late-key/Unicode boundary cases;
- all 2,081 ordered permutations of length zero through four from eight
  representative keys;
- 500 fixed-seed generated dictionaries.

The generated implementation disagreed with the direct contract zero times.
It disagreed with the trusted canonical 166 times.

The canonical has a material defect: after the first key establishes a state,
its `else: break` exits on the next consistently cased key.  It can therefore
ignore a later bad key.  For example:

```text
input:       {"a": 0, "b": 0, "A": 0}
canonical:   true
generated:   false
contract:    false
```

This is a canonical/program divergence, but the generated implementation is
the one that agrees with the stated contract on the witnessed case.

Evidence:

- `evidence/03-differential.log`: complete scope, counts, first 20 mismatches,
  zero generated-contract failures, and exit 0.
- `evidence/17-ground-python-comparison.log`: selected empty, branch, late-key,
  and Unicode results.
- `evidence/differential_check.py` and
  `evidence/ground_python_compare.py`: preserved reviewer scripts.

## 3. Clean proof reconstruction

### Toolchain and source isolation

The installed K toolchain is K `v7.1.337`.  Both definitions were built from
scratch-copied source.  The candidate `.build/` directory and all candidate
caches were ignored.

### Concrete definition

Fresh LLVM compilation used:

```text
kompile /tmp/audit-work/src/reference-semantics/semantics.k
  --backend llvm
  --main-module MPY-KRUN
  --syntax-module MPY-SYNTAX
  --output-definition /tmp/audit-work/build/runtime-kompiled
```

It exited 0.  The compiler reported non-exhaustiveness warnings in fixed,
unused helpers (`mapStrVS`, float helpers, `joinCodes`, and out-of-bounds
`valSeqAt`).  None occurs on this program's execution path.

The candidate smoke program was regenerated with the trusted translator and
executed against that definition.  `krun` exited 0 with final `.K`, `NoExc`,
and exit code 0.  A separate reviewer ground suite covered empty, single lower,
single upper, uncased string, non-string, and late mixed-case keys and also
finished with `.K`, `NoExc`, and exit code 0.

Evidence:

- `evidence/06-generate-smoke-mpy.log`
- `evidence/07-kompile-llvm.log`
- `evidence/08-krun-smoke.log`
- `evidence/13-ground-cases-translate.log`
- `evidence/14-ground-cases-krun.log`
- `evidence/ground_cases.py`

### Proof definition and target claims

Fresh Haskell compilation used:

```text
kompile /tmp/audit-work/src/verification.k
  --backend haskell
  --main-module CHECK-DICT-CASE-VERIFICATION
  --syntax-module MPY-SYNTAX
  --output-definition /tmp/audit-work/build/verification-kompiled
```

It exited 0.  The combined proof and each positive target claim selected
individually exited 0 and printed `#Top`:

| Run | Result |
|---|---|
| all claims | `#Top`, exit 0 |
| `CHECK-DICT-CASE-SPEC.entry-reaches-loop` only | `#Top`, exit 0 |
| `CHECK-DICT-CASE-SPEC.loop-and-return` only | `#Top`, exit 0 |

Evidence:

- `evidence/09-kompile-haskell.log`
- `evidence/10-kprove-all.log`
- `evidence/11-kprove-entry-only.log`
- `evidence/12-kprove-loop-only.log`

Thus clean reconstruction succeeds as verification under the candidate theory.
The static soundness failure in Stage 5 means these `#Top` results are not a
legitimate proof under the supplied semantics.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

`entry-reaches-loop` starts from the standard initial MPY configuration,
loads `checkDictCaseModule()`, and calls `check_dict_case` on
`dictV(KS, VS)`.  It claims reachability of the real loop head after:

- installing the exact function closure;
- allocating the callee scope;
- binding `dict`;
- initializing `has_key=false`, `all_lower=true`, `all_upper=true`, and
  `key=noneV`;
- evaluating `dict.keys()` to a newly allocated `list(KS)`;
- pushing the exact return continuation.

Its destination still contains the submitted loop, return expression, and
`#endcall`; it is not itself a final-result claim.

`loop-and-return` starts from that loop/return continuation with arbitrary
remaining `KS`, current flags, current `dict` and `key`, and framed heap
state.  It claims that executing the loop and return produces:

```text
keySeenAfter(KS, SEEN)
and
((LOWER and allLowerKeys(KS)) or
 (UPPER and allUpperKeys(KS)))
```

while popping the frame, deleting the callee scope, restoring environment 0,
and preserving exception and exit-code state.

The two claim interfaces compose: the entry destination matches the loop
claim's source with `SEEN=false`, `LOWER=true`, `UPPER=true`, the original
dictionary, `OLDKEY=noneV`, the allocated key-list heap, and the matching
frame/counters.

### Program identity

The four zero-argument AST functions in `verification.k` expand to the exact
submitted `solution.mpy` module, body, loop body, and result expression.  The
byte-identity translator check independently pins the submitted `.mpy` to
`solution.py`.  There is no substituted algorithm, free return variable, or
tautological destination.

### Satisfiable witnesses and substitutions

An entry-precondition witness is:

```text
KS = vCons(str(iCons(97, .IntSeq)), .ValSeq)   // key "a"
VS = vCons(0, .ValSeq)
initial heap = .Map
initial env/scopes/stack/ret/exc/exit-code = exactly those in the claim
```

The composed claimed result reduces to `true`; the generated Python and
canonical Python implementations both return `true` for `{"a": 0}`, and the
reviewer K ground suite accepts it.

For `{"a": 0, "b": 0, "A": 0}`, the claimed bare-string result reduces to
`false`; the generated Python and concrete K executions return `false`, while
the defective canonical returns `true`.

For the empty dictionary, `keySeenAfter(.ValSeq, false)` is false, matching
both Python implementations and concrete K.

There is nevertheless a language-model limitation.  The supplied semantics'
`strToCodes` only accepts characters below 128, and its case predicates only
recognize ASCII A-Z/a-z.  Both Python implementations classify `{"é": 0}` as
lower-case and return `true`; the fresh Unicode `krun` fails in
`strToCodes("\xc3\xa9")` with exit 113.  This would be an intent-adequacy
concern, not the reason for the final failure.

Evidence:

- `evidence/15-unicode-translate.log`
- `evidence/16-unicode-krun.log`
- `evidence/unicode_case.py`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/04-rule-inventory.log` is the line-addressable inventory of every
`configuration`, `context`, `syntax`, `rule`, `claim`, priority attribute,
function/total declaration, concrete rule, and opaque declaration in:

- `reference-semantics/semantics.k`;
- all 23 supplied helper `.k` files;
- candidate `verification.k`;
- candidate `spec.k`.

The supplied tree contains 24 K source files, 227 `syntax` declaration
starts, 695 rule starts, five contexts, and one configuration.  The candidate
adds 11 function/total symbols in eight syntax declaration starts, 24 rules,
six priority rules, and two claims.  It adds no `functional` declarations,
no simplification rules, and no opaque symbols.

Per-file counts and attribute searches are preserved in
`evidence/20-rule-counts-and-attributes.log`.

### Supplied semantics inventory and relevance decision

The following table accounts for every fixed-semantics file; the detailed
log enumerates each declaration and rule within the file.

| File/module | Role and decision for this program |
|---|---|
| `semantics.k` | Assembles `MPY` and `MPY-KRUN`; fixed module boundary, unchanged. |
| `syntax.k` | Declares all AST constructors. Used: `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Bool`, `NoneVal`, `For`, `Call`, `Attribute`, `If`, `UnaryOp`, `Return`, `BoolOp`. Declarations match the translated AST. |
| `core.k` | Defines values, cells/configuration, load/sequencing, scope lookup, builtin scope, argument evaluation, literals, truth, allocation, and sequence helpers. The relevant rules preserve the exact cells used by both claims. |
| `iter.k` | Declares iterator protocol terms used by the loop. |
| `range.k` | Fixed but unused. |
| `operators.k` | Routes `UnaryOp("not",...)`; relevant routing is standard. Other operators are unused. |
| `int.k` | Integer operations are unused by control/result computation; integer keys remain ordinary non-string `Val`s. |
| `bool.k` | Implements truthy `not` and short-circuit/value-returning `and`/`or`. Relevant and consistent with the submitted expression. |
| `float.k` | Fixed opaque/concrete float boundary; unused. |
| `str.k` | Represents strings as `IntSeq`; relevant representation is sound at the selected supplied-semantics level but ASCII-limited relative to CPython. |
| `set.k` | Unused. |
| `list.k` | Key-list allocation and iteration are relevant and structurally consume one key per loop step. Other list operations are unused. |
| `tuple.k` | The `#bindTgt(Name,Val)` rule is used by `For`; tuple construction/unpacking is unused. |
| `subscript.k` | Unused. |
| `comprehension.k` | Unused. |
| `methods.k` | `applyMethod` for `islower`/`isupper` and `hasLower`/`hasUpper` are relevant. They implement the supplied ASCII case model. Other methods are unused. |
| `controls.k` | Assignment, `If`, `For`, `#loop`, `#loopStep`, and loop-label continuation are relevant. They preserve evaluation order and update exactly the local scope. |
| `functions.k` | Function installation, parameter binding, return, frame pop, scope deletion, and environment restoration are relevant and match the claim cells. |
| `builtins.k` | `isinstance(...,str)` and `isStrV` are relevant. Opaque MD5 and unrelated builtins are unused. |
| `call.k` | Callee lookup, argument evaluation, builtin/method/closure dispatch, and heap-reference dereference are relevant. The priority-40 dereference rule is central to the false witness below. |
| `sort.k` | Opaque/concrete sort boundaries are unused. |
| `assert.k` | Used only by concrete reviewer/smoke programs, not by the proof claims. |
| `dict.k` | `dictV` and priority-40 `.keys()` allocation are relevant. Literal/update/equality rules are unused. |
| `concrete.k` | Imported only by LLVM `MPY-KRUN`; its deep equality and keyed-sort legs are unused. It is absent from the proof module. |

At the selected semantics level, the used fixed rules give left-to-right call
and argument evaluation, ordered dictionary keys, finite structural list
iteration, ordinary scope updates, and explicit call/return state changes.
The unused opaque symbols (`md5hexCodes`, float symbols, `sortVS`, and
`sortKeyVS`) cannot influence this program's control, state, or result.

### Candidate-local definitional rules

The 24 local rules divide as follows:

1. Four exact AST definitions:
   `checkDictLoopBody`, `checkDictResultExpr`, `checkDictBody`, and
   `checkDictCaseModule`.  Each has one equation and is total.  They are
   byte-structurally faithful to `solution.mpy`.
2. Six classification equations:
   `stringCaseKey`, `lowerCaseKey`, and `upperCaseKey`, each with its
   constructor case and `owise` case.  For bare `str(IntSeq)` and non-reference
   values, these agree with `isStrV` and the supplied method predicates.
3. Six priority-30 operational splitter rules for `isinstance`, `islower`, and
   `isupper`.
4. Four structurally descending `allLowerKeys`/`allUpperKeys` equations.
5. Three `keySeenAfter` equations.  The `true/nonempty` overlap has identical
   right-hand side `true`; coverage is complete.
6. One total `checkDictCaseResult` equation, which is the standard remaining-
   keys loop invariant.

The ordinary equations have complete constructor coverage, descending
recursion, and no contradictory overlaps.  The lower/upper method splitters
are guarded to bare strings and agree with the supplied method equations on
their match domains.  The `isinstance` splitters are not equivalent on their
complete match domain.

### Materially unsound operational bridge and false witness

Candidate rules at `verification.k:62-71` match:

```text
#applyK(toCall(builtinV("isinstance")),
        (V, typeV("str"), .Vals))
```

with arbitrary `V` and arbitrary framed continuation/cells.  They have
priority 30.  In the supplied semantics, `call.k:38-41` first dereferences a
heap-reference argument and has priority 40.  Lower numerical priority wins,
so the candidate rule preempts the supplied dereference.

Use this ground state:

```text
V = ref(7)
heap = 7 |-> str(iCons(97, .IntSeq))   // underlying value "a"
```

The bridge-free supplied semantics proves:

```text
#applyK(... (ref(7), typeV("str"), .Vals)) => true
```

because it dereferences `ref(7)` before `isStrV`.  The candidate-extended
definition proves the opposite result `false`, because
`stringCaseKey(ref(7))` reduces to false.

This disagreement propagates to an actual submitted positive claim.  The
reviewer instantiated the exact `loop-and-return` precondition with:

```text
KS        = vCons(ref(7), .ValSeq)
SEEN      = false
LOWER     = true
UPPER     = true
OLDKEY    = noneV
DICT      = dictV(vCons(ref(7), .ValSeq), vCons(0, .ValSeq))
HEAP      = 7 |-> str(iCons(97, .IntSeq))
NEXTHEAP  = 8
```

and all exact scope/frame/control cells required by the claim.  There is no
`requires` clause excluding this state; `KS`, `DICT`, and `HEAP` have precisely
the sorts quantified by the claim.

From that same loop state:

- the bridge-free definition proves final result `true`;
- the candidate definition proves final result `false`.

The candidate's generalized postcondition also reduces to `false` because it
classifies `ref(7)` itself as a non-string.  Thus the candidate has proved a
false conclusion for a state satisfying the declared target precondition.

This witness is not an ordinary CPython dictionary state—Python list-like heap
references are not hashable dictionary keys.  That does not save the submitted
proof: the candidate deliberately states `loop-and-return` over arbitrary
`ValSeq` and arbitrary `Map`, supplies no well-formedness/reachability
precondition, and imports the false splitter globally.  The witness is inside
the positive claim's declared domain.  A narrower no-reference guard or a
proved well-formed-state invariant is absent.

Machine evidence:

- `evidence/21-kompile-bridge-free.log`: initial fixed-only definition build.
- `evidence/22-fixed-ref-proof.log`: fixed direct result `true`, `#Top`, exit 0.
- `evidence/23-extended-ref-proof.log`: candidate direct result `false`,
  `#Top`, exit 0.
- `evidence/25-kompile-bridge-free-with-helpers.log`: fixed-only definition
  with reviewer AST naming helpers, exit 0.
- `evidence/26-fixed-loop-witness-proof.log`: fixed loop result `true`,
  `#Top`, exit 0.
- `evidence/27-extended-loop-witness-proof.log`: candidate loop result
  `false`, `#Top`, exit 0.
- `evidence/bridge-audit-base.k`,
  `evidence/bridge-fixed-ref-spec.k`,
  `evidence/bridge-extended-ref-spec.k`,
  `evidence/bridge-fixed-loop-witness.k`, and
  `evidence/bridge-extended-loop-witness.k`: complete reviewer sources.

`evidence/24-fixed-loop-witness-proof.log` preserves an initial reviewer
parser-error attempt.  It is not used as evidence; the corrected artifact
subsequently built and proved successfully in evidence 25-26.

Because this is a concrete opposite-result witness under the fixed and
extended definitions, the splitter is a materially unsound operational
bridge, not merely an evidence gap.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted or reused.

I created `evidence/spec-vacuity.k`, copied it into scratch, and negated the
result-bearing destination of the loop claim:

```text
notBool checkDictCaseResult(KS, SEEN, LOWER, UPPER)
```

This mutation is false for satisfying states.  For example, with
`KS=.ValSeq`, `SEEN=true`, `LOWER=true`, and `UPPER=false`, real loop/return
execution yields `true`, while the mutated destination requires `false`.

`kprove --dry-run` parsed and built the mutation successfully and exited 0.
The real proof run exited 1 with `WarnStuckClaimState`; its residual contains a
fully executed `false ~> .K` branch and the unmet destination implication.
This is the expected result-bearing failure, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:

- `evidence/18-vacuity-dry-run.log`
- `evidence/19-vacuity-proof.log`
- `evidence/spec-vacuity.k`

The candidate proof is therefore non-vacuous and result-sensitive.  It remains
invalid because that result is obtained under the unsound bridge identified in
Stage 5.

## 7. Proven versus assumed accounting

### What the successful `#Top` runs establish

Under the *candidate-extended* K theory, they establish:

1. the exact submitted module/call/setup reaches the generalized loop state;
2. the generalized loop/return state reaches the Boolean fold named by
   `checkDictCaseResult`;
3. the result is constrained strongly enough that negating it produces a
   stuck proof.

They do not establish those facts under the unmodified supplied semantics,
because the candidate extension changes `isinstance` behavior on part of the
loop claim's domain.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted mounted supplied semantics | Defines all execution, cells, values, calls, and methods | Integrity-checked and authoritative for this audit. |
| K builtins/backend (`Int`, `Bool`, `String`, maps/lists, equality, rewriting/SMT) | Mathematical reduction and proof search | Ordinary toolchain trust boundary. |
| Supplied opaque float, MD5, and sorting symbols | Potential values in other programs | Imported but unreachable/unused here; no result influence. |
| ASCII `strToCodes` and ASCII case predicates | String literal execution and case results | Relevant intent limitation relative to CPython Unicode; witnessed by the Unicode run. |
| Candidate AST naming functions | Program identity/readability | Fully defined, exact, and acceptable. |
| Candidate list folds/result function | Postcondition and invariant | Fully defined and mathematically sound. |
| Candidate priority-30 `isinstance` splitters | Branch choice, accumulator state, final result | Illegitimate operational bridge; fixed-versus-extended opposite-result witness. |
| Differential testing | Python implementation-to-prompt/canonical bridge on 2,599 finite inputs | Empirical only; it does not replace a K connection theorem. |
| Informal composition of the two reachability claims | Entry-to-final theorem presentation | Interfaces match exactly, but composition cannot repair an unsound imported rule. |
| Partial-correctness interpretation | Termination is not the theorem's conclusion | Standard reachability/partial-correctness boundary. |

### Final decision

Clean build and non-vacuity pass.  Program/translator pinning also passes, and
the generated Python agrees with the natural-language predicate on the
preserved differential scope.  Nevertheless, the proof relies on a materially
unsound operational rule and proves the opposite of the fixed semantics on a
ground instance of its own positive loop claim.  This meets the
`FAIL / NOT_LEGIT` boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
