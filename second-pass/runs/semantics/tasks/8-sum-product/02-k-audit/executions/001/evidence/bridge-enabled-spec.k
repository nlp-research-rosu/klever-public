requires "verification.k"

module LOOP-BRIDGE-ENABLED-WITNESS
  imports SUM-PRODUCT-LEMMA

  // Deliberately false sensitivity claim over the same state as
  // bridge-fixed-spec.k. The promoted rule requires <env> 1, so it must not
  // fabricate scope-1 updates when <env> is 0. Expected result: proof failure
  // with the fixed scope-0 updates visible in the residual.
  claim [bridge-env-zero]:
    <k>
      #loop(
        list(intVals(iCons(2, .IntSeq))),
        Name("number"),
        sumProductLoopBody)
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "total" |-> 100
        "product" |-> 7
        "number" |-> 9,
        parent(-1))
      1 |-> scope(
        "numbers" |-> list(intVals(iCons(2, .IntSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "total" |-> 100
        "product" |-> 7
        "number" |-> 9,
        parent(-1))
      1 |-> scope(
        "numbers" |-> list(intVals(iCons(2, .IntSeq)))
        "total" |-> 2
        "product" |-> 2
        "number" |-> 2,
        parent(0))
    </scopes>
endmodule
