requires "verification.k"

module SPEC
  imports VERIFICATION

  // Recurring for-loop head.  "number" is present after the first iteration;
  // the entry claim executes that first step directly, then uses this
  // circularity for the arbitrary remaining suffix.
  claim [loop-invariant]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        AugAssign(Name("total"), "+", Name("number"))
        AugAssign(Name("product"), "*", Name("number"))
      )
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "numbers" |-> list(INPUT:ValSeq)
        "number"  |-> (OLD:Val => ?LAST:Val)
        "total"   |-> (S:Int => sumFrom(VS, S))
        "product" |-> (P:Int => productFrom(VS, P))
        .Map,
        parent(0)
      )
      ...
    </scopes>
    requires allInts(VS)

  // Full entry theorem.  It starts from the supplied semantics' initial state,
  // loads the exact translated implementation, invokes the exact binding, and
  // covers every finite ValSeq whose elements are all semantic Int values.
  claim [sum-product]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Tuple")
        FuncDef("sum_product", Params("numbers"),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(1))
          For(Name("number"), Name("numbers"),
            AugAssign(Name("total"), "+", Name("number"))
            AugAssign(Name("product"), "*", Name("number")))
          Return(TupleExpr(Name("total"), Name("product"))))
      ))
      ~> Call(Name("sum_product"), list(VS:ValSeq))
      =>
      tuple(vCons(sumFrom(VS, 0),
            vCons(productFrom(VS, 1), .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        =>
        "sum_product" |->
          closureVal(
            "numbers", .ParamNames,
            Assign(Name("total"), Int(0))
            Assign(Name("product"), Int(1))
            For(Name("number"), Name("numbers"),
              AugAssign(Name("total"), "+", Name("number"))
              AugAssign(Name("product"), "*", Name("number")))
            Return(TupleExpr(Name("total"), Name("product"))),
            0
          ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
