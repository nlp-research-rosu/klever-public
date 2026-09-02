requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact syntactic abbreviations for the translated solution.py body.
  syntax Stmts ::= "sumSquaresLoopBody" [macro]
  rule sumSquaresLoopBody
    => If(
         Compare(BinOp("%", Name("index"), Int(3)), CmpOp("==", Int(0))),
         AugAssign(
           Name("result"),
           "+",
           BinOp("*", Name("value"), Name("value")))
         .Stmts,
         If(
           Compare(BinOp("%", Name("index"), Int(4)), CmpOp("==", Int(0))),
           AugAssign(
             Name("result"),
             "+",
             BinOp(
               "*",
               BinOp("*", Name("value"), Name("value")),
               Name("value")))
           .Stmts,
           AugAssign(Name("result"), "+", Name("value"))
           .Stmts)
         .Stmts)
       AugAssign(Name("index"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "sumSquaresFunctionBody" [macro]
  rule sumSquaresFunctionBody
    => Assign(Name("result"), Int(0))
       Assign(Name("index"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), sumSquaresLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Stmt ::= "sumSquaresDef" [macro]
  rule sumSquaresDef
    => FuncDef("sum_squares", Params("lst"), sumSquaresFunctionBody)

  // Domain predicate: exactly the finite ValSeq values whose elements are Int.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool notBool isRefV(V) andBool allInts(REST)

  // A guarded total projection following K's total-projection idiom.  It
  // exposes the Int subsort only on paths where isInt has been established.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(I:Int) => I
    [simplification]

  rule projectIntTotal(projectIntTotal(V:Val)) => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twins of MPY-INT's Int multiplication and addition.
  // They do not change either operation; they expose the static Int operands
  // carried by symbolic Val variables after allInts has supplied the guards.
  rule applyBin("*", V:Val, W:Val)
    => projectIntTotal(V) *Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  rule applyBin("+", I:Int, V:Val)
    => I +Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  // Mathematical contribution of the element at index I.
  syntax Int ::= squareContribution(Int, Int) [function, total]
  rule squareContribution(V:Int, I:Int)
    => V *Int V
    requires pyMod(I, 3) ==Int 0
  rule squareContribution(V:Int, I:Int)
    => (V *Int V) *Int V
    requires pyMod(I, 3) =/=Int 0
      andBool pyMod(I, 4) ==Int 0
  rule squareContribution(V:Int, I:Int)
    => V
    requires pyMod(I, 3) =/=Int 0
      andBool pyMod(I, 4) =/=Int 0

  // Exact tail-recursive fold over the remaining integer-valued sequence.
  // The complementary non-Int case totalizes the mathematical helper outside
  // the theorem's allInts domain; it is never used by either positive claim.
  syntax Int ::= sumSquaresAcc(ValSeq, Int, Int) [function, total]
  rule sumSquaresAcc(.ValSeq, _I:Int, ACC:Int) => ACC
  rule sumSquaresAcc(vCons(V:Val, REST:ValSeq), I:Int, ACC:Int)
    => sumSquaresAcc(
         REST,
         I +Int 1,
         ACC +Int squareContribution(projectIntTotal(V), I))
    requires isInt(V)
  rule sumSquaresAcc(vCons(V:Val, _REST:ValSeq), _I:Int, _ACC:Int)
    => 0
    requires notBool isInt(V)
endmodule
