requires "verification.k"

module SPEC-AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity mutation: both copies of the executed closure body
  // initialize result from y rather than x, but the claim still demands 10.
  claim [changed-program-body]:
    <k>
      #loadAll(
        Module(
          FuncDef("x_or_y", Params("n", "x", "y"),
            If(
              Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")) .Stmts,
              .Stmts)
            Assign(Name("i"), Int(2))
            Assign(Name("result"), Name("y"))
            While(
              Compare(Name("i"), CmpOp("<", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("==", Int(0))),
                Assign(Name("result"), Name("y")) .Stmts,
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))) .Stmts)
            Return(Name("result")) .Stmts)))
      ~> Call(Name("x_or_y"), 2, 10, 20)
      => ?V:Val
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "x_or_y" |->
          closureVal(
            "n", "x", "y", .ParamNames,
            If(
              Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")) .Stmts,
              .Stmts)
            Assign(Name("i"), Int(2))
            Assign(Name("result"), Name("y"))
            While(
              Compare(Name("i"), CmpOp("<", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("==", Int(0))),
                Assign(Name("result"), Name("y")) .Stmts,
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))) .Stmts)
            Return(Name("result")) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?V ==K 10
endmodule
