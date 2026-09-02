requires "verification.k"

module SPEC
  imports VERIFICATION

  // sum(map(len, ...)) is precisely the sum of every string's length.
  claim <k> totalChars(.StrVals) => 0 </k>

  claim <k>
          totalChars(pyStr(S) :: REST)
        => lengthString(S) +Int totalChars(REST)
        </k>

  // If the first total is no greater, total_match returns the first list.
  claim <k>
          run(solutionProgram,
              args(pyList(LIST1), pyList(LIST2)))
        => pyList(LIST1)
        </k>
    requires totalChars(LIST1) <=Int totalChars(LIST2)

  // If the second total is strictly smaller, it is returned.
  claim <k>
          run(solutionProgram,
              args(pyList(LIST1), pyList(LIST2)))
        => pyList(LIST2)
        </k>
    requires totalChars(LIST1) >Int totalChars(LIST2)

  // The tie behavior from the natural-language contract is explicit.
  claim <k>
          run(solutionProgram,
              args(pyList(LIST1), pyList(LIST2)))
        => pyList(LIST1)
        </k>
    requires totalChars(LIST1) ==Int totalChars(LIST2)
endmodule
