requires "verification.k"

module GROUND-PROOF-EMPTY-BASE
  imports VERIFICATION-BASE

  claim [target]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "has_close_elements",
            Params("numbers", "threshold"),
            Assign(Name("result"), Bool(false))
            Assign(Name("i"), Int(0))
            Assign(Name("j"), Int(0))
            Assign(Name("elem"), Float(0.0))
            Assign(Name("elem2"), Float(0.0))
            For(
              Name("elem"),
              Name("numbers"),
              Assign(Name("j"), Int(0))
              For(
                Name("elem2"),
                Name("numbers"),
                If(
                  Compare(Name("i"), CmpOp("!=", Name("j"))),
                  If(
                    Compare(
                      Call(
                        Name("abs"),
                        BinOp("-", Name("elem"), Name("elem2"))
                      ),
                      CmpOp("<", Name("threshold"))
                    ),
                    Assign(Name("result"), Bool(true)),
                    .Stmts
                  ),
                  .Stmts
                )
                Assign(Name("j"), BinOp("+", Name("j"), Int(1)))
                Assign(Name("elem2"), Float(0.0))
              )
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              Assign(Name("j"), Int(0))
              Assign(Name("elem"), Float(0.0))
            )
            Return(Name("result"))
          )
        )
      )
      ~> Call(
           Name("has_close_elements"),
           list(floatVals(.FloatSeq)),
           0.5
         )
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "has_close_elements" |->
          closureVal(
            ("numbers", "threshold"),
            Assign(Name("result"), Bool(false))
            Assign(Name("i"), Int(0))
            Assign(Name("j"), Int(0))
            Assign(Name("elem"), Float(0.0))
            Assign(Name("elem2"), Float(0.0))
            For(
              Name("elem"),
              Name("numbers"),
              Assign(Name("j"), Int(0))
              For(
                Name("elem2"),
                Name("numbers"),
                If(
                  Compare(Name("i"), CmpOp("!=", Name("j"))),
                  If(
                    Compare(
                      Call(
                        Name("abs"),
                        BinOp("-", Name("elem"), Name("elem2"))
                      ),
                      CmpOp("<", Name("threshold"))
                    ),
                    Assign(Name("result"), Bool(true)),
                    .Stmts
                  ),
                  .Stmts
                )
                Assign(Name("j"), BinOp("+", Name("j"), Int(1)))
                Assign(Name("elem2"), Float(0.0))
              )
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              Assign(Name("j"), Int(0))
              Assign(Name("elem"), Float(0.0))
            )
            Return(Name("result")),
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
endmodule
