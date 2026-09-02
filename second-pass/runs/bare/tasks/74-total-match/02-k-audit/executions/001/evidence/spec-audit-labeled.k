requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  claim [empty-total]:
    <k> totalChars(.StrVals) => 0 </k>

  claim [cons-total]:
    <k>
      totalChars(pyStr(S) :: REST)
      => lengthString(S) +Int totalChars(REST)
    </k>

  claim [first-when-no-greater]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST1)
    </k>
    requires totalChars(LIST1) <=Int totalChars(LIST2)

  claim [second-when-smaller]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST2)
    </k>
    requires totalChars(LIST1) >Int totalChars(LIST2)

  claim [first-on-tie]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST1)
    </k>
    requires totalChars(LIST1) ==Int totalChars(LIST2)
endmodule
