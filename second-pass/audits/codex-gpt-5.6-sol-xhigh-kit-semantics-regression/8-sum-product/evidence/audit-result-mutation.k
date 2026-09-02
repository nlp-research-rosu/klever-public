requires "verification.k"

module AUDIT-RESULT-MUTATION
  imports VERIFICATION

  // Satisfiable witness: the original program called on the empty integer list.
  // Deliberately false obligation: empty product is changed from 1 to 2.
  claim [false-empty-product]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", ("List", "Tuple", .ParamNames))
        FuncDef("sum_product", Params("numbers", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(1))
          Assign(Name("number"), Int(0))
          For(Name("number"), Name("numbers"),
            AugAssign(Name("total"), "+", Name("number"))
            AugAssign(Name("product"), "*", Name("number")) .Stmts)
          Return(TupleExpr(Name("total"), Name("product"), .Exprs)) .Stmts)
        .Stmts))
      ~> Call(Name("sum_product"), (list(.ValSeq), .Exprs))
      => tuple(vCons(0, vCons(2, .ValSeq)))
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
               AugAssign(Name("product"), "*", Name("number")) .Stmts)
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
