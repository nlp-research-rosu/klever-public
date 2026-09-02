requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [total-empty]:
    <k> totalChars(.StrVals) => 0 </k>

  claim [total-step]:
    <k>
      totalChars(pyStr(S) :: REST)
      => lengthString(S) +Int totalChars(REST)
    </k>

  claim [first-le]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST1)
    </k>
    requires totalChars(LIST1) <=Int totalChars(LIST2)

  claim [second-lt]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST2)
    </k>
    requires totalChars(LIST1) >Int totalChars(LIST2)

  claim [tie-first]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST1)
    </k>
    requires totalChars(LIST1) ==Int totalChars(LIST2)
endmodule
