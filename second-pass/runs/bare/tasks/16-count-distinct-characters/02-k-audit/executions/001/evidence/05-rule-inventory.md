# Reviewer rule inventory

This inventory covers all local declarations and rules in the submitted
`semantic.k` and `verification.k`. There are no generated helper K files.

## Local syntax and configuration

`MPY-SYNTAX` declares:

1. `Program ::= Module(Stmts)`.
2. `Stmts ::= List{Stmt, ""}`.
3. `Stmt ::= FuncDef(String, Params, Stmts)`.
4. `Stmt ::= Return(Expr)`.
5. `Params ::= Params(Strings)`.
6. `Strings ::= List{String, ","}`.
7. `Expr ::= Name(String)`.
8. `Expr ::= Attribute(Expr, String)`.
9. `Expr ::= Call(Expr, Exprs)`.
10. `Exprs ::= List{Expr, ","}`.

`SEMANTIC` declares:

11. `Value ::= StrVal(String)`.
12. `Value ::= SetVal(Set)`.
13. `Value ::= IntVal(Int)`.
14. `Result ::= noResult | Value`.
15. `KResult ::= Value`.
16. `KItem ::= #lower`.
17. `KItem ::= #set`.
18. `KItem ::= #len`.
19. `KItem ::= #finish`.
20. `String ::= lowerString(String) [function]`.
21. `String ::= lowerChar(String) [function]`.
22. `Set ::= charsSet(String) [function]`.

`VERIFICATION` declares:

23. `Int ::= expectedDistinctCharacters(String) [function]`.

There are no local `[total]` or `[functional]` declarations, opaque symbols,
explicit numeric priorities, or `[simplification]` attributes. The sole local
priority mechanism is the `[owise]` fallback for `lowerChar`.

The configuration is `<mpy>` containing `<k>` initialized by `$PGM:Program`,
an empty `<env>` map, `<input>` initialized by `$INPUT:String`, and `<result>`
initialized to `noResult`. Every cell is read or written by a used rule.

## Ordinary operational rules

1. Module/entry harness (lines 52–55): for the sole one-parameter function with
   the required name and an empty environment, bind its parameter to
   `StrVal(input)` and execute its body. This is a specialized entry harness,
   not general Python module execution. It matches the actual program and
   preserves any following continuation.
2. Return (line 57): the sole final `Return(E)` evaluates `E`, schedules
   `#finish`, and preserves the outer continuation. Sound for the used body.
3. Name lookup (lines 59–60): replace a bound name by its map value. Sound for
   the actual `"string"` lookup.
4. Lower-call scheduling (line 63): evaluate the receiver of an exact,
   zero-argument syntactic `.lower()` call before `#lower`. Specialized but
   sound for the used plain-string receiver and fixed source binding.
5. Lower application (line 64): rewrite `StrVal(S) ~> #lower` to
   `StrVal(lowerString(S))`. This is an external-operation bridge whose value
   is unsound for Python strings because `lowerString` implements only ASCII
   uppercase mapping. Witness: `"Åå"` produces candidate result 2, while both
   Python implementations return 1.
6. Set-call scheduling (line 66): evaluate the one argument of the exact
   syntactic `set` call before `#set`. Specialized but sound for this module,
   which does not rebind `set`.
7. Set application (line 67): rewrite `StrVal(S) ~> #set` to
   `SetVal(charsSet(S))`. This bridge is unsound for Python's code-point
   iteration through the candidate's actual `-cINPUT` route. Raw `"😀"` is
   observed in the K configuration as `"\xf0\x9f\x98\x80"` and produces
   candidate result 4, while `len(set("😀".lower()))` is 1 in both Python
   programs. A Unicode literal embedded directly in K source has a different
   representation; that distinction makes an explicit input bridge necessary.
8. Len-call scheduling (line 69): evaluate the one argument of the exact
   syntactic `len` call before `#len`. Specialized but sound for this module,
   which does not rebind `len`.
9. Len application (line 70): native K set `size` becomes `IntVal`; sound
   conditional on `SetVal` representing the intended Python set.
10. Finish (lines 72–73): when the computation is exactly
    `IntVal(I) ~> #finish`, empty it and write the value to the initially empty
    result cell. It accepts no trailing continuation and is sound for the used
    top-level return path.

Together, scheduling is receiver/inner-argument first:
`lower -> set -> len -> finish`. No used allocation, mutation, output,
exception, loop, call stack, or guard construct is silently fabricated.

## Function/equational rules

11. `lowerString("") => ""` (line 79): true.
12. Nonempty `lowerString` recursion (lines 80–83): walks one K substring unit,
    applies `lowerChar`, and recurses. Guards are disjoint with the empty rule
    and concrete executions terminate, but the operation is not Python Unicode
    lowercasing.
13. ASCII uppercase `lowerChar` (lines 86–87): adding 32 for code points
    65–90 agrees with Python on that exact range.
14. `lowerChar(C) => C [owise]` (line 88): false as a model of Python
    lowercasing. Concrete false-conclusion witness: `C = "Å"` is outside the
    ASCII guard, so the rule preserves it, but Python concludes
    `"Å".lower() == "å"`.
15. `charsSet("") => .Set` (line 93): true.
16. Nonempty `charsSet` recursion (lines 94–97): inserts successive K substring
    units into a native set. It is terminating in the tested concrete domain
    but false as a model of iteration over Python Unicode code points.
    Concrete false-conclusion witness: on the runtime K representation
    `S = "\xf0\x9f\x98\x80"` arising from `-cINPUT="😀"`, the candidate program
    concludes set size 4 and the corresponding Python string concludes size 1.
17. `expectedDistinctCharacters(S) =>
    size(charsSet(lowerString(S)))` (`verification.k` line 9): a terminating,
    transparent definitional summary of the same candidate semantic functions.
    It is not opaque or unconstrained, but it inherits both semantic defects
    and provides no independent connection to Python's Unicode behavior.

## Spec claims

`spec.k` has four positive reachability claims: one universal over every K
`String`, then concrete `"xyzXYZ"`, `"Jerry"`, and empty-string claims. There
are no helper/loop claims. The universal postcondition is exact
`IntVal(expectedDistinctCharacters(S))`; the concrete results are exact
integers, not free variables.
