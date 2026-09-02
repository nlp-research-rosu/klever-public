requires "verification.k"

module SPEC-UNICODE-PYTHON-RESULT
  imports VERIFICATION

  // This is the result both actual Python implementations produce.
  claim [python-selects-first]:
    <k>
      run(
        solutionProgram,
        args(
          pyList(pyStr("🙂") :: .StrVals),
          pyList(pyStr("ab") :: .StrVals)))
      => pyList(pyStr("🙂") :: .StrVals)
    </k>
endmodule
