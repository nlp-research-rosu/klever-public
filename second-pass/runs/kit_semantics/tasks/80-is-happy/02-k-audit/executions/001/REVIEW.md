# Independent adversarial review: 80-is-happy

The candidate contains a legitimate partial-correctness proof of the submitted
program. I rebuilt both definitions from source, independently reran the
positive claims, mechanically pinned the claim body to the trusted translation
of `solution.py`, reviewed every K source sentence, and made two proof-sensitive
mutations. No candidate-produced compiled definition, cache, `#Top`, trace, or
`PROOF.md` was trusted.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem and generation
condition. I used its `container_paths` rather than its host provenance paths.
There is no mode/mount contradiction: `/reference/reference-semantics` is
present.

I read and independently checked the launcher-owned campaign lock, `/run.json`,
`/task.json`, `/generation-result.json`, all seven specifically required
generation records (`invocation.json`, `metrics.json`, `runtime-metrics.json`,
`usage.json`, `codex-last.txt`, `codex-output.log`, and `prompt.txt`), and the
structured trace under `/generation-evidence/codex-trace/`. These generation
records were treated only as claims. The structured trace has 607 parseable
JSONL records. Its raw SHA-256 and pipeline tree SHA-256 agree with the
independently hashed launcher records.

The campaign block is JSON-identical to `/audit-campaign-lock.json`, and the
lock's independently computed SHA-256 matches the recorded value. Every
launcher-declared single-file hash matches mounted bytes. All required
launcher records are readable regular files or real directories. All required
candidate proof artifacts are readable regular files. There are no symlinks in
the candidate, reference, or generation trees.

The candidate prompt and translator are byte-identical to their trusted
mounted versions. A recursive entry-kind and byte comparison found the
candidate `reference-semantics/` identical to
`/reference/reference-semantics`: 25 entries, no missing or additional path,
no changed or mistyped entry, and no symlink. The independently reconstructed
pipeline tree hashes also match their applicable launcher records:

- candidate tree:
  `faf18aa5172dbb6027240d41b4fdbdcfd0ab5f16d8da2c7e6c4ac2946a14bb99`;
- supplied semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `68d84ab51c52e5ffd4b58ab7fa68c9ef60d77ac1b620482707f2cce1bfd8d09d`.

The reproducible checker, exact command, status, record enumeration, hashes,
and trace event counts are in
`evidence/stage1_integrity.py` and `evidence/stage1_integrity.log`. It exited
zero. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is: for a string `s`, return
true exactly when its length is at least three and the characters in every
contiguous width-three window are pairwise distinct. The trusted canonical
implementation first rejects lengths below three and then rejects a window if
any of its three pairwise character comparisons is equal.

`/candidate/solution.py:1-16` implements the same predicate in one pass. After
the first two characters, `previous2`, `previous1`, and `code` are the three
codes in the current window. Its condition is precisely the negation of their
pairwise distinctness. Once `happy` becomes false it is never reset, and the
return separately enforces length at least three. Python's `ord` is injective
on the one-character strings produced by string iteration, so comparing these
codes is equivalent to comparing the characters.

I copied source artifacts to `/tmp/audit-work/80-is-happy`, ran the trusted
translator there, and compared bytes:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both MPY files have SHA-256
`5a11c6466138f4d30f771591956641321ef2a9743b3110218c0b1b84a03a2dd2`;
the command exited zero. See `evidence/stage2_regeneration.log`.

The independent differential program in
`evidence/stage2_differential.py` imports the two Python entry points and also
computes the natural-language contract directly. It tested:

- all six documented examples;
- 21 empty, short, repeated-character, and branch-boundary cases;
- every string over `abc` of lengths zero through seven (3,280 cases);
- 2,503 seeded representative cases through length 80, including ASCII,
  accented, CJK, emoji, NUL, and maximum Unicode code points;
- code points 1 through 200, a length-12,000 case, and a length-1,000
  supplementary-plane case.

There were 5,717 unique inputs and zero disagreements among the candidate,
canonical, and direct contract oracle. The preserved corpus is
`evidence/stage2_cases.json` (SHA-256
`f85830f425b4a81b838bdc2ce64b8cdf009b9741fd89f216549bc84f38f8b802`);
the command and zero exit status are in
`evidence/stage2_differential.log`. These finite tests support program fidelity;
they are not treated as the proof.

## 3. Clean proof reconstruction

The scratch tree contains only copied source artifacts and reviewer-generated
files. I did not copy or consult a candidate-built definition or cache. The
installed tools are K v7.1.293 and Python 3.10.12; `kup` is absent, but the
independently installed `kompile`, `kprove`, and `krun` are functional
(`evidence/stage3_tool_versions.log`).

The exact fresh commands and outcomes were:

| Purpose | Command | Result |
|---|---|---|
| Concrete definition | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| Proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| All target claims | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | `#Top`, exit 0 |
| Independently focused helper claim | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant` | `#Top`, exit 0 |

The bounded complete logs are respectively
`evidence/stage3_llvm_kompile.log`,
`evidence/stage3_haskell_kompile.log`,
`evidence/stage3_kprove_all.log`, and
`evidence/stage3_kprove_loop.log`. The compiler emitted only unused-variable
warnings from fixed source and existential post-state variables. Filtering the
entry claim alone would remove its loop lemma from the specification, so the
decisive entry run is the full two-claim proof, not an artificially filtered
run.

I also translated and concretely ran the exact submitted function plus seven
boundary assertions using the fresh LLVM definition. `krun` exited zero. The
source, trusted-translation output, byte-identity check, and logs are
`evidence/stage4_concrete_witness.py`,
`evidence/stage4_concrete_witness.mpy`,
`evidence/stage4_concrete_witness_identity.log`,
`evidence/stage4_concrete_translate.log`, and
`evidence/stage4_concrete_krun.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

The `loop-invariant` claim at `/candidate/spec.k:6` assumes `I >= 2` and an
ordinary function frame containing the remaining string `IS`, prior codes
`P2/P1`, current accumulated Boolean `H`, and the real loop body. It says that
executing the remainder of the loop:

- changes `happy` to `H and scanHappy(IS,I,P2,P1)`;
- increments `i` by exactly the remaining length;
- terminates the loop while preserving the surrounding continuation.

The actual final values of the previous-character temporaries are existential,
which is a sound weakening. The entry continuation reads only `happy` and `i`.

The `is-happy` entry claim at `/candidate/spec.k:45` has no input restriction:
`IS` is an arbitrary finite `IntSeq`. Its pre-state contains a standard builtins
scope, an empty heap and stack, and an `is_happy` closure. It executes
`Call(Name("is_happy"), str(IS))` and constrains the returned Boolean by an
equality:

```text
R = (length(IS) >= 3) and scanHappy(IS, 0, -1, -1)
```

This is result-constraining, not a free result, implication, or tautology.
`scanHappy` ignores the two sentinel values during the first two iterations and
then requires exactly the three pairwise inequalities in each successive
width-three window. Consequently the postcondition is equivalent to the
trusted source contract on all strings.

### Mechanical program pin

The entry does not merely call a similarly named oracle. The script
`evidence/stage4_program_pinning.py` parses constructor terms from the
byte-regenerated `solution.mpy` and the claim closure. It confirms:

- the sole module binding is `is_happy`;
- `Params("s")` corresponds to `("s", .ParamNames)`;
- after only normalizing the syntax spelling of an empty `.Stmts`, both bodies
  have the same 289 constructor tokens;
- the fixed `FuncDef` rule at
  `/reference/reference-semantics/semantics/functions.k:14-16` stores those
  same parameters, body, and defining environment;
- the claim closure uses the matching defining environment 0.

The command exited zero; see `evidence/stage4_program_pinning.log`. Thus trusted
regeneration plus a constructor-level comparison pins the manually embedded
claim term to the real submitted MPY program.

The claim then uses the fixed call/frame rules, not a proof-local evaluator.
In particular, `/reference/reference-semantics/semantics/call.k:69-74` binds
the argument and enters that closure body. The helper claim embeds the actual
`For` body from `/candidate/solution.mpy`, including `ord`, the guard, all four
assignments, and their real order.

### Satisfying states and substitutions

The entry precondition is satisfied, for example, by each direct claim state
with `IS = .IntSeq`, `(97)`, `(97,98,99)`, or `(97,98,97)`. The loop precondition
is satisfied by `IS=(99)`, `I=2`, `P2=97`, `P1=98`, and `H=true`.

`evidence/stage4_claim_witnesses.py` independently evaluates the formal summary
and both Python implementations. The preserved log shows:

```text
""     -> false
"a"    -> false
"aa"   -> false
"abc"  -> true
"aba"  -> false
"abca" -> true
"abac" -> false
```

All three results agree, and the concrete loop witness yields true. The script
exited zero (`evidence/stage4_claim_witnesses.log`).

Finally, I changed the `Bool(true)` initializer inside the closure term actually
executed by the entry claim to `Bool(false)` while leaving its postcondition
unchanged. This is not an external-source-only mutation. The altered claim
failed with `WarnStuckClaimState`, a residual executed `false`, an unmet result
condition, and exit 1. The exact mutation and proof are
`evidence/stage4_body_mutation.diff`,
`evidence/audit-spec-body.k`, and
`evidence/stage4_body_sensitivity_kprove.log`. The theorem is sensitive to the
submitted function body.

## 5. Rule-by-rule static soundness review

I read all 2,333 lines of `semantics.k`, every supplied helper K file,
`verification.k`, and `spec.k`. The sentence parser in
`evidence/stage5_inventory.py` produced the exhaustive, source-hashed inventory
`evidence/stage5_rule_inventory.md`:

- 26 files and 934 K sentences;
- 228 syntax declarations, 698 rules, five contexts, one configuration, and
  two claims;
- 45 priority-bearing sentences;
- 111 `total` declarations;
- 22 `no-evaluators` opaque declarations;
- zero `functional` and zero `simplification` attributes;
- one proof-local declaration and all three proof-local equations.

Every inventory entry contains its complete source sentence, attributes,
location, and disposition. The dispositions cover all 934 entries exactly:
167 fixed declarations/configuration sentences, 97 fixed used and
semantically faithful sentences, 642 fixed sentences with no reachable match,
22 unused opaque declarations with no dependent claim, three proof-local exact
equations, one proof-local declaration, and two positive proof obligations.
The inventory SHA-256 is
`3e7e1d86e4801ccd9bc879cbaa93614628cd569b67226f3046322c8134bb82d6`;
the generating command exited zero in `evidence/stage5_inventory.log`.

### Used syntax and execution rules

The submitted MPY uses `Module`, `FuncDef`, `Params`, `Assign`, `For`, `If`,
`Return`, `Name`, `Str`, `Int`, `Bool`, `UnaryOp`, `BinOp`, `BoolOp`,
`Compare/CmpOp`, `Call`, and statement/expression sequences. Each maps to the
fixed declarations and the following reviewed operational route:

- `core.k` supplies the standard cells, module/statement sequencing, lexical
  lookup through local, global, and builtin scopes, and left-to-right argument
  evaluation.
- `functions.k` stores the exact closure, binds its parameter, handles return,
  restores the caller frame, and deallocates the plain local scope.
- `call.k` evaluates the callee before arguments, dispatches the resolved
  closure, and resolves `ord` through the builtin scope.
- `controls.k`, `tuple.k`, and `iter.k` evaluate normal assignments, choose the
  `If` branch, iterate through `#loop`, and bind each yielded character to
  `ch`.
- `str.k` makes each string iteration step yield the corresponding one-code
  string. `builtins.k` maps `ord` of that one-code string back to the code.
- `operators.k`, `int.k`, and `bool.k` implement the used unary minus, integer
  addition/comparisons, and Python short-circuit `and`/`or`.

Strictness, contexts, and explicit continuations give the same evaluation order
as the source. The loop updates `ch`, executes the body, and recurs; the body
has no `break`, exception, heap allocation, or early return. The final `Return`
therefore observes exactly the accumulated `i` and `happy`. Plain frames lack
the `"$cells"` marker, so the higher-priority cell-write and cell-read variants
cannot overlap this path. Other priority rules are either disjoint by
constructor/sort or structurally unreachable. The ordinary and priority rules
that can match have no unresolved overlap.

### Proof-local extension

`verification.k` adds no `<k>` rule, semantic shortcut, oracle, axiom, lemma,
priority rule, opaque symbol, or simplifier. It adds only:

```text
scanHappy(.IntSeq, ...) = true
scanHappy(C :: REST, I, _, P1) = scanHappy(REST, I+1, P1, C)       if I < 2
scanHappy(C :: REST, I, P2, P1) =
  C!=P1 and C!=P2 and P1!=P2 and scanHappy(REST,I+1,P1,C)          if I >= 2
```

The empty/cons cases are disjoint. On a cons, `I < 2` and `I >= 2` are disjoint
and exhaustive over `Int`. Each recursive call strictly shortens `REST`, so
the `[function,total]` declaration is justified. The equations are the exact
mathematical summary of the real loop and cannot bypass its execution:
`scanHappy` appears only in claim conditions and never matches the `<k>` cell.

The supplied tree contains 22 opaque `no-evaluators` symbols:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None
occurs in the program, either claim, `scanHappy`, an active side condition, or
a reachable redex. No theorem conclusion depends on an opaque result.
Likewise, rules for lists, dictionaries, sets, ranges, sorting, floats,
methods, comprehensions, imports, assertions, subscripting, and unrelated
builtins cannot match a constructor on this execution path.

The fixed string-literal converter is ASCII-only, but the entry theorem does
not construct its input from a K string literal: it quantifies directly over
`str(IS)` for every finite `IntSeq`. The only literal used by the function is
the ASCII empty string. Consequently this fixed-semantics limitation does not
narrow the source-contract string domain. The formal entry domain is actually
broader than Unicode code-point sequences because its integers are
unrestricted.

No inventoried rule can encode this task's answer, fabricate a used result, or
make a false conclusion about this program reachable. I therefore make no
unsound-rule allegation for which a false-conclusion witness would be required.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. In scratch I independently
changed only the entry's result-constraining postcondition to require the
negation of the proved predicate:

```text
R = not ((length(IS) >= 3) and scanHappy(IS,0,-1,-1))
```

This is meaningful and false for every correctly executed input; for the
concrete satisfying witness `IS=.IntSeq`, execution returns false while the
mutation requires true.

The mutation is preserved as `evidence/audit-spec-vacuity.k` with the exact
change in `evidence/stage6_false_mutation.diff`. A dry run compiled the mutated
specification successfully and exited zero
(`evidence/stage6_false_mutation_build.log`). The real proof run then executed
the unchanged closure, reached `<k> false ~> .K </k>` with
`IS = .IntSeq`, failed the destination implication with
`WarnStuckClaimState`, and exited 1
(`evidence/stage6_false_mutation_kprove.log`). This is the expected unmet
obligation, not a parser error, timeout, missing import, unrelated crash, or
unreachable mutation.

## 7. Proven versus assumed accounting

The successful all-claims reachability proof establishes this partial
correctness statement:

> For every finite `IntSeq IS`, executing the exact submitted `is_happy`
> closure from the stated normal MPY call configuration, if it reaches the
> return state, returns true exactly when `IS` has length at least three and
> every contiguous triple has three pairwise-distinct codes.

The loop claim establishes, for arbitrary remaining sequences and arbitrary
prior codes with `I >= 2`, that the real loop preserves the conjunction of the
old `happy` value and the pairwise-distinct predicate for every remaining
window, while increasing the index by the remaining length. This is an
unbounded structural result, not finite unrolling or fixed-size testing. The
benchmark asks for partial correctness, so a separate termination theorem is
not required.

The trust and evidence boundaries are:

1. **Supplied MPY semantics.** This is the benchmark-selected fixed semantics
   boundary. Its mounted source is recursively identical to the trusted
   reference. I nevertheless audited every source sentence and all active
   rules; no proof-specific rule was treated as trusted merely because it sits
   beside the supplied tree. This boundary is acceptable for
   `SUPPLIED_SEMANTICS`.
2. **K implementation and mathematical builtins.** `kompile`, the Haskell
   `kore-exec` prover, the LLVM runtime, and K's standard integer, Boolean,
   map/list, string, and SMT behavior are trusted toolchain primitives. This is
   the ordinary low-level proof-system boundary, not a task-answer assumption.
3. **Python-to-MPY translation and manual claim embedding.** The translator is
   a trusted input. Byte regeneration proves the submitted MPY is its output,
   and the independent constructor comparison proves the executed closure is
   that same binding and body. This bridge is mechanically evidenced rather
   than accepted from candidate prose.
4. **String representation.** MPY represents a Python string as its finite
   sequence of integer character codes; iteration yields singleton strings and
   `ord` returns that code. On Python's string domain, equality of these codes
   is equality of characters. This direct representation argument is
   acceptable and is supported—but not proved—by the Unicode differential
   cases.
5. **Contract formalization.** A simple structural induction on `scanHappy`
   shows that the first two elements add no window obligation and each later
   element adds exactly the three inequalities for the new contiguous triple.
   This is ordinary mathematics visible in three disjoint equations, not an
   empirical or opaque correctness bridge.
6. **Opaque imported symbols.** All 22 fixed opaque declarations are listed in
   the exhaustive inventory, but none is reachable or appears in a dependent
   claim. They contribute no assumption to this theorem.
7. **Tests and prose.** Differential testing, concrete `krun` assertions,
   generation traces, and candidate prose do not establish the theorem. The
   first two provide bounded evidence for the source/representation bridges;
   the last two were not used as proof evidence.

There is no materially narrowed HumanEval domain, substituted program,
unconstrained result, semantic answer rule, unused body, failed reconstruction,
or vacuity. The remaining boundaries are the normal supplied-semantics and K
toolchain trust boundaries, with no non-fatal theorem-specific adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
