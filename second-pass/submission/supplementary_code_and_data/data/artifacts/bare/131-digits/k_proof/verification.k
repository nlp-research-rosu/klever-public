requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTICS
  imports BOOL

  syntax KItem ::= "CheckProgram" "(" Program "," Program ")"
                 | "ProgramsMatch"

  // The exact condition and body of the loop emitted in solution.mpy.
  syntax Expr ::= "digitsCond" [function, total]
  rule digitsCond
    => Compare(Name("n"), CmpOp(">", Int(0)))

  syntax Stmts ::= "digitsLoopBody" [function, total]
  rule digitsLoopBody
    => Assign(Name("digit"), BinOp("%", Name("n"), Int(10)))
       If(Compare(BinOp("%", Name("digit"), Int(2)),
                  CmpOp("==", Int(1))),
          If(Compare(Name("result"), CmpOp("==", Int(0))),
             Assign(Name("result"), Name("digit")),
             Assign(Name("result"),
                    BinOp("*", Name("result"), Name("digit")))),
          .Stmts)
       Assign(Name("n"), BinOp("//", Name("n"), Int(10)))

  // This is a constructor-for-constructor copy of solution.mpy.  Keeping it
  // here makes the program a closed term that can occur in reachability claims.
  syntax Program ::= "SolutionProgram" [function, total]
  rule SolutionProgram
    => Module(
         FuncDef("digits", Params("n"),
           Assign(Name("result"), Int(0))
           While(digitsCond, digitsLoopBody)
           Return(Name("result"))))

  // Used by prove.sh to compare the generated .mpy tree structurally with
  // the closed program term above, after SolutionProgram expands.
  rule CheckProgram(P, P) => ProgramsMatch

  // Extend accumulator A with decimal digit D.  Zero is the sentinel for
  // "no odd digit seen"; decimal odd digits themselves are never zero.
  syntax Int ::= addOddDigit(Int, Int) [function, total]
  rule addOddDigit(A, D) => A
    requires D %Int 2 ==Int 0
  rule addOddDigit(A, D) => D
    requires (D %Int 2 =/=Int 0) andBool (A ==Int 0)
  rule addOddDigit(A, D) => A *Int D
    requires (D %Int 2 =/=Int 0) andBool (A =/=Int 0)

  // Fold the remaining base-10 digits of N into A, least-significant first.
  syntax Int ::= oddProductFrom(Int, Int) [function, total]
  rule oddProductFrom(N, A) => A
    requires N <=Int 0
  rule oddProductFrom(N, A)
    => oddProductFrom(N /Int 10, addOddDigit(A, N %Int 10))
    requires N >Int 0

  syntax Int ::= oddProduct(Int) [function, total]
  rule oddProduct(N) => oddProductFrom(N, 0)

  // The digit cell is operational scratch state, but tracking its exact final
  // value makes the loop invariant cover the entire configuration.
  syntax Int ::= finalScratchDigit(Int, Int) [function, total]
  rule finalScratchDigit(N, D) => D
    requires N <=Int 0
  rule finalScratchDigit(N, _D)
    => finalScratchDigit(N /Int 10, N %Int 10)
    requires N >Int 0
endmodule
