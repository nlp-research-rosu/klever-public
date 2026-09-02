requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The generated solution.mpy term, followed by a call of its public entry point.
  syntax KItem ::= "#getOddCollatz" "(" Int ")"
  rule #getOddCollatz(N:Int)
    => #loadAll(
         Module(
           FuncDef("get_odd_collatz", Params("n"),
             Assign(Name("odd_numbers"), ListExpr(.Exprs))
             While(Compare(Name("n"), CmpOp("!=", Int(1))),
               If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
                 Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
                 Assign(
                   Name("n"),
                   BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
                 Assign(Name("n"), BinOp("//", Name("n"), Int(2)))))
             Expr(Call(Attribute(Name("odd_numbers"), "append"), Int(1)))
             Return(Call(Name("sorted"), Name("odd_numbers"))))))
       ~> Call(Name("get_odd_collatz"), Int(N), .Exprs)

  // Functional specification of the unsorted odd Collatz values.  The
  // accumulator form mirrors the loop invariant.  These equations deliberately
  // express partial correctness: their unfolding follows the same Collatz
  // transition as the program and therefore does not assume the conjecture.
  syntax ValSeq ::= collatzResult(Int, ValSeq) [function]

  rule collatzResult(1, A:ValSeq)
    => valSeqConcat(A, vCons(1, .ValSeq))

  rule collatzResult(N:Int, A:ValSeq)
    => collatzResult(
         3 *Int N +Int 1,
         valSeqConcat(A, vCons(N, .ValSeq)))
    requires N =/=Int 1 andBool pyMod(N, 2) ==Int 1

  rule collatzResult(N:Int, A:ValSeq)
    => collatzResult((N -Int pyMod(N, 2)) /Int 2, A)
    requires N =/=Int 1 andBool notBool (pyMod(N, 2) ==Int 1)

  // The exact closure installed by loading solution.mpy.  This abbreviation
  // keeps concrete end-to-end claims readable.
  syntax Val ::= "getOddCollatzClosure" [function]
  rule getOddCollatzClosure
    => closureVal(
         "n", .ParamNames,
         Assign(Name("odd_numbers"), ListExpr(.Exprs))
         While(Compare(Name("n"), CmpOp("!=", Int(1))),
           If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
             Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
             Assign(
               Name("n"),
               BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
             Assign(Name("n"), BinOp("//", Name("n"), Int(2)))))
         Expr(Call(Attribute(Name("odd_numbers"), "append"), Int(1)))
         Return(Call(Name("sorted"), Name("odd_numbers"))),
         0)
endmodule
