# Filter by Substring K Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `filter_by_substring`, execute its translated AST with a local K semantics, and close a universal correctness proof plus the prompt examples.

**Architecture:** The Python implementation is a list comprehension. A compact functional K evaluator interprets the exact constructor families emitted for that implementation, while an independent recursive `filterRef` defines the contract over an algebraic string-list value. Symbolic equivalence is proved by K's circularity/induction over that list.

**Tech Stack:** Python 3.10 AST, `py2mpy.py`, K Framework 7.1.293, Haskell backend, POSIX shell.

## Global Constraints

- Do not modify `prompt.py` or `py2mpy.py`.
- Keep all artifacts under `/work`.
- Preserve `filter_by_substring(strings: List[str], substring: str) -> List[str]`.
- Every positive `kprove` target must print `#Top` and exit zero.
- No Git repository exists, so commit steps are replaced by explicit validation checkpoints.

---

### Task 1: Establish the Python behavior test

**Files:**
- Create: `solution.py`
- Generate: `solution.mpy`

**Interfaces:**
- Consumes: the signature and examples in `prompt.py`.
- Produces: `filter_by_substring(strings: List[str], substring: str) -> List[str]` and its pure constructor translation.

- [ ] **Step 1: Run a failing import test before implementation**

Run:

```bash
python3 - <<'PY'
from solution import filter_by_substring
assert filter_by_substring([], "a") == []
PY
```

Expected: non-zero exit because `solution.py` does not exist.

- [ ] **Step 2: Implement the minimal function**

Create `solution.py` with the prompt import, signature, docstring, and this body:

```python
return [string for string in strings if substring in string]
```

- [ ] **Step 3: Verify Python behavior and translation**

Run:

```bash
python3 - <<'PY'
from solution import filter_by_substring
assert filter_by_substring([], "a") == []
assert filter_by_substring(["abc", "bacd", "cde", "array"], "a") == ["abc", "bacd", "array"]
assert filter_by_substring(["x", "x", ""], "") == ["x", "x", ""]
PY
python3 py2mpy.py solution.py > solution.mpy
```

Expected: both commands exit zero; `solution.mpy` contains one `ListComp` and one `CmpOp("in", ...)`.

### Task 2: Establish red K execution and proof targets

**Files:**
- Create: `spec.k`
- Create: `verification.k`

**Interfaces:**
- Consumes: translated constructors from `solution.mpy`.
- Produces: named claims `universal`, `empty-example`, and `prompt-example`; `filterRef(PyList, String)`.

- [ ] **Step 1: Write the claims and reference function before the semantics exists**

Define an algebraic `PyList` with `Nil` and `Cons(String, PyList)`. Define `filterRef` by recursion, with keep/drop rules guarded by `findString(HEAD, SUBSTRING, 0) =/=Int -1` and equality to `-1`. State one claim whose left side executes the translated module on symbolic `INPUT:PyList` and `SUBSTRING:String`, and two ground example claims.

- [ ] **Step 2: Observe the expected red compilation**

Run:

```bash
kprove spec.k --definition .kbuild/semantic-kompiled --claim UNIVERSAL
```

Expected: non-zero because `semantic.k` has not been compiled and its constructor/evaluator syntax is absent.

### Task 3: Implement the minimum constructor semantics

**Files:**
- Create: `semantic.k`
- Modify: `verification.k`

**Interfaces:**
- Consumes: `Module`, `ImportFrom`, `FuncDef`, `Params`, `Return`, `ListComp`, `CompFor`, `Name`, `Compare`, and `CmpOp` terms.
- Produces: `execute(Pgm, String, PyList, String)`, expression evaluation under a `Map`, and terminal `PyList` results.

- [ ] **Step 1: Declare constructor and runtime syntax**

Declare statement sequences using K's separatorless `List{Stmt, ""}` and comma-separated expression/parameter helper lists matching `py2mpy.py`. Declare `PyList ::= Nil | Cons(String, PyList)`, and a top-level `<k>` configuration initialized by the program plus function/input/substring configuration variables.

- [ ] **Step 2: Add generic definition lookup and invocation**

Ignore `ImportFrom` during function lookup, select a `FuncDef` by name, bind its two formal parameters in a `Map`, and interpret its `Return` expression. No rule may mention `filter_by_substring`.

- [ ] **Step 3: Add list-comprehension and membership evaluation**

Evaluate names by environment lookup. Recursively traverse the source `PyList`; extend the environment with the generator target; retain each head when the translated `Compare(... CmpOp("in", ...))` evaluates true, otherwise drop it. Implement membership via `findString`.

- [ ] **Step 4: Compile and exercise both examples**

Run:

```bash
kompile semantic.k --backend haskell --main-module VERIFICATION --syntax-module SEMANTIC-SYNTAX --directory .kbuild
krun solution.mpy --definition .kbuild/semantic-kompiled -cFUNCTION='"filter_by_substring"' -cINPUT='Nil' -cSUBSTRING='"a"'
krun solution.mpy --definition .kbuild/semantic-kompiled -cFUNCTION='"filter_by_substring"' -cINPUT='Cons("abc",Cons("bacd",Cons("cde",Cons("array",Nil))))' -cSUBSTRING='"a"'
```

Expected: terminal `Nil` and `Cons("abc",Cons("bacd",Cons("array",Nil)))` results.

### Task 4: Close and harden every proof

**Files:**
- Modify: `spec.k`
- Create: `prove.sh`
- Create only if needed: `NOTES.md`

**Interfaces:**
- Consumes: compiled semantics and the three named claims.
- Produces: independently auditable commands and zero-exit `#Top` output for each positive target.

- [ ] **Step 1: Run each claim independently**

Run one `kprove spec.k --definition .kbuild/semantic-kompiled --claim <NAME>` command for each of `UNIVERSAL`, `EMPTY-EXAMPLE`, and `PROMPT-EXAMPLE`. If universal symbolic-list matching does not induce automatically, factor the recursive evaluator/reference equivalence into a guarded helper claim and use it as a lemma.

- [ ] **Step 2: Record the exact reproducible workflow**

Write `prove.sh` with `set -euo pipefail`, translation, Python assertions, `kompile`, two `krun` checks, and all positive `kprove` commands. Remove `.kbuild` explicitly before compilation so stale definitions cannot satisfy the gate.

- [ ] **Step 3: Run the complete verification gate**

Run:

```bash
bash -n prove.sh
./prove.sh
```

Expected: zero exit, correct `krun` results, and `#Top` from every positive proof command. If not, preserve diagnostics and explain the concrete remaining issue in `NOTES.md` without claiming success.
