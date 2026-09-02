requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changes the real product update from *= to +=.
  // For [2,4], the mutated program returns (6,7), so (6,8) is false.
  claim [changed-body-still-original-result]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", ("List", "Tuple", .ParamNames))
        FuncDef("sum_product", Params("numbers", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(1))
          Assign(Name("number"), Int(0))
          For(Name("number"), Name("numbers"),
            AugAssign(Name("total"), "+", Name("number"))
            AugAssign(Name("product"), "+", Name("number")) .Stmts)
          Return(TupleExpr(Name("total"), Name("product"), .Exprs)) .Stmts)
        .Stmts))
      ~> Call(
           Name("sum_product"),
           (list(vCons(2, vCons(4, .ValSeq))), .Exprs))
      => tuple(vCons(6, vCons(8, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
         0 |-> scope(.Map, parent(-1)) )
      =>
      ( -1 |-> builtinsScope
         0 |-> scope(
           "sum_product" |-> closureVal(
             ("numbers", .ParamNames),
             Assign(Name("total"), Int(0))
             Assign(Name("product"), Int(1))
             Assign(Name("number"), Int(0))
             For(Name("number"), Name("numbers"),
               AugAssign(Name("total"), "+", Name("number"))
               AugAssign(Name("product"), "+", Name("number")) .Stmts)
             Return(TupleExpr(Name("total"), Name("product"), .Exprs)) .Stmts,
             0),
           parent(-1)) )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
