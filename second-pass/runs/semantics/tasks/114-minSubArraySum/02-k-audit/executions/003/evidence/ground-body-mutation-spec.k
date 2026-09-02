requires "verification-body-mutation.k"

module LOOP-BODY-MUTATION-GROUND-SPEC
  imports VERIFICATION-BASE

  // Satisfiable witness: the mutated body subtracts 1 from current=0, so the
  // real final current/smallest are -1, while the original summary requires 1.
  claim
    <k>
      #loop(
        list(intVals(iCons(1, .IntSeq))),
        Name("value"),
        kadaneBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        (("nums" |-> list(intVals(iCons(1, .IntSeq))))
         ("smallest" |-> 1)
         ("current" |-> 0)
         ("value" |-> 0))
          =>
        (("nums" |-> list(intVals(iCons(1, .IntSeq))))
         ("smallest" |-> 1)
         ("current" |-> 1)
         ("value" |-> 1)),
        parent(0))
    </scopes>
endmodule
