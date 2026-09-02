# Independent adversarial audit — 132-is-nested

## Executive decision

The candidate is **not a legitimate proof as submitted**. Fresh reconstruction
does reproduce exit-0 `#Top` for every positive claim, the translated Python
program agrees well with the trusted canonical implementation, and a fresh
false-result mutation is rejected. However, the entry proof installs
`proved-scan-loop` as an operational rule over a strictly broader scope context
than the loop theorem actually proved. A concrete valid-bracket witness shows
that fixed semantics returns `false` while the installed rule proves `true`.
This is a demonstrated false conclusion, not merely a missing justification.

The failure does not assert that `solution.py` is functionally wrong. It rejects
the submitted K proof theory because its result depends on a materially unsound
proof rule.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
mode/mount contradiction and no infrastructure breach.

I performed a recursive `lstat`-based comparison that checks relative paths,
entry types, symlinks, and SHA-256 content without following candidate links.
The trusted and candidate semantics trees each contain 26 entries; the
comparison reports zero missing, extra, mistyped, symlinked, or
content-mismatched entries. `/candidate/prompt.py` and
`/candidate/py2mpy.py` are byte-identical to their trusted counterparts.
Commands and results are in:

- `evidence/tree_integrity.py`
- `evidence/stage1_provenance.sh`
- `evidence/stage1_provenance.log`

The candidate's proof and program source artifacts (`solution.py`,
`solution.mpy`, `spec.k`, and `verification.k`) are ordinary files, not
symlinks. Candidate-built `__pycache__` content was not copied or used.
All executable source was copied to
`/tmp/audit-work/132-is-nested/source`, using the trusted reference semantics
tree rather than any candidate build product.

### Missing provenance artifacts

The following requested candidate artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was found. No candidate `PROOF.md` or
`spec-vacuity.k` was present either. These omissions remove provenance evidence,
but they did not prevent an independent source-level reconstruction and are not
being converted into an infrastructure error.

**Stage 1 result:** semantics and source integrity pass; generation provenance is
incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt admits finite strings containing only `[` and `]`. The
function must return `True` exactly when the string contains a nested pair as a
subsequence: equivalently, there are positions `i < j < k < l` whose characters
are `[[ ]]`.

The trusted canonical implementation collects opening positions in ascending
order and closing positions in descending order. Reaching `cnt >= 2` means two
opening indices can be matched with two later, distinct closing indices; this is
equivalent to the four-position nested subsequence above.

The submitted implementation is a saturated five-state automaton:

- states 0–2 record up to two observed openings;
- states 2–4 record up to two later closings;
- it returns true exactly at state 4.

On the stated bracket-only domain, its use of `else` is equivalent to testing
for `]`.

### Trusted translation

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced a byte-identical `solution.mpy`. Both files have SHA-256:

`2ae25652f4b8334470ad0f669458c35757c408e5fd85fe6219197da365bf9c9c`.

See `evidence/stage2_fidelity.sh` and
`evidence/stage2_fidelity.log`.

### Independent differential test

`evidence/differential.py` imports the trusted canonical function and the
scratch generated function independently. It checks:

- all six documented examples;
- empty, one-character, minimal-true, saturation, and long boundary inputs;
- every one of the `2^0 + ... + 2^12 = 8,191` bracket strings through length 12;
- 1,000 deterministic generated strings of lengths 13 through 80;
- all six branch outcomes in the generated automaton.

After deduplication, 9,193 distinct inputs were compared. The mismatch count was
zero, both functions always returned actual booleans, and every branch boundary
was exercised. Two additional length-10,000 boundary strings were included.
The exact scope and results are in `evidence/stage2_fidelity.log`.

This is finite adequacy evidence, not a substitute for a K proof.

**Stage 2 result:** pass on the intended input domain.

## 3. Clean proof reconstruction

K 7.1.337 was available. No candidate definition, cache, trace, or claimed
`#Top` was reused.

### Fresh definitions and concrete execution

From `/tmp/audit-work/132-is-nested/source`:

1. The trusted supplied semantics was compiled with the LLVM backend as
   `runtime-kompiled` (exit 0).
2. `concrete_tests.py` was regenerated with the trusted translator; it was
   byte-identical to the submitted `concrete_tests.mpy`.
3. The regenerated tests ran to `.K` with `NoExc` and exit code 0.
4. `verification.k` was compiled with the Haskell backend first without and
   then with the installed loop lemma (both exit 0).

Evidence:

- `evidence/stage3_runtime_build.log`
- `evidence/stage3_concrete_tests.log`
- `evidence/stage3_concrete_regeneration.log`
- `evidence/stage3_base_build.log`
- `evidence/stage3_lemma_build.log`

Compiler warnings concern unused variables in `strLt`; the LLVM build also
reports the supplied total `valSeqAt` abstraction as non-exhaustive. None is on
this program's execution path.

### Independent positive claim results

Every target was rerun separately with its fully qualified compiled label:

| Claim | Definition | Exit | Result | Evidence |
|---|---|---:|---|---|
| `IS-NESTED-LOOP-SPEC.scan-loop` | base verification | 0 | `#Top` | `evidence/stage3_scan_loop.log` |
| `IS-NESTED-TOP-SPEC.empty-input` | with loop lemma | 0 | `#Top` | `evidence/stage3_empty_input.log` |
| `IS-NESTED-TOP-SPEC.all-bracket-strings` | with loop lemma | 0 | `#Top` | `evidence/stage3_all_bracket_strings.log` |
| both top claims together | with loop lemma | 0 | `#Top` | `evidence/stage3_all_top_claims.log` |

The first attempt used short filtering labels; this K version rejected those
three commands at exit 113 as unused labels. Those administrative failures are
preserved in `evidence/stage3_reconstruct.log` and the
`stage3_*_short_label.log` files. The labels were recovered from the compiled
spec and the claims were then rerun successfully. No timeout occurred, and the
short-label errors are not treated as proof failures or successes.

**Stage 3 result:** verification closure reproduced. This establishes closure
under the candidate-extended theory; static soundness remains a separate gate.

## 4. Adequacy and real-program pinning

### Claim meanings

`scan-loop` starts at the real loop head inside a one-argument function call.
The callee scope contains integer `state = I`, arbitrary `char` and `string`
values, the module and builtins scopes are fixed, the heap is empty, and the
call frame and continuation are exact. Its precondition is `0 <= I <= 4`. It
claims that the remaining loop, the function return, and call-frame pop produce
the boolean `scanState(I, BS) == 4` and restore caller state.

`empty-input` starts a call to `is_nested` in the exact post-module-load scope
and claims the empty bracket encoding returns `false`.

`all-bracket-strings` starts the same call for an arbitrary finite `BSeq` and
claims the return equals `nested(BS)`, which reduces to
`scanState(0, BS) == 4`.

The postconditions are result-constraining: `scanState` has exhaustive,
structurally recursive equations, and `nested` is not a free result symbol.

### Program identity

The entry `<k>` cells call a manually installed `isNestedClosure`; they do not
load a filename dynamically. This factoring is nevertheless pinned to the
current submitted program:

- the trusted translator regenerates `solution.mpy` byte-for-byte;
- `scanBody` is exactly the translated `For` body;
- `isNestedBody` is exactly the translated assignment, loop, and return
  sequence;
- `isNestedClosure` has exactly the submitted parameter list, body, and module
  environment;
- the entry scope is exactly the state produced after loading this
  one-definition module.

The compiled stuck-state output in `evidence/stage6_vacuity_proof.log` also
prints the fully expanded closure, allowing this correspondence to be checked
against `solution.mpy`.

### Satisfying ground states

`evidence/spec-witness.k` and `evidence/stage4_witness.log` exhibit and prove:

- the loop precondition with `I = 0`, `BS = bNil`, and a fully concrete legal
  frame, yielding `false`;
- the empty entry configuration, yielding `false`;
- the universal entry configuration instantiated with `[[]]`, yielding `true`.

The same inputs were evaluated by an independent Python summary, the trusted
canonical implementation, and the submitted implementation. All agree.

**Stage 4 result:** the claims are satisfiable, result-bearing, and accurately
factor the submitted function. The natural-language meaning of `nested` is
still an informal mathematical bridge, supported by the differential evidence.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.md`, generated by
`evidence/inventory_k.py`, inventories every source-level configuration,
syntax statement, rule, claim, and evaluation context in the clean supplied
semantics, `verification.k`, and `spec.k`. It contains 953 items:

- 708 rules, of which 46 have priority and 662 are ordinary non-priority rules;
- 236 syntax statements;
- 153 function-bearing declarations and 111 total declarations;
- 22 opaque/no-evaluator declarations;
- 26 `owise` rules;
- five evaluation contexts;
- one configuration and three claims;
- zero local `simplification` rules and zero `functional`-attribute
  declarations.

Each item includes exact source, module, attributes/class, and disposition.
The supplied-semantics items are exact trusted baseline items. The 22 opaque
baseline operations (float, sort, and similar operations) are not reachable
from this program or its claims. The candidate introduces no opaque
result-bearing proof symbol.

`evidence/used_construct_map.md` maps every submitted syntax form to its
declaration and execution rules and records the complete cell footprint.
Evaluation is left-to-right; function calls allocate and pop one scope and one
stack frame; lookup follows local, module, then builtins scopes; iteration is in
source order; assignment updates only the callee scope; no heap allocation,
exception, or exit-code change occurs on the claimed domain.

### Candidate-local declarations and rules

The factored program-body equations are exact and terminating.
`openStep` and `closeStep` implement the actual branch guards.
`scanState` recurses strictly on `BSeq`, has disjoint constructor equations, and
preserves the `0..4` state invariant. `nested` is a truthful name for the
automaton's accepting condition.

The three `bCodes` iterator rules are a conservative lazy input encoding:
`bOpen` yields code 91, `bClose` yields code 93, and `bNil` ends iteration.
They affect only `k` and agree with native string iteration for all finite
constructor terms by structural reasoning. The candidate supplies no
bridge-free universal K connection theorem from this lazy representation to
native `iCons` strings. Because no false case or overlap exists and the program
only iterates the input, I record this as an informal representation/intent
bridge rather than calling it unsound.

### Rejected operational rule: `proved-scan-loop`

The proved `scan-loop` claim fixes the complete remaining scopes to:

- scope 0 containing only `is_nested -> isNestedClosure`; and
- scope -1 equal to `builtinsScope`.

The installed rule replaces those fixed scopes with `_REST:Map`. That broadens
the operational bridge to arbitrary module and parent-scope bindings even
though the displaced loop performs dynamic lookup of `ord`. Priority 40 makes
the shortcut preempt ordinary loop execution. No theorem establishes the
bridge for that larger context.

This is not only an evidence gap. `evidence/bridge-witness.k` supplies a false
conclusion witness within the rule's declared domain:

- the input is the valid bracket string `[[]]`;
- state starts at 0 and every configuration cell is well-formed;
- scope 0 shadows `ord` with the existing builtin `len`;
- scope -1 remains the ordinary builtins scope.

Under fixed semantics, each `ord(char)` call therefore evaluates as
`len(char) = 1`; state never increments and execution terminates at `false`.
The base proof exits 1 with a `WarnStuckClaimState` whose final `<k>` cell is
`false`, while the destination requires `true`
(`evidence/stage5_bridge_base.log`).

Under the candidate's installed rule, the identical state proves exit-0
`#Top` (`evidence/stage5_bridge_extended.log`). The only change is importing
the module containing `proved-scan-loop`.

This witness uses an intended-domain bracket input and demonstrates a concrete
false result enabled by the rule. It establishes a binding-fidelity and context-
containment violation. Narrowing the rule back to the exact scopes of the
proved claim would remove this witness, but that is not the submitted rule.

**Stage 5 result:** fail. The extended theory contains a materially unsound
operational proof rule.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is preserved as
`evidence/spec-vacuity-audit.k`. It changes the universal result from
`nested(BS)` to `notBool nested(BS)`. For the satisfying input `BS = bNil`, both
Python implementations and the true summary return `false`, while the mutation
demands `true`; see `evidence/stage6_vacuity_witness.log`.

The mutated spec was first compiled with `kprove --dry-run` and emitted a
compiled JSON spec at exit 0 (`evidence/stage6_vacuity_build.log`). The actual
proof then exited 1 with `WarnStuckClaimState`; the residual explicitly reports
the failed equality between `scanState(0, BS) == 4` and its negation
(`evidence/stage6_vacuity_proof.log`). This is the expected unmet result
obligation, not a parser error, missing import, crash, or timeout.

**Stage 6 result:** pass. The entry claim is non-vacuous and discriminates a
false result. This does not cure the separate Stage 5 soundness failure.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the exact supplied semantics **plus all candidate rules**, K proves:

1. the stated generalized loop summary for the exact fixed loop-claim
   configuration;
2. the empty encoded string returns `false`; and
3. every finite proof-side `BSeq` input returns
   `scanState(0, BS) == 4`.

These are partial-correctness reachability claims. The successful output is not
a proof under only the supplied semantics because the entry definition imports
the rejected `proved-scan-loop` operational rule.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.337 parser/compiler/Haskell/LLVM backends and builtin Int/Bool/Map/List theories | All execution and proof results | Ordinary accepted toolchain boundary |
| Exact `/reference/reference-semantics` tree | Evaluation, calls, state, control, and results | Authoritative supplied-semantics boundary; integrity verified |
| Trusted `/reference/py2mpy.py` | Python-to-MPY program identity | Accepted trusted input; byte identity reproduced |
| `bCodes` lazy iteration rules | Which characters the symbolic input yields | Structurally truthful and finite; no universal K connection theorem to native strings |
| ASCII facts `ord('[')=91`, `ord(']')=93` | Branch selection | Matches supplied semantics and ordinary Python behavior |
| Manual closure factoring | Connection between entry claim and submitted module | Exact for the current one-function translated program; source and compiled expansion checked |
| `nested(BS)` versus the English nested-subsequence property | Human-facing intent | Informal mathematical argument plus finite differential evidence; not a separate K theorem |
| Trusted canonical implementation | Differential oracle on 9,193 inputs | Finite empirical support only |
| `proved-scan-loop` over `_REST:Map` | Entire loop, return value, and call-frame cleanup in entry proof | **Illegitimate:** false operational generalization with a machine-demonstrated counterexample |

No opaque float, sort, hash, allocation, or other supplied abstraction affects
this proof. Behavior for strings containing characters other than brackets is
outside the prompt and formal domain. The formal claim also does not state a
separate theorem that the automaton definition is equivalent to the English
subsequence predicate.

### Final rationale

The implementation appears correct, the positive claims reconstruct, and the
non-vacuity gate passes. Nevertheless, proof legitimacy requires every
contributing operational rule to be valid over its full match domain.
`proved-scan-loop` is not: the fixed-versus-extended witness establishes
`false` versus `true` on the same well-formed valid-bracket state. A successful
`#Top` obtained in a theory containing that false operational shortcut cannot
be accepted as the required legitimate proof.

There was no audit infrastructure failure: the semantics-mode mount was
consistent, tools were available, builds completed, and all decisive commands
terminated normally.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
