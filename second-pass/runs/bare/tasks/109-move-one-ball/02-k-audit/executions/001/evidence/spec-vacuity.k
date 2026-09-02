requires "semantic.k"

module SPEC-VACUITY
  imports HUMAN-EVAL

  // Deliberately false: require the opposite Boolean result while retaining
  // the original satisfiable nonempty precondition and exact final state.
  claim [opposite-result]:
        <k> theSolution
          => bVal(notBool rotationSortable(I :: IS)) ~> .K
        </k>
        <input> I :: IS </input>
        <env> .Map
          => "arr" |-> listVal(I :: IS)
             "drops" |-> iVal(cyclicDrops(I :: IS))
             "previous" |-> iVal(last(I :: IS))
             "value" |-> iVal(last(I :: IS))
        </env>
endmodule

