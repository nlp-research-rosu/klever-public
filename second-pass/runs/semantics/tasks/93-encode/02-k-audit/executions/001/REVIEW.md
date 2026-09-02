# Independent adversarial audit: 93-encode

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted function under the supplied MPY semantics. I reconstructed
the definition and proof from source, obtained a fresh joint `#Top`, confirmed
that the loop helper itself closes, checked that the proof-local summary is
defined rather than opaque, and made both a body mutation and a false-result
mutation fail at the expected obligations.

The verdict is `CONCERNS / LEGIT`, not `PASS`, because four requested generation
and provenance artifacts are absent, the formal entry starts at a directly
constructed exact closure rather than proving module-load/name-lookup as a
separate reachability lemma, and the bridge from the formal ASCII summary to the
trusted Python/natural-language contract is supported by static reasoning and
finite differential evidence rather than a separate K equivalence theorem.
None of those limitations lets a false result be proved for the intended
English-alphabet/space domain.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` exists and is a directory, so the trusted
mount does not contradict the mode. There is no infrastructure breach.

The recursive candidate/trusted comparison checked entry names, entry types,
symlinks, extra/missing entries, and bytes:

- Every candidate semantics entry is a regular file/directory of the same type
  as the trusted entry.
- There are no symlinks below `/candidate/reference-semantics`.
- There are no missing or additional entries.
- Recursive `diff -ruN --no-dereference` exits `0`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `856a164439599802d5210e2969c1c5673c84b83b4bdca5db34384d7b10d3d741`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

Evidence: [integrity script](evidence/stage1_integrity.sh) and
[integrity log](evidence/stage1_integrity.log).

### Missing and additional artifacts

The following requested untrusted provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. Consequently I could not check
generation metadata or reconcile a trace with the submitted files. This is a
provenance/evidence defect and one reason for `CONCERNS`; it is not used as a
substitute for the source-level audit.

The proof sources `solution.py`, `solution.mpy`, `spec.k`, `verification.k`,
and the complete supplied-semantics tree are present as ordinary files.
`prove.sh`, `concrete_tests.py`, and `concrete_tests.mpy` are additional
untrusted convenience artifacts. Candidate `ktemp/` and `__pycache__/` are
generated caches; neither was copied into nor reused by the clean build.

All execution sources were copied to `/tmp/audit-work/candidate-src`; trusted
inputs were copied separately to `/tmp/audit-work/trusted`. Builds and
experiments were performed only in scratch.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `encode(message)` to:

1. swap the case of every English-alphabet letter; and
2. after that case swap, replace every vowel with the character two English
   alphabet positions/code points later.

Thus a lowercase source vowel becomes its uppercase successor-by-two and an
uppercase source vowel becomes its lowercase successor-by-two. Consonants only
change case. Although the prose says “only letters,” its second documented
example contains spaces; I treat ASCII English letters plus spaces as the
intended domain and spaces as preserved.

The trusted canonical implementation constructs the ten ASCII vowel
replacements, calls `message.swapcase()`, then applies the replacement map to
each resulting character. The submitted implementation iterates left to right,
swaps each character, computes `ord`, tests the same ten vowel codes, appends
`chr(code + 2)` on the vowel branch, and otherwise appends the swapped
character. These algorithms agree on the intended domain.

### Translator fidelity

The trusted command

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/solution.py
```

regenerated `solution.mpy`. The regenerated and submitted files are byte
identical, both with SHA-256
`04539dc1d1d48cd87de3b5256faf3b8abf63700e553c9687088765473ad625e5`.
Evidence: [fidelity script](evidence/stage2_fidelity.sh) and
[fidelity log](evidence/stage2_fidelity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports
`/tmp/audit-work/trusted/canonical.py::encode` and
`/tmp/audit-work/candidate-src/solution.py::encode`. It covers:

- both documented examples;
- empty input and individual vowel/consonant/case/space boundaries;
- all ASCII lowercase and uppercase letters;
- every length-one and length-two string over 52 ASCII letters plus space
  (2,862 cases);
- 1,000 deterministic random strings of lengths 0 through 256
  (seed `930093`).

There were 3,885 cases and zero mismatches. Exact generated inputs are in
[differential_inputs.jsonl](evidence/differential_inputs.jsonl), SHA-256
`7d994ca59083366e88efcde26479dc48d59d5ff5b86e73118af3a305ea6e2c5a`.
The command, scope, examples, and exit `0` are in
[differential_test.log](evidence/differential_test.log).

This finite test supports, but does not itself prove, the universal bridge.
The static code comparison supplies the broader ordinary-mathematics argument.
Non-ASCII Unicode case mappings are excluded by the prompt’s “English
alphabet” wording and by the supplied semantics’ documented ASCII model.

## 3. Clean proof reconstruction

The installed tools are K `v7.1.337`; exact paths and versions are in
[toolchain.log](evidence/toolchain.log).

### Fresh concrete definition

From `/tmp/audit-work/candidate-src`, with no candidate kompiled directory:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

This exits `0`; see [runtime build log](evidence/stage3_kompile_runtime.log).
The compiler reports non-exhaustive total-function warnings for unrelated
helpers (`mapStrVS`, float conversion helpers, `joinCodes`, and `valSeqAt`);
none is on the submitted program’s proof path.

The candidate assertion program executes to `.K`, empty heap/stack, normal
exception state, and exit code `0`:
[candidate concrete log](evidence/stage3_krun_candidate_tests.log).

I also authored a separate boundary suite, translated it with the trusted
translator, and ran it against the fresh definition. It covers empty input,
both examples, all vowels, all lowercase and uppercase letters, and mixed
spaces/cases. It exits `0`:
[independent source](evidence/audit_concrete_tests.py),
[script](evidence/stage3_independent_krun.sh), and
[log](evidence/stage3_independent_krun.log).

### Fresh proof definition and positive claims

The proof definition was built with:

```text
kompile verification.k --backend haskell --main-module ENCODE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

It exits `0`; see
[verification build log](evidence/stage3_kompile_verification.log).

The independent target run was:

```text
kprove spec.k --definition verification-kompiled --spec-module ENCODE-SPEC
```

It exits `0` and prints `#Top`; see
[all-claims proof log](evidence/stage3_kprove_all.log). This proof unit contains
all three positive claims: `encode-total`, `encode-init`, and `encode-loop`;
therefore the joint `#Top` closes every submitted obligation, including the
helper circularity on which the end-to-end claim depends.

As additional checks, filtering to `ENCODE-SPEC.encode-init` and
`ENCODE-SPEC.encode-loop` independently produces `#Top`, exit `0`:
[init log](evidence/stage3_kprove_encode_init.log) and
[loop log](evidence/stage3_kprove_encode_loop.log).

A diagnostic that filtered to `encode-total` alone was manually interrupted
after approximately 90 seconds. The filter removes the submitted loop helper,
so this is not the submitted joint proof and is not evidence against its
closure. It is recorded transparently in
[the diagnostic log](evidence/stage3_kprove_encode_total_only.log). No candidate
verdict is based on that diagnostic.

## 4. Adequacy and real-program pinning

Detailed plain-language preconditions, postconditions, and ground satisfying
states are preserved in [claim_witnesses.md](evidence/claim_witnesses.md).

### `encode-total`

The precondition directly calls a closure with parameter `message`, defining
scope `0`, the exact function body, and argument `str(INPUT)`. Module scope,
builtins parent, allocation stores, stack, return state, exception state, and
exit code are all ground and normal. There is no side condition on `INPUT`, so
`INPUT = .IntSeq` and the code sequence for `"test"` are both satisfying
instances.

The postcondition requires the returned `<k>` value to be exactly
`str(encodeCodes(INPUT))`. It is neither a free variable nor a one-way
implication. All other listed cells are preserved.

### `encode-init`

The precondition is the same realizable direct-closure call. The destination is
the actual loop head followed by the actual `Return(Name("result"))` and
`#endcall`. It fixes the callee environment to contain the original message,
empty `result`/`char`, and `code = 0`, and fixes the exact caller frame. This is
a finite call-setup/initialization claim, not a summary that skips the loop.

### `encode-loop`

The precondition is the real `#loop` over a remaining string, with the real loop
body and return/endcall continuation. `ACC` is the current output. `_MESSAGE`,
`_OLDCHAR`, and `_OLDCODE` are generalized, but the loop does not read
`message`, and overwrites `char` and `code` before their relevant uses. The
generalization is therefore sound.

The postcondition is exactly `str(encodeAcc(INPUT, ACC))` and fixes restoration
of the caller environment, removal of the callee scope/frame, and normal
heap/return/exception/exit cells. A satisfying nontrivial instance is remaining
input `"test"` with accumulator `"P"`, whose result is `"PTGST"`.

### Pinning evidence

The proof does not parse `solution.mpy` at proof time; it uses two macros.
I compared them exhaustively with the byte-regenerated AST:

- `encodeFunctionBody` is exactly the four initial/loop/return statements from
  `solution.mpy`.
- `encodeLoopBody` is exactly the swapcase, ord, ten-way `or`, conditional
  `chr(code + 2)`, and string accumulation emitted by the translator.
- Parameter name/order and defining scope match the generated `FuncDef`.

The fixed `FuncDef` rule would install this exact closure and fixed lookup would
retrieve it. The formal entry begins immediately at the resulting closure call,
so it omits module installation/name lookup but does not substitute a different
body or binding. The independently translated `krun` suite executes the full
module path and leaves the exact closure in module scope.

Body sensitivity was tested in a separate fresh definition: changing only the
pinned loop expression from `code + 2` to `code + 3`, while leaving the summary
and claims unchanged, builds successfully but makes `kprove` exit `1`. The
residual exposes the expected accumulator disagreement, including `99` versus
`100`. Evidence:
[mutation description](evidence/body_mutation.md),
[mutated source](evidence/verification-body-mutated.k),
[build log](evidence/stage5_body_mutation_build.log), and
[failed proof log](evidence/stage5_body_mutation_proof.log).

### Concrete result substitutions

[claim_substitution.py](evidence/claim_substitution.py) evaluates the exact
`swapC`/`encodeCode` equations on empty input, both examples, all vowels, and a
mixed consonant/space case, then compares with both Python implementations.
There are zero mismatches; see
[substitution log](evidence/stage4_claim_substitution.log).

The same ground formal summaries, both result branches, and the nonempty loop
accumulator close as reachability claims with `#Top`, exit `0`:
[ground spec](evidence/summary-ground.k) and
[ground proof log](evidence/stage4_summary_ground_kprove.log).
An earlier bare functional-claim form was rejected because this Haskell backend
does not support functional claims; that resolved diagnostic is preserved in
[the unsupported-form log](evidence/stage4_summary_ground_functional_unsupported.log)
and is not used as proof evidence.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) inventories every declaration/rule in
the supplied `semantics.k`, all semantics helper files, `verification.k`, and
`spec.k`. The complete row-by-row inventory, including location, full normalized
declaration, attributes, and audit decision, is
[k_inventory.csv](evidence/k_inventory.csv), SHA-256
`85c214026bd88146bc348bdc4f91fe1d910d5bd2a12ae03c9938996518187987`.

The 1,033 records comprise:

- 703 ordinary/macro/concrete rules;
- 233 syntax declarations;
- 88 imports;
- 5 contexts;
- 1 configuration;
- 3 reachability claims.

Attributes include 150 function declarations, 112 total declarations, 45
priority-bearing records, 35 concrete records, 25 symbol records, 22
`no-evaluators` records, 26 `owise` records, and the macro/strictness records.
There are zero `simplification` rules and zero `functional` declarations.
Counts and command status are in
[inventory summary](evidence/k_inventory_summary.txt) and
[inventory log](evidence/stage5_inventory.log).

The submitted construct-to-rule mapping is
[program_construct_map.md](evidence/program_construct_map.md). Every construct
in `solution.mpy` has both a syntax declaration and an executable fixed rule
path.

### Fixed supplied semantics

The 695 fixed rules are byte-identical to the trusted supplied tree, not
candidate proof extensions. I reviewed their complete files and treated them as
the selected language definition. For the real submitted path:

- configuration cells consistently model computation, current scope, scope
  store/location, heap/location, call stack, return, exception, and exit code;
- call evaluation resolves the exact callee, evaluates arguments left to right,
  allocates a new scope, binds the single parameter, and pushes the exact
  continuation;
- strictness/contexts evaluate assignments, comparisons, integer addition, and
  conditions in the required order;
- `BoolOp("or", ...)` is short-circuiting and value-returning, but every operand
  here is a Boolean comparison;
- string iteration yields one code at a time in order;
- loop binding updates `char`, the body executes, and the remaining iterator
  returns to the same loop head;
- `swapC` has disjoint uppercase/lowercase/otherwise cases; `mapSwap` is
  structural;
- `ord` accepts the singleton yielded by string iteration;
- `chr` is guarded to ASCII, and every reachable call in this program is an
  ASCII vowel code plus two (at most 119), so the guard is always satisfied;
- string concatenation is left-to-right and structurally recursive;
- `Return` drops the remaining callee continuation, and `#pop` restores the
  exact caller cells stated by the claims.

Relevant priorities are specializations for heap/cell/reference cases; the
entry state has no such objects, and the ordinary rules are selected. The fixed
`Call` rule is `owise`, but no problem-local operational interception exists.
No fixed or proof-local rule bypasses this program’s body.

The imported theory also contains deliberately opaque primitives for other
tasks. The 25 symbol declarations are:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

None is syntactically reachable from `solution.mpy`, its summaries, or its
claims. Likewise, total-but-underconstrained helpers mentioned by compiler
warnings are not reachable. They therefore do not influence a branch, state,
result, or postcondition in this theorem. I found no concrete or symbolic
witness by which one could enable a false conclusion on the intended input
domain; accordingly I do not label them unsound. Their narrower limitation is
that this audit says nothing about proofs for programs that use those
primitives.

### Candidate proof-local inventory

`verification.k` adds exactly:

- two syntax macros and their two macro equations for the exact submitted loop
  and function bodies;
- `isVowelCode`, one total Boolean equation over exactly the ten ASCII vowel
  codes;
- `encodeCode`, two guarded equations;
- `encodeAcc`, base and structural-recursive equations;
- `encodeCodes`, one wrapper equation.

The macros are compile-time AST abbreviations, not operational bridges.
`isVowelCode` is a fully defined mathematical predicate. The two `encodeCode`
guards are complementary and disjoint, and their right-hand sides match the two
real branches after `swapcase`. The `encodeAcc` patterns are constructor
disjoint, cover every finite `IntSeq`, and recurse on the strict tail.
`encodeCodes` merely chooses the empty accumulator.

There is no proof-local priority, simplification, concrete rule, opaque symbol,
oracle, totalization gap, or operational rule that preempts fixed semantics.
The program-derived summary is connected to execution by the universal
`encode-loop` reachability claim itself; it is not injected by a shortcut using
the same symbol in execution and postcondition. Its body-sensitivity failure
confirms that the summary cannot survive a material body change.

I found no unsound candidate rule. Therefore there is no required false
conclusion witness to report for an unsoundness finding.

## 6. Fresh non-vacuity test

The fresh mutation changes the end-to-end destination from

```text
str(encodeCodes(INPUT))
```

to

```text
str(iCons(88, encodeCodes(INPUT)))
```

while retaining the original support claims. This prefixes every alleged
result with code `88` (`"X"`). A concrete satisfying witness is
`INPUT = .IntSeq` and the ground initial cells from `encode-total`: real
execution returns `""`, whereas the mutation demands `"X"`.

The exact mutation and witness are
[spec-vacuity.k](evidence/spec-vacuity.k) and
[nonvacuity_witness.md](evidence/nonvacuity_witness.md).

The dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled --spec-module ENCODE-SPEC-VACUITY --dry-run
```

exits `0`, establishing that the mutation parses/builds; see
[mutation build log](evidence/stage6_mutation_build.log).

The actual proof command:

```text
kprove spec-vacuity.k --definition verification-kompiled --spec-module ENCODE-SPEC-VACUITY
```

exits `1` with `WarnStuckClaimState`. The residual is the expected unmet
condition:

```text
encodeAcc(INPUT, .IntSeq)
#Equals
iCons(88, encodeAcc(INPUT, .IntSeq))
```

It is not a parser error, missing import, timeout, or unrelated crash. See
[mutation proof log](evidence/stage6_mutation_proof.log).

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the fixed supplied MPY semantics, for every finite K `IntSeq` supplied as
the string argument in the ground entry configuration, if execution follows
the modeled function call/loop and terminates, the exact submitted function
body returns `str(encodeCodes(INPUT))`, restores the caller environment and
stack, leaves the heap empty, and leaves return/exception/exit state normal.
The loop theorem is accumulator-parametric:
starting at the exact loop head with remaining `INPUT` and current `ACC`
returns exactly `str(encodeAcc(INPUT, ACC))`.

This is partial correctness. It is not a K theorem that the Python interpreter
terminates, a formal equivalence theorem against `canonical.py`, or a theorem
about non-ASCII Unicode behavior.

### Trust ledger

1. **Trusted mounted inputs.** `/reference/prompt.py`,
   `/reference/canonical.py`, `/reference/py2mpy.py`, and
   `/reference/reference-semantics` are authoritative by the audit task.
   Candidate prompt, translator, and semantics match them byte-for-byte.

2. **K implementation and builtin theories.** Correctness of K `v7.1.337`, the
   Haskell/LLVM backends, parsing, matching logic, and builtin integer/Boolean/
   string/map/list operations is outside the candidate theorem. This is the
   ordinary machine-checked-proof trust boundary.

3. **Supplied ASCII language model.** `strToCodes`, `swapC`, and `chr` model the
   ASCII subset. This is acceptable for the stated English-alphabet domain and
   the example spaces. It would be inadequate for general Unicode letters.

4. **Direct-closure entry bridge.** The proof starts from the exact closure
   value instead of the full `Module(FuncDef(...))` plus `Name("encode")`.
   Fixed `FuncDef`/lookup rules, exact macro comparison, the full-module `krun`,
   and the body mutation support this bridge. It is a documented formal-scope
   limitation but does not leave the body, binding, result, or control
   unconstrained.

5. **Proof-inert opaque imported symbols.** All 25 are listed in Stage 5. They
   affect none of this theorem’s terms or claims. No conclusion here depends on
   an interpretation of them.

6. **Natural-language/canonical bridge.** The interpretation of
   `encodeCodes` as “swap case, then advance vowels by two” follows directly
   from its exhaustive equations and the trusted `swapC` equations. Agreement
   with both Python implementations is also empirically supported by 3,885
   differential inputs and the ground substitutions. The finite tests are not
   promoted to a universal proof.

7. **Termination and excluded behavior.** The result is reported as partial
   correctness. Non-ASCII case expansion, malformed MPY values, Python
   exceptions outside the modeled subset, and unrelated supplied-semantics
   constructs are excluded.

### Gate assessment

- Real-program soundness: **PASS**. Exact body, fixed execution, no operational
  shortcut/oracle, joint `#Top`, body sensitivity, satisfiable preconditions,
  and a rejected false result.
- Intent adequacy: **PASS with documented scope**. The English ASCII
  letter/space contract matches the code and summary; general Unicode is
  excluded.
- Trust/evidence auditability: **CONCERN**. The four generation/provenance
  artifacts are absent, and the full-module/canonical equivalence bridges are
  static/empirical rather than separate reachability theorems.

These concerns limit provenance and theorem packaging, not the legitimacy of
the reconstructed result-constraining proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
