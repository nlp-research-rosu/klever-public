# Independent adversarial review: 10-make-palindrome

This audit used the supplied-semantics route. I treated every artifact under
`/candidate` as untrusted, copied the sources into
`/tmp/audit-work/palindrome-audit`, and rebuilt all executable definitions there.
No candidate-built definition or cache was used. K was available as version
v7.1.337; the exact version records are
[toolchain-kompile-version.log](/audit-output/evidence/toolchain-kompile-version.log)
and [toolchain-kprove-version.log](/audit-output/evidence/toolchain-kprove-version.log).

The candidate is **not a legitimate proof of the real generated program**.
Although both submitted claims reconstruct to `#Top` and the loop postcondition
is result-constraining, no claim loads `solution.mpy` or calls
`make_palindrome`. The main claim starts at an assumed internal loop state after
module loading, function lookup, argument binding, `i = 0`, `len`, and `range`.
In addition, the proof depends on a globally over-broad helper-call rewrite that
skips fixed call/frame execution while omitting all state cells. A concrete
legal-string witness shows that this rewrite can prove false preservation of
the scopes cell.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` exists as required for
`SUPPLIED_SEMANTICS`. There is no infrastructure breach.

The recursive inventory and comparisons are recorded in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log), produced by
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh).

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `60e80406...70913`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485ea...db16`).
- `/candidate/reference-semantics/` is recursively identical to the trusted
  tree: no missing, additional, changed, mistyped, or symlinked entry was found.
- No candidate artifact is a symlink.
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`, and the
  concrete-test sources are regular files.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log` are
  all missing. No structured generation trace is present. Thus there were no
  provenance reports to corroborate, but their absence is not confused with a
  tool or mount failure.

The complete line-numbered source capture is
[source-artifacts.log](/audit-output/evidence/source-artifacts.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `make_palindrome(string)` to return the shortest
palindrome beginning with `string`. Equivalently, find the earliest suffix start
whose suffix is palindromic, then append the reverse of the prefix preceding
that suffix. The documented results are `""`, `"catac"` for `"cat"`, and
`"catac"` for `"cata"`.

The trusted canonical implementation handles the empty string separately, then
increments a suffix start until it finds a palindromic suffix. The candidate
uses `for i in range(len(string))`, returns at the same first palindromic
suffix, and falls through to `return string`. The fall-through is correct for
the empty input; for every nonempty string, the one-character final suffix is
palindromic, so a return occurs inside the loop. This is a different control
shape but the same algorithm over the intended `str` domain.

The trusted translator regenerated the submitted MPy exactly:

- translator exit: 0;
- byte comparison exit: 0;
- both files have SHA-256
  `35c4f27b1777a537986a86a6fa03ff7363983cba78eeac0e26452dfec9b8af5b`.

Commands and results are in
[stage2-regeneration.log](/audit-output/evidence/stage2-regeneration.log).

The independent differential script
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical module and the scratch copy of the candidate. It also uses a
third, direct suffix-search oracle and checks that every result begins with the
input and is a palindrome. Its preserved input set is
[differential-inputs.json](/audit-output/evidence/differential-inputs.json):
documented examples; empty, single-character, palindrome, and non-palindrome
boundaries; Unicode and control-character cases; every string over `abc` of
length 0 through 7; and 2,000 seeded strings of length 0 through 40.

The run covered 5,307 category entries, 5,198 unique inputs, and observed first
palindromic-suffix starts 0 through 39. There were zero mismatches
([stage2-differential.log](/audit-output/evidence/stage2-differential.log)).
This is finite implementation evidence, not a substitute for a K reachability
proof.

## 3. Clean proof reconstruction

The scratch source copy initially contained no compiled definition. I built
both concrete and proof definitions from source.

| Operation | Evidence | Exit/result |
|---|---|---|
| LLVM build of trusted supplied semantics, module `MPY-KRUN` | [stage3-kompile-runtime.log](/audit-output/evidence/stage3-kompile-runtime.log) | 0 |
| Concrete execution of the six submitted assertions | [stage3-krun-concrete-tests.log](/audit-output/evidence/stage3-krun-concrete-tests.log) | 0, final `.K`, `NoExc`, exit code 0 |
| Haskell build of `verification.k`, module `VERIFICATION` | [stage3-kompile-verification.log](/audit-output/evidence/stage3-kompile-verification.log) | 0 |
| Helper claim alone | [stage3-kprove-helper.log](/audit-output/evidence/stage3-kprove-helper.log) | 0, `#Top` |
| Loop claim alone | [stage3-kprove-loop.log](/audit-output/evidence/stage3-kprove-loop.log) | 0, `#Top` |
| Original two-claim `SPEC` | [stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log) | 0, `#Top` |

The isolated positive specs are preserved as
[stage3-spec-helper-only.k](/audit-output/evidence/stage3-spec-helper-only.k)
and [stage3-spec-loop-only.k](/audit-output/evidence/stage3-spec-loop-only.k).
The compiler warnings concern unused variables and non-exhaustive trusted
functions outside the used path; they did not turn any command into a failure.

Thus the candidate's reported kind of verification result is reproducible.
`#Top` here establishes closure only under the supplied definition plus the
rules in `verification.k`; stages 4 and 5 show why that is not a whole-program
correctness proof.

## 4. Adequacy and real-program pinning

### Submitted claims in plain language

The helper claim at `/candidate/spec.k:8` assumes execution is already inside a
helper frame. The local frame contains `string = str(S)`, the continuation is
exactly `#endcall`, a caller frame is already on the stack, and
`L0 > 0` with `L0` absent from the remainder of the scopes map. It claims that
executing the literal `Return(string == string[::-1])` returns
`palindromeIS(S)`, pops the frame, and restores the caller.

The loop claim at `/candidate/spec.k:30` assumes execution is already at
`#loop(rangeObj(I, isLen(S), 1), ...)`, followed by the final
`Return(Name("string"))` and `#endcall`. It assumes a fully fabricated local,
module, and builtin scope; a caller frame already on the stack; and
`0 <= I <= isLen(S)` and `L > 0`. It claims the returned value is exactly
`str(palindromeFrom(S,I))` and that the function frame is popped.

Both postconditions are equalities to explicit summaries. Neither is a free
result variable, tautology, or one-way implication. The fresh false mutation in
stage 6 confirms that this fragment-level result is constrained.

### Satisfiable witnesses and substitutions

[stage4-witnesses.log](/audit-output/evidence/stage4-witnesses.log) gives ground
states satisfying each precondition:

- helper: `S = [99,97,116]` (`"cat"`), `L0 = 1`, `CALLER0 = 0`,
  empty `REST0`, stack tail, and heap;
- loop: the same `S`, `I = 0`, `L = 1`, `J = 0`, `CALLER = 0`, and empty
  stack tail/heap;
- loop boundary: `S = .IntSeq`, `I = 0 = isLen(S)`, `L = 1`.

For `"cat"`, `palindromeIS` is false in the claim, canonical Python, and
candidate Python. `palindromeFrom("cat",0)`, canonical Python, and candidate
Python all produce `"catac"`. At the empty boundary, all three produce `""`.

### Material pinning failure

No `<k>` cell in `spec.k` contains `Module(...)`, `#loadAll`, the submitted
`solution.mpy`, `Call(Name("make_palindrome"), ...)`, or
`#applyK(toCall(makePalindromeClosure), ...)`. The exact
`makePalindromeClosure` term appears only as a value assumed in the module
scope. The main claim never invokes that value.

Consequently, the proof does not establish:

1. loading the two definitions from `solution.mpy`;
2. resolving the entry-point binding;
3. evaluating and binding the actual argument;
4. entering the candidate function;
5. executing `i = 0`;
6. looking up and evaluating `len` and `range`; or
7. reaching the claimed `#loop` state from that execution.

The loop body is the actual submitted AST fragment and matches real control
flow once that internal state is assumed. That is not enough: the decision
boundary explicitly rejects a proof of a substituted or assumed fragment in
place of the real generated program. This is independently sufficient for
`FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and used semantics

[rule-inventory.txt](/audit-output/evidence/rule-inventory.txt), generated by
[build_rule_inventory.py](/audit-output/evidence/build_rule_inventory.py),
lists every configuration, syntax declaration, context, and rule once with
source file, line, attributes, and source hash. It contains 944 items across
the assembled semantics, all 23 helper K files, and `verification.k`:

- 1 configuration and 5 contexts;
- 77 ordinary syntax declarations;
- 43 function declarations;
- 82 `function,total` declarations;
- 25 symbol declarations, 22 of them `no-evaluators`;
- 4 macro declarations;
- 707 rules, including all 56 priority-bearing, 29 `owise`, and
  54 concrete-bearing rules.

There are no local `[simplification]` or `[functional]` declarations. The 928
items from the supplied semantics are byte-for-byte the trusted selected
semantics. They are therefore accepted as the fixed semantics level, not as
candidate proof extensions. The used-path audit maps every submitted AST
construct to its declarations and operational rules in
[used-construct-map.md](/audit-output/evidence/used-construct-map.md). It covers
configuration and module loading, sequencing, definition creation, name lookup,
calls and left-to-right arguments, frame allocation/binding/pop, assignment,
`len`, `range`, iteration, target binding, `if`, slicing, integer negation,
string equality/concatenation, and return.

The 25 supplied opaque symbols concern float operations, sorting, and MD5.
None is reachable from `solution.mpy` or either submitted claim. The supplied
string-literal conversion is ASCII-only (`semantics/str.k:13-17`), whereas the
natural prompt does not restrict Python strings. The claims instead quantify
directly over arbitrary `IntSeq`; this is a language/entry bridge limitation,
not an opaque oracle used to close the submitted claims.

### All 16 proof-local items in `verification.k`

| Lines | Item and decision |
|---|---|
| 9, 11-14 | `prefixIS` and its two equations. Definitional summary. The guards are disjoint; recursion descends for positive `N`. It gives the first `N` elements on all uses where `N <= isLen(S)`. No false overlap or oracle. |
| 16-17 | `palindromeIS(S) = (S ==K revIS(S))`. Definitional summary using the supplied, recursively defined `revIS`; it exactly models the helper's string equality. |
| 21-35 | `makePalindromeClosure`. A truthful syntactic constant: its body is byte-for-byte the submitted entry closure. It pins an assumed scope value but does not prove that the program was loaded or the closure called. |
| 40-48 | `palindromeFrom` and its three equations. Definitional summary. On the claimed domain `I >= 0`, the guards partition `I < len` into palindrome/non-palindrome and terminate by incrementing `I`; `I >= len` returns `S`. This describes first-suffix scanning. |
| 53-56 | Suffix-slice operational bridge. For `0 <= I <= len`, `S[I:]` agrees with supplied `dropIS(S,I)`. It is value-only and the displaced fixed rules do not touch other cells. No counterexample was found. The candidate nevertheless supplies no bridge-free universal connection theorem over the full arbitrary continuation represented by `...`; this is an evidence gap, not an unsoundness finding. |
| 58-61 | Prefix-slice operational bridge. The same assessment applies to `S[:I] = prefixIS(S,I)` under its in-bounds guard. |
| 63-65 | Reverse-slice operational bridge. Fixed `slStart/slStop/buildIS` at step `-1` agrees with supplied `revIS`. Again, no false witness was found, but no candidate connection theorem is supplied. |
| 70-79 | Helper-call operational bridge. **Unsound over its declared match domain.** It replaces `#applyK` with a Boolean while omitting `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, and every other state cell, and accepts an arbitrary continuation. The narrower helper-body claim begins after call setup and only with a fresh, fully constrained frame; it is not a universal connection theorem for this rule. The concrete false conclusion witness is detailed below. |
| 84-85 | Symbolic finite-map deletion identity. With `L` absent from `REST`, deleting the explicit `L |-> Scope` entry yields `REST`. The guard excludes overlap; this is ordinary finite-map mathematics and introduces no result oracle. |

The four priority-40 proof rules preempt the generic supplied slice/call rules.
The summary functions are not opaque: their equations fix their values. The
helper bridge's value is also defined, so the defect is not an unconstrained
Boolean oracle; it is skipped and falsely preserved operational state.

### Required false-conclusion witness for the unsound helper bridge

The witness uses the documented intended-domain string `"cat"` and the exact
submitted helper closure. Its configuration has `env = 0`, a module scope at
location 0 containing `"sentinel" |-> 42`, the builtin scope at -1,
`scopeLoc = 0`, and empty stack/heap. The proof-local rule matches because it
mentions only `<k>`.

- With `VERIFICATION`, the bridge proves `false` while preserving the sentinel
  scope: exit 0 and `#Top`
  ([stage5-helper-bridge-collision.k](/audit-output/evidence/stage5-helper-bridge-collision.k),
  [stage5-helper-bridge-collision.log](/audit-output/evidence/stage5-helper-bridge-collision.log)).
- With bridge-free fixed semantics, the real call allocates at location 0,
  overwrites that scope, executes the helper, and deletes the callee scope on
  pop. It returns the same Boolean but the remaining scopes contain only the
  builtin scope. The unchanged-state reachability claim exits 1 with
  `WarnStuckClaimState`
  ([stage5-helper-fixed-collision.k](/audit-output/evidence/stage5-helper-fixed-collision.k),
  [stage5-helper-fixed-collision.log](/audit-output/evidence/stage5-helper-fixed-collision.log)).

This is a concrete false scopes-cell conclusion enabled by the rule. The fact
that the submitted loop claim happens to assume a fresh allocator does not make
a globally false, unguarded semantic rule valid.

The successful loop proof materially depends on the bridge. I rebuilt a
definition with only that rule removed
([stage5-verification-no-helper.k](/audit-output/evidence/stage5-verification-no-helper.k)).
The definition builds, but the loop proof exits 1 at the real helper call/frame
setup with a stuck `#bindP`/body state
([stage5-kprove-no-helper.log](/audit-output/evidence/stage5-kprove-no-helper.log)).
This is proof-dependency evidence, not merely a timeout.

## 6. Fresh non-vacuity test

The fresh mutation changes the loop destination from
`str(palindromeFrom(S,I))` to
`str(seqConcat(palindromeFrom(S,I), iCons(33,.IntSeq)))`, deliberately appending
`"!"`. The satisfying witness `S = .IntSeq`, `I = 0`, `L = 1` returns `""`,
not `"!"`.

The preserved mutation is
[stage6-spec-vacuity-fresh.k](/audit-output/evidence/stage6-spec-vacuity-fresh.k).
`kprove --dry-run` exits 0, proving that it parses and builds
([stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log)).
The actual proof exits 1 with `WarnStuckClaimState`; the residual explicitly
contains the unmet condition
`S =/= seqConcat(S, iCons(33,.IntSeq))`
([stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log)).

The fragment theorem is therefore non-vacuous and result-constraining. This
does not repair its missing entry proof or legitimize the unsound operational
bridge.

## 7. Proven versus assumed accounting

What the reconstructed `#Top` establishes is precisely:

1. conditional on an already-created helper frame with the submitted helper
   body and the proof extensions, the helper returns the sequence-palindrome
   Boolean and pops that frame; and
2. conditional on the exact assumed loop/scopes/stack state and
   `0 <= I <= len(S)`, the loop fragment returns
   `str(palindromeFrom(S,I))` and pops its already-existing function frame.

It does **not** establish partial correctness from execution of the submitted
MPy module or entry-point call.

Trust and assumption ledger:

- **K backend and supplied semantics:** trusted execution/proof engine plus the
  byte-identical mounted semantics. This is the mandated semantics boundary.
- **Supplied primitive mathematics:** unbounded integers, maps, lists, strings,
  and K equality. Acceptable as the selected semantics level.
- **Supplied opaque float/sort/MD5 symbols:** present but irrelevant to every
  submitted construct and claim.
- **`prefixIS`, `palindromeIS`, `palindromeFrom`, and the closure constant:**
  proof-local definitions with explicit equations; mathematically inspectable,
  not opaque. They characterize a result but do not connect the real entry call
  to the assumed loop state.
- **Three slice bridges:** result-bearing operational accelerations supported
  by source-level equation inspection and concrete executions, but without the
  required bridge-free universal connection claims. Their finite evidence does
  not itself prove universal equivalence.
- **Helper-call bridge:** illegitimate. It skips program-defined call/body/frame
  execution over a larger match domain than the helper claim justifies and has
  the concrete false state witness in stage 5.
- **Natural-language shortestness bridge:** the recursive summary chooses the
  first palindromic suffix, which informally yields the shortest appended
  prefix. The candidate contains no separate K theorem of minimality.
- **Python differential bridge:** 5,198 unique cases support equivalence of the
  candidate implementation, canonical implementation, and direct oracle only
  on those tested inputs. It cannot connect the K loop fragment to program
  entry, and it does not validate K's ASCII-only literal path for arbitrary
  Python Unicode strings.
- **Provenance:** the four named generation records and structured trace are
  absent, so there is no additional auditable generation history.

Gate A fails both real-program body/entry pinning and operational-bridge
soundness. Gate B's Python implementation-to-intent evidence is strong but
cannot compensate for the absent K entry theorem. Gate C retains the documented
provenance and universal-connection limitations. Fresh reconstruction and the
non-vacuity mutation therefore do not satisfy the decision boundary for a
legitimate proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
