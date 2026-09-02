requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // This claim deliberately changes the source update to
  // result = result * factorial + 1 while retaining the original summary.
  claim [false-loop-invariant]:
    <k>
      #while(Compare(Name("i"), CmpOp("<=", Name("n"))),
        Assign(
          Name("factorial"),
          BinOp("*", Name("factorial"), Name("i")))
        Assign(
          Name("result"),
          BinOp("+",
            BinOp("*", Name("result"), Name("factorial")),
            Int(1)))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "n"         |-> N:Int
        "factorial" |-> (F:Int => factorialAfter(I, N, F))
        "result"    |-> (R:Int => productAfter(I, N, F, R))
        "i"         |-> (I:Int => N +Int 1),
        _P:Parent)
      ...
    </scopes>
    requires N >=Int 1
      andBool I >=Int 1
      andBool I <=Int N +Int 1
endmodule
