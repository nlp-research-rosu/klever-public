requires "connection-definition.k"

module BRIDGE-NEGATIVE
  imports CONNECTION-DEFINITION

  // Deliberately false opposite interpretations of the two bridge values.
  claim [wrong-int-equality]:
    <k> applyCmp("==", 2, 2) => false </k>

  claim [wrong-int-unary-minus]:
    <k> applyUn("-", 2) => 2 </k>
endmodule
