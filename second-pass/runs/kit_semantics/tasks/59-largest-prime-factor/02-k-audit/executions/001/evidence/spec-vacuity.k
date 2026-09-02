requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [loop]:
    <k>
      #while(
        Compare(Name("n"), CmpOp(">", Name("factor"))),
        If(
          Compare(
            BinOp("%", Name("n"), Name("factor")),
            CmpOp("==", Int(0))
          ),
          Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))) .Stmts,
          Assign(Name("factor"), BinOp("+", Name("factor"), Int(1))) .Stmts
        ) .Stmts
      )
      ~> Return(Name("n")) .Stmts
      ~> #endcall
      ~> .K
      => ?RESULT:Int
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (
      -1 |-> builtinsScope
      0 |-> scope(
        "largest_prime_factor" |->
          closureVal(
            "n" , .ParamNames,
            Assign(Name("factor"), Int(2))
            While(
              Compare(Name("n"), CmpOp(">", Name("factor"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("factor")),
                  CmpOp("==", Int(0))
                ),
                Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))) .Stmts,
                Assign(Name("factor"), BinOp("+", Name("factor"), Int(1))) .Stmts
              ) .Stmts
            )
            Return(Name("n"))
            .Stmts,
            0
          ),
        parent(-1)
      )
      1 |-> scope(
        "factor" |-> F:Int
        "n" |-> N:Int,
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "largest_prime_factor" |->
          closureVal(
            "n" , .ParamNames,
            Assign(Name("factor"), Int(2))
            While(
              Compare(Name("n"), CmpOp(">", Name("factor"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("factor")),
                  CmpOp("==", Int(0))
                ),
                Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))) .Stmts,
                Assign(Name("factor"), BinOp("+", Name("factor"), Int(1))) .Stmts
              ) .Stmts
            )
            Return(Name("n"))
            .Stmts,
            0
          ),
        parent(-1)
      )
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires F >=Int 2
    ensures ?RESULT ==Int lpfFrom(N, F)

  claim [entry]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_prime_factor",
            Params("n"),
            Assign(Name("factor"), Int(2))
            While(
              Compare(Name("n"), CmpOp(">", Name("factor"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("factor")),
                  CmpOp("==", Int(0))
                ),
                Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))) .Stmts,
                Assign(Name("factor"), BinOp("+", Name("factor"), Int(1))) .Stmts
              ) .Stmts
            )
            Return(Name("n"))
            .Stmts
          )
          .Stmts
        )
      )
      ~> Call(Name("largest_prime_factor"), Int(N0:Int) , .Exprs)
      => ?RESULT:Int
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_prime_factor" |->
          closureVal(
            "n" , .ParamNames,
            Assign(Name("factor"), Int(2))
            While(
              Compare(Name("n"), CmpOp(">", Name("factor"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("factor")),
                  CmpOp("==", Int(0))
                ),
                Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))) .Stmts,
                Assign(Name("factor"), BinOp("+", Name("factor"), Int(1))) .Stmts
              ) .Stmts
            )
            Return(Name("n"))
            .Stmts,
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N0 ==Int 15
    ensures ?RESULT ==Int lpfFrom(N0, 2) +Int 1
endmodule
