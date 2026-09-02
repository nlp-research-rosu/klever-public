requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the correct result on [2, 3] is (5, 6), not (6, 6).
  claim [false-postcondition]:
    <k>
      Call(
        Name("sum_product"),
        list(vCons(2, vCons(3, .ValSeq)))
      )
      =>
      tuple(vCons(6, vCons(6, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
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
endmodule
