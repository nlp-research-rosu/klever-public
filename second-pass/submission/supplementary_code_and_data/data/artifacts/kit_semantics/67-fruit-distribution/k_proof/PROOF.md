VALIDATED

## What is proven

Every claim in `spec.k` was proved by `kprove`: there is one positive target
claim, `SPEC.fruit-distribution`. Under the supplied MPY semantics and the
claim's precondition, the exact translated function body returns
`N -Int APPLES -Int ORANGES`.

This is a partial-correctness result. It says that every terminating execution
from the stated domain reaches the stated result; it does not prove
termination.

## Formal claim

The claim begins at an exact invocation of a `closureVal` with parameters
`("s", "n")` and the body translated from `solution.py`:

```python
return n - int(s.split()[0]) - int(s.split()[3])
```

The input domain is:

- `s` is an MPY string whose whitespace split is exactly
  `[APPLECODES, "apples", "and", ORANGECODES, "oranges"]`;
- both number tokens are nonempty sequences of ASCII decimal digits;
- the supplied semantics' `int` conversion maps those tokens to the
  nonnegative integers `APPLES` and `ORANGES`;
- `N >=Int APPLES +Int ORANGES`.

The result cell is constrained to `N -Int APPLES -Int ORANGES`. The theorem
also requires the caller environment, scopes, stack, return state, exception
state, and exit code to be restored. The two lists allocated by the two
`split()` calls are intentionally unobserved, so the final heap and heap
location are existentially framed.

`solution.mpy` is regenerated from `solution.py` and checked against
`solution.mpy.sha256`. The closure body in `spec.k` was structurally compared
with that generated term. The final SHA-256 of `solution.mpy` is
`280a1b9812a03c3679da3bf6dd8dc7be48f2c78769ec1a5ce6ff7b1ba73a5902`.

## Proof-extension inventory

There are no proof extensions.

`verification.k` only imports the supplied `MPY` module. It declares no
function, equation, simplification, concrete rule, ordinary rewrite, priority
rule, operational bridge, trusted primitive, or auxiliary claim. `spec.k`
contains only the positive target claim. The two other claim files are
independent expected-failure validation probes and are not imported by the
positive proof.

Consequently, the proof-extension contract's per-extension fields have no
entries: all source operations execute using the fixed reference semantics.

## Commands and actual results

The complete recorded workflow is executable as:

```bash
./prove.sh
```

It exited `0`. Its substantive commands and results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
sha256sum --check solution.mpy.sha256
```

Output: `solution.mpy: OK`. Exit: `0`.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
```

Exit: `0`. The final configuration in `concrete-krun.log` has `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>` after all four prompt
examples. LLVM compilation emitted non-exhaustiveness and unused-variable
warnings from the supplied semantics but completed successfully.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Output: `#Top`. Exit: `0`. The exact prover output is preserved in
`proof-target.log`. Haskell compilation/proof parsing also emitted only
unused-variable warnings from the supplied semantics and unused existential
heap-variable warnings from `spec.k`.

The false-postcondition probe was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Exit: `1`, as expected. `proof-vacuity.log` contains
`WarnStuckClaimState`; its failed implication compares the actual
`N -Int APPLES -Int ORANGES` with the deliberately false
`N -Int APPLES -Int ORANGES +Int 1`.

The operational/body-sensitivity probe was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Exit: `1`, as expected. `proof-body-mutation.log` contains
`WarnStuckClaimState`; replacing subtraction of oranges by addition produces
`N -Int APPLES +Int ORANGES`, which does not imply the target result.

The independent finite differential test was:

```bash
python3 differential_test.py
```

Output: `cases=436 mismatches=0`. Exit: `0`.

## Gate results

### Gate A — PASS

- **A1, program identity/body sensitivity:** the target starts with the exact
  closure parameters, body, arguments, and defining environment. The generated
  translation passes the recorded digest check. The wrong-body K probe exits
  `1` with the changed result visible in its residual.
- **A2, state preservation:** no execution is skipped. Fixed semantics performs
  both list allocations, call-frame allocation/removal, parameter binding,
  lookups, return, and frame pop. Heap growth is explicitly abstracted because
  it is not observable in the HumanEval contract; all relevant control and
  exception cells are constrained.
- **A3, binding/evaluation/control:** there is no operational bridge. The exact
  closure fixes the entry binding and body, while parameter and builtin
  lookups, left-to-right call evaluation, subscripting, arithmetic, return, and
  frame restoration all execute through the supplied semantics.
- **A4, consistency:** the proof adds no equations or rules, so there are no
  proof-local coverage, overlap, totality, or descent obligations.
- **A5, non-vacuity/result constraint:** the concrete state
  `s = "5 apples and 6 oranges", N = 19` satisfies the domain and terminates
  with `8`; all four supplied examples finish with no exception. The `+1`
  postcondition mutation exits `1` and exposes the unmet equality.

### Gate B — PASS

- **B1:** the formal domain covers arbitrary-length nonnegative decimal apple
  and orange counts, the literal words in the prompt, whitespace tokenization,
  and a total at least as large as their sum. This makes explicit the
  well-formed-basket assumptions implicit in the prompt.
- **B2:** K integers are unbounded, matching Python integers for this
  arithmetic. The fixed model is ASCII-oriented and the theorem excludes
  malformed strings and exception paths; those restrictions are immaterial to
  the prompt's stated examples and input form.
- **B3:** no new summary stands between execution and the result. `splitWS`,
  `applyBuiltin("int", ...)`, and `intDigAcc` are fixed semantic definitions;
  digit/nonempty guards connect them to nonnegative decimal parsing. The
  separate regex-based differential oracle gives finite CPython evidence.
- **B4:** the implementation and theorem both compute total fruit minus the
  parsed apple and orange counts.

### Gate C — PASS

The trust ledger below names every component outside the target theorem, the
evidence artifacts exist, all commands and outcomes are recorded, and formal
facts are separated from finite evidence and excluded behavior.

## Trust boundary

| Component | Exact relevant symbols/rules | Influence and dependents | Evidence |
|---|---|---|---|
| Supplied read-only MPY semantics | `Call`, `#callee`, `#applyK`, `closureVal`, `#bindP`, `Return`, `#pop`, `splitWS`, `#alloc`, `applyIndex`, `valSeqAt`, `applyBuiltin("int", ...)`, `intDigAcc`, `applyBin("-" ...)` | Defines value, control, temporary scopes, heap allocation, and exception behavior for `SPEC.fruit-distribution`; it is the fixed execution model, not proved by this task | LLVM prompt-example run, body/postcondition mutations, and 436 CPython differential cases |
| `py2mpy.py` | CPython-AST mappings for `FunctionDef`, `Return`, `BinOp`, `Call`, `Attribute`, and `Subscript` | Supplies the source-to-MPY syntax link; it does not add proof rules | Deterministic regeneration, empty `diff`, recorded SHA-256, and structural inspection of the exact AST/body |
| K toolchain and Haskell backend | K v7.1.293, reachability engine, builtin integer/string theories, SMT reasoning | Establishes `#Top` for the target claim and rejects both mutations | Exact commands, logs, exit codes, and complete `prove.sh` exit `0` |
| CPython/intent adequacy bridge | Python `str.split`, `int`, indexing, and integer subtraction | Supports the claim that the MPY theorem represents the HumanEval Python behavior; it is empirical rather than a universal equivalence theorem | `differential_test.py`, using an independently written regex oracle, reports 436 cases and zero mismatches |

No proof-local trusted primitive, opaque result, or program-derived abstraction
affects the theorem.

## Empirically supported facts

`concrete-tests.py` contains the four examples from `prompt.py`; the LLVM MPY
run finished all assertions with `.K`, `NoExc`, and exit code `0`.

`differential_test.py` imports the real `solution.py` implementation and compares
it with an independently written `re.fullmatch` oracle. Its scope is the four
prompt examples plus the Cartesian product of twelve boundary apple counts,
twelve boundary orange counts, and three mango counts: 436 total inputs, zero
mismatches. This is finite validation evidence, not a universal proof.

## Excluded behavior

- Malformed strings, missing tokens, non-decimal or signed counts, and their
  Python exception behavior.
- Negative fruit counts or totals smaller than apples plus oranges.
- General Unicode string behavior beyond the supplied ASCII-oriented model.
- Observation of temporary lists allocated by the two `split()` calls.
- Termination as a liveness theorem; the K result is partial correctness.
- A universal proof that the supplied MPY semantics or `py2mpy.py` is equivalent
  to CPython. Those components are explicitly trusted and empirically checked.
