requires "reference-semantics/semantics.k"

module DOUBLE-THE-DIFFERENCE-VERIFICATION
  imports MPY

  // A symbolic sequence of exactly the numeric values admitted by the prompt.
  // Keeping the Int/Float choice in the constructor lets kprove split the
  // sequence structurally instead of treating an arbitrary Val as non-integer.
  syntax NumSeq ::= ".NumSeq"
                  | iNum(Int, NumSeq)
                  | fNum(Float, NumSeq)

  // numVals is a proof-domain representation of a list's ValSeq.  Its iterator
  // rules expose the NumSeq constructor directly to symbolic narrowing.
  syntax ValSeq ::= numVals(NumSeq)
  rule <k> #iterNext(list(numVals(.NumSeq)))
        => #iterDone ... </k>
  rule <k> #iterNext(list(numVals(iNum(I, REST))))
        => #iterYield(I, list(numVals(REST))) ... </k>
  rule <k> #iterNext(list(numVals(fNum(F, REST))))
        => #iterYield(F, list(numVals(REST))) ... </k>

  syntax Int ::= oddSquare(Int) [function, total]
  rule oddSquare(I)
    => #if I >Int 0 andBool pyMod(I, 2) ==Int 1
       #then I *Int I
       #else 0
       #fi

  syntax Int ::= doubleDifferenceSpec(NumSeq) [function, total]
  rule doubleDifferenceSpec(.NumSeq)       => 0
  rule doubleDifferenceSpec(iNum(I, REST))
    => oddSquare(I) +Int doubleDifferenceSpec(REST)
  rule doubleDifferenceSpec(fNum(_F, REST))
    => doubleDifferenceSpec(REST)

  syntax Val ::= finalNumber(NumSeq, Val) [function, total]
  rule finalNumber(.NumSeq, OLD)          => OLD
  rule finalNumber(iNum(I, REST), _OLD)   => finalNumber(REST, I)
  rule finalNumber(fNum(F, REST), _OLD)   => finalNumber(REST, F)
endmodule
