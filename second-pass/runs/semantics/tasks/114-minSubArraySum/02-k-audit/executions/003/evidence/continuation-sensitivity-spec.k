requires "verification.k"

module CONTINUATION-SENSITIVITY-BASE-SPEC
  imports VERIFICATION-BASE

  claim
    <k>
      #loop(
        list(intVals(iCons(1, iCons(-2, .IntSeq)))),
        Name("value"),
        kadaneBody)
      ~> Assign(Name("after"), Int(99))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        (("nums" |-> list(intVals(iCons(1, iCons(-2, .IntSeq)))))
         ("smallest" |-> 1)
         ("current" |-> 0)
         ("value" |-> 0)
         ("after" |-> 0))
          =>
        (("nums" |-> list(intVals(iCons(1, iCons(-2, .IntSeq)))))
         ("smallest" |-> -2)
         ("current" |-> -2)
         ("value" |-> -2)
         ("after" |-> 99)),
        parent(0))
    </scopes>
endmodule

module CONTINUATION-SENSITIVITY-BRIDGE-SPEC
  imports VERIFICATION

  claim
    <k>
      #loop(
        list(intVals(iCons(1, iCons(-2, .IntSeq)))),
        Name("value"),
        kadaneBody)
      ~> Assign(Name("after"), Int(99))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        (("nums" |-> list(intVals(iCons(1, iCons(-2, .IntSeq)))))
         ("smallest" |-> 1)
         ("current" |-> 0)
         ("value" |-> 0)
         ("after" |-> 0))
          =>
        (("nums" |-> list(intVals(iCons(1, iCons(-2, .IntSeq)))))
         ("smallest" |-> -2)
         ("current" |-> -2)
         ("value" |-> -2)
         ("after" |-> 99)),
        parent(0))
    </scopes>
endmodule
