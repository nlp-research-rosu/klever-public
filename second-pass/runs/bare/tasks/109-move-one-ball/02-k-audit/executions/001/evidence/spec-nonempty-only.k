requires "semantic.k"

module SPEC-NONEMPTY-ONLY
  imports HUMAN-EVAL

  claim [nonempty]:
        <k> theSolution
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

