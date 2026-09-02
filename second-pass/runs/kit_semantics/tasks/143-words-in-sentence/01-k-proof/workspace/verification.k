requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Compile-time aliases for the exact AST emitted in solution.mpy.
  syntax Expr ::= "#primeTuple" [macro]
  rule #primeTuple
    => TupleExpr(
         Int(2),  Int(3),  Int(5),  Int(7),  Int(11),
         Int(13), Int(17), Int(19), Int(23), Int(29),
         Int(31), Int(37), Int(41), Int(43), Int(47),
         Int(53), Int(59), Int(61), Int(67), Int(71),
         Int(73), Int(79), Int(83), Int(89), Int(97))

  syntax Stmt ::= "#emitSelected" [macro]
  rule #emitSelected
    => Assign(
         Name("result"),
         BinOp(
           "+",
           BinOp("+", Name("result"), Name("word")),
           Str(" ")))

  syntax Stmt ::= "#maybeEmit" [macro]
  rule #maybeEmit
    => If(
         Compare(
           Call(Name("len"), Name("word")),
           CmpOp("in", #primeTuple)),
         #emitSelected,
         .Stmts)

  syntax Stmt ::= "#scanBody" [macro]
  rule #scanBody
    => If(
         Compare(Name("char"), CmpOp("==", Str(" "))),
         #maybeEmit
         Assign(Name("word"), Str("")),
         Assign(
           Name("word"),
           BinOp("+", Name("word"), Name("char"))))

  syntax Stmts ::= "#wordsBody" [macro]
  rule #wordsBody
    => Assign(Name("result"), Str(""))
       Assign(Name("word"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("sentence"), #scanBody)
       #maybeEmit
       Return(Call(Attribute(Name("result"), "strip"), .Exprs))

  syntax Module ::= "#solutionModule" [macro]
  rule #solutionModule
    => Module(
         FuncDef(
           "words_in_sentence",
           Params("sentence"),
           #wordsBody))

  // The implementation's finite prime test. Under the prompt's length bound
  // every word length is at most 100, so these are exactly all possible primes.
  syntax Bool ::= primeLength(Int)
    [function, total, no-evaluators]
  rule primeLength(N) => true
    requires N ==Int 2  orBool N ==Int 3  orBool N ==Int 5
      orBool N ==Int 7  orBool N ==Int 11 orBool N ==Int 13
      orBool N ==Int 17 orBool N ==Int 19 orBool N ==Int 23
      orBool N ==Int 29 orBool N ==Int 31 orBool N ==Int 37
      orBool N ==Int 41 orBool N ==Int 43 orBool N ==Int 47
      orBool N ==Int 53 orBool N ==Int 59 orBool N ==Int 61
      orBool N ==Int 67 orBool N ==Int 71 orBool N ==Int 73
      orBool N ==Int 79 orBool N ==Int 83 orBool N ==Int 89
      orBool N ==Int 97
    [simplification]
  rule primeLength(N) => false
    requires notBool (
      N ==Int 2  orBool N ==Int 3  orBool N ==Int 5
      orBool N ==Int 7  orBool N ==Int 11 orBool N ==Int 13
      orBool N ==Int 17 orBool N ==Int 19 orBool N ==Int 23
      orBool N ==Int 29 orBool N ==Int 31 orBool N ==Int 37
      orBool N ==Int 41 orBool N ==Int 43 orBool N ==Int 47
      orBool N ==Int 53 orBool N ==Int 59 orBool N ==Int 61
      orBool N ==Int 67 orBool N ==Int 71 orBool N ==Int 73
      orBool N ==Int 79 orBool N ==Int 83 orBool N ==Int 89
      orBool N ==Int 97)
    [simplification]

  syntax IntSeq ::= emitWord(IntSeq, IntSeq) [function, total]
  rule emitWord(W:IntSeq, O:IntSeq)
    => #if primeLength(isLen(W))
       #then seqConcat(seqConcat(O, W), iCons(32, .IntSeq))
       #else O
       #fi

  // Exact fold summaries for the three locals changed by the character loop.
  // scanOutput excludes the final unterminated word; #maybeEmit after the loop
  // performs that final emission.
  syntax IntSeq ::= scanOutput(IntSeq, IntSeq, IntSeq)
    [function, total, no-evaluators]
  rule scanOutput(.IntSeq, _W:IntSeq, O:IntSeq) => O
    [simplification]
  rule scanOutput(iCons(32, R:IntSeq), W:IntSeq, O:IntSeq)
    => scanOutput(R, .IntSeq, emitWord(W, O))
    [simplification]
  rule scanOutput(iCons(C:Int, R:IntSeq), W:IntSeq, O:IntSeq)
    => scanOutput(R, seqConcat(W, iCons(C, .IntSeq)), O)
    requires C =/=Int 32
    [simplification]

  syntax IntSeq ::= scanWord(IntSeq, IntSeq)
    [function, total, no-evaluators]
  rule scanWord(.IntSeq, W:IntSeq) => W
    [simplification]
  rule scanWord(iCons(32, R:IntSeq), _W:IntSeq)
    => scanWord(R, .IntSeq)
    [simplification]
  rule scanWord(iCons(C:Int, R:IntSeq), W:IntSeq)
    => scanWord(R, seqConcat(W, iCons(C, .IntSeq)))
    requires C =/=Int 32
    [simplification]

  syntax IntSeq ::= scanLast(IntSeq, IntSeq)
    [function, total, no-evaluators]
  rule scanLast(.IntSeq, CH:IntSeq) => CH [simplification]
  rule scanLast(iCons(C:Int, R:IntSeq), _CH:IntSeq)
    => scanLast(R, iCons(C, .IntSeq))
    [simplification]

  syntax IntSeq ::= sentenceResult(IntSeq) [function, total]
  rule sentenceResult(CS:IntSeq)
    => revIS(
         trimWS(
           revIS(
             trimWS(
               emitWord(
                 scanWord(CS, .IntSeq),
                 scanOutput(CS, .IntSeq, .IntSeq))))))

endmodule
