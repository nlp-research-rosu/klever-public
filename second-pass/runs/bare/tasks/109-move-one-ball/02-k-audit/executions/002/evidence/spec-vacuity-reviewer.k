requires "semantic.k"

module SPEC-VACUITY-REVIEWER
  imports HUMAN-EVAL

  // Deliberately false result obligation.  The satisfying input
  // 3 :: 4 :: 5 :: 1 :: 2 :: .IList returns true, not false.
  claim <k> theSolution
          => bVal(false) ~> .K
        </k>
        <input> I :: IS </input>
        <env> .Map
          => "arr" |-> listVal(I :: IS)
             "drops" |-> iVal(cyclicDrops(I :: IS))
             "previous" |-> iVal(last(I :: IS))
             "value" |-> iVal(last(I :: IS))
        </env>
endmodule
