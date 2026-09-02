requires "verification.k"

module AUDITOR-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed constructor term itself is mutated: invalid return -1 -> 7.
  claim [mutated-executed-body]:
    <k>
      #loadAll(
        Module(
          Import("math")
          FuncDef("triangle_area", Params("a", "b", "c"),
            If(BoolOp(
              "or",
              Compare(BinOp("+", Name("a"), Name("b")), CmpOp("<=", Name("c"))),
              Compare(BinOp("+", Name("a"), Name("c")), CmpOp("<=", Name("b"))),
              Compare(BinOp("+", Name("b"), Name("c")), CmpOp("<=", Name("a")))),
              Return(Int(7)),
              .Stmts)
            Assign(
              Name("semi_perimeter"),
              BinOp(
                "/",
                BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
                Int(2)))
            Assign(
              Name("area"),
              Call(
                Attribute(Name("math"), "sqrt"),
                BinOp(
                  "*",
                  BinOp(
                    "*",
                    BinOp(
                      "*",
                      Name("semi_perimeter"),
                      BinOp("-", Name("semi_perimeter"), Name("a"))),
                    BinOp("-", Name("semi_perimeter"), Name("b"))),
                  BinOp("-", Name("semi_perimeter"), Name("c")))))
            Return(Call(Name("round"), Name("area"), Int(2)))))
        )
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A +Int B <=Int C
endmodule
