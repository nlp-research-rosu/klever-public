requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTICS
  imports MAP-SYMBOLIC

  // A compact name for the exact AST emitted in solution.mpy.  Both krun and
  // kprove therefore execute the same constructor-level program.
  syntax Stmt ::= "solutionLoop" [macro]
  rule solutionLoop =>
    While(Compare(Name("i"), CmpOp("<", Name("k"))),
      Assign(Name("value"), Subscript(Name("arr"), Name("i")))
      If(BoolOp(
        "and",
        Compare(UnaryOp("-", Int(100)), CmpOp("<", Name("value"))),
        Compare(Name("value"), CmpOp("<", Int(100)))),
        Assign(Name("total"), BinOp("+", Name("total"), Int(1))),
        .Stmts)
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))

  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(FuncDef("add_elements", Params("arr", "k"),
      Assign(Name("total"), Int(0))
      Assign(Name("i"), Int(0))
      Assign(Name("value"), Int(0))
      solutionLoop
      Return(Name("total"))))

  // Mathematical contract: the contribution of one integer, followed by the
  // sum of contributions at positions [I, K).  These equations are independent
  // of the implementation's loop and conditional control flow.
  syntax Int ::= "smallContribution" "(" Int ")" [function, total]
  rule smallContribution(I) => I
    requires -100 <Int I andBool I <Int 100
  rule smallContribution(I) => 0
    requires I <=Int -100 orBool I >=Int 100

  syntax Int ::= "sumRange" "(" List "," Int "," Int ")" [function, total]
  rule sumRange(_A, I, K) => 0
    requires I >=Int K
  rule sumRange(A, I, K) =>
    smallContribution(intAt(A, I)) +Int sumRange(A, I +Int 1, K)
    requires I <Int K
endmodule
