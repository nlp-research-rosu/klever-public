requires "verification.k"

module SUM-PRODUCT-LOOP-SPEC
  imports SUM-PRODUCT-VERIFICATION

  // Generalized loop invariant.  It states both accumulator equations and
  // tracks the loop target so the circularity matches the next iteration.
  claim [loop-correct]:
    <k>
      #loop(list(intVals(IS)), Name("number"), sumProductLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(GLOBAL:Map, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT:Val
        "total" |-> SUM:Int
        "product" |-> PRODUCT:Int
        "number" |-> CURRENT:Int,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(GLOBAL, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT
        "total" |-> intSeqSumFrom(SUM, IS)
        "product" |-> intSeqProductFrom(PRODUCT, IS)
        "number" |-> lastInt(IS, CURRENT),
        parent(0))
    </scopes>

endmodule

module SUM-PRODUCT-FUNCTION-SPEC
  imports SUM-PRODUCT-LEMMA

  // End-to-end theorem over the exact translated module and an arbitrary
  // finite sequence of mathematical integers.  SUM-PRODUCT-LEMMA is the
  // staged rewrite form of loop-correct, which prove.sh proves first.
  claim [function-correct]:
    <k>
      #loadAll(sumProductModule)
      ~> Call(Name("sum_product"), list(intVals(IS)))
      => tuple(vCons(intSeqSumFrom(0, IS),
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
