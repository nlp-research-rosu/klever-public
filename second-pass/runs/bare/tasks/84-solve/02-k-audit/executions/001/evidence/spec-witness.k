requires "semantic.k"

module SPEC-WITNESS
  imports SEMANTIC

  // Direct, satisfiable substitutions drawn from three entry-claim ranges.
  claim [witness-zero]:
    <k> checkInput(0) => true </k>

  claim [witness-example]:
    <k> checkInput(147) => true </k>

  claim [witness-endpoint]:
    <k> checkInput(10000) => true </k>
endmodule
