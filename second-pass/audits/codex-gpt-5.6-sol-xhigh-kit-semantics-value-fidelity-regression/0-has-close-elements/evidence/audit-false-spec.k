requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  claim [inner-loop]:
    <k>
      #loop(
        list(floatVals(REST:FloatSeq)),
        Name("elem2"),
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
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "numbers" |-> list(floatVals(ALL:FloatSeq))
        "threshold" |-> T:Float
        "result" |-> (
          R:Bool
          =>
          innerAcc(R, X:Float, I:Int, J:Int, REST, T)
        )
        "i" |-> I
        "j" |-> (J => J +Int floatLen(REST))
        "elem" |-> X
        "elem2" |-> 0.0,
        parent(0)
      )
      0 |-> scope("has_close_elements" |-> CLOSURE:Val, parent(-1))
      -1 |-> builtinsScope
    </scopes>

  claim [outer-loop]:
    <k>
      #loop(
        list(floatVals(REST:FloatSeq)),
        Name("elem"),
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
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "numbers" |-> list(floatVals(ALL:FloatSeq))
        "threshold" |-> T:Float
        "result" |-> (
          R:Bool
          =>
          outerAcc(R, I:Int, REST, ALL, T)
        )
        "i" |-> (I => I +Int floatLen(REST))
        "j" |-> 0
        "elem" |-> (0.0):Float
        "elem2" |-> (0.0):Float,
        parent(0)
      )
      0 |-> scope("has_close_elements" |-> CLOSURE:Val, parent(-1))
      -1 |-> builtinsScope
    </scopes>

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
           list(floatVals(INPUT:FloatSeq)),
           THRESHOLD:Float
         )
      =>
      true
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
