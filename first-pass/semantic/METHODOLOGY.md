# Verifying all 164 HumanEval solutions in K — methodology

*A narrative + technical account of how every OpenAI HumanEval reference solution was
formally verified in the K Framework. Written as source material for a tech report:
it records not just the final techniques but the journey — the design decisions, the
dead-ends, the intuitions that turned out wrong, and the reasoning that fixed them.*

*Companion documents (authoritative, terser): [`../NOTES.md`](../NOTES.md) (cross-cutting
proof techniques and K frictions), [`../ROADMAP.md`](../ROADMAP.md) (the four-technique
taxonomy and status), [`../PROVEN.md`](../PROVEN.md) (all 164 in completion order),
[`CANONICAL-GAPS.md`](CANONICAL-GAPS.md) (what the rewrites simplify away),
[`src/`](src/) (the copy-select semantics library), and the
[`notes/*-probe/`](notes/) investigations (the differential probes cited throughout).*

---

## 0. Result and one-paragraph summary

**All 164 HumanEval problems (`HumanEval/0`–`/163`) are verified end-to-end in the K
Framework** (installed K v7.1.293, Haskell/Booster backend `kprove` + Z3). For each
problem we take the dataset's own reference Python (`canonical_solution`), turn it into a
minimal, sound K semantics, and discharge a reachability `claim` to `#Top` that says the
function computes a differential-tested *summary specification*. A proof counts only if it
passes four gates: (1) the verified solution is behaviour-equivalent to the dataset
canonical, (2) the concrete program passes a `krun` "smoke" run of the dataset test cases,
(3) `kprove` reaches `#Top` over **symbolic** inputs, and (4) a corrupted postcondition
*fails* to prove (non-vacuity). Genuine domain knowledge that is not the program's own
logic (a sort is a sorted permutation, `x**0.5` is a square root, MD5 is a hash,
operator-precedence `eval`) is reduced to a small number of **trusted, irreducible
`[simplification]` lemmas** — honestly flagged, meant to be discharged later in "klean"
(Lean-in-K). The whole thing was built from a clean slate on git branch `yuqing/pass-0`.

---

## 1. Starting point: a clean slate and a self-contained dataset

The project began with a deliberate **nuke-and-restart**. An earlier attempt existed but was
judged "too convoluted" — it drove a formal-verification-kit (FVK) skill through a 7-step
Codex prompt chain, and its proofs (see §3) were unreliable. The user's instruction was to
"build the thing from the ground up interactively," treating the FVK reference as *"not
reliable and very likely to contain mistakes.*" So the working tree was reduced to
`.gitignore`, `.gitmodules`, and the vendored `references/` submodules; all subsequent work
is per-problem, hand-crafted, and interactively reviewed.

**The dataset is self-contained** (`data/humaneval/HumanEval.jsonl`, 164 records). Each
record has five fields that anchor the entire methodology:

| field | role |
| --- | --- |
| `prompt` | the question: imports + signature + docstring (with doctest examples), body-less |
| `canonical_solution` | the reference **body** fragment — completes the prompt |
| `entry_point` | the function name, e.g. `has_close_elements` |
| `test` | a `check(candidate)` function of asserts (the hidden tests) |
| `task_id` | e.g. `HumanEval/0` |

`prompt + canonical_solution` is the complete runnable reference; `test` supplies the
ground-truth `check` cases. `scripts/dissect_humaneval.py` splits all 164 into regenerable
per-problem folders (`{num}-{entry-point-dashed}/`, e.g. `3-below-zero`); a self-check ran
all 164 assembled programs and confirmed 164/164 pass their own tests. Only the *script* is
committed — the generated folders are `.gitignore`d and reproducible from the dataset.

---

## 2. The representation: `.mpy` and the pure transliterator

A Python program is verified through an intermediate term language called **`.mpy`**: the
Python AST re-spelled 1:1 as K constructor terms. `scripts/py2mpy.py` does `ast.parse` →
walk → emit, where **each AST node maps to exactly one K constructor** and *no* semantics
is carried. For example `below_zero` becomes

```text
Module(FuncDef("below_zero", Params("operations"),
  Assign(Name("balance"), Int(0))
  Assign(Name("result"), Bool(false))
  For(Name("op"), Name("operations"),
    AugAssign(Name("balance"), "+", Name("op"))
    If(Compare(Name("balance"), CmpOp("<", Int(0))),
       Assign(Name("result"), Bool(true)), .Stmts))
  Return(Name("result"))))
```

Two design commitments make this work:

- **Purity.** py2mpy is a *pure transliterator* — "keep the behaviour as controllable as
  possible." The two semantic shortcuts an earlier front-end had baked in were removed:
  `is`/`is not` are emitted as `CmpOp("is", …)` (not collapsed to `==`), and chained
  comparison `a < b < c` becomes one `Compare` carrying the operator *and* operand lists
  (not pre-`and`ed). Method calls stay `Call(Attribute(recv, "append"), …)`. All meaning is
  deferred to the K layer; the only unavoidable "decision" is reading a literal's Python
  type (`bool` before `int`, since `bool ⊂ int`).

- **The two-halves contract.** The constructor names py2mpy emits and the syntax productions
  in the `.k` grammar are *two halves of one interface*. There is no type-check between
  them; a mismatch simply fails at `kparse`. py2mpy's emitted vocabulary is therefore the
  living spec the grammar must satisfy.

- **The coverage gate = the soundness backbone of translation.** Any AST node py2mpy does
  not handle raises `Unsupported(<NodeType>)` and stops, *naming the node*. So py2mpy
  accepts exactly the Python subset the semantics models — nothing slips through unmodeled.
  `import`/`from-import` emit no-ops (no module system); any *use* of an imported name goes
  stuck in K. A first coverage sweep of all 164 canonicals transliterated **148/164** cleanly;
  the 16 gaps were honest gates (10 keyword-args, 4 lambda, 1 `try`, 1 for-else), not bugs.

Output is Lisp-indented for readability; `--ast` dumps the Python AST for eyeball 1:1
checking. The vocabulary spans expressions (`Int Float Str Bool NoneVal Name BinOp UnaryOp
BoolOp Compare/CmpOp ListExpr TupleExpr Subscript Slice Attribute Call IfExp
ListComp/GenExp/CompFor …`) and statements (`Module FuncDef/Params Assign AugAssign Return
If For While Break Continue Pass Assert Expr Import ImportFrom`); statement lists are bare
juxtaposition.

---

## 3. Why the old proofs were unreliable — and what "reliable" means here

Before building anything, the two old proofs that had reached `#Top` (`below_zero`,
`separate_paren_groups`) were audited. They *type-checked* as proofs but certified far less
than they appeared to, and understanding exactly why set the reliability bar for the whole
project. The old `verification.k` introduced a **parallel model**: a fresh algebraic list
type `IList`, a fresh loop `#iloop`, and a rule that swapped the real `#forIn` over the heap
list for `#iloop` over `IList`. Four gaps followed:

1. **The model↔reality bridge is asserted, never proved.** The old `SPEC_AUDIT.md` says it
   outright: *"the symbolic bridge is not proved."* They had tried native symbolic lists and
   retreated because *"the native empty-`#loop` rule matched too broadly before K could split
   the symbolic list."*
2. **The input domain is secretly narrower.** The paren loop `#ploop` knew only `(`, `)`, and
   space — it cannot represent a string with any other character. `IList` is a clean symbolic
   list, not `List[int]`.
3. **Summary functions are trusted axioms** — `[simplification]` rules rewritten *with*, never
   proved and never differential-tested. A subtly wrong summary closes the proof and certifies
   the wrong property.
4. **Even `Name` lookup is overridden** in the proof module — so the proof runs different rules
   than concrete execution.

What `#Top` actually certified there was: *"the hand-built model satisfies the summary spec,
for symbolic inputs within the restricted proof domain."* This diagnosis produced the
project's **five reliability principles** (now in `NOTES.md §Reliable-proof methodology`):

1. **No proof-domain bridge.** Drive the *same* rules and data that `krun` executes; inject
   symbolic inputs without forking the execution path (e.g. a `syntax Expr ::= Val` subsort
   so a symbolic `list(…)` can be a call argument).
2. **One semantics for execution and proof.** No proof-only rule overrides. Env access must
   work for both concrete `krun` maps and symbolic `kprove` maps.
3. **Differential-test every summary axiom** against CPython on random inputs (typically 0
   mismatches over 50,000 samples) *before* trusting it.
4. **Prove non-vacuity.** Corrupt the postcondition and confirm `kprove` fails, so `#Top`
   genuinely depends on the claimed property.
5. **Keep the real input domain** — quantify over arbitrary symbolic inputs.

**The honest "proven chain"** the project stands behind:

```text
canonical ──(diff-test ~40–60k random + hidden test)──▶ rewrite
          ──(py2mpy)──▶ .mpy
          ──(kprove #Top over ALL symbolic inputs)──▶ summary
          ──(diff-test 0/50k vs CPython)──▶ CPython
```

Only the middle link is a machine proof; the two end links are differential-tested; the
minimal-consistent per-problem semantics (shared by `krun` and `kprove`, no bridge) is the
trust base.

---

## 4. The golden template: `HumanEval/3 below_zero`

The first end-to-end proof, `3-below-zero`, is the reference template every later proof
copies. Its construction fixed the core machinery.

- **Represent the iterated structure with an algebraic cons-list in the semantics itself.**
  `List[int]` is `seq(IntSeq)` with `IntSeq ::= .IntSeq | iCons(Int, IntSeq)`. K's builtin
  `List`/`Map` cannot be inducted over symbolically — that is *the* reason the old proofs
  built a bridge — whereas an algebraic cons-list shared by `krun` and `kprove` inducts
  cleanly with no bridge. Strings are modeled the same way: `str(IntSeq)` of char codes.
- **The proof is two claims.** Claim 1 is the **loop invariant = induction hypothesis =
  circularity**: for any `IntSeq S`, running `#loop(S, …)` from a scope with `balance=B,
  result=R` ends with `balance = B + sumSeq(S)`, `result = R orBool wentNeg(S, B)`. kprove
  applies this claim to the tail `REST` — self-application, well-founded because ≥1 rewrite
  step consumes the head. Claim 2 is the **entry theorem**, which reaches `#loop(OPS,…)` and
  applies claim 1 as *one step* instead of unrolling. `=>` is **rewriting/reachability, not
  equality**; `[all-path]` means "from any LHS state, every path reaches RHS."
- **The summary functions are the spec.** `wentNeg`/`sumSeq` are `[simplification]` rewrite
  rules stating what the code *should* compute; the postcondition asserts `result ==
  wentNeg(OPS, 0)`. They were differential-tested vs CPython at 0/50000 before use.
- **Observe the result in program state.** The entry claim runs the real `Assign(Name("result"),
  Call(below_zero, …))` to `<k> => .K` and asserts the root-scope binding `result <-
  wentNeg(OPS, 0)` — program-faithful. (Later standardized to the `ensures ?R == summary`
  form; see §11.)

**The two headline frictions surfaced here** and recur throughout:

- **Symbolic maps do not normalize over a symbolic base.** A loop body produces shadowed keys
  (`[balance<-B]…[balance<-B+I]`); over a *symbolic* base map K will not collapse them, so the
  circularity cannot match and the proof stalls. Fix: write the invariant's bindings over a
  **concrete `.Map` base** listing the function's exact locals — what execution produces
  anyway. (Deeper cause, understood later: matching is structural and shallow, reading
  constructors; symbolic env access must be phrased as *functions* — `{ENV[X]}:>Val`,
  `M[X <- V]` — so `MAP-SYMBOLIC`'s lemmas peel updates without knowing the base.)
- **Non-vacuity as a discipline.** Corrupting the postcondition to `result <- false` made
  `kprove` fail the implication check, confirming `#Top` was non-vacuous.

---

## 5. Minimal *and* consistent semantics; the scope-chain function model

The governing principle, in the user's words: *"we want a minimal-consistent semantic.
Minimal means we don't want anything more than the `.mpy` node. Consistent means every
reachable/expressible reduction must be sound — and it should not be achieved by leaf-cutting
and guarding (which is ad-hoc and tends to miss cases); that is done only when there's no way
around."* Two halves:

- **Minimal** — a problem's `semantics.k` declares only the constructors that problem's
  `.mpy` uses. Constructs the program cannot express need no handling.
- **Consistent** — every program the semantics *can* express and reduce must be **sound**. A
  reachable reduction that yields a *wrong* answer is a bug; **getting stuck is fine** (it
  faithfully models an error). Soundness comes from a *correct-by-construction model*, not
  guards. Guards are ad-hoc and miss cases, so they are a last resort.

This principle drove the single most important semantics decision. The first function model
used a global `<funcs>` table plus a flat `<env>`. It had two *reachable-wrong* paths: a
nested `def` wrote the global table (making the inner function global), and `closure(PS,BODY)`
captured no defining environment (free variables in a true closure would be stuck). The first
fix patched these with guards; the user rejected that as "hacky" and the model was rebuilt as
a **lexical-closure scope-chain**: `<store>` holds `scope(bindings, parent)` records, `<env>`
is the current scope *location* (an `Int`), `closureVal` captures its *definition* scope, and
call frames are `frame(continuation, callerEnv)`. This is correct by construction —
scope-chain lookup finds a local before a global, a nested def lands in the enclosing scope —
so both guards were *deleted*.

A measured and important cost finding (`NOTES §"loops free, recursion pays"`): the heap/scope
env costs a **loop** proof *nothing* (the loop makes no calls, so `<store>` never grows — the
invariant just moves from a flat map into one scope record), but a **recursion** proof *does*
pay (the store grows one scope per frame). This was validated with throwaway probes
(`/tmp/rec.k`, `/tmp/clo.k`): closures and recursion *execute* fine, a non-recursive proof
closes `#Top` instantly over the heap env, but a recursion proof (`count_down`) times out.
"Closures are cheap; recursion proofs are hard, with or without closures."

The **return model** was likewise worked out against the K/RV corpus rather than guessed. A
naive one-item-at-a-time unwind hangs a `while True: return`, because the standard SIMPLE
idiom `return V; ~> _ => V ~> K` discards the *entire* rest of the `<k>` cell atomically
(loops included) — you cannot strip it item by item. The reference adopts the frame-skip
idiom with a **decoupled pop**: `V ~> #ret ~> _ => #pop` (discard the frame body, staging the
value in a `<ret>` cell) and `#pop => V ~> CONT` (a clean head-rewrite that pops the frame).
Decoupling keeps the **loop invariant LOCAL** — it describes the loop's effect on the
frame-local `<env>`/`<store>` and never names the `<stack>` — which is exactly what RV's
`python-semantics`, WASM `loops-spec`/`functions-spec`, and IMP++ `sum-spec` all do. (A
concrete-stack shortcut proved `below_zero` but was nested-call-unsafe; the local-invariant
discipline is the general answer.)

---

## 6. The copy-select reference library

Once ~60 problems shared a large common core, the semantics was consolidated into
[`src/`](src/) — the **authoritative** version of every construct, split RV-style into one
module per file and assembled by `src/semantics.k` (module `MPY`):

| file | module | holds |
| --- | --- | --- |
| `mpy-syntax.k` | `MPY-SYNTAX` | AST productions |
| `mpy-core.k` | `MPY-CORE` | **the configuration**, `Val` sorts, load/seq, `Name` lookup, `truthy`; *declares* `applyBin`/`applyCmp` |
| `mpy-operators.k` | `MPY-OPERATORS` | UnaryOp/BinOp (incl. floored `pyMod`)/Compare/BoolOp/IfExp |
| `mpy-str.k`, `mpy-list.k`, `mpy-tuple.k`, `mpy-subscript.k` | … | strings, the general `list(ValSeq)`, tuples, subscript/slice |
| `mpy-statements.k` | `MPY-STATEMENTS` | Assign/AugAssign/If/For/While/break/continue |
| `mpy-functions.k` | `MPY-FUNCTIONS` | def/call/return frame stack |
| `mpy-builtins.k` | `MPY-BUILTINS` | `len/sum/abs/min/max/ord/chr/str/range`, `all`/`any` |
| `mpy-comprehension.k` | `MPY-COMPREHENSION` | list/gen comprehensions |
| `lemmas.k` | `MPY-LEMMAS` | proof-only lemma layer (imports `MPY`; never the reverse) |

**Copy-select, not import.** A per-problem `semantics.k` is *cut from* these modules, not
imported. Importing `MPY-LIST` would make `ListExpr` reducible even when the program never
uses it, breaking minimality — so per-problem cuts stay single-file and trimmed *below* file
granularity (dropping individual `Val` variants and `applyBin`/`applyCmp` cases). The split
exists for the reference's navigability; the reference is the single source of truth for *how*
each construct is written, so a rule never drifts between problems. An improvement to a
construct lands here first, then propagates.

Design decisions folded into the library along the way, each checked against CPython or the
RV corpus:

- **Floored `%`/`//`.** Python `%` is floored (sign of the divisor): `-7 % 3 == 2`,
  `7 % -3 == -2`. K's `modInt` is *Euclidean* and `%Int` is C-truncated; both are wrong for a
  negative divisor. The reference uses `pyMod(a,b) => ((a %Int b) +Int b) %Int b` and
  `a // b => (a -Int pyMod(a,b)) /Int b`. (For a positive divisor — every HumanEval `%`/`//` —
  `modInt` happens to agree, which is why the old proofs survived; the general rule is still
  the sound one.)
- **Short-circuit variadic `and`/`or`.** `BoolOp("or", A, B, C)` is variadic and value-returning
  (`1 and 2 == 2`), so it is modeled with a continuation `#boolL` that stops at the first
  decisive operand. Crucially `truthy(V)` stays in the `requires` guard, never in the `<k>`
  cell — because the value you *test* is not the value you *return*.
- **ASCII-only strings, non-ASCII stuck.** An empirical probe found K's string lexing
  inconsistent for non-ASCII (`ord("é")` → 233 code point, but `strToCodes("中")` came through
  as raw UTF-8 bytes `iCons(228,184,173)`). Rather than return a wrong answer, `strToCodes` and
  `chr` are guarded to `code < 128`, so a non-ASCII code jams — the faithful-error discipline.
  The whole corpus is ASCII, so the invariant "every code in a `str(IntSeq)` is 0–127" holds
  and all string ops are sound.
- **Lazy `range` and one unified `#loop`.** `range` is a lazy `rangeObj(Int,Int,Int)` `Val`
  iterated by a single `#loop` via RV's `__next__` protocol; the per-kind advance must be
  **rewrite rules (which case-split), not a function** (a function guard forces kprove to
  *decide* `I < HI` for symbolic `N` → `DecidePredicateUnknown`).
- **In-cell loop label (from WASM `loops-spec.k`).** The loop-back continuation lives *in* the
  `<k>` cell as `loopLbl(#loop(tail))`, and `break`/`continue` (`#brk`/`#cont`) navigate the
  cell to the nearest `loopLbl`, discarding one item at a time. This let verification demos run
  over the *whole* `MPY` semantics (no cut) — and, notably, showed that **in-cell `continue`
  needs no resume slot**, retiring the earlier `<lstack>` side-cell.
- **Partial operations stay partial.** `l[0]` is `applyIndex(seq(iCons(H,_)), 0) => H` — one
  rule, index 0 only; on `[]` there is no rule so it gets stuck, exactly Python's `IndexError`.
  Never add a total fallback (a default would be a reachable wrong answer); instead restrict the
  entry claim to the function's real domain.

The library is kept kompilable and tested: `tests/semantics/<case>/` pairs a CPython oracle
`.py` with the `.mpy` K runs (each case is differential), and `tests/verification/<case>/`
holds self-contained `kprove` demos (`loop-break`, `loop-continue`, `range-loop`).
`CANONICAL-GAPS.md` tracks, per feature, what the rewrites deliberately avoid (comprehensions,
`.append` list-mutation, `.split`/`.join`/`.lower` method dispatch, `lambda`) so the choices
are recorded, not accidental.

---

## 7. The proof *gate suite* (per problem, non-negotiable)

Every problem runs the same pipeline, copying `3-below-zero`:

1. **Solution + oracle.** Write `solution.py` (== canonical where possible; otherwise a
   behaviour-preserving rewrite that avoids blocked constructs), and *verify* equivalence to
   the dataset canonical over ~20–60k random + corner inputs (0 mismatches) **and** the hidden
   `check`. Generate `.mpy`, `smoke.py`, `smoke.mpy` via `py2mpy`.
2. **Minimal semantics.** `semantics.k` cut from the reference; `kompile --backend llvm`; run
   **`krun` smoke** (dataset `check` cases as `Assert(…)`) — must give `<exc> NoExc`, exit 0.
   The smoke gate catches constructors the symbolic proof never touches (e.g. an input `ListExpr`
   the solution receives as a parameter) — never skip it.
3. **Verification + spec.** `verification.k` holds the `[simplification]` summary functions,
   **differential-tested 0/50000 vs CPython**; `spec.k` holds the loop-invariant circularity +
   entry claim. `kompile --backend haskell`; `kprove` → **`#Top`**.
4. **Robust non-vacuity.** Corrupt the postcondition; re-`kprove`; confirm **absence of `#Top`**
   (`grep -c '^#Top'` is 0). This is subtle and was hardened twice: a corrupted spec can fail
   *either* by "the implication check … has failed" *or* by getting stuck ("configuration cannot
   be rewritten further") — both count, so test for absence of `#Top`, not a specific error
   string. The corruption must use a **constructor the module defines** (a foreign sort gives a
   *parse error*, not a refutation), and the "cannot be rewritten further" phrase may be
   line-wrapped (join before grepping). Prefer a cheap **constructor-clash** corruption
   (`result := str("")` where a list is expected) — never put the symbolic summary term on both
   sides of the implication (that triggers an occurs-check blowup).

Two operational rules, both learned from incidents:

- **Memory-capped `kprove`, always.** A non-vacuity corruption once sent `kore-exec` into an
  occurs-check blowup that exhausted RAM+swap and OOM-killed the editor. Every `kprove` (proof
  *and* non-vacuity) now runs inside a cgroup:
  `systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet timeout 1800 kprove …
  [--depth N]`. `MemorySwapMax=0` is the critical half — it prevents the multi-minute
  swap-thrash *before* the OOM. A run killed by the cap is *inconclusive*, not a refutation.
  A correctly constructed HumanEval proof closes fast, so hitting the cap signals a
  mis-constructed spec.
- **Rebuild the haskell definition after ANY `semantics.k` edit** (even a comment) before
  `kprove` — a stale kompiled definition vs newer source surfaces as a spurious
  "module differs / outer parse error" (exit 113), which repeatedly masqueraded as a real bug.

---

## 8. The differential-probe methodology (the meta-technique)

The single most transferable lesson: **never trust intuition about *why* a proof fails or
whether a construct is needed — build a minimal, one-variable differential probe** (a tiny
semantics with a small controlled difference) under [`notes/<name>-probe/`](notes/), and
confirm a known-good configuration reproduces `#Top` before concluding anything. This is now a
standing memory (`differential-probe-proofs`). It was earned the hard way: over the project,
several confident "kprove can't do X" conclusions were *all* wrong, and probes overturned them.

**The Z3 mechanism the probes exposed** (the technical heart of the whole approach). At a loop
invariant's inductive step, the reached term is `(A +Int I) +Int Y` and the goal is
`A +Int (I +Int Y)` where `Y = summary(...)` — pure `+Int` associativity. `+Int` is a *hooked
function, not an AC constructor*, so kprove does not normalize it structurally; it hands the
term to Z3. Z3 closes associativity by treating `summary(...)` as *some fixed integer* via
**congruence** — but only if the symbol is **`[total]`** (defined everywhere, hence
SMT-abstractable). A partial `[function]` is *not* sent to Z3, so kprove falls back to a
*syntactic* comparison, `(A+I)+Y ≠ A+(I+Y)`, and fails. This has an exact **counter-vs-list
asymmetry**: structural recursion *decreases* its argument, so its summary can be `[total]`;
arithmetic recursion *increases* toward `N` (`I+1`), so K's termination check rejects `[total]`.
The three ways out, each used in the corpus:

1. a **closed-form** summary (no recursive function symbol — e.g. Gauss `N*(N-1)/2` for a
   `range` sum, which Z3 discharges including the floor `/2`);
2. a **`[total]`** summary (when the recursion is structural);
3. **thread the accumulator** — `sumRange(I, N, ACC)` instead of `ACC + sumTo(I,N)` — so each
   step's reached term is syntactically equal to the unfold and no associativity is needed.
   Parameterize the summary by `(current, stop)`, not `(start, count)`, so the unfold matches the
   induction hypothesis directly.

Three probes made this concrete, each overturning a "wall":

- **`lstack-probe`** — the belief that a `<lstack>` side-cell "jams on a symbolic counter" was
  false; an 8-rung ladder (counter/seq × total/non-total/threaded/closed-form) showed the *only*
  real failure is an additive **non-total** summary; the sequence loop fails too once its summary
  is non-total.
- **`ret-probe`** — the belief that the `#ret ~> #pop` *split* is necessary was false; the
  apparent failure was a probe bug (a stray `...` after `~> _` leaving a dangling tail var). The
  split only *buys* a stack-agnostic local invariant.
- **`val-cast-probe`** (the marquee result) — iterating the general heterogeneous `list(ValSeq)`
  in a proof. A circularity folds a symbolic sequence only if the loop variable is in
  **constructor position** (not buried in a function like `ints2vals(IS)`, where kprove
  unifies-not-splits) *and* the split exposes a concrete-sort head. For `list(ValSeq)`, a symbolic
  element `V:Val` cannot be branched on (`if x<0`) because a bare `{V}:>Int` downcast is partial
  and not SMT-representable. The fix, taken verbatim from RV's `kasmer` `ceils.k` idiom, is a
  **total cast**:

  ```k
  syntax Int ::= projectIntTotal(KItem) [function, total, symbol(projectIntTotal), no-evaluators]
  ```

  Being *declared* total (with `no-evaluators` it stays abstract on symbolic input), Z3 treats
  `projectIntTotal(V)` as an unknown integer, so `projectIntTotal(V) <Int 0` is decidable and the
  branch splits. `[simplification]` bridge rules (`{V}:>Int => projectIntTotal(V) requires
  isInt(V)`) make it kprove-only and inert for `krun`. It is *sound* because a partial function
  can be totalized with junk on undefined points, and an `allInt(VS)` precondition guarantees the
  proof only ever hits real ints (where it equals the true cast) — the standard
  uninterpreted-total-function idiom, the same one KEVM uses for `keccak`/`hash`. (A caution
  learned here: a *partial* fold summary landing in a config cell can crash the Haskell backend
  outright with `\bottom`/`ErrorBottomTotalFunction`, because a total `Map:in_keys` over the tainted
  scope hits `\bottom` — so **mark `[total]` every exhaustive helper that appears in `<store>`/`<k>`**,
  the summaries *and* the structural builders `seqConcat`/`strSeqConcat`/`reverse`.)

---

## 9. The technique catalog (the "recombination" middle)

The bulk of the 164 were reached by *recombining* a growing ladder of primitives, each
introduced by proving one problem that establishes it, then reskinning siblings (often by
`sed` from the closest proven sibling, always re-running the full gate suite — "cheap to
build, not cheap to trust"). A condensed catalog (fuller detail in `NOTES.md`):

- **Scalar / bool / value-predicate folds** — `below_zero`(3), `below_threshold`(52),
  `double_the_difference`(151), `digitSum`(66). Define the summary with the *same branch-split*
  as the program's `If` (`maxFold` split on `e > m`) so paths line up with no extra lemma.
- **Dual / coupled / position-dependent folds** — tuples via one invariant updating both
  accumulators (`sum_product`(8)); Kadane's coupled `cur`/`best`(114); position-dependent folds
  carrying an index accumulator (`sum_squares`(142)); a **`prev`-accumulator** turning an
  adjacent compare `arr[i]<arr[i-1]` into a forward fold (`can_arrange`(135)); wider windows
  carrying N previous elements (`is_happy`(80), `get_closest_vowel`(118)); flag-parameterized
  folds with existential post-loop state (`intersperse`(5)).
- **Strings as `str(IntSeq)`** — reverse-and-compare palindromes (48), char-vs-literal compare via
  a structural `==K` decomposition lemma (`iCons(C,S) ==K iCons(D,T) => C==Int D andBool S==K T`)
  reducing to Int reasoning (61); string MAP vs string FILTER (27 vs 51); `ord`/`chr` as
  **name-dispatch builtins** intercepting `Call(Name("ord"),…)` before the generic call rule;
  multi-way membership as a short-circuit `or` (64); left-append list/string builders needing two
  concat lemmas (right-reassociation + right-identity, `seqConcat(S,.IntSeq)=>S`, 30).
- **Containers** — list-of-strings `strs(StrSeq)` layered on strings (28, 29); higher-order filter
  with a **symbolic element-predicate** (`startsWith`/`contains` kept as an opaque total `Bool`, so
  body-`If` and summary branch on the *same* term — the proof establishes the filter *structure*
  independent of the predicate's value, 29/7); `zip` two-list lockstep induction (`#zipLoop`, two
  base cases, 152/11); the general heterogeneous `list(ValSeq)` (§8).
- **Control flow** — statement-`If` and guard-chains whose spec is a closed-form `#if … #then …
  #else … #fi` (159/102; requires `imports K-EQUAL`); multiple sequential loops, one invariant per
  loop keyed by loop body (110); `for i in range(len)` recognized as element-iteration + an index
  counter (no general subscript needed); `split()` as a scan with a **trailing-sentinel delimiter**
  so the last flush happens in-loop (101/117).
- **`while` loops** — the first (`how_many_times`(18)) showed a `while` proves like a `for`
  because its body desugars back to `While(cond, body)` — the same circularity shape; induct on
  whatever the condition shrinks (`rest[1:]` tail-drop). `while`s consuming a *structure* (suffix)
  are in reach; `while`s counting down a *number* need numeric-measure or partial correctness (§10).
- **Nested loops** — run the inner `#rangeLoop` in the `<k>` *head* with the outer step as
  continuation (`#afterInner`), and reuse the inner invariant as a lemma for the outer; use
  cell-frame `... </k>` claim form (a `~> REST` framing times out). First proven on
  `find_closest_elements`(20), then a jagged 2D matrix `get_row`(87) with *no* trusted primitive
  (scan each row's columns descending → row-asc/col-desc directly).

---

## 10. Four techniques for hard domains (Xiaohong's taxonomy)

`ROADMAP.md §2` records the taxonomy that unblocked everything believed "blocked," in order of
preference:

1. **Direct minimal-semantics proof** (loop-invariant circularity + differential-tested summary)
   — the default, most of the corpus.
2. **Trusted domain primitive → klean.** When a fact is genuine mathematics/engineering rather
   than the program's logic, model it as an opaque `[function, total, symbol(…), no-evaluators]`
   symbol (opaque on symbolic input, concrete for `krun`) plus **`[simplification]` lemmas stating
   exactly the domain facts the wrapper needs**. The K proof then verifies the *wrapper*; the
   lemmas are **trusted in K and meant to be proved in klean (Lean-in-K)**. Discipline: minimize
   the number and complexity of the lemmas and make each one *state a meaningful domain fact*, not
   restate the spec. Used for `sortI`/`sortD`/`sortLA` (sort — whose correctness is *also* proved,
   see below), `isP` (is_prime), `projectIntTotal` (val-cast), `heronArea` (float area),
   `md5hex` (hash), `doAlgebra` (operator-precedence eval).
3. **Partial correctness (coinductive).** For loops whose termination is unknown or has no
   closed-form trip count, prove "**if the loop halts, the result is correct**." kprove's
   `[all-path]` circularity is *coinductive* (greatest fixpoint) — it discharges the recursive case
   with no termination measure, guarded by the "≥1 step of progress" firewall. Use a
   threaded-accumulator summary. Validated in `partial-correctness-probe` on a real Collatz `3n+1`
   loop, then used for `factorize`(25), `is_multiply_prime`(75), `get_odd_collatz`(123, Collatz),
   `prime_fib`(39), and the two float `while`-loops of `find_zero`(32). The theorem is stated
   honestly as *partial* in each `PROOF.md`.
4. **Threaded shrinking-loop (total).** A `while n>0: n //= 10` loop *does* halt; the
   threaded-accumulator trick makes the arithmetic close for *total* correctness, unlocking
   digit/bit decomposition of a symbolic int (`skjkasdkd`(94), `unique_digits`(104)).

### Case study — the opaque-sort cluster (six problems, long believed blocked)

Problems that *sort then process* stalled because the reference formulations **iterate** the
opaque `sortI(L)` term, which is neither `.IntSeq` nor `iCons`. Two independent routes cracked
the whole cluster:

1. **Index-reformulation (preferred).** The result is a position-function of the sorted ranks, so
   reformulate to **index** `sortI(L)` by position via the opaque accessor `atK` (the "120/47
   trick"), and rebuild with a plain `range` loop. Nothing iterates the opaque term. `strange_sort_list`(70)
   is `s[i//2]` / `s[n-1-i//2]`; also 37/33/105/19.
2. **Universal loop-invariant lemma.** State the post-sort loop over a *fresh* symbolic sorted list
   `S` (proved by the fold circularity); the entry's `sortI(L)` loop closes as the instance
   `S := sortI(L)`. Sound because a `∀S` lemma is applied to a specific term (no havoc). Validated
   in `sort-apply-probe` (entry alone `#Top`=0, entry+lemma `#Top`=1).

And, separately, **full sort correctness was proven** (`sort-probe`): insertion sort is a *sorted
permutation*. Ordering is a local adjacent-pair property (clean induction); permutation is a global
multiset-counting property (the hard half) — proven by making `count` peel the cons unconditionally
with `#if` (never deciding the witness), threading the witness `Y` through the driver, and using
`ensures ?A2 : sorted(?A2) andBool count(Y, ?A2) == count(Y, L)`. This makes the six trusted-sort
proofs proof-backed rather than assumed. The episode also produced the `ensures` convention: `ensures
P(result)` is the K postcondition slot for **properties/relations** (especially existential `?X`
outputs you don't compute), versus `result = summary` for closed-form answers.

### Case study — floats

The Haskell backend has **no float hooks at all** — even a *ground* `FLOAT.sub` errors — so no
native float op survives to the prover. Yet float problems are provable two ways. For the mapping/
folding problems (`rescale_to_unit`(21), `mean_absolute_deviation`(4)), wrap every float op as an
opaque trusted primitive (`subF`/`divF`, concrete K `Float` for a real `krun`, opaque in `kprove`),
verify only the *structure* with an accumulator-threaded summary; the lone unavoidable ground float
(`-1.0` in `find_zero`) is emitted as a literal, never computed. For the bisection `while`-loops of
`find_zero`(32), the `float-while-guard` probe overturned an assumption: kprove **case-splits any
Bool** (guard true → body / false → exit) *regardless* of float decidability, so the coinductive
circularity discharges partial correctness. (A separate set of ~10 float problems merged from a
collaborator use a **dyadic scaled-integer model** — a float `v` represented as `flt(v · 2^62)` —
scoped to the exact-representable domain `< 2^53`, e.g. `rounded_avg`(103), `truncate_number`(2).)

### Case study — the last blocker, `bf`(148)

`bf` maps two symbolic planet-name strings to orbit indices via two 8-way `if/elif` chains, then
slices the fixed planet tuple strictly between them — an 81-branch case-split whose invalid branch
must conclude `idxOf(P) => -1` when `P` equals none of eight symbolic strings. The `bf-probe`
isolated two bugs: (1) **`=/=K` does not normalize to `notBool(==K)`** — the solver won't discharge
the 8-way `=/=K` conjunction against `P ==K "Mercury" = false` atoms, so the fallback must be written
with `notBool(P ==K name)`; and (2) a **`#if`-cascade `idxOf` survives uncollapsed** when buried
inside another guard, so `idxOf` must be **rule-based** (8 positive `requires P ==K name` rules + the
`notBool` conjunction fallback) firing to a *bare Int* per branch. Both properties are load-bearing;
together they closed the full 81-branch spec (`--depth 30000`, ~25 min) → 164/164.

---

## 11. Workflow, scale, and the convergence-to-canonical phase

**Autonomous loop.** Much of the middle was run as a self-paced `/loop`: each iteration reads a
human-only kill switch `.agent-continue` (the agent never writes it), picks the next provable
problem, runs the full gate suite, commits one problem per commit, and `git push`es the isolated
`yuqing/pass-0` branch. Heavy proofs run in the background and re-notify on completion. A problem
counts as *done* only if its folder has `spec.k` + a `PROOF.md` showing `#Top`.

**Parallel batches with a trust-but-verify gate.** Template-close problems (each a small delta on a
proven sibling) were proven by a fan-out Workflow — one agent per problem, each writing only its own
folder and *not* committing, handed the closest sibling plus the soundness-critical op-rules verbatim
(so it cannot invent `modInt`/short-circuit `BoolOp`). Agents are trusted only after the main loop
**independently re-verifies** each: fresh `kompile` + `kprove` = `#Top`, non-vacuity fails, *and* a
human-style read confirms the semantics is minimal + sound and the spec carries the strong
postcondition. `kprove #Top` alone does not catch an unsound-but-passing semantics — the soundness
read is the part that does.

**The capability roadmap.** All 164 were categorized up front (a 16-agent workflow, judged against
the *real-proof* `below_zero` rubric, cross-checked by an adversarial critic) into
easy/medium/hard/blocked buckets with prerequisite features and a spec sketch — which sequenced the
whole effort and revealed that many "blocked" problems had integer-restriction or partial-correctness
escapes.

**Convergence to canonical (the "pass-0" phase).** Reaching 164/164 initially used
behaviour-preserving *rewrites* where a construct was unsupported. A final phase rebuilds each proof
on the unified `src/` semantics with the standing goal **`solution == canonical`**: the reference was
grown with the missing constructs (builtin-call family; list comprehensions → nested `for` + multi-`if`;
`GeneratorExp` with `all`/`any`/`sum`-of-bools aggregators) so the dataset's own code runs verbatim,
and each proof is reconverted following a fixed recipe (`pass-0-conversion-procedure`): solution ==
canonical (or an honest note if impossible, e.g. comprehensions before they were implemented); smoke =
*all* HumanEval `check` cases with bare-bool asserts (`assert x` / `assert not x`); one summary, no
redundant property; the `ensures ?R == summary` postcondition form (which also works on the loop
invariant, disproving an earlier assumption); terse `.k` comments (rationale lives in the `.md` docs);
and a full re-run of every gate. `CANONICAL-GAPS.md` measures the residual drift — the deliberately
rewritten-around features (`.append` list-mutation, method dispatch, `lambda`) that stay
per-problem rewrites until there is a reason to model a mutable-object layer.

---

## 12. Lessons (condensed)

- **`#Top` is only as trustworthy as the claim setup.** The reliability gaps (proof-domain bridge,
  narrowed domain, untested axioms, overridden rules) are invisible to `kprove` — the differential
  test, the non-vacuity check, and the human soundness read are what make `#Top` mean something.
- **Model, don't guard.** Reachable-wrong is a bug; stuck is fine. A correct-by-construction model
  (scope-chain closures, algebraic cons-lists, partial index/`chr`) beats leaf-cutting guards.
- **Never trust an "it's impossible."** Every wall in this project that was declared impossible from
  intuition turned out to be a formulation bug — a non-total summary, a stray `...`, a dropped
  `[total]` attribute. Build a one-variable probe and read the `.out` line by line.
- **Total-ness is the SMT currency.** Whether a summary is `[total]` decides whether Z3 will abstract
  it; closed-form / `[total]` / threaded-accumulator are the three ways to keep the arithmetic
  closing.
- **Trust honestly and minimally.** Genuine domain knowledge (sort, hash, eval, floats) is reduced to
  a few irreducible, meaningful `[simplification]` lemmas, flagged as klean-bound — never smuggled in
  as a silently-wrong summary.
- **Cap every `kprove`.** An unbounded `kore-exec` can take the machine down; `MemorySwapMax=0` +
  a memory cap + a timeout make a runaway die in its own cgroup, and a cap hit is a signal, not a
  refutation.

---

## Appendix: completion order and structure

The 164 proofs, in git-completion order with the technique for each, are listed in
[`../PROVEN.md`](../PROVEN.md). The per-problem layout is `semantics.k` (module `<NAME>`, shared by
`krun` and `kprove`) / `verification.k` (module `<NAME>-VERIFICATION`, the summary lemmas — `kompile`
this) / `spec.k` (module `<NAME>-SPEC`, the claims — `kprove` this), plus `solution.py`/`.mpy`,
`smoke.py`/`.mpy`, `canonical.py`, `README.md`, `PROOF.md`. The golden reference is
[`../questions/3-below-zero/`](../questions/3-below-zero/); the smallest worked proof is
[`tests/verification/loop-break/`](tests/verification/loop-break/).
