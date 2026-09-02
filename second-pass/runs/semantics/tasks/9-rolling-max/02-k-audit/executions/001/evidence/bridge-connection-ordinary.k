requires "verification-no-bridges.k"

module BRIDGE-CONNECTION
  imports VERIFICATION

  // Universal connection theorems for the complete two bridge domains.
  // The candidate bridge rules are absent from the imported definition.
  claim [empty-iterator-connection]:
    <k> #iterNext(list(intsVS(.IntSeq))) ~> CONT
      => #iterDone ~> CONT
    </k>

  claim [cons-iterator-connection]:
    <k> #iterNext(list(intsVS(iCons(I:Int, R:IntSeq)))) ~> CONT
      => #iterYield(I, list(intsVS(R))) ~> CONT
    </k>

  // A satisfiable observable suffix confirms that the accelerated transition
  // neither consumes nor replaces the active continuation.
  claim [continuation-preservation-witness]:
    <k> #iterNext(list(intsVS(iCons(7, .IntSeq))))
         ~> Assign(Name("sentinel"), Int(9))
      => #iterYield(7, list(intsVS(.IntSeq)))
         ~> Assign(Name("sentinel"), Int(9))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
