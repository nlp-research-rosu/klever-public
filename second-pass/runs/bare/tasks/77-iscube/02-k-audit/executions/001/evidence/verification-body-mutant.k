requires "semantic.k"

module VERIFICATION
  imports MPY
  imports K-EQUAL
  imports MAP-SYMBOLIC

  // A compact name for exactly the constructor tree in solution.mpy.  The
  // rule only abbreviates that tree; execution still uses the MPY rules.
  syntax Pgm ::= "iscubeProgram"
  rule iscubeProgram =>
    Module(
      FuncDef("iscube", Params("a"),
        If(Compare(Name("a"), CmpOp("<", Int(0))),
          Assign(Name("a"), UnaryOp("-", Name("a"))),
          .Stmts)
        Assign(Name("n"), Int(0))
        While(Compare(
          BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
          CmpOp("<", Name("a"))),
          Assign(Name("n"), BinOp("+", Name("n"), Int(1))))
        Return(Compare(
          BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
          CmpOp("<", Name("a"))))))

  syntax Int ::= "cube" "(" Int ")" [function, total]
  rule cube(I) => I *Int I *Int I
endmodule

module GAP-VERIFICATION
  imports VERIFICATION

  // Nonlinear integer arithmetic is incomplete in SMT solvers.  These two
  // valid monotonic-cube lemmas supply exactly the missing induction facts for
  // the open interval N^3 < A < (N+1)^3; they do not summarize the loop.
  rule I <Int N +Int 1 => true
    requires 0 <=Int I
     andBool I <=Int N +Int 1
     andBool 0 <=Int N
     andBool 0 <Int D
     andBool D <Int ((N +Int 1) *Int (N +Int 1) *Int (N +Int 1))
                       -Int (N *Int N *Int N)
     andBool (I *Int I *Int I) <Int (N *Int N *Int N) +Int D
    [simplification]

  rule I ==Int N +Int 1 => true
    requires 0 <=Int I
     andBool I <=Int N +Int 1
     andBool 0 <=Int N
     andBool 0 <Int D
     andBool D <Int ((N +Int 1) *Int (N +Int 1) *Int (N +Int 1))
                       -Int (N *Int N *Int N)
     andBool (I *Int I *Int I) >=Int (N *Int N *Int N) +Int D
    [simplification]
endmodule
