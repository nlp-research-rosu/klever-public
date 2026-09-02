// reference/src/semantics/int.k — MPY-INT
// Int cases of the operator dispatch; Python // and % are floored (pyMod).

module MPY-INT
  imports MPY-CORE

  rule applyUn("-", I:Int) => 0 -Int I

  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
  // bool is a subtype of int: any Bool operand promotes to 0/1 and re-dispatches
  // to the Int cases (the "+" mixed cases above are kept, so "+" is excluded here
  // to avoid a duplicate rule — Bool + Bool still promotes via the Bool x Bool rule).
  rule applyBin(OP:String, B1:Bool, B2:Bool) => applyBin(OP, boolAsInt(B1), boolAsInt(B2))
       requires isArithOp(OP)
  rule applyBin(OP:String, B:Bool, I:Int)    => applyBin(OP, boolAsInt(B), I)
       requires isArithOp(OP) andBool OP =/=String "+"
  rule applyBin(OP:String, I:Int, B:Bool)    => applyBin(OP, I, boolAsInt(B))
       requires isArithOp(OP) andBool OP =/=String "+"
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0

  syntax Int ::= pyMod(Int, Int) [function]
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2

  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
endmodule
