requires "verification.k"

module LOOP-BRIDGE-FIXED-WITNESS
  imports SUM-PRODUCT-VERIFICATION

  // One-element integer input, but an environment value admitted by the
  // promoted lemma and excluded by the proved loop claim. Under fixed
  // semantics, target binding and AugAssign update scope 0.
  claim [fixed-env-zero]:
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
        "total" |-> 102
        "product" |-> 14
        "number" |-> 2,
        parent(-1))
      1 |-> scope(
        "numbers" |-> list(intVals(iCons(2, .IntSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0))
    </scopes>
endmodule
