requires "verification.k"

module CUBE-SPEC
  imports VERIFICATION

  // Inductive loop invariant when the normalized input is exactly N^3.
  claim [cube-loop]:
    <k>
      While(Compare(
        BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
        CmpOp("<", Name("a"))),
        Assign(Name("n"), BinOp("+", Name("n"), Int(1))))
      => .K
      ...
    </k>
    <env>
      "a" |-> IntVal(cube(N))
      "n" |-> (IntVal(I) => IntVal(N))
    </env>
    requires 0 <=Int I andBool I <=Int N

  // Every nonnegative cube is accepted by the translated program.
  claim [nonnegative-cube]:
    <k>
      iscubeProgram ~> invoke(IntVal(cube(N))) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(true) ~> .K </result>
    requires 0 <=Int N

  // Negative cubes normalize to their positive magnitude and are accepted.
  claim [negative-cube]:
    <k>
      iscubeProgram ~> invoke(IntVal(0 -Int cube(N))) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(true) ~> .K </result>
    requires 0 <Int N
endmodule

module GAP-SPEC
  imports GAP-VERIFICATION

  // The loop stops at N+1 for an input strictly between N^3 and (N+1)^3.
  claim [gap-loop]:
    <k>
      While(Compare(
        BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
        CmpOp("<", Name("a"))),
        Assign(Name("n"), BinOp("+", Name("n"), Int(1))))
      => .K
      ...
    </k>
    <env>
      "a" |-> IntVal(cube(N) +Int D)
      "n" |-> (IntVal(I) => IntVal(N +Int 1))
    </env>
    requires 0 <=Int I
     andBool I <=Int N +Int 1
     andBool 0 <=Int N
     andBool 0 <Int D
     andBool D <Int cube(N +Int 1) -Int cube(N)

  // Every positive non-cube lies strictly between two consecutive cubes.
  claim [positive-noncube]:
    <k>
      iscubeProgram ~> invoke(IntVal(cube(N) +Int D)) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(false) ~> .K </result>
    requires 0 <=Int N
     andBool 0 <Int D
     andBool D <Int cube(N +Int 1) -Int cube(N)

  // The corresponding negative non-cubes normalize to the same magnitude.
  claim [negative-noncube]:
    <k>
      iscubeProgram ~> invoke(IntVal(0 -Int (cube(N) +Int D))) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(false) ~> .K </result>
    requires 0 <=Int N
     andBool 0 <Int D
     andBool D <Int cube(N +Int 1) -Int cube(N)
endmodule
