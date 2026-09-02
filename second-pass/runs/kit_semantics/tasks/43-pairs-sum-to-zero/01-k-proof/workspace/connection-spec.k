requires "connection-definition.k"

module CONNECTION-SPEC
  imports CONNECTION-DEFINITION

  claim [int-equality]:
    <k> applyCmp("==", I:Int, J:Int) => intProj(I) ==Int J ... </k>

  claim [int-unary-minus]:
    <k> applyUn("-", I:Int) => 0 -Int intProj(I) ... </k>
endmodule
