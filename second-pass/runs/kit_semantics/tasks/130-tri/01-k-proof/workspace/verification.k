requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT-SYNTAX

  syntax Int ::= triValue(Int) [function, total]
  syntax ValSeq ::= triComplete(ValSeq, Int, Int) [function, total]
                  | triResult(Int) [function, total]

  // Parse-time aliases for the exact translated implementation.
  syntax Expr ::= "triLoopCondition" [macro]
  rule triLoopCondition
    => Compare(Name("i"), CmpOp("<=", Name("n")))

  syntax Stmts ::= "triLoopBody" [macro]
  rule triLoopBody
    => If(Compare(Name("i"), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("values"), "append"), Int(1))),
          If(Compare(Name("i"), CmpOp("==", Int(1))),
            Expr(Call(Attribute(Name("values"), "append"), Int(3))),
            If(Compare(BinOp("%", Name("i"), Int(2)),
                       CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("values"), "append"),
                        BinOp("+", Int(1),
                                   BinOp("//", Name("i"), Int(2))))),
              Expr(Call(Attribute(Name("values"), "append"),
                        BinOp("*",
                          BinOp("+", BinOp("//", Name("i"), Int(2)), Int(1)),
                          BinOp("+", BinOp("//", Name("i"), Int(2)), Int(3))))))))
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= "triFunctionBody" [macro]
  rule triFunctionBody
    => Assign(Name("values"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       While(triLoopCondition, triLoopBody)
       Return(Name("values"))

  syntax Stmts ::= "triDefinition" [macro]
  rule triDefinition
    => FuncDef("tri", Params("n"), triFunctionBody)
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  // Mathematical value at an index. Negative indices are outside the task
  // domain; assigning them 0 makes this proof-local function total.
  rule triValue(I:Int) => 0
    requires I <Int 0
  rule triValue(I:Int)
    => ((I -Int pyMod(I, 2)) /Int 2 +Int 1)
       *Int ((I -Int pyMod(I, 2)) /Int 2 +Int 3)
    requires I >=Int 0 andBool pyMod(I, 2) ==Int 1
  rule triValue(I:Int)
    => 1 +Int (I -Int pyMod(I, 2)) /Int 2
    requires I >=Int 0 andBool pyMod(I, 2) ==Int 0

  // Complete an arbitrary prefix P by appending values I through N. The two
  // guards are disjoint and cover every integer I,N pair; recursion increases
  // I and therefore terminates after max(N-I+1, 0) steps.
  rule triComplete(P:ValSeq, I:Int, N:Int) => P
    requires I >Int N
  rule triComplete(P:ValSeq, I:Int, N:Int)
    => triComplete(
         valSeqConcat(P, vCons(triValue(I), .ValSeq)),
         I +Int 1,
         N)
    requires I <=Int N

  rule triResult(N:Int) => triComplete(.ValSeq, 0, N)
endmodule
