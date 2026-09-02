requires "verification.k"

module NUMERICAL-LETTER-GRADE-SPEC
  imports NUMERICAL-LETTER-GRADE-VERIFICATION

  // ---- Append invariant, variant B (gpa bound; circularity). Fixed ref: the
  // body never allocates.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("gpa"),
        If(Compare(Name("gpa"), CmpOp("==", Float(4.0))),
                Expr(Call(Attribute(Name("letter_grade"), "append"), Str("A+"))),
                If(Compare(Name("gpa"), CmpOp(">", Float(3.7))),
                  Expr(
                    Call(Attribute(Name("letter_grade"), "append"), Str("A"))),
                  If(Compare(Name("gpa"), CmpOp(">", Float(3.3))),
                    Expr(
                      Call(Attribute(Name("letter_grade"), "append"), Str("A-"))),
                    If(Compare(Name("gpa"), CmpOp(">", Float(3.0))),
                      Expr(
                        Call(
                          Attribute(Name("letter_grade"), "append"),
                          Str("B+"))),
                      If(Compare(Name("gpa"), CmpOp(">", Float(2.7))),
                        Expr(
                          Call(
                            Attribute(Name("letter_grade"), "append"),
                            Str("B"))),
                        If(Compare(Name("gpa"), CmpOp(">", Float(2.3))),
                          Expr(
                            Call(
                              Attribute(Name("letter_grade"), "append"),
                              Str("B-"))),
                          If(Compare(Name("gpa"), CmpOp(">", Float(2.0))),
                            Expr(
                              Call(
                                Attribute(Name("letter_grade"), "append"),
                                Str("C+"))),
                            If(Compare(Name("gpa"), CmpOp(">", Float(1.7))),
                              Expr(
                                Call(
                                  Attribute(Name("letter_grade"), "append"),
                                  Str("C"))),
                              If(Compare(Name("gpa"), CmpOp(">", Float(1.3))),
                                Expr(
                                  Call(
                                    Attribute(Name("letter_grade"), "append"),
                                    Str("C-"))),
                                If(Compare(Name("gpa"), CmpOp(">", Float(1.0))),
                                  Expr(
                                    Call(
                                      Attribute(Name("letter_grade"), "append"),
                                      Str("D+"))),
                                  If(Compare(Name("gpa"), CmpOp(">", Float(0.7))),
                                    Expr(
                                      Call(
                                        Attribute(
                                          Name("letter_grade"),
                                          "append"),
                                        Str("D"))),
                                    If(Compare(Name("gpa"), CmpOp(">", Float(0.0))),
                                      Expr(
                                        Call(
                                          Attribute(
                                            Name("letter_grade"),
                                            "append"),
                                          Str("D-"))),
                                      Expr(
                                        Call(
                                          Attribute(
                                            Name("letter_grade"),
                                            "append"),
                                          Str("E"))))))))))))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "numerical_letter_grade" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "grades" <- GV:Val ] [ "letter_grade" <- ref(AR:Int) ]
                    [ "gpa" <- _:Val ], parent(0)) =>
         scope(.Map [ "grades" <- GV ] [ "letter_grade" <- ref(AR) ]
                    [ "gpa" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(gradeFold(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS)
    [all-path]

  // ---- Variant A (pre-first-iteration).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("gpa"),
        If(Compare(Name("gpa"), CmpOp("==", Float(4.0))),
                Expr(Call(Attribute(Name("letter_grade"), "append"), Str("A+"))),
                If(Compare(Name("gpa"), CmpOp(">", Float(3.7))),
                  Expr(
                    Call(Attribute(Name("letter_grade"), "append"), Str("A"))),
                  If(Compare(Name("gpa"), CmpOp(">", Float(3.3))),
                    Expr(
                      Call(Attribute(Name("letter_grade"), "append"), Str("A-"))),
                    If(Compare(Name("gpa"), CmpOp(">", Float(3.0))),
                      Expr(
                        Call(
                          Attribute(Name("letter_grade"), "append"),
                          Str("B+"))),
                      If(Compare(Name("gpa"), CmpOp(">", Float(2.7))),
                        Expr(
                          Call(
                            Attribute(Name("letter_grade"), "append"),
                            Str("B"))),
                        If(Compare(Name("gpa"), CmpOp(">", Float(2.3))),
                          Expr(
                            Call(
                              Attribute(Name("letter_grade"), "append"),
                              Str("B-"))),
                          If(Compare(Name("gpa"), CmpOp(">", Float(2.0))),
                            Expr(
                              Call(
                                Attribute(Name("letter_grade"), "append"),
                                Str("C+"))),
                            If(Compare(Name("gpa"), CmpOp(">", Float(1.7))),
                              Expr(
                                Call(
                                  Attribute(Name("letter_grade"), "append"),
                                  Str("C"))),
                              If(Compare(Name("gpa"), CmpOp(">", Float(1.3))),
                                Expr(
                                  Call(
                                    Attribute(Name("letter_grade"), "append"),
                                    Str("C-"))),
                                If(Compare(Name("gpa"), CmpOp(">", Float(1.0))),
                                  Expr(
                                    Call(
                                      Attribute(Name("letter_grade"), "append"),
                                      Str("D+"))),
                                  If(Compare(Name("gpa"), CmpOp(">", Float(0.7))),
                                    Expr(
                                      Call(
                                        Attribute(
                                          Name("letter_grade"),
                                          "append"),
                                        Str("D"))),
                                    If(Compare(Name("gpa"), CmpOp(">", Float(0.0))),
                                      Expr(
                                        Call(
                                          Attribute(
                                            Name("letter_grade"),
                                            "append"),
                                          Str("D-"))),
                                      Expr(
                                        Call(
                                          Attribute(
                                            Name("letter_grade"),
                                            "append"),
                                          Str("E"))))))))))))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "numerical_letter_grade" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "grades" <- GV:Val ] [ "letter_grade" <- ref(AR:Int) ], parent(0)) =>
         scope(.Map [ "grades" <- GV ] [ "letter_grade" <- ref(AR) ]
                    [ "gpa" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(gradeFold(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS) andBool 0 <Int vsLen(VS)
    [all-path]

  // ---- Entry — the REAL canonical code, verbatim .mpy.
  claim
    <k>
      FuncDef("numerical_letter_grade", Params("grades"),
          Assign(Name("letter_grade"), ListExpr(.Exprs))
          For(Name("gpa"), Name("grades"),
            If(Compare(Name("gpa"), CmpOp("==", Float(4.0))),
              Expr(Call(Attribute(Name("letter_grade"), "append"), Str("A+"))),
              If(Compare(Name("gpa"), CmpOp(">", Float(3.7))),
                Expr(
                  Call(Attribute(Name("letter_grade"), "append"), Str("A"))),
                If(Compare(Name("gpa"), CmpOp(">", Float(3.3))),
                  Expr(
                    Call(Attribute(Name("letter_grade"), "append"), Str("A-"))),
                  If(Compare(Name("gpa"), CmpOp(">", Float(3.0))),
                    Expr(
                      Call(
                        Attribute(Name("letter_grade"), "append"),
                        Str("B+"))),
                    If(Compare(Name("gpa"), CmpOp(">", Float(2.7))),
                      Expr(
                        Call(
                          Attribute(Name("letter_grade"), "append"),
                          Str("B"))),
                      If(Compare(Name("gpa"), CmpOp(">", Float(2.3))),
                        Expr(
                          Call(
                            Attribute(Name("letter_grade"), "append"),
                            Str("B-"))),
                        If(Compare(Name("gpa"), CmpOp(">", Float(2.0))),
                          Expr(
                            Call(
                              Attribute(Name("letter_grade"), "append"),
                              Str("C+"))),
                          If(Compare(Name("gpa"), CmpOp(">", Float(1.7))),
                            Expr(
                              Call(
                                Attribute(Name("letter_grade"), "append"),
                                Str("C"))),
                            If(Compare(Name("gpa"), CmpOp(">", Float(1.3))),
                              Expr(
                                Call(
                                  Attribute(Name("letter_grade"), "append"),
                                  Str("C-"))),
                              If(Compare(Name("gpa"), CmpOp(">", Float(1.0))),
                                Expr(
                                  Call(
                                    Attribute(Name("letter_grade"), "append"),
                                    Str("D+"))),
                                If(Compare(Name("gpa"), CmpOp(">", Float(0.7))),
                                  Expr(
                                    Call(
                                      Attribute(
                                        Name("letter_grade"),
                                        "append"),
                                      Str("D"))),
                                  If(Compare(Name("gpa"), CmpOp(">", Float(0.0))),
                                    Expr(
                                      Call(
                                        Attribute(
                                          Name("letter_grade"),
                                          "append"),
                                        Str("D-"))),
                                    Expr(
                                      Call(
                                        Attribute(
                                          Name("letter_grade"),
                                          "append"),
                                        Str("E"))))))))))))))))
          Return(Name("letter_grade")))
      Assign(Name("result"), Call(Name("numerical_letter_grade"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "numerical_letter_grade" <- ?_:Val ]
                       [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(gradeFold(VS, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS) andBool 0 <Int vsLen(VS)
    [all-path]
endmodule
