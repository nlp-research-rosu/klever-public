requires "connection.k"

module AUDIT-UNICODE-MODEL
  imports CONNECTION

  // CPython reports "é".islower() == True.  The supplied ASCII-oriented
  // model reports false for code point 233 because it has no ASCII lowercase.
  claim [latin-small-e-acute-is-not-lower-in-model]:
    <k>
      #applyK(
        toCall(boundMethodV(str(iCons(233, .IntSeq)), "islower")),
        .Vals)
      =>
      false
    </k>
endmodule
