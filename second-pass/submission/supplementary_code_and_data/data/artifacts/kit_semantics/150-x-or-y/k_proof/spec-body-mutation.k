requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: result is initialized to y instead of x.
  // The original theorem's required result for prime input 2 is 10.
  claim [changed-body]:
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
      ~> Call(Name("x_or_y"), Int(2), Int(10), Int(20))
      => ?V:Val
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => ?FINALSCOPES:Map
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
