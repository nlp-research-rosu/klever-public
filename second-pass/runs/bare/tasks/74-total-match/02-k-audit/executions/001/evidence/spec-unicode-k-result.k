requires "verification.k"

module SPEC-UNICODE-K-RESULT
  imports VERIFICATION

  // K accepts this false description of real Python execution.
  claim [k-selects-second]:
    <k>
      run(
        solutionProgram,
        args(
          pyList(pyStr("🙂") :: .StrVals),
          pyList(pyStr("ab") :: .StrVals)))
      => pyList(pyStr("ab") :: .StrVals)
    </k>
endmodule
