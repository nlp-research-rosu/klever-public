requires "reference-semantics/semantics.k"

module FIB-VERIFICATION
  imports MPY

  syntax Stmts ::= "fibBody" [function]
  syntax Val ::= "fibClosure" [function]
  syntax Module ::= "fibProgram" [function]

  rule fibBody =>
    Expr(
      Str(
        "Return n-th Fibonacci number.\n    >>> fib(10)\n    55\n    >>> fib(1)\n    1\n    >>> fib(8)\n    21\n    "))
    Assign(Name("a"), Int(1))
    Assign(Name("b"), Int(1))
    Assign(Name("_"), Int(0))
    For(Name("_"), Call(Name("range"), Name("n")),
      Assign(
        TupleExpr(Name("a"), Name("b")),
        TupleExpr(Name("b"), BinOp("+", Name("a"), Name("b")))))
    Return(Name("a"))

  rule fibClosure =>
    closureVal(("n", .ParamNames), fibBody, 0)

  rule fibProgram =>
    Module(FuncDef("fib", Params("n"), fibBody))

  // A mathematical tail-recursive Fibonacci fold. Starting from
  // (A,B,I) = (0,1,0), it returns the N-th Fibonacci number.
  syntax Int ::= fibRun(Int, Int, Int, Int) [function, total]
  syntax Int ::= fibSpec(Int) [function, total]

  rule fibRun(A:Int, _:Int, I:Int, N:Int) => A
    requires I >=Int N

  rule fibRun(A:Int, B:Int, I:Int, N:Int)
    => fibRun(B, A +Int B, I +Int 1, N)
    requires I <Int N

  rule fibSpec(N:Int) => fibRun(0, 1, 0, N)
endmodule
