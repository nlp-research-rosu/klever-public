requires "semantic.k"

module SPEC-EMPTY-ONLY
  imports HUMAN-EVAL

  claim [empty]:
        <k> theSolution => bVal(true) ~> .K </k>
        <input> .IList </input>
        <env> .Map => "arr" |-> listVal(.IList) </env>
endmodule

