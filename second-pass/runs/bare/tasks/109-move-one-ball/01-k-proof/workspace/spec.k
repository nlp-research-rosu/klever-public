requires "semantic.k"

module HUMAN-EVAL-SPEC
  imports HUMAN-EVAL

  // Empty input is explicitly required to return true.
  claim <k> theSolution => bVal(true) ~> .K </k>
        <input> .IList </input>
        <env> .Map => "arr" |-> listVal(.IList) </env>

  // For every nonempty integer list, the translated program computes the
  // independent rotation-sortability predicate from verification.k.
  claim <k> theSolution
          => bVal(rotationSortable(I :: IS)) ~> .K
        </k>
        <input> I :: IS </input>
        <env> .Map
          => "arr" |-> listVal(I :: IS)
             "drops" |-> iVal(cyclicDrops(I :: IS))
             "previous" |-> iVal(last(I :: IS))
             "value" |-> iVal(last(I :: IS))
        </env>
endmodule
