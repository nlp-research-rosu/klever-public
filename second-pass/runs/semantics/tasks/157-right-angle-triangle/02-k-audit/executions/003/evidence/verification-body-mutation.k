requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is exactly the function body emitted in solution.mpy.  Keeping it as
  // a named function lets each claim call the submitted implementation without
  // loading any extra, proof-only Python code.
  syntax Stmts ::= "#rightAngleTriangleBody" [function]
  rule #rightAngleTriangleBody
    => If(Compare(Name("a"), CmpOp("<=", Int(0))),
          Return(Bool(false)),
          .Stmts)
       If(Compare(Name("b"), CmpOp("<=", Int(0))),
          Return(Bool(false)),
          .Stmts)
       If(Compare(Name("c"), CmpOp("<=", Int(0))),
          Return(Bool(false)),
          .Stmts)
       If(Compare(
            BinOp("+",
              BinOp("*", Name("a"), Name("a")),
              BinOp("*", Name("b"), Name("b"))),
            CmpOp("==", BinOp("*", Name("c"), Name("c")))),
          Return(Bool(false)),
          .Stmts)
       If(Compare(
            BinOp("+",
              BinOp("*", Name("a"), Name("a")),
              BinOp("*", Name("c"), Name("c"))),
            CmpOp("==", BinOp("*", Name("b"), Name("b")))),
          Return(Bool(true)),
          .Stmts)
       If(Compare(
            BinOp("+",
              BinOp("*", Name("b"), Name("b")),
              BinOp("*", Name("c"), Name("c"))),
            CmpOp("==", BinOp("*", Name("a"), Name("a")))),
          Return(Bool(true)),
          .Stmts)
       Return(Bool(false))

  syntax Val ::= "#rightAngleTriangleClosure" [function]
  rule #rightAngleTriangleClosure
    => closureVal(("a", "b", "c"), #rightAngleTriangleBody, 0)

  syntax KItem ::= "#runRightAngleTriangle"
                   "(" Int "," Int "," Int ")"
  rule #runRightAngleTriangle(A:Int, B:Int, C:Int)
    => Call(#rightAngleTriangleClosure, A, B, C)
endmodule
