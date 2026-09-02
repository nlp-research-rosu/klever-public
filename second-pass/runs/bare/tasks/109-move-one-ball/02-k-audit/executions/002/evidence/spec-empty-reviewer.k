requires "semantic.k"

module SPEC-EMPTY-REVIEWER
  imports HUMAN-EVAL

  claim <k> theSolution => bVal(true) ~> .K </k>
        <input> .IList </input>
        <env> .Map => "arr" |-> listVal(.IList) </env>
endmodule
