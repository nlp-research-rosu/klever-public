requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact summary of the remaining structural string iteration. P2 and P1
  // are the character codes two and one positions before the next character.
  syntax Bool ::= scanHappy(IntSeq, Int, Int, Int) [function, total]
  rule scanHappy(.IntSeq, _:Int, _:Int, _:Int) => true
  rule scanHappy(iCons(C:Int, REST:IntSeq), I:Int, _:Int, P1:Int)
    => scanHappy(REST, I +Int 1, P1, C)
    requires I <Int 2
  rule scanHappy(iCons(C:Int, REST:IntSeq), I:Int, P2:Int, P1:Int)
    => (C =/=Int P1)
       andBool (C =/=Int P2)
       andBool (P1 =/=Int P2)
       andBool scanHappy(REST, I +Int 1, P1, C)
    requires I >=Int 2
endmodule
