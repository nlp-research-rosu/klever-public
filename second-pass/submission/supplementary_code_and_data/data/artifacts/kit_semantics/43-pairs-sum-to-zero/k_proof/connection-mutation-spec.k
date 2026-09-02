requires "connection-definition.k"

module CONNECTION-MUTATION-SPEC
  imports CONNECTION-DEFINITION

  claim [bad-int-equality]:
    <k> applyCmp("==", 2, 2) => false </k>

  claim [bad-int-unary-minus]:
    <k> applyUn("-", 2) => 2 </k>
endmodule
