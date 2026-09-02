# Independent adversarial audit: 48-is-palindrome

## Outcome

The reconstructed reachability proof is legitimate and result-constraining. It
executes the submitted `solution.mpy` body under the supplied semantics and
proves that the return value is equality between the input code sequence and
its reverse. The sole proof-local rule only gives that expression the name
`palindrome`; it does not intercept or replace execution. A second reconstruction
with that local rule absent proves the raw expression directly.

The verdict is `CONCERNS / LEGIT`, not `PASS`, for two auditability/intent-bridge
limitations:

1. all four named generation-provenance records and any structured generation
   trace are absent; and
2. the supplied concrete string-literal semantics is explicitly ASCII-only and
   failed on a non-ASCII literal, so the bridge from Python's full Unicode
   `str` domain to the theorem's abstract `IntSeq` representation remains
   informal (though it is supported by independent differential testing).

Neither limitation permits a false K conclusion about the submitted symbolic
program.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so there is no infrastructure
contradiction requiring `AUDIT_ERROR`. The complete trusted and candidate
inventories are preserved in
[01-trusted-mount-inventory.log](/audit-output/evidence/01-trusted-mount-inventory.log)
and
[02-candidate-inventory.log](/audit-output/evidence/02-candidate-inventory.log).

Integrity results:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- A recursive, no-dereference comparison of
  `/candidate/reference-semantics/` against the trusted tree reports no
  changed, missing, additional, mistyped, or symlinked entry. The inventory
  shows only ordinary directories and regular files.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. Candidate caches and `__pycache__` were not copied or used.
- Hashes and the exact comparisons are in
  [03-provenance-comparisons.log](/audit-output/evidence/03-provenance-comparisons.log)
  and
  [28-source-hashes.log](/audit-output/evidence/28-source-hashes.log).

The following named records are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace under any candidate filename exists. Presence
checks are in
[04-provenance-artifact-presence.log](/audit-output/evidence/04-provenance-artifact-presence.log).
There is also no candidate `PROOF.md` or candidate-built K definition. These
absences prevent an audit of the generation history, but do not remove a source
artifact needed for the independently reconstructed proof.

All execution used a source-only scratch copy under
`/tmp/audit-work/48-is-palindrome`; the copy operation and resulting inventory
are recorded in
[05-scratch-source-copy.log](/audit-output/evidence/05-scratch-source-copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a Python string, return `True` exactly
when reading the string from left to right yields the same sequence as reading
it from right to left. The documented cases are the empty string, `"aba"`,
`"aaaaa"`, and `"zbcd"`. The trusted canonical implementation checks every
mirrored pair and returns `False` on the first mismatch.

The submitted implementation is:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

This is a different algorithm but has the same result on Python `str`: the
right operand is the exact reversed sequence and equality returns a Boolean.

The trusted translator regenerated `solution.mpy` byte-for-byte. Both submitted
and regenerated files have SHA-256
`8278b02d667e625ef15bdd083acb6461d92384f78a36828c230508569475e863`;
see
[07-translation-byte-identity.log](/audit-output/evidence/07-translation-byte-identity.log).

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and scratch copy of the generated Python module under
distinct module names. It tests:

- all four documented examples;
- empty, one-character, even/odd length, equal/different pair, interior
  mismatch, NUL, combining-code-point, non-BMP, and Unicode cases;
- constructed mismatch positions for lengths 2 through 14;
- every binary-alphabet string of lengths 0 through 7; and
- 300 seeded generated strings of lengths 0 through 40 over a mixed alphabet.

All 650 printed inputs produced Boolean results with zero mismatches
([08-python-differential.log](/audit-output/evidence/08-python-differential.log),
exit 0). This is finite evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

K toolchain: `kompile`, `kprove`, and `krun` are the independently installed
K v7.1.337 binaries under `/usr/bin`; `kup` is absent. Exact discovery and
versions are in
[09-k-toolchain.log](/audit-output/evidence/09-k-toolchain.log).

Fresh builds and runs:

| Operation | Result | Evidence |
|---|---:|---|
| Compile trusted supplied semantics with LLVM (`MPY-KRUN`) | exit 0 | [11-kompile-llvm.log](/audit-output/evidence/11-kompile-llvm.log) |
| Run reviewer ASCII boundary assertions | exit 0, final `.K`, `NoExc`, exit code 0 | [14-krun-ascii-concrete-test.log](/audit-output/evidence/14-krun-ascii-concrete-test.log) |
| Compile candidate proof definition with Haskell (`VERIFICATION`) | exit 0 | [15-kompile-haskell-verification.log](/audit-output/evidence/15-kompile-haskell-verification.log) |
| Prove every claim in `SPEC` (one entry claim) | exit 0 and `#Top` | [16-kprove-positive.log](/audit-output/evidence/16-kprove-positive.log) |
| Compile a reviewer definition importing only fixed `MPY` semantics | exit 0 | [20-kompile-fixed-semantics.log](/audit-output/evidence/20-kompile-fixed-semantics.log) |
| Prove the raw result under fixed semantics, without `palindrome` | exit 0 and `#Top` | [21-kprove-raw-fixed-semantics.log](/audit-output/evidence/21-kprove-raw-fixed-semantics.log) |

The reviewer concrete sources and trusted translations are preserved in
[semantics_concrete_ascii_test.py](/audit-output/evidence/semantics_concrete_ascii_test.py)
and
[13-translate-ascii-concrete-test.log](/audit-output/evidence/13-translate-ascii-concrete-test.log).

The LLVM compiler emitted non-exhaustiveness warnings for several unused
helpers (`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`). None is on the
submitted program's execution path. The Haskell build emitted only unused
variable warnings in `strLt`.

A broader concrete test containing `é` failed at `strToCodes` with exit 113
([12-krun-concrete-test.log](/audit-output/evidence/12-krun-concrete-test.log)).
This is expected from the fixed source's explicit “ASCII-only” literal rule in
`semantics/str.k`; it is an adequacy/evidence limitation, not a failed positive
target claim. The symbolic entry claim receives `str(IS)` directly and does
not execute `Str(S)` or `strToCodes`.

A first reviewer attempt to express ground checks as functional claims was
rejected because this backend does not support functional claims. It was not
counted as evidence. The same cases, expressed as supported `<k>` reachability
claims, closed with `#Top`; both the diagnostic and successful form are
preserved in
[18-kprove-ground-substitution.log](/audit-output/evidence/18-kprove-ground-substitution.log),
[ground-substitution.k](/audit-output/evidence/ground-substitution.k), and
[19-kprove-ground-reachability.log](/audit-output/evidence/19-kprove-ground-reachability.log).

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `IS` is any `IntSeq`;
- execution starts by loading the exact submitted module;
- module environment is location 0 with the trusted builtins scope as parent;
- heap and stack are empty, allocation counters are initial, return state is
  `noRet`, no exception is present, and exit code is 0.

There is no additional `requires` clause. For example, `IS = .IntSeq` and
`IS = iCons(97, iCons(98, iCons(97, .IntSeq)))` are concrete satisfying
states.

Postcondition:

- the call has returned `palindrome(IS)` in `<k>`;
- the module scope retains exactly the loaded `is_palindrome` closure;
- the environment, heap, allocation counters, stack, return state, exception,
  and exit code have the specified final values.

The `<k>` program AST in `spec.k` is byte-for-byte the AST regenerated from
`solution.py`: `Module`, the one `FuncDef`, the exact parameter, and
`Return(Compare(Name("text"), CmpOp("==", Subscript(... Slice(...,-1)))))`.
The closure required in the final scope repeats the same body, preventing a
different function from satisfying the state postcondition. There are no loop
or helper claims and no substituted program.

Actual control flow is:

```text
#loadAll / statement sequencing
  -> FuncDef stores the exact closure
  -> Call evaluates Name("is_palindrome")
  -> one argument str(IS) is bound to "text" in a fresh frame
  -> Return evaluates Name("text") and text[::-1]
  -> string equality returns IS ==K reverse(IS)
  -> #pop restores the caller and leaves that Boolean in <k>
```

The negative-step slice specializes as follows:

```text
slStart(noB, someB(-1), len) = len - 1
slStop(noB, someB(-1), len)  = -1
slStep(someB(-1))            = -1
buildIS(IS, len - 1, -1, -1) = the reversed sequence
```

Thus the return is constrained, rather than a free variable, tautology, or
one-way implication. Most importantly, the reviewer
[raw-spec.k](/audit-output/evidence/raw-spec.k) proves the exact same execution
to `IS ==K buildIS(...)` using
[fixed-verification.k](/audit-output/evidence/fixed-verification.k), which has
no local rule at all.

Concrete substitutions are in
[adequacy_witness.py](/audit-output/evidence/adequacy_witness.py) and
[27-adequacy-witnesses.log](/audit-output/evidence/27-adequacy-witnesses.log):

| Python input | `IntSeq` codes | claimed result | canonical | generated |
|---|---|---:|---:|---:|
| `""` | `[]` | `True` | `True` | `True` |
| `"aba"` | `[97,98,97]` | `True` | `True` | `True` |
| `"zbcd"` | `[122,98,99,100]` | `False` | `False` | `False` |
| `"éaé"` | `[233,97,233]` | `True` | `True` | `True` |
| `"éaè"` | `[233,97,232]` | `False` | `False` | `False` |

The formal domain is actually broader than Python strings because `IntSeq`
admits arbitrary mathematical integers, not only valid Unicode scalar values.
This over-breadth does not make the rule false: reversal and structural
equality are defined for every such sequence.

## 5. Rule-by-rule static soundness review

The exhaustive reviewer inventory is
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), generated by
[inventory_k.sh](/audit-output/evidence/inventory_k.sh). It gives a source
file, line, declaration text, and decision for every local declaration:

- 228 syntax declarations;
- 696 rules (695 fixed supplied rules and one proof-local rule);
- 5 evaluation contexts;
- 1 configuration; and
- 1 entry claim.

Counts, every `total`/opaque declaration, every priority attribute, and the
absence of any simplification rule are recorded in
[25-inventory-summary-and-attributes.log](/audit-output/evidence/25-inventory-summary-and-attributes.log).
There are no `[functional]` declarations. The earlier full source-line
inventory is
[06-k-declaration-inventory.log](/audit-output/evidence/06-k-declaration-inventory.log).

For the 695 fixed rules, `ACCEPT_FIXED_*` in the TSV means: the candidate copy
is identical to the selected trusted semantics; the rule was reviewed for
overlap or reachability into the audited execution; and it is accepted at that
selected semantics level. It does not claim that this deliberately small
language is a complete model of all Python. All modules were included in the
inventory, including `MPY-CONCRETE`, although `MPY-CONCRETE` is imported only
by `MPY-KRUN` and is absent from the proof module `MPY`.

### Used syntax and rules

| Submitted construct | Declaration and operative rules |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` `#loadAll` and statement sequencing |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` creates `closureVal` in the current scope |
| `Call`, `Name` | `call.k` callee/argument routing; `core.k` scope-chain lookup |
| parameter binding and return | `call.k` fresh frame; `functions.k` `#bindP`, `Return`, `#pop` |
| `Compare`, `CmpOp("==",...)` | `operators.k` left-before-right contexts and comparison dispatch |
| `Subscript`, `Slice`, `NoBound` | `subscript.k` bound evaluation, slice normalization, `doSlice` |
| `UnaryOp("-", Int(1))` | strict unary evaluation; `core.k` integer literal; `int.k` negation |
| string slice/equality | `subscript.k` `buildIS`; `str.k` equality via structural `==K` |

Evaluation order is left-to-right where it matters. The call resolves the
loaded binding before arguments, binds the sole actual argument to the sole
formal parameter, and pushes/pops exactly one frame. `Return` has the intended
abrupt effect inside that frame. The program performs no allocation or
mutation, emits no output, and raises no modeled exception on a `str(IS)`
argument. Final state cells in the claim match the real state footprint.

For the actual slice, the guards on `slStart`, `slStop`, and `buildIS` are
disjoint. `isLen` is structurally total, step is exactly `-1`, every
`intSeqAt` use is in bounds, and the recursion descends one index. No
zero-step, out-of-bounds, or underspecified `valSeqAt` case is reachable.

### Proof-local extension

`verification.k` contains exactly:

```k
syntax Bool ::= palindrome(IntSeq) [function]
rule palindrome(IS:IntSeq)
  => IS ==K buildIS(IS, isLen(IS) -Int 1, -1, -1)
```

Classification: definitional summary. It does not appear on the left of an
operational `<k>` rewrite, does not skip a program body, and reads or writes no
configuration cell. Its single unconditional equation covers its entire
`IntSeq` domain, has no overlap, introduces no opaque value, and is
nonrecursive. The right side is the ordinary mathematical definition used by
the prompt: equality with the reverse. The fixed-semantics-only raw proof is an
independent machine-checked connection from execution to exactly this right
side.

There are no proof-local priorities, operational bridges, helper claims,
lemmas, totality declarations, simplifications, or oracles.

### Opaque and broad fixed boundaries

The fixed semantics declares opaque sort, float, and MD5 symbols. The complete
list is in
[29-opaque-symbol-inventory.log](/audit-output/evidence/29-opaque-symbol-inventory.log):
`sortVS`, `sortKeyVS`, the float/conversion family, and `md5hexCodes`. None
occurs in `solution.mpy`, the entry claim, or the reachable execution above,
so none can affect control or the result.

The concrete compiler's non-exhaustive totality warnings likewise concern
unused list/float/method helpers. The only observed used-language gap is
non-ASCII `Str` literal conversion. The entry theorem bypasses that literal
conversion by receiving an already encoded `str(IS)`. This is an evidence gap,
not an unsound rule: no false conclusion witness exists for any candidate
proof-local rule, and no rule is labeled unsound.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`. The reviewer created
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), changing
the result-constraining target from:

```k
palindrome(IS)
```

to:

```k
notBool palindrome(IS)
```

The initial state and executed body remain unchanged. `"aba"` (codes
`[97,98,97]`) is a satisfying witness for which the original result is `true`
and the mutation demands `false`.

The mutation parsed and compiled successfully in dry-run mode (exit 0,
[22-vacuity-dry-run.log](/audit-output/evidence/22-vacuity-dry-run.log)).
The actual proof exited 1 with `WarnStuckClaimState`; its residual explicitly
shows the unmet implication between the sequence equality and its negation
([23-vacuity-proof-expected-failure.log](/audit-output/evidence/23-vacuity-proof-expected-failure.log)).
This is the expected semantic failure, not a parser error, missing import,
timeout, or unrelated crash.

As a separate body-sensitivity test,
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k) changes
both copies of the executed closure body from `==` to `!=` while retaining the
original postcondition. It also exits 1 with the expected equality-versus-
negation residual
([26-body-mutation-expected-failure.log](/audit-output/evidence/26-body-mutation-expected-failure.log)).
The proof therefore depends on the submitted body.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` semantics, for every `IS:IntSeq`, execution from the
entry configuration of the exact submitted module and call is partially
correct: if it reaches the specified final configuration, its returned Boolean
is

```text
IS == reverse(IS)
```

The fresh symbolic proof actually reconstructs that reachability and closes
with `#Top`. It also establishes the stated final environment, scopes, heap,
allocation counters, stack, return state, exception state, and exit code. The
raw fixed-semantics proof establishes the same result without relying on the
name `palindrome`.

### Trusted or informal boundaries

- **Supplied semantics and K toolchain.** The trusted fixed tree, K built-in
  integer/Boolean/string/map/list operations, parser, compiler, and Haskell
  backend are in the trust base. This is the ordinary and required low-level
  boundary.
- **Trusted translator.** Byte identity proves that the submitted `.mpy` is
  exactly what the trusted translator emitted. Correctness of the mounted
  translator itself is supplied as an input.
- **`IntSeq` to Python `str` bridge.** Interpreting Python characters as their
  code-point sequence is informal, not a K theorem. Reverse and equality
  agree under that representation; 650 Python differential cases and the
  concrete substitutions support it. The fixed concrete literal route is
  ASCII-only and cannot supply full Unicode executable evidence.
- **Natural-language meaning.** “Palindrome iff equal to the reversed
  sequence” is ordinary mathematics, not a separate K theorem. It is exactly
  what both the canonical and generated Python functions compute.
- **Opaque fixed symbols.** All fixed sort/float/MD5 primitives are trusted by
  the language definition but are unreachable here and have no dependent
  claim.
- **Termination scope.** The judgment is partial correctness. No claim about
  behavior on non-`str` Python values is made; the intended annotated domain is
  `str`.
- **Generation provenance.** Missing run-input, metrics, Codex report/log, and
  structured trace prevent verification of the generation narrative. They do
  not substitute for or contribute to the reconstructed K proof.

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent
adequacy) is sound but retains the informal `IntSeq`/Unicode bridge. Gate C
(auditability) has the documented missing-provenance limitation. These
limitations justify `CONCERNS` while the independently reconstructed proof
remains `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
