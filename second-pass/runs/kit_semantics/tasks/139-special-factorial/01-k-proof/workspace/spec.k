requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(Compare(Name("i"), CmpOp("<=", Name("n"))),
        Assign(
          Name("factorial"),
          BinOp("*", Name("factorial"), Name("i")))
        Assign(
          Name("result"),
          BinOp("*", Name("result"), Name("factorial")))
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

  claim [special-factorial]:
    <k>
      #loadAll(Module(
        FuncDef("special_factorial", Params("n"),
          Assign(Name("factorial"), Int(1))
          Assign(Name("result"), Int(1))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            Assign(
              Name("factorial"),
              BinOp("*", Name("factorial"), Name("i")))
            Assign(
              Name("result"),
              BinOp("*", Name("result"), Name("factorial")))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
          Return(Name("result")))))
      ~> Call(Name("special_factorial"), (N:Int, .Exprs))
      => productAfter(1, N, 1, 1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "special_factorial" |->
             closureVal(
               ("n", .ParamNames),
               Assign(Name("factorial"), Int(1))
               Assign(Name("result"), Int(1))
               Assign(Name("i"), Int(1))
               While(Compare(Name("i"), CmpOp("<=", Name("n"))),
                 Assign(
                   Name("factorial"),
                   BinOp("*", Name("factorial"), Name("i")))
                 Assign(
                   Name("result"),
                   BinOp("*", Name("result"), Name("factorial")))
                 Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
               Return(Name("result")),
               0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
endmodule
