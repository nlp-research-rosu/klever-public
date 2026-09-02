module SPEC
  imports SEMANTIC

  // Loop invariant: ACC is the stable result accumulated before INPUT.
  claim
    <k> (loop("string", loopBody(), INPUT)
         ~> (Return(Name("result")) .Stmts) ~> functionEnd ~> .K)
      => .K </k>
    <env> ("prefix" |-> strVal(PREFIX)
           "result" |-> listVal(ACC)
           _RESTENV) => ?_ </env>
    <functions> _FUNCTIONS </functions>
    <input> _ALLINPUT </input>
    <prefix> PREFIX </prefix>
    <output> noOutput => listVal(filterAcc(INPUT, PREFIX, ACC)) </output>
    [label(loop-correct)]

  // End-to-end correctness for the exact translated solution and all inputs.
  claim
    <k> solutionProgram() => .K </k>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    <input> INPUT </input>
    <prefix> PREFIX </prefix>
    <output> noOutput => listVal(filterByPrefix(INPUT, PREFIX)) </output>
    [label(program-correct)]
endmodule
