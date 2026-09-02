module SPEC-VACUITY
  imports SEMANTIC

  // Unchanged support lemma, independently proved in 03_positive_proofs.log.
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
    [label(loop-correct-vacuity-support)]

  // Deliberately false: append an extra sentinel to every returned list.
  claim
    <k> solutionProgram() => .K </k>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    <input> INPUT </input>
    <prefix> PREFIX </prefix>
    <output> noOutput
      => listVal(appendOne(filterByPrefix(INPUT, PREFIX), "__AUDIT_FALSE__"))
    </output>
    [label(false-program-result)]
endmodule
