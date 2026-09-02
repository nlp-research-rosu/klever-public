requires "verification.k"

module SUM-PRODUCT-SPEC
  imports SUM-PRODUCT-VERIFICATION

  // ---- Loop invariant (circularity) — dual fold; sum_value / prod_value in the store.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("n"),
        AugAssign(Name("sum_value"),  "+", Name("n"))
        AugAssign(Name("prod_value"), "*", Name("n")))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "numbers" <- NV:Val ] [ "sum_value" <- SV:Int ] [ "prod_value" <- PV:Int ] [ "n" <- _:Val ], P:Parent) =>
        scope(.Map [ "numbers" <- NV ] [ "sum_value" <- ?SOut:Int ] [ "prod_value" <- ?POut:Int ] [ "n" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?SOut ==Int SV +Int sumSeq(intListOf(VS)) andBool ?POut ==Int PV *Int prodSeq(intListOf(VS))
    [all-path]

  // ---- Entry claim — result = sum_product(list(VS)) == (sumSeq(intListOf(VS)), prodSeq(intListOf(VS))).
  claim
    <k>
      FuncDef("sum_product", Params("numbers"),
        Assign(Name("sum_value"), Int(0))
        Assign(Name("prod_value"), Int(1))
        For(Name("n"), Name("numbers"),
          AugAssign(Name("sum_value"),  "+", Name("n"))
          AugAssign(Name("prod_value"), "*", Name("n")))
        Return(TupleExpr(Name("sum_value"), Name("prod_value"))))
      Assign(Name("result"), Call(Name("sum_product"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sum_product" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==K tuple(vCons(sumSeq(intListOf(VS)), vCons(prodSeq(intListOf(VS)), .ValSeq)))
    [all-path]
endmodule
