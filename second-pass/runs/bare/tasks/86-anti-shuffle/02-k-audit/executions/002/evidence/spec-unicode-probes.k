module UNICODE-PROBES
  imports VERIFICATION

  claim [escaped-identity]:
    <python>
      <k> run(solutionProgram, "\u03a9") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "\u03a9" </result>
    </python>

  claim [escaped-byte-reversal]:
    <python>
      <k> run(solutionProgram, "\u03a9") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "\xa9\xce" </result>
    </python>

  claim [escaped-empty-false]:
    <python>
      <k> run(solutionProgram, "\u03a9") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "" </result>
    </python>

  claim [escaped-greek-order]:
    <python>
      <k> run(solutionProgram, "\u03b2\u03a9") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "\u03a9\u03b2" </result>
    </python>

  claim [escaped-astral-order]:
    <python>
      <k> run(solutionProgram, "\U0001f600a\U0001f98a") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "a\U0001f600\U0001f98a" </result>
    </python>
endmodule
