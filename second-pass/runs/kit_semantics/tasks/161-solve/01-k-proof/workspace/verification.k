requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Constructor disjointness needed to simplify the reference isalpha rule
  // after string iteration has produced a one-character string.
  rule iCons(C:Int, .IntSeq) ==K .IntSeq => false
    [simplification]

  // Compile-time aliases for the exact AST emitted in solution.mpy.
  syntax Stmts ::= "loopBody" [macro]
  rule loopBody
    => Assign(
         Name("reversed_s"),
         BinOp("+", Name("c"), Name("reversed_s")))
       If(
         Call(Attribute(Name("c"), "isalpha"), .Exprs),
         AugAssign(
           Name("swapped"),
           "+",
           Call(Attribute(Name("c"), "swapcase"), .Exprs))
         Assign(Name("has_letter"), Bool(true))
         .Stmts,
         AugAssign(Name("swapped"), "+", Name("c"))
         .Stmts)
       .Stmts

  syntax Stmts ::= "solveBody" [macro]
  rule solveBody
    => Expr(
         Str("Toggle letter case, or reverse a string containing no letters."))
       Assign(Name("swapped"), Str(""))
       Assign(Name("reversed_s"), Str(""))
       Assign(Name("has_letter"), Bool(false))
       Assign(Name("c"), Str(""))
       For(Name("c"), Name("s"), loopBody)
       If(
         Name("has_letter"),
         Return(Name("swapped")) .Stmts,
         .Stmts)
       Return(Name("reversed_s"))
       .Stmts

  // Accumulator form of "some character is alphabetic".
  syntax Bool ::= charAlpha(Int) [function, total]
  rule charAlpha(C:Int)
    => notBool (iCons(C, .IntSeq) ==K .IntSeq)
       andBool allAlpha(iCons(C, .IntSeq))

  syntax Bool ::= alphaAcc(IntSeq, Bool) [function, total]
  rule alphaAcc(.IntSeq, FOUND:Bool) => FOUND
  rule alphaAcc(iCons(C:Int, REST:IntSeq), FOUND:Bool)
    => alphaAcc(REST, true)
    requires charAlpha(C)
    [simplification]
  rule alphaAcc(iCons(C:Int, REST:IntSeq), FOUND:Bool)
    => alphaAcc(REST, FOUND)
    requires notBool charAlpha(C)
    [simplification]

  // Accumulator form of the exact per-character transformation.
  syntax IntSeq ::= toggleAcc(IntSeq, IntSeq) [function, total]
  rule toggleAcc(.IntSeq, OUT:IntSeq) => OUT
  rule toggleAcc(iCons(C:Int, REST:IntSeq), OUT:IntSeq)
    => toggleAcc(
         REST,
         seqConcat(OUT, iCons(swapC(C), .IntSeq)))
    requires charAlpha(C)
    [simplification]
  rule toggleAcc(iCons(C:Int, REST:IntSeq), OUT:IntSeq)
    => toggleAcc(
         REST,
         seqConcat(OUT, iCons(C, .IntSeq)))
    requires notBool charAlpha(C)
    [simplification]

  // Exact final value of Python's for-loop target (initialized before the loop).
  syntax Str ::= lastChar(IntSeq, Str) [function, total]
  rule lastChar(.IntSeq, INITIAL:Str) => INITIAL
  rule lastChar(iCons(C:Int, REST:IntSeq), _:Str)
    => lastChar(REST, str(iCons(C, .IntSeq)))

  // The HumanEval result over the reference semantics' character model.
  syntax Str ::= solveResult(IntSeq) [function, total]
  rule solveResult(INPUT:IntSeq) => str(toggleAcc(INPUT, .IntSeq))
    requires alphaAcc(INPUT, false)
  rule solveResult(INPUT:IntSeq) => str(revIS(INPUT))
    requires notBool alphaAcc(INPUT, false)
endmodule
