requires "verification.k"

module REVIEWER-BODY-MUTATION
  imports VERIFICATION

  // Operational-sensitivity mutation: change the theorem's actually executed
  // function body from addition to multiplication while retaining add's post.
  // X=2, Y=3 is a satisfying counterexample (6 is not 5).
  claim [fresh-changed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef("add", Params("x", "y"),
            Return(BinOp("*", Name("x"), Name("y"))))
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
               Return(BinOp("*", Name("x"), Name("y"))) .Stmts,
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
