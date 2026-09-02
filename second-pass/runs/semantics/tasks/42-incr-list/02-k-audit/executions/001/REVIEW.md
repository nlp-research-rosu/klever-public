# Independent adversarial review: 42-incr-list

The candidate contains a legitimate, result-constraining partial-correctness
proof of its real translated program under the supplied MPY semantics. The
proof was rebuilt from source and rejects both a false result and a changed
program body. I assign concerns, rather than an unqualified pass, because the
four requested generation/provenance records are absent and because the formal
theorem covers finite lists of mathematical integers, while the Python prompt's
annotation says only `list`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is a real directory.
There is no infrastructure breach.

The recursive, no-symlink comparison found:

- `/candidate/reference-semantics/` has exactly the same entries, types, and
  bytes as `/reference/reference-semantics/`. There are no missing, extra,
  changed, mistyped, or symlinked semantics entries.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `8b6d8ac13f22a485fb80312ee1b077ba1cc2653fbff4c36fb7e3d36ca1b8d609`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. The candidate tree contains no symlink.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are all missing. No structured generation trace is
  present under any trace/generation filename. Consequently there were no
  generation claims, token metrics, prior report, or trace to inspect.

The exact tree, per-file semantics comparison, missing-artifact results, hashes,
command, and exit 1 (caused only by the four missing records) are in
`evidence/stage1-integrity.log`; the reviewer script is
`evidence/stage1_integrity.sh`. The absence of those untrusted provenance
records limits auditability but does not substitute for, or defeat, the fresh
proof reconstruction below.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt says: return a list whose elements are each incremented by
one. The trusted canonical implementation is the comprehension
`[(e + 1) for e in l]`. The candidate implements the same transformation by
allocating `result`, iterating over `l`, appending `x + 1`, and returning the
new list.

Running the trusted copied translator on the scratch copy of `solution.py`
produced a file byte-identical to submitted `solution.mpy`; both SHA-256 values
are
`811ba0bc5a0aa8ce22bfa580e3e6d165e2638b036e676be0f25b8a4acf753125`.
See `evidence/stage2_translation.sh` and
`evidence/stage2-translation.log` (exit 0).

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the generated entry point. It compares return value, return
type, input mutation, distinct-result allocation, and exception behavior over:

- both documented examples;
- eight explicit boundary cases: empty, one-element zero/negative/positive,
  two elements, mixed signs, 64-bit extrema, and 100-digit integers;
- 256 deterministic generated cases of lengths 0 through 16, with ordinary,
  64-bit-boundary, and arbitrary-precision values.

The complete 266-input JSON, seed `420042`, input digest
`4ca5b6e425d85bc7b2bd7128806dfcbedb84f113ca314e6540056606a4a9faf4`,
command, and result are in `evidence/stage2-differential.log`: exit 0,
`MISMATCH_COUNT=0`.

This establishes finite behavioral evidence, not a universal theorem. It
supports the implementation-to-canonical bridge for `list[int]`.

## 3. Clean proof reconstruction

All candidate sources were copied to `/tmp/audit-work/review/candidate`.
Trusted sources were separately copied to `/tmp/audit-work/review/trusted`.
No candidate-compiled definition or cache existed in, or was imported into,
the scratch builds. K was independently found at version v7.1.337; see
`evidence/tool-versions.log`.

Fresh build and concrete execution:

| Operation | Evidence | Result |
|---|---|---|
| LLVM build of `reference-semantics/semantics.k`, main `MPY-KRUN` | `evidence/stage3-kompile-runtime.log` | exit 0 |
| Candidate concrete assertions under the fresh LLVM definition | `evidence/stage3-krun-concrete-tests.log` | exit 0, final `.K`, `NoExc`, exit-code 0 |
| Auditor-authored Python harness | `evidence/stage3-fresh-python-harness.log` | exit 0 |
| Same auditor harness translated by the trusted translator and run under fresh K | `evidence/stage3-fresh-concrete-harness.log` | exit 0, final `.K`, `NoExc`, exit-code 0 |
| Haskell build of `verification.k`, main `VERIFICATION` | `evidence/stage3-kompile-verification.log` | exit 0 |

The fresh harness is preserved as
`evidence/stage3_concrete_harness.py` and covers empty, singleton, mixed-sign,
both documented, and arbitrary-precision inputs. Its translator/run driver is
`evidence/stage3_concrete_harness.sh`.

Positive proof targets:

- `SPEC.incr-loop` was run as an individual selected claim:
  `evidence/stage3-kprove-incr-loop.log` records exit 0 and `#Top`.
- `SPEC.incr-list` declares `[depends(incr-loop)]`, so its valid selected run
  must retain that dependency. The explicit selection of both target and
  dependency in `evidence/stage3-kprove-explicit-all-claims.log` records exit
  0 and `#Top`.
- An unfiltered independent run matching the submitted proof shape also records
  exit 0 and `#Top` in `evidence/stage3-kprove-all-long.log`.

Two attempts selecting only `SPEC.incr-list` timed out at 300 and 900 seconds
with no output (`evidence/stage3-kprove-incr-list.log` and
`evidence/stage3-kprove-incr-list-long.log`). These runs filtered away the
claim's explicitly declared dependency; they are recorded as resource
diagnostics and are not treated as proof failures. The dependency-correct
explicit run closes in about five seconds.

Compiler warnings concern unused variables and non-exhaustive functions in
unused supplied constructs. No warning occurs on a term reachable from this
program. Both required positive claims close under the freshly built proof
definition.

## 4. Adequacy and real-program pinning

### Claim meanings

`SPEC.incr-loop` starts at the actual `#loop` generated for the program's
`For(Name("x"), Name("l"), ...)`, with an arbitrary remaining integer sequence
`IS`, continuation `CONT`, current scope, accumulator reference `H`, and
accumulator prefix `PREFIX`. With no additional precondition, its post-state
has consumed the loop, preserved `CONT`, and changed the list at `H` to
`PREFIX` followed by `incrVals(IS)`. The final loop variable is existential,
which is harmless because neither the return nor the functional contract uses
it.

`SPEC.incr-list` has no `requires` clause. For every algebraic
`IS:IntSeq`, it starts from the exact initial MPY configuration, loads
`solutionProgram`, calls `incr_list` with `list(intVals(IS))`, and observes the
returned heap object. Its destination is `list(?RESULT)` and its mandatory
condition is the equality `?RESULT ==K incrVals(IS)`. This is an exact equality,
not a free result, tautology, or one-way implication. Normal environment,
empty stack, `noRet`, and `NoExc` are also required; final internal scope and
heap details are existential because the functional postcondition does not
claim them.

### Pinning

`verification.k:8-18` defines `solutionProgram` as the complete submitted AST:
the function name, parameter, ASCII docstring, empty result allocation, real
`for` statement, `append(x + 1)`, and return. The trusted translation identity
above independently pins that constructor tree to the submitted
`solution.mpy`. The entry computation loads this term and goes through the
supplied loader, function-definition, name lookup, call-frame, parameter
binding, statement, loop, append, return, and pop rules. It does not replace
the function with a summary.

The loop claim uses `incrLoopBody`, whose equation at
`verification.k:35-40` is exactly the real loop body. The entry claim's
`[depends(incr-loop)]` connects that helper claim to the real loop head.

The satisfying symbolic states and plain-language substitutions are recorded
in `evidence/stage4-claim-witnesses.md`. In particular:

- `IS=.IntSeq` yields `.ValSeq`, corresponding to `[]`;
- `IS=iCons(2,iCons(-1,.IntSeq))` yields
  `vCons(3,vCons(0,.ValSeq))`, corresponding to `[3,0]`;
- a loop prefix `[7]` and remaining input `[2,-1]` yields `[7,3,0]`.

Both Python implementations agree with all three substitutions
(`evidence/stage4-witness-check.log`, exit 0). Auditor-authored ground K claims
for the empty and two-element entry states each close with exit 0 and `#Top`
in `evidence/stage4-kprove-ground-empty.log` and
`evidence/stage4-kprove-ground-two-elements.log`. The claims themselves are
preserved in `evidence/spec-ground-witness.k`.

## 5. Rule-by-rule static soundness review

`evidence/k-rule-inventory.md` is the exhaustive line-addressed inventory,
generated by `evidence/inventory_k.py` from the fresh source. The reproducible
generation command, hashes, and exit 0 are in
`evidence/stage5-inventory-generation.log`. It contains 943 items:

- 231 local syntax-declaration blocks;
- 704 local rules;
- 5 contexts;
- 1 configuration;
- 2 claims.

It explicitly tags 149 function-declaration blocks, 110 `total` declarations,
29 priority-bearing items, 26 `owise` items, 4 macro items, 2 simplification
rules, and all 25 explicit `symbol(...)` declarations. There is no local
`functional` declaration. Every item includes its exact source, attributes,
reachability classification, and reviewer disposition.

### Supplied semantics and used-construct map

The configuration in `core.k:49-60` supplies module scope 0, builtins scope
-1, empty heap/stack, and normal return/exception state. The submitted AST uses
only these syntax families:

`Module`, `FuncDef`, `Params`, `Expr(Str)`, `Assign(Name,ListExpr)`,
`For(Name,Name,Stmts)`, `Call`, `Attribute`, `BinOp("+")`, `Int`, and
`Return`.

The real execution path maps to:

- module load and statement sequencing in `core.k:124-127`;
- function closure creation in `functions.k:14-16`;
- name lookup in `core.k:130-154`;
- callee/argument left-to-right evaluation and closure dispatch in
  `core.k:183-191` and `call.k:15-24,69-75`;
- call-scope allocation, parameter binding, return, and frame pop in
  `functions.k:62-90`;
- docstring conversion/discard in `str.k:13-17` and `controls.k:46-48`;
- list construction/allocation in `list.k:12-20` and `core.k:117-121`;
- assignment in `controls.k:8-18`;
- loop protocol/control in `controls.k:62-74` and target binding in
  `tuple.k:30-41`;
- integer addition in `operators.k:10-17` and `int.k:7-17`;
- `append`'s in-place update in `list.k:52-55`;
- final return/pop and the proof-harness observer.

Strictness/sequence-strictness on the AST syntax gives the required evaluation
order. The loaded definition binds `incr_list` in scope 0 before the call;
normal lookup selects that exact closure. The call creates scope 1, binds `l`,
and preserves the caller continuation in the stack. The empty result list is
freshly allocated, `result` keeps its reference, and every `append` updates
that same heap location. The `for` source is evaluated once. `Return` sets the
return value, discards the remaining function computation, and `#pop` restores
scope 0 before observation. There is no exceptional path for integer `+`.

Rules for floats, strings beyond the ASCII docstring, ranges, sets, dicts,
subscripts, comprehensions, sorting, assertions, and unrelated builtins cannot
match a term on this AST path. The 25 explicit supplied symbols (the float
operation family, `sortVS`, `sortKeyVS`, and `md5hexCodes`) are therefore
low-level unused trust boundaries; none can affect control, heap, returned
value, or either postcondition. `MPY-CONCRETE` is imported only by `MPY-KRUN`,
not by the proof module.

The fixed-semantics priority rules on the reachable path are containment
rules: heap-reference dereferencing, mutable-method selection, and cell-aware
variants. For `append`, `isMutMethod("append")` is true, so the priority-40
in-place append rule preempts the generic pure-method dispatch. Its state
footprint is exactly heap address `H`; it returns `noneV` as Python append
does. The ordinary and priority alternatives either have disjoint guards or
agree on their overlap. No used `total` function lacks a constructor case.

### Proof-local inventory

Every extension in `verification.k` was reviewed independently:

1. `solutionProgram` (`function,total`) is a terminating constant definition
   equal to the trusted-translated AST. It names execution; it does not
   summarize the answer.
2. `intVals(IntSeq)` is a fresh input-representation constructor, not a
   function or oracle. The two `#iterNext` equations cover exactly the empty
   and cons constructors of `IntSeq`. They yield the same head and tail that
   the fixed list-iterator rules yield for `.ValSeq` and `vCons`. Their full
   match context is a leading `#iterNext(...)` with an arbitrary preserved
   continuation; they read/write no cell, allocate nothing, raise nothing, and
   introduce no abrupt control. They cannot preempt the supplied iterator
   rules because those rules do not match `intVals`.
3. `incrVals` (`function,total`) has exhaustive empty/cons equations and
   recursively computes exactly `I +Int 1` for each element. Recursive descent
   is on the tail.
4. `incrLoopBody` (`function,total`) is the exact source body, not an
   abstraction.
5. The two `valSeqConcat` simplifications are right-association and right
   identity. They are true for finite sequences, agree with the supplied
   left-recursive definition on overlaps, and orient toward a right-associated
   terminating normal form.
6. `#observeResult` is a proof-harness observer after the function has
   returned. Its exact context is `ref(H) ~> #observeResult` followed by an
   arbitrary preserved suffix; it reads precisely `heap[H]`, consumes only the
   observer marker, and changes no program cell. It cannot bypass the call,
   loop, or return.

The fresh body-sensitivity experiment changes only the loaded program's
`Int(1)` to `Int(2)`, retains the original `[1]` obligation for input `[0]`,
and uses a separately compiled definition. The mutant build and spec dry run
both exit 0 (`evidence/stage5-body-mutant-kompile.log`,
`evidence/stage5-body-sensitivity-dry-run.log`). The proof then exits 1 with
`WarnStuckClaimState` and the concrete residual `list(vCons(2,.ValSeq))`
(`evidence/stage5-body-sensitivity-proof.log`). The preserved artifacts are
`evidence/verification-body-mutant.k` and
`evidence/spec-body-sensitivity.k`. This demonstrates actual body sensitivity
and rules out a result oracle that ignores the program.

No inventoried rule makes a false conclusion reachable on the intended
integer-list domain. Accordingly, there is no unsoundness allegation requiring
a false-conclusion witness; the limitations below are scope/evidence gaps, not
soundness defects.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or relied upon. The fresh mutation is
preserved as `evidence/spec-vacuity.k`. It uses the satisfiable empty input,
executes the complete real program, and changes the result obligation from
`[]` to the demonstrably false `[0]`.

`evidence/stage6-vacuity-dry-run.log` records a successful build/dry run
(exit 0). `evidence/stage6-vacuity-proof.log` records exit 1,
`WarnStuckClaimState`, and the expected reached residual
`list(.ValSeq)`, which cannot unify with the demanded nonempty list. This is an
unmet result obligation after normal execution, not a parser error, missing
import, timeout, unreachable mutation, or unrelated crash. The proof is
therefore non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What is formally established

Under the supplied MPY semantics plus the reviewed proof-local definitions,
for every finite algebraic sequence of mathematical integers `IS`, if the exact
submitted `incr_list` call terminates from the displayed initial configuration,
the observed returned list is exactly `incrVals(IS)`: same length and order,
with each element increased by mathematical integer one. The loop claim
establishes the accumulator invariant for an arbitrary prefix and remaining
suffix. This is partial correctness; it is not a theorem about all Python
objects or all CPython behavior.

### Trust ledger

- **Supplied MPY semantics:** selected by the problem and byte-identical to the
  trusted tree. All proof claims depend on its loader, scope, call, heap, loop,
  list, integer, and return rules. This is the intended fixed semantic level.
- **K toolchain and builtin theories:** K v7.1.337, the Haskell/LLVM backends,
  reachability/circularity machinery, mathematical integers, maps, lists, and
  equality are trusted. This is the ordinary machine-checking boundary.
- **`intVals` interpretation:** the external theorem encoding assumes
  `intVals(iCons(...))` denotes the corresponding finite Python integer list.
  Its only observable operation is exhaustively and transparently defined by
  the two iterator equations. This boundary is acceptable and not
  answer-bearing, but the bridge to Python values is informal plus finite
  differential evidence, not a separate bridge-free K theorem.
- **Translator/source bridge:** the translator and prompt are trusted mounted
  inputs; byte regeneration pins Python source to MPY. This bridge is directly
  reproducible.
- **Python intent bridge:** the trusted canonical implementation and 266-case
  differential run support equivalence on tested `list[int]` values. Testing
  is finite evidence only.
- **Opaque supplied symbols:** the 25 explicit float/sort/MD5 symbols and all
  unrelated partial functions are outside this execution path. No positive
  claim depends on their interpretation.
- **Generated provenance:** no generation log, metrics, final report, input
  record, or trace was available. Nothing from those missing records was
  assumed.

### Limitations and decision

The proof's `IntSeq` domain exactly covers finite lists of mathematical
integers, including negative and arbitrary-precision values. The source
annotation is merely `list`, and the canonical Python expression also accepts
other objects for which `e + 1` is defined (for example floats and booleans).
The examples strongly support integer lists as the intended core domain, but
the formal theorem does not cover non-integer numeric elements, Python
subclasses, custom addition, or exceptional inputs. It also does not state a
postcondition about input non-mutation or temporary heap shape, although both
Python implementations agree on non-mutation in the finite differential run.

These are documented intent/evidence limitations, not mechanisms by which a
false integer-list conclusion can be proved. Together with the missing
provenance records, they warrant `CONCERNS / LEGIT`. Clean reconstruction,
exact result equality, body sensitivity, satisfying witnesses, and the fresh
false mutation establish that the submitted proof itself is legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
