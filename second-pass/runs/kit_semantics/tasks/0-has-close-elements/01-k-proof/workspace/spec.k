requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [inner-loop]:
    <k>
      #loop(list(REM:ValSeq), Name("number2"),
        If(Compare(Name("i"), CmpOp("<", Name("j"))),
          If(
            Compare(
              Call(Name("abs"),
                BinOp("-", Name("number1"), Name("number2"))),
              CmpOp("<", Name("threshold"))),
            Assign(Name("found"), Bool(true)),
            .Stmts),
          .Stmts)
        Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0  |-> scope("has_close_elements" |-> _CLOSURE:Val, parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
        "numbers"  |-> list(VS:ValSeq)
        "threshold"|-> T:Float
        "found"    |-> (B:Bool =>
                         rowAcc(B, asFloat(A), T, I, J, REM))
        "i"        |-> I:Int
        "j"        |-> (J:Int => ?JFinal:Int)
        "number1"  |-> A:Val
        "number2"  |-> (_OLD:Val => ?LAST:Val),
        parent(0))
    </scopes>
    <heap> .Map </heap>
    requires allFloats(VS)
     andBool allFloats(REM)
     andBool isFloat(A)
     andBool 0 <=Int I
     andBool 0 <=Int J

  claim [outer-loop]:
    <k>
      #loop(list(REM:ValSeq), Name("number1"),
        Assign(Name("j"), Int(0))
        For(Name("number2"), Name("numbers"),
          If(Compare(Name("i"), CmpOp("<", Name("j"))),
            If(
              Compare(
                Call(Name("abs"),
                  BinOp("-", Name("number1"), Name("number2"))),
                CmpOp("<", Name("threshold"))),
              Assign(Name("found"), Bool(true)),
              .Stmts),
            .Stmts)
          Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0  |-> scope("has_close_elements" |-> _CLOSURE:Val, parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
        "numbers"  |-> list(VS:ValSeq)
        "threshold"|-> T:Float
        "found"    |-> (B:Bool => outerAcc(B, VS, T, I, REM))
        "i"        |-> (I:Int => I +Int vsLen(REM))
        "j"        |-> (_J:Int => ?JFinal:Int)
        "number1"  |-> (_N1:Val => ?N1Final:Val)
        "number2"  |-> (_N2:Val => ?N2Final:Val),
        parent(0))
    </scopes>
    <heap> .Map </heap>
    requires allFloats(VS)
     andBool allFloats(REM)
     andBool 0 <=Int I

  claim [has-close-elements]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef("has_close_elements", Params("numbers", "threshold"),
            Assign(Name("found"), Bool(false))
            Assign(Name("i"), Int(0))
            Assign(Name("j"), Int(0))
            Assign(Name("number1"), Float(0.0))
            Assign(Name("number2"), Float(0.0))
            For(Name("number1"), Name("numbers"),
              Assign(Name("j"), Int(0))
              For(Name("number2"), Name("numbers"),
                If(Compare(Name("i"), CmpOp("<", Name("j"))),
                  If(
                    Compare(
                      Call(Name("abs"),
                        BinOp("-", Name("number1"), Name("number2"))),
                      CmpOp("<", Name("threshold"))),
                    Assign(Name("found"), Bool(true)),
                    .Stmts),
                  .Stmts)
                Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
            Return(Name("found")))))
      ~> Call(Name("has_close_elements"), list(VS:ValSeq), T:Float)
      => outerAcc(false, VS, T, 0, VS)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
              "has_close_elements" |->
                closureVal(
                  ("numbers", "threshold"),
                  Assign(Name("found"), Bool(false))
                  Assign(Name("i"), Int(0))
                  Assign(Name("j"), Int(0))
                  Assign(Name("number1"), Float(0.0))
                  Assign(Name("number2"), Float(0.0))
                  For(Name("number1"), Name("numbers"),
                    Assign(Name("j"), Int(0))
                    For(Name("number2"), Name("numbers"),
                      If(Compare(Name("i"), CmpOp("<", Name("j"))),
                        If(
                          Compare(
                            Call(Name("abs"),
                              BinOp("-",
                                Name("number1"), Name("number2"))),
                            CmpOp("<", Name("threshold"))),
                          Assign(Name("found"), Bool(true)),
                          .Stmts),
                        .Stmts)
                      Assign(Name("j"),
                        BinOp("+", Name("j"), Int(1))))
                    Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
                  Return(Name("found")),
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
    requires allFloats(VS)
endmodule
