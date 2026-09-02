# Independent adversarial review: 111-histogram

This is a completed audit under `SUPPLIED_SEMANTICS`. I treated every
candidate artifact as untrusted, copied source-only inputs to
`/tmp/audit-work/reconstruction`, rebuilt both K definitions there, and did not
reuse any candidate cache or compiled definition.

The reconstructed K claims all close and the result mutation is properly
rejected. Nevertheless, the candidate does **not** prove the requested
all-input histogram contract. Five claims are concrete examples. The remaining
eight range only over synthetic `tokenText` values of length one through three;
there is no theorem connecting those values to real strings, and the proposed
connection is false over the claims' full formal domain. Thus the successful
proof is a bounded collection of execution facts, not a partial-correctness
proof of `histogram` over its intended input domain.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present as required by the rendered
`SUPPLIED_SEMANTICS` mode. The trusted mount therefore does not contradict the
mode, and this is a candidate audit rather than an infrastructure error.

The read-only integrity checker recursively compared entry names, entry types,
and SHA-256 file contents. Results:

- candidate symlinks: 0;
- candidate semantics entries: 25 (the helper directory plus files);
- missing, additional, mistyped, symlinked, or changed semantics entries: 0;
- candidate `prompt.py` is byte-identical to `/reference/prompt.py`,
  SHA-256
  `c30d14cdaa12a3c8fd5b0cf5ce64622c84276ea5f9709d0494b836617938da59`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`,
  SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The exact checks and status are in
[`stage1-provenance.log`](evidence/logs/stage1-provenance.log); all candidate
source hashes are in
[`stage1-candidate-manifest.log`](evidence/logs/stage1-candidate-manifest.log).
This comparison establishes only that the fixed semantics was not changed. It
does not bless the two candidate rules in `verification.k`.

### Missing provenance records

The following requested candidate records are absent:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`;
- any file identifiable as a structured trace (`*trace*`, `.jsonl`, or
  `.ndjson`).

There was consequently no generation record to corroborate. The candidate also
contained a Python `__pycache__`; I treated it as an untrusted generated cache
and did not copy or use it. No candidate-built K definition was present or
used. The missing records are a provenance-integrity limitation, but the
trusted mounts and live K toolchain were sufficient to complete the technical
audit.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and domain

The trusted prompt asks for a dictionary containing every lowercase letter
tied for the greatest frequency in a space-separated input, with the frequency
as its value; the empty input returns `{}`. On the strict documented domain I
used, the input language is:

```text
empty, or [a-z]( [a-z])*
```

The trusted canonical implementation uses `test.split(" ")`, counts each
nonempty token to find the maximum, then inserts every token having that count.
On the strict domain above, it implements the stated contract.

The submitted `solution.py` uses a standard two-pass implementation:

1. `test.split()` and an insertion-ordered `counts` dictionary compute each
   token frequency and the running maximum;
2. a second pass through `counts.keys()` emits exactly the keys whose count is
   the maximum.

Every new-key/existing-key branch, maximum-update/non-update branch, and
result-include/exclude branch is reachable on the strict domain.

### Translation identity

I regenerated the MiniPython AST from the submitted Python using the trusted
translator:

```bash
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
```

Both commands exited 0. Both files have SHA-256
`d324282bd904e34a1ef8f2d5c2f8622dbd9d0bed9ada7e28385e3fb92bc15ed9`.
See
[`stage2-regenerate-mpy.log`](evidence/logs/stage2-regenerate-mpy.log),
[`stage2-mpy-byte-compare.log`](evidence/logs/stage2-mpy-byte-compare.log), and
[`stage2-mpy-hashes.log`](evidence/logs/stage2-mpy-hashes.log).

### Independent differential execution

[`differential.py`](evidence/differential.py) independently imports the trusted
canonical entry point and the submitted generated entry point. It ran:

- all 5 documented examples;
- 13 explicit empty, single-token, branch-boundary, tie, and stress cases;
- every sequence of length 0 through 7 over `a`, `b`, and `c` (3,280 generated
  cases);
- 500 deterministic random sequences of length 0 through 50 over six letters,
  seed 111.

After deduplication, 3,757 strict-domain inputs were compared with zero
mismatches. The complete deterministic input set is
[`differential-inputs.json`](evidence/differential-inputs.json), and the command,
scope, results, and exit 0 are in
[`stage2-differential.log`](evidence/logs/stage2-differential.log).

Boundary probes outside the strict domain expose a real implementation-to-
canonical difference. For leading/trailing spaces, repeated internal spaces,
tabs, and newlines, Python's no-argument `split()` and the canonical
`split(" ")` differ. For example:

```text
input "a  b"
canonical -> {"a": 1, "": 1, "b": 1}
submitted -> {"a": 1, "b": 1}
```

This does not produce a strict-domain mismatch, but it means that a more
permissive reading of “space separated” is not proved or empirically aligned.
The differential run is finite evidence about program fidelity; it is not the
missing universal K theorem.

## 3. Clean proof reconstruction

The live tools were independently available:

```text
kompile: /usr/bin/kompile
kprove:  /usr/bin/kprove
K version v7.1.337, build 2026-06-18
```

### Fresh concrete definition

From the source-only scratch copy:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none
```

Both exited 0. Logs:
[`stage3-build-runtime.log`](evidence/logs/stage3-build-runtime.log) and
[`stage3-run-candidate-concrete.log`](evidence/logs/stage3-run-candidate-concrete.log).

I also translated and ran an auditor-authored K test containing empty, one-
token, repeated-token, distinct-token, maximum, non-maximum, and tie cases. It
exited 0; see
[`reviewer-concrete-tests.py`](evidence/reviewer-concrete-tests.py),
[`reviewer-concrete-tests.mpy`](evidence/reviewer-concrete-tests.mpy),
[`stage4-translate-reviewer-concrete.log`](evidence/logs/stage4-translate-reviewer-concrete.log),
and
[`stage4-run-reviewer-concrete.log`](evidence/logs/stage4-run-reviewer-concrete.log).

The LLVM compiler reported non-exhaustive `[total]` matches for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are fixed supplied
semantics declarations. None is on this submitted program's path: this program
does not use `map`, float operations, `join`, sorting, or list/tuple positional
indexing. Dictionary reads use `dGet`, not `valSeqAt`.

### Fresh proof definition and aggregate target

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module HISTOGRAM-SPEC
```

The build exited 0. The proof exited 0 and printed `#Top`. Logs:
[`stage3-build-proof.log`](evidence/logs/stage3-build-proof.log) and
[`stage3-prove-all.log`](evidence/logs/stage3-prove-all.log).

### Independent run of every positive claim

The candidate claims were unlabeled. I made the mechanical source-identical
copy [`spec-labeled.k`](evidence/spec-labeled.k), adding only labels `c01`
through `c13`, and ran each claim separately with:

```bash
kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module HISTOGRAM-SPEC \
  --claims HISTOGRAM-SPEC.cNN \
  --warnings none
```

Every one of the 13 runs exited 0 and printed `#Top`:

| Claim | Independent proof log |
|---|---|
| c01 | [`stage3-prove-c01-labelcheck.log`](evidence/logs/stage3-prove-c01-labelcheck.log) |
| c02 | [`stage3-prove-c02-corrected.log`](evidence/logs/stage3-prove-c02-corrected.log) |
| c03 | [`stage3-prove-c03-corrected.log`](evidence/logs/stage3-prove-c03-corrected.log) |
| c04 | [`stage3-prove-c04-corrected.log`](evidence/logs/stage3-prove-c04-corrected.log) |
| c05 | [`stage3-prove-c05-corrected.log`](evidence/logs/stage3-prove-c05-corrected.log) |
| c06 | [`stage3-prove-c06-corrected.log`](evidence/logs/stage3-prove-c06-corrected.log) |
| c07 | [`stage3-prove-c07-corrected.log`](evidence/logs/stage3-prove-c07-corrected.log) |
| c08 | [`stage3-prove-c08-corrected.log`](evidence/logs/stage3-prove-c08-corrected.log) |
| c09 | [`stage3-prove-c09-corrected.log`](evidence/logs/stage3-prove-c09-corrected.log) |
| c10 | [`stage3-prove-c10-corrected.log`](evidence/logs/stage3-prove-c10-corrected.log) |
| c11 | [`stage3-prove-c11-corrected.log`](evidence/logs/stage3-prove-c11-corrected.log) |
| c12 | [`stage3-prove-c12-corrected.log`](evidence/logs/stage3-prove-c12-corrected.log) |
| c13 | [`stage3-prove-c13-corrected.log`](evidence/logs/stage3-prove-c13-corrected.log) |

An initial attempt used a `label(...)` spelling that this installed K release
did not expose to `--claims`; those diagnostic runs exited 113 with “Unused
filtering labels” and are retained in the logs. They are not counted as target
proof failures. The corrected shorthand labels and module-qualified selectors
above are the positive runs.

## 4. Adequacy and real-program pinning

### Common entry state and result constraint

Every claim starts from a satisfiable ordinary initial configuration:

- `<env>` is module scope 0;
- scope 0 is empty and has the supplied builtins scope `-1` as parent;
- `<scopeLoc>` is 1;
- heap and stack are empty, and `<heapLoc>` is 0;
- return state is `noRet`, exception state is `NoExc`, and exit code is 0.

The destination requires the whole `<k>` computation to be consumed, restores
module environment 0 and scope location 1, empties the call stack, and retains
`noRet`, `NoExc`, and exit code 0. Final scopes, heap, and heap allocation
counter are existentially unconstrained.

There is no direct result cell in the destination. Instead,
`histogramCheck(INPUT, EXPECTED)` expands to the exact function body followed
by:

```text
Assert(histogram(INPUT) == EXPECTED)
```

Under the supplied `Assert` rules, a wrong result reaches `AssertionError` and
exit code 1, which cannot satisfy the claimed destination. The result is
therefore constrained indirectly but meaningfully; it is not a free
right-hand-side variable or tautology.

### Plain-language meaning of all entry claims

All claims share the state pre/postcondition above. Their input/result
obligations are:

| Claim | Additional precondition and required result |
|---|---|
| c01 | Real concrete input `""` must return `{}`. |
| c02 | Real concrete input `"a b c"` must return all three keys with count 1. |
| c03 | Real concrete input `"a b b a"` must return `a` and `b`, each with count 2. |
| c04 | Real concrete input `"a b c a b"` must return `a` and `b`, each with count 2. |
| c05 | Real concrete input `"b b b b a"` must return only `b: 4`. |
| c06 | For any unconstrained K `IntSeq` `A`, the **synthetic** value `str(tokenText([str(A)]))` must return the one key `str(A): 1`. |
| c07 | For any `A`, the synthetic two-element sequence `[A,A]` must return `A: 2`. |
| c08 | For synthetic `[A,B]` with structural `A != B`, return both with count 1. |
| c09 | For synthetic `[A,A,A]`, return `A: 3`. |
| c10 | For synthetic `[A,A,B]` with `A != B`, return `A: 2`. |
| c11 | For synthetic `[A,B,A]` with `A != B`, return `A: 2`. |
| c12 | For synthetic `[A,B,B]` with `A != B`, return `B: 2`. |
| c13 | For synthetic `[A,B,C]` with all three structurally distinct, return all three with count 1. |

Thus c06–c13 cover every equality partition only for lengths one, two, and
three. They do not quantify over arbitrary list length and are not a loop
invariant or induction theorem. The two longer documented inputs remain
individual concrete executions.

### Program identity

The `<k>` terms do not load `solution.mpy` from disk; they execute the
`FuncDef` duplicated in the macro. I therefore parsed both the submitted
`solution.mpy` and a ground macro application through the fresh proof
definition with macro expansion, then compared their first `FuncDef` JSON
subtrees.

Both normalized KAST subtrees have SHA-256
`6b1cc8ed1f8f170cec7cd74b521c8662a4a2874292ad5788a285d0b2dbe62e3d`
and are exactly equal. See
[`solution-expanded.json`](evidence/solution-expanded.json),
[`macro-expanded.json`](evidence/macro-expanded.json), and
[`stage4-compare-kast-clone.log`](evidence/logs/stage4-compare-kast-clone.log).
Together with translator byte identity, this pins the currently submitted
program AST rather than a substituted algorithm.

All function calls, both loops, dictionary updates, comparisons, and the return
execute through the supplied rules. There are no helper loop claims or summaries
that skip those bodies.

### Satisfying substitutions

[`claim_witnesses.py`](evidence/claim_witnesses.py) instantiates each symbolic
shape with concrete letters (`z`, `y`, and `x` as needed), and uses the listed
concrete inputs for c01–c05. Both Python implementations matched every expected
dictionary, 13/13; see
[`stage4-claim-witnesses.log`](evidence/logs/stage4-claim-witnesses.log).

These ground substitutions demonstrate satisfiable preconditions and correct
listed results. They do not supply the missing denotation theorem from
`tokenText` to real strings and do not extend the formal theorem past length
three.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k-inventory.tsv`](evidence/k-inventory.tsv) is a line-addressed inventory of
every local declaration and rule in the supplied assembled semantics and
helpers, `verification.k`, and `spec.k`. It contains 945 rows:

- 1 configuration;
- 229 syntax declarations;
- 697 rules;
- 5 explicit contexts;
- 13 target claims.

Attributes inventoried include 146 `[function]`, 107 `[total]`, 29 priority, 32
`[concrete]`, 26 `[owise]`, 22 `[no-evaluators]`, 25 `[symbol]`, 5 macro, 1
`macro-rec`, 1 constructor, 2 strict, and 1 seqstrict occurrence. There are no
local `[functional]` or `[simplification]` declarations/rules. The generation
summary and exit 0 are in
[`stage5-k-inventory.log`](evidence/logs/stage5-k-inventory.log).

For each supplied-semantics row, the inventory records that it is part of the
byte-identical selected fixed semantics; rules relevant to the submitted
program were then checked against the concrete Python behavior. The exact used
construct-to-rule mapping is
[`used-construct-map.md`](evidence/used-construct-map.md). Files and features
unrelated to this program—float arithmetic, mathematical imports, sorting,
hashing, comprehensions, range, set, tuple unpacking, slicing, and most
builtins—cannot contribute to these claim closures.

### Configuration, order, state, calls, and returns

The relevant fixed rules preserve the intended operational order:

- assignment evaluates the right-hand side before mutation;
- binary operands evaluate left-to-right;
- a call evaluates the callee then arguments left-to-right;
- `For` evaluates its iterable once and repeatedly binds one yielded value;
- `If` evaluates its guard before selecting exactly one branch;
- dictionary literals evaluate keys then values in insertion order;
- dictionary updates retain first insertion position and replace the parallel
  value;
- `split()` and `keys()` allocate list objects in `<heap>/<heapLoc>`;
- a function call allocates a scope, changes `<env>/<scopeLoc>/<stack>`, binds
  `test`, executes the actual body, and `Return` unwinds back to the caller;
- assertion failure changes both `<exc>` and `<exit-code>`.

For the intended string/int dictionary values, `==K` key identity, integer
arithmetic/comparisons, ordered keys, dictionary lookup/update, and dictionary
equality agree with the Python observations needed by this program. All
subscript reads are safe on the path: an existing-count read follows membership,
the maximum read follows an assignment, and result construction iterates known
keys.

No fixed opaque float, sort, or MD5 symbol reaches a branch, result, state cell,
or postcondition in these claims. The baseline totality warnings identified in
stage 3 are also off-path. I found no supplied-rule interaction on the used path
that fabricates the histogram answer or bypasses either loop.

### Candidate extension 1: `tokenText`

```k
syntax IntSeq ::= tokenText(ValSeq) [constructor]
```

This adds a new constructor to the internal string-code sort. It is not produced
by parsing a concrete `Str("...")`, and the supplied semantics has no mapping
from it to bytes/code points. Formal variables nested beneath it may contain
arbitrary integers, whitespace, another `tokenText`, or values with no Python
string denotation. It is therefore a synthetic proof-domain value, not a
declaration of a real input language.

### Candidate extension 2: synthetic split equation

```k
rule splitWS(tokenText(TS:ValSeq), .IntSeq, .ValSeq) => TS
```

This ordinary function equation has no guard, priority, totality, or
simplification attribute. It does not overlap the supplied `.IntSeq` or
`iCons(...)` equations, so I do **not** label it internally inconsistent or
globally false in the extended algebra. Its narrower defect is that it directly
chooses the program-visible split result of a novel input without a bridge-free
connection theorem to the real `splitWS` computation. That result controls both
loops, every branch, and the asserted return dictionary.

The dependency is machine-visible:

- after removing `tokenText` entirely, all five real concrete claims still
  prove with `#Top`; see
  [`verification-ground.k`](evidence/verification-ground.k),
  [`spec-ground.k`](evidence/spec-ground.k), and
  [`stage5-prove-ground-without-tokenText.log`](evidence/logs/stage5-prove-ground-without-tokenText.log);
- retaining the constructor but removing only the split equation makes c06
  fail at
  `splitWS(tokenText(...), .IntSeq, .ValSeq)`, before the first loop can
  iterate; see
  [`verification-no-split.k`](evidence/verification-no-split.k),
  [`spec-no-split.k`](evidence/spec-no-split.k), and
  [`stage5-prove-symbolic-without-split.log`](evidence/logs/stage5-prove-symbolic-without-split.log).

There is also a concrete false-denotation witness. c06 has no restriction on
`A`. Instantiate `A` with code points `[97,32,98]`, the concrete text `"a b"`.
The candidate extension treats `str(A)` as one pre-split token, and K proves
the synthetic result `{"a b": 1}` with `#Top`. Both actual Python
implementations on the real text `"a b"` return `{"a": 1, "b": 1}`. Artifacts:
[`spec-synthetic-whitespace-witness.k`](evidence/spec-synthetic-whitespace-witness.k),
[`synthetic_bridge_witness.py`](evidence/synthetic_bridge_witness.py),
[`stage5-prove-synthetic-whitespace-witness.log`](evidence/logs/stage5-prove-synthetic-whitespace-witness.log),
and
[`stage5-compare-synthetic-denotation.log`](evidence/logs/stage5-compare-synthetic-denotation.log).

This witness does not show that the equation contradicts itself on the novel
constructor. It shows that the candidate's prose interpretation—“a one-token
input” for every `A:IntSeq`—cannot serve as a universal connection to a real
string. Even if `A`, `B`, and `C` were guarded to single lowercase characters,
the claims would still cover only sequence lengths at most three.

### Candidate extensions 3 and 4: `histogramCheck`

```k
syntax Module ::= histogramCheck(Expr, Expr) [macro]
rule histogramCheck(INPUT, EXPECTED) => Module(exact FuncDef ... Assert(...))
```

The syntax declaration and macro rule are compile-time wrappers. The embedded
function is independently AST-identical to `solution.mpy`. The added assertion
does not supply a return value or rewrite the function call; it observes the
real returned dictionary and fails on inequality. This is a legitimate
postcondition harness for the inputs it actually states.

### Static soundness conclusion

The four candidate declarations/rules include no priority rule, simplification,
total function, opaque evaluator, or task-answer equation. The macro wrapper is
sound and body-sensitive. The synthetic split rule is consistent as a
definition of a new algebraic input but is unconnected to concrete string
execution and cannot justify the symbolic claims as claims about real inputs.
No other local rule repairs that missing bridge, and no claim supplies an
arbitrary-length invariant.

## 6. Fresh non-vacuity test

I created [`spec-vacuity.k`](evidence/spec-vacuity.k), a fresh mutation of the
real single-token obligation:

```text
input:            "a"
real result:      {"a": 1}
mutated expected: {"a": 2}
```

The Python witness confirmed the mutation is false; see
[`stage6-false-witness-python-corrected.log`](evidence/logs/stage6-false-witness-python-corrected.log).

The mutation parsed and compiled successfully:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  --warnings none
```

Exit: 0. Evidence:
[`stage6-vacuity-dry-run.log`](evidence/logs/stage6-vacuity-dry-run.log).

The live proof command then exited 1:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --warnings none
```

The residual is the expected reachable final configuration with `.K`,
`AssertionError`, and exit code 1; it cannot unify with the destination's
`NoExc` and exit code 0. This is a meaningful unmet result obligation, not a
parse error, timeout, missing import, or unrelated crash. Full bounded output:
[`stage6-vacuity-proof.log`](evidence/logs/stage6-vacuity-proof.log).

Non-vacuity therefore passes. It confirms that each listed expected dictionary
matters; it does not enlarge the listed input set.

## 7. Proven versus assumed accounting and verdict

### What the successful reachability proof actually establishes

Under K v7.1.337 and the supplied fixed semantics, the AST-identical submitted
function terminates without assertion failure for:

1. the five concrete strings in c01–c05, with exactly the stated dictionaries;
2. eight bounded synthetic pre-split value patterns covering all equality
   partitions of lengths one, two, and three.

The K proof genuinely executes the counting loop, maximum update, result loop,
function return, dictionary equality, and assertion for those configurations.
The positive `#Top` results and the negative mutation jointly support that
narrow statement.

It does **not** establish:

- the histogram contract for every valid space-separated lowercase-letter
  string;
- any induction or loop invariant for arbitrary token-list length;
- any connection between `tokenText(TS)` and the code sequence of a concrete
  real string whose `split()` result is `TS`;
- canonical agreement on malformed, repeated-whitespace, tab, newline, or
  leading/trailing-whitespace inputs.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K compiler, Haskell prover, LLVM runtime, and builtin Int/Bool/String/Map/List theories | All parsing, execution, and proof closure | Necessary low-level trusted computing base; live versions and statuses recorded. |
| Byte-identical supplied MiniPython semantics | Control, scopes, heap, calls, loops, dictionaries, exceptions | Authorized fixed semantics in this mode. Used-path rules were statically mapped and concretely exercised. |
| Trusted `py2mpy.py` | Python-to-AST bridge | Byte-identical candidate copy; regenerated AST is byte-identical. Acceptable trusted input boundary. |
| `histogramCheck` AST clone | Which program body is proved and how the result is observed | Machine-compared KAST identity; assertion mutation is discriminating. Acceptable for the listed inputs. |
| `tokenText` plus its `splitWS` equation | Supplies the list iterated by both loops in c06–c13 and therefore their final results | Program-derived, result-bearing synthetic abstraction with no bridge-free connection theorem. Its claimed concrete-string denotation has a recorded false witness. Illegitimate as support for real-input generality. |
| Differential Python tests | Program-to-canonical agreement | Independent, reproducible, zero mismatches over 3,757 strict-domain inputs. Finite empirical evidence only. |
| Strict interpretation of “space separated lowercase letters” | Excludes observed whitespace divergences | Reasonable but informal domain bridge; a permissive interpretation would expose implementation disagreement. |
| Supplied opaque float, sorting, and MD5 symbols | None on these claims | Inventoried but off-path; they neither help nor weaken this proof result. |

### Decision

The source program and translated AST are faithful on the strict intended
domain, fresh proof reconstruction succeeds, the five real examples are honest
executions, and the claims are non-vacuous. Those facts are insufficient for
legitimacy of the requested program proof.

There is no entry claim for an arbitrary valid input and no loop invariant or
arbitrary-length summary. The only attempted generalization is bounded to
length three and starts from synthetic pre-split terms rather than concrete
strings. Removing its split equation exposes the exact stuck computation, and
its unrestricted proposed denotation has a concrete false witness. Differential
testing cannot replace either the absent universal reachability claim or the
missing connection theorem. Accordingly, the candidate contains verified test
cases, not a legitimate partial-correctness proof of the real generated program
over the natural contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
