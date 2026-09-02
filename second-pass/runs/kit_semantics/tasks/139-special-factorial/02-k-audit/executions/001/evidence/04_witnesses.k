requires "verification.k"

module AUDIT-WITNESSES
  imports VERIFICATION

  // A concrete state satisfying the loop claim's precondition:
  // N=4, I=1, F=1, R=1, L=1.
  claim [loop-precondition-witness-n4]:
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
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "n"         |-> 4
        "factorial" |-> (1 => 24)
        "result"    |-> (1 => 288)
        "i"         |-> (1 => 5),
        parent(0))
      ...
    </scopes>

  // A concrete state satisfying the entry claim's N>=1 precondition. The
  // destination is an independent ground result, not productAfter.
  claim [entry-precondition-witness-n4]:
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
      ~> Call(Name("special_factorial"), (4, .Exprs))
      => 288
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
endmodule
