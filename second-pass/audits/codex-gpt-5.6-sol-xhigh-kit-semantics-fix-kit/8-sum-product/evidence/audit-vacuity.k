requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Reviewer-authored fresh mutation. The satisfying input [1,2,3,4]
  // returns (10,24); only the product obligation is changed to the false 25.
  claim [false-example-product]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Tuple")
        FuncDef("sum_product", Params("numbers"),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(1))
          Assign(Name("number"), Int(0))
          For(Name("number"), Name("numbers"),
            Assign(Name("total"),
              BinOp("+", Name("total"), Name("number")))
            Assign(Name("product"),
              BinOp("*", Name("product"), Name("number")))
            .Stmts)
          Return(TupleExpr(Name("total"), Name("product"), .Exprs))
          .Stmts)
        .Stmts))
      ~> Call(Name("sum_product"),
              (list(intVals(iList(1, iList(2, iList(3, iList(4, .IntList)))))), .Exprs))
      => tuple(vCons(10, vCons(25, .ValSeq)))
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
endmodule
