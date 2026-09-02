requires "verification.k"

module AUDIT-LEMMA-SCOPE-PROBE
  imports SUM-PRODUCT-VERIFICATION

  claim [lemma-scope-connection]:
    <k>
      #loop(list(intVals(IS)), Name("number"), sumProductLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(GLOBAL:Map, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT:Val
        "total" |-> SUM:Int
        "product" |-> PRODUCT:Int
        "number" |-> CURRENT:Int,
        parent(0))
      REST:Map
      =>
      0 |-> scope(GLOBAL, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT
        "total" |-> intSeqSumFrom(SUM, IS)
        "product" |-> intSeqProductFrom(PRODUCT, IS)
        "number" |-> lastInt(IS, CURRENT),
        parent(0))
      REST
    </scopes>
endmodule
