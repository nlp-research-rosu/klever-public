# Adversarial audit: 14-all-prefixes

The reconstructed K proof is legitimate for the requested return-value
property. It executes a K term that is independently pinned to the
trusted-translator output, proves a result-bearing loop invariant, and constrains
both the returned reference and its heap content. No proof-local operational
bridge, oracle, opaque result, or answer-encoding rule was found.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
auditability/model-bridge limitations:

1. `run-input.json`, `metrics.json`, `codex-last.txt`, and
   `codex-output.log` are absent, so the requested generation provenance cannot
   be audited.
2. The supplied semantics intentionally treats the unused
   `from typing import List` import as trivia and its concrete K string-literal
   path is ASCII-only. Neither limitation affects this function's returned
   prefixes, but both are real differences from unrestricted CPython execution.

All candidate material was treated as untrusted. `/candidate` was not modified.
The scratch reconstruction is
`/tmp/audit-work/proof-audit.Dl0nBZ/candidate`; reviewer-authored scripts,
mutations, inputs, and bounded logs are under
[`evidence/`](evidence/).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is
therefore no rendered-mode/mount contradiction and no infrastructure breach.

The following checks all exited 0:

```text
cmp /candidate/prompt.py /reference/prompt.py
cmp /candidate/py2mpy.py /reference/py2mpy.py
diff -qr --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
```

Neither semantics tree contains a symlink. The recursive comparison includes
all 24 supplied K source files; there are no missing, additional, changed,
mistyped, or symlinked entries inside the candidate's
`reference-semantics/`. The candidate prompt and translator are byte-identical
to their trusted mounted versions. Exact commands, statuses, inventory, and
hashes are in
[`01-integrity-fidelity.log`](evidence/01-integrity-fidelity.log), produced by
[`01-integrity-fidelity.sh`](evidence/01-integrity-fidelity.sh).

The required proof/program sources `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, and the recursively compared semantics are regular files.
The candidate also contains `prove.sh`, smoke files, and a Python bytecode
cache; none was trusted or reused.

### Missing provenance artifacts

The following requested files do not exist under `/candidate`:

```text
/candidate/run-input.json
/candidate/metrics.json
/candidate/codex-last.txt
/candidate/codex-output.log
```

No structured generation trace is present. Consequently there were no
candidate generation claims to credit or rebut. This is an evidence/provenance
defect, not a failure of the reconstructed reachability claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For every Python `str` value `s`, return all nonempty prefixes in increasing
length order:

```text
[s[:1], s[:2], ..., s[:len(s)]]
```

The empty string returns `[]`. This restatement follows
`/reference/prompt.py` and the loop in `/reference/canonical.py`.

The candidate uses:

```python
for end in range(1, len(string) + 1):
    prefixes.append(string[:end])
```

This differs syntactically from the canonical `range(len(string))` with
`string[:i+1]`, but has the same endpoints and ordering on the intended `str`
domain.

### Trusted translation identity

The submitted program was retransliterated in scratch with:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py \
  > /tmp/audit-work/proof-audit.Dl0nBZ/regenerated-solution.mpy
```

The command exited 0. `cmp` between that file and submitted `solution.mpy`
exited 0; both have SHA-256:

```text
98271db4e02d617f8a444f10b620c44eefe9021daa13c685cfe7db4ddc7418ca
```

Thus the submitted `.mpy` is exactly the trusted translation of the submitted
Python source.

### Independent differential reconstruction

[`02-differential.py`](evidence/02-differential.py) independently loads
`/reference/canonical.py` and the scratch copy of candidate `solution.py`. It
does not reuse K equations. It checked:

- the documented `"abc"` example;
- empty and length-one branch boundaries;
- fixed ASCII, NUL, whitespace, combining-character, BMP, and astral Unicode
  cases;
- every string of lengths 0 through 5 over
  `("a", "b", "é", "🙂")`; and
- 500 deterministically generated strings of lengths 0 through 80.

After deduplication, 1,860 inputs were evaluated with zero mismatches. The exact
deterministic corpus is
[`differential-inputs.json`](evidence/differential-inputs.json), the result is
[`differential-results.json`](evidence/differential-results.json), and the
command exited 0 in
[`02-differential.log`](evidence/02-differential.log).

This is finite evidence for the Python-to-intent bridge; it is not used as a
substitute for the K proof.

## 3. Clean proof reconstruction

No compiled candidate definition or cache was copied. Only source artifacts
were copied into the fresh scratch directory. K reported version
`v7.1.337`.

### Concrete definition and executions

The concrete definition was freshly built:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. `krun solution.mpy --definition runtime-kompiled` exited 0 with a
completed configuration. An independently translated ASCII assertion program
covering `""`, `"a"`, `"abc"`, and `"a b"` also exited 0; its final heap shows
the expected prefix lists.

A separate reviewer test containing the astral literal `"é🙂"` failed before
execution with K's scanner error:

```text
The surrogate code points in the range [U+D800, U+DFFF] are illegal
in Unicode escape sequences
```

That exact failure is preserved in
[`03-reconstruct.log`](evidence/03-reconstruct.log). It is not a candidate
result divergence: the positive claim receives the input directly as
`str(S:IntSeq)` and does not parse it through `Str(String)`. The successful
ASCII rerun and final heap are in
[`03b-followup.log`](evidence/03b-followup.log). The finite Python differential
test separately includes astral strings.

### Proof definition and positive claims

The proof definition was freshly built:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. The original candidate spec then ran exactly as submitted:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`.

The claims were also checked modularly with reviewer-added labels:

- `--claims loop` exited 0 and printed `#Top`.
- After that independent loop proof, an identical loop claim was marked
  `[trusted]` solely as the already-established modular dependency in
  `spec-entry-modular.k`; the entry proof exited 0 and printed `#Top`.

The successful loop command and status are in
[`03-reconstruct.log`](evidence/03-reconstruct.log); the modular entry command
and status are in
[`03b-followup.log`](evidence/03b-followup.log). Selecting `entry` while
removing its helper invariant causes unbounded symbolic loop unrolling and was
manually interrupted; that diagnostic is explicitly excluded from proof
evidence in
[`03-interruption-note.txt`](evidence/03-interruption-note.txt). The original
joint `#Top`, separate loop `#Top`, and dependent entry `#Top` provide the
required positive evidence.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

The loop claim assumes:

- `END <= STOP`;
- the current environment is scope `L`;
- that scope has `end = _PREV`, `prefixes = ref(H)`, and
  `string = str(S)`;
- heap location `H` contains `list(ACC)`; and
- the active computation is the real loop head
  `#loop(rangeObj(END, STOP, 1), Name("end"),
  allPrefixesLoopBody())`, followed by arbitrary continuation `CONT`.

It concludes that the loop reaches `CONT`, preserves the string and list
reference, may leave `end` at an unconstrained integer value, and changes the
list at `H` to:

```text
prefixesAcc(S, END, STOP, ACC)
```

That fold appends `S[:END]`, then `S[:END+1]`, through
`S[:STOP-1]`. Leaving the final loop variable unconstrained is sound and
irrelevant: no later source statement reads `end`.

At the very first source loop head, `end` has not yet been bound. The entry
proof therefore does not incorrectly apply this invariant there: the empty
range terminates directly, while a nonempty range executes the first iteration,
binds `end`, and only then reaches the invariant's shape. This matches the real
control flow.

A concrete satisfying loop state is:

```text
S = [97, 98]       ("ab")
END = 1
STOP = 3
ACC = []
L = H = 0
SC = HP = empty maps
PREV = 0
P = parent(-1)
CONT = .K
```

Its precondition `1 <= 3` is true, and the claimed heap content is
`["a", "ab"]`, equal to both Python implementations.

### Entry claim in plain language

For every algebraic integer sequence `S`, the entry claim starts from the
semantics' exact initial module state, loads `solutionModule()`, and invokes
`all_prefixes` with semantic string `str(S)`. It concludes:

- the returned value is exactly `ref(0)`;
- heap location 0 is exactly `list(allPrefixes(S))`;
- exactly one heap object was allocated (`heapLoc` becomes 1);
- the temporary call scope was removed (`scopeLoc` returns to 1);
- the module scope contains the exact function closure;
- stack and return state are restored; and
- no modeled exception or nonzero exit occurred.

The returned value is therefore not free and the postcondition is not an
implication or tautology. It fixes both object identity in the K heap and every
element of the returned list.

There is no additional logical precondition beyond `S:IntSeq`. Satisfying
ground substitutions for `""`, `"abc"`, and `"é🙂"` produce respectively
`[]`, `["a","ab","abc"]`, and `["é","é🙂"]`; the formal fold, trusted
canonical, and candidate Python results all agree. Exact states and results are
in [`06-adequacy.log`](evidence/06-adequacy.log).

### Pinning the submitted program

Pinning has three independent parts:

1. Trusted retransliteration is byte-identical to submitted `solution.mpy`
   (Stage 2).
2. `allPrefixesLoopBody`, `allPrefixesBody`, `allPrefixesDef`, and
   `solutionModule` expand structurally to that same translated AST. They do not
   summarize or replace the execution.
3. Reviewer claim
   [`program-pinning.k`](evidence/program-pinning.k) loads
   `solutionModule()` and requires the installed closure to contain the explicit
   submitted body. It exited 0 and printed `#Top` in
   [`06-adequacy.log`](evidence/06-adequacy.log).

The proof does not dynamically read `solution.mpy`; it uses an exact
constructor copy. The independent byte comparison and explicit load claim close
that otherwise manual identity bridge for the submitted artifact.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule-inventory.tsv`](evidence/rule-inventory.tsv) is the exhaustive inventory
of the 24 fixed-semantics files plus `verification.k` and `spec.k`. Every row
records source file and line, normalized full declaration/rule text (including
guards and attributes), kind, path role, decision, and rationale. It was
generated by
[`05-build-rule-inventory.py`](evidence/05-build-rule-inventory.py); the command
and hash are in
[`05-rule-inventory.log`](evidence/05-rule-inventory.log).

Inventory totals:

| Category | Count |
|---|---:|
| Syntax declarations | 233 |
| Ordinary semantic/proof rules | 702 |
| Context declarations | 5 |
| Configurations | 1 |
| Reachability claims | 2 |
| Total inventoried items | 943 |
| `[function]` declarations | 151 |
| `[total]` declarations | 111 |
| Symbol declarations | 25 |
| `[no-evaluators]` declarations | 22 |
| Rules with priorities | 45 |
| `[concrete]` rules | 35 |
| `[owise]` rules | 26 |
| Simplification/simplifier rules | 0 |
| `[functional]` declarations | 0 |

Role decisions in the TSV are:

- 182 fixed-semantics items on the real execution/proof path:
  `ACCEPT_REVIEWED`;
- 746 fixed-semantics items outside this program's construct/value path:
  `ACCEPT_OUT_OF_PATH` or `ACCEPT_UNUSED_OPAQUE`;
- 13 proof-local declarations/rules: `ACCEPT_REVIEWED`; and
- 2 target claims: `ACCEPT_REVIEWED`.

For out-of-path fixed rules, the decision is deliberately limited: they are
byte-identical members of the selected supplied semantics and do not contribute
a rewrite, branch, value, or assumption to these claims. This audit does not
claim that the supplied MiniPython subset is a complete semantics of all
Python.

### Construct-to-semantics map

| Submitted construct | Fixed declarations and rules used | Review |
|---|---|---|
| `Module`, `ImportFrom`, statement sequence | `syntax.k`; `core.k` `#loadAll`/sequence; `controls.k` import rules | The module loads in source order. The `typing` import is modeled as no-op; see the witnessed limitation below. |
| `FuncDef`, call, parameter, return | `functions.k` frame/bind/return/pop; `call.k` callee/argument/closure rules | Binding selects the loaded closure, arguments evaluate left-to-right, the call scope is allocated then removed, heap objects escape, and return discards only the callee continuation as Python return should. |
| Docstring expression | `str.k` ASCII `Str` conversion; `controls.k` `Expr(Val)` | The actual docstring is ASCII and is evaluated then discarded without state effects. |
| `prefixes = []` | strict assignment, `list.k` literal evaluation, `core.k` allocation | Allocates exactly heap location 0 and binds `prefixes` to `ref(0)`. |
| `len(string) + 1` | lookup/call rules; `builtins.k` `len`; `core.k` `isLen`; `int.k` addition | Exact length and unbounded-integer addition; no result abstraction. |
| `range(1, stop)` and `for` | `builtins.k` range constructor; `range.k` iterator; `controls.k` `For/#loop/#loopStep` | Step is fixed at 1, endpoint is exclusive, target binding occurs before the body, and the continuation returns to the next loop head. |
| `string[:end]` | `subscript.k` ordered bound evaluation, `doSlice`, slice-index helpers, `buildIS` | With no lower/step bounds, this builds exactly the first `end` sequence elements, clamped to the string length. |
| `prefixes.append(...)` | attribute/call routing; `list.k` priority-40 append and `valSeqConcat` | Receiver remains the heap reference and the rule performs the exact in-place append at that heap location. |
| `return prefixes` | name lookup and frame-pop rules | Returns `ref(0)`, restores caller control cells, deletes the temporary scope, and retains the heap list. |

The used strictness/context declarations enforce the source evaluation order.
The only applicable result-bearing priority rule is the exact mutating append
rule. Cell-variable assignment priorities have false guards in this plain
function frame; ref/list-slice priorities do not match the semantic string
slice. All 45 priorities and their guards are individually listed in the TSV.

### Proof-local inventory and decisions

| Local extension | Class and decision |
|---|---|
| `prefixesAcc` declaration and two equations | Definitional mathematical summary, not an operational bridge. Guards `END < STOP` and `END >= STOP` are disjoint and exhaustive over integers. The recursive case increases `END`, strictly decreasing `STOP-END`; the base returns `ACC`. It uses fixed `doSlice` and `valSeqConcat` exactly as the body does. Accepted. |
| `allPrefixes` declaration/equation | Definitional name for `prefixesAcc(S,1,isLen(S)+1,.ValSeq)`. This is the exact source range. Accepted. |
| `allPrefixesLoopBody` declaration/equation | Ground structural constructor for the submitted append/slice body. Its single equation covers its only nullary argument. Accepted. |
| `allPrefixesBody` declaration/equation | Ground structural constructor for the complete submitted body, including docstring, allocation, loop, and return. Accepted. |
| `allPrefixesDef` declaration/equation | Ground structural constructor for the submitted definition and parameter. Accepted. |
| `solutionModule` declaration/equation | Ground structural constructor for the submitted import and function. Accepted. |

The four nullary structural constructors are `[function,total]` with one
nonoverlapping equation each. `prefixesAcc` and `allPrefixes` are functions but
not falsely declared total. No proof-local rule has `priority`,
`simplification`, `concrete`, `owise`, opacity, or a fresh unconstrained value.
No local rule matches `<k>` or bypasses source execution.

### Opaque and total symbols

The 25 supplied opaque symbol declarations are `md5hexCodes`; the float-family
symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
`toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`; and `sortVS`/`sortKeyVS`. Every one is classified
`FIXED_UNUSED` in the inventory. No reachable term, branch, state update,
summary, or postcondition contains one. They have no dependent claim here.

Relevant total functions (`isLen`, list concatenation, range test, and the
positive-step slice helpers) have constructor-decreasing or closed arithmetic
equations on the used domain. Their guards are disjoint on the instantiated
path. No overlap was found that gives different right-hand sides.

### Concrete modeling divergence witness

The used supplied rule at `semantics/controls.k:36` treats every non-`math`
`ImportFrom` as a no-op. That is not full-state CPython behavior. A concrete
witness is the actual submitted module: CPython binds global `List` to
`typing.List` and records evaluated function annotations, while the K final
module scope contains only `all_prefixes`. The witness command exited 0 in
[`07-import-model-witness.log`](evidence/07-import-model-witness.log), and the
corresponding K scope is in
[`03-reconstruct.log`](evidence/03-reconstruct.log).

This is not hidden or proof-local, and it cannot enable a false prefix-list
result on the intended domain: neither `List` nor the annotations are read by
the function body, and both Python implementations plus concrete K executions
agree on the result. It is therefore recorded as a language/state adequacy
concern, not as a materially unsound correctness rule for this theorem.

No proof-local or used result-bearing rule was labeled unsound. Accordingly
there is no missing false-conclusion witness for an asserted proof-rule
unsoundness.

## 6. Fresh non-vacuity test

The reviewer-created
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) changes the entry
postcondition to prepend the empty string to the returned list:

```text
list(vCons(str(.IntSeq), allPrefixes(S)))
```

The satisfying input `S = .IntSeq` corresponds to Python `""`. Both trusted
canonical and candidate Python return `[]`; the mutation requires `[""]`.
[`04-vacuity-witness.py`](evidence/04-vacuity-witness.py) records this ground
witness.

The mutation dry run exited 0, so it parsed and built successfully. The actual
proof exited 1 with `WarnStuckClaimState`; the residual contains the real final
heap `0 |-> list(.ValSeq)`, which cannot unify with the false destination. It
then reports:

```text
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
```

The script recognized this as `EXPECTED_NON_VACUITY_REJECTION`. Exact commands,
statuses, and residual are in
[`04-vacuity.log`](evidence/04-vacuity.log). The mutation used the separately
proved loop claim only as its established modular dependency, so the failure is
the intended false result obligation rather than a missing invariant or parser
error.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied `MPY` semantics, for every finite `IntSeq` value `S`, from
the exact initial configuration:

1. the exact translated module is loaded;
2. the exact submitted `all_prefixes` body is called with `str(S)`;
3. the loop's in-place list updates produce
   `prefixesAcc(S,1,isLen(S)+1,.ValSeq)`;
4. execution returns `ref(0)`;
5. heap location 0 contains exactly that value sequence; and
6. the modeled stack, return, scope-allocation, exception, and exit cells have
   the claimed final values.

The proof is a partial-correctness reachability proof using the loop claim as a
circularity. It does not rely on differential tests for closure. The program
also operationally terminates for each finite sequence because the range step
is positive and the remaining distance decreases, but no stronger external
termination theorem is claimed here.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 frontend, Haskell prover, LLVM runner, and builtin Int/Bool/String/Map/List theories | All machine-checked evidence | Ordinary K trusted computing base. Fresh builds and a rejecting mutation reduce, but cannot eliminate, implementation trust. |
| Byte-identical supplied semantics | All source execution and cell behavior | Required selected semantics. Used rules were manually traced. The non-result import-state abstraction and concrete astral-literal limitation are documented. |
| Trusted `/reference/py2mpy.py` | Python-to-`.mpy` identity | Trusted input by audit authority; byte identity proves the submitted translation matches it. |
| `doSlice`, `isLen`, range iteration, allocation, call, and append equations | Formal result | Defined fixed-semantics rules, not opaque primitives. Their used cases were reviewed for guards, descent, state, and control. |
| 25 opaque float/digest/sort symbols | None | Unreachable and absent from both claims and all proof-local summaries; acceptable for this theorem only. |
| Mathematical reading of `IntSeq` as a Python character sequence | Intent bridge | Prefix slicing is representation-parametric. Checked on ASCII/BMP/astral ground substitutions and 1,860 Python cases, but this finite evidence is not a universal theorem about every CPython Unicode implementation detail. |
| CPython canonical implementation and differential corpus | Intent/fidelity support only | Independent finite oracle; never imported by K and not a proof axiom. |
| Separately proved loop invariant | Entry claim | Not ultimately assumed: the original joint run and loop-only run both print `#Top`; `[trusted]` appears only in the reviewer modular entry and mutation specs to reuse that established claim. |
| Candidate generation provenance | None | Four requested provenance files are missing. No proof conclusion relies on their contents, but auditability is reduced. |

### Gate summary

- Real-program soundness: **pass** under the selected supplied semantics. The
  submitted body executes, proof-local summaries are definitional, the result
  is fixed, and the false mutation is rejected.
- Intent adequacy: **pass for the requested prefix-list result**, with the
  documented non-result import/global-state and concrete string-literal
  limitations.
- Trust/evidence auditability: **concern** because the requested generation
  provenance artifacts are absent. The proof, reconstruction, inventory,
  differential corpus, satisfying witnesses, and mutation are otherwise
  reproducible from preserved artifacts.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
