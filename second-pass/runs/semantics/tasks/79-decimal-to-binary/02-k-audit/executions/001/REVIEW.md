# Independent adversarial audit: 79-decimal-to-binary

This audit used the required `using-kit` then `validating-proof` workflow. I
treated every file under `/candidate` as untrusted, kept it read-only, copied
source inputs to `/tmp/audit-work/79-decimal-to-binary`, and rebuilt all K
definitions there. Reviewer-authored artifacts and bounded command logs are in
`/audit-output/evidence`.

The candidate is legitimate, with concerns. The positive claim reconstructs,
constrains the exact returned string, and executes the exact submitted function
body. The proof-local slice rule is a true pure sequence identity and I found no
false conclusion witness. The concern is evidentiary: the candidate supplies no
bridge-free universal K theorem for that rule, and my fresh universal
bridge-free claim remains stuck on the supplied semantics' abstract-tail
representation. Ground fixed-semantics connections, an opposite-result
rejection, and a direct mathematical derivation support the rule, but they do
not replace that missing universal machine-checked connection theorem.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the required trusted tree
`/reference/reference-semantics` is present. There is no infrastructure-mode
contradiction.

`evidence/check_provenance.sh` recursively compared the candidate and trusted
semantics trees with `diff -r --no-dereference`. The command exited 0:

- every relative entry is present on both sides;
- there are no additional, missing, mistyped, or changed semantics entries;
- every semantics entry has the expected regular-file or directory type;
- there are no symlinks anywhere in `/candidate`.

The candidate `prompt.py` is byte-identical to `/reference/prompt.py`, and the
candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Exact checks,
entry types, and results are in `evidence/01-provenance.log`; source hashes are
in `evidence/20-source-hashes.log`.

### Present and missing artifacts

The proof-critical artifacts are present as regular files:

- `solution.py`
- `solution.mpy`
- `spec.k`
- `verification.k`
- `prompt.py`
- `py2mpy.py`
- `reference-semantics/semantics.k` and all required helper K files

The following requested generation-evidence artifacts are missing and therefore
could not be read even as untrusted claims:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any structured generation trace (`*trace*` or `*.jsonl`)

This is an auditability limitation, not a substitute for or a failure of the
fresh reconstruction. The candidate also contains optional `smoke.py`,
`smoke.mpy`, and `prove.sh` files plus an untrusted
`__pycache__/solution.cpython-310.pyc`; the cache was ignored. There is no
candidate `PROOF.md` or candidate vacuity artifact to rely on.

The trusted-input/semantics integrity check found zero integrity failures.

Evidence:

- `evidence/check_provenance.sh`
- `evidence/01-provenance.log`
- `evidence/19-tool-versions.log`
- `evidence/20-source-hashes.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a nonnegative integer written in decimal form, return its ordinary base-2
digits as a string, with `"db"` immediately before and after the digit string.
The payload must be nonempty and contain only `"0"` and `"1"`. Thus 15 maps to
`"db1111db"` and 32 maps to `"db100000db"`.

The trusted canonical implementation is:

```python
return "db" + bin(decimal)[2:] + "db"
```

The submitted `solution.py` has exactly that executable body. The prompt does
not explicitly say “nonnegative,” while the formal claim requires `N >=Int 0`.
For negative Python integers, the canonical implementation itself produces a
payload beginning with `"b"` after slicing (for example, `-1` gives
`"dbb1db"`), which conflicts with the prompt's binary-character condition.
Accordingly, the formal nonnegative domain is the coherent intended domain, but
the prompt's omission is noted as a scope ambiguity.

### Trusted translation

I regenerated the MiniPython AST using the trusted mounted translator:

```text
python3 /tmp/audit-work/79-decimal-to-binary/trusted-py2mpy.py \
  /tmp/audit-work/79-decimal-to-binary/solution.py \
  > /tmp/audit-work/79-decimal-to-binary/solution.regenerated.mpy
cmp /tmp/audit-work/79-decimal-to-binary/solution.regenerated.mpy \
  /tmp/audit-work/79-decimal-to-binary/solution.mpy
```

The translator and `cmp` both exited 0. The regenerated AST is byte-identical
to the submitted `solution.mpy`. See
`evidence/regenerate_and_compare.sh` and
`evidence/02-translation-identity.log`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the copied generated entry point. It exercised:

- documented values 15 and 32;
- zero, one, and the `N = 0`/`N > 0` formal branch boundary;
- values immediately below, at, and above every power of two from
  \(2^1\) through \(2^{128}\);
- 512 deterministic generated nonnegative integers up to 1024 bits
  (seed `790079`);
- nine informational out-of-domain values, including negative integers,
  `None`, the empty string, the empty list, booleans, and a float.

There were 902 intended-domain cases, 911 total cases, zero canonical
divergences, and zero valid-output shape failures. Inputs and results are
preserved in `evidence/differential_inputs.json`,
`evidence/differential_results.json`, and
`evidence/03-differential.log`.

Finite differential testing supports program/canonical fidelity; it is not the
K proof.

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied. I built fresh LLVM and
Haskell definitions from the scratch source copy using K v7.1.337.

### Concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit: 0. Log: `evidence/04-kompile-runtime.log`.

The submitted module parsed and ran:

```text
krun solution.mpy --definition runtime-kompiled --output none
```

Exit: 0. Log: `evidence/05-krun-solution.log`.

The fresh concrete smoke program tested 0, 1, 15, 32, and 103. It terminated
with `.K`, `NoExc`, and exit code 0:

```text
krun smoke.mpy --definition runtime-kompiled --output pretty
```

Exit: 0. Log: `evidence/06-krun-smoke.log`.

### Proof definition and every positive target claim

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit: 0. Log: `evidence/07-kompile-proof.log`.

`spec.k` contains exactly one positive target claim,
`decimal-to-binary-correct`. I ran it independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --output pretty
```

Output: `#Top`. Exit: 0. Log:
`evidence/08-kprove-positive.log`.

### Independent full-module reconstruction claim

The candidate entry helper embeds the function closure directly. To test
whether that pins the actual module, I authored
`evidence/spec-real-program.k`, whose initial `<k>` cell loads the full
submitted `Module(FuncDef(...))` AST and then calls
`Name("decimal_to_binary")`.

My first version deliberately expected the post-state module scope to be empty.
It failed after reaching the correct result because real module loading
correctly retains the function binding (`evidence/09-kprove-real-program.log`).
After retaining that exact binding in the post-state, the full-module symbolic
claim produced `#Top` and exit 0:

```text
kprove spec-real-program.k --definition verification-kompiled \
  --spec-module SPEC-REAL-PROGRAM --output pretty
```

Log: `evidence/10-kprove-real-program-correct-state.log`.

This extra auditor claim is not used to replace the candidate claim. It
independently confirms that the embedded closure has the same parameter,
definition environment, body, return result, and call behavior as the full
submitted AST. The only state difference is the expected module-level function
binding created by actually loading the module.

The builds emitted supplied-semantics warnings discussed in stage 5. None was a
build or proof failure.

## 4. Adequacy and real-program pinning

### Entry precondition

The sole entry claim starts with:

- an arbitrary K integer `N` satisfying `N >=Int 0`;
- `<k> #runDecimalToBinary(N) </k>`;
- module environment location 0;
- an empty module scope whose parent is the supplied builtins scope at -1;
- empty heap and stack;
- allocation counters at their initial values;
- `noRet`, `NoExc`, and exit code 0.

This is satisfiable. For example, `N = 0` with the exact displayed cells is a
concrete satisfying state.

### Entry postcondition

The claim requires `<k>` to become exactly:

```text
str(iCons(100,
    iCons(98,
      seqConcat(binCodes(N),
        iCons(100, iCons(98, .IntSeq))))))
```

That is the code-point sequence `"db" ++ binCodes(N) ++ "db"`. It is not a
free result variable, a tautology, or a one-way implication. All other cells
are constrained to be restored exactly to the entry values.

`evidence/claim_witnesses.py` independently modeled the `binCodes` equations,
used Python `format(N, "b")` as a separate mathematical oracle, and compared
the formal RHS, trusted canonical, and generated Python results for:

```text
0, 1, 2, 15, 32, 103, 2^128 - 1, 2^128
```

All eight inputs satisfy the precondition and all four results agree. See
`evidence/11-claim-witnesses.log`.

### Actual control flow and body pinning

`#runDecimalToBinary` rewrites to a call of:

- parameter list exactly `"decimal"`;
- definition environment exactly 0;
- the exact translated `Return(BinOp("+", BinOp("+", Str("db"),
  Subscript(Call(Name("bin"), Name("decimal")),
  Slice(Int(2), NoBound, NoBound))), Str("db")))` body.

That body is byte-pinned to `solution.mpy` by the trusted translation check and
was also exercised through full module loading in the auditor claim above.
The normal call machinery allocates a temporary local scope, binds `decimal`,
resolves `bin` through the builtins parent, evaluates both string additions
left-to-right, evaluates the slice bounds in order, returns, pops the frame,
deallocates the temporary scope, and restores every displayed cell.

There is no loop and no auxiliary loop claim. The only helper affecting the
body is the slice equation reviewed in stage 5.

Adequacy result: the formal claim constrains the intended function result and
pins the real submitted body on the coherent nonnegative domain. The direct
entry harness does not model the persistent function name binding created by
module import; that state is irrelevant to the requested pure function result,
and the full-module claim explicitly checks the exact difference.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k-rule-inventory.tsv` lists every local `syntax`, `configuration`,
`context`, `rule`, and `claim` statement in the supplied semantics helpers,
`verification.k`, and `spec.k`, with source file, line, attributes, provenance,
and normalized full statement. `evidence/k-rule-review.tsv` adds a local
reachability classification and a disposition to every row. The generating
script is `evidence/k_inventory.py`.

The exhaustive totals are:

| Item | Count |
|---|---:|
| Files reviewed | 26 |
| Inventoried statements | 932 |
| Ordinary rules | 697 |
| Syntax declarations | 228 |
| Contexts | 5 |
| Configurations | 1 |
| Claims | 1 |
| Statements carrying `function` | 145 |
| Statements carrying `total` | 107 |
| Statements carrying `concrete` | 35 |
| Symbol declarations | 25 |
| `no-evaluators` declarations | 22 |
| Priority-bearing statements | 46 |
| `owise` statements | 26 |
| Functional declarations | 0 |
| Simplification rules | 0 |

Per-file rule/syntax/context counts are in
`evidence/k-rule-inventory-summary.txt` and
`evidence/12c-k-inventory.log`. Of the 932 statements, 83 are reachable or
result-defining for this theorem, three are proof-critical local declarations
or rules, one is the entry claim, and 845 belong only to fixed supplied
semantics that cannot be reached from this submitted AST and entry
configuration.

The top-level `reference-semantics/semantics.k` is an import/module assembler
and contains no local syntax or rewrite rules. Its complete module graph was
inspected. All helper K files are represented in the inventory.

### Mapping every submitted construct

| Submitted construct | Declaration and governing semantics |
|---|---|
| `Module`, statement list | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef`, `Params`, parameter name | `syntax.k:41,57,60`; `functions.k:14` |
| `Return` | `syntax.k:41` strictness; `functions.k:78,85` |
| `BinOp("+", ...)` | `syntax.k:9` `seqstrict(2,3)`; `operators.k:12`; `str.k:24` |
| `Str("db")` | `syntax.k:9`; `str.k:13-17` |
| `Call` and argument list | `syntax.k:9,37`; `call.k:19-21,31,69`; `core.k:185-191` |
| `Name("decimal")`, `Name("bin")` | `syntax.k:9`; `core.k:130-158` |
| `Subscript(..., Slice(...))` | `syntax.k:9,38-39`; `subscript.k:27-28,44-69` |
| `Int(2)`, `NoBound` | `syntax.k:9,39`; `core.k:194`; `subscript.k:49-56` |
| string concatenation result | `str.k:20-24` |
| nonnegative `bin` | `builtins.k:17,108,114-121`; `int.k:19-20` |

All exact rows and full statements are in
`evidence/k-rule-review.tsv`.

### Configuration, order, calls, state, and guards

- The configuration cells in `core.k:49-60` match every entry cell.
- `BinOp` is sequentially strict left-to-right; `Return` is strict; call
  arguments use the shared left-to-right `#evalArgs` loop; the slice object and
  three bounds are evaluated in Python order.
- The direct closure call pins definition environment 0. The parameter is
  bound in a fresh local frame. `decimal` resolves locally; `bin` falls through
  to the fixed builtins scope.
- Strings are immutable `str(IntSeq)` values. This program performs no heap
  allocation. Function call scope and stack effects are undone by `#pop`.
- `N >=Int 0` selects the nonnegative `bin` rule. `binCodes(0)` and
  `binCodes(N > 0)` are disjoint; `binAcc` decreases by integer division by two
  and emits code 48 or 49 from the remainder.
- `seqConcat` equations are disjoint by `.IntSeq` versus `iCons` and descend on
  the first sequence.
- The fixed semantics has no reachable exception for an integer `N >= 0`.
  `bin(N)` always starts with code points 48, 98 and at least one digit, so the
  slice starting at two is in range.

### Candidate proof extensions

There are exactly two local rewrite rules and one local syntax declaration.

#### `#runDecimalToBinary(Int)`

Classification: exact entry harness.

The rule does not summarize or replace the property-bearing computation. It
constructs the exact translated closure and then routes through ordinary call,
lookup, builtin, slice, addition, return, and frame rules. Its syntax is unique,
so there is no overlap. It changes no cell directly. Trusted translation
identity and the fresh full-module symbolic claim establish body and binding
sensitivity.

#### `doSlice(str(iCons(FIRST, iCons(SECOND, REST))), someB(2), noB, noB)`

Classification: pure operational/equational bridge for fixed string slicing.

The rule rewrites the result to `str(REST)` at priority 40. Its complete match
domain is:

- a string with at least two code points;
- lower bound exactly 2;
- absent upper bound;
- absent step.

It has no `<k>` or cell pattern, introduces no abrupt control, changes no
environment, heap, stack, allocation, exception, or return state, and can be
used in any expression context because `doSlice` is a pure function. Its only
overlap is the supplied general `doSlice(str(...), ...)` equation. On this
domain, the right-hand sides agree.

Direct derivation from the supplied rules:

1. `isLen(iCons(FIRST, iCons(SECOND, REST)))` is
   `2 + isLen(REST)`.
2. The default step is 1 and the default stop is the full length.
3. The normalized start is 2.
4. `buildIS` therefore emits exactly positions 2 through length minus one,
   which are precisely `REST`. The empty-tail case stops immediately; the
   nonempty case follows by structural induction on `REST`.

This rule does not mention `binCodes`, the function name, or the requested
postcondition. It removes the fixed `"0b"` prefix from whatever tail the
supplied `bin` rule produced; it does not encode or fabricate the binary digits.

Independent bridge evidence:

- A separately compiled, bridge-free `MPY` definition closed fixed-semantics
  claims for empty, one-element, and three-element tails:
  `evidence/13-kompile-fixed-proof.log`,
  `evidence/slice-ground.k`, and
  `evidence/14b-kprove-slice-ground-fixed.log`.
- The same ground claims close with the extension:
  `evidence/16-kprove-slice-ground-extended.log`.
- An opposite interpretation claiming that a one-element tail becomes empty
  exits 1 and leaves the actual `str(iCons(67,.IntSeq))` residual:
  `evidence/slice-wrong.k` and
  `evidence/17-kprove-slice-wrong-extended.log`.

Evidence limitation: the fresh bridge-free universal claim over arbitrary
`REST:IntSeq` does not close. It exits 1 with the unresolved supplied term
`buildIS(..., isLen(REST)+2, ...)`, exactly the abstract-tail limitation the
candidate rule is intended to bridge. See `evidence/slice-universal.k` and
`evidence/15-kprove-slice-universal-fixed.log`. This is not a counterexample or
a false conclusion witness. I found no false witness on the intended domain,
so I do not label the rule unsound; I record the narrower missing universal
machine-checked connection theorem.

### Supplied declarations not on the proof path

The fixed supplied semantics contains 25 symbol/opaque boundaries:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

None is reachable from this program or appears in its claim. The same is true
of all rules in the assert, bool, comprehension, concrete, controls, dict,
float, iter, list, methods, range, set, sort, and tuple modules, except for
shared declarations explicitly marked reachable in the row-level review.
Their existence cannot select a branch or determine this theorem's result.

Fresh compilation warned that several supplied `[total]` functions are not
syntactically exhaustive: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`. None occurs on the candidate proof path. The concrete smoke
path uses only defined, in-range cases. These warnings expose global subset
limitations of the supplied semantics, not a candidate-added rule and not a
false conclusion for the intended inputs.

No candidate proof rule is an opaque oracle, no rule bypasses the submitted
body, no rule assumes the final result, and no candidate simplification,
totality declaration, or auxiliary claim exists.

## 6. Fresh non-vacuity test

I authored `evidence/spec-vacuity.k` in scratch after inspecting the candidate.
It changes the final code point of the required suffix from 98 (`"b"`) to 99
(`"c"`). Thus the mutated claim requires `"db" ++ binCodes(N) ++ "dc"`.

`N = 0` is a concrete satisfying input. The real formal and Python result is
`"db0db"`, while the mutation requires `"db0dc"`.

Exact command:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

The mutation parsed and built successfully, reached the result-checking
obligation, printed `WarnStuckClaimState`, and exited 1. The residual explicitly
compares:

```text
seqConcat(binCodes(N), iCons(100, iCons(98, .IntSeq)))
```

against:

```text
seqConcat(binCodes(N), iCons(100, iCons(99, .IntSeq)))
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. See
`evidence/18-kprove-vacuity.log`.

Non-vacuity result: pass.

## 7. Proven versus assumed accounting

### Precisely proven

Under the byte-identical supplied K semantics and the two reviewed local rules,
the all-path reachability claim establishes partial correctness for every K
integer `N >= 0` from the displayed clean entry configuration:

- the exact submitted function body executes;
- the final `<k>` value is exactly the string code sequence
  `"db" ++ binCodes(N) ++ "db"`;
- environment, scopes, allocation counters, heap, stack, return state,
  exception state, and exit code are restored to the claimed values.

The proof does not merely say that some output exists. The failed mutation
shows that changing one required output character invalidates the proof.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.337 frontend, LLVM runtime, Haskell prover, and built-in integer/string/map theories | all dynamic and symbolic evidence | Standard toolchain trust boundary; version and commands recorded |
| `/reference/reference-semantics` | the entire theorem | Required supplied semantics; candidate tree is byte-identical |
| Supplied `bin` contract and defined `binCodes`/`binAcc` equations | program result and postcondition | Acceptable fixed external primitive: Python's `bin` is outside the program-defined body; relevant equations are explicit and guarded |
| Mathematical reading of `binCodes` as the ordinary no-leading-zero base-2 representation | bridge from formal RHS to English intent | Informal induction on repeated quotient/remainder by two, supported by independent `format(N,"b")` witnesses and the 902-case differential run |
| Proof-local two-code-point slice equation | closure of the symbolic slice | Mathematically sound and ground-connected to fixed semantics; concerning only because the universal bridge-free K connection does not close |
| Trusted translator plus exact embedded body | program identity | Byte identity, manual AST comparison, and a fresh full-module symbolic `#Top` |
| Finite Python differential evidence | canonical/generated and intent bridge on tested values | Empirical only; no universal-proof claim |
| 25 supplied opaque symbols and unrelated total functions | none | Unreachable and irrelevant to this theorem |

The `binCodes` symbol is not opaque: for the formal nonnegative domain it has
explicit zero and positive equations, and `binAcc` descends on the quotient.
The proof's use of the same fixed symbol in the supplied `bin` result and the
postcondition is a named contract for an external builtin, not an unconstrained
program-derived oracle.

### Excluded or limited behavior

- Negative integers are outside the formal precondition.
- Non-integer Python inputs and Python exception behavior are outside the K
  claim.
- Termination beyond the requested partial-correctness interpretation is not a
  separately stated theorem.
- Global fidelity of unused MiniPython constructs, floats, sorting, MD5,
  invalid indexing, and unused total functions is not established.
- Missing generation metadata prevents independent reconstruction of the
  candidate's claimed generation history.
- There is no bridge-free universal K theorem for the proof-local slice
  equation; this is the principal reason for `CONCERNS` rather than `PASS`.

### Decision

The proof reconstructs, is non-vacuous and result-constraining, and pins the
real generated program on the coherent intended domain. No materially unsound
rule or false conclusion witness was found. The missing universal machine
connection for the otherwise valid slice identity, the absent generation
metadata, and the prompt's implicit nonnegative-domain assumption are
documented limitations.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
