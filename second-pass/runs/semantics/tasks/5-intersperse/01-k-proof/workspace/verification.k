requires "reference-semantics/semantics.k"

module INTERSPERSE-VERIFICATION
  imports MPY

  syntax ValSeq ::= intersperseAcc(ValSeq, ValSeq, Int) [function, total]
  rule intersperseAcc(ACC:ValSeq, .ValSeq, _:Int) => ACC
  rule intersperseAcc(.ValSeq, vCons(V:Val, REST:ValSeq), D:Int)
    => intersperseAcc(vCons(V, .ValSeq), REST, D)
  rule intersperseAcc(vCons(A:Val, AS:ValSeq),
                      vCons(V:Val, REST:ValSeq), D:Int)
    => intersperseAcc(
         valSeqConcat(
           valSeqConcat(vCons(A, AS), vCons(D, .ValSeq)),
           vCons(V, .ValSeq)),
         REST,
         D)

  syntax ValSeq ::= intersperseVS(ValSeq, Int) [function, total]
  rule intersperseVS(NUMBERS:ValSeq, D:Int)
    => intersperseAcc(.ValSeq, NUMBERS, D)

  syntax Val ::= lastNumber(Val, ValSeq) [function, total]
  rule lastNumber(OLD:Val, .ValSeq) => OLD
  rule lastNumber(_:Val, vCons(V:Val, REST:ValSeq))
    => lastNumber(V, REST)
endmodule
