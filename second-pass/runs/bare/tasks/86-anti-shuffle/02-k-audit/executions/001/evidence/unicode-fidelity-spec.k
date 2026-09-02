module UNICODE-FIDELITY-SPEC
  imports VERIFICATION

  // UTF-8 bytes for U+03A9. The identity baseline preserves CE A9, and both
  // real Python implementations preserve the single code point, but the
  // submitted semantics splits and sorts the bytes to A9 CE.
  claim [python-unicode-result]:
    <python>
      <k> run(solutionProgram, "\xce\xa9") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "\xce\xa9" </result>
    </python>
endmodule
