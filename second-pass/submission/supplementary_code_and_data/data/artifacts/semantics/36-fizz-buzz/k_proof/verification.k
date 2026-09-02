requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A direct mathematical reading of the prompt: recursively inspect the
  // base-10 digits of each selected non-negative integer.
  syntax Bool ::= divisibleBy11Or13(Int) [function, total]
  rule divisibleBy11Or13(I:Int)
    => pyMod(I, 11) ==Int 0 orBool pyMod(I, 13) ==Int 0

  syntax Int ::= countSevensAcc(Int, Int) [function]
  rule countSevensAcc(A:Int, 0) => A [simplification]
  rule countSevensAcc(A:Int, I:Int)
    => countSevensAcc(
         A +Int 1,
         (I -Int pyMod(I, 10)) /Int 10)
    requires I >Int 0 andBool pyMod(I, 10) ==Int 7
    [simplification]
  rule countSevensAcc(A:Int, I:Int)
    => countSevensAcc(A, (I -Int pyMod(I, 10)) /Int 10)
    requires I >Int 0 andBool pyMod(I, 10) =/=Int 7
    [simplification]

  // Accumulate the selected digit counts over the half-open interval [I,N).
  syntax Int ::= fizzBuzzAcc(Int, Int, Int) [function]
  rule fizzBuzzAcc(A:Int, I:Int, N:Int) => A
    requires I >=Int N
  rule fizzBuzzAcc(A:Int, I:Int, N:Int)
    => fizzBuzzAcc(countSevensAcc(A, I), I +Int 1, N)
    requires I <Int N andBool divisibleBy11Or13(I)
  rule fizzBuzzAcc(A:Int, I:Int, N:Int)
    => fizzBuzzAcc(A, I +Int 1, N)
    requires I <Int N andBool notBool divisibleBy11Or13(I)

  syntax Int ::= fizzBuzzSpec(Int) [function, total]
  rule fizzBuzzSpec(N:Int) => fizzBuzzAcc(0, 0, N)

  // Exact AST fragments emitted by py2mpy.py for solution.py.  Keeping them
  // named makes the loop-invariant claims in spec.k readable.
  syntax Stmts ::= "INNER-BODY" [macro]
  rule INNER-BODY
    => If(Compare(BinOp("%", Name("x"), Int(10)), CmpOp("==", Int(7))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts)
       Assign(Name("x"), BinOp("//", Name("x"), Int(10)))

  syntax Stmts ::= "OUTER-BODY" [macro]
  rule OUTER-BODY
    => If(BoolOp(
            "or",
            Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
            Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
          Assign(Name("x"), Name("i"))
          While(Compare(Name("x"), CmpOp(">", Int(0))), INNER-BODY),
          .Stmts)
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmt ::= "FIZZ-BUZZ-DEF" [macro]
  rule FIZZ-BUZZ-DEF
    => FuncDef(
         "fizz_buzz",
         Params("n"),
         Assign(Name("count"), Int(0))
         Assign(Name("i"), Int(0))
         Assign(Name("x"), Int(0))
         While(Compare(Name("i"), CmpOp("<", Name("n"))), OUTER-BODY)
         Return(Name("count")))

  syntax Val ::= "FIZZ-BUZZ-CLOSURE" [macro]
  rule FIZZ-BUZZ-CLOSURE
    => closureVal(
         "n",
         Assign(Name("count"), Int(0))
         Assign(Name("i"), Int(0))
         Assign(Name("x"), Int(0))
         While(Compare(Name("i"), CmpOp("<", Name("n"))), OUTER-BODY)
         Return(Name("count")),
         0)
endmodule
