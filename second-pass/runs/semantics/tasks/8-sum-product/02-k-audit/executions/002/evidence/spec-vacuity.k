requires "verification.k"

module AUDIT-SUM-PRODUCT-VACUITY-SPEC
  imports SUM-PRODUCT-LEMMA

  claim [false-sum-plus-one]:
    <k>
      #loadAll(sumProductModule)
      ~> Call(Name("sum_product"), list(intVals(IS)))
      => tuple(vCons(intSeqSumFrom(0, IS) +Int 1,
               vCons(intSeqProductFrom(1, IS), .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "sum_product" |-> closureVal("numbers", sumProductBody, 0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
