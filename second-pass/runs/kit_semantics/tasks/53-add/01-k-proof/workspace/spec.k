requires "verification.k"

module SPEC
  imports VERIFICATION

  // For arbitrary mathematical integers X and Y, load the exact translated
  // function body, invoke its module binding, and observe the returned value.
  claim [add-correct]:
    <k>
      #loadAll(
        Module(
          FuncDef("add", Params("x", "y"),
            Return(BinOp("+", Name("x"), Name("y"))))
        )
      )
      ~> Call(Name("add"), Int(X:Int), Int(Y:Int))
      => X +Int Y
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> (
         scope(.Map, parent(-1))
         =>
         scope(
           "add" |->
             closureVal(
               "x", "y", .ParamNames,
               Return(BinOp("+", Name("x"), Name("y"))) .Stmts,
               0
             ),
           parent(-1)
         )
       )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
