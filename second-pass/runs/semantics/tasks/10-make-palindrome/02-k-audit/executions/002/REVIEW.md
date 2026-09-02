# Independent adversarial review: 10-make-palindrome

The candidate's Python implementation is consistent with the HumanEval
contract, its submitted K claims rebuild to `#Top`, and its loop claim is
non-vacuous. Those facts do not amount to the requested proof. There is no
entry claim for `make_palindrome`. The only main claim begins at an already
constructed `#loop`, after function lookup/call, parameter binding, `i = 0`,
`len`, `range`, and `For` elaboration have all been omitted.

The candidate places an exact copy of the full function closure in a module
scope map and calls that a pin. It is never executed or looked up by either
claim. In a fresh definition I changed that closure to `return "WRONG"`; the
unchanged loop claim still returned `#Top`. This is a fatal real-program
pinning failure, not a source-maintenance observation.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the supplied-semantics
boundary is internally consistent.

I read the launcher-owned audit input and campaign lock, the run/task/result
records, invocation and metrics records, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and all 397 JSONL records in the structured
trace. The absent `runtime-metrics.json` is permitted for
`legacy-selected-stage1`; I did not reconstruct it or count it as a defect.
The generation transcript's prior `#Top` statements were treated only as
untrusted historical claims.

Independent checks established:

- The `audit_campaign` object exactly equals `/audit-campaign-lock.json`, whose
  SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All 10 layout-required records are regular, readable files. Fifteen
  launcher-declared direct hashes and all seven hashes in
  `generation-result.json` match their mounted bytes.
- The candidate prompt and translator are byte-identical to their trusted
  mounts.
- The candidate and trusted semantics trees contain the same 24 relative
  regular files with identical bytes. There are no missing, additional,
  changed, mistyped, special, or symlinked entries. A reviewer-defined
  path-plus-content digest is
  `07af80d60236b96efdecb0e54e7d1ee708ca7e1e94c67320f7763cfba6d89216`
  for each tree.
- The candidate contains all required proof deliverables. Their adequacy is
  assessed below rather than inferred from their presence.
- `kompile` and `kprove` both report K v7.1.293, matching the campaign lock.

The reproducible checker and exact result are in the
[Stage 1 provenance evidence](/audit-output/evidence/01-provenance/commands.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `make_palindrome(string)` to return the shortest
palindrome beginning with `string`. The canonical implementation returns `""`
for the empty input, otherwise scans suffixes from the beginning until it finds
the longest palindromic suffix and appends the reverse of the preceding prefix.

The candidate uses an equivalent `for i in range(len(string))` algorithm. The
empty range falls through to `return string`; for nonempty strings the
single-character last suffix guarantees a return. No length bound or
finite-size restriction appears in the source contract.

Regenerating with the trusted translator produced byte identity:

```text
solution.mpy             35c4f27b1777a537986a86a6fa03ff7363983cba78eeac0e26452dfec9b8af5b
solution.regenerated.mpy 35c4f27b1777a537986a86a6fa03ff7363983cba78eeac0e26452dfec9b8af5b
translator exit 0; cmp exit 0
```

The independent differential script imports the trusted canonical entry point
and the candidate entry point. Its oracle enumerates prefix-preserving
palindrome completions by increasing appended length; it does not call either
implementation. It covered the three documented cases, explicit empty/first
iteration/interior/last-iteration branch boundaries, Unicode and control
characters, all strings over `abc` of lengths 0 through 8, and 500 seeded
strings of lengths 0 through 60. All 10,333 unique inputs matched the oracle
with zero divergence. See the
[script](/audit-output/evidence/02-program-fidelity/differential_test.py) and
[command log](/audit-output/evidence/02-program-fidelity/commands.log).

This supports program fidelity on the tested inputs. It is finite evidence, not
a replacement for a K proof.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/reconstruction`. The semantics
copy came from the trusted reference mount. I did not copy or use any candidate
kompiled definition or cache.

Fresh reconstruction gave:

- LLVM `MPY-KRUN` compilation: exit 0.
- Trusted retranslation of `concrete-tests.py`: exit 0 and byte-identical to
  the submitted `.mpy`.
- `krun` of the six submitted assertions: exit 0 with `.K`, `NoExc`, empty
  stack, and exit code 0.
- Haskell `VERIFICATION` compilation: exit 0.
- Combined `kprove spec.k`: exit 0 and `#Top`.
- The two unlabeled claims copied unchanged into separate modules: each
  independently exited 0 and printed `#Top`.

The compilers reported supplied-semantics non-exhaustiveness warnings for
unused functions such as `mapStrVS`, several float helpers, `joinCodes`, and
`valSeqAt`, plus unused-variable warnings. No such warned function is used by
`solution.mpy`; the warnings are included in the trust accounting below.

Exact commands, statuses, and bounded output are in the
[Stage 3 reconstruction log](/audit-output/evidence/03-reconstruction/commands.log).
The dynamic verification gate passes for the claims that were actually
submitted.

## 4. Adequacy and real-program pinning

### Submitted claims in plain language

The first claim assumes an already activated helper frame at location `L0 > 0`,
with `string` bound to `str(S)`, a caller frame on the stack, `noRet`, and a
fresh/disjoint frame key. It executes only the translated
`Return(string == string[::-1]) ~> #endcall`. It says this body returns
`palindromeIS(S)`, removes the helper scope, restores the caller environment
and scope location, and leaves heap/exception/exit state unchanged.

The second claim assumes an already activated `make_palindrome` frame and an
already evaluated iterator `rangeObj(I, isLen(S), 1)`, where
`0 <= I <= isLen(S)` and the frame location `L` is positive. It executes:

```text
#loop(rangeObj(I, isLen(S), 1), Name("i"), translated If body)
~> Return(Name("string")) ~> #endcall
```

It says that this loop tail returns `str(palindromeFrom(S, I))` and pops the
existing function frame.

Both preconditions are satisfiable. For the helper, take `L0 = 1`,
`CALLER0 = 0`, `S = "cat"`, a `REST0` containing only the module and builtins
scopes, `scopeLoc = 2`, and the displayed caller frame. For the loop, take
`L = 1`, `I = J = 0`, `CALLER = 0`, `S = "cat"`, `scopeLoc = 2`, empty
heap/tail stack, and the exact displayed scopes. A ground summary claim reduces
`palindromeFrom("cat", 0)` to `"catac"`; both Python implementations also
return `"catac"`.

### Mechanical comparisons and the fatal gap

The constructor-level checker confirms:

- the body literal in `makePalindromeClosure` is exactly the trusted
  translation's `make_palindrome` body, modulo explicit inert `.Stmts` units;
- the submitted `#loop` target, `If` body, and trailing return equal the
  corresponding translated `For` fragment; and
- the evaluated iterator corresponds to `range(len(string))`.

That comparison does not establish an entry theorem. The checker also confirms
that `makePalindromeClosure` occurs in no `<k>` cell. It is only a value in the
framed module-scope map. The main claim omits:

1. module execution or lookup of `make_palindrome`;
2. function application and argument binding;
3. `Assign(Name("i"), Int(0))`;
4. lookup/call of `len` and `range`; and
5. the operational `For`-to-`#loop` step.

This is not merely semantically inert normalization. These are material
operations and control effects of the submitted program.

The dead-binding mutation makes the distinction concrete. I replaced the
literal full body in `makePalindromeClosure` with
`Return(Str("WRONG"))`. A fresh Haskell build succeeded, and the unchanged
loop theorem still proved `#Top`. Conversely, changing the actually executed
loop success branch to return the unextended input caused exit 1 with a stuck
result equality. Thus the theorem is sensitive to its loop fragment but
insensitive to the full submitted function body it purports to pin.

The comparison script, mutated sources, commands, and residual are in the
[Stage 4 adequacy evidence](/audit-output/evidence/04-adequacy/commands.log).
Because no claim executes the actual entry function body, the candidate proves
a substituted tail configuration rather than the real generated program. This
alone is a decisive legitimacy failure.

## 5. Rule-by-rule static soundness review

The exhaustive machine inventory covers every declaration in the 24 supplied
K files, `verification.k`, and `spec.k`: 231 syntax declarations, 707 rule
declarations, five contexts, one configuration, and two claims. Each record
includes source span, attributes, normalized text, and a digest. See the
[complete 1,029-record inventory](/audit-output/evidence/05-static/rule-inventory.txt)
and its [generator](/audit-output/evidence/05-static/inventory_k.py).

### Material fixed-semantics path

The submitted term uses the following fixed rules:

| Program construct | Declaration and operational path |
|---|---|
| `Module`, statement lists | `MPY-SYNTAX`; `#loadAll` and statement sequencing in `core.k` |
| `FuncDef`, calls, parameters | closure creation in `functions.k`; callee/left-to-right argument routing in `call.k`; `#bindP`, frames, return and pop in `functions.k` |
| names and builtins | scope-chain `#look` and `builtinsScope` in `core.k` |
| `i = 0`, `If`, `For` | assignment/branch/loop rules in `controls.k`; target binding in `tuple.k` |
| `len`, `range` | `applyBuiltin`/`seqLen` in `builtins.k`; `rangeObj` iteration in `range.k` |
| unary minus, string `==` and `+` | dispatch in `operators.k`; integer minus in `int.k`; `str` equality/concatenation in `str.k` |
| three slice shapes | bound evaluation and `#slStep`/`doSlice`/`buildIS` in `subscript.k`, accelerated by candidate bridges |
| reverse/drop/length | `revIS`, `dropIS` in `methods.k`; `isLen` in `core.k` |

The configuration records computation, current environment, scopes and next
scope location, heap and next heap location, call stack, return state,
exception, and exit code. Fixed call/return rules allocate and remove a scope,
save/restore the caller and continuation, and preserve heap state for this
pure helper. Strictness and explicit contexts give the material expression
evaluation order.

### Every proof-local declaration and rule

There are four proof-local function declarations, no proof-local `total`,
`functional`, `simplification`, `concrete`, or opaque/no-evaluator
declarations, and four priority rules.

1. `prefixIS` rule for `N <= 0`: returning the empty sequence is the standard
   prefix definition and is true on its complete guard.
2. `prefixIS` constructor rule for `N > 0`: it preserves the head and descends
   on both sequence and `N`. It is partial for an empty sequence with positive
   `N`, but is not declared total and every proof use has `N <= isLen(S)`.
3. `palindromeIS(S) => S ==K revIS(S)`: a truthful definition of palindrome on
   the fixed `IntSeq` string model.
4. `makePalindromeClosure`: constructor-equal to the translated closure. It is
   a truthful definitional constant, but it is dead in the submitted claims.
5. First `palindromeFrom` equation: if `I` is in range and the suffix is a
   palindrome, it returns the input plus the reversed length-`I` prefix.
6. Second `palindromeFrom` equation: on the complementary in-range guard, it
   increments `I`.
7. Final `palindromeFrom` equation: at or beyond the length, it returns `S`.
   The three guards are disjoint and exhaustive; recursive calls increase `I`
   toward the base case. These equations truthfully define the scan summary.
   They do not themselves prove the human-facing theorem that the result is a
   shortest palindrome.
8. Suffix-slice priority bridge: under `0 <= I <= isLen(S)`, fixed
   `buildIS` with start `I`, stop `len`, step `1` equals `dropIS(S,I)`.
9. Prefix-slice priority bridge: under the same guard, fixed `buildIS` with
   start `0`, stop `I`, step `1` equals `prefixIS(S,I)`.
10. Reverse-slice priority bridge: fixed omitted bounds with step `-1` traverse
    from `len-1` to `0`, equal to `revIS(S)`.
11. Exact helper-application priority bridge: it replaces an already evaluated
    application of the exact helper closure and one `str(S)` argument with
    `palindromeIS(S)`.
12. Symbolic map-removal rule: the compiled fixed syntax identifies
    `_[_<-undef]` as the `MAP.remove` hook. Removing `L` from
    `(L |-> Scope) REST` yields `REST` when `L` is absent from `REST`; the rule
    is a valid finite-map identity.

The three slice bridges touch only `<k>` and preserve an arbitrary
continuation. Ground, bridge-free fixed-semantics claims for `"cat"[1:]`,
`"cat"[:2]`, and `"cat"[::-1]` all proved `#Top`. A bridge-free universal
audit attempt built correctly but stopped at the missing structural lemma
equating fixed `buildIS` with `dropIS`; the candidate supplies no such
universal connection theorem. This is an evidence gap, not a false-rule
witness.

The helper body's submitted claim gives meaningful symbolic evidence for its
value, but it starts after invocation and imports the module containing the
proposed helper bridge. It is not the required bridge-free universal theorem
from `#applyK` through allocation, binding, body execution, return, and pop.
Moreover, the bridge itself omits freshness and `noRet` guards. Those
conditions do hold on all uses in the submitted loop claim (`scopeLoc = L+1`,
scopes at `L,0,-1`, `L>0`, and `noRet`). Malformed arbitrary configurations
outside the intended entry-state domain can distinguish the bridge from fixed
execution, but I found no false conclusion witness on the intended valid
string-input domain. Accordingly I classify it as over-broad and lacking the
required formal connection evidence, not as a witnessed intended-domain
unsoundness.

The supplied semantics contains opaque/no-evaluator float, keyed-sort, and MD5
symbols and compiler-noted partial `total` declarations. They are unchanged
trusted-baseline components and none is reached by this program. The concrete
`strToCodes` rule supports ASCII literals only; the symbolic claims use
arbitrary `IntSeq`, so this limits concrete K/Unicode evidence but does not
restrict the formal loop variable to ASCII.

No proof-local rule encodes an unconstrained result oracle, and I found no
concrete or symbolic false conclusion enabled by a proof-local rule on a valid
state for an intended string input. The static failure is instead the absence
of the required operational connection theorems and, decisively, the absence
of an entry theorem.

## 6. Fresh non-vacuity test

I created a fresh mutation changing the loop postcondition from
`str(palindromeFrom(S,I))` to that value with character code 88 (`"X"`)
appended. The empty-string state with `S = .IntSeq`, `I = 0`, and `L = 1`
satisfies the original precondition, while the real result is empty and the
mutation demands `"X"`.

The mutated spec parsed and built. `kprove` exited 1 with
`WarnStuckClaimState`, an unexplored-branches warning following that failure,
and the expected unmet equality
`S = seqConcat(S, iCons(88, .IntSeq))` on the exhausted-loop branch. It was not
a parser error, timeout, import failure, or unrelated crash.

The mutation and bounded command log are in the
[Stage 6 non-vacuity evidence](/audit-output/evidence/06-non-vacuity/commands.log).
The submitted loop theorem is result-constraining and discriminating. Its
non-vacuity does not enlarge its scope to the missing program prefix.

## 7. Proven versus assumed accounting

What the successful reachability checks establish is precisely:

- from an already activated helper-body state satisfying its frame
  precondition, the translated helper body returns whether `S` equals its
  reverse; and
- from an already activated `make_palindrome` frame whose computation has
  already reached the specified range loop at symbolic position `I`, the loop
  tail returns the recursively defined `palindromeFrom(S,I)` under the supplied
  semantics plus candidate extension rules.

These are partial-correctness reachability results: they constrain terminating
outcomes from those formal start states. They do not establish that invoking
the submitted `make_palindrome` binding reaches the loop theorem's start state.

The trust and assumption ledger is:

- **K toolchain and logic:** K v7.1.293, its Haskell/LLVM backends, SMT
  reasoning, and builtin integer/map/list hooks are trusted.
- **Supplied semantics:** the byte-identical 24-file MPY semantics is the fixed
  operational model. Unused opaque float/sort/MD5 symbols and unused
  non-exhaustive functions remain outside this theorem's material path.
- **String model:** symbolic Python strings are modeled as finite `IntSeq`
  values; sequence equality, concatenation, reverse, length, slice, and range
  mathematics are trusted as reviewed above. Concrete non-ASCII literal
  coverage is not established by `krun`.
- **Proof-local equations:** `prefixIS`, `palindromeIS`,
  `palindromeFrom`, the literal closure, and map removal are accepted only with
  the guards and meanings listed in Stage 5.
- **Operational bridges:** the three slice accelerations and exact helper-call
  acceleration affect the returned value and proof closure. Ground evidence
  and direct mathematical review support their intended uses, but the
  candidate has no bridge-free universal connection theorems over their full
  match domains.
- **Translator bridge:** byte-identical trusted regeneration mechanically
  connects `solution.py` to `solution.mpy`.
- **Intent bridge:** the fact that the first palindromic suffix yields the
  shortest palindrome extension is an ordinary informal mathematical argument,
  not a separately stated K predicate/theorem.
- **Differential evidence:** 10,333 Python cases support implementation
  equivalence and the human contract only on those finite cases.

Gate accounting:

- Real-program soundness/adequacy: **fails**. The full entry body is dead
  environment data, not the executed claim term; changing it to a false body
  leaves `#Top`.
- Local result constraint/non-vacuity: **passes** for the loop-tail theorem.
- Intent adequacy for the requested proof: **fails** because the sound local
  lemma is not connected to invocation of the unrestricted entry point.
- Evidence auditability: the recorded tests and reconstructions are
  reproducible, but operational connection evidence is incomplete.

The benchmark decision boundary explicitly makes a substituted-program or
non-pinning proof illegitimate. Successful reconstruction and non-vacuity of a
strict suffix lemma cannot compensate for the missing entry theorem.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
