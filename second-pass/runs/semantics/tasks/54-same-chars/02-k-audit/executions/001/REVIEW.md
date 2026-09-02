# Independent adversarial review: 54-same-chars

This audit used the required `using-kit` and `validating-proof` procedures. It
treated `/candidate` as read-only and untrusted, copied sources to
`/tmp/audit-work`, rebuilt every definition from source, and wrote only
reviewer evidence below `/audit-output/evidence`.

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists. There is no infrastructure
breach.

## 1. Input and provenance integrity

The candidate tree, artifact types, and missing-file checks are recorded in
[01-provenance-tree.log](evidence/01-provenance-tree.log). All candidate proof
sources used in this audit are regular files. There are no symlinks anywhere
under `/candidate`, including under `reference-semantics/`.

Integrity results:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`cmp`, exit 0): [02-prompt-compare.log](evidence/02-prompt-compare.log).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`cmp`, exit 0): [03-translator-compare.log](evidence/03-translator-compare.log).
- The complete candidate `reference-semantics/` tree is recursively identical
  to the trusted tree. There are no missing, additional, changed, mistyped, or
  symlinked entries (`diff -ruN --no-dereference`, exit 0):
  [04-semantics-compare.log](evidence/04-semantics-compare.log).
- The copied source hashes are preserved in
  [19-source-hashes.log](evidence/19-source-hashes.log).

The following named provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace (no JSON or trace artifact is present)

They therefore could not be read even as untrusted claims. The extra
`/candidate/__pycache__/solution.cpython-310.pyc` was ignored and never
executed. The absence of the provenance records is an auditability concern, but
not a missing proof source: `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, the supplied semantics, and the build script are present.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks whether two words have the same characters. The trusted
canonical implementation defines that precisely as `set(s0) == set(s1)`:
duplicate count and order do not matter; membership does. The intended input
domain is pairs of Python strings, including empty strings.

`/candidate/solution.py` implements exactly the canonical return expression.
Using the trusted copied translator to regenerate `solution.mpy` produced byte
identity with the submitted file. Both files have SHA-256
`50ea732f523d5b7b821b7f2c3a1055e0456cf1e8b9b57d306d967066453a8d07`;
the translator and comparison both exited 0:
[05-translation-identity.log](evidence/05-translation-identity.log).

The independent differential driver is
[differential_same_chars.py](evidence/differential_same_chars.py). It imports
separate scratch copies of the trusted canonical module and candidate module.
Its scope was:

- all six documented examples;
- empty/empty and each one-sided-empty case;
- equal singleton, duplicate, order, proper-subset in both directions,
  disjoint, case, whitespace, NUL, accented, and emoji cases;
- all 14,641 pairs from the 121 strings of length 0 through 4 over `ab!`;
- 2,000 deterministic random pairs of length 0 through 24 over an alphabet
  containing ASCII, whitespace, NUL, `é`, and an emoji.

The run checked 16,663 pairs, found zero mismatches, and exited 0:
[06-differential.log](evidence/06-differential.log). This is finite evidence,
not a substitute for the K proof.

## 3. Clean proof reconstruction

The toolchain was `/usr/bin/kompile` and `/usr/bin/kprove`, K
`v7.1.337`; see [00-toolchain.log](evidence/00-toolchain.log). No candidate
compiled definition or cache was reused.

Fresh reconstruction results:

1. The concrete supplied semantics was compiled from the scratch source with
   LLVM:

   ```text
   kompile reference-semantics/semantics.k --backend llvm \
     --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
     --output-definition /tmp/audit-work/runtime-kompiled
   ```

   Exit status was 0:
   [07-kompile-concrete.log](evidence/07-kompile-concrete.log). The compiler
   reported non-exhaustiveness warnings for unrelated helpers and unused
   variables; none is on the `same_chars` execution path.

2. Running the actual submitted `solution.mpy` with that fresh definition
   exited 0. The final module scope binds `same_chars` to the closure whose
   parameters and body match the submitted AST:
   [08-krun-solution-module.log](evidence/08-krun-solution-module.log).

3. The proof definition was compiled from scratch with Haskell:

   ```text
   kompile verification.k --backend haskell \
     --main-module SAME-CHARS-VERIFICATION \
     --syntax-module SAME-CHARS-VERIFICATION \
     --output-definition /tmp/audit-work/verification-kompiled
   ```

   Exit status was 0:
   [09-kompile-proof.log](evidence/09-kompile-proof.log).

4. `spec.k` contains one positive target claim and no helper claims. The
   independent command

   ```text
   kprove spec.k \
     --definition /tmp/audit-work/verification-kompiled \
     --spec-module SAME-CHARS-SPEC
   ```

   printed `#Top` and exited 0:
   [10-kprove-positive.log](evidence/10-kprove-positive.log).

5. As an additional concrete check, the reviewer-authored boundary harness
   [concrete_boundary.py](evidence/concrete_boundary.py) was translated with
   the trusted translator
   ([11-translate-concrete-boundary.log](evidence/11-translate-concrete-boundary.log))
   and executed with the fresh LLVM definition. All eight assertions completed,
   `<exc>` remained `NoExc`, the exit code remained 0, and `krun` exited 0:
   [12-krun-concrete-boundary.log](evidence/12-krun-concrete-boundary.log).

Thus the clean-build and positive-proof gate passes.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim. It has no explicit `requires`, so its formal inputs
are arbitrary values of sort `IntSeq`. Its configuration precondition is an
exact fresh module state:

- current environment location 0;
- empty module scope 0 whose parent is the fixed builtins scope at -1;
- next scope location 1;
- empty heap with next heap location 0;
- empty call stack, no return pending, no exception, and exit code 0.

From that state, `#sameChars(S0,S1)` must reach the Boolean
`sameSet(dedupCodes(S0), dedupCodes(S1))`. Every other listed cell must return
to its initial value. This is equality of the two sets of distinct integer
character codes, expressed as mutual membership. The postcondition is an
equality-producing expression, not a free result variable, tautology, or
one-way implication.

The precondition is satisfiable. For example, let both `S0` and `S1` be
`.IntSeq` and use the displayed initial cells. The claimed result is `true`.
For a false-result witness, codes `[97,98]` and `[99,100]` yield `false`.
The two reviewer ground claims both closed with `#Top`:
[spec-ground-witness.k](evidence/spec-ground-witness.k) and
[16-kprove-ground-witnesses.log](evidence/16-kprove-ground-witnesses.log).
The corresponding Python inputs `("", "")` and `("ab", "cd")` return,
respectively, `True` and `False` in both implementations, as recorded in the
differential log.

### Wrapper and actual program

The candidate entry `<k>` cell starts with the fresh symbol `#sameChars`; it
does not itself load the submitted `solution.mpy`. Its single rule expands that
symbol to an ordinary call of a closure containing the full function body. The
closure's parameter list, statement list, argument order, defining environment
0, and both `set` calls are constructor-for-constructor identical to the
closure produced by loading the submitted `solution.mpy`. The trusted
translation identity and the concrete module-load result independently confirm
that syntactic link.

To avoid relying only on that inspection, the audit built a second Haskell
definition importing only the fixed `MPY` semantics—never `verification.k`:
[20-kompile-fixed-proof.log](evidence/20-kompile-fixed-proof.log). The
reviewer-authored bridge-free claim
[spec-actual-program-connection.k](evidence/spec-actual-program-connection.k)
loads the exact submitted module AST, retains the resulting `same_chars`
binding in scope 0, resolves the name normally, and invokes it on arbitrary
symbolic `IntSeq` inputs. It parsed successfully
([21-actual-connection-dry-run.log](evidence/21-actual-connection-dry-run.log)),
then printed `#Top` and exited 0 under the fixed semantics:
[22-kprove-actual-connection.log](evidence/22-kprove-actual-connection.log).

This establishes a universal fixed-semantics connection for the real module,
not just finite test cases. The candidate wrapper factors away the persistent
module binding, which is unobservable to this return-value task, while running
the same body through the same lookup, argument, frame, and return rules. The
connection is strong enough to pin the result to the real generated program.
However, the connection theorem is reviewer-authored rather than included with
the candidate; that is one reason for `CONCERNS` rather than `PASS`.

## 5. Rule-by-rule static soundness review

The source-anchored exhaustive inventory is generated by
[inventory_k.py](evidence/inventory_k.py) and preserved in
[13-rule-inventory.log](evidence/13-rule-inventory.log). It covers all 24
supplied helper files plus assembled `semantics.k`, `verification.k`, and
`spec.k` (26 K files total). It enumerates every top-level syntax declaration,
configuration, context, rule, claim, relevant attribute, guard, priority, and
source line.

Inventory totals are:

| Category | Count |
|---|---:|
| Syntax declarations | 228 |
| Functional declarations | 145 |
| `total` declarations | 107 |
| Opaque or explicitly named symbols | 25 |
| Semantic rules | 696 |
| Priority rules | 49 |
| `owise` rules | 29 |
| Rules carrying `concrete` | 36 |
| Simplification rules | 0 |
| Claims | 1 |

Of the 696 rules, 695 are in the byte-identical supplied-semantics tree and one
is candidate-local. The disposition for every inventory entry under
`reference-semantics/` is **accepted at the selected fixed-semantics boundary**:
it is not a candidate proof extension. This is not an assumption that those
rules are all needed. The used execution slice was checked individually below;
unused rules cannot be reached by this program. The fixed semantics imports 25
opaque/named symbols:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`.

None is reachable from `same_chars`; no final value, branch, cell, or proof
condition depends on one. The concrete-only sort/float rules are likewise
inert in the Haskell proof.

The candidate-local inventory is exactly:

1. `syntax KItem ::= "#sameChars" "(" IntSeq "," IntSeq ")"`; and
2. one unconditional rule expanding it to `Call(closureVal(...), ...)`.

There are no candidate-local functions, `total`/`functional` declarations,
opaque symbols, priorities, simplifications, mathematical lemmas, loop claims,
or result oracles. The local rule is a definitional entry wrapper, not an
answer-encoding summary: after one rewrite, fixed semantics executes the
complete program-defined body. It reads only `S0` and `S1`, changes only the
active computation, frames all other cells, introduces no abrupt control
effect, and delegates calls and return to fixed rules. The bridge-free theorem
in Stage 4 validates its result against real module execution over the complete
symbolic input domain.

### Used syntax and rules

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` loads statement lists and `functions.k` installs the closure in the current scope. |
| `Call`, argument lists | `call.k` evaluates the callee, then `core.k` evaluates arguments left-to-right. The special math/MD5 interceptors do not match; the generic `owise` call rule is selected. |
| `Name("same_chars")`, `Name("set")`, parameters | `core.k` walks current scope to parents. The actual-program theorem resolves `same_chars` in scope 0; each `set` resolves at builtins scope -1; parameters resolve in the callee frame. Present/absent map guards are complementary. |
| `closureVal`, parameter binding, `Return` | `call.k` allocates the frame and pushes the continuation; `functions.k` binds `s0` then `s1`, records the return, pops the frame, deallocates its scope, and restores environment/stack/scope location. The cell-variable priority rule is disabled because this is a plain frame. |
| `Compare` and `CmpOp("==", ...)` | `operators.k` evaluates left then right and dispatches once both are values. Heap-reference priority rules cannot match these direct `setV` values. |
| `set(str(...))` | `builtins.k` maps it to `setV(dedupCodes(...))`; this constructor does not allocate or mutate the heap. |
| set equality | `set.k` maps `setV == setV` to `sameSet`; `sameSet` is two `subsetCodes` checks. `dedupCodes`, `dedupFrom`, `codeIn`, and `snocCode` are structurally recursive; the duplicate/non-duplicate guards are exact Boolean complements. |

Evaluation order is therefore callee, first argument, second argument, left
`set`, right `set`, equality, return. The temporary callee scope is the only
state allocation and is restored; heap, exception, return state, and exit code
match the postcondition. There is no loop or helper claim to audit.

The LLVM compiler's non-exhaustiveness warnings concern `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and out-of-bounds `valSeqAt`; none occurs in the
mapped syntax or proof path. They expose no false equality and are not
candidate-added rules. No rule is labeled unsound in this review, so the
false-conclusion-witness requirement for an unsoundness finding is not
triggered.

As an operational-sensitivity check, the auditor changed only the second
argument of the wrapper body from `s1` to `s0`. The mutant is preserved as
[verification-body-mutant.k](evidence/verification-body-mutant.k), compiled
successfully ([17-kompile-body-mutant.log](evidence/17-kompile-body-mutant.log)),
and made the original theorem fail with an expected result-equality residual
and exit 1:
[18-kprove-body-mutant-failure.log](evidence/18-kprove-body-mutant-failure.log).
Thus the proof is sensitive to the real property-bearing computation.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`.

The fresh mutation
[spec-vacuity.k](evidence/spec-vacuity.k) changes the result obligation to
`notBool sameSet(dedupCodes(S0), dedupCodes(S1))`. It is demonstrably false for
the satisfying input `S0 = S1 = .IntSeq`, where the actual and intended result
is `true`.

The mutated claim parsed and compiled to KORE successfully with `--dry-run`,
exit 0:
[24-vacuity-final-dry-run.log](evidence/24-vacuity-final-dry-run.log). The real proof run
then exited 1 with `WarnStuckClaimState`; its residual explicitly shows that the
computed mutual-subset Boolean cannot imply its negation:
[25-kprove-vacuity-final-failure.log](evidence/25-kprove-vacuity-final-failure.log). This is
the expected unmet result obligation, not a parser error, missing import,
timeout, or unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for all symbolic finite `IntSeq` inputs in
the exact initial state, executing the complete translated `same_chars` body
returns
`sameSet(dedupCodes(S0), dedupCodes(S1))` and restores the listed temporary
machine state. The candidate claim establishes this through the entry wrapper;
the bridge-free fixed-semantics claim independently establishes it by loading
and calling the exact submitted module. This is a partial-correctness result;
it is not a claim about behavior outside the modeled input/state domain.

The result is discriminating: opposite-result and body mutations fail. There
are no proof-local oracles, opaque summaries, assumptions, or lemmas that fix
the desired answer.

### Trusted or external boundaries

- **Supplied MPY semantics:** accepted as the mode-selected fixed semantics
  after exact recursive integrity comparison. All proof claims depend on its
  configuration, lookup, call, return, set, and equality rules.
- **K implementation and builtin theories:** the K parser/compiler/prover and
  builtin integer, Boolean, string, map, list, and equality hooks are trusted.
  This is the ordinary low-level proof checker boundary.
- **Trusted translator:** byte identity proves the submitted `.mpy` is exactly
  what the mounted translator emitted. Correctness of that translator as a
  model of Python is not itself proved in K.
- **Canonical intent bridge:** interpreting “same characters” as Python set
  equality comes from the trusted prompt and canonical implementation.
  `sameSet` has transparent recursive equations matching that mathematics, but
  the natural-language interpretation and the mapping of Python characters to
  integer-code sequences remain an informal boundary.
- **Imported opaque symbols:** all 25 are listed in Stage 5. None is reachable,
  so they have no dependent claim here and introduce no result-bearing trust.
- **Actual-program wrapper link:** universal fixed-semantics evidence now
  supports it, but the candidate did not supply that connection theorem.

### Empirical evidence and its limits

The 16,663-pair Python differential supports candidate-to-canonical fidelity.
The eight-case MPY run supports concrete behavior of the used supplied
semantics. The actual-module `krun` result supports the parsed closure shape.
None of those finite runs replaces the universal K claims; conversely, the K
claims do not formally verify the trusted Python-to-MPY translator or the
English interpretation.

### Decision

The reconstructed proof is sound, result-constraining, body-sensitive, and
connected to the real submitted program. No false rule or result-bearing oracle
contributes. It is therefore legitimate.

The status is `CONCERNS` rather than `PASS` because the candidate omitted all
named generation/provenance records and did not include its own bridge-free
actual-module connection theorem; the audit had to reconstruct that key
pinning evidence independently. These are auditability and evidence limitations,
not mechanisms that permit a false conclusion.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
