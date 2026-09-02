// spec.k — triangle_area, TRAP-FREE (P71). One entry claim over canonical's
// straight-line body: the or-condition case-splits; the valid branch's inline
// float chain reduces to heronV's composition; result == triangleAreaRes.
//
//   kompile verification.k --backend haskell --main-module TRIANGLE-AREA-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module TRIANGLE-AREA-SPEC

requires "verification.k"

module TRIANGLE-AREA-SPEC
  imports TRIANGLE-AREA-VERIFICATION

  claim
    <k>
      FuncDef("triangle_area", Params("a", "b", "c"),
        If(BoolOp("or",
            Compare(BinOp("+", Name("a"), Name("b")), CmpOp("<=", Name("c"))),
            Compare(BinOp("+", Name("a"), Name("c")), CmpOp("<=", Name("b"))),
            Compare(BinOp("+", Name("b"), Name("c")), CmpOp("<=", Name("a")))),
          Return(UnaryOp("-", Int(1))),
          .Stmts)
        Assign(Name("s"),
          BinOp("/", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Int(2)))
        Assign(Name("area"),
          BinOp("**",
            BinOp("*",
              BinOp("*",
                BinOp("*", Name("s"), BinOp("-", Name("s"), Name("a"))),
                BinOp("-", Name("s"), Name("b"))),
              BinOp("-", Name("s"), Name("c"))),
            Float(0.5)))
        Assign(Name("area"), Call(Name("round"), Name("area"), Int(2)))
        Return(Name("area")))
      Assign(Name("result"), Call(Name("triangle_area"), A:Int, B:Int, C:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "triangle_area" <- ?_:Val ] [ "result" <- triangleAreaRes(A, B, C) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
