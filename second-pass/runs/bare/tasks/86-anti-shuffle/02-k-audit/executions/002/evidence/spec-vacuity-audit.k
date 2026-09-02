module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // False on the satisfiable entry state with input "hello":
  // both Python implementations and the K semantics return "ehllo".
  claim [false-hello-result]:
    <python>
      <k> run(solutionProgram, "hello") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "ehllp" </result>
    </python>
endmodule
