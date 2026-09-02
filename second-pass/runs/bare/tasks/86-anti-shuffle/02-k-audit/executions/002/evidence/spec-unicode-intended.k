module UNICODE-INTENDED-SPEC
  imports VERIFICATION

  // Python treats Ω as one character; sorting a one-character word is identity.
  claim [unicode-single-character]:
    <python>
      <k> run(solutionProgram, "Ω") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "Ω" </result>
    </python>
endmodule
