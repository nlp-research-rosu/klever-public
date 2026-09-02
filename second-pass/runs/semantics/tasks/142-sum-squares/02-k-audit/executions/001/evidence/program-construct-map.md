# Submitted-program construct and rule map

The submitted MPY uses `Module`, `FuncDef`, `Params`, `Assign`, `Name`,
`Int`, `For`, `If`, `Compare`, `BinOp`, `CmpOp`, `AugAssign`, and `Return`.
All are declared in the fixed `semantics/syntax.k` (`Module`/parameter forms
at lines 56–61, statements at 41–54, expressions at 9–31).

The end-to-end proof starts with a `Call` in an exact module-scope closure
rather than with module loading. The connection to the translated MPY is:

- fixed `functions.k:13–15` loads `FuncDef("sum_squares", Params("lst"),
  BODY)` into `closureVal(("lst", .ParamNames), BODY, 0)`;
- proof macros `verification.k:48–83` expand to the exact translated `BODY`;
- the entry scope in `spec.k:96–103` contains exactly that closure.

The actual execution path is:

1. `call.k:15–19` evaluates `Name("sum_squares")`; `core.k:130–154`
   resolves the exact closure.
2. `core.k:185–191` evaluates the single already-valued list argument;
   `call.k:83–90` allocates the local frame and enters `#bindP ~> BODY ~>
   #endcall`; `functions.k:55–69` binds `lst`.
3. `core.k:124–127` sequences the statements. `controls.k:9–31` implements
   the two assignments and each integer `AugAssign`.
4. `syntax.k` strictness plus `operators.k:7–17` gives left-to-right
   integer expression/compare evaluation; `int.k:7–27` supplies `+`, `*`,
   `%`, `==`, and Python modulo.
5. `controls.k:65–74` implements `For`, with the proof-local
   `verification.k:15–19` iterator rules exposing the proof-only `Ints`
   representation one element at a time. `tuple.k:31–41` binds `value`.
6. `controls.k:51–54` selects the two nested `If` branches. The first test
   has priority by control flow, including indices divisible by both 3 and 4.
7. `functions.k:72–91` records the return value, restores the caller
   continuation/environment, removes the local scope, and resets `scopeLoc`.

No used construct allocates heap data in the proof: the input is an unboxed
read-only `list(intVals(IS))`. The proof pins empty heap, `NoExc`, `noRet`,
empty stack, and exit code 0 at entry; the body claim also pins frame cleanup.
Unused baseline language rules (floats, strings, dicts, slices, comprehensions,
sorting, opaque digests, and so on) cannot fire on this AST or these values.
