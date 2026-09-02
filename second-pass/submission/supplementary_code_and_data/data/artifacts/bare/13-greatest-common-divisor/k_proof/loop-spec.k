requires "loop-verification.k"

module LOOP-SPEC
  imports LOOP-VERIFICATION

  claim
    <k>
      execStmt(While(
        Compare(Name("b"), CmpOp("!=", Int(0))),
        Assign(Name("r"), BinOp("%", Name("a"), Name("b")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("r"))
      ))
      => .K
    </k>
    <env>
      ("a" |-> A) ("b" |-> B) ("r" |-> R0:Int)
      => ("a" |-> gcdSpec(A, B)) ("b" |-> 0)
         ("r" |-> finalR(B, R0))
    </env>
    requires (A >=Int 0) andBool (B >=Int 0)
endmodule
