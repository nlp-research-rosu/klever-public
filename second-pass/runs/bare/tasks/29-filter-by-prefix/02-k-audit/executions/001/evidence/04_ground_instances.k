module GROUND-INSTANCES
  imports SEMANTIC

  // Ground instance of program-correct:
  // INPUT = ["abc", "bcd", "cde", "array"], PREFIX = "a".
  claim
    <k> solutionProgram() => .K </k>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    <input>
      cons("abc", cons("bcd", cons("cde", cons("array", nil))))
    </input>
    <prefix> "a" </prefix>
    <output> noOutput
      => listVal(cons("abc", cons("array", nil)))
    </output>
    [label(ground-program)]

  // Ground instance of loop-correct:
  // ACC = ["prior"], remaining INPUT = ["abc", "b"], PREFIX = "a".
  claim
    <k> (loop("string", loopBody(), cons("abc", cons("b", nil)))
         ~> (Return(Name("result")) .Stmts) ~> functionEnd ~> .K)
      => .K </k>
    <env> ("prefix" |-> strVal("a")
           "result" |-> listVal(cons("prior", nil))) => ?_ </env>
    <functions> .Map </functions>
    <input> nil </input>
    <prefix> "a" </prefix>
    <output> noOutput
      => listVal(cons("prior", cons("abc", nil)))
    </output>
    [label(ground-loop)]
endmodule
