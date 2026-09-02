requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // True exactly for strings in the prompt's input domain.
  syntax Bool ::= parenCodes(IntSeq) [function, total]
  rule parenCodes(.IntSeq) => true
  rule parenCodes(iCons(C:Int, CS:IntSeq))
    => (C ==Int 40 orBool C ==Int 41) andBool parenCodes(CS)

  // Exact summaries of the source loop's three changing locals.
  // Code 40 is '('; every other code follows the source program's else branch.
  syntax Int ::= nextBalance(Int, Int) [function, total]
  rule nextBalance(C:Int, B:Int) => B +Int 1
    requires C ==Int 40
    [simplification]
  rule nextBalance(C:Int, B:Int) => B -Int 1
    requires C =/=Int 40
    [simplification]

  syntax Int ::= scanBalance(IntSeq, Int) [function, total]
  rule scanBalance(.IntSeq, B:Int) => B
  rule scanBalance(iCons(C:Int, CS:IntSeq), B:Int)
    => scanBalance(CS, nextBalance(C, B))

  syntax Int ::= nextMinimum(Int, Int) [function, total]
  rule nextMinimum(N:Int, M:Int) => N
    requires N <Int M
  rule nextMinimum(N:Int, M:Int) => M
    requires N >=Int M

  syntax Int ::= scanMinimum(IntSeq, Int, Int) [function, total]
  rule scanMinimum(.IntSeq, _B:Int, M:Int) => M
  rule scanMinimum(iCons(C:Int, CS:IntSeq), B:Int, M:Int)
    => scanMinimum(
         CS,
         nextBalance(C, B),
         nextMinimum(nextBalance(C, B), M))

  syntax Val ::= scanLast(IntSeq, Val) [function, total]
  rule scanLast(.IntSeq, OLD:Val) => OLD
  rule scanLast(iCons(C:Int, CS:IntSeq), _OLD:Val)
    => scanLast(CS, str(iCons(C, .IntSeq)))

  // A parenthesis string is good iff its final balance is zero and no prefix
  // has negative balance.
  syntax Bool ::= goodParens(IntSeq) [function, total]
  rule goodParens(CS:IntSeq)
    => scanBalance(CS, 0) ==Int 0
       andBool scanMinimum(CS, 0, 0) >=Int 0

  syntax Bool ::= possibleMatch(IntSeq, IntSeq) [function, total]
  rule possibleMatch(A:IntSeq, B:IntSeq)
    => goodParens(seqConcat(A, B)) orBool goodParens(seqConcat(B, A))

  syntax Str ::= matchAnswer(IntSeq, IntSeq) [function, total]
  rule matchAnswer(A:IntSeq, B:IntSeq)
    => str(iCons(89, iCons(101, iCons(115, .IntSeq))))
    requires possibleMatch(A, B)
  rule matchAnswer(A:IntSeq, B:IntSeq)
    => str(iCons(78, iCons(111, .IntSeq)))
    requires notBool possibleMatch(A, B)
endmodule
