requires "verification.k"

module AUDIT-PINNING-SPEC
  imports TRIANGLE-VERIFICATION

  // The module below is inserted from solution.mpy by this reviewer script.
  // Loading it must bind the same exact closure/body used by the call claims.
  claim
    <k> #loadAll(Module(
  FuncDef("triangle_area", Params("a", "b", "c"),
    If(BoolOp(
      "or",
      Compare(BinOp("+", Name("a"), Name("b")), CmpOp("<=", Name("c"))),
      Compare(BinOp("+", Name("a"), Name("c")), CmpOp("<=", Name("b"))),
      Compare(BinOp("+", Name("b"), Name("c")), CmpOp("<=", Name("a")))),
      Return(UnaryOp("-", Int(1))),
      .Stmts)
    Assign(
      Name("s"),
      BinOp(
        "/",
        BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
        Int(2)))
    Return(
      Call(
        Name("round"),
        BinOp(
          "**",
          BinOp(
            "*",
            BinOp(
              "*",
              BinOp("*", Name("s"), BinOp("-", Name("s"), Name("a"))),
              BinOp("-", Name("s"), Name("b"))),
            BinOp("-", Name("s"), Name("c"))),
          Float(0.5)),
        Int(2)))))) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> triangleAreaClosure,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
