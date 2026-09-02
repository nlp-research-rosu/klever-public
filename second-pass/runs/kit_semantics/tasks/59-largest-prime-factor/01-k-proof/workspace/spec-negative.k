requires "verification.k"

module SPEC-NEGATIVE
  imports VERIFICATION

  claim [false-post]:
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
      ~> Call(Name("largest_prime_factor"), Int(4) , .Exprs)
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
    ensures ?RESULT ==Int 3

  claim [body-mutation]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_prime_factor",
            Params("n"),
            Assign(Name("factor"), Int(3))
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
      ~> Call(Name("largest_prime_factor"), Int(4) , .Exprs)
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
            Assign(Name("factor"), Int(3))
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
    ensures ?RESULT ==Int 2
endmodule
